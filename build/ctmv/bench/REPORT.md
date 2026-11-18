# CTMV claim benchmark

Date: 2026-11-18. Harness: `gen_vaults.py`, `run_bench.mjs`, `run_scale.mjs`, `analyze.py`. Real engines (jade-kg WASM, sqlite-vec) and real embeddings (bge-small-en-v1.5, all-MiniLM-L6-v2). 60 generated vaults (30 templated, 30 hand-rewritten style), about 100 notes each, with planted bridges, false friends, replaced notes, disputes and causal chains. Intervals are 95% bootstrap.

## Verdicts

| Claim | Verdict |
|---|---|
| Finds cross-domain analogies that similarity search misses | **Holds only with good extraction.** Dense and hybrid are near chance; keyword is lured by false friends. CTMV gets 1.00 with oracle claims, 0.78-0.81 at 90% accurate pattern labels, 0.50 at 70%, 0.28 at 50%. The automatic embedding tagger scored 0.05, no better than search. |
| Drops replaced (superseded) notes | **Holds, but is cheap.** CTMV 0% stale vs 100% for dense. A plain "drop a result that another result links to as its replacement" rule also scores 0% stale. Noisy claims leave 16-44% stale. |
| Flags disputes (cause vs prevent) | **Holds, unique to CTMV.** All baselines are silent. 100% found with oracle claims, 33-66% with noisy claims, at about 0.8-1.5 false alarms per vault. |
| Warped multi-hop retrieval | **Holds.** Recall@3 0.91-0.93 (realistic claims) vs 0.76-0.79 dense plus feedback, 0.58-0.60 dense. Part of the gain is expansion alone; the warp adds beyond plain graph expansion when claims are noisy. |
| Commutativity error delta is a useful signal | **Weak.** AUROC 0.84 with oracle claims, 0.65 realistic, below chance with the tagger. Saturates (about half the notes have delta = 1). |
| Replay is deterministic | **Verified.** Identical fact fingerprints in 30/30 shuffled reloads. |
| sqlite-vec cosine is correct | **Verified.** Max error 7e-07. |
| Scales | **Limits found.** Fine to about 1000 notes. Shared-idea facts grow quadratically with group size, every query caps at 200 answers, and the lab's pair-edge computation is O(N^2). |

## Limitations

- Synthetic data with a closed pattern ontology; ground truth comes from the generator (circular oracle).
- Vaults of about 100 notes; no real personal vault.
- No language-model extractor was tested. The decisive unknown is how accurate one is. The break-even in these runs is roughly 50-70% pattern accuracy.
- Two small embedding models only.
- Write crash-safety and multi-user use not tested.

## Detailed tables


## Style: templated text (30 vaults, bge-small embeddings)

### T1. Cross-domain bridges: precision@K of unlinked cross-domain pairs (K = number of true bridges)

| extractor quality | dense | keyword | hybrid | CTMV | CTMV candidate set: precision / recall |
|---|---|---|---|---|---|
| oracle claims | 0.05 [0.04, 0.07] | 0.33 [0.30, 0.36] | 0.26 [0.23, 0.29] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| pattern labels 90% right | 0.05 [0.03, 0.07] | 0.33 [0.30, 0.36] | 0.26 [0.23, 0.29] | 0.78 [0.75, 0.82] | 0.85 [0.82, 0.88] / 0.80 [0.76, 0.83] |
| pattern labels 70% right | 0.05 [0.04, 0.07] | 0.33 [0.30, 0.36] | 0.26 [0.23, 0.29] | 0.50 [0.44, 0.56] | 0.58 [0.53, 0.64] / 0.51 [0.45, 0.57] |
| pattern labels 50% right | 0.05 [0.04, 0.07] | 0.33 [0.30, 0.36] | 0.26 [0.23, 0.29] | 0.28 [0.24, 0.32] | 0.36 [0.31, 0.40] / 0.28 [0.24, 0.32] |
| 50% of claims missed | 0.05 [0.04, 0.07] | 0.33 [0.30, 0.36] | 0.26 [0.23, 0.29] | 0.29 [0.24, 0.33] | 1.00 [1.00, 1.00] / 0.29 [0.24, 0.33] |
| realistic mix (70% recall, 20% entity mismatch, 10% wrong) | 0.05 [0.04, 0.07] | 0.33 [0.30, 0.36] | 0.26 [0.23, 0.29] | 0.47 [0.42, 0.51] | 0.70 [0.65, 0.75] / 0.49 [0.44, 0.54] |
| automatic few-shot embedding tagger | 0.05 [0.03, 0.07] | 0.33 [0.30, 0.36] | 0.26 [0.23, 0.29] | 0.06 [0.04, 0.09] | 0.21 [0.17, 0.24] / 0.46 [0.41, 0.51] |

