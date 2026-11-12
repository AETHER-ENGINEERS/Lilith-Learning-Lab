#!/usr/bin/env python3
"""Build quantum-web-lab into one self-contained HTML file (and a webxdc .xdc).

    python3 build.py                                  -> dist/quantum-web-lab.html and .xdc (a free playground)
    python3 build.py --config lab.json --out lab.html -> a lab with your levels and settings
    python3 build.py --no-python                      -> smaller file without MicroPython

From Python:  import build; html = build.build_html(config_dict, python=True)
See docs/embedding.md for the config format."""
import argparse, base64, gzip, json, os, struct, sys, zlib, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))


def mp_dir():
    """vendor/micropython here, or a sibling vendor/micropython when this folder is vendored into another project."""
    for d in (os.path.join(HERE, "vendor", "micropython"), os.path.join(HERE, "..", "micropython")):
        if os.path.exists(os.path.join(d, "micropython.wasm")):
            return d
    raise SystemExit("micropython.wasm not found (looked in vendor/micropython)")


def read(*p):
    with open(os.path.join(HERE, *p), encoding="utf-8") as f:
        return f.read()


def gz64(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.b64encode(gzip.compress(data, 9, mtime=0)).decode()


def mp_loader():
    """MicroPython's loader as a classic script (it is turned into a Worker, which cannot import modules from a blob)."""
    m = open(os.path.join(mp_dir(), "micropython.mjs"), encoding="utf-8").read()
    m = m.replace("import.meta.url", '"http://localhost/micropython.mjs"').replace("export default _createMicroPythonModule", "").replace("export async function loadMicroPython", "async function loadMicroPython")
    assert "import.meta" not in m and "export async" not in m and "export default" not in m
    return m


def js_json(obj):
    return json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def build_html(config=None, python=True, title="Quantum Web Lab"):
    cfg = dict(config or {})
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             "<title>%s</title><style>html,body{margin:0;background:#0f0b18}%s</style></head><body><div id=\"app\"></div>" % (title, read("src", "theme.css"))]
    parts.append('<script id="qwl-config" type="application/json">%s</script>' % js_json(cfg))
    parts.append("<script>" + read("src", "core.js") + "\n" + read("src", "ui.js") + "\n" + read("src", "pyrun.js") + "</script>")
    if python and cfg.get("python", True):
        wasm = open(os.path.join(mp_dir(), "micropython.wasm"), "rb").read()
        payload = {"mjs": gz64(mp_loader()), "wasm": gz64(wasm), "lib": read("src", "microqiskit.py")}
        parts.append("<script>window.QWL_PY=" + js_json(payload) + ";</script>")
    else:
        cfg["python"] = False
        parts[2] = '<script id="qwl-config" type="application/json">%s</script>' % js_json(cfg)
    parts.append("<script>(function(){var c={};try{c=JSON.parse(document.getElementById('qwl-config').textContent)}catch(e){}if(window.QWL_CONFIG)c=Object.assign(c,window.QWL_CONFIG);QWL.mount(document.getElementById('app'),c)})();</script></body></html>")
    return "".join(parts)


def icon_png(size=128):
    """A small purple icon, written without any library."""
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            dx, dy = x - size / 2, y - size / 2
            r = (dx * dx + dy * dy) ** 0.5
            if r < size * 0.18:
                px = (255, 255, 255, 255)
            elif abs(r - size * 0.33) < size * 0.025 or abs(r - size * 0.46) < size * 0.02:
                px = (217, 172, 255, 255)
            elif r < size * 0.5:
                px = (38, 27, 59, 255)
            else:
                px = (15, 11, 24, 0)
            row += bytes(px)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def build_xdc(html, path, name="Quantum Web Lab"):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("index.html", html)
        z.writestr("manifest.toml", 'name = "%s"\nsource_code_url = "https://github.com/lucky-edgelord/quantum-web-lab"\n' % name)
        z.writestr("icon.png", icon_png())


def default_config():
    return json.load(open(os.path.join(HERE, "presets", "playground.json"), encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", help="JSON config for the lab")
    ap.add_argument("--out", help="output .html path")
    ap.add_argument("--xdc", help="also write a webxdc .xdc here")
    ap.add_argument("--no-python", action="store_true", help="leave MicroPython out (smaller)")
    ap.add_argument("--title", default="Quantum Web Lab")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8")) if a.config else default_config()
    html = build_html(cfg, python=not a.no_python, title=a.title)
    if a.config is None and a.out is None:
        os.makedirs(os.path.join(HERE, "dist"), exist_ok=True)
        a.out = os.path.join(HERE, "dist", "quantum-web-lab.html")
        a.xdc = a.xdc or os.path.join(HERE, "dist", "quantum-web-lab.xdc")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s (%d KB)" % (a.out, len(html) // 1024))
    if a.xdc:
        build_xdc(html, a.xdc, a.title)
        print("wrote %s (%d KB)" % (a.xdc, os.path.getsize(a.xdc) // 1024))


if __name__ == "__main__":
    main()
