"""Python tutorial, chapters 7-12."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

B = []

B.append(CH(
 "Functions",
 ("Functions", ["def | defines | A function", "Parameter | receives | A value", "return | sends back | A result", "Default | fills in | A missing argument", "Scope | limits | A name", "Docstring | describes | A function", "Recursion | calls | Itself"]),
 ["A function is a named block of code you can run again and again. def starts it, and return sends a value back.",
  "Parameters are names for the inputs. Default values make some inputs optional.",
  "Names made inside a function are local to it. A function can call itself, which is called recursion."],
 [("Function", "A named, reusable block of code."), ("Parameter", "A name for an input in the definition."), ("Argument", "The actual value passed in a call."),
  ("return", "Ends the function and gives back a value."), ("Scope", "Where a name can be seen."), ("Recursion", "A function that calls itself on a smaller problem.")],
 ["def name(params): then an indented body.", "A function without return gives back None.", "def f(x, y=10): y is optional.", "Call with names: f(1, y=2).", "Variables made inside are local.", "A recursive function needs a base case that stops it."],
 [T("When you notice you are writing the same lines twice, make a function. A function has a name, takes inputs and gives back a result. The def line defines it. Nothing runs until you call it."),
  C("def area(w, h=1):\n    \"\"\"Area of a rectangle.\"\"\"\n    return w * h\n\nprint(area(3, 4))    # 12\nprint(area(5))       # 5\nprint(area(h=2, w=6))# 12", "python"),
  T("Variables made inside a function live only there. This is called local scope. It keeps functions tidy, because they cannot damage each other's names by accident. Pass things in as parameters and send them back with return."),
  T("A function can call itself. This is recursion. It works when a problem contains a smaller copy of itself. You must give a base case, a simple input that returns right away, or the calls never end."),
  C("def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)\n\nprint(fact(5))   # 120\n\ndef total(items):\n    if not items:\n        return 0\n    return items[0] + total(items[1:])", "python"),
  T("Good functions do one thing, have a clear name and avoid surprises. A docstring, the text in triple quotes just under def, explains what the function does. Small functions are easy to test, and you can combine them into bigger programs.")],
 [("What does a function without return give back?", ["None", "0", "An error", "Empty text"], 0, "None."),
  ("What does a base case do?", ["Stops recursion", "Starts a loop", "Names a function", "Prints"], 0, "No more self-calls."),
  ("Where is a local variable visible?", ["Inside its function", "Everywhere", "In other files", "Never"], 0, "Local scope.")],
 [("What is a parameter?", "A name for an input."), ("What is recursion?", "A function calling itself."), ("What is a docstring?", "Text describing a function."), ("What does def do?", "Defines a function.")],
 [MATCH("Terms", "Match each term with its meaning.", [("Parameter", "A name in the definition"), ("Argument", "A value in the call"), ("return", "Gives back a result"), ("Default", "Used when no argument is given")]),
  PL("Factorial", "Write fact(n): n factorial using recursion (fact of 0 is 1).", "fact(n)", """
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)
""", [[0], [1], [5], [10]], "A base case, then n times fact(n - 1).", approx=None),
  PL("Fibonacci", "Write fib(n): the nth Fibonacci number where fib(0) is 0 and fib(1) is 1.", "fib(n)", """
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
""", [[0], [1], [2], [10], [20]], "Keep the last two numbers.", approx=None),
  PL("Power with default", "Write power(x, n=2): x raised to n without using **, using a loop.", "power(x, n=2)", """
def power(x, n=2):
    r = 1
    for _ in range(n):
        r *= x
    return r
