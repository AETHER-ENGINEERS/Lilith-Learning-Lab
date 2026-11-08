"""Gödel Machine course, chapters 1-6."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 1
CHS.append(CH(
 "What is a Gödel machine?",
 ("The big idea", [
  "Gödel machine | is | Self-improving program",
  "Gödel machine | rewrites | Its own code",
  "Rewrite | requires | Proof of improvement",
  "Jürgen Schmidhuber | proposed | Gödel machine in 2003",
  "Kurt Gödel | inspired | Self-referential formulas",
  "Gödel machine | belongs to | Meta-learning",
  "AIXI [ch10] | is compared with | Gödel machine"]),
 ["A Gödel machine is a hypothetical self-improving computer program that aims to solve problems optimally. It rewrites its own code, but only when it can prove that the new code gives a better strategy. Jürgen Schmidhuber proposed it in 2003, and it is named after Kurt Gödel, whose work inspired its mathematical foundations.",
  "It belongs to meta-learning, or learning to learn. The motivation is that an ordinary program has one hardwired algorithm and does not account for a changing environment, whereas a Gödel machine can change its own algorithm, including the part that does the changing.",
  "No full implementation has been created. The course treats it as a theory: you learn the machine step by step and build toy versions of its parts in Python."],
 [("Gödel machine", "A hypothetical self-improving program that rewrites any part of its own code once it has proved the rewrite is useful."),
  ("Self-improvement", "A change to the program's own code that raises its expected future success."),
  ("Self-referential", "Able to describe and reason about its own code, including the reasoning part."),
  ("Meta-learning", "Learning to learn: improving the learning procedure itself."),
  ("Provably optimal", "Justified by a formal proof within the machine's axiom system, not by testing."),
  ("Utility", "The quantity the machine tries to maximize, such as expected future reward.")],
 ["A Gödel machine rewrites its own code only after proving the rewrite helps.",
  "It was proposed by Jürgen Schmidhuber in 2003 and named after Kurt Gödel.",
  "It can rewrite any part of itself, including its proof searcher.",
  "It is a theoretical design; no full implementation exists.",
  "It is a form of meta-learning and is often compared with Hutter's AIXI."],
 [T("A Gödel machine is a hypothetical self-improving computer program that aims to solve problems in an optimal way. It rewrites its own code when it can prove that the new code provides a better strategy. It was invented by Jürgen Schmidhuber, first proposed in 2003, and is named after the logician Kurt Gödel, whose work inspired its mathematical foundations."),
  T("The idea sits within meta-learning, also called learning to learn. Proposed uses include automating human design decisions, transferring knowledge between related tasks, and designing more robust and general learning architectures. The Wikipedia article is explicit that this is theory: no full implementation has been created."),
  T("Why is the design needed? A traditional computer solves a problem with one input and one output, and its initial algorithm is hardwired. That ignores a dynamic natural environment, where inputs keep arriving and the best behaviour changes. The Gödel machine was meant to overcome that."),
  T("The machine's name and power come from using provably useful changes of any part of its own code, in a self-referential way. Schmidhuber's paper calls it a class of mathematically rigorous, general, fully self-referential, self-improving problem solvers. Those are the author's own claims; this course explains them and also covers the limits."),
  T("In outline, the machine starts with software that has three ingredients. An initial policy for dealing with the environment, which is allowed to be poor. A proof searcher, which hunts for formal proofs. And an axiomatic description of itself and its world: its hardware, its goal, what is known about the environment, and what actions and computation cost."),
  T("The searcher looks for a proof of one special statement, called the target theorem. It says: rewriting myself in this particular way will give a higher expected utility than not rewriting. If a proof is found, the machine executes the rewrite. The rewrite may change any part of the software, even the proof searcher itself."),
  T("The paper then argues that such a rewrite is globally optimal, not just locally. By then the machine has also had to prove that continuing to search for better rewrites is not worth waiting for. Chapter 7 covers this carefully."),
  T("Here is the machine's main loop, in words. Run the current policy and keep collecting reward. Meanwhile the proof searcher runs. When it proves a target theorem, switch to the proposed new code. Then carry on, with the new code now doing both the acting and the searching."),
  T("The route through the course follows the paper. Chapters 2 to 4 give the background and the machine model: Gödel's ideas, the state and the utility, and the axioms. Chapters 5 to 8 give the proof searcher, the target theorem, the optimality theorem and bias-optimal proof search. The last chapters cover examples, related work, limits and a toy machine you build yourself."),
  T("A note on sources. They are the Wikipedia article on the Gödel machine, Schmidhuber's technical report on arXiv, the paper by Steunebrink and Schmidhuber on implementations, and the work of Yudkowsky and Herreshoff on the Löbian obstacle.")],
 [("What triggers a Gödel machine to rewrite its code?", ["A timer", "A proof that the rewrite gives higher utility", "A user request", "A random choice"], 1, "The rewrite happens only after a proof."),
  ("Who proposed the Gödel machine?", ["Kurt Gödel", "Alan Turing", "Jürgen Schmidhuber", "Marcus Hutter"], 2, "He first proposed it in 2003."),
  ("What is the state of implementation according to Wikipedia?", ["Widely deployed", "No full implementation has been created", "Used in all phones", "Only in games"], 1, "It remains largely theoretical."),
  ("Which part of its software may a Gödel machine rewrite?", ["Only the policy", "Only the axioms", "Any part, including the proof searcher", "Nothing"], 2, "It is fully self-referential.")],
 [("When was the Gödel machine first proposed?", "2003, by Jürgen Schmidhuber."), ("What field is it part of?", "Meta-learning."), ("What is the target theorem for?", "To justify a self-rewrite."),
  ("Why 'Gödel'?", "Gödel's self-referential formulas inspired the construction.")],
 [ORDER("The main loop", "Put the steps of the machine's cycle in order.", ["Run the current policy and collect reward", "Search for a proof of the target theorem", "Find a proof that switching beats continuing", "Execute the switchprog (the rewrite)", "Continue with the rewritten code"]),
  MATCH("Key terms", "Match each term with its meaning.", [("Policy", "How the machine acts in its environment"), ("Proof searcher", "The part that hunts for formal proofs"), ("Target theorem", "The claim that a rewrite raises utility"), ("Utility", "The quantity to maximize"), ("Meta-learning", "Learning to learn")]),
  FILL("Basics", "A Gödel machine rewrites its code only after a {{proof|proving}} that the change helps. It was proposed by Jürgen {{Schmidhuber}} in {{2003}}.")]))

# ------------------------------------------------------------ 2
CHS.append(CH(
 "Gödel's ideas and the limits of proof",
 ("Gödel and limits", [
  "Gödel 1931 | showed | Incompleteness",
  "Formal system | can encode | Statements about itself",
  "Gödel numbering | maps | Formulas to numbers",
  "Gödel sentence | says | I am not provable",
  "Consistent system | cannot prove | Its own consistency",
  "Rice's theorem | limits | Deciding program properties",
  "Gödel machine [ch1] | inherits | These limits"]),
 ["Gödel showed in 1931 that any consistent formal system strong enough to express arithmetic contains true statements it cannot prove. His proof encodes formulas as numbers, which lets a system talk about its own proofs and build a sentence that says it is not provable.",
  "Related limits: a consistent system cannot prove its own consistency, and Rice's theorem says every non-trivial question about what a program computes is undecidable in general.",
  "A Gödel machine reasons inside a formal system, so it inherits these limits. The paper accepts this: the machine ignores self-improvements whose usefulness it cannot prove."],
 [("Formal system", "A set of axioms and inference rules from which theorems are derived."),
  ("Consistent", "Not able to prove both a statement and its negation."),
  ("Incompleteness", "A consistent system covering arithmetic has true statements it cannot prove."),
  ("Gödel numbering", "Assigning each formula a unique natural number so statements can be about statements."),
  ("Gödel sentence", "A statement that asserts its own unprovability."),
  ("Rice's theorem", "Every non-trivial semantic property of programs is undecidable.")],
 ["Gödel's incompleteness theorem: powerful consistent systems have unprovable truths.",
  "Gödel numbering lets a system reason about its own formulas.",
  "The Gödel machine uses self-reference, so it is bound by the same limits.",
  "Rice's theorem: no general procedure decides non-trivial program properties.",
  "The machine simply ignores improvements it cannot prove."],
 [T("The machine is named for Kurt Gödel because of how he turned logic on itself. In 1931 he introduced a way to encode formulas and proofs as natural numbers, now called Gödel numbering. Once formulas are numbers, a statement about numbers can be a statement about formulas, so a system can talk about its own proofs."),
  T("With that, he built a sentence that says, in effect, I am not provable in this system. If the system is consistent, it cannot prove this sentence, yet the sentence is true. That is the first incompleteness theorem: any formal system that encompasses arithmetic is either flawed, meaning inconsistent, or contains statements that it cannot prove."),
  T("Schmidhuber describes Gödel as the founder of theoretical computer science, because he introduced a universal coding language based on integers. The Gödel machine reuses that trick in a practical direction: its software and its proofs are strings, and the axioms include a description of its own code."),
  M(r"\text{Gödel number of } s_1 s_2 \dots s_n \;=\; 2^{c(s_1)} \cdot 3^{c(s_2)} \cdots p_n^{\,c(s_n)}"),
  T("Here is a simple version of numbering, with my own symbol codes. Give each symbol a positive code c. Then raise the first prime, 2, to the code of the first symbol, the second prime, 3, to the code of the second symbol, and so on, and multiply. Unique factorization into primes means the number can be decoded back into the symbols."),
  T("A second famous limit: a consistent system cannot prove its own consistency. Later chapters connect this to Löb's theorem and to a problem that arises when an agent must trust its own proofs."),
  T("A third limit comes from computability. Rice's theorem says that any non-trivial property of what a program computes is undecidable in general. So no algorithm can decide, for every program, whether it is better than another. A system that must prove such properties will be able to prove only some of them."),
  T("What does this mean for a Gödel machine? The wiki article states it directly: even a Gödel machine with unlimited computational resources must ignore those self-improvements whose effectiveness it cannot prove. The paper adds a point about resources: a machine with limited time and space cannot profit from improvements it cannot prove within its limits."),
  T("The paper also notes that the machine does not exceed ordinary computers in power. In an interview Schmidhuber says it is not computationally more powerful than a Turing machine. Its claim is about efficiency: it can exploit any provably useful speed-up of any part of its software."),
  T("The practice section has a numbering lab: you encode a symbol list as a Gödel number and decode it back. Keep to short lists, since the numbers grow very fast.")],
 [("What did Gödel's first incompleteness theorem show?", ["Every statement can be proved", "A consistent system covering arithmetic has true unprovable statements", "Computers are impossible", "Primes are infinite"], 1, "Powerful consistent systems are incomplete."),
  ("What does Gödel numbering do?", ["Assigns each formula a number so systems can refer to their own formulas", "Counts proofs", "Sorts axioms", "Encrypts data"], 0, "It makes self-reference possible."),
  ("What must a Gödel machine do with improvements it cannot prove?", ["Apply them anyway", "Ignore them", "Delete the machine", "Ask a human"], 1, "Provability is the gate."),
  ("Is a Gödel machine more powerful than a Turing machine?", ["Yes, it solves undecidable problems", "No, the claim is about efficiency", "Only with quantum hardware", "Only with a large memory"], 1, "It cannot overcome the limits of computability.")],
 [("Who introduced Gödel numbering?", "Kurt Gödel, in 1931."), ("What does Rice's theorem say?", "Non-trivial program properties are undecidable in general."),
  ("Gödel sentence?", "A statement that says it cannot be proved."), ("Can a consistent system prove its own consistency?", "No.")],
 [MATCH("Limits", "Match each result with its message.", [("Incompleteness", "True statements can be unprovable"), ("Gödel numbering", "Formulas coded as numbers"), ("Rice's theorem", "Program properties are undecidable in general"), ("Consistency", "No statement and its negation are both provable")]),
  PL("Gödel numbering", "Give each symbol a positive integer code. Write godel_number(codes): the product of the n-th prime raised to the n-th code (primes 2, 3, 5, 7, 11, ...). The empty list gives 1. Keep inputs short: the numbers get large quickly.",
     "godel_number(codes)", """
