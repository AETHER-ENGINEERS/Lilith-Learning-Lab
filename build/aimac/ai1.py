"""Artificial Intelligence course, chapters 1-5."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

A = []

A.append(CH(
 "What AI is: rational agents",
 ("Agents", [
  "Agent | perceives with | Sensors", "Agent | acts with | Actuators", "Rational agent | maximises | Expected performance",
  "Performance measure | defines | Success", "PEAS | describes | A task environment", "Environment | can be | Partially observable",
  "Learning agent | improves | Its performance element"]),
 ["Artificial intelligence is the study of building agents: things that perceive an environment and act in it. This course follows the structure of the textbook Artificial Intelligence: A Modern Approach by Russell and Norvig, condensed and re-explained in original words.",
  "The central idea is the rational agent. It picks the action that is expected to give the best score on a performance measure, given what it has perceived so far.",
  "Rationality is not perfection. The agent cannot know what it could not perceive. It is judged on expected, not lucky, outcomes."],
 [("Agent", "Anything that perceives its environment through sensors and acts through actuators."),
  ("Percept sequence", "Everything the agent has perceived so far."),
  ("Rational agent", "An agent that chooses the action with the best expected performance."),
  ("Performance measure", "The score that says how well the environment is doing."),
  ("PEAS", "Performance measure, Environment, Actuators, Sensors."),
  ("Fully observable", "The sensors give the whole relevant state.")],
 ["An agent maps percept sequences to actions.", "Rational means best expected performance, not omniscient.",
  "Describe a task with PEAS before designing the agent.", "Environments differ: observable or not, deterministic or not, episodic or sequential, static or dynamic.",
  "Agent types: simple reflex, model-based, goal-based, utility-based, learning.", "The standard model: optimise a fixed objective. Its danger is a wrong objective."],
 [T("Early definitions of AI argued about whether a machine should think like a human or act like one, and whether it should be judged by human behaviour or by an ideal standard. The approach that won out in practice is to define AI by what an agent does: it should act to achieve its goals as well as it can."),
  T("An agent is a function from everything it has perceived to an action. A table listing an action for every possible history would be astronomically large, so real agents are programs that compute the action compactly."),
  T("Consider a vacuum cleaner agent in two rooms. Its sensors tell it which room it is in and whether that room is dirty. Its actuators let it move left, move right or suck. A sensible performance measure awards one point per clean room per time step. Notice the measure is about the world, not about how the agent feels."),
  T("Task environments are described by PEAS. For an automated taxi: the performance measure covers safety, speed, comfort and cost; the environment is roads, traffic and pedestrians; the actuators are steering, brakes and horn; the sensors are cameras, radar and GPS."),
  T("Five agent designs grow in power. A simple reflex agent reacts to the current percept with condition-action rules. A model-based agent keeps an internal picture of the world. A goal-based agent searches for actions that reach a goal. A utility-based agent weighs trade-offs with a numeric utility. A learning agent improves any of these from experience."),
  T("Modern AI mostly follows the standard model: build a machine that optimises an objective we give it. This works only if the objective is right. A very capable machine with a slightly wrong objective can do real harm, which is why later chapters return to uncertainty about objectives and to ethics.")],
 [("Which describes a rational agent?", ["It maximises expected performance given what it perceived", "It always makes the perfect move", "It copies human behaviour", "It never learns"], 0, "Rationality is about expected outcomes."),
  ("What does PEAS stand for?", ["Performance, Environment, Actuators, Sensors", "Plan, Execute, Act, Search", "Percept, Effect, Action, State", "Probability, Entropy, Axioms, Sets"], 0, "It describes the task environment."),
  ("Which agent weighs trade-offs between outcomes?", ["Utility-based", "Simple reflex", "Table-driven", "Random"], 0, "Utility scores compare outcomes.")],
 [("What is a percept sequence?", "Everything perceived so far."), ("Why is a lookup table agent impractical?", "The table is astronomically large."), ("What is the standard model?", "Optimise a fixed objective."), ("What do actuators do?", "Let the agent act on the world.")],
 [MATCH("Agent types", "Match each agent with what it adds.", [("Simple reflex", "Condition-action rules"), ("Model-based", "Internal state of the world"), ("Goal-based", "Searches for goal states"), ("Utility-based", "Numeric trade-offs"), ("Learning", "Improves from experience")]),
  FILL("PEAS", "To describe a task, list the {{performance|performance measure}}, the environment, the {{actuators}} and the sensors."),
  PL("Vacuum score", "Write vacuum_score(history): history is a list of states, each a list of two numbers (1 = room dirty, 0 = clean). Return the number of clean rooms summed over all time steps.",
     "vacuum_score(history)", """
