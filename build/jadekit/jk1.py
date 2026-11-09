"""Jade Agent Kit course, chapters 1-6."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

A = []

A.append(CH(
 "Meet the kit and lean loading",
 ("The kit", [
  "Jade Agent Kit | is | A browser workspace for agents", "createKit | creates | The kit with a file system", "kit.use | loads | A feature on demand",
  "Lean loading | downloads | Only what you use", "Module | is | One feature file", "Version pin | protects | Your app from changes", "Jade Vault | is | Where the pieces come from"]),
 ["The Jade Agent Kit is a workspace that lives inside a web page and gives an AI agent a place to get things done. It has a virtual file system, a shell, Python, JavaScript, SQLite, search, decisions, scheduling and an agent, and every piece is optional.",
  "Its main idea is lean loading. The first call, createKit, sets up only the file system. Each other feature is its own module that downloads the first time a page uses it. A page that needs only files stays tiny.",
  "This course follows the kit's documentation, version 3, and builds small working models of each idea in Python so you understand how the real thing behaves."],
 [("Kit", "The object that createKit returns; every feature hangs off it."), ("Feature", "An optional module such as shell, python, sqlite or agent."),
  ("kit.use", "Loads one or more features and returns them."), ("Lean loading", "Downloading a feature only when it is first used."), ("Pinning", "Importing a fixed version so the code never changes under you."), ("VFS", "The virtual file system, kit.vfs.")],
 ["You import createKit from a CDN, pinned to a version such as v3.0.0.", "createKit alone loads just the file system (about 6.6 KB gzipped).", "kit.use('python') loads Python; kit.use('sqlite', 'bm25') loads several.",
  "Helpers such as kit.run, kit.tool, kit.decide, kit.embed and kit.agent load what they need by themselves.", "kit.has('python') tells whether a feature is loaded.", "createKit({ use: [...] }) preloads; use: 'all' loads everything."],
 [T("Imagine a toolbox where every tool stays at the shop until you ask for it. That is lean loading. You carry a small box with a workbench in it, the file system, and fetch a saw or a drill only when a job needs one."),
  T("The first step is one import from a CDN. You pin the version, because the CDN caches tagged versions permanently and an unpinned import could change your app later."),
  C("import { createKit } from 'https://cdn.jsdelivr.net/gh/lucky-edgelord/Jade-agent-kit@v3.0.0/dist/jade-agent-kit.js';\n\nconst kit = await createKit({ persist: 'my-app' });\nkit.vfs.write('/hello.txt', 'hello world\\n');\nconst r = await kit.run('cat /hello.txt | tr a-z A-Z');\nconsole.log(r.stdout); // HELLO WORLD", "js"),
  T("In this example createKit loads only the file system and keeps it in the browser's IndexedDB under the name my-app. The call to kit.run then loads the shell and its BusyBox program on first use, which is why the output appears after a short wait the first time."),
  T("Sizes show the idea. The core is about 6.6 kilobytes gzipped. The shell adds about 12.6 plus 5 kilobytes and a 300 kilobyte WebAssembly file. Python adds 8.5 kilobytes plus about half a megabyte for MicroPython. SQLite adds 9 kilobytes and about 900 kilobytes of WebAssembly. BM25 search is only 2.1 kilobytes with no extra download."),
  T("You can also load features yourself with kit.use, preload them in createKit, or import single modules without createKit at all. Shared code sits in common chunk files so nothing downloads twice, and you can self-host by copying the dist and assets folders together.")],
 [("What does createKit load by itself?", ["Only the file system", "The shell and Python", "Everything", "Only the agent"], 0, "Everything else is loaded on demand."),
  ("Why pin the CDN import to a version?", ["Tagged versions are cached permanently and will not change", "It is faster to type", "It enables Python", "It is required for IndexedDB"], 0, "A fixed version keeps your app stable."),
  ("Which call tells whether Python is loaded?", ["kit.has('python')", "kit.use('python')", "kit.python()", "kit.load()"], 0, "kit.has checks without loading.")],
 [("What does persist do?", "Keeps the file system in IndexedDB under a name."), ("What does kit.run load on first use?", "The shell and BusyBox."), ("How do you preload features?", "createKit({ use: [...] })."), ("Where do runtimes come from?", "A CDN, set by the cdn option.")],
 [MATCH("Load costs", "Match each feature with what it downloads.", [("shell", "BusyBox as WebAssembly"), ("python", "MicroPython"), ("sqlite", "SQLite WebAssembly"), ("bm25", "Nothing extra")]),
  FILL("Using features", "Call kit.{{use}}('python') to load Python, and kit.{{has}}('python') to check whether it is already loaded."),
  PL("Download cost", "Write total_kb(features): features is a list of names from shell, python, sqlite, bm25. Each costs its gzipped code plus its extra download in KB: shell 12.6+5.0+300, python 8.5+500, sqlite 9.0+900, bm25 2.1+0. Add the core 6.6 KB once. Return the total rounded to 1 decimal.",
     "total_kb(features)", """
