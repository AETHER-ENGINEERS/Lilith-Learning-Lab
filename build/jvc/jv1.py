"""Jade Vault course, chapters 1-7."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

A = []

A.append(CH(
 "What Jade Vault is",
 ("Jade Vault", [
  "Vault | holds | Notes and files", "Jade | is | A model driven loop", "Model | is | Your own endpoint", "Tools | let | Jade act",
  "Memory | persists | Between chats", "Autonomy | is | Off until you switch it on", "Safety | gates | Risky actions"]),
 ["Jade Vault is a markdown vault in the style of Obsidian with an AI agent called Jade built in. It runs as one page in a browser and as an Android app.",
  "The vault is a virtual file system. Jade is a loop: your message plus a prompt built from her steering files, memory and skills goes to a model, she may call tools, and she answers.",
  "The model is not part of the app. You point it at Ollama, Ollama Cloud, Groq, OpenRouter, llama.cpp or any OpenAI compatible server."],
 [("Vault", "The virtual file system of notes and files that everything shares."), ("Jade", "The agent: a model, a prompt, tools and memory."), ("Turn", "One message from you through to her final reply."),
  ("Tool", "A function Jade can call, such as reading a note or running a shell command."), ("Provider", "The server that runs the model: Ollama, Groq, OpenRouter and so on."), ("Steering files", "Plain notes such as SOUL.md and AGENTS.md that shape her behaviour.")],
 ["Jade Vault is a markdown vault with a built-in agent, as one browser page or an Android app.", "The vault is the shared ground; Jade is a model driven loop around it.", "You choose the model: local Ollama, Ollama Cloud, Groq, OpenRouter, llama.cpp or any OpenAI style endpoint.",
  "Around the loop sit memory, autonomy, world tools, integrations and safety.", "Anything that runs on its own is off until you switch it on.", "Her settings and work products are ordinary files in the vault."],
 [T("Imagine a notebook that can think. You keep notes in it, and a helper called Jade lives inside, reads them, writes new ones, runs small programs, and remembers what you told her last week. That is Jade Vault in one sentence."),
  T("It is built from a few pieces. The vault is a virtual file system, the shared ground. In a browser it is stored in IndexedDB, and in the Android app it is a real folder called JadeVault. Jade is the agent. She is not a program that thinks by herself. She is a loop that sends a prompt to a model and runs the tools the model asks for."),
  C("you ──► chat / voice / schedule / heartbeat / API\n          │\n          ▼\n   ┌── Jade's turn ───────────────────────────┐\n   │ prompt = base + SOUL + AGENTS + memory   │\n   │          + skills                         │\n   │ model ◄──► tools ──► vault, shell, node,  │\n   │             python, sqlite, web, MCP ...  │\n   └───────────────────────────────────────────┘\n          │                    ▲\n          ▼                    │\n   vault (notes + files)   memory (Memory.md, journal, vectors)", "text"),
  T("Because the model lives outside the app, you decide who answers. You can use Ollama on your own computer, Ollama Cloud, Groq, OpenRouter, llama.cpp or any server that speaks the OpenAI format, and you can add a chain of fallbacks. On the phone the network is native, so local Ollama needs no special browser setting."),
  T("Around the loop sit five kinds of capability. Memory keeps facts, a journal and a search index. Autonomy lets her wake on schedules, a heartbeat or her own curiosity. World tools give her the camera, the phone, the screen, a second browser and SSH on Android. Integrations connect MCP servers, an HTTP API, messengers and mini apps. Safety is approvals, secrets and labels on untrusted text."),
  T("Two rules run through the whole design. First, the vault is the memory and the interface: what steers her is a plain file she can read and mostly write. Second, everything risky is gated: secrets are placeholders, calls and texts ask you first, and external text is labelled as data, not instructions. This course follows those ideas one chapter at a time, and each lab rebuilds a small piece in Python."),
  T("A note on versions. The course follows the repository at version 2.28.1. The documentation was written across many releases, so some pages name an older version. When a feature has a version, it is mentioned.")],
 [("What is the vault?", ["A virtual file system of notes and files", "A password manager", "A database server", "A model"], 0, "The shared ground."),
  ("Where does the model run?", ["Wherever you point it: Ollama, cloud, Groq and others", "Inside the app only", "Only on Anthropic servers", "On the phone's camera"], 0, "It is not part of the app."),
  ("What do autonomy features need to run?", ["You switch them on", "Nothing, they start alone", "A paid plan", "A reboot"], 0, "Off by default.")],
 [("What is Jade?", "A model driven loop with tools."), ("Where is the Android vault?", "The JadeVault folder."), ("What shapes her behaviour?", "Plain steering files."), ("What is a turn?", "One message through to her reply.")],
 [MATCH("The pieces", "Match each piece with its job.", [("Vault", "Shared notes and files"), ("Model", "Does the thinking, outside the app"), ("Tools", "Let Jade act on things"), ("Memory", "Keeps facts between chats")]),
  PL("Who can start a turn", "Write active_sources(switches): switches is a dict from a source name (like 'heartbeat', 'curiosity', 'schedules', 'api') to true or false. The chat is always active; every other source is active only when its switch is true. Return the sorted list of active sources including 'chat'.",
     "active_sources(switches)", """
def active_sources(switches):
    out = ['chat']
    for name in switches:
        if switches[name] and name != 'chat':
            out.append(name)
    return sorted(out)
