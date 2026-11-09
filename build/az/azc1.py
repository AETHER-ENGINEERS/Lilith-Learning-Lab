"""AlphaZero course, chapters 1-4."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

LINES_SRC = "[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]"

# ------------------------------------------------------------ 1
CHS.append(CH(
 "What is AlphaZero?",
 ("The big picture", [
  "AlphaZero | generalizes | AlphaGo Zero",
  "AlphaZero | learns by | Self-play",
  "AlphaZero | knows | Only the game rules",
  "Neural network | outputs | Move probabilities and value",
  "Monte Carlo tree search | uses | The network",
  "Search result | trains | The network",
  "AlphaZero | played | Chess, shogi and Go"]),
 ["AlphaZero is a reinforcement learning algorithm from DeepMind that learns board games from scratch. It starts from random play and is given nothing but the rules. It plays against itself, and in its first paper it reached superhuman strength in chess, shogi and Go.",
  "Its core is a loop. A neural network guides a Monte Carlo tree search. The search picks moves and plays games against itself. The finished games become training data that improve the network, which makes the next search better.",
  "The course builds every piece in small Python programs: game search, tree search, the network's outputs, the loss, the training loop and a tiny working search for tic-tac-toe."],
 [("Tabula rasa", "Latin for blank slate: learning without human data or hand-written knowledge."),
  ("Self-play", "The program plays games against itself and learns from the results."),
  ("Policy", "A probability distribution over moves."),
  ("Value", "A number estimating how good a position is; here the expected game outcome."),
  ("MCTS", "Monte Carlo tree search: a search that builds a tree from many simulated games."),
  ("Reinforcement learning", "Learning from outcomes of actions rather than from labelled examples.")],
 ["AlphaZero is a general version of AlphaGo Zero.",
  "It uses only the rules of the game: no opening books, no human games, no hand-written evaluation.",
  "One network f(s) = (p, v) gives move probabilities and a value.",
  "MCTS guided by the network chooses moves; the search results train the network.",
  "The same algorithm and hyperparameters were used for chess, shogi and Go, except the exploration noise.",
  "The program was never released; the papers describe the algorithm."],
 [T("AlphaZero is a reinforcement learning algorithm published by DeepMind in a preprint in December 2017, with a peer-reviewed version in the journal Science on 7 December 2018. Its abstract claims that, starting from random play and given no domain knowledge except the game rules, it reached superhuman play in chess and shogi as well as Go within 24 hours, and convincingly defeated a world-champion program in each."),
  T("To see why that mattered, look at what came before. The strongest chess and shogi programs used a highly optimized alpha-beta search with many domain-specific adaptations, and an evaluation function written by human experts over decades. AlphaZero replaces the handwritten evaluation and move-ordering rules with a deep neural network, and replaces alpha-beta with a general-purpose Monte Carlo tree search."),
  T("The line of programs. AlphaGo Fan beat the European Go champion Fan Hui in October 2015. AlphaGo Lee beat Lee Sedol in March 2016. AlphaGo Master then beat a team of professionals online. These versions all started from supervised learning on human expert games. AlphaGo Zero, published in Nature in October 2017, removed the human data completely and learned Go from self-play alone; it beat the earlier champion-defeating AlphaGo 100 games to 0."),
  T("AlphaZero is the next step: a more generic version of AlphaGo Zero. It drops Go-specific details such as symmetry augmentation and the gating of new networks, and applies the same algorithm to chess and shogi, whose rules are asymmetric and whose moves are harder to encode. The only game-specific setting that changed between games was the scale of the exploration noise."),
  M(r"(\mathbf{p},\, v) = f_{\theta}(s)"),
  T("The heart of it is one function. A neural network f with parameters theta takes a board position s and returns a vector p of move probabilities and a scalar v, the expected outcome of the game for the player to move. Early in training the outputs are close to random. Everything else in the algorithm exists to make them good."),
  T("The loop has three steps that repeat. First, play: at every position, run a tree search that uses the network, choose a move from the search result, and play a whole game against yourself. Second, record: for each position keep the search's move probabilities and the final outcome. Third, train: adjust the network so that p matches the search probabilities and v matches the outcomes. Then play again with the improved network."),
  T("A useful way to see it, used in the papers: the search acts as a policy improvement step, since it produces better move probabilities than the raw network gives, and the network is trained toward them. Self-play outcomes act as policy evaluation. Chapter 8 returns to this."),
  T("A note on sources. This course follows the AlphaZero preprint and Science paper by Silver and colleagues, the AlphaGo Zero paper in Nature, and secondary coverage of the matches and the debate that followed. Numbers quoted come from those sources. Chapter 11 is my own tic-tac-toe implementation, a small demonstration of the idea and not a copy of DeepMind's code, which was never released."),
  T("Be realistic about scale. The published training used thousands of specialized chips. The labs here are tiny versions that teach the mechanics; they are not meant to reach master strength.")],
 [("What does AlphaZero need to know about a game?", ["Opening books", "Only the rules", "Human games", "A hand-written evaluation"], 1, "It starts tabula rasa."),
  ("What does the network f(s) output?", ["A move only", "Move probabilities and a value", "A board image", "A win count"], 1, "(p, v) = f_theta(s)."),
  ("What replaces alpha-beta search in AlphaZero?", ["Minimax", "Monte Carlo tree search guided by the network", "Brute force", "A lookup table"], 1, "A general-purpose MCTS."),
  ("What is the main difference from AlphaGo?", ["It plays slower", "It uses no human data", "It uses no neural network", "It plays only Go"], 1, "AlphaGo started from human expert games.")],
 [("When was the Science paper published?", "7 December 2018."), ("Which games in the first paper?", "Chess, shogi and Go."), ("What are p and v?", "Move probabilities and the expected outcome."),
  ("Was the code released?", "No, the program was not released.")],
 [ORDER("The AlphaZero loop", "Put the steps in order.", ["Play a game with network-guided tree search", "Record each position with its search probabilities", "Score the finished game as win, draw or loss", "Train the network on the recorded data", "Play again with the improved network"]),
  MATCH("Programs", "Match each program with its description.", [("AlphaGo Lee", "Beat Lee Sedol in 2016"), ("AlphaGo Zero", "Go from self-play only"), ("AlphaZero", "One algorithm for chess, shogi and Go"), ("Stockfish", "Alpha-beta chess engine"), ("Elmo", "Shogi champion program")]),
  FILL("Basics", "AlphaZero learns {{tabula rasa|from scratch}} using only the game {{rules}}. A network gives move probabilities and a {{value}}. Games against itself are called {{self-play}}.")]))

# ------------------------------------------------------------ 2
CHS.append(CH(
 "Games, search and classical engines",
 ("Game trees", [
  "Game | has | States and legal moves",
  "Zero-sum game | gives | Opposite payoffs",
  "Game tree | lists | All move sequences",
  "Minimax | assumes | Best play by both",
  "Negamax | is | Minimax with sign flip",
  "Alpha-beta | prunes | Hopeless branches",
  "Evaluation function | scores | Non-terminal positions"]),
 ["The games AlphaZero plays are two-player, zero-sum, perfect-information games: players alternate, one's gain is the other's loss, and nothing is hidden. They can be drawn as a game tree whose root is the current position and whose edges are legal moves.",
  "Minimax searches the tree assuming both sides play best. Negamax is the same idea written with one function by flipping the sign at each level. Alpha-beta pruning skips branches that cannot change the result.",
  "Full trees are far too big for chess, so classical engines search to a limited depth and score the leaves with a handwritten evaluation function. Replacing that function with a learned one is the main idea AlphaZero builds on."],
 [("State", "A complete description of the game position, including whose turn it is."),
  ("Zero-sum", "One player's win is exactly the other's loss."),
  ("Game tree", "A tree of positions connected by legal moves."),
  ("Minimax", "Choose the move that is best assuming the opponent also plays best."),
  ("Negamax", "Minimax written as value(s) = max over moves of minus value(child)."),
  ("Alpha-beta pruning", "Skip branches that cannot affect the final minimax value."),
  ("Evaluation function", "A heuristic that scores a position when the search stops early.")],
 ["Perfect-information two-player zero-sum games can be searched as trees.",
  "Negamax: value(s) = max over moves of -value(child); terminal win = +1 for the winner's side.",
  "Alpha-beta gives the same value as minimax with fewer nodes if moves are well ordered.",
  "Chess programs before AlphaZero used alpha-beta with handwritten evaluation and many tricks.",
  "Shogi is harder than chess: bigger board and captured pieces can be dropped back.",
  "Stockfish later adopted a small neural evaluation, so the contrast is no longer absolute."],
 [T("Before AlphaZero's own ideas, we need the vocabulary of game search. The papers apply to games with two players who alternate moves, where one player's win is the other's loss and the full position is visible to both. Chess, shogi and Go all fit. Poker, with hidden cards, does not."),
  T("A game tree has the current position at its root, one child for each legal move, and so on until positions where the game is over. Each finished position has a result, win, draw or loss. For tic-tac-toe the tree is small enough to search completely. For chess it is astronomically large."),
  T("Minimax gives each position a value, assuming that both players choose the best option. The player to move picks the child with the best value for themselves. Negamax is the compact way to write it, using the fact that the game is zero-sum: the value of a position for the player to move is the best, over all moves, of the negative of the child's value, because the child is seen from the opponent's side."),
  M(r"V(s) = \max_{a}\,\bigl(-V(s')\bigr), \qquad s' = \text{result of move } a \text{ in } s"),
  T("At a finished position the value is plus one if the player to move has won, minus one if they have lost and zero for a draw. In practice the player to move has always just been beaten when a game ends by a completed line, so the value there is minus one."),
  T("Alpha-beta pruning keeps two numbers, the best value already guaranteed to the player to move and to the opponent, and stops looking at a branch once it cannot matter. The result is exactly the minimax value, but far fewer nodes are visited when good moves are tried first. Chess engines add move-ordering rules, transposition tables, search extensions, opening books, endgame tablebases and many other devices."),
  T("Even so, nobody can search chess to the end. Engines stop at a depth and call an evaluation function, a formula written by humans from features such as material, king safety and pawn structure. The AlphaZero paper describes Stockfish this way, and notes that other strong programs, including Deep Blue, use very similar architectures. Stockfish itself later added a small neural network evaluation, so today's classical engines blur the line; the 2017 contrast was between handwritten and learned knowledge."),
  T("Shogi, Japanese chess, is harder for such methods than chess: it is played on a larger board, and a captured piece changes sides and may be dropped almost anywhere. Go, with its large branching factor and hard-to-score positions, resisted classical search for even longer. The question AlphaZero asks is whether one method can handle all three without handwritten knowledge."),
  T("The practice section implements the fundamentals on tic-tac-toe: detect a winner, compute negamax values, and count how many nodes minimax and alpha-beta visit. Boards are strings of nine characters, X, O or a dot for empty, read row by row.")],
 [("Which kind of game fits AlphaZero's setting?", ["Poker", "Chess", "Hidden-information games", "One-player puzzles only"], 1, "Perfect-information two-player zero-sum games."),
  ("What does negamax return at a position?", ["The best value for the player to move", "The number of moves", "The loser", "Zero always"], 0, "It flips the sign for the opponent's view."),
  ("What does alpha-beta pruning change?", ["The minimax value", "How many nodes are examined", "The rules", "The evaluation"], 1, "The value is the same, with fewer nodes."),
  ("What did classical chess engines use at depth limits?", ["A handwritten evaluation function", "A neural network", "Random play", "Human games"], 0, "They scored leaves with expert-designed formulas.")],
 [("What is a zero-sum game?", "One player's gain is the other's loss."), ("What is a leaf?", "A position where the search stops."), ("Why is shogi harder than chess?", "Larger board and drops."),
  ("What does alpha-beta need to be effective?", "Good move ordering.")],
 [PL("Who has won?", "A board is a string of nine characters 'X', 'O' or '.', read row by row. Write winner(board): return 'X' or 'O' if that player has three in a row, 'D' if the board is full with no line, and '.' if the game is still going.",
     "winner(board)", """
