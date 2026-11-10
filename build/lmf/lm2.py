# -*- coding: utf-8 -*-
"""LMFDB course, part 2: counting points, modular forms, L-functions, modularity, Galois representations."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clib import *
from lm1 import APP

CHS = []

CHS.append(CH(
 "Counting points and the numbers a_p",
 ("Counting points", [
  "Curve | mod p | Has finitely many points",
  "Count | gives | a_p",
  "a_p | equals | p + 1 minus N_p",
  "Hasse | bounds | |a_p| by 2 sqrt p",
  "a_p | are | Fingerprints",
  "Bad prime | breaks | The count"]),
 ["Reduce an elliptic curve mod a prime p and count the points N_p. The number a_p = p + 1 - N_p is the trace of Frobenius, and Hasse proved |a_p| is at most 2 times the square root of p.",
  "The sequence a_2, a_3, a_5 ... is a fingerprint of the curve. It is the data the LMFDB shows under 'Frobenius traces' and the input to the curve's L-function.",
  "The labs count points by brute force and check the Hasse bound."],
 [("Reduction mod p", "Reading the curve's equation over F_p."),
  ("N_p", "The number of points on the curve over F_p, including the point at infinity."),
  ("a_p", "p + 1 - N_p, the trace of Frobenius."),
  ("Hasse bound", "|a_p| <= 2 sqrt p."),
  ("Good reduction", "The reduced curve is still smooth; this holds for p not dividing the conductor.")],
 ["N_p = 1 + number of solutions (x, y) in F_p x F_p.",
  "a_p = p + 1 - N_p.",
  "Hasse: |a_p| <= 2 sqrt p, or a_p^2 <= 4p.",
  "For short form, N_p = 1 + sum over x of (1 + (f(x)/p)).",
  "Bad primes divide the conductor; there a_p is 0 or plus or minus 1.",
  "For the conductor 11 curve: a_2 = -2, a_3 = -1, a_5 = 1, a_7 = -2, a_13 = 4."],
 [T("The easiest way to meet an elliptic curve arithmetically is to count its points over finite fields. Take the curve y squared + y = x cubed - x squared - 10x - 20. Over F_2 there are only 2 times 2 = 4 pairs (x, y) to check, and adding the point at infinity gives the total. Doing this for each prime p gives numbers N_p, and from these the traces a_p = p + 1 - N_p."),
  C("p    2   3   5   7   11  13  17  19  23\na_p -2  -1   1  -2   1   4  -2   0  -1", "text"),
  T("These numbers are the same for every curve in the same isogeny class, and they are the LMFDB's 'Frobenius traces'. Hasse proved that a_p cannot be large: the absolute value is at most two times the square root of p. For p = 13 the bound is about 7.2, and indeed a_13 = 4. The number a_p is the trace of the Frobenius map, the map that sends each coordinate to its p-th power. The Frobenius has two eigenvalues of absolute value the square root of p, which explains the bound."),
  M(r"|a_p| \le 2\sqrt{p}, \qquad a_p = p+1-\#E(\mathbb F_p)"),
  T("There are two exceptions. At the primes dividing the conductor, the curve has bad reduction, and the formula changes: a_p is 1, -1 or 0 depending on the type. For the curve of conductor 11, a_11 = 1. Everywhere else the count behaves well. For a curve with short form, the count simplifies to N_p = 1 plus the sum over x of 1 + (f(x)/p), where f(x) = x cubed + a x + b and the fraction is the Legendre symbol from chapter 2.")],
 [("What is a_p?", ["p + 1 minus the number of points", "The rank", "The torsion", "The conductor"], 0, "Trace of Frobenius."),
  ("What does Hasse's bound say?", ["|a_p| <= 2 sqrt p", "a_p = 0", "a_p > p", "a_p is prime"], 0, "Small traces."),
  ("What is N_p?", ["The number of points over F_p", "A prime", "The rank", "The class number"], 0, "Including infinity."),
  ("For the conductor 11 curve, what is a_3?", ["-1", "1", "2", "0"], 0, "From the table."),
  ("Which primes are bad?", ["Those dividing the conductor", "All odd primes", "p = 2 only", "None"], 0, "Bad reduction."),
  ("What map has trace a_p?", ["Frobenius", "Translation", "Reflection", "Hecke"], 0, "Raising to the p-th power.")],
 [("a_p", "p + 1 - N_p"), ("Hasse", "|a_p| <= 2 sqrt p"), ("a_2, a_3, a_5", "-2, -1, 1 for the conductor 11 curve"), ("Frobenius", "Raising to the p-th power"), ("bad prime", "Divides the conductor")],
 [MATCH("Match the a_p", "Pair the prime with a_p for the conductor 11 curve.", [("2", "-2"), ("3", "-1"), ("5", "1"), ("7", "-2"), ("13", "4"), ("17", "-2")]),
  PL("Count points in the short form", "Write count_points(a, b, p) for y^2 = x^3 + ax + b over F_p (p an odd prime): return 1 plus, for each x in 0..p-1, the number of y in 0..p-1 with y*y % p equal to (x**3 + a*x + b) % p. (That is, include the point at infinity.)", "count_points(a, b, p)", '''
def count_points(a, b, p):
    n = 1
    for x in range(p):
        rhs = (x ** 3 + a * x + b) % p
        for y in range(p):
            if (y * y) % p == rhs:
                n += 1
    return n
''', [[-1, 0, 5], [-1, 0, 7], [1, 1, 5], [2, 3, 7], [-1, 0, 13], [0, 1, 11]], "Check every (x, y) pair."),
  PL("The trace a_p for the curve of conductor 11", "Write ap_general(a1, a2, a3, a4, a6, p): count solutions (x, y) in F_p^2 of y^2 + a1*x*y + a3*y = x^3 + a2*x^2 + a4*x + a6 mod p, add 1 for infinity, and return p + 1 minus the total. For [0, -1, 1, -10, -20] you should get -2 at p = 2 and 4 at p = 13.", "ap_general(a1, a2, a3, a4, a6, p)", '''
def ap_general(a1, a2, a3, a4, a6, p):
    n = 1
    for x in range(p):
        for y in range(p):
            lhs = y * y + a1 * x * y + a3 * y
            rhs = x ** 3 + a2 * x * x + a4 * x + a6
            if (lhs - rhs) % p == 0:
                n += 1
    return p + 1 - n
''', [[0, -1, 1, -10, -20, 2], [0, -1, 1, -10, -20, 3], [0, -1, 1, -10, -20, 5], [0, -1, 1, -10, -20, 7], [0, -1, 1, -10, -20, 13], [0, -1, 1, -10, -20, 17], [0, -1, 1, -10, -20, 19]], "Brute force over x and y; reduce the difference mod p."),
  PL("Check the Hasse bound", "Write hasse_ok(ap, p): True when ap*ap <= 4*p, otherwise False.", "hasse_ok(ap, p)", '''
def hasse_ok(ap, p):
    return ap * ap <= 4 * p
''', [[-2, 2], [4, 13], [8, 13], [-1, 3], [3, 2], [0, 5]], "Compare the square with 4p to avoid square roots.")]
))

CHS.append(CH(
 "Modular forms",
 ("Modular forms", [
  "Modular form | lives on | The upper half-plane",
  "Weight | sets | The transformation",
  "Level | sets | The congruence subgroup",
  "q-expansion | lists | The coefficients",
  "Cusp form | vanishes | At cusps",
  "Eisenstein series | are | The easy forms"]),
 ["A modular form is a complex function on the upper half-plane with a rigid symmetry under a group of matrices. Its Fourier expansion in q = e^(2 pi i z) carries arithmetic information in the coefficients.",
  "Weight k and level N classify the space of forms. Eisenstein series give simple examples with divisor sums as coefficients; cusp forms, such as Delta, have arithmetic coefficients like Ramanujan's tau.",
  "The labs compute Eisenstein series and the first coefficients of Delta."],
 [("Modular form", "A holomorphic function on the upper half-plane transforming under a congruence subgroup with weight k."),
  ("q-expansion", "The Fourier series sum a_n q^n, where q = e^(2 pi i z)."),
  ("Weight", "The integer k in the transformation f((az+b)/(cz+d)) = (cz+d)^k f(z)."),
  ("Level", "The integer N defining the group Gamma_0(N)."),
  ("Cusp form", "A modular form whose q-expansion starts at n = 1.")],
 ["f((az+b)/(cz+d)) = (cz+d)^k f(z) for matrices in the group.",
  "q = e^(2 pi i z) and f = sum a_n q^n.",
  "E_4 = 1 + 240 sum sigma_3(n) q^n; E_6 = 1 - 504 sum sigma_5(n) q^n.",
  "Delta = q prod (1 - q^n)^24 is a weight 12 cusp form of level 1.",
  "Dimensions of spaces are finite and known by formulas.",
  "The LMFDB labels spaces as N.k.chi."],
 [T("A modular form is a function with astonishing symmetry. Let z live in the upper half-plane, the complex numbers with positive imaginary part. A modular form f of weight k satisfies f of (a z + b) over (c z + d) equals (c z + d) to the k times f of z, for all integer matrices of determinant one, at least those in a chosen group. The simplest group is the full SL2(Z), of level 1. For level N, we use the subgroup Gamma_0(N) of matrices with c divisible by N."),
  T("Such a function is periodic: f(z + 1) = f(z). So it has a Fourier series, which we write in q = e to the 2 pi i z as the sum of a_n q^n. These coefficients are the point. The simplest modular forms are Eisenstein series. For weight 4, E_4 = 1 + 240 times the sum of sigma_3(n) q^n, where sigma_3(n) is the sum of the cubes of the divisors of n. So E_4 = 1 + 240q + 2160q^2 + 6720q^3 + ..."),
  T("The most famous modular form is Delta, a weight 12 cusp form of level 1: Delta = q times the product of (1 - q^n) to the 24th power. Expand it and you get Ramanujan's tau function: q - 24q^2 + 252q^3 - 1472q^4 + 4830q^5 - 6048q^6 - 16744q^7 + ... Ramanujan observed that tau is multiplicative: tau(mn) = tau(m) tau(n) when m and n are coprime. That fact is a first sign of the Hecke operators, which we meet in the next chapter."),
  M(r"\Delta(z)=q\prod_{n\ge1}(1-q^n)^{24}=\sum_{n\ge1}\tau(n)q^n"),
  T("A cusp form is one whose expansion starts at n = 1, so it vanishes at the cusps. The space of cusp forms of weight k and level N is finite-dimensional, with dimension given by formulas. For level 1, the first cusp form appears in weight 12, which is why Delta is so special: it is the unique one there. The LMFDB stores bases for these spaces, along with q-expansions, as the main data of the modular forms collection.")],
 [("What is q in a q-expansion?", ["e^(2 pi i z)", "A prime", "The level", "The weight"], 0, "A coordinate on the disc."),
  ("What is the first cusp form of level 1?", ["Delta, weight 12", "E_4", "E_6", "A weight 2 form"], 0, "Unique in weight 12."),
  ("What is tau(2)?", ["-24", "24", "1", "252"], 0, "The coefficient of q^2."),
  ("What is E_4's q coefficient?", ["240", "1", "504", "24"], 0, "240 sigma_3(1)."),
  ("What does weight k control?", ["The transformation factor (cz + d)^k", "The level", "The conductor", "The rank"], 0, "Part of the symmetry."),
  ("What is a cusp form?", ["One that vanishes at the cusps", "One with level 1", "One of weight 2", "A form with no q-expansion"], 0, "Starts at n = 1.")],
 [("Delta", "q prod (1 - q^n)^24"), ("tau(n)", "1, -24, 252, -1472, 4830, ..."), ("E_4", "1 + 240q + 2160q^2 + ..."), ("level N", "Gamma_0(N)"), ("weight k", "Transformation exponent")],
 [MATCH("Match tau", "Pair n with Ramanujan's tau(n).", [("1", "1"), ("2", "-24"), ("3", "252"), ("4", "-1472"), ("5", "4830"), ("6", "-6048")]),
  PL("Divisor power sums", "Write sigma(n, k): the sum of d**k over all divisors d of n.", "sigma(n, k)", '''
def sigma(n, k):
    total = 0
    for d in range(1, n + 1):
        if n % d == 0:
            total += d ** k
    return total
''', [[1, 3], [2, 3], [6, 1], [12, 3], [28, 1], [10, 5]], "Loop d from 1 to n and test divisibility."),
  PL("The Eisenstein series E4", "Write eisenstein4(n): the first n+1 coefficients [1, 240*sigma_3(1), ..., 240*sigma_3(n)] of E_4. (sigma_3(m) is the sum of the cubes of the divisors of m.)", "eisenstein4(n)", '''
def eisenstein4(n):
    out = [1]
    for m in range(1, n + 1):
        s = 0
        for d in range(1, m + 1):
            if m % d == 0:
                s += d ** 3
        out.append(240 * s)
    return out
''', [[1], [3], [5], [8]], "Compute sigma_3 for each m and multiply by 240."),
  PL("Ramanujan's tau", "Write delta_coeffs(n): the coefficients tau(1), ..., tau(n) of Delta = q * prod (1 - q^m)^24, as a list. Hint: build the product P of (1 - q^m)^24 for m = 1..n-1 as a list of n integers, truncating at degree n - 1, then tau(k) = P[k-1].", "delta_coeffs(n)", '''
def delta_coeffs(n):
    P = [1] + [0] * (n - 1)
    for m in range(1, n):
        for _ in range(24):
            for i in range(n - 1, m - 1, -1):
                P[i] -= P[i - m]
    return P
''', [[1], [2], [5], [8], [10]], "Multiply the polynomial by (1 - q^m) twenty-four times for each m, working from the top degree down.")]
))

CHS.append(CH(
 "Hecke operators and newforms",
 ("Hecke and newforms", [
  "Hecke operator | acts on | Modular forms",
  "Eigenform | has | Multiplicative coefficients",
  "Newform | is | A normalised eigenform",
  "Old form | comes from | A lower level",
  "Coefficient field | contains | The a_n",
  "Label | names | Level weight orbit"]),
 ["Hecke operators T_p act on spaces of modular forms. A form that is an eigenvector of all of them has multiplicative coefficients and a nice Euler product. The new part of the space is spanned by newforms, which the LMFDB labels N.k.a.x.",
  "For a newform the q-expansion coefficient a_p is the Hecke eigenvalue at p. The a_p sometimes lie in a larger number field, and Galois conjugate newforms are grouped into an orbit.",
  "The labs test multiplicativity and compute the Hecke relation for tau."],
 [("Hecke operator", "A linear operator T_n on modular forms built from sums over cosets; it commutes with other T_m."),
  ("Eigenform", "A form that is an eigenvector for all Hecke operators."),
  ("Newform", "A normalised cuspidal eigenform not coming from a lower level."),
  ("Oldform", "A form built from a newform of lower level by f(z), f(dz)."),
  ("Galois orbit", "A set of newforms whose coefficients are Galois conjugates of each other.")],
 ["T_p on weight k, level N, prime p not dividing N, takes a_n to a_{pn} + p^(k-1) a_{n/p}.",
  "For a newform, a_1 = 1 and a_{mn} = a_m a_n for coprime m, n.",
  "a_{p^(r+1)} = a_p a_{p^r} - p^(k-1) a_{p^(r-1)} for good p.",
  "Tau satisfies tau(p^2) = tau(p)^2 - p^11.",
  "The LMFDB label N.k.a.x = level, weight, character orbit, newform orbit.",
  "Deligne: |a_p| <= 2 p^((k-1)/2)."],
 [T("The modular forms of a given weight and level form a vector space. On it act the Hecke operators T_n, one for each n. They commute with each other, so the space can be broken into joint eigenspaces. A form that is an eigenvector of every T_n has a very rigid structure: its coefficients a_n are the eigenvalues. For a normalised one (a_1 = 1), this gives a_m a_n = a_{mn} for coprime m, n, and a recursion for prime powers."),
  T("Check it with Delta. tau(2) = -24 and tau(3) = 252, so tau(6) should be -24 times 252, which is -6048. It is. For prime powers, tau(4) = tau(2)^2 - 2^11 = 576 - 2048 = -1472. Again it matches. These relations are the Hecke relations, and they explain why the coefficients of Delta look so special: they are the eigenvalues of a very symmetric operator."),
  M(r"a_{p^{r+1}} = a_p\, a_{p^r} - p^{k-1} a_{p^{r-1}} \quad (p\nmid N)"),
  T("When the level is not 1, there are also oldforms. If f has level M and M divides N, then f(z) and f(dz) for d dividing N/M have level N, but they are not new. The newforms are those that cannot be built from lower levels, and they form a basis for the new part of the space. The LMFDB labels them level.weight.character.letter. The form 11.2.a.a is the unique newform of level 11, weight 2, trivial character. Its q-expansion starts q - 2q^2 - q^3 + 2q^4 + q^5 + 2q^6 - 2q^7 - 2q^9 ..."),
  T("Sometimes the coefficients of a newform do not lie in Q but in a number field, the coefficient field. Then the newform has Galois conjugates, which together form an orbit, and the label's last letter distinguishes the orbits. Deligne proved that the coefficients obey a Hecke-Ramanujan bound: the absolute value of a_p is at most 2 times p to the (k - 1)/2. For weight 2 this is exactly the Hasse bound.")],
 [("What does a Hecke operator do?", ["Acts linearly on modular forms", "Counts points", "Defines a field", "Computes a class number"], 0, "T_n."),
  ("What does tau(6) equal?", ["tau(2) times tau(3)", "tau(2) plus tau(3)", "tau(5)", "0"], 0, "Multiplicative."),
  ("What is a newform?", ["A normalised eigenform not from a lower level", "A form of weight 1", "Any modular form", "An Eisenstein series"], 0, "No oldform content."),
  ("What is tau(4)?", ["-1472", "-576", "1472", "2048"], 0, "tau(2)^2 - 2^11."),
  ("What does the label 11.2.a.a say?", ["Level 11, weight 2", "Level 2, weight 11", "A field of degree 11", "A curve of rank 2"], 0, "N.k."),
  ("What bound did Deligne prove?", ["|a_p| <= 2 p^((k-1)/2)", "a_p = 0", "a_p is an integer", "|a_p| >= 1"], 0, "Generalises Hasse.")],
 [("T_n", "Hecke operator"), ("a_mn = a_m a_n", "Multiplicativity for coprime m, n"), ("tau(4) = tau(2)^2 - 2^11", "Hecke recursion"), ("newform", "Normalised new eigenform"), ("Deligne", "The Ramanujan-Petersson bound")],
 [MATCH("Hecke recursion for tau", "Pair each statement with its value.", [("tau(2)*tau(3)", "-6048"), ("tau(2)^2 - 2^11", "-1472"), ("tau(2)", "-24"), ("tau(3)", "252")]),
  PL("The Hecke relation at a prime power", "Write hecke_next(ap, ar, arm, p, k): return ap*ar - p**(k-1)*arm, which is a_{p^(r+1)} from a_p, a_{p^r}, a_{p^(r-1)}.", "hecke_next(ap, ar, arm, p, k)", '''
def hecke_next(ap, ar, arm, p, k):
    return ap * ar - p ** (k - 1) * arm
''', [[-24, 1, 1, 2, 12], [-24, -24, 1, 2, 12], [252, 252, 1, 3, 12], [-2, 1, 1, 2, 2]], "Apply the recursion directly."),
  PL("Test multiplicativity", "Write is_multiplicative(coeffs): coeffs[0] is a_1, coeffs[1] is a_2 and so on. Return True if coeffs[0] == 1 and, for all coprime m, n with m*n <= len(coeffs), a_{mn} == a_m * a_n. Use gcd by Euclid.", "is_multiplicative(coeffs)", '''
def is_multiplicative(coeffs):
    def g(a, b):
        while b:
            a, b = b, a % b
        return a
    if not coeffs or coeffs[0] != 1:
        return False
    n = len(coeffs)
    for m in range(1, n + 1):
        for k in range(1, n + 1):
            if m * k <= n and g(m, k) == 1:
                if coeffs[m * k - 1] != coeffs[m - 1] * coeffs[k - 1]:
                    return False
    return True
''', [[[1, -24, 252, -1472, 4830, -6048, -16744, 84480, -113643, -115920]], [[1, 2, 3, 4]], [[1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2]], [[2, 1]]], "Check every coprime pair m, k whose product fits in the list.")]
))

CHS.append(CH(
 "L-functions",
 ("L-functions", [
  "L-function | has | A Dirichlet series",
  "Euler product | factors | Over primes",
  "Functional equation | relates | s and k - s",
  "Analytic continuation | extends | The domain",
  "Zeros | encode | Arithmetic",
  "Critical line | holds | The zeros, conjecturally"]),
 ["An L-function packages the local data at every prime into one analytic function. It has a Dirichlet series, an Euler product, an analytic continuation and a functional equation. The LMFDB lists many of them with plots, zeros and special values.",
  "The Riemann zeta function is the simplest. A newform f gives L(f, s) = sum a_n n^(-s), and an elliptic curve gives L(E, s) built from its a_p. The generalised Riemann hypothesis says the nontrivial zeros all lie on the critical line.",
  "The labs form Euler factors and partial products."],
 [("L-function", "A Dirichlet series with an Euler product, analytic continuation and a functional equation."),
  ("Euler factor", "The local factor at a prime p in the Euler product."),
  ("Functional equation", "A relation between L(s) and L(k - s) with a root number of absolute value one."),
  ("Critical strip", "The region where the real part of s lies strictly between the edges of absolute convergence."),
  ("Root number", "The sign (or unit) in the functional equation; it predicts the parity of the rank.")],
 ["Zeta: sum n^-s = product 1/(1 - p^-s).",
  "Newform: L(f, s) = sum a_n n^-s = product 1/(1 - a_p p^-s + p^(k-1-2s)).",
  "Elliptic curve (weight 2): factor 1/(1 - a_p p^-s + p^(1-2s)).",
  "Functional equation relates s and k - s (weight k) with a root number.",
  "GRH: nontrivial zeros of L-functions have real part (k/2) on the critical line.",
  "The LMFDB lists zeros, plots, and degree and conductor for each L-function."],
 [T("An L-function is a bundle of numbers, one per prime, packaged into an analytic function. The Riemann zeta function is the prototype: the sum over n of n to the minus s, which equals the product over p of 1 divided by 1 minus p to the minus s. The right side shows that zeta knows all the primes. The left side shows it is a Dirichlet series. Riemann showed it extends to the whole complex plane except s = 1, and that it satisfies a functional equation relating s to 1 minus s."),
  T("Every newform f of weight k has an L-function: L(f, s) is the sum of a_n n to the minus s. Because the a_n are multiplicative with a Hecke recursion, it has an Euler product with local factors 1 over (1 minus a_p p to the minus s plus p to the (k - 1 - 2s)). For an elliptic curve E, the L-function L(E, s) has the same form with k = 2 and a_p the trace of Frobenius. We multiply the factors over the primes up to some bound to approximate it, as the lab does for zeta."),
  M(r"L(E,s)=\prod_{p\nmid N}\frac{1}{1-a_p p^{-s}+p^{1-2s}}\prod_{p\mid N}\frac{1}{1-a_p p^{-s}}"),
  T("The deepest facts are the analytic continuation and the functional equation. For a newform of level N, the completed L-function relates s to k minus s, up to a sign called the root number. A root number of minus 1 forces the L-function to vanish at the central point, and the Birch and Swinnerton-Dyer conjecture ties the order of vanishing at that point to the rank of the elliptic curve. The generalised Riemann hypothesis, still unproven, says all nontrivial zeros lie on the vertical line through the center of the critical strip."),
  T("The LMFDB lists L-functions with a label that includes the degree, conductor, character and spectral parameters, and shows the zeros, plots of Z(t), the Euler factors and the special values. Compare an elliptic curve's page with the page of its modular form, and you will find the same L-function, linked from both. That link is the modularity theorem in action, which is the next chapter.")],
 [("What does an Euler product show?", ["The series factors over primes", "The series is finite", "The series diverges", "The series is real"], 0, "Unique factorisation."),
  ("What is a functional equation?", ["A relation between L(s) and L(k - s)", "A polynomial", "A matrix", "A differential equation"], 0, "Symmetry about the centre."),
  ("What does the root number predict?", ["Parity of the rank", "The conductor", "The class number", "The torsion"], 0, "Sign of the equation."),
  ("Where do the nontrivial zeros of zeta lie (conjecturally)?", ["On the critical line", "On the real axis", "At integers", "Nowhere"], 0, "Re s = 1/2."),
  ("Which factor does an elliptic curve contribute at a good prime?", ["1/(1 - a_p p^-s + p^(1-2s))", "1/(1 - p^-s)", "p^-s", "a_p"], 0, "Degree two."),
  ("What does the LMFDB show for an L-function?", ["Zeros, plots, Euler factors", "Only the label", "Only a proof", "Only the coefficients"], 0, "Rich data.")],
 [("zeta", "sum n^-s = product 1/(1 - p^-s)"), ("L(E, s)", "Built from the a_p"), ("functional equation", "s to k - s"), ("root number", "Sign in the functional equation"), ("GRH", "Zeros on the critical line")],
 [MATCH("Match the L-function", "Pair each object with its L-function.", [("trivial character", "Riemann zeta"), ("Newform f", "sum a_n n^-s"), ("Elliptic curve E", "built from a_p"), ("Dirichlet character", "sum chi(n) n^-s")]),
  PL("An Euler factor for an elliptic curve", "Write euler_factor(ap, p, s): the value of 1 / (1 - ap * p**(-s) + p**(1 - 2*s)) as a float, for a good prime p.", "euler_factor(ap, p, s)", '''
def euler_factor(ap, p, s):
    return 1.0 / (1.0 - ap * p ** (-s) + p ** (1 - 2 * s))
''', [[-2, 2, 2], [-1, 3, 2], [1, 5, 2], [-2, 7, 3], [4, 13, 2]], "Compute the denominator, then invert.", approx=1e-9),
  PL("A partial Euler product", "Write partial_L(aps, s): aps is a list of [p, ap] for good primes. Return the product of the Euler factors 1 / (1 - ap * p**(-s) + p**(1 - 2*s)) over the list, as a float.", "partial_L(aps, s)", '''
def partial_L(aps, s):
    total = 1.0
    for p, ap in aps:
        total *= 1.0 / (1.0 - ap * p ** (-s) + p ** (1 - 2 * s))
    return total
''', [[[[2, -2], [3, -1], [5, 1], [7, -2]], 2], [[[2, -2], [3, -1]], 3], [[[13, 4], [17, -2], [19, 0]], 2]], "Multiply as you go.", approx=1e-9)]
))

CHS.append(CH(
 "Modularity: curves meet forms",
 ("Modularity", [
  "Elliptic curve | has | a_p",
  "Newform | has | a_p",
  "Modularity | equates | The two",
  "Conductor | equals | The level",
  "Wiles | proved | Fermat's Last Theorem",
  "Isogeny class | maps to | One newform"]),
 ["The modularity theorem says that every elliptic curve over Q corresponds to a weight 2 newform whose level equals the curve's conductor, with matching coefficients: a_p(E) = a_p(f) for all good primes.",
  "The conductor 11 curve and the newform 11.2.a.a have the same a_p. Wiles proved a large part of this, enough to prove Fermat's Last Theorem, and the full theorem followed.",
  "The labs compare a curve's a_p with the q-expansion of a newform."],
 [("Modularity theorem", "Every elliptic curve over Q is modular: its L-function equals that of a weight 2 newform."),
  ("Isogeny", "A map between elliptic curves preserving the group structure; isogenous curves share a_p."),
  ("Taniyama-Shimura-Weil", "The conjecture that became the modularity theorem."),
  ("Frey curve", "A curve built from a hypothetical Fermat solution that would be non-modular."),
  ("Galois representation", "A homomorphism from the Galois group to a matrix group.")],
 ["Conductor of E = level of the newform f.",
  "a_p(E) = a_p(f) for p not dividing the conductor.",
  "Isogenous curves correspond to the same newform.",
  "Wiles (1995) and Taylor-Wiles for semistable curves; Breuil-Conrad-Diamond-Taylor (2001) for all.",
  "Ribet showed that a Frey curve would not be modular; Wiles proved it must be, so no solutions.",
  "In the LMFDB, a curve page links to its modular form, with the same L-function."],
 [T("This is the central result. Take the elliptic curve with conductor 11, y squared plus y equals x cubed minus x squared minus 10x minus 20. We counted its points mod p and found a_p equal to -2, -1, 1, -2, 1, 4, -2, 0 for p = 2, 3, 5, 7, 11, 13, 17, 19. Now take the newform 11.2.a.a, whose q-expansion is q - 2q^2 - q^3 + 2q^4 + q^5 + 2q^6 - 2q^7 + 0 q^8 - 2q^9 - 2q^10 + q^11 - 2q^12 + 4q^13 ... The coefficients at primes are the same list. That is not an accident."),
  C("p       2   3   5   7  11  13  17  19\na_p(E) -2  -1   1  -2   1   4  -2   0\na_p(f) -2  -1   1  -2   1   4  -2   0", "text"),
  T("The modularity theorem says that this happens for every elliptic curve over the rationals: there is a weight 2 newform f whose level is the conductor of E and whose Hecke eigenvalues are the traces of Frobenius. This is a completely unexpected bridge. On one side, algebra: solutions of a cubic equation over finite fields. On the other side, analysis: a function on the upper half-plane with a transformation law. The two are different, yet they produce identical sequences."),
  T("The theorem has a famous consequence. Suppose a, b, c satisfy a^n + b^n = c^n for a prime n at least 5. Frey built an elliptic curve from them, y squared = x (x - a^n)(x + b^n), with strange properties. Ribet proved that such a curve could not be modular. Wiles proved, in 1995, that semistable elliptic curves are modular, which includes the Frey curve. Therefore no solutions exist: Fermat's Last Theorem. In 2001 Breuil, Conrad, Diamond and Taylor extended the proof to all elliptic curves over Q."),
  T("Behind the scenes is the idea of a Galois representation. The absolute Galois group of Q acts on the torsion points of the curve, and this action, in the right language, is the same as the one attached to the modular form. The LMFDB shows both objects and links them, with the same L-function on both pages. This is the template for the Langlands program: match objects of geometry and Galois theory with automorphic forms, so that L-functions agree.")],
 [("What does the modularity theorem say?", ["Every elliptic curve over Q comes from a modular form", "Every modular form is a curve", "Curves have rank 0", "L-functions have no zeros"], 0, "Matching a_p."),
  ("What equals the conductor of E?", ["The level of its newform", "The weight", "The rank", "The torsion"], 0, "Level matches."),
  ("Who proved the semistable case?", ["Wiles (with Taylor)", "Gauss", "Ramanujan", "Hecke"], 0, "1995."),
  ("What did Ribet prove?", ["A Frey curve could not be modular", "Modularity in general", "The Riemann hypothesis", "Hasse's bound"], 0, "A key step."),
  ("What is a_5 for the conductor 11 newform?", ["1", "-1", "2", "0"], 0, "From the q-expansion."),
  ("Why is modularity surprising?", ["It links algebraic and analytic objects", "It is trivial", "It is false", "It only works for p = 2"], 0, "A bridge between worlds.")],
 [("a_p(E) = a_p(f)", "Modularity"), ("11.2.a.a", "The newform of the conductor 11 curve"), ("Wiles 1995", "Semistable modularity"), ("Frey curve", "From a hypothetical Fermat solution"), ("Langlands", "The grand pattern")],
 [MATCH("Match the object to its role", "Pair each name with what it did.", [("Frey", "built a curve from a Fermat solution"), ("Ribet", "showed it could not be modular"), ("Wiles", "proved modularity for semistable curves"), ("Breuil-Conrad-Diamond-Taylor", "completed modularity")]),
  PL("Compare a curve with a form", "Write matches(ap_curve, coeffs, primes): ap_curve is a list of a_p for the given primes, coeffs is the q-expansion list [a_1, a_2, ...] of a newform (coeffs[n-1] is a_n). Return True if for every prime in primes the curve value equals the form coefficient.", "matches(ap_curve, coeffs, primes)", '''
def matches(ap_curve, coeffs, primes):
    for i in range(len(primes)):
        if ap_curve[i] != coeffs[primes[i] - 1]:
            return False
    return True
''', [[[-2, -1, 1, -2], [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4], [2, 3, 5, 7]], [[-2, -1, 2], [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4], [2, 3, 5]], [[4], [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4], [13]]], "Index the coefficients by p - 1."),
  PL("Find the first disagreement", "Write first_mismatch(ap_curve, coeffs, primes): return the first prime whose curve a_p differs from the form coefficient, or 0 if they all agree.", "first_mismatch(ap_curve, coeffs, primes)", '''
def first_mismatch(ap_curve, coeffs, primes):
    for i in range(len(primes)):
        if ap_curve[i] != coeffs[primes[i] - 1]:
            return primes[i]
    return 0
''', [[[-2, -1, 1, -2], [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4], [2, 3, 5, 7]], [[-2, -1, 3], [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4], [2, 3, 5]], [[1, 1], [1, 1, 1, 1, 1, 1, 1], [2, 3]]], "Same loop, return the prime.")]
))

CHS.append(CH(
 "Galois representations, Sato-Tate and BSD",
 ("Beyond modularity", [
  "Galois group | acts on | Roots and torsion",
  "Representation | encodes | The action",
  "Frobenius | has | A trace a_p",
  "Sato-Tate | describes | The distribution of a_p",
  "BSD | links | Rank and L(1)",
  "Langlands | generalises | All of this"]),
 ["A Galois representation records how the Galois group of Q acts on the points of a curve or the roots of a polynomial. At each prime, Frobenius has a trace a_p, and the representation is determined by these traces.",
  "The Sato-Tate theorem says that a_p divided by 2 sqrt p is distributed like cos of an angle with a sine squared density. The Birch and Swinnerton-Dyer conjecture ties the rank to the order of vanishing of L(E, s) at s = 1.",
  "The labs normalise a_p and test a Hasse-style bound."],
 [("Galois representation", "A homomorphism from the Galois group to GL_n of some field."),
  ("Frobenius element", "The Galois element acting as x to x^p at a prime p."),
  ("Sato-Tate distribution", "The conjectured and proved distribution of normalised a_p for curves without complex multiplication."),
  ("BSD conjecture", "Rank of E(Q) equals the order of vanishing of L(E, s) at s = 1."),
  ("Complex multiplication", "Extra symmetry of a curve by an order in an imaginary quadratic field.")],
 ["Normalised trace: a_p / (2 sqrt p) lies in [-1, 1].",
  "Sato-Tate: the angle theta with a_p = 2 sqrt p cos(theta) has density (2/pi) sin^2(theta).",
  "BSD: rank = ord_{s=1} L(E, s), plus a formula for the leading coefficient.",
  "Artin representations match Galois representations of finite image to L-functions.",
  "The Langlands program: automorphic representations correspond to Galois representations.",
  "The LMFDB lists Sato-Tate groups for curves and abelian varieties."],
 [T("The Galois group of Q, which is the symmetry group of all the algebraic numbers, acts on lots of objects. It acts on the roots of a polynomial. It acts on the torsion points of an elliptic curve. A Galois representation is a record of this action as a family of matrices. At a prime p where the representation is unramified, there is a special element, Frobenius, and the trace of its matrix is the a_p we have been computing. So the a_p are the main data of the representation: the local snapshots of a global symmetry."),
  T("How are the a_p distributed? Hasse tells us they lie between minus 2 root p and 2 root p. Dividing, a_p over two root p lies in minus 1 to 1. Write it as cos of an angle theta. The Sato-Tate theorem, proved for elliptic curves over Q without complex multiplication, says that these angles are distributed with density two over pi times sine squared of theta. Computing a_p for a thousand primes and plotting a histogram shows the bell-like shape of the semicircle. For curves with complex multiplication, such as y squared = x cubed - x, the distribution differs: half of the a_p are zero."),
  M(r"a_p = 2\sqrt p\,\cos\theta_p,\qquad d\mu_{ST}=\tfrac{2}{\pi}\sin^2\theta\,d\theta"),
  T("The Birch and Swinnerton-Dyer conjecture is one of the Clay Millennium Problems. It says that the rank of the group of rational points equals the order of vanishing of L(E, s) at s = 1."),
  T("The conjecture also gives an exact formula for the leading Taylor coefficient in terms of the regulator, the Tamagawa numbers, the torsion and the order of the Tate-Shafarevich group. The LMFDB displays all these invariants for each curve, so you can test the formula numerically. It is proved in some cases of rank 0 and 1, and unproved in general."),
  T("The Langlands program generalises all this. For every n-dimensional Galois representation there should be an automorphic form whose L-function matches. Modularity is the n = 2 case for elliptic curves. For n = 1, it is class field theory, proved by Artin. For Artin representations, it is conjectural in general. This organises the LMFDB: each collection is a corner of the Langlands picture, and the links between collections are instances of Langlands correspondences.")],
 [("What does Frobenius have at a prime p?", ["A trace a_p", "A class number", "A rank", "A conductor"], 0, "In the representation."),
  ("What is a_p / (2 sqrt p) in?", ["[-1, 1]", "[0, 1]", "[1, 2]", "All of R"], 0, "Hasse."),
  ("Which distribution do the angles follow?", ["Sato-Tate, (2/pi) sin^2", "Uniform", "Normal", "Poisson"], 0, "Semicircle-like."),
  ("What does BSD relate?", ["Rank and the order of vanishing", "Rank and conductor", "Torsion and class number", "Level and weight"], 0, "At s = 1."),
  ("What is the n = 1 case of Langlands?", ["Class field theory", "Modularity", "Fermat's Last Theorem", "Hasse's bound"], 0, "Artin reciprocity."),
  ("What kind of curve has half of its a_p zero?", ["CM curve like y^2 = x^3 - x", "Any curve", "A curve of rank 5", "A curve of conductor 11"], 0, "Complex multiplication.")],
 [("Frobenius trace", "a_p"), ("Sato-Tate", "Angles with density (2/pi) sin^2"), ("BSD", "Rank = order of vanishing"), ("CM", "Complex multiplication"), ("Langlands", "Galois reps and automorphic forms")],
 [MATCH("Match the term", "Pair each term with its description.", [("Sato-Tate", "distribution of normalised a_p"), ("BSD", "rank and L(E, 1)"), ("Frobenius", "trace is a_p"), ("CM", "extra endomorphisms"), ("Langlands", "Galois to automorphic")]),
  PL("The normalised trace", "Write normalised(ap, p): ap / (2 * sqrt(p)) as a float, using p ** 0.5 for the root.", "normalised(ap, p)", '''
def normalised(ap, p):
    return ap / (2.0 * p ** 0.5)
''', [[-2, 2], [4, 13], [1, 5], [0, 19], [-1, 23]], "Divide by two times the square root of p.", approx=1e-9),
  PL("Fraction of zero traces", "Write zero_fraction(aps): the fraction of entries of the list aps that are 0, as a float. Return 0.0 for an empty list. CM curves have a large fraction.", "zero_fraction(aps)", '''
def zero_fraction(aps):
    if not aps:
        return 0.0
    z = 0
    for a in aps:
        if a == 0:
            z += 1
    return z / len(aps)
''', [[[0, 2, 0, -2]], [[1, 2, 3]], [[]], [[0, 0, 0, 0, 1]]], "Count zeros and divide by the length.", approx=1e-9)]
))

CHS.append(CH(
 "Using the LMFDB and what lies beyond",
 ("Using the LMFDB", [
  "Browse | finds | Collections",
  "Search | filters | By invariants",
  "Label | opens | A single page",
  "API | returns | JSON",
  "Genus 2 curves | extend | Elliptic curves",
  "Open data | invites | Your own experiments"]),
 ["The LMFDB has collections beyond those in this course: genus 2 curves, abelian varieties over finite fields, Siegel and Hilbert modular forms, Maass forms, Artin representations and local fields. Each follows the same plan: invariants, labels, links.",
  "You can search by invariants (conductor, rank, torsion, degree, discriminant), open a page by label, or query the data through an API. Pages show proven and computed data; read the notes on what is proven.",
  "The labs read a label and compute simple statistics, and the last exam checks the whole course."],
 [("Genus 2 curve", "A curve y^2 = f(x) with f of degree 5 or 6; its Jacobian is a 2-dimensional abelian variety."),
  ("Abelian variety", "A higher-dimensional analogue of an elliptic curve."),
  ("Maass form", "A non-holomorphic eigenfunction of the Laplacian on the upper half-plane."),
  ("Artin representation", "A complex representation of a Galois group with finite image."),
  ("API", "A programmatic interface for downloading data.")],
 ["Each LMFDB collection has search forms, label pages and downloadable data.",
  "Labels encode invariants: conductor, class, and index.",
  "Genus 2 curves have L-functions of degree 4.",
  "Pages distinguish proven from computed data; look for notes.",
  "You can reproduce an a_p or a class number yourself, as in the labs.",
  "Cross-links between collections show the Langlands correspondences."],
 [T("Now that you know the main characters, a tour of the database makes sense. The home page lists the collections: Elliptic curves over Q and over number fields, Genus 2 curves, Number fields, Modular forms (classical, Hilbert, Bianchi, Maass), Dirichlet characters, L-functions, Galois groups, Artin representations, Abelian varieties over finite fields, and more."),
  T("Each collection has a browse page, a search form, and a page per object. The object page opens with a label and a block of invariants, followed by tables, plots and links."),
  T("Searching is by invariants. For curves, you might ask for conductor under 1000, rank 2, and torsion trivial. For number fields, degree 3 with discriminant between minus 1000 and minus 100. For modular forms, level 23 and weight 2. The results are a table of labels, and each opens a page. The database also gives downloadable data in formats for Sage, Magma and Pari, and a programmatic interface, so you can fetch thousands of curves and compute your own statistics, for example the histogram of normalised a_p."),
  T("Genus 2 curves are the next step up. Where an elliptic curve is y squared = a cubic, a genus 2 curve is y squared = a quintic or sextic. Their Jacobians are two-dimensional abelian varieties, and their L-functions have degree four, with four numbers per Euler factor. The paramodular conjecture, a cousin of modularity, predicts that such curves match Siegel modular forms. Maass forms are non-holomorphic cousins of modular forms; they are eigenfunctions of the Laplacian on the upper half-plane and have no known algebraic origin, but they have L-functions too."),
  T("When using the database, keep a scientific attitude. Some data are proven, such as the conductor, the discriminant and the torsion subgroup. Some are computed under assumptions, such as the rank and the Tate-Shafarevich group in some cases. The pages say so. Cross-check what you can: compute a_p for a curve and compare it with the newform's coefficients, compute a class number from reduced forms. The data are most valuable when you can understand where they come from."),
  T("Where next? Read about the Langlands program, learn Sage or Pari/GP to compute with elliptic curves and modular forms, and look at the open problems the database is meant to support: BSD, the Sato-Tate conjectures in higher genus, the paramodular conjecture and the generalised Riemann hypothesis. The best way in is to pick one curve and one form, and follow their links around the database.")],
 [("What does a genus 2 curve's L-function have?", ["Degree four", "Degree one", "Degree two", "Degree six"], 0, "Four numbers per prime."),
  ("What does the API give?", ["Programmatic access to the data", "Proofs", "Videos", "Only plots"], 0, "JSON."),
  ("What are Maass forms?", ["Non-holomorphic eigenfunctions of the Laplacian", "Holomorphic forms", "Elliptic curves", "Fields"], 0, "On the upper half-plane."),
  ("How should you treat the rank in the database?", ["Check whether it is proven or computed", "Always trust it", "Ignore it", "Recompute only a_p"], 0, "Read the notes."),
  ("What is a good first experiment?", ["Compare a curve's a_p with its newform", "Memorise labels", "Skip the maths", "Only read pages"], 0, "As in the labs."),
  ("What does a label let you do?", ["Open a specific object page", "Prove a theorem", "Draw a graph", "Factor a number"], 0, "Like an address.")],
 [("genus 2", "y^2 = quintic or sextic"), ("Maass form", "Non-holomorphic Laplace eigenfunction"), ("API", "Programmatic access"), ("proven vs computed", "Read the notes on each page"), ("Langlands", "The unifying pattern")],
 [MATCH("Match the collection to its idea", "Pair each collection with a one-line description.", [("Elliptic curves", "cubic curves with a group law"), ("Modular forms", "symmetric functions with q-expansions"), ("Number fields", "finite extensions of Q"), ("Dirichlet characters", "multiplicative functions mod N"), ("L-functions", "analytic packages of local data")]),
  PL("Average of the a_p", "Write mean_ap(aps): the mean of the list aps as a float (0.0 for an empty list). By Sato-Tate it tends to 0 for non-CM curves.", "mean_ap(aps)", '''
def mean_ap(aps):
    if not aps:
        return 0.0
    return sum(aps) / len(aps)
''', [[[-2, -1, 1, -2, 1, 4, -2, 0]], [[1, -1]], [[]], [[3]]], "Sum and divide.", approx=1e-9),
  PL("Largest normalised trace", "Write max_normalised(pairs): pairs is a list of [p, ap]. Return the maximum of abs(ap) / (2 * p**0.5) as a float. By Hasse this is at most 1.", "max_normalised(pairs)", '''
def max_normalised(pairs):
    best = 0.0
    for p, ap in pairs:
        v = abs(ap) / (2.0 * p ** 0.5)
        if v > best:
            best = v
    return best
''', [[[[2, -2], [3, -1], [5, 1], [7, -2], [13, 4]]], [[[11, 1]]], [[]]], "Track the largest value seen.", approx=1e-9),
  FILL("A scientific attitude", "Some data in the LMFDB are {{proven}} and some are only {{computed}}. You should {{cross-check}} what you can.")]
))
