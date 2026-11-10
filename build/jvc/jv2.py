"""Jade Vault course, chapters 8-14."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

B = []

B.append(CH(
 "Flows: automations in steps",
 ("Flows", [
  "Flow | is | A list of steps", "Step output | is | $json for the next", "Expression | sits in | Double braces", "Trigger | starts | A flow",
  "Retry | repeats | A failing step", "Run log | records | Every step", "Decide | picks | By probability"]),
 ["A flow is an n8n style automation kept as JSON in /Jade/Flows. It is a list of steps that run in order, and each step's output becomes $json for the next step.",
  "Step types include Tool, JavaScript, Shell, Decide, Ask AI, Jade agent, Note, Set fields, If, Switch, For each, Wait, Notify, Run flow and Stop. Text fields may hold double-brace expressions.",
  "A flow starts by hand, on a schedule, or when a note changes, and each run is logged step by step."],
 [("Flow", "A saved list of steps, run in order."), ("$json", "The output of the previous step, available to the next."), ("Trigger", "What starts a flow: by hand, a schedule or a note change."),
  ("Decide step", "A step that picks one option and returns probabilities."), ("Retry", "Running a failing step again, up to three times."), ("Expression", "JavaScript inside {{ }} in a text field, run in a sandbox without network.")],
 ["Flows are JSON files /Jade/Flows/NAME.flow.json.", "Each step's output is $json for the next; other names are $input, $node[\"Step\"], $vars, $item, $index, $now and $today.", "Steps can retry 0 to 3 times or continue on error.",
  "Triggers: by hand, a schedule (every weekday at 9am, cron, @daily), or a note or folder change.", "Flows also run from the shell (flow run), scripts (jade.flow), the API and Jade's flow tool.", "Every run is logged with each step's input, output and time."],
 [T("A flow is a small program built from boxes. The first box reads a note, the next decides something, the next writes a result. You can build one in the Flows tab, or ask Jade to build it, and it is saved as a JSON file in the vault."),
  C("{\"name\": \"Inbox triage\", \"trigger\": {\"type\": \"note\", \"path\": \"/Inbox.md\"}, \"steps\": [\n  {\"type\": \"note\", \"name\": \"Inbox\", \"action\": \"read\", \"path\": \"/Inbox.md\"},\n  {\"type\": \"each\", \"items\": \"$json.split('\\n').filter(l => l.startsWith('- '))\", \"steps\": [\n    {\"type\": \"decide\", \"name\": \"Urgent?\", \"state\": \"{{ $item }}\", \"question\": \"Is this urgent?\", \"kind\": \"yesno\"},\n    {\"type\": \"if\", \"condition\": \"$json.result === true\", \"then\": [\n      {\"type\": \"note\", \"action\": \"append\", \"path\": \"/Urgent.md\", \"content\": \"- [ ] {{ $item }}\"}]}]},\n  {\"type\": \"notify\", \"title\": \"Inbox triaged\"}]}", "json"),
  T("Data moves through the steps like water through pipes. The output of one step is called $json in the next. You reach it inside any text field with double braces, such as {{ $json.name }}. Other names are available: the input of the flow, the output of a named step, variables, the loop item and its index, and today's date."),
  T("Steps do many things. A Tool step calls any of Jade's tools. A JavaScript step runs code in a sandbox. A Shell step runs a command. A Decide step asks a small decision model and returns the winner with a confidence and probabilities. An Ask AI step gets one answer. A Jade agent step runs a full chat turn. There are also If, Switch, For each, Wait, Notify, Run flow and Stop."),
  T("Flows can fail, so each step can retry up to three times or continue on error. Every run is logged with the input, output, log and time of each step, so you can see exactly where it went wrong. A flow that fails sends a notification when it ran from a schedule."),
  T("Flows start in several ways: by hand, on a schedule, or when a note or folder changes. They can also be called from the shell with flow run, from scripts with jade.flow, over the HTTP API, and by Jade herself with the flow tool. Because command and flow schedules need no model, a flow is the right tool for anything that should simply happen the same way each time.")],
 [("What is $json?", ["The previous step's output", "The flow's name", "A secret", "The model"], 0, "It chains the steps."),
  ("How many retries can a step have?", ["0 to 3", "Unlimited", "Exactly 10", "None"], 0, "Or continue on error."),
  ("Where are flows stored?", ["/Jade/Flows/NAME.flow.json", "/Templates", "/Apps", "In the model"], 0, "Plain JSON.")],
 [("What does a Decide step return?", "A result, confidence, probabilities."), ("What starts a flow?", "Hand, schedule or note change."), ("Do expressions get the network?", "No."), ("What does For each do?", "Repeats steps per item.")],
 [MATCH("Step types", "Match each step with what it does.", [("Tool", "Call one of Jade's tools"), ("Shell", "Run a BusyBox command"), ("Decide", "Pick an option with probabilities"), ("Notify me", "Send a notification")]),
  PL("Fill a template", "Write render(tpl, data): replace each {{ $json }} with str(data) when data is not a dict, and each {{ $json.a.b }} with the value at that path in the dict data (use str of the value). A missing path gives an empty string. Other text is unchanged.",
     "render(tpl, data)", """
def render(tpl, data):
    out = ''
    i = 0
    while i < len(tpl):
        if tpl[i:i + 2] == '{{':
            j = tpl.find('}}', i)
            if j > 0:
                expr = tpl[i + 2:j].strip()
                val = ''
                if expr == '$json':
                    val = '' if isinstance(data, dict) else str(data)
                elif expr.startswith('$json.'):
                    cur = data
                    ok = True
                    for key in expr[6:].split('.'):
                        if isinstance(cur, dict) and key in cur:
                            cur = cur[key]
                        else:
                            ok = False
                            break
                    val = str(cur) if ok else ''
                out += val
                i = j + 2
                continue
        out += tpl[i]
        i += 1
    return out
""", [["Hello {{ $json.name }}!", {"name": "Ada"}], ["{{ $json }} items", 5], ["{{ $json.user.city }}", {"user": {"city": "Lisbon"}}], ["{{ $json.missing }}.", {"a": 1}], ["plain", {}]], "Walk the path key by key.", approx=None),
  PL("Retry a step", "Write run_step(results, retries, continue_on_error): results is a list of booleans, the outcome of each attempt in order (true is success). A step is tried up to retries + 1 times and stops at the first success. Return [status, attempts] where status is 'ok' on success, otherwise 'continued' if continue_on_error is true or 'failed'.",
     "run_step(results, retries, continue_on_error)", """
def run_step(results, retries, continue_on_error):
    attempts = 0
    for ok in results[:retries + 1]:
        attempts += 1
        if ok:
            return ['ok', attempts]
    if continue_on_error:
        return ['continued', attempts]
    return ['failed', attempts]
""", [[[False, False, True], 2, False], [[False, False, True], 1, False], [[False, False, True], 1, True], [[True], 3, False], [[], 0, False]], "Stop at the first success.", approx=None),
  PL("Run a flow", "Write run_flow(steps, data): data is a dict and each step changes it in turn. A step ['set', key, value] sets a key. A step ['if', key, value, 'stop'] ends the flow when data[key] equals value. A step ['stop'] ends the flow. Return [stopped, pairs] where stopped tells whether the flow ended early and pairs is the final data as a sorted list of [key, value] pairs.",
     "run_flow(steps, data)", """