def total_kb(features):
    cost = {'shell': 12.6 + 5.0 + 300, 'python': 8.5 + 500, 'sqlite': 9.0 + 900, 'bm25': 2.1}
    t = 6.6
    for f in features:
        t += cost[f]
    return round(t, 1)
""", [[[]], [["bm25"]], [["shell", "python"]], [["shell", "python", "sqlite", "bm25"]]], "Start at the core and add each feature.", approx=0.05)]))

A.append(CH(
 "The virtual file system",
 ("VFS", [
  "kit.vfs | is | An in-memory file system", "persist | saves to | IndexedDB", "write | creates | Missing folders", "read | returns | A string",
  "readBytes | returns | A Uint8Array", "on | reports | Changed paths", "Everything else | shares | The VFS"]),
 ["kit.vfs is a small file system in the browser. Paths look like /notes/a.md. Writing a file creates any missing folders. Because the shell, Python, JavaScript, SQLite, the agent's tools and the brain all use the same file system, a file written by one is seen by all.",
  "By default it lives in memory. With persist set to a name, changes are saved to IndexedDB shortly after each change, and flush saves immediately.",
  "The lab builds a tiny file system to see how paths and folders work."],
 [("Path", "A slash-separated name such as /logs/run.txt."), ("mkdirp", "Create a folder and any missing parents."), ("flush", "Save to IndexedDB right now."),
  ("snapshot", "A copy of the current state."), ("import", "Load files from an object mapping paths to contents."), ("on", "Subscribe to changes.")],
 ["write(path, data) takes a string or bytes and creates missing folders.", "read gives a string; readBytes gives a Uint8Array.", "list(dir) returns the names in a folder.",
  "exists, isDir and stat inspect a path.", "move, copy and rm change the tree.", "Data persists only if you set persist; otherwise it is memory only."],
 [T("Think of the VFS as a folder tree that exists only inside your web page. It behaves like a normal disk, but nothing touches the user's real files. That makes it a safe place to let an agent write and run things."),
  C("kit.vfs.mkdirp('/logs');\nkit.vfs.write('/logs/run.txt', 'started');\nkit.vfs.write('/logs/data.bin', new Uint8Array([1, 2, 3]));\n\nkit.vfs.read('/logs/run.txt');        // string\nkit.vfs.readBytes('/logs/data.bin');  // Uint8Array\nkit.vfs.list('/logs');                // names in the folder\n\nkit.vfs.copy('/logs/run.txt', '/logs/run-backup.txt', true);\nkit.vfs.on(p => console.log('changed:', p));\nawait kit.vfs.flush();                // save to IndexedDB now\nkit.vfs.import({ '/config.json': '{}' });", "js"),
  T("Writes create parent folders on their own, so you rarely call mkdirp. The on method lets your page react to changes, for example to redraw a file list when the agent saves a note."),
  T("Persistence is a choice. Pass persist with a name when you create the kit and the workspace survives reloads. Leave it out and everything vanishes when the page closes. The brain, schedules, flows and notes all keep their files under a hidden /.kit folder in this same tree, so persisting the kit persists them too."),
  T("Because everything shares the VFS, it is also the meeting point between tools. The agent can write a CSV, Python can read it with open, SQLite can load it, and the shell can count its lines with wc. No copying between systems is needed.")],
 [("What happens when you write to /a/b/c.txt and the folders do not exist?", ["They are created", "An error is thrown", "The write is ignored", "Only /a is created"], 0, "write creates missing folders."),
  ("When does the VFS survive a page reload?", ["When persist is set", "Always", "Never", "When Python is loaded"], 0, "Otherwise it is memory only."),
  ("Which method returns a Uint8Array?", ["readBytes", "read", "list", "stat"], 0, "read returns a string.")],
 [("What does list return?", "Names inside a folder."), ("What does on do?", "Calls you with each changed path."), ("What is /.kit?", "Where features keep their files."), ("How do you save at once?", "await kit.vfs.flush().")],
 [ORDER("Saving work", "Put the steps to keep files across reloads in order.", ["Create the kit with persist set to a name", "Write files to kit.vfs", "The kit saves to IndexedDB shortly after each change", "Reload the page and the files are still there"]),
  PL("Tiny file system", "Write run_fs(ops): ops is a list of [op, path, data] where op is 'write' or 'rm'. Start with an empty file system. A write creates the file. An rm removes the file. After all ops return the sorted list of the folders that still contain at least one file, directly or through subfolders, as paths without the file name (for example '/a' and '/a/b'); the root '/' is not included.",
     "run_fs(ops)", """
