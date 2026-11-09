"""Theory of Computation course, chapters 9-12."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

RUN_TM = """
def run_tm(machine, tape, max_steps):
    nstates = machine[0]
    nsyms = machine[1]
    nhalt = machine[2]
    delta = {}
    for t in machine[3]:
        delta[(t[0], t[1])] = (t[2], t[3], t[4])
    cells = {}
    for i in range(len(tape)):
        cells[i] = tape[i]
    state = 0
    head = 0
    steps = 0
    while state < nstates - nhalt:
        if steps >= max_steps:
            return [-1, state, []]
        key = (state, cells.get(head, nsyms))
        if key not in delta:
            return [-2, state, []]
        nxt = delta[key]
        state = nxt[0]
        cells[head] = nxt[1]
        if nxt[2] == 'R':
            head += 1
        else:
            head -= 1
        steps += 1
    if not cells:
        return [steps, state, []]
    out = []
    for i in range(min(cells), max(cells) + 1):
        out.append(cells.get(i, nsyms))
    while out and out[-1] == nsyms:
        out.pop()
    while out and out[0] == nsyms:
        out.pop(0)
    return [steps, state, out]
"""

INC = [3, 2, 1, [[0, 0, 0, 0, "R"], [0, 1, 0, 1, "R"], [0, 2, 1, 2, "L"], [1, 1, 1, 0, "L"], [1, 0, 2, 1, "L"], [1, 2, 2, 1, "L"]]]
SRC = [3, 2, 1, [[0, 0, 0, 1, "R"], [0, 1, 2, 1, "L"], [0, 2, 2, 2, "R"], [1, 0, 0, 0, "R"], [1, 1, 1, 0, "R"], [1, 2, 2, 2, "L"], [2, 0, 0, 1, "L"], [2, 1, 2, 0, "R"], [2, 2, 1, 1, "R"]]]
LOOP = [2, 1, 1, [[0, 0, 0, 0, "R"], [0, 1, 0, 1, "R"]]]
PART = [3, 2, 1, [[0, 0, 0, 0, "R"], [0, 1, 1, 1, "R"], [1, 0, 2, 0, "R"]]]

# ------------------------------------------------------------ 9
CHS.append(CH(
 "Turing machines",
 ("The Turing machine", [
  "Turing machine | has | Infinite tape and finite control",
  "Transition | reads | State and tape symbol",
  "Transition | writes | Symbol, state and move",
  "Halting state | ends | Computation",
  "Machine | may | Loop forever",
  "Recognizer | gives | Recursively enumerable language",
  "Halting recognizer | gives | Recursive language",
  "String processor | computes | Partial recursive function"]),
 ["Turing defined computation with a simple model: an unbounded tape of cells, a read and write head, and a finite state control. In each step the machine reads a cell, changes state, writes a symbol and moves one cell left or right.",
  "The machine may halt or run forever. As a recognizer it accepts by halting, giving recursively enumerable languages; if it halts on every input the language is recursive. As a string processor it computes partial recursive functions, total ones if it always halts.",
  "A Turing machine can be written down as a finite list of five-tuples, so it can be encoded as a string. That idea leads to the universal machine in chapter 10."],
 [("Turing machine", "T = (S, A, delta, s0, b, F): states, alphabet, transition function, start state, blank symbol, halting states."),
  ("Tape", "An unbounded row of cells, each holding a symbol or the blank."),
  ("Head", "The read and write position on the tape."),
  ("Halting state", "A state in F; entering it stops the machine."),
  ("Recursively enumerable", "Accepted by some Turing machine, which may loop on strings outside the language."),
  ("Recursive language", "Accepted by a Turing machine that halts on every input."),
  ("Partial recursive function", "A function computed by a Turing machine that may fail to halt on some inputs.")],
 ["A Turing machine has an unbounded tape and a finite state control.",
  "delta maps (state, symbol) to (state, symbol, L or R).",
  "Computation starts in s0 with the input on the tape and ends in a halting state, if ever.",
  "Languages accepted by halting: recursively enumerable; by halting on all inputs: recursive.",
  "Computed functions: partial recursive, or recursive if total.",
  "A machine is a finite set of five-tuples (s, a, s', a', d)."],
 [T("In the 1930s Alan Turing set out to characterize which mathematical functions are computable. He began by making the notion of computability precise, and the heart of his definition is a general machine, today called the Turing machine. One cannot prove that a definition is correct, only that it is useful and captures our intuitions; the Church-Turing thesis, which says every effective procedure can be done by such a machine, is of that kind."),
  T("The ingredients are a potentially infinite tape on which symbols can be written and rewritten, and a finite state control with a read and write head. Turing's intuitive model was a mathematician at work: read the page in front of you, think a bit by changing your state, perhaps rewrite the page, then turn back or forward a page."),
  M(r"T = (S, A, \delta, s_0, b, F), \qquad \delta : S \times (A \cup \{b\}) \to S \times (A \cup \{b\}) \times \{L, R\}"),
  T("Formally, a Turing machine has a finite set of states S, an alphabet A, a transition function delta, a start state s0, a blank symbol b that marks unused cells, and a set F of halting states, which may also be accepting. To run it, write a finite input string from A star on the tape, with all other cells blank, start in s0 with the head on the first input symbol, and then follow delta: depending on the state and the symbol under the head, change state, write a symbol, and move one cell left or right."),
  T("The machine continues until it enters a halting state. It might never do so: an infinite loop is possible, and this possibility is the source of almost everything difficult in computability."),
  T("There are four standard ways to read what a machine computes. As a language recognizer, a string is in the language if the machine halts on it; such languages are called recursively enumerable. As a special recognizer, some halting states are accepting and the rest rejecting; if a machine halts on every input, its language is called recursive. As a string processor, the output is the tape contents at halting, which gives a partial recursive function, since there may be no output for some inputs. And a string processor that always halts computes a recursive function."),
  T("Here is a machine you can run in the app below. It adds one to a binary number: the head moves right to the end, then carries leftward, turning each one to zero until it finds a zero or a blank to turn into a one. It has three states, with state two halting. The first two moves run to the end of the input, and the last state does the carry."),
  T("Turing's first deep insight was that a machine can itself be encoded as a finite string. The sets S, A and F are finite, so each needs only a count. We may take s0 to be the first state and assume the halting states are last in the list, so only their number is needed. The blank can be treated as one extra symbol. That leaves delta, a finite set of five-tuples of the form state, symbol, new state, new symbol, direction."),
  T("The notes give an example, encoded as three states, two symbols and one halting state, followed by nine tuples, one for each state and each symbol including the blank. Exercise in the notes: draw its control and find its language. Here is the answer you can verify in the lab. The start state zero reads a zero by writing a one and staying in state zero, moving right; reading a one it goes to halting state two; reading a blank it also goes to state two. State one is never reached from state zero, so it plays no role. So the machine halts on every input, after scanning the leading zeros. Under the halting-means-accept reading, its language is every string. One more note: the tuples listed for the halting state are never used, since the machine stops on entering it."),
  T("Practice: the lab runs machines in the same encoding, and the app lets you watch one step by step.")],
 [("What does a Turing machine do in one step?", ["Reads, changes state, writes, moves", "Sorts the tape", "Prints", "Counts symbols"], 0, "Read a cell, update state and cell, move left or right."),
  ("What happens when a Turing machine enters a halting state?", ["It starts over", "It stops", "It loops", "It erases the tape"], 1, "That ends the computation."),
  ("What is a language called if a machine halts on every input?", ["Recursively enumerable only", "Recursive", "Regular", "Finite"], 1, "A decider."),
  ("Can a Turing machine be encoded as a finite string?", ["No", "Yes, as a finite set of five-tuples", "Only if it halts", "Only if the tape is finite"], 1, "States, symbols and delta are all finite.")],
 [("What does delta output?", "New state, new symbol, and a direction L or R."), ("What marks unused cells?", "The blank symbol b."), ("What is a partial recursive function?", "Computed by a machine that may not halt on every input."),
  ("What is the Church-Turing thesis?", "Everything effectively computable is computable by a Turing machine.")],
 [PL("Run a Turing machine", "A machine is [nstates, nsyms, nhalt, tuples]. Symbols are 0 to nsyms-1 and the blank is nsyms. Halting states are the last nhalt states. Each tuple is [state, symbol, new_state, new_symbol, direction] with direction \"L\" or \"R\". Start in state 0 with the head on tape[0]; cells not given are blank. Write run_tm(machine, tape, max_steps): return [steps, final_state, tape] where tape is the list of cells from the leftmost to the rightmost non-blank cell. If the machine has not halted after max_steps steps return [-1, state, []]. If no tuple applies in a non-halting state, return [-2, state, []].",
     "run_tm(machine, tape, max_steps)", RUN_TM, [[INC, [1, 0, 1], 100], [INC, [1, 1], 100], [INC, [], 100], [SRC, [0, 0, 1], 100], [SRC, [], 100], [SRC, [1], 100], [LOOP, [0, 0], 20], [PART, [0, 0], 20]], "Store the tape in a dictionary from position to symbol; loop while the state is not a halting state."),
  PL("Missing transitions", "A machine is complete when every non-halting state has a tuple for every symbol including the blank. Write missing_transitions(machine): the sorted list of [state, symbol] pairs of non-halting states that lack a tuple.",
     "missing_transitions(machine)", """
