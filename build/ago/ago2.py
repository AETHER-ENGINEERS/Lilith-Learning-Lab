"""AlphaGo course, chapters 5-8."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 5
CHS.append(CH(
 "Learning from experts: the SL policy network",
 ("Supervised learning", [
  "Expert games | provide | Position and move pairs",
  "SL policy network | predicts | The expert's move",
  "Cross-entropy | measures | Prediction error",
  "Gradient ascent | maximizes | Log likelihood",
  "KGS Go Server | supplied | 30 million positions",
  "Accuracy | reached | 57.0 percent",
  "Fast and slow | trade | Accuracy for speed"]),
 ["The first training stage is plain supervised learning. Take positions from games played by strong humans on the KGS Go Server, and train the network to give high probability to the move the expert actually played.",
  "The training signal is the log likelihood of the human move: the weights are nudged in the direction that makes that move more probable. In the paper, a 13-layer network trained on 30 million positions predicted the expert move 57.0 percent of the time, against 44.4 percent for the previous best.",
  "The labs write the loss, its gradient and a full tiny training loop for a linear softmax model."],
 [("Supervised learning", "Learning to predict labels, here the expert's move for each position."),
  ("Cross-entropy", "The loss minus the log of the probability given to the correct label."),
  ("Log likelihood", "The log of the probability the model assigned to the data."),
  ("Gradient", "The direction in which a function increases fastest."),
  ("Top-1 accuracy", "How often the highest-probability move equals the expert's move."),
  ("Overfitting", "Fitting training data but failing on new data.")],
 ["The SL policy network is trained to maximize the log likelihood of the human move.",
  "Update: delta sigma is proportional to the gradient of log p_sigma(a | s) with respect to sigma.",
  "For softmax outputs, the gradient of -log p_a with respect to the logits is p - onehot(a).",
  "The paper: 13 layers, 30 million positions, 57.0 percent accuracy (55.7 percent from raw board and history only).",
  "The earlier state of the art was 44.4 percent.",
  "A stronger accuracy gave much stronger play, though the network was slower to evaluate."],
 [T("Stage one of AlphaGo is imitation. The training data are positions from the KGS Go Server, a site where strong amateurs play. The paper says the data set held 29.4 million positions from 160,000 games. For each position the label is the move the player actually chose, one of 361 points."),
  T("The network gives a probability for each point. The natural loss is the negative log of the probability given to the human move, called cross-entropy. If the network is sure about the right move the loss is near zero. If it gives the move a tiny probability the loss is large."),
  M(r"L(\sigma) \;=\; -\log p_{\sigma}(a \mid s)"),
  T("To train, compute the gradient of the loss and take a small step the other way. For the final softmax layer there is a neat result. The gradient of minus log p of the correct action with respect to the scores, the logits, is just the vector of predicted probabilities minus a one-hot vector for the correct action. A move that was too unlikely gets pushed up and every other move gets pushed down in proportion to its probability."),
  T("The paper trained with stochastic gradient ascent on the log likelihood, which is the same thing as descent on the loss. After training, the 13-layer network predicted the expert move correctly 57.0 percent of the time using all features, and 55.7 percent with only the board and move history. The best earlier result the paper cites was 44.4 percent. That sounds modest, but there are 361 candidate points and humans disagree with themselves."),
  T("A key finding was that small gains in accuracy led to large gains in playing strength. Bigger networks were more accurate but slower to evaluate. The network's evaluation took a few milliseconds, which is why the paper also trains a much faster, weaker policy for rollouts, the subject of the next chapter."),
  T("Imitation has a ceiling. A network trained to copy humans plays like a blend of the humans in its data. To go beyond them, the paper adds a second stage in which the network improves through self-play, chapter 7. But the SL network remains useful in the final search. The paper reports that the SL policy gives better priors to the tree search than the stronger RL policy, perhaps because humans pick a diverse set of promising moves while RL tunes onto a single best move."),
  T("The practice section writes cross-entropy, the accuracy metrics, the softmax gradient, one training step for a linear softmax model and a small training loop.")],
 [("What does the SL policy network learn to predict?", ["The expert's move", "The winner", "The komi", "The rules"], 0, "Imitation of human games."),
  ("What is the gradient of -log p_a with respect to the logits?", ["p minus a one-hot vector", "p times 2", "Zero", "The board"], 0, "Pushes the right move up."),
  ("What accuracy did the SL network reach?", ["57.0 percent", "99 percent", "10 percent", "24.2 percent"], 0, "With all input features."),
  ("Where did the training positions come from?", ["The KGS Go Server", "Chess databases", "Random play", "Self-play"], 0, "Strong human amateur games.")],
 [("Why not stop at supervised learning?", "It only imitates the humans in its data."), ("What does top-1 accuracy measure?", "How often the best guess is the expert move."), ("What is overfitting?", "Memorizing the training data."),
  ("Which gave better search priors, SL or RL?", "The SL policy, according to the paper.")],
 [PL("Cross-entropy", "Write cross_entropy(p, a): minus the natural log of p[a]. Use import math.",
     "cross_entropy(p, a)", """
