# -*- coding: utf-8 -*-
"""GOFAI course, part 2: heuristics and games, rules and expert systems, planning, constraints, limits."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Heuristic search and A*",
 ("Heuristic search", [
  "Heuristic | estimates | Cost to goal",
  "Greedy search | follows | The heuristic",
  "A star | adds | Cost so far",
  "Admissible | never | Overestimates",
  "Priority queue | orders | The frontier",
  "Manhattan distance | is | A grid heuristic",
  "Optimal | means | Cheapest path"]),
 ["A heuristic is a rule of thumb that estimates how far a state is from the goal. Using it to choose which state to expand next makes search much faster than blind search.",
  "A* orders states by f = g + h, where g is the cost so far and h is the heuristic estimate to go. If h never overestimates the true cost (it is admissible), A* finds a cheapest path.",
  "On a grid the Manhattan distance, the sum of horizontal and vertical steps, is a common admissible heuristic."],
 [("Heuristic", "An estimate of the remaining cost from a state to the goal."),
  ("Admissible heuristic", "A heuristic that never overestimates the true remaining cost."),
  ("A* search", "Best-first search that expands the state with the lowest g plus h."),
  ("Priority queue", "A queue that always returns the item with the lowest key."),
  ("Manhattan distance", "The sum of the absolute differences in x and y.")],
 ["f(n) = g(n) + h(n).",
  "Admissible: h(n) never exceeds the true cost.",
  "Admissible h gives optimal A*.",
  "Greedy search uses only h and is not optimal.",
  "Manhattan distance for 4-way grids."],
 [T("Blind search treats every direction the same. But you often have a hunch. If you want to go north-east, a path going south-west is probably wasted. A heuristic turns the hunch into a number: an estimate of how far each state is from the goal."),
  T("Greedy best-first search always expands the state that looks closest to the goal. It can be quick, but it can also be fooled. A route that heads straight at the goal may run into a wall and end up far longer than a detour. It does not weigh the cost already paid."),
  T("A* fixes this by adding the two. For each state, g is the cost from the start so far and h is the estimated cost to the goal. A* always expands the state with the smallest f, the sum. If h never overestimates, A* is both complete and optimal."),
  T("On a grid where you move up, down, left or right, the Manhattan distance, the sum of the x and y differences, never overestimates, because you must make at least that many steps. If diagonal moves are allowed, the straight-line distance or the larger of the two differences is safer."),
  T("Designing heuristics is a classic GOFAI skill. For the sliding-tile puzzle, the number of misplaced tiles and the sum of Manhattan distances of tiles are both admissible, and the second is stronger. A stronger admissible heuristic means fewer states to search.")],
 [("What does A* minimise when choosing the next state?", ["g + h", "g only", "h only", "depth only"], 0, "Cost so far plus estimate."),
  ("What does admissible mean?", ["Never overestimates", "Always exact", "Always zero", "Always large"], 0, "Keeps A* optimal."),
  ("Which heuristic suits a 4-way grid?", ["Manhattan distance", "Number of cells", "Random", "Zero only"], 0, "Sum of dx and dy."),
  ("What data structure holds A*'s frontier?", ["A priority queue", "A stack", "A plain queue", "A set only"], 0, "Lowest f first."),
  ("Is greedy best-first search optimal?", ["No", "Yes", "Only on grids", "Only with h = 0"], 0, "It ignores g."),
  ("What happens with h = 0 in A*?", ["It behaves like uniform-cost search", "It fails", "It becomes DFS", "It becomes greedy"], 0, "Only g counts.")],
 [("f = g + h", "A* priority"), ("Admissible", "h never overestimates"), ("Manhattan", "|dx| + |dy|"), ("Greedy", "uses only h")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("g", "cost so far"), ("h", "estimated cost to go"), ("f", "g plus h"), ("Admissible", "never overestimates")]),
  PL("Manhattan distance", "Write manhattan(a, b): a and b are [x, y] pairs. Return the sum of the absolute differences.", "manhattan(a, b)", '''
def manhattan(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    if dx < 0:
        dx = 0 - dx
    if dy < 0:
        dy = 0 - dy
    return dx + dy
''', [[[0, 0], [3, 4]], [[2, 5], [2, 5]], [[-1, 2], [3, -2]], [[7, 1], [4, 1]]], "Add the two absolute differences."),
  PL("A* on a grid", "Write astar(grid, start, goal): grid is a list of strings where '#' is a wall and '.' is open; start and goal are [row, col]. Moves are up, down, left, right with cost 1. Use the Manhattan distance as h. Return the length of a cheapest path (number of steps), or -1 if the goal is unreachable.", "astar(grid, start, goal)", '''
def astar(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    def h(p):
        return abs(p[0] - goal[0]) + abs(p[1] - goal[1])
    best = {}
    best[(start[0], start[1])] = 0
    open_list = [[h(start), 0, start[0], start[1]]]
    while open_list:
        bi = 0
        for i in range(1, len(open_list)):
            if open_list[i] < open_list[bi]:
                bi = i
        f, g, r, c = open_list.pop(bi)
        if r == goal[0] and c == goal[1]:
            return g
        if g > best.get((r, c), 10 ** 9):
            continue
        for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                ng = g + 1
                if ng < best.get((nr, nc), 10 ** 9):
                    best[(nr, nc)] = ng
                    open_list.append([ng + h([nr, nc]), ng, nr, nc])
    return -1
''', [[["....", "....", "...."], [0, 0], [2, 3]], [["..#.", "..#.", "...."], [0, 0], [0, 3]], [["..#.", "###.", "...."], [0, 0], [2, 0]], [["."], [0, 0], [0, 0]]], "Pick the open entry with the lowest f each time."),
  PL("Sliding puzzle heuristic", "Write misplaced(board, goal): both are flat lists of tile numbers with 0 for the blank. Return the number of tiles (not counting the blank) that are not in their goal position.", "misplaced(board, goal)", '''
def misplaced(board, goal):
    n = 0
    for i in range(len(board)):
        if board[i] != 0 and board[i] != goal[i]:
            n = n + 1
    return n
''', [[[1, 2, 3, 4, 5, 6, 7, 8, 0], [1, 2, 3, 4, 5, 6, 7, 8, 0]], [[1, 2, 3, 4, 5, 6, 7, 0, 8], [1, 2, 3, 4, 5, 6, 7, 8, 0]], [[2, 1, 3, 4, 5, 6, 7, 8, 0], [1, 2, 3, 4, 5, 6, 7, 8, 0]]], "Compare each position, skipping the blank.")]
))

CHS.append(CH(
 "Game playing: minimax and alpha-beta",
 ("Games", [
  "Game tree | lists | Moves",
  "Minimax | assumes | Best play",
  "MAX | maximises | Score",
  "MIN | minimises | Score",
  "Evaluation | scores | Positions",
  "Alpha-beta | prunes | Branches",
  "Depth limit | bounds | Search"]),
 ["For two-player games with perfect information, GOFAI builds a game tree of moves and counter-moves. Minimax assumes both sides play the best they can: MAX picks the move with the highest value and MIN picks the lowest.",
  "Real games are too big to search completely, so programs search to a depth limit and score positions with an evaluation function that counts material, mobility and similar features.",
  "Alpha-beta pruning gives the same result as minimax while skipping branches that cannot affect the answer, which roughly doubles the reachable depth."],
 [("Minimax", "A rule that chooses the move maximising the worst-case outcome against a best-playing opponent."),
  ("Evaluation function", "A function that scores a non-final position for one side."),
  ("Alpha-beta pruning", "Minimax with cut-offs for branches that cannot change the result."),
  ("Horizon effect", "Misjudging a position because a threat lies just past the search depth."),
  ("Zero-sum game", "A game in which one player's gain equals the other's loss.")],
 ["MAX picks the largest child value; MIN the smallest.",
  "Leaves hold scores; internal nodes get backed-up values.",
  "Alpha-beta never changes the minimax value.",
  "Good move ordering prunes more.",
  "Deep Blue beat Kasparov in 1997 using search."],
 [T("Draw the possible moves as a tree. At the root it is your turn, and each branch is a move. At each child it is the opponent's turn with their own branches, and so on down to the end of the game or a chosen depth. This is the game tree."),
  T("Give each end position a score from your point of view: plus one for a win, zero for a draw, minus one for a loss. Now work upward. At a node where you move, take the highest child value. Where the opponent moves, assume they take the lowest. The value at the root is what you can guarantee against best play. That is minimax."),
  T("Chess has too many positions to search to the end, so programs stop at a depth limit and use an evaluation function. A simple one counts the value of pieces: pawns one, knights and bishops three, rooks five, queen nine. Better ones add king safety, pawn structure and mobility."),
  T("Alpha-beta pruning tracks the best value MAX can already get (alpha) and the best MIN can already hold (beta). If a branch can no longer improve on those bounds, the rest of it is skipped. The final answer is unchanged, but with good move ordering the program searches about twice as deep in the same time."),
  T("This approach reached its peak with IBM's Deep Blue, which beat world champion Garry Kasparov in 1997 with special chips searching hundreds of millions of positions per second. It was brute force guided by hand-built evaluation, a showpiece for GOFAI. Later programs used learning instead.")],
 [("What does MAX do at its node?", ["Takes the highest child value", "Takes the lowest", "Takes the average", "Takes a random child"], 0, "Maximises."),
  ("What does MIN assume?", ["The opponent picks the lowest value for MAX", "The opponent plays randomly", "The opponent passes", "The opponent copies MAX"], 0, "Worst case for MAX."),
  ("What does alpha-beta change?", ["Speed, not the result", "The minimax value", "The rules", "The evaluation"], 0, "Same answer, less work."),
  ("Why use an evaluation function?", ["To score non-final positions at the depth limit", "To print the board", "To store moves", "To train a network"], 0, "Cannot search to the end."),
  ("Who beat Kasparov in 1997?", ["Deep Blue", "AlphaGo", "ELIZA", "MYCIN"], 0, "IBM."),
  ("What is a zero-sum game?", ["One player's gain is the other's loss", "A game with no winner", "A game with zero moves", "A game of chance"], 0, "Total is constant.")],
 [("Minimax", "best play against best play"), ("Alpha-beta", "pruned minimax"), ("Evaluation", "score at the depth limit"), ("Deep Blue", "beat Kasparov, 1997")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("MAX", "chooses the highest value"), ("MIN", "chooses the lowest value"), ("Alpha-beta", "prunes without changing the result"), ("Horizon effect", "threat just past the depth limit")]),
  PL("Minimax", "Write minimax(tree, maximizing). A tree is either a number (a leaf score) or a list of subtrees. maximizing is True when MAX moves at this node. Return the minimax value.", "minimax(tree, maximizing)", '''
def minimax(tree, maximizing):
    if not isinstance(tree, list):
        return tree
    vals = [minimax(t, not maximizing) for t in tree]
    if maximizing:
        return max(vals)
    return min(vals)
''', [[3, True], [[3, 5], True], [[[3, 5], [2, 9]], True], [[[3, 5], [2, 9]], False], [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], True]], "Alternate maximizing at each level."),
  PL("Alpha-beta leaves", "Write ab_count(tree, maximizing): run minimax with alpha-beta pruning and return a list [value, leaves_visited] where leaves_visited counts the leaf scores actually looked at. Use alpha = negative infinity (-1000) and beta = infinity (1000) at the start. Visit children left to right and stop when beta is at most alpha.", "ab_count(tree, maximizing)", '''
def ab_count(tree, maximizing):
    count = [0]
    def go(t, mx, alpha, beta):
        if not isinstance(t, list):
            count[0] = count[0] + 1
            return t
        if mx:
            v = -1000
            for c in t:
                v = max(v, go(c, False, alpha, beta))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v
        v = 1000
        for c in t:
            v = min(v, go(c, True, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
    value = go(tree, maximizing, -1000, 1000)
    return [value, count[0]]
''', [[[[3, 5], [2, 9]], True], [[[[3, 5], [6, 9]], [[1, 2], [0, -1]]], True], [4, True], [[[1, 2], [3, 4], [5, 6]], False]], "Carry alpha and beta down, and break when they cross."),
  PL("Material evaluation", "Write material(pieces): pieces is a string of piece letters; uppercase belongs to MAX and lowercase to MIN. Values are p/P 1, n/N 3, b/B 3, r/R 5, q/Q 9. Return MAX's total minus MIN's total.", "material(pieces)", '''
def material(pieces):
    vals = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9}
    total = 0
    for ch in pieces:
        v = vals.get(ch.lower(), 0)
        if ch.isupper():
            total = total + v
        else:
            total = total - v
    return total
''', [["PPNQ"], ["Qq"], ["RRrbn"], [""], ["PPPPpp"]], "Add for capitals and subtract for lowercase.")]
))

CHS.append(CH(
 "Rule-based systems and expert systems",
 ("Expert systems", [
  "Rule | has | If and then",
  "Working memory | holds | Facts",
  "Inference engine | applies | Rules",
  "Forward chaining | starts | From facts",
  "Backward chaining | starts | From goals",
  "Expert system | encodes | Expertise",
  "Knowledge engineer | builds | Rules"]),
 ["A production system has a set of if-then rules, a working memory of facts, and an inference engine that matches rules against facts and fires them. Expert systems apply this to specialised fields such as medicine and chemistry.",
  "Forward chaining starts with known facts and fires rules to derive new ones until nothing changes. Backward chaining starts with a goal and works back to see which facts would prove it.",
  "Expert systems like MYCIN also attach certainty factors and can explain their reasoning by showing the rules used."],
 [("Production rule", "A statement of the form IF conditions THEN conclusions."),
  ("Working memory", "The set of facts currently believed true."),
  ("Forward chaining", "Reasoning from facts to conclusions by firing rules."),
  ("Backward chaining", "Reasoning from a goal to the facts needed to support it."),
  ("Knowledge engineer", "A person who turns an expert's knowledge into rules.")],
 ["IF conditions THEN conclusion.",
  "Forward chaining is data-driven.",
  "Backward chaining is goal-driven.",
  "Explanation: show the rules that fired.",
  "The knowledge acquisition bottleneck: rules are hard to collect."],
 [T("Ask a doctor how they diagnose and you may hear rules. If the patient has a fever and a stiff neck, then suspect meningitis. An expert system writes such rules as data and lets a general engine run them. The engine does not know medicine. All the knowledge is in the rules."),
  T("In forward chaining, the engine keeps a pool of facts. It looks for rules whose conditions are all in the pool, fires one and adds its conclusion to the pool. It repeats until no new facts appear. This suits situations where data arrives and you want to see what follows."),
  T("In backward chaining the engine begins with a question. Is this bacterial infection caused by this organism? It looks for rules that conclude this, then makes their conditions into new questions. It asks the user for facts it cannot derive. Prolog works this way, and it asks only what it needs."),
  T("MYCIN, built at Stanford in the 1970s, had about six hundred rules and gave certainty factors between minus one and one. It matched the advice of specialists in tests, and could explain by listing the rules it used. It was never used in practice, partly for legal and ethical reasons."),
  T("Expert systems met limits. Collecting rules from experts was slow, called the knowledge acquisition bottleneck. Large rule sets became hard to maintain and interact in unexpected ways. The systems failed ungracefully outside their narrow domain. Even so, the rule-based approach lives on in business rules and decision engines.")],
 [("What is working memory?", ["The set of current facts", "The program's RAM", "The rule list", "The user interface"], 0, "Facts believed true."),
  ("Which chaining starts from known facts?", ["Forward", "Backward", "Sideways", "Random"], 0, "Data-driven."),
  ("Which chaining starts from a goal?", ["Backward", "Forward", "Neither", "Both"], 0, "Goal-driven."),
  ("What did MYCIN diagnose?", ["Bacterial infections", "Car faults", "Chess positions", "Weather"], 0, "Stanford, 1970s."),
  ("What is the knowledge acquisition bottleneck?", ["Getting expert knowledge into rules is slow", "Computers are slow", "Rules run out", "Memory is full"], 0, "Human effort."),
  ("What can an expert system do that a neural net often cannot?", ["Explain by showing rules", "Learn from pixels", "Recognise faces", "Predict stock prices"], 0, "Traceable reasoning.")],
 [("Forward chaining", "facts to conclusions"), ("Backward chaining", "goal to facts"), ("MYCIN", "blood infection advice"), ("Certainty factor", "number for belief")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Production rule", "IF conditions THEN conclusion"), ("Working memory", "facts so far"), ("Forward chaining", "data-driven"), ("Backward chaining", "goal-driven"), ("Inference engine", "matches and fires rules")]),
  PL("Forward chaining", "Write forward(rules, facts). rules is a list of [conditions, conclusion] where conditions is a list of fact names. facts is a list of fact names known to be true. Fire rules repeatedly until nothing new is added, and return the sorted list of all facts.", "forward(rules, facts)", '''
def forward(rules, facts):
    known = {}
    for f in facts:
        known[f] = 1
    changed = True
    while changed:
        changed = False
        for r in rules:
            ok = True
            for c in r[0]:
                if c not in known:
                    ok = False
            if ok and r[1] not in known:
                known[r[1]] = 1
                changed = True
    return sorted(known.keys())
''', [[[[["fever", "stiff_neck"], "meningitis_suspected"], [["meningitis_suspected"], "needs_test"]], ["fever", "stiff_neck"]], [[[["a"], "b"], [["b"], "c"]], ["a"]], [[[["a", "z"], "b"]], ["a"]], [[], ["x"]]], "Loop until a full pass adds nothing."),
  PL("Backward chaining", "Write backward(rules, facts, goal): return True if goal is a known fact or there is a rule concluding goal all of whose conditions can be proved the same way. Rules are [conditions, conclusion]. Assume the rules contain no cycles.", "backward(rules, facts, goal)", '''
def backward(rules, facts, goal):
    if goal in facts:
        return True
    for r in rules:
        if r[1] == goal:
            ok = True
            for c in r[0]:
                if not backward(rules, facts, c):
                    ok = False
                    break
            if ok:
                return True
    return False
''', [[[[["a"], "b"], [["b"], "c"]], ["a"], "c"], [[[["a"], "b"]], [], "b"], [[[["a", "z"], "b"]], ["a"], "b"], [[], ["g"], "g"]], "Prove each condition recursively."),
  PL("Explain a conclusion", "Write explain(rules, facts, goal): return the list of rule indices (positions in rules, starting at 0) that fired, in order, in forward chaining from facts until goal is derived. Fire the first applicable rule in list order each time it adds a new fact. If goal is already in facts return []. If it cannot be derived return None.", "explain(rules, facts, goal)", '''
def explain(rules, facts, goal):
    known = {}
    for f in facts:
        known[f] = 1
    used = []
    while goal not in known:
        fired = False
        for i in range(len(rules)):
            r = rules[i]
            ok = True
            for c in r[0]:
                if c not in known:
                    ok = False
            if ok and r[1] not in known:
                known[r[1]] = 1
                used.append(i)
                fired = True
                break
        if not fired:
            return None
    return used
''', [[[[["a"], "b"], [["b"], "c"], [["x"], "y"]], ["a"], "c"], [[[["a"], "b"]], ["a", "b"], "b"], [[[["a"], "b"]], [], "b"]], "Record the index each time a rule adds a fact.")]
))

CHS.append(CH(
 "Planning: STRIPS and the frame problem",
 ("Planning", [
  "State | is | A set of facts",
  "Action | has | Preconditions",
  "Action | has | Add and delete lists",
  "Plan | is | A sequence of actions",
  "STRIPS | represents | Actions",
  "Frame problem | asks | What stays the same",
  "Means-ends analysis | reduces | Differences"]),
 ["Planning finds a sequence of actions that turns an initial state into a goal state. In STRIPS, a state is a set of facts, and each action has preconditions that must hold, an add list of facts it makes true, and a delete list of facts it makes false.",
  "Applying an action to a state removes the delete list and adds the add list, leaving everything else unchanged. Planning is then a search over states, where good heuristics and clever representations matter.",
  "The frame problem is the difficulty of stating, in a general logic, everything that an action does not change."],
 [("STRIPS", "The Stanford Research Institute Problem Solver, and the action format it introduced."),
  ("Precondition", "A fact that must hold before an action can be applied."),
  ("Add and delete lists", "The facts an action makes true and the facts it makes false."),
  ("Frame problem", "The problem of representing what does not change when an action occurs."),
  ("Means-ends analysis", "Reducing the difference between current state and goal, as in GPS.")],
 ["State = set of facts.",
  "Apply: new = (state minus delete) plus add.",
  "Applicable if preconditions are a subset of state.",
  "Plan = sequence of applicable actions reaching the goal.",
  "STRIPS assumption solves the frame problem for simple domains."],
 [T("Imagine a robot in a world of blocks. A state is a set of facts such as OnTable(A), On(B, A), Clear(B), HandEmpty. The goal might be On(A, B). An action such as Unstack(B, A) needs Clear(B), On(B, A) and HandEmpty, and changes the state."),
  T("A STRIPS action lists preconditions, an add list and a delete list. Unstack(B, A) adds Holding(B) and Clear(A), and deletes On(B, A), Clear(B) and HandEmpty. To apply it, check the preconditions are in the state, remove the deleted facts and insert the added facts. All other facts stay as they were."),
  T("A plan is a sequence of actions such that each one is applicable when its turn comes, and the final state contains the goal. A planner searches for such a sequence. Forward search starts from the initial state, and backward search starts from the goal and works out what must hold before."),
  T("That last sentence in the STRIPS definition, all other facts stay as they were, hides a deep problem. In general logic, you have to say explicitly that moving a block does not change the colour of the table, the position of the other blocks, or the weather. Writing all those frame axioms is impractical. McCarthy and Hayes named this the frame problem in 1969."),
  T("STRIPS sidesteps it by assuming that anything not in the add or delete lists stays unchanged. That works in tidy worlds, but fails when actions have indirect effects or when the world changes by itself. Modern planners such as those using PDDL, a descendant of STRIPS, power logistics, scheduling and robotics, with heuristics that make them fast.")],
 [("What is a state in STRIPS?", ["A set of facts", "A number", "A sequence of actions", "A graph colour"], 0, "What is true now."),
  ("What does an action's delete list do?", ["Removes facts from the state", "Adds facts", "Lists preconditions", "Counts steps"], 0, "Makes them false."),
  ("When is an action applicable?", ["When its preconditions are in the state", "Always", "When the goal holds", "When the add list is empty"], 0, "Preconditions subset of state."),
  ("What is the frame problem?", ["Stating what does not change", "A graphics bug", "A search failure", "A proof of resolution"], 0, "McCarthy and Hayes, 1969."),
  ("What does a plan consist of?", ["A sequence of actions", "A single fact", "A rule set", "A score"], 0, "Reaches the goal."),
  ("What descended from STRIPS?", ["PDDL", "HTML", "SQL", "CSS"], 0, "Planning language.")],
 [("STRIPS", "preconditions, add list, delete list"), ("PDDL", "modern planning language"), ("Plan", "sequence of actions"), ("Frame problem", "what stays the same?")],
 [MATCH("Match the part of an action", "Pair each part with its role.", [("Preconditions", "must hold before"), ("Add list", "facts made true"), ("Delete list", "facts made false"), ("Plan", "sequence of actions")]),
  PL("Apply an action", "Write apply_action(state, action). state is a list of facts (strings). action is a dict with keys 'pre', 'add', 'del', each a list of facts. If every fact in 'pre' is in the state return the new state as a sorted list: (state minus 'del') plus 'add', without duplicates. Otherwise return None.", "apply_action(state, action)", '''
def apply_action(state, action):
    for p in action["pre"]:
        if p not in state:
            return None
    new = {}
    for f in state:
        if f not in action["del"]:
            new[f] = 1
    for f in action["add"]:
        new[f] = 1
    return sorted(new.keys())
''', [[["HandEmpty", "Clear(B)", "On(B,A)"], {"pre": ["HandEmpty", "Clear(B)", "On(B,A)"], "add": ["Holding(B)", "Clear(A)"], "del": ["HandEmpty", "Clear(B)", "On(B,A)"]}], [["HandEmpty"], {"pre": ["Holding(B)"], "add": ["x"], "del": []}], [["a"], {"pre": [], "add": ["b"], "del": ["a"]}]], "Check preconditions, then remove and add."),
  PL("Plan by breadth-first search", "Write plan(init, goal, actions). init and goal are lists of facts, actions is a list of dicts with keys 'name', 'pre', 'add', 'del'. Return the shortest list of action names that reaches a state containing all goal facts, trying actions in list order, or None if no plan exists. If the goal already holds return []. Use breadth-first search over states.", "plan(init, goal, actions)", '''
def plan(init, goal, actions):
    start = sorted(init)
    queue = [[start, []]]
    seen = {tuple(start): 1}
    head = 0
    while head < len(queue):
        state, steps = queue[head]
        head = head + 1
        ok = True
        for g in goal:
            if g not in state:
                ok = False
        if ok:
            return steps
        for a in actions:
            good = True
            for p in a["pre"]:
                if p not in state:
                    good = False
            if not good:
                continue
            new = {}
            for f in state:
                if f not in a["del"]:
                    new[f] = 1
            for f in a["add"]:
                new[f] = 1
            ns = sorted(new.keys())
            key = tuple(ns)
            if key not in seen:
                seen[key] = 1
                queue.append([ns, steps + [a["name"]]])
    return None
''', [[["at_home"], ["at_work"], [{"name": "walk", "pre": ["at_home"], "add": ["at_work"], "del": ["at_home"]}]], [["a"], ["a"], []], [["a"], ["c"], [{"name": "ab", "pre": ["a"], "add": ["b"], "del": ["a"]}, {"name": "bc", "pre": ["b"], "add": ["c"], "del": ["b"]}]], [["a"], ["z"], [{"name": "ab", "pre": ["a"], "add": ["b"], "del": []}]]], "Treat each state as a node and each action as an edge."),
  PL("Goal reached?", "Write satisfied(state, goal): True if every fact in goal is in state.", "satisfied(state, goal)", '''
def satisfied(state, goal):
    for g in goal:
        if g not in state:
            return False
    return True
''', [[["a", "b", "c"], ["a", "c"]], [["a"], ["a", "b"]], [[], []]], "Check every goal fact.")]
))

CHS.append(CH(
 "Constraints and logic programming",
 ("Constraints", [
  "Variable | takes | A value",
  "Domain | lists | Allowed values",
  "Constraint | restricts | Combinations",
  "Backtracking | tries | And undoes",
  "Propagation | prunes | Domains",
  "Prolog | runs | Logic",
  "Horn clause | has | One positive literal"]),
 ["A constraint satisfaction problem (CSP) has variables, each with a domain of possible values, and constraints on combinations of values. Map colouring, scheduling and Sudoku are classic examples.",
  "Backtracking search assigns variables one at a time and undoes a choice when a constraint is violated. Constraint propagation prunes domains early, such as removing values that conflict with a neighbour's only remaining value.",
  "Logic programming, as in Prolog, states facts and rules as Horn clauses and answers queries by backward chaining with unification and backtracking."],
 [("CSP", "A problem defined by variables, domains and constraints."),
  ("Backtracking", "A depth-first search that undoes assignments that lead to a violation."),
  ("Constraint propagation", "Using constraints to remove impossible values from domains."),
  ("Horn clause", "A clause with at most one positive literal, the form used by Prolog."),
  ("Prolog", "A logic programming language based on Horn clauses and backward chaining.")],
 ["CSP = variables + domains + constraints.",
  "Backtracking: assign, check, undo.",
  "Choose the most constrained variable first.",
  "Prolog: facts, rules and queries.",
  "Prolog searches depth-first with backtracking."],
 [T("A map-colouring puzzle asks for a colour for each region so that no two neighbouring regions share a colour. Regions are the variables, the colours are the domain, and the constraint is that neighbours differ. The same pattern fits timetabling, where classes are variables, time slots are the domain and clashes are forbidden."),
  T("The basic method is backtracking. Pick a variable, try a value, and check the constraints. If it is fine, move on to the next variable. If no value works, go back and change an earlier choice. This is depth-first search with early failure, and it avoids exploring any branch that has already broken a constraint."),
  T("Heuristics speed it up a great deal. Choosing the variable with the fewest remaining values, the most constrained one, finds dead ends sooner. Constraint propagation, such as arc consistency, removes values that cannot be part of any solution before search even starts. Sudoku solvers work this way."),
  T("Prolog turns logic into a programming language. A program is a set of facts and rules, such as parent(tom, bob) and grandparent(X, Z) :- parent(X, Y), parent(Y, Z). A query such as grandparent(tom, Who) is answered by backward chaining, unifying each goal with facts and rule heads, and backtracking when a choice fails."),
  T("Prolog, created by Colmerauer and Kowalski in the early 1970s, was chosen for Japan's Fifth Generation Computer project in the 1980s. That project did not deliver the expected breakthroughs, but Prolog and constraint solvers are still used in scheduling, configuration and language processing, and its ideas live on in modern solvers.")],
 [("What is a CSP?", ["Variables, domains and constraints", "A sorting algorithm", "A neural net", "A database"], 0, "A structured puzzle."),
  ("What does backtracking do on failure?", ["Undoes an earlier choice", "Stops the program", "Restarts from scratch", "Ignores the constraint"], 0, "Goes back."),
  ("Which variable should be chosen first?", ["The most constrained one", "The least constrained", "A random one", "The last one"], 0, "Fail early."),
  ("What is a Horn clause?", ["At most one positive literal", "Two negations", "A loop", "A fact with no head"], 0, "Prolog's form."),
  ("How does Prolog answer a query?", ["Backward chaining with unification", "Forward chaining only", "Random guesses", "Sorting"], 0, "Depth-first."),
  ("Which project used Prolog in the 1980s?", ["Japan's Fifth Generation", "Apollo", "Deep Blue", "Human Genome"], 0, "A national AI programme.")],
 [("CSP", "variables, domains, constraints"), ("Backtracking", "assign, check, undo"), ("Prolog", "logic programming"), ("Arc consistency", "prune domains by pairs")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Variable", "a thing to assign"), ("Domain", "the allowed values"), ("Constraint", "a restriction on combinations"), ("Backtracking", "undo and retry"), ("Prolog", "facts, rules and queries")]),
  PL("Map colouring", "Write colour_map(graph, colours): graph is a dict from region to a list of neighbouring regions (symmetric). colours is a list of colour names. Colour the regions in sorted name order using backtracking, trying colours in list order. Return the list of colours in sorted region order, or None if impossible.", "colour_map(graph, colours)", '''
def colour_map(graph, colours):
    regions = sorted(graph.keys())
    assign = {}
    def ok(r, c):
        for nb in graph[r]:
            if assign.get(nb) == c:
                return False
        return True
    def go(i):
        if i == len(regions):
            return True
        r = regions[i]
        for c in colours:
            if ok(r, c):
                assign[r] = c
                if go(i + 1):
                    return True
                del assign[r]
        return False
    if go(0):
        return [assign[r] for r in regions]
    return None
''', [[{"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}, ["red", "green", "blue"]], [{"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}, ["red", "green"]], [{"A": ["B"], "B": ["A"]}, ["x", "y"]], [{"W": ["X"], "X": ["W", "Y"], "Y": ["X"]}, ["r", "g"]]], "Try each colour, recurse, and undo if the rest fails."),
  PL("N queens count", "Write queens(n): the number of ways to place n queens on an n by n board so that no two attack each other (same row, column or diagonal). Use backtracking row by row.", "queens(n)", '''
def queens(n):
    cols = []
    def ok(c):
        r = len(cols)
        for i in range(r):
            if cols[i] == c or abs(cols[i] - c) == r - i:
                return False
        return True
    def go():
        if len(cols) == n:
            return 1
        total = 0
        for c in range(n):
            if ok(c):
                cols.append(c)
                total = total + go()
                cols.pop()
        return total
    return go()
''', [[1], [2], [4], [5], [6]], "Place one queen per row and check columns and diagonals."),
  PL("Grandparent query", "Write grandparents(parents, person): parents is a list of [parent, child] facts. Return the sorted list of grandparents of person, the parents of the parents. This is the Prolog rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).", "grandparents(parents, person)", '''
def grandparents(parents, person):
    out = {}
    for p in parents:
        if p[1] == person:
            for q in parents:
                if q[1] == p[0]:
                    out[q[0]] = 1
    return sorted(out.keys())
''', [[[["tom", "bob"], ["bob", "ann"], ["liz", "bob"]], "ann"], [[["tom", "bob"]], "bob"], [[["a", "b"], ["b", "c"], ["c", "d"]], "d"]], "Join the parent facts on the middle person.")]
))

CHS.append(CH(
 "Limits, legacy and the road to neuro-symbolic AI",
 ("Legacy", [
  "Common sense | resisted | Rules",
  "Cyc | encoded | Common sense",
  "Brittleness | limits | Rule systems",
  "Symbol grounding | asks | Where meaning comes from",
  "Learning | rose | After 2010",
  "Knowledge graphs | survive | In search",
  "Neuro-symbolic | combines | Both"]),
 ["GOFAI ran into walls. Everyday common sense turned out to need millions of facts and exceptions. Rule systems were brittle at the edges of their knowledge, and the frame, qualification and ramification problems made precise logical descriptions of the world endless.",
  "Projects like Cyc, started by Douglas Lenat in 1984, tried to write down common sense by hand, and are still running. Meanwhile, learning from data overtook hand-written rules in vision, speech and language.",
  "The symbolic legacy remains in search, planning, verification, databases and knowledge graphs. Neuro-symbolic AI tries to give learned systems the ability to reason, and symbolic systems the ability to learn."],
 [("Common-sense knowledge", "Everyday facts and expectations that people share, such as water making things wet."),
  ("Cyc", "A long-running project to encode common-sense knowledge in formal logic."),
  ("Symbol grounding problem", "The question of how symbols get meaning beyond other symbols."),
  ("Brittleness", "The tendency of rule systems to fail sharply outside their narrow domain."),
  ("Neuro-symbolic AI", "Approaches that combine neural networks with symbolic reasoning.")],
 ["Common sense needs huge amounts of knowledge.",
  "Rule systems are brittle at their edges.",
  "Searle's Chinese Room argued against pure symbol manipulation.",
  "Symbolic ideas survive in search, planning and verification.",
  "Neuro-symbolic AI mixes learning and reasoning."],
 [T("People know without thinking that a glass dropped on a hard floor will break, that you cannot pour a liquid into a closed bottle, and that an elephant does not fit in a car. Nobody listed these facts for us. Writing them all down turned out to be vast, because each fact has exceptions, and each exception has exceptions."),
  T("Cyc is the boldest attempt. Beginning in 1984, a team has entered millions of assertions about the everyday world in a formal language and written inference rules over them. It is useful for some tasks. But after forty years, it has not reached the broad understanding its founders hoped for, which many see as a sign of the limits of hand-coding."),
  T("Philosophers raised deeper doubts. John Searle's Chinese Room argued in 1980 that shuffling symbols by rules, however well done, does not give understanding. The symbol grounding problem asks how a symbol can mean anything without a link to the world. Defenders replied that understanding may arise from the whole system, and the debate continues."),
  T("After 2010, deep learning delivered large gains on perception and language without hand-written rules. It learns from examples, copes with noise and needs no knowledge engineer. But it has its own weaknesses: errors that are hard to explain, a need for lots of data, and uncertain reasoning. These are exactly what symbolic methods were designed for."),
  T("So the symbolic ideas are far from dead. Search guides game programs and route planners. Logic verifies chips and software. Knowledge graphs power search engines and assistants. Neuro-symbolic systems pair neural perception with a reasoning step, or let language models call a solver. Studying GOFAI gives you the other half of the toolbox.")],
 [("Why is common sense hard for rule systems?", ["It needs huge amounts of knowledge and exceptions", "It is too short", "It is secret", "It uses colours"], 0, "Endless detail."),
  ("What is Cyc?", ["A long-running common-sense knowledge project", "A chess engine", "A Tarot deck", "A search engine"], 0, "Started in 1984."),
  ("What did Searle's Chinese Room argue?", ["Symbol shuffling alone is not understanding", "Computers can be taught Chinese", "Rules are enough", "Translation is easy"], 0, "1980."),
  ("What is brittleness?", ["Failing sharply outside narrow knowledge", "Running slowly", "Using more memory", "Looping forever"], 0, "Typical of expert systems."),
  ("What does neuro-symbolic AI try to do?", ["Combine learning and reasoning", "Replace all computers", "Draw pictures", "Avoid data"], 0, "Best of both."),
  ("Where do symbolic ideas still appear?", ["Search, planning, verification and knowledge graphs", "Nowhere", "Only in museums", "Only in games"], 0, "Everywhere in software.")],
 [("Cyc", "common-sense knowledge base, 1984"), ("Chinese Room", "Searle's 1980 argument"), ("Brittleness", "failure outside the narrow domain"), ("Neuro-symbolic", "learning plus reasoning")],
 [MATCH("Match the limit", "Pair each problem with its description.", [("Frame problem", "stating what does not change"), ("Brittleness", "sharp failure at the edges"), ("Knowledge bottleneck", "rules are slow to collect"), ("Symbol grounding", "where does meaning come from?"), ("Common sense", "huge amounts of everyday facts")]),
  ORDER("A short history", "Order these events from earliest to latest.", ["Dartmouth workshop", "Expert system boom", "Cyc project begins", "Deep Blue beats Kasparov", "Deep learning surge"]),
  FILL("Wrap up", "GOFAI used explicit {{symbols}} and rules. Its weakness was {{brittleness}} at the edges of its knowledge, and its legacy lives on in search, planning and {{knowledge}} graphs."),
  PL("Which approach?", "Write approach(task): return 'symbolic' for 'route planning', 'theorem proving', 'scheduling' and 'chip verification'; 'learning' for 'image recognition', 'speech recognition' and 'translation'; 'hybrid' for 'question answering'; otherwise 'unknown'.", "approach(task)", '''
def approach(task):
    if task in ["route planning", "theorem proving", "scheduling", "chip verification"]:
        return "symbolic"
    if task in ["image recognition", "speech recognition", "translation"]:
        return "learning"
    if task == "question answering":
        return "hybrid"
    return "unknown"
''', [["route planning"], ["image recognition"], ["question answering"], ["cooking"], ["scheduling"]], "Three lists of tasks."),
  PL("Rule coverage", "Write coverage(rules, cases): rules is a list of [conditions, conclusion] with conditions a list of fact names. cases is a list of fact lists. Return the number of cases for which at least one rule has all its conditions present. This shows the brittleness of a rule set on new cases.", "coverage(rules, cases)", '''
def coverage(rules, cases):
    n = 0
    for case in cases:
        hit = False
        for r in rules:
            ok = True
            for c in r[0]:
                if c not in case:
                    ok = False
            if ok:
                hit = True
        if hit:
            n = n + 1
    return n
''', [[[[["fever", "rash"], "measles"]], [["fever", "rash", "cough"], ["fever"], ["rash"]]], [[], [["a"]]], [[[["a"], "b"], [["c"], "d"]], [["a"], ["c"], ["e"]]]], "A case is covered if any rule fires on it.")]
))
