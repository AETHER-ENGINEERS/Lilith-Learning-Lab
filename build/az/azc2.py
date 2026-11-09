"""AlphaZero course, chapters 5-8."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 5
CHS.append(CH(
 "MCTS guided by the network (PUCT)",
 ("AlphaZero's search", [
  "Edge | stores | N, W, Q and P",
  "Selection | maximizes | Q plus U",
  "U | grows with | Prior P",
  "U | shrinks with | Visits N",
  "Leaf | is evaluated by | Network",
  "Backup | flips | Sign each level",
  "Root visits | give | Move probabilities"]),
 ["Each edge of the search tree stores a visit count N, a total value W, a mean value Q equal to W over N, and a prior probability P from the network. Selection picks the edge with the largest Q plus U, where U is an exploration bonus proportional to the prior and shrinking with visits.",
  "When a simulation reaches a leaf, the network evaluates it. Its policy becomes the priors of the new edges and its value is backed up along the path, with the sign flipped at every level since the players alternate. No random rollout is used.",
  "After many simulations the root visit counts form a probability distribution over moves. That distribution is the search's answer, and it is also the training target for the policy."],
 [("Edge statistics", "For each move from a position: visit count N, total value W, mean value Q = W/N, prior P."),
  ("PUCT", "Polynomial upper confidence trees: the selection rule Q + c * P * sqrt(sum N) / (1 + N)."),
  ("Prior", "The network's probability for a move, used to guide search before the move has been tried."),
  ("Leaf expansion", "Creating the edges for a new position, with priors from the network."),
  ("Backup", "Updating counts and values along the path from leaf to root."),
  ("Search policy", "The distribution over root moves given by visit counts.")],
 ["Selection: a = argmax over moves of Q(s,a) + U(s,a).",
  "U(s,a) = c * P(s,a) * sqrt(sum_b N(s,b)) / (1 + N(s,a)).",
  "Leaf: (p, v) = f(s); store p as priors, back up v.",
  "Backup: N += 1, W += v, Q = W / N, with the sign flipped at each level.",
  "In the AlphaZero pseudocode c is c_init + log((1 + N + c_base) / c_base), with c_init = 1.25 and c_base = 19652.",
  "Training used 800 simulations per move."],
 [T("Chapter 3 described MCTS with UCB1 and random rollouts. AlphaZero keeps the four phases but changes both ingredients. Let us look at the tree. For every position s in the tree and every legal move a, there is an edge storing four numbers: a visit count N, a total value W, a mean value Q equal to W divided by N, and a prior probability P that came from the network when the position was first expanded."),
  T("Selection. Starting at the root, each simulation picks, at every position, the edge that maximizes Q plus U. The exploration term U is proportional to the prior, grows with the total number of visits to the position, and shrinks as the edge itself is visited. This follows the AlphaGo Zero paper."),
  M(r"U(s,a) = c_{\mathrm{puct}}\; P(s,a)\;\frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)}"),
  T("Look at the behaviour. Early in the search all N are zero, so Q is taken as zero and moves are chosen by the prior alone: the network's favourites are tried first. As a move is visited its bonus falls, and moves with lower priors but good values start to win. Moves with high Q keep being visited. In the long run the visit counts concentrate on the best moves."),
  T("Expansion and evaluation. When the walk reaches a position that is not yet in the tree, the network is called once on it. It returns p and v. The vector p, masked to the legal moves, gives the priors of the new edges. The scalar v is the value of the position for the player to move. There is no rollout to the end of the game."),
  T("Backup, with a subtlety. Every edge's Q is from the point of view of the player who chooses that move. The value v belongs to the player to move at the leaf, who is the opponent of the player who chose the last edge. So the last edge receives minus v, the one above it plus v, and so on, alternating up to the root. Each edge on the path also gets N plus one."),
  T("The AlphaZero paper does not print the exploration formula in its main text, and the later pseudocode makes the constant depend on the visit count of the position: log of one plus N plus c_base over c_base, plus c_init, with c_init equal to 1.25 and c_base equal to 19652. The constant grows very slowly with visits. The papers give no experiments on this choice, and the reason for modifying the formula was not discussed. The version in the lab is the simple AlphaGo Zero form."),
  T("Choosing the move. After the simulations, the search returns a probability distribution based on root visit counts. In training, moves are chosen in proportion to those counts. In evaluation, the program picks the most-visited move. During training each search used 800 simulations."),
  T("Cost and speed. The papers report AlphaZero searching about 80 thousand positions per second in chess, 40 thousand in shogi and 16 thousand in Go. Stockfish searched about 70 million per second, and the shogi program Elmo about 35 million. AlphaZero examines roughly a thousand times fewer positions, but each is judged by a much better evaluator. In the practice section you will implement the score, the selection and the backup.")],
 [("Which statistics does each edge store?", ["N, W, Q and P", "Only N", "Only a win flag", "The whole board"], 0, "Visit count, total value, mean value and prior."),
  ("What replaces the rollout in AlphaZero's MCTS?", ["Random play", "The network's value output", "A database", "Alpha-beta"], 1, "The leaf is evaluated by f."),
  ("Why is the value negated going up the tree?", ["To confuse the search", "The players alternate, so one's gain is the other's loss", "Values are always negative", "It saves memory"], 1, "Each edge is scored from its mover's view."),
  ("How does U change as N(s,a) grows?", ["It grows", "It shrinks", "It stays", "It becomes the prior"], 1, "The exploration bonus decays with visits.")],
 [("What is c_init?", "1.25 in the AlphaZero pseudocode."), ("What is c_base?", "19652 in the pseudocode."), ("How many simulations per move in training?", "800."),
  ("What does the search return?", "A distribution from root visit counts.")],
 [PL("PUCT score", "Write puct_score(q, p, n_a, n_parent, c): q + c * p * sqrt(n_parent) / (1 + n_a), where n_parent is the total visits to the position.",
     "puct_score(q, p, n_a, n_parent, c)", """
