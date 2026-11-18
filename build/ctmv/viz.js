/* 3D tri-layer view (G on top, V in the middle, M at the bottom), drawn from the live data of the lab:
   V positions come from the notes' areas, M positions from a 2-D projection (PCA) of the real sqlite-vec vectors,
   G nodes are the ideas that jade-kg finds in two or more notes. Drag to orbit, tap a node to inspect it. */
const VZ = { rot: 0.58, tilt: 0.44, orbit: true, show: { G: true, V: true, M: true }, sel: null, hit: [], drag: false, moved: false, lx: 0, ly: 0, d: null, lam: 0.75, mu: 0.5 };
const VZ_COL = ['#ff007f', '#00ffa3', '#00f0ff', '#bd72f3', '#ffb800', '#7aa2ff'];
const vzHash = s => E.hash(s) / 4294967295;
function vzPca(names) {
  const D = vecs[names[0]].length, X = names.map(n => Array.from(vecs[n]));
  const mean = Array(D).fill(0); X.forEach(r => r.forEach((v, i) => mean[i] += v / X.length)); X.forEach(r => r.forEach((v, i) => r[i] = v - mean[i]));
  const comps = [];
  for (let c = 0; c < 2; c++) {
    let v = Array.from({ length: D }, (_, i) => vzHash('pca' + c + '_' + i) - 0.5);
    for (let it = 0; it < 40; it++) { const w = Array(D).fill(0); X.forEach(r => { const d = r.reduce((s, x, i) => s + x * v[i], 0); r.forEach((x, i) => w[i] += d * x); }); const n = Math.hypot(...w) || 1; v = w.map(x => x / n); }
    comps.push(v); X.forEach(r => { const d = r.reduce((s, x, i) => s + x * v[i], 0); r.forEach((x, i) => r[i] -= d * v[i]); });
  }
  const X0 = names.map(n => Array.from(vecs[n]).map((v, i) => v - mean[i]));
  let pts = X0.map(r => comps.map(v => r.reduce((s, x, i) => s + x * v[i], 0)));
  const m = Math.max(...pts.flat().map(Math.abs)) || 1; return pts.map(p => [p[0] / m * 0.85, p[1] / m * 0.85]);
}
function vizRebuild() {
  const names = notes.map(n => n.name), areas = [...new Set(notes.map(n => n.tags[0] || 'other'))];
  const anchors = {}; areas.forEach((a, i) => { const ang = i / areas.length * Math.PI * 2 + 0.8; anchors[a] = [Math.cos(ang) * 0.58, Math.sin(ang) * 0.5, VZ_COL[i % VZ_COL.length]]; });
  const sym = {}; notes.forEach(n => sym[n.name] = E.symNeighbours(kg, n.name));
  const m2 = vzPca(names);
  const N = {}; notes.forEach((n, i) => { const a = anchors[n.tags[0] || 'other'];
    N[n.name] = { n, vx: Math.max(-0.9, Math.min(0.9, a[0] + (vzHash(n.name + 'x') - 0.5) * 0.4)), vz: Math.max(-0.9, Math.min(0.9, a[1] + (vzHash(n.name + 'z') - 0.5) * 0.4)), mx: m2[i][0], mz: m2[i][1], col: a[2], sym: sym[n.name] }; });
  const cs = {}; notes.forEach(n => { const seen = new Set(); n.claims.forEach(([s, r, o]) => [s, o].forEach(c => { if (!seen.has(c)) { seen.add(c); (cs[c] = cs[c] || []).push(n.name); } })); });
  const concepts = Object.entries(cs).filter(([c, l]) => l.length >= 2).map(([c, l]) => ({ id: c, notes: l, x: l.reduce((s, x) => s + N[x].vx, 0) / l.length, z: l.reduce((s, x) => s + N[x].vz, 0) / l.length }));
  const relax = (pts, key, min) => { for (let it = 0; it < 60; it++) for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) { const a = pts[i], b = pts[j]; let dx = a[key[0]] - b[key[0]], dz = a[key[1]] - b[key[1]]; const L = Math.hypot(dx, dz) || 0.01; if (L < min) { const k = (min - L) / 2 / L; dx *= k; dz *= k; a[key[0]] += dx; a[key[1]] += dz; b[key[0]] -= dx; b[key[1]] -= dz; } } pts.forEach(p => { p[key[0]] = Math.max(-0.92, Math.min(0.92, p[key[0]])); p[key[1]] = Math.max(-0.92, Math.min(0.92, p[key[1]])); }); };
  relax(Object.values(N), ['vx', 'vz'], 0.24); relax(concepts, ['x', 'z'], 0.3);
  const knn = []; names.forEach(a => E.knn(db, vecs[a], 3).filter(r => r.name !== a).slice(0, 2).forEach(r => knn.push([a, r.name])));
  VZ.d = { N, names, concepts, knn, bridges: E.bridges(notes, vecs, kg).filter(b => b.cross).slice(0, 4), delta: Object.fromEntries(E.delta(db, kg, notes, vecs).map(r => [r.name, r])) };
  if (!VZ.sel || !N[VZ.sel]) VZ.sel = names[0];
  vizInfo();
}
function vzWarp() {
  const d = VZ.d, out = {}; for (const k of d.names) { const p = d.N[k], nb = Object.keys(p.sym);
    if (nb.length) { const cx = nb.reduce((s, x) => s + d.N[x].mx, 0) / nb.length, cz = nb.reduce((s, x) => s + d.N[x].mz, 0) / nb.length; out[k] = [p.mx * (1 - 0.5 * VZ.lam) + cx * 0.5 * VZ.lam, p.mz * (1 - 0.5 * VZ.lam) + cz * 0.5 * VZ.lam]; } else out[k] = [p.mx, p.mz]; }
  for (const key of es.conflict) { const [a, b] = key.split('|'); if (!out[a] || !out[b]) continue; let dx = out[a][0] - out[b][0], dz = out[a][1] - out[b][1]; const L = Math.hypot(dx, dz) || 0.1; dx /= L; dz /= L;
    out[a][0] += dx * VZ.mu * 0.3; out[a][1] += dz * VZ.mu * 0.3; out[b][0] -= dx * VZ.mu * 0.3; out[b][1] -= dz * VZ.mu * 0.3; }
  return out;
}
function vizInfo() {
  const d = VZ.d; if (!d) return; const r = d.delta[VZ.sel]; if (!r) return;
  $('vzinfo').innerHTML = `<b>${esc(VZ.sel)}</b> · δ ${r.delta.toFixed(2)}<br><span class="dim">M says:</span> ${tags(r.geo)}<br><span class="dim">V+G say:</span> ${tags(r.sym)}`;
}
function vzProj(x, y, z, W, H) {
  const c = Math.cos(VZ.rot), s = Math.sin(VZ.rot), rx = x * c - z * s, rz = x * s + z * c, sc = Math.min(W * 0.4, H * 0.36);
  return { x: W / 2 + rx * sc, y: H * 0.5 - y * sc * 0.74 + rz * sc * VZ.tilt };
}
function vzPlane(ctx, y, col, label, W, H) {
  const c = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(p => vzProj(p[0], y, p[1], W, H));
  ctx.beginPath(); ctx.moveTo(c[0].x, c[0].y); c.slice(1).forEach(p => ctx.lineTo(p.x, p.y)); ctx.closePath(); ctx.fillStyle = col.replace('1)', '0.04)'); ctx.fill(); ctx.strokeStyle = col.replace('1)', '0.55)'); ctx.lineWidth = 1.2; ctx.stroke();
  ctx.fillStyle = col.replace('1)', '0.9)'); ctx.font = '700 10px monospace'; ctx.fillText(label, c[3].x + 6, c[3].y - 6);
}
function vizDraw(t) {
  requestAnimationFrame(vizDraw);
  const cv = $('vzc'); if (!cv || !cv.offsetParent || !VZ.d) return;
  const W = cv.clientWidth, H = cv.clientHeight, dpr = window.devicePixelRatio || 1;
  if (cv.width !== Math.round(W * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
  const ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
  if (VZ.orbit && !VZ.drag) VZ.rot += 0.0016;
  const d = VZ.d, yG = 0.8, yV = 0, yM = -0.8, wp = vzWarp(); VZ.hit = [];
  if (VZ.show.M) { vzPlane(ctx, yM, 'rgba(0,255,163,1)', 'M manifold (sqlite-vec)', W, H);
    ctx.lineWidth = 0.8; for (let r = 0; r <= 12; r++) { ctx.beginPath(); for (let cc = 0; cc <= 12; cc++) { const x = -1 + cc / 6, z = -1 + r / 6; let well = 0; d.names.forEach(k => { const q = wp[k]; well += Math.exp(-((x - q[0]) ** 2 + (z - q[1]) ** 2) * 7.5) * 0.14 * (0.4 + VZ.lam); }); const p = vzProj(x, yM - well, z, W, H); cc ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y); } ctx.strokeStyle = 'rgba(0,255,163,0.16)'; ctx.stroke(); } }
  if (VZ.show.V) vzPlane(ctx, yV, 'rgba(0,240,255,1)', 'V vault (markdown)', W, H);
  if (VZ.show.G) vzPlane(ctx, yG, 'rgba(255,0,127,1)', 'G graph (jade-kg)', W, H);
  const pV = {}, pM = {}, pG = {}; d.names.forEach(k => { pV[k] = vzProj(d.N[k].vx, yV, d.N[k].vz, W, H); pM[k] = vzProj(wp[k][0], yM - 0.05, wp[k][1], W, H); }); d.concepts.forEach(c => pG[c.id] = vzProj(c.x, yG, c.z, W, H));
  const line = (a, b, col, w, dash) => { ctx.beginPath(); ctx.setLineDash(dash || []); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.strokeStyle = col; ctx.lineWidth = w; ctx.stroke(); ctx.setLineDash([]); };
  d.names.forEach(k => { const hl = k === VZ.sel; if (VZ.show.V && VZ.show.M) line(pV[k], pM[k], hl ? 'rgba(0,255,163,0.85)' : 'rgba(0,240,255,0.14)', hl ? 1.8 : 0.8, [3, 4]); });
  if (VZ.show.V && VZ.show.G) d.concepts.forEach(c => c.notes.forEach(k => { const hl = k === VZ.sel; line(pV[k], pG[c.id], hl ? 'rgba(255,0,127,0.85)' : 'rgba(255,0,127,0.15)', hl ? 1.8 : 0.8, [2, 4]); }));
  if (VZ.show.M) { d.knn.forEach(([a, b]) => line(pM[a], pM[b], 'rgba(0,255,163,0.25)', 0.9));
    for (const key of es.conflict) { const [a, b] = key.split('|'); if (pM[a] && pM[b]) line(pM[a], pM[b], 'rgba(255,80,80,0.8)', 1.6, [4, 3]); } }
  if (VZ.show.V) { notes.forEach(n => n.links.forEach(l => { if (pV[l]) line(pV[n.name], pV[l], 'rgba(0,240,255,0.6)', 1.4); }));
    const pulse = 0.6 + 0.4 * Math.sin(t * 0.005); d.bridges.forEach(b => line(pV[b.a], pV[b.b], `rgba(255,0,127,${pulse})`, 2, [5, 5]));
    for (const e of Object.values(d.N)) { const o = e.n.claims.find(c => c[1] === 'supersedes'); if (o && pV[o[2]]) line(pV[e.n.name], pV[o[2]], 'rgba(255,184,0,0.8)', 1.4, [2, 3]); } }
  if (VZ.show.M) d.names.forEach(k => { const p = pM[k], g = ctx.createRadialGradient(p.x, p.y, 1, p.x, p.y, 12); g.addColorStop(0, 'rgba(0,255,163,0.9)'); g.addColorStop(1, 'rgba(0,255,163,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, 12, 0, 7); ctx.fill(); ctx.beginPath(); ctx.arc(p.x, p.y, 3.5, 0, 7); ctx.fillStyle = '#00ffa3'; ctx.fill(); VZ.hit.push({ id: k, x: p.x, y: p.y, r: 14 }); });
  if (VZ.show.V) d.names.forEach(k => { const p = pV[k], sel = k === VZ.sel; ctx.beginPath(); ctx.arc(p.x, p.y, sel ? 6.5 : 4.5, 0, 7); ctx.fillStyle = sel ? '#fff' : d.N[k].col; ctx.fill(); ctx.strokeStyle = '#04060e'; ctx.lineWidth = 1.2; ctx.stroke();
    ctx.fillStyle = sel ? '#fff' : 'rgba(226,232,240,0.85)'; ctx.font = (sel ? '700 11px' : '500 9.5px') + ' system-ui'; ctx.fillText(k.length > 18 && !sel ? k.slice(0, 17) + '…' : k, p.x + 8, p.y + 3); VZ.hit.push({ id: k, x: p.x, y: p.y, r: 16 }); });
  if (VZ.show.G) d.concepts.forEach(c => { const p = pG[c.id]; ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(Math.PI / 4); ctx.fillStyle = '#ff007f'; ctx.shadowColor = '#ff007f'; ctx.shadowBlur = 9; ctx.fillRect(-4.5, -4.5, 9, 9); ctx.restore(); ctx.fillStyle = '#ff99cc'; ctx.font = '700 9.5px monospace'; ctx.fillText(c.id, p.x + 9, p.y + 3); VZ.hit.push({ id: c.notes[0], x: p.x, y: p.y, r: 14 }); });
}
(function () {
  const cv = $('vzc'), xy = e => { const r = cv.getBoundingClientRect(), p = e.touches ? (e.touches[0] || e.changedTouches[0]) : e; return [p.clientX - r.left, p.clientY - r.top, p.clientX, p.clientY]; };
  const start = e => { const [, , cx, cy] = xy(e); VZ.drag = true; VZ.moved = false; VZ.orbit = false; VZ.lx = cx; VZ.ly = cy; };
  const move = e => { if (!VZ.drag) return; const [, , cx, cy] = xy(e); const dx = cx - VZ.lx, dy = cy - VZ.ly; if (Math.abs(dx) + Math.abs(dy) > 3) VZ.moved = true; VZ.rot += dx * 0.008; VZ.tilt = Math.max(0.2, Math.min(0.85, VZ.tilt + dy * 0.004)); VZ.lx = cx; VZ.ly = cy; if (e.cancelable && e.touches) e.preventDefault(); };
  const end = e => { if (VZ.drag && !VZ.moved) { const [mx, my] = xy(e); for (let i = VZ.hit.length - 1; i >= 0; i--) { const h = VZ.hit[i]; if (Math.hypot(mx - h.x, my - h.y) <= h.r + 6) { VZ.sel = h.id; vizInfo(); if (window.goal) goal('viz'); break; } } } else if (VZ.drag && window.goal) goal('orbit'); VZ.drag = false; };
  cv.addEventListener('mousedown', start); window.addEventListener('mousemove', move); window.addEventListener('mouseup', end);
  cv.addEventListener('touchstart', start, { passive: true }); cv.addEventListener('touchmove', move, { passive: false }); cv.addEventListener('touchend', end);
  for (const L of ['G', 'V', 'M']) $('vz' + L).onclick = e => { VZ.show[L] = !VZ.show[L]; e.target.classList.toggle('on', VZ.show[L]); };
  $('vzlam').oninput = e => { VZ.lam = +e.target.value; $('vzlamv').textContent = e.target.value; if (VZ.lam > 0.4 && window.goal) goal('vzwarp'); };
  $('vzmu').oninput = e => { VZ.mu = +e.target.value; $('vzmuv').textContent = e.target.value; };
  $('vzorb').onclick = e => { VZ.orbit = !VZ.orbit; e.target.classList.toggle('on', VZ.orbit); };
  requestAnimationFrame(vizDraw);
})();