def vacuum_score(history):
    s = 0
    for st in history:
        for d in st:
            if d == 0:
                s += 1
    return s
""", [[[[1, 1], [0, 1], [0, 0]]], [[[0, 0]]], [[[1, 1], [1, 1]]], [[[0, 1], [0, 1], [0, 0], [0, 0]]]], "Count the zeros.", approx=None),
  PL("Reflex vacuum", "Write reflex_action(percept): percept is [location, status] with location 'A' or 'B' and status 'dirty' or 'clean'. Return 'suck' if dirty, otherwise 'right' at A and 'left' at B.",
     "reflex_action(percept)", """
def reflex_action(percept):
    loc, status = percept[0], percept[1]
    if status == 'dirty':
        return 'suck'
    if loc == 'A':
        return 'right'
    return 'left'
""", [[["A", "dirty"]], [["B", "dirty"]], [["A", "clean"]], [["B", "clean"]]], "Three condition-action rules.", approx=None)]))

A.append(CH(
 "Solving problems by search",
 ("Search", [
  "Search | explores | A state space", "Frontier | holds | Unexpanded nodes", "Breadth-first | finds | Shortest path in steps",
  "Uniform-cost | finds | Cheapest path", "A* | uses | Cost plus heuristic", "Admissible heuristic | never | Overestimates",
  "Iterative deepening | saves | Memory"]),
 ["A problem-solving agent looks ahead. It models the world as states and actions, then searches for a sequence of actions leading to a goal.",
  "Uninformed methods use only the problem definition: breadth-first, uniform-cost, depth-first and iterative deepening. Informed methods use a heuristic estimate of the remaining cost. A star search combines the cost so far with that estimate and is optimal when the estimate never overestimates.",
  "The labs write breadth-first search and A star on a small graph."],
 [("State space", "All states reachable from the start by any actions."),
  ("Frontier", "Nodes that are generated but not yet expanded."),
  ("Heuristic", "An estimate h(n) of the cost from n to the goal."),
  ("Admissible", "A heuristic that never overestimates the true cost."),
  ("Branching factor", "The number of successors per state, b."),
  ("Optimal", "A search that always finds a cheapest solution.")],
 ["Define a problem by initial state, actions, transition model, goal test and path cost.", "BFS is complete and finds the fewest steps, but uses O(b^d) memory.",
  "Uniform-cost search expands the cheapest frontier node first.", "Depth-first uses little memory but may not find the best path.",
  "A* orders by f = g + h; optimal if h is admissible (and consistent for graph search).", "Heuristics come from relaxed problems."],
 [T("Imagine finding a route from one city to another. A state is a city, an action is a road, and a goal is reaching the destination. The set of all cities and roads forms a graph. Search explores this graph from the start, keeping a frontier of places it has seen but not yet explored."),
  T("Breadth-first search expands the oldest frontier node first, using a queue. It finds the path with the fewest steps. Its drawback is memory: the frontier can hold every node at the current depth, which grows like b to the power d."),
  T("Roads have different lengths. Uniform-cost search expands the node with the lowest cost so far, using a priority queue. It finds the cheapest path. Depth-first search uses a stack and little memory, but can wander down a long path and miss shorter ones."),
  T("Informed search adds knowledge. A heuristic h(n) estimates the remaining cost. For a map, the straight-line distance to the goal is a good one: no road is shorter than a straight line."),
  M(r"f(n) \;=\; g(n) + h(n)"),
  T("A star expands the node with the smallest f, where g is the cost so far and h the estimate of the cost to go. If h never overestimates, A star is optimal. If h is also consistent, meaning h(n) is at most the step cost plus h of the next node, it never needs to reopen a node."),
  T("Where do heuristics come from? Often from a relaxed version of the problem. In the sliding tile puzzle, pretend tiles can pass through each other; the number of moves needed is the sum of tile distances, the Manhattan distance, which is admissible.")],
 [("Which search finds the path with fewest steps?", ["Breadth-first", "Depth-first", "Greedy best-first", "Random"], 0, "It expands level by level."),
  ("What does an admissible heuristic do?", ["Never overestimates the true cost", "Always equals the true cost", "Overestimates slightly", "Ignores cost"], 0, "That keeps A* optimal."),
  ("What does A* sort the frontier by?", ["g(n) + h(n)", "h(n) only", "g(n) only", "Depth"], 0, "Cost so far plus estimate.")],
 [("Why is BFS memory hungry?", "It stores a whole level of nodes."), ("What is a relaxed problem?", "One with fewer restrictions."), ("What does uniform-cost optimise?", "Path cost."), ("What is the frontier?", "Generated but unexpanded nodes.")],
 [ORDER("A* loop", "Put the A* steps in order.", ["Put the start node on the frontier", "Remove the node with the lowest f", "If it is the goal, return the path", "Expand it and add its successors with new f values", "Repeat until the frontier is empty"]),
  PL("BFS steps", "Write bfs_steps(graph, start, goal): graph is a dict from node name to a list of neighbours. Return the fewest number of edges from start to goal, or -1 if unreachable.",
     "bfs_steps(graph, start, goal)", """
