#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the CTMV course (Commutative Tri-Modal Vault) with labs built on jade-agent-kit and jade-vault.
12 chapters, 24 figures, tables, 4 browser labs (real SQLite + sqlite-vec + jade-kg), a few offline Python labs.
Usage: python3 make_ctmv_course.py [out.json]"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CT = os.path.join(HERE, "ctmv")
sys.path.insert(0, CT); sys.path.insert(1, os.path.join(HERE, "vq")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "cd"))
import cmk, cfigdefs, figs, ct_a, ct_b, labs  # noqa: E402
from clib import T  # noqa: E402

CHS = ct_a.CHS + ct_b.CHS
assert len(CHS) == 12

# the four browser labs (webxdc) go first in their chapters' practice lists
for _i, _k in ((4, "three"), (6, "bridge"), (9, "warp"), (10, "garden")):
    CHS[_i]["practice"].insert(0, labs.lab(_k))


# shorter summaries for four chapters (the summary slide keeps the rest of the items in one narration chunk)
SHORT = {
 0: ["A knowledge base, a vector database and an AI memory all fail in four ways.", "Ideas from different fields never meet, collections decay, old and new facts both come back, and memory is locked to one model.", "CTMV keeps three views of the same notes to answer each one. It is a design to test, not a proven product."],
 8: ["Similarity search ranks by distance. CTMV changes how distance is measured without moving any vector.", "A causal link multiplies the distance by one minus lambda. A conflict adds mu. At zero you get plain search.", "The warp is a view, so you can turn it off at any time."],
 10: ["Many AI memories are stored where only one assistant can read them. CTMV makes the files the memory and everything else a cache.", "Replay rebuilds G and M from the files. A new embedding model changes M only, and a fingerprint of the facts proves the replay.", "Plain files also mean anyone can inspect the memory with ordinary tools."],
 11: ["The labs use the Jade Agent Kit for files, SQLite and sqlite-vec, and the Jade Vault reasoner. Only the embedder is a toy.", "A real build adds an embedding model and a way to propose claims for you to approve.", "CozoDB could host graph and vectors together. Either way, a design is not a result: measure it."],
}
for _i, _s in SHORT.items():
    CHS[_i]["summary"] = _s

ANCHOR = re.compile(r"\s*\(See (Figure|Table) [\d.]+ below\.\)")
NFIG = NTAB = 0
for _ci, _ch in enumerate(CHS):
    _nf = _nt = 0
    _out = []
    for _b in _ch["lesson"]:
        if _b["type"] == "text":
            _b["items"] = [ANCHOR.sub("", it) for it in _b["items"]]
        if _b["type"] in ("figure", "table"):
            if _b["type"] == "figure":
                _nf += 1; _lab = "Figure %d.%d" % (_ci + 1, _nf); _b["caption"] = _lab + ". " + _b["caption"]
            else:
                _nt += 1; _lab = "Table %d.%d" % (_ci + 1, _nt); _b["title"] = _lab + ". " + _b["title"]
            for _p in reversed(_out):
                if _p["type"] == "text":
                    _p["items"][-1] = _p["items"][-1].rstrip() + " (See %s below.)" % _lab
                    break
        _out.append(_b)
    _ch["lesson"] = _out
    assert _nf >= 2 and _nt >= 2, (_ci + 1, _nf, _nt)
    NFIG += _nf; NTAB += _nt


def _split(t, lim=380):
    if len(t) <= lim:
        return [t]
    cuts = [m.end() for m in re.finditer(r"[.!?] (?=[A-Z(])", t)]
    if not cuts:
        return [t]
    k = min(cuts, key=lambda c: abs(c - len(t) / 2))
    return _split(t[:k].rstrip(), lim) + _split(t[k:], lim)


for _ch in CHS:
    for _b in _ch["lesson"]:
        if _b["type"] == "text":
            _b["items"] = [x for it in _b["items"] for x in _split(it)]

for _ch in CHS:
    _ch["summary"] = [x for it in _ch["summary"] for x in _split(it, 240)]

for _i in range(1, len(CHS)):
    _prev = CHS[_i - 1]
    CHS[_i]["lesson"].insert(0, T("Quick recap of the last chapter, " + _prev["title"] + ":", *["• " + k for k in _prev["keyPoints"]]))