Chance level is 0.031. False friends (same word, different meaning) among each method's top K, mean count: dense 0.27, keyword 4.00, CTMV 0.00.
Bridges that dense search ranks outside its top 3K: 25.0 per vault on average; CTMV's candidate set contains 1.00 [1.00, 1.00] of them with oracle claims.

### T2. Contradictions: top-3 retrieval, 6 superseded-note queries and 4 dispute queries per vault

| extractor quality | method | current note found | stale note also returned | dispute: both returned unflagged |
|---|---|---|---|---|
| oracle claims | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| recall80 | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 0.90 [0.86, 0.94] | 0.16 [0.11, 0.21] | 0.23 [0.14, 0.33] |
| canon30 | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 0.87 [0.81, 0.92] | 0.28 [0.22, 0.34] | 0.23 [0.16, 0.33] |
| realistic mix (70% recall, 20% entity mismatch, 10% wrong) | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 0.91 [0.87, 0.94] | 0.44 [0.38, 0.51] | 0.53 [0.41, 0.65] |

Constraint check (Datalog): detects planted disputes, and false alarms.

| extractor quality | disputes detected | false alarms per vault | replaced notes recognised |
|---|---|---|---|
| oracle | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| recall80 | 0.66 [0.57, 0.75] | 0.77 [0.50, 1.07] | 0.82 [0.76, 0.87] |
| canon30 | 0.63 [0.56, 0.71] | 1.00 [0.63, 1.33] | 0.68 [0.61, 0.74] |
| realistic | 0.36 [0.26, 0.46] | 0.77 [0.50, 1.07] | 0.52 [0.45, 0.58] |

### T3. Multi-hop: recall@3 of a 3-note causal chain, query names only the first link

| extractor quality | dense | keyword | hybrid | dense + feedback (PRF) | graph expand (no warp) | CTMV warp λ=0 | CTMV λ=0.6 | CTMV λ=0.9 |
|---|---|---|---|---|---|---|---|---|
| oracle | 0.58 [0.55, 0.61] | 0.39 [0.37, 0.40] | 0.54 [0.52, 0.57] | 0.76 [0.74, 0.78] | 1.00 [1.00, 1.00] | 0.83 [0.81, 0.85] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| recall80 | 0.58 [0.55, 0.61] | 0.39 [0.37, 0.40] | 0.54 [0.52, 0.56] | 0.76 [0.73, 0.78] | 0.70 [0.66, 0.73] | 0.83 [0.81, 0.85] | 0.93 [0.91, 0.95] | 0.93 [0.91, 0.95] |
| canon30 | 0.58 [0.55, 0.61] | 0.39 [0.37, 0.40] | 0.54 [0.52, 0.56] | 0.76 [0.73, 0.78] | 0.74 [0.70, 0.78] | 0.83 [0.81, 0.85] | 0.96 [0.95, 0.98] | 0.98 [0.97, 0.99] |
| realistic | 0.58 [0.55, 0.61] | 0.39 [0.37, 0.40] | 0.54 [0.51, 0.57] | 0.76 [0.74, 0.78] | 0.53 [0.49, 0.56] | 0.83 [0.81, 0.85] | 0.91 [0.89, 0.93] | 0.92 [0.90, 0.94] |

### T4. Is δ informative? AUROC for flagging notes that are in a planted bridge or false friend

| extractor quality | δ | "note has few claims" (sparsity) | share of notes with δ = 1 |
|---|---|---|---|
| oracle | 0.84 [0.84, 0.85] | 0.40 [0.40, 0.40] | 0.49 |
| acc70 | 0.83 [0.82, 0.83] | 0.40 [0.40, 0.40] | 0.46 |
| recall50 | 0.63 [0.62, 0.64] | 0.43 [0.41, 0.45] | 0.81 |
| realistic | 0.65 [0.64, 0.66] | 0.41 [0.39, 0.42] | 0.74 |
| tagger | 0.43 [0.41, 0.44] | 0.10 [0.09, 0.12] | 0.83 |