import math
def cross_entropy(p, a):
    return -math.log(p[a])
""", [[[0.5, 0.5], 0], [[0.9, 0.05, 0.05], 0], [[0.9, 0.05, 0.05], 2], [[0.25, 0.25, 0.25, 0.25], 3], [[1.0], 0]], "Look up the probability of the correct move and take -log.", approx=1e-9),
  PL("Top-k accuracy", "Write topk_accuracy(rows, labels, k): rows is a list of probability lists, labels the expert move for each. Return the fraction of rows where the label is among the k highest-probability moves (ties go to the lower index).",
     "topk_accuracy(rows, labels, k)", """
def topk_accuracy(rows, labels, k):
    hit = 0
    for p, a in zip(rows, labels):
        order = sorted(range(len(p)), key=lambda i: (-p[i], i))
        if a in order[:k]:
            hit += 1
    return hit / len(rows)
""", [[[[0.6, 0.3, 0.1], [0.2, 0.5, 0.3], [0.1, 0.1, 0.8]], [0, 2, 2], 1], [[[0.6, 0.3, 0.1], [0.2, 0.5, 0.3], [0.1, 0.1, 0.8]], [1, 0, 1], 2], [[[0.5, 0.5]], [1], 1], [[[0.4, 0.4, 0.2]], [1], 2]], "Sort move indices by probability and check the top k.", approx=1e-9),
  PL("Softmax gradient", "Write logit_grad(p, a): the gradient of -log p[a] with respect to the logits, that is p with 1 subtracted at position a.",
     "logit_grad(p, a)", """
def logit_grad(p, a):
    g = list(p)
    g[a] = g[a] - 1.0
    return g
""", [[[0.5, 0.5], 0], [[0.2, 0.3, 0.5], 2], [[1.0], 0], [[0.1, 0.9], 0]], "Copy p and subtract one at the label.", approx=1e-12),
  PL("One training step", "A linear softmax model has weights W (a list of rows, one per move, each of the same length as the feature vector x). Write sgd_step(W, x, a, lr): compute logits z_i = sum_j W[i][j] * x[j], p = softmax(z), and return the new weights W[i][j] - lr * (p[i] - onehot[i]) * x[j]. Use import math.",
     "sgd_step(W, x, a, lr)", """
import math
def sgd_step(W, x, a, lr):
    z = []
    for row in W:
        z.append(sum(w * v for w, v in zip(row, x)))
    m = max(z)
    e = [math.exp(t - m) for t in z]
    s = sum(e)
    p = [t / s for t in e]
    out = []
    for i in range(len(W)):
        target = 1.0 if i == a else 0.0
        out.append([W[i][j] - lr * (p[i] - target) * x[j] for j in range(len(x))])
    return out
""", [[[[0.0, 0.0], [0.0, 0.0]], [1.0, 2.0], 0, 0.5], [[[0.1, 0.2], [0.3, 0.4], [0.0, 0.0]], [1.0, 0.0], 2, 0.1], [[[1.0]], [2.0], 0, 0.3], [[[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]], [1.0, 1.0, 1.0], 1, 1.0]], "The gradient of each weight is (p_i - target_i) times x_j.", approx=1e-9),
  PL("A tiny training loop", "Train a linear softmax model with zero initial weights on the examples (xs[i] features, ys[i] label) for the given number of epochs (one pass over the examples in order is one epoch, one step per example, learning rate lr). Return the accuracy on the same examples as a fraction. Write train_accuracy(xs, ys, n_moves, epochs, lr).",
     "train_accuracy(xs, ys, n_moves, epochs, lr)", """
import math
def train_accuracy(xs, ys, n_moves, epochs, lr):
    d = len(xs[0])
    W = [[0.0] * d for i in range(n_moves)]
    def probs(x):
        z = [sum(w * v for w, v in zip(row, x)) for row in W]
        m = max(z)
        e = [math.exp(t - m) for t in z]
        s = sum(e)
        return [t / s for t in e]
    for ep in range(epochs):
        for x, y in zip(xs, ys):
            p = probs(x)
            for i in range(n_moves):
                t = 1.0 if i == y else 0.0
                for j in range(d):
                    W[i][j] -= lr * (p[i] - t) * x[j]
    ok = 0
    for x, y in zip(xs, ys):
        p = probs(x)
        best = 0
        for i in range(n_moves):
            if p[i] > p[best] + 1e-12:
                best = i
        if best == y:
            ok += 1
    return ok / len(xs)
