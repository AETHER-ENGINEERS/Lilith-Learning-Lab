"""Theory of Computation course, chapters 5-8."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 5
CHS.append(CH(
 "Markov models",
 ("Probabilistic machines", [
  "Markov model | resembles | Finite automaton",
  "Transition | is chosen | By probability",
  "Transition matrix | has | Rows summing to one",
  "T squared | gives | Two step probabilities",
  "Long run | gives | Stationary distribution",
  "Hidden Markov model | emits | Symbols from states"]),
 ["A Markov model is like a finite automaton in which the next state is chosen by probabilities instead of by input. It usually has no final states; it runs by itself and may emit a symbol at each step, so it produces strings instead of reading them.",
  "It is described by a transition matrix T whose entry in row i and column j is the probability of going from state i to state j. Rows sum to one. Multiplying the matrix by itself gives probabilities over several steps.",
  "Run for very many steps, many chains settle to a stationary distribution. In a hidden Markov model you see only the emitted symbols, not the states."],
 [("Markov model", "A system with finitely many states in which the next state depends only on the current one, chosen by fixed probabilities."),
  ("Transition matrix", "The matrix T with T[i][j] = probability of moving from state i to state j."),
  ("Stochastic row", "A row of probabilities between 0 and 1 that sum to 1."),
  ("Stationary distribution", "A distribution over states that does not change when one more step is taken."),
  ("Emission", "A symbol the system outputs from a state or a transition."),
  ("Hidden Markov model", "A Markov model whose states cannot be observed directly, only the symbols they emit.")],
 ["A Markov model has states and probabilistic transitions, usually no accepting states.",
  "Row i of T gives the probabilities of the next state from state i; each row sums to 1.",
  "Probabilities after n steps are given by T^n.",
  "The long-run behaviour is linked to eigenvectors of T.",
  "Markov models are used for DNA sequences; hidden Markov models for genome analysis.",
  "The model has no input; randomness replaces it."],
 [T("An important relative of finite automata is the Markov model, often called a Markov chain. The structure is similar: a finite set of states and transitions between them. The difference is that transitions are chosen by probabilities, and there are usually no final or accepting states."),
  T("To keep track of what the system is doing, we let it emit a symbol, either per transition or per state reached. These machines take no input except whatever drives the probabilities, but they give output strings. Markov models are therefore natural models of discrete dynamical systems: a finite state set and a chance of moving from any state to any other."),
  T("The usual specification is the transition matrix T. Entry p_ij is the probability of going from state i to state j in the next time step. Every entry lies between 0 and 1 and every row sums to 1, since the system must go somewhere."),
  M(r"T = \begin{pmatrix} p_{11} & \cdots & p_{1n} \\ \vdots & \ddots & \vdots \\ p_{n1} & \cdots & p_{nn} \end{pmatrix}, \qquad \sum_j p_{ij} = 1"),
  T("Probabilities over two steps are given by T squared. Check it: the probability of going from i to j in two steps is the sum over all middle states k of p_ik times p_kj. That sum is exactly the entry of the matrix product. Over n steps the probabilities are T to the n."),
  T("Two exercises in the notes point to the key ideas. First, run the system for a very long time. How would you estimate the relative frequency of each state? Answer: take a high power of T, or start from any distribution and keep applying T. For many chains the result approaches a stationary distribution, a vector v with v T equal to v."),
  T("Second, what do eigenvalues and eigenvectors of T tell you? The stationary distribution is a left eigenvector with eigenvalue one. The other eigenvalues control how fast the chain forgets where it started. These facts are standard and not proved in the notes; the labs here estimate them by repeated multiplication."),
  T("Examples in the notes. A generic Markov model for DNA sequences has one state per nucleotide, with transition probabilities estimated from data. A more elaborate model is a hidden Markov model: the system moves among hidden states, and what you observe is the emitted symbols. The notes only outline this; such models are widely used for analyzing genome sequences."),
  T("A caution about vocabulary. A Markov model is not a finite automaton, but its support, the transitions with nonzero probability, forms one. Where an automaton decides yes or no, a Markov model generates strings with probabilities attached.")],
 [("What must be true of each row of a transition matrix?", ["Sum to 1", "Sum to 0", "Contain only 1s", "Be sorted"], 0, "From any state the system must go somewhere."),
  ("What gives the n-step transition probabilities?", ["T times n", "T to the power n", "The inverse of T", "The sum of rows"], 1, "Matrix power."),
  ("What does a hidden Markov model hide?", ["The output", "The states", "The matrix size", "The probabilities"], 1, "You see only the emitted symbols."),
  ("How does a Markov model differ from a DFA?", ["Transitions are probabilistic and there is usually no input", "It has more states", "It cannot loop", "It has a stack"], 0, "Chance replaces input.")],
 [("What is T^2[i][j]?", "The probability of going from i to j in two steps."), ("Do Markov models take input?", "No, they generate output."), ("What is a stationary distribution?", "A distribution unchanged by a step: vT = v."),
  ("Where are they used?", "DNA sequence models, hidden Markov models for genomes.")],
 [PL("Is it a transition matrix?", "Write is_stochastic(T): true if every entry is between 0 and 1 (inclusive) and every row sums to 1 (within 1e-9).",
     "is_stochastic(T)", """
