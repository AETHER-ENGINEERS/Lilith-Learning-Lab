#!/usr/bin/env python3
"""Build courses/catalog.json (and docs/catalog.json for the Lilith University site) from the course files.
Also writes category, tags and level into each course file (idempotent). Usage: python3 make_catalog.py"""
import glob, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
REPO = "lucky-edgelord/Lilith-Learning-Lab"

# id -> (category, level, tags)
META = {
 "rl-python-gymnasium-sb3": ("Artificial Intelligence", "Intermediate", ["reinforcement learning", "python", "gymnasium", "stable-baselines3"]),
 "alphazero": ("Artificial Intelligence", "Advanced", ["reinforcement learning", "games", "self-play", "mcts"]),
 "alphago": ("Artificial Intelligence", "Advanced", ["reinforcement learning", "games", "go", "mcts", "deep learning"]),
 "aixi": ("Artificial Intelligence", "Advanced", ["agi", "theory", "solomonoff", "universal ai"]),
 "godel-machine": ("Artificial Intelligence", "Advanced", ["agi", "self-improvement", "theory", "logic"]),
 "mcts": ("Artificial Intelligence", "Intermediate", ["search", "games", "bandits", "python"]),
 "ppo": ("Artificial Intelligence", "Intermediate", ["reinforcement learning", "policy gradient", "rlhf", "python"]),
 "dpo": ("Artificial Intelligence", "Intermediate", ["alignment", "rlhf", "preferences", "language models", "python"]),
 "transformer": ("Artificial Intelligence", "Intermediate", ["deep learning", "attention", "language models", "python"]),
 "vq-vae": ("Artificial Intelligence", "Intermediate", ["deep learning", "generative models", "discrete representations", "python"]),
 "harness-engineering": ("Artificial Intelligence", "Intermediate", ["agents", "llm", "tools", "evals", "python"]),
 "operating-systems": ("Computer Science", "Beginner", ["operating systems", "processes", "memory", "scheduling"]),
 "compiler-design": ("Computer Science", "Intermediate", ["compilers", "parsing", "languages", "python"]),
 "theory-of-computation": ("Computer Science", "Intermediate", ["automata", "computability", "complexity", "python"]),
 "curry-howard-lambek": ("Computer Science", "Advanced", ["type theory", "logic", "category theory", "lambda calculus"]),
 "jetson-agx-xavier": ("Hardware and Embedded", "Intermediate", ["nvidia", "jetson", "embedded", "gpu"]),
 "everyday-percentages": ("Getting Started", "Beginner", ["sample", "maths"]),
}
EXTRA = os.path.join(HERE, "catalog_meta.json")   # courses added later register here: {"id": [category, level, [tags]]}
if os.path.exists(EXTRA):
    META.update({k: tuple(v) for k, v in json.load(open(EXTRA, encoding="utf-8")).items()})


def main():
    import apply_eli5  # add the ELI5 block to every chapter first
    for f in sorted(glob.glob(os.path.join(ROOT, 'courses', '*.course.json'))):
        apply_eli5.apply(f)
    import apply_tables  # a table and references in every chapter
    for f in sorted(glob.glob(os.path.join(ROOT, 'courses', '*.course.json'))):
        apply_tables.apply(f)
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "courses", "*.course.json"))):
        raw = open(p, encoding="utf-8").read()
        c = json.loads(raw)
        cat, level, tags = META.get(c["id"], ("Other", "Intermediate", []))
        if c.get("category") != cat or c.get("level") != level or c.get("tags") != tags:
            c["category"], c["level"], c["tags"] = cat, level, tags
            json.dump(c, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        labs = [l for ch in c["chapters"] for l in ch.get("practice", [])]
        outline = []
        for ch in c["chapters"]:
            outline.append({"title": ch["title"], "summary": " ".join(ch.get("summary", [])), "keyPoints": ch.get("keyPoints", []),
                            "glossary": [g["term"] for g in ch.get("glossary", [])]})
        out.append({
            "id": c["id"], "file": os.path.basename(p), "title": c["title"], "subtitle": c.get("subtitle", ""), "author": c.get("author", ""),
            "description": c.get("description", ""), "category": cat, "level": level, "tags": tags,
            "chapters": len(c["chapters"]), "labs": len(labs), "pythonLabs": sum(1 for l in labs if l["type"] == "python"),
            "quiz": sum(len(ch.get("quiz", [])) for ch in c["chapters"]), "exam": len(c.get("finalExam", {}).get("questions", [])),
            "bytes": os.path.getsize(p), "outline": outline,
        })
    cats = sorted({x["category"] for x in out})
    cat = {"format": "lilith-catalog", "version": 1, "repo": REPO, "raw": "https://raw.githubusercontent.com/%s/main/courses/" % REPO,
           "categories": cats, "courses": out}
    for dest in (os.path.join(ROOT, "courses", "catalog.json"), os.path.join(ROOT, "docs", "catalog.json")):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        json.dump(cat, open(dest, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("catalog: %d courses, %d categories, %d bytes" % (len(out), len(cats), os.path.getsize(os.path.join(ROOT, "courses", "catalog.json"))))


if __name__ == "__main__":
    main()
