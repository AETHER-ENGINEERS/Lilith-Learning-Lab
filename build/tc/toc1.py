"""Theory of Computation course, chapters 1-4."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 1
CHS.append(CH(
 "Symbols, strings and languages",
 ("Basic objects", [
  "Alphabet | is | Finite set of symbols",
  "String | is built from | Alphabet",
  "Empty string | has | Length zero",
  "A star | contains | All strings over A",
  "Language | is | Subset of A star",
  "Recognizer | decides | Membership in a language"]),
 ["The theory of computation starts with strings. An alphabet is a finite set of symbols, a string is a finite sequence of them, and a language is any set of strings over the alphabet.",
  "A star is the set of all strings over A, including the empty string. Every language is a subset of A star, so a language is just a yes or no question about strings.",
  "Processing a string into a yes or no answer is pattern recognition, and that is the view the rest of the course takes."],
 [("Alphabet", "A finite set of symbols."),
  ("String", "A finite ordered sequence of symbols from an alphabet; repeats are allowed."),
  ("Length", "The number of symbols in a string, counting repeats."),
  ("Empty string", "The unique string of length zero, written epsilon. It is not the empty set."),
  ("A star", "The set of all strings over A, of every finite length including zero."),
  ("Language", "Any subset of A star."),
  ("Concatenation of sets", "ST is the set of all strings xy with x in S and y in T.")],
 ["An alphabet is finite; a string is a finite sequence over it.",
  "The empty string has length 0 and is not the same thing as the empty set.",
  "ST = {xy : x in S, y in T}; A^0 = {epsilon}; A^(n+1) = A A^n.",
  "A* is the union of all A^n.",
  "A language is any subset of A*.",
  "A machine that answers yes or no for strings is a language recognizer."],
 [T("This course follows Tom Carter's 2005 notes, Introduction to the theory of computation, written for the Complex Systems Summer School. The notes are short and deliberately abbreviated. This course slows down, adds worked examples and runs the ideas as small Python programs."),
  T("Classical computation turns an input string of symbols into an output string. A special case matters most: when the only possible outputs are yes and no, processing a string is the same as recognizing a pattern. Deciding whether a string belongs to a set is the central question of the whole subject."),
  T("The notes start by refusing to define the word symbol. That leaves a slot open, so the abstract theory can later be connected to anything in the world: letters, bits, molecules in a protein, sounds, events. Everything else is built from that single undefined idea."),
  T("Definitions. An alphabet is a finite set of symbols. A string over an alphabet A is a finite ordered sequence of symbols from A, and repeats are allowed. Its length counts every symbol, so the string aabbcc has length six. The empty string, written epsilon, has length zero. Careful: it is a string, so it is not the empty set, which has no elements at all."),
  T("Next, products of sets of strings. If S and T are sets of strings, then ST is the set of every x followed by a y, with x taken from S and y from T. This is the first operation that later becomes concatenation in regular expressions."),
  M(r"ST = \{\, xy \mid x \in S,\ y \in T \,\}"),
  T("Powers come from repeating that product. A to the zero is the set containing only the empty string. A to the n plus one is A times A to the n. And A star is the union over all n of A to the n. So A star contains every finite string over A, including epsilon."),
  M(r"A^{0} = \{\varepsilon\}, \qquad A^{n+1} = A\,A^{n}, \qquad A^{*} = \bigcup_{n=0}^{\infty} A^{n}"),
  T("Finally, a language L over A is a subset of A star. Nothing more. Even a random subset counts. The set of strings of even length is a language, the set of valid C programs is a language, and the set of all strings is a language. Whether a machine can recognize a given language is the question that drives chapters 3 to 10."),
  T("A quick example. Let A be the two symbols a and b. Then A to the two is aa, ab, ba and bb. A star lists epsilon, a, b, aa, ab, ba, bb, aaa, and so on, forever. The practice section has you build these lists, which also shows that A star can be listed one string at a time, a fact chapter 2 uses.")],
 [("Which statement about the empty string is correct?", ["It is the same as the empty set", "It has length zero and is a string", "It is not in A star", "It is a symbol"], 1, "Epsilon is a string of length 0; the empty set contains no strings."),
  ("What is a language over an alphabet A?", ["A finite set of symbols", "Any subset of A star", "A single string", "A grammar"], 1, "A language is a set of strings."),
  ("What is |aabbcc|?", ["3", "6", "2", "12"], 1, "Repeated symbols are counted."),
  ("What is A^0?", ["The empty set", "The set containing only the empty string", "A", "A star"], 1, "A^0 = {epsilon}.")],
 [("Why leave 'symbol' undefined?", "So the theory can connect to anything in the world."), ("Is A star finite?", "No, it is infinite for any nonempty alphabet."), ("What is ST?", "All strings xy with x in S and y in T."),
  ("Is a language always a regular pattern?", "No, any set of strings is a language.")],
 [PL("Product of string sets", "A set of strings is given as a list. Write concat_sets(S, T): the list of all strings xy with x in S and y in T, without duplicates, sorted. The empty string is written as \"\".",
     "concat_sets(S, T)", """
