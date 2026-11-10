#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Homotopy Type Theory course. Usage: python3 make_hott_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "hott"))
import cmk, ht1, ht2, make_apps  # noqa: E402
make_apps.main()
CHS = ht1.CHS + ht2.CHS
PRONOUNCE = {"HoTT": "hot", "Voevodsky": "voh ev sky", "Martin-Lof": "mar tin loff", "univalence": "yoo nih vay lence", "Univalence": "yoo nih vay lence", "univalent": "yoo nih vay lent",
    "homotopy": "hoe mot oh pee", "Homotopy": "hoe mot oh pee", "groupoid": "groop oid", "Groupoid": "groop oid", "Eckmann-Hilton": "eck man hill ton", "Freudenthal": "froy den tall",
    "Agda": "ahg duh", "Rocq": "rock", "Coq": "coke", "GADT": "gad tee", "Hopf": "hopf", "Curry-Howard": "curry how ard", "refl": "reflect", "Sigma": "sig muh", "Pi": "pie",
    "Church": "church", "Coquand": "koh kahn", "Awodey": "ah woh dee", "Shulman": "shool man", "fibre": "fy ber", "fibres": "fy bers", "Omega": "oh may guh", "pi1": "pie one"}
SANDBOX = cmk.terminal("HoTT cheat sheet", "hott>", "A scripted lookup. Try: refl, ap, transport, univalence, circle, levels", [
    ("refl", ["refl : a = a. The trivial path; every point is equal to itself."]),
    ("ap", ["ap f p : f a = f b for p : a = b. Functions respect paths."]),
    ("transport", ["transport B p : B a -> B b. Move a term in the fibre over a to the fibre over b."]),
    ("univalence", ["(A = B) is equivalent to (A ~ B). Equivalent types are equal."]),
    ("circle", ["S1: base : S1, loop : base = base. pi1(S1) = Z."]),
    ("levels", ["-2 contractible, -1 proposition, 0 set, 1 groupoid. Nat and Bool are sets."]),
])
EXAM = [
 ("What does a : A mean?", ["a is a term of type A", "a is a subset of A", "a equals A", "a implies A"], 0, "A typing judgment."),
 ("In HoTT, a proof of a = b is...", ["A path from a to b", "A number", "A set", "A truth value"], 0, "An identification."),
 ("What does a Pi type collect?", ["Dependent functions", "Dependent pairs", "Paths", "Universes"], 0, "For all."),
 ("How big is a Sigma type over 3 points with fibres of size 2?", ["6", "8", "5", "9"], 0, "2 + 2 + 2."),
 ("How big is a Pi type over 3 points with fibres of size 2?", ["8", "6", "5", "9"], 0, "2 x 2 x 2."),
 ("Which type stands for False?", ["The empty type", "The unit type", "Bool", "Nat"], 0, "No terms."),
 ("What is the proof of A implies A?", ["The identity function", "A pair", "A loop", "Nothing"], 0, "lam x. x."),
 ("Which law is not provable in pure type theory?", ["A or not A", "A -> A", "A and B implies A", "A -> B -> A"], 0, "Excluded middle."),
 ("What does ap f p give?", ["A path from f a to f b", "A path from a to b", "A pair", "A number"], 0, "Functions respect paths."),
 ("What does transport do?", ["Moves a term along a path", "Reverses a path", "Counts points", "Defines a type"], 0, "Fibres follow paths."),
 ("What is enough to prove a statement about all paths?", ["The case refl", "The case 0", "Nothing", "Two cases"], 0, "Path induction."),
 ("What is a 2-path?", ["A path between paths", "Two points", "A pair of types", "A function"], 0, "Higher structure."),
 ("What do loops at a base point form?", ["The loop space", "A function", "A proof of False", "A number"], 0, "Omega(A, a)."),
 ("What level is a contractible type?", ["-2", "-1", "0", "1"], 0, "A point."),
 ("A proposition has...", ["At most one term up to paths", "Exactly two terms", "Infinitely many", "No terms"], 0, "Level -1."),
 ("Is Nat a set?", ["Yes", "No", "Only after truncation", "Only in Agda"], 0, "Unique equalities."),
 ("What does univalence say?", ["Paths A = B match equivalences A ~ B", "All types are sets", "J has no proof", "Nat is empty"], 0, "In a universe."),
 ("How many self-equivalences does a 3-point set have?", ["6", "3", "9", "27"], 0, "3 factorial."),
 ("What are the constructors of S1?", ["base and loop", "zero and succ", "true and false", "inl and inr"], 0, "A point and a loop."),
 ("Is loop equal to refl in S1?", ["No", "Yes", "Only for n = 1", "Always"], 0, "That is why it is interesting."),
 ("What is pi1 of the circle?", ["The integers", "Zero", "The reals", "Z mod 2"], 0, "Winding numbers."),
 ("What is pi_3 of the two-sphere?", ["Z", "0", "Z/2", "Z/12"], 0, "The Hopf fibration."),
 ("Which method proves pi1(S1) = Z?", ["Encode-decode", "Brute force", "Truncation only", "Sorting"], 0, "Two maps built by transport."),
 ("Why do we want cubical type theory?", ["So univalence computes", "To remove types", "To avoid paths", "To make Nat finite"], 0, "Computational content."),
 ("What is the HoTT book?", ["A free textbook, 2013", "A game", "A compiler", "A database"], 0, "Written by a large group."),
 ("What does the suspension of S1 give?", ["The two-sphere", "The interval", "A point", "S1"], 0, "Raises dimension."),
]
CFG = dict(id="homotopy-type-theory", title="Homotopy Type Theory",
    subtitle="Types as spaces, proofs as programs, equality as paths: a first course with Python labs and a circle explorer",
    description="A beginner-friendly introduction to homotopy type theory: types and terms, dependent Pi and Sigma types, propositions as types, identity types and paths, higher paths and groupoids, homotopy levels, equivalences and univalence, higher inductive types such as the circle, the fundamental group of the circle, and cubical type theory with proof assistants. Python labs recompute counts, reduce path words and compute winding numbers; two small interactive apps let you explore loops on the circle and propositions as types.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="hott", apps={"__CIRCLE__": "circle.html", "__PROPS__": "props.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "homotopy-type-theory.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
