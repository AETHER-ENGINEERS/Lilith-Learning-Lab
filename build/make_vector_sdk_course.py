#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Vector SDK course. Usage: python3 make_vector_sdk_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "vsdk"))
import cmk, vsdk_a, vsdk_b, make_apps  # noqa: E402
make_apps.main()
CHS = vsdk_a.CHS + vsdk_b.CHS
PRONOUNCE = {"Vector": "vec tor", "Nostr": "nos ter", "npub": "en pub", "nsec": "en sec", "npub1": "en pub one", "nsec1": "en sec one", "tokio": "toe key oh", "Rust": "rust",
    "relay": "ree lay", "relays": "ree lays", "AES-256-GCM": "A E S two fifty six G C M", "SHA-256": "shaw two fifty six", "NIP-59": "nip fifty nine", "NIP-17": "nip seventeen",
    "NIP-25": "nip twenty five", "NIP-40": "nip forty", "NIP-96": "nip ninety six", "NIP-46": "nip forty six", "wss": "W S S", "Tor": "tor", "Arti": "ar tee", "mnemonic": "nuh mon ik",
    "bech32": "beck thirty two", "Cargo": "car go", "SDK": "S D K", "API": "A P I", "OpenAI": "open A I", "systemd": "system D", "Concord": "con cord", "JSON": "jay son", "DM": "D M", "DMs": "D Ms"}
