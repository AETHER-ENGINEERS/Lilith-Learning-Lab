# 12. Quantifying Uncertainty

## Acting Under Uncertainty

An agent rarely knows the exact state of the world. Logic gives either "true" or "false", which breaks down when sensors are noisy or knowledge is incomplete. A **rational** agent weighs how likely each outcome is and how much it matters. **Decision theory = probability theory + utility theory.**

## Basic Probability Notation

- A **sample space** is the set of all possible worlds; a **probability model** assigns each world a number between 0 and 1, and the numbers add up to 1.
- A **proposition** is a set of worlds; its probability is the sum of the worlds in it.
- **Unconditional (prior) probability** P(a) is the belief before evidence. **Conditional probability** P(a | b) is the belief after learning b:

P(a | b) = P(a ∧ b) / P(b)

- **Random variables** have a *domain* (Weather could be sunny, rain, cloud, snow) and a *probability distribution* over it. A **joint distribution** gives the probability of every combination of values of several variables.

### Axioms (Kolmogorov)
1. 0 ≤ P(ω) ≤ 1 for every world.
2. The probabilities of all worlds sum to 1.
3. For any proposition, P(a) is the sum of the probabilities of the worlds in a.

Useful consequences: P(¬a) = 1 − P(a), and **inclusion-exclusion**: P(a ∨ b) = P(a) + P(b) − P(a ∧ b).

Why should an agent follow these axioms? If its betting odds violate them, a clever opponent can construct bets that guarantee the agent loses (the *Dutch book* argument).

## Inference Using Full Joint Distributions

With a full joint table you can answer any query by adding up matching entries. To get P(cavity | toothache):
1. Sum all entries where *toothache* is true to get P(toothache).
2. Sum the entries where both are true.
3. Divide.

**Normalisation** simplifies this: compute the unnormalised values for each answer and scale them so they sum to 1; the constant α replaces the division.

The problem: the table has 2ⁿ entries for n Boolean variables. It is useless in practice for large n, so we need structure.

## Independence

Two variables are **independent** if P(a, b) = P(a)P(b), that is, knowing one tells nothing about the other. Independence cuts a joint table into small independent pieces, but absolute independence is rare. A weaker, more useful idea is **conditional independence**: Toothache and Catch are independent *given* Cavity. Conditional independence turns exponential tables into products of small ones.

## Bayes' Rule and Its Use

**Bayes' rule** reverses a conditional:

P(b | a) = P(a | b) P(b) / P(a)

It matters because causal knowledge P(symptom | disease) is often easier to get than diagnostic knowledge P(disease | symptom).

| Term | Name |
|---|---|
| P(b) | prior |
| P(a \| b) | likelihood |
| P(b \| a) | posterior |
| P(a) | evidence (normaliser) |

**Worked example.** A disease affects 1 in 10,000 people. A test is 99% sensitive with a 1% false-positive rate. If you test positive, the chance you have the disease is only about 1%, because false positives from the huge healthy population outnumber true positives. Ignoring the prior (*base-rate neglect*) is a classic error.

Bayes' rule combines evidence naively as: P(cause | e₁, e₂) ∝ P(cause) P(e₁ | cause) P(e₂ | cause). This is the **naive Bayes** model: one cause with conditionally independent effects. It is simple, scales linearly and works surprisingly well for classification (for example, spam filtering).

## Summary

- Probability lets an agent express degrees of belief.
- Conditional independence is the key to compact representations.
- Bayes' rule turns causal knowledge into diagnostic inference.

# 13. Probabilistic Reasoning

## Bayesian Networks

A **Bayesian network** is a directed acyclic graph with:
- one **node** per random variable,
- an **edge** from X to Y when X directly influences Y (X is a *parent* of Y),
- a **conditional probability table (CPT)** P(X | Parents(X)) for every node.

The network represents the full joint distribution as a product of local terms:

P(x₁,...,xₙ) = ∏ P(xᵢ | parents(xᵢ))

A network with n Boolean variables and at most k parents per node needs only n·2ᵏ numbers instead of 2ⁿ.

### Building a network
1. Choose the variables.
2. Order them so causes come before effects (a **causal** ordering gives the smallest, most natural networks).
3. For each variable, pick as parents the earlier variables that directly affect it.
4. Fill in the CPTs.

### Example: burglar alarm
Burglary and Earthquake cause Alarm; Alarm causes JohnCalls and MaryCalls. From a handful of numbers you can compute questions like P(Burglary | JohnCalls, MaryCalls).

## Conditional Independence: d-separation