def winner(board):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in lines:
        if board[a] != '.' and board[a] == board[b] and board[b] == board[c]:
            return board[a]
    if '.' not in board:
        return 'D'
    return '.'
""", [["XXXOO...."], ["XOXOXOOXO"], ["XOXXOOOXX"], ["X...O...."], ["OOO.XX.X."], ["........."]], "Check the eight lines, then whether any square is empty."),
  PL("Negamax", "Write negamax(board, player): the game value for the player to move, assuming best play by both: +1 if they can force a win, 0 for a draw, -1 if they lose. If the game is already over, a finished line belongs to the other player, so return -1 when the winner is not player, +1 when it is, and 0 for a draw. player is 'X' or 'O'.",
     "negamax(board, player)", """
def negamax(board, player):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    def result(b):
        for x, y, z in lines:
            if b[x] != '.' and b[x] == b[y] and b[y] == b[z]:
                return b[x]
        if '.' not in b:
            return 'D'
        return '.'
    r = result(board)
    if r == 'D':
        return 0
    if r != '.':
        if r == player:
            return 1
        return -1
    other = 'O'
    if player == 'O':
        other = 'X'
    best = -2
    for i in range(9):
        if board[i] == '.':
            v = -negamax(board[:i] + player + board[i + 1:], other)
            if v > best:
                best = v
    return best
