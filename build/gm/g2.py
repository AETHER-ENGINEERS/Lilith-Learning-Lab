"""Gödel Machine course, chapters 7-12."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 7
CHS.append(CH(
 "Global optimality",
 ("Why the rewrite is globally optimal", [
  "Target theorem | compares | Switch versus continue search",
  "Continue branch | includes | Later better rewrites",
  "Theorem 4.1 | states | Rewrite is globally optimal",
  "Greedy rewrite | is not | Required",
  "Relaxed target theorem | still gives | Global optimality",
  "Meta-levels | collapse into | One level"]),
 ["Theorem 4.1 in the paper says that once the machine has proved a target theorem and switched, the resulting change is globally optimal: no other self-rewrite, now or later, could have done better, given the axioms. The reason is that the continue option already includes every future rewrite the searcher might find.",
  "So the machine is not greedy. It does not take the first improvement; it takes a switch only when the proof says that switching now beats everything it could do by waiting. The paper also argues that all meta-levels collapse into one, because the same proof searcher improves itself.",
  "The guarantee is relative to the axioms and requires them to be consistent. It is not a guarantee about the real world beyond what the axioms say."],
 [("Globally optimal", "No other rewrite, available now or later, would have a higher expected utility, according to the axioms."),
  ("Greedy", "Taking the first improvement found, without comparing with future improvements."),
  ("Meta-level", "A level of learning that improves a lower level, such as a learner that improves the learner."),
  ("Relaxed version", "Rewrite when the change is provably not worse; optimality holds in the weaker sense.")],
 ["The continue branch of the target theorem contains all later rewrites.",
  "Therefore a proved target theorem means switching now is at least as good as any alternative.",
  "The machine is not greedy: it can leave a worse-looking but later-better path alone.",
  "All meta-levels collapse into one level.",
  "Guarantees hold only if the axioms are consistent.",
  "A bogus utility change cannot be proved better under the present utility."],
 [T("Chapter 6 ended with a subtle point: the target theorem compares switching with continuing, and continuing includes the possibility that the proof searcher finds something even better later. This chapter spells out what follows from it."),
  T("Theorem 4.1 in the paper reads, in plain words: given the initial axiom system, once the machine has executed a rewrite after proving a target theorem, no other rewrite, whether at that moment or at any later moment, can have higher expected utility. The proof is short. At the time of the switch the machine has proved that u with the switch is greater than u without it. The without-it branch contains every future rewrite. So no future rewrite beats this switch."),
  T("That makes the machine non-greedy. A greedy learner takes any improvement it can find. The Gödel machine may instead decline an improvement now, because it can prove that waiting for a better one pays off more, for example a rewrite that makes the proof searcher itself faster. The comparison is not with the present policy; it is with the best future."),
  T("Take a small example with numbers. Policy A earns 10 per step. Candidate B earns 12 per step but costs 30 steps to apply. Candidate C earns 20 per step but costs 40 steps to apply, and it is provable only later. With 100 steps left, B gives 12 times 70, which is 840, against 1000 for staying, so B is not worth it. A greedy rule that only checks rate would jump to B and lose."),
  M(r"u_{\text{switch}} \;=\; r_{\text{new}}\,(T - t_1 - c) \qquad u_{\text{stay}} \;=\; r_{\text{old}}\,(T - t_1)"),
  T("The paper also discusses the relaxed target theorem, with at-least-as-high in place of strictly higher, and shows that global optimality still holds in the sense that no later rewrite can be strictly better. The strict version avoids pointless rewrites with equal utility."),
  T("The collapse of meta-levels. In many learning systems you stack levels: a learner, a meta-learner that tunes the learner, a meta-meta-learner, and so on, each fixed by the designer. Here the proof searcher can rewrite the entire software, including itself, so there is a single level. Improvements to improvement happen inside the same loop and are judged by the same target theorem."),
  T("The paper answers common worries in a short question and answer section. What if a later self-change breaks the machine? Any change was proved to raise utility before it was executed, so a later change is judged the same way. What if the machine adopts a bogus utility? A new utility is acceptable only if the present utility says it is better, so a reward-hacking replacement would fail the test."),
  T("Be careful about what is claimed. These are mathematical results inside a formal framework, and they inherit its assumptions: a consistent axiom system, a correct hardware model, and enough resources to find proofs. Whether a real machine could ever satisfy them is open, as chapter 11 discusses."),
  T("In the practice section you compute the total reward of a plan with several switches, and find the best single switch, which shows why comparing with the stay option matters.")],
 [("What does the continue branch of the target theorem contain?", ["Nothing", "Every later rewrite the searcher might find", "Only the current policy", "The hardware"], 1, "That is why the choice is globally optimal."),
  ("Is the Gödel machine greedy?", ["Yes, it takes the first improvement", "No, it can decline an improvement because waiting is provably better", "Only at the start", "Only for rewards"], 1, "It compares with the best future."),
  ("What does 'all meta-levels collapse' mean?", ["Memory is freed", "One proof searcher improves everything, including itself", "There are no levels", "The machine halts"], 1, "A single level suffices."),
  ("What do the optimality guarantees assume?", ["The axioms are consistent", "The environment is deterministic", "Infinite time", "A human supervises"], 0, "Inconsistent axioms prove anything.")],
 [("What is Theorem 4.1?", "A proved-and-executed rewrite is globally optimal."), ("Why not greedy?", "Waiting for a better rewrite can be provably better."), ("Relaxed version?", "At least as high utility."),
  ("Bogus utility?", "Needs a proof that it is better under the present utility.")],
 [PL("Total reward with switches", "The machine earns rate0 per step for horizon steps. A switch is [time, new_rate, cost]: at that time it spends cost steps earning nothing, then continues at new_rate. Write total_reward(rate0, horizon, switches) for switches sorted by time. Steps are numbered from 0 to horizon-1. Ignore any switch whose time is at or after the horizon, and cut off a switch cost that runs past the end.",
     "total_reward(rate0, horizon, switches)", """
