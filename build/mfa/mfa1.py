"""Mathematics for CS and AI, part 1: discrete mathematics and linear algebra."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Logic and proof",
 ("Logic", [
  "Proposition | is | True or false",
  "Connective | combines | Propositions",
  "Implication | is false only | True implies false",
  "Quantifier | ranges over | A domain",
  "Proof | establishes | A theorem",
  "Induction | proves | Statements for all n",
  "Contradiction | refutes | The opposite"]),
 ["Logic is the grammar of mathematics and of programs. A proposition is a statement that is true or false. Connectives such as and, or, not and implies build new propositions from old ones, and truth tables say exactly when they hold.",
  "Quantifiers say for all and there exists. Proofs are arguments that a statement must hold: direct proof, proof by contradiction, and mathematical induction, which proves a statement for every natural number.",
  "Every later chapter relies on these tools. The labs evaluate formulas, check tautologies and prove a sum formula by testing it."],
 [("Proposition", "A statement that is either true or false."),
  ("Implication", "p implies q is false only when p is true and q is false."),
  ("Tautology", "A formula true under every assignment of its variables."),
  ("Quantifier", "For all (universal) or there exists (existential)."),
  ("Induction", "Prove a base case, and that each case implies the next."),
  ("Contrapositive", "Not q implies not p; equivalent to p implies q.")],
 ["Connectives: not, and, or, implies, if and only if.",
  "p implies q is equivalent to (not p) or q, and to its contrapositive.",
  "De Morgan: not (p and q) = (not p) or (not q); not (p or q) = (not p) and (not q).",
  "Negating for all gives there exists not; negating there exists gives for all not.",
  "Induction: P(0) and (P(n) implies P(n+1)) give P(n) for all n.",
  "Strong induction assumes P(k) for all k below n."],
 [T("A proposition is a sentence that is either true or false, like 7 is prime. We combine propositions with connectives. And is true when both parts are. Or is true when at least one is. Not flips the value. The most important and most misunderstood connective is implication."),
  T("The statement p implies q is false in exactly one case: p true and q false. If p is false the implication is true whatever q is. This is called vacuous truth. The statement is equivalent to not p or q. It is also equivalent to its contrapositive, not q implies not p, but not to its converse, q implies p."),
  M(r"\neg(p \wedge q) \equiv \neg p \vee \neg q, \qquad \neg(p \vee q) \equiv \neg p \wedge \neg q, \qquad p \Rightarrow q \equiv \neg p \vee q"),
  T("Quantifiers add generality. For all x in a set, P of x says that P holds for every element. There exists x such that P of x says some element works. To negate a quantified statement, swap the quantifier and negate the body. The negation of every swan is white is some swan is not white."),
  T("Proof techniques turn these into arguments. A direct proof assumes the hypothesis and derives the conclusion. Proof by contradiction assumes the conclusion is false and derives an absurdity. Proof by induction handles statements about all natural numbers: prove the case for zero, then prove that if the case for n holds, so does the case for n plus one."),
  M(r"\sum_{k=1}^{n} k \;=\; \frac{n(n+1)}{2}"),
  T("As an example, the formula above holds for n equal to one, since both sides are one. If it holds for n, adding n plus one to both sides gives the formula for n plus one. Induction is the logical twin of recursion: a recursive function and an inductive proof have the same shape. Later, in the type theory chapter, you will see that this resemblance is exact.")],
 [("When is p implies q false?", ["p true and q false", "p false and q true", "Both false", "Both true"], 0, "Only then."),
  ("What is the contrapositive of p implies q?", ["not q implies not p", "q implies p", "not p implies not q", "p and q"], 0, "Equivalent to the original."),
  ("What does induction need?", ["A base case and a step", "Only a step", "Only examples", "A contradiction"], 0, "Then all n follow."),
  ("Negation of for all x P(x)?", ["There exists x not P(x)", "For all x not P(x)", "There exists x P(x)", "Not exists"], 0, "Swap and negate.")],
 [("What is vacuous truth?", "An implication with a false hypothesis is true."), ("What is a tautology?", "True in every row of the truth table."), ("De Morgan for and?", "not (p and q) = not p or not q."), ("What is strong induction?", "Assume all smaller cases.")],
 [PL("Implication", "Write implies(p, q): 1 if p implies q, 0 otherwise (p and q are 0 or 1).",
     "implies(p, q)", """
def implies(p, q):
    if p == 1 and q == 0:
        return 0
    return 1
""", [[0, 0], [0, 1], [1, 0], [1, 1]], "False only for true then false."),
  PL("Tautology check", "A formula is given as a function name: 0 = (p or not p), 1 = (p and q), 2 = (p implies p), 3 = (not (p and q)) equals (not p or not q). Write is_taut(k): 1 if formula k is true for all four assignments of p and q, otherwise 0.",
     "is_taut(k)", """
