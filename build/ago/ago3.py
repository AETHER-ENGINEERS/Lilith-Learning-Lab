"""AlphaGo course, chapters 9-12."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

TTT = """
LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
def result(b):
    for l in LINES:
        if b[l[0]] != '.' and b[l[0]] == b[l[1]] and b[l[1]] == b[l[2]]:
            return b[l[0]]
    if '.' not in b:
        return 'D'
    return '.'
"""

# ------------------------------------------------------------ 9
CHS.append(CH(
 "The search: policy and value inside MCTS",
 ("AlphaGo search", [
  "Selection | maximizes | Q plus u",
  "u | grows with | Prior",
  "u | shrinks with | Visit count",
  "Leaf evaluation | mixes | Value network and rollout",
  "Backup | updates | Q and N",
  "Final move | is | Most visited",
  "Expansion | needs | Visit threshold"]),
 ["AlphaGo's search is Monte Carlo tree search with a twist: the networks guide it. Each edge of the tree stores a prior probability P from the SL policy network, a visit count N, and an average value Q.",
  "Selection picks the move with the highest Q plus a bonus u that is large for moves with a big prior and few visits. When a leaf is reached it is expanded, then evaluated two ways: by the value network, and by a fast rollout. The two are mixed with weight one half each.",
  "After the search the program plays the most visited move, not the one with the highest Q."],
 [("Prior P(s, a)", "The policy network's probability for move a in position s."),
  ("Visit count N(s, a)", "How many simulations passed through the edge."),
  ("Action value Q(s, a)", "The mean of the evaluations of all simulations through the edge."),
  ("Bonus u(s, a)", "An exploration term, proportional to P divided by 1 plus N."),
  ("Mixing parameter lambda", "The weight on the rollout in the leaf evaluation; 0.5 in the paper."),
  ("Virtual loss", "A temporary penalty added to a path being explored, so parallel threads spread out.")],
 ["Selection: a_t = argmax over a of Q(s_t, a) + u(s_t, a).",
  "u = c_puct * P * sqrt(sum_b N(s, b)) / (1 + N(s, a)) with c_puct = 5 in the paper.",
  "Leaf value: V = (1 - lambda) v_theta + lambda z, with lambda = 0.5.",
  "Backup: N += 1 and Q becomes the mean of all V in the subtree.",
  "A leaf is expanded when its edge has been visited 40 times (threshold n_thr = 40).",
  "At the end, play the most visited move; resign if the win estimate falls below 10 percent."],
 [T("The search is the heart of AlphaGo, where the four learned components meet. Each node of the search tree is a position. For each legal move from it, an edge stores three numbers. P is the prior probability of the move, supplied by a policy network. N is how many simulations have passed through the edge. Q is the average value of the evaluations found beneath it."),
  T("Every simulation starts at the root and walks down the tree, at each node taking the action that maximizes Q plus a bonus u. The bonus is proportional to the prior and shrinks as the edge is visited more. Moves the network likes get explored first; moves visited often rely on their measured value."),
  M(r"a_t \;=\; \arg\max_a\bigl(\, Q(s_t, a) + u(s_t, a)\,\bigr), \qquad u(s,a) \;=\; c_{\mathrm{puct}}\, P(s,a)\, \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)}"),
  T("The paper's methods give the constant c puct as five. The main text says only that u is proportional to the prior over one plus the visit count, and the fuller form with the square root appears in the methods. This is the rule that AlphaZero later reused under the name PUCT, a variant of the UCT rule from chapter 3."),
  T("When a simulation reaches a leaf, the leaf is evaluated in two ways. The value network gives v theta of the leaf, and a fast rollout with the rollout policy plays the game to the end for a result z. The leaf value is a blend of the two."),
  M(r"V(s_L) \;=\; (1-\lambda)\, v_\theta(s_L) \;+\; \lambda\, z_L, \qquad \lambda = 0.5"),
  T("The paper tested the blend. A version using only the value network, lambda equal to zero, reached an Elo rating of about 2,177, and the mixed version with lambda one half did best, with the two kinds of evaluation complementing each other: the value network is accurate on the position as a whole and the rollouts catch sharp tactical details."),
  T("The backup step then goes up the path. Each edge on the path gets its count N increased by one, and its Q set to the mean of all leaf values from the simulations that passed through it. A detail to watch: Q must be seen from the viewpoint of the player who owns the edge, so the sign flips from level to level."),
  T("Other numbers from the methods. The SL policy network supplies the priors, with a softmax temperature of 0.67. A node is expanded only once its edge has been visited forty times; before that the cheaper tree policy provides the priors. Parallel threads use a virtual loss of three to avoid all following the same path. In the end the program plays the most visited move at the root, and it resigns if its best estimated win probability drops below ten percent.")],
 [("What does the bonus u favour?", ["High prior and few visits", "Low prior and many visits", "Illegal moves", "The last move"], 0, "P over 1 plus N."),
  ("What is lambda in the leaf evaluation?", ["The rollout weight, 0.5", "The komi", "The learning rate", "The number of threads"], 0, "V = (1 - lambda) v + lambda z."),
  ("Which move does AlphaGo play at the root?", ["The most visited", "The highest prior", "A random one", "The last explored"], 0, "Visits are more robust than Q."),
  ("What is virtual loss for?", ["To spread parallel threads over different paths", "To lose games on purpose", "To resign", "To raise Q"], 0, "A temporary penalty.")],
 [("What is c_puct?", "A constant, 5 in the paper."), ("What does Q average?", "The leaf values in the subtree."), ("When is a node expanded?", "After 40 visits to its edge."),
  ("When does AlphaGo resign?", "When its win estimate drops below 10 percent.")],
 [PL("Select an edge", "Write select(Q, N, P, cpuct): return the index of the edge maximizing Q[i] + cpuct * P[i] * sqrt(sum(N)) / (1 + N[i]); ties go to the smaller index. Use import math.",
     "select(Q, N, P, cpuct)", """