def run_fs(ops):
    files = {}
    for op, path, data in ops:
        if op == 'write':
            files[path] = data
        elif op == 'rm' and path in files:
            del files[path]
    dirs = set()
    for p in files:
        parts = p.split('/')
        cur = ''
        for part in parts[1:-1]:
            cur += '/' + part
            dirs.add(cur)
    return sorted(dirs)
""", [[[["write", "/a/b/c.txt", "x"], ["write", "/a/d.txt", "y"]]], [[["write", "/a/b/c.txt", "x"], ["rm", "/a/b/c.txt", ""]]], [[["write", "/x.txt", "1"]]], [[["write", "/logs/run.txt", "s"], ["write", "/logs/old/a.txt", "o"], ["rm", "/logs/run.txt", ""]]]], "Collect parent folders of surviving files.", approx=None),
  PL("List a folder", "Write list_dir(paths, dir): paths is a list of file paths; dir is a folder path like '/a' ('/' for the root). Return the sorted names directly inside dir (files and subfolder names, without duplicates).",
     "list_dir(paths, dir)", """
def list_dir(paths, dir):
    prefix = dir
    if not prefix.endswith('/'):
        prefix += '/'
    names = set()
    for p in paths:
        if p.startswith(prefix):
            rest = p[len(prefix):]
            names.add(rest.split('/')[0])
    return sorted(names)