import math
def puct_score(q, p, n_a, n_parent, c):
    return q + c * p * math.sqrt(n_parent) / (1 + n_a)
""", [[0.0, 0.5, 0, 0, 1.5], [0.2, 0.5, 3, 10, 1.5], [-0.1, 0.1, 20, 100, 2.0], [0.5, 0.0, 5, 50, 1.0]], "Direct from the formula.", 1e-9),
  PL("Select an edge", "The position has three lists: Q (mean values), P (priors) and N (visit counts), one entry per move. Write puct_select(Q, P, N, c): the index of the move with the highest PUCT score, taking n_parent as the sum of N. On equal scores choose the lowest index.",
     "puct_select(Q, P, N, c)", """
import math
def puct_select(Q, P, N, c):
    total = 0
    for n in N:
        total += n
    best = -1
    bestscore = None
    for i in range(len(Q)):
        score = Q[i] + c * P[i] * math.sqrt(total) / (1 + N[i])
        if bestscore is None or score > bestscore:
            bestscore = score
            best = i
    return best
""", [[[0, 0, 0], [0.2, 0.5, 0.3], [0, 0, 0], 1.5], [[0.1, 0.4, 0.0], [0.5, 0.3, 0.2], [10, 4, 1], 1.5], [[0.9, 0.0], [0.1, 0.9], [50, 0], 1.0], [[0.0, 0.0], [0.5, 0.5], [3, 3], 2.0]], "Compute each score and keep the first strict maximum."),
  PL("Visit-dependent constant", "In the AlphaZero pseudocode the constant grows with the number of visits n to the position: c(n) = ln((1 + n + c_base) / c_base) + c_init. Write c_dynamic(n, c_init, c_base) using math.log.",
     "c_dynamic(n, c_init, c_base)", """
import math
def c_dynamic(n, c_init, c_base):
    return math.log((1 + n + c_base) / c_base) + c_init
""", [[0, 1.25, 19652], [800, 1.25, 19652], [100000, 1.25, 19652], [0, 1.5, 100]], "Plug in the formula.", 1e-9),
  PL("Back up a value", "stats is a list of [N, W] pairs, one per edge. path lists the edge indices from the root down to the last edge, and v is the leaf's value for the player to move at the leaf. Write backup(stats, path, v): the last edge gets W += -v, the one above it W += +v, alternating, and every edge on the path gets N += 1. Return the new stats.",
     "backup(stats, path, v)", """
def backup(stats, path, v):
    out = []
    for s in stats:
        out.append([s[0], s[1]])
    sign = -1.0
    for k in range(len(path) - 1, -1, -1):
        e = path[k]
        out[e][0] += 1
        out[e][1] += sign * v
        sign = -sign
    return out
