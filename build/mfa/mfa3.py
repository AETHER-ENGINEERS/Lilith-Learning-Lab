"""Mathematics for CS and AI, part 3: statistics, information theory, Markov chains, algebra, category theory, type theory."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Statistics: estimation, likelihood and hypothesis tests",
 ("Statistics", [
  "Sample | estimates | A population",
  "Likelihood | scores | Parameters",
  "MLE | maximises | Likelihood",
  "MAP | adds | A prior",
  "Confidence interval | brackets | An estimate",
  "p-value | measures | Surprise under the null",
  "Bias-variance | trades | Fit against stability"]),
 ["Statistics goes from data back to the world. We draw a sample and estimate properties of the population. The likelihood scores how well a parameter explains the data, and maximum likelihood picks the best parameter. A prior adds earlier belief, giving the MAP estimate.",
  "A confidence interval says how precise an estimate is. A hypothesis test asks whether the data would be surprising if nothing were going on. The bias-variance trade-off explains overfitting and underfitting in machine learning.",
  "The labs compute estimates, a maximum-likelihood coin bias, a confidence interval, a z statistic and a bias-variance example."],
 [("Estimator", "A rule that computes a parameter guess from data."),
  ("Likelihood", "P(data | parameter) viewed as a function of the parameter."),
  ("MLE", "The parameter value that maximises the likelihood."),
  ("MAP", "The mode of the posterior: likelihood times prior."),
  ("Confidence interval", "A range built to contain the true value with stated frequency."),
  ("p-value", "The chance of data at least this extreme if the null hypothesis is true.")],
 ["Sample mean estimates the mean; sample variance divides by n - 1.",
  "For a coin with k heads in n flips, the MLE of p is k/n.",
  "95 percent interval for a mean: mean +/- 1.96 s/sqrt(n).",
  "z = (mean - mu0) / (s / sqrt(n)).",
  "MSE = bias^2 + variance (+ noise).",
  "Least squares is the MLE under Gaussian noise."],
 [T("You cannot ask every voter, so you ask a sample and estimate. The sample mean is an estimator of the population mean. It is unbiased, and its error shrinks with the square root of the sample size. For the variance we divide by n minus one, which corrects for using the same data to find the mean."),
  T("The likelihood turns the question around. Fix the data and ask: how plausible is each value of the parameter? For a coin that gave seven heads in ten flips, the likelihood of a bias p peaks at p equals 0.7. Choosing the peak is maximum likelihood estimation. Many familiar methods are special cases; least squares is maximum likelihood with Gaussian noise."),
  M(r"\hat\theta_{\text{MLE}} = \arg\max_\theta\, P(D\mid\theta), \qquad \hat\theta_{\text{MAP}} = \arg\max_\theta\, P(D\mid\theta)\,P(\theta)"),
  T("Adding a prior gives the maximum a posteriori estimate. A prior that prefers small weights turns into weight decay in neural networks. With little data the prior matters a lot; with lots of data the likelihood wins."),
  T("A confidence interval reports the precision of an estimate. For a mean it is the estimate plus or minus about two standard errors. A hypothesis test starts from a null, such as the new drug does nothing, and asks how surprising the data would be if it were true. A small p-value means surprising. It does not give the probability that the null is true, a common mistake."),
  M(r"\mathrm{MSE} = \mathrm{bias}^2 + \mathrm{variance} + \text{noise}"),
  T("The bias-variance trade-off is the central idea of learning from data. A simple model is stable but may miss the pattern, which is bias. A flexible model fits the sample but changes wildly with new data, which is variance. Total error combines both. Good practice balances them using held-out data.")],
 [("What is the MLE of a coin's bias after k heads in n flips?", ["k/n", "n/k", "0.5", "k"], 0, "The peak of the likelihood."),
  ("What does a small p-value mean?", ["Data would be surprising under the null", "The null is false for sure", "The effect is large", "The sample is small"], 0, "Not the chance the null is true."),
  ("What does MAP add to MLE?", ["A prior", "More data", "A test", "A mean"], 0, "Likelihood times prior."),
  ("What is overfitting in these terms?", ["High variance", "High bias", "No noise", "A prior"], 0, "Fits noise.")],
 [("Why n - 1?", "Corrects for estimating the mean from the same data."), ("Least squares is?", "MLE with Gaussian noise."), ("Interval width?", "About two standard errors."), ("Prior as weight decay?", "A prior preferring small weights.")],
 [PL("Sample mean and variance", "Write stats(xs): return [mean, sample variance with n-1] rounded to 6 decimals.",
     "stats(xs)", """