def run_flow(steps, data):
    d = {}
    for k in data:
        d[k] = data[k]
    for st in steps:
        if st[0] == 'set':
            d[st[1]] = st[2]
        elif st[0] == 'if':
            if d.get(st[1]) == st[2]:
                return [True, [[k, d[k]] for k in sorted(d)]]
        elif st[0] == 'stop':
            return [True, [[k, d[k]] for k in sorted(d)]]
    return [False, [[k, d[k]] for k in sorted(d)]]
""", [[[["set", "a", 1], ["set", "b", 2]], {}], [[["set", "x", "ok"], ["if", "x", "ok", "stop"], ["set", "y", 9]], {}], [[["stop"], ["set", "z", 1]], {"q": 0}], [[], {"k": 5}]], "Copy the data, then apply each step.", approx=None)]))

B.append(CH(
 "Playbooks: deterministic automation",
 ("Playbooks", [
  "Playbook | is | JSON tasks", "Task | has | do and keywords", "when | skips | A task", "loop | repeats | A task",
  "register | stores | A result", "rescue | handles | Failure", "Approval | binds | A hash of content"]),
 ["A playbook is Jade's version of Ansible: a saved JSON list of tasks that call any tool, the browser or built-in actions, in the same order each time, with no model in the loop.",
  "Tasks have a do action and keywords such as when, loop, register, retries, until, failed_when, ignore_errors, block, rescue and always. Strings may hold double-brace expressions in a small safe language.",
  "You approve a playbook when it is saved, and again whenever its content changes, so a schedule or flow can run it unattended."],
 [("Playbook", "A saved JSON list of tasks run without a model."), ("Task", "One action with arguments and keywords."), ("register", "A keyword that stores a task's result in a variable."),
  ("rescue", "Tasks that run when a block fails."), ("Approval hash", "A fingerprint of the playbook; a change makes it unapproved."), ("Expression language", "A safe mini language for when, until and templates.")],
 ["Chat is for exploring and deciding; a playbook is for repeating.", "Playbooks live in /Jade/Playbooks/NAME.json and are edited in the Playbooks tab.", "The expression language has no JavaScript: only variables, literals, operators and listed functions.",
  "An undefined name is an error, not an empty string.", "At most 1000 tasks and 300 seconds per run (maximum 900).", "Only an approved, unchanged playbook runs from a flow or a schedule."],
 [T("When Jade explores, she reasons. When something must happen the same way every time, reasoning is a risk. A playbook removes the model from the loop. It is a list of tasks, each a tool call with fixed arguments, so the same input gives the same steps."),
  C("{\"description\":\"Price of the lamp\",\"allow_hosts\":[\"shop.example\"],\"vars\":{\"max\":50},\"tasks\":[\n {\"name\":\"Open the shop\",\"do\":\"browser.goto\",\"url\":\"https://shop.example/lamp\"},\n {\"do\":\"browser.extract\",\"css\":\".price\",\"register\":\"price\"},\n {\"do\":\"assert\",\"that\":[\"price | float <= max\"],\"msg\":\"too expensive: {{ price }}\"},\n {\"do\":\"save\",\"path\":\"/Jade/Playbooks/out/lamp.txt\",\"value\":\"{{ today() }} {{ price }}\",\"append\":true}]}", "json"),
  T("If you know Ansible, the keywords will look familiar. The keyword when skips a task if its expression is false. Loop repeats over a list. Register stores a result in a variable. Retries and until repeat a failing task. Failed_when turns a success into a failure. Ignore_errors keeps going. A block groups tasks, rescue runs on failure and always runs either way."),
  T("The expression language is a small safe interpreter. It has numbers, strings, lists, comparison and logic operators, in, is defined, and a list of filters such as float, which strips currency symbols so that the text $12.50 becomes 12.5. It never runs JavaScript. A name that is not defined is an error rather than silently empty, which catches typos before they cause damage."),
  T("Approval is what makes unattended runs safe. When you save a playbook from the tab, you approve it, and the approval is tied to a hash of its content. If anyone changes the file, the hash changes and the playbook is no longer approved until you approve it again. A flow or schedule will refuse to run a playbook that is new or changed."),
  T("More limits protect you. The allow_hosts list limits where the browser may go and which URLs any task may fetch. Run variables are limited to the ones the playbook declares. Saves go only under /Jade/Playbooks/out. A failure stops the run at that task unless you wrote ignore_errors or a rescue, and nothing is repaired or guessed.")],
 [("What does when do?", ["Skips the task if false", "Repeats the task", "Stores a result", "Approves it"], 0, "A condition."),
  ("What happens when you edit an approved playbook?", ["It needs approving again", "It still runs", "It is deleted", "Jade approves it"], 0, "The hash changes."),
  ("What is an undefined name in an expression?", ["An error", "An empty string", "Zero", "True"], 0, "Typos are caught.")],
 [("What does register do?", "Stores a task result."), ("What is rescue for?", "Handling failure."), ("What does allow_hosts limit?", "Where requests may go."), ("Is a model in the loop?", "No.")],
 [MATCH("Keywords", "Match each keyword with its job.", [("when", "Skip if the expression is false"), ("loop", "Repeat over a list"), ("register", "Store the result in a variable"), ("rescue", "Run on failure")]),
  PL("Evaluate an expression", "Write eval_expr(expr, vars): clauses joined by ' or ' (weaker) and ' and '. A clause is 'left OP right' with spaces around OP in == != < <= > >=, or 'x is defined' / 'x is not defined'. An operand is a number, a quoted string, true, false, or a variable name, optionally followed by ' | float' or ' | int' (float strips every character except digits, . and -). Return true or false, or 'error' if a variable used is not defined.",
     "eval_expr(expr, vars)", """
def eval_expr(expr, vars):
    class Undef(Exception):
        pass

    def val(tok):
        tok = tok.strip()
        conv = None
        if ' | ' in tok:
            tok, conv = tok.split(' | ', 1)
            tok = tok.strip()
            conv = conv.strip()
        if tok[:1] == '"' or tok[:1] == "'":
            v = tok[1:-1]
        elif tok == 'true':
            v = True
        elif tok == 'false':
            v = False
        else:
            try:
                v = float(tok) if '.' in tok else int(tok)
            except ValueError:
                if tok not in vars:
                    raise Undef()
                v = vars[tok]
        if conv in ('float', 'int'):
            if isinstance(v, str):
                keep = ''
                for ch in v:
                    if ch.isdigit() or ch in '.-':
                        keep += ch
                v = float(keep)
            else:
                v = float(v)
            if conv == 'int':
                v = int(v)
        return v

    def clause(c):
        c = c.strip()
        if c.endswith(' is not defined'):
            return c[:-15].strip() not in vars
        if c.endswith(' is defined'):
            return c[:-11].strip() in vars
        for op in ['==', '!=', '<=', '>=', '<', '>']:
            parts = c.split(' ' + op + ' ', 1)
            if len(parts) == 2:
                a = val(parts[0])
                b = val(parts[1])
                if op == '==':
                    return a == b
                if op == '!=':
                    return a != b
                if op == '<':
                    return a < b
                if op == '>':
                    return a > b
                if op == '<=':
                    return a <= b
                return a >= b
        return bool(val(c))

    try:
        for alt in expr.split(' or '):
            ok = True
            for c in alt.split(' and '):
                if not clause(c):
                    ok = False
                    break
            if ok:
                return True
        return False
    except Undef:
        return 'error'
