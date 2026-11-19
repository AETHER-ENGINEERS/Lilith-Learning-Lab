"""egglog for the patterns without loops: series-parallel structure modulo associativity and commutativity.
A graph is reduced by two moves (merge parallel edges into Par, merge a pass-through node into Ser). Egglog then decides equality
modulo the laws (Par commutative and associative, Ser associative). Two notes match when they share a reduced piece with 2+ leaves.
usage: python3 egg_sp.py VAULT_DIR OUT_JSON"""
from __future__ import annotations
import json, sys, glob, itertools, collections
import numpy as np, networkx as nx
from egglog import *
import iso

class T(Expr):
    @classmethod
    def up(cls) -> T: ...
    @classmethod
    def dn(cls) -> T: ...
    def ser(self, o: T) -> T: ...
    def par(self, o: T) -> T: ...

def reduce_graph(edges):
    """returns the list of remaining (u, v, term) after parallel and series reductions; term is a nested tuple"""
    E = [(a, b, ('+' if s == '+' else '-')) for a, b, s in edges if a != b]            # self loops handled by the loop test
    changed = True
    while changed:
        changed = False
        d = collections.defaultdict(list)
        for i, (a, b, t) in enumerate(E): d[(a, b)].append(i)
        for k, idx in d.items():
            if len(idx) > 1:
                ts = tuple(sorted([E[i][2] for i in idx], key=repr)); keep = [e for i, e in enumerate(E) if i not in idx]
                t = ts[0]
                for x in ts[1:]: t = ('par', t, x)
                E = keep + [(k[0], k[1], t)]; changed = True; break
        if changed: continue
        ins = collections.defaultdict(list); outs = collections.defaultdict(list)
        for i, (a, b, t) in enumerate(E): outs[a].append(i); ins[b].append(i)
        for n in set(ins) & set(outs):
            if len(ins[n]) == 1 and len(outs[n]) == 1 and ins[n][0] != outs[n][0]:
                i, j = ins[n][0], outs[n][0]; a, _, t1 = E[i]; _, b, t2 = E[j]
                if a != b:
                    E = [e for k, e in enumerate(E) if k not in (i, j)] + [(a, b, ('ser', t1, t2))]; changed = True; break
    return E
def to_expr(t):
    if t == '+': return T.up()
    if t == '-': return T.dn()
    return (to_expr(t[1]).ser if t[0] == 'ser' else to_expr(t[1]).par)(to_expr(t[2]))
def leaves(t): return 1 if isinstance(t, str) else leaves(t[1]) + leaves(t[2])

def build():
    eg = EGraph(); a, b, c = vars_("a b c", T)
    eg.register(rewrite(a.par(b)).to(b.par(a)), rewrite(a.par(b).par(c)).to(a.par(b.par(c))), rewrite(a.ser(b).ser(c)).to(a.ser(b.ser(c))))
    return eg

if __name__ == '__main__':
    d, outf = sys.argv[1], sys.argv[2]; files = [f for f in sorted(glob.glob(d + '/vault_*.json')) if 'graphs' in json.load(open(f))]
    V_all = {f: json.load(open(f)) for f in files}; red = {}
    terms = set()
    for f, V in V_all.items():
        for n, e in V['graphs'].items():
            rs = [t for (_, _, t) in reduce_graph(e) if leaves(t) >= 2]; red[(f, n)] = rs; terms |= set(rs)
    eg = build(); ex = {t: to_expr(t) for t in terms}
    for t, x in ex.items(): eg.register(x)
    eg.run(25)
    canon = {t: str(eg.extract(x)) for t, x in ex.items()}
    print('distinct reduced terms', len(terms), 'classes modulo AC', len(set(canon.values())))
    ctr = collections.Counter(canon[t] for ts in red.values() for t in ts); print('most common pieces:'); [print('  ', v, k[:90]) for k, v in ctr.most_common(4)]
    noloop = 0; red_notes = collections.Counter(); cnt = collections.Counter()
    res = []
    for f, V in V_all.items():
        truth = V['truth']['pattern_of']; dom = {n['name']: n['domain'] for n in V['notes']}; names = [n['name'] for n in V['notes'] if n['domain'] != 'meta']
        for n, p in truth.items(): cnt[p] += 1; red_notes[p] += bool(red.get((f, n)))
        sig = {n: {canon[t] for t in red.get((f, n), [])} for n in names}
        pairs = [(a, b) for a, b in itertools.combinations(names, 2) if dom[a] != dom[b]]
        tb = {tuple(sorted(p)) for p in V['truth']['bridges']}; ff = {tuple(sorted(p)) for p in V['truth']['false_friends']}
        y = [1 if tuple(sorted(p)) in tb else 0 for p in pairs]; K = sum(y); sc = [len(sig[a] & sig[b]) for a, b in pairs]
        idx = np.argsort(-np.array(sc, float), kind='stable')[:K]; pos = [i for i, s in enumerate(sc) if s > 0]
        res.append(dict(K=K, chance=K / len(pairs), pk=sum(y[i] for i in idx) / K, auroc=iso.auroc(sc, y), ff=sum(tuple(sorted(pairs[i])) in ff for i in idx), npos=len(pos), tp=sum(y[i] for i in pos), ffpos=sum(tuple(sorted(pairs[i])) in ff for i in pos)))
    print('patterns with a reducible piece (2+ leaves):', {p: f'{red_notes[p]}/{cnt[p]}' for p in sorted(cnt)})
    print('SP match: P@K %.2f AUROC %.2f false friends in top K %.2f chance %.3f' % (np.mean([r['pk'] for r in res]), np.nanmean([r['auroc'] for r in res]), np.mean([r['ff'] for r in res]), np.mean([r['chance'] for r in res])))
    n = sum(r['npos'] for r in res); t = sum(r['tp'] for r in res); K = sum(r['K'] for r in res)
    print('pairs sharing a piece: %d, true bridges %d (precision %.2f, recall %.2f), false friends %d' % (n, t, t / max(1, n), t / K, sum(r['ffpos'] for r in res)))
    json.dump(res, open(outf, 'w'))