def missing_transitions(machine):
    nstates = machine[0]
    nsyms = machine[1]
    nhalt = machine[2]
    have = []
    for t in machine[3]:
        have.append([t[0], t[1]])
    out = []
    for s in range(nstates - nhalt):
        for a in range(nsyms + 1):
            if [s, a] not in have:
                out.append([s, a])
    return out
""", [[INC], [SRC], [LOOP], [PART]], "For each non-halting state and each symbol from 0 to nsyms, check for a tuple."),
  {"type": "webxdc", "title": "Turing machine stepper", "intro": "Step through the binary incrementer, then try the machine that never halts.", "height": 560, "html": "__TM__"},
  ORDER("One step", "Put a machine's step in order.", ["Read the symbol under the head", "Look up the tuple for the state and symbol", "Write the new symbol", "Enter the new state", "Move the head left or right"]),
  FILL("Turing machines", "A Turing machine has a finite state control and an unbounded {{tape}}. It stops when it enters a {{halting}} state. A machine that halts on every input recognizes a {{recursive}} language.")]))

# ------------------------------------------------------------ 10
CHS.append(CH(
 "Universal machines, halting and Gödel",
 ("What cannot be computed", [
  "Machine | is encoded as | Finite string",
  "Universal machine | simulates | Any machine",
  "Halting problem | is | Noncomputable",
  "Rice | generalizes | Halting to nontrivial questions",
  "Gödel | showed | Unprovable truths exist",
  "Truth | is | Not computable"]),
 ["Because a machine is a finite string, another machine can take it as input. A universal Turing machine reads an encoded machine and an input and simulates the first on the second.",
  "Turing used this to prove that no machine can decide, for every machine and input, whether it halts. The only sure way to learn if a machine halts is to run it, and if it does not halt you cannot know that you have waited long enough.",
  "The notes connect this with Gödel's incompleteness theorem: any sufficiently general formal system has true statements it cannot prove. Informally, truth is noncomputable."],
 [("Universal Turing machine", "A Turing machine that, given the encoding of a machine T and an input, simulates T on that input."),
  ("Halting problem", "Decide, given a machine and an input, whether the machine halts."),
  ("Undecidable", "Having no algorithm that always answers correctly."),
  ("Semi-decidable", "Can be confirmed when the answer is yes, by running, but not refuted in general."),
  ("Incompleteness", "Gödel's result: sufficiently general consistent systems contain true but unprovable statements."),
  ("Diagonalization", "Using a table of behaviours to build one that differs from every row.")],
 ["A Turing machine's encoding can be fed to another Turing machine.",
  "A universal machine simulates any machine given its encoding and input.",
  "There is no machine that decides halting for all machines and inputs.",
  "Essentially every non-trivial question about machines is undecidable.",
  "Gödel: true statements exist that a formal system cannot prove.",
  "Together: truth cannot be computed."],
 [T("Turing's next insight follows from the encoding. If a machine is a finite string, that string can be the input of another machine. Careful construction gives a universal Turing machine, one that can simulate any other. Turing gave its specification."),
  T("To use it, take a specific machine T and a specific input string. Encode T in the universal machine's alphabet, encode the input, concatenate the two and write the result on the tape. The universal machine then shuttles between the encoded input and the encoded instructions, carrying out T's computation step by step. Your laptop works the same way: the program is data."),
  T("Turing then proved that some questions have no algorithmic answer. The famous one is the halting problem: given a machine and an input, does the machine halt? There cannot be a machine that always halts and answers this correctly. The notes put it plainly: in effect the only sure way to know if a machine halts on a string is to run it, and the trouble is that if it does not halt, you cannot know it is looping until you have waited forever."),
  T("A sketch of why. Suppose a halting decider H existed. Build a new machine D that takes a machine encoding as input, asks H whether that machine halts on its own encoding, and then does the opposite: it loops if H says halts, and halts if H says loops. Now feed D its own encoding. If D halts on itself, H said it halts, so D loops. If D loops, H said it loops, so D halts. Contradiction. This is the same diagonal trick as Cantor's, now applied to a table of machines and inputs."),
  M(r"D(\langle M \rangle) = \begin{cases} \text{loop} & \text{if } M \text{ halts on } \langle M \rangle \\ \text{halt} & \text{otherwise} \end{cases}"),
  T("A caution about the notes. They phrase the problem as: given a program, does it contain an infinite loop? The standard halting problem is slightly different. It fixes an input, and asks whether the program stops on that input. A program might loop forever on some inputs and halt on others, and a program with a loop in its text might always halt. Keep the standard form in mind."),
  T("The practical consequence is that you can only half-answer. Run the machine. If it halts, you know. If it has not halted after a million steps, you know nothing. The lab implements this bounded check. Such properties are called semi-decidable."),
  T("Beyond halting, the notes say that almost every interesting question about Turing machines, essentially any non-trivial question about what a program does, is undecidable. In the language of logic, undecidable means no algorithm decides the question. This general fact is known as Rice's theorem."),
  T("Gödel's work arrived at almost the same time. He showed that in any sufficiently general formal logical system there are true statements that cannot be proved within it. The notes put it together with Turing's result and say that, in effect, truth is a noncomputable function. They also say the two results are mathematically equivalent. That is better read as informal: the results are closely related, and the halting problem gives one standard proof of incompleteness, but they are not literally the same theorem. The Gödel Machine course in this library builds on exactly this link.")],
 [("What does a universal Turing machine do?", ["Halts on every input", "Simulates any machine given its encoding and input", "Solves the halting problem", "Prints primes"], 1, "Program as data."),
  ("What does the halting problem ask?", ["Whether a given machine halts on a given input", "Whether a machine is fast", "Whether a tape is empty", "Whether a string is a palindrome"], 0, "It is noncomputable."),
  ("How can you tell for sure that a machine halts?", ["Run it and see it stop", "Analyse its states", "Count its tuples", "Ask a universal machine"], 0, "Running confirms halting but never refutes it."),
  ("What does Gödel's incompleteness theorem say?", ["Every truth is provable", "Some truths in a rich enough system are unprovable", "Systems are inconsistent", "Proofs are short"], 1, "That is the incompleteness result.")],
 [("Is halting semi-decidable?", "Yes: run and wait for it to stop."), ("What is diagonalization?", "Building an item that differs from every row of a list."), ("Rice's theorem?", "Non-trivial program properties are undecidable."),
  ("Is the Gödel result equal to Turing's?", "Closely related, not literally the same.")],
 [PL("Bounded halting check", "Using the machine encoding from the last chapter (blank = nsyms, halting states are the last nhalt states), write halts_within(machine, tape, n): true if the machine enters a halting state within n steps, false otherwise (a machine that has no applicable tuple also counts as not halting). This is the part of the halting problem that can be answered.",
     "halts_within(machine, tape, n)", RUN_TM + """