""", [[[[1, 0], [0, 1], [1, 1]], [0, 1, 2], 3, 20, 0.5], [[[1, 0], [0, 1]], [0, 1], 2, 1, 0.1], [[[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]], [0, 1, 2, 1], 3, 50, 0.5], [[[1.0], [2.0]], [0, 1], 2, 10, 0.2]], "Reuse the one-step update inside two loops, then count correct predictions.", approx=1e-9),
  ORDER("Supervised training", "Order the steps of one update.", ["Take a position and the expert's move", "Compute the network's move probabilities", "Compute the cross-entropy loss", "Compute the gradient", "Adjust the weights against the gradient"]),
  MATCH("Numbers from the paper", "Match each item with its value.", [("SL network layers", "13"), ("Training positions", "About 30 million"), ("Accuracy, all features", "57.0 percent"), ("Accuracy, raw board and history", "55.7 percent"), ("Previous best", "44.4 percent")]),
  FILL("Imitation", "The SL network is trained to maximize the {{log likelihood|likelihood}} of the human move. For a softmax the gradient is the probabilities minus a {{one-hot|onehot}} vector.")]))

# ------------------------------------------------------------ 6
CHS.append(CH(
 "Speed: the rollout and tree policies",
 ("Fast policies", [
  "Rollout policy | is | Linear softmax",
  "Rollout policy | uses | Local pattern features",
  "Rollout policy | takes | About 2 microseconds",
  "Accuracy | is | 24.2 percent",
  "Tree policy | gives | Placeholder priors",
  "Speed | enables | Many rollouts",
  "SL network | takes | A few milliseconds"]),
 ["The deep network is slow: several milliseconds per position. A Monte Carlo rollout needs a move at every step of a game that may last 150 moves. So AlphaGo trains a second, much smaller policy for rollouts: a linear softmax over small pattern features.",
  "It picks a move in about 2 microseconds, about 1,500 times faster than the SL policy network, at the cost of accuracy: 24.2 percent against 57.0 percent.",
  "A similar linear policy, the tree policy, supplies provisional priors for new tree nodes until the network has finished evaluating them."],
 [("Rollout policy", "A fast linear softmax policy used to play out games to the end."),
  ("Pattern feature", "A feature describing the local stones around a point, such as a 3 by 3 neighbourhood."),
  ("Linear softmax", "Score each move as a weighted sum of its features, then softmax."),
  ("Tree policy", "A slightly richer linear policy used for provisional priors."),
  ("Microsecond", "One millionth of a second."),
  ("Throughput", "How many games can be played per second.")],
 ["The rollout policy p_pi is a linear softmax of small pattern features.",
  "It reached 24.2 percent accuracy and takes about 2 microseconds per action.",
  "It ran about 1,000 simulations per second per CPU thread on an empty board.",
  "The SL policy network takes about 3 ms, roughly 1,500 times slower.",
  "The tree policy p_tau is similar to the rollout policy with more features.",
  "Fast and weak is the right tool when you need millions of moves."],
 [T("A Monte Carlo rollout plays a game to the end from a position. With about a hundred and fifty moves in a game, one rollout needs about a hundred choices. If each choice cost three milliseconds, as for the deep network, a single rollout would take a third of a second. The search needs thousands. So a different tool is needed for that job."),
  T("The paper trains a fast rollout policy p pi. It is a linear softmax of small pattern features. For each legal move it computes features of the nearby stones, takes a weighted sum, and applies a softmax across moves. The paper says it achieved 24.2 percent accuracy, against 57.0 percent for the big network, but needs only about two microseconds to select an action. That is about fifteen hundred times faster."),
  M(r"p_\pi(a \mid s) \;=\; \frac{\exp\!\bigl(\mathbf{w}\cdot\boldsymbol{\phi}(s,a)\bigr)}{\sum_{b}\exp\!\bigl(\mathbf{w}\cdot\boldsymbol{\phi}(s,b)\bigr)}"),
  T("What are the features? The paper lists a set of small pattern features, including patterns of stones in a three by three neighbourhood around a move and some features about the last move and responses to it. A three by three neighbourhood has eight surrounding points, each empty, black or white, so each local pattern can be given a single number by reading the eight points as digits in base three. The practice section builds that."),
  T("The linear model has so few computations that the paper reports about one thousand simulations per second per CPU thread on an empty board. This is the throughput a Monte Carlo search needs. It was trained on 8 million positions from the Tygem server, with the same supervised method as the big network."),
  T("There is also the tree policy p tau. It has a similar structure but richer features. The paper uses it for a specific job: when the tree grows a new node, the network that supplies priors takes time to compute. In the meantime, the tree policy gives provisional values, so the search is never blocked waiting for the network."),
  T("The trade is a general one in engineering search programs. A slow and accurate component is used sparingly, at the important decision points. A fast and crude component fills the bulk of the work. AlphaGo uses the deep networks in the tree and the linear policy in the rollouts, then blends their opinions, chapter 9."),
  T("In the practice section you score moves with a linear softmax, encode a three by three pattern as a number, compute throughput and the speed ratio, and sample a rollout move deterministically.")],
 [("Why does AlphaGo use a separate rollout policy?", ["The big network is too slow for millions of moves", "The rules differ", "It is more accurate", "It is simpler to code"], 0, "Speed."),
  ("What accuracy does the rollout policy reach?", ["24.2 percent", "57.0 percent", "99 percent", "5 percent"], 0, "Weaker but about 1,500 times faster."),
  ("What is a 3 by 3 pattern?", ["The stones around a point", "The komi", "A move list", "A score"], 0, "Eight neighbours, each empty, black or white."),
  ("What is the tree policy for?", ["Provisional priors for new nodes", "Resigning", "Scoring", "Choosing komi"], 0, "Used until the network has evaluated.")],
 [("How fast is the rollout policy?", "About 2 microseconds per move."), ("Is it a deep network?", "No, it is a linear softmax."), ("What data trained it?", "8 million positions from Tygem."),
  ("What does it trade?", "Accuracy for speed.")],
 [PL("Score moves with a linear policy", "features[i] is the feature vector of legal move i; weights is the shared weight vector. Write linear_policy(features, weights): the softmax over moves of the dot product of weights with each feature vector. Use import math.",
     "linear_policy(features, weights)", """
