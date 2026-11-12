"""MicroQiskit for the Quantum Web Lab: a tiny Qiskit-style toolkit that runs on MicroPython and CPython.  MIT licence.

    from microqiskit import QuantumCircuit, simulate
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    print(simulate(qc, 1000, 'counts'))
    print(qc.draw())
    print(qc.qasm())

Like Qiskit, qubit 0 is the RIGHT-most digit of a result such as '01' (little endian).
(The composer in the lab shows qubit 0 on the LEFT, like Q.js. The bars are labelled for you.)
Supported gates: id h x y z s sdg t tdg sx sxdg | rx ry rz p (angle first) | cx cy cz ch swap | cp (angle first) | ccx ccz | measure barrier.
"""
from math import pi, cos, sin, sqrt

__version__ = '0.1.0'
_last = None
_ONE = ('id', 'h', 'x', 'y', 'z', 's', 'sdg', 't', 'tdg', 'sx', 'sxdg')
_ROT = ('rx', 'ry', 'rz', 'p')
_CTRL = {'cx': ('x', 1), 'cy': ('y', 1), 'cz': ('z', 1), 'ch': ('h', 1), 'cp': ('p', 1), 'ccx': ('x', 2), 'ccz': ('z', 2)}
_NQ = {'swap': 2, 'cx': 2, 'cy': 2, 'cz': 2, 'ch': 2, 'cp': 2, 'ccx': 3, 'ccz': 3}
_SYM = {'id': 'I', 'h': 'H', 'x': 'X', 'y': 'Y', 'z': 'Z', 's': 'S', 'sdg': 'SD', 't': 'T', 'tdg': 'TD', 'sx': 'SX', 'sxdg': 'SXD', 'rx': 'RX', 'ry': 'RY', 'rz': 'RZ', 'p': 'P'}
_ALIAS = {'id': 'id', 'u1': 'p', 'cu1': 'cp', 'cnot': 'cx', 'ccnot': 'ccx', 'toffoli': 'ccx', 'sdag': 'sdg', 'tdag': 'tdg'}


def last():
    """The most recent QuantumCircuit that was created (the lab reads it after your code runs)."""
    return _last


def _angle(a):
    """pi/2 style text for an angle, like the lab's code panel."""
    if abs(a) < 1e-12:
        return '0'
    sign = '-' if a < 0 else ''
    x = abs(a) / pi
    for m in range(1, 13):
        k = round(x * m)
        if 0 < k <= 4 * m and abs(x * m - k) < 1e-9:
            g, h = k, m
            while h:
                g, h = h, g % h
            kk, mm = k // g, m // g
            return sign + ('pi' if kk == 1 else str(kk) + '*pi') + ('' if mm == 1 else '/' + str(mm))
    return sign + str(round(abs(a), 6))


def _mat(name, t=0.0):
    r = 0.7071067811865476
    if name == 'id': return (1, 0, 0, 1)
    if name == 'h': return (r, r, r, -r)
    if name == 'x': return (0, 1, 1, 0)
    if name == 'y': return (0, -1j, 1j, 0)
    if name == 'z': return (1, 0, 0, -1)
    if name == 's': return (1, 0, 0, 1j)
    if name == 'sdg': return (1, 0, 0, -1j)
    if name == 't': return (1, 0, 0, complex(r, r))
    if name == 'tdg': return (1, 0, 0, complex(r, -r))
    if name == 'sx': return (complex(.5, .5), complex(.5, -.5), complex(.5, -.5), complex(.5, .5))
    if name == 'sxdg': return (complex(.5, -.5), complex(.5, .5), complex(.5, .5), complex(.5, -.5))
    c, s = cos(t / 2), sin(t / 2)
    if name == 'rx': return (c, complex(0, -s), complex(0, -s), c)
    if name == 'ry': return (c, -s, s, c)
    if name == 'rz': return (complex(c, -s), 0, 0, complex(c, s))
    if name == 'p': return (1, 0, 0, complex(cos(t), sin(t)))
    raise ValueError('no gate called ' + name)


