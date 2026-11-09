"""Monte Carlo tree search course."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

NIM = """Nim in these labs: a pile of n stones; players alternate taking 1, 2 or 3 stones; whoever takes the last stone wins."""

CHS.append(CH(
 "What is Monte Carlo tree search?",
 ("MCTS", [
  "MCTS | builds | A search tree",
  "MCTS | uses | Random simulations",
  "Tree | grows | Asymmetrically",
  "UCT | balances | Exploration and exploitation",
  "MCTS | is | Anytime",
  "Coulom | named | MCTS in 2006",
  "Kocsis and Szepesvari | proposed | UCT"]),
 ["Monte Carlo tree search, MCTS, is a way to choose good actions in a decision problem by growing a search tree guided by random simulations. It needs little domain knowledge beyond the rules.",
  "It was developed around 2006. Remi Coulom described the idea and gave it the name. Levente Kocsis and Csaba Szepesvari proposed UCT, which uses a bandit rule to decide which branch to explore. It then transformed computer Go.",
  "MCTS repeats four steps: selection, expansion, simulation and backpropagation. This course builds each step in small Python labs on the game of Nim."],
 [("Monte Carlo method", "Estimating a quantity by averaging random samples."),
  ("Search tree", "A tree whose nodes are game states and whose edges are moves."),
  ("Simulation (rollout)", "Playing a game to the end with random or simple moves."),
  ("UCT", "Upper Confidence bounds applied to Trees: MCTS with the UCB1 selection rule."),
  ("Anytime algorithm", "One that can be stopped at any moment and still return its best answer so far."),
  ("Iteration", "One pass of the four MCTS steps.")],
 ["MCTS needs only a model of the rules: legal moves, transitions and terminal results.",
  "Four steps per iteration: selection, expansion, simulation, backpropagation.",
  "The tree grows towards promising moves, so it is asymmetric.",
  "UCT (Kocsis and Szepesvari, 2006) applies the UCB1 bandit rule at every node.",
  "Coulom (2006) used the term Monte Carlo tree search.",
  "Browne and colleagues (2012) surveyed the method and its many variants."],
 [T("Suppose you must pick a move in a game with far too many positions to search fully. Chess programs use a hand-written evaluation function to judge positions. In Go, nobody could write a good one. MCTS found another way: judge a move by playing many quick games from it and counting how often you win."),
  T("The idea has two parts. The Monte Carlo part is random sampling. Play a game to the end with random moves and see who wins. One game tells little, but the average of many tells something. The tree part is bookkeeping. Remember the results in a tree, so that more effort goes to moves that look good."),
  M(r"Q(s,a) \;\approx\; \frac{1}{N(s,a)}\sum_{i=1}^{N(s,a)} z_i, \qquad z_i \in \{0, 1\}\ \text{the result of the } i\text{-th simulation}"),
  T("Credit goes to several people. Bruce Abramson in 1990 suggested estimating position values by random playouts. Remi Coulom in 2006 built these ideas into a tree search for Go and called it Monte Carlo tree search. In the same year Levente Kocsis and Csaba Szepesvari published UCT, which supplied the missing piece: a principled rule for choosing which branch to explore. The 2012 survey by Cameron Browne and colleagues is the standard overview, and this course follows it."),
  T("MCTS has attractive properties. It needs only the rules of the game, not an evaluation function. It is anytime: stop it after one second or one hour and it still has a best move. The tree grows unevenly, deeper where moves look strong. And with enough time its choice converges to the best move, a property proved for UCT."),
  T("It also has limits that later chapters discuss. Random playouts can be misleading, and MCTS can be fooled by traps, positions where one precise reply refutes an attractive move. AlphaGo, studied in a sister course, kept the tree but replaced random playouts by neural networks."),
  T("The labs use Nim as a test game. A pile of n stones; players alternate taking one, two or three; whoever takes the last stone wins. It is small enough to check every answer by hand, and rich enough to show every idea.")],
 [("What does MCTS estimate by simulation?", ["Win rates of moves", "Board size", "Rules", "Time"], 0, "Average results of random games."),
  ("Which rule did UCT add?", ["A bandit rule for choosing branches", "A random move", "A neural network", "A hash table"], 0, "UCB1 applied at each node."),
  ("What does anytime mean?", ["Can be stopped any time with a best answer", "Runs forever", "Needs a clock", "Uses no memory"], 0, "More time gives a better answer."),
  ("How many steps does an iteration have?", ["Four", "Two", "Six", "One"], 0, "Selection, expansion, simulation, backpropagation.")],
 [("Who named MCTS?", "Remi Coulom, 2006."), ("Who proposed UCT?", "Kocsis and Szepesvari, 2006."), ("Which survey is standard?", "Browne et al., 2012."), ("What replaced playouts in AlphaGo?", "Neural network evaluation.")],
 [ORDER("One MCTS iteration", "Put the four steps in order.", ["Selection: walk down the tree", "Expansion: add a new node", "Simulation: play out to the end", "Backpropagation: update the path"]),
  MATCH("Terms", "Match each term with its meaning.", [("Rollout", "Quick game to the end"), ("UCT", "MCTS with UCB1 selection"), ("Anytime", "Can stop at any moment"), ("Search tree", "States and moves"), ("Monte Carlo", "Averaging random samples")]),
  FILL("Basics", "MCTS repeats {{selection}}, expansion, simulation and {{backpropagation|back propagation}}.")]))

CHS.append(CH(
 "Games, trees and the need for search",
 ("Game trees", [
  "Game tree | has | States as nodes",
  "Move | is | An edge",
  "Branching factor | counts | Moves per state",
  "Minimax | solves | Small games exactly",
  "Terminal state | has | A result",
  "Nim | is | Our test game",
  "Tree size | grows | Exponentially"]),
 ["A game can be drawn as a tree. The root is the current position, each edge is a legal move, and the leaves are finished games. Solving a small game means labelling every node as a win or a loss for the player to move.",
  "Minimax does this exactly, working up from the leaves. A position is a win if some move leads to a position that is a loss for the opponent. Minimax is perfect but needs the whole tree, which grows exponentially: with b moves per state and depth d there are about b to the d leaves.",
  "Go has about 250 moves per position and games of 150 moves, so exact search is hopeless. That is the gap MCTS fills."],
 [("Game tree", "A tree of all positions reachable by legal play."),
  ("Branching factor", "The average number of legal moves in a position."),
  ("Minimax", "Exact evaluation: you pick the best move, the opponent picks the worst for you."),
  ("Terminal state", "A position where the game is over."),
  ("Win or loss for the player to move", "The exact value of a position under perfect play."),
  ("Nim", "A take-away game; here you remove 1 to 3 stones and taking the last wins.")],
 ["Nim: take 1 to 3 stones; the player who takes the last stone wins.",
  "A position with 0 stones is lost for the player to move: the opponent just took the last.",
  "Minimax: win if any move leads to a loss for the opponent.",
  "The tree has about b^d leaves; Go's b is about 250.",
  "In Nim with a take limit of 3, positions that are multiples of 4 are lost for the player to move.",
  "MCTS estimates what minimax computes, using samples."],
 [T("Take a pile of ten stones. You and I alternate; each turn removes one, two or three; whoever takes the last stone wins. What should you do first? You could picture all possibilities: three first moves, each followed by three replies, and so on. That picture is the game tree."),
  T("Leaves are finished games. A position with no stones left means the previous player took the last stone and won, so the player to move has lost. Work backwards. A position is winning for the player to move if at least one move leads to a position that is losing for the opponent. It is losing if every move leads to a position that is winning for the opponent."),
  M(r"W(n) = \begin{cases} \text{lost} & n = 0 \\ \text{won} & \exists\, k \in \{1,2,3\},\ k \le n,\ W(n-k) = \text{lost} \\ \text{lost} & \text{otherwise} \end{cases}"),
  T("This is minimax in its simplest form. For Nim, the answer has a pattern: a pile that is a multiple of four is lost for the player to move, since whatever you take, the opponent can take enough to leave another multiple of four. Any other pile is won: take what leaves a multiple of four."),
  T("Minimax scales badly. The number of leaves is about b to the d for b moves and depth d. Chess has b around 35 and games of about 80 plies, far beyond any computer. Go has b around 250 and about 150 plies. Chess programs cut the tree with alpha-beta pruning and an evaluation function. For Go, no good evaluation was known."),
  T("MCTS takes a different route. It does not try to cover the tree. It samples it, and focuses the samples. In the labs below you write exact solvers for Nim first, because they give the ground truth against which the sampled estimates can be judged.")],
 [("Which pile sizes are lost for the player to move (take 1 to 3)?", ["Multiples of 4", "Odd numbers", "Multiples of 3", "Primes"], 0, "Including 0."),
  ("What is the value of 0 stones?", ["Lost for the player to move", "Won", "Draw", "Undefined"], 0, "The opponent took the last stone."),
  ("What is a winning position?", ["Some move leads to a losing position for the opponent", "Every move wins", "No move exists", "The pile is odd"], 0, "Minimax."),
  ("Why is exact search hopeless in Go?", ["The tree is astronomically large", "Rules are secret", "Moves are random", "Boards are small"], 0, "About 250 to the power 150.")],
 [("What is b?", "The branching factor."), ("What is d?", "The depth of the game."), ("How big is the tree?", "About b to the d."), ("What does minimax need?", "The whole tree.")],
 [PL("Legal moves", NIM + " Write nim_moves(n): the list of legal takes from a pile of n stones, in increasing order: 1, 2, 3 limited by n.",
     "nim_moves(n)", """
