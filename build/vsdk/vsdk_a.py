# -*- coding: utf-8 -*-
"""Vector SDK course, part 1: overview, identity, channels, events."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "What the Vector SDK is, and which version to trust",
 ("Vector SDK", [
  "Vector SDK | builds | Bots",
  "Vector | is | Private messenger",
  "Bot | has | One identity",
  "vector-core | provides | Crypto and storage",
  "nostr-sdk | provides | Relay transport",
  "Docs 0.3.0 | differ from | Repo 0.2.1",
  "Rust | is | The SDK language"]),
 ["The Vector SDK is a Rust library for building bots that talk over Vector, a privacy-focused messenger built on the Nostr protocol. A bot gets its own identity, can message people and communities, and reacts to events.",
  "This course follows the public GitBook documentation, which describes SDK version 0.3.0 and says it targets Vector 0.4.0 and later. All statements are as reported in that documentation in November 2026.",
  "The GitHub repository VectorPrivacy/Vector-SDK was found at crate version 0.2.1 on its main branch, with an older API built around VectorBot::quick. Always check which version you depend on before copying code."],
 [("Vector", "A private messenger built on Nostr, with end-to-end encrypted direct messages and communities."),
  ("Nostr", "An open protocol where clients talk to relays using signed events and public keys."),
  ("Relay", "A server that stores and forwards Nostr events."),
  ("npub", "A bech32 encoded public key starting with npub1; the address of a user or bot."),
  ("nsec", "A bech32 encoded private key starting with nsec1; keep it secret.")],
 ["Rust library, tokio runtime, builder API in the 0.3.0 docs.",
  "The docs say 0.3.0 targets Vector 0.4.0 and later.",
  "The repo main branch showed 0.2.1: verify versions before copying code.",
  "A bot has exactly one identity per process.",
  "Treat anything here as reported, not guaranteed."],
 [T("A messenger needs three things: a way to prove who you are, a way to send messages privately, and a way to hear about new messages. The Vector SDK gives a bot all three, so a program can take part in chats like a person would."),
  T("Under the hood it uses a crate called vector-core for encryption, networking and storage, and the nostr-sdk crate to talk to relays. It runs on tokio, Rust's asynchronous runtime, so event handlers do not block each other."),
  T("Be careful with versions. The hosted documentation presents a builder API, VectorBot::builder, and says it is version 0.3.0. The GitHub main branch we inspected still reported 0.2.1 and used a shorter VectorBot::quick entry point. Code written for one may not compile with the other."),
  C("// Cargo.toml (version as the 0.3.0 docs describe it; check crates.io or the repo for the real one)\n[dependencies]\nvector-sdk = \"0.3\"\ntokio = { version = \"1\", features = [\"full\"] }", "toml"),
  T("The honest way to use any SDK is to pin an exact version, read the examples that match it, and run a small echo bot before building anything large. This course marks which API belongs to which documented version."),
  T("Everything here is about the SDK, not the Vector app itself. The documentation also covers the Concord Protocol and the messenger's own features, which this course leaves out.")],
 [("What language is the SDK written in?", ["Rust", "Python", "Go", "C#"], 0, "Cargo crate."),
  ("What does a Vector bot's address look like?", ["An npub1 key", "An email", "A phone number", "A URL"], 0, "Bech32 public key."),
  ("What does vector-core provide?", ["Encryption, networking and storage", "The UI", "Billing", "Maps"], 0, "The engine."),
  ("Which two version numbers differed?", ["Docs 0.3.0 and repo main 0.2.1", "1.0 and 2.0", "Python 2 and 3", "None"], 0, "Check before copying."),
  ("Which runtime does it use?", ["tokio", "asyncio", "node", "rayon only"], 0, "Async Rust."),
  ("What is a relay?", ["A server that stores and forwards events", "A router", "A key", "A bot"], 0, "Nostr.")],
 [("npub", "Public key address"), ("nsec", "Private key, secret"), ("tokio", "Rust async runtime"), ("Version pinning", "Fix an exact dependency version")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("npub", "public address"), ("nsec", "private key"), ("relay", "stores and forwards events"), ("vector-core", "crypto, network, storage")]),
  FILL("Overview", "The SDK is written in {{Rust}}. A bot's public address starts with {{npub1}}. Its private key must be kept {{secret}}. Servers that forward events are called {{relays}}."),
  PL("Which API?", "Write api_style(version): versions are strings like '0.2.1' or '0.3.0'. Return 'quick' for a minor version below 3, otherwise 'builder'.", "api_style(version)", '''
def api_style(version):
    parts = version.split('.')
    minor = int(parts[1])
    if minor < 3:
        return 'quick'
    return 'builder'
''', [['0.2.1'], ['0.3.0'], ['0.4.2'], ['0.1.0']], "Look at the middle number."),
  PL("Key kind", "Write key_kind(key): return 'public' if the text starts with 'npub1', 'secret' if it starts with 'nsec1', otherwise 'unknown'.", "key_kind(key)", '''
def key_kind(key):
    if key.startswith('npub1'):
        return 'public'
    if key.startswith('nsec1'):
        return 'secret'
    return 'unknown'
''', [['npub1abc'], ['nsec1xyz'], ['hello'], ['']], "Prefix test."),
  PL("Safe to log?", "Write safe_to_log(text): return False if the text contains 'nsec1' anywhere, otherwise True.", "safe_to_log(text)", '''
def safe_to_log(text):
    return 'nsec1' not in text
''', [['bot started'], ['key=nsec1qq'], ['npub1abc online'], ['']], "Never log secrets."),
  PL("Compatible?", "Write compatible(sdk_minor, vector_version): the docs say SDK 0.3 targets Vector 0.4.0 and later. vector_version is like '0.4.1'. Return True when sdk_minor is 3 or more and the Vector minor number is 4 or more (major 0).", "compatible(sdk_minor, vector_version)", '''
def compatible(sdk_minor, vector_version):
    parts = vector_version.split('.')
    major = int(parts[0])
    minor = int(parts[1])
    if sdk_minor < 3:
        return False
    return major > 0 or minor >= 4
''', [[3, '0.4.0'], [3, '0.3.9'], [2, '0.5.0'], [3, '1.0.0']], "Two conditions.")]))


CHS.append(CH(
 "Identity and keys: building a bot",
 ("Identity", [
  "Builder | creates | VectorBot",
  "nsec | gives | Identity",
  "mnemonic | derives | Keys",
  "Keyless bot | saves | identity.nsec",
  "data_dir | holds | Bot state",
  "One identity | per | Process",
  "npub | is shown by | bot.npub()"]),
 ["In the documented builder API you start with VectorBot::builder(), choose how the bot gets its keys, optionally set a data directory, and call build, which connects and returns the bot.",
  "Keys can come from an nsec, from a mnemonic phrase, or from nothing. A keyless bot generates a key, saves it as identity.nsec in its data directory, and reuses it next time. Keys you pass in explicitly stay in memory only.",
  "A process has one bot identity. To run more than one keyless bot on the same machine, give each its own data directory."],
 [("Builder", "A configuration object that collects options before build creates the bot."),
  ("Mnemonic", "A list of words from which keys can be derived."),
  ("Keyless bot", "A bot built without supplied keys; it generates and persists its own."),
  ("Data directory", "The folder where the bot stores its state and, for keyless bots, identity.nsec."),
  ("Environment variable", "A setting such as VECTOR_NSEC used by the examples to pass the key.")],
 ["VectorBot::builder()...build().await? creates and connects.",
  "Use .nsec(), .mnemonic() or leave keys out.",
  "Keyless bots save identity.nsec in the data directory.",
  "More than one keyless bot needs separate .data_dir() values.",
  "bot.npub() gives the public address to share."],
 [T("Think of a bot as a new employee who needs a badge. The nsec is the badge's secret code, and the npub is the name on the badge that other people see. Whoever knows the secret code can act as the bot, so it must stay private."),
  C("// as described in the 0.3.0 documentation\nuse vector_sdk::VectorBot;\n\n#[tokio::main]\nasync fn main() -> Result<(), Box<dyn std::error::Error>> {\n    let nsec = std::env::var(\"VECTOR_NSEC\")?;\n    let bot = VectorBot::builder()\n        .nsec(&nsec)\n        .build()\n        .await?;\n    println!(\"My address: {}\", bot.npub());\n    Ok(())\n}", "rust"),
  T("The build call is where the bot logs in, connects to relays and syncs. Many errors such as not connected or not logged in appear when you use the bot before build has finished, so always await it first."),
  T("Without keys, the bot creates a fresh identity the first time. It writes the secret to identity.nsec in the data directory and loads it on later runs, so its address stays the same. Keys you pass explicitly are never written to disk by the SDK."),
  T("If you start two keyless bots from the same directory they would share one identity file, which is a mistake. Give each bot its own data_dir. And never commit identity.nsec or print an nsec to a log."),
  T("Read the nsec from an environment variable, as the documented examples do with VECTOR_NSEC, rather than from a source file. Rotate it by creating a new identity if you suspect it leaked, and tell your contacts the new npub.")],
 [("Where is a keyless bot's key stored?", ["identity.nsec in its data directory", "In the cloud", "Nowhere", "In the npub"], 0, "Reused on restart."),
  ("When are explicit keys written to disk?", ["Never, they stay in memory", "Always", "On exit", "To the relay"], 0, "Memory only."),
  ("What do two keyless bots on one machine need?", ["Different data directories", "The same nsec", "No setup", "Two processes with one key"], 0, "Separate identity files."),
  ("What does build().await? do?", ["Connects and returns the bot", "Deletes keys", "Sends a message", "Compiles Rust"], 0, "Setup."),
  ("How do examples pass the key?", ["VECTOR_NSEC environment variable", "Hardcoded", "In the URL", "By email"], 0, "No secrets in code."),
  ("Which is safe to share?", ["npub", "nsec", "identity.nsec", "mnemonic"], 0, "Public key.")],
 [("bot.npub()", "Returns the public address"), ("identity.nsec", "Saved secret of a keyless bot"), ("VECTOR_NSEC", "Env variable used by examples"), (".data_dir()", "Choose where state is stored")],
 [APP("POLICY", "Invite policy lab", "Try the three invite policies and see which invitations a bot accepts."),
  MATCH("Match the key source", "Pair each setup with what happens.", [("nsec supplied", "key stays in memory"), ("no keys", "identity.nsec is saved and reused"), ("two keyless bots", "need separate data directories"), ("mnemonic", "keys are derived from words")]),
  FILL("Identity", "A bot built with no keys is {{keyless}}. It saves {{identity.nsec}} in its data {{directory}}. Only the {{npub}} should be shared."),
  PL("Bech32-looking npub", "Write npub_ok(s): True when s starts with 'npub1', has exactly 63 characters, and every character after 'npub1' is in the bech32 set 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'. (This checks the shape only, not the checksum.)", "npub_ok(s)", '''
def npub_ok(s):
    if not s.startswith('npub1'):
        return False
    if len(s) != 63:
        return False
    chars = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    for ch in s[5:]:
        if ch not in chars:
            return False
    return True
''', [['npub1' + 'q' * 58], ['npub1' + 'q' * 57], ['npub1' + 'b' * 58], ['nsec1' + 'q' * 58], ['npub1' + 'qpzry9x8gf2tvdw0s3jn54khce6mua7l' + 'q' * 26]], "Length 63."),
  PL("Where does the key come from?", "Write key_source(nsec, mnemonic, has_saved_file): return 'nsec' if nsec is non-empty, else 'mnemonic' if mnemonic is non-empty, else 'saved' if has_saved_file, else 'generate'.", "key_source(nsec, mnemonic, has_saved_file)", '''
def key_source(nsec, mnemonic, has_saved_file):
    if nsec != '':
        return 'nsec'
    if mnemonic != '':
        return 'mnemonic'
    if has_saved_file:
        return 'saved'
    return 'generate'
''', [['k', '', False], ['', 'w w w', True], ['', '', True], ['', '', False]], "Priority order."),
  PL("Written to disk?", "Write persists(source): True only when the key source is 'generate' (a new keyless identity is saved); False for 'nsec', 'mnemonic' and 'saved'.", "persists(source)", '''
def persists(source):
    return source == 'generate'
''', [['generate'], ['nsec'], ['saved'], ['mnemonic']], "Explicit keys stay in memory."),
  PL("Data dir clash", "Write clashes(dirs): dirs is a list of data directory names for keyless bots. Return the sorted list of directory names used more than once.", "clashes(dirs)", '''
def clashes(dirs):
    out = []
    for d in dirs:
        if dirs.count(d) > 1 and d not in out:
            out.append(d)
    out.sort()
    return out
''', [[['a', 'b', 'a']], [['x', 'y']], [[]], [['d', 'd', 'd']]], "Count duplicates.")]))


CHS.append(CH(
 "Channels, messages and replies",
 ("Messaging", [
  "bot.dm | opens | Channel",
  "Channel | sends | Text and files",
  "reply | links to | Message id",
  "edit | changes | Own message",
  "react | adds | Emoji",
  "typing | shows | 30 second hint",
  "send_file | uploads | Encrypted file"]),
 ["Messages go through a Channel. You get one for a direct message with bot.dm(npub), or from a chat or community with bot.channel(id), and then call methods on it.",
  "A channel can send text, reply to a specific message, edit or delete a message, add a reaction, show that the bot is typing, and send a file from disk.",
  "Typing indicators are short lived: the documentation describes them as expiring after 30 seconds, so a bot that is still working should send them again."],
 [("Channel", "A conversation the bot can send to: a direct message or a community chat."),
  ("Reply", "A message that points at an earlier message by its id."),
  ("Reaction", "An emoji attached to a message."),
  ("Typing indicator", "A temporary signal that the bot is composing a message."),
  ("Attachment", "A file sent with a message; it is encrypted before upload.")],
 ["bot.dm(npub) for direct messages; bot.channel(id) for others.",
  "send, reply, edit, delete, react, typing, send_file.",
  "Relative file paths resolve against the working directory.",
  "Typing hints expire after about 30 seconds.",
  "A DM send can fail if the person has no reachable inbox relays."],
 [T("A channel is a doorway to one conversation. Once the bot has the doorway it can speak, answer a particular earlier remark, fix a typo in its own message, or react with a thumbs up."),
  C("// sketch of the 0.3.0 documented methods\nlet chat = bot.dm(\"npub1...\").await?;\nlet sent = chat.send(\"Hello!\").await?;\nchat.reply(&sent_id, \"Replying to that\").await?;\nchat.react(&sent_id, \"👍\").await?;\nchat.typing().await?;\nchat.send_file(\"report.pdf\").await?;", "rust"),
  T("Replies and reactions need the id of the message they refer to. That id usually comes from an incoming message or from the result of a send, so keep it if you plan to edit or react later."),
  T("Files are encrypted before they are uploaded and a hash lets the receiver check integrity. A relative path such as report.pdf is resolved against the working directory of the process, so a service started from another folder may not find it."),
  T("Direct messages in Vector rely on the recipient's inbox relays. If the person has none that the bot can reach, the send fails with an error rather than going nowhere, and you should tell your user instead of retrying forever."),
  T("Never send private data to a channel without thinking about who is in it. In a community, everyone with access can read what the bot posts.")],
 [("How do you open a direct message?", ["bot.dm(npub)", "bot.run()", "bot.build()", "bot.sync()"], 0, "Returns a channel."),
  ("What does reply need?", ["The target message id", "A token", "A mnemonic", "A relay"], 0, "Reference."),
  ("How long does a typing hint last?", ["About 30 seconds", "Forever", "1 second", "1 hour"], 0, "Expires."),
  ("What resolves a relative send_file path?", ["The working directory", "The data dir always", "The relay", "The npub"], 0, "Check where you launch."),
  ("Why might a DM fail?", ["No reachable inbox relays", "Bad weather", "Too many emojis", "Wrong Rust version"], 0, "Delivery path."),
  ("Are files sent as plain bytes?", ["No, encrypted first", "Yes", "Only images", "Only small ones"], 0, "AES-256-GCM.")],
 [("react", "Add an emoji to a message"), ("edit", "Change a message you sent"), ("typing", "Show composing status"), ("send_file", "Upload and send a file")],
 [MATCH("Match the call", "Pair each need with the call.", [("answer a message", "reply"), ("fix a typo", "edit"), ("show activity", "typing"), ("share a PDF", "send_file")]),
  FILL("Messaging", "Open a direct chat with bot.{{dm}}(npub). Add an emoji with {{react}}. A typing hint expires after about {{30}} seconds. Files are {{encrypted}} before upload."),
  PL("Typing still showing?", "Write typing_active(sent_at, now): a typing hint lasts 30 seconds. True when now minus sent_at is less than 30.", "typing_active(sent_at, now)", '''
def typing_active(sent_at, now):
    return (now - sent_at) < 30
''', [[0, 10], [0, 30], [100, 129], [100, 131]], "Strictly less than 30."),
  PL("Keep typing alive", "Write typing_times(duration, refresh): while the bot works for duration seconds, it re-sends typing every refresh seconds starting at 0. Return the list of times at which a hint is sent (all times below duration).", "typing_times(duration, refresh)", '''
def typing_times(duration, refresh):
    out = []
    t = 0
    while t < duration:
        out.append(t)
        t += refresh
    return out
''', [[70, 25], [10, 25], [0, 25], [50, 10]], "Loop until duration."),
  PL("Resolve a path", "Write resolve(cwd, path): if path starts with '/', return it; otherwise join cwd and path with a single '/' between (no double slash).", "resolve(cwd, path)", '''
def resolve(cwd, path):
    if path.startswith('/'):
        return path
    if cwd.endswith('/'):
        return cwd + path
    return cwd + '/' + path
''', [['/srv/bot', 'report.pdf'], ['/srv/bot/', 'a/b.txt'], ['/srv', '/tmp/x.png']], "Absolute stays."),
  PL("Reply target", "Write reply_to(messages, text): messages is a list of [id, text]. Return the id of the first message whose text equals the given text, or 'none'.", "reply_to(messages, text)", '''
def reply_to(messages, text):
    for mid, t in messages:
        if t == text:
            return mid
    return 'none'
''', [[[['a1', 'hi'], ['a2', 'help']], 'help'], [[['a1', 'hi']], 'bye'], [[], 'x']], "Search by text."),
  PL("Message chunks", "Write chunks(text, size): split text into pieces of at most size characters and return the list. An empty text gives an empty list.", "chunks(text, size)", '''
def chunks(text, size):
    out = []
    i = 0
    while i < len(text):
        out.append(text[i:i + size])
        i += size
    return out
''', [['abcdefg', 3], ['', 5], ['abc', 3], ['abcd', 10]], "Step through the text.")]))


CHS.append(CH(
 "Events, handlers and incoming messages",
 ("Events", [
  "on_message | handles | IncomingMessage",
  "on_event | handles | BotEvent",
  "is_mine | filters | Own messages",
  "BotEvent | has | Eight variants",
  "Handlers | run | Independently",
  "Reconnect | catches up | Missed messages",
  "member() | gives | Sender"]),
 ["Bots are event driven. You register a handler with on_message for chat messages or on_event for the wider set of events. Handlers are asynchronous and run independently, so a slow one does not block the others.",
  "The documentation lists eight BotEvent variants: Message, MessageUpdate, Delete, MemberJoin, MemberLeave, Typing, Invite and Removed.",
  "An IncomingMessage gives you its text, whether it is yours, its channel, and in communities the community and member. Always skip messages the bot sent itself."],
 [("IncomingMessage", "The object passed to on_message: text, channel, sender and reply helpers."),
  ("BotEvent", "An enum of everything a bot can be told about."),
  ("is_mine", "A check that tells you the bot itself sent the message."),
  ("Catch-up", "Fetching messages that arrived while the bot was offline."),
  ("Dispatch", "Calling the right handler for each event.")],
 ["on_message(handler) for chat; on_event(handler) for all events.",
  "Eight variants: Message, MessageUpdate, Delete, MemberJoin, MemberLeave, Typing, Invite, Removed.",
  "Skip is_mine() messages to avoid loops.",
  "The bot reconnects automatically and catches up.",
  "Keep the process alive or no events will arrive."],
 [T("Imagine a switchboard operator. Calls arrive in any order, and each one is passed to the right desk. In the SDK, every incoming thing becomes an event, and your handlers are the desks."),
  C("// as described in the docs\nbot.on_message(|msg| async move {\n    if msg.is_mine() {\n        return;\n    }\n    let text = msg.text();\n    if text == \"ping\" {\n        let _ = msg.reply(\"pong\").await;\n    }\n}).await;", "rust"),
  T("This is the shape of the documented echo-style bot. The first check protects against loops; without it the bot would answer its own replies. After registering handlers, the main task must stay alive, for example by awaiting a signal, or the process exits and no events arrive."),
  T("on_event is for everything else. A MemberJoin lets a moderation bot greet newcomers, an Invite tells the bot it was asked to join a community, and Removed says it was taken out. Typing events are short lived signals you can usually ignore."),
  T("Because handlers run independently, do not rely on two events being processed in the order they arrived. If order matters, use ids and timestamps from the events, not the order of your code running."),
  T("If the connection drops, the SDK reconnects by itself and catches up on messages it missed, according to the docs. Your handlers should therefore be safe to run for messages that are a little old.")],
 [("How many BotEvent variants are documented?", ["Eight", "Two", "Twenty", "One"], 0, "Message through Removed."),
  ("Why check is_mine()?", ["Avoid answering itself", "Speed", "Encryption", "Billing"], 0, "Loops."),
  ("Do handlers block each other?", ["No, they run independently", "Yes, strictly in order", "Only on Linux", "Only in DMs"], 0, "Independent."),
  ("Which event tells the bot it was invited?", ["Invite", "Delete", "Typing", "Message"], 0, "Variant."),
  ("What if the process exits?", ["No events arrive", "Events queue forever", "Nothing changes", "Relays push anyway"], 0, "Keep it alive."),
  ("What happens after a disconnect?", ["Auto-reconnect and catch-up", "The bot is deleted", "Needs a manual restart", "Messages are lost"], 0, "As documented.")],
 [("on_event", "Receive any BotEvent"), ("MemberJoin", "Someone joined a community"), ("Removed", "The bot was removed from a community"), ("Typing", "A typing signal")],
 [APP("EVENTS", "Event router", "Send events through a bot and see which handler would run."),
  MATCH("Match the event", "Pair each situation with the BotEvent.", [("someone joined", "MemberJoin"), ("someone left", "MemberLeave"), ("bot invited", "Invite"), ("message removed", "Delete")]),
  FILL("Events", "Chat messages go to {{on_message}}. Other events go to {{on_event}}. Skip messages where {{is_mine}} is true. The SDK documents {{eight}} event variants."),
  PL("Route an event", "Write route(event): 'Message' and 'MessageUpdate' give 'chat'; 'MemberJoin' and 'MemberLeave' give 'members'; 'Invite' and 'Removed' give 'membership'; 'Delete' gives 'moderation'; 'Typing' gives 'ignore'; anything else gives 'unknown'.", "route(event)", '''
def route(event):
    if event in ('Message', 'MessageUpdate'):
        return 'chat'
    if event in ('MemberJoin', 'MemberLeave'):
        return 'members'
    if event in ('Invite', 'Removed'):
        return 'membership'
    if event == 'Delete':
        return 'moderation'
    if event == 'Typing':
        return 'ignore'
    return 'unknown'
''', [['Message'], ['MemberJoin'], ['Invite'], ['Delete'], ['Typing'], ['Foo']], "A lookup."),
  PL("Should the bot answer?", "Write answers(is_mine, text, trigger): False if is_mine; otherwise True when text equals the trigger ignoring case and surrounding spaces.", "answers(is_mine, text, trigger)", '''
def answers(is_mine, text, trigger):
    if is_mine:
        return False
    return text.strip().lower() == trigger.lower()
''', [[False, ' Ping ', 'ping'], [True, 'ping', 'ping'], [False, 'pong', 'ping']], "Own messages first."),
  PL("Catch up", "Write missed(seen_ids, server_ids): return the ids in server_ids that are not in seen_ids, keeping order.", "missed(seen_ids, server_ids)", '''
def missed(seen_ids, server_ids):
    out = []
    for i in server_ids:
        if i not in seen_ids:
            out.append(i)
    return out
''', [[[1, 2], [1, 2, 3, 4]], [[], [5]], [[7], [7]]], "Set difference in order."),
  PL("Count by kind", "Write count_events(events): return a sorted list of [name, count] pairs for the event names in the list.", "count_events(events)", '''
def count_events(events):
    names = []
    for e in events:
        if e not in names:
            names.append(e)
    names.sort()
    return [[n, events.count(n)] for n in names]
''', [[['Message', 'Typing', 'Message']], [[]], [['Invite']]], "Count each name.")]))