""", [["price | float <= max", {"price": "$12.50", "max": 50}], ["price | float > max", {"price": "$99.00", "max": 50}], ["x == 3 and y == 4", {"x": 3, "y": 4}], ["x == 3 or y == 9", {"x": 1, "y": 9}], ["z == 1", {"x": 1}], ["z is defined", {"x": 1}], ["z is not defined", {"x": 1}], ["name == 'ana'", {"name": "ana"}]], "Split on or, then and, then the operator.", approx=None),
  PL("Run tasks", "Write run_tasks(tasks, vars): each task is a dict with 'do' ('set', 'fail' or 'assert'), and optional 'when' (a variable name that must be truthy), 'ignore_errors' and, for set, 'name' and 'value', for assert 'name' (a variable that must be truthy). Run them in order. A task whose 'when' variable is missing or falsy is skipped. 'set' stores value in vars. 'fail' fails; 'assert' fails when its variable is falsy. A failure is ignored when ignore_errors is true, otherwise it stops the run. Return [ok, ok_count, skipped, failed, ignored] where ok is false if the run stopped.",
     "run_tasks(tasks, vars)", """
def run_tasks(tasks, vars):
    v = {}
    for k in vars:
        v[k] = vars[k]
    ok_n = 0
    skipped = 0
    failed = 0
    ignored = 0
    for t in tasks:
        w = t.get('when')
        if w is not None and not v.get(w):
            skipped += 1
            continue
        do = t['do']
        bad = False
        if do == 'set':
            v[t['name']] = t['value']
        elif do == 'fail':
            bad = True
        elif do == 'assert':
            bad = not v.get(t['name'])
        if bad:
            if t.get('ignore_errors'):
                ignored += 1
            else:
                failed += 1
                return [False, ok_n, skipped, failed, ignored]
        else:
            ok_n += 1
    return [True, ok_n, skipped, failed, ignored]
""", [[[{"do": "set", "name": "a", "value": 1}, {"do": "assert", "name": "a"}], {}], [[{"do": "set", "name": "a", "value": 1}, {"do": "fail", "when": "b"}], {}], [[{"do": "fail", "ignore_errors": True}, {"do": "set", "name": "x", "value": 2}], {}], [[{"do": "set", "name": "a", "value": 1}, {"do": "fail"}, {"do": "set", "name": "b", "value": 2}], {}]], "A failure that is not ignored stops the run.", approx=None),
  PL("Approval hash", "Write fnv1a(text): the 32 bit FNV-1a hash of the characters' code points (all below 256): start with h = 2166136261; for each character, h = (h XOR code) then multiplied by 16777619, keeping only the lowest 32 bits. Return h as an integer.",
     "fnv1a(text)", """
def fnv1a(text):
    h = 2166136261
    for ch in text:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h
""", [[""], ["a"], ["playbook"], ["playbook "]], "Mask to 32 bits at every step.", approx=None)]))

B.append(CH(
 "The knowledge graph",
 ("Knowledge", [
  "Fact | is | A relation", "Rule | derives | New facts", "Constraint | forbids | Contradictions", "Reasoner | is | Datalog in Rust",
  "Verdict | is | Proven, contradicted or unknown", "Open world | means | Missing is not false", "Proposed | waits for | Your confirmation"]),
 ["The knowledge graph holds facts such as works_at(alice, acme), rules that derive new facts, and constraints that must never be broken. A Datalog reasoner, written in Rust and run as WebAssembly, checks claims against them.",
  "Every answer is one of three: proven with its proof, contradicted, or unknown. The graph is open-world: something missing is not false.",
  "Facts Jade adds are proposed until you confirm them, so you decide what counts."],
 [("Fact", "A relation between things, like works_at(alice, acme)."), ("Rule", "A statement that derives new facts: head :- conditions."), ("Constraint", "A pattern that must never match, written with a leading !."),
  ("Reasoner", "The engine that derives facts and checks claims."), ("Open world", "Assuming unknown things might be true, not false."), ("Proof", "The facts and rules a conclusion rests on.")],
 ["Facts live in /Jade/Knowledge/facts.jsonl and rules in /Jade/Knowledge/rules.dl.", "Rules use variables that start with a capital letter: above(X, Z) :- reports_to(X, Y), above(Y, Z).", "A constraint such as ! one_employer: works_at(P, A), works_at(P, B), A != B. flags any match.",
  "Verdicts are proven, contradicted (the opposite holds or a constraint would break) or unknown.", "Confirmed facts are yours; proposed ones wait for you; rejected ones can never be added again.", "A graph of 180,000 derived facts took about 0.15 s in the browser's tests."],
 [T("A knowledge graph stores knowledge as small statements. A fact says a relation holds between things, for example works_at with alice and acme. Rules let the graph work out more facts. If bob reports to alice and carol reports to bob, then a rule about above can conclude that carol is above alice."),
  C("works_at(alice, acme)\nreports_to(bob, alice)\nreports_to(carol, bob)\n\nabove(X, Y) :- reports_to(X, Y).\nabove(X, Z) :- reports_to(X, Y), above(Y, Z).\n\n! one_employer: works_at(P, A), works_at(P, B), A != B.", "text"),
  T("Constraints say what must never happen. The line starting with an exclamation mark says that a person may not work at two different places. If two facts match it, the graph reports a contradiction and shows the facts involved. Running Check over notes that Jade turned into facts is a way to find where your own notes disagree."),
  T("A question gets one of three answers. Proven means the claim follows from the facts and rules, and the proof is shown. Contradicted means its opposite holds, or accepting it would break a constraint. Unknown means nothing says either way. That last answer is important: the graph is open-world, so a missing fact is not treated as false."),
  T("The reasoner is Datalog, a small logic language that always terminates and is fast. It is written in Rust and compiled to WebAssembly, so it runs in the page. Two rules keep it sound: every variable in a rule head or comparison must appear first in an ordinary condition, and a relation cannot depend on its own absence round a loop."),
  T("The graph is under your control. Facts you add are confirmed. Facts Jade adds are proposed, and a proof that rests on a proposed fact says so. If you reject a fact, Jade cannot add it again. With Verify answers on, she checks the factual claims in her own answers against the graph and marks each with a tick, a cross or a question mark.")],
 [("What does unknown mean?", ["Nothing in the graph says either way", "The claim is false", "The claim is proven", "The graph is broken"], 0, "Open world."),
  ("What does a constraint do?", ["Flags matches as contradictions", "Adds a fact", "Deletes facts", "Runs a flow"], 0, "It names what must never happen."),
  ("Who confirms facts Jade adds?", ["You", "The model", "A flow", "Nobody"], 0, "They start as proposed.")],
 [("What is a rule head?", "The fact a rule derives."), ("What language is the reasoner?", "Datalog."), ("Where are the facts stored?", "facts.jsonl."), ("What are the three verdicts?", "Proven, contradicted, unknown.")],
 [MATCH("Verdicts", "Match each verdict with its meaning.", [("Proven", "Follows from facts and rules, with a proof"), ("Contradicted", "The opposite holds or a constraint breaks"), ("Unknown", "The graph does not say"), ("Proposed fact", "Added by Jade, waiting for you")]),
  PL("Parse a fact", "Write parse_fact(s): turn 'works_at(alice, \"Acme Corp\")' into ['works_at', 'alice', 'Acme Corp']: the relation name, then the arguments split on commas that are outside double quotes, trimmed, with the quotes removed. A number argument stays text. Return an empty list if there are no parentheses.",
     "parse_fact(s)", """
