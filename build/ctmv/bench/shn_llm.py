"""Kulikauskas's three structure kinds (sequence, hierarchy, network) as a feature of each note, and the six restructurings between them.
Kind from the note's relation graph: acyclic path = sequence; acyclic tree (no node with 2 parents, some node with 2+ children) = hierarchy; anything with a cycle or a node with 2+ parents = network.
usage: python3 shn.py VAULT_DIR OUT_JSON"""
import json, sys, glob, itertools, collections
import numpy as np, networkx as nx
import iso
def kind(edges):
    g = iso.G(edges)
    if g.number_of_edges() == 0: return 'none'
    if not nx.is_directed_acyclic_graph(g) or any(d > 1 for _, d in g.in_degree()): return 'network'
    return 'hierarchy' if any(d > 1 for _, d in g.out_degree()) else 'sequence'
if __name__ == '__main__':
    d, outf = sys.argv[1], sys.argv[2]; files = [f for f in sorted(glob.glob(d + '/vault_*.json')) if 'graphs' in json.load(open(f))]
    byp = collections.defaultdict(collections.Counter); res = []
    for f in files:
        V = json.load(open(f)); truth = V['truth']['pattern_of']; dom = {n['name']: n['domain'] for n in V['notes']}
        names = [n['name'] for n in V['notes'] if n['domain'] != 'meta']; K_ = {n: V['kinds'][n] for n in names}
        for n, p in truth.items(): byp[p][K_[n]] += 1
        pairs = [(a, b) for a, b in itertools.combinations(names, 2) if dom[a] != dom[b]]
        tb = {tuple(sorted(p)) for p in V['truth']['bridges']}; ff = {tuple(sorted(p)) for p in V['truth']['false_friends']}
        y = [1 if tuple(sorted(p)) in tb else 0 for p in pairs]; K = sum(y)
        same = [1.0 if K_[a] == K_[b] and K_[a] != 'none' else 0.0 for a, b in pairs]
        conv = collections.Counter((K_[a], K_[b]) if K_[a] <= K_[b] else (K_[b], K_[a]) for (a, b), t in zip(pairs, y) if t)
        idx = np.argsort(-np.array(same), kind='stable')[:K]
        res.append(dict(K=K, chance=K / len(pairs), same_bridge=sum(s for s, t in zip(same, y) if t), same_all=sum(same), n=len(pairs), pk=sum(y[i] for i in idx) / K, auroc=iso.auroc(same, y), conv=dict(((a + '|' + b), c) for (a, b), c in conv.items())))
    print('kind of each pattern note (graph-derived):')
    for p in sorted(byp): print('  ', p.ljust(18), dict(byp[p]))
    K = sum(r['K'] for r in res); sb = sum(r['same_bridge'] for r in res); sa = sum(r['same_all'] for r in res); n = sum(r['n'] for r in res)
    print('bridges whose two notes have the same kind: %d of %d (%.2f); all cross-domain pairs with the same kind: %.2f' % (sb, K, sb / K, sa / n))
    print('same-kind score: P@K %.2f AUROC %.2f chance %.3f' % (np.mean([r['pk'] for r in res]), np.nanmean([r['auroc'] for r in res]), np.mean([r['chance'] for r in res])))
    c = collections.Counter()
    for r in res:
        for k, v in r['conv'].items(): c[k] += v
    print('kind pairs among true bridges:', dict(c.most_common(8)))
    json.dump(res, open(outf, 'w'))