def godel_number(codes):
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    n = 1
    for i in range(len(codes)):
        n = n * primes[i] ** codes[i]
    return n
""", [[[1, 2, 3]], [[4]], [[]], [[2, 1, 1, 2]], [[3, 3, 3, 3, 3]]], "Take primes in order and multiply prime ** code."),
  PL("Decode a Gödel number", "Write decode_godel(n): the inverse of the numbering. Divide n by 2 as many times as possible and count, then by 3, and so on, until n is 1. Return the list of exponents. Assume every code is at least 1, so there are no gaps.",
     "decode_godel(n)", """
def decode_godel(n):
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    out = []
    i = 0
    while n > 1:
        count = 0
        while n % primes[i] == 0:
            n = n // primes[i]
            count += 1
        out.append(count)
        i += 1
    return out
""", [[108], [16], [1], [9072000], [2310 ** 2]], "Loop over primes. For each prime count how many times it divides n."),
  FILL("Limits", "Gödel's first theorem says a consistent system covering arithmetic is {{incomplete}}. Gödel {{numbering}} codes formulas as numbers. A Gödel machine must {{ignore|skip}} improvements it cannot prove.")]))

# ------------------------------------------------------------ 3
CHS.append(CH(
 "The machine model and utility",
 ("State, inputs and utility", [
  "Hardware | runs in | Discrete cycles",
  "State s(t) | is changed by | Transition function F",
  "Variable time | holds | Binary encoding of t",
  "Variable x | holds | Environment input",
  "Variable y | holds | Machine output",
  "Software p | contains | Policy and proof searcher",
  "Utility u | is | Expected future reward",
  "Environment | is drawn from | Set of distributions"]),
 ["The machine's hardware has a single life made of discrete cycles t = 1, 2, ..., T. The state s(t) changes by a hardwired transition function that depends on the previous state and the environment.",
  "Four variables matter: time holds the binary encoding of t; x holds the environment's input; y holds the machine's output; and p is the software, which at the start contains an initial policy and an initial proof searcher.",
  "The goal is to maximize expected utility: the conditional expectation of the sum of future rewards from now until the end of life, under an unknown environment distribution drawn from a set of possible ones."],
 [("Cycle", "One discrete time step of the machine's single life."),
  ("State", "Everything stored in the machine at time t: memory, registers, variables."),
  ("Transition function", "The hardwired rule that maps the previous state and the environment's reaction to the next state."),
  ("Policy", "The part of the software that decides how to interact with the environment."),
  ("Reward", "A real number the machine receives at a time step, encoded in its state."),
  ("Utility", "The expected sum of rewards from the current time to the end of life."),
  ("Environment distribution", "An unknown probability law over the environment's behaviour, drawn from a set M.")],
 ["The machine lives for T cycles; T may or may not be known.",
  "s(t) = F(s(t-1), Env(t-1)).",
  "time, x, y and p are the main variables.",
  "u(s, Env) is the expected sum of future rewards given the current state.",
  "Variants: worst-case performance, or reward per time interval.",
  "Utility is defined in terms of the current state, so it changes if the machine rewrites u."],
 [T("To define the machine precisely, Schmidhuber's report starts with the hardware. It has a single life, which consists of discrete cycles or time steps t = 1, 2, and so on up to T. The final time T may or may not be known in advance."),
  T("The hardware can be a universal Turing machine, a space-bounded Turing machine or the abstract model of a personal computer. At any moment it has a state s(t), a finite binary string. The state changes by a hardwired state transition function F, which takes the previous state and the environment's reaction and returns the new state."),
  M(r"s(t) = F\big(s(t-1),\, \mathrm{Env}(t-1)\big) \quad (t > 1)"),
  T("Four variables are stored in the state. Time holds a binary encoding of the current step, starting from 1 and increasing every cycle. The variable x holds input from the environment; it changes only when a program executes an instruction that requests input. The variable y holds the outputs; its default value at the start is zero. And p is the software, which includes an initial policy for interacting with the environment, plus an initial proof searcher."),
  T("The goal. At every time the machine tries to maximize its expected future success. The paper formalizes this as the utility u of the current state and environment: the conditional expectation of the sum of all rewards from the present time up to the end of life."),
  M(r"u(s, \mathrm{Env}) \;=\; E_{\mu}\!\left[\, \sum_{\tau = \mathrm{time}}^{T} r(\tau) \;\Big|\; s,\ \mathrm{Env} \right]"),
  T("In this formula r of tau is the real-valued reward encoded in the state at step tau. The expectation uses a distribution mu, which is unknown. It is drawn from a set M of distributions that could describe the environment. The variable time is the current time, taken from the state s."),
  T("This formulation allows alternatives. A designer could use worst-case performance over M instead of the expectation, or reward per time interval. The Wikipedia article adds that the utility accounts for the possibility of extending the machine's expected lifespan."),
  T("An important consequence: since the utility function is stored in the machine's state, the machine can reason about it, and may in principle change it. But a change of the utility function is allowed only if the new one is provably better according to the present utility function. This is the reply to the worry that the machine might adopt a bogus goal."),
  T("The practice section computes expected utility over a few environment distributions and the cumulative reward between two times.")],
 [("What does the variable x hold?", ["The machine's output", "Input from the environment", "The utility", "The proof"], 1, "y holds outputs."),
  ("What is utility in the paper?", ["Expected sum of future rewards", "Memory used", "Number of proofs", "Clock speed"], 0, "From the current time to the end of life."),
  ("What is mu in the utility formula?", ["The reward", "An unknown environment distribution from a set M", "The proof length", "A prime"], 1, "The expectation is taken under mu."),
  ("May the machine change its own utility function?", ["Never", "Only if the change is provably better under the present utility", "Whenever it likes", "Only at time one"], 1, "That blocks bogus goals.")],
 [("What is T?", "The final time step of the machine's life."), ("What is r(t)?", "The reward at step t."), ("Which variable holds p?", "p is the software, with the policy and proof searcher."),
  ("Alternatives to expectation?", "Worst-case performance or reward per interval.")],
 [MATCH("Variables", "Match each variable with what it holds.", [("time", "Binary encoding of the current step"), ("x", "Input from the environment"), ("y", "Output to the environment"), ("p", "The software: policy and proof searcher"), ("s", "The whole machine state")]),
  PL("Expected utility", "The environment is one of several possibilities, each [probability, rewards] where rewards[0] is the reward at step 1. Write expected_utility(envs, t): the expected sum of rewards from step t (1-based) to the end, averaged using the probabilities.",
     "expected_utility(envs, t)", """