import math
def linear_policy(features, weights):
    z = []
    for f in features:
        z.append(sum(w * x for w, x in zip(weights, f)))
    m = max(z)
    e = [math.exp(t - m) for t in z]
    s = sum(e)
    return [t / s for t in e]
""", [[[[1, 0], [0, 1]], [1.0, 2.0]], [[[1, 1, 0], [0, 0, 1], [1, 0, 1]], [0.5, 0.5, 1.0]], [[[1.0]], [3.0]], [[[0, 0], [0, 0]], [1.0, 1.0]]], "Compute one dot product per move, then softmax.", approx=1e-9),
  PL("Encode a 3 by 3 pattern", "The eight points around a move are given as a list of eight characters from '.', 'X', 'O'. Write pattern_id(cells): read them as base-3 digits (. = 0, X = 1, O = 2), first cell most significant, and return the integer.",
     "pattern_id(cells)", """
def pattern_id(cells):
    v = 0
    for ch in cells:
        d = 0
        if ch == 'X':
            d = 1
        elif ch == 'O':
            d = 2
        v = v * 3 + d
    return v
""", [[["."] * 8], [["X"] * 8], [["O"] * 8], [[".", ".", ".", ".", ".", ".", ".", "X"]], [["X", "O", ".", "X", "O", ".", "X", "O"]]], "Multiply the running value by 3 and add the digit."),
  PL("Throughput and speed ratio", "Write rollout_stats(us_per_move, game_length, slow_ms): return [games per second, how many times faster than a slow policy needing slow_ms milliseconds per move]. Games per second = 1,000,000 / (us_per_move * game_length). The ratio = slow_ms * 1000 / us_per_move.",
     "rollout_stats(us_per_move, game_length, slow_ms)", """
def rollout_stats(us_per_move, game_length, slow_ms):
    gps = 1000000.0 / (us_per_move * game_length)
    return [gps, slow_ms * 1000.0 / us_per_move]
""", [[2, 150, 3], [10, 100, 3], [2, 1, 5], [4, 200, 1]], "Convert units carefully.", approx=1e-9),
  PL("Draw a rollout move", "Write sample_move(p, u): choose a move index from the probability list p using a uniform number u in [0, 1): return the first index whose cumulative probability exceeds u (the last index if none does).",
     "sample_move(p, u)", """
def sample_move(p, u):
    total = 0.0
    for i in range(len(p)):
        total += p[i]
        if total > u:
            return i
    return len(p) - 1