def stats(xs):
    n = len(xs)
    m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / (n - 1)
    return [round(m, 6), round(v, 6)]
""", [[[1, 2, 3, 4, 5]], [[2, 2, 2]], [[1, 3]], [[10, 20, 30, 40]]], "Divide by n - 1 for variance.", approx=1e-6),
  PL("Coin MLE by grid search", "Write mle_coin(k, n): over p = 0.00, 0.01, ... 1.00, return the p that maximises p^k (1-p)^(n-k) (first best), rounded to 2 decimals.",
     "mle_coin(k, n)", """
def mle_coin(k, n):
    best = 0.0
    bp = 0.0
    for i in range(101):
        p = i / 100.0
        l = p ** k * (1 - p) ** (n - k)
        if l > best:
            best = l
            bp = p
    return round(bp, 2)
""", [[7, 10], [0, 5], [5, 5], [3, 12]], "The peak is at k/n."),
  PL("Confidence interval", "Write ci(xs): the 95 percent interval of the mean, [low, high], using 1.96 s / sqrt(n) with n-1 variance, rounded to 4 decimals. Use import math.",
     "ci(xs)", """
import math
def ci(xs):
    n = len(xs)
    m = sum(xs) / n
    s = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    h = 1.96 * s / math.sqrt(n)
    return [round(m - h, 4), round(m + h, 4)]
""", [[[1, 2, 3, 4, 5]], [[10, 12, 11, 13, 9, 10]], [[5, 5, 5, 6]]], "Mean plus or minus two standard errors.", approx=1e-4),
  PL("z statistic", "Write zstat(xs, mu0): (mean - mu0) / (s / sqrt n) with n-1 variance, rounded to 4 decimals. Use import math.",
     "zstat(xs, mu0)", """
import math
def zstat(xs, mu0):
    n = len(xs)
    m = sum(xs) / n
    s = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return round((m - mu0) / (s / math.sqrt(n)), 4)
