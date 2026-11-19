"""Isomorphism hunting across domains, tested on the generated vaults with language-model-extracted signed relation graphs.
Methods (all ignore node names, so different vocabulary cannot help or hurt):
  wl     Weisfeiler-Lehman fingerprint of the signed directed graph, cosine of the fingerprint histograms
  smap   structure mapping: the largest connected, sign-preserving common subgraph (edges mapped consistently);  score = mapped edges / larger graph
  au     anti-unification: the same common subgraph written as a rule with variables; accepted only if it has >= 2 edges (systematicity) 
  gw     Gromov-Wasserstein optimal transport between the two graphs' shortest-path metrics
  hunch+smap  the language model's grouping (llm_leap.py), kept only if structure mapping confirms it
baselines: dense cosine (bge-small), keyword overlap.
Usage: python3 iso.py VAULT_DIR LEAP_JSON OUT_JSON [--distractors]"""
import json, sys, glob, itertools, collections, math
import numpy as np, networkx as nx

def G(edges):
    g = nx.DiGraph()
    for a, b, s in edges: g.add_edge(a, b, s=s)
    return g

def wl_hist(g, it=3):
    lab = {n: (g.in_degree(n), g.out_degree(n)) for n in g}; H = collections.Counter(lab.values())
    for _ in range(it):
        new = {}
        for n in g:
            out = tuple(sorted((g[n][m]['s'], lab[m]) for m in g.successors(n))); inn = tuple(sorted((g[m][n]['s'], lab[m]) for m in g.predecessors(n)))
            new[n] = hash((lab[n], out, inn))
        lab = new; H.update(lab.values())
    return H
def cosc(a, b):
    k = set(a) | set(b); x = np.array([a.get(i, 0) for i in k], float); y = np.array([b.get(i, 0) for i in k], float); d = np.linalg.norm(x) * np.linalg.norm(y); return float(x @ y / d) if d else 0.0

def common(g1, g2):
    """largest connected sign-preserving common subgraph; returns (edges, mapping)"""
    E1 = list(g1.edges(data='s')); E2 = list(g2.edges(data='s')); best = ([], {})
    def extend(m, used, rev):
        nonlocal best
        if len(used) > len(best[0]): best = (list(used), dict(m))
        for (a, b, s) in E1:
            if (a, b) in used: continue
            if a not in m and b not in m: continue
            for (c, d, t) in E2:
                if t != s: continue
                if (c, d) in rev: continue
                if (a in m and m[a] != c) or (b in m and m[b] != d): continue
                if (a not in m and c in m.values()) or (b not in m and d in m.values()): continue
                if a == b and c != d or a != b and c == d: continue
                m2 = dict(m); m2[a] = c; m2[b] = d
                extend(m2, used + [(a, b)], rev | {(c, d)})
    for (a, b, s) in E1[:8]:
        for (c, d, t) in E2[:8]:
            if t != s or (a == b) != (c == d): continue
            m = {a: c} if a == b else {a: c, b: d}
            extend(m, [(a, b)], {(c, d)})
    return best
def smap(g1, g2):
    if not g1.number_of_edges() or not g2.number_of_edges(): return 0.0, [], {}
    ed, m = common(g1, g2); return len(ed) / max(g1.number_of_edges(), g2.number_of_edges()), ed, m
def rule(g1, ed, m):
    """anti-unified rule: the matched edges with fresh variables"""
    names = {}
    v = lambda n: names.setdefault(n, 'XYZUVWST'[len(names) % 8])
    return ' ; '.join(f"{v(a)} {'raises' if g1[a][b]['s'] == '+' else 'lowers'} {v(b)}" for a, b in ed)

def gw(g1, g2):
    import ot
    if g1.number_of_nodes() < 2 or g2.number_of_nodes() < 2: return 0.0
    def C(g):
        u = g.to_undirected(); n = list(u); sp = dict(nx.all_pairs_shortest_path_length(u)); M = np.array([[sp[a].get(b, len(n) + 1) for b in n] for a in n], float); return M / (M.max() or 1)
    c1, c2 = C(g1), C(g2); p, q = np.ones(len(c1)) / len(c1), np.ones(len(c2)) / len(c2)
    d = ot.gromov.gromov_wasserstein2(c1, c2, p, q, 'square_loss'); return float(math.exp(-4 * d))

