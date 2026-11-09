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
def nd(*objs): return ''.join(json.dumps(o) + '\n' for o in objs)
def route(r):
    u = r.request.url; body = r.request.post_data or ''; seen.append(u.split('11434')[-1] if '11434' in u else u)
    H = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'}
    if r.request.method == 'OPTIONS': return r.fulfill(status=204, headers=H)
    if u.endswith('/api/tags'): return r.fulfill(status=200, headers=H, content_type='application/json', body=json.dumps({'models': [{'name': 'tutor:1b'}, {'name': 'clef'}]}))
    if u.endswith('/v1/systemone'): return r.fulfill(status=200, headers=H, content_type='application/json', body=json.dumps({'model': 'clef', 'answers': {'q': {'score': 2, 'confidence': 0.81}}}))
    if u.endswith('/api/chat'):
        j = json.loads(body); last = j['messages'][-1]
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
    # course builder
    pg.click('#libbtn'); pg.wait_for_selector('#bld'); pg.click('#bld'); pg.wait_for_selector('#bt'); pg.fill('#bt', 'Bees'); pg.select_option('#bn', '3'); pg.click('#bgo')
    pg.wait_for_function("document.body.innerText.includes('Tiny Topic')", timeout=20000); pg.wait_for_timeout(500)
    check(pg.evaluate("__app.ST.courses.some(c=>c.id==='tiny-topic-ai')"), 'built course imported')
    shot(pg, 'ai5_built')
    b.close()
print('errors', errors); print('FAILS', fails)
sys.exit(1 if fails or errors else 0)
