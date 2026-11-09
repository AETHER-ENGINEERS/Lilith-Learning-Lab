#!/usr/bin/env python3
"""UI test for office hours, AI settings, graded teach-backs and the course builder, with mocked Ollama endpoints.
Usage: python3 tests/ai_ui_test.py <web dir> <courses dir> [screenshot dir]"""
import sys, os, json
from playwright.sync_api import sync_playwright
web, courses = sys.argv[1], sys.argv[2]; shots = sys.argv[3] if len(sys.argv) > 3 else None
fails, errors, seen = [], [], []
def check(c, m):
    if not c: fails.append(m); print('FAIL', m)
def shot(p, n):
    if shots: os.makedirs(shots, exist_ok=True); p.screenshot(path=os.path.join(shots, n + '.png'))
MOCK = """(()=>{const syn={speaking:false,getVoices(){return[]},cancel(){},speak(u){setTimeout(()=>{u.onend&&u.onend()},20)}};
Object.defineProperty(window,'speechSynthesis',{value:syn,configurable:true});window.SpeechSynthesisUtterance=class{constructor(t){this.text=t}};})();"""
def open_lib(pg):
    if pg.locator('#bld').count() and pg.locator('#bld').is_visible(): return
    pg.click('#libbtn'); pg.wait_for_timeout(300)
    if not (pg.locator('#bld').count() and pg.locator('#bld').is_visible()): pg.click('#libbtn')
    pg.wait_for_selector('#bld')
def nd(*objs): return ''.join(json.dumps(o) + '\n' for o in objs)
def route(r):
    u = r.request.url; body = r.request.post_data or ''; seen.append(u.split('11434')[-1] if '11434' in u else u)
    H = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'}
    if r.request.method == 'OPTIONS': return r.fulfill(status=204, headers=H)
    if u.endswith('/api/tags'): return r.fulfill(status=200, headers=H, content_type='application/json', body=json.dumps({'models': [{'name': 'tutor:1b', 'capabilities': ['completion', 'tools']}, {'name': 'clef', 'capabilities': ['decision']}]}))
    if u.endswith('/v1/systemone'): return r.fulfill(status=200, headers=H, content_type='application/json', body=json.dumps({'model': 'clef', 'answers': {'q': {'score': 2, 'confidence': 0.81}}}))
    if u.endswith('/api/chat'):
        j = json.loads(body); last = j['messages'][-1]
        tools = [t['function']['name'] for t in (j.get('tools') or [])]
        if 'deep_research' in tools and ('bees dance' in last.get('content', '') or last['role'] == 'tool'):
            if last['role'] == 'tool': return r.fulfill(status=200, headers=H, content_type='application/x-ndjson', body=nd({'message': {'content': 'From my research: ' + last['content'][:400]}}, {'done': True}))
            return r.fulfill(status=200, headers=H, content_type='application/x-ndjson', body=nd(call('deep_research', {'question': 'Why do honey bees dance?'}), {'done': True}))
        if 'finish_course' in tools or ('skill' in tools and 'check_chapter' not in tools and 'deep_research' not in tools):
            agent_log.append(len(j['messages']))
            return r.fulfill(status=200, headers=H, content_type='application/x-ndjson', body=nd(agent_step(j, tools), {'done': True}))
        if j['messages'][0]['role'] == 'system' and 'Design a' in last.get('content', ''): pass
        if 'Design a' in last['content']:
            plan = {'title': 'Tiny Topic', 'subtitle': 's', 'description': 'd', 'category': 'Science', 'tags': ['t'], 'chapters': [{'title': 'One', 'focus': 'f', 'queries': ['q']}]}
            return r.fulfill(status=200, headers=H, content_type='application/x-ndjson', body=nd({'message': {'content': json.dumps(plan)}}, {'done': True}))
        if 'Write chapter' in last['content']:
            ch = {'title': 'One', 'summary': ['A summary.'], 'lesson': [{'type': 'text', 'items': ['Some lesson text.']}], 'quiz': [{'q': 'Q?', 'options': ['a', 'b'], 'answer': 1, 'explain': 'e'}], 'feynman': {'analogy': 'like a bee', 'stall': 'why?'}}
            return r.fulfill(status=200, headers=H, content_type='application/x-ndjson', body=nd({'message': {'content': json.dumps(ch)}}, {'done': True}))
        return r.fulfill(status=200, headers=H, content_type='application/x-ndjson', body=nd({'message': {'content': 'Think of it '}}, {'message': {'content': 'like a pizza.'}}, {'done': True}))
    if 'wikipedia' in u: return r.fulfill(status=200, headers=H, content_type='application/json', body=json.dumps({'query': {'search': [{'title': 'Bee', 'snippet': 'insect'}]}}))
    if 'r.jina.ai' in u: return r.fulfill(status=200, headers=H, content_type='text/plain', body='Bees make honey.')
    r.fulfill(status=404, headers=H, body='nf')