""", [[[1, 2, 3, 4, 5], 2], [[10, 12, 11, 13, 9, 10], 10], [[5, 6, 7], 5]], "Distance from the null in standard errors.", approx=1e-4),
  ORDER("Hypothesis test", "Order the steps.", ["State the null hypothesis", "Choose a test statistic", "Compute it from the data", "Find the p-value", "Decide against a chosen threshold"]),
  MATCH("Statistics", "Match each term with its meaning.", [("MLE", "Peak of the likelihood"), ("MAP", "Peak with a prior"), ("p-value", "Surprise under the null"), ("Bias", "Systematic error"), ("Variance", "Sensitivity to the sample")]),
  FILL("Estimation", "Maximum likelihood chooses the parameter that makes the data most {{likely|probable}}; MAP adds a {{prior}}.")]))

CHS.append(CH(
 "Information theory: entropy, cross-entropy and KL divergence",
 ("Information", [
  "Surprise | is | -log p",
  "Entropy | averages | Surprise",
  "Cross-entropy | scores | A model",
  "KL divergence | measures | Distribution gap",
  "Mutual information | measures | Shared information",
  "Bit | is | One yes-no answer",
  "Compression | is limited by | Entropy"]),
 ["Information theory measures uncertainty and information in bits. A rare event is more surprising than a common one, so surprise is minus the log of the probability. Entropy is the average surprise of a distribution: how unpredictable it is.",
  "Cross-entropy measures the cost of coding data from one distribution with a model of another, and is the standard loss for classifiers and language models. The KL divergence is the extra cost, a measure of how far a model is from the truth. Mutual information measures what two variables share.",
  "The labs compute entropy, cross-entropy, KL divergence and mutual information."],
 [("Surprise", "-log2 p(x) bits."),
  ("Entropy", "H(p) = -sum p log p."),
  ("Cross-entropy", "H(p, q) = -sum p log q."),
  ("KL divergence", "D(p || q) = sum p log (p/q) = H(p, q) - H(p)."),
  ("Mutual information", "I(X;Y) = H(X) + H(Y) - H(X, Y)."),
  ("Bit", "The information in one fair yes-no answer.")],
 ["A fair coin has entropy 1 bit; a certain event has 0.",
  "Entropy is maximal for the uniform distribution: log2 n.",
  "KL divergence is never negative and zero only when p = q.",
  "KL is not symmetric: D(p||q) differs from D(q||p).",
  "Minimising cross-entropy over q equals minimising KL to p.",
  "Shannon: no lossless code beats the entropy on average."],
 [T("Suppose someone tells you it rained in a desert. That is surprising, so it carries a lot of information. Learning that the sun rose tells you nothing. Shannon captured this: the information of an event with probability p is minus the log of p. With base two logs it is measured in bits, the number of yes-no questions needed."),
  M(r"H(p) = -\sum_x p(x)\log_2 p(x), \qquad H(p,q) = -\sum_x p(x)\log_2 q(x)"),
  T("Entropy is the average surprise: how many bits you need on average to say which outcome happened. A fair coin has one bit. A coin that is almost always heads has little. A uniform choice among n options has log of n bits, the most possible. Entropy is also a hard limit on lossless compression."),
  T("Now suppose reality follows p but you code using a model q. The average cost is the cross-entropy, which is always at least the entropy. Training a classifier or a language model with cross-entropy loss means making the model's distribution match the data. The excess cost is the KL divergence."),
  M(r"D_{\mathrm{KL}}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p) \;\ge\; 0"),
  T("KL divergence is not a true distance, since it is not symmetric, but it is zero only when the distributions agree. It appears in variational autoencoders, in PPO's trust region and in DPO's regulariser. Mutual information measures how much knowing one variable reduces uncertainty about another, the foundation of feature selection and representation learning.")],
 [("Entropy of a fair coin?", ["1 bit", "0 bits", "2 bits", "0.5 bits"], 0, "Maximum for two outcomes."),
  ("Is KL divergence symmetric?", ["No", "Yes", "Only for coins", "Always zero"], 0, "D(p||q) differs from D(q||p)."),
  ("What does cross-entropy loss minimise?", ["The gap to the data distribution", "The data size", "The entropy of data", "The learning rate"], 0, "Equivalent to KL."),
  ("What is the lowest KL value?", ["0", "-1", "1", "Infinity"], 0, "Only when p = q.")],
 [("Surprise of probability 1/8?", "3 bits."), ("Compression limit?", "The entropy."), ("KL in RL?", "Trust region and regularisation."), ("Mutual information zero?", "Independent variables.")],
 [PL("Entropy", "Write entropy(p): entropy in bits of a probability list (ignore zeros), rounded to 6 decimals. Use import math.",
     "entropy(p)", """
import math
def entropy(p):
    h = 0.0
    for x in p:
        if x > 0:
            h -= x * math.log(x) / math.log(2)
    return round(h, 6)
""", [[[0.5, 0.5]], [[1.0]], [[0.25, 0.25, 0.25, 0.25]], [[0.9, 0.1]]], "Average surprise.", approx=1e-6),
  PL("Cross-entropy", "Write cross_ent(p, q): -sum p log2 q in bits, rounded to 6 decimals. Use import math.",
     "cross_ent(p, q)", """
import math
def cross_ent(p, q):
    h = 0.0
    for a, b in zip(p, q):
        if a > 0:
            h -= a * math.log(b) / math.log(2)
    return round(h, 6)
""", [[[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.9, 0.1]], [[1.0, 0.0], [0.8, 0.2]]], "Code with the wrong model.", approx=1e-6),
  PL("KL divergence", "Write kl(p, q): D(p||q) in bits for lists with q > 0 wherever p > 0, rounded to 6 decimals. Use import math.",
     "kl(p, q)", """
import math
def kl(p, q):
    d = 0.0
    for a, b in zip(p, q):
        if a > 0:
            d += a * math.log(a / b) / math.log(2)
    return round(d, 6)
""", [[[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.9, 0.1]], [[0.9, 0.1], [0.5, 0.5]]], "Extra bits.", approx=1e-6),
  PL("Mutual information", "Write mi(joint): mutual information in bits of a joint table (list of rows summing to 1), rounded to 6 decimals. Use import math.",
     "mi(joint)", """
import math
def mi(joint):
    px = [sum(r) for r in joint]
    py = [sum(joint[i][j] for i in range(len(joint))) for j in range(len(joint[0]))]
    t = 0.0
    for i in range(len(joint)):
        for j in range(len(joint[0])):
            v = joint[i][j]
            if v > 0:
                t += v * math.log(v / (px[i] * py[j])) / math.log(2)
    return round(t, 6)