def bfs_steps(graph, start, goal):
    seen = {start: 0}
    queue = [start]
    i = 0
    while i < len(queue):
        n = queue[i]
        i += 1
        if n == goal:
            return seen[n]
        for m in graph[n]:
            if m not in seen:
                seen[m] = seen[n] + 1
                queue.append(m)
    return -1
""", [[{"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}, "a", "d"], [{"a": ["b"], "b": [], "c": []}, "a", "c"], [{"a": ["b", "c"], "b": ["c"], "c": ["a"]}, "a", "a"], [{"s": ["a", "b"], "a": ["g"], "b": ["c"], "c": ["g"], "g": []}, "s", "g"]], "Use a queue and a seen dict.", approx=None),
  PL("A* cost", "Write astar_cost(graph, h, start, goal): graph maps node to a dict of neighbour to edge cost; h maps node to the heuristic. Return the cheapest path cost from start to goal using A star, or -1 if unreachable.",
     "astar_cost(graph, h, start, goal)", """
def astar_cost(graph, h, start, goal):
    best = {start: 0}
    frontier = [(h[start], start)]
    while frontier:
        k = 0
        for i in range(len(frontier)):
            if frontier[i][0] < frontier[k][0]:
                k = i
        f, n = frontier.pop(k)
        if n == goal:
            return best[n]
        if f > best[n] + h[n]:
            continue
        for m in graph[n]:
            g = best[n] + graph[n][m]
            if m not in best or g < best[m]:
                best[m] = g
                frontier.append((g + h[m], m))
    return -1