""", [[3], [2, 10], [5, 0], [4, 3]], "Multiply n times.", approx=None),
  PL("Is prime", "Write is_prime(n): True when n is a prime number.", "is_prime(n)", """
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
""", [[1], [2], [9], [13], [97], [100]], "Try dividers up to the square root.", approx=None)]))

B.append(CH(
 "Comprehensions and functional tools",
 ("Comprehensions", ["Comprehension | builds | A list in one line", "Filter | keeps | Matching items", "Map | transforms | Each item", "lambda | is | A small function", "sorted key | orders | By a rule", "zip | pairs | Sequences", "any all | test | Many items"]),
 ["A list comprehension builds a list in one line: [x * 2 for x in nums if x > 0]. It reads like a sentence.",
  "lambda makes a tiny unnamed function. sorted, min and max accept a key function.",
  "zip pairs up sequences, and any and all test whole lists."],
 [("Comprehension", "A short way to build a list, dict or set from a loop."), ("lambda", "A small anonymous function."), ("key", "A function that tells sorted what to compare."),
  ("zip", "Pairs up items from several sequences."), ("any", "True if at least one item is True."), ("all", "True if every item is True.")],
 ["[expr for x in items if cond] makes a list.", "{k: v for ...} makes a dict; {x for ...} makes a set.", "lambda x: x * 2 is a function.", "sorted(items, key=len) sorts by length.", "zip(a, b) pairs items by position.", "any(...) and all(...) test conditions."],
 [T("Many loops just build a new list from an old one. A comprehension does that in one line. Read it from left to right: give me expr for each x in items, if cond. It is shorter and often clearer than a loop with append."),
  C("nums = [1, 2, 3, 4, 5, 6]\nsquares = [n * n for n in nums]\nevens = [n for n in nums if n % 2 == 0]\nlookup = {n: n * n for n in nums}\nprint(squares, evens)\nprint(lookup[3])   # 9", "python"),
  T("A lambda is a function with no name, written in one line. It is handy as a key for sorting. If you sort words by length, the key function tells sorted how to measure each word."),
  C("words = ['pear', 'fig', 'banana']\nprint(sorted(words, key=len))\nprint(sorted(words, key=lambda w: w[-1]))\nprint(max(words, key=len))\nnames = ['a', 'b']\nscores = [10, 20]\nprint(list(zip(names, scores)))", "python"),
  T("The functions any and all check a whole list at once. Any is True if one item passes. All is True only if every item passes. Together with a comprehension, they say a lot in a few words.")],
 [("What does [n*2 for n in nums] do?", ["Doubles each number", "Sums them", "Sorts them", "Prints them"], 0, "A new list."),
  ("What does all() need?", ["Every item True", "One item True", "No items", "Two items"], 0, "Not just one."),
  ("What is lambda?", ["A small unnamed function", "A loop", "A class", "A module"], 0, "Often used as a key.")],
 [("What does zip do?", "Pairs items by position."), ("What does key= do?", "Tells sorted how to compare."), ("What is any()?", "True if one item is True."), ("Can you make a dict with a comprehension?", "Yes.")],
 [MATCH("Tools", "Match each tool with its job.", [("sorted(x, key=len)", "Sort by length"), ("zip(a, b)", "Pair up items"), ("any(x)", "At least one is True"), ("[x for x in y]", "Build a new list")]),
  PL("Squares of evens", "Write even_squares(nums): the squares of the even numbers, in a list comprehension.", "even_squares(nums)", """
def even_squares(nums):
    return [n * n for n in nums if n % 2 == 0]
""", [[[1, 2, 3, 4]], [[]], [[7, 9]], [[6]]], "Filter then transform.", approx=None),
  PL("Longest word", "Write longest(words): the longest word; on a tie the first one. Return an empty string for no words.", "longest(words)", """
def longest(words):
    if not words:
        return ''
    return max(words, key=len)
""", [[["a", "bbb", "cc"]], [[]], [["ab", "cd"]]], "max accepts key=len.", approx=None),
  PL("Dot product", "Write dot(a, b): multiply matching items of two lists and add them up.", "dot(a, b)", """
def dot(a, b):
    return sum([x * y for x, y in zip(a, b)])
