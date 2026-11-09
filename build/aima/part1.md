# 1. Introduction to AI

## What is AI?

Artificial Intelligence (AI) is the study and construction of **agents** that perceive an environment and act in it to achieve goals. The field has four classic ways of defining its aim: acting humanly (pass the Turing test), thinking humanly (model the mind), thinking rationally (follow the laws of logic) and acting rationally (do the best thing given what is known).

Modern AI mostly follows the last view. A **rational agent** chooses the action that is expected to maximise its performance measure, given what it has perceived. This definition is general: it covers a thermostat, a chess program and a self-driving car.

## The Standard Model and the Value Alignment Problem

In the *standard model* we build machines that optimise an objective that we specify. This works when the objective is complete, but a machine given a slightly wrong objective may pursue it with perfect efficiency and cause harm. This is the **value alignment problem**: making sure the machine's objectives match human preferences. A newer view builds machines that are uncertain about the true objective and therefore defer to people.

## A Short History

- **1943-1955:** artificial neurons (McCulloch and Pitts), Turing's paper on machine intelligence, early neural networks.
- **1956:** the Dartmouth workshop names the field "artificial intelligence".
- **1956-1969:** early enthusiasm: logic provers, game players, the perceptron.
- **1966-1973:** a dose of reality: combinatorial explosion, limits of single-layer perceptrons.
- **1969-1986:** expert systems capture human knowledge as rules.
- **1986 onward:** back-propagation revives neural networks; probability and statistics enter the mainstream.
- **2011 onward:** big data, fast hardware and deep learning give breakthroughs in vision, speech, games and language.

## State of the Art

AI systems now play Go and chess above human level, recognise images and speech, translate languages, drive vehicles in limited conditions, help diagnose disease and write text and code. Each of these successes is narrow; general intelligence remains an open goal.

## Risks and Benefits

Benefits include automation of dull work, scientific discovery and better health care. Risks include bias in decisions, loss of privacy, surveillance, misuse in weapons, job disruption and loss of control. Responsible AI means measuring and managing these risks from the start.

# 2. Intelligent Agents

## Agents and Environments

An **agent** maps what it perceives to an action. The sequence of everything it has perceived is the *percept sequence*. The **agent function** gives the action for each percept sequence; the **agent program** is the code that implements it.

## Good Behaviour: Rationality

A **performance measure** scores a sequence of environment states. A rational agent picks, for each percept sequence, the action expected to maximise that score using the knowledge it has. Rationality is not omniscience: it depends on what the agent knows and can perceive. It also includes **exploration** and **learning**: gathering information is part of acting well.

## The Task Environment (PEAS)

Describing a problem starts with PEAS: **P**erformance measure, **E**nvironment, **A**ctuators, **S**ensors. For an automated taxi: performance is safety, speed and comfort; the environment is roads and traffic; actuators are steering, brakes and horn; sensors are cameras, GPS and speedometer.

## Properties of Environments

| Property | Easy | Hard |
|---|---|---|
| Observability | Fully observable | Partially observable |
| Agents | Single agent | Multi-agent |
| Determinism | Deterministic | Stochastic |
| Episodes | Episodic | Sequential |
| Change | Static | Dynamic |
| State | Discrete | Continuous |
| Rules | Known | Unknown |

Chess is fully observable, deterministic, discrete and multi-agent. Taxi driving is partially observable, stochastic, sequential, dynamic and continuous: the hardest case.

## Structure of Agents

- **Simple reflex agents** act on the current percept using condition-action rules.
- **Model-based reflex agents** keep an internal state that tracks the parts of the world they cannot see, using a transition model and a sensor model.
- **Goal-based agents** consider the future consequences of actions in order to reach a goal.
- **Utility-based agents** score outcomes with a utility function so they can trade off conflicting goals and handle uncertainty.
- **Learning agents** add a learning element that improves the performance element, a critic that gives feedback, and a problem generator that proposes exploratory actions.

## How Agent Components Represent the World

Representations range from **atomic** (a state is a black box), through **factored** (a state is a set of variables with values), to **structured** (objects and relations between them). More expressive representations are more powerful but make reasoning and learning harder.

# 3. Solving Problems by Searching

## Problem-Solving Agents

A problem-solving agent with a goal finds a sequence of actions that reaches it. The process is: formulate the goal, formulate the problem, **search** for a solution, then execute it. This works best in observable, deterministic, discrete, known environments.

## Formal Definition of a Search Problem

A search problem consists of:

