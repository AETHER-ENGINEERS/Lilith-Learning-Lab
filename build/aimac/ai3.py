"""AI course, chapters 11-15."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

C = []

C.append(CH(
 "Making decisions: utility and MDPs",
 ("Decisions", [
  "Utility | ranks | Outcomes", "Expected utility | guides | Choices", "Risk aversion | bends | Utility of money", "MDP | models | Sequential decisions",
  "Policy | maps | States to actions", "Bellman equation | defines | Utility", "Value iteration | solves | MDPs"]),
 ["A rational agent chooses the action with the highest expected utility: the sum over outcomes of probability times utility. Utility of money is usually concave, which explains risk aversion.",
  "When decisions come in sequence, we use a Markov decision process: states, actions, a transition model and rewards. The solution is a policy that gives an action for each state. Value iteration computes it by repeatedly applying the Bellman update.",
  "The labs write expected utility and value iteration."],
 [("Utility", "A number that says how much an outcome is preferred."), ("Expected utility", "Probability-weighted average of utilities."), ("MDP", "Markov decision process."),
  ("Policy", "A rule that gives an action for each state."), ("Discount factor", "Gamma below one: how much future rewards count."), ("Bellman equation", "U(s) = R(s) + gamma max over a of sum P(s' | s, a) U(s').")],
 ["Maximise expected utility.", "A concave utility of money means risk aversion.", "A policy, not a plan, is the solution when outcomes are uncertain.",
  "Value iteration repeats the Bellman update until values settle.", "Policy iteration alternates evaluating and improving a policy.", "A POMDP is an MDP with hidden state: plan over belief states."],
 [T("Suppose you can take a sure 40 dollars or a coin flip that pays 100 or nothing. The coin flip has an expected value of 50, yet many people take the sure 40. That is not irrational: the tenth extra dollar is worth less than the first. Utility captures this: it is a curve, not a straight line."),
  M(r"EU(a) \;=\; \sum_{s'} P(s' \mid a)\,U(s')"),
  T("The principle of maximum expected utility says to pick the action with the largest value of this sum. It follows from a few reasonable axioms about preferences, such as transitivity. People do violate the axioms in practice, as the Allais paradox shows, but the principle remains the design standard for machines."),
  T("Many problems need a sequence of decisions in an uncertain world. A Markov decision process has states, actions, a transition model P(s' | s, a), and a reward per state. Because outcomes are uncertain, the answer is a policy: what to do in every state we might reach."),
  M(r"U(s) \;=\; R(s) + \gamma \max_a \sum_{s'} P(s' \mid s,a)\,U(s')"),
  T("This is the Bellman equation. The utility of a state is its reward plus the discounted expected utility of the best action. Value iteration starts with all utilities at zero and applies the equation to every state again and again. It converges because the update shrinks differences by the factor gamma. The best policy then picks the action that achieves the maximum.")],
 [("What should a rational agent maximise?", ["Expected utility", "The best outcome", "Expected money", "Probability only"], 0, "Probability-weighted utility."),
  ("What is the solution of an MDP?", ["A policy", "A single plan", "A heuristic", "A proof"], 0, "An action for every state."),
  ("What does the discount factor do?", ["Weights future rewards less", "Increases rewards", "Removes uncertainty", "Fixes the policy"], 0, "Gamma below one.")],
 [("What is risk aversion?", "Preferring a sure payoff over a gamble."), ("What is policy iteration?", "Alternate evaluating and improving."), ("What is a POMDP?", "An MDP with hidden state."), ("Why does value iteration converge?", "The update is a contraction.")],
 [FILL("Utility", "A rational agent chooses the action with the highest {{expected}} {{utility}}."),
  PL("Expected utility", "Write expected_utility(outcomes): outcomes is a list of [probability, utility]. Return the expected utility rounded to 9 decimals.",
     "expected_utility(outcomes)", """
def expected_utility(outcomes):
    s = 0.0
    for p, u in outcomes:
        s += p * u
    return round(s, 9)
