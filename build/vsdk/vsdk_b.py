# -*- coding: utf-8 -*-
"""Vector SDK course (vector_sdk 0.12.0), part 2: communities, running one, optional features, security."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Communities: joining, members and invites",
 ("Communities", [
  "Community | has | Members and channels",
  "InvitePolicy | decides | Invites",
  "Manual | is | Default",
  "Public | accepts | Anyone",
  "Whitelist | accepts | Listed npubs",
  "member() | gives | Sender",
  "bot.join | joins | By link"]),
 ["A community is a shared space with members, roles and channels. Your bot can join one by link with bot.join, preview a link first with bot.preview_link, or create its own with bot.create_community.",
  "Invites are handled by the invite policy on the builder. Manual is the default: invites wait for bot.pending_invites and bot.accept_invite. Public accepts from anyone. Whitelist accepts only listed npubs and ignores the rest. Auto-accept also picks up invites that arrived while the bot was offline.",
  "When a message arrives from a community, msg.member() gives the sender as a member you can act on: kick, ban, unban, grant or revoke admin, and check is_admin."],
 [("InvitePolicy", "Manual, Public or Whitelist; decides what happens to invitations."),
  ("Pending invite", "An invitation waiting for a manual decision."),
  ("Preview", "Reading a link's details before joining; says whether it was read from the community itself (verified)."),
  ("Member", "A person in a community, with actions such as kick and ban."),
  ("Whitelist", "Only these npubs may invite the bot; entries are bech32 npub1 values.")],
 ["Builder: .public() or .whitelist([...]); default is Manual.",
  "Manual: bot.pending_invites() then bot.accept_invite(id).",
  "bot.join(link), bot.preview_link(link), bot.create_community(name, NewCommunity).",
  "msg.member(): kick(), ban(), unban(), grant_admin(), revoke_admin(), is_admin().",
  "Auto-accept also joins invites that arrived while offline."],
 [T("Think of a clubhouse that sends your bot invitations. Manual means a person checks each one. Public means the bot joins any club that asks. Whitelist means it only joins clubs invited by people on its list, which keeps it from being spammed into random communities."),
  C("VectorBot::builder().nsec(key).public().build().await?;                    // accept from anyone\nVectorBot::builder().nsec(key).whitelist([\"npub1owner...\"]).build().await?;  // only these accounts\n\n// default: wait for you\nfor invite in bot.pending_invites().await? {\n    bot.accept_invite(&invite.id).await?;\n}", "rust"),
  T("With a whitelist, an invite from anyone else is ignored. The list must hold bech32 npub values, and the builder converts hex keys for you. A restarted bot still joins invites that arrived while it was down, in the automatic modes."),
  C("if let Some(member) = msg.member() {\n    member.kick().await?;          // or .ban() / .unban()\n    member.grant_admin().await?;   // or .revoke_admin()\n    if member.is_admin() { /* ... */ }\n}\nlet community = bot.community(community_id);\ncommunity.invite(\"npub1...\").await?;\nlet link = community.create_invite().await?;", "rust"),
  T("Moderation actions are checked the way every member's client would judge them. If the bot lacks the right, the call returns an error instead of publishing an edit that everyone would ignore, so handle the error rather than assuming success."),
  T("Racing bans compose: when many ban calls happen at once during a spam wave, they queue per community and drain into one change. For a whole wave, ban_many and unban_many batch the work into a single key rotation.")],
 [("What is the default invite policy?", ["Manual", "Public", "Whitelist", "Reject all"], 0, "A person decides."),
  ("What happens to an unlisted inviter under Whitelist?", ["Ignored", "Accepted", "Banned", "Replied to"], 0, "Not auto accepted."),
  ("Does auto-accept join invites received offline?", ["Yes", "No", "Only Public", "Only Manual"], 0, "Per the README."),
  ("What does preview_link tell you?", ["Whether details were read from the community itself", "The bot's key", "Member list", "Nothing"], 0, "verified."),
  ("What if the bot lacks the right to ban?", ["The call returns an error", "It succeeds silently", "The bot dissolves", "A retry loop"], 0, "Checked first."),
  ("What are ban_many and unban_many for?", ["Batching a wave into one rotation", "Banning forever", "Listing bans", "Logging"], 0, "Efficiency.")],
 [("pending_invites", "Invites waiting for a decision"), ("accept_invite", "Join from an invite"), ("create_invite", "Mint an invite link"), ("Dissolved", "A community sealed by its owner")],
 [APP("POLICY", "Invite policy lab", "Try each policy against different senders and see what the bot does."),
  MATCH("Match the policy", "Pair each policy with its behaviour.", [("Manual", "waits for accept_invite"), ("Public", "accepts anyone"), ("Whitelist, listed", "accepts"), ("Whitelist, unlisted", "ignored")]),
  FILL("Communities", "The default policy is {{Manual}}. A {{whitelist}} accepts only listed npubs. Join by link with bot.{{join}}. Check the sender with msg.{{member}}()."),
  PL("Invite decision", "Write decide(policy, sender, whitelist): policy is 'manual', 'public' or 'whitelist'. Return 'pending' for manual; 'accept' for public; for whitelist 'accept' when sender is listed, else 'ignore'.", "decide(policy, sender, whitelist)", '''
def decide(policy, sender, whitelist):
    if policy == 'manual':
        return 'pending'
    if policy == 'public':
        return 'accept'
    if sender in whitelist:
        return 'accept'
    return 'ignore'
''', [['public', 'x', []], ['manual', 'x', ['x']], ['whitelist', 'a', ['a', 'b']], ['whitelist', 'z', ['a']]], "Three policies."),
  PL("Startup invites", "Write startup(policy, offline_invites, whitelist): offline_invites is a list of sender names. 'public' accepts all, 'whitelist' accepts those listed, 'manual' none. Return the accepted senders in order.", "startup(policy, offline_invites, whitelist)", '''
def startup(policy, offline_invites, whitelist):
    out = []
    for s in offline_invites:
        if policy == 'public' or (policy == 'whitelist' and s in whitelist):
            out.append(s)
    return out
''', [['public', ['a', 'b'], []], ['whitelist', ['a', 'b'], ['b']], ['manual', ['a'], ['a']]], "Automatic modes only."),
  PL("Whitelist form", "Write whitelist_ok(entries): True when every entry starts with 'npub1' (hex keys are not accepted raw).", "whitelist_ok(entries)", '''
def whitelist_ok(entries):
    for e in entries:
        if not e.startswith('npub1'):
            return False
    return True
''', [[['npub1abc']], [['npub1a', 'ab12']], [[]]], "Bech32 only."),
  PL("Ban a wave", "Write rotations(bans): bans is a list of lists, each inner list the names banned at the same moment. Return how many key rotations are needed if each simultaneous group is batched into one.", "rotations(bans)", '''
def rotations(bans):
    n = 0
    for group in bans:
        if len(group) > 0:
            n += 1
    return n
''', [[[['a', 'b', 'c'], ['d']]], [[[]]], [[]]], "One per non-empty group."),
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
 "Running a community: roles, channels, permissions and policies",
 ("Management", [
  "Role | bundles | Permissions",
  "Category | groups | Channels",
  "Overwrite | adjusts | A channel",
  "Timeout | mutes | A member",
  "Audit log | records | Every action",
  "Policies | write | Rulebooks",
  "arm | ends | Dry run"]),
 ["From 0.12 a bot can do what a person with admin rights can do: create roles with permissions, make categories and channels, set per-channel overwrites, time members out, set nicknames, pin messages, and read a typed audit log.",
  "Each action is checked the way every member's client will judge it, so a refusal comes back as an error rather than an edit that everyone ignores.",
  "Moderation policies add rulebooks. community.policies() writes rules such as words, links, repetition, flooding or a joining cohort, previews them against real history, and acts only when armed."],
 [("Role", "A named set of permissions given to members; created with RoleSpec."),
  ("Permissions", "Bit flags such as KICK, BAN, MODERATE_MEMBERS, VIEW_CHANNEL and SEND_MESSAGES, combined with the | operator."),
  ("Overwrite", "A channel level rule that allows or denies permissions for a role or member."),
  ("Timeout", "A temporary silence applied to a member for a duration."),
  ("Armed", "A policy autopilot acts on verdicts only after arm; until then it is a dry run.")],
 ["RoleSpec::new(name).color(..).permissions(Permissions::KICK | ...).",
  "create_category, create_channel_with(NewChannel::default().private().in_category(id)).",
  "channel.set_overwrite(Overwrite::role(&role).allow(...)).",
  "member.timeout(duration), member.add_role(&role), msg.pin().",
  "Policies start in dry-run; only arm() lets them act, and never on less than proof."],
 [T("Running a community is mostly bookkeeping: who may do what, and where. Roles bundle permissions, categories group channels, and overwrites adjust the rules for one channel. The SDK exposes each as a typed call."),
  C("use vector_sdk::{NewChannel, Overwrite, Permissions, RoleSpec};\n\nlet mods = community.create_role(\n    RoleSpec::new(\"Mods\").color(0x59fcb3)\n        .permissions(Permissions::KICK | Permissions::MODERATE_MEMBERS).shown(),\n).await?;\nlet support = community.create_category(\"Support\").await?;\nlet tickets = community.create_channel_with(\"tickets\",\n    NewChannel::default().private().in_category(support.id())).await?;\ntickets.set_overwrite(Overwrite::role(&mods)\n    .allow(Permissions::VIEW_CHANNEL | Permissions::SEND_MESSAGES)).await?;\nmember.add_role(&mods).await?;\nmember.timeout(std::time::Duration::from_secs(600)).await?;", "rust"),
  T("Permissions are bit flags, so combining them uses the bitwise or operator and testing one uses a bitwise and. member.can and channel.permissions_of let a bot check what someone may do before it acts."),
  T("The audit log is typed. Each entry has an action, a target and an actor, so a bot can answer questions like who changed this role. BotEvent::CommunityChange pushes the same facts live, naming who made each change."),
  T("Policies are the careful way to moderate automatically. You write named rules, preview them against recent history, then enable them. A verdict says whether it can be proved from the record or is only inference, and a strong hunch lands in a queue for a human instead of triggering an action."),
  T("An autopilot starts as a dry run that only reports what it would do. Calling arm makes it act, and it still never removes anyone on less than proof. Keep a person in the loop for anything destructive, such as dissolving a community.")],
 [("How do you combine permissions?", ["With the | operator", "With +", "With a string", "You cannot"], 0, "Bit flags."),
  ("What does arm do?", ["Ends the dry run so a policy can act", "Bans everyone", "Creates a role", "Mutes the bot"], 0, "Explicit step."),
  ("Is a policy armed by default?", ["No, it starts in dry-run", "Yes", "Only for admins", "Only for Public bots"], 0, "Rehearse first."),
  ("What do you get from audit_log()?", ["Typed actions with target and actor", "Raw JSON only", "A file", "Nothing"], 0, "Typed."),
  ("What if the bot lacks a permission?", ["The call returns an error", "It is ignored by clients", "Silent success", "A panic"], 0, "Checked locally first."),
  ("What does a strong hunch become in a policy?", ["A human review item", "An automatic ban", "A deletion", "A role"], 0, "needs_human.")],
 [("RoleSpec", "Builder for a new role"), ("NewChannel", "Settings for a new channel: private, category, voice, forum"), ("Overwrite", "Per-channel allow or deny"), ("is_provable", "Whether a verdict survives replay")],
 [MATCH("Match the tool", "Pair each need with the tool.", [("group channels", "Category"), ("bundle permissions", "Role"), ("adjust one channel", "Overwrite"), ("silence a member for a while", "Timeout")]),
  FILL("Management", "Combine permissions with the bitwise {{or}} operator. A policy starts as a {{dry}} run until you call {{arm}}. The {{audit}} log records every action."),
  PL("Build a mask", "Write make_mask(names): bits are KICK 1, BAN 2, VIEW_CHANNEL 10, SEND_MESSAGES 11, MODERATE_MEMBERS 20 (these are teaching values, check the crate for real ones). Return the OR of 1 << bit for each known name; ignore unknown names.", "make_mask(names)", '''
def make_mask(names):
    bits = {'KICK': 1, 'BAN': 2, 'VIEW_CHANNEL': 10, 'SEND_MESSAGES': 11, 'MODERATE_MEMBERS': 20}
    m = 0
    for n in names:
        if n in bits:
            m = m | (1 << bits[n])
    return m
''', [[['KICK', 'MODERATE_MEMBERS']], [[]], [['VIEW_CHANNEL', 'SEND_MESSAGES', 'NOPE']]], "OR the bits."),
  PL("Has permission", "Write has_perm(mask, name) with the same teaching bits as the previous lab (KICK 1, BAN 2, VIEW_CHANNEL 10, SEND_MESSAGES 11, MODERATE_MEMBERS 20). True if that bit is set; False for an unknown name.", "has_perm(mask, name)", '''
def has_perm(mask, name):
    bits = {'KICK': 1, 'BAN': 2, 'VIEW_CHANNEL': 10, 'SEND_MESSAGES': 11, 'MODERATE_MEMBERS': 20}
    if name not in bits:
        return False
    return ((mask >> bits[name]) & 1) == 1
''', [[1 << 11, 'SEND_MESSAGES'], [1 << 11, 'BAN'], [0, 'KICK'], [3 << 10, 'VIEW_CHANNEL']], "Shift and mask."),
  PL("Channel overwrite", "Write effective(base, allow, deny): all are integer masks. The result is (base OR allow) AND NOT deny, using bitwise operations.", "effective(base, allow, deny)", '''
def effective(base, allow, deny):
    return (base | allow) & ~deny
''', [[3, 4, 1], [0, 6, 2], [7, 0, 0]], "Allow then deny."),
  PL("Timeout over?", "Write timed_out(until, now): True while now is before until.", "timed_out(until, now)", '''
def timed_out(until, now):
    return now < until
''', [[600, 100], [600, 600], [600, 900]], "Strictly before."),
  PL("Armed action", "Write act(armed, proof): returns 'dry run' when not armed; when armed returns 'act' if proof is True, otherwise 'needs human'.", "act(armed, proof)", '''
def act(armed, proof):
    if not armed:
        return 'dry run'
    if proof:
        return 'act'
    return 'needs human'
''', [[False, True], [True, True], [True, False], [False, False]], "Never act on less than proof."),
  PL("Flood rule", "Write flooding(times, window, limit): times is a sorted list of message times in seconds from one account. True when more than limit messages fall inside any window of the given length (start inclusive, end exclusive).", "flooding(times, window, limit)", '''
def flooding(times, window, limit):
    for i in range(len(times)):
        c = 0
        for t in times:
            if t >= times[i] and t < times[i] + window:
                c += 1
        if c > limit:
            return True
    return False
''', [[[0, 1, 2, 3, 4, 5], 10, 3], [[0, 20, 40], 10, 1], [[], 10, 0]], "Slide a window.")]))


CHS.append(CH(
 "Voice, Mini Apps and the optional networks",
 ("Optional features", [
  "voice | joins | Calls",
  "whisper | transcribes | Speech",
  "xdc | joins | Mini Apps",
  "tor | routes through | Tor",
  "i2p | routes through | I2P router",
  "net client | avoids | Address leaks",
  "Cargo feature | plus builder | Both needed"]),
 ["Four optional features extend a bot. Voice joins voice channels and hears 48 kHz mono audio per speaker. Whisper turns clips into text. Xdc joins Mini Apps, small shared apps in a chat. Tor and I2P route traffic through anonymity networks.",
  "Tor and I2P need the Cargo feature and a builder call, .tor() or .i2p(). The feature alone only compiles the code in. A bot on Tor or I2P must name it on every run.",
  "For web requests, such as to a language model, use vector_sdk::net::build_http_client so a bot on Tor or I2P never leaks its address with a side request."],
 [("Voice channel", "A channel where members talk; the bot gets PCM audio per speaker."),
  ("PCM frame", "A 20 ms block of 48 kHz mono audio."),
  ("Mini App", "A .xdc file shared in a chat: a game or tool everyone who opens it uses together."),
  ("Session", "A bot's connection to one open copy of a Mini App."),
  ("Outproxy", "A gateway from I2P to the ordinary internet.")],
 ["Voice: channel.join_voice(); call.listen(); call.say(pcm).",
  "Audio is 48 kHz mono PCM; a frame is 20 ms.",
  "Mini Apps: bot.xdc(app_id).run(handler); sessions end after 3 minutes idle or 15 minutes quiet.",
  "Tor and I2P need the feature and .tor() or .i2p().",
  "Use vector_sdk::net::build_http_client for side requests."],
 [T("Voice turns a bot into a participant in a call. Audio arrives as short frames, twenty milliseconds each, one stream per speaker. At 48 thousand samples per second, one frame is 960 samples. The bot can queue its own audio with say, and wait for it with say_and_wait."),
  C("let call = bot.channel(voice_channel_id).join_voice().await?;\ncall.say(&vector_sdk::voice::tone(440.0, 1000));       // one second of A4\nwhile let Some(speech) = call.listen().await {\n    println!(\"{:?}: {} samples\", speech.npub, speech.pcm.len());\n}", "rust"),
  T("A bot must be listening, through run or on_event, to join a call. A call ends when a moderator disconnects or moves the bot: listen returns None and say returns false, and moved_to names the new channel if you want to follow. Building voice needs cmake for libopus."),
  T("A Mini App is a web app packaged as an xdc file. With the xdc feature the bot can be an opponent, a referee, or the server behind an app that needs more than a phone. Handler sessions end when the handler returns, after 3 minutes with nobody connected, or after 15 minutes without a message."),
  T("Be aware of what Mini Apps reveal. Players in a session can see each other's IP address, and the bot's. A bot on Tor or I2P stays out of sessions unless you explicitly allow outside transport."),
  C("// Tor needs the Cargo feature AND the builder call\n// cargo add vector_sdk --features tor\nlet bot = VectorBot::builder().nsec(key).tor().build().await?;\n// I2P uses the router already running on the machine (SAM at 127.0.0.1:7656)\nlet bot = VectorBot::builder().nsec(key).i2p().build().await?;", "rust")],
 [("What audio format does voice use?", ["48 kHz mono PCM", "MP3", "8 kHz stereo", "Opus only"], 0, "Frames of 20 ms."),
  ("Which feature transcribes speech?", ["whisper", "xdc", "tor", "i2p"], 0, "whisper.cpp."),
  ("What does Tor need?", ["Feature and .tor()", "Only the feature", "Only .tor()", "A VPN"], 0, "Both."),
  ("What does I2P rely on?", ["A router already running locally", "A built-in router", "A browser", "Tor"], 0, "SAM bridge."),
  ("What can players in a Mini App session see?", ["Each other's IP address", "Nothing", "The nsec", "The password"], 0, "Privacy cost."),
  ("Why use net::build_http_client?", ["Side requests use the bot's own transport", "It is faster", "It signs messages", "It is required for voice"], 0, "No address leak.")],
 [("join_voice", "Join a voice channel call"), ("Utterances", "Groups frames into one clip per speaker per pause"), ("xdc session", "A bot's link to an open Mini App"), (".clearnet()", "Return to direct connections")],
 [APP("EVENTS", "Event router", "Try events from voice, Mini Apps and communities on the same router."),
  MATCH("Match the feature", "Pair each feature with its job.", [("voice", "join calls"), ("whisper", "turn speech into text"), ("xdc", "take part in Mini Apps"), ("tor", "route through Tor")]),
  FILL("Optional", "Voice audio is {{48}} kHz {{mono}} PCM. Tor needs the Cargo feature and the {{builder}} call. Use the SDK's {{net}} http client for side requests."),
  PL("Samples per frame", "Write frame_samples(rate, ms): return how many samples a frame of ms milliseconds has at the given sample rate (an integer).", "frame_samples(rate, ms)", '''
def frame_samples(rate, ms):
    return rate * ms // 1000
''', [[48000, 20], [48000, 1000], [16000, 20]], "rate times seconds."),
  PL("Tone length", "Write tone_samples(rate, ms): number of samples in a tone lasting ms milliseconds at the given rate.", "tone_samples(rate, ms)", '''
def tone_samples(rate, ms):
    return rate * ms // 1000
''', [[48000, 1000], [48000, 250], [8000, 500]], "Same arithmetic."),
  PL("Session alive?", "Write session_alive(idle_minutes, quiet_minutes, handler_returned): a Mini App handler session ends when the handler returned, or nobody has been connected for 3 minutes, or no message for 15 minutes. Return True while none of these has happened.", "session_alive(idle_minutes, quiet_minutes, handler_returned)", '''
def session_alive(idle_minutes, quiet_minutes, handler_returned):
    if handler_returned:
        return False
    if idle_minutes >= 3:
        return False
    if quiet_minutes >= 15:
        return False
    return True
''', [[0, 0, False], [3, 0, False], [0, 15, False], [1, 2, True], [2, 14, False]], "Three ways to end."),
  PL("Anonymity configured?", "Write network_ok(feature_on, builder_call): True only if both the Cargo feature and the builder call are present.", "network_ok(feature_on, builder_call)", '''
def network_ok(feature_on, builder_call):
    return feature_on and builder_call
''', [[True, True], [True, False], [False, True], [False, False]], "Both."),
  PL("Does the call end?", "Write call_state(event): 'disconnect' and 'move' give 'ended'; 'mute' and 'deafen' give 'active'; anything else gives 'active'.", "call_state(event)", '''
def call_state(event):
    if event in ('disconnect', 'move'):
        return 'ended'
    return 'active'
''', [['disconnect'], ['move'], ['mute'], ['talk']], "A moderator action ends it.")]))


CHS.append(CH(
 "Security, privacy and troubleshooting",
 ("Operations", [
  "Keys | stay | Out of code",
  "wss | protects | Relay traffic",
  "Relays | see | Metadata",
  "Not connected | means | build not done",
  "No events | means | Process exited",
  "vector-lab | tests | Live relays",
  "Supervisor | restarts | The bot"]),
 ["Treat the nsec and mnemonic as passwords: read them from the environment or a secret store, never commit or log them, and rotate when in doubt. Use wss relays, cap the size of files you accept, and keep logs free of message text.",
  "Be honest about limits. Relays can see metadata and can delay or withhold messages, profile information is public, and a leaked key can expose what that key could read. Voice and Mini App sessions can reveal network addresses unless the bot uses Tor or I2P.",
  "Most failures are simple: using the bot before build finishes, letting the process exit, a relative file path, or missing rights. vector-lab can test a setup against real relays before you deploy."],
 [("wss", "A websocket secured with TLS."),
  ("Metadata", "Facts about a message such as time and size that remain visible even when the content is encrypted."),
  ("vector-lab", "A tool in the repository that runs bots against real relays and checks what each saw."),
  ("Supervisor", "A process manager such as systemd that restarts the bot."),
  ("Runbook", "Written steps for operating and recovering a service.")],
 ["Never hardcode, commit or log keys.",
  "Await build() before any other call.",
  "No events: keep the process alive.",
  "Relative file paths follow the working directory; use absolute paths in services.",
  "Test against real relays with vector-lab before deploying."],
 [T("Security for a bot is mostly discipline. The encryption is the SDK's job, but the key, the host and the logs are yours. A bot that logs every message has undone the privacy it was built to provide."),
  T("Keep keys out of code and out of version control. Read VECTOR_NSEC from the environment, give the data directory restrictive file permissions, and keep a plan for rotating the identity if it leaks. Rotating means a new npub, so tell the people who rely on it."),
  C("# turn on library logging while diagnosing (set RUST_LOG for Rust crates)\nRUST_LOG=vector_sdk=debug cargo run --example echo_bot\n\n# check a setup against real relays\ncargo run -p vector-lab -- all --relays wss://your.relay", "bash"),
  T("When something fails, check the cheap things first. Is the process running? Did build finish before the first call? Is the key right? Does the bot have the right in that community? Is the relay reachable? Only then read deeper logs."),
  T("Two classic mistakes: registering handlers and then letting main return, and relying on a relative path in a service. A service started by systemd runs from a different folder than your shell, so send_file with a relative name may not find the file."),
  T("For retries, wait longer each time with a cap, and treat errors differently. A network error deserves a retry, a bad key does not. The SDK already reconnects and catches up for you, so do not add a second reconnect loop on top.")],
 [("Where should the nsec live?", ["Environment or secret store", "In the source", "In a log", "In the README"], 0, "Not in code."),
  ("Not connected error. First check?", ["build() finished", "Change relay", "Upgrade Rust", "Reboot"], 0, "Await build."),
  ("No events arrive. Why?", ["The process exited", "Relays are full", "Wrong emoji", "Tor"], 0, "Keep running."),
  ("Why use absolute paths in services?", ["Working directory differs from your shell", "They are faster", "Required by Rust", "Relays need them"], 0, "systemd."),
  ("What can relays see?", ["Metadata", "Message text of encrypted DMs", "The nsec", "Nothing"], 0, "Limits of privacy."),
  ("Should you add your own reconnect loop?", ["No, the SDK reconnects", "Yes always", "Only for DMs", "Only for voice"], 0, "Avoid doubling.")],
 [("RUST_LOG", "Sets Rust log level"), ("vector-lab", "Live relay checks"), ("Rotation", "Moving to a new key"), ("Backoff", "Waiting longer after each failure")],
 [MATCH("Match the symptom", "Pair each symptom with the first check.", [("not connected", "await build"), ("no events", "process alive"), ("ban refused", "bot's rights"), ("file not found", "working directory")]),
  FILL("Operations", "Never log or commit the {{nsec}}. Use {{wss}} relays. Relays can see {{metadata}}. Test with {{vector-lab}} before you deploy."),
  ORDER("Diagnose", "Put the checks in a sensible order.", ["Is the process running?", "Did build() finish?", "Is the key correct?", "Does the bot have the right?", "Read debug logs"]),
  PL("Backoff with cap", "Write waits(n, base, cap): return the first n retry waits; the first is base, each next doubles, never above cap.", "waits(n, base, cap)", '''
def waits(n, base, cap):
    out = []
    w = base
    for i in range(n):
        out.append(min(w, cap))
        w = w * 2
    return out
''', [[5, 1, 10], [3, 2, 100], [0, 1, 1]], "Double and clamp."),
  PL("Retry or stop", "Write retry_decision(error): 'network' and 'timeout' give 'retry'; 'auth' and 'invalid_key' give 'stop'; 'refused' gives 'tell person'; anything else gives 'log'.", "retry_decision(error)", '''
def retry_decision(error):
    if error in ('network', 'timeout'):
        return 'retry'
    if error in ('auth', 'invalid_key'):
        return 'stop'
    if error == 'refused':
        return 'tell person'
    return 'log'
''', [['network'], ['auth'], ['refused'], ['weird']], "Different errors, different actions."),
  PL("Diagnose", "Write diagnose(symptom): 'not connected' gives 'await build'; 'no events' gives 'keep process alive'; 'refused' gives 'check rights'; 'file missing' gives 'check working directory'; anything else gives 'enable debug logs'.", "diagnose(symptom)", '''
def diagnose(symptom):
    if symptom == 'not connected':
        return 'await build'
    if symptom == 'no events':
        return 'keep process alive'
    if symptom == 'refused':
        return 'check rights'
    if symptom == 'file missing':
        return 'check working directory'
    return 'enable debug logs'
''', [['not connected'], ['no events'], ['refused'], ['file missing'], ['strange']], "A lookup."),
  PL("File policy", "Write accept_file(size_bytes, limit_bytes, allowed_type, kind): True only when the size is within the limit and the kind is in the allowed_type list.", "accept_file(size_bytes, limit_bytes, allowed_type, kind)", '''
def accept_file(size_bytes, limit_bytes, allowed_type, kind):
    return size_bytes <= limit_bytes and kind in allowed_type
''', [[100, 1000, ['png', 'pdf'], 'png'], [2000, 1000, ['png'], 'png'], [100, 1000, ['png'], 'exe']], "Both checks."),
  PL("Redact for logs", "Write redact(text): split on single spaces; any word starting with 'nsec1' becomes 'nsec1[redacted]'. Join with single spaces.", "redact(text)", '''
def redact(text):
    out = []
    for w in text.split(' '):
        if w.startswith('nsec1'):
            out.append('nsec1[redacted]')
        else:
            out.append(w)
    return ' '.join(out)
''', [['key nsec1abcdef loaded'], ['no secrets here'], ['nsec1zz']], "Words that start with nsec1.")]))