""", [["XX.OO....", "X"], ["XO.XO....", "X"], ["XO.XO....", "O"], ["XOXOXO...", "X"], ["XXOOO.X..", "X"], ["XOXOOXXXO", "X"]], "Recurse on every empty square and negate the child's value."),
  PL("How much does pruning save?", "Write node_counts(board, player): return [plain, pruned]. plain is the number of positions visited (including the starting one) by negamax that tries every empty square in index order. pruned is the number visited by alpha-beta negamax (window starting at -2 and 2, same move order, cut off when alpha reaches beta). A position with a finished game counts as visited but is not expanded.",
     "node_counts(board, player)", """
def node_counts(board, player):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    def result(b):
        for x, y, z in lines:
            if b[x] != '.' and b[x] == b[y] and b[y] == b[z]:
                return b[x]
        if '.' not in b:
            return 'D'
        return '.'
    def flip(p):
        if p == 'X':
            return 'O'
        return 'X'
    def plain(b, p):
        if result(b) != '.':
            return 1
        n = 1
        for i in range(9):
            if b[i] == '.':
                n += plain(b[:i] + p + b[i + 1:], flip(p))
        return n
    count = [0]
    def ab(b, p, alpha, beta):
        count[0] += 1
        r = result(b)
        if r == 'D':
            return 0
        if r != '.':
            if r == p:
                return 1
            return -1
        best = -2
        for i in range(9):
            if b[i] == '.':
                v = -ab(b[:i] + p + b[i + 1:], flip(p), -beta, -alpha)
                if v > best:
                    best = v
                if best > alpha:
                    alpha = best
                if alpha >= beta:
                    break
        return best
    ab(board, player, -2, 2)
    return [plain(board, player), count[0]]
