"""Checks the Q.js labs: every level's shown solution really solves its level, and the circuit editor renders."""
import sys, os, json
from playwright.sync_api import sync_playwright

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ql", "apps")
shots = sys.argv[1] if len(sys.argv) > 1 else "/tmp/shots"
os.makedirs(shots, exist_ok=True)
fails = []

def check(c, msg):
    print(("ok   " if c else "FAIL ") + msg)
    if not c: fails.append(msg)

with sync_playwright() as p:
    b = p.chromium.launch()
    for name in ("qgates", "qentangle", "qalgo"):
        pg = b.new_page(viewport={"width": 420, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.add_init_script("window.lilith={complete:function(){window.__done=(window.__done||0)+1}}")
        pg.goto("file://" + os.path.abspath(os.path.join(root, name + ".html")))
        pg.wait_for_timeout(800)
        n = pg.evaluate("LEVELS.length")
        check(pg.evaluate("document.querySelectorAll('#circuit *').length > 5") , name + ": editor rendered")
        for i in range(n):
            pg.evaluate("li=%d; show()" % i)
            pg.wait_for_timeout(300)
            status0 = pg.inner_text("#status")
            sol = pg.evaluate("LEVELS[li].solution")
            pg.evaluate("loadText(LEVELS[li].solution)")
            pg.wait_for_timeout(500)
            st = pg.inner_text("#status")
            check("Solved" in st, "%s level %d solves with its solution (%s)" % (name, i + 1, st[:40].replace("\n", " ")))
            if i == 0: check("Solved" not in status0, name + ": level 1 starts unsolved")
        if name == "qentangle":
            pg.evaluate("li=1; show()"); pg.wait_for_timeout(300)
            for c in ("new 3", "h 1", "cnot 1 2", "explain"):
                pg.fill("#cmd", c); pg.click("#go"); pg.wait_for_timeout(500)
            out = pg.inner_text("#out")
            check("Entangled" in out and "|11" in out, "qentangle: console builds a Bell state and explains it")
            check("Solved" in pg.inner_text("#status"), "qentangle: console commands solve a level")
            pg.fill("#cmd", "h 9"); pg.click("#go"); pg.wait_for_timeout(200)
            check("This circuit has 3" in pg.inner_text("#out"), "console: friendly error for bad qubit")
            pg.fill("#cmd", "banana"); pg.click("#go"); pg.wait_for_timeout(200)
            check("do not know" in pg.inner_text("#out"), "console: unknown command is friendly")
            pg.fill("#cmd", "shots 20"); pg.click("#go"); pg.wait_for_timeout(200)
            check("Measured 20" in pg.inner_text("#out"), "console: shots")
            pg.fill("#cmd", "undo"); pg.click("#go"); pg.wait_for_timeout(300)
            check("Undone" in pg.inner_text("#out"), "console: undo")
            check("JavaScript console" not in pg.inner_text("body"), name + ": no JavaScript-console text")
        if name == "qgates": pg.screenshot(path=os.path.join(shots, "ql_gates.png"))
        check(pg.evaluate("window.__done||0") >= 1, name + ": lab completion fired")
        check(not errs, name + ": no page errors " + str(errs[:2]))
    pg = b.new_page(viewport={"width": 420, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script("window.lilith={complete:function(){window.__done=(window.__done||0)+1}}")
    pg.goto("file://" + os.path.abspath(os.path.join(root, "qplay.html")))
    pg.wait_for_timeout(800)
    check("00" in pg.inner_text("#bars") and "11" in pg.inner_text("#bars"), "qplay: Bell circuit shows 00 and 11")
    pg.click("#shots"); pg.wait_for_timeout(200)
    check(pg.evaluate("window.__done||0") >= 1, "qplay: shots complete the lab")
    pg.fill("#cmd", "new 1"); pg.click("#go"); pg.fill("#cmd", "coin 1"); pg.click("#go"); pg.wait_for_timeout(500)
    check("50%" in pg.inner_text("#out") and "superposition" in pg.inner_text("#out"), "qplay: coin gives 50% and superposition")
    pg.click("button.chip >> text=help"); pg.wait_for_timeout(200)
    check("Add a gate" in pg.inner_text("#out"), "qplay: chips work")
    check("JavaScript console" not in pg.inner_text("body"), "qplay: no JavaScript-console text")
    pg.screenshot(path=os.path.join(shots, "ql_play.png"))
    check(not errs, "qplay: no page errors " + str(errs[:2]))
    b.close()
print("FAILS", fails)
sys.exit(1 if fails else 0)