def total_reward(rate0, horizon, switches):
    t = 0
    rate = rate0
    total = 0
    for sw in switches:
        when = sw[0]
        if when >= horizon:
            break
        total += (when - t) * rate
        t = when
        t = min(horizon, t + sw[2])
        rate = sw[1]
    total += (horizon - t) * rate
    return total
""", [[10, 100, []], [10, 100, [[0, 12, 5]]], [10, 100, [[0, 12, 30]]], [10, 100, [[20, 15, 10], [60, 20, 5]]], [10, 50, [[60, 99, 1]]], [10, 50, [[45, 99, 20]]]], "Accumulate reward up to each switch, jump over the cost steps, then change the rate."),
  PL("Best single switch", "Candidates are [time, new_rate, cost] as before. Write best_switch(rate0, horizon, candidates): the index of the candidate whose single switch gives the highest total reward, but only if it is strictly better than not switching; otherwise return -1. For ties, choose the first. Use the same reward rules as before.",
     "best_switch(rate0, horizon, candidates)", """
def best_switch(rate0, horizon, candidates):
    def total(sw):
        when = sw[0]
        if when >= horizon:
            return rate0 * horizon
        t = min(horizon, when + sw[2])
        return when * rate0 + (horizon - t) * sw[1]
    best = rate0 * horizon
    idx = -1
    for i in range(len(candidates)):
        v = total(candidates[i])
        if v > best:
            best = v
            idx = i
    return idx
""", [[10, 100, [[0, 12, 30], [0, 20, 40]]], [10, 100, [[0, 12, 5], [0, 11, 0]]], [10, 100, [[0, 10, 0]]], [10, 100, []], [10, 100, [[50, 30, 10], [0, 15, 20]]]], "Compute each candidate's total and keep the first strict maximum above the stay total."),
  MATCH("Optimality", "Match each idea with its role.", [("Continue branch", "Includes every future rewrite"), ("Strict target theorem", "Avoids pointless equal rewrites"), ("Collapsed meta-levels", "One searcher improves everything"), ("Consistent axioms", "Needed for the guarantee")]),
  FILL("Optimality", "A proved rewrite is {{globally}} optimal. The machine is not {{greedy}}. All meta-levels {{collapse}} into one.")]))

# ------------------------------------------------------------ 8
CHS.append(CH(
 "Bias-optimal proof search (BIOPS)",
 ("Universal search for proofs", [
  "Universal search | allots | Time in proportion to probability",
  "Phase i | gives | Budget 2^i times P(w)",
  "BIOPS | is | Bias-optimal proof search",
  "BIOPS | finds | Proof of target theorem",
  "Bias-optimal | means | Optimal given the bias",
  "OOPS | reuses | Earlier solutions"]),
 ["Bias-optimal proof search, or BIOPS, is the paper's search scheme for the proof searcher. It tests proof techniques in phases: in phase i, each technique w with probability P(w) of at least 2 to the minus i receives a budget of 2 to the i times P(w) steps.",
  "Theorem 5.1 says that if a proof technique exists that proves the target theorem in time t, BIOPS finds it in time of order t divided by P(w), up to a constant factor. Bias-optimal means optimal given the bias, which is the probability distribution P over techniques.",
  "BIOPS is an online search. When a technique fails, the effects on the scratch memory are undone, and the next one runs. A successful technique may be reused: the Optimal Ordered Problem Solver shares this idea."],
 [("Universal search", "Levin's scheme for searching programs in order, giving each a time share proportional to its prior probability."),
  ("P(w)", "The probability of technique w, often 2 to the minus its code length."),
  ("Phase", "One round of the search; phase i doubles the total time of the previous phase."),
  ("Bias", "The prior distribution over techniques, which says which are tried first."),
  ("Bias-optimal", "Within a constant factor of the best possible, given the bias."),
  ("BIOPS", "Bias-optimal proof search, Schmidhuber's scheme for the Gödel machine's searcher."),
  ("OOPS", "Optimal Ordered Problem Solver, a related method that reuses earlier solutions.")],
 ["BIOPS runs in phases i = 1, 2, 3, ...",
  "In phase i a technique w with P(w) >= 2^-i gets 2^i * P(w) steps.",
  "Total time per phase is at most 2^i.",
  "If a technique proves the theorem in t steps, BIOPS finds it in O(t / P(w)).",
  "It is optimal only given the bias P.",
  "The O() hides a constant factor, which may be large."],
 [T("The proof searcher needs a schedule for trying proof techniques. Chapter 5 said the simplest way, enumerating all proofs by size, is exponential. Universal search, invented by Leonid Levin, does better: it tries programs in a way that spends time in proportion to their probability."),
  T("Say each proof technique w has a probability P of w. A natural choice is 2 to the minus the length of its code, so shorter techniques are more likely. The schedule works in phases. In phase i, every technique with P of w at least 2 to the minus i is run for 2 to the i times P of w steps."),
  M(r"\text{phase } i:\quad P(w) \ge 2^{-i} \;\Rightarrow\; \text{budget}(w) = 2^{i}\,P(w)"),
  T("Consider the total time. In phase i the budgets add up to at most 2 to the i times the sum of the probabilities, which is at most 2 to the i. Each phase costs at most twice the previous one, so the search time is dominated by the last phase."),
  T("Now the guarantee. Suppose technique w proves the target theorem in t steps. It first gets a large enough budget in the phase where 2 to the i times P of w is at least t. That phase i satisfies 2 to the i of order t divided by P of w. All phases up to i together take at most about twice that. So BIOPS finds the proof in time of order t over P of w. This is Theorem 5.1."),
  T("This is what bias-optimal means. BIOPS is not faster than a perfect searcher, but it is within a constant factor of the best searcher that uses the same bias. It cannot avoid the constant, which is large when the winning technique is improbable, that is, long."),
  T("The paper also defines n-bias-optimal variants, in which the search is allowed to be a factor n slower in exchange for other properties, and notes that a proof technique's effects are undone before the next one starts, so each test is independent."),
  T("Relation to OOPS. The Optimal Ordered Problem Solver, also by Schmidhuber, applies the same time allocation to a sequence of tasks and lets later tasks reuse the code that solved earlier ones. The paper suggests the Gödel machine's searcher can profit from this by keeping useful proof fragments."),
  T("In the practice section you implement a small Levin-style search. Each technique has a code length k, so P is 2 to the minus k, and a step count needed to succeed or minus one if it never succeeds.")],
 [("In BIOPS phase i, what budget does technique w get?", ["P(w)", "2^i * P(w)", "i", "1"], 1, "Higher phases give more time."),
  ("What does Theorem 5.1 promise?", ["Constant-time proofs", "The proof is found within O(t / P(w)) steps", "No proof is needed", "Only short proofs"], 1, "Up to a constant factor given the bias."),
  ("What does 'bias-optimal' mean?", ["Optimal for any distribution", "Optimal up to a constant given the prior over techniques", "Biased toward errors", "Optimal for random inputs"], 1, "The prior is the bias."),
  ("What is a drawback of universal search?", ["It is unsound", "The constant factor can be huge", "It cannot find proofs", "It needs a human"], 1, "Improbable (long) techniques are costly.")],
 [("Who invented universal search?", "Leonid Levin."), ("What is P(w) typically?", "2 to the minus code length."), ("Cost per phase?", "At most 2^i."),
  ("What does OOPS add?", "Reuse of earlier solutions across tasks.")],
 [PL("A Levin-style search", "Each technique is [name, k, steps] with probability P = 2^-k, where steps is how many steps it needs to prove the target, or -1 if it never will. In phase i = 1, 2, 3, ... every technique with k <= i runs with a budget of 2^(i-k) steps (the integer 2^i * P). Each run, successful or not, uses its whole budget unless it finishes earlier, and costs its steps used. Write levin_search(techs): return [phase, name, total_steps], where phase is the first phase in which some technique finishes (its steps <= its budget), name is the first such technique in list order, and total_steps adds the steps used by all runs up to and including that run (each earlier run uses its full budget, the finishing run uses its real steps). If nothing finishes in 40 phases, return [0, \"none\", total_steps] with the steps used in those 40 phases.",
     "levin_search(techs)", """