""", [[["/a/b/c.txt", "/a/d.txt", "/e.txt"], "/a"], [["/a/b/c.txt", "/a/d.txt", "/e.txt"], "/"], [["/a/b/c.txt", "/a/b/x.txt"], "/a/b"], [["/a/b/c.txt"], "/z"]], "Strip the prefix; take the first segment.", approx=None)]))

A.append(CH(
 "The shell: kit.run and sessions",
 ("Shell", [
  "kit.run | runs | A command string", "BusyBox | provides | Unix commands", "Pipes | connect | Commands", "Session | keeps | cwd and env",
  "Custom command | is | A function", "No if or for | means | Use node or python", "Engine | can be | auto, wasm or js"]),
 ["kit.run executes a shell command string against the virtual file system. It understands pipes, redirects, and, or, variables, command substitution and globs. The commands come from BusyBox 1.37 compiled to WebAssembly, with JavaScript versions of common ones as a fallback.",
  "A session gives you your own working directory and environment variables, with options for streaming output, a timeout and cancellation. You can also register your own commands as functions.",
  "There are no if or for blocks in the shell. For real scripting, call node or python."],
 [("BusyBox", "A single program that provides many Unix commands."), ("Pipe", "Sends one command's output into the next as input."), ("Session", "A shell with its own cwd and env."),
  ("stdout and stderr", "Normal output and error output."), ("Exit code", "0 means success; other numbers mean failure."), ("Glob", "A pattern such as *.md that matches file names.")],
 ["kit.run returns an object with stdout (and the exit status).", "A && B runs B only if A succeeds; A || B runs B only if A fails.", "kit.shell.session({ cwd, env }) creates a separate shell.",
  "session.run(cmd, { onOutput, timeoutMs, signal }) streams, limits time and can be cancelled.", "kit.shell.commands.name = fn registers a custom command.", "Built-in extras: node, js, python, python3, sqlite3, sh, xargs, cd, export, which, help."],
 [T("The shell lets an agent do what people do at a terminal: list files, search them, count lines, move things around. Because it is real BusyBox compiled to WebAssembly, the commands behave as you would expect from Linux."),
  C("await kit.run('ls -la / && grep -rn TODO /src | head');\n\nconst sh = kit.shell.session({ cwd: '/project', env: { NAME: 'x' } });\nawait sh.run('cd lib && pwd', { onOutput: (text, isErr) => {}, timeoutMs: 30000, signal });", "js"),
  T("Operators work as in a normal shell. A pipe sends output onward. The && operator runs the next command only if the first succeeded, and || runs it only if the first failed. Variables and command substitution with a dollar sign work too."),
  T("There is no if or for in the shell language. This is a deliberate limit: when you need loops or conditions, run a script with node or python, which are available as commands."),
  C("kit.shell.commands.hello = c => {\n  c.o(`hello ${c.argv[0] ?? ''}\\n`);\n  return 0;\n};\nawait kit.run('hello world');", "js"),
  T("A custom command receives a context. It has argv for the arguments, stdin for piped input, o for standard output, e for standard error, and sh.cwd for the working directory. It returns an exit code, and 0 means success. The engine setting can be auto, wasm or js; auto uses BusyBox when it has loaded.")],
 [("What does A && B do?", ["Runs B only if A succeeds", "Runs both at once", "Runs B only if A fails", "Pipes A into B"], 0, "&& chains on success."),
  ("How do you do a loop in the kit's shell?", ["Run node or python", "Use a for block", "Use while", "You cannot"], 0, "The shell has no if or for blocks."),
  ("What does a custom command return?", ["An exit code", "A promise of text", "A file", "Nothing"], 0, "0 means success.")],
 [("What is BusyBox?", "Many Unix commands in one program."), ("What does c.o do?", "Writes to standard output."), ("What is a session for?", "Its own cwd and variables."), ("What does signal do?", "Lets you cancel a run.")],
 [MATCH("Operators", "Match each operator with its meaning.", [("|", "Send output to the next command"), ("&&", "Run next only on success"), ("||", "Run next only on failure"), (">", "Redirect output to a file")]),
  PL("Split a command", "Write split_cmd(line): split a shell line on '&&' into groups, and each group on '|' into stages. Strip spaces around each part. Return a list of groups, each a list of stage strings.",
     "split_cmd(line)", """
def split_cmd(line):
    out = []
    for g in line.split('&&'):
        stages = [s.strip() for s in g.split('|')]
        out.append(stages)
    return out
""", [["ls -la / && grep -rn TODO /src | head"], ["cat a | tr a-z A-Z"], ["pwd"], ["a && b && c | d | e"]], "Split on && first, then on |.", approx=None),
  PL("And and or", "Write run_chain(steps): steps is a list of [operator, exit_code] where operator is '' for the first command, '&&' or '||' for later ones, and exit_code is what that command WOULD return if it ran. Simulate the shell: a command after && runs only if the last run command returned 0; after || only if it returned non-zero. Return the list of indices of the commands that actually ran.",
     "run_chain(steps)", """