""", [["XO.XO....", "X"], ["XX.OO....", "X"], ["XOXOXO...", "X"], ["XOXOX.O..", "O"], ["XOXXOOOX.", "X"]], "Write two recursive functions; in the pruned one pass (-beta, -alpha) down and keep alpha updated."),
  ORDER("Negamax step", "Order the steps for one position.", ["Check whether the game is over", "If not, list every legal move", "Search each resulting position from the opponent's side", "Negate each child's value", "Return the best of these values"]),
  FILL("Search", "In a {{zero-sum|zero sum}} game, one player's gain is the other's loss. Negamax flips the {{sign}} at each level. Alpha-beta {{pruning|prunes}} branches that cannot change the result.")]))

# ------------------------------------------------------------ 3
CHS.append(CH(
 "Monte Carlo tree search",
 ("Search by sampling", [
  "MCTS | builds | Search tree incrementally",
  "Selection | descends | From root to leaf",
  "Expansion | adds | New node",
  "Simulation | plays out | A game to the end",
  "Backup | updates | Visit counts and values",
  "UCB1 | balances | Exploration and exploitation",
  "Bandit problem | inspires | Selection rule"]),
 ["Monte Carlo tree search grows a tree one simulation at a time. Each simulation walks down the tree choosing promising moves, adds a new node, evaluates it and passes the result back up. Over many simulations the statistics at the root point to the best move.",
  "The classic choice rule comes from multi-armed bandits: try moves with a high average reward, but also moves tried rarely. UCB1 adds an exploration bonus that shrinks as a move is visited more.",
  "Classic MCTS evaluates a new node by playing random moves to the end of the game. AlphaZero keeps the same four phases but replaces the random rollout with the network's value."],
 [("Simulation", "One pass of the search: select down the tree, expand, evaluate, back up."),
  ("Rollout", "Playing a game to the end, often with random moves, to estimate a position's value."),
  ("Exploitation", "Choosing the move that looks best so far."),
  ("Exploration", "Trying moves with little data in case they are better."),
  ("UCB1", "Upper confidence bound rule: mean reward plus a bonus that falls with visits."),
  ("Multi-armed bandit", "Repeated choice among options with unknown payoffs, balancing learning and earning."),
  ("UCT", "UCB applied to trees of moves, from Kocsis and Szepesvári.")],
 ["Four phases: selection, expansion, evaluation (or simulation), backup.",
  "Each node stores visit counts and a mean value.",
  "UCB1 score: mean + c * sqrt(ln(parent visits) / visits).",
  "Unvisited moves are tried first.",
  "Classic MCTS uses random rollouts; AlphaZero uses a learned value instead.",
  "The root's visit counts are the output of the search."],
 [T("Alpha-beta search looks at every move to a fixed depth. Monte Carlo tree search instead grows a tree unevenly, spending most effort on promising lines. It needs no handwritten evaluation, only the rules, which is why it suited Go, where good evaluation functions were hard to write."),
  T("Each node of the tree is a position, and each edge a move. For every edge we keep a visit count and a total value. One simulation has four phases. Selection: starting at the root, repeatedly choose a child by a rule until reaching a position not yet in the tree. Expansion: add that position. Evaluation: estimate how good it is. Backup: walk back up the path and update the counts and values of every edge used."),
  T("The question is how to choose in selection. This is the multi-armed bandit problem: several slot machines with unknown payoffs. You want to pull the best one, but you only learn about each by pulling it. Pure greed can get stuck on a mediocre option that happened to pay early. Pure exploration wastes pulls."),
  M(r"\mathrm{UCB1}(a) = \frac{W_a}{N_a} + c\,\sqrt{\frac{\ln N}{N_a}}"),
  T("The UCB1 rule picks the option with the highest score. W over N is the average reward so far of option a, which favours good options. The second term is a bonus that is large for options with few visits and shrinks as they are tried, which favours exploring. N is the total number of pulls and c sets how adventurous the search is. Applied to the edges at each tree node this gives the UCT algorithm, due to Kocsis and Szepesvári."),
  T("Classic MCTS evaluates a newly added position by a rollout: play random moves to the end and note who won. One rollout is a noisy estimate, but averaged over thousands it is informative. Go programs built on this approach reached strong amateur level before neural networks."),
  T("The final move is chosen from the root's statistics. Usually the most visited move is chosen, not the one with the best average, because visit counts are more robust. A move with a great average after two visits is probably luck."),
  T("What AlphaZero changes: the rollout is replaced by the network's value estimate, and the UCB rule is replaced by a variant that also uses the network's move probabilities as a prior. The structure of four phases stays the same. Chapter 5 gives the exact rule."),
  T("In the practice section you compute the UCB1 score and write the selection step.")],
 [("What are the four phases of an MCTS simulation?", ["Selection, expansion, evaluation, backup", "Train, test, deploy, repeat", "Shuffle, deal, bid, play", "Read, write, run, halt"], 0, "Walk down, add, evaluate, update."),
  ("Why does UCB1 add a bonus term?", ["To favour rarely tried moves", "To slow the search", "To remove randomness", "To count wins"], 0, "It encourages exploration."),
  ("What does classic MCTS do to evaluate a new node?", ["A rollout with random moves", "A neural network", "A database lookup", "Nothing"], 0, "AlphaZero replaces this with a learned value."),
  ("What is usually used to pick the final move?", ["The root visit counts", "The deepest line", "A coin flip", "The last move tried"], 0, "Visit counts are robust.")],
 [("What is c in UCB1?", "The exploration constant."), ("Who introduced UCT?", "Kocsis and Szepesvári."), ("Why rollouts?", "To estimate value without handwritten knowledge."),
  ("What does AlphaZero replace rollouts with?", "The network's value output.")],
 [PL("UCB1 score", "Write ucb1(total, n, parent_n, c): total / n + c * sqrt(ln(parent_n) / n). For an option never tried (n = 0) return 1000000000.0 so it is chosen first. Use math.sqrt and math.log.",
     "ucb1(total, n, parent_n, c)", """