def nim_moves(n):
    out = []
    for k in range(1, 4):
        if k <= n:
            out.append(k)
    return out
""", [[0], [1], [2], [5], [10]], "At most three moves, and never more than n."),
  PL("Exact value", "Write nim_wins(n): 1 if the player to move wins Nim with n stones (exact minimax by recursion), otherwise 0.",
     "nim_wins(n)", """
def nim_wins(n):
    if n == 0:
        return 0
    for k in range(1, 4):
        if k <= n and nim_wins(n - k) == 0:
            return 1
    return 0
""", [[0], [1], [3], [4], [5], [8], [11], [12]], "Win if some move leaves a lost position."),
  PL("Size of the tree", "Write tree_size(n): the number of nodes in the full game tree of Nim from a pile of n (the root counts, and each legal move leads to a child).",
     "tree_size(n)", """
def tree_size(n):
    total = 1
    for k in range(1, 4):
        if k <= n:
            total += tree_size(n - k)
    return total
""", [[0], [1], [3], [6], [10]], "One for this node plus the sizes of the children."),
  PL("Best exact move", "Write best_move(n): the smallest take that leaves a lost position for the opponent, or 1 if there is none (exact minimax).",
     "best_move(n)", """
def best_move(n):
    def wins(m):
        if m == 0:
            return 0
        for k in range(1, 4):
            if k <= m and wins(m - k) == 0:
                return 1
        return 0
    for k in range(1, 4):
        if k <= n and wins(n - k) == 0:
            return k
    return 1
""", [[1], [2], [5], [6], [7], [8], [10]], "Try the takes in order."),
  ORDER("Solving a game", "Order the minimax steps.", ["Label terminal positions", "Label positions whose moves all lead to wins for the opponent as losses", "Label positions with a move to a loss as wins", "Work backwards to the root", "Read off the best move"]),
  MATCH("Nim", "Match each pile with its value for the player to move.", [("0", "Lost"), ("4", "Lost"), ("5", "Won"), ("8", "Lost"), ("11", "Won")]),
  FILL("Search", "Minimax is exact but the tree has about b to the {{d|depth}} leaves, where b is the {{branching}} factor.")]))

CHS.append(CH(
 "Random playouts and Monte Carlo estimation",
 ("Playouts", [
  "Playout | plays | Random moves to the end",
  "Win rate | estimates | Position value",
  "More playouts | reduce | Noise",
  "Error | shrinks as | One over root n",
  "Pseudo-random numbers | make | Runs repeatable",
  "LCG | generates | Pseudo-random numbers",
  "Random policy | is | Weak but unbiased"]),
 ["A playout (also called a rollout or simulation) plays a game to the end with random moves. Its result, win or loss, is a noisy estimate of the position's value. Averaging many playouts reduces the noise.",
  "The standard error of an average of n samples shrinks like one over the square root of n. Ten times more playouts make the estimate about three times more accurate.",
  "The labs use a tiny linear congruential generator for pseudo-random numbers, so that every result is exactly repeatable."],
 [("Playout", "A simulated game from a position to its end."),
  ("Win rate", "Wins divided by playouts."),
  ("Standard error", "The typical size of the estimate's error."),
  ("Pseudo-random generator", "A deterministic formula producing numbers that look random."),
  ("LCG", "Linear congruential generator: x becomes (a x + c) mod m."),
  ("Seed", "The starting value of a generator.")],
 ["The playout result for the player to move is 1 for a win and 0 for a loss.",
  "Win rate = wins / playouts.",
  "Standard error is about sqrt(p (1 - p) / n).",
  "A random playout policy picks uniformly among legal moves.",
  "Estimates from random play are noisy and may be biased as a measure of perfect-play value.",
  "In the labs: x -> (75 x + 74) mod 65537, a small LCG, picks the move index as x mod number of moves."],
 [T("Take the Nim position with five stones. We know the exact answer: it is won for the player to move, by taking one stone. Pretend we do not know. We could play random games from here and count how often the player to move wins. If the estimate is above one half, the position looks good."),
  T("Each playout is a short story. Starting at the position, the player to move picks a random legal move, then the other player, and so on until the pile is empty. The one who took the last stone wins. Record 1 if that was the player who started, otherwise 0."),
  M(r"\hat{p} = \frac{1}{n}\sum_{i=1}^{n} z_i, \qquad \mathrm{SE}(\hat{p}) \approx \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}"),
  T("This is the Monte Carlo estimate and its standard error. With 100 playouts and a true rate of one half, the error is around five percentage points. With 10,000 playouts it is around half a point. The cost grows linearly with n while the error shrinks only with its square root, a good reason to spend playouts where they matter."),
  T("There is a subtlety. The win rate under random play is not the value under perfect play. A position can be lost against a perfect opponent, yet random opponents blunder so often that it wins most playouts. MCTS reduces this problem by choosing moves inside the tree better than randomly, so playouts are used only below the tree's frontier."),
  T("For repeatable labs we need random numbers that are reproducible. A linear congruential generator updates a number by x to (a times x plus c) modulo m. The labs use a tiny one with m of 65537, a of 75 and c of 74, so everything stays far below the integer limit. Its quality is poor for serious work but fine for teaching.")],
 [("What does a playout return?", ["Win or loss of a simulated game", "A move", "A tree", "The rules"], 0, "A noisy estimate."),
  ("How does error shrink with n playouts?", ["Like one over the square root of n", "Like one over n squared", "It does not", "Linearly"], 0, "Ten times more for three times accuracy."),
  ("Why a seeded generator?", ["Repeatable results", "Better randomness", "Faster code", "Smaller tree"], 0, "Same seed, same run."),
  ("Is random-play win rate equal to perfect-play value?", ["No, it can differ", "Always", "Never", "Only in Nim"], 0, "Random opponents blunder.")],
 [("What is the LCG here?", "x -> (75 x + 74) mod 65537."), ("What is SE?", "sqrt(p (1-p) / n)."), ("What do we average?", "Playout results."), ("Where are playouts used?", "Below the tree frontier.")],
 [PL("Next random number", "Write lcg(x): the next value of the generator, (75 * x + 74) % 65537.",
     "lcg(x)", """
def lcg(x):
    return (75 * x + 74) % 65537
""", [[1], [0], [12345], [65536]], "One line of arithmetic."),
  PL("One random playout", NIM + " Write playout(n, seed): play random legal moves from n stones until the pile is empty. At each step: x = lcg(x) (starting from seed), the legal takes are 1..min(3, n), and the take is moves[x % len(moves)]. Return 1 if the player who moved first at the start takes the last stone, else 0. Here lcg(x) = (75 * x + 74) % 65537.",
     "playout(n, seed)", """
def playout(n, seed):
    x = seed
    player = 0
    last = 1
    if n == 0:
        return 0
    while n > 0:
        x = (75 * x + 74) % 65537
        top = 3 if n >= 3 else n
        k = 1 + x % top
        n -= k
        last = player
        player = 1 - player
    return 1 if last == 0 else 0
""", [[5, 1], [5, 2], [10, 7], [4, 3], [1, 5], [0, 1], [12, 99]], "Alternate players; the last mover wins."),
  PL("Win-rate estimate", "Write estimate(n, k, seed): the fraction of k playouts from n stones won by the player to move. Playout j (from 0) uses the seed (seed + j) as its starting value. Same playout rule as before. Return wins / k.",
     "estimate(n, k, seed)", """
def estimate(n, k, seed):
    wins = 0
    for j in range(k):
        x = seed + j
        m = n
        player = 0
        last = 1
        if m == 0:
            continue
        while m > 0:
            x = (75 * x + 74) % 65537
            top = 3 if m >= 3 else m
            t = 1 + x % top
            m -= t
            last = player
            player = 1 - player
        if last == 0:
            wins += 1
    return wins / k
""", [[5, 20, 1], [4, 20, 1], [8, 30, 5], [1, 10, 3], [10, 50, 11]], "Count playouts won by the first player.", approx=1e-9),
  PL("Standard error", "Write std_error(p, n): sqrt(p * (1 - p) / n). Use import math.",
     "std_error(p, n)", """
import math
def std_error(p, n):
    return math.sqrt(p * (1 - p) / n)