""", [[[[0, 0.0], [0, 0.0], [0, 0.0]], [0, 2], 0.5], [[[1, 0.25], [0, 0.0]], [0], -1.0], [[[0, 0.0], [0, 0.0], [0, 0.0], [0, 0.0]], [3, 1, 0], 1.0], [[[2, 1.0]], [], 0.7]], "Walk the path from the end; start with -v and flip the sign at each step.", 1e-9),
  ORDER("Selection walk", "Put the steps of one simulation in order.", ["Start at the root", "Pick the edge with the highest Q plus U", "Repeat until reaching a position not yet in the tree", "Evaluate that position with the network", "Back up the value, flipping the sign each level"]),
  FILL("PUCT", "The exploration bonus is proportional to the {{prior}} and shrinks with {{visits|visit counts}}. The value is {{negated|flipped}} at each level because the players alternate. Training used {{800}} simulations.")]))

# ------------------------------------------------------------ 6
CHS.append(CH(
 "Exploration: noise and temperature",
 ("Making self-play diverse", [
  "Self-play | needs | Exploration",
  "Dirichlet noise | is added to | Root priors",
  "Noise scale | follows | Typical legal moves",
  "Temperature | shapes | Move choice",
  "Early moves | are sampled | In proportion to visits",
  "Late moves | are chosen | Greedily",
  "Search inside tree | ignores | Temperature"]),
 ["If a program always plays its single best move, it may play the same game forever and learn nothing new. AlphaZero adds randomness in two places: noise on the root priors, and sampling the played move from the visit counts.",
  "The Dirichlet noise mixes a random probability vector into the network's priors at the root. Its concentration is scaled inversely to the typical number of legal moves: 0.3 for chess, 0.15 for shogi, 0.03 for Go. This was the only game-specific hyperparameter.",
  "Temperature controls how sharply the visit counts are turned into move probabilities. At temperature one, moves are chosen in proportion to visits. As it approaches zero, the most-visited move is always chosen."],
 [("Dirichlet noise", "A random probability vector added to the root priors to force some exploration."),
  ("Concentration alpha", "A Dirichlet parameter; small values give spiky vectors favouring a few moves."),
  ("Epsilon", "The mixing weight of the noise; 0.25 in AlphaGo Zero."),
  ("Temperature tau", "Exponent 1/tau applied to visit counts before normalizing."),
  ("Greedy play", "Always choosing the move with the most visits."),
  ("Sampling", "Choosing a move at random according to a probability distribution.")],
 ["Root prior with noise: P = (1 - eps) * p + eps * eta, eta ~ Dirichlet(alpha).",
  "alpha is 0.3 (chess), 0.15 (shogi), 0.03 (Go): inversely related to move counts.",
  "Move choice: pi(a) proportional to N(a)^(1/tau).",
  "AlphaGo Zero: tau = 1 for the first 30 moves of a game, then tau near 0.",
  "In evaluation matches the most-visited move is played.",
  "Noise and temperature affect the move played, not the learning rule."],
 [T("Self-play only teaches the program something if the games vary. A program that always plays its best-looking move, from the same start, would repeat one game. So AlphaZero deliberately injects randomness, in two places."),
  T("The first place is the root of each search. Dirichlet noise is added to the network's prior probabilities at the root, so moves the network currently dislikes still get tried. The mix is a weighted average of the network's prior and a random vector eta drawn from a Dirichlet distribution. AlphaGo Zero used epsilon equal to 0.25; the AlphaZero paper does not state epsilon in its main text."),
  M(r"P(s_{\mathrm{root}}, a) = (1-\varepsilon)\, p_a + \varepsilon\, \eta_a, \qquad \eta \sim \mathrm{Dir}(\alpha)"),
  T("What the Dirichlet distribution does. It produces random vectors of non-negative numbers summing to one. With a small concentration alpha the vectors are spiky: most mass sits on a few moves, chosen at random. That is what you want, since a good surprise is usually one specific alternative, not a faint boost for everything. The AlphaZero paper scales alpha inversely to the typical number of legal moves: 0.3 for chess, 0.15 for shogi and 0.03 for Go. Go has the most legal moves and gets the smallest alpha."),
  T("The second place is the move actually played. After the search, the root visit counts N are turned into a distribution with a temperature tau. The probability of a move is proportional to its visit count raised to the power one over tau. At tau equal to one this is plain proportion to visits. As tau goes toward zero the largest count takes everything, so the most-visited move is chosen."),
  M(r"\pi(a) = \frac{N(a)^{1/\tau}}{\sum_b N(b)^{1/\tau}}"),
  T("AlphaGo Zero used tau equal to one for the first 30 moves of each game, so openings vary, and then almost zero, so later play is sharp. The AlphaZero paper describes moves chosen in proportion to root visit counts during training and greedily in evaluation, without printing a temperature schedule in its main text. Both settings are therefore described here as AlphaGo Zero's."),
  T("Two clarifications. First, the temperature affects only which real move is played in the game. Inside a search, the tree is still walked by the PUCT rule. Second, the training target for the policy is the visit distribution, not the move that was played, so the occasional exploratory move does not teach the network to play badly."),
  T("In the practice section you turn visit counts into a policy at a given temperature, mix noise into priors, set the schedule, and sample from a distribution given a random number.")],
 [("What is Dirichlet noise added to?", ["The board", "The root priors", "The reward", "The weights"], 1, "It forces extra exploration at the root."),
  ("Which game gets the smallest alpha?", ["Chess", "Shogi", "Go", "All the same"], 2, "Go has the most legal moves."),
  ("What does tau close to zero do?", ["Plays proportional to visits", "Always plays the most visited move", "Plays at random", "Passes"], 1, "N^(1/tau) concentrates on the maximum."),
  ("Does the temperature change how the tree is searched?", ["Yes, everywhere", "No, only the move played", "Only at leaves", "Only at the root's children"], 1, "Inside the search PUCT is used.")],
 [("What is eps in AlphaGo Zero?", "0.25."), ("Temperature rule in AlphaGo Zero?", "tau = 1 for the first 30 moves, then near 0."), ("What is the policy training target?", "The search visit distribution."),
  ("Why spiky noise?", "To try specific alternative moves.")],
 [PL("Visits to policy", "Write visits_to_policy(N, tau): if tau is 0, return a list with 1.0 at the first index of the largest count and 0.0 elsewhere. Otherwise raise each count to the power 1 / tau and divide by the total. The counts are not all zero.",
     "visits_to_policy(N, tau)", """
