"""Course editor (docs/editor): write a course from scratch, check it with the app's validator, undo, autosave,
download, open real courses without losing anything, open from the library, and hand a course to the web app.
Usage: python3 tests/editor_test.py <courses dir> [screenshot dir]"""
import sys, os, json, shutil, subprocess, threading, http.server, functools, tempfile
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); courses = os.path.abspath(sys.argv[1]); shots = sys.argv[2] if len(sys.argv) > 2 else None
site = tempfile.mkdtemp()
subprocess.check_call([sys.executable, os.path.join(HERE, '..', 'build_web.py'), '--web', os.path.join(site, 'app')], stdout=subprocess.DEVNULL)
subprocess.check_call([sys.executable, os.path.join(HERE, '..', 'build_web.py'), '--editor', os.path.join(site, 'editor')], stdout=subprocess.DEVNULL)
shutil.copy(os.path.join(courses, 'catalog.json'), os.path.join(site, 'catalog.json'))
FAILS, errs = [], []
def check(name, cond, info=''):
    print(('ok   ' if cond else 'FAIL ') + name + ('' if cond else '  ' + str(info)[:500]))
    if not cond: FAILS.append(name)
def shot(pg, n):
    if shots: os.makedirs(shots, exist_ok=True); pg.screenshot(path=os.path.join(shots, n + '.png'), full_page=False)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=site)); threading.Thread(target=srv.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:%d/' % srv.server_address[1]
def validate_node(text):
    js = "const K=require(process.argv[1]);const v=K.validate(require('fs').readFileSync(0,'utf8'));console.log(JSON.stringify({ok:v.ok,errors:v.errors,warnings:v.warnings,n:v.ok?v.course.chapters.length:0,labs:v.ok?v.course.chapters.reduce((a,c)=>a+c.practice.length,0):0,quiz:v.ok?v.course.chapters.reduce((a,c)=>a+c.quiz.length,0):0}))"
    return json.loads(subprocess.run(['node', '-e', js, os.path.join(HERE, '..', 'src', 'course.js')], input=text, capture_output=True, text=True).stdout)
def raw_route(route):
    name = route.request.url.split('/courses/')[-1]
    p = os.path.join(courses, name)
    route.fulfill(status=200 if os.path.exists(p) else 404, body=open(p).read() if os.path.exists(p) else 'nf', headers={'Access-Control-Allow-Origin': '*'})
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 1360, 'height': 900}, accept_downloads=True)
    ctx.route('https://raw.githubusercontent.com/**', raw_route)
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('dialog', lambda d: d.accept())
    pg.goto(base + 'editor/'); pg.wait_for_selector('#side .nav'); pg.wait_for_timeout(400)
    check('blank course is valid', pg.inner_text('#vstat') in ('Ready',) or 'warning' in pg.inner_text('#vstat'), pg.inner_text('#vstat'))
    # course basics
    pg.fill('label.f:has-text("Title") >> input', 'Bees 101'); pg.fill('label.f:has-text("Course id") >> input', 'bees-101')
    pg.fill('label.f:has-text("Tags") >> input', 'bees, biology'); pg.wait_for_timeout(700)
    check('title shows in the sidebar', 'Bees 101' in pg.inner_text('#side'))
    # the title is required: error, then fixed
    pg.fill('label.f:has-text("Title") >> input', ''); pg.wait_for_timeout(700)
    check('missing title is an error', 'error' in pg.inner_text('#vstat') and 'title' in pg.inner_text('#issues'), pg.inner_text('#issues'))
    pg.fill('label.f:has-text("Title") >> input', 'Bees 101'); pg.wait_for_timeout(700)
    # chapter 1
    pg.click('#chlist .nav >> nth=0'); pg.wait_for_selector('h2:has-text("Chapter 1")')
    pg.fill('main > label.f:has-text("Title") >> input', 'The hive')
    pg.click('summary:has-text("Feynman")') if not pg.is_visible('label.f:has-text("Analogy")') else None
    pg.fill('label.f:has-text("Analogy") >> textarea', 'A hive is like a busy city where everyone has one job.'); pg.fill('label.f:has-text("Teach-back question") >> input', 'What does a worker bee do?')
    pg.fill('label.f:has-text("Sentences") >> textarea', 'Bees live in hives.\nA hive has one queen.')
    pg.click('summary:has-text("Lesson")') if not pg.is_visible('label.f:has-text("Paragraphs")') else None
    pg.fill('label.f:has-text("Paragraphs") >> textarea', 'Worker bees collect nectar.\n\nThe queen lays eggs.')
    pg.click('summary:has-text("Quiz")'); pg.click('button:has-text("+ Add question")'); pg.wait_for_selector('.item label.f:has-text("Question") >> input')
    pg.fill('.item label.f:has-text("Question") >> input', 'Who lays the eggs?')
    opts = pg.locator('.opt input[type=text]'); opts.nth(0).fill('Workers'); opts.nth(1).fill('The queen'); opts.nth(2).fill('Drones')
    pg.locator('.opt input[type=radio]').nth(1).check()
    pg.click('summary:has-text("Practice labs")'); pg.click('button:has-text("+ fill")'); pg.wait_for_selector('label.f:has-text("Text with blanks") >> textarea')
    pg.fill('label.f:has-text("Text with blanks") >> textarea', 'Bees make honey from nectar.'); pg.wait_for_timeout(800)
    check('fill lab without blanks is flagged', 'fill lab needs {{answer}} blanks' in pg.inner_text('#issues'), pg.inner_text('#issues'))
    check('chapter with problems is marked in the sidebar', '•' in pg.inner_text('#chlist'))
    pg.fill('label.f:has-text("Text with blanks") >> textarea', 'Bees make {{honey}} from nectar.'); pg.wait_for_timeout(800)
    C = pg.evaluate('__editor.C'); ch = C['chapters'][0]
    check('chapter written', ch['title'] == 'The hive' and ch['summary'] == ['Bees live in hives.', 'A hive has one queen.'] and ch['quiz'][0]['answer'] == 1 and ch['quiz'][0]['options'] == ['Workers', 'The queen', 'Drones'], ch)
    check('Feynman block first, in the standard wording', ch['lesson'][0]['items'][0].startswith('Explain it simply. A hive') and 'What does a worker bee do?' in ch['lesson'][0]['items'][1] and ch['lesson'][1]['items'] == ['Worker bees collect nectar.', 'The queen lays eggs.'], ch['lesson'])
    check('course is ready', pg.inner_text('#vstat') == 'Ready', pg.inner_text('#vstat') + ' ' + pg.inner_text('#issues'))
    shot(pg, 'editor1_chapter')
    # add, duplicate, reorder, delete chapters; undo
    pg.click('button:has-text("+ Add chapter")'); pg.wait_for_selector('h2:has-text("Chapter 2")')
    pg.click('#chlist .nav >> nth=0'); pg.click('button:has-text("Duplicate") >> nth=0'); pg.wait_for_timeout(300)
    check('duplicate', len(pg.evaluate('__editor.C.chapters')) == 3 and pg.evaluate('__editor.C.chapters[1].title') == 'The hive')
    pg.click('button.danger:has-text("Delete") >> nth=0'); pg.wait_for_timeout(300)
    check('delete', len(pg.evaluate('__editor.C.chapters')) == 2)
    pg.click('#bUndo'); pg.wait_for_timeout(300)
    check('undo brings it back', len(pg.evaluate('__editor.C.chapters')) == 3)
    # autosave survives a reload
    pg.wait_for_timeout(600); pg.reload(); pg.wait_for_selector('#side .nav'); pg.wait_for_timeout(400)
    check('autosaved draft', pg.evaluate('__editor.C.title') == 'Bees 101' and len(pg.evaluate('__editor.C.chapters')) == 3)
    # download and validate with the app's validator
    with pg.expect_download() as dl: pg.click('#bDown')
    check('file name from the id', dl.value.suggested_filename == 'bees-101.course.json', dl.value.suggested_filename)
    v = validate_node(open(dl.value.path()).read()); check('downloaded course validates', v['ok'] and v['n'] == 3 and v['quiz'] >= 1, v)
    # hand it to the web app
    with ctx.expect_page() as np: pg.click('#bTry')
    app = np.value; app.on('pageerror', lambda e: errs.append('app: ' + str(e))); app.wait_for_selector('#main'); app.wait_for_timeout(1500)
    check('the app imported the course', app.evaluate("__app.ST.courses.some(c=>c.id==='bees-101')"), app.inner_text('body')[:300])
    shot(app, 'editor3_in_app'); app.close()
    # open every real course from a file, visit every chapter and every section, and download: nothing may be lost
    for f in sorted(x for x in os.listdir(courses) if x.endswith('.course.json')):
        text = open(os.path.join(courses, f)).read(); before = validate_node(text)
        with pg.expect_file_chooser() as fc: pg.click('#bOpen')
        fc.value.set_files(os.path.join(courses, f)); pg.wait_for_timeout(300)
        n = len(json.loads(text)['chapters'])
        for i in range(n):
            pg.evaluate("i => document.querySelectorAll('#chlist .nav')[i].click()", i)
        pg.wait_for_timeout(250)
        with pg.expect_download() as dl: pg.click('#bDown')
        after = validate_node(open(dl.value.path()).read())
        check('round trip ' + f, after['ok'] and (after['n'], after['labs'], after['quiz']) == (before['n'], before['labs'], before['quiz']) and len(after['warnings']) <= len(before['warnings']), (before, after))
    # open from the library (catalog on the site, course files from GitHub raw)
    pg.click('#bLib'); pg.wait_for_selector('#dlg .nav'); pg.click('#dlg .nav:has-text("Data Structures")'); pg.wait_for_timeout(1500)
    check('opened from the library', pg.evaluate('__editor.C.id') == 'data-structures-algorithms' and pg.inner_text('#vstat') != '', pg.evaluate('__editor.C.id'))
    pg.click('#chlist .nav >> nth=1'); pg.click('summary:has-text("Practice labs")'); pg.wait_for_timeout(300); shot(pg, 'editor2_labs')
    # paste: bad JSON and a non-course are refused
    pg.click('#bPaste'); pg.fill('#dlg textarea', '{oops'); pg.click('#dlg button.pri'); check('bad paste refused', 'Not valid JSON' in pg.inner_text('#dlg'))
    pg.fill('#dlg textarea', '{"format":"lilith-settings"}'); pg.click('#dlg button.pri'); check('settings file refused', 'not a Lilith course' in pg.inner_text('#dlg')); pg.click('#dlg button:has-text("Cancel")')
    # phone layout
    m = b.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=2, is_mobile=True, has_touch=True); mp = m.new_page(); mp.on('pageerror', lambda e: errs.append('mobile: ' + str(e)))
    mp.goto(base + 'editor/'); mp.wait_for_selector('#side .nav'); mp.wait_for_timeout(300)
    check('phone: no sideways scroll', mp.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), mp.evaluate('document.documentElement.scrollWidth'))
    shot(mp, 'editor4_phone'); m.close()
    b.close()
srv.shutdown(); shutil.rmtree(site, ignore_errors=True)
check('no page errors', not errs, errs)
print('FAILS', FAILS); sys.exit(1 if FAILS else 0)
