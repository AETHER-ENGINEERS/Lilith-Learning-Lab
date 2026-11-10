#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the GOFAI (symbolic AI) course. Usage: python3 make_gofai_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "gofai"))
import cmk, g1, g2, make_apps  # noqa: E402
make_apps.main()
CHS = g1.CHS + g2.CHS
PRONOUNCE = {"GOFAI": "go fie", "Haugeland": "how geh land", "McCarthy": "muh car thee", "Minsky": "min skee", "Newell": "new el", "Shannon": "shan un", "DENDRAL": "den dral", "MYCIN": "my sin",
    "STRIPS": "strips", "PDDL": "P D D L", "Prolog": "pro log", "Colmerauer": "col mer oh", "Kowalski": "ko val skee", "Searle": "serl", "Kasparov": "kas par off", "Cyc": "sike", "Lenat": "len at",
    "unification": "you nih fih kay shun", "unifier": "you nih fy er", "admissible": "ad miss ih bull", "heuristic": "hyoo ris tik", "heuristics": "hyoo ris tiks", "minimax": "min ih max",
    "A*": "A star", "SAT": "sat", "Horn": "horn", "Whitehead": "white head", "Principia": "prin kip ee uh", "Mathematica": "math uh mat ih kuh", "tautology": "taw tol oh jee", "ontology": "on tol oh jee",
    "ontologies": "on tol oh jees", "Wikidata": "wiki data", "brittleness": "brit ul ness"}
SANDBOX = cmk.terminal("GOFAI cheat sheet", "ai>", "A scripted lookup. Try: bfs, dfs, astar, minimax, resolution, strips, chaining", [
    ("bfs", ["Breadth-first: queue, shallowest first, fewest steps."]),
    ("dfs", ["Depth-first: stack, deepest first, little memory, not optimal."]),
    ("astar", ["A*: expand the lowest f = g + h; optimal if h is admissible."]),
    ("minimax", ["MAX takes the highest child value, MIN the lowest. Alpha-beta prunes without changing the result."]),
    ("resolution", ["From (A or X) and (not A or Y) derive (X or Y). The empty clause means contradiction."]),
    ("strips", ["Apply: new state = (state minus delete list) plus add list, if preconditions hold."]),
    ("chaining", ["Forward: facts to conclusions. Backward: goal to facts."]),
])
EXAM = [
 ("What does GOFAI stand for?", ["Good Old-Fashioned AI", "General Optimal Function AI", "Graph Oriented Fact AI", "Greatest Of Formal AI"], 0, "Haugeland, 1985."),
 ("When was the field named at Dartmouth?", ["1956", "1936", "1976", "1996"], 0, "Summer workshop."),
 ("What does the physical symbol system hypothesis claim?", ["Symbol manipulation is enough for intelligence", "Only brains think", "Neural nets are best", "Robots are needed"], 0, "Newell and Simon."),
 ("What does IS-A mean in a semantic network?", ["A category link", "A cause link", "A part link", "A time link"], 0, "Canary IS-A bird."),
 ("What is inheritance?", ["Properties passing from category to member", "A file copy", "A loop", "A search"], 0, "Saves repetition."),
 ("How many rows in a truth table with 3 variables?", ["8", "6", "9", "3"], 0, "2 to the 3."),
 ("What does resolution on (A or X) and (not A or Y) give?", ["X or Y", "A or Y", "not X", "X and Y"], 0, "Cancel A."),
 ("What does reaching the empty clause show?", ["The clauses are inconsistent", "They are satisfiable", "A tautology", "Nothing"], 0, "Contradiction."),
 ("What does unification do?", ["Finds a substitution making two terms identical", "Sorts a list", "Runs a program", "Draws a graph"], 0, "Pattern matching."),
 ("Can two different constants unify?", ["No", "Yes", "Only in Prolog", "Only if short"], 0, "A and B differ."),
 ("Which data structure does BFS use?", ["A queue", "A stack", "A heap only", "A tree only"], 0, "First in, first out."),
 ("Which search uses a stack?", ["Depth-first", "Breadth-first", "A*", "Uniform cost"], 0, "Last in, first out."),
 ("What does A* minimise when choosing the next state?", ["g + h", "g only", "h only", "depth only"], 0, "Cost plus estimate."),
 ("What does admissible mean?", ["Never overestimates", "Always exact", "Always zero", "Always large"], 0, "Keeps A* optimal."),
 ("What does MIN assume?", ["The opponent picks the lowest value for MAX", "The opponent plays randomly", "The opponent passes", "The opponent copies MAX"], 0, "Worst case."),
 ("What does alpha-beta change?", ["Speed, not the result", "The minimax value", "The rules", "The evaluation"], 0, "Same answer."),
 ("Who beat Kasparov in 1997?", ["Deep Blue", "AlphaGo", "ELIZA", "MYCIN"], 0, "IBM."),
 ("Which chaining starts from known facts?", ["Forward", "Backward", "Sideways", "Random"], 0, "Data-driven."),
 ("What was MYCIN used for?", ["Suggesting antibiotics", "Playing chess", "Translating", "Drawing"], 0, "An expert system."),
 ("What is a state in STRIPS?", ["A set of facts", "A number", "A sequence of actions", "A graph colour"], 0, "What is true now."),
 ("What is the frame problem?", ["Stating what does not change", "A graphics bug", "A search failure", "A proof rule"], 0, "McCarthy and Hayes."),
 ("What is a CSP?", ["Variables, domains and constraints", "A sorting algorithm", "A neural net", "A database"], 0, "A structured puzzle."),
 ("What does backtracking do on failure?", ["Undoes an earlier choice", "Stops the program", "Restarts from scratch", "Ignores the constraint"], 0, "Goes back."),
 ("How does Prolog answer a query?", ["Backward chaining with unification", "Forward chaining only", "Random guesses", "Sorting"], 0, "Depth-first."),
 ("What did Searle's Chinese Room argue?", ["Symbol shuffling alone is not understanding", "Computers can learn Chinese", "Rules are enough", "Translation is easy"], 0, "1980."),
 ("What does neuro-symbolic AI try to do?", ["Combine learning and reasoning", "Replace all computers", "Draw pictures", "Avoid data"], 0, "Best of both."),
]
CFG = dict(id="gofai-symbolic-ai", title="GOFAI: Symbolic AI",
    subtitle="Logic, search, rules and planning: how Good Old-Fashioned AI reasons, with runnable Python labs and a search visualiser",
    description="A hands-on course in symbolic AI, also called Good Old-Fashioned AI: its history, knowledge representation with networks and frames, propositional and predicate logic with resolution and unification, uninformed and heuristic search, game playing with minimax and alpha-beta, rule-based and expert systems, STRIPS planning and the frame problem, constraint satisfaction and Prolog, and the limits and legacy of the approach including neuro-symbolic AI. Every chapter has Python labs, and an interactive grid shows breadth-first, depth-first and A* search side by side.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="gofai", apps={"__SEARCH__": "search.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "gofai-symbolic-ai.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
