#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Vectiq user guide course, based on the Vectiq documentation. 11 chapters, 22 figures, 22 tables, offline Python labs.
Usage: python3 make_vectiq_course.py [out.json]"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vu")); sys.path.insert(1, os.path.join(HERE, "vq")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "cd"))
import cmk, vu_a, figs, figdefs  # noqa: E402
from clib import T  # noqa: E402

CHS = vu_a.CHS
assert len(CHS) == 11

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


for _i in range(1, len(CHS)):
    _prev = CHS[_i - 1]
    CHS[_i]["lesson"].insert(0, T("Quick recap of the last chapter, " + _prev["title"] + ":", *["• " + k for k in _prev["keyPoints"]]))

MNEM = [
 ("Own key, always on", "Give the bot its Own account, keep the computer Always on, test with !ping: 'Own, On, Ping'."),
 ("Edit, check, reload", "Change settings in three beats: Edit, Check, Reload (E-C-R). Module switches need a restart."),
 ("Greet, prove, pick", "New member: Greet, Prove, Pick = welcome, verification, role menu."),
 ("Three strikes, then time", "Every third warning triggers a timeout: 3, 6, 9. Case numbers keep the record."),
 ("Log, look, then delete", "New safety rule: Log, Look, Loosen or tighten, then Delete: 'L-L-D'."),
 ("Chat for XP, claim for coins", "Chat earns XP, !daily earns coins, a streak adds 25 a day up to 10 days."),
 ("Zone first", "Before events, set the Zone first, then Create, RSVP, Remind: 'Z-C-R-R'."),
 ("Open, claim, close", "Ticket: Open, Claim, Close, then read the Transcript: 'O-C-C-T'."),
 ("The bot is the referee", "Games: apps Ask, the bot Decides. Music needs yt-dlp and ffmpeg."),
 ("Lock the control room", "Dashboard: localhost, then HTTPS, then base_url. MCP token is a key: keep read_only when unsure."),
 ("Save, read, copy", "Routine: Save a restore point, Read the log, Copy backups elsewhere."),
]
assert len(MNEM) == len(CHS)
for _c, (_m, _d) in zip(CHS, MNEM):
    _full = _m + ". " + _d
    _c["lesson"].append(T("Memory trick: " + _full))
    _c["cards"].append({"q": "Memory trick for: " + _c["title"] + "?", "a": _full})
IMAGES = figs.build_all()

import make_vectiq_course as _tech  # reuse pronunciations
PRONOUNCE = dict(_tech.PRONOUNCE); PRONOUNCE.update({"launchd": "launch D", "systemd": "system D", "pipx": "pip ex", "Caddy": "caddy", "Tailscale": "tail scale", "winget": "win get", "Homebrew": "home brew", "kickstart": "kick start", "roster": "roster"})

SANDBOX = cmk.terminal("Vectiq command cheat sheet", "!", "A scripted lookup of chat commands, not the real bot. Try: ping, warn, timeout, ban, purge, level, daily, shop, event, giveaway, poll, ticket, game, play, notify, dashboard, backup, verify", [
    ("ping", ["!ping    the bot answers if it is running and in the community", "!help    lists what is on"]),
    ("warn", ["!warn @sam reason   !warnings @sam   !delwarn 17   !clearwarns @sam", "third warning: timeout of one hour (then 6 and 9)"]),
    ("timeout", ["!timeout @sam 30m reason    !untimeout @sam", "durations: 30m, 2h, 1d12h; max 28 days"]),
    ("ban", ["!kick @sam   !ban @sam reason   !tempban @sam 3d reason", "!softban @sam   !unban npub1... (also lifts softbans)"]),
    ("purge", ["!purge 25 deletes the last 25 (max 100)", "!lock / !unlock   !slowmode 10 (0 = off)"]),
    ("level", ["!rank   !leaderboard [page]   !levelcurve", "!levelreward add 5 Regular   !levelreward remove 5"]),
    ("daily", ["!daily (200 coins, 24 h; keep the streak by claiming within 48 h)", "!work   !balance   !deposit 100   !withdraw 100   !pay @sam 50"]),
    ("shop", ["!shop   !buy VIP   !inventory", "admin: !shop add 500 VIP | description role:Name   !shop remove VIP"]),
    ("event", ["!event create Title | friday 8pm | 2h | description", "!event timezone America/New_York   !event rsvp 4 going", "!event edit 4 capacity 8 / repeat weekly / remind 1d, 30m"]),
    ("giveaway", ["!giveaway start 1h 2 Prize   end ID   reroll ID   cancel ID   list"]),
    ("poll", ["!poll Best colour? | Red | Green | Blue   (2 to 9 options)", "!analytics 30   !userinfo @sam   !communityinfo"]),
    ("ticket", ["!tickets open reason   claim   close   transcript 12"]),
    ("game", ["!game tictactoe | connect4 | trivia | slots", "!gamestats   !gameboard trivia"]),
    ("play", ["!play words or link   !search   !queue   !skip   !shuffle   !volume 60   !filter bassboost"]),
    ("notify", ["!module on notifications", "!notify add youtube @Name #videos   !notify add twitch name #live @Role   !notify remove 2"]),
    ("dashboard", ["modules.dashboard: true, then open http://localhost:8090", "!dashboard sends a sign-in link by DM", "vectiq --add-user NAME --npub npub1..."]),
    ("backup", ["!restorepoint create label   !restorepoint rollback N confirm", "vectiq --backup label; --list-backups; --restore N (bot stopped)"]),
    ("verify", ["modes: question, button, captcha", "!verification   !forceverify @sam   !unverify @sam   !softban @sam"]),
])

