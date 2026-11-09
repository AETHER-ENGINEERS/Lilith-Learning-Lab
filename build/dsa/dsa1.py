"""Data structures and algorithms, part 1."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Complexity and Big-O",
 ("Complexity", [
  "Algorithm | solves | A problem",
  "Time | grows with | Input size",
  "Big-O | bounds | Growth rate",
  "Constant | beats | Linear",
  "Logarithmic | beats | Linear",
  "Exponential | explodes | Quickly",
  "Space | counts | Memory used"]),
 ["An algorithm is a step-by-step method that solves a problem. We compare algorithms not by seconds on one machine but by how the work grows as the input grows. Big-O notation describes that growth, keeping only the dominant term.",
  "Common classes, from fast to slow, are constant, logarithmic, linear, n log n, quadratic and exponential. Space complexity counts memory in the same way. Amortised analysis averages occasional expensive steps over many cheap ones.",
  "The labs count operations, compare growth rates and find the Big-O class of simple loops."],
 [("Algorithm", "A finite sequence of precise steps that solves a problem."),
  ("Big-O", "An upper bound on growth: f(n) is O(g(n)) if f stays below a constant times g for large n."),
  ("Time complexity", "How the number of steps grows with input size n."),
  ("Space complexity", "How the memory used grows with n."),
  ("Amortised cost", "Average cost per operation over a long sequence."),
  ("Worst case", "The most work over all inputs of a given size.")],
 ["Order: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!).",
  "Drop constants and lower terms: 3n^2 + 5n + 2 is O(n^2).",
  "A single loop over n items is O(n); nested loops are O(n^2).",
  "Halving the problem each step gives O(log n).",
  "Appending to a growing array is O(1) amortised.",
  "Big-O is an upper bound; Omega is a lower bound; Theta is both."],
 [T("How fast is a program? Seconds depend on the machine, so we count steps instead, and ask how the count grows as the input gets bigger. Finding a name in an unsorted list of n names takes up to n looks. Finding a word in a dictionary takes far fewer, because you can jump to the middle and halve the search each time."),
  M(r"f(n) = O(g(n)) \iff \exists\, c, n_0:\ f(n) \le c\,g(n)\ \ \forall n \ge n_0"),
  T("Big-O keeps only the part that grows fastest and ignores constant factors. The expression three n squared plus five n plus two is O of n squared, because for big n the square dominates. Doubling n makes an O of n squared algorithm four times slower, but an O of n algorithm only twice as slow."),
  T("A few classes cover most programs. Constant time, O of one, does not depend on n, like reading one array cell. Logarithmic time, O of log n, halves the work each step, as in binary search. Linear time scans everything once. N log n is the cost of good sorting. Quadratic time compares all pairs. Exponential time doubles with each added item and is only usable for tiny inputs."),
  T("To analyse code, count the loops. One loop over n items is linear. A loop inside a loop is quadratic. A loop that halves the remaining range is logarithmic. Recursive code gives recurrences, solved later in the divide and conquer chapter."),
  T("Sometimes an operation is usually cheap but occasionally costly, like appending to a dynamic array that doubles its storage when full. Amortised analysis spreads the rare cost over all operations and shows the average is constant. Always state whether you mean the worst, the average or the amortised case.")],
 [("What is O(3n^2 + 5n)?", ["O(n^2)", "O(n)", "O(5n)", "O(3)"], 0, "Keep the dominant term."),
  ("Which grows fastest?", ["2^n", "n^2", "n log n", "n"], 0, "Exponential."),
  ("Binary search takes?", ["O(log n)", "O(n)", "O(1)", "O(n^2)"], 0, "Halves each step."),
  ("Two nested loops over n items?", ["O(n^2)", "O(n)", "O(log n)", "O(2n)"], 0, "All pairs.")],
 [("Why ignore constants?", "They do not change the growth rate."), ("What is amortised O(1)?", "Cheap on average over many operations."), ("Theta means?", "Tight bound, both upper and lower."), ("What is the worst case?", "The most steps over all inputs.")],
 [PL("Count loop steps", "Write steps(n): the number of times the body runs in two nested loops, i from 0..n-1 and j from i..n-1.",
     "steps(n)", """
def steps(n):
    c = 0
    for i in range(n):
        for j in range(i, n):
            c += 1
    return c
""", [[0], [1], [5], [10]], "It is n(n+1)/2."),
  PL("Halving steps", "Write halvings(n): how many times you can halve n (integer division) before it reaches 1. That is floor(log2 n); for n < 1 return 0.",
     "halvings(n)", """
def halvings(n):
    c = 0
    while n > 1:
        n //= 2
        c += 1
    return c
""", [[1], [2], [8], [1000], [1024]], "Logarithms count halvings."),
  PL("Which grows faster", "Write faster(n): return 1 if 2^n is larger than n^3 for this n, else 0.",
     "faster(n)", """
def faster(n):
    return 1 if 2 ** n > n ** 3 else 0
""", [[5], [10], [9], [20]], "Exponential eventually wins."),
  PL("Linear search count", "Write comparisons(xs, t): the number of comparisons a linear search makes to find t (or len(xs) if absent).",
     "comparisons(xs, t)", """
def comparisons(xs, t):
    c = 0
    for x in xs:
        c += 1
        if x == t:
            return c
    return c
""", [[[5, 3, 8], 3], [[5, 3, 8], 9], [[1], 1], [[], 4]], "Stop at the first match."),
  PL("Doubling array growth", "A dynamic array starts with capacity 1 and doubles when full. Write copies(n): the total number of element copies made while appending n items.",
     "copies(n)", """
def copies(n):
    cap = 1
    size = 0
    total = 0
    for _ in range(n):
        if size == cap:
            total += size
            cap *= 2
        size += 1
    return total
