"""AIXI course, chapters 5-8."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

TOY_OUT = """
def toy_output(program, length):
    n = 0
    while n < len(program) and program[n] == '1':
        n += 1
    if n == 0 or n >= len(program) or program[n] != '0':
        return ''
    pattern = program[n + 1:]
    if len(pattern) != n:
        return ''
    out = ''
    for i in range(length):
        out += pattern[i % n]
    return out
"""

# ------------------------------------------------------------ 5
CHS.append(CH(
 "Kolmogorov complexity and the universal prior",
 ("Complexity", [
  "Kolmogorov complexity | is | Length of shortest program",
  "Universal Turing machine | runs | Programs",
  "Invariance theorem | bounds | Change of machine",
  "Kolmogorov complexity | is | Incomputable",
  "Prefix-free code | satisfies | Kraft inequality",
  "Universal prior | weights | 2 to minus length",
  "Occam | is formalized by | Short programs"]),
 ["The Kolmogorov complexity of a string is the length of the shortest program that prints it on a fixed universal computer. A string with a pattern has a short program. A random string has no program much shorter than itself.",
  "Changing the computer changes the complexity by at most a constant, so the notion is meaningful. But no program can compute it exactly.",
  "The universal prior gives a string the total weight of all programs that produce it, each program counting two to the power of minus its length. This is Occam's razor written as arithmetic."],
 [("Kolmogorov complexity", "K(x): the length of the shortest program that outputs x on a given universal machine."),
  ("Universal Turing machine", "A machine that can simulate any other machine given its description as part of the program."),
  ("Invariance theorem", "For two universal machines, complexities differ by at most a constant not depending on x."),
  ("Prefix-free", "No program is the beginning of another program."),
  ("Kraft inequality", "For a prefix-free set of programs, the sum of 2^-length is at most 1."),
  ("Universal prior", "Probability of a string = sum of 2^-length over programs that produce it."),
  ("Incomputable", "No algorithm computes K(x) for every x.")],
 ["K(x) is the length of the shortest program printing x.",
  "The reference machine matters only up to an additive constant (invariance theorem).",
  "K is not computable.",
  "Prefix-free programs obey the Kraft inequality, so 2^-length can be read as probabilities.",
  "M(x) is the sum of 2^-length(p) over programs whose output starts with x.",
  "Shorter explanations get exponentially more weight."],
 [T("Compare two strings of a thousand bits. The first is zero, one, zero, one, and so on. The second is the result of a thousand fair coin flips. The first can be described by a very short program: print zero one, five hundred times. The second seems to need a program that contains the bits themselves. Kolmogorov complexity makes this precise."),
  T("Fix a universal computer U. The Kolmogorov complexity of a string x, written K of x, is the length in bits of the shortest program that makes U print x. Solomonoff, Kolmogorov and Chaitin each arrived at this idea independently in the 1960s. A string is regular when K of x is much smaller than its length."),
  T("Which computer? The invariance theorem says it hardly matters for long strings. If V is another universal computer, then K under U and K under V differ by at most a constant c that depends on U and V but not on the string, because U can simulate V given a fixed-length interpreter. Chapter 12 returns to this: the constant is harmless in theory, yet for the short histories an agent sees in practice it can matter a lot."),
  T("Kolmogorov complexity cannot be computed. If a program could compute K, we could use it to search for the first string whose complexity exceeds some large number n, but that search would itself be a short program, only about log n bits long, which is a contradiction. We can compute upper bounds, by finding some program, and never prove that a bound is tight in general."),
  T("Now turn lengths into probabilities. Take programs to be bit strings from a prefix-free set: no program is the beginning of another. A fair coin that produces bits one at a time and stops when a complete program has appeared gives program p probability two to the power of minus its length. The Kraft inequality guarantees that these probabilities add up to at most one."),
  M(r"M(x) \;=\; \sum_{p:\ U(p)\ \text{starts with}\ x} 2^{-\ell(p)}"),
  T("This is Solomonoff's universal prior, in the monotone form used for prediction. The probability of a string x is the chance that U, fed with random bits, prints something that begins with x. Strings with short programs get large probability. A string with complexity K gets probability roughly two to the minus K, up to terms of lower order, so a string with a program ten bits shorter is a thousand times more likely."),
  T("The practice section uses a toy machine, my own illustration. A program is n ones, then a zero, then a pattern of exactly n bits; the machine repeats the pattern forever. The program length is two n plus one. You can run it, compute the shortest program for a string, check that the set is prefix-free and compute the prior over a finite set of programs.")],
 [("What is K(x)?", ["The length of the shortest program printing x", "The number of ones in x", "The runtime of x", "The probability of x"], 0, "Kolmogorov complexity."),
  ("Is K computable?", ["Yes", "No", "Only for short strings", "Only on GPUs"], 1, "No algorithm computes it for all x."),
  ("What does the invariance theorem say?", ["The choice of universal machine changes K by at most a constant", "K never changes", "K is always small", "All strings have equal K"], 0, "A fixed-length interpreter suffices."),
  ("How is a program of length l weighted in the universal prior?", ["2 to the power minus l", "l", "l squared", "1/l"], 0, "Shorter programs weigh exponentially more.")],
 [("What is a prefix-free set?", "No program starts another."), ("What does Kraft say?", "Sum of 2^-length is at most 1."), ("Why is K incomputable?", "A search for complex strings would itself be a short program."),
  ("What does a regular string have?", "A program much shorter than itself.")],
 [PL("Run the toy machine", "A program is n ones, a zero, then exactly n pattern bits (n at least 1); the output is the pattern repeated forever. Write toy_output(program, length): the first length output bits as a string, or the empty string '' if the program is not valid.",
     "toy_output(program, length)", TOY_OUT, [["1010", 6], ["110101", 5], ["1110111", 7], ["10", 3], ["0101", 3], ["11010", 4], ["100", 4]], "Count the leading ones to get n, then check that exactly n bits follow the zero."),
  PL("Shortest program", "Using the same toy machine (program length 2n+1), write toy_K(x): the length of the shortest valid program whose output begins with the non-empty bit string x. Try every n from 1 up to len(x) and every pattern of n bits.",
     "toy_K(x)", """