def is_stochastic(T):
    for row in T:
        total = 0.0
        for p in row:
            if p < 0 or p > 1:
                return False
            total += p
        if abs(total - 1.0) > 1e-9:
            return False
    return True
""", [[[[0.5, 0.5], [0.2, 0.8]]], [[[0.5, 0.6], [0.2, 0.8]]], [[[1, 0], [0, 1]]], [[[0.5, 0.5], [-0.1, 1.1]]]], "Check each probability and the sum of each row."),
  PL("Distribution after n steps", "A row vector v gives the probability of being in each state. One step makes the new vector v'[j] = sum over i of v[i] * T[i][j]. Write markov_after(T, v, n): the vector after n steps.",
     "markov_after(T, v, n)", """
def markov_after(T, v, n):
    k = len(v)
    for step in range(n):
        w = [0.0] * k
        for i in range(k):
            for j in range(k):
                w[j] += v[i] * T[i][j]
        v = w
    return v
""", [[[[0.9, 0.1], [0.5, 0.5]], [1.0, 0.0], 1], [[[0.9, 0.1], [0.5, 0.5]], [1.0, 0.0], 2], [[[0.9, 0.1], [0.5, 0.5]], [0.0, 1.0], 3], [[[0, 1], [1, 0]], [1.0, 0.0], 5]], "Apply one multiplication per step; build a new vector each time.", 1e-9),
  PL("Probability of a path", "Write seq_prob(T, start, seq): the probability that a chain starting in state start next visits the states in seq, in order. Multiply T[prev][next] along the way; an empty seq has probability 1.",
     "seq_prob(T, start, seq)", """
def seq_prob(T, start, seq):
    p = 1.0
    prev = start
    for s in seq:
        p *= T[prev][s]
        prev = s
    return p
""", [[[[0.9, 0.1], [0.5, 0.5]], 0, [0, 1]], [[[0.9, 0.1], [0.5, 0.5]], 1, [1, 1, 0]], [[[0.9, 0.1], [0.5, 0.5]], 0, []]], "Multiply one matrix entry per step.", 1e-9),
  PL("The long run", "Estimate the stationary distribution by starting from the uniform vector and applying T 500 times. Write stationary(T): the resulting vector with every entry rounded to 4 decimals.",
     "stationary(T)", """
def stationary(T):
    k = len(T)
    v = [1.0 / k] * k
    for step in range(500):
        w = [0.0] * k
        for i in range(k):
            for j in range(k):
                w[j] += v[i] * T[i][j]
        v = w
    out = []
    for x in v:
        out.append(round(x, 4))
    return out