""", [[0.5, 100], [0.5, 10000], [0.9, 50], [0.0, 10]], "Plain formula.", approx=1e-9),
  ORDER("Estimating a position", "Order the steps.", ["Seed the generator", "Play a random game to the end", "Record the result for the player to move", "Repeat n times", "Divide wins by n"]),
  MATCH("Statistics", "Match each term with its meaning.", [("Win rate", "Wins over playouts"), ("Standard error", "Typical estimate error"), ("Seed", "Generator start value"), ("LCG", "Simple pseudo-random formula"), ("Playout", "Random game to the end")]),
  FILL("Sampling", "The error of a Monte Carlo average shrinks like one over the square {{root}} of the number of {{playouts|samples}}.")]))

CHS.append(CH(
 "Bandits and the UCB1 rule",
 ("Bandits", [
  "Bandit | has | Several arms",
  "Pull | gives | A random reward",
  "Exploitation | picks | The best known arm",
  "Exploration | tries | Uncertain arms",
  "UCB1 | adds | A confidence bonus",
  "Regret | measures | Loss versus the best arm",
  "UCB1 | by | Auer et al. 2002"]),
 ["A multi-armed bandit is the simplest setting where exploration and exploitation clash. There are several arms, each paying a random reward with an unknown mean. You pull one arm per round and want the highest total reward.",
  "UCB1, by Auer, Cesa-Bianchi and Fischer in 2002, picks the arm with the highest upper confidence bound: its average reward plus a bonus that is large for rarely pulled arms. Its regret grows only logarithmically with the number of pulls.",
  "In MCTS, each move at each node is an arm and each playout is a pull."],
 [("Multi-armed bandit", "A problem of repeatedly choosing among arms with unknown reward distributions."),
  ("Exploitation", "Choosing the arm that has looked best so far."),
  ("Exploration", "Choosing an arm to learn about it."),
  ("UCB1", "Choose the arm maximising mean + c sqrt(2 ln N / n_i)."),
  ("Regret", "The reward lost by not always playing the best arm."),
  ("Confidence bonus", "The term that grows when an arm has been tried few times.")],
 ["UCB1 value of arm i: mean_i + c * sqrt(2 ln N / n_i).",
  "N is the total number of pulls and n_i the pulls of arm i; untried arms are pulled first.",
  "The bonus shrinks as n_i grows and grows slowly as N grows, so every arm is revisited eventually.",
  "UCB1 has logarithmic regret in the number of pulls (Auer et al., 2002).",
  "In UCT the constant is written C_p; the survey notes 1/sqrt(2) for rewards in [0, 1].",
  "In MCTS the arm is a child move; the reward is a playout result."],
 [T("Imagine a row of slot machines. Each pays out on average a different amount, which you do not know. You have a thousand coins. If you pull each once and then stick with the best looking one, you may be fooled by luck. If you keep trying all of them, you waste coins on poor machines. How do you balance?"),
  T("UCB1 gives a clean answer. Give each arm a score equal to its average reward so far plus a bonus. The bonus is big when the arm has been pulled rarely, because the average is then unreliable, and small when it has been pulled many times. Always pull the arm with the highest score. This is optimism in the face of uncertainty."),
  M(r"\mathrm{UCB1}_i \;=\; \bar{X}_i \;+\; c\,\sqrt{\frac{2\ln N}{n_i}}"),
  T("Look at the bonus. As n i grows the bonus falls, so well-sampled arms must earn their place with their average. As the total N grows, ln N grows slowly, so a neglected arm's bonus rises until it is tried again. No arm is dropped forever. Auer and colleagues proved that the total regret grows only logarithmically in the number of pulls, which is the best order possible."),
  T("The constant c sets the balance. In the original analysis for rewards between zero and one, c is one. The MCTS survey writes the constant for UCT as C p and notes the value one over the square root of two satisfies the theory for rewards in the unit interval. In practice it is tuned. Larger values explore more."),
  T("The labs write the UCB1 score, choose the best arm, and measure regret in a small deterministic bandit.")],
 [("What does the UCB1 bonus do?", ["Favours rarely tried arms", "Favours the best arm only", "Ignores counts", "Adds noise"], 0, "Shrinks as n grows."),
  ("What does regret measure?", ["Reward lost against the best arm", "Time", "Memory", "Arm count"], 0, "Logarithmic for UCB1."),
  ("What happens to the bonus as N grows with n_i fixed?", ["It grows slowly", "It shrinks", "It is constant", "It flips sign"], 0, "ln N increases."),
  ("What is exploitation?", ["Choosing the best known arm", "Choosing at random", "Trying new arms only", "Stopping"], 0, "Versus exploration.")],
 [("Who proved the regret bound?", "Auer, Cesa-Bianchi and Fischer, 2002."), ("What are untried arms given?", "Priority; infinite value."), ("What is c?", "The exploration constant."), ("What is the arm in MCTS?", "A child move.")],
 [PL("UCB1 score", "Write ucb1(mean, total, count, c): mean + c * sqrt(2 * ln(total) / count). Use import math.",
     "ucb1(mean, total, count, c)", """
import math
def ucb1(mean, total, count, c):
    return mean + c * math.sqrt(2 * math.log(total) / count)
""", [[0.5, 10, 2, 1.0], [0.5, 100, 20, 1.0], [0.0, 2, 1, 0.5], [0.9, 50, 49, 1.0], [0.3, 20, 5, 0.7071]], "Mean plus the bonus.", approx=1e-9),
  PL("Choose an arm", "Write choose_arm(means, counts, c): the index of the arm with the highest UCB1 score; an arm with count 0 is chosen immediately (the lowest such index). The total is the sum of counts. Ties go to the lowest index. Use import math.",
     "choose_arm(means, counts, c)", """
import math
def choose_arm(means, counts, c):
    for i in range(len(counts)):
        if counts[i] == 0:
            return i
    total = sum(counts)
    best = -1e18
    arg = 0
    for i in range(len(counts)):
        s = means[i] + c * math.sqrt(2 * math.log(total) / counts[i])
        if s > best + 1e-12:
            best = s
            arg = i
    return arg
""", [[[0.5, 0.6], [10, 10], 1.0], [[0.5, 0.6], [0, 5], 1.0], [[0.9, 0.1], [50, 2], 1.0], [[0.9, 0.1], [50, 2], 0.1], [[0.2, 0.8, 0.5], [5, 5, 5], 1.0]], "Untried arms first, then the highest score."),
  PL("Run a deterministic bandit", "Arms have fixed rewards (a list of numbers; pulling arm i always gives rewards[i]). Write run_ucb(rewards, rounds, c): pull each arm once, then use UCB1 for the remaining rounds (means are the running averages). Return the list of pull counts per arm. Ties go to the lowest index. Use import math.",
     "run_ucb(rewards, rounds, c)", """
import math
def run_ucb(rewards, rounds, c):
    k = len(rewards)
    counts = [0] * k
    sums = [0.0] * k
    for t in range(rounds):
        if t < k:
            arg = t
        else:
            total = sum(counts)
            best = -1e18
            arg = 0
            for i in range(k):
                s = sums[i] / counts[i] + c * math.sqrt(2 * math.log(total) / counts[i])
                if s > best + 1e-12:
                    best = s
                    arg = i
        counts[arg] += 1
        sums[arg] += rewards[arg]
    return counts
""", [[[0.2, 0.8], 50, 1.0], [[0.5, 0.5, 0.5], 30, 1.0], [[0.1, 0.9, 0.4], 100, 0.5], [[1.0, 0.0], 20, 1.0]], "Keep counts and sums."),
  PL("Regret", "Write regret(rewards, counts): the total regret = sum over arms of counts[i] * (best reward - rewards[i]).",
     "regret(rewards, counts)", """
def regret(rewards, counts):
    best = max(rewards)
    total = 0.0
    for r, n in zip(rewards, counts):
        total += n * (best - r)
    return total