def parse_fact(s):
    s = s.strip()
    a = s.find('(')
    if a < 0 or not s.endswith(')'):
        return []
    rel = s[:a].strip()
    inner = s[a + 1:-1]
    args = []
    cur = ''
    inq = False
    for ch in inner:
        if ch == '"':
            inq = not inq
        elif ch == ',' and not inq:
            args.append(cur.strip())
            cur = ''
        else:
            cur += ch
    args.append(cur.strip())
    return [rel] + args
""", [["works_at(alice, acme)"], ["works_at(alice, \"Acme Corp\")"], ["team_size(acme, 12)"], ["nothing"], ["f(a)"]], "Track whether you are inside quotes.", approx=None),
  PL("Reports to, transitively", "Write above(pairs): pairs is a list of [x, y] meaning x reports to y. Return the sorted list of every [x, z] derived by the rules above(X,Y) :- reports_to(X,Y) and above(X,Z) :- reports_to(X,Y), above(Y,Z). Cycles must not loop forever.",
     "above(pairs)", """
def above(pairs):
    known = set()
    for x, y in pairs:
        known.add((x, y))
    changed = True
    while changed:
        changed = False
        for x, y in pairs:
            for a, b in list(known):
                if a == y and (x, b) not in known:
                    known.add((x, b))
                    changed = True
    return sorted([list(p) for p in known])
""", [[[["bob", "alice"], ["carol", "bob"]]], [[]], [[["a", "b"], ["b", "a"]]], [[["d", "c"], ["c", "b"], ["b", "a"]]]], "Repeat until nothing new is added.", approx=None),
  PL("One employer", "Write one_employer(facts): facts is a list of [relation, subject, object]. For the relation works_at, return the sorted list of subjects that work at two or more different objects (the constraint ! one_employer).",
     "one_employer(facts)", """
def one_employer(facts):
    jobs = {}
    for rel, subj, obj in facts:
        if rel == 'works_at':
            if subj not in jobs:
                jobs[subj] = set()
            jobs[subj].add(obj)
    out = []
    for s in jobs:
        if len(jobs[s]) > 1:
            out.append(s)
    return sorted(out)
""", [[[["works_at", "alice", "acme"], ["works_at", "alice", "globex"], ["works_at", "bob", "acme"]]], [[]], [[["works_at", "a", "x"], ["works_at", "a", "x"]]], [[["owns", "a", "x"], ["owns", "a", "y"]]]], "Collect the set of employers per person.", approx=None),
  PL("Verdict", "Write verdict(facts, claim, single_valued): facts and claim are [relation, subject, object]; single_valued is a list of relations that allow only one object per subject. Return 'proven' when the claim is in facts; 'contradicted' when its relation is single valued and facts hold the same relation and subject with a different object; otherwise 'unknown' (open world).",
     "verdict(facts, claim, single_valued)", """
def verdict(facts, claim, single_valued):
    for f in facts:
        if f == claim:
            return 'proven'
    if claim[0] in single_valued:
        for f in facts:
            if f[0] == claim[0] and f[1] == claim[1] and f[2] != claim[2]:
                return 'contradicted'
    return 'unknown'
""", [[[["works_at", "alice", "acme"]], ["works_at", "alice", "acme"], ["works_at"]], [[["works_at", "alice", "acme"]], ["works_at", "alice", "globex"], ["works_at"]], [[["works_at", "alice", "acme"]], ["works_at", "bob", "acme"], ["works_at"]], [[["likes", "a", "x"]], ["likes", "a", "y"], ["works_at"]]], "Check for the claim, then for a clash.", approx=None)]))

B.append(CH(
 "Autonomous mode and plans",
 ("Autonomy", [
  "Queue | holds | Three tiers", "Tier 1 | is | Interrupts", "Tier 2 | is | A priority queue", "Tier 3 | is | Round robin",
  "Limits | bound | Steps and hours", "Plans | draw | Gantt charts", "Critical path | sets | The finish date"]),
 ["In autonomous mode Jade works through a queue on her own, the way an operating system schedules programs: interrupts first, then a priority queue with aging, then round robin with feedback for long goals.",
  "You set the limits: steps per hour, a daily cap, quiet hours, a pause while you use the app, and approval for tools that reach outside the vault. Everything is logged.",
  "Plans are Gantt charts for projects with dependencies, milestones and a critical path."],
 [("Autonomous mode", "Jade works through her queue without being asked, within your limits."), ("Interrupt", "An urgent item that goes first."), ("Aging", "Raising a waiting task's priority so it is not starved."),
  ("Round robin", "Giving each long goal short turns in rotation."), ("Gantt chart", "A bar chart of tasks over time."), ("Critical path", "The chain of tasks that sets the finish date.")],
 ["Tier 1 interrupts go first in arrival order; Jade may hold at most 3 of her own.", "Tier 2 orders by priority 0 to 100, plus up to 40 for waiting, plus 10, 30 or 50 for a deadline within a day, an hour or already passed.",
  "Tier 3 gets slices of 2, 4 or 8 steps; a goal that uses its slice drops a level, one that waits 30 minutes rises one.", "Tier 3 gets every 4th turn when tier 2 also has work.", "Each slice ends with STATUS: done, continue or blocked.",
  "Defaults: 60 steps an hour, 600 a day, quiet hours 11pm to 7am."],
 [T("If you have ever waited for a slow computer, you have met a scheduler. An operating system must decide which program runs next. Jade Vault applies the same idea to an agent's to-do list. In Schedule, Queue, a switch called Autonomous lets her work through it without you."),
  T("The queue has three tiers. Tier one is interrupts: urgent items that go first, in arrival order, with at most three that Jade herself may hold. Tier two is a priority queue for one-off work. Each task has a priority from 0 to 100, and waiting raises it by up to 40, so nothing waits forever. A deadline within a day adds 10, within an hour adds 30, and one that has passed adds 50."),
  T("Tier three is round robin for long goals. A goal gets a short slice of 2, 4 or 8 model steps depending on its level. A goal that uses its whole slice drops a level, and one that waited 30 minutes rises one. When tiers two and three both have work, tier three gets at least every fourth turn, so long goals never starve. Between slices she keeps only a short note, and each slice ends with a status line: done, continue or blocked."),
  T("Limits keep this safe. She stops in quiet hours, which start at 11pm and end at 7am at first, and when the step budget for the hour or day is used. She pauses while you use the app or chat. Tools that reach outside the vault, such as phone, SSH, browsers and MCP servers, wait for your Allow button for that one task. Stop turns it all off at once, and every action is logged to /Jade/Autonomy/log.md."),
  T("Plans are for work that takes weeks. Under Schedule, Plans shows a project as a Gantt chart with a bar per task, arrows for dependencies, diamonds for milestones and a line for today. The critical path is the chain of dependent tasks that sets the finish date, drawn with a bright edge. Dragging a bar moves the tasks that depend on it."),
  T("Plans and the queue are separate, with one link. With autonomous mode on and the setting to work on her ready plan tasks, each of Jade's tasks whose dependencies are done becomes a tier three goal, and finishing it marks the plan task 100 percent.")],
 [("What does tier 1 hold?", ["Interrupts", "Long goals", "One-off tasks", "Plans"], 0, "They go first."),
  ("What does aging do?", ["Raises priority while a task waits", "Deletes old tasks", "Slows tools", "Closes the app"], 0, "Prevents starvation."),
  ("What sets the finish date of a plan?", ["The critical path", "The first task", "The longest name", "Today's date"], 0, "The longest dependent chain.")],
 [("What does STATUS: blocked mean?", "She needs your help."), ("What stops autonomous mode at once?", "Stop."), ("Where is it logged?", "/Jade/Autonomy/log.md."), ("What is a milestone?", "A diamond marker.")],
 [MATCH("Tiers", "Match each tier with what it is for.", [("Tier 1", "Urgent interrupts"), ("Tier 2", "One-off work by priority"), ("Tier 3", "Long goals in turns"), ("Plans", "Gantt charts for projects")]),
  PL("Effective priority", "Write effective_priority(base, waiting_bonus, minutes_to_deadline): base is 0 to 100. Add the waiting bonus capped at 40. Add a deadline bonus: none when minutes_to_deadline is None or more than 1440; 10 when at most 1440; 30 when at most 60; 50 when 0 or less (already passed). Return the total.",
     "effective_priority(base, waiting_bonus, minutes_to_deadline)", """