def toy_K(x):
    def out(program, length):
        n = 0
        while n < len(program) and program[n] == '1':
            n += 1
        if n == 0 or n >= len(program) or program[n] != '0':
            return ''
        pattern = program[n + 1:]
        if len(pattern) != n:
            return ''
        s = ''
        for i in range(length):
            s += pattern[i % n]
        return s
    for n in range(1, len(x) + 1):
        for k in range(2 ** n):
            pat = ''
            for j in range(n):
                if (k >> (n - 1 - j)) & 1:
                    pat += '1'
                else:
                    pat += '0'
            prog = '1' * n + '0' + pat
            if out(prog, len(x)) == x:
                return len(prog)
    return -1
""", [["0"], ["01010101"], ["0000000"], ["011011011"], ["0110"], ["1101001"], ["101"]], "Lengths grow with n, so the first match found when going up in n is the shortest."),
  PL("Is it prefix-free?", "Write prefix_free(codes): True if no code word in the list of bit strings is the beginning of a different code word (a duplicate also counts as a violation).",
     "prefix_free(codes)", """
def prefix_free(codes):
    for i in range(len(codes)):
        for j in range(len(codes)):
            if i != j and codes[j].startswith(codes[i]):
                return False
    return True
""", [[["0", "10", "110", "111"]], [["0", "01"]], [["10", "11", "0"]], [["1", "1"]], [["00", "01", "10", "11"]], [["", "1"]]], "Compare every ordered pair of different positions."),
  PL("Kraft sum and the prior", "Write toy_prior(x, nmax): return [kraft, M] where kraft is that sum for ALL toy programs with n from 1 to nmax (length 2n+1, 2^n patterns each) and M is the sum of 2^-length over those programs whose output begins with the bit string x. Use the toy machine. The function is toy_prior(x, nmax).",
     "toy_prior(x, nmax)", """
def toy_prior(x, nmax):
    kraft = 0.0
    m = 0.0
    for n in range(1, nmax + 1):
        for k in range(2 ** n):
            pat = ''
            for j in range(n):
                if (k >> (n - 1 - j)) & 1:
                    pat += '1'
                else:
                    pat += '0'
            w = 2.0 ** (-(2 * n + 1))
            kraft += w
            s = ''
            for i in range(len(x)):
                s += pat[i % n]
            if s == x:
                m += w
    return [kraft, m]