""", [[[[0.9, 0.1], [0.5, 0.5]]], [[[0.5, 0.5], [0.5, 0.5]]], [[[0.5, 0.25, 0.25], [0.25, 0.5, 0.25], [0.25, 0.25, 0.5]]], [[[0.8, 0.2, 0.0], [0.1, 0.6, 0.3], [0.2, 0.2, 0.6]]]], "Repeat the one-step update 500 times.", 0.001),
  FILL("Markov models", "The rows of a transition matrix {{sum to 1|sum to one}}. The n-step probabilities are given by T to the {{n}}. In a hidden Markov model the {{states}} are not observed.")]))

# ------------------------------------------------------------ 6
CHS.append(CH(
 "Context free grammars and languages",
 ("Beyond regular", [
  "Grammar | has | Variables, terminals, start, productions",
  "Production | rewrites | One variable",
  "Derivation | generates | Strings",
  "Balanced parentheses | is | Context free not regular",
  "Palindromes | are | Context free not regular",
  "Regular | is contained in | Context free",
  "Pushdown automaton | recognizes | Context free languages"]),
 ["Some natural languages are not regular, for example balanced parentheses and palindromes. A larger class, the context free languages, is described by context free grammars: a start symbol and production rules that replace one variable by a string.",
  "Starting from the start symbol and applying productions, you generate the strings of the language. A derivation is a sequence of such steps ending in only terminals.",
  "Every regular language is context free, but not the reverse. To recognize context free languages, add a pushdown stack to a finite automaton: a pushdown automaton."],
 [("Context free grammar", "G = (V, T, S, P): variables, terminals, a start symbol and productions A to alpha."),
  ("Production", "A rule A to alpha, replacing the variable A by the string alpha."),
  ("Derivation", "A sequence of production applications; written alpha derives beta."),
  ("Context free language", "The language L(G) of terminal strings derivable from the start symbol."),
  ("Pushdown automaton", "A finite automaton with a stack."),
  ("Variable", "A symbol that occurs on the left of some production and must be rewritten."),
  ("Terminal", "A symbol of the final strings; never rewritten.")],
 ["A context free grammar is G = (V, T, S, P).",
  "A production is A -> alpha with A a single variable.",
  "L(G) = {w in T* : S derives w}.",
  "Balanced brackets: R -> epsilon | (R) | RR.",
  "Palindromes: R -> epsilon | a | b | aRa | bRb.",
  "Regular languages are context free; the converse fails."],
 [T("Regular languages are useful, but not every interesting language is regular. It is not hard to show that balanced parentheses and palindromes are not regular. Remember that a language is just a set of strings. A larger class, the context free languages, is more expressive, and a context free grammar specifies one."),
  T("Grammars play for context free languages the role that regular expressions play for regular ones: they generate strings of the language. A context free grammar G has two alphabets, the variables V and the terminals T, a start symbol S taken from V, and a finite set of production rules P. Each production has the form A arrow alpha, with A a single variable and alpha any string of variables and terminals."),
  T("A production is used like this. If a string contains a variable A somewhere, between a prefix gamma and a suffix delta, you may replace A by alpha and get gamma alpha delta. One application is written with a double arrow; zero or more applications are written with a starred double arrow. The language of the grammar is then every string made only of terminals that can be derived from the start symbol."),
  M(r"L(G) = \{\, w \in T^{*} \mid S \Rightarrow^{*} w \,\}"),
  T("Example one: balanced parentheses. The notes give S arrow R, then R arrow epsilon, R arrow open R close, and R arrow R R. The first rule is just a renaming and could be dropped. To derive the string open close open close, rewrite R to R R, then each R to open R close, then each remaining R to epsilon. The notes ask how to add square and curly brackets: just add the two extra productions R arrow square R square and R arrow curly R curly."),
  T("Example two: palindromes over a and b. R arrow epsilon or a or b, and R arrow aRa or bRb. Each use of aRa puts an a on both ends, so the string reads the same both ways. The notes ask for a grammar for algebraic expressions with x, y, plus, minus, times and parentheses; a standard one has an expression variable that is a sum of terms, a term that is a product of factors, and a factor that is x, y or a parenthesized expression."),
  T("Two facts the notes state as exercises. Every regular language is context free: a finite automaton turns into a grammar where each state is a variable and each transition on a is a rule X arrow aY, with epsilon rules for final states. And some context free languages are not regular, with balanced parentheses as the standard example, whose proof uses the pumping idea."),
  T("Now the recognizing side. A finite automaton cannot count nesting depth, because it has only finitely many states. Add a pushdown stack, an unbounded last-in first-out store, and it can: push on an open bracket, pop on a close bracket. Such machines are pushdown automata, or PDAs, and they recognize exactly the context free languages."),
  T("The notes give an example grammar for the RNP-1 protein motif. It has one rule per position: S arrow r W1 or k W1, W1 arrow g W2, W2 arrow one of a group of letters followed by W3, and so on up to W7. Every rule has at most one variable and it is at the right end. That shape is what shows the language is regular: a right-linear grammar is a finite automaton in disguise, with variables as states. The practice section implements this motif."),
  T("The notes also ask whether one could write a context free grammar for the structure of a tRNA molecule, which folds back on itself into stems. That is exactly the nested pairing a context free grammar is good at, in the same way matching brackets is. It is a pointer to biological uses, not a result.")],
 [("What does a production A -> alpha do?", ["Replaces variable A by alpha", "Reads input", "Deletes the grammar", "Counts symbols"], 0, "It rewrites one variable."),
  ("Which machine recognizes context free languages?", ["DFA", "NFA", "Pushdown automaton", "Markov model"], 2, "A finite automaton plus a stack."),
  ("Which language is not regular?", ["Strings ending in 01", "Balanced parentheses", "Even number of ones", "All strings"], 1, "Counting nesting needs unbounded memory."),
  ("What shape shows a grammar is regular?", ["Right-linear rules", "Many variables on the left", "Recursion", "Epsilon rules"], 0, "At most one variable, at the right end.")],
 [("What does R -> RR do?", "Concatenates two balanced strings."), ("Is every regular language context free?", "Yes."), ("What is the stack for?", "Counting nesting."),
  ("What is a derivation?", "A chain of productions from the start symbol.")],
 [PL("Balanced brackets", "Write balanced(s): true if every bracket in s is matched correctly. Brackets are (), [] and {}; the string contains only brackets. Use a stack: push opening brackets, and for a closing bracket pop and compare.",
     "balanced(s)", """
