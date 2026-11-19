# CTMV claim benchmark and the curiosity, creativity and inquiry experiments

Date: 2026-11-18. Harness in this folder: `gen_vaults.py`, `run_bench.mjs`, `run_scale.mjs`, `analyze.py` (claims); `llm_extract.py` (language-model extractor); `curiosity.py`, `llm_leap.py` (curiosity and leaps); `inquiry.py`, `run_inquiry.py`, `run_inquiry2.py` (inquiry agent); `llm_graph.py`, `iso.py` (isomorphism hunting); `egg_iso.py`, `egg_sp.py` (egglog); `shn.py`, `llm_kind.py` (sequence, hierarchy, network). Real engines (jade-kg WASM, sqlite-vec), real embeddings (bge-small-en-v1.5, all-MiniLM-L6-v2) and a real language model (gemma4:31b through Ollama cloud). 60 generated vaults (30 templated, 30 hand-rewritten style) of about 100 notes with planted bridges, false friends, replaced notes, disputes and causal chains. Intervals are 95% bootstrap. The inquiry experiments use simulated worlds.

## Part 1. Verdicts on the original claims (updated after the fixes and the language-model run)

| Claim | Verdict |
|---|---|
| Finds cross-domain analogies that similarity search misses | **Holds, and the extractor was the open question.** Dense and hybrid search are near chance; keyword search is lured by false friends. With perfect claims CTMV scores 1.00, at 90% accurate labels 0.78-0.81, at 70% 0.50, at 50% 0.28. The small embedding tagger scored 0.05. **A language model (gemma4:31b) reading each note gave 0.99 [0.97, 1.00]** (causal-claim recall 0.99, precision 0.75 because it also extracts side claims, pattern accuracy 0.99). |
| Drops replaced notes | **Holds, and is best done in the link layer.** With an explicit "replaces [[old]]" sentence the engine now marks the old note replaced without any extractor: 0% stale for the language-model and the noisy extractors alike. Before the fix the language-model run left 84% stale and raised 6 false dispute alarms per vault, because the model never produces "supersedes" claims. The plain link-dedupe baseline also scores 0% stale, but only when links mean replacement (it breaks if notes also carry ordinary see-also links). |
| Flags disputes (cause vs prevent) | **Holds, unique to CTMV.** All baselines are silent. 100% found with perfect or language-model claims and no false alarms after the link-layer fix; 33% with the realistic noisy mix (false alarms fell from about 0.8-1.5 per vault to 0 once replacements come from the link layer; first-run numbers are in Part 7). |
| Warped multi-hop retrieval | **Holds.** Recall@3 1.00 with perfect or language-model claims, 0.91-0.93 with noisy claims, against 0.79 for dense plus feedback and 0.60 for dense. The lambda sweep (table T3b) shows a plateau: 0.81 at lambda 0, 0.98 at 0.4, 1.00 from 0.5 with good claims; with noisy claims 0.82 at 0.1 rising slowly to 0.93 at 0.9. There is no sharp optimum; any value from 0.6 to 0.9 is fine. Part of the gain is multi-hop expansion alone (lambda 0 already gives 0.81). |
| Commutativity error delta is a useful signal | **Weak.** AUROC 0.84-0.85 with perfect or language-model claims, 0.65-0.67 realistic, below chance with the tagger. About half of all notes have delta = 1. Prefer the explicit bridge query. |
| Replay is deterministic | **Verified.** Identical fact fingerprints in 30/30 shuffled reloads (the lab fingerprint bug is fixed). |
| sqlite-vec cosine is correct | **Verified.** Max error 7e-07. |
| Scales | **Limits found, two fixed in the engine.** Shared-idea facts grow with the square of a concept's group size: generic hub concepts (more than 40 notes) are now skipped. The pair-edge step no longer tests every pair of notes (indexed by subject and object). Lazy bridges around chosen notes are available (`E.bridges(..., focus)`). Every reasoner query still caps at 200 answers, so the harness fetches facts per note. |

## Part 2. What changed in the engine after the first report

- Replaced-note handling in the link layer (`replaces [[old]]`), feeding the reasoner rule `replaced(Old)`.
- Hub-degree cap (40) on the shared-idea rule, lazy bridge search with a focus list, indexed edge sets, per-note fact fingerprint.
- `E.curiosity` (see Part 3).

