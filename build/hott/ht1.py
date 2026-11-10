# -*- coding: utf-8 -*-
"""HoTT course, part 1: types, Pi and Sigma, Curry-Howard, identity types, higher paths."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=680):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Why types? The big idea of HoTT",
 ("Homotopy type theory", [
  "Type theory | replaces | Set theory",
  "Type | has | Terms",
  "Proposition | is | A type",
  "Proof | is | A term",
  "Equality | is | A path",
  "Univalence | says | Equivalent types are equal",
  "HoTT | studies | Shapes of types"]),
 ["Homotopy type theory, or HoTT, reads types as spaces, terms as points, and equalities as paths between points. A proof that two things are equal becomes a path you can walk, bend and compose.",
  "It combines two old ideas: Martin-Lof type theory, a foundation for mathematics and programming, and homotopy theory, the study of shapes up to continuous deformation.",
  "The result is a foundation where equal things really are interchangeable, which is exactly what mathematicians always wanted equality to mean."],
 [("Type", "A collection of terms, such as Nat or Bool. Every term belongs to exactly one type."),
  ("Term", "An element of a type, written a : A."),
  ("Judgment", "A basic claim, such as a : A (a is a term of type A) or a = b : A (definitionally equal)."),
  ("Path", "In HoTT, an identification of two terms of the same type."),
  ("Univalence", "The axiom that equivalent types are equal."),
  ("Propositions as types", "The reading where a statement is a type and a proof is a term of it.")],
 ["a : A means the term a has type A, like 3 : Nat.",
  "Statements are types; proofs are terms.",
  "Equal means connected by a path.",
  "Paths can be reversed and composed, like loops on a map.",
  "Univalence: equivalent types are equal.",
  "HoTT gives a foundation that proof assistants can check."],
 [T("In ordinary set theory, a thing can belong to many sets, and equality is a yes-or-no fact outside the system. In type theory every thing has a type, born with it, like a passport. The number 3 is a Nat, and that is part of what it is."),
  T("We write a : A for 'a is a term of type A'. We write A -> B for functions from A to B, and A x B for pairs. A new idea comes with a type: Bool has two terms, true and false. Nat has zero and a successor operation, so 0, 1, 2 and so on."),
  T("A judgment is a basic assertion that the rules can check. 3 : Nat is a judgment, and so is 2 + 1 = 3 : Nat, which says the two sides compute to the same thing. Judgments are about computation. They are not things you prove inside the theory."),
  T("The surprise is that logic comes for free. A statement like 'A implies B' is read as the function type A -> B, and a proof of it is a function that turns proofs of A into proofs of B. This is the Curry-Howard idea, and the next chapters build it up."),
  T("Then comes the homotopy. Equality of two terms a and b of type A is itself a type, written a = b. A term of it is a path from a to b. Two paths can be equal too, by a path between paths. The tower of paths between paths gives each type a shape."),
  T("Vladimir Voevodsky noticed in the 2000s that this matches homotopy theory. The program, with Awodey, Warren, Coquand, Shulman and many others, produced the HoTT book in 2013. Its flagship idea, univalence, says equivalent types may be treated as equal.")],
 [("What does a : A mean?", ["a is a term of type A", "a is a subset of A", "a equals A", "a implies A"], 0, "Typing judgment."),
  ("In HoTT, what is a proof of a = b?", ["A path from a to b", "A number", "A truth table", "A set"], 0, "An identification."),
  ("Which idea does homotopy theory supply?", ["Shapes up to deformation", "Counting primes", "Sorting lists", "Compiling code"], 0, "Spaces and paths."),
  ("What does univalence say?", ["Equivalent types are equal", "All types are sets", "Every type is Bool", "Paths do not exist"], 0, "Transfer along equivalences."),
  ("A statement 'A implies B' is read as...", ["The function type A -> B", "The pair A x B", "The type Nat", "A path"], 0, "Curry-Howard."),
  ("Is 2 + 1 = 3 : Nat a theorem or a judgment?", ["A judgment about computation", "An axiom", "A path between paths", "False"], 0, "Both sides compute to the same value.")],
 [("a : A", "term a has type A"), ("A -> B", "functions from A to B"), ("a = b", "the type of paths from a to b"), ("Univalence", "equivalent types are equal"), ("Judgment", "a basic claim the rules can check")],
 [MATCH("Match the notation", "Pair each notation with its reading.", [("a : A", "a is a term of type A"), ("A -> B", "function type"), ("A x B", "pair type"), ("a = b", "type of paths from a to b")]),
  FILL("The core slogans", "In HoTT, propositions are {{types}}, proofs are {{terms}}, and equalities are {{paths}}."),
  PL("Judge a term", "Write type_of(expr). An expression is a list: ['num', n] has type 'Nat'; ['bool', b] has type 'Bool'; ['pair', e1, e2] has type '(' + T1 + ' x ' + T2 + ')'; ['add', e1, e2] has type 'Nat' if both parts are Nat, otherwise 'error'; ['if', c, a, b] has the type of a if c is Bool and a and b have the same type, otherwise 'error'. Any 'error' inside makes the result 'error'.", "type_of(expr)", '''
def type_of(expr):
    k = expr[0]
    if k == "num":
        return "Nat"
    if k == "bool":
        return "Bool"
    if k == "pair":
        a = type_of(expr[1])
        b = type_of(expr[2])
        if a == "error" or b == "error":
            return "error"
        return "(" + a + " x " + b + ")"
    if k == "add":
        if type_of(expr[1]) == "Nat" and type_of(expr[2]) == "Nat":
            return "Nat"
        return "error"
    if k == "if":
        c = type_of(expr[1])
        a = type_of(expr[2])
        b = type_of(expr[3])
        if c == "Bool" and a == b and a != "error":
            return a
        return "error"
    return "error"
''', [[["num", 3]], [["bool", True]], [["pair", ["num", 1], ["bool", False]]], [["add", ["num", 1], ["num", 2]]], [["add", ["num", 1], ["bool", True]]],
      [["if", ["bool", True], ["num", 1], ["num", 2]]], [["if", ["num", 1], ["num", 1], ["num", 2]]], [["if", ["bool", False], ["num", 1], ["bool", True]]]], "Recurse on the parts, and return 'error' when a rule is broken.")]
))

CHS.append(CH(
 "Functions, pairs and dependent types",
 ("Pi and Sigma", [
  "Function type | is | A to B",
  "Dependent function | is | Pi type",
  "Pair type | is | A times B",
  "Dependent pair | is | Sigma type",
  "Pi type | is | A product",
  "Sigma type | is | A sum",
  "Fibre | depends on | A point"]),
 ["A dependent type is a family of types B(x) indexed by x : A. For each x you get a type, called the fibre over x.",
  "A dependent function type, Pi over x : A of B(x), has functions that send each x to a term in its own fibre B(x). A dependent pair type, Sigma over x : A of B(x), holds pairs of a point x and a term in the fibre over x.",
  "When B does not depend on x, Pi becomes the function type A -> B and Sigma becomes the product A x B. Counting terms of finite types shows the names: Pi multiplies, Sigma adds."],
 [("Dependent type", "A family of types B(x), one for each term x of A."),
  ("Pi type", "The type of dependent functions; its size is a product of the fibre sizes."),
  ("Sigma type", "The type of dependent pairs; its size is a sum of the fibre sizes."),
  ("Fibre", "The type B(x) sitting over a point x."),
  ("Universe", "A type whose terms are types, written U.")],
 ["Pi: for all. Sigma: there exists.",
  "|Pi x:A. B(x)| = product of |B(x)|.",
  "|Sigma x:A. B(x)| = sum of |B(x)|.",
  "Non-dependent Pi is A -> B; non-dependent Sigma is A x B.",
  "A universe U holds small types as terms."],
 [T("Think of a school. For each student x there is a set B(x) of classes the student attends. This is a family indexed by students. That is exactly a dependent type."),
  T("A Pi type is a rule that picks one class for every student. A Sigma type is a single pair: one chosen student together with one of that student's classes. 'For all' goes with Pi, and 'there exists' goes with Sigma."),
  T("Count with finite types. If A has 3 students and every student has 2 classes, a rule that picks one class for each student has 2 x 2 x 2 = 8 choices. A single pair of student and class has 3 x 2 = 6 choices, which is a sum 2 + 2 + 2."),
  T("When every fibre is the same type B, the Pi type is the ordinary function type A -> B with |B| to the power |A| terms. The Sigma type is the product A x B. Dependence adds nothing new, so the usual types are special cases."),
  T("To talk about families of types we need types as terms. A universe U is a type whose terms are types. The family B : A -> U assigns each point a type. Writing U : U would cause paradoxes, so in practice there is a hierarchy U0, U1, U2 and so on.")],
 [("What does a Pi type collect?", ["Dependent functions", "Dependent pairs", "Paths", "Universes"], 0, "For all."),
  ("What does a Sigma type collect?", ["Dependent pairs", "Dependent functions", "Booleans", "Proofs of False"], 0, "There exists."),
  ("If A has 3 points and each fibre has 2, how big is the Sigma type?", ["6", "8", "5", "9"], 0, "2 + 2 + 2."),
  ("If A has 3 points and each fibre has 2, how big is the Pi type?", ["8", "6", "5", "9"], 0, "2 x 2 x 2."),
  ("Non-dependent Pi becomes...", ["A -> B", "A x B", "A + B", "A = B"], 0, "Ordinary functions."),
  ("What is a universe?", ["A type of types", "A proof", "A path", "A number"], 0, "U.")],
 [("Pi", "for all; product of fibres"), ("Sigma", "there exists; sum of fibres"), ("Fibre", "B(x) over x"), ("Universe", "a type of types")],
 [MATCH("Match logic to type", "Pair each statement with its type former.", [("for all x, B(x)", "Pi type"), ("there exists x with B(x)", "Sigma type"), ("A implies B", "A -> B"), ("A and B", "A x B")]),
  PL("Count terms", "Write count_type(kind, fibre_sizes). fibre_sizes is a list with one size for each point of A. If kind is 'pi' return the product of the sizes; if kind is 'sigma' return the sum of the sizes. The product of an empty list is 1 and the sum is 0.", "count_type(kind, fibre_sizes)", '''
def count_type(kind, fibre_sizes):
    if kind == "pi":
        r = 1
        for s in fibre_sizes:
            r = r * s
        return r
    r = 0
    for s in fibre_sizes:
        r = r + s
    return r
''', [["pi", [2, 2, 2]], ["sigma", [2, 2, 2]], ["pi", [1, 3, 2]], ["sigma", [1, 3, 2]], ["pi", []], ["sigma", []], ["pi", [2, 0, 3]]], "Multiply for pi and add for sigma."),
  PL("Function counts", "Write count_functions(a, b): the number of ordinary functions from a type with a points to a type with b points. This is b to the power a (note that 0 to the power 0 is 1).", "count_functions(a, b)", '''
def count_functions(a, b):
    r = 1
    for i in range(a):
        r = r * b
    return r
''', [[3, 2], [2, 3], [0, 0], [0, 5], [4, 1], [3, 0]], "Multiply b by itself a times.")]
))

CHS.append(CH(
 "Propositions as types: Curry-Howard",
 ("Curry-Howard", [
  "Proposition | is | A type",
  "Implication | is | Function",
  "Conjunction | is | Pair",
  "Disjunction | is | Sum type",
  "False | is | Empty type",
  "Negation | is | Map to empty",
  "Proof | is | A program"]),
 ["Under the Curry-Howard correspondence, a logical formula is a type and a proof of it is a program of that type. Proving a theorem and writing a program are the same activity.",
  "Implication is a function type, and is proved by a function. And is a pair type. Or is a sum type, with a left and a right case. False is the empty type, and not-A means A -> False.",
  "Excluded middle and double negation elimination have no general proof in pure type theory. Statements that need them are not provable constructively."],
 [("Curry-Howard", "The correspondence between proofs and programs, and between formulas and types."),
  ("Lambda abstraction", "Writing a function as a binder, lam x. body."),
  ("Application", "Using a function on an argument, f a."),
  ("Empty type", "The type with no terms; it stands for False."),
  ("Constructive logic", "Logic where a proof of 'exists' must produce a witness.")],
 ["A -> B is both implication and function.",
  "A x B is both 'and' and pair.",
  "A + B is both 'or' and sum.",
  "Empty type: false. Not A is A -> Empty.",
  "Excluded middle is not provable in pure type theory."],
 [T("Take the formula A implies A. It is true for any statement A, and the proof is easy: assume A and say it again. As a program that is the identity function lam x. x, of type A -> A."),
  T("Now A implies (B implies A). Assume A, then assume B, and then answer A. As a program, lam x. lam y. x. This function takes two arguments and returns the first. The type of the program is the formula it proves."),
  T("A simple type checker is a proof checker. Given the term lam x : A. x, it finds the type A -> A by looking at how the variable x is used. If the term does not typecheck there is no proof. This is the same logic as in the lab for this chapter."),
  T("And is a pair. To prove A and B, give a proof of each. To use it, take out a half with fst or snd. Or is a tagged choice: inl a or inr b. To use a proof of A or B, you must handle both cases, like a case split in a program."),
  T("False has no proof, so it is the empty type. Not A is the function type A -> False. A proof of not A turns any proof of A into a contradiction. Classical logic adds the law A or not A, but a program of that type would have to decide A, which is impossible in general."),
  T("In Haskell the same ideas show up in everyday code. The function const :: a -> b -> a is the proof of A implies (B implies A), and the type Either a b is a disjunction. A program that compiles is a proof of its type, as long as it terminates and uses no undefined."),
  C("-- Haskell: types as propositions\nidentity :: a -> a\nidentity x = x\n\nconstFn :: a -> b -> a\nconstFn x _ = x\n\nswapPair :: (a, b) -> (b, a)\nswapPair (x, y) = (y, x)", "haskell")],
 [("What does A x B stand for in logic?", ["A and B", "A or B", "Not A", "A implies B"], 0, "Pair."),
  ("What is the proof of A -> A?", ["The identity function", "A pair", "The empty type", "A path"], 0, "lam x. x."),
  ("How is not-A defined?", ["A -> False", "A x False", "A + False", "False -> A"], 0, "Map to the empty type."),
  ("Which law is not provable in pure type theory?", ["A or not A", "A -> A", "A and B implies A", "A -> (B -> A)"], 0, "Excluded middle."),
  ("What is a proof of A or B?", ["inl a or inr b", "A pair (a, b)", "A function", "A path"], 0, "Tagged choice."),
  ("A type checker that accepts a term is also...", ["A proof checker", "A compiler", "A sorter", "A parser"], 0, "Checks the proof.")],
 [("A -> B", "implication = function"), ("A x B", "conjunction = pair"), ("A + B", "disjunction = sum"), ("Empty", "false"), ("Not A", "A -> Empty")],
 [MATCH("Match the connective", "Pair each logical connective with its type.", [("implies", "function type"), ("and", "pair type"), ("or", "sum type"), ("false", "empty type")]),
  FILL("Curry-Howard", "A proof of A implies B is a {{function}} from proofs of A to proofs of B. The identity function proves A implies {{A}}. False is the {{empty}} type."),
  PL("A tiny proof checker", "Write infer(term, ctx). A term is ['var', name], ['lam', name, type, body] or ['app', f, a]. A type is a string such as 'A' or a list ['->', t1, t2]. ctx is a dict from names to types. Return the type of the term, or 'error'. A lam of type t with body type r has type ['->', t, r]. An app needs f of type ['->', t1, t2] and an argument of type t1, and gives t2.", "infer(term, ctx)", '''
def infer(term, ctx):
    k = term[0]
    if k == "var":
        if term[1] in ctx:
            return ctx[term[1]]
        return "error"
    if k == "lam":
        c = {}
        for key in ctx:
            c[key] = ctx[key]
        c[term[1]] = term[2]
        r = infer(term[3], c)
        if r == "error":
            return "error"
        return ["->", term[2], r]
    if k == "app":
        f = infer(term[1], ctx)
        a = infer(term[2], ctx)
        if f == "error" or a == "error":
            return "error"
        if isinstance(f, list) and f[0] == "->" and f[1] == a:
            return f[2]
        return "error"
    return "error"
''', [[["lam", "x", "A", ["var", "x"]], {}], [["lam", "x", "A", ["lam", "y", "B", ["var", "x"]]], {}], [["app", ["lam", "x", "A", ["var", "x"]], ["var", "a"]], {"a": "A"}],
      [["app", ["lam", "x", "A", ["var", "x"]], ["var", "b"]], {"b": "B"}], [["var", "z"], {}], [["lam", "f", ["->", "A", "B"], ["lam", "x", "A", ["app", ["var", "f"], ["var", "x"]]]], {}]],
   "Copy the context before adding the lambda variable.")]
))

CHS.append(CH(
 "Identity types and paths",
 ("Identity types", [
  "Identity type | holds | Paths",
  "Reflexivity | is | The trivial path",
  "Path | has | Inverse",
  "Paths | compose | End to start",
  "Function | acts on | Paths",
  "Transport | moves | Fibres along paths",
  "Path induction | proves | By refl only"]),
 ["For terms a, b : A, the identity type a = b holds the proofs that a and b are equal. In HoTT we call a term p : a = b a path from a to b.",
  "The basic path is refl : a = a. The induction principle for paths, written J, says that to prove something about all paths it is enough to prove it for refl.",
  "From this one rule come symmetry (reverse a path), transitivity (compose paths), ap (apply a function to a path) and transport (move a term along a path)."],
 [("Identity type", "The type a = b of identifications between a and b."),
  ("refl", "The constant path refl_a : a = a."),
  ("Path induction", "The rule that lets you assume a path is refl when proving things about all paths."),
  ("ap", "Applying a function f to a path p : a = b to get ap f p : f a = f b."),
  ("Transport", "Moving a term in a fibre B(a) along a path p : a = b to a term in B(b).")],
 ["refl : a = a.",
  "Reverse: p : a = b gives inverse p : b = a.",
  "Compose: p : a = b and q : b = c give p . q : a = c.",
  "ap f p : f a = f b.",
  "transport B p : B(a) -> B(b)."],
 [T("A path from a to b is a way to get from a to b inside the type. The simplest path stays put: refl at a. Because every type has refl at every point, every point is connected to itself."),
  T("From refl we can build the rest. To reverse a path, just walk it backwards. To follow a path from a to b, then a path from b to c, join them end to start. Joined paths are written p . q. Reverse paths are written p inverse."),
  T("A function carries paths with it. If f : A -> B and p is a path from a to a prime in A, then ap f p is a path from f a to f a prime in B. Functions respect equality, so 'equal inputs give equal outputs' is just ap."),
  T("Transport is the dependent version. A type family B over A tells you what sits over each point. If p is a path from a to b, then transport along p turns a term in B(a) into a term in B(b). Facts about a can be moved to b along any identification."),
  T("Path induction is the elimination rule. To prove a statement about every path p from x to y for all x and y, it is enough to prove it for refl at each x. This one rule gives you inverse, composition, ap and transport, and it is why proofs of equality can be so short."),
  C("-- Agda-style sketch\nsym : {A : Type} {a b : A} -> a == b -> b == a\nsym refl = refl\n\ntrans : {A : Type} {a b c : A} -> a == b -> b == c -> a == c\ntrans refl q = q\n\nap : {A B : Type} (f : A -> B) {a b : A} -> a == b -> f a == f b\nap f refl = refl", "text")],
 [("What is refl?", ["The path from a to a", "A function", "A universe", "A pair"], 0, "Trivial identification."),
  ("What does ap f p give?", ["A path from f a to f b", "A path from a to b", "A pair", "A number"], 0, "Functions respect paths."),
  ("What does transport do?", ["Moves a term along a path", "Reverses a path", "Counts points", "Defines a type"], 0, "Fibres follow paths."),
  ("What is enough to prove for all paths?", ["The case refl", "The case of numbers", "A pair", "Nothing"], 0, "Path induction."),
  ("If p : a = b and q : b = c, p . q is...", ["a = c", "b = b", "a = a", "c = a"], 0, "Composition."),
  ("What is the inverse of p : a = b?", ["A path b = a", "A path a = a", "A function", "A type"], 0, "Walk backwards.")],
 [("refl", "the trivial path"), ("p . q", "compose paths"), ("inverse p", "reverse the path"), ("ap f p", "apply f to a path"), ("transport", "move along a path")],
 [MATCH("Match the path operation", "Pair each operation with its description.", [("refl", "stay put"), ("inverse", "walk backwards"), ("compose", "join end to start"), ("ap", "carry a path through a function"), ("transport", "move a term along a path")]),
  PL("Compose paths", "Paths are lists of points, for example [1, 2, 3] goes from 1 to 3. Write compose(p, q): if the last point of p equals the first point of q, return the joined path with the shared point kept once; otherwise return an empty list. Write the answer for q starting where p ends.", "compose(p, q)", '''
def compose(p, q):
    if len(p) == 0 or len(q) == 0:
        return []
    if p[len(p) - 1] != q[0]:
        return []
    r = []
    for x in p:
        r.append(x)
    for i in range(1, len(q)):
        r.append(q[i])
    return r
''', [[[1, 2, 3], [3, 4]], [[1, 2], [3, 4]], [[5], [5, 6, 7]], [[1, 2, 3], [3]], [[], [1]]], "Skip the first point of q when you copy it."),
  PL("Inverse and ap", "Write invert_apply(p, f): reverse the path p, then apply the function table f (a dict mapping a string of the point to a new point, with points as ints) to every point. Use f[str(x)] for point x. Return the new list.", "invert_apply(p, f)", '''
def invert_apply(p, f):
    r = []
    i = len(p) - 1
    while i >= 0:
        r.append(f[str(p[i])])
        i = i - 1
    return r
''', [[[1, 2, 3], {"1": 10, "2": 20, "3": 30}], [[4], {"4": 0}], [[1, 2, 1], {"1": 5, "2": 6}]], "Walk the list from the end.")]
))

CHS.append(CH(
 "Higher paths and the groupoid structure",
 ("Higher paths", [
  "Path | between | Paths",
  "Types | form | Infinity groupoids",
  "Composition | is | Associative up to path",
  "Inverse | cancels | Up to path",
  "Loop | is | A path to itself",
  "Loop space | holds | Loops at a point",
  "Eckmann-Hilton | makes | Higher loops commute"]),
 ["Paths are terms of the identity type, so two paths p, q : a = b can themselves be compared by the type p = q. A term of that is a 2-path, a path between paths.",
  "Composition of paths is associative, has refl as a unit, and has inverses, but only up to a higher path. A type with this structure is an infinity-groupoid.",
  "A loop at a is a path a = a. The loops at a form the loop space, and its structure is where homotopy groups come from."],
 [("2-path", "A path between two paths with the same ends."),
  ("Groupoid", "A structure with objects, reversible arrows, composition and identities."),
  ("Loop", "A path from a point to itself."),
  ("Loop space", "The type of loops a = a at a base point a, written Omega(A, a)."),
  ("Eckmann-Hilton argument", "Two compatible products on a set that share a unit must agree and be commutative.")],
 ["p = q is a type; its terms are 2-paths.",
  "Associativity: (p . q) . r = p . (q . r) by a path.",
  "p . inverse p = refl by a path.",
  "Loops at a form the loop space Omega(A, a).",
  "Each type is a tower of paths: an infinity-groupoid."],
 [T("Take a map of a city with one-way and two-way streets. A path is a route. Two routes with the same ends are different, but you can ask whether one can be smoothly bent into the other. If so, there is a 2-path between them."),
  T("The laws of composition hold up to such bends. Joining three routes in one order or the other gives routes that are not identical, but they are connected by a bend. Going out and back along the same route can be shrunk to staying put, up to a bend."),
  T("There is no end to the tower, since 2-paths are also compared, giving 3-paths, and so on. A type with all these layers is an infinity-groupoid. This is how type theory sees a space: as points, paths, paths between paths, forever."),
  T("A loop at a base point a is a path from a to a. The loops at a form the loop space. Composition of loops gives a group-like structure. Taking loops again, loops of loops, gives the higher loop spaces, and those are commutative by the Eckmann-Hilton argument."),
  T("In the lab you work with the simplest model: free groupoid words. A route is a word in letters a and b, with capital letters for walking backwards. A letter followed by its inverse cancels. Reducing a word gives its normal form, the shortest route that is equal to it.")],
 [("What is a 2-path?", ["A path between paths", "Two points", "A pair of types", "A universe"], 0, "Higher structure."),
  ("What do loops at a base point form?", ["The loop space", "A function", "A proof of False", "A set of numbers"], 0, "Omega(A, a)."),
  ("What does a . inverse a equal, up to a path?", ["refl", "a", "b", "empty"], 0, "Cancellation."),
  ("A type seen with all its higher paths is...", ["An infinity-groupoid", "A Boolean algebra", "A graph", "A list"], 0, "Towers of paths."),
  ("Why are higher loops commutative?", ["Eckmann-Hilton", "Pythagoras", "Euclid", "Cantor"], 0, "Two products agree."),
  ("Do the groupoid laws hold on the nose?", ["Only up to higher paths", "Always as identity", "Never", "Only for Nat"], 0, "Coherence.")],
 [("Loop", "a path from a to a"), ("Omega(A, a)", "the loop space"), ("2-path", "a path between paths"), ("Groupoid", "objects with invertible arrows"), ("Eckmann-Hilton", "higher loops commute")],
 [ORDER("Reduce a route", "Put the steps in the order you would cancel the word a b B A c.", ["Find the adjacent pair b B", "Cancel it", "Find the new adjacent pair a A", "Cancel it", "Left with c"]),
  PL("Reduce a word", "Write reduce_word(w). w is a string of letters where a lowercase letter is a step and the same capital letter is its inverse, for example 'aA' cancels. Repeatedly remove adjacent pairs of a letter and its inverse (like 'aA' or 'Bb') and return the reduced string.", "reduce_word(w)", '''
def reduce_word(w):
    out = []
    for ch in w:
        if len(out) > 0 and out[len(out) - 1] != ch and out[len(out) - 1].lower() == ch.lower():
            out.pop()
        else:
            out.append(ch)
    return "".join(out)
''', [["abBA"], ["aabAAb"], ["abc"], ["aAbBcC"], ["abBAc"], [""], ["aaAAa"]], "Use a stack: cancel when the top is the opposite case of the same letter."),
  PL("Inverse of a word", "Write word_inverse(w): the inverse of a route reverses the order and swaps the case of each letter. 'abC' becomes 'cBA'.", "word_inverse(w)", '''
def word_inverse(w):
    r = []
    i = len(w) - 1
    while i >= 0:
        ch = w[i]
        if ch == ch.lower():
            r.append(ch.upper())
        else:
            r.append(ch.lower())
        i = i - 1
    return "".join(r)
''', [["abC"], ["a"], [""], ["AbcD"]], "Walk backwards and flip the case.")]
))
