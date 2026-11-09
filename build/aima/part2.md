# 7. Logical Agents

## Knowledge-Based Agents

A **knowledge-based agent** keeps a **knowledge base (KB)**: a set of sentences written in a formal language. It works in a loop. It TELLs the KB what it perceives, ASKs the KB what to do, and then TELLs the KB which action it took. The big idea is the split between *what the agent knows* (the sentences) and *how it reasons* (the inference procedure). You can improve either one without touching the other.

Two styles of building the KB exist. The **declarative** approach writes down facts and lets inference do the rest. The **procedural** approach hard-codes behaviour. Real agents usually mix both.

## The Wumpus World

The wumpus world is a small grid cave used as a running example. It contains a monster (the wumpus), bottomless pits and a heap of gold. The agent perceives a *stench* next to the wumpus, a *breeze* next to a pit, a *glitter* on the gold square, a *bump* when it hits a wall, and a *scream* when the wumpus dies.

| Feature | Value |
|---|---|
| Environment | Partially observable, discrete, static, sequential |
| Goal | Grab the gold and climb out alive |
| Danger | Falling into a pit, meeting a live wumpus |
| Actions | Move forward, turn, grab, shoot (one arrow), climb |

The agent cannot see which squares are safe. It must *infer* safety from breezes and stenches. For example, if square [1,2] has no breeze, then neighbouring squares cannot hold a pit.

## Logic: Syntax, Semantics, Models

- **Syntax** says which strings are well-formed sentences.
- **Semantics** says what a sentence means: in each possible world (a **model**) it is true or false.
- A sentence **entails** another (written α ⊨ β) when β is true in every model where α is true.
- A procedure is **sound** if it derives only entailed sentences, and **complete** if it can derive every entailed sentence.

Model checking enumerates models to test entailment. It is easy to understand but costs time exponential in the number of symbols.

## Propositional Logic

Propositional logic uses symbols that are true or false, joined by the connectives **not (¬)**, **and (∧)**, **or (∨)**, **implies (⇒)** and **if and only if (⇔)**.

Useful facts:
- A sentence is **valid** if true in all models (a tautology) and **satisfiable** if true in at least one.
- Inference rules such as **modus ponens** (from α and α ⇒ β, conclude β) and **resolution** are sound.
- **Conjunctive normal form (CNF)** is an AND of ORs of literals; any sentence can be converted to it.

### Wumpus rules in propositional form

Let B(x,y) mean "breeze at x,y" and P(x,y) mean "pit at x,y". The rule "a square is breezy exactly when a neighbour has a pit" is written once per square:

B(1,1) ⇔ (P(1,2) ∨ P(2,1))

The weakness is clear: one rule per square, so the KB grows with the cave.

## Inference by Theorem Proving

### Resolution

Resolution takes two clauses that contain complementary literals and produces a new clause without them. To prove KB ⊨ α, add ¬α to the KB, convert to CNF and resolve repeatedly. If the **empty clause** appears, the set is contradictory and α follows. Resolution is sound and complete for propositional logic.

### Horn clauses and chaining

A **Horn clause** has at most one positive literal. KBs made only of Horn clauses allow very fast inference:
- **Forward chaining** starts from known facts and fires rules whose premises are all true, until the query appears. It is *data-driven*.
- **Backward chaining** starts from the query and looks for rules that conclude it, then tries to prove their premises. It is *goal-driven*.

Both run in time linear in the size of the KB.

## Efficient Model Checking: SAT Solvers

The **SAT problem** asks whether a propositional formula is satisfiable. It is NP-complete, yet modern solvers handle formulas with millions of variables.

- **DPLL** is a backtracking search with three tricks: *early termination*, *pure symbol heuristic* and *unit clause heuristic*.
- **CDCL** (conflict-driven clause learning) adds *learned clauses* so the same mistake is never repeated.
- **Local search** such as WalkSAT flips variables to reduce unsatisfied clauses; it is incomplete but often fast.

Many planning and verification problems are turned into SAT and handed to a solver.

## Agents Based on Propositional Logic