""", [[[[0.25, 0.25], [0.25, 0.25]]], [[[0.5, 0.0], [0.0, 0.5]]], [[[0.4, 0.1], [0.1, 0.4]]]], "How far from independent.", approx=1e-6),
  ORDER("Measuring a model", "Order the steps.", ["Take the true distribution p", "Take the model distribution q", "Compute the cross-entropy H(p, q)", "Subtract the entropy H(p)", "The remainder is the KL divergence"]),
  MATCH("Information", "Match each quantity with its meaning.", [("Entropy", "Average surprise"), ("Cross-entropy", "Cost with the wrong model"), ("KL divergence", "Extra bits"), ("Mutual information", "Shared information"), ("Bit", "One yes-no answer")]),
  FILL("Information", "Entropy is the average {{surprise}}; cross-entropy minus entropy equals the {{KL|Kullback-Leibler}} divergence.")]))

CHS.append(CH(
 "Markov chains and stochastic processes",
 ("Markov", [
  "State | describes | Where you are",
  "Transition matrix | holds | Move probabilities",
  "Markov property | forgets | The past",
  "Stationary distribution | is | The long-run mix",
  "Random walk | wanders | On a graph",
  "MDP | adds | Actions and rewards",
  "PageRank | is | A stationary distribution"]),
 ["A Markov chain moves between states with fixed probabilities where the next state depends only on the current one. A transition matrix lists the probabilities, and multiplying a distribution by it advances one step.",
  "Under mild conditions the chain forgets its start and settles into a stationary distribution. This idea gives PageRank, sampling methods such as MCMC, hidden Markov models and the Markov decision processes of reinforcement learning.",
  "The labs step a chain, compute its stationary distribution by iteration, simulate a random walk exactly by enumeration and evaluate a small MDP value."],
 [("Markov property", "The future depends on the present, not the past."),
  ("Transition matrix", "P_ij = chance of moving from i to j; rows sum to 1."),
  ("Stationary distribution", "A distribution pi with pi P = pi."),
  ("Ergodic", "Irreducible and aperiodic: converges to a unique stationary distribution."),
  ("MDP", "A Markov chain with actions and rewards."),
  ("Discount factor", "gamma < 1 weighs near rewards more than far rewards.")],
 ["A distribution evolves by pi_{t+1} = pi_t P.",
  "The stationary pi satisfies pi = pi P and sums to 1.",
  "n-step probabilities are entries of P^n.",
  "PageRank adds random jumps to guarantee a unique answer.",
  "MDP value: V(s) = max_a [R + gamma sum P V(s')].",
  "MCMC builds a chain whose stationary distribution is the target."],
 [T("Think of weather as sunny or rainy. If it is sunny today, there is a ninety percent chance of sun tomorrow; if rainy, a fifty percent chance of rain. Tomorrow depends only on today, not on last week. That memoryless rule is the Markov property. The probabilities form a transition matrix whose rows each sum to one."),
  M(r"\pi_{t+1} = \pi_t P, \qquad \pi = \pi P,\ \ \textstyle\sum_i \pi_i = 1"),
  T("If you start with a distribution over states, multiplying by the matrix gives the distribution one step later. Do it repeatedly and, for a well-behaved chain, the distribution converges to a fixed one, the stationary distribution, no matter where you started. It is the long-run share of time spent in each state."),
  T("A random walk on a graph, where you move to a random neighbour, is a Markov chain. PageRank models a web surfer who follows links at random and sometimes jumps to a random page; the stationary distribution ranks pages by how often the surfer visits. Markov chain Monte Carlo reverses the idea: design a chain whose stationary distribution is one you want to sample."),
  T("Add actions and rewards and you get a Markov decision process, the model behind reinforcement learning. The value of a state is the best expected total discounted reward from it, satisfying the Bellman equation. Q-learning and PPO, met in earlier courses, are ways of solving it."),
  M(r"V(s) = \max_a\Bigl[R(s,a) + \gamma\sum_{s'}P(s'\mid s,a)\,V(s')\Bigr]")],
 [("What is the Markov property?", ["The future depends only on the present", "The past matters most", "States are random", "Rewards are fixed"], 0, "Memoryless."),
  ("What sums to 1 in a transition matrix?", ["Each row", "Each column", "The diagonal", "Nothing"], 0, "Probabilities from a state."),
  ("What is a stationary distribution?", ["pi = pi P", "pi = 0", "P = I", "A start state"], 0, "Unchanged by a step."),
  ("What does PageRank compute?", ["A stationary distribution", "A median", "A sort", "A hash"], 0, "A random surfer.")],
 [("n-step probabilities?", "Entries of P^n."), ("MCMC idea?", "Chain whose stationary distribution is the target."), ("Bellman equation?", "Value from best action plus discounted next value."), ("Ergodic?", "Converges to a unique stationary distribution.")],
 [PL("One step", "Write step(pi, P): the distribution after one step, pi P, rounded to 6 decimals.",
     "step(pi, P)", """
