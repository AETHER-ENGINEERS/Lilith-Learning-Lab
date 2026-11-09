"""Insert a Feynman-method block ("Explain it simply" + "Teach it back") at the
start of each chapter's lesson. Data: build/feynman/<course-id>.py defining
FEY = [ (analogy, stall) or None per chapter ]. Idempotent."""
import json, glob, os, sys, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "Explain it simply."

def block(analogy, stall):
    return {"type": "text", "items": [
        MARK + " " + analogy,
        "Teach it back. Explain this chapter out loud to a ten-year-old, with no jargon and no notes. "
        "If you cannot answer this, reread the lesson at that spot: " + stall]}

def apply(path):
    d = json.load(open(path))
    fp = os.path.join(ROOT, "build", "feynman", d["id"] + ".py")
    if not os.path.exists(fp):
        return None
    spec = importlib.util.spec_from_file_location("fey_" + d["id"].replace("-", "_"), fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    n = 0
    for i, ch in enumerate(d["chapters"]):
        e = m.FEY[i] if i < len(m.FEY) else None
        lesson = [b for b in ch.get("lesson", [])
                  if not (isinstance(b, dict) and b.get("type", "text") == "text"
                          and (b.get("items") or [""])[0].startswith(MARK))]
        if e:
            lesson.insert(0, block(*e)); n += 1
        ch["lesson"] = lesson
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=1)
    return n

if __name__ == "__main__":
    for f in sorted(glob.glob(os.path.join(ROOT, "courses", "*.course.json"))):
        r = apply(f)
        print(os.path.basename(f), r)