class QuantumCircuit:
    def __init__(self, num_qubits, num_clbits=0):
        global _last
        if num_qubits < 1:
            raise ValueError('a circuit needs at least 1 qubit')
        self.num_qubits = num_qubits
        self.num_clbits = num_clbits
        self.data = []
        _last = self

    def _check(self, *qs):
        for q in qs:
            if not (isinstance(q, int) and 0 <= q < self.num_qubits):
                raise ValueError('qubit ' + str(q) + ' does not exist, this circuit has ' + str(self.num_qubits))
        if len(set(qs)) != len(qs):
            raise ValueError('a gate cannot use the same qubit twice')

    def _one(self, name, q):
        self._check(q)
        self.data.append((name, q))

    def _rot(self, name, theta, q):
        self._check(q)
        self.data.append((name, float(theta), q))

    def id(self, q): self._one('id', q)
    def h(self, q): self._one('h', q)
    def x(self, q): self._one('x', q)
    def y(self, q): self._one('y', q)
    def z(self, q): self._one('z', q)
    def s(self, q): self._one('s', q)
    def sdg(self, q): self._one('sdg', q)
    def t(self, q): self._one('t', q)
    def tdg(self, q): self._one('tdg', q)
    def sx(self, q): self._one('sx', q)
    def sxdg(self, q): self._one('sxdg', q)
    def rx(self, theta, q): self._rot('rx', theta, q)
    def ry(self, theta, q): self._rot('ry', theta, q)
    def rz(self, theta, q): self._rot('rz', theta, q)
    def p(self, theta, q): self._rot('p', theta, q)

    def cx(self, c, t):
        self._check(c, t); self.data.append(('cx', c, t))

    def cy(self, c, t):
        self._check(c, t); self.data.append(('cy', c, t))

    def cz(self, c, t):
        self._check(c, t); self.data.append(('cz', c, t))

    def ch(self, c, t):
        self._check(c, t); self.data.append(('ch', c, t))

    def swap(self, a, b):
        self._check(a, b); self.data.append(('swap', a, b))

    def cp(self, theta, c, t):
        self._check(c, t); self.data.append(('cp', float(theta), c, t))

    def ccx(self, a, b, t):
        self._check(a, b, t); self.data.append(('ccx', a, b, t))

    def ccz(self, a, b, t):
        self._check(a, b, t); self.data.append(('ccz', a, b, t))

    def measure(self, q, c):
        self._check(q)
        if not (isinstance(c, int) and 0 <= c < self.num_clbits):
            raise ValueError('bit ' + str(c) + ' does not exist. Make the circuit with QuantumCircuit(' + str(self.num_qubits) + ', ' + str(max(self.num_clbits, c + 1) if isinstance(c, int) else 'bits') + ')')
        self.data.append(('measure', q, c))

    def barrier(self):
        self.data.append(('barrier',))

    def measure_all(self):
        self.num_clbits = max(self.num_clbits, self.num_qubits)
        for q in range(self.num_qubits):
            self.data.append(('measure', q, q))

    # ---- text views ----
    def _qubits_of(self, op):
        name = op[0]
        if name == 'barrier': return []
        if name == 'measure': return [op[1]]
        if name in _ROT: return [op[2]]
        if name == 'cp': return [op[2], op[3]]
        return list(op[1:])

    def qasm(self):
        n = self.num_qubits
        ms = [op for op in self.data if op[0] == 'measure']
        nb = self.num_clbits if ms else 0
        out = ['OPENQASM 3.0;', 'include "stdgates.inc";', 'qubit[' + str(n) + '] q;']
        if nb:
            out.append('bit[' + str(nb) + '] c;')
        for op in self.data:
            name = op[0]
            if name == 'barrier':
                out.append('barrier q;')
            elif name == 'measure':
                out.append('c[' + str(op[2]) + '] = measure q[' + str(op[1]) + '];')
            elif name == 'id' or name in _ONE:
                out.append(name + ' q[' + str(op[1]) + '];')
            elif name in _ROT:
                out.append(name + '(' + _angle(op[1]) + ') q[' + str(op[2]) + '];')
            elif name == 'cp':
                out.append('cp(' + _angle(op[1]) + ') q[' + str(op[2]) + '], q[' + str(op[3]) + '];')
            elif name == 'ccz':
                out.append('h q[' + str(op[3]) + '];')
                out.append('ccx q[' + str(op[1]) + '], q[' + str(op[2]) + '], q[' + str(op[3]) + '];')
                out.append('h q[' + str(op[3]) + '];')
            else:
                out.append(name + ' ' + ', '.join(['q[' + str(q) + ']' for q in op[1:]]) + ';')
        return '\n'.join(out)

    def draw(self, ascii_only=False):
        """A text picture of the circuit (same look as the lab's ASCII tab). Qubit 0 is the top row."""
        n = self.num_qubits
        U = not ascii_only
        H, V, X, CT, SW = ('\u2500', '\u2502', '\u253c', '\u25cf', '\u00d7') if U else ('-', '|', '+', '@', 'x')
        free = [0] * n
        cols = []
        for op in self.data:
            qs = self._qubits_of(op)
            if not qs:
                top = max(free)
                free = [top] * n
                continue
            lo, hi = min(qs), max(qs)
            c = max(free[lo:hi + 1])
            for q in range(lo, hi + 1):
                free[q] = c + 1
            while len(cols) <= c:
                cols.append([])
            cols[c].append(op)
        rows = ['q' + str(q) + ' |0' + ('\u27e9' if U else '>') + H for q in range(n)]
        conns = ['' for _ in range(n - 1)]
        head = ' ' * len(rows[0])
        conns = [' ' * len(rows[0]) for _ in range(n - 1)]
        for ci in range(len(cols)):
            cells = [None] * n
            spans = {}
            inside = {}
            for op in cols[ci]:
                name = op[0]
                qs = self._qubits_of(op)
                if name == 'measure':
                    cells[op[1]] = '[M]'
                elif name == 'swap':
                    cells[op[1]] = SW
                    cells[op[2]] = SW
                elif name in _CTRL:
                    base, nc = _CTRL[name]
                    for q in qs[:nc]:
                        cells[q] = CT
                    t = qs[-1]
                    par = '(' + _angle(op[1]) + ')' if name == 'cp' else ''
                    cells[t] = '(+)' if base == 'x' else CT if base == 'z' else '[' + _SYM[base] + par + ']'
                else:
                    par = '(' + _angle(op[1]) + ')' if name in _ROT else ''
                    cells[qs[0]] = '[' + _SYM[name] + par + ']'
                if len(qs) > 1:
                    for k in range(min(qs), max(qs)):
                        spans[k] = 1
                    for k in range(min(qs) + 1, max(qs)):
                        inside[k] = 1
            w = 5
            for s in cells:
                if s and len(s) + 2 > w:
                    w = len(s) + 2
            mid = w // 2
            for q in range(n):
                s = cells[q]
                if s is None:
                    rows[q] += (H * mid + X + H * (w - mid - 1)) if (q in inside) else H * w
                else:
                    left = (w - len(s)) // 2
                    rows[q] += H * left + s + H * (w - len(s) - left)
            for q in range(n - 1):
                conns[q] += (' ' * mid + V + ' ' * (w - mid - 1)) if q in spans else ' ' * w
            lab = str(ci + 1)
            head += ' ' * max(0, mid - len(lab) // 2) + lab + ' ' * max(0, w - max(0, mid - len(lab) // 2) - len(lab))
        out = [head.rstrip()]
        for q in range(n):
            out.append(rows[q])
            if q < n - 1:
                out.append(conns[q].rstrip())
        return '\n'.join(out)

    def __repr__(self):
        return '<QuantumCircuit ' + str(self.num_qubits) + ' qubits, ' + str(len(self.data)) + ' operations>'


# ---------------- simulator (qubit 0 is the lowest bit, like Qiskit) ----------------
def _apply(re, im, q, m, cmask):
    bit = 1 << q
    for i in range(len(re)):
        if i & bit or (i & cmask) != cmask:
            continue
        j = i | bit
        a = complex(re[i], im[i])
        b = complex(re[j], im[j])
        na = m[0] * a + m[1] * b
        nb = m[2] * a + m[3] * b
        re[i] = na.real; im[i] = na.imag; re[j] = nb.real; im[j] = nb.imag


def _run(qc):
    n = qc.num_qubits
    N = 1 << n
    re = [0.0] * N
    im = [0.0] * N
    re[0] = 1.0
    for op in qc.data:
        name = op[0]
        if name in ('barrier', 'measure'):
            continue
        if name == 'swap':
            a, b = 1 << op[1], 1 << op[2]
            for i in range(N):
                if (i & a) and not (i & b):
                    j = (i ^ a) | b
                    re[i], re[j] = re[j], re[i]
                    im[i], im[j] = im[j], im[i]
        elif name in _CTRL:
            base, nc = _CTRL[name]
            theta = op[1] if name == 'cp' else 0.0
            qs = list(op[2:]) if name == 'cp' else list(op[1:])
            cmask = 0
            for q in qs[:nc]:
                cmask |= 1 << q
            _apply(re, im, qs[-1], _mat(base, theta), cmask)
        elif name in _ROT:
            _apply(re, im, op[2], _mat(name, op[1]), 0)
        else:
            _apply(re, im, op[1], _mat(name), 0)
    return re, im


def _key(index, qc, meas):
    """The result text for a basis index. With measurements: classical bits c[m-1]..c[0]; without: every qubit, q[n-1]..q[0]."""
    if meas:
        bits = [0] * qc.num_clbits
        for q, c in meas:
            bits[c] = (index >> q) & 1
        return ''.join([str(bits[c]) for c in range(qc.num_clbits - 1, -1, -1)])
    return ''.join([str((index >> q) & 1) for q in range(qc.num_qubits - 1, -1, -1)])


def simulate(qc, shots=1024, get='counts', seed=None):
    """Run a circuit. get = 'counts' | 'memory' | 'statevector' | 'probabilities'."""
    re, im = _run(qc)
    N = len(re)
    probs = [re[i] * re[i] + im[i] * im[i] for i in range(N)]
    meas = [(op[1], op[2]) for op in qc.data if op[0] == 'measure']
    if get == 'statevector':
        return [complex(re[i], im[i]) for i in range(N)]
    if get == 'probabilities':
        out = {}
        for i in range(N):
            if probs[i] > 1e-12:
                k = _key(i, qc, meas)
                out[k] = out.get(k, 0.0) + probs[i]
        return dict((k, round(out[k], 10)) for k in sorted(out))
    import random
    if seed is not None:
        random.seed(seed)
    cum = []
    acc = 0.0
    for p in probs:
        acc += p
        cum.append(acc)
    mem = []
    for _ in range(shots):
        x = random.random() * acc
        lo, hi = 0, N - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cum[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        mem.append(_key(lo, qc, meas))
    if get == 'memory':
        return mem
    if get != 'counts':
        raise ValueError("get must be 'counts', 'memory', 'statevector' or 'probabilities'")
    counts = {}
    for k in mem:
        counts[k] = counts.get(k, 0) + 1
    return dict((k, counts[k]) for k in sorted(counts))


# ---------------- micro QASM: read the same OpenQASM subset the lab reads ----------------
def _num(s):
    s = s.replace(' ', '').lower().replace('\u03c0', 'pi')
    pos = [0]

    def peek():
        return s[pos[0]] if pos[0] < len(s) else ''

    def factor():
        c = peek()
        if c == '-':
            pos[0] += 1
            return -factor()
        if c == '(':
            pos[0] += 1
            v = expr()
            if peek() != ')':
                raise ValueError('missing ) in the angle ' + s)
            pos[0] += 1
            return v
        if s[pos[0]:pos[0] + 2] == 'pi':
            pos[0] += 2
            return pi
        j = pos[0]
        while j < len(s) and (s[j].isdigit() or s[j] in '.e' or (s[j] in '+-' and j > pos[0] and s[j - 1] == 'e')):
            j += 1
        if j == pos[0]:
            raise ValueError('I could not read the angle ' + s)
        v = float(s[pos[0]:j])
        pos[0] = j
        if s[pos[0]:pos[0] + 3] == 'deg':
            pos[0] += 3
            v = v * pi / 180
        return v

    def term():
        v = factor()
        while peek() in ('*', '/') and peek() != '':
            o = peek()
            pos[0] += 1
            r = factor()
            v = v * r if o == '*' else v / r
        return v

    def expr():
        v = term()
        while peek() in ('+', '-') and peek() != '':
            o = peek()
            pos[0] += 1
            r = term()
            v = v + r if o == '+' else v - r
        return v

    out = expr()
    if pos[0] < len(s):
        raise ValueError('I could not read the angle ' + s)
    return out


def _ref(tok, regs, what):
    tok = tok.strip()
    if '[' in tok:
        name, rest = tok.split('[', 1)
        idx = int(rest.split(']')[0])
        if name not in regs:
            raise ValueError('there is no ' + what + ' called ' + name + ' (declare it first)')
        off, size = regs[name]
        if idx >= size:
            raise ValueError(tok + ' is out of range, ' + name + ' has ' + str(size))
        return [off + idx]
    if tok not in regs:
        raise ValueError('there is no ' + what + ' called ' + tok + ' (declare it first)')
    off, size = regs[tok]
    return [off + i for i in range(size)]


def from_qasm(text):
    """Build a QuantumCircuit from OpenQASM 2 or 3 text (the same subset the lab reads)."""
    lines = []
    in_block = False
    for ln in text.split('\n'):
        if in_block:
            if '*/' in ln:
                in_block = False
                ln = ln.split('*/', 1)[1]
            else:
                continue
        if '/*' in ln:
            ln = ln.split('/*', 1)[0]
            in_block = True
        lines.append(ln.split('//')[0])
    stmts = [s.strip() for s in ' '.join(lines).split(';')]
    qregs, cregs, nq, nc = {}, {}, 0, 0
    ops = []
    for s in stmts:
        if not s:
            continue
        low = s.lower()
        word = low.split('(')[0].split(' ')[0].split('[')[0]
        if word in ('openqasm', 'include'):
            continue
        if word in ('qubit', 'qreg', 'bit', 'creg'):
            if word in ('qubit', 'bit'):
                rest = s[len(word):].strip()
                size = 1
                if rest.startswith('['):
                    size = int(rest[1:rest.index(']')])
                    rest = rest[rest.index(']') + 1:].strip()
                name = rest
            else:
                rest = s[len(word):].strip()
                name = rest.split('[')[0].strip()
                size = int(rest.split('[')[1].split(']')[0])
            if word in ('qubit', 'qreg'):
                qregs[name] = (nq, size)
                nq += size
            else:
                cregs[name] = (nc, size)
                nc += size
            continue
        if word == 'barrier':
            ops.append(('barrier',))
            continue
        if word in ('gate', 'def', 'for', 'while', 'if', 'reset', 'opaque', 'let', 'const', 'int', 'float', 'bool', 'input', 'output'):
            raise ValueError('microQASM does not support "' + word + '" yet')
        if word == 'measure' or '= measure' in low or '=measure' in low:
            if '->' in s:
                a, b = s[len('measure'):].split('->')
                qs, cs = _ref(a, qregs, 'qubit'), _ref(b, cregs, 'bit')
            elif '=' in s:
                b, a = s.split('=', 1)
                qs, cs = _ref(a.strip()[len('measure'):], qregs, 'qubit'), _ref(b, cregs, 'bit')
            else:
                qs = _ref(s[len('measure'):], qregs, 'qubit')
                cs = list(range(len(qs)))
            for q, c in zip(qs, cs):
                ops.append(('measure', q, c))
            continue
        head, _, rest = s.partition(' ')
        params = []
        if '(' in s.split(' ')[0] or ('(' in head):
            full = s[:s.index(')') + 1]
            head = full[:full.index('(')]
            params = [_num(a) for a in full[full.index('(') + 1:-1].split(',') if a.strip()]
            rest = s[s.index(')') + 1:]
        name = _ALIAS.get(head.lower(), head.lower())
        args = [_ref(a, qregs, 'qubit') for a in rest.split(',')]
        if name not in _ONE and name not in _ROT and name not in _NQ:
            raise ValueError('microQASM does not know the gate ' + head)
        longest = max([len(a) for a in args])
        for i in range(longest):
            qq = [a[0] if len(a) == 1 else a[i] for a in args]
            if name in _ROT:
                ops.append((name, params[0], qq[0]))
            elif name == 'cp':
                ops.append(('cp', params[0], qq[0], qq[1]))
            else:
                ops.append(tuple([name] + qq))
    if not nq:
        raise ValueError('no qubits declared. Start with: OPENQASM 3.0; then qubit[2] q;')
    qc = QuantumCircuit(nq, nc)
    qc.data = ops
    return qc