## Part 3. Artificial curiosity and intuitive leaps (Schmidhuber)

Idea: be curious about what improves your compression of the data (compression progress), not about what surprises you. In the vault a hypothesis "this note is an instance of pattern p" is worth testing when it shortens the description. Noise is never chosen because it has nothing learnable.

**3a. In the vault (engine, `E.curiosity`, Lab 5).** The hypothesis adds one claim. The reasoner derives what the pattern is known to do; every claim the note already stated that is now derivable is saved. progress = claims saved minus 1. On the sample vault the top hypothesis is "resonance is positive feedback" (saves "causes runaway growth", which makes the retry storm and the microphone squeal its cross-domain partners); a filler note about a standup scores -1. This is a worked example, not a benchmark.

**3b. Transfer of known patterns with embeddings only (`curiosity.py`).** Seed: patterns labelled in two of five domains; task: label the other domains. Domain-centred embeddings, compression-progress threshold, prototypes updated after every accepted leap. Best setting (label cost 1.5 bits, margin 0.5):

| vaults | seed domains | precision | recall | false hits on non-pattern notes |
|---|---|---|---|---|
| templated | 3 | 0.93 | 0.68 | 6 |
| templated | 2 | 0.92 | 0.56 | 5 |
| rewritten | 3 | 0.53 | 0.24 | 36 |
| rewritten | 2 | 0.53 | 0.16 | 33 |

Baselines at the same seeds (one-shot tagger on plain embeddings): precision 0.11-0.19. Centring plus the progress criterion roughly quintuples precision on templated text and gives about 0.5 on rewritten text. **Verdict: curiosity helps, but embeddings alone carry only part of the shape signal; on rewritten text it is a ranking aid, not a labeller.**

**3c. Inventing a pattern nobody named, from embeddings only (negative result).** Grouping unexplained notes by a shared direction after centring: purity 0.09-0.39 (random groups 0.04-0.11); at the best setting (theta 0.7) 33% of the templated patterns and 3% of the rewritten ones were rediscovered. **Embeddings alone do not invent patterns.**

**3d. Intuitive leap by a language model (`llm_leap.py`).** The model is shown all non-meta notes of a vault, given no pattern list, and asked to group notes that share an underlying mechanism across domains and to name the mechanism in its own words. One call per vault.

| style | vaults | groups | pure groups | true bridge pairs found | pairs proposed correct |
|---|---|---|---|---|---|
| rewritten | 30 | 176 | 174 | 870 of 874 (0.995) | 0.99 |
| templated | 30 | 175 | 174 | 934 of 938 (0.996) | 0.99 |

The false friends (same word, different meaning) were not grouped. Caveat: the planted analogies are written to be clear and the vault holds about 45 candidate notes; real notes will be harder. The model sees the whole list in one prompt, which search does not.

## Part 4. MC-AIXI-style inquiry agent with curiosity and creativity (`inquiry.py`)

Setting: a hidden system in a new domain. The agent can run experiments (choose a starting value 0.5, 1 or 2 and a watch time of 3 or 6 steps; noisy time series back) and then predict which pattern governs it (+1 right, -1 wrong, 0.05 per experiment).

- **AIXI part.** The environment model is a Bayesian mixture over hypotheses with prior 2^-(description bits) (a Solomonoff-style mixture; MC-AIXI uses context-tree weighting here). Planning is Monte-Carlo tree search (UCT). Approximations: one world sampled from the posterior per rollout, open-loop tree over experiments, no posterior update inside the tree, horizon 3.
- **Library = the vault's cross-domain patterns:** growth feeds itself, correction toward a set point, delayed correction (swing), constant push (8 models).
- **Curiosity.** Intrinsic reward = Bayesian information gain (bits) of an experiment = the compression progress of the mixture on its data, weight 0.5.
- **Creativity.** When no hypothesis compresses an observation (reduced chi-square above 4), the agent invents composites of library patterns (sum of two effects, or one effect gated by the other, e.g. logistic growth), at extra description cost, and re-scores them on all past data.

World types: 150 episodes per cell, same seeds across agents. "Library" worlds are one of the 8 known models; "composite" worlds (sum of correction and growth, or logistic growth) are in no library.

