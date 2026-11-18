#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Vectiq course (lucky-edgelord/aio-vector-bot, MIT). 13 chapters, 26 figures, 26 tables, offline Python labs.
Usage: python3 make_vectiq_course.py [out.json]"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vq")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "cd"))
import cmk, vq_a, vq_b, figs, figdefs, vqmaps  # noqa: E402
from clib import T  # noqa: E402

CHS = vq_a.CHS + vq_b.CHS
assert len(CHS) == 13

ANCHOR = re.compile(r"\s*\(See (Figure|Table) [\d.]+ below\.\)")
NFIG = NTAB = 0
for _ci, _ch in enumerate(CHS):
    _nf = _nt = 0
    _out = []
    for _b in _ch["lesson"]:
        if _b["type"] == "text":
            _b["items"] = [ANCHOR.sub("", it) for it in _b["items"]]
        if _b["type"] in ("figure", "table"):
            if _b["type"] == "figure":
                _nf += 1; _lab = "Figure %d.%d" % (_ci + 1, _nf); _b["caption"] = _lab + ". " + _b["caption"]
            else:
                _nt += 1; _lab = "Table %d.%d" % (_ci + 1, _nt); _b["title"] = _lab + ". " + _b["title"]
            for _p in reversed(_out):
                if _p["type"] == "text":
                    _p["items"][-1] = _p["items"][-1].rstrip() + " (See %s below.)" % _lab
                    break
        _out.append(_b)
    _ch["lesson"] = _out
    assert _nf >= 2 and _nt >= 2, (_ci + 1, _nf, _nt)
    NFIG += _nf; NTAB += _nt


def _split(t, lim=380):
    if len(t) <= lim:
        return [t]
    cuts = [m.end() for m in re.finditer(r"[.!?] (?=[A-Z(])", t)]
    if not cuts:
        return [t]
    k = min(cuts, key=lambda c: abs(c - len(t) / 2))
    return _split(t[:k].rstrip(), lim) + _split(t[k:], lim)


for _ch in CHS:
    for _b in _ch["lesson"]:
        if _b["type"] == "text":
            _b["items"] = [x for it in _b["items"] for x in _split(it)]

assert len(vqmaps.MAPS) == len(CHS)
for _c, _m in zip(CHS, vqmaps.MAPS):
    _c["maps"] = [{"title": _m[0], "links": _m[1]}]

for _i in range(1, len(CHS)):
    _prev = CHS[_i - 1]
    CHS[_i]["lesson"].insert(0, T("Quick recap of the last chapter, " + _prev["title"] + ":", *["• " + k for k in _prev["keyPoints"]]))

MNEM = [
 ("Bot, SQLite, modules", "Vectiq = a community Bot on Vector, with SQLite memory, split into Modules: 'B-S-M'. Groups: 'Some Men Can Find Imaginary' = Safety, Members, Community, Fun, Integrations."),
 ("Cogs talk, stores remember", "Cogs Chat with Vector, Stores Save to SQL, rules stay Clean: 'Chat, Save, Clean'."),
 ("One lock, one thread, one version", "Database: one connection, one lock, to_thread, and a user_version. Transactions are all-or-nothing: 'Both or None'."),
 ("Defaults, file, dashboard", "Settings stack: Defaults, File, Dashboard, Dotenv for secrets. 'Dogs Find Dishes, Digging Deep'. Top layer wins."),
 ("One slot, one provider", "A slot is a seat: 'One bum per seat'. Plugins start Off: 'new guests wait outside'."),
 ("Check, cool, run", "A command passes Check, then Cooldown, then Runs: 'Check, Cool, Run'. Errors go to one place."),
 ("Five n squared", "Level step: 5 n squared, plus 50 n, plus 100. 'Five squared fifty a hundred'. Cooldown means one award a minute."),
 ("All or nothing coins", "Money moves Atomically: 'Hold the note until they have it.' Streak bonus = 25 times (streak minus 1), capped at 10."),
 ("Log first, then delete", "Try rules with Log before Delete, Warn, Timeout: 'Look, Delete, Warn, Time out' (L-D-W-T)."),
 ("Stamp the hand, remember the face", "Verify once, Store the result, Hash the device with a secret: 'Stamp, Store, Scramble'."),
 ("The bot is the referee", "Apps Ask, the Bot Decides, the rules are Pure: 'Ask, Decide, Pay'."),
 ("Save before you leap", "Restore points: Schedule, Automatic, Manual = 'SAM'. Rollback saves first."),
 ("Rehearse small, then big", "Test Rules, then Stores, then Cogs, using fakes. Plugins import only from vectiq.plugin: 'R-S-C, API only'."),
]
assert len(MNEM) == len(CHS)
for _c, (_m, _d) in zip(CHS, MNEM):
    _full = _m + ". " + _d
    _c["lesson"].append(T("Memory trick: " + _full))
    _c["cards"].append({"q": "Memory trick for: " + _c["title"] + "?", "a": _full})