""", [[[0.2, 0.8], [10, 40]], [[0.5, 0.5], [5, 5]], [[0.1, 0.9, 0.4], [3, 90, 7]]], "Weight the gap by the pulls.", approx=1e-9),
  ORDER("Using UCB1", "Order the steps.", ["Pull every arm once", "Compute each arm's mean", "Add the confidence bonus", "Pull the arm with the highest score", "Update its count and mean"]),
  MATCH("Bandit terms", "Match each term with its meaning.", [("Exploitation", "Use what looks best"), ("Exploration", "Learn about other arms"), ("Bonus", "Large for rarely tried arms"), ("Regret", "Reward lost"), ("UCB1", "Mean plus confidence bonus")]),
  FILL("UCB1", "UCB1 adds a confidence {{bonus}} that is large for arms pulled {{rarely|few times|seldom}}.")]))

CHS.append(CH(
 "The four steps: selection, expansion, simulation, backpropagation",
 ("One iteration", [
  "Selection | descends | Using a tree policy",
  "Expansion | adds | A new child",
  "Simulation | plays | A default policy",
  "Backpropagation | updates | Visits and wins",
  "Node | stores | N and W",
  "Root | is | The current position",
  "Result | flips | Between players"]),
 ["Each iteration starts at the root. Selection walks down through nodes already in the tree, following a tree policy. When it reaches a node with an untried move, expansion adds a child for one. Simulation plays from the new node to the end with a default policy. Backpropagation then updates every node on the path with the result.",
  "Each node stores two numbers: its visit count N and its total reward W. The mean reward is W over N.",
  "Because the players alternate, the result must be flipped as it travels up: a win for one player is a loss for the other."],
 [("Tree policy", "The rule used to pick children while inside the tree."),
  ("Default policy", "The rule used to play moves in the simulation, often random."),
  ("Visit count N", "How many iterations passed through a node."),
  ("Total reward W", "The sum of results backed up through a node."),
  ("Untried move", "A legal move with no child node yet."),
  ("Frontier", "The boundary between the tree and the unexplored part.")],
 ["Selection: from the root, follow the tree policy to a node that is not fully expanded or is terminal.",
  "Expansion: add one child for an untried move.",
  "Simulation: play the default policy from the new child to a terminal state.",
  "Backpropagation: add 1 to N on every node of the path, and add the result to W from that node's perspective.",
  "Rewards from a node's parent's perspective alternate with depth.",
  "After the iterations, the move is chosen from the root's children."],
 [T("MCTS grows a tree one node per iteration. Each iteration is the same four-step cycle, and the cycle is the heart of the algorithm. Learn it well and the rest is variation."),
  T("Selection. Start at the root, the current position. If the node is fully expanded, which means every legal move already has a child, pick a child with the tree policy and move down. Repeat until you reach a node that has an untried move, or a finished game."),
  T("Expansion. If the node has an untried move, create the child for it and add it to the tree. Only one node is added per iteration, which keeps the tree growing slowly and evenly."),
  T("Simulation. From the new node, play the game to the end with the default policy. In plain MCTS the default policy is uniformly random. The final result is recorded: win, loss or perhaps a score."),
  M(r"N(v) \leftarrow N(v) + 1, \qquad W(v) \leftarrow W(v) + r_v \quad\text{for every node } v \text{ on the path}"),
  T("Backpropagation. Walk back up the path from the new node to the root. Add one to each node's visit count and add the result to its total. Take care of perspective. In a two-player game the result that is good for the player who made the move into a node is bad for the player moving out of it. So the reward alternates between one and zero down the path. Many programs store at each node the result from the viewpoint of the player who moved into it, so the selection at the parent can simply maximise."),
  T("The loop then repeats, thousands or millions of times. The visit counts concentrate on strong moves, and the final choice reads them off. The labs implement each step on a small tree stored in lists.")],
 [("How many nodes does expansion add?", ["One", "All children", "None", "The whole tree"], 0, "Per iteration."),
  ("What does simulation use?", ["The default policy", "The tree policy", "A neural network only", "Minimax"], 0, "Often random moves."),
  ("What is updated in backpropagation?", ["N and W on the path", "The rules", "Only the root", "Only the leaf"], 0, "From the new node up to the root."),
  ("Why flip the result?", ["Players alternate", "To save time", "Rewards are negative", "To avoid ties"], 0, "A win for one is a loss for the other.")],
 [("Where does selection stop?", "At a node with an untried move or a terminal node."), ("What does a node store?", "N and W."), ("What starts an iteration?", "The root."), ("What is W/N?", "The mean reward.")],
 [PL("Backpropagate", "A path is a list of nodes from the root down to the new node, each node a [visits, total] pair. Write backprop(path, result): add 1 to the visits of each node and add the result to the total of the new (last) node, alternating the result between result and 1 - result going up the path (the last node gets result, its parent gets 1 - result, and so on). Return the updated path.",
     "backprop(path, result)", """
def backprop(path, result):
    out = []
    n = len(path)
    for i in range(n):
        steps = n - 1 - i
        r = result if steps % 2 == 0 else 1 - result
        out.append([path[i][0] + 1, path[i][1] + r])
    return out
""", [[[[0, 0], [0, 0], [0, 0]], 1], [[[2, 1], [1, 0]], 0], [[[5, 3]], 1], [[[1, 1], [1, 0], [1, 1], [0, 0]], 1]], "Count back from the last node to decide the sign."),
  PL("Untried moves", "A node for a Nim pile of n stones has children for some takes. Write untried(n, tried): the list of legal takes (1..min(3, n)) that are not in the list tried, in increasing order.",
     "untried(n, tried)", """
def untried(n, tried):
    out = []
    for k in range(1, 4):
        if k <= n and k not in tried:
            out.append(k)
    return out
""", [[5, []], [5, [1, 2, 3]], [2, [1]], [0, []], [4, [2]]], "Legal moves minus those with children."),
  PL("Mean reward", "Write mean_reward(node): node is [visits, total]; return total / visits, or 0.5 if visits is 0.",
     "mean_reward(node)", """
def mean_reward(node):
    if node[0] == 0:
        return 0.5
    return node[1] / node[0]
""", [[[4, 3]], [[0, 0]], [[10, 2]], [[1, 1]]], "Guard the empty case.", approx=1e-12),
  PL("Expand a node", "A node's children are stored as a list of [take, visits, total]. Write expand(children, n): if there are untried takes for a pile of n (legal takes not yet in the list), add a child [take, 0, 0] for the smallest untried take and return the new list; otherwise return the list unchanged.",
     "expand(children, n)", """
def expand(children, n):
    tried = [c[0] for c in children]
    for k in range(1, 4):
        if k <= n and k not in tried:
            return children + [[k, 0, 0]]
    return children
""", [[[], 5], [[[1, 3, 2]], 5], [[[1, 3, 2], [2, 1, 1], [3, 1, 0]], 5], [[], 0], [[[1, 1, 1]], 1]], "Add the smallest missing legal take."),
  ORDER("An iteration", "Order the steps.", ["Start at the root", "Descend by the tree policy", "Add a child for an untried move", "Play a simulation to the end", "Update visits and rewards up the path"]),
  MATCH("Pieces", "Match each piece with its job.", [("Tree policy", "Chooses inside the tree"), ("Default policy", "Plays the simulation"), ("N", "Visit count"), ("W", "Total reward"), ("Expansion", "Adds a child")]),
  FILL("Cycle", "A node stores the visit count {{N}} and total reward {{W}}.")]))

CHS.append(CH(
 "UCT and a complete search",
 ("UCT", [
  "UCT | applies | UCB1 in the tree",
  "Child score | is | Mean plus bonus",
  "C | sets | Exploration weight",
  "Iterations | are | The search budget",
  "Best move | is | Most visited child",
  "Tree | reuses | Past work",
  "Search | is | Anytime"]),
 ["UCT is MCTS with UCB1 as the tree policy: at each node, descend to the child maximising its mean reward plus an exploration bonus. This treats every node as a bandit problem.",
  "With the pieces from earlier chapters we can write a full search. Run a fixed number of iterations from the current position, then play the root move with the most visits.",
  "The labs do exactly that on Nim, with a small deterministic random generator, so the whole search is repeatable."],
 [("UCT score", "mean + C sqrt(ln N_parent / n_child), in the survey's form with a constant."),
  ("Search budget", "The number of iterations or the time allowed."),
  ("Root move", "The move chosen from the root after the search."),
  ("Most visited child", "The child with the highest visit count."),
  ("Fully expanded", "A node with a child for every legal move."),
  ("Convergence", "With enough iterations UCT's choice approaches the optimal move.")],
 ["UCT picks the child maximising mean + C * sqrt(ln(N_parent) / n_child).",
  "Browne et al. write the bonus as 2 C_p sqrt(2 ln n / n_j); the constants differ only by scaling C.",
  "Kocsis and Szepesvari proved that UCT converges to the minimax value for finite games.",
  "Choose the final move by visits.",
  "More iterations give better play.",
  "The labs fix C = 1 and a deterministic generator."],
 [T("Now we assemble the full algorithm. At each node reached in selection that has all its moves tried, use the UCT rule to choose among its children. Where it has untried moves, expand one. Then simulate and back up."),
  M(r"v^{*} \;=\; \arg\max_{v'\,\in\,\mathrm{children}(v)}\ \left( \frac{W(v')}{N(v')} \;+\; C\sqrt{\frac{\ln N(v)}{N(v')}} \right)"),
  T("The survey writes the rule with a factor of two and a constant C p, but the shape is the same: the first term favours moves that did well, the second favours moves tried little. The constant C is tuned for the game. A larger C explores more and may waste simulations; a smaller C exploits more and may miss good moves."),
  T("Kocsis and Szepesvari proved a strong property: for finite games, with enough iterations the probability of choosing a suboptimal move goes to zero, so UCT converges to the minimax answer. The result is asymptotic. In practice the number of iterations needed can be very large, particularly in games with traps."),
  T("How to pick the move at the end? The most robust choice is the child with the most visits, since a high visit count means UCT kept finding it worth exploring. The child with the highest mean can be a lucky sample with few visits. Chapter 7 compares the options."),
  T("Because the search tree carries over, a program can keep the subtree of the move actually played and reuse its statistics on the next turn. And because the search is anytime, the program can think for as long as the clock allows.")],
 [("What does UCT choose in the tree?", ["The child with the highest mean plus bonus", "A random child", "The first child", "The last child"], 0, "UCB1 at each node."),
  ("What does a larger C do?", ["More exploration", "Less exploration", "Nothing", "Smaller tree"], 0, "Bigger bonus."),
  ("Which move is played at the end?", ["Usually the most visited", "The least visited", "A random one", "The first"], 0, "Robust."),
  ("What is proved about UCT?", ["Convergence to minimax for finite games", "It is always fast", "It needs no memory", "It never loses"], 0, "Asymptotically.")],
 [("What are the parts of the score?", "Mean reward and exploration bonus."), ("What does a high C do?", "Explores more."), ("What can be reused?", "The subtree of the played move."), ("Is convergence fast?", "Not necessarily.")],
 [PL("UCT score", "Write uct_score(w, n, parent_n, c): w / n + c * sqrt(ln(parent_n) / n); an unvisited child (n = 0) has infinite score, return 1e18. Use import math.",
     "uct_score(w, n, parent_n, c)", """
