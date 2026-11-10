"""Python tutorial, chapters 1-6."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

A = []

A.append(CH(
 "Hello, Python",
 ("Basics", ["Program | is | A list of instructions", "print | shows | Text on screen", "Variable | names | A value", "= | assigns | A name", "Comment | explains | Code", "Type | describes | A value", "Interpreter | runs | Your code"]),
 ["Python is a language for giving a computer instructions. You write lines, and the interpreter runs them top to bottom.",
  "A variable is a name for a value. The equals sign puts a value into a name.",
  "Every value has a type, such as int, float, str or bool."],
 [("Interpreter", "The program that reads and runs your Python code."), ("Variable", "A name that points to a value."), ("Type", "The kind of a value, like int or str."),
  ("print", "A function that shows values."), ("Comment", "Text after # that Python ignores."), ("Assignment", "Giving a name a value with =.")],
 ["Lines run from top to bottom.", "name = value creates or changes a variable.", "print(a, b) shows values separated by spaces.", "type(x) tells you the type.", "Names use letters, digits and underscores, and cannot start with a digit.", "A # starts a comment."],
 [T("A program is a recipe. The computer follows each line in order. Python reads easily, so many people start with it. You can try every example in the practice area of this course."),
  C("print('Hello, world!')\nname = 'Ada'\nage = 36\nprint(name, 'is', age)\nprint(type(name), type(age))", "python"),
  T("A variable is a label stuck on a box. The line age = 36 puts the number 36 in a box labelled age. Later lines can read the box or replace what is inside. Choose clear names, like total_price, so you can read your program later."),
  T("Python has a few basic types. An int is a whole number. A float has a decimal point. A str is text in quotes. A bool is True or False. The function type tells you which one a value is. Mixing them wrongly causes an error, which is Python's way of telling you something is off."),
  C("x = 5          # int\ny = 2.5        # float\nz = '5'        # str, not a number\nprint(x + y)   # 7.5\nprint(z + z)   # 55, text joined\nprint(x + z)   # TypeError", "python"),
  T("Errors are normal. Python prints the line and the kind of problem. Read the last line first. Fixing errors is a large part of programming, and each one teaches you something.")],
 [("What does = do?", ["Gives a name a value", "Compares two values", "Prints", "Ends a program"], 0, "Assignment."),
  ("What type is 2.5?", ["float", "int", "str", "bool"], 0, "It has a decimal point."),
  ("What does # start?", ["A comment", "A loop", "A function", "A string"], 0, "Python ignores it.")],
 [("What is a variable?", "A name for a value."), ("What does type() return?", "The type of a value."), ("What is a bool?", "True or False."), ("What runs your code?", "The interpreter.")],
 [MATCH("Types", "Match each value with its type.", [("42", "int"), ("3.14", "float"), ("'hello'", "str"), ("True", "bool")]),
  FILL("Variables", "Write {{name}} = 5 to make a variable, and use {{print}}(name) to show it."),
  PL("Greeting", "Write greet(name): return the text 'Hello, ' followed by name and an exclamation mark.", "greet(name)", """
def greet(name):
    return 'Hello, ' + name + '!'
""", [["Ada"], ["world"], [""]], "Join text with +.", approx=None),
  PL("Swap", "Write swap(a, b): return a list with the two values in the opposite order.", "swap(a, b)", """
def swap(a, b):
    return [b, a]
