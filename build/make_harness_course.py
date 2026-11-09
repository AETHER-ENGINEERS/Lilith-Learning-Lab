#!/usr/bin/env python3
"""Build the harness engineering course. Usage: python3 make_harness_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "hrn"))
import cmk, hrn  # noqa: E402

PRONOUNCE = {
    "MCP": "M C P", "JSON": "jay son", "API": "A P I", "APIs": "A P Is", "LLM": "L L M", "GPUs": "G P Us", "GPU": "G P U",
    "pass@k": "pass at k", "pass@3": "pass at 3", "sub-agent": "sub agent", "Sub-agent": "Sub agent", "sub-agents": "sub agents",
    "idempotent": "eye dem poh tent", "Idempotent": "Eye dem poh tent", "idempotence": "eye dem poh tence", "Idempotence": "Eye dem poh tence",
    "Anthropic": "an throp ick", "toolset": "tool set", "todo": "to do", "dev": "dev",
}

SANDBOX = cmk.terminal("Harness lookup", "hx>", "A scripted lookup, not a real agent. Try: loop, parts, limits, evals", [
    ("loop", ["build prompt -> call model -> parse reply -> run tool or finish -> append observation", "always bound with a step limit"]),
    ("parts", ["instructions, tools, memory, context management, permissions, orchestration, observability, evals"]),
    ("limits", ["steps, tokens, time, money, retries", "backoff delay = min(cap, base * 2^attempt)"]),
    ("evals", ["success rate = successes / runs", "pass@k = 1 - (1 - p)^k", "keep a regression suite"]),
    ("safety", ["allowlist, approval for risky actions, sandbox, path checks, audit log"]),
])

EXAM = [
 ("What is an agent in the harness view?", ["A model plus a harness", "Only a model", "A database", "A prompt"], 0, "The harness gives tools, memory and a loop."),
 ("What does the model do on its own?", ["Turns text into text", "Runs commands", "Stores files", "Checks permissions"], 0, "Everything else is the harness."),
 ("Which layer is the widest?", ["Harness engineering", "Prompt engineering", "Tokenization", "Fine-tuning"], 0, "It includes context and prompt work."),
 ("What does context engineering decide?", ["What the model sees at each step", "Model size", "Learning rate", "Licensing"], 0, "Beyond wording."),
 ("What ends the agent loop?", ["A final answer or a limit", "The first tool call", "A timer only", "The tool result"], 0, "Always bound it."),
 ("What should happen on a malformed model reply?", ["Report it and continue", "Crash", "Delete history", "Stop silently"], 0, "Turn it into an observation."),
 ("Why use a scripted model in tests?", ["Deterministic results", "Higher accuracy", "Lower latency only", "No tools needed"], 0, "Same replies each time."),
 ("What does the model see of a tool?", ["Name, description and schema", "Its source code", "Its tests", "Its logs"], 0, "So descriptions matter."),
 ("What should a validation failure return?", ["A helpful error message as an observation", "A crash", "Nothing", "A random result"], 0, "Part of the prompt."),
 ("Which is better design?", ["A few clear tools", "Many overlapping tools", "One tool with no description", "No tools"], 0, "Models confuse similar tools."),
 ("What is MCP?", ["A standard for exposing tools and data to models", "A model", "A GPU", "A prompt style"], 0, "Model Context Protocol."),
 ("Why truncate large tool outputs?", ["To save context", "To hide errors", "To speed up the GPU", "To avoid logs"], 0, "And say that you did."),
 ("What is pinned in the context?", ["System prompt and task", "The oldest observation", "Every tool result", "Nothing"], 0, "They must stay visible."),
 ("What goes first when the budget is exceeded?", ["The oldest unpinned messages", "The newest message", "The task", "The system prompt"], 0, "Recent content matters most."),
 ("What does summarization do?", ["Compresses old messages", "Adds tools", "Trains the model", "Deletes the task"], 0, "Lossy but smaller."),
 ("What is context rot?", ["Quality loss in a bloated or stale context", "A bug in tokenization", "A GPU fault", "A licence term"], 0, "A practitioner term."),
 ("Where does long-term memory live?", ["Outside the model", "In the weights", "In the GPU", "In the prompt only"], 0, "Files or a database."),
 ("What is a checkpoint?", ["A saved snapshot of run state", "A tool", "A prompt", "A bug"], 0, "To resume after a crash."),
 ("Why are rules enforced in the harness code?", ["A prompt is only a request", "Code is faster", "Models cannot read", "It is cheaper"], 0, "Controls must not depend on the model's compliance."),
 ("What does default deny mean?", ["Unknown actions are refused", "All actions are allowed", "Ask the model", "Log only"], 0, "Allowlist."),
 ("What is least privilege?", ["Granting only the access the task needs", "Giving full access", "Denying all access", "Sharing keys"], 0, "Limits damage."),
 ("What is prompt injection?", ["Instructions hidden in data the model reads", "A faster prompt", "A training method", "A tool"], 0, "Treat results as data."),
 ("Why resolve '..' in paths before checking?", ["To stop escapes from the workspace", "To shorten paths", "To sort files", "To save memory"], 0, "Path traversal."),
 ("What is a context firewall?", ["Keeping a sub-agent's detail out of the parent's context", "A network device", "A prompt filter", "A tool"], 0, "Return summaries."),
 ("Which subtasks can run in parallel?", ["Those with no unmet dependencies", "Dependent ones", "None", "Only the first"], 0, "Ready tasks."),
 ("What must a sub-agent's brief contain?", ["Everything it needs", "The parent's whole history", "Nothing", "Only its name"], 0, "It cannot see the parent."),
 ("Which error deserves a retry?", ["A timeout", "Invalid arguments", "File not found", "Permission denied"], 0, "Transient errors only."),
 ("What does exponential backoff do?", ["Waits longer after each failure", "Retries instantly", "Stops forever", "Skips steps"], 0, "Often doubling with a cap."),
 ("What does loop detection watch for?", ["The same action repeated without progress", "Long answers", "Slow networks", "Big files"], 0, "Stuck agents."),
 ("What does a trace record?", ["Each step of a run", "Only the answer", "The weights", "GPU load"], 0, "Prompts, calls, results, cost."),
 ("What should a grader check?", ["The outcome", "The exact wording", "The reply length", "The font"], 0, "For example, whether tests pass."),
 ("What is pass@k?", ["Chance at least one of k tries succeeds", "Chance all fail", "A token count", "A latency"], 0, "1 - (1 - p)^k."),
 ("What do regression evals guard?", ["Tasks that already worked", "New hard tasks", "Model size", "Prompt length"], 0, "Scores should stay near 100 percent."),
 ("Why run each eval task several times?", ["Agents are random", "To use more tokens", "Graders are slow", "Logs are short"], 0, "One run proves little."),
 ("What is ablation?", ["Removing a component to test its value", "Adding a tool", "Training", "Summarizing"], 0, "Rerun the evals."),
 ("Where should you start building a harness?", ["Simple loop plus a small eval", "A large multi-agent swarm", "A new model", "A big framework"], 0, "Add only what traces justify."),
 ("What may happen to scaffolding when models improve?", ["It can become unnecessary or harmful", "It becomes mandatory", "It doubles in value", "Nothing"], 0, "Re-test it."),
 ("What kind of sources does this course mostly use?", ["Practitioner write-ups, which are secondary", "Peer-reviewed proofs", "Law texts", "Hardware manuals"], 0, "The field is young."),
]

CFG = dict(id="harness-engineering", title="Harness Engineering for AI Agents", subtitle="The loop, tools, context, memory, guardrails, orchestration and evals, with Python labs",
    description="Agent = model + harness. Build the pieces of an agent harness in small deterministic Python labs: the agent loop, tool schemas, context management, memory and checkpoints, guardrails and permissions, sub-agents, retries and limits, traces and evals. Based on recent practitioner write-ups, which are secondary sources.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="hrn", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "harness-engineering.course.json")
    cmk.main(CFG, hrn.CHS, [sys.argv[0], out])
