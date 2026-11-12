#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the quantum computing course. Usage: python3 make_quantum_computing_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "qc"))
sys.path.insert(0, os.path.join(HERE, "ql"))
import cmk, quantum_a, quantum_b, quantum_c, quantum_d, make_apps  # noqa: E402
import figs  # noqa: E402
import maps as qmaps  # noqa: E402
from clib import T  # noqa: E402
import labs  # noqa: E402  (Quantum Web Lab configs)
make_apps.main()
CHS = quantum_c.INTRO + quantum_a.CHS[:4] + quantum_d.BLOCH + quantum_a.CHS[4:] + quantum_b.CHS[:4] + quantum_c.QASM + quantum_c.QISKIT + quantum_b.CHS[4:]
KEEP_PY = {"Count the numbers", "Two chances", "Apply H", "H, phase, H", "Tensor product", "Grover chance", "Standard error", "A stack of filters", "Chance from the angle"}
LAB_FOR = ["bits", "qubit", "gates", "interference", "bloch", "circuits", "twoq", "entangle", "algo", "noise", "qasm", "qiskit", "free"]
for _c in CHS:
    _c["lesson"] = [x for x in _c["lesson"] if not (isinstance(x, dict) and x.get("type") == "webxdc" and x["html"] != "__QPOLAR__")]
    _c["practice"] = [x for x in _c["practice"] if not (x["type"] == "webxdc" and x["html"] != "__QPOLAR__") and (x["type"] != "python" or x["title"] in KEEP_PY)]
    _apps = [x for x in _c["lesson"] if isinstance(x, dict) and x.get("type") == "webxdc"]
    _c["lesson"] = [x for x in _c["lesson"] if x not in _apps]
    _c["practice"] = _apps + _c["practice"]
for _i, _k in enumerate(LAB_FOR):
    _ch = CHS[_i + 1]
    _ch["practice"].insert(0, dict(labs.LABS[_k]))

FIG = lambda name, cap: {"type": "figure", "image": name, "caption": cap}
INS = [
 ("Quantum mechanics", "Start with a ball", "qm-ball-electron.svg", "A ball has one path. An electron is a cloud of possibilities until you look."),
 ("Quantum mechanics", "Normal thinking says", "qm-filters.svg", "Two crossed filters block all light, yet a third filter between them lets some through."),
 ("Bits, chance", "A qubit is more like", "bits-vs-qubits.svg", "A bit, a coin and a qubit side by side."),
 ("Bits, chance", "Here is why people", "bits-double.svg", "Each extra qubit doubles the numbers you need."),
 ("The qubit", "To turn amplitudes", "qubit-squares.svg", "Square the amplitudes to get the chances."),
 ("One-qubit gates", "Z does not change", "gates-effect.svg", "X, H and Z change the amplitudes in different ways."),
 ("Interference", "Here is the experiment", "interference-waves.svg", "Waves in step add up. Waves out of step cancel."),
 ("Interference", "Now put a Z between", "interference-paths.svg", "H, Z, H: the routes to 0 cancel and the routes to 1 add up."),
 ("The Bloch sphere", "Height is chance", "bloch-sphere.svg", "The Bloch sphere: north pole is 0, south pole is 1, the equator holds the blends."),
 ("The Bloch sphere", "The H gate is a half turn", "bloch-gates.svg", "Each gate is a turn of the globe."),
 ("Reading circuits", "Look at a circuit like", "circuit-read.svg", "A circuit read from left to right: blend, link, look."),
 ("Two qubits", "The CNOT gate has", "cnot-table.svg", "CNOT flips the second qubit only when the first is 1."),
 ("Entanglement", "The state is now half", "bell-pair.svg", "A Bell pair: the two results always agree."),
 ("Small algorithms", "Grover's search is", "grover-bars.svg", "Grover on four items: mark the prize, then reflect about the average."),
 ("Noise, shots", "How big is the wobble", "shots-wobble.svg", "More shots give steadier counts."),
 ("OpenQASM", "Think of OpenQASM", "qasm-vs-circuit.svg", "The same Bell circuit as a picture and as OpenQASM."),
 ("Qiskit", "Next is the trap", "endian.svg", "Our composer puts qubit 0 on the left. Qiskit puts it on the right."),
 ("Qiskit", "A full Qiskit program", "qiskit-pipeline.svg", "Build, transpile, run, read."),
 ("Uses, myths", "What could a large", "uses-map.svg", "Where quantum computers may help, and where they will not."),
]
_fig_no = {}
for _t, _p, _f, _cap in INS:
    _ci = [i for i, c in enumerate(CHS) if c["title"].startswith(_t)][0]
    _ch = CHS[_ci]
    _k = [i for i, b in enumerate(_ch["lesson"]) if b["type"] == "text" and b["items"][0].startswith(_p)]
    assert _k, (_t, _p)
    _fig_no[_ci] = _fig_no.get(_ci, 0) + 1
    _num = "%d.%d" % (_ci + 1, _fig_no[_ci])
    _anchor = _ch["lesson"][_k[0]]
    _anchor["items"][-1] = _anchor["items"][-1].rstrip() + " (See Figure %s below.)" % _num
    _ch["lesson"].insert(_k[0] + 1, FIG(_f, "Figure %s. %s" % (_num, _cap)))