import math
def select(Q, N, P, cpuct):
    root = math.sqrt(sum(N))
    best = -1e9
    arg = 0
    for i in range(len(Q)):
        s = Q[i] + cpuct * P[i] * root / (1 + N[i])
        if s > best + 1e-12:
            best = s
            arg = i
    return arg
""", [[[0.0, 0.0, 0.0], [0, 0, 0], [0.2, 0.5, 0.3], 5.0], [[0.1, 0.4, 0.0], [10, 5, 1], [0.2, 0.5, 0.3], 5.0], [[0.5, 0.0], [100, 1], [0.1, 0.9], 5.0], [[-0.2, 0.3, 0.3], [4, 4, 4], [0.3, 0.3, 0.4], 1.0], [[0.9, 0.1], [50, 0], [0.5, 0.5], 0.0]], "Compute Q plus the bonus for every edge and take the largest."),
  PL("Mix the leaf evaluations", "Write leaf_value(v, z, lam): (1 - lam) * v + lam * z.",
     "leaf_value(v, z, lam)", """
def leaf_value(v, z, lam):
    return (1 - lam) * v + lam * z
""", [[0.4, 1, 0.5], [0.4, -1, 0.5], [0.4, 1, 0.0], [-0.6, 1, 1.0], [0.0, 0, 0.5]], "A weighted average of the two numbers.", approx=1e-12),
  PL("Back up a value", "An edge has visit count N and mean value Q. A simulation returns value v through it. Write backup(Q, N, v): return [new Q, new N] with N + 1 and Q equal to the running mean.",
     "backup(Q, N, v)", """
def backup(Q, N, v):
    n = N + 1
    return [Q + (v - Q) / n, n]
""", [[0.0, 0, 1.0], [0.5, 1, -0.5], [0.2, 9, 1.0], [-1.0, 3, -1.0], [0.25, 4, 0.75]], "New mean = old mean + (v - old mean) / new count.", approx=1e-12),
  PL("Virtual loss", "With virtual loss n_vl a path being explored temporarily has N + n_vl visits and total value W - n_vl. Write q_virtual(W, N, nvl): the resulting Q = (W - nvl) / (N + nvl).",
     "q_virtual(W, N, nvl)", """
def q_virtual(W, N, nvl):
    return (W - nvl) / (N + nvl)
""", [[6.0, 10, 3], [0.0, 0, 3], [-2.0, 4, 3], [10.0, 20, 0]], "Apply the penalty to both numerator and denominator.", approx=1e-12),
  PL("Final move and resignation", "Write finish(N, Q): return [index of the most visited move (ties go to the smaller index), 1 if the best Q is below -0.8 (resign) else 0]. N and Q are lists per root move.",
     "finish(N, Q)", """
def finish(N, Q):
    best = 0
    for i in range(len(N)):
        if N[i] > N[best]:
            best = i
    resign = 0
    if max(Q) < -0.8:
        resign = 1
    return [best, resign]