def run_chain(steps):
    ran = []
    last = 0
    for i in range(len(steps)):
        op, code = steps[i]
        go = False
        if op == '':
            go = True
        elif op == '&&':
            go = last == 0
        elif op == '||':
            go = last != 0
        if go:
            ran.append(i)
            last = code
    return ran
""", [[[["", 0], ["&&", 0], ["&&", 1]]], [[["", 1], ["&&", 0], ["||", 0]]], [[["", 0], ["||", 1], ["&&", 0]]], [[["", 2]]]], "Track the exit code of the last command that ran.", approx=None)]))

A.append(CH(
 "Python, JavaScript and SQLite",
 ("Runtimes", [
  "kit.python | runs | MicroPython", "kit.js | runs | A Node-style sandbox", "Web Worker | isolates | Each runtime", "kit.sqlite | opens | Databases in the VFS",
  "Parameters | prevent | Injection", "sqlite-vec | adds | Vector search", "FTS5 | adds | Full-text search"]),
 ["The kit can run code. kit.python runs MicroPython 1.27 in a Web Worker; its open and os see the same virtual file system. kit.js runs JavaScript in another worker with require, fs, path, node:sqlite and fetch, but no npm packages.",
  "kit.sqlite opens database files stored in the VFS and runs SQLite 3.53 in WebAssembly. With sqlite-vec it can store and search vectors, and FTS5 gives full-text search.",
  "In the lab you will build a safe parameterised query."],
 [("MicroPython", "A small Python for constrained environments."), ("Worker", "A background thread in the browser."), ("require", "Node's way to load a module."),
  ("Parameterised query", "SQL with ? placeholders and values passed separately."), ("db.save", "Writes the database back to the VFS."), ("vec0", "The sqlite-vec virtual table type.")],
 ["kit.python.run(code, { cwd }) runs Python; open() and os use the VFS.", "kit.js.run(code, { cwd, timeoutMs, globals, network }) returns the script's return value as r.result.", "Inside JavaScript, kit.tool(name, args) calls any kit tool.",
  "kit.sqlite.open(path) takes a VFS path or ':memory:'.", "db.exec for schema, db.run for writes with params, db.query for rows as objects.", "Always pass values as parameters, never glue them into SQL."],
 [T("Reading and writing files is not enough for most jobs; sometimes the agent needs to compute. The kit offers two languages. Python is handy for data and text. JavaScript is natural in a browser and can use the kit's own tools."),
  C("const r = await kit.python.run(`import json\\nprint(json.dumps({'n': 1}))`, { cwd: '/' });\n\nconst j = await kit.js.run(`\n  const { twice } = require('./lib/util.js');\n  const t = await kit.tool('read', { path: '/notes/a.md' });\n  return { ok: true };\n`, { cwd: '/', timeoutMs: 60000, globals: { input: 42 }, network: true });\n// j.result -> { ok: true }", "js"),
  T("Both run in Web Workers, so a long calculation does not freeze the page, and the timeoutMs option stops runaway code. JavaScript can require fs, path, util, os, http, https and node:sqlite, plus local files, but no packages from npm."),
  C("const db = await kit.sqlite.open('/data/notes.db');\ndb.exec(`create table if not exists note(id integer primary key, body text)`);\ndb.run(`insert into note(body) values (?)`, ['buy coffee']);\nconst rows = db.query(`select * from note where id > ?`, [0]);\ndb.save();", "js"),
  T("Notice the question marks. A parameterised query keeps the SQL text and the values apart, so a value such as a quote character can never change the meaning of the statement. That is how SQL injection is prevented."),
  C("db.exec(`create virtual table vec_notes using vec0(embedding float[3])`);\ndb.run(`insert into vec_notes(rowid, embedding) values (?, ?)`, [1, '[0.5, 0.1, 0.9]']);\nconst nearest = db.query(\n  `select rowid, distance from vec_notes where embedding match ? order by distance limit 3`,\n  ['[0.5, 0.1, 0.8]']);", "js"),
  T("With the sqlite-vec extension a vec0 table stores vectors of a fixed size, and a match query returns the nearest rows with their distance. The next chapters use this for meaning-based search.")],
 [("What does r.result hold after kit.js.run?", ["The script's return value", "Its console output", "The exit code", "The file list"], 0, "return becomes r.result."),
  ("Why use ? placeholders in SQL?", ["Values cannot change the statement's meaning", "They are faster to type", "They enable FTS5", "They save the database"], 0, "It prevents injection."),
  ("Can kit.js use npm packages?", ["No", "Yes, all", "Only with network", "Only in Python"], 0, "Only the listed modules and local files.")],
 [("What does db.save do?", "Writes the database to the VFS."), ("What is ':memory:'?", "A temporary database."), ("What does globals do?", "Passes values into the script."), ("Where does Python's open look?", "At the VFS.")],
 [FILL("Database calls", "Use db.{{exec}} for schema, db.{{run}} for writes with parameters and db.{{query}} to read rows."),
  PL("Safe query", "Write bind(sql, params): replace each '?' in sql, left to right, with the matching value: numbers as they are (str), strings in single quotes with every single quote doubled. Return the final string.",
     "bind(sql, params)", """
