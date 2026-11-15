/* Verilog lab UI: levels with editable files, Run, console, waveform and goals. Config in window.VLCFG. */
(function () {
  const CFG = window.VLCFG, L = CFG.levels, key = 'vlab:' + CFG.title;
  let done = {}, saved = {}, cur = 0, tab = 0, files = [], last = null, completed = false, busy = false;
  try { const s = JSON.parse(localStorage.getItem(key) || '{}'); done = s.done || {}; saved = s.code || {}; } catch (e) { }
  const $ = s => document.querySelector(s);
  const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  document.body.innerHTML = '<div class="card"><h2>' + esc(CFG.title) + '</h2><div class="k" id="intro"></div></div><div class="card"><div class="chips" id="chips"></div><div id="lt"></div></div>' +
    '<div class="card"><div class="tabs" id="tabs"></div><textarea id="ed" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off"></textarea>' +
    '<div class="row"><button id="run">Run</button><button class="s" id="hint">Hint</button><button class="s" id="sol">Show solution</button><button class="s" id="rst">Start over</button></div>' +
    '<div id="hintbox" class="small"></div></div>' +
    '<div class="card"><b>Goals</b><ul id="goals"></ul><div id="status" class="small"></div></div>' +
    '<div class="card"><b>Console</b><pre id="con">Press Run.</pre><b>Waveform</b><div class="small" id="wnote">Signals appear after a run that dumps a VCD.</div><div class="wave" id="wave"><canvas id="cv" height="10"></canvas></div><div class="row"><button class="s" id="zin">Zoom in</button><button class="s" id="zout">Zoom out</button></div></div>';
  $('#intro').textContent = CFG.intro || '';
  let zoom = 1;
  function save() { try { localStorage.setItem(key, JSON.stringify({ done: done, code: saved })); } catch (e) { } }
  function chips() {
    $('#chips').innerHTML = '';
    L.forEach(function (lv, i) { const b = document.createElement('button'); b.className = 'chip' + (i === cur ? ' on' : '') + (done[i] ? ' done' : ''); b.textContent = (done[i] ? '✓ ' : '') + (i + 1); b.onclick = function () { enter(i); }; $('#chips').appendChild(b); });
  }
  function tabs() {
    $('#tabs').innerHTML = '';
    files.forEach(function (f, i) { const b = document.createElement('button'); b.className = i === tab ? '' : 's'; b.textContent = f.name + (f.edit ? '' : ' (read only)'); b.onclick = function () { pull(); tab = i; push(); tabs(); }; $('#tabs').appendChild(b); });
  }
  function pull() { if (files[tab]) files[tab].src = $('#ed').value; }
  function push() { const f = files[tab]; $('#ed').value = f.src; $('#ed').readOnly = !f.edit; }
  function goalsView(res) {
    $('#goals').innerHTML = '';
    L[cur].goals.forEach(function (g, i) { const li = document.createElement('li'); const ok = res && res[i]; li.className = ok ? 'ok' : ''; li.textContent = (ok ? '✓ ' : '○ ') + g.t; $('#goals').appendChild(li); });
  }
  function enter(i) {
    cur = i; const lv = L[i];
    files = lv.files.map(function (f) { const s = saved[i + ':' + f.name]; return { name: f.name, src: (f.edit && s != null) ? s : f.src, edit: !!f.edit }; });
    tab = Math.max(0, files.findIndex(function (f) { return f.edit; }));
    $('#lt').innerHTML = '<b>' + esc(lv.title) + '</b><div class="info" style="margin-top:4px">' + lv.text.split('\n').map(function (p) { return '<p style="margin:4px 0">' + esc(p) + '</p>'; }).join('') + '</div>';
    $('#hintbox').textContent = ''; $('#con').textContent = 'Press Run.'; $('#status').textContent = ''; last = null;
    tabs(); push(); goalsView(null); chips(); drawWave(null);
  }
  function evalGoals(r) {
    return L[cur].goals.map(function (g) {
      if (g.re === 'COMPILE') return r.ok;
      return r.ok && new RegExp(g.re, 'm').test(r.log);
    });
  }
  async function run() {
    if (busy) return last; busy = true; pull();
    files.forEach(function (f) { if (f.edit) saved[cur + ':' + f.name] = f.src; });
    $('#run').disabled = true; $('#status').textContent = 'compiling and simulating…';
    let r;
    try { r = await VL.run(files.map(function (f) { return { name: f.name, src: f.src }; }), L[cur].gen); } catch (e) { r = { ok: false, log: 'engine error: ' + e, vcd: null }; }
    last = r; $('#con').innerHTML = (r.ok ? '' : '<span class="err">') + esc(r.log.replace(/^VCD info:.*\n?/m, '').replace(/^\/[\w.]+:\d+: \$finish called at.*$/m, '').trim() || '(no output)') + (r.ok ? '' : '</span>');
    const res = evalGoals(r); goalsView(res);
    const all = res.every(Boolean);
    $('#status').textContent = r.ok ? (all ? 'Level complete.' : 'Compiled. Not all goals met yet.') : 'Compile error: fix it and run again.';
    if (all) { done[cur] = 1; }
    save(); chips(); drawWave(r.vcd);
    if (!completed && L.every(function (x, i) { return done[i]; })) { completed = true; try { if (window.lilith && window.lilith.complete) window.lilith.complete(); } catch (e) { } }
    $('#run').disabled = false; busy = false; return r;
  }
  function solve(i) {
    if (i !== cur) enter(i);
    const lv = L[cur];
    files.forEach(function (f) { if (lv.solution[f.name] != null) f.src = lv.solution[f.name]; });
    push(); return run();
  }
  /* ---- waveform ---- */
  function parseVCD(t) {
    const vars = {}, order = [], scope = []; let time = 0, end = 0; const lines = t.split('\n'); let defs = true;
    for (let ln of lines) {
      ln = ln.trim(); if (!ln) continue;
      if (defs) {
        if (ln.startsWith('$scope')) scope.push(ln.split(/\s+/)[2]);
        else if (ln.startsWith('$upscope')) scope.pop();
        else if (ln.startsWith('$var')) { const p = ln.split(/\s+/); const id = p[3]; if (!vars[id]) { vars[id] = { name: p[4], w: +p[2], depth: scope.length, ev: [] }; order.push(id); } }
        else if (ln.startsWith('$enddefinitions')) defs = false;
        continue;
      }
      const c = ln[0];
      if (c === '#') { time = +ln.slice(1); if (time > end) end = time; }
      else if (c === 'b' || c === 'B') { const p = ln.split(/\s+/); if (vars[p[1]]) vars[p[1]].ev.push([time, p[0].slice(1)]); }
      else if ('01xXzZ'.indexOf(c) >= 0) { const id = ln.slice(1); if (vars[id]) vars[id].ev.push([time, c]); }
    }
    return { vars: vars, order: order, end: end };
  }
  function valAt(v, t) { let r = 'x'; for (let k = 0; k < v.ev.length; k++) { if (v.ev[k][0] <= t) r = v.ev[k][1]; else break; } return r; }
  function hex(b) { if (/[xz]/i.test(b)) return b.toLowerCase().indexOf('x') >= 0 ? 'x' : 'z'; return parseInt(b, 2).toString(16); }
  function drawWave(vcd) {
    const cv = $('#cv'); const ctx = cv.getContext('2d');
    if (!vcd) { cv.width = 10; cv.height = 10; $('#wnote').style.display = ''; return; }
    const W = parseVCD(vcd); const ids = W.order.filter(function (id) { return W.vars[id].ev.length; }).slice(0, 16);
    if (!ids.length) { cv.width = 10; cv.height = 10; return; }
    $('#wnote').style.display = 'none';
    const rowH = 30, lab = 76, base = Math.max(300, $('#wave').clientWidth || 300), width = Math.floor((base - lab) * zoom) + lab, H = ids.length * rowH + 22;
    cv.width = width; cv.height = H; ctx.fillStyle = '#0a0712'; ctx.fillRect(0, 0, width, H);
    const end = W.end || 1, X = t => lab + (t / end) * (width - lab - 6);
    ctx.font = '11px ui-monospace,monospace'; ctx.textBaseline = 'middle';
    ctx.strokeStyle = '#2a2040'; ctx.fillStyle = '#7d72a0';
    const step = Math.pow(10, Math.floor(Math.log10(end / 5 || 1))) * (end / 5 / Math.pow(10, Math.floor(Math.log10(end / 5 || 1))) > 5 ? 5 : end / 5 / Math.pow(10, Math.floor(Math.log10(end / 5 || 1))) > 2 ? 2 : 1);
    for (let t = 0; t <= end; t += step) { ctx.beginPath(); ctx.moveTo(X(t), 14); ctx.lineTo(X(t), H); ctx.stroke(); ctx.fillText(String(t), X(t) + 2, 7); }
    ids.forEach(function (id, r) {
      const v = W.vars[id], y0 = 22 + r * rowH, yh = y0 + 6, yl = y0 + rowH - 8;
      ctx.fillStyle = '#d6ccf0'; ctx.fillText(v.name.slice(0, 10), 4, y0 + rowH / 2);
      const evs = v.ev.slice(); const pts = evs.map(function (e) { return e[0]; });
      for (let k = 0; k < evs.length; k++) {
        const x1 = X(evs[k][0]), x2 = X(k + 1 < evs.length ? evs[k + 1][0] : end), val = evs[k][1];
        const bad = /[xz]/i.test(val);
        ctx.strokeStyle = bad ? '#ff7a9a' : '#7be0a4'; ctx.lineWidth = 1.5;
        if (v.w === 1) {
          const y = (val === '1') ? yh : (val === '0' ? yl : (yh + yl) / 2);
          ctx.beginPath(); ctx.moveTo(x1, y); ctx.lineTo(x2, y); ctx.stroke();
          if (k > 0) { const pv = evs[k - 1][1], py = (pv === '1') ? yh : (pv === '0' ? yl : (yh + yl) / 2); ctx.beginPath(); ctx.moveTo(x1, py); ctx.lineTo(x1, y); ctx.stroke(); }
        } else {
          ctx.beginPath(); ctx.moveTo(x1 + 2, (yh + yl) / 2); ctx.lineTo(x1 + 5, yh); ctx.lineTo(x2 - 3, yh); ctx.lineTo(x2, (yh + yl) / 2); ctx.lineTo(x2 - 3, yl); ctx.lineTo(x1 + 5, yl); ctx.closePath(); ctx.stroke();
          if (x2 - x1 > 16) { ctx.fillStyle = bad ? '#ff7a9a' : '#ffd27f'; ctx.fillText(hex(val), x1 + 8, (yh + yl) / 2); }
        }
      }
    });
  }
  $('#run').onclick = function () { run(); };
  $('#hint').onclick = function () { $('#hintbox').textContent = 'Hint: ' + L[cur].hint; };
  $('#sol').onclick = function () { const lv = L[cur]; files.forEach(function (f) { if (lv.solution[f.name] != null) f.src = lv.solution[f.name]; }); push(); $('#hintbox').textContent = 'Solution loaded. Press Run to check it, and read it line by line.'; };
  $('#rst').onclick = function () { saved = {}; Object.keys(saved).forEach(function (k) { delete saved[k]; }); enter(cur); };
  $('#zin').onclick = function () { zoom = Math.min(16, zoom * 2); if (last) drawWave(last.vcd); };
  $('#zout').onclick = function () { zoom = Math.max(1, zoom / 2); if (last) drawWave(last.vcd); };
  $('#ed').addEventListener('keydown', function (e) { if (e.key === 'Tab') { e.preventDefault(); const t = e.target, s = t.selectionStart; t.value = t.value.slice(0, s) + '  ' + t.value.slice(t.selectionEnd); t.selectionStart = t.selectionEnd = s + 2; } });
  window.__lab = { lab: CFG, enter: enter, run: run, solve: solve, isDone: function (i) { return !!done[i]; }, setCode: function (n, s) { files.forEach(function (f) { if (f.name === n) { f.src = s; } }); push(); } };
  $('#rst').onclick = function () { Object.keys(saved).forEach(function (k) { if (k.indexOf(cur + ':') === 0) delete saved[k]; }); enter(cur); };
  enter(0);
})();
