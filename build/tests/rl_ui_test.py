import sys, os, json, time
from playwright.sync_api import sync_playwright
web, course, shots = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(shots, exist_ok=True); errs = []; fails = []
def check(c, m):
    if not c: fails.append(m); print('FAIL', m)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=2, is_mobile=True, has_touch=True)
    ctx.add_init_script("Object.defineProperty(window,'speechSynthesis',{value:{speaking:false,getVoices(){return[]},cancel(){},speak(u){setTimeout(()=>{u.onend&&u.onend()},30)}}});window.SpeechSynthesisUtterance=function(t){this.text=t};")
    page = ctx.new_page(); page.on('pageerror', lambda e: errs.append(str(e)))
    page.goto('file://' + os.path.join(web, 'index.html')); page.wait_for_selector('#imp')
    with page.expect_file_chooser() as fc: page.click('#imp')
    fc.value.set_files([course]); page.wait_for_selector('#modal[open]'); time.sleep(.5); page.click('#ml'); page.wait_for_selector('#lgo')
    page.screenshot(path=shots + '/rl_home.png')
    page.click('#nav [data-t="practice"]'); page.wait_for_selector('[data-lab]')
    labs = [l.get_attribute('data-lab') for l in page.query_selector_all('[data-lab]')]; print(labs[:12])
    # bandit
    page.click('[data-lab="ch4/lab2"]'); page.wait_for_selector('iframe'); page.wait_for_timeout(700)
    fr = page.frame_locator('iframe')
    for _ in range(4): fr.locator('#auto').click()
    page.wait_for_timeout(500); page.screenshot(path=shots + '/rl_bandit.png')
    prog = page.evaluate("JSON.parse(localStorage.getItem('lilith-lab-v1')).prog['rl-python-gymnasium-sb3']")
    check(prog['lab'].get('ch4/lab2'), 'bandit lab completed: ' + json.dumps(prog['lab']))
    page.click('#lback')
    # grid
    page.click('[data-lab="ch5/lab2"]'); page.wait_for_selector('iframe'); page.wait_for_timeout(700)
    fr = page.frame_locator('iframe'); fr.locator('#b2').click(); page.wait_for_timeout(400); fr.locator('#b2').click(); page.wait_for_timeout(500)
    page.screenshot(path=shots + '/rl_grid.png')
    st = fr.locator('#st').inner_text(); print(st)
    prog = page.evaluate("JSON.parse(localStorage.getItem('lilith-lab-v1')).prog['rl-python-gymnasium-sb3']")
    check(prog['lab'].get('ch5/lab2'), 'grid lab completed: ' + json.dumps(prog['lab']))
    page.click('#lback')
    # lecture on a chapter renders
    page.click('#nav [data-t="lecture"]'); page.wait_for_timeout(300)
    if not page.query_selector('#exgo'): page.evaluate('__onBack()'); page.wait_for_timeout(300)
    check('16 questions' in page.inner_text('#main'), 'course finalExam used: ' + page.inner_text('#main')[-300:])
    page.click('[data-lec="8"]'); page.wait_for_selector('#slide'); page.wait_for_timeout(1500); page.screenshot(path=shots + '/rl_lecture8.png')
    b.close()
print('ERRORS', errs, 'FAILS', fails); sys.exit(1 if errs or fails else 0)
