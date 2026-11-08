import sys, os, time, json
from playwright.sync_api import sync_playwright
web, course = sys.argv[1], sys.argv[2]
d = json.load(open(course)); lab = d['chapters'][6]['practice'][0]
fails = []; errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_context(viewport={'width': 390, 'height': 800}, is_mobile=True, has_touch=True).new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + os.path.join(web, 'index.html')); pg.wait_for_selector('#imp')
    with pg.expect_file_chooser() as fc: pg.click('#imp')
    fc.value.set_files([course]); pg.wait_for_selector('#modal[open]'); time.sleep(.5); pg.click('#ml'); pg.wait_for_selector('#lgo')
    pg.click('#nav [data-t="practice"]'); pg.wait_for_selector('[data-lab]')
    pg.click('[data-lab="ch7/lab0"]'); pg.wait_for_selector('#run')
    pg.fill('#code', lab['solution']); pg.click('#run')
    pg.wait_for_selector('#res b', timeout=30000); t = pg.inner_text('#res'); print(t.replace('\n', ' | '))
    if 'ALL CORRECT' not in t: fails.append('fcfs solution')
    pg.screenshot(path='/tmp/shots/os_lab.png')
    pg.click('#nav [data-t="practice"]'); pg.wait_for_selector('[data-lab="ch7/lab4"]'); pg.click('[data-lab="ch7/lab4"]')
    time.sleep(2)
    fr = pg.frame_locator('iframe').first
    for a in ['SJN', 'SRT', 'RR']:
        fr.get_by_role('button', name=a, exact=True).click()
    print(fr.locator('#msg').inner_text())
    pg.screenshot(path='/tmp/shots/os_sched.png')
    b.close()
print('ERRORS', errs, 'FAILS', fails); sys.exit(1 if errs or fails else 0)