def expected_utility(envs, t):
    total = 0
    for p, rewards in envs:
        total += p * sum(rewards[t - 1:])
    return total
""", [[[[0.5, [1, 1, 1, 1]], [0.5, [0, 2, 2, 0]]], 1], [[[0.5, [1, 1, 1, 1]], [0.5, [0, 2, 2, 0]]], 3], [[[1.0, [5, 5]]], 3]], "Slice the reward list from index t-1 and sum it, weight by the probability."),
  PL("Reward between two times", "The paper's axioms use R(t1, t2): the cumulative reward between times t1 and t2. Write reward_between(rewards, t1, t2) for a list of per-step rewards (step 1 is index 0), including both t1 and t2. Return 0 if t1 is greater than t2.",
     "reward_between(rewards, t1, t2)", """
def reward_between(rewards, t1, t2):
    if t1 > t2:
        return 0
    return sum(rewards[t1 - 1:t2])
""", [[[3, 1, 4, 1, 5], 2, 4], [[3, 1, 4, 1, 5], 1, 5], [[3, 1, 4], 3, 2]], "Both ends are included, so slice from t1-1 to t2."),
  FILL("Model", "The state changes by a hardwired {{transition}} function. The goal is expected future {{reward}}. The environment is drawn from a set of {{distributions}}.")]))

# ------------------------------------------------------------ 4
CHS.append(CH(
 "The axioms",
 ("The initial axiom system", [
  "Axiom system | is stored in | Initial software p(1)",
  "Hardware axioms | describe | State changes",
  "Reward axioms | describe | Costs and lifetime",
  "Environment axioms | restrict | Future inputs",
  "Uncertainty axioms | give | Probability and arithmetic",
  "Initial state axioms | describe | Contents of s(1)",
  "Utility axioms | define | Goal u"]),
 ["The machine's initial software includes an axiomatic description of itself and its world. The proof searcher derives theorems from these axioms by inference rules.",
  "The axiom groups are hardware axioms, reward axioms, environment axioms, uncertainty and string-manipulation axioms, initial-state axioms and utility axioms. Together they let the machine prove statements about its own future states and rewards.",
  "Because the axiom system is part of the software, it can itself be rewritten, but only by a proven-useful rewrite. Optimality claims hold relative to a consistent axiom system."],
 [("Axiom", "A statement accepted without proof, from which theorems are derived."),
  ("Hardware axioms", "Describe how the state can change from one cycle to the next."),
  ("Reward axioms", "Describe the costs of instructions and outputs, rewards in the input, and the lifetime."),
  ("Environment axioms", "Restrict how new inputs are produced from earlier inputs and outputs."),
  ("Uncertainty axioms", "Standard arithmetic, calculus and probability theory, plus string manipulation."),
  ("Initial state axioms", "Statements about the contents of the state at time 1."),
  ("Utility axioms", "The definition of the utility function u.")],
 ["Six axiom groups: hardware, reward, environment, uncertainty, initial state, utility.",
  "The axioms are part of the software and can be improved by proven rewrites.",
  "The environment axioms can be as weak as 'any computable distribution' or as strong as 'deterministic'.",
  "Optimality holds if the axiom system is consistent.",
  "Standard mathematics lets the machine reason about expected rewards."],
 [T("The machine's initial software p(1) carries an axiomatic system A. The proof searcher derives theorems from A with a few inference rules, and a theorem of the right form triggers a rewrite. The paper lists what A contains."),
  T("Hardware axioms describe how the state can change from one cycle to the next. For a Turing machine they cover the tape contents, the head positions and the internal state. For a microprocessor they cover registers and instruction pointers. With these the machine can derive what its hardware will do if it runs a given program."),
  T("Reward axioms describe the costs of hardware instructions and the physical costs of output actions. They also describe reward events arriving in the input, and the total lifetime as a scalar. A typical derived quantity is R of t1 and t2, the cumulative reward between two times."),
  T("Environment axioms restrict how new inputs are produced, given earlier inputs and outputs. They can be very weak, for example saying the true distribution is any computable one, or the Speed Prior. They can be strong, for example a Markovian interface or a fully predictable environment."),
  T("Uncertainty axioms and string-manipulation axioms are the standard axioms of arithmetic, calculus, probability theory, statistics and string manipulation. They allow proofs about future values of variables, expected rewards and remaining lifetime. This is why the framework can handle uncertainty with ordinary formal mathematics."),
  T("Initial-state axioms are statements about the contents of the state at time 1, for instance that a particular substring of the state equals a particular string. They let the machine reconstruct its own initial code, which is needed to talk about itself."),
  T("Utility axioms define the goal: the utility function u, for example the expected sum of future rewards. Because the utility is an axiom, a target theorem can compare utilities of different futures."),
  T("Now two cautions. First, consistency. The optimality theorem in chapter 7 assumes the axiom system is consistent. If it were inconsistent, it could prove anything, including target theorems for harmful rewrites. Second, the system is not fixed: since the axioms are part of the software, a proven rewrite may add theorems derived from the axioms, or replace axioms, as the paper lists among possible self-improvements."),
  T("The practice section lets you classify statements by axiom group and use the standard result that makes hardware axioms useful: simulate a tiny machine's state transitions.")],
 [("Which axioms define the goal?", ["Hardware axioms", "Utility axioms", "Environment axioms", "Initial state axioms"], 1, "They define u."),
  ("Which axioms say how registers and the instruction pointer change?", ["Reward axioms", "Hardware axioms", "Uncertainty axioms", "None"], 1, "They describe transitions between cycles."),
  ("What do uncertainty axioms contain?", ["Standard arithmetic, probability and string manipulation", "The user's wishes", "Proof searcher code", "Nothing"], 0, "They support proofs about expected rewards."),
  ("What does the optimality theorem assume about the axioms?", ["They are consistent", "They are short", "They are random", "They are secret"], 0, "Inconsistent axioms prove anything.")],
 [("How many axiom groups?", "Six."), ("Strong vs weak environment axioms?", "Weak: any computable distribution. Strong: deterministic."), ("Why initial-state axioms?", "To let the machine reconstruct its own initial state and code."),
  ("What if the axioms are inconsistent?", "They prove everything, so the guarantees fail.")],
 [MATCH("Axiom groups", "Match each group with what it describes.", [("Hardware axioms", "How the state changes each cycle"), ("Reward axioms", "Costs, rewards and lifetime"), ("Environment axioms", "How inputs depend on earlier inputs and outputs"), ("Uncertainty axioms", "Arithmetic, probability, strings"), ("Utility axioms", "The definition of u")]),
  PL("Which axiom group?", "Write axiom_group(statement). Return \"hardware\" if the statement mentions \"register\" or \"instruction pointer\"; \"reward\" if it mentions \"cost\" or \"lifetime\"; \"environment\" if it mentions \"input\"; \"utility\" if it mentions \"utility\"; otherwise \"other\". Check them in that order.",
     "axiom_group(statement)", """
