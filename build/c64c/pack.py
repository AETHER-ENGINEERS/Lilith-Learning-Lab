"""Pack files into one gzip blob (path, data records) and base64 it for embedding in webxdc apps."""
import gzip, base64, struct, os
W = "/home/claude/8bitworkshop/8bitworkshop/"
ZIP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tc", "zip", "share", "cc65")


def pack(files):
    out = b""
    for p, d in files:
        pb = p.encode()
        out += struct.pack("<HI", len(pb), len(d)) + pb + d
    return base64.b64encode(gzip.compress(out, 9)).decode()


def emu_blob():
    return pack([("c64.wasm", open(W + "res/c64/c64.wasm", "rb").read()), ("c64.bios", open(W + "res/c64/c64.bios", "rb").read())])


def tools_blob():
    fl = []
    for t in ("cc65", "ca65", "ld65"):
        fl.append((t + ".wasm", open(W + "src/worker/wasm/%s.wasm" % t, "rb").read()))
    for sub in ("include", "cfg"):
        for root, _, fs in os.walk(os.path.join(ZIP, sub)):
            for f in fs:
                p = os.path.join(root, f)
                if sub == "include" and not (f.endswith(".h") or "/sys" in root or "/c64" in root):
                    pass
                fl.append(("share/cc65/" + os.path.relpath(p, ZIP), open(p, "rb").read()))
    fl.append(("share/cc65/lib/c64.lib", open(os.path.join(ZIP, "lib", "c64.lib"), "rb").read()))
    for root, _, fs in os.walk(os.path.join(ZIP, "asminc")):
        for f in fs:
            p = os.path.join(root, f)
            fl.append(("share/cc65/" + os.path.relpath(p, ZIP), open(p, "rb").read()))
    return pack(fl)


if __name__ == "__main__":
    a = emu_blob(); b = tools_blob()
    print(len(a), len(b))