""", [[{"s": {"a": 1, "b": 4}, "a": {"g": 5}, "b": {"g": 1}, "g": {}}, {"s": 4, "a": 4, "b": 1, "g": 0}, "s", "g"], [{"s": {"a": 1}, "a": {"g": 1}, "g": {}, "z": {}}, {"s": 2, "a": 1, "g": 0, "z": 0}, "s", "z"], [{"s": {"a": 2, "b": 1}, "a": {"g": 1}, "b": {"a": 1}, "g": {}}, {"s": 3, "a": 1, "b": 2, "g": 0}, "s", "g"]], "Always expand the lowest f.", approx=None)]))

A.append(CH(
 "Beyond classical search: local search and games",
 ("Local search and games", [
  "Hill climbing | moves to | Best neighbour", "Local maximum | traps | Hill climbing", "Simulated annealing | accepts | Some worse moves",
  "Minimax | assumes | A perfect opponent", "Alpha-beta | prunes | Irrelevant branches", "Evaluation function | scores | Cut-off positions", "Monte Carlo tree search | uses | Random playouts"]),
 ["Some problems have no meaningful path, only a good final state. Local search keeps a single state and improves it step by step. Hill climbing can get stuck on a local maximum; random restarts and simulated annealing help.",
  "In two-player games, minimax chooses the move that is best assuming the opponent also plays best. Alpha-beta pruning skips branches that cannot change the decision. Monte Carlo tree search, used in Go programs, chooses moves by many random playouts.",
  "The labs compute a minimax value and a hill climb."],
 [("Local search", "Search that keeps only the current state."), ("Hill climbing", "Repeatedly move to the best neighbour."), ("Simulated annealing", "Hill climbing that sometimes accepts worse moves, less often over time."),
  ("Minimax", "Best move assuming optimal play by both sides."), ("Alpha-beta pruning", "Skipping branches that cannot matter."), ("Evaluation function", "An estimate of a position's value.")],
 ["Local search uses little memory and suits optimisation.", "Hill climbing: local maxima, ridges and plateaus.", "Simulated annealing accepts a worse move with probability exp(delta/T).",
  "Minimax value: max at our turns, min at the opponent's.", "Alpha-beta can double the reachable depth with good move ordering.", "MCTS balances exploring and exploiting with random rollouts."],
 [T("Think of climbing a hill in fog: you can only see nearby ground. Hill climbing moves to the best neighbouring state and stops when none is better. It is fast, but can stop on a small hill that is not the highest one."),
  T("Two cures are popular. Random restarts run hill climbing many times from different starting points. Simulated annealing sometimes accepts a worse move, with a probability that shrinks as a temperature value falls. Early on it explores widely; later it settles."),
  T("Games add an opponent. Minimax searches the game tree. At our moves we take the maximum value, at the opponent's moves the minimum. The value of the root is what we get if both sides play perfectly."),
  T("Games are big, so we cut off the search at some depth and use an evaluation function to score the position. Alpha-beta pruning keeps a window of values already guaranteed to each side and stops exploring a branch once it cannot beat them. The result is the same as minimax but with far fewer nodes."),
  T("Monte Carlo tree search suits games like Go, where evaluation by hand is hard. It repeats four steps: select a promising node, expand it, play a random game to the end, and back up the result. Nodes that win more often get visited more."),
  T("Games with chance, such as backgammon, add chance nodes with expected values. Games with hidden information, such as poker, need reasoning about belief states.")],
 [("What does minimax assume?", ["The opponent plays optimally", "The opponent plays randomly", "There is no opponent", "The game is short"], 0, "Worst case for us."),
  ("What can trap hill climbing?", ["A local maximum", "A global maximum", "Too much memory", "A heuristic"], 0, "No neighbour is better."),
  ("What does alpha-beta change in the minimax result?", ["Nothing, it only prunes", "It makes it random", "It lowers the value", "It adds moves"], 0, "Same decision, fewer nodes.")],
 [("What does simulated annealing do?", "Sometimes accepts worse moves."), ("What is an evaluation function for?", "Score positions at the cut-off."), ("What does MCTS use?", "Random playouts."), ("Why random restarts?", "To escape local maxima.")],
 [MATCH("Methods", "Match each method with its idea.", [("Hill climbing", "Move to the best neighbour"), ("Simulated annealing", "Accept worse moves with falling probability"), ("Minimax", "Best move against a perfect opponent"), ("Alpha-beta", "Prune branches that cannot matter"), ("MCTS", "Random playouts")]),
  PL("Minimax value", "Write minimax(tree, maximizing): tree is either a number (a leaf) or a list of subtrees. Return the minimax value; maximizing is true when it is the maximiser's turn.",
     "minimax(tree, maximizing)", """
def minimax(tree, maximizing):
    if not isinstance(tree, list):
        return tree
    vals = [minimax(t, not maximizing) for t in tree]
    if maximizing:
        return max(vals)
    return min(vals)
""", [[3, True], [[3, 5], True], [[[3, 5], [2, 9]], True], [[[3, 12, 8], [2, 4, 6], [14, 5, 2]], True], [[[3, 12, 8], [2, 4, 6], [14, 5, 2]], False]], "Recurse; alternate max and min.", approx=None),
  PL("Hill climb", "Write hill_climb(values, start): values is a list of numbers; neighbours of index i are i-1 and i+1 (if they exist). Repeatedly move to the better neighbour if it is larger than the current value; return the index where you stop.",
     "hill_climb(values, start)", """