""", [[[0.5, 0.3, 0.2], 0.0], [[0.5, 0.3, 0.2], 0.55], [[0.5, 0.3, 0.2], 0.95], [[0.25, 0.25, 0.25, 0.25], 0.5], [[1.0], 0.9]], "Walk through the cumulative sum."),
  ORDER("Why two policies", "Order the argument.", ["The deep network is accurate but takes milliseconds", "Rollouts need millions of moves", "A linear softmax takes microseconds", "Train it on the same expert moves", "Use it for rollouts and keep the deep network for the tree"]),
  MATCH("Policies", "Match each policy with its property.", [("SL policy network", "Deep, 57.0 percent, milliseconds"), ("Rollout policy", "Linear, 24.2 percent, microseconds"), ("Tree policy", "Provisional priors for new nodes"), ("RL policy network", "Self-play improved"), ("Value network", "Position evaluation")]),
  FILL("Speed", "The rollout policy is a {{linear}} softmax of pattern features. It takes about {{2}} microseconds per move, trading {{accuracy}} for speed.")]))

# ------------------------------------------------------------ 7
CHS.append(CH(
 "Getting better: policy gradient self-play",
 ("Reinforcement learning", [
  "RL policy network | starts as | Copy of SL network",
  "Self-play | plays against | Earlier versions",
  "Reward | is | Plus or minus one at game end",
  "REINFORCE | follows | Outcome times gradient of log p",
  "Opponent pool | prevents | Overfitting to one opponent",
  "RL network | wins | Over 80 percent against SL",
  "RL network | wins | 85 percent against Pachi"]),
 ["Imitation copies the experts' moves; it does not directly optimize winning. The second stage fixes that. The RL policy network starts as a copy of the SL network and plays games against earlier versions of itself, adjusting its weights to win.",
  "The update is the policy gradient. After a game, every move played is made more likely if the game was won and less likely if it was lost: the weights move in the direction of the gradient of log p, multiplied by plus one or minus one.",
  "The result was strong. The RL policy network won more than 80 percent of games against the SL network, and 85 percent against Pachi with no search at all."],
 [("Self-play", "The program plays games against itself or earlier copies."),
  ("Policy gradient", "Adjust a policy's parameters to increase the expected reward."),
  ("REINFORCE", "The simplest policy gradient: reward times the gradient of the log probability of the action taken."),
  ("Opponent pool", "A set of earlier versions to play against, for stability."),
  ("Outcome z", "Plus one for a win, minus one for a loss, at the end of the game."),
  ("Baseline", "A number subtracted from the reward to reduce noise; the simplest choice is zero.")],
 ["The RL network is initialized to the SL weights (rho = sigma).",
  "It plays against randomly selected earlier iterations, to avoid overfitting to the current self.",
  "Update: delta rho is proportional to (d log p_rho(a_t | s_t) / d rho) times z_t.",
  "The reward is +1 for a win and -1 for a loss; zero for all other steps.",
  "Training used 10,000 mini-batches of 128 games on 50 GPUs for a day.",
  "The RL network beat the SL network over 80 percent of the time and Pachi 85 percent without search."],
 [T("Supervised learning optimizes the wrong thing. It makes the network predict what a human would do, which is related to winning but not the same thing. The paper's second stage adjusts the policy toward the correct goal of winning games, rather than maximizing predictive accuracy."),
  T("The RL policy network p rho has the same structure as the SL network, and its weights rho start equal to the SL weights sigma. It then plays games against other versions. The paper says the opponent is a randomly selected earlier iteration of the network. Using a pool of older versions stabilizes training and prevents overfitting to the current policy. The pool is refreshed every five hundred iterations."),
  T("Each game ends with a reward. The outcome z at the end is plus one for a win and minus one for a loss, and all intermediate rewards are zero. Now the learning rule. For every position s t and move a t in the game, the weights move in proportion to the gradient of the log probability of the move, multiplied by the outcome z t of the game as seen by the player who made the move."),
  M(r"\Delta\rho \;\propto\; \frac{\partial \log p_\rho(a_t \mid s_t)}{\partial \rho}\; z_t"),
  T("Read this carefully. If the player won, z is plus one, and the gradient is added: every move of the winning game becomes a bit more probable. If the player lost, z is minus one, and the gradient is subtracted: every move of the lost game becomes a bit less probable. Some of those moves were good and some bad, but on average winners play better moves than losers. With many games, signal beats noise."),
  T("The scale was large. The paper reports training with mini-batches of 128 games, 10,000 of them, on 50 GPUs, for one day. The result, tested by play, was strong. Playing head-to-head, the RL policy network won more than 80 percent of games against the SL policy network. Using no search at all, it won 85 percent of games against Pachi, the strongest open-source program, which ran 100,000 simulations per move. Earlier networks trained only by supervised learning won 11 percent against Pachi."),
  T("An important caution from the paper: when the strongest RL network was used to give priors in the tree search, AlphaGo played worse than with the SL network. The RL network was stronger alone but its use in the search was less helpful. Where the RL network matters is the next stage: it generates the games from which the value network learns."),
  T("The practice section implements the REINFORCE update on a tiny softmax policy, the expected update when the game outcomes are known, a training loop that watches the policy shift toward winning moves, and the pool schedule.")],
 [("How is the RL network initialized?", ["From the SL network", "At random", "From the rules", "From the value network"], 0, "rho = sigma."),
  ("What does a won game do to its moves?", ["Makes them more probable", "Makes them less probable", "Nothing", "Removes them"], 0, "z = +1 pushes the gradient up."),
  ("Why play against older versions?", ["It stabilizes training", "It is faster", "To save memory", "To copy humans"], 0, "Prevents overfitting to the current policy."),
  ("How did the RL network do against Pachi without search?", ["Won 85 percent", "Lost most games", "Won 11 percent", "Tied"], 0, "Compared to 11 percent for the SL-only network.")],
 [("What is the reward?", "+1 for a win and -1 for a loss at the end."), ("What does REINFORCE multiply?", "The gradient of log probability by the outcome."), ("How often was the pool refreshed?", "Every 500 iterations."),
  ("Was the RL network better in the tree search?", "No, the SL network gave better priors.")],
 [PL("One REINFORCE step", "A policy has logits (a list). The agent took action a and the game outcome was z (+1 or -1). Write reinforce_step(logits, a, z, lr): p = softmax(logits); return logits[i] + lr * z * (onehot[i] - p[i]) for each i. Use import math.",
     "reinforce_step(logits, a, z, lr)", """
