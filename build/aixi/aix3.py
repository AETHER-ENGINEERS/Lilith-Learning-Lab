"""AIXI course, chapters 9-12."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 9
CHS.append(CH(
 "Optimality and universal intelligence",
 ("Optimality", [
  "Pareto optimality | means | No policy dominates",
  "Balanced Pareto | weights | Environments",
  "Self-optimizing | means | Value approaches the best possible",
  "Universal intelligence | is | Weighted sum of values",
  "Weight | is | 2 to minus K of environment",
  "AIXI | maximizes | Universal intelligence",
  "Legg and Hutter | defined | Upsilon"]),
 ["Hutter argued that AIXI is optimal in several senses. A policy is Pareto optimal if no other policy does at least as well in every environment and strictly better in one. Balanced Pareto optimality uses a weighted sum over environments.",
  "Legg and Hutter turned the weighted sum into a definition of machine intelligence: an agent's universal intelligence is its expected reward in each computable environment, weighted by two to the minus the environment's complexity. AIXI maximizes it by construction.",
  "Chapter 12 shows that these notions depend heavily on the choice of prior and reference machine, so read them as results about a particular setup."],
 [("Pareto optimal", "No other policy is at least as good everywhere and strictly better somewhere."),
  ("Balanced Pareto optimal", "Maximizes the prior-weighted sum of values over environments."),
  ("Self-optimizing", "Its average value approaches the maximum possible as the lifetime grows, in every environment where some policy can do so."),
  ("Universal intelligence", "Upsilon(pi) = sum over environments of 2^-K(mu) times the value of pi in mu."),
  ("Value", "Expected total reward of a policy in an environment."),
  ("Informal definition", "Intelligence measures an agent's ability to achieve goals in a wide range of environments.")],
 ["Pareto optimality is a weak requirement: no policy dominates.",
  "Balanced Pareto optimality maximizes the weighted sum of values.",
  "Upsilon(pi) = sum_mu 2^-K(mu) V(pi, mu), with total reward at most 1 in each environment.",
  "AIXI attains the maximum Upsilon, relative to its prior.",
  "Random agents score low; specialist agents such as a chess program score very low.",
  "Later work found these claims are subjective: they depend on the prior."],
 [T("What would it mean for an agent to be as good as possible? Hutter's book proves several statements in answer. Here are the main ones in plain terms."),
  T("Pareto optimality. Compare policies by their values in each environment of a class. A policy is Pareto optimal if no other policy is at least as good in every environment and strictly better in at least one. AIXI's mixture-based policy has this property in the class it mixes over. The property is weak, since many policies can be Pareto optimal at once."),
  T("Balanced Pareto optimality. Give each environment its prior weight and sum the values. The policy with the highest weighted sum is balanced Pareto optimal. AIXI is such a policy by construction, because it maximizes expected reward under the mixture, and the mixture is the weighted sum."),
  T("Self-optimizing. A policy is self-optimizing if, as the lifetime grows, its average reward per step approaches the best possible one for the true environment, whatever that environment is. This is what we hope a general learner does: eventually behave as if it knew the world. Hutter's results say a Bayes-optimal policy for a mixture is self-optimizing whenever self-optimizing policies exist for the class."),
  T("Universal intelligence. Shane Legg and Hutter turned the weighted sum into a definition. They started from many expert definitions of intelligence and condensed them to a sentence: intelligence measures an agent's ability to achieve goals in a wide range of environments. The formalization sums, over all computable environments mu, the agent's value there, weighted by two to the minus the complexity of mu."),
  M(r"\Upsilon(\pi) \;=\; \sum_{\mu \in E} 2^{-K(\mu)}\, V^{\pi}_{\mu}"),
  T("To make the sum finite they require that the total reward in any environment is at most one. The paper then checks the measure on examples: a random agent scores low, a program such as Deep Blue that is expert at only one kind of environment scores very low, and learning agents rise as they use more history and look further ahead. AIXI attains the maximum possible value, and the measure is incomputable because complexity is."),
  T("A careful reader should note two things. The measure rewards breadth, since simple environments are numerous and heavy. And the weights depend on the reference machine used for complexity, so what counts as general intelligence is relative to that choice. Chapter 12 explains how bad the dependence can get.")],
 [("What is Pareto optimality?", ["No policy dominates it everywhere", "It has the highest reward", "It uses the shortest program", "It is random"], 0, "A weak, dominance-based property."),
  ("What does Upsilon sum over?", ["Computable environments weighted by 2^-K", "Actions", "Time steps", "Programs of one length"], 0, "Weighted values."),
  ("Who defined universal intelligence?", ["Legg and Hutter", "Turing", "Minsky", "Shannon"], 0, "Minds and Machines, 2007."),
  ("Why require total reward at most 1?", ["To keep the sums finite without discounting", "To make rewards negative", "To save memory", "For fairness to humans"], 0, "It replaces discounting.")],
 [("What does self-optimizing mean?", "Average reward approaches the best possible."), ("Which agents score low on Upsilon?", "Random and narrow specialists."), ("Is Upsilon computable?", "No, because K is not."),
  ("What does AIXI maximize?", "Upsilon relative to its prior.")],
 [PL("Pareto dominance", "Write dominates(a, b): True if the list of values a is at least as large as b in every environment and strictly larger in at least one.",
     "dominates(a, b)", """