def hill_climb(values, start):
    i = start
    while True:
        best = i
        for j in (i - 1, i + 1):
            if 0 <= j < len(values) and values[j] > values[best]:
                best = j
        if best == i:
            return i
        i = best
""", [[[1, 3, 2, 5, 9, 4], 0], [[1, 3, 2, 5, 9, 4], 3], [[5], 0], [[1, 2, 3, 4], 0], [[4, 3, 2, 1], 3]], "Stop when no neighbour is higher.", approx=None)]))

A.append(CH(
 "Constraint satisfaction",
 ("CSP", [
  "CSP | has | Variables, domains, constraints", "Constraint graph | shows | Which variables interact", "Backtracking | assigns | One variable at a time",
  "Forward checking | prunes | Neighbour domains", "Arc consistency | removes | Unsupported values", "MRV | picks | Most constrained variable", "Min-conflicts | repairs | Complete assignments"]),
 ["A constraint satisfaction problem, or CSP, is defined by variables, the values each may take, and constraints on which combinations are allowed. Map colouring, scheduling and Sudoku are classic examples.",
  "Because constraints expose structure, a CSP solver can do much better than blind search. Backtracking assigns variables one at a time and undoes a choice when a constraint fails. Propagation, such as forward checking and arc consistency, removes impossible values early.",
  "The labs write a constraint check and a backtracking colour solver."],
 [("Variable", "A thing to assign a value to."), ("Domain", "The set of allowed values for a variable."), ("Constraint", "A restriction on combinations of values."),
  ("Arc consistency", "Every value has a supporting value in each neighbour."), ("MRV", "Choose the variable with the fewest remaining values."), ("Min-conflicts", "Local search that reassigns a conflicted variable.")],
 ["CSP = variables + domains + constraints.", "Backtracking is depth-first search over partial assignments.", "Forward checking removes values that a new assignment rules out.",
  "Arc consistency propagates constraints between variable pairs.", "Order heuristics: MRV, degree, least-constraining value.", "A tree-shaped constraint graph can be solved in linear time."],
 [T("Colouring a map so that neighbouring regions differ is a classic CSP. The variables are the regions, the domain of each is the set of colours, and the constraints say neighbours must differ. A solution is a complete assignment that breaks no constraint."),
  T("Plain search would try combinations without noticing that a bad choice early on dooms everything after it. Backtracking assigns one variable at a time and as soon as a constraint is violated it goes back and tries a different value."),
  T("Constraint propagation makes this far stronger. Forward checking, after each assignment, removes from the neighbours' domains any value that now conflicts. If a domain empties, we back up at once. Arc consistency goes further: a value is removed if some neighbour has no value compatible with it."),
  T("Heuristics for choosing matter a lot. Minimum remaining values picks the variable with the fewest legal values, so failures show up early. The degree heuristic breaks ties by choosing the variable involved in the most constraints. The least-constraining value rule tries the value that rules out the fewest options for neighbours."),
  T("For some problems local search works better. Min-conflicts starts from a full assignment, picks a conflicted variable and gives it the value that causes the fewest conflicts. It solves huge problems such as n-queens remarkably fast."),
  T("Structure helps. If the constraint graph is a tree, the problem can be solved in time linear in the number of variables. Otherwise we can cut the graph into a tree by assigning a few variables first.")],
 [("What does a CSP consist of?", ["Variables, domains and constraints", "States and actions only", "A heuristic", "Probabilities"], 0, "That is the definition."),
  ("What does MRV choose?", ["The variable with the fewest legal values", "The most constrained value", "A random variable", "The last variable"], 0, "Fail early."),
  ("When can a CSP be solved in linear time?", ["When the constraint graph is a tree", "When domains are large", "Never", "When it has one variable"], 0, "Tree structure.")],
 [("What does forward checking do?", "Prunes neighbour domains."), ("What is min-conflicts?", "Local search repair."), ("What is backtracking?", "DFS over partial assignments."), ("What is a constraint graph?", "Variables as nodes, constraints as edges.")],
 [FILL("Colouring", "In map colouring the {{variables}} are regions and the constraints say {{neighbours|neighbors|adjacent regions}} must differ."),
  PL("Consistent colouring", "Write is_valid(edges, colors): edges is a list of [a, b] pairs of region names; colors maps a region to a colour. Return true if no edge joins two regions with the same colour.",
     "is_valid(edges, colors)", """
