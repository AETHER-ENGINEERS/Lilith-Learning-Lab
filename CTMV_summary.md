# Commutative Tri-Modal Vault (CTMV): Summary

## Summary

CTMV is a design for personal knowledge bases and AI memory that keeps one set of notes in three synchronized views:

- **V (vault):** plain markdown notes. This is the only source of truth.
- **G (graph):** facts, rules and constraints derived from the notes, run in a Datalog reasoner that gives proofs and answers "proven", "contradicted" or "unknown".
- **M (manifold):** a vector for each note in SQLite with sqlite-vec, for nearest-neighbour search.

It targets four failures of note piles and AI memory: related ideas that never meet, collections that decay, old and new facts that both come back, and memory locked inside one tool. The idea is that the three views should agree. Where they disagree, that is a clue: a cross-domain bridge, a false friend, or a missing fact.

We built a 13-chapter course with 5 in-app labs and tested the claims on 60 generated vaults, using real engines, real embeddings and a language model (gemma4:31b).

**Verdict:** worth building in a smaller form. A language model extracts claims from notes, and the reasoner flags contradictions and replaced notes and follows cause-and-effect chains. The manifold geometry (δ, warping) and the curiosity machinery added little. All tests used generated notes with clear planted patterns, so the next step is a trial on about 100 of your real notes.

## What held up in testing

- **Cross-domain bridges:** search is near chance. A language model reading each note reached 0.99 precision.
- **Replaced notes:** dropped reliably when a note says "replaces [[old]]". No extractor is needed.
- **Disputes ("X helps Y" versus "X hurts Y"):** only CTMV flags them. 100% found with clean claims and no false alarms.
- **Following a chain from its first link:** 1.00 recall with good claims, against 0.60 for plain search.
- **Replay and sqlite-vec:** identical facts after rebuilding, and vector distances accurate to under 1e-6.

## What did not hold up

- **δ (commutativity error):** weak. It separates bridge notes only with perfect claims.
- **Inventing patterns from embeddings alone:** barely better than random.
- **Scale:** quadratic fact growth and a 200-answer query cap. Partly fixed with a hub cap, indexed edge sets and lazy bridge search.

## Glossary

| Term | Meaning |
|---|---|
| CTMV | Commutative Tri-Modal Vault: three views (V, G, M) of one set of notes that should agree. |
| V | The markdown vault. The source of truth; back this up. |
| G | The fact graph built from claim lines, with rules, constraints and proofs. |
| M | The vector space of notes, stored with sqlite-vec. |
| Claim line | A dash line with three words: subject relation object. |
| π (extract) | The step that turns notes into facts. |
| φ (embed) | The step that turns notes into vectors. |
| f (warp, anchor) | Using facts to adjust how distance is measured. |
| δ | Disagreement between the two routes. 1 minus the overlap of a note's neighbours in M and in V and G. |
| Bridge | Two notes from different fields that share an idea in G, sit far apart in M and have no link in V. |
| False friend | Two notes that use the same words for different meanings. |
| Gardener | A helper that suggests links, syntheses and gaps. It never rewrites your notes. |
| λ (pull) | Shrinks the distance along causal links. |
| μ (push) | Adds distance between conflicting notes. |
| Multi-hop retrieval | Seed on the nearest note, hop along causal links, drop replaced notes, flag disputed ones. |
| Replay | Discard G and M and rebuild them from the files. Same facts, maybe different geometry. |
| Link layer | Plain text conventions such as "replaces [[old]]" that work without any extractor. |
| Compression progress | Schmidhuber's curiosity reward: how much shorter your description of the data became. |
| Anti-unification | Writing the common shape of two examples as a rule with variables. |
| MC-AIXI | A runnable approximation of Hutter's universal agent: tree search over a mixture of hypotheses. |

## Key points

- Notes are the memory. G and M are caches you can rebuild at any time.
- Facts are never guessed: every answer is proven, contradicted or unknown.
- Nearness is not truth. Search finds similar words, not shared structure.
- A bridge is far in M, shared in G and unlinked in V.
- Contradictions and replaced notes are the most clearly useful parts.
- Handle replacement in the link layer, not by extraction.
- A language model is what makes the extraction good enough.
- The language model proposes cross-field patterns. Structure matching verifies them and writes the rule.
- Keep rules with a loop or three or more edges. Two-edge rules are too generic.
- Curiosity helps most when your model class is wrong. Creativity is what finds a law outside it.
- A design is not a result. Test it on real notes before trusting it.

## Limits

- Synthetic data with clearly planted patterns; real notes will score lower.
- One language model and two small embedding models were tested.
- The 99% bridge precision is for clear notes of about 45 candidates per vault.
- The inquiry agent is a rough approximation of AIXI in a small hand-built world.

## Credits

Jade Agent Kit (MIT), Jade Vault jade-kg (MIT), SQLite (public domain), sqlite-vec by Alex Garcia (MIT or Apache-2.0). The CTMV concept follows the description you supplied. Course text, labs and benchmark code are original.