""", [[[[0.5, 100], [0.5, 0]]], [[[1.0, 40]]], [[[0.2, 10], [0.3, -5], [0.5, 2]]]], "Sum of p times u.", approx=1e-9),
  PL("Value iteration", "Write value_iteration(P, R, gamma, iters): P[s][a] is a list of [probability, next_state]; R[s] the reward; run iters rounds of the Bellman update from zero values (use the values from the previous round for all states). Return the final values rounded to 6 decimals.",
     "value_iteration(P, R, gamma, iters)", """
def value_iteration(P, R, gamma, iters):
    n = len(R)
    U = [0.0] * n
    for _ in range(iters):
        new = []
        for s in range(n):
            best = None
            for a in P[s]:
                q = 0.0
                for p, s2 in a:
                    q += p * U[s2]
                if best is None or q > best:
                    best = q
            if best is None:
                best = 0.0
            new.append(R[s] + gamma * best)
        U = new
    return [round(x, 6) for x in U]
""", [[[[[[1.0, 1]], [[1.0, 0]]], [[[1.0, 1]]]], [0.0, 1.0], 0.9, 50], [[[[[1.0, 0]]]], [2.0], 0.5, 30], [[[[[0.8, 1], [0.2, 0]]], [[[1.0, 1]]]], [0.0, 1.0], 0.9, 100]], "Update from the previous round's values.", approx=1e-5)]))

C.append(CH(
 "Multiple agents and game theory",
 ("Game theory", [
  "Game | has | Players, actions, payoffs", "Dominant strategy | beats | All alternatives", "Nash equilibrium | is | No profitable deviation",
  "Prisoner's dilemma | shows | Cooperation problem", "Auction | allocates | Goods by bids", "Vickrey auction | rewards | Truthful bids", "Mechanism design | shapes | Rules"]),
 ["When several agents act, each one's best choice depends on the others. Game theory studies this. A Nash equilibrium is a set of strategies where no player gains by changing alone.",
  "The prisoner's dilemma shows that individually rational choices can leave everyone worse off. Mechanism design flips the question: choose the rules so that self-interested agents produce a good result. A Vickrey auction makes honest bidding the best strategy.",
  "The labs find equilibria and run an auction."],
 [("Strategy", "A rule for choosing actions."), ("Payoff", "What a player receives from an outcome."), ("Dominant strategy", "Best whatever others do."),
  ("Nash equilibrium", "No player can gain by changing alone."), ("Mechanism", "The rules of an interaction."), ("Vickrey auction", "Highest bidder wins and pays the second-highest bid.")],
 ["Normal form: a table of payoffs.", "Dominant strategies are the simplest solution.", "Not every game has a pure Nash equilibrium; mixed strategies always exist.",
  "In the prisoner's dilemma defection is dominant, yet cooperation pays more.", "Vickrey: bidding your true value is dominant.", "Social choice: Arrow's theorem limits fair voting."],
 [T("In a game, a player's payoff depends on everyone's choices. Take two suspects held apart. If both stay silent they get a light sentence. If one confesses while the other stays silent, the confessor goes free. If both confess, both get a medium sentence."),
  T("Whatever the other does, confessing is better for you. It is a dominant strategy. So both confess, and both get the medium sentence, although mutual silence would have been better for both. Individual rationality leads to a collective loss."),
  T("A Nash equilibrium is a profile of strategies such that no player can do better by changing their own strategy while the others stay put. In the prisoner's dilemma, both confessing is the unique equilibrium. Some games, like rock-paper-scissors, have no equilibrium in pure strategies, only in mixed ones where players randomise."),
  T("Repeating the game changes the picture. When players meet many times, strategies such as tit-for-tat, which cooperates first and then copies the other's last move, can sustain cooperation."),
  T("Mechanism design is game theory in reverse: pick the rules to get the outcome you want. In a sealed-bid second-price auction, the winner pays the second-highest bid. Then bidding anything other than your true value cannot help you: a lower bid risks losing a profitable win, a higher bid risks winning at a loss. Truth telling is a dominant strategy."),
  T("When people vote, the picture is hard. Arrow's theorem shows that no ranked voting rule satisfies a short list of fairness conditions at the same time. The best we can do is choose which compromises to accept.")],
 [("What is a Nash equilibrium?", ["No player gains by deviating alone", "The best joint outcome", "A random choice", "A dominant strategy for all"], 0, "Each strategy is a best reply."),
  ("Why is the prisoner's dilemma a dilemma?", ["Defection is dominant yet both lose", "There is no payoff", "It has no equilibrium", "Players cannot choose"], 0, "Mutual cooperation is better for both."),
  ("What is the best bid in a Vickrey auction?", ["Your true value", "Half your value", "Double your value", "Zero"], 0, "It is a dominant strategy.")],
 [("What is tit-for-tat?", "Cooperate, then copy the last move."), ("What is a mixed strategy?", "Randomising over actions."), ("What is mechanism design?", "Designing rules for desired outcomes."), ("What does Arrow's theorem show?", "No perfect ranked voting rule.")],
 [MATCH("Game terms", "Match each term with its meaning.", [("Dominant strategy", "Best whatever others do"), ("Nash equilibrium", "No gain from changing alone"), ("Mixed strategy", "Randomise over actions"), ("Vickrey auction", "Winner pays second price")]),
  PL("Pure Nash equilibria", "Write nash(A, B): A[i][j] is the row player's payoff and B[i][j] the column player's when row plays i and column plays j. Return the list of [i, j] pairs that are pure Nash equilibria, in row-major order.",
     "nash(A, B)", """
