// Tests for src/ai.js against local mock servers (Ollama, OpenAI-compatible, decisions, search). Run: node tests/test_ai.js
const http = require('http'), assert = require('assert');
const mem = {}; global.localStorage = { getItem: k => mem[k] || null, setItem: (k, v) => { mem[k] = v; } };
const AI = require('../src/ai.js');
let log = [];
const server = http.createServer((req, res) => {
  let b = ''; req.on('data', d => b += d); req.on('end', () => {
    const j = b ? JSON.parse(b) : {}; log.push(req.method + ' ' + req.url);
    if (req.url === '/api/tags') return res.end(JSON.stringify({ models: [{ name: 'tutor:1b' }, { name: 'clef' }] }));
    if (req.url === '/models') return res.end(JSON.stringify({ data: [{ id: 'gpt-x' }] }));
    if (req.url === '/api/chat') {
      const last = j.messages[j.messages.length - 1];
      res.setHeader('Content-Type', 'application/x-ndjson');
      if (last.role === 'user' && /search/.test(last.content) && j.tools) return res.end(JSON.stringify({ message: { role: 'assistant', content: '', tool_calls: [{ function: { name: 'search_course', arguments: { query: 'dogs bark' } } }] } }) + '\n' + JSON.stringify({ done: true }) + '\n');
      if (last.role === 'tool') return res.end(JSON.stringify({ message: { content: 'Dogs ' } }) + '\n' + JSON.stringify({ message: { content: 'bark. ' + last.content.slice(0, 5) } }) + '\n' + JSON.stringify({ done: true }) + '\n');
      return res.end(JSON.stringify({ message: { content: 'hello' } }) + '\n' + JSON.stringify({ done: true }) + '\n');
    }
    if (req.url === '/chat/completions') {
      res.setHeader('Content-Type', 'text/event-stream');
      return res.end('data: ' + JSON.stringify({ choices: [{ delta: { content: 'he' } }] }) + '\n\ndata: ' + JSON.stringify({ choices: [{ delta: { content: 'llo ' + (j.messages[0].role) } }] }) + '\n\ndata: [DONE]\n\n');
    }
    if (req.url === '/v1/systemone') {
      const q = j.questions.q; assert(q.type === 'noul' || q.type === 'score' || q.type === 'choice');
      return res.end(JSON.stringify({ model: j.model, answers: { q: q.type === 'noul' ? { noul: 0.9 } : q.type === 'score' ? { score: 3, confidence: 0.7 } : { choice: Object.keys(q.criteria)[1], confidence: 0.6 } } }));
    }
    res.statusCode = 404; res.end('{}');
  });
});
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r)); const base = 'http://127.0.0.1:' + server.address().port;
  AI.setCfg({ provider: 'ollama', ollamaUrl: base, ollamaModel: 'tutor:1b', decideModel: 'clef' });
  assert.deepStrictEqual(await AI.listModels(), ['clef', 'tutor:1b']);
  assert(AI.enabled());
  let streamed = ''; assert.strictEqual(await AI.complete([{ role: 'user', content: 'hi' }], { onDelta: d => streamed += d }), 'hello'); assert.strictEqual(streamed, 'hello');
  // tool loop through search_course
  const courseIndex = AI.indexCourses([{ id: 'c', title: 'Pets', chapters: [{ title: 'Dogs', summary: ['dogs bark at the mail carrier'] }, { title: 'Cats', summary: ['cats purr'] }] }]);
  const tools = []; const ans = await AI.agent([{ role: 'user', content: 'please search the course' }], { tools: ['search_course'], courseIndex, onTool: n => tools.push(n) });
  assert.deepStrictEqual(tools, ['search_course']); assert(/^Dogs bark\. 1\. P/.test(ans), ans);
  // decisions
  assert.deepStrictEqual((await AI.decide({ type: 'yesno', question: 'Is it right?', state: 'x' })).answer, true);
  const sc = await AI.decide({ type: 'score', question: 'How good?', options: ['bad', 'ok', 'good', 'great'], state: 'x' }); assert.strictEqual(sc.answer, 3); assert.strictEqual(sc.confidence, 0.7);
  assert.strictEqual((await AI.decide({ type: 'choice', question: 'Which?', options: ['a', 'b'], state: 'x' })).answer, 'b');
  // openai-compatible
  AI.setCfg({ provider: 'openai', openaiUrl: base, openaiModel: 'gpt-x' });
  assert.deepStrictEqual(await AI.listModels(), ['gpt-x']);
  assert.strictEqual(await AI.complete([{ role: 'system', content: 's' }, { role: 'user', content: 'hi' }]), 'hello system');
  // decide falls back to the chat model on openai (answer parse)
  // course builder with mocked search/fetch and chat
  AI.setCfg({ provider: 'ollama' });
  const realChat = AI.complete; let n = 0;
  AI.webSearch = async q => [{ title: 'Page ' + q, url: 'https://ex.org/' + encodeURIComponent(q), snippet: 'snip' }]; AI.webFetch = async u => 'Facts from ' + u;
  AI.complete = async (m) => {
    n++; const u = m[m.length - 1].content;
    if (/Design a/.test(u)) return '```json\n' + JSON.stringify({ title: 'Bees', subtitle: 's', description: 'd', category: 'Science', tags: ['bees'], chapters: [{ title: 'Hive', focus: 'f', queries: ['hive'] }, { title: 'Honey', focus: 'f' }] }) + '\n```';
    if (/previous reply was invalid/.test(u)) return JSON.stringify({ title: 'Honey', summary: ['s'], lesson: [{ type: 'text', items: ['x'] }], quiz: [{ q: 'q', options: ['a', 'b'], answer: 1, explain: 'e' }], feynman: { analogy: 'a', stall: 'why?' } });
    if (/chapter 2/.test(u)) return '{"title":"Honey","summary":["s"],"lesson":["x"],"quiz":[{"q":"q","options":["a","b"],"answer":5}]}';
    return JSON.stringify({ title: 'Hive', summary: ['s'], lesson: [{ type: 'text', items: ['x'] }], quiz: [{ q: 'q', options: ['a', 'b'], answer: 0, explain: 'e' }], feynman: { analogy: 'bees live in a city', stall: 'what does a hive do?' } });
  };
  const logs = []; const course = await AI.buildCourse({ topic: 'Bees', chapters: 2, onLog: m => logs.push(m) });
  assert.strictEqual(course.chapters.length, 3); assert.strictEqual(course.chapters[2].title, 'Sources');
  assert(course.chapters[0].lesson[0].items[0].startsWith('Explain it simply.')); assert(logs.some(l => /Repairing/.test(l)));
  const K = require('../src/course.js'); const v = K.validate(JSON.stringify(course)); assert(v.ok, JSON.stringify(v.errors));
  AI.complete = realChat; server.close(); console.log('AI TESTS PASSED');
})().catch(e => { console.error(e); process.exit(1); });