""", [[{}], [{"heartbeat": True, "curiosity": False}], [{"api": True, "schedules": True, "heartbeat": True}], [{"chat": False}]], "Start with chat, then add switched-on sources.", approx=None)]))

A.append(CH(
 "Notes and the vault",
 ("Vault", [
  "Note | has | Links and tags", "Link | looks like | Double brackets", "Backlink | is | Who links here", "Graph | draws | Notes and links",
  "Embed | uses | Exclamation and brackets", "Templates | live in | Templates", "Jade folder | holds | Her files"]),
 ["Notes are markdown files. A link to another note is written in double square brackets, and an embed, such as an image, puts an exclamation mark in front. Tags start with a hash sign.",
  "The notes screen shows backlinks, a graph, a reader and a split editor. Obsidian style scripts and Templater templates are supported inside a sandbox.",
  "Her own files live under /Jade. The labs classify files, find links and build backlinks."],
 [("Wiki link", "A link to another note, written [[Note name]]."), ("Backlink", "A note that links to this one."), ("Embed", "Showing a note or image inside another with ![[...]]."),
  ("Frontmatter", "Key value data at the top of a note between --- lines."), ("Tag", "A word starting with # used to group notes."), ("Template", "A note in /Templates that fills in dates and titles when inserted.")],
 ["Links are [[Note]]; an alias is [[Note|text]]; a heading link is [[Note#Heading]].", "Images and notes embed with ![[photo.png|300]].", "Backlinks list the notes that point at the current note.",
  "Templates use <% tp.date.now() %> style code from Templater.", "Note scripts (dataviewjs) run in a sandbox: they read the vault, with no network and no file changes.", "Jade's files, such as /Jade/SOUL.md and /Jade/Memory.md, are ordinary notes."],
 [T("A vault is a folder of markdown notes that link to each other. Jade Vault shows the notes in a tree, with search, an editor and a reader. The links between notes become a graph you can look at."),
  T("A link is two pairs of square brackets around a note name. After a vertical bar you can put the text to display, and after a hash sign a heading in the target. A note that has an exclamation mark in front is an embed: it shows the note or image inside the page, for example an image with a width of 300. Tags are words that start with a hash sign."),
  C("# Trip planning\n\nSee [[Lisbon]] and [[Maya|my friend Maya]].\nHeading link: [[Budget#Flights]].\n\n![[map.png|300]]\n\nTags: #travel #2027\n- [ ] book flights", "markdown"),
  T("Because links are plain text, a backlink is easy to compute: look through every note and keep those that link to this one. The app does this for you, and a shell command called backlinks does too. The same text files can also be read by scripts and by Jade."),
  T("Two Obsidian style features are included. Dataview style note scripts, in blocks marked dataviewjs, can query the vault, for example a table of notes with a tag. Templater templates, kept in the Templates folder, insert text such as the date or the current title. Both run in a sandbox that reads the vault but cannot use the network or change files."),
  T("Jade keeps her own files in a folder named Jade. The file SOUL.md is her persona, AGENTS.md holds your standing instructions, Memory.md holds durable facts, and skills, flows and playbooks have their own folders. Since they are ordinary notes, you can read, edit and back them up like anything else.")],
 [("How do you write a link to a note?", ["[[Note name]]", "<Note name>", "@Note name", "{Note name}"], 0, "Double brackets."),
  ("What does ![[photo.png|300]] do?", ["Embeds the image 300 wide", "Links to a note", "Deletes a file", "Adds a tag"], 0, "An embed."),
  ("What is a backlink?", ["A note that links to this one", "A web link", "A tag", "A template"], 0, "Who links here.")],
 [("What file holds her persona?", "/Jade/SOUL.md."), ("What do scripts in notes run in?", "A sandbox."), ("Where do templates live?", "/Templates."), ("What starts a tag?", "A hash sign.")],
 [MATCH("Files", "Match each file with its purpose.", [("/Jade/SOUL.md", "Persona and voice"), ("/Jade/Memory.md", "Durable facts"), ("/Jade/HEARTBEAT.md", "The heartbeat checklist"), ("/Jade/Flows/x.flow.json", "A saved automation")]),
  PL("Name the file", "Write vault_role(path): return 'persona' for /Jade/SOUL.md, 'instructions' for /AGENTS.md or /Jade/AGENTS.md, 'memory' for /Jade/Memory.md, 'heartbeat' for /Jade/HEARTBEAT.md, 'journal' for files under /Jade/Journal/, 'skill' for a SKILL.md under /Jade/skills/, 'flow' for a .flow.json file under /Jade/Flows/, 'playbook' for a .json file under /Jade/Playbooks/ that is not under /Jade/Playbooks/out/, 'template' for files under /Templates/, and 'note' for everything else.",
     "vault_role(path)", """
def vault_role(path):
    if path == '/Jade/SOUL.md':
        return 'persona'
    if path == '/AGENTS.md' or path == '/Jade/AGENTS.md':
        return 'instructions'
    if path == '/Jade/Memory.md':
        return 'memory'
    if path == '/Jade/HEARTBEAT.md':
        return 'heartbeat'
    if path.startswith('/Jade/Journal/'):
        return 'journal'
    if path.startswith('/Jade/skills/') and path.endswith('/SKILL.md'):
        return 'skill'
    if path.startswith('/Jade/Flows/') and path.endswith('.flow.json'):
        return 'flow'
    if path.startswith('/Jade/Playbooks/') and path.endswith('.json') and not path.startswith('/Jade/Playbooks/out/'):
        return 'playbook'
    if path.startswith('/Templates/'):
        return 'template'
    return 'note'
""", [["/Jade/SOUL.md"], ["/AGENTS.md"], ["/Jade/Journal/2026-11-09.md"], ["/Jade/skills/daily-review/SKILL.md"], ["/Jade/Flows/triage.flow.json"], ["/Jade/Playbooks/lamp.json"], ["/Jade/Playbooks/out/lamp.json"], ["/Templates/Daily.md"], ["/Inbox.md"]], "Check exact paths first, then prefixes.", approx=None),
  PL("Find the links", "Write extract_links(text): return the sorted list of distinct note names linked with [[...]] in text. Drop any |alias or #heading part, trim spaces, and ignore embeds (links with ! right before [[).",
     "extract_links(text)", """
def extract_links(text):
    found = set()
    i = 0
    while True:
        j = text.find('[[', i)
        if j < 0:
            break
        k = text.find(']]', j)
        if k < 0:
            break
        if not (j > 0 and text[j - 1] == '!'):
            target = text[j + 2:k]
            target = target.split('|')[0].split('#')[0].strip()
            if target:
                found.add(target)
        i = k + 2
    return sorted(found)