SANDBOX = cmk.terminal("Vector SDK cheat sheet", "vector>", "A scripted lookup for vector_sdk 0.12.0. Try: install, build, keys, send, post, events, commands, invites, roles, voice, tor, security, trouble", [
    ("install", ["cargo add vector_sdk; cargo add tokio --features full. Rust 1.75 or newer. Features: tor, i2p, voice, whisper, xdc."]),
    ("build", ["VectorBot::builder().nsec(key).build().await? Then bot.run(handler) or bot.on_message(handler)."]),
    ("keys", ["No key: created once and reused. .nsec(), .mnemonic(), .password(), VectorBot::generate_nsec(). .data_dir() or VECTOR_DATA_DIR. One bot per process."]),
    ("send", ["bot.channel(id) or bot.dm(npub), then send, reply, react, unreact, typing, edit, delete, send_file, send_bytes."]),
    ("post", ["channel.post(text, PostOptions::default().reply_to(id).expires_in(600).to_bot(npub))."]),
    ("events", ["BotEvent: Ready, Message, Reaction, ReactionRemoved, Edit, Delete, MemberJoin, MemberLeave, Typing, CommunityChange, Dissolved, VoicePresence, Invite, Removed. History: channel.history(n)."]),
    ("commands", ["bot.command(name, desc).string().int().number().flag().user().choice().run(handler). Matched commands never reach on_message."]),
    ("invites", ["Manual (default): pending_invites, accept_invite. .public() accepts anyone. .whitelist([...]) only listed npubs. Join by link: bot.join(link)."]),
    ("roles", ["community.create_role(RoleSpec::new(..).permissions(Permissions::KICK | ..)), create_category, create_channel_with, set_overwrite, member.timeout, audit_log, policies() (dry run until arm)."]),
    ("voice", ["Feature voice: channel.join_voice(), call.listen(), call.say(pcm). 48 kHz mono PCM, 20 ms frames. whisper adds transcription."]),
    ("tor", ["Needs the Cargo feature and .tor(). I2P: feature and .i2p(), router with SAM on 127.0.0.1:7656. .clearnet() to go back."]),
    ("security", ["Keys from the environment, never logged or committed. Use wss. Relays see metadata. Rotate if leaked."]),
    ("trouble", ["Not connected: await build. No events: keep the process alive. Refused action: check rights. Relative path: use absolute paths. Debug with RUST_LOG=vector_sdk=debug."]),
])
EXAM = [
 ("What is the crate version used here?", ["0.12.0", "0.3.0", "0.2.1", "1.0"], 0, "Published 2026-11-11."),
 ("Minimum Rust version?", ["1.75", "1.50", "1.90", "1.0"], 0, "MSRV."),
 ("Which crate is the engine?", ["vector-core", "serde", "zip", "tempfile"], 0, "Crypto, network, storage."),
 ("Which are optional features?", ["tor, i2p, voice, whisper, xdc", "http, ftp", "gpu", "none"], 0, "Off by default."),
 ("What happens with no key?", ["Created once and reused", "Build fails", "A shared key", "A new key every run"], 0, "Stable identity."),
 ("Several keyless bots need:", ["Separate data directories", "One nsec", "Tor", "Nothing"], 0, "Avoid sharing."),
 ("Bots per process?", ["One", "Two", "Unlimited", "Zero"], 0, "README rule."),
 ("Do DMs and community channels need different code?", ["No, same Channel API", "Yes", "Only files", "Only replies"], 0, "One API."),
 ("How do you make a message expire?", ["post with expires_in", "edit", "react", "typing"], 0, "PostOptions."),
 ("How do you send a file from memory?", ["send_bytes", "send_file only", "upload", "post_file"], 0, "Bytes with a name."),
 ("Why check is_mine()?", ["Avoid reply loops", "Speed", "Billing", "Relays"], 0, "Skip own messages."),
 ("How do you read old messages?", ["channel.history(n)", "on_message replay", "bot.old()", "Ready"], 0, "Pull, not push."),
 ("What does run add over on_event?", ["Clean Ctrl-C exit", "Encryption", "History", "Retries"], 0, "Same stream."),
 ("Which argument becomes a dropdown?", ["choice", "string", "int", "flag"], 0, "Client UI."),
 ("Does a matched command reach on_message?", ["No", "Yes", "Only DMs", "Only admins"], 0, "Consumed."),
 ("Default invite policy?", ["Manual", "Public", "Whitelist", "None"], 0, "A person accepts."),
 ("Unlisted inviter under Whitelist:", ["Ignored", "Accepted", "Banned", "Replied"], 0, "Not accepted."),
 ("How do you combine permissions?", ["With |", "With +", "Strings", "Cannot"], 0, "Bit flags."),
 ("What does arm do?", ["Lets a policy act for real", "Bans all", "Makes a role", "Mutes the bot"], 0, "Ends dry run."),
 ("Voice audio format?", ["48 kHz mono PCM", "MP3", "8 kHz stereo", "WAV only"], 0, "20 ms frames."),
 ("Tor needs:", ["Feature and .tor()", ".tor() only", "Feature only", "VPN"], 0, "Both."),
 ("Mini App players can see:", ["Each other's IP address", "Nothing", "The nsec", "The password"], 0, "Privacy cost."),
 ("No events arrive. First check:", ["Process still running", "Delete keys", "Change relay", "Upgrade Rust"], 0, "Do not exit main."),
 ("Relative send_file path resolves against:", ["Working directory", "Relay", "npub", "Data dir"], 0, "Use absolute paths."),
 ("Where should the nsec live?", ["Environment or secret store", "Source", "Log", "README"], 0, "Not in code."),
]
CFG = dict(id="vector-sdk", title="Vector SDK: Private Bots on Nostr",
    subtitle="Identity, channels, events, communities, encryption and operations for Vector bots, with Python labs",
    description="A hands-on course based on the published vector_sdk crate, version 0.12.0 (11 November 2026, MIT, Rust 1.75+), its README, changelog and examples. Older write-ups describe 0.3.0 or 0.2.1; this course follows the current crate. Learn how a Rust bot gets an identity, sends and receives through one Channel API, handles events and history, declares typed slash commands, joins and runs communities with roles, overwrites and moderation policies, uses the optional voice, Mini App, Tor and I2P features, and is secured and troubleshot. Labs run offline and simulate the rules in Python, since Rust cannot run here.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="vsdk", apps={"__POLICY__": "policy.html", "__EVENTS__": "events.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "vector-sdk.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
