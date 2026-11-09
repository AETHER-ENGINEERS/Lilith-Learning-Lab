#!/usr/bin/env python3
"""Build the Data Structures and Algorithms course. Usage: python3 make_dsa_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "dsa"))
import cmk, dsa1, dsa2  # noqa: E402

CHS = dsa1.CHS + dsa2.CHS

PRONOUNCE = {"BFS": "B F S", "DFS": "D F S", "BST": "B S T", "DAG": "dag", "LIFO": "lie foe", "FIFO": "fie foe", "LCS": "L C S",
    "Dijkstra's": "dike struz", "Dijkstra": "dike stra", "Kruskal's": "kruss kulz", "Kruskal": "kruss kul", "Huffman": "huff man",
    "Floyd's": "floyds", "Timsort": "tim sort", "AVL": "A V L", "Omega": "oh may guh", "Theta": "thay tuh", "memoisation": "mem oh eye zation",
    "Eratosthenes": "air uh tos thuh neez", "heapify": "heap ih fy", "Heapify": "heap ih fy", "Prim": "prim"}

SANDBOX = cmk.terminal("Complexity lookup", "ds>", "A scripted cheat sheet, not a profiler. Try: sort, search, structures, graph", [
    ("sort", ["insertion O(n^2) | merge O(n log n) | quick O(n log n) avg | heap O(n log n) | counting O(n + k)"]),
    ("search", ["linear O(n) | binary O(log n) on sorted data | hash O(1) average | BST O(height)"]),
    ("structures", ["array: index O(1) | linked list: head insert O(1) | stack, queue: O(1) | heap: push, pop O(log n) | hash table: O(1) avg"]),
    ("graph", ["BFS, DFS O(V + E) | Dijkstra O((V + E) log V) | Kruskal O(E log E)"]),
])

EXAM = [
 ("What is O(3n^2 + 5n)?", ["O(n^2)", "O(n)", "O(3n)", "O(1)"], 0, "Dominant term."),
 ("Binary search time?", ["O(log n)", "O(n)", "O(1)", "O(n^2)"], 0, "Halving."),
 ("Insert in the middle of an array costs?", ["O(n)", "O(1)", "O(log n)", "O(n^2)"], 0, "Shift later items."),
 ("Appending to a dynamic array is?", ["O(1) amortised", "O(n) always", "O(log n)", "O(n^2)"], 0, "Doubling."),
 ("What do prefix sums give?", ["O(1) range sums", "Sorting", "Hashing", "Searching"], 0, "One subtraction."),
 ("Insert at the head of a linked list?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 0, "Two pointers."),
 ("What does Floyd's algorithm detect?", ["A cycle", "A maximum", "Duplicates", "Sorted order"], 0, "Fast meets slow."),
 ("Stack order?", ["Last in first out", "First in first out", "Sorted", "Random"], 0, "Like plates."),
 ("Which structure does BFS use?", ["A queue", "A stack", "A heap", "A tree"], 0, "Rings outward."),
 ("What stores function calls?", ["The call stack", "A queue", "A hash table", "A heap"], 0, "Return addresses."),
 ("Average hash table lookup?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 0, "Constant."),
 ("What is a collision?", ["Two keys in one bucket", "A full table", "A missing key", "A resize"], 0, "Pigeonhole."),
 ("What does an inorder traversal of a BST give?", ["Sorted keys", "Reverse keys", "Levels", "Random keys"], 0, "Left, node, right."),
 ("Worst-case BST search?", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], 0, "A chain."),
 ("Where is the minimum of a min-heap?", ["At the root", "At the end", "In the middle", "Anywhere"], 0, "Heap property."),
 ("Heap push or pop cost?", ["O(log n)", "O(1)", "O(n)", "O(n log n)"], 0, "Sift."),
 ("BFS or DFS cost?", ["O(V + E)", "O(V^2) always", "O(E^2)", "O(1)"], 0, "Each once."),
 ("A topological order exists for?", ["DAGs", "Any graph", "Trees only", "Complete graphs"], 0, "No cycles."),
 ("Merge sort time?", ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"], 0, "Always."),
 ("Quick sort worst case?", ["O(n^2)", "O(n log n)", "O(n)", "O(1)"], 0, "Bad pivots."),
 ("Counting sort needs?", ["Small integer keys", "Any keys", "Sorted input", "A heap"], 0, "O(n + k)."),
 ("What does binary search require?", ["Sorted data", "A hash table", "Unique items", "A tree"], 0, "And random access."),
 ("What is a monotonic predicate?", ["False then true as input grows", "Always true", "Random", "A hash"], 0, "Allows search on answer."),
 ("What does every recursion need?", ["A base case", "A loop", "A hash", "A heap"], 0, "Else it never stops."),
 ("How many subsets of n items?", ["2^n", "n!", "n^2", "2n"], 0, "Include or not."),
 ("What does dynamic programming avoid?", ["Recomputing subproblems", "Recursion", "Tables", "Sorting"], 0, "Cache."),
 ("Memoisation is?", ["Top-down with a cache", "Bottom-up", "Greedy", "Random"], 0, "Recursive plus dictionary."),
 ("Cost of a DP?", ["States times work per state", "Always exponential", "Always linear", "Constant"], 0, "Count the table."),
 ("Interval scheduling greedy rule?", ["Earliest finish first", "Shortest first", "Earliest start first", "Random"], 0, "Exchange argument."),
 ("Dijkstra needs?", ["Non-negative weights", "A tree", "Negative weights", "Sorted nodes"], 0, "Else greedy fails."),
 ("What does Kruskal sort?", ["Edges", "Vertices", "Components", "Paths"], 0, "By weight."),
 ("What does union-find answer?", ["Whether two items share a set", "Shortest paths", "Sorted order", "The maximum"], 0, "Find and union."),
 ("Can greedy fail?", ["Yes, for some problems", "Never", "Only on trees", "Only with heaps"], 0, "Coin change with odd coins."),
 ("What is stable sorting?", ["Equal items keep their order", "No extra memory", "Always fast", "In place"], 0, "Matters for records."),
]

CFG = dict(id="data-structures-algorithms", title="Data Structures and Algorithms",
    subtitle="Complexity, arrays, lists, hashing, trees, heaps, graphs, sorting, searching, recursion, dynamic programming and greedy methods, with Python labs",
    description="The core data structures and algorithms every programmer needs, explained intuitively and practised in Python: Big-O, arrays and two pointers, linked lists, stacks and queues, hash tables, trees, heaps, graph traversal, sorting, binary search, recursion and divide and conquer, dynamic programming, and greedy algorithms with shortest paths and spanning trees. Every chapter has an ELI5 block.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="dsa", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "data-structures-algorithms.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
