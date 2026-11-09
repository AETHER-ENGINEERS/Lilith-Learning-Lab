#!/usr/bin/env python3
"""Build the Theory of Computation course. Usage: python3 make_theory_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tc"))
import toc1, toc2, toc3  # noqa: E402
from make_trinity_course import split_long, stack  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "tc", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {
    "Kleene": "klay nee", "Chomsky": "chom ski", "Markov": "mar kov", "Gödel": "gur dull", "Kolmogorov": "kol mo gor off",
    "Chaitin": "chay tin", "Wittgenstein": "vit gen stine", "Crutchfield": "crutch field", "Entscheidungsproblem": "ent shy doongs problem",
    "NP-complete": "N P complete", "NP-completeness": "N P completeness", "ASCII": "ask ee", "RNP-1": "R N P one", "tRNA": "t R N A",
    "yacc": "yak", "Bison": "bison", "Tom Carter": "Tom Carter", "ε": "epsilon", "∅": "the empty set", "δ": "delta",
    "DFAs": "D F As", "NFAs": "N F As", "DFA": "D F A", "NFA": "N F A", "PDAs": "P D As", "PDA": "P D A", "UTM": "U T M",
    "RSA": "R S A", "DNA": "D N A", "Theta": "theta", "Sigma": "sigma",
}

SANDBOX = {
    "type": "terminal", "title": "Computation lookup", "prompt": "toc>",
    "intro": "A scripted lookup, not a real machine. Try: hierarchy, dfa, tm, halting, classes, help",
    "chips": ["hierarchy", "dfa", "tm", "halting", "classes", "help"],
    "commands": [
        {"re": "^help$", "out": ["hierarchy  the Chomsky hierarchy", "dfa        the parts of a finite automaton", "tm         the parts of a Turing machine", "halting    the halting problem in one line", "classes    P, NP and NP-complete"]},
        {"re": "^hierarchy$", "out": ["regular < deterministic context free < context free < context sensitive < recursive < recursively enumerable", "machines: finite automaton, DPDA, PDA, linear bounded automaton, halting TM, TM"]},
        {"re": "^dfa$", "out": ["M = (S, A, s0, delta, F): states, alphabet, start, transition function, final states"]},
        {"re": "^tm$", "out": ["T = (S, A, delta, s0, b, F): delta maps (state, symbol) to (state, symbol, L or R)"]},
        {"re": "^halting$", "out": ["No algorithm decides, for every machine and input, whether the machine halts. Running it is the only sure way to see that it does."]},
        {"re": "^classes$", "out": ["P: solvable in polynomial time. NP: solutions checkable in polynomial time. NP-complete: hardest in NP. Is P = NP? Open."]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "err"}],
    "tasks": []
}

EXAM = [
 ("What is a language over an alphabet A?", ["A finite set of symbols", "Any subset of A star", "A grammar", "A single string"], 1, "A language is a set of strings."),
 ("What is the length of the string aabbcc?", ["3", "6", "12", "0"], 1, "Repeated symbols are counted."),
 ("Which is true of the empty string?", ["It is the empty set", "It has length zero", "It is not in A star", "It is a symbol"], 1, "Epsilon is a string of length 0."),
 ("What does Cantor's argument show about a power set?", ["P(S) is smaller than S", "P(S) is strictly larger than S", "They are equal", "P(S) is empty"], 1, "No function from S onto P(S) exists."),
 ("Why are there languages no program can recognize?", ["Programs are too slow", "Countably many programs but uncountably many languages", "All languages are finite", "Computers are physical"], 1, "Counting argument."),
 ("Which set is NOT countable?", ["The integers", "The rationals", "The real numbers", "A star for a finite alphabet"], 2, "R is the same size as P(N)."),
 ("What does a DFA's transition function return?", ["A set of states", "Exactly one state", "A symbol", "A number"], 1, "Determinism."),
 ("When does an NFA accept?", ["When every path reaches a final state", "When some path reaches a final state", "When the string is empty", "Never"], 1, "One accepting path is enough."),
 ("How many DFA states might an n-state NFA need?", ["n", "n squared", "Up to 2^n", "Always 2n"], 2, "Subsets of states."),
 ("DFAs, NFAs and NFAs with epsilon moves recognize...", ["Different classes", "The same class of languages", "Only finite languages", "Only context free languages"], 1, "The regular languages."),
 ("What does r + s mean in a regular expression (in these notes)?", ["Concatenation", "Union", "Star", "Complement"], 1, "Plus is union."),
 ("Is 00110011110 in (00+11)*(101+110)?", ["Yes", "No", "Only with epsilon", "Undefined"], 0, "00 11 00 11 then 110."),
 ("Which direction of the regular-language theorem uses R^k_ij?", ["Expression to machine", "Machine to expression", "Neither", "Both"], 1, "State elimination along paths."),
 ("Each row of a Markov transition matrix...", ["Sums to 1", "Sums to 0", "Is sorted", "Is the identity"], 0, "The system must go somewhere."),
 ("What gives n-step transition probabilities?", ["n times T", "T to the power n", "The determinant", "The trace"], 1, "Matrix powers."),
 ("What is a stationary distribution?", ["A vector unchanged by one step", "The first row of T", "All zeros", "A final state"], 0, "vT = v."),
 ("Which language is context free but not regular?", ["Even number of ones", "Balanced parentheses", "Strings ending in 01", "All strings"], 1, "Counting nesting needs a stack."),
 ("A production A -> alpha in a context free grammar has...", ["A single variable on the left", "Terminals on the left", "A stack", "No right side"], 0, "That is what context free means."),
 ("Which machine recognizes context free languages?", ["DFA", "Pushdown automaton", "Markov model", "Counter"], 1, "A finite automaton plus a stack."),
 ("What shape of rules makes a grammar regular?", ["Right-linear rules", "Any rules", "Rules with two variables", "Rules with no terminals"], 0, "At most one variable, at the right end."),
 ("What do grep, lex and yacc have in common?", ["They all use recognizers built from patterns or grammars", "They are compilers", "They are Turing machines", "They are Markov models"], 0, "Tools from regular expressions and grammars."),
 ("Which machine matches context sensitive languages?", ["Finite automaton", "Pushdown automaton", "Linear bounded automaton", "Markov model"], 2, "A Turing machine bounded by the input."),
 ("Which is the strongest class in the hierarchy?", ["Regular", "Context free", "Recursive", "Recursively enumerable"], 3, "Accepted by general Turing machines."),
 ("A Turing machine halts on every input. Its language is...", ["Regular", "Recursive", "Finite", "Empty"], 1, "A decider."),
 ("What does a Turing machine's delta return?", ["A state only", "A new state, a symbol and a direction", "A number", "A set of states"], 1, "State, write, move."),
 ("What does a universal Turing machine do?", ["Decides halting", "Simulates any machine from its encoding", "Always halts", "Sorts the tape"], 1, "Program as data."),
 ("What is true of the halting problem?", ["It is solved by a fast algorithm", "No algorithm decides it for all machines and inputs", "It is solved for finite tapes", "It is NP-complete"], 1, "Turing's theorem."),
 ("How can you be sure a machine halts?", ["Run it and see it halt", "Read its code", "Count states", "You never can"], 0, "Halting is confirmed by running."),
 ("What does g in O(f) mean?", ["g is at most c times f for all large n", "g equals f", "g is always smaller than f", "g is constant"], 0, "Up to a constant, eventually."),
 ("What does NP mean here?", ["Not polynomial", "Solutions can be checked in polynomial time", "No problem", "Nondeterministic Turing machine only"], 1, "Verification is cheap."),
 ("What does NP-complete mean?", ["Hardest problems in NP", "Problems outside NP", "Problems in P only", "Unsolvable problems"], 0, "Every NP problem translates to it."),
 ("Which problem is NP-complete in the notes?", ["Boolean satisfiability", "Primality testing", "Sorting", "Halting"], 0, "SAT."),
 ("Why is factoring important to cryptography?", ["It is easy", "It is hard for large numbers, which RSA relies on", "It is undecidable", "It is NP-complete for sure"], 1, "Security rests on its apparent difficulty."),
 ("Why does entropy of a string depend on a model?", ["Strings have no information", "Different probability models give different values", "It is always zero", "It is always the length"], 1, "Entropy is relative to a model."),
 ("Why is computational complexity noncomputable?", ["It needs infinite strings", "It would require solving the halting problem", "UTMs differ", "It is random"], 1, "You cannot tell which programs halt with the right output."),
]


def build():
    chapters = toc1.CHS + toc2.CHS + toc3.CHS
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__TM__": app("tm.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "theory-of-computation",
        "title": "Theory of Computation",
        "subtitle": "Automata, grammars, Turing machines and complexity",
        "author": "Lilith Learning Lab",
        "description": "A 12-chapter course based on Tom Carter's 2005 notes Introduction to the theory of computation (Complex Systems Summer School): strings and languages, countability, finite automata, regular expressions, Markov models, context free grammars, recognizers and generators, the Chomsky hierarchy, Turing machines, universal machines and the halting problem, computability and tractability (big-O, NP, satisfiability), and computational complexity of strings. Python labs run on the built-in MicroPython engine and build small working versions of each idea. A few imprecise statements in the notes are corrected and flagged in the lessons.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: Theory of Computation", "passMark": 70, "size": 20,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "theory-of-computation.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
