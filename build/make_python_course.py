#!/usr/bin/env python3
"""Build the Python tutorial course. Usage: python3 make_python_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "ptc"))
import cmk, pt1, pt2  # noqa: E402

PRONOUNCE = {
    "Python": "pie thon", "def": "def", "elif": "el if", "bool": "bool", "int": "int", "str": "stir", "len": "len", "init": "init", "__init__": "dunder init", "lambda": "lam duh", "yield": "yield",
    "json": "jay son", "JSON": "jason", "dumps": "dumps", "loads": "loads", "KeyError": "key error", "ValueError": "value error", "TypeError": "type error", "IndexError": "index error",
    "ZeroDivisionError": "zero division error", "enumerate": "in um er ate", "zip": "zip", "sqrt": "square root", "isinstance": "is instance", "datetime": "date time", "ELI5": "E L I five",
    "FizzBuzz": "fizz buzz", "Collatz": "kol lats", "Fibonacci": "fib uh nah chee", "Roman": "roman", "stdlib": "standard library", "API": "A P I", "None": "none", "True": "true", "False": "false",
    "args": "args", "kwargs": "kwargs", "sorted": "sorted", "ASCII": "ass kee", "PEP": "pep", "REPL": "rep ul", "IDE": "I D E", "Gerasimov": "gair uh sim off",
}

SANDBOX = cmk.terminal("Python cheat sheet", "py>", "A scripted lookup, not a real interpreter. Try: print, types, slice, if, for, list, dict, def, try, class", [
    ("print", ["print('hi', 3) shows: hi 3", "print(a, b, sep='-') changes the separator"]),
    ("types", ["int 5, float 2.5, str 'a', bool True, list [], dict {}, tuple (), set {1}", "type(x) tells you which"]),
    ("slice", ["s[1:4] is items 1 to 3", "s[::-1] reverses; s[-1] is the last"]),
    ("if", ["if c: ... elif c2: ... else: ...", "== compares, = assigns"]),
    ("for", ["for x in items: ...", "range(3) is 0, 1, 2"]),
    ("list", ["a.append(x), a.pop(), sorted(a), len(a)", "b = a[:] makes a copy"]),
    ("dict", ["d['k'] = 1; d.get('z', 0)", "for k, v in d.items()"]),
    ("def", ["def f(x, y=1): return x + y", "No return gives None"]),
    ("try", ["try: ... except ValueError: ... finally: ...", "raise ValueError('why')"]),
    ("class", ["class A: def __init__(self, x): self.x = x", "class B(A): inherits from A"]),
])

EXAM = [
 ("What does the = sign do?", ["Assigns a value to a name", "Compares", "Prints", "Ends"], 0, "Assignment."),
 ("What type is 3.0?", ["float", "int", "str", "bool"], 0, "It has a decimal point."),
 ("What does print do?", ["Shows values", "Reads files", "Defines a function", "Stops"], 0, "Output."),
 ("What does # start?", ["A comment", "A loop", "A string", "A class"], 0, "Ignored by Python."),
 ("What is 9 // 2?", ["4", "4.5", "5", "1"], 0, "Floor division."),
 ("What is 9 % 2?", ["1", "4", "0", "2"], 0, "Remainder."),
 ("What is 'abc'[1]?", ["b", "a", "c", "ab"], 0, "Index starts at 0."),
 ("What is 'hello'[1:3]?", ["el", "he", "ell", "hel"], 0, "Stop is excluded."),
 ("Can a string be changed in place?", ["No", "Yes", "Only digits", "Only once"], 0, "Immutable."),
 ("Which operator compares for equality?", ["==", "=", "!", "=>"], 0, "Two signs."),
 ("What marks a block in Python?", ["Indentation", "Braces", "Semicolons", "Brackets"], 0, "Four spaces."),
 ("Which is falsy?", ["An empty list", "The number 1", "Non-empty text", "True"], 0, "Empty things count as False."),
 ("What is range(4)?", ["0, 1, 2, 3", "1, 2, 3, 4", "0 to 4", "4"], 0, "Stops before 4."),
 ("What does break do?", ["Leaves the loop", "Skips one round", "Starts a loop", "Prints"], 0, "Immediately."),
 ("When use a while loop?", ["When waiting for a condition", "Never", "Only with lists", "Only with text"], 0, "Unknown count."),
 ("What does append do?", ["Adds to the end of a list", "Sorts", "Copies", "Deletes"], 0, "At the end."),
 ("What does b = a do for a list?", ["Makes another name for the same list", "Copies the list", "Sorts it", "Empties it"], 0, "Alias."),
 ("Can a tuple change?", ["No", "Yes", "Only numbers", "Only the last item"], 0, "Fixed."),
 ("What does d.get('k', 0) do?", ["Gives 0 if k is missing", "Raises an error", "Deletes k", "Adds k"], 0, "Safe lookup."),
 ("What does a set not allow?", ["Duplicates", "Numbers", "Text", "Loops"], 0, "Unique items."),
 ("What does def do?", ["Defines a function", "Defines a variable", "Imports", "Ends"], 0, "Starts a function."),
 ("What does a function without return give back?", ["None", "0", "An error", "Empty text"], 0, "None."),
 ("What does a recursive function need?", ["A base case", "A class", "A module", "A set"], 0, "To stop."),
 ("What does [n*n for n in nums] build?", ["A list of squares", "A number", "A set", "A function"], 0, "A comprehension."),
 ("What is lambda?", ["A small unnamed function", "A class", "A loop", "A module"], 0, "One line."),
 ("What does zip do?", ["Pairs items by position", "Compresses files", "Sorts", "Counts"], 0, "Parallel sequences."),
 ("What error is int('x')?", ["ValueError", "KeyError", "IndexError", "NameError"], 0, "Bad value."),
 ("When does finally run?", ["Always", "Only on error", "Never", "Only on success"], 0, "Cleanup."),
 ("Why name the error in except?", ["To avoid hiding bugs", "To be faster", "To be longer", "It is required"], 0, "Catch what you expect."),
 ("What is self in a method?", ["The object itself", "The class", "A module", "A keyword for loops"], 0, "First parameter."),
 ("What does __init__ do?", ["Sets up a new object", "Deletes it", "Prints it", "Copies it"], 0, "Constructor."),
 ("What does inheritance do?", ["Reuses a parent class", "Speeds up loops", "Imports a module", "Copies a list"], 0, "Child from parent."),
 ("What does import do?", ["Loads a module", "Deletes a file", "Prints", "Defines a class"], 0, "Makes names available."),
 ("What does yield do?", ["Gives a value and pauses a generator", "Ends the program", "Imports", "Raises an error"], 0, "Lazily."),
 ("What is an edge case?", ["An unusual input at the limit", "A typical input", "A bug fix", "A module"], 0, "Test them."),
 ("What is refactoring?", ["Cleaning working code", "Adding features", "Deleting tests", "Running code"], 0, "Same behaviour."),
 ("What is the best first version of a program?", ["The smallest working one", "The final one", "The fastest", "None"], 0, "Grow it."),
]

CFG = dict(id="python-tutorial", title="Python Tutorial: From First Line to Small Projects", subtitle="Learn Python by doing: values, loops, lists, functions, classes and more, with a lab in every chapter",
    description="A hands-on Python tutorial for beginners. You will learn variables and types, numbers and strings, decisions, loops, lists and tuples, dictionaries and sets, functions, comprehensions, errors, classes, modules and generators, then combine them in small projects. Every chapter has a short ELI5 block, a quiz and Python labs that run on the built-in interpreter, so you can practise without installing anything.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="ptc", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "python-tutorial.course.json")
    cmk.main(CFG, pt1.A + pt2.B, [sys.argv[0], out])