def effective_priority(base, waiting_bonus, minutes_to_deadline):
    p = base + min(40, waiting_bonus)
    m = minutes_to_deadline
    if m is None:
        return p
    if m <= 0:
        return p + 50
    if m <= 60:
        return p + 30
    if m <= 1440:
        return p + 10
    return p
""", [[50, 0, None], [50, 100, None], [50, 10, 1000], [50, 10, 30], [50, 10, -5], [20, 40, 5000]], "Check the deadline from the tightest case outward.", approx=None),
  PL("May she work now?", "Write may_work(hour, quiet_start, quiet_end, used_hour, max_hour, used_day, max_day, user_active): return the first reason that applies: 'user active' if user_active is true; 'quiet hours' if the hour is in quiet hours (quiet_start to quiet_end, wrapping past midnight when quiet_start is bigger, end exclusive); 'hour budget' if used_hour >= max_hour; 'day budget' if used_day >= max_day; otherwise 'go'.",
     "may_work(hour, quiet_start, quiet_end, used_hour, max_hour, used_day, max_day, user_active)", """
def may_work(hour, quiet_start, quiet_end, used_hour, max_hour, used_day, max_day, user_active):
    if user_active:
        return 'user active'
    if quiet_start > quiet_end:
        quiet = hour >= quiet_start or hour < quiet_end
    else:
        quiet = quiet_start <= hour < quiet_end
    if quiet:
        return 'quiet hours'
    if used_hour >= max_hour:
        return 'hour budget'
    if used_day >= max_day:
        return 'day budget'
    return 'go'
""", [[12, 23, 7, 10, 60, 100, 600, False], [23, 23, 7, 0, 60, 0, 600, False], [3, 23, 7, 0, 60, 0, 600, False], [7, 23, 7, 0, 60, 0, 600, False], [12, 23, 7, 60, 60, 100, 600, False], [12, 23, 7, 10, 60, 600, 600, False], [12, 23, 7, 0, 60, 0, 600, True]], "Handle midnight wrap-around.", approx=None),
  PL("Critical path", "Write critical_path(tasks): tasks is a list of [name, days, deps] with deps a list of names. A task finishes days after the latest finish of its dependencies. Return [total_days, path] where total_days is the latest finish over all tasks and path is the chain of task names from the first to the last along the longest route. On a tie pick the smallest name.",
     "critical_path(tasks)", """
def critical_path(tasks):
    info = {}
    for name, days, deps in tasks:
        info[name] = [days, deps]
    fin = {}

    def finish(n):
        if n in fin:
            return fin[n]
        days, deps = info[n]
        best = 0
        for d in deps:
            best = max(best, finish(d))
        fin[n] = days + best
        return fin[n]

    for n in info:
        finish(n)
    if not info:
        return [0, []]
    end = sorted(info, key=lambda n: [-fin[n], n])[0]
    path = [end]
    cur = end
    while info[cur][1]:
        deps = info[cur][1]
        cur = sorted(deps, key=lambda n: [-fin[n], n])[0]
        path.append(cur)
    path.reverse()
    return [fin[end], path]
""", [[[["design", 3, []], ["build", 5, ["design"]], ["docs", 2, ["design"]], ["ship", 1, ["build", "docs"]]]], [[["a", 4, []]]], [[["a", 2, []], ["b", 2, []], ["c", 1, ["a", "b"]]]], [[]]], "Compute each finish time by recursion.", approx=None)]))

B.append(CH(
 "Think, delegate and the model router",
 ("Think", [
  "think | builds | A tree of thoughts", "Verifier | can say | No", "Tier 1 | vetoes | Failures", "Beam | keeps | The top few",
  "delegate | runs | A sub-agent", "Report | returns | One summary", "Router | picks | A model per message"]),
 ["The think tool searches a tree of reasoning lines and checks each with something that can say no, such as running code or checking a file. The best verified line is the answer.",
  "A failed check from a real verifier is a veto, not an average, so a confident judge cannot rescue a solution that fails its test.",
  "The delegate tool runs a sub-agent with a clean context and returns one report. The model router chooses a quick or strong model for each message."],
 [("Tree of thoughts", "Branching several lines of reasoning and keeping the best checked ones."), ("Verifier", "A check, such as running code, that can reject a thought."), ("Veto", "A failure that cannot be averaged away."),
  ("Beam search", "Keeping only the top few nodes at each depth."), ("Delegate", "A sub-agent that works in its own clean context and reports back."), ("Model router", "A decision model that picks which of your models answers.")],
 ["think verifiers: code (read-only JavaScript), file, rubric and an independent judge.", "Search modes are beam (default), best_first and puct, with budgets in nodes, seconds and tokens.", "Trees are saved after each step and episodes are logged.",
  "delegate is read-only by default, with 8 steps (max 15) and 120 s (max 300), and its report is capped at 6000 characters.", "A delegate cannot nest or run twice at once.", "The router uses the decision model to send everyday chat to a quick model and hard questions to a strong one."],
 [T("Models often answer with confidence and are wrong. The think tool is a cure based on checking. Instead of one answer, Jade tries several lines of thought, and each line is checked by something that can say no: a test that runs, a file that must exist, a rubric of yes or no items, or an independent judge."),
  T("The design document ranks verifiers in tiers. Tier one is executable ground truth, such as running code and checking the result. It can veto. A solution that fails its test does not get partial credit from a judge that likes it. Lower tiers are scored, and the model grading itself is the weakest, with its weight capped."),
  M(r"s=\frac{\sum_i w_i\,c_i\,s_i}{\sum_i w_i\,c_i}\qquad A_t=\sum_{k\ge 0}(\gamma\lambda)^k\,\delta_{t+k},\;\;\delta_t=r_t+\gamma V_{t+1}-V_t"),
  T("A node's score is the weighted average of its checks, where each weight also counts how reliable that verifier has proved to be. When a line reaches a result, a credit step finds which thought mattered most, using generalised advantage estimation, an idea from reinforcement learning. Search is beam by default because a phone can only afford about ten to forty node checks, too few for statistics-heavy methods."),
  T("The delegate tool is a different kind of help. It starts a small second agent with a clean context, lets it read, search and fetch for a few steps, and returns one short report. The pages it read never fill Jade's own context. By default it is read-only. It cannot call itself, and its report is framed as data."),
  T("The model router is a third. Before each message, the decision model, which can be a local model through Ollaya or Ollama, picks which of your models should answer. Everyday chat goes to a quick one and a hard request goes to a strong one. This saves time and cost, and you configure it under Decision models.")],
 [("What is a tier 1 failure?", ["A veto", "A small penalty", "A warning", "A retry"], 0, "Not averaged away."),
  ("What does delegate return?", ["One report", "Every page it read", "A new vault", "A model"], 0, "Context stays clean."),
  ("Which search mode is the default?", ["Beam", "PUCT", "Random", "Depth first"], 0, "Cheap and predictable.")],
 [("What is a verifier?", "A check that can say no."), ("Why is beam the default?", "Small budgets."), ("What does the router choose?", "Which model answers."), ("Can a delegate nest?", "No.")],
 [MATCH("Verifier tiers", "Match each tier with its kind.", [("Tier 1", "Executable ground truth"), ("Tier 2", "A rubric of structural constraints"), ("Tier 3", "An independent judge"), ("Tier 4", "Self-critique")]),
  PL("Score a node", "Write node_score(evals): evals is a list of [tier, weight, confidence, score] with score from 0 to 1. If any tier 1 evaluation has a score below 0.5 the node is vetoed: return [0.0, True]. Otherwise cap tier 4 weights at 0.25 and return [sum(w*c*s) / sum(w*c) rounded to 4 decimals, False]; with no weight return [0.0, False].",
     "node_score(evals)", """