| world | agent | accuracy | experiments | reward |
|---|---|---|---|---|
| library | random experiments | 0.99 | 4.0 | 0.77 |
| library | planner, no curiosity | 1.00 | 1.0 | 0.95 |
| library | planner + curiosity | 1.00 | 1.0 | 0.95 |
| library | planner + curiosity + creativity | 1.00 | 1.0 | 0.95 |
| composite | random experiments | 0.00 | 4.0 | -1.20 |
| composite | planner, no curiosity | 0.00 | 1.2 | -1.06 |
| composite | planner + curiosity | 0.00 | 1.0 | -1.05 |
| composite | planner + curiosity + creativity | **0.90** | 3.5 | **0.62** |
| composite | random experiments + creativity | 0.88 | 4.0 | 0.56 |

Cost sweep with creativity switched on for both agents (100 episodes per cell). The "plain" agent has no curiosity bonus:

| world | experiment cost | plain: accuracy / experiments | curious: accuracy / experiments |
|---|---|---|---|
| library | 0.05, 0.3, 0.6 | 1.00 / 1.0 | 1.00 / 1.0 |
| composite | 0.05 | 0.33 / 1.4 | 0.87 / 3.5 |
| composite | 0.3 | 0.34 / 1.4 | 0.85 / 3.2 |
| composite | 0.6 | 0.31 / 1.2 | 0.87 / 3.2 |

Findings, stated plainly:
1. **Creativity is what discovers the new law**: 0.00 to 0.90 accuracy. Without it no agent can name a pattern outside its library.
2. **Curiosity matters when the model class is wrong.** With the correct hypothesis in the library, the Bayesian planner already values information and curiosity adds nothing (AIXI explores optimally by itself). When the true law is missing, the plain agent trusts its confident but wrong mixture and stops after about 1.4 experiments (accuracy 0.33); the curious agent keeps experimenting, sees the data fail to compress, triggers the creative step and reaches 0.85-0.87, at every experiment cost tested. At cost 0.6 this costs reward (-1.17 versus -1.10) but buys the answer.
3. Random experiments plus creativity also work (0.88) on these small worlds. The planner's advantage here is fewer experiments on library worlds (1 vs 4) and fewer on composite worlds (3.5 vs 4), not accuracy.
4. Limits: small hand-built world, composites generated by a fixed grammar, approximations listed above, no learning of the library itself. This is a simulation of the loop, not evidence about scientific discovery in general.


## Part 8. Isomorphism hunting across domains (`llm_graph.py`, `iso.py`)

Question: can structure alone, with no shared vocabulary and no pattern list, find and name cross-domain patterns? A language model turned each domain note into a small signed relation graph (nodes, "raises" or "lowers" edges, loops when the note describes one). 20 rewritten-style vaults, about 45 candidate notes each. Every method below ignores node names. Scores: precision at K (K = number of planted bridges; chance 0.028) and AUROC over all cross-domain pairs.

| method | P@K | AUROC | false friends in top K |
|---|---|---|---|
| dense embeddings | 0.00 | 0.46 | 0.25 |
| keyword overlap | 0.00 | 0.59 | 0.00 |
| Weisfeiler-Lehman fingerprint | 0.10 | 0.80 | 0.05 |
| structure mapping (largest common signed subgraph) | 0.10 | 0.82 | 0.05 |
| anti-unification (common subgraph of 2+ edges) | 0.24 | 0.67 | 0.00 |
| anti-unification, strict (3+ edges) | 0.14 | 0.56 | 0.10 |
| Gromov-Wasserstein alignment | 0.23 | 0.80 | 0.00 |
| language-model hunch (`llm_leap.py`) | 1.00 precision, 0.99 recall | | 0 |
| hunch, kept only if anti-unification (2+ edges) confirms | 0.99 precision, 0.36 recall | | |
| hunch, kept only if strict check (3+ edges) confirms | 1.00 precision, 0.13 recall | | |

With 120 single-edge "A causes B" distractor notes added to the candidates (chance falls to 0.011), structure mapping collapses to P@K 0.01 and WL to 0.06, while anti-unification (needs 2+ edges) and Gromov-Wasserstein are unchanged at 0.24 and 0.23. That is the over-generality trap, and the systematicity requirement is what avoids it.

