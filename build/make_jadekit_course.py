#!/usr/bin/env python3
"""Build the Jade Agent Kit course. Usage: python3 make_jadekit_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "jadekit"))
import cmk, jk1, jk2  # noqa: E402

PRONOUNCE = {
    "Jade": "jade", "kit": "kit", "createKit": "create kit", "kit.use": "kit dot use", "kit.run": "kit dot run", "kit.vfs": "kit dot V F S", "vfs": "V F S", "VFS": "V F S",
    "BusyBox": "busy box", "WebAssembly": "web assembly", "MicroPython": "micro python", "SQLite": "S Q L ite", "sqlite": "S Q L ite", "sqlite-vec": "S Q L ite vec", "FTS5": "F T S five",
    "BM25": "B M twenty five", "IDF": "I D F", "ELI5": "E L I five", "IndexedDB": "indexed D B", "CDN": "C D N", "npm": "N P M", "JSON": "jason", "API": "A P I", "LLM": "L L M",
    "Ollama": "oh llama", "Ollaya": "oh lie uh", "MCP": "M C P", "cron": "cron", "n8n": "N eight N", "HEARTBEAT_OK": "heartbeat okay", "Anthropic": "an throp ik", "OpenAI": "open A I",
    "stdout": "standard out", "stderr": "standard error", "Obsidian": "ob sid ee an", "Sentry": "sentry", "ONNX": "onyx", "WebGPU": "web G P U", "Ansible": "an sib ul", "gzipped": "G zipped",
}

SANDBOX = cmk.terminal("Kit cheat sheet", "kit>", "A scripted lookup, not the real kit. Try: create, vfs, run, agent, decide, schedule", [
    ("create", ["const kit = await createKit({ persist: 'my-app' });", "only the file system loads; the rest loads on demand"]),
    ("vfs", ["kit.vfs.write(path, data)  kit.vfs.read(path)  kit.vfs.list(dir)", "persist saves to IndexedDB; flush() saves now"]),
    ("run", ["await kit.run('ls / && cat a | head')", "no if or for in the shell: use node or python"]),
    ("agent", ["const agent = await kit.agent({ onEvent }); await agent.prompt('...')", "tools: read write edit bash search fetch; maxSteps 40"]),
    ("decide", ["await kit.decide({ state, question, options })", "types: choice, score, yesno; returns probabilities"]),
    ("schedule", ["kit.schedule.add({ when: 'every day at 2am', command: '...' })", "jobs run only while a page with the kit is open"]),
    ("bm25", ["kit.bm25.search(docs, query)", "searchFiles(query, { root }) returns path, score, line, snippet"]),
])

EXAM = [
 ("What does createKit load by default?", ["Only the file system", "Everything", "The agent", "Python and SQLite"], 0, "Lean loading."),
 ("Why pin the CDN import to a version?", ["Tags are cached permanently", "It is shorter", "It enables Python", "It is required"], 0, "Stable code."),
 ("Which call loads Python?", ["kit.use('python')", "kit.python()", "kit.load()", "createKit.python"], 0, "Or call kit.python.run after use."),
 ("What does persist do?", ["Saves the file system to IndexedDB", "Starts the agent", "Opens a shell", "Encrypts keys"], 0, "Otherwise memory only."),
 ("Which VFS method returns bytes?", ["readBytes", "read", "list", "stat"], 0, "A Uint8Array."),
 ("What does write do for missing folders?", ["Creates them", "Fails", "Ignores", "Asks"], 0, "Parents are created."),
 ("What does A && B do in the shell?", ["Runs B only if A succeeds", "Runs both", "Pipes A to B", "Runs B on failure"], 0, "Chains on success."),
 ("How do you loop in the kit's shell?", ["Use node or python", "for block", "while block", "goto"], 0, "No if or for."),
 ("What does a custom command return?", ["An exit code", "Text", "A file", "A promise"], 0, "0 is success."),
 ("What does kit.js.run's result field hold?", ["The return value", "Console output", "Exit code", "Files"], 0, "r.result."),
 ("Why use ? placeholders in SQL?", ["Prevent injection", "Speed", "FTS5", "Saving"], 0, "Values stay separate."),
 ("Can kit.js use npm packages?", ["No", "Yes", "Only with network", "Only for tf"], 0, "Listed modules only."),
 ("What does BM25 reward?", ["Frequent, rare query words", "Long documents", "Short words", "Capital letters"], 0, "TF and IDF."),
 ("Which search matches meaning?", ["Vector search", "BM25", "grep", "ls"], 0, "Embeddings."),
 ("Where can kit.embed run?", ["Local Ollama", "Ollama Cloud", "Python", "SQLite"], 0, "Cloud has no embedding models."),
 ("What does hybrid: true do?", ["Merge meaning and BM25 results", "Use cloud", "Disable search", "Sort by id"], 0, "Rank fusion."),
 ("What does kit.tool always return?", ["A string", "An object", "A boolean", "A file"], 0, "Errors start with Error:."),
 ("Which field names the Anthropic schema?", ["input_schema", "parameters", "args", "spec"], 0, "OpenAI uses parameters."),
 ("When does an agent turn end?", ["Model replies with no tool request", "After one tool", "After 40 seconds", "When saved"], 0, "Plain text reply."),
 ("What is the default maxSteps?", ["40", "5", "100", "1"], 0, "Stops runaway loops."),
 ("Which tools need an Ollama Cloud key?", ["search and fetch", "read and write", "bash", "edit"], 0, "Web access via cloud."),
 ("What does the guard do?", ["Compacts old turns near the context limit", "Blocks tools", "Encrypts files", "Starts jobs"], 0, "Keeps chats in the window."),
 ("What does the router do?", ["Sends only needed tools", "Routes network", "Picks files", "Deletes tools"], 0, "Saves context."),
 ("Where do skills live?", ["/.kit/skills/<name>/SKILL.md", "On a server", "In cookies", "In the model"], 0, "Plain files."),
 ("What does a decide choice result include?", ["probabilities and confidence", "A file", "A schedule", "A diff"], 0, "Calibrated."),
 ("Which decide type gives a boolean?", ["yesno", "score", "choice", "rank"], 0, "answer."),
 ("What do the five cron fields start with?", ["minute", "second", "hour", "year"], 0, "minute hour dom month dow."),
 ("When do scheduled jobs run?", ["While a page with the kit is open", "Always on a server", "Only at night", "Never"], 0, "Browser only."),
 ("What allows a sensitive Sentry source?", ["The allow option", "Nothing", "The agent", "The model"], 0, "App decides."),
 ("What is a backlink?", ["A note that links to this one", "A web link", "A tag", "A template"], 0, "Who links here."),
 ("Who approves a playbook?", ["The host app", "The agent", "The model", "No one"], 0, "Not the agent."),
 ("How does an agent use a secret?", ["By name with {{ NAME }}", "By value", "By path", "It cannot"], 0, "It never sees the value."),
 ("What does HEARTBEAT_OK do?", ["Stays silent", "Alerts", "Stops the kit", "Clears tasks"], 0, "Nothing to report."),
]

CFG = dict(id="jade-agent-kit", title="Jade Agent Kit: A Workspace for AI Agents", subtitle="Files, shell, code, search, tools, agents and safe automation in the browser, with Python labs",
    description="Learn the Jade Agent Kit (version 3), a lean browser workspace for AI agents: the virtual file system, shell, Python, JavaScript and SQLite runtimes, BM25 and vector search, tools for language models, the agent loop and brain, decisions, scheduling, Sentry, notes and safe automation with approvals and secrets. Each chapter has an ELI5 block and Python labs that rebuild the ideas.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="jadekit", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "jade-agent-kit.course.json")
    cmk.main(CFG, jk1.A + jk2.B, [sys.argv[0], out])