def is_taut(k):
    for p in (0, 1):
        for q in (0, 1):
            if k == 0:
                v = 1 if (p == 1 or p == 0) else 0
            elif k == 1:
                v = 1 if (p == 1 and q == 1) else 0
            elif k == 2:
                v = 1
            else:
                a = 0 if (p == 1 and q == 1) else 1
                b = 1 if (p == 0 or q == 0) else 0
                v = 1 if a == b else 0
            if v == 0:
                return 0
    return 1
""", [[0], [1], [2], [3]], "Enumerate all four rows."),
  PL("Check an identity by testing", "Write sum_formula_holds(n): 1 if 1 + 2 + ... + k equals k(k+1)/2 for every k from 1 to n, else 0.",
     "sum_formula_holds(n)", """
def sum_formula_holds(n):
    s = 0
    for k in range(1, n + 1):
        s += k
        if 2 * s != k * (k + 1):
            return 0
    return 1
""", [[1], [10], [100], [0]], "Testing is not proof, but it catches mistakes."),
  PL("De Morgan counterexample search", "Write de_morgan_fails(): return the number of assignments of (p, q) out of 4 for which not (p and q) differs from (not p) or (not q). (It is 0.)",
     "de_morgan_fails()", """
def de_morgan_fails():
    bad = 0
    for p in (0, 1):
        for q in (0, 1):
            a = 1 - (p * q)
            b = 1 if (1 - p) + (1 - q) > 0 else 0
            if a != b:
                bad += 1
    return bad
""", [[]], "A law has no counterexamples."),
  ORDER("Induction proof", "Order the steps.", ["State the claim P(n)", "Prove the base case", "Assume P(k) for some k", "Prove P(k+1) from it", "Conclude P(n) for all n"]),
  MATCH("Logic", "Match each term with its meaning.", [("Tautology", "Always true"), ("Contrapositive", "not q implies not p"), ("Existential quantifier", "There exists"), ("Vacuous truth", "False hypothesis"), ("Induction", "Base case plus step")]),
  FILL("Proof", "An implication is false only when the hypothesis is true and the conclusion is {{false}}. Induction proves a base case and an inductive {{step}}.")]))

CHS.append(CH(
 "Sets, relations and functions",
 ("Sets", [
  "Set | collects | Distinct elements",
  "Union | joins | Sets",
  "Cartesian product | pairs | Elements",
  "Relation | is | A set of pairs",
  "Function | maps | Each input once",
  "Bijection | pairs | Perfectly",
  "Equivalence relation | partitions | A set"]),
 ["A set is a collection of distinct things. Sets have union, intersection and complement; the Cartesian product forms pairs. A relation is a set of pairs, and a function is a relation that gives exactly one output for each input.",
  "Injective functions never merge inputs, surjective ones hit every output, and bijective ones are both and so can be inverted. Equivalence relations split a set into disjoint classes, which is how we define things like integers modulo n.",
  "The labs implement set operations, compose functions and test properties of relations."],
 [("Set", "An unordered collection of distinct elements."),
  ("Cartesian product", "A x B is the set of pairs (a, b)."),
  ("Relation", "A subset of a Cartesian product."),
  ("Function", "A relation with exactly one output per input."),
  ("Injective, surjective, bijective", "One-to-one; onto; both."),
  ("Equivalence relation", "Reflexive, symmetric and transitive.")],
 ["|A union B| = |A| + |B| - |A intersect B|.",
  "|A x B| = |A| |B|; a set of n elements has 2^n subsets.",
  "A function f: A -> B has one output per input.",
  "f is invertible exactly when it is a bijection.",
  "Equivalence: reflexive, symmetric, transitive; its classes partition the set.",
  "Composition: (g o f)(x) = g(f(x))."],
 [T("Sets are the basic language. We write membership as x in A. Two sets are equal when they have the same elements, and order and repetition do not matter. The power set of A is the set of all subsets of A, and has two to the n elements when A has n."),
  M(r"|A \cup B| = |A| + |B| - |A \cap B|, \qquad |A \times B| = |A|\,|B|, \qquad |\mathcal{P}(A)| = 2^{|A|}"),
  T("A relation from A to B is a subset of the product A times B. Less than on the integers is a relation. A function is a special relation in which each input has exactly one output. We write f from A to B. The set A is the domain and B the codomain. The image is the set of outputs actually reached."),
  T("Three properties matter. A function is injective if different inputs give different outputs. It is surjective if every element of the codomain is an output. It is bijective if it is both, in which case an inverse function exists. Bijections between sets show they have the same size, which is how we compare infinite sizes."),
  T("An equivalence relation is reflexive, symmetric and transitive. It groups elements into equivalence classes, and the classes partition the set. Congruence modulo n is an equivalence relation on the integers, and its classes are the residues zero to n minus one."),
  T("In computing, sets are the model for types and collections, functions are the model of programs, and relations model databases. Later chapters on category theory and type theory start from functions and ask what can be said using only composition.")],
 [("How many subsets does a 4-element set have?", ["16", "8", "4", "24"], 0, "2^4."),
  ("What does an injective function do?", ["Never maps two inputs to one output", "Hits every output", "Has no inverse", "Is constant"], 0, "One-to-one."),
  ("What is a bijection?", ["Injective and surjective", "Only injective", "Only surjective", "A relation"], 0, "Has an inverse."),
  ("What do equivalence classes form?", ["A partition", "A chain", "A tree", "A graph"], 0, "Disjoint and covering.")],
 [("Size of A x B?", "|A| times |B|."), ("Power set size?", "2 to the |A|."), ("What is the image?", "The outputs actually reached."), ("Is less-than an equivalence?", "No: it is not reflexive.")],
 [PL("Union size", "Write union_size(a, b): the number of elements in the union of two lists treated as sets.",
     "union_size(a, b)", """
