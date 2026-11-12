/*! quantum-web-lab core | MIT | simulator, circuit model, Q.js style text, ASCII diagrams, micro QASM, MicroQiskit codegen.
    The text notation and the diagram look follow Q.js by Stewart Smith (https://github.com/stewdio/q.js, MIT). */
(function (root) {
  'use strict';
  var QWL = root.QWL = root.QWL || {};
  QWL.version = '0.1.0';
  var PI = Math.PI, SQ = Math.SQRT1_2;

  /* ---------- angles ---------- */
  // parseAngle("pi/2") "3*pi/4" "-pi" "90deg" "0.5" -> radians
  function parseAngle(src) {
    var s = String(src).replace(/\s+/g, '').toLowerCase().replace(/°/g, 'deg').replace(/π/g, 'pi').replace(/math\.pi/g, 'pi'), i = 0;
    function peek() { return s.charAt(i); }
    function num() {
      var m = /^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/.exec(s.slice(i)); if (!m) throw new Error('I could not read the angle "' + src + '"');
      i += m[0].length; var v = parseFloat(m[0]);
      if (s.substr(i, 3) === 'deg') { i += 3; v = v * PI / 180; } return v;
    }
    function factor() {
      if (peek() === '-') { i++; return -factor(); } if (peek() === '+') { i++; return factor(); }
      if (peek() === '(') { i++; var v = expr(); if (peek() !== ')') throw new Error('missing ) in the angle "' + src + '"'); i++; return v; }
      if (s.substr(i, 2) === 'pi') { i += 2; return PI; }
      return num();
    }
    function term() { var v = factor(); while (peek() === '*' || peek() === '/') { var o = s.charAt(i++), r = factor(); v = o === '*' ? v * r : v / r; } return v; }
    function expr() { var v = term(); while (peek() === '+' || peek() === '-') { var o = s.charAt(i++), r = term(); v = o === '+' ? v + r : v - r; } return v; }
    var out = expr(); if (i < s.length) throw new Error('I could not read the angle "' + src + '"'); return out;
  }
  function fmtAngle(a) {
    if (Math.abs(a) < 1e-12) return '0';
    var sign = a < 0 ? '-' : '', x = Math.abs(a) / PI, m, k;
    for (m = 1; m <= 12; m++) { k = Math.round(x * m); if (k > 0 && k <= 4 * m && Math.abs(x * m - k) < 1e-9) {
      var g = gcd(k, m), kk = k / g, mm = m / g; return sign + (kk === 1 ? 'pi' : kk + '*pi') + (mm === 1 ? '' : '/' + mm); } }
    return sign + String(Math.round(Math.abs(a) * 1e6) / 1e6);
  }
  function gcd(a, b) { return b ? gcd(b, a % b) : a; }

  /* ---------- gates ---------- */
  // sym = text symbol, nq = qubits, np = params, ctrl = [base gate, controls], grp = colour group
  var GATES = {
    i: { sym: 'I', nq: 1, np: 0, grp: 'id', info: 'Does nothing.' },
    h: { sym: 'H', nq: 1, np: 0, grp: 'h', info: 'Hadamard: makes a fair blend of 0 and 1.' },
    x: { sym: 'X', nq: 1, np: 0, grp: 'pauli', info: 'X: flips 0 and 1 (a NOT).' },
    y: { sym: 'Y', nq: 1, np: 0, grp: 'pauli', info: 'Y: a flip with a twist of phase.' },
    z: { sym: 'Z', nq: 1, np: 0, grp: 'pauli', info: 'Z: flips the sign of the 1 part (phase).' },
    s: { sym: 'S', nq: 1, np: 0, grp: 'phase', info: 'S: a quarter turn of phase (90 degrees).' },
    sdg: { sym: 'SD', nq: 1, np: 0, grp: 'phase', info: 'S dagger: undoes S.' },
    t: { sym: 'T', nq: 1, np: 0, grp: 'phase', info: 'T: an eighth turn of phase (45 degrees).' },
    tdg: { sym: 'TD', nq: 1, np: 0, grp: 'phase', info: 'T dagger: undoes T.' },
    sx: { sym: 'SX', nq: 1, np: 0, grp: 'phase', info: 'Square root of X: half a flip.' },
    sxdg: { sym: 'SXD', nq: 1, np: 0, grp: 'phase', info: 'Undoes SX.' },
    rx: { sym: 'RX', nq: 1, np: 1, grp: 'rot', info: 'Rotate around X by an angle.' },
    ry: { sym: 'RY', nq: 1, np: 1, grp: 'rot', info: 'Rotate around Y by an angle.' },
    rz: { sym: 'RZ', nq: 1, np: 1, grp: 'rot', info: 'Rotate around Z by an angle (turns phase).' },
    p: { sym: 'P', nq: 1, np: 1, grp: 'rot', info: 'Phase gate: turns the phase of 1 by an angle.' },
    cx: { sym: 'X', nq: 2, np: 0, grp: 'ctl', ctrl: ['x', 1], name: 'CNOT', info: 'CNOT: flips the target when the control is 1.' },
    cy: { sym: 'Y', nq: 2, np: 0, grp: 'ctl', ctrl: ['y', 1], name: 'CY', info: 'Controlled Y.' },
    cz: { sym: 'Z', nq: 2, np: 0, grp: 'ctl', ctrl: ['z', 1], name: 'CZ', info: 'Controlled Z: flips the sign when both are 1.' },
    ch: { sym: 'H', nq: 2, np: 0, grp: 'ctl', ctrl: ['h', 1], name: 'CH', info: 'Controlled H.' },
    cp: { sym: 'P', nq: 2, np: 1, grp: 'ctl', ctrl: ['p', 1], name: 'CP', info: 'Controlled phase.' },
    ccx: { sym: 'X', nq: 3, np: 0, grp: 'ctl', ctrl: ['x', 2], name: 'CCX', info: 'Toffoli: flips the target when both controls are 1.' },
    ccz: { sym: 'Z', nq: 3, np: 0, grp: 'ctl', ctrl: ['z', 2], name: 'CCZ', info: 'Controlled-controlled Z.' },
    swap: { sym: 'SWAP', nq: 2, np: 0, grp: 'ctl', name: 'SWAP', info: 'Swaps two qubits.' },
    measure: { sym: 'M', nq: 1, np: 0, grp: 'meas', name: 'M', info: 'Measure: read the qubit as a plain 0 or 1.' }
  };
  var ALIAS = { id: 'i', u1: 'p', cu1: 'cp', cphase: 'cp', phase: 'p', cnot: 'cx', ccnot: 'ccx', toffoli: 'ccx', sdag: 'sdg', tdag: 'tdg', sxdag: 'sxdg', cnot_: 'cx' };
  function mat(g, p) {
    var c, s;
    switch (g) {
      case 'i': return [1, 0, 0, 0, 0, 0, 1, 0];
      case 'h': return [SQ, 0, SQ, 0, SQ, 0, -SQ, 0];
      case 'x': return [0, 0, 1, 0, 1, 0, 0, 0];
      case 'y': return [0, 0, 0, -1, 0, 1, 0, 0];
      case 'z': return [1, 0, 0, 0, 0, 0, -1, 0];
      case 's': return [1, 0, 0, 0, 0, 0, 0, 1];
      case 'sdg': return [1, 0, 0, 0, 0, 0, 0, -1];
      case 't': return [1, 0, 0, 0, 0, 0, SQ, SQ];
      case 'tdg': return [1, 0, 0, 0, 0, 0, SQ, -SQ];
      case 'sx': return [.5, .5, .5, -.5, .5, -.5, .5, .5];
      case 'sxdg': return [.5, -.5, .5, .5, .5, .5, .5, -.5];
      case 'rx': c = Math.cos(p / 2); s = Math.sin(p / 2); return [c, 0, 0, -s, 0, -s, c, 0];
      case 'ry': c = Math.cos(p / 2); s = Math.sin(p / 2); return [c, 0, -s, 0, s, 0, c, 0];
      case 'rz': c = Math.cos(p / 2); s = Math.sin(p / 2); return [c, -s, 0, 0, 0, 0, c, s];
      case 'p': return [1, 0, 0, 0, 0, 0, Math.cos(p), Math.sin(p)];
    }
    throw new Error('no matrix for ' + g);
  }

  /* ---------- circuit model ---------- */
  function Circuit(n) { this.n = n || 1; this.ops = []; this.cols = 0; }
  Circuit.prototype.clone = function () { var c = new Circuit(this.n); c.cols = this.cols; c.ops = this.ops.map(function (o) { return { g: o.g, q: o.q.slice(), p: o.p.slice(), col: o.col, c: o.c }; }); return c; };
  Circuit.prototype.add = function (g, q, p, col) {
    g = ALIAS[g] || g; var d = GATES[g]; if (!d) throw new Error('unknown gate "' + g + '"');
    q = [].concat(q); p = p === undefined || p === null ? [] : [].concat(p);
    if (q.length !== d.nq) throw new Error(g + ' needs ' + d.nq + ' qubit' + (d.nq > 1 ? 's' : '') + ', got ' + q.length);
    if (p.length !== d.np) throw new Error(g + ' needs ' + d.np + ' angle' + (d.np === 1 ? '' : 's') + ', got ' + p.length);
    var seen = {}; q.forEach(function (x) { if (!(x >= 0 && x < this.n) || x !== Math.floor(x)) throw new Error('qubit ' + x + ' does not exist (this circuit has ' + this.n + ')'); if (seen[x]) throw new Error('a gate cannot use qubit ' + x + ' twice'); seen[x] = 1; }, this);
    var op = { g: g, q: q, p: p, col: col === undefined ? this.cols : col };
    if (g === 'measure') op.c = q[0];
    this.ops.push(op); if (op.col + 1 > this.cols) this.cols = op.col + 1; return this;
  };
  Circuit.prototype.span = function (op) { var lo = Math.min.apply(0, op.q), hi = Math.max.apply(0, op.q); return [lo, hi]; };
  // give every op a column, as early as it fits (used for code that has no columns)
  Circuit.prototype.layout = function (breaks) {
    var free = [], i, self = this; for (i = 0; i < this.n; i++) free.push(0); var floor = 0, cols = 0;
    this.ops.forEach(function (op, k) {
      if (breaks && breaks[k]) { floor = cols; }
      var sp = self.span(op), c = floor, q; for (q = sp[0]; q <= sp[1]; q++) if (free[q] > c) c = free[q];
      op.col = c; for (q = sp[0]; q <= sp[1]; q++) free[q] = c + 1; if (c + 1 > cols) cols = c + 1;
    }); this.cols = cols; return this;
  };
  Circuit.prototype.sorted = function () { return this.ops.map(function (o, i) { return [o, i]; }).sort(function (a, b) { return a[0].col - b[0].col || a[1] - b[1]; }).map(function (x) { return x[0]; }); };
  Circuit.prototype.opAt = function (q, col) { for (var i = 0; i < this.ops.length; i++) { var o = this.ops[i]; if (o.col === col && o.q.indexOf(q) >= 0) return o; } return null; };
  Circuit.prototype.counts = function () { var r = {}; this.ops.forEach(function (o) { var k = o.g; r[k] = (r[k] || 0) + 1; }); return r; };
  Circuit.prototype.hasMeasure = function () { return this.ops.some(function (o) { return o.g === 'measure'; }); };

  /* ---------- simulator ---------- */
  var MAXQ = 12;
  function applyMat(re, im, n, q, m, cmask) {
    var bit = 1 << (n - 1 - q), N = re.length, i, j, ar, ai, br, bi;
    for (i = 0; i < N; i++) {
      if (i & bit) continue; if ((i & cmask) !== cmask) continue; j = i | bit;
      ar = re[i]; ai = im[i]; br = re[j]; bi = im[j];
      re[i] = m[0] * ar - m[1] * ai + m[2] * br - m[3] * bi; im[i] = m[0] * ai + m[1] * ar + m[2] * bi + m[3] * br;
      re[j] = m[4] * ar - m[5] * ai + m[6] * br - m[7] * bi; im[j] = m[4] * ai + m[5] * ar + m[6] * bi + m[7] * br;
    }
  }
  function simulate(circ) {
    var n = circ.n; if (n > MAXQ) throw new Error('This lab simulates up to ' + MAXQ + ' qubits.');
    var N = 1 << n, re = new Float64Array(N), im = new Float64Array(N); re[0] = 1;
    circ.sorted().forEach(function (op) {
      var d = GATES[op.g]; if (op.g === 'measure') return;
      if (op.g === 'swap') {
        var ma = 1 << (n - 1 - op.q[0]), mb = 1 << (n - 1 - op.q[1]), i, j, t;
        for (i = 0; i < N; i++) if ((i & ma) && !(i & mb)) { j = (i ^ ma) | mb; t = re[i]; re[i] = re[j]; re[j] = t; t = im[i]; im[i] = im[j]; im[j] = t; }
        return;
      }
      if (d.ctrl) {
        var cm = 0, k; for (k = 0; k < d.ctrl[1]; k++) cm |= 1 << (n - 1 - op.q[k]);
        applyMat(re, im, n, op.q[op.q.length - 1], mat(d.ctrl[0], op.p[0]), cm);
      } else applyMat(re, im, n, op.q[0], mat(op.g, op.p[0]), 0);
    });
    var probs = new Array(N), i; for (i = 0; i < N; i++) probs[i] = re[i] * re[i] + im[i] * im[i];
    return { n: n, re: re, im: im, probs: probs };
  }
  function label(i, n) { var s = ''; for (var k = n - 1; k >= 0; k--) s += (i >> k) & 1; return s; }   // qubit 0 is the leftmost digit
  function marginals(res) { var out = [], q, i; for (q = 0; q < res.n; q++) { var p = 0, bit = 1 << (res.n - 1 - q); for (i = 0; i < res.probs.length; i++) if (i & bit) p += res.probs[i]; out.push(p); } return out; }
  function bloch(res, q) {
    var bit = 1 << (res.n - 1 - q), x = 0, y = 0, z = 0, i, j;
    for (i = 0; i < res.probs.length; i++) { if (i & bit) { z -= res.probs[i]; continue; } z += res.probs[i]; j = i | bit;
      x += 2 * (res.re[i] * res.re[j] + res.im[i] * res.im[j]); y += 2 * (res.re[i] * res.im[j] - res.im[i] * res.re[j]); }
    return { x: x, y: y, z: z };
  }
  function rng(seed) { var a = (seed >>> 0) || 1; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  // shots over the measured qubits (in classical bit order) or over every qubit when nothing is measured
  function sample(circ, res, shots, seed) {
    var r = rng(seed === undefined ? 1 : seed), cum = [], acc = 0, i, out = {}, n = res.n;
    var meas = circ.ops.filter(function (o) { return o.g === 'measure'; }).sort(function (a, b) { return a.c - b.c; }).map(function (o) { return o.q[0]; });
    for (i = 0; i < res.probs.length; i++) { acc += res.probs[i]; cum.push(acc); }
    for (var s = 0; s < shots; s++) {
      var x = r() * acc, lo = 0, hi = cum.length - 1; while (lo < hi) { var mid = (lo + hi) >> 1; if (cum[mid] < x) lo = mid + 1; else hi = mid; }
      var key = label(lo, n); if (meas.length) key = meas.map(function (q) { return key.charAt(q); }).join('');
      out[key] = (out[key] || 0) + 1;
    }
    return out;
  }

  /* ---------- Q.js style text ---------- */
  var SYMS = {}; Object.keys(GATES).forEach(function (g) { var d = GATES[g]; if (!d.ctrl && g !== 'i' || g === 'i') SYMS[d.sym] = g; });
  SYMS.SDG = 'sdg'; SYMS.TDG = 'tdg'; SYMS.SXDG = 'sxdg'; SYMS.ID = 'i';
  var CTRLSYM = { X: ['cx', 'ccx'], Y: ['cy'], Z: ['cz', 'ccz'], H: ['ch'], P: ['cp'] };
  function splitRow(row) {
    var out = [], cur = '', depth = 0, k, ch;
    for (k = 0; k < row.length; k++) { ch = row.charAt(k);
      if (ch === '(') depth++; if (ch === ')') depth--;
      if (depth === 0 && (ch === '-' || /\s/.test(ch))) { if (cur) out.push(cur); cur = ''; } else cur += ch; }
    if (cur) out.push(cur); return out;
  }
  function fromText(text) {
    var rows = String(text).split(/\r?\n/).map(function (r) { return r.replace(/\/\/.*$/, '').trim(); }).filter(Boolean).map(splitRow);
    if (!rows.length) rows = [['I']]; var w = 0; rows.forEach(function (r) { if (r.length > w) w = r.length; });
    var c = new Circuit(rows.length), col, r;
    for (col = 0; col < w; col++) {
      var groups = {}, order = [];
      for (r = 0; r < rows.length; r++) {
        var tok = rows[r][col]; if (tok === undefined) continue;
        var m = /^([A-Za-z]+)(?:\(([^)]*)\))?(?:#(\d+))?$/.exec(tok); if (!m) throw new Error('I do not understand "' + tok + '" (row ' + (r + 1) + ', step ' + (col + 1) + ')');
        var sym = m[1].toUpperCase(), g = SYMS[sym]; if (!g) throw new Error('I do not know the gate "' + m[1] + '" (row ' + (r + 1) + ', step ' + (col + 1) + ')');
        var args = m[2] !== undefined ? m[2].split(',').map(parseAngle) : [];
        if (m[3] !== undefined) {
          var key = sym + '(' + (m[2] || '') + ')'; if (!groups[key]) { groups[key] = { sym: sym, p: args, items: [] }; order.push(key); }
          groups[key].items.push([+m[3], r]); continue;
        }
        if (g === 'i') continue;
        if (GATES[g].np !== args.length) throw new Error(m[1] + ' needs ' + GATES[g].np + ' angle(s), like ' + m[1] + '(pi/2) (row ' + (r + 1) + ')');
        c.add(g, [r], args, col);
      }
      order.forEach(function (key) {
        var gr = groups[key], qs = gr.items.sort(function (a, b) { return a[0] - b[0]; }).map(function (x) { return x[1]; });
        if (gr.sym === 'SWAP') { if (qs.length !== 2) throw new Error('SWAP#0 and SWAP#1 must be used together (step ' + (col + 1) + ')'); c.add('swap', qs, [], col); return; }
        var names = CTRLSYM[gr.sym]; if (!names) throw new Error(gr.sym + ' cannot be linked with #');
        var nm = names[qs.length - 2]; if (!nm || qs.length < 2) throw new Error(gr.sym + '#0 needs a partner like ' + gr.sym + '#1 in the same step (step ' + (col + 1) + ')');
        c.add(nm, qs, gr.p, col);
      });
    }
    c.cols = w; return c;
  }
  function tokenFor(op, q) {
    var d = GATES[op.g], idx;
    var par = d.np ? '(' + op.p.map(fmtAngle).join(',') + ')' : '';
    if (d.ctrl || op.g === 'swap') { idx = op.q.indexOf(q); return d.sym + par + '#' + idx; }
    return d.sym + par;
  }
  function toText(circ) {
    var rows = [], q, c;
    for (q = 0; q < circ.n; q++) { var r = []; for (c = 0; c < circ.cols; c++) { var op = circ.opAt(q, c); r.push(op ? tokenFor(op, q) : 'I'); } rows.push(r); }
    return rows.map(function (r) { return r.join('-'); }).join('\n');
  }

  /* ---------- ASCII diagram (Q.js style boxes) ---------- */
  function toDiagram(circ, opt) {
    opt = opt || {}; var U = opt.unicode !== false, W = U ? { h: '─', v: '│', x: '┼', ctl: '●', tgt: '(+)', sw: '×', ket: '⟩', l: '[', r: ']' } : { h: '-', v: '|', x: '+', ctl: '@', tgt: '(+)', sw: 'x', ket: '>', l: '[', r: ']' };
    var n = circ.n, rows = [], conns = [], head = '', q, c;
    function rep(ch, k) { var s = ''; while (k-- > 0) s += ch; return s; }
    for (q = 0; q < n; q++) { rows.push('q' + q + ' |0' + W.ket + W.h); } for (q = 0; q < n - 1; q++) conns.push('');
    var pad = rows[0].length; for (q = 0; q < n; q++) { var pre = rows[q]; while (pre.length < pad) pre += W.h; rows[q] = pre; }
    head = rep(' ', pad); for (q = 0; q < n - 1; q++) conns[q] = rep(' ', pad);
    for (c = 0; c < circ.cols; c++) {
      var cells = [], wmax = 1;
      for (q = 0; q < n; q++) cells.push(null);
      var links = [];
      circ.ops.forEach(function (op) {
        if (op.col !== c) return; var d = GATES[op.g];
        if (op.g === 'measure') { cells[op.q[0]] = 'M'; return; }
        if (op.g === 'swap') { op.q.forEach(function (k) { cells[k] = 'SW'; }); links.push(op); return; }
        if (d.ctrl) {
          var nc = d.ctrl[1], base = d.ctrl[0], k;
          for (k = 0; k < nc; k++) cells[op.q[k]] = 'C';
          var t = op.q[op.q.length - 1]; cells[t] = base === 'x' ? 'T' : base === 'z' ? 'C' : '[' + GATES[base].sym + (d.np ? '(' + op.p.map(fmtAngle).join(',') + ')' : '') + ']';
          links.push(op); return;
        }
        cells[op.q[0]] = '[' + d.sym + (d.np ? '(' + op.p.map(fmtAngle).join(',') + ')' : '') + ']';
      });
      cells.forEach(function (s) { if (s && s.length > wmax) wmax = s.length; });
      var cw = Math.max(5, wmax + 2), mid = Math.floor(cw / 2);
      var spanRows = {}; links.forEach(function (op) { var sp = op.q.slice().sort(function (a, b) { return a - b; }); for (var k = sp[0]; k < sp[sp.length - 1]; k++) spanRows[k] = 1; });
      var inside = {}; links.forEach(function (op) { var lo = Math.min.apply(0, op.q), hi = Math.max.apply(0, op.q); for (var k = lo + 1; k < hi; k++) if (!cells[k]) inside[k] = 1; });
      function cell(s, q) {
        var body;
        if (s === null) { body = inside[q] ? rep(W.h, mid) + W.x + rep(W.h, cw - mid - 1) : rep(W.h, cw); return body; }
        var txt = s === 'C' ? W.ctl : s === 'T' ? W.tgt : s === 'SW' ? W.sw : s === 'M' ? W.l + 'M' + W.r : s;
        var L = Math.floor((cw - txt.length) / 2); return rep(W.h, L) + txt + rep(W.h, cw - txt.length - L);
      }
      for (q = 0; q < n; q++) rows[q] += cell(cells[q], q);
      for (q = 0; q < n - 1; q++) conns[q] += spanRows[q] ? rep(' ', mid) + W.v + rep(' ', cw - mid - 1) : rep(' ', cw);
      var lab = String(c + 1); head += rep(' ', Math.max(0, mid - Math.floor(lab.length / 2))) + lab + rep(' ', Math.max(0, cw - Math.max(0, mid - Math.floor(lab.length / 2)) - lab.length));
    }
    var out = [head.replace(/\s+$/, '')];
    for (q = 0; q < n; q++) { out.push(rows[q]); if (q < n - 1) out.push(conns[q].replace(/\s+$/, '')); }
    return out.join('\n');
  }

  /* ---------- OpenQASM export ---------- */
  function toQasm(circ, ver) {
    ver = ver || 3; var L = [], n = circ.n, ms = circ.ops.filter(function (o) { return o.g === 'measure'; }), nb = ms.length ? Math.max.apply(0, ms.map(function (o) { return o.c; })) + 1 : 0;
    if (ver === 2) { L.push('OPENQASM 2.0;', 'include "qelib1.inc";', 'qreg q[' + n + '];'); if (nb) L.push('creg c[' + nb + '];'); }
    else { L.push('OPENQASM 3.0;', 'include "stdgates.inc";', 'qubit[' + n + '] q;'); if (nb) L.push('bit[' + nb + '] c;'); }
    var prevCol = -1;
    circ.sorted().forEach(function (op) {
      var qs = op.q.map(function (x) { return 'q[' + x + ']'; }), ang = op.p.map(fmtAngle), name = op.g;
      if (op.g === 'measure') { L.push(ver === 2 ? 'measure q[' + op.q[0] + '] -> c[' + op.c + '];' : 'c[' + op.c + '] = measure q[' + op.q[0] + '];'); return; }
      if (op.g === 'ccz') { var t = qs[2]; L.push('h ' + t + ';', 'ccx ' + qs.join(', ') + ';', 'h ' + t + ';'); return; }
      if (ver === 2) { if (name === 'p') name = 'u1'; if (name === 'cp') name = 'cu1'; }
      L.push(name + (ang.length ? '(' + ang.join(', ') + ')' : '') + ' ' + qs.join(', ') + ';');
    });
    return L.join('\n');
  }

  /* ---------- micro QASM import ---------- */
  var QASM_OK = 'h x y z s sdg t tdg sx sxdg rx ry rz p u1 cx cy cz ch swap cp cu1 ccx, id, measure, barrier';
  function fromQasm(src) {
    var text = String(src).replace(/\/\*[\s\S]*?\*\//g, function (m) { return m.replace(/[^\n]/g, ' '); }), lines = text.split('\n'), stmts = [], buf = '', startLine = 1, k;
    lines.forEach(function (ln, i) { ln = ln.replace(/\/\/.*$/, ''); var parts = ln.split(';');
      parts.forEach(function (p, j) { if (!buf.trim()) startLine = i + 1; buf += (buf ? ' ' : '') + p;
        if (j < parts.length - 1) { if (buf.trim()) stmts.push([buf.trim(), startLine]); buf = ''; } }); });
    if (buf.trim() && !/^[}\s]*$/.test(buf)) { var bw = /^(gate|def|for|while|if|reset|opaque|let|const|int|float|bool|input|output|array|extern|cal|defcal)\b/.exec(buf.trim());
      if (bw) throw new Error('line ' + startLine + ': microQASM does not support "' + bw[1] + '" yet. It reads these gates: ' + QASM_OK + '.');
      throw new Error('line ' + lines.length + ': the last line needs a ; at the end'); }
    var qregs = {}, cregs = {}, nq = 0, nc = 0, pending = [], breaks = {}, ver = 3;
    function fail(l, msg) { throw new Error('line ' + l + ': ' + msg); }
    function ref(s, regs, l, what) {
      var m = /^([A-Za-z_]\w*)(?:\[(\d+)\])?$/.exec(s.trim()); if (!m) fail(l, 'I cannot read "' + s.trim() + '"');
      var r = regs[m[1]]; if (!r) fail(l, 'there is no ' + what + ' called "' + m[1] + '" (declare it first)');
      if (m[2] === undefined) { var all = [], i; for (i = 0; i < r.size; i++) all.push(r.off + i); return all; }
      if (+m[2] >= r.size) fail(l, m[1] + '[' + m[2] + '] is out of range, ' + m[1] + ' has ' + r.size + ' ' + what + 's'); return [r.off + +m[2]];
    }
    stmts.forEach(function (st) {
      var s = st[0], l = st[1], m;
      if ((m = /^OPENQASM\s+(\d)(\.\d+)?$/i.exec(s))) { ver = +m[1]; if (ver !== 2 && ver !== 3) fail(l, 'microQASM reads OpenQASM 2 and 3'); return; }
      if (/^include\b/.test(s)) return;
      if ((m = /^qubit(?:\[(\d+)\])?\s+([A-Za-z_]\w*)$/.exec(s)) || (m = /^qreg\s+([A-Za-z_]\w*)\[(\d+)\]$/.exec(s))) {
        var isQreg = /^qreg/.test(s), name = isQreg ? m[1] : m[2], size = isQreg ? +m[2] : (m[1] === undefined ? 1 : +m[1]); qregs[name] = { off: nq, size: size }; nq += size; return; }
      if ((m = /^bit(?:\[(\d+)\])?\s+([A-Za-z_]\w*)$/.exec(s)) || (m = /^creg\s+([A-Za-z_]\w*)\[(\d+)\]$/.exec(s))) {
        var isCreg = /^creg/.test(s), cn = isCreg ? m[1] : m[2], cs = isCreg ? +m[2] : (m[1] === undefined ? 1 : +m[1]); cregs[cn] = { off: nc, size: cs }; nc += cs; return; }
      if ((m = /^barrier\b/.exec(s))) { breaks[pending.length] = 1; return; }
      var mm = /^(?:(.+?)\s*=\s*)?measure\s+([^>]+?)(?:\s*->\s*(.+))?$/.exec(s);
      if (mm) {
        var target = mm[1] || mm[3], qs = ref(mm[2], qregs, l, 'qubit'), cs2;
        if (target) { cs2 = ref(target, cregs, l, 'bit'); if (cs2.length !== qs.length) fail(l, 'measure needs the same number of qubits and bits'); }
        else { cs2 = qs.map(function (x, i) { return i; }); }
        qs.forEach(function (q, i) { pending.push({ g: 'measure', q: [q], p: [], c: cs2[i] }); }); return; }
      if (/^(gate|def|for|while|if|reset|opaque|let|const|int|float|bool|input|output|array|extern|cal|defcal)\b/.test(s)) fail(l, 'microQASM does not support "' + s.split(/\s|\(/)[0] + '" yet. It reads these gates: ' + QASM_OK + '.');
      m = /^([A-Za-z_]\w*)\s*(?:\(([^)]*)\))?\s*(.+)$/.exec(s);
      if (!m) fail(l, 'I could not read this line: "' + s + '"');
      var gname = m[1].toLowerCase(); gname = ALIAS[gname] || gname; var gd = GATES[gname];
      if (!gd || gname === 'measure' || gname === 'ccz') fail(l, 'microQASM does not know the gate "' + m[1] + '". It reads: ' + QASM_OK + '.');
      var params; try { params = m[2] !== undefined && m[2].trim() ? m[2].split(',').map(parseAngle) : []; } catch (e) { fail(l, e.message); }
      if (params.length !== gd.np) fail(l, gname + ' needs ' + gd.np + ' angle' + (gd.np === 1 ? '' : 's') + (gd.np ? ', like ' + gname + '(pi/2)' : ' and none were given'));
      var args = m[3].split(',').map(function (a) { return ref(a, qregs, l, 'qubit'); });
      if (args.length !== gd.nq) fail(l, gname + ' needs ' + gd.nq + ' qubit' + (gd.nq > 1 ? 's' : '') + ' but got ' + args.length);
      var len = Math.max.apply(0, args.map(function (a) { return a.length; })), i;
      for (i = 0; i < len; i++) { var qq = args.map(function (a) { return a.length === 1 ? a[0] : a[i]; }); pending.push({ g: gname, q: qq, p: params, line: l }); }
    });
    if (!nq) throw new Error('no qubits declared. Start with: OPENQASM 3.0; then qubit[2] q;');
    var c = new Circuit(nq);
    pending.forEach(function (o) { try { c.add(o.g, o.q, o.p, 0); if (o.g === 'measure') c.ops[c.ops.length - 1].c = o.c; } catch (e) { throw new Error('line ' + (o.line || '?') + ': ' + e.message); } });
    c.layout(breaks); return c;
  }

  /* ---------- MicroQiskit (Python) code ---------- */
  function toPython(circ, extra) {
    var ms = circ.ops.filter(function (o) { return o.g === 'measure'; }), nb = ms.length ? Math.max.apply(0, ms.map(function (o) { return o.c; })) + 1 : 0, L = [], usesPi = false, body = [];
    function ang(a) { var s = fmtAngle(a); if (/pi/.test(s)) { usesPi = true; return s; } return s; }
    circ.sorted().forEach(function (op) {
      var g = op.g, a = op.p.map(ang), q = op.q;
      if (g === 'measure') { body.push('qc.measure(' + q[0] + ', ' + op.c + ')'); return; }
      if (g === 'i') return;
      if (g === 'ccz') { body.push('qc.h(' + q[2] + ')', 'qc.ccx(' + q.join(', ') + ')', 'qc.h(' + q[2] + ')'); return; }
      var args = a.concat(q.map(String)); body.push('qc.' + g + '(' + args.join(', ') + ')');
    });
    L.push('from microqiskit import QuantumCircuit, simulate'); if (usesPi) L.push('from math import pi');
    L.push('', 'qc = QuantumCircuit(' + circ.n + (nb ? ', ' + nb : '') + ')'); L = L.concat(body);
    L.push('', "print(simulate(qc, 1000, 'counts'))"); if (extra) L.push(extra); return L.join('\n');
  }

  /* ---------- goals (declarative checks, so a course can ship them as JSON) ---------- */
  // goal: { probs:[{state:"11", min:0.99} | {state:"0", approx:0.5, tol:0.02}], gates:{min,max,only:[],require:[],forbid:[]}, linked:true|false, start:"..." }
  function check(goal, circ, res) {
    goal = goal || {}; var why = [], ok = true;
    (goal.probs || []).forEach(function (t) {
      var p = 0, i; res.probs.forEach(function (x, i) { if (label(i, res.n).indexOf(t.state) === 0) p += x; });
      var good = t.min !== undefined ? p >= t.min : t.max !== undefined ? p <= t.max : Math.abs(p - t.approx) <= (t.tol === undefined ? 0.02 : t.tol);
      if (!good) { ok = false; why.push(t.hint || ('|' + t.state + '⟩ is ' + Math.round(p * 100) + '%')); }
    });
    var gs = goal.gates; if (gs) {
      var cnt = circ.counts(), real = Object.keys(cnt).filter(function (g) { return g !== 'i'; }), total = 0; real.forEach(function (g) { total += cnt[g]; });
      if (gs.min !== undefined && total < gs.min) { ok = false; why.push('use at least ' + gs.min + ' gate' + (gs.min > 1 ? 's' : '')); }
      if (gs.max !== undefined && total > gs.max) { ok = false; why.push('use at most ' + gs.max + ' gates'); }
      if (gs.only) real.forEach(function (g) { if (gs.only.indexOf(g) < 0 && !(g === 'measure' && gs.only.indexOf('m') >= 0)) { ok = false; why.push('only these gates are allowed: ' + gs.only.join(', ')); } });
      (gs.require || []).forEach(function (g) { if (!cnt[g]) { ok = false; why.push('you need a ' + g + ' gate'); } });
      (gs.forbid || []).forEach(function (g) { if (cnt[g]) { ok = false; why.push('no ' + g + ' gates this time'); } });
      Object.keys(gs.count || {}).forEach(function (g) { var r = gs.count[g], v = cnt[g] || 0; if (r.min !== undefined && v < r.min) { ok = false; why.push('use at least ' + r.min + ' ' + g); } if (r.max !== undefined && v > r.max) { ok = false; why.push('use at most ' + r.max + ' ' + g); } });
    }
    if (goal.linked !== undefined) { var has = circ.ops.some(function (o) { return o.q.length > 1; }); if (has !== goal.linked) { ok = false; why.push(goal.linked ? 'link two qubits with a CNOT or CZ' : 'no linking gates this time'); } }
    return { ok: ok, why: why };
  }

  QWL.Circuit = Circuit; QWL.GATES = GATES; QWL.ALIAS = ALIAS; QWL.parseAngle = parseAngle; QWL.fmtAngle = fmtAngle; QWL.simulate = simulate; QWL.label = label; QWL.marginals = marginals; QWL.bloch = bloch;
  QWL.sample = sample; QWL.rng = rng; QWL.fromText = fromText; QWL.toText = toText; QWL.toDiagram = toDiagram; QWL.toQasm = toQasm; QWL.fromQasm = fromQasm; QWL.toPython = toPython; QWL.check = check; QWL.MAXQ = MAXQ;
  if (typeof module !== 'undefined') module.exports = QWL;
})(typeof window !== 'undefined' ? window : globalThis);