def levin_search(techs):
    total = 0
    for i in range(1, 41):
        for t in techs:
            name = t[0]
            k = t[1]
            steps = t[2]
            if k > i:
                continue
            budget = 2 ** (i - k)
            if steps != -1 and steps <= budget:
                total += steps
                return [i, name, total]
            total += budget
    return [0, 'none', total]
""", [[[["a", 1, 8], ["b", 2, 3]]], [[["a", 3, 2], ["b", 1, -1]]], [[["a", 2, -1]]], [[["x", 1, 1]]], [[["a", 1, 3], ["b", 1, 3]]]], "Loop over phases, then techniques. Skip a technique if k > i, compute 2 ** (i - k), finish if steps fits."),
  MATCH("BIOPS terms", "Match each term with its meaning.", [("P(w)", "Prior probability of a technique"), ("Phase", "One round of the doubling schedule"), ("Bias", "The prior that sets try-order"), ("OOPS", "Reuses solutions across tasks"), ("O(t / P(w))", "Time to find a proof taking t steps")]),
  FILL("Search", "In phase i a technique gets a budget of {{2^i * P(w)|2^i P(w)}}. BIOPS is optimal only up to a {{constant}} factor, given its {{bias|prior}}.")]))

# ------------------------------------------------------------ 9
CHS.append(CH(
 "Examples and kinds of self-improvement",
 ("What can a Gödel machine improve?", [
  "Gödel machine | improves | Policy and searcher",
  "Self-improvement | includes | Speed-ups",
  "Proof of speed-up | needs | Axioms about hardware",
  "Example | is | Goldbach counterexample search",
  "Example | is | Fuel robot with Speed Prior",
  "Example | is | Graph or TSP solver"]),
 ["The paper lists several kinds of self-improvement the machine could prove useful, from small speed-ups of a subroutine to replacing the utility function or the axioms themselves. Each kind needs a proof inside the axiom system.",
  "Three illustrative scenarios appear in the paper: a program that speeds up a graph or travelling-salesman solver, a search for a counterexample to Goldbach's conjecture, and a robot with limited fuel that must plan around depots under a weak environment assumption, the Speed Prior.",
  "These are thought experiments, not experimental results. They show how a target theorem could be stated and what must be proved."],
 [("Speed-up", "A rewrite that makes a subroutine faster, so that more reward or more search fits in the remaining time."),
  ("Goldbach's conjecture", "Every even integer greater than 2 is the sum of two primes; unproven."),
  ("Counterexample search", "A program that checks even numbers one by one and stops if it finds one that is not a sum of two primes."),
  ("Speed Prior", "A prior that favours environments computable quickly; it gives a weak, plausible environment assumption."),
  ("Depot", "A place where the robot can refuel."),
  ("Travelling salesman problem", "Find the shortest tour through a set of cities.")],
 ["The paper lists eight kinds of self-improvement.",
  "A Gödel machine may improve its policy, its searcher, its axioms and even its utility function, always with a proof.",
  "Speed-ups are the most direct example: a faster subroutine raises expected reward.",
  "The Goldbach example shows search under a time limit.",
  "The robot example shows planning under uncertainty about the environment.",
  "No example has been demonstrated experimentally."],
 [T("What can a Gödel machine improve? In section 6.1 the paper lists several kinds of self-improvement, all of them proved useful by the target theorem. They include: changing the initial policy; speeding up a subroutine, which gives more reward or more search per step; changing the proof searcher or its search order; adding axioms or lemmas that shorten future proofs; modifying the hardware model after the real hardware changes; and, in principle, changing the utility function or the axioms themselves."),
  T("A key point is that a speed-up of the proof searcher is a self-improvement like any other. A faster searcher finds later proofs sooner, and this can be proved worthwhile even without knowing the exact utility, as chapter 6 noted. This is how the machine's efficiency can compound."),
  T("Example one: a graph or travelling-salesman solver. Suppose the policy is a slow heuristic. A rewrite replaces it with a faster algorithm. The machine proves from the hardware axioms that the new code runs in fewer steps and returns the same answer, and from the utility axioms that finishing earlier gives more reward. That proves the target theorem."),
  T("Example two: Goldbach's conjecture. Suppose the machine's task is to find a counterexample. The policy checks even numbers in turn. If a counterexample exists, the reward comes when it is found, so a faster check is useful. If none exists the policy runs forever and the reward never arrives, so the machine should not spend unlimited resources on it. The paper uses this to show how time budgeting matters."),
  T("Here is the check itself. For an even number n, look for a prime p up to n over 2 such that n minus p is also prime. If you find one, n is fine. If you reach no such p, n is a counterexample. The practice section implements this for small numbers. No counterexample is known to exist; it has been checked far beyond what the lab will do."),
  T("Example three: a fuel robot. A robot uses one liter of fuel per hour and must keep running to earn reward. The environment contains fuel depots at certain times, but the robot does not know the true environment. The paper uses the Speed Prior as a weak assumption: the environment is computable, and fast-computable environments are more likely. The machine can then prove statements about expected survival under that prior."),
  T("The point of all three: a self-improvement is justified by a proof about future reward, and the proof depends on the axioms. The more precise the axioms, the more improvements the machine can justify. The weaker the axioms, the fewer."),
  T("In the practice section you search for Goldbach pairs, scan for a counterexample below a limit, and compute how long a robot survives.")],
 [("What justifies a self-improvement in a Gödel machine?", ["A user vote", "A proof of higher expected utility", "A random test", "A deadline"], 1, "Every rewrite needs a proof."),
  ("What is a speed-up of the proof searcher?", ["A forbidden change", "A self-improvement like any other", "A hardware fault", "A new reward"], 1, "It may compound the machine's efficiency."),
  ("What is the Speed Prior used for in the fuel robot example?", ["To count fuel", "As a weak assumption about the environment", "To choose depots", "To encrypt data"], 1, "Fast-computable environments get more weight."),
  ("What does the Goldbach example illustrate?", ["That the conjecture is true", "Time budgeting for a search that might never finish", "Prime factorization", "Proof checking"], 1, "No counterexample is known.")],
 [("Goldbach's conjecture?", "Every even number above 2 is a sum of two primes."), ("Is it proved?", "No."), ("What does the robot burn?", "One liter of fuel per hour in the example."),
  ("Are these results?", "No, they are thought experiments.")],
 [MATCH("Kinds of improvement", "Match each change with its effect.", [("Faster subroutine", "More reward per unit time"), ("Faster proof searcher", "Later proofs are found sooner"), ("New lemma axiom", "Shorter future proofs"), ("Better hardware model", "Axioms match real hardware")]),
  PL("Goldbach pair", "Write goldbach_pair(n) for an even n at least 4: return [p, n-p] with p the smallest prime such that n-p is also prime, or [] if none exists.",
     "goldbach_pair(n)", """