""", [[[1, 2, 3], [4, 5, 6]], [[], []], [[2], [5]]], "Combine zip with a comprehension.", approx=None),
  PL("Sort by last letter", "Write by_last(words): the words sorted by their last letter, ties kept in original order.", "by_last(words)", """
def by_last(words):
    return sorted(words, key=lambda w: w[-1])
""", [[["cab", "bad", "aaa"]], [[]], [["ab", "cb", "aa"]]], "sorted is stable.", approx=None)]))

B.append(CH(
 "Errors and exceptions",
 ("Errors", ["Exception | signals | A problem", "try | guards | Risky code", "except | handles | A named error", "raise | throws | An error", "finally | always | Runs", "Traceback | shows | Where it broke", "Validation | checks | Input"]),
 ["When something goes wrong Python raises an exception. If nothing handles it, the program stops and prints a traceback.",
  "try and except let you handle an error and carry on. raise lets your own code signal a problem.",
  "Catch the specific error you expect, not everything."],
 [("Exception", "An object that signals something went wrong."), ("Traceback", "The report of where the error happened."), ("try", "A block of code that may fail."),
  ("except", "A block that runs when a named error happens."), ("raise", "Starts an exception on purpose."), ("finally", "A block that always runs at the end.")],
 ["Common errors: ValueError, TypeError, KeyError, IndexError, ZeroDivisionError.", "try: ... except ValueError: ... handles one kind.", "except Exception as e: gives you the error object.", "raise ValueError('message') makes your own.", "finally runs whether or not an error happened.", "Read tracebacks from the bottom up."],
 [T("Errors happen: a file is missing, someone types text instead of a number, you divide by zero. Python stops with a message called a traceback. Read it from the bottom: the last line names the error, and the lines above show where."),
  C("def to_int(text):\n    try:\n        return int(text)\n    except ValueError:\n        return None\n\nprint(to_int('42'))    # 42\nprint(to_int('abc'))   # None\n\ntry:\n    print(1 / 0)\nexcept ZeroDivisionError:\n    print('cannot divide by zero')", "python"),
  T("Catch only what you expect. A bare except hides bugs, because it also swallows mistakes you did not plan for. Name the error type. The finally block runs no matter what, which is good for cleanup."),
  T("Your own code can raise errors too. If a function gets input that makes no sense, raise a ValueError with a clear message rather than returning a wrong answer quietly. Failing early and loudly makes bugs easier to find."),
  C("def sqrt_int(n):\n    if n < 0:\n        raise ValueError('negative number')\n    return int(n ** 0.5)\n\ntry:\n    sqrt_int(-4)\nexcept ValueError as e:\n    print('problem:', e)\nfinally:\n    print('done')", "python")],
 [("Which error is int('abc')?", ["ValueError", "KeyError", "IndexError", "SyntaxError"], 0, "Right type, wrong value."),
  ("When does finally run?", ["Always", "Only on errors", "Never", "Only if no error"], 0, "For cleanup."),
  ("What does raise do?", ["Throws an exception", "Catches one", "Ignores one", "Prints one"], 0, "You signal the problem.")],
 [("What is a traceback?", "The error report."), ("Why name the error in except?", "Avoid hiding bugs."), ("What does KeyError mean?", "A missing dict key."), ("What does raise do?", "Starts an exception.")],
 [MATCH("Errors", "Match each situation with its error.", [("int('x')", "ValueError"), ("[1][5]", "IndexError"), ("{}['a']", "KeyError"), ("1 / 0", "ZeroDivisionError")]),
  PL("Safe divide", "Write safe_div(a, b): a divided by b, or None when b is 0 (handle it with try and except).", "safe_div(a, b)", """
def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
""", [[6, 3], [1, 0], [0, 5], [7, 2]], "Catch ZeroDivisionError.", approx=None),
  PL("Parse numbers", "Write parse_all(items): a list with the integer value of each text item, using None where it is not a whole number.", "parse_all(items)", """
