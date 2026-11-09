"""Data structures and algorithms, part 2."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Graphs and traversal",
 ("Graphs", [
  "Graph | has | Vertices and edges",
  "Adjacency list | stores | Neighbours",
  "BFS | explores | Layer by layer",
  "DFS | explores | Deep first",
  "Visited set | prevents | Loops",
  "Topological sort | orders | A DAG",
  "Connected components | group | Reachable nodes"]),
 ["Graphs model networks of things and links. Stored as adjacency lists, they use memory proportional to vertices plus edges. Two traversals underlie almost every graph algorithm: breadth-first search with a queue and depth-first search with a stack or recursion.",
  "A visited set keeps traversals from looping. BFS finds shortest paths in unweighted graphs, DFS finds connected components, detects cycles and gives topological orders of dependency graphs.",
  "The labs build adjacency lists, run BFS and DFS, count components and sort tasks topologically."],
 [("Adjacency list", "For each vertex, the list of its neighbours."),
  ("BFS", "Visit nearest vertices first, using a queue."),
  ("DFS", "Follow a path as deep as possible, then backtrack."),
  ("Connected component", "A maximal set of mutually reachable vertices."),
  ("DAG", "A directed graph with no cycles."),
  ("Topological order", "Vertices ordered so each edge goes forward.")],
 ["BFS and DFS both run in O(V + E).",
  "BFS gives fewest-edge paths in unweighted graphs.",
  "DFS timestamps help find cycles and components.",
  "Adjacency lists suit sparse graphs; matrices suit dense ones.",
  "Topological order exists only for DAGs.",
  "Always mark a vertex visited when you first reach it."],
 [T("A graph is a set of vertices joined by edges. Maps, social networks, the web and course prerequisites are graphs. To store one, give each vertex a list of its neighbours. That takes memory proportional to the number of vertices plus edges, much better than an n by n table when few links exist."),
  T("Breadth-first search starts at a source and visits all neighbours, then their neighbours, and so on, using a queue. Because it explores in rings, the first time it reaches a vertex is along a path with the fewest edges. It runs in time proportional to vertices plus edges."),
  M(r"T_{\text{BFS}} = T_{\text{DFS}} = O(V + E)"),
  T("Depth-first search goes the other way: follow one path as far as it goes, then back up and try the next branch. It uses a stack, or recursion, which is the same thing. Marking vertices as visited stops it from going round cycles forever. It is the basis for finding connected components, checking for cycles and finding strongly connected components."),
  T("A topological sort orders the tasks of a dependency graph so every task comes after the tasks it needs. A simple method repeatedly removes a vertex with no incoming edges, Kahn's algorithm. If some vertices are left over, the graph has a cycle and no order exists. Build tools and course planners use it all the time.")],
 [("BFS finds?", ["Fewest-edge paths", "Weighted shortest paths", "The maximum", "A cycle only"], 0, "Rings outward."),
  ("What does BFS use?", ["A queue", "A stack", "A heap", "A hash"], 0, "First in first out."),
  ("Cost of BFS or DFS?", ["O(V + E)", "O(V^2) always", "O(E^2)", "O(1)"], 0, "Each vertex and edge once."),
  ("Topological order exists for?", ["DAGs", "Any graph", "Trees only", "Complete graphs"], 0, "No cycles.")],
 [("Why a visited set?", "Avoid loops and repeats."), ("Sparse graph storage?", "Adjacency lists."), ("Kahn's algorithm?", "Remove sources repeatedly."), ("DFS data structure?", "A stack or recursion.")],
 [PL("Build adjacency lists", "Write adj(n, edges): the undirected adjacency list (neighbours sorted ascending) for vertices 0..n-1 from a list of [u, v] edges.",
     "adj(n, edges)", """
def adj(n, edges):
    a = [[] for i in range(n)]
    for u, v in edges:
        a[u].append(v)
        a[v].append(u)
    return [sorted(x) for x in a]
""", [[3, [[0, 1], [1, 2]]], [2, []], [4, [[0, 3], [0, 1], [3, 1]]]], "Add both directions."),
  PL("BFS order", "Write bfs(n, edges, s): the vertices in BFS visiting order from s (neighbours in ascending order).",
     "bfs(n, edges, s)", """
def bfs(n, edges, s):
    a = [[] for i in range(n)]
    for u, v in edges:
        a[u].append(v)
        a[v].append(u)
    a = [sorted(x) for x in a]
    seen = [0] * n
    seen[s] = 1
    q = [s]
    i = 0
    while i < len(q):
        x = q[i]
        i += 1
        for y in a[x]:
            if not seen[y]:
                seen[y] = 1
                q.append(y)
    return q
""", [[4, [[0, 1], [0, 2], [1, 3]], 0], [3, [[0, 1]], 2], [5, [[0, 1], [1, 2], [2, 3], [3, 4]], 2]], "A queue and a seen list."),
  PL("Count components", "Write components(n, edges): the number of connected components, using DFS.",
     "components(n, edges)", """