EXAM = [
 ("Whose key should the bot use?", ["Its own account's key", "Your personal key", "A friend's key", "None"], 0, "A separate account."),
 ("What command tests the bot?", ["!ping", "!hello", "!test all", "!on"], 0, "It answers."),
 ("What does the first install build?", ["The Rust core", "A website", "A game", "A phone app"], 0, "Needs rustc, cargo, cmake."),
 ("Where does the bot's key go?", [".env", "config.yaml", "chat", "a note"], 0, "Never in the YAML."),
 ("Which route needs no clone?", ["pipx", "install.sh", "install.ps1", "docker only"], 0, "pipx install from git."),
 ("What validates config.yaml?", ["--check", "--run", "--wipe", "--zap"], 0, "Plain messages."),
 ("What applies most changes?", ["!vectiq reload", "!apply", "!reboot", "nothing"], 0, "Bot owners only."),
 ("Do module switches need a restart?", ["Yes", "No", "Only some", "Only on Docker"], 0, "Reload is not enough."),
 ("Which placeholder gives the member count?", ["{count}", "{name}", "{mention}", "{id}"], 0, "Number of members."),
 ("What previews the welcome message?", ["!testwelcome", "!welcome", "!preview", "!hello"], 0, "Needs Manage Community."),
 ("Which verification mode uses a web page?", ["captcha", "question", "button", "gate"], 0, "Needs a key and address."),
 ("Where does the CAPTCHA secret go?", [".env", "config.yaml", "chat", "README"], 0, "Never in the YAML."),
 ("How do you write a space in a role name in a menu?", ["underscore", "dash", "quote", "slash"], 0, "Music_Lover."),
 ("What happens at the third warning by default?", ["One-hour timeout", "Ban", "Nothing", "Kick"], 0, "And at six and nine."),
 ("Which command lists a member's cases?", ["!history", "!purge", "!lock", "!poll"], 0, "All cases."),
 ("What does !purge 25 do?", ["Deletes 25 messages", "Bans 25", "Warns 25", "Lists 25"], 0, "Up to 100."),
 ("What lifts a tempban?", ["The bot at the end time", "A mod by hand", "Nothing", "The member"], 0, "Checked every 30 seconds."),
 ("What should a new safety rule begin with?", ["action log", "action ban", "action kick", "no test"], 0, "Watch first."),
 ("In linksafety, which list wins?", ["allow", "block", "public lists", "random"], 0, "Allow beats everything."),
 ("What catches resized copies of a picture?", ["A perceptual hash", "The file name", "The upload time", "The size"], 0, "Fingerprint."),
 ("Who is skipped by safety rules?", ["Staff and exempt roles", "Everyone", "Nobody", "Bots only"], 0, "Manage Messages."),
 ("Can both Sentire modules run?", ["No, one slot", "Yes", "Only on Mac", "Only with Docker"], 0, "Shared automod slot."),
 ("How often can XP be earned?", ["Once per cooldown", "Every message", "Once a day", "Never"], 0, "60 seconds by default."),
 ("How do you give a role at a level?", ["!levelreward add", "!rank", "!daily", "!shop"], 0, "Or in config."),
 ("When does a daily streak continue?", ["Claim within 48 hours", "Claim within 1 hour", "Never", "Weekly"], 0, "Else restarts."),
 ("How does a shop item give a role?", ["role:Name in the description", "A separate command", "It cannot", "!giverole"], 0, "Created if missing."),
 ("Total XP for level 5?", ["1,150", "500", "5,000", "250"], 0, "From the table."),
 ("What is required to create an event?", ["Title and time", "A picture", "A length", "Everything"], 0, "Others optional."),
 ("What fixes event times that are hours off?", ["!event timezone", "!event fix", "!reboot", "nothing"], 0, "Default is UTC."),
 ("How many poll options are allowed?", ["2 to 9", "1 to 3", "10 to 20", "Any"], 0, "Numbered reactions."),
 ("What does reroll do?", ["Draws a replacement winner", "Restarts", "Cancels", "Deletes"], 0, "After a giveaway ends."),
 ("Who sees a ticket?", ["Opener and the support role", "Everyone", "The bot only", "Nobody"], 0, "Name a support_role."),
 ("Is the security cam on by default?", ["No", "Yes", "Only on Mac", "Only for owners"], 0, "It shows everything."),
 ("Who decides game state?", ["The bot", "Each player", "The relay", "Chance"], 0, "Referee."),
 ("What does music need besides vectiq[music]?", ["ffmpeg", "Java", "A printer", "Docker only"], 0, "And yt-dlp."),
 ("What happens to old feed items when you add a feed?", ["Remembered, not posted", "All posted", "Deleted", "DMed"], 0, "No flood."),
 ("Is the dashboard on by default?", ["No", "Yes", "Only for owners", "Only on Mac"], 0, "modules.dashboard."),
 ("Who may sign in to the dashboard?", ["Admins and bot owners", "Anyone", "Members", "Bots"], 0, "Restricted."),
 ("What does MCP read_only do?", ["Lets assistants only look", "Hides the dashboard", "Stops the bot", "Locks the DB"], 0, "No changes."),
 ("What stops dashboard sign-in cookies working?", ["http and https mismatch", "Long passwords", "Dark mode", "Many members"], 0, "Set base_url correctly."),
 ("What is never inside a restore point?", ["The bot's key", "The database", "Config", "Pictures"], 0, "Keep your own copy."),
 ("What should you read first when something breaks?", ["The log", "Social media", "The licence", "Nothing"], 0, "Most problems are named."),
 ("Which flag restores a restore point?", ["--restore N", "--undo", "--back", "--revert"], 0, "Stop the bot first."),
 ("What if two copies of the bot run in one process?", ["Only one Vector bot per process is allowed", "Double XP", "Both work", "Nothing"], 0, "Stop the other."),
]
print("exam", len(EXAM))

