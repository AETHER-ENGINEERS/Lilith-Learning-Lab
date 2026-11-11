"""The AI's hidden workspace (Jade Agent Kit inside the app): starts offline, runs the shell, Python and the file tools,
checks chapters and assembles a course; and the Android native HTTP bridge (mocked) streams responses.
Usage: python3 tests/workspace_test.py <web dir>   (runs over http and over file://)"""
import sys, os, json, threading, http.server, functools
from playwright.sync_api import sync_playwright

web = os.path.abspath(sys.argv[1])
FAILS = []
def check(name, cond, info=''):
    print(('ok   ' if cond else 'FAIL ') + name + ('' if cond else '  ' + str(info)[:400]))
    if not cond: FAILS.append(name)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=web))
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

CH = {"title": "Tiny", "summary": ["One."], "lesson": [{"type": "text", "items": ["Para."]}, {"type": "table", "title": "T", "head": ["A", "B"], "rows": [["1", "2"], ["3", "4"]]}], "references": [{"title": "R", "url": "https://example.com"}], "quiz": [{"q": "Q?", "options": ["a", "b"], "answer": 0, "explain": "e"}],
      "practice": [{"type": "fill", "title": "F", "text": "The {{word}}."}]}
JS = """async (ch) => {
  const A = window.LilithAI, out = {};
  const t0 = Date.now(); await A.workspace(); out.startMs = Date.now() - t0;
  out.bash = await A.runTool('bash', { command: 'mkdir -p /tmp && echo hello world | tr a-z A-Z > /tmp/x.txt && cat /tmp/x.txt' });
  out.python = await A.runTool('python', { code: 'import math\\nprint(round(math.sqrt(2), 3))' });
  out.write = await A.runTool('write', { path: '/build/t/plan.json', content: JSON.stringify({ title: 'Tiny course', tags: ['x'] }) });
  await A.runTool('write', { path: '/build/t/ch01.json', content: JSON.stringify(ch) });
  await A.runTool('write', { path: '/build/t/ch02.json', content: '{"title": "Broken", "quiz": [{"q":"?","options":["a","b"],"answer":5}]}' });
  out.bad = await A.runTool('check_chapter', { path: '/build/t/ch02.json' });
  out.good = await A.runTool('check_chapter', { path: '/build/t/ch01.json' });
  const ctx = { sources: [{ url: 'https://example.org/a', title: 'A' }] };
  out.finishBad = await A.runTool('finish_course', { dir: '/build/t' }, ctx);
  await A.runTool('edit', { path: '/build/t/ch02.json', oldText: '"answer":5', newText: '"answer":1' });
  out.stillBad = await A.runTool('check_chapter', { path: '/build/t/ch02.json' });
  await A.runTool('write', { path: '/build/t/ch02.json', content: JSON.stringify(Object.assign({}, ch, { title: 'Second' })) });
  out.finish = await A.runTool('finish_course', { dir: '/build/t' }, ctx);
  out.course = ctx.result;
  await A.runTool('write', { path: '/research/n/notes.md', content: '- chlorophyll absorbs red and blue light (https://example.org)' });
  out.search = await A.runTool('search_files', { query: 'chlorophyll light', path: '/' });
  out.skill = await A.runTool('skill', { name: 'course-builder' });
  out.noskill = await A.runTool('skill', { name: 'nope' });
  out.unknown = await A.runTool('nope', {});
  out.tasks = await A.runTool('tasks', { action: 'add', titles: ['one', 'two'] });
  out.logs = A.logs().length;
  return out;
}"""
NATIVE = """async () => {
  // a fake Android bridge: answers with a streamed NDJSON body in three chunks
  const calls = [];
  window.AndroidTTS = { httpStart: (id, m, u, h, b) => { calls.push({ id, m, u, h: JSON.parse(h), b });
      setTimeout(() => {
        if (u.includes('/fail')) { window.__httpEv(id, 'x', 'Unable to resolve host', ''); return; }
        window.__httpEv(id, 'h', '200', JSON.stringify({ 'content-type': 'application/x-ndjson' }));
        const parts = ['{"message":{"content":"Hel"}}\\n', '{"message":{"content":"lo"}}\\n{"done":true}', '\\n'];
        parts.forEach((p, i) => setTimeout(() => window.__httpEv(id, 'd', btoa(p), ''), 5 * (i + 1)));
        setTimeout(() => window.__httpEv(id, 'e', '', ''), 40);
      }, 5); }, httpAbort: () => {} };
  localStorage.setItem('lilith.ai', JSON.stringify({ provider: 'cloud', cloudKey: 'k123', cloudModel: 'gpt-oss:120b' }));
  const A = window.LilithAI; let streamed = '';
  const r = await A.chat([{ role: 'user', content: 'hi' }], { onDelta: d => streamed += d });
  let err = ''; try { await fetch('https://ollama.com/fail'); } catch (e) { err = e.message; }
  let err2 = ''; try { localStorage.setItem('lilith.ai', JSON.stringify({ provider: 'ollama', ollamaUrl: 'https://x.example/fail', ollamaModel: 'm' })); await A.listModels(); } catch (e) { err2 = e.message; }
  delete window.AndroidTTS;
  return { content: r.content, streamed, call: calls[0], err, err2 };
}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'] if False else ['--no-sandbox'])
    for label, url in (('http', 'http://127.0.0.1:%d/index.html' % port), ('file', 'file://' + web + '/index.html')):
        pg = b.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(url); pg.wait_for_timeout(600)
        try:
            o = pg.evaluate(JS, CH)
        except Exception as e:
            check(label + ': workspace runs', False, e); continue
        print('   (%s) workspace started in %d ms' % (label, o['startMs']))
        check(label + ': shell (BusyBox)', 'HELLO WORLD' in o['bash'], o['bash'])
        check(label + ': python', o['python'].strip() == '1.414', o['python'])
        check(label + ': write', o['write'].startswith('Created'), o['write'])
        check(label + ': check_chapter finds problems', 'Problems' in o['bad'] and 'answer' in o['bad'] and 'summary' in o['bad'], o['bad'])
        check(label + ': check_chapter passes a good chapter', o['good'].startswith('OK'), o['good'])
        check(label + ': finish_course refuses broken chapters', o['finishBad'].startswith('Error') and 'ch02.json' in o['finishBad'], o['finishBad'])
        check(label + ': edit + recheck', 'Problems' in o['stillBad'] and 'answer' not in o['stillBad'], o['stillBad'])
        c = o['course'] or {}
        check(label + ': course assembled', o['finish'].startswith('Done') and c.get('format') == 'lilith-course' and len(c.get('chapters', [])) == 3 and c['chapters'][-1]['title'] == 'Sources' and 'ai-built' in c.get('tags', []), o['finish'])
        check(label + ': search_files (BM25)', '/research/n/notes.md' in o['search'], o['search'])
        check(label + ': skill', 'finish_course' in o['skill'] and o['noskill'].startswith('Error'), o['noskill'])
        check(label + ': unknown tool is an error, not a crash', o['unknown'].startswith('Error'))
        check(label + ': tasks', '#1' in o['tasks'] and 'two' in o['tasks'], o['tasks'])
        check(label + ': tools are logged', o['logs'] > 3, o['logs'])
        n = pg.evaluate(NATIVE)
        check(label + ': native bridge streams a chat', n['content'] == 'Hello' and n['streamed'] == 'Hello', n)
        check(label + ': native bridge gets method, url, auth, body', n['call']['m'] == 'POST' and n['call']['u'] == 'https://ollama.com/api/chat' and n['call']['h'].get('Authorization') == 'Bearer k123' and '"stream":true' in n['call']['b'], n['call'])
        check(label + ': native network error is reported', 'Unable to resolve host' in n['err'], n['err'])
        check(label + ': scan error is explained', 'Unable to resolve host' in n['err2'], n['err2'])
        check(label + ': no page errors', not errs, errs)
        pg.close()
    b.close()
srv.shutdown()
print('FAILS', FAILS)
sys.exit(1 if FAILS else 0)
