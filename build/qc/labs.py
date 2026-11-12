# -*- coding: utf-8 -*-
"""Quantum Web Lab configurations for the quantum computing course (one lab per chapter, levels as JSON)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "vendor", "quantum-web-lab"))
import build as qwl  # noqa: E402  (the vendored quantum-web-lab build.py)


def P(state, **kw):
    d = {"state": state}
    d.update(kw)
    return d


def LV(title, intro, start, goal, solution, hint="", after="", code=None):
    d = {"title": title, "intro": intro, "start": start, "goal": goal, "solution": solution, "hint": hint, "after": after}
    if not code and goal.get("via") == "text":
        code = solution
    if code:
        d["solutionCode"] = code
    return d


def lab(title, intro, cfg, python=False, height=1150):
    cfg = dict(cfg)
    cfg.setdefault("python", python)
    if not python:
        cfg["code"] = [c for c in cfg.get("code", ["qasm", "text", "ascii"]) if c != "python"]
    return {"type": "webxdc", "title": title, "intro": intro, "height": height, "html": qwl.build_html(cfg, python=python, title=title)}


GATE_BASIC = ["h", "x", "y", "z", "s", "t", "cx", "cz", "swap", "ccx", "rx", "ry", "rz", "p", "measure"]
CODE_ALL = ["python", "qasm", "text", "ascii"]
BLANK6 = "I-I-I-I-I-I"
BLANK3x5 = "I-I-I-I-I\nI-I-I-I-I\nI-I-I-I-I"

LABS = {}

LABS["bits"] = lab("Coins and bits", "Flip a bit, make a fair coin, then make two coins. Watch how many chances appear.", {
    "qubits": 1, "steps": 4, "maxQubits": 2, "palette": ["h", "x"], "results": ["chances", "shots"], "code": ["text", "ascii"], "console": False,
    "levels": [
        LV("Flip the bit", "Every qubit starts as 0. Use a gate so the result is 1 with certainty.", "I-I-I-I", {"probs": [P("1", min=0.99)]}, "X-I-I-I", "The X gate is a NOT.", "X swaps 0 and 1."),
        LV("A fair coin", "Make a perfect 50/50 coin: half the time 0, half the time 1.", "I-I-I-I", {"probs": [P("0", approx=0.5)]}, "H-I-I-I", "The H gate makes a blend.", "That is superposition."),
        LV("Two fair coins", "Now there are two qubits. Make both of them fair coins, so all four answers (00, 01, 10, 11) are equally likely.", "I-I-I-I\nI-I-I-I", {"probs": [P("00", approx=0.25), P("11", approx=0.25), P("01", approx=0.25), P("10", approx=0.25)]}, "H-I-I-I\nH-I-I-I", "Put an H on each wire. Use the + button for a second qubit if needed.", "Two qubits give four chances. Each extra qubit doubles them.")]})

LABS["qubit"] = lab("Qubit playground", "Make chances, then open Inspect to see amplitudes and phase.", {
    "qubits": 1, "steps": 5, "maxQubits": 2, "palette": ["x", "h", "z", "ry"], "results": ["chances", "inspect", "shots"], "code": CODE_ALL, "console": True, "chips": ["h 0", "x 0", "ry pi/3 0", "run", "shots 20", "undo", "help"],
    "levels": [
        LV("Make a 1", "Start from 0. Make the chance of 1 equal to 100%.", "I-I-I-I-I", {"probs": [P("1", min=0.99)]}, "X-I-I-I-I", "X flips a plain 0 into a plain 1."),
        LV("A fair blend", "Make the chances 50% and 50%. Then open Inspect: both amplitudes are about 0.707.", "I-I-I-I-I", {"probs": [P("0", approx=0.5)]}, "H-I-I-I-I", "H makes an even blend."),
        LV("A weighted coin", "Make 0 come up about 85% of the time. The RY gate turns the amplitudes by any angle. Try an angle near 0.8.", "I-I-I-I-I", {"probs": [P("0", approx=0.85, tol=0.03)], "gates": {"require": ["ry"]}}, "RY(0.8)-I-I-I-I", "Pick RY, type 0.8 in the angle box (radians), tap a square.", "A small turn gives an uneven coin."),
        LV("Same chances, different phase", "Make a 50/50 coin that has a negative amplitude: use H and then Z. In Inspect, the phase dial of |1> points the other way.", "I-I-I-I-I", {"probs": [P("0", approx=0.5)], "gates": {"require": ["h", "z"]}}, "H-Z-I-I-I", "H first, then Z.", "The chances did not change, but the sign did.")]}, python=True)

LABS["gates"] = lab("Gate puzzles", "Solve the levels by tapping gates into the circuit.", {
    "qubits": 1, "steps": 6, "maxQubits": 1, "palette": ["h", "x", "y", "z", "t"], "results": ["chances", "inspect", "shots"], "code": CODE_ALL,
    "levels": [
        LV("Flip the bit", "Every qubit starts as 0. Add a gate so the result is 1 with certainty.", BLANK6, {"probs": [P("1", min=0.99)]}, "X-I-I-I-I-I", "The X gate is the quantum NOT.", "X swaps 0 and 1."),
        LV("Coin flip", "Make a perfect 50/50 coin.", BLANK6, {"probs": [P("0", approx=0.5)]}, "H-I-I-I-I-I", "The H gate is called Hadamard.", "That is superposition."),
        LV("Undo the coin flip", "This circuit starts with an H. Add more gates so the qubit ends as 0 with certainty, keeping the H.", "H-I-I-I-I-I", {"probs": [P("0", min=0.99)], "gates": {"min": 2, "require": ["h"]}}, "H-H-I-I-I-I", "Gates can be their own undo button.", "H is its own inverse."),
        LV("Interference", "Using only H and Z, make the result 1 with certainty. Z does not change chances by itself, so think about what happens between two H gates.", BLANK6, {"probs": [P("1", min=0.99)], "gates": {"only": ["h", "z"], "count": {"h": {"min": 2}}}}, "H-Z-H-I-I-I", "Put a Z between two H gates.", "The two paths cancel for 0 and add up for 1."),
        LV("A weighted coin", "Using only H and T, make 0 come up about 85% of the time.", BLANK6, {"probs": [P("0", approx=0.85, tol=0.05)], "gates": {"only": ["h", "t"]}}, "H-T-H-I-I-I", "A small phase between two H gates tilts the coin.", "A small phase gives a biased coin."),
        LV("Build a Z from T gates", "Using only H and T gates, end as 1 with certainty. Four T gates in a row add up to a half turn of phase.", BLANK6, {"probs": [P("1", min=0.99)], "gates": {"only": ["h", "t"], "count": {"t": {"min": 2}}}}, "H-T-T-T-T-H", "H, then four T gates, then H.", "Four T gates make one Z.")]}, python=True)

LABS["interference"] = lab("Interference lab", "Steer the chances with phase. Use Inspect to watch the phase dials.", {
    "qubits": 1, "steps": 6, "maxQubits": 1, "palette": ["h", "z", "s", "t", "rz"], "results": ["chances", "inspect"], "code": ["text", "qasm", "ascii"],
    "levels": [
        LV("Cancel it", "This circuit starts with an H. Add a second H so the qubit returns to 0.", "H-I-I-I-I-I", {"probs": [P("0", min=0.99)], "gates": {"count": {"h": {"min": 2}}}}, "H-H-I-I-I-I", "Two H gates cancel.", "The two paths to 1 cancel."),
        LV("Flip with a sign", "Make the result 1 using only H and Z.", BLANK6, {"probs": [P("1", min=0.99)], "gates": {"only": ["h", "z"], "count": {"h": {"min": 2}}}}, "H-Z-H-I-I-I", "H, Z, H.", "A sign flip turned cancel into add."),
        LV("Two S gates", "Using only H and S gates make the result 1. Each S is a quarter turn of phase.", BLANK6, {"probs": [P("1", min=0.99)], "gates": {"only": ["h", "s"], "count": {"s": {"min": 2}}}}, "H-S-S-H-I-I", "Two S gates make one Z.", "S then S is a Z."),
        LV("A 25% coin", "Using H, RZ and H, make the chance of 1 about 25%. The chance is sin squared of half the angle. Try pi/3.", BLANK6, {"probs": [P("1", approx=0.25, tol=0.02)], "gates": {"require": ["rz"], "count": {"h": {"min": 2}}}}, "H-RZ(pi/3)-H-I-I-I", "Pick RZ, choose an angle, put it between two H gates.", "An angle between two H gates sets any chance you like.")]})

LABS["circuits"] = lab("Circuit text lab", "Type circuits as text. Open the Code box, pick Q text, edit, and press Apply.", {
    "qubits": 2, "steps": 4, "maxQubits": 3, "palette": GATE_BASIC, "results": ["chances"], "code": CODE_ALL, "codeOpen": True, "codeTab": "text", "console": True,
    "levels": [
        LV("Type a Bell pair", "In the Q text tab, type the two rows H-X#0 and I-X#1, then press Apply.", "I-I-I\nI-I-I", {"probs": [P("00", approx=0.5), P("11", approx=0.5)], "via": "text"}, "H-X#0-I\nI-X#1-I", "Row 1 is qubit 0, row 2 is qubit 1. Put each row on its own line.", "Rows are qubits and dashes separate the steps."),
        LV("Make 10", "Type a circuit where the result is always 10. Qubit 0 is on the left.", "I-I\nI-I", {"probs": [P("10", min=0.99)], "via": "text"}, "X-I\nI-I", "Only the first row needs a gate.", "The left digit is qubit 0."),
        LV("Three in a row", "Type a three qubit circuit that gives 000 or 111, half each.", "I-I-I\nI-I-I\nI-I-I", {"probs": [P("000", approx=0.5), P("111", approx=0.5)], "via": "text"}, "H-X#0-I\nI-X#1-X#0\nI-I-X#1", "H, then two CNOTs in a chain.", "That is the GHZ state.")]}, python=True)

LABS["twoq"] = lab("Two-qubit lab", "Link two qubits with CNOT and SWAP.", {
    "qubits": 2, "steps": 4, "maxQubits": 3, "palette": ["x", "h", "cx", "cz", "swap"], "results": ["chances", "inspect"], "code": ["qasm", "text", "ascii"],
    "levels": [
        LV("Copy a bit", "Qubit 0 starts as 1. Use a CNOT so both qubits end as 1.", "X-I-I-I\nI-I-I-I", {"probs": [P("11", min=0.99)], "gates": {"require": ["cx"]}}, "X-X#0-I-I\nI-X#1-I-I", "Pick CNOT: tap the control (qubit 0), then the target (qubit 1) in the same step.", "CNOT copies a classical bit."),
        LV("Control is off", "Add a CNOT (control qubit 0, target qubit 1) that does nothing because the control is 0.", "I-I-I-I\nI-I-I-I", {"probs": [P("00", min=0.99)], "linked": True}, "I-X#0-I-I\nI-X#1-I-I", "Do not flip qubit 0 first.", "A CNOT only acts when the control is 1."),
        LV("Swap them", "Qubit 0 starts as 1. Move the 1 to qubit 1 with a SWAP.", "X-I-I-I\nI-I-I-I", {"probs": [P("01", min=0.99)], "gates": {"require": ["swap"]}}, "X-SWAP#0-I-I\nI-SWAP#1-I-I", "Pick SWAP and tap both qubits in the same step.", "SWAP exchanges two qubits.")]})

LABS["entangle"] = lab("Entanglement lab", "Make entangled pairs and open Inspect: a shared qubit has a short Bloch arrow.", {
    "qubits": 3, "steps": 5, "maxQubits": 3, "palette": ["h", "x", "cx", "cz"], "results": ["chances", "inspect", "shots"], "code": CODE_ALL, "chips": ["new 3", "h 0", "cx 0 1", "cx 1 2", "explain", "undo", "help"],
    "levels": [
        LV("Copy a bit", "Qubit 0 starts as 1. Use a CNOT so the first two qubits both end as 1, giving 110.", "X-I-I-I-I\nI-I-I-I-I\nI-I-I-I-I", {"probs": [P("110", min=0.99)], "linked": True}, "X-X#0-I-I-I\nI-X#1-I-I-I\nI-I-I-I-I", "CNOT with control qubit 0 and target qubit 1.", "CNOT copies a classical bit."),
        LV("Make a Bell pair", "Make qubits 0 and 1 entangled so you only ever see 000 or 110, half each.", BLANK3x5, {"probs": [P("000", approx=0.5), P("110", approx=0.5)], "linked": True}, "H-X#0-I-I-I\nI-X#1-I-I-I\nI-I-I-I-I", "H on qubit 0, then a CNOT from qubit 0 to qubit 1.", "They always agree, yet each alone is random."),
        LV("Opposite pair", "Make qubits 0 and 1 always disagree: half the time 010, half the time 100.", BLANK3x5, {"probs": [P("010", approx=0.5), P("100", approx=0.5)]}, "H-X#0-I-I-I\nX-X#1-I-I-I\nI-I-I-I-I", "Start from the Bell pair and flip qubit 1 before the CNOT.", "A different Bell state."),
        LV("Three-way entanglement", "Make all three qubits agree: half the time 000, half the time 111 (the GHZ state).", BLANK3x5, {"probs": [P("000", approx=0.5), P("111", approx=0.5)]}, "H-X#0-I-I-I\nI-X#1-X#0-I-I\nI-I-X#1-I-I", "After H on qubit 0, chain two CNOTs.", "Entanglement can span many qubits.")]}, python=True)

LABS["algo"] = lab("Algorithm lab", "Deutsch and Grover circuits to explore.", {
    "qubits": 2, "steps": 9, "maxQubits": 2, "maxSteps": 12, "palette": ["h", "x", "z", "cx", "cz"], "results": ["chances", "inspect"], "code": CODE_ALL, "chips": ["new 2", "h 0", "h 1", "cz 0 1", "run", "undo", "help"],
    "levels": [
        LV("Deutsch: a constant oracle", "Qubit 0 ends as 1 when the hidden function is balanced and 0 when it is constant. Step 3 holds the oracle, right now a CNOT (balanced). Remove it, so the function is constant.", "I-H-X#0-H\nX-H-X#1-I", {"probs": [P("0", min=0.99)], "linked": False}, "I-H-I-H\nX-H-I-I", "Take both halves of the CNOT out of the third step.", "A constant function leaves qubit 0 at 0."),
        LV("Deutsch: a balanced oracle", "Put the CNOT back in the oracle step (control qubit 0, target qubit 1). That is the balanced function f(x) = x. Qubit 0 should end as 1.", "I-H-I-H\nX-H-I-I", {"probs": [P("1", min=0.99)], "linked": True}, "I-H-X#0-H\nX-H-X#1-I", "Third step: a CNOT from qubit 0 to qubit 1.", "Balanced gives 1. One question told us which kind it is."),
        LV("Grover: find 11", "Search four items for the marked one, 11. H on both, mark 11 with a controlled-Z, then reflect: H, X on both, controlled-Z, X on both, H.", "H-I-I-I-I-I-I-I-I\nH-I-I-I-I-I-I-I-I", {"probs": [P("11", min=0.99)]}, "H-Z#0-H-X-Z#0-X-H-I-I\nH-Z#1-H-X-Z#1-X-H-I-I", "Pick CZ and tap both qubits in the same step.", "Amplitude was moved onto the marked item."),
        LV("Grover: find 01", "Now the marked item is 01. Flip qubit 0 with X before and after the marking controlled-Z, then use the same reflection.", "H-I-I-I-I-I-I-I-I\nH-I-I-I-I-I-I-I-I", {"probs": [P("01", min=0.99)]}, "H-X-Z#0-X-H-X-Z#0-X-H\nH-I-Z#1-I-H-X-Z#1-X-H", "The oracle is X on qubit 0, controlled-Z, X on qubit 0.", "Any single item among 4 is found in one round.")]}, python=True)

LABS["noise"] = lab("Shots lab", "A Bell pair. Run shots with different seeds and watch the counts wobble around 50 and 50.", {
    "qubits": 2, "steps": 4, "maxQubits": 2, "palette": ["h", "x", "cx"], "start": "H-X#0-I-I\nI-X#1-I-I", "results": ["shots", "chances"], "resultsTab": "shots", "code": ["qasm", "ascii"], "complete": "shots", "chips": ["shots 20", "shots 1000", "run", "help"]})

LABS["qiskit"] = lab("Qiskit lab", "Build circuits in the Python tab with MicroQiskit, a tiny Qiskit that runs here. Open Code for this circuit, edit, and press Run.", {
    "qubits": 2, "steps": 5, "maxQubits": 3, "palette": GATE_BASIC, "results": ["chances", "shots"], "code": CODE_ALL, "codeOpen": True, "codeTab": "python", "console": False,
    "levels": [
        LV("Bell pair in Python", "Write qc.h(0) and qc.cx(0, 1) in the Python tab, then press Run.", "I-I-I-I-I\nI-I-I-I-I", {"probs": [P("00", approx=0.5), P("11", approx=0.5)], "via": "python"}, "H-X#0-I-I-I\nI-X#1-I-I-I", "Two lines: qc.h(0) and qc.cx(0, 1).", "Your code drew the circuit.", "from microqiskit import QuantumCircuit, simulate\n\nqc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure(0, 0)\nqc.measure(1, 1)\n\nprint(simulate(qc, 1000, 'counts'))"),
        LV("A rotation", "Use qc.rx(pi, 0) to make qubit 0 come out as 1. Add from math import pi at the top.", "I-I-I-I-I\nI-I-I-I-I", {"probs": [P("1", min=0.99)], "via": "python", "gates": {"require": ["rx"]}}, "RX(pi)-I-I-I-I\nI-I-I-I-I", "RX turns the qubit around the X axis. A half turn is pi.", "RX(pi) is a flip, like X.", "from microqiskit import QuantumCircuit, simulate\nfrom math import pi\n\nqc = QuantumCircuit(2)\nqc.rx(pi, 0)\n\nprint(simulate(qc, 100, 'counts'))"),
        LV("GHZ in Python", "Make three qubits agree: 000 or 111. Use a QuantumCircuit(3).", "I-I-I-I-I\nI-I-I-I-I\nI-I-I-I-I", {"probs": [P("000", approx=0.5), P("111", approx=0.5)], "via": "python"}, "H-X#0-I-I-I\nI-X#1-X#0-I-I\nI-I-X#1-I-I", "qc.h(0), then qc.cx(0, 1), then qc.cx(1, 2).", "A chain of CNOTs spreads the link.", "from microqiskit import QuantumCircuit, simulate\n\nqc = QuantumCircuit(3)\nqc.h(0)\nqc.cx(0, 1)\nqc.cx(1, 2)\n\nprint(simulate(qc, 1000, 'counts'))")]}, python=True)

LABS["qasm"] = lab("OpenQASM lab", "Write circuits as micro QASM. Open Code for this circuit, pick OpenQASM, edit, and press Apply.", {
    "qubits": 2, "steps": 5, "maxQubits": 4, "palette": GATE_BASIC, "results": ["chances", "shots"], "code": CODE_ALL, "codeOpen": True, "codeTab": "qasm", "console": False,
    "levels": [
        LV("Bell pair in OpenQASM", "Replace the program with: OPENQASM 3.0; qubit[2] q; h q[0]; cx q[0], q[1]; and press Apply.", "I-I-I-I-I\nI-I-I-I-I", {"probs": [P("00", approx=0.5), P("11", approx=0.5)], "via": "qasm"}, "H-X#0-I-I-I\nI-X#1-I-I-I", "Each gate is one line ending in a semicolon.", "That plain text is the same circuit.", "OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\nh q[0];\ncx q[0], q[1];"),
        LV("Fix the program", "This QASM program should make a Bell pair but one line is missing. Add it and press Apply.", "H-I-I-I-I\nI-I-I-I-I", {"probs": [P("00", approx=0.5), P("11", approx=0.5)], "via": "qasm"}, "H-X#0-I-I-I\nI-X#1-I-I-I", "The missing line is a CNOT: cx q[0], q[1];", "Now the two qubits are linked.", "OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\nh q[0];\ncx q[0], q[1];"),
        LV("One line for a whole register", "Use h q; to put every qubit of a 3 qubit register in superposition, so all 8 results are equally likely.", "I-I-I-I-I\nI-I-I-I-I\nI-I-I-I-I", {"probs": [P("000", approx=0.125, tol=0.01), P("111", approx=0.125, tol=0.01), P("010", approx=0.125, tol=0.01)], "via": "qasm"}, "H-I-I-I-I\nH-I-I-I-I\nH-I-I-I-I", "Declare qubit[3] q; then write h q;", "A register name without a number means all its qubits.", "OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[3] q;\nh q;"),
        LV("An angle", "Write rz(pi/2) between two h gates on one qubit so that the chance of 1 is 50%.", "I-I-I-I-I", {"probs": [P("1", approx=0.5, tol=0.02)], "via": "qasm", "gates": {"require": ["rz"]}}, "H-RZ(pi/2)-H-I-I", "Three lines: h, rz(pi/2), h.", "Angles can be written as pi/2.", "OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[1] q;\nh q[0];\nrz(pi/2) q[0];\nh q[0];")]}, python=True)

LABS["free"] = lab("Free playground", "Everything in one place: gates, chances, Inspect, shots, Python, OpenQASM, Q text, ASCII and the console.", {
    "qubits": 3, "steps": 6, "maxQubits": 5, "palette": GATE_BASIC, "results": ["chances", "shots", "inspect"], "code": CODE_ALL, "complete": "run", "start": "H-X#0-I-I-I-I\nI-X#1-I-I-I-I\nI-I-I-I-I-I"}, python=True)