The graph structure encodes conditional independence:
- A variable is independent of its **non-descendants** given its **parents**.
- A variable is independent of every other variable given its **Markov blanket** (parents, children and children's other parents).
- **d-separation** is a graph test that says exactly which independencies hold given evidence. Three basic patterns: a **chain** (A→B→C) is blocked by observing B; a **common cause** (A←B→C) is blocked by observing B; a **collider** (A→B←C) is *opened* by observing B or any descendant (this is the "explaining away" effect: if the alarm rang and an earthquake happened, burglary becomes less likely).

## Efficient Representation of CPTs

Big CPTs can be written compactly:
- **Deterministic nodes** (value fixed by parents, e.g. NorthAmerican = Canadian ∨ US ∨ Mexican).
- **Noisy-OR:** each cause independently fails to produce the effect with some inhibition probability; needs only k numbers for k causes.
- **Continuous variables** use parametric forms such as the *linear Gaussian* and *logistic/probit* models for discrete children with continuous parents.

## Exact Inference

### Enumeration
Sum the joint over all hidden variables. Correct but repeats work.

### Variable elimination
Evaluate the sum right to left, storing intermediate results as **factors** and multiplying/summing out variables one at a time. Cost depends on the **elimination order** and the network's **treewidth**. For **polytrees** (singly connected networks) it is linear in the network size; for general networks the problem is **#P-hard**.

### Clustering (junction tree)
Group nodes into a tree of clusters to answer many queries after a single preprocessing step.

## Approximate Inference

When exact inference is too costly, use sampling:

| Method | Idea | Weakness |
|---|---|---|
| **Direct (prior) sampling** | sample variables in topological order | wastes samples that disagree with evidence |
| **Rejection sampling** | throw away samples that contradict the evidence | very wasteful when evidence is unlikely |
| **Likelihood weighting** | fix evidence, weight each sample by its likelihood | weights can become tiny in large networks |
| **Markov chain Monte Carlo (MCMC, Gibbs sampling)** | do a random walk over complete assignments, resampling one variable given its Markov blanket | needs time to "burn in" |

**Loopy belief propagation** passes messages on graphs with cycles; it often works well but may not converge.

## Causal Networks

A Bayesian network can be read as a **causal** model. The **do-operator** distinguishes *observing* X = x from *intervening* to set X = x. Intervention cuts the arrows into X. The **backdoor criterion** says which variables to adjust for to estimate a causal effect from observational data, and **counterfactuals** ask "what would have happened if...?" Causal reasoning explains why correlation is not causation.

## Summary

- Bayesian networks encode joint distributions compactly through conditional independence.
- Exact inference is polynomial on trees and hard in general; sampling and MCMC give approximate answers.
- Causal networks support reasoning about interventions.

# 14. Probabilistic Reasoning over Time

## Time and Uncertainty

To track a changing world, model it as a sequence of **time slices**. Each slice has hidden **state variables** Xₜ and observed **evidence variables** Eₜ.

Two assumptions simplify the model:
- **Markov assumption:** the current state depends only on a bounded history, usually the previous state: P(Xₜ | X₀:ₜ₋₁) = P(Xₜ | Xₜ₋₁).
- **Sensor (evidence) assumption:** the evidence depends only on the current state.

A **stationary process** has the same rules at every step. We need three things: a prior P(X₀), a **transition model** P(Xₜ | Xₜ₋₁) and a **sensor model** P(Eₜ | Xₜ).

## Inference Tasks

| Task | Question |
|---|---|
| **Filtering** | what is the belief state now, given all evidence so far? |
| **Prediction** | what will the state be k steps ahead? |
| **Smoothing** | what was the state at an earlier time, given all evidence up to now? |
| **Most likely explanation** | which sequence of states best explains the evidence? |

**Filtering** is done *recursively*: new belief = α · sensor model × (sum over old states of transition model × old belief). The cost per update is constant, so an agent can track the world forever.

**Smoothing** uses a forward pass and a backward pass (the **forward-backward algorithm**), with time linear in the sequence length.

**Viterbi** finds the most likely state sequence, by dynamic programming with "max" in place of "sum".

## Hidden Markov Models (HMMs)

An **HMM** has a single discrete state variable. With S states the transition model is an S×S matrix, so the filtering update is a matrix–vector product. Classic uses include speech recognition, gene finding and activity recognition. The matrix view makes **constant-space smoothing** and **online** algorithms possible.

### Example: locating a robot
A robot on a grid has noisy distance sensors. The HMM belief is a probability over grid cells. Each move spreads the belief (transition uncertainty), and each sensor reading sharpens it.

## Kalman Filters

A **Kalman filter** handles **continuous** state with *linear* dynamics and Gaussian noise. The belief stays Gaussian forever; it is described by a mean and covariance that are updated in closed form. It is used for tracking aircraft, GPS and navigation.

Its limits: it needs linear models and unimodal Gaussians. The **extended Kalman filter** linearises nonlinear models but can fail badly with strong nonlinearity.

## Dynamic Bayesian Networks (DBNs)

A **DBN** has several state variables per slice and edges between consecutive slices. HMMs and Kalman filters are special cases. A DBN is more compact than the equivalent HMM, since a factored state with n Boolean variables avoids a table of 2ⁿ × 2ⁿ numbers. Exact inference by "unrolling" the network is usually too costly, so we use:

- **Particle filtering:** keep N samples ("particles") of the state. At each step: (1) propagate each particle through the transition model, (2) weight it by the likelihood of the new evidence, (3) *resample* in proportion to the weights. The cost per update is constant and it handles non-Gaussian, nonlinear problems. It is the standard tool in robot localisation.

## Keeping Track of Many Objects

When several objects are tracked at once, the **data association** problem appears: which observation belongs to which object? Solutions use probabilistic assignment, the Hungarian algorithm, or MCMC.

## Summary

- Temporal models rest on the Markov and sensor assumptions.
- Filtering, prediction, smoothing and most-likely-sequence are the key tasks.
- HMMs, Kalman filters and DBNs are structured models; particle filters give general approximate inference.

# 15. Probabilistic Programming

## Relational Probability Models

Bayesian networks are like propositional logic: one node per ground fact. A **relational probability model (RPM)** brings FOL-like expressiveness. It defines random variables for *all objects* and relations through templates such as:

Honest(s) ~ Bernoulli(0.9) and Rating(r) depends on Quality(b) and Honest(Reviewer(r)).

A *book-rating* example: each book has a hidden quality; each customer has an honesty; each rating depends on both. One short program defines a network of any size.

Under **closed-universe semantics** you know the objects. With **open-universe** semantics you are uncertain about *how many* objects exist and which observations refer to which object (identity uncertainty). Examples: counting vehicles in video, or deciding if two web records are the same person.

## Probabilistic Programming Languages

A **probabilistic programming language (PPL)** lets you write a generative model as a program and handles inference automatically. Typical features:

- Random choices (`sample`) and **observations** (`observe` or conditioning).
- **Inference engines:** importance sampling, MCMC (including Hamiltonian Monte Carlo), variational inference.
- Language families: logic-based (BLOG, ProbLog), Lisp-style (Church, Venture), Python-embedded (Pyro, PyMC, Stan, NumPyro).

A *generative* model is easy to write; the PPL inverts it to answer "given the data, what are the parameters?".

### Example: a Bayesian coin
Model: bias ~ Uniform(0,1); each flip ~ Bernoulli(bias). Observe 7 heads in 10 flips. The posterior for the bias is concentrated near 0.7 with visible spread, giving honest uncertainty rather than a single point estimate.

## Inference in Probabilistic Programs

- **Likelihood weighting** and **importance sampling** on the program trace.
- **MCMC** proposes changes to random choices and accepts or rejects them (Metropolis–Hastings).
- **Variational inference** fits a simpler distribution to the posterior by optimisation.
- **Open-universe inference** uses MCMC moves that add or delete objects.

## Why It Matters

PPLs separate *modelling* from *inference*. They are used in:
- the CTBT seismic-monitoring system (detecting nuclear tests),
- cognitive science, epidemiology and astronomy,
- model-based machine learning.

## Summary

- RPMs define whole families of Bayesian networks with objects and relations.
- Open-universe models handle uncertainty about what exists.
- PPLs provide generic inference engines so that modelling is separate from algorithms.

# 16. Making Simple Decisions

## Combining Beliefs and Desires

A rational agent chooses the action with the highest **expected utility (EU)**:

EU(a) = Σ P(outcome | a) × U(outcome)

The principle of **maximum expected utility (MEU)** is the foundation of decision theory.

## The Basis of Utility Theory

If an agent's preferences satisfy a few *axioms of utility theory* (orderability, transitivity, continuity, substitutability, monotonicity, decomposability), then a utility function exists and the agent acts as if maximising its expectation. Violating transitivity makes the agent exploitable (a "money pump").

- **Utility** is only defined up to a positive linear transformation: the *ratios of differences* matter.
- A **normalised utility** gives 1 to the best prize and 0 to the worst catastrophe.
- The **micromort** (one-in-a-million chance of death) and **QALY** (quality-adjusted life year) are practical units used in health and safety.

## Utility Functions

### Money
People generally prefer a sure payoff to a gamble with the same expected money: they are **risk-averse**. The utility of money is *concave* (diminishing returns). The gap between the expected value of a gamble and its **certainty equivalent** is the **risk premium** (this is why insurance exists).

### Multiattribute utility
When outcomes have several attributes (cost, safety, time), use:
- **Dominance:** if option A is at least as good as B on every attribute, discard B.
- **Preference independence** and an **additive** value function V = Σ wᵢ Vᵢ(xᵢ).
- **Utility under uncertainty** with multiplicative or more complex forms.

### Common human biases
People violate the axioms systematically: the **Allais paradox**, the **Ellsberg paradox** (ambiguity aversion), **framing effects** and the **optimiser's curse** (picking the option with the highest *estimate* biases estimates upward). Prospect theory describes how people actually behave.

## Decision Networks

A **decision network** (influence diagram) extends a Bayesian network with:
- **chance nodes** (ovals): random variables,
- **decision nodes** (rectangles): the agent's choices,
- **utility nodes** (diamonds): the value of an outcome.

To decide: for each setting of the decision nodes, compute the expected utility with a Bayesian-network query, then choose the best.

### Example: airport siting
Decisions: where to build. Chance: noise, cost, accidents. Utility: a function of those. The network computes the expected utility of each site.

## The Value of Information

Sometimes it is worth paying for information before deciding. The **value of perfect information (VPI)** about a variable E is the expected increase in utility if we learn E before acting:

VPI(E) = (expected utility with knowledge of E) − (expected utility now)

Properties: VPI is never negative; it is not additive across several variables; and it depends on the order of acquisition. A good agent asks for information only when VPI exceeds the cost, which is the basis for *information-gathering* actions such as medical tests.

## Unknown Preferences

An agent may be uncertain about *what the human wants*. The **assistance game** formulation has a robot that does not know the human's utility function but tries to maximise it. The **off-switch** result: a robot that is uncertain about the human's preferences has a reason to *allow* itself to be switched off, because the human's action is evidence about what is best. A robot that is certain of its objective has no such incentive.

## Summary

- Rational choice is maximum expected utility; utility reflects preferences, risk attitude and multiple attributes.
- Decision networks combine probability and utility; information has computable value.
- Uncertainty about human preferences is central to building safe, beneficial AI.

# 17. Making Complex Decisions

## Sequential Decision Problems

In a **sequential** problem the utility depends on a *sequence* of decisions. In a stochastic, fully observable environment the problem is a **Markov decision process (MDP)**:
- a set of **states**, with an initial state,
- a set of **actions** for each state,
- a **transition model** P(s′ | s, a),
- a **reward function** R(s, a, s′).

The solution is a **policy** π(s) that gives an action for every state (a fixed plan is not enough, because the outcome is uncertain). The **optimal policy** π* maximises expected total (discounted) reward.

### Utilities over time
- **Finite horizon:** the best action may depend on the time left (nonstationary).
- **Infinite horizon** with **discount factor γ** < 1 makes the sum of rewards finite and the optimal policy stationary. The utility of a sequence is the **discounted sum** R₀ + γR₁ + γ²R₂ + ...

## Value Iteration

The **utility of a state** U(s) is the expected discounted sum of rewards from s under the optimal policy. It satisfies the **Bellman equation**:

U(s) = max over a of Σ P(s′ | s, a) [R(s, a, s′) + γ U(s′)]

**Value iteration** starts with arbitrary utilities and repeatedly applies the Bellman update to every state. It converges to the unique solution (the update is a **contraction**). Then the policy is read off by choosing the action that maximises the right-hand side. Convergence is faster for smaller γ.

## Policy Iteration

**Policy iteration** alternates two steps:
1. **Policy evaluation:** compute the utility of the current policy by solving a linear system (or by a few simple Bellman backups).
2. **Policy improvement:** make the policy greedy with respect to those utilities.

It stops when the policy no longer changes, which usually takes few iterations. It can be faster than value iteration. **Asynchronous** versions update states in any order and focus on important ones (prioritised sweeping).

## Partially Observable MDPs (POMDPs)

When the agent cannot see the state, we have a **POMDP**: an MDP plus a **sensor model** P(e | s). The agent maintains a **belief state** b (a probability distribution over states). The **optimal action depends only on the belief state**, so a POMDP is an MDP over a continuous belief space.

- The belief update after action a and percept e is the same as filtering.
- Value functions over belief space are piecewise linear and convex.
- Exact solution is intractable for all but tiny problems, so approximate methods are used: **point-based value iteration**, **online search** (look ahead over belief states with sampling, e.g. POMCP), and DBN-based representations.

A POMDP agent naturally values **information-gathering**: it acts to reduce uncertainty when that leads to better rewards later.

## Algorithms for Solving MDPs, at a Glance

| Algorithm | Needs | Idea |
|---|---|---|
| Value iteration | model | repeat Bellman updates |
| Policy iteration | model | evaluate, then improve |
| Online search | model + simulator | look ahead from the current state |
| Monte Carlo methods | simulator | estimate values from sampled trajectories |
| Reinforcement learning (Ch. 22) | experience only | learn without knowing the model |

## Summary

- MDPs model sequential decisions under uncertainty; solutions are policies.
- Value and policy iteration solve small MDPs exactly using the Bellman equation.
- POMDPs add partial observability and need belief states and approximation.

# 18. Multiagent Decision Making

## Properties of Multiagent Environments

When several agents act in the same world, each agent's best action depends on the others. Dimensions to consider: how many agents; whether they share goals (cooperative) or compete; whether they can communicate; and whether the environment is static or dynamic.

## Non-Cooperative Game Theory

A **game** has players, actions (strategies) and a **payoff** for each combination. A **pure strategy** picks one action; a **mixed strategy** randomises.

### Dominance and equilibrium
- A strategy is **dominant** if it is best regardless of what others do.
- A **Nash equilibrium** is a profile of strategies where no player can gain by changing alone. Every finite game has at least one Nash equilibrium (possibly mixed).
- **Prisoner's dilemma:** both players defect even though both would do better by cooperating. Defection is dominant, yet the outcome is **Pareto-dominated**.

| | Cooperate | Defect |
|---|---|---|
| **Cooperate** | 3, 3 | 0, 5 |
| **Defect** | 5, 0 | 1, 1 |

- **Zero-sum games** (one player's gain is the other's loss) are solved by the **minimax** and **maximin** values; mixed strategies from a **linear program** give the equilibrium (e.g. rock-paper-scissors).
- **Repeated games** allow cooperation to emerge via strategies like **tit-for-tat**.
- **Sequential games** are drawn as game trees; **imperfect information** is handled by information sets and by sequence-form linear programs (poker).

## Cooperative Game Theory

Players may form **coalitions** and share a payoff. The **core** is the set of fair divisions that no coalition wants to leave. The **Shapley value** assigns each player their average marginal contribution over all orderings of joining the coalition. These concepts price teamwork in settings such as cost sharing.

## Making Collective Decisions

### Auctions
Auction design aims to make bidding simple and results good for the seller or society.
- **English (ascending) auction:** bid up; the winner pays their bid.
- **Sealed-bid first-price:** the winner pays their bid, so bidders shade their bids.
- **Vickrey (second-price) auction:** the highest bidder wins but pays the *second-highest* bid. Bidding your true value is a **dominant strategy** (it is *strategy-proof*).

### Mechanism design
**Mechanism design** engineers the rules of a game so that self-interested agents produce a good collective outcome. The **revelation principle** says that we can restrict attention to mechanisms in which truthful reporting is optimal. The **VCG** mechanism makes each agent pay the harm they cause to others.

### Voting and social choice
**Arrow's theorem** says no ranking-based voting rule can satisfy a short list of reasonable fairness conditions at once. **Gibbard–Satterthwaite** says that any reasonable voting rule is open to manipulation. Rules include plurality, Borda count, approval voting and instant-runoff.

### Matching
**Stable matching** (Gale–Shapley) pairs students with schools or doctors with hospitals so that no two parties prefer each other to their assigned partners.

## Multiagent Planning and Coordination

For cooperative agents we need **joint plans** and **conventions** (shared expectations such as which side of the road to drive on). Mechanisms include communication, **joint intentions**, and **multibody planning**. Common models:
- **Decentralised POMDPs** (Dec-POMDPs), where agents share rewards but not observations,
- **task allocation** by auction or by contract-net protocols,
- **emergent behaviour** of swarms, ants and flocks from simple local rules.

Learning in multiagent environments (**multiagent reinforcement learning**) adds the difficulty that the environment is non-stationary because other agents are also learning.

## Summary

- Game theory analyses strategic interaction; Nash equilibrium is the main solution concept.
- Mechanism design, auctions and voting shape the rules so that good outcomes arise.
- Cooperation needs shared plans, conventions and communication.
