/* CMOS switch labs: transistor switches and building gates from pull-up / pull-down networks. Config in window.CMOSCFG. */
(function () {
  const CFG = window.CMOSCFG, L = CFG.levels, key = 'cmos:' + CFG.title;
  let done = {}, cur = 0, seen = {}, completed = false, ch = {}, inp = {};
  try { done = JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) { }
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  document.body.innerHTML = '<div class="card"><h2>' + esc(CFG.title) + '</h2><div class="k">' + esc(CFG.intro) + '</div></div><div class="card"><div class="chips" id="chips"></div><div id="lt"></div></div><div class="card" id="play"></div><div class="card"><b>Goals</b><ul id="goals"></ul></div>';
  function save() { try { localStorage.setItem(key, JSON.stringify(done)); } catch (e) { } }
  function chips() { $('#chips').innerHTML = ''; L.forEach(function (lv, i) { const b = document.createElement('button'); b.className = 'chip' + (i === cur ? ' on' : '') + (done[i] ? ' done' : ''); b.textContent = (done[i] ? '✓ ' : '') + (i + 1); b.onclick = function () { enter(i); }; $('#chips').appendChild(b); }); }
  function btn(txt, cls, fn) { const b = document.createElement('button'); b.textContent = txt; if (cls) b.className = cls; b.onclick = fn; return b; }
  function goalsView(list) { $('#goals').innerHTML = ''; list.forEach(function (g) { const li = document.createElement('li'); li.className = g[1] ? 'ok' : ''; li.textContent = (g[1] ? '✓ ' : '○ ') + g[0]; $('#goals').appendChild(li); }); }
  function finish(list) {
    if (list.every(function (g) { return g[1]; })) { done[cur] = 1; save(); chips(); }
    if (!completed && L.every(function (x, i) { return done[i]; })) { completed = true; try { if (window.lilith && window.lilith.complete) window.lilith.complete(); } catch (e) { } }
  }
  function enter(i) {
    cur = i; seen = {}; const lv = L[i]; ch = {}; inp = {};
    $('#lt').innerHTML = '<b>' + esc(lv.title) + '</b><div class="info" style="margin-top:4px">' + lv.text.split('\n').map(function (p) { return '<p style="margin:4px 0">' + esc(p) + '</p>'; }).join('') + '</div><div id="hintbox" class="small"></div>';
    if (lv.kind === 'gate') { lv.ins.forEach(function (n) { inp[n] = 0; }); Object.keys(lv.start).forEach(function (k) { ch[k] = lv.start[k]; }); }
    else inp.G = 0;
    chips(); render();
  }
  /* ---------- switch levels ---------- */
  function sw(kind, g) { return kind === 'n' ? g === 1 : g === 0; }
  function drawSwitch(on, label, y) {
    return '<g transform="translate(0,' + y + ')"><line x1="60" y1="0" x2="60" y2="22" stroke="#d6ccf0" stroke-width="3"/>' +
      (on ? '<line x1="60" y1="22" x2="60" y2="58" stroke="#7be0a4" stroke-width="4"/>' : '<line x1="60" y1="22" x2="86" y2="50" stroke="#a99dc7" stroke-width="3"/>') +
      '<line x1="60" y1="58" x2="60" y2="80" stroke="#d6ccf0" stroke-width="3"/><text x="100" y="45" fill="#f1ebff" font-size="13">' + label + '</text></g>';
  }
  function renderSwitch(lv) {
    const g = inp.G; let svg, status;
    if (lv.mode === 'inv') {
      const pOn = sw('p', g), nOn = sw('n', g), out = pOn ? 1 : 0;
      seen['in' + g] = out;
      svg = '<svg viewBox="0 0 320 250" width="100%" style="max-width:360px;display:block;margin:auto"><text x="40" y="14" fill="#ffd27f" font-size="13">VDD (1)</text>' + drawSwitch(pOn, 'pMOS ' + (pOn ? 'ON' : 'off'), 20) + '<line x1="60" y1="100" x2="60" y2="125" stroke="#d6ccf0" stroke-width="3"/><circle cx="60" cy="125" r="5" fill="#7ab8ff"/><line x1="60" y1="125" x2="170" y2="125" stroke="#7ab8ff" stroke-width="3"/><circle cx="190" cy="125" r="16" fill="' + (out ? '#ffd27f' : '#2a2040') + '" stroke="#ffd27f"/><text x="178" y="130" fill="#0f0b18" font-size="13">Y=' + out + '</text>' + drawSwitch(nOn, 'nMOS ' + (nOn ? 'ON' : 'off'), 128) + '<text x="40" y="238" fill="#a99dc7" font-size="13">GND (0)</text></svg>';
      status = 'Input A = ' + g + ' gives output Y = ' + out;
    } else {
      const on = sw(lv.mode, g); seen['g' + g] = 1;
      svg = '<svg viewBox="0 0 320 140" width="100%" style="max-width:360px;display:block;margin:auto"><text x="40" y="14" fill="#ffd27f" font-size="13">' + (lv.mode === 'n' ? 'supply' : 'supply') + '</text>' + drawSwitch(on, (lv.mode === 'n' ? 'nMOS' : 'pMOS') + (on ? ' ON' : ' off'), 18) + '<circle cx="60" cy="118" r="14" fill="' + (on ? '#ffd27f' : '#2a2040') + '" stroke="#ffd27f"/><text x="82" y="123" fill="#f1ebff" font-size="13">lamp ' + (on ? 'lit' : 'dark') + '</text></svg>';
      status = 'Gate = ' + g + ' → the switch is ' + (on ? 'closed (conducting)' : 'open');
    }
    $('#play').innerHTML = svg + '<div class="info" style="text-align:center">' + status + '</div><div class="row" style="justify-content:center"></div>';
    const row = $('#play .row'); row.appendChild(btn('Gate = 0', g === 0 ? '' : 's', function () { inp.G = 0; render(); })); row.appendChild(btn('Gate = 1', g === 1 ? '' : 's', function () { inp.G = 1; render(); }));
    return lv.goals.map(function (gl) { return [gl.t, seen[gl.k] !== undefined]; });
  }
  /* ---------- gate levels: pull-up / pull-down networks ---------- */
  function comb(kind, ops, vals) { return kind === 'S' ? ops.every(Boolean) : ops.some(Boolean); }
  function net(lv, side) {
    // lv.shape: {inner:[names], rest:[names]}: network = top( inner-group, ...rest ), side picks n/p conduction
    const tr = side === 'pd' ? function (n) { return inp[n] === 1; } : function (n) { return inp[n] === 0; };
    const c = ch[side];
    if (!lv.inner) return comb(c.top, lv.ins.map(tr));
    const innerV = comb(c.inner, lv.inner.map(tr)); return comb(c.top, [innerV].concat(lv.rest.map(tr)));
  }
  function evalRow(lv) { const pu = net(lv, 'pu'), pd = net(lv, 'pd'); return { pu: pu, pd: pd, y: pu && !pd ? '1' : (pd && !pu ? '0' : (pu && pd ? 'X' : 'Z')) }; }
  function renderGate(lv) {
    const saveIn = JSON.parse(JSON.stringify(inp)); const n = lv.ins.length, rows = [];
    for (let m = 0; m < (1 << n); m++) { lv.ins.forEach(function (nm, k) { inp[nm] = (m >> (n - 1 - k)) & 1; }); const r = evalRow(lv); r.m = m; r.vals = lv.ins.map(function (nm) { return inp[nm]; }); r.want = String(lv.table[r.vals.join("")]); rows.push(r); }
    Object.keys(saveIn).forEach(function (k) { inp[k] = saveIn[k]; });
    const live = evalRow(lv);
    function pick(side, which, label) {
      const d = document.createElement('div'); d.className = 'row'; d.appendChild(document.createTextNode(label + ': '));
      ['S', 'P'].forEach(function (o) { d.appendChild(btn(o === 'S' ? 'series' : 'parallel', ch[side][which] === o ? '' : 's', function () { ch[side][which] = o; render(); })); });
      return d;
    }
    const box = $('#play'); box.innerHTML = '';
    const desc = function (side, nm) { const c = ch[side]; const w = function (k) { return k === 'S' ? 'in series' : 'in parallel'; }; return lv.inner ? nm + ': (' + lv.inner.join(', ') + ' ' + w(c.inner) + ') and ' + lv.rest.join(', ') + ' combined ' + w(c.top) : nm + ': ' + lv.ins.join(', ') + ' ' + w(c.top); };
    box.appendChild(Object.assign(document.createElement('div'), { className: 'info', innerHTML: '<b>Target: Y = ' + esc(lv.expr) + '</b>' }));
    box.appendChild(Object.assign(document.createElement('div'), { className: 'small', textContent: desc('pu', 'Pull-up (pMOS to VDD)') }));
    if (lv.inner) box.appendChild(pick('pu', 'inner', 'pull-up, ' + lv.inner.join('+') + ' group')); box.appendChild(pick('pu', 'top', 'pull-up, top level'));
    box.appendChild(Object.assign(document.createElement('div'), { className: 'small', textContent: desc('pd', 'Pull-down (nMOS to GND)') }));
    if (lv.inner) box.appendChild(pick('pd', 'inner', 'pull-down, ' + lv.inner.join('+') + ' group')); box.appendChild(pick('pd', 'top', 'pull-down, top level'));
    const ir = document.createElement('div'); ir.className = 'row'; ir.appendChild(document.createTextNode('Try inputs: '));
    lv.ins.forEach(function (nm) { ir.appendChild(btn(nm + '=' + inp[nm], inp[nm] ? '' : 's', function () { inp[nm] = 1 - inp[nm]; render(); })); });
    box.appendChild(ir);
    box.appendChild(Object.assign(document.createElement('div'), { className: 'info', innerHTML: 'Now: pull-up <b>' + (live.pu ? 'ON' : 'off') + '</b>, pull-down <b>' + (live.pd ? 'ON' : 'off') + '</b> → Y = <b>' + (live.y === 'X' ? 'X (short circuit!)' : live.y === 'Z' ? 'Z (floating)' : live.y) + '</b>' }));
    let t = '<table style="width:100%;border-collapse:collapse;font-size:12px;margin-top:6px"><tr style="color:#a99dc7"><td>' + lv.ins.join(' ') + '</td><td>pull-up</td><td>pull-down</td><td>Y</td><td>wanted</td></tr>';
    rows.forEach(function (r) { const ok = r.y === r.want; t += '<tr style="color:' + (ok ? '#7be0a4' : '#ff7a9a') + '"><td>' + r.vals.join(' ') + '</td><td>' + (r.pu ? 'on' : 'off') + '</td><td>' + (r.pd ? 'on' : 'off') + '</td><td>' + r.y + '</td><td>' + r.want + '</td></tr>'; });
    box.appendChild(Object.assign(document.createElement('div'), { innerHTML: t + '</table>' }));
    return [['No row shorts VDD to GND (never X)', rows.every(function (r) { return r.y !== 'X'; })], ['The output is never left floating (never Z)', rows.every(function (r) { return r.y !== 'Z'; })], ['Y equals the target in every row', rows.every(function (r) { return r.y === r.want; })]];
  }
  function render() { const lv = L[cur]; const gl = lv.kind === 'gate' ? renderGate(lv) : renderSwitch(lv); goalsView(gl); finish(gl); }
  function solve(i) { if (i !== cur) enter(i); const lv = L[cur]; if (lv.kind === 'gate') { ch = JSON.parse(JSON.stringify(lv.sol)); render(); } else { inp.G = 0; render(); inp.G = 1; render(); } }
  window.__lab = { lab: CFG, enter: enter, solve: solve, isDone: function (i) { return !!done[i]; } };
  enter(0);
})();