def bind(sql, params):
    out = ''
    i = 0
    for ch in sql:
        if ch == '?':
            v = params[i]
            i += 1
            if isinstance(v, str):
                out += "'" + v.replace("'", "''") + "'"
            else:
                out += str(v)
        else:
            out += ch
    return out
""", [["select * from note where id > ?", [0]], ["insert into note(body) values (?)", ["buy coffee"]], ["select * from t where a = ? and b = ?", ["o'brien", 3]], ["x", []]], "Walk the string; swap each ?.", approx=None)]))

A.append(CH(
 "BM25 keyword search",
 ("BM25", [
  "BM25 | ranks | Documents for a query", "Term frequency | rewards | Repeated words", "Inverse document frequency | rewards | Rare words", "Length normalisation | penalises | Long documents",
  "kit.bm25.search | searches | An array", "BM25 class | builds | A reusable index", "searchFiles | searches | Files in a folder"]),
 ["BM25 is a ranking formula for keyword search: documents that contain the query words more often, especially rare words, and that are not too long, score higher. It needs no downloads and is only 2.1 KB in the kit.",
  "kit.bm25.search ranks an array of texts for one query. The BM25 class builds an index once for many queries. searchFiles ranks files under a folder, which is how an agent finds the right note.",
  "The lab implements the scoring yourself."],
 [("Term frequency", "How many times a word appears in a document."), ("Document frequency", "How many documents contain the word."), ("IDF", "Inverse document frequency: rarer words weigh more."),
  ("k1 and b", "BM25's saturation and length-normalisation parameters."), ("Index", "A prepared structure for quick searching."), ("Snippet", "The matching line returned by searchFiles.")],
 ["search(docs, query) returns objects with id, text and score.", "new kit.bm25.BM25(docs) builds a reusable index; index.search(query, { limit }).", "searchFiles(query, { root }) returns path, score, line and snippet.",
  "Scores are relative: compare them within one search, not across searches.", "BM25 matches words, not meaning; embeddings come next.", "The page says its scoring follows Python's rank_bm25."],
 [T("When you search a pile of notes for the word coffee, which note should come first? One that mentions coffee three times is a better guess than one that mentions it once. A note that mentions the rare word espresso is more special than one that only says the common word the. BM25 turns those instincts into a number."),
  C("kit.bm25.search(['the cat sat', 'a dog ran', 'cats and dogs'], 'cat');\n\nconst index = new kit.bm25.BM25([{ id: 'a', text: '…' }, { id: 'b', text: '…' }]);\nindex.search('query', { limit: 5 });\n\nkit.bm25.searchFiles('error handling', { root: '/src' });", "js"),
  M(r"\mathrm{score}(D,Q)=\sum_{q\in Q}\mathrm{IDF}(q)\cdot\frac{f(q,D)\,(k_1+1)}{f(q,D)+k_1\,(1-b+b\,|D|/\mathrm{avgdl})}"),
  T("For each query word, IDF measures how rare it is. The fraction rewards frequent use inside the document, but with diminishing returns controlled by k1, so saying a word ten times is not ten times better. The b term shrinks the score for documents longer than average."),
  T("The kit's documentation says its scoring follows the Python library rank_bm25 and does not spell out the constants, so check the source if you need exact numbers. In practice you use the order of results, not the raw scores."),
  T("The agent's search_files tool is built on searchFiles. Given a folder, it returns the best matching lines with their file path, which lets an agent find the right place in a big workspace without reading everything.")],
 [("Which words does IDF weigh more?", ["Rare words", "Common words", "Short words", "The first word"], 0, "Rarity carries information."),
  ("What does length normalisation do?", ["Reduces the score of long documents", "Removes short words", "Sorts by length", "Counts letters"], 0, "Otherwise long texts would always win."),
  ("What does searchFiles return?", ["path, score, line and snippet", "Only file names", "The whole file", "A boolean"], 0, "It points at the matching line.")],
 [("Does BM25 understand meaning?", "No, it matches words."), ("What does limit do?", "Caps the number of results."), ("When use the BM25 class?", "For many queries on one set of documents."), ("Where do scores compare?", "Within the same search.")],
 [ORDER("Ranking", "Put the BM25 steps in order.", ["Split the query into words", "Count each word in each document", "Weigh each word by how rare it is", "Adjust for document length", "Sort documents by total score"]),
  PL("BM25 score", "Write bm25(docs, query): docs is a list of strings, query a string. Lower-case and split on spaces. Use k1=1.5, b=0.75, IDF = ln(1 + (N - n + 0.5) / (n + 0.5)) where N is the number of docs and n the number containing the word. Return each document's score, rounded to 6 decimals, in the original order. Use import math.",
     "bm25(docs, query)", """
