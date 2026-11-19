"""Schmidhuber-style artificial curiosity for CTMV, tested on the generated vaults.
Idea: the vault is a data stream and the 'compressor' is the set of patterns (abstractions) the model knows.
A hypothesis ("note x is an instance of pattern p") is worth testing when accepting it shortens the description of the vault:
   progress(x, p) = bits to code x's shape on its own  -  bits to code it as 'p plus a small residual'  -  bits for the label.
Noise has no learnable shape, so its progress is never positive (Schmidhuber's point: be curious about what is learnable, not what is surprising).
Leaps happen in two ways: (1) transfer: known patterns are recognised in domains where they were never seen; (2) invention: a group of
unexplained notes that share one new shape is proposed as a new pattern (an abstraction nobody named).
Usage: python3 curiosity.py VAULT_DIR OUT_JSON [--model bge] [--seed-domains 2]"""
import json, sys, glob, random, math
import numpy as np

def centre(X, doms):
    """remove the part of each vector that is shared by its whole domain: what is left is the 'shape' of the note"""
    X = X.copy()
    for d in set(doms):
        idx = [i for i, x in enumerate(doms) if x == d]
        X[idx] -= X[idx].mean(axis=0)
    n = np.linalg.norm(X, axis=1, keepdims=True); return X / np.where(n == 0, 1, n)

def run(V, model='bge', seed_domains=2, rng=None, label_bits=3.0, sigma_scale=1.0, hold_out_pattern=None, max_rounds=60, min_margin=0.5):
    names = [n['name'] for n in V['notes']]; dom = {n['name']: n['domain'] for n in V['notes']}
    truth = V['truth']['pattern_of']
    X = np.array([V['vec'][model][n] for n in names]); X /= np.linalg.norm(X, axis=1, keepdims=True)
    # domain for centring: only real domains; meta notes (opinions, filler about other things) are centred together
    Xc = centre(X, [dom[n] for n in names])
    doms = sorted({dom[n] for n in names if n in truth and dom[n] != 'meta'}); rng = rng or random.Random(0); rng.shuffle(doms)
    seed_d = set(doms[:seed_domains])
    known = {n: truth[n] for n in names if n in truth and dom[n] in seed_d and truth[n] != hold_out_pattern}
    idx = {n: i for i, n in enumerate(names)}
    unl = [n for n in names if n not in known and dom[n] != 'meta']          # candidates (the vault's own domains)
    log = []
    def protos(kn):
        P = {}
        for p in sorted(set(kn.values())):
            M = Xc[[idx[n] for n, q in kn.items() if q == p]]; c = M.mean(axis=0); P[p] = c / (np.linalg.norm(c) or 1)
        return P
    P = protos(known)
    # noise level: residual of known notes around their own prototype (what 'an instance of p' looks like)
    def resid(kn, P): return np.array([1 - Xc[idx[n]] @ P[p] for n, p in kn.items()]) if kn else np.array([0.5])
    accepted = dict(known)
    cand_idx = np.array([idx[n] for n in unl])
    for rnd in range(max_rounds):
        # null model: how close do ordinary (unexplained) notes come to each prototype? Only a note much closer than that is 'learnable shape'.
        Z = {}
        for p, c in P.items():
            d = 1 - Xc[cand_idx] @ c; Z[p] = (d.mean() - d) / (d.std() + 1e-9)
        best = None
        for k, n in enumerate(unl):
            if n in accepted: continue
            zs = sorted(((Z[p][k], p) for p in P), reverse=True); z, p = zs[0]; margin = z - (zs[1][0] if len(zs) > 1 else 0)
            prog = 0.5 * z * z * 1.4427 - label_bits                      # bits saved by coding the note as 'p + noise' instead of from scratch, minus the label
            if margin < min_margin: continue
            if best is None or prog > best[0]: best = (prog, n, p, z)
        if best is None or best[0] <= 0: break
        prog, n, p, z = best; accepted[n] = p; log.append(dict(round=rnd, note=n, pattern=p, progress=prog))
        P = protos(accepted)                                                # learning: the prototype moves, which changes what is surprising next round
    return dict(known=known, accepted=accepted, log=log, seeds=sorted(seed_d))

