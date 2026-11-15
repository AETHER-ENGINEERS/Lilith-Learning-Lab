"""Check Verilog labs: every level must be unsolved with its starter code and solved with its solution, and the lab must report completion."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import build
from playwright.sync_api import sync_playwright


def check(labs, which=None, verbose=True):
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for idx, (title, intro, h, levels) in enumerate(labs):
            if which is not None and idx not in which: continue
            html = build.lab_html(title, intro, levels); path = "/tmp/vl_lab_%d.html" % idx; open(path, "w", encoding="utf-8").write(html)
            pg = b.new_page(viewport={"width": 420, "height": 1100}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.add_init_script("window.lilith={complete:function(){window.__done=true}}")
            pg.goto("file://" + path); pg.wait_for_function("window.__lab")
            res = []
            for i in range(len(levels)):
                pg.evaluate("i => __lab.enter(i)", i)
                r0 = pg.evaluate("async () => { const r = await __lab.run(); return r.ok ? r.log.slice(0,300) : 'COMPILE: ' + r.log.slice(0,300) }")
                pre = pg.evaluate("i => __lab.isDone(i)", i)
                pg.evaluate("i => __lab.solve(i)", i)
                ok = pg.evaluate("i => __lab.isDone(i)", i)
                res.append((pre, ok, r0, pg.inner_text("#goals").replace("\n", " | "), pg.inner_text("#con")[:400]))
            done = pg.evaluate("!!window.__done")
            good = all((not pre) and ok for pre, ok, *_ in res) and done and not errs
            if not good: bad += 1
            print(("ok  " if good else "BAD ") + title, len(levels), "levels", "complete" if done else "NOT complete", errs[:2] if errs else "")
            if not good or verbose == "all":
                for i, (pre, ok, r0, g, con) in enumerate(res):
                    if pre or not ok: print("   level", i + 1, "starter-done" if pre else "", "solution-FAILED" if not ok else "", "\n      goals:", g, "\n      console:", con.replace("\n", " / "))
            pg.close()
        b.close()
    return bad


if __name__ == "__main__":
    import labs_all
    which = [int(x) for x in sys.argv[1:]] or None
    bad = check(labs_all.LABS, which)
    print("VERILOG LABS", "PASSED" if not bad else "FAILED %d" % bad); sys.exit(1 if bad else 0)