import math
def reinforce_step(logits, a, z, lr):
    m = max(logits)
    e = [math.exp(t - m) for t in logits]
    s = sum(e)
    p = [t / s for t in e]
    out = []
    for i in range(len(logits)):
        t = 1.0 if i == a else 0.0
        out.append(logits[i] + lr * z * (t - p[i]))
    return out
""", [[[0.0, 0.0], 0, 1, 0.5], [[0.0, 0.0], 0, -1, 0.5], [[1.0, 2.0, 3.0], 2, 1, 0.1], [[0.5, 0.5, 0.5], 1, -1, 1.0]], "The direction is z times (onehot minus p).", approx=1e-9),
  PL("Expected update", "Suppose action i always gives outcome zs[i] (each +1 or -1). The expected REINFORCE update is the sum over i of p[i] * zs[i] * (onehot_i - p). Write expected_step(logits, zs, lr): return the new logits after one expected update with learning rate lr. Use import math.",
     "expected_step(logits, zs, lr)", """
import math
def expected_step(logits, zs, lr):
    m = max(logits)
    e = [math.exp(t - m) for t in logits]
    s = sum(e)
    p = [t / s for t in e]
    n = len(logits)
    out = []
    for j in range(n):
        g = 0.0
        for i in range(n):
            t = 1.0 if i == j else 0.0
            g += p[i] * zs[i] * (t - p[j])
        out.append(logits[j] + lr * g)
    return out
""", [[[0.0, 0.0], [1, -1], 1.0], [[0.0, 0.0, 0.0], [-1, 1, -1], 0.5], [[2.0, 0.0], [1, -1], 0.1], [[0.0, 0.0], [1, 1], 1.0]], "Accumulate p_i times z_i times (onehot_i[j] minus p_j) for each j.", approx=1e-9),
  PL("Does it learn?", "Repeat expected_step many times. Write train_bandit(zs, lr, steps): start from zero logits and apply the expected update steps times; return the probability of the first best action (the lowest index with the largest outcome) after training, rounded to 4 decimals.",
     "train_bandit(zs, lr, steps)", """
import math
def train_bandit(zs, lr, steps):
    n = len(zs)
    logits = [0.0] * n
    for k in range(steps):
        m = max(logits)
        e = [math.exp(t - m) for t in logits]
        s = sum(e)
        p = [t / s for t in e]
        new = []
        for j in range(n):
            g = 0.0
            for i in range(n):
                t = 1.0 if i == j else 0.0
                g += p[i] * zs[i] * (t - p[j])
            new.append(logits[j] + lr * g)
        logits = new
    m = max(logits)
    e = [math.exp(t - m) for t in logits]
    s = sum(e)
    best = 0
    for i in range(n):
        if zs[i] > zs[best]:
            best = i
    return round(e[best] / s, 4)
