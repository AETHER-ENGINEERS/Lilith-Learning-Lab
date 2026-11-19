# CTMV Playground: experiment spec for a canvas build

Goal: a single-page, offline, canvas-based playground (plain HTML, CSS and JavaScript, no libraries needed) that lets a person run the experiments that worked and see the structure. Only the parts that passed testing are included. No language model is called: where the real system uses one, the playground uses a JSON fixture or a text box where the user pastes model output (schemas below).

Style: dark background, one accent colour per view (V blue, G amber, M teal), large readable labels, every control labelled in plain words, every result shows a one-line explanation. Tabs along the top, canvas on the left, controls and a log on the right.

## Shared data model

```js
note = { name: "retry-storm", title: "...", domain: "software", text: "...",
         claims: [["retry_load","causes","outage"], ...],      // [subject, relation, object]; relation in causes | prevents | is
         replaces: ["old-note-name"],                           // from a sentence "replaces [[old-note-name]]"
         links: ["other-note"] }                                // ordinary see-also links
graph = { edges: [["from","to","+"|"-"], ...] }                // per note, signed relation graph, optional
```

Claim line syntax in the editor: a line `- subject relation object` (three lowercase words, underscores allowed). A line containing `replaces [[name]]` fills `replaces`. A line `- x is positive_feedback` states a pattern.

Provide 12 sample notes (fixture below) across four domains. The user can edit notes, add notes, and import or export all notes as JSON.

## Tab 1: Vault and facts (V and G)

- Left: note list and editor. Right: derived facts as a table.
- Rules, written in plain JavaScript (do not build a Datalog engine):
  - `replaced(old)` if a note's `replaces` contains it, or a claim `[n, "supersedes", old]` exists.
  - `dispute(a, b)`: two different notes a, b, neither replaced, with claims `[x,"causes",y]` in a and `[x,"prevents",y]` in b, same x and y.
  - `shares(a, b, pattern)`: both notes state `[_, "is", pattern]`, different domains, not linked to each other (links or wikilinks in either direction).
  - `inherits(x, r, o)`: if `[x,"is",p]` is stated and any note states `[p, r, o]`, then x inherits `[x, r, o]`.
- Show disputes as red badges on both notes, replaced notes struck through, shared patterns as amber arcs between notes.
- Acceptance: with the sample fixture, exactly 1 dispute, 1 replaced note, and the listed bridges appear (see fixture expectations).

## Tab 2: Three views on one canvas

- Draw the same notes in three panels: V (list with link arrows), G (graph, nodes are notes, edges are shared patterns and causal hand-offs), M (2D scatter of a toy embedding).
- Toy embedding: bag of words over the note text, hashed into 32 dimensions, L2 normalised, projected to 2D with the first two principal components (power iteration). Real embeddings are not needed.
- Hover a note to highlight it in all three panels. A **bridge** is drawn as an amber line: shared pattern in G, not linked in V, and cosine similarity of the toy vectors below the median of all pairs.
- A false friend is two notes from different domains whose text share a word but not a pattern: draw a grey dashed line labelled "same word, different meaning" if they share at least one non-stop word and no pattern.
- Acceptance: the two planted bridge pairs appear as amber lines; the planted false-friend pair appears as grey dashed.

## Tab 3: Multi-hop retrieval with a pull (what worked)

- Query box (text) and a lambda slider from 0 to 1, default 0.75, plus a mu slider (push, default 0.5), top-k = 3.
- Algorithm:
  1. Score every note by cosine of toy vectors to the query. Seed = best note.
  2. Causal edges: note a to b when a claim object of a equals a claim subject of b (hand-off). Hop along causal edges from the seed up to 3 steps; a hop is allowed when `d(seed, candidate) <= slack` where slack = 0.5 and `d = (1 - cosine) * (1 - lambda * causal) + mu * conflict` (causal = 1 if the pair is joined by a causal edge, conflict = 1 if they form a dispute).
  3. Drop replaced notes. Flag disputed notes with a red marker. Return the top-k by d.
- Show three result lists side by side: plain similarity, similarity with feedback (take the top result, add its words to the query, search again), and the warped multi-hop result. Highlight replaced and disputed notes that plain search returned.
- Acceptance: on the fixture query "why did the service fall over" the plain list contains the replaced note; the warped list does not, and returns the three-note causal chain.