""", [[1, 2], ["x", "y"], [5, 5]], "Return [b, a].", approx=None)]))

A.append(CH(
 "Numbers and strings",
 ("Values", ["Number | supports | Arithmetic", "// | gives | Whole division", "% | gives | Remainder", "** | means | Power", "String | is | Text", "Index | picks | A character", "Slice | cuts | A part"]),
 ["Python does arithmetic with + - * / and more: // for whole division, % for the remainder and ** for powers.",
  "A string is text. You can join strings, repeat them, pick characters by index and cut pieces with slices.",
  "Strings have methods such as upper, split, replace and strip."],
 [("Floor division", "// divides and drops the fraction."), ("Modulo", "% gives the remainder after division."), ("Index", "A position in a string or list, starting at 0."),
  ("Slice", "A part cut out with s[start:stop]."), ("Method", "A function attached to a value, like s.upper()."), ("Immutable", "Cannot be changed in place; strings are immutable.")],
 ["7 // 2 is 3, 7 % 2 is 1, 2 ** 3 is 8.", "Dividing with / always gives a float.", "s[0] is the first character; s[-1] is the last.", "s[1:4] gives characters 1, 2 and 3.", "Strings never change; methods return new strings.", "round(x, 2) rounds to 2 decimals."],
 [T("Python is a fine calculator. Plus, minus, times and divide work as you expect. The slash gives a float, even for 6 / 3. Two slashes give a whole-number result. The percent sign gives the remainder, which is handy for questions like is this number even."),
  C("print(7 / 2)    # 3.5\nprint(7 // 2)   # 3\nprint(7 % 2)    # 1\nprint(2 ** 10)  # 1024\nprint(round(3.14159, 2))  # 3.14", "python"),
  T("A string is a row of characters. Counting starts at zero, so the first character is at index 0. Negative indexes count from the end. A slice takes a part. The start is included and the stop is not."),
  C("s = 'Python'\nprint(s[0], s[-1])   # P n\nprint(s[1:4])        # yth\nprint(s[:2], s[2:])  # Py thon\nprint(len(s))        # 6\nprint(s.upper())     # PYTHON", "python"),
  T("Strings come with many methods. Split breaks text into a list of words. Join puts a list back together. Replace swaps one piece for another. Strip removes spaces at the ends. Because strings cannot change, each method gives you a new string and leaves the old one alone."),
  C("words = 'a,b,c'.split(',')   # ['a', 'b', 'c']\nprint('-'.join(words))          # a-b-c\nprint('  hi  '.strip())         # hi\nprint('cat'.replace('c', 'b'))  # bat\nprint('Hello %s, you are %d' % ('Ada', 36))", "python")],
 [("What is 7 // 2?", ["3", "3.5", "4", "1"], 0, "Floor division."),
  ("What is 'Python'[1:3]?", ["yt", "Py", "yth", "ytho"], 0, "Start 1, stop 3 (not included)."),
  ("What is 10 % 3?", ["1", "3", "0", "3.33"], 0, "The remainder.")],
 [("What does // do?", "Whole-number division."), ("What does s[-1] give?", "The last character."), ("Can a string change in place?", "No."), ("What does split do?", "Breaks text into a list.")],
 [MATCH("Operators", "Match each expression with its result.", [("7 // 2", "3"), ("7 % 2", "1"), ("2 ** 3", "8"), ("7 / 2", "3.5")]),
  PL("Is it even?", "Write is_even(n): return True when n is even.", "is_even(n)", """
def is_even(n):
    return n % 2 == 0
""", [[4], [7], [0], [-2]], "Use the remainder.", approx=None),
  PL("Reverse text", "Write reverse(s): return s backwards.", "reverse(s)", """
def reverse(s):
    out = ''
    for ch in s:
        out = ch + out
    return out
""", [["abc"], [""], ["racecar"], ["Python"]], "Build the answer by adding each letter in front.", approx=None),
  PL("Initials", "Write initials(name): return the first letter of each word, upper case, joined together.", "initials(name)", """
def initials(name):
    out = ''
    for w in name.split():
        out += w[0].upper()
    return out