""", [[[10, 50, 20], [0.1, 0.3, 0.2]], [[5, 5], [0.0, 0.1]], [[1, 2, 3], [-0.9, -0.85, -0.95]], [[7], [-0.8]]], "Most visits for the move; compare the largest Q with the resign threshold."),
  ORDER("One AlphaGo simulation", "Order the steps.", ["Walk down the tree choosing the edge with the highest Q plus u", "Reach a leaf and expand it", "Evaluate with the value network", "Play a fast rollout to the end", "Mix the two values and back them up"]),
  MATCH("Search terms", "Match each symbol with its meaning.", [("P", "Prior from the policy network"), ("N", "Visit count"), ("Q", "Mean value of simulations"), ("u", "Exploration bonus"), ("lambda", "Mixing weight of the rollout")]),
  FILL("Search", "The leaf value mixes the {{value network|value}} with a {{rollout}}. The program plays the {{most visited|most-visited}} move.")]))

# ------------------------------------------------------------ 10
CHS.append(CH(
 "Engineering and strength: hardware, Elo, scaling",
 ("Strength", [
  "Elo rating | predicts | Win probability",
  "Single machine | used | 48 CPUs and 8 GPUs",
  "Distributed AlphaGo | used | 1,202 CPUs and 176 GPUs",
  "Asynchronous search | runs | Many simulations in parallel",
  "Virtual loss | spreads | Threads",
  "AlphaGo | won | 494 of 495 games against programs",
  "Value-only | scored | Elo about 2,177"]),
 ["Strength in Go is measured with the Elo rating: a difference of 400 points means the stronger side is expected to win about 91 percent of the time. The paper's table gives a single-machine AlphaGo about 2,890 and the distributed version about 3,140, against 1,929 for Crazy Stone.",
  "The distributed version used 1,202 CPUs and 176 GPUs in the match against Fan Hui. The paper also ran a tournament in which the single-machine version, with 48 CPUs and 8 GPUs, won 494 of its 495 games against other Go programs.",
  "The search ran asynchronously: many threads walk the tree at once, while the networks are evaluated on GPUs in a batch behind them."],
 [("Elo rating", "A rating scale where the expected score depends on the rating difference."),
  ("Expected score", "1 / (1 + 10^(-d/400)) for a rating advantage d."),
  ("Asynchronous search", "Many simulations run at the same time and share the tree."),
  ("Search thread", "One of the parallel workers."),
  ("Handicap", "Extra stones given to the weaker player at the start."),
  ("Distributed version", "AlphaGo running across a cluster of machines.")],
 ["Elo: expected score = 1 / (1 + 10^(-d/400)); 400 points is about 91 percent.",
  "Single machine: 40 search threads, 48 CPUs, 8 GPUs, Elo about 2,890.",
  "Distributed: 40 search threads, 1,202 CPUs, 176 GPUs, Elo about 3,140.",
  "Against other programs the single machine won 494 of 495 games with 5 seconds per move.",
  "Distributed AlphaGo beat the single-machine version 77 percent of the time.",
  "Mixed evaluation beat value-only and rollout-only versions."],
 [T("How strong is strong? The Nature paper answers with a tournament. It pitted AlphaGo against the best programs available: Crazy Stone, Zen, Pachi, Fuego and GnuGo, giving each five seconds per move. The single-machine AlphaGo won 494 out of 495 games, a winning rate of 99.8 percent. Against four handicap stones it still won 77 percent against Crazy Stone, 86 percent against Zen and 99 percent against Pachi."),
  T("The paper converts results to Elo ratings, a scale in which a given rating difference corresponds to a given expected score. Distributed AlphaGo scored 3,140, single-machine AlphaGo 2,890, Crazy Stone 1,929, Zen 1,888, Pachi 1,298, Fuego 1,148 and GnuGo 431. The distributed version won 77 percent of games against the single machine, which fits a difference of about 250 Elo."),
  M(r"E \;=\; \frac{1}{1 + 10^{-d/400}}"),
  T("Here d is the rating advantage, and E the expected score. A difference of zero gives one half. A difference of four hundred gives about ninety-one percent. The formula can be reversed to get the Elo difference implied by a winning rate, which the practice section does."),
  T("Now the engineering. The single-machine version used 48 CPUs and 8 GPUs, and forty search threads. The distributed version used 1,202 CPUs and 176 GPUs, again with forty search threads but with evaluation spread across machines. The paper's largest test configuration reached 1,920 CPUs and 280 GPUs. The paper's table also shows the rating rising with extra GPUs on one machine, then flattening."),
  T("Parallel search raises a problem. If forty threads each pick the best edge at the same time, they all pick the same one. The remedy is virtual loss: when a thread passes through an edge, the edge temporarily looks worse by a few lost games, so the next thread is nudged to a different path. When the evaluation returns, the penalty is removed and the real result is added."),
  T("The networks are slow, so the search does not wait for them. When a thread reaches a leaf, it requests an evaluation and continues. The paper says that the evaluation of the policy network happens asynchronously on GPUs, while the search thread uses the quick tree policy for provisional priors, then updates them when the network answers. Rollouts, by contrast, run on the CPUs."),
  T("In the practice section you convert between Elo and win rates, build a rating table, compute the cost of the rollouts, and decide handicaps from rating differences.")],
 [("What does a 400 Elo advantage mean?", ["About 91 percent expected score", "A guaranteed win", "A draw", "50 percent"], 0, "E = 1 / (1 + 10^-1)."),
  ("What did single-machine AlphaGo score against other programs?", ["494 of 495", "250 of 495", "1 of 495", "495 of 495"], 0, "99.8 percent."),
  ("Why use virtual loss?", ["So parallel threads explore different paths", "To reduce hardware", "To end games", "To make Q negative"], 0, "A temporary penalty."),
  ("What does the distributed version have over the single machine?", ["More CPUs and GPUs", "A different rule set", "Human help", "A bigger board"], 0, "1,202 CPUs and 176 GPUs against 48 and 8.")],
 [("What is Elo for?", "Predicting win probabilities."), ("How many search threads were used?", "Forty."), ("What won 77 percent against the single machine?", "The distributed version."),
  ("What is asynchronous search?", "Parallel simulations sharing one tree.")],
 [PL("Expected score", "Write elo_expected(d): 1 / (1 + 10 ** (-d / 400)).",
     "elo_expected(d)", """
