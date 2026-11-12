# -*- coding: utf-8 -*-
"""Hierarchical concept maps for the quantum course: one root, branches, leaves, and a few cross links.
Chapter numbers in [chN] tags follow the course order."""
def M(title, text):
    return (title, [ln.strip() for ln in text.strip().split("\n") if ln.strip()])

STRUCT = [
 M("Quantum mechanics", """
Quantum mechanics | rests on | Packets
Quantum mechanics | rests on | Waves
Quantum mechanics | rests on | Peeking
Packets | means | Light comes in quanta
Packets | shown by | Photons
Waves | means | Things spread out
Waves | shown by | Two slits
Peeking | means | Looking changes things
Peeking | shown by | Polarizer filters
Polarizer filters | lead to | Qubits [ch3]
Waves | explain | Interference [ch5]
Looking changes things | is called | Measurement [ch3]
"""),
 M("Bits and qubits", """
Bits and qubits | include | Bit
Bits and qubits | include | Qubit [ch3]
Bits and qubits | include | Chance
Bit | is | Definitely 0 or 1
Bit | n bits hold | One value at a time
Qubit [ch3] | is | Two amplitudes
Qubit [ch3] | n qubits need | 2 to the n numbers
Chance | comes from | Squaring amplitudes
Chance | is seen by | Measuring many times
Chance | is carried by | Qubit [ch3]
"""),
 M("A qubit", """
A qubit | has | Amplitudes
A qubit | has | A measurement
A qubit | can be | Plain 0 or 1
Amplitudes | are | Two numbers a and b
Amplitudes | can be | Negative
Negative | leads to | Phase [ch5]
A measurement | gives | One answer
A measurement | chance is | Amplitude squared
Amplitude squared | adds up to | 100 percent
Plain 0 or 1 | gives | A certain result
Plain 0 or 1 | are the poles of | Bloch sphere [ch6]
Amplitudes | squared give | Amplitude squared
"""),
 M("One-qubit gates", """
One-qubit gates | include | X gate
One-qubit gates | include | H gate
One-qubit gates | include | Z gate
One-qubit gates | include | T gate
X gate | flips | 0 and 1
H gate | makes | A fair blend
H gate | twice gives | The start again
Z gate | flips | The sign only
Z gate | steers | Phase [ch5]
T gate | is | An eighth turn
T gate | four of them make | A Z gate
H gate | sets up | Interference [ch5]
T gate | is a turn on | Bloch sphere [ch6]
"""),
 M("Interference", """
Interference | needs | Paths
Interference | needs | Phase
Interference | can be | Constructive
Interference | can be | Destructive
Interference | shown by | H then Z then H
Paths | are | Routes to an answer
Paths | combine by | Add first then square
Phase | is | The sign or angle
Phase | set by | Z S and T gates
Constructive | means | Same sign, bigger chance
Destructive | means | Opposite sign, cancels
H then Z then H | turns | 0 into 1
Phase | decides | Constructive
Phase | decides | Destructive
"""),
 M("Bloch sphere", """
Bloch sphere | shows | Height
Bloch sphere | shows | Round
Bloch sphere | shows | Poles
Bloch sphere | shows | Turns
Bloch sphere | warns with | A short arrow
Height | sets | Chance of 1
Round | is | Phase
Poles | north is | Plain 0
Poles | south is | Plain 1
Poles | middle is | Fair blends
Turns | X Y Z are | Half turns
Turns | S and T are | Quarter and eighth turns
Turns | H is | A slanted half turn
A short arrow | means | Entangled qubit [ch9]
Round | is set by | Z S and T gates
"""),
 M("A circuit", """
A circuit | has | Rows
A circuit | has | Columns
A circuit | has | Gates
Rows | are | Qubit wires
Rows | top row is | Qubit 0
Columns | are | Steps in time
Columns | are read | Left to right
Gates | are drawn as | Boxes
Gates | I means | A rest
Gates | written as | Q text like H-X-I
Q text like H-X-I | converts to | OpenQASM [ch12]
"""),
 M("Two qubits", """
Two qubits | have | Four answers
Two qubits | combine by | Tensor product
Two qubits | link with | CNOT
Four answers | are | 00 01 10 and 11
Four answers | need | Four amplitudes
Tensor product | joins | Separate qubits
Tensor product | multiplies | Their amplitudes
CNOT | has a | Control qubit
CNOT | has a | Target qubit
Control qubit | if 1 | Target flips
CNOT | leads to | Entanglement [ch9]
Tensor product | cannot make | Entanglement [ch9]
"""),
 M("Entanglement", """
Entanglement | is made by | H then CNOT
Entanglement | gives | A Bell pair
Entanglement | has | Myths
Entanglement | grows into | GHZ states
H then CNOT | blends | The control qubit
H then CNOT | binds | The target qubit
A Bell pair | shows | 00 or 11
A Bell pair | never shows | 01 or 10
A Bell pair | alone is | A fair coin
Myths | it is not | A phone line
Myths | is seen as | A short Bloch arrow [ch6]
A Bell pair | is made of | Two qubits [ch8]
"""),
 M("Quantum algorithms", """
Quantum algorithms | include | Deutsch
Quantum algorithms | include | Grover
Deutsch | asks | One question, not two
Deutsch | finds | Constant or balanced
Deutsch | uses | Interference [ch5]
Grover | searches | A marked item
Grover | step 1 | Mark the item
Grover | step 2 | Mirror about the average
Grover | step 3 | Measure
Grover | speeds up by | A square root
Grover | uses | Interference [ch5]
Grover | is checked with | Shots [ch11]
"""),
 M("Real hardware", """
Real hardware | has | Noise
Real hardware | needs | Shots
Real hardware | needs | Error correction
Real hardware | is checked on | A simulator
Noise | comes from | Imperfect gates
Noise | comes from | Fragile qubits
Shots | are | Repeated runs
Shots | give | Counts
Counts | wobble | Less with more shots
Error correction | spreads | One qubit over many
Error correction | needs | Many noisy qubits
A simulator | needs | Memory that doubles per qubit
Shots | match | Bell pair counts [ch9]
"""),
 M("OpenQASM file", """
OpenQASM file | starts with | A header
OpenQASM file | then has | Declarations
OpenQASM file | then has | Gate lines
OpenQASM file | comes in | Version 2
OpenQASM file | comes in | Version 3
A header | names | The version
A header | includes | stdgates.inc
Declarations | such as | qubit[2] q
Declarations | such as | bit[2] c
Gate lines | such as | h q[0]
Gate lines | such as | cx q[0], q[1]
Version 2 | writes | qreg and creg
Version 3 | writes | qubit and bit
Gate lines | match | Circuit columns [ch7]
"""),
 M("Qiskit", """
Qiskit | step 1 | Build
Qiskit | step 2 | Transpile
Qiskit | step 3 | Run
Qiskit | step 4 | Read
Qiskit | has a trap | Qubit 0 on the right
Qiskit | has a small cousin | MicroQiskit
Build | uses | QuantumCircuit
QuantumCircuit | exports | OpenQASM [ch12]
Transpile | fits | A chip's gates
Run | uses | A Sampler
Read | shows | Counts
MicroQiskit | runs | Offline in our lab
"""),
 M("Quantum uses", """
Quantum computers | are good for | Molecules
Quantum computers | are good for | Searching
Quantum computers | are good for | Secrets
Quantum computers | are not for | Everyday apps
Molecules | simulate | Chemistry
Searching | uses | Grover's idea [ch10]
Secrets | break with | Shor's algorithm
Shor's algorithm | threatens | Some codes
Everyday apps | like | Email and games
Everyday apps | stay on | Normal computers
"""),
]


MAPS = [[a] for a in STRUCT]