def goldbach_pair(n):
    def is_prime(k):
        if k < 2:
            return False
        d = 2
        while d * d <= k:
            if k % d == 0:
                return False
            d += 1
        return True
    p = 2
    while p <= n // 2:
        if is_prime(p) and is_prime(n - p):
            return [p, n - p]
        p += 1
    return []
""", [[4], [10], [28], [100], [98]], "Try p from 2 upward; test both p and n - p with a primality helper."),
  PL("First counterexample", "Write first_counterexample(limit): scan even numbers 4, 6, 8, ... up to limit (inclusive) and return the first one with no Goldbach pair, or -1 if there is none. (Expect -1.)",
     "first_counterexample(limit)", """
def first_counterexample(limit):
    def is_prime(k):
        if k < 2:
            return False
        d = 2
        while d * d <= k:
            if k % d == 0:
                return False
            d += 1
        return True
    n = 4
    while n <= limit:
        found = False
        p = 2
        while p <= n // 2:
            if is_prime(p) and is_prime(n - p):
                found = True
                break
            p += 1
        if not found:
            return n
        n += 2
    return -1
""", [[10], [200], [3], [4]], "For each even n look for a pair; return n if you find none."),
  PL("Fuel robot", "A robot starts with initial liters and burns 1 liter per hour. Depots are [time, liters]: at that hour it picks up fuel if it is still running (fuel is above 0 just before the hour). Write robot_lifetime(initial, depots): the hour at which it runs out, counting hours from 0. Depots are sorted by time. If fuel is 0 at the start, return 0.",
     "robot_lifetime(initial, depots)", """
def robot_lifetime(initial, depots):
    fuel = initial
    t = 0
    for d in depots:
        when = d[0]
        if fuel <= 0:
            return t
        if when > t + fuel:
            return t + fuel
        fuel -= when - t
        t = when
        fuel += d[1]
    return t + max(fuel, 0)