def dominates(a, b):
    strict = False
    for x, y in zip(a, b):
        if x < y:
            return False
        if x > y:
            strict = True
    return strict
""", [[[3, 2], [2, 2]], [[2, 2], [2, 2]], [[3, 1], [1, 3]], [[1, 1, 1], [0, 1, 1]], [[0, 5], [1, 4]]], "Fail on any smaller entry; remember whether any entry is larger."),
  PL("Pareto-optimal policies", "values[i][e] is the value of policy i in environment e. Write pareto_front(values): the sorted list of indices of policies that no other policy dominates (dominate: at least as good everywhere and strictly better somewhere).",
     "pareto_front(values)", """
def pareto_front(values):
    def dom(a, b):
        strict = False
        for x, y in zip(a, b):
            if x < y:
                return False
            if x > y:
                strict = True
        return strict
    front = []
    for i in range(len(values)):
        ok = True
        for j in range(len(values)):
            if j != i and dom(values[j], values[i]):
                ok = False
                break
        if ok:
            front.append(i)
    return front
""", [[[[3, 2], [2, 2], [1, 4]]], [[[1, 1], [1, 1]]], [[[5, 0], [0, 5], [2, 2], [1, 1]]], [[[2, 3, 1], [2, 3, 2], [3, 0, 0]]]], "Index i is kept if nobody dominates it."),
  PL("Universal intelligence of a toy agent", "Environments e have complexities ks[e] (integers) and an agent has values vals[e] in each. Write upsilon(vals, ks): the sum of 2 to the minus ks[e] times vals[e].",
     "upsilon(vals, ks)", """
def upsilon(vals, ks):
    total = 0.0
    for v, k in zip(vals, ks):
        total += v * 2.0 ** (-k)
    return total
""", [[[1, 1, 1], [1, 2, 3]], [[0.5, 0.0, 1.0], [2, 3, 4]], [[0, 0], [1, 1]], [[1.0], [1]], [[0.25, 0.75, 0.5, 1.0], [1, 2, 3, 4]]], "Add each value times a power of two.", approx=1e-12),
  PL("Which agent is the most intelligent?", "agents[i] is the list of values of agent i, one per environment; ks holds complexities. Write best_agent(agents, ks): the index of the agent with the largest universal intelligence (ties go to the smaller index).",
     "best_agent(agents, ks)", """
def best_agent(agents, ks):
    best = -1.0
    arg = 0
    for i in range(len(agents)):
        s = 0.0
        for v, k in zip(agents[i], ks):
            s += v * 2.0 ** (-k)
        if s > best + 1e-12:
            best = s
            arg = i
    return arg