### Robustness: second embedding model (MiniLM) vs bge-small, bridges P@K

| model | dense | keyword | CTMV (oracle claims) | CTMV (realistic) |
|---|---|---|---|---|
| bge | 0.05 [0.04, 0.07] | 0.33 [0.30, 0.36] | 1.00 [1.00, 1.00] | 0.47 [0.42, 0.51] |
| minilm | 0.01 [0.01, 0.02] | 0.33 [0.30, 0.36] | 1.00 [1.00, 1.00] | 0.47 [0.42, 0.52] |

### T6. Replay

- Fact fingerprint identical after reloading the notes in a shuffled order: 30/30 vaults; identical reasoner answers: 30/30.
- Fact fingerprint identical across the two embedding models: 30/30 (expected, because G is built from the claims only).
- Nearest-neighbour agreement between the two embedding models (Jaccard of the top 3): 0.63. So M really does change when the model changes.
- sqlite-vec cosine distance vs direct computation: max error 7.2e-07.
- Truncated pair queries during the runs: 0 of 450 runs.

## Style: rewritten text (30 vaults, bge-small embeddings)

### T1. Cross-domain bridges: precision@K of unlinked cross-domain pairs (K = number of true bridges)

| extractor quality | dense | keyword | hybrid | CTMV | CTMV candidate set: precision / recall |
|---|---|---|---|---|---|
| oracle claims | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| pattern labels 90% right | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.81 [0.78, 0.85] | 0.87 [0.84, 0.91] / 0.81 [0.78, 0.85] |
| pattern labels 70% right | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 0.00 [0.00, 0.00] | 0.51 [0.46, 0.56] | 0.61 [0.56, 0.67] / 0.52 [0.46, 0.57] |
| pattern labels 50% right | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.26 [0.22, 0.30] | 0.33 [0.28, 0.37] / 0.26 [0.22, 0.30] |
| 50% of claims missed | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 0.00 [0.00, 0.00] | 0.31 [0.27, 0.35] | 1.00 [1.00, 1.00] / 0.30 [0.26, 0.34] |
| realistic mix (70% recall, 20% entity mismatch, 10% wrong) | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 0.00 [0.00, 0.00] | 0.47 [0.42, 0.52] | 0.70 [0.64, 0.76] / 0.51 [0.44, 0.57] |
| automatic few-shot embedding tagger | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.05 [0.04, 0.07] | 0.05 [0.04, 0.06] / 0.25 [0.21, 0.29] |

Chance level is 0.029. False friends (same word, different meaning) among each method's top K, mean count: dense 0.23, keyword 4.00, CTMV 0.00.
Bridges that dense search ranks outside its top 3K: 28.6 per vault on average; CTMV's candidate set contains 1.00 [1.00, 1.00] of them with oracle claims.

### T2. Contradictions: top-3 retrieval, 6 superseded-note queries and 4 dispute queries per vault

| extractor quality | method | current note found | stale note also returned | dispute: both returned unflagged |
|---|---|---|---|---|
| oracle claims | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| recall80 | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 0.87 [0.82, 0.92] | 0.22 [0.16, 0.29] | 0.23 [0.15, 0.31] |
| canon30 | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 0.79 [0.73, 0.85] | 0.31 [0.24, 0.37] | 0.25 [0.16, 0.35] |
| realistic mix (70% recall, 20% entity mismatch, 10% wrong) | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 0.87 [0.82, 0.92] | 0.38 [0.32, 0.46] | 0.56 [0.45, 0.67] |

Constraint check (Datalog): detects planted disputes, and false alarms.

| extractor quality | disputes detected | false alarms per vault | replaced notes recognised |
|---|---|---|---|
| oracle | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| recall80 | 0.67 [0.59, 0.74] | 0.97 [0.63, 1.30] | 0.74 [0.67, 0.81] |
| canon30 | 0.65 [0.57, 0.73] | 1.53 [1.17, 1.93] | 0.65 [0.58, 0.72] |
| realistic | 0.33 [0.24, 0.42] | 0.90 [0.57, 1.27] | 0.59 [0.53, 0.66] |

### T3. Multi-hop: recall@3 of a 3-note causal chain, query names only the first link

