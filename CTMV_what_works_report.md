# CTMV: what actually works

Scope: only results that held up in testing. Everything else is listed at the end as dropped or untested.
Date: 2026-11-18. Full tables and all negative results are in `build/ctmv/bench/REPORT.md`.

## Test setup (read this before trusting any number)

- 60 generated vaults (30 templated, 30 hand-rewritten style), about 100 notes each, with planted bridges, false friends, replaced notes, disputes and causal chains. Isomorphism and structure tests used 20 of the rewritten-style vaults (about 45 candidate notes each).
- Real engines and models: jade-kg (Datalog, WASM), sqlite-vec, bge-small-en-v1.5 and all-MiniLM-L6-v2 embeddings, gemma4:31b (language model through Ollama cloud), egglog 14.0, POT (optimal transport), networkx.
- **Every result below is on generated notes with clearly planted patterns. None has been tested on a real vault.** Expect lower numbers on messy notes.

## 1. The core pipeline that works

**A language model reads each note and writes claim lines; a Datalog reasoner keeps and checks them; notes stay the source of truth.**

| Part | Result |
|---|---|
| Language-model claim extraction | causal-claim recall 0.99, precision 0.75 (it adds side claims; harmless), pattern-label accuracy 0.99 |
| Cross-domain bridges from claims (shared pattern, different field, no link) | precision at K 0.99 with language-model claims, 1.00 with perfect claims. Dense and hybrid search are near chance. Keyword search is fooled by false friends |
| Replaced notes | 0% stale results when the newer note says "replaces [[old]]" (link layer, no extractor needed). Plain search returns 100% stale |
| Disputes ("X causes Y" against "X prevents Y", neither replaced) | 100% flagged with language-model or perfect claims, 0 false alarms once replacements come from the link layer. Every search baseline is silent |
| Multi-hop retrieval (seed, hop along causal links, drop replaced, flag disputed) | recall at 3: 1.00 with language-model claims; 0.91-0.93 with noisy claims; dense 0.58-0.60; dense plus feedback 0.76-0.79 |
| Replay | 30 of 30 shuffled rebuilds give identical facts |
| sqlite-vec cosine | max error 7e-07 |

Practical settings: pull weight lambda anywhere in 0.5-0.9 (a plateau: lambda 0 gives 0.81, 0.4 gives 0.98, 0.5 and up gives 1.00 with good claims). Skip concept hubs with more than 40 notes in the shared-idea rule. Fetch facts per note because the reasoner caps every query at 200 answers.

## 2. Finding and naming cross-domain patterns

**Language model proposes, structure verifies, the rule is kept.**

| Step | Result |
|---|---|
| Language-model hunch: group notes that share a mechanism across fields, no pattern list given | 1804 of 1812 planted bridges found (0.995), pair precision 0.99, false friends not grouped |
| Verify with anti-unification (common signed subgraph of 2 or more edges) | keeps 99% precision, but only 36% of the true pairs (many notes do not turn into informative graphs) |
| Stricter check (3 or more edges) | precision 1.00, recall 0.13 |
| Patterns invented with no ontology (groups of verified pairs) | 80 groups, 79 pure, 76 of 119 planted patterns recovered |
| Anti-unified rules | 126 of 198 were generic two-edge chains; 72 had 3 or more edges. Keep rules with a loop or 3 or more edges |

## 3. Structure invariants that were informative

| Invariant | Result |
|---|---|
| **Loop polarity** (signs multiply around a feedback loop; egglog with a rotation law and a sign-multiplication law) | even loops: positive feedback, contagion, threshold cascade; odd loops: negative feedback, oscillation. Same-polarity pairs: 0.32 of planted bridges in the top K (chance 0.03), no false friends. egglog agreed with a plain rotation check in every case |
| **Gromov-Wasserstein alignment** of the two graphs | AUROC 0.80, 0.84 when single-edge distractor notes are added. Never matched a false friend. Needs graphs of 2 or more nodes |
| **Structure kind** (sequence, hierarchy, network, after Kulikauskas) from the graph | 65% of true bridges share the kind, against 16% of all cross-domain pairs. AUROC 0.76. Loop patterns are all networks; bottleneck and buffer are mostly sequences |
| Polarity and structure kind together | 0.33 at K, AUROC 0.78: best structure-only pair score |
| **Algebra tables** (operation tables canonicalised by relabelling) | parity addition, sign multiplication, XOR on bits and a 180-degree flip come out as one structure, the two-element group Z2. AND and OR are one structure with 0 and 1 swapped. Addition mod 3 equals rotating a triangle. Demonstration only, not benchmarked |

## 4. Curiosity and creativity that worked

| Experiment | Result |
|---|---|
| Curiosity score in the vault (hypothesis "this note is an instance of pattern p"; progress = claims that become derivable minus 1) | works as a worked example: top hypothesis "resonance is positive feedback"; a filler note scores below zero. Not a benchmark |
| Curiosity ranking with embeddings only (domain-centred, progress threshold), templated notes | precision 0.93, recall 0.68 with 3 seed domains. On rewritten notes precision 0.53, recall 0.24: a ranking aid only |
| Inquiry agent (planner over a Bayesian mixture of hypotheses, tree search, information-gain curiosity, invention by combining library patterns), simulated worlds | known law: 1 experiment, 100% right. **New composite law: 0% without creativity, 0.87-0.90 with it.** A confident planner without curiosity stops after about 1.4 experiments and is right about a third of the time; the curious one keeps going, notices the data do not compress, invents, and reaches 0.85-0.87 at every experiment cost tested (0.05, 0.3, 0.6). Random experiments plus creativity also reach 0.88, so the planner's edge is fewer experiments, not accuracy |

## 5. Dropped: did not work

- The commutativity-error score delta as a detector: AUROC 0.84 with perfect claims, 0.65 realistic, below chance with the embedding tagger; saturates at 1 for about half of the notes. Use explicit bridge queries.
- A small embedding-based tagger for claims: precision at K 0.05, no better than search.
- Inventing new patterns from embeddings alone: barely above random (3% to 33% of patterns rediscovered, groups of purity 0.09-0.39).
- Weisfeiler-Lehman fingerprints and plain structure mapping as bridge finders: they fell to 0.06 and 0.01 at K once single-edge notes were added. Anti-unification with a 2-edge minimum is the version that holds.
- Series-parallel reduction modulo associativity and commutativity (egglog): precision 0.21; generic chains dominate.
- Replacement handled by extractor claims: 84% stale and 6 false dispute alarms per vault with the language-model extractor. Use the link layer.

## 6. Untested or limited

- Real vaults, messy notes, long notes, notes in other languages.
- The six restructuring moves between sequence, hierarchy and network (chronicle, evolution, catalog, atlas, canon, tour): no planted conversions in the data.
- Non-loop patterns (bottleneck, buffer, redundancy: 159 of 409 pattern notes) are weakly captured by the extracted graphs. The kind field helps a little.
- Extraction cost (about 100 model calls per vault), latency and stability across models.
- Scale above about 1000 notes (the lab's pair-edge step was fixed; the 200-answer query cap remains).
- Rule synthesis for e-graphs (not tried), category-theoretic tools, persistent homology (not tried).

## 7. Next step before building more

Run extraction, the dispute and replacement checks and the cross-field grouping on 100 of your real notes and read what it surfaces. If you learn a few things you did not know, build the small version: language-model extraction, the reasoner, link-layer replacement, hunch plus loop-and-anti-unification check. If it mostly returns obvious or wrong links, stop.