""", [["0", 3], ["01", 4], ["0101", 4], ["000", 5], ["1", 1], ["0110", 5]], "Build every pattern from the bits of k, weigh by 2 to the minus (2n+1), and compare the repeated pattern with x."),
  ORDER("Why K is incomputable", "Order the steps of the standard argument.", ["Suppose a program computes K", "Write a program that searches for the first string with K above n", "That program is only about log n bits long", "So the string it finds has K at most about log n", "This contradicts K being above n"]),
  MATCH("Ideas", "Match each idea with its statement.", [("Invariance theorem", "Machine choice costs a constant"), ("Kraft inequality", "Sum of 2^-length at most 1"), ("Prefix-free", "No code word begins another"), ("Universal prior", "Sums 2^-length over programs"), ("Regular string", "Short description")]),
  FILL("Complexity", "Kolmogorov complexity is the {{length}} of the shortest program. It is {{incomputable|not computable}}. Programs are weighted by two to the minus their {{length}}.")]))

# ------------------------------------------------------------ 6
CHS.append(CH(
 "Solomonoff induction",
 ("Universal prediction", [
  "Solomonoff prior | is | A mixture of all computable measures",
  "Prediction | is | Ratio of prior probabilities",
  "M | dominates | Every computable measure",
  "Dominance constant | is | 2 to minus K of mu",
  "Total error | is | Bounded by complexity",
  "Prediction error | tends to | Zero on computable data",
  "Solomonoff induction | is | Incomputable"]),
 ["Solomonoff induction predicts the next symbol by the ratio M of x followed by a symbol, to M of x. It is the Bayesian mixture of chapter 4 over every computable hypothesis, with weights from the universal prior.",
  "Its signature result is a bound on total error. If the data comes from any computable source mu, the predictions converge to mu's own, and the total prediction error, however long the sequence, is bounded by a constant proportional to K of mu.",
  "The result is strong and rare: one predictor that works for every computable world. The price is that M itself is incomputable."],
 [("Solomonoff prior M", "The universal prior over sequences, a mixture of all lower semicomputable semimeasures."),
  ("Semimeasure", "A probability-like function whose probabilities may add to less than one."),
  ("Prediction", "M(x a) divided by M(x) for the next symbol a."),
  ("Dominance", "M(x) is at least 2^-K(mu) times mu(x) for every computable mu, up to a constant."),
  ("Convergence", "On data from computable mu, M's predictions approach mu's."),
  ("Lower semicomputable", "Approximable from below, but without a known error bound.")],
 ["Prediction is a ratio: M(x a) / M(x).",
  "M is a mixture over all computable environments with weights 2^-K.",
  "Dominance: M(x) >= c 2^-K(mu) mu(x).",
  "Hence total prediction error on mu-data is bounded by a multiple of K(mu).",
  "For a deterministic computable sequence the number of wrong predictions is bounded by a multiple of K.",
  "M is only lower semicomputable, so Solomonoff induction cannot be run exactly."],
 [T("Prediction in the Solomonoff style is a single formula. Having seen a string x, the probability that the next symbol is a equals M of x followed by a, divided by M of x. Programs that disagree with x have already dropped out of both sums, and programs that survive vote for the next symbol with weight two to the minus their length."),
  M(r"M(a \mid x) \;=\; \dfrac{M(x\,a)}{M(x)}"),
  T("Why does this work? Chapter 4 showed that a mixture is at least as large as each member times its weight. Here the members are all the computable probability models, and the weight of model mu is about two to the minus K of mu, the complexity of its shortest description. So M of x is at least about two to the minus K of mu times mu of x. A model with a short description is poorly handicapped."),
  T("From dominance comes the guarantee. If the data is really drawn from a computable mu, then the total expected squared difference between M's predictions and mu's, summed over the whole infinite sequence, is bounded by a constant multiple of K of mu. Hutter's analyses and the textbook of Li and Vitanyi state it. A sum that stays bounded forces the terms to shrink, so the predictions converge to the truth."),
  T("For a deterministic computable sequence the picture is even starker. The number of wrong predictions made by the predictor is bounded by a multiple of K of the sequence, as the introduction of Leike and Hutter's paper recalls. A sequence with a ten-bit description costs the predictor a handful of mistakes, and after that it predicts that sequence correctly forever."),
  T("A good way to see the mechanism is halving. Keep all deterministic hypotheses consistent with the data so far, each with its weight. Predict with the weighted majority vote. Whenever you are wrong, the wrong side held at least half of the surviving weight and is eliminated, so the surviving weight at least halves. The true hypothesis never goes, and its weight is at least two to the minus e. So at most e mistakes can happen."),
  T("The catch is again computability. M is lower semicomputable: it can be approximated from below by running more programs for more steps, but there is never a point at which we know how close we are. Many programs never halt, and deciding which do is the halting problem. So Solomonoff induction is a limit, not an algorithm."),
  T("The practice section computes the toy prior's prediction, and simulates the weighted-majority argument with a bound on mistakes.")],
 [("How is the next-symbol probability computed?", ["M(xa) / M(x)", "M(x) times M(a)", "The longest program", "Random"], 0, "A ratio of prior probabilities."),
  ("What is the dominance weight of mu?", ["About 2^-K(mu)", "K(mu)", "1/2", "0"], 0, "Simpler models weigh more."),
  ("What does the total prediction error bound depend on?", ["The complexity of the true source", "The sequence length", "The random seed", "Nothing"], 0, "It is a multiple of K(mu)."),
  ("Why can't we run Solomonoff induction exactly?", ["M is only lower semicomputable", "It needs too many GPUs", "It is not Bayesian", "It forgets"], 0, "Halting is undecidable.")],
 [("Predict how?", "Ratio M(xa)/M(x)."), ("What happens on computable data?", "Predictions converge; total error is bounded."), ("What is halving?", "Eliminating at least half of the weight at every mistake."),
  ("Who first formalized it?", "Ray Solomonoff in 1964.")],
 [PL("Predict with the toy prior", "Using the toy machine (n ones, a zero, n pattern bits; the pattern repeats; program weight 2^-(2n+1); programs up to n = nmax), write toy_predict(x, nmax): the probability that the next bit is 1 after the non-empty string x, as M(x1) / M(x) with M summed over those programs.",
     "toy_predict(x, nmax)", """