""", [["ada lovelace"], ["grace brewster hopper"], ["x"], [""]], "Split, take the first letter of each.", approx=None)]))

A.append(CH(
 "Making decisions",
 ("Decisions", ["Condition | is | True or False", "if | runs | A block", "elif | tries | Another case", "else | catches | The rest", "and or not | combine | Conditions", "Indent | marks | A block", "Comparison | gives | A bool"]),
 ["An if statement runs a block of code only when a condition is True. Add elif and else for other cases.",
  "Conditions come from comparisons like == != < > <= >=, joined with and, or and not.",
  "Indentation, four spaces, shows which lines belong to the block."],
 [("Condition", "An expression that is True or False."), ("Block", "Indented lines that belong to an if, loop or function."), ("elif", "Short for else if: another condition to try."),
  ("Truthy", "A value treated as True: non-zero numbers and non-empty things."), ("Falsy", "0, empty text, empty list and None count as False."), ("Ternary", "x if cond else y: a one-line choice.")],
 ["== compares; = assigns.", "Python checks if, then each elif, then else, and runs the first match only.", "and needs both True; or needs one; not flips.", "Chained comparisons work: 0 < x < 10.", "Empty values are falsy.", "Indent with four spaces and stay consistent."],
 [T("Programs make choices. The if statement asks a question, and the lines indented below it run only if the answer is True. Python uses the indent itself to know where a block starts and ends, so spacing matters."),
  C("age = 17\nif age >= 18:\n    print('adult')\nelif age >= 13:\n    print('teen')\nelse:\n    print('child')", "python"),
  T("A comparison gives True or False. Use == to ask if two values are equal. A single = would assign instead, which is a classic mistake. You can join conditions with and, or and not. Python lets you chain, so 0 < x < 10 means what it looks like."),
  T("Python also treats some values as True or False on their own. Zero, empty text, an empty list and None count as False. Everything else counts as True. That lets you write if items: to mean if the list has anything in it."),
  C("x = 7\nprint(0 < x < 10)          # True\nprint(x > 5 and x % 2 == 0) # False\nlabel = 'big' if x > 5 else 'small'\nprint(label)\nif []:\n    print('never')", "python")],
 [("Which checks equality?", ["==", "=", "!", "=>"], 0, "Two equals signs."),
  ("What marks a block?", ["Indentation", "Braces", "Semicolons", "Parentheses"], 0, "Four spaces."),
  ("Is an empty list truthy?", ["No", "Yes", "Only if None", "Error"], 0, "It counts as False.")],
 [("What does elif mean?", "Else, try another condition."), ("What does and need?", "Both True."), ("Is 0 truthy?", "No."), ("What does not do?", "Flips True and False.")],
 [FILL("Choices", "Use {{if}} to test, {{elif}} for another case and {{else}} for the rest."),
  PL("Grade", "Write grade(score): return 'A' for 90 or more, 'B' for 80 or more, 'C' for 70 or more, otherwise 'F'.", "grade(score)", """
def grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    return 'F'
""", [[95], [90], [85], [70], [10]], "Check from the highest.", approx=None),
  PL("Leap year", "Write leap(year): True if divisible by 4, except years divisible by 100 unless also divisible by 400.", "leap(year)", """
def leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
""", [[2024], [1900], [2000], [2023]], "Combine with and, or.", approx=None),
  PL("FizzBuzz one", "Write fizz(n): return 'FizzBuzz' if divisible by 3 and 5, 'Fizz' if by 3, 'Buzz' if by 5, otherwise the number as text.", "fizz(n)", """
def fizz(n):
    if n % 15 == 0:
        return 'FizzBuzz'
    if n % 3 == 0:
        return 'Fizz'
    if n % 5 == 0:
        return 'Buzz'
    return str(n)
