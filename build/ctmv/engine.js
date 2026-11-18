/* CTMV engine for the labs. It is built from the Jade components:
   - JadeKit (jade-agent-kit): SQLite 3.53 + sqlite-vec as WebAssembly, the file system (vfs)
   - jade_kg.wasm (jade-vault): the Datalog reasoner with proofs
   Nothing here is a model: the "embedding" is a small hashing function, so labs run offline and always give the same numbers. */
const E = {};
E.enc = new TextEncoder(); E.dec = new TextDecoder();

/* ---------- V: the markdown vault ---------- */
E.parseNote = (name, text) => {
  const lines = text.split('\n');
  const title = (lines[0] || '').replace(/^#\s*/, '');
  const tags = ((lines.find(l => l.startsWith('tags:')) || '').slice(5)).split(',').map(s => s.trim()).filter(Boolean);
  const claims = lines.filter(l => l.startsWith('- ')).map(l => l.slice(2).trim().split(/\s+/)).filter(p => p.length === 3);
  const links = [...text.matchAll(/\[\[([^\]]+)\]\]/g)].map(m => m[1]);
  const body = lines.filter(l => !l.startsWith('#') && !l.startsWith('tags:') && !l.startsWith('- ')).join(' ').replace(/\[\[|\]\]/g, '');
  return { name, title, tags, claims, links, body };
};
E.notes = (vault) => Object.entries(vault).map(([n, t]) => E.parseNote(n, t));

/* ---------- G: facts and rules for jade-kg ---------- */
E.RULES = `% concepts a note talks about
concept(C) :- claim(N, C, R, O).
concept(O) :- claim(N, S, R, O).
mentions(N, C) :- claim(N, C, R, O).
mentions(N, C) :- claim(N, S, R, C).
% two notes share an idea
shares(A, B, C) :- mentions(A, C), mentions(B, C), A != B.
% a causal chain: X leads to Z through one step
leads_to(X, Y) :- claim(N, X, causes, Y).
leads_to(X, Z) :- claim(N, X, causes, Y), leads_to(Y, Z).
% every note that says X is positive feedback has the same shape
same_shape(A, B) :- claim(A, X, is, S), claim(B, Y, is, S), A != B.
% a note replaced by a newer one is no longer current
replaced(Old) :- claim(New, New, supersedes, Old).
% contradictions
! cause_and_prevent: claim(N1, X, causes, Y), claim(N2, X, prevents, Y), not replaced(N1), not replaced(N2).
`;
E.kgFacts = (notes) => {
  const f = [], q = s => /^[a-z0-9_]+$/.test(s) ? s : JSON.stringify(s);
  for (const n of notes) {
    for (const [s, r, o] of n.claims) {
      const subj = r === 'supersedes' ? n.name : s;  // a note replaces another: its own name is the subject
      f.push(`claim(${q(n.name)}, ${q(subj)}, ${q(r)}, ${q(o)}).`);
    }
    for (const l of n.links) f.push(`links(${q(n.name)}, ${q(l)}).`);
  }
  return f.join('\n');
};
E.kgCall = null;
E.initKg = async (bytes) => {
  const { instance } = await WebAssembly.instantiate(bytes, {});
  const x = instance.exports;
  E.kgCall = req => { const b = E.enc.encode(JSON.stringify(req)); const p = x.kg_alloc(b.length); new Uint8Array(x.memory.buffer, p, b.length).set(b); const q = x.kg_call(p, b.length); const out = JSON.parse(E.dec.decode(new Uint8Array(x.memory.buffer, q, x.kg_out_len()))); x.kg_free(p, b.length); return out; };
};
E.loadKg = (notes) => {
  const r = E.kgCall({ op: 'load', rules: E.RULES + '\n' + E.kgFacts(notes) });
  if (!r.ok && r.error) throw new Error(r.error);
  return r;
};