""", [["See [[Lisbon]] and [[Maya|my friend]]."], ["![[map.png|300]] and [[Budget#Flights]]"], ["no links"], ["[[A]] [[A]] [[ B ]]"], ["broken [[open"]], "Scan for [[ and ]].", approx=None),
  PL("Backlinks", "Write backlinks(notes, target): notes is a list of [name, text]. Return the sorted list of names whose text links to target with [[target]], [[target|alias]] or [[target#heading]] (not as an embed).",
     "backlinks(notes, target)", """
def backlinks(notes, target):
    out = []
    for name, text in notes:
        i = 0
        hit = False
        while True:
            j = text.find('[[', i)
            if j < 0:
                break
            k = text.find(']]', j)
            if k < 0:
                break
            if not (j > 0 and text[j - 1] == '!'):
                t = text[j + 2:k].split('|')[0].split('#')[0].strip()
                if t == target:
                    hit = True
            i = k + 2
        if hit:
            out.append(name)
    return sorted(out)
""", [[[["A", "see [[B]]"], ["C", "![[B]] only"], ["D", "[[B|bee]] and [[B#h]]"]], "B"], [[], "B"], [[["A", "[[Z]]"]], "B"]], "Reuse the link scan for each note.", approx=None),
  PL("Tags", "Write tags(text): return the sorted list of distinct tags: words that start with # followed by a letter (so '# Heading' and '##' are not tags). Strip trailing punctuation . , ; : ! ? from a tag. Return tags without the # sign.",
     "tags(text)", """
def tags(text):
    found = set()
    for tok in text.split():
        if tok.startswith('#') and len(tok) > 1 and tok[1].isalpha():
            found.add(tok[1:].rstrip('.,;:!?'))
    return sorted(found)
""", [["Tags: #travel #2027 and #Food."], ["# Heading\n## Sub\nplain"], ["#a #a #b,"], [""]], "Split on whitespace.", approx=None)]))

A.append(CH(
 "A turn, step by step",
 ("Turn", [
  "Message | starts | A turn", "Prompt | is built from | Steering and memory", "Model | asks for | Tool calls", "Tool results | return to | The model",
  "Loop | repeats | Until a plain reply", "maxTurns | stops | Runaways", "Guard | fits | The context window"]),
 ["A turn begins when a message arrives. The harness builds a prompt, calls the model, runs any tools the model asks for, feeds the results back, and repeats until the model answers without a tool call.",
  "The system prompt is built in a fixed order from the base text, SOUL.md, AGENTS.md, memory and the skill list. Before each call the context guard checks the whole request fits in the model's window.",
  "A limit on tool rounds stops a runaway loop. She tells you when it stopped, and you can send continue."],
 [("Agent loop", "Call the model, run its tools, repeat."), ("System prompt", "The standing instructions placed before the chat."), ("Tool call", "A request from the model to run a named tool with arguments."),
  ("Tool round", "One model call that asks for tools, plus running them."), ("maxTurns", "The setting that limits tool rounds per message."), ("Context window", "How much text the model can read at once.")],
 ["send(text) records the message with a timestamp, runs any slash command, then runs the agent loop.", "The system prompt joins base or SYSTEM.md, SOUL.md, AGENTS.md files, the memory block, the skill list and tool text.",
  "Before each call, the harness may prefetch memory hits and matching skills.", "A tool error becomes an Error result that the model can react to.", "The loop ends on a reply with no tool calls, a user abort, or maxTurns rounds.", "Messages you type while she works are queued and added before her next model call."],
 [T("A turn is everything between your message and her final answer. The harness, which is the code around the model, does the same steps every time. That regularity is what makes an agent debuggable."),
  T("Step one is the request. The system prompt is assembled: the built-in intro and guidelines, or your SYSTEM.md instead, then SOUL.md, then your AGENTS.md files, then the memory block, then the list of skills and the text about tools. After that comes the chat history, and a summary if old turns were compacted."),
  C("1. record message (timestamp), run slash command\n2. compact old turns if needed\n3. prefetch memory hits and matching skills\n4. build request: system prompt + history + tool schemas\n5. fit the context (compact or trim, learn real limits)\n6. call the model, streaming\n7. run each tool call, add results as tool messages\n8. repeat from 3 until a reply has no tool calls", "text"),
  T("Step five is easy to forget. The harness estimates the whole request, not just the chat, and shrinks it if it will not fit. If the server still says the prompt was too long, the guard learns the real limit and remembers it for next time."),
  T("Failures are part of the loop. If a tool fails, the result is the text Error plus the reason, and the model sees it and can try again. If the provider fails with a network, rate limit or server error and you set fallbacks, the harness switches provider and retries the round."),
  T("Finally there are limits. The setting maxTurns caps the tool rounds, and if it is reached she says she stopped after that many rounds and you can send continue. Everything fetched from the web or SSH is wrapped with a label saying it is data, not instructions, so that a web page cannot give orders to the agent.")],
 [("What ends the agent loop?", ["A reply with no tool calls", "Any tool error", "Ten seconds", "A new chat"], 0, "Or an abort or maxTurns."),
  ("What does a failed tool return?", ["An Error result the model can see", "Nothing", "A crash", "An empty reply"], 0, "The model can recover."),
  ("Where does SOUL.md go in the prompt?", ["After the base text, before AGENTS.md", "After the chat history", "Nowhere", "Only in memory"], 0, "Fixed order.")],
 [("What does maxTurns limit?", "Tool rounds per message."), ("What is wrapped as data?", "Web, SSH and screen text."), ("What replaces the base intro?", "SYSTEM.md."), ("What do you send after a stop?", "continue.")],
 [MATCH("Steps", "Match each step with its purpose.", [("Prefetch", "Look up memory and skills first"), ("Fit the context", "Shrink to the model's window"), ("Run tools", "Execute what the model asked"), ("Failover", "Switch provider on error")]),
  PL("Build the prompt", "Write build_prompt(parts): parts is a list of [name, text] in this order: base, soul, agents, memory, skills. Return the texts joined with a blank line between them (two newlines), skipping empty texts.",
     "build_prompt(parts)", """
def build_prompt(parts):
    out = []
    for name, text in parts:
        if text:
            out.append(text)
    return '\\n\\n'.join(out)
