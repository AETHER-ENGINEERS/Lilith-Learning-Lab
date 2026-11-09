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


def make_pages(out):
    """Static web app for GitHub Pages: the same app plus a manifest, icons and an offline service worker."""
    from PIL import Image, ImageDraw
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    sys.argv = [sys.argv[0], "--web", out]
    main()
    html = open(os.path.join(out, "index.html"), encoding="utf-8").read()
    html = html.replace("<head>", '<head>\n<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#120a22">\n<link rel="icon" href="icon-192.png">', 1)
    html = html.replace("</body>", "<script>if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){})})}</script>\n</body>", 1)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    for n in (192, 512):
        im = Image.new("RGB", (n, n), "#1b1030")
        d = ImageDraw.Draw(im)
        d.ellipse([n * .08, n * .08, n * .92, n * .92], fill="#b26bff")
        d.polygon([(n * .36, n * .26), (n * .36, n * .74), (n * .74, n * .74), (n * .74, n * .62), (n * .5, n * .62), (n * .5, n * .26)], fill="#1b1030")
        im.save(os.path.join(out, "icon-%d.png" % n))
    json.dump({"name": "Lilith Learning Lab", "short_name": "Lilith Lab", "start_url": "./", "scope": "./", "display": "standalone",
               "background_color": "#120a22", "theme_color": "#120a22", "description": "Free, offline courses with a talking teacher and runnable labs.",
               "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
              open(os.path.join(out, "manifest.webmanifest"), "w"), indent=1)
    files = []
    for root, _, fs in os.walk(out):
        for f in fs:
            if f != "sw.js":
                files.append(os.path.relpath(os.path.join(root, f), out).replace(os.sep, "/"))
    import hashlib
    ver = hashlib.sha1(open(os.path.join(out, "index.html"), "rb").read() + open(os.path.join(out, "mp.js"), "rb").read()).hexdigest()[:10]
    sw = ("var V='lilith-" + ver + "';var A=" + json.dumps(["./"] + sorted(files)) + ";\n"
          "self.addEventListener('install',function(e){e.waitUntil(caches.open(V).then(function(c){return c.addAll(A)}).then(function(){return self.skipWaiting()}))});\n"
          "self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(x){return x!==V}).map(function(x){return caches.delete(x)}))}).then(function(){return self.clients.claim()}))});\n"
          "self.addEventListener('fetch',function(e){if(e.request.method!=='GET')return;var u=new URL(e.request.url);if(u.origin!==location.origin)return;"
          "e.respondWith(caches.match(e.request).then(function(r){return r||fetch(e.request)}))});\n")
    open(os.path.join(out, "sw.js"), "w").write(sw)
    print("wrote GitHub Pages web app to", out)


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
    if args[:1] == ["--pages"]:
        make_pages(args[1])
        return
    print(__doc__)


if __name__ == "__main__":
    main()