CFG = dict(id="vectiq-user-guide", title="Running a Community with Vectiq: A User Guide",
    subtitle="Install, configure and operate the Vectiq bot: welcome, moderation, levels, events, tickets, games and keeping it healthy",
    description="A practical, beginner-friendly guide to using Vectiq (github.com/lucky-edgelord/aio-vector-bot, MIT), the community-management bot for the Vector messenger, based on its documentation at lucky-edgelord.github.io/aio-vector-bot. "
    "In 11 chapters you plan and install the bot, learn the configuration file, modules and setup wizard, welcome and verify new members, moderate day to day, protect the community with link safety, image guard and Sentire, run levels and a coin economy with a shop, schedule events, giveaways and polls, handle support tickets, add games, music and feed alerts, use the dashboard, webhooks and AI assistants, and finally keep it running with restore points, updates and troubleshooting. "
    "There are 22 numbered figures, 22 numbered tables, a recap, a memory trick, an expanded ELI5 and a concept map in every chapter, a command cheat sheet in the sandbox, a final exam, and a few short Python labs that run offline in the app. "
    "Credits: the course is original and follows the public documentation of Vectiq by lucky-edgelord and the Vectiq contributors (MIT licence). The documentation credits Logiq and MEE6 for feature shape, GateBot by henk.tech for verification ideas and Sentire by JSKitty of VectorPrivacy for automod. Settings and defaults may change as the project grows, so check the live documentation for the latest values.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, images=IMAGES)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "vectiq-user-guide.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
    print("figures", NFIG, "tables", NTAB)
