#!/usr/bin/env python3
"""Browse-online UI test with mocked GitHub. Usage: python3 tests/store_test.py <web dir> <courses dir> [shots]"""
import sys, os
from playwright.sync_api import sync_playwright
web, courses = sys.argv[1], sys.argv[2]
shots = sys.argv[3] if len(sys.argv) > 3 else None
errors, fails = [], []
def check(c, m):
    if not c: fails.append(m); print('FAIL', m)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, has_touch=True, is_mobile=True)
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    def route(r):
        name = r.request.url.split('/courses/')[-1]
        f = os.path.join(courses, name)
        if os.path.exists(f):
            r.fulfill(status=200, body=open(f, 'rb').read(), headers={'access-control-allow-origin': '*', 'content-type': 'text/plain'})
        else:
            r.fulfill(status=404, body='nf')
    ctx.route('https://raw.githubusercontent.com/**', route)
    page.goto('file://' + os.path.abspath(web) + '/index.html'); page.wait_for_timeout(600)
    page.click('#brw'); page.wait_for_selector('[data-get]', timeout=5000)
    n = page.locator('[data-get]').count()
    check(n >= 17, 'catalog lists courses: %d' % n)
    check(page.locator('[data-sc]').count() >= 5, 'category chips')
    if shots: os.makedirs(shots, exist_ok=True); page.screenshot(path=shots + '/store.png')
    page.fill('#sq', 'vq-vae'); page.wait_for_timeout(200)
    check(page.locator('[data-get]').count() == 1, 'search narrows to 1')
    page.click('[data-get]'); page.wait_for_selector('#mo', timeout=8000)
    page.click('#ml'); page.wait_for_timeout(200)
    check('Installed' in page.inner_text('#main'), 'installed marker')
    page.fill('#sq', 'operating'); page.wait_for_timeout(200)
    page.click('[data-get]'); page.wait_for_selector('#mo', timeout=8000); page.click('#ml'); page.wait_for_timeout(200)
    page.click('#sb'); page.wait_for_timeout(200)
    check('Computer Science' in page.inner_text('#main') or 'Artificial Intelligence' in page.inner_text('#main'), 'library shows the category')
    if shots: page.screenshot(path=shots + '/lib.png')
    b.close()
print('errors', errors); print('FAILS', fails)
sys.exit(1 if (errors or fails) else 0)
