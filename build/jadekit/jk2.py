"""Jade Agent Kit course, chapters 7-13."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

B = []

B.append(CH(
 "Tools for language models",
 ("Tools", [
  "kit.tools | describes | Tools to a model", "OpenAI shape | uses | type function", "Anthropic shape | uses | input_schema", "kit.tool | runs | A tool by name",
  "Result | is always | A string", "Failure | starts with | Error:", "tools.add | registers | Your own tool"]),
 ["A language model cannot touch files or run code by itself. It can only ask for a tool call. kit.tools gives the model a description of each tool, and kit.tool(name, args) runs the call and returns the result as text.",
  "The kit generates definitions in two shapes: the OpenAI shape, which Ollama also uses, and the Anthropic shape. You can add your own tools with a description, a JSON Schema for the inputs and a run function.",
  "The labs build a dispatcher and a schema generator."],
 [("Tool", "A function the model may ask to run."), ("JSON Schema", "A standard way to describe the shape of arguments."), ("Dispatcher", "Code that runs a tool by name."),
  ("Tool call", "The model's request: a name and arguments."), ("Tool result", "Text returned to the model."), ("Subset", "A chosen list of tools to offer.")],
 ["kit.tools.openai() returns { type: 'function', function: { name, description, parameters } } entries.", "kit.tools.anthropic(['read', 'bash']) returns { name, description, input_schema } entries.", "kit.tool(name, args) always returns a string; errors begin with 'Error:'.",
  "Built in: read, write, edit, bash, python, javascript, sqlite, search_files, decide, tasks, schedule, sentry, search, fetch.", "kit.tools.add(name, { description, parameters, run }) registers a tool.", "edit needs oldText to be unique unless replaceAll is set."],
 [T("Picture a model as a clever person in a locked room who can pass notes through a slot. The note says: please read this file. You do it and pass the contents back. Tools are the list of requests you are willing to carry out, and the description of each tells the model how to ask."),
  C("kit.tools.add('now', {\n  description: 'the time',\n  parameters: { type: 'object', properties: {} },\n  run: () => new Date().toISOString()\n});\n\nconst tools = kit.tools.openai();   // now includes 'now'\nconst time = await kit.tool('now', {});", "js"),
  T("There are two description shapes because providers differ. In the OpenAI shape every entry says type function and holds the name, a description and a parameters schema. In the Anthropic shape the entry has name, description and input_schema. The content is the same."),
  T("The dispatcher kit.tool takes a name and an arguments object and always returns a string. If something goes wrong, the string begins with the word Error and a colon. Checking that prefix is how your code, or the model, notices failure. Returning text instead of throwing lets the model read the error and try again."),
  T("The edit tool shows careful tool design. It replaces exact text, and the old text must appear exactly once unless replaceAll is set. That stops the model from changing the wrong place by accident."),
  T("Most of the other built-ins are tools you have already met: python, javascript and sqlite run code, search_files uses BM25, decide asks a decision model, and tasks, schedule and sentry manage lists, jobs and rules. The search and fetch tools use Ollama Cloud and need a cloud key.")],
 [("What does kit.tool always return?", ["A string", "An object", "A promise of a file", "A boolean"], 0, "Failures start with Error:."),
  ("What is the Anthropic tool shape's schema field called?", ["input_schema", "parameters", "args", "schema"], 0, "The OpenAI shape uses parameters."),
  ("Why must edit's oldText be unique?", ["To avoid changing the wrong place", "To save memory", "To speed up search", "It is a style rule"], 0, "Unless replaceAll is set.")],
 [("How do you offer a subset of tools?", "Pass a list of names."), ("What do search and fetch need?", "An Ollama Cloud key."), ("What does bash keep?", "A persistent shell session."), ("What does a tool definition need?", "description, parameters, run.")],
 [MATCH("Tool shapes", "Match the shape with its field.", [("OpenAI function", "parameters"), ("Anthropic tool", "input_schema"), ("Custom tool", "run"), ("kit.tool result", "Always a string")]),
  PL("Dispatcher", "Write call_tool(tools, name, args): tools is a dict name -> [required_args list, kind] where kind is 'echo' (return the value of args['text']), 'add' (return the string of args['a'] + args['b']) or 'fail' (always fails). Return a string. Unknown name: 'Error: unknown tool NAME'. Missing required arg: 'Error: missing ARG'. A 'fail' tool: 'Error: failed'.",
     "call_tool(tools, name, args)", """
def call_tool(tools, name, args):
    if name not in tools:
        return 'Error: unknown tool ' + name
    req, kind = tools[name][0], tools[name][1]
    for r in req:
        if r not in args:
            return 'Error: missing ' + r
    if kind == 'echo':
        return str(args['text'])
    if kind == 'add':
        return str(args['a'] + args['b'])
    return 'Error: failed'
""", [[{"say": [["text"], "echo"], "sum": [["a", "b"], "add"], "boom": [[], "fail"]}, "say", {"text": "hi"}], [{"say": [["text"], "echo"], "sum": [["a", "b"], "add"], "boom": [[], "fail"]}, "sum", {"a": 2, "b": 3}], [{"say": [["text"], "echo"]}, "sum", {}], [{"sum": [["a", "b"], "add"]}, "sum", {"a": 1}], [{"boom": [[], "fail"]}, "boom", {}]], "Look the tool up, check args, run.", approx=None),
  PL("Anthropic to OpenAI", "Write to_openai(tool): tool is [name, description, input_schema_properties_names]. Return the OpenAI-shaped function as a list [type, name, description, required_list_of_names] where type is 'function' and required is the property names sorted.",
     "to_openai(tool)", """
