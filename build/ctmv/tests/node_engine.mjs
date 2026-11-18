import fs from 'node:fs'; import vm from 'node:vm';
const KIT='/home/claude/lucky-edgelord/jade-agent-kit';
const of=globalThis.fetch; globalThis.fetch=async(u,...a)=>{u=String(u); if(u.startsWith('file:')) return new Response(fs.readFileSync(new URL(u))); return of(u,...a)};
globalThis.location={href:'file:///x/'};
const { createKit } = await import(KIT+'/dist/jade-agent-kit.js');
const kit = await createKit({busybox:false, scheduler:false});
const src = fs.readFileSync('vault.js','utf8')+fs.readFileSync('engine.js','utf8')+';globalThis.E=E;globalThis.VAULT=VAULT;';
(0,eval)(src);
await E.initKg(fs.readFileSync('/home/claude/lucky-edgelord/jade-vault/app/vendor/jade_kg.wasm'));
const db = await kit.sqlite.open?.(':memory:') ;
console.log(Object.keys(kit.sqlite), typeof db, db && Object.keys(Object.getPrototypeOf(db)));
const notes = E.notes(VAULT);
const kg = E.loadKg(notes); console.log('stats', JSON.stringify(kg.stats));
const vecs = await E.buildMani(db, notes, 64);
console.log('knn', JSON.stringify(E.knn(db, vecs['retry-storm'], 4)));
const rows = E.delta(db, kg, notes, vecs);
for (const r of rows) console.log(r.name.padEnd(18), r.delta.toFixed(2), 'geo', r.geo.join(','), '| sym', r.sym.join(','));
console.log('bridges', JSON.stringify(E.bridges(notes, vecs, kg).slice(0,5).map(b=>[b.a,b.b,b.via,b.cos.toFixed(2),b.cross])));
const es = E.edgeSets(notes, kg); console.log('causal', [...es.causal], 'conflict', [...es.conflict], 'replaced', [...es.replaced], 'viol', JSON.stringify(es.violations.map(v=>v.constraint)));
for (const lam of [0,0.6]) console.log('retrieve lam',lam, JSON.stringify(E.retrieve(db,notes,vecs,es,'what keeps the service down after a failure',{lam}).map(r=>[r.name,+r.d.toFixed(2)])));
console.log('plain', JSON.stringify(E.plain(db,'does a long cache time to live serve old data',3)));
console.log('retrieve cache', JSON.stringify(E.retrieve(db,notes,vecs,es,'does a long cache time to live serve old data',{drop:false}).map(r=>[r.name,+r.d.toFixed(2),r.replaced])));
console.log('hash', E.factsHash(kg));
console.log(E.kgCall({op:'verify',handle:kg.handle,claim:'leads_to(retry_storm, outage)'}).text);
for (const q of ['clients retry too much','how can overload be stopped','a swing goes higher and higher','does a long cache time to live serve old data','what is wrong with a long time to live','should clients retry straight away']) {
  console.log('Q',q); console.log('  plain', E.plain(db,q,3).map(r=>r.name+':'+r.dist.toFixed(2)).join(' '));
  for (const lam of [0,0.7]) console.log('  warp',lam, E.retrieve(db,notes,vecs,es,q,{lam,mu:0.8,slack:0.45}).map(r=>r.name+':'+r.d.toFixed(2)).join(' '));
}