def elo_expected(d):
    return 1 / (1 + 10 ** (-d / 400))
""", [[0], [400], [-400], [250], [1000]], "Direct formula.", approx=1e-9),
  PL("Elo from a win rate", "Write elo_diff(w): the rating advantage implied by winning rate w (0 < w < 1): 400 * log10(w / (1 - w)), rounded to 1 decimal. Use import math.",
     "elo_diff(w)", """
import math
def elo_diff(w):
    return round(400 * math.log10(w / (1 - w)), 1)
""", [[0.5], [0.77], [0.8], [0.85], [0.998]], "Invert the expected-score formula."),
  PL("Predict a match", "ratings is a dict-free list of [name, rating] pairs. Write head_to_head(ratings, i, j): the expected score of player i against player j, rounded to 3 decimals.",
     "head_to_head(ratings, i, j)", """
def head_to_head(ratings, i, j):
    d = ratings[i][1] - ratings[j][1]
    return round(1 / (1 + 10 ** (-d / 400)), 3)
""", [[[["distributed", 3140], ["single", 2890], ["Crazy Stone", 1929]], 0, 1], [[["distributed", 3140], ["single", 2890], ["Crazy Stone", 1929]], 1, 2], [[["distributed", 3140], ["single", 2890], ["Crazy Stone", 1929]], 2, 0], [[["a", 1000], ["b", 1000]], 0, 1]], "Take the rating difference, then the formula."),
  PL("Rank by rating", "Write ranking(ratings): the list of names sorted from highest to lowest rating (ties by the order given). ratings is a list of [name, rating].",
     "ranking(ratings)", """
def ranking(ratings):
    order = sorted(range(len(ratings)), key=lambda i: (-ratings[i][1], i))
    return [ratings[i][0] for i in order]