IMAGES = figs.build_all()

PRONOUNCE = {"Vectiq": "VEK tick", "Vector": "vec tor", "vector-sdk-py": "vector S D K pie", "Logiq": "LOJ ick", "MEE6": "me six", "Sentire": "sen TEER ay", "SQLite": "S Q L ite", "SQL": "S Q L", "sqlite3": "S Q L ite three",
    "WAL": "wall", "asyncio": "a sink eye oh", "async": "a sink", "await": "a wait", "PyO3": "pie oh three", "Pillow": "pillow", "PyYAML": "pie yam ul", "YAML": "yam ul", "FastAPI": "fast A P I", "FastMCP": "fast M C P",
    "MCP": "M C P", "uvicorn": "you vee corn", "yt-dlp": "Y T D L P", "pytest": "pie test", "dataclass": "data class", "importlib": "import lib", "HMAC": "H mac", "CAPTCHA": "cap chah", "Turnstile": "turn style", "hCaptcha": "H captcha",
    "reCAPTCHA": "re cap chah", "NudeNet": "nude net", "oisd": "oh eye S D", "WebXDC": "web X D C", "xdc": "X D C", "npub": "en pub", "nsec": "en sec", "GateBot": "gate bot", "henk": "henk", "JSKitty": "J S kitty",
    "TTL": "T T L", "CLI": "C L I", "API": "A P I", "UI": "you eye", "DMs": "D Ms", "DM": "D M", "JSON": "jay son", "HTTPS": "H T T P S", "HTTP": "H T T P", "CHECK": "check", "pragma": "prag ma", "PRAGMA": "prag ma",
    "to_thread": "to thread", "BEGIN": "begin", "IMMEDIATE": "immediate", "ROLLBACK": "roll back", "COMMIT": "commit", "tictactoe": "tic tac toe", "connect4": "connect four", "Docker": "docker", "systemd": "system D", "launchd": "launch D",
    "ELI5": "E L I five", "MIT": "M I T", "ruff": "ruff", "cogs": "cogs", "cog": "cog", "stdio": "standard I O", "bearer": "bearer", "Unix": "you nix", "NIP-40": "nip forty", "ics": "I C S", "env": "env", "dotenv": "dot env"}

SANDBOX = cmk.terminal("Vectiq cheat sheet", "vectiq>", "A scripted lookup, not the real bot. Try: install, check, setup, modules, module, level, daily, warn, verify, game, restore, mcp, plugin, test, layers", [
    ("install", ["git clone https://github.com/lucky-edgelord/aio-vector-bot", "python3 -m venv .venv && .venv/bin/pip install -e \".[dev]\"", "needs Python 3.10+, and Rust, cargo and cmake to build the Vector SDK"]),
    ("check", ["vectiq --check     validate config.yaml and .env", "vectiq --init      write a starter config", "vectiq --setup     run the setup wizard"]),
    ("setup", ["secrets in .env: VECTOR_NSEC=...", "settings in config.yaml, merged over DEFAULTS", "dashboard overrides are stored in the database"]),
    ("modules", ["vectiq --modules    list modules", "groups: Safety, Members, Community, Fun, Integrations", "!module on NAME / off NAME / reload NAME / scan"]),
    ("module", ["Module(name, label, help, group, cogs, default, imports, provides, defaults, settings, ...)", "slot = provides or name; one enabled provider per slot", "plugins start off"]),
    ("level", ["xp for a level = sum of 5n^2 + 50n + 100 for n below the level", "level 1 = 100, level 2 = 255, level 3 = 475", "default award 15 to 25 XP, cooldown 60 s"]),
    ("daily", ["paid = amount + bonus * min(streak - 1, cap)", "defaults 200, 25, 10", "day 11 pays 450"]),
    ("warn", ["!warn @member reason      adds a case", "3 warnings by default trigger a timeout", "durations: 90m, 1h30m, 2d; bare number is minutes"]),
    ("verify", ["modes: question, button, captcha", "device marks: HMAC of ip, cookie, fingerprint", "on_duplicate: refuse | kick | softban"]),
    ("game", ["!game tictactoe    shares the WebXDC app", "the bot joins the realtime channel as referee", "rules in games/ are pure Python"]),
    ("restore", ["vectiq --backup \"before the event\"", "vectiq --list-backups; vectiq --restore 3 (bot stopped)", "!restorepoint create / rollback N confirm"]),
    ("mcp", ["pip install \"vectiq[mcp]\"; !module on mcp", "http://127.0.0.1:8770/mcp with a bearer token", "read_only: true lets assistants look only"]),
    ("plugin", ["vectiq --new-module NAME", "define MODULE and async def setup(bot)", "import only from vectiq.plugin (API_VERSION 1)"]),
    ("test", [".venv/bin/pytest -q && .venv/bin/ruff check .", "Database(':memory:'), Stores(db), FakeBank, fake_community"]),
    ("layers", ["cogs/ = Vector I/O   stores/ = SQL   db/ = SQLite + migrations", "games/ and render/ = pure rules and Pillow pictures"]),
])

