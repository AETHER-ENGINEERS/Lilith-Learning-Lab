# -*- coding: utf-8 -*-
"""Quantum computing for beginners, part 1: chapters 1-5."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=1000):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Bits, chance and why quantum is different",
 ("Quantum basics", [
  "Bit | is | 0 or 1",
  "Qubit | is | 0 and 1 at once",
  "Probability | describes | chance",
  "Superposition | is | Mix of 0 and 1",
  "n qubits | hold | 2^n amounts",
  "Classical computer | uses | Bits"]),
 ["A normal computer stores everything as bits. A bit is a tiny switch that is either 0 or 1. Photos, games and messages are all long rows of switches.",
  "A quantum computer uses qubits. A qubit can be 0, 1, or a special mix of both until you look at it. Looking at it is called measuring, and it always gives a plain 0 or 1.",
  "This is not magic and it is not faster at everything. It is a different way to compute, and for a few jobs it can be much faster. This course teaches the real ideas, and you will play with a real simulator all the way."],
 [("Bit", "The smallest piece of information: 0 or 1."),
  ("Qubit", "A quantum bit. It can be in a mix of 0 and 1."),
  ("Superposition", "Being in a mix of states at the same time."),
  ("Measurement", "Looking at a qubit, which gives a plain 0 or 1."),
  ("Simulator", "A normal computer program that pretends to be a quantum computer.")],
 ["A bit is 0 or 1. A qubit can be a mix of both.",
  "n bits hold one value. n qubits need 2 to the power n numbers to describe.",
  "Measuring always gives a plain 0 or 1.",
  "Quantum computers help with some jobs, not everything.",
  "We use the Q.js simulator, which runs right here."],
 [T("Start with a coin. Flip it and it lands heads or tails. Before you look, you do not know which. Chance describes how likely each one is. A fair coin is 50 percent heads and 50 percent tails."),
  T("A normal bit is like a coin lying flat: it is definitely heads or definitely tails. You can read it as often as you like and it never changes. Computers are built from billions of these."),
  T("A qubit is more like a coin spinning in the air. While it spins it is not heads and not tails, it is a blend. When it lands, which is when you measure, you get one clean answer. The blend only decides the chances."),
  T("Here is why people get excited. To describe 3 normal bits you write 3 digits. To describe 3 qubits you need 8 numbers, one for each possible answer. Add one qubit and you double the numbers. 50 qubits already need more numbers than any laptop can store."),
  C("# how many numbers describe n qubits?\nfor n in range(1, 8):\n    print(n, 'qubits need', 2 ** n, 'numbers')", "python"),
  T("A big warning, because the internet gets this wrong. A quantum computer is not trying every answer at once and handing you the best. When you measure you only get one answer. The skill is in arranging things so the right answer becomes the likely one. You will learn how.")],
 [("What does a bit store?", ["0 or 1", "Any number", "A word", "A picture"], 0, "Two states."),
  ("What does measuring a qubit give you?", ["A plain 0 or 1", "A blend", "Both at once", "Nothing"], 0, "It lands like a coin."),
  ("How many numbers describe 3 qubits?", ["8", "3", "6", "9"], 0, "2 to the power 3."),
  ("Adding one qubit does what to the numbers needed?", ["Doubles them", "Adds one", "Halves them", "Nothing"], 0, "Powers of two."),
  ("Is a quantum computer better at everything?", ["No, only some jobs", "Yes", "It is slower at all", "Nobody knows"], 0, "Special jobs."),
  ("What is a simulator?", ["A normal computer pretending to be quantum", "A real quantum chip", "A game controller", "A battery"], 0, "That is what we use.")],
 [("Bit", "0 or 1"), ("Qubit", "A bit that can be a blend of 0 and 1"), ("Superposition", "A blend of states"), ("2 to the n", "Numbers needed for n qubits"), ("Simulator", "Software that acts like a quantum computer")],
 [MATCH("Match the word", "Pair each word with what it means.", [("Bit", "0 or 1"), ("Qubit", "A mix of 0 and 1"), ("Measurement", "Looking gives a plain answer"), ("Simulator", "Software pretending to be quantum")]),
  FILL("Bits and qubits", "A normal computer stores {{bits}}. A {{qubit}} can be a mix of 0 and 1. When you {{measure}} it you get a plain 0 or 1. The mix is called {{superposition}}."),
  PL("Count the numbers", "Write states(n): how many numbers describe n qubits? That is 2 to the power n.", "states(n)", '''
def states(n):
    return 2 ** n
''', [[1], [3], [10]], "Doubling for each qubit."),
  PL("Memory needed", "Each number takes 16 bytes. Write memory_bytes(n): bytes needed to store n qubits.", "memory_bytes(n)", '''
def memory_bytes(n):
    return 2 ** n * 16
''', [[10], [20], [30]], "2 to the n times 16."),
  PL("Coin chance", "Write coin_chance(heads, total): the fraction of heads, rounded to 2 decimals.", "coin_chance(heads, total)", '''
def coin_chance(heads, total):
    return round(heads / total, 2)
''', [[5, 10], [1, 3], [7, 20]], "Divide and round."),
  ORDER("Order the idea", "Put the life of a qubit in order.", ["Start as a plain 0", "Make a blend", "Measure it", "Get a plain 0 or 1"])]))

CHS.append(CH(
 "The qubit: states, amplitudes and measurement",
 ("Qubit", [
  "|0> | is | Plain zero",
  "|1> | is | Plain one",
  "Amplitude | squared gives | Probability",
  "State | holds | Two amplitudes",
  "Measurement | picks | 0 or 1",
  "Probabilities | add to | 1"]),
 ["A qubit state has two numbers called amplitudes, one for 0 and one for 1. Write the state as (a, b). The state |0> is (1, 0) and |1> is (0, 1).",
  "The chance of seeing 0 is a squared, and the chance of seeing 1 is b squared. This is the Born rule. The chances must add to 1, so the state is always scaled to fit.",
  "Measuring makes the qubit pick one answer using those chances, and afterwards it stays as that answer. The blend is gone. That is why you measure at the end of a circuit."],
 [("Amplitude", "A number attached to each outcome. Squared, it is the chance."),
  ("Born rule", "Chance of an outcome equals its amplitude squared."),
  ("Normalize", "Scale a state so the chances add up to 1."),
  ("Ket", "The bracket notation |0> for a state."),
  ("Collapse", "After measuring, the state becomes the answer you saw.")],
 ["State (a, b): amplitude a for 0, b for 1.",
  "Chance of 0 is a squared. Chance of 1 is b squared.",
  "Chances add up to exactly 1.",
  "Measuring picks one and the blend is gone.",
  "Amplitudes can be negative. Chances never are."],
 [T("Every qubit state is described by two amplitudes. Think of them as dials. One dial is for the answer 0 and one for the answer 1. A plain 0 has the first dial full and the second at zero."),
  T("To turn amplitudes into chances you square them. If the state is (0.7071, 0.7071), the chance of 0 is 0.7071 times 0.7071, which is about 0.5. The chance of 1 is also 0.5. That is a fair coin flip. This is called the Born rule."),
  C("a, b = 0.7071, 0.7071\nprint('chance of 0:', round(a * a, 2))\nprint('chance of 1:', round(b * b, 2))", "python"),
  T("Why square? Because amplitudes can be negative, and a chance cannot. Squaring makes every answer positive. Later you will see that the sign matters a lot, because amplitudes can cancel each other out."),
  T("Now try it yourself. The first lab in this chapter is our own Lilith Composer, powered by the Q.js engine. Tap the H gate, then tap a square on the wire. The bars show the chances. Then use the Q Console under the circuit: type H 1 and press Go."),
  APP("QPLAY", "Quantum playground", "Build circuits by tapping gates or typing commands in the Q Console. Press Run 100 shots to measure many times."),
  T("When you run shots, each shot is one full measurement. A coin that is 50 percent heads will not give exactly half every time, just like a real coin. More shots give numbers closer to the true chances.")],
 [("The state |1> has amplitudes:", ["(0, 1)", "(1, 0)", "(1, 1)", "(0, 0)"], 0, "Zero for 0, one for 1."),
  ("How do you get a chance from an amplitude?", ["Square it", "Double it", "Add one", "Take its sign"], 0, "The Born rule."),
  ("Amplitudes 0.7071 and 0.7071 give chances:", ["About 50 and 50 percent", "100 and 0", "70 and 70", "25 and 75"], 0, "0.5 each."),
  ("Do chances add up to 1?", ["Yes, always", "Only sometimes", "No", "Only for 1 qubit"], 0, "Something must happen."),
  ("After measuring, the qubit is:", ["Plain 0 or plain 1", "Still a blend", "Destroyed", "Random each time"], 0, "Collapse."),
  ("Can an amplitude be negative?", ["Yes", "No", "Only for 1", "Only for 0"], 0, "But chances are never negative.")],
 [("Born rule", "Chance = amplitude squared"), ("Collapse", "Measuring leaves a plain answer"), ("Normalize", "Scale chances to add to 1"), ("Ket", "|0> style label for a state")],
 [MATCH("Match the state", "Pair the state with what it is.", [("(1, 0)", "plain zero"), ("(0, 1)", "plain one"), ("(0.7071, 0.7071)", "fair coin"), ("(0.7071, -0.7071)", "fair coin with opposite sign")]),
  FILL("The Born rule", "The chance of an outcome is its amplitude {{squared}}. Measuring makes the blend {{collapse}}. The chances always add up to {{1}}."),
  PL("Two chances", "Write born(a, b): return [chance of 0, chance of 1] after scaling so they add to 1. Round both to 4 decimals.", "born(a, b)", '''
def born(a, b):
    t = a * a + b * b
    return [round(a * a / t, 4), round(b * b / t, 4)]
''', [[1, 0], [1, 1], [3, 4]], "Divide each square by the total."),
  PL("Normalize", "Write normalize(a, b): scale the pair so its squares add to 1. Return [a, b] rounded to 4 decimals.", "normalize(a, b)", '''
def normalize(a, b):
    n = (a * a + b * b) ** 0.5
    return [round(a / n, 4), round(b / n, 4)]
''', [[3, 4], [1, 1], [0, 5]], "Divide by the length."),
  PL("Measure once", "Write measure(p0, r): given the chance p0 of 0 and a random number r between 0 and 1, return 0 if r is less than p0, else 1.", "measure(p0, r)", '''
def measure(p0, r):
    if r < p0:
        return 0
    return 1
''', [[0.5, 0.3], [0.5, 0.7], [0.9, 0.95]], "A cut on the number line."),
  ORDER("Order the steps", "Put the steps of reading a qubit in order.", ["Write the amplitudes", "Square each amplitude", "Get the chances", "Measure to get one answer"])]))

CHS.append(CH(
 "One-qubit gates: X, H, Z and T",
 ("Gates", [
  "Gate | changes | A qubit state",
  "X gate | flips | 0 and 1",
  "H gate | makes | A blend",
  "Z gate | flips | The sign",
  "T gate | turns | Phase a little",
  "Gates | are | Reversible"]),
 ["A gate is a tiny step that changes a qubit. You build a quantum program by lining gates up on a wire, like beads on a string. Time moves left to right.",
  "X flips 0 and 1, like a NOT. H, the Hadamard, turns a plain 0 into a fair blend. Z flips the sign of the 1 amplitude, which you cannot see directly. T is a smaller sign turn, a quarter of a half-turn.",
  "Every gate can be undone, because it is reversible. Doing X twice is a no-op, and doing H twice gets you back where you started. That is one big difference from normal logic gates."],
 [("Gate", "A step that changes a qubit."),
  ("Hadamard (H)", "Makes an even blend from a plain 0 or 1."),
  ("Pauli X", "The NOT gate: swaps the 0 and 1 amplitudes."),
  ("Phase", "A hidden angle on the 1 amplitude."),
  ("Reversible", "Every gate can be undone.")],
 ["X swaps the two amplitudes.",
  "H turns (1,0) into (0.7071, 0.7071).",
  "Z negates the 1 amplitude. T turns the phase by a quarter step.",
  "H twice is the same as nothing.",
  "Gates are reversible, unlike measuring."],
 [T("X is the easiest gate. It swaps the two amplitudes. A plain 0 becomes a plain 1 and a plain 1 becomes a plain 0. Think of it as a flip switch."),
  T("H, called the Hadamard gate, is the star. Give it a plain 0 and it makes an equal blend. Measure that and you get a fair coin flip. In Q.js you write it as H. This is how you make your first superposition."),
  T("Z does not change the chances of a plain 0 or 1, so it looks like nothing happens. What it does is flip the sign of the 1 amplitude. The sign is called phase. You cannot see it directly, but it changes what the next gate does."),
  C("# the gates as number pairs\ndef x(s): return [s[1], s[0]]\ndef z(s): return [s[0], -s[1]]\nr = 0.7071\ndef h(s): return [r * (s[0] + s[1]), r * (s[0] - s[1])]\nprint(h([1, 0]))\nprint(h(h([1, 0])))", "python"),
  T("Look at that last line. H followed by H returns to the start. The second H cancels the first. This is the hint of something deeper that you will meet in the next chapter."),
  APP("QGATES", "Gate puzzles", "Solve the levels by tapping gates into the circuit, or type commands like H 1 into the Q Console. The shots and the bars show you what changes."),
  T("Tip: in the editor each column is one moment in time and each row is one qubit. You can type circuits in the Q Console too: H 1 adds an H on qubit 1 in the next free column.")],
 [("What does X do?", ["Swaps 0 and 1", "Makes a blend", "Measures", "Nothing"], 0, "A flip."),
  ("What does H do to a plain 0?", ["Makes a fair blend", "Makes 1", "Flips the sign", "Deletes it"], 0, "A coin flip."),
  ("What does H then H do?", ["Returns to the start", "Makes 1", "Makes a blend", "Breaks it"], 0, "They cancel."),
  ("What does Z change?", ["The sign of the 1 amplitude", "Nothing at all", "0 into 1", "The number of qubits"], 0, "Phase."),
  ("Are gates reversible?", ["Yes", "No", "Only X", "Only H"], 0, "Measurement is the one that is not."),
  ("In a circuit, time moves:", ["Left to right", "Right to left", "Top to bottom", "Nowhere"], 0, "Columns are moments.")],
 [("H", "Makes or undoes a blend"), ("X", "NOT: swaps 0 and 1"), ("Z", "Flips the sign of the 1"), ("T", "A quarter-step phase turn")],
 [MATCH("Match the gate", "Pair the gate with its job.", [("X", "Swaps 0 and 1"), ("H", "Makes a fair blend"), ("Z", "Flips the sign of 1"), ("T", "Small phase turn")]),
  FILL("Gate facts", "{{X}} flips 0 and 1. {{H}} makes a fair blend. {{Z}} flips the sign of the 1 amplitude. Every gate is {{reversible}}."),
  PL("Apply X", "Write apply_x(s): swap the two numbers of the state s and return a list.", "apply_x(s)", '''
def apply_x(s):
    return [s[1], s[0]]
''', [[[1, 0]], [[0, 1]], [[0.6, 0.8]]], "Swap them."),
  PL("Apply H", "Write apply_h(s): new state is [r*(a+b), r*(a-b)] with r = 0.70710678. Round both to 4 decimals.", "apply_h(s)", '''
def apply_h(s):
    r = 0.70710678
    return [round(r * (s[0] + s[1]), 4), round(r * (s[0] - s[1]), 4)]
''', [[[1, 0]], [[0, 1]], [[0.7071, 0.7071]]], "Sum and difference."),
  PL("Apply Z", "Write apply_z(s): keep the first number and flip the sign of the second.", "apply_z(s)", '''
def apply_z(s):
    return [s[0], 0 - s[1]]
''', [[[1, 0]], [[0, 1]], [[0.6, 0.8]]], "Negate the second."),
  PL("Run a gate string", "Write run_gates(g): start at [1, 0] and apply each letter of g (H, X or Z) in order. Return the chances of 0 and 1 as [p0, p1], rounded to 4 decimals. Use r = 0.70710678.", "run_gates(g)", '''
def run_gates(g):
    r = 0.70710678
    a, b = 1.0, 0.0
    for c in g:
        if c == 'X':
            a, b = b, a
        elif c == 'Z':
            b = 0 - b
        elif c == 'H':
            a, b = r * (a + b), r * (a - b)
    return [round(a * a, 4), round(b * b, 4)]
''', [["H"], ["HH"], ["X"], ["HZH"]], "Loop over the letters."),
  ORDER("Order the circuit", "Put these steps in order for making a fair coin from nothing.", ["Start with a plain 0", "Apply H", "Measure", "Read a fair random bit"])]))

CHS.append(CH(
 "Interference: the real power",
 ("Interference", [
  "Amplitudes | can | Add up",
  "Same sign | gives | Constructive",
  "Opposite sign | gives | Destructive",
  "Phase | decides | Which one",
  "H then H | returns | Start",
  "Algorithms | use | Interference"]),
 ["Amplitudes are like waves. Two waves that line up make a bigger wave. Two waves that are opposite cancel out to nothing. Quantum computers use exactly this.",
  "When two paths lead to the same answer, you add their amplitudes first, and then square. Same sign gives a bigger chance, called constructive interference. Opposite signs cancel, called destructive.",
  "That is the whole trick behind quantum speedups: use phases so that wrong answers cancel and the right answer grows. A coin cannot do this, because ordinary chances only add."],
 [("Interference", "Amplitudes adding or cancelling."),
  ("Constructive", "Same sign: the chance grows."),
  ("Destructive", "Opposite sign: the chance shrinks."),
  ("Phase", "The sign or angle of an amplitude."),
  ("Path", "One route a qubit could take to an answer.")],
 ["Add amplitudes, then square.",
  "Same sign grows. Opposite sign cancels.",
  "H, then Z, then H turns 0 into 1.",
  "H, then T, then H gives an in-between chance.",
  "Quantum speedups come from steering interference."],
 [T("Here is the experiment of the chapter. Start with a plain 0. Apply H to make a blend. Apply H again. The qubit returns to a plain 0 every time. Nothing random happened at all."),
  T("That is strange. After the first H you had a fair coin. A fair coin flipped by another fair coin should still be random. The reason it is not: the two paths to the answer 1 have opposite signs and cancel, and the two paths to 0 add up."),
  T("Now put a Z between the two H gates. Z flips a sign, so now the paths to 0 cancel and the paths to 1 add up. H then Z then H turns a plain 0 into a plain 1 with certainty. The phase is the steering wheel."),
  C("# H, then a phase turn of phi, then H\nimport math\nfor phi in (0, 90, 180):\n    p1 = math.sin(math.radians(phi) / 2) ** 2\n    print(phi, 'degrees gives chance of 1:', round(p1, 2))", "python"),
  T("With a phase of 0 you get 0 percent, with 180 degrees you get 100 percent, and with 90 degrees you get 50 percent. A phase of 180 degrees is exactly a Z gate. The T gate is 45 degrees. Try these in the labs."),
  T("This is why quantum computing needs careful design. You cannot just throw gates at a problem. You line up phases so that the wrong answers cancel. The next chapters build real examples.")],
 [("Two equal waves with the same sign make:", ["A bigger wave", "Nothing", "A smaller wave", "A random wave"], 0, "Constructive."),
  ("Two equal waves with opposite signs make:", ["Nothing", "A bigger wave", "Noise", "A copy"], 0, "Destructive."),
  ("What do H, H do to plain 0?", ["Return plain 0", "Make 1", "Make a coin", "Nothing works"], 0, "Cancelling paths."),
  ("What do H, Z, H do to plain 0?", ["Make plain 1", "Return plain 0", "Make a coin", "Break it"], 0, "Z flips the sign."),
  ("What does a phase of 180 degrees equal?", ["A Z gate", "An X gate", "An H gate", "Nothing"], 0, "A half-turn."),
  ("Why can a normal coin not do this?", ["Chances only add", "Coins are small", "Coins are random", "Coins cannot flip"], 0, "No cancelling.")],
 [("Constructive", "Same sign, chance grows"), ("Destructive", "Opposite sign, cancels"), ("Phase", "Hidden angle of an amplitude"), ("H-Z-H", "Turns 0 into 1")],
 [MATCH("Match the circuit", "Pair the circuit with the result for a plain 0.", [("H then H", "stays 0"), ("H then Z then H", "becomes 1"), ("X then X", "stays 0"), ("H then T then H", "an in-between chance")]),
  FILL("Interference", "Opposite amplitudes {{cancel}}. Same-sign amplitudes make a {{bigger}} chance. The sign is called the {{phase}}. A Z gate is a phase of {{180}} degrees."),
  PL("Add the paths", "Two paths lead to the same answer with amplitudes a and b. Write join(a, b): return the chance, which is (a + b) squared, rounded to 4 decimals.", "join(a, b)", '''
def join(a, b):
    return round((a + b) ** 2, 4)
''', [[0.5, 0.5], [0.5, -0.5], [0.3, 0.4]], "Add first, then square."),
  PL("H, phase, H", "Write p_one(phi): chance of 1 after H, a phase turn of phi degrees, and H. It equals sin of half the angle, squared. Use import math. Round to 4 decimals.", "p_one(phi)", '''
import math
def p_one(phi):
    return round(math.sin(math.radians(phi) / 2) ** 2, 4)
''', [[0], [90], [180], [60]], "Half the angle."),
  PL("Which interference", "Write kind(a, b): if a and b have the same sign return 'constructive', if opposite signs return 'destructive', if either is zero return 'none'.", "kind(a, b)", '''
def kind(a, b):
    if a == 0 or b == 0:
        return 'none'
    if (a > 0) == (b > 0):
        return 'constructive'
    return 'destructive'
''', [[1, 1], [1, -1], [0, 2], [-3, -2]], "Compare the signs."),
  ORDER("Order the idea", "Put the steps of an interference trick in order.", ["Make a blend with H", "Turn a phase on one path", "Combine the paths with another H", "The wrong answer cancels"])]))

CHS.append(CH(
 "Reading circuits and the text syntax",
 ("Circuits", [
  "Circuit | has | Rows and columns",
  "Row | is | A qubit",
  "Column | is | A moment",
  "I | means | Do nothing",
  "X#0 and X#1 | make | A CNOT",
  "Text | describes | A circuit"]),
 ["A quantum circuit is a grid. Each row is one qubit and each column is one moment in time. A gate sits where a row and a column meet. An empty spot is the identity, written I, which does nothing.",
  "Q.js lets you write a circuit as plain text. Gates in a row are joined with a dash, and rows are on separate lines. So H-X-I on one line means H, then X, then nothing.",
  "To link two qubits you tag gates with #. X#0 is the control and X#1 is its target, together a CNOT. Typing circuits as text is quick and easy to share."],
 [("Circuit", "A grid of gates on qubit wires."),
  ("Moment", "One column: things that happen at the same time."),
  ("Identity (I)", "A gate that does nothing."),
  ("Control", "The qubit that decides if the gate happens."),
  ("Target", "The qubit that gets changed.")],
 ["Rows are qubits. Columns are moments.",
  "I is a gate that does nothing.",
  "Separate gates in a row with a dash.",
  "X#0 and X#1 in one column form a CNOT.",
  "The Q Console builds circuits with commands such as H 1."],
 [T("Look at a circuit like a music sheet. The rows are instruments and the columns are beats. All gates in one column happen together. Moving to the next column moves time forward."),
  C("H-X-I\nI-I-H", "text"),
  T("That is a 2 qubit circuit. The first line is qubit 1 and the second is qubit 2. In the first moment qubit 1 gets an H. In the second moment qubit 1 gets an X. The third moment has nothing for qubit 1 and an H for qubit 2."),
  T("To make a CNOT, put X#0 on the control row and X#1 on the target row, in the same column. The CNOT flips the target only when the control is 1. Next chapter explains why it is special."),
  C("H-X#0\nI-X#1", "text"),
  T("You do not have to type this by hand. In the Q Console you can type H 1 and then CNOT 1 2, and the console writes the text for you. Type text to see it. The same text can go back into the editor."),
  T("Practice by reading. Every circuit you meet from now on is just this grid, so you can always tell what it does by reading left to right.")],
 [("What is a row in a circuit?", ["A qubit", "A moment", "A gate", "A bit of noise"], 0, "One wire each."),
  ("What is a column?", ["A moment in time", "A qubit", "A measurement", "A chip"], 0, "Gates in a column happen together."),
  ("What does I do?", ["Nothing", "Flips", "Blends", "Measures"], 0, "The identity."),
  ("What do X#0 and X#1 in one column make?", ["A CNOT", "Two X gates", "An H", "A swap"], 0, "Control and target."),
  ("Which qubit does a gate with #0 act as?", ["The control", "The target", "A bystander", "The output"], 0, "# zero is the control."),
  ("In H-X-I, what comes first?", ["H", "X", "I", "Nothing"], 0, "Left to right.")],
 [("Identity", "The gate I: does nothing"), ("Column", "One moment in time"), ("X#0 / X#1", "Control and target of a CNOT"), ("Circuit text", "Rows separated by new lines")],
 [MATCH("Match the symbol", "Pair each piece with its meaning.", [("I", "does nothing"), ("H", "makes a blend"), ("X#0", "control of a CNOT"), ("X#1", "target of a CNOT")]),
  FILL("Reading circuits", "Each row is a {{qubit}}. Each column is a {{moment}}. A gate written {{I}} does nothing. In text, gates in a row are joined with a {{dash}}."),
  PL("List the gates", "Write gate_list(text): return the gates in the circuit text in reading order, row by row, skipping I. Drop the # tag from each, so X#0 becomes X. Rows are on separate lines, gates joined by dashes.", "gate_list(text)", '''
def gate_list(text):
    out = []
    for row in text.split('\\n'):
        for tok in row.split('-'):
            tok = tok.strip()
            if tok and tok != 'I':
                out.append(tok.split('#')[0])
    return out
''', [["H-X-I"], ["H-X#0-I\nI-X#1-I"], ["I-I\nI-I"]], "Split, filter, clean."),
  PL("Circuit size", "Write size(text): return [number of qubits, number of moments]. Rows are lines, moments are the items in the first line.", "size(text)", '''
def size(text):
    rows = [r for r in text.split('\\n') if r.strip()]
    return [len(rows), len(rows[0].split('-'))]
''', [["H-X-I\nI-I-H"], ["H"], ["I-I-I-I\nI-I-I-I\nI-I-I-I"]], "Rows and the width of the first row."),
  PL("Count a gate", "Write count_gate(text, g): how many times the gate g appears. Ignore any # tag.", "count_gate(text, g)", '''
def count_gate(text, g):
    n = 0
    for row in text.split('\\n'):
        for tok in row.split('-'):
            if tok.strip().split('#')[0] == g:
                n += 1
    return n
''', [["H-H-X", "H"], ["H-X#0\nI-X#1", "X"], ["I-I", "H"]], "Loop and compare."),
  ORDER("Order the reading", "Put these in order for reading a circuit.", ["Find the rows", "Find the moments", "Read left to right", "Note which gates link rows"])]))