import math
def ucb1(total, n, parent_n, c):
    if n == 0:
        return 1000000000.0
    return total / n + c * math.sqrt(math.log(parent_n) / n)
""", [[3, 5, 20, 1.4], [0, 0, 20, 1.4], [10, 10, 100, 1.0], [1, 1, 3, 2.0]], "Handle n = 0 first; otherwise apply the formula.", 1e-9),
  PL("UCB selection", "Each option is [total, n]. The parent count is the sum of all n. Write select_ucb(stats, c): the index of an untried option if there is one (the lowest index), otherwise the index with the highest UCB1 score (the lowest index on ties).",
     "select_ucb(stats, c)", """
import math
def select_ucb(stats, c):
    parent = 0
    for s in stats:
        parent += s[1]
    for i in range(len(stats)):
        if stats[i][1] == 0:
            return i
    best = -1
    bestscore = None
    for i in range(len(stats)):
        score = stats[i][0] / stats[i][1] + c * math.sqrt(math.log(parent) / stats[i][1])
        if bestscore is None or score > bestscore:
            bestscore = score
            best = i
    return best
""", [[[[3, 5], [2, 2], [0, 1]], 1.4], [[[3, 5], [2, 2], [0, 0]], 1.4], [[[30, 50], [1, 2]], 0.1], [[[30, 50], [1, 2]], 3.0], [[[1, 2], [1, 2]], 1.0]], "Return the first untried index; else track the best score with a strict comparison."),
  ORDER("One simulation", "Put the phases of one MCTS simulation in order.", ["Select moves from the root down the tree", "Expand a new position", "Evaluate it", "Back up the value along the path"]),
  MATCH("MCTS terms", "Match each term with its meaning.", [("Selection", "Walk down using a rule"), ("Expansion", "Add a new node"), ("Rollout", "Random play to the end"), ("Backup", "Update stats along the path"), ("UCB1", "Mean plus exploration bonus")]),
  FILL("MCTS", "UCB1 adds an {{exploration}} bonus to the mean value. The final move is chosen from the root {{visit}} counts. AlphaZero replaces rollouts with the network's {{value}}.")]))

# ------------------------------------------------------------ 4
CHS.append(CH(
 "The policy and value network",
 ("The function f", [
  "Network f | maps | Position to policy and value",
  "Policy head | outputs | Move probabilities",
  "Value head | outputs | Expected outcome",
  "Softmax | turns | Scores into probabilities",
  "Legal move mask | removes | Illegal moves",
  "Chess | uses | 8 by 8 by 73 move planes",
  "Residual blocks | form | Network body"]),
 ["AlphaZero's network takes a board position and returns two things: a probability for every possible move (the policy) and one number estimating the outcome (the value). One shared body of convolutional layers feeds two output heads.",
  "The policy is produced with a softmax over all moves, then illegal moves are zeroed out and the rest renormalized. For chess, moves are encoded as 73 planes of 8 by 8 squares: for each from-square, 56 queen-style moves, 8 knight moves and 9 underpromotions.",
  "Early in training the network knows nothing, so p is nearly uniform and v is near zero. Everything it later knows comes from self-play."],
 [("Policy", "A probability for each move, written p."),
  ("Value", "A number v between -1 and +1: expected outcome for the player to move."),
  ("Softmax", "A function that turns any list of scores into positive numbers summing to 1."),
  ("Legal-move mask", "Setting the probability of illegal moves to zero and renormalizing."),
  ("Residual block", "A group of convolutional layers with a skip connection; AlphaGo Zero and AlphaZero stack many."),
  ("Plane", "One 8 by 8 layer of the input or the output."),
  ("Input planes", "Layers describing the position, such as piece locations, history and castling rights.")],
 ["(p, v) = f_theta(s).",
  "Softmax: p_i = exp(x_i) / sum_j exp(x_j).",
  "Illegal moves are masked out and the policy renormalized.",
  "Chess input: 119 planes of 8x8 (8 steps of piece history plus constant planes).",
  "Chess output: 8 x 8 x 73 = 4,672 move slots.",
  "Value target z is -1 for a loss, 0 for a draw, +1 for a win."],
 [T("The learned part of AlphaZero is a single neural network f with parameters theta. It takes a position and returns a pair: a vector p giving a probability for each move, and a scalar v estimating the expected outcome. The papers describe the body as many residual blocks of convolutional layers with batch normalization and rectifier non-linearities, followed by two small output heads."),
  T("The value v is a number between minus one and plus one, from the point of view of the player to move. A value near plus one means a likely win, near minus one a likely loss. Unlike AlphaGo Zero, which assumed only win or loss, AlphaZero estimates the expected outcome, which also covers draws, an important thing in chess where most top games are drawn."),
  T("Turning scores into a policy. The last layer of the policy head produces one raw score per possible move. A softmax makes them positive and sums them to one. It subtracts the largest score first for numerical stability, which does not change the result."),
  M(r"p_i = \frac{e^{x_i}}{\sum_j e^{x_j}}"),
  T("Most possible moves are illegal in any given position. So the policy is masked: probabilities of illegal moves are set to zero and the remainder renormalized to sum to one. If every legal move happens to have zero probability, a sensible fallback is to spread probability evenly over the legal moves."),
  T("Representing chess. The paper's input is a stack of 8 by 8 planes. It holds piece positions for each side over the last eight positions, plus constant planes for the side to move, the move count, castling rights and the no-progress counter, 119 planes in total. The output is 8 by 8 by 73. Each square of the grid marks the square a piece moves from, and the 73 planes say how it moves."),
  T("Of the 73 planes, 56 are queen-style moves: eight compass directions times seven distances. Eight are knight moves. Nine are underpromotions, a pawn moving or capturing to a knight, bishop or rook. That gives 8 times 8 times 73, which is 4,672 move slots. Promotions to a queen are encoded as ordinary queen-style moves."),
  T("For shogi and Go the encodings differ, but the principle is the same: the game rules supply the board and a fixed catalogue of moves, and the network learns everything else. This is why the algorithm is general: only the encoding of positions and moves is game-specific."),
  T("In the practice section you implement the softmax, the legal-move mask, and the queen-move plane numbering. The compass order used in the lab is my own convention; the paper does not fix an order in its text.")],
 [("What does the value output estimate?", ["The best move", "The expected game outcome", "The number of moves left", "The board size"], 1, "From the viewpoint of the player to move."),
  ("What does a softmax do?", ["Sorts scores", "Turns scores into probabilities", "Removes illegal moves", "Doubles the score"], 1, "Positive numbers that sum to 1."),
  ("How many move slots does AlphaZero's chess output have?", ["64", "73", "4,672", "119"], 2, "8 x 8 x 73."),
  ("What happens to illegal moves?", ["They are rewarded", "They get zero probability and the rest is renormalized", "They are ignored by the board", "They are repeated"], 1, "A legal-move mask.")],
 [("What is the head?", "An output branch of the network."), ("How many queen-style planes?", "56 (8 directions x 7 distances)."), ("What is z?", "The final outcome: -1, 0 or +1."),
  ("Why 119 input planes?", "Eight steps of piece history plus constant planes.")],
 [PL("Softmax", "Write softmax(xs): subtract the maximum score from every score, exponentiate each (math.exp), and divide by the total. Return the list of probabilities.",
     "softmax(xs)", """