def concat_sets(S, T):
    out = []
    for x in S:
        for y in T:
            w = x + y
            if w not in out:
                out.append(w)
    out.sort()
    return out
""", [[["a", "b"], ["c", "d"]], [[""], ["x", "y"]], [[], ["a"]], [["a", "ab"], ["b", ""]]], "Two loops, build x + y, skip duplicates, then sort."),
  PL("List A star up to length n", "Write strings_up_to(alphabet, n): every string over the alphabet (given as a string of symbols) of length 0 to n, shortest first, and within the same length in alphabet order. The empty string comes first.",
     "strings_up_to(alphabet, n)", """
def strings_up_to(alphabet, n):
    out = [""]
    layer = [""]
    for i in range(n):
        nxt = []
        for w in layer:
            for c in alphabet:
                nxt.append(w + c)
        out = out + nxt
        layer = nxt
    return out
""", [["ab", 2], ["01", 0], ["01", 3], ["a", 3]], "Build each length from the previous one by appending every symbol."),
  MATCH("Basic terms", "Match each term with its meaning.", [("Alphabet", "A finite set of symbols"), ("String", "A finite sequence of symbols"), ("Epsilon", "The string of length zero"), ("A star", "All strings over A"), ("Language", "A subset of A star")]),
  FILL("Strings", "An {{alphabet}} is a finite set of symbols. A {{language}} over A is a subset of A star. The string of length zero is the {{empty}} string.")]))

# ------------------------------------------------------------ 2
CHS.append(CH(
 "Countability and the limits of computation",
 ("Sizes of infinity", [
  "Same size | means | One-to-one onto function",
  "Countable | means | At most size of N",
  "Integers | are | Countable",
  "Rationals | are | Countable",
  "A star | is | Countably infinite",
  "Power set | is | Strictly larger",
  "Languages | are | Uncountable",
  "Programs | are | Countable"]),
 ["Two sets have the same size if a one-to-one onto function connects them. A set is countable when it is no bigger than the natural numbers. The integers, the rationals and A star are all countable.",
  "Cantor's argument shows that the power set of any set is strictly bigger than the set. So the set of all languages over an alphabet is uncountable.",
  "Programs are finite strings, so there are only countably many. Therefore some languages have no program that decides them. This is the first non-computability result, and it needs no machine at all."],
 [("One-to-one", "A function that never sends two different inputs to the same output."),
  ("Onto", "A function whose outputs cover the whole target set."),
  ("Countably infinite", "The same size as the natural numbers."),
  ("Uncountable", "Strictly larger than the natural numbers."),
  ("Power set", "The set of all subsets of S, written P(S)."),
  ("Diagonal argument", "Build an object that differs from the i-th item of a list at position i, so it cannot be on the list.")],
 ["|S| = |T| iff there is a one-to-one onto function.",
  "Z, Q, S x S and A* are countable when S is countable and A is a finite alphabet.",
  "For every set S, |S| < |P(S)| (Cantor).",
  "R and P(N) have the same size, so R is uncountable.",
  "There are countably many programs but uncountably many languages.",
  "So some languages cannot be recognized by any algorithm."],
 [T("Before studying machines, the notes make a counting argument that already shows computers have limits. It rests on a precise notion of size. Two sets S and T have the same size when some one-to-one function from S onto T exists. We write S is at most T when a one-to-one function from S into T exists, and strictly smaller when such a function exists but no onto function does."),
  T("A set is finite if it is smaller than the natural numbers, countable if it is no larger, countably infinite if it has exactly the same size, and uncountable if it is strictly larger. The natural numbers themselves are built from nothing: zero is the empty set, one is the set containing zero, and in general n plus one is the set of 0 up to n."),
  T("Countable examples. The integers can be listed 0, 1, minus 1, 2, minus 2 and so on. The rationals are countable too: list pairs of integers along diagonals. If S is countable, so is S times S, and S to the n for any finite n. And for any nonempty finite alphabet A, A star is countably infinite, since you can list it by length and then alphabetically. The notes leave these as exercises; the labs here do all of them."),
  M(r"|S| < |\mathcal{P}(S)| \quad \text{for every set } S"),
  T("The key theorem is Cantor's. Every set S is smaller than its power set P of S. First, S is at most P of S, since each element s maps to the one-element set containing s. Second, no function f from S to P of S can be onto, and here is the proof."),
  T("Given any f, build the set R of those x in S with x not in f of x. R is a subset of S, so it is a candidate to be hit. Suppose f of some s equals R. If s is in f of s, then s is in R, so by the definition of R it is not in f of s: a contradiction. If s is not in f of s, then s satisfies the condition for R, so s is in R, which is f of s: again a contradiction. So no s exists, and f is not onto."),
  M(r"R_f = \{\, x \in S \mid x \notin f(x) \,\}"),
  T("Consequences. The power set of N is uncountable. The real numbers are the same size as P of N, via binary expansions, so the reals are uncountable as well. The notes leave this proof as an exercise with a hint: show R is the same size as the interval from 0 to 1, then use binary representations."),
  T("Now the application to computing. Assume every algorithm can be written as a program, and every program is a finite string of ASCII characters. ASCII star is countably infinite, so there are at most countably many programs. But a language over an alphabet is any subset of A star, so there are uncountably many languages. Therefore there are languages with no program that decides membership. Most languages cannot be recognized by any computer algorithm."),
  T("Notice what this argument gives and does not give. It proves that unrecognizable languages exist but does not name a single one. Chapter 10 produces a concrete example, the halting problem.")],
 [("Which function shows that Z is countable?", ["Listing 0, 1, -1, 2, -2, ...", "Listing 0, 1, 2, ... only", "Squaring", "None exists"], 0, "That list hits each integer exactly once."),
  ("What does Cantor's argument show about P(S)?", ["It is smaller than S", "It is strictly larger than S", "It equals S", "It is empty"], 1, "No function from S to P(S) is onto."),
  ("Why are there only countably many programs?", ["Programs are short", "Each is a finite string over a finite alphabet", "Programs are numbers", "Computers are finite"], 1, "A star is countable for a finite alphabet."),
  ("What follows from the counting argument?", ["Every language has a recognizer", "Some languages have no recognizer", "All languages are regular", "P equals NP"], 1, "There are uncountably many languages.")],
 [("Is Q countable?", "Yes, list pairs along diagonals."), ("Is R countable?", "No, it is the same size as P(N)."), ("What is R_f?", "{x in S : x not in f(x)}, the set missing from the image of f."),
  ("Does counting name an unrecognizable language?", "No, it only proves one exists.")],
 [PL("Listing the integers", "List the integers in the order 0, 1, -1, 2, -2, 3, -3, ... with positions starting at 0. Write int_at(k): the integer at position k.",
     "int_at(k)", """
