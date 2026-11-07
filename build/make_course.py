#!/usr/bin/env python3
"""Build the Jetson AGX Xavier course JSON for Lilith Learning Lab from docs/jetson_agx_xavier_tutorial.md
plus the hand-written maps, quizzes and labs in xavier_extras.py.

Usage: python3 make_course.py <output.json>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xavier_extras as X

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "docs")


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            km = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
            if km and km.group(2):
                meta[km.group(1)] = km.group(2).strip().strip('"')
        text = text[m.end():]
    return meta, text


def paragraphs(md):
    out, buf = [], []
    for ln in md.splitlines():
        if ln.strip():
            buf.append(ln.strip())
        elif buf:
            out.append(" ".join(buf)); buf = []
    if buf:
        out.append(" ".join(buf))
    return out


def bullets(md):
    return [re.sub(r"^\s*-\s+", "", l).strip() for l in md.splitlines() if re.match(r"^\s*-\s+", l)]


def lesson_blocks(md, images):
    """examples markdown -> lesson blocks; returns (blocks, conceptmaps)"""
    blocks, maps, items = [], [], []
    def flush():
        nonlocal items
        if items:
            blocks.append({"type": "text", "items": items}); items = []
    lines = md.split("\n"); i = 0; para = []
    def flushp():
        nonlocal para
        if para:
            items.append(" ".join(para)); para = []
    while i < len(lines):
        ln = lines[i]
        f = re.match(r"^```(\w*)", ln)
        im = re.match(r"^!\[([^\]]*)\]\(images/([^)]+)\)\s*$", ln.strip())
        if f:
            flushp(); flush(); buf = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            if f.group(1) == "conceptmap":
                title = "Concept map"; links = []
                for l in buf:
                    t = re.match(r"^title:\s*(.*)$", l)
                    if t: title = t.group(1)
                    elif l.count("|") == 2: links.append(l.strip())
                maps.append({"title": title, "links": links})
            else:
                blocks.append({"type": "code", "lang": f.group(1) or "text", "code": "\n".join(buf)})
        elif im:
            flushp(); flush()
            if im.group(2) in images:
                blocks.append({"type": "figure", "image": im.group(2), "caption": im.group(1)})
        elif re.match(r"^\s*-\s+", ln):
            flushp(); items.append(re.sub(r"^\s*-\s+", "", ln).strip())
        elif not ln.strip():
            flushp()
        else:
            para.append(ln.strip())
        i += 1
    flushp(); flush()
    return blocks, maps


def pack_xdc(dirname):
    import base64, io, zipfile
    d = os.path.join(HERE, "demo_apps", dirname)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(d)):
            z.write(os.path.join(d, fn), fn)
    return base64.b64encode(buf.getvalue()).decode()


def main(out):
    text = open(os.path.join(DOCS, "jetson_agx_xavier_tutorial.md"), encoding="utf-8").read()
    meta, body = front_matter(text)
    images = {}
    img_dir = os.path.join(DOCS, "images")
    for fn in sorted(os.listdir(img_dir)):
        if fn.endswith(".svg"):
            images[fn] = open(os.path.join(img_dir, fn), encoding="utf-8").read()
    raw = {}
    for part in re.split(r"^## ", body, flags=re.M)[1:]:
        head, _, rest = part.partition("\n")
        hm = re.match(r"^(\d+)\.\s+(.*)$", head.strip())
        if not hm: continue
        sec = {}
        for sp in re.split(r"^### ", rest, flags=re.M)[1:]:
            name, _, content = sp.partition("\n"); sec[name.strip().lower()] = content.strip("\n")
        raw[int(hm.group(1))] = (hm.group(2).strip(), sec)
    # glossary: placement of the 45 terms
    terms = []
    for ln in raw[20][1].get("key points", "").splitlines():
        gm = re.match(r"^- \*\*(.+?)\*\*:\s*(.*)$", ln)
        if gm: terms.append((gm.group(1), gm.group(2)))
    placed = {}
    for term, d in terms:
        if term in X.GLOSSARY_CH:
            placed[term] = X.GLOSSARY_CH[term]; continue
        alts = [re.sub(r"\s*\(.*?\)", "", term).strip()] + re.findall(r"\((.*?)\)", term)
        best, bs = None, 0
        for n, (title, sec) in raw.items():
            if n in (0, 20, 21, 22): continue
            txt = "\n".join(sec.values())
            c = sum(len(re.findall(re.escape(a), txt, flags=re.I)) for a in alts if len(a) > 1)
            if c > bs: bs, best = c, n
        placed[term] = best if best is not None else 1
    chapters = []
    for n in sorted(raw):
        title, sec = raw[n]
        blocks, cmaps = lesson_blocks(sec.get("examples", ""), images)
        maps = [{"title": t, "links": l} for t, l in X.MAPS.get(n, [])] + cmaps
        gl = [{"term": t, "def": d} for t, d in terms if placed[t] == n] + [{"term": t, "def": d} for t, d in X.EXTRA_GLOSSARY.get(n, [])]
        kp = bullets(sec.get("key points", ""))
        summary = paragraphs(sec.get("summary", ""))
        if n == 20:
            gl = [{"term": t, "def": d} for t, d in terms]
            kp = ["Every term used in the course is here, with a one-line meaning.", "Slash terms such as DLA / NVDLA name two spellings of the same idea.", "Use the flashcards and the glossary search in the Practice tab to review them."]
        cards = []
        for ln in sec.get("check yourself", "").splitlines():
            cm = re.match(r"^- Q:\s*(.*?)\s*\|\s*A:\s*(.*)$", ln)
            if cm: cards.append({"q": cm.group(1), "a": cm.group(2)})
        quiz = [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in X.QUIZ.get(n, [])]
        practice = list(X.LABS.get(n, []))
        if n == 10:
            practice.append({'type': 'webxdc', 'id': 'dla-explorer', 'title': 'DLA placement explorer', 'intro': 'An interactive webxdc app packed inside this course file. Build a model and watch layers land on the DLA or fall back to the GPU.', 'xdc': pack_xdc('dla-explorer'), 'height': 560})
        chapters.append({"id": "ch%d" % n, "number": n, "title": title, "maps": maps, "summary": summary, "glossary": gl, "keyPoints": kp,
                         "lesson": blocks, "quiz": quiz, "cards": cards, "practice": practice})
    course = {
        "format": "lilith-course", "version": 1, "id": "jetson-agx-xavier",
        "title": "NVIDIA Jetson AGX Xavier", "subtitle": "Hardware and software, from the chip to a multi-engine pipeline",
        "author": "Lilith Learning Lab", "description": "Learn the NVIDIA Jetson AGX Xavier: every processor, the memory, power, JetPack, CUDA, TensorRT, the DLA, VPI, cameras, containers and troubleshooting. Each chapter has a concept map, summary, glossary, key points, a lesson, a quiz and practice labs.",
        "pronounce": X.PRONOUNCE, "images": images, "chapters": chapters, "sandbox": X.sandbox(),
    }
    json.dump(course, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, os.path.getsize(out) // 1024, "KB,", len(chapters), "chapters")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "xavier.course.json")