def toy_predict(x, nmax):
    def M(s):
        m = 0.0
        for n in range(1, nmax + 1):
            for k in range(2 ** n):
                pat = ''
                for j in range(n):
                    if (k >> (n - 1 - j)) & 1:
                        pat += '1'
                    else:
                        pat += '0'
                t = ''
                for i in range(len(s)):
                    t += pat[i % n]
                if t == s:
                    m += 2.0 ** (-(2 * n + 1))
        return m
    return M(x + '1') / M(x)
""", [["0101", 6], ["0000", 6], ["01", 5], ["011011", 6], ["1", 4], ["0010", 6]], "Compute M for x plus a one and for x, then divide.", approx=1e-9),
  PL("Weighted majority", "Hypotheses are repeating bit patterns (strings; the sequence is the pattern repeated). weights[i] is an integer e_i meaning prior weight 2^-e_i (the weights sum to at most 1). The true sequence is hypotheses[truth] repeated, for steps bits. At each step predict by weighted majority among hypotheses consistent with all bits so far (if the weights are tied, predict 1). Write halving(hypotheses, exps, truth, steps) returning [number of mistakes, exps[truth]].",
     "halving(hypotheses, exps, truth, steps)", """
def halving(hypotheses, exps, truth, steps):
    alive = list(range(len(hypotheses)))
    mistakes = 0
    for t in range(steps):
        bit = {}
        w0 = 0.0
        w1 = 0.0
        for i in alive:
            h = hypotheses[i]
            b = h[t % len(h)]
            w = 2.0 ** (-exps[i])
            if b == '1':
                w1 += w
            else:
                w0 += w
        pred = '1'
        if w0 > w1:
            pred = '0'
        h = hypotheses[truth]
        actual = h[t % len(h)]
        if pred != actual:
            mistakes += 1
        keep = []
        for i in alive:
            g = hypotheses[i]
            if g[t % len(g)] == actual:
                keep.append(i)
        alive = keep
    return [mistakes, exps[truth]]
