/* Lilith Learning Lab: optional AI features. Ollama (local), Ollama Cloud, any OpenAI-compatible endpoint;
   web search and fetch; the Ollama decisions API (/v1/systemone); BM25 search over installed courses; the research-based course builder.
   Nothing here runs unless the person turns it on in Settings > AI. */
(function (root) {
  'use strict';
  var AI = {};
  var DEF = { provider: 'ollama', ollamaUrl: 'http://localhost:11434', ollamaModel: '', cloudKey: '', cloudModel: '', openaiUrl: 'https://api.openai.com/v1', openaiKey: '', openaiModel: '',
              search: true, decide: true, decideModel: '', corsProxy: '' };
  var store = (function () { try { return root.localStorage; } catch (e) { return null; } })();
  AI.cfg = function () { var c = {}; try { c = JSON.parse((store && store.getItem('lilith.ai')) || '{}'); } catch (e) {} var o = {}; for (var k in DEF) o[k] = c[k] === undefined ? DEF[k] : c[k]; return o; };
  AI.setCfg = function (patch) { var c = AI.cfg(); for (var k in patch) c[k] = patch[k]; try { store && store.setItem('lilith.ai', JSON.stringify(c)); } catch (e) {} return c; };
  AI.CLOUD = 'https://ollama.com';
  AI.enabled = function () { var c = AI.cfg(); return c.provider === 'openai' ? !!(c.openaiModel) : c.provider === 'cloud' ? !!(c.cloudKey && c.cloudModel) : !!c.ollamaModel; };

  /* ---------- helpers ---------- */
  function trimUrl(u) { return String(u || '').replace(/\/+$/, ''); }
  function viaProxy(u) { var p = AI.cfg().corsProxy; if (!p) return u; return p.indexOf('{url}') >= 0 ? p.replace('{url}', encodeURIComponent(u)) : p + u; }
  function http(u, init) { return (root.__aiFetch || root.fetch.bind(root))(viaProxy(u), init); }
  async function errOf(r) { var m = 'HTTP ' + r.status; try { var j = await r.json(); m = (j.error && (j.error.message || j.error)) || j.message || m; } catch (e) {} if (r.status === 401) m = 'the API key was rejected (401)'; return new Error(typeof m === 'string' ? m : JSON.stringify(m)); }
  AI.extractJson = function (t) {
    t = String(t || '').replace(/```(?:json)?/gi, '').trim();
    var a = t.indexOf('{'), b = t.lastIndexOf('}'); if (a < 0 || b < a) throw new Error('no JSON in the reply');
    var s = t.slice(a, b + 1);
    try { return JSON.parse(s); } catch (e) { return JSON.parse(s.replace(/,\s*([}\]])/g, '$1')); }
  };
  AI.slug = function (s) { return String(s || 'course').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48) || 'course'; };

  /* ---------- BM25 (Okapi ranking as in Python's rank_bm25, with the Lucene idf) ---------- */
  var STOP = {}; 'a an the and or of to in on for is are was be as at by it this that with from not but if then so do does can will'.split(' ').forEach(function (w) { STOP[w] = 1; });
  function toks(s) { return String(s || '').toLowerCase().split(/[^a-z0-9]+/).filter(function (w) { return w && !STOP[w]; }); }
  AI.bm25 = function (docs, k1, b) {
    k1 = k1 || 1.5; b = b === undefined ? 0.75 : b;
    var N = docs.length, tf = [], df = {}, len = 0;
    docs.forEach(function (d) { var t = toks(d.text), m = {}; t.forEach(function (w) { m[w] = (m[w] || 0) + 1; }); tf.push({ m: m, n: t.length }); len += t.length; for (var w in m) df[w] = (df[w] || 0) + 1; });
    var avg = N ? len / N : 0, idf = {};
    for (var w in df) idf[w] = Math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5));   // Lucene-style idf: never negative, so tiny course sets still rank
    return { search: function (q, n) {
      var qs = toks(q), out = [];
      for (var i = 0; i < N; i++) { var s = 0; for (var j = 0; j < qs.length; j++) { var f = tf[i].m[qs[j]]; if (f) s += (idf[qs[j]] || 0) * f * (k1 + 1) / (f + k1 * (1 - b + b * tf[i].n / (avg || 1))); } if (s > 0) out.push({ i: i, score: s, doc: docs[i] }); }
      out.sort(function (x, y) { return y.score - x.score; }); return out.slice(0, n || 5);
    } };
  };
  /* index every chapter of the installed courses: one passage per chapter part */
  AI.indexCourses = function (courses) {
    var docs = [];
    courses.forEach(function (c) { (c.chapters || []).forEach(function (ch, i) {
      var head = c.title + ' / ' + (i + 1) + '. ' + ch.title;
      var parts = [['summary', (ch.summary || []).join(' ')], ['glossary', (ch.glossary || []).map(function (g) { return g.term + ': ' + g.def; }).join(' ')], ['key points', (ch.keyPoints || []).join(' ')]];
      (ch.lesson || []).forEach(function (b) { if (b && (b.type === 'text' || !b.type) && b.items) parts.push(['lesson', b.items.join(' ')]); else if (typeof b === 'string') parts.push(['lesson', b]); });
      parts.forEach(function (p) { if (p[1].trim()) docs.push({ course: c.id, ch: i, head: head, kind: p[0], text: head + ' ' + p[1], body: p[1] }); });
    }); });
    return { docs: docs, idx: AI.bm25(docs) };
  };

  /* ---------- providers ---------- */
  function ollamaHost(c) { return c.provider === 'cloud' ? AI.CLOUD : trimUrl(c.ollamaUrl); }
  function headersFor(c) {
    var h = { 'Content-Type': 'application/json' };
    if (c.provider === 'cloud' && c.cloudKey) h.Authorization = 'Bearer ' + c.cloudKey;
    if (c.provider === 'openai' && c.openaiKey) h.Authorization = 'Bearer ' + c.openaiKey;
    return h;
  }
  AI.model = function () { var c = AI.cfg(); return c.provider === 'openai' ? c.openaiModel : c.provider === 'cloud' ? c.cloudModel : c.ollamaModel; };
  AI.listModels = async function () {
    var c = AI.cfg(), r;
    if (c.provider === 'openai') { r = await http(trimUrl(c.openaiUrl) + '/models', { headers: headersFor(c) }); if (!r.ok) throw await errOf(r); var j = await r.json(); return (j.data || j.models || []).map(function (m) { return m.id || m.name; }).filter(Boolean).sort(); }
    r = await http(ollamaHost(c) + '/api/tags', { headers: headersFor(c) }); if (!r.ok) throw await errOf(r);
    var t = await r.json(); return (t.models || []).map(function (m) { return m.name || m.model; }).filter(Boolean).sort();
  };
  function toOpenAI(msgs) {
    var out = [], seq = 0, pend = [];
    msgs.forEach(function (m) {
      if (m.role === 'tool') { var p = pend.shift(); out.push({ role: 'tool', tool_call_id: p ? p.id : 'call_0', content: String(m.content || '') }); return; }
      if (m.role === 'assistant' && m.tool_calls && m.tool_calls.length) {
        pend = []; var calls = m.tool_calls.map(function (t) { var id = 'call_' + (++seq); pend.push({ id: id }); return { id: id, type: 'function', function: { name: t.name, arguments: JSON.stringify(t.args || {}) } }; });
        out.push({ role: 'assistant', content: m.content || null, tool_calls: calls }); return;
      }
      out.push({ role: m.role, content: String(m.content || '') });
    }); return out;
  }
  function toOllama(msgs) {
    return msgs.map(function (m) {
      if (m.role === 'tool') return { role: 'tool', content: String(m.content || ''), tool_name: m.name };
      if (m.role === 'assistant' && m.tool_calls && m.tool_calls.length) return { role: 'assistant', content: m.content || '', tool_calls: m.tool_calls.map(function (t) { return { function: { name: t.name, arguments: t.args || {} } }; }) };
      return { role: m.role, content: String(m.content || '') };
    });
  }
  async function readLines(r, onLine) {
    var rd = r.body.getReader(), dec = new TextDecoder(), buf = '';
    for (;;) { var x = await rd.read(); if (x.done) break; buf += dec.decode(x.value, { stream: true }); var i; while ((i = buf.indexOf('\n')) >= 0) { var line = buf.slice(0, i).trim(); buf = buf.slice(i + 1); if (line) onLine(line); } }
    if (buf.trim()) onLine(buf.trim());
  }
  /* one model turn: returns { content, toolCalls:[{name,args}] } and streams text through onDelta */
  AI.chat = async function (messages, o) {
    o = o || {}; var c = AI.cfg(), content = '', calls = [], model = o.model || AI.model();
    if (!model) throw new Error('No AI model is selected (Settings > AI).');
    if (c.provider === 'openai') {
      var body = { model: model, messages: toOpenAI(messages), stream: true, temperature: o.temperature === undefined ? 0.4 : o.temperature };
      if (o.tools && o.tools.length) { body.tools = o.tools; body.tool_choice = 'auto'; }
      var r = await http(trimUrl(c.openaiUrl) + '/chat/completions', { method: 'POST', headers: headersFor(c), body: JSON.stringify(body), signal: o.signal });
      if (!r.ok) throw await errOf(r);
      var acc = [];
      await readLines(r, function (line) {
        if (line.indexOf('data:') !== 0) return; var d = line.slice(5).trim(); if (d === '[DONE]') return; var j; try { j = JSON.parse(d); } catch (e) { return; }
        if (j.error) throw new Error(j.error.message || String(j.error));
        var dl = (j.choices && j.choices[0] && j.choices[0].delta) || {};
        if (dl.content) { content += dl.content; o.onDelta && o.onDelta(dl.content); }
        (dl.tool_calls || []).forEach(function (tc) { var i = tc.index === undefined ? acc.length : tc.index; var a = acc[i] = acc[i] || { name: '', args: '' }; if (tc.function && tc.function.name) a.name += tc.function.name; if (tc.function && tc.function.arguments) a.args += tc.function.arguments; });
      });
      acc.forEach(function (a) { if (a.name) { var args = {}; try { args = JSON.parse(a.args || '{}'); } catch (e) {} calls.push({ name: a.name, args: args }); } });
      return { content: content, toolCalls: calls };
    }
    var req = { model: c.provider === 'cloud' ? String(model).replace(/[:\-]cloud$/i, '') : model, messages: toOllama(messages), stream: true, options: { temperature: o.temperature === undefined ? 0.4 : o.temperature } };
    if (o.tools && o.tools.length) req.tools = o.tools;
    var r2 = await http(ollamaHost(c) + '/api/chat', { method: 'POST', headers: headersFor(c), body: JSON.stringify(req), signal: o.signal });
    if (!r2.ok) throw await errOf(r2);
    await readLines(r2, function (line) {
      var j; try { j = JSON.parse(line); } catch (e) { return; } if (j.error) throw new Error(j.error);
      var m = j.message || {}; if (m.content) { content += m.content; o.onDelta && o.onDelta(m.content); }
      (m.tool_calls || []).forEach(function (t) { var a = t.function && t.function.arguments; if (typeof a === 'string') { try { a = JSON.parse(a); } catch (e) { a = {}; } } calls.push({ name: t.function.name, args: a || {} }); });
    });
    return { content: content, toolCalls: calls };
  };
  AI.complete = async function (messages, o) { var r = await AI.chat(messages, o); return r.content; };

  /* ---------- tools: course search, web search, web fetch ---------- */
  AI.TOOLS = {
    search_course: { description: 'Search the installed courses (BM25) for passages about a topic. Use first for questions about course material.', params: { query: 'what to look for' } },
    web_search: { description: 'Search the web for current information. Returns titles, URLs and snippets.', params: { query: 'search query' } },
    web_fetch: { description: 'Fetch a web page and return it as plain text or Markdown.', params: { url: 'http or https URL' } }
  };
  AI.toolDefs = function (names) {
    return names.map(function (n) { var t = AI.TOOLS[n], props = {}, req = []; for (var k in t.params) { props[k] = { type: 'string', description: t.params[k] }; req.push(k); }
      return { type: 'function', function: { name: n, description: t.description, parameters: { type: 'object', properties: props, required: req } } }; });
  };
  function clip(s, n) { s = String(s || ''); return s.length > n ? s.slice(0, n) + '\n[...cut]' : s; }
  AI.webSearch = async function (query, max) {
    max = max || 5; var c = AI.cfg(), errors = [];
    var tries = [];
    if (c.cloudKey) tries.push('ollama');
    tries.push('wikipedia', 'ddg');
    for (var i = 0; i < tries.length; i++) {
      var p = tries[i], res = [];
      try {
        if (p === 'ollama') {
          var r = await http(AI.CLOUD + '/api/web_search', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + c.cloudKey }, body: JSON.stringify({ query: query, max_results: max }) });
          if (!r.ok) throw new Error('HTTP ' + r.status);
          res = ((await r.json()).results || []).map(function (x) { return { title: x.title, url: x.url, snippet: clip(x.content, 600) }; });
        } else if (p === 'wikipedia') {
          var w = await http('https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&origin=*&srlimit=' + max + '&srsearch=' + encodeURIComponent(query)); if (!w.ok) throw new Error('HTTP ' + w.status);
          res = (((await w.json()).query || {}).search || []).map(function (x) { return { title: x.title, url: 'https://en.wikipedia.org/wiki/' + encodeURIComponent(x.title.replace(/ /g, '_')), snippet: x.snippet.replace(/<[^>]+>/g, '') }; });
        } else {
          var d = await http('https://api.duckduckgo.com/?format=json&no_html=1&skip_disambig=1&q=' + encodeURIComponent(query)); if (!d.ok) throw new Error('HTTP ' + d.status); var dj = await d.json();
          if (dj.AbstractText) res.push({ title: dj.Heading || query, url: dj.AbstractURL, snippet: dj.AbstractText });
          (dj.RelatedTopics || []).forEach(function (t) { (t.Topics || [t]).forEach(function (u) { if (u.FirstURL) res.push({ title: (u.Text || '').split(' - ')[0], url: u.FirstURL, snippet: u.Text || '' }); }); });
          res = res.slice(0, max);
        }
        if (!res.length) throw new Error('no results');
        return res;
      } catch (e) { errors.push(p + ': ' + (e.message === 'Failed to fetch' ? 'blocked (network or CORS)' : e.message)); }
    }
    throw new Error('web search failed (' + errors.join('; ') + ')');
  };
  AI.webFetch = async function (url) {
    if (!/^https?:\/\//.test(url)) throw new Error('url must start with http:// or https://');
    var c = AI.cfg();
    if (c.cloudKey) { try { var r = await http(AI.CLOUD + '/api/web_fetch', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + c.cloudKey }, body: JSON.stringify({ url: url }) }); if (r.ok) { var j = await r.json(); return '# ' + (j.title || url) + '\n\n' + (j.content || ''); } } catch (e) {} }
    var r2 = await http('https://r.jina.ai/' + url, { headers: { 'X-Return-Format': 'markdown' } });
    if (!r2.ok) throw new Error('fetch failed: HTTP ' + r2.status); return r2.text();
  };
  AI.runTool = async function (name, args, ctx) {
    try {
      if (name === 'search_course') { var hits = ctx && ctx.courseIndex ? ctx.courseIndex.idx.search(args.query, 4) : []; return hits.length ? hits.map(function (h, i) { return (i + 1) + '. ' + h.doc.head + ' (' + h.doc.kind + ')\n' + clip(h.doc.body, 700); }).join('\n\n') : 'No matching passage in the installed courses.'; }
      if (name === 'web_search') { var r = await AI.webSearch(String(args.query || '')); return r.map(function (x, i) { return (i + 1) + '. ' + x.title + '\n   ' + x.url + '\n   ' + String(x.snippet).replace(/\s+/g, ' ').trim(); }).join('\n\n'); }
      if (name === 'web_fetch') return clip(await AI.webFetch(String(args.url || '')), 6000);
      return 'Unknown tool ' + name;
    } catch (e) { return 'Tool error: ' + e.message; }
  };
  /* chat with tools: loops until the model answers in text (max rounds) */
  AI.agent = async function (messages, o) {
    o = o || {}; var c = AI.cfg(), names = (o.tools || []).filter(function (n) { return n === 'search_course' || c.search; });
    var defs = names.length ? AI.toolDefs(names) : null, msgs = messages.slice(), final = '', noTools = false;
    for (var round = 0; round < (o.maxRounds || 4); round++) {
      var res;
      try { res = await AI.chat(msgs, { tools: noTools ? null : defs, onDelta: o.onDelta, signal: o.signal, temperature: o.temperature }); }
      catch (e) { if (defs && !noTools && /tool/i.test(e.message)) { noTools = true; round--; continue; } throw e; }
      if (!res.toolCalls.length) { final = res.content; break; }
      msgs.push({ role: 'assistant', content: res.content, tool_calls: res.toolCalls });
      for (var i = 0; i < res.toolCalls.length; i++) {
        var t = res.toolCalls[i]; o.onTool && o.onTool(t.name, t.args);
        var out = await AI.runTool(t.name, t.args, o); o.onToolResult && o.onToolResult(t.name, out);
        msgs.push({ role: 'tool', name: t.name, content: out });
      }
      if (round === (o.maxRounds || 4) - 1) { var last = await AI.chat(msgs, { onDelta: o.onDelta, signal: o.signal }); final = last.content; }
    }
    return final;
  };

  /* ---------- decisions API (Ollama /v1/systemone, local and cloud) ---------- */
  AI.olReq = function (body, cloud) {
    var maps = {}, qs = {};
    Object.keys(body.questions || {}).forEach(function (name) {
      var q = body.questions[name], nq = {}; for (var k in q) nq[k] = q[k];
      if ((q.type || 'choice') === 'choice' && Array.isArray(q.criteria)) {
        var keys = q.criteria.map(function (o, i) { var s = String(o).trim(); var k0 = s.length && s.length <= 100 ? s : 'option_' + (i + 1); return q.criteria.findIndex(function (x) { return String(x).trim() === s; }) === i ? k0 : 'option_' + (i + 1); });
        var cr = {}; keys.forEach(function (k, i) { cr[k] = String(q.criteria[i]); }); nq.criteria = cr; maps[name] = { keys: keys, opts: q.criteria.map(String) };
      }
      qs[name] = nq;
    });
    var model = String(body.model || ''); if (cloud) model = model.replace(/[:\-]cloud$/i, '');
    var out = {}; for (var k2 in body) out[k2] = body[k2]; out.model = model; out.questions = qs; return { req: out, maps: maps };
  };
  AI.olAns = function (a, m) {
    if (!a || typeof a !== 'object') return a; var out = {}; for (var k in a) out[k] = a[k];
    if ('choice' in a && m) { var i = typeof a.choice === 'number' ? a.choice : m.keys.indexOf(String(a.choice)); if (i >= 0 && i < m.opts.length) out.choice = m.opts[i]; }
    if (typeof a.noul === 'number') { var p = Math.max(0, Math.min(1, a.noul)); out.noul = p >= 0.5; out.p_true = p; if (out.confidence == null) out.confidence = Math.max(p, 1 - p); }
    return out;
  };
  /* type: 'yesno' | 'score' (options = level descriptions, lowest first) | 'choice'. Returns {answer, confidence, via}. */
  AI.decide = async function (o) {
    var c = AI.cfg(), t = o.type === 'yesno' ? 'noul' : (o.type || 'choice');
    var q = { type: t, instructions: String(o.question || '') };
    if (t === 'choice' || t === 'score') q.criteria = (o.options || []).map(String);
    var state = typeof o.state === 'string' ? o.state : JSON.stringify(o.state || '');
    var native = c.decide && c.provider !== 'openai' && (c.decideModel || c.provider === 'cloud');
    if (native) {
      var cloud = c.provider === 'cloud', model = c.decideModel || (cloud ? 'clef' : '');
      if (model) {
        var pr = AI.olReq({ model: model, state: state, questions: { q: q } }, cloud);
        var r = await http(ollamaHost(c) + '/v1/systemone', { method: 'POST', headers: headersFor(c), body: JSON.stringify(pr.req), signal: o.signal });
        if (!r.ok) throw await errOf(r);
        var j = await r.json(), a = AI.olAns((j.answers || {}).q, pr.maps.q);
        if (!a) throw new Error('the decision model returned no answer');
        var ans = t === 'noul' ? a.noul : t === 'score' ? a.score : a.choice;
        return { answer: ans, confidence: a.confidence == null ? null : +a.confidence, via: 'decision model ' + (j.model || model) };
      }
    }
    /* fallback: ask the chat model for a small JSON verdict */
    var ask = 'Answer ONLY with JSON {"answer": ..., "confidence": 0..1}. ' + (t === 'noul' ? 'answer is true or false.' : t === 'score' ? 'answer is an integer index into the levels (0 = lowest): ' + JSON.stringify(q.criteria) : 'answer is exactly one of: ' + JSON.stringify(q.criteria)) + '\nQuestion: ' + q.instructions + '\nText:\n' + state;
    var txt = await AI.complete([{ role: 'user', content: ask }], { temperature: 0, signal: o.signal });
    var v = AI.extractJson(txt);
    return { answer: v.answer, confidence: v.confidence == null ? null : +v.confidence, via: 'chat model' };
  };

  /* ---------- the teacher's persona and context ---------- */
  AI.teacherSystem = function (ctx) {
    var s = 'You are Teacher, the friendly tutor inside Lilith Learning Lab. Explain simply first (analogies, plain words), then add precision. Use the Feynman method: when the learner is unsure, ask them to explain it back in their own words and point to the gap. Keep replies short enough for a phone screen. If you are not sure, say so. ';
    s += 'Use search_course to ground answers in the installed courses, and web_search and web_fetch when the course does not cover something or the question is about recent facts; cite the URLs you used.';
    if (ctx && ctx.course) s += '\nThe learner is studying "' + ctx.course + '"' + (ctx.chapter ? ', chapter "' + ctx.chapter + '"' : '') + '.';
    if (ctx && ctx.passages) s += '\nRelevant passages from the course:\n' + ctx.passages;
    return s;
  };

  /* ---------- the research-based course builder ---------- */
  var SCHEMA = 'A chapter object: {"title":"", "maps":[{"title":"","links":["A | relation | B", ...]}], "summary":["2-3 short sentences"], "glossary":[{"term":"","def":""}], "keyPoints":["",...], ' +
    '"lesson":[{"type":"text","items":["short paragraphs"]}], "quiz":[{"q":"","options":["","",""],"answer":0,"explain":""}], "cards":[{"q":"","a":""}], ' +
    '"practice":[{"type":"fill","title":"","text":"The word is {{answer}}."},{"type":"order","title":"","items":["first","second","third"]},{"type":"match","title":"","pairs":[["term","meaning"],["",""]]}], ' +
    '"feynman":{"analogy":"a plain-words analogy of under 330 characters, as if for a ten-year-old","stall":"one question the learner must be able to answer"}}';
  AI.buildCourse = async function (o) {
    var log = o.onLog || function () {}, sig = o.signal, topic = String(o.topic || '').trim(), level = o.level || 'Beginner', n = Math.max(3, Math.min(12, o.chapters || 6));
    if (!topic) throw new Error('Say what the course is about.');
    var sources = [], seen = {};
    function addSrc(url, title) { if (url && !seen[url]) { seen[url] = 1; sources.push({ url: url, title: title || url }); } }
    async function research(queries, pages) {
      var notes = '';
      for (var qi = 0; qi < queries.length; qi++) {
        if (sig && sig.aborted) throw new Error('Cancelled');
        var res = []; try { log('Searching: ' + queries[qi]); res = await AI.webSearch(queries[qi], 5); } catch (e) { log('Search failed: ' + e.message); }
        for (var i = 0; i < Math.min(pages, res.length); i++) {
          var r = res[i]; addSrc(r.url, r.title); notes += '## ' + r.title + ' (' + r.url + ')\n' + clip(r.snippet, 500) + '\n';
          try { log('Reading: ' + r.url); notes += clip(await AI.webFetch(r.url), 2500) + '\n\n'; } catch (e) { log('Could not read ' + r.url); }
        }
      }
      return notes;
    }
    /* 1. overview research and the outline */
    var overview = AI.cfg().search ? await research([topic + ' overview', topic + ' syllabus course outline'], 2) : '';
    log('Planning the outline');
    var outlineTxt = await AI.complete([{ role: 'system', content: 'You design short online courses. Reply with JSON only.' }, { role: 'user', content:
      'Design a ' + n + '-chapter course on "' + topic + '" for ' + level + ' learners, in a logical teaching order. Use these research notes if present.\n\nNotes:\n' + clip(overview, 7000) +
      '\n\nReply as {"title":"","subtitle":"","description":"2 sentences","category":"","tags":["",...],"chapters":[{"title":"","focus":"what it teaches","queries":["one web search query"]}]}' }], { temperature: 0.3, signal: sig });
    var plan = AI.extractJson(outlineTxt); if (!plan.chapters || !plan.chapters.length) throw new Error('The model did not return an outline.');
    plan.chapters = plan.chapters.slice(0, n);
    var chapters = [];
    /* 2. each chapter: research, write, check */
    for (var ci = 0; ci < plan.chapters.length; ci++) {
      if (sig && sig.aborted) throw new Error('Cancelled');
      var pc = plan.chapters[ci]; log('Chapter ' + (ci + 1) + '/' + plan.chapters.length + ': ' + pc.title);
      var notes = AI.cfg().search ? await research([(pc.queries && pc.queries[0]) || (topic + ' ' + pc.title)], 2) : '';
      var prompt = 'Write chapter ' + (ci + 1) + ' of the course "' + plan.title + '" (' + level + '): "' + pc.title + '" (' + (pc.focus || '') + '). Base the facts on the notes; do not invent facts or numbers. Plain words, short sentences, no copied passages. ' +
        'Include 5-6 lesson paragraphs, 4 quiz questions with 3-4 options each, 4 flashcards, 4-6 glossary terms, a concept map with 5-7 links, and three practice labs (fill, order, match).\n\nNotes:\n' + clip(notes, 8000) + '\n\nReply with JSON only. ' + SCHEMA;
      var ch = null, lastErr = '';
      for (var attempt = 0; attempt < 2 && !ch; attempt++) {
        var txt = await AI.complete([{ role: 'system', content: 'You write accurate, friendly course chapters as JSON.' }, { role: 'user', content: prompt + (lastErr ? '\n\nYour previous reply was invalid: ' + lastErr + '. Fix it.' : '') }], { temperature: 0.4, signal: sig });
        try { var cand = AI.extractJson(txt); AI.checkChapter(cand); ch = cand; } catch (e) { lastErr = e.message; log('Repairing chapter ' + (ci + 1) + ': ' + e.message); }
      }
      if (!ch) throw new Error('Chapter ' + (ci + 1) + ' could not be written: ' + lastErr);
      chapters.push(ch);
    }
    return AI.assembleCourse(plan, chapters, sources, level);
  };
  AI.checkChapter = function (c) {
    if (!c || typeof c !== 'object') throw new Error('not an object');
    if (!c.title) throw new Error('missing title');
    if (!Array.isArray(c.summary) || !c.summary.length) throw new Error('missing summary');
    if (!Array.isArray(c.lesson) || !c.lesson.length) throw new Error('missing lesson');
    if (!Array.isArray(c.quiz) || !c.quiz.length) throw new Error('missing quiz');
    c.quiz.forEach(function (q) { if (!q.q || !Array.isArray(q.options) || q.options.length < 2 || typeof q.answer !== 'number' || q.answer < 0 || q.answer >= q.options.length) throw new Error('a quiz question has no valid answer index'); });
  };
  AI.assembleCourse = function (plan, chapters, sources, level) {
    var out = chapters.map(function (c) {
      var ch = {}; for (var k in c) if (k !== 'feynman') ch[k] = c[k];
      ch.lesson = (c.lesson || []).map(function (b) { return typeof b === 'string' ? { type: 'text', items: [b] } : b; });
      var f = c.feynman; if (f && f.analogy) ch.lesson.unshift({ type: 'text', items: ['Explain it simply. ' + String(f.analogy).slice(0, 380), 'Teach it back. Explain this chapter out loud to a ten-year-old, with no jargon and no notes. If you cannot answer this, reread the lesson at that spot: ' + (f.stall || 'what is the main idea?')] });
      return ch;
    });
    if (sources.length) out.push({ title: 'Sources', summary: ['Where the facts in this course came from. Check them for yourself.'], keyPoints: ['Read the sources, because a summary can be wrong.'], lesson: [{ type: 'text', items: sources.slice(0, 30).map(function (s) { return s.title + ': ' + s.url; }) }],
      quiz: [{ q: 'Why check the sources?', options: ['A summary can contain mistakes', 'They are always perfect', 'They are decoration'], answer: 0, explain: 'AI-written courses can be wrong; the sources are how you verify.' }] });
    return { format: 'lilith-course', version: 1, id: AI.slug(plan.title) + '-ai', title: plan.title, subtitle: plan.subtitle || '', author: 'Lilith Learning Lab (AI-built)', description: (plan.description || '') + ' Built from web research; verify the facts with the Sources chapter.',
      category: plan.category || 'Other', level: level, tags: (plan.tags || []).concat(['ai-built']).slice(0, 8), chapters: out };
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = AI; else root.LilithAI = AI;
})(typeof window !== 'undefined' ? window : globalThis);