- a set of **states** (the state space);
- an **initial state**;
- one or more **goal states** (or a goal test);
- the **actions** available in each state;
- a **transition model** giving the result of an action;
- an **action cost** function.

A **solution** is a path from the initial state to a goal; an **optimal** solution has the lowest path cost. Example: route finding on a map, where states are cities, actions are drives and cost is distance.

## Search Algorithms

Search builds a **search tree** from the initial state. A node holds a state, its parent, the action that led to it and the path cost. The **frontier** is the set of nodes that have been generated but not expanded. The generic loop: take a node from the frontier, test it, expand it and add the children. A **reached** table avoids revisiting states (graph search).

### Measuring performance

- **Completeness:** does it find a solution if one exists?
- **Cost optimality:** is the solution the cheapest?
- **Time complexity** and **space complexity**, in terms of branching factor *b*, solution depth *d* and maximum depth *m*.

## Uninformed (Blind) Search

| Algorithm | Frontier | Complete | Optimal | Time | Space |
|---|---|---|---|---|---|
| Breadth-first | FIFO queue | Yes | Yes (equal costs) | O(b^d) | O(b^d) |
| Uniform-cost | Priority by path cost | Yes | Yes | O(b^(1+C*/e)) | same |
| Depth-first | LIFO stack | No (infinite paths) | No | O(b^m) | O(bm) |
| Depth-limited | Stack with a depth limit l | No | No | O(b^l) | O(bl) |
| Iterative deepening | Repeated depth-limited | Yes | Yes (equal costs) | O(b^d) | O(bd) |
| Bidirectional | Two frontiers | Yes | Yes (equal costs) | O(b^(d/2)) | O(b^(d/2)) |

**Breadth-first** expands the shallowest node first, so it finds the shortest path in steps but uses much memory. **Uniform-cost** expands the node with the lowest path cost. **Depth-first** uses little memory but can get lost. **Iterative deepening** combines the memory of depth-first with the completeness of breadth-first and is the preferred blind method for large spaces.

## Informed (Heuristic) Search

A **heuristic** h(n) estimates the cost from node n to a goal. It lets the search prefer promising nodes.

- **Greedy best-first search** expands the node with the smallest h(n). It is fast but neither optimal nor complete in general.
- **A\* search** expands the node with the smallest f(n) = g(n) + h(n), where g(n) is the cost so far. If h is **admissible** (never overestimates) and, for graph search, **consistent** (h(n) <= c(n, a, n') + h(n')), A\* is complete and optimal.
- **Weighted A\*** uses f = g + W h with W > 1: faster, but only bounded-suboptimal.
- **Memory-bounded variants:** IDA\*, recursive best-first search (RBFS) and simplified memory-bounded A\* (SMA\*).

### Designing heuristics

Good heuristics come from **relaxed problems**: remove constraints, solve the easier problem exactly, and use its cost. For the 8-puzzle, ignoring that tiles block each other gives the **Manhattan distance**. Another source is **pattern databases**, which store exact costs of solving sub-problems, and **learning** heuristics from experience. A heuristic that dominates another (always at least as large, still admissible) expands fewer nodes.

# 4. Search in Complex Environments

## Local Search and Optimisation

When the path does not matter and only the final state does (scheduling, circuit layout, n-queens), **local search** keeps a single current state and moves to neighbours. It uses little memory and works in huge spaces. The landscape has a **global maximum**, **local maxima**, **ridges** and **plateaus**.

- **Hill climbing** moves to the best neighbour and can stall at local maxima. Variants: stochastic, first-choice, random-restart.
- **Simulated annealing** sometimes accepts a worse move with probability e^(dE/T), where the temperature T falls slowly. Early randomness escapes local maxima; later it settles.
- **Local beam search** keeps k states, choosing the best k successors of all of them.
- **Evolutionary algorithms** keep a population, select fit individuals, recombine them (crossover) and mutate them.

## Search in Continuous Spaces

For continuous variables, use **gradient ascent or descent**: x <- x + alpha grad f(x). **Newton-Raphson** uses second derivatives for faster convergence. **Constrained optimisation** adds restrictions; **linear programming** has linear objective and constraints and can be solved efficiently, and **convex optimisation** generalises this.

## Search with Nondeterministic Actions

When actions have uncertain outcomes, a solution is a **contingency plan**, not a path. It uses conditional branches (if-then-else). An **AND-OR search tree** has OR nodes (the agent chooses an action) and AND nodes (all possible outcomes must be handled).

## Search in Partially Observable Environments