Invented patterns: grouping the confirmed pairs without any ontology gave 80 groups, 79 of them pure, covering 76 of 119 planted patterns across the vaults (64%). Of 198 anti-unified rules, 126 were generic two-edge chains ("X raises Y; Y raises Z") and 72 had three or more edges. The informative ones are loops: threshold cascade came out as "X raises Y; Y raises Z; Z raises X; Z raises U" (a loop with a side effect), and positive feedback as a loop.

Findings, plainly:
1. **Structure alone finds cross-domain pairs far above chance and above embeddings** (AUROC 0.80 versus 0.46) with no shared words, but it is not accurate enough to rank bridges on its own (P@K at most 0.24).
2. **The language model's hunch is much better than any structural method, and structure is best used as a verifier and a rule extractor.** The check keeps nearly all correct pairs it confirms (0.99 precision) and hands back a rule, but it only confirms 36% of the true pairs because many notes (redundancy, buffer, bottleneck) do not turn into informative graphs.
3. **Anti-unification gives checkable patterns, and loop patterns come out well.** Many of the extracted rules are too generic to be useful, so keep rules with a loop or three or more edges, and send the rest back to the language model or to you.
4. **Gromov-Wasserstein is the surprise**: the best structure-only AUROC under distractors (0.84), and it never matched a false friend. It needs graphs with two or more nodes.
5. Weak spots: patterns that are not loops (redundancy, buffer, bottleneck) are hard to express as a few signed edges. Everything depends on the extraction step, and the planted analogies are clear.


## Part 9. Invariants and isomorphisms with egglog (`egg_iso.py`, `egg_sp.py`)

Question: can equality saturation (egglog 14.0) make the invariants and isomorphisms visible? Setup: the same 20 language-model-extracted graph vaults as Part 8. Two experiments.

**9a. Feedback loops.** Each loop in a note's graph is a cyclic sequence of signs. Rules given to egglog: rotation does not change a loop; signs multiply around the loop (polarity); length counts edges. After saturation, two loops share an e-class exactly when they are isomorphic as signed loops. 12 distinct loops fell into 9 classes. The result agreed with a plain Python rotation check in every case (0 disagreements), so here egglog is correct but adds no power over a few lines of code; its value is that the laws are declarative and can be extended.

The derived invariants show clearly which patterns are loops and what kind (notes per true pattern, polarity P or M and loop length):

| true pattern | notes | with no loop | loops found |
|---|---|---|---|
| positive feedback | 57 | 0 | P (even): length 2: 17, 3: 17, 4: 16, 1: 7 |
| contagion | 43 | 6 | P: length 1: 24, 2: 13 |
| threshold cascade | 60 | 17 | P: length 3: 36, 4: 6 |
| negative feedback | 47 | 6 | M (odd): length 2: 22, 3: 19; P2: 6 |
| oscillation | 43 | 3 | M: length 2: 16, 3: 9; P2: 8; P1: 6 |
| bottleneck | 55 | 55 | none |
| buffer | 45 | 45 | none |
| redundancy | 59 | 59 | none |

Reading: loop polarity is a real invariant. Even (reinforcing) loops mark positive feedback, contagion and threshold cascades. Odd (balancing) loops mark negative feedback and oscillation. Bottleneck, buffer and redundancy (159 of 409 pattern notes) never form a loop at all.

| method | P@K | AUROC | false friends in top K |
|---|---|---|---|
| same isomorphic loop | 0.16 | 0.57 | 0.10 |
| same polarity and length | 0.18 | 0.58 | 0.10 |
| same polarity only | **0.32** | 0.69 | 0.00 |

Pairs sharing an isomorphic loop: 131, of which 71 true bridges (precision 0.54, recall 0.13). As a check on the language model's hunch (550 proposed, 549 correct) a shared loop keeps 71 with 70 correct: precision 0.99, recall 0.13. The polarity-only score gives the best structure-only P@K so far (0.32, against 0.24 for anti-unification and 0.23 for Gromov-Wasserstein) and never matched a false friend. It is a coarse class label, not a pair finder: positive feedback and threshold cascade share the same polarity.

