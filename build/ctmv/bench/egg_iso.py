"""Invariants and isomorphisms with egglog (equality saturation).
Each note's relation graph (signed edges, language-model extracted) gives its feedback loops. A loop is a cyclic sequence of signs.
Rules given to egglog: rotation does not change a loop (Cyc(a r) = Cyc(r a)); signs multiply around the loop (polarity); length counts edges.
After saturation, two loops are the same e-class exactly when they are isomorphic as signed loops, and polarity and length are derived invariants.
usage: python3 egg_iso.py VAULT_DIR LEAP_JSON OUT_JSON"""
from __future__ import annotations
import json, sys, glob, itertools, collections
import numpy as np, networkx as nx
from egglog import *
import iso

class Sg(Expr):
    @classmethod
    def p(cls) -> Sg: ...
    @classmethod
    def m(cls) -> Sg: ...
    def mul(self, o: Sg) -> Sg: ...
class Nat(Expr):
    @classmethod
    def z(cls) -> Nat: ...
    def s(self) -> Nat: ...
class Seq(Expr):
    @classmethod
    def nil(cls) -> Seq: ...
    @classmethod
    def cons(cls, s: Sg, r: Seq) -> Seq: ...
    def app(self, s: Sg) -> Seq: ...
    def pol(self) -> Sg: ...
    def size(self) -> Nat: ...
class Cyc(Expr):
    def __init__(self, s: Seq) -> None: ...
    def pol(self) -> Sg: ...
    def size(self) -> Nat: ...

def make_egraph():
    eg = EGraph(); a, x = vars_("a x", Sg); r = var("r", Seq); q = var("q", Seq)
    eg.register(
        rewrite(Sg.p().mul(Sg.p())).to(Sg.p()), rewrite(Sg.p().mul(Sg.m())).to(Sg.m()), rewrite(Sg.m().mul(Sg.p())).to(Sg.m()), rewrite(Sg.m().mul(Sg.m())).to(Sg.p()),
        rewrite(Seq.nil().app(x)).to(Seq.cons(x, Seq.nil())), rewrite(Seq.cons(a, r).app(x)).to(Seq.cons(a, r.app(x))),
        rewrite(Cyc(Seq.cons(a, r))).to(Cyc(r.app(a))),                                        # rotation
        rewrite(Seq.nil().pol()).to(Sg.p()), rewrite(Seq.cons(a, r).pol()).to(a.mul(r.pol())),
        rewrite(Seq.nil().size()).to(Nat.z()), rewrite(Seq.cons(a, r).size()).to(r.size().s()),
        rewrite(Cyc(q).pol()).to(q.pol()), rewrite(Cyc(q).size()).to(q.size()))
    return eg
def mk(signs):
    s = Seq.nil()
    for g in reversed(signs): s = Seq.cons(Sg.p() if g == '+' else Sg.m(), s)
    return s

def cycles(g):
    out = []
    for cyc in nx.simple_cycles(g, length_bound=6):
        sg = [g[cyc[i]][cyc[(i + 1) % len(cyc)]]['s'] for i in range(len(cyc))] if len(cyc) > 1 else [g[cyc[0]][cyc[0]]['s']]
        out.append(tuple(sg))
    return out

def canon_table(all_signs):
    eg = make_egraph(); items = {}
    for sg in all_signs:
        c = Cyc(mk(sg)); eg.register(c, c.pol(), c.size()); items[sg] = c
    eg.run(60)
    tab = {}
    for sg, c in items.items():
        k = str(eg.extract(c)); pol = str(eg.extract(c.pol())); size = str(eg.extract(c.size())).count('.s()') + 0
        tab[sg] = (k, 'P' if 'Sg.p()' == pol else 'M', len(sg))
    return tab, eg, items