def step(pi, P):
    n = len(pi)
    return [round(sum(pi[i] * P[i][j] for i in range(n)), 6) for j in range(n)]
""", [[[1, 0], [[0.9, 0.1], [0.5, 0.5]]], [[0.5, 0.5], [[0.9, 0.1], [0.5, 0.5]]], [[0.2, 0.3, 0.5], [[0, 1, 0], [0, 0, 1], [1, 0, 0]]]], "Row vector times matrix.", approx=1e-6),
  PL("Stationary distribution", "Write stationary(P, steps): start from the uniform distribution and apply pi P for steps iterations; return the distribution rounded to 4 decimals.",
     "stationary(P, steps)", """
def stationary(P, steps):
    n = len(P)
    pi = [1.0 / n] * n
    for _ in range(steps):
        pi = [sum(pi[i] * P[i][j] for i in range(n)) for j in range(n)]
    return [round(x, 4) for x in pi]
""", [[[[0.9, 0.1], [0.5, 0.5]], 100], [[[0.5, 0.5], [0.5, 0.5]], 5], [[[0.7, 0.3], [0.4, 0.6]], 200]], "Iterate until it settles.", approx=1e-3),
  PL("Probability of ending in a state", "Write after(P, start, n, target): the probability of being in state target after n steps from state start, rounded to 6 decimals.",
     "after(P, start, n, target)", """
def after(P, start, n, target):
    k = len(P)
    pi = [0.0] * k
    pi[start] = 1.0
    for _ in range(n):
        pi = [sum(pi[i] * P[i][j] for i in range(k)) for j in range(k)]
    return round(pi[target], 6)
""", [[[[0.9, 0.1], [0.5, 0.5]], 0, 1, 1], [[[0.9, 0.1], [0.5, 0.5]], 0, 3, 0], [[[0, 1], [1, 0]], 0, 5, 1]], "Evolve a point mass.", approx=1e-6),
  PL("Value of a two-step plan", "Write value(r1, r2, gamma): the discounted return r1 + gamma r2 + gamma^2 r2 + ... for rewards r1 then r2 forever, as r1 + gamma r2/(1 - gamma), rounded to 6 decimals.",
     "value(r1, r2, gamma)", """
def value(r1, r2, gamma):
    return round(r1 + gamma * r2 / (1 - gamma), 6)