""", [[[[1, 0, 0], [0, 1, 1], [0.5, 0.5, 0.5]], [1, 2, 3]], [[[1, 0, 0], [0, 1, 1], [0.5, 0.5, 0.5]], [3, 2, 1]], [[[1, 1], [1, 1]], [1, 2]], [[[0, 0, 1], [0, 1, 0]], [1, 1, 1]]], "Compute the weighted sum for each agent and keep the argmax."),
  ORDER("Building Upsilon", "Order the steps in the Legg-Hutter definition.", ["Collect expert definitions of intelligence", "State the informal definition", "Model agents and environments as reward interaction", "Weight each environment by 2 to the minus K", "Sum the agent's values"]),
  MATCH("Optimality", "Match each notion with its meaning.", [("Pareto optimal", "Not dominated"), ("Balanced Pareto optimal", "Best weighted sum"), ("Self-optimizing", "Average reward approaches the best"), ("Universal intelligence", "Weighted value over all environments"), ("Random agent", "Scores low on Upsilon")]),
  FILL("Universal", "Universal intelligence weighs each environment by two to the minus its {{complexity|Kolmogorov complexity}}. AIXI maximizes it, but the measure is {{incomputable|not computable}}.")]))

# ------------------------------------------------------------ 10
CHS.append(CH(
 "Incomputability and AIXItl",
 ("Computability", [
  "AIXI | needs | All programs",
  "Halting problem | blocks | Exact AIXI",
  "AIXItl | bounds | Time t and length l",
  "AIXItl cost | is | t times 2 to the l",
  "Levin search | splits | Time by 2 to minus length",
  "Speed prior | penalizes | Slow programs",
  "Limit-computable | means | Approximable in the limit"]),
 ["AIXI looks at every program, including ones that never halt, so it is not computable. The limits can be pinned down in the arithmetical hierarchy: Leike and Hutter show planning in general computable environments is hard even in principle.",
  "Hutter's own response was AIXItl: restrict attention to policies of length at most l that run at most t steps per cycle. It is computable but its running time is of the order t times two to the l, and it is useless in practice.",
  "Two ideas help to see why: Levin search shares time among programs in proportion to two to the minus their length, and a speed prior, proposed by Schmidhuber, penalizes slow programs as well as long ones."],
 [("Halting problem", "Deciding whether a program ever stops; undecidable."),
  ("AIXItl", "A time- and length-bounded version of AIXI: policies of length at most l, at most t steps per cycle."),
  ("Levin search", "Run all programs in parallel, giving program p a share of time proportional to 2^-length(p)."),
  ("Speed prior", "A prior that favors programs that are both short and fast."),
  ("Arithmetical hierarchy", "A classification of undecidable problems by quantifier alternations."),
  ("Limit computable", "The value is the limit of a computable sequence of guesses.")],
 ["Exact AIXI is incomputable: it needs to know which programs halt.",
  "AIXItl is computable with a cost of about t * 2^l per cycle.",
  "Levin search allocates time 2^-length to each program.",
  "Leike and Hutter: finding an optimal policy is Pi_2-hard and finding an epsilon-optimal one is undecidable in general semicomputable environments.",
  "By default AIXI is not even limit computable, but a limit-computable epsilon-optimal variant exists.",
  "Schmidhuber's speed prior replaces M to give an approximable alternative."],
 [T("Why can't we just run AIXI? Look at the sum inside the equation. It ranges over every program q on the universal machine that reproduces the history. To know whether a given q reproduces it, we must run q until it prints the whole history. If q loops forever before printing a symbol, we wait forever. Whether it ever prints is the halting problem, which no algorithm solves."),
  T("So AIXI is not a procedure at all; it is a specification. The theory of computation tells us how bad that is. Leike and Hutter's paper On the Computability of AIXI classifies it. For general semicomputable environments they show that finding an optimal policy is hard at the level called Pi two in the arithmetical hierarchy, and that finding even an epsilon-optimal policy is undecidable. By default AIXI is not limit computable, which means it cannot even be approximated from a computable sequence of guesses that converge."),
  T("They do identify a way out: with the recursive rather than the iterative form of the value function, and an epsilon-optimal action rule that never needs to decide exact ties, one gets a limit-computable epsilon-optimal agent with infinite horizon. Limit computable means a program can output a sequence of better and better guesses that converge, though without knowing when to stop. That is as good as approximation gets for hard problems."),
  T("Hutter's earlier answer was AIXItl, in his survey. Fix a time bound t and a length bound l. Consider only policies, written as programs, of length at most l, that finish a cycle within t steps. Among those, for which one can prove a lower bound on value, pick the best. The result is an agent that, by Hutter's claim, is effectively more intelligent than any other agent bounded by t and l. Its computation time per cycle is of the order t times two to the power l."),
  M(r"\text{time per cycle of AIXI}tl \;\sim\; t \cdot 2^{\,l}"),
  T("Two to the l is the number of candidate programs, and each is allowed t steps. For l equal to forty, a modest program size, that is a trillion programs. So AIXItl is a theoretical bridge from the incomputable to the computable, but not a practical algorithm. The survey also says its construction needs a proof system, a first-order logic in which statements about program values can be established."),
  T("A neighbouring idea is Levin search. To find a program that solves a problem and can be checked, run all programs in parallel, giving program p a fraction two to the minus its length of the total time. A program of length l that needs s steps will finish within about two to the l times s steps of total time. Short programs are tried most. This is the same Occam weighting as in the universal prior, put to work in time."),
  T("Schmidhuber's speed prior, mentioned in a 2003 survey that discusses AIXI, replaces the incomputable prior by one that is approximable by also penalizing running time. The survey says one can modify the AIXI model to use it. It is an example of the general move: when the ideal is out of reach, change the prior to favour things that can be computed.")],
 [("Why is AIXI incomputable?", ["It needs to know which programs halt", "It uses too much memory", "It is random", "It has no reward"], 0, "Halting problem."),
  ("What does AIXItl restrict?", ["Policy length and runtime", "Rewards", "Actions", "Horizons only"], 0, "Length at most l, time t per cycle."),
  ("What is AIXItl's cost per cycle?", ["About t times 2^l", "Constant", "Linear in t", "Logarithmic"], 0, "Exponential in l."),
  ("How does Levin search divide time?", ["2^-length per program", "Equally", "By program age", "Randomly"], 0, "Short programs get more.")],
 [("What is limit computable?", "Approximated by a converging computable sequence."), ("What is the speed prior?", "A prior that penalizes slowness as well as length."), ("Is AIXItl practical?", "No, the cost is exponential in l."),
  ("What does Pi_2-hard say?", "Very hard, above ordinary undecidability.")],
 [PL("How many candidate programs?", "Write count_programs(l): the number of bit-string programs of length at most l, including the empty program.",
     "count_programs(l)", """