**9b. Patterns without loops.** Graphs reduced to series-parallel terms (merge parallel edges, merge pass-through nodes), then egglog decides equality modulo associativity and commutativity. 20 distinct reduced terms fell into 17 classes. Pairs sharing a piece: 364, true bridges 76 (precision 0.21, recall 0.14); P@K 0.15, AUROC 0.56. The pieces are dominated by generic two-step chains ("up then up", 148 of the pieces). Bottleneck, buffer and redundancy notes yield almost no distinctive structure, because the extractor draws them as one or two edges.

Findings, plainly:
1. **Egglog does make one invariant visible: loop polarity**, and it cleanly separates reinforcing from balancing structures. That is useful as a label and as an explanation.
2. **It does not find isomorphisms the extractor did not draw.** About 40% of the pattern notes have no loop, and the structure left for them is too generic to match. The limit is the extraction, not the matcher.
3. **It does not beat the language model's hunch.** As a verifier it behaves like anti-unification (99% precision) with lower recall.
4. **Egglog proves equalities under laws you supply; it does not discover the laws.** Rule synthesis for e-graphs (for example Ruler) is a possible next step and was not tested.


## Part 10. Sequences, hierarchies and networks as a note feature (`shn.py`, `llm_kind.py`)

After Kulikauskas, "Organizing Thoughts into Sequences, Hierarchies, and Networks" (Minciu Sodas, 1998-99). The three structure kinds become a field on each note. Two independent ways of getting it: (a) from the note's extracted relation graph (acyclic path = sequence; acyclic tree = hierarchy; a cycle or a node with two parents = network), (b) a language model asked to label the note directly. Same 20 rewritten-style vaults as Parts 8 and 9.

| kind from the graph, by true pattern (notes) | sequence | hierarchy | network | none |
|---|---|---|---|---|
| positive feedback (57) | 0 | 0 | 57 | 0 |
| negative feedback (47) | 0 | 0 | 47 | 0 |
| oscillation (43) | 2 | 1 | 40 | 0 |
| contagion (43) | 4 | 0 | 37 | 2 |
| threshold cascade (60) | 16 | 0 | 43 | 1 |
| bottleneck (55) | 41 | 0 | 14 | 0 |
| buffer (45) | 23 | 4 | 18 | 0 |
| redundancy (59) | 29 | 0 | 12 | 18 |

| score | P@K | AUROC | note |
|---|---|---|---|
| same kind, from the graph | 0.10 | 0.76 | 65% of true bridges have the same kind; 16% of all cross-domain pairs do |
| same kind, labelled by the model | 0.11 | 0.64 | 36% of true bridges share the label |
| both extractors agree on the same kind | 0.19 | 0.60 | |
| same polarity (Part 9) | 0.32 | 0.69 | |
| same polarity and same graph kind | **0.33** | 0.78 | best structure-only P@K so far |

Chance P@K is 0.028. The two extractors agree on the kind of only 55% of notes (534 of 969), mostly "sequence" against "none".

Findings:
1. **The kind is a real but coarse feature.** Loop patterns are all networks. Bottleneck and buffer notes are mostly sequences, and redundancy notes are sequences or empty, so the kind helps a little where the loop invariants gave nothing. Same kind raises the odds of a true bridge about fourfold (65% against 16%).
2. **It is unstable under extraction.** A third of the bridges differ in kind, and the graph-derived and the model-labelled kinds agree on only 55% of notes. We cannot tell a true restructuring from extraction noise.
3. **The six restructurings (chronicle, evolution, catalog, atlas, canon, tour) were not tested.** The generated vaults plant no conversions between structure kinds, so there is nothing to measure them against. A test needs notes written as the same content in two kinds, or real notes.
4. **Use:** as an explicit field (and navigation modes such as a tour or an atlas) it is cheap and useful. As a bridge detector it adds a little on top of polarity (0.32 to 0.33 P@K) and nothing beyond that.

## Part 5. Limitations of all of the above

- Synthetic data with a closed pattern ontology (the language-model leap uses no ontology, but the planted analogies are explicit); ground truth comes from the generator.
- The language model was told the claim format and the relation names; its side claims lower claim precision to 0.75 without hurting bridges.
- One language model, two small embedding models, vaults of about 100 notes.
- Crash safety of writes and multi-user use not tested. The cost of the model calls (about 100 calls per vault for extraction) was not measured.

## Part 6. Detailed tables (rewritten-style vaults, including the language-model and lambda-sweep rows)
 text (30 vaults, bge-small embeddings)

