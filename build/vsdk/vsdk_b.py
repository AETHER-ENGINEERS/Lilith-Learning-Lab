# -*- coding: utf-8 -*-
"""Vector SDK course, part 2: communities, privacy and security, example bots, troubleshooting."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Communities, invites and members",
 ("Communities", [
  "Community | has | Members and roles",
  "Invite | is handled by | Policy",
  "Manual | needs | accept_invite",
  "Public | accepts | Anyone",
  "Whitelist | accepts | Listed npubs",
  "Member | can be | Kicked or banned",
  "capabilities | tell | What bot may do"]),
 ["A community is a shared space with members and roles. Your bot can be invited to one, read and send messages there, welcome new members, and, if it has the rights, moderate.",
  "What happens to an invitation depends on the invite policy you set on the builder. Manual is the default and leaves invites pending until you call accept_invite. Public accepts everyone. Whitelist accepts only listed npubs and quietly ignores the rest.",
  "Invitations that arrived while the bot was offline are accepted on startup in the automatic modes."],
 [("Invite policy", "The builder setting that decides what the bot does with invitations."),
  ("Whitelist", "A list of npubs whose invitations are accepted automatically."),
  ("Capability", "A right the bot has in a community, such as kicking or banning."),
  ("Role", "A set of rights given to members, such as admin."),
  ("Owner", "The member who created the community; only they can dissolve it.")],
 ["Default policy is Manual: use pending_invites() and accept_invite(&id).",
  "Public accepts anyone; Whitelist accepts only listed npubs and silently ignores others.",
  "Check community.capabilities() before kick or ban.",
  "dissolve() is owner only and cannot be undone.",
  "sync_communities() refreshes stale ids."],
 [T("Think of a club that sends your bot a membership card. Manual policy means a person looks at each card first. Public policy means the bot joins any club that asks. Whitelist means it only joins clubs run by people on a list."),
  C("// as described in the 0.3.0 docs\nlet bot = VectorBot::builder()\n    .nsec(&nsec)\n    .whitelist([\"npub1friend...\"])\n    .build()\n    .await?;\n\nfor invite in bot.pending_invites().await? {\n    // in Manual mode you decide\n    bot.accept_invite(&invite.id).await?;\n}", "rust"),
  T("In the whitelist mode, invitations from anyone else are silently ignored; the sender gets no refusal message. For a public helper bot you choose Public, but then anyone can add it to a community, so consider what it will do there."),
  T("Once inside, a community gives you member lists, roles, and methods to edit the name and description, create invites or leave. A Member can be asked for its profile, and checked with is_owner and is_admin."),
  T("Moderation actions such as kick and ban need admin rights. The bot should check capabilities first instead of trying and failing. Dissolve is the most destructive action: only the owner may call it, and it cannot be undone, so a bot should never do it without a person confirming."),
  T("If an id you stored no longer works, the bot's local view is stale. Run sync_communities to refresh it before assuming the community is gone.")],
 [("What is the default invite policy?", ["Manual", "Public", "Whitelist", "Reject"], 0, "A person decides."),
  ("What happens to a non-listed invite in Whitelist mode?", ["Silently ignored", "Accepted", "Error sent", "Banned"], 0, "No refusal."),
  ("Who may dissolve a community?", ["The owner only", "Any admin", "Any member", "The bot always"], 0, "Irreversible."),
  ("Before kick or ban, check:", ["capabilities()", "npub()", "typing()", "send()"], 0, "Admin rights."),
  ("Stale community id fix?", ["sync_communities()", "Restart relay", "Change nsec", "Delete the bot"], 0, "Refresh."),
  ("Offline invites in automatic modes?", ["Accepted on startup", "Lost", "Rejected", "Deleted"], 0, "Per the docs.")],
 [("pending_invites", "Invites waiting for a decision"), ("accept_invite", "Join a community from an invite"), ("capabilities", "What the bot may do"), ("dissolve", "Owner-only destruction")],
 [APP("POLICY", "Invite policy lab", "Try each policy against different senders and see what the bot does."),
  MATCH("Match the policy", "Pair each policy with its behaviour.", [("Manual", "waits for accept_invite"), ("Public", "accepts anyone"), ("Whitelist", "accepts only listed npubs"), ("Whitelist, unlisted sender", "silently ignored")]),
  FILL("Communities", "The default policy is {{Manual}}. A {{whitelist}} accepts only listed npubs. Kick and ban need {{admin}} rights, and only the {{owner}} can dissolve a community."),
  PL("Invite decision", "Write decide(policy, sender, whitelist): policy is 'manual', 'public' or 'whitelist'. Return 'accept' for public, and for whitelist when the sender is listed; 'pending' for manual; 'ignore' for an unlisted sender under whitelist.", "decide(policy, sender, whitelist)", '''
def decide(policy, sender, whitelist):
    if policy == 'public':
        return 'accept'
    if policy == 'manual':
        return 'pending'
    if sender in whitelist:
        return 'accept'
    return 'ignore'
''', [['public', 'x', []], ['manual', 'x', ['x']], ['whitelist', 'a', ['a', 'b']], ['whitelist', 'z', ['a']]], "Three policies."),
  PL("Startup invites", "Write startup(policy, offline_invites, whitelist): offline_invites is a list of sender names. In 'public' accept all, in 'whitelist' accept those listed, in 'manual' accept none. Return the accepted senders in order.", "startup(policy, offline_invites, whitelist)", '''
def startup(policy, offline_invites, whitelist):
    out = []
    for s in offline_invites:
        if policy == 'public' or (policy == 'whitelist' and s in whitelist):
            out.append(s)
    return out
''', [['public', ['a', 'b'], []], ['whitelist', ['a', 'b'], ['b']], ['manual', ['a'], ['a']]], "Automatic modes only."),
  PL("May moderate", "Write may_ban(caps, target_is_owner): caps is a list of capability names. True only when 'ban' is in caps and the target is not the owner.", "may_ban(caps, target_is_owner)", '''
def may_ban(caps, target_is_owner):
    return ('ban' in caps) and not target_is_owner
''', [[['ban', 'kick'], False], [['kick'], False], [['ban'], True], [[], False]], "Check the rights."),
  PL("Confirm destructive", "Write allow_action(action, confirmed_by_person): 'dissolve' and 'leave' need confirmation (return confirmed_by_person); 'send' and 'react' are always True; anything else is False.", "allow_action(action, confirmed_by_person)", '''
def allow_action(action, confirmed_by_person):
    if action in ('dissolve', 'leave'):
        return confirmed_by_person
    return action in ('send', 'react')
''', [['dissolve', False], ['dissolve', True], ['send', False], ['unknown', True]], "Destructive needs a person."),
  PL("Admins", "Write admins(members): members is a list of [npub, role] with role 'owner', 'admin' or 'member'. Return the sorted npubs of owners and admins.", "admins(members)", '''
def admins(members):
    out = []
    for n, r in members:
        if r in ('owner', 'admin'):
            out.append(n)
    out.sort()
    return out
''', [[[['b', 'admin'], ['a', 'owner'], ['c', 'member']]], [[]]], "Filter by role.")]))


CHS.append(CH(
 "Privacy, encryption and security practice",
 ("Security", [
  "Files | use | AES-256-GCM",
  "Hash | checks | Integrity",
  "NIP-59 | wraps | DMs",
  "Relays | can | Delay or withhold",
  "Profile | is | Public",
  "Key leak | exposes | Old messages",
  "Tor | hides | Network address"]),
 ["The documentation says files are encrypted with AES-256-GCM and verified with a SHA-256 hash, and that direct messages use NIP-59 gift wrapping. Reactions use NIP-25, typing indicators use NIP-40 expiry, and inbox relays use NIP-17.",
  "Privacy still has limits. Relays can withhold or delay messages, profile data is public, and if a key is compromised, past messages could be exposed.",
  "Good practice follows from that: never hardcode or commit keys, use wss relays, cap file sizes, keep logs free of sensitive data, rotate keys on a schedule, and report vulnerabilities privately."],
 [("AES-256-GCM", "An authenticated encryption mode; it hides content and detects tampering."),
  ("SHA-256", "A hash function used to check that data did not change."),
  ("Gift wrap", "A Nostr technique that hides who is talking to whom inside an outer envelope."),
  ("wss", "A websocket connection protected by TLS."),
  ("Tor", "An anonymity network that hides your network address; optional in the SDK through a feature.")],
 ["Do not commit keys; use environment variables.",
  "Use wss:// relays only.",
  "Cap file sizes and avoid logging sensitive content.",
  "A compromised key can expose old messages; rotate every 6 to 12 months.",
  "Report vulnerabilities privately; the team acknowledges within 48 hours."],
 [T("Imagine sending a letter inside a locked box, then inside a plain envelope with a fake return address. The box hides the contents, the outer envelope hides who is writing to whom. That is the idea behind encrypted files and gift-wrapped direct messages."),
  T("AES-256-GCM uses a 256-bit key, which is 32 bytes. The GCM mode also adds an authentication tag, conventionally 16 bytes, so the encrypted data is longer than the original by that amount, and any change to it is detected when decrypting."),
  T("The SHA-256 hash is like a fingerprint. If a downloaded file does not match the fingerprint that came with it, it was damaged or tampered with, and the bot should refuse to use it."),
  T("Be honest about limits. A relay can see that something arrived even if it cannot read it, and can drop or delay messages. Profile information such as a name is public. And since keys do not expire on their own, losing one can expose history."),
  C("// the optional Tor feature, as the docs describe it\n# Cargo.toml:  vector-sdk = { version = \"0.3\", features = [\"tor\"] }\nlet bot = VectorBot::builder()\n    .nsec(&nsec)\n    .tor()\n    .build()\n    .await?;", "rust"),
  T("Tor needs both the Cargo feature and the tor call. Without the feature the call has no effect, so test that it really takes effect rather than assuming it did. Startup is slower because the embedded client has to bootstrap during build.")],
 [("Which cipher protects files?", ["AES-256-GCM", "ROT13", "MD5", "None"], 0, "Authenticated encryption."),
  ("What does a SHA-256 hash check?", ["Integrity", "Speed", "Language", "Billing"], 0, "Fingerprint."),
  ("What can a relay do?", ["Withhold or delay messages", "Read gift-wrapped DMs", "Change your key", "Nothing"], 0, "Limits of privacy."),
  ("What does a leaked key expose?", ["Old messages", "Nothing", "Only new ones", "Just the name"], 0, "Rotate."),
  ("Which relay URL scheme is safe?", ["wss://", "ws://", "http://", "ftp://"], 0, "TLS."),
  ("Tor requires:", ["The Cargo feature and .tor()", "Only .tor()", "Only the feature", "A VPN"], 0, "Both.")],
 [("NIP-17", "Inbox relay lists for DMs"), ("NIP-25", "Reactions"), ("NIP-40", "Event expiration; used for typing"), ("NIP-59", "Gift wrap")],
 [MATCH("Match the protection", "Pair each risk with the safeguard.", [("tampered file", "SHA-256 check"), ("hidden sender", "gift wrap"), ("leaked key", "rotate keys"), ("plain connection", "wss relays")]),
  FILL("Security", "Files are encrypted with {{AES-256-GCM}}. A {{hash}} detects changes. Use {{wss}} relays and never commit a {{key}}."),
  PL("Encrypted size", "Write encrypted_len(plain_len): AES-GCM adds a 16 byte tag. Return plain_len + 16.", "encrypted_len(plain_len)", '''
def encrypted_len(plain_len):
    return plain_len + 16
''', [[0], [100], [1048576]], "Add the tag."),
  PL("Valid key size", "Write key_ok(key_bytes): True when the AES-256 key has exactly 32 bytes.", "key_ok(key_bytes)", '''
def key_ok(key_bytes):
    return key_bytes == 32
''', [[32], [16], [64], [0]], "256 bits."),
  PL("Safe relay", "Write relay_ok(url): True when the url starts with 'wss://'.", "relay_ok(url)", '''
def relay_ok(url):
    return url.startswith('wss://')
''', [['wss://relay.example'], ['ws://relay.example'], ['https://x'], ['']], "TLS only."),
  PL("File policy", "Write accept_file(size_bytes, limit_bytes, hash_matches): True only when the size is within the limit and the hash matches.", "accept_file(size_bytes, limit_bytes, hash_matches)", '''
def accept_file(size_bytes, limit_bytes, hash_matches):
    return size_bytes <= limit_bytes and hash_matches
''', [[100, 1000, True], [2000, 1000, True], [100, 1000, False], [1000, 1000, True]], "Both checks."),
  PL("Rotation due", "Write rotation_due(months_since_rotation, max_months): True when months_since_rotation is at least max_months.", "rotation_due(months_since_rotation, max_months)", '''
def rotation_due(months_since_rotation, max_months):
    return months_since_rotation >= max_months
''', [[3, 6], [6, 6], [14, 12]], "Rotate on schedule."),
  PL("Redact for logs", "Write redact(text): replace every occurrence of the characters following 'nsec1' (letters and digits) with the word nsec1[redacted]. Operate on whitespace-separated words: a word starting with 'nsec1' becomes 'nsec1[redacted]'. Return the joined text with single spaces.", "redact(text)", '''
def redact(text):
    out = []
    for w in text.split(' '):
        if w.startswith('nsec1'):
            out.append('nsec1[redacted]')
        else:
            out.append(w)
    return ' '.join(out)
''', [['key nsec1abcdef loaded'], ['no secrets here'], ['nsec1zz']], "Words that start with nsec1.")]))


CHS.append(CH(
 "Example bots: echo, slash, AI, moderation, files",
 ("Examples", [
  "echo_bot | repeats | Text",
  "slash_command_bot | parses | /ping /echo /roll /help",
  "ai_bot | calls | OpenAI-compatible API",
  "moderation_bot | welcomes and bans | By word filter",
  "whitelist_bot | accepts | Listed invites",
  "file_bot | sends | Files",
  "cargo run | starts | An example"]),
 ["The documentation ships a set of example bots: echo_bot, slash_command_bot, ai_bot, moderation_bot, whitelist_bot, file_bot and save_files_bot. All need the VECTOR_NSEC environment variable, and you start one with cargo run -p vector-sdk --example name.",
  "The slash_command_bot handles /ping, /echo, /roll and /help by parsing message text, since these are bot-side conventions in a chat, not a server feature. The ai_bot calls an OpenAI-compatible endpoint, shows a typing indicator, replies in threads and keeps a history per chat. It needs OPENAI_API_KEY.",
  "The moderation_bot welcomes members on MemberJoin and bans on a word filter."],
 [("Example", "A small runnable program in the repository that shows one feature."),
  ("Slash-style command", "A message starting with a slash that the bot parses itself."),
  ("History", "The list of earlier messages sent to a language model as context."),
  ("Word filter", "A rule that matches banned words in a message."),
  ("OPENAI_API_KEY", "The environment variable the AI example expects for its model endpoint.")],
 ["cargo run -p vector-sdk --example echo_bot with VECTOR_NSEC set.",
  "slash_command_bot: /ping, /echo, /roll, /help.",
  "ai_bot needs OPENAI_API_KEY and keeps per-chat history.",
  "moderation_bot: welcome on MemberJoin, ban on filtered words.",
  "Run examples with a throwaway identity first."],
 [T("The best way to learn an SDK is to run its smallest program. The echo bot receives a message and sends the same text back. It touches the whole path: identity, connection, event, reply."),
  C("# in a shell (names as reported in the examples page)\nexport VECTOR_NSEC='nsec1...'   # use a throwaway identity\ncargo run -p vector-sdk --example echo_bot", "bash"),
  T("The command bot adds parsing: split the text at the first space, look at the command word, and act. The documented set is ping, echo, roll and help, and anything else gets the help text."),
  T("The AI bot is the largest example. For each incoming message it shows typing, sends the conversation so far to an OpenAI-compatible endpoint, and replies. Keep the history short, because long histories cost money and slow replies."),
  T("The moderation bot shows why handlers need care. A filter that bans on a single word will punish innocent people; a careful bot warns first, logs the reason without the message text, and leaves final decisions to admins."),
  T("Before pointing any example at a real community, run it in a private test chat with a throwaway key, and read its source so you know exactly what it will do with the permissions you give it.")],
 [("Which variable do all examples need?", ["VECTOR_NSEC", "HOME", "PATH", "RUST_LOG only"], 0, "Identity."),
  ("How is an example started?", ["cargo run -p vector-sdk --example name", "python run.py", "npm start", "make"], 0, "Cargo."),
  ("What does ai_bot call?", ["An OpenAI-compatible endpoint", "A local file", "Nothing", "A relay"], 0, "Needs OPENAI_API_KEY."),
  ("What does moderation_bot do on MemberJoin?", ["Sends a welcome", "Bans", "Leaves", "Dissolves"], 0, "Greeting."),
  ("Safest way to try an example?", ["Throwaway identity, private chat", "Production key, big community", "No key", "Public key only"], 0, "Test first."),
  ("What does an unknown command get?", ["The help text", "A ban", "Nothing", "A crash"], 0, "Friendly fallback.")],
 [("echo_bot", "Repeats incoming text"), ("file_bot", "Uses Channel::send_file"), ("save_files_bot", "Stores received files"), ("RUST_LOG", "Controls log verbosity")],
 [MATCH("Match the example", "Pair each example with its job.", [("echo_bot", "repeat text"), ("slash_command_bot", "ping echo roll help"), ("moderation_bot", "welcome and filter"), ("file_bot", "send a file")]),
  FILL("Examples", "Examples need the {{VECTOR_NSEC}} variable. The AI example needs {{OPENAI_API_KEY}}. Start one with cargo {{run}} -p vector-sdk --example name."),
  PL("Command handler", "Write command(text): '/ping' gives 'pong'; '/echo something' gives 'something'; '/help' gives 'commands: /ping /echo /roll /help'; anything else gives the same help text.", "command(text)", '''
def command(text):
    help_text = 'commands: /ping /echo /roll /help'
    if text == '/ping':
        return 'pong'
    if text.startswith('/echo '):
        return text[6:]
    return help_text
''', [['/ping'], ['/echo hello there'], ['/help'], ['hi'], ['/echo']], "Split on the first space."),
  PL("Parse a roll", "Write parse_roll(text): text is like '/roll 2d6'. Return [count, sides] as integers, or [0, 0] if it is not in that form. Count and sides must be at least 1.", "parse_roll(text)", '''
def parse_roll(text):
    if not text.startswith('/roll '):
        return [0, 0]
    body = text[6:]
    if 'd' not in body:
        return [0, 0]
    a, b = body.split('d', 1)
    if a == '' or b == '':
        return [0, 0]
    for ch in a + b:
        if ch not in '0123456789':
            return [0, 0]
    n = int(a)
    s = int(b)
    if n < 1 or s < 1:
        return [0, 0]
    return [n, s]
''', [['/roll 2d6'], ['/roll d6'], ['/roll 0d6'], ['roll 2d6'], ['/roll 1d20']], "Split at d."),
  PL("Welcome message", "Write welcome(name, community): return 'Welcome, ' + name + ', to ' + community + '!'", "welcome(name, community)", '''
def welcome(name, community):
    return 'Welcome, ' + name + ', to ' + community + '!'
''', [['Ana', 'Rust Club'], ['Bo', 'Vector']], "String joining."),
  PL("Word filter", "Write flagged(message, banned): True when any banned word appears as a whole word in the message (compare lower case, split on spaces).", "flagged(message, banned)", '''
def flagged(message, banned):
    words = message.lower().split(' ')
    for b in banned:
        if b.lower() in words:
            return True
    return False
''', [['this is spam', ['spam']], ['spammy words', ['spam']], ['Hello', ['x']], ['BUY now', ['buy']]], "Whole words only."),
  PL("Trim history", "Write trim(history, max_items): keep only the last max_items entries of the list, in order.", "trim(history, max_items)", '''
def trim(history, max_items):
    if max_items <= 0:
        return []
    if len(history) <= max_items:
        return history
    return history[len(history) - max_items:]
''', [[['a', 'b', 'c'], 2], [['a'], 5], [['a', 'b'], 0]], "Keep the tail.")]))


CHS.append(CH(
 "Troubleshooting, tracing and deployment",
 ("Operations", [
  "Not connected | means | build not finished",
  "RUST_LOG | enables | Debug logs",
  "No events | means | Process not alive",
  "send_file | uses | Working directory",
  "Bunker signer | cannot do | Concord rekeys",
  "Backoff | spaces | Reconnects",
  "Supervisor | restarts | The bot"]),
 ["Most problems fall into a few families. A not connected or not logged in error means you used the bot before build finished. A DM send failure usually means no reachable inbox relays. A stale id means run sync_communities.",
  "If on_message never fires, keep the process alive and message the printed npub from another account. If kick or ban fails, check capabilities. If send_file cannot find a file, check the working directory. Turn on debug logging with RUST_LOG=vector_sdk=debug.",
  "In production run the bot under a supervisor, keep secrets out of logs, and monitor reconnect storms."],
 [("RUST_LOG", "An environment variable that sets the log level for Rust crates."),
  ("Supervisor", "A tool such as systemd that restarts a crashed process."),
  ("Bunker signer", "A remote NIP-46 signer; the docs say it cannot perform Concord rekeys."),
  ("Reconnect storm", "Many rapid reconnect attempts, often from a bad network or key."),
  ("Health check", "A small test that shows the bot is alive and can send.")],
 ["Await build() before any other call.",
  "No events? Keep the process alive and message the printed npub.",
  "RUST_LOG=vector_sdk=debug for detail.",
  "Check capabilities before moderation; run sync_communities for stale ids.",
  "Supervise, log without secrets, back off on retries."],
 [T("When something fails, work from the cheapest check to the dearest. First, is the process running and did build finish? Second, is the key right? Third, can the target be reached? Only then read deeper logs."),
  C("# turn on debug output (name as given in the troubleshooting page)\nRUST_LOG=vector_sdk=debug cargo run -p vector-sdk --example echo_bot", "bash"),
  T("A classic mistake is registering a handler and then letting main return. The program ends, the connection closes and nothing is ever delivered. Wait on a signal or a channel so the process stays alive."),
  T("A second classic is a relative path. A service started by systemd runs from another folder than your shell, so report.pdf is not where you thought. Use absolute paths in services."),
  T("For retries use exponential backoff with a cap and some randomness, so a fleet of bots does not stampede a relay after an outage. Treat authentication errors differently from network errors: do not retry a bad key."),
  T("Deploy under systemd or a container with a restart policy. Give each bot its own data directory, protect the directory with file permissions, and keep a runbook: how to rotate the key, how to read logs, and who to tell.")],
 [("Error: not connected. Likely cause?", ["Used the bot before build finished", "Wrong Rust", "Bad emoji", "Large file"], 0, "Await build."),
  ("on_message never fires. First check?", ["Process stays alive", "Change the language", "Delete data dir", "Buy a relay"], 0, "Keep running."),
  ("How do you enable debug logs?", ["RUST_LOG=vector_sdk=debug", "--loud", "DEBUG=1 only", "Edit the key"], 0, "Env var."),
  ("send_file fails on a relative path. Why?", ["Resolved against the working directory", "Files must be tiny", "Relays block it", "Wrong npub"], 0, "Use absolute paths."),
  ("Stale community id?", ["sync_communities()", "Rotate key", "Restart tor", "Rewrite handler"], 0, "Refresh."),
  ("Should a bad key be retried forever?", ["No, treat it as fatal", "Yes", "Only at night", "Only in Tor"], 0, "Auth errors differ.")],
 [("Health check", "Confirms the bot can send"), ("systemd", "Linux supervisor"), ("Jitter", "Randomness added to a backoff delay"), ("Runbook", "Written steps for operating a service")],
 [MATCH("Match the symptom", "Pair each symptom with the first check.", [("not logged in", "await build"), ("no events", "process alive"), ("kick fails", "capabilities"), ("file not found", "working directory")]),
  FILL("Operations", "Use {{RUST_LOG}} to see debug output. Run a bot under a {{supervisor}} such as systemd. Retry with {{backoff}}, and never retry a bad {{key}} forever."),
  ORDER("Diagnose", "Put the checks in a sensible order.", ["Is the process running?", "Did build() finish?", "Is the key correct?", "Is the target reachable?", "Read debug logs"]),
  PL("Backoff with cap", "Write waits(n, base, cap): return the first n retry waits; the first is base, each next doubles, never above cap.", "waits(n, base, cap)", '''
def waits(n, base, cap):
    out = []
    w = base
    for i in range(n):
        out.append(min(w, cap))
        w = w * 2
    return out
''', [[5, 1, 10], [3, 2, 100], [0, 1, 1]], "Double and clamp."),
  PL("Retry or stop", "Write retry_decision(error): 'network' and 'timeout' give 'retry'; 'auth' and 'invalid_key' give 'stop'; 'no_relays' gives 'tell person'; anything else gives 'log'.", "retry_decision(error)", '''
def retry_decision(error):
    if error in ('network', 'timeout'):
        return 'retry'
    if error in ('auth', 'invalid_key'):
        return 'stop'
    if error == 'no_relays':
        return 'tell person'
    return 'log'
''', [['network'], ['auth'], ['no_relays'], ['weird']], "Different errors, different actions."),
  PL("Diagnose", "Write diagnose(symptom): 'not connected' or 'not logged in' gives 'await build'; 'no events' gives 'keep process alive'; 'dm failed' gives 'check inbox relays'; 'kick failed' gives 'check capabilities'; 'file missing' gives 'check working directory'; anything else gives 'enable debug logs'.", "diagnose(symptom)", '''
def diagnose(symptom):
    if symptom in ('not connected', 'not logged in'):
        return 'await build'
    if symptom == 'no events':
        return 'keep process alive'
    if symptom == 'dm failed':
        return 'check inbox relays'
    if symptom == 'kick failed':
        return 'check capabilities'
    if symptom == 'file missing':
        return 'check working directory'
    return 'enable debug logs'
''', [['not connected'], ['no events'], ['dm failed'], ['kick failed'], ['file missing'], ['strange']], "A lookup."),
  PL("Reconnect storm", "Write storm(times, window, limit): times is a sorted list of reconnect attempt times in seconds. Return True if more than limit attempts fall inside any window of the given length (counting from an attempt time, inclusive of start, exclusive of end).", "storm(times, window, limit)", '''
def storm(times, window, limit):
    for i in range(len(times)):
        c = 0
        for t in times:
            if t >= times[i] and t < times[i] + window:
                c += 1
        if c > limit:
            return True
    return False
''', [[[0, 1, 2, 3, 4, 5], 10, 3], [[0, 20, 40], 10, 1], [[], 10, 0], [[5, 5, 5], 1, 2]], "Slide a window.")]))
