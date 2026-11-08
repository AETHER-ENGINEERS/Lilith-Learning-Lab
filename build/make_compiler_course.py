#!/usr/bin/env python3
"""Build the Compiler Design course. Usage: python3 make_compiler_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "cd"))
import c1, c2, c3  # noqa: E402
from make_trinity_course import split_long, stack  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "cd", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {   # plain substring replacement in the app: avoid short keys that sit inside other words
    "lexemes": "lex eems", "lexeme": "lex eem", "lexer": "lex er", "Kleene": "klay nee", "ε": "epsilon",
    "SLR(1)": "S L R one", "LALR(1)": "L A L R one", "LL(1)": "L L one", "LR(1)": "L R one", "LL(k)": "L L k", "LR(k)": "L R k",
    "LALR": "L A L R", "SLR": "S L R", "CFG": "C F G", "ASTs": "A S Ts", "DAG": "dag", "SDT": "S D T",
    "CISC": "sisk", "RISC": "risk", "DFA": "D F A", "NFA": "N F A", "l-value": "L value", "r-value": "R value",
    "L-attributed": "L attributed", "S-attributed": "S attributed", "getReg": "get reg", "Algol": "al gol", "peephole": "peep hole",
    "Tutorialspoint": "tutorials point", "scanf": "scan eff", "printf": "print eff", "JNZ": "jump if not zero", "SHL": "shift left",
    "GOTO": "go to", "goto": "go to",
}

SANDBOX = {
    "type": "terminal", "title": "Compiler lookup", "prompt": "cc>",
    "intro": "A scripted lookup, not a real compiler. Try: phases, tokens, parsers, ir, opt, help",
    "chips": ["phases", "tokens", "parsers", "ir", "opt", "help"],
    "commands": [
        {"re": "^help$", "out": ["phases   the phases of a compiler", "tokens   what a lexer produces for int x = 5;", "parsers  top-down and bottom-up parsing", "ir       three-address code example", "opt      optimizations at a glance"]},
        {"re": "^phases$", "out": ["lexical -> syntax -> semantic -> intermediate code -> optimization -> code generation", "symbol table and error handling are used by every phase"]},
        {"re": "^tokens$", "out": ["int x = 5;", "KEYWORD int | ID x | OP = | NUM 5 | PUNCT ;"]},
        {"re": "^parsers$", "out": ["top-down: recursive descent, LL(1). Left-most derivation.", "bottom-up: shift-reduce, LR. Right-most derivation in reverse."]},
        {"re": "^ir$", "out": ["a = b + c * d", "t1 = c * d", "t2 = b + t1", "a = t2"]},
        {"re": "^opt$", "out": ["peephole, strength reduction (x*2 -> x<<1), dead code elimination,", "loop-invariant code motion, common sub-expression elimination"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "warn"}],
    "tasks": []
}

EXAM = [
    ("What must a compiler preserve?", ["Speed", "The meaning of the program", "Variable names", "Comments"], 1, "Translation must not change what the program means."),
    ("Which tool merges object files into an executable?", ["Assembler", "Linker", "Loader", "Preprocessor"], 1, "It resolves references between modules."),
    ("What is the front end of a compiler?", ["The analysis phase", "The synthesis phase", "The linker", "The loader"], 0, "It reads and checks the source."),
    ("What does the lexical analyzer produce?", ["A parse tree", "Tokens", "Machine code", "A symbol table only"], 1, "Pairs of token name and attribute."),
    ("How is intvalue scanned by the longest match rule?", ["Keyword int then value", "One identifier", "Two numbers", "An error"], 1, "The longest lexeme wins."),
    ("Which operator has the highest precedence in regular expressions?", ["Union", "Concatenation", "Kleene star", "Question mark"], 2, "Star, then concatenation, then union."),
    ("What does x+ mean?", ["Zero or more x", "One or more x", "At most one x", "Exactly one x"], 1, "It equals x followed by x star."),
    ("A finite automaton accepts a string when...", ["It ends in a final state", "It is short", "It starts in a final state only", "It has no transitions"], 0, "The input is consumed and the state is final."),
    ("Why can't a lexer check balanced parentheses?", ["Regular expressions cannot count nesting", "They are not tokens", "It is too slow", "It has no input"], 0, "A context-free grammar is needed."),
    ("When is a grammar ambiguous?", ["It has epsilon", "Some string has two parse trees", "It has no terminals", "It is left recursive"], 1, "Precedence or a rewrite removes it."),
    ("Which grammar feature can make a top-down parser loop forever?", ["Left recursion", "Epsilon", "Terminals", "Parentheses"], 0, "It keeps expanding the same non-terminal."),
    ("Left-factor A to a b | a c.", ["A to a A', A' to b | c", "A to b | c", "A to a b c", "A to A a"], 0, "Pull out the common prefix."),
    ("What marks the end of input for a predictive parser?", ["epsilon", "$", "id", "nothing"], 1, "The stack also has it at the bottom."),
    ("In LL(1), what does the second L stand for?", ["Look-ahead", "Left-most derivation", "Longest match", "Linked list"], 1, "The first L is left-to-right scanning."),
    ("What does a reduce step do in a shift-reduce parser?", ["Reads a token", "Replaces a handle by its left side", "Reports an error", "Ends the parse"], 1, "It is a production applied in reverse."),
    ("What does panic mode do?", ["Inserts tokens", "Skips input up to a delimiter", "Restarts compiling", "Ignores errors forever"], 1, "It resumes after the semicolon."),
    ("Which attributes take values from child nodes?", ["Inherited", "Synthesized", "Global", "Static"], 1, "S-attributed definitions use only these."),
    ("Which is a semantic error?", ["Missing semicolon", "Assigning a string to an int", "Misspelled keyword", "Unbalanced bracket"], 1, "The syntax is fine; the types are wrong."),
    ("Where are activation records kept?", ["Heap", "Control stack", "Object file", "Symbol table"], 1, "Calls nest last in, first out."),
    ("With pass by value, a change to the formal parameter...", ["Changes the actual parameter", "Does not change the actual parameter", "Is an error", "Changes globals"], 1, "Only the r-value was copied."),
    ("What does lookup return for a name that is not in the table?", ["The type", "0", "An exception", "The scope"], 1, "By the tutorial's convention."),
    ("How many addresses does three-address code have at most?", ["One", "Two", "Three", "Four"], 2, "Hence the name."),
    ("What problem do triples have?", ["No operator field", "Reordering breaks positional references", "They need registers", "They are machine dependent"], 1, "Indirect triples use pointers."),
    ("x * 2 replaced by x << 1 is an example of...", ["Dead-code elimination", "Strength reduction", "Left factoring", "Linking"], 1, "A cheaper operation with the same result."),
    ("What does a DAG for a basic block expose?", ["Common sub-expressions", "Syntax errors", "Tokens", "Comments"], 0, "Shared nodes are computed once."),
    ("Which statements are leaders of basic blocks?", ["Only the first", "The first, branch targets and statements after a branch", "Every statement", "Only labels"], 1, "Each leader starts a new block."),
    ("What is loop-invariant code?", ["Code that never executes", "Code computing the same value every iteration", "Code with a goto", "Dead code"], 1, "It can be moved out of the loop."),
    ("What does code motion fix?", ["Partial redundancy", "Syntax errors", "Left recursion", "Token spelling"], 0, "Compute the shared value once on every path."),
]


def build():
    chapters = c1.CHS + c2.CHS + c3.CHS
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__PARSER__": app("parser.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "compiler-design",
        "title": "Compiler Design",
        "subtitle": "Theory and practice, with Python labs",
        "author": "Lilith Learning Lab",
        "description": "A 17-chapter course based on the Tutorialspoint Compiler Design tutorial: compiler architecture and phases, lexical analysis, regular expressions, finite automata, syntax analysis, top-down and bottom-up parsing, error recovery, semantic analysis, runtime environments, symbol tables, intermediate code, code generation and optimization. Python labs run on the built-in MicroPython engine; each lab builds a small working version of a compiler component. Known errors in the source tutorial are corrected and flagged in the lessons.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: Compiler Design", "passMark": 70, "size": 20,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "compiler-design.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