def halts_within(machine, tape, n):
    r = run_tm(machine, tape, n)
    return r[0] >= 0
""", [[INC, [1, 0, 1], 100], [INC, [1, 0, 1], 3], [SRC, [0, 0, 1], 100], [LOOP, [0, 0], 1000], [PART, [0, 0], 20]], "Run with a step limit; the answer is yes only when the run ended in a halting state."),
  PL("Build the diagonal machine", "H is a square table: H[i][j] is 1 if machine i halts on input j and 0 if not. Write halting_diagonal(H): the list D where D[i] is 0 if H[i][i] is 1 and 1 otherwise. Then D[i] differs from the diagonal entry of every row, so D is not a row of H.",
     "halting_diagonal(H)", """
def halting_diagonal(H):
    out = []
    for i in range(len(H)):
        if H[i][i] == 1:
            out.append(0)
        else:
            out.append(1)
    return out
""", [[[[1, 0], [0, 1]]], [[[0, 0, 0], [1, 1, 1], [0, 1, 0]]], [[[1]]]], "Flip the diagonal."),
  MATCH("Computability", "Match each result with its message.", [("Universal machine", "Simulates any machine from its encoding"), ("Halting problem", "No algorithm decides it for all inputs"), ("Rice", "Non-trivial questions are undecidable"), ("Gödel", "True but unprovable statements exist"), ("Semi-decidable", "Confirmed by running, never refuted")]),
  FILL("Halting", "A {{universal}} machine simulates any machine. The {{halting}} problem is undecidable. The only sure way to see that a machine halts is to {{run}} it.")]))

# ------------------------------------------------------------ 11
CHS.append(CH(
 "Computability and tractability",
 ("Time, growth and NP", [
  "Big O | compares | Growth of functions",
  "Polynomial | is | Tractable",
  "Exponential | is | Intractable",
  "NP | means | Solutions checked in polynomial time",
  "NP complete | is | Hardest in NP",
  "Satisfiability | is | NP complete",
  "Factoring | is | In NP",
  "P versus NP | is | Open"]),
 ["Computable does not mean practical. We measure how time and space grow with the size of the input, using big-O notation, and call a problem tractable if some algorithm runs in polynomial time.",
  "NP problems are those whose proposed solutions can be checked in polynomial time. NP-complete problems are the hardest of them: a fast algorithm for any one would give fast algorithms for all. Boolean satisfiability is NP-complete.",
  "Whether polynomial time equals NP is open. Factoring is in NP, and the security of RSA relies on its apparent difficulty; primality, by contrast, is decidable in polynomial time."],
 [("Big-O", "g is in O(f) if g(n) is at most c times f(n) for some c and all large n."),
  ("Theta", "g is in Theta(f) if g is in O(f) and f is in O(g)."),
  ("Tractable", "Solvable by an algorithm whose worst-case time is polynomial."),
  ("NP", "Problems whose solutions can be verified in polynomial time."),
  ("NP-complete", "A problem in NP into which every problem in NP can be translated in polynomial time."),
  ("Satisfiability", "Given a Boolean formula, is there an assignment making it true?"),
  ("Factoring", "Given a number, find its prime factors.")],
 ["g in O(f) iff there are c > 0 and N with |g(n)| <= c |f(n)| for all n >= N.",
  "Classes: logarithmic, linear, quadratic, polynomial, exponential, factorial.",
  "Tractable: polynomial; intractable otherwise (as far as we know).",
  "NP: verifying a solution is easy, finding one may not be.",
  "NP-complete: if one is solved in polynomial time, all of NP is.",
  "Satisfiability is NP-complete; factoring is in NP; whether P = NP is open."],
 [T("Some problems are not computable at all. Others are computable but take far too long. The notes now turn to the second kind. First, the halting problem again: they describe it as whether a program contains an infinite loop, and, as in chapter 10, the careful statement fixes an input. More practically, we want to know whether a program runs in a reasonable time and with reasonable memory."),
  T("We classify algorithms by how the resources they need grow with the size of the input. Typical resources are time and storage space. We may care about worst-case or average-case behaviour. For theory we usually care about large inputs."),
  M(r"g \in O(f) \iff \exists\, c > 0,\ N \ge 0 \ :\ |g(n)| \le c\,|f(n)| \ \ \forall\, n \ge N"),
  T("That is big-O. It compares the growth of functions on the natural numbers while ignoring constant factors and small inputs. Theta of f is the set of g such that g is in O of f and f is in O of g, so g and f grow at the same rate. An algorithm's running time is measured in elementary operations as a function of the number of bits in the encoded input."),
  T("Common categories, in order of growth: logarithmic, linear, quadratic, polynomial, exponential, factorial. Exponential means growing like b to the n for some b above one; factorial is n factorial. A problem is called tractable if we know an algorithm solving it in at most polynomial time, and intractable otherwise."),
  T("Now NP. Many problems have the property that if someone hands you a solution, you can check it in polynomial time. These are the nondeterministically polynomial, or NP, problems. One way to think of it: imagine arbitrarily many machines, each trying one candidate solution, and whichever finds a solution tells you. Notice that this does not mean they are easy to solve, only to check."),
  T("Among them are the NP-complete problems, which are universal for NP. A problem S is NP-complete if it is in NP and any NP problem can be translated into an instance of S by a polynomial-time algorithm. So a polynomial-time algorithm for one NP-complete problem would give polynomial-time algorithms for every NP problem."),
  T("Example one: factoring. If M is the number to factor, the input size m is about the number of digits of M. The school method divides by every number up to the square root of M, which takes about 10 to the m over 2 steps, exponential in the number of digits. But if someone gives you two numbers claimed to be factors, checking takes one multiplication, about m squared operations. So factoring is in NP. The notes add that primality can be decided in polynomial time, but that test does not produce factors for composite numbers. Factoring matters because encryption such as RSA depends on it being hard for numbers with hundreds of digits. Note that factoring is in NP, but it is not known to be NP-complete."),
  T("Example two: Boolean satisfiability. Take n Boolean variables and a formula that is an AND of clauses, each clause an OR of variables and negated variables. A solution is an assignment of zero or one to each variable that makes the formula true. There are 2 to the n assignments. Checking one assignment takes polynomial time, but there are exponentially many to try. Satisfiability is NP-complete, and a feasible algorithm for it would settle the famous question of whether P equals NP. The labs check and brute-force small formulas.")],
 [("What does g in O(f) mean?", ["g is at most c times f for large n", "g equals f", "g is smaller than f for all n", "g is constant"], 0, "Up to a constant, eventually."),
  ("What is true of NP problems?", ["They are unsolvable", "A proposed solution can be checked in polynomial time", "They are all exponential", "They are all linear"], 1, "Verification is easy."),
  ("What does NP-complete mean?", ["Every NP problem translates to it in polynomial time and it is in NP", "It is impossible", "It is linear", "It is a language"], 0, "These are the hardest in NP."),
  ("Which statement about factoring is correct?", ["It is in NP", "It is known to be NP-complete", "It is undecidable", "It is linear time"], 0, "A claimed factorisation is easy to check.")],
 [("What is tractable?", "Solvable in polynomial time."), ("What is SAT?", "Is there an assignment making the formula true?"), ("Why does RSA rely on factoring?", "Factoring large numbers is believed hard."),
  ("Is P=NP solved?", "No, it is open.")],
 [PL("Check a big-O witness", "Polynomials are lists of coefficients, lowest degree first: [5, 3] is 5 + 3n. Write in_big_o(g, f, c, N, upto): true if |g(n)| <= c * |f(n)| for every integer n from N to upto inclusive.",
     "in_big_o(g, f, c, N, upto)", """