""", [[["0", "1", "01", "011"], [1, 2, 3, 4], 3, 12], [["0", "1", "01", "011"], [1, 2, 3, 4], 0, 6], [["01", "001", "0001", "00001"], [2, 2, 3, 3], 3, 15], [["1", "0", "10"], [1, 2, 3], 2, 8], [["110", "10", "1"], [1, 2, 3], 0, 9]], "Track which hypotheses are still consistent; vote with 2.0 ** (-e) weights."),
  ORDER("Halving argument", "Order the steps.", ["Keep all hypotheses consistent with the data", "Predict by weighted majority", "If wrong, the losing side held at least half of the weight", "Eliminate every hypothesis that disagreed", "The surviving weight at least halves per mistake"]),
  MATCH("Facts", "Match each fact with its source.", [("Universal prior and induction", "Solomonoff, 1964"), ("Mixture dominance", "Bayesian sum is at least each term"), ("Error bound", "A multiple of K of the true source"), ("Lower semicomputable", "Can be approximated from below"), ("Halving", "Mistakes at most log of 1 over weight")]),
  FILL("Prediction", "Solomonoff prediction is the {{ratio}} M(xa)/M(x). On computable data the total error is bounded by a multiple of the {{complexity|Kolmogorov complexity}} of the source. M is only {{lower semicomputable|lower-semicomputable}}.")]))

# ------------------------------------------------------------ 7
CHS.append(CH(
 "The AIXI equation",
 ("AIXI", [
  "AIXI | uses | Universal prior over environments",
  "AIXI | plans by | Expectimax",
  "Program q | simulates | An environment",
  "Weight | is | 2 to minus program length",
  "Consistency | filters | Programs by history",
  "Reward sum | scores | Futures",
  "Action | is | Argmax of expected reward"]),
 ["The AIXI equation puts the pieces together. A program q stands for an environment: given the agent's actions, it outputs the percepts. Each q consistent with the history so far is weighted by two to the minus its length. The agent takes the action with the highest weighted expected total reward.",
  "Written in full, a maximum over the next action alternates with sums over the next percept, all the way to the horizon, with the reward sum multiplying a weighted count of the consistent programs.",
  "On a small finite class of environments the same computation is easy to carry out. The practice section builds it and the app lets you watch it work."],
 [("AIXI equation", "The rule a_k = argmax over actions of an alternating max-sum expression over future percepts, weighted by 2^-length of consistent programs."),
  ("Program q", "A program for the universal machine standing for a candidate environment."),
  ("Consistent", "Producing exactly the percepts seen so far when given the actions taken."),
  ("Horizon m", "The last step counted in the reward sum."),
  ("Lifetime", "The total number of steps the agent will act, here m."),
  ("Reference machine", "The universal Turing machine U used to read programs.")],
 ["a_k = argmax_{a_k} sum_{o_k r_k} ... max_{a_m} sum_{o_m r_m} [r_k + ... + r_m] sum_{q: U(q, a_1..a_m) = o_1 r_1 .. o_m r_m} 2^-length(q).",
  "The inner sum is the Solomonoff-style weight of all environments producing that future.",
  "The only parameters are the reference machine U and the horizon m.",
  "In a finite class: weight each consistent environment, expand the tree, take the best action.",
  "Deterministic consistent environments are eliminated as soon as their reply differs from the percept seen.",
  "Computing the real thing needs all programs, including those that never halt."],
 [T("Here is the definition, in words first. At step k the agent has taken actions a one to a k minus one and received percepts o one r one up to o k minus one r k minus one. It must choose a k. For each candidate action it looks at each possible next percept, then each next action, and so on until the horizon m. At the end of each branch it counts the total reward. The weight of a branch is the total two to the minus length of the programs that would produce exactly that history."),
  M(r"a_k \;=\; \arg\max_{a_k} \sum_{o_k r_k} \;\cdots\; \max_{a_m} \sum_{o_m r_m} \bigl[\, r_k + \cdots + r_m \,\bigr] \sum_{q:\; U(q,\,a_1\dots a_m) = o_1 r_1 \dots o_m r_m} 2^{-\ell(q)}"),
  T("This is the equation printed in Veness and colleagues' paper as equation one, and it matches the formulation in Hutter's survey. Read it from the left. The maximum chooses the action. The sum over percepts averages over what the environment might say. The pairs repeat to the horizon. The innermost sum is the Solomonoff weight of the future: the total weight of programs q that, given the actions, would print this entire history of percepts."),
  T("Notice what is missing. There are no hidden states and no probabilities supplied by the designer. The programs q do the job of both: a program may be a deterministic simulator, or it may use its own coin flips through the universal machine's randomness. Short programs dominate, so simple worlds are believed first and complicated ones only when the evidence demands."),
  T("To make this concrete, take a finite list of deterministic candidate environments, each with a length playing the role of program length. Weight each by two to the minus its length. After each percept, drop those that would have replied differently. The remaining weights give the probability of each possible next reward, and the expectimax recursion of chapter 3 does the rest. That is exactly AIXI, restricted to a tiny class."),
  T("This restriction is not cheating about the idea but it is cheating about the difficulty. The real class is infinite and contains programs that do not halt. A faithful implementation would need to know, for each program, whether it ever produces the next percept. That is why the real thing is incomputable, and why chapter 10 and 11 turn to approximations."),
  T("In the app you see the filtered class, the posterior weights and the action chosen, step by step, in a small world. In the practice section you write the same pieces as functions.")],
 [("What does the innermost sum in the AIXI equation count?", ["The weight of programs producing the history", "The reward", "The actions", "The horizon"], 0, "Sum of 2^-length over consistent programs."),
  ("What are the free parameters of AIXI?", ["The universal machine and the horizon", "Learning rate and depth", "Batch size", "None at all"], 0, "Plus the discount if used."),
  ("What happens to a deterministic hypothesis whose reply differs from the percept seen?", ["It is eliminated", "It gains weight", "It is duplicated", "Nothing"], 0, "It is inconsistent with the history."),
  ("Why is the full equation incomputable?", ["It requires knowing which programs halt", "It needs a GPU", "The horizon is infinite", "It uses randomness"], 0, "Halting problem.")],
 [("What is q?", "A program standing for an environment."), ("What is the weight of q?", "2 to the minus its length."), ("What does max choose?", "The agent's action."), ("What does sum over percepts do?", "Averages over environment replies.")],
 [PL("Which environments are consistent?", "An environment is [kind, param, length]. Rewards for a binary-action game: 'const' pays 1 iff the action equals param; 'alt' pays 1 iff the action differs from the previous action (the previous action before step 1 is 0); 'never' pays 0; 'parity' pays 1 iff the action equals (t mod 2) at step t (t counts from 1). The history is a list of [action, reward] pairs. Write consistent(envs, history): the list of indices of environments that would have given exactly those rewards.",
     "consistent(envs, history)", """
