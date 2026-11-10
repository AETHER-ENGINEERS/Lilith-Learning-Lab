# -*- coding: utf-8 -*-
"""LMFDB course, part 1: the database, integers, number fields, characters, elliptic curves."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}

CHS.append(CH(
 "What the LMFDB is",
 ("The LMFDB", [
  "LMFDB | stores | Number theory objects",
  "Object | has | A label",
  "Elliptic curve | links to | Modular form",
  "Modular form | has | An L-function",
  "Number field | has | A Galois group",
  "Langlands program | connects | The objects"]),
 ["The L-functions and Modular Forms Database (LMFDB) is a free online atlas of objects from number theory: elliptic curves, modular forms, number fields, Dirichlet characters, L-functions, genus 2 curves, Galois groups and more.",
  "Each object has a unique label, a page of properties, and links to related objects. The links are the real point: the same L-function can arise from an elliptic curve and from a modular form.",
  "This course teaches the mathematics behind the main collections and how to read their pages, with Python labs that recompute what the database lists."],
 [("LMFDB", "The L-functions and Modular Forms Database, a collaborative online database of number theory objects."),
  ("Label", "A short code that names an object uniquely, such as 11.a for a class of elliptic curves."),
  ("L-function", "A function of a complex variable built from arithmetic data, such as the Riemann zeta function."),
  ("Modular form", "A highly symmetric complex function on the upper half-plane, described by a q-expansion."),
  ("Langlands program", "A web of conjectures and theorems linking Galois representations, automorphic forms and L-functions.")],
 ["An LMFDB page lists invariants you can recompute and cross-check.",
  "Elliptic curves, modular forms and L-functions are tied by the modularity theorem.",
  "Labels follow patterns: number fields d.r.D.i, newforms N.k.a.x, curves N.a.n.",
  "The database holds computed data, so the data is checkable but not a proof.",
  "Always check the live site: collections grow and pages change."],
 [T("Imagine a map of all the numbers you can build by solving polynomial equations, and every secret tune hidden in their prime numbers. That is roughly what number theorists study, and the LMFDB is an atlas of it. It holds tens of millions of objects: number fields, elliptic curves over the rationals, modular forms, Dirichlet characters, genus 2 curves, abelian varieties, Artin representations, Maass forms and L-functions. It is open to everyone, with an API."),
  T("Why a database? In number theory, much progress starts with experiments. You compute a thousand examples and see a pattern. The LMFDB stores the computed examples, checks them against each other, and records the relations. For example, take the elliptic curve of conductor 11, y squared plus y equals x cubed minus x squared. Count its points modulo each prime p, and you get a sequence of numbers a_p. Now take the modular form of level 11 and weight 2, and read the coefficients of its q-expansion: they are the same numbers. That coincidence is the modularity theorem, and the database shows it on one page."),
  T("Each collection has its own labels. A newform is labelled level.weight.character.letter, as in 11.2.a.a. An elliptic curve over Q is labelled by its conductor and an isogeny class letter, then numbers: 11.a2. A number field is labelled degree.real places.discriminant.index, as in 2.0.3.1, which is Q of the square root of minus three. Knowing the pattern lets you read a label like a street address."),
  T("This course follows the database's own order. We recall the arithmetic you need (primes, congruences, quadratic residues), meet number fields, Dirichlet characters, elliptic curves and modular forms, and then L-functions, which tie everything together. At each stage there is Python that recomputes what the database lists, such as the a_p of a curve or the coefficients of the modular form Delta. A caution: the database holds computations, not proofs. Treat the numbers as evidence and the theorems as the explanation."),
  T("A note on what we cannot do offline. This course works without internet, so it does not query the live site. You will compute small examples yourself and compare them with the values quoted in the text. When you go online, look at the same objects there, and you will find the same numbers, along with much more.")],
 [("What does LMFDB stand for?", ["L-functions and Modular Forms Database", "Large Modular Forms Data Bank", "Linear Maps and Fields Database", "Lattice Modules and Forms DB"], 0, "A number theory atlas."),
  ("What is a label?", ["A unique code naming an object", "A proof", "A graph", "A formula"], 0, "Like 11.2.a.a."),
  ("What does the modularity theorem link?", ["Elliptic curves and modular forms", "Primes and squares", "Fields and rings", "Graphs and trees"], 0, "Same a_p."),
  ("What does 2.0.3.1 label?", ["Q(sqrt(-3))", "Q(sqrt 5)", "Q(i)", "A cubic field"], 0, "Degree 2, no real places, disc 3."),
  ("Is the data in the database a proof?", ["No, it is computed evidence", "Yes always", "Only for curves", "Only for fields"], 0, "Experiments suggest theorems."),
  ("What is 11.2.a.a?", ["A newform label", "A number field", "A Galois group", "A character"], 0, "Level 11, weight 2.")],
 [("LMFDB", "L-functions and Modular Forms Database"), ("11.2.a.a", "Newform of level 11, weight 2"), ("2.0.3.1", "Q(sqrt(-3))"), ("a_p", "Trace of Frobenius, p + 1 minus the number of points"), ("Modularity", "Every elliptic curve over Q comes from a modular form")],
 [MATCH("Match object to label style", "Pair each LMFDB object with a label that fits it.", [("Number field", "2.0.3.1"), ("Newform", "11.2.a.a"), ("Elliptic curve class", "11.a"), ("Dirichlet character", "5.2")]),
  FILL("LMFDB basics", "The LMFDB stores {{labelled}} objects. Elliptic curves and modular forms are linked by the {{modularity}} theorem. The data is computed {{evidence}}, not a proof."),
  PL("Read a newform label", "Write parse_newform(label) for a label like '11.2.a.a' (level.weight.character_orbit.newform_orbit). Return [level, weight, character_orbit, newform_orbit] with level and weight as integers.", "parse_newform(label)", '''
def parse_newform(label):
    p = label.split(".")
    return [int(p[0]), int(p[1]), p[2], p[3]]
''', [["11.2.a.a"], ["1.12.a.a"], ["23.2.a.a"], ["37.2.b.a"]], "Split on dots and convert the first two parts to int."),
  PL("Read a number field label", "Write parse_field(label) for a label like '2.0.3.1' (degree.real_places.abs_discriminant.index). Return [degree, real_places, abs_discriminant, index] as integers.", "parse_field(label)", '''
def parse_field(label):
    return [int(x) for x in label.split(".")]
''', [["2.0.3.1"], ["2.2.5.1"], ["3.1.23.1"], ["2.0.4.1"]], "Every part is an integer.")]
))

CHS.append(CH(
 "Arithmetic toolkit: primes, congruences and squares",
 ("Arithmetic toolkit", [
  "Prime | divides | Integers",
  "Congruence | works | Modulo n",
  "Residue | is | A square mod p",
  "Legendre symbol | detects | Squares",
  "Euler criterion | computes | The symbol",
  "Reciprocity | links | Two primes"]),
 ["Almost everything in the LMFDB is detected one prime at a time. We need quick tools: primes, congruences modulo n, quadratic residues and the Legendre symbol.",
  "The Legendre symbol (a/p) is 1 if a is a nonzero square mod p, -1 if not, and 0 if p divides a. It is the key to counting points on a curve mod p.",
  "The labs sieve primes and compute the Legendre symbol by Euler's criterion."],
 [("Congruence", "a is congruent to b mod n if n divides a - b."),
  ("Quadratic residue", "A number a such that x squared is congruent to a mod p has a solution."),
  ("Legendre symbol", "(a/p): 1 if a is a square mod p, -1 if not, 0 if p divides a."),
  ("Euler's criterion", "(a/p) is congruent to a^((p-1)/2) mod p."),
  ("Quadratic reciprocity", "A law relating (p/q) and (q/p) for odd primes p and q.")],
 ["Sieve of Eratosthenes finds all primes up to n.",
  "Modular arithmetic: add and multiply, then reduce mod n.",
  "Half of the nonzero residues mod an odd prime p are squares.",
  "(a/p) = a^((p-1)/2) mod p, read as 1 or -1 (p - 1).",
  "Reciprocity: (p/q)(q/p) = (-1)^(((p-1)/2)((q-1)/2)).",
  "Counting solutions mod p is how a_p is defined."],
 [T("The LMFDB looks at numbers prime by prime, so we begin with primes. A prime is a number with exactly two divisors, one and itself. The sieve of Eratosthenes finds all of them up to n: write the numbers, cross out multiples of 2, then of 3, then 5, and the survivors are primes. Everything we do later, such as counting points on a curve, is done modulo a prime p."),
  T("Modular arithmetic means working with remainders. Two integers are congruent mod n if they leave the same remainder when divided by n. On a clock, 15 is congruent to 3 mod 12. Addition and multiplication respect this, so you can reduce at every step. Mod an odd prime p, each nonzero number has an inverse, which makes the residues a field, called F_p."),
  T("Which numbers are squares mod p? Try p = 7. The squares of 1 to 6 are 1, 4, 2, 2, 4, 1, so the nonzero squares are 1, 2 and 4. Exactly half of the nonzero residues are squares. The Legendre symbol records this: (a/p) is 1 for 1, 2, 4, and -1 for 3, 5, 6. Euler's criterion gives a quick test: raise a to the power (p - 1)/2 mod p. You get 1 for a square and p - 1, that is -1, for a non-square."),
  M(r"\left(\frac{a}{p}\right) \equiv a^{(p-1)/2} \pmod p"),
  T("Why does this matter for elliptic curves? To count the points on y squared equals f(x) mod p, you check each x. If f(x) is a nonzero square, there are two values of y; if it is zero, one; if it is a non-square, none. So the number of y for each x is 1 + (f(x)/p). This formula turns point counting into Legendre symbols, and the labs use it directly. Quadratic reciprocity, due to Gauss, relates (p/q) to (q/p) and is the first appearance of the idea that the Langlands program generalises.")],
 [("How many nonzero squares are there mod an odd prime p?", ["(p - 1)/2", "p - 1", "p", "p/2"], 0, "Half."),
  ("What is (3/7)?", ["-1", "1", "0", "3"], 0, "3 is not a square mod 7."),
  ("What does Euler's criterion compute?", ["The Legendre symbol", "The gcd", "The class number", "The discriminant"], 0, "a^((p-1)/2)."),
  ("How many y values for x with f(x) a nonzero square?", ["2", "1", "0", "p"], 0, "Plus and minus root."),
  ("What is F_p?", ["The integers mod a prime", "The reals", "A polynomial", "A curve"], 0, "A field."),
  ("Who proved quadratic reciprocity first?", ["Gauss", "Euler", "Fermat", "Riemann"], 0, "In 1796.")],
 [("(a/p)", "Legendre symbol"), ("a^((p-1)/2)", "Euler's criterion"), ("F_p", "Integers mod p"), ("sieve", "Finds primes"), ("1 + (f(x)/p)", "Number of y for a given x")],
 [MATCH("Squares mod 7", "Match each number to whether it is a square mod 7.", [("1", "square"), ("2", "square"), ("3", "non-square"), ("4", "square"), ("5", "non-square"), ("6", "non-square")]),
  PL("Primes up to n", "Write primes_upto(n): the list of primes up to and including n, using a sieve.", "primes_upto(n)", '''
def primes_upto(n):
    if n < 2:
        return []
    flags = [True] * (n + 1)
    flags[0] = False
    flags[1] = False
    i = 2
    while i * i <= n:
        if flags[i]:
            j = i * i
            while j <= n:
                flags[j] = False
                j += i
        i += 1
    return [k for k in range(n + 1) if flags[k]]
''', [[1], [2], [20], [50], [100]], "Cross out multiples of each prime starting from its square."),
  PL("The Legendre symbol", "Write legendre(a, p) for an odd prime p. Return 0 if p divides a, 1 if a is a square mod p and -1 otherwise. Use Euler's criterion with pow(a, (p - 1) // 2, p).", "legendre(a, p)", '''
def legendre(a, p):
    a = a % p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1
''', [[1, 7], [3, 7], [2, 7], [5, 11], [0, 5], [10, 13], [6, 13]], "Compute the power mod p, then map p - 1 to -1."),
  FILL("Rules", "The Legendre symbol of a square is {{1}}. A multiple of p gives {{0}}. Euler's criterion raises a to the power {{(p-1)/2}}.")]
))

CHS.append(CH(
 "Number fields",
 ("Number fields", [
  "Number field | extends | The rationals",
  "Degree | counts | The dimension",
  "Discriminant | measures | Ramification",
  "Ring of integers | holds | Algebraic integers",
  "Class number | counts | Ideal classes",
  "Galois group | holds | The symmetries"]),
 ["A number field is a finite extension of the rationals, such as Q(sqrt(-3)). The LMFDB lists them by degree, signature and discriminant, with the ring of integers, the class number and the Galois group.",
  "The discriminant tells which primes ramify. The class number measures how far unique factorisation fails. The Galois group records the symmetries of the roots.",
  "The labs compute class numbers of imaginary quadratic fields by counting reduced quadratic forms."],
 [("Number field", "A field containing Q that has finite dimension over Q."),
  ("Discriminant", "An integer that measures how a field differs from Q; the primes dividing it ramify."),
  ("Ring of integers", "The algebraic integers inside a number field."),
  ("Class number", "The size of the ideal class group; it is 1 exactly when factorisation is unique."),
  ("Galois group", "The group of symmetries of the roots of the defining polynomial.")],
 ["Q(sqrt d) has degree 2 and discriminant d (or 4d).",
  "The label d.r.D.i gives degree, real places, |discriminant| and an index.",
  "Class number 1 means unique factorisation of ideals into primes is also element-wise.",
  "Heegner: the imaginary quadratic fields with class number 1 have discriminants -3, -4, -7, -8, -11, -19, -43, -67, -163.",
  "A prime p ramifies in K if it divides the discriminant.",
  "The Galois group of a quadratic field is Z/2."],
 [T("Adjoin the square root of minus three to the rationals, and you get a field Q(sqrt(-3)): numbers of the form a + b times the square root of minus three, with rational a and b. It has dimension two over Q, so degree two. Its complex embeddings come in a conjugate pair, so it has no real places. The LMFDB gives it the label 2.0.3.1: degree 2, zero real places, discriminant of absolute value 3, first such field. Its cousin Q(sqrt 5) is 2.2.5.1, with two real places."),
  T("Every number field has a ring of integers, the elements that satisfy a monic integer polynomial. In Q(i) it is the Gaussian integers Z[i]. Integers can sometimes factor in different ways in the ring of integers. In Z[sqrt(-5)], six equals 2 times 3 and also (1 + sqrt(-5)) times (1 - sqrt(-5)). Factorisation of numbers is not unique, but factorisation of ideals is. The class number h counts how far unique factorisation of numbers fails; h = 1 means it holds. Q(sqrt(-5)) has class number 2."),
  T("The discriminant measures the size of the ring of integers and detects ramification. A prime p ramifies when it divides the discriminant, meaning p generates a product of repeated prime ideals. In Q(sqrt(-3)) only 3 ramifies. Stark and Heegner showed there are exactly nine imaginary quadratic fields with class number 1: discriminants minus 3, 4, 7, 8, 11, 19, 43, 67 and 163. The last one gives the famous near integer e to the pi root 163, which is almost an integer."),
  T("We can compute class numbers of imaginary quadratic fields without any theory of ideals, by counting reduced binary quadratic forms ax^2 + bxy + cy^2 with discriminant D = b^2 - 4ac. A form is reduced if the absolute value of b is at most a, and a is at most c, with b nonnegative when a = c or the absolute value of b equals a. The number of reduced forms of discriminant D is the class number h(D) when D is a fundamental discriminant. The lab does exactly this count and recovers h(-23) = 3 and h(-163) = 1."),
  T("The Galois group records the symmetries of the roots. For a quadratic field, it is the group of two elements swapping the two roots. For a cubic like x^3 - x - 1, which has discriminant -23, the group is the symmetric group S3 of order six. The LMFDB shows the group using a label like 6T2, which names the transitive group of degree 6 and number 2.")],
 [("What is the degree of Q(sqrt(-3))?", ["2", "1", "3", "4"], 0, "Two-dimensional over Q."),
  ("What does the class number measure?", ["Failure of unique factorisation", "The degree", "The number of real places", "The discriminant"], 0, "h = 1 is good."),
  ("Which discriminant has class number 1?", ["-163", "-23", "-15", "-84"], 0, "Heegner."),
  ("What does a prime dividing the discriminant do?", ["Ramifies", "Splits", "Is inert", "Vanishes"], 0, "Repeated prime ideals."),
  ("What is h(-23)?", ["3", "1", "2", "4"], 0, "Three reduced forms."),
  ("What is the Galois group of x^3 - x - 1?", ["S3", "Z/3", "Z/2", "A4"], 0, "Discriminant -23.")],
 [("2.0.3.1", "Q(sqrt(-3))"), ("h = 1", "Unique factorisation"), ("disc -163", "Class number 1"), ("ramified", "Divides the discriminant"), ("S3", "Galois group of a typical cubic")],
 [MATCH("Match the field to its label", "Pair each field with its LMFDB label.", [("Q(sqrt(-3))", "2.0.3.1"), ("Q(i)", "2.0.4.1"), ("Q(sqrt 5)", "2.2.5.1"), ("cubic of disc -23", "3.1.23.1")]),
  PL("Class number by counting forms", "Write class_number(D) for a negative discriminant D: count reduced forms (a, b, c) with b*b - 4*a*c = D, |b| <= a <= c, and b >= 0 when |b| == a or a == c. Return the count. Loop a from 1 while 3*a*a <= -D, b from -a+1 to a.", "class_number(D)", '''
def class_number(D):
    count = 0
    a = 1
    while 3 * a * a <= -D:
        for b in range(-a + 1, a + 1):
            num = b * b - D
            if num % (4 * a) == 0:
                c = num // (4 * a)
                if c >= a and not (a == c and b < 0):
                    count += 1
        a += 1
    return count
''', [[-3], [-4], [-7], [-15], [-23], [-84], [-163]], "For each a and b, c is determined by D; check divisibility and the reduced conditions."),
  FILL("Fields and ramification", "A prime ramifies when it divides the {{discriminant}}. The {{class}} number measures failure of unique factorisation. Exactly {{nine}} imaginary quadratic fields have class number 1.")]
))

CHS.append(CH(
 "Dirichlet characters and their L-functions",
 ("Dirichlet characters", [
  "Character | is | A multiplicative map",
  "Conductor | is | The modulus",
  "Dirichlet L-function | sums | chi(n) / n^s",
  "Zeta | is | The trivial character",
  "Primes in progressions | follow | Nonvanishing L(1)",
  "Euler product | factors | The sum"]),
 ["A Dirichlet character is a function chi on the integers that is periodic mod N, multiplicative and zero when n shares a factor with N. Each gives an L-function, the sum of chi(n)/n^s.",
  "The Riemann zeta function is the case chi = 1. The Dirichlet L-functions prove that arithmetic progressions contain infinitely many primes. The LMFDB lists characters by modulus and Conrey label.",
  "The labs compute a quadratic character and an Euler product."],
 [("Dirichlet character", "A completely multiplicative function mod N that is zero on integers sharing a factor with N."),
  ("Conductor", "The smallest modulus from which the character can be defined."),
  ("L-function", "A Dirichlet series like the sum of chi(n)/n^s, with an Euler product."),
  ("Euler product", "An expression of an L-function as a product over primes."),
  ("Primitive character", "A character not induced from a character of smaller modulus.")],
 ["chi(mn) = chi(m) chi(n); chi(n + N) = chi(n).",
  "The quadratic character mod p is the Legendre symbol.",
  "L(s, chi) = sum chi(n) n^(-s) = product over p of 1/(1 - chi(p) p^(-s)).",
  "Zeta(s) = sum n^(-s) = product of 1/(1 - p^(-s)).",
  "Dirichlet's theorem: infinitely many primes in a + Nk when gcd(a, N) = 1.",
  "The LMFDB label N.k names the character with modulus N and Conrey number k."],
 [T("Take the numbers mod 4 and define chi(n) to be 1 for n congruent to 1, -1 for n congruent to 3, and 0 for even n. This function is multiplicative: chi(3) times chi(3) is chi(9) = 1. It is a Dirichlet character. The associated L-function is 1 - 1/3^s + 1/5^s - 1/7^s and so on. At s = 1 it gives the Leibniz series for pi over four. Dirichlet characters generalise this idea to every modulus."),
  T("The Riemann zeta function is the sum of one over n^s, which is the L-function of the trivial character. Euler found that the sum factors into a product over the primes: zeta(s) is the product over p of 1 over (1 - p to the minus s). This works because every integer factors uniquely into primes. Every Dirichlet L-function has an Euler product too, with the character value chi(p) in each factor, and the product encodes how the character behaves on primes."),
  M(r"L(s,\chi)=\sum_{n\ge1}\frac{\chi(n)}{n^{s}}=\prod_{p}\frac{1}{1-\chi(p)p^{-s}}"),
  T("Dirichlet used these L-functions to prove that every arithmetic progression a, a + N, a + 2N and so on contains infinitely many primes when a and N share no factor. The key is that L(1, chi) is not zero for any nontrivial character. In the LMFDB, a character is listed by its modulus N and Conrey label k, so 5.2 is a character mod 5 with a specific order. The page shows the order, the parity (even or odd), the conductor and the values on generators."),
  T("A character is primitive when it cannot come from a smaller modulus. The conductor is the smallest modulus that works. The Legendre symbol mod an odd prime p is the unique quadratic character, so (a/p) is chi(a) for chi of order two. Its L-function counts how primes split in Q(sqrt p*), where p* is plus or minus p. This is the first example of a deep fact: the behaviour of primes in a number field is encoded in an L-function.")],
 [("What is chi(n) for the character mod 4 at n = 3?", ["-1", "1", "0", "3"], 0, "3 is congruent to 3 mod 4."),
  ("What does an Euler product show?", ["The sum factors over primes", "The sum diverges", "The sum is finite", "The sum is zero"], 0, "Unique factorisation."),
  ("Which L-function is the trivial character's?", ["Riemann zeta", "Delta", "An elliptic curve's", "A Maass form's"], 0, "Sum of n^-s."),
  ("What did Dirichlet prove with L(1, chi)?", ["Infinitely many primes in progressions", "The Riemann hypothesis", "Fermat's last theorem", "Modularity"], 0, "Nonvanishing."),
  ("What is a character's conductor?", ["The smallest modulus defining it", "Its order", "Its parity", "Its value at 1"], 0, "Primitive means conductor = modulus."),
  ("What is the quadratic character mod p?", ["The Legendre symbol", "The gcd", "The Euler phi", "The sine"], 0, "(a/p).")],
 [("chi(mn) = chi(m)chi(n)", "Multiplicativity"), ("Zeta", "L-function of the trivial character"), ("N.k", "A character label"), ("Dirichlet", "Primes in progressions"), ("conductor", "Smallest modulus")],
 [MATCH("Character mod 4", "Match n with chi(n) for the nontrivial character mod 4.", [("1", "1"), ("2", "0"), ("3", "-1"), ("4", "0"), ("5", "1"), ("7", "-1")]),
  PL("The character mod 4", "Write chi4(n): return 0 for even n, 1 if n is 1 mod 4, and -1 if n is 3 mod 4.", "chi4(n)", '''
def chi4(n):
    if n % 2 == 0:
        return 0
    return 1 if n % 4 == 1 else -1
''', [[1], [2], [3], [5], [7], [9], [11], [100]], "Use n % 4."),
  PL("The zeta Euler product", "Write zeta_euler(s, bound): the product over primes p up to bound of 1 / (1 - p**(-s)), as a float. Zeta(2) is about 1.6449.", "zeta_euler(s, bound)", '''
def zeta_euler(s, bound):
    result = 1.0
    for p in range(2, bound + 1):
        if all(p % q for q in range(2, int(p ** 0.5) + 1)):
            result *= 1.0 / (1.0 - p ** (-s))
    return result
''', [[2, 100], [2, 1000], [3, 50], [4, 50]], "Test each number for primality as you go.", approx=1e-9)]
))

CHS.append(CH(
 "Elliptic curves over the rationals",
 ("Elliptic curves", [
  "Curve | is | y^2 = x^3 + ax + b",
  "Points | form | A group",
  "Discriminant | detects | Singularity",
  "Conductor | collects | Bad primes",
  "Rank | measures | Free rational points",
  "Torsion | is | The finite part"]),
 ["An elliptic curve is a smooth cubic curve with a chosen point. Its rational points form a group, described by a rank (how many independent infinite-order points) and a finite torsion part.",
  "A model y squared = x cubed + ax + b has discriminant -16(4a cubed + 27b squared). The curve is smooth when this is nonzero. The conductor packages the primes where the curve has bad reduction, and appears in the LMFDB label.",
  "The labs compute the discriminant and the j-invariant."],
 [("Elliptic curve", "A smooth cubic curve with a marked point, with a group law on its points."),
  ("Discriminant", "A number that vanishes exactly when the curve is singular."),
  ("j-invariant", "A number that identifies a curve up to isomorphism over the algebraic closure."),
  ("Conductor", "An integer built from the primes of bad reduction."),
  ("Mordell-Weil group", "The group of rational points: Z^r times a finite torsion group.")],
 ["Short Weierstrass form: y^2 = x^3 + ax + b over Q.",
  "Discriminant: -16(4a^3 + 27b^2); nonzero means smooth.",
  "j = 1728 * 4a^3 / (4a^3 + 27b^2).",
  "Mordell's theorem: the rational points form a finitely generated group.",
  "Torsion subgroups over Q: Mazur lists the 15 possibilities.",
  "The LMFDB label 11.a2 is conductor 11, class a, number 2."],
 [T("An elliptic curve is the set of solutions of y squared equals x cubed plus a x plus b, together with a point at infinity. The word elliptic comes from elliptic integrals, not from ellipses. The curve is smooth when the cubic has no repeated root, which happens exactly when the discriminant, minus 16 times (4 a cubed plus 27 b squared), is nonzero. If it vanishes, the curve has a node or a cusp, and we do not call it elliptic."),
  T("The magic is that the points on a smooth cubic form a group. Draw the line through two points P and Q; it meets the curve at a third point; reflect it in the x-axis, and call the result P plus Q. The point at infinity is the identity. This is the Mordell-Weil group of the rational points. Mordell proved it is finitely generated: it is Z to the power r, times a finite group. The number r is the rank. The finite group is the torsion subgroup, which Mazur showed can only be one of fifteen groups."),
  T("Every curve has a j-invariant, 1728 times 4a cubed over (4a cubed plus 27b squared). Two curves with the same j are isomorphic over the complex numbers, though not always over Q. The conductor N of a curve over Q is an integer divisible by exactly the primes where the curve degenerates when reduced mod p, which are the primes dividing the minimal discriminant. In the LMFDB label 11.a2, the 11 is the conductor, a names the isogeny class, and 2 numbers the curve within the class."),
  T("The big open problem is to understand the rank. Is it computable? Which ranks occur? The Birch and Swinnerton-Dyer conjecture says the rank equals the order of vanishing of the L-function at s = 1. The LMFDB records ranks, torsion, regulators and the data needed to test this conjecture for millions of curves. The curve y squared + y = x cubed - x squared - 10x - 20 has conductor 11 and rank 0, with a torsion subgroup of order five. We will use it throughout the course."),
  T("Try the explorer at the end of this chapter. Choose a and b, then a prime p. It plots the points of the curve over F_p, counts them, and shows the discriminant and the a_p. Try y squared = x cubed - x with p = 5, and see how few points there are. Then try a singular curve, such as a = 0 and b = 0, and see why the discriminant warns you.")],
 [("When is y^2 = x^3 + ax + b smooth?", ["When 4a^3 + 27b^2 is not 0", "When a = 0", "When b = 0", "Always"], 0, "Nonzero discriminant."),
  ("What does the rank count?", ["Independent points of infinite order", "Torsion points", "Bad primes", "The degree"], 0, "Free part of Mordell-Weil."),
  ("What does the conductor involve?", ["Primes of bad reduction", "Primes of good reduction", "The rank", "The j-invariant"], 0, "Appears in the label."),
  ("Who classified torsion over Q?", ["Mazur", "Gauss", "Euler", "Hecke"], 0, "Fifteen groups."),
  ("What is j for a curve, informally?", ["An invariant of isomorphism over C", "The conductor", "The rank", "A prime"], 0, "Same j, same curve over the complex numbers."),
  ("In the label 11.a2, what is 11?", ["The conductor", "The rank", "The torsion", "The discriminant"], 0, "Level.")],
 [("y^2 = x^3 + ax + b", "Short Weierstrass form"), ("-16(4a^3 + 27b^2)", "Discriminant"), ("Mordell-Weil", "Z^r times a finite group"), ("Mazur", "Torsion theorem"), ("BSD", "Rank equals order of vanishing of L at 1")],
 [MATCH("Match curve terms", "Pair each term with what it describes.", [("Discriminant", "detects singular curves"), ("Rank", "free part of rational points"), ("Torsion", "finite part of rational points"), ("Conductor", "primes of bad reduction"), ("j-invariant", "isomorphism class over C")]),
  PL("The discriminant", "Write disc(a, b) for the curve y^2 = x^3 + ax + b. Return -16 * (4*a**3 + 27*b**2).", "disc(a, b)", '''
def disc(a, b):
    return -16 * (4 * a ** 3 + 27 * b ** 2)
''', [[0, 1], [-1, 0], [1, 1], [-2, 3], [0, 0], [-4, 4]], "Plug into the formula."),
  PL("The j-invariant as a fraction", "Write j_invariant(a, b): the j-invariant 1728 * 4a^3 / (4a^3 + 27b^2) as a reduced fraction [numerator, denominator] with a positive denominator. Return None if the curve is singular. Use math-free gcd (Euclid).", "j_invariant(a, b)", '''
def j_invariant(a, b):
    d = 4 * a ** 3 + 27 * b ** 2
    if d == 0:
        return None
    n = 1728 * 4 * a ** 3
    x, y = abs(n), abs(d)
    while y:
        x, y = y, x % y
    g = x if x else 1
    n //= g
    d //= g
    if d < 0:
        n, d = -n, -d
    return [n, d]
''', [[0, 1], [-1, 0], [1, 1], [-2, 3], [0, 0], [3, 5]], "Reduce with Euclid's algorithm and fix the sign of the denominator."),
  APP("CURVES", "Elliptic curve explorer", "Choose a, b and a prime p. See the points mod p, the count, a_p and the discriminant. Look at three different smooth curves to finish.")]
))
