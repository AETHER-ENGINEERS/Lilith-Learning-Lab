import sys, os, time
from playwright.sync_api import sync_playwright
web, course = sys.argv[1], sys.argv[2]
fails = []; errs = []
def check(c, m):
    if not c: fails.append(m); print('FAIL', m)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, is_mobile=True, has_touch=True)
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + os.path.join(web, 'index.html')); pg.wait_for_selector('#imp')
    with pg.expect_file_chooser() as fc: pg.click('#imp')
    fc.value.set_files([course]); pg.wait_for_selector('#modal[open]'); time.sleep(.5); pg.click('#ml'); pg.wait_for_selector('#lgo')
    pg.click('#nav [data-t="practice"]'); pg.wait_for_selector('[data-lab]')
    pg.click('[data-lab="ch1/lab0"]'); pg.wait_for_selector('#run')
    pg.fill('#code', "print('ready')\ndef square(n):\n    return n*n\n"); pg.click('#run')
    pg.wait_for_selector('#res b', timeout=30000); t = pg.inner_text('#res'); print(t.replace('\n', ' | '))
    check('ALL CORRECT' in t, 'solution passes')
    pg.fill('#code', "def square(n):\n    return n+n\n"); pg.click('#run'); pg.wait_for_function("document.querySelector('#res').innerText.includes('NOT YET')", timeout=30000)
    check('FAIL' in pg.inner_text('#res'), 'wrong code fails')
    pg.fill('#code', "def square(n:\n  pass"); pg.click('#run'); pg.wait_for_function("document.querySelector('#res').innerText.includes('ERROR')", timeout=30000)
    print(pg.inner_text('#res').replace('\n', ' | '))
    pg.fill('#code', "print('hi', 1+1)\nfor i in range(3): print(i)"); pg.click('#runo'); pg.wait_for_function("document.querySelector('#res').innerText.includes('hi 2')", timeout=30000)
    print(pg.inner_text('#res').replace('\n', ' | '))
    pg.fill('#code', "while True: pass"); t0 = time.time(); pg.click('#run'); pg.wait_for_function("document.querySelector('#res').innerText.includes('longer than')", timeout=30000)
    check(time.time() - t0 < 14, 'endless loop stopped in time')
    pg.fill('#code', "def square(n):\n    return n*n\nprint('ready')"); pg.click('#run'); pg.wait_for_function("document.querySelector('#res').innerText.includes('ALL CORRECT')", timeout=30000)
    pg.screenshot(path='/tmp/shots/py_lab.png')
    b.close()
print('ERRORS', errs, 'FAILS', fails); sys.exit(1 if errs or fails else 0)