def axiom_group(statement):
    s = statement.lower()
    if 'register' in s or 'instruction pointer' in s:
        return 'hardware'
    if 'cost' in s or 'lifetime' in s:
        return 'reward'
    if 'input' in s:
        return 'environment'
    if 'utility' in s:
        return 'utility'
    return 'other'
""", [["The instruction pointer advances by 1"], ["Each output has a cost of 3 units"], ["The next input depends on the last output"], ["Utility is the sum of future rewards"], ["2 + 2 = 4"]], "Lower-case the text, then test the keywords in the given order."),
  PL("Hardware axiom in action", "A tiny machine has one register r and instructions \"INC\", \"DEC\" and \"DBL\" (double). Write run_hw(r, program): the hardware axioms say each instruction changes r by one rule; return the register after the whole program. An unknown instruction leaves r unchanged.",
     "run_hw(r, program)", """
def run_hw(r, program):
    for ins in program:
        if ins == 'INC':
            r += 1
        elif ins == 'DEC':
            r -= 1
        elif ins == 'DBL':
            r *= 2
    return r
""", [[3, ["INC", "DBL", "DEC"]], [0, []], [5, ["DBL", "DBL", "NOP"]]], "Apply the rule for each instruction in order."),
  FILL("Axioms", "{{Hardware}} axioms describe state changes. {{Utility}} axioms define the goal. The optimality theorem assumes the axioms are {{consistent}}.")]))

# ------------------------------------------------------------ 5
CHS.append(CH(
 "The proof searcher",
 ("Searching for proofs", [
  "Proof searcher | searches | Proof techniques",
  "Proof technique | is | Program that outputs proofs",
  "Proof-modifying instructions | number | Six",
  "get-axiom | appends | An axiom",
  "apply-rule | derives | New theorem",
  "Only valid proofs | can be built | Verification is trivial",
  "Proof | is stored in | Variable proof"]),
 ["The proof searcher does not enumerate proofs by brute force, which would take time exponential in the proof size. It tests proof techniques: programs, written in a universal language, whose output is a proof.",
  "A proof technique can modify the proof only through six instructions: get-axiom, apply-rule, delete-theorem, set-switchprog, check and state2theorem. Since there is no other way to change the proof, an incorrect theorem can never be inserted, which makes verifying a proof trivial.",
  "A proof is a list of theorems. Each theorem is either an axiom or follows from earlier theorems by an inference rule, such as modus ponens."],
 [("Proof technique", "A program, in a universal language, that outputs a proof by calling the proof-modifying instructions."),
  ("get-axiom", "Appends the n-th axiom of the axiom scheme to the proof."),
  ("apply-rule", "Applies the k-th inference rule to the m-th and n-th theorems and appends the result."),
  ("delete-theorem", "Removes a theorem to free storage; it can no longer be used."),
  ("set-switchprog", "Sets the candidate rewrite to a substring of the proof technique's scratch memory."),
  ("check", "Tests whether the last theorem is a target theorem and, if so, arranges the switch."),
  ("state2theorem", "Turns a currently observable part of the state into a time-stamped theorem.")],
 ["Proofs are built only by six instructions, so a wrong theorem cannot appear.",
  "Verification is therefore trivial.",
  "Proof techniques are programs that produce proofs; they are faster than brute-force enumeration.",
  "delete-theorem saves space but deleted theorems cannot be reused.",
  "state2theorem lets the machine use observations about its own current state.",
  "check ends the search when the last theorem is a target theorem."],
 [T("The proof searcher is the part of the initial software that hunts for a proof of the target theorem. The simplest way to search for proofs is brute force: enumerate all proofs in order of size. That takes exponential time in the proof size, so it is hopeless for anything but tiny proofs."),
  T("The paper instead lets the searcher test proof techniques. A proof technique is a program, written in a universal language such as a variant of PROLOG or a FORTH-like language, whose output is a proof. Techniques can read parts of the machine's state, including the input x and the code of the initial software, and they write temporary results to a scratch area. Their output goes into a string variable called proof."),
  T("A proof technique may change the proof only through six instructions. Because these are the only ways to modify the proof, it is impossible to insert an incorrect theorem, so checking that a proof is valid is trivial. The six are as follows."),
  T("One, get-axiom with an index n: it appends the n-th axiom from the axiom scheme to the proof. Two, apply-rule with k, m and n: it applies the k-th inference rule, for example modus ponens, to the m-th and n-th theorems, and appends the result. If the rule does not apply, the current proof technique is interrupted."),
  T("Three, delete-theorem with m: it removes the m-th theorem, which frees storage; deleted theorems can no longer be used. Four, set-switchprog with m and n: it sets the candidate rewrite, the switchprog, to the substring of the scratch area from m to n, provided that substring is not empty."),
  T("Five, check: it tests whether the last theorem is a target theorem. If it is, and there is still enough time to set the switch bit before the deadline, it sets the bit, waits, and transfers control to the switchprog. Six, state2theorem with m and n: it converts the currently observable contents of part of the state into a time-stamped theorem. Observed facts need no proof, because the observation has already happened."),
  T("Let us see a tiny version. Suppose the axioms are p, p implies q, and q implies r. A proof technique runs: get-axiom 1, get-axiom 2, apply modus ponens to theorems 1 and 2, which gives q. Then get-axiom 3 and apply modus ponens again to get r. Every line is either an axiom or a valid consequence, so the final proof is correct by construction."),
  T("The searcher is an online variant of universal search. It tests techniques one after another, giving each a budget of steps, and undoes their effects on the scratch area between tests. Chapter 8 covers the exact scheme and why it is asymptotically optimal."),
  T("In the practice section you implement the proof builder with get-axiom, modus ponens and delete-theorem, and see that an invalid step is rejected, so no wrong theorem ever enters.")],
 [("Why is proof verification trivial in this design?", ["Proofs are short", "Only six instructions can modify the proof, and each yields a valid theorem", "A human checks them", "Proofs are random"], 1, "No instruction can insert an incorrect theorem."),
  ("What is a proof technique?", ["A theorem", "A program that outputs proofs", "An axiom", "A rewrite"], 1, "The searcher tests such programs."),
  ("What does apply-rule do?", ["Deletes an axiom", "Applies an inference rule to two earlier theorems", "Changes the hardware", "Prints the proof"], 1, "For example modus ponens."),
  ("What does state2theorem allow?", ["Using an observed part of the state as a time-stamped theorem", "Deleting the state", "Changing the utility", "Running faster"], 0, "Observations need no proof.")],
 [("How many proof-modifying instructions?", "Six."), ("Which instruction ends the search?", "check, when it sees a target theorem."), ("Why not brute force?", "It is exponential in proof size."),
  ("What does delete-theorem save?", "Storage.")],
 [MATCH("Instructions", "Match each instruction to its job.", [("get-axiom", "Append an axiom to the proof"), ("apply-rule", "Derive a new theorem from two earlier ones"), ("delete-theorem", "Free the space of a theorem"), ("set-switchprog", "Choose the candidate rewrite"), ("check", "See whether the last theorem is the target theorem"), ("state2theorem", "Turn an observed part of the state into a theorem")]),
  PL("A tiny proof builder", "Theorems are strings: an atom like \"p\" or an implication \"p->q\" between atoms. Write run_proof(axioms, steps). Each step is a string: \"axiom n\" appends axioms[n-1]; \"mp m n\" applies modus ponens to theorem m (a statement X) and theorem n (the statement X->Y) and appends Y; \"delete m\" removes theorem m. Indices are 1-based into the current list of theorems. Return the final list of theorems. If a step is not valid (bad index, or modus ponens does not apply), return \"error at \" and the 1-based step number, and add nothing.",
     "run_proof(axioms, steps)", """
