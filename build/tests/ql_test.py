"""Checks the Quantum Web Lab labs inside the quantum course: loads each lab and verifies every level's shown solution solves it."""
import sys, os, json, tempfile
from playwright.sync_api import sync_playwright

root = os.path.dirname(os.path.abspath(__file__))
course = json.load(open(os.path.join(root, "..", "..", "courses", "quantum-computing.course.json"), encoding="utf-8"))
fails = []

def check(c, msg):
    print(("ok   " if c else "FAIL ") + msg)
    if not c: fails.append(msg)

labs = [(ch["title"], l) for ch in course["chapters"] for l in ch["practice"] if l["type"] == "webxdc" and "QWL" in l["html"]]
check(len(labs) == 12, "12 Quantum Web Labs in the course (found %d)" % len(labs))
tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b = p.chromium.launch()
    for i, (ct, lab) in enumerate(labs):
        f = os.path.join(tmp, "lab%d.html" % i); open(f, "w", encoding="utf-8").write(lab["html"])
        pg = b.new_page(viewport={"width": 420, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.add_init_script("window.lilith={complete:function(){window.__done=(window.__done||0)+1}}")
        pg.goto("file://" + f); pg.wait_for_timeout(1200)
        n = pg.evaluate("(function(){var e=document.querySelector('.qwl');var a=(e&&e.__qwl)||document.querySelector('*[class~=qwl]').__qwl;return a.cfg.levels?a.cfg.levels.length:0})()")
        check(pg.evaluate("document.querySelectorAll('.qwl').length>0"), lab["title"] + ": renders")
        for k in range(n):
            pg.evaluate("document.querySelector('.qwl').__qwl.showLevel(%d)" % k); pg.wait_for_timeout(250)
            pg.click("#solbtn"); pg.click("#loadsol"); pg.wait_for_timeout(400)
            if pg.evaluate("!!document.querySelector('.qwl').__qwl.cfg.levels[%d].goal.via" % k):
                pg.click("#apply"); pg.wait_for_timeout(4000)
            check("Solved" in pg.inner_text("#status"), "%s level %d solution solves it" % (lab["title"], k + 1))
        if not n:
            pg.evaluate("document.querySelector('.qwl').__qwl.runCommand('run')"); pg.wait_for_timeout(300)
        check(not errs, lab["title"] + ": no page errors " + str(errs[:2]))
        pg.close()
    b.close()
print("FAILS", fails); sys.exit(1 if fails else 0)