""", [[1], [2], [5], [16], [100]], "Total copies stay below 2n."),
  ORDER("Analyse an algorithm", "Order the steps.", ["Define the input size n", "Identify the basic operation", "Count how often it runs as n grows", "Drop constants and lower terms", "State the Big-O class"]),
  MATCH("Growth", "Match each algorithm with its class.", [("Array index", "O(1)"), ("Binary search", "O(log n)"), ("Linear scan", "O(n)"), ("Merge sort", "O(n log n)"), ("All pairs", "O(n^2)")]),
  FILL("Big-O", "Big-O keeps only the {{dominant|fastest-growing}} term; halving the range each step gives {{logarithmic|log n|O(log n)}} time.")]))

CHS.append(CH(
 "Arrays, strings and two pointers",
 ("Arrays", [
  "Array | stores | Items contiguously",
  "Index | gives | O(1) access",
  "Insert | shifts | Later items",
  "String | is | An array of characters",
  "Two pointers | scan | From both ends",
  "Sliding window | tracks | A range",
  "Prefix sum | answers | Range queries"]),
 ["An array stores items side by side in memory, so any item is reached by its index in constant time. Inserting or deleting in the middle shifts later items and costs linear time. Dynamic arrays grow by doubling.",
  "Strings are arrays of characters. Many problems on arrays fall to simple patterns: two pointers moving from both ends, a sliding window over a range, and prefix sums that answer range-sum questions in constant time after one pass.",
  "The labs reverse in place, check palindromes, find pairs with a target sum, maximise a window and build prefix sums."],
 [("Array", "A contiguous block of equal-sized cells indexed from 0."),
  ("Dynamic array", "An array that doubles its capacity when full."),
  ("Two pointers", "Two indices moving through the data, often from opposite ends."),
  ("Sliding window", "A range that grows or shrinks as it moves along."),
  ("Prefix sum", "P[i] = sum of the first i items; range sum = P[j] - P[i]."),
  ("In place", "Modifying data without extra storage proportional to n.")],
 ["Access O(1); search O(n); insert or delete in the middle O(n); append O(1) amortised.",
  "Two pointers on a sorted array finds a pair in O(n).",
  "Sliding window turns an O(n k) scan into O(n).",
  "Prefix sums answer sum(i..j) in O(1) after O(n) setup.",
  "Strings are immutable in many languages: building by repeated joining costs O(n^2).",
  "Check the empty array and one-element cases."],
 [T("Imagine a row of lockers numbered from zero. Because they are side by side, you can walk straight to locker 37 without opening the others. That is an array: any element is available by index in constant time. The price is that inserting in the middle forces everyone after the new item to shift one place."),
  T("A dynamic array hides the fixed size. When full, it allocates a block twice as big and copies the items over. Most appends are cheap and the occasional copy is paid for by the many cheap ones, so appending is constant on average. Python lists work this way."),
  T("Two pointers is a favourite trick. To reverse an array, swap the first and last items and move the pointers inward. To find two numbers in a sorted array that add to a target, start at both ends: if the sum is too big, move the right pointer left; if too small, move the left pointer right. One pass, no nested loops."),
  M(r"\text{sum}(i..j) = P[j+1] - P[i], \qquad P[0]=0,\ P[k+1] = P[k] + a_k"),
  T("A sliding window handles questions about ranges. To find the largest sum of any k consecutive numbers, add the next item and drop the oldest one instead of recomputing the whole range. Prefix sums do the opposite job: after one pass that stores running totals, the sum of any range is a single subtraction."),
  T("Strings are arrays of characters, so the same patterns apply: palindromes by two pointers, longest substring without repeats by a sliding window. A frequent gotcha is that strings can be immutable, so gluing them in a loop copies repeatedly; collect pieces in a list and join once.")],
 [("Access by index costs?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 0, "Direct address."),
  ("Insert in the middle of an array costs?", ["O(n)", "O(1)", "O(log n)", "O(n^2)"], 0, "Shift the rest."),
  ("What do prefix sums give?", ["O(1) range sums", "Sorting", "Searching", "Hashing"], 0, "One subtraction."),
  ("Two pointers on a sorted array finds a pair in?", ["O(n)", "O(n^2)", "O(log n)", "O(1)"], 0, "One pass.")],
 [("Why double the capacity?", "Amortised O(1) append."), ("What is in place?", "No extra storage proportional to n."), ("Window trick?", "Add new item, drop old one."), ("String join gotcha?", "Repeated concatenation copies.")],
 [PL("Reverse in place", "Write reverse(a): return the list reversed using two pointers (swap from both ends).",
     "reverse(a)", """
def reverse(a):
    a = list(a)
    i = 0
    j = len(a) - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1
    return a
""", [[[1, 2, 3, 4]], [[1]], [[]], [[5, 4, 3]]], "Swap and move inward."),
  PL("Palindrome", "Write is_pal(s): 1 if the string reads the same both ways, else 0.",
     "is_pal(s)", """
def is_pal(s):
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return 0
        i += 1
        j -= 1
    return 1
""", [["abba"], ["abc"], ["a"], [""], ["racecar"]], "Compare the ends."),
  PL("Pair with target sum", "Write pair_sum(a, t): for a sorted list a, return [i, j] with i < j and a[i] + a[j] == t using two pointers, or [-1, -1].",
     "pair_sum(a, t)", """
def pair_sum(a, t):
    i = 0
    j = len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == t:
            return [i, j]
        if s < t:
            i += 1
        else:
            j -= 1
    return [-1, -1]
""", [[[1, 2, 4, 7, 11], 9], [[1, 2, 3], 10], [[2, 5], 7], [[], 1]], "Move the pointer that fixes the sum."),
  PL("Max window sum", "Write max_window(a, k): the largest sum of k consecutive items (a has at least k items), by sliding the window.",
     "max_window(a, k)", """
