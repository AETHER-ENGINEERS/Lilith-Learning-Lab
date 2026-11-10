#!/usr/bin/env python3
"""Build the Jade Vault course. Usage: python3 make_jadevault_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "jvc"))
import cmk, jv1, jv2  # noqa: E402

PRONOUNCE = {
    "Jade": "jade", "Ollama": "oh lah mah", "Ollaya": "oh lye uh", "MCP": "M C P", "BM25": "B M twenty five", "RRF": "R R F", "SQLite": "S Q L ite", "FTS5": "F T S five",
    "webxdc": "web X D C", "Vector": "vector", "Sentry": "sentry", "playbook": "play book", "Playbook": "play book", "playbooks": "play books", "Playbooks": "play books", "Datalog": "data log",
    "WebGPU": "web G P U", "LiteRT": "lite R T", "ONNX": "onyx", "ELI5": "E L I five", "IndexedDB": "indexed D B", "Obsidian": "obsidian", "Templater": "templater", "Dataview": "data view",
    "OpenRouter": "open router", "Groq": "grok", "SSH": "S S H", "JSON": "jason", "YAML": "yam ul", "PBKDF2": "P B K D F two", "AES": "A E S", "GCM": "G C M", "WebAssembly": "web assembly",
    "Rust": "rust", "Lisp": "lisp", "Scheme": "scheme", "Clojure": "clo zhure", "defmacro": "def macro", "quasiquote": "kwazi quote", "Gantt": "gant", "GAE": "G A E", "PUCT": "puct",
    "Playwright": "play right", "Chromium": "chromium", "BusyBox": "busy box", "cron": "kron", "Ansible": "an sib ul", "n8n": "N eight N", "SHA-256": "S H A two fifty six", "FNV-1a": "F N V one A",
    "APK": "A P K", "HTTP": "H T T P", "API": "A P I", "URL": "U R L", "CORS": "cors", "Discord": "discord", "Markdown": "mark down", "markdown": "mark down", "JDK": "J D K", "SDK": "S D K",
    "LLM": "L L M", "AI": "A I", "DSL": "D S L", "STATUS": "status", "HEARTBEAT": "heart beat", "SOUL": "soul", "AGENTS": "agents", "SYSTEM": "system", "jade": "jade", "TensorFlow": "tensor flow",
    "Fleet": "fleet", "kv": "K V", "jq": "J Q", "sqlite-vec": "S Q L ite vec", "sha256": "S H A two fifty six", "vault": "vault", "Loci": "low sigh", "Link": "link",
}

SANDBOX = cmk.terminal("Jade cheat sheet", "jade>", "A scripted lookup, not a real program. Try: vault, turn, tools, memory, skills, flows, playbook, knowledge, lisp, backup", [
    ("vault", ["Notes are markdown files; [[links]] and #tags connect them", "Browser: IndexedDB. Android: the JadeVault folder"]),
    ("turn", ["compact, prefetch, build request, fit context, call model, run tools, repeat", "maxTurns limits tool rounds; send continue to go on"]),
    ("tools", ["Switches decide which tools the model sees", "Secrets are {{NAME}} placeholders filled outside the model"]),
    ("memory", ["/Jade/Memory.md and a journal per day", "Hybrid search: keywords plus vectors, merged by reciprocal rank fusion"]),
    ("skills", ["/Jade/skills/NAME/SKILL.md with name and description", "15 or fewer are all listed; more are routed to the best few"]),
    ("flows", ["/Jade/Flows/NAME.flow.json; each step's output is $json", "Retries 0 to 3, or continue on error"]),
    ("playbook", ["JSON tasks, no model; when, loop, register, rescue", "Approved by hash; a change needs approving again"]),
    ("knowledge", ["Facts, Datalog rules, constraints", "Proven, contradicted or unknown (open world)"]),
    ("lisp", ["(tool/NAME :arg value) calls any tool", "fuel=N limits steps; pure=yes runs with no tools"]),
    ("backup", ["JSON, gzip, optional AES-GCM with PBKDF2", "Jade can start a backup but never restore one"]),
])

EXAM = [
 ("What is Jade Vault, in short?", ["A markdown vault with an AI agent", "A password manager", "A web browser", "A game engine"], 0, "Notes plus an agent."),
 ("Where does the browser version keep the vault?", ["IndexedDB", "A cloud drive", "A USB stick", "The model"], 0, "A virtual file system."),
 ("Where does the Android app keep it?", ["The JadeVault folder", "Only in RAM", "A server", "The cache"], 0, "Real files."),
 ("Is the model part of the app?", ["No, you connect one", "Yes, built in", "Only on Android", "Only offline"], 0, "Ollama, Groq and others."),
 ("What do [[double brackets]] make?", ["A link between notes", "A tag", "A secret", "A heading"], 0, "Backlinks follow."),
 ("What is the first step of a turn?", ["Compact old turns", "Call the model", "Run tools", "Save memory"], 0, "Make room first."),
 ("What does maxTurns limit?", ["Tool rounds in a reply", "Chats", "Notes", "Model size"], 0, "Then you say continue."),
 ("How is external text treated?", ["Labelled as data", "As instructions", "Deleted", "Trusted"], 0, "Against injection."),
 ("How do secrets reach a tool?", ["As {{NAME}} placeholders filled outside the model", "Pasted into the prompt", "Spoken aloud", "Stored in notes"], 0, "The model never sees them."),
 ("Who may restore a backup?", ["Only you", "Jade", "A flow", "A schedule"], 0, "She cannot."),
 ("Which file holds long-term memory?", ["/Jade/Memory.md", "/Jade/SOUL.md", "/Jade/Flows", "/Jade/Logs"], 0, "Plain markdown."),
 ("What is the vector index?", ["A cache that can be rebuilt", "The source of truth", "A backup", "A skill"], 0, "Markdown is the truth."),
 ("What does reciprocal rank fusion do?", ["Merges ranked lists", "Encrypts notes", "Counts tokens", "Runs tools"], 0, "Keywords plus vectors."),
 ("What is BM25?", ["A keyword ranking formula", "A model", "A tool", "A key"], 0, "The fallback search."),
 ("What does a skill file need in its frontmatter?", ["name and description", "A password", "A date", "Nothing"], 0, "SKILL.md."),
 ("How many skills are all listed in the prompt?", ["15 or fewer", "Exactly 6", "Always 100", "None"], 0, "More are routed."),
 ("What does find_skill do?", ["Searches the skills not listed", "Deletes skills", "Runs a flow", "Backs up"], 0, "The rest."),
 ("What does an empty HEARTBEAT.md do?", ["Skips the model call", "Crashes", "Calls the model twice", "Deletes memory"], 0, "Nothing to do."),
 ("What does the heartbeat answer when nothing needs doing?", ["HEARTBEAT_OK", "STOP", "DONE", "Nothing"], 0, "A quiet reply."),
 ("What limits curiosity?", ["A window of hours and a daily cap", "Nothing", "Only the model", "Only the phone"], 0, "08:00 to 22:00, 5 a day."),
 ("How much does the self-score count in curiosity?", ["A quarter, capped near the measured value", "All of it", "Nothing", "Double"], 0, "Measured results win."),
 ("What starts a flow?", ["Hand, schedule or note change", "Only a button", "Only Jade", "Only cron"], 0, "Also shell and API."),
 ("What is $json in a flow?", ["The previous step's output", "A secret", "The flow name", "The model"], 0, "Chaining."),
 ("How many retries can a flow step have?", ["0 to 3", "Unlimited", "Exactly 1", "10"], 0, "Or continue on error."),
 ("Is a model in the loop of a playbook?", ["No", "Always", "Sometimes", "Only on Android"], 0, "Deterministic."),
 ("What does a playbook's approval depend on?", ["A hash of its content", "Its name", "Its date", "Its size"], 0, "Changes need re-approval."),
 ("What does an undefined name do in a playbook expression?", ["It is an error", "Is empty", "Is zero", "Is true"], 0, "Catches typos."),
 ("What does allow_hosts limit?", ["Where requests may go", "Who may log in", "Disk size", "Model choice"], 0, "Network safety."),
 ("What is a knowledge graph fact?", ["A relation like works_at(alice, acme)", "A heading", "A tag", "A skill"], 0, "Subject and object."),
 ("What does unknown mean in the graph?", ["Nothing says either way", "False", "True", "Broken"], 0, "Open world."),
 ("Who confirms facts Jade adds?", ["You", "The model", "A flow", "Nobody"], 0, "They start as proposed."),
 ("What goes first in autonomous mode?", ["Tier 1 interrupts", "Long goals", "Plans", "Schedules"], 0, "In arrival order."),
 ("What sets a plan's finish date?", ["The critical path", "The first task", "Today", "The model"], 0, "Longest chain."),
 ("What does a failed tier 1 check do in think?", ["Vetoes the node", "Lowers the score a bit", "Nothing", "Retries"], 0, "Ground truth."),
 ("What does the delegate tool return?", ["One report", "Every page it read", "A vault", "A model"], 0, "Context stays clean."),
 ("How do you call a tool from Jade Lisp?", ["(tool/NAME :arg value)", "run NAME", "tool.NAME()", "@NAME"], 0, "Keyword arguments."),
 ("What does fuel limit?", ["Evaluation steps", "Disk", "Network", "Memory"], 0, "Runaway loops."),
 ("What does the HTTP API need on every call but health?", ["The bearer token", "A cookie", "Nothing", "A password"], 0, "Off by default."),
 ("What encrypts backups?", ["AES-GCM with a PBKDF2 key", "ROT13", "Nothing", "MD5"], 0, "210,000 rounds."),
 ("What happens when a build patch matches twice?", ["The build fails with AMBIGUOUS", "It applies twice", "It is skipped", "A warning only"], 0, "Exactly once."),
]

CFG = dict(id="jade-vault", title="Jade Vault: A Markdown Vault with an AI Agent", subtitle="Notes, memory, tools, flows, playbooks and a knowledge graph, explained with small Python models",
    description="Learn how Jade Vault works: an Obsidian-style markdown vault with an AI agent called Jade, as one HTML page and an Android app. You will follow a turn step by step, then study tools and safety, memory and hybrid search, skills, the heartbeat, schedules and curiosity, flows, playbooks, the knowledge graph with Datalog rules, autonomous mode and Gantt plans, the think tool, delegation, Jade Lisp, the HTTP API, backups and the patch-based build. The course follows version 2.28.1. Each chapter has an ELI5 block and Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="jvc", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "jade-vault.course.json")
    cmk.main(CFG, jv1.A + jv2.B, [sys.argv[0], out])