for _i in range(1, len(CHS)):
    _prev = CHS[_i - 1]
    CHS[_i]["lesson"].insert(0, T("Quick recap of the last chapter, " + _prev["title"] + ":", *["• " + k for k in _prev["keyPoints"]]))
MNEM = [
 ("PWP: Packets, Waves, Peeking", "Tiny things come in Packets, spread like Waves, and change when you Peek."),
 ("A bit lies flat, a qubit spins", "Coin on the table is a bit, coin in the air is a qubit. Add a qubit and the list doubles: 2, 4, 8, 16."),
 ("Square it to share it", "Square each amplitude to get a chance, and the chances share 100 percent between them."),
 ("Flip, Blend, Twist", "X Flips, H Blends, Z Twists the sign. Two H gates cancel: blend, then un-blend."),
 ("Same shines, opposite vanishes", "Same sign adds up and shines. Opposite sign cancels and vanishes. Add first, then square."),
 ("Top is Zero, bottom is One", "Top is Zero, bottom is One. Height tells the chance, going Round tells the phase, and gates are turns of the globe."),
 ("Rows are players, columns are beats", "Rows are players (qubits), columns are beats (time). Read left to right, with qubit 0 on top."),
 ("Controller nods, Target turns", "If the Controller says 1, the Target turns. If it says 0, nothing happens."),
 ("Blend, then Bind", "Blend one qubit with H, then Bind it to another with CNOT, and you have a Bell pair."),
 ("Mark, Mirror, Measure", "Grover is Mark the prize, Mirror about the average, then Measure. Deutsch asks once instead of twice."),
 ("Quadruple the shots, halve the wobble", "Four times as many shots makes the wobble half as big."),
 ("Name it, Size it, Use it", "OpenQASM: Name the version, Size the qubits, Use the gates, one per line."),
 ("Build, Transpile, Run, Read", "Qiskit is Build, Transpile, Run, Read. And Qiskit keeps qubit 0 on the Right."),
 ("Molecules, Searching, Secrets", "Quantum is a special tool: Molecules, Searching, Secrets. It is not a faster everything."),
]
assert len(MNEM) == len(CHS)
for _c, (_m, _d) in zip(CHS, MNEM):
    _full = _d if _d.startswith(_m) else _m + ". " + _d
    _c["lesson"].append(T("Memory trick: " + _full))
    _c["cards"].append({"q": "Memory trick for: " + _c["title"] + "?", "a": _full})
assert len(qmaps.MAPS) == len(CHS)
for _c, _ms in zip(CHS, qmaps.MAPS):
    _c["maps"] = [{"title": _t, "links": _l} for _t, _l in _ms]
IMAGES = figs.build_all()
PRONOUNCE = {"qubit": "cue bit", "qubits": "cue bits", "Qubit": "cue bit", "Qubits": "cue bits", "Q.js": "Q J S", "MicroQiskit": "micro kiss kit", "Bloch": "block", "Bloch sphere": "block sphere", "QASM": "kasm", "CNOT": "see not", "Hadamard": "had a mard",
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
 ("On the Bloch sphere, where is a plain 1?", ["South pole", "North pole", "Equator", "Centre"], 0, "Bottom of the globe."),
 ("What does a shorter arrow inside the Bloch ball tell you?", ["The qubit is entangled", "The qubit is plain 0", "Nothing", "Noise only"], 0, "Information is shared."),
 ("Shor's algorithm is for:", ["Factoring", "Sorting", "Printing", "Typing"], 0, "Breaks some codes."),
 ("Is a quantum computer faster at everything?", ["No", "Yes", "Only games", "Only email"], 0, "Special jobs only."),
]
CFG = dict(id="quantum-computing", title="Quantum Computing for Beginners",
    subtitle="Qubits, gates, the Bloch sphere, interference and entanglement with hands-on circuit labs, for curious kids, teens and adults",
    description="A friendly first course on quantum computing with no maths beyond squares and multiplication. Learn bits and qubits, amplitudes and measurement, the X, H, Z and T gates, interference, circuit text, CNOT, entanglement and Bell states, Deutsch and Grover's algorithms, noise and shots, and what quantum computers are really good for. Every chapter has a hands-on lab built on our own Quantum Web Lab (github.com/lucky-edgelord/quantum-web-lab): a mobile-friendly circuit composer with live chances, Inspect view, a friendly console, ASCII and Q text notation, MicroQiskit (a tiny Qiskit that runs offline) and micro OpenQASM. A few short Python labs build the maths in code. The circuit text notation is inspired by Q.js by Stewart Smith (github.com/stewdio/q.js, MIT) and the layout by the IBM Quantum Composer. Includes an intuitive intro to quantum mechanics, an interactive Bloch sphere chapter, a Qiskit chapter and an OpenQASM chapter.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="ql", images=IMAGES, apps={"__QPOLAR__": "qpolar.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "quantum-computing.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