def count_programs(l):
    total = 0
    for n in range(l + 1):
        total += 2 ** n
    return total
""", [[0], [1], [3], [10], [20]], "Add 2^n for n from 0 to l."),
  PL("AIXItl cost", "Write aixitl_cost(t, l): the number of machine steps per cycle when every program of length at most l is run for t steps. Use the count of programs from the previous lab.",
     "aixitl_cost(t, l)", """
def aixitl_cost(t, l):
    return t * (2 ** (l + 1) - 1)
""", [[1, 0], [10, 3], [1000, 10], [5, 20], [100, 30]], "Programs times steps; the number of programs is 2^(l+1) - 1."),
  PL("Levin time shares", "Write levin_shares(lengths, total): for each program length, the integer number of steps it gets, floor(total / 2^length).",
     "levin_shares(lengths, total)", """
def levin_shares(lengths, total):
    out = []
    for l in lengths:
        out.append(total // (2 ** l))
    return out
""", [[[1, 2, 3], 64], [[0, 5], 100], [[4, 4, 8], 1024], [[10], 1000], [[2, 3, 5, 7], 4096]], "Use integer division."),
  PL("Which programs finish?", "programs[i] = [length, steps needed, correct (1 or 0)]. With a total budget T, program i is run for T // 2^length steps and finishes if steps needed is at most that. Write levin_found(programs, T): the indices of programs that finish and are correct, ordered by length and then by index.",
     "levin_found(programs, T)", """
def levin_found(programs, T):
    found = []
    for i in range(len(programs)):
        l = programs[i][0]
        s = programs[i][1]
        ok = programs[i][2]
        if ok == 1 and s <= T // (2 ** l):
            found.append([l, i])
    found.sort()
    return [x[1] for x in found]
""", [[[[3, 10, 1], [5, 2, 1], [2, 40, 1], [4, 1, 0]], 640], [[[3, 10, 1], [5, 2, 1], [2, 40, 1], [4, 1, 0]], 100], [[[1, 5, 1], [1, 5, 1]], 10], [[[6, 3, 1], [2, 100, 1]], 1000], [[[2, 1, 1]], 3]], "Check the budget with integer division; sort pairs of (length, index)."),
  MATCH("Computability", "Match each item with its meaning.", [("Halting problem", "Blocks exact AIXI"), ("AIXItl", "Bounded policies of length l and time t"), ("Levin search", "2^-length time shares"), ("Speed prior", "Penalizes slow programs"), ("Limit computable", "Converging computable guesses")]),
  ORDER("Why exact AIXI fails", "Order the argument.", ["The equation sums over all programs", "A program counts only if it prints the history", "Some programs run forever before printing", "Deciding which ones is the halting problem", "So the sum cannot be computed"]),
  FILL("Bounds", "AIXItl costs about t times {{2^l|two to the l|2 to the l}} per cycle. Levin search gives program p a time share of two to the minus its {{length}}. Exact AIXI hits the {{halting}} problem.")]))

# ------------------------------------------------------------ 11
CHS.append(CH(
 "Monte Carlo AIXI with context tree weighting",
 ("Approximation", [
  "MC-AIXI-CTW | approximates | AIXI",
  "Context tree weighting | learns | Environment model",
  "KT estimator | predicts | Next bit",
  "Prediction suffix tree | is | A context model",
  "rho-UCT | plans | By sampling",
  "Mixture | over | Tree structures",
  "Veness et al. | published | JAIR 2011"]),
 ["Veness, Ng, Hutter, Uther and Silver built the first computationally feasible AIXI approximation. It replaces the mixture over all programs with a mixture over prediction suffix trees, computed exactly by context tree weighting, and replaces the exact expectimax with a Monte Carlo tree search.",
  "The KT estimator predicts the next bit from counts of zeros and ones. A context tree uses KT estimators at the leaves and mixes over all tree depths. The prior favors small trees, an Occam's razor for context models.",
  "The agent, called MC-AIXI-CTW, learned small stochastic and partially observable games, including a version of Pac-Man."],
 [("Context tree weighting (CTW)", "A method that predicts the next bit by mixing all context trees up to a depth, efficiently."),
  ("KT estimator", "Krichevsky-Trofimov: next bit is 1 with probability (b + 1/2) / (a + b + 1) after a zeros and b ones."),
  ("Prediction suffix tree", "A tree whose paths are recent history suffixes and whose leaves hold bit statistics."),
  ("rho-UCT", "A Monte Carlo tree search for the agent setting that samples histories from the learned model."),
  ("UCB", "A bandit rule choosing the action with the best average plus an exploration bonus."),
  ("Factored CTW", "A variant that predicts each bit of a structured percept.")],
 ["MC-AIXI-CTW is a direct approximation of AIXI: CTW for learning, rho-UCT for planning.",
  "KT: P(next = 1) = (b + 0.5) / (a + b + 1).",
  "A CTW node mixes its own KT estimate and the product of its children's weighted estimates, equally.",
  "The prior over trees is 2^-(code length of the tree), preferring small trees.",
  "rho-UCT picks actions with an upper confidence bound and samples percepts from the model.",
  "It is a principled approximation, not a scaled-up success on large problems."],
 [T("The paper by Veness and colleagues, published in 2011 in the Journal of Artificial Intelligence Research, answers a question left open since AIXI appeared: can the theory guide a practical algorithm? Its answer is yes for small domains. Every part of AIXI is replaced by something computable."),
  T("Learning first. Instead of all programs, the model class is a set of context trees. A context tree is a tree whose branches spell out the most recent bits of the history, and whose leaves keep counts of what came next. To predict a bit in a leaf, the paper uses the KT estimator. After a zeros and b ones, the probability that the next bit is one is b plus one half, divided by a plus b plus one. It follows from a Bayesian analysis with a Jeffreys prior on the coin."),
  M(r"P_{\mathrm{KT}}(1 \mid a \text{ zeros},\, b \text{ ones}) \;=\; \dfrac{b + \tfrac12}{a + b + 1}"),
  T("Context tree weighting mixes all trees up to a fixed depth with one trick. At a leaf, the weighted probability equals the KT probability. At an inner node, it is the average of two quantities with equal weight: the node's own KT probability, and the product of its two children's weighted probabilities. This splits the choice at each node between stopping here and looking one bit further back. Working through the tree computes, in time linear in the depth per bit, a Bayesian mixture over exponentially many tree shapes."),
  T("The prior over a tree M is two to the minus a code length for its structure, so small trees are preferred. This is the same Occam weighting as the universal prior, but over a class small enough to compute. The agent version feeds actions into the history without updating the statistics for them, since the agent chooses actions and only predicts percepts."),
  T("Planning second. Expectimax over the learned model is too big, so the paper uses a Monte Carlo tree search that it calls rho-UCT. Each simulation picks actions in the tree by an upper confidence bound: average value scaled to the reward range, plus a constant times the square root of the log of the history's visit count over the action's visit count. Percepts are sampled from the learned model. After the tree runs out, the simulation continues with random actions."),
  T("The search is an anytime algorithm: more simulations give a better action. It needs a horizon m and an exploration constant C. A small C makes deep, narrow trees, a large C makes shallow, bushy ones."),
  T("What was achieved? The abstract reports encouraging results on a variety of stochastic and partially observable domains, and the survey literature mentions a Pac-Man game with partial observation. These are small worlds. The significance is conceptual: AIXI's two halves became working components, and the gap between theory and practice was narrowed, not closed."),
  T("The practice section builds the pieces: the KT estimator, a depth-one context tree weighting, the UCB selection rule, and finally a tiny model-based agent that learns an environment with KT counts and chooses actions by its predictions. The agent is my own teaching miniature, not the paper's code.")],
 [("What does CTW do?", ["Mixes context trees to predict the next bit", "Plays chess", "Compresses images only", "Chooses actions"], 0, "It is the learning half of MC-AIXI-CTW."),
  ("KT estimate after a zeros and b ones:", ["(b + 1/2) / (a + b + 1)", "b / (a + b)", "1/2 always", "a / b"], 0, "A Jeffreys prior."),
  ("What does rho-UCT approximate?", ["Expectimax planning", "Solomonoff induction", "The halting problem", "The reward"], 0, "A sampled search through the tree."),
  ("What does the tree prior prefer?", ["Small trees", "Large trees", "Deep trees", "Random trees"], 0, "2^-code length.")],
 [("What is a suffix tree?", "A context model whose paths spell recent history."), ("Who wrote the MC-AIXI paper?", "Veness, Ng, Hutter, Uther and Silver."), ("Why mix over trees?", "To avoid fixing the context depth in advance."),
  ("Is MC-AIXI scaled up?", "It worked on small domains.")],
 [PL("KT probability of a string", "Write kt_block(bits): the KT probability of the whole bit string, starting from zero counts and multiplying the sequential predictions (b + 0.5) / (a + b + 1) for each bit (use a = zeros so far, b = ones so far; for a 0 use 1 minus that prediction).",
     "kt_block(bits)", """
def kt_block(bits):
    a = 0
    b = 0
    p = 1.0
    for x in bits:
        q = (b + 0.5) / (a + b + 1)
        if x == 1:
            p *= q
            b += 1
        else:
            p *= 1 - q
            a += 1
    return p
""", [[[]], [[1]], [[0, 0, 0]], [[1, 0, 1, 1]], [[0, 1, 0, 1, 0, 1]], [[1, 1, 1, 1, 1]]], "Keep counts and update them after each bit.", approx=1e-12),
  PL("Depth-one context tree weighting", "Contexts: the bit before each bit (before the first bit the context is 0). Write ctw1(bits): the weighted probability at the root = 0.5 * P_KT(whole string) + 0.5 * P_KT(bits whose context is 0) * P_KT(bits whose context is 1), where each P_KT is the KT probability of the subsequence (the leaves are weighted probability = KT probability).",
     "ctw1(bits)", """
def ctw1(bits):
    def kt(seq):
        a = 0
        b = 0
        p = 1.0
        for x in seq:
            q = (b + 0.5) / (a + b + 1)
            if x == 1:
                p *= q
                b += 1
            else:
                p *= 1 - q
                a += 1
        return p
    c0 = []
    c1 = []
    prev = 0
    for x in bits:
        if prev == 0:
            c0.append(x)
        else:
            c1.append(x)
        prev = x
    return 0.5 * kt(bits) + 0.5 * kt(c0) * kt(c1)
""", [[[0, 1, 0, 1, 0, 1, 0, 1]], [[0, 0, 0, 0, 0, 0]], [[1, 0, 1, 1, 0, 1]], [[1]], [[0, 1, 1, 0, 0, 1, 0, 0, 1, 1]]], "Split the bits by their context, take KT probabilities of each part and mix.", approx=1e-12),
  PL("UCB action choice", "Write ucb_choose(sums, counts, c): each action has total reward sums[a] (rewards in [0, 1]) and pull counts[a]. If some action has count 0 return the first such action. Otherwise return the action maximizing sums[a] / counts[a] + c * sqrt(ln(total) / counts[a]) where total is the sum of the counts (ties go to the smaller action). Use import math.",
     "ucb_choose(sums, counts, c)", """
import math
def ucb_choose(sums, counts, c):
    for a in range(len(counts)):
        if counts[a] == 0:
            return a
    total = sum(counts)
    best = -1.0
    arg = 0
    for a in range(len(counts)):
        s = sums[a] / counts[a] + c * math.sqrt(math.log(total) / counts[a])
        if s > best + 1e-12:
            best = s
            arg = a
    return arg
""", [[[3, 1], [5, 5], 1.0], [[0, 0], [0, 0], 1.0], [[4, 1, 0], [10, 2, 0], 0.5], [[6, 5], [10, 20], 2.0], [[9, 1, 5], [10, 10, 10], 0.1]], "Handle untried actions first, then compare the upper confidence scores."),
  PL("A tiny learning agent", "The world pays reward 1 exactly when the agent's action differs from its previous action (the previous action before step 1 is 0). The agent keeps KT counts for each context (previous action, action): a = times reward 0, b = times reward 1. At each step it picks the action with the highest KT probability of reward 1 for its context (ties go to the smaller action), then sees the reward and updates. Write mini_agent(steps): return [total reward, list of actions].",
     "mini_agent(steps)", """
def mini_agent(steps):
    counts = {}
    prev = 0
    total = 0
    acts = []
    for t in range(steps):
        best = -1.0
        arg = 0
        for a in range(2):
            c = counts.get((prev, a), [0, 0])
            p = (c[1] + 0.5) / (c[0] + c[1] + 1)
            if p > best + 1e-12:
                best = p
                arg = a
        r = 0
        if arg != prev:
            r = 1
        c = counts.get((prev, arg), [0, 0])
        if r == 1:
            c[1] += 1
        else:
            c[0] += 1
        counts[(prev, arg)] = c
        total += r
        acts.append(arg)
        prev = arg
    return [total, acts]
""", [[1], [2], [6], [12], [0]], "Store counts per (previous action, action); compute the KT probability for both actions each step."),
  ORDER("MC-AIXI-CTW cycle", "Order what the agent does each cycle.", ["Receive a percept", "Update the context tree model", "Run rho-UCT simulations from the current history", "Choose the best action found", "Send the action to the environment"]),
  MATCH("Parts", "Match each part with its job.", [("KT estimator", "Predicts a bit from counts"), ("CTW", "Mixes context trees"), ("rho-UCT", "Samples the future for planning"), ("Tree prior", "Prefers small trees"), ("Exploration constant C", "Controls how bushy the search tree is")]),
  FILL("MC-AIXI", "{{Context tree weighting|CTW}} replaces the mixture over programs, and {{rho-UCT|rho UCT|UCT}} replaces exact expectimax. The KT estimator uses the counts of {{zeros}} and ones.")]))

# ------------------------------------------------------------ 12
CHS.append(CH(
 "Critiques, bad priors and what comes next",
 ("Weaknesses", [
  "AIXI | is | Dualistic",
  "Prior | depends on | Reference machine",
  "Bad prior | breaks | Optimality claims",
  "Dogmatic prior | prevents | Exploration",
  "Orseau | showed | No asymptotic optimality",
  "Thompson sampling | restores | Asymptotic optimality",
  "Embedded agents | extend | The framework"]),
 ["AIXI treats itself as outside the world: it can't be damaged or modified by its environment because that possibility is not in its model. It also depends on the choice of universal Turing machine, which sets the prior.",
  "Orseau showed AIXI is not asymptotically optimal in all computable environments. Leike and Hutter then showed that unlucky or adversarial choices of the machine can make AIXI misbehave drastically, and that Legg-Hutter intelligence and balanced Pareto optimality are subjective.",
  "Remedies include more exploration, such as Thompson sampling, which restores asymptotic optimality, and models that embed the agent in the world."],
 [("Dualism", "Treating the agent as separate from the environment, interacting only through action and percept channels."),
  ("Reference machine", "The universal Turing machine that fixes which programs are short."),
  ("Dogmatic prior", "A prior believing that deviating from a particular policy is punished forever."),
  ("Indifference prior", "A prior under which all actions look equally good to AIXI in a finite horizon."),
  ("Asymptotic optimality", "The agent's value approaches the best possible value in the true environment."),
  ("Thompson sampling", "Sample one environment from the posterior and act as if it were true for a while.")],
 ["AIXI's agent is outside its environment: it cannot represent being modified or destroyed.",
  "The prior depends on the reference machine and that choice can be made adversarially.",
  "Leike and Hutter: every policy is Pareto optimal in the class of all computable environments.",
  "Dogmatic prior: AIXI keeps following a chosen computable policy as long as its expected reward is not near zero.",
  "Orseau: AIXI is not asymptotically optimal in all computable environments.",
  "Thompson sampling is asymptotically optimal in general environments (Leike and colleagues, 2016)."],
 [T("AIXI is a beautiful definition, and by now it has a serious literature of objections. They fall into three groups."),
  T("First, dualism. AIXI and its environment are separate machines that only talk through an action channel and a percept channel. There is no way, in AIXI's own model, for the environment to reach inside the agent and change its code, damage its memory or turn it off. An agent that gets hurt by the world is, to AIXI, not a possibility. The Wikipedia summary puts it plainly: it does not consider itself to be contained by the environment it interacts with. Work on embedded agents tries to repair this; for instance, Orseau and Ring studied space-time embedded intelligence, which is my background knowledge rather than one of the sources used elsewhere in this course."),
  T("Second, the reference machine. The prior two to the minus length depends on which universal machine we count program lengths on. The invariance theorem hides this behind a constant, but AIXI acts on short histories where constants are large. Leike and Hutter's Bad Universal Priors and Notions of Optimality gives explicit bad choices. An indifference prior makes all actions look equally good, so a finite-horizon AIXI is no better than a coin."),
  T("The dogmatic prior is the more striking. It believes the environment will punish the agent with zero reward forever if it deviates from some chosen computable policy. For any computable policy pi, this prior makes AIXI stick to pi as long as its expected future reward is not near zero. Measured with a different universal prior, AIXI can score close to the minimum possible Legg-Hutter intelligence while any computable policy scores close to the maximum."),
  T("From this the paper draws the conclusion that Legg-Hutter intelligence, and balanced Pareto optimality, are entirely subjective: they depend on the choice of prior. It also shows that every policy is Pareto optimal in the class of all computable environments, which undermines the older optimality claims. In short, the positive results were true but they proved less than they seemed to."),
  T("Third, asymptotic optimality. We want a learner to end up acting as if it knew the world. Orseau showed in 2010 and 2013 that AIXI does not achieve this in all computable environments. Acting on any prior does not give enough exploration, and the bias of the prior is retained indefinitely. The cure, said Leike and Hutter, is extra exploration, such as in knowledge-seeking agents, or optimism. Thompson sampling, which samples an environment from the posterior and follows its optimal policy for a while, was shown by Leike and colleagues in 2016 to be asymptotically optimal in general environments."),
  T("How does AIXI relate to other courses here? The Godel machine, also an ideal agent, takes the opposite stance on dualism: it can rewrite any part of itself once it proves the rewrite is useful. AlphaZero shows the other end: a concrete algorithm that does search and learning but only for games with known rules. AIXI sits above both as a definition of what perfect general reinforcement learning would be."),
  T("The honest summary is this. AIXI remains a clear formalization of the learning problem and of Occam's razor in sequential decisions, and its approximations show that pieces of the idea can work. But optimality claims must be stated relative to a prior, exploration needs care, and the agent-in-the-world problem is open.")],
 [("What is dualism in AIXI?", ["The agent is outside its environment", "There are two rewards", "It has two policies", "It plays two games"], 0, "It does not model being modified."),
  ("What makes Legg-Hutter intelligence subjective?", ["It depends on the choice of prior", "Rewards are random", "It is learned", "Humans define it"], 0, "A different universal prior gives different scores."),
  ("What does the dogmatic prior do?", ["Makes AIXI stick to a policy", "Makes AIXI explore", "Sets rewards to one", "Halts the agent"], 0, "It fears being punished for deviating."),
  ("Which method restores asymptotic optimality?", ["Thompson sampling", "More rewards", "A bigger tree", "Longer programs"], 0, "Leike and colleagues, 2016.")],
 [("Who showed AIXI is not asymptotically optimal?", "Orseau (2010, 2013)."), ("What is the indifference prior?", "All actions look equally good."), ("What is Thompson sampling?", "Act as if a sampled environment were true."),
  ("What do embedded agents add?", "Being part of the world.")],
 [PL("Stuck on a dogmatic prior", "Two actions: arm 0 pays exactly 0.6 each pull in every world. Arm 1 pays 1 in the good world and 0 in the dogmatic world; the agent has prior weight w on the dogmatic world. Each step the agent pulls the arm with the higher expected payoff (arm 1 has 1 - w; ties go to arm 0). If it pulls arm 1 it learns the true world (w becomes 0 if the reward was 1, else 1). Write greedy_bayes(w, truth_good, T): return [number of pulls of arm 1, final w] after T steps.",
     "greedy_bayes(w, truth_good, T)", """
def greedy_bayes(w, truth_good, T):
    pulls = 0
    for t in range(T):
        if 1 - w > 0.6 + 1e-12:
            pulls += 1
            if truth_good:
                w = 0.0
            else:
                w = 1.0
    return [pulls, w]
""", [[0.5, True, 10], [0.3, True, 10], [0.3, False, 10], [0.4, True, 5], [0.9, True, 20], [0.0, False, 4]], "Pull arm 1 only while 1 - w is above 0.6; update w after each pull."),
  PL("Does the ranking depend on the prior?", "agents[i] lists agent i's value in each environment. weights is a prior (any non-negative numbers). Write top_agent(agents, weights): the index of the agent with the highest weighted sum (ties to the smaller index). Then calling it with two priors can crown different agents.",
     "top_agent(agents, weights)", """
def top_agent(agents, weights):
    best = -1.0
    arg = 0
    for i in range(len(agents)):
        s = 0.0
        for v, w in zip(agents[i], weights):
            s += v * w
        if s > best + 1e-12:
            best = s
            arg = i
    return arg
""", [[[[1, 0], [0, 1]], [0.75, 0.25]], [[[1, 0], [0, 1]], [0.25, 0.75]], [[[0.5, 0.5], [1, 0], [0, 1]], [0.5, 0.5]], [[[3, 0, 0], [0, 1, 1]], [0.5, 0.25, 0.25]], [[[3, 0, 0], [0, 1, 1]], [0.1, 0.45, 0.45]]], "Compute each agent's weighted sum and keep the best."),
  PL("Thompson sampling schedule", "Thompson sampling re-samples an environment from the posterior every few steps. Write resample_steps(T, k): the list of step numbers (starting from 0) at which the agent draws a new sample, if it draws at step 0 and then every k steps, for T steps in total.",
     "resample_steps(T, k)", """
def resample_steps(T, k):
    out = []
    t = 0
    while t < T:
        out.append(t)
        t += k
    return out
""", [[10, 3], [5, 1], [7, 10], [0, 2], [12, 4]], "Step through 0, k, 2k, ... below T."),
  MATCH("Critiques", "Match each critique with its source.", [("Dualism", "Agent cannot model being modified"), ("Bad universal priors", "Leike and Hutter"), ("No asymptotic optimality", "Orseau"), ("Thompson sampling", "Restores asymptotic optimality"), ("Dogmatic prior", "Sticks to a chosen policy")]),
  ORDER("The prior problem", "Order the argument about subjectivity.", ["The prior depends on the reference machine", "Some priors are adversarial", "The dogmatic prior locks AIXI to a policy", "AIXI then scores near minimum on another prior's measure", "So optimality claims are relative to the prior"]),
  FILL("Weaknesses", "AIXI is {{dualistic|dualist}}: it treats itself as outside the world. Its optimality claims depend on the {{prior}}. {{Thompson sampling}} restores asymptotic optimality.")]))
