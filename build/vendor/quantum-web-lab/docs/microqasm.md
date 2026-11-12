# micro QASM

micro QASM is the OpenQASM subset that the lab reads (`QWL.fromQasm`, and `microqiskit.from_qasm` in Python) and writes (`QWL.toQasm`, `qc.qasm()`).

```
OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;
bit[3] c;
h q[0];
cx q[0], q[1];
rz(pi/4) q[2];
h q;                      // a whole register at once
barrier q;                // starts a new step in the picture
c = measure q;            // or: c[0] = measure q[1];
```

**Reads**

* Header: `OPENQASM 3.0;` or `2.0;`, `include ...;` (ignored).
* Registers: `qubit[n] q;`, `qubit q;`, `bit[n] c;` and the version 2 forms `qreg q[n];`, `creg c[n];`. Several registers are fine.
* Gates: `id h x y z s sdg t tdg sx sxdg rx ry rz p u1 cx cnot cy cz ch swap cp cu1 ccx toffoli`.
* Angles: numbers (radians), `pi`, `pi/2`, `3*pi/4`, `-pi`, `(1+1)*pi/4`, `90deg`.
* Measure: `c = measure q;`, `c[0] = measure q[1];`, `measure q -> c;`, `measure q[0] -> c[0];`, `measure q;`
* Comments: `// line` and `/* block */`.

**Does not read yet** (a friendly error with the line number says so): `gate`, `def`, `for`, `while`, `if`, `reset`, `opaque`, classical types and expressions. This keeps the parser small and the messages clear.

**Writes** OpenQASM 3 by default (`QWL.toQasm(c, 3)`) or 2 (`toQasm(c, 2)`, which uses `u1`/`cu1`). `ccz` is written as `h`, `ccx`, `h` because it is not in `stdgates.inc`.

In the picture, gates are placed as early as they fit. A `barrier` forces the next gate into a new step.