def run_proof(axioms, steps):
    thms = []
    for k in range(len(steps)):
        parts = steps[k].split()
        err = 'error at ' + str(k + 1)
        cmd = parts[0]
        if cmd == 'axiom':
            n = int(parts[1])
            if n < 1 or n > len(axioms):
                return err
            thms.append(axioms[n - 1])
        elif cmd == 'mp':
            m = int(parts[1])
            n = int(parts[2])
            if m < 1 or n < 1 or m > len(thms) or n > len(thms):
                return err
            x = thms[m - 1]
            imp = thms[n - 1]
            if '->' not in imp:
                return err
            a, b = imp.split('->')
            if a != x:
                return err
            thms.append(b)
        elif cmd == 'delete':
            m = int(parts[1])
            if m < 1 or m > len(thms):
                return err
            thms.pop(m - 1)
        else:
            return err
    return thms
""", [[["p", "p->q", "q->r"], ["axiom 1", "axiom 2", "mp 1 2"]], [["p", "p->q", "q->r"], ["axiom 1", "axiom 2", "mp 1 2", "axiom 3", "mp 3 4", "delete 2"]], [["p", "p->q"], ["axiom 1", "mp 1 1"]], [["p"], ["axiom 5"]], [["p", "q->r"], ["axiom 1", "axiom 2", "mp 1 2"]]],
     "Keep a list of theorems. Check indices before using them. For mp, split the implication at '->' and compare its left side with theorem m."),
  PL("Can the target be proved in budget?", "A proof technique is given by the number of steps it needs. The searcher gives each technique in turn a budget. Write first_success(costs, budget): the 0-based index of the first technique whose cost is at most the budget, or -1 if there is none.",
     "first_success(costs, budget)", """
