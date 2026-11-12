# -*- coding: utf-8 -*-
"""Quantum computing course: the plain-words intro, Qiskit and OpenQASM chapters."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

INTRO, QISKIT, QASM = [], [], []


def APP(key, title, intro, h=1000):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


INTRO.append(CH(
 "Quantum mechanics in plain words",
 ("The small world", [
  "Atoms | follow | Quantum rules",
  "Light | acts like | Waves and packets",
  "Quantum | means | Comes in packets",
  "Looking | changes | What you see",
  "Photon | has | Polarization",
  "Polarization | can be | A qubit"]),
 ["Everything is made of tiny things, and tiny things do not behave like baseballs. Quantum mechanics is the rulebook for the small world of atoms, electrons and light.",
  "Three ideas carry the whole subject. Things come in packets. Before you look, a thing can be a blend of possibilities. And looking changes what you get.",
  "You do not need to believe it blindly. You will test it with a simulated experiment about light and sunglasses, which gives a surprise that normal thinking cannot explain."],
 [("Quantum", "A small packet. Light and energy come in packets called quanta."),
  ("Photon", "One packet of light."),
  ("Wave", "A spreading ripple that can add up or cancel."),
  ("Polarization", "The direction a light wave wiggles."),
  ("Uncertainty", "You cannot know everything about a tiny thing at once.")],
 ["Energy and light come in packets, called quanta.",
  "Tiny things act like waves that can add or cancel.",
  "Before you look, a thing can be a blend of possibilities.",
  "Looking changes the result.",
  "A photon's polarization is the easiest real qubit."],
 [T("Start with a ball. Roll it and you know where it is and how fast it goes, always. Baseball rules are called classical physics. They work for balls, cars and planets. They fail for the really small, like an electron."),
  T("Idea one: things come in packets. You cannot pour light out like water. Light comes as little lumps called photons, and energy as small steps. The word quantum just means a packet or a step. You can have one photon or two, never one and a half."),
  T("Idea two: tiny things spread like waves. Shoot one electron at a wall with two slits and it does not pick one slit. It goes through like a wave and the two ripples meet on the other side. Over many electrons the screen shows stripes, from ripples adding and cancelling. Stripes are interference, the same idea you will use for algorithms."),
  C("# two ripples meet; phi is how far out of step they are\nimport math\nfor phi in (0, 90, 180):\n    brightness = 2 * (1 + math.cos(math.radians(phi)))\n    print(phi, 'degrees out of step: brightness', round(brightness, 2))", "python"),
  T("Idea three: looking changes things. If you place a detector at the slits to see which slit the electron used, the stripes vanish. Asking the electron a plain question forces a plain answer, and the blend is gone. That is measurement, and you met it with the qubit."),
  T("Now a test you can do with sunglasses. A polarizing filter is a tiny fence. Light that wiggles along the fence gets through, and light that wiggles across is blocked. Two filters crossed at 90 degrees block everything. Put a third filter at 45 degrees between them, and some light comes back through! Adding a blocker let more light pass."),
  T("Normal thinking says that is impossible. Quantum thinking says each filter is a measurement. After the 45 degree filter, the photon is re-set to that direction, so it has a fair chance of passing the last filter. Open the lab and try it. A photon's direction is a perfect real-world qubit.")],
 [("What does the word quantum mean?", ["A small packet or step", "Very fast", "Very big", "Invisible"], 0, "Lumps."),
  ("What is one packet of light?", ["A photon", "An atom", "A wave", "A proton"], 0, "Photon."),
  ("What do the stripes in the double slit show?", ["Interference of waves", "Dirt on the screen", "Broken light", "Heat"], 0, "Add and cancel."),
  ("What happens if you detect which slit was used?", ["The stripes vanish", "The stripes get brighter", "Nothing", "The slits close"], 0, "Measurement forces an answer."),
  ("Two crossed polarizers let through:", ["Nothing", "Everything", "Half", "Only red"], 0, "90 degrees."),
  ("Adding a third filter at 45 degrees:", ["Lets some light through", "Blocks more", "Does nothing", "Breaks the filters"], 0, "Each filter resets the direction.")],
 [("Quantum", "A packet or step"), ("Interference", "Waves adding or cancelling"), ("Polarization", "The direction light wiggles"), ("Measurement", "Looking forces a plain answer")],
 [APP("QPOLAR", "Polarizer lab", "Send photons through filters. First block everything with two crossed filters, then add a middle filter and watch light return.", 900),
  MATCH("Match the idea", "Pair each idea with its meaning.", [("Quantum", "a small packet"), ("Interference", "waves add or cancel"), ("Polarizer", "a fence for light"), ("Measurement", "looking forces an answer")]),
  FILL("Plain words", "Light comes in packets called {{photons}}. Waves can add or {{cancel}}. Looking at a tiny thing {{changes}} what you see. Crossed filters block {{all}} the light."),
  PL("Packets", "Energy comes in whole packets. Write packets(total, size): return [how many whole packets fit, what is left over].", "packets(total, size)", '''
def packets(total, size):
    return [total // size, total % size]
''', [[10, 3], [7, 7], [2, 5]], "Whole division and remainder."),
  PL("A filter", "A photon wiggling at an angle meets a filter. The chance it passes is cos squared of the angle between them. Write passes(angle): use import math and round to 4 decimals.", "passes(angle)", '''
import math
def passes(angle):
    return round(math.cos(math.radians(angle)) ** 2, 4)
''', [[0], [30], [45], [90]], "Cosine squared."),
  PL("A stack of filters", "Write chain(angles): angles is the list of filter angles in order. A photon that already passed the first filter passes each next one with chance cos squared of the difference. Return the product, rounded to 4 decimals.", "chain(angles)", '''
import math
def chain(angles):
    p = 1.0
    for i in range(1, len(angles)):
        p = p * math.cos(math.radians(angles[i] - angles[i - 1])) ** 2
    return round(p, 4)
''', [[[0, 90]], [[0, 45, 90]], [[0, 30, 60, 90]]], "Multiply each step."),
  PL("Two slits", "Two ripples of size a meet, out of step by phi degrees. The brightness is 2*a*a*(1 + cos phi). Write two_slits(a, phi), rounded to 4 decimals.", "two_slits(a, phi)", '''
import math
def two_slits(a, phi):
    return round(2 * a * a * (1 + math.cos(math.radians(phi))), 4)
''', [[1, 0], [1, 180], [1, 90]], "Ripples add or cancel."),
  ORDER("Order the surprise", "Put the three filter experiment in order.", ["Light passes the first filter", "The middle filter sets a new direction", "The last filter now lets some through", "Light shows up where there was none"])]))

QISKIT.append(CH(
 "From the composer to real code: OpenQASM and Qiskit",
 ("Code", [
  "Composer | writes | Code",
  "Qiskit | is | Python toolkit",
  "OpenQASM | is | Text format",
  "QuantumCircuit | holds | Gates",
  "Statevector | gives | Chances",
  "IBM Quantum | runs | Real chips"]),
 ["Every circuit you drew has a text form. The Code panel under the composer shows it as Qiskit, an open source Python toolkit from IBM, and as OpenQASM, a plain text format many tools read.",
  "In Qiskit you make a QuantumCircuit and call methods like h, x and cx. A Statevector gives you the exact chances, and a Sampler runs shots on a simulator or a real chip.",
  "Watch one trap: Qiskit counts qubits from 0 and prints qubit 0 on the right, while our composer reads q[0] at the top and writes it on the left."],
 [("Qiskit", "An open source Python toolkit for quantum circuits."),
  ("QuantumCircuit", "The Qiskit object that holds your gates."),
  ("OpenQASM", "A plain text language for circuits."),
  ("Sampler", "Runs a circuit many times and returns counts."),
  ("Transpile", "Rewrite a circuit to use the gates a chip supports.")],
 ["qc = QuantumCircuit(2) makes 2 qubits.",
  "qc.h(0) is an H on qubit 0. qc.cx(0, 1) is a CNOT.",
  "Statevector(qc).probabilities_dict() gives exact chances.",
  "Qiskit prints qubit 0 on the right.",
  "OpenQASM 3 is the shared text format."],
 [T("Open any lab and the Code panel below the composer. Build the Bell state with H then CNOT and open Qiskit. You will see a few lines of Python. The composer did not invent the code. It just translated your picture."),
  C("from qiskit import QuantumCircuit\nfrom qiskit.quantum_info import Statevector\n\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0, 1)\n\nprint(Statevector(qc).probabilities_dict())", "python"),
  T("Line by line. The first line makes a circuit with 2 qubits, both starting at 0. The H puts qubit 0 in a blend. The CNOT links qubit 1 to it. Statevector works out the chances exactly with no shots, like our bars. The output shows 00 and 11 with 0.5 each."),
  T("Next is the trap. Our composer reads left to right, so q[0] is the leftmost bit. Qiskit does the opposite and writes qubit 0 on the right. A state we call 10 appears in Qiskit as 01. The result is the same, only the label is flipped, so always check which one you are reading."),
  C("OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\nh q[0];\ncx q[0], q[1];\nbit[2] c;\nc = measure q;", "text"),
  T("OpenQASM is the same circuit as plain text. Many tools can read it, so it works like a shared language. To run on a real chip, you make a free IBM Quantum account, pick a machine, and the toolkit transpiles your circuit into the gates that chip supports. Queues can take a while, so simulate first."),
  T("A good habit: draw it in the composer, look at the Qiskit code, change one line, and predict what changes. Then try the code in a notebook. Reading code that you drew yourself is a gentle way into real quantum programming.")],
 [("What is Qiskit?", ["A Python toolkit for quantum circuits", "A quantum chip", "A game", "A web browser"], 0, "From IBM, open source."),
  ("Which line makes an H on the first qubit?", ["qc.h(0)", "qc.h(1)", "qc.cx(0, 1)", "qc.x(0)"], 0, "Numbering starts at 0."),
  ("Where does Qiskit print qubit 0?", ["On the right", "On the left", "In the middle", "Nowhere"], 0, "Little endian."),
  ("What does a Statevector give you?", ["Exact chances", "Noise", "Shots only", "Gates"], 0, "No shots needed."),
  ("What is OpenQASM?", ["A plain text circuit format", "A chip", "A password", "An image"], 0, "Shared language."),
  ("Why transpile?", ["Match the gates a chip supports", "Make it fun", "Add noise", "Measure"], 0, "Chips have limits.")],
 [("QuantumCircuit", "Qiskit object holding gates"), ("cx", "Qiskit name for CNOT"), ("OpenQASM", "Shared text format"), ("Transpile", "Rewrite for a chip")],
 [MATCH("Match the code", "Pair each Qiskit call with the gate.", [("qc.h(0)", "H on qubit 0"), ("qc.x(1)", "X on qubit 1"), ("qc.cx(0, 1)", "CNOT 0 to 1"), ("qc.cz(0, 1)", "CZ 0 and 1")]),
  FILL("Qiskit", "A circuit is a {{QuantumCircuit}}. The CNOT method is called {{cx}}. Qiskit prints qubit 0 on the {{right}}. {{OpenQASM}} is a plain text format."),
  PL("Write Qiskit lines", "Each gate is a list like ['h', 0] or ['cx', 0, 1]. Write to_qiskit(gates): return one string per gate like 'qc.h(0)' and 'qc.cx(0, 1)'.", "to_qiskit(gates)", '''
def to_qiskit(gates):
    out = []
    for g in gates:
        args = ', '.join([str(x) for x in g[1:]])
        out.append('qc.' + g[0] + '(' + args + ')')
    return out
''', [[[["h", 0], ["cx", 0, 1]]], [[["x", 2]]], [[["h", 0], ["z", 0], ["h", 0]]]], "Name plus arguments."),
  PL("Flip the bits", "Qiskit writes qubit 0 on the right. Write flip_bits(label): the label with its characters in reverse order. Do not use slice steps.", "flip_bits(label)", '''
def flip_bits(label):
    out = ''
    for ch in label:
        out = ch + out
    return out
''', [["01"], ["110"], ["1"]], "Prepend each character."),
  PL("Circuit depth", "Depth is how many steps a circuit needs. Each gate is a list of the qubits it touches. A gate starts after every qubit it uses is free. Write depth(gates): return the biggest step count.", "depth(gates)", '''
def depth(gates):
    t = {}
    best = 0
    for g in gates:
        s = 0
        for q in g:
            if t.get(q, 0) > s:
                s = t.get(q, 0)
        s += 1
        for q in g:
            t[q] = s
        if s > best:
            best = s
    return best
''', [[[[0], [1], [0, 1]]], [[[0], [0], [0]]], [[[0, 1], [1, 2], [0, 2]]]], "Track a clock per qubit."),
  PL("Counts to chances", "A Sampler returns counts as [state, count] pairs. Write probs(counts, shots): return [[state, count / shots rounded to 4 decimals], ...] in the same order.", "probs(counts, shots)", '''
def probs(counts, shots):
    return [[c[0], round(c[1] / shots, 4)] for c in counts]
''', [[[["00", 48], ["11", 52]], 100], [[["0", 1], ["1", 3]], 4]], "Divide each count."),
  ORDER("Order the workflow", "Put a typical quantum coding workflow in order.", ["Draw the circuit", "Read the code", "Simulate it", "Run it on real hardware"])]))


QASM.append(CH(
 "OpenQASM: the shared language of circuits",
 ("OpenQASM", [
  "OpenQASM | is | Circuit text",
  "qubit[n] q | makes | Qubits",
  "h q[0]; | applies | A gate",
  "cx | is | CNOT",
  "measure | fills | Bits",
  "Many tools | read | OpenQASM"]),
 ["OpenQASM stands for Open Quantum Assembly Language. It writes a circuit as plain lines of text, one gate per line. IBM Quantum Composer, Qiskit and many other tools can read and write it.",
  "A program has a header, a place to declare qubits, a list of gates and a measurement. Every line ends with a semicolon. Comments start with two slashes.",
  "Version 3 is the modern one and the composer shows it. Older files use version 2, with slightly different words, and you can convert them by hand."],
 [("OpenQASM", "Open Quantum Assembly Language: plain text for circuits."),
  ("Header", "The first lines: version and the gate library."),
  ("stdgates.inc", "The standard gate library: h, x, y, z, t, cx, cz and more."),
  ("Declaration", "A line that makes qubits or bits, like qubit[2] q;"),
  ("Measure", "Reads qubits into classical bits.")],
 ["Start with OPENQASM 3.0; and include stdgates.inc.",
  "qubit[2] q; makes two qubits. bit[2] c; makes two result bits.",
  "h q[0]; is an H on the first qubit. cx q[0], q[1]; is a CNOT.",
  "c = measure q; reads all qubits into bits.",
  "Version 2 used qreg, creg and measure q -> c."],
 [T("Think of OpenQASM as the recipe card for a circuit. The picture in the composer and the card say exactly the same thing. The advantage of text is that you can save it, mail it, paste it into other tools or run it on a real machine."),
  C("OPENQASM 3.0;\ninclude \"stdgates.inc\";\n\nqubit[2] q;\nbit[2] c;\n\nh q[0];\ncx q[0], q[1];\n\nc = measure q;", "text"),
  T("Read it top down. The first line names the version. The include line brings in the standard gates, so h, x and cx mean what you expect. The qubit line makes two qubits called q, numbered from 0. The bit line makes two classical bits called c to hold the answers."),
  T("Then come the gates, one per line, in the order they happen. A gate name, a space, then the qubits it acts on. h q[0]; is an H on qubit 0. cx q[0], q[1]; is a CNOT with qubit 0 as control and qubit 1 as target. The last line measures every qubit into the bits."),
  T("Here is how our composer symbols map to the text. H is h, X is x, Y is y, Z is z, T is t, CNOT is cx and CZ is cz. Each column of the composer becomes a few lines, in order from left to right. Open the Code panel on the OpenQASM tab and watch it change as you tap."),
  C("OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0], q[1];\nmeasure q -> c;", "text"),
  T("You will meet older version 2 files. They say qreg and creg instead of qubit and bit, include a library called qelib1.inc, and measure with an arrow. The gates are the same. Converting between the two is mostly renaming a few lines."),
  T("Version 3 adds extras that you will grow into. You can define your own gate, like a recipe that calls other gates. You can run a gate only if a measured bit is 1, which is how teleportation works. And you can write angles for rotation gates, like rz(pi/4) q[0]; which is a smaller phase turn.")],
 [("What does OpenQASM stand for?", ["Open Quantum Assembly Language", "Open Quantum Answer Machine", "Only Quantum Math", "Open Qubit Array"], 0, "Text for circuits."),
  ("What does h q[0]; do?", ["H on the first qubit", "H on every qubit", "A CNOT", "A measurement"], 0, "Gate, space, qubit."),
  ("Which line makes 3 qubits in version 3?", ["qubit[3] q;", "qreg q[3];", "make 3;", "q = 3;"], 0, "Version 3 wording."),
  ("What is cx?", ["A CNOT", "A copy", "A cross", "A clear"], 0, "Controlled X."),
  ("Which version used qreg?", ["Version 2", "Version 3", "Both", "Neither"], 0, "Older files."),
  ("How do you read qubits into bits in version 3?", ["c = measure q;", "measure q -> c;", "read q;", "end;"], 0, "Assign the measure.")],
 [("Header", "Version and gate library lines"), ("cx", "OpenQASM name for CNOT"), ("measure", "Read qubits into bits"), ("qreg", "Version 2 way to make qubits")],
 [MATCH("Match the symbol", "Pair each composer gate with its OpenQASM name.", [("H", "h"), ("CNOT", "cx"), ("CZ", "cz"), ("T", "t")]),
  FILL("OpenQASM", "A program starts with the {{OPENQASM}} line. {{qubit}} declares qubits and {{bit}} declares result bits. A CNOT is written {{cx}}. Version 2 used {{qreg}}."),
  PL("Write the header", "Write header(n): return the three header lines for n qubits: 'OPENQASM 3.0;', the include line for stdgates.inc in double quotes, and 'qubit[n] q;' (with the real number).", "header(n)", '''
def header(n):
    return ['OPENQASM 3.0;', 'include "stdgates.inc";', 'qubit[' + str(n) + '] q;']
''', [[1], [3], [5]], "Join the number into the last line."),
  PL("Read a gate line", "Write parse_gate(line): turn 'cx q[0], q[1];' into ['cx', [0, 1]] and 'h q[2];' into ['h', [2]].", "parse_gate(line)", '''
def parse_gate(line):
    line = line.strip().rstrip(';')
    name, rest = line.split(' ', 1)
    qs = []
    for p in rest.split(','):
        qs.append(int(p.strip().split('[')[1].split(']')[0]))
    return [name, qs]
''', [["cx q[0], q[1];"], ["h q[2];"], ["cz q[1], q[2];"]], "Split off the name, then dig the numbers out of the brackets."),
  PL("Count the gates", "Write count_gates(program): how many lines of the program are gates. A gate line starts with one of h, x, y, z, t, cx, cz. Ignore everything else.", "count_gates(program)", '''
def count_gates(program):
    names = ['h', 'x', 'y', 'z', 't', 'cx', 'cz']
    n = 0
    for line in program.split('\\n'):
        line = line.strip()
        if line and line.split(' ')[0] in names:
            n += 1
    return n
''', [["OPENQASM 3.0;\nqubit[2] q;\nh q[0];\ncx q[0], q[1];"], ["h q[0];\nx q[0];\nz q[0];"], ["OPENQASM 3.0;"]], "Check the first word of each line."),
  PL("Version 2 to 3", "Write upgrade(line): convert one old line. 'OPENQASM 2.0;' becomes 'OPENQASM 3.0;'. 'qreg q[2];' becomes 'qubit[2] q;'. 'creg c[2];' becomes 'bit[2] c;'. 'measure q -> c;' becomes 'c = measure q;'. Anything else is unchanged.", "upgrade(line)", '''
def upgrade(line):
    if line == 'OPENQASM 2.0;':
        return 'OPENQASM 3.0;'
    if line.startswith('qreg '):
        name, size = line[5:-1].split('[')
        return 'qubit[' + size[:-1] + '] ' + name + ';'
    if line.startswith('creg '):
        name, size = line[5:-1].split('[')
        return 'bit[' + size[:-1] + '] ' + name + ';'
    if line == 'measure q -> c;':
        return 'c = measure q;'
    return line
''', [["OPENQASM 2.0;"], ["qreg q[2];"], ["creg c[3];"], ["measure q -> c;"], ["h q[0];"]], "Handle each kind of line."),
  PL("Composer to OpenQASM", "Write to_qasm(text): turn composer text into gate lines. Rows are qubits, gates in a row are joined by dashes. Go column by column. In each column list the single gates by row (h, x, y, z, t, in lower case), then a linked pair: X#0 and X#1 make 'cx q[a], q[b];' and Z#0 and Z#1 make 'cz q[a], q[b];'. Skip I.", "to_qasm(text)", '''
def to_qasm(text):
    rows = [r.split('-') for r in text.split('\\n') if r.strip()]
    out = []
    for c in range(len(rows[0])):
        ctl = -1
        tg = -1
        kind = ''
        for r in range(len(rows)):
            t = rows[r][c]
            if t == 'I':
                continue
            if t.endswith('#0'):
                ctl = r
                kind = t[0]
            elif t.endswith('#1'):
                tg = r
            else:
                out.append(t.lower() + ' q[' + str(r) + '];')
        if ctl >= 0 and tg >= 0:
            name = 'cx' if kind == 'X' else 'cz'
            out.append(name + ' q[' + str(ctl) + '], q[' + str(tg) + '];')
    return out
''', [["H-X#0\nI-X#1"], ["X-I-Z\nI-H-I"], ["H-Z#0\nH-Z#1"]], "Walk the columns, then the rows."),
  ORDER("Order the program", "Put the parts of an OpenQASM program in order.", ["OPENQASM 3.0; header", "include the standard gates", "declare qubits and bits", "gates", "measure"])]))
