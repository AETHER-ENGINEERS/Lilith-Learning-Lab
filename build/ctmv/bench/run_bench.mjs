// Run the CTMV claims tests on generated vaults, with the real engine (jade-kg + sqlite-vec via the Jade Agent Kit).
// Usage: node run_bench.mjs VAULTDIR OUT.json
import fs from 'node:fs';
const KIT = '/home/claude/lilith-learning-lab/build/vendor';
const HERE = new URL('.', import.meta.url).pathname;
const of = globalThis.fetch;
globalThis.fetch = async (u, ...a) => { u = String(u); if (u.endsWith('sqlite3.wasm')) return new Response(fs.readFileSync(KIT + '/jade-agent-kit/sqlite3.wasm')); return of(u, ...a); };
globalThis.location = { href: 'https://kit.local/' };
(0, eval)(fs.readFileSync(KIT + '/jade-agent-kit/jade-agent-kit.iife.js', 'utf8'));
const JadeKit = globalThis.JadeKit;
const kit = await JadeKit.createKit({ busybox: false, scheduler: false });
(0, eval)(fs.readFileSync(HERE + '../vault.js', 'utf8') + fs.readFileSync(HERE + '../engine.js', 'utf8') + ';globalThis.E=E;');
await E.initKg(fs.readFileSync(KIT + '/jade-vault/jade_kg.wasm'));

const [dir, outFile] = process.argv.slice(2);
const MODELS = ['bge', 'minilm'];
const STOP = new Set('a an the of to and or is are in on it its so as at by for with that this be we was were each every one two than then them they their yet our i my has have had does do what how'.split(' '));
const toks = s => s.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(w => w && !STOP.has(w));
const norm = v => { const n = Math.hypot(...v) || 1; return Float32Array.from(v, x => x / n); };
const dot = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; };
const rrf = (...lists) => { const sc = {}; lists.forEach(l => l.forEach((x, i) => sc[x] = (sc[x] || 0) + 1 / (60 + i + 1))); return Object.keys(sc).sort((a, b) => sc[b] - sc[a]); };
const mean = a => a.length ? a.reduce((s, x) => s + x, 0) / a.length : NaN;
function auroc(scores, labels) { const idx = scores.map((s, i) => i).sort((a, b) => scores[a] - scores[b]); let r = 0, rankSum = 0, i = 0; const n1 = labels.filter(Boolean).length, n0 = labels.length - n1; if (!n1 || !n0) return NaN;
  while (i < idx.length) { let j = i; while (j + 1 < idx.length && scores[idx[j + 1]] === scores[idx[i]]) j++; const avg = (i + j) / 2 + 1; for (let k = i; k <= j; k++) if (labels[idx[k]]) rankSum += avg; i = j + 1; } return (rankSum - n1 * (n1 + 1) / 2) / (n1 * n0); }
function ap(ranked, truth) { let hit = 0, s = 0; ranked.forEach((x, i) => { if (truth.has(x)) { hit++; s += hit / (i + 1); } }); return truth.size ? s / truth.size : NaN; }
const pk = (key => (a, b) => [a, b].sort().join('|'))();