def max_window(a, k):
    s = sum(a[:k])
    best = s
    for i in range(k, len(a)):
        s += a[i] - a[i - k]
        if s > best:
            best = s
    return best
""", [[[1, 4, 2, 10, 2, 3, 1], 3], [[5], 1], [[-1, -2, -3], 2], [[2, 2, 2, 2], 4]], "Add the new, drop the old."),
  PL("Prefix sums", "Write range_sums(a, queries): for each [i, j] (inclusive) return sum(a[i..j]) using prefix sums.",
     "range_sums(a, queries)", """
def range_sums(a, queries):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    return [p[j + 1] - p[i] for i, j in queries]
""", [[[1, 2, 3, 4], [[0, 3], [1, 2], [2, 2]]], [[5, -1, 2], [[0, 0], [0, 2]]]], "One subtraction each."),
  ORDER("Sliding window", "Order the steps for the max sum of k items.", ["Sum the first k items", "Record it as the best", "Add the next item", "Subtract the item leaving the window", "Update the best and repeat"]),
  MATCH("Array patterns", "Match each pattern with its use.", [("Two pointers", "Pairs in sorted data"), ("Sliding window", "Best range of fixed size"), ("Prefix sum", "Fast range sums"), ("Dynamic array", "Amortised append"), ("In place", "No extra storage")]),
  FILL("Arrays", "Array access by index is {{O(1)|constant}} time; inserting in the middle must {{shift}} later items.")]))

CHS.append(CH(
 "Linked lists",
 ("Linked lists", [
  "Node | holds | Value and next",
  "Head | starts | The list",
  "Insert at head | costs | O(1)",
  "Search | costs | O(n)",
  "Reverse | flips | Pointers",
  "Fast and slow | detect | Cycles",
  "Doubly linked | adds | Previous"]),
 ["A linked list is a chain of nodes; each node holds a value and a pointer to the next node. Unlike arrays there is no jump-by-index, but inserting or deleting at a known node needs only pointer changes.",
  "Classic tasks are reversing a list, finding the middle with a fast and a slow pointer, detecting a cycle and merging sorted lists. Doubly linked lists keep a pointer back as well, which makes deletion from both ends easy.",
  "The labs use arrays to simulate nodes: a list of values and a list of next-indices."],
 [("Node", "A record with a value and a link to another node."),
  ("Head", "The first node; the entry point to the list."),
  ("Singly linked", "Each node points only forward."),
  ("Doubly linked", "Each node points forward and backward."),
  ("Cycle", "A node whose chain leads back to an earlier node."),
  ("Floyd's algorithm", "Fast pointer moves 2 steps, slow 1; they meet if there is a cycle.")],
 ["Insert or delete at the head: O(1).",
  "Access or search by position: O(n).",
  "Reverse in O(n) time and O(1) extra space.",
  "Fast and slow pointers find the middle and detect cycles.",
  "Linked lists use extra memory for pointers and are cache-unfriendly.",
  "Arrays win for random access; lists win for frequent splicing."],
 [T("Picture a treasure hunt where each clue tells you where the next clue is. That is a linked list. Each node stores a value and a reference to the next node, and the head is the first clue. To reach the tenth item you must follow ten links, so access by position costs linear time."),
  T("The reward is cheap changes. To insert a new node after a given node, point the new node at that node's successor and the node at the new one: two pointer updates, no shifting. Deleting works the same way. Adding at the head is constant time, which makes linked lists a natural base for stacks."),
  T("To reverse a list, walk along it keeping three pointers: the previous node, the current node and the next. At each step, redirect the current node's pointer back to the previous one, then advance. When the walk ends, the previous node is the new head. It takes one pass and no extra storage."),
  T("The fast and slow pointer trick finds the middle: move one pointer two steps and another one step, and when the fast one reaches the end the slow one is at the middle. If the list has a cycle, the fast pointer eventually laps the slow one, so they meet. This is Floyd's tortoise and hare algorithm."),
  T("A doubly linked list keeps a link backward too, so you can delete a node you are standing on and walk in both directions, at the price of more memory. In practice arrays are faster for most work because they are laid out contiguously and friendly to the processor cache; linked lists matter when you splice often.")],
 [("Insert at the head costs?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 0, "Two pointer changes."),
  ("Access the k-th node costs?", ["O(k)", "O(1)", "O(log k)", "O(k^2)"], 0, "Follow links."),
  ("What does Floyd's algorithm detect?", ["A cycle", "The maximum", "Sorted order", "Duplicates"], 0, "Fast meets slow."),
  ("Where does the slow pointer end when fast reaches the end?", ["The middle", "The head", "The end", "Nowhere"], 0, "Half speed.")],
 [("Why reverse needs three pointers?", "To avoid losing the rest of the list."), ("Doubly linked benefit?", "Delete and walk in both directions."), ("Why are arrays faster in practice?", "Cache-friendly layout."), ("Linked-list weakness?", "No random access.")],
 [PL("Walk a list", "A list is given as vals and nxt arrays (nxt[i] is the index of the next node or -1) with head index h. Write to_list(vals, nxt, h): the values in order.",
     "to_list(vals, nxt, h)", """
def to_list(vals, nxt, h):
    out = []
    while h != -1:
        out.append(vals[h])
        h = nxt[h]
    return out
""", [[[10, 20, 30], [1, 2, -1], 0], [[5], [-1], 0], [[1, 2, 3], [-1, 0, 1], 2], [[], [], -1]], "Follow next until -1."),
  PL("Reverse a list", "Write reverse_list(vals, nxt, h): reverse the linked list by redirecting pointers (not copying values) and return the values in the new order.",
     "reverse_list(vals, nxt, h)", """