def to_openai(tool):
    return ['function', tool[0], tool[1], sorted(tool[2])]
""", [[["read", "Read a file", ["path", "offset"]]], [["now", "the time", []]], [["edit", "Replace text", ["path", "oldText", "newText"]]]], "Rearrange the fields.", approx=None)]))

B.append(CH(
 "The agent loop",
 ("Agent", [
  "kit.agent | is | A small coding agent", "Loop | alternates | Model and tools", "maxSteps | limits | The loop", "onEvent | streams | text, tool_call, tool_result",
  "Six tools | are | read write edit bash search fetch", "Provider | is | cloud or local", "abort | stops | The run"]),
 ["kit.agent() builds a small coding agent in the style of the pi agent. It pairs a model running on Ollama with a loop and a fixed set of tools: read, write, edit, bash, search and fetch. Ask it to write a file, run it and report, and it does so.",
  "The loop is simple. Send the conversation to the model. If the reply asks for tools, run them and add the results to the conversation, then ask again. When the reply is plain text, the turn is over. maxSteps stops runaway loops.",
  "The lab simulates the loop with a scripted model."],
 [("Agent", "A model plus a loop plus tools."), ("Turn", "One prompt and everything the agent does to answer it."), ("Step", "One model call in the loop."),
  ("Event", "A message sent to onEvent while the agent works."), ("Provider", "Where the model runs: cloud or local."), ("Messages", "The conversation so far, agent.messages.")],
 ["Pass ollamaKey to createKit for Ollama Cloud; omit it for Ollama on your machine.", "Defaults: gpt-oss:120b on cloud, qwen3:8b locally; maxSteps defaults to 40.", "Methods: prompt(text), abort(), reset(), and the messages list.",
  "Events: text, thinking, tool_call, tool_result, turn_end, done, error (and route, context, compaction with a brain).", "search and fetch always use Ollama Cloud, so they need a cloud key.", "Give extra tools with tools: [...DEFAULT_TOOLS, 'tasks', 'schedule']."],
 [T("The agent is a loop in which a model asks for things and the kit does them. That is all. The surprise is how much a small loop can accomplish when the tools are good, since reading, writing, editing and running a shell cover most of what a programmer does."),
  C("const kit = await createKit({ ollamaKey: 'YOUR_KEY' });\nconst agent = await kit.agent({\n  onEvent: e => { if (e.type === 'text') console.log(e.delta); },\n});\nconst answer = await agent.prompt('List the files in the workspace.');", "js"),
  T("Each pass through the loop is a step. The model may stream thinking and text, and it may emit a tool call. The kit runs the tool, produces a tool result, appends it, and calls the model again. When the model answers without asking for a tool, the turn ends and prompt resolves with the answer."),
  T("Options let you tune this. The system option sets the instructions. The think option asks supporting models to reason at low, medium or high effort. The tools option picks which tools the model may use. maxSteps, 40 by default, stops a confused agent from looping forever."),
  T("Where the model runs is a choice. With a cloud key the default is Ollama Cloud. Without one, the agent uses Ollama on the machine at the default address. The two clients are available as kit.ollama and kit.local, and both offer chat, models, embed, webSearch and webFetch."),
  T("Because everything happens in the shared virtual file system, an agent task like write fizzbuzz.py, run it and show me the output is just three tool calls: write, bash, then a final reply. Nothing leaves the browser except the model calls.")],
 [("When does an agent turn end?", ["When the model replies without asking for a tool", "After one tool call", "After 40 minutes", "When the file is saved"], 0, "That reply is the answer."),
  ("What does maxSteps protect against?", ["Endless loops", "Slow networks", "Large files", "Wrong passwords"], 0, "Default 40."),
  ("Which tools need an Ollama Cloud key even with a local agent?", ["search and fetch", "read and write", "bash", "edit"], 0, "They call Ollama Cloud's web endpoints.")],
 [("What does agent.abort do?", "Stops the current run."), ("What does reset do?", "Clears history."), ("What is the tool_result event?", "A tool's output."), ("What is the default provider with a key?", "Cloud.")],
 [ORDER("One turn", "Put one agent turn in order.", ["The user prompt is added to the messages", "The model is called", "The model asks to run a tool", "The kit runs it and adds the result", "The model is called again and replies with text", "The turn ends"]),
  PL("Simulated loop", "Write run_agent(script, max_steps): script is a list of model replies. Each reply is ['tool', result_text] (asks for a tool, whose result is result_text) or ['text', answer]. Each reply consumes one step. Run until a 'text' reply, then return ['done', answer, steps_used]. If max_steps replies pass without text, return ['stopped', '', max_steps]. If the script runs out first, return ['error', '', steps_used].",
     "run_agent(script, max_steps)", """
def run_agent(script, max_steps):
    steps = 0
    for r in script:
        if steps >= max_steps:
            break
        steps += 1
        if r[0] == 'text':
            return ['done', r[1], steps]
    if steps >= max_steps:
        return ['stopped', '', max_steps]
    return ['error', '', steps]