""", [[1, 2, 0.5], [0, 1, 0.9], [5, 0, 0.99]], "A geometric series.", approx=1e-6),
  ORDER("PageRank idea", "Order the steps.", ["Model pages as states and links as moves", "Add random jumps", "Build the transition matrix", "Iterate pi = pi P until stable", "Rank pages by pi"]),
  MATCH("Markov", "Match each item with its meaning.", [("Markov property", "Memoryless"), ("Transition matrix", "Rows sum to 1"), ("Stationary distribution", "pi = pi P"), ("MDP", "Chain with actions and rewards"), ("Discount", "Weighs near rewards more")]),
  FILL("Markov", "A Markov chain's next state depends only on the {{current|present}} state; the long-run mix is the {{stationary}} distribution.")]))

CHS.append(CH(
 "Algebra and category theory",
 ("Algebra", [
  "Monoid | has | Associative product and identity",
  "Group | adds | Inverses",
  "Category | has | Objects and arrows",
  "Functor | maps | Categories",
  "Natural transformation | maps | Functors",
  "Monad | wraps | Effects",
  "Universal property | defines | By arrows"]),
 ["Algebra studies structures with operations. A monoid has an associative operation and a do-nothing element; a group also has inverses. These abstract patterns appear all over computing: strings under concatenation, numbers under addition, permutations and symmetries.",
  "Category theory goes one level up and studies structure by arrows alone. A category has objects and composable arrows. A functor maps one category to another preserving structure, which is exactly what a map over a list does. Monads package effects such as state and failure.",
  "The labs check monoid and group laws, implement a functor on lists and options, compose arrows and build a tiny monad."],
 [("Monoid", "A set with an associative operation and an identity element."),
  ("Group", "A monoid in which every element has an inverse."),
  ("Category", "Objects, arrows, composition and identities."),
  ("Functor", "A structure-preserving map between categories."),
  ("Monad", "A functor with unit and bind, modelling computation with effects."),
  ("Universal property", "Characterising an object by how arrows relate to it.")],
 ["Monoid laws: (a b) c = a (b c); e a = a e = a.",
  "Group: every a has an inverse with a a^-1 = e.",
  "Category: composition is associative; id composes neutrally.",
  "Functor laws: F(id) = id; F(g o f) = F(g) o F(f).",
  "Monad laws: left identity, right identity, associativity of bind.",
  "Product and sum types are universal constructions."],
 [T("A monoid is a very simple idea: a way to combine things, where grouping does not matter, plus a neutral element. Adding numbers with zero, joining strings with the empty string, and merging lists all fit. Because grouping does not matter, a monoid can be combined in parallel, which is why map-reduce works."),
  M(r"(a\cdot b)\cdot c = a\cdot(b\cdot c), \qquad e\cdot a = a\cdot e = a"),
  T("A group adds inverses: every element can be undone. The symmetries of a shape, the rotations of a cube and the integers under addition are groups. Groups describe symmetry, and symmetry is behind convolutional networks, which share weights across positions, and equivariant networks."),
  T("A category is a collection of objects and arrows between them, where arrows compose and each object has an identity arrow. Sets and functions form a category; so do types and programs. The idea is to ignore what objects contain and study how they connect. Two objects are the same, up to isomorphism, if there are arrows both ways that undo each other."),
  T("A functor maps a category into another, sending objects to objects and arrows to arrows, while respecting composition and identities. A list type with its map function is a functor: it turns a function from A to B into a function on lists of A to lists of B. A natural transformation maps between functors, such as turning an option into a list."),
  M(r"F(\mathrm{id}_A) = \mathrm{id}_{F(A)}, \qquad F(g\circ f) = F(g)\circ F(f)"),
  T("A monad is a functor with two operations: wrap a plain value, and chain computations that return wrapped values. It captures effects such as possible failure, state, logging or probability, while keeping code composable. A universal property defines something by how it relates to all others; the product of two types is the unique type with two projections.")],
 [("What does a monoid need?", ["Associativity and an identity", "Inverses", "Commutativity", "Division"], 0, "Group adds inverses."),
  ("What is a functor?", ["A structure-preserving map between categories", "A number", "A loop", "A type error"], 0, "Like map on lists."),
  ("Why do monoids parallelise well?", ["Grouping does not matter", "They are fast", "They are commutative", "They are small"], 0, "Associativity."),
  ("What do groups describe?", ["Symmetry", "Randomness", "Sorting", "Compression"], 0, "Undoable transformations.")],
 [("Functor law for composition?", "F(g o f) = F(g) o F(f)."), ("Is addition a monoid?", "Yes, with identity 0."), ("What is a natural transformation?", "A map between functors."), ("What is a monad for?", "Composable effects.")],
 [PL("Monoid laws check", "Write is_monoid(elems, table, e): elems is a list of 0..n-1, table[a][b] is the product, e the identity. Return 1 if the operation is associative and e is neutral, else 0.",
     "is_monoid(elems, table, e)", """
def is_monoid(elems, table, e):
    for a in elems:
        if table[e][a] != a or table[a][e] != a:
            return 0
        for b in elems:
            for c in elems:
                if table[table[a][b]][c] != table[a][table[b][c]]:
                    return 0
    return 1
""", [[[0, 1, 2], [[0, 1, 2], [1, 2, 0], [2, 0, 1]], 0], [[0, 1], [[0, 1], [1, 1]], 0], [[0, 1], [[1, 0], [0, 1]], 0]], "Check every triple."),
  PL("Inverses in Z_n", "Write has_inverses(n): 1 if every nonzero residue mod n has a multiplicative inverse (that is, n is prime), else 0.",
     "has_inverses(n)", """
def has_inverses(n):
    for a in range(1, n):
        ok = 0
        for b in range(1, n):
            if (a * b) % n == 1:
                ok = 1
        if not ok:
            return 0
    return 1