EXAM = [
 ("What is Vectiq?", ["A community-management bot for Vector", "A new messenger", "A database", "A web browser"], 0, "It manages communities."),
 ("Which library does Vectiq build on?", ["vector-sdk-py", "Django", "Flask", "Tkinter"], 0, "A discord.py style Vector library."),
 ("What does Vectiq store data in?", ["SQLite", "MongoDB", "Excel", "Redis only"], 0, "A single file."),
 ("Which is not a module group?", ["Hardware", "Safety", "Fun", "Integrations"], 0, "Groups: Safety, Members, Community, Fun, Integrations."),
 ("Which licence does Vectiq use?", ["MIT", "GPLv3 only", "Proprietary", "None"], 0, "Free with notice."),
 ("Where may SQL appear?", ["Only in stores", "In cogs", "In render", "In rules"], 0, "The layering rule."),
 ("Which layer talks to Vector?", ["Cogs", "Stores", "db", "games rules"], 0, "All Vector I/O."),
 ("Why do rules avoid the network?", ["Easy offline tests", "Speed", "Colour", "Licence"], 0, "Pure functions."),
 ("What does render draw?", ["Pillow pictures", "SQL", "Web pages", "Audio"], 0, "Rank cards and calendars."),
 ("Why is sqlite3 run in a thread?", ["It blocks", "It is slow to import", "It needs root", "For colour"], 0, "Keep the event loop free."),
 ("What does a transaction give?", ["All or nothing", "Encryption", "Caching", "Logging only"], 0, "Atomic."),
 ("Where is the schema version kept?", ["PRAGMA user_version", "config.yaml", "A log", "The dashboard"], 0, "Inside the file."),
 ("How do you change a shipped table?", ["Append a migration", "Edit the old one", "Drop the file", "Use pip"], 0, "Never edit an applied migration."),
 ("What does WAL allow?", ["Readers and a writer together", "Faster Python", "Encryption", "Compression"], 0, "Write-ahead logging."),
 ("Which setting layer wins?", ["Dashboard overrides", "DEFAULTS", "config.yaml", "README"], 0, "Top layer."),
 ("Where do secrets belong?", [".env", "config.yaml", "dashboard", "the repo"], 0, "Kept apart."),
 ("What does a recursive merge do?", ["Merges nested keys", "Replaces sections", "Sorts keys", "Deletes defaults"], 0, "Only the written keys change."),
 ("Which flag validates config?", ["--check", "--wipe", "--zap", "--pdf"], 0, "Validation."),
 ("What is a slot?", ["A job one module holds at a time", "A database table", "A command", "A theme"], 0, "Avoids two automods."),
 ("Plugins start...", ["Switched off", "Switched on", "Deleted", "Hidden"], 0, "Safe by default."),
 ("What do cogs hold?", ["Commands, listeners, loops", "Only SQL", "Only images", "Only config"], 0, "Vector-facing code."),
 ("Native slash command limit?", ["64", "8", "256", "none"], 0, "NATIVE_LIMIT."),
 ("What handles command failures?", ["on_command_error", "print", "nothing", "the DB"], 0, "Central handler."),
 ("Default XP per message award?", ["15 to 25", "1 to 2", "500", "0"], 0, "xp_min and xp_max."),
 ("Total XP for level 2?", ["255", "100", "55", "300"], 0, "100 plus 155."),
 ("Which curve does leveling use?", ["MEE6", "Linear", "Random", "Fibonacci"], 0, "5n squared + 50n + 100."),
 ("Why rank cards in a thread?", ["Image work is slow", "Pillow needs root", "SQL requires it", "For colour"], 0, "Keep the loop free."),
 ("Default daily amount?", ["200", "10", "2000", "1"], 0, "economy.daily_amount."),
 ("Day 11 payout with defaults?", ["450", "200", "225", "275"], 0, "200 plus 25 times 10."),
 ("What does a missed streak do?", ["Restarts at one", "Doubles", "Pays more", "Bans"], 0, "Reset."),
 ("Why are transfers atomic?", ["No half-moved coins", "Speed", "Looks", "Fewer tables"], 0, "All or nothing."),
 ("Default warnings before timeout?", ["3", "1", "20", "0"], 0, "warn_threshold."),
 ("What does enforce do on error?", ["Never raises", "Crashes the bot", "Bans staff", "Restarts"], 0, "Safe to call."),
 ("In linksafety what beats everything?", ["allow", "block", "lists", "random"], 0, "Allow list."),
 ("A bare number in a duration means...", ["minutes", "seconds", "days", "error"], 0, "parse_duration."),
 ("Which verification mode needs a web address?", ["captcha", "question", "button", "none"], 0, "A personal page."),
 ("Why store verification in the DB?", ["Survives lost role or rejoin", "Saves disk", "Colour", "Law"], 0, "Persistent."),
 ("Why HMAC for device marks?", ["Cannot be reversed without the secret", "Shorter text", "Faster", "Prettier"], 0, "Privacy."),
 ("Who decides game state?", ["The bot", "The phones", "The relay", "Nobody"], 0, "Referee."),
 ("What does the packager guarantee?", ["Identical bytes per build", "Encryption", "Updates", "Speed"], 0, "Fixed timestamp."),
 ("Is the bot key in a restore point?", ["Never", "Always", "Only manual", "Only scheduled"], 0, "Kept in .env."),
 ("What happens before a rollback?", ["A point of now is saved", "Data deleted", "Nothing", "Bot restarts"], 0, "Undoable."),
 ("What does MCP read_only do?", ["Lets assistants only look", "Hides the token", "Stops the bot", "Encrypts"], 0, "No changes."),
 ("What must a plugin define?", ["MODULE and async setup(bot)", "A database", "A page", "A class Bot"], 0, "Description and entry."),
 ("Plugins should import from...", ["vectiq.plugin", "vectiq.stores", "vectiq.db", "anywhere"], 0, "Stable API."),
 ("How are stores tested?", ["In-memory SQLite", "Live Vector", "A phone", "By hand"], 0, "Database(':memory:')."),
]
print("exam", len(EXAM))