""", [[[["tool", "ok"], ["text", "hi"]], 5], [[["tool", "a"], ["tool", "b"], ["tool", "c"]], 2], [[["tool", "a"]], 5], [[["text", "now"]], 1]], "Count a step per reply.", approx=None),
  PL("Collect events", "Write events(script): same script format. Return the list of event names the agent would emit: for 'tool' replies emit 'tool_call' then 'tool_result'; for the 'text' reply emit 'text' then 'turn_end' then 'done' and stop.",
     "events(script)", """
def events(script):
    out = []
    for r in script:
        if r[0] == 'tool':
            out.append('tool_call')
            out.append('tool_result')
        else:
            out.append('text')
            out.append('turn_end')
            out.append('done')
            break
    return out
""", [[[["tool", "x"], ["text", "y"]]], [[["text", "y"]]], [[["tool", "a"], ["tool", "b"], ["text", "c"]]]], "Emit per reply.", approx=None)]))

B.append(CH(
 "The agent brain",
 ("Brain", [
  "Brain | adds | Optional agent parts", "Memory | stores | Durable facts", "Skills | are | SKILL.md folders", "Guard | compacts | Long chats",
  "Router | limits | Which tools are sent", "Delegate | spawns | A sub-agent", "Think | searches | Tree of thoughts"]),
 ["The brain is a set of optional parts you switch on with kit.agent({ brain }). Each part downloads on first use, adds its own tool and hooks into the loop. Their files live as plain text under /.kit/ in the file system, so people can read and edit them.",
  "Memory remembers facts and finds the right ones for each prompt. Skills are instructions the agent loads when needed. The guard keeps long chats inside the model's context window. The router sends only the tools a message seems to need. Other parts add a knowledge graph with proofs, tree-of-thoughts thinking, sub-agents and chat history.",
  "The labs build a compactor, a secret filter and a tool router."],
 [("Context window", "How much text the model can read at once."), ("Compaction", "Replacing older turns with a summary."), ("Skill", "A folder with a SKILL.md of instructions."),
  ("Plugin", "Code that hooks into the agent loop."), ("Journal", "A short note written after each prompt."), ("Router", "Chooses tools or models for each prompt.")],
 ["brain: ['memory', 'skills', 'history', 'guard'] picks parts; brain: true turns on memory, skills, history and guard; 'all' loads everything.", "memory keeps /.kit/memory/Memory.md, retrieves by BM25 (or embeddings) and filters out anything that looks like a password or key.",
  "skills reads /.kit/SOUL.md, /AGENTS.md and /.kit/SYSTEM.md, and skills in /.kit/skills/<name>/SKILL.md.", "guard estimates request size and compacts older turns near the limit.", "router sends core tools and exposes the rest through more_tools.",
  "delegate spawns a read-only sub-agent unless write: true; knowledge proves or contradicts claims; think runs a verified search."],
 [T("A bare agent has a short memory and a big appetite for context. The brain adds the things a long-lived assistant needs, and you choose which. This matches the kit's lean spirit: a part you do not enable costs nothing."),
  C("const kit = await createKit({ persist: 'my-app', ollamaKey, memory: { journal: true } });\nconst agent = await kit.agent({ brain: ['memory', 'skills', 'history', 'guard'] });\nawait agent.prompt('Remember that I take my coffee black');\nconst later = await kit.agent({ brain: true, resume: agent.id });", "js"),
  T("Memory stores facts as plain text under sections. For each new prompt it retrieves the best-matching lines, so the model sees only what is relevant. It refuses to save anything that looks like a password or key. With the journal option the model writes a short entry after each prompt, and durable facts it names are remembered."),
  T("Skills give the agent know-how without bloating every prompt. A skill is a folder with a SKILL.md. When there are more than fifteen, only the closest matches are listed. Persona and standing instructions come from SOUL.md and AGENTS.md. The agent course you are reading is itself built on the idea that instructions can be files."),
  T("The guard watches the size of each request. When the chat nears the context window, it compacts older turns into a summary and keeps the latest turns whole. It even learns a model's true limit from prompt is too long errors and retries."),
  T("The router saves tokens. Offering forty tools to a model costs context, so it sends the core tools plus those a message seems to need and lets the model ask for more with more_tools. The knowledge part holds facts and rules and returns proven, contradicted or unknown with a proof, so claims can be checked rather than trusted."),
  T("Delegate hands a sub-task to a fresh sub-agent that is read-only by default, limited in steps and time, and returns one report. Think explores several approaches and verifies each by running code, a shell command, a file check or a rubric; a failed hard check removes that branch.")],
 [("What does the guard do near the context limit?", ["Compacts older turns into a summary", "Deletes the chat", "Switches the model", "Stops the agent"], 0, "It keeps recent turns."),
  ("What does memory refuse to store?", ["Anything that looks like a password or key", "Names", "Numbers", "Dates"], 0, "A safety filter."),
  ("Where do skills live?", ["/.kit/skills/<name>/SKILL.md", "In the model", "On a server", "In cookies"], 0, "As plain files.")],
 [("What does more_tools do?", "Reveals tools the router hid."), ("What is delegate for?", "A sub-task in a fresh context."), ("What does resume do?", "Continues a saved chat by id."), ("What is knowledge's verdict set?", "Proven, contradicted, unknown.")],
 [MATCH("Brain parts", "Match each part with its job.", [("memory", "Remember and recall facts"), ("guard", "Keep chats inside the context window"), ("router", "Send only needed tools"), ("delegate", "Run a sub-agent"), ("skills", "Load instructions from SKILL.md")]),
  PL("Looks like a secret", "Write looks_secret(text): return true if text contains a word (split on spaces) that starts with 'sk-' or 'key_' or 'pass:' (case-insensitive), or contains the lowercase text 'password' followed by anything.",
     "looks_secret(text)", """