import math
def uct_score(w, n, parent_n, c):
    if n == 0:
        return 1e18
    return w / n + c * math.sqrt(math.log(parent_n) / n)
""", [[3, 5, 20, 1.0], [0, 0, 20, 1.0], [10, 10, 100, 0.5], [1, 2, 3, 1.4]], "Mean plus bonus.", approx=1e-9),
  PL("Select a child", "Write select_child(children, parent_n, c): children is a list of [take, visits, total] where total is the reward for the player choosing that take; return the take of the child with the highest UCT score (an unvisited child first; ties to the lowest take). Use import math.",
     "select_child(children, parent_n, c)", """
import math
def select_child(children, parent_n, c):
    best = -1e18
    arg = children[0][0]
    for take, n, w in children:
        if n == 0:
            return take
        s = w / n + c * math.sqrt(math.log(parent_n) / n)
        if s > best + 1e-12:
            best = s
            arg = take
    return arg
""", [[[[1, 5, 3], [2, 5, 2], [3, 5, 4]], 15, 1.0], [[[1, 5, 3], [2, 0, 0]], 5, 1.0], [[[1, 50, 30], [2, 2, 2]], 52, 1.0], [[[1, 50, 30], [2, 2, 2]], 52, 0.1]], "Compute each score."),
  PL("Full UCT search on Nim", NIM + " Write uct_nim(n, iterations, c, seed): run UCT from a pile of n stones. Each node stores visits N and total W from the viewpoint of the player who made the move INTO it (so at the parent we maximise W/N). Selection: at a node with an untried take, expand the smallest untried take; otherwise choose the child by w/n + c*sqrt(ln(parent N)/n) (ties to the lowest take). Simulation: random playout with x = (75*x + 74) % 65537, take = 1 + x % min(3, pile), x continuing across iterations (start at seed). Backpropagate alternating perspective. Return the take with the most visits at the root (ties to the lowest). For a terminal node (pile 0) the player who moved into it won (result 1 for that node).",
     "uct_nim(n, iterations, c, seed)", """
import math
def uct_nim(n, iterations, c, seed):
    # node: [pile, visits, total, children dict take->node]
    root = [n, 0, 0.0, {}]
    x = seed
    for it in range(iterations):
        node = root
        path = [node]
        # selection and expansion
        while node[0] > 0:
            top = 3 if node[0] >= 3 else node[0]
            untried = None
            for k in range(1, top + 1):
                if k not in node[3]:
                    untried = k
                    break
            if untried is not None:
                child = [node[0] - untried, 0, 0.0, {}]
                node[3][untried] = child
                node = child
                path.append(node)
                break
            best = -1e18
            arg = 1
            for k in range(1, top + 1):
                ch = node[3][k]
                s = ch[2] / ch[1] + c * math.sqrt(math.log(max(node[1], 1)) / ch[1])
                if s > best + 1e-12:
                    best = s
                    arg = k
            node = node[3][arg]
            path.append(node)
        # simulation: result for the player who moved into the last node
        pile = node[0]
        if pile == 0:
            r = 1
        else:
            mover = 1  # 1 = the player to move at the node (not the one who moved into it)
            last = 0
            while pile > 0:
                x = (75 * x + 74) % 65537
                top = 3 if pile >= 3 else pile
                pile -= 1 + x % top
                last = mover
                mover = 1 - mover
            # last == 1 means the player to move at the node took the last stone
            r = 0 if last == 1 else 1
        for i in range(len(path) - 1, -1, -1):
            path[i][1] += 1
            path[i][2] += r
            r = 1 - r
    best = -1
    arg = 1
    for k in sorted(root[3].keys()):
        if root[3][k][1] > best:
            best = root[3][k][1]
            arg = k
    return arg
""", [[5, 300, 1.0, 1], [6, 300, 1.0, 7], [8, 400, 1.0, 3], [10, 400, 1.0, 11], [4, 200, 1.0, 5]], "Follow the description exactly; the same generator makes it repeatable."),
  ORDER("A search", "Order the steps.", ["Create the root node", "Run the four steps many times", "Stop when the budget is used", "Look at the root's children", "Play the most visited move"]),
  MATCH("UCT", "Match each term with its meaning.", [("C", "Exploration weight"), ("Most visits", "Robust final choice"), ("Budget", "Number of iterations"), ("Subtree reuse", "Keep the played branch"), ("Convergence", "Approaches minimax")]),
  FILL("Search", "UCT picks the child with the highest mean plus an exploration {{bonus}}; at the end we play the most {{visited}} child.")]))

CHS.append(CH(
 "Choosing the final move",
 ("Final move", [
  "Max child | has | Highest mean",
  "Robust child | has | Most visits",
  "Max-robust child | has | Both",
  "Secure child | maximises | A lower bound",
  "Ties | broken by | Rule",
  "Few visits | mean | Unreliable",
  "Most visits | is | The usual choice"]),
 ["After the iterations, the program must pick a move from the root's children. The survey lists several criteria. The max child has the highest mean reward. The robust child has the highest visit count. The max-robust child is the one with both, and if none exists the search continues. The secure child maximises a lower confidence bound.",
  "The mean of a barely visited child is unreliable: a single lucky playout can make it look perfect. Visit counts are steadier, so the robust child is the usual choice.",
  "The labs implement each criterion and show where they disagree."],
 [("Max child", "The child with the highest mean reward."),
  ("Robust child", "The child with the most visits."),
  ("Max-robust child", "A child that is both max and robust."),
  ("Secure child", "The child maximising mean minus a multiple of its standard error."),
  ("Lower confidence bound", "A pessimistic estimate: mean minus a margin."),
  ("Tie-breaking", "A fixed rule for equal scores.")],
 ["Robust child: argmax visits.",
  "Max child: argmax mean.",
  "Secure child: argmax of mean - A / sqrt(n) for a constant A.",
  "A child with 1 visit and mean 1.0 is not trustworthy.",
  "UCT concentrates visits on good moves, so max and robust usually agree after many iterations.",
  "Disagreement signals that more iterations are needed."],
 [T("Suppose the search ends with three candidate moves. Move A: 900 visits, mean 0.62. Move B: 80 visits, mean 0.70. Move C: 3 visits, mean 1.00. Which to play?"),
  T("The max child is C, with the highest mean. But three playouts prove little: the true win rate could be well below one half. The robust child is A, the most visited. UCT only keeps visiting a move while it looks competitive, so a large visit count is evidence that the move held up under pressure. A is the usual choice."),
  M(r"\text{robust: } \arg\max_a N(a), \qquad \text{max: } \arg\max_a \frac{W(a)}{N(a)}, \qquad \text{secure: } \arg\max_a \left(\frac{W(a)}{N(a)} - \frac{A}{\sqrt{N(a)}}\right)"),
  T("The secure child penalises uncertainty explicitly. Subtract from the mean a margin that shrinks with the number of visits. With a suitable A, move C is penalised heavily and move A scores best again. The survey mentions this among the options and describes the bound as a lower confidence bound."),
  T("When max and robust children differ, a common remedy is to keep searching until they agree, which is the idea behind the max-robust child. Some programs extend the thinking time when the best move is unclear, and cut it short when it is obvious."),
  T("A last practical point is ties. Several children can have the same visit count, particularly in short searches. Pick by a fixed rule such as the highest mean, then the lowest index, so that behaviour is repeatable.")],
 [("Which child is robust?", ["The most visited", "The highest mean", "The first", "The last"], 0, "Steadier evidence."),
  ("Why distrust a child with 3 visits?", ["Its mean is unreliable", "It is illegal", "It is slow", "It is deep"], 0, "Few samples."),
  ("What does a secure child do?", ["Penalises uncertainty", "Ignores counts", "Maximises visits only", "Picks at random"], 0, "Lower confidence bound."),
  ("What if max and robust disagree?", ["Keep searching", "Stop", "Play at random", "Resign"], 0, "The max-robust idea.")],
 [("Which is the usual choice?", "The robust child."), ("What is a lower confidence bound?", "Mean minus a margin."), ("Can max and robust agree?", "Usually, after many iterations."), ("What breaks ties?", "A fixed rule.")],
 [PL("Robust child", "Write robust_child(stats): stats is a list of [move, visits, total]; return the move with the most visits (ties to the highest mean, then the lowest move).",
     "robust_child(stats)", """