With no or limited sensing the agent works with a **belief state**: the set of states it might be in. In a **sensorless** (conformant) problem, a plan must work from any state in the belief set. In general, after each action and percept the belief state is updated (predict, then update with the percept).

## Online Search and Unknown Environments

In **online search** the agent must act and explore at once, because it does not know the map or the effects of actions. It must also be able to undo moves (safe exploration). **Online DFS** and **LRTA\*** (learning real-time A\*) improve their cost estimates as they travel.

# 5. Adversarial Search and Games

## Game Theory Basics

AI studies deterministic, turn-taking, two-player, zero-sum, perfect-information games such as chess and Go. A game has an initial state, a to-move function, actions, a result function, a terminal test and a **utility** at terminal states. The agent is MAX, the opponent MIN.

## Minimax Search

The **minimax value** of a node is the utility for MAX of playing optimally from there, assuming MIN also plays optimally. MAX chooses the maximum of the children's values; MIN the minimum. Minimax is a depth-first search of the game tree. Its time is O(b^m); the space is O(bm).

## Alpha-Beta Pruning

Alpha-beta pruning gives the same answer as minimax but skips branches that cannot affect the result. **alpha** is the best value found so far for MAX along the path; **beta** is the best for MIN. If a node's value is already worse for the player than an option available earlier, the rest of its children are skipped. With perfect move ordering, the time falls to O(b^(m/2)), allowing about twice the search depth. Good ordering uses **killer moves**, the best move from a shallower search, and **transposition tables** that cache positions already evaluated.

## Heuristic Evaluation and Cutoffs

Real games are too large to search to the end. Instead, cut off the search at a depth limit and apply a **heuristic evaluation function** that estimates the utility of a non-terminal position, typically a weighted sum of features such as material and mobility. Techniques include **iterative deepening**, quiescence search (continue in unstable positions) and forward pruning.

## Monte Carlo Tree Search

MCTS builds a search tree selectively using random playouts. Four steps repeat: **selection** (descend by a policy such as UCB1, which balances exploitation and exploration), **expansion**, **simulation** (a playout to the end) and **backpropagation** of the result. It works without a hand-written evaluation function and powers modern Go programs, where it was combined with neural networks in AlphaGo.

## Stochastic Games

With chance (dice, cards) add **chance nodes**: a node's value is the expected value over outcomes. This is **expectiminimax**. Because the evaluation function must now measure expected utility, it should be a positive linear transformation of the true probability of winning.

## Limitations

Game search assumes a known model and exact rules. Its limits include huge branching factors (Go), partial observability (poker) and the need for a good evaluation. Modern systems learn both policy and evaluation by self-play.

# 6. Constraint Satisfaction Problems

## Defining a CSP

A **constraint satisfaction problem** has variables X1..Xn, each with a domain of values, and constraints that limit the combinations. A solution assigns every variable a value that satisfies all constraints. Examples: map colouring (adjacent regions differ), Sudoku, scheduling, circuit layout.

Constraints can be unary, binary, or higher-order (global constraints such as *Alldiff*). A binary CSP is drawn as a **constraint graph**.

## Constraint Propagation

**Inference** reduces domains by enforcing local consistency:

- **Node consistency:** every value satisfies the unary constraints.
- **Arc consistency:** for every arc (Xi, Xj), each value of Xi has some compatible value in Xj. The **AC-3** algorithm repeatedly revises arcs and re-queues affected neighbours, in O(c d^3) time.
- **Path consistency** and **k-consistency** check larger groups of variables.
- **Global constraints** use special algorithms, for example *Alldiff* detects when m variables share fewer than m values.

## Backtracking Search

**Backtracking** assigns one variable at a time and backs up when a conflict appears. It is smarter with heuristics:

- **Minimum remaining values (MRV):** pick the variable with the fewest legal values.
- **Degree heuristic:** break ties by the most constraints on unassigned variables.
- **Least constraining value:** try the value that rules out the fewest options for neighbours.
- **Forward checking and MAC** (maintaining arc consistency) propagate after every assignment.
- **Conflict-directed backjumping** returns to the variable that actually caused the failure.

## Local Search for CSPs

**Min-conflicts** starts with a full assignment and repeatedly changes a variable in conflict to the value that causes the fewest conflicts. It solves n-queens for a million queens in a few steps, and is widely used for scheduling.

## Problem Structure

If the constraint graph is a **tree**, the CSP can be solved in O(n d^2) by making it arc-consistent from the leaves to the root. General graphs can be reduced by **cutset conditioning** (fix a set of variables so the rest forms a tree) or by **tree decomposition**. Symmetries can be broken with extra constraints to cut the search.