""", [[[["Pachi", 1298], ["Zen", 1888], ["Crazy Stone", 1929], ["Fuego", 1148]]], [[["a", 5], ["b", 5]]], [[["x", 1], ["y", 3], ["z", 2]]]], "Sort the indices by rating, highest first."),
  ORDER("Parallel search", "Order the events for one thread.", ["Walk down the tree", "Add a virtual loss on the path", "Request evaluation of the leaf", "Continue with provisional priors", "Replace the virtual loss with the real result"]),
  MATCH("Hardware and ratings", "Match each item with its value.", [("Single machine", "48 CPUs, 8 GPUs"), ("Distributed (match)", "1,202 CPUs, 176 GPUs"), ("Distributed Elo", "About 3,140"), ("Single Elo", "About 2,890"), ("Crazy Stone Elo", "About 1,929")]),
  FILL("Strength", "A {{400|four hundred}} point Elo advantage gives about {{91}} percent expected score. Virtual loss helps {{parallel|multiple}} threads explore different paths.")]))

# ------------------------------------------------------------ 11
CHS.append(CH(
 "Capstone: a miniature AlphaGo",
 ("A tiny AlphaGo", [
  "Policy prior | guides | Search",
  "PUCT selection | chooses | Edges",
  "Rollout | plays | To the end",
  "Value stub | gives | Zero",
  "Leaf value | mixes | Value and rollout",
  "Backup | flips | Sign each level",
  "Visits | decide | The move"]),
 ["This chapter puts the pieces together on tic-tac-toe, small enough to run in a lab. The prior comes from a hand-made rule instead of a policy network, the value network is a stub that always says zero, and the rollouts use a tiny random generator. Everything else follows the paper: PUCT selection with constant five, a leaf value mixing value and rollout, a sign flip in backup and the most-visited move at the end.",
  "It is a teaching miniature, not DeepMind's program. Its purpose is to show that the loop of chapter 9 is short to write.",
  "Build it in steps: result detection, prior, rollout, then the full search."],
 [("Prior", "The preference over moves before any search; here a hand-made table."),
  ("Stub value", "A placeholder value network that returns zero."),
  ("Rollout", "A random game played to the end from the leaf."),
  ("Sign flip", "The value of a child is the negative of its value for the parent."),
  ("Visit counts", "The result of the search; the most visited move is played."),
  ("Seed", "The start of the pseudo-random generator, fixing the results.")],
 ["Selection uses Q + 5 * P * sqrt(sum N) / (1 + N).",
  "A new leaf is evaluated as 0.5 * v + 0.5 * z with v = 0 here.",
  "z is the outcome of a random rollout from the leaf's player-to-move view.",
  "Values flip sign each level going up.",
  "Terminal positions are scored exactly: -1 for the player to move who has lost, 0 for a draw.",
  "The move with most visits is chosen."],
 [T("Time to build. The game is tic-tac-toe, played on a board of nine characters, X, O or a dot. It has no hidden depth, but it has everything the search needs: legal moves, terminal positions and sign flips between the players."),
  T("Start with the prior. A real AlphaGo asks the SL policy network. We use a hand-made table that favours the centre, then the corners, then the edges. After a softmax over the legal moves it plays the role of the probabilities P. Next, the value network. A trained one is out of reach in a lab, so the stub value is zero, meaning no opinion. The rollouts do the real work, and the mixing weight one half applies to the zero."),
  T("The rollout is a random game played from the leaf to the end. We use the same small generator as in chapter 3, so the results are repeatable. The outcome z is scored from the point of view of the player to move at the leaf: plus one if that player eventually wins, minus one if they lose, zero for a draw."),
  T("The search itself is a loop. In each simulation, walk down from the root. At each node already in the tree, apply the PUCT rule to choose a move, using the stored visit counts and values. At the first new node, create it, compute its priors, evaluate it with the mixed value, and stop. If the walk reaches a finished game, score it exactly. Then walk back up, adding one to each count and the value to each total, flipping the sign each time."),
  M(r"V = \tfrac12\, v_\theta + \tfrac12\, z, \qquad v_\theta \equiv 0"),
  T("The sign flip deserves attention. A value is always stored from the viewpoint of the player who plays the edge. A good result for the child node, where the opponent moves, is a bad result for us. So when passing a value up one level, negate it. Forgetting this is the commonest bug in tree-search code."),
  T("At the end the visit counts at the root are the answer. With enough simulations the winning moves collect most of the visits. The most visited move is played, following the paper. The program is far too small to play Go, but the same loop with a real network and a Go simulator is what AlphaGo does."),
  T("In the practice section you first write the board helpers and the prior, then the rollout, and finally the whole search, comparing it with a position where the win is easy to see.")],
 [("What does the stub value network return?", ["Zero", "One", "The best move", "The komi"], 0, "No opinion; the rollouts do the work."),
  ("Why flip the sign in backup?", ["Players alternate", "Values are negative", "To save memory", "It is optional"], 0, "A good result for the child is bad for the parent."),
  ("Which move does the miniature play?", ["The most visited", "The highest prior", "The first legal", "The last visited"], 0, "As in the paper."),
  ("What is z?", ["The rollout outcome", "The prior", "The komi", "The loss"], 0, "Scored from the leaf player's view.")],
 [("What replaces the policy network?", "A hand-made prior table."), ("What replaces the value network?", "A stub returning zero."), ("Why use a seeded generator?", "So results are repeatable."),
  ("Is the miniature strong?", "No, it is a teaching example.")],
 [PL("Prior over moves", "The hand-made score of each square is [3, 2, 3, 2, 4, 2, 3, 2, 3] (corners 3, edges 2, centre 4). Write prior(board): the softmax of 0.5 * score over the empty squares (zero probability for occupied squares). Return a list of nine probabilities rounded to 9 decimals. Use import math.",
     "prior(board)", """
import math
SC = [3, 2, 3, 2, 4, 2, 3, 2, 3]
def prior(board):
    e = []
    for i in range(9):
        if board[i] == '.':
            e.append(math.exp(0.5 * SC[i]))
        else:
            e.append(0.0)
    s = sum(e)
    return [round(x / s, 9) for x in e]