def first_success(costs, budget):
    for i in range(len(costs)):
        if costs[i] <= budget:
            return i
    return -1
""", [[[50, 20, 10], 15], [[50, 20], 10], [[], 5]], "Scan in order and return the first index that fits."),
  FILL("Proof searcher", "A proof {{technique}} is a program that outputs proofs. There are {{six|6}} proof-modifying instructions. Because they only build valid proofs, {{verification}} is trivial.")]))

# ------------------------------------------------------------ 6
CHS.append(CH(
 "The target theorem and the switch",
 ("Target theorem", [
  "Switchprog | is | Candidate rewrite",
  "Switchbit | decides | Whether to switch",
  "Target theorem | compares | Utility with and without switching",
  "check | executes | Switch if target theorem proved",
  "t1 | is | Time of the switch",
  "Rewrite | may change | Any part of p, including the proof searcher",
  "Switching | is delayed by | Proof finding time"]),
 ["A switchprog is a candidate program that can rewrite any part of the machine's software. The machine runs it only if it has proved a target theorem: the utility with the switch bit set to 1 is higher than with the bit set to 0.",
  "Setting the bit to 0 means continuing as before, with the searcher still looking for other rewrites. Setting it to 1 means running the switchprog at time t1. The time t1 accounts for the delay between finding the proof and acting on it.",
  "A relaxed version replaces the strict inequality with at least as high, so the machine rewrites itself as soon as the change is provably not harmful."],
 [("Switchprog", "The proposed rewrite: a program that may change any part of the software."),
  ("Switchbit", "A bit that is 0 for continue as before and 1 for run the switchprog."),
  ("Target theorem", "The statement that utility with switchbit = 1 exceeds utility with switchbit = 0."),
  ("t1", "The time step at which the switch would occur, after the proof is found."),
  ("Relaxed target theorem", "The version with at-least-as-high instead of strictly higher.")],
 ["Target theorem: u(switch) > u(continue), at time t1.",
  "The switch is executed only after the proof.",
  "The comparison need not compute exact utilities, only which is higher.",
  "A relaxed version uses at-least-as-high.",
  "The switchprog can rewrite anything, even the axioms and the proof searcher."],
 [T("When a proof technique calls set-switchprog, it names a substring of its scratch area as the candidate rewrite. That candidate is the switchprog. It is a program that, when run, may rewrite any part of the machine's software p, including the axioms, the policy and the proof searcher itself."),
  T("The machine will run the switchprog only if it has proved that doing so is better than not doing so. The statement to prove is called the target theorem. To state it, the machine uses a switch bit. When the bit is 0, the machine continues as before. When it is 1, the machine runs the switchprog at a time t1."),
  M(r"u\big[\, s(t_1) \oplus (\mathrm{switchbit}(t_1) = 1),\ \mathrm{Env}(t_1) \big] \;>\; u\big[\, s(t_1) \oplus (\mathrm{switchbit}(t_1) = 0),\ \mathrm{Env}(t_1) \big]"),
  T("Read this as: the utility of the world in which the switch bit is one is higher than the utility of the world in which it is zero. The symbol with the circled plus means replace the switch bit value in the state. The time t1 handles the delay between finding a proof and acting on it."),
  T("The check instruction, from the previous chapter, does the rest. It looks at the last theorem. If that is a target theorem, it checks that there is still time to set the bit before t1. If so it sets the bit, waits until t1 passes, and transfers control to the switchprog."),
  T("Importantly, the continue-as-before option is not the same as doing nothing. Continuing as before means the proof searcher keeps looking for other rewrites. So the target theorem effectively says that the switchprog is better than waiting for any later rewrite the searcher might find. Chapter 7 uses exactly this point to explain global optimality."),
  T("The proof does not need exact numbers. The paper stresses that the machine only has to show which of the two utilities is higher, not to compute them. For example, a factor-2 speed-up of a proof-searcher subroutine can be shown worthwhile without knowing the exact utility."),
  T("The relaxed version. Replace the strict greater-than with at-least-as-high. Then the machine rewrites itself as soon as it can prove the change will not make things worse, and the optimality theorem holds with the weaker inequality."),
  T("Here is a worked example with numbers. The current policy earns 10 reward per step, and 100 steps remain. A switchprog gives 12 per step but needs 5 steps to run, during which nothing is earned. Continuing earns 1000. Switching earns 12 times 95, which is 1140. So the target theorem is true. If instead the switch took 20 steps, switching would earn 12 times 80, which is 960, so it is false."),
  T("In the practice section you check target theorems for numbers like these, order the steps of a switch, and use the Switch Explorer app.")],
 [("What does switchbit = 0 mean?", ["Run the switchprog", "Continue as before, with the searcher still running", "Halt", "Reset the clock"], 1, "It is the continue option."),
  ("Why is the target theorem comparing with 'continue as before' and not 'do nothing'?", ["It is a typo", "Continuing includes future search for better rewrites", "Doing nothing is illegal", "It is faster"], 1, "That is what makes the choice non-greedy."),
  ("Does the machine need to compute exact utilities?", ["Yes", "No, only to prove which one is higher", "Only at time 1", "Only for rewards"], 1, "A comparison suffices."),
  ("What does the relaxed version change?", ["The hardware", "Strictly greater becomes at least as high", "The axioms are removed", "The reward is doubled"], 1, "It allows no-harm rewrites.")],
 [("What is t1?", "The time of the switch."), ("What may a switchprog rewrite?", "Any part of the software."), ("What does check do?", "Executes the switch once a target theorem is proved."),
  ("Strict vs relaxed?", "> versus >=.")],
 [ORDER("Making a switch", "Put the steps in order.", ["A proof technique sets the switchprog", "The technique proves the target theorem", "check sees that the last theorem is a target theorem", "check sets the switch bit before t1", "Control passes to the switchprog"]),
  MATCH("Switch terms", "Match each term to its role.", [("switchprog", "The candidate rewrite"), ("switchbit", "0 to continue, 1 to switch"), ("target theorem", "Switching has higher utility"), ("t1", "When the switch takes effect")]),
  PL("Does the target theorem hold?", "The current policy earns r_old per step. A switchprog earns r_new per step but needs switch_time steps with no reward. There are remaining steps left. Write target_holds(r_old, r_new, switch_time, remaining, strict). Compare the total reward of switching, r_new times the steps left after the switch (not below zero), with continuing, r_old times remaining. Return true if switching is strictly greater (when strict is true) or at least as high (when strict is false).",
     "target_holds(r_old, r_new, switch_time, remaining, strict)", """
