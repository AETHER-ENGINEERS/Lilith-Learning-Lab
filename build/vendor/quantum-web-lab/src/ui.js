/*! quantum-web-lab UI | MIT | QWL.mount(element, config) draws an IBM-composer style, phone-friendly circuit lab. */
(function (root) {
  'use strict';
  var QWL = root.QWL, G = QWL.GATES;
  var DEFAULTS = {
    title: '', intro: '', qubits: 2, steps: 6, maxQubits: 5, maxSteps: 14, start: '', startQasm: '', startPython: '',
    palette: ['h', 'x', 'y', 'z', 's', 't', 'cx', 'cz', 'swap', 'ccx', 'rx', 'ry', 'rz', 'p', 'sdg', 'tdg', 'sx', 'measure'],
    results: ['chances', 'shots', 'inspect'], code: ['python', 'qasm', 'text', 'ascii'], codeOpen: false, console: true, python: true, levels: null, seed: 1, shots: 1024,
    chips: ['h 0', 'x 0', 'cx 0 1', 'run', 'shots 20', 'undo', 'help']
  };
  var TABNAME = { python: 'Python', qasm: 'OpenQASM', text: 'Q text', ascii: 'ASCII' };
  var ANG = ['pi/4', 'pi/2', 'pi', '3*pi/2'];
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function h(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }

  QWL.mount = function (el, cfg) {
    cfg = Object.assign({}, DEFAULTS, cfg || {});
    var S = { c: null, res: null, tool: cfg.palette[0] || 'h', pend: null, undo: [], redo: [], angle: 'pi/2', rtab: cfg.resultsTab || cfg.results[0], ctab: cfg.codeTab || cfg.code[0], left: true, uni: true, dirty: false, seed: cfg.seed, shots: cfg.shots, counts: null, li: 0, solved: {}, pending: false, completed: false, chart: 'chances', via: 'composer' };
    var $ = function (id) { return el.querySelector('#' + id); };
    el.classList.add('qwl'); el.innerHTML = '';
    var P = cfg.palette.filter(function (g) { return G[g]; });

    /* ---------- skeleton ---------- */
    var html = '';
    if (cfg.title || cfg.intro) html += '<div class="card" id="hd">' + (cfg.title ? '<h2>' + esc(cfg.title) + '</h2>' : '') + (cfg.intro ? '<div class="k">' + cfg.intro + '</div>' : '') + '</div>';
    if (cfg.levels) html += '<div class="card" id="lv"><h2 id="lt"></h2><div class="k" id="li"></div></div>';
    html += '<div class="card"><div class="pal" id="pal"></div><div class="aprow" id="aprow" style="display:none"></div><div class="tip" id="tip"></div><div class="gw"><div class="grid" id="grid"></div></div>' +
      '<div class="tools"><button class="ic" id="uq" title="Fewer qubits">&minus;</button><span class="k">qubits</span><button class="ic" id="aq" title="More qubits">+</button>' +
      '<button class="ic" id="us" title="Fewer steps">&minus;</button><span class="k">steps</span><button class="ic" id="as" title="More steps">+</button><span class="sp"></span>' +
      '<button class="ic" id="undo" title="Undo">&#x21B6;</button><button class="ic" id="redo" title="Redo">&#x21B7;</button><button class="ic" id="clr" title="Clear">&#x2715;</button></div></div>';
    if (cfg.levels) html += '<div id="status" class="card"></div>';
    html += '<div class="card"><div id="rtabs"></div><div id="rbody"></div></div>';
    if (cfg.levels) html += '<div id="lbtn"><button class="ab" id="next" style="display:none">Next level</button><button class="ab s" id="reset">Reset</button><button class="ab s" id="hint">Hint</button><button class="ab s" id="solbtn">Show a solution</button></div><div id="sol"></div>';
    if (cfg.code.length) html += '<div class="card"><details id="codebox"' + (cfg.codeOpen ? ' open' : '') + '><summary>Code for this circuit</summary><div id="ctabs" style="margin-top:6px"></div><div id="cbody"></div></details></div>';
    if (cfg.console) html += '<div class="card"><details open><summary>&#x1F5A5;&#xFE0F; Q Console: type commands</summary><div class="out" id="out" style="margin-top:6px"></div><div id="chips" style="margin-top:6px"></div><div class="crow"><input id="cmd" type="text" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="Type a command, like  h 0"><button class="ab" id="go" style="margin:0">Go</button></div></details></div>';
    el.innerHTML = html;

    /* ---------- circuit state ---------- */
    function snap() { return JSON.stringify({ n: S.c.n, cols: S.c.cols, ops: S.c.ops }); }
    function load(s) { var o = JSON.parse(s), c = new QWL.Circuit(o.n); c.cols = o.cols; c.ops = o.ops; return c; }
    function evalAll() { S.res = QWL.simulate(S.c); S.counts = null; }
    function setCircuit(c, record) {
      if (c.cols < 1) c.cols = 1; if (c.cols < cfg.steps && !record) c.cols = Math.max(c.cols, cfg.steps);
      if (record !== false && S.c) { S.undo.push(snap()); if (S.undo.length > 80) S.undo.shift(); S.redo = []; }
      S.c = c; S.pend = null; S.dirty = false; evalAll(); render(); afterChange();
    }
    function edit(fn, fromCon) { var c = S.c.clone(); fn(c); S.via = fromCon ? 'console' : 'composer'; if (fromCon) S.pending = true; setCircuit(c, true); }
    function doUndo() { if (!S.undo.length) return false; S.redo.push(snap()); S.c = load(S.undo.pop()); S.pend = null; S.dirty = false; evalAll(); render(); afterChange(); return true; }
    function doRedo() { if (!S.redo.length) return false; S.undo.push(snap()); S.c = load(S.redo.pop()); S.pend = null; S.dirty = false; evalAll(); render(); afterChange(); return true; }
    function removeAt(c, q, col) { c.ops = c.ops.filter(function (o) { return !(o.col === col && o.q.indexOf(q) >= 0); }); }
    function fit(c, need) { while (c.cols < need) c.cols++; }

    /* ---------- palette & tips ---------- */
    function buildPal() {
      var b = '';
      P.forEach(function (g) { var d = G[g], t = d.name || d.sym; b += '<button class="gb ' + d.grp + (g === S.tool ? ' on' : '') + '" data-g="' + g + '" title="' + esc(d.info) + '">' + esc(t) + '</button>'; });
      b += '<button class="gb erase' + (S.tool === 'erase' ? ' on' : '') + '" data-g="erase">Erase</button>';
      $('pal').innerHTML = b;
      Array.prototype.forEach.call($('pal').querySelectorAll('.gb'), function (e) { e.onclick = function () { S.tool = e.getAttribute('data-g'); S.pend = null; buildPal(); render(); }; });
      var d = G[S.tool], ar = $('aprow');
      if (d && d.np) { var a = '<span class="k">Angle:</span>'; ANG.forEach(function (x) { a += '<button class="chip' + (x === S.angle ? ' on' : '') + '" data-a="' + x + '">' + x.replace('pi', 'π') + '</button>'; });
        a += '<input id="angin" value="' + esc(S.angle) + '" aria-label="angle, like pi/3 or 45deg">'; ar.innerHTML = a; ar.style.display = 'flex';
        Array.prototype.forEach.call(ar.querySelectorAll('.chip'), function (e) { e.onclick = function () { S.angle = e.getAttribute('data-a'); buildPal(); }; });
        $('angin').onchange = function () { try { QWL.parseAngle(this.value); S.angle = this.value; } catch (e) { tip(e.message, true); } buildPal(); };
      } else ar.style.display = 'none';
    }
    var tipMsg = null;
    function tip(msg, bad) { tipMsg = msg; var t = $('tip'); t.textContent = msg; t.className = 'tip' + (bad ? ' bad' : ''); }
    function defaultTip() {
      if (S.tool === 'erase') return 'Tap a gate to remove it.'; var d = G[S.tool]; if (!d) return '';
      if (d.nq === 1) return d.info + ' Tap a square on a wire.';
      if (S.pend) return 'Now tap ' + (d.ctrl ? (S.pend.qs.length < d.ctrl[1] ? 'the next control' : 'the target') : 'the other qubit') + ' in the same step.';
      return d.info + ' Tap ' + (d.ctrl ? 'a control' : 'a qubit') + ', then the rest in the same step.';
    }

    /* ---------- grid ---------- */
    function cellView(op, q) {
      var d = G[op.g];
      if (op.g === 'swap') return '<span class="sw">×</span>';
      if (d.ctrl) { var i = op.q.indexOf(q), isT = i === op.q.length - 1, base = d.ctrl[0];
        if (!isT) return '<span class="dot"></span>';
        if (base === 'x') return '<span class="tg">+</span>'; if (base === 'z') return '<span class="dot"></span>';
        return '<span class="g ctl">' + G[base].sym + (d.np ? '<small>' + esc(QWL.fmtAngle(op.p[0]).replace('pi', 'π')) + '</small>' : '') + '</span>'; }
      return '<span class="g ' + d.grp + '">' + d.sym + (d.np ? '<small>' + esc(QWL.fmtAngle(op.p[0]).replace('pi', 'π')) + '</small>' : '') + '</span>';
    }
    function render() {
      var c = S.c, n = c.n, m = c.cols, hh = '', q, k;
      for (q = 0; q < n; q++) { hh += '<div class="row"><div class="lab">q[' + q + ']</div>';
        for (k = 0; k < m; k++) { var op = c.opAt(q, k), sel = S.pend && S.pend.col === k && S.pend.qs.indexOf(q) >= 0, inner = op ? cellView(op, q) : (sel ? '<span class="dot"></span>' : '');
          hh += '<div class="cell' + (op || sel ? ' has' : '') + (sel ? ' sel' : '') + '" data-r="' + q + '" data-c="' + k + '">' + inner + '</div>'; }
        hh += '<div class="ring" id="ring' + q + '"></div></div>'; }
      c.ops.forEach(function (op) { if (op.q.length > 1) { var lo = Math.min.apply(0, op.q), hi = Math.max.apply(0, op.q);
        hh += '<div class="ln" style="left:' + (46 + op.col * 42 + 21) + 'px;top:' + (lo * 44 + 22) + 'px;height:' + ((hi - lo) * 44) + 'px"></div>'; } });
      $('grid').innerHTML = hh;
      Array.prototype.forEach.call($('grid').querySelectorAll('.cell'), function (e) { e.onclick = function () { tapCell(+e.getAttribute('data-r'), +e.getAttribute('data-c')); }; });
      $('undo').disabled = !S.undo.length; $('redo').disabled = !S.redo.length; $('uq').disabled = n <= 1; $('aq').disabled = n >= cfg.maxQubits; $('us').disabled = m <= 1; $('as').disabled = m >= cfg.maxSteps;
      buildPal(); tip(defaultTip()); paintRings(); paintResults(); paintCode();
    }
    function paintRings() { var mg = QWL.marginals(S.res); mg.forEach(function (p, i) { var e = $('ring' + i); if (e) e.style.background = 'conic-gradient(var(--qb-acc) ' + Math.round(p * 360) + 'deg,transparent 0deg)'; }); }
    function tapCell(r, col) {
      var T = S.tool, d = G[T];
      if (T === 'erase') return edit(function (c) { removeAt(c, r, col); });
      if (!d) return;
      if (d.nq === 1) { var ex = S.c.opAt(r, col), pr = d.np ? [QWL.parseAngle(S.angle)] : [];
        if (ex && ex.g === T && (!d.np || Math.abs(ex.p[0] - pr[0]) < 1e-9)) return edit(function (c) { removeAt(c, r, col); });
        try { return edit(function (c) { removeAt(c, r, col); c.add(T, [r], pr, col); if (T === 'measure') c.ops[c.ops.length - 1].c = r; }); } catch (e) { return tip(e.message, true); } }
      if (!S.pend || S.pend.col !== col) S.pend = { col: col, qs: [] };
      var at = S.pend.qs.indexOf(r); if (at >= 0) { S.pend = null; return render(); }
      S.pend.qs.push(r);
      if (S.pend.qs.length < d.nq) return render();
      var qs = S.pend.qs.slice(), lo = Math.min.apply(0, qs), hi = Math.max.apply(0, qs), pr2 = d.np ? [QWL.parseAngle(S.angle)] : [];
      edit(function (c) { c.ops = c.ops.filter(function (o) { return !(o.col === col && o.q.some(function (x) { return qs.indexOf(x) >= 0; })); }); c.add(T, qs, pr2, col); });
    }

    /* ---------- results ---------- */
    function lab(i) { var s = QWL.label(i, S.res.n); return S.left ? s : s.split('').reverse().join(''); }
    function paintResults() {
      var tabs = '', body = '', res = S.res, n = res.n;
      cfg.results.forEach(function (t) { tabs += '<button class="chip' + (t === S.rtab ? ' on' : '') + '" data-t="' + t + '">' + { chances: 'Chances', shots: 'Shots', inspect: 'Inspect' }[t] + '</button>'; });
      tabs += '<button class="chip" id="bo" title="Which side qubit 0 is on">q0 on the ' + (S.left ? 'left' : 'right') + '</button>';
      $('rtabs').innerHTML = tabs;
      Array.prototype.forEach.call($('rtabs').querySelectorAll('[data-t]'), function (e) { e.onclick = function () { S.rtab = e.getAttribute('data-t'); paintResults(); }; });
      $('bo').onclick = function () { S.left = !S.left; paintResults(); paintCode(); };
      function chart(vals, fmt) { var hh = '', rows = []; vals.forEach(function (v, i) { rows.push([i, v]); });
        if (n > 3) rows = rows.filter(function (r) { return r[1] > 0.0005; }); if (rows.length > 40) rows.length = 40;
        rows.forEach(function (r) { hh += '<div class="bc"><span class="v">' + fmt(r[1]) + '</span><div class="b" style="height:' + Math.round(Math.min(1, r[1] / (vals.max || 1)) * 92) + 'px"></div><span class="l">' + lab(r[0]) + '</span></div>'; }); return '<div class="chart">' + hh + '</div>'; }
      if (S.rtab === 'chances') { var pv = res.probs.slice(); pv.max = 1; body = chart(pv, function (v) { return Math.round(v * 100) + '%'; }); }
      else if (S.rtab === 'shots') {
        body = '<div><button class="ab" id="rs" style="margin:0 6px 0 0">Run ' + S.shots + ' shots</button><span class="k">seed</span> <button class="ic" id="sd" style="width:auto;padding:0 12px;border-radius:8px">' + S.seed + '</button></div>';
        if (S.counts) { var tot = 0, mx = 0, arr = []; Object.keys(S.counts).sort().forEach(function (k) { tot += S.counts[k]; if (S.counts[k] > mx) mx = S.counts[k]; arr.push(k); });
          var hh = ''; arr.forEach(function (k) { var key = S.left ? k : k.split('').reverse().join(''); hh += '<div class="bc"><span class="v">' + S.counts[k] + '</span><div class="b" style="height:' + Math.round(S.counts[k] / mx * 92) + 'px"></div><span class="l">' + key + '</span></div>'; });
          body += '<div class="chart" style="margin-top:6px">' + hh + '</div><div class="k">' + tot + ' shots. The same seed always gives the same shots.</div>'; }
        else body += '<div class="k" style="margin-top:6px">Each shot measures the circuit once. Run many shots to see the chances appear.</div>';
      } else {
        var rowsH = '', i; for (i = 0; i < res.probs.length; i++) { if (res.probs[i] < 1e-6 && n > 3) continue; var re = res.re[i], im = res.im[i], mag = Math.sqrt(res.probs[i]), ph = Math.atan2(im, re);
          var dial = '<svg width="26" height="26" viewBox="-13 -13 26 26"><circle r="11" fill="none" stroke="#3a2d55"/>' + (mag > 1e-6 ? '<line x1="0" y1="0" x2="' + (10 * Math.cos(ph)).toFixed(2) + '" y2="' + (-10 * Math.sin(ph)).toFixed(2) + '" stroke="hsl(' + Math.round((ph * 180 / Math.PI + 360) % 360) + ',80%,65%)" stroke-width="2.5" stroke-linecap="round"/>' : '') + '</svg>';
          rowsH += '<tr><td>|' + lab(i) + '⟩</td><td><span class="mag" style="width:' + Math.round(mag * 60) + 'px"></span> ' + mag.toFixed(3) + '</td><td>' + dial + '</td><td>' + (mag > 1e-6 ? Math.round(ph * 180 / Math.PI) + '°' : '') + '</td><td>' + Math.round(res.probs[i] * 100) + '%</td></tr>'; }
        var bl = ''; for (i = 0; i < n; i++) { var b = QWL.bloch(res, i), len = Math.sqrt(b.x * b.x + b.y * b.y + b.z * b.z);
          bl += '<div class="bl"><svg width="44" height="44" viewBox="-22 -22 44 44"><circle r="19" fill="none" stroke="#3a2d55"/><line x1="-19" y1="0" x2="19" y2="0" stroke="#3a2d55" stroke-dasharray="2 3"/><line x1="0" y1="-19" x2="0" y2="19" stroke="#3a2d55" stroke-dasharray="2 3"/><line x1="0" y1="0" x2="' + (19 * b.x).toFixed(1) + '" y2="' + (-19 * b.z).toFixed(1) + '" stroke="#d9acff" stroke-width="2"/><circle cx="' + (19 * b.x).toFixed(1) + '" cy="' + (-19 * b.z).toFixed(1) + '" r="3" fill="#e06aa8"/></svg><div>q[' + i + ']' + (len < 0.98 ? '<br>shared (' + len.toFixed(2) + ')' : '') + '</div></div>'; }
        body = '<table class="st"><tr class="k"><td>state</td><td>size</td><td>phase</td><td></td><td>chance</td></tr>' + rowsH + '</table><div class="k" style="margin-top:6px">The little arrow shows the phase. A qubit that is shared with others (entangled) has a short arrow below.</div><div class="blochs">' + bl + '</div>';
      }
      $('rbody').innerHTML = body;
      if ($('rs')) { $('rs').onclick = function () { S.counts = QWL.sample(S.c, S.res, S.shots, S.seed); paintResults(); if (cfg.complete === 'shots') complete(); }; $('sd').onclick = function () { S.seed = S.seed % 99 + 1; S.counts = null; paintResults(); }; }
    }

    /* ---------- code panel ---------- */
    var pyOut = '';
    function codeText(t) { return t === 'python' ? QWL.toPython(S.c) : t === 'qasm' ? QWL.toQasm(S.c) : t === 'text' ? QWL.toText(S.c) : QWL.toDiagram(S.c, { unicode: S.uni }); }
    function paintCode() {
      if (!cfg.code.length || !$('ctabs')) return;
      var tabs = ''; cfg.code.forEach(function (t) { tabs += '<button class="chip' + (t === S.ctab ? ' on' : '') + '" data-c="' + t + '">' + TABNAME[t] + '</button>'; });
      $('ctabs').innerHTML = tabs;
      Array.prototype.forEach.call($('ctabs').querySelectorAll('.chip'), function (e) { e.onclick = function () { S.ctab = e.getAttribute('data-c'); S.dirty = false; pyOut = ''; paintCode(); }; });
      var t = S.ctab, body, note = '';
      if (t === 'ascii') { body = '<pre id="code">' + esc(codeText(t)) + '</pre><button class="chip' + (S.uni ? '' : ' on') + '" id="uni">Plain ASCII only</button><button class="chip" id="cp">Copy</button>'; note = 'A text picture of the circuit. Time runs to the right. ● is a control and (+) a target.'; }
      else { body = '<textarea class="code" id="code" spellcheck="false" autocapitalize="none" autocomplete="off">' + esc(codeText(t)) + '</textarea>' +
        '<div><button class="ab" id="apply">' + (t === 'python' ? '▶ Run' : 'Apply') + '</button><button class="chip" id="cp">Copy</button></div><div id="cmsg"></div>' + (t === 'python' ? '<pre id="pout" style="display:none"></pre>' : '');
        note = t === 'python' ? 'MicroQiskit, a tiny Qiskit that runs right here. Edit it and press Run: the circuit above follows your code. Qiskit puts qubit 0 on the right of a result.' : t === 'qasm' ? 'OpenQASM 3 (and 2) text. Edit it and press Apply. microQASM reads the common gates and measure.' : 'Q.js style text: rows are qubits, columns are steps. X#0 and X#1 make a CNOT. You can edit it too.'; }
      $('cbody').innerHTML = body + '<div class="k" style="margin-top:4px">' + note + '</div>';
      var ta = $('code'); if (ta && ta.tagName === 'TEXTAREA') { ta.oninput = function () { S.dirty = true; };
        ta.onkeydown = function (e) { if (e.key === 'Tab') { e.preventDefault(); var s = ta.selectionStart; ta.value = ta.value.slice(0, s) + '    ' + ta.value.slice(ta.selectionEnd); ta.selectionStart = ta.selectionEnd = s + 4; } }; }
      if ($('uni')) $('uni').onclick = function () { S.uni = !S.uni; paintCode(); };
      if ($('cp')) $('cp').onclick = function () { var txt = ta ? ta.value : $('code').textContent, b = this; try { navigator.clipboard.writeText(txt).then(function () { b.textContent = 'Copied'; }, function () { b.textContent = 'Select and copy'; }); } catch (e) { b.textContent = 'Select and copy'; } setTimeout(function () { b.textContent = 'Copy'; }, 1500); };
      if ($('apply')) $('apply').onclick = applyCode;
      if (pyOut && $('pout')) { $('pout').style.display = 'block'; $('pout').textContent = pyOut; }
    }
    function cmsg(m, bad) { var e = $('cmsg'); if (e) e.innerHTML = '<span class="' + (bad ? 'bad' : 'ok') + '">' + esc(m) + '</span>'; }
    function applyCode() {
      var t = S.ctab, src = $('code').value, c;
      function take(c2, ok) { S.via = t; if (c2.n > cfg.maxQubits) throw new Error('This lab allows up to ' + cfg.maxQubits + ' qubits.'); if (c2.cols > cfg.maxSteps) cfg.maxSteps = c2.cols; setCircuit(c2, true); cmsg(ok || 'Done. The circuit now matches your code.', false); }
      try {
        if (t === 'text') { c = QWL.fromText(src); take(c); }
        else if (t === 'qasm') { c = QWL.fromQasm(src); take(c); }
        else if (t === 'python') {
          if (!QWL.py || !QWL.py.available()) { cmsg('Python is not available in this build. Use the OpenQASM or Q text tab.', true); return; }
          $('apply').disabled = true; $('apply').textContent = 'Running...';
          QWL.py.run(src).then(function (r) { pyOut = (r.out || '').trim(); var btn = $('apply'); if (btn) { btn.disabled = false; btn.textContent = '▶ Run'; }
            if (r.err) { paintCode(); $('code').value = src; S.dirty = true; cmsg(r.err, true); return; }
            try { if (!r.qasm) throw new Error('Your code did not make a QuantumCircuit. Try: qc = QuantumCircuit(2)'); var c3 = QWL.fromQasm(r.qasm); S.via = 'python'; if (c3.n > cfg.maxQubits) throw new Error('This lab allows up to ' + cfg.maxQubits + ' qubits.'); var keep = src; if (c3.cols > cfg.maxSteps) cfg.maxSteps = c3.cols; setCircuit(c3, true); $('code').value = keep; S.dirty = true; if ($('pout')) { $('pout').style.display = pyOut ? 'block' : 'none'; $('pout').textContent = pyOut; } cmsg('Ran fine. The circuit above follows your code.', false); }
            catch (e) { cmsg(e.message, true); } });
        }
      } catch (e) { cmsg(e.message, true); }
    }

    /* ---------- levels ---------- */
    function checkLevel() {
      if (!cfg.levels) return; var L = cfg.levels[S.li], r = QWL.check(L.goal, S.c, S.res), st = $('status');
      if (r.ok && L.goal && L.goal.via && S.via !== L.goal.via) { r = { ok: false, why: ['build it in the ' + ({ python: 'Python', qasm: 'OpenQASM', text: 'Q text' }[L.goal.via] || L.goal.via) + ' tab (open "Code for this circuit")'] }; }
      if (r.ok) { st.innerHTML = '<span class="ok">Solved!</span> ' + esc(L.after || ''); if (!S.solved[S.li]) { S.solved[S.li] = 1; if (Object.keys(S.solved).length >= cfg.levels.length) complete(); }
        $('next').style.display = S.li < cfg.levels.length - 1 ? '' : 'none'; }
      else st.innerHTML = '<span class="k">Not yet.' + (r.why.length ? ' ' + esc(r.why[0]) + '.' : '') + '</span>';
    }
    function showLevel(i) {
      var L = cfg.levels[i]; S.li = i; $('lt').innerHTML = 'Level ' + (i + 1) + ' of ' + cfg.levels.length + ': ' + esc(L.title); $('li').innerHTML = L.intro || ''; $('sol').innerHTML = ''; $('next').style.display = 'none';
      var c = L.startQasm ? QWL.fromQasm(L.startQasm) : QWL.fromText(L.start || 'I'); if (L.qubits && c.n < L.qubits) { c = QWL.fromText(L.start || 'I'); }
      S.undo = []; S.redo = []; if (c.cols < cfg.steps) c.cols = cfg.steps; S.via = 'composer'; setCircuit(c, false); S.via = 'composer';
    }
    function complete() { if (S.completed) return; S.completed = true; try { if (cfg.onComplete) cfg.onComplete(); else if (root.lilith && root.lilith.complete) root.lilith.complete(); } catch (e) {} }
    function afterChange() { if (cfg.levels) checkLevel(); if (S.pending) { S.pending = false; conPrint(); } if (cfg.complete === 'run' && S.c.ops.length) complete(); }

    /* ---------- console ---------- */
    function say(html, cls) { var o = $('out'); if (!o) return; var d = h('div', cls || '', html); o.appendChild(d); o.scrollTop = o.scrollHeight; }
    function bar(p) { var n = Math.round(p * 20), s = ''; for (var i = 0; i < 20; i++) s += i < n ? '█' : '░'; return s; }
    function explain() {
      var r = S.res, big = []; r.probs.forEach(function (p, i) { if (p > 0.005) big.push([i, p]); });
      if (big.length === 1) return 'It always ends as |' + QWL.label(big[0][0], r.n) + '⟩. No luck involved.';
      var mg = QWL.marginals(r), ent = r.n > 1 && r.probs.some(function (p, i) { var pr = 1; for (var k = 0; k < r.n; k++) pr *= ((i >> (r.n - 1 - k)) & 1) ? mg[k] : 1 - mg[k]; return Math.abs(pr - p) > 0.02; });
      if (ent) return 'Entangled! The qubits are linked: knowing one tells you about the others.';
      var eq = big.every(function (b) { return Math.abs(b[1] - big[0][1]) < 0.02; });
      return eq ? 'A fair mix of ' + big.length + ' outcomes. That is superposition!' : 'A weighted mix: some outcomes are more likely than others.';
    }
    function conPrint() { var r = S.res, hh = ''; r.probs.forEach(function (p, i) { if (p >= 0.005 || r.probs.length <= 4) hh += '|' + QWL.label(i, r.n) + '⟩ ' + bar(p) + ' ' + Math.round(p * 100) + '%\n'; }); say(esc(hh), 'sys'); say('&#x1F4A1; ' + explain(), 'ok'); }
    function lastCol(c, lo, hi) { var m = 0; c.ops.forEach(function (o) { var a = Math.min.apply(0, o.q), b = Math.max.apply(0, o.q); if (b >= lo && a <= hi && o.col + 1 > m) m = o.col + 1; }); return m; }
    function helpText() { say('<b>Add a gate</b> (it goes in the first free step):\n  h 0       coin flip on qubit 0\n  x 1       flip qubit 1  (qubits count from 0)\n  rz pi/2 0   turn the phase\n  cx 0 1    qubit 0 controls qubit 1\n  ccx 0 1 2, cz 0 1, swap 0 1, m 0\n<b>See what happens</b>:\n  run       the chances\n  shots 20  measure it 20 times\n  show      draw it in text\n  qasm / python / text   see the code\n<b>Other</b>:\n  new 3     a fresh circuit with 3 qubits\n  clear, undo, redo, help', 'sys'); }
    function runCmd(line) {
      var raw = line.trim(); if (!raw) return; say('&#x203a; ' + esc(raw), 'you');
      var w = raw.replace(/^[>›$\s]+/, '').split(/[\s,]+/).filter(Boolean), c = w[0].toLowerCase(), m = w.length === 1 ? /^([a-z]+)(\d+)$/.exec(c) : null; if (m) { w = [m[1], m[2]]; c = m[1]; }
      var nm = { coin: 'h', flip: 'x', not: 'x', hadamard: 'h', cnot: 'cx', toffoli: 'ccx', m: 'measure', phase: 't' }[c] || c, name = G[nm] ? nm : (QWL.ALIAS[nm] || nm);
      if (c === 'help' || c === '?') return helpText();
      if (G[name]) { var d = G[name], args = w.slice(1), p = [];
        if (d.np) { if (!args.length) return say('&#x1F914; ' + name + ' needs an angle first, like <b>' + name + ' pi/2 0</b>.', 'bad'); try { p = [QWL.parseAngle(args.shift())]; } catch (e) { return say('&#x1F914; ' + esc(e.message), 'bad'); } }
        if (args.length !== d.nq) return say('&#x1F914; <b>' + name + '</b> needs ' + d.nq + ' qubit number' + (d.nq > 1 ? 's' : '') + ', like <b>' + name + (d.np ? ' pi/2' : '') + ' ' + (d.nq === 1 ? '0' : d.nq === 2 ? '0 1' : '0 1 2') + '</b>.', 'bad');
        var qs = args.map(Number), bad = qs.filter(function (x) { return !(x >= 0 && x < S.c.n && x === Math.floor(x)); });
        if (bad.length) return say('&#x1F914; This circuit has qubits 0 to ' + (S.c.n - 1) + '. Make a bigger one with <b>new 3</b>.', 'bad');
        if (cfg.palette.indexOf(name) < 0 && name !== 'measure') return say('&#x1F914; The ' + name + ' gate is not part of this lab.', 'bad');
        try { var lo = Math.min.apply(0, qs), hi = Math.max.apply(0, qs), col = lastCol(S.c, lo, hi); if (col >= cfg.maxSteps) throw new Error('The circuit is full. Try clear, or ask for fewer steps.');
          edit(function (cc) { fit(cc, col + 1); cc.add(name, qs, p, col); if (name === 'measure') cc.ops[cc.ops.length - 1].c = qs[0]; }, true); say('Added ' + (d.name || d.sym) + ' (step ' + (col + 1) + ').', 'sys'); } catch (e) { say('&#x1F914; ' + esc(e.message), 'bad'); } return; }
      if (c === 'run' || c === 'explain' || c === 'go') { S.pending = true; evalAll(); render(); afterChange(); return; }
      if (c === 'shots' || c === 'measure') { var k = Math.max(1, Math.min(5000, parseInt(w[1], 10) || 20)), cnt = QWL.sample(S.c, S.res, k, Math.floor(Math.random() * 1e6)), hh = 'Measured ' + k + ' times:\n';
        Object.keys(cnt).sort().forEach(function (s) { hh += '|' + (S.left ? s : s.split('').reverse().join('')) + '⟩ ' + '█'.repeat(Math.max(1, Math.round(cnt[s] / k * 24))) + ' ' + cnt[s] + '\n'; }); say(esc(hh), 'sys'); say('Every measurement gives one answer. The chances show up when you repeat it.', 'ok'); if (cfg.complete === 'shots') complete(); return; }
      if (c === 'show' || c === 'draw' || c === 'diagram') return say(esc(QWL.toDiagram(S.c, { unicode: S.uni })), 'sys');
      if (c === 'text') return say(esc(QWL.toText(S.c)), 'sys'); if (c === 'qasm') return say(esc(QWL.toQasm(S.c)), 'sys'); if (c === 'python') return say(esc(QWL.toPython(S.c)), 'sys');
      if (c === 'new' || c === 'qubits') { var nq = parseInt(w[1], 10) || 1; if (nq < 1 || nq > cfg.maxQubits) return say('&#x1F914; Pick 1 to ' + cfg.maxQubits + ' qubits.', 'bad'); var nc = new QWL.Circuit(nq); nc.cols = cfg.steps; S.pending = true; setCircuit(nc, true); return say('New circuit with ' + nq + ' qubit' + (nq > 1 ? 's' : '') + ', all starting as 0.', 'sys'); }
      if (c === 'clear' || c === 'reset') { var cl = S.c.clone(); cl.ops = []; S.pending = true; setCircuit(cl, true); return say('Cleared.', 'sys'); }
      if (c === 'undo') { S.pending = true; if (!doUndo()) { S.pending = false; return say('Nothing to undo.', 'bad'); } return say('Undone.', 'sys'); }
      if (c === 'redo') { if (!doRedo()) return say('Nothing to redo.', 'bad'); return say('Redone.', 'sys'); }
      var guess = ['help', 'run', 'shots', 'show', 'text', 'new', 'clear', 'undo', 'h', 'x', 'cx'], near = ''; guess.forEach(function (x) { if (!near && x.charAt(0) === c.charAt(0)) near = x; });
      say('&#x1F914; I do not know <b>' + esc(c) + '</b> yet.' + (near ? ' Did you mean <b>' + near + '</b>?' : '') + ' Type <b>help</b> to see what I know.', 'bad');
    }

    /* ---------- wiring ---------- */
    $('aq').onclick = function () { edit(function (c) { c.n++; }); };
    $('uq').onclick = function () { edit(function (c) { var last = c.n - 1; c.ops = c.ops.filter(function (o) { return o.q.indexOf(last) < 0; }); c.n--; }); };
    $('as').onclick = function () { edit(function (c) { c.cols++; }); };
    $('us').onclick = function () { edit(function (c) { var m = 0; c.ops.forEach(function (o) { if (o.col + 1 > m) m = o.col + 1; }); if (c.cols > Math.max(1, m)) c.cols--; else { c.ops = c.ops.filter(function (o) { return o.col < c.cols - 1; }); c.cols--; } }); };
    $('undo').onclick = doUndo; $('redo').onclick = doRedo; $('clr').onclick = function () { edit(function (c) { c.ops = []; }); };
    if (cfg.console) { var ch = $('chips'); cfg.chips.forEach(function (x) { var b = h('button', 'chip', esc(x)); b.onclick = function () { $('cmd').value = x; $('go').click(); }; ch.appendChild(b); });
      $('go').onclick = function () { var v = $('cmd').value; $('cmd').value = ''; runCmd(v); }; $('cmd').addEventListener('keydown', function (e) { if (e.key === 'Enter') $('go').click(); });
      say('Hi! I am the Q Console. Type <b>help</b> or tap a button below.', 'sys'); }
    if (cfg.levels) {
      $('next').onclick = function () { if (S.li < cfg.levels.length - 1) showLevel(S.li + 1); }; $('reset').onclick = function () { showLevel(S.li); };
      $('hint').onclick = function () { $('sol').innerHTML = '<div class="card k">Hint: ' + esc(cfg.levels[S.li].hint || 'Try the buttons and watch the chances.') + '</div>'; };
      $('solbtn').onclick = function () { var L = cfg.levels[S.li], py = L.solutionCode, kind = L.goal && L.goal.via; $('sol').innerHTML = '<div class="card"><div class="k">One solution' + (py ? ' (' + ({ python: 'Python', qasm: 'OpenQASM', text: 'Q text' }[kind] || 'code') + ')' : ' (Q text)') + ':</div><pre>' + esc(py || L.solution || '') + '</pre><button class="ab s" id="loadsol">' + (py ? 'Put it in the editor' : 'Load it') + '</button></div>';
        $('loadsol').onclick = function () { if (py) { S.ctab = kind; var cb = $('codebox'); if (cb) cb.open = true; paintCode(); var ta = $('code'); if (ta && ta.tagName === 'TEXTAREA') { ta.value = py; S.dirty = true; cmsg('Now press ' + (kind === 'python' ? 'Run' : 'Apply') + '.', false); } } else setCircuit(QWL.fromText(L.solution), true); }; };
    }

    /* ---------- start ---------- */
    var start;
    try { start = cfg.startQasm ? QWL.fromQasm(cfg.startQasm) : cfg.start ? QWL.fromText(cfg.start) : new QWL.Circuit(cfg.qubits); } catch (e) { start = new QWL.Circuit(cfg.qubits); }
    if (cfg.levels) showLevel(0); else { if (start.cols < cfg.steps) start.cols = cfg.steps; setCircuit(start, false); }
    var api = { cfg: cfg, state: S, circuit: function () { return S.c; }, setCircuit: setCircuit, runCommand: runCmd, render: render, showLevel: showLevel };
    el.__qwl = api; return api;
  };
})(typeof window !== 'undefined' ? window : globalThis);