/* ---------- M: the toy embedder and sqlite-vec ---------- */
E.STOP = new Set('a an the of to and or is are in on it its so as at by for with that this be we use was were each every one two than then them they their yet'.split(' '));
E.tokens = (s) => s.toLowerCase().replace(/[^a-z0-9_ ]+/g, ' ').split(/\s+/).filter(w => w && !E.STOP.has(w));
E.hash = (s) => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
E.embed = (text, dim = 64) => {
  const v = new Float32Array(dim);
  for (const w of E.tokens(text)) { const g = ['^' + w + '$']; for (let i = 0; i + 3 <= w.length; i++) g.push(w.slice(i, i + 3));
    for (const t of g) { const h = E.hash(t); v[h % dim] += (h & 0x10000) ? 1 : -1; } }
  let n = Math.hypot(...v) || 1; return v.map(x => x / n);
};
E.noteText = n => n.title + '. ' + n.body + ' ' + n.claims.map(c => c.join(' ').replace(/_/g, ' ')).join('. ');
E.vecBytes = v => new Uint8Array(v.buffer, v.byteOffset, v.byteLength);
E.cos = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; };
E.buildMani = async (db, notes, dim) => {
  db.exec(`DROP TABLE IF EXISTS notes_vec; DROP TABLE IF EXISTS notes;`);
  db.exec(`CREATE TABLE notes(id INTEGER PRIMARY KEY, name TEXT UNIQUE, title TEXT); CREATE VIRTUAL TABLE notes_vec USING vec0(embedding float[${dim}] distance_metric=cosine);`);
  const vecs = {};
  db.transaction(() => { notes.forEach((n, i) => { const v = E.embed(E.noteText(n), dim); vecs[n.name] = v;
    db.run('INSERT INTO notes(id,name,title) VALUES (?,?,?)', [i + 1, n.name, n.title]);
    db.run('INSERT INTO notes_vec(rowid, embedding) VALUES (?, ?)', [BigInt(i + 1), E.vecBytes(v)]); }); });
  return vecs;
};
E.knn = (db, v, k) => db.query('SELECT n.name AS name, d.distance AS dist FROM notes_vec d JOIN notes n ON n.id = d.rowid WHERE d.embedding MATCH ? AND k = ? ORDER BY d.distance', [E.vecBytes(v), k]);