def nash(A, B):
    out = []
    for i in range(len(A)):
        for j in range(len(A[0])):
            best_row = True
            for k in range(len(A)):
                if A[k][j] > A[i][j]:
                    best_row = False
            best_col = True
            for k in range(len(A[0])):
                if B[i][k] > B[i][j]:
                    best_col = False
            if best_row and best_col:
                out.append([i, j])
    return out
""", [[[[3, 0], [5, 1]], [[3, 5], [0, 1]]], [[[2, 0], [0, 1]], [[1, 0], [0, 2]]], [[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]]], "Check both players' best replies.", approx=None),
  PL("Vickrey auction", "Write vickrey(bids): bids is a list of at least two numbers. Return [index of the winner (lowest index if tied), price paid], where the price is the second-highest bid.",
     "vickrey(bids)", """
def vickrey(bids):
    w = 0
    for i in range(len(bids)):
        if bids[i] > bids[w]:
            w = i
    second = None
    for i in range(len(bids)):
        if i != w and (second is None or bids[i] > second):
            second = bids[i]
    return [w, second]
""", [[[10, 20, 15]], [[5, 5]], [[7, 3, 9, 8]], [[1, 2]]], "Find the max, then the best of the rest.", approx=None)]))

C.append(CH(
 "Learning from examples",
 ("Learning", [
  "Supervised learning | maps | Inputs to outputs", "Overfitting | fits | Noise", "Cross-validation | estimates | Generalisation", "Decision tree | splits on | Information gain",
  "Linear regression | minimises | Squared error", "Regularisation | penalises | Complexity", "Ensembles | combine | Many models"]),
 ["Learning lets an agent improve from data. In supervised learning the data are input-output pairs and the aim is a function that predicts well on new inputs. The main danger is overfitting: a model that fits noise in the training data.",
  "Decision trees split on the attribute with the highest information gain. Linear models fit a line or plane by minimising squared error, using a formula or gradient descent. Nearest neighbours predict from the closest examples. Ensembles such as random forests combine many models.",
  "The labs compute entropy, nearest neighbours and a gradient step."],
 [("Training set", "Examples used to fit the model."), ("Test set", "Held-out examples used to estimate performance."), ("Overfitting", "Low training error but high error on new data."),
  ("Entropy", "A measure of uncertainty in a distribution."), ("Information gain", "Reduction in entropy from a split."), ("Regularisation", "A penalty that discourages complex models.")],
 ["Hold out data to measure generalisation.", "Bias-variance trade-off: simple models underfit, complex ones overfit.", "Entropy H = minus the sum of p log2 p.",
  "Decision trees choose the split with the largest information gain.", "Linear regression: minimise squared error; gradient descent updates w by minus alpha times the gradient.", "Bagging averages models; boosting trains them in sequence."],
 [T("Give a program thousands of examples of house sizes and prices, and ask it to predict the price of a new house. This is supervised learning. The hypothesis is a function; the learning algorithm searches for one that matches the examples."),
  T("A model that matches the training data perfectly is not necessarily good. A very flexible curve can wiggle through every point, including the noise, and predict poorly on a new house. This is overfitting. To detect it, keep some data aside for testing, or use cross-validation, which rotates which part is held out."),
  T("A decision tree asks a series of questions. To choose the question, we measure how much it reduces uncertainty. Entropy measures uncertainty: zero when all examples agree, one bit for an even split between two classes. The best question is the one with the highest information gain."),
  M(r"H(p) \;=\; -\sum_i p_i \log_2 p_i"),
  T("Linear regression fits a line. We pick the weights that minimise the sum of squared errors. For one input there are closed forms. In general we use gradient descent: move the weights a small step against the gradient of the error. The step size is the learning rate."),
  T("Other models include nearest neighbours, which predict from the closest training examples, and support vector machines, which find a wide margin and use kernels for curved boundaries. Regularisation adds a penalty on weights to resist overfitting. Ensembles, such as random forests and boosted trees, combine many weak models and often win on tabular data.")],
 [("What is overfitting?", ["Fitting noise so new data are predicted poorly", "A low learning rate", "Using too little data to test", "A perfect model"], 0, "Training error is low, test error high."),
  ("What does entropy measure?", ["Uncertainty", "Accuracy", "Speed", "Size of the data"], 0, "Zero when the outcome is certain."),
  ("What does gradient descent do?", ["Moves weights against the error gradient", "Sorts data", "Adds noise", "Counts features"], 0, "Small steps downhill.")],
 [("What is cross-validation?", "Rotating the held-out part."), ("What does a kernel allow?", "Curved boundaries from linear methods."), ("What is bagging?", "Averaging models trained on resamples."), ("What is a learning rate?", "The size of each update step.")],
 [ORDER("Gradient descent", "Put the steps in order.", ["Start with initial weights", "Compute the error gradient on the data", "Move the weights a small step against the gradient", "Repeat until the error stops improving"]),
  PL("Entropy", "Write entropy(counts): counts is a list of non-negative class counts. Return the entropy in bits, rounded to 9 decimals (skip zero counts; 0 for an empty total). Use import math.",
     "entropy(counts)", """