def node_score(evals):
    num = 0.0
    den = 0.0
    for tier, w, c, s in evals:
        if tier == 1 and s < 0.5:
            return [0.0, True]
        if tier == 4:
            w = min(w, 0.25)
        num += w * c * s
        den += w * c
    if den == 0:
        return [0.0, False]
    return [round(num / den, 4), False]
""", [[[[1, 1.0, 1.0, 1.0], [3, 1.0, 0.8, 0.6]]], [[[1, 1.0, 1.0, 0.0], [3, 1.0, 1.0, 0.9]]], [[[4, 1.0, 1.0, 1.0], [3, 0.5, 1.0, 0.5]]], [[]]], "Check for a veto first.", approx=1e-3),
  PL("Keep the beam", "Write beam_keep(nodes, width): nodes is a list of [id, score]. Return the ids of the top width nodes, highest score first, ties by id.",
     "beam_keep(nodes, width)", """
def beam_keep(nodes, width):
    ordered = sorted(nodes, key=lambda n: [-n[1], n[0]])
    return [n[0] for n in ordered[:width]]
""", [[[["a", 0.5], ["b", 0.9], ["c", 0.9], ["d", 0.1]], 2], [[["a", 1.0]], 3], [[], 2], [[["x", 0.2], ["y", 0.2]], 1]], "Sort by score then id.", approx=None),
  PL("Advantages", "Write advantages(rewards, values, gamma, lam): for steps t from 0, delta_t = r_t + gamma*V_(t+1) - V_t, where V after the last step is 0. A_t = delta_t + gamma*lam*A_(t+1), with A after the last step 0. Return the list of A_t rounded to 4 decimals.",
     "advantages(rewards, values, gamma, lam)", """
def advantages(rewards, values, gamma, lam):
    n = len(rewards)
    out = [0.0] * n
    nxt = 0.0
    for t in range(n - 1, -1, -1):
        v_next = values[t + 1] if t + 1 < n else 0.0
        delta = rewards[t] + gamma * v_next - values[t]
        nxt = delta + gamma * lam * nxt
        out[t] = round(nxt, 4)
    return out
""", [[[0, 0, 1], [0.2, 0.4, 0.8], 0.95, 0.9], [[1], [0.5], 0.95, 0.9], [[0, 1], [0.0, 0.0], 0.9, 1.0], [[], [], 0.95, 0.9]], "Work backwards from the last step.", approx=1e-3),
  PL("Delegate limits", "Write delegate_limits(steps, seconds): steps defaults to 8 and seconds to 120 when None. Clamp steps to 1..15 and seconds to 1..300. Return [steps, seconds].",
     "delegate_limits(steps, seconds)", """
def delegate_limits(steps, seconds):
    if steps is None:
        steps = 8
    if seconds is None:
        seconds = 120
    return [max(1, min(15, steps)), max(1, min(300, seconds))]