MNEM = [
 ("Islands, decay, conflict, lock", "Four ways memory fails: Islands, Decay, Conflict, Lock-in: 'I D C L'."),
 ("V is truth, G is logic, M is feel", "Vault for people, Graph for logic, Manifold for feeling. Only V is precious."),
 ("Write, then rename", "Never save in place: write a temp file, then rename it. A note is whole or untouched."),
 ("Facts, rules, constraints", "Facts say, rules derive, constraints catch. Answers: proven, contradicted, unknown."),
 ("Text to point to neighbour", "Text becomes a vector, a vector becomes a neighbour. Nearness is not truth."),
 ("Two routes, one place", "Embed straight (phi) or extract then warp (f of pi). Delta is how far apart they land."),
 ("Far, shared, unlinked", "A bridge is Far in M, Shared in G, Unlinked in V."),
 ("Look, list, leave it", "The gardener Looks, Lists suggestions, and Leaves the decision to you."),
 ("Pull causes, push conflicts", "Lambda pulls causes closer, mu pushes conflicts apart. Change the ruler, not the map."),
 ("Seed, hop, drop, flag", "Retrieval: Seed, Hop, Drop the replaced, Flag the disputed."),
 ("Files are the memory", "Throw away G and M, replay from the files. Same facts, maybe new geometry."),
 ("Build, plant, measure", "Build on Jade parts, Plant known bridges and conflicts, Measure against plain search."),
]
assert len(MNEM) == len(CHS)
for _c, (_m, _d) in zip(CHS, MNEM):
    _full = _m + ". " + _d
    _c["lesson"].append(T("Memory trick: " + _full))
    _c["cards"].append({"q": "Memory trick for: " + _c["title"] + "?", "a": _full})
IMAGES = figs.build_all()

PRONOUNCE = {"CTMV": "C T M V", "sqlite-vec": "S Q L ite vec", "SQLite": "S Q L ite", "jade-kg": "jade K G", "Datalog": "data log", "WebAssembly": "web assembly",
  "k-NN": "K N N", "kNN": "K N N", "RAG": "rag", "vec0": "vec zero", "FTS5": "F T S five", "Ollama": "oh llama", "CozoDB": "cozo D B", "Wikilink": "wiki link",
  "wikilink": "wiki link", "wikilinks": "wiki links", "Wikilinks": "wiki links", "FNV-1a": "F N V one a", "Rust": "rust", "markdown": "mark down", "Markdown": "mark down",
  "φ": "phi", "π": "pi", "δ": "delta", "λ": "lambda", "μ": "mu", "∘": "composed with", "≅": "is about equal to", "≈": "is about equal to",
  "retry_storm": "retry storm", "positive_feedback": "positive feedback", "runaway_growth": "runaway growth", "Jade": "jade", "pre-version-1": "pre version one"}

SANDBOX = cmk.terminal("CTMV cheat sheet", "ctmv>", "A scripted lookup of the pieces, not the real engine. Try: note, claim, rule, constraint, query, verify, vec0, knn, delta, bridge, warp, replay, atomic", [
    ("note", ["# Retry storm", "tags: ops", "prose...", "- retry_storm causes overload", "See also [[circuit-breaker]]."]),
    ("claim", ["claim(NOTE, SUBJECT, RELATION, OBJECT).", "built from a dash line with three words"]),
    ("rule", ["leads_to(X, Z) :- claim(N, X, causes, Y), leads_to(Y, Z)."]),
    ("constraint", ["! cause_and_prevent: claim(N1, X, causes, Y), claim(N2, X, prevents, Y)."]),
    ("query", ["{op:'query', handle, q:'leads_to(retry_storm, X)'}", "answers: overload, outage"]),
    ("verify", ["{op:'verify', handle, claim:'leads_to(retry_storm, outage)'}", "PROVEN, with the facts and rules used"]),
    ("vec0", ["CREATE VIRTUAL TABLE v USING vec0(embedding float[64] distance_metric=cosine);"]),
    ("knn", ["SELECT rowid, distance FROM v WHERE embedding MATCH ? AND k = 4 ORDER BY distance;"]),
    ("delta", ["1 - |N_M(v) and N_G(v)| / |N_M(v) or N_G(v)|"]),
    ("bridge", ["shared in G, far in M, no link in V, different tags"]),
    ("warp", ["w = d * (1 - lambda) for a causal link", "w = d + mu for a conflict"]),
    ("replay", ["discard G and M; read the files; extract and embed; compare fact fingerprints"]),
    ("atomic", ["kit.vfs.write('/vault/.tmp', text); kit.vfs.move('/vault/.tmp', '/vault/note.md');"]),
])