def looks_secret(text):
    low = text.lower()
    if 'password' in low:
        return True
    for w in low.split(' '):
        if w.startswith('sk-') or w.startswith('key_') or w.startswith('pass:'):
            return True
    return False
""", [["I take my coffee black"], ["my password is hunter2"], ["use sk-abc123 for the api"], ["the key_prod value"], ["passing the salt"]], "Check the word starts and a substring.", approx=None),
  PL("Compact a chat", "Write compact(messages, limit, keep): messages is a list of strings; size is the total length of all. If the size is at most limit return the list unchanged. Otherwise replace all but the last keep messages with ONE summary message 'summary of N messages' (N = number replaced) placed first, and return the new list.",
     "compact(messages, limit, keep)", """
def compact(messages, limit, keep):
    total = 0
    for m in messages:
        total += len(m)
    if total <= limit:
        return messages
    n = len(messages) - keep
    if n <= 0:
        return messages
    return ['summary of ' + str(n) + ' messages'] + messages[n:]
""", [[["aaaa", "bbbb", "cccc"], 100, 1], [["aaaa", "bbbb", "cccc", "dddd"], 8, 2], [["aaaa", "bbbb"], 3, 5], [["x" * 10, "y" * 10, "z" * 10], 15, 1]], "Summarise the older ones.", approx=None),
  PL("Tool router", "Write route(message, core, hints): core is a list of always-sent tool names; hints is a list of [keyword, tool] pairs. Return the sorted list of tool names to send: the core tools plus every tool whose keyword appears in the lower-cased message.",
     "route(message, core, hints)", """
def route(message, core, hints):
    m = message.lower()
    chosen = set(core)
    for kw, tool in hints:
        if kw in m:
            chosen.add(tool)
    return sorted(chosen)
""", [["Please search the web for cats", ["read", "bash"], [["search", "search"], ["schedule", "schedule"]]], ["hello", ["read"], [["search", "search"]]], ["schedule it and search", ["read"], [["search", "search"], ["schedule", "schedule"]]]], "Core plus keyword matches.", approx=None)]))

B.append(CH(
 "Decisions: fast calibrated choices",
 ("Decisions", [
  "kit.decide | asks | A decision model", "choice | picks | One option", "score | rates | On a scale", "yesno | answers | True or false",
  "Probabilities | show | Confidence", "kit.decisions | sets | Server and model", "Servers | are | ollaya, ollama, cloud"]),
 ["Not every question needs a long conversation. kit.decide sends a state, such as a log line or a message, and a question to a small decision model that answers with calibrated probabilities. It is meant for quick, cheap jobs like triage, routing and checks.",
  "There are three kinds. choice picks one of your options. score rates the state on a scale you define. yesno answers a question with a boolean. The result always includes how confident the model is.",
  "The labs reshape probabilities into the kit's result form."],
 [("Decision model", "A small model trained to give probabilities for a choice."), ("Calibrated", "Probabilities that match how often the answer is right."), ("Option", "One possible answer."),
  ("Confidence", "The probability of the chosen answer."), ("Triage", "Sorting items by type or urgency."), ("Server", "Where the decision model runs.")],
 ["type: 'choice' (default) needs options; the result has result, choice, confidence and probabilities.", "type: 'score' rates against your options such as low, medium, high.", "type: 'yesno' returns a boolean answer.",
  "kit.decisions picks the server: 'ollaya' (default), 'ollama' (0.35 or later) or 'cloud'.", "The kit translates between server formats so answers look the same.", "Give an agent the decide tool by adding it to tools."],
 [T("A language model that writes paragraphs is overkill for the question is this log line an error or a warning. A decision model is smaller and answers with numbers: 91 percent bug, 6 percent network, 3 percent user input. The numbers let you act, for example by asking a person when the confidence is low."),
  C("await kit.decide({ state: 'TypeError at list.js:42', question: 'What kind of problem?', options: ['bug', 'network', 'user input'] });\nawait kit.decide({ state: log, question: 'How urgent?', type: 'score', options: ['low', 'medium', 'high'] });\nawait kit.decide({ state: msg, question: 'Is this spam?', type: 'yesno' });\n\n// choice result\n// { type: 'choice', result: 'bug', choice: 'bug', confidence: 0.91,\n//   probabilities: { bug: 0.91, ... }, model, server }", "js"),
  T("Servers differ in how they take options and report answers. Ollaya takes options as a list and returns a boolean for yes or no. Ollama takes options as an object and derives yes or no from the probability of true. The kit hides these differences so your code sees one shape."),
  T("Configure the backend with createKit decide settings or kit.decisions: the server, the model such as winnow:e4b, and optionally host and apiKey. Ollama Cloud needs a cloud key, and its clef model needs a paid plan or credits."),
  T("Because the answer includes probabilities, you can build rules like: if confidence is below 70 percent, ask the agent or the user. This pattern, a cheap fast check first and a larger model only when unsure, is a good way to make an agent both quick and careful.")],
 [("Which decision type returns a boolean?", ["yesno", "choice", "score", "none"], 0, "answer holds the boolean."),
  ("What does confidence mean in a choice result?", ["The probability of the chosen option", "The model size", "The number of options", "The time taken"], 0, "Calibrated."),
  ("Why use a decision model?", ["Fast, cheap triage and checks", "To write essays", "To store files", "To draw charts"], 0, "That is its purpose.")],
 [("Default server?", "ollaya."), ("What does score return besides a number?", "A legend."), ("Which option gives choices?", "options."), ("How does an agent get decide?", "Add it to tools.")],
 [FILL("Types", "Use type {{yesno}} for a boolean, type {{score}} for a rating and the default {{choice}} to pick one option."),
  PL("Choice result", "Write choice_result(options, weights): weights are non-negative numbers, one per option. Normalise them into probabilities and return [chosen_option, confidence, probabilities] where the choice is the option with the highest probability (first on ties), confidence its probability and probabilities a list in option order; round to 4 decimals.",
     "choice_result(options, weights)", """
