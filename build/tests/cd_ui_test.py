import sys, os, time, json
from playwright.sync_api import sync_playwright
web, course = sys.argv[1], sys.argv[2]
d = json.load(open(course))
ci = 3; labs = d['chapters'][ci]['practice']; li = [i for i, l in enumerate(labs) if l.get('fn') == 'tokenize'][0]
cj = 8; wl = [i for i, l in enumerate(d['chapters'][cj]['practice']) if l['type'] == 'webxdc'][0]
fails = []; errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_context(viewport={'width': 390, 'height': 800}, is_mobile=True, has_touch=True).new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + os.path.join(web, 'index.html')); pg.wait_for_selector('#imp')
    with pg.expect_file_chooser() as fc: pg.click('#imp')
    fc.value.set_files([course]); pg.wait_for_selector('#modal[open]'); time.sleep(.5); pg.click('#ml'); pg.wait_for_selector('#lgo')
    pg.click('#nav [data-t="practice"]'); pg.wait_for_selector('[data-lab]')
    lid = 'ch%d/lab%d' % (ci + 1, li)
    pg.click('[data-lab="%s"]' % lid); pg.wait_for_selector('#run')
    pg.fill('#code', labs[li]['solution']); pg.click('#run')
    pg.wait_for_selector('#res b', timeout=30000); t = pg.inner_text('#res'); print(t.replace('\n', ' | ')[:200])
    if 'ALL CORRECT' not in t: fails.append('tokenize solution')
    pg.screenshot(path='/tmp/shots/cd_lab.png')
    pg.fill('#code', labs[li]['starter']); pg.click('#run'); pg.wait_for_function("document.querySelector('#res').innerText.includes('NOT YET')", timeout=30000)
    # webxdc stepper in chapter 9
    pg.click('#nav [data-t="practice"]') if False else None
    pg.goto('file://' + os.path.join(web, 'index.html'))
    b.close()
print('ERRORS', errs, 'FAILS', fails); sys.exit(1 if errs or fails else 0)