def visits_to_policy(N, tau):
    if tau == 0:
        best = 0
        for i in range(len(N)):
            if N[i] > N[best]:
                best = i
        out = [0.0] * len(N)
        out[best] = 1.0
        return out
    w = []
    total = 0.0
    for n in N:
        x = n ** (1.0 / tau)
        w.append(x)
        total += x
    out = []
    for x in w:
        out.append(x / total)
    return out
""", [[[1, 2, 3, 4], 1.0], [[1, 2, 3, 4], 0], [[10, 30, 60], 0.5], [[10, 30, 60], 2.0], [[5, 5, 0], 1.0], [[0, 7, 7], 0]], "tau = 0 is the argmax special case; otherwise normalize N ** (1/tau).", 1e-9),
  PL("Mix in noise", "Write mix_noise(p, noise, eps): the list (1 - eps) * p[i] + eps * noise[i].",
     "mix_noise(p, noise, eps)", """
def mix_noise(p, noise, eps):
    out = []
    for i in range(len(p)):
        out.append((1 - eps) * p[i] + eps * noise[i])
    return out
""", [[[0.5, 0.3, 0.2], [0.0, 1.0, 0.0], 0.25], [[1.0, 0.0], [0.5, 0.5], 0.0], [[1.0, 0.0], [0.5, 0.5], 1.0]], "A weighted average of two vectors.", 1e-9),
  PL("Temperature schedule", "Write temperature_for_move(move_number, threshold): 1.0 if move_number (counting from 1) is at most threshold, otherwise 0.0.",
     "temperature_for_move(move_number, threshold)", """
def temperature_for_move(move_number, threshold):
    if move_number <= threshold:
        return 1.0
    return 0.0
""", [[1, 30], [30, 30], [31, 30], [5, 0]], "A simple threshold."),
  PL("Sample a move", "Sampling from a distribution can be done with one uniform random number u in [0, 1). Write sample_index(pi, u): the first index whose running total of probabilities is greater than u (if rounding leaves none, return the last index whose probability is above 0).",
     "sample_index(pi, u)", """
def sample_index(pi, u):
    total = 0.0
    last = 0
    for i in range(len(pi)):
        if pi[i] > 0:
            last = i
        total += pi[i]
        if total > u:
            return i
    return last