""", [[5, []], [5, [[3, 4]]], [5, [[6, 4]]], [0, [[1, 5]]], [3, [[2, 3], [4, 10]]]], "Move from depot to depot. If the next depot is farther than the fuel lasts, the robot stops before it."),
  FILL("Examples", "Goldbach's conjecture says every even number above 2 is a sum of two {{primes}}. The robot example uses the {{Speed}} Prior as a weak assumption about the environment.")]))

# ------------------------------------------------------------ 10
CHS.append(CH(
 "Relations to other work",
 ("Related ideas", [
  "AIXI | combines | Solomonoff induction and expectimax",
  "AIXI(t,l) | uses | Bounded resources",
  "HSEARCH | is | Hardwired proof search",
  "Gödel machine | rewrites | Its own searcher",
  "OOPS | is | Ordered problem solver",
  "Success-story algorithm | evaluates | Self-modifications"]),
 ["The Gödel machine is compared with several earlier ideas. Hutter's AIXI is a theoretically optimal agent that combines Solomonoff's universal prediction with expectimax planning, but it is incomputable. A resource-bounded variant, AIXI(t,l), is computable but still has a huge constant. Hutter's HSEARCH is a hardwired proof searcher whose search is bias-optimal but cannot be rewritten.",
  "The Gödel machine differs in that its proof searcher can rewrite itself. Related Schmidhuber methods include OOPS, the Success-Story Algorithm for evaluating self-modifications, and Universal Search.",
  "The differences are about what is fixed and what can change, so a table of what is hardwired in each approach is a good way to remember them."],
 [("AIXI", "Hutter's theoretically optimal reinforcement learning agent: Solomonoff induction plus expectimax. Incomputable."),
  ("AIXI(t,l)", "A computable, resource-bounded variant of AIXI with time t and length l, with a very large constant factor."),
  ("HSEARCH", "Hutter's hardwired search for proofs of program properties, bias-optimal but not self-modifying."),
  ("Solomonoff induction", "A universal prediction method that weights every computable hypothesis by 2 to the minus its length."),
  ("Expectimax", "A planning rule: maximize over actions, average over chance outcomes."),
  ("Success-Story Algorithm", "A method that keeps a self-modification only if reward rate improved since it was made."),
  ("KT", "The Levin complexity: program length plus the log of its running time.")],
 ["AIXI is optimal but incomputable; AIXI(t,l) is computable but impractical.",
  "HSEARCH uses a fixed bias-optimal proof search; the Gödel machine can rewrite its search.",
  "OOPS is Schmidhuber's earlier solver that reuses solutions.",
  "The Success-Story Algorithm checks self-modifications empirically, not by proof.",
  "Levin's Kt measures length plus the log of running time.",
  "Each approach differs in what is fixed."],
 [T("The Gödel machine did not appear in a vacuum. The paper compares it with several lines of work. The most important comparison is with Marcus Hutter's AIXI, which was published at around the same time."),
  T("AIXI combines two ideas. Solomonoff induction predicts the future by giving every computable hypothesis a weight of 2 to the minus its length. Expectimax planning then picks, at each step, the action that maximizes expected reward over the predicted futures. The result is optimal in a certain sense for a wide class of environments, but it is incomputable."),
  T("Hutter also gave AIXI(t,l), a computable variant that considers only policies of length at most l and runs each for at most t steps. It is asymptotically optimal in some sense, but the constant is enormous, so it is not practical. Hutter's HSEARCH searches for proofs that a program is optimal, using a fixed bias-optimal scheme."),
  T("The paper's comparison, in short. AIXI(t,l) and HSEARCH have hardwired searchers and do not improve themselves. The Gödel machine's searcher, which is also a bias-optimal proof searcher, can be rewritten by a proven-useful switch, so it can overcome the initial constants over time. That is the claim; it has not been shown in practice."),
  T("Related Schmidhuber methods. The Optimal Ordered Problem Solver, OOPS, solves a sequence of problems and keeps useful earlier programs for reuse. The Success-Story Algorithm, SSA, lets a learner modify itself and keeps a modification only if the reward rate since it was made beats the rate before. SSA checks success empirically, whereas the Gödel machine checks by proof."),
  T("Universal Search by Levin, chapter 8, is the root of the time-allocation idea. A related quantity is Levin complexity, Kt: the length of a program plus the logarithm of its running time. It trades off short code against slow code, and it is the quantity that universal search implicitly minimizes."),
  M(r"Kt(x) \;=\; \min_{p}\big\{\, |p| + \lceil \log_2 \text{steps}(p) \rceil \,\big\}"),
  T("The Speed Prior, also by Schmidhuber, is a prior on environments that favours those computable quickly. It is a weaker, more realistic assumption than the Solomonoff prior, and it appears in the fuel robot example."),
  T("Note the difference between approaches in kind. AIXI is a mathematical definition of an optimal agent. The Gödel machine is a design for an agent that improves itself by proof. They are not competing implementations; they answer different questions, and the paper explicitly discusses how its machine could use AIXI-like components.")],
 [("What does AIXI combine?", ["Hashing and sorting", "Solomonoff induction and expectimax", "Gödel numbering and Rice's theorem", "OOPS and SSA"], 1, "That is Hutter's construction."),
  ("What is the key difference between HSEARCH and the Gödel machine's searcher?", ["HSEARCH is hardwired; the Gödel machine can rewrite its searcher", "HSEARCH is slower", "HSEARCH is a neural network", "There is none"], 0, "Self-modification of the searcher."),
  ("How does the Success-Story Algorithm judge a self-modification?", ["By a proof", "By whether the reward rate improved since it was made", "By its length", "By a vote"], 1, "It is empirical."),
  ("What does Kt measure?", ["Program length plus log running time", "Only length", "Only speed", "Memory use"], 0, "Levin complexity.")],
 [("Is AIXI computable?", "No."), ("Is AIXI(t,l) practical?", "No, the constant is huge."), ("What does OOPS reuse?", "Programs that solved earlier tasks."),
  ("Speed Prior?", "A prior that favours quickly computable environments.")],
 [PL("Expectimax", "A decision tree is a number (a leaf's value), or [\"max\", [children]] (pick the best child), or [\"exp\", [[p, child], ...]] (probability-weighted average of the children). Write expectimax(node): the value of the root.",
     "expectimax(node)", """