""", [[15], [9], [10], [7]], "Test the combined case first.", approx=None)]))

A.append(CH(
 "Loops",
 ("Loops", ["for | walks | A sequence", "range | makes | Numbers", "while | repeats | Until False", "break | leaves | A loop", "continue | skips | One round", "Accumulator | collects | A result", "enumerate | adds | An index"]),
 ["A for loop repeats code for each item in a sequence. A while loop repeats as long as a condition is True.",
  "range(n) gives the numbers 0 to n minus 1. break leaves a loop early and continue skips to the next round.",
  "A common pattern is an accumulator: start with an empty total, then add to it in each round."],
 [("Loop", "Code that repeats."), ("Iterate", "To go through items one at a time."), ("range", "A sequence of numbers: range(start, stop, step)."),
  ("Accumulator", "A variable that builds up a result in a loop."), ("break", "Ends the loop right away."), ("Infinite loop", "A loop whose condition never becomes False.")],
 ["for x in items: runs once per item.", "range(5) is 0,1,2,3,4; range(2, 6) is 2,3,4,5; range(0, 10, 3) is 0,3,6,9.", "while cond: repeats; make sure something changes.", "break exits; continue jumps to the next round.", "enumerate(items) gives index and item.", "Loops can sit inside loops."],
 [T("Computers are good at repeating. A for loop takes each item of a sequence in turn and runs its block with that item. The word range makes a sequence of numbers, so you can repeat something a set number of times."),
  C("for i in range(3):\n    print('round', i)\n\ntotal = 0\nfor n in [4, 8, 15]:\n    total += n\nprint(total)   # 27", "python"),
  T("A while loop repeats as long as its condition holds. You must change something inside, or it never stops. Use break to leave early, for example when you find what you were looking for."),
  C("n = 27\nsteps = 0\nwhile n != 1:\n    n = n // 2 if n % 2 == 0 else 3 * n + 1\n    steps += 1\nprint(steps)   # 111\n\nfor i, ch in enumerate('abc'):\n    print(i, ch)", "python"),
  T("Loops can nest. A loop inside a loop runs its full set for each round of the outer one. That is how you build tables and grids. Pick the loop that matches the job: for when you know the items, while when you wait for a condition.")],
 [("What is range(3)?", ["0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "3"], 0, "Starts at 0, stops before 3."),
  ("What does break do?", ["Leaves the loop", "Skips one round", "Restarts", "Prints"], 0, "Immediately."),
  ("What does continue do?", ["Skips to the next round", "Stops the program", "Repeats the round", "Nothing"], 0, "Jumps ahead.")],
 [("When use while?", "When waiting for a condition."), ("What is an accumulator?", "A running result."), ("What does enumerate give?", "Index and item."), ("What is range(2, 5)?", "2, 3, 4.")],
 [MATCH("Ranges", "Match each range with its numbers.", [("range(3)", "0, 1, 2"), ("range(1, 4)", "1, 2, 3"), ("range(0, 10, 5)", "0, 5"), ("range(0)", "nothing")]),
  PL("Sum to n", "Write total(n): the sum of 1 to n using a loop.", "total(n)", """
def total(n):
    t = 0
    for i in range(1, n + 1):
        t += i
    return t
""", [[5], [1], [0], [100]], "Use an accumulator.", approx=None),
  PL("Count vowels", "Write vowels(s): how many of a, e, i, o, u appear in s, ignoring case.", "vowels(s)", """
def vowels(s):
    c = 0
    for ch in s.lower():
        if ch in 'aeiou':
            c += 1
    return c
""", [["Hello"], ["xyz"], ["AEIOU"], [""]], "Loop over the characters.", approx=None),
  PL("Collatz steps", "Write collatz(n): the number of steps to reach 1, where even n becomes n // 2 and odd n becomes 3n + 1.", "collatz(n)", """