def reverse_list(vals, nxt, h):
    nxt = list(nxt)
    prev = -1
    cur = h
    while cur != -1:
        n = nxt[cur]
        nxt[cur] = prev
        prev = cur
        cur = n
    out = []
    cur = prev
    while cur != -1:
        out.append(vals[cur])
        cur = nxt[cur]
    return out
""", [[[10, 20, 30], [1, 2, -1], 0], [[5], [-1], 0], [[1, 2], [1, -1], 0]], "prev, cur, next."),
  PL("Middle node", "Write middle(vals, nxt, h): the value of the middle node (the second middle for even length), using fast and slow pointers.",
     "middle(vals, nxt, h)", """
def middle(vals, nxt, h):
    slow = h
    fast = h
    while fast != -1 and nxt[fast] != -1:
        slow = nxt[slow]
        fast = nxt[nxt[fast]]
    return vals[slow]
""", [[[1, 2, 3], [1, 2, -1], 0], [[1, 2, 3, 4], [1, 2, 3, -1], 0], [[7], [-1], 0]], "Fast moves twice as far."),
  PL("Has a cycle", "Write has_cycle(nxt, h): 1 if following next from h loops forever (Floyd's algorithm), else 0.",
     "has_cycle(nxt, h)", """
def has_cycle(nxt, h):
    slow = h
    fast = h
    while fast != -1 and nxt[fast] != -1:
        slow = nxt[slow]
        fast = nxt[nxt[fast]]
        if slow == fast:
            return 1
    return 0
""", [[[1, 2, -1], 0], [[1, 2, 0], 0], [[0], 0], [[1, 1], 0], [[-1], 0]], "They meet if there is a loop."),
  ORDER("Reverse a list", "Order the steps in the loop.", ["Save the next node", "Point the current node back at the previous", "Move previous to current", "Move current to the saved next", "Stop when current is empty"]),
  MATCH("Lists", "Match each term with its meaning.", [("Head", "First node"), ("Singly linked", "Pointers forward only"), ("Doubly linked", "Pointers both ways"), ("Floyd", "Cycle detection"), ("Insert at head", "O(1)")]),
  FILL("Lists", "A linked list node stores a value and a {{next|pointer}} link; finding a cycle uses a {{fast}} and a slow pointer.")]))

CHS.append(CH(
 "Stacks, queues and deques",
 ("Stacks and queues", [
  "Stack | is | Last in first out",
  "Queue | is | First in first out",
  "Deque | works | At both ends",
  "Push and pop | change | The top",
  "Enqueue and dequeue | change | The ends",
  "Call stack | tracks | Function calls",
  "Monotonic stack | finds | Next greater"]),
 ["A stack allows adding and removing only at one end: last in, first out, like a pile of plates. A queue adds at the back and removes from the front: first in, first out, like a line at a shop. A deque works at both ends.",
  "Stacks power undo, expression evaluation, bracket matching and the call stack of recursion. Queues power scheduling and breadth-first search. A monotonic stack solves next-greater-element problems in linear time.",
  "The labs match brackets, evaluate postfix expressions, simulate a queue and find the next greater elements."],
 [("Stack", "LIFO structure with push and pop."),
  ("Queue", "FIFO structure with enqueue and dequeue."),
  ("Deque", "Double-ended queue: push and pop at both ends."),
  ("Call stack", "The stack of active function calls."),
  ("Postfix notation", "Operators follow operands: 3 4 + means 3 + 4."),
  ("Monotonic stack", "A stack kept in sorted order to answer next-greater queries.")],
 ["All basic stack and queue operations are O(1).",
  "A stack implemented on an array pushes and pops at the end.",
  "A queue on an array uses head and tail indices or a deque.",
  "Balanced brackets: push openers, pop on closers and match.",
  "Postfix evaluation: push numbers, apply operators to the top two.",
  "Next greater element: pop smaller items as larger ones arrive."],
 [T("A stack is a pile of plates. You add a plate on top and you take a plate from the top, so the last plate in is the first out. The two operations, push and pop, take constant time. Your web browser's back button and your editor's undo are stacks of past states."),
  T("Computers use a stack to remember where they were. When a function calls another, the return address goes on the call stack; when the callee finishes, it is popped. Deep recursion can overflow this stack. Any recursive algorithm can be rewritten with an explicit stack."),
  T("To check brackets, scan the text. Push each opening bracket; for each closing bracket, pop and check it matches. If the stack is empty at the end and no mismatch occurred, the brackets are balanced. The same idea evaluates postfix expressions: push numbers, and when an operator arrives, pop two numbers, apply it and push the result."),
  T("A queue is the line at a shop: people join at the back and are served from the front. Operating systems queue jobs; breadth-first search uses a queue to explore nearest nodes first. A deque supports both ends and is the standard tool for sliding-window maximum problems."),
  T("A monotonic stack keeps its items in sorted order. To find, for each number, the next larger number to its right, scan from left to right and pop every stack item smaller than the new number: the new number is their answer. Each item is pushed and popped once, so the whole scan is linear.")],
 [("Stack order?", ["Last in first out", "First in first out", "Sorted", "Random"], 0, "Like plates."),
  ("Queue order?", ["First in first out", "Last in first out", "Sorted", "Reverse"], 0, "Like a line."),
  ("What does BFS use?", ["A queue", "A stack", "A heap", "A tree"], 0, "Nearest first."),
  ("What stores function calls?", ["The call stack", "The heap", "A queue", "A hash table"], 0, "Return addresses.")],
 [("Cost of push and pop?", "O(1)."), ("Deque use?", "Both ends; sliding window max."), ("Recursion and stacks?", "Recursion uses the call stack."), ("Postfix benefit?", "No parentheses needed.")],
 [PL("Balanced brackets", "Write balanced(s): 1 if the brackets ()[]{} in s are properly nested and matched, else 0.",
     "balanced(s)", """
