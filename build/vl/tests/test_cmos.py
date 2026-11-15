import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import build, labs_cmos
from playwright.sync_api import sync_playwright
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for k, (title, intro, h, levels) in enumerate(labs_cmos.LABS_CMOS):
        path = "/tmp/cmos_%d.html" % k; open(path, "w").write(build.cmos_html(title, intro, levels))
        pg = b.new_page(viewport={"width": 420, "height": 1000}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.add_init_script("window.lilith={complete:function(){window.__done=true}}")
        pg.goto("file://" + path); pg.wait_for_function("window.__lab")
        res = []
        for i in range(len(levels)):
            pg.evaluate("i => __lab.enter(i)", i); pre = pg.evaluate("i => __lab.isDone(i)", i)
            pg.evaluate("i => __lab.solve(i)", i); ok = pg.evaluate("i => __lab.isDone(i)", i); res.append((pre, ok))
        done = pg.evaluate("!!window.__done"); good = all((not a) and c for a, c in res) and done and not errs
        bad += not good; print(("ok  " if good else "BAD ") + title, res, done, errs[:2])
        pg.screenshot(path="/tmp/cmos_%d.png" % k, full_page=True)
    b.close()
print("CMOS LABS", "PASSED" if not bad else "FAILED"); sys.exit(1 if bad else 0)