def collatz(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps
""", [[1], [6], [27], [7]], "A while loop fits.", approx=None),
  PL("Triangle", "Write triangle(n): a list of n strings; row i (starting at 1) is i stars.", "triangle(n)", """
def triangle(n):
    rows = []
    for i in range(1, n + 1):
        rows.append('*' * i)
    return rows
""", [[3], [1], [0]], "Repeat a string with *.", approx=None)]))

A.append(CH(
 "Lists and tuples",
 ("Sequences", ["List | holds | Ordered items", "Tuple | is | A fixed list", "append | adds | An item", "Index | picks | One item", "Slice | copies | A part", "sort | orders | Items", "Mutable | means | Changeable"]),
 ["A list holds items in order and can change. Square brackets make one, and you reach items by index.",
  "Lists have methods: append, pop, insert, remove, sort and more. Slices copy parts.",
  "A tuple is like a list that cannot change. Use it for small fixed groups, like a point."],
 [("List", "An ordered, changeable collection."), ("Tuple", "An ordered, fixed collection in parentheses."), ("Mutable", "Can be changed after creation."),
  ("append", "Adds an item to the end of a list."), ("Unpacking", "Splitting a sequence into names: a, b = pair."), ("Alias", "Two names for the same list; changing one changes both.")],
 ["items = [3, 1, 2]; items[0] is 3.", "append adds, pop removes the last, insert and remove work by place and value.", "sorted(items) returns a new list; items.sort() changes in place.", "len, sum, min and max work on lists.", "b = a makes an alias; b = a[:] or list(a) makes a copy.", "Tuples: (1, 2); unpack with x, y = point."],
 [T("A list is a row of boxes, each with a position. Make one with square brackets. You can change items, add more and remove some. The same indexing and slicing rules as strings work here."),
  C("nums = [5, 3, 8]\nnums.append(1)      # [5, 3, 8, 1]\nnums[0] = 9         # [9, 3, 8, 1]\nprint(nums[1:3])    # [3, 8]\nprint(len(nums), sum(nums), max(nums))\nprint(sorted(nums)) # new sorted list", "python"),
  T("Beware of aliases. The line b = a does not copy the list. It gives the same list a second name, so a change through b shows up in a. To make a real copy, use a slice with nothing in it, or the list function."),
  C("a = [1, 2]\nb = a\nb.append(3)\nprint(a)      # [1, 2, 3]\nc = a[:]\nc.append(4)\nprint(a, c)   # [1, 2, 3] [1, 2, 3, 4]", "python"),
  T("A tuple is a list you promise not to change. It is written with parentheses and is good for things that belong together, like a point with x and y. You can unpack a tuple into separate names in one line. Functions often return tuples to give back several values at once."),
  C("point = (3, 4)\nx, y = point\nprint(x, y)\nfirst, *rest = [1, 2, 3]\nprint(first, rest)   # 1 [2, 3]\nnames = ['bo', 'al']\nnames.sort()\nprint(names)", "python")],
 [("What does append do?", ["Adds to the end", "Sorts", "Copies", "Removes the first"], 0, "At the end."),
  ("Can a tuple change?", ["No", "Yes", "Only numbers", "Only once"], 0, "It is fixed."),
  ("What does b = a do to a list?", ["Makes an alias", "Copies it", "Sorts it", "Deletes it"], 0, "Same list, two names.")],
 [("What is a tuple?", "A fixed sequence."), ("How to copy a list?", "a[:] or list(a)."), ("sorted vs sort?", "New list vs in place."), ("What does pop do?", "Removes the last item.")],
 [MATCH("List methods", "Match each call with its effect.", [("append(x)", "Add to the end"), ("pop()", "Remove the last"), ("sort()", "Order in place"), ("insert(0, x)", "Add at the front")]),
  PL("Largest two", "Write top_two(nums): return the two largest numbers, largest first, as a list. Assume at least two numbers.", "top_two(nums)", """
def top_two(nums):
    s = sorted(nums, reverse=True)
    return [s[0], s[1]]
""", [[[3, 9, 4, 7]], [[1, 2]], [[5, 5, 1]]], "Sort descending.", approx=None),
  PL("Remove duplicates", "Write unique(items): return the items without repeats, keeping first-seen order.", "unique(items)", """
def unique(items):
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out
""", [[[1, 2, 1, 3, 2]], [[]], [["a", "a"]]], "Check before you append.", approx=None),
  PL("Rotate", "Write rotate(items, k): move the first k items to the end.", "rotate(items, k)", """
def rotate(items, k):
    if not items:
        return []
    k = k % len(items)
    return items[k:] + items[:k]
""", [[[1, 2, 3, 4], 1], [[1, 2, 3], 3], [[], 2], [[1, 2, 3, 4, 5], 7]], "Two slices joined.", approx=None),
  PL("Running total", "Write running(nums): a list where each item is the sum of all numbers up to that point.", "running(nums)", """
def running(nums):
    out = []
    t = 0
    for n in nums:
        t += n
        out.append(t)
    return out
""", [[[1, 2, 3, 4]], [[]], [[5]], [[2, -1, 3]]], "Keep a total and append it.", approx=None)]))

A.append(CH(
 "Dictionaries and sets",
 ("Mappings", ["Dict | maps | Keys to values", "Key | finds | A value", "get | reads | Safely", "items | gives | Key and value", "Set | holds | Unique items", "Union | joins | Sets", "Counting | uses | A dict"]),
 ["A dictionary stores pairs: a key and its value. You look things up by key, and lookups are fast.",
  "Methods such as get, items, keys and values help you read a dict. Keys must be unchangeable, like text, numbers or tuples.",
  "A set holds unique items and supports union, intersection and difference."],
 [("Dictionary", "A collection of key and value pairs."), ("Key", "The label used to look a value up."), ("Set", "A collection with no duplicates and no order."),
  ("Union", "All items from both sets."), ("Intersection", "Items in both sets."), ("Hashable", "Unchangeable enough to be a key.")],
 ["d = {'a': 1}; d['a'] is 1; d['b'] = 2 adds.", "d.get('z', 0) gives 0 if missing; d['z'] would raise KeyError.", "for k, v in d.items() visits each pair.", "'a' in d tests for a key.", "Sets: {1, 2}; set(list) removes duplicates.", "a | b union, a & b intersection, a - b difference."],
 [T("A list finds things by position. A dictionary finds them by name. It is like a phone book: look up a name and get a number. Each key appears once, and each key has one value."),
  C("ages = {'ada': 36, 'bo': 25}\nages['cy'] = 41\nprint(ages['ada'])          # 36\nprint(ages.get('zed', 0))   # 0\nfor name, age in ages.items():\n    print(name, age)\nprint('bo' in ages)         # True", "python"),
  T("Counting is a classic use. Walk through the items, and for each one add one to its count in a dictionary. The get method with a default of zero makes this short, because a missing key counts as zero."),
  C("counts = {}\nfor ch in 'banana':\n    counts[ch] = counts.get(ch, 0) + 1\nprint(counts)   # {'b': 1, 'a': 3, 'n': 2}", "python"),
  T("A set is a bag of unique items. Adding something twice has no effect. Sets are fast at asking whether an item is in the bag, and they do the maths of overlap: union, intersection and difference. Use a set to remove duplicates, or to compare two groups."),
  C("a = {1, 2, 3}\nb = {3, 4}\nprint(a | b)   # {1, 2, 3, 4}\nprint(a & b)   # {3}\nprint(a - b)   # {1, 2}\nprint(set([1, 1, 2]))   # {1, 2}", "python")],
 [("How do you read a key safely?", ["d.get(key, default)", "d[key]", "d.read(key)", "key.d"], 0, "No error when missing."),
  ("What does a set not allow?", ["Duplicates", "Numbers", "Text", "Loops"], 0, "Items are unique."),
  ("What does a & b give?", ["Items in both", "All items", "Items only in a", "Nothing"], 0, "Intersection.")],
 [("What is a key?", "The label for a value."), ("What does items() give?", "Key and value pairs."), ("What is a set?", "Unique items."), ("What is d.get()?", "A safe lookup.")],
 [MATCH("Set operations", "Match the operator with the result for {1,2,3} and {3,4}.", [("a | b", "{1, 2, 3, 4}"), ("a & b", "{3}"), ("a - b", "{1, 2}"), ("b - a", "{4}")]),
  PL("Word count", "Write word_count(text): return a sorted list of [word, count] pairs for the lower-cased words in text.", "word_count(text)", """
def word_count(text):
    counts = {}
    for w in text.lower().split():
        counts[w] = counts.get(w, 0) + 1
    return sorted([[w, counts[w]] for w in counts])
""", [["the cat the dog"], ["A a"], [""]], "Count with a dict, then sort.", approx=None),
  PL("Invert", "Write invert(d): swap keys and values; return the pairs as a sorted list of [new_key, new_value]. Values are unique.", "invert(d)", """
def invert(d):
    return sorted([[d[k], k] for k in d])
""", [[{"a": 1, "b": 2}], [{}], [{"x": "y"}]], "Build pairs in reverse.", approx=None),
  PL("Common items", "Write common(a, b): the sorted list of items found in both lists, without repeats.", "common(a, b)", """
def common(a, b):
    return sorted(set(a) & set(b))
""", [[[1, 2, 3], [2, 3, 4]], [[1], [2]], [["x", "y", "x"], ["x"]]], "Use a set intersection.", approx=None),
  PL("Anagrams", "Write anagram(a, b): True if the two words use the same letters, ignoring case.", "anagram(a, b)", """
def anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())
""", [["listen", "silent"], ["abc", "abd"], ["Dusty", "study"], ["a", "aa"]], "Compare sorted letters.", approx=None)]))