def target_holds(r_old, r_new, switch_time, remaining, strict):
    stay = r_old * remaining
    left = remaining - switch_time
    if left < 0:
        left = 0
    go = r_new * left
    if strict:
        return go > stay
    return go >= stay
""", [[10, 12, 5, 100, True], [10, 12, 20, 100, True], [10, 10, 0, 50, True], [10, 10, 0, 50, False], [5, 100, 200, 100, True]], "Compute both totals and compare."),
  PL("Break-even switch time", "For the same setting, write max_switch_time(r_old, r_new, remaining): the largest whole number of steps the switch may take so that switching is still strictly better than continuing. If even a switch of zero steps is not better, return -1. Assume r_new is greater than 0.",
     "max_switch_time(r_old, r_new, remaining)", """
def max_switch_time(r_old, r_new, remaining):
    best = -1
    for s in range(remaining + 1):
        if r_new * (remaining - s) > r_old * remaining:
            best = s
    return best
""", [[10, 12, 100], [10, 10, 100], [10, 20, 40], [10, 11, 1]], "Try every switch time from 0 up to remaining and keep the largest that works."),
  {"type": "webxdc", "title": "Switch explorer", "intro": "Change the numbers and watch the two utilities. Try one case where the target theorem holds and one where it does not.", "height": 520, "html": "__SWITCH__"},
  FILL("Target theorem", "The {{switchprog}} is the candidate rewrite. The machine switches only after proving the {{target}} theorem. The relaxed version allows {{equal|equality|at least as high}} utility.")]))