def auroc(sc, lab):
    sc = np.array(sc); lab = np.array(lab); P = sc[lab == 1]; N = sc[lab == 0]
    if not len(P) or not len(N): return float('nan')
    return float(np.mean([(p > n) + 0.5 * (p == n) for p in P for n in N]))

STOP = set('a an the of to and or is are in on it its so as at by for with that this be we was were each every one two than then them they their yet our'.split())
def toks(s): return {w for w in ''.join(c if c.isalnum() else ' ' for c in s.lower()).split() if w not in STOP}

def run(path, leap, distractors=False):
    V = json.load(open(path)); truth = V['truth']['pattern_of']; dom = {n['name']: n['domain'] for n in V['notes']}
    names = [n['name'] for n in V['notes'] if n['domain'] != 'meta']; graphs = {n: G(V['graphs'].get(n, [])) for n in names}
    body = {n['name']: n['title'] + ' ' + n['body'] for n in V['notes']}; vec = {n: np.array(V['vec']['bge'][n]) for n in dom}
    if distractors:                                       # single-edge notes that any 'A causes B' matcher would match with anything
        for n in V['notes']:
            if n['domain'] == 'meta' and (n['name'].startswith(('chain', 'benign'))):
                cl = [c for c in V['variants']['oracle'][n['name']] if c[1] == 'causes']
                if cl: names.append(n['name']); graphs[n['name']] = G([[cl[0][0], cl[0][2], '+']]); dom[n['name']] = 'x' + n['name']
    pairs = [(a, b) for a, b in itertools.combinations(names, 2) if dom[a] != dom[b]]
    tb = {tuple(sorted(p)) for p in V['truth']['bridges']}; ff = {tuple(sorted(p)) for p in V['truth']['false_friends']}
    y = [1 if tuple(sorted(p)) in tb else 0 for p in pairs]
    S = {k: [] for k in ('dense', 'keyword', 'wl', 'smap', 'au', 'au3', 'gw')}; rules = {}
    H = {n: wl_hist(graphs[n]) for n in names}
    for a, b in pairs:
        S['dense'].append(float(vec[a] @ vec[b] / (np.linalg.norm(vec[a]) * np.linalg.norm(vec[b]))))
        ta, tb_ = toks(body[a]), toks(body[b]); S['keyword'].append(len(ta & tb_) / (len(ta | tb_) or 1))
        S['wl'].append(cosc(H[a], H[b]) if graphs[a].number_of_edges() and graphs[b].number_of_edges() else 0.0)
        s, ed, m = smap(graphs[a], graphs[b]); S['smap'].append(s)
        S['au'].append(s if len(ed) >= 2 else 0.0)                                     # systematicity: a one-edge match is not a pattern
        S['au3'].append(s if len(ed) >= 3 else 0.0)
        if len(ed) >= 2: rules[(a, b)] = rule(graphs[a], ed, m)
        S['gw'].append(gw(graphs[a], graphs[b]) if graphs[a].number_of_edges() >= 2 and graphs[b].number_of_edges() >= 2 else 0.0)
    K = sum(y); out = {'K': K, 'n_pairs': len(pairs), 'chance': K / len(pairs)}
    def pk(sc, thr=None):
        idx = np.argsort(-np.array(sc), kind='stable')[:K]; hit = sum(y[i] for i in idx); f = sum(tuple(sorted(pairs[i])) in ff for i in idx); return hit / K, f
    for k, sc in S.items():
        p, f = pk(sc); out[k] = dict(pk=p, auroc=auroc(sc, y), ff=f)
    # language-model hunch, then structure mapping as the check
    hp = set()
    for g in leap.get(V['seed'], []):
        ns = [n for n in g.get('notes', []) if n in graphs]
        hp |= {tuple(sorted(p)) for p in itertools.combinations(ns, 2)}
    cand = [i for i, p in enumerate(pairs) if tuple(sorted(p)) in hp]
    ver = [i for i in cand if S['au'][i] >= 0.5]; ver3 = [i for i in cand if S['au3'][i] >= 0.5]
    out['verified3'] = dict(kept=len(ver3), tp=sum(y[i] for i in ver3))
    out['hunch'] = dict(proposed=len(cand), tp=sum(y[i] for i in cand)); out['verified'] = dict(kept=len(ver), tp=sum(y[i] for i in ver))
    # pattern invention: connected groups of confirmed pairs, no ontology
    # accepted pairs = verified; groups = connected components
    gx = nx.Graph(); gx.add_edges_from(pairs[i] for i in ver); comps = [c for c in nx.connected_components(gx) if len(c) >= 2]
    pure = 0; found = set()
    for c in comps:
        lab = collections.Counter(truth.get(n, 'none') for n in c); maj, cnt = lab.most_common(1)[0]
        if maj != 'none' and cnt / len(c) >= 0.75: pure += 1; found.add(maj)
    out['groups'] = dict(n=len(comps), pure=pure, patterns_found=len(found), patterns=len(set(truth.values())))
    out['rule_len'] = [rules[pairs[i]].count(';') + 1 for i in ver if pairs[i] in rules]
    ex = [(pairs[i], rules[pairs[i]]) for i in ver if pairs[i] in rules][:3]; out['examples'] = [(list(p), r) for p, r in ex]
    return out