def is_valid(edges, colors):
    for a, b in edges:
        if colors[a] == colors[b]:
            return False
    return True
""", [[[["a", "b"], ["b", "c"]], {"a": "r", "b": "g", "c": "r"}], [[["a", "b"], ["b", "c"]], {"a": "r", "b": "r", "c": "g"}], [[], {"a": "r"}], [[["a", "b"], ["b", "c"], ["a", "c"]], {"a": "r", "b": "g", "c": "b"}]], "Check every edge.", approx=None),
  PL("Backtracking colouring", "Write colour_map(regions, edges, colors): regions is a list of names, edges a list of [a, b], colors a list of colour names. Try colours in the given order, assign regions in the given order with backtracking, and return the first solution as a list of colours in region order, or an empty list if none exists.",
     "colour_map(regions, edges, colors)", """
def colour_map(regions, edges, colors):
    nb = {r: [] for r in regions}
    for a, b in edges:
        nb[a].append(b)
        nb[b].append(a)
    assign = {}
    def go(i):
        if i == len(regions):
            return True
        r = regions[i]
        for c in colors:
            ok = True
            for m in nb[r]:
                if assign.get(m) == c:
                    ok = False
            if ok:
                assign[r] = c
                if go(i + 1):
                    return True
                del assign[r]
        return False
    if go(0):
        return [assign[r] for r in regions]
    return []
