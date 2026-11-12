#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the quantum computing course. Usage: python3 make_quantum_computing_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "qc"))
sys.path.insert(0, os.path.join(HERE, "ql"))
import cmk, quantum_a, quantum_b, quantum_c, make_apps  # noqa: E402
import labs  # noqa: E402  (Quantum Web Lab configs)
make_apps.main()
CHS = quantum_c.INTRO + quantum_a.CHS + quantum_b.CHS[:4] + quantum_c.QISKIT + quantum_c.QASM + quantum_b.CHS[4:]
KEEP_PY = {"Count the numbers", "Two chances", "Apply H", "H, phase, H", "Tensor product", "Grover chance", "Standard error", "A stack of filters"}
LAB_FOR = ["bits", "qubit", "gates", "interference", "circuits", "twoq", "entangle", "algo", "noise", "qiskit", "qasm", "free"]
for _c in CHS:
    _c["lesson"] = [x for x in _c["lesson"] if not (isinstance(x, dict) and x.get("type") == "webxdc" and x["html"] != "__QPOLAR__")]
    _c["practice"] = [x for x in _c["practice"] if not (x["type"] == "webxdc" and x["html"] != "__QPOLAR__") and (x["type"] != "python" or x["title"] in KEEP_PY)]
    _apps = [x for x in _c["lesson"] if isinstance(x, dict) and x.get("type") == "webxdc"]
    _c["lesson"] = [x for x in _c["lesson"] if x not in _apps]
    _c["practice"] = _apps + _c["practice"]
for _i, _k in enumerate(LAB_FOR):
    _ch = CHS[_i + 1]
    _ch["practice"].insert(0, dict(labs.LABS[_k]))
PRONOUNCE = {"qubit": "cue bit", "qubits": "cue bits", "Qubit": "cue bit", "Qubits": "cue bits", "Q.js": "Q J S", "MicroQiskit": "micro kiss kit", "QASM": "kasm", "CNOT": "see not", "Hadamard": "had a mard",
    "Pauli": "pow lee", "Deutsch": "doich", "Grover": "grow ver", "Grover's": "grow vers", "Shor": "shore", "Shor's": "shores", "GHZ": "G H Z", "Bell": "bell",
    "amplitude": "am plih tude", "amplitudes": "am plih tudes", "decoherence": "dee co here ence", "Qiskit": "kiss kit", "Cirq": "surk", "oracle": "or a kul",
    "superposition": "super position", "entangled": "en tangled", "entanglement": "en tangle ment", "Stewart": "stew art", "IBM": "I B M", "ket": "ket",
    "PC": "P C", "NOT": "not", "SDK": "S D K", "MicroPython": "micro python", "tensor": "ten sor", "Born": "born", "asin": "arc sine", "OpenQASM": "open kasm", "Qiskit": "kiss kit", "polarizer": "polar eyes er", "photon": "foe ton", "photons": "foe tons", "quanta": "kwon ta", "quantum": "kwon tum", "Transpile": "trans pile", "transpile": "trans pile"}