""", [[[0.2, 0.5, 0.3], 0.0], [[0.2, 0.5, 0.3], 0.19], [[0.2, 0.5, 0.3], 0.2], [[0.2, 0.5, 0.3], 0.69], [[0.2, 0.5, 0.3], 0.71], [[0.0, 1.0, 0.0], 0.5]], "Accumulate the probabilities and stop when the total passes u."),
  MATCH("Exploration", "Match each device with its effect.", [("Dirichlet noise", "Extra root exploration"), ("Temperature 1", "Sample in proportion to visits"), ("Temperature near 0", "Play the most visited move"), ("Small alpha", "Spiky random vector"), ("Epsilon", "Mixing weight of the noise")]),
  FILL("Exploration", "Noise is added to the root {{priors|prior probabilities}}. The temperature turns {{visit}} counts into move probabilities. AlphaGo Zero used temperature 1 for the first {{30}} moves.")]))

# ------------------------------------------------------------ 7
CHS.append(CH(
 "Self-play and training data",
 ("What a game produces", [
  "Self-play game | produces | Position records",
  "Record | contains | State, pi and z",
  "pi | is | Search probabilities",
  "z | is | Final outcome",
  "z | is seen from | Player to move",
  "Symmetry augmentation | is used by | AlphaGo Zero",
  "AlphaZero | does not use | Augmentation"]),
 ["A self-play game gives one training example per position played: the position s, the search probabilities pi that were used to choose the move, and the final outcome z of the game. The outcome is the same game result, but seen from the side of whoever was to move in that position.",
  "So if the first player wins, z is plus one for every position where the first player was to move and minus one for the others. A draw gives zero for all.",
  "Go has eightfold symmetry, which AlphaGo Zero used to multiply its data. Chess and shogi are not symmetric, so AlphaZero does not augment its data or transform positions during search."],
 [("Training example", "A triple (s, pi, z): position, search probabilities and outcome."),
  ("Search probabilities pi", "The distribution over moves produced by MCTS at that position."),
  ("Outcome z", "-1, 0 or +1 from the point of view of the player to move."),
  ("Replay data", "Recent self-play games from which training batches are drawn."),
  ("Symmetry augmentation", "Using rotated and reflected copies of a position as extra examples."),
  ("Terminal position", "A position where the game is over and can be scored by the rules.")],
 ["Each position in a game yields (s_t, pi_t, z_t).",
  "z_t = +1 if the player to move at t eventually wins, -1 if loses, 0 for a draw.",
  "pi_t comes from the visit counts, not from the move actually played.",
  "Games end by the rules of the game; Go also ends after 722 moves.",
  "AlphaGo Zero used the symmetries of Go; AlphaZero does not augment data.",
  "Positions are drawn from recent games to train the network."],
 [T("What does a game of self-play teach? Each game is a sequence of positions s1, s2, up to a final position sT. At every position the program ran a search and played a move. After the game ends, the rules say who won. The program then writes one record for every position played."),
  T("A record has three parts. The position s_t, in the network's input encoding. The search probabilities pi_t, the distribution over moves produced by the tree search at that position. And the outcome z_t. The value z is plus one if the player to move at position t went on to win, minus one if they went on to lose, and zero for a draw."),
  M(r"z_t = \begin{cases} +1 & \text{player to move at } t \text{ wins} \\ 0 & \text{draw} \\ -1 & \text{player to move at } t \text{ loses} \end{cases}"),
  T("An example. Suppose a game lasts five moves and the first player wins. The first player moved at moves one, three and five; they get z equal to plus one for those positions. The second player moved at positions two and four, and gets minus one. Note that the same game result is seen from alternating sides, which matches the network's value being defined for the player to move."),
  T("Where the target pi comes from matters. It is the visit distribution from the search, not the move chosen. Because moves early in a game are sampled randomly in proportion to visits, the move played is a noisy sample, while pi is the search's whole opinion. Training the policy toward pi teaches the network to predict what a better search would conclude."),
  T("Where the game ends. The rules decide: checkmate, stalemate or other draws in chess, for example. AlphaGo Zero ended Go games when both players passed or after 19 times 19 times 2, which is 722, moves, and scored by Tromp-Taylor rules. In AlphaZero the outcome may be a draw, which matters for chess: it optimizes the expected outcome, not just the chance of winning."),
  T("Symmetry. Go positions have eight symmetries: four rotations, each with or without a reflection. AlphaGo Zero used these, for example by feeding the network a random transform of the board during training and search. The rules of chess and shogi are asymmetric, and so AlphaZero does not augment the training data and does not transform the board during MCTS."),
  T("Where the data goes. Self-play games are generated continuously by many workers; the training process samples mini-batches of positions from recent games. In the published AlphaZero runs, self-play used 5,000 first-generation TPUs while 64 second-generation TPUs trained the network."),
  T("In the practice section you build the outcome list for a game, form the training triples, and count the distinct symmetric copies of a tic-tac-toe board.")],
 [("What does a self-play record contain?", ["Only the winner", "State, search probabilities and outcome", "Only the moves", "The network weights"], 1, "(s, pi, z)."),
  ("From whose view is z defined?", ["Always the first player", "The player to move at that position", "The winner", "The loser"], 1, "So it matches the value head."),
  ("What is pi in a training record?", ["The move played", "The search's visit distribution", "The reward", "A random vector"], 1, "It comes from MCTS."),
  ("Does AlphaZero use symmetry augmentation?", ["Yes, for chess", "No, chess and shogi are asymmetric", "Yes, for shogi", "Only at test time"], 1, "AlphaGo Zero used it for Go; AlphaZero does not.")],
 [("What is z for a draw?", "0."), ("Who generates the data?", "Self-play workers using the latest network."), ("How many symmetries has Go?", "Eight."),
  ("Why is the target pi not the played move?", "pi is less noisy and richer.")],
 [PL("Outcomes from the mover's view", "A game lasts num_plies moves. Player 0 moves first, then players alternate (plies 0, 1, 2, ...). winner is 0 or 1, or -1 for a draw. Write outcomes(num_plies, winner): the list of z for each ply: 0 for a draw, +1 if the player moving at that ply is the winner, otherwise -1.",
     "outcomes(num_plies, winner)", """
