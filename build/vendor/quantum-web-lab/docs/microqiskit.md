# MicroQiskit

`src/microqiskit.py` is a tiny Qiskit-style toolkit for MicroPython (and CPython). It has no dependencies, and it is the code that runs in the lab's Python tab.

```python
from microqiskit import QuantumCircuit, simulate
from math import pi

qc = QuantumCircuit(2, 2)        # qubits, classical bits
qc.h(0)
qc.cx(0, 1)
qc.rz(pi / 2, 0)                 # angle first, like Qiskit
qc.measure(0, 0)
qc.measure(1, 1)

print(simulate(qc, 1000, 'counts'))        # {'00': 506, '11': 494}
print(simulate(qc, get='statevector'))     # list of complex numbers
print(qc.draw())                           # ASCII picture (draw(True) is plain ASCII)
print(qc.qasm())                           # OpenQASM 3 text
```

| | |
|---|---|
| gates | `id h x y z s sdg t tdg sx sxdg`, `rx ry rz p` (angle first), `cx cy cz ch swap`, `cp` (angle first), `ccx ccz`, `measure(q, c)`, `measure_all()`, `barrier()` |
| `simulate(qc, shots=1024, get='counts', seed=None)` | `get` is `'counts'`, `'memory'` (one string per shot), `'statevector'` or `'probabilities'` |
| `qc.data` | list of tuples such as `('h', 0)`, `('rx', 1.57, 0)`, `('cx', 0, 1)` (like the original MicroQiskit) |
| `from_qasm(text)` | build a circuit from OpenQASM 2 or 3 text (the micro QASM subset) |
| `last()` | the circuit created most recently. The lab reads `qc` (or `last()`) after your code runs |

**Bit order.** Like Qiskit, qubit 0 is the right-most digit of a result (`'01'` means qubit 0 is 1). The composer in the lab writes qubit 0 on the left (Q.js style) and has a button to flip its labels.

Errors are written for beginners (`qubit 5 does not exist, this circuit has 1`).
Up to about 10 qubits is comfortable on a phone.

How it is tested: `tests/microqiskit.test.mjs` runs it on the real MicroPython WebAssembly build and checks every result against the JavaScript simulator, including generated QASM and the ASCII diagram.