""", [[["a", "b", "c"], [["a", "b"], ["b", "c"]], ["r", "g"]], [["a", "b", "c"], [["a", "b"], ["b", "c"], ["a", "c"]], ["r", "g"]], [["a", "b", "c"], [["a", "b"], ["b", "c"], ["a", "c"]], ["r", "g", "b"]], [["x"], [], ["r"]]], "Recurse over regions; undo on failure.", approx=None)]))

A.append(CH(
 "Logical agents: propositional logic",
 ("Logic", [
  "Knowledge base | holds | Sentences", "Entailment | means | True in all models", "Model checking | enumerates | Truth assignments",
  "Resolution | is | Sound and complete", "Horn clauses | allow | Linear inference", "SAT solver | decides | Satisfiability", "Wumpus world | illustrates | Logical agents"]),
 ["A knowledge-based agent keeps sentences in a knowledge base and uses inference to decide what to do. Propositional logic has symbols that are true or false, combined with not, and, or, implies and if and only if.",
  "A sentence is entailed by the knowledge base if it is true in every model where the knowledge base is true. Inference algorithms are sound if they derive only entailed sentences and complete if they derive all of them. Resolution is sound and complete for propositional logic.",
  "The labs evaluate sentences and test entailment by enumerating models."],
 [("Knowledge base", "A set of sentences held true."), ("Model", "An assignment of true or false to every symbol."), ("Entailment", "KB entails a when a holds in every model of KB."),
  ("Sound", "Derives only what is entailed."), ("Complete", "Can derive everything that is entailed."), ("Horn clause", "A clause with at most one positive literal.")],
 ["Syntax defines sentences; semantics defines their truth in a model.", "Entailment: KB entails a iff KB and not a is unsatisfiable.", "Model checking is exponential in the number of symbols.",
  "Resolution proves entailment by deriving the empty clause.", "Horn clauses admit forward and backward chaining in linear time.", "Modern SAT solvers handle millions of clauses (DPLL, clause learning)."],
 [T("A knowledge-based agent tells its knowledge base what it perceives and asks what to do. The strength of this design is that the knowledge is stated declaratively, and the same inference engine works on many problems."),
  T("In propositional logic a symbol such as Rain is either true or false. A model assigns a value to every symbol. We combine symbols with not, and, or, implies and if and only if. A sentence is true or false in each model by simple rules."),
  M(r"KB \models \alpha \quad\Longleftrightarrow\quad \text{every model of } KB \text{ is a model of } \alpha"),
  T("The simplest inference is model checking: enumerate all assignments and check that alpha is true wherever the knowledge base is true. It is sound and complete, but with n symbols there are 2 to the n models."),
  T("Resolution works on clauses, which are disjunctions of literals. From two clauses that contain a complementary pair, it derives a new clause without that pair. To prove alpha, add not alpha to the knowledge base and try to derive the empty clause, which signals a contradiction."),
  T("If the knowledge base consists of Horn clauses, inference is simpler. Forward chaining fires rules whose premises are known until the query appears. Backward chaining works from the goal. Both run in time linear in the size of the knowledge base."),
  T("The Wumpus world is a small cave game used to show these ideas. Pits cause breezes in adjacent squares; the Wumpus causes a stench. By combining percepts with rules, the agent can prove which squares are safe.")],
 [("What does KB entails a mean?", ["a is true in every model where KB is true", "a is in KB", "a is false", "KB is false"], 0, "That is entailment."),
  ("Which inference method is sound and complete for propositional logic?", ["Resolution", "Forward chaining on any KB", "Guessing", "Hill climbing"], 0, "Refutation by resolution."),
  ("Why are Horn clauses attractive?", ["Chaining is linear time", "They are shorter to write", "They are always false", "They need no symbols"], 0, "Efficient inference.")],
 [("What is a model?", "A truth assignment to all symbols."), ("What is resolution's goal?", "Derive the empty clause."), ("What does sound mean?", "Only entailed sentences are derived."), ("What does a SAT solver decide?", "Whether a formula can be true.")],
 [MATCH("Terms", "Match the term with its meaning.", [("Entailment", "True in all models of the KB"), ("Sound", "Derives only entailed sentences"), ("Complete", "Derives all entailed sentences"), ("Horn clause", "At most one positive literal")]),
  PL("Entails", "Write entails(kb, alpha, symbols): kb and alpha are lists of clauses (kb is a list of clauses that must all hold; alpha is a single clause). A clause is a list of strings, where a leading '-' means negation, and a clause is true if any literal is true. symbols lists all symbol names. Return true if every model satisfying all clauses of kb also satisfies alpha.",
     "entails(kb, alpha, symbols)", """
def entails(kb, alpha, symbols):
    n = len(symbols)
    for mask in range(2 ** n):
        m = {}
        for i in range(n):
            m[symbols[i]] = (mask >> i) & 1 == 1
        def val(lit):
            if lit[0] == '-':
                return not m[lit[1:]]
            return m[lit]
        def holds(cl):
            for lit in cl:
                if val(lit):
                    return True
            return False
        good = True
        for cl in kb:
            if not holds(cl):
                good = False
        if good and not holds(alpha):
            return False
    return True
""", [[[["-p", "q"], ["p"]], ["q"], ["p", "q"]], [[["-p", "q"]], ["q"], ["p", "q"]], [[["p", "q"]], ["p"], ["p", "q"]], [[["-a", "b"], ["-b", "c"], ["a"]], ["c"], ["a", "b", "c"]], [[], ["p", "-p"], ["p"]]], "Enumerate all 2^n models.", approx=None),
  PL("Forward chaining", "Write forward_chain(rules, facts, query): rules is a list of [premises, conclusion] with premises a list of symbols; facts a list of symbols. Return true if the query can be derived.",
     "forward_chain(rules, facts, query)", """
def forward_chain(rules, facts, query):
    known = set(facts)
    changed = True
    while changed:
        changed = False
        for prem, concl in rules:
            if concl not in known:
                ok = True
                for p in prem:
                    if p not in known:
                        ok = False
                if ok:
                    known.add(concl)
                    changed = True
    return query in known
""", [[[[["a", "b"], "c"], [["c"], "d"]], ["a", "b"], "d"], [[[["a", "b"], "c"]], ["a"], "c"], [[], ["x"], "x"], [[[["a"], "b"], [["b"], "c"]], ["a"], "c"]], "Keep firing rules until nothing new.", approx=None)]))