### T1. Cross-domain bridges: precision@K of unlinked cross-domain pairs (K = number of true bridges)

| extractor quality | dense | keyword | hybrid | CTMV | CTMV candidate set: precision / recall |
|---|---|---|---|---|---|
| oracle claims | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| language model (gemma4:31b) reads each note | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] | 0.00 [0.00, 0.00] | 0.99 [0.97, 1.00] | 1.00 [1.00, 1.00] / 0.99 [0.97, 1.00] |
| realistic mix (70% recall, 20% entity mismatch, 10% wrong) | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.47 [0.42, 0.52] | 0.70 [0.64, 0.76] / 0.51 [0.45, 0.57] |

Chance level is 0.029. False friends (same word, different meaning) among each method's top K, mean count: dense 0.23, keyword 4.00, CTMV 0.00.
Bridges that dense search ranks outside its top 3K: 28.6 per vault on average; CTMV's candidate set contains 1.00 [1.00, 1.00] of them with oracle claims.

### T2. Contradictions: top-3 retrieval, 6 superseded-note queries and 4 dispute queries per vault

| extractor quality | method | current note found | stale note also returned | dispute: both returned unflagged |
|---|---|---|---|---|
| oracle claims | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| language model (gemma4:31b) reads each note | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| realistic mix (70% recall, 20% entity mismatch, 10% wrong) | dense | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | hybrid | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
|  | linkdedupe | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
|  | ctmv | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.57 [0.45, 0.68] |

Constraint check (Datalog): detects planted disputes, and false alarms.

| extractor quality | disputes detected | false alarms per vault | replaced notes recognised |
|---|---|---|---|
| oracle | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| llm | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| realistic | 0.33 [0.24, 0.42] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |

### T3. Multi-hop: recall@3 of a 3-note causal chain, query names only the first link

| extractor quality | dense | keyword | hybrid | dense + feedback (PRF) | graph expand (no warp) | CTMV warp λ=0 | CTMV λ=0.6 | CTMV λ=0.9 |
|---|---|---|---|---|---|---|---|---|
| oracle | 0.60 [0.57, 0.63] | 0.40 [0.38, 0.41] | 0.56 [0.54, 0.58] | 0.79 [0.77, 0.81] | 1.00 [1.00, 1.00] | 0.81 [0.79, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| llm | 0.60 [0.57, 0.63] | 0.40 [0.38, 0.41] | 0.56 [0.54, 0.58] | 0.79 [0.77, 0.81] | 1.00 [1.00, 1.00] | 0.81 [0.79, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| realistic | 0.60 [0.57, 0.63] | 0.40 [0.38, 0.41] | 0.56 [0.54, 0.58] | 0.79 [0.77, 0.81] | 0.57 [0.53, 0.60] | 0.81 [0.79, 0.83] | 0.91 [0.89, 0.92] | 0.93 [0.91, 0.94] |

### T3b. Lambda sweep (recall@3, slack 0.5)

| extractor | λ=0 | λ=0.1 | λ=0.2 | λ=0.3 | λ=0.4 | λ=0.5 | λ=0.6 | λ=0.7 | λ=0.8 | λ=0.9 | λ=1.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| oracle claims | 0.81 | 0.83 | 0.89 | 0.93 | 0.98 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| language model (gemma4:31b) reads each note | 0.81 | 0.83 | 0.89 | 0.93 | 0.98 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| realistic mix (70% recall, 20% entity mismatch, 10% wrong) | 0.81 | 0.82 | 0.84 | 0.86 | 0.89 | 0.90 | 0.91 | 0.91 | 0.92 | 0.93 | 0.92 |

### T4. Is δ informative? AUROC for flagging notes that are in a planted bridge or false friend

| extractor quality | δ | "note has few claims" (sparsity) | share of notes with δ = 1 |
|---|---|---|---|
| oracle | 0.85 [0.85, 0.85] | 0.40 [0.40, 0.40] | 0.49 |
| llm | 0.84 [0.84, 0.85] | 0.37 [0.36, 0.38] | 0.50 |
| realistic | 0.67 [0.66, 0.68] | 0.41 [0.39, 0.43] | 0.73 |



## Part 7. Original detailed tables (first run)




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