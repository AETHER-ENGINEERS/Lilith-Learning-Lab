import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app_emu, app_basic, labs_c64
for k, (desc, src, goals) in labs_c64.LABS.items():
    tabs = ["c", "asm"] if k == "c" else ["asm"]
    app_emu.make_app(desc, tabs, src, goals, studio=(k == "c"), out="emu_%s.html" % k)