def in_big_o(g, f, c, N, upto):
    def val(p, n):
        total = 0
        for k in range(len(p) - 1, -1, -1):
            total = total * n + p[k]
        return total
    for n in range(N, upto + 1):
        if abs(val(g, n)) > c * abs(val(f, n)):
            return False
    return True
""", [[[0, 0, 3], [0, 0, 1], 3, 0, 100], [[0, 0, 3], [0, 0, 1], 2, 0, 100], [[5, 3], [0, 1], 4, 5, 200], [[5, 3], [0, 1], 4, 1, 200], [[0, 0, 1], [0, 1], 100, 0, 1000]], "Evaluate both polynomials at each n and compare."),
  PL("Trial division cost", "The school method for factoring tries d = 2, 3, 4, ... and stops at the first d that divides M, or when d * d exceeds M. Write trial_division_steps(M): how many values of d it tries.",
     "trial_division_steps(M)", """
def trial_division_steps(M):
    d = 2
    steps = 0
    while d * d <= M:
        steps += 1
        if M % d == 0:
            return steps
        d += 1
    return steps
""", [[91], [97], [1000003], [15485863], [2], [100]], "Count each division attempt."),
  PL("Verify a factorisation", "Verifying is cheap. Write verify_factors(M, a, b): true if a and b are both greater than 1 and a * b equals M.",
     "verify_factors(M, a, b)", """