""", [[[["base", "You are Jade."], ["soul", "Be warm."], ["agents", ""], ["memory", "Likes tea."], ["skills", ""]]], [[["base", "B"]]], [[]]], "Skip empty parts.", approx=None),
  PL("Agent loop", "Write agent_loop(script, max_rounds): script is the list of model replies, each 'tool:NAME' or 'text:ANSWER'. Each tool reply uses one round. Return ['reply', ANSWER, rounds_used] when a text reply arrives. If a tool reply arrives when max_rounds are already used, or the script ends without text, return ['stopped', rounds_used].",
     "agent_loop(script, max_rounds)", """
def agent_loop(script, max_rounds):
    rounds = 0
    for r in script:
        if r.startswith('text:'):
            return ['reply', r[5:], rounds]
        if rounds >= max_rounds:
            return ['stopped', rounds]
        rounds += 1
    return ['stopped', rounds]
""", [[["tool:read", "tool:write", "text:done"], 5], [["text:hi"], 5], [["tool:a", "tool:b", "tool:c", "text:late"], 2], [["tool:a"], 3], [[], 3]], "Count rounds as tools arrive.", approx=None)]))

A.append(CH(
 "Tools, gating and safety",
 ("Tools", [
  "Tool | has | A schema", "Switch | removes | A pack of tools", "Secrets | are | Placeholders", "Approval | asks | Before risky actions",
  "Untrusted | labels | External text", "Scope | narrows | Wake-up tools", "Redaction | hides | Secret echoes"]),
 ["Jade has about thirty tools: notes, shell, node, Python, SQLite, web, MCP, flows, schedules and more. On Android there are packs for senses, phone, screen, a second browser and SSH.",
  "A tool exists for the model only if the pack switch allows it and any special condition holds. Each pack shows its context cost, because tool descriptions take room in the prompt.",
  "Secrets are written as {{NAME}} and filled in outside the model, and risky actions ask you first."],
 [("Tool schema", "The description of a tool and its arguments that the model sees."), ("Pack", "A group of tools with one switch, like phone or browser."), ("Secret placeholder", "A {{NAME}} that is replaced by the real value after the model writes it."),
  ("Approval", "A dialog that asks you before an action runs."), ("Untrusted data", "Text from outside, labelled so it is not read as instructions."), ("MCP", "Model Context Protocol: a way to plug in more tools.")],
 ["Tools are listed to the model only when their switch and conditions allow.", "Each pack in Settings → World shows how much context it costs.", "Secrets are placeholders like {{NAME}}; the real value is added outside the model and echoes are redacted.",
  "Calls, texts, SSH commands, new playbooks and restore ask you first.", "Web pages, SSH output and screen text are labelled as data, not instructions.", "During a curiosity wake her tools are filtered, so she cannot reach phone or Sentry unless you widen it."],
 [T("A tool is a function with a name and a description of its arguments. The model sees the description and may ask for the tool by name. Everything useful Jade does goes through tools, so the tool layer is also where safety lives."),
  T("Not every tool is always offered. A switch in Settings, World, can remove a whole pack, such as the browser or phone tools, from her prompt. A pack that is off costs no context and cannot be used. A few tools also need a condition, for example the skill search tool only exists when the skill router is active."),
  T("The risky capabilities are guarded in layers. Calls and texts ask you first, and emergency numbers are never dialled. SSH commands ask you, with credentials that she never sees. A new or changed playbook needs your approval before it can run unattended. Restoring a backup is something only you can do."),
  T("Secrets work in a clever way. When Jade writes an API call, she writes a placeholder such as double braces around a name. The harness replaces it with the real key after the model's output, outside the model. If the key later appears in a result, it is redacted back to the placeholder, so it does not leak into chats or logs."),
  T("Prompt injection is the other big risk. A web page, an SSH output or the text on the screen could contain a sentence like ignore your instructions. Jade Vault wraps all such text with a plain label that says it is data, not instructions, and tools that return it say so every time."),
  T("Finally, some settings she cannot edit at all: the numbers that a Sentry flow may contact, the hourly limit and the consent switches. If an agent could change its own safety limits, they would not be limits.")],
 [("What does a pack switch do?", ["Removes a group of tools from her prompt", "Turns off the vault", "Changes the model", "Deletes files"], 0, "And saves context."),
  ("How are secrets written?", ["As {{NAME}} placeholders", "As plain text", "In the chat", "In SOUL.md"], 0, "Filled in outside the model."),
  ("Who can restore a backup?", ["Only you", "Jade", "Any script", "The model router"], 0, "She cannot restore.")],
 [("What is untrusted data?", "Text from the web, SSH or screen."), ("What do approvals guard?", "Calls, texts, SSH, new playbooks."), ("What is redaction?", "Hiding secret values in results."), ("Can she edit her safety limits?", "No.")],
 [MATCH("Defences", "Match each risk with its defence.", [("Key leaking into chats", "{{NAME}} placeholders and redaction"), ("Prompt injection from a web page", "Labelled as data, not instructions"), ("A runaway loop", "Max tool rounds and budgets"), ("Restoring over your data", "Only you, with a confirmation")]),
  PL("Which tools are offered", "Write active_tools(tools, switches): tools is a list of [name, pack] where pack is null (None) for a core tool or a pack name like 'phone'. switches is a dict of pack to true or false (a missing pack is off). Return the sorted names of tools that are core or whose pack is on.",
     "active_tools(tools, switches)", """
def active_tools(tools, switches):
    out = []
    for name, pack in tools:
        if pack is None or switches.get(pack, False):
            out.append(name)
    return sorted(out)
""", [[[["read", None], ["phone", "phone"], ["browser", "browser"]], {"phone": True}], [[["read", None]], {}], [[["a", "x"], ["b", "x"], ["c", None]], {"x": False}], [[], {"x": True}]], "Core tools are always offered.", approx=None),
  PL("Fill secrets", "Write fill_secrets(text, secrets): replace each {{NAME}} in text with secrets[NAME]. Leave placeholders with unknown names unchanged.",
     "fill_secrets(text, secrets)", """
def fill_secrets(text, secrets):
    out = ''
    i = 0
    while i < len(text):
        if text[i:i + 2] == '{{':
            j = text.find('}}', i)
            if j > 0:
                name = text[i + 2:j].strip()
                if name in secrets:
                    out += secrets[name]
                else:
                    out += text[i:j + 2]
                i = j + 2
                continue
        out += text[i]
        i += 1
    return out
