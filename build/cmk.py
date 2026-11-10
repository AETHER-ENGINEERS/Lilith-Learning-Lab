"""Shared course assembler. A make_<x>_course.py script calls main() with its config."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_trinity_course import split_long, stack  # noqa: E402


def main(cfg, chapters, argv):
    appdir = cfg.get("appdir")
    htmls = {}
    for ph, fname in cfg.get("apps", {}).items():
        with open(os.path.join(HERE, appdir, "apps", fname), encoding="utf-8") as f:
            htmls[ph] = f.read()
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in htmls:
                lab["html"] = htmls[lab["html"]]
    exam = [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in cfg["exam"]]
    for e in exam:
        assert 0 <= e["answer"] < len(e["options"]), e["q"]
    course = {
        "format": "lilith-course", "version": 1, "id": cfg["id"], "title": cfg["title"], "subtitle": cfg["subtitle"],
        "author": "Lilith Learning Lab", "description": cfg["description"], "pronounce": cfg["pronounce"],
        "chapters": chapters,
        "finalExam": {"title": "Final exam: " + cfg["title"], "passMark": 70, "size": 20, "questions": exam},
        "sandbox": cfg["sandbox"],
    }
    if cfg.get("images"):
        course["images"] = cfg["images"]
    out = argv[1] if len(argv) > 1 else cfg["id"] + ".course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(course, f, ensure_ascii=False, indent=1)
    labs = sum(len(c["practice"]) for c in chapters)
    py = sum(1 for c in chapters for l in c["practice"] if l["type"] == "python")
    print("wrote %s: %d chapters, %d labs (%d python), exam %d" % (out, len(chapters), labs, py, len(exam)))


def terminal(title, prompt, intro, items):
    """items: list of (command, [output lines])"""
    cmds = [{"re": "^help$", "out": ["%-10s %s" % (c, o[0][:60]) for c, o in items]}]
    for c, o in items:
        cmds.append({"re": "^%s$" % c, "out": o})
    cmds.append({"re": ".", "out": ["Unknown command. Type help."], "cls": "err"})
    return {"type": "terminal", "title": title, "prompt": prompt, "intro": intro + ", help",
            "chips": [c for c, o in items] + ["help"], "commands": cmds, "tasks": []}