def expectimax(node):
    if not isinstance(node, list):
        return node
    kind = node[0]
    if kind == 'max':
        best = None
        for c in node[1]:
            v = expectimax(c)
            if best is None or v > best:
                best = v
        return best
    total = 0
    for pc in node[1]:
        total += pc[0] * expectimax(pc[1])
    return total
""", [[5], [["max", [3, 7, 4]]], [["exp", [[0.5, 10], [0.5, 0]]]], [["max", [["exp", [[0.5, 10], [0.5, 0]]], 4]]], [["exp", [[0.25, ["max", [1, 8]]], [0.75, 4]]]]], "Recurse. A number is a leaf; max takes the largest child value; exp sums probability times child value."),
  PL("Levin complexity cost", "Write kt_cost(length, steps): the program length plus the number of bits needed to write the step count, that is, the smallest b with 2^b at least steps (use a loop, not a library). Treat steps of 1 as 0 bits.",
     "kt_cost(length, steps)", """
def kt_cost(length, steps):
    b = 0
    while 2 ** b < steps:
        b += 1
    return length + b
""", [[10, 1], [10, 2], [10, 1000], [3, 1024], [3, 1025]], "Count how many times you double 1 before reaching steps."),
  MATCH("Related work", "Match each method with its main idea.", [("AIXI", "Solomonoff prediction plus expectimax"), ("AIXI(t,l)", "Computable bounded variant"), ("HSEARCH", "Hardwired bias-optimal proof search"), ("OOPS", "Reuse solutions across tasks"), ("SSA", "Keep modifications that improved reward rate"), ("Speed Prior", "Prefers quickly computable environments")]),
  FILL("Related work", "AIXI combines Solomonoff {{induction}} with {{expectimax}} planning. Unlike HSEARCH, the Gödel machine can rewrite its own {{searcher|proof searcher}}.")]))

# ------------------------------------------------------------ 11
CHS.append(CH(
 "Limits, criticism and open problems",
 ("What is known and unknown", [
  "No full implementation | exists | Yet",
  "Resource bounds | limit | Provable improvements",
  "Blum speed-up | shows | Some problems lack optimal programs",
  "Löb's theorem | creates | Löbian obstacle",
  "Steunebrink and Schmidhuber | studied | Implementation",
  "Speculation | is | Author's own"]),
 ["The Gödel machine remains a theoretical design. Resource limits mean it can prove only improvements whose proofs fit in time and space; by Rice's theorem it must ignore many useful changes; and by Blum's speed-up theorem some problems have no optimal program at all.",
  "Löb's theorem, a relative of Gödel's second incompleteness theorem, creates the Löbian obstacle: an agent that trusts its own proofs seems to run into a barrier when it tries to prove that a successor which uses the same reasoning is safe. Yudkowsky and Herreshoff studied this in the context of self-modifying systems.",
  "Steunebrink and Schmidhuber explored what an implementation would need, such as a solver and searcher pair and meta-circular evaluators. Claims about consciousness or about humans being Gödel machines are speculation by the author and are not results."],
 [("Löb's theorem", "If a system can prove that provability of P implies P, then it can prove P. It restricts self-trust."),
  ("Löbian obstacle", "The difficulty that an agent cannot straightforwardly prove that a proof-using successor is safe, because of Löb's theorem."),
  ("Blum speed-up theorem", "There are computable problems for which every program can be replaced by a much faster one, so no optimal program exists."),
  ("Meta-circular evaluator", "An interpreter for a language written in that language itself."),
  ("Resource bound", "A limit on time or space available for finding proofs."),
  ("Speculative claim", "A statement not backed by a theorem or an experiment.")],
 ["No complete implementation of the Gödel machine exists.",
  "Unprovable improvements are ignored; Rice's theorem makes many properties undecidable.",
  "Blum: some problems have no fastest program.",
  "Löb's theorem limits an agent's trust in its own proofs.",
  "Implementation studies define Solver and Searcher parts and use meta-circular evaluators.",
  "Philosophical claims such as that humans are Gödel machines are speculation."],
 [T("This chapter collects the limits, in the spirit of reading the paper with a critical eye. The first is the simplest: there is no complete implementation. The design is mathematically precise, but running it needs a lot of engineering that nobody has shown to work."),
  T("Second, resources. The paper admits that a machine with limited time and space cannot profit from improvements whose proofs are too long. It also admits that by Rice's theorem many useful improvements are undecidable. Even with unlimited resources, the machine must ignore those self-improvements whose effectiveness it cannot prove."),
  T("Third, the Blum speed-up theorem. Manuel Blum showed that there are computable problems for which every program has a much faster one, so there is no optimal program. The paper notes that for such problems no solver can be best, and a Gödel machine can only keep speeding up."),
  T("Fourth, the Löbian obstacle. Löb's theorem says that if a system proves that provability of a statement implies the statement, then it proves the statement. As a result a consistent system cannot assert that its own proofs are sound. For a self-modifying agent that approves a successor only when it can prove the successor safe, this blocks a naive proof that a successor with the same reasoning is safe."),
  T("Yudkowsky and Herreshoff's work at the Machine Intelligence Research Institute discusses this obstacle in detail and explores partial ways around it. Their conclusion is that tiling, an agent trusting a successor of its own kind, is hard under the straightforward proof-based approach. This is a research problem, not a refutation: the Gödel machine's target theorem asks about utility, not trust in the successor's proofs, and it is not settled how the two connect."),
  T("Fifth, the question of implementation. Steunebrink and Schmidhuber's paper on Gödel machine implementations describes an architecture with a Solver, which acts in the environment, and a Searcher, which looks for proofs, using meta-circular evaluators so that the system can interpret and modify its own code. They also describe a system called Sleight. Their work shows how much is needed beyond the original mathematical description."),
  T("Finally, a word on speculation. Schmidhuber has suggested connections between the Gödel machine and consciousness, and has suggested that humans may be Gödel machines in a loose sense. These are the author's own views; they are not derived from the theorems and are not established. The course marks them as speculative, and so should anyone who cites them."),
  T("The practical lesson is to read the guarantees carefully. They say: given consistent axioms, correct hardware and enough time, each executed rewrite is globally optimal. They do not say that a real system exists, that the axioms are right, or that proofs will be found in time."),
  T("In the practice section you simulate a resource-bounded machine that can use only provable rewrites that fit in a proof budget, which shows what the ignore-the-unprovable rule means in practice.")],
 [("What is the status of the Gödel machine?", ["Fully implemented", "A theoretical design with no complete implementation", "A product", "Refuted"], 1, "Implementation studies exist but no full system."),
  ("What does the Blum speed-up theorem imply?", ["All problems have fastest programs", "Some problems have no optimal program", "Proofs are short", "P equals NP"], 1, "Every program can be beaten."),
  ("What does Löb's theorem restrict?", ["Memory size", "A system's ability to assert that its own proofs are sound", "Prime numbers", "Search speed"], 1, "That leads to the Löbian obstacle."),
  ("How should claims that humans are Gödel machines be treated?", ["As proven", "As speculation by the author", "As refuted", "As axioms"], 1, "They are not derived from the theorems.")],
 [("What do Steunebrink and Schmidhuber describe?", "An implementation architecture with a Solver and a Searcher."), ("Who studied the Löbian obstacle?", "Yudkowsky and Herreshoff, among others."), ("Rice's theorem effect?", "Many improvements cannot be proved."),
  ("Are guarantees unconditional?", "No, they depend on consistent axioms and enough resources.")],
 [PL("Provable rewrites within a budget", "Candidates are [name, gain, provable, proof_cost]. The machine has a proof budget. It considers only provable candidates, in order of gain from highest to lowest (ties keep the original order), and takes a candidate if its proof_cost fits in what is left of the budget, subtracting the cost. Skip candidates that do not fit and carry on. Write choose_rewrites(cands, budget): the list of chosen names in the order taken.",
     "choose_rewrites(cands, budget)", """