""", [[[1, -1], 0.5, 40], [[-1, 1, -1], 0.5, 60], [[1, -1, -1, -1], 1.0, 10], [[1, 1], 0.5, 5]], "Run the expected update in a loop; compute the softmax at the end.", approx=1e-3),
  PL("Opponent pool schedule", "The opponent pool receives a snapshot of the current policy every `every` iterations. Write snapshots(total, every): the list of iteration numbers (counting from 1) at which a snapshot is added, up to and including total.",
     "snapshots(total, every)", """
def snapshots(total, every):
    out = []
    t = every
    while t <= total:
        out.append(t)
        t += every
    return out
""", [[2000, 500], [499, 500], [10, 3], [0, 5], [1500, 500]], "Step through multiples of every."),
  ORDER("RL update", "Order the steps.", ["Start from the SL weights", "Play a game against a random earlier version", "Record the outcome z", "Add z times the gradient of log p for each move", "Refresh the opponent pool every 500 iterations"]),
  MATCH("Terms", "Match each term with its meaning.", [("z", "Game outcome, plus or minus one"), ("Policy gradient", "Move toward higher expected reward"), ("Opponent pool", "Earlier versions as opponents"), ("rho", "Weights of the RL network"), ("sigma", "Weights of the SL network")]),
  FILL("Self-play", "Winning games make their moves {{more}} probable and losing games make them {{less}} probable. The RL network is initialized from the {{SL|supervised}} network.")]))

# ------------------------------------------------------------ 8
CHS.append(CH(
 "Judging positions: the value network",
 ("Evaluation", [
  "Value network | predicts | Winner from position",
  "Training data | is | Self-play games of RL network",
  "One position | per | Game",
  "Loss | is | Mean squared error",
  "KGS data | causes | Overfitting",
  "Value network | matches | RL rollouts",
  "Value network | is | 15,000 times cheaper"]),
 ["The value network estimates the outcome of the game from a position: a single number between minus one and one. It is a deep network like the policy network, with one scalar output, and it takes an extra input plane saying whose turn it is.",
  "Training it needed care. Positions from a single game are strongly correlated, and early attempts that used all positions from human games memorized the games and failed on new ones. The fix was to generate 30 million positions, each from a different self-play game, and to regress them on the game outcomes.",
  "The result approached the accuracy of Monte Carlo rollouts with the RL policy, with about 15,000 times less computation."],
 [("Value function", "The expected outcome of the game from a position under good play."),
  ("Regression", "Training a network to output a number close to a target, here the game outcome."),
  ("Mean squared error", "The average of squared differences between prediction and target."),
  ("Overfitting", "Memorizing training data instead of learning general patterns."),
  ("Correlated data", "Samples that are not independent, such as many positions from one game."),
  ("Target z", "The final result of the game, +1 or -1, from the viewpoint of the player to move.")],
 ["v_theta(s) predicts the game outcome from position s.",
  "Trained by regression with mean squared error on (s, z) pairs.",
  "30 million positions, each from a separate self-play game of the RL network.",
  "Training on KGS human games overfit: test error 0.37 against training error 0.19.",
  "With the self-play data: training MSE 0.226 and test MSE 0.234.",
  "One evaluation approaches the accuracy of RL-policy rollouts at about 15,000 times less compute."],
 [T("Now the part that gave AlphaGo its eye for positions. The value network v theta takes a board and predicts the outcome of the game for the player to move, between minus one for a sure loss and plus one for a sure win. It has the same convolutional structure as the policy network, plus the player-colour plane, and ends in a single number."),
  T("The data are pairs: a position and the final result of the game it came from. Training is regression. The network's output should be close to the result, and the loss is the mean squared error. A perfectly unsure network that always says zero has a squared error of one on every sample, since the result is plus or minus one. So an error below one means the network has learned something."),
  M(r"L(\theta) \;=\; \bigl(z - v_\theta(s)\bigr)^2 \qquad\text{(averaged over training positions)}"),
  T("The obvious plan, training on positions from the human expert games, failed. The paper reports that the network memorized the game outcomes instead of generalizing: mean squared error 0.19 on the training set but 0.37 on the test set. The reason is correlation. Successive positions in one game are nearly identical, and all share one result, so the network can recognize which game a position is from and recite the result."),
  T("The cure is to break the correlation. The paper generated a new data set by self-play with the RL policy network. For each game, it picks one random time step u, plays the moves before u from the SL policy network, makes one random move at step u to add variety, and then plays on with the RL policy network until the end. Only the position at step u and the final outcome go into the data. This produced 30 million positions, each from a separate game."),
  T("With that data the value network trained properly, with a mean squared error of 0.226 on the training set and 0.234 on the test set, little overfitting. The paper trained it with 50 million mini-batches of 32 positions on 50 GPUs for a week. The result: a single evaluation of the value network approached the accuracy of Monte Carlo rollouts using the RL policy network, with about fifteen thousand times less computation."),
  T("The comparison is vivid. Before this, evaluating a position meant playing it out many times. Now one forward pass of the network gives a comparable answer. This is the second half of how AlphaGo shortens the search: the value network replaces deep lines of play by a single judgement."),
  T("In the practice section you compute the squared-error loss, the target from the winner, the sampling schedule used for the self-play data set, and the gap that reveals overfitting.")],
 [("What does v_theta(s) output?", ["The expected game outcome", "A move", "The komi", "The number of liberties"], 0, "A number between -1 and 1."),
  ("Why did training on KGS games overfit?", ["Positions within a game are correlated", "The games were short", "Go has no rules", "The network was too small"], 0, "The network memorized the outcomes."),
  ("How were the 30 million self-play positions chosen?", ["One position from each separate game", "All positions from a few games", "The first move only", "Random boards"], 0, "That breaks the correlation."),
  ("How much cheaper was a value evaluation than RL rollouts?", ["About 15,000 times", "About 2 times", "The same", "Slightly"], 0, "Near equal accuracy.")],
 [("What loss is used?", "Mean squared error."), ("What does always predicting 0 score?", "A squared error of 1."), ("What is the fix for overfitting?", "One position per self-play game."),
  ("What does the value network add as input?", "A plane for the player's colour.")],
 [PL("Value loss", "Write value_mse(preds, targets): the mean of (target - pred)^2.",
     "value_mse(preds, targets)", """