def verify_factors(M, a, b):
    return a > 1 and b > 1 and a * b == M
""", [[91, 7, 13], [91, 1, 91], [1000036000099, 1000003, 1000033], [91, 7, 14], [15, 3, 5]], "One multiplication and two comparisons."),
  PL("Check a satisfying assignment", "A formula is a list of clauses; each clause is a list of non-zero integers: k means variable k is true, -k means variable k is false (variables are numbered from 1). An assignment is a list of 0 and 1 where position 0 is variable 1. Write sat_check(clauses, assign): true if every clause contains at least one true literal.",
     "sat_check(clauses, assign)", """
def sat_check(clauses, assign):
    for cl in clauses:
        ok = False
        for lit in cl:
            v = assign[abs(lit) - 1]
            if (lit > 0 and v == 1) or (lit < 0 and v == 0):
                ok = True
                break
        if not ok:
            return False
    return True
""", [[[[1, -2], [2, 3], [-1, -3]], [1, 1, 0]], [[[1, -2], [2, 3], [-1, -3]], [1, 0, 0]], [[[1], [-1]], [1]], [[], [0]]], "Each clause needs one true literal."),
  PL("Brute-force SAT", "Write sat_brute(clauses, n): try the 2^n assignments in this order: for m = 0, 1, 2, ..., 2^n - 1, variable i (starting at 1) gets bit (i-1) of m. Return the first satisfying assignment as a list of 0 and 1, or an empty list if none exists.",
     "sat_brute(clauses, n)", """