""", [[None, None], [20, 500], [0, 0], [10, 200]], "Apply defaults, then clamp.", approx=None)]))

B.append(CH(
 "Jade Lisp and scripting",
 ("Lisp", [
  "Jade Lisp | is | A small Lisp", "tool/NAME | calls | Any tool", "Macros | build | New words", "Sandbox | runs | Untrusted programs",
  "Fuel | limits | Steps", "jade.* | scripts | Tools from node", "DSL | is | A small language"]),
 ["Jade Lisp is a small Lisp in the style of Scheme and Clojure, part of the base system. It builds small languages for rules and workflows, and scripts that call Jade's tools.",
  "Programs can run in a sandbox with only the verbs you give them and a step limit called fuel, so a program written by someone else cannot read files, call tools or loop forever.",
  "Scripts in node can also use a jade object: jade.tool, jade.ask, jade.decide, jade.flow, jade.shell, jade.notify and a key value store."],
 [("Lisp", "A language where code is lists, written with parentheses."), ("Macro", "Code that writes code; defmacro with quasiquote."), ("DSL", "A domain specific language: a small language for one job."),
  ("Fuel", "A limit on evaluation steps that stops runaway programs."), ("Sandbox", "A place where a program can use only the functions you give it."), ("jade.tool", "A script call that runs any of Jade's tools.")],
 ["Data: numbers, strings, symbols, :keywords, lists, maps, nil, #t and #f.", "Forms include define, lambda, let, if, cond, while and defmacro; tail calls run in constant space.", "(tool/NAME :arg value) runs any tool; jade/ask, jade/flow, jade/shell and jade/notify are also available.",
  "pure=yes runs a whole program without tools, files or JavaScript; fuel=N limits steps.", "Three ways to build a DSL: macros, a sandbox, or parsing the text as data.", "In node: await jade.tool(name, args), jade.ask(prompt), jade.decide({...}), jade.flow(name, input), jade.kv."],
 [T("A Lisp program is a tree written with parentheses. The first item in a list is the function and the rest are its arguments, so adding two numbers is written plus, one, two inside parentheses. It looks odd at first, but it has a great advantage: code and data have the same shape, so programs can easily write and inspect other programs."),
  C("(define square (lambda (x) (* x x)))\n(square 5)                ; => 25\n\n(define fact\n  (lambda (n) (if (< n 2) 1 (* n (fact (- n 1))))))\n(fact 5)                  ; => 120\n\n;; calling Jade's tools from Lisp\n(tool/notes_search :query \"Lisbon\")\n(jade/notify \"Done\" \"The report is ready\")", "lisp"),
  T("Jade Lisp has the usual forms: define, lambda, let, if, cond and loops with named let, plus macros written with defmacro and quasiquote. It adds maps with keywords, try and catch for errors, and tail calls that run in constant space, so a loop does not grow the stack."),
  T("Every tool is callable from Lisp as tool slash name, with keyword arguments. That makes it a good scripting language for chains of tools, and for small languages. There are three ways to build a DSL. With macros, the new language is Lisp with new words. In a sandbox, you give the language its verbs as plain functions and run a program written by someone else where only those verbs exist. Or you can parse the text as data and walk the forms yourself."),
  T("The sandbox is the safe choice for untrusted programs, such as one from a note or another model. The program cannot read files, call tools or loop forever, because you also give it a step limit called fuel. The option pure=yes runs a whole program with no tools, files or JavaScript at all."),
  T("Outside Lisp, the node scripts in the shell, in a flow's JavaScript step and in Jade's own bash, have a jade object. A call such as jade.tool with a name and arguments runs a tool, jade.ask gets one model answer without a whole chat, jade.decide asks the decision model, jade.flow runs a flow, and jade.kv keeps small values between runs. Files that a script writes are visible to the tools it calls, and the other way round.")],
 [("What does fuel limit?", ["Evaluation steps", "Memory", "Network use", "Output size"], 0, "It stops runaway programs."),
  ("How do you call a tool from Lisp?", ["(tool/NAME :arg value)", "tool.NAME(arg)", "run NAME", "@NAME"], 0, "Keyword arguments."),
  ("What does pure=yes do?", ["Runs without tools, files or JavaScript", "Cleans the vault", "Speeds up the model", "Deletes macros"], 0, "A safe mode.")],
 [("What is a DSL?", "A small language for one job."), ("What is a macro?", "Code that writes code."), ("What is jade.kv?", "Small stored values."), ("Where is the interpreter?", "/Jade/tools/lisp.js.")],
 [FILL("Lisp", "Calling a tool from Lisp is written (tool/{{NAME}} :arg value), and a step limit is called {{fuel}}."),
  PL("Tokenize", "Write tokens(src): split a Lisp program into tokens: the characters ( and ) are tokens of their own, and everything else is split on whitespace.",
     "tokens(src)", """
def tokens(src):
    return src.replace('(', ' ( ').replace(')', ' ) ').split()
""", [["(+ 1 2)"], ["(define x (* 2 3))"], [""], ["a b"]], "Pad the parentheses with spaces.", approx=None),
  PL("A tiny Lisp", "Write lisp_eval(src, fuel): evaluate a program of one or more forms and return the value of the last. Support integers and decimals, #t, #f and nil (None), the builtins + - * < > = (with - on one argument negating), if (only #f and nil are false), define, lambda and let with bindings like ((a 1) (b 2)). Every evaluation step uses 1 fuel; return 'out of fuel' when fuel runs out, and 'error' for any other error (such as an unknown name).",
     "lisp_eval(src, fuel)", """
def lisp_eval(src, fuel):
    toks = src.replace('(', ' ( ').replace(')', ' ) ').split()
    pos = [0]

    def parse():
        t = toks[pos[0]]
        pos[0] += 1
        if t == '(':
            out = []
            while toks[pos[0]] != ')':
                out.append(parse())
            pos[0] += 1
            return out
        if t == '#t':
            return True
        if t == '#f':
            return False
        if t == 'nil':
            return None
        try:
            return int(t)
        except ValueError:
            pass
        try:
            return float(t)
        except ValueError:
            pass
        return t

    budget = [fuel]

    def lookup(env, name):
        while env is not None:
            if name in env[0]:
                return env[0][name]
            env = env[1]
        raise KeyError(name)

    def ev(x, env):
        budget[0] -= 1
        if budget[0] < 0:
            raise RuntimeError('fuel')
        if x is True or x is False or x is None:
            return x
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, str):
            return lookup(env, x)
        op = x[0]
        if op == 'if':
            c = ev(x[1], env)
            if c is not False and c is not None:
                return ev(x[2], env)
            if len(x) > 3:
                return ev(x[3], env)
            return None
        if op == 'define':
            env[0][x[1]] = ev(x[2], env)
            return env[0][x[1]]
        if op == 'lambda':
            return ['closure', x[1], x[2], env]
        if op == 'let':
            scope = [{}, env]
            for b in x[1]:
                scope[0][b[0]] = ev(b[1], env)
            return ev(x[2], scope)
        fn = ev(op, env)
        args = [ev(a, env) for a in x[1:]]
        if isinstance(fn, list):
            scope = [{}, fn[3]]
            for i in range(len(fn[1])):
                scope[0][fn[1][i]] = args[i]
            return ev(fn[2], scope)
        return fn(*args)

    def add(*a):
        t = 0
        for v in a:
            t += v
        return t

    def sub(*a):
        if len(a) == 1:
            return -a[0]
        t = a[0]
        for v in a[1:]:
            t -= v
        return t

    def mul(*a):
        t = 1
        for v in a:
            t *= v
        return t

    glob = [{'+': add, '-': sub, '*': mul, '<': lambda a, b: a < b, '>': lambda a, b: a > b, '=': lambda a, b: a == b}, None]
    try:
        forms = []
        while pos[0] < len(toks):
            forms.append(parse())
        result = None
        for f in forms:
            result = ev(f, glob)
        return result
    except RuntimeError as e:
        if str(e) == 'fuel':
            return 'out of fuel'
        return 'error'
    except Exception:
        return 'error'