| extractor quality | dense | keyword | hybrid | dense + feedback (PRF) | graph expand (no warp) | CTMV warp λ=0 | CTMV λ=0.6 | CTMV λ=0.9 |
|---|---|---|---|---|---|---|---|---|
| oracle | 0.60 [0.57, 0.63] | 0.40 [0.38, 0.41] | 0.56 [0.54, 0.58] | 0.79 [0.77, 0.81] | 1.00 [1.00, 1.00] | 0.81 [0.79, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| recall80 | 0.60 [0.57, 0.63] | 0.40 [0.38, 0.41] | 0.56 [0.54, 0.59] | 0.79 [0.77, 0.81] | 0.75 [0.70, 0.79] | 0.81 [0.79, 0.83] | 0.95 [0.93, 0.97] | 0.96 [0.94, 0.97] |
| canon30 | 0.60 [0.57, 0.63] | 0.40 [0.38, 0.41] | 0.56 [0.54, 0.58] | 0.79 [0.77, 0.81] | 0.74 [0.70, 0.77] | 0.81 [0.79, 0.83] | 0.95 [0.94, 0.96] | 0.98 [0.97, 0.99] |
| realistic | 0.60 [0.57, 0.63] | 0.40 [0.38, 0.41] | 0.56 [0.54, 0.58] | 0.79 [0.77, 0.81] | 0.57 [0.53, 0.60] | 0.81 [0.79, 0.83] | 0.91 [0.89, 0.92] | 0.93 [0.91, 0.94] |

### T4. Is δ informative? AUROC for flagging notes that are in a planted bridge or false friend

| extractor quality | δ | "note has few claims" (sparsity) | share of notes with δ = 1 |
|---|---|---|---|
| oracle | 0.85 [0.85, 0.85] | 0.40 [0.40, 0.40] | 0.49 |
| acc70 | 0.83 [0.83, 0.84] | 0.40 [0.40, 0.40] | 0.47 |
| recall50 | 0.63 [0.62, 0.64] | 0.42 [0.41, 0.44] | 0.82 |
| realistic | 0.67 [0.66, 0.68] | 0.41 [0.39, 0.43] | 0.73 |
| tagger | 0.44 [0.42, 0.47] | 0.18 [0.16, 0.21] | 0.68 |

### Robustness: second embedding model (MiniLM) vs bge-small, bridges P@K

| model | dense | keyword | CTMV (oracle claims) | CTMV (realistic) |
|---|---|---|---|---|
| bge | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 1.00 [1.00, 1.00] | 0.47 [0.41, 0.52] |
| minilm | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 1.00 [1.00, 1.00] | 0.46 [0.41, 0.51] |

### T6. Replay

- Fact fingerprint identical after reloading the notes in a shuffled order: 30/30 vaults; identical reasoner answers: 30/30.
- Fact fingerprint identical across the two embedding models: 30/30 (expected, because G is built from the claims only).
- Nearest-neighbour agreement between the two embedding models (Jaccard of the top 3): 0.56. So M really does change when the model changes.
- sqlite-vec cosine distance vs direct computation: max error 7.5e-07.
- Truncated pair queries during the runs: 0 of 450 runs.

## Scale (synthetic vault, 2 to 3 claims per note, random 384-dimensional vectors)

| scenario | notes | derived facts | load ms | full edge-set ms | vector insert ms | kNN ms/query | problems |
|---|---|---|---|---|---|---|---|
| typical (group 10) | 100 | 2802 | 23 | 274 | 39 | 1.4 |  |
| typical (group 10) | 300 | 8406 | 29 | 1954 | 36 | 0.6 |  |
| typical (group 10) | 1000 | 40884 | 87 | 19939 | 58 | 0.9 |  |
| typical (group 10) | 3000 | 122652 | 240 | - | 138 | 1.7 |  |
| typical (group 10) | 10000 | 1074600 | 4753 | - | - | - |  |
| big-group (group 100) | 1000 | 220794 | 111 | 164067 | 62 | 0.8 |  |
| big-group (group 400) | 2000 | 1641605 | 2683 | - | 70 | 1.6 | queries capped at 200 answers |
| hub (group 10, hub 10%) | 1000 | 50628 | 43 | 53808 | 44 | 0.6 |  |
| hub (group 10, hub 30%) | 1500 | 279919 | 262 | - | 28 | 0.9 |  |
| hub (group 10, hub 30%) | 3000 | 942675 | 1045 | - | 118 | 2.9 | queries capped at 200 answers |