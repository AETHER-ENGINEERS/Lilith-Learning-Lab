"""Helpers for the compiler course. PL() runs the reference solution in CPython to fill in the expected results,
so every lab's expectation comes from running code. test_course.js then re-checks everything on MicroPython."""
import sys, os, json, copy, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "trinity"))
from tlib import T, C, M  # noqa: F401


def PL(title, intro, sig, solution, cases, hint, approx=None):
    """sig: 'name(a, b)'. solution: function source (dedented). cases: list of arg lists."""
    fn = sig.split("(")[0]
    sol = textwrap.dedent(solution).strip("\n") + "\n"
    ns = {}
    exec(sol, ns)
    tests = []
    for args in cases:
        out = ns[fn](*copy.deepcopy(args))
        out = json.loads(json.dumps(out))
        t = {"args": args, "expect": out}
        if approx:
            t["approx"] = approx
        tests.append(t)
    return {"type": "python", "title": title, "intro": intro, "fn": fn,
            "starter": "def %s:\n    # your code\n    pass\n" % sig,
            "tests": tests, "hint": hint, "solution": sol}


def MATCH(title, intro, pairs):
    return {"type": "match", "title": title, "intro": intro, "pairs": [list(p) for p in pairs]}


def FILL(title, text):
    return {"type": "fill", "title": title, "text": text}


def ORDER(title, intro, items):
    return {"type": "order", "title": title, "intro": intro, "items": items}


def CH(title, maps, summary, glossary, key, lesson, quiz, cards, practice):
    return {"title": title, "maps": [{"title": maps[0], "links": maps[1]}], "summary": summary,
            "glossary": [{"term": a, "def": b} for a, b in glossary], "keyPoints": key, "lesson": lesson,
            "quiz": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in quiz],
            "cards": [{"q": q, "a": a} for q, a in cards], "practice": practice}