## Tab 4: Loops and isomorphism (egglog-style laws, in JS)

- Left: a small editor where the user draws a signed directed graph: click to add nodes, drag to add edges, click an edge to toggle + and -. Provide presets: positive feedback loop, negative feedback loop, oscillation (2-loop with delay), threshold cascade (loop with a side branch).
- Compute for every simple cycle (length up to 6):
  - sign list around the cycle, **polarity** = product of signs (even number of minus signs = reinforcing, odd = balancing),
  - **canonical form** = lexicographically smallest rotation of the sign list. Two loops are isomorphic as signed loops when canonical forms are equal.
- Show a "same shape?" panel: two graphs side by side, verdict "same loop" / "same polarity only" / "different", with the matching nodes highlighted.
- Show a compact table of the invariants: polarity and loop length for each preset.
- Acceptance (these must come out exactly):
  - `++-` and `+-+` and `-++` are the same loop (canonical `++-`), polarity odd.
  - `+--` has polarity even and is not the same loop as `++-`.
  - Positive feedback preset: even polarity. Negative feedback preset: odd polarity.

## Tab 5: Algebra tables (same structure under different names)

- Show a library of operation tables as small grids: parity addition (even/odd), sign multiplication (+/-), XOR on bits (0/1), flip twice (stay/flip), AND, OR, addition mod 3, rotating a triangle (0, 120, 240 degrees). Let the user define a new 2x2 or 3x3 table by typing the cells.
- Algorithm: relabel the elements in every possible order (permutations, up to 6 elements), take the lexicographically smallest table as the canonical form. Equal canonical form = isomorphic. Also compute the laws that hold: associative, commutative, has identity, every element has an inverse, self-inverse, idempotent.
- Display groups of tables with the same canonical form, each group with its laws, and draw lines between members.
- Acceptance: {parity addition, sign multiplication, XOR, flip twice} are one group (laws: associative, commutative, identity, inverses, self-inverse). {AND, OR} are one group (idempotent). {addition mod 3, triangle rotation} are one group. No other merges.

## Tab 6: Structure kind (sequence, hierarchy, network)