A **logical agent** can keep a *current-state* belief: which squares are known safe, which may hold pits. It uses **fluents** (facts that change over time) with a time index, and **effect axioms** plus **frame axioms** (what does *not* change). The frame problem is the cost of writing all the "unchanged" facts. **Successor-state axioms** say, for each fluent, how it becomes true at the next step.

## Summary

- A knowledge-based agent TELLs and ASKs a KB.
- Logic gives syntax, semantics and entailment; inference should be sound and ideally complete.
- Resolution is complete for propositional logic; Horn-clause chaining is linear.
- SAT solvers (DPLL, CDCL, WalkSAT) make propositional reasoning practical.
- Propositional logic is limited because it cannot talk about objects and relations compactly.

# 8. First-Order Logic

## Why Go Beyond Propositional Logic

Propositional logic has no way to say "all squares next to a pit are breezy" in one sentence. **First-order logic (FOL)** adds **objects**, **relations** and **functions**, and the **quantifiers** *for all* (∀) and *there exists* (∃). It is expressive enough for most of mathematics and much of common sense.

## Syntax and Semantics

| Element | Meaning | Example |
|---|---|---|
| Constant | names one object | Richard, John |
| Predicate | a relation among objects | Brother(Richard, John) |
| Function | maps objects to an object | LeftLeg(John) |
| Variable | stands for any object | x |
| Quantifier | ∀x or ∃x | ∀x King(x) ⇒ Person(x) |
| Equality | two terms are the same object | Father(John) = Henry |

A **model** in FOL contains a set of objects (the *domain*) and an *interpretation* that says which object each constant names, and which tuples satisfy each predicate.

### Quantifier rules of thumb
- Use **⇒** with **∀**: "all kings are persons" is ∀x King(x) ⇒ Person(x).
- Use **∧** with **∃**: "some king is crazy" is ∃x King(x) ∧ Crazy(x).
- ¬∀x P is the same as ∃x ¬P, and ¬∃x P is the same as ∀x ¬P.

Getting these pairings wrong is the most common beginner mistake.

## Using First-Order Logic

### Assertions and queries
TELL the KB facts such as King(John); ASK queries such as ∃x Person(x). The answer may be a **substitution** (binding list) such as {x/John}.

### Domains
- **Kinship:** Parent, Mother, Grandparent are defined from a few base predicates.
- **Numbers and sets:** Peano axioms define the natural numbers; set axioms define membership, union and subset.
- **Lists:** Nil and Cons build sequences.

### The wumpus world in FOL
Perception rules link percepts to the world: "if the agent perceives a breeze at time t then the agent's square is breezy." One general rule replaces dozens of propositional ones:

∀s Breezy(s) ⇔ ∃r Adjacent(r, s) ∧ Pit(r)

## Knowledge Engineering in FOL

A reliable process for building a KB:
1. **Identify the task** (which questions must the KB answer?).
2. **Assemble the knowledge** from experts and documents.
3. **Decide on a vocabulary** of predicates, functions and constants (the *ontology*).
4. **Encode general knowledge** as axioms.
5. **Encode a specific problem instance.**
6. **Pose queries** and get answers.
7. **Debug** the KB: missing axioms give "cannot prove", wrong axioms give wrong proofs.

## Summary

- FOL adds objects, relations, functions and quantifiers to propositional logic.
- Pair ∀ with ⇒ and ∃ with ∧.
- A good ontology and a careful knowledge-engineering process matter as much as the logic.

# 9. Inference in First-Order Logic

## Reducing to Propositional Inference

**Universal instantiation** replaces a universally quantified variable by a ground term. **Existential instantiation** replaces ∃ with a new constant (a *Skolem constant*). By instantiating with every possible ground term, a FOL KB can be turned into a propositional one. With functions the set of ground terms is infinite, but **Herbrand's theorem** says that if a sentence is entailed, a finite subset of instantiations proves it. FOL entailment is **semidecidable**: algorithms can say yes to every entailed sentence, but may run forever on a non-entailed one.

## Unification and Lifting