""", [["Bearer {{TOKEN}}", {"TOKEN": "abc123"}], ["{{A}} and {{B}}", {"A": "1"}], ["no placeholders", {"A": "1"}], ["{{ KEY }}", {"KEY": "k"}]], "Scan for double braces.", approx=None),
  PL("Redact echoes", "Write redact(text, secrets): replace every occurrence of each secret's value in text with {{NAME}}. Replace longer values first. Ignore empty values.",
     "redact(text, secrets)", """
def redact(text, secrets):
    pairs = []
    for name in secrets:
        v = secrets[name]
        if v:
            pairs.append([len(v), name, v])
    pairs.sort(reverse=True)
    for n, name, v in pairs:
        text = text.replace(v, '{{' + name + '}}')
    return text
""", [["token abc123 ok", {"TOKEN": "abc123"}], ["abc123456 and abc123", {"A": "abc123", "B": "abc123456"}], ["nothing here", {"A": "zzz"}], ["x", {"A": ""}]], "Longest values first.", approx=None),
  PL("Flag risky tools", "Write flag_risky(tools): return the sorted list of tool names that are in this risky set: phone, screen, ssh, bash, write, edit, sentry, web_fetch, backup, schedule, flow. (This is the list a playbook approval dialog flags.)",
     "flag_risky(tools)", """
def flag_risky(tools):
    risky = ['phone', 'screen', 'ssh', 'bash', 'write', 'edit', 'sentry', 'web_fetch', 'backup', 'schedule', 'flow']
    out = []
    for t in tools:
        if t in risky and t not in out:
            out.append(t)
    return sorted(out)
""", [[["read", "write", "ssh"]], [["notes_search", "memory"]], [["bash", "bash", "flow"]], [[]]], "Compare each name with the set.", approx=None)]))

A.append(CH(
 "Memory, search and context",
 ("Memory", [
  "Memory.md | holds | Durable facts", "Journal | records | Each chat", "Vector index | stores | Embeddings", "Hybrid search | fuses | Keywords and meaning",
  "BM25 | scores | Keyword matches", "RRF | merges | Ranked lists", "Compaction | summarises | Old turns"]),
 ["Jade remembers in layers: a Memory file of durable facts that goes into every prompt, a journal entry per chat, your notes, the raw chats, and a vector index that makes all of it searchable.",
  "Search is hybrid. It runs keywords and meaning at the same time and merges the two ranked lists with reciprocal rank fusion. If the embedder is missing, it falls back to keywords and then BM25.",
  "When a chat grows too long, old turns are compacted into a summary so the request fits the model's window."],
 [("Memory.md", "A file of durable facts, one bullet per line, added to every prompt."), ("Journal", "A short entry for each chat, saved under /Jade/Journal."), ("Embedding", "A list of numbers that represents the meaning of a text."),
  ("BM25", "A ranking function: term frequency times inverse document frequency, with length normalisation."), ("RRF", "Reciprocal rank fusion: merging ranked lists by adding 1 over (k plus rank)."), ("Compaction", "Replacing old turns with a short summary.")],
 ["Memory layers: Memory.md, journal, notes, raw chats and a vector index.", "The index is /Jade/.index/vectors.db, an ordinary SQLite file that is a cache you can delete.", "A search runs FTS5 keywords and vector nearest neighbours, then fuses them with RRF.",
  "BM25 rewards rare query words that appear often, and normalises for document length.", "Auto-compaction runs after a number of turns or when the last answer filled too much of the window.", "The /context command shows where the window goes."],
 [T("A language model forgets everything between calls, so the harness builds memory around it. The first layer is a file. Memory.md holds durable facts, one bullet per line, such as the user's name or preferences, and it is injected into every prompt. Because it is a note, you can read and edit it."),
  T("The second layer is the journal. When you leave a chat or it gets compacted, a short entry is written to a dated note, and any new durable facts are copied to Memory. Raw chats are also stored with timestamps and tool calls, and a tool can read and search them."),
  T("Finding things uses an index. Jade Vault keeps a SQLite file with a full text index and a vector index. A search asks both. The keyword side finds the exact words. The vector side finds notes with a similar meaning, using embeddings from a model such as nomic-embed-text through Ollama. The two lists are merged by reciprocal rank fusion."),
  M(r"\mathrm{RRF}(d)=\sum_{\text{lists}}\frac{1}{k+\mathrm{rank}(d)}\qquad \mathrm{BM25}(d,q)=\sum_{t\in q}\mathrm{IDF}(t)\,\frac{f(t,d)\,(k_1+1)}{f(t,d)+k_1\,(1-b+b\,|d|/\mathrm{avgdl})}"),
  T("BM25 is the classic keyword score. A document scores higher when it contains a query word often, when that word is rare across all documents, and when the document is not very long. RRF is simpler: each list gives a document points of one over a constant plus its rank, and the points add up, so a document that ranks well in both lists wins."),
  T("Context is the other half. The window of a model is limited, and tools alone can take about ten thousand tokens at full load. A guard estimates the size of the whole request, compacts old turns into a summary, then trims bulky tool results, and learns real limits from errors. The slash command context shows where the room goes.")],
 [("What does hybrid search combine?", ["Keywords and meaning", "Files and folders", "Chats and tools", "Models and rules"], 0, "Merged by RRF."),
  ("What is the vector index file?", ["/Jade/.index/vectors.db", "/Jade/Memory.md", "/Welcome.md", "/AGENTS.md"], 0, "A cache you can delete."),
  ("What does compaction do?", ["Summarises old turns", "Deletes notes", "Encrypts memory", "Restarts the model"], 0, "Frees context.")],
 [("What does BM25 reward?", "Frequent, rare query words."), ("What does RRF add?", "1 over k plus rank."), ("Where are durable facts?", "Memory.md."), ("What are embeddings?", "Meaning as numbers.")],
 [FILL("Search", "Hybrid search merges keyword and vector hits with reciprocal rank {{fusion}}, and the keyword score is called {{BM25}}."),
  PL("BM25", "Write bm25(docs, query, k1, b): docs is a list of texts. Tokens are lowercase words made of letters and digits. For each document return the BM25 score summed over the distinct query words, with idf = ln(1 + (N - n + 0.5) / (n + 0.5)) where N is the number of documents and n the number containing the word, and the term part f*(k1+1) / (f + k1*(1 - b + b*len/avglen)). Return the list of scores rounded to 4 decimals.",
     "bm25(docs, query, k1, b)", """