agent_log = []
CH_BAD = {'title': 'Bees', 'summary': ['Bees make honey.'], 'lesson': [{'type': 'text', 'items': ['Bees live in hives.']}], 'quiz': [{'q': 'What do bees make?', 'options': ['honey', 'milk'], 'answer': 9, 'explain': 'Honey.'}],
          'feynman': {'analogy': 'A hive is like a busy kitchen.', 'stall': 'Why do bees visit flowers?'}}
def call(name, args): return {'message': {'content': '', 'tool_calls': [{'function': {'name': name, 'arguments': args}}]}}
def agent_step(j, tools):
    msgs = j['messages']; done = [m for m in msgs if m['role'] == 'assistant' and m.get('tool_calls')]
    user = next(m['content'] for m in msgs if m['role'] == 'user')
    if 'Ants' in user:   # an agent that never uses its tools: the builder must fall back
        return {'message': {'content': 'I would write a course about ants.'}}
    if 'finish_course' in tools:
        d = '/build/bees'
        script = [('skill', {'name': 'course-builder'}), ('web_search', {'query': 'bees'}), ('web_fetch', {'url': 'https://en.wikipedia.org/wiki/Bee'}),
                  ('write', {'path': d + '/plan.json', 'content': json.dumps({'title': 'Busy Bees', 'subtitle': 'Hives', 'description': 'About bees.', 'category': 'Science', 'tags': ['bees'], 'chapters': [{'title': 'Bees', 'focus': 'basics'}]})}),
                  ('write', {'path': d + '/ch01.json', 'content': json.dumps(CH_BAD)}), ('check_chapter', {'path': d + '/ch01.json'}),
                  ('edit', {'path': d + '/ch01.json', 'oldText': '"answer": 9', 'newText': '"answer": 0'}), ('check_chapter', {'path': d + '/ch01.json'}),
                  ('finish_course', {'dir': d})]
        if len(done) < len(script): return call(*script[len(done)])
        return {'message': {'content': 'Busy Bees, 1 chapter.'}}
    script = [('skill', {'name': 'deep-research'}), ('web_search', {'query': 'why bees dance'}), ('web_fetch', {'url': 'https://en.wikipedia.org/wiki/Waggle_dance'}),
              ('write', {'path': '/research/why-do-bees-dance/notes.md', 'content': '- the waggle dance shows direction (https://en.wikipedia.org/wiki/Waggle_dance)'})]
    if len(done) < len(script): return call(*script[len(done)])
    return {'message': {'content': 'Bees dance to show other bees where food is: the angle points the way.'}}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=2, has_touch=True, is_mobile=True)
    ctx.add_init_script(MOCK); ctx.route('**/*', lambda r: route(r) if r.request.url.startswith('http') else r.continue_())
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto('file://' + os.path.abspath(web) + '/index.html'); pg.wait_for_selector('#main')
    with pg.expect_file_chooser() as fc: pg.click('#imp')
    fc.value.set_files([os.path.join(courses, 'sample-percentages.course.json')])
    pg.wait_for_selector('#modal[open]'); pg.wait_for_timeout(600); pg.click('#ml'); pg.wait_for_timeout(300)
    pg.click('#libbtn'); pg.wait_for_selector('.crs')
    pg.click('[data-open="everyday-percentages"]'); pg.wait_for_selector('#lgo')
    # office tab without AI shows the setup card
    pg.click('#nav [data-t="ask"]'); pg.wait_for_selector('#ofset'); check('Set up AI' in pg.inner_text('#main'), 'setup card without AI')
    # AI settings: scan and save
    pg.click('#ofset'); pg.wait_for_selector('#aiscan'); pg.fill('#aiurl', 'http://localhost:11434'); pg.click('#aiscan'); pg.wait_for_selector('#aires:not(.hide)'); pg.wait_for_timeout(500)
    check('tutor:1b' in pg.inner_text('#aires'), 'scan lists models: ' + pg.inner_text('#aires'))
    check('1 chat model' in pg.inner_text('#aires') and '1 decision model(s): clef' in pg.inner_text('#aires'), 'chat and decision models are told apart: ' + pg.inner_text('#aires'))
    shot(pg, 'ai1_settings')
    pg.click('#aitest'); pg.wait_for_timeout(800); check('Model says' in pg.inner_text('#aires'), 'test works')
    pg.fill('#aidm', 'clef'); pg.click('#aiok'); pg.wait_for_timeout(400)
    # course-wide office hours
    pg.click('#nav [data-t="ask"]'); pg.wait_for_selector('#ofq')
    pg.fill('#ofq', 'What is a percent?'); pg.click('#ofsend'); pg.wait_for_function("document.querySelectorAll('.ob.a').length>=2 && document.body.innerText.includes('like a pizza')", timeout=8000)
    check('like a pizza' in pg.inner_text('#ofm'), 'streamed answer shown'); shot(pg, 'ai2_office_course')
    # teach-back graded by the decisions API
    pg.click('[data-c="3"]'); pg.fill('#ofq', 'A percent is a part out of one hundred.'); pg.click('#ofsend'); pg.wait_for_function("document.body.innerText.includes('Teach-back check')", timeout=8000)
    check('Mostly right' in pg.inner_text('#ofm') and '81%' in pg.inner_text('#ofm'), 'decision verdict shown: ' + pg.inner_text('#ofm')[-200:])
    check(any('systemone' in s for s in seen), 'systemone called'); shot(pg, 'ai3_teachback')
    # persisted thread
    pg.click('#nav [data-t="read"]'); pg.click('#nav [data-t="ask"]'); pg.wait_for_selector('#ofq')
    check(pg.locator('.ob.u').count() >= 2, 'thread persisted')
    # lab office hours
    pg.click('#nav [data-t="practice"]'); pg.wait_for_selector('[data-lab]'); pg.click('[data-lab]'); pg.wait_for_selector('#asklab'); pg.click('#asklab'); pg.wait_for_selector('#office[open] #ofq')
    check('lab' in pg.inner_text('#office').lower(), 'lab scope label'); pg.fill('#ofq', 'Give me a hint'); pg.click('#ofsend'); pg.wait_for_function("document.querySelector('#office').innerText.includes('like a pizza')", timeout=8000); shot(pg, 'ai4_lab_office')
    pg.evaluate("document.getElementById('office').close()")
    # lecture: office hours pause after each section
    pg.click('#nav [data-t="lecture"]'); pg.wait_for_selector('[data-lec]'); pg.click('[data-lec="1"]'); pg.wait_for_selector('#slide')
    n = pg.evaluate("__app.LEC.deck.slides.filter(s=>s.type==='office').length"); check(n >= 3, 'office slides in the lecture: %d' % n)
    # Teacher decides to research a question in depth, in the background
    pg.click('#nav [data-t="ask"]'); pg.wait_for_selector('#ofq'); check(pg.locator('#ofres').count() == 0, 'no research button for the learner')
    pg.fill('#ofq', 'Why do bees dance?'); pg.click('#ofsend')
    pg.wait_for_function("document.querySelector('#ofm').innerText.includes('From my research')", timeout=20000)
    t = pg.inner_text('#ofm'); check('angle points the way' in t and 'Waggle_dance' in t, 'research answer has sources: ' + t[-300:])
    check('notes.md' not in t and 'skill' not in t, 'workspace details stay hidden'); shot(pg, 'ai6_research')
    check(pg.evaluate("LilithAI.workspace().then(k=>k.vfs.read('/research/why-do-bees-dance/notes.md'))").startswith('- the waggle'), 'research notes in the workspace')
    # course builder: the agent researches, writes, fails a check, fixes it and finishes
    open_lib(pg); pg.click('#bld'); pg.wait_for_selector('#bt'); pg.fill('#bt', 'Bees'); pg.select_option('#bn', '3')
    texts = []
    pg.expose_function('__seen', lambda t: texts.append(t))
    pg.evaluate("new MutationObserver(()=>{const e=document.getElementById('bptxt'); if(e) window.__seen(e.textContent)}).observe(document.getElementById('modal'),{subtree:true,childList:true,characterData:true})")
    pg.click('#bgo')
    pg.wait_for_function("__app.ST.courses.some(c=>c.id==='busy-bees-ai')", timeout=30000); pg.wait_for_timeout(500)
    print('progress lines:', sorted(set(texts)))
    check(any('Researching the topic' in t for t in texts) and any('Writing chapter 1 of 3' in t for t in texts), 'plain progress shown: %s' % sorted(set(texts)))
    check(not any(('http' in t or '.json' in t or 'Searching' in t) for t in texts), 'no background details shown')
    check(pg.evaluate("LilithAI.workspace().then(k=>k.vfs.exists('/build/bees/research.md'))"), 'background research saved for the builder')
    c = pg.evaluate("__app.readCourse('busy-bees-ai')")
    check(c and c['chapters'][0]['quiz'][0]['answer'] == 0 and c['chapters'][-1]['title'] == 'Sources' and 'wiki/Bee' in json.dumps(c['chapters'][-1]), 'agent-built course: fixed and sourced')
    check(not any('Design a' in str(x) for x in seen), 'agent builder did not need the fallback')
    check('wiki/Waggle_dance' in json.dumps(c['chapters'][-1]), 'sources from the background research are in the course')
    shot(pg, 'ai5_built')
    pg.evaluate("document.getElementById('modal').open && document.getElementById('modal').close()")
    # an agent that does not use its tools: fall back to the step-by-step builder
    open_lib(pg); pg.click('#bld'); pg.wait_for_selector('#bt'); pg.fill('#bt', 'Ants'); pg.select_option('#bn', '3'); pg.click('#bgo')
    pg.wait_for_function("__app.ST.courses.some(c=>c.id==='tiny-topic-ai')", timeout=30000)
    check('Switching to the step-by-step builder' in pg.evaluate("LilithAI.logText()") or 'step-by-step' in pg.evaluate("LilithAI.logText()"), 'fallback logged')
    pg.wait_for_timeout(500); pg.evaluate("document.getElementById('modal').open && document.getElementById('modal').close()")
    # settings export and import
    pg.click('#gear'); pg.wait_for_selector('#sexp'); pg.click('#sexp'); pg.wait_for_selector('#exk')
    with pg.expect_download() as dl: pg.click('#exs')
    exp = json.loads(open(dl.value.path()).read())
    check(exp['format'] == 'lilith-settings' and exp['ai']['provider'] == 'ollama' and 'cloudKey' not in exp['ai'] and exp['ai']['decideModel'] == 'clef', 'export without keys: %s' % exp)
    pg.evaluate("LilithAI.setCfg({cloudKey:'secret-123'})")
    pg.click('#gear'); pg.wait_for_selector('#sexp'); pg.click('#sexp'); pg.wait_for_selector('#exk'); pg.click('#exk')
    with pg.expect_download() as dl: pg.click('#exs')
    check(json.loads(open(dl.value.path()).read())['ai'].get('cloudKey') == 'secret-123', 'export with keys')
    pg.click('#gear'); pg.wait_for_selector('#simp'); pg.click('#simp'); pg.wait_for_selector('#imt')
    pg.fill('#imt', '{"format":"lilith-course"}'); pg.click('#imo'); pg.wait_for_timeout(200); check('not a settings file' in pg.inner_text('#imr'), 'course refused as settings')
    pg.fill('#imt', '{"format":"lilith-settings","version":1,"ai":{"provider":"bogus"}}'); pg.click('#imo'); pg.wait_for_timeout(200); check('unknown provider' in pg.inner_text('#imr'), 'bad provider refused')
    pg.fill('#imt', 'not json'); pg.click('#imo'); pg.wait_for_timeout(200); check('Not valid JSON' in pg.inner_text('#imr'), 'bad json refused')
    imp = {'format': 'lilith-settings', 'version': 1, 'app': {'set': {'rate': 1.5, 'captions': False, 'evil': 'x'}, 'repo': 'someone/courses'}, 'ai': {'provider': 'openai', 'openaiUrl': 'https://api.example.com/v1', 'openaiModel': 'm1', 'verbose': True, 'junk': 1}}
    pg.fill('#imt', json.dumps(imp)); pg.click('#imo'); pg.wait_for_timeout(300)
    st = pg.evaluate("({set: __app.ST.set, repo: __app.ST.repo, ai: LilithAI.cfg()})")
    check(st['set']['rate'] == 1.5 and st['set']['captions'] is False and 'evil' not in st['set'] and st['repo'] == 'someone/courses', 'app settings imported: %s' % st['set'])
    check(st['ai']['provider'] == 'openai' and st['ai']['openaiModel'] == 'm1' and st['ai']['verbose'] is True and 'junk' not in st['ai'] and st['ai']['cloudKey'] == 'secret-123', 'AI settings imported: %s' % st['ai'])
    # the log viewer shows activity and hides keys
    pg.click('#gear'); pg.wait_for_selector('#aiset'); pg.click('#aiset'); pg.wait_for_selector('#ailog'); pg.click('#ailog'); pg.wait_for_selector('#lgv')
    lt = pg.inner_text('#lgv'); check('Model scan' in lt or 'Found' in lt, 'log shows the scan'); check('secret-123' not in pg.evaluate("LilithAI.logText()"), 'keys hidden in log'); shot(pg, 'ai7_log')
    pg.click('#lgx')
    # browsing courses scrolls even after a lecture was open
    open_lib(pg); pg.wait_for_selector('[data-open="everyday-percentages"]'); pg.click('[data-open="everyday-percentages"]'); pg.wait_for_selector('#lgo')
    pg.click('#nav [data-t="lecture"]'); pg.wait_for_selector('[data-lec]'); pg.click('[data-lec="1"]'); pg.wait_for_selector('#slide')
    open_lib(pg); pg.click('#brw'); pg.wait_for_timeout(300)
    check(not pg.evaluate("document.getElementById('main').classList.contains('fill')"), 'Browse online scrolls after a lecture was open')
    b.close()
print('errors', errors); print('FAILS', fails)
sys.exit(1 if fails or errors else 0)