Instantiating blindly creates many useless facts. **Lifted inference** works with variables directly. The key tool is **unification**: find a substitution that makes two expressions identical.

| Pair | Unifier |
|---|---|
| Knows(John, x) and Knows(John, Jane) | {x/Jane} |
| Knows(John, x) and Knows(y, Mother(y)) | {y/John, x/Mother(John)} |
| Knows(John, x) and Knows(x, Elizabeth) | fails (same variable x) |

The **most general unifier (MGU)** is unique up to renaming. The **occur check** prevents binding a variable to a term that contains it.

**Generalised modus ponens** applies a rule whose premises unify with known facts and produces the substituted conclusion.

## Forward Chaining

A **definite clause** has exactly one positive literal. Forward chaining repeatedly fires any rule whose premises unify with known facts and adds the new conclusion, until the query is derived or nothing changes. For *Datalog* knowledge bases (no function symbols) it terminates and is complete. Efficiency tricks include:
- **Pattern matching** of rule premises against facts (the *Rete* network keeps partial matches).
- **Incremental forward chaining:** only rules affected by a new fact are rechecked.
- **Irrelevant facts:** magic sets restrict work to facts relevant to the goal.

Forward chaining powers **production systems** and **deductive databases**.

## Backward Chaining

Backward chaining starts with the goal and finds rules whose conclusion unifies with it, then proves their premises depth-first, passing along the growing substitution. It is the engine of **Prolog**.

- It is a depth-first search, so it uses little memory.
- It can loop forever (left recursion) and repeat work; **tabling** fixes the repetition.
- **Logic programming** (Prolog) uses Horn clauses, the *closed world assumption* and *negation as failure*.

## Resolution

For FOL, convert sentences to **clausal form**:
1. Eliminate implications.
2. Move negation inward.
3. Standardise variables apart.
4. **Skolemise** to remove existential quantifiers.
5. Drop universal quantifiers.
6. Distribute ∨ over ∧.

The **resolution rule** unifies a literal with the negation of one in another clause. Resolution is **refutation-complete**: if KB ∧ ¬α is unsatisfiable, resolution will find the empty clause. Practical provers add strategies such as *unit preference*, *set of support*, *input resolution* and **subsumption** (delete clauses that are less general than another). Equality is handled with *paramodulation* or a **demodulation** rewrite.

Theorem provers have proved real results: the Robbins conjecture, and they are used to verify hardware and software.

## Summary

- Lifted inference uses unification to avoid blind instantiation.
- Forward chaining suits data-driven problems; backward chaining suits goal-driven problems.
- Resolution is refutation-complete for FOL, though search may not halt.

# 10. Knowledge Representation

## Ontological Engineering

An **ontology** organises the concepts of a domain. An **upper ontology** describes the most general concepts (objects, events, time, substances) that every domain shares.

## Categories and Objects

- Categories group objects. They can be **predicates** (Basketball(b)) or **objects** (Basketballs) so we can state properties of the category itself.
- **Inheritance** passes properties down a hierarchy: members of a subclass have the properties of its superclass.
- **Physical composition** (PartOf) and **measurements** (Length(x) = Inches(1.5)) extend the vocabulary.
- **Natural kinds** (tigers) differ from **defined kinds** (bachelor) because they have no crisp definition.

## Events and Time

**Event calculus** describes *fluents* and the events that start (Initiates) or end (Terminates) them, and the times at which they hold. Intervals, ordering and **processes** (continuous events such as flying) are represented with predicates such as Meet, Before, During and Overlap.

## Mental Objects and Modal Logic

To talk about what agents *know* or *believe*, we need **modal logic**: operators like K_A(P) ("A knows P") whose arguments are propositions, not objects. Possible-world semantics gives them meaning. The alternative is to treat sentences as **reified** objects (strings) in FOL.

## Reasoning Systems for Categories

- **Semantic networks** draw categories as nodes and relations as links; fast inheritance is their strength.
- **Description logics** define concepts from other concepts with operators such as And, All, AtLeast. The core tasks are *subsumption* (is concept A a subset of B?) and *classification*. They underlie the **Web Ontology Language (OWL)** and the semantic web.