def parse_all(items):
    out = []
    for t in items:
        try:
            out.append(int(t))
        except ValueError:
            out.append(None)
    return out
""", [[["1", "x", "30"]], [[]], [["4.5", "7"]]], "try inside the loop.", approx=None),
  PL("Safe lookup", "Write lookup(d, key, default): the value for key, or default if missing, using try and except KeyError.", "lookup(d, key, default)", """
def lookup(d, key, default):
    try:
        return d[key]
    except KeyError:
        return default
""", [[{"a": 1}, "a", 0], [{"a": 1}, "b", 0], [{}, "x", "none"]], "KeyError for a missing key.", approx=None),
  PL("Validate age", "Write check_age(age): return 'ok' for a whole number from 0 to 150, otherwise 'invalid'. Catch a raised ValueError inside.", "check_age(age)", """
def check_age(age):
    try:
        if not isinstance(age, int) or age < 0 or age > 150:
            raise ValueError('bad')
        return 'ok'
    except ValueError:
        return 'invalid'
""", [[30], [-1], [200], [0], [150], ["x"]], "Raise and catch in one function.", approx=None)]))

B.append(CH(
 "Classes and objects",
 ("Classes", ["Class | is | A blueprint", "Object | is | An instance", "__init__ | sets up | An object", "self | is | The object itself", "Method | is | A function in a class", "Attribute | stores | Data", "Inheritance | reuses | A parent class"]),
 ["A class is a blueprint, and an object is one thing built from it. Objects bundle data (attributes) and behaviour (methods).",
  "The __init__ method sets up a new object. Every method takes self, the object it works on.",
  "A class can inherit from another to reuse and change its behaviour."],
 [("Class", "A blueprint for objects."), ("Object", "One instance made from a class."), ("Attribute", "A variable stored on an object."),
  ("Method", "A function defined inside a class."), ("self", "The object a method is working on."), ("Inheritance", "A class taking on the features of another.")],
 ["class Name: starts a class.", "def __init__(self, ...): runs when you create an object.", "self.x = x stores an attribute.", "obj.method() calls a method.", "class Dog(Animal): inherits from Animal.", "Methods can be overridden in the child class."],
 [T("So far you have used built-in types like lists and strings. A class lets you make your own. Think of a class as a cookie cutter and an object as a cookie. You describe once what a thing has and what it can do, and then make as many as you like."),
  C("class Counter:\n    def __init__(self, start=0):\n        self.value = start\n\n    def add(self, n=1):\n        self.value += n\n        return self.value\n\nc = Counter()\nc.add()\nc.add(5)\nprint(c.value)   # 6", "python"),
  T("The method named __init__ runs when you make a new object. The first parameter, self, is the object itself. Attributes you set on self stay with that object. Every method receives self first, so it can read and change the object's data."),
  T("Inheritance lets a new class start from an old one. The child class gets all the parent's attributes and methods and can change or add some. It models the idea that a dog is a kind of animal."),
  C("class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return self.name + ' makes a sound'\n\nclass Dog(Animal):\n    def speak(self):\n        return self.name + ' barks'\n\nfor a in [Animal('Generic'), Dog('Rex')]:\n    print(a.speak())", "python"),
  T("Use classes when data and the actions on it belong together, such as a bank account with a balance and deposit and withdraw. For simple jobs a function or a dict is often enough. Choose the simplest tool that keeps your program clear.")],
 [("What is self?", ["The object itself", "The class", "A module", "A string"], 0, "First parameter of methods."),
  ("What does __init__ do?", ["Sets up a new object", "Deletes it", "Prints it", "Copies it"], 0, "Runs on creation."),
  ("What does inheritance give?", ["Reuse of a parent class", "A faster loop", "A new module", "A copy of a list"], 0, "Child gets parent features.")],
 [("What is an object?", "An instance of a class."), ("What is a method?", "A function in a class."), ("What is an attribute?", "Data on an object."), ("What can a child class do?", "Override methods.")],
 [FILL("Classes", "Write {{class}} Dog: to start a class, and {{__init__}}(self, name) to set it up."),
  PL("Bank account", "Write account_run(start, actions): create an account with balance start. Each action is ['deposit', n] or ['withdraw', n]; a withdrawal larger than the balance is refused and changes nothing. Use a class inside. Return [final_balance, refused_count].", "account_run(start, actions)", """
