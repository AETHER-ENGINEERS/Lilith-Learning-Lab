#!/usr/bin/env python3
"""Screenshots for the README. Usage: python3 tests/readme_shots.py <web dir> <courses dir> <out dir>"""
import sys, os, json
from playwright.sync_api import sync_playwright
web, courses, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
MOCK = """(()=>{const syn={speaking:false,getVoices(){return[]},cancel(){},speak(u){setTimeout(()=>{u.onend&&u.onend()},40)}};
Object.defineProperty(window,'speechSynthesis',{value:syn,configurable:true});window.SpeechSynthesisUtterance=class{constructor(t){this.text=t}};})();"""
CAT = json.load(open(os.path.join(courses, 'catalog.json')))
def route(r):
    u = r.request.url
    if u.endswith('catalog.json'):
        r.fulfill(status=200, body=json.dumps(CAT), content_type='application/json')
    else:
        r.fulfill(status=404, body='nf')
def shot(page, n): page.screenshot(path=os.path.join(out, n + '.png'))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=2, has_touch=True, is_mobile=True)
    ctx.add_init_script(MOCK)
    ctx.route('https://raw.githubusercontent.com/**', route)
    page = ctx.new_page()
    page.goto('file://' + os.path.abspath(web) + '/index.html'); page.wait_for_selector('#main')
    ids = ['mathematics-for-cs-ai', 'data-structures-algorithms', 'transformer', 'operating-systems', 'ppo']
    with page.expect_file_chooser() as fc:
        page.click('#imp')
    fc.value.set_files([os.path.join(courses, i + '.course.json') for i in ids])
    page.wait_for_selector('#modal[open]'); page.wait_for_timeout(1200)
    page.click('#ml'); page.wait_for_timeout(300)
    page.click('#libbtn'); page.wait_for_selector('.crs'); page.wait_for_timeout(300)
    shot(page, '1-library')
    page.click('[data-open="mathematics-for-cs-ai"]'); page.wait_for_selector('#lgo'); page.wait_for_timeout(300)
    shot(page, '2-course')
    page.click('#nav [data-t="read"]'); page.wait_for_timeout(300)
    page.click('[data-n="1"]'); page.wait_for_selector('h2'); page.wait_for_timeout(300)
    page.evaluate("(()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.textContent.indexOf('ELI5')>=0){n.parentElement.scrollIntoView({block:'start'});break}}window.scrollBy(0,-30)})()")
    page.wait_for_timeout(300); shot(page, '3-eli5')
    page.click('#nav [data-t="maps"]'); page.wait_for_selector('.mapbox'); page.wait_for_timeout(300)
    shot(page, '4-map')
    page.click('#nav [data-t="practice"]'); page.wait_for_selector('[data-lab]'); page.wait_for_timeout(300)
    labs = page.eval_on_selector_all('[data-lab]', 'els=>els.map(e=>e.dataset.lab)')
    page.click('[data-lab="ch1/lab1"]'); page.wait_for_selector('#code'); page.wait_for_timeout(300)
    sol = json.load(open(os.path.join(courses, 'mathematics-for-cs-ai.course.json')))['chapters'][0]['practice'][1]['solution']
    page.fill('#code', sol); page.wait_for_timeout(200)
    page.click('#chk') if page.query_selector('#chk') else page.get_by_text('Run tests').click(); page.wait_for_timeout(7000)
    shot(page, '5-python-lab')
    page.click('#lback'); page.click('#nav [data-t="progress"]'); page.wait_for_timeout(400)
    shot(page, '6-progress')
    page.click('#libbtn'); page.wait_for_selector('#brw'); page.click('#brw'); page.wait_for_selector('[data-get]'); page.wait_for_timeout(400)
    shot(page, '7-browse')
    b.close()
