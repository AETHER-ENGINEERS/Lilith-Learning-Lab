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


PROC = [
 M("The sunglasses experiment", """
Lamp | shines through | First filter
First filter | makes | Vertical light
Vertical light | then meets | Crossed filter
Crossed filter | blocks | All the light
Vertical light | or meets first | Middle filter at 45 degrees
Middle filter at 45 degrees | passes | Half the light
Half the light | then meets | Last filter at 90 degrees
Last filter at 90 degrees | passes | A quarter of the light
A quarter of the light | shows | Looking changes things
"""),
 M("From bit to qubit", """
A bit | add chance | A coin with chances
A coin with chances | add a hidden direction | A qubit
A qubit | when measured | One answer
One answer | repeated many times | Chances appear
A qubit | add another | Two qubits
Two qubits | add another | Three qubits
Three qubits | the list doubles each time | 2 to the n numbers
"""),
 M("Life of a measurement", """
Prepare a qubit | gives | Two amplitudes
Two amplitudes | square them | Two chances
Two chances | nature picks | One answer
One answer | the qubit now is | That plain state
That plain state | repeat from the start | Many shots
Many shots | add up to | Counts
Counts | approach | The chances
"""),
 M("Building with gates", """
Start at 0 | apply X | Plain 1
Start at 0 | apply H | Fair blend
Fair blend | apply H again | Back to plain 0
Fair blend | apply Z | Blend with flipped sign
Blend with flipped sign | apply H | Plain 1
Plain 1 | apply X | Plain 0
"""),
 M("The H, phase, H recipe", """
Start at 0 | apply H | Fair blend
Fair blend | turn the phase | Blend with a twist
Blend with a twist | apply H | Chance set by the twist
Chance set by the twist | twist of 0 degrees | Always 0
Chance set by the twist | twist of 90 degrees | 50 50
Chance set by the twist | twist of 180 degrees | Always 1
"""),
 M("Turning the arrow", """
North pole | apply H | Plus x point
Plus x point | apply S | Plus i point
Plus i point | apply S | Minus x point
Minus x point | apply H | South pole
South pole | measure | Always 1
"""),
 M("Reading a circuit", """
Find the rows | each row is | One qubit
One qubit | start at | The left edge
The left edge | read | One column at a time
One column at a time | notice | Linked gates
Linked gates | have | A control and a target
One column at a time | until | The measurement
The measurement | gives | The result
"""),
 M("How CNOT acts", """
Look at the control | if it is 0 | Target unchanged
Look at the control | if it is 1 | Target flips
Target unchanged | so | 00 stays 00
Target flips | so | 10 becomes 11
Look at the control | if it is a blend | Both cases at once
Both cases at once | which makes | An entangled pair
"""),
 M("Making a Bell pair", """
Two qubits at 0 | apply H to qubit 0 | Qubit 0 is a blend
Qubit 0 is a blend | apply CNOT 0 to 1 | A Bell pair
A Bell pair | measure | 00 or 11
00 or 11 | repeat many shots | Half and half
A Bell pair | measure qubit 0 | Qubit 1 is now certain
"""),
 M("One round of Grover", """
Even blend of all items | mark the prize | Prize has a negative sign
Prize has a negative sign | mirror about the average | Prize amplitude grows
Prize amplitude grows | repeat about root N times | Prize is nearly certain
Prize is nearly certain | measure | Find the prize
Prize amplitude grows | repeat too long | Overshoot and fade
"""),
 M("Trusting a result", """
Run many shots | gives | Noisy counts
Noisy counts | compare with | Expected chances
Expected chances | the gap is | Standard error
Standard error | shrinks with | More shots
More shots | still limited by | Hardware noise
Hardware noise | is fixed by | Error correction
"""),
 M("Writing OpenQASM", """
Write the header | then | Declare qubits
Declare qubits | then | Declare bits
Declare bits | then | Add gate lines
Add gate lines | then | Measure
Measure | then | Save the file
Save the file | then | Load it in a tool
Load it in a tool | then | Run it
Write the header | choose | Version 2 or 3
"""),
 M("A MicroQiskit session", """
Write Python | builds | A QuantumCircuit
A QuantumCircuit | add | Gates with h and cx
Gates with h and cx | then | simulate
simulate | returns | Counts
A QuantumCircuit | also gives | OpenQASM text
OpenQASM text | loads into | The composer
Gates with h and cx | on real Qiskit add | Transpile and Sampler
"""),
 M("Is quantum a good fit?", """
A hard problem | ask | Is there structure to use?
Is there structure to use? | if yes | Quantum may help
Is there structure to use? | if no | Use a normal computer
Quantum may help | needs | Many reliable qubits
Many reliable qubits | need | Error correction [ch11]
A hard problem | or is it | Email or games
Email or games | use | A normal computer
"""),
]

MAPS = [[a, b] for a, b in zip(STRUCT, PROC)]