def outcomes(num_plies, winner):
    out = []
    for t in range(num_plies):
        mover = t % 2
        if winner == -1:
            out.append(0)
        elif mover == winner:
            out.append(1)
        else:
            out.append(-1)
    return out
""", [[5, 0], [4, 1], [3, -1], [0, 0], [6, 0]], "The mover at ply t is t % 2."),
  PL("Build training examples", "states and pis are lists with one entry per ply (a state string and a probability list). Write build_examples(states, pis, winner): a list of [state, pi, z] for each ply, with z computed as in the previous lab (player 0 moves at even plies, winner is 0, 1 or -1 for a draw).",
     "build_examples(states, pis, winner)", """
def build_examples(states, pis, winner):
    out = []
    for t in range(len(states)):
        mover = t % 2
        if winner == -1:
            z = 0
        elif mover == winner:
            z = 1
        else:
            z = -1
        out.append([states[t], pis[t], z])
    return out
""", [[["a", "b", "c"], [[1.0], [0.5, 0.5], [1.0]], 0], [["a", "b"], [[0.4, 0.6], [1.0]], 1], [["a"], [[1.0]], -1], [[], [], 0]], "Combine each state and pi with the z for that ply."),
  PL("Symmetric copies", "A 3x3 board is a string of nine characters read row by row. Its eight symmetries are the four rotations and their mirror images. Write symmetric_boards(board): the sorted list of distinct boards among those eight (including the original).",
     "symmetric_boards(board)", """
def symmetric_boards(board):
    def rot(b):
        out = ['.'] * 9
        for r in range(3):
            for c in range(3):
                out[c * 3 + (2 - r)] = b[r * 3 + c]
        return ''.join(out)
    def mirror(b):
        out = ['.'] * 9
        for r in range(3):
            for c in range(3):
                out[r * 3 + (2 - c)] = b[r * 3 + c]
        return ''.join(out)
    seen = []
    b = board
    for i in range(4):
        for x in (b, mirror(b)):
            if x not in seen:
                seen.append(x)
        b = rot(b)
    seen.sort()
    return seen