def choose_rewrites(cands, budget):
    items = []
    for i in range(len(cands)):
        c = cands[i]
        if c[2]:
            items.append([-c[1], i, c[0], c[3]])
    items.sort()
    left = budget
    out = []
    for it in items:
        if it[3] <= left:
            left -= it[3]
            out.append(it[2])
    return out
""", [[[["a", 5, True, 10], ["b", 9, True, 20], ["c", 12, False, 1]], 25], [[["a", 5, True, 10], ["b", 9, True, 20]], 100], [[["a", 5, True, 10], ["b", 5, True, 10]], 10], [[["a", 5, False, 1]], 10], [[], 10]], "Filter to provable ones, sort by gain descending (stable), then take greedily while the budget lasts."),
  MATCH("Limits", "Match each limit with its source.", [("Some problems have no fastest program", "Blum speed-up theorem"), ("Many program properties are undecidable", "Rice's theorem"), ("Self-trust obstacle", "Löb's theorem"), ("Unprovable improvements are skipped", "Provability gate"), ("Consciousness claims", "Speculation")]),
  FILL("Limits", "No full {{implementation}} of the Gödel machine exists. The {{Löbian}} obstacle comes from Löb's theorem. Claims about consciousness are {{speculative|speculation}}.")]))

# ------------------------------------------------------------ 12
CHS.append(CH(
 "Build a toy Gödel machine",
 ("A toy model", [
  "Toy machine | has | Rate and horizon",
  "Candidate | has | New rate, cost and proof time",
  "Proof time | uses | Part of the horizon",
  "Switch rule | compares | Stay and switch totals",
  "Share | is | Fraction spent on searching",
  "Toy machine | omits | Real proof search"]),
 ["The capstone is a toy model that keeps the essential logic: the machine earns reward at a rate, searches for proofs about candidate rewrites, and switches only when the proved total reward is strictly higher than staying.",
  "Each candidate has a new rate, a switching cost and a proof time. Searching takes part of the machine's effort, modelled by a share. The toy leaves out real logic: the proofs are replaced by arithmetic.",
  "Building it ties the earlier chapters together: the target theorem is the comparison, the proof time is the delay, and the order of candidates is the search order."],
 [("Rate", "Reward per step of the current policy."),
  ("Horizon", "The total number of steps in the machine's life."),
  ("Candidate", "A possible rewrite with a new rate, a switch cost and a proof time."),
  ("Proof time", "Steps needed to prove the candidate's target theorem."),
  ("Share", "Percentage of effort spent on searching, which reduces earned reward."),
  ("Toy model", "A simplified model that keeps the main logic and drops the details.")],
 ["Process candidates in order.",
  "Searching for the proof of a candidate takes its proof time, during which reward is earned at a reduced rate.",
  "Switch only if switching is strictly better than staying for the remaining time.",
  "Skip candidates whose proof would not finish before the end.",
  "Integer arithmetic keeps results exact.",
  "This is a model, not an implementation."],
 [T("Now put it together. The toy machine has an integer reward rate and a horizon, the number of steps in its life. It also has a list of candidate rewrites. Each candidate has a name, a new rate, a switching cost in steps, and a proof time, the number of steps its proof search needs."),
  T("The machine works through the candidates in order. For each one it spends the proof time searching. During the search it still acts, but a share of its effort goes to searching, so the reward is reduced to the rate times 100 minus the share, divided by 100, using integer division."),
  M(r"\text{reward}(n,\ r) \;=\; \left\lfloor \frac{n \cdot r \cdot (100 - \text{share})}{100} \right\rfloor"),
  T("When the proof is done, the machine compares two totals for the remaining time. Staying earns the remaining steps at the current rate, with the share applied. Switching loses the cost steps, then earns the rest at the new rate, with the share applied. If switching is strictly greater, the machine switches: it spends the cost steps, sets the new rate and records the candidate's name."),
  T("A candidate is skipped when its proof time would not finish before the end: if the current time plus the proof time is at least the horizon, the machine stops searching and just earns until the end. A rejected candidate still costs its proof time, as in a real search."),
  T("At the end, add the reward from the current time to the horizon at the current rate. Return the total and the names of the candidates that were switched to, in order. This function is the capstone lab."),
  T("Try it with numbers. Rate 10, horizon 100, share 0. Candidate A: new rate 14, cost 5, proof time 10. After 10 steps, t is 10 and total 100. Remaining 90. Stay: 900. Switch: 85 times 14 which is 1190. Switch, t becomes 15, rate 14. Then 85 steps at 14 add 1190. The total is 1290."),
  T("Compare with the theory. The toy keeps three properties: a rewrite happens only when the comparison says it is strictly better, comparison is with staying for the rest of the time, and time spent searching is paid for. It omits the axioms, the logic, the self-reference and the rewriting of the searcher. So it illustrates the decision rule, not the machine."),
  T("You have reached the end of the course. The exam mixes questions from every chapter. Keep the sources in mind: the Wikipedia article, Schmidhuber's report, the Steunebrink and Schmidhuber paper, and the Yudkowsky and Herreshoff work. Treat the speculative parts as the author's opinions.")],
 [("When does the toy machine switch?", ["Whenever a candidate exists", "When switching is strictly better than staying for the remaining time", "At random", "At time zero"], 1, "That mirrors the target theorem."),
  ("What does the share model?", ["Memory", "The fraction of effort spent on searching", "The reward", "The cost"], 1, "It reduces the earned reward."),
  ("What does the toy model omit?", ["The decision rule", "The axioms, logic and self-reference", "Time", "Rewards"], 1, "It keeps only the arithmetic."),
  ("What happens to a candidate whose proof time runs past the horizon?", ["It is applied anyway", "The machine stops searching and just earns", "It is doubled", "It is repeated"], 1, "There is no time left to use it.")],
 [("What is the strict rule?", "Switch only if switch total > stay total."), ("What is the share?", "Percentage of effort used for searching."), ("What is a rejected candidate?", "One whose proof was found but whose switch is not strictly better."),
  ("Does the toy prove anything?", "No, it computes the comparison directly.")],
 [PL("The toy Gödel machine", "Write toy_godel(rate0, horizon, candidates, share). Start with t = 0, total = 0, rate = rate0, and an empty list of switched names. For each candidate [name, new_rate, cost, proof_time] in order: if t + proof_time >= horizon, stop. Otherwise add the reward for proof_time steps at the current rate, namely proof_time * rate * (100 - share) // 100, and move t forward by proof_time. Let remaining = horizon - t. stay = remaining * rate * (100 - share) // 100. switch = (remaining - cost) * new_rate * (100 - share) // 100, but never below 0 (if remaining < cost use 0). If switch > stay, then t += cost, rate = new_rate, and append the name (the cost steps earn nothing). At the end add (horizon - t) * rate * (100 - share) // 100. Return [total, switched_names].",
     "toy_godel(rate0, horizon, candidates, share)", """