def consistent(envs, history):
    def reward(env, acts):
        kind = env[0]
        a = acts[-1]
        if kind == 'const':
            if a == env[1]:
                return 1
            return 0
        if kind == 'alt':
            prev = 0
            if len(acts) > 1:
                prev = acts[-2]
            if a != prev:
                return 1
            return 0
        if kind == 'parity':
            if a == len(acts) % 2:
                return 1
            return 0
        return 0
    good = []
    for i in range(len(envs)):
        acts = []
        ok = True
        for a, r in history:
            acts.append(a)
            if reward(envs[i], acts) != r:
                ok = False
                break
        if ok:
            good.append(i)
    return good
""", [[[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], []], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[0, 1]]], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[1, 1], [1, 0]]], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[1, 1], [0, 1], [1, 1]]], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[1, 0]]]], "Replay the actions; compare each computed reward with the one in the history."),
  PL("Posterior weights", "With the same environments, write posterior(envs, history): for each environment the weight 2^-length if it is consistent with the history, else 0, divided by the total (normalized so they sum to 1). If none is consistent return all zeros.",
     "posterior(envs, history)", """
def posterior(envs, history):
    def reward(env, acts):
        kind = env[0]
        a = acts[-1]
        if kind == 'const':
            if a == env[1]:
                return 1
            return 0
        if kind == 'alt':
            prev = 0
            if len(acts) > 1:
                prev = acts[-2]
            if a != prev:
                return 1
            return 0
        if kind == 'parity':
            if a == len(acts) % 2:
                return 1
            return 0
        return 0
    raw = []
    for env in envs:
        acts = []
        ok = True
        for a, r in history:
            acts.append(a)
            if reward(env, acts) != r:
                ok = False
                break
        if ok:
            raw.append(2.0 ** (-env[2]))
        else:
            raw.append(0.0)
    total = sum(raw)
    if total == 0:
        return raw
    return [x / total for x in raw]
""", [[[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], []], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[1, 1]]], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[0, 0], [1, 1]]], [[["const", 0, 3], ["const", 1, 3]], [[0, 1], [1, 1]]], [[["const", 0, 3], ["alt", 0, 5], ["parity", 0, 6]], [[1, 1], [0, 1], [1, 1]]]], "Weight 2.0 ** (-length) for consistent environments, then divide by the total.", approx=1e-9),
  PL("Choose the action", "Write aixi_action(envs, history, horizon): the AIXI action for this small class. Use the environments of the previous lab (deterministic, rewards as defined). Weight each consistent environment by 2^-length. The percept is just the reward. Do expectimax over the next horizon steps: for each action group the consistent environments by the reward they would give, weight each group by its share of the total weight, and recurse with the smaller group. Return [expected total reward, best first action]; break ties by the smaller action.",
     "aixi_action(envs, history, horizon)", """
def aixi_action(envs, history, horizon):
    def reward(env, acts):
        kind = env[0]
        a = acts[-1]
        if kind == 'const':
            if a == env[1]:
                return 1
            return 0
        if kind == 'alt':
            prev = 0
            if len(acts) > 1:
                prev = acts[-2]
            if a != prev:
                return 1
            return 0
        if kind == 'parity':
            if a == len(acts) % 2:
                return 1
            return 0
        return 0
    start = []
    acts0 = []
    for i in range(len(envs)):
        acts = []
        ok = True
        for a, r in history:
            acts.append(a)
            if reward(envs[i], acts) != r:
                ok = False
                break
        if ok:
            start.append(i)
    base = [a for a, r in history]
    def best(idx, acts, k):
        if k == 0 or len(idx) == 0:
            return [0.0, 0]
        total = 0.0
        for i in idx:
            total += 2.0 ** (-envs[i][2])
        top = -1.0
        arg = 0
        for a in range(2):
            na = acts + [a]
            g = [[], []]
            for i in idx:
                g[reward(envs[i], na)].append(i)
            v = 0.0
            for r in range(2):
                if len(g[r]) > 0:
                    w = 0.0
                    for i in g[r]:
                        w += 2.0 ** (-envs[i][2])
                    v += w / total * (r + best(g[r], na, k - 1)[0])
            if v > top + 1e-12:
                top = v
                arg = a
        return [top, arg]
    return best(start, base, horizon)