def balanced(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in '([{':
            st.append(ch)
        elif ch in pairs:
            if not st or st.pop() != pairs[ch]:
                return 0
    return 1 if not st else 0
""", [["()[]{}"], ["(]"], ["((("], [""], ["{[()]}"]], "Push openers, pop on closers."),
  PL("Postfix evaluation", "Write postfix(tokens): evaluate a list of strings such as ['3','4','+','2','*'] with + - * and integers; return the result.",
     "postfix(tokens)", """
def postfix(tokens):
    st = []
    for t in tokens:
        if t in ('+', '-', '*'):
            b = st.pop()
            a = st.pop()
            if t == '+':
                st.append(a + b)
            elif t == '-':
                st.append(a - b)
            else:
                st.append(a * b)
        else:
            st.append(int(t))
    return st[0]
""", [[['3', '4', '+', '2', '*']], [['5']], [['2', '3', '4', '*', '+']], [['10', '3', '-']]], "Pop two, push result."),
  PL("Next greater element", "Write next_greater(a): for each item the next larger item to its right, or -1, with a monotonic stack.",
     "next_greater(a)", """
def next_greater(a):
    res = [-1] * len(a)
    st = []
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res
""", [[[2, 1, 5, 3, 6]], [[3, 2, 1]], [[1, 2, 3]], [[]]], "Pop smaller items."),
  PL("Queue simulation", "Write serve(arrivals, k): jobs arrive in the given order into a queue and the server removes k jobs in order; return the list of jobs left in the queue (front first).",
     "serve(arrivals, k)", """
def serve(arrivals, k):
    q = list(arrivals)
    head = 0
    for _ in range(k):
        if head < len(q):
            head += 1
    return q[head:]
""", [[[1, 2, 3, 4], 2], [[1], 5], [[], 1], [[5, 6], 0]], "First in, first out."),
  ORDER("Check brackets", "Order the steps.", ["Scan the characters left to right", "Push each opening bracket", "On a closing bracket pop and compare", "Fail if empty or mismatched", "Succeed if the stack is empty at the end"]),
  MATCH("Stacks and queues", "Match each use with its structure.", [("Undo", "Stack"), ("Print jobs", "Queue"), ("Breadth-first search", "Queue"), ("Recursion", "Call stack"), ("Sliding window maximum", "Deque")]),
  FILL("Stack", "A stack is {{LIFO|last in first out|last-in first-out}}; a queue is {{FIFO|first in first out|first-in first-out}}.")]))

CHS.append(CH(
 "Hash tables",
 ("Hashing", [
  "Hash function | maps | Keys to numbers",
  "Bucket | holds | Entries",
  "Collision | is | Two keys one bucket",
  "Chaining | stores | Lists in buckets",
  "Open addressing | probes | Other slots",
  "Load factor | triggers | Resizing",
  "Dictionary | is | A hash table"]),
 ["A hash table stores key-value pairs and finds a key in constant time on average. A hash function turns the key into a number, which picks a bucket. Different keys can land in the same bucket, a collision, handled by chaining or probing.",
  "When the table fills up, the load factor grows and collisions rise, so the table is resized. Python dictionaries and sets are hash tables. They are the first tool for counting, grouping and finding duplicates.",
  "The labs implement a hash function, a chained table, two-sum with a dictionary and frequency counts."],
 [("Hash function", "A function mapping a key to an integer bucket index."),
  ("Collision", "Two different keys with the same bucket."),
  ("Chaining", "Each bucket holds a list of entries."),
  ("Open addressing", "On collision, probe other slots in a fixed order."),
  ("Load factor", "Number of entries divided by number of buckets."),
  ("Hash set", "A hash table that stores keys only.")],
 ["Average insert, lookup and delete: O(1); worst case O(n).",
  "A good hash spreads keys evenly over buckets.",
  "Resize (double the buckets) when the load factor passes about 0.7.",
  "Keys must be hashable: immutable and with stable hashes.",
  "Use a dictionary for counting, grouping and caching.",
  "Hash tables do not keep sorted order."],
 [T("Suppose you want to find a person's phone number instantly. You could store numbers in an array indexed by a code computed from the name. That code is a hash, and the array is a hash table. Looking up a key means computing its hash, jumping to that cell and reading the value: constant time, no matter how many entries there are."),
  M(r"\text{bucket}(k) = h(k) \bmod m"),
  T("A good hash function spreads keys evenly. A simple one for strings multiplies a running total by a prime and adds each character, then takes the remainder by the table size. Since there are far more possible keys than buckets, two keys sometimes collide, by the pigeonhole principle."),
  T("There are two main ways to handle collisions. Chaining makes each bucket a small list holding all entries that landed there. Open addressing keeps everything in the array and, on a collision, tries the next slot or another one given by a probe sequence. Both stay fast when the table is not too full."),
  T("The load factor is the ratio of entries to buckets. When it grows past a threshold such as seventy percent, the table doubles its bucket array and re-inserts every key. Like the dynamic array, this rare costly step is amortised across many cheap operations."),
  T("Hash tables answer the question 'have I seen this before?' in one step, which is why they solve counting words, finding duplicates and the classic two-sum problem: for each number, check whether its complement is already in the dictionary. Their weakness is order: they do not keep keys sorted.")],
 [("Average lookup in a hash table?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 0, "Constant on average."),
  ("What is a collision?", ["Two keys in one bucket", "A full table", "A missing key", "A hash error"], 0, "Pigeonhole."),
  ("What does chaining do?", ["Stores lists in buckets", "Sorts keys", "Resizes", "Deletes keys"], 0, "Many entries per bucket."),
  ("When is a table resized?", ["When the load factor is high", "When empty", "Never", "On every insert"], 0, "Keeps collisions low.")],
 [("Why immutable keys?", "Their hash must not change."), ("Worst-case lookup?", "O(n) if everything collides."), ("Two-sum idea?", "Look up the complement."), ("Hash tables and order?", "No sorted order.")],
 [PL("String hash", "Write h(s, m): the hash of string s: start with 0; for each character c do v = (v * 31 + ord(c)) % m; return v.",
     "h(s, m)", """
def h(s, m):
    v = 0
    for c in s:
        v = (v * 31 + ord(c)) % m
    return v
""", [["abc", 101], ["", 7], ["hello", 1000], ["a", 10]], "Multiply, add, wrap."),
  PL("Chained table", "Write chained(keys, m): insert the integer keys into a table with m buckets (bucket = key % m) using chaining; return the list of bucket lengths.",
     "chained(keys, m)", """
def chained(keys, m):
    b = [[] for i in range(m)]
    for k in keys:
        b[k % m].append(k)
    return [len(x) for x in b]
""", [[[1, 2, 3, 4, 5, 6], 3], [[10, 20, 30], 10], [[], 4]], "One list per bucket."),
  PL("Two-sum with a dictionary", "Write two_sum(a, t): indices [i, j] (i < j) of two items summing to t using a dictionary, or [-1, -1].",
     "two_sum(a, t)", """
def two_sum(a, t):
    seen = {}
    for j, x in enumerate(a):
        if t - x in seen:
            return [seen[t - x], j]
        seen[x] = j
    return [-1, -1]
""", [[[2, 7, 11, 15], 9], [[3, 2, 4], 6], [[1, 2], 10], [[3, 3], 6]], "Look up the complement."),
  PL("Most frequent item", "Write most_common(a): the value that occurs most often (the smallest value if tied).",
     "most_common(a)", """
def most_common(a):
    c = {}
    for x in a:
        c[x] = c.get(x, 0) + 1
    best = None
    for k in c:
        if best is None or c[k] > c[best] or (c[k] == c[best] and k < best):
            best = k
    return best
""", [[[1, 2, 2, 3, 3]], [[5]], [[4, 4, 1, 1, 1]]], "Count with a dictionary."),
  PL("Has duplicates", "Write has_dup(a): 1 if any value appears twice, else 0, using a set.",
     "has_dup(a)", """
def has_dup(a):
    s = set()
    for x in a:
        if x in s:
            return 1
        s.add(x)
    return 0
""", [[[1, 2, 3]], [[1, 2, 1]], [[]], [[7, 7]]], "Seen before?"),
  ORDER("Insert into a hash table", "Order the steps.", ["Compute the hash of the key", "Reduce it modulo the table size", "Find the bucket", "Handle any collision", "Store the key and value"]),
  MATCH("Hashing", "Match each term with its meaning.", [("Collision", "Two keys one bucket"), ("Chaining", "List per bucket"), ("Load factor", "Entries over buckets"), ("Hash set", "Keys only"), ("Probe", "Try another slot")]),
  FILL("Hashing", "A hash table finds keys in {{O(1)|constant}} time on average; two keys in one bucket form a {{collision}}.")]))

CHS.append(CH(
 "Trees and binary search trees",
 ("Trees", [
  "Tree | has | A root and children",
  "Binary tree | has | At most two children",
  "BST | orders | Left smaller right larger",
  "Traversal | visits | Every node",
  "Height | limits | Search time",
  "Balanced | keeps | Height log n",
  "Inorder | gives | Sorted order"]),
 ["A tree is a hierarchy: a root with children, each a root of its own subtree. A binary tree allows at most two children. A binary search tree keeps smaller keys on the left and larger on the right, so search, insertion and deletion follow one path.",
  "Traversals visit every node: preorder, inorder, postorder and level order. Inorder on a BST gives sorted order. Cost depends on height; balanced trees such as AVL and red-black trees keep the height logarithmic.",
  "The labs build a BST from an array of nodes, search it, compute heights and traverse."],
 [("Tree", "A connected graph with no cycles, rooted at one node."),
  ("Binary search tree", "A binary tree where left < node < right at every node."),
  ("Height", "The number of edges on the longest root-to-leaf path."),
  ("Traversal", "A systematic visit of all nodes."),
  ("Balanced tree", "A tree whose height stays O(log n)."),
  ("Leaf", "A node with no children.")],
 ["BST search, insert, delete: O(h), with h the height.",
  "Balanced: h = O(log n); degenerate (sorted inserts): h = n.",
  "Inorder (left, node, right) of a BST lists keys sorted.",
  "Preorder copies a tree; postorder deletes it bottom-up.",
  "Level order uses a queue.",
  "AVL and red-black trees rebalance with rotations."],
 [T("A family tree is a hierarchy: one ancestor at the top, children below, and each child can have children. Computer scientists draw the same shape for file systems, web pages and expressions. The top is the root, nodes without children are leaves, and the height counts the longest path down."),
  T("A binary search tree is a tree for fast searching. Every node has a key; everything in its left subtree is smaller, and everything in its right subtree is larger. To find a key, compare it with the node and go left or right, discarding half the tree each time, like binary search."),
  M(r"\text{search cost} = O(h), \qquad h \approx \log_2 n \text{ if balanced},\quad h = n \text{ if a chain}"),
  T("The cost depends on the height. If keys arrive in random order the tree is bushy and the height is about log of n. But inserting sorted keys makes a chain with height n, and search becomes linear. Self-balancing trees such as AVL and red-black trees fix this by rotating nodes after inserts and deletes, guaranteeing logarithmic height."),
  T("Traversals visit each node exactly once. Inorder goes left, node, right and prints a BST in sorted order. Preorder visits the node first and is used to copy a tree. Postorder visits children first and is used to delete one or evaluate an expression tree. Level order uses a queue and goes row by row."),
  T("Deleting from a BST has three cases. A leaf is removed outright. A node with one child is replaced by that child. A node with two children is replaced by its inorder successor, the smallest key in the right subtree, which keeps the ordering intact.")],
 [("Inorder traversal of a BST gives?", ["Sorted keys", "Reverse keys", "Random keys", "Levels"], 0, "Left, node, right."),
  ("Worst-case BST search?", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], 0, "A chain."),
  ("What fixes unbalanced trees?", ["Rotations", "Hashing", "Sorting", "Queues"], 0, "AVL and red-black."),
  ("Level order uses?", ["A queue", "A stack", "A heap", "Recursion only"], 0, "Row by row.")],
 [("Leaf?", "A node with no children."), ("Height of a single node?", "0 edges."), ("Successor use?", "Replaces a deleted node with two children."), ("Why balance?", "Keep search O(log n).")],
 [PL("BST search", "A BST is given as arrays key, left, right (child index or -1) with root 0. Write bst_has(key, left, right, t): 1 if t is in the tree else 0.",
     "bst_has(key, left, right, t)", """
def bst_has(key, left, right, t):
    cur = 0
    while cur != -1:
        if key[cur] == t:
            return 1
        cur = left[cur] if t < key[cur] else right[cur]
    return 0
""", [[[5, 3, 8], [1, -1, -1], [2, -1, -1], 8], [[5, 3, 8], [1, -1, -1], [2, -1, -1], 4], [[5], [-1], [-1], 5]], "Go left or right."),
  PL("Inorder traversal", "Write inorder(key, left, right): the keys by inorder traversal from root 0.",
     "inorder(key, left, right)", """
def inorder(key, left, right):
    out = []
    st = []
    cur = 0
    while cur != -1 or st:
        while cur != -1:
            st.append(cur)
            cur = left[cur]
        cur = st.pop()
        out.append(key[cur])
        cur = right[cur]
    return out
""", [[[5, 3, 8, 1], [1, 3, -1, -1], [2, -1, -1, -1]], [[5], [-1], [-1]], [[2, 1, 3], [1, -1, -1], [2, -1, -1]]], "Left, node, right."),
  PL("Tree height", "Write height(left, right): the height (edges on the longest root-to-leaf path) of the tree rooted at 0; a single node has height 0.",
     "height(left, right)", """
def height(left, right):
    best = 0
    st = [[0, 0]]
    while st:
        node, d = st.pop()
        if d > best:
            best = d
        if left[node] != -1:
            st.append([left[node], d + 1])
        if right[node] != -1:
            st.append([right[node], d + 1])
    return best
""", [[[1, -1, -1], [2, -1, -1]], [[-1], [-1]], [[1, 2, -1], [-1, -1, -1]]], "Track the depth."),
  PL("Build a BST by insertion", "Write build_inorder(keys): insert the distinct keys one by one into a BST (as nodes in arrays) and return the inorder keys, which must come out sorted.",
     "build_inorder(keys)", """
def build_inorder(keys):
    key = []
    left = []
    right = []
    for k in keys:
        key.append(k)
        left.append(-1)
        right.append(-1)
        i = len(key) - 1
        if i == 0:
            continue
        cur = 0
        while True:
            if k < key[cur]:
                if left[cur] == -1:
                    left[cur] = i
                    break
                cur = left[cur]
            else:
                if right[cur] == -1:
                    right[cur] = i
                    break
                cur = right[cur]
    out = []
    st = []
    cur = 0 if key else -1
    while cur != -1 or st:
        while cur != -1:
            st.append(cur)
            cur = left[cur]
        cur = st.pop()
        out.append(key[cur])
        cur = right[cur]
    return out
""", [[[5, 2, 8, 1, 9]], [[3, 2, 1]], [[1]], [[]]], "Insertion keeps the order."),
  ORDER("BST insert", "Order the steps.", ["Start at the root", "Compare the new key with the node", "Go left if smaller, right if larger", "Repeat until an empty child slot", "Attach the new node there"]),
  MATCH("Trees", "Match each traversal with its order.", [("Preorder", "Node, left, right"), ("Inorder", "Left, node, right"), ("Postorder", "Left, right, node"), ("Level order", "Row by row"), ("Height", "Longest path")]),
  FILL("BST", "In a BST the left subtree holds {{smaller}} keys; an {{inorder}} traversal lists keys sorted.")]))

CHS.append(CH(
 "Heaps and priority queues",
 ("Heaps", [
  "Priority queue | serves | The best item first",
  "Binary heap | is | A complete tree in an array",
  "Min-heap | keeps | Smallest on top",
  "Push | sifts | Up",
  "Pop | sifts | Down",
  "Heapify | builds | In O(n)",
  "Heap sort | sorts | In O(n log n)"]),
 ["A priority queue always serves the item with the highest priority next, like an emergency room. A binary heap implements it as a complete binary tree stored in an array where each parent is no larger than its children (a min-heap).",
  "Push adds at the end and sifts up; pop removes the top, moves the last item to the root and sifts down. Both take logarithmic time. Heapify builds a heap from n items in linear time, and heap sort uses it. Heaps power Dijkstra's algorithm and top-k queries.",
  "The labs implement push and pop, heapify, heap sort and a top-k selector."],
 [("Priority queue", "An abstract type with insert and extract-min (or max)."),
  ("Binary heap", "A complete binary tree with the heap property, stored in an array."),
  ("Heap property", "In a min-heap each parent is at most its children."),
  ("Sift up/down", "Swap an item with its parent or smaller child to restore order."),
  ("Heapify", "Turn an arbitrary array into a heap in O(n)."),
  ("Top-k", "Keep a heap of size k to find the k largest items.")],
 ["Array layout: parent of i is (i-1)//2; children are 2i+1 and 2i+2.",
  "Push and pop are O(log n); peek is O(1).",
  "Heapify is O(n); heap sort is O(n log n) and in place.",
  "A min-heap gives the smallest quickly, not full sorted order.",
  "Top-k of n items: O(n log k) with a size-k heap.",
  "Dijkstra and Huffman coding use heaps."],
 [T("In a hospital, the sickest patient is treated first, not the one who arrived first. A priority queue behaves like this: you may insert anything at any time, and the next item out is always the most urgent. A sorted list would do, but inserting into it costs linear time. A heap does both operations in logarithmic time."),
  T("A binary heap is a complete binary tree: every level is full except possibly the last, which fills from the left. That shape fits perfectly in an array. The root is at index zero. The children of node i sit at 2i plus 1 and 2i plus 2, and its parent at i minus 1 divided by two, rounded down."),
  M(r"\text{parent}(i) = \lfloor (i-1)/2 \rfloor, \qquad \text{children}(i) = 2i+1,\ 2i+2"),
  T("In a min-heap each parent is no larger than its children, so the smallest item is always at the root. To push, put the new item at the end and swap it with its parent while it is smaller. To pop, take the root, move the last item to the root and swap it downward with its smaller child until the order is restored. Each walk is at most the height, log n."),
  T("Building a heap from a whole array can be done in linear time: starting from the last parent, sift each node down. Heap sort builds a max-heap and repeatedly swaps the top into the sorted tail. Heaps also answer top-k questions: keep a small heap of the k best so far and replace its smallest when something better arrives.")],
 [("Where is the minimum in a min-heap?", ["At the root", "At the end", "In the middle", "Anywhere"], 0, "Heap property."),
  ("Push cost?", ["O(log n)", "O(1)", "O(n)", "O(n log n)"], 0, "Sift up."),
  ("Children of index i?", ["2i+1 and 2i+2", "i+1 and i+2", "i/2", "i*i"], 0, "Array layout."),
  ("Heapify cost?", ["O(n)", "O(n log n)", "O(1)", "O(n^2)"], 0, "Less than n pushes.")],
 [("Heap vs sorted array?", "Faster inserts."), ("Peek cost?", "O(1)."), ("Heap sort in place?", "Yes."), ("Top-k trick?", "Size-k heap.")],
 [PL("Push into a min-heap", "Write push(h, x): the list after pushing x into min-heap list h (sift up).",
     "push(h, x)", """
def push(h, x):
    h = list(h)
    h.append(x)
    i = len(h) - 1
    while i > 0:
        p = (i - 1) // 2
        if h[p] > h[i]:
            h[p], h[i] = h[i], h[p]
            i = p
        else:
            break
    return h
""", [[[1, 3, 5], 2], [[], 4], [[2, 3, 4], 1], [[1, 2], 9]], "Swap with a larger parent."),
  PL("Pop from a min-heap", "Write pop(h): return [smallest, rest-of-heap-list] after removing the root (sift down). h is non-empty.",
     "pop(h)", """
def pop(h):
    h = list(h)
    top = h[0]
    last = h.pop()
    if h:
        h[0] = last
        i = 0
        n = len(h)
        while True:
            l = 2 * i + 1
            r = 2 * i + 2
            s = i
            if l < n and h[l] < h[s]:
                s = l
            if r < n and h[r] < h[s]:
                s = r
            if s == i:
                break
            h[i], h[s] = h[s], h[i]
            i = s
    return [top, h]
""", [[[1, 3, 5, 4]], [[7]], [[1, 2, 3]]], "Swap with the smaller child."),
  PL("Heap sort", "Write heap_sort(a): the list sorted ascending using a min-heap (push all, pop all).",
     "heap_sort(a)", """
def heap_sort(a):
    h = []
    for x in a:
        h.append(x)
        i = len(h) - 1
        while i > 0 and h[(i - 1) // 2] > h[i]:
            p = (i - 1) // 2
            h[p], h[i] = h[i], h[p]
            i = p
    out = []
    while h:
        out.append(h[0])
        last = h.pop()
        if h:
            h[0] = last
            i = 0
            n = len(h)
            while True:
                l = 2 * i + 1
                r = 2 * i + 2
                s = i
                if l < n and h[l] < h[s]:
                    s = l
                if r < n and h[r] < h[s]:
                    s = r
                if s == i:
                    break
                h[i], h[s] = h[s], h[i]
                i = s
    return out
""", [[[5, 2, 9, 1]], [[1]], [[]], [[3, 3, 1]]], "Pop in order."),
  PL("Top k largest", "Write top_k(a, k): the k largest items in descending order, keeping a min-heap of size k (a simple list kept as a heap is fine).",
     "top_k(a, k)", """
def top_k(a, k):
    best = []
    for x in a:
        if len(best) < k:
            best.append(x)
        else:
            m = min(best)
            if x > m:
                best[best.index(m)] = x
    best.sort()
    best.reverse()
    return best
""", [[[5, 1, 9, 3, 7], 3], [[1, 2], 5], [[4, 4, 4], 2]], "Replace the smallest when beaten."),
  ORDER("Pop from a min-heap", "Order the steps.", ["Save the root as the answer", "Move the last item to the root", "Compare it with its children", "Swap with the smaller child if larger", "Repeat until the heap property holds"]),
  MATCH("Heaps", "Match each term with its meaning.", [("Priority queue", "Best item next"), ("Heap property", "Parent <= children"), ("Sift up", "Used by push"), ("Sift down", "Used by pop"), ("Heapify", "Build in O(n)")]),
  FILL("Heaps", "In a min-heap the {{smallest|minimum}} item is at the root; push and pop each take {{O(log n)|logarithmic}} time.")]))