def robust_child(stats):
    best = None
    for move, n, w in stats:
        m = w / n if n > 0 else 0.0
        key = (n, m)
        if best is None or n > best[0] or (n == best[0] and m > best[1] + 1e-12):
            best = (n, m, move)
    return best[2]
""", [[[[1, 900, 558], [2, 80, 56], [3, 3, 3]]], [[[1, 10, 5], [2, 10, 6]]], [[[1, 10, 5], [2, 10, 5]]], [[[3, 1, 1]]]], "Compare visits, then the mean."),
  PL("Max child", "Write max_child(stats): the move with the highest mean total/visits (visits above 0), ties to the lowest move.",
     "max_child(stats)", """
def max_child(stats):
    best = -1.0
    arg = stats[0][0]
    for move, n, w in stats:
        if n > 0:
            m = w / n
            if m > best + 1e-12:
                best = m
                arg = move
    return arg
""", [[[[1, 900, 558], [2, 80, 56], [3, 3, 3]]], [[[1, 10, 5], [2, 10, 6]]], [[[1, 4, 2], [2, 4, 2]]], [[[5, 0, 0], [6, 2, 1]]]], "Highest mean."),
  PL("Secure child", "Write secure_child(stats, a): the move maximising mean - a / sqrt(visits) (visits above 0), ties to the lowest move. Use import math.",
     "secure_child(stats, a)", """
import math
def secure_child(stats, a):
    best = -1e18
    arg = stats[0][0]
    for move, n, w in stats:
        if n > 0:
            s = w / n - a / math.sqrt(n)
            if s > best + 1e-12:
                best = s
                arg = move
    return arg
""", [[[[1, 900, 558], [2, 80, 56], [3, 3, 3]], 1.0], [[[1, 900, 558], [2, 80, 56], [3, 3, 3]], 0.0], [[[1, 100, 60], [2, 100, 61]], 1.0], [[[1, 4, 4], [2, 400, 300]], 1.0]], "A pessimistic score."),
  PL("Do they agree?", "Write agree(stats): 1 if the robust child (most visits, ties to the highest mean then lowest move) and the max child (highest mean, ties to the lowest move) are the same move, otherwise 0.",
     "agree(stats)", """
def agree(stats):
    best = None
    for move, n, w in stats:
        m = w / n if n > 0 else 0.0
        if best is None or n > best[0] or (n == best[0] and m > best[1] + 1e-12):
            best = (n, m, move)
    rob = best[2]
    bm = -1.0
    mx = stats[0][0]
    for move, n, w in stats:
        if n > 0:
            m = w / n
            if m > bm + 1e-12:
                bm = m
                mx = move
    return 1 if rob == mx else 0
""", [[[[1, 900, 558], [2, 80, 56], [3, 3, 3]]], [[[1, 10, 7], [2, 5, 2]]], [[[1, 10, 5], [2, 10, 6]]], [[[1, 1, 1]]]], "Compare the two choices."),
  ORDER("Choosing a move", "Order the steps.", ["Finish the search iterations", "Read visits and means of root children", "Distrust means with few visits", "Pick the most visited child", "Play that move"]),
  MATCH("Criteria", "Match each criterion with its rule.", [("Max child", "Highest mean"), ("Robust child", "Most visits"), ("Secure child", "Best lower bound"), ("Max-robust", "Both agree"), ("Tie-break", "Fixed rule")]),
  FILL("Choice", "The {{robust}} child has the most visits; a child with few visits has an unreliable {{mean|average}}.")]))

CHS.append(CH(
 "Enhancements: RAVE, priors, widening and more",
 ("Variants", [
  "RAVE | shares | Move statistics across the tree",
  "AMAF | counts | Moves played anywhere later",
  "First-play urgency | values | Unvisited children",
  "Progressive widening | limits | Children by visits",
  "Heuristic playouts | replace | Uniform random",
  "Transposition table | merges | Equal positions",
  "Parallel MCTS | uses | Virtual loss"]),
 ["Plain UCT is slow to learn in big games. The survey describes many enhancements. All-moves-as-first, AMAF, and its tree version RAVE share information between positions: a move that did well when played later in a playout is probably good now.",
  "Other ideas: give unvisited children a first-play urgency value; widen the set of considered moves gradually as the node gets more visits; use domain knowledge or a policy to bias playouts; merge identical positions in a transposition table; and run many threads using virtual loss.",
  "These are from the survey and later work; the labs implement three of the simplest."],
 [("AMAF", "All moves as first: credit a move when it appears anywhere later in the playout."),
  ("RAVE", "Rapid Action Value Estimation: blends AMAF and ordinary statistics in the tree."),
  ("First-play urgency", "A value assigned to unvisited children in place of infinity."),
  ("Progressive widening", "Allow only a growing number of children as the parent's visits increase."),
  ("Transposition", "Different move orders reaching the same position."),
  ("Virtual loss", "A temporary penalty that steers parallel threads to different branches.")],
 ["AMAF/RAVE: from Gelly and Silver's work on Go, described in the survey.",
  "RAVE blends: beta * AMAF mean + (1 - beta) * ordinary mean, with beta falling as visits grow.",
  "First-play urgency: unvisited children get a fixed score instead of infinity.",
  "Progressive widening: allowed children = ceil(k * visits^alpha).",
  "Heuristic or learned playout policies play better than uniform random.",
  "Parallelisation: tree parallelism with virtual loss, leaf or root parallelism."],
 [T("Plain UCT treats every position separately. In Go, with hundreds of moves, a large number of playouts is needed before any move has enough statistics. The enhancements make better use of each playout."),
  T("All-moves-as-first is the best known idea. In a playout, a move that appears later may have helped even though it was not played at the root. AMAF credits every move that either side played later in the playout, as though it had been played first. This gives many more samples per move, though noisier ones. RAVE combines the AMAF estimate with the ordinary estimate, trusting AMAF early and the ordinary mean as visits accumulate."),
  M(r"Q_{\mathrm{RAVE}}(a) \;=\; \beta\, Q_{\mathrm{AMAF}}(a) + (1-\beta)\, Q(a), \qquad \beta \text{ falls as } N(a) \text{ grows}"),
  T("The unvisited-children rule matters too. Plain UCT gives an unvisited child an infinite score, so every child is tried once before any is tried twice. With 250 moves that costs 250 playouts at every node. First-play urgency instead gives an unvisited child a fixed value, so a good known move can be revisited before all the others are tried."),
  T("Progressive widening handles very large or continuous move sets. At first only a few children are allowed. As the parent's visit count rises, more are allowed, usually in proportion to a power of the visit count. The best-looking moves, by a heuristic, are added first."),
  T("Domain knowledge helps in playouts. Instead of uniformly random moves, a heuristic policy might prefer captures or local replies. A stronger default policy gives better estimates, though not always: the survey notes that a stronger playout policy does not guarantee a stronger search. Later systems replaced playouts with learned value estimates. That is the step AlphaGo took."),
  T("Finally, parallelism. Several threads can share the tree. Virtual loss temporarily counts a visit as a loss on the path being explored, which discourages other threads from following it. The labs implement an AMAF update, first-play urgency and progressive widening.")],
 [("What does AMAF credit?", ["Moves played later in the playout", "Only the first move", "The terminal state", "Illegal moves"], 0, "As if they had been played first."),
  ("What does first-play urgency replace?", ["Infinite score for unvisited children", "The playout", "The root", "The rules"], 0, "A fixed value."),
  ("What does progressive widening do?", ["Allows more children as visits grow", "Prunes the tree", "Adds noise", "Doubles C"], 0, "ceil(k visits^alpha)."),
  ("What is virtual loss for?", ["Steering parallel threads apart", "Lowering the score of winners", "Saving memory", "Ending the search"], 0, "A temporary penalty.")],
 [("What does RAVE blend?", "AMAF and ordinary means."), ("Which sources describe these?", "The 2012 survey."), ("Why widen gradually?", "Huge move sets."), ("What replaced playouts in AlphaGo?", "A value network.")],
 [PL("AMAF update", "A playout is a list of moves played in order (both sides). Write amaf_update(table, playout, result): table is a list of [move, count, total]; for every move appearing in the playout, add 1 to its count and add result to its total (once per move even if it appears twice). Return the updated table.",
     "amaf_update(table, playout, result)", """