import math
def entropy(counts):
    t = sum(counts)
    if t == 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / t
            h -= p * math.log(p) / math.log(2)
    return round(h, 9)
""", [[[1, 1]], [[4, 0]], [[1, 1, 2]], [[9, 5]], [[]]], "Sum -p log2 p.", approx=1e-9),
  PL("Nearest neighbour", "Write knn(train, labels, q, k): train is a list of numeric points (lists); labels the class of each; return the majority label among the k points closest (squared Euclidean distance) to q. Break ties in votes by choosing the label whose nearest member is closer.",
     "knn(train, labels, q, k)", """
def knn(train, labels, q, k):
    d = []
    for i in range(len(train)):
        s = 0.0
        for a, b in zip(train[i], q):
            s += (a - b) * (a - b)
        d.append((s, i))
    d.sort()
    votes = {}
    first = {}
    for pos in range(k):
        lab = labels[d[pos][1]]
        votes[lab] = votes.get(lab, 0) + 1
        if lab not in first:
            first[lab] = pos
    best = None
    for lab in votes:
        if best is None or votes[lab] > votes[best] or (votes[lab] == votes[best] and first[lab] < first[best]):
            best = lab
    return best
""", [[[[0, 0], [1, 1], [5, 5], [6, 6]], ["a", "a", "b", "b"], [0.5, 0.5], 3], [[[0, 0], [1, 1], [5, 5], [6, 6]], ["a", "a", "b", "b"], [5.5, 5.5], 1], [[[0], [2], [3], [10]], ["x", "y", "y", "x"], [2.4], 3]], "Sort by distance and vote.", approx=None),
  PL("Gradient step", "Write gd_line(xs, ys, w, b, lr, steps): fit y = w x + b by gradient descent on mean squared error, starting from w and b, for the given number of steps. Return [w, b] rounded to 6 decimals.",
     "gd_line(xs, ys, w, b, lr, steps)", """
def gd_line(xs, ys, w, b, lr, steps):
    n = len(xs)
    for _ in range(steps):
        gw = 0.0
        gb = 0.0
        for x, y in zip(xs, ys):
            e = w * x + b - y
            gw += 2 * e * x / n
            gb += 2 * e / n
        w -= lr * gw
        b -= lr * gb
    return [round(w, 6), round(b, 6)]