def account_run(start, actions):
    class Account:
        def __init__(self, balance):
            self.balance = balance
            self.refused = 0

        def deposit(self, n):
            self.balance += n

        def withdraw(self, n):
            if n > self.balance:
                self.refused += 1
            else:
                self.balance -= n

    a = Account(start)
    for kind, n in actions:
        if kind == 'deposit':
            a.deposit(n)
        else:
            a.withdraw(n)
    return [a.balance, a.refused]
""", [[100, [["deposit", 50], ["withdraw", 30]]], [10, [["withdraw", 20], ["withdraw", 5]]], [0, []]], "A class with two methods and a counter.", approx=None),
  PL("Stack", "Write stack_run(ops): use a class with push and pop. Each op is ['push', x] or ['pop']; pop on an empty stack gives None. Return the list of values popped, in order.", "stack_run(ops)", """
def stack_run(ops):
    class Stack:
        def __init__(self):
            self.items = []

        def push(self, x):
            self.items.append(x)

        def pop(self):
            if not self.items:
                return None
            return self.items.pop()

    s = Stack()
    out = []
    for op in ops:
        if op[0] == 'push':
            s.push(op[1])
        else:
            out.append(s.pop())
    return out
""", [[[["push", 1], ["push", 2], ["pop"], ["pop"], ["pop"]]], [[]], [[["pop"]]]], "The last pushed comes out first.", approx=None),
  PL("Inheritance", "Write speak_all(kinds): kinds is a list of 'animal' or 'dog'. Make a base class Animal whose speak returns 'sound', and a Dog subclass whose speak returns 'woof'. Return the list of what each speaks.", "speak_all(kinds)", """
def speak_all(kinds):
    class Animal:
        def speak(self):
            return 'sound'

    class Dog(Animal):
        def speak(self):
            return 'woof'

    out = []
    for k in kinds:
        obj = Dog() if k == 'dog' else Animal()
        out.append(obj.speak())
    return out
