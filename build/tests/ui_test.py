#!/usr/bin/env python3
"""UI test in headless Chrome (mobile viewport). Usage: python3 tests/ui_test.py <web dir> <courses dir> [screenshot dir]"""
import sys, os, json, time
from playwright.sync_api import sync_playwright

web, courses = sys.argv[1], sys.argv[2]
shots = sys.argv[3] if len(sys.argv) > 3 else None
errors, fails = [], []
def check(c, m):
    if not c: fails.append(m); print('FAIL', m)
def shot(page, name):
    if shots: os.makedirs(shots, exist_ok=True); page.screenshot(path=os.path.join(shots, name + '.png'))

MOCK = """
(() => {
  const spoken = []; window.__spoken = spoken;
  class U { constructor(t){ this.text=t; } }
  const syn = { speaking:false, getVoices(){ return []; }, cancel(){ clearTimeout(this.t); },
    speak(u){ spoken.push(u.text); clearTimeout(this.t); setTimeout(()=>{ u.onstart&&u.onstart(); u.onboundary&&u.onboundary(); }, 5); this.t=setTimeout(()=>{ u.onend&&u.onend(); }, 40); } };
  Object.defineProperty(window, 'speechSynthesis', { value: syn, configurable: true });
  window.SpeechSynthesisUtterance = U;
})();
"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=2, has_touch=True, is_mobile=True)
    ctx.add_init_script(MOCK)
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.goto('file://' + os.path.join(web, 'index.html'))
    page.wait_for_selector('#main')

    # ---- empty state
    check('Your lab is empty' in page.inner_text('#main'), 'empty state shown')
    check(page.inner_text('h1') == 'Lilith Learning Lab', 'title')
    check(len(page.query_selector_all('svg.ic')) > 5, 'material icons rendered')
    check(not any(ord(ch) > 0x2000 and ord(ch) < 0x3000 and ch not in '·' for ch in page.inner_text('body')), 'no stray symbol glyphs in text')
    shot(page, '01_empty')

    # ---- import both courses through the file chooser
    with page.expect_file_chooser() as fc:
        page.click('#imp')
    fc.value.set_files([os.path.join(courses, 'sample-percentages.course.json'), os.path.join(courses, 'jetson-agx-xavier.course.json')])
    page.wait_for_selector('#modal[open]')
    time.sleep(0.6)
    txt = page.inner_text('#modal')
    check('Imported' in txt, 'import dialog: ' + txt[:80])
    shot(page, '02_imported')
    page.click('#ml'); page.wait_for_timeout(300)
    page.click('#libbtn'); page.wait_for_selector('#pst')
    check(len(page.query_selector_all('.crs')) == 2, 'two courses in library')

    # bad import
    page.click('#pst'); page.fill('#pj', '{"title":"x"}'); page.click('#pi')
    page.wait_for_selector('#modal[open]'); check('Could not import' in page.inner_text('#modal'), 'bad json rejected'); page.evaluate("document.getElementById('modal').close()")

    # ---- open the sample (small) course and run a full chapter
    page.click('[data-open="everyday-percentages"]')
    page.wait_for_selector('#lgo')
    check('Everyday Math' in page.inner_text('#sub'), 'header shows course')
    shot(page, '03_course_home')
    app = lambda js: page.evaluate(js)
    page.click('[data-lec="1"]')
    page.wait_for_selector('#slide')
    stages = app("__app.LEC.deck.slides.map(s=>s.stage)")
    order = [x for i, x in enumerate(stages) if i == 0 or stages[i-1] != x]
    check(order == ['title', 'map', 'summary', 'glossary', 'points', 'lesson', 'quiz', 'practice', 'end'], 'deck order: ' + str(order))
    quiz_seen = 0
    for _ in range(400):
        page.wait_for_timeout(100)
        t = app("(()=>{const L=__app.LEC;const c=L.deck.chunks[__app.NAR.state.i];return L.deck.slides[c.slide].type})()")
        if t == 'map' and 'm' not in globals(): shot(page, '04_map'); globals()['m'] = 1
        if t == 'quiz' and page.query_selector('.opt:not([disabled])'):
            if quiz_seen == 0: shot(page, '06_quiz')
            held = app('__app.NAR.state.held')
            check(held, 'narrator holds on the quiz question')
            page.click('.opt[data-k="1"]'); quiz_seen += 1; page.wait_for_timeout(300)
            if quiz_seen == 1: shot(page, '07_quiz_answered')
            page.wait_for_timeout(300)
        if t == 'practice': break
    check(quiz_seen == 3, 'answered 3 quiz questions: %d' % quiz_seen)
    page.wait_for_timeout(600)
    shot(page, '08_practice_slide')
    prog = app("JSON.parse(localStorage.getItem('lilith-lab-v1')).prog['everyday-percentages']")
    check(prog['q']['p1']['done'] and prog['q']['p1']['total'] == 3 and prog['q']['p1']['best'] == 2, 'quiz recorded 2/3: ' + json.dumps(prog['q']))
    check(all(prog['st']['p1'].get(k) for k in ['map', 'summary', 'glossary', 'points']), 'content stages marked: ' + json.dumps(prog['st']))
    # open a practice lab from the slide
    page.click('[data-lab="lab0"]'); page.wait_for_selector('#labbody'); shot(page, '09_lab_fill')
    ins = page.query_selector_all('.fillp input')
    ins[0].fill('hundred'); ins[1].fill('0.75'); page.click('#chk'); page.wait_for_timeout(200)
    check('ALL' in page.inner_text('#res').upper() or 'CORRECT' in page.inner_text('#res').upper(), 'fill lab passes: ' + page.inner_text('#res')[:60]); shot(page, '10_lab_fill_done')
    page.click('#lback'); page.wait_for_timeout(300)
    check(page.query_selector('#slide') is not None, 'back to lecture')
    # labs from the practice tab
    page.click('#nav [data-t="practice"]'); page.wait_for_selector('[data-lab]')
    check(len(page.query_selector_all('[data-lab]')) >= 7, 'labs listed')
    page.click('[data-lab="p1/lab1"]'); page.wait_for_selector('.matchr')
    sels = page.query_selector_all('.matchr select')
    for sl, v in zip(sels, ['1/2', '1/4', '1/10', '1']): sl.select_option(v)
    page.click('#chk'); check('PASS' in page.inner_text('#res').upper() and 'FAIL' not in page.inner_text('#res').upper(), 'match lab passes: ' + page.inner_text('#res')[:80])
    page.click('#lback'); page.click('[data-lab="p1/lab2"]'); page.wait_for_selector('.ordl')
    for t in ['Look at the percent, for example 35%', 'Drop the % sign', 'Divide by 100', 'Read the decimal: 0.35']:
        page.click('[data-p="%s"]' % t)
    page.click('#chk'); check('FAIL' not in page.inner_text('#res').upper(), 'order lab passes: ' + page.inner_text('#res')[:80]); shot(page, '11_lab_order')
    page.click('#lback'); page.click('[data-lab="p2/lab0"]'); page.wait_for_selector('#code')
    page.fill('#code', 'function percentOf(p, whole) { return p / 100 * whole; }'); page.click('#run'); page.wait_for_timeout(1200)
    check('FAIL' not in page.inner_text('#res').upper() and 'PASS' in page.inner_text('#res').upper(), 'code lab passes in worker: ' + page.inner_text('#res')[:100]); shot(page, '12_lab_code')
    page.fill('#code', 'function percentOf(p, whole) { while(true){} }'); page.click('#run'); page.wait_for_timeout(4000)
    check('longer' in page.inner_text('#res').lower() or 'time' in page.inner_text('#res').lower(), 'endless loop is stopped: ' + page.inner_text('#res')[:100])
    page.click('#lback'); page.click('[data-lab="p2/lab1"]'); page.wait_for_selector('#code'); page.fill('#code', '0.3 * 200 = 60'); page.click('#chk')
    check('FAIL' not in page.inner_text('#res').upper(), 'write lab passes: ' + page.inner_text('#res')[:100])
    page.click('#lback'); page.click('[data-lab="p2/lab3"]'); page.wait_for_selector('#tin')
    for c in ['calc 20 of 80', 'calc 10 of 350']:
        page.fill('#tin', c); page.press('#tin', 'Enter'); page.wait_for_timeout(100)
    check('16' in page.inner_text('#tout') and '35' in page.inner_text('#tout'), 'terminal output'); shot(page, '13_terminal')
    page.click('#lback'); page.click('[data-lab="p2/lab2"]'); page.wait_for_selector('iframe'); page.wait_for_timeout(600)
    fr = page.frame_locator('iframe')
    fr.locator('#s').evaluate("e=>{e.value=35;e.dispatchEvent(new Event('input'))}"); page.wait_for_timeout(600)
    shot(page, '14_webxdc')
    prog = app("JSON.parse(localStorage.getItem('lilith-lab-v1')).prog['everyday-percentages']")
    check(prog['lab'].get('p2/lab2'), 'webxdc lab completed via lilith.complete(): ' + json.dumps(prog['lab']))
    check(len((prog.get('xdc') or {}).get('p2/lab2', [])) >= 1, 'webxdc update stored: ' + json.dumps(prog.get('xdc'))[:80])
    page.click('#lback')
    # ---- final exam (built from all chapter quizzes here: 5 questions)
    page.click('#nav [data-t="lecture"]'); page.wait_for_timeout(300)
    if not page.query_selector('#exgo'): page.evaluate('__onBack()'); page.wait_for_timeout(300)
    page.wait_for_selector('#exgo'); shot(page, '15_home_exam')
    page.click('#exgo'); page.wait_for_selector('.opt')
    n = app('__app.EXAM.qs.length'); check(n == 5, 'exam has 5 questions: %d' % n)
    for i in range(n):
        ans = app('__app.EXAM.qs[__app.EXAM.i].answer')
        wrong = (ans + 1) % 2 if i == 0 else ans          # get exactly one wrong
        page.click('.opt[data-k="%d"]' % wrong)
        if i == 0: shot(page, '16_exam_q')
        page.click('#exnext')
    page.wait_for_selector('#exagain'); shot(page, '17_exam_result')
    rt = page.inner_text('#main'); check('4 of 5' in rt and 'Passed' in rt, 'exam result 4/5 passed: ' + rt[:120])
    prog = app("JSON.parse(localStorage.getItem('lilith-lab-v1')).prog['everyday-percentages']")
    check(prog['exam']['bestPct'] == 80 and prog['exam']['passed'] and prog['exam']['attempts'] == 1, 'exam saved: ' + json.dumps(prog.get('exam')))
    page.click('#exdone'); page.wait_for_selector('.pbar'); shot(page, '18_progress')
    check('final exam' in page.inner_text('#main').lower() and 'Best score 80%' in page.inner_text('#main'), 'progress shows exam')
    check('% complete' in page.inner_text('#sub'), 'progress in header: ' + page.inner_text('#sub'))

    # ---- Xavier course: lecture with narration, maps tab + tour, read, flashcards
    page.click('#libbtn'); page.click('[data-open="jetson-agx-xavier"]'); page.wait_for_selector('#lgo')
    shot(page, '16_xavier_home')
    page.click('[data-lec="10"]'); page.wait_for_selector('#slide'); page.wait_for_timeout(2500)
    spoken = app('window.__spoken'); check(len(spoken) >= 3, 'narration speaks: %d' % len(spoken))
    check(any('Concept map' in s or 'concept map' in s for s in spoken), 'tour narrated')
    shot(page, '17_xavier_lecture')
    page.click('#lback')
    page.click('#nav [data-t="maps"]'); page.wait_for_selector('.mapbox'); shot(page, '18_maps')
    page.click('#tour'); page.wait_for_selector('svg.mapsvg'); page.wait_for_timeout(2500); shot(page, '19_tour')
    check(app('__app.LEC.tour') is True, 'tour mode')
    page.click('#lback'); page.click('#nav [data-t="read"]'); page.click('[data-n="10"]'); page.wait_for_selector('h2'); shot(page, '20_read')
    page.click('#nav [data-t="practice"]'); page.wait_for_selector('[data-lab]')
    page.click('[data-lab="ch10/dla-explorer"]'); page.wait_for_selector('iframe.xframe'); page.wait_for_timeout(600); shot(page, '21_xavier_webxdc')
    fr = page.frame_locator('iframe.xframe'); fr.locator('#demo').click(); page.wait_for_timeout(300)
    check('GPU' in fr.locator('#stack').inner_text(), 'webxdc app packed in .xdc runs')
    page.click('#lback')
    page.click('[data-p="sandbox"]'); page.wait_for_selector('.term')
    page.fill('#tin', 'sudo nvpmodel -q'); page.press('#tin', 'Enter'); check('MAXN' in page.inner_text('.term'), 'sandbox terminal'); shot(page, '22_sandbox')
    page.click('[data-p="cards"]'); page.wait_for_selector('#show'); page.click('#show'); page.click('#got'); shot(page, '23_cards')
    page.click('[data-p="gloss"]'); page.fill('#gq', 'DLA'); check(len(page.query_selector_all('#gl dt')) >= 1, 'glossary search')

    # ---- persistence across reload
    page.reload(); page.wait_for_selector('#lgo')
    check('Jetson' in page.inner_text('#sub'), 'current course restored after reload')
    page.click('#libbtn'); page.wait_for_selector('.crs')
    check(len(page.query_selector_all('.crs')) == 2, 'courses survive reload')
    # ---- delete
    page.click('[data-del="everyday-percentages"]'); page.wait_for_selector('#myes'); page.click('#myes'); page.wait_for_timeout(300)
    check(len(page.query_selector_all('.crs')) == 1, 'course deleted')
    gone = app("localStorage.getItem('lilith-course:everyday-percentages')"); check(gone is None, 'course data removed from storage')
    page.click('[data-del="jetson-agx-xavier"]'); page.click('#myes'); page.wait_for_timeout(300)
    check('Your lab is empty' in page.inner_text('#main'), 'back to empty state after deleting all'); shot(page, '24_empty_again')
    b.close()

errors = [e for e in errors if 'favicon' not in e]
print('PAGE ERRORS:', errors)
print('FAILS:', fails)
sys.exit(1 if (errors or fails) else 0)