""", [["X........"], ["....X...."], ["X...O...."], ["XO......."], ["XOX......"]], "Rotate four times, mirror each, and keep the distinct strings."),
  ORDER("From game to data", "Put the steps in order.", ["Play a game using MCTS at every move", "The game ends and the rules give the result", "Compute z for each position from the mover's view", "Store (state, pi, z) for each position", "Sample batches of records to train the network"]),
  FILL("Data", "Each record is a {{state|position}}, search probabilities pi and an {{outcome|result}} z. AlphaZero does not use symmetry {{augmentation}}. A draw has z equal to {{0|zero}}.")]))

# ------------------------------------------------------------ 8
CHS.append(CH(
 "The loss function and training",
 ("Learning from search", [
  "Value head | learns | Outcome z",
  "Policy head | learns | Search pi",
  "Loss | adds | Value, policy and weight terms",
  "Cross-entropy | measures | Policy mismatch",
  "L2 term | limits | Weight size",
  "Search | acts as | Policy improvement",
  "Self-play result | acts as | Policy evaluation"]),
 ["The network is trained on the self-play records to make two predictions: the value v should match the game outcome z, and the policy p should match the search probabilities pi. A third term penalizes large weights.",
  "The loss is the sum of a squared error on the value, a cross-entropy between pi and p, and an L2 regularization term. It is minimized with mini-batch gradient descent on batches of positions.",
  "This works as policy iteration. The search improves on the raw policy, the network is trained to imitate the improved policy, and the improved network makes the next search stronger."],
 [("Loss function", "A number that measures the network's error; training lowers it."),
  ("Mean squared error", "The average of squared differences, used for the value."),
  ("Cross-entropy", "-sum pi log p: how well p matches the target distribution pi."),
  ("L2 regularization", "A penalty c times the squared size of the weights."),
  ("Mini-batch", "A small random sample of training positions used for one gradient step."),
  ("Learning rate", "The size of each update step; AlphaZero lowered it in stages."),
  ("KL divergence", "A measure of how different two distributions are; cross-entropy minus entropy.")],
 ["l = (z - v)^2 - pi . log p + c ||theta||^2.",
  "The value target z is -1, 0 or +1.",
  "The policy target pi is the MCTS visit distribution.",
  "AlphaZero used mini-batches of 4,096 positions for 700 thousand steps.",
  "The learning rate was 0.2, dropped to 0.02, then 0.002, then 0.0002.",
  "Search = policy improvement; game outcome = policy evaluation."],
 [T("The records from chapter 7 are the training data. For each position s, the network gives p and v. We want v close to the outcome z, and p close to the search distribution pi. One number combines these goals, the loss."),
  M(r"\ell = (z - v)^2 \;-\; \boldsymbol{\pi}^{\top} \log \mathbf{p} \;+\; c\,\lVert \theta \rVert^2"),
  T("The first term is a squared error on the value: if the network said minus one for a position whose game was won, the error is large. The second term is the cross-entropy between the search distribution pi and the network's p, a sum over moves of minus pi times the logarithm of p. It is smallest when p equals pi. The third term is a penalty on the size of the weights controlled by a constant c, a standard guard against overfitting."),
  T("Cross-entropy is related to a distance between distributions. The cross-entropy of pi against p equals the entropy of pi plus the KL divergence from pi to p. The entropy of pi does not depend on the network, so minimizing the cross-entropy is the same as minimizing the KL divergence: pulling p toward pi."),
  T("Gradient descent. The loss is averaged over a mini-batch of positions sampled from self-play data, and the parameters theta take a step against the gradient, scaled by the learning rate. AlphaZero's published runs used 700 thousand mini-batches of 4,096 positions. The learning rate started at 0.2 and was dropped to 0.02, then 0.002 and finally 0.0002. The same network and settings were used for all three games."),
  T("Why does this work at all? The viewpoint in the papers is policy iteration. The raw network policy is a guess. Searching with the network gives a better policy, because the search looks ahead and corrects the network's mistakes with real game continuations. The network is trained toward that better policy, which improves it. This is policy improvement. The game outcomes, in turn, show how good the play really was, and so train the value, which is policy evaluation."),
  T("Bootstrapping. At first the network is random, so the search is only slightly better than random, and its games are noisy. But the outcomes of games are real facts decided by the rules, so even random play carries signal: positions leading to wins are given higher values. Gradually the value estimates improve, the search improves, and so on."),
  T("A note of caution from the literature. Later research observed that neither AlphaZero nor MuZero guarantees policy improvement unless all actions are evaluated at the root, and proposed Gumbel-based variants that do. So the improvement picture is a good intuition, not a theorem about the original algorithm."),
  T("In the practice section you compute the policy loss, the whole loss, the KL divergence and the learning rate schedule.")],
 [("What does the value head try to match?", ["The search probabilities", "The game outcome z", "The move played", "The weights"], 1, "Squared error against z."),
  ("What is the target for the policy head?", ["The move played", "The search visit distribution pi", "A random vector", "The value"], 1, "Cross-entropy with pi."),
  ("What is the third term of the loss for?", ["Speed", "Penalizing large weights", "Counting moves", "Drawing games"], 1, "L2 regularization."),
  ("How did the learning rate change?", ["It rose", "It was lowered in stages from 0.2", "It stayed 0.2", "It was random"], 1, "0.2, 0.02, 0.002, 0.0002.")],
 [("What is l?", "(z-v)^2 - pi.log p + c||theta||^2."), ("Why is the search a policy improvement?", "It beats the raw network policy."), ("How many steps were used?", "700 thousand mini-batches of 4,096."),
  ("What is KL used for?", "The distance from pi to p.")],
 [PL("Policy loss", "Write policy_loss(pi, p): the cross-entropy, minus the sum over moves of pi[i] * ln(p[i]), skipping moves where pi[i] is 0. Use math.log.",
     "policy_loss(pi, p)", """