def choice_result(options, weights):
    t = sum(weights)
    p = [w / t for w in weights]
    best = 0
    for i in range(len(p)):
        if p[i] > p[best]:
            best = i
    return [options[best], round(p[best], 4), [round(x, 4) for x in p]]
""", [[["bug", "network", "user input"], [91, 6, 3]], [["a", "b"], [1, 1]], [["low", "medium", "high"], [0, 2, 8]]], "Divide by the total.", approx=1e-4),
  PL("Ask a human when unsure", "Write act(probs, options, threshold): probs is a list of probabilities for options. If the highest probability is at least threshold return the option name; otherwise return 'ask'.",
     "act(probs, options, threshold)", """
def act(probs, options, threshold):
    best = 0
    for i in range(len(probs)):
        if probs[i] > probs[best]:
            best = i
    if probs[best] >= threshold:
        return options[best]
    return 'ask'
""", [[[0.91, 0.06, 0.03], ["bug", "network", "user"], 0.7], [[0.4, 0.35, 0.25], ["a", "b", "c"], 0.7], [[0.7, 0.3], ["x", "y"], 0.7]], "Compare the best against the threshold.", approx=None)]))

B.append(CH(
 "Scheduling and tasks",
 ("Schedule", [
  "kit.schedule | runs | Jobs on a timetable", "when | accepts | English or cron", "Job kinds | are | command, prompt, js, python, run", "kit.cron | parses | Schedules",
  "Persistence | writes | /.kit/schedule.json", "kit.tasks | keeps | A task list", "Page open | is required | For jobs to run"]),
 ["kit.schedule runs jobs at times you describe in plain English, like every monday at 6pm, or in five-field cron form. A job can run a shell command, a JavaScript or Python snippet, an agent prompt, or a function. kit.tasks keeps a simple task list that people and agents share.",
  "Jobs run only while a page with the kit is open. A job missed while the page was closed runs once when it reopens. Jobs are saved to /.kit/schedule.json, except function jobs, which you re-add on each load.",
  "The labs write a cron matcher and a small task list."],
 [("Cron", "A five-field schedule: minute, hour, day of month, month, day of week."), ("Job", "A saved action with a when."), ("Missed run", "A scheduled time that passed while the page was closed."),
  ("Task", "A to-do with status and optional notes and due date."), ("runNow", "Run a job immediately."), ("Interval", "A repeat step such as */5.")],
 ["kit.schedule.add({ name, when, command | prompt | js | python | run }).", "when understands 'every day at 2am', 'in 20 minutes', '@hourly' or 5-field cron, in local time.", "list(), runNow(name), disable(name), remove(name); on emits run, error, change.",
  "scheduler: false in createKit keeps it stopped until kit.schedule.start().", "kit.cron has fromText, parse, next, upcoming and describe.", "kit.tasks: add, start, done, update, list, text, on, clear."],
 [T("A scheduler is an alarm clock that runs code. You describe when in the way you would say it aloud, and the kit turns it into cron, the classic five-field format that Unix has used for decades."),
  C("kit.schedule.add({ name: 'backup', when: 'every day at 2am', command: 'tar -czf /backup.tgz /notes' });\nkit.schedule.add({ when: 'in 20 minutes', js: `require('fs').writeFileSync('/ping.txt', 'pong')` });\nkit.schedule.add({ when: '@hourly', python: 'print(\"hi\")' });", "js"),
  T("In cron the five fields are minute, hour, day of month, month and day of week. A star means every value, a number means that value, a comma lists several, a dash gives a range, and a slash gives a step, so star slash five in the minute field means every five minutes."),
  T("Everything happens in a web page, so there is no background server. If the user closes the page, nothing runs. When they open it again, a job that was missed runs once to catch up. This is the right trade for a browser tool but means you should not rely on exact timing for critical work."),
  C("const [a] = kit.tasks.add(['Plan the API', 'Write tests']);\nkit.tasks.start(a.id); kit.tasks.done(a.id);\nkit.tasks.update(2, { notes: 'edge cases' });\nkit.tasks.list({ status: 'pending' }); kit.tasks.text();\nkit.tasks.on(items => render(items)); kit.tasks.clear();", "js"),
  T("Tasks give the agent and the user a shared checklist. The agent can add, start and finish tasks through the tasks tool, and your page can show the same list with kit.tasks.on. Give an agent both with tools set to the defaults plus tasks and schedule.")],
 [("What do the five cron fields mean, in order?", ["minute, hour, day of month, month, day of week", "second, minute, hour, day, year", "hour, minute, day, week, year", "day, month, year, hour, minute"], 0, "That is standard cron."),
  ("What happens to a job missed while the page was closed?", ["It runs once when the page reopens", "It is lost", "It runs many times", "It runs on a server"], 0, "Catch-up run."),
  ("Which jobs are not saved?", ["Function jobs", "Command jobs", "Python jobs", "Prompt jobs"], 0, "Re-add them on each load.")],
 [("What does disable do?", "Pauses a job."), ("What does tasks.text return?", "A plain-text checklist."), ("What does @hourly mean?", "Every hour."), ("What does scheduler: false do?", "Keeps the scheduler stopped.")],
 [MATCH("Cron forms", "Match each cron field text with its meaning.", [("*/5", "Every five"), ("1-5", "A range"), ("1,15", "A list"), ("*", "Every value")]),
  PL("Does this field match", "Write field_matches(field, value): field is one cron field made of comma-separated parts; each part is '*', a number, a range 'a-b', or a step '*/n'. Return true if value matches any part.",
     "field_matches(field, value)", """
