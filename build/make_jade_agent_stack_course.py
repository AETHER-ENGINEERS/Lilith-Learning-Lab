#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Jade Agent Stack course. Usage: python3 make_jade_agent_stack_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "jas"))
import cmk, jas_a, jas_b, make_apps  # noqa: E402
make_apps.main()
CHS = jas_a.CHS + jas_b.CHS
PRONOUNCE = {"Jade": "jayd", "Vault": "vawlt", "Kit": "kit", "UI/UX": "you eye you ex", "MCP": "M C P", "YAML": "yam ul", "PyYAML": "pie yam ul", "REPL": "reppel", "CLI": "C L I",
    "JSON": "jay son", "SDK": "S D K", "HTTP": "H T T P", "REST": "rest", "CDN": "C D N", "OAuth2": "oh auth two", "SHA-256": "shaw two fifty six", "idempotency": "eye dem poh ten see",
    "idempotent": "eye dem poh tent", "keyring": "key ring", "PocketBase": "pocket base", "JADE103": "jade one oh three", "TTL": "T T L", "UUIDv7": "U U I D version seven",
    "Lisp": "lisp", "asyncio": "a sink eye oh", "loopback": "loop back", "exfiltration": "ex fill tray shun"}
SANDBOX = cmk.terminal("Jade cheat sheet", "jade>", "A scripted lookup. Try: init, doctor, secret, approvals, playbook, site, mcp, serve, exit, errors, versions", [
    ("init", ["jade init: seven steps, resumable. --yes for defaults, --answers FILE for headless."]),
    ("doctor", ["jade doctor: reachable, authenticated, compatible, no tokens in URLs."]),
    ("secret", ["jade secret set NAME (hidden prompt), list (names only), rm NAME. Order: env JADE_SECRET_NAME, keyring, 0600 file."]),
    ("approvals", ["Patterns by capability and target. Deny wins. Uncovered: confirm or --yolo. Destructive: confirm."]),
    ("playbook", ["check, plan, approve, run. Fail modes: stop, continue, rollback. Approval is bound to the file hash."]),
    ("site", ["jade site new / check / build / preview / plan / deploy. Plan makes no calls."]),
    ("mcp", ["jade mcp serves commands as tools over stdio: site_build, site_deploy, playbook_run, docs_search."]),
    ("serve", ["jade serve: 127.0.0.1:9765. Other hosts need a bearer token in the header."]),
    ("exit", ["0 ok, 1 user error, 2 remote error, 3 refused for safety."]),
    ("errors", ["JADE1xx auth, 2xx remote, 3xx safety, 4xx input, 500 doctor. JADE103: stop, do not retry."]),
    ("versions", ["Base 0.6.0+, Vault 2.18.3+, Kit 3.1.0+, UI 1.2.0+ for toolkit 0.1.0. Major mismatch refused."]),
])
EXAM = [
 ("What is the Stack?", ["A client toolkit over four Jade repositories", "A replacement for Vault", "A database", "A browser"], 0, "Client."),
 ("Vault is the:", ["Control plane", "Resource plane", "Theme library", "Database"], 0, "Agent loop."),
 ("Base keeps the:", ["Authoritative audit log", "Transcript", "Themes", "Shell"], 0, "agent_audit."),
 ("What is the Vault-Base seam?", ["MCP, with the same tools over REST", "A file share", "Email", "FTP"], 0, "/api/agent/mcp."),
 ("What should happen after credential_refused?", ["Stop and tell the person", "Retry", "Escalate scopes", "Ignore"], 0, "Do not retry."),
 ("Where are secrets looked up first?", ["Environment variables", "A file", "The URL", "The config"], 0, "JADE_SECRET_."),
 ("Why are tokens in URLs refused?", ["They leak into logs", "They are long", "They are slow", "They are unusual"], 0, "Header-only."),
 ("What wins between allow and deny?", ["Deny", "Allow", "Newest", "Longest"], 0, "Always deny."),
 ("What does an idempotency key do?", ["Runs a mutation once", "Encrypts it", "Speeds it", "Hides it"], 0, "Replay."),
 ("Default task credential lifetime?", ["15 minutes", "1 year", "Forever", "1 second"], 0, "Short."),
 ("Exit code 3 means:", ["Refused for safety", "OK", "User error", "Remote error"], 0, "Stop."),
 ("JADE2xx errors concern:", ["The remote target", "Typos", "Safety", "Themes"], 0, "Remote."),
 ("Major version mismatch gives:", ["Refusal", "Warning", "Nothing", "Upgrade"], 0, "JADE203."),
 ("What does playbook plan do?", ["Lists calls without making any", "Runs", "Deletes", "Signs"], 0, "Dry run."),
 ("Approval is bound to:", ["The file hash", "The date", "The user", "The folder"], 0, "Edits invalidate."),
 ("Rollback does what?", ["Undoes finished tasks in reverse", "Skips errors", "Retries forever", "Deletes logs"], 0, "Needs undo."),
 ("A minimal site needs:", ["name, tagline, template", "a server", "a database", "a framework"], 0, "Three lines."),
 ("Spec page with the same path as a template page:", ["Replaces it", "Is ignored", "Appends", "Errors"], 0, "Replace by path."),
 ("email:email! means:", ["A required email field", "Optional text", "A file", "A relation"], 0, "Bang."),
 ("site.build over MCP is:", ["site_build", "site-build", "build", "siteBuild"], 0, "Underscore."),
 ("jade serve binds to:", ["127.0.0.1 by default", "0.0.0.0 always", "Nowhere", "The cloud"], 0, "Loopback."),
 ("What cannot an agent do over MCP?", ["Approve a playbook", "Search docs", "Build a site", "List commands"], 0, "Needs a person."),
 ("Prompt injection means:", ["Hostile text steering an agent", "A faster prompt", "A UI bug", "A typo"], 0, "Data as instructions."),
 ("Which scopes are root-like?", ["schema, hooks, settings", "read", "write", "gateway"], 0, "Grant sparingly."),
 ("Why run agents as a lesser user?", ["Guards do not cover a shell as you", "Speed", "Disk", "Style"], 0, "Contain."),
 ("How to report a vulnerability?", ["Privately via security advisory", "Public issue", "Tweet", "Ignore"], 0, "Responsible."),
]
CFG = dict(id="jade-agent-stack", title="Jade Agent Stack",
    subtitle="Driving Jade Vault and Agent Base safely: harness, approvals, playbooks, sites, surfaces and security, with Python labs",
    description="A hands-on course based on the open Jade Agent Stack toolkit (github.com/lucky-edgelord/jade-agent-stack, MIT). Learn how the Jade parts fit together (Vault asks, Base answers, Base logs, Base can say no); configuration, the OS keyring and header-only authentication; the harness with approval patterns where deny wins, idempotency keys and short-lived task credentials; stable error codes, exit codes and version compatibility; portable YAML playbooks with check, plan, approve, run, rollback and resume; the site compiler from a YAML spec to pages and a Base backend; the CLI, REPL, JSON lines, MCP, HTTP and Python surfaces and how agents work through them; and the threat model with defences against prompt injection. Based on version 0.1.0 of the documentation; check the repository for later changes. Every chapter has Python labs verified in the built-in interpreter, plus an approvals tester and a playbook run simulator.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="jas", apps={"__APPROVE__": "approve.html", "__RUN__": "run.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "jade-agent-stack.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
