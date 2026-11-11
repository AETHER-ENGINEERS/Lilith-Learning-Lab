# -*- coding: utf-8 -*-
"""Statistics and probability, part 1."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Describing data: centre, spread and shape",
 ("Descriptive", [
  "Mean | is | The balance point",
  "Median | resists | Outliers",
  "Variance | measures | Spread",
  "Standard deviation | is | Root variance",
  "Quartiles | split | Ordered data",
  "Outlier | is | Far from the rest",
  "Histogram | shows | Shape"]),
 ["Statistics starts by summarising data. The mean and median describe the centre, the variance, standard deviation and interquartile range describe the spread, and a histogram shows the shape.",
  "The mean is pulled by outliers; the median is not. Use the sample standard deviation with n minus 1 in the denominator when estimating from a sample.",
  "Always plot the data before trusting a summary: very different datasets can share the same mean and variance."],
 [("Mean", "The sum of the values divided by their count."),
  ("Median", "The middle value of the sorted data, or the average of the two middle values."),
  ("Variance", "The average squared deviation from the mean; the sample version divides by n minus 1."),
  ("Standard deviation", "The square root of the variance, in the same units as the data."),
  ("Interquartile range", "The distance from the first to the third quartile, covering the middle half of the data.")],
 ["mean = sum / n.",
  "sample variance = sum (x - mean)^2 / (n - 1).",
  "IQR = Q3 - Q1.",
  "Outlier rule: beyond 1.5 IQR from the quartiles.",
  "Plot first."],
 [T("Imagine the wages of ten people in a cafe. Nine earn about the same; the owner earns fifty times more. The mean wage says everyone is rich; the median says what a typical worker earns. Different summaries answer different questions, and the first skill in statistics is choosing the right one."),
  T("The mean is the balance point of the data, the median is the middle, and the mode is the most common value. For a roughly symmetric dataset they agree; for a skewed one, such as incomes, the mean is pulled toward the long tail. For spread, the variance averages the squared distances from the mean, and the standard deviation takes the square root so it has the data's own units. When computed from a sample to estimate a population, divide by n minus 1 rather than n; this is Bessel's correction, because the sample mean sits closer to the sample points than the true mean would."),
  C("import statistics as st\ndata = [2, 4, 4, 4, 5, 5, 7, 9]\nprint(st.mean(data), st.median(data), st.mode(data))\nprint(st.pvariance(data), st.variance(data))   # divide by n, divide by n-1\nprint(st.stdev(data))", "python"),
  T("Quartiles cut the sorted data into four equal parts. The distance between the first and third, the interquartile range, is a spread measure that outliers hardly move. A common rule flags points more than one and a half interquartile ranges beyond the quartiles. Skewness and kurtosis describe the lopsidedness and tail weight of the shape."),
  T("Summaries hide things. Anscombe's quartet is four small datasets with the same mean, variance and correlation, yet one is a curve, one has an outlier and one is a vertical line. A histogram or scatter plot would reveal this in a second. Plot first, summarise second.")],
 [("Which summary resists outliers?", ["Median", "Mean", "Range", "Variance"], 0, "Middle value."),
  ("Why divide by n - 1 for a sample variance?", ["The sample mean is closer to the data than the true mean", "To make it larger for fun", "It is a tradition only", "To remove outliers"], 0, "Bessel."),
  ("What is the standard deviation?", ["The square root of the variance", "The mean of the squares", "The median spread", "The range"], 0, "Same units."),
  ("What does the IQR cover?", ["The middle half of the data", "The whole range", "The tails", "The mode"], 0, "Q3 - Q1."),
  ("What does Anscombe's quartet show?", ["Different data can share summaries", "Mean is always best", "Outliers do not matter", "Plots are unnecessary"], 0, "Plot first."),
  ("For right-skewed data, the mean is usually:", ["Above the median", "Below the median", "Equal to it", "Zero"], 0, "Pulled by the tail.")],
 [("statistics.mean, median, stdev", "Python summaries"), ("n - 1", "sample correction")],
 [MATCH("Match the term", "Pair each summary with its meaning.", [("Mean", "balance point"), ("Median", "middle value"), ("Variance", "average squared deviation"), ("IQR", "middle-half spread"), ("Mode", "most common value")]),
  PL("Mean and median", "Write centre(xs): [mean, median] rounded to 3 decimals.", "centre(xs)", '''
def centre(xs):
    s = sorted(xs)
    n = len(s)
    med = s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2.0
    return [round(sum(xs) / float(n), 3), round(med, 3)]
''', [[[2, 4, 4, 4, 5, 5, 7, 9]], [[1, 2, 3]], [[10, 1, 1, 1, 100]]], "Sort for the median.", approx=None),
  PL("Sample variance", "Write svar(xs): the sample variance (divide by n - 1) rounded to 4 decimals.", "svar(xs)", '''
def svar(xs):
    n = len(xs)
    m = sum(xs) / float(n)
    return round(sum([(x - m) ** 2 for x in xs]) / (n - 1), 4)
''', [[[2, 4, 4, 4, 5, 5, 7, 9]], [[1, 2, 3, 4]], [[5, 5, 5]]], "Bessel's correction.", approx=0.0005),
  PL("Quartiles", "Write quartiles(xs): [Q1, median, Q3] using the median of the lower half and upper half (excluding the middle element when n is odd); rounded to 3 decimals.", "quartiles(xs)", '''
def med(s):
    n = len(s)
    return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2.0
def quartiles(xs):
    s = sorted(xs)
    n = len(s)
    lower = s[:n // 2]
    upper = s[(n + 1) // 2:]
    return [round(med(lower), 3), round(med(s), 3), round(med(upper), 3)]
''', [[[1, 2, 3, 4, 5, 6, 7, 8]], [[1, 2, 3, 4, 5, 6, 7]], [[3, 7, 8, 5, 12, 14, 21, 13, 18]]], "Split the sorted list in halves.", approx=None),
  PL("Outliers by IQR", "Write outliers(xs): the sorted values below Q1 - 1.5 IQR or above Q3 + 1.5 IQR (quartiles as in the previous lab).", "outliers(xs)", '''
def med(s):
    n = len(s)
    return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2.0
def outliers(xs):
    s = sorted(xs)
    n = len(s)
    q1 = med(s[:n // 2])
    q3 = med(s[(n + 1) // 2:])
    iqr = q3 - q1
    return [x for x in s if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr]
''', [[[1, 2, 3, 4, 5, 100]], [[1, 2, 3]], [[-50, 10, 11, 12, 13, 14]]], "Fences."),
  PL("Z-scores", "Write zscores(xs): (x - mean) / sample standard deviation for each x, rounded to 3 decimals.", "zscores(xs)", '''
import math
def zscores(xs):
    n = len(xs)
    m = sum(xs) / float(n)
    s = math.sqrt(sum([(x - m) ** 2 for x in xs]) / (n - 1))
    return [round((x - m) / s, 3) for x in xs]
''', [[[1, 2, 3]], [[10, 20, 30, 40]], [[5, 7]]], "Standardise.", approx=None),
  PL("Histogram counts", "Write hist(xs, lo, hi, bins): counts of values in equal-width bins over [lo, hi); values equal to hi go in the last bin; values outside are ignored.", "hist(xs, lo, hi, bins)", '''
def hist(xs, lo, hi, bins):
    w = (hi - lo) / float(bins)
    c = [0] * bins
    for x in xs:
        if x < lo or x > hi:
            continue
        k = int((x - lo) / w)
        if k >= bins:
            k = bins - 1
        c[k] = c[k] + 1
    return c
''', [[[1, 2, 2, 3, 9, 10], 0, 10, 5], [[0, 5, 10], 0, 10, 2], [[-1, 11], 0, 10, 2]], "Bin the data."),
  PL("Weighted mean", "Write wmean(values, weights): the weighted mean rounded to 3 decimals.", "wmean(values, weights)", '''
def wmean(values, weights):
    return round(sum([v * w for v, w in zip(values, weights)]) / float(sum(weights)), 3)
''', [[[80, 90], [1, 3]], [[1, 2, 3], [1, 1, 1]], [[10], [5]]], "Grades with credit weights.", approx=0.002)]
))

CHS.append(CH(
 "Probability: events, rules and conditional probability",
 ("Probability", [
  "Sample space | lists | Outcomes",
  "Event | is | A set of outcomes",
  "Addition rule | handles | Or",
  "Multiplication rule | handles | And",
  "Conditional | restricts | The space",
  "Independence | means | No influence",
  "Bayes | reverses | Conditioning"]),
 ["Probability measures uncertainty on a scale from 0 to 1. It starts with a sample space of outcomes and events as subsets. The rules: probabilities of exclusive events add, the complement has 1 minus p, and P(A and B) = P(A) P(B | A).",
  "Conditional probability restricts attention to the cases where one event happened. Independent events do not change each other's probability. Bayes' theorem turns P(B | A) into P(A | B) and explains why a positive test for a rare disease is often a false alarm.",
  "Counting with permutations and combinations lets you find probabilities for equally likely outcomes."],
 [("Sample space", "The set of all possible outcomes of an experiment."),
  ("Event", "A subset of the sample space; it happens if the outcome is in it."),
  ("Conditional probability", "P(A | B) = P(A and B) / P(B): the chance of A given that B occurred."),
  ("Independence", "Events A and B are independent if P(A and B) = P(A) P(B)."),
  ("Bayes' theorem", "P(A | B) = P(B | A) P(A) / P(B).")],
 ["P(not A) = 1 - P(A).",
  "P(A or B) = P(A) + P(B) - P(A and B).",
  "P(A and B) = P(A) P(B | A).",
  "Bayes: posterior is likelihood times prior over evidence.",
  "C(n, k) = n! / (k! (n - k)!)."],
 [T("Roll a fair die. The sample space is the six faces. 'An even number' is the event {2, 4, 6}, with probability three sixths. If all outcomes are equally likely, probability is favourable outcomes over total outcomes, and probability becomes counting. Two basic rules follow: the probability that A does not happen is one minus the probability that it does, and for two events the chance of either is the sum minus the overlap, to avoid counting the overlap twice."),
  T("Conditioning means shrinking the world. The probability that a card is a king is four in fifty-two. Given that it is a face card, there are twelve candidates, so it is four in twelve. In symbols, P(A | B) = P(A and B) / P(B). Rearranged, P(A and B) = P(B) P(A | B), the multiplication rule. If knowing B does not change the chance of A, the events are independent and the rule simplifies to P(A) P(B). Beware: independent is not the same as exclusive. Exclusive events cannot both happen, so they are strongly dependent."),
  T("Bayes' theorem reverses a conditional. Suppose a disease affects 1 percent of people, a test catches 90 percent of cases and falsely flags 5 percent of healthy people. If you test positive, what is the chance you are ill? Out of 10,000 people, 100 are ill and 90 test positive; 9,900 are healthy and 495 test positive. Of 585 positives, only 90 are ill: about 15 percent. Rare conditions produce mostly false positives even with good tests. People who ignore the prior make this base-rate error constantly."),
  C("from math import comb, factorial\nprint(comb(5, 2))           # 10 ways to choose 2 of 5\nprint(factorial(4))         # 24 orderings\n# P(ill | positive)\nprior, sens, fpr = 0.01, 0.90, 0.05\npos = sens * prior + fpr * (1 - prior)\nprint(sens * prior / pos)   # about 0.154", "python"),
  T("Counting underlies many problems. The number of orderings of n distinct things is n factorial. Choosing k from n without regard to order is n choose k. Many puzzles such as the birthday problem, where 23 people give a better than even chance of a shared birthday, are easiest by computing the chance of no coincidence and subtracting from one.")],
 [("What is P(not A)?", ["1 - P(A)", "P(A)", "0", "2 P(A)"], 0, "Complement."),
  ("What is P(A | B)?", ["P(A and B) / P(B)", "P(A) P(B)", "P(B | A)", "1 - P(B)"], 0, "Restrict to B."),
  ("What does independence mean?", ["B does not change P(A)", "A and B cannot both happen", "A always follows B", "P(A) = 0"], 0, "No influence."),
  ("With a 1 percent base rate, why are positives mostly false alarms?", ["The healthy majority produces many false positives", "Tests are random", "Doctors err", "The prior is irrelevant"], 0, "Base rate."),
  ("How many ways to choose 2 from 5?", ["10", "20", "25", "5"], 0, "5 choose 2."),
  ("Are exclusive events independent?", ["No, they are strongly dependent", "Yes always", "Only for dice", "Only for cards"], 0, "If A happens B cannot.")],
 [("comb(n, k)", "choose"), ("P(A|B) = P(A,B)/P(B)", "conditional")],
 [MATCH("Match the rule", "Pair each rule with its formula.", [("Complement", "1 - P(A)"), ("Conditional", "P(A and B) / P(B)"), ("Independence", "P(A) P(B)"), ("Bayes", "likelihood times prior over evidence"), ("Combinations", "n! / (k! (n-k)!)")]),
  PL("Combinations", "Write choose(n, k): the number of ways to choose k items from n.", "choose(n, k)", '''
def choose(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r
''', [[5, 2], [10, 0], [6, 6], [4, 7], [20, 10]], "Multiply and divide step by step."),
  PL("Inclusion-exclusion", "Write p_or(pa, pb, pab): P(A or B), rounded to 4 decimals.", "p_or(pa, pb, pab)", '''
def p_or(pa, pb, pab):
    return round(pa + pb - pab, 4)
''', [[0.5, 0.3, 0.1], [0.2, 0.2, 0.0], [0.6, 0.6, 0.6]], "Do not count the overlap twice.", approx=0.0002),
  PL("Conditional probability", "Write cond(p_ab, p_b): P(A | B) rounded to 4 decimals.", "cond(p_ab, p_b)", '''
def cond(p_ab, p_b):
    return round(p_ab / p_b, 4)
''', [[0.1, 0.4], [0.25, 0.5], [0.0, 0.3]], "Restrict to B.", approx=0.0002),
  PL("Bayes' rule", "Write posterior(prior, sens, fpr): P(condition | positive test), rounded to 4 decimals.", "posterior(prior, sens, fpr)", '''
def posterior(prior, sens, fpr):
    pos = sens * prior + fpr * (1 - prior)
    return round(sens * prior / pos, 4)
''', [[0.01, 0.9, 0.05], [0.5, 0.9, 0.05], [0.001, 0.99, 0.01]], "Mind the base rate.", approx=0.0002),
  PL("Birthday problem", "Write birthday(n): the probability that among n people at least two share a birthday (365 days, equally likely), rounded to 4 decimals.", "birthday(n)", '''
def birthday(n):
    p = 1.0
    for i in range(n):
        p = p * (365 - i) / 365.0
    return round(1 - p, 4)
''', [[23], [10], [50], [1]], "Compute the chance of no match.", approx=0.0002),
  PL("Dice sums", "Write dice_sum_prob(target, n): the probability that the sum of n fair six-sided dice equals target, rounded to 4 decimals.", "dice_sum_prob(target, n)", '''
def dice_sum_prob(target, n):
    ways = {0: 1}
    for i in range(n):
        new = {}
        for s in ways:
            for f in range(1, 7):
                new[s + f] = new.get(s + f, 0) + ways[s]
        ways = new
    return round(ways.get(target, 0) / (6.0 ** n), 4)
''', [[7, 2], [12, 2], [3, 3], [20, 2]], "Count the ways.", approx=0.0002),
  PL("Total probability", "Write total_p(priors, likelihoods): sum of prior x likelihood over the cases, rounded to 4 decimals.", "total_p(priors, likelihoods)", '''
def total_p(priors, likelihoods):
    return round(sum([a * b for a, b in zip(priors, likelihoods)]), 4)
''', [[[0.5, 0.5], [0.2, 0.4]], [[0.3, 0.7], [1.0, 0.0]], [[1.0], [0.25]]], "The denominator in Bayes.", approx=0.0002)]
))

CHS.append(CH(
 "Random variables and distributions",
 ("Distributions", [
  "Random variable | assigns | A number",
  "PMF | gives | Discrete probabilities",
  "PDF | gives | Density",
  "CDF | accumulates | Probability",
  "Binomial | counts | Successes",
  "Poisson | counts | Rare events",
  "Normal | is | The bell curve"]),
 ["A random variable assigns a number to each outcome. Discrete ones have a probability mass function, continuous ones a density; the cumulative distribution function gives P(X at most x) for both.",
  "A few families do most of the work: Bernoulli and binomial for yes/no trials, geometric for waiting, Poisson for counts of rare events, uniform, exponential, and the normal distribution, whose bell curve is described by a mean and a standard deviation.",
  "For a normal variable, about 68, 95 and 99.7 percent of values lie within one, two and three standard deviations."],
 [("Random variable", "A function assigning a number to each outcome of a random experiment."),
  ("Probability mass function", "For a discrete variable, the probability of each value."),
  ("Density", "For a continuous variable, a curve whose area over an interval is the probability of that interval."),
  ("Binomial distribution", "The number of successes in n independent trials each with probability p."),
  ("Normal distribution", "The symmetric bell-shaped distribution determined by its mean and standard deviation.")],
 ["Binomial: C(n, k) p^k (1-p)^(n-k).",
  "Poisson: e^-lam lam^k / k!.",
  "Normal: z = (x - mu) / sigma.",
  "68-95-99.7 rule.",
  "CDF is non-decreasing from 0 to 1."],
 [T("A random variable turns outcomes into numbers: the sum of two dice, the number of heads in ten tosses, the waiting time for a bus. Its distribution lists how the probability is spread. For a discrete variable the probability mass function gives each value a probability that sums to one. For a continuous variable, where any exact value has probability zero, a density curve is used and probabilities are areas under it. The cumulative distribution function, the probability of being at or below x, works in both cases."),
  T("Some distributions appear again and again. A Bernoulli variable is a single yes or no with probability p. Add up n independent ones and you get a binomial: the number of heads in n tosses, or customers who click out of n visitors. When n is large and p small, the count of rare events such as typos per page or calls per minute follows a Poisson distribution with a single rate parameter. The waiting time between such events is exponential."),
  C("from math import comb, exp, factorial, erf, sqrt\ndef binom(k, n, p): return comb(n, k) * p**k * (1-p)**(n-k)\ndef poisson(k, lam): return exp(-lam) * lam**k / factorial(k)\ndef norm_cdf(x, mu=0, sd=1): return 0.5 * (1 + erf((x - mu) / (sd * sqrt(2))))\nprint(binom(3, 10, 0.5), poisson(2, 3), norm_cdf(1.96))", "python"),
  T("The normal distribution is the star. It is symmetric and bell-shaped, fixed by its mean mu and standard deviation sigma. Converting to a z-score, z = (x - mu) / sigma, puts any normal onto the standard scale, where tables and the 68-95-99.7 rule apply: about 68 percent of values fall within one sigma of the mean, 95 percent within two, and 99.7 percent within three. Heights, measurement errors and many sums of small effects are close to normal, as the next chapter explains."),
  T("Matching a distribution to a situation is a modelling choice. Counts of successes among n trials suggest a binomial; counts per time suggest a Poisson; measurements with symmetric noise suggest a normal; positive skewed quantities such as incomes suggest log-normal. Check the assumptions: independence, constant probability, and fixed n. Real data often have heavier tails than a normal curve predicts.")],
 [("What does a PMF give?", ["Probabilities of discrete values", "Areas of curves", "Means only", "Variances only"], 0, "Sums to one."),
  ("What is the probability of an exact value of a continuous variable?", ["Zero", "One", "One half", "The density"], 0, "Only intervals count."),
  ("Which distribution counts successes in n trials?", ["Binomial", "Normal", "Exponential", "Uniform"], 0, "Fixed n."),
  ("Which models counts of rare events per interval?", ["Poisson", "Binomial with n = 2", "Normal only", "Uniform"], 0, "Rate lambda."),
  ("What share of a normal lies within two sigma?", ["About 95 percent", "About 50 percent", "About 68 percent", "About 99.9 percent"], 0, "Empirical rule."),
  ("What does a z-score measure?", ["Standard deviations from the mean", "Probability", "Frequency", "Skew"], 0, "Standardise.")],
 [("scipy.stats.norm.cdf", "normal CDF"), ("scipy.stats.binom.pmf", "binomial PMF")],
 [MATCH("Match the distribution", "Pair each with its use.", [("Bernoulli", "one yes/no trial"), ("Binomial", "successes in n trials"), ("Poisson", "rare events per interval"), ("Exponential", "waiting time between events"), ("Normal", "symmetric bell curve")]),
  PL("Binomial PMF", "Write binom_pmf(k, n, p): C(n, k) p^k (1-p)^(n-k) rounded to 5 decimals.", "binom_pmf(k, n, p)", '''
def binom_pmf(k, n, p):
    c = 1
    for i in range(1, k + 1):
        c = c * (n - k + i) // i
    return round(c * p ** k * (1 - p) ** (n - k), 5)
''', [[3, 10, 0.5], [0, 5, 0.1], [5, 5, 0.9], [2, 4, 0.25]], "Count the ways times the probability.", approx=0.00005),
  PL("Poisson PMF", "Write poisson_pmf(k, lam): e^-lam lam^k / k! rounded to 5 decimals.", "poisson_pmf(k, lam)", '''
import math
def poisson_pmf(k, lam):
    f = 1
    for i in range(2, k + 1):
        f = f * i
    return round(math.exp(-lam) * lam ** k / f, 5)
''', [[2, 3], [0, 1], [5, 2.5], [1, 0.5]], "Rare events.", approx=0.00005),
  PL("Normal CDF", "Write norm_cdf(x, mu, sd): P(X <= x) for a normal variable, rounded to 4 decimals (use the error function).", "norm_cdf(x, mu, sd)", '''
import math
def norm_cdf(x, mu, sd):
    return round(0.5 * (1 + math.erf((x - mu) / (sd * math.sqrt(2)))), 4)
''', [[1.96, 0, 1], [100, 100, 15], [130, 100, 15], [-1, 0, 1]], "Standardise first.", approx=0.0002),
  PL("Binomial CDF", "Write binom_cdf(k, n, p): P(X <= k) rounded to 5 decimals.", "binom_cdf(k, n, p)", '''
def binom_cdf(k, n, p):
    t = 0.0
    for j in range(0, k + 1):
        c = 1
        for i in range(1, j + 1):
            c = c * (n - j + i) // i
        t = t + c * p ** j * (1 - p) ** (n - j)
    return round(t, 5)
''', [[3, 10, 0.5], [0, 3, 0.2], [10, 10, 0.5]], "Add the PMF.", approx=0.00005),
  PL("Expected value", "Write expect(values, probs): the expected value rounded to 4 decimals.", "expect(values, probs)", '''
def expect(values, probs):
    return round(sum([v * p for v, p in zip(values, probs)]), 4)
''', [[[1, 2, 3], [0.2, 0.5, 0.3]], [[0, 10], [0.9, 0.1]], [[5], [1.0]]], "Probability-weighted average.", approx=0.0002),
  PL("Variance of a distribution", "Write dist_var(values, probs): the variance sum p (x - mean)^2 rounded to 4 decimals.", "dist_var(values, probs)", '''
def dist_var(values, probs):
    m = sum([v * p for v, p in zip(values, probs)])
    return round(sum([p * (v - m) ** 2 for v, p in zip(values, probs)]), 4)
''', [[[1, 2, 3], [0.2, 0.5, 0.3]], [[0, 1], [0.5, 0.5]], [[4], [1.0]]], "Spread of the distribution.", approx=0.0002),
  PL("Empirical rule", "Write within_k_sigma(k): the probability that a standard normal lies within k standard deviations of the mean, rounded to 4 decimals.", "within_k_sigma(k)", '''
import math
def within_k_sigma(k):
    return round(math.erf(k / math.sqrt(2)), 4)
''', [[1], [2], [3], [1.96]], "68-95-99.7.", approx=0.0002)]
))

CHS.append(CH(
 "Expectation, the law of large numbers and the central limit theorem",
 ("Limit theorems", [
  "Expectation | is | The long-run average",
  "Variance | adds | For independent",
  "Law of large numbers | says | Averages converge",
  "Central limit theorem | says | Means look normal",
  "Standard error | shrinks | With root n",
  "Sampling distribution | describes | A statistic",
  "Simulation | checks | Theory"]),
 ["Expectation is the long-run average, and it is linear: the expected value of a sum is the sum of expected values. Variances add for independent variables.",
  "The law of large numbers says sample means approach the true mean as the sample grows. The central limit theorem says that, for almost any starting distribution, the mean of many independent draws is approximately normal with standard deviation sigma over root n.",
  "That standard error shrinks slowly: to halve the uncertainty you need four times the data. These results are why the normal distribution dominates statistics."],
 [("Expectation", "The probability-weighted average of the possible values of a random variable."),
  ("Law of large numbers", "The sample mean converges to the true mean as the sample size grows."),
  ("Central limit theorem", "The distribution of the sample mean approaches a normal as the sample size grows, whatever the underlying distribution (with finite variance)."),
  ("Standard error", "The standard deviation of a statistic, for the mean sigma divided by the square root of n."),
  ("Sampling distribution", "The distribution of a statistic over repeated samples.")],
 ["E[X + Y] = E[X] + E[Y].",
  "Var(X + Y) = Var X + Var Y if independent.",
  "SE of mean = sigma / sqrt(n).",
  "CLT: mean is about N(mu, sigma^2 / n).",
  "Four times the data, half the error."],
 [T("Toss a coin ten times and you may see seven heads. Toss it ten thousand times and the fraction of heads settles near one half. This is the law of large numbers: averages of independent trials converge to the expectation. It is why casinos win and why polls work, but it says nothing about streaks balancing out; the coin has no memory."),
  T("Expectation behaves nicely. The expected value of a sum is always the sum of expectations, even if the variables depend on each other. A fair die has expectation 3.5, so ten dice sum to 35 on average. Variance is less forgiving: variances add only for independent variables. A consequence: the mean of n independent draws has variance sigma squared over n, so its standard deviation, the standard error, is sigma over the square root of n."),
  T("The central limit theorem is the deeper surprise. Take any distribution with finite variance, skewed or lumpy, and average n independent draws. As n grows, the distribution of that average becomes bell-shaped: normal with mean mu and standard deviation sigma over root n. That is why so many measured quantities, which are sums of many small effects, look normal, and why the tools of the next chapters work. Try it in the playground: draw from a skewed distribution and watch the histogram of means turn into a bell."),
  C("import random, statistics as st\nrandom.seed(1)\nmeans = [st.mean(random.expovariate(1.0) for _ in range(30)) for _ in range(2000)]\nprint(st.mean(means), st.stdev(means))   # about 1 and 1/sqrt(30) = 0.18", "python"),
  T("Mind the limits. Convergence is slow: the error shrinks like one over root n, so each extra digit of accuracy costs a hundred times more data. Heavy-tailed distributions, such as the Cauchy distribution, have no mean at all, and averages never settle. Dependent data, like consecutive days of weather, reduce the effective sample size. Simulation is a strong sanity check: when in doubt, generate data from the model and watch.")],
 [("What does the law of large numbers say?", ["Sample means approach the true mean", "Streaks always correct", "Variance vanishes", "Data become normal"], 0, "Convergence."),
  ("What is E[X + Y]?", ["E[X] + E[Y]", "E[X] E[Y]", "0", "Var X"], 0, "Linear."),
  ("What is the standard error of a mean?", ["sigma / sqrt(n)", "sigma x n", "sigma squared", "n / sigma"], 0, "Root n."),
  ("What does the CLT say?", ["Means become approximately normal", "All data are normal", "Medians equal means", "Variance is constant"], 0, "Bell curve of means."),
  ("To halve the standard error you need:", ["Four times the data", "Twice the data", "Half the data", "Ten times the data"], 0, "Root n."),
  ("When does the mean fail to settle?", ["Heavy tails such as the Cauchy", "Large samples", "Normal data", "Uniform data"], 0, "No finite mean.")],
 [("random.expovariate", "skewed draws"), ("mean of means", "sampling distribution")],
 [APP("CLT", "Central limit theorem lab", "Choose a skewed source distribution and a sample size, then draw many sample means and watch their histogram become a bell. Try three different sample sizes to complete the lab.", 800),
  MATCH("Match the term", "Pair each result with its meaning.", [("Law of large numbers", "averages converge"), ("CLT", "means look normal"), ("Standard error", "sigma over root n"), ("Linearity", "E of a sum is the sum of E"), ("Sampling distribution", "distribution of a statistic")]),
  PL("Standard error", "Write se(sigma, n): sigma divided by the square root of n, rounded to 4 decimals.", "se(sigma, n)", '''
import math
def se(sigma, n):
    return round(sigma / math.sqrt(n), 4)
''', [[10, 25], [1, 100], [3, 1], [2, 16]], "Root n.", approx=0.0002),
  PL("Sample size for precision", "Write needed_n(sigma, target_se): the smallest integer n such that sigma / sqrt(n) is at most target_se.", "needed_n(sigma, target_se)", '''
import math
def needed_n(sigma, target_se):
    n = int(math.ceil((sigma / float(target_se)) ** 2 - 1e-9))
    return max(n, 1)
''', [[10, 1], [15, 3], [1, 0.1], [2, 2]], "Square the ratio."),
  PL("Running mean", "Write running_mean(xs): the list of means of the first 1, 2, ..., n values, rounded to 3 decimals.", "running_mean(xs)", '''
def running_mean(xs):
    out = []
    t = 0.0
    for i, x in enumerate(xs):
        t = t + x
        out.append(round(t / (i + 1), 3))
    return out
''', [[[1, 3, 5, 7]], [[10]], [[2, 2, 2]]], "Watch convergence.", approx=None),
  PL("Variance of a sum", "Write var_sum(vars_, covs): variance of a sum of independent variables is the sum of variances; if covs is nonempty, add twice each listed covariance. Rounded to 3 decimals.", "var_sum(vars_, covs)", '''
def var_sum(vars_, covs):
    return round(sum(vars_) + 2 * sum(covs), 3)
''', [[[1, 2, 3], []], [[4, 4], [1.5]], [[1], []]], "Independence means zero covariance.", approx=0.002),
  PL("Simulate means", "Write sim_means(n_samples, n, seed): using the linear congruential generator x = (x * 1103515245 + 12345) mod 2^31, starting at seed, produce n_samples sample means, each the average of n uniform values x / 2^31; return the list of means rounded to 3 decimals.", "sim_means(n_samples, n, seed)", '''
def sim_means(n_samples, n, seed):
    x = seed
    out = []
    for i in range(n_samples):
        t = 0.0
        for j in range(n):
            x = (x * 1103515245 + 12345) % 2147483648
            t = t + x / 2147483648.0
        out.append(round(t / n, 3))
    return out
''', [[3, 4, 1], [2, 10, 7], [1, 1, 5]], "A deterministic generator keeps results reproducible.", approx=None),
  PL("Chebyshev bound", "Write chebyshev(k): the maximum fraction of any distribution that can lie k or more standard deviations from the mean, 1 / k^2 (capped at 1), rounded to 4 decimals.", "chebyshev(k)", '''
def chebyshev(k):
    return round(min(1.0, 1.0 / (k * k)), 4)
''', [[2], [3], [0.5], [1]], "A distribution-free guarantee.", approx=0.0002)]
))
