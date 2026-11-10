# -*- coding: utf-8 -*-
"""GOFAI course, part 1: history, representation, logic, unification, search."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "What GOFAI is: symbols, rules and the dream of reasoning machines",
 ("GOFAI", [
  "GOFAI | means | Good Old-Fashioned AI",
  "Symbol | stands for | A thing or idea",
  "Rule | transforms | Symbols",
  "Search | explores | Possibilities",
  "Knowledge base | stores | Facts and rules",
  "Dartmouth 1956 | named | Artificial intelligence",
  "Connectionism | is | The contrast"]),
 ["GOFAI, Good Old-Fashioned Artificial Intelligence, is the approach that builds intelligence from explicit symbols and rules: facts written down, logic applied to them, and search through possible answers. The name was coined by the philosopher John Haugeland in 1985.",
  "It dominated AI from the 1950s to the 1980s and produced theorem provers, game players, planners and expert systems. Its rival, connectionism, learns patterns in numbers, as neural networks do.",
  "This course teaches the core ideas with small programs you can run: representation, logic, search, rules, planning, constraints and what GOFAI could not do."],
 [("GOFAI", "Good Old-Fashioned AI: intelligence built from explicit symbols and rules."),
  ("Symbol", "A token that stands for something, such as a fact, object or action."),
  ("Knowledge base", "A collection of facts and rules a program can reason over."),
  ("Physical symbol system hypothesis", "Newell and Simon's claim that a system that manipulates symbols has what is needed for general intelligence."),
  ("Connectionism", "The approach that models intelligence with networks of simple units that learn from data.")],
 ["GOFAI = symbols + rules + search.",
  "Dartmouth workshop, 1956, named the field.",
  "Logic Theorist (1956) and GPS (1957) were early programs.",
  "Expert systems peaked in the 1980s.",
  "AI winters followed over-promising."],
 [T("When people first imagined thinking machines, they imagined machines that follow rules. A person solves a puzzle by writing down what is known and working out what follows. So a program could write facts as symbols and work out the rest by rules. That is the heart of GOFAI."),
  T("The field was named at a summer workshop at Dartmouth College in 1956, organised by John McCarthy, Marvin Minsky, Nathaniel Rochester and Claude Shannon. That same year Allen Newell, Herbert Simon and Cliff Shaw showed the Logic Theorist, which proved theorems from Whitehead and Russell's Principia Mathematica."),
  T("Newell and Simon followed it with the General Problem Solver in 1957, which separated what a problem is from how to search for solutions. In 1976 they stated the physical symbol system hypothesis: manipulating symbols is both necessary and sufficient for intelligent action. Much of GOFAI is an attempt to test this claim."),
  T("In the 1970s and 1980s, expert systems captured the knowledge of human specialists as thousands of if-then rules. DENDRAL guessed chemical structures. MYCIN suggested antibiotics for blood infections. Companies invested heavily. But the systems were brittle and costly to maintain, and funding fell in the so-called AI winters."),
  T("Today most headline AI uses learned models, but the symbolic ideas have not vanished. Search runs in route planners and game engines. Logic checks hardware and software. Knowledge graphs power web search. And recent work called neuro-symbolic AI tries to combine learning with reasoning. Knowing GOFAI helps you see what each approach is good at.")],
 [("What does GOFAI stand for?", ["Good Old-Fashioned AI", "General Optimal Function AI", "Graph Oriented Fact AI", "Greatest Of Formal AI"], 0, "Coined by Haugeland."),
  ("When was the field named at Dartmouth?", ["1956", "1936", "1976", "1996"], 0, "Summer workshop."),
  ("Which program proved theorems from Principia Mathematica?", ["Logic Theorist", "MYCIN", "DENDRAL", "ELIZA"], 0, "Newell, Simon, Shaw."),
  ("What does the physical symbol system hypothesis claim?", ["Symbol manipulation is enough for intelligence", "Only brains think", "Neural networks are best", "Intelligence needs robots"], 0, "1976."),
  ("What was MYCIN used for?", ["Suggesting antibiotics", "Playing chess", "Translating text", "Drawing"], 0, "An expert system."),
  ("What is GOFAI's main rival approach?", ["Connectionism", "Cryptography", "Compilers", "Databases"], 0, "Learning from data.")],
 [("1956", "Dartmouth workshop"), ("Logic Theorist", "first theorem-proving program"), ("GPS", "General Problem Solver, 1957"), ("MYCIN", "medical expert system"), ("PSSH", "physical symbol system hypothesis")],
 [MATCH("Match the program", "Pair each program with what it did.", [("Logic Theorist", "proved theorems"), ("GPS", "general problem solving by means-ends analysis"), ("DENDRAL", "guessed chemical structures"), ("MYCIN", "recommended antibiotics")]),
  ORDER("A short timeline", "Order these events from earliest to latest.", ["Dartmouth workshop", "General Problem Solver", "Physical symbol system hypothesis", "Expert system boom of the 1980s", "Knowledge graph search"]),
  FILL("Core idea", "GOFAI builds intelligence from explicit {{symbols}} and {{rules}} plus search."),
  PL("Era of a year", "Write era(year): return 'foundations' for 1950 to 1969, 'knowledge' for 1970 to 1989, 'winter' for 1990 to 1999, 'modern' for 2000 or later, and 'before' for anything earlier than 1950.", "era(year)", '''
def era(year):
    if year < 1950:
        return "before"
    if year < 1970:
        return "foundations"
    if year < 1990:
        return "knowledge"
    if year < 2000:
        return "winter"
    return "modern"
''', [[1940], [1956], [1976], [1985], [1995], [2010]], "Check the limits in order.")]
))

CHS.append(CH(
 "Knowledge representation: networks, frames and ontologies",
 ("Representation", [
  "Semantic network | links | Concepts",
  "IS-A | gives | Inheritance",
  "Frame | has | Slots",
  "Default | can be | Overridden",
  "Ontology | defines | Categories",
  "Knowledge graph | stores | Triples",
  "Representation | shapes | Reasoning"]),
 ["How you write knowledge down decides what a program can do with it. A semantic network draws concepts as nodes and relations as labelled links, such as canary IS-A bird. A frame bundles slots and values for a concept, such as a bird with wings and a way of moving.",
  "IS-A links allow inheritance: a canary inherits what is true of birds unless told otherwise. Defaults can be overridden, so a penguin IS-A bird but cannot fly.",
  "An ontology is a shared list of categories and relations, and a knowledge graph stores facts as subject, relation, object triples."],
 [("Semantic network", "A graph with concepts as nodes and labelled relations as links."),
  ("Frame", "A structure of slots and values describing a typical object or situation."),
  ("Inheritance", "A property passing from a category down to its members."),
  ("Default reasoning", "Assuming a typical property unless there is information against it."),
  ("Triple", "A fact in the form subject, relation, object.")],
 ["IS-A links build a hierarchy.",
  "Members inherit properties from categories.",
  "Defaults: birds fly, unless exceptions say otherwise.",
  "Frames: slots with values and defaults.",
  "Knowledge graph: facts as triples."],
 [T("Think of a family tree for ideas. Canary is a kind of bird. Bird is a kind of animal. Animal is a kind of living thing. You write each link once, and the program can answer many questions. Is a canary an animal? Follow the links up and you reach yes."),
  T("Properties move down the same links. Birds can fly, so canaries can fly. Animals breathe, so canaries breathe. You do not have to write the fact once per animal. That saving is called inheritance, and it keeps a knowledge base small and consistent."),
  T("Exceptions complicate it. Penguins are birds, but they do not fly. A good system lets a more specific fact beat a general one: the nearest node on the path wins. This is default reasoning. Dealing with the exceptions properly is one of the main reasons GOFAI got hard."),
  T("A frame gathers what is known about a type of thing. A restaurant frame has slots for menu, waiter, bill and a typical script of ordering, eating and paying. When you hear that someone went to a restaurant, the frame lets you fill in the unstated parts, which is a kind of common sense."),
  T("Modern systems store such knowledge as triples, subject, relation, object, in a knowledge graph. Wikidata and the graphs behind web search work this way. An ontology fixes the vocabulary, so different programs mean the same thing by the same word. The Semantic Web is this idea at scale.")],
 [("What does IS-A mean in a semantic network?", ["A category link", "A cause link", "A part link", "A time link"], 0, "Canary IS-A bird."),
  ("What is inheritance?", ["Properties passing from category to member", "A copy of a file", "A loop", "A kind of search"], 0, "Saves repetition."),
  ("Why do penguins matter in knowledge representation?", ["They are exceptions to a default", "They are rare", "They are birds that sing", "They have no category"], 0, "Birds fly, penguins do not."),
  ("What is a frame?", ["Slots and values for a concept", "A window", "A proof", "A graph colour"], 0, "A structured description."),
  ("What is a triple?", ["Subject, relation, object", "Three rules", "Three players", "Three nodes only"], 0, "A fact."),
  ("What does an ontology provide?", ["Shared categories and relations", "A faster CPU", "A random seed", "A neural net"], 0, "Common vocabulary.")],
 [("IS-A", "category link"), ("Frame", "slots and defaults"), ("Inheritance", "properties pass down"), ("Triple", "subject, relation, object"), ("Ontology", "shared vocabulary")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Semantic network", "concepts linked by relations"), ("Frame", "slots and defaults for a concept"), ("Inheritance", "properties pass down IS-A links"), ("Ontology", "shared categories and relations"), ("Triple", "subject, relation, object")]),
  PL("Is it a kind of?", "Write is_a(kb, x, y): kb is a dict mapping a concept to its parent (the concept it IS-A), for example {'canary': 'bird', 'bird': 'animal'}. Return True if y can be reached from x by following parents (x equals y also counts), otherwise False.", "is_a(kb, x, y)", '''
def is_a(kb, x, y):
    seen = 0
    while seen < 100:
        if x == y:
            return True
        if x not in kb:
            return False
        x = kb[x]
        seen = seen + 1
    return False
''', [[{"canary": "bird", "bird": "animal"}, "canary", "animal"], [{"canary": "bird", "bird": "animal"}, "animal", "canary"], [{"canary": "bird"}, "canary", "canary"], [{}, "a", "b"], [{"penguin": "bird", "bird": "animal"}, "penguin", "bird"]], "Walk up the parents until you hit y or run out."),
  PL("Inherited property", "Write inherited(kb, props, x, name): kb is a dict child to parent, props is a dict from concept to a dict of its own properties. Return the value of property name for x, using the nearest concept on the path from x upward that defines it, or None if no concept does.", "inherited(kb, props, x, name)", '''
def inherited(kb, props, x, name):
    steps = 0
    while steps < 100:
        if x in props and name in props[x]:
            return props[x][name]
        if x not in kb:
            return None
        x = kb[x]
        steps = steps + 1
    return None
''', [[{"canary": "bird", "bird": "animal", "penguin": "bird"}, {"bird": {"flies": True}, "animal": {"breathes": True}, "penguin": {"flies": False}}, "canary", "flies"],
      [{"canary": "bird", "bird": "animal", "penguin": "bird"}, {"bird": {"flies": True}, "animal": {"breathes": True}, "penguin": {"flies": False}}, "penguin", "flies"],
      [{"canary": "bird", "bird": "animal", "penguin": "bird"}, {"bird": {"flies": True}, "animal": {"breathes": True}, "penguin": {"flies": False}}, "penguin", "breathes"],
      [{"canary": "bird", "bird": "animal"}, {"bird": {"flies": True}}, "canary", "colour"]], "The nearest definition wins, so look at x first."),
  PL("Query triples", "Write query(triples, s, r, o): triples is a list of [subject, relation, object]. A query argument of None means any value. Return the list of triples that match, in the original order.", "query(triples, s, r, o)", '''
def query(triples, s, r, o):
    out = []
    for t in triples:
        if s is not None and t[0] != s:
            continue
        if r is not None and t[1] != r:
            continue
        if o is not None and t[2] != o:
            continue
        out.append(t)
    return out
''', [[[["a", "likes", "b"], ["a", "knows", "c"], ["d", "likes", "b"]], None, "likes", "b"], [[["a", "likes", "b"], ["a", "knows", "c"]], "a", None, None], [[["a", "likes", "b"]], "z", None, None]], "Skip any triple that fails a given test.")]
))

CHS.append(CH(
 "Propositional logic and resolution",
 ("Propositional logic", [
  "Proposition | is | True or false",
  "Connective | combines | Propositions",
  "Truth table | lists | All cases",
  "Tautology | is | Always true",
  "Entailment | follows | From premises",
  "Resolution | refutes | A set of clauses",
  "Clause | is | A disjunction of literals"]),
 ["Propositional logic works with statements that are true or false and connectives such as not, and, or and implies. A truth table lists the value of a formula for every assignment of truth values to its variables.",
  "A formula is a tautology if it is true in every row, satisfiable if true in some row, and a contradiction if true in none. A set of premises entails a conclusion if the conclusion is true in every row that makes all premises true.",
  "Resolution is a single rule that is complete for refutation: to show that premises entail a goal, add the negation of the goal and derive the empty clause."],
 [("Tautology", "A formula true under every assignment."),
  ("Satisfiable", "True under at least one assignment."),
  ("Entailment", "A conclusion follows from premises if every assignment making the premises true makes it true."),
  ("Clause", "A disjunction of literals, such as A or not B."),
  ("Resolution", "From (A or X) and (not A or Y) derive (X or Y).")],
 ["n variables give 2^n rows.",
  "Tautology: always true. Contradiction: never.",
  "P implies Q is the same as not P or Q.",
  "Resolution: cancel a literal and its negation.",
  "Empty clause means contradiction."],
 [T("A statement like 'it is raining' is either true or false. Combine them with not, and, or, and implies. 'If it rains then the grass is wet' is a rule. Together with 'it rains' it lets you conclude 'the grass is wet'. This step is called modus ponens, and it is the basic move of logic."),
  T("To check a formula mechanically, build its truth table. With two variables there are four rows, with three there are eight, with n there are two to the n. That growth is why exact checking becomes slow. The SAT problem, deciding if any row works, is hard in general, though modern solvers handle huge cases."),
  T("A formula true in every row is a tautology, such as P or not P. If a conclusion is true in every row where the premises are true, we say the premises entail it. This is semantic entailment, the thing we want programs to decide correctly."),
  T("Resolution works on clauses, which are ORs of literals. Convert each formula to clauses. Take two clauses, one with A and one with not A, and merge the rest: (A or X) and (not A or Y) give (X or Y). Repeating until the empty clause appears shows the set is inconsistent."),
  T("To prove that premises entail a goal by resolution, add the negation of the goal to the clauses and see if you can reach the empty clause. This refutation proof is complete, which means it always finds a proof when one exists. It underlies automated theorem provers and the SAT solvers used in chip design.")],
 [("How many rows in a truth table with 3 variables?", ["8", "6", "9", "3"], 0, "2 to the 3."),
  ("What is a tautology?", ["True under every assignment", "True under some assignment", "False under every assignment", "A kind of clause"], 0, "P or not P."),
  ("P implies Q is equivalent to...", ["not P or Q", "P and not Q", "not P and Q", "P or Q"], 0, "A standard identity."),
  ("What does resolution on (A or X) and (not A or Y) give?", ["X or Y", "A or Y", "not X", "X and Y"], 0, "Cancel A."),
  ("What does reaching the empty clause show?", ["The clauses are inconsistent", "The clauses are satisfiable", "A tautology", "Nothing"], 0, "Contradiction."),
  ("How do you prove a goal with resolution?", ["Add its negation and derive the empty clause", "Search for the goal directly", "Count the rows", "Add the goal and stop"], 0, "Refutation.")],
 [("Tautology", "always true"), ("Modus ponens", "from P and P implies Q, infer Q"), ("Resolution", "cancel a literal and its negation"), ("SAT", "does any assignment satisfy the formula?")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Tautology", "true in every row"), ("Contradiction", "true in no row"), ("Satisfiable", "true in some row"), ("Entailment", "true whenever the premises are true"), ("Clause", "an OR of literals")]),
  PL("Evaluate a formula", "Write evaluate(f, env). A formula is a string variable name like 'A', or a list: ['not', f], ['and', f, g], ['or', f, g], ['implies', f, g]. env maps names to True or False. Return the truth value.", "evaluate(f, env)", '''
def evaluate(f, env):
    if isinstance(f, str):
        return env[f]
    op = f[0]
    if op == "not":
        return not evaluate(f[1], env)
    a = evaluate(f[1], env)
    b = evaluate(f[2], env)
    if op == "and":
        return a and b
    if op == "or":
        return a or b
    return (not a) or b
''', [["A", {"A": True}], [["not", "A"], {"A": True}], [["implies", "A", "B"], {"A": True, "B": False}], [["implies", "A", "B"], {"A": False, "B": False}], [["and", "A", ["or", "B", "C"]], {"A": True, "B": False, "C": True}]], "Recurse on the structure."),
  PL("Tautology check", "Write is_tautology(f, names). f is a formula as in the previous lab and names is the list of variable names. Return True if f is true under all 2^n assignments.", "is_tautology(f, names)", '''
def ev(f, env):
    if isinstance(f, str):
        return env[f]
    op = f[0]
    if op == "not":
        return not ev(f[1], env)
    a = ev(f[1], env)
    b = ev(f[2], env)
    if op == "and":
        return a and b
    if op == "or":
        return a or b
    return (not a) or b
def is_tautology(f, names):
    n = len(names)
    for i in range(2 ** n):
        env = {}
        for j in range(n):
            env[names[j]] = (i // (2 ** j)) % 2 == 1
        if not ev(f, env):
            return False
    return True
''', [[["or", "P", ["not", "P"]], ["P"]], [["implies", "P", "Q"], ["P", "Q"]], [["implies", ["and", "P", ["implies", "P", "Q"]], "Q"], ["P", "Q"]], [["and", "P", ["not", "P"]], ["P"]]], "Try every assignment with bit tricks or nested loops."),
  PL("Resolve two clauses", "Write resolve(c1, c2). A clause is a list of literal strings, where a leading '-' means not, for example ['A', '-B']. If the clauses contain a complementary pair (a literal and its negation), return the resolvent, the sorted list of remaining literals without duplicates, using the first complementary pair found when scanning c1 in order. Otherwise return None.", "resolve(c1, c2)", '''
def neg(l):
    if l[0] == "-":
        return l[1:]
    return "-" + l
def resolve(c1, c2):
    for l in c1:
        if neg(l) in c2:
            rest = {}
            for x in c1:
                if x != l:
                    rest[x] = 1
            for x in c2:
                if x != neg(l):
                    rest[x] = 1
            return sorted(rest.keys())
    return None
''', [[["A", "X"], ["-A", "Y"]], [["A"], ["-A"]], [["A", "B"], ["C"]], [["-P", "Q"], ["P", "R", "Q"]]], "Find a literal whose negation is in the other clause.")]
))

CHS.append(CH(
 "Predicate logic and unification",
 ("Predicate logic", [
  "Predicate | describes | Objects",
  "Quantifier | ranges | Over objects",
  "Variable | stands for | Any object",
  "Substitution | replaces | Variables",
  "Unification | matches | Two terms",
  "Most general unifier | is | The simplest match",
  "Prolog | uses | Unification"]),
 ["Predicate logic adds objects, predicates and quantifiers to propositional logic. It lets you say all humans are mortal and Socrates is human, so Socrates is mortal.",
  "To apply a general rule to a particular fact, a program must match patterns. Unification finds a substitution of variables that makes two terms identical, such as turning Human(x) and Human(Socrates) into the same term by setting x to Socrates.",
  "Unification is the core operation of resolution theorem provers and of Prolog."],
 [("Predicate", "A property or relation applied to objects, such as Human(Socrates)."),
  ("Quantifier", "For all or there exists, binding a variable."),
  ("Substitution", "A mapping from variables to terms."),
  ("Unifier", "A substitution that makes two terms identical."),
  ("Occurs check", "A test that stops a variable being bound to a term containing itself.")],
 ["All humans are mortal: for all x, Human(x) implies Mortal(x).",
  "Variables begin with a lowercase letter; constants are capitalised, in this course.",
  "Unify Human(x) with Human(Socrates): x = Socrates.",
  "A variable can unify with any term not containing itself.",
  "Different constants never unify."],
 [T("Propositional logic cannot say much about the world. You need a different proposition for every person: SocratesIsHuman, PlatoIsHuman, and so on. Predicate logic fixes this. Human is a predicate, and Human(x) is a statement about any object x. A quantifier binds x: for all x, if x is human then x is mortal."),
  T("Now the program has a rule with a variable and a fact with a constant. To use the rule it must match them. Human(x) against Human(Socrates): the predicate is the same, and the argument x can be Socrates. The substitution, written x maps to Socrates, makes both sides identical. This matching is unification."),
  T("Unification works recursively. Two constants unify only if they are equal. A variable unifies with any term, and the binding is recorded. Two compound terms unify if they have the same name and number of arguments and every pair of arguments unifies under one consistent substitution. Otherwise unification fails."),
  T("A catch is the occurs check. Unifying x with F(x) would need an infinite term, so a correct unifier refuses. Prolog historically skipped this check for speed, which can lead to odd behaviour. Many modern systems offer it as an option."),
  T("Unification gives GOFAI much of its power. Resolution for predicate logic unifies a literal with a negated literal, then resolves. Prolog does the same in a fixed order, which makes logic into a programming language. Planners and parsers use it to match patterns against facts.")],
 [("What does unification do?", ["Finds a substitution making two terms identical", "Sorts a list", "Runs a program", "Draws a graph"], 0, "Pattern matching."),
  ("Unify Human(x) with Human(Socrates). What is x?", ["Socrates", "Human", "Mortal", "Nothing"], 0, "x maps to Socrates."),
  ("Can two different constants unify?", ["No", "Yes", "Only in Prolog", "Only if short"], 0, "A and B are different."),
  ("What is the occurs check for?", ["Stopping x unifying with F(x)", "Counting variables", "Speeding up search", "Printing"], 0, "No infinite terms."),
  ("Which system uses unification at its core?", ["Prolog", "A spreadsheet", "A compiler only", "A database index"], 0, "Logic programming."),
  ("What does a universal quantifier say?", ["For all objects", "For some object", "For no objects", "For the first object"], 0, "For all x.")],
 [("Human(x)", "predicate with a variable"), ("x maps to Socrates", "a substitution"), ("MGU", "most general unifier"), ("Occurs check", "reject x = F(x)")],
 [MATCH("Match the unification case", "Pair each pair of terms with the result.", [("f(x) and f(A)", "x = A"), ("A and A", "unify with no bindings"), ("A and B", "fail"), ("x and F(x)", "fail (occurs check)")]),
  PL("Unify", "Write unify(a, b). Terms are strings or lists. A string starting with a lowercase letter is a variable; a string starting with an uppercase letter is a constant; a list [name, arg1, arg2, ...] is a compound term whose first item is a string name. Return the substitution as a list of [variable, term] pairs sorted by variable name (the bindings found, without applying later ones to earlier ones), or None if they do not unify. Include the occurs check.", "unify(a, b)", '''
def is_var(t):
    return isinstance(t, str) and t[0].islower()
def walk(t, s):
    while is_var(t) and t in s:
        t = s[t]
    return t
def occurs(v, t, s):
    t = walk(t, s)
    if t == v:
        return True
    if isinstance(t, list):
        for x in t:
            if occurs(v, x, s):
                return True
    return False
def uni(a, b, s):
    a = walk(a, s)
    b = walk(b, s)
    if a == b:
        return s
    if is_var(a):
        if occurs(a, b, s):
            return None
        s[a] = b
        return s
    if is_var(b):
        if occurs(b, a, s):
            return None
        s[b] = a
        return s
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i in range(len(a)):
            s = uni(a[i], b[i], s)
            if s is None:
                return None
        return s
    return None
def unify(a, b):
    s = uni(a, b, {})
    if s is None:
        return None
    out = []
    for k in sorted(s.keys()):
        out.append([k, s[k]])
    return out
''', [[["Human", "x"], ["Human", "Socrates"]], ["A", "A"], ["A", "B"], ["x", ["F", "x"]], [["P", "x", "B"], ["P", "A", "y"]], [["P", "x", "x"], ["P", "A", "B"]]], "Walk variables through the substitution before comparing."),
  PL("Apply a substitution", "Write apply_sub(t, s): replace variables in the term t using the substitution dict s, repeatedly until nothing changes. Terms are as before (lowercase strings are variables, lists are compound terms).", "apply_sub(t, s)", '''
def apply_sub(t, s):
    if isinstance(t, str):
        n = 0
        while t in s and n < 50:
            t = s[t]
            n = n + 1
        if isinstance(t, list):
            return apply_sub(t, s)
        return t
    return [apply_sub(x, s) for x in t]
''', [[["Human", "x"], {"x": "Socrates"}], [["P", "x", "y"], {"x": "y", "y": "A"}], ["z", {}], [["F", ["G", "x"]], {"x": "B"}]], "Resolve each variable down to a term, then recurse into lists.")]
))

CHS.append(CH(
 "Search: finding answers by exploring",
 ("Search", [
  "State | describes | A situation",
  "Operator | moves | Between states",
  "Goal test | ends | Search",
  "BFS | finds | Shortest paths",
  "DFS | goes | Deep first",
  "Frontier | holds | States to expand",
  "Branching | grows | Exponentially"]),
 ["Many AI problems are search problems: a start state, operators that move from one state to another, and a goal test. Finding a route, solving a puzzle or planning a move are all ways of exploring a graph of states.",
  "Breadth-first search expands states level by level, and finds a shortest path when every step costs the same. Depth-first search goes deep along one branch first, using little memory but possibly missing short answers.",
  "The enemy of search is the exponential growth of states with depth, called the combinatorial explosion."],
 [("State space", "The set of all states reachable from the start by applying operators."),
  ("Frontier", "The states that have been found but not yet expanded."),
  ("Breadth-first search", "Search that expands the shallowest states first, using a queue."),
  ("Depth-first search", "Search that expands the deepest state first, using a stack."),
  ("Branching factor", "The average number of operators applicable in a state.")],
 ["BFS uses a queue; DFS uses a stack.",
  "BFS is complete and finds fewest steps.",
  "DFS uses less memory but is not optimal.",
  "Branching b and depth d give about b^d states.",
  "Keep a visited set to avoid loops."],
 [T("Think of a maze as a graph. Each junction is a state, each corridor an operator that takes you to a neighbouring junction. The start is where you are, and the goal is the exit. Search is the systematic way to try the junctions without going round in circles."),
  T("Breadth-first search explores in rings. First all the junctions one step away, then two steps away, and so on. It keeps the found-but-unvisited junctions in a queue, first in first out. The first time it reaches the goal, it has used the fewest possible steps."),
  T("Depth-first search chooses one corridor and follows it as far as it goes, backing up only when stuck. It keeps junctions in a stack. It needs little memory since it stores only one path, but it can wander down a long wrong path and return a long answer when a short one exists."),
  T("The cost is the number of states. If every state has b choices and the answer is d steps away, breadth-first search may look at about b to the power d states. Chess has about thirty moves per position, so looking ahead ten moves would need on the order of 30 to the 10th power, far too many. This is the combinatorial explosion."),
  T("To avoid loops, keep a set of visited states and never expand one twice. To avoid blind exploration, use extra knowledge to guide the search, which is the idea of heuristics in the next chapter. The widget in this chapter lets you see the difference between the strategies on a grid.")],
 [("Which data structure does BFS use?", ["A queue", "A stack", "A heap only", "A tree only"], 0, "First in, first out."),
  ("Which data structure does DFS use?", ["A stack", "A queue", "A set only", "A list of lists"], 0, "Last in, first out."),
  ("Which search finds a fewest-steps path when steps cost the same?", ["Breadth-first", "Depth-first", "Random", "Neither"], 0, "Level by level."),
  ("What is the branching factor?", ["Average number of moves per state", "Depth of the tree", "Number of goals", "Memory used"], 0, "b."),
  ("Why keep a visited set?", ["To avoid loops and repeats", "To speed up printing", "To find more goals", "To sort the frontier"], 0, "Graphs have cycles."),
  ("What is the combinatorial explosion?", ["Exponential growth in states", "A software bug", "A graphics effect", "A sorting method"], 0, "b to the d.")],
 [("BFS", "queue, shortest path in steps"), ("DFS", "stack, deep first"), ("Frontier", "found but not expanded"), ("Branching factor", "moves per state")],
 [APP("SEARCH", "Search on a grid", "Draw walls by tapping cells, then press Run to watch breadth-first, depth-first and A* explore the grid. Run all three strategies to complete this lab.", 720),
  MATCH("Match the strategy", "Pair each strategy with a fact.", [("BFS", "queue; fewest steps"), ("DFS", "stack; little memory"), ("Visited set", "avoids loops"), ("Combinatorial explosion", "states grow as b to the d")]),
  PL("Breadth-first search", "Write bfs(graph, start, goal): graph is a dict from node to a list of neighbours. Return the shortest path as a list of nodes from start to goal (inclusive), or an empty list if there is none. Expand neighbours in the order they are listed.", "bfs(graph, start, goal)", '''
def bfs(graph, start, goal):
    queue = [[start]]
    seen = {start: 1}
    head = 0
    while head < len(queue):
        path = queue[head]
        head = head + 1
        node = path[len(path) - 1]
        if node == goal:
            return path
        for nb in graph.get(node, []):
            if nb not in seen:
                seen[nb] = 1
                queue.append(path + [nb])
    return []
''', [[{"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A", "D"], [{"A": ["B"], "B": []}, "A", "A"], [{"A": ["B"], "B": [], "C": []}, "A", "C"], [{"S": ["A", "B"], "A": ["G"], "B": ["C"], "C": ["G"], "G": []}, "S", "G"]], "Keep a queue of paths and a visited set."),
  PL("Depth-first search", "Write dfs(graph, start, goal): return the first path from start to goal found by depth-first search that expands neighbours in the listed order and never visits a node twice (a visited set shared by the whole search). Return an empty list if there is none.", "dfs(graph, start, goal)", '''
def dfs(graph, start, goal):
    seen = {}
    def go(node, path):
        if node == goal:
            return path
        seen[node] = 1
        for nb in graph.get(node, []):
            if nb not in seen:
                r = go(nb, path + [nb])
                if r:
                    return r
        return []
    return go(start, [start])
''', [[{"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A", "D"], [{"A": ["B", "C"], "B": [], "C": ["D"], "D": []}, "A", "D"], [{"A": ["B"], "B": ["A"]}, "A", "C"], [{"S": ["A", "B"], "A": ["B"], "B": ["G"], "G": []}, "S", "G"]], "Recurse, marking nodes visited as you go."),
  PL("Count states", "Write states(b, d): the number of nodes in a complete search tree with branching factor b and depth d (the root counts as depth 0): 1 + b + b^2 + ... + b^d.", "states(b, d)", '''
def states(b, d):
    total = 0
    p = 1
    for i in range(d + 1):
        total = total + p
        p = p * b
    return total
''', [[2, 3], [3, 4], [1, 5], [10, 2], [30, 3]], "Add up the powers of b.")]
))