""", [[[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [], 1], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [], 3], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[0, 0]], 3], [[["const", 0, 3], ["const", 1, 3], ["alt", 0, 5], ["parity", 0, 6], ["never", 0, 2]], [[1, 1]], 3], [[["const", 0, 4], ["alt", 0, 3]], [[1, 1]], 4], [[["const", 0, 3], ["alt", 0, 5], ["parity", 0, 6]], [[1, 1], [0, 1]], 3]], "Recurse on (consistent group, actions so far, steps left); the group for each reward gets its share of the weight.", approx=1e-9),
  {"type": "webxdc", "title": "AIXI explorer", "intro": "Choose a hidden world and let AIXI act. Watch worlds drop out as the history contradicts them, and see how the shortest surviving world dominates. Run at least six steps.", "height": 640, "html": "__AIXI__"},
  ORDER("AIXI step", "Order the steps of one AIXI decision.", ["List the programs consistent with the history", "Weight each by 2 to the minus its length", "Expand the future for each action and percept", "Average the reward sums by weight", "Take the action with the highest average"]),
  MATCH("Parts", "Match each part with its role.", [("Max", "Chooses the action"), ("Sum over percepts", "Averages over the environment"), ("2^-length(q)", "Occam weight"), ("Consistency", "Removes contradicted programs"), ("Horizon m", "Last step counted")]),
  FILL("Equation", "AIXI weights each consistent program by two to the minus its {{length}}. It maximizes the expected {{reward}} sum up to the {{horizon}}.")]))

# ------------------------------------------------------------ 8
CHS.append(CH(
 "Horizons and discounting",
 ("Time", [
  "Finite horizon | counts | m steps",
  "Geometric discount | has | Fixed effective horizon",
  "Harmonic discount | has | Growing horizon",
  "Infinite horizon | needs | Summable rewards",
  "Immortal agent | is | Lazy",
  "Discount | affects | Exploration",
  "Horizon | trades | Foresight against cost"]),
 ["The AIXI equation sums reward up to a horizon m. How far ahead should the agent look? Too short and it is greedy. Too long and the sums may not converge, or, in a patient universe, the agent may keep postponing.",
  "Discounting replaces a hard cutoff with weights on the steps. Geometric discounting makes the near future matter much more than the far future. Hutter's survey also discusses harmonic discounting, whose horizon grows as the agent ages.",
  "None of these choices is neutral: the discount shapes how much the agent explores, and chapter 12 shows prior and discount can interact badly."],
 [("Horizon", "How many future steps count."),
  ("Geometric discount", "Step k is weighted by gamma^k with gamma below one."),
  ("Effective horizon", "The number of steps after which the remaining weight is negligible."),
  ("Harmonic discount", "Weights proportional to 1/(k(k+1)); the effective horizon grows with age."),
  ("Summability", "The total of all weights must be finite for an infinite sum of rewards to make sense."),
  ("Lazy agent", "An agent so patient that postponing a reward never costs it anything.")],
 ["A finite lifetime m is simplest but the agent must know m.",
  "Geometric discounting: effective horizon about log(1/eps) / log(1/gamma).",
  "Harmonic discounting: tail after step t is about 1/t, so the horizon grows linearly with age.",
  "With no discounting and an infinite life, delaying rewards forever can look optimal.",
  "Hutter notes immortal agents are lazy.",
  "The choice of discount is part of the problem specification, not a detail."],
 [T("Everything so far had a fixed number of steps m. That makes the agent finite-minded: at the last step it simply takes the best immediate reward, whatever it did to the world. If the agent's lifetime is unknown or unbounded, we need a different idea."),
  T("The cleanest is discounting. Give step k the weight gamma k, with gamma a number between zero and one. The total weight is finite, so the sum of rewards converges even for an infinite life. The effective horizon is the point after which the remaining weight is tiny. With gamma equal to a half, ten steps already capture over 99.9 percent of the weight. With gamma near one, the agent looks very far ahead."),
  M(r"\sum_{k \ge m} \gamma^{k} \;=\; \frac{\gamma^{m}}{1-\gamma}"),
  T("Hutter's survey also describes universal and harmonic discounting. In harmonic discounting step k gets weight one over k times k plus one, so the total is one and the remaining weight after step t is exactly one over t. Then an agent of age t that wants to look far enough ahead to capture all but a fraction of the remaining weight needs a horizon that grows in proportion to its age, something geometric discounting cannot do."),
  T("Why not drop discounting and just sum all rewards of an infinite life? Then the sums can diverge, and even when they converge, as the survey notes in its discussion of horizons, immortal agents become lazy: if all time is available, any pleasant outcome can always be postponed with no penalty. A discount or a finite horizon is what makes the agent act now."),
  T("Legg and Hutter solved the problem differently in their intelligence measure, chapter 9: they require that total reward in every environment is bounded by one. That makes discounting unnecessary but restricts the environments considered."),
  T("The choice also decides how much the agent explores. A short effective horizon values immediate reward and discourages experiments that pay off late. A long one tolerates experiments. Since AIXI's belief about the world starts almost empty, exploration matters, and the next chapters show that the prior and the discount together decide whether AIXI explores enough."),
  T("The practice section computes tails of geometric sums, effective horizons and the discounted value of a reward stream, plus the growing harmonic horizon.")],
 [("What does a geometric discount do?", ["Weights step k by gamma^k", "Removes rewards", "Adds noise", "Doubles rewards"], 0, "Near steps count more."),
  ("How does the harmonic horizon behave?", ["It grows with age", "It is constant", "It shrinks", "It is zero"], 0, "The tail is 1/t."),
  ("What is a problem with an infinite undiscounted life?", ["Sums may diverge and the agent may be lazy", "Rewards are negative", "The agent runs out of memory", "Nothing"], 0, "Delay costs nothing."),
  ("What did Legg and Hutter use instead of discounting?", ["Bounded total reward", "A larger horizon", "Random rewards", "No rewards"], 0, "Total reward at most 1 in each environment.")],
 [("What is the effective horizon?", "Steps until the remaining weight is negligible."), ("What does gamma near 1 mean?", "A far-sighted agent."), ("Why is an immortal agent lazy?", "Postponing costs nothing."),
  ("What does discounting do to exploration?", "Shorter horizons discourage experiments.")],
 [PL("Effective horizon", "With geometric discount gamma, the weight after step m is gamma^m / (1 - gamma) (steps counted from 0, so the weights are gamma^0, gamma^1, ...). Write effective_horizon(gamma, eps): the smallest integer m at which this tail is at most eps.",
     "effective_horizon(gamma, eps)", """
