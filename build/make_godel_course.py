#!/usr/bin/env python3
"""Build the Goedel Machine course. Usage: python3 make_godel_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "gm"))
import g1, g2  # noqa: E402
from make_trinity_course import split_long, stack  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "gm", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {
    "Gödel": "gur dull", "Goedel": "gur dull", "Schmidhuber's": "shmid hoo ber's", "Schmidhuber": "shmid hoo ber",
    "Löbian": "lurb ian", "Löb's": "lurb's", "Löb": "lurb", "Hutter's": "hoot er's", "Hutter": "hoot er",
    "AIXI(t,l)": "eye ksee T L", "AIXI": "eye ksee", "Solomonoff": "sol o mon off", "Steunebrink": "stoy ne brink",
    "Yudkowsky": "yud kow ski", "Herreshoff": "herr es off", "Kolmogorov": "kol mo gor off", "Levin": "lev in",
    "IDSIA": "id see ah", "BIOPS": "bye ops", "OOPS": "oops", "HSEARCH": "H search", "switchprog": "switch prog",
    "switchbit": "switch bit", "Sleight": "slight", "Blum": "bloom", "Goldbach": "gold bahk", "expectimax": "expecti max",
    "Expectimax": "Expecti max", "Kt": "K T", "MIRI": "meer ee",
}

SANDBOX = {
    "type": "terminal", "title": "Gödel machine lookup", "prompt": "gm>",
    "intro": "A scripted lookup, not a real machine. Try: loop, parts, theorem, axioms, help",
    "chips": ["loop", "parts", "theorem", "axioms", "help"],
    "commands": [
        {"re": "^help$", "out": ["loop      the main cycle", "parts     the ingredients of the initial software", "theorem   the target theorem", "axioms    the six axiom groups"]},
        {"re": "^loop$", "out": ["run policy -> search for a proof -> prove target theorem -> switch to the new code -> continue"]},
        {"re": "^parts$", "out": ["initial policy, proof searcher, axiomatic description of the machine and its world"]},
        {"re": "^theorem$", "out": ["u(switchbit = 1) > u(switchbit = 0) at time t1", "switchbit 0 means continue as before, including future search"]},
        {"re": "^axioms$", "out": ["hardware, reward, environment, uncertainty, initial state, utility"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "err"}],
    "tasks": []
}

EXAM = [
    ('Who proposed the Gödel machine?', ['Kurt Gödel', 'Jürgen Schmidhuber', 'Marcus Hutter', 'Alan Turing'], 1, 'Schmidhuber first proposed it in 2003.'),
    ('A Gödel machine rewrites its code only when...', ['A timer fires', 'It has proved the rewrite raises expected utility', 'A user asks', 'It is bored'], 1, 'The proof is the gate.'),
    ('What does Gödel numbering allow?', ['Faster sorting', 'Formulas to be coded as numbers so a system can talk about itself', 'Encrypting proofs', 'Counting axioms'], 1, 'It makes self-reference possible.'),
    ('What must a Gödel machine do with improvements it cannot prove?', ['Apply them', 'Ignore them', 'Randomize them', 'Ask a human'], 1, 'Even with unlimited resources.'),
    ('Is the Gödel machine more powerful than a Turing machine?', ['Yes', 'No, its claim is about efficiency', 'Only with more memory', 'Only for proofs'], 1, 'It cannot overcome computability limits.'),
    ('Which variable holds environment input?', ['y', 'x', 'p', 'time'], 1, 'y holds outputs.'),
    ('What is utility in the paper?', ['Memory used', 'Expected sum of future rewards', 'Number of proofs', 'Program length'], 1, 'From the current time to the end of life.'),
    ('May the machine change its utility function?', ['Never', 'Only if the change is provably better under the present utility', 'Whenever', 'Only at the start'], 1, 'That blocks bogus goals.'),
    ('Which axioms describe how the state changes each cycle?', ['Utility axioms', 'Hardware axioms', 'Reward axioms', 'Uncertainty axioms'], 1, 'They model the hardware.'),
    ('What do the guarantees assume about the axiom system?', ['It is consistent', 'It is short', 'It is random', 'It is hidden'], 0, 'An inconsistent system proves anything.'),
    ('How many proof-modifying instructions are there?', ['Three', 'Six', 'Ten', 'One'], 1, 'get-axiom, apply-rule, delete-theorem, set-switchprog, check, state2theorem.'),
    ('Why is proof verification trivial?', ['Proofs are tiny', 'Only the six instructions can modify a proof, and each keeps it valid', 'Humans check', 'Proofs are random'], 1, 'No wrong theorem can be inserted.'),
    ('What is a proof technique?', ['An axiom', 'A program that outputs proofs', 'A theorem', 'A reward'], 1, 'The searcher tests such programs.'),
    ('What does the switchbit mean when it is 0?', ['Switch now', 'Continue as before, with the searcher still running', 'Halt', 'Reset'], 1, 'It is the continue option.'),
    ('What does the target theorem say?', ['The axioms are consistent', 'Switching has higher utility than continuing', 'The program halts', 'The proof is short'], 1, 'u with switchbit 1 exceeds u with switchbit 0.'),
    ('Why is the machine not greedy?', ['It never switches', 'Continuing includes better future rewrites, so it can decline an early improvement', 'It is random', 'It is slow'], 1, 'The comparison is with the best future.'),
    ('What does the relaxed target theorem change?', ['Removes the proof', 'Strictly higher becomes at least as high', 'Doubles the reward', 'Changes the hardware'], 1, 'It allows no-harm rewrites.'),
    ('In BIOPS phase i, a technique w gets how many steps?', ['P(w)', '2^i * P(w)', 'i', '1'], 1, 'If P(w) is at least 2^-i.'),
    ('What does Theorem 5.1 promise?', ['Constant-time proofs', 'A proof of t steps is found in O(t / P(w))', 'No proofs needed', 'Proofs always exist'], 1, 'Up to a constant, given the bias.'),
    ('What does bias-optimal mean?', ['Optimal for every prior', 'Optimal up to a constant given the prior over techniques', 'Biased toward errors', 'Random'], 1, 'The prior is the bias.'),
    ('Which example uses the Speed Prior?', ['Graph solver', 'Fuel robot', 'Sorting', 'Compiler'], 1, 'It is a weak environment assumption.'),
    ("What is Goldbach's conjecture?", ['Primes are infinite', 'Every even number above 2 is a sum of two primes', 'P equals NP', 'Every number is prime'], 1, 'It is unproven.'),
    ('What does AIXI combine?', ['Hashing and sorting', 'Solomonoff induction and expectimax', 'OOPS and SSA', 'Rice and Blum'], 1, "Hutter's agent is incomputable."),
    ('How does the Success-Story Algorithm judge a self-modification?', ['By proof', 'By whether the reward rate improved since it was made', 'By its length', 'By a vote'], 1, 'It is empirical.'),
    ('What does the Blum speed-up theorem imply?', ['All problems have a fastest program', 'Some problems have no optimal program', 'Proofs are short', 'P equals NP'], 1, 'Every program can be beaten.'),
    ("What does Löb's theorem restrict?", ['Memory', "A system's ability to assert that its own proofs are sound", 'Primes', 'Search speed'], 1, 'It gives the Löbian obstacle.'),
    ('What is the status of the Gödel machine?', ['Widely deployed', 'A theoretical design without a full implementation', 'Refuted', 'A product'], 1, 'Implementation studies exist.'),
    ('How should claims that humans are Gödel machines be treated?', ['As theorems', "As the author's speculation", 'As refuted', 'As axioms'], 1, 'They do not follow from the theorems.'),
]




def build():
    chapters = g1.CHS + g2.CHS
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__SWITCH__": app("switch.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "godel-machine",
        "title": "Gödel Machine",
        "subtitle": "Self-referential, provably optimal self-improvement",
        "author": "Lilith Learning Lab",
        "description": "A 12-chapter course on the Gödel machine, Jürgen Schmidhuber's 2003 design for a self-referential, self-improving problem solver that rewrites its own code only after proving the rewrite helps. Based on the Wikipedia article, Schmidhuber's technical report, the Steunebrink and Schmidhuber paper on implementation and the Yudkowsky and Herreshoff work on the Löbian obstacle. Covers Gödel's ideas, the machine model, the axioms, the proof searcher, the target theorem, global optimality, bias-optimal proof search, examples, related work and limits, with Python labs on the built-in MicroPython engine. It is a theoretical design with no full implementation; speculative claims are marked as the author's own.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: Gödel Machine", "passMark": 70, "size": 20,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "godel-machine.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