""", [[[0, 1, 2, 3], [1, 3, 5, 7], 0.0, 0.0, 0.05, 2000], [[1, 2, 3], [2, 4, 6], 0.0, 0.0, 0.05, 1], [[0, 1], [0, 0], 1.0, 1.0, 0.1, 10]], "Average the gradients.", approx=1e-5)]))

C.append(CH(
 "Neural networks and reinforcement learning",
 ("Deep learning", [
  "Neuron | computes | Weighted sum plus activation", "Backpropagation | computes | Gradients", "Convolution | shares | Weights across positions", "Transformer | uses | Attention",
  "Reward | guides | Reinforcement learning", "Q-learning | learns | Action values", "Exploration | trades with | Exploitation"]),
 ["Neural networks stack layers of simple units. Each unit takes a weighted sum of its inputs and applies a nonlinearity such as ReLU. Back-propagation applies the chain rule backward to get the gradient of the loss for every weight.",
  "Convolutional networks suit images, sharing small filters across positions. Transformers use attention and power modern language models. Reinforcement learning learns from rewards, not labelled answers: Q-learning estimates the value of each action in each state by temporal-difference updates.",
  "The labs write a small forward pass, a softmax and a Q-learning update."],
 [("Activation function", "A nonlinearity such as ReLU or sigmoid."), ("Back-propagation", "Chain-rule gradient computation, output to input."), ("Convolution", "A small filter slid over an image."),
  ("Attention", "A weighted focus on relevant inputs."), ("Reward", "A scalar signal of how well the agent is doing."), ("Q-value", "The expected return of taking an action in a state.")],
 ["A unit: output = activation(w . x + b).", "Without nonlinear activations, many layers collapse into one linear map.", "Training: forward pass, loss, back-propagation, weight update.",
  "Regularisers: dropout, weight decay, data augmentation.", "Q-learning: Q(s,a) += alpha (r + gamma max Q(s',a') - Q(s,a)).", "Explore with epsilon-greedy; exploit by taking the best known action."],
 [T("A neuron takes numbers in, multiplies each by a weight, adds them and a bias, and passes the sum through a nonlinear function. One neuron can draw a line between two classes. Many layers can draw complex shapes, because the nonlinearity prevents the layers from collapsing into a single linear map."),
  T("Training adjusts the weights to reduce a loss. The forward pass computes the output and the loss. Back-propagation uses the chain rule to find how the loss changes with each weight, working from the output back to the input. A gradient step then nudges all weights. Doing this on mini-batches is stochastic gradient descent."),
  T("Special architectures use structure. A convolutional network slides small filters over an image, so it detects an edge anywhere with the same weights. Recurrent networks and especially transformers handle sequences. A transformer lets every position attend to every other, weighing how relevant each is."),
  T("Reinforcement learning has no teacher with correct answers. The agent acts, receives rewards and learns what works. Its objective is the total discounted reward. It must balance exploring new actions with exploiting what it knows. A simple rule, epsilon-greedy, takes a random action with small probability."),
  M(r"Q(s,a) \;\leftarrow\; Q(s,a) + \alpha\bigl[\,r + \gamma \max_{a'} Q(s',a') - Q(s,a)\,\bigr]"),
  T("Q-learning applies this update after each step. The bracket is the temporal-difference error: the gap between what we just observed plus the best estimate afterwards, and what we predicted. Deep Q-networks use a neural network in place of a table. Policy-gradient methods adjust a policy directly, and human feedback can train the reward itself.")],
 [("Why do networks need nonlinear activations?", ["Otherwise layers collapse to one linear map", "To save memory", "To avoid bias terms", "To speed up data loading"], 0, "Linear layers compose to a linear layer."),
  ("What does back-propagation compute?", ["Gradients of the loss for each weight", "The data labels", "The learning rate", "The architecture"], 0, "Via the chain rule."),
  ("What does the TD error compare?", ["Observed return estimate with the current prediction", "Two policies", "Two networks", "Train and test data"], 0, "It drives the update.")],
 [("What does a convolution share?", "Weights across positions."), ("What is epsilon-greedy?", "Random action with small probability."), ("What is dropout?", "Randomly zeroing units while training."), ("What does attention do?", "Weights inputs by relevance.")],
 [ORDER("Training step", "Put one training step in order.", ["Run the forward pass", "Compute the loss", "Back-propagate gradients", "Update the weights"]),
  PL("Neuron", "Write neuron(w, x, b): return ReLU of the weighted sum w . x plus b, as a number rounded to 9 decimals.",
     "neuron(w, x, b)", """
