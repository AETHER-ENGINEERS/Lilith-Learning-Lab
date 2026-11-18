# -*- coding: utf-8 -*-
"""CTMV course, chapters 1-6."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *  # noqa
def F(n, cap): return {"type": "figure", "image": "ct-%s.svg" % n, "caption": cap}
def TB(title, head, rows): return {"type": "table", "title": title, "head": head, "rows": rows}
CHS = []

CHS.append(CH("The problem: four ways a pile of notes fails",
 ("Four failures", ["Notes | suffer | Islands", "Notes | suffer | Decay", "Notes | suffer | Conflict", "Memory | suffers | Lock-in", "CTMV | answers | Islands", "CTMV | answers | Decay", "CTMV | answers | Conflict", "CTMV | answers | Lock-in"]),
 ["A personal knowledge base, a vector database and an AI assistant's memory all store things. They all fail in the same four ways. Ideas from different fields never meet. The collection decays without anyone noticing. Old and new facts disagree and both come back. And the memory is welded to one model.",
  "The Commutative Tri-Modal Vault, or CTMV, is a design that keeps three views of the same notes: files, facts and geometry. It tries to answer each failure with something the three views can do together.",
  "This course builds the idea step by step, and in the labs you run a small but real version made from parts of the Jade projects. It is a design to understand and test, not a finished product with proven results."],
 [("CTMV", "Commutative Tri-Modal Vault: markdown notes plus a fact graph plus a vector space that are kept consistent."), ("Knowledge base", "A collection of notes you keep to remember and think."), ("Vector database", "A store that finds items by closeness of their number lists."), ("RAG", "Retrieval-augmented generation: look up notes, then let a model answer using them."), ("Lock-in", "Being unable to leave a tool or model without losing your data's value.")],
 ["Plain search finds similar words, not shared ideas.", "Collections rot: gaps, orphans and stale notes pile up.", "Retrieval can return an old note and its correction side by side.", "Memory tied to one embedding model is stranded when the model changes.", "CTMV is a design; this course tests it with small real parts."],
 [T("Imagine a big drawer of notes. You wrote a note about overloaded web servers, and years later another about microphone feedback. They are the same pattern, a loop that feeds itself, but the words are different, so a search never connects them. That is failure one."),
  F("1-1", "The four failures in one line."),
  T("Failure two is quiet. Nobody tells you that an idea appears in five notes but has no note of its own, or that two notes quietly contradict each other. Failure three hurts most with AI helpers: when a note says one thing in 2023 and its replacement says the opposite in 2024, a plain search may hand both to the model, and it answers with confidence."),
  TB("The four failures", ["Failure", "What you see", "What CTMV tries"], [["isolated islands", "related ideas in different fields never meet", "bridges: shared idea, no link"], ["silent decay", "gaps, orphans, unlinked pairs", "a gardener that suggests fixes"], ["confident conflict", "old and new facts both retrieved", "warped, contradiction-aware retrieval"], ["lock-in", "memory tied to one model or tool", "plain files you can replay"]]),
  F("1-2", "Plain search stores; the goal is an engine that also reasons."),
  TB("Where each tool falls short", ["Tool", "Good at", "Weak at"], [["folder of notes", "being readable and yours", "finding anything by meaning"], ["keyword search", "exact words", "ideas written in other words"], ["vector database", "similar meaning", "logic, conflict, explanations"], ["AI memory", "convenience", "inspection, portability, correction"]]),
  T("In the labs you will not need a big model or the internet. You will use pieces from the Jade projects: a small SQLite database with a vector search extension, and a reasoner that answers questions with proofs. A toy text hashing function stands in for the language model, so every result is repeatable.")],
 [("What is failure one in this course?", ["Related ideas in different fields never meet", "The disk is full", "Notes are too long", "Search is slow"], 0, "Islands: no shared words, so no connection."), ("Why is a conflict dangerous for an AI helper?", ["It may answer confidently from the old note", "It refuses to answer", "It deletes notes", "It runs slowly"], 0, "Both notes come back and the model has to guess."), ("What is CTMV?", ["A design with three consistent views of notes", "A single database", "A chat app", "A model"], 0, "Files, facts and geometry."), ("Is CTMV a proven product?", ["No, it is a design to test", "Yes, fully benchmarked", "It is a law", "It is a library"], 0, "The course says so openly.")],
 [("Name the four failures.", "Islands, decay, confident conflict, lock-in."), ("Why can plain search miss a connection?", "It compares wording, not shared ideas."), ("What do the labs use instead of a language model?", "A toy hashing embedder, so results repeat."), ("What are the labs built from?", "Jade Agent Kit SQLite with sqlite-vec, and the Jade Vault reasoner.")],
 [MATCH("Match failure and symptom", "Pair each failure with what you notice.", [("islands", "related ideas never meet"), ("decay", "gaps and orphans pile up"), ("conflict", "old and new both returned"), ("lock-in", "stuck with one model")]),
  FILL("The goal", "A passive archive only {{stores}}; CTMV tries to also {{reason}} about what it stores.")]))

CHS.append(CH("One idea, three modalities: V, G and M",
 ("Three views", ["Vault V | holds | Markdown files", "Graph G | holds | Facts and rules", "Manifold M | holds | Vectors", "G | is built from | V", "M | is built from | V", "V | is | The truth", "Each view | covers | The others' gaps"]),
 ["CTMV keeps every note in three forms. V is the vault: plain markdown files. G is the graph: facts and rules that can be checked. M is the manifold: a vector for each note, so you can ask which notes are near each other.",
  "V is the truth; G and M are built from it and can be rebuilt at any time. This is what makes the system inspectable. Each view is strong where another is weak, so the combination can do things none of them can alone.",
  "The word commutative in the name is a promise about consistency, which chapter 6 explains with a diagram."],
 [("V", "The vault: markdown notes on disk."), ("G", "The graph: facts, rules and constraints, answered with proofs."), ("M", "The manifold: one vector per note in a space where closeness means similar meaning."), ("Modality", "One way of representing the same knowledge."), ("Source of truth", "The one copy that wins when copies disagree.")],
 ["V, G and M are three views of the same notes.", "V is the source of truth; G and M are rebuildable.", "G is exact and explains itself; M is fuzzy and fast.", "Together they find connections neither finds alone."],
 [T("Think of one town seen three ways. A photograph shows what it looks like. A street map shows exactly which road joins which. A list of distances tells you what is near what. Each answers different questions, and all three describe the same town."),
  F("2-1", "Only the bottom of the stack is precious; the others can be recreated."),
  TB("The three modalities", ["View", "Made of", "Answers", "Cannot do"], [["V vault", "markdown files", "what did I write?", "reason or compare by itself"], ["G graph", "facts, rules, constraints", "does A lead to B? is anything contradictory?", "guess when facts are missing"], ["M manifold", "one vector per note", "which notes feel alike?", "explain why, or tell cause from similarity"]]),
  T("A useful way to remember it: V is for people, G is for logic, M is for feeling. People can read V. Logic can prove things in G. And M gives a sense of nearness that logic alone does not have."),
  F("2-2", "Each view makes up for what the others lack."),
  TB("A tiny example, three ways", ["View", "What it holds for the note called retry-storm"], [["V", "the markdown file with its text, tags and claim lines"], ["G", "claim(retry-storm, retry_storm, causes, overload) and more"], ["M", "a vector of 64 numbers; its nearest neighbours are other notes"]]),
  T("In the labs, the vault sits in the Jade Agent Kit's in-memory file system, G is the Jade Vault reasoner, and M is a SQLite table with the sqlite-vec extension. They are real components, small enough to run in a page.")],
 [("Which view is the source of truth?", ["V, the vault", "G, the graph", "M, the manifold", "None"], 0, "Files win."), ("Which view finds nearness?", ["M", "G", "V", "None"], 0, "Vectors measure closeness."), ("Which view gives proofs?", ["G", "M", "V", "None"], 0, "Facts and rules."), ("What happens if M is deleted?", ["It is rebuilt from V", "All is lost", "G breaks", "V changes"], 0, "It is a cache.")],
 [("What do V, G and M stand for?", "Vault, Graph, Manifold."), ("Which can be rebuilt?", "G and M, from V."), ("Why three views?", "Each is strong where another is weak."), ("What is G's weakness?", "It cannot guess; missing is unknown.")],
 [MATCH("Match view and strength", "Pair each view with what it is best at.", [("V", "readable and portable"), ("G", "exact proofs"), ("M", "nearness by meaning"), ("all three", "covering each other's gaps")]),
  ORDER("Order by trust", "Put the views from most trusted source to most rebuildable.", ["V vault", "G graph", "M manifold"])]))

CHS.append(CH("V: the markdown vault",
 ("The vault", ["Note | has | Heading", "Note | has | Tags", "Note | has | Claim lines", "Note | has | Wikilinks", "Write | uses | Rename", "File system | keeps | Notes", "G and M | read | Notes"]),
 ["The vault is a folder of markdown files. A note has a heading, a line of tags, some prose, and optionally claim lines and links to other notes. Plain text means you can read it, back it up, search it with any tool and keep it for decades.",
  "For the machine to reason about a note, the course uses one simple convention: a line that starts with a dash and has exactly three words is a claim, in the order subject, relation, object. Links are written in double square brackets.",
  "Writes are atomic: write a temporary file, then rename it over the note. Then a power cut can never leave half a note."],
 [("Markdown", "A plain text format with simple marks such as hash for headings."), ("Claim line", "A line like - retry_storm causes overload that the extractor turns into a fact."), ("Wikilink", "A link written as [[note-name]]."), ("Atomic write", "A write that either fully happens or not at all."), ("Virtual file system", "A file system that lives in memory or in a page, such as the Jade Agent Kit's.")],
 ["A note is heading, tags, prose, claim lines and links.", "A claim line has three words: subject relation object.", "Links are [[name]].", "Write a temporary file and rename it so a note is never half-written."],
 [T("The vault has to be boring on purpose. If your memory is stored in a format that only one program can read, you lose it when that program goes away. A folder of text files will outlive almost every tool."),
  F("3-1", "The parts of a note. Only the claim lines carry formal meaning."),
  C("# Retry storm\ntags: ops\nAfter a hiccup every client retries at once; the extra load keeps the service down.\n- retry_storm is positive_feedback\n- retry_storm causes overload\n- overload causes outage\nSee also [[circuit-breaker]].", "markdown"),
  TB("Reading a note", ["Piece", "How the tool reads it"], [["# Retry storm", "the title"], ["tags: ops", "the area, used to tell fields apart"], ["prose", "text that feeds the embedding"], ["- a causes b", "three words become a fact"], ["[[circuit-breaker]]", "an explicit link between notes"]]),
  T("Why such a plain convention? Because extracting meaning from free text needs a language model, and the first goal is something you can inspect. Later, a model can propose claim lines for you to approve; the Jade Vault does exactly this, marking facts as proposed until you confirm them."),
  F("3-2", "Write then rename."),
  C("// the Jade Agent Kit's file system\nkit.vfs.write('/vault/.tmp-note', text);\nkit.vfs.move('/vault/.tmp-note', '/vault/note.md');", "js"),
  TB("Good habits for a vault", ["Habit", "Reason"], [["one idea per note", "easier to link and compare"], ["use the same word for the same thing", "retry_storm, not retry storm and retries"], ["date things that may change", "so a newer note can replace an older one"], ["never store only in G or M", "they are rebuilt from the files"]])],
 [("How many words does a claim line have in this course?", ["Three", "One", "Five", "Any"], 0, "Subject, relation, object."), ("How is a link written?", ["[[name]]", "<name>", "(name)", "#name"], 0, "A wikilink."), ("Why write a temp file first?", ["So a note is never half-written", "To make it faster", "To hide it", "To compress it"], 0, "Rename is atomic."), ("Why plain text?", ["It outlives tools", "It is smaller", "It is encrypted", "It is private"], 0, "Any program can read it.")],
 [("What is a claim line?", "A dash line with subject, relation, object."), ("What do tags do?", "They name the area of a note."), ("What is atomic writing?", "Write temp, then rename."), ("Where do the labs keep the vault?", "In the kit's in-memory file system.")],
 [FILL("A safe write", "Write a {{temporary}} file and then {{rename}} it over the note."),
  MATCH("Match note piece", "Pair each piece with its role.", [("# heading", "the title"), ("tags:", "the area"), ("- a causes b", "a fact"), ("[[x]]", "a link")]),
  PL("Read the claim lines", "Write parse_claims(text). Return a list of [subject, relation, object] for every line that starts with a dash and a space and has exactly three words after it. Keep the order.", "parse_claims(text)", '''
def parse_claims(text):
    out = []
    for line in text.split("\\n"):
        if line.startswith("- "):
            words = line[2:].split()
            if len(words) == 3:
                out.append(words)
    return out
''', [["# Note\n- a causes b\nsome prose\n- c prevents d"], ["- only two"], ["- x is y\n- p q r s"], [""]], "Loop over the lines. Check the start, split the rest, and count the words.")]))

CHS.append(CH("G: facts, rules and proofs",
 ("The graph", ["Claim line | becomes | Fact", "Rules | derive | New facts", "Constraints | catch | Contradictions", "Query | asks | Questions", "Verify | returns | Verdict", "Proof | names | Facts used", "Open world | means | Unknown is allowed"]),
 ["G is a small logic engine. Every claim line becomes a fact. Rules say what follows from facts, for example that a cause of a cause is also a cause further along. Constraints say what must never happen, for example that the same thing may not both cause and prevent the same outcome.",
  "The engine in the labs is the Jade Vault's knowledge reasoner, written in Rust and run as WebAssembly. It speaks a Datalog-style language, answers questions with variables, verifies claims, and shows a proof listing every fact and rule it used.",
  "It is an open world: if nothing is known, the answer is unknown, not false. This is the opposite of a database that treats missing as no."],
 [("Fact", "One statement such as claim(note, a, causes, b)."), ("Rule", "If these facts hold, then this new fact holds."), ("Constraint", "A pattern that must never match; any match is a contradiction."), ("Datalog", "A small logic language with facts, rules and variables that begin with capitals."), ("Proof", "The chain of facts and rules behind an answer.")],
 ["Claim lines become facts.", "Rules derive new facts; constraints catch contradictions.", "Verdicts: proven, contradicted, unknown.", "Proofs name every fact used.", "Open world: missing is unknown, not false."],
 [T("Here is the idea in a story. You tell a very careful librarian: retry storms cause overload, and overload causes outage. You then ask, does a retry storm lead to an outage? The librarian does not guess. She points to your two statements and the rule that chains them."),
  F("4-1", "From a claim line to an answer that shows its proof."),
  C("% a rule: a chain of causes\nleads_to(X, Y) :- claim(N, X, causes, Y).\nleads_to(X, Z) :- claim(N, X, causes, Y), leads_to(Y, Z).\n\n% a constraint: a thing must not both cause and prevent the same outcome\n! cause_and_prevent: claim(N1, X, causes, Y), claim(N2, X, prevents, Y).", "text"),
  T("Capital letters are variables, which stand for anything. The first rule says that any claim of the form X causes Y means X leads to Y. The second says if X causes Y and Y leads to Z, then X leads to Z. The line starting with an exclamation mark is a constraint. In the labs this reasoner shows ✓ PROVEN, with the exact facts it rested on."),
  TB("What you can ask G", ["Question", "Example", "Answer"], [["query", "leads_to(retry_storm, X)", "every X that follows"], ["verify", "leads_to(retry_storm, outage)", "proven, contradicted or unknown"], ["why", "show the proof of one fact", "facts and rules, step by step"], ["check", "any constraint broken?", "the list of contradictions"]]),
  F("4-2", "The engine says unknown when it does not know."),
  TB("The three verdicts", ["Verdict", "Meaning"], [["proven", "facts and rules show it"], ["contradicted", "the opposite holds, or it would break a constraint"], ["unknown", "nothing says either way"]]),
  T("The honest limit: G is only as good as the claims written in V. It does no arithmetic beyond comparisons and no probabilities. Its strength is exactness and explanation, not guessing.")],
 [("What does a rule do?", ["Derives new facts from known ones", "Deletes notes", "Draws charts", "Embeds text"], 0, "If these hold, then that holds."), ("What does unknown mean?", ["Nothing says either way", "False", "True", "An error"], 0, "Open world."), ("What is a constraint for?", ["Catching contradictions", "Speeding up", "Storing vectors", "Formatting"], 0, "Any match is a problem."), ("What does a proof show?", ["The facts and rules used", "A picture", "A score", "The time"], 0, "Nothing is hidden.")],
 [("What is a variable in Datalog?", "A name beginning with a capital letter."), ("What is the open-world idea?", "Missing is unknown, not false."), ("What engine do the labs use?", "The Jade Vault reasoner, as WebAssembly."), ("Where do facts come from?", "Claim lines in the notes.")],
 [MATCH("Match the verdict", "Pair each situation with the verdict.", [("facts show it", "proven"), ("the opposite holds", "contradicted"), ("nothing known", "unknown")]),
  FILL("Facts and logic", "Claim lines become {{facts}}; {{rules}} derive more; {{constraints}} catch contradictions.")]))

CHS.append(CH("M: the manifold of meaning",
 ("The manifold", ["Note text | becomes | Vector", "Vector | lives in | Manifold", "Close vectors | mean | Similar notes", "sqlite-vec | stores | Vectors", "k-NN | finds | Neighbours", "Embedder | can be | Swapped", "Hashing | stands in for | A model"]),
 ["M gives every note a point in a space, a list of numbers called a vector. Notes with similar meaning should end up near each other, so you can ask for the nearest neighbours of a note or of a question. This is what vector databases do.",
  "In real use an embedding model turns text into the numbers. In the labs, a small hashing function does it, so everything runs offline and gives the same numbers every time. It is crude: it mostly notices shared words and word parts, not deep meaning.",
  "The labs store vectors in SQLite using the sqlite-vec extension, from the Jade Agent Kit, and ask it for the nearest ones. Distance here is cosine distance: zero means the same direction, bigger means further apart."],
 [("Vector", "A list of numbers that describes a note's position."), ("Embedding", "Turning text into a vector."), ("k-NN", "k nearest neighbours: the k closest items to a point."), ("Cosine distance", "One minus the cosine of the angle between two vectors."), ("sqlite-vec", "A SQLite extension that stores vectors and finds nearest ones; it is still pre-version-1 software.")],
 ["M places each note as a vector; nearby means similar.", "The labs use a hashing toy embedder for repeatable results.", "sqlite-vec stores vectors and finds nearest neighbours.", "Swapping the embedder changes M and nothing else."],
 [T("Picture a map of a library where books about similar topics sit close together, even if their titles share no words. The map is not the library; it is a way to find your way around. M is that map, computed by a function that you can replace."),
  F("5-1", "How the toy embedder makes a vector. A real model replaces the middle steps."),
  C("CREATE VIRTUAL TABLE notes_vec USING vec0(\n  embedding float[64] distance_metric=cosine);\n\nSELECT rowid, distance FROM notes_vec\n WHERE embedding MATCH ? AND k = 4\n ORDER BY distance;", "sql"),
  TB("Terms about M", ["Term", "In plain words"], [["embedding size", "how many numbers per note (64 in the labs)"], ["cosine distance", "0 = same direction, 1 = unrelated, up to 2 = opposite"], ["k", "how many neighbours to return"], ["vec0", "the sqlite-vec table type"]]),
  F("5-2", "The toy and the real thing have the same shape."),
  TB("Toy versus real embedder", ["Property", "Toy hashing", "Real model"], [["needs internet or model", "no", "yes or a local model"], ["repeatable", "always", "usually, per model version"], ["understands meaning", "barely", "much better"], ["can be swapped later", "yes", "yes, then M is rebuilt"]]),
  T("A caution that matters: the nearest vector is not necessarily the right answer. Nearness measures similarity of wording or topic. It cannot tell cause from effect, old from new, or agreement from contradiction. That is what G and the next chapters add.")],
 [("What does M store?", ["A vector per note", "Proofs", "Passwords", "Images only"], 0, "Positions in space."), ("What does cosine distance 0 mean?", ["Same direction", "Opposite", "Unrelated", "Error"], 0, "As close as possible."), ("Why use a hashing embedder in labs?", ["Offline and repeatable", "It is the most accurate", "It is secret", "It is faster than anything"], 0, "No model is needed."), ("Can M tell old from new?", ["No", "Yes", "Always", "Only in SQLite"], 0, "Nearness is not time or truth.")],
 [("What is k-NN?", "The k nearest neighbours."), ("What stores vectors in the labs?", "SQLite with sqlite-vec."), ("What changes if you swap the embedder?", "Only M."), ("Can nearness tell contradiction?", "No.")],
 [ORDER("Order the embedding steps", "Put the toy embedder's steps in order.", ["take the note text", "split into word parts", "hash into slots", "scale to length one", "store in vec0"]),
  MATCH("Match term", "Pair each term with its meaning.", [("vector", "list of numbers"), ("k-NN", "closest items"), ("cosine distance", "0 means same direction"), ("sqlite-vec", "SQLite vector extension")])]))

CHS.append(CH("The commuting square and the error δ",
 ("Commutation", ["V | goes to G by | Extract pi", "V | goes to M by | Embed phi", "G | goes to M by | Warp f", "Two routes | should | Agree", "Disagreement | is measured by | delta", "High delta | is | A clue"]),
 ["There are two ways to get from a note to a place in the manifold. One goes straight: embed the text, which is φ. The other goes through logic: extract facts, which is π, and then use them to warp and anchor the geometry, which is f. If the two routes agree, the picture commutes.",
  "The formula f∘π(v) ≅ φ(v) says that going through the facts lands near going straight. The error δ(v) measures how far apart the two routes end up for a note v.",
  "In practice, no model is perfect, so δ is never zero everywhere. That is useful. Where the routes disagree, something interesting is happening: a hidden connection, a misleading resemblance, or a fact nobody wrote down."],
 [("π (extract)", "The map from V to G: from text to facts."), ("φ (embed)", "The map from V to M: from text to a vector."), ("f (warp and anchor)", "The map from G into M: using facts to adjust distances and positions."), ("Commutative", "Different routes to the same place give the same result."), ("δ", "The commutativity error: how much the two routes disagree for a note.")],
 ["Two routes: embed directly, or extract facts and warp.", "The square commutes if both routes meet.", "δ measures disagreement per note.", "High δ is a clue, not necessarily an error."],
 [T("Consider two friends finding a restaurant. One follows the map, one follows the smell of food. If both arrive at the same door, the map and the nose agree. If they end up on different streets, one of them knows something the other does not. δ is how far apart the two friends end up."),
  F("6-1", "The two routes from a note to the manifold."),
  M("f(\\pi(v)) \\approx \\varphi(v), \\qquad \\delta(v) = \\operatorname{disagreement}\\bigl(f(\\pi(v)),\\ \\varphi(v)\\bigr)"),
  T("There are many ways to measure disagreement. The labs use a simple, easy-to-read one that compares neighbourhoods rather than exact positions: take the note's nearest neighbours in M, take its neighbours according to G and V, and measure how much the two sets overlap."),
  M("\\delta(v) = 1 - \\frac{|N_M(v) \\cap N_G(v)|}{|N_M(v) \\cup N_G(v)|}"),
  TB("Reading δ", ["δ", "Meaning", "Likely reason"], [["near 0", "the views agree", "wording and logic match"], ["middle", "partial agreement", "some shared words, some shared facts"], ["near 1", "the views disagree", "a bridge, a false friend or a missing fact"]]),
  F("6-2", "High δ is where to look."),
  TB("What the neighbour sets are", ["Set", "Built from"], [["N_M(v)", "the k nearest notes by cosine distance in sqlite-vec"], ["N_G(v)", "notes that share an idea with v in G, or are linked from V"]]),
  T("The word anchoring in f means pinning points: if G says two notes are about the same thing, f can pull them toward each other, and if G says they contradict, f can push them apart. The next chapters use this idea without moving any vectors, by changing the ruler instead.")],
 [("What is φ?", ["Embed text into M", "Extract facts", "Warp distances", "Write files"], 0, "Direct route."), ("What is π?", ["Extract facts from V", "Embed", "Search", "Compress"], 0, "Text to facts."), ("What does a high δ mean?", ["The views disagree", "The system crashed", "The note is long", "Nothing"], 0, "It is a clue."), ("What does commute mean here?", ["Both routes end at the same place", "Travel to work", "Swap files", "Sort"], 0, "Same result either way.")],
 [("What is the formula?", "f of pi of v is about phi of v."), ("What does the lab use for δ?", "One minus the overlap of two neighbour sets."), ("Is high δ an error?", "No, a clue."), ("What does f do?", "Uses facts to adjust distances or positions.")],
 [MATCH("Match symbol", "Pair each symbol with its meaning.", [("π", "extract facts"), ("φ", "embed text"), ("f", "warp using facts"), ("δ", "disagreement")]),
  PL("Compute δ", "Write overlap_delta(geo, sym). geo and sym are lists of note names. Return 1 minus the size of the overlap divided by the size of the union, rounded to 2 decimals. If both lists are empty return 0.", "overlap_delta(geo, sym)", '''
def overlap_delta(geo, sym):
    a = set(geo)
    b = set(sym)
    union = a | b
    if not union:
        return 0
    return round(1 - len(a & b) / len(union), 2)
''', [[["a", "b", "c"], ["a", "b", "c"]], [["a", "b"], ["c"]], [["a", "b", "c"], ["b", "c", "d"]], [[], []], [["x"], []]], "Use sets: the overlap is the intersection, the union is both together.")]))