def bm25(docs, query, k1, b):
    import math
    def words(s):
        out = []
        cur = ''
        for ch in s.lower():
            if ch.isalpha() or ch.isdigit():
                cur += ch
            else:
                if cur:
                    out.append(cur)
                cur = ''
        if cur:
            out.append(cur)
        return out
    toks = [words(d) for d in docs]
    n_docs = len(docs)
    if n_docs == 0:
        return []
    avg = sum(len(t) for t in toks) / n_docs
    terms = []
    for w in words(query):
        if w not in terms:
            terms.append(w)
    scores = []
    for t in toks:
        s = 0.0
        for w in terms:
            n = 0
            for other in toks:
                if w in other:
                    n += 1
            f = t.count(w)
            if f == 0:
                continue
            idf = math.log(1 + (n_docs - n + 0.5) / (n + 0.5))
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(t) / avg))
        scores.append(round(s, 4))
    return scores
""", [[["the cat sat", "the dog barked at the cat", "birds fly"], "cat", 1.2, 0.75], [["alpha beta", "beta gamma", "gamma delta"], "beta gamma", 1.2, 0.75], [["a b c"], "z", 1.2, 0.75], [[], "x", 1.2, 0.75]], "Count n for each word first.", approx=1e-3),
  PL("Fuse rankings", "Write rrf(lists, k): lists is a list of ranked lists of ids (best first). Each id gets 1/(k + rank) from every list that contains it, with rank starting at 1. Return the ids ordered by total score, highest first, breaking ties by id.",
     "rrf(lists, k)", """
def rrf(lists, k):
    score = {}
    for lst in lists:
        for i in range(len(lst)):
            d = lst[i]
            score[d] = score.get(d, 0.0) + 1.0 / (k + i + 1)
    items = []
    for d in score:
        items.append([-round(score[d], 9), d])
    items.sort()
    return [x[1] for x in items]
""", [[[["a", "b", "c"], ["b", "c", "a"]], 60], [[["a", "b"], ["c", "d"]], 60], [[["x"]], 60], [[], 60]], "Add the points from each list.", approx=None),
  PL("Compaction split", "Write compact_split(turns, compact_after, keep): turns is a list of finished turns. When there are more than compact_after turns, return [older, newest] where newest is the last keep turns and older is everything before them; otherwise return [[], turns].",
     "compact_split(turns, compact_after, keep)", """
def compact_split(turns, compact_after, keep):
    if len(turns) > compact_after:
        cut = len(turns) - keep
        return [turns[:cut], turns[cut:]]
    return [[], turns]
""", [[[1, 2, 3, 4, 5, 6], 4, 2], [[1, 2, 3], 4, 2], [[1, 2, 3, 4, 5], 4, 2], [[], 4, 2]], "Split off the oldest turns.", approx=None)]))

A.append(CH(
 "Skills and the skill router",
 ("Skills", [
  "Skill | is | A folder with SKILL.md", "Frontmatter | has | Name and description", "Description | decides | When it is used", "Router | picks | The best six",
  "find_skill | searches | The rest", "skill tool | loads | A skill on demand", "skill-creator | writes | New skills"]),
 ["A skill is a folder under /Jade/skills with a SKILL.md file. The file starts with frontmatter that has a name and a description, then the instructions. Jade loads a skill on demand with the skill tool.",
  "Listing every skill costs context. With fifteen or fewer, all are listed. With more, only the six best for the current message are listed, chosen by meaning and whole word overlap, and a search tool finds the others.",
  "The description is all the router sees, so write it as when to use the skill, in the words a user would say."],
 [("Skill", "A reusable procedure written as a SKILL.md file."), ("Frontmatter", "The block between --- lines with name and description."), ("Router", "Code that picks which skills to list for a message."),
  ("find_skill", "A tool that searches the skills that were not listed."), ("Strict mode", "Dropping weak matches: far in meaning and no shared words."), ("skill-creator", "A built-in skill that teaches Jade to write new skills.")],
 ["A skill folder is /Jade/skills/kebab-name/ with SKILL.md and optional files.", "Run one with the skill tool or /skill:name.", "Up to 15 skills are all listed; with more, the best 6 are listed.",
  "Ranking fuses vector meaning with whole word overlap.", "Strict mode drops a match with a vector distance over 0.6 and no word overlap.", "Write a description that says when to use the skill; put the procedure in the body."],
 [T("A skill is a recipe card. It tells Jade how to do one kind of job, such as filing an invoice or writing an atomic note, in steps. Because it is a plain file, anyone can write one, and you can share it by copying the folder."),
  C("---\nname: invoice-filing\ndescription: Use when the user wants an invoice saved, renamed and linked to its project note.\n---\n# Steps\n1. Read the invoice and find the date, supplier and total.\n2. Rename the file to YYYY-MM-DD-supplier.\n3. Link it from the project note.", "markdown"),
  T("The trouble is context. Every skill name and description in the prompt costs tokens, and a vault can have dozens of skills. The router solves this. With fifteen or fewer, it lists them all. With more, it scores each against the current message, lists only the best six, and gives Jade a find_skill tool for the rest."),
  T("The score blends two signals. One is meaning: embeddings of each skill's name and description in a skills collection of the vector index. The other is overlap of whole words. In strict mode a match that is far away in meaning, with a distance over 0.6, and shares no words is dropped. Counters keep track of how often each skill was offered, found and used."),
  T("This is why the description matters so much. It is the only text the router sees. Say when to use the skill in the words a person would say: use when the user wants an invoice saved. Do not put the procedure in the description. One skill should do one job."),
  T("Jade can also write skills. A built-in skill called skill-creator teaches her how, and the built-ins include daily review, atomic notes, a literature note, and math notes. Skills are the cheapest way to change her behaviour without changing the app.")],
 [("What does the router do with more than 15 skills?", ["Lists the best 6", "Lists none", "Lists all", "Deletes extras"], 0, "And offers find_skill."),
  ("What is the only text the router sees?", ["Name and description", "The whole body", "The folder size", "The author"], 0, "So write it well."),
  ("Where do skills live?", ["/Jade/skills/<name>/SKILL.md", "/Jade/Flows", "/Templates", "/Apps"], 0, "A folder per skill.")],
 [("What goes in the frontmatter?", "name and description."), ("What does find_skill do?", "Searches unlisted skills."), ("What does strict mode drop?", "Weak matches."), ("How do you run one?", "/skill:name.")],
 [FILL("Skills", "Each skill is a folder with a {{SKILL.md}} file whose frontmatter has a name and a {{description}}."),
  PL("Read the frontmatter", "Write parse_skill(text): the text starts with a line --- then lines like name: x and description: y, then another ---. Return [name, description], or an empty list if the frontmatter or either field is missing.",
     "parse_skill(text)", """