def int_at(k):
    if k % 2 == 1:
        return (k + 1) // 2
    return -(k // 2)
""", [[0], [1], [2], [3], [4], [99], [100]], "Odd positions hold positive numbers, even positions hold negatives."),
  PL("Pairing function", "To show N x N is countable, number the pairs along diagonals: (0,0), (0,1), (1,0), (0,2), (1,1), (2,0), ... Write cantor_pair(i, j): the position of (i, j) when pairs are listed by increasing i+j, and within the same i+j by increasing j. Use position = (i+j)(i+j+1)/2 + j.",
     "cantor_pair(i, j)", """
def cantor_pair(i, j):
    d = i + j
    return d * (d + 1) // 2 + j
""", [[0, 0], [0, 1], [1, 0], [0, 2], [1, 1], [2, 0], [10, 7]], "Use the given formula with integer division."),
  PL("Inverse pairing", "Write cantor_unpair(n): the pair [i, j] at position n of the same list. Find the diagonal d first (the largest d with d(d+1)/2 at most n), then j = n - d(d+1)/2 and i = d - j.",
     "cantor_unpair(n)", """
def cantor_unpair(n):
    d = 0
    while (d + 1) * (d + 2) // 2 <= n:
        d += 1
    j = n - d * (d + 1) // 2
    return [d - j, j]
""", [[0], [1], [2], [5], [6], [100]], "Walk d upward until the next diagonal would start beyond n."),
  PL("Index of a string", "List all strings over an alphabet by length, then in alphabet order: the empty string is 0, then the first symbol is 1, and so on. Write string_index(s, alphabet): the position of s. Treat the alphabet as digits 1..k and compute index = index * k + digit for each symbol.",
     "string_index(s, alphabet)", """
def string_index(s, alphabet):
    k = len(alphabet)
    idx = 0
    for c in s:
        idx = idx * k + alphabet.index(c) + 1
    return idx
""", [["", "ab"], ["a", "ab"], ["b", "ab"], ["aa", "ab"], ["ba", "ab"], ["abba", "ab"], ["101", "01"]], "This is counting in bijective base k."),
  PL("Cantor's missing set", "A function f from {0..n-1} to subsets of {0..n-1} is given as a list: f[x] is the list of elements of the subset assigned to x. Write cantor_set(f): the sorted list of x with x not in f[x]. This set is not f(y) for any y.",
     "cantor_set(f)", """
def cantor_set(f):
    out = []
    for x in range(len(f)):
        if x not in f[x]:
            out.append(x)
    return out
""", [[[[0], [0, 1], []]], [[[1], [2], [0]]], [[[0, 1, 2], [0, 1, 2], [0, 1, 2]]], [[[], [], []]]], "Loop over x and test membership of x in f[x]."),
  FILL("Counting", "A set is {{countable}} when it is no bigger than the natural numbers. Cantor showed the power set of S is {{strictly|strictly larger|larger}} than S. There are {{uncountably|uncountably many}} languages but only countably many programs.")]))

# ------------------------------------------------------------ 3
CHS.append(CH(
 "Finite automata",
 ("DFAs and NFAs", [
  "DFA | has | States, alphabet, start, delta, finals",
  "Delta | maps | State and symbol to state",
  "Extended delta | processes | Whole strings",
  "L(M) | is | Strings leading to a final state",
  "NFA | allows | Several next states",
  "Epsilon move | changes state | Without input",
  "DFA | equals | NFA in power",
  "NFA with n states | may need | 2^n DFA states"]),
 ["A deterministic finite automaton has finitely many states, a start state, final states and a transition function that gives exactly one next state for each state and symbol. It reads a string and accepts if it ends in a final state.",
  "A nondeterministic automaton may have several next states, or none. It accepts if some path ends in a final state. Epsilon moves let it change state without reading input.",
  "All three kinds accept exactly the same languages. Converting an NFA to a DFA can need as many as 2 to the n states, which is why NFAs are easier to write and DFAs easier to run."],
 [("DFA", "A deterministic finite automaton: states S, alphabet A, start s0, transition function delta from S x A to S, and final states F."),
  ("Extended transition function", "The function that applies delta symbol by symbol to a whole string."),
  ("L(M)", "The language of machine M: all strings that lead from the start state to a final state."),
  ("NFA", "A nondeterministic finite automaton; delta gives a set of possible next states."),
  ("Epsilon move", "A transition taken without reading any input symbol."),
  ("Subset construction", "Converting an NFA to a DFA whose states are sets of NFA states."),
  ("Recognizer", "A machine that decides membership in its language.")],
 ["A DFA is M = (S, A, s0, delta, F).",
  "L(M) = {x : delta-hat(s0, x) is in F}.",
  "An NFA's delta returns a set of states; it accepts when the set reached meets F.",
  "DFAs, NFAs and NFAs with epsilon moves define the same languages.",
  "An NFA with n states can need up to 2^n DFA states.",
  "NFAs are easy to write; DFAs can be implemented directly."],
 [T("The notes begin with the simplest machines, finite automata. 'Machine' here is abstract: a precise description of an algorithm that could be implemented in hardware or software. The machines are meant to recognize languages, that is, to answer yes or no for each input string."),
  T("A deterministic finite automaton, or DFA, is a five-part description: a finite set of states S, an alphabet A, a start state s0, a transition function delta from S times A to S, and a set F of final or accepting states. You feed it a string. It starts in s0 and for each symbol moves to the state delta says."),
  M(r"\hat\delta(s, \varepsilon) = s, \qquad \hat\delta(s, ax) = \hat\delta(\delta(s, a), x)"),
  T("Read the second line as: a string made of a first symbol a followed by the rest x. Take one step on a, then process x from the new state. A correction to the source: the notes print this as xa, which as written would apply the last symbol first; the version here, with the first symbol peeled off, is the standard one and matches how machines actually run. Either way the idea is one application of delta per symbol. The language of the machine is every string that ends up in a final state."),
  M(r"L(M) = \{\, x \in A^{*} \mid \hat\delta(s_0, x) \in F \,\}"),
  T("Example. A two-state machine tracks whether the number of ones seen so far is even. The start state is even and also final. A zero keeps the state, a one swaps the states. It accepts exactly the strings with an even number of ones. This is a recognizer for that language, and also a function from strings to zero and one."),
  T("Generalization one: nondeterminism. An NFA has the same five parts, but delta now returns a set of states, possibly empty. For a symbol the machine may go to any member of the set, as if it could try all choices at once. The string is accepted if the set of states reachable at the end contains a final state."),
  T("A surprising fact: NFAs add no power. A language is accepted by some DFA if and only if it is accepted by some NFA. The proof, left as an exercise in the notes, builds a DFA whose states are sets of NFA states. The price is size: an NFA with n states may need a DFA with 2 to the n states. NFAs are easy to write down, but DFAs can be run directly."),
  T("Generalization two: epsilon moves. The machine may also change state without reading input. Then delta takes a state and either a symbol or epsilon. To run it, you add to every state set all the states reachable by epsilon moves alone, called the epsilon closure. The notes leave the exact definitions and the equal-power proof as exercises, and the labs below carry them out."),
  T("A summary of the logic. Three machine kinds, one class of languages. In chapter 4 you will meet the matching notation, regular expressions. In the practice section you implement all three machine kinds and measure how many DFA states the subset construction really produces.")],
 [("What does a DFA's transition function give?", ["A set of states", "Exactly one next state", "A string", "A probability"], 1, "Determinism: one successor per state and symbol."),
  ("When does an NFA accept a string?", ["When every path ends in a final state", "When some path ends in a final state", "When no path exists", "When the string is empty"], 1, "It suffices that the reachable set meets F."),
  ("Do NFAs recognize more languages than DFAs?", ["Yes", "No, the same class", "Only with epsilon moves", "Only finite ones"], 1, "They can be converted to DFAs."),
  ("How many DFA states might an n-state NFA need?", ["n", "2n", "Up to 2^n", "n squared"], 2, "Subsets of the NFA states.")],
 [("What is F?", "The set of final (accepting) states."), ("What is an epsilon move?", "A transition that reads no input."), ("Why use an NFA?", "It is shorter to write down."),
  ("Why use a DFA?", "It can be implemented directly.")],
 [PL("Run a DFA", "States are numbered from 0; the start state is 0. The table gives, for each state, the next state for symbols 0 and 1: table[state][symbol]. Write dfa_accepts(table, finals, s) for a binary string s: true if the machine ends in a state in finals.",
     "dfa_accepts(table, finals, s)", """
def dfa_accepts(table, finals, s):
    state = 0
    for c in s:
        state = table[state][int(c)]
    return state in finals
""", [[[[0, 1], [1, 0]], [0], "0110"], [[[0, 1], [1, 0]], [0], "1011"], [[[0, 1], [1, 0]], [0], ""], [[[1, 0], [1, 2], [1, 0]], [2], "0101"], [[[1, 0], [1, 2], [1, 0]], [2], "1010"], [[[1, 0], [1, 2], [1, 0]], [2], "01"]], "Start in state 0 and follow table[state][int(c)] for each symbol."),
  PL("Run an NFA", "Now table[state][symbol] is a list of possible next states. Write nfa_accepts(table, finals, s): keep the list of all states you could be in, and accept if one of them is final at the end.",
     "nfa_accepts(table, finals, s)", """
def nfa_accepts(table, finals, s):
    cur = [0]
    for c in s:
        nxt = []
        for q in cur:
            for r in table[q][int(c)]:
                if r not in nxt:
                    nxt.append(r)
        cur = nxt
    for q in cur:
        if q in finals:
            return True
    return False
""", [[[[[0], [0, 1]], [[2], [2]], [[3], [3]], [[], []]], [3], "100"], [[[[0], [0, 1]], [[2], [2]], [[3], [3]], [[], []]], [3], "0100"], [[[[0], [0, 1]], [[2], [2]], [[3], [3]], [[], []]], [3], "011"], [[[[0], [0, 1]], [[2], [2]], [[3], [3]], [[], []]], [3], ""]], "Track the set of current states; an empty set means the run died."),
  PL("NFA with epsilon moves", "Each row now has three entries: next states on 0, on 1, and on epsilon (the last entry). Write nfa_eps_accepts(table, finals, s). Before reading anything, and after each symbol, add every state reachable by epsilon moves (the closure).",
     "nfa_eps_accepts(table, finals, s)", """
def nfa_eps_accepts(table, finals, s):
    def closure(states):
        out = list(states)
        i = 0
        while i < len(out):
            q = out[i]
            i += 1
            for r in table[q][len(table[q]) - 1]:
                if r not in out:
                    out.append(r)
        return out
    cur = closure([0])
    for c in s:
        nxt = []
        for q in cur:
            for r in table[q][int(c)]:
                if r not in nxt:
                    nxt.append(r)
        cur = closure(nxt)
    for q in cur:
        if q in finals:
            return True
    return False
""", [[[[[0], [], [1]], [[], [1], []]], [1], "0011"], [[[[0], [], [1]], [[], [1], []]], [1], ""], [[[[0], [], [1]], [[], [1], []]], [1], "10"], [[[[0], [], [1]], [[], [1], []]], [1], "0101"], [[[[0], [], [1]], [[], [1], []]], [1], "111"]], "Write a helper that grows a list with epsilon successors until nothing new appears."),
  PL("Count DFA states", "Write subset_count(table): the number of different sets of NFA states that can be reached from {0} by reading symbols (the states of the DFA made by the subset construction), including the start set. table[state][symbol] lists the next states; there are no epsilon moves.",
     "subset_count(table)", """
def subset_count(table):
    nsym = len(table[0])
    start = [0]
    seen = [start]
    todo = [start]
    while todo:
        cur = todo.pop()
        for a in range(nsym):
            nxt = []
            for q in cur:
                for r in table[q][a]:
                    if r not in nxt:
                        nxt.append(r)
            nxt.sort()
            if nxt not in seen:
                seen.append(nxt)
                todo.append(nxt)
    return len(seen)
""", [[[[[0], [0, 1]], [[2], [2]], [[3], [3]], [[], []]]], [[[[0], [1]], [[1], [0]]]], [[[[0, 1], [0]], [[], [1]]]]], "Keep a list of seen sorted state lists and expand each new one."),
  MATCH("Machines", "Match each machine feature with its meaning.", [("delta in a DFA", "Exactly one next state"), ("delta in an NFA", "A set of next states"), ("Epsilon move", "Change state with no input"), ("Final state", "Accepting at the end of the string"), ("Subset construction", "Turns an NFA into a DFA")]),
  FILL("Finite automata", "A DFA accepts a string when it ends in a {{final|accepting}} state. An NFA with n states may need up to {{2^n}} DFA states. DFAs and NFAs recognize the {{same}} class of languages.")]))

# ------------------------------------------------------------ 4
CHS.append(CH(
 "Regular expressions and languages",
 ("Describing regular languages", [
  "Regular expression | represents | Regular set",
  "Union | combines | Two languages",
  "Concatenation | joins | Languages",
  "Star | repeats | A language",
  "Regular language | equals | Finite automaton language",
  "Thompson style proof | uses | NFAs with epsilon moves",
  "State elimination proof | uses | R sets of paths"]),
 ["A regular expression is built from the empty set, the empty string and single symbols using union, concatenation and star, and nothing else. Each one represents a regular set of strings.",
  "The central theorem says that regular languages are exactly the languages of finite automata. One direction builds an NFA by induction on the expression. The other builds an expression from a DFA by tracking paths that avoid higher-numbered states.",
  "Regular expressions generate the strings of a language; automata recognize them. The two views are interchangeable."],
 [("Regular expression", "A formula built from the empty set, epsilon and symbols with union, concatenation and star."),
  ("Regular set", "The set of strings a regular expression represents."),
  ("Union", "R union S: strings in either set. Written r + s in the notes."),
  ("Concatenation", "RS: a string from R followed by one from S."),
  ("Kleene star", "R star: zero or more strings from R joined together."),
  ("Path set R^k_ij", "Strings that take the machine from state i to state j without passing through states numbered k or higher in between.")],
 ["Regular expressions: empty set, epsilon, a, and r + s, rs, r*.",
  "Regular sets: the empty set, {epsilon}, {a}, R union S, RS, R*.",
  "A language is regular iff it is accepted by some finite automaton.",
  "Expression to machine: induction on the expression, with epsilon moves.",
  "Machine to expression: R^(k+1)_ij = R^k_ij union R^k_ik (R^k_kk)* R^k_kj.",
  "Many tools use regular expressions, for example the 're' in grep."],
 [T("Finite automata recognize languages. We also want a concise way to describe such a language, and a way to generate its strings instead of testing candidates one by one. Regular expressions do that. The languages they describe are called regular languages, or regular sets of strings."),
  T("The definition is inductive. Over an alphabet A, the following are regular expressions: the empty set, the empty string epsilon, and any single symbol a. If r and s are regular expressions, so are r plus s, rs and r star. Nothing else is. The plus means union in these notes, as in many theory texts; most programming tools write a vertical bar for it."),
  M(r"r + s \;\mapsto\; R \cup S, \qquad rs \;\mapsto\; RS, \qquad r^{*} \;\mapsto\; R^{*}"),
  T("Example from the notes. The expression 00 plus 11, starred, followed by 101 plus 110 describes strings made of any number of 00 or 11 blocks and then ending in 101 or 110. Its set begins 101, 110, 00101, 00110, 11101, 11110, 0000101 and so on. The string 00110011110 is in it: blocks 00, 11, 00, 11 and then 110. The string 00111100101110 is not: it ends in 110, which would leave a prefix of odd length, but the blocks 00 and 11 always have even total length."),
  T("The first big theorem: a language is regular if and only if it is the language of some finite automaton. The proof has two halves. Part one goes from expression to machine by induction on the size of the expression. The base cases are the empty set, epsilon and a single symbol, each a tiny machine. For the inductive step you combine machines for R and S into machines for R union S, RS and R star, using NFAs with epsilon moves."),
  T("Part two goes from machine to expression. Number the states s0 to s(n minus 1) of a DFA. Let R^k_ij be the set of strings that take the machine from state i to state j without going through any intermediate state numbered k or higher. At k equal to zero these are single symbols (and epsilon when i equals j). Then add one more allowed state at a time:"),
  M(r"R^{k+1}_{ij} = R^{k}_{ij} \,\cup\, R^{k}_{ik}\,\bigl(R^{k}_{kk}\bigr)^{*}\,R^{k}_{kj}"),
  T("Read this as: to go from i to j allowing state k, either you never visit k, or you go from i to k, loop around k any number of times, and then go from k to j. At k equal to n, every state is allowed, and the language of the machine is the union of R^n_0j over all final states j. By induction each set has a regular expression, which completes the proof. The notes leave verifying the details as an exercise."),
  T("Why this matters. Regular expressions are compact, the tools for them are everywhere, and much theory is known. The notes show a protein motif described by a pattern very much like a regular expression, which hints at uses in biology. Chapter 6 shows that regular expressions are not enough for every pattern, for example balanced parentheses.")],
 [("What does r + s mean in these notes?", ["Concatenation", "Union", "Star", "Intersection"], 1, "The plus is the union operator."),
  ("What is the language of a finite automaton called?", ["Context free", "Regular", "Recursive", "Context sensitive"], 1, "Regular languages equal DFA languages."),
  ("How is a regular expression turned into a machine?", ["By induction on its size, using NFAs with epsilon moves", "By running it", "By sorting symbols", "Not possible"], 0, "Base cases and three combining constructions."),
  ("What does R^k_ij avoid?", ["Final states", "Intermediate states numbered k or higher", "The start state", "Loops"], 1, "That is the induction parameter.")],
 [("What does r* represent?", "Zero or more repeats of strings in R."), ("Does the pattern need epsilon?", "Yes, as a base case."), ("Is 00110011110 in (00+11)*(101+110)?", "Yes."),
  ("What does the 're' in grep mean?", "Regular expression.")],
 [PL("Regular expression matcher", "Write re_match(r, s): true if the whole string s is in the language of the regular expression r. Syntax: letters or digits are symbols, + is union, writing two things next to each other is concatenation, * is star (binds tightest), parentheses group, and () is epsilon.",
     "re_match(r, s)", """
def re_match(r, s):
    pos = [0]
    def peek():
        if pos[0] < len(r):
            return r[pos[0]]
        return ''
    def expr():
        left = term()
        while peek() == '+':
            pos[0] += 1
            right = term()
            left = ('u', left, right)
        return left
    def term():
        node = ('e',)
        while peek() != '' and peek() != '+' and peek() != ')':
            f = factor()
            node = ('c', node, f)
        return node
    def factor():
        a = atom()
        while peek() == '*':
            pos[0] += 1
            a = ('s', a)
        return a
    def atom():
        c = peek()
        pos[0] += 1
        if c == '(':
            n = expr()
            pos[0] += 1
            return n
        return ('l', c)
    tree = expr()
    def ends(node, i):
        k = node[0]
        if k == 'e':
            return [i]
        if k == 'l':
            if i < len(s) and s[i] == node[1]:
                return [i + 1]
            return []
        if k == 'u':
            out = ends(node[1], i)
            for e in ends(node[2], i):
                if e not in out:
                    out.append(e)
            return out
        if k == 'c':
            out = []
            for j in ends(node[1], i):
                for e in ends(node[2], j):
                    if e not in out:
                        out.append(e)
            return out
        seen = [i]
        todo = [i]
        while todo:
            j = todo.pop()
            for e in ends(node[1], j):
                if e not in seen:
                    seen.append(e)
                    todo.append(e)
        return seen
    return len(s) in ends(tree, 0)
""", [["(00+11)*(101+110)", "101"], ["(00+11)*(101+110)", "00110011110"], ["(00+11)*(101+110)", "00111100101110"], ["(00+11)*(101+110)", "0000101"], ["(00+11)*(101+110)", "1"], ["(a+b)*abb", "babb"], ["(a+b)*abb", "ab"], ["(ab)*", ""], ["a(b+c)*", "abcbc"], ["a*", "b"]], "Parse into a tree (union, concatenation, star, symbol), then compute for each node the set of positions where a match can end."),
  PL("Shortest accepted string", "A DFA over the binary alphabet is given as table[state][symbol], start state 0, with a list of final states. Write shortest_accepted(table, finals): the shortest string it accepts (the empty string if the start state is final); among strings of the same length, the one that tries symbol 0 before 1 first. Return \"none\" if no string is accepted.",
     "shortest_accepted(table, finals)", """
def shortest_accepted(table, finals):
    nsym = len(table[0])
    seen = [0]
    queue = [[0, ""]]
    head = 0
    while head < len(queue):
        state = queue[head][0]
        word = queue[head][1]
        head += 1
        if state in finals:
            return word
        for a in range(nsym):
            nxt = table[state][a]
            if nxt not in seen:
                seen.append(nxt)
                queue.append([nxt, word + str(a)])
    return "none"
""", [[[[0, 1], [1, 0]], [1]], [[[0, 1], [1, 0]], [0]], [[[1, 0], [1, 2], [1, 0]], [2]], [[[0, 0], [1, 1]], [1]]], "Do a breadth-first search over states, remembering the word that reached each state."),
  MATCH("Operators", "Match each construct with the set it makes.", [("r + s", "Union R or S"), ("rs", "Concatenation RS"), ("r*", "Zero or more repeats"), ("epsilon", "Only the empty string"), ("empty set", "No strings at all")]),
  FILL("Regular", "A language is regular exactly when a {{finite}} automaton accepts it. The three operations are union, {{concatenation}} and {{star|Kleene star}}. The expression r + s means {{union}}.")]))