def balanced(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in '([{':
            stack.append(c)
        else:
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()
    return len(stack) == 0
""", [[""], ["()"], ["([]{})"], ["(]"], ["(()"], [")("], ["{[()()]}"]], "A stack lets you remember the nesting."),
  PL("Generate a grammar's language", "Rules are given as [left, right] pairs of strings; variables are upper-case letters, terminals anything else, the start symbol is \"S\", and an empty right side means epsilon. Write cfg_generate(rules, maxlen): the sorted list of every terminal string of length at most maxlen that can be derived, always rewriting the leftmost variable and discarding any sentential form longer than maxlen + 4 symbols.",
     "cfg_generate(rules, maxlen)", """
def cfg_generate(rules, maxlen):
    cap = maxlen + 4
    seen = set(['S'])
    todo = ['S']
    words = set()
    while todo:
        form = todo.pop()
        idx = -1
        for i in range(len(form)):
            if form[i].isupper():
                idx = i
                break
        if idx == -1:
            if len(form) <= maxlen:
                words.add(form)
            continue
        for r in rules:
            if r[0] == form[idx]:
                new = form[:idx] + r[1] + form[idx + 1:]
                if len(new) <= cap and new not in seen:
                    seen.add(new)
                    todo.append(new)
    out = list(words)
    out.sort()
    return out
""", [[[["S", "R"], ["R", ""], ["R", "(R)"], ["R", "RR"]], 4], [[["S", "R"], ["R", ""], ["R", "a"], ["R", "b"], ["R", "aRa"], ["R", "bRb"]], 3], [[["S", "aSb"], ["S", ""]], 6], [[["S", "aS"], ["S", "b"]], 3]], "Keep a stack of forms to expand; replace the leftmost variable with each matching rule's right side."),
  PL("A pushdown recognizer", "The language a^n b^n (n a's followed by exactly n b's, n may be 0) is context free but not regular. Write pda_anbn(s): push for each a, pop for each b, reject an a after a b, a b with an empty stack, or any other symbol, and accept if the stack is empty at the end.",
     "pda_anbn(s)", """
def pda_anbn(s):
    stack = []
    phase = 0
    for c in s:
        if c == 'a':
            if phase == 1:
                return False
            stack.append('A')
        elif c == 'b':
            phase = 1
            if not stack:
                return False
            stack.pop()
        else:
            return False
    return len(stack) == 0
""", [[""], ["ab"], ["aabb"], ["aab"], ["abab"], ["ba"], ["abb"], ["aaabbb"]], "A counter made from a stack: push per a, pop per b."),
  PL("The RNP-1 motif", "The motif grammar has one letter per position. Position 1: r or k. Position 2: g. Position 3: any of afilmnqstvwy. Position 4: any of agsci. Position 5: f or y. Position 6: any of liva. Position 7: any of acdefghiklmnpqrstvwy. Position 8: f, y or m. Write rnp1(s): true if s matches all eight positions exactly.",
     "rnp1(s)", """
def rnp1(s):
    allowed = ['rk', 'g', 'afilmnqstvwy', 'agsci', 'fy', 'liva', 'acdefghiklmnpqrstvwy', 'fym']
    if len(s) != 8:
        return False
    for i in range(8):
        if s[i] not in allowed[i]:
            return False
    return True
""", [["rgaaflaf"], ["kgqgyvdm"], ["rgaaflaq"], ["rgaafla"], ["xgaaflaf"], ["rgaaflafa"]], "One allowed set per position; check length first."),
  MATCH("Grammar terms", "Match each term with its meaning.", [("Variable", "Rewritten by productions"), ("Terminal", "Appears in the final string"), ("Start symbol", "Where every derivation begins"), ("Production", "A rule A -> alpha"), ("PDA", "Finite automaton with a stack")]),
  FILL("Grammars", "A context free grammar has {{variables}}, terminals, a start symbol and {{productions|production rules}}. Balanced parentheses are context free but not {{regular}}. A {{pushdown|PDA}} automaton adds a stack.")]))

# ------------------------------------------------------------ 7
CHS.append(CH(
 "Language recognizers and generators",
 ("Two views of a language", [
  "Grammar | generates | Strings",
  "Recognizer | accepts | Strings",
  "Parser | is | Recognizer for programming languages",
  "Compiler | begins with | Syntax check",
  "Tools | build | Recognizers from grammars",
  "Meaning | is | Effect of running"]),
 ["Languages have two faces. A grammar generates strings; a recognizer, also called a parser, syntax checker or lexical analyzer, decides whether a string belongs. A compiler's first pass is exactly such a recognizer.",
  "In practice a grammar guides you as you write: it tells you which symbols may come next. Tools can turn a grammar into a recognizer automatically, for example lex for regular expressions and yacc or Bison for context free grammars.",
  "The notes touch on meaning only briefly: in a programming language, the meaning of a statement is the effect it has when the program runs, and following Wittgenstein, meaning is use."],
 [("Recognizer", "A machine that decides whether a string is in a language."),
  ("Parser", "A recognizer that also builds the structure of the string."),
  ("Lexical analyzer", "A recognizer that splits text into tokens; typically regular."),
  ("Grammar", "A concise specification of the patterns a string must follow."),
  ("lex", "A tool that builds lexical analyzers from regular expressions."),
  ("yacc, Bison", "Tools that build parsers from context free grammars."),
  ("Context sensitive grammar", "A more general grammar form that lets rules depend on surrounding symbols.")],
 ["Generating and recognizing are dual views.",
  "Parsers, syntax checkers and lexical analyzers are all recognizers.",
  "Grammars give a concise spec and can be turned into recognizers automatically.",
  "grep: regular expressions; lex: lexical analyzers; yacc: parsers.",
  "The meaning of j = 5; is the memory update it causes.",
  "Compare the compiler design course for lexers and parsers in depth."],
 [T("There is a pleasing duality between generating the elements of a language and recognizing them. Often what we want is a reasonably efficient machine that recognizes elements. These are called parsers, syntax checkers or lexical analyzers. If you use a compiler for C plus plus, the first pass does this checking."),
  T("The other thing we want is a concise specification of the syntax rules. That is a grammar. We have seen context free grammars. A more general form is the context sensitive grammar, whose rules may depend on neighbours; chapter 8 places it in the hierarchy."),
  T("Grammars serve two roles. As generators they produce strings of the language in a methodical way. In practice we also use them as guides: when you write a program, the grammar tells you which symbols may come next, and you choose among them. The string is generated by you, constrained by the grammar."),
  T("A grammar can also drive the construction of a recognizer, and for the regular, context free and context sensitive classes this has been largely automated. For Unix users, the re in grep stands for regular expression, and the tool lex builds lexical analyzers. The notes also mention yacc, yet another compiler compiler, and its GNU version Bison, which build parsers from grammars."),
  T("What about meaning? The notes take a modest approach for computer languages: the meaning of a language element is the effect it has in the world, in particular in a computer when the program runs. For example, the C plus plus statement j equals five finds the memory location associated with the name j and updates it to the value five."),
  T("Tools like yacc help link language elements to such effects, by attaching actions to grammar rules. The notes close the topic with the philosophical remark that meaning is use, from Wittgenstein, and promise nothing more. The treatment here is similarly modest: meaning as effect, nothing deeper."),
  T("A practical example of the duality. Take the palindrome grammar from chapter 6. As a generator it produces strings by repeatedly wrapping a smaller palindrome with a matching pair. As a recognizer you check the first and last symbol, strip them, and repeat. Same language, two programs. The labs let you do both: derive strings from a grammar by choosing rules, and run a tiny language by its effects."),
  T("If you want to go deeper into lexers and parsers, the Compiler Design course in this library builds them step by step.")],
 [("What is the first pass of many compilers?", ["Code generation", "Syntax and lexical checking", "Linking", "Optimization"], 1, "It recognizes the language of valid programs."),
  ("What does lex build?", ["Parsers", "Lexical analyzers from regular expressions", "Interpreters", "Linkers"], 1, "Regular expressions become scanners."),
  ("What is the meaning of j = 5; in this view?", ["Its length", "The memory update it causes", "A comment", "Nothing"], 1, "Meaning as effect."),
  ("What do grammars do in practice besides generating?", ["Guide what may come next while writing", "Store data", "Run programs", "Compress files"], 0, "They constrain the choices.")],
 [("grep?", "Search with regular expressions."), ("yacc?", "Yet another compiler compiler; builds parsers."), ("Meaning is?", "Use, after Wittgenstein."),
  ("Is a lexer regular?", "Typically yes.")],
 [PL("Guided derivation", "Rules are [left, right] pairs as before, with start symbol \"S\". Write derive(rules, choices): start from \"S\" and for each choice (an index into rules) replace the leftmost variable (upper-case letter) by that rule's right side, as long as the rule's left side matches that variable. Return the final string, or \"invalid\" if a rule does not match or there is no variable left to rewrite.",
     "derive(rules, choices)", """
def derive(rules, choices):
    form = 'S'
    for k in choices:
        idx = -1
        for i in range(len(form)):
            if form[i].isupper():
                idx = i
                break
        if idx == -1:
            return 'invalid'
        r = rules[k]
        if r[0] != form[idx]:
            return 'invalid'
        form = form[:idx] + r[1] + form[idx + 1:]
    return form
""", [[[["S", "R"], ["R", ""], ["R", "a"], ["R", "b"], ["R", "aRa"], ["R", "bRb"]], [0, 4, 5, 3]], [[["S", "R"], ["R", ""], ["R", "a"], ["R", "b"], ["R", "aRa"], ["R", "bRb"]], [0, 4, 1]], [[["S", "R"], ["R", ""], ["R", "a"], ["R", "b"], ["R", "aRa"], ["R", "bRb"]], [0, 1, 1]], [[["S", "R"], ["R", ""], ["R", "a"], ["R", "b"], ["R", "aRa"], ["R", "bRb"]], [1]], [[["S", "R"], ["R", ""], ["R", "a"], ["R", "b"], ["R", "aRa"], ["R", "bRb"]], [0, 4]]], "Find the leftmost upper-case letter each time and check the rule's left side."),
  PL("Meaning as effect", "A tiny language has statements \"x = 5\", \"x = y\", \"x = y + z\" and \"x = y - z\", where each operand is a variable or an integer, and unset variables are 0. Write run_assign(program, var): run the statements in order and return the final value of var (0 if never set).",
     "run_assign(program, var)", """
def run_assign(program, var):
    mem = {}
    def val(tok):
        if tok.lstrip('-').isdigit():
            return int(tok)
        return mem.get(tok, 0)
    for line in program:
        parts = line.split('=')
        name = parts[0].strip()
        right = parts[1].strip().split()
        if len(right) == 3:
            a = val(right[0])
            b = val(right[2])
            if right[1] == '+':
                mem[name] = a + b
            else:
                mem[name] = a - b
        else:
            mem[name] = val(right[0])
    return mem.get(var, 0)
""", [[["j = 5"], "j"], [["j = 5", "k = j + 2", "j = k - 1"], "j"], [["j = 5", "k = j + 2", "j = k - 1"], "k"], [["a = 3"], "z"], [["a = 3", "b = a", "a = b + b"], "a"]], "Keep a dictionary of values; evaluate the right side, then store."),
  ORDER("Meaning of j = 5;", "Put the effect of running the statement in order.", ["The program reaches the statement", "The system finds the memory location named j", "The value 5 is evaluated", "The location is updated to 5", "Execution moves to the next statement"]),
  MATCH("Tools", "Match each tool with what it does.", [("grep", "Searches using regular expressions"), ("lex", "Builds lexical analyzers"), ("yacc", "Builds parsers from grammars"), ("Bison", "The GNU version of yacc")]),
  FILL("Recognizers", "Generating and {{recognizing}} strings are dual views. The 're' in grep stands for {{regular}} expression. The meaning of a program statement is its {{effect}}.")]))

# ------------------------------------------------------------ 8
CHS.append(CH(
 "The Chomsky hierarchy",
 ("Grammar and machine classes", [
  "Regular | is accepted by | DFA or NFA",
  "Deterministic context free | uses | Deterministic PDA",
  "Context free | uses | Nondeterministic PDA",
  "Context sensitive | uses | Linear bounded automaton",
  "Recursive | uses | Halting Turing machine",
  "Recursively enumerable | uses | Turing machine",
  "Each class | contains | The one above it"]),
 ["In the 1950s Noam Chomsky compared the power of formal language systems and arranged them in a hierarchy. From weakest to strongest: regular, deterministic context free, context free, context sensitive, recursive, and recursively enumerable. Each has a matching machine.",
  "Human languages fit none of these classes neatly. At the least they are context sensitive with extra features, and hundreds of further classes have been studied since.",
  "In research it often pays to pick a weak class, such as regular or Markov models, because tools are better and results simpler, and move up only when the problem demands it."],
 [("Chomsky hierarchy", "The nested classes of formal languages from regular up to recursively enumerable."),
  ("Context sensitive grammar", "A grammar whose rules do not shrink strings; recognized by linear bounded automata."),
  ("Linear bounded automaton", "A Turing machine whose tape is limited to the length of the input."),
  ("Recursive language", "A language decided by a Turing machine that halts on every input."),
  ("Recursively enumerable language", "A language accepted by some Turing machine, which may loop on non-members."),
  ("Epsilon-machine", "A minimal predictive model of a process, from Jim Crutchfield's work, in the regular spirit.")],
 ["Regular < deterministic context free < context free < context sensitive < recursive < r.e.",
  "Machines: DFA/NFA, DPDA, PDA, linear bounded automaton, halting TM, TM.",
  "More power means more languages but harder analysis.",
  "Human languages are at least context sensitive, with more features.",
  "Pick the weakest class that fits the problem.",
  "Chomsky linked the idea to how children acquire language."],
 [T("The tools of the last chapters are often used to design a specialized language for a task. A harder and more interesting job is the reverse: given an existing or observed language, find a grammar or recognizer for it. A natural example is English or Spanish. More generally, any system whose behaviour can be written as strings, and whose patterns we want to find, is a candidate."),
  T("In the 1950s linguists began applying formal language theory to human languages. Noam Chomsky compared the relative power of formal systems, that is, which languages each can specify, and is usually credited with establishing the relationships now called the Chomsky hierarchy. He also observed how fast young children acquire language, far faster than typical learning algorithms would allow, and hypothesized an inborn general language machine that is tuned to one language by early exposure."),
  T("The classical hierarchy pairs each language class with a machine class. Regular languages go with deterministic or nondeterministic finite automata. Deterministic context free languages go with deterministic pushdown automata, and context free languages with nondeterministic pushdown automata. Context sensitive languages go with linear bounded automata, Turing machines with a tape no longer than the input. Recursive languages go with Turing machines that halt on every input, and recursively enumerable languages with general Turing machines."),
  T("The classes are nested. Every regular language is deterministic context free, which is context free, which is context sensitive, which is recursive, which is recursively enumerable. Each step up adds languages and loses easy properties. For regular languages, equivalence of two machines can be checked; for general Turing machines, almost every question is undecidable, as chapter 10 shows."),
  T("In terms of grammar shapes, the classes are often read off the rules. A right-linear grammar, where each rule has at most one variable and it is at the end, gives regular languages. A rule with a single variable on the left gives context free. Rules whose right side is never shorter than the left give context sensitive. Anything else is unrestricted, giving the recursively enumerable languages. The lab classifies grammars this way."),
  T("Human languages do not fit neatly. The notes say they are at the very least context sensitive but need additional features, and that since the 1950s many more language categories have been identified, probably hundreds. A deeper question is whether a concise formal grammar for a human language even makes sense, and what it would mean."),
  T("The notes then give practical advice. It is worth knowing the variety of language types, but usually you restrict attention to one class and see which parts of your problem fit. Regular languages are concise, easy to work with and well supported by tools, and Markov models are well studied. So it often makes sense to try a regular or Markov approach first, as in Jim Crutchfield's epsilon-machines, or hidden Markov models for genome sequences.")],
 [("Which machine recognizes context sensitive languages?", ["DFA", "Pushdown automaton", "Linear bounded automaton", "Markov model"], 2, "A Turing machine with a tape bounded by the input."),
  ("Which class is the most general in the list?", ["Regular", "Context free", "Recursive", "Recursively enumerable"], 3, "Accepted by general Turing machines."),
  ("Are human languages regular?", ["Yes", "No, at least context sensitive", "Only English", "Only written ones"], 1, "They need more power than regular."),
  ("Why prefer a weak class when possible?", ["It is cheaper and tools are better", "It is always more accurate", "It needs no data", "It is random"], 0, "Concise and well-supported.")],
 [("Who formalized the hierarchy?", "Noam Chomsky, in the 1950s."), ("Nesting order?", "Regular inside context free inside context sensitive inside recursive inside r.e."), ("Machine for recursive?", "A Turing machine that halts on every input."),
  ("What is an epsilon-machine?", "A minimal predictive model of a process.")],
 [PL("Classify a grammar", "Rules are [left, right] pairs of strings; upper-case letters are variables. Write chomsky_class(rules): return 3 if every rule has a single variable on the left and a right side that is zero or more terminals optionally followed by exactly one variable at the very end (right-linear); otherwise 2 if every left side is a single variable; otherwise 1 if no right side is shorter than its left side; otherwise 0.",
     "chomsky_class(rules)", """
def chomsky_class(rules):
    def single(l):
        return len(l) == 1 and l.isupper()
    def linear(r):
        if r == '':
            return True
        i = 0
        while i < len(r) and not r[i].isupper():
            i += 1
        if i == len(r):
            return True
        return i == len(r) - 1
    ok3 = True
    ok2 = True
    ok1 = True
    for r in rules:
        l = r[0]
        rhs = r[1]
        if not (single(l) and linear(rhs)):
            ok3 = False
        if not single(l):
            ok2 = False
        if len(rhs) < len(l):
            ok1 = False
    if ok3:
        return 3
    if ok2:
        return 2
    if ok1:
        return 1
    return 0
""", [[[["S", "aS"], ["S", "b"]]], [[["S", "R"], ["R", ""], ["R", "(R)"], ["R", "RR"]]], [[["S", "aAb"], ["aA", "aab"]]], [[["S", "ab"], ["ab", "a"]]], [[["S", "rW"], ["W", "g"]]], [[["S", "Ab"], ["A", "a"]]]], "Test the strictest class first and fall back to weaker ones."),
  ORDER("Power", "Order the language classes from the weakest to the strongest.", ["Regular", "Deterministic context free", "Context free", "Context sensitive", "Recursive", "Recursively enumerable"]),
  MATCH("Machines", "Match each language class with its machine.", [("Regular", "Finite automaton"), ("Deterministic context free", "Deterministic pushdown automaton"), ("Context free", "Nondeterministic pushdown automaton"), ("Context sensitive", "Linear bounded automaton"), ("Recursive", "Turing machine that halts on every input"), ("Recursively enumerable", "General Turing machine")]),
  FILL("Hierarchy", "The hierarchy was set out by Noam {{Chomsky}}. Context free languages need a {{pushdown|stack}} automaton. Human languages are at least context {{sensitive}}.")]))
