# -*- coding: utf-8 -*-
"""Quantum computing for beginners, part 2: chapters 6-10."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=1000):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Two qubits: tensor products and CNOT",
 ("Two qubits", [
  "Two qubits | have | 4 amplitudes",
  "Tensor product | combines | Qubits",
  "CNOT | links | Two qubits",
  "Control | decides | If target flips",
  "Product state | is | Separate qubits",
  "States | are labelled | 00 01 10 11"]),
 ["Two qubits have four possible answers: 00, 01, 10 and 11. So a two qubit state is four amplitudes. In our composer the left bit is qubit 0, the top wire.",
  "If the qubits are separate, you can build the four amplitudes by multiplying: the tensor product. A, B gives a0 b0, a0 b1, a1 b0 and a1 b1. A state you can build this way is called a product state.",
  "The CNOT gate links two qubits. If the control is 1, it flips the target. If the control is 0, nothing happens. With H plus CNOT you can make states that are not product states."],
 [("Tensor product", "Multiplying amplitudes to combine separate qubits."),
  ("Product state", "A state of separate, unlinked qubits."),
  ("CNOT", "Flips the target if the control is 1."),
  ("Basis state", "A plain state such as 01."),
  ("Control", "The qubit that decides whether the target flips.")],
 ["Two qubits have 4 amplitudes, one per answer.",
  "Tensor product: multiply the amplitudes.",
  "CNOT swaps the amplitudes of 10 and 11.",
  "A state is a product if a0*d equals b*c for amplitudes a, b, c, d.",
  "Not every two qubit state is a product."],
 [T("One qubit has two answers, 0 and 1. Two qubits have four, written 00, 01, 10 and 11. The first digit is qubit 0. A state needs one amplitude for each, so four numbers. Three qubits would need eight."),
  T("If you set two qubits up separately, you can find the combined state by multiplying. Qubit 0 is (a0, a1) and qubit 1 is (b0, b1). The combined amplitudes are a0 times b0, a0 times b1, a1 times b0 and a1 times b1. This is the tensor product."),
  C("def tensor(a, b):\n    return [a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]]\nprint(tensor([1, 0], [0, 1]))   # 0 and 1 gives 01\nprint(tensor([0.7071, 0.7071], [1, 0]))", "python"),
  T("The CNOT gate has two inputs. If the control qubit is 0, it does nothing. If the control is 1, it flips the target. On the four amplitudes, that means the answers 10 and 11 swap. The other two stay."),
  C("def cnot(s):\n    return [s[0], s[1], s[3], s[2]]\nprint(cnot([0, 0, 1, 0]))  # 10 becomes 11", "python"),
  T("Try it in the lab: pick X and tap qubit 0, then CNOT from 0 to 1, and look at the chances. You should see 11. The CNOT copied the 1 from qubit 0 onto qubit 1."),
  T("Everything so far could be done by separate qubits. The next chapter shows how H and CNOT together make something new: the qubits can no longer be pulled apart.")],
 [("How many amplitudes describe 2 qubits?", ["4", "2", "3", "8"], 0, "00 01 10 11."),
  ("What does CNOT do when the control is 0?", ["Nothing", "Flips the target", "Measures", "Swaps"], 0, "No control, no change."),
  ("What does CNOT do when the control is 1?", ["Flips the target", "Nothing", "Flips both", "Erases"], 0, "Target flips."),
  ("What is the tensor product used for?", ["Combining separate qubits", "Measuring", "Making noise", "Undoing a gate"], 0, "Multiplying amplitudes."),
  ("Which two answers swap under CNOT?", ["10 and 11", "00 and 01", "00 and 11", "01 and 10"], 0, "Control is 1."),
  ("In the label 01, which is qubit 0?", ["The left digit", "The right digit", "Both", "Neither"], 0, "Our composer reads left first.")],
 [("Tensor product", "Combine by multiplying"), ("CNOT", "Flip target if control is 1"), ("Basis state", "A plain 00, 01, 10 or 11"), ("Product state", "Made of separate qubits")],
 [MATCH("Match the gate", "Pair each situation with what CNOT does.", [("control 0", "nothing happens"), ("control 1", "target flips"), ("00", "stays 00"), ("10", "becomes 11")]),
  FILL("Two qubits", "Two qubits have {{4}} amplitudes. The {{tensor}} product combines separate qubits. A {{CNOT}} flips the target when the control is 1."),
  PL("Tensor product", "Write tensor(a, b): the four amplitudes [a0*b0, a0*b1, a1*b0, a1*b1], rounded to 4 decimals.", "tensor(a, b)", '''
def tensor(a, b):
    return [round(a[0] * b[0], 4), round(a[0] * b[1], 4), round(a[1] * b[0], 4), round(a[1] * b[1], 4)]
''', [[[1, 0], [0, 1]], [[0.7071, 0.7071], [1, 0]], [[0, 1], [0.6, 0.8]]], "Multiply each pair."),
  PL("Apply CNOT", "Write cnot(s): s has 4 amplitudes. Swap the last two and return the new list.", "cnot(s)", '''
def cnot(s):
    return [s[0], s[1], s[3], s[2]]
''', [[[1, 0, 0, 0]], [[0, 0, 1, 0]], [[0.5, 0.5, 0.5, 0.5]]], "Swap positions 2 and 3."),
  PL("Label a state", "Write label(i, n): the binary label of number i using n digits. For example label(2, 2) is '10'.", "label(i, n)", '''
def label(i, n):
    s = ''
    for _ in range(n):
        s = str(i % 2) + s
        i = i // 2
    return s
''', [[2, 2], [5, 3], [0, 4]], "Peel off bits."),
  PL("Is it a product?", "Write is_product(s): s has 4 amplitudes. A state is a product if s0*s3 equals s1*s2 (round both to 4 decimals). Return True or False.", "is_product(s)", '''
def is_product(s):
    return round(s[0] * s[3], 4) == round(s[1] * s[2], 4)
''', [[[1, 0, 0, 0]], [[0.7071, 0, 0, 0.7071]], [[0.5, 0.5, 0.5, 0.5]]], "Cross multiply."),
  ORDER("Order the steps", "Put the steps of a CNOT in order.", ["Look at the control", "Control is 1", "Flip the target", "Control is 0 means nothing changes"])]))

CHS.append(CH(
 "Entanglement and Bell states",
 ("Entanglement", [
  "H then CNOT | makes | Bell state",
  "Bell state | is | Entangled",
  "Entangled | means | Linked outcomes",
  "Measure one | tells you | The other",
  "GHZ | is | Three qubit Bell",
  "Entanglement | is not | Messaging"]),
 ["Entanglement is when qubits are linked so tightly that you cannot describe one without the others. The famous recipe: put H on qubit 0, then a CNOT from 0 to 1.",
  "The result is the Bell state. It is half 00 and half 11. Measure it and you get 00 or 11, each 50 percent of the time, never 01 or 10. Each qubit alone is a fair coin, but the two coins always agree.",
  "Entanglement does not send messages faster than light. The results look random to each side. You only see the link when you compare them afterwards."],
 [("Entanglement", "Qubits linked so they cannot be described separately."),
  ("Bell state", "The two-qubit entangled state made with H and CNOT."),
  ("Correlated", "Outcomes that agree or match."),
  ("GHZ state", "A three-qubit entangled state: all 0 or all 1."),
  ("Product state", "A state that is not entangled.")],
 ["H on qubit 0, then CNOT 0 to 1, makes a Bell state.",
  "Bell outcomes: 00 or 11, 50 percent each.",
  "Each qubit alone looks like a fair coin.",
  "The two coins always agree.",
  "No message is sent: the results are random until compared."],
 [T("Here is the recipe. Start with two plain 0 qubits. Put an H on qubit 0. Now qubit 0 is a blend. Add a CNOT with qubit 0 as the control and qubit 1 as the target. The control is a blend, so the target is a blend too, and they are tied together."),
  T("The state is now half 00 and half 11. If you measure qubit 0 and see 0, qubit 1 will be 0. If you see 1, qubit 1 will be 1. Each coin alone is perfectly random, yet the two always agree."),
  T("This cannot be a product state. A product state has a0 times d equal to b times c. Here the amplitudes are 0.7071, 0, 0, 0.7071. The first times the last is 0.5, but the middle two give 0. They do not match, so this state is entangled."),
  C("def bell(i):\n    r = 0.7071\n    s = [0, 0, 0, 0]\n    s[i] = 1\n    s = [r*(s[0]+s[2]), r*(s[1]+s[3]), r*(s[0]-s[2]), r*(s[1]-s[3])]  # H on qubit 0\n    return [s[0], s[1], s[3], s[2]]                                    # CNOT\nprint(bell(0))", "python"),
  T("Time for the lab in the practice section. Solve the levels: copy a bit with CNOT, make a Bell pair, make the opposite pair, and build a three-qubit GHZ state. In the Q Console you can type new 3, h 0, cx 0 1, cx 1 2 and explain."),
  APP("QENT", "Entanglement lab", "Make entangled pairs with the editor or the Q Console. After CNOT, type explain and the console will tell you if the qubits are entangled."),
  T("One more myth to bust. Entanglement is not a phone line. If you are far away from your friend and you measure your qubit, you see a random result. It only shows a pattern when you later compare results. That is why it cannot send messages.")],
 [("What makes a Bell state?", ["H then CNOT", "X then X", "Z then Z", "Two H gates"], 0, "A blend plus a link."),
  ("Bell state results are:", ["00 or 11", "01 or 10", "Any of four", "Only 00"], 0, "They always agree."),
  ("Each qubit alone looks like:", ["A fair coin", "A plain 0", "A plain 1", "Nothing"], 0, "50 percent."),
  ("Can entanglement send messages faster than light?", ["No", "Yes", "Sometimes", "Only with Bell states"], 0, "Results look random alone."),
  ("A GHZ state of 3 qubits gives:", ["000 or 111", "Any of 8", "001 or 110", "Only 000"], 0, "All agree."),
  ("An entangled state is:", ["Not a product state", "A plain state", "A noisy state", "A measured state"], 0, "Cannot be separated.")],
 [("Bell state", "H plus CNOT on 00"), ("GHZ", "Three entangled qubits: 000 or 111"), ("Correlation", "Results that agree"), ("No messaging", "Entanglement alone sends no message")],
 [MATCH("Match the state", "Pair each circuit with its outcomes.", [("H, CNOT", "00 or 11"), ("X, then CNOT", "11"), ("H on 0 only", "0 or 1 on qubit 0"), ("H, CNOT, CNOT on 3 qubits", "000 or 111")]),
  FILL("Entanglement", "An H and a {{CNOT}} make a {{Bell}} state. The two coins always {{agree}}. It cannot send {{messages}}."),
  PL("Make a Bell state", "Start with the plain state at index i of 4 (a 1 at position i). Apply H to qubit 0 (pairs index 0 with 2, and 1 with 3: new0=r*(s0+s2), new1=r*(s1+s3), new2=r*(s0-s2), new3=r*(s1-s3), r=0.70710678), then CNOT (swap last two). Write bell(i) and round to 4 decimals.", "bell(i)", '''
def bell(i):
    r = 0.70710678
    s = [0, 0, 0, 0]
    s[i] = 1
    s = [r * (s[0] + s[2]), r * (s[1] + s[3]), r * (s[0] - s[2]), r * (s[1] - s[3])]
    s = [s[0], s[1], s[3], s[2]]
    return [round(x, 4) for x in s]
''', [[0], [1], [2], [3]], "H then swap the last two."),
  PL("Do they agree?", "Write agree(samples): samples is a list of two-digit strings like '00' or '01'. Return the fraction where both digits match, rounded to 2 decimals.", "agree(samples)", '''
def agree(samples):
    n = 0
    for s in samples:
        if s[0] == s[1]:
            n += 1
    return round(n / len(samples), 2)
''', [[["00", "11", "11", "00"]], [["00", "01", "10", "11"]], [["01", "10"]]], "Count the matches."),
  PL("GHZ chances", "Write ghz(n): return the list [['0'*n, 0.5], ['1'*n, 0.5]], the two possible results of an n qubit GHZ state.", "ghz(n)", '''
def ghz(n):
    return [['0' * n, 0.5], ['1' * n, 0.5]]
''', [[2], [3], [5]], "All zeros or all ones."),
  PL("Tally the shots", "Write tally(samples): count each result and return a sorted list of [result, count] pairs.", "tally(samples)", '''
def tally(samples):
    d = {}
    for s in samples:
        d[s] = d.get(s, 0) + 1
    return sorted([[k, v] for k, v in d.items()])
''', [[["00", "11", "11", "00", "11"]], [["01"]], [["a", "b", "a"]]], "A dictionary of counts."),
  ORDER("Order the recipe", "Put the Bell state recipe in order.", ["Start with two plain 0 qubits", "Apply H to qubit 0", "Apply CNOT from 0 to 1", "Measure: 00 or 11"])]))

CHS.append(CH(
 "Small algorithms: Deutsch and Grover",
 ("Algorithms", [
  "Oracle | hides | A secret",
  "Deutsch | asks | Constant or balanced",
  "One query | is enough | For Deutsch",
  "Grover | finds | A marked item",
  "Grover | needs | About root N steps",
  "Phase | marks | The answer"]),
 ["An oracle is a black box that hides a secret function. Deutsch's problem: is the hidden rule constant (same answer for both inputs) or balanced (different answers)? A normal computer must ask twice. A quantum circuit can ask once.",
  "Grover's search finds a marked item in an unsorted list of N items. A normal computer needs about N over 2 tries on average. Grover needs about the square root of N steps. For a million items that is about a thousand steps instead of half a million.",
  "Both use the interference you learned: the oracle marks the answer with a phase, and the other gates make wrong answers cancel and the right one grow."],
 [("Oracle", "A black box that holds a secret rule."),
  ("Constant function", "Gives the same answer for every input."),
  ("Balanced function", "Gives 0 for half the inputs and 1 for the other half."),
  ("Grover search", "A quantum search that takes about the square root of N steps."),
  ("Speedup", "Fewer steps needed than the best normal way.")],
 ["Deutsch: one oracle query tells constant from balanced.",
  "Grover: about the square root of N steps for N items.",
  "Both mark answers with a phase and interfere.",
  "Grover's speedup is quadratic, not magic.",
  "You can build 2 qubit Grover in the lab."],
 [T("Imagine a secret rule that takes a 0 or a 1 and gives back a 0 or a 1. There are four possible rules. Two are constant: always 0 or always 1. Two are balanced: copy the input, or flip it. You must find out which kind it is."),
  T("A normal computer must ask the rule twice, once for 0 and once for 1, to compare the answers. Deutsch's circuit asks once. It puts the input in a blend, asks the oracle, and then lets the two paths interfere. If the rule is constant the answer is 0, if balanced the answer is 1."),
  C("def deutsch(f0, f1):\n    a0 = ((-1) ** f0 + (-1) ** f1) / 2\n    p0 = a0 * a0\n    return 'constant' if p0 > 0.5 else 'balanced'\nprint(deutsch(0, 0), deutsch(0, 1))", "python"),
  T("Grover's search is the more useful one. Take 4 hidden boxes and one of them has a prize. A normal computer checks boxes one at a time. Grover starts with an even blend of all boxes, marks the prize with a phase, and then does a reflection that makes the prized box more likely."),
  T("For 4 items one round makes the prize certain. For larger lists you repeat the round about pi over 4 times the square root of N times. Do too few rounds and the prize is not yet likely. Do too many and it fades again. It rotates like a clock hand."),
  C("import math\nN = 16\nk = int(math.pi / 4 * math.sqrt(N))\nprint('rounds:', k)\ntheta = math.asin(1 / math.sqrt(N))\nprint('chance of prize:', round(math.sin((2 * k + 1) * theta) ** 2, 3))", "python"),
  APP("QALGO", "Algorithm lab", "Run Deutsch and Grover circuits yourself. The Q Console can build them: try new 2, H 1, H 2, CZ 1 2 and run to see the first steps."),
  T("Nobody gets to skip checking. Real Grover circuits include an oracle and a flip around the average. The lab gives you ready circuits to experiment with so you can see the answer rise.")],
 [("What is an oracle?", ["A black box with a secret rule", "A quantum computer", "A gate", "A qubit"], 0, "You only ask it."),
  ("How many oracle queries does Deutsch need?", ["1", "2", "4", "8"], 0, "A normal computer needs 2."),
  ("A constant function:", ["Gives the same answer every time", "Gives half 0 half 1", "Is random", "Has no answer"], 0, "Always 0 or always 1."),
  ("Grover search takes about:", ["Square root of N steps", "N steps", "N squared steps", "1 step"], 0, "A quadratic speedup."),
  ("What happens if you run Grover too many times?", ["The answer fades again", "It stays perfect", "It crashes", "It gets faster"], 0, "It rotates past."),
  ("How is the answer marked?", ["With a phase", "With a colour", "With a measurement", "With a copy"], 0, "A sign flip.")],
 [("Oracle", "A hidden rule you can only query"), ("Deutsch", "Constant or balanced with one query"), ("Grover", "Search in about root N steps"), ("Phase marking", "Flip the sign of the answer")],
 [MATCH("Match the idea", "Pair each term with its meaning.", [("Oracle", "hidden rule"), ("Constant", "same answer always"), ("Balanced", "half 0 and half 1"), ("Grover", "quantum search")]),
  FILL("Algorithms", "{{Deutsch}} tells constant from balanced with one query. {{Grover}} search takes about the square {{root}} of N steps. The answer is marked with a {{phase}}."),
  PL("Deutsch's answer", "A rule gives f0 for input 0 and f1 for input 1. Write deutsch(f0, f1): compute a0 = ((-1)**f0 + (-1)**f1) / 2, p0 = a0 times a0, and return 'constant' if p0 is more than 0.5, else 'balanced'.", "deutsch(f0, f1)", '''
def deutsch(f0, f1):
    a0 = ((-1) ** f0 + (-1) ** f1) / 2
    p0 = a0 * a0
    if p0 > 0.5:
        return 'constant'
    return 'balanced'
''', [[0, 0], [1, 1], [0, 1], [1, 0]], "Cancelling or adding."),
  PL("Grover rounds", "Write rounds(n): the number of Grover rounds for n qubits, int(3.14159265 / 4 * sqrt(N)) where N = 2**n. Use ** 0.5 for the square root.", "rounds(n)", '''
def rounds(n):
    N = 2 ** n
    return int(3.14159265 / 4 * N ** 0.5)
''', [[2], [4], [10], [20]], "Quarter pi times root N."),
  PL("Grover chance", "Write grover(N, k): chance of finding the prize in a list of N items after k rounds. With theta = asin(1/sqrt(N)), chance = sin((2k+1)*theta) squared. Use import math. Round to 4 decimals.", "grover(N, k)", '''
import math
def grover(N, k):
    theta = math.asin(1 / math.sqrt(N))
    return round(math.sin((2 * k + 1) * theta) ** 2, 4)
''', [[4, 1], [8, 1], [8, 2], [16, 3]], "A rotating arrow."),
  PL("Normal search", "Write classic(n): average number of checks to find one of n items by looking one at a time, that is (n + 1) / 2, rounded to 1 decimal.", "classic(n)", '''
def classic(n):
    return round((n + 1) / 2, 1)
''', [[4], [100], [1000000]], "Halfway on average."),
  ORDER("Order Grover", "Put the steps of Grover's search in order.", ["Make an even blend of all items", "Mark the answer with a phase", "Reflect to boost the answer", "Repeat about root N times, then measure"])]))

CHS.append(CH(
 "Noise, shots and real hardware",
 ("Real quantum computers", [
  "Shots | repeat | Measurements",
  "More shots | give | Better estimates",
  "Noise | causes | Errors",
  "Decoherence | loses | Quantum state",
  "Error correction | uses | Extra qubits",
  "Simulator | needs | 2^n memory"]),
 ["Real quantum chips are fragile. Heat, vibration and stray signals disturb qubits and make mistakes. This is noise, and the loss of the quantum blend is called decoherence. Many chips work near absolute zero.",
  "Because one measurement gives one random answer, you run the circuit many times. Each run is a shot. A hundred shots show you the chances roughly, a thousand show more. The error shrinks with the square root of the shots.",
  "A normal computer can simulate a quantum one, but it needs 2 to the n numbers. Around 30 qubits fills a normal PC and around 50 fills a supercomputer. That is exactly why real hardware is interesting."],
 [("Shot", "One run of the circuit with one measurement."),
  ("Noise", "Unwanted disturbance that causes errors."),
  ("Decoherence", "The qubit losing its quantum blend."),
  ("Error correction", "Using many noisy qubits to make one reliable one."),
  ("Standard error", "How far a measured chance is likely to be from the true one.")],
 ["A shot is one run and one measurement.",
  "Estimates improve with the square root of the shots.",
  "Noise and decoherence cause errors.",
  "Error correction needs many extra qubits.",
  "Simulating n qubits needs 2^n numbers."],
 [T("When you ran 100 shots earlier, you noticed that the Bell state did not give exactly 50 and 50. That is not a bug. Each shot is one random measurement, like a coin flip, so the totals wobble around the true chances."),
  T("How big is the wobble? About the square root of p times one minus p, divided by the square root of shots. For a fair coin and 100 shots that is about 0.05, or 5 percent. For 10,000 shots it is 0.005. To be 10 times more accurate you need 100 times more shots."),
  C("shots = 100\np = 0.5\nerr = (p * (1 - p) / shots) ** 0.5\nprint('standard error:', round(err, 3))", "python"),
  T("On real hardware the picture is messier. Gates are not perfect, qubits slowly lose their blend, and measurement can read the wrong answer. Today's machines have dozens to hundreds of noisy qubits, and engineers are working on error correction."),
  T("Error correction spreads one reliable qubit across many noisy ones, similar to how you repeat a message three times so one smudge does not matter. It is a big engineering goal, and useful big machines need it."),
  T("Finally, why a simulator is limited. Every qubit you add doubles the memory. At 16 bytes per number, 30 qubits need 16 gigabytes. 40 qubits need 16 terabytes. That is why a simulator like our lab is great for learning on small circuits, but real chips are needed for large ones.")],
 [("What is a shot?", ["One run and one measurement", "A gate", "A qubit", "A noise"], 0, "Repeat to see chances."),
  ("More shots make the estimate:", ["More accurate", "Less accurate", "The same", "Random"], 0, "Smaller wobble."),
  ("What is decoherence?", ["Losing the quantum blend", "Adding a qubit", "A fast gate", "A shot"], 0, "Noise breaks it."),
  ("What does error correction use?", ["Many extra qubits", "Fewer qubits", "Bigger shots", "A calculator"], 0, "Redundancy."),
  ("How much memory does 30 qubits need at 16 bytes?", ["16 gigabytes", "16 kilobytes", "1 megabyte", "480 bytes"], 0, "2^30 times 16."),
  ("To be 10 times more accurate you need:", ["100 times more shots", "10 times more shots", "Twice the shots", "One shot"], 0, "Square root.")],
 [("Shot", "One run"), ("Decoherence", "Quantum blend fades"), ("Error correction", "Many noisy qubits make one good one"), ("2 to the n", "Memory growth of a simulator")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Shot", "one run"), ("Noise", "unwanted errors"), ("Decoherence", "blend fades"), ("Error correction", "extra qubits for safety")]),
  FILL("Real hardware", "Each {{shot}} is one run. More shots give a smaller {{error}}. {{Noise}} makes real chips make mistakes. A simulator needs {{memory}} that doubles with every qubit."),
  PL("Standard error", "Write std_error(p, shots): sqrt(p * (1 - p) / shots), rounded to 4 decimals. Use ** 0.5.", "std_error(p, shots)", '''
def std_error(p, shots):
    return round((p * (1 - p) / shots) ** 0.5, 4)
''', [[0.5, 100], [0.5, 10000], [0.1, 400]], "The wobble."),
  PL("How many shots", "Write shots_needed(p, err): the number of shots so the standard error is at most err. Compute v = p*(1-p)/(err*err), round v to 6 decimals, then round up to a whole number.", "shots_needed(p, err)", '''
def shots_needed(p, err):
    v = round(p * (1 - p) / (err * err), 6)
    n = int(v)
    if n < v:
        n += 1
    return n
''', [[0.5, 0.05], [0.5, 0.01], [0.1, 0.02]], "Round up."),
  PL("A noisy chance", "A qubit flips with chance f by mistake. If the true chance of 1 is p, the measured chance is p*(1-f) + (1-p)*f. Write noisy(p, f) rounded to 4 decimals.", "noisy(p, f)", '''
def noisy(p, f):
    return round(p * (1 - f) + (1 - p) * f, 4)
''', [[1, 0.05], [0, 0.05], [0.5, 0.2]], "Two ways to read a 1."),
  PL("Biggest simulator", "Write max_qubits(gb): the largest n so that 2**n * 16 bytes fits in gb gigabytes (1 gigabyte is 1024**3 bytes).", "max_qubits(gb)", '''
def max_qubits(gb):
    n = 0
    while 2 ** (n + 1) * 16 <= gb * 1024 ** 3:
        n += 1
    return n
''', [[1], [16], [64]], "Grow n until it no longer fits."),
  ORDER("Order the measurement", "Put the steps of estimating a chance in order.", ["Build the circuit", "Run many shots", "Count each result", "Divide by the number of shots"])]))

CHS.append(CH(
 "Uses, myths and where to go next",
 ("Where next", [
  "Shor | breaks | Big numbers",
  "Quantum | helps | Some problems",
  "Chemistry | needs | Simulation",
  "Grover | gives | Root speedup",
  "Myths | include | Tries all answers",
  "Next | is | Learn and play"]),
 ["Quantum computers are expected to help with a few kinds of problems: simulating molecules and materials, searching, and breaking some codes. Shor's algorithm can factor large numbers much faster than known normal methods.",
  "That is why people are building new codes that resist quantum attacks. Everyday tasks like browsing, email, games and spreadsheets will not get faster. Quantum computers are co-processors for special jobs.",
  "To keep going: play with the Quantum Web Lab, try IBM Quantum and other free cloud services, follow Qiskit and Cirq tutorials, and read about the linear algebra under the hood. You already know the key ideas."],
 [("Shor's algorithm", "A quantum method for factoring big numbers."),
  ("Post-quantum", "Codes designed to resist quantum computers."),
  ("Quantum chemistry", "Simulating molecules, a natural quantum job."),
  ("Qiskit", "An open source quantum programming toolkit."),
  ("Co-processor", "A helper chip used for special tasks.")],
 ["Shor factors big numbers quickly.",
  "Grover gives a square root speedup for search.",
  "Chemistry and materials are natural uses.",
  "A quantum computer will not speed up everyday apps.",
  "Keep learning with simulators and cloud tools."],
 [T("What could a large reliable quantum computer do? The most natural job is simulating nature, because nature is quantum. That might mean better batteries, medicines and fertilizers. A normal computer struggles because the numbers double with every particle."),
  T("Shor's algorithm factors a large number into primes. Today's internet security often relies on factoring being hard. A big enough quantum computer would break some of it. The reply is new encryption that quantum computers cannot break, and it is already being rolled out."),
  C("def factor(n):\n    out = []\n    d = 2\n    while d * d <= n:\n        while n % d == 0:\n            out.append(d)\n            n //= d\n        d += 1\n    if n > 1:\n        out.append(n)\n    return out\nprint(factor(221))", "python"),
  T("The code above factors by trying every divisor. It is fine for small numbers and hopeless for numbers hundreds of digits long. Shor's trick is to find a repeating pattern using interference, and from the pattern it works out the factors."),
  T("Common myths. A quantum computer does not try every answer at once and pick the best. It is not a faster laptop. It cannot send messages faster than light. And it is not here to replace your phone."),
  T("You now know qubits, amplitudes, gates, interference, entanglement and a little of two algorithms. Keep playing. Build a circuit, guess the result before you run it, and see if you were right. That is how real quantum programmers learn.")],
 [("What is Shor's algorithm for?", ["Factoring big numbers", "Sorting", "Searching a list", "Making games"], 0, "It threatens some codes."),
  ("Will a quantum computer speed up email?", ["No", "Yes", "Greatly", "Only on Mondays"], 0, "Special jobs only."),
  ("Which job is natural for quantum computers?", ["Simulating molecules", "Playing music", "Showing photos", "Typing"], 0, "Nature is quantum."),
  ("What is post-quantum cryptography?", ["Codes that resist quantum attacks", "Faster internet", "A new qubit", "A simulator"], 0, "Preparing early."),
  ("Does a quantum computer try every answer at once?", ["No", "Yes", "Only in labs", "Only with H"], 0, "That is a myth."),
  ("Where can you keep learning?", ["Quantum Web Lab, Qiskit and cloud tools", "Nowhere", "Only books", "Only a lab"], 0, "Many free options.")],
 [("Shor", "Factoring algorithm"), ("Post-quantum", "Codes safe against quantum computers"), ("Qiskit", "Open source quantum toolkit"), ("Myth", "Tries every answer at once")],
 [MATCH("Match the idea", "Pair each idea with what it is about.", [("Shor", "factoring"), ("Grover", "search"), ("Chemistry", "simulating molecules"), ("Post-quantum", "safe codes")]),
  FILL("Where next", "{{Shor}} factors large numbers. {{Grover}} speeds up search. Quantum computers are {{special}} helpers, not faster laptops. Keep learning with {{simulators}}."),
  PL("Find the factors", "Write factor(n): the list of prime factors of n in increasing order, for example factor(12) is [2, 2, 3].", "factor(n)", '''
def factor(n):
    out = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out
''', [[15], [21], [91], [221]], "Trial division."),
  PL("Greatest common divisor", "Shor uses gcd. Write gcd(a, b) with Euclid's method.", "gcd(a, b)", '''
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
''', [[12, 18], [35, 64], [221, 13]], "Remainders."),
  PL("Square root speedup", "Write steps(n): [normal steps, Grover steps] to search n items, normal is n, Grover is int(n ** 0.5).", "steps(n)", '''
def steps(n):
    return [n, int(n ** 0.5)]
''', [[100], [10000], [1000000]], "n versus root n."),
  PL("Judge the job", "Write helps(job): return 'big speedup' for 'factoring' and 'chemistry', 'square root speedup' for 'search', and 'no help' for anything else.", "helps(job)", '''
def helps(job):
    if job in ('factoring', 'chemistry'):
        return 'big speedup'
    if job == 'search':
        return 'square root speedup'
    return 'no help'
''', [["factoring"], ["search"], ["email"], ["chemistry"]], "A small lookup."),
  ORDER("Order your path", "Put a good learning path in order.", ["Play with the Quantum Web Lab", "Learn the gates and interference", "Try small algorithms", "Run on a cloud quantum computer"])]))