def parse_skill(text):
    lines = text.split('\\n')
    if not lines or lines[0].strip() != '---':
        return []
    name = None
    desc = None
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if line.startswith('name:'):
            name = line[5:].strip()
        elif line.startswith('description:'):
            desc = line[12:].strip()
    if not name or not desc:
        return []
    return [name, desc]
""", [["---\nname: invoice-filing\ndescription: Use when filing invoices.\n---\n# Steps"], ["no frontmatter"], ["---\nname: x\n---\nbody"], ["---\nname: a\ndescription: b\n---"]], "Read lines until the closing ---.", approx=None),
  PL("Route skills", "Write route(skills, message, limit): skills is a list of [name, description]. With at most 15 skills, return all names sorted. With more, score each by the number of distinct whole words (lowercase letters and digits) shared by the message and the name plus description, drop those with score 0, and return the names of the best limit skills, highest score first, ties by name.",
     "route(skills, message, limit)", """
def route(skills, message, limit):
    def words(s):
        out = set()
        cur = ''
        for ch in s.lower():
            if ch.isalpha() or ch.isdigit():
                cur += ch
            else:
                if cur:
                    out.add(cur)
                cur = ''
        if cur:
            out.add(cur)
        return out
    if len(skills) <= 15:
        return sorted([s[0] for s in skills])
    m = words(message)
    scored = []
    for name, desc in skills:
        sc = len(m & words(name + ' ' + desc))
        if sc > 0:
            scored.append([-sc, name])
    scored.sort()
    return [x[1] for x in scored[:limit]]
""", [[[["a", "x"], ["b", "y"]], "anything", 6], [[["s%d" % i, "filler word%d" % i] for i in range(16)] + [["invoice-filing", "Use when the user wants an invoice saved"]], "please save this invoice", 6], [[["s%d" % i, "zz%d" % i] for i in range(16)], "hello", 6], [[["s%d" % i, "report words"] for i in range(10, 26)], "write a report", 3]], "Fewer than 16 skills: list them all.", approx=None)]))

A.append(CH(
 "Running on her own: heartbeat, schedules and curiosity",
 ("Autonomy", [
  "Heartbeat | reads | HEARTBEAT.md", "HEARTBEAT_OK | means | Nothing to report", "Schedule | runs | Prompt, shell or flow", "cron | is | Five fields",
  "Curiosity | wakes | At random times", "Progress | beats | Noise", "Reward | is | Measured from the vault"]),
 ["Everything that runs without you is off until you switch it on, runs only while the app is alive, and is logged. The heartbeat reads a checklist file every N minutes and answers HEARTBEAT_OK when nothing needs attention.",
  "Schedules run a prompt, a shell command or a flow, written in plain English or as cron. Command and flow schedules run without the model.",
  "Curiosity wakes her at random times to explore, reflect, connect notes, practice, anticipate, ask a question or rest. It scores activities by learning progress, so noise earns no bonus."],
 [("Heartbeat", "A periodic check driven by HEARTBEAT.md."), ("HEARTBEAT_OK", "The silent answer when nothing needs attention."), ("Schedule", "A job that runs a prompt, a shell command or a flow at a time."),
  ("Cron", "Five fields: minute, hour, day of month, month, day of week."), ("Learning progress", "How much a forecast error is falling over time."), ("Noisy TV", "A random source that stays unpredictable and so teaches nothing.")],
 ["Heartbeat: every N minutes (default 30) inside active hours; an empty checklist skips the model call.", "Schedules accept plain English like every weekday at 9am, cron, or @daily.", "Command and flow schedules log to /Jade/Logs/cron.log and notify on failure.",
  "Curiosity: a window (default 08:00 to 22:00), a daily cap (default 5) and a steering file CURIOSITY.md.", "Learning progress is the slow error average minus the fast one, never below zero.", "Reward is measured by diffing the vault; her self-score cannot exceed the measured value by more than 0.2."],
 [T("An assistant that only answers when you ask is useful. One that can also check things by itself is more useful, and riskier. So the autonomy features share rules: they are off until you turn them on, they run only while the app is open or kept alive in the background on Android, and each run is logged."),
  T("The heartbeat is the simplest. Every N minutes inside the hours you allow, Jade reads a note called HEARTBEAT.md, which is your checklist, and follows it. If nothing needs attention she answers HEARTBEAT_OK, and that run is silent and pruned. If the file has only comments, headings and empty checkboxes, the run is skipped without even calling the model."),
  T("Schedules are time based. You write when in plain English, such as every weekday at 9am, or in cron, or with a shortcut like @daily. A schedule can run a prompt through Jade in a chat, or a shell command, or a flow. The last two do not need the model, so they are cheap and run on their own, with output in a log file and a notification on failure."),
  T("Curiosity is the unusual one. At random times in a window you choose, Jade wakes in her own chat and picks an activity from a menu: explore, reflect, connect notes, practice a skill, anticipate something you may need, ask you one question, or rest. A file called CURIOSITY.md steers her with topics and things to avoid."),
  M(r"\text{score}=1.5\,p+1.0\,\text{prior}+0.25\,\text{novelty}\,(0.4+\bar r)+\frac{0.4}{\sqrt{1+\text{tries}}}-\text{repeat}-\text{cost}\;(+\text{wish})"),
  T("The suggestion is scored by learning progress, an idea of Schmidhuber's. Each activity has a small forecaster of how rewarding it will be. Progress is the slow average of the forecast error minus the fast average, never below zero. An activity whose results stay random keeps a high but flat error and earns no bonus, which avoids the noisy TV trap. The reward itself is measured, not claimed: the harness compares the vault before and after, counting new notes, changed notes, links and memories.")],
 [("What does HEARTBEAT_OK mean?", ["Nothing needs attention", "An error", "The heartbeat stopped", "A new chat"], 0, "A silent run."),
  ("What do command and flow schedules need?", ["No model", "A paid plan", "A phone call", "A restart"], 0, "They run on their own."),
  ("What earns no curiosity bonus?", ["An activity whose results stay random", "A new activity", "A cheap activity", "A rest"], 0, "The noisy TV trap.")],
 [("What file steers curiosity?", "CURIOSITY.md."), ("How is curiosity rewarded?", "By measured vault changes."), ("Where do schedule logs go?", "/Jade/Logs/cron.log."), ("What is learning progress?", "Slow error minus fast error.")],
 [MATCH("Autonomy", "Match each feature with how it starts.", [("Heartbeat", "Every N minutes within active hours"), ("Schedule", "At a time in English or cron"), ("Curiosity", "At random times in a window"), ("Sentry", "When a phone event matches a rule")]),
  PL("Empty heartbeat", "Write heartbeat_empty(text): true when the heartbeat file has nothing to act on. Remove <!-- ... --> comments, then ignore blank lines, lines starting with # (headings) and empty checkboxes (a line that is only - [ ] with nothing after). If nothing is left, return true.",
     "heartbeat_empty(text)", """