const files = fs.readdirSync(dir).filter(f => /^vault_\d+\.json$/.test(f)).sort();
const results = [];
for (const f of files) {
  const V = JSON.parse(fs.readFileSync(dir + '/' + f, 'utf8'));
  const byName = {}; V.notes.forEach(n => byName[n.name] = n);
  const docTok = {}; V.notes.forEach(n => docTok[n.name] = toks(n.title + ' ' + n.body));
  const df = {}; Object.values(docTok).forEach(t => new Set(t).forEach(w => df[w] = (df[w] || 0) + 1));
  const NN = V.notes.length, idf = w => Math.log(1 + NN / (df[w] || 0.5));
  const tfv = ts => { const m = {}; ts.forEach(w => m[w] = (m[w] || 0) + idf(w)); const n = Math.hypot(...Object.values(m)) || 1; for (const k in m) m[k] /= n; return m; };
  const lexcos = (a, b) => { let s = 0; for (const k in a) if (b[k]) s += a[k] * b[k]; return s; };
  const docVec = {}; V.notes.forEach(n => docVec[n.name] = tfv(docTok[n.name]));
  const truthBridge = new Set(V.truth.bridges.map(([a, b]) => pk(a, b))), ffSet = new Set(V.truth.false_friends.map(([a, b]) => pk(a, b)));
  const anomNotes = new Set([...V.truth.bridges.flat(), ...V.truth.false_friends.flat()]);
  for (const model of MODELS) {
    const DIM = V.vec[model][V.notes[0].name].length;
    const VEC = new Map(); const vecs = {};
    V.notes.forEach(n => { vecs[n.name] = norm(V.vec[model][n.name]); VEC.set('NOTE:' + n.name, vecs[n.name]); });
    V.queries.forEach(q => VEC.set('Q:' + q.id, norm(q.vec[model])));
    E.embed = (t) => VEC.get(t); E.noteText = n => 'NOTE:' + n.name;
    const db = await kit.sqlite.open(':memory:');
    const t0 = Date.now();
    const baseNotes = V.notes.map(n => ({ name: n.name, title: n.title, body: n.body, tags: [n.domain], claims: [], links: n.links, replaces: n.name.startsWith('new-') ? n.links : [] }));
    await E.buildMani(db, baseNotes, DIM); const tM = Date.now() - t0;
    for (const variant of Object.keys(V.variants)) {
      if (process.env.VARIANTS && !process.env.VARIANTS.split(',').includes(variant)) continue;
      if (model !== 'bge' && !['oracle', 'realistic', 'tagger', 'acc70'].includes(variant)) continue;
      const notes = baseNotes.map(n => ({ ...n, claims: V.variants[variant][n.name] || [] }));
      const t1 = Date.now(); const kg = E.loadKg(notes); const tG = Date.now() - t1;
      const es = E.edgeSets(notes, kg);
      const rec = { seed: V.seed, model, variant, nNotes: NN, tM, tG, tagger_acc: V.tagger_acc };
      // ---- sqlite-vec sanity: its cosine distance equals 1 - dot ----
      { const a = V.notes[0].name, r = E.knn(db, vecs[a], 5); rec.vec_err = Math.max(...r.map(x => Math.abs(x.dist - (1 - dot(vecs[a], vecs[x.name]))))); }
      // ---- T1 bridges ----
      const cand = []; const cos = {};
      for (let i = 0; i < NN; i++) for (let j = i + 1; j < NN; j++) { const a = V.notes[i], b = V.notes[j]; if (a.domain === 'meta' || b.domain === 'meta' || a.domain === b.domain) continue; if (a.links.includes(b.name) || b.links.includes(a.name)) continue; const k = pk(a.name, b.name); cand.push(k); cos[k] = dot(vecs[a.name], vecs[b.name]); }
      const K = truthBridge.size; const shares = {};
      { rec.sharesTrunc = false; for (const n of notes) { const r = E.kgCall({ op: 'query', handle: kg.handle, q: `shares(${JSON.stringify(n.name)}, B, C)`, limit: 200 }); const rows = r.answers || []; if (rows.length >= 200) rec.sharesTrunc = true; for (const x of rows) { const k = pk(n.name, x.bindings.B); (shares[k] = shares[k] || new Set()).add(x.bindings.C); } } }
      const lex = {}; cand.forEach(k => { const [a, b] = k.split('|'); lex[k] = lexcos(docVec[a], docVec[b]); });
      const rank = (sc) => [...cand].sort((x, y) => sc[y] - sc[x]);
      const dense = rank(cos), lexr = rank(lex), hybrid = rrf(dense, lexr);
      const ctmvScore = {}; cand.forEach(k => ctmvScore[k] = shares[k] ? 1000 * shares[k].size - cos[k] : -cos[k]);   // shared idea first, least similar first
      const ctmv = rank(ctmvScore); const ctmvSet = cand.filter(k => shares[k]);
      const evalR = (r) => ({ pk: r.slice(0, K).filter(k => truthBridge.has(k)).length / K, ap: ap(r, truthBridge) });
      rec.t1 = { K, ncand: cand.length, base: K / cand.length, dense: evalR(dense), lexical: evalR(lexr), hybrid: evalR(hybrid), ctmv: evalR(ctmv),
        ctmvSet: { n: ctmvSet.length, prec: ctmvSet.length ? ctmvSet.filter(k => truthBridge.has(k)).length / ctmvSet.length : NaN, rec: ctmvSet.filter(k => truthBridge.has(k)).length / K },
        ffInTop: { dense: dense.slice(0, K).filter(k => ffSet.has(k)).length, ctmv: ctmv.slice(0, K).filter(k => ffSet.has(k)).length, lexical: lexr.slice(0, K).filter(k => ffSet.has(k)).length },
        // bridges the dense search ranks outside its top 3K
        hard: (() => { const rd = new Map(dense.map((k, i) => [k, i])); const hard = [...truthBridge].filter(k => rd.get(k) >= 3 * K); return { n: hard.length, ctmvRec: hard.length ? hard.filter(k => shares[k]).length / hard.length : NaN }; })() };
      // ---- T2 supersession / disputes ----
      const names = V.notes.map(n => n.name);
      const dtop = (q, k) => E.knn(db, VEC.get('Q:' + q.id), k).map(r => r.name);
      const qdoc = q => tfv(toks(q.text));
      const ltop = (q, k) => names.map(n => [n, lexcos(qdoc(q), docVec[n])]).sort((a, b) => b[1] - a[1]).slice(0, k).map(x => x[0]);
      const htop = (q, k) => rrf(dtop(q, NN), ltop(q, NN)).slice(0, k);
      const ctop = (q, k, o) => E.retrieve(db, notes, vecs, es, 'Q:' + q.id, { dim: DIM, ...o }).slice(0, k);
      const t2 = { sup: { dense: {}, hybrid: {}, ctmv: {} }, dis: { dense: {}, hybrid: {}, ctmv: {} } };
      const supQ = V.queries.filter(q => q.type === 'supersede'), disQ = V.queries.filter(q => q.type === 'dispute');
      const sup = (get) => ({ hit: mean(supQ.map(q => get(q).includes(q.relevant[0]) ? 1 : 0)), stale: mean(supQ.map(q => get(q).includes(q.stale[0]) ? 1 : 0)), both: mean(supQ.map(q => get(q).includes(q.relevant[0]) && get(q).includes(q.stale[0]) ? 1 : 0)) });
      t2.sup.dense = sup(q => dtop(q, 3)); t2.sup.hybrid = sup(q => htop(q, 3)); t2.sup.ctmv = sup(q => ctop(q, 3).map(r => r.name));
      const dis = (get) => { const r = disQ.map(q => get(q)); return { any: mean(r.map((x, i) => disQ[i].relevant.some(n => x.map(y => y.name || y).includes(n)) ? 1 : 0)), both: mean(r.map((x, i) => disQ[i].relevant.every(n => x.map(y => y.name || y).includes(n)) ? 1 : 0)), flagged: mean(r.map((x, i) => x.some(y => y.disputed && disQ[i].relevant.includes(y.name)) ? 1 : 0)), silentBoth: mean(r.map((x, i) => (disQ[i].relevant.every(n => x.map(y => y.name || y).includes(n)) && !x.some(y => y.disputed)) ? 1 : 0)) }; };
      const ldd = q => { const d = dtop(q, 4); return d.filter(x => !d.some(y => y !== x && byName[y].links.includes(x))).slice(0, 3); };   // drop a note when another result links to it
      t2.sup.linkdedupe = sup(ldd); t2.dis.linkdedupe = dis(ldd);
      // same filter, but every note also carries two random see-also links (as real vaults do), and replacements are only recognised by explicit links
      const rngL = (() => { let x = 12345; return () => (x = (x * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff; })();
      const seeAlso = {}; for (const n of V.notes) seeAlso[n.name] = [0, 1].map(() => V.notes[Math.floor(rngL() * V.notes.length)].name).filter(m => m !== n.name);
      const ldn = q => { const d = dtop(q, 4); return d.filter(x => !d.some(y => y !== x && (byName[y].links.includes(x) || (seeAlso[y] || []).includes(x)))).slice(0, 3); };
      t2.sup.linkdedupe_seealso = sup(ldn); t2.dis.linkdedupe_seealso = dis(ldn);
      t2.dis.dense = dis(q => dtop(q, 3)); t2.dis.hybrid = dis(q => htop(q, 3)); t2.dis.ctmv = dis(q => ctop(q, 3));
      // constraint check
      { const chk = E.kgCall({ op: 'check', handle: kg.handle }); const vs = (chk.violations || []).map(v => pk(v.bindings.N1, v.bindings.N2)); const vset = new Set(vs);
        const dset = new Set(V.truth.disputes.map(([a, b]) => pk(a, b))), supset = new Set(V.truth.supersede.map(s => pk(s.old, s.new))), benign = new Set(V.truth.benign.map(([a, b]) => pk(a, b)));
        t2.check = { disputeRecall: [...dset].filter(k => vset.has(k)).length / dset.size, falsePos: vs.filter(k => !dset.has(k)).length, supersedeFired: [...supset].filter(k => vset.has(k)).length / supset.size, benignFired: [...benign].filter(k => vset.has(k)).length / benign.size, nViol: vset.size };
        const rep = E.kgCall({ op: 'query', handle: kg.handle, q: 'replaced(X)', limit: 100 }); const rs = new Set((rep.answers || []).map(a => a.bindings.X)); t2.replacedRecall = V.truth.supersede.filter(s => rs.has(s.old)).length / V.truth.supersede.length; t2.replacedFalse = [...rs].filter(x => !V.truth.supersede.some(s => s.old === x)).length; }
      rec.t2 = t2;
      // ---- T3 multi-hop chains ----
      const chainQ = V.queries.filter(q => q.type === 'chain');
      const adj = {}; notes.forEach(n => n.claims.forEach(([s, r, o]) => { if (r === 'causes') (adj[s] = adj[s] || []).push([o, n.name]); }));
      const subjNotes = {}; notes.forEach(n => n.claims.forEach(([s, r, o]) => { if (r === 'causes') (subjNotes[s] = subjNotes[s] || []).push(n.name); }));
      const gexp = (q, k) => { const seed = dtop(q, 1)[0]; const out = [seed]; let front = (byName[seed] && notes.find(n => n.name === seed).claims.filter(c => c[1] === 'causes').map(c => c[2])) || []; const seen = new Set(out);
        for (let h = 0; h < 4 && out.length < k; h++) { const nxt = []; for (const e of front) for (const nm of subjNotes[e] || []) if (!seen.has(nm)) { seen.add(nm); out.push(nm); nxt.push(...notes.find(n => n.name === nm).claims.filter(c => c[1] === 'causes').map(c => c[2])); } front = nxt; } return out.slice(0, k); };
      const ch = (get) => { const r = chainQ.map(q => get(q).map(y => y.name || y)); return { rec: mean(r.map((x, i) => chainQ[i].relevant.filter(n => x.includes(n)).length / chainQ[i].relevant.length)), full: mean(r.map((x, i) => chainQ[i].relevant.every(n => x.includes(n)) ? 1 : 0)), prec: mean(r.map((x, i) => x.length ? x.filter(n => chainQ[i].relevant.includes(n)).length / x.length : 0)) }; };
      const prf = q => { const d1 = dtop(q, 1)[0], qv = VEC.get('Q:' + q.id); return E.knn(db, norm(Array.from(qv, (x, i) => x + vecs[d1][i])), 3).map(r => r.name); };   // pseudo-relevance feedback
      rec.t3 = { prf: ch(prf), dense: ch(q => dtop(q, 3)), lexical: ch(q => ltop(q, 3)), hybrid: ch(q => htop(q, 3)), gexpand: ch(q => gexp(q, 3)) };
      for (const lam of [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]) for (const slack of [0.3, 0.5]) rec.t3[`ctmv_l${lam}_s${slack}`] = ch(q => ctop(q, 3, { lam, mu: 0.8, slack }));
      // ---- T4 delta ----
      const dl = E.delta(db, kg, notes, vecs, 3); const lab = dl.map(r => anomNotes.has(r.name));
      const cc = notes.map(n => n.claims.length);
      rec.t4 = { auroc_delta: auroc(dl.map(r => r.delta), lab), auroc_sparsity: auroc(cc.map(c => -c), lab), auroc_random: 0.5, nPos: lab.filter(Boolean).length,
        deltaMean: mean(dl.map(r => r.delta)), deltaMeanPos: mean(dl.filter((r, i) => lab[i]).map(r => r.delta)), deltaMeanNeg: mean(dl.filter((r, i) => !lab[i]).map(r => r.delta)), fracDeltaOne: mean(dl.map(r => r.delta >= 0.999 ? 1 : 0)) };
      // ---- T6 replay (oracle only) ----
      if (variant === 'oracle') {
        const allFacts = (h) => E.hashStr(notes.flatMap(n => (E.kgCall({ op: 'query', handle: h, q: `claim(${JSON.stringify(n.name)}, S, R, O)`, limit: 200 }).answers || []).map(a => [n.name, a.bindings.S, a.bindings.R, a.bindings.O].join(' '))).sort().join('\n'));
        const fp = allFacts(kg.handle); const sh = [...notes].sort(() => 0.5 - Math.random()); const kg2 = E.loadKg(sh); const fp2 = allFacts(kg2.handle);
        const subs = [...new Set(notes.flatMap(n => n.claims.filter(c => c[1] === 'causes').map(c => c[0])))]; const ans = (h) => JSON.stringify(subs.flatMap(sj => (E.kgCall({ op: 'query', handle: h, q: `leads_to(${JSON.stringify(sj)}, Y)`, limit: 200 }).answers || []).map(a => sj + '>' + a.bindings.Y)).sort());
        rec.t6 = { fpSame: fp === fp2, answersSame: ans(kg.handle) === ans(kg2.handle) };
        rec.nn = {}; for (const n of names.slice(0, 60)) rec.nn[n] = E.knn(db, vecs[n], 4).filter(r => r.name !== n).slice(0, 3).map(r => r.name);
        rec.fp = fp;
        E.kgCall({ op: 'free', handle: kg2.handle });
      }
      E.kgCall({ op: 'free', handle: kg.handle });
      results.push(rec);
    }
    db.close?.({ save: false });
  }
  process.stderr.write(`vault ${V.seed} done\n`);
}
fs.writeFileSync(outFile, JSON.stringify(results));