""", [[["animal", "dog"]], [[]], [["dog", "dog"]]], "Override speak in the subclass.", approx=None)]))

B.append(CH(
 "Modules, iterators and generators",
 ("Modules", ["Module | is | A file of code", "import | loads | A module", "math | offers | Maths", "Iterator | gives | One item at a time", "Generator | uses | yield", "Lazy | means | On demand", "Standard library | comes | With Python"]),
 ["A module is a file of Python code you load with import. Python ships with a large standard library: math, random, json, datetime and more.",
  "An iterator hands out items one at a time. A generator is a function that uses yield to make one.",
  "Generators are lazy: they make each value only when asked, so they can be very long, even endless."],
 [("Module", "A file of code you can import."), ("import", "Loads a module so you can use it."), ("Standard library", "The modules that come with Python."),
  ("Iterator", "An object that gives items one at a time."), ("Generator", "A function that yields values lazily."), ("yield", "Gives a value and pauses the function.")],
 ["import math; math.sqrt(16) is 4.0.", "from math import pi imports one name.", "json.dumps and json.loads turn data to text and back.", "A for loop works on anything iterable.", "yield pauses a function and gives a value.", "next(gen) asks a generator for its next value."],
 [T("You do not have to write everything yourself. A module is a file of finished code. The import line loads it, and then you use its names with a dot. Python includes hundreds of modules in its standard library."),
  C("import math\nprint(math.sqrt(16), math.pi)\nfrom math import floor\nprint(floor(2.7))   # 2\nimport json\ntext = json.dumps({'a': [1, 2]})\nprint(text)\nprint(json.loads(text)['a'])", "python"),
  T("A for loop works on anything you can iterate over, and an iterator is the thing doing the handing out. A list holds all its items at once. A generator makes each item only when asked. That saves memory and can even describe an endless sequence."),
  C("def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor x in countdown(3):\n    print(x)        # 3 2 1\n\ngen = countdown(2)\nprint(next(gen), next(gen))", "python"),
  T("The keyword yield is like return that remembers its place. The function pauses at the yield, gives a value, and picks up from the same spot on the next request. Generator expressions look like comprehensions with round brackets, and work lazily too."),
  C("squares = (n * n for n in range(1000000))\nprint(next(squares), next(squares))\nprint(sum(n for n in range(10)))   # 45", "python")],
 [("What does import do?", ["Loads a module", "Deletes code", "Prints", "Runs a loop"], 0, "Makes its names available."),
  ("What does yield do?", ["Gives a value and pauses", "Ends the program", "Defines a class", "Imports"], 0, "Lazily."),
  ("What is lazy evaluation?", ["Making values only when needed", "Skipping errors", "Slow code", "Sorting"], 0, "On demand.")],
 [("What is the standard library?", "Modules shipped with Python."), ("What is a generator?", "A function that yields."), ("What does next() do?", "Gets the next value."), ("What is json for?", "Turning data into text.")],
 [MATCH("Modules", "Match each module with its use.", [("math", "Square roots and constants"), ("json", "Data as text"), ("random", "Random numbers"), ("datetime", "Dates and times")]),
  PL("Hypotenuse", "Write hyp(a, b): the length of the hypotenuse using math.sqrt, rounded to 3 decimals.", "hyp(a, b)", """
def hyp(a, b):
    import math
    return round(math.sqrt(a * a + b * b), 3)
""", [[3, 4], [1, 1], [5, 12], [0, 2]], "Pythagoras.", approx=1e-3),
  PL("Generator take", "Write first_squares(n): use a generator function that yields the squares 1, 4, 9, ... forever, and return the first n squares as a list.", "first_squares(n)", """
def first_squares(n):
    def squares():
        k = 1
        while True:
            yield k * k
            k += 1
    g = squares()
    return [next(g) for _ in range(n)]
""", [[0], [1], [5]], "An endless generator, take n values.", approx=None),
  PL("JSON round trip", "Write roundtrip(data): turn data into JSON text with json.dumps and return the text.", "roundtrip(data)", """
def roundtrip(data):
    import json
    return json.dumps(data)