EXAM = [
 ("Which is NOT one of the four failures?", ["A slow screen", "Islands", "Confident conflict", "Lock-in"], 0, "The four are islands, decay, conflict and lock-in."),
 ("What does V stand for?", ["Vault", "Vector", "Verdict", "Version"], 0, "Markdown files."),
 ("What does G stand for?", ["Graph", "Gain", "Guess", "Group"], 0, "Facts and rules."),
 ("What does M stand for?", ["Manifold", "Memory", "Model", "Matrix"], 0, "Vectors in a space."),
 ("Which view is the source of truth?", ["V", "G", "M", "A cache"], 0, "The files."),
 ("Which views can be rebuilt?", ["G and M", "V only", "None", "All but G"], 0, "From V."),
 ("What is a claim line here?", ["A dash line with three words", "A heading", "A tag", "A link"], 0, "Subject relation object."),
 ("How is a link written?", ["[[name]]", "{name}", "<<name>>", "@name"], 0, "A wikilink."),
 ("Why write a temp file then rename?", ["So a note is never half-written", "It is shorter", "To encrypt", "To sort"], 0, "Atomic."),
 ("What does a Datalog rule do?", ["Derives new facts", "Deletes facts", "Embeds text", "Formats notes"], 0, "If-then."),
 ("What does a constraint do?", ["Catches contradictions", "Adds notes", "Hides facts", "Speeds search"], 0, "Any match is a problem."),
 ("What does unknown mean?", ["Nothing says either way", "False", "True", "Error"], 0, "Open world."),
 ("What does a proof show?", ["Facts and rules used", "A picture", "A time", "A score"], 0, "Nothing hidden."),
 ("What does a variable begin with?", ["A capital letter", "A digit", "A dash", "A hash"], 0, "X, Y, Z."),
 ("What does M store per note?", ["A vector", "A proof", "A password", "A link"], 0, "A position."),
 ("What does cosine distance 0 mean?", ["Same direction", "Opposite", "Unrelated", "Missing"], 0, "As close as possible."),
 ("What does k-NN return?", ["The k closest items", "The k oldest", "The k longest", "Random"], 0, "Nearest neighbours."),
 ("Why a toy embedder in the labs?", ["Offline and repeatable", "Most accurate", "Fastest ever", "Secret"], 0, "No model needed."),
 ("Which extension stores vectors in SQLite here?", ["sqlite-vec", "pgvector", "Lucene", "Redis"], 0, "From the kit."),
 ("What is sqlite-vec's maturity?", ["Pre-version-1", "Finished and frozen", "Abandoned", "Closed source"], 0, "Interfaces may change."),
 ("What is phi?", ["Embed text into M", "Extract facts", "Warp distances", "Write files"], 0, "Direct route."),
 ("What is pi?", ["Extract facts from V", "Embed", "Warp", "Delete"], 0, "Text to facts."),
 ("What is f?", ["Uses facts to adjust geometry", "A file", "A format", "A function name only"], 0, "Warp and anchor."),
 ("What is delta?", ["Disagreement between the two routes", "A note count", "A file size", "A model"], 0, "Commutativity error."),
 ("What does a high delta suggest?", ["A clue to look closer", "A crash", "Nothing", "A deleted file"], 0, "Bridge, false friend or missing fact."),
 ("Which describes a bridge?", ["Shared in G, far in M, unlinked in V", "Same words", "A link in V", "Same tag"], 0, "Same pattern, other words."),
 ("Which describes a false friend?", ["Near in M, nothing shared in G", "Far in M, shared in G", "Linked", "Orphan"], 0, "Similar words, other meaning."),
 ("Who decides to keep a bridge?", ["The person", "SQLite", "The embedder", "Nobody"], 0, "Engine suggests."),
 ("What is a gap?", ["An idea in several notes with no note of its own", "An empty file", "A short note", "A bug"], 0, "A concept without a home."),
 ("What is an orphan?", ["A note nothing links to", "A note with tags", "A long note", "A new note"], 0, "No links in or out."),
 ("What does the gardener do?", ["Suggests, never rewrites", "Deletes", "Edits silently", "Emails"], 0, "Your notes stay yours."),
 ("What does lambda do?", ["Pulls causal neighbours closer", "Pushes conflicts", "Sets k", "Deletes"], 0, "Shrinks distance."),
 ("What does mu do?", ["Adds distance for conflicts", "Removes links", "Embeds", "Counts"], 0, "Pushes apart."),
 ("Do vectors move when warping?", ["No, only the ruler", "Yes", "Only some", "Only conflicts"], 0, "A view, not an edit."),
 ("What do lambda 0 and mu 0 give?", ["Plain search", "No results", "Errors", "Random"], 0, "Warping off."),
 ("What is a seed in retrieval?", ["The nearest note to the question", "The newest note", "A random note", "A tag"], 0, "Where expansion starts."),
 ("What happens to a replaced note?", ["Dropped from results", "Deleted from V", "Flagged only", "Moved"], 0, "A newer note supersedes it."),
 ("What happens to a disputed pair?", ["Flagged, not hidden", "Silently dropped", "Merged", "Edited"], 0, "No winner yet."),
 ("What does replay rebuild?", ["G and M from the files", "The files", "The model", "The OS"], 0, "Derived views."),
 ("What changes with a new embedder?", ["M only", "V", "G", "Everything"], 0, "Facts stay."),
 ("What shows a replay was faithful?", ["Equal fact fingerprints", "A faster run", "More notes", "A new tag"], 0, "Same facts."),
 ("Which licence covers Jade Agent Kit?", ["MIT", "GPL", "Proprietary", "None"], 0, "Open source."),
 ("What is still a toy in the labs?", ["The embedder", "The reasoner", "SQLite", "The file system"], 0, "Hashing."),
 ("Is CTMV proven by this course?", ["No, it needs measuring", "Yes", "Always", "Only on Android"], 0, "A design, not a result."),
 ("How would you test it?", ["Plant bridges and conflicts, then measure", "Trust it", "Read the logo", "Guess"], 0, "Evaluation."),
]
print("exam", len(EXAM))