""", [["........."], ["....X...."], ["XOXOXOO.."], ["X.O.X.O.."]], "Exponentiate scaled scores for empty squares only, then normalize.", approx=1e-9),
  PL("A random rollout", "Using the generator x = (75 * x + 74) % 65537 (state starts at seed), play random moves from the board for the player to move until the game ends; at each turn choose empty squares in ascending order and use index x % (number of empty squares). Write rollout(board, player, seed): return [outcome from the view of the player to move at the start (+1 win, -1 loss, 0 draw), the final state of the generator].",
     "rollout(board, player, seed)", TTT + """
def rollout(board, player, seed):
    b = list(board)
    x = seed
    me = player
    cur = player
    while True:
        r = result(b)
        if r != '.':
            if r == 'D':
                return [0, x]
            if r == me:
                return [1, x]
            return [-1, x]
        empt = [i for i in range(9) if b[i] == '.']
        x = (75 * x + 74) % 65537
        m = empt[x % len(empt)]
        b[m] = cur
        if cur == 'X':
            cur = 'O'
        else:
            cur = 'X'
""", [["XX.OO....", "X", 5], ["........." , "X", 1], ["XOXOXOO..", "X", 9], ["XO.XO....", "O", 3], ["XXXOO....", "O", 2]], "Play until result() says the game is over; map the winner to +1, -1 or 0."),
  PL("Miniature AlphaGo", "Write mini_alphago(board, player, sims, seed): run sims simulations of the AlphaGo search on tic-tac-toe. Each tree node (keyed by the board string and player) stores per-move N and W (total value) and priors from the prior() table above. Selection: argmax over legal moves of Q + 5 * P * sqrt(sum N) / (1 + N), Q = W / N (0 if N = 0), ties go to the smaller index. At an unseen node create it and evaluate the leaf as 0.5 * 0 + 0.5 * z where z is the random rollout outcome (generator state shared across simulations, starting at seed) from that node's player-to-move view; at a finished game use the exact value (-1 if the previous mover just won, 0 for a draw). Back up with sign flips. Return the list of nine root visit counts.",
     "mini_alphago(board, player, sims, seed)", TTT + """
import math
SC = [3, 2, 3, 2, 4, 2, 3, 2, 3]
def mini_alphago(board, player, sims, seed):
    state = [seed]
    tree = {}
    def other(p):
        if p == 'X':
            return 'O'
        return 'X'
    def rollout(b0, p0):
        b = list(b0)
        cur = p0
        while True:
            r = result(b)
            if r != '.':
                if r == 'D':
                    return 0
                if r == p0:
                    return 1
                return -1
            empt = [i for i in range(9) if b[i] == '.']
            state[0] = (75 * state[0] + 74) % 65537
            b[empt[state[0] % len(empt)]] = cur
            cur = other(cur)
    def make(b):
        e = []
        for i in range(9):
            if b[i] == '.':
                e.append(math.exp(0.5 * SC[i]))
            else:
                e.append(0.0)
        s = sum(e)
        return {'P': [x / s for x in e], 'N': [0] * 9, 'W': [0.0] * 9}
    def sim(b, p):
        r = result(b)
        if r != '.':
            if r == 'D':
                return 0.0
            return -1.0
        key = ''.join(b) + p
        if key not in tree:
            tree[key] = make(b)
            z = rollout(b, p)
            return 0.5 * 0.0 + 0.5 * z
        nd = tree[key]
        root = math.sqrt(sum(nd['N']))
        best = -1e9
        mv = -1
        for i in range(9):
            if b[i] == '.':
                q = 0.0
                if nd['N'][i] > 0:
                    q = nd['W'][i] / nd['N'][i]
                s = q + 5 * nd['P'][i] * root / (1 + nd['N'][i])
                if s > best + 1e-12:
                    best = s
                    mv = i
        nb = list(b)
        nb[mv] = p
        v = -sim(nb, other(p))
        nd['N'][mv] += 1
        nd['W'][mv] += v
        return v
    b = list(board)
    for k in range(sims):
        sim(b, player)
    return tree[''.join(b) + player]['N']
""", [["XX.OO....", "X", 40, 1], ["........." , "X", 30, 3], ["XO.XO....", "X", 40, 7], ["XOXOX.O..", "O", 30, 5]], "Follow chapter 9: select, expand once per simulation, evaluate, back up with sign flips."),
  PL("Which move does it play?", "Write choose(counts): the index of the largest visit count (ties to the smaller index).",
     "choose(counts)", """
def choose(counts):
    best = 0
    for i in range(len(counts)):
        if counts[i] > counts[best]:
            best = i
    return best