import math
def softmax(xs):
    m = max(xs)
    exps = []
    for x in xs:
        exps.append(math.exp(x - m))
    total = 0.0
    for e in exps:
        total += e
    out = []
    for e in exps:
        out.append(e / total)
    return out
""", [[[0.0, 0.0]], [[1.0, 2.0, 3.0]], [[1000.0, 1001.0]], [[-1.0, 0.0, 1.0, 2.0]]], "Subtract the max first so large scores do not overflow.", 1e-9),
  PL("Mask illegal moves", "Write mask_normalize(p, legal): keep p[i] for the indices in the list legal, set all others to 0, and divide by the new total so it sums to 1. If the total is 0, give every legal move probability 1 / len(legal).",
     "mask_normalize(p, legal)", """
def mask_normalize(p, legal):
    q = []
    total = 0.0
    for i in range(len(p)):
        if i in legal:
            q.append(p[i])
            total += p[i]
        else:
            q.append(0.0)
    out = []
    for i in range(len(p)):
        if total == 0:
            if i in legal:
                out.append(1.0 / len(legal))
            else:
                out.append(0.0)
        else:
            out.append(q[i] / total)
    return out
""", [[[0.5, 0.3, 0.2], [0, 2]], [[0.25, 0.25, 0.25, 0.25], [1]], [[0.0, 0.0, 1.0], [0, 1]], [[0.1, 0.2, 0.3, 0.4], [0, 1, 2, 3]]], "First zero the illegal entries, then divide by the sum of what remains.", 1e-9),
  PL("Queen-move plane", "In AlphaZero's chess encoding, 56 planes hold queen-style moves. Use this convention: directions are numbered 0 to 7 in the order N (-1,0), NE (-1,+1), E (0,+1), SE (+1,+1), S (+1,0), SW (+1,-1), W (0,-1), NW (-1,-1), written as (row change, column change), and distances run 1 to 7. Write queen_move_plane(dr, dc): the plane number direction * 7 + (distance - 1), or -1 if (dr, dc) is not a straight or diagonal move of distance 1 to 7.",
     "queen_move_plane(dr, dc)", """
