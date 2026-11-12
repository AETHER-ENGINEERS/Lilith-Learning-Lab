"""Insert an ELI5 ("explain it like I am five") block at the
start of each chapter's lesson. Data: build/eli5/<course-id>.py defining
FEY = [ (analogy, stall) or None per chapter ]. Idempotent."""
import json, glob, os, sys, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "ELI5."
OLD = ("Explain it simply.",)

def block(analogy, stall=None):
    parts = [x.strip() for x in analogy.split("\n\n") if x.strip()]
    parts[0] = MARK + " " + parts[0]
    return {"type": "text", "items": parts}

def apply(path):
    d = json.load(open(path))
    fp = os.path.join(ROOT, "build", "eli5", d["id"] + ".py")
    if not os.path.exists(fp):
        return None
    spec = importlib.util.spec_from_file_location("fey_" + d["id"].replace("-", "_"), fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    n = 0
    for i, ch in enumerate(d["chapters"]):
        e = m.FEY[i] if i < len(m.FEY) else None
        lesson = [b for b in ch.get("lesson", [])
                  if not (isinstance(b, dict) and b.get("type", "text") == "text"
                          and (b.get("items") or [""])[0].startswith((MARK,) + OLD))]
        if e:
            at = 1 if lesson and isinstance(lesson[0], dict) and (lesson[0].get("items") or [""])[0].startswith("Quick recap") else 0
            lesson.insert(at, block(*e)); n += 1
        ch["lesson"] = lesson
    d.setdefault("pronounce", {})["ELI5"] = "E L I five"
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=1)
    return n

if __name__ == "__main__":
    for f in sorted(glob.glob(os.path.join(ROOT, "courses", "*.course.json"))):
        r = apply(f)
        print(os.path.basename(f), r)