if __name__ == '__main__':
    d, leap_f, outf = sys.argv[1], sys.argv[2], sys.argv[3]; dis = '--distractors' in sys.argv
    leap = {r['seed']: r['raw'] for r in json.load(open(leap_f))}
    res = []
    for f in sorted(glob.glob(d + '/vault_*.json')):
        V = json.load(open(f))
        if 'graphs' not in V: continue
        res.append(run(f, leap, dis)); print(f, flush=True)
    json.dump(res, open(outf, 'w'))
    for k in ('dense', 'keyword', 'wl', 'smap', 'au', 'au3', 'gw'):
        print(k, 'P@K %.2f' % np.mean([r[k]['pk'] for r in res]), 'AUROC %.2f' % np.nanmean([r[k]['auroc'] for r in res]), 'false friends in top K %.2f' % np.mean([r[k]['ff'] for r in res]))
    print('chance %.3f' % np.mean([r['chance'] for r in res]))
    h = sum(r['hunch']['proposed'] for r in res); t = sum(r['hunch']['tp'] for r in res); v = sum(r['verified']['kept'] for r in res); vt = sum(r['verified']['tp'] for r in res); K = sum(r['K'] for r in res)
    print('hunch: proposed %d correct %d (precision %.2f recall %.2f) | after structure check: kept %d correct %d (precision %.2f recall %.2f)' % (h, t, t / max(1, h), t / K, v, vt, vt / max(1, v), vt / K))
    v3 = sum(r['verified3']['kept'] for r in res); v3t = sum(r['verified3']['tp'] for r in res); print('hunch + strict check (3+ edges): kept %d correct %d (precision %.2f recall %.2f)' % (v3, v3t, v3t / max(1, v3), v3t / K))
    g = sum(r['groups']['n'] for r in res); p = sum(r['groups']['pure'] for r in res); pf = sum(r['groups']['patterns_found'] for r in res); pt = sum(r['groups']['patterns'] for r in res)
    print('groups from verified pairs: %d, pure %d, patterns recovered %d/%d' % (g, p, pf, pt))
    rl = [x for r in res for x in r['rule_len']]; print('rules from verified pairs: %d, one or two edges %d, three or more edges %d' % (len(rl), sum(x <= 2 for x in rl), sum(x >= 3 for x in rl)))
    for r in res[:3]:
        for p_, rl in r['examples'][:2]: print('  ', p_, '->', rl)