def effective_horizon(gamma, eps):
    m = 0
    while gamma ** m / (1 - gamma) > eps:
        m += 1
    return m
""", [[0.5, 0.001], [0.9, 0.01], [0.99, 0.1], [0.5, 1.0], [0.75, 0.0001]], "Increase m until the tail drops to eps or below."),
  PL("Discounted return", "Write discounted_return(rewards, gamma): the sum of gamma^k times rewards[k] for k from 0.",
     "discounted_return(rewards, gamma)", """
def discounted_return(rewards, gamma):
    total = 0.0
    for k in range(len(rewards)):
        total += rewards[k] * gamma ** k
    return total
""", [[[1, 1, 1], 0.5], [[0, 0, 5], 0.9], [[1, 0, 1, 0, 1], 1.0], [[], 0.5], [[2, 1], 0.1]], "Accumulate in a loop.", approx=1e-9),
  PL("Harmonic horizon", "Under harmonic discounting the tail after step t is proportional to 1/t. An agent at age t wants a horizon h so that the weight beyond t + h is at most 1/q of the weight beyond t, i.e. t / (t + h) is at most 1/q. Write harmonic_horizon(t, q): the smallest non-negative integer h with t * q <= t + h.",
     "harmonic_horizon(t, q)", """
def harmonic_horizon(t, q):
    h = 0
    while t * q > t + h:
        h += 1
    return h
""", [[1, 10], [5, 4], [100, 2], [10, 1], [7, 3]], "Search upward from zero (or solve h = t * (q - 1))."),
  ORDER("Lazy agent", "Order the argument.", ["No discount and an infinite lifetime", "Any reward can be postponed without penalty", "Postponing always looks at least as good", "The agent never collects", "A discount or finite horizon restores action"]),
  MATCH("Horizons", "Match each scheme with its property.", [("Finite horizon m", "Agent must know its lifetime"), ("Geometric discount", "Fixed effective horizon"), ("Harmonic discount", "Horizon grows with age"), ("Bounded total reward", "Used by Legg and Hutter"), ("No discount, infinite life", "Immortal agents are lazy")]),
  FILL("Horizons", "A {{geometric}} discount gives a fixed effective horizon. A {{harmonic}} discount makes the horizon grow with age. Without discounting, immortal agents are {{lazy}}.")]))