CFG = dict(id="ctmv-vault", title="The Commutative Tri-Modal Vault: Memory That Reasons",
    subtitle="Markdown notes, a fact graph and a vector space kept consistent: bridges, gardening, contradiction-aware retrieval and memory you can replay",
    description="A beginner-friendly course on the Commutative Tri-Modal Vault (CTMV), a design for personal knowledge bases and AI memory that answers four failures: related ideas that never meet, collections that decay, old and new facts that both come back, and memory locked to one model. "
    "In 12 chapters you learn the three views of one vault (V markdown files, G facts and rules with proofs, M vectors), the commuting square and its error delta, cross-domain bridges, gap and contradiction gardening, metric warping, multi-hop retrieval that drops replaced notes and flags disputes, and replayable, model-agnostic memory. "
    "Four hands-on labs run in the app, offline, on real components: the Jade Agent Kit's SQLite with sqlite-vec and file system, and the Jade Vault's Datalog reasoner (jade-kg); only the text embedder is a small toy so results repeat. A few short Python labs run on the app's MicroPython. "
    "There are 24 numbered figures, numbered tables, a recap, a memory trick, an expanded ELI5 and a concept map in every chapter, a cheat sheet in the sandbox and a final exam. "
    "Credits: the CTMV concept follows the description supplied by the course requester; the text and code here are original. Labs use Jade Agent Kit (MIT), Jade Vault jade-kg (MIT), SQLite (public domain) and sqlite-vec by Alex Garcia (MIT or Apache-2.0). CTMV is a design to understand and test, not a proven product.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, images=IMAGES)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "ctmv-vault.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
    print("figures", NFIG, "tables", NTAB)
