"""Give every chapter a table and a references list.
Tables: if a chapter has no table block, add 'Key terms at a glance' from its glossary (up to 6 rows).
References: build/references/<course-id>.json = {"course": [{"title","url","note"}...], "chapters": {"1": [...]}}.
A chapter without its own list gets the course list; a course with no file gets the honest note below.
Idempotent."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
NOTE = {"title": "Written for Lilith Learning Lab from standard textbooks and documentation; no web sources were fetched", "url": "", "note": "Check facts against current documentation."}


def apply(path):
    d = json.load(open(path, encoding="utf-8"))
    rp = os.path.join(HERE, "references", d["id"] + ".json")
    ref = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {}
    course_refs = ref.get("course") or [NOTE]
    nt = nr = 0
    for i, ch in enumerate(d["chapters"]):
        lesson = ch.setdefault("lesson", [])
        if not any(isinstance(b, dict) and b.get("type") == "table" for b in lesson):
            g = [x for x in ch.get("glossary", []) if x.get("term") and x.get("def")][:6]
            if len(g) >= 2:
                lesson.append({"type": "table", "title": "Key terms at a glance", "head": ["Term", "Meaning"],
                               "rows": [[x["term"].replace("|", "/"), x["def"].replace("|", "/")] for x in g]})
                nt += 1
        if not ch.get("references"):
            ch["references"] = (ref.get("chapters") or {}).get(str(i + 1)) or course_refs
            nr += 1
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return nt, nr