def components(n, edges):
    a = [[] for i in range(n)]
    for u, v in edges:
        a[u].append(v)
        a[v].append(u)
    seen = [0] * n
    c = 0
    for s in range(n):
        if not seen[s]:
            c += 1
            st = [s]
            seen[s] = 1
            while st:
                x = st.pop()
                for y in a[x]:
                    if not seen[y]:
                        seen[y] = 1
                        st.append(y)
    return c
""", [[5, [[0, 1], [2, 3]]], [3, []], [4, [[0, 1], [1, 2], [2, 3]]]], "Start a new search for each unseen vertex."),
  PL("Topological sort", "Write topo(n, edges): a topological order of a DAG of directed edges [u, v] using Kahn's algorithm; always take the smallest available vertex. Return [] if there is a cycle.",
     "topo(n, edges)", """
def topo(n, edges):
    indeg = [0] * n
    out = [[] for i in range(n)]
    for u, v in edges:
        out[u].append(v)
        indeg[v] += 1
    ready = [i for i in range(n) if indeg[i] == 0]
    res = []
    while ready:
        ready.sort()
        x = ready.pop(0)
        res.append(x)
        for y in out[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                ready.append(y)
    return res if len(res) == n else []
""", [[4, [[0, 1], [1, 2], [0, 3]]], [3, [[0, 1], [1, 2], [2, 0]]], [3, []]], "Remove vertices with no prerequisites."),
  ORDER("BFS", "Order the steps.", ["Put the source in the queue and mark it", "Take the front vertex", "Visit its unmarked neighbours", "Mark them and enqueue them", "Repeat until the queue is empty"]),
  MATCH("Graph terms", "Match each term with its meaning.", [("BFS", "Queue; rings outward"), ("DFS", "Stack; deep first"), ("DAG", "Directed, no cycles"), ("Component", "Reachable group"), ("Adjacency list", "Neighbour lists")]),
  FILL("Graphs", "Breadth-first search uses a {{queue}}; both traversals cost O(V + E) because each vertex and {{edge}} is handled once.")]))

CHS.append(CH(
 "Sorting",
 ("Sorting", [
  "Sort | orders | Items",
  "Bubble | swaps | Neighbours",
  "Insertion | inserts | Into a sorted prefix",
  "Merge sort | merges | Sorted halves",
  "Quick sort | partitions | Around a pivot",
  "Counting sort | counts | Small integers",
  "Stable | keeps | Equal order"]),
 ["Sorting puts items in order and makes many other tasks easier, such as searching and finding duplicates. Simple methods like bubble and insertion sort take quadratic time. Merge sort and quick sort take n log n.",
  "Merge sort splits, sorts each half and merges, and it is stable. Quick sort partitions around a pivot and is fast on average. Comparison sorting cannot beat n log n, but counting sort uses the key values to reach linear time for small integer keys.",
  "The labs implement insertion sort, merge, quick sort partition and counting sort."],
 [("Stable sort", "Keeps the original order of equal items."),
  ("In-place sort", "Uses O(1) extra memory."),
  ("Merge sort", "Divide, sort halves, merge: O(n log n) always."),
  ("Quick sort", "Partition around a pivot: O(n log n) average, O(n^2) worst."),
  ("Counting sort", "Counts each key; O(n + k) for keys in 0..k."),
  ("Comparison bound", "Any comparison sort needs Omega(n log n) comparisons.")],
 ["Insertion sort: O(n^2) worst, O(n) on nearly sorted data.",
  "Merge sort: O(n log n), O(n) extra space, stable.",
  "Quick sort: O(n log n) average, in place, not stable.",
  "Heap sort: O(n log n), in place.",
  "Counting and radix sort: linear for bounded keys.",
  "Library sorts (Timsort) combine merge and insertion sort."],
 [T("Sorting is like arranging a hand of playing cards. Insertion sort does what you do naturally: take the next card and slide it into its place among the cards already sorted. For n cards it may take up to n squared moves, but if the hand is almost sorted it is very fast."),
  T("Merge sort splits the array in half, sorts each half recursively and merges the two sorted halves by repeatedly taking the smaller front item. There are log n levels of splitting, each costing n for the merges, so the total is n log n, whatever the input. It needs extra memory for merging but is stable."),
  M(r"T(n) = 2\,T(n/2) + O(n) \;\Rightarrow\; T(n) = O(n\log n)"),
  T("Quick sort picks a pivot, moves smaller items to its left and larger to its right, and recurses on both sides. On average it takes n log n and works in place, which makes it very fast in practice. A bad pivot, such as the smallest item every time, degrades it to n squared, so pivots are chosen randomly or by median of three."),
  T("There is a limit: any sorting method that works only by comparing items needs at least about n log n comparisons, because it must distinguish among n factorial orderings. To go faster you must use more than comparisons. Counting sort tallies how many times each small integer occurs and writes them out in order, in time linear in n plus the key range."),
  T("A sort is stable if equal items keep their relative order, which matters when sorting records by one field after another. The sort in your language library is usually Timsort, a stable hybrid of merge and insertion sort that exploits runs already in order.")],
 [("Merge sort time?", ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"], 0, "Always."),
  ("Quick sort worst case?", ["O(n^2)", "O(n log n)", "O(n)", "O(1)"], 0, "Bad pivots."),
  ("What does stable mean?", ["Equal items keep their order", "No extra memory", "Always fast", "In place"], 0, "Matters for multi-key sorts."),
  ("Counting sort needs?", ["Small integer keys", "Any keys", "Sorted input", "A heap"], 0, "O(n + k).")],
 [("Insertion sort strength?", "Nearly sorted data."), ("Lower bound?", "n log n for comparisons."), ("Pivot choice?", "Random or median of three."), ("Timsort?", "Hybrid of merge and insertion.")],
 [PL("Insertion sort", "Write insertion_sort(a): the list sorted ascending by insertion.",
     "insertion_sort(a)", """
def insertion_sort(a):
    a = list(a)
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a
""", [[[5, 2, 4, 1]], [[]], [[1, 2, 3]], [[3, 3, 1]]], "Slide into place."),
  PL("Merge two sorted lists", "Write merge(a, b): merge two sorted lists into one sorted list.",
     "merge(a, b)", """
def merge(a, b):
    i = 0
    j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
""", [[[1, 3, 5], [2, 4, 6]], [[], [1]], [[1, 1], [1]], [[5], [1, 2]]], "Take the smaller front item."),
  PL("Merge sort", "Write merge_sort(a): the list sorted using recursive merge sort.",
     "merge_sort(a)", """
def merge_sort(a):
    if len(a) <= 1:
        return list(a)
    m = len(a) // 2
    l = merge_sort(a[:m])
    r = merge_sort(a[m:])
    i = 0
    j = 0
    out = []
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            out.append(l[i])
            i += 1
        else:
            out.append(r[j])
            j += 1
    out.extend(l[i:])
    out.extend(r[j:])
    return out
""", [[[5, 2, 9, 1, 5, 6]], [[]], [[1]], [[3, 2, 1]]], "Split, sort, merge."),
  PL("Partition", "Write partition(a): take the last element as pivot; return [smaller_items, pivot, larger_or_equal_items] keeping the original order inside each part.",
     "partition(a)", """
def partition(a):
    p = a[-1]
    lo = [x for x in a[:-1] if x < p]
    hi = [x for x in a[:-1] if x >= p]
    return [lo, p, hi]
""", [[[3, 8, 1, 5, 4]], [[1]], [[2, 2, 2]]], "Smaller left, larger right."),
  PL("Counting sort", "Write counting_sort(a, k): sort integers in 0..k with counting sort.",
     "counting_sort(a, k)", """
def counting_sort(a, k):
    c = [0] * (k + 1)
    for x in a:
        c[x] += 1
    out = []
    for v in range(k + 1):
        out.extend([v] * c[v])
    return out
""", [[[3, 1, 2, 1, 0], 3], [[], 2], [[2, 2], 2]], "Count then write out."),
  ORDER("Quick sort", "Order the steps.", ["Pick a pivot", "Partition around it", "Recursively sort the smaller side", "Recursively sort the larger side", "Concatenate the results"]),
  MATCH("Sorting", "Match each sort with its key property.", [("Merge sort", "Always n log n, stable"), ("Quick sort", "Fast in place on average"), ("Insertion sort", "Great on nearly sorted data"), ("Counting sort", "Linear for small keys"), ("Heap sort", "n log n in place")]),
  FILL("Sorting", "Comparison sorts need at least about n log n comparisons; a {{stable}} sort keeps equal items in their original order.")]))

CHS.append(CH(
 "Searching and binary search",
 ("Searching", [
  "Linear search | scans | Everything",
  "Binary search | halves | A sorted range",
  "Midpoint | splits | The range",
  "Invariant | guards | Correctness",
  "Lower bound | finds | First position",
  "Search on answer | binary searches | A property",
  "Hash lookup | skips | Order"]),
 ["Linear search checks every item, taking linear time. If the data is sorted, binary search compares with the middle item and discards half the range each step, taking logarithmic time.",
  "Binary search is easy to describe and easy to get wrong. A clear invariant, the answer lies within the current range, prevents off-by-one errors. Variants find the first or last position of a value. You can also binary search over an answer, such as the smallest speed that finishes in time.",
  "The labs write binary search, find insertion points, count occurrences and search on an answer."],
 [("Binary search", "Repeatedly halve a sorted range by comparing with the middle."),
  ("Invariant", "A condition true at each loop step that proves correctness."),
  ("Lower bound", "The first index whose item is not less than the target."),
  ("Monotonic predicate", "A yes/no test that is false then true as the input grows."),
  ("Off-by-one error", "Using lo or hi one place wrong."),
  ("Interpolation search", "Guess the position from the value, for uniform data.")],
 ["Binary search needs sorted data and random access.",
  "Time O(log n): 1000 items need at most 10 steps; a billion need 30.",
  "Use mid = lo + (hi - lo) // 2 in languages with fixed-width integers.",
  "Decide the invariant first, then write the loop.",
  "Lower bound gives insertion points and counts via two searches.",
  "Search on answer works whenever a yes/no test is monotonic."],
 [T("Guess a number between one and a thousand. If I only say higher or lower, you can always find it in ten guesses: ask about 500, then 250 or 750, and so on. Each guess halves what remains. This is binary search, and it works on any sorted array."),
  M(r"n \to n/2 \to n/4 \to \cdots \to 1 \quad\Rightarrow\quad \lceil \log_2 n \rceil \text{ steps}"),
  T("The idea is simple, but small mistakes are common: infinite loops, skipping the answer, reading outside the array. The cure is to state an invariant. For example: the target, if present, lies in positions lo to hi inclusive. Each step must keep that true while shrinking the range."),
  T("A useful variant is the lower bound: the first position whose item is at least the target. It gives the insertion point for a new item in a sorted list. The number of occurrences of a value is the upper bound minus the lower bound, two searches."),
  T("Binary search is not only for arrays. Whenever a yes/no question is monotonic, false for small inputs and true from some point on, you can binary search for the switch. What is the smallest speed that lets a machine finish a job in eight hours? Test a speed; if it works, try slower, otherwise faster. This search on the answer solves many problems that look hard at first.")],
 [("Binary search time?", ["O(log n)", "O(n)", "O(1)", "O(n log n)"], 0, "Halving."),
  ("What does it require?", ["Sorted data", "A hash table", "Unique items", "A tree"], 0, "And random access."),
  ("How many steps for 1,000,000 items?", ["About 20", "About 1000", "About 500,000", "1"], 0, "log2 of a million."),
  ("What is a monotonic predicate?", ["False then true as input grows", "Always true", "Random", "A hash"], 0, "Allows search on the answer.")],
 [("Invariant for binary search?", "The target lies in lo..hi."), ("Lower bound?", "First item not less than the target."), ("Count of a value?", "Upper bound minus lower bound."), ("Search on answer?", "Binary search on a yes/no test.")],
 [PL("Binary search", "Write bsearch(a, t): the index of t in the sorted list a, or -1.",
     "bsearch(a, t)", """
def bsearch(a, t):
    lo = 0
    hi = len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == t:
            return mid
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
""", [[[1, 3, 5, 7, 9], 7], [[1, 3, 5], 4], [[], 1], [[2], 2]], "Keep the target in lo..hi."),
  PL("Lower bound", "Write lower_bound(a, t): the first index i with a[i] >= t (len(a) if none) in a sorted list.",
     "lower_bound(a, t)", """
def lower_bound(a, t):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid
    return lo
""", [[[1, 2, 2, 2, 5], 2], [[1, 2, 5], 3], [[1, 2], 9], [[], 1]], "The insertion point."),
  PL("Count occurrences", "Write count(a, t): how many times t appears in sorted list a, using two binary searches.",
     "count(a, t)", """
def count(a, t):
    def lb(x):
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo
    return lb(t + 1) - lb(t)
""", [[[1, 2, 2, 2, 5], 2], [[1, 2, 5], 3], [[7, 7, 7], 7]], "Integers: lower bound of t+1 minus that of t."),
  PL("Search on the answer", "Write min_speed(piles, hours): the smallest integer speed k such that eating every pile at k per hour (a pile of p takes ceil(p/k) hours) finishes within hours. Binary search k between 1 and max(piles).",
     "min_speed(piles, hours)", """
def min_speed(piles, hours):
    lo = 1
    hi = max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        need = 0
        for p in piles:
            need += (p + mid - 1) // mid
        if need <= hours:
            hi = mid
        else:
            lo = mid + 1
    return lo
""", [[[3, 6, 7, 11], 8], [[30, 11, 23, 4, 20], 5], [[5], 5], [[1, 1, 1], 3]], "Faster is monotonic."),
  ORDER("Binary search", "Order the steps in one loop.", ["Set lo and hi to the ends", "Find the middle index", "Compare the middle item with the target", "Discard the half that cannot hold the target", "Stop when the range is empty"]),
  MATCH("Searching", "Match each search with its cost.", [("Linear search", "O(n)"), ("Binary search", "O(log n)"), ("Hash lookup", "O(1) average"), ("BST search", "O(height)"), ("Search on answer", "O(log range) tests")]),
  FILL("Binary search", "Binary search needs {{sorted}} data and halves the range each step, so it takes {{O(log n)|logarithmic|log n}} time.")]))

CHS.append(CH(
 "Recursion and divide and conquer",
 ("Recursion", [
  "Recursion | calls | Itself",
  "Base case | stops | The recursion",
  "Divide and conquer | splits | Then combines",
  "Recurrence | describes | The cost",
  "Master theorem | solves | Recurrences",
  "Backtracking | tries | Then undoes",
  "Memoisation | caches | Results"]),
 ["Recursion solves a problem by solving smaller versions of the same problem. Every recursive function needs a base case that stops it and a step that makes progress toward it. The call stack remembers pending work.",
  "Divide and conquer splits a problem into parts, solves them recursively and combines the answers. Merge sort and binary search are examples. The cost is written as a recurrence, and the master theorem gives its solution. Backtracking explores choices and undoes them to enumerate subsets, permutations and puzzles.",
  "The labs write recursive functions, count recurrence cost and enumerate subsets and permutations."],
 [("Base case", "The smallest input answered directly."),
  ("Recursive case", "Reduces the problem and calls the function again."),
  ("Divide and conquer", "Split, solve parts, combine."),
  ("Recurrence", "A formula giving the cost in terms of smaller inputs."),
  ("Backtracking", "Build a solution step by step, undoing choices that fail."),
  ("Tail recursion", "A recursive call as the very last action.")],
 ["Always write the base case first.",
  "T(n) = a T(n/b) + O(n^d): compare a with b^d (master theorem).",
  "Binary search: T(n) = T(n/2) + O(1) = O(log n).",
  "Merge sort: T(n) = 2T(n/2) + O(n) = O(n log n).",
  "Naive Fibonacci is exponential; caching makes it linear.",
  "Subsets: 2^n; permutations: n!."],
 [T("Russian dolls: to open the whole set, open the biggest doll and find a smaller set of dolls inside. Keep going until the last tiny doll that does not open. Recursion works this way. A function solves a big problem by calling itself on a smaller one. The tiny doll is the base case, and without it the calls never stop."),
  T("A classic example is the factorial. By definition, n factorial is n times the factorial of n minus one, and the factorial of zero is one. The function calls itself with a smaller number each time until it reaches zero, then the pending multiplications finish on the way back. The computer remembers them on the call stack."),
  T("Divide and conquer is recursion with three steps: divide the problem into parts, conquer each part recursively and combine the answers. Merge sort divides the array in half, sorts each half and merges. Fast exponentiation computes a to the n by squaring a to the n over two. Many geometric and numeric algorithms follow this pattern."),
  M(r"T(n) = a\,T(n/b) + O(n^d) \;\Rightarrow\; T(n)=\begin{cases}O(n^d) & a<b^d\\ O(n^d\log n) & a=b^d\\ O(n^{\log_b a}) & a>b^d\end{cases}"),
  T("The master theorem reads the cost off the recurrence. Merge sort has a equal to two, b equal to two and d equal to one: a equals b to the d, so the answer is n log n. Binary search has a equal to one, b equal to two and d equal to zero, again balanced, giving log n."),
  T("Backtracking explores choices one at a time. To list all subsets, for each item either include it or not, recurse, then undo the choice. The tree of choices has two to the n leaves. It is also how puzzle solvers like sudoku and the n-queens problem work, cutting off branches that already break the rules.")],
 [("What does every recursion need?", ["A base case", "A loop", "A hash", "A heap"], 0, "Otherwise it never stops."),
  ("Merge sort recurrence?", ["2T(n/2) + O(n)", "T(n-1) + 1", "T(n/2) + 1", "2T(n-1)"], 0, "Two halves plus merge."),
  ("How many subsets of n items?", ["2^n", "n!", "n^2", "2n"], 0, "Include or not."),
  ("How many permutations of n items?", ["n!", "2^n", "n^2", "n"], 0, "Orderings.")],
 [("Master theorem balanced case?", "n^d log n."), ("Why does naive Fibonacci blow up?", "It repeats subproblems."), ("Backtracking idea?", "Choose, recurse, undo."), ("Recursion and stacks?", "Each call uses stack space.")],
 [PL("Power by squaring", "Write power(a, n): a^n by divide and conquer (n >= 0) using about log n multiplications.",
     "power(a, n)", """
def power(a, n):
    if n == 0:
        return 1
    h = power(a, n // 2)
    if n % 2 == 0:
        return h * h
    return h * h * a
""", [[2, 10], [3, 0], [5, 3], [7, 1]], "Square the half."),
  PL("Sum of digits", "Write digit_sum(n): the sum of decimal digits of n >= 0, recursively.",
     "digit_sum(n)", """
def digit_sum(n):
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)
""", [[0], [9], [123], [9999]], "Last digit plus the rest."),
  PL("All subsets", "Write subsets(a): the list of all subsets of a, each a list in input order, ordered by backtracking where each item is first excluded then included. For [1,2] the result is [[], [2], [1], [1, 2]].",
     "subsets(a)", """
def subsets(a):
    out = []
    cur = []
    def go(i):
        if i == len(a):
            out.append(list(cur))
            return
        go(i + 1)
        cur.append(a[i])
        go(i + 1)
        cur.pop()
    go(0)
    return out
""", [[[1, 2]], [[]], [[1, 2, 3]]], "Choose, recurse, undo."),
  PL("Permutations count", "Write perms(a): all permutations of a list of distinct items in lexicographic order of positions (swap-free: pick each unused item in turn).",
     "perms(a)", """
def perms(a):
    out = []
    used = [0] * len(a)
    cur = []
    def go():
        if len(cur) == len(a):
            out.append(list(cur))
            return
        for i in range(len(a)):
            if not used[i]:
                used[i] = 1
                cur.append(a[i])
                go()
                cur.pop()
                used[i] = 0
    go()
    return out
""", [[[1, 2, 3]], [[1]], [[1, 2]]], "Pick each unused item in turn."),
  ORDER("Write a recursion", "Order the steps.", ["State what the function returns", "Write the base case", "Reduce the problem", "Call the function on the smaller problem", "Combine the result"]),
  MATCH("Recursion", "Match each recurrence with its solution.", [("T(n) = T(n/2) + 1", "O(log n)"), ("T(n) = 2T(n/2) + n", "O(n log n)"), ("T(n) = T(n-1) + 1", "O(n)"), ("T(n) = 2T(n-1)", "O(2^n)"), ("T(n) = 2T(n/2) + 1", "O(n)")]),
  FILL("Recursion", "Every recursive function needs a {{base}} case; merge sort's cost solves to O(n {{log n|log}}).")]))

CHS.append(CH(
 "Dynamic programming",
 ("Dynamic programming", [
  "Subproblem | repeats | Often",
  "Memoisation | caches | Top-down",
  "Tabulation | fills | Bottom-up",
  "State | names | A subproblem",
  "Transition | links | States",
  "Knapsack | picks | Items under a limit",
  "LCS | compares | Sequences"]),
 ["Dynamic programming solves problems whose recursive solution repeats the same subproblems. By storing each answer once, either top-down with a cache or bottom-up with a table, exponential work becomes polynomial.",
  "The recipe is to define the state, write the transition that builds a state from smaller ones, set the base cases and read off the answer. Classic problems include Fibonacci, coin change, the knapsack, the longest common subsequence and edit distance.",
  "The labs solve Fibonacci, coin change, 0/1 knapsack, longest common subsequence and edit distance."],
 [("Overlapping subproblems", "The same smaller problem is needed many times."),
  ("Optimal substructure", "An optimal solution contains optimal solutions to subproblems."),
  ("Memoisation", "Top-down recursion with a cache."),
  ("Tabulation", "Bottom-up filling of a table."),
  ("State", "The parameters that identify a subproblem."),
  ("Transition", "The rule computing a state from smaller states.")],
 ["Cost is (number of states) x (cost per transition).",
  "Fibonacci: F(n) = F(n-1) + F(n-2); O(n) with a cache.",
  "Coin change: ways[a] sums ways[a - coin] over coins.",
  "Knapsack: best[i][w] = max(skip item, take item).",
  "LCS: match extends the diagonal; else take the max of two neighbours.",
  "Space can often be reduced to one or two rows."],
 [T("The naive recursive Fibonacci recomputes the same values again and again: computing F of fifty makes billions of calls. The fix is to remember. Each time you compute a value, store it; next time just look it up. This simple idea, remember what you computed, is dynamic programming."),
  T("There are two styles. In memoisation you keep the recursive code and add a dictionary: before computing, check the cache. In tabulation you fill a table from the smallest subproblems upward, so no recursion is needed. Both give the same result and the same running time; tabulation uses less stack."),
  T("Designing a solution follows a recipe. First choose the state: what numbers describe a subproblem? Then find the transition: how is the answer for a state built from answers of smaller ones? Then set the base cases, decide the order to fill the table and say where the final answer sits. The cost is the number of states times the work per state."),
  M(r"\text{best}[i][w] = \max\bigl(\text{best}[i-1][w],\ v_i + \text{best}[i-1][w-w_i]\bigr)"),
  T("In the 0/1 knapsack you may take or leave each item to maximise value under a weight limit. For each item and each capacity, either skip the item, or take it and use the remaining capacity best from before. The table has items times capacity cells, so it runs in pseudo-polynomial time."),
  T("Sequence problems use two-dimensional tables. The longest common subsequence of two strings extends the diagonal when the characters match, and otherwise takes the better of dropping a character from either string. Edit distance, the fewest insertions, deletions and replacements to turn one word into another, is similar and powers spell checkers.")],
 [("What does DP avoid?", ["Recomputing subproblems", "Recursion", "Tables", "Sorting"], 0, "Cache the answers."),
  ("Memoisation is?", ["Top-down with a cache", "Bottom-up", "Greedy", "Random"], 0, "Recursive plus dictionary."),
  ("Cost of a DP?", ["States times work per state", "Always exponential", "Always linear", "Constant"], 0, "Count the table."),
  ("Knapsack transition?", ["Skip or take the item", "Sort items", "Always take", "Random"], 0, "A max of two choices.")],
 [("Overlapping subproblems?", "Same smaller problem needed repeatedly."), ("Edit distance uses?", "Insert, delete, replace."), ("Why fill in order?", "Dependencies must be ready."), ("Space reduction?", "Keep only the rows needed.")],
 [PL("Fibonacci with memo", "Write fib(n): the n-th Fibonacci number (F0 = 0, F1 = 1) using a table.",
     "fib(n)", """
def fib(n):
    if n < 2:
        return n
    a = 0
    b = 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
""", [[0], [1], [10], [50], [70]], "Remember the last two values."),
  PL("Coin change ways", "Write ways(coins, amount): the number of combinations of coins (unlimited supply) that sum to amount.",
     "ways(coins, amount)", """
def ways(coins, amount):
    w = [0] * (amount + 1)
    w[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            w[a] += w[a - c]
    return w[amount]
""", [[[1, 2, 5], 5], [[2], 3], [[1], 0], [[1, 2, 3], 4]], "Loop over coins outside."),
  PL("0/1 knapsack", "Write knapsack(weights, values, cap): the best total value with total weight at most cap, each item used at most once.",
     "knapsack(weights, values, cap)", """
def knapsack(weights, values, cap):
    best = [0] * (cap + 1)
    for i in range(len(weights)):
        w = weights[i]
        v = values[i]
        for c in range(cap, w - 1, -1):
            if best[c - w] + v > best[c]:
                best[c] = best[c - w] + v
    return best[cap]
""", [[[1, 3, 4, 5], [1, 4, 5, 7], 7], [[2], [3], 1], [[1, 1], [1, 1], 2]], "Go downward to use items once."),
  PL("Longest common subsequence", "Write lcs(a, b): the length of the longest common subsequence of two strings.",
     "lcs(a, b)", """
def lcs(a, b):
    n = len(a)
    m = len(b)
    t = [[0] * (m + 1) for i in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max(t[i - 1][j], t[i][j - 1])
    return t[n][m]
""", [["abcde", "ace"], ["abc", "def"], ["", "a"], ["aggtab", "gxtxayb"]], "Extend the diagonal on a match."),
  PL("Edit distance", "Write edit(a, b): the minimum insertions, deletions and replacements to turn a into b.",
     "edit(a, b)", """
def edit(a, b):
    n = len(a)
    m = len(b)
    t = [[0] * (m + 1) for i in range(n + 1)]
    for i in range(n + 1):
        t[i][0] = i
    for j in range(m + 1):
        t[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c = 0 if a[i - 1] == b[j - 1] else 1
            t[i][j] = min(t[i - 1][j] + 1, t[i][j - 1] + 1, t[i - 1][j - 1] + c)
    return t[n][m]
""", [["kitten", "sitting"], ["", "abc"], ["abc", "abc"], ["horse", "ros"]], "Three moves, take the cheapest."),
  ORDER("Design a DP", "Order the steps.", ["Define the state", "Write the transition", "Set the base cases", "Choose the fill order", "Read the answer from the table"]),
  MATCH("DP problems", "Match each problem with its table.", [("Fibonacci", "One row"), ("Knapsack", "Items by capacity"), ("LCS", "Two strings by two strings"), ("Edit distance", "Prefix pairs"), ("Coin change", "Amount")]),
  FILL("DP", "Dynamic programming stores answers to {{overlapping|repeated}} subproblems; memoisation is {{top-down|top down}} and tabulation is bottom-up.")]))

CHS.append(CH(
 "Greedy algorithms, shortest paths and spanning trees",
 ("Greedy", [
  "Greedy | picks | The best now",
  "Exchange argument | proves | Greedy correct",
  "Interval scheduling | picks | Earliest finish",
  "Dijkstra | finds | Shortest paths",
  "Minimum spanning tree | connects | At least cost",
  "Union-find | tracks | Components",
  "Huffman | builds | Short codes"]),
 ["A greedy algorithm makes the best-looking choice at each step and never looks back. It is fast and simple, and for the right problems it is provably optimal. The proof usually shows that an optimal solution can be changed to include the greedy choice.",
  "Classic greedy results: choosing the most intervals by earliest finish time, Huffman coding, Dijkstra's shortest paths with non-negative weights, and Kruskal's and Prim's minimum spanning trees. Union-find is the data structure that makes Kruskal fast.",
  "The labs schedule intervals, run Dijkstra, build a minimum spanning tree with union-find and compute Huffman code cost."],
 [("Greedy choice", "Take the locally best option and commit."),
  ("Exchange argument", "Show swapping into the greedy choice never hurts."),
  ("Dijkstra", "Repeatedly settle the unsettled vertex with the smallest distance."),
  ("Spanning tree", "A tree that connects all vertices."),
  ("Union-find", "Structure with find (which set) and union (merge sets)."),
  ("Huffman code", "A prefix code with shorter codes for frequent symbols.")],
 ["Interval scheduling: sort by finish time, take every compatible interval.",
  "Dijkstra with a heap: O((V + E) log V); needs non-negative weights.",
  "Kruskal: sort edges, add if they join different components; O(E log E).",
  "Prim: grow a tree from a vertex by the cheapest edge out.",
  "Union-find with path compression is almost O(1) per operation.",
  "Greedy fails for coin change with odd coin sets and for knapsack."],
 [T("A greedy algorithm is like making change: give the biggest coin that fits, then repeat. For ordinary currencies this gives the fewest coins, but with coins of one, three and four, making six by greed takes four, one and one when two threes would do. Greedy is only right for problems with the right structure, and each use needs a proof."),
  T("Interval scheduling asks to fit the most non-overlapping meetings in one room. The best greedy rule is surprising: always pick the meeting that finishes earliest. The proof is an exchange argument: in any optimal schedule you can swap the first meeting for the earliest-finishing one without losing any."),
  T("Dijkstra's algorithm finds shortest paths from a source in a graph with non-negative edge weights. Keep a tentative distance for every vertex. Repeatedly take the unsettled vertex with the smallest distance, settle it, and relax its edges: if going through it makes a neighbour closer, update. A heap makes the choice fast."),
  M(r"d[v] \leftarrow \min\bigl(d[v],\ d[u] + w(u,v)\bigr)"),
  T("A minimum spanning tree connects all vertices with the least total edge weight. Kruskal's algorithm sorts the edges and adds each one unless it would form a cycle. To test for a cycle quickly we use union-find: each component is a set; find returns its representative and union merges two sets."),
  T("Huffman coding builds the best prefix code for compression. Repeatedly take the two least frequent symbols and join them under a new node whose weight is the sum. Frequent symbols end up near the top with short codes. The total cost is the sum of all the merged weights.")],
 [("Interval scheduling rule?", ["Earliest finish time first", "Shortest first", "Earliest start first", "Random"], 0, "Exchange argument."),
  ("Dijkstra needs?", ["Non-negative weights", "A tree", "Negative weights", "Sorted nodes"], 0, "Else the greedy step is wrong."),
  ("Kruskal sorts?", ["Edges", "Vertices", "Components", "Paths"], 0, "By weight."),
  ("Union-find answers?", ["Whether two items share a set", "Shortest paths", "Sorted order", "The maximum"], 0, "Find and union.")],
 [("Why can greedy fail?", "Local best is not always global best."), ("Prim vs Kruskal?", "Grow one tree vs. merge forests."), ("Path compression?", "Flatten the tree on find."), ("Huffman prefix code?", "No code is a prefix of another.")],
 [PL("Interval scheduling", "Write max_meetings(intervals): the maximum number of non-overlapping [start, end] intervals (an interval may start exactly when another ends).",
     "max_meetings(intervals)", """
def max_meetings(intervals):
    iv = sorted(intervals, key=lambda p: p[1])
    count = 0
    end = None
    for s, e in iv:
        if end is None or s >= end:
            count += 1
            end = e
    return count
""", [[[[1, 3], [2, 4], [3, 5]]], [[[1, 2]]], [[[1, 10], [2, 3], [4, 5]]], [[]]], "Earliest finish first."),
  PL("Dijkstra", "Write dijkstra(n, edges, s): shortest distances from s on a directed graph with edges [u, v, w] (w >= 0); unreachable vertices get -1.",
     "dijkstra(n, edges, s)", """
def dijkstra(n, edges, s):
    INF = 10 ** 9
    adj = [[] for i in range(n)]
    for u, v, w in edges:
        adj[u].append([v, w])
    d = [INF] * n
    d[s] = 0
    done = [0] * n
    for _ in range(n):
        u = -1
        for i in range(n):
            if not done[i] and d[i] < INF and (u == -1 or d[i] < d[u]):
                u = i
        if u == -1:
            break
        done[u] = 1
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return [x if x < INF else -1 for x in d]
""", [[3, [[0, 1, 4], [0, 2, 1], [2, 1, 2]], 0], [3, [[0, 1, 1]], 0], [2, [], 1]], "Settle the closest vertex each time."),
  PL("Minimum spanning tree weight", "Write mst(n, edges): total weight of a minimum spanning tree (Kruskal with union-find) of an undirected connected graph with edges [u, v, w].",
     "mst(n, edges)", """
def mst(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a = find(u)
        b = find(v)
        if a != b:
            parent[a] = b
            total += w
    return total
""", [[3, [[0, 1, 1], [1, 2, 2], [0, 2, 3]]], [4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 5]]], [1, []]], "Add an edge unless it makes a cycle."),
  PL("Huffman cost", "Write huffman(freqs): the total weighted cost of the Huffman code: repeatedly merge the two smallest frequencies, adding their sum to the cost.",
     "huffman(freqs)", """
def huffman(freqs):
    h = sorted(freqs)
    cost = 0
    while len(h) > 1:
        a = h.pop(0)
        b = h.pop(0)
        cost += a + b
        h.append(a + b)
        h.sort()
    return cost
""", [[[5, 9, 12, 13, 16, 45]], [[1, 1]], [[7]], [[1, 2, 3]]], "Merge the two smallest."),
  ORDER("Kruskal", "Order the steps.", ["Sort all edges by weight", "Take the lightest unused edge", "Check its ends are in different components", "If so add it and union the components", "Stop when n - 1 edges are chosen"]),
  MATCH("Greedy", "Match each algorithm with its rule.", [("Interval scheduling", "Earliest finish"), ("Dijkstra", "Closest unsettled vertex"), ("Kruskal", "Lightest safe edge"), ("Huffman", "Merge two smallest"), ("Union-find", "Track components")]),
  FILL("Greedy", "Dijkstra requires {{non-negative|nonnegative}} edge weights; Kruskal uses {{union-find|union find}} to avoid cycles.")]))
