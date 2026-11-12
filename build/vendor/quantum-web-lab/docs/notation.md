# Q text and ASCII diagrams

The text notation comes from Q.js: rows are qubits, steps are separated by `-` (or spaces), and `#` links gates in the same step.

```
H-X#0-RZ(pi/2)-M
I-X#1-I-------M
```

| token | meaning |
|---|---|
| `I` | do nothing |
| `H X Y Z S SD T TD SX SXD` | single-qubit gates (`SD` is S dagger) |
| `RX(pi/2)` `RY(...)` `RZ(...)` `P(...)` | rotation and phase gates. Angles: radians, `pi/4`, `90deg` |
| `X#0 X#1` | CNOT: the last `#` is the target, earlier ones are controls. Three (`X#0 X#1 X#2`) make a Toffoli |
| `Z#0 Z#1`, `Y#0 Y#1`, `H#0 H#1`, `P(pi/2)#0 P(pi/2)#1` | CZ (or CCZ), CY, CH, controlled phase |
| `SWAP#0 SWAP#1` | swap |
| `M` | measure |

Add `// comments` at the end of a line. One linked group per symbol per step.

`QWL.toDiagram(circuit)` (and `qc.draw()` in MicroQiskit) prints the same circuit as text:

```
         1    2        3
q0 |0⟩──[H]───●────[RZ(pi/2)]──
              │
q1 |0⟩───────(+)──────────────
```

`{unicode:false}` (`qc.draw(True)`) uses plain ASCII: `-[H]---@---`.