def union_size(a, b):
    s = set(a)
    for x in b:
        s.add(x)
    return len(s)
""", [[[1, 2, 3], [3, 4]], [[], []], [[1, 1, 1], [1]], [[1, 2], [3, 4, 5]]], "Use a set."),
  PL("Power set size by listing", "Write power_set_count(n): the number of subsets of {0..n-1}, found by counting bitmasks from 0 to 2^n - 1.",
     "power_set_count(n)", """
def power_set_count(n):
    c = 0
    for mask in range(2 ** n):
        c += 1
    return c
""", [[0], [1], [4], [8]], "Every subset is a bitmask."),
  PL("Is it a bijection?", "A function on {0..n-1} is given as a list f of length n with values in 0..n-1. Write is_bijection(f): 1 if it is one-to-one (and so onto), else 0.",
     "is_bijection(f)", """
def is_bijection(f):
    return 1 if len(set(f)) == len(f) else 0
""", [[[1, 2, 0]], [[0, 0, 1]], [[0]], [[2, 1, 0, 3]]], "No repeated outputs."),
  PL("Compose and invert", "Write compose(f, g): the list h with h[i] = g[f[i]] (apply f then g).",
     "compose(f, g)", """
def compose(f, g):
    return [g[f[i]] for i in range(len(f))]
""", [[[1, 2, 0], [2, 0, 1]], [[0, 1], [1, 0]], [[2, 2, 2], [0, 1, 2]]], "Index twice."),
  PL("Equivalence classes mod n", "Write classes_mod(items, n): group the integers in items by residue mod n and return the list of n lists (residue 0 first), keeping input order.",
     "classes_mod(items, n)", """
def classes_mod(items, n):
    out = [[] for r in range(n)]
    for x in items:
        out[x % n].append(x)
    return out
""", [[[1, 2, 3, 4, 5, 6], 3], [[10, 11], 2], [[7], 5]], "One list per residue."),
  ORDER("Check a function property", "Order the steps to test injectivity.", ["List all inputs", "Compute each output", "Compare outputs pairwise", "If two coincide the function is not injective", "Otherwise it is injective"]),
  MATCH("Functions", "Match each property with its meaning.", [("Injective", "No two inputs share an output"), ("Surjective", "Every output is hit"), ("Bijective", "Invertible"), ("Image", "Outputs reached"), ("Composition", "g after f")]),
  FILL("Sets", "A set of n elements has {{2^n|2 to the n|two to the n}} subsets. A {{bijection}} is both injective and surjective.")]))

CHS.append(CH(
 "Counting and combinatorics",
 ("Counting", [
  "Product rule | multiplies | Independent choices",
  "Sum rule | adds | Exclusive cases",
  "Permutation | orders | Items",
  "Combination | chooses | Unordered items",
  "Binomial coefficient | counts | Subsets",
  "Pigeonhole | forces | Collisions",
  "Inclusion-exclusion | corrects | Overlaps"]),
 ["Counting is the maths behind complexity, probability and hashing. The product rule multiplies independent choices; the sum rule adds disjoint cases. A permutation orders items; a combination picks a subset.",
  "The number of ways to choose k of n items is the binomial coefficient n choose k. The pigeonhole principle says that more items than boxes forces a box with two, and inclusion-exclusion corrects for overlaps.",
  "The labs compute factorials, binomials, derangement-style counts and the birthday collision probability."],
 [("Factorial", "n! = n (n-1) ... 1, the number of orderings of n items."),
  ("Permutation", "An ordered arrangement; P(n, k) = n!/(n-k)!."),
  ("Combination", "An unordered choice; C(n, k) = n!/(k!(n-k)!)."),
  ("Binomial theorem", "(x + y)^n = sum C(n, k) x^k y^(n-k)."),
  ("Pigeonhole principle", "n + 1 items in n boxes: some box has two."),
  ("Inclusion-exclusion", "Add singles, subtract pairs, add triples, and so on.")],
 ["P(n, k) = n (n-1) ... (n-k+1).",
  "C(n, k) = C(n-1, k-1) + C(n-1, k) (Pascal).",
  "Sum of C(n, k) over k equals 2^n.",
  "Pigeonhole: if more than n items go into n boxes, some box holds at least two.",
  "Birthday problem: collisions appear after about sqrt(n) draws from n values.",
  "Stars and bars: ways to split n identical items into k groups is C(n+k-1, k-1)."],
 [T("How many passwords of length four use the digits zero to nine? Each of four positions has ten options, independent of the others, so the product rule gives ten to the fourth, or 10,000. If the options depend on the case, split into disjoint cases and add: the sum rule."),
  T("Ordering matters in permutations. Arranging n different items gives n factorial orderings: n choices for the first place, n minus one for the next, and so on. Picking and ordering k of n gives n times n minus one down to n minus k plus one."),
  M(r"\binom{n}{k} \;=\; \frac{n!}{k!\,(n-k)!}, \qquad \binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}, \qquad \sum_{k=0}^{n}\binom{n}{k} = 2^{n}"),
  T("When order does not matter, divide out the orderings: n choose k counts the subsets of size k. The recurrence is Pascal's rule and builds Pascal's triangle. Summing a row gives two to the n, the number of all subsets, matching the power set of the last chapter."),
  T("The pigeonhole principle is simple and powerful: put more than n items into n boxes and some box holds two. It proves that any lossless compressor must enlarge some inputs. A probabilistic cousin is the birthday problem: among only 23 people, two share a birthday with probability above one half. Collisions in hash tables appear after about the square root of the table size."),
  T("Inclusion-exclusion counts a union: add the sizes of the sets, subtract the pairwise overlaps, add back triple overlaps, and so on. We will meet all of this again as the foundation of discrete probability.")],
 [("How many orderings of 5 distinct items?", ["120", "25", "60", "5"], 0, "5!."),
  ("What is C(5, 2)?", ["10", "20", "5", "25"], 0, "5!/(2!3!)."),
  ("What does pigeonhole say?", ["More items than boxes forces a shared box", "Boxes are equal", "Items are distinct", "Boxes are empty"], 0, "Collisions are unavoidable."),
  ("What does a row of Pascal's triangle sum to?", ["2^n", "n!", "n^2", "n"], 0, "All subsets.")],
 [("Product rule?", "Multiply independent choices."), ("Sum rule?", "Add disjoint cases."), ("Birthday threshold?", "About the square root of n."), ("Stars and bars?", "C(n+k-1, k-1).")],
 [PL("Factorial", "Write factorial(n): n! for n at least 0.",
     "factorial(n)", """