def neuron(w, x, b):
    s = b
    for a, c in zip(w, x):
        s += a * c
    if s < 0:
        s = 0.0
    return round(s, 9)
""", [[[1, 2], [3, 4], 0.5], [[1, -1], [1, 5], 0], [[0.5], [2], -3], [[], [], 1.25]], "Weighted sum, then max with zero.", approx=1e-9),
  PL("Softmax", "Write softmax(z): return the list of exp(z_i) divided by the sum, each rounded to 9 decimals. Subtract the maximum first for stability. Use import math.",
     "softmax(z)", """
import math
def softmax(z):
    m = max(z)
    e = [math.exp(v - m) for v in z]
    t = sum(e)
    return [round(v / t, 9) for v in e]
""", [[[0.0, 0.0]], [[1.0, 2.0, 3.0]], [[1000.0, 1000.0]], [[-1.0, 0.0, 1.0, 2.0]]], "Shift by the max.", approx=1e-9),
  PL("Q-learning update", "Write q_update(Q, s, a, r, s2, alpha, gamma): Q is a dict from state to a dict from action to value. Update Q[s][a] in place by the Q-learning rule and return the new value rounded to 9 decimals.",
     "q_update(Q, s, a, r, s2, alpha, gamma)", """
def q_update(Q, s, a, r, s2, alpha, gamma):
    best = max(Q[s2].values())
    Q[s][a] += alpha * (r + gamma * best - Q[s][a])
    return round(Q[s][a], 9)