def toy_godel(rate0, horizon, candidates, share):
    t = 0
    total = 0
    rate = rate0
    names = []
    for c in candidates:
        name = c[0]
        new_rate = c[1]
        cost = c[2]
        ptime = c[3]
        if t + ptime >= horizon:
            break
        total += ptime * rate * (100 - share) // 100
        t += ptime
        remaining = horizon - t
        stay = remaining * rate * (100 - share) // 100
        if remaining < cost:
            sw = 0
        else:
            sw = (remaining - cost) * new_rate * (100 - share) // 100
        if sw > stay:
            t += cost
            rate = new_rate
            names.append(name)
    total += (horizon - t) * rate * (100 - share) // 100
    return [total, names]
""", [[10, 100, [["A", 14, 5, 10]], 0], [10, 100, [["A", 11, 40, 10]], 0], [10, 100, [["A", 14, 5, 10], ["B", 20, 10, 20]], 0], [10, 100, [["A", 14, 5, 95]], 0], [10, 100, [["A", 12, 5, 10], ["B", 12, 5, 10]], 20], [10, 100, [], 50]],
     "Follow the steps in order. Use integer arithmetic exactly as described. Break out of the loop when the proof cannot finish before the horizon."),
  MATCH("Toy and theory", "Match each part of the toy with the theory it mirrors.", [("switch > stay", "Strict target theorem"), ("proof_time", "Delay before the switch"), ("Candidate order", "Search order"), ("share", "Cost of running the searcher"), ("Break when out of time", "No time left to use a proof")]),
  FILL("Capstone", "The toy machine switches only if the switch total is {{strictly|strictly greater}} better than staying. Time spent on {{proof|proof search|searching}} is paid for in reward.")]))
