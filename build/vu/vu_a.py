# -*- coding: utf-8 -*-
"""Vectiq user guide course chapters."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *  # noqa
def F(n, cap): return {"type": "figure", "image": "vu-%s.svg" % n, "caption": cap}
def TB(title, head, rows): return {"type": "table", "title": title, "head": head, "rows": rows}
CHS = []

CHS.append(CH("Before you start: the plan and the install",
 ("Setup", ["Bot | needs | Own Vector account", "Bot | needs | Computer that stays on", "Install | via | Script", "Install | via | pipx", "Install | via | Docker", "Key | goes in | .env", "Test | is | !ping"]),
 ["Vectiq is a bot you run yourself. You put it on a computer that stays on, such as a Mac mini, a Linux server or a spare laptop, give it its own Vector account, and invite that account to your community. When the computer is off, the bot is off.",
  "Use a separate account for the bot. Its key sits in a file on the computer, and the account needs strong roles in your community, so never give it your personal key.",
  "The first install compiles a Rust core, which takes several minutes. After that, the goal is simple: the bot answers !ping."],
 [("Prefix", "The symbol before a command; the default is an exclamation mark."), ("nsec", "The secret key of a Vector account; the bot's key goes in VECTOR_NSEC."), ("Invite link", "A link that lets the bot join a community."), ("pipx", "A tool that installs Python programs in their own space."), ("Docker Compose", "A way to run the bot in a container with one command.")],
 ["You need a computer that stays on, Python 3.10 or newer, a separate bot account and admin rights in the community.", "install.sh handles macOS and Linux; install.ps1 handles Windows.", "pipx install works without cloning; Docker suits a server or NAS.", "The bot key goes in .env, which is never shared.", "Check it works with !ping."],
 [T("Think of hiring a helper for your clubhouse. You give the helper their own key card, not yours, and a desk that is always open. That is the whole idea of setting up Vectiq."),
  F("1-1", "The route from an empty computer to a bot that answers."),
  TB("What you need", ["Item", "Why"], [["a computer that stays on", "the bot keeps a connection open to Vector"], ["Python 3.10 or newer", "Vectiq is written in Python"], ["a bot-only Vector account", "keeps your own key safe"], ["admin rights in the community", "to invite the bot and give it roles"], ["rustc, cargo and cmake", "to build the Vector SDK the first time"]]),
  T("On a Mac or Linux, clone the code and run ./install.sh. It installs what is missing, makes a virtual environment, asks for the bot's key and invite links, offers the setup wizard, checks the config and starts the bot at login. Options like --no-service and --yes skip parts or questions."),
  C("git clone https://github.com/lucky-edgelord/aio-vector-bot\ncd aio-vector-bot\n./install.sh", "sh"),
  F("1-2", "Four ways to install."),
  TB("Install routes", ["Route", "Command", "Good for"], [["macOS and Linux", "./install.sh", "most people"], ["Windows", ".\\install.ps1", "uses winget; not yet tested on real machines"], ["pipx", "pipx install \"vectiq[dashboard,webhooks] @ git+https://github.com/lucky-edgelord/aio-vector-bot\"", "no clone"], ["Docker", "docker compose up -d", "server or NAS"]]),
  T("The Windows and Linux installers and the Mac login item are described by the project as not yet tested on real machines. If something is off, open an issue in the repository.")],
 [("Whose key does the bot use?", ["Its own account's key", "Your personal key", "A shared key", "No key"], 0, "Always a separate account."), ("What command checks the bot is alive?", ["!ping", "!hello", "!alive", "!bot"], 0, "The first test."), ("What does the first install build?", ["The Rust core of the SDK", "A website", "A game", "A database server"], 0, "Needs rustc, cargo, cmake."), ("Where does the key go?", [".env", "config.yaml", "Chat", "README"], 0, "VECTOR_NSEC."), ("Which Python version?", ["3.10 or newer", "2.7", "3.6", "Any"], 0, "Required.")],
 [("Why a separate account?", "The key lives on the computer and the account is powerful."), ("What if the computer sleeps?", "The bot is off until it wakes."), ("Which flag skips questions?", "--yes."), ("Where do logs go?", "data/vectiq.log or the service log.")],
 [MATCH("Match install route", "Pair each route with its command.", [("macOS and Linux", "./install.sh"), ("Windows", ".\\install.ps1"), ("server", "docker compose up -d"), ("no clone", "pipx install")]),
  FILL("First steps", "Give the bot its own {{account}}, put its key in {{.env}}, invite it, and test with {{!ping}}.")]))

CHS.append(CH("Configuration, modules and the setup wizard",
 ("Settings", ["Wizard | asks | Questions", "config.yaml | holds | Settings", "check | validates | Config", "reload | applies | Changes", "modules | switch | Features", "Dashboard | edits | Settings", "Restore point | before | Wizard save"]),
 ["Everything about how Vectiq behaves is in one file, config.yaml, and every setting has a comment next to it. The easiest start is the setup wizard, which asks one question per screen and writes your answers into the file, keeping the comments.",
  "To change a setting by hand: edit the file, check it with --check, and apply it with !vectiq reload. Turning a module on or off needs a restart.",
  "Each feature is a module with a switch. Switch off what you do not need, and its commands and background jobs stay idle."],
 [("config.yaml", "The main settings file with a comment for each setting."), ("Wizard", "A guided questionnaire that writes your config."), ("Reload", "Apply most changes without a restart."), ("Module switch", "A true or false under modules: for a feature."), ("Settings reference", "The documentation page listing every setting and default.")],
 ["Run the wizard with python -m vectiq --setup or from the dashboard.", "Check with --check; errors are plain sentences.", "!vectiq reload applies most changes; module switches need a restart.", "The old config is saved as config.yaml.bak.", "A restore point is made before the wizard saves."],
 [T("Imagine a control panel with a lot of switches and dials. The wizard walks you through them one at a time. Later you can fiddle by hand, with a safety net: a checker that tells you in words if you set a dial to a nonsense value."),
  F("2-1", "Pick the style that suits you; they all change the same settings."),
  C("modules:\n  leveling: true\n  economy: true\n  tickets: true\n  securitycam: false   # off by default\n\nevents:\n  timezone: America/New_York", "yaml"),
  T("For example, a typo such as an unknown time zone produces a message like events.timezone: unknown time zone, instead of a crash. This is why checking before applying is a good habit."),
  F("2-2", "Edit, check, apply."),
  TB("Ways to change settings", ["Where", "Best for", "Needs restart?"], [["setup wizard", "first setup", "after saving"], ["dashboard", "quick tweaks", "usually no"], ["config.yaml", "full control, version control", "module switches"], ["chat commands", "on-the-spot changes", "no"]]),
  TB("Config commands", ["Command", "Does"], [["python -m vectiq --check", "validate config"], ["python -m vectiq --setup", "run the wizard"], ["!vectiq reload", "apply most changes (bot owners)"], ["!module on NAME", "switch a module on"], ["vectiq --export-config / --import-config", "move settings between machines"]]),
  T("Dashboard changes are saved separately from the file and sit on top of it, as chapter 4 of the technical course explains. If you ever wonder why a value differs from the file, look at the dashboard.")],
 [("What validates the config?", ["--check", "--run", "--stop", "--zip"], 0, "Plain error messages."), ("What applies most changes?", ["!vectiq reload", "!restart all", "!apply", "nothing"], 0, "Bot owners only."), ("Does the wizard keep comments?", ["Yes", "No", "Only some", "It deletes the file"], 0, "And saves config.yaml.bak."), ("Do module switches need a restart?", ["Yes", "No", "Only on Mac", "Only on Docker"], 0, "Reload is not enough."), ("What is made before the wizard saves?", ["A restore point", "A new account", "A website", "Nothing"], 0, "So you can roll back.")],
 [("Where is every setting documented?", "The settings reference."), ("What if the check fails?", "Fix the named setting and check again."), ("What is the safest change loop?", "Edit, check, reload."), ("Can the dashboard change settings?", "Yes, and the audit log records it.")],
 [MATCH("Match config tool", "Pair each tool with its job.", [("--check", "validate"), ("--setup", "wizard"), ("!vectiq reload", "apply changes"), ("!module on", "switch a feature on")]),
  FILL("Safe changes", "{{Edit}} the file, {{check}} it, then {{reload}} the bot.")]))

CHS.append(CH("Welcoming members: welcome, verification, onboarding and role menus",
 ("Welcome", ["Welcome | greets | New member", "Verification | proves | Human", "Onboarding | chains | Steps", "Role menu | lets | Pick roles", "Placeholders | fill | Message", "Gate | hides | Unverified messages"]),
 ["Three modules look after a new member. Welcome greets them, verification checks they are a person, and onboarding walks them through the steps and lets them pick roles. You can use any one alone.",
  "Welcome messages use placeholders such as the member's mention and name, and !testwelcome shows a preview. Verification offers a question, a reaction or a CAPTCHA, and a gate can hide messages from people who have not verified yet.",
  "Role menus are messages where members react to take a role and unreact to drop it. Onboarding posts a menu built from your list of emoji and roles."],
 [("Placeholder", "A fill-in such as the member's name inside a message template."), ("Gate", "A setting that deletes messages from unverified members."), ("Lobby", "A separate community where people verify before being invited to the real one."), ("Role menu", "A message of emoji and roles that members react to."), ("Onboarding", "A sequence of steps for new members, by default verify then pick roles.")],
 ["Placeholders: {mention}, {name}, {community}, {count}.", "Verification modes: question, button, captcha.", "gate: off, channel or all; spam_kick softbans repeat offenders.", "Role menu: !rolemenus create Title | emoji=Role ...", "Onboarding default steps: verify, then pick_roles."],
 [T("Picture the door of a clubhouse. First someone says hello, then checks your ticket, then offers you a badge for your favourite hobby. That is welcome, verification and onboarding."),
  F("3-1", "The three modules can be used together or one at a time."),
  C("welcome:\n  enabled: true\n  channel: general\n  message: \"Welcome to {community}, {mention}! You are member #{count}.\"", "yaml"),
  F("3-2", "Placeholders are replaced when the message is sent."),
  TB("Welcome placeholders", ["Placeholder", "Becomes"], [["{mention}", "pings the member"], ["{name}", "their name"], ["{community}", "your community's name"], ["{count}", "the number of members"]]),
  T("Verification stores the result, so a member who loses the role or rejoins gets it back without checking again. For CAPTCHA mode you need a web address and a key from a CAPTCHA provider, and the secret goes in .env, never in config.yaml. Always run !verification to see anything that is missing."),
  TB("Gate, lobby and softban", ["Feature", "What it does"], [["gate: channel", "only the verification channel is open to unverified members"], ["gate: all", "every channel hides their messages"], ["spam_kick", "softban after that many gated messages in 15 minutes"], ["invite_to", "verify in a lobby, then invite to the real community"], ["min_age", "ask an age first; younger members are softbanned"]]),
  C("!rolemenus create Pick your roles | 🎮=Gamer 🎨=Artist 💻=Dev\n!rolemenus list\n!rolemenus delete 3", "text"),
  T("Use an underscore for a space inside a role name, so 🎵=Music_Lover makes a role called Music Lover. The bot needs permission to manage roles.")],
 [("What does !testwelcome do?", ["Previews the welcome message", "Bans someone", "Deletes channels", "Sends a DM to all"], 0, "Needs Manage Community."), ("What do members do to get a role?", ["React to the menu", "Type a password", "Pay coins", "Nothing"], 0, "Unreact to drop it."), ("Where does the CAPTCHA secret go?", [".env", "config.yaml", "chat", "the README"], 0, "Never in the YAML."), ("What is a lobby?", ["A separate community for verifying", "A role", "A game", "A log"], 0, "Then invited to the real one."), ("Default onboarding steps?", ["verify, pick_roles", "ban, kick", "pay, play", "none"], 0, "In that order.")],
 [("What replaces {count}?", "The number of members."), ("How do spaces work in role names?", "Use an underscore."), ("What does gate do?", "Hides or deletes messages from unverified members."), ("Which command shows verification problems?", "!verification.")],
 [MATCH("Match placeholder", "Pair each placeholder with its meaning.", [("{mention}", "pings the member"), ("{name}", "member's name"), ("{community}", "community name"), ("{count}", "member count")]),
  FILL("Greeting", "Use {{placeholders}} in the welcome message, preview with {{!testwelcome}}, and keep CAPTCHA secrets in {{.env}}."),
  PL("Fill in a welcome message", "Write render_welcome(template, name, community, count). Replace {name}, {community} and {count} in the template with the given values and return the result.", "render_welcome(template, name, community, count)", '''
def render_welcome(template, name, community, count):
    return (template.replace("{name}", name)
            .replace("{community}", community)
            .replace("{count}", str(count)))
''', [["Hi {name}, welcome to {community}!", "Sam", "Nebula", 5], ["You are member #{count}.", "Ana", "Club", 120], ["No fields", "x", "y", 1], ["{name} {name}", "Bo", "C", 2]], "Use replace for each placeholder; count must be turned into text."),
  PL("Read a role menu", "Write parse_role_menu(text). text has pairs like 'a=Gamer b=Music_Lover' separated by spaces. Return a list of [key, role] pairs, turning underscores in the role into spaces.", "parse_role_menu(text)", '''
def parse_role_menu(text):
    out = []
    for part in text.split():
        if "=" in part:
            k, v = part.split("=", 1)
            out.append([k, v.replace("_", " ")])
    return out
''', [["a=Gamer b=Artist"], ["x=Music_Lover"], [""], ["q=Big_Red_Team z=Dev"]], "Split on spaces, then on the first equals sign.")]))

CHS.append(CH("Moderation day to day",
 ("Moderation", ["Warn | adds | Case", "Threshold | triggers | Action", "Timeout | is | Temporary mute", "Tempban | lifts | Itself", "Softban | removes | On sight", "modlog | shows | Cases", "Purge | deletes | Messages", "Lock | stops | Sending"]),
 ["Every moderation action is stored as a numbered case, so you can see what happened, who did it and why. Commands need the matching Vector permission, so someone who cannot time people out in Vector cannot do it through the bot either.",
  "Warnings escalate. With the defaults, a third warning gives a one-hour timeout, and the same again at six and nine. You can change the action, the length, or turn escalation off.",
  "The bot refuses to act on you, on itself and on the community owner, and says so instead of failing quietly."],
 [("Case", "A numbered record of a moderation action."), ("Timeout", "A temporary mute, up to 28 days by default."), ("Tempban", "A ban that lifts itself after a set time."), ("Softban", "Removal that repeats whenever the member returns."), ("Purge", "Delete the last messages in a channel.")],
 ["!warn, !warnings, !delwarn, !clearwarns manage warnings.", "!timeout, !untimeout, !kick, !ban, !tempban, !softban, !unban act on members.", "Durations: 30m, 2h, 1d12h.", "!case, !history and !modlog look back; log_channel mirrors cases.", "!purge up to 100, !lock/!unlock, !slowmode N."],
 [T("A moderator's notebook has numbered pages. Each page says who, what, when and why. Warnings stack up, and a rule says what happens at the third page."),
  F("4-1", "With the defaults, every third warning triggers a one-hour timeout."),
  C("moderation:\n  warn_threshold: 3\n  warn_action: timeout   # timeout | kick | ban | none\n  warn_action_minutes: 60\n  log_channel: mod-log", "yaml"),
  TB("Member actions", ["Command", "Effect"], [["!warn @sam reason", "adds a warning case"], ["!timeout @sam 30m reason", "mutes for 30 minutes"], ["!kick / !ban", "removes or bans"], ["!tempban @sam 3d reason", "ban that ends in 3 days"], ["!softban @sam reason", "removed again every return"], ["!unban npub... reason", "lifts bans and softbans"]]),
  T("The bot checks for expired tempbans every 30 seconds. A softban becomes a real ban after the member comes back the number of times set by softban_escalate, three by default."),
  F("4-2", "Everyday tools for people, places and history."),
  TB("Looking back and cleaning up", ["Command", "Effect"], [["!case 12", "show one case"], ["!history @sam", "all cases for a member"], ["!modlog", "latest cases"], ["!purge 25", "delete last 25 messages"], ["!lock / !unlock", "stop or allow everyone sending"], ["!slowmode 10", "soft slowmode; staff exempt"]]),
  T("Communities still on Vector's legacy roster do not accept per-channel permission changes, so lock and unlock may not work until the community is upgraded.")],
 [("What happens at the third warning by default?", ["A one-hour timeout", "A ban", "Nothing", "A kick"], 0, "And again at six and nine."), ("What lifts a tempban?", ["The bot, on time", "A moderator", "Nothing", "The member"], 0, "Checked every 30 seconds."), ("Can the bot act on the owner?", ["No", "Yes", "Only kick", "Only warn"], 0, "It says so."), ("What does !purge 25 do?", ["Deletes 25 messages", "Bans 25", "Warns 25", "Mutes 25"], 0, "Up to 100."), ("Which shows a member's cases?", ["!history", "!lock", "!tempban", "!slowmode"], 0, "Lists every case.")],
 [("How do you stop escalation?", "Set warn_action to none."), ("Maximum timeout?", "28 days by default."), ("Where can cases be mirrored?", "moderation.log_channel."), ("Who can use mod commands?", "People with the matching Vector permission.")],
 [MATCH("Match command to effect", "Pair each command with what it does.", [("!warn", "adds a case"), ("!tempban", "ban that ends"), ("!history", "member's cases"), ("!purge", "deletes messages")]),
  FILL("Fair moderation", "Every action is a {{case}}, warnings escalate at the {{threshold}}, and a {{softban}} repeats on return."),
  PL("Does this warning trigger an action?", "Write warn_action(count, threshold). Return 'timeout' when count is at least 1 and is an exact multiple of threshold (3, 6, 9 for threshold 3), otherwise 'none'.", "warn_action(count, threshold)", '''
def warn_action(count, threshold):
    if count >= 1 and count % threshold == 0:
        return "timeout"
    return "none"
''', [[1, 3], [3, 3], [4, 3], [6, 3], [9, 3], [0, 3], [5, 5], [10, 5]], "Use the remainder operator.")]))

CHS.append(CH("Protecting your community: link safety, image guard and Sentire",
 ("Protection", ["Link safety | uses | Public blocklists", "Allow list | beats | Everything", "Image guard | uses | Blocklist", "Image guard | optional | Detector", "Sentire | is | Automod", "Actions | are | Log delete warn timeout", "Exempt | skips | Staff"]),
 ["Safety modules watch for trouble so you do not have to. Link safety removes links to scam, malware, phishing and tracking sites using public lists. Image guard blocks pictures you have flagged, and can score nudity with a detector. Sentire is the full automod.",
  "They share the same actions: log, delete, warn or timeout. Staff with Manage Messages and any exempt roles or channels are skipped.",
  "The golden rule for any new rule: start with action log, read the mod log for a few days, and only then switch to delete. No detector is perfect."],
 [("Blocklist", "A list of bad domains or pictures that are removed."), ("Allow list", "Domains that are never blocked."), ("Perceptual hash", "A picture fingerprint that survives resizing."), ("Detector", "A tool that scores a picture, for example for nudity."), ("Strike score", "Sentire's per-member score that decays over time.")],
 ["!module on linksafety downloads the lists on first start.", "allow beats everything; block beats the lists.", "Reply to a picture with !imageguard block reason to add it to the blocklist.", "Image detectors: off, nudenet, nsfw-detector, sightengine, http.", "Sentire and Sentire (official) share one slot; only one runs."],
 [T("A shop with a bouncer, a security camera and a lost-and-found. Link safety is the bouncer reading each label, image guard remembers faces of known troublemakers, and Sentire watches behaviour over time."),
  F("5-1", "Several layers, each catching different things."),
  C("linksafety:\n  nsfw: false\n  allow: [example-shortener.com]\n  block: [annoying.example]\n  action: log      # start gentle", "yaml"),
  TB("Link safety facts", ["Item", "Detail"], [["default list", "oisd big, about 230,000 domains"], ["catches", "links with or without https, and subdomains"], ["optional", "Google Safe Browsing key in .env"], ["test a link", "!linksafety check <link>"], ["offline", "a cached copy of the lists is used"]]),
  T("Image guard's blocklist needs nothing extra and works on resized or re-saved copies thanks to the fingerprint. Detectors run on your own computer or through an API, and the first check loads the model in the background so chat stays fast."),
  F("5-2", "Tune from gentle to firm."),
  TB("Choosing an image detector", ["Detector", "Runs", "Setup"], [["off", "-", "blocklist only"], ["nudenet", "your computer", "pip install vectiq[nudenet]"], ["nsfw-detector", "your computer", "TensorFlow and a model file"], ["sightengine", "their API", "account and keys in .env"], ["http", "your own API", "give a URL"]]),
  T("Sentire is a separate program by JSKitty of VectorPrivacy. Vectiq can build and run your own copy, or invite the official Sentire-001. It starts by only watching and reporting; you arm each action when you are ready.")],
 [("What should a new rule start with?", ["action log", "action ban", "action kick", "no testing"], 0, "Watch first."), ("Which list wins in linksafety?", ["allow", "block", "public", "none"], 0, "Allow beats everything."), ("What catches resized copies of a picture?", ["The perceptual hash", "The file name", "The time", "The size"], 0, "A fingerprint."), ("Who is skipped by safety rules?", ["Staff and exempt roles", "Everyone", "Nobody", "Bots only"], 0, "Manage Messages."), ("Can both Sentire modules run?", ["No, one slot", "Yes", "Only on Mac", "Only with Docker"], 0, "They share automod.")],
 [("Where does the Safe Browsing key go?", ".env."), ("How to test a link?", "!linksafety check."), ("Why log first?", "To see mistakes without hurting members."), ("Does Sentire start armed?", "No, it only watches at first.")],
 [MATCH("Match protection", "Pair each module with its job.", [("linksafety", "bad links"), ("imageguard", "pictures"), ("Sentire", "behaviour and raids"), ("allow list", "never blocked")]),
  FILL("Careful rules", "Start with action {{log}}, read the {{mod log}}, then switch to {{delete}}.")]))

CHS.append(CH("Levels, coins and the shop",
 ("Engagement", ["Chatting | earns | XP", "XP | becomes | Level", "Level | can grant | Role", "!daily | pays | Coins", "Streak | adds | Bonus", "Shop | sells | Items", "Items | can give | Roles"]),
 ["Members earn XP by chatting, and XP adds up to levels. Each level needs more than the last, so early levels come quickly. You can give a role at a level, such as a Regular role at level 5.",
  "The economy gives every member a wallet. They earn coins from daily rewards and work, keep savings in a bank, pay each other and buy items from a shop that can sell roles.",
  "The two systems are separate modules, so you can run either one alone."],
 [("XP", "Experience points from chatting; 15 to 25 at most once a minute by default."), ("Level reward", "A role granted automatically at a level."), ("Streak", "Consecutive daily claims; each extra day adds a bonus up to a cap."), ("Wallet and bank", "Cash on hand and savings."), ("Shop item", "Something members can buy, optionally giving a role.")],
 ["XP step n to n+1 costs 5n squared plus 50n plus 100; !levelcurve shows it.", "!rank and !leaderboard show cards; leveling.cards false gives plain text.", "!levelreward add 5 Regular gives a role at level 5.", "!daily pays 200; the streak continues if you claim again within 48 hours.", "!shop add 1500 Supporter | text role:Supporter makes an item that gives a role."],
 [T("Think of an arcade. You earn tickets for playing, tickets can be saved or spent on prizes, and a long visiting streak earns a little extra every day."),
  TB("How long to reach a level", ["Level", "Total XP", "At 20 XP a minute"], [["1", "100", "about 5 minutes"], ["5", "1,150", "about 1 hour"], ["10", "4,675", "about 4 hours"], ["20", "23,850", "about 20 hours"], ["30", "67,525", "about 56 hours"]]),
  F("6-1", "Chatting earns XP; daily and work earn coins."),
  C("!levelreward add 5 Regular\n!levelreward remove 5\n!levelcurve", "text"),
  T("Level-up messages go to the channel the member was typing in, or to one fixed channel if you set announce_channel. Channels where you do not want XP can be listed in no_xp_channels."),
  TB("Economy commands", ["Command", "Does"], [["!balance / !daily / !work", "look and earn"], ["!pay @sam 50", "send coins"], ["!deposit / !withdraw", "move to and from the bank"], ["!richest / !transactions", "leaderboard and your history"], ["!shop / !buy VIP / !inventory", "look, buy, see owned"], ["!addmoney @sam 1000", "admin gift; negative takes away"]]),
  F("6-2", "A shop item can give a role when bought."),
  C("!shop add 500 VIP | Gold name colour\n!shop add 1500 Supporter | Show your support role:Supporter\n!shop remove VIP", "text"),
  T("Games use the same wallet, so winners are paid with the same coins, and slots bets come from real balances.")],
 [("How often can XP be earned?", ["Once per cooldown, default 60 s", "Every message", "Once a day", "Never"], 0, "Spamming does not help."), ("How do you give a role at a level?", ["!levelreward add", "!rank", "!daily", "!shop"], 0, "Or in config."), ("When does a daily streak continue?", ["Within 48 hours", "Within 1 hour", "Never", "Weekly only"], 0, "Else restarts."), ("How does a shop item give a role?", ["role:Name in the description", "A separate command", "It cannot", "!giverole"], 0, "Created if missing."), ("Who can use !addmoney?", ["Administrators", "Everyone", "Nobody", "Only bots"], 0, "Negative takes away.")],
 [("Which shows next levels' XP?", "!levelcurve."), ("What command lists the richest?", "!richest."), ("How to turn off rank pictures?", "leveling.cards false."), ("Where is the starting balance set?", "economy.start_balance, 100 by default.")],
 [MATCH("Match engagement command", "Pair each command with what it does.", [("!rank", "shows a card"), ("!daily", "claims coins"), ("!buy", "spends coins"), ("!levelreward", "role at a level")]),
  FILL("Rewards", "Chatting earns {{XP}}, a long {{streak}} adds a bonus, and a shop item can give a {{role}}."),
  PL("Minutes to reach a level", "Write minutes_to_level(level, xp_per_min). Total XP for a level is the sum of 5*n*n + 50*n + 100 for n from 0 to level - 1. Return how many whole minutes at xp_per_min XP a minute are needed, rounding up.", "minutes_to_level(level, xp_per_min)", '''
def minutes_to_level(level, xp_per_min):
    total = 0
    for n in range(level):
        total += 5 * n * n + 50 * n + 100
    return (total + xp_per_min - 1) // xp_per_min
''', [[1, 20], [5, 20], [10, 20], [20, 20], [30, 20], [5, 25]], "Add the steps, then divide rounding up.")]))

CHS.append(CH("Events, giveaways, polls and analytics",
 ("Activities", ["Event | has | RSVP", "Event | has | Waitlist", "Event | sends | Reminders", "Event | can | Repeat", "Giveaway | picks | Random winners", "Poll | has | Numbered options", "Analytics | shows | Activity"]),
 ["Schedule an event with one message and members RSVP with a reaction. The bot posts it in your announcements channel, reminds people before it starts, and can repeat it. Set the community's time zone once so times come out right.",
  "Giveaways run for a set time with several winners and rerolls. Polls take two to nine options. Analytics shows messages, joins and leaves per day.",
  "All of these are quick to run from chat, and the dashboard shows entry counts and charts."],
 [("RSVP", "A reply saying you are going, maybe, or not."), ("Waitlist", "People beyond the capacity who move up if someone leaves."), ("Reroll", "Draw a replacement giveaway winner."), ("Time zone", "The clock an event's time is read in."), ("Banner", "The picture the bot draws or you attach for an event.")],
 ["!event create Title | when | length | description (title and time required).", "When can be friday 8pm, tomorrow 18:30, in 2h, 2026-11-20 20:00.", "Set the zone once: !event timezone America/New_York.", "Reminders default to 60 and 15 minutes before; a missed one over ten minutes late is skipped.", "!giveaway start 1h 2 Prize; !poll Q | A | B."],
 [T("Organising a party. You announce it, people tick yes or maybe, you remind them the day before, and if the room is small, extra guests wait in line and are let in if someone drops out."),
  F("7-1", "An event goes from post to repeat."),
  C("!event timezone America/New_York\n!event create Game night | friday 8pm | 2h | Bring snacks\n!event edit 4 capacity 8\n!event edit 4 repeat weekly", "text"),
  TB("Event settings and options", ["Item", "Detail"], [["who can create", "staff by default; events.who_can_create: everyone opens it"], ["length", "default 60 minutes; between 1 minute and 14 days"], ["reminders", "channel post and DMs; defaults 60 and 15 minutes"], ["repeat", "daily, weekly, biweekly, monthly, none"], ["image", "attach a picture or use the drawn banner"]]),
  T("Members react with the tick, thinking face or cross on the footer. The newest reaction wins, and taking it back clears the answer. They can also type !event rsvp 4 going."),
  F("7-2", "Quick tools for community activities."),
  TB("Giveaway commands", ["Command", "Does"], [["!giveaway start 1h 2 Nitro", "start, one hour, two winners"], ["!giveaway end ID", "finish now"], ["!giveaway reroll ID", "draw a replacement"], ["!giveaway cancel ID", "stop without winners"], ["!giveaway list", "see what is running"]]),
  T("Polls look like !poll Best colour? | Red | Green | Blue, and members vote with one tap. !analytics 30 shows a month of messages, joins and leaves per day plus the busiest channels.")],
 [("What is required to create an event?", ["Title and time", "Only a title", "Everything", "A picture"], 0, "Others are optional."), ("What fixes times that are hours off?", ["!event timezone", "!event fix", "!restart", "Nothing"], 0, "Default is UTC."), ("How many options may a poll have?", ["2 to 9", "1 to 3", "10 to 20", "Any"], 0, "Numbered reactions."), ("What does reroll do?", ["Draws a replacement winner", "Restarts", "Cancels", "Deletes"], 0, "After a giveaway ends."), ("What happens to RSVPs on repeat?", ["Fresh clean list", "Kept", "Deleted forever", "Doubled"], 0, "Old post kept as a record.")],
 [("Who can create events?", "Staff by default."), ("What does the waitlist do?", "Moves people up when a place opens."), ("How long is the longest event?", "14 days."), ("Where do events go?", "events.channel, matched loosely.")],
 [MATCH("Match activity command", "Pair each command with what it does.", [("!event create", "schedule"), ("!giveaway start", "begin a draw"), ("!poll", "ask a question"), ("!analytics", "activity numbers")]),
  FILL("Planning", "Set the {{time zone}} once, members RSVP with {{reactions}}, and extra people join the {{waitlist}}."),
  PL("Read an event line", "Write parse_event(text). text looks like 'title | when | length | description'. Return a list of four items [title, when, length, description], each stripped of spaces, with None for any part that is missing.", "parse_event(text)", '''
def parse_event(text):
    parts = [p.strip() for p in text.split("|")]
    out = []
    for i in range(4):
        out.append(parts[i] if i < len(parts) and parts[i] else None)
    return out
''', [["Game night | friday 8pm | 2h | Bring snacks"], ["Quiz | tomorrow 18:30"], ["Only title"], ["A | b | | desc"]], "Split on the bar and pad to four items."),
  PL("Is this a valid poll?", "Write poll_ok(text). text looks like 'Question | Option | Option'. Return True if there are between 2 and 9 options after the question, otherwise False.", "poll_ok(text)", '''
def poll_ok(text):
    parts = [p.strip() for p in text.split("|")]
    n = len(parts) - 1
    return 2 <= n <= 9
''', [["Best colour? | Red | Green | Blue"], ["Q | A"], ["Q | A | B"], ["Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9"], ["Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10"]], "Count the parts after the first.")]))

CHS.append(CH("Support tickets, security cam and role-based access",
 ("Support", ["Ticket | is | Private channel", "Ticket | claimed by | Staff", "Ticket | closed by | Command or reaction", "Transcript | keeps | Conversation", "Security cam | echoes | All messages", "Security cam | needs | Staff channel"]),
 ["Tickets give each request its own private channel. A member opens one, staff claim it, and when it is resolved anyone with access closes it. The conversation is kept as a transcript.",
  "The bot needs Manage Channels to create ticket channels. Name a support role, or only the bot and the opener can see a ticket.",
  "The security cam is a different tool: it copies every message from every channel into one staff channel. It is off by default, and you must think carefully about who can read that channel and whether members should know."],
 [("Ticket", "A private support channel for one request."), ("Claim", "A staff member says they are handling a ticket."), ("Transcript", "The saved messages of a ticket."), ("Support role", "The role that can see every ticket."), ("Security cam", "A staff channel that echoes the whole community.")],
 ["!tickets open reason; !tickets claim; !tickets close.", "A lock emoji reaction also closes a ticket.", "Settings: category, support_role, max_open_per_user, transcripts.", "!tickets transcript 12 reads a saved one.", "!securitycam set makes the current channel the cam."],
 [T("A help desk in a shop. Each customer gets a numbered booth. A staff member says I will take this one. When finished, the booth is cleared but the notes are filed."),
  F("8-1", "From opening to transcript."),
  C("tickets:\n  category: Support\n  support_role: Moderator\n  max_open_per_user: 2\n  transcripts: true", "yaml"),
  TB("Ticket commands", ["Command", "Who", "Does"], [["!tickets open reason", "member", "creates ticket-NN"], ["!tickets claim", "staff", "marks it handled"], ["!tickets close", "opener or staff", "closes and deletes the channel"], ["!tickets transcript 12", "staff", "reads the saved conversation"]]),
  T("Communities on the legacy roster do not accept per-channel permission settings, so Vectiq creates a plain private channel and grants access another way. You might see two similarly named channels in that case."),
  F("8-2", "The four main ticket settings."),
  TB("Security cam rules", ["Item", "Detail"], [["default", "off"], ["turn on", "modules.securitycam true, then !securitycam set"], ["left out", "its own channel, the bot's messages, other bots by default"], ["ignore", "securitycam.ignore_channels for private places"], ["warning", "everyone who can read the cam channel reads everything"]]),
  T("Make the camera channel staff-only and consider telling members it exists. Attachments are re-uploaded so they stay after the original is gone; files that cannot be copied are listed as links.")],
 [("Who sees a ticket?", ["Opener and the support role", "Everyone", "Only the bot", "Nobody"], 0, "Name a support_role."), ("What closes a ticket besides !tickets close?", ["A lock reaction", "A ban", "A poll", "Nothing"], 0, "Configurable emoji."), ("Is the security cam on by default?", ["No", "Yes", "Only on Mac", "Only for owners"], 0, "Privacy."), ("What permission creates ticket channels?", ["Manage Channels", "Ban Members", "Mention", "None"], 0, "Bot needs it."), ("Are transcripts kept after closing?", ["Yes, if enabled", "Never", "Only a day", "Only for staff"], 0, "transcripts true.")],
 [("What if there is no support_role?", "Only the bot and the opener can see it."), ("How do you stop the cam?", "!securitycam off."), ("How to ignore a private channel?", "securitycam.ignore_channels."), ("Where is a transcript shown?", "!tickets transcript or the dashboard.")],
 [MATCH("Match support item", "Pair each item with its meaning.", [("claim", "staff takes the ticket"), ("transcript", "saved conversation"), ("support_role", "sees all tickets"), ("security cam", "echoes everything")]),
  FILL("Help desk", "A ticket is a {{private}} channel, staff {{claim}} it, and the conversation is kept as a {{transcript}}.")]))

CHS.append(CH("Games, music and feed alerts",
 ("Fun", ["Game | is | WebXDC app", "Bot | is | Referee", "Music | needs | yt-dlp and ffmpeg", "Queue | holds | Songs", "Notifications | watch | Feeds", "Feeds | include | YouTube", "Feeds | include | Twitch", "Feeds | include | RSS"]),
 ["Games are small apps shared into the chat: Tic-Tac-Toe, Connect Four, trivia and slots. The bot is the referee, so a modified app cannot cheat. Winners earn coins from your economy.",
  "Music plays in voice channels with a queue, loops, shuffle, filters, vote-skips and a DJ role. It needs two extra tools, yt-dlp and ffmpeg.",
  "Notifications post in a channel when a YouTube channel uploads, a Twitch channel goes live, or any RSS feed has something new."],
 [("Referee", "The bot component that holds the true game state."), ("Queue", "The ordered list of songs waiting to play."), ("Feed", "A source of updates such as a YouTube channel."), ("Join when", "When the bot joins a game: opened or shared."), ("DJ role", "A role allowed to control the music.")],
 ["!game tictactoe, connect4, trivia, slots.", "!gamestats and !gameboard trivia show records.", "Music: pip install vectiq[music] plus ffmpeg; !module on music.", "!play, !skip, !queue, !shuffle, !volume 60.", "!notify add youtube @Name #videos."],
 [T("A games room has a referee who holds the dice and the scoreboard. Players can only say what they want to do. The referee makes it real."),
  F("9-1", "Games, music and alerts all run as modules."),
  C("!game tictactoe\n!game slots\n!gamestats\n!gameboard trivia", "text"),
  TB("The four games", ["Game", "How it plays"], [["Tic-Tac-Toe", "two seats, others watch, rematch allowed"], ["Connect Four", "two seats, rematch allowed"], ["Trivia", "lobby then eight timed questions; faster is better"], ["Slots", "bet real coins up to slots_max_bet"]]),
  T("If the app says retry, the bot only trusts frames that come straight from a player's own device. Opening the game again fixes it. With join_when set to opened, the bot joins only when someone opens a game, which saves resources."),
  TB("Music essentials", ["Command", "Does"], [["!play words or link", "queue a song or playlist"], ["!search", "show five results to pick"], ["!queue / !nowplaying", "see the list and progress"], ["!skip / !skipto 4 / !back", "move around"], ["!shuffle / !loop / !filter bassboost", "change playback"]]),
  F("9-2", "New feeds do not flood the channel."),
  C("notifications:\n  channel: announcements\n  feeds:\n    - {type: youtube, source: \"@SomeChannel\", channel: videos}", "yaml"),
  T("Twitch needs a free app from the Twitch developer console, with its client id and secret in .env. YouTube and RSS need no account. A YouTube live stream shows up when YouTube publishes its page.")],
 [("Who decides game state?", ["The bot", "Each player", "The relay", "Chance"], 0, "The referee."), ("What does music need besides vectiq[music]?", ["ffmpeg", "A printer", "Java", "Docker only"], 0, "And yt-dlp."), ("What happens to old feed items?", ["Remembered, not posted", "Posted all at once", "Deleted", "Sent by DM"], 0, "No flood."), ("What does a game 'retry' mean?", ["Reopen the app", "You are banned", "The bot is off", "Server is full"], 0, "Unverified frame."), ("What do slots bets use?", ["Real wallet coins", "Pretend coins", "XP", "Nothing"], 0, "Up to slots_max_bet.")],
 [("Where do Twitch keys go?", ".env."), ("How to see a trivia leaderboard?", "!gameboard trivia."), ("What starts music?", "!module on music then !play."), ("Which games have two seats?", "Tic-Tac-Toe and Connect Four.")],
 [MATCH("Match fun feature", "Pair each feature with its command.", [("game", "!game tictactoe"), ("music", "!play"), ("alerts", "!notify add"), ("record", "!gamestats")]),
  FILL("Fun", "The bot is the {{referee}}, music needs {{ffmpeg}}, and new feeds are {{remembered}} so there is no flood.")]))

CHS.append(CH("The dashboard, webhooks and AI assistants",
 ("Control", ["Dashboard | is | Web admin", "Dashboard | needs | HTTPS outside", "Sign in | by | Code or password", "Audit log | records | Changes", "Webhook | lets | Tools post in", "Events | mirror to | Channel", "MCP | lets | Assistant manage"]),
 ["The dashboard is a web page where staff manage the bot without typing commands. It is off by default: set modules.dashboard to true, restart, and open the address. Only admins of a served community and the bot's owners can sign in, by a one-time code sent by DM or by a username and password you create with a command.",
  "Webhooks let outside tools post into a channel with a secret URL, and mirror Vectiq events such as moderation actions into a channel.",
  "The MCP module lets an AI assistant such as Claude manage the community with a token. Treat that token like the bot's own key."],
 [("Dashboard", "A browser page for managing the bot."), ("Audit log", "A record of changes made through the dashboard."), ("Webhook", "A secret URL that lets another tool post a message."), ("MCP", "Model Context Protocol: lets an assistant use tools."), ("base_url", "The address people really use to reach the dashboard.")],
 ["Dashboard default port 8090 on 127.0.0.1.", "vectiq --add-user NAME --npub npub1... makes a login.", "Sign-in codes last 10 minutes; sessions 7 days.", "Webhook secrets are shown once; the bot stores only a hash.", "MCP listens on 127.0.0.1:8770 with a bearer token; read_only lets assistants look only."],
 [T("The dashboard is the control room with screens for every part of the community. Webhooks are doorbells that outside tools can ring. MCP is a key you hand to an assistant, so keep it safe."),
  F("10-1", "Several ways to run the same bot."),
  C("modules:\n  dashboard: true\ndashboard:\n  host: 127.0.0.1\n  port: 8090\n  base_url: \"http://localhost:8090\"", "yaml"),
  TB("Dashboard pages", ["Page", "Use"], [["Overview", "messages, joins, busiest channels"], ["Members", "search, level, coins, warnings"], ["Moderation", "cases, bans, log channel"], ["Leveling / Economy", "settings, shop, balances"], ["Tickets / Giveaways / Role menus", "manage and read"], ["Restore points / Setup wizard", "safety and setup (owners)"]]),
  T("To reach the dashboard from elsewhere, put HTTPS in front with Caddy or Tailscale and set base_url to the public address. A mismatch between http and https stops sign-in cookies from working."),
  F("10-2", "Steps before exposing the dashboard."),
  TB("Webhook fields", ["Field", "Meaning"], [["name", "unique name for the hook"], ["channel", "where it posts"], ["notify", "who is DMed the secret URL once"], ["events", "Vectiq events mirrored into the channel"]]),
  T("An MCP assistant can create channels, set permissions, give roles and moderate members, and everything it changes is in the audit log. With the token it can do anything the bot can, so use read_only when you only want answers.")],
 [("Is the dashboard on by default?", ["No", "Yes", "Only for owners", "Only on Mac"], 0, "Set modules.dashboard."), ("Who may sign in?", ["Community admins and bot owners", "Anyone", "Only members", "Only bots"], 0, "Others get the same answer as unknown."), ("How often is a webhook secret shown?", ["Once", "Always", "Never", "Daily"], 0, "Only a hash is stored."), ("What does MCP read_only do?", ["Allows looking only", "Hides the dashboard", "Stops the bot", "Locks the DB"], 0, "No changes."), ("What stops sign-in cookies?", ["http and https mismatch", "A long password", "Dark mode", "Too many members"], 0, "Set base_url correctly.")],
 [("Default dashboard port?", "8090."), ("How to make a dashboard login?", "vectiq --add-user."), ("Where is the audit log?", "On the dashboard."), ("Why HTTPS?", "To protect logins outside localhost.")],
 [MATCH("Match control surface", "Pair each with its use.", [("dashboard", "browser admin"), ("webhook", "outside tool posts in"), ("MCP", "AI assistant manages"), ("audit log", "record of changes")]),
  FILL("Control", "Put {{HTTPS}} in front of the dashboard, keep the MCP {{token}} private, and use {{read_only}} when you only want answers.")]))

CHS.append(CH("Keeping it running: restore points, updates and troubleshooting",
 ("Care", ["Restore point | saves | Everything but key", "Log | names | Problems", "Update | needs | Restore point first", "Service | restarts | Bot", "Docker | keeps | Data folders", "Troubleshooting | starts with | Log"]),
 ["A bot you rely on needs a routine. Restore points are zip snapshots of the database, config and settings, made on a schedule, before risky changes and by hand. Rolling back first makes a point of the current state, so you can undo it. The bot's key is never inside a restore point.",
  "Run the bot as a service so it starts at login or boot: launchd on macOS, a systemd user service on Linux, a scheduled task on Windows, or Docker Compose with restart enabled. Keep copies of restore points on another machine.",
  "When something is wrong, read the log first. Most problems are named there."],
 [("Service", "A background program the operating system starts and restarts for you."), ("Restore point", "A zip snapshot for rolling back."), ("Log", "The bot's running diary of what it did and what went wrong."), ("Rollback", "Return to an earlier restore point."), ("Compose", "Docker's way to run the bot with config and data folders.")],
 ["Restore points: every 24 hours, before risky changes, by hand.", "vectiq --backup text; --list-backups; --restore N with the bot stopped.", "Update: git pull and rebuild, or pipx upgrade vectiq.", "Logs: data/vectiq.log, journalctl --user -u vectiq -f, or docker compose logs -f.", "Only one Vector bot can run per process: stop the other copy."],
 [T("A shop owner locks up every night, keeps a copy of the accounts in a second building, and reads the day's notes when something looks odd. That routine is what keeps a bot healthy too."),
  F("11-1", "A simple routine for a healthy bot."),
  TB("Restarting by platform", ["Platform", "Restart", "Log"], [["macOS", "launchctl kickstart -k gui/$(id -u)/com.vectiq.bot", "tail -f data/vectiq.log"], ["Linux user service", "systemctl --user restart vectiq", "journalctl --user -u vectiq -f"], ["Windows", "Stop-ScheduledTask Vectiq; Start-ScheduledTask Vectiq", "Get-Content data\\vectiq.log -Wait"], ["Docker", "docker compose restart", "docker compose logs -f"]]),
  T("Before an update, make a restore point. In Docker, run the backup command with a label like before update, then pull and rebuild. Copy docker-data/restore-points off the machine for a real backup."),
  F("11-2", "Common problems and where to look."),
  TB("Troubleshooting guide", ["Problem", "Check"], [["bot does not answer", "is it in the community, the prefix, is the module on, permissions, communities list"], ["only one Vector bot per process", "stop the second copy"], ["no sign-in code", "right npub, DMs and message requests, or !dashboard"], ["event time wrong", "!event timezone"], ["game says retry", "reopen the app"], ["no cam echoes", "!securitycam shows a channel, module on"]]),
  T("When asking for help, include the relevant lines from the log and the output of vectiq --version. Never paste your .env or your keys.")],
 [("What is never inside a restore point?", ["The bot's key", "The database", "Config", "Pictures"], 0, "Keep your own copy of .env."), ("What should you read first when something is wrong?", ["The log", "The README", "Social media", "Nothing"], 0, "Most problems are named."), ("Which flag restores?", ["--restore N", "--undo", "--back", "--revert"], 0, "Stop the bot first."), ("What makes the bot start at login?", ["The installer's service", "Nothing", "A bookmark", "Chat"], 0, "launchd, systemd or a task."), ("What if two copies run?", ["Only one Vector bot per process", "Both work", "Double XP", "Nothing"], 0, "Stop the other.")],
 [("How often are scheduled points made?", "Every 24 hours by default."), ("Where do Docker backups live?", "docker-data/restore-points."), ("How to update with pipx?", "pipx upgrade vectiq."), ("Why copy backups elsewhere?", "A disk failure would take both.")],
 [MATCH("Match care task", "Pair each task with its tool.", [("snapshot", "restore point"), ("read problems", "the log"), ("start at boot", "service"), ("undo", "rollback")]),
  FILL("A routine", "Make a {{restore point}} before updating, read the {{log}} when stuck, and copy backups to {{another}} machine.")]))