def value_mse(preds, targets):
    total = 0.0
    for p, z in zip(preds, targets):
        total += (z - p) ** 2
    return total / len(preds)
""", [[[0.0, 0.0], [1, -1]], [[0.5, -0.5], [1, -1]], [[1.0, -1.0, 1.0], [1, -1, -1]], [[0.2], [1]]], "Average the squared differences.", approx=1e-12),
  PL("Target from the winner", "Write target(winner, to_move): +1 if the player to move is the winner, otherwise -1 (both are 'B' or 'W').",
     "target(winner, to_move)", """
def target(winner, to_move):
    if winner == to_move:
        return 1
    return -1
""", [["B", "B"], ["B", "W"], ["W", "W"], ["W", "B"]], "Compare the two letters."),
  PL("Sign accuracy", "A value prediction is right if it has the same sign as the target (a prediction of exactly 0 is wrong). Write sign_accuracy(preds, targets): the fraction right.",
     "sign_accuracy(preds, targets)", """
def sign_accuracy(preds, targets):
    ok = 0
    for p, z in zip(preds, targets):
        if p * z > 0:
            ok += 1
    return ok / len(preds)
""", [[[0.3, -0.2, 0.0, 0.9], [1, -1, 1, -1]], [[0.5], [1]], [[-0.5, -0.5], [1, -1]], [[0.1, 0.2], [1, 1]]], "Multiply and check the sign.", approx=1e-12),
  PL("Overfitting gap", "Write overfit_report(train_mse, test_mse): return [gap, flag] where gap = test_mse - train_mse (rounded to 3 decimals) and flag is 1 if the gap exceeds 0.1, else 0.",
     "overfit_report(train_mse, test_mse)", """
def overfit_report(train_mse, test_mse):
    gap = round(test_mse - train_mse, 3)
    flag = 0
    if gap > 0.1:
        flag = 1
    return [gap, flag]
""", [[0.19, 0.37], [0.226, 0.234], [0.3, 0.3], [0.1, 0.25]], "Subtract, round, compare.", approx=1e-9),
  PL("Pick the self-play sample", "Write sample_plan(game_length, u): for a game of the given length and the chosen random step u (1-based), return [number of moves played by the SL policy, 1 for the random move, number of moves played by the RL policy until the game ends]. The data point is the position after the random move.",
     "sample_plan(game_length, u)", """
def sample_plan(game_length, u):
    return [u - 1, 1, game_length - u]
""", [[100, 30], [150, 1], [120, 120], [60, 31]], "Moves before u, the move u, and the moves after."),
  ORDER("Building the value data", "Order the steps for one data point.", ["Pick a random step u", "Play moves before u with the SL policy", "Make one random move at step u", "Finish the game with the RL policy", "Store the position after step u with the final outcome"]),
  MATCH("Numbers", "Match each item with its value.", [("Training positions", "30 million"), ("KGS training error", "0.19"), ("KGS test error", "0.37"), ("Self-play test error", "0.234"), ("Speed advantage over rollouts", "About 15,000 times")]),
  FILL("Value", "The value network is trained by {{regression}} on the game {{outcome|result}}. Each of the 30 million positions came from a {{separate|different}} game.")]))