CFG = dict(id="vectiq-community-bot", title="Vectiq: Building a Community Bot for Vector",
    subtitle="How a real Python community-management bot is put together: SQLite, modules, cogs, economy, moderation, WebXDC games and plugins",
    description="A beginner-friendly tour of Vectiq (github.com/lucky-edgelord/aio-vector-bot, MIT), a community-management bot for the Vector messenger written in Python on vector-sdk-py. "
    "In 13 chapters you learn what the bot does and how its code is organised: the layering rule (cogs for Vector, stores for SQL, pure rules for logic), the async SQLite database with transactions and migrations, the layered configuration, the module and slot system, cogs and commands, the leveling curve, the atomic economy, moderation and safety modules, verification with device checks, WebXDC games with the bot as referee, restore points, the dashboard and MCP, and finally testing with fakes and writing your own plugin. "
    "There are 26 numbered figures, 26 numbered tables, a recap, a memory trick, an expanded ELI5 and a concept map in every chapter, a final exam, and a handful of short Python labs that run offline in the app: the XP curve, daily streaks, durations, domain lists, migrations, config merging, device marks, tic-tac-toe and slot conflicts. "
    "Credits: the course is original and describes the open source project Vectiq by lucky-edgelord and the Vectiq contributors (MIT licence). The project credits Logiq and MEE6 for the feature shape, GateBot by henk.tech (MIT) for the verification ideas and Sentire by JSKitty of VectorPrivacy for automod. Vector is a trademark of its owners and is not affiliated with this course. Read the source at the repository to see the current code.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, images=IMAGES)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "vectiq-community-bot.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
    print("figures", NFIG, "tables", NTAB)
