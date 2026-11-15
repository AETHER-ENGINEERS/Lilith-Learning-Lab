# -*- coding: utf-8 -*-
"""Packs the VeriSim / Icarus Verilog WebAssembly engine (GPL-2.0) into one compressed script for offline webxdc labs."""
import os, zlib, base64, json
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "..", "vendor", "verisim")
_cache = None


def engine_js():
    global _cache
    if _cache:
        return _cache
    blobs = {}
    for n in ("ivlpp", "ivl", "vvp"):
        js = open(os.path.join(V, n + ".js"), encoding="utf-8").read()
        assert "export default Module;" in js
        js = js.replace("export default Module;", "window.__VLM['%s']=Module;" % n).replace("import.meta.url", "'file:///vl/'")
        js = "(function(){" + js + "\n})();"
        for k, d in ((n + "_js", js.encode("utf-8")), (n + "_wasm", open(os.path.join(V, n + ".wasm"), "rb").read())):
            c = zlib.compressobj(9, zlib.DEFLATED, -15); z = c.compress(d) + c.flush()
            blobs[k] = base64.b64encode(z).decode()
    _cache = "window.VL_BLOBS=" + json.dumps(blobs) + ";\n" + open(os.path.join(HERE, "engine.js"), encoding="utf-8").read()
    return _cache