""", [[{"x": {"l": 0.0, "r": 0.0}, "y": {"l": 1.0, "r": 2.0}}, "x", "r", 1.0, "y", 0.5, 0.9], [{"x": {"l": 1.0}, "y": {"l": 0.0}}, "x", "l", 0.0, "y", 0.1, 0.9], [{"s": {"a": 2.0, "b": 3.0}}, "s", "a", 1.0, "s", 0.5, 0.5]], "Move toward target by alpha.", approx=1e-9)]))

C.append(CH(
 "Language, perception, robots and the future of AI",
 ("Applied AI", [
  "Language model | predicts | The next word", "n-gram | counts | Word sequences", "Parsing | builds | Syntax trees", "Image edges | are | Intensity changes",
  "Stereo | gives | Depth", "Robot planning | works in | Configuration space", "Ethics | asks | Who is affected"]),
 ["Natural language processing starts with language models: probability distributions over word sequences. Simple n-gram models count short sequences. Neural models trained on huge text collections now generate fluent text, though they can still state falsehoods confidently.",
  "Computer vision recovers scene properties from images, using edges, motion, stereo and, above all, deep networks for recognition. Robots perceive, plan in a space of joint configurations, and control motors with feedback.",
  "AI also raises questions about fairness, privacy, safety and control. The textbook's closing view is that machines should be uncertain about human preferences, so they stay open to correction."],
 [("Language model", "A probability distribution over text."), ("n-gram", "A model that predicts a word from the previous n minus one words."), ("Perplexity", "How surprised a model is by test text; lower is better."),
  ("IoU", "Intersection over union of two boxes."), ("Configuration space", "One axis per joint of the robot."), ("Value alignment", "Making a machine's goals match human values.")],
 ["Smoothing stops unseen n-grams getting zero probability.", "Parsing assigns a grammatical structure; ambiguity is the main difficulty.", "Image classification, detection and segmentation use convolutional or transformer networks.",
  "Depth from stereo = focal length times baseline divided by disparity.", "Motion planning in configuration space; controllers such as PID close the loop.", "Fairness definitions can conflict when base rates differ."],
 [T("A language model assigns a probability to a sequence of words. The simplest kind, the bigram model, estimates the chance of each word given the previous one by counting in a large text. Unseen pairs would get probability zero, so we smooth the counts."),
  T("Modern models use embeddings, vectors that place similar words near each other, and a transformer with attention. They are pretrained on vast text to predict the next token, then adapted for tasks. They are fluent but can hallucinate: say things that sound right and are not supported."),
  T("Vision asks what is in an image. Edges are places where brightness changes sharply. Two cameras give depth: nearby points shift more between the images, so depth equals focal length times baseline over disparity. Deep networks classify images, detect objects with boxes scored by intersection over union, and segment pixels."),
  T("A robot arm with many joints moves in a high-dimensional configuration space, where each point fixes all joint angles. Planners such as probabilistic roadmaps and rapidly exploring random trees sample this space and connect free points. Controllers such as a PID loop use the error, its integral and its derivative to follow the plan. Robots also localise with particle filters and build maps at the same time, called SLAM."),
  T("Capable AI raises real concerns. Systems can be unfair if trained on biased data, and different fairness criteria cannot all hold when groups differ in base rates. Privacy, security and misuse matter. Safety means building systems that pursue what people truly want, not only what we wrote down."),
  T("The textbook closes with a proposal: build machines that are uncertain about human preferences and learn them from our behaviour. Such a machine has a reason to ask, to defer, and to allow itself to be switched off. The field's future depends on technical progress and on wise governance.")],
 [("What does a language model estimate?", ["Probability of word sequences", "Image depth", "Robot torque", "Utility of money"], 0, "It predicts text."),
  ("How do two cameras give depth?", ["Through disparity between the images", "By counting edges", "By colour", "By motion blur"], 0, "Depth = f B / d."),
  ("Why might a safe AI be uncertain about its objective?", ["So it stays open to human correction", "To run faster", "To avoid learning", "To use less data"], 0, "That gives it reason to defer.")],
 [("What is hallucination?", "Fluent but unsupported output."), ("What is SLAM?", "Mapping while localising."), ("What is perplexity?", "Surprise on test text."), ("Why smooth n-gram counts?", "To avoid zero probabilities.")],
 [MATCH("Areas", "Match each tool with its job.", [("n-gram model", "Predict the next word from counts"), ("IoU", "Score overlap of boxes"), ("PID controller", "Follow a target with feedback"), ("Particle filter", "Locate a robot on a map")]),
  PL("Bigram probability", "Write bigram_prob(text, prev, word): text is a list of words. Return count(prev followed by word) divided by count(prev as the first of a pair); 0 if prev never starts a pair. Round to 9 decimals.",
     "bigram_prob(text, prev, word)", """
def bigram_prob(text, prev, word):
    c = 0
    d = 0
    for i in range(len(text) - 1):
        if text[i] == prev:
            d += 1
            if text[i + 1] == word:
                c += 1
    if d == 0:
        return 0.0
    return round(c / d, 9)
""", [[["the", "cat", "sat", "on", "the", "mat"], "the", "cat"], [["the", "cat", "sat", "on", "the", "mat"], "the", "dog"], [["a", "b", "a", "b", "a", "c"], "a", "b"], [["x"], "x", "y"]], "Count pairs.", approx=1e-9),
  PL("IoU", "Write iou(a, b): a and b are boxes [x1, y1, x2, y2] with x1 < x2 and y1 < y2. Return intersection area divided by union area, rounded to 9 decimals.",
     "iou(a, b)", """
def iou(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    inter = 0.0
    if w > 0 and h > 0:
        inter = w * h
    ua = (a[2] - a[0]) * (a[3] - a[1])
    ub = (b[2] - b[0]) * (b[3] - b[1])
    return round(inter / (ua + ub - inter), 9)
""", [[[0, 0, 2, 2], [1, 1, 3, 3]], [[0, 0, 1, 1], [2, 2, 3, 3]], [[0, 0, 2, 2], [0, 0, 2, 2]], [[0, 0, 4, 4], [1, 1, 2, 2]]], "Overlap width and height.", approx=1e-9),
  PL("Stereo depth", "Write depth(f, baseline, disparity): return f times baseline divided by disparity, rounded to 6 decimals.",
     "depth(f, baseline, disparity)", """
def depth(f, baseline, disparity):
    return round(f * baseline / disparity, 6)
""", [[700, 0.1, 10], [500, 0.5, 25], [1000, 0.2, 8]], "One formula.", approx=1e-6)]))
