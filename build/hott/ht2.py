# -*- coding: utf-8 -*-
"""HoTT course, part 2: homotopy levels, equivalences and univalence, higher inductive types, homotopy groups, practice."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=680):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Homotopy levels: propositions and sets",
 ("Homotopy levels", [
  "Contractible | has | One point",
  "Proposition | has | At most one proof",
  "Set | has | Trivial path spaces",
  "1-type | has | Nontrivial loops",
  "Level n | restricts | Path spaces",
  "Truncation | forces | A lower level",
  "Nat | is | A set"]),
 ["Types come in levels by how complicated their paths are. A contractible type is a single point up to paths. A proposition has at most one term up to paths. A set has no interesting paths between paths.",
  "Level n + 1 means that all path types a = b have level n. The levels start at -2 for contractible, -1 for propositions, 0 for sets and 1 for groupoid-like types.",
  "Truncation squeezes a type into a lower level. For example, a set truncation keeps only which component you are in, forgetting the paths."],
 [("Contractible", "A type with a center point such that every point equals it; level -2."),
  ("Proposition", "A type any two of whose terms are equal; level -1."),
  ("Set", "A type whose path types are propositions; level 0."),
  ("n-type", "A type whose path types are (n-1)-types."),
  ("Truncation", "Turning a type into the closest type at a lower level.")],
 ["Level -2: contractible. Level -1: proposition. Level 0: set.",
  "A proposition has at most one proof.",
  "A set has paths that are all unique.",
  "Nat and Bool are sets.",
  "Truncation forgets higher paths."],
 [T("Look at a type from a distance. If it is just one point with nothing to wiggle, it is contractible, like a single dot. If it has at most one point, so any two proofs are the same, it is a proposition. These behave like true or false in ordinary logic."),
  T("If it has many points but each pair is joined by at most one path, it is a set. The natural numbers are a set: 3 is 3 in one way only. Sets are what ordinary mathematics uses, and in HoTT they are a special case."),
  T("If the paths of a type can themselves differ, but the paths between paths are unique, the type is a 1-type, or a groupoid. A circle is the typical example. Its loops are counted by the integers, which is the first interesting homotopy."),
  T("The level of a type is a property, not a choice. Sigma and Pi types preserve levels. A function type into a proposition is a proposition. This is why logic with propositions works well in HoTT: the usual rules hold."),
  T("Truncation makes the right statement for 'there exists'. A plain Sigma type remembers which witness, but we often only want to know that one exists. Propositional truncation squashes the Sigma type to a proposition, so existence means no more than just that it exists.")],
 [("What level is a contractible type?", ["-2", "-1", "0", "1"], 0, "A point."),
  ("A proposition has...", ["At most one term up to paths", "Exactly two terms", "Infinitely many", "No terms"], 0, "Level -1."),
  ("Is Nat a set?", ["Yes", "No", "Only after truncation", "Only in Agda"], 0, "Unique equalities."),
  ("What does truncation do?", ["Forgets higher paths", "Adds paths", "Deletes the type", "Counts points"], 0, "Lowers the level."),
  ("What is a typical 1-type?", ["The circle", "A point", "Bool", "Empty"], 0, "Nontrivial loops."),
  ("Which levels are logic's propositions?", ["-1", "0", "1", "2"], 0, "Squashed to a mere yes or no.")],
 [("Level -2", "contractible"), ("Level -1", "proposition"), ("Level 0", "set"), ("Level 1", "groupoid"), ("Truncation", "forget higher paths")],
 [MATCH("Match the level", "Pair each type with its homotopy level.", [("A single point", "contractible"), ("The empty type", "proposition"), ("Bool", "set"), ("The circle", "1-type")]),
  PL("Classify a toy type", "A toy type has n points, and each point has the same number of loops (automorphisms). Write level(n, loops, connected). Follow these rules in order: n == 0 gives -1 (the empty type is a proposition); n == 1 and loops == 1 gives -2 (contractible); loops > 1 gives 1 (nontrivial loops); anything else gives 0 (a set). The argument connected is kept for the picture but not needed.", "level(n, loops, connected)", '''
def level(n, loops, connected):
    if n == 0:
        return -1
    if n == 1 and loops == 1:
        return -2
    if loops > 1:
        return 1
    return 0
''', [[0, 1, False], [1, 1, True], [3, 1, False], [1, 2, True], [5, 1, False], [2, 3, False]], "Follow the rules in the order given."),
  PL("Count components", "Write components(n, edges): the number of connected components of a graph with n points 0..n-1 and a list of edges [a, b]. This counts the points of the set truncation.", "components(n, edges)", '''
def components(n, edges):
    parent = []
    for i in range(n):
        parent.append(i)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in edges:
        a = find(e[0])
        b = find(e[1])
        if a != b:
            parent[a] = b
    roots = {}
    for i in range(n):
        roots[find(i)] = 1
    return len(roots)
''', [[4, [[0, 1], [2, 3]]], [5, []], [3, [[0, 1], [1, 2]]], [0, []], [6, [[0, 1], [2, 3], [4, 5], [1, 2]]]], "Union-find, or walk the graph from each unseen point.")]
))

CHS.append(CH(
 "Equivalences and univalence",
 ("Univalence", [
  "Equivalence | is | A good bijection",
  "Equivalence | has | An inverse",
  "Identity | gives | Equivalence",
  "Univalence | turns | Equivalence into path",
  "Path in U | is | An equivalence",
  "Transport | follows | Equivalence",
  "Structure | transfers | Along equivalence"]),
 ["An equivalence between types A and B is a function with an inverse up to paths, written A ~ B. For sets it is exactly a bijection.",
  "Every path A = B in the universe gives an equivalence, by transport. The univalence axiom says that this map is itself an equivalence, so equivalences are the same as paths in the universe.",
  "Therefore equivalent types are interchangeable: any property proved for A can be transported to B."],
 [("Equivalence", "A function with a two-sided inverse up to homotopy."),
  ("Bijection", "A function between sets with an inverse; an equivalence of sets."),
  ("Univalence axiom", "The map from paths A = B in a universe to equivalences A ~ B is an equivalence."),
  ("Transport along an equivalence", "Moving structure or properties from one type to an equivalent one."),
  ("Isomorphism", "An invertible structure-preserving map; univalence makes isomorphic structures equal.")],
 ["A ~ B: a function with an inverse up to paths.",
  "For finite sets, equivalence = bijection.",
  "Univalence: (A = B) is equivalent to (A ~ B).",
  "Isomorphic things are equal; use either.",
  "n points have n! self-equivalences."],
 [T("In everyday mathematics, we say two things are 'the same' if they are isomorphic, and then we freely replace one with the other. But set theory does not support this: a statement about one may be false for the other if it looks at the details of how it is built. Univalence fixes that."),
  T("An equivalence is a function f with an inverse g such that going there and back is homotopic to doing nothing. For two sets, this is simply a bijection. For richer types there is extra data, because the homotopies must be coherent."),
  T("Take any path between two types in the universe. Transport along the path gives an equivalence, so every identification yields one. The axiom says the reverse: every equivalence arises, uniquely, from a path. So A = B and A ~ B are the same."),
  T("The consequences are strong. Anything you prove about a type, like a group structure, can be carried over to an equivalent type automatically, with no special proof. The principle that isomorphic structures are indistinguishable becomes a theorem."),
  T("Count to see equivalence at work. A set with 3 points has 3! = 6 self-equivalences, the permutations. The type of equivalences from a 3-point set to itself has exactly six points, and the path space of the 3-point set in the universe also has six points. They match, as univalence predicts.")],
 [("For finite sets, an equivalence is...", ["A bijection", "A subset", "A path of length 2", "A proposition"], 0, "Two-sided inverse."),
  ("What does the univalence axiom say?", ["Paths A = B correspond to equivalences A ~ B", "All types are sets", "Nat is empty", "J has no proof"], 0, "In a universe."),
  ("How many self-equivalences does a 3-point set have?", ["6", "3", "9", "27"], 0, "3 factorial."),
  ("What can you transport along an equivalence?", ["Structure and properties", "Only numbers", "Nothing", "Only proofs of False"], 0, "That is the point."),
  ("Are isomorphic groups equal in HoTT?", ["Yes, by univalence", "No", "Only finite ones", "Only Z"], 0, "Isomorphism becomes identity."),
  ("What gives an equivalence from a path in U?", ["Transport", "Truncation", "Sorting", "Counting"], 0, "Path to equivalence.")],
 [("A ~ B", "equivalence of types"), ("Univalence", "(A = B) ~ (A ~ B)"), ("n!", "equivalences of an n-point set"), ("Bijection", "equivalence of sets")],
 [MATCH("Match the idea", "Pair each idea with its meaning.", [("Equivalence", "function with an inverse up to paths"), ("Bijection", "equivalence between sets"), ("Univalence", "equivalences are paths in the universe"), ("Transport", "carry a property along a path")]),
  PL("Is it an equivalence?", "A function on n points 0..n-1 is given as a list f where f[i] is the image of i. Write is_equiv(f): return True if f is a bijection (every point 0..n-1 is hit exactly once), otherwise False.", "is_equiv(f)", '''
def is_equiv(f):
    n = len(f)
    seen = {}
    for x in f:
        if x < 0 or x >= n:
            return False
        if x in seen:
            return False
        seen[x] = 1
    return len(seen) == n
''', [[[1, 0, 2]], [[0, 0, 1]], [[]], [[2, 1, 0]], [[0, 3, 1]], [[3, 1, 0, 2]]], "Check range and that no value repeats."),
  PL("Inverse of an equivalence", "Write quasi_inverse(f): for a bijection f given as a list, return the list g with g[f[i]] = i. Then going there and back is the identity.", "quasi_inverse(f)", '''
def quasi_inverse(f):
    g = []
    for i in range(len(f)):
        g.append(0)
    for i in range(len(f)):
        g[f[i]] = i
    return g
''', [[[1, 2, 0]], [[0]], [[2, 0, 1, 3]], [[3, 2, 1, 0]]], "Fill the inverse by sending f[i] back to i."),
  PL("Count self-equivalences", "Write count_equivs(n): the number of equivalences from an n-point set to itself, which is n factorial.", "count_equivs(n)", '''
def count_equivs(n):
    r = 1
    for i in range(2, n + 1):
        r = r * i
    return r
''', [[0], [1], [3], [5], [7]], "Multiply 2 through n.")]
))

CHS.append(CH(
 "Higher inductive types: the circle",
 ("Higher inductive types", [
  "HIT | has | Point constructors",
  "HIT | has | Path constructors",
  "Circle | has | A base point",
  "Circle | has | A loop",
  "Interval | has | Two ends",
  "Interval | is | Contractible",
  "Suspension | glues | Two cones"]),
 ["An ordinary inductive type lists point constructors. A higher inductive type, or HIT, may also list path constructors: new equalities that must hold.",
  "The circle S1 has one point base and one path loop : base = base. The interval has two points and a path joining them. Spheres and other shapes are built the same way.",
  "These are the types that let HoTT reason about real shapes directly."],
 [("Higher inductive type", "A type defined by point constructors and path constructors."),
  ("Circle S1", "The HIT with a point base and a loop base = base."),
  ("Interval", "The HIT with points 0, 1 and a path between them; it is contractible."),
  ("Suspension", "The HIT with two poles and a path from north to south for every point of the original type."),
  ("Recursion principle", "To map out of a HIT, say where each constructor goes.")],
 ["S1: base : S1 and loop : base = base.",
  "Interval: two ends joined by a path; it is contractible.",
  "Suspension of S^n is S^(n+1).",
  "To map out of S1, give a point and a loop in the target.",
  "HITs add shape, not just data."],
 [T("Imagine defining the natural numbers: zero, and successor. Now imagine a type with one point, and one path from that point back to itself. That is the circle. It has base, a point, and loop, an identification of base with itself that is not equal to refl."),
  T("The loop is not trivial, and that is the whole point. A path that goes around once is different from standing still. Going around twice gives a different path again. The paths base = base look like the integers: loop to the n for any whole number n, with negative numbers meaning the other way."),
  T("To define a function out of the circle you must say where base goes and what loop goes to. A point in the target and a loop at that point are enough. This is the recursion principle, and for the circle it means that maps S1 to X are the same as loops in X."),
  T("The interval has two points, zero and one, and a path between them. It looks like a line, and it is contractible. Because it has a path from zero to one, it gives a way to prove that equal functions are equal by a path, which is function extensionality."),
  T("The suspension of a type A has a north pole and a south pole, and for every point of A a path from north to south. The suspension of two points is a circle, and the suspension of a circle is a two-sphere. Spheres of every dimension come out by repeating it.")],
 [("What does a HIT add to an inductive type?", ["Path constructors", "Faster code", "More universes", "Fewer points"], 0, "Equalities."),
  ("What are the constructors of S1?", ["base and loop", "zero and succ", "true and false", "inl and inr"], 0, "A point and a loop."),
  ("Is loop equal to refl in S1?", ["No", "Yes", "Only for n = 1", "Always"], 0, "That is what makes S1 interesting."),
  ("Is the interval contractible?", ["Yes", "No", "Only in Agda", "It is a circle"], 0, "Collapses to a point."),
  ("What is the suspension of S1?", ["The two-sphere S2", "The interval", "A point", "S1"], 0, "Raises dimension."),
  ("To map out of S1 you give...", ["A point and a loop in the target", "Two numbers", "A set", "A function"], 0, "Recursion principle.")],
 [("S1", "base and loop"), ("Interval", "two ends joined by a path"), ("Suspension", "two poles and paths between"), ("HIT", "inductive type with paths")],
 [APP("CIRCLE", "Walk around the circle", "Press loop, inverse loop or the other buttons to build a route around the circle. The word is reduced for you, and the winding number counts how many times you went round. Reach a winding number of 3 or -3 to complete this lab."),
  MATCH("Match the type to its constructors", "Pair each type with how it is defined.", [("Circle", "a point and a loop"), ("Interval", "two points and a path"), ("Nat", "zero and successor"), ("Bool", "true and false")]),
  PL("Winding number", "A route on the circle is a string of letters: 'l' goes around once forwards and 'L' goes around once backwards. Write winding(w): the number of l minus the number of L. Routes with the same winding number are equal paths.", "winding(w)", '''
def winding(w):
    n = 0
    for ch in w:
        if ch == "l":
            n = n + 1
        elif ch == "L":
            n = n - 1
    return n
''', [["lll"], ["llL"], ["lLlL"], [""], ["LLLl"], ["lllLLLL"]], "Count up for l and down for L."),
  PL("Loop to the power n", "Write loop_power(n): the route that goes around n times, as a string. For positive n use n copies of 'l'; for negative n use abs(n) copies of 'L'; for 0 return an empty string.", "loop_power(n)", '''
def loop_power(n):
    if n >= 0:
        return "l" * n
    return "L" * (0 - n)
''', [[3], [-2], [0], [1], [-5]], "Pick l or L depending on the sign.")]
))

CHS.append(CH(
 "Homotopy groups and the fundamental group of the circle",
 ("Homotopy groups", [
  "Loop space | gives | Fundamental group",
  "pi1 of circle | is | The integers",
  "Encode-decode | proves | The theorem",
  "Cover | is | A type family",
  "Sphere | has | Homotopy groups",
  "pi n | is | n-fold loops",
  "Freudenthal | stabilizes | pi k of spheres"]),
 ["The n-th homotopy group of a pointed type is the set of n-fold loops, with 'same up to a path' as equality. For n = 1 this is the fundamental group.",
  "The fundamental group of the circle is the integers. In HoTT the proof uses a type family over the circle, whose fibre over every point is the integers and where transport along loop adds one.",
  "The homotopy groups of spheres are a famous hard table. Some entries are easy, and some are still being computed."],
 [("Fundamental group", "The group of loops at a base point up to paths; pi1(A, a)."),
  ("Homotopy group", "pi_n(A, a), the n-fold loops at a, with truncation to a set."),
  ("Encode-decode method", "Prove a path space is some type by building maps in both directions using transport."),
  ("Universal cover", "A type family over the circle with fibre Z, used to prove pi1(S1) = Z."),
  ("Freudenthal suspension theorem", "Suspension eventually becomes an equivalence on low homotopy groups.")],
 ["pi1(S1) = Z: loops are counted by integers.",
  "Encode: send a loop to its winding number.",
  "Decode: send n to loop to the n.",
  "pi_k(S^n) = 0 for k < n; pi_n(S^n) = Z.",
  "Stable groups appear by Freudenthal."],
 [T("Use a rope and a pole. A loop of rope around the pole can be undone only by unwinding it. How many times it winds around, and in which direction, is an integer. This count is what the fundamental group of the circle measures."),
  T("To prove the group of loops at base in S1 is Z in HoTT, first define a family of types over the circle. Its fibre at every point is Z, but going around the loop shifts the integers by one. So transport along loop is adding one."),
  T("Then encode: transport the integer 0 along a given path to get an integer, which counts the winding. Decode: for n, go around the loop n times. The two maps cancel. This is called the encode-decode method, and it is how most path spaces are computed in HoTT."),
  T("Higher homotopy groups come from loops of loops. The circle has none: pi_k of S1 is trivial for k above 1. The two-sphere is different. It has pi_2 = Z, and also pi_3 = Z, a famous surprise from the Hopf fibration."),
  T("Spheres have a table that grows ever more complex, with finite groups like Z/2 and Z/12 scattered in it. The Freudenthal theorem says that after enough suspensions the groups stop changing, which gives the stable homotopy groups. HoTT proves such theorems in the same language as everything else.")],
 [("What is pi1 of the circle?", ["The integers", "Zero", "The reals", "Z mod 2"], 0, "Winding numbers."),
  ("What does transport along loop do in the cover?", ["Adds one", "Does nothing", "Doubles", "Negates"], 0, "Shifts Z."),
  ("What is pi_2 of the two-sphere?", ["Z", "0", "Z/2", "Z/12"], 0, "Same dimension."),
  ("What is pi_3 of the two-sphere?", ["Z", "0", "Z/2", "Z/12"], 0, "The Hopf fibration."),
  ("Which method proves pi1(S1) = Z?", ["Encode-decode", "Induction on Nat only", "Truncation only", "Brute force"], 0, "Two maps."),
  ("What does a higher homotopy group count?", ["Loops of loops", "Prime numbers", "Points", "Functions"], 0, "n-fold loops.")],
 [("pi1(S1)", "the integers Z"), ("pi_n(S^n)", "Z"), ("pi_3(S2)", "Z by Hopf"), ("Encode-decode", "build both maps by transport")],
 [MATCH("Match the group", "Pair each homotopy group with its value.", [("pi_1(S1)", "Z"), ("pi_2(S2)", "Z"), ("pi_3(S2)", "Z"), ("pi_2(S1)", "0")]),
  PL("Encode a loop", "Write encode(w): the winding number of a route written with 'l' (forward) and 'L' (back); then the decoded route is loop_power of that number. Return the pair [n, route] where n is the winding number and route is the shortest equivalent string made of only 'l' (when n is positive) or only 'L' (when n is negative).", "encode(w)", '''
def encode(w):
    n = 0
    for ch in w:
        if ch == "l":
            n = n + 1
        elif ch == "L":
            n = n - 1
    if n >= 0:
        return [n, "l" * n]
    return [n, "L" * (0 - n)]
''', [["lLlll"], ["LLl"], [""], ["lL"], ["LLLLL"]], "Compute n, then rebuild the shortest route."),
  PL("Sphere homotopy table", "Write pi_sphere(n, k) for a small table: return the group as a string. pi_k(S^n) is '0' when k is less than n; 'Z' when k equals n. Use the known values: pi_3(S2) = 'Z', pi_4(S2) = 'Z/2', pi_5(S2) = 'Z/2', pi_4(S3) = 'Z/2', pi_5(S3) = 'Z/2', pi_6(S3) = 'Z/12', and for any n = 1 and k > 1 the group is '0'. Anything else in the table you were not given: return '?'.", "pi_sphere(n, k)", '''
def pi_sphere(n, k):
    if n == 1:
        if k == 1:
            return "Z"
        return "0"
    if k < n:
        return "0"
    if k == n:
        return "Z"
    table = {"2,3": "Z", "2,4": "Z/2", "2,5": "Z/2", "3,4": "Z/2", "3,5": "Z/2", "3,6": "Z/12"}
    key = str(n) + "," + str(k)
    if key in table:
        return table[key]
    return "?"
''', [[1, 1], [1, 3], [2, 1], [2, 2], [2, 3], [3, 6], [4, 4], [3, 7], [2, 4]], "Handle n = 1 first, then the diagonal, then the table.")]
))

CHS.append(CH(
 "Cubical type theory and proof assistants",
 ("Practice", [
  "HoTT book | explains | The theory",
  "Cubical Agda | computes | Univalence",
  "Rocq | supports | HoTT library",
  "Lean | offers | Mathlib",
  "Cubical | uses | Interval variables",
  "Univalence | computes in | Cubical",
  "Haskell | illustrates | Curry-Howard"]),
 ["Plain HoTT assumes univalence as an axiom, so programs using it can get stuck. Cubical type theory builds paths from an interval, so univalence computes.",
  "Cubical Agda is a proof assistant with these features. Rocq (formerly Coq) has HoTT libraries, and Lean has a large library of ordinary mathematics.",
  "The HoTT book, free online, is the standard introduction. This course is a gentle path to it."],
 [("Cubical type theory", "A version of type theory where paths are functions from an interval, and univalence has computational meaning."),
  ("Cubical Agda", "A variant of Agda with cubical features."),
  ("Proof assistant", "Software that checks formal proofs written as typed terms."),
  ("Function extensionality", "Functions that agree at every point are equal; provable via the interval."),
  ("HoTT book", "Homotopy Type Theory: Univalent Foundations of Mathematics, 2013.")],
 ["Cubical: a path is a function from the interval.",
  "Univalence computes in cubical type theory.",
  "Agda, Rocq and Lean can all check proofs.",
  "The HoTT book is free and written by a large group.",
  "Types you write in Haskell show the idea in small."],
 [T("The axiom of univalence is added from outside to plain type theory. That is fine for a proof, but a program built with it cannot always run, because the axiom has no computation rule. This bothers people who like programs that evaluate."),
  T("Cubical type theory makes paths concrete. A path from a to b is a function from an interval, taking a at one end and b at the other. With this, composition, transport and univalence all compute. It also gives function extensionality for free."),
  T("To try this yourself, use a proof assistant. Cubical Agda has the new features built in. Rocq has a HoTT library and Lean has a very large collection of mathematics, though with different foundations. You give each one terms, and it checks the types."),
  T("Haskell cannot state dependent types fully, but it can show the main ideas. A GADT can index a type by a value, a type class can carry evidence, and phantom types can mark facts at compile time. These give a feel for how types carry proofs."),
  T("Where to go next? Read the first chapters of the HoTT book, then try path induction and the circle in a proof assistant. Compute pi1(S1) once yourself. After that the rest of the book, about higher inductive types, cohomology and the cumulative hierarchy, is open to you."),
  C("-- Haskell: a vector indexed by its length (a dependent-type taste)\n{-# LANGUAGE GADTs, DataKinds, KindSignatures #-}\ndata Nat = Z | S Nat\n\ndata Vec (n :: Nat) a where\n  Nil  :: Vec 'Z a\n  Cons :: a -> Vec n a -> Vec ('S n) a\n\n-- head only accepts a nonempty vector, checked by the type\nvhead :: Vec ('S n) a -> a\nvhead (Cons x _) = x", "haskell")],
 [("Why do we want cubical type theory?", ["So univalence computes", "To remove types", "To make Nat finite", "To avoid paths"], 0, "Computational content."),
  ("What is a path in cubical type theory?", ["A function from an interval", "A pair", "A set", "A type of numbers"], 0, "Interval maps."),
  ("Which tool has cubical features built in?", ["Cubical Agda", "A spreadsheet", "A text editor", "A browser"], 0, "A proof assistant."),
  ("What is the HoTT book?", ["A free textbook", "A video game", "A compiler", "A database"], 0, "2013."),
  ("What does vhead guarantee in the Vec example?", ["The vector is nonempty", "The vector is sorted", "The vector has 3 items", "The vector is empty"], 0, "Checked by the type."),
  ("What is a proof assistant?", ["Software that checks formal proofs", "A search engine", "A calculator", "A word processor"], 0, "Typed terms.")],
 [("Cubical", "paths from an interval, univalence computes"), ("Agda", "dependently typed language and proof assistant"), ("Rocq", "formerly Coq"), ("Lean", "proof assistant with Mathlib"), ("HoTT book", "free textbook, 2013")],
 [APP("PROPS", "Propositions as types", "Pick a statement to see the program that proves it and its type. Then try excluded middle: no program exists. Look at three statements to complete this lab.", 640),
  MATCH("Match the tool", "Pair each tool with a fact about it.", [("Cubical Agda", "univalence computes"), ("Lean", "large library of mathematics"), ("Rocq", "formerly Coq"), ("Haskell", "shows types as propositions in everyday code")]),
  FILL("Wrap up", "Plain HoTT adds univalence as an {{axiom}}. In cubical type theory a path is a function from the {{interval}}, and univalence {{computes}}."),
  PL("Church numerals", "Church numerals encode numbers as functions that apply f n times. Write church_apply(n, k) where we use the function 'add k' starting at 0: apply the step 'add k' to 0 exactly n times and return the result. This shows a number as a program.", "church_apply(n, k)", '''
def church_apply(n, k):
    x = 0
    for i in range(n):
        x = x + k
    return x
''', [[3, 2], [0, 5], [4, 4], [1, 7], [6, 3]], "Repeat adding k, n times.")]
))
