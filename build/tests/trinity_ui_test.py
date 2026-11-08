import sys, os, json, time
from playwright.sync_api import sync_playwright
web, course, shots = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(shots, exist_ok=True); errs = []; fails = []
def check(c, m):
    if not c: fails.append(m); print('FAIL', m)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=2, is_mobile=True, has_touch=True)
    ctx.add_init_script("Object.defineProperty(window,'speechSynthesis',{value:{speaking:false,getVoices(){return[]},cancel(){},speak(u){window.__said=(window.__said||[]).concat([u.text]);setTimeout(()=>{u.onend&&u.onend()},30)}}});window.SpeechSynthesisUtterance=function(t){this.text=t};")
    page = ctx.new_page(); page.on('pageerror', lambda e: errs.append(str(e)))
    page.goto('file://' + os.path.join(web, 'index.html')); page.wait_for_selector('#imp')
    with page.expect_file_chooser() as fc: page.click('#imp')
    fc.value.set_files([course]); page.wait_for_selector('#modal[open]'); time.sleep(.5); page.click('#ml'); page.wait_for_selector('#lgo')
    # Read view of ch9: formulas render with KaTeX
    page.click('#nav [data-t="read"]'); page.wait_for_timeout(300)
    page.click('.chap[data-n="9"]'); page.wait_for_timeout(1200)
    nk = page.locator('#main .katex').count(); print('katex in read view:', nk)
    check(nk >= 4, 'KaTeX elements rendered in Read view: %d' % nk)
    check('\\frac' not in page.inner_text('#main') and '$$' not in page.inner_text('#main'), 'no raw delimiters visible')
    page.evaluate("document.querySelector('#main .katex').scrollIntoView({block:'center'})"); page.wait_for_timeout(200); page.screenshot(path=shots + '/trin_math.png')
    page.evaluate('__onBack()'); page.wait_for_timeout(300)
    # Lecture: walk slides of ch9 until a formula appears; it must be KaTeX, not raw $$
    page.click('#nav [data-t="lecture"]'); page.wait_for_timeout(300)
    if not page.query_selector('[data-lec="1"]'): page.evaluate('__onBack()'); page.wait_for_timeout(300)
    page.click('[data-lec="1"]'); page.wait_for_selector('#slide')
    page.click('#lplay'); page.wait_for_timeout(300)
    for _ in range(14):
        if page.locator('#slide .katex').count(): break
        page.click('#lns'); page.wait_for_timeout(500)
    page.evaluate("document.querySelectorAll('#slide .b.hid').forEach(e=>e.classList.remove('hid'))"); page.wait_for_timeout(400)
    txt = page.inner_text('#slide')
    check('$$' not in txt and '\\begin' not in txt and '\\to' not in txt, 'raw LaTeX on lecture slide: ' + txt[:120])
    check(page.locator('#slide .katex').count() >= 1, 'KaTeX formula shown on a lecture slide: ' + txt[:150].replace(chr(10), ' | '))
    page.screenshot(path=shots + '/trin_lecture_math.png')
    page.evaluate('__onBack()'); page.wait_for_timeout(300)
    page.click('#nav [data-t="practice"]'); page.wait_for_selector('[data-lab]')
    for lab in ['ch5/lab2', 'ch9/lab2']:
        page.click('[data-lab="%s"]' % lab); page.wait_for_selector('iframe'); page.wait_for_timeout(700)
        fr = page.frame_locator('iframe')
        if lab == 'ch5/lab2':
            fr.locator('#st').click(); page.wait_for_timeout(200)
            for _ in range(3): fr.locator('#st').click(); page.wait_for_timeout(150)
            fr.locator('#all').click(); page.wait_for_timeout(300)
        else:
            rows = fr.locator('.row')
            for i in range(6): rows.nth(i).click()
            page.wait_for_timeout(300)
        page.screenshot(path=shots + '/trin_%s.png' % lab.replace('/', '_'))
        prog = page.evaluate("JSON.parse(localStorage.getItem('lilith-lab-v1')).prog['curry-howard-lambek']")
        check(prog['lab'].get(lab), lab + ' completed: ' + json.dumps(prog['lab']))
        page.click('#lback')
    # inline math in lab text (match options / quiz)
    page.click('[data-lab="ch11/lab0"]'); page.wait_for_selector('input,textarea'); page.wait_for_timeout(300)
    page.screenshot(path=shots + '/trin_lean.png')
    b.close()
print('ERRORS', errs, 'FAILS', fails); sys.exit(1 if errs or fails else 0)
