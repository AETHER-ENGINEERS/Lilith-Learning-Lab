#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the LMFDB course. Usage: python3 make_lmfdb_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "lmf"))
import cmk, lm1, lm2, make_apps  # noqa: E402
make_apps.main()
CHS = lm1.CHS + lm2.CHS
PRONOUNCE = {"LMFDB": "L M F D B", "L-function": "L function", "L-functions": "L functions", "Dirichlet": "dee ree klay", "Legendre": "luh zhahndr", "Hasse": "hah suh",
    "Hecke": "heck uh", "Ramanujan": "rah mah noo jan", "Eisenstein": "eye zen stine", "Mordell": "more dell", "Mazur": "mah zoor", "Heegner": "hay g ner", "Frobenius": "fro bay nee us",
    "Sato-Tate": "sah toe tah tay", "Birch": "birch", "Swinnerton-Dyer": "swin ner ton dire", "Langlands": "lang lands", "Maass": "mahss", "Galois": "gal wah", "Deligne": "deh leen",
    "Taniyama": "tah nee yah mah", "Shimura": "shih moo rah", "Weil": "vay", "Wiles": "wiles", "Ribet": "ree bay", "Gauss": "gowss", "Euler": "oiler", "Eratosthenes": "air uh tos thuh neez",
    "isogeny": "eye sodge uh nee", "modularity": "mod you lair uh tee", "Sage": "sayj", "Pari": "pah ree", "Magma": "mag muh", "Tate-Shafarevich": "tate shah fah reh vich", "Gamma_0": "gamma zero"}