def field_matches(field, value):
    for part in field.split(','):
        if part == '*':
            return True
        if part.startswith('*/'):
            if value % int(part[2:]) == 0:
                return True
        elif '-' in part:
            a, b = part.split('-')
            if int(a) <= value <= int(b):
                return True
        elif int(part) == value:
            return True
    return False
""", [["*", 7], ["*/5", 10], ["*/5", 11], ["1-5", 3], ["1-5", 6], ["1,15", 15], ["0,30", 29]], "Check each comma-separated part.", approx=None),
  PL("Task list", "Write run_tasks(cmds): cmds is a list of [command, argument]. Commands: 'add' (argument is a title; new tasks get id 1, 2, 3... and status 'pending'), 'start' (argument is an id; status 'active'), 'done' (status 'done'), 'clear' (removes done tasks). Return the final list of [id, title, status].",
     "run_tasks(cmds)", """
def run_tasks(cmds):
    tasks = []
    nid = 1
    for c, a in cmds:
        if c == 'add':
            tasks.append([nid, a, 'pending'])
            nid += 1
        elif c == 'start' or c == 'done':
            for t in tasks:
                if t[0] == a:
                    t[2] = 'active' if c == 'start' else 'done'
        elif c == 'clear':
            tasks = [t for t in tasks if t[2] != 'done']
    return tasks
""", [[[["add", "Plan"], ["add", "Test"], ["start", 1], ["done", 1]]], [[["add", "a"], ["done", 1], ["clear", 0]]], [[["add", "x"], ["add", "y"], ["done", 2], ["clear", 0], ["add", "z"]]]], "Keep ids increasing.", approx=None)]))

B.append(CH(
 "Sentry, notes and senses",
 ("Sentry", [
  "Sentry | watches | The page and device", "Rule | has | A condition and an action", "Sensitive systems | need | allow", "Notes | are | An Obsidian-style vault",
  "Wiki links | connect | Notes", "Backlinks | show | Who links here", "Senses | include | Camera and microphone"]),
 ["Sentry is a rule engine that watches the page and the device and acts when a condition occurs. It can watch things like battery, network, idle time, keys, motion, light, location, sound level, camera changes, and your own states and events. Sensitive sources must be allowed by the app.",
  "The kit also includes a notes vault in the style of Obsidian, stored on the file system, with wiki links, backlinks, tags, search, renames that update links, daily notes and templates.",
  "Senses let an agent reach the world: HTTP with secrets, MCP servers, camera, microphone, location, other sensors, and a look tool that lets the agent see an image."],
 [("Sentry rule", "A watch on a source with a condition and an action."), ("Wiki link", "A [[Note name]] reference to another note."), ("Backlink", "A note that links to this one."),
  ("Tag", "A #word that groups notes."), ("MCP", "Model Context Protocol: a standard way to connect tools."), ("Sensitive system", "A source that needs the app's permission, like location.")],
 ["Sentry watches battery, network, idle, keys, motion, light, location, sound level, camera change and custom events.", "createKit({ sentry: { allow: ['location'] } }) lets the app permit sensitive systems.", "Agents manage rules through the sentry tool.",
  "Notes support [[wiki links]], backlinks, #tags, search, daily notes and templates.", "Renaming a note updates every link to it.", "look lets the agent see an image; backups can be gzip, optionally encrypted."],
 [T("Most of the kit waits for you to ask it something. Sentry turns that around: it watches and speaks up. A rule might say when the battery drops below twenty percent, save everything and tell the user."),
  T("Sources include the battery, the network state, whether the user is idle, key presses, motion, light level, location, sound level and a change in what the camera sees. You can also define your own states and events so your app can feed rules with its own information."),
  C("const kit = await createKit({\n  sentry: { allow: ['location'] },   // the app permits a sensitive system\n});", "js"),
  T("Some sources are sensitive. The app must permit them through the allow option, so an agent can create a rule about location only when the page owner has said yes. This keeps the power to watch under the human's control."),
  T("The notes feature is a personal wiki stored in the file system. A note links to another with double square brackets. The kit can show backlinks, the notes that point to a note, search by text or tag, rename a note and fix every link to it, and make daily notes from a template."),
  T("Senses connect the workspace to the outside. HTTP calls can use secrets without exposing them. MCP servers add more tools. Camera, microphone, location and other sensors give the agent input, and the look tool lets it see an image. Backups compress the workspace and can encrypt it.")],
 [("How does an app allow a sensitive Sentry source?", ["Through the allow option", "It is always allowed", "By editing the VFS", "It cannot"], 0, "The app decides."),
  ("What is a backlink?", ["A note that links to this note", "A broken link", "A web link", "A tag"], 0, "Who links here."),
  ("What does look do?", ["Lets the agent see an image", "Lists files", "Opens a note", "Starts Python"], 0, "Vision input.")],
 [("What are wiki links?", "[[Note]] references."), ("What do daily notes use?", "Templates."), ("What happens on rename?", "Links update."), ("Can a rule use custom events?", "Yes.")],
 [ORDER("A sentry rule", "Put the life of a rule in order.", ["The app allows the system if it is sensitive", "A rule is created with a condition and an action", "Sentry watches the source", "The condition becomes true", "The action runs"]),
  PL("Backlinks", "Write backlinks(notes, target): notes is a list of [name, text]; text may contain wiki links like [[Other]]. Return the sorted names of notes whose text links to target (no duplicates, a note does not count as linking to itself).",
     "backlinks(notes, target)", """
