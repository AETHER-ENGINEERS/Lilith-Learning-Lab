#!/usr/bin/env python3
"""Build the web assets for the Lilith Learning Lab Android app: index.html plus the avatar frames.
The app ships EMPTY: courses are imported at run time as JSON files (see courses/ and course.js).

Usage: python3 build_web.py --web <dir>
"""
import base64, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def make_html():
    tpl = open(os.path.join(HERE, "src", "app.html"), encoding="utf-8").read()
    js = lambda n: open(os.path.join(HERE, "src", n), encoding="utf-8").read().replace("</", "<\\/")
    for tag, f in (("ICONS", "icons.js"), ("XDC", "xdc.js"), ("COURSE", "course.js"), ("MAPS", "maps.js"), ("MATH", "math.js"), ("NARRATE", "narrate.js"), ("SLIDES", "slides.js")):
        tpl = tpl.replace("/*__%s__*/" % tag, js(f))
    return tpl


def make_mp(out):
    """Pack MicroPython (loader + wasm) into mp.js so a WebView can load it with a script tag."""
    d = os.path.join(HERE, "vendor", "micropython")
    mjs = open(os.path.join(d, "micropython.mjs"), encoding="utf-8").read()
    # make it a classic script (module workers do not start from a blob under file://)
    mjs = mjs.replace("import.meta.url", '"http://localhost/micropython.mjs"').replace("export default _createMicroPythonModule", "").replace("export async function loadMicroPython", "async function loadMicroPython")
    assert "import.meta" not in mjs and "export async" not in mjs and "export default" not in mjs
    wasm = base64.b64encode(open(os.path.join(d, "micropython.wasm"), "rb").read()).decode()
    open(os.path.join(out, "mp.js"), "w", encoding="utf-8").write("window.LilithMP={mjs:" + json.dumps(mjs) + ",wasm:\"" + wasm + "\"};\n")


def main():
    args = sys.argv[1:]
    if args[:1] == ["--web"]:
        out = args[1]
        os.makedirs(os.path.join(out, "avatar"), exist_ok=True)
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(make_html())
        make_mp(out)
        for f in ("katex.min.js", "katex.css"):
            shutil.copy(os.path.join(HERE, "vendor", "katex", f), os.path.join(out, f))
        d = os.path.join(HERE, "assets", "avatar")
        for f in sorted(os.listdir(d)):
            if f.endswith(".webp"):
                shutil.copy(os.path.join(d, f), os.path.join(out, "avatar", f))
        print("wrote web assets to", out)
        return
    print(__doc__)


if __name__ == "__main__":
    main()
