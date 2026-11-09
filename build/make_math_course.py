#!/usr/bin/env python3
"""Build the Mathematics for CS and AI course. Usage: python3 make_math_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mfa"))
import cmk, mfa1, mfa2, mfa3  # noqa: E402

CHS = mfa1.CHS + mfa2.CHS + mfa3.CHS

PRONOUNCE = {
    "SVD": "S V D", "PCA": "P C A", "MLE": "M L E", "MAP": "map", "KL": "K L", "CLT": "C L T", "MCMC": "M C M C", "MDP": "M D P",
    "RSA": "R S A", "BFS": "B F S", "DFS": "D F S", "GCD": "G C D", "gcd": "G C D", "PageRank": "page rank", "SGD": "S G D",
    "Eratosthenes": "air uh tos thuh neez", "Gaussian": "gow see an", "Bernoulli": "ber noo lee", "Kolmogorov": "kol muh gor off",
    "Jacobian": "jah co bee an", "Hessian": "hess ee an", "Lagrange": "lah grahnj", "eigenvalue": "eye gen value", "eigenvector": "eye gen vector",
    "Eigen": "eye gen", "Euclid's": "yoo klids", "Euclid": "yoo klid", "Shannon": "shannon", "Bayes": "bays", "Bayes'": "bays", "Markov": "mar koff",
    "monoid": "mon oid", "functor": "funk tor", "monad": "moe nad", "Curry-Howard": "curry howard", "Coq": "coke", "Lean": "lean",
    "lambda": "lam duh", "Pascal's": "pas kals", "Cauchy-Schwarz": "co shee shvarts", "Fermat's": "fair mahs", "Fermat": "fair mah",
    "isomorphism": "eye so mor fism", "bijection": "by jek shun", "injective": "in jek tiv", "surjective": "sur jek tiv",
}

SANDBOX = cmk.terminal("Math lookup", "m>", "A scripted lookup of formulas, not a calculator. Try: bayes, chain, entropy, eigen, group", [
    ("bayes", ["P(H|E) = P(E|H) P(H) / P(E)", "posterior is proportional to likelihood times prior"]),
    ("chain", ["dy/dx = dy/du * du/dx", "backprop multiplies Jacobians from the loss backwards"]),
    ("entropy", ["H(p) = -sum p log2 p", "cross-entropy H(p,q) = H(p) + KL(p||q)"]),
    ("eigen", ["A v = lambda v", "det(A - lambda I) = 0"]),
    ("group", ["closure, associativity, identity, inverses", "a monoid drops inverses"]),
    ("gradient", ["grad f points uphill", "descent: x <- x - lr * grad f(x)"]),
])

EXAM = [
 ("When is p implies q false?", ["p true and q false", "p false and q true", "Both false", "Both true"], 0, "The only failing row."),
 ("What does induction need?", ["A base case and a step", "Only examples", "A contradiction", "A counterexample"], 0, "Then every n follows."),
 ("How many subsets does a set of 5 elements have?", ["32", "10", "25", "120"], 0, "2^5."),
 ("What is a bijection?", ["Injective and surjective", "Only injective", "Only surjective", "Any relation"], 0, "It has an inverse."),
 ("How many orderings of 4 distinct items?", ["24", "16", "12", "4"], 0, "4!."),
 ("What is C(6, 2)?", ["15", "12", "30", "8"], 0, "6!/(2!4!)."),
 ("What do the degrees of a graph sum to?", ["Twice the number of edges", "The number of edges", "The number of vertices", "Zero"], 0, "Handshake lemma."),
 ("How many edges has a tree on n vertices?", ["n - 1", "n", "n + 1", "n squared"], 0, "Connected and acyclic."),
 ("What is gcd(48, 18)?", ["6", "3", "12", "9"], 0, "Euclid."),
 ("What does Fermat's little theorem give?", ["Inverses modulo a prime", "Prime factors", "Square roots", "Logarithms"], 0, "a^(p-2)."),
 ("What does the dot product of orthogonal vectors equal?", ["0", "1", "Their length", "Undefined"], 0, "cos 90 = 0."),
 ("What is (AB) transpose?", ["B transpose times A transpose", "A transpose times B transpose", "AB", "BA"], 0, "Order reverses."),
 ("What does det = 0 mean?", ["The matrix is not invertible", "It is the identity", "All entries are zero", "It is symmetric"], 0, "Space is flattened."),
 ("What is an eigenvector?", ["A direction only stretched by the matrix", "A zero vector", "A row of a matrix", "A determinant"], 0, "A v = lambda v."),
 ("What does PCA find?", ["Directions of greatest variance", "The mean", "Outliers only", "Labels"], 0, "Top covariance eigenvectors."),
 ("What does the derivative measure?", ["Instantaneous rate of change", "Total area", "The average", "The maximum"], 0, "Slope of the tangent."),
 ("Which rule differentiates a composition?", ["Chain rule", "Product rule", "Power rule", "Sum rule"], 0, "Outer times inner."),
 ("What is backpropagation?", ["The chain rule applied from the loss backwards", "Random search", "Sorting", "Clustering"], 0, "Multiply local slopes."),
 ("What does the gradient point toward?", ["Steepest increase", "Steepest decrease", "A minimum", "Zero"], 0, "Uphill."),
 ("What is dL/dx for y = W x?", ["W transpose times dL/dy", "W times dL/dy", "x", "Zero"], 0, "Backward through a linear layer."),
 ("What does gradient descent do?", ["Steps against the gradient", "Steps along the gradient", "Picks randomly", "Sorts data"], 0, "Downhill."),
 ("What is special about convex functions?", ["Every local minimum is global", "They have no minimum", "They have two valleys", "Their gradient is zero"], 0, "One valley."),
 ("What does a Lagrange multiplier handle?", ["Constraints", "Noise", "Sorting", "Overflow"], 0, "Parallel gradients."),
 ("What is P(not A)?", ["1 - P(A)", "P(A)", "0", "P(A) squared"], 0, "Complement."),
 ("What does Bayes' rule give?", ["P(H | E) from P(E | H)", "The mean", "The variance", "A sum"], 0, "Reverses the conditional."),
 ("What is base-rate neglect?", ["Ignoring the prior", "Ignoring the test", "Counting twice", "Rounding errors"], 0, "Rare things stay rare."),
 ("What is E[X] for a fair die?", ["3.5", "3", "4", "6"], 0, "Average of one to six."),
 ("What does the central limit theorem say?", ["Averages become Gaussian", "Averages vanish", "Sums are uniform", "Variance is zero"], 0, "Many small effects."),
 ("What is the MLE of a coin's bias after k heads in n flips?", ["k/n", "n/k", "0.5", "k"], 0, "The likelihood peak."),
 ("What does MAP add to MLE?", ["A prior", "More data", "A p-value", "A mean"], 0, "Likelihood times prior."),
 ("What is the entropy of a fair coin?", ["1 bit", "0 bits", "2 bits", "0.5 bits"], 0, "Maximal for two outcomes."),
 ("Cross-entropy minus entropy equals what?", ["KL divergence", "Mutual information", "Variance", "Zero"], 0, "The extra bits."),
 ("What is the Markov property?", ["The future depends only on the present", "The past matters most", "Rewards are fixed", "States are random"], 0, "Memoryless."),
 ("What does a stationary distribution satisfy?", ["pi = pi P", "pi = 0", "P = I", "pi sums to 0"], 0, "Unchanged by a step."),
 ("What does a monoid need?", ["Associativity and an identity", "Inverses", "Commutativity", "Division"], 0, "A group adds inverses."),
 ("What must a functor preserve?", ["Identities and composition", "Sizes", "Names", "Order only"], 0, "F(g o f) = F(g) o F(f)."),
 ("What does a function type A -> B correspond to in logic?", ["A implies B", "A and B", "A or B", "Not A"], 0, "Curry-Howard."),
 ("What is beta reduction?", ["Substituting an argument into a function body", "Adding a type", "Sorting terms", "Looping"], 0, "How lambda terms compute."),
]

CFG = dict(id="mathematics-for-cs-ai", title="Mathematics for Computer Science and AI",
    subtitle="Discrete maths, linear algebra, calculus, probability, information theory, category and type theory, with Python labs",
    description="The mathematics behind modern computer science and machine learning, built from the ground up and explained intuitively: logic and proof, sets, counting, graphs, number theory, linear algebra, calculus and multivariate calculus, optimization, probability and statistics, information theory, Markov chains, abstract algebra and category theory, type theory and the lambda calculus. Every chapter has an explain-it-simply Feynman block, quizzes and Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="mfa", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "mathematics-for-cs-ai.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
