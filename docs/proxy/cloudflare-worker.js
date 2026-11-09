/* A small CORS proxy for the Lilith Learning Lab web version (Cloudflare Workers, free plan).
   ollama.com and some other APIs do not let web pages call them directly, so the browser blocks the request.
   Deploy this as a Worker, then in the web app: Settings > AI settings > CORS proxy = https://<your-worker>.workers.dev/?{url}
   The Android app does not need it.

   It only forwards to the hosts listed below, only answers pages from ALLOWED_ORIGINS, and passes your
   Authorization header through without storing it. Edit both lists to suit you. */
const HOSTS = ['ollama.com', 'api.openai.com', 'api.duckduckgo.com', 'r.jina.ai', 'en.wikipedia.org'];
const ALLOWED_ORIGINS = ['https://lucky-edgelord.github.io'];

export default {
  async fetch(req) {
    const origin = req.headers.get('Origin') || '';
    const cors = {
      'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Authorization, Content-Type, X-Return-Format',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin',
    };
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (!ALLOWED_ORIGINS.includes(origin)) return new Response('origin not allowed', { status: 403, headers: cors });
    let target;
    try { target = new URL(decodeURIComponent(new URL(req.url).search.slice(1))); } catch { return new Response('use ?<encoded url>', { status: 400, headers: cors }); }
    if (target.protocol !== 'https:' || !HOSTS.includes(target.hostname)) return new Response('host not allowed', { status: 403, headers: cors });
    const headers = new Headers();
    for (const h of ['Authorization', 'Content-Type', 'X-Return-Format']) { const v = req.headers.get(h); if (v) headers.set(h, v); }
    const r = await fetch(target, { method: req.method, headers, body: req.method === 'GET' ? undefined : req.body });
    const out = new Headers(r.headers); for (const [k, v] of Object.entries(cors)) out.set(k, v);
    return new Response(r.body, { status: r.status, headers: out });   // streamed, so chat replies arrive as they are written
  },
};