def queen_move_plane(dr, dc):
    if dr == 0 and dc == 0:
        return -1
    if dr != 0 and dc != 0 and abs(dr) != abs(dc):
        return -1
    dist = max(abs(dr), abs(dc))
    if dist > 7:
        return -1
    sr = 0
    if dr > 0:
        sr = 1
    elif dr < 0:
        sr = -1
    sc = 0
    if dc > 0:
        sc = 1
    elif dc < 0:
        sc = -1
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    for k in range(8):
        if dirs[k][0] == sr and dirs[k][1] == sc:
            return k * 7 + dist - 1
    return -1
""", [[-1, 0], [0, 3], [2, 2], [-7, 7], [1, 2], [0, 0], [0, -7], [-3, -3], [8, 0]], "Find the unit direction, the distance, then look up the direction number."),
  MATCH("Network outputs", "Match each item with its meaning.", [("p", "Move probabilities"), ("v", "Expected outcome"), ("Softmax", "Scores to probabilities"), ("Mask", "Zero for illegal moves"), ("73 planes", "Move types per from-square in chess")]),
  FILL("Network", "The chess output has 8 x 8 x {{73}} = 4,672 move slots. The value is between -1 and {{+1|1|plus one}}. A {{softmax}} turns scores into probabilities.")]))
