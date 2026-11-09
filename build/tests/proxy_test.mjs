// The CORS proxy template (docs/proxy/cloudflare-worker.js): allowed hosts and origins only, headers and streaming passed through.
import assert from 'node:assert';
const { default: W } = await import(new URL('../../docs/proxy/cloudflare-worker.js', import.meta.url));
const O = 'https://lucky-edgelord.github.io', P = 'https://p.example/?';
let got = null;
globalThis.fetch = async (u, init) => { got = { u: String(u), init }; return new Response('{"models":[]}', { status: 200, headers: { 'content-type': 'application/json' } }); };
const req = (url, o = {}) => new Request(P + encodeURIComponent(url), { headers: { Origin: O, ...(o.h || {}) }, method: o.m || 'GET', body: o.b });
let r = await W.fetch(new Request(P + 'x', { method: 'OPTIONS', headers: { Origin: O } }));
assert.strictEqual(r.status, 204); assert.strictEqual(r.headers.get('access-control-allow-origin'), O);
r = await W.fetch(req('https://ollama.com/api/tags', { h: { Authorization: 'Bearer k' } }));
assert.strictEqual(r.status, 200); assert.strictEqual(got.u, 'https://ollama.com/api/tags'); assert.strictEqual(got.init.headers.get('Authorization'), 'Bearer k');
assert.strictEqual(r.headers.get('access-control-allow-origin'), O); assert.strictEqual(await r.text(), '{"models":[]}');
r = await W.fetch(req('https://ollama.com/api/chat', { m: 'POST', b: '{"a":1}', h: { 'Content-Type': 'application/json' } }));
assert.strictEqual(got.init.method, 'POST');
got = null; r = await W.fetch(req('https://evil.example/steal')); assert.strictEqual(r.status, 403); assert.strictEqual(got, null);
r = await W.fetch(req('http://ollama.com/api/tags')); assert.strictEqual(r.status, 403);
r = await W.fetch(new Request(P + encodeURIComponent('https://ollama.com/api/tags'), { headers: { Origin: 'https://other.site' } })); assert.strictEqual(r.status, 403);
r = await W.fetch(new Request('https://p.example/?%E0%A4%A', { headers: { Origin: O } })); assert.strictEqual(r.status, 400);
console.log('PROXY TESTS PASSED');