def baseline_tagger(V, model='bge', seed_domains=2, rng=None, tau=0.0, centred=True):
    """one-shot: assign each candidate to the best prototype if similarity > tau (no curiosity loop, no progress criterion)"""
    names = [n['name'] for n in V['notes']]; dom = {n['name']: n['domain'] for n in V['notes']}; truth = V['truth']['pattern_of']
    X = np.array([V['vec'][model][n] for n in names]); X /= np.linalg.norm(X, axis=1, keepdims=True)
    Xc = centre(X, [dom[n] for n in names]) if centred else X
    doms = sorted({dom[n] for n in names if n in truth and dom[n] != 'meta'}); rng = rng or random.Random(0); rng.shuffle(doms)
    seed_d = set(doms[:seed_domains]); idx = {n: i for i, n in enumerate(names)}
    known = {n: truth[n] for n in names if n in truth and dom[n] in seed_d}
    P = {}
    for p in sorted(set(known.values())):
        M = Xc[[idx[n] for n, q in known.items() if q == p]]; c = M.mean(axis=0); P[p] = c / np.linalg.norm(c)
    out = dict(known)
    for n in names:
        if n in known or dom[n] == 'meta': continue
        s = {p: Xc[idx[n]] @ c for p, c in P.items()}; p = max(s, key=s.get)
        if s[p] > tau: out[n] = p
    return out

def invent(V, model='bge', exclude=(), min_size=3, label_bits=6.0, theta=0.5, max_size=8):
    """creativity: propose NEW patterns. Greedy: pick the group of unexplained notes (from different domains) whose centred vectors
    share one direction, if describing them by that direction saves more bits than the cost of a new name."""
    names = [n['name'] for n in V['notes']]; dom = {n['name']: n['domain'] for n in V['notes']}
    X = np.array([V['vec'][model][n] for n in names]); X /= np.linalg.norm(X, axis=1, keepdims=True)
    Xc = centre(X, [dom[n] for n in names]); idx = {n: i for i, n in enumerate(names)}
    pool = [n for n in names if n not in exclude and dom[n] != 'meta']; proposals = []
    for _ in range(6):
        best = None
        for a in pool:                                           # seed a candidate abstraction on each note, grow it greedily
            S = Xc[[idx[n] for n in pool]] @ Xc[idx[a]]
            order = [pool[i] for i in np.argsort(-S)]
            grp = [a]
            for b in order:
                if b == a: continue
                cand = grp + [b]; M = Xc[[idx[n] for n in cand]]; c = M.mean(axis=0); c /= (np.linalg.norm(c) or 1)
                tight = float(np.mean(M @ c))
                if tight < theta or len(cand) > max_size: break
                grp = cand
            if len(grp) >= min_size:
                M = Xc[[idx[n] for n in grp]]; c = M.mean(axis=0); c /= np.linalg.norm(c)
                gain = float(sum(M @ c) * 4 - label_bits)      # bits saved by one shared direction (4 bits per unit of agreement)
                if len({dom[n] for n in grp}) >= 2 and (best is None or gain > best[0]): best = (gain, grp)
        if not best or best[0] <= 0: break
        proposals.append(dict(gain=best[0], notes=best[1])); pool = [n for n in pool if n not in best[1]]
    return proposals

if __name__ == '__main__':
    d, out = sys.argv[1], sys.argv[2]; res = []
    for f in sorted(glob.glob(d + '/vault_*.json')):
        V = json.load(open(f)); truth = V['truth']['pattern_of']; dom = {n['name']: n['domain'] for n in V['notes']}
        for sd in (2,):
            rec = dict(seed=V['seed'], seed_domains=sd)
            for tag, fn in [('curiosity', lambda: run(V, seed_domains=sd, rng=random.Random(V['seed']))['accepted']),
                            ('tagger_centred', lambda: baseline_tagger(V, seed_domains=sd, rng=random.Random(V['seed']))),
                            ('tagger_plain', lambda: baseline_tagger(V, seed_domains=sd, rng=random.Random(V['seed']), tau=0.3, centred=False))]:
                acc = fn(); seeds = set(run(V, seed_domains=sd, rng=random.Random(V['seed']))['known'])
                targets = [n for n in truth if n not in seeds and dom[n] != 'meta' and (n in V['variants']['oracle'])]
                new = {n: p for n, p in acc.items() if n not in seeds}
                rec[tag] = dict(targets=len(targets), assigned=len(new), correct=sum(truth.get(n) == p for n, p in new.items()), wrong_on_nonpattern=sum(n not in truth for n in new))
            res.append(rec)
    json.dump(res, open(out, 'w'))
    for tag in ('curiosity', 'tagger_centred', 'tagger_plain'):
        T = sum(r[tag]['targets'] for r in res); a = sum(r[tag]['assigned'] for r in res); c = sum(r[tag]['correct'] for r in res); w = sum(r[tag]['wrong_on_nonpattern'] for r in res)
        print(tag, 'assigned', a, 'correct', c, 'precision %.2f' % (c / max(1, a)), 'recall %.2f' % (c / max(1, T)), 'false hits on non-pattern notes', w)
