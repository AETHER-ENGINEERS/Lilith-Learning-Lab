"""Drive the four CTMV labs in a headless browser: each must complete through real clicks, also inside the app's sandbox (iframe + CSP)."""
import os, sys, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import labs
from playwright.sync_api import sync_playwright
CSP = "default-src 'self' data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src data: blob:"

def wrap(lab_html):
    inner = '<meta http-equiv="Content-Security-Policy" content="%s">' % CSP + lab_html
    return '<!doctype html><body><script>window.lilith={complete:function(){window.__done=true}};addEventListener("message",e=>{if(e.data==="done")window.__done=true})</script>' \
           '<iframe id=f sandbox="allow-scripts allow-forms allow-modals allow-downloads" style="width:500px;height:900px" srcdoc="%s"></iframe></body>' % H.escape(inner, quote=True)


TAP = """() => { const cv = document.getElementById('vzc'); const r = cv.getBoundingClientRect(); const fire = (t, x, y, el) => (el || window).dispatchEvent(new MouseEvent(t, {clientX: r.left + x, clientY: r.top + y, bubbles: true}));
  const h = VZ.hit[VZ.hit.length - 1]; fire('mousedown', h.x, h.y, cv); fire('mouseup', h.x, h.y); return VZ.sel; }"""
DRAG = """() => { const cv = document.getElementById('vzc'); const r = cv.getBoundingClientRect(); const fire = (t, x, y, el) => (el || window).dispatchEvent(new MouseEvent(t, {clientX: r.left + x, clientY: r.top + y, bubbles: true}));
  fire('mousedown', 50, 50, cv); fire('mousemove', 120, 70); fire('mouseup', 120, 70); }"""

def drive(key, fr, pg):
    fr.click('button[data-t=x]'); fr.wait_for_timeout(400)
    if key == 'three': fr.evaluate(DRAG)
    if key != 'garden': print('   tap ->', fr.evaluate(TAP))
    if key == 'warp': fr.evaluate("document.getElementById('vzlam').value=0.8;document.getElementById('vzlam').dispatchEvent(new Event('input'))")
    pg.screenshot(path='/tmp/ctmv_viz_%s.png' % key)
    c = lambda s: fr.click(s)
    if key == 'three':
        c('button[data-t=v]'); fr.select_option('#note', 'retry-storm')
        c('button[data-t=g]'); c('#runq'); assert 'overload' in fr.inner_text('#gout'), fr.inner_text('#gout')
        c('#runv'); assert 'PROVEN' in fr.inner_text('#gout')
        c('button[data-t=m]'); fr.select_option('#mnote','retry-storm'); c('#runk'); print('   ', fr.inner_text('#mout')[:200]); assert 'circuit-breaker' in fr.inner_text('#mout')
    elif key == 'bridge':
        c('button[data-t=d]'); txt = fr.inner_text('#dtab'); assert 'microphone-squeal' in txt
        rows = fr.query_selector_all('#btab tr')
        for r in rows:
            if 'retry-storm ↔ microphone-squeal' in r.inner_text() or 'microphone-squeal ↔ retry-storm' in r.inner_text(): r.query_selector('button').click()
    elif key == 'warp':
        c('button[data-t=w]')
        fr.evaluate("document.getElementById('lam').value=0.7;document.getElementById('lam').dispatchEvent(new Event('input'))")
        fr.evaluate("document.getElementById('mu').value=0.8;document.getElementById('mu').dispatchEvent(new Event('input'))")
        fr.click('button.q[data-q="clients retry too much"]'); print('   ', fr.inner_text('#wout').replace('\n', ' | ')[:300])
        fr.click('button.q[data-q="should clients retry straight away"]'); print('   ', fr.inner_text('#wout').replace('\n', ' | ')[:300])
        fr.click('button.q[data-q="what is wrong with a long time to live"]'); print('   ', fr.inner_text('#wout').replace('\n', ' | ')[:300])
    elif key == 'garden':
        c('button[data-t=v]'); c('#newNote'); fr.fill('#md', '# Echo\ntags: audio\nSound bounces back and is heard again.\n- echo causes ringing_noise'); c('#saveNote')
        c('button[data-t=r]'); c('#gard'); print('   ', fr.inner_text('#rout').replace('\n', ' | ')[:500])
        fr.select_option('#dim', '128'); c('#replay'); print('   ', fr.inner_text('#rout').replace('\n', ' | ')[:400])

def run(sandbox=True):
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for key in labs.LABS:
            l = labs.lab(key); path = '/tmp/ctmv_%s.html' % key
            open(path, 'w', encoding='utf-8').write(wrap(l['html']) if sandbox else '<script>window.lilith={complete:function(){window.__done=true}}</script>' + l['html'])
            pg = b.new_page(viewport={'width': 520, 'height': 1000}); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.goto('file://' + path)
            fr = pg.frame_locator('#f') if sandbox else pg
            # the sandboxed frame is cross-origin: use frame objects
            if sandbox:
                pg.wait_for_selector('#f'); frame = pg.frames[1]
            else: frame = pg
            frame.wait_for_function('window.__ready || window.__err', timeout=60000)
            err = frame.evaluate('window.__err'); 
            if err: print('BOOT FAIL', key, err); bad += 1; continue
            try: drive(key, frame, pg)
            except BaseException as e: print('DRIVE FAIL', key, repr(e)[:300], frame.evaluate('document.getElementById("gout").textContent')); bad += 1; continue
            goals = frame.evaluate('JSON.stringify(window.__lab.done)'); comp = frame.evaluate('window.__lab.completed()')
            want = [g[0] for g in l and labs.LABS[key]['goals']]
            ok = comp and all(g in goals for g in want) and not errs
            print(('ok  ' if ok else 'BAD '), key, goals, 'completed' if comp else 'NOT completed', errs[:2])
            bad += (not ok)
            pg.close()
        b.close()
    return bad
if __name__ == '__main__':
    sys.exit(1 if run('--plain' not in sys.argv) else 0)