def amaf_update(table, playout, result):
    seen = []
    for m in playout:
        if m not in seen:
            seen.append(m)
    out = []
    for move, n, w in table:
        if move in seen:
            out.append([move, n + 1, w + result])
        else:
            out.append([move, n, w])
    return out
""", [[[[1, 0, 0], [2, 0, 0], [3, 0, 0]], [1, 3, 1], 1], [[[1, 2, 1], [2, 2, 2]], [2], 0], [[[1, 0, 0]], [], 1], [[[1, 1, 1], [2, 1, 0]], [1, 2], 1]], "Credit each distinct move once."),
  PL("RAVE blend", "Write rave_value(q_amaf, q_tree, n, k): beta = sqrt(k / (3 * n + k)); return beta * q_amaf + (1 - beta) * q_tree (n is the visit count, k an equivalence parameter). Use import math.",
     "rave_value(q_amaf, q_tree, n, k)", """
import math
def rave_value(q_amaf, q_tree, n, k):
    beta = math.sqrt(k / (3 * n + k))
    return beta * q_amaf + (1 - beta) * q_tree
""", [[0.6, 0.4, 0, 100], [0.6, 0.4, 100, 100], [0.6, 0.4, 10000, 100], [0.2, 0.9, 5, 50]], "Beta falls as n grows.", approx=1e-9),
  PL("Progressive widening", "Write allowed_children(visits, k, alpha): the number of children allowed, ceil(k * visits ** alpha) but at least 1. Use import math.",
     "allowed_children(visits, k, alpha)", """
import math
def allowed_children(visits, k, alpha):
    v = int(math.ceil(k * (visits ** alpha) - 1e-9))
    return max(1, v)
""", [[1, 1, 0.5], [4, 1, 0.5], [100, 1, 0.5], [0, 2, 0.5], [9, 2, 0.5]], "Round up, minimum 1."),
  PL("First-play urgency", "Write fpu_select(children, parent_n, c, fpu): children is a list of [move, visits, total]; an unvisited child has score fpu, others w/n + c*sqrt(ln(parent_n)/n). Return the move with the highest score (ties to the lowest index). Use import math.",
     "fpu_select(children, parent_n, c, fpu)", """
import math
def fpu_select(children, parent_n, c, fpu):
    best = -1e18
    arg = children[0][0]
    for move, n, w in children:
        if n == 0:
            s = fpu
        else:
            s = w / n + c * math.sqrt(math.log(parent_n) / n)
        if s > best + 1e-12:
            best = s
            arg = move
    return arg
""", [[[[1, 10, 8], [2, 0, 0], [3, 10, 5]], 20, 1.0, 0.5], [[[1, 10, 8], [2, 0, 0]], 20, 1.0, 2.0], [[[1, 10, 8], [2, 0, 0]], 20, 0.5, 0.9], [[[1, 0, 0], [2, 0, 0]], 5, 1.0, 1.0]], "Use the fixed value for unvisited children."),
  ORDER("Using RAVE", "Order the steps.", ["Play a random game to the end", "List the moves played in it", "Credit each distinct move with the result", "Blend AMAF and tree means", "Select with the blended value"]),
  MATCH("Enhancements", "Match each enhancement with its idea.", [("AMAF", "Credit moves played later"), ("RAVE", "Blend AMAF with tree means"), ("First-play urgency", "Finite value for unvisited"), ("Progressive widening", "More children as visits grow"), ("Virtual loss", "Steer parallel threads")]),
  FILL("Variants", "{{RAVE}} blends AMAF with tree statistics, and progressive {{widening}} grows the child set.")]))

CHS.append(CH(
 "Two players, perspective and heuristics",
 ("Two-player search", [
  "Perspective | flips | Each ply",
  "Negamax | uses | One sign convention",
  "Draws | count as | One half",
  "Score games | need | Normalised rewards",
  "MCTS | resembles | Selective minimax",
  "Minimax | prunes | With alpha-beta",
  "Playout bias | is | A risk"]),
 ["Two-player games need care with perspective. A node should store results from the viewpoint of the player who moved into it, and the reward flips at every level. Draws score one half.",
  "MCTS is often seen as a selective, sampled version of minimax: the mean values in the tree approach minimax values, while the tree grows deeper along strong lines.",
  "Compared with alpha-beta, MCTS shines when evaluation functions are hard to write and branching is large; alpha-beta shines when a good evaluation function exists and tactics are narrow."],
 [("Perspective", "The player from whose viewpoint a reward is measured."),
  ("Negamax", "A form of minimax where each level negates the value."),
  ("Alpha-beta", "A pruning method that skips branches that cannot affect the minimax result."),
  ("Evaluation function", "A hand-written estimate of a position's value."),
  ("Normalised reward", "A reward scaled into the range 0 to 1."),
  ("Trap", "A position where one precise move refutes an attractive line.")],
 ["Win = 1, draw = 0.5, loss = 0 from the perspective of the player who moved into the node.",
  "Backup: r for the leaf's mover; 1 - r for the other player, alternating.",
  "MCTS needs no evaluation function; alpha-beta usually does.",
  "Alpha-beta prunes exactly; MCTS focuses statistically.",
  "MCTS can be weak in narrow tactical lines with traps.",
  "Hybrid systems exist; AlphaGo-style systems mix MCTS with learned networks."],
 [T("In a two-player game, one side's gain is the other's loss. That structure has to be respected in the tree. At a node where the opponent is to move, the opponent will pick the child that is best for them, which is worst for us. If the node stores the result from the viewpoint of whoever moved into it, the choice at the parent is always a plain maximisation over children, one level at a time."),
  M(r"r_{\mathrm{opp}} \;=\; 1 - r_{\mathrm{me}}, \qquad \text{win} = 1,\ \ \text{draw} = \tfrac12,\ \ \text{loss} = 0"),
  T("This is the zero-sum symmetry. With scores that are not wins and losses, such as points, the common approach is to scale them into the range zero to one so that the same bandit rule applies, and to treat a draw as one half."),
  T("How does MCTS relate to the classical alternative? Alpha-beta search explores the game tree to a fixed depth with pruning, then calls an evaluation function. Its results are exact for that depth. MCTS explores unevenly, with no fixed depth, and uses playouts in place of an evaluation function. Its values are statistical. The tree-wide averages tend to minimax values as iterations grow."),
  T("Which is better depends on the game. Chess has good hand-made evaluation functions and many narrow tactical lines, a good fit for alpha-beta. Go has huge branching and no good evaluation function, a good fit for MCTS. Where lines are very narrow, a single refutation can be missed by sampling. The survey describes such trap states as a weakness of plain MCTS."),
  T("Bias in the playouts is a further risk. If the default policy is biased, so are the estimates. Domain knowledge can help and can also hurt. A broader point: since 2016, programs such as AlphaGo and AlphaZero keep the MCTS tree but evaluate leaves with neural networks and steer selection with a learned policy, as described in the sister courses.")],
 [("How are draws scored?", ["One half", "Zero", "One", "Minus one"], 0, "Between win and loss."),
  ("What does a node's stored reward represent?", ["The viewpoint of the player who moved into it", "A fixed player", "The loser", "Time"], 0, "So parents maximise."),
  ("When is MCTS especially useful?", ["Large branching with no good evaluation function", "Tiny games", "Fully solved games", "Single-move games"], 0, "Like Go."),
  ("What is a trap?", ["One precise reply refutes an attractive move", "A random move", "A draw", "A repeated state"], 0, "Sampling can miss it.")],
 [("What is negamax?", "Minimax with a sign flip."), ("What does alpha-beta need?", "Usually an evaluation function."), ("Which is exact?", "Alpha-beta to its depth."), ("Which is statistical?", "MCTS.")],
 [PL("Flip the result", "Write backup_values(depth, result): the reward for each node on a path of depth nodes (root first), where the last node gets result and its parent 1 - result, alternately. Return the list from root to last.",
     "backup_values(depth, result)", """
def backup_values(depth, result):
    out = []
    for i in range(depth):
        steps = depth - 1 - i
        out.append(result if steps % 2 == 0 else 1 - result)
    return out
""", [[3, 1], [4, 0], [1, 1], [5, 0.5]], "Count steps from the last node.", approx=1e-12),
  PL("Score a game", "Write game_score(winner, me): 1 if winner == me, 0.5 if winner is 'draw', else 0.",
     "game_score(winner, me)", """
def game_score(winner, me):
    if winner == 'draw':
        return 0.5
    return 1 if winner == me else 0
""", [['a', 'a'], ['b', 'a'], ['draw', 'a'], ['draw', 'b']], "Three cases.", approx=1e-12),
  PL("Negamax on Nim", "Write negamax(n): the exact value for the player to move in Nim with n stones: +1 if the player to move wins and -1 if loses, computed by negamax: value(0) = -1; otherwise the maximum over takes k of -value(n - k).",
     "negamax(n)", """