""", [[[0, 5, 1, 0, 9, 0, 0, 0, 2]], [[3, 3, 0]], [[0]], [[1, 2, 3, 3, 2, 1]]], "Keep the first maximum."),
  ORDER("Build the miniature", "Order the build steps.", ["Detect finished games", "Write the prior table", "Write the random rollout", "Write selection with the bonus", "Write backup with sign flips"]),
  MATCH("Stand-ins", "Match each stand-in with the real component.", [("Hand-made table", "SL policy network"), ("Stub returning 0", "Value network"), ("Random generator rollouts", "Rollout policy"), ("Tic-tac-toe rules", "Go simulator"), ("Visit counts", "Final move choice")]),
  FILL("Capstone", "Values flip {{sign}} going up the tree. The final move is the {{most visited|most-visited}} one. The stub value network always says {{zero|0}}.")]))

# ------------------------------------------------------------ 12
CHS.append(CH(
 "Matches, successors and criticism",
 ("History and legacy", [
  "AlphaGo Fan | beat | Fan Hui 5-0",
  "AlphaGo Lee | beat | Lee Sedol 4-1",
  "Lee Sedol | won | Game 4",
  "AlphaGo Master | won | 60-0 online",
  "AlphaGo Zero | dropped | Human data",
  "AlphaZero | generalized | To chess and shogi",
  "Criticism | targets | Compute and generality"]),
 ["The first AlphaGo, later called Fan, beat Fan Hui 5-0 in October 2015. A stronger version, Lee, beat Lee Sedol four games to one in March 2016. Lee won game four after a move, number 78, that the program had not anticipated.",
  "Master, an updated version, won 60 straight online games in late December 2016 and early January 2017, and in May 2017 beat Ke Jie 3-0. AlphaGo Zero then learned Go from self-play alone, without human games, and beat the Lee version 100-0.",
  "Critics pointed to the huge computing cost, the reliance on human data in the first versions, and the narrowness of Go as a test of intelligence."],
 [("AlphaGo Fan", "The October 2015 version that beat Fan Hui."),
  ("AlphaGo Lee", "The March 2016 version that beat Lee Sedol."),
  ("AlphaGo Master", "The 2017 version that won 60-0 online and beat Ke Jie."),
  ("AlphaGo Zero", "A version trained from scratch by self-play with no human data."),
  ("Move 78", "Lee Sedol's move in game four, called the divine move."),
  ("Honorary dan", "A professional rank awarded by Go associations to AlphaGo.")],
 ["October 2015: AlphaGo beat Fan Hui, a 2-dan professional, 5-0.",
  "March 2016: AlphaGo beat Lee Sedol 4-1; all games ended by resignation; Chinese rules with 7.5 komi.",
  "Lee won game four by resignation at move 180, his move 78 was unanticipated by the program.",
  "Master won 60 online games without a loss and beat Ke Jie 3-0 in May 2017.",
  "AlphaGo Zero beat the Lee version 100-0 and later versions without human data.",
  "AlphaZero extended the Zero method to chess and shogi."],
 [T("The first public match was in secret. In October 2015 the distributed version of AlphaGo played Fan Hui, the European champion and a professional of two dan, in five games. It won all five. It was the first time a Go program had beaten a professional without handicap on a full board. The news was held until the Nature paper appeared on 27 January 2016."),
  T("Then came Seoul. From 9 to 15 March 2016, AlphaGo played Lee Sedol, a nine dan professional, in five games under Chinese rules with seven and a half points komi. The prize was one million US dollars, to be donated to charities. AlphaGo won games one, two and three, each by resignation, so the match was decided after three games."),
  T("Game two is remembered for move 37 by AlphaGo, a surprising shoulder hit that commentators found strange at first; this is widely reported but is not covered in the sources that I used here. Game four is remembered for Lee Sedol. He won by resignation at move 180, and his move 78 is often called the divine move. Afterwards Aja Huang explained that AlphaGo's networks had not expected that move and so the program failed to adjust, a weakness the team patched. Game five went to AlphaGo, for a final score of four to one."),
  T("Lee Sedol said after the match that he had misjudged the program's abilities and that the loss was not a defeat of mankind. AlphaGo received an honorary nine dan from the Korea Baduk Association. Fan Hui, by contrast, described the program's style as conservative, and the referee of his match said the same. Strategists noted that AlphaGo prized probability of winning over the size of its lead, so it often chose safe moves that won by little."),
  T("Next versions. In late December 2016 and early January 2017, an account named Master, later confirmed to be an updated AlphaGo, won sixty games without a loss against top professionals online, including three against the top-ranked Ke Jie. In May 2017 at the Future of Go Summit in Wuzhen, Master beat Ke Jie three games to nothing. AlphaGo was then retired."),
  T("Then the Zero line removed the human data. AlphaGo Zero, published in October 2017, learned from self-play alone. After three days it surpassed the Lee version, winning a hundred games to none, and after forty days it exceeded all earlier versions. AlphaZero, in December 2017, applied the same idea to chess and shogi as well as Go. The AlphaZero course in this library covers it."),
  M(r"\text{Fan}\ \to\ \text{Lee}\ \to\ \text{Master}\ \to\ \text{Zero}\ \to\ \text{AlphaZero}"),
  T("Criticism and caveats. The original needed expert game records, so it depended on human knowledge. Its hardware was large: a cluster of CPUs and GPUs, or by one account 1,920 CPUs and 280 GPUs for the Lee match. It needs a perfect simulator of the rules to search. Go is also only one game, and doing well at it does not by itself show general intelligence. Lee Sedol retired in 2019, saying that AI dominance meant he could never be the top overall player."),
  T("What changed in the world? Professional players studied AlphaGo's moves and revised long-held opening habits. Fan Hui, who lost to it, said the experience taught him to see things he had not seen before, and his ranking climbed afterwards. A film about the preparation for the Lee match, directed by Greg Kohs, was released.")],
 [("Who did AlphaGo beat in October 2015?", ["Fan Hui", "Lee Sedol", "Ke Jie", "Kasparov"], 0, "5-0."),
  ("Who won game four of the Lee match?", ["Lee Sedol", "AlphaGo", "Nobody", "Fan Hui"], 0, "By resignation at move 180."),
  ("What did AlphaGo Zero remove?", ["Human game data", "The search", "The rules", "The networks"], 0, "It learned from self-play alone."),
  ("What did Master win online?", ["60 games without a loss", "10 games", "All but one", "None"], 0, "Late December 2016 to January 2017.")],
 [("What was the Lee match prize?", "One million US dollars, donated to charity."), ("What was the komi?", "7.5 points."), ("What extended Zero to chess and shogi?", "AlphaZero."),
  ("How did Lee describe the result?", "Not a defeat of mankind.")],
 [PL("Match arithmetic", "Write match_status(results): results is a list of 'A' (AlphaGo wins) or 'L' (Lee wins) per game, in order. Return [AlphaGo wins, Lee wins, the 1-based game number at which someone first reached 3 wins, or 0 if nobody did].",
     "match_status(results)", """