def sat_brute(clauses, n):
    for m in range(2 ** n):
        assign = []
        for i in range(n):
            assign.append((m >> i) & 1)
        good = True
        for cl in clauses:
            ok = False
            for lit in cl:
                v = assign[abs(lit) - 1]
                if (lit > 0 and v == 1) or (lit < 0 and v == 0):
                    ok = True
                    break
            if not ok:
                good = False
                break
        if good:
            return assign
    return []
""", [[[[1, -2], [2, 3], [-1, -3]], 3], [[[1], [-1]], 1], [[[1, 2], [-1, 2], [1, -2]], 2], [[[1, 2, 3], [-1], [-2], [-3]], 3]], "Loop m from 0 to 2^n - 1, extract bits, check every clause."),
  MATCH("Complexity", "Match each term with its meaning.", [("O(f)", "Grows no faster than f, up to a constant"), ("Tractable", "Polynomial-time solvable"), ("NP", "Solutions verifiable in polynomial time"), ("NP-complete", "Hardest problems in NP"), ("SAT", "Boolean satisfiability")]),
  FILL("Tractability", "Problems solvable in {{polynomial}} time are called tractable. In NP a given solution can be {{checked|verified}} quickly. {{Satisfiability|SAT}} is NP-complete.")]))

# ------------------------------------------------------------ 12
CHS.append(CH(
 "Computational complexity of strings",
 ("Measuring complexity", [
  "Entropy | needs | Probability model",
  "Upper bound | is | Number of bits",
  "Lower bound | is | Zero",
  "Computational complexity | is | Shortest program length",
  "Complexity | is | Noncomputable",
  "Entropy and complexity | are | Essentially equal"]),
 ["Given a long string of bits recording a system, how complex is the system? One answer is information entropy, but it depends on a probability model and has no model-free value: it ranges from zero to the length of the string.",
  "Another is computational complexity: the length of the shortest machine and input pair that makes a standard universal machine output the string. It is well defined but noncomputable, by the halting problem.",
  "We can improve upper bounds by trying many programs with time limits, and the two measures are in a precise sense essentially equal, so either can be useful. The measure is also called Kolmogorov or algorithmic complexity."],
 [("Information entropy", "The average information of a probability model; for a given string it depends on the model chosen."),
  ("Computational complexity", "The length of the shortest machine and input pair that makes a fixed universal machine output the string."),
  ("Upper bound", "A value the quantity cannot exceed; here the length of the string."),
  ("Lower bound", "A value the quantity cannot go below; here zero."),
  ("Noncomputable function", "A function no algorithm can compute for all inputs."),
  ("Kolmogorov complexity", "Another name for the shortest-description-length measure, studied by Kolmogorov and Chaitin.")],
 ["Entropy needs a probability model; there are many.",
  "Under a fair-coin model the entropy of a string is its length; under a model that predicts it exactly it is zero.",
  "Computational complexity: the shortest (machine, input) pair giving the string.",
  "Its upper bound is about the length of the string; the lower bound is zero.",
  "It is noncomputable because of the halting problem; better upper bounds come from trying machines.",
  "The two measures are essentially equal."],
 [T("The last topic of the notes asks a different kind of question. Suppose we watch a system for a fixed time with some instruments, and record what we see as a finite string of bits. Can we assign a meaningful number to the complexity of the system from that string alone?"),
  T("The first approach is information entropy. The trouble is that entropy is relative to a probability model, and many models are possible. If the model is an unbiased coin, the string is just one possible outcome and its information content is its length in bits, which is the upper bound. If the model gives this one string probability one, the entropy is zero, the lower bound. Neither says much."),
  M(r"H = -\sum_{i} p_i \log_2 p_i"),
  T("To use entropy well, one must run the system many times and build the best probability model from the results, ideally in the limit of infinitely many observations. In practice we have limited observations and settle for an incomplete answer, possibly improved by judicious subsampling."),
  T("The second approach uses a universal Turing machine. Fix one standard UTM. Ask for the minimum length of a pair, a machine T and an input sigma, that makes the UTM leave the string beta on its tape as output. That minimum length is called the computational complexity of beta. It depends on which UTM was chosen, but only up to a constant, so we may take a standard one."),
  T("Bounds. The lower bound is zero, as for entropy. For an upper bound, take the machine that halts at once, whatever it is given. Pair it with beta itself as the input. That pair leaves beta as output and its length is essentially the length of beta, since the machine's code is tiny. This agrees with the entropy upper bound. Writing out such an encoding is an exercise in the notes."),
  T("In theory, the complexity of every string exists: the set of lengths of working pairs is nonempty, so it has a smallest element. In practice there is a catch. By Turing's halting result, we cannot always tell whether a given machine on a given input halts and leaves the right output. We may just have to run it and wait forever. So computational complexity is a noncomputable function."),
  T("But we can still shrink the upper bound. Try many machines, put limits on how long each may run before we discard it, and hope for luck. That is the computer scientist's reading of the situation, while the theory is the mathematician's. The notes say the philosopher has plenty to chew on."),
  T("Both measures leave us unsure in principle. Entropy needs infinitely many observations to be sure of the model. Complexity needs infinitely long runs to exclude some machines. The notes add a reassuring fact: the two values, though never guaranteed in practice, are essentially equal, so you can pick whichever suits what you know about the system. Read that as a statement about averages up to a constant, as in algorithmic information theory, rather than as an identity for every string."),
  T("That ends the notes. A fitting summary of the whole course: some things cannot be computed, some can be computed but not in reasonable time, and even measuring how complex something is runs into the same limits.")],
 [("Why is entropy of a string ambiguous?", ["It depends on the chosen probability model", "Strings have no entropy", "It is always zero", "It is always the length"], 0, "Different models give different values."),
  ("What is the computational complexity of a string here?", ["Its length", "The length of the shortest (machine, input) pair producing it on a fixed UTM", "Its number of ones", "Its running time"], 1, "That is the definition used in the notes."),
  ("Why is computational complexity noncomputable?", ["Strings are infinite", "It would require solving the halting problem", "UTMs differ", "Machines are random"], 1, "You cannot tell which machines halt."),
  ("What can reduce the upper bound in practice?", ["Trying many machines with time limits", "Guessing", "Doubling the string", "Nothing"], 0, "Search for shorter descriptions.")],
 [("Upper bound of complexity?", "About the length of the string."), ("Lower bound?", "Zero."), ("What did Kolmogorov and Chaitin study?", "Descriptive (algorithmic) complexity."),
  ("Do the two measures agree?", "Essentially, up to a constant.")],
 [PL("Shannon entropy", "Write shannon_entropy(probs): the entropy in bits, minus the sum of p times log base 2 of p, skipping zero probabilities. Use math.log(p) / math.log(2).",
     "shannon_entropy(probs)", """