""", [[{"a": [1, 2]}], [[1, 2, 3]], ["hi"], [{}]], "json.dumps does the work.", approx=None)]))

B.append(CH(
 "Putting it together",
 ("Projects", ["Problem | breaks into | Small functions", "Test | checks | A function", "Edge case | is | An unusual input", "Debug | finds | Mistakes", "Refactor | cleans | Working code", "Algorithm | is | A method", "Project | combines | Everything"]),
 ["Real programs split a problem into small functions, test each one, and combine them.",
  "Test normal inputs and edge cases such as empty input, one item or negative numbers. When something fails, print values or use a debugger to find out why.",
  "You now know enough Python to build small tools, and to keep learning from documentation."],
 [("Decomposition", "Splitting a problem into small parts."), ("Test", "A check that a function gives the expected result."), ("Edge case", "An unusual input at the limit of what is allowed."),
  ("Debugging", "Finding and fixing mistakes."), ("Refactoring", "Improving code without changing what it does."), ("Algorithm", "A step by step method for a task.")],
 ["Start with the smallest working version.", "Write a function for each idea.", "Test with simple, edge and large inputs.", "Print or log values to see what the code does.", "Read error messages carefully.", "Improve names and remove repetition only after it works."],
 [T("A big problem is easier when you cut it into small ones. To analyse a text file you might write one function to split it into words, one to count them and one to report the top results. Each piece is small enough to test alone."),
  C("def words(text):\n    return [w.strip('.,!?').lower() for w in text.split()]\n\ndef count(ws):\n    c = {}\n    for w in ws:\n        c[w] = c.get(w, 0) + 1\n    return c\n\ndef top(c, n):\n    return sorted(c.items(), key=lambda p: (-p[1], p[0]))[:n]\n\nprint(top(count(words('To be, or not to be.')), 2))", "python"),
  T("Test early and often. Try a normal case, an empty input, a single item and a surprising one. Many bugs hide at the edges. When a result looks wrong, print the values in the middle to see where it went off."),
  T("Do not worry about writing perfect code the first time. Make it work, then make it clear. Rename confusing variables, split long functions and remove repeated lines. Because you tested it, you can change it with confidence."),
  T("Where to go next? Read other people's code, build small tools for your own needs and use the Python documentation. Learn the libraries for your goals: data, web, games or automation. The best way to learn is to build something you care about.")],
 [("What should a test include?", ["Normal and edge cases", "Only easy cases", "Nothing", "Only large input"], 0, "Edges hide bugs."),
  ("What is refactoring?", ["Cleaning working code", "Adding bugs", "Deleting tests", "Running code"], 0, "Same behaviour, clearer code."),
  ("What first?", ["The smallest working version", "The final design", "The tests only", "Nothing"], 0, "Grow from something that works.")],
 [("What is decomposition?", "Splitting into parts."), ("What is an edge case?", "An unusual input."), ("How to debug?", "Print values and read errors."), ("What is an algorithm?", "A step by step method.")],
 [MATCH("Habits", "Match each habit with its benefit.", [("Small functions", "Easy to test"), ("Edge-case tests", "Find hidden bugs"), ("Printing values", "See what code does"), ("Refactoring", "Clearer code")]),
  PL("Top words", "Write top_words(text, n): lower-case the text, strip . , ! ? from words, count them, and return the n most common as [word, count] pairs, ordered by count (high first) then word.", "top_words(text, n)", """
def top_words(text, n):
    c = {}
    for w in text.split():
        w = w.strip('.,!?').lower()
        if w:
            c[w] = c.get(w, 0) + 1
    pairs = sorted(c.items(), key=lambda p: (-p[1], p[0]))
    return [[w, k] for w, k in pairs[:n]]
""", [["To be, or not to be.", 2], ["a b a", 5], ["", 3]], "Count, then sort with a two-part key.", approx=None),
  PL("Palindrome", "Write is_pal(s): True if s reads the same backwards, ignoring case, spaces and punctuation.", "is_pal(s)", """
def is_pal(s):
    t = ''
    for ch in s.lower():
        if ch.isalpha() or ch.isdigit():
            t += ch
    r = ''
    for ch in t:
        r = ch + r
    return t == r
""", [["A man, a plan, a canal: Panama"], ["hello"], [""], ["Was it a car or a cat I saw?"]], "Keep letters and digits only.", approx=None),
  PL("Binary search", "Write bsearch(items, target): items is sorted. Return the index of target, or -1. Use binary search, not a scan.", "bsearch(items, target)", """
def bsearch(items, target):
    lo = 0
    hi = len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
""", [[[1, 3, 5, 7, 9], 7], [[1, 3, 5], 4], [[], 1], [[2], 2]], "Halve the range each time.", approx=None),
  PL("Roman numerals", "Write roman(n): the Roman numeral for n from 1 to 3999.", "roman(n)", """
def roman(n):
    table = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'], [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']]
    out = ''
    for v, s in table:
        while n >= v:
            out += s
            n -= v
    return out
""", [[1], [4], [9], [58], [1994], [3999]], "Take the biggest value that fits, over and over.", approx=None)]))
