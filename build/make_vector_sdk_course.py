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
SANDBOX = cmk.terminal("Vector SDK cheat sheet", "vector>", "A scripted lookup. Try: version, build, keys, send, reply, events, invites, security, tor, examples, trouble", [
    ("version", ["Docs describe SDK 0.3.0 (targets Vector 0.4.0+). The GitHub main branch showed 0.2.1 with VectorBot::quick. Pin and verify."]),
    ("build", ["VectorBot::builder().nsec(&nsec).build().await? connects. Optional: .mnemonic, .password, .public, .whitelist, .data_dir, .tor, .tor_bridges."]),
    ("keys", ["Keyless bots save identity.nsec in the data directory. Explicit keys stay in memory. One identity per process."]),
    ("send", ["bot.dm(npub) or bot.channel(id), then send, reply, edit, delete, react, typing, send_file."]),
    ("reply", ["channel.reply(msg_id, text). IncomingMessage also has reply and react."]),
    ("events", ["on_message(handler), on_event(handler). BotEvent: Message, MessageUpdate, Delete, MemberJoin, MemberLeave, Typing, Invite, Removed."]),
    ("invites", ["Manual (default): accept_invite. Public: accept anyone. Whitelist: listed npubs only, others silently ignored."]),
    ("security", ["AES-256-GCM files, SHA-256 integrity, NIP-59 gift wrap. Use wss, never commit keys, rotate every 6 to 12 months."]),
    ("tor", ["Needs the tor Cargo feature and .tor(); without the feature .tor() has no effect."]),
    ("examples", ["cargo run -p vector-sdk --example echo_bot (also slash_command_bot, ai_bot, moderation_bot, whitelist_bot, file_bot, save_files_bot). Needs VECTOR_NSEC."]),
    ("trouble", ["Not connected: await build. No events: keep the process alive. DM fails: inbox relays. Stale id: sync_communities. Debug: RUST_LOG=vector_sdk=debug."]),
])
EXAM = [
 ("What is the Vector SDK written in?", ["Rust", "Python", "Go", "Java"], 0, "Cargo crate."),
 ("A bot's public address starts with:", ["npub1", "nsec1", "http", "0x"], 0, "Bech32."),
 ("Which key must stay secret?", ["nsec", "npub", "relay URL", "bot name"], 0, "Private key."),
 ("Which versions did the docs and repo main show?", ["0.3.0 docs and 0.2.1 repo", "1.0 both", "2.0 and 3.0", "None"], 0, "Verify versions."),
 ("What does a keyless bot save?", ["identity.nsec", "Nothing", "The password", "The npub only"], 0, "In the data dir."),
 ("Two keyless bots on a machine need:", ["Separate data dirs", "One nsec", "Tor", "Nothing"], 0, "Avoid sharing."),
 ("Explicit keys are:", ["Kept in memory only", "Always saved", "Sent to relays", "Printed"], 0, "Per docs."),
 ("How do you open a DM?", ["bot.dm(npub)", "bot.run", "bot.sync", "bot.dissolve"], 0, "Channel."),
 ("A typing hint expires after:", ["About 30 seconds", "1 second", "1 day", "Never"], 0, "NIP-40."),
 ("Relative send_file paths resolve against:", ["Working directory", "Relay", "npub", "Data dir always"], 0, "Use absolute paths."),
 ("How many BotEvent variants?", ["Eight", "Two", "Four", "Twelve"], 0, "Listed in docs."),
 ("Why check is_mine()?", ["Avoid reply loops", "Speed", "Encryption", "Billing"], 0, "Skip own messages."),
 ("Default invite policy?", ["Manual", "Public", "Whitelist", "None"], 0, "A person accepts."),
 ("Whitelist, unlisted sender:", ["Silently ignored", "Accepted", "Banned", "Replied"], 0, "No refusal."),
 ("Who can dissolve a community?", ["The owner", "Any member", "Any bot", "Relays"], 0, "Irreversible."),
 ("Files are encrypted with:", ["AES-256-GCM", "ROT13", "MD5", "None"], 0, "Authenticated."),
 ("Integrity is checked with:", ["SHA-256", "CRC8", "Parity", "Nothing"], 0, "Hash."),
 ("Which relay scheme is safe?", ["wss://", "ws://", "http://", "ftp://"], 0, "TLS."),
 ("Tor needs:", ["Cargo feature and .tor()", ".tor() only", "Feature only", "VPN"], 0, "Both."),
 ("Examples need the variable:", ["VECTOR_NSEC", "HOME", "PATH", "USER"], 0, "Identity."),
 ("ai_bot needs:", ["OPENAI_API_KEY", "A GPU", "Tor", "A mnemonic"], 0, "Endpoint key."),
 ("No events arrive. First check:", ["Process kept alive", "Delete keys", "Change relay", "Upgrade Rust"], 0, "Do not exit main."),
 ("Stale community id:", ["sync_communities()", "New key", "Rewrite", "Ignore"], 0, "Refresh."),
 ("Debug logging:", ["RUST_LOG=vector_sdk=debug", "--verbose", "DEBUG only", "None"], 0, "Env var."),
 ("A leaked key may expose:", ["Old messages", "Nothing", "Only the name", "Only new ones"], 0, "Rotate."),
]
CFG = dict(id="vector-sdk", title="Vector SDK: Private Bots on Nostr",
    subtitle="Identity, channels, events, communities, encryption and operations for Vector bots, with Python labs",
    description="A hands-on course based on the public Vector SDK documentation (vector-privacy.gitbook.io/vector-privacy/vector-sdk) and the VectorPrivacy/Vector-SDK repository. The documentation describes SDK 0.3.0 with a builder API, while the repository main branch we inspected still showed 0.2.1, so everything is presented as reported in November 2026 and you should verify the version you use. Learn how a Rust bot gets an identity, sends and reacts to messages, handles events, manages communities and invites, protects files and keys, and is troubleshot and deployed. Labs run offline and simulate the rules in Python, since Rust cannot run here.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="vsdk", apps={"__POLICY__": "policy.html", "__EVENTS__": "events.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "vector-sdk.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