## Reasoning with Default Information

Common sense uses defaults: "birds fly" is true unless the bird is a penguin. Reasoning that takes back conclusions when new facts arrive is **nonmonotonic**.

- **Circumscription** minimises the abnormal cases.
- **Default logic** adds rules like "if P holds and it is consistent that Q, conclude Q."
- **Truth maintenance systems (TMS)** record why each belief is held, so beliefs can be retracted when their justification disappears.
- The **closed-world assumption** treats anything not provably true as false.

## Summary

- Ontologies organise concepts; categories support inheritance.
- Event calculus represents change; modal logic represents belief and knowledge.
- Description logics power knowledge graphs and OWL.
- Nonmonotonic reasoning handles defaults and exceptions.

# 11. Automated Planning

## The Planning Problem

**Planning** finds a sequence of actions that achieves a goal. Unlike search with a black-box successor function, planning uses a **factored representation**: states are sets of propositions, and actions are described by their effects.

### PDDL

The **Planning Domain Definition Language (PDDL)** describes:
- the **initial state** (a conjunction of ground atoms),
- **actions** with *preconditions* (what must hold) and *effects* (what becomes true or false),
- the **goal** (a conjunction of literals).

Example action (air cargo):

*Fly(p, from, to)*: precondition At(p, from) ∧ Plane(p) ∧ Airport(from) ∧ Airport(to); effect ¬At(p, from) ∧ At(p, to).

The **closed-world assumption** applies: anything not listed is false. The **STRIPS** assumption means effects only change what is listed, so the frame problem disappears.

## Algorithms for Classical Planning

| Approach | Idea |
|---|---|
| **Forward state-space search** | start at the initial state, apply applicable actions |
| **Backward (regression) search** | start from the goal, work back to the start |
| **SAT planning** | encode "a plan of length k exists" as a SAT problem |
| **Planning graph (GRAPHPLAN)** | layered graph of possible facts and actions; extracts plans |
| **Partial-order planning** | commit only to needed orderings |

### Heuristics for planning
Good heuristics come from **relaxed problems**:
- **Ignore preconditions:** each action may be done anytime.
- **Ignore delete lists:** actions never remove facts (very effective; used in FF and its descendants).
- **State abstraction:** merge states to build a pattern database.

### Planning graphs
A planning graph alternates *state levels* and *action levels*. **Mutex links** mark pairs of actions or facts that cannot hold together. If a goal fact never appears, or only appears mutex, the goal is unreachable within that many steps. The level at which all goal facts appear gives an admissible heuristic.

## Hierarchical Planning

A **hierarchical task network (HTN)** starts with a high-level action and refines it using **methods** into lower-level steps until only primitive actions remain. It lets experts write the structure of good plans ("to travel: book, pack, go") and scales to very large problems. **Angelic** semantics reason about the set of outcomes a high-level action might achieve.

## Planning and Acting in Nondeterministic Domains

When the world is not fully predictable, plans become more complex:
- **Sensorless (conformant) planning** finds a plan that works without observations.
- **Contingent planning** builds a plan with conditional branches ("if the door is locked, then ...").
- **Online planning** interleaves planning, acting and **replanning**.

States become **belief states** (sets of possible states). Fast progress comes from **monitoring** the execution and replanning when something unexpected occurs.

## Time, Schedules and Resources

Real planning needs durations and resources. A **scheduling** problem assigns start times to actions under ordering constraints and resource limits. The **critical path method** finds the longest chain of dependent actions and hence the shortest possible total time. Hierarchical planning and constraint solving are combined for jobs such as factory production and space-mission operations.

## Analysis of Planning Approaches

- Forward search with good heuristics is the dominant approach for classical planning.
- SAT-based planning wins when plans are short and highly constrained.
- HTN planning is the practical choice when domain knowledge about plan structure is available.

## Summary

- PDDL describes states, actions, and goals in a factored way.
- Relaxed-problem heuristics make forward search effective.
- HTNs, contingent plans and online replanning extend planning to realistic settings.