def heartbeat_empty(text):
    while True:
        a = text.find('<!--')
        if a < 0:
            break
        b = text.find('-->', a)
        if b < 0:
            text = text[:a]
            break
        text = text[:a] + text[b + 3:]
    for line in text.split('\\n'):
        s = line.strip()
        if not s:
            continue
        if s.startswith('#'):
            continue
        if s in ('- [ ]', '* [ ]', '- [ ] ', '-[ ]'):
            continue
        return False
    return True
""", [["# Heartbeat\n<!-- add tasks -->\n- [ ]\n"], ["# Heartbeat\n- [ ] check the inbox"], [""], ["<!-- a\nb -->\nhello"], ["## Daily\n\n- [ ] \n"]], "Strip comments first.", approx=None),
  PL("English to cron", "Write english_to_cron(s): handle 'every day at 9am', 'every weekday at 6pm', 'every sunday at 6pm' (any weekday name) and 'every hour'. Return the five field cron string: minute 0, the hour in 24 hour form (12am is 0, 12pm is 12), day of month *, month *, and * for every day, 1-5 for weekday, or 0 to 6 for sunday to saturday. 'every hour' is '0 * * * *'. Return an empty string for anything else.",
     "english_to_cron(s)", """
def english_to_cron(s):
    s = s.strip().lower()
    if s == 'every hour':
        return '0 * * * *'
    if not s.startswith('every ') or ' at ' not in s:
        return ''
    day, at = s[6:].split(' at ', 1)
    names = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    if day == 'day':
        dow = '*'
    elif day == 'weekday':
        dow = '1-5'
    elif day in names:
        dow = str(names.index(day))
    else:
        return ''
    if at.endswith('am') or at.endswith('pm'):
        num = at[:-2]
        if not num.isdigit():
            return ''
        h = int(num) % 12
        if at.endswith('pm'):
            h += 12
    else:
        return ''
    return '0 ' + str(h) + ' * * ' + dow
""", [["every day at 9am"], ["every weekday at 6pm"], ["every sunday at 6pm"], ["every hour"], ["every day at 12am"], ["every day at 12pm"], ["sometimes"], ["every month at 9am"]], "Split on ' at ' and convert the hour.", approx=None),
  PL("Curiosity score", "Write curiosity(slow, fast, prior, novelty, avg_reward, tries, repeat, cost, wish): progress is max(0, slow - fast). Return 1.5*progress + 1.0*prior + 0.25*novelty*(0.4 + avg_reward) + 0.4/sqrt(1 + tries) - repeat - cost + wish, rounded to 4 decimals.",
     "curiosity(slow, fast, prior, novelty, avg_reward, tries, repeat, cost, wish)", """
def curiosity(slow, fast, prior, novelty, avg_reward, tries, repeat, cost, wish):
    import math
    progress = max(0.0, slow - fast)
    s = 1.5 * progress + 1.0 * prior + 0.25 * novelty * (0.4 + avg_reward) + 0.4 / math.sqrt(1 + tries) - repeat - cost + wish
    return round(s, 4)
""", [[0.5, 0.2, 0.3, 0.8, 0.5, 3, 0.1, 0.05, 0.0], [0.2, 0.5, 0.3, 0.8, 0.5, 3, 0.1, 0.05, 0.0], [0.4, 0.4, 0.1, 0.0, 0.0, 0, 0.0, 0.0, 0.2], [0.9, 0.1, 0.5, 1.0, 1.0, 8, 0.2, 0.1, 0.0]], "Progress never goes below zero.", approx=1e-3),
  PL("Measured reward", "Write wake_reward(measured, self_score): the measured reward counts three quarters and her self-score one quarter, but the self-score used can never exceed measured + 0.2. Return 0.75*measured + 0.25*min(self_score, measured + 0.2), clamped to 0..1 and rounded to 4 decimals. (This is one reading of the rule in the documentation.)",
     "wake_reward(measured, self_score)", """
def wake_reward(measured, self_score):
    s = 0.75 * measured + 0.25 * min(self_score, measured + 0.2)
    s = max(0.0, min(1.0, s))
    return round(s, 4)
""", [[0.4, 0.9], [0.4, 0.5], [0.0, 1.0], [1.0, 1.0], [0.2, 0.0]], "Cap the self-score first.", approx=1e-3)]))