def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r
""", [[0], [1], [5], [10], [15]], "Multiply up."),
  PL("Binomial", "Write choose(n, k): the binomial coefficient, computed with Pascal's rule or a product (0 if k is out of range).",
     "choose(n, k)", """
def choose(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r
""", [[5, 2], [10, 0], [10, 10], [20, 10], [4, 5]], "Multiply and divide stepwise."),
  PL("Pascal row", "Write pascal_row(n): the list of C(n, k) for k = 0..n.",
     "pascal_row(n)", """
def pascal_row(n):
    row = [1]
    for i in range(n):
        row = [1] + [row[j] + row[j + 1] for j in range(len(row) - 1)] + [1]
    return row
""", [[0], [1], [4], [6]], "Each entry is the sum of two above."),
  PL("Birthday collision probability", "Write birthday(k, n): the probability that among k people with n equally likely birthdays at least two share one, rounded to 6 decimals.",
     "birthday(k, n)", """
def birthday(k, n):
    p = 1.0
    for i in range(k):
        p *= (n - i) / n
    return round(1 - p, 6)
""", [[23, 365], [2, 365], [1, 365], [50, 365], [10, 10]], "One minus the chance all differ.", approx=1e-6),
  PL("Inclusion-exclusion for two sets", "Write union_count(a, b, both): |A union B| from |A|, |B| and |A intersect B|.",
     "union_count(a, b, both)", """
def union_count(a, b, both):
    return a + b - both
""", [[10, 5, 2], [3, 3, 3], [0, 4, 0]], "Subtract the overlap once."),
  ORDER("Counting a password", "Order the steps.", ["Decide the number of positions", "Count the options at each position", "Check the choices are independent", "Multiply the option counts", "Report the product"]),
  MATCH("Counting", "Match each count with its value.", [("5!", "120"), ("C(5,2)", "10"), ("2^4", "16"), ("P(5,2)", "20"), ("C(4,0)", "1")]),
  FILL("Counting", "Choosing k of n items without order gives the {{binomial}} coefficient; more items than boxes forces a {{collision|shared box}}.")]))

CHS.append(CH(
 "Graphs, trees and relations as graphs",
 ("Graphs", [
  "Graph | has | Vertices and edges",
  "Degree | counts | Edges at a vertex",
  "Path | joins | Vertices by edges",
  "Tree | is | A connected acyclic graph",
  "Adjacency matrix | stores | Edges",
  "BFS and DFS | explore | Graphs",
  "Handshake lemma | sums | Degrees"]),
 ["A graph is a set of vertices joined by edges. Graphs model networks, dependencies, states and relations. Degree counts the edges at a vertex, and the handshake lemma says the degrees add up to twice the number of edges.",
  "A tree is a connected graph without cycles; a tree on n vertices has n minus 1 edges. Graphs are stored as adjacency lists or matrices and explored with breadth-first or depth-first search.",
  "The labs build adjacency structures, count degrees, test for trees and run a breadth-first search."],
 [("Graph", "A set of vertices V and edges E."),
  ("Degree", "The number of edges at a vertex."),
  ("Path and cycle", "A walk without repeated vertices; a closed path."),
  ("Tree", "A connected graph with no cycle."),
  ("Adjacency matrix", "A matrix A with A[i][j] = 1 when there is an edge i to j."),
  ("Connected component", "A maximal set of mutually reachable vertices.")],
 ["Sum of degrees = 2 |E| (handshake lemma).",
  "A tree on n vertices has n - 1 edges and a unique path between any two vertices.",
  "A connected graph on n vertices has at least n - 1 edges.",
  "Powers of the adjacency matrix count walks: (A^k)[i][j] is the number of walks of length k.",
  "BFS finds shortest paths in unweighted graphs.",
  "A directed acyclic graph can be topologically ordered."],
 [T("A graph consists of vertices and edges. Roads, social networks, the links of a web, the dependencies between software packages and the states of an automaton are all graphs. An edge may be undirected or directed, and may carry a weight."),
  T("The degree of a vertex is the number of edges at it. Every edge contributes to two degrees, so the sum of all degrees is twice the number of edges. This handshake lemma implies that the number of odd-degree vertices is even."),
  M(r"\sum_{v \in V} \deg(v) \;=\; 2\,|E|"),
  T("A path is a sequence of vertices linked by edges. A graph is connected if a path joins every pair of vertices. A tree is a connected graph with no cycles. Trees on n vertices always have exactly n minus one edges, and between any two vertices there is exactly one path. Rooted trees organise hierarchies: file systems, syntax trees, search trees."),
  T("To compute with graphs we store them. An adjacency list gives each vertex its neighbours and is compact for sparse graphs. An adjacency matrix has a one at row i, column j when there is an edge. A nice fact links it to linear algebra: the k-th power of the matrix counts the walks of length k between each pair of vertices."),
  T("Breadth-first search explores outward in layers and finds shortest paths when edges have equal cost. Depth-first search dives deep before backtracking and underlies topological sorting and cycle detection. The data structures and algorithms course covers them in full. Here we use graphs as a language for relations.")],
 [("What do the degrees of a graph sum to?", ["Twice the number of edges", "The number of edges", "The number of vertices", "Zero"], 0, "Handshake lemma."),
  ("How many edges does a tree on n vertices have?", ["n - 1", "n", "n + 1", "2n"], 0, "Connected and acyclic."),
  ("What does (A^k)[i][j] count?", ["Walks of length k", "Shortest paths", "Degrees", "Cycles only"], 0, "A link to linear algebra."),
  ("What does BFS find in unweighted graphs?", ["Shortest paths", "Longest paths", "Cycles only", "Colours"], 0, "Layer by layer.")],
 [("Is a tree connected?", "Yes."), ("Has a tree a cycle?", "No."), ("What is a component?", "A maximal connected piece."), ("How to store a sparse graph?", "Adjacency lists.")],
 [PL("Degrees", "Write degrees(n, edges): the list of degrees of the vertices 0..n-1 of an undirected graph given by a list of [u, v] edges.",
     "degrees(n, edges)", """
def degrees(n, edges):
    d = [0] * n
    for u, v in edges:
        d[u] += 1
        d[v] += 1
    return d
""", [[3, [[0, 1], [1, 2]]], [4, []], [3, [[0, 1], [0, 2], [1, 2]]], [2, [[0, 1]]]], "Each edge adds to two degrees."),
  PL("Is it a tree?", "Write is_tree(n, edges): 1 if the undirected graph is connected and has exactly n - 1 edges, else 0.",
     "is_tree(n, edges)", """
def is_tree(n, edges):
    if len(edges) != n - 1:
        return 0
    adj = [[] for i in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [0] * n
    stack = [0]
    seen[0] = 1
    cnt = 1
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if not seen[y]:
                seen[y] = 1
                cnt += 1
                stack.append(y)
    return 1 if cnt == n else 0
""", [[3, [[0, 1], [1, 2]]], [3, [[0, 1], [0, 1]]], [4, [[0, 1], [1, 2], [2, 3]]], [4, [[0, 1], [2, 3], [0, 1]]], [1, []]], "n - 1 edges and connected."),
  PL("Walks by matrix power", "Write walks(adj, k): the number of walks of length k from vertex 0 to vertex n-1, where adj is the adjacency matrix (list of rows). Compute with repeated multiplication.",
     "walks(adj, k)", """
def walks(adj, k):
    n = len(adj)
    cur = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for _ in range(k):
        nxt = [[0] * n for i in range(n)]
        for i in range(n):
            for j in range(n):
                s = 0
                for t in range(n):
                    s += cur[i][t] * adj[t][j]
                nxt[i][j] = s
        cur = nxt
    return cur[0][n - 1]
""", [[[[0, 1, 0], [1, 0, 1], [0, 1, 0]], 2], [[[0, 1, 0], [1, 0, 1], [0, 1, 0]], 3], [[[0, 1], [1, 0]], 5], [[[0, 1, 1], [1, 0, 1], [1, 1, 0]], 3]], "Matrix powers count walks."),
  PL("BFS distance", "Write bfs_dist(n, edges, s, t): the number of edges on a shortest path from s to t in an undirected graph, or -1 if unreachable.",
     "bfs_dist(n, edges, s, t)", """
def bfs_dist(n, edges, s, t):
    adj = [[] for i in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dist = [-1] * n
    dist[s] = 0
    q = [s]
    i = 0
    while i < len(q):
        x = q[i]
        i += 1
        for y in adj[x]:
            if dist[y] < 0:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist[t]
""", [[4, [[0, 1], [1, 2], [2, 3]], 0, 3], [4, [[0, 1], [2, 3]], 0, 3], [3, [[0, 1], [1, 2], [0, 2]], 0, 2], [2, [], 0, 0]], "Layer by layer from s."),
  ORDER("BFS", "Order the steps.", ["Put the start vertex in a queue", "Remove the front vertex", "Visit its unvisited neighbours", "Add them to the queue with distance + 1", "Repeat until the queue is empty"]),
  MATCH("Graphs", "Match each term with its meaning.", [("Degree", "Edges at a vertex"), ("Tree", "Connected and acyclic"), ("Adjacency matrix", "Edge table"), ("Path", "Walk without repeats"), ("Component", "Maximal connected piece")]),
  FILL("Graphs", "A tree on n vertices has {{n-1|n - 1|n minus 1}} edges. The degrees sum to twice the number of {{edges}}.")]))

CHS.append(CH(
 "Number theory and modular arithmetic",
 ("Number theory", [
  "Divisibility | defines | Factors",
  "GCD | is | Largest common divisor",
  "Euclid | computes | The GCD fast",
  "Modular arithmetic | wraps | Around a modulus",
  "Prime | has | Two divisors",
  "Fermat | gives | Fast powers and inverses",
  "RSA | relies on | Hard factoring"]),
 ["Number theory studies integers. Divisibility, primes and the greatest common divisor underlie hashing, random number generators and cryptography. Modular arithmetic, which wraps numbers around a modulus, is arithmetic on a clock.",
  "Euclid's algorithm computes the greatest common divisor quickly. Fast exponentiation computes large powers modulo n, and Fermat's little theorem gives modular inverses for a prime modulus. These tools make public-key cryptography possible.",
  "The labs implement gcd, modular exponentiation, the sieve of Eratosthenes and modular inverses."],
 [("Divides", "a divides b when b = a k for an integer k."),
  ("GCD", "The greatest common divisor of two numbers."),
  ("Congruence", "a is congruent to b mod n when n divides a - b."),
  ("Prime", "An integer above 1 with only 1 and itself as divisors."),
  ("Modular inverse", "x with a x congruent to 1 mod n; exists when gcd(a, n) = 1."),
  ("Fermat's little theorem", "For prime p and a not divisible by p: a^(p-1) is congruent to 1 mod p.")],
 ["gcd(a, b) = gcd(b, a mod b); gcd(a, 0) = a.",
  "Modular arithmetic respects + and x: (a + b) mod n = ((a mod n) + (b mod n)) mod n.",
  "Square-and-multiply computes a^e mod n in O(log e) steps.",
  "Fermat: a^(p-1) = 1 mod p, so a^(-1) = a^(p-2) mod p.",
  "Every integer above 1 factors uniquely into primes.",
  "RSA's security rests on the difficulty of factoring large products of primes."],
 [T("We say a divides b if b is a times some integer. Every integer greater than one is either prime, with no divisors but one and itself, or a product of primes in a unique way. The greatest common divisor of two numbers is the largest number dividing both. Euclid, two thousand years ago, found how to compute it quickly."),
  M(r"\gcd(a, b) = \gcd(b,\ a \bmod b), \qquad \gcd(a, 0) = a"),
  T("The rule works because any common divisor of a and b also divides a mod b. Each step shrinks the numbers fast: the algorithm runs in time proportional to the number of digits."),
  T("Modular arithmetic works with remainders. We say a is congruent to b modulo n when n divides the difference. Addition and multiplication respect this: you may reduce at any point. Hours on a clock add modulo twelve. Hash functions and checksums use it constantly."),
  M(r"a^{p-1} \equiv 1 \pmod p \quad (p \text{ prime},\ p \nmid a), \qquad a^{-1} \equiv a^{p-2} \pmod p"),
  T("Large powers are computed by repeated squaring: to find a to the e, square a repeatedly and multiply in the squares that match the binary digits of e. This needs only a logarithmic number of multiplications, each reduced modulo n so the numbers stay small. Fermat's little theorem then provides modular inverses when n is prime."),
  T("Public-key cryptography builds on this. RSA multiplies two large primes to make a public modulus. Anyone can encrypt with modular powers, but undoing it appears to require factoring the modulus. The same ideas give hash tables, pseudo-random generators and error-correcting codes.")],
 [("What is gcd(12, 18)?", ["6", "3", "12", "36"], 0, "Largest common divisor."),
  ("What is 7 mod 3?", ["1", "2", "0", "3"], 0, "Remainder."),
  ("What does Fermat give?", ["Inverses mod a prime", "Square roots", "Primes", "Logarithms"], 0, "a^(p-2)."),
  ("What is cryptography's hard problem here?", ["Factoring", "Addition", "Sorting", "Counting"], 0, "Large products of primes.")],
 [("Euclid's step?", "gcd(a, b) = gcd(b, a mod b)."), ("How many steps for pow?", "About log e."), ("Is 1 prime?", "No."), ("When does an inverse exist?", "When gcd(a, n) = 1.")],
 [PL("GCD", "Write gcd(a, b): the greatest common divisor by Euclid's algorithm.",
     "gcd(a, b)", """
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
""", [[12, 18], [17, 5], [100, 75], [0, 9], [1071, 462]], "Replace (a, b) by (b, a mod b)."),
  PL("Modular exponentiation", "Write powmod(a, e, n): a^e mod n by square-and-multiply.",
     "powmod(a, e, n)", """
def powmod(a, e, n):
    r = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            r = (r * a) % n
        a = (a * a) % n
        e //= 2
    return r
""", [[2, 10, 1000], [3, 200, 13], [7, 0, 5], [5, 117, 19], [2, 1000, 1009]], "Square and halve the exponent."),
  PL("Sieve of Eratosthenes", "Write primes_upto(n): the list of primes up to n.",
     "primes_upto(n)", """
def primes_upto(n):
    if n < 2:
        return []
    s = [1] * (n + 1)
    s[0] = 0
    s[1] = 0
    i = 2
    while i * i <= n:
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = 0
        i += 1
    return [k for k in range(n + 1) if s[k]]
""", [[1], [2], [20], [50]], "Cross out multiples."),
  PL("Modular inverse", "Write inverse(a, p): the inverse of a modulo the prime p, computed as a^(p-2) mod p.",
     "inverse(a, p)", """
def inverse(a, p):
    r = 1
    e = p - 2
    b = a % p
    while e > 0:
        if e % 2 == 1:
            r = (r * b) % p
        b = (b * b) % p
        e //= 2
    return r
""", [[3, 7], [2, 11], [10, 13], [5, 17]], "Fermat's little theorem."),
  ORDER("Euclid", "Order the steps to find gcd(48, 18).", ["Divide 48 by 18: remainder 12", "Divide 18 by 12: remainder 6", "Divide 12 by 6: remainder 0", "Stop when the remainder is 0", "The last divisor 6 is the gcd"]),
  MATCH("Number theory", "Match each item with its value or idea.", [("gcd(12, 18)", "6"), ("7 mod 3", "1"), ("Fermat's inverse", "a^(p-2)"), ("RSA", "Factoring is hard"), ("Sieve", "Finds primes")]),
  FILL("Modular", "Euclid's algorithm computes the {{gcd|greatest common divisor}}; powers mod n use repeated {{squaring|square}}.")]))

CHS.append(CH(
 "Linear algebra I: vectors and matrices",
 ("Vectors", [
  "Vector | has | Magnitude and direction",
  "Dot product | measures | Alignment",
  "Norm | gives | Length",
  "Matrix | is | A linear map",
  "Matrix product | composes | Maps",
  "Transpose | flips | Rows and columns",
  "Cosine | scores | Angle similarity"]),
 ["Linear algebra is the language of data and of neural networks. A vector is a list of numbers, a point or an arrow in space. The dot product measures how aligned two vectors are, and the norm measures length.",
  "A matrix is a table of numbers and also a linear map: it turns vectors into vectors. Multiplying matrices composes maps. Almost every layer of a neural network is a matrix multiplication followed by a simple nonlinear function.",
  "The labs implement dot products, norms, cosine similarity, matrix-vector and matrix-matrix products and the transpose."],
 [("Vector", "An ordered list of numbers, an element of R^n."),
  ("Dot product", "x . y = sum x_i y_i = |x||y| cos(theta)."),
  ("Norm", "|x| = sqrt(x . x): the length of a vector."),
  ("Matrix", "A rectangular array that represents a linear map."),
  ("Matrix product", "(AB)_ij = sum_k A_ik B_kj; composition of maps."),
  ("Transpose", "Swap rows and columns: (A^T)_ij = A_ji.")],
 ["Dot product: x . y = |x||y| cos(theta); zero for orthogonal vectors.",
  "Cauchy-Schwarz: |x . y| <= |x||y|.",
  "Matrix product is associative but not commutative.",
  "(AB)^T = B^T A^T.",
  "A linear map satisfies f(ax + by) = a f(x) + b f(y).",
  "Cosine similarity = (x . y)/(|x||y|), used to compare embeddings."],
 [T("A vector is a list of n numbers. We can add vectors and scale them, and these two operations are what make linear algebra linear. Geometrically a vector in two or three dimensions is an arrow. In machine learning a vector is a data point, an embedding or a set of weights."),
  M(r"x \cdot y \;=\; \sum_{i=1}^{n} x_i y_i \;=\; \lVert x\rVert\,\lVert y\rVert \cos\theta, \qquad \lVert x \rVert = \sqrt{x\cdot x}"),
  T("The dot product multiplies matching entries and adds them. It equals the product of the lengths and the cosine of the angle between the vectors. If it is zero the vectors are orthogonal. Dividing by the lengths gives the cosine similarity, a measure of alignment between embeddings that ignores their size."),
  T("A matrix with m rows and n columns defines a linear map from vectors of length n to vectors of length m. The map sends x to A x, where each output entry is the dot product of a row with x. Rotations, scalings and projections are all matrices."),
  M(r"(AB)_{ij} \;=\; \sum_{k} A_{ik}\,B_{kj}, \qquad (AB)^{\top} = B^{\top} A^{\top}"),
  T("The product of two matrices corresponds to doing one map after the other. The order matters: A times B is usually not B times A. The sizes must match, with the columns of A equal to the rows of B. Matrix multiplication is associative, which lets us regroup long chains of layers."),
  T("Look at a neural-network layer: the output is a nonlinear function of W x plus b, with a weight matrix W. A whole batch of inputs is a matrix and is processed by one large multiplication, which GPUs do very fast. This is why linear algebra is at the heart of deep learning.")],
 [("What is the dot product of orthogonal vectors?", ["0", "1", "Their length", "Undefined"], 0, "cos 90 degrees = 0."),
  ("Is matrix multiplication commutative?", ["No", "Yes", "Only for squares", "Only for vectors"], 0, "AB is usually not BA."),
  ("What is (AB) transpose?", ["B transpose times A transpose", "A transpose times B transpose", "AB", "BA"], 0, "Order reverses."),
  ("What does cosine similarity ignore?", ["Vector length", "Direction", "Sign", "Dimension"], 0, "Only the angle matters.")],
 [("Norm of (3, 4)?", "5."), ("Matrix as a map?", "x goes to A x."), ("Is it associative?", "Yes."), ("What does a layer compute?", "A nonlinearity of W x + b.")],
 [PL("Dot product", "Write dot(x, y): the dot product of two equal-length lists.",
     "dot(x, y)", """
def dot(x, y):
    s = 0
    for a, b in zip(x, y):
        s += a * b
    return s
""", [[[1, 2, 3], [4, 5, 6]], [[1, 0], [0, 1]], [[2], [3]], [[0, 0], [1, 1]]], "Sum of products."),
  PL("Norm and cosine", "Write cosine(x, y): the cosine similarity of two nonzero vectors, rounded to 9 decimals. Use import math.",
     "cosine(x, y)", """
import math
def cosine(x, y):
    d = sum(a * b for a, b in zip(x, y))
    nx = math.sqrt(sum(a * a for a in x))
    ny = math.sqrt(sum(b * b for b in y))
    return round(d / (nx * ny), 9)
""", [[[1, 0], [0, 1]], [[1, 1], [2, 2]], [[1, 2, 3], [4, 5, 6]], [[1, 0], [-1, 0]]], "Dot over the product of norms.", approx=1e-9),
  PL("Matrix-vector product", "Write matvec(A, x): the product A x for a matrix given as a list of rows.",
     "matvec(A, x)", """
def matvec(A, x):
    out = []
    for row in A:
        s = 0
        for a, b in zip(row, x):
            s += a * b
        out.append(s)
    return out
""", [[[[1, 2], [3, 4]], [1, 1]], [[[1, 0], [0, 1]], [5, 6]], [[[2, 0, 1]], [1, 2, 3]], [[[0, 1], [1, 0]], [7, 8]]], "Dot product per row."),
  PL("Matrix product", "Write matmul(A, B): the product of two matrices given as lists of rows.",
     "matmul(A, B)", """
def matmul(A, B):
    n = len(A)
    m = len(B[0])
    k = len(B)
    out = [[0] * m for i in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0
            for t in range(k):
                s += A[i][t] * B[t][j]
            out[i][j] = s
    return out
""", [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], [[[1, 0], [0, 1]], [[2, 3], [4, 5]]], [[[1, 2, 3]], [[1], [2], [3]]], [[[0, 1], [1, 0]], [[0, 1], [1, 0]]]], "Triple loop."),
  PL("Transpose", "Write transpose(A): the transpose of a matrix.",
     "transpose(A)", """
def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]
""", [[[[1, 2], [3, 4]]], [[[1, 2, 3]]], [[[1], [2]]]], "Swap indices."),
  ORDER("A layer", "Order the steps of one neural-network layer.", ["Take the input vector x", "Multiply by the weight matrix W", "Add the bias b", "Apply the nonlinearity", "Pass the result on"]),
  MATCH("Vectors", "Match each item with its meaning.", [("Dot product", "Alignment"), ("Norm", "Length"), ("Cosine similarity", "Angle only"), ("Matrix product", "Composition of maps"), ("Transpose", "Swap rows and columns")]),
  FILL("Linear", "The dot product of orthogonal vectors is {{0|zero}}, and the product of matrices is not {{commutative}}.")]))