/* ---------- the three views of one note, and their disagreement ---------- */
E.symNeighbours = (kg, name) => {
  const r = E.kgCall({ op: 'query', handle: kg.handle, q: `shares(${JSON.stringify(name)}, B, C)`, limit: 200 });
  const out = {}; for (const a of r.answers || []) { out[a.bindings.B] = (out[a.bindings.B] || []); out[a.bindings.B].push(a.bindings.C); }
  return out;
};
E.delta = (db, kg, notes, vecs, k = 3) => {
  const rows = notes.map(n => {
    const geo = E.knn(db, vecs[n.name], k + 1).map(r => r.name).filter(x => x !== n.name).slice(0, k);
    const symMap = E.symNeighbours(kg, n.name); const sym = Object.keys(symMap).concat(n.links).filter((x, i, a) => a.indexOf(x) === i);
    const inter = geo.filter(x => sym.includes(x)); const uni = [...new Set(geo.concat(sym))];
    const d = uni.length ? 1 - inter.length / uni.length : 0;
    return { name: n.name, geo, sym, shared: symMap, delta: d, geoOnly: geo.filter(x => !sym.includes(x)), symOnly: sym.filter(x => !geo.includes(x)) };
  });
  return rows;
};
/* shared ideas that carry no link and sit far apart in the manifold: bridge candidates */
E.bridges = (notes, vecs, kg) => {
  const out = [];
  for (let i = 0; i < notes.length; i++) for (let j = i + 1; j < notes.length; j++) {
    const a = notes[i], b = notes[j]; if (a.links.includes(b.name) || b.links.includes(a.name)) continue;
    const sm = E.symNeighbours(kg, a.name)[b.name]; if (!sm) continue;
    const common = sm.filter(c => !['outage'].includes(c));
    const dom = n => n.tags[0];
    out.push({ a: a.name, b: b.name, via: sm, cos: E.cos(vecs[a.name], vecs[b.name]), cross: dom(a) !== dom(b) });
  }
  return out.sort((p, q) => (q.cross - p.cross) || (p.cos - q.cos));
};
/* ---------- warped distance and multi-hop retrieval ---------- */
E.edgeSets = (notes, kg) => {
  const causal = new Set(), conflict = new Set(), replaced = new Set();
  const rep = E.kgCall({ op: 'query', handle: kg.handle, q: 'replaced(X)', limit: 50 });
  for (const a of rep.answers || []) replaced.add(a.bindings.X);
  const chk = E.kgCall({ op: 'check', handle: kg.handle });
  const viol = chk.violations || [];
  const sym = (a, b) => [a, b].sort().join('|');
  for (const a of notes) for (const b of notes) if (a.name < b.name) {
    const shared = E.symNeighbours(kg, a.name)[b.name] || [];
    // a claim in a whose object is the subject of a claim in b (or the reverse) is a causal hand-off
    const hand = (x, y) => x.claims.some(([s, r, o]) => r === 'causes' && y.claims.some(([s2]) => s2 === o)) || x.claims.some(([s, r, o]) => r === 'causes' && y.claims.some(([s2, r2, o2]) => o2 === o && r2 === 'causes'));
    if (hand(a, b) || hand(b, a)) causal.add(sym(a.name, b.name));
    if (a.claims.some(c => c[1] === 'supersedes' && c[2] === b.name) || b.claims.some(c => c[1] === 'supersedes' && c[2] === a.name)) causal.add(sym(a.name, b.name));
    const oppose = a.claims.some(([s, r, o]) => (r === 'causes' || r === 'prevents') && b.claims.some(([s2, r2, o2]) => s2 === s && o2 === o && r2 !== r && (r2 === 'causes' || r2 === 'prevents')));
    if (oppose && !replaced.has(a.name) && !replaced.has(b.name)) conflict.add(sym(a.name, b.name));
  }
  return { causal, conflict, replaced, violations: viol, key: sym };
};
E.warp = (d, a, b, es, lam, mu) => {
  const k = es.key(a, b); let w = d;
  if (es.causal.has(k)) w *= (1 - lam);
  if (es.conflict.has(k)) w += mu;
  return w;
};
/* multi-hop: nearest notes to the query, then expand along the warped metric within a budget */
E.retrieve = (db, notes, vecs, es, qtext, { lam = 0.6, mu = 0.8, hops = 2, slack = 0.45, dim = 64, drop = true } = {}) => {
  const qv = E.embed(qtext, dim); const seeds = E.knn(db, qv, 1);
  const dist = {}; seeds.forEach(s => dist[s.name] = s.dist); const budget = seeds[0].dist + slack;
  const names = notes.map(n => n.name);
  for (let h = 0; h < hops; h++) for (const a of Object.keys(dist)) for (const b of names) if (b !== a) {
    const d = 1 - E.cos(vecs[a], vecs[b]); const nd = dist[a] + E.warp(d, a, b, es, lam, mu);
    if (nd <= budget + 1e-9 && (!(b in dist) || nd < dist[b] - 1e-12)) dist[b] = nd;
  }
  let res = Object.entries(dist).map(([name, d]) => ({ name, d, replaced: es.replaced.has(name), disputed: [...es.conflict].some(k => k.split('|').includes(name)) })).sort((x, y) => x.d - y.d);
  if (drop) res = res.filter(r => !r.replaced);
  return res;
};
/* plain similarity retrieval for comparison */
E.plain = (db, qtext, k, dim = 64) => E.knn(db, E.embed(qtext, dim), k);

/* ---------- replay: rebuild G and M from V alone ---------- */
E.hashStr = s => E.hash(s).toString(16).padStart(8, '0');
E.factsHash = (kg) => { const r = E.kgCall({ op: 'query', handle: kg.handle, q: 'claim(N, S, R, O)', limit: 1000 }); return E.hashStr((r.answers || []).map(a => ['N', 'S', 'R', 'O'].map(k => a.bindings[k]).join(' ')).sort().join('\n')); };
