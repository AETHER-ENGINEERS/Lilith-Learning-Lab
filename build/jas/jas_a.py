# -*- coding: utf-8 -*-
"""Jade Agent Stack course, part 1: roles, config and secrets, the harness, errors and versions."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "The stack: five parts and one contract",
 ("Jade stack", [
  "Vault | is | Control plane",
  "Base | is | Resource plane",
  "Kit | embeds | Vault in a page",
  "UI/UX | presents | Web components",
  "Stack | is | A client of all four",
  "Contract | says | Base can say no",
  "Refusal | means | Stop"]),
 ["Jade Agent Stack is one Python package that drives four other Jade repositories: Vault, Agent Base, Agent Kit and Agent UI/UX. It is a client, not a fork, and it speaks to them only through documented interfaces.",
  "The division of labour is summed up in one line: Vault asks, Base answers, Base logs, Base can say no. Vault owns the agent loop and the person's transcript; Base owns identity, the database, the model gateway, billing and the authoritative audit log.",
  "The rules between them are short: tool calls over MCP or REST, one short-lived credential per task, an idempotency key on every mutation, and a refusal means stop and tell the person."],
 [("Control plane", "The part that decides and schedules: here Jade Vault, with the agent loop, schedules, approvals and the person."),
  ("Resource plane", "The part that holds and serves resources: here Jade Agent Base, with identity, database, model gateway, billing and audit log."),
  ("Jade Agent Kit", "The embeddable subset of Vault, an agent in any web page."),
  ("Task credential", "A short-lived, least-privilege credential minted for one task."),
  ("Audit log", "Base's authoritative record of every tool call and refusal, which agents cannot change.")],
 ["Vault asks. Base answers. Base logs. Base can say no.",
  "Seam: MCP at /api/agent/mcp, same tools over REST.",
  "Vault owns the transcript; Base owns the audit.",
  "One credential per task, at most 24 h.",
  "403 credential_refused: stop, do not retry."],
 [T("Imagine a company with a manager and a records office. The manager decides what to do and talks to people; the records office keeps the files, checks who is allowed to see what, and writes down every request it handles, including the ones it turns down. Jade splits an AI agent system the same way. Jade Vault is the manager, the control plane. Jade Agent Base is the records office, the resource plane."),
  T("Four repositories, and one toolkit over them. Vault runs the agent loop, schedules, the heartbeat, autonomy levels, budgets and approvals, and shows the person the transcript. Base provides identity, the database, the model gateway, billing and the audit log. Kit is the embeddable subset of Vault, so a web page can host an agent. UI/UX supplies web components and themes. The Stack package is a client over all of them: an SDK, a command line, a setup wizard, a safety harness, portable playbooks and a site compiler. It copies none of their logic."),
  T("The seam between Vault and Base is the Model Context Protocol. Base serves tools at its MCP endpoint, and the same tools are available over plain REST. Every tool call carries an authority, a short-lived credential that Vault mints for one task. Base validates the arguments, checks scopes, runs the call, logs it and answers. If it says no, with a missing scope, a refused credential or a reused idempotency key, the client stops and tells the person; it does not look for a way around."),
  C("# the shape of one call, in pseudocode\ncred = vault.mint(task='job-42', scopes=['read', 'write'], ttl='15m')\nresult = base.call('records_list', {'collection': 'posts'}, credential=cred)\n# Base: validate -> check scope -> run -> write agent_audit -> answer\n# on 403 credential_refused: stop, tell the person, never retry", "python"),
  T("Because Base keeps the authoritative audit log, even a compromised or confused agent leaves a trail that it cannot edit. Because credentials are short and narrow, a stolen one is worth little. Because Vault owns the transcript, Base never stores conversations on its behalf. Throughout this course, watch for how each design choice limits the damage a mistaken or manipulated agent can do.")],
 [("Who owns the person's transcript?", ["Vault", "Base", "Kit", "UI/UX"], 0, "Control plane."),
  ("Who holds the authoritative audit log?", ["Base", "Vault", "The toolkit", "The browser"], 0, "agent_audit."),
  ("What is the seam between Vault and Base?", ["MCP, with the same tools over REST", "A shared file", "Email", "SQL"], 0, "/api/agent/mcp."),
  ("What should a client do after a 403 credential_refused?", ["Stop and tell the person", "Retry in a loop", "Use a bigger token", "Ignore it"], 0, "Do not retry around a refusal."),
  ("Is the Stack a fork of the four repositories?", ["No, it is a client over their interfaces", "Yes", "It replaces Vault", "It replaces Base"], 0, "Client."),
  ("How long can a task credential live at most?", ["24 hours", "One year", "Forever", "One second"], 0, "15 minutes by default.")],
 [("pip install jade-agent-stack", "install the toolkit"), ("/api/agent/mcp", "Base's MCP endpoint")],
 [MATCH("Match the part", "Pair each part with its role.", [("Vault", "agent loop and approvals"), ("Base", "identity, data, gateway, audit"), ("Kit", "agent embedded in a page"), ("UI/UX", "web components and themes"), ("Stack", "client toolkit over all four")]),
  PL("Next action after a response", "Write next_action(status, code, is_mutation): return 'ok' for status 200; 'stop' for 403 (any code, a refusal is final); 'fix' for 400; 'newkey' for 422; 'retry' for status 0 (a network error) when is_mutation is False, otherwise 'stop' (mutations never retry by themselves); 'stop' for anything else.", "next_action(status, code, is_mutation)", '''
def next_action(status, code, is_mutation):
    if status == 200:
        return 'ok'
    if status == 403:
        return 'stop'
    if status == 400:
        return 'fix'
    if status == 422:
        return 'newkey'
    if status == 0:
        return 'stop' if is_mutation else 'retry'
    return 'stop'
''', [[200, '', False], [403, 'credential_refused', False], [400, 'invalid', True], [422, 'key_reused', True], [0, '', False], [0, '', True], [500, '', False]], "Refusals are final; reads may retry."),
  PL("Who owns it", "Write owner(topic): return 'vault' for 'transcript', 'schedules', 'approvals' or 'agent loop'; 'base' for 'audit', 'identity', 'database', 'billing' or 'gateway'; 'kit' for 'embed'; 'ui' for 'theme'; otherwise 'unknown'.", "owner(topic)", '''
def owner(topic):
    if topic in ('transcript', 'schedules', 'approvals', 'agent loop'):
        return 'vault'
    if topic in ('audit', 'identity', 'database', 'billing', 'gateway'):
        return 'base'
    if topic == 'embed':
        return 'kit'
    if topic == 'theme':
        return 'ui'
    return 'unknown'
''', [['transcript'], ['audit'], ['embed'], ['theme'], ['weather']], "Match the ownership table."),
  PL("Valid TTL", "Write ttl_ok(seconds): True if a credential lifetime is at least 1 second and at most 24 hours (86400 seconds).", "ttl_ok(seconds)", '''
def ttl_ok(seconds):
    return 1 <= seconds <= 86400
''', [[900], [0], [86400], [86401], [1]], "Bounded lifetimes."),
  PL("Task identity in the audit log", "Write audit_for_task(entries, task_id): entries is a list of [task_id, tool, outcome]; return the entries for that task as [tool, outcome] pairs in order.", "audit_for_task(entries, task_id)", '''
def audit_for_task(entries, task_id):
    return [[e[1], e[2]] for e in entries if e[0] == task_id]
''', [[[['a', 'records_list', 'ok'], ['b', 'collection_delete', 'refused'], ['a', 'record_create', 'ok']], 'a'], [[], 'x'], [[['b', 't', 'ok']], 'a']], "Every call carries a task id."),
  PL("Scopes are enough", "Write allowed_by_scope(granted, required): True if every required scope is in granted.", "allowed_by_scope(granted, required)", '''
def allowed_by_scope(granted, required):
    return all([r in granted for r in required])
''', [[['read', 'write'], ['read']], [['read'], ['read', 'schema']], [[], []]], "Least privilege.")]
))

CHS.append(CH(
 "Install, configuration and secrets",
 ("Config", [
  "jade init | writes | jade.config.yaml",
  "Discovery | walks | Up the folders",
  "Unknown keys | are | Errors",
  "Secrets | live in | The keyring",
  "Environment | wins | First",
  "Token in URL | is | Refused",
  "Doctor | checks | Every target"]),
 ["Install with pip (Python 3.11 or later, needing only PyYAML). The setup wizard jade init writes jade.config.yaml, and jade doctor checks that every target is reachable, authenticated, compatible and free of tokens in URLs.",
  "The config is found by walking up from the working directory, or from the JADE_CONFIG variable. Unknown keys are errors, and the file never holds secrets.",
  "Secrets are looked up in an order: JADE_SECRET environment variables first (good for CI), then the OS keyring, then an opt-in 0600 file. Tokens travel only in the Authorization header."],
 [("jade.config.yaml", "The toolkit's configuration file: targets, models, approvals, defaults and routes, with no secrets."),
  ("OS keyring", "The operating system's secret store, used under the service name jade."),
  ("Header-only authentication", "Sending tokens in an Authorization header, never in the URL."),
  ("jade doctor", "A command that checks configuration, secrets and each target."),
  ("Resumable wizard", "A setup wizard that remembers earlier answers and can be restarted or run headless.")],
 ["pip install jade-agent-stack.",
  "jade init, then jade doctor.",
  "Config: $JADE_CONFIG, else walk up.",
  "Secrets: env, keyring, 0600 file.",
  "A URL with a token is refused."],
 [T("Getting started takes two commands. After installing the package, jade init walks through seven steps: environment, targets, auth, models, permissions, a smoke test and writing the file. It is resumable, so an interrupted setup continues where it stopped, and it can run headless with a file of answers or with defaults. Then jade doctor confirms that each target can be reached, that your token works, that versions are compatible and that no token is hiding in a URL."),
  T("The configuration file is plain YAML. Under targets you name Base and Vault by URL, plus the keyring name of the token for each. Other keys set model defaults, approvals, call timeouts and routes. The toolkit finds the file by looking in the working directory and then each parent folder in turn, unless the JADE_CONFIG variable points somewhere. Any key it does not recognise is an error, which catches typos before they silently do nothing."),
  C("# jade.config.yaml (no secrets here)\nversion: 1\ntargets:\n  base:\n    url: https://base.example.com\n    token: jade.base.example.com      # the keyring name, not the token\n    credentials: {ttl: 15m, enabled: true}\n  vault:\n    url: http://127.0.0.1:8099\napprovals:\n  base.read: [\"*\"]\ndefaults: {timeout: 30, chat_timeout: 300}", "yaml"),
  T("Secrets deserve more care than settings. The lookup order is environment variables named JADE_SECRET followed by the upper-cased secret name, then the OS keyring under the service jade, and finally a file with mode 0600 that you must opt into. The jade secret commands set, list names of and remove secrets, and never print values. Tokens go in the Authorization header; a URL containing a token, which would end up in logs and browser history, is refused by the client and by the local server, and a Vault that still accepts a token in the query string is refused as well."),
  T("Every one of these choices is about keeping secrets out of places where they leak: files committed to version control, shell histories, log lines and error messages. Output and errors are redacted of registered secrets. The habit to take away is that configuration describes where things are, and secrets are only ever fetched at the moment of use.")],
 [("What does jade doctor check?", ["Reachability, authentication, compatibility and no URL tokens", "Only spelling", "Only disk space", "Nothing"], 0, "Every target."),
  ("Where is the config found?", ["Walking up from the working directory, or $JADE_CONFIG", "Only in /etc", "Only in the cloud", "At random"], 0, "Discovery."),
  ("What happens to an unknown config key?", ["It is an error", "It is ignored", "It is deleted", "It is encrypted"], 0, "Catches typos."),
  ("Which secret source is checked first?", ["Environment variables", "The 0600 file", "The URL", "The config file"], 0, "CI friendly."),
  ("Why refuse tokens in URLs?", ["They leak into logs and history", "They are too long", "They are slow", "They are old"], 0, "Header-only."),
  ("What does the config hold for a token?", ["The keyring name, not the token", "The token", "A password", "Nothing at all"], 0, "No secrets.")],
 [("jade secret set NAME", "store a secret"), ("JADE_SECRET_<NAME>", "environment override")],
 [MATCH("Match the item", "Pair each item with its job.", [("jade init", "setup wizard"), ("jade doctor", "health check"), ("jade secret set", "store a secret safely"), ("JADE_CONFIG", "point to a config file"), ("keyring", "OS secret store")]),
  PL("Environment variable name", "Write env_name(secret): 'JADE_SECRET_' followed by the secret name upper-cased with every character that is not a letter or digit replaced by an underscore.", "env_name(secret)", '''
def env_name(secret):
    out = ''
    for ch in secret.upper():
        if ('A' <= ch <= 'Z') or ('0' <= ch <= '9'):
            out = out + ch
        else:
            out = out + '_'
    return 'JADE_SECRET_' + out
''', [['jade.base.example.com'], ['openai-key'], ['A1']], "Letters and digits stay."),
  PL("Keyring name from a URL", "Write keyring_name(url): 'jade.' followed by the host of the URL (strip the scheme; cut at the first '/' or ':').", "keyring_name(url)", '''
def keyring_name(url):
    rest = url
    if '://' in rest:
        rest = rest.split('://')[1]
    for sep in ('/', ':'):
        if sep in rest:
            rest = rest.split(sep)[0]
    return 'jade.' + rest
''', [['https://base.example.com/api'], ['http://127.0.0.1:8099'], ['https://vault.local']], "One name per host."),
  PL("Find the config", "Write find_config(cwd, existing, env_path): if env_path is not empty return it; otherwise starting at cwd (an absolute path like /a/b/c) look for cwd + '/jade.config.yaml' in the list existing, then the parent folder, and so on up to /. Return the first path found or None.", "find_config(cwd, existing, env_path)", '''
def find_config(cwd, existing, env_path):
    if env_path:
        return env_path
    parts = [p for p in cwd.split('/') if p]
    while True:
        folder = '/' + '/'.join(parts)
        cand = (folder if parts else '') + '/jade.config.yaml'
        if cand in existing:
            return cand
        if not parts:
            return None
        parts = parts[:-1]
''', [['/home/me/proj/sub', ['/home/me/jade.config.yaml'], ''], ['/a/b', [], ''], ['/a/b', ['/a/b/jade.config.yaml', '/jade.config.yaml'], ''], ['/x', [], '/etc/jade.yaml']], "Walk up folder by folder."),
  PL("Where does the secret come from", "Write secret_source(name_env_set, keyring_has, file_allowed, file_has): return 'env' if name_env_set; else 'keyring' if keyring_has; else 'file' if file_allowed and file_has; else None.", "secret_source(name_env_set, keyring_has, file_allowed, file_has)", '''
def secret_source(name_env_set, keyring_has, file_allowed, file_has):
    if name_env_set:
        return 'env'
    if keyring_has:
        return 'keyring'
    if file_allowed and file_has:
        return 'file'
    return None
''', [[True, True, True, True], [False, True, False, False], [False, False, True, True], [False, False, False, True]], "The lookup order."),
  PL("URL carries a token", "Write url_has_token(url): True if the part after the first '?' contains a parameter named token (token=), access_token= or api_key=, or the URL has user:password@ credentials before the host.", "url_has_token(url)", '''
def url_has_token(url):
    rest = url.split('://')[-1]
    host = rest.split('/')[0]
    if '@' in host:
        return True
    if '?' not in url:
        return False
    q = url.split('?', 1)[1]
    for pair in q.split('&'):
        k = pair.split('=')[0]
        if k in ('token', 'access_token', 'api_key'):
            return True
    return False
''', [['https://v.example.com/v1/status?token=abc'], ['https://v.example.com/v1/status'], ['https://u:p@host/x'], ['https://h/x?a=1&api_key=z'], ['https://h/x?mytoken=1']], "Credentials belong in headers."),
  PL("Unknown config keys", "Write unknown_keys(cfg_keys, allowed): the sorted keys in cfg_keys that are not in allowed.", "unknown_keys(cfg_keys, allowed)", '''
def unknown_keys(cfg_keys, allowed):
    return sorted([k for k in cfg_keys if k not in allowed])
''', [[['version', 'targets', 'aprovals'], ['version', 'targets', 'approvals']], [['version'], ['version']], [['z', 'a'], []]], "Typos become errors.")]
))

CHS.append(CH(
 "The harness: approvals, idempotency and task credentials",
 ("Harness", [
  "Harness | checks | Every call",
  "Approval | allows | By pattern",
  "Deny | wins | Over allow",
  "Idempotency key | prevents | Double runs",
  "Task credential | limits | Scope and time",
  "Destructive | needs | A person",
  "Approvals log | records | Decisions"]),
 ["Every SDK call and command passes through the harness before it leaves, in the same process. It applies approvals, attaches idempotency keys and mints short-lived credentials.",
  "Approvals are patterns by capability and target, such as base.write: record_*:bookings. Deny rules win over allow rules. A call that no rule covers needs a person to confirm, and destructive tools need confirmation even when allowed.",
  "Mutations always carry an idempotency key, so a retry cannot run twice. Task credentials last minutes and carry only the scopes the task needs; a refusal stops the run."],
 [("Harness", "The in-process layer that checks every call: approvals, idempotency, credentials and compatibility."),
  ("Approval rule", "A pattern permitting or denying a capability on a target, where deny always beats allow."),
  ("Idempotency key", "An identifier ensuring a mutation runs once; a repeat gets the first answer."),
  ("Task credential", "A short-lived token with limited scopes minted for one task."),
  ("Yolo", "A flag that skips confirmation, always recorded in the approvals log.")],
 ["base.write: [\"record_*:bookings\"].",
  "Deny wins.",
  "Uncovered call: confirm or --yolo.",
  "Reads retry; mutations do not.",
  "Credential TTL 15 minutes by default."],
 [T("Think of the harness as a security desk at the door of a building. Every call, whether from a script, an agent or a person at the command line, must pass it. The desk consults a list of what is permitted. If an entry denies the visitor, that settles it. If nothing mentions the visitor, a person is asked. Only if an entry allows the visit does it go ahead without asking, and even then the desk insists on a signature for anything destructive."),
  T("The list is the approvals section of the config. Each key names a capability: base.read, base.write, base.schema and other Base scopes, vault.chat, vault.flow, kit.page, shell, http_request. Each value lists target patterns where star matches anything, like record_star colon bookings meaning any record tool on the bookings collection. A deny rule always wins, even over a broader allow. A bare true is rejected as too vague. Every confirmation, refusal and use of the yolo flag is appended to a local approvals log with the time, target, task and scope."),
  C("approvals:\n  base.read: [\"*\"]\n  base.write: [\"record_*:bookings\"]\n  base.schema: {allow: [\"collection_create:*\"], deny: [\"collection_delete:*\"]}\n  shell: {allow: [ls, cat, grep], deny: [rm, curl, wget]}", "yaml"),
  T("Idempotency is the second safeguard. A mutation always carries a key: one you give, one from a context manager, or a fresh UUID. Base runs a given key once and replays the first answer for 24 hours. So if a phone sleeps mid-flow, or a network drops after the request arrived, sending it again is safe. The same key with different arguments is a conflict, error JADE205. Reads may retry on network errors; mutations never retry on their own, because the toolkit cannot know whether the first attempt happened."),
  T("The third safeguard is the task credential. A with-block over a task mints a Base credential, valid fifteen minutes by default, scoped to what the task needs, and revokes it afterwards. Even a hijacked task cannot do more than its scopes allow, and not for long. If Base answers credential_refused the run stops and is not retried. Compatibility is checked as well: a major version mismatch with a target is refused. Together, approvals limit what may be asked, keys limit repeats, and credentials limit power.")],
 [("What wins between a matching allow and deny?", ["Deny", "Allow", "The newer rule", "The shorter rule"], 0, "Deny wins."),
  ("What happens to a call no rule covers?", ["A person must confirm, or --yolo", "It runs silently", "It is deleted", "It is cached"], 0, "Not assumed safe."),
  ("What does an idempotency key prevent?", ["Running a mutation twice", "Reading data", "Logging in", "Parsing YAML"], 0, "Replay."),
  ("Do mutations retry automatically?", ["No, never by themselves", "Always", "Ten times", "Only at night"], 0, "Unknown outcome."),
  ("Why short-lived task credentials?", ["A hijacked task can do little and not for long", "They are cheaper", "They are faster", "They are prettier"], 0, "Least privilege."),
  ("What does JADE205 mean?", ["Same key with other arguments", "Bad token", "Timeout", "Missing file"], 0, "Idempotency conflict.")],
 [("harness.task('job', scopes=[...])", "mint a task credential"), ("--yolo", "skip confirmation, logged")],
 [APP("APPROVE", "Approvals tester", "Write allow and deny patterns and test targets against them. See how deny wins, how an uncovered call needs a person and how destructive tools still ask. Reach three different decision kinds to complete the lab.", 820),
  MATCH("Match the safeguard", "Pair each safeguard with what it limits.", [("Approvals", "what may be asked"), ("Idempotency key", "repeat runs"), ("Task credential", "power and time"), ("Deny rule", "overrides allow"), ("Approvals log", "decisions recorded")]),
  PL("Glob match", "Write glob(pattern, text): True if text matches the pattern, where '*' matches any run of characters (including none) and everything else must match exactly.", "glob(pattern, text)", '''
def glob(pattern, text):
    parts = pattern.split('*')
    if len(parts) == 1:
        return pattern == text
    if not text.startswith(parts[0]):
        return False
    pos = len(parts[0])
    for mid in parts[1:-1]:
        i = text.find(mid, pos)
        if i < 0:
            return False
        pos = i + len(mid)
    last = parts[-1]
    if len(text) - pos < len(last):
        return False
    return text.endswith(last)
''', [['record_*:bookings', 'record_create:bookings'], ['record_*:bookings', 'record_create:posts'], ['*', 'anything'], ['a*b*c', 'axxbyyc'], ['a*b', 'ab'], ['exact', 'exact'], ['exact', 'exactly']], "Split on stars."),
  PL("Approval decision", "Write decide(allow, deny, target, destructive): 'deny' if any deny pattern matches target (using * globbing); else 'allow' if an allow pattern matches and not destructive; 'confirm' if an allow pattern matches and destructive; 'confirm' if nothing matches.", "decide(allow, deny, target, destructive)", '''
def glob(pattern, text):
    parts = pattern.split('*')
    if len(parts) == 1:
        return pattern == text
    if not text.startswith(parts[0]):
        return False
    pos = len(parts[0])
    for mid in parts[1:-1]:
        i = text.find(mid, pos)
        if i < 0:
            return False
        pos = i + len(mid)
    last = parts[-1]
    if len(text) - pos < len(last):
        return False
    return text.endswith(last)
def decide(allow, deny, target, destructive):
    for d in deny:
        if glob(d, target):
            return 'deny'
    matched = False
    for a in allow:
        if glob(a, target):
            matched = True
    if matched and not destructive:
        return 'allow'
    return 'confirm'
''', [[['collection_*:*'], ['collection_delete:*'], 'collection_delete:users', True], [['collection_*:*'], ['collection_delete:*'], 'collection_create:users', False], [['records_list'], [], 'records_list', False], [[], [], 'record_create:x', False], [['collection_*:*'], [], 'collection_delete:x', True]], "Deny first, then allow, else ask."),
  PL("Replay with idempotency keys", "Write replay(calls): calls is a list of [key, args_string]. Simulate Base: the first time a key is seen with its args it is 'ran'; the same key with the same args again is 'replayed'; the same key with different args is 'conflict'. Return the list of outcomes.", "replay(calls)", '''
def replay(calls):
    seen = {}
    out = []
    for key, args in calls:
        if key not in seen:
            seen[key] = args
            out.append('ran')
        elif seen[key] == args:
            out.append('replayed')
        else:
            out.append('conflict')
    return out
''', [[[['k1', 'a'], ['k1', 'a'], ['k2', 'b'], ['k1', 'c']]], [[]], [[['x', '1'], ['x', '1'], ['x', '1']]]], "Once per key."),
  PL("Parse a duration", "Write seconds(text): convert '30s', '15m', '2h' or '1d' into seconds; a bare number string means seconds.", "seconds(text)", '''
def seconds(text):
    unit = text[-1]
    if unit in 'smhd':
        n = int(text[:-1])
        return n * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
    return int(text)
''', [['15m'], ['30s'], ['2h'], ['1d'], ['90']], "Unit suffixes."),
  PL("Credential still valid", "Write cred_valid(minted_at, ttl_seconds, now, revoked): True if not revoked and now is before minted_at + ttl_seconds.", "cred_valid(minted_at, ttl_seconds, now, revoked)", '''
def cred_valid(minted_at, ttl_seconds, now, revoked):
    return (not revoked) and now < minted_at + ttl_seconds
''', [[100, 900, 500, False], [100, 900, 1000, False], [100, 900, 500, True], [0, 900, 900, False]], "Revocation fails closed."),
  PL("Least-privilege scopes", "Write narrow(requested, agent_scopes): the sorted list of scopes in requested that are also in agent_scopes (a credential can only be a subset of the agent's scopes).", "narrow(requested, agent_scopes)", '''
def narrow(requested, agent_scopes):
    return sorted([s for s in set(requested) if s in agent_scopes])
''', [[['read', 'write', 'billing'], ['read', 'write']], [['schema'], ['read']], [['read', 'read'], ['read']]], "A subset of the agent's scopes.")]
))

CHS.append(CH(
 "Errors, exit codes and version compatibility",
 ("Errors", [
  "Error code | is | Stable",
  "Remediation | tells | What to do",
  "Exit 0 | means | Ok",
  "Exit 1 | means | User error",
  "Exit 2 | means | Remote error",
  "Exit 3 | means | Refused for safety",
  "STACK.md | lists | Compatible versions"]),
 ["Every failure has a stable code of the form JADE and three digits, a message and a remediation. The first digit groups them: 1xx auth and secrets, 2xx remote, 3xx safety, 4xx user input, 5xx doctor.",
  "Exit codes tell scripts what kind of failure it was: 0 ok, 1 user error, 2 remote error, 3 refused for safety. A script should treat 3 as a stop, not something to retry.",
  "Version checks keep the parts compatible: a different major version is refused (JADE203), an older minor is a warning. A Vault that accepts tokens in URLs is refused (JADE102)."],
 [("Stable error code", "An identifier that never changes meaning, so tools can react to it."),
  ("Remediation", "A sentence telling the reader how to fix the problem."),
  ("Exit code", "The number a command returns to the shell: 0 success, nonzero failure."),
  ("Major version", "The first number of a version; a change means incompatible interfaces."),
  ("Doctor", "The health check comparing target versions with STACK.md.")],
 ["JADE1xx auth, 2xx remote, 3xx safety, 4xx input.",
  "0 ok, 1 user, 2 remote, 3 safety.",
  "Never retry exit 3.",
  "Major mismatch refused, older minor warns.",
  "str(error) never shows a secret."],
 [T("Good error handling is half of good automation. Jade's errors have codes that never change meaning, such as JADE100 for not configured or JADE301 for denied by approvals, a human message, and a remediation sentence. Printing an error shows all three, and never a secret, because messages pass through redaction. In Python they all derive from one class, JadeError, carrying the code, message, remediation and exit code."),
  T("The codes are grouped. The hundreds digit says where to look. JADE1xx concerns authentication and secrets: no config, a bad token, a refused legacy URL-token Vault, a refused credential, a missing secret store or secret. JADE2xx concerns the remote target: unreachable, protocol mismatch, an error answer, an incompatible version, a timeout, an idempotency conflict. JADE3xx is safety: approval required, denied, unsafe without confirmation, playbook not approved. JADE4xx is bad input: invalid config, playbook or site spec, unknown or ambiguous tool, not found, stale generated files. JADE500 means doctor failed."),
  C("import jade\ntry:\n    jade.Stack.load().call('base', 'collection_delete', {'name': 'x'})\nexcept jade.JadeError as e:\n    print(e.code, e.exit_code)     # e.g. JADE302 3\n    print(e.remediation)           # what to do next", "python"),
  T("Scripts see the same classification as exit codes. Zero is success. One is your mistake: fix the input. Two is the remote side: it may be down, so a read can be retried later. Three is a refusal for safety: approvals, credentials, or an unapproved playbook. A wrapper script must treat three as final. Retrying around a refusal is exactly the behaviour the design tries to prevent."),
  T("Versions are the other source of trouble, so the toolkit declares what it works with in STACK.md: Base from 0.6.0, Vault from 2.18.3, Kit from 3.1.0 and UI from 1.2.0 in version 0.1.0. Doctor compares what each target reports. A different major version is refused, since interfaces changed incompatibly. An older minor version only warns. Because JADE102 treats a Vault that still accepts tokens in query strings as unsafe, a too-old Vault is refused for security reasons as well.")],
 [("What does exit code 3 mean?", ["Refused for safety", "Success", "User error", "Remote error"], 0, "Do not retry."),
  ("What does JADE301 mean?", ["Denied by approvals", "Bad token", "Timeout", "Stale files"], 0, "3xx is safety."),
  ("Which digit group is remote errors?", ["2xx", "1xx", "3xx", "4xx"], 0, "Where to look."),
  ("What happens on a major version mismatch?", ["The target is refused", "Nothing", "A warning only", "Auto upgrade"], 0, "JADE203."),
  ("What does an older minor version cause?", ["A warning", "A refusal", "A crash", "Deletion"], 0, "Compatible but old."),
  ("Do error messages contain secrets?", ["Never, they are redacted", "Always", "Sometimes", "Only in debug"], 0, "Redaction.")],
 [("jade.JadeError", "base class for errors"), ("jade doctor", "compare versions")],
 [MATCH("Match the code", "Pair each code or exit with its meaning.", [("JADE103", "credential refused"), ("JADE204", "timed out"), ("JADE403", "unknown tool"), ("Exit 2", "remote error"), ("Exit 3", "refused for safety")]),
  PL("Exit code for an error", "Write exit_code(code): given the numeric part of a JADE code (such as 103 or 301): 3 for 102, 103 and 300 to 399; 2 for 200 to 299; otherwise 1.", "exit_code(code)", '''
def exit_code(code):
    if code in (102, 103) or 300 <= code <= 399:
        return 3
    if 200 <= code <= 299:
        return 2
    return 1
''', [[100], [102], [103], [200], [205], [301], [401], [500]], "Group by the hundreds digit, with two exceptions."),
  PL("Should a script retry", "Write should_retry(exit, is_read): True only for exit 2 on a read; never for 0, 1 or 3.", "should_retry(exit, is_read)", '''
def should_retry(exit, is_read):
    return exit == 2 and is_read
''', [[2, True], [2, False], [3, True], [1, True], [0, True]], "Refusals are final."),
  PL("Parse a version", "Write parse_version(text): [major, minor, patch] as integers from 'a.b.c' (missing parts are 0).", "parse_version(text)", '''
def parse_version(text):
    p = [int(x) for x in text.split('.')]
    while len(p) < 3:
        p.append(0)
    return p[:3]
''', [['0.6.0'], ['2.18.3'], ['3.1'], ['1']], "Three numbers."),
  PL("Compatibility verdict", "Write compat(have, minimum): compare versions 'a.b.c': 'refused' if the major numbers differ; 'warn' if the majors agree but have is older than minimum; otherwise 'ok'.", "compat(have, minimum)", '''
def pv(t):
    p = [int(x) for x in t.split('.')]
    while len(p) < 3:
        p.append(0)
    return p[:3]
def compat(have, minimum):
    h = pv(have)
    m = pv(minimum)
    if h[0] != m[0]:
        return 'refused'
    if h < m:
        return 'warn'
    return 'ok'
''', [['0.6.2', '0.6.0'], ['0.5.9', '0.6.0'], ['1.0.0', '0.6.0'], ['2.18.3', '2.18.3'], ['2.19.0', '2.18.3'], ['2.17.0', '2.18.3'], ['3.0.0', '2.18.3']], "Major must agree."),
  PL("Doctor summary", "Write doctor(results): results is a list of [target, verdict] where verdict is 'ok', 'warn' or 'refused'. Return 'failed' if any is refused, else 'warnings' if any is warn, else 'ok'.", "doctor(results)", '''
def doctor(results):
    v = [r[1] for r in results]
    if 'refused' in v:
        return 'failed'
    if 'warn' in v:
        return 'warnings'
    return 'ok'
''', [[[['base', 'ok'], ['vault', 'warn']]], [[['base', 'ok'], ['vault', 'refused']]], [[['base', 'ok']]], [[]]], "Worst verdict wins."),
  PL("Legacy Vault check", "Write vault_status(accepts_url_token, accept_legacy): 'refused' if the Vault accepts tokens in URLs and accept_legacy is False; 'warn' if it does and accept_legacy is True; else 'ok'.", "vault_status(accepts_url_token, accept_legacy)", '''
def vault_status(accepts_url_token, accept_legacy):
    if accepts_url_token:
        return 'warn' if accept_legacy else 'refused'
    return 'ok'
''', [[True, False], [True, True], [False, False]], "JADE102.")]
))