def backlinks(notes, target):
    out = set()
    for name, text in notes:
        if name == target:
            continue
        if '[[' + target + ']]' in text:
            out.add(name)
    return sorted(out)
""", [[[["A", "see [[B]] and [[C]]"], ["B", "back to [[A]]"], ["C", "[[B]]"]], "B"], [[["A", "x"], ["B", "y"]], "A"], [[["B", "[[B]] self"], ["A", "[[B]]"]], "B"]], "Look for the double-bracket text.", approx=None),
  PL("Rename a note", "Write rename_links(notes, old, new): notes is a list of [name, text]. Return the notes with the note named old renamed to new and every [[old]] in all texts replaced by [[new]].",
     "rename_links(notes, old, new)", """
def rename_links(notes, old, new):
    out = []
    for name, text in notes:
        if name == old:
            name = new
        out.append([name, text.replace('[[' + old + ']]', '[[' + new + ']]')])
    return out
""", [[[["A", "see [[B]]"], ["B", "text"]], "B", "Bee"], [[["A", "x"]], "Z", "Y"], [[["A", "[[A]] and [[B]]"]], "A", "Alpha"]], "Rename the note and the links.", approx=None),
  PL("Battery rule", "Write sentry(rules, events): rules is a list of [source, op, limit, action] where op is '<' or '>'; events is a list of [source, value]. For each event in order, for each rule in order whose source matches and condition holds, append its action to the output. Return the list of actions.",
     "sentry(rules, events)", """
def sentry(rules, events):
    out = []
    for src, val in events:
        for r in rules:
            if r[0] == src:
                if (r[1] == '<' and val < r[2]) or (r[1] == '>' and val > r[2]):
                    out.append(r[3])
    return out