import math
def bm25(docs, query):
    toks = [d.lower().split() for d in docs]
    N = len(docs)
    avg = sum(len(t) for t in toks) / N
    k1 = 1.5
    b = 0.75
    scores = []
    for t in toks:
        s = 0.0
        for q in query.lower().split():
            n = 0
            for u in toks:
                if q in u:
                    n += 1
            if n == 0:
                continue
            idf = math.log(1 + (N - n + 0.5) / (n + 0.5))
            f = t.count(q)
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(t) / avg))
        scores.append(round(s, 6))
    return scores
""", [[["the cat sat", "a dog ran", "cats and dogs"], "cat"], [["coffee coffee tea", "coffee", "tea tea tea tea"], "coffee"], [["a b c", "a a a"], "a b"], [["x y", "y z", "z x"], "z"]], "Compute idf per word, then sum per document.", approx=1e-5)]))

A.append(CH(
 "Embeddings and vector search",
 ("Vectors", [
  "Embedding | is | A vector for text", "kit.embed | uses | Local Ollama", "Distance | measures | Similarity", "kit.vectors | stores | Embeddings in SQLite",
  "Hybrid search | merges | Meaning and keywords", "Model tag | prevents | Mixing models", "Cloud | has no | Embedding models"]),
 ["An embedding turns text into a list of numbers so that texts with similar meaning have nearby vectors. kit.embed makes them using a model running locally through Ollama, such as embeddinggemma or nomic-embed-text. Ollama Cloud has no embedding models.",
  "kit.vectors keeps embeddings in a SQLite file using sqlite-vec. A search embeds your question and returns the nearest records. Hybrid search also uses BM25 and merges the two rankings.",
  "The labs compute similarity and merge rankings."],
 [("Embedding", "A vector that captures meaning."), ("Cosine similarity", "Closeness of direction of two vectors."), ("Nearest neighbour", "The stored vector closest to the query."),
  ("Hybrid search", "Combining semantic and keyword rankings."), ("Store", "A vector database opened with kit.vectors.open."), ("Rank fusion", "Merging rankings by position.")],
 ["kit.embed(text) gives one vector; kit.embed(array, { model }) gives many.", "store = await kit.vectors.open(path); store.add(items); store.search(query, { limit }).", "Results have id, text, meta, distance and score.",
  "{ hybrid: true } merges meaning search with BM25.", "A store remembers its model and rejects vectors from another.", "Pull an embedding model in Ollama first."],
 [T("Keyword search fails when the words differ: a note about cats sleeping many hours will not match the question how long do kittens nap. An embedding places both near each other because their meanings are close."),
  C("const store = await kit.vectors.open('/data/notes.db');\nawait store.add([{ id: 'n1', text: 'Cats sleep many hours a day', meta: { source: 'wiki' } }]);\nconst hits = await store.search('how long do cats sleep', { limit: 5 });\nconst merged = await store.search('cats sleep', { hybrid: true });\nstore.close();", "js"),
  T("The store embeds each text when you add it and the query when you search. Closeness is usually measured by cosine similarity, which compares direction, not length. A store records which model made its vectors and refuses vectors from a different model, because numbers from different models cannot be compared."),
  M(r"\cos(a,b)=\frac{a\cdot b}{\|a\|\,\|b\|}"),
  T("Meaning search and keyword search each miss things the other finds, so hybrid mode runs both and merges the results. One common way to merge is reciprocal rank fusion: each list gives a document the score one over a constant plus its rank, and the scores are added."),
  T("The memory and skills parts of the agent brain can use the same embeddings to find the most relevant facts or skills for each prompt, which is covered in a later chapter.")],
 [("What does an embedding capture?", ["Meaning as a vector", "Spelling only", "File size", "Word count"], 0, "Similar meaning means nearby vectors."),
  ("Why does a store reject vectors from another model?", ["They cannot be compared", "They are too long", "They are slower", "They use more disk"], 0, "Different models, different spaces."),
  ("What does hybrid: true do?", ["Merges meaning and BM25 results", "Disables search", "Uses the cloud", "Sorts by id"], 0, "Best of both.")],
 [("Which models can embed?", "Local Ollama models like embeddinggemma."), ("Does Ollama Cloud embed?", "No."), ("What is cosine similarity?", "Direction closeness."), ("What does store.remove do?", "Deletes a record.")],
 [MATCH("Search types", "Match each search with what it matches.", [("BM25", "Words in common"), ("Vector search", "Similar meaning"), ("Hybrid", "Both, merged"), ("searchFiles", "Lines in files")]),
  PL("Cosine similarity", "Write cosine(a, b): the cosine similarity of two equal-length vectors, rounded to 6 decimals. Use import math.",
     "cosine(a, b)", """
