# -*- coding: utf-8 -*-
"""Vector SDK course (vector_sdk 0.12.0), part 1: overview, accounts, sending, events, commands."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "What the Vector SDK is: crate 0.12.0 and its parts",
 ("Vector SDK 0.12.0", [
  "vector_sdk | builds | Bots and clients",
  "vector-core | provides | Engine",
  "nostr-sdk | provides | Relay transport",
  "tokio | runs | Async handlers",
  "Features | add | tor i2p voice whisper xdc",
  "MSRV | is | Rust 1.75",
  "Repository | is | VectorPrivacy/Vector"]),
 ["vector_sdk is a Rust crate for building bots and clients for Vector, a private encrypted messenger built on Nostr. Version 0.12.0 was published on 11 November 2026 under the MIT licence, and needs Rust 1.75 or newer.",
  "It sits on top of vector-core, which does the encryption, networking and storage. You write about a dozen lines to get a bot that sends and receives messages, files and reactions, joins communities, and survives network drops.",
  "Older write-ups are out of date. A GitBook page described version 0.3.0 and a standalone repository showed 0.2.1. This course follows the published 0.12.0 crate, its README, changelog and examples."],
 [("vector_sdk", "The Rust crate for building Vector bots; the crate name uses an underscore, the docs.rs name a hyphen."),
  ("vector-core", "The engine crate underneath: protocol, encryption, networking and storage. Version 0.11 is required by SDK 0.12."),
  ("Feature flag", "A Cargo option that compiles in an optional part: tor, i2p, voice, whisper or xdc."),
  ("MSRV", "Minimum supported Rust version; 1.75 for this crate."),
  ("Nostr", "An open protocol of signed events passed through relays.")],
 ["cargo add vector_sdk and cargo add tokio --features full.",
  "0.12.0 published 2026-11-11, MIT, MSRV 1.75, edition 2021.",
  "Features: tor, i2p, voice, whisper, xdc. None are on by default.",
  "Depends on vector-core 0.11, nostr-sdk 0.45, tokio 1.49.",
  "Repository: github.com/VectorPrivacy/Vector; docs: docs.rs/vector-sdk."],
 [T("A messenger bot needs three things: an identity, a way to send privately, and a way to hear what happens. The Vector SDK packages all three. You never touch the protocol or the encryption yourself; the crate does it for you."),
  C("# Cargo\ncargo add vector_sdk\ncargo add tokio --features full", "bash"),
  C("use vector_sdk::VectorBot;\n\n#[tokio::main]\nasync fn main() -> vector_sdk::Result<()> {\n    let bot = VectorBot::builder()\n        .nsec(\"nsec1...\")   // or omit it and a key is created for you\n        .build()\n        .await?;\n\n    println!(\"Online as {}\", bot.npub());\n\n    bot.on_message(|_bot, msg| async move {\n        if msg.is_mine() { return; }\n        let _ = msg.reply(&format!(\"You said: {}\", msg.text())).await;\n    }).await?;\n    Ok(())\n}", "rust"),
  T("This is the crate's own quick start. Notice that the handler receives the bot and the message, skips its own messages with is_mine, and replies. The same code works for direct messages and for community channels."),
  T("The crate has no optional parts switched on by default. The tor and i2p features route traffic through anonymity networks, voice and whisper let a bot join voice calls and transcribe speech, and xdc lets it take part in Mini Apps. Each adds dependencies, so enable only what you need."),
  T("Versions matter. The library is young and moves quickly, with minor releases adding large features. Pin an exact version in Cargo.toml, read the changelog before upgrading, and treat anything you read elsewhere as possibly out of date.")],
 [("What is the crate's current version in this course?", ["0.12.0", "0.3.0", "0.2.1", "1.0.0"], 0, "Published 2026-11-11."),
  ("Which crate does the real work underneath?", ["vector-core", "serde", "zip", "tempfile"], 0, "Engine."),
  ("What is the minimum Rust version?", ["1.75", "1.50", "1.90", "2021"], 0, "MSRV."),
  ("Which are optional features?", ["tor, i2p, voice, whisper, xdc", "http, ftp", "gpu, ui", "none"], 0, "Off by default."),
  ("What is the licence?", ["MIT", "GPL", "Proprietary", "Apache only"], 0, "Permissive."),
  ("Why pin the version?", ["The crate changes quickly", "Rust requires it", "To save disk", "Relays demand it"], 0, "Read the changelog.")],
 [("vector-core", "The engine crate"), ("tokio", "Async runtime"), ("Cargo feature", "Optional compiled part"), ("docs.rs", "Hosted API documentation")],
 [MATCH("Match the piece", "Pair each piece with its job.", [("vector_sdk", "ergonomic bot API"), ("vector-core", "crypto, network, storage"), ("tokio", "async runtime"), ("nostr-sdk", "relay transport")]),
  FILL("Overview", "The SDK is a {{Rust}} crate built on {{vector-core}}. Optional parts are switched on with Cargo {{features}}. It needs Rust {{1.75}} or newer."),
  PL("Feature to purpose", "Write purpose(feature): 'tor' gives 'anonymity'; 'i2p' gives 'anonymity'; 'voice' gives 'calls'; 'whisper' gives 'transcription'; 'xdc' gives 'mini apps'; anything else gives 'unknown'.", "purpose(feature)", '''
def purpose(feature):
    table = {'tor': 'anonymity', 'i2p': 'anonymity', 'voice': 'calls', 'whisper': 'transcription', 'xdc': 'mini apps'}
    return table.get(feature, 'unknown')
''', [['tor'], ['voice'], ['whisper'], ['xdc'], ['http']], "A lookup with a default."),
  PL("Whisper needs voice", "Write enabled(features): the whisper feature switches voice on too. Given a list of features, return the sorted list including voice whenever whisper is present, without duplicates.", "enabled(features)", '''
def enabled(features):
    out = []
    for f in features:
        if f not in out:
            out.append(f)
    if 'whisper' in out and 'voice' not in out:
        out.append('voice')
    out.sort()
    return out
''', [[['whisper']], [['tor', 'xdc']], [['voice', 'whisper']], [[]]], "Whisper implies voice."),
  PL("Meets MSRV?", "Write meets_msrv(rust_version): the crate needs Rust 1.75. rust_version is a string like '1.80.1'. Return True when it is at least 1.75.", "meets_msrv(rust_version)", '''
def meets_msrv(rust_version):
    parts = rust_version.split('.')
    major = int(parts[0])
    minor = int(parts[1])
    if major != 1:
        return major > 1
    return minor >= 75
''', [['1.75.0'], ['1.74.9'], ['1.80.1'], ['2.0.0']], "Compare the minor number."),
  PL("Newer release?", "Write newer(a, b): a and b are versions like '0.12.0'. Return True when a is a later version than b.", "newer(a, b)", '''
def newer(a, b):
    pa = [int(x) for x in a.split('.')]
    pb = [int(x) for x in b.split('.')]
    return pa > pb
''', [['0.12.0', '0.3.0'], ['0.3.0', '0.12.0'], ['0.12.0', '0.12.0'], ['1.0.0', '0.99.9']], "Compare as numbers, not text."),
  PL("Safe to log?", "Write safe_to_log(text): return False if the text contains 'nsec1' anywhere, otherwise True.", "safe_to_log(text)", '''
def safe_to_log(text):
    return 'nsec1' not in text
''', [['bot started'], ['key=nsec1qq'], ['npub1abc online']], "Never log secrets.")]))


CHS.append(CH(
 "Accounts and keys: identity, data directory, one bot per process",
 ("Accounts", [
  "No key | creates | Identity on first run",
  "nsec | is | An existing key",
  "mnemonic | is | Twelve word seed",
  "password | unlocks | Encrypted keys",
  "data_dir | holds | Identity and database",
  "One bot | per | Process",
  "generate_nsec | mints | A fresh key"]),
 ["There are four ways to give the bot an identity. Give no key and build creates one on first run and reuses it every run after. Give an nsec, a twelve word mnemonic, or a password for keys that are encrypted at rest. VectorBot::generate_nsec mints a fresh key yourself.",
  "A keyless bot's identity is stable across restarts, so it keeps its chats and community memberships. Storage defaults to a per-OS application directory. Override it with data_dir or the VECTOR_DATA_DIR variable.",
  "Every bot on a machine needs its own data directory, and a bot owns its process while it runs, so run one bot per process."],
 [("nsec", "A bech32 private key beginning nsec1; whoever has it is the bot."),
  ("npub", "The matching public key beginning npub1; safe to share."),
  ("Mnemonic", "A twelve word seed phrase from which the key is derived."),
  ("Data directory", "Where the bot stores its identity and database."),
  ("VECTOR_DATA_DIR", "An environment variable that sets the data directory.")],
 ["No key: created on first run, reused afterwards.",
  ".nsec(), .mnemonic(), .password(), VectorBot::generate_nsec().",
  ".data_dir(path) or VECTOR_DATA_DIR; one directory per bot.",
  "Run one bot per process; for more bots run more processes.",
  "A bot on Tor or I2P must name it again on every run."],
 [T("Think of the key as the bot's passport. The npub is the number everyone can read, and the nsec is the secret that proves it is really the bot. Anyone holding the nsec can act as the bot, so it must never appear in code, logs or screenshots."),
  C("let bot = VectorBot::builder()\n    .nsec(std::env::var(\"VECTOR_NSEC\")?)   // read from the environment\n    .data_dir(\"/var/lib/mybot\")\n    .build()\n    .await?;\nprintln!(\"{}\", bot.npub());", "rust"),
  T("Leaving the key out is perfect for a first bot. The first run creates an identity and stores it in the data directory, and every later run loads the same one. If you run several keyless bots on one machine, give each its own data directory, or they would share one identity."),
  T("A mnemonic is a twelve word seed phrase that can recreate the key. Treat it exactly like an nsec. The password option is only for keys that were saved encrypted."),
  T("A bot owns the process while it runs, so the rule is one bot per process. To run several bots, run several processes, each with its own data directory and key."),
  T("Read secrets from the environment, as the examples do with VECTOR_NSEC. If you suspect a key leaked, move the bot to a new identity and tell the people who use it the new npub.")],
 [("What happens with no key?", ["An identity is created and reused", "Build fails", "A shared key is used", "The bot is anonymous each run"], 0, "Stable identity."),
  ("How do several keyless bots coexist?", ["Each gets its own data directory", "They share one", "Impossible", "Use Tor"], 0, "Separate state."),
  ("How many bots per process?", ["One", "Two", "As many as you like", "Zero"], 0, "Per the README."),
  ("Which value is safe to share?", ["npub", "nsec", "mnemonic", "password"], 0, "Public key."),
  ("Where should the nsec come from?", ["An environment variable or secret store", "Source code", "A log line", "A README"], 0, "Not in code."),
  ("How do you set the data directory?", ["data_dir() or VECTOR_DATA_DIR", "bot.dir", "nsec", "feature flag"], 0, "Two ways.")],
 [("generate_nsec", "Create a new key"), (".password()", "For encrypted-at-rest keys"), ("One bot per process", "A rule from the README"), (".clearnet()", "Move back to direct connections")],
 [APP("POLICY", "Invite policy lab", "Preview the invite policies you will meet in a later chapter."),
  MATCH("Match the key source", "Pair each option with its meaning.", [("no key", "created and reused"), (".nsec()", "an existing key"), (".mnemonic()", "twelve word seed"), (".password()", "encrypted at rest")]),
  FILL("Identity", "With no key, build creates an identity on the first run and {{reuses}} it. Several keyless bots each need their own {{data_dir}}. Run one bot per {{process}}. Never share the {{nsec}}."),
  PL("Bech32-shaped npub", "Write npub_ok(s): True when s starts with 'npub1', has exactly 63 characters, and every character after 'npub1' is in the bech32 set 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'. (Shape only, not the checksum.)", "npub_ok(s)", '''
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
''', [['npub1' + 'q' * 58], ['npub1' + 'q' * 57], ['npub1' + 'b' * 58], ['nsec1' + 'q' * 58]], "Length 63."),
  PL("Where does the key come from?", "Write key_source(nsec, mnemonic, has_saved_identity): return 'nsec' if nsec is non-empty, else 'mnemonic' if mnemonic is non-empty, else 'saved' if has_saved_identity, else 'create'.", "key_source(nsec, mnemonic, has_saved_identity)", '''
def key_source(nsec, mnemonic, has_saved_identity):
    if nsec != '':
        return 'nsec'
    if mnemonic != '':
        return 'mnemonic'
    if has_saved_identity:
        return 'saved'
    return 'create'
''', [['k', '', False], ['', 'w w', True], ['', '', True], ['', '', False]], "Priority order."),
  PL("Mnemonic length", "Write mnemonic_ok(phrase): True when the phrase has exactly 12 words separated by single spaces.", "mnemonic_ok(phrase)", '''
def mnemonic_ok(phrase):
    words = phrase.split(' ')
    if len(words) != 12:
        return False
    for w in words:
        if w == '':
            return False
    return True
''', [['a b c d e f g h i j k l'], ['a b c'], ['a b c d e f g h i j k  l'], ['']], "Twelve words."),
  PL("Data directory clashes", "Write clashes(dirs): dirs is a list of data directory names, one per bot. Return the sorted list of directory names used more than once.", "clashes(dirs)", '''
def clashes(dirs):
    out = []
    for d in dirs:
        if dirs.count(d) > 1 and d not in out:
            out.append(d)
    out.sort()
    return out
''', [[['a', 'b', 'a']], [['x', 'y']], [[]], [['d', 'd', 'd']]], "Count duplicates."),
  PL("Pick the data dir", "Write data_dir(explicit, env_value, default): the explicit value wins if non-empty, then the env_value, then the default.", "data_dir(explicit, env_value, default)", '''
def data_dir(explicit, env_value, default):
    if explicit != '':
        return explicit
    if env_value != '':
        return env_value
    return default
''', [['/a', '/b', '/c'], ['', '/b', '/c'], ['', '', '/c']], "Priority order.")]))


CHS.append(CH(
 "Channels: one API for DMs and communities",
 ("Messaging", [
  "Channel | covers | DM and community",
  "bot.channel(id) | opens | A channel",
  "bot.dm(npub) | opens | A direct chat",
  "reply | threads to | A message",
  "post | sends with | PostOptions",
  "send_bytes | sends | From memory",
  "react_custom | uses | Emoji packs"]),
 ["You send through a Channel. A direct message chat and a community channel are handled identically, so you never branch on which one it is. Get one with bot.channel(id), bot.dm(npub), or msg.channel() on an incoming message.",
  "The channel methods cover send, reply, post with options, react and unreact, typing, edit, delete, send_file and send_bytes. Incoming messages also have reply and react shortcuts, and received files are in msg.message.attachments.",
  "channel.post takes PostOptions so a message can be a reply, can expire after a number of seconds, or can be addressed to one bot."],
 [("Channel", "A conversation you can send to: a DM or a community channel."),
  ("PostOptions", "Settings for post: reply_to, expires_in, to_bot and caption."),
  ("Attachment", "A file received with a message; fetch it with download_attachment or save_attachment."),
  ("Custom emoji", "A pack emoji written as :code: in any message the bot sends."),
  ("Typing indicator", "A short lived signal that the bot is composing.")],
 ["bot.channel(id).send(text) works for DMs and community channels.",
  "reply(msg_id, text) threads; post(text, PostOptions) adds expiry or addressing.",
  "send_file(path) from disk; send_bytes(bytes, name, opts) from memory.",
  "react, unreact, react_custom; edit and delete only your own messages.",
  "typing() shows the indicator."],
 [T("The big idea is that a Channel hides the difference between a private chat and a community room. Your code says send, reply or react, and the SDK works out the encryption and the relays."),
  C("msg.reply(\"got it\").await?;        // reply in the same chat or channel\nmsg.react(\"👍\").await?;            // react to it\nmsg.channel().typing().await?;     // show a typing indicator\n\n// or by id:\nbot.channel(id).send(\"hi\").await?;", "rust"),
  T("post is the general sender. With PostOptions you can reply to a message, set an expiry so the message disappears after a number of seconds, address a command to one particular bot, or attach a caption to a file that you send from memory with send_bytes."),
  C("use vector_sdk::PostOptions;\n\nchannel.post(\"Rules updated, see the pins\",\n    PostOptions::default().reply_to(msg_id).expires_in(3600)).await?;\n\nchannel.send_bytes(png_bytes, \"chart.png\",\n    PostOptions::default().caption(\"today\")).await?;", "rust"),
  T("Custom emoji work by equipping a pack with bot.subscribe_emoji_pack, then writing :code: in text. If two packs share a shortcode with different images, the SDK numbers them, such as :love~1: and :love~2:."),
  T("A bot can only edit and delete its own messages. To remove someone else's message in a community it needs moderation rights, covered later. Remember that everything the bot posts in a community is visible to everyone who can read that channel.")],
 [("Do DMs and community channels need separate code?", ["No, same Channel API", "Yes", "Only for files", "Only for replies"], 0, "One API."),
  ("How do you send a file from memory?", ["send_bytes", "send_file only", "post_file", "upload"], 0, "Bytes with a name."),
  ("What does expires_in do?", ["Makes the message expire after seconds", "Mutes the bot", "Deletes the channel", "Encrypts it"], 0, "PostOptions."),
  ("Which messages can the bot edit?", ["Its own", "Anyone's", "Admins only", "None"], 0, "Authors only."),
  ("How is a custom emoji written?", [":code:", "<code>", "#code", "emoji(code)"], 0, "Shortcode."),
  ("Where are received files?", ["msg.message.attachments", "msg.files()", "bot.inbox", "channel.disk"], 0, "Attachments.")],
 [("react_custom", "React with a pack emoji and image URL"), ("send_file", "Send a file from disk"), ("to_bot", "Address a message to one bot"), ("unreact", "Withdraw a reaction")],
 [MATCH("Match the call", "Pair each need with the call.", [("answer a message", "reply"), ("make a message expire", "post with expires_in"), ("send a chart from memory", "send_bytes"), ("show activity", "typing")]),
  FILL("Channels", "A Channel covers {{DMs}} and community channels. Use {{post}} with PostOptions for expiry. Send from memory with {{send_bytes}}. A bot can only {{edit}} its own messages."),
  PL("Expired?", "Write expired(sent_at, expires_in, now): all in seconds. True when the message has an expiry (expires_in > 0) and now is at least sent_at + expires_in.", "expired(sent_at, expires_in, now)", '''
def expired(sent_at, expires_in, now):
    if expires_in <= 0:
        return False
    return now >= sent_at + expires_in
''', [[0, 600, 599], [0, 600, 600], [0, 0, 9999], [100, 60, 200]], "Zero means no expiry."),
  PL("Resolve a path", "Write resolve(cwd, path): if path starts with '/', return it; otherwise join cwd and path with exactly one '/'.", "resolve(cwd, path)", '''
def resolve(cwd, path):
    if path.startswith('/'):
        return path
    if cwd.endswith('/'):
        return cwd + path
    return cwd + '/' + path
''', [['/srv/bot', 'report.pdf'], ['/srv/bot/', 'a/b.txt'], ['/srv', '/tmp/x.png']], "Relative paths follow the working directory."),
  PL("Shortcode clashes", "Write numbered(packs): packs is a list of [pack, code]. If a code appears in more than one pack, those entries become code~1, code~2 and so on in order of appearance. Return the list of final names in the original order.", "numbered(packs)", '''
def numbered(packs):
    counts = {}
    for p, c in packs:
        counts[c] = counts.get(c, 0) + 1
    seen = {}
    out = []
    for p, c in packs:
        if counts[c] > 1:
            seen[c] = seen.get(c, 0) + 1
            out.append(c + '~' + str(seen[c]))
        else:
            out.append(c)
    return out
''', [[[['a', 'love'], ['b', 'love'], ['a', 'wave']]], [[['a', 'x']]], [[]]], "Count first, then number."),
  PL("Reply target", "Write reply_to(messages, text): messages is a list of [id, text]. Return the id of the first message whose text equals the given text, or 'none'.", "reply_to(messages, text)", '''
def reply_to(messages, text):
    for mid, t in messages:
        if t == text:
            return mid
    return 'none'
''', [[[['a1', 'hi'], ['a2', 'help']], 'help'], [[['a1', 'hi']], 'bye'], [[], 'x']], "Search by text."),
  PL("Can edit?", "Write can_edit(author, bot_npub, deleted): True only when the author is the bot and the message is not deleted.", "can_edit(author, bot_npub, deleted)", '''
def can_edit(author, bot_npub, deleted):
    return author == bot_npub and not deleted
''', [['a', 'a', False], ['b', 'a', False], ['a', 'a', True]], "Own and alive.")]))


CHS.append(CH(
 "Receiving: handlers, BotEvent and history",
 ("Events", [
  "on_message | gets | Messages",
  "on_event | gets | BotEvent stream",
  "run | adds | Ctrl-C exit",
  "Ready | marks | Subscriptions live",
  "News | arrives | Once",
  "History | is read with | channel.history",
  "Cursor | pages | By position"]),
 ["bot.on_message handles every incoming chat message. bot.on_event gives the full BotEvent stream, and bot.run does the same but also exits cleanly on Ctrl-C. A slow handler will not hold up the others.",
  "BotEvent covers Ready, Message, Reaction, ReactionRemoved, Edit, Delete, MemberJoin, MemberLeave, Typing, CommunityChange, Dissolved, VoicePresence, Invite, Removed and more, each naming what changed and, where it applies, who did it.",
  "Everything sent since the bot began listening arrives once, live or through a catch-up. What came earlier is history. Read it on purpose with channel.history."],
 [("BotEvent", "The enum of everything the bot can be told about."),
  ("Ready", "Fires once per listen when the realtime subscriptions are registered."),
  ("CommunityChange", "One event per change to roles, channels, bans, timeouts, pins and more, naming who made it."),
  ("History", "Messages from before the bot began listening; read explicitly, never pushed as events."),
  ("Cursor", "A durable position (time and id) used to page through history.")],
 ["on_message for chat; on_event or run for everything.",
  "Skip msg.is_mine() to avoid reply loops.",
  "Ready fires even with zero communities.",
  "News arrives once; old messages are history, read with channel.history(n).",
  "The bot reconnects and catches up by itself."],
 [T("A bot is driven by events, like a switchboard. The SDK turns each thing that happens into a BotEvent, and your handler decides what to do. Handlers run independently, so one slow handler does not stall the others."),
  C("bot.on_event(|bot, event| async move {\n    match event {\n        BotEvent::Message(msg) if !msg.is_mine() => { msg.reply(\"hi\").await.ok(); }\n        BotEvent::MemberJoin { channel_id, .. } => {\n            bot.channel(channel_id).send(\"welcome!\").await.ok();\n        }\n        BotEvent::Delete { by, moderated: true, .. } => println!(\"mod removed a message: {by:?}\"),\n        _ => {}\n    }\n}).await?;", "rust"),
  T("The first arm skips the bot's own messages. The second welcomes someone who joined. The third notices when a moderator deleted a message, which a plain message handler would never see. The last arm ignores everything else, so adding new variants later does not break your code."),
  T("The SDK is careful about what counts as news. Anything sent after the bot began listening arrives exactly once, even if the bot was reconnecting. A relay replaying a month-old join does not greet anyone, and old messages pulled in by a sync never show up as Message events."),
  T("To read earlier messages, ask for them: channel.history(n) returns the newest n messages the bot holds locally, and history_before takes a Cursor to page further back. A Cursor is a time and an id, so it stays valid even if its message is later deleted."),
  T("Typing events carry an until time, the moment the indicator expires, so a bot can ignore stale ones. Keep the process alive after registering handlers: if main returns, the bot stops hearing anything.")],
 [("What does run add over on_event?", ["A clean Ctrl-C exit", "Encryption", "History", "Retries off"], 0, "Same stream."),
  ("Why check is_mine()?", ["Avoid answering itself", "Speed", "Billing", "Relays"], 0, "Loops."),
  ("When does Ready fire?", ["Once per listen when subscriptions register", "On every message", "On exit", "Never"], 0, "Even with 0 communities."),
  ("How do you read old messages?", ["channel.history(n)", "on_message replay", "bot.old()", "Ready"], 0, "Pull, not push."),
  ("What is a Cursor?", ["A durable position for paging", "A mouse pointer", "A key", "A relay"], 0, "Time and id."),
  ("What does a Typing event's until mean?", ["When the indicator expires", "Who typed", "Message id", "Relay name"], 0, "Unix seconds.")],
 [("Edit", "A message was edited by its author"), ("Dissolved", "A community was dissolved by its owner"), ("Removed", "The bot was removed from a community"), ("history_before", "Page further back with a Cursor")],
 [APP("EVENTS", "Event router", "Send BotEvents through a bot and see which handler would act."),
  MATCH("Match the event", "Pair each situation with the BotEvent.", [("someone joined", "MemberJoin"), ("moderator removed a message", "Delete with moderated"), ("bot was kicked", "Removed"), ("roles changed", "CommunityChange")]),
  FILL("Events", "Chat messages reach {{on_message}}. The full stream is {{on_event}}. Skip messages where {{is_mine}} is true. Old messages are read with channel.{{history}}."),
  PL("Route an event", "Write route(event): 'Message' and 'Edit' give 'chat'; 'MemberJoin' and 'MemberLeave' give 'members'; 'Invite' and 'Removed' give 'membership'; 'Delete' gives 'moderation'; 'CommunityChange' gives 'audit'; 'Typing' gives 'ignore'; anything else gives 'unknown'.", "route(event)", '''
def route(event):
    if event in ('Message', 'Edit'):
        return 'chat'
    if event in ('MemberJoin', 'MemberLeave'):
        return 'members'
    if event in ('Invite', 'Removed'):
        return 'membership'
    if event == 'Delete':
        return 'moderation'
    if event == 'CommunityChange':
        return 'audit'
    if event == 'Typing':
        return 'ignore'
    return 'unknown'
''', [['Message'], ['MemberJoin'], ['Invite'], ['Delete'], ['CommunityChange'], ['Typing'], ['Foo']], "A lookup."),
  PL("Is it news?", "Write is_news(sent_at, listening_since, allowance): an event is news when it was sent at or after listening_since minus the allowance (all seconds).", "is_news(sent_at, listening_since, allowance)", '''
def is_news(sent_at, listening_since, allowance):
    return sent_at >= listening_since - allowance
''', [[100, 100, 0], [90, 100, 0], [90, 100, 300], [10, 1000, 300]], "Clock allowance."),
  PL("Typing still showing?", "Write typing_active(until, now): True when now is before the until time.", "typing_active(until, now)", '''
def typing_active(until, now):
    return now < until
''', [[130, 100], [100, 100], [50, 100]], "Strictly before."),
  PL("Page history", "Write page(history, limit): history is a list of message ids from oldest to newest. Return the newest limit ids, oldest first.", "page(history, limit)", '''
def page(history, limit):
    if limit <= 0:
        return []
    if len(history) <= limit:
        return history
    return history[len(history) - limit:]
''', [[['a', 'b', 'c', 'd'], 2], [['a'], 5], [['a', 'b'], 0]], "The tail of the list."),
  PL("Older than cursor", "Write before(history, cursor_id, limit): history is a list of ids oldest to newest. Return up to limit ids that come before cursor_id, newest of them last. If cursor_id is not found return [].", "before(history, cursor_id, limit)", '''
def before(history, cursor_id, limit):
    if cursor_id not in history:
        return []
    i = history.index(cursor_id)
    older = history[:i]
    if limit <= 0:
        return []
    if len(older) <= limit:
        return older
    return older[len(older) - limit:]
''', [[['a', 'b', 'c', 'd'], 'd', 2], [['a', 'b'], 'a', 5], [['a'], 'z', 1]], "Slice before the cursor.")]))


CHS.append(CH(
 "Slash commands with typed arguments",
 ("Commands", [
  "bot.command | declares | A command",
  "Manifest | is published | At listen start",
  "Picker | shows | Every client",
  "Typed args | arrive | Parsed",
  "Matched command | skips | on_message",
  "choice | becomes | A dropdown",
  "user | becomes | A member picker"]),
 ["Do not parse message text by hand. Declare a command with bot.command(name, description), add typed arguments, and give it a handler. The SDK publishes a manifest, so every Vector client shows a slash picker with a field per argument.",
  "Argument types are string, int, number, flag, user and choice. A choice becomes a dropdown, a user becomes a member picker, and an int becomes a number field. The client validates the input before it is sent.",
  "A matched command runs its handler and never reaches on_message, so commands and free chat can live side by side."],
 [("Manifest", "The published list of a bot's commands and their arguments."),
  ("CommandCtx", "The object a command handler receives, with typed getters and reply."),
  ("Choice argument", "An argument limited to a fixed list of options, shown as a dropdown."),
  ("Required", "Whether the user must supply the argument."),
  ("Consumed", "A matched command is handled by its own function and not passed on to message handlers.")],
 ["bot.command(name, description).string(...).choice(...).run(handler).",
  "Types: string, int, number, flag, user, choice.",
  "Read values with ctx.str, ctx.int, ctx.number, ctx.flag.",
  "Matched commands never reach on_message.",
  "The wire format is plain text like '/roll 20', so old clients can type it."],
 [T("Parsing chat text yourself is fragile: people mistype, add spaces, and forget options. Declared commands move that work into the client, which draws a form and checks it, so your handler only ever sees well-formed values."),
  C("bot.command(\"weather\", \"Current conditions for a city\")\n    .string(\"city\", \"Which city\", true)                       // required text\n    .choice(\"units\", \"Temperature units\", [\"c\", \"f\"], false)  // optional dropdown\n    .run(|ctx| async move {\n        let city = ctx.str(\"city\").unwrap_or_default();\n        let units = ctx.str(\"units\").unwrap_or(\"c\");\n        ctx.reply(format!(\"Weather in {city} (°{})...\", units.to_uppercase())).await.ok();\n    });", "rust"),
  T("The third argument of each declaration says whether it is required. The choice call takes the list of allowed values, so a user cannot send an unit you do not handle. Read values off the context by name, and supply a default for optional ones."),
  T("The manifest is published automatically when the bot starts listening, and its order is the order you registered the commands, so the picker stays stable across restarts. There is a limit on the number of commands, and names must be unique."),
  T("On the wire a command is just message text such as slash roll 20, parsed against the manifest. That means any client, however old, can invoke a command by typing it, and your bot can still serve it."),
  T("Because matched commands are consumed, do not also expect them in on_message. Keep free-form chat handling there, and keep commands for actions with clear arguments.")],
 [("Which argument types exist?", ["string, int, number, flag, user, choice", "only string", "json, xml", "list, map"], 0, "Six."),
  ("What does a choice argument become?", ["A dropdown", "A text box", "A file picker", "A checkbox"], 0, "Client UI."),
  ("Does a matched command reach on_message?", ["No", "Yes", "Only in DMs", "Only for admins"], 0, "Consumed."),
  ("When is the manifest published?", ["When the bot starts listening", "At compile time", "Never", "On every message"], 0, "Automatic."),
  ("What order do commands appear in?", ["Registration order", "Alphabetical", "Random", "By use"], 0, "Deterministic."),
  ("Can an old client use the command?", ["Yes, by typing the text", "No", "Only with the feature", "Only on Tor"], 0, "Plain text on the wire.")],
 [("ctx.reply", "Answer from a command handler"), (".flag()", "A boolean argument"), (".user()", "An npub argument"), (".int()", "An integer argument")],
 [MATCH("Match the argument", "Pair each argument with how clients show it.", [("choice", "dropdown"), ("user", "member picker"), ("int", "number field"), ("flag", "toggle")]),
  FILL("Commands", "Declare a command with bot.{{command}}. A {{choice}} argument becomes a dropdown. Matched commands never reach {{on_message}}. Read text values with ctx.{{str}}."),
  PL("Parse a command", "Write parse(text): text like '/roll 20' or '/echo hello there'. Return [name, rest] where name excludes the slash and rest is the remaining text (empty if none). Return [] if text does not start with '/'.", "parse(text)", '''
def parse(text):
    if not text.startswith('/'):
        return []
    body = text[1:]
    if ' ' in body:
        i = body.index(' ')
        return [body[:i], body[i + 1:]]
    return [body, '']
''', [['/roll 20'], ['/echo hello there'], ['/help'], ['hello']], "Split at the first space."),
  PL("Validate a choice", "Write choice_ok(value, options): True when value is exactly one of options.", "choice_ok(value, options)", '''
def choice_ok(value, options):
    return value in options
''', [['c', ['c', 'f']], ['k', ['c', 'f']], ['', ['c']]], "Membership."),
  PL("Required arguments", "Write missing(spec, given): spec is a list of [name, required]; given is a list of names supplied. Return the sorted names that are required but not given.", "missing(spec, given)", '''
def missing(spec, given):
    out = []
    for name, required in spec:
        if required and name not in given:
            out.append(name)
    out.sort()
    return out
''', [[[['city', True], ['units', False]], []], [[['city', True]], ['city']], [[['b', True], ['a', True]], ['c']]], "Required and absent."),
  PL("Roll dice", "Write parse_roll(arg): arg like '2d6'. Return [count, sides] as integers, or [0, 0] if it is not digits d digits with both at least 1.", "parse_roll(arg)", '''
def parse_roll(arg):
    if 'd' not in arg:
        return [0, 0]
    a, b = arg.split('d', 1)
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
''', [['2d6'], ['d6'], ['0d6'], ['1d20'], ['abc']], "Split at d."),
  PL("Register commands", "Write register(names, max_commands): names is the list of command names in order. Return the list of results: 'ok' for a new name while under max_commands, 'duplicate' if the name is already registered, 'too many' if already at max_commands.", "register(names, max_commands)", '''
def register(names, max_commands):
    done = []
    out = []
    for n in names:
        if n in done:
            out.append('duplicate')
        elif len(done) >= max_commands:
            out.append('too many')
        else:
            done.append(n)
            out.append('ok')
    return out
''', [[['a', 'b', 'a', 'c'], 2], [['x'], 5], [[], 3]], "Check duplicates before the limit.")]))