def match_status(results):
    a = 0
    l = 0
    decided = 0
    for i in range(len(results)):
        if results[i] == 'A':
            a += 1
        else:
            l += 1
        if decided == 0 and (a == 3 or l == 3):
            decided = i + 1
    return [a, l, decided]
""", [[["A", "A", "A", "L", "A"]], [["A", "A", "L", "L", "A"]], [["L", "A"]], [["A", "L", "A", "L", "L"]], [[]]], "Count wins and note when either reaches three."),
  PL("Win rate to Elo", "AlphaGo Zero beat the Lee version 100-0 and the Master version 89-11. Write score_pct(wins, losses): the percentage of games won, rounded to 1 decimal.",
     "score_pct(wins, losses)", """
def score_pct(wins, losses):
    return round(100.0 * wins / (wins + losses), 1)
""", [[4, 1], [100, 0], [89, 11], [60, 0], [1, 4]], "A simple ratio."),
  PL("Order the versions", "versions is a list of [name, year, month]. Write timeline(versions): the names sorted by date (year, then month; ties by the given order).",
     "timeline(versions)", """
def timeline(versions):
    order = sorted(range(len(versions)), key=lambda i: (versions[i][1], versions[i][2], i))
    return [versions[i][0] for i in order]
""", [[[["Lee", 2016, 3], ["Fan", 2015, 10], ["Zero", 2017, 10], ["Master", 2017, 5]]], [[["a", 2020, 1], ["b", 2020, 1]]], [[["x", 2019, 12], ["y", 2019, 2]]]], "Sort indices by year and month."),
  ORDER("History", "Put the milestones in order.", ["AlphaGo Fan beats Fan Hui 5-0", "AlphaGo Lee beats Lee Sedol 4-1", "Master wins 60-0 online", "Master beats Ke Jie 3-0", "AlphaGo Zero beats Lee 100-0"]),
  MATCH("Versions", "Match each version with its achievement.", [("AlphaGo Fan", "5-0 against Fan Hui"), ("AlphaGo Lee", "4-1 against Lee Sedol"), ("AlphaGo Master", "60-0 online, 3-0 against Ke Jie"), ("AlphaGo Zero", "No human data; 100-0 against Lee"), ("AlphaZero", "Chess, shogi and Go")]),
  {"type": "webxdc", "title": "Go liberties board", "intro": "Play on a small board. Place stones in turn, watch the liberties of each group, and capture a group. Capture at least one group and play six moves.", "height": 680, "html": "__GO__"},
  FILL("Legacy", "Lee Sedol won game {{four|4}} with move {{78}}. AlphaGo {{Zero}} learned from self-play without human data.")]))