import math
def policy_loss(pi, p):
    total = 0.0
    for i in range(len(pi)):
        if pi[i] > 0:
            total -= pi[i] * math.log(p[i])
    return total
""", [[[0.5, 0.5], [0.5, 0.5]], [[1.0, 0.0], [0.5, 0.5]], [[0.7, 0.2, 0.1], [0.6, 0.3, 0.1]], [[1.0], [1.0]]], "Skip terms with zero target probability.", 1e-9),
  PL("The whole loss", "Write total_loss(z, v, pi, p, theta, c): (z - v)^2 + policy loss (as above) + c * the sum of squares of the numbers in theta.",
     "total_loss(z, v, pi, p, theta, c)", """
import math
def total_loss(z, v, pi, p, theta, c):
    value = (z - v) ** 2
    pol = 0.0
    for i in range(len(pi)):
        if pi[i] > 0:
            pol -= pi[i] * math.log(p[i])
    reg = 0.0
    for w in theta:
        reg += w * w
    return value + pol + c * reg
""", [[1, 0.5, [0.5, 0.5], [0.5, 0.5], [1.0, -1.0], 0.01], [-1, -1, [1.0, 0.0], [0.9, 0.1], [], 0.1], [0, 0.3, [0.2, 0.8], [0.4, 0.6], [2.0], 0.5]], "Three terms: value error, cross-entropy and weight penalty.", 1e-9),
  PL("KL divergence", "Write kl_divergence(pi, p): the sum over moves where pi[i] > 0 of pi[i] * ln(pi[i] / p[i]). Cross-entropy minus the entropy of pi equals this.",
     "kl_divergence(pi, p)", """
import math
def kl_divergence(pi, p):
    total = 0.0
    for i in range(len(pi)):
        if pi[i] > 0:
            total += pi[i] * math.log(pi[i] / p[i])
    return total
""", [[[0.5, 0.5], [0.5, 0.5]], [[1.0, 0.0], [0.5, 0.5]], [[0.7, 0.2, 0.1], [0.6, 0.3, 0.1]], [[0.25, 0.75], [0.5, 0.5]]], "Only moves with positive pi contribute.", 1e-9),
  PL("Learning-rate schedule", "A schedule is a list of [start_step, rate] pairs sorted by start_step. Write lr_at(step, schedule): the rate of the last pair whose start_step is at most step.",
     "lr_at(step, schedule)", """
def lr_at(step, schedule):
    rate = schedule[0][1]
    for s in schedule:
        if s[0] <= step:
            rate = s[1]
    return rate
""", [[0, [[0, 0.2], [100, 0.02], [200, 0.002]]], [99, [[0, 0.2], [100, 0.02], [200, 0.002]]], [100, [[0, 0.2], [100, 0.02], [200, 0.002]]], [500, [[0, 0.2], [100, 0.02], [200, 0.002]]]], "Scan the schedule and keep the rate of the latest start that has been reached.", 1e-12),
  MATCH("Loss terms", "Match each term with its job.", [("(z - v)^2", "Value matches the outcome"), ("- pi . log p", "Policy matches the search"), ("c ||theta||^2", "Keeps weights small"), ("KL divergence", "Distance from pi to p"), ("Learning rate", "Size of each update step")]),
  FILL("Training", "The policy target is the search {{visit|visit count}} distribution. The value target is the game {{outcome|result}}. Training moves the network toward a {{better|improved}} policy found by the search.")]))
