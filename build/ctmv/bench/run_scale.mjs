// Scale test: how the real engine behaves as the vault grows (timing, limits, silent truncation).
import fs from 'node:fs';
const KIT = '/home/claude/lilith-learning-lab/build/vendor'; const HERE = new URL('.', import.meta.url).pathname;
const of = globalThis.fetch; globalThis.fetch = async (u, ...a) => String(u).endsWith('sqlite3.wasm') ? new Response(fs.readFileSync(KIT + '/jade-agent-kit/sqlite3.wasm')) : of(u, ...a);
globalThis.location = { href: 'https://kit.local/' };
(0, eval)(fs.readFileSync(KIT + '/jade-agent-kit/jade-agent-kit.iife.js', 'utf8'));
const kit = await globalThis.JadeKit.createKit({ busybox: false, scheduler: false });
(0, eval)(fs.readFileSync(HERE + '../vault.js', 'utf8') + fs.readFileSync(HERE + '../engine.js', 'utf8') + ';globalThis.E=E;');
await E.initKg(fs.readFileSync(KIT + '/jade-vault/jade_kg.wasm'));
let seed = 7; const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
const DIM = 384; const out = [];
for (const [scen, N, group, hub] of [['typical', 100, 10, 0], ['typical', 300, 10, 0], ['typical', 1000, 10, 0], ['typical', 3000, 10, 0], ['typical', 10000, 10, 0],
  ['big-group', 1000, 100, 0], ['big-group', 2000, 400, 0], ['hub', 1000, 10, 0.1], ['hub', 1500, 10, 0.3], ['hub', 3000, 10, 0.3]]) {
  const notes = []; for (let i = 0; i < N; i++) { const cl = [[`s${i}`, 'is', `pat${Math.floor(i / group)}`], [`s${i}`, 'causes', `s${(i * 7 + 3) % N}`]]; if (rnd() < hub) cl.push([`s${i}`, 'causes', 'outage']); notes.push({ name: `n${i}`, title: `t${i}`, body: 'x', tags: ['d' + (i % 5)], claims: cl, links: [] }); }
  const rec = { scen, N, group, hub, facts: N * 2 + Math.round(N * hub) };
  let t = Date.now(); let kg; try { kg = E.loadKg(notes); rec.loadMs = Date.now() - t; rec.derived = kg.stats.derived; } catch (e) { rec.loadErr = String(e.message).slice(0, 80); out.push(rec); console.log(JSON.stringify(rec)); continue; }
  t = Date.now(); const r = E.kgCall({ op: 'query', handle: kg.handle, q: 'shares(A, B, C)', limit: 100000 }); rec.sharesMs = Date.now() - t; rec.sharesRows = (r.answers || []).length; rec.sharesTruncated = rec.sharesRows >= 200;  // the engine caps every query at 200 answers
  // the per-note neighbour query that delta and the lab use has a default limit of 200
  { const big = notes.findIndex((n, i) => true); const q = E.kgCall({ op: 'query', handle: kg.handle, q: 'shares("n0", B, C)', limit: 200 }); rec.neighbourRowsCapped = (q.answers || []).length >= 200; }
  t = Date.now(); try { E.edgeSets(notes.slice(0, Math.min(N, 300)), kg); rec.edgeSets300Ms = Date.now() - t; } catch (e) { rec.edgeErr = String(e.message).slice(0, 60); }
  if (N <= 1000) { t = Date.now(); const es = E.edgeSets(notes, kg); rec.edgeSetsFullMs = Date.now() - t; }
  E.kgCall({ op: 'free', handle: kg.handle });
  if (N <= 3000) {
    const db = await kit.sqlite.open(':memory:'); const vecs = {}; notes.forEach(n => { const v = Float32Array.from({ length: DIM }, () => rnd() - 0.5); const m = Math.hypot(...v); vecs[n.name] = v.map(x => x / m); });
    E.embed = t => vecs[t]; E.noteText = n => n.name; t = Date.now(); await E.buildMani(db, notes, DIM); rec.vecInsertMs = Date.now() - t;
    t = Date.now(); for (let i = 0; i < 100; i++) E.knn(db, vecs['n' + i], 5); rec.knnMsPer = (Date.now() - t) / 100; db.close?.({ save: false });
  }
  out.push(rec); console.log(JSON.stringify(rec));
}
fs.writeFileSync(process.argv[2] || '/tmp/scale.json', JSON.stringify(out));