import math
def shannon_entropy(probs):
    total = 0.0
    for p in probs:
        if p > 0:
            total -= p * math.log(p) / math.log(2)
    return total
""", [[[0.5, 0.5]], [[1.0]], [[0.25, 0.25, 0.25, 0.25]], [[0.9, 0.1]], [[0.5, 0.25, 0.25, 0.0]]], "Skip zeros to avoid log of zero.", 1e-9),
  PL("Entropy of a string", "Estimate the model from the string itself: the probability of each symbol is its frequency. Write empirical_entropy(s): the entropy in bits per symbol (0 for the empty string).",
     "empirical_entropy(s)", """
import math
def empirical_entropy(s):
    n = len(s)
    if n == 0:
        return 0.0
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    total = 0.0
    for c in counts:
        p = counts[c] / n
        total -= p * math.log(p) / math.log(2)
    return total
""", [[""], ["0000"], ["0101"], ["aab"], ["abcd"], ["0001"]], "Count each symbol, convert to probabilities, then apply the formula.", 1e-9),
  PL("A cheap description bound", "A crude upper bound on complexity: either list the string (cost = its length) or describe its runs. Run-length cost = the sum over runs of (1 + number of digits of the run length). Write description_bound(s): the smaller of len(s) and the run-length cost (0 for the empty string).",
     "description_bound(s)", """
def description_bound(s):
    if len(s) == 0:
        return 0
    cost = 0
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        cost += 1 + len(str(j - i))
        i = j
    return min(len(s), cost)
""", [[""], ["0" * 100], ["0101"], ["0000011111"], ["abc"], ["a" * 9 + "b" * 12]], "Walk through runs and add 1 + digits of the run length for each."),
  MATCH("Measures", "Match each measure with its feature.", [("Entropy", "Depends on a probability model"), ("Computational complexity", "Shortest machine and input pair"), ("Upper bound", "About the length of the string"), ("Lower bound", "Zero"), ("Halting problem", "Makes complexity noncomputable")]),
  FILL("Complexity", "Entropy depends on a probability {{model}}. Computational complexity is {{noncomputable|not computable}} because of the {{halting}} problem.")]))
