"""Aggregate benchmark results into tables with bootstrap 95% confidence intervals. Usage: analyze.py templated.json rewritten.json scale.json OUT.md"""
import json, sys, numpy as np
rng = np.random.default_rng(0)
def ci(x):
    x = np.array([v for v in x if v == v], float)
    if len(x) == 0: return (float('nan'),) * 3
    b = [rng.choice(x, len(x)).mean() for _ in range(2000)]
    return x.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5)
def fmt(t): return '%.2f [%.2f, %.2f]' % t
def dci(a, b):  # paired difference
    d = [x - y for x, y in zip(a, b) if x == x and y == y]; return ci(d)
def load(p): return json.load(open(p))
def sel(R, variant, model='bge'): return sorted([r for r in R if r['variant'] == variant and r['model'] == model], key=lambda r: r['seed'])
out = []
P = lambda *a: out.append(' '.join(str(x) for x in a))
data = {'templated': load(sys.argv[1]), 'rewritten': load(sys.argv[2])}
scale = load(sys.argv[3])
ACC = {'llm': 'language model (gemma4:31b) reads each note', 'oracle': 'oracle claims', 'acc90': 'pattern labels 90% right', 'acc70': 'pattern labels 70% right', 'acc50': 'pattern labels 50% right', 'recall50': '50% of claims missed', 'realistic': 'realistic mix (70% recall, 20% entity mismatch, 10% wrong)', 'tagger': 'automatic few-shot embedding tagger'}
for style, R in data.items():
    n = len(sel(R, 'oracle')); P(f'\n## Style: {style} text ({n} vaults, bge-small embeddings)\n')
    P('### T1. Cross-domain bridges: precision@K of unlinked cross-domain pairs (K = number of true bridges)\n')
    P('| extractor quality | dense | keyword | hybrid | CTMV | CTMV candidate set: precision / recall |'); P('|---|---|---|---|---|---|')
    for v in ['oracle', 'llm', 'acc90', 'acc70', 'acc50', 'recall50', 'realistic', 'tagger']:
        rs = sel(R, v)
        if not rs: continue
        cells = [fmt(ci([r['t1'][m]['pk'] for r in rs])) for m in ['dense', 'lexical', 'hybrid', 'ctmv']]
        P('| %s | %s | %s |' % (ACC[v], ' | '.join(cells), '%s / %s' % (fmt(ci([r['t1']['ctmvSet']['prec'] for r in rs])), fmt(ci([r['t1']['ctmvSet']['rec'] for r in rs])))))
    rs = sel(R, 'oracle'); P(f"\nChance level is {np.mean([r['t1']['base'] for r in rs]):.3f}. False friends (same word, different meaning) among each method's top K, mean count: dense {np.mean([r['t1']['ffInTop']['dense'] for r in rs]):.2f}, keyword {np.mean([r['t1']['ffInTop']['lexical'] for r in rs]):.2f}, CTMV {np.mean([r['t1']['ffInTop']['ctmv'] for r in rs]):.2f}.")
    P(f"Bridges that dense search ranks outside its top 3K: {np.mean([r['t1']['hard']['n'] for r in rs]):.1f} per vault on average; CTMV's candidate set contains {fmt(ci([r['t1']['hard']['ctmvRec'] for r in rs]))} of them with oracle claims.\n")
    P('### T2. Contradictions: top-3 retrieval, 6 superseded-note queries and 4 dispute queries per vault\n')
    P('| extractor quality | method | current note found | stale note also returned | dispute: both returned unflagged |'); P('|---|---|---|---|---|')
    for v in ['oracle', 'llm', 'recall80', 'canon30', 'realistic']:
        rs = sel(R, v)
        if not rs: continue
        for m in ['dense', 'hybrid', 'linkdedupe', 'ctmv']:
            P('| %s | %s | %s | %s | %s |' % (ACC.get(v, v) if m == 'dense' else '', m, fmt(ci([r['t2']['sup'][m]['hit'] for r in rs])), fmt(ci([r['t2']['sup'][m]['stale'] for r in rs])), fmt(ci([r['t2']['dis'][m]['silentBoth'] for r in rs]))))
    P('\nConstraint check (Datalog): detects planted disputes, and false alarms.\n')
    P('| extractor quality | disputes detected | false alarms per vault | replaced notes recognised |'); P('|---|---|---|---|')
    for v in ['oracle', 'llm', 'recall80', 'canon30', 'realistic']:
        rs = sel(R, v)
        if rs: P('| %s | %s | %s | %s |' % (v, fmt(ci([r['t2']['check']['disputeRecall'] for r in rs])), fmt(ci([r['t2']['check']['falsePos'] for r in rs])), fmt(ci([r['t2']['replacedRecall'] for r in rs]))))
    P('\n### T3. Multi-hop: recall@3 of a 3-note causal chain, query names only the first link\n')
    P('| extractor quality | dense | keyword | hybrid | dense + feedback (PRF) | graph expand (no warp) | CTMV warp λ=0 | CTMV λ=0.6 | CTMV λ=0.9 |'); P('|---|---|---|---|---|---|---|---|---|')
    for v in ['oracle', 'llm', 'recall80', 'canon30', 'realistic']:
        rs = sel(R, v)
        if rs: P('| %s | %s |' % (v, ' | '.join(fmt(ci([r['t3'][k]['rec'] for r in rs])) for k in ['dense', 'lexical', 'hybrid', 'prf', 'gexpand', 'ctmv_l0_s0.5', 'ctmv_l0.6_s0.5', 'ctmv_l0.9_s0.5'])))
    if style == 'rewritten' and sel(R, 'oracle'):
        P('\n### T3b. Lambda sweep (recall@3, slack 0.5)\n'); lams = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        P('| extractor | ' + ' | '.join(f'λ={l}' for l in lams) + ' |'); P('|---|' + '---|' * len(lams))
        for v in ['oracle', 'llm', 'realistic']:
            rs = sel(R, v)
            if rs and 'ctmv_l0.1_s0.5' in rs[0]['t3']: P(f'| {ACC.get(v, v)} | ' + ' | '.join(f"{np.mean([r['t3']['ctmv_l%s_s0.5' % (int(l) if l in (0, 1) else l)]['rec'] for r in rs]):.2f}" for l in lams) + ' |')
    P('\n### T4. Is δ informative? AUROC for flagging notes that are in a planted bridge or false friend\n')
    P('| extractor quality | δ | "note has few claims" (sparsity) | share of notes with δ = 1 |'); P('|---|---|---|---|')
    for v in ['oracle', 'llm', 'acc70', 'recall50', 'realistic', 'tagger']:
        rs = sel(R, v)
        if rs: P('| %s | %s | %s | %.2f |' % (v, fmt(ci([r['t4']['auroc_delta'] for r in rs])), fmt(ci([r['t4']['auroc_sparsity'] for r in rs])), np.mean([r['t4']['fracDeltaOne'] for r in rs])))
    # robustness: second embedder
    P('\n### Robustness: second embedding model (MiniLM) vs bge-small, bridges P@K\n'); P('| model | dense | keyword | CTMV (oracle claims) | CTMV (realistic) |'); P('|---|---|---|---|---|')
    for m in ['bge', 'minilm']:
        a, b = sel(R, 'oracle', m), sel(R, 'realistic', m)
        P('| %s | %s | %s | %s | %s |' % (m, fmt(ci([r['t1']['dense']['pk'] for r in a])), fmt(ci([r['t1']['lexical']['pk'] for r in a])), fmt(ci([r['t1']['ctmv']['pk'] for r in a])), fmt(ci([r['t1']['ctmv']['pk'] for r in b]))))
    # replay
    a = sel(R, 'oracle', 'bge'); b = sel(R, 'oracle', 'minilm')
    ov = []
    for ra, rb in zip(a, b):
        for k, v in ra['nn'].items(): ov.append(len(set(v) & set(rb['nn'][k])) / len(set(v) | set(rb['nn'][k])))
    P('\n### T6. Replay\n'); P(f"- Fact fingerprint identical after reloading the notes in a shuffled order: {sum(r['t6']['fpSame'] for r in a)}/{len(a)} vaults; identical reasoner answers: {sum(r['t6']['answersSame'] for r in a)}/{len(a)}.")
    P(f"- Fact fingerprint identical across the two embedding models: {sum(x['fp'] == y['fp'] for x, y in zip(a, b))}/{len(a)} (expected, because G is built from the claims only).")
    P(f"- Nearest-neighbour agreement between the two embedding models (Jaccard of the top 3): {np.mean(ov):.2f}. So M really does change when the model changes.")
    P(f"- sqlite-vec cosine distance vs direct computation: max error {max(r['vec_err'] for r in R):.1e}.")
    P(f"- Truncated pair queries during the runs: {sum(bool(r.get('sharesTrunc')) for r in R)} of {len(R)} runs.")
P('\n## Scale (synthetic vault, 2 to 3 claims per note, random 384-dimensional vectors)\n')
P('| scenario | notes | derived facts | load ms | full edge-set ms | vector insert ms | kNN ms/query | problems |'); P('|---|---|---|---|---|---|---|---|')
for r in scale:
    prob = r.get('loadErr') or ('queries capped at 200 answers' if r.get('neighbourRowsCapped') else '')
    P('| %s (group %d%s) | %d | %s | %s | %s | %s | %s | %s |' % (r['scen'], r['group'], ', hub %.0f%%' % (100 * r['hub']) if r['hub'] else '', r['N'], r.get('derived', '-'), r.get('loadMs', '-'), r.get('edgeSetsFullMs', '-'), r.get('vecInsertMs', '-'), '%.1f' % r['knnMsPer'] if 'knnMsPer' in r else '-', prob))
open(sys.argv[4], 'w').write('\n'.join(out))
print('\n'.join(out))