""", [[5], [6], [7], [9]], "Only primes work."),
  PL("Functor map on a list", "Write fmap_check(xs): apply the functor laws to lists with f(x) = x + 1 and g(x) = 2 x. Return 1 if map(g o f) equals map(g) after map(f) for the list xs, else 0.",
     "fmap_check(xs)", """
def fmap_check(xs):
    f = lambda x: x + 1
    g = lambda x: 2 * x
    left = [g(f(x)) for x in xs]
    right = [g(y) for y in [f(x) for x in xs]]
    return 1 if left == right else 0
""", [[[1, 2, 3]], [[]], [[0]]], "Composition is preserved."),
  PL("Option monad bind", "Represent an option as a list: [] is none, [x] is some x. Write run(x): compute halve then dec where halve(n) = [n/2] if n is even else [], and dec(n) = [n-1] if n > 0 else []. Return the final option via bind.",
     "run(x)", """
def run(x):
    def halve(n):
        return [n // 2] if n % 2 == 0 else []
    def dec(n):
        return [n - 1] if n > 0 else []
    def bind(m, f):
        return f(m[0]) if m else []
    return bind(bind([x], halve), dec)
""", [[8], [7], [0], [2]], "Stop at the first none."),
  ORDER("Check a functor", "Order the steps.", ["Map objects to objects", "Map arrows to arrows", "Check identities are preserved", "Check composition is preserved", "Conclude it is a functor"]),
  MATCH("Algebra", "Match each structure with its description.", [("Monoid", "Associative with identity"), ("Group", "Monoid with inverses"), ("Category", "Objects and arrows"), ("Functor", "Maps categories"), ("Monad", "Composable effects")]),
  FILL("Category", "A functor must preserve identities and {{composition}}; a group is a monoid where every element has an {{inverse}}.")]))

CHS.append(CH(
 "Type theory and the lambda calculus",
 ("Types", [
  "Lambda | builds | Functions",
  "Application | applies | A function",
  "Type | classifies | A term",
  "Beta reduction | computes | A result",
  "Curry-Howard | links | Proofs and programs",
  "Dependent type | mentions | Values",
  "Proof assistant | checks | Proofs"]),
 ["The lambda calculus is the smallest programming language: just functions and application. A function is written with lambda, and applying it substitutes the argument. Everything computable can be expressed in it.",
  "Types classify terms and rule out nonsense, like adding a string to a number. The Curry-Howard correspondence says types are propositions and programs are proofs. Dependent types let types mention values, and proof assistants use them to check mathematics by computer.",
  "The labs evaluate lambda terms with Church numerals, type-check tiny expressions and implement a Boolean type."],
 [("Lambda term", "A variable, a function (lambda x. body), or an application (f a)."),
  ("Beta reduction", "(lambda x. t) a reduces to t with a for x."),
  ("Type", "A label saying what kind of value a term is."),
  ("Church numeral", "The number n encoded as n-fold function application."),
  ("Curry-Howard", "Propositions are types; proofs are programs."),
  ("Dependent type", "A type that depends on a value.")],
 ["Syntax: x | lambda x. t | t u.",
  "Beta: (lambda x. t) u -> t[x := u].",
  "Typing: if x : A and t : B then lambda x. t : A -> B.",
  "Church numerals: n = lambda f. lambda x. f^n x.",
  "A -> B reads as 'A implies B'; a pair type reads as 'and'; a sum type as 'or'.",
  "Simply typed terms always terminate."],
 [T("The lambda calculus has only three things: variables, functions and applications. A function that adds one is written lambda x dot x plus one. Applying it to three replaces x by three. This replacement is called beta reduction, and repeating it is how computation happens. Remarkably, this tiny system can express every computable function."),
  M(r"(\lambda x.\,t)\,u \;\to_\beta\; t[x := u]"),
  T("Even numbers can be built from functions. The Church numeral for n is the function that applies another function n times. Addition and multiplication follow by composing these. Booleans work too: true picks the first of two choices and false picks the second."),
  T("Types make programs safer. A type says what kind of thing a term is; a function from A to B takes an A and gives a B. A type checker rejects terms that do not fit, such as applying a number as if it were a function. In the simply typed calculus every well-typed program terminates, which is both a strength and a limit."),
  M(r"\frac{x:A \vdash t:B}{\vdash \lambda x.\,t : A\to B}, \qquad \frac{\vdash f:A\to B \quad \vdash a:A}{\vdash f\,a : B}"),
  T("Here is the deep connection. The rules above, read as logic, are the rules for implication: a function from A to B is a proof that A implies B, and applying it is modus ponens. A pair of values is a proof of and; a tagged choice is a proof of or. This is the Curry-Howard correspondence, and it explains why running a program and simplifying a proof are the same process."),
  T("Dependent types go further by letting types mention values, such as a list of exactly n items. They can express precise specifications, and with them for all and there exists become types. Proof assistants such as Lean and Coq are built on this: if the proof type-checks, the theorem holds. They have verified compilers, operating-system kernels and parts of modern mathematics.")],
 [("What is beta reduction?", ["Substituting an argument into a function body", "Adding types", "Sorting", "Looping"], 0, "How computation happens."),
  ("What does A -> B correspond to in logic?", ["A implies B", "A and B", "A or B", "Not A"], 0, "Curry-Howard."),
  ("What is a Church numeral?", ["A number as repeated application", "A type", "A list", "A loop"], 0, "n times f."),
  ("What does a proof assistant do?", ["Type-checks proofs", "Guesses theorems", "Sorts lists", "Draws graphs"], 0, "If it checks, the theorem holds.")],
 [("Pair type means?", "Logical and."), ("Sum type means?", "Logical or."), ("Dependent type example?", "A vector of length n."), ("Does simply typed calculus loop forever?", "No, terms terminate.")],
 [PL("Church numerals", "Represent a Church numeral n by a function. Write church_add(a, b): build the numerals for a and b as functions (apply f n times), add them (apply f a times, then b times), and return the integer obtained by applying the sum to the successor function and 0.",
     "church_add(a, b)", """
def church_add(a, b):
    def num(n):
        return lambda f: lambda x: _rep(n, f, x)
    def _rep(n, f, x):
        for _ in range(n):
            x = f(x)
        return x
    def add(m, k):
        return lambda f: lambda x: m(f)(k(f)(x))
    s = add(num(a), num(b))
    return s(lambda v: v + 1)(0)
""", [[2, 3], [0, 0], [5, 7], [10, 0]], "Apply f a times then b times."),
  PL("Church booleans", "True picks its first argument and false its second. Write church_if(c, a, b): c is 1 for true or 0 for false; return a if true else b by using the Church functions.",
     "church_if(c, a, b)", """
def church_if(c, a, b):
    T = lambda x: lambda y: x
    F = lambda x: lambda y: y
    cond = T if c == 1 else F
    return cond(a)(b)
""", [[1, 10, 20], [0, 10, 20], [1, 5, 5]], "A boolean is a chooser."),
  PL("Type-check a tiny expression", "Types are 'int' or 'fun' (a function int->int). Expressions are lists: ['num'], ['inc'], or ['app', f, x] meaning f applied to x. Write check(e): return 1 if e is well typed (app needs f of type fun and x of type int), else 0.",
     "check(e)", """
def typeof(e):
    if e[0] == 'num':
        return 'int'
    if e[0] == 'inc':
        return 'fun'
    if e[0] == 'app':
        f = typeof(e[1])
        x = typeof(e[2])
        if f == 'fun' and x == 'int':
            return 'int'
        return 'bad'
    return 'bad'
def check(e):
    return 0 if typeof(e) == 'bad' else 1
""", [[['num']], [['app', ['inc'], ['num']]], [['app', ['num'], ['num']]], [['app', ['inc'], ['inc']]], [['app', ['inc'], ['app', ['inc'], ['num']]]]], "Types guard application."),
  PL("Normalise a unary term", "Terms are nested lists: 0 for zero or ['s', t] for successor. Write to_int(t): the number of successors, a tiny proof-by-induction function.",
     "to_int(t)", """
def to_int(t):
    n = 0
    while t != 0:
        t = t[1]
        n += 1
    return n
""", [[0], [['s', 0]], [['s', ['s', ['s', 0]]]]], "Recursion mirrors induction."),
  ORDER("Evaluate a lambda term", "Order the steps to evaluate (lambda x. x + 1) 3.", ["Find the application", "Take the function body x + 1", "Substitute 3 for x", "Get 3 + 1", "Compute 4"]),
  MATCH("Types", "Match each type-theory idea with its logic reading.", [("Function type A -> B", "A implies B"), ("Pair type", "A and B"), ("Sum type", "A or B"), ("Program", "Proof"), ("Beta reduction", "Proof simplification")]),
  FILL("Curry-Howard", "A program of type A -> B is a proof that A {{implies}} B; the lambda calculus computes by {{beta|substitution}} reduction.")]))