def negamax(n):
    if n == 0:
        return -1
    best = -2
    for k in range(1, 4):
        if k <= n:
            v = -negamax(n - k)
            if v > best:
                best = v
    return best
""", [[0], [1], [4], [5], [8], [9], [12]], "One recursion with a negation."),
  PL("Normalise a score", "Write normalise(score, lo, hi): scale a score from [lo, hi] into [0, 1], that is (score - lo) / (hi - lo).",
     "normalise(score, lo, hi)", """
def normalise(score, lo, hi):
    return (score - lo) / (hi - lo)
""", [[5, 0, 10], [0, -1, 1], [50, 0, 100], [3, 3, 7]], "Linear scaling.", approx=1e-12),
  ORDER("Backing up a result", "Order the steps for a two-player game.", ["Find the result for the last node's mover", "Store it at the last node", "Give the parent one minus the result", "Alternate going up", "Update the visit counts too"]),
  MATCH("Two players", "Match each idea with its meaning.", [("Perspective flip", "Reward alternates by level"), ("Draw", "0.5"), ("Alpha-beta", "Exact pruned search"), ("Negamax", "Sign-flipped minimax"), ("Trap", "Sampling may miss it")]),
  FILL("Two players", "At each level of the tree the reward flips to one {{minus|-}} the result, and a draw counts as {{one half|0.5|half}}.")]))

CHS.append(CH(
 "Applications, limits and where it leads",
 ("Beyond games", [
  "MCTS | conquered | Computer Go",
  "MCTS | used in | General game playing",
  "MCTS | used in | Planning and scheduling",
  "Limits | include | Traps",
  "Limits | include | Sparse rewards",
  "AlphaGo | combined | MCTS and networks",
  "Next | is | Learned search"]),
 ["MCTS was the breakthrough behind the strong Go programs of 2006 to 2015 and then became a general tool: in video games, general game playing, planning, scheduling and optimisation problems. The survey lists applications across games and non-game domains.",
  "It has weak spots. Traps can fool it; very long games with sparse rewards give little signal; the cost per iteration limits depth. Remedies include better playouts, learned priors and learned values.",
  "The modern line of work, AlphaGo, AlphaZero and MuZero, keeps the tree search and replaces random playouts by learned networks."],
 [("General game playing", "Playing any game given only its rules."),
  ("Sparse reward", "A signal that appears only at the very end."),
  ("PUCT", "A UCT variant that adds a prior probability from a neural network."),
  ("MuZero", "A system that also learns a model of the environment for the search."),
  ("Planning", "Choosing actions by looking ahead in a model."),
  ("Learned value", "A neural network estimate of a position's value, used instead of a playout.")],
 ["Go programs using MCTS reached strong amateur level before 2015.",
  "The survey covers games and non-game domains such as planning and scheduling.",
  "Weaknesses: traps, long sparse-reward horizons, memory growth.",
  "PUCT adds a policy prior to the selection rule.",
  "AlphaGo (2016) and AlphaZero (2017) combine MCTS with deep networks.",
  "MCTS needs a model of the environment, or a learned one as in MuZero."],
 [T("Before 2006, the best Go programs played at the level of a modest club player. With MCTS, programs climbed to strong amateur level within a few years, long before neural networks were available, which is why the method became famous. It was the first reliable way to handle the huge branching of Go."),
  T("The method spread. General game playing programs, which are given only the rules of a new game, adopted it because it needs no hand-made evaluation. Video games, planning problems, scheduling and optimisation tasks followed, as the survey documents. Wherever you have a simulator and a decision tree, MCTS is a candidate."),
  T("It has limits you should know. Traps, as in chapter 9, can be missed. When a game is long and the only reward comes at the end, random playouts have little signal. Each iteration costs a playout, so depth is limited. And memory grows with the tree. Remedies include better default policies, domain heuristics and early cut-offs with an evaluation."),
  M(r"a^{*} \;=\; \arg\max_a \left( Q(s,a) + c\, P(s,a)\,\frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \right)"),
  T("The formula above is PUCT, the selection rule of AlphaGo and AlphaZero: the exploration bonus is scaled by a prior probability P from a policy network, so the search tries promising moves first. Leaves are scored by a value network instead of a random playout. The tree, the four steps and the visit-count choice stay. That is why knowing MCTS makes those systems easy to read."),
  T("MuZero goes one step further by learning the model of the environment as well, so that the tree can search where the rules are not given. You will find the details in the courses on AlphaGo and AlphaZero in this library."),
  T("Where to go next: read the Browne survey for the long list of variants, implement MCTS for a game of your choice such as tic-tac-toe or Connect Four, and compare it with your own alpha-beta program. In the labs, you will build the pieces of the PUCT rule, measure tree statistics and write a simple tournament.")],
 [("Where was MCTS a breakthrough?", ["Computer Go", "Sorting", "Compilers", "Networking"], 0, "From 2006."),
  ("What does PUCT add?", ["A prior from a policy network", "A random move", "A bigger tree", "A timer"], 0, "Used by AlphaGo."),
  ("What is a weakness of MCTS?", ["Traps and sparse rewards", "It cannot be stopped", "It needs an evaluation function", "It is exact"], 0, "Also memory and playout cost."),
  ("What does MCTS need?", ["A model of the environment", "A labelled dataset", "A GPU", "A human opponent"], 0, "Rules or a learned model.")],
 [("What replaced playouts in AlphaGo?", "A value network."), ("What does the prior do?", "Guides which moves to try first."), ("Is MCTS limited to games?", "No."), ("What is MuZero?", "MCTS with a learned model.")],
 [PL("PUCT score", "Write puct(q, p, n_child, n_parent, c): q + c * p * sqrt(n_parent) / (1 + n_child). Use import math.",
     "puct(q, p, n_child, n_parent, c)", """
import math
def puct(q, p, n_child, n_parent, c):
    return q + c * p * math.sqrt(n_parent) / (1 + n_child)
""", [[0.5, 0.3, 0, 10, 1.0], [0.5, 0.3, 9, 10, 1.0], [0.0, 1.0, 0, 100, 2.0], [0.7, 0.1, 5, 50, 1.5]], "Prior-scaled exploration.", approx=1e-9),
  PL("Tree statistics", "Write tree_stats(parents): parents is a list where parents[i] is the parent index of node i (the root has -1). Return [number of nodes, depth of the deepest node (root depth 0), number of leaves].",
     "tree_stats(parents)", """
def tree_stats(parents):
    n = len(parents)
    depth = [0] * n
    for i in range(n):
        d = 0
        j = i
        while parents[j] != -1:
            j = parents[j]
            d += 1
        depth[i] = d
    has_child = [0] * n
    for i in range(n):
        if parents[i] != -1:
            has_child[parents[i]] = 1
    leaves = n - sum(has_child)
    return [n, max(depth), leaves]
""", [[[-1, 0, 0, 1, 1]], [[-1]], [[-1, 0, 1, 2, 3]], [[-1, 0, 0, 0]]], "Follow parents to the root."),
  PL("Branching of the tree", "Write avg_branching(parents): the average number of children of the nodes that have at least one child (0 if none).",
     "avg_branching(parents)", """
def avg_branching(parents):
    cnt = {}
    for p in parents:
        if p != -1:
            cnt[p] = cnt.get(p, 0) + 1
    if len(cnt) == 0:
        return 0
    return sum(cnt.values()) / len(cnt)
""", [[[-1, 0, 0, 1, 1]], [[-1]], [[-1, 0, 1, 2]], [[-1, 0, 0, 0, 1]]], "Count children per parent.", approx=1e-12),
  PL("Win share", "A tournament result is a list of 'a', 'b' or 'draw'. Write share_a(results): player a's score share, (wins + 0.5 draws) / games (0 for an empty list).",
     "share_a(results)", """
def share_a(results):
    if len(results) == 0:
        return 0
    s = 0.0
    for r in results:
        if r == 'a':
            s += 1
        elif r == 'draw':
            s += 0.5
    return s / len(results)
""", [[['a', 'a', 'b', 'draw']], [[]], [['b', 'b']], [['draw', 'draw']]], "Draws count half.", approx=1e-12),
  ORDER("From MCTS to AlphaGo", "Order the idea's development.", ["Random playouts for evaluation", "A bandit rule for selection (UCT)", "Strong Go programs from MCTS", "Policy priors in selection (PUCT)", "Value networks in place of playouts"]),
  MATCH("Landmarks", "Match each name with its contribution.", [("Coulom", "Named MCTS"), ("Kocsis and Szepesvari", "UCT"), ("Auer et al.", "UCB1"), ("Browne et al.", "The survey"), ("AlphaGo", "MCTS plus deep networks")]),
  FILL("Legacy", "AlphaGo kept the {{tree}} search and replaced random playouts with a {{value}} network.")]))