SANDBOX = cmk.terminal("LMFDB cheat sheet", "lmf>", "A scripted lookup, not the live database. Try: labels, ap, tau, bsd, modularity", [
    ("labels", ["Number field d.r.D.i: 2.0.3.1 = Q(sqrt(-3)) | Newform N.k.a.x: 11.2.a.a | Elliptic curve class N.a: 11.a"]),
    ("ap", ["Curve of conductor 11: a_2..a_19 = -2, -1, 1, -2, 1, 4, -2, 0 (p = 2, 3, 5, 7, 11, 13, 17, 19)"]),
    ("tau", ["Delta: tau(1..6) = 1, -24, 252, -1472, 4830, -6048"]),
    ("bsd", ["BSD: rank of E(Q) = order of vanishing of L(E, s) at s = 1"]),
    ("modularity", ["Every elliptic curve over Q is modular: a_p(E) = a_p(f) for a weight 2 newform f of level = conductor"]),
])
EXAM = [
 ("What does LMFDB stand for?", ["L-functions and Modular Forms Database", "Large Modular Fields Data Bank", "Linear Maps and Fields DB", "Lattice Modules Forms DB"], 0, "A number theory atlas."),
 ("What does 2.0.3.1 label?", ["Q(sqrt(-3))", "Q(sqrt 5)", "Q(i)", "A cubic"], 0, "d.r.D.i."),
 ("What is 11.2.a.a?", ["A newform", "A number field", "A character", "A group"], 0, "Level 11, weight 2."),
 ("What is (3/7)?", ["-1", "1", "0", "3"], 0, "3 is not a square mod 7."),
 ("Euler's criterion computes...", ["The Legendre symbol", "The gcd", "The rank", "The class number"], 0, "a^((p-1)/2)."),
 ("How many nonzero squares mod an odd prime p?", ["(p-1)/2", "p-1", "p", "2"], 0, "Half."),
 ("What does the class number measure?", ["Failure of unique factorisation", "The degree", "The rank", "The level"], 0, "h = 1 is unique."),
 ("Which discriminant gives class number 1?", ["-163", "-23", "-15", "-84"], 0, "Heegner."),
 ("What is h(-23)?", ["3", "1", "2", "4"], 0, "Three reduced forms."),
 ("What does a prime dividing the discriminant do?", ["Ramifies", "Splits", "Is inert", "Disappears"], 0, "Ramification."),
 ("What is chi(3) for the nontrivial character mod 4?", ["-1", "1", "0", "3"], 0, "3 is 3 mod 4."),
 ("What does an Euler product show?", ["A series factors over primes", "It is finite", "It diverges", "It is real"], 0, "Unique factorisation."),
 ("When is y^2 = x^3 + ax + b smooth?", ["4a^3 + 27b^2 nonzero", "a = 0", "b = 0", "always"], 0, "Discriminant."),
 ("What does the rank count?", ["Independent infinite-order points", "Torsion points", "Bad primes", "The degree"], 0, "Free part."),
 ("What did Mazur classify?", ["Torsion over Q", "Class numbers", "Ranks", "Levels"], 0, "Fifteen groups."),
 ("What is a_p?", ["p + 1 minus the number of points", "The rank", "The conductor", "The level"], 0, "Trace of Frobenius."),
 ("Hasse's bound says...", ["|a_p| <= 2 sqrt p", "a_p = 0", "a_p > p", "a_p is prime"], 0, "Small traces."),
 ("For the conductor 11 curve, a_2 is...", ["-2", "2", "0", "1"], 0, "From the table."),
 ("What do bad primes divide?", ["The conductor", "The rank", "The torsion", "The class number"], 0, "Bad reduction."),
 ("What is q in a q-expansion?", ["e^(2 pi i z)", "A prime", "The level", "The weight"], 0, "A coordinate."),
 ("What is Delta?", ["A weight 12 cusp form of level 1", "A weight 2 form", "An Eisenstein series", "A curve"], 0, "q prod (1-q^n)^24."),
 ("What is tau(2)?", ["-24", "24", "1", "252"], 0, "Coefficient of q^2."),
 ("What is the q coefficient of E_4?", ["240", "1", "504", "24"], 0, "240 sigma_3(1)."),
 ("What is a cusp form?", ["Vanishes at the cusps", "Has level 1", "Has weight 2", "Has no expansion"], 0, "Starts at n=1."),
 ("What does tau(6) equal?", ["tau(2) tau(3)", "tau(2) + tau(3)", "tau(5)", "0"], 0, "Multiplicative."),
 ("What is tau(4)?", ["-1472", "-576", "1472", "2048"], 0, "tau(2)^2 - 2^11."),
 ("What is a newform?", ["Normalised eigenform not from lower level", "A weight 1 form", "Any modular form", "An Eisenstein series"], 0, "No oldform content."),
 ("What does a Hecke operator do?", ["Acts linearly on modular forms", "Counts points", "Defines a field", "Computes class numbers"], 0, "T_n."),
 ("Riemann zeta is the L-function of...", ["The trivial character", "Delta", "A curve", "A Maass form"], 0, "Sum of n^-s."),
 ("What is a functional equation?", ["A relation between L(s) and L(k-s)", "A polynomial", "A matrix", "A graph"], 0, "Symmetry."),
 ("What does the root number predict?", ["Parity of the rank", "The conductor", "The class number", "The torsion"], 0, "Sign."),
 ("What does the modularity theorem say?", ["Every elliptic curve over Q comes from a modular form", "Every form is a curve", "All ranks are 0", "L-functions have no zeros"], 0, "Matching a_p."),
 ("What equals the conductor of E?", ["The level of its newform", "The weight", "The rank", "The torsion"], 0, "Level."),
 ("What did Wiles prove in 1995?", ["Modularity for semistable curves", "The Riemann hypothesis", "BSD", "Sato-Tate"], 0, "With Taylor."),
 ("What does BSD relate?", ["Rank and order of vanishing at s = 1", "Rank and conductor", "Level and weight", "Torsion and class number"], 0, "A Millennium Problem."),
 ("What is the n = 1 Langlands case?", ["Class field theory", "Modularity", "Fermat's Last Theorem", "Hasse's bound"], 0, "Artin reciprocity."),
 ("Which curves have half of their a_p equal to zero?", ["CM curves", "All curves", "Rank 5 curves", "Conductor 11"], 0, "Complex multiplication."),
 ("How should you treat data in the LMFDB?", ["Check whether it is proven or computed", "Always trust it", "Ignore it", "Never use it"], 0, "Read the notes."),
]
CFG = dict(id="lmfdb", title="The LMFDB: L-functions, Modular Forms and Elliptic Curves",
    subtitle="A guided tour of the L-functions and Modular Forms Database: number fields, characters, elliptic curves, modular forms and L-functions, with Python labs that recompute the data",
    description="Learn the mathematics behind the LMFDB, the free online atlas of number theory. Start with primes and quadratic residues, meet number fields and Dirichlet characters, count points on elliptic curves, compute modular forms such as Delta, and see how the modularity theorem ties curves, forms and L-functions together. Every chapter has labs that recompute what the database lists, plus an elliptic curve explorer.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="lmf", apps={"__CURVES__": "curves.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "lmfdb.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