if __name__ == '__main__':
    d, leap_f, outf = sys.argv[1], sys.argv[2], sys.argv[3]
    leap = {r['seed']: r['raw'] for r in json.load(open(leap_f))}; files = [f for f in sorted(glob.glob(d + '/vault_*.json')) if 'graphs' in json.load(open(f))]
    V_all = {f: json.load(open(f)) for f in files}
    signs = set()
    for V in V_all.values():
        for n, e in V['graphs'].items(): signs |= set(cycles(iso.G(e)))
    tab, eg, items = canon_table(signs)
    print('distinct loops', len(signs), 'rotation classes', len({v[0] for v in tab.values()}))
    # verify the table against a pure-python canonical form (rotation minimal) so the e-graph is not trusted blindly
    pyc = lambda sg: min(tuple(sg[i:] + sg[:i]) for i in range(len(sg)))
    bad = sum(1 for a, b in itertools.combinations(signs, 2) if (tab[a][0] == tab[b][0]) != (pyc(a) == pyc(b)))
    print('disagreements with plain python rotation check:', bad)
    # invariants table: for each true pattern, which (polarity, length) loops its notes contain
    inv = collections.defaultdict(collections.Counter); nonloop = collections.Counter(); cnt = collections.Counter()
    for V in V_all.values():
        for n, p in V['truth']['pattern_of'].items():
            cnt[p] += 1; cs = cycles(iso.G(V['graphs'].get(n, [])))
            if not cs: nonloop[p] += 1
            for c in set(cs): inv[p][tab[c][1] + str(tab[c][2])] += 1
    print('\\ninvariants by true pattern (polarity P/M + loop length: notes)')
    for p in sorted(cnt): print(' ', p.ljust(18), 'notes', cnt[p], 'no loop', nonloop[p], dict(inv[p].most_common(4)))
    res = []
    for f, V in V_all.items():
        truth = V['truth']['pattern_of']; dom = {n['name']: n['domain'] for n in V['notes']}
        names = [n['name'] for n in V['notes'] if n['domain'] != 'meta']
        info = {}
        for n in names:
            cs = {tab[c] for c in cycles(iso.G(V['graphs'].get(n, [])))}
            info[n] = dict(exact={c[0] for c in cs}, kind={(c[1], c[2]) for c in cs}, pol={c[1] for c in cs})
        pairs = [(a, b) for a, b in itertools.combinations(names, 2) if dom[a] != dom[b]]
        tb = {tuple(sorted(p)) for p in V['truth']['bridges']}; ff = {tuple(sorted(p)) for p in V['truth']['false_friends']}
        y = [1 if tuple(sorted(p)) in tb else 0 for p in pairs]; K = sum(y)
        S = {'egg_exact': [len(info[a]['exact'] & info[b]['exact']) for a, b in pairs], 'egg_kind': [len(info[a]['kind'] & info[b]['kind']) for a, b in pairs],
             'egg_pol': [len(info[a]['pol'] & info[b]['pol']) for a, b in pairs]}
        S['egg_combo'] = [2 * x + k for x, k in zip(S['egg_exact'], S['egg_kind'])]
        r = dict(K=K, chance=K / len(pairs))
        for k, sc in S.items():
            idx = np.argsort(-np.array(sc, float), kind='stable')[:K]; r[k] = dict(pk=sum(y[i] for i in idx) / K, auroc=iso.auroc(sc, y), ff=sum(tuple(sorted(pairs[i])) in ff for i in idx), pos=sum(1 for s in sc if s > 0))
        hp = set()
        for g in leap.get(V['seed'], []):
            ns = [n for n in g.get('notes', []) if n in info]; hp |= {tuple(sorted(p)) for p in itertools.combinations(ns, 2)}
        cand = [i for i, p in enumerate(pairs) if tuple(sorted(p)) in hp]; ver = [i for i in cand if S['egg_exact'][i] > 0]
        r['hunch'] = dict(proposed=len(cand), tp=sum(y[i] for i in cand)); r['verified'] = dict(kept=len(ver), tp=sum(y[i] for i in ver))
        # pairs with a shared loop that are NOT true bridges (what does the loop rule over-match?)
        pos = [i for i, s in enumerate(S['egg_exact']) if s > 0]; r['exact_pairs'] = dict(n=len(pos), tp=sum(y[i] for i in pos), ff=sum(tuple(sorted(pairs[i])) in ff for i in pos))
        res.append(r)
    json.dump(res, open(outf, 'w'))
    for k in ('egg_exact', 'egg_kind', 'egg_pol', 'egg_combo'):
        print(k, 'P@K %.2f' % np.mean([r[k]['pk'] for r in res]), 'AUROC %.2f' % np.nanmean([r[k]['auroc'] for r in res]), 'false friends in top K %.2f' % np.mean([r[k]['ff'] for r in res]))
    print('chance %.3f' % np.mean([r['chance'] for r in res]))
    ep = sum(r['exact_pairs']['n'] for r in res); et = sum(r['exact_pairs']['tp'] for r in res); K = sum(r['K'] for r in res)
    print('pairs sharing an isomorphic loop: %d, of which true bridges %d (precision %.2f), recall of all bridges %.2f' % (ep, et, et / max(1, ep), et / K))
    h = sum(r['hunch']['proposed'] for r in res); ht = sum(r['hunch']['tp'] for r in res); v = sum(r['verified']['kept'] for r in res); vt = sum(r['verified']['tp'] for r in res)
    print('hunch %d (precision %.2f) -> loop check keeps %d, correct %d (precision %.2f, recall %.2f)' % (h, ht / h, v, vt, vt / max(1, v), vt / K))