import math
def cosine(a, b):
    d = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        d += x * y
        na += x * x
        nb += y * y
    return round(d / (math.sqrt(na) * math.sqrt(nb)), 6)
""", [[[1, 0], [1, 0]], [[1, 0], [0, 1]], [[1, 2, 3], [2, 4, 6]], [[0.5, 0.1, 0.9], [0.5, 0.1, 0.8]]], "Dot product over the product of lengths.", approx=1e-5),
  PL("Reciprocal rank fusion", "Write fuse(a, b, k): a and b are lists of ids ordered best first; each id gets 1/(k + rank) from every list it appears in (rank starts at 1). Return the ids sorted by total score, best first; ties by first appearance in a then b.",
     "fuse(a, b, k)", """
def fuse(a, b, k):
    score = {}
    order = []
    for lst in (a, b):
        for i in range(len(lst)):
            x = lst[i]
            if x not in score:
                score[x] = 0.0
                order.append(x)
            score[x] += 1.0 / (k + i + 1)
    ranked = sorted(range(len(order)), key=lambda j: (-round(score[order[j]], 12), j))
    return [order[j] for j in ranked]
""", [[["a", "b", "c"], ["c", "b", "d"], 60], [["a"], ["b"], 60], [["x", "y"], ["x", "y"], 10], [["a", "b"], ["c", "a"], 1]], "Add reciprocal ranks.", approx=None)]))