""", [["(+ 1 2)", 1000], ["(define sq (lambda (x) (* x x))) (sq 5)", 1000], ["(define fact (lambda (n) (if (< n 2) 1 (* n (fact (- n 1)))))) (fact 5)", 2000], ["(define loop (lambda () (loop))) (loop)", 60], ["(if #f 1 2)", 100], ["(if 0 1 2)", 100], ["(let ((a 2) (b 3)) (* a b))", 100], ["(nothing 1)", 100], ["(- 5)", 100]], "Pass an environment through each evaluation.", approx=None)]))

B.append(CH(
 "Connect, back up, secure and build",
 ("Connect", [
  "HTTP API | answers | JSON over GET", "Token | guards | Every call", "Backup | goes to | Your server", "Encryption | uses | AES-GCM and PBKDF2",
  "Build | applies | Exact-match patches", "Tests | run in | Playwright", "APK | needs | No Android SDK"]),
 ["Jade Vault connects outward in several ways: an HTTP API on the phone, MCP servers, the Vector and Discord messengers, webxdc mini apps, and a fleet broker that shares one vault between devices.",
  "A scheduled backup uploads a compressed, optionally encrypted file to your own server. Jade can start one but she cannot restore.",
  "The app is built by applying ordered exact-match patches to a base page; if a patch does not match, the build fails loudly."],
 [("HTTP API", "An optional phone-side server that answers GET requests with JSON; off by default."), ("Bearer token", "A secret sent in the Authorization header to prove access."), ("Webxdc", "Sandboxed offline mini apps in a zip with index.html."),
  ("Vector, Discord", "Messengers where Jade can be a bot, through small bridge servers."), ("Fleet", "One shared vault on a small server used by phones and browsers."), ("Exact-match patch", "A replacement whose old text must occur exactly once, or the build stops.")],
 ["The API is off by default; every call except /v1/health needs the token.", "/v1/chat?message=TEXT sends a message that also appears in the app; errors are JSON with HTTP 400, 401, 404, 409, 502 or 504.",
  "A backup is JSON, gzip, then optionally AES-GCM with a PBKDF2 key of 210,000 rounds; the server checks a SHA-256 header.", "Backup names use only letters, digits, dot, dash and underscore and end in .json or .json.gz.",
  "Webxdc apps are sandboxed with no vault access and no network.", "npm run build makes dist/jade-vault.html; npm test runs dozens of Playwright suites; the APK needs a JDK, not the Android SDK."],
 [T("A personal agent is more useful when it can be reached. Jade Vault has several doors, and each is a switch that is off until you turn it on. The HTTP API lives in the Android app. When enabled, it listens on your chosen port and answers GET requests with JSON. A message sent to the chat endpoint goes through the normal chat and appears in the app."),
  C("curl -H \"Authorization: Bearer $TOKEN\" \\\n  \"http://PHONE:8787/v1/chat?message=What%20notes%20mention%20Lisbon%3F\"\n\n# errors are JSON too: {\"ok\":false,\"error\":{\"code\":\"busy\",\"message\":\"...\"}}\n# 400 bad request  401 token  404 unknown chat  409 busy  502 model error  504 still working", "bash"),
  T("Other doors include MCP servers, configured in a file, that plug in more tools. The Vector and Discord bridges let Jade act as a bot, with roles: the owner gets the full Jade, admins get extra powers, and everyone else gets friendly chat. Webxdc apps, such as the built-in Jade Link messenger, are small sandboxed apps that can exchange updates with her but cannot see your vault or the network."),
  T("Backups protect your data. A scheduled backup uploads to a server you run. The file is JSON, compressed with gzip, and optionally encrypted with AES-GCM using a key derived with PBKDF2 at 210,000 rounds. The server checks a checksum header, stores the file atomically with strict permissions, and keeps the newest few of each kind. Jade has a backup tool with status, now and list, but she cannot restore. If you lose the passphrase there is no recovery."),
  T("The build is unusual. There is no bundler. A base page is patched by many replacements, and each one's old text must occur exactly once. Zero matches stops the build with MISSING and more than one stops it with AMBIGUOUS, so it never produces a half-patched page. Feature modules are then injected in a fixed order, and the result is one HTML file."),
  T("Testing uses Playwright with headless Chromium plus engine tests, and every feature gets a test. The Android app is built without the Android SDK, using stubs, a dex step, a packaging tool and signing. The repository also states honestly what has not run on a real phone. That habit of saying what was and was not tested is a good one to copy. You now have the map: use the vault, let Jade work within limits, and extend it with skills, flows and playbooks.")],
 [("What does every API call except /v1/health need?", ["The token", "A password", "Wi-Fi only", "Nothing"], 0, "Bearer token."),
  ("What does HTTP 409 mean here?", ["Jade is busy", "Bad token", "Unknown chat", "Model error"], 0, "One message at a time."),
  ("What does a patch that matches twice cause?", ["The build fails with AMBIGUOUS", "It applies twice", "It is skipped", "A warning"], 0, "Exactly once is required.")],
 [("Can Jade restore a backup?", "No."), ("What encrypts backups?", "AES-GCM with PBKDF2."), ("Is the API on by default?", "No."), ("What do webxdc apps lack?", "Vault and network access.")],
 [MATCH("Doors", "Match each connection with what it is.", [("HTTP API", "GET requests answered with JSON"), ("MCP server", "Extra tools plugged in"), ("Vector bridge", "Jade as a messenger bot"), ("Webxdc app", "A sandboxed offline mini app")]),
  PL("Exact-match patch", "Write rep(text, old, new): replace old with new in text when old occurs exactly once. Return the new text; return 'MISSING' if old does not occur and 'AMBIGUOUS' if it occurs more than once (counting non-overlapping occurrences).",
     "rep(text, old, new)", """
def rep(text, old, new):
    n = text.count(old)
    if n == 0:
        return 'MISSING'
    if n > 1:
        return 'AMBIGUOUS'
    return text.replace(old, new)
""", [["a b c", "b", "X"], ["a b c", "z", "X"], ["a b b", "b", "X"], ["abc", "abc", ""]], "Count the occurrences first.", approx=None),
  PL("Backup file names", "Write valid_backup_name(name): true when the name is not empty, uses only letters, digits, dot, dash and underscore, and ends with .json or .json.gz.",
     "valid_backup_name(name)", """
def valid_backup_name(name):
    if not name:
        return False
    for ch in name:
        if not (ch.isalpha() or ch.isdigit() or ch in '.-_'):
            return False
    return name.endswith('.json') or name.endswith('.json.gz')
""", [["jade-vault-full-20261109.json.gz"], ["jade-vault-config-1.enc.json"], ["../etc/passwd"], ["backup.zip"], ["a b.json"], [""]], "Check every character, then the ending.", approx=None),
  PL("Error status", "Write api_status(kind): map the error kind to the HTTP status: 'bad_request' 400, 'token' 401, 'unknown_chat' 404, 'busy' 409, 'model_error' 502, 'timeout' 504. Any other kind is 500.",
     "api_status(kind)", """
def api_status(kind):
    table = {'bad_request': 400, 'token': 401, 'unknown_chat': 404, 'busy': 409, 'model_error': 502, 'timeout': 504}
    return table.get(kind, 500)
""", [["bad_request"], ["token"], ["unknown_chat"], ["busy"], ["model_error"], ["timeout"], ["other"]], "A small lookup table.", approx=None),
  PL("Keep the newest", "Write keep_newest(names, keep): names look like 'jade-vault-KIND-TIMESTAMP.json.gz' where KIND has no dashes and timestamps sort in time order. For each kind keep the newest keep files. Return the sorted list of names to delete.",
     "keep_newest(names, keep)", """
def keep_newest(names, keep):
    groups = {}
    for n in names:
        kind = n.split('-')[2] if n.count('-') >= 3 else ''
        if kind not in groups:
            groups[kind] = []
        groups[kind].append(n)
    out = []
    for kind in groups:
        files = sorted(groups[kind])
        cut = len(files) - keep
        if cut > 0:
            out.extend(files[:cut])
    return sorted(out)
""", [[["jade-vault-full-1.json.gz", "jade-vault-full-2.json.gz", "jade-vault-full-3.json.gz", "jade-vault-config-1.json.gz"], 2], [["jade-vault-full-1.json.gz"], 1], [[], 3], [["jade-vault-full-1.json.gz", "jade-vault-config-1.json.gz", "jade-vault-config-2.json.gz"], 1]], "Group by kind, sort, drop the oldest.", approx=None)]))