- For the graph from Tab 4 (or any note's graph), compute the kind: no edges = none; acyclic and every node has at most one parent and at most one child = **sequence**; acyclic, every node has at most one parent, some node has two or more children = **hierarchy**; anything with a cycle or a node with two parents = **network**.
- Show the six restructurings as buttons that transform the current structure and say what they mean: chronicle (sequence into hierarchy: group a chain into eras), evolution (hierarchy into sequence: lay a tree out over time), catalog (hierarchy into network: add cross links to a tree), atlas (network into hierarchy: choose a spanning tree), canon (sequence into network: add association links over a chain), tour (network into sequence: walk a path). Each is a few lines of graph manipulation. These six are **illustrations only; they were not validated** (label them so).
- Acceptance: the four presets from Tab 4 are all "network"; a three-node chain is "sequence"; a node with two children and no cycle is "hierarchy".

## Tab 7: Curiosity (compression progress)

- Uses the Tab 1 notes and facts. For every note without an `is` claim and every pattern stated elsewhere, form the hypothesis "subject of note is pattern".
- Progress = number of claims of that note that become derivable through `inherits` under the hypothesis, minus 1 (the cost of stating it). Show the table sorted by progress, with the claims that would be saved and the other-domain notes that would then share the pattern.
- Buttons: **Take the leap** (appends the claim line to the note and re-derives, so the new bridge appears on Tab 2), **Add a filler note** (a note with a claim that no pattern predicts; it must score -1 for every hypothesis and never be chosen).
- Acceptance: with the fixture, "resonance is positive_feedback" is the top hypothesis with progress 0 or more, and taking it creates bridges to the retry storm and the microphone squeal. The filler note scores -1 everywhere.

## Tab 8: Inquiry agent (simulated science)

A hidden system with unknown dynamics. The agent runs experiments, learns, notices when nothing fits, invents, and predicts.

**World.** State x with optional velocity v. A hidden model is one of:

| name | step |
|---|---|
| pos (a in {0.2, 0.4}) | x' = x + a*x |
| neg (a in {0.3, 0.6}) | x' = x + a*(1 - x) |
| osc (a in {0.3, 0.6}) | x' = x + v; v' = v - a*(x - 1) (v starts at 0) |
| drift (a in {0.2, 0.4}) | x' = x + a |
| composite: sum(neg, pos) | x' = x + a_neg*(1 - x) + a_pos*x |
| composite: gate(pos, neg), logistic | x' = x + a*x*max(0, 1 - x/K), K in {2, 3} |

**Actions.** Run an experiment: start value x0 in {0.5, 1, 2} and watch time h in {3, 6}. Observation = the series of x for h steps plus Gaussian noise (sigma 0.08). Predict = name the pattern (ends the episode, reward +1 if right, -1 if wrong). Each experiment costs 0.05.

**Agent (an approximation of MC-AIXI).**
- Model: Bayesian mixture over the 8 library models (the first four rows with both parameter values), prior 2^-3 each, then normalised. Posterior update with the Gaussian likelihood of the observed series.
- Planner: UCT tree search over experiment sequences, depth 3, 120 simulations. Each rollout samples a world from the current posterior, simulates the chosen experiments, and ends by predicting the most probable family. Reward in the rollout = (beta times the information gain in bits of each experiment, beta = 0.5 when curiosity is on, 0 when off) minus experiment costs, plus the final prediction reward. Information gain = KL(posterior after || posterior before) in bits. Open-loop tree, one world per rollout.
- Stop rule: predict when predicting now is worth at least as much as the best next experiment and the top family has posterior of at least 0.6, or after 6 experiments.
- **Creativity switch:** after an experiment, compute the smallest reduced chi-square between the observation and any current model's mean series. If it is above 4, add composites of the library patterns (sum of two effects, or one effect gated by the other, with extra prior cost of 7 to 8 bits, i.e. 2^-10 to 2^-11), and re-score all past observations.
- Controls: curiosity on/off, creativity on/off, world type (known library law / new composite law), experiment cost (0.05, 0.3, 0.6), random-experiment baseline, run one episode with animation, run 100 episodes and show accuracy and average experiments.
- Canvas: the time series of each experiment against every model's predicted curve (greyed when its posterior mass is small), a bar chart of the posterior over families, a small tree showing the chosen action sequence.

**Acceptance (100 episodes each, tolerance +/- 0.12):**

| world | agent | accuracy | experiments |
|---|---|---|---|
| known library law | planner, curiosity on or off | 1.00 | about 1 |
| new composite law | planner, curiosity on, creativity on | 0.85-0.90 | about 3-3.5 |
| new composite law | planner, curiosity off, creativity on | about 0.33 | about 1.4 |
| new composite law | any agent, creativity off | 0.00 | 1-4 |
| new composite law | random experiments, creativity on | about 0.88 | 4 |

## Fixture: 12 sample notes

Use these as the default vault (domains: software, audio, ecology, finance). Claims are the extraction output a language model would give.

```json
[
 {"name":"retry-storm","domain":"software","text":"When a service slows, clients retry, which adds load, which slows it further. The queue explodes within minutes.","claims":[["slow_service","causes","retries"],["retries","causes","extra_load"],["extra_load","causes","slow_service"],["retry_storm","is","positive_feedback"]],"links":["outage-2024-03"]},
 {"name":"mic-squeal","domain":"audio","text":"A microphone near its own speaker picks up the sound, amplifies it and sends it out louder until a piercing whistle takes over.","claims":[["mic_gain","causes","speaker_loudness"],["speaker_loudness","causes","mic_gain"],["mic_squeal","is","positive_feedback"]],"links":[]},
 {"name":"resonance","domain":"physics","text":"Pushing a swing at its natural rhythm makes each swing bigger, so the next push adds to a larger motion.","claims":[["resonance","causes","runaway_growth"]],"links":[]},
 {"name":"thermostat","domain":"home","text":"When the room cools the heater switches on, and when it warms the heater switches off, which holds a steady temperature.","claims":[["thermostat","is","negative_feedback"],["heater_on","prevents","cold_room"]],"links":[]},
 {"name":"bank-run","domain":"finance","text":"Rumours make savers withdraw, which strains the bank, which fuels more rumours.","claims":[["bank_strain","causes","rumours"],["rumours","causes","withdrawals"],["withdrawals","causes","bank_strain"],["bank_run","is","positive_feedback"]],"links":[]},
 {"name":"caching-v1","domain":"software","text":"Caching every page makes the site faster for readers.","claims":[["caching","causes","faster_site"]],"links":[]},
 {"name":"caching-v2","domain":"software","text":"Caching now replaces [[caching-v1]]: stale pages slow the site down, so caching prevents speed on dynamic pages.","claims":[["caching","prevents","faster_site"]],"replaces":["caching-v1"],"links":["caching-v1"]},
 {"name":"yeast-help","domain":"kitchen","text":"Extra yeast makes the bread rise higher.","claims":[["extra_yeast","causes","taller_loaf"]],"links":[]},
 {"name":"yeast-hurt","domain":"kitchen","text":"Extra yeast makes the loaf collapse in the oven.","claims":[["extra_yeast","prevents","taller_loaf"]],"links":[]},
 {"name":"pitch-music","domain":"audio","text":"Pitch is how high a note sounds.","claims":[],"links":[]},
 {"name":"pitch-baseball","domain":"sports","text":"A pitch is a thrown ball.","claims":[],"links":[]},
 {"name":"standup","domain":"ops","text":"The team meets on Mondays to share news.","claims":[["standup","happens","monday"]],"links":[]}
]
```

Expected results on this fixture:
- Replaced: `caching-v1`.
- Disputes: `yeast-help` against `yeast-hurt` (one dispute). `caching-v1` against `caching-v2` is NOT a dispute because `caching-v1` is replaced.
- Bridges (shared pattern, different domain, no link): retry-storm with mic-squeal, retry-storm with bank-run, mic-squeal with bank-run.
- False friend: `pitch-music` with `pitch-baseball`.
- Curiosity: top hypothesis `resonance is positive_feedback` (saves the claim "resonance causes runaway_growth" only if some note states `[positive_feedback, causes, runaway_growth]`; add one such claim to `mic-squeal`, as `["positive_feedback","causes","runaway_growth"]`, so the hypothesis saves 1). Filler `standup` scores -1.
- Multi-hop query "why did the service fall over": seed `retry-storm`; hops to nothing else here, so add the three-note chain `deploy-bug` (claims deploy_bug causes slow_service), `slow-service` handled by retry-storm; the plain list must not contain `caching-v1` after dropping replaced notes.

(Gemini: if the multi-hop acceptance is too thin on 12 notes, add 3 chain notes: `deploy-bug` [deploy_bug causes slow_service], `retry-storm` as above, `outage-2024-03` [extra_load causes outage]; the query "why did the service fall over" should return the chain deploy-bug, retry-storm, outage-2024-03 under the warp but not under plain similarity.)

## Language-model hooks (optional, user pastes output)

Extraction prompt (show it in a copy box) and expected JSON `{"claims":[["subject","relation","object"],...]}`, relation in causes, prevents, is; subjects and objects lowercase snake_case; "is" only for these mechanisms: positive_feedback, negative_feedback, bottleneck, buffer, threshold_cascade, oscillation, redundancy, contagion.

Cross-domain grouping prompt and expected JSON `{"groups":[{"mechanism":"name","notes":["note-name","note-name"]}]}`. Playground action: verify each group with the Tab 4 loop check and a 2-edge common-subgraph check, and mark groups as confirmed or unconfirmed.

Graph prompt and expected JSON `{"edges":[["from","to","+"|"-"],...]}`, at most 7 edges, loops included when the note describes one.

## Do not include (did not work)

The commutativity-error score, embedding-only pattern invention, Weisfeiler-Lehman as a bridge finder, series-parallel egglog matching, extractor-claimed replacement. If you want a "what failed" tab, show them as a read-only table with the numbers from the report.

## Honest labels the UI must show

- "Toy embedding: the real system uses a neural embedding model."
- "Language-model steps are replaced by pasted output."
- "Numbers in the acceptance tests come from generated notes with clear planted patterns, not from real notes."