SANDBOX = cmk.terminal("Quantum cheat sheet", "q>", "A scripted lookup. Try: qubit, x, h, z, t, cnot, bell, ghz, deutsch, grover, shots, noise, shor, console", [
    ("qubit", ["A qubit has two amplitudes. The chance of 0 is a squared, the chance of 1 is b squared."]),
    ("x", ["X swaps 0 and 1. Type X 1 in the Q Console."]),
    ("h", ["H turns a plain 0 into a fair blend. H twice returns to the start."]),
    ("z", ["Z flips the sign (phase) of the 1 amplitude. H, Z, H turns 0 into 1."]),
    ("t", ["T is a quarter-step phase turn (45 degrees)."]),
    ("cnot", ["CNOT flips the target when the control is 1. In text: X#0 on the control row, X#1 on the target row."]),
    ("bell", ["H on qubit 1 then CNOT 1 2 gives 00 or 11, 50 percent each."]),
    ("ghz", ["H, CNOT 1 2, CNOT 2 3 gives 000 or 111."]),
    ("deutsch", ["One oracle query tells constant from balanced."]),
    ("grover", ["About pi/4 times root N rounds finds the marked item."]),
    ("shots", ["Each shot is one run. The error shrinks with the square root of shots."]),
    ("noise", ["Noise and decoherence cause errors. Error correction needs extra qubits."]),
    ("shor", ["A quantum algorithm for factoring big numbers."]),
    ("console", ["Q Console commands: H 1, X 2, Z 1, T 1, CNOT 1 2, CZ 1 2, SWAP 1 2, run, shots 20, show, text, new 3, clear, undo, help, explain."]),
])
EXAM = [
 ("A bit is:", ["0 or 1", "A blend", "A gate", "A wave"], 0, "Two states."),
 ("A qubit can be:", ["A blend of 0 and 1", "Only 0", "Only 1", "A number above 1"], 0, "Superposition."),
 ("Measuring a qubit gives:", ["A plain 0 or 1", "A blend", "Both", "Nothing"], 0, "Collapse."),
 ("How many numbers describe 4 qubits?", ["16", "4", "8", "12"], 0, "2 to the 4."),
 ("The chance of an outcome is:", ["Amplitude squared", "Amplitude", "Amplitude plus 1", "Double the amplitude"], 0, "Born rule."),
 ("Chances always add up to:", ["1", "0", "2", "100"], 0, "Something must happen."),
 ("What does X do?", ["Swaps 0 and 1", "Makes a blend", "Measures", "Flips the sign"], 0, "A NOT."),
 ("What does H do to a plain 0?", ["Makes a fair blend", "Makes 1", "Nothing", "Measures"], 0, "A coin flip."),
 ("H then H does:", ["Return to the start", "Make 1", "Make a blend", "Nothing works"], 0, "Cancelling paths."),
 ("H, Z, H on plain 0 gives:", ["Plain 1", "Plain 0", "A fair coin", "Nothing"], 0, "Phase steers."),
 ("Opposite amplitudes:", ["Cancel", "Add", "Multiply", "Double"], 0, "Destructive."),
 ("A Z gate is a phase of:", ["180 degrees", "90 degrees", "45 degrees", "0 degrees"], 0, "A half turn."),
 ("In a circuit text, a row is:", ["A qubit", "A moment", "A gate", "A shot"], 0, "One wire."),
 ("The gate I does:", ["Nothing", "Flips", "Blends", "Measures"], 0, "Identity."),
 ("X#0 and X#1 together form:", ["A CNOT", "An H", "A swap", "A measurement"], 0, "Control and target."),
 ("CNOT flips the target when:", ["The control is 1", "The control is 0", "Always", "Never"], 0, "Conditional."),
 ("Two qubits have how many amplitudes?", ["4", "2", "3", "8"], 0, "Four answers."),
 ("A Bell state gives:", ["00 or 11", "01 or 10", "Any", "Only 00"], 0, "Always agree."),
 ("Entanglement can send messages faster than light:", ["No", "Yes", "Sometimes", "Only Bell states"], 0, "It cannot."),
 ("Deutsch needs how many oracle queries?", ["1", "2", "4", "0"], 0, "Quantum saves one."),
 ("Grover search takes about:", ["Root N steps", "N steps", "N squared", "1 step"], 0, "Quadratic."),
 ("A shot is:", ["One run and one measurement", "A gate", "A qubit", "A phase"], 0, "Repeat for chances."),
 ("More shots make estimates:", ["More accurate", "Less accurate", "The same", "Random"], 0, "Root shots."),
 ("Shor's algorithm is for:", ["Factoring", "Sorting", "Printing", "Typing"], 0, "Breaks some codes."),
 ("Is a quantum computer faster at everything?", ["No", "Yes", "Only games", "Only email"], 0, "Special jobs only."),
]
CFG = dict(id="quantum-computing", title="Quantum Computing for Beginners",
    subtitle="Qubits, gates, interference and entanglement with hands-on circuit labs, for curious kids, teens and adults",
    description="A friendly first course on quantum computing with no maths beyond squares and multiplication. Learn bits and qubits, amplitudes and measurement, the X, H, Z and T gates, interference, circuit text, CNOT, entanglement and Bell states, Deutsch and Grover's algorithms, noise and shots, and what quantum computers are really good for. Every chapter has a hands-on lab built on our own Quantum Web Lab (github.com/lucky-edgelord/quantum-web-lab): a mobile-friendly circuit composer with live chances, Inspect view, a friendly console, ASCII and Q text notation, MicroQiskit (a tiny Qiskit that runs offline) and micro OpenQASM. A few short Python labs build the maths in code. The circuit text notation is inspired by Q.js by Stewart Smith (github.com/stewdio/q.js, MIT) and the layout by the IBM Quantum Composer. Includes an intuitive intro to quantum mechanics, a Qiskit chapter and an OpenQASM chapter.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="ql", apps={"__QPOLAR__": "qpolar.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "quantum-computing.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