""", [[[["battery", "<", 20, "save"], ["sound", ">", 80, "alert"]], [["battery", 50], ["battery", 15], ["sound", 90]]], [[["light", "<", 10, "lamp"]], [["light", 5], ["light", 10]]], [[], [["battery", 1]]]], "Check each rule per event.", approx=None)]))

B.append(CH(
 "Automation and staying safe",
 ("Automation", [
  "Flows | are | n8n-style workflows", "Playbooks | run | Without a model", "Approval | gates | Playbooks", "Autonomy | runs | A work queue",
  "Heartbeat | checks | A checklist", "Secrets | stay | Out of the file system", "Agents | cannot | Approve their own playbooks"]),
 ["The kit can automate. Flows are n8n-style workflows of steps with triggers. Playbooks are Ansible-style task lists that run without a model. Autonomy keeps a work queue within budgets, a heartbeat checks a list every few minutes, and curiosity makes the agent explore on its own.",
  "Automation needs guard rails. A playbook runs unattended only after your app approves it, and any change needs approval again. Agents can save playbooks but cannot approve them. Secrets such as API keys are passed in by the app, kept out of the file system, and referred to by name only.",
  "This final chapter ties the kit together and ends with a design checklist."],
 [("Flow", "A saved workflow of steps with a trigger."), ("Playbook", "An approved task list that runs without a model."), ("Approval gate", "A human or app decision required before running."),
  ("Budget", "A limit on steps per hour or per day."), ("Heartbeat", "A periodic check of /.kit/HEARTBEAT.md."), ("Secret", "A value kept out of files and logs.")],
 ["Flows: step types include tool, js, shell, decide, llm, agent, file, set, if, switch, each, wait, notify, playbook, flow and stop; triggers are manual, schedule or file change.", "Playbooks support when, loop, register, retries, block/rescue/always, assert, tags and secrets redacted from logs.",
  "playbooks.approve(name) or an approve callback in createKit; changes require re-approval.", "Autonomy: queue with priorities that age, deadlines, budgets, quiet hours; it pauses while the user is active.",
  "Heartbeat: a reply of HEARTBEAT_OK stays silent; anything else raises an alert.", "createKit({ secrets: { NAME: value } }); agents see names and use {{ NAME }}."],
 [T("Once an assistant can act, people want it to act on its own: summarise my inbox every evening, check my list every half hour. The kit supports this, and its design shows how to do it carefully."),
  C("const flows = await kit.use('flows');\nflows.save({ name: 'Digest', trigger: { type: 'schedule', when: 'every day at 18:00' }, steps: [\n  { type: 'file', action: 'read', path: '/inbox.md' },\n  { type: 'llm', prompt: 'Summarise in 3 bullets:\\n{{ $json }}' },\n  { type: 'notify', title: 'Digest', body: '{{ $json }}' }] });\nawait flows.run('Digest');", "js"),
  T("A flow is a list of steps. Each step does one thing, like read a file, ask a model, or notify the user, and the output of one step is available to the next through double-brace expressions that run in a sandboxed worker. Triggers can be manual, on a schedule, or when a file changes."),
  T("A playbook is stricter. It is a list of tasks run without any model in the loop, with conditions, loops, retries and cleanup blocks. Because it runs unattended, it must be approved by your app before its first run, and any edit requires approval again. An agent may write a playbook, but cannot approve it. That separation is the central safety idea."),
  T("Autonomy lets the agent work through a queue by itself, but within budgets of steps per hour and per day, outside quiet hours, and pausing while the user is active. Tools on a deny list wait for an explicit allow. The heartbeat is the gentlest form: every N minutes the agent reads a checklist and replies HEARTBEAT_OK if nothing needs attention, which stays silent."),
  T("Secrets are handled by name. The app hands API keys to the kit, which keeps them out of the file system and redacts them from logs. The agent sees only names and writes {{ NAME }} where the value is needed, so a prompt injection cannot make it print a key it never saw."),
  T("A design checklist to finish. Start lean and load only what you use. Persist the kit if work must survive. Give the agent only the tools it needs. Make the human the approver for anything unattended. Keep secrets out of files. Allow sensitive senses deliberately. Prefer many small, checked steps to one large leap.")],
 [("Who approves a playbook?", ["The host app, not the agent", "The agent", "The model", "Nobody"], 0, "Agents cannot approve their own."),
  ("How does an agent refer to a secret?", ["By name, like {{ NAME }}", "By its value", "By file path", "It cannot"], 0, "It never sees the value."),
  ("What does a HEARTBEAT_OK reply do?", ["Stays silent", "Sends an alert", "Stops the kit", "Clears the list"], 0, "Nothing needs attention.")],
 [("What triggers a flow?", "Manual, schedule or file change."), ("What does autonomy respect?", "Budgets and quiet hours."), ("What is curiosity?", "Random exploring wake-ups."), ("What does Jade Lisp do?", "DSLs that can call every tool.")],
 [MATCH("Safety", "Match each safeguard with what it protects.", [("Approval gate", "Unattended playbooks"), ("allow option", "Sensitive senses"), ("Secrets by name", "API keys"), ("Budgets", "Runaway automation")]),
  PL("Playbook gate", "Write may_run(playbooks, approved, name): playbooks is a list of [name, version] pairs for saved playbooks; approved is a list of [name, version] pairs the host approved. Return 'run' if the exact [name, version] of the saved playbook is approved; 'needs approval' if saved but not approved (including a changed version); 'unknown' if no playbook has that name. The name argument is the playbook to run.",
     "may_run(playbooks, approved, name)", """
def may_run(playbooks, approved, name):
    for n, v in playbooks:
        if n == name:
            for an, av in approved:
                if an == n and av == v:
                    return 'run'
            return 'needs approval'
    return 'unknown'
""", [[[["backup", 1]], [["backup", 1]], "backup"], [[["backup", 2]], [["backup", 1]], "backup"], [[["backup", 1]], [], "backup"], [[], [], "x"]], "A change in version loses approval.", approx=None),
  PL("Fill in a flow", "Write fill(text, values): replace every occurrence of '{{ NAME }}' (with the spaces) in text by values[NAME] for each NAME in values; leave unknown placeholders unchanged. Return the text.",
     "fill(text, values)", """
def fill(text, values):
    for k in values:
        text = text.replace('{{ ' + k + ' }}', str(values[k]))
    return text
""", [["Hello {{ NAME }}", {"NAME": "Ada"}], ["{{ A }} and {{ B }}", {"A": "1", "B": "2"}], ["{{ X }}", {"Y": "1"}], ["no placeholders", {}]], "Replace by name.", approx=None),
  PL("Budget", "Write run_queue(tasks, per_hour, quiet, hour): tasks is a list of [name, steps]; per_hour is the step budget for this hour; quiet is true if it is a quiet hour; hour unused. Run tasks in order while the budget remains: a task runs only if its steps fit in the remaining budget. Return the list of task names that ran; if quiet, return an empty list.",
     "run_queue(tasks, per_hour, quiet, hour)", """
def run_queue(tasks, per_hour, quiet, hour):
    if quiet:
        return []
    left = per_hour
    out = []
    for name, steps in tasks:
        if steps <= left:
            out.append(name)
            left -= steps
    return out
""", [[[["a", 5], ["b", 10], ["c", 3]], 10, False, 14], [[["a", 5]], 10, True, 3], [[["a", 4], ["b", 4], ["c", 4]], 10, False, 9]], "Spend the budget task by task.", approx=None)]))
