# -*- coding: utf-8 -*-
"""Vectiq course, chapters 7-13."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *  # noqa
from vq_a import F, TB

CHS = []

CHS.append(CH("Leveling: the XP curve and the level store",
 ("Leveling", ["Message | earns | XP", "XP | has | Cooldown", "XP | sums to | Level", "Curve | is | 5n squared plus 50n plus 100", "Level up | can give | Role reward", "Rank | shown as | Pillow card", "Leaderboard | ranks | Members", "LevelStore | owns | All SQL"]),
 ["Leveling rewards activity. Each message earns a random amount of XP, but only once per cooldown, so spamming does not help. Total XP decides your level.",
  "Vectiq uses the MEE6 curve: the XP to climb from level n to n+1 is 5n squared plus 50n plus 100. The total to reach a level is the sum of those steps. A short loop turns XP into a level and back.",
  "All the database work is in LevelStore; the cog only listens to messages, announces level-ups and draws rank cards with Pillow in a worker thread so the bot never lags."],
 [("XP", "Experience points earned by chatting."), ("Level", "A rank derived from total XP using the curve."), ("Cooldown", "The pause between XP awards, 60 seconds by default."), ("Role reward", "A role given automatically when a member reaches a level."), ("Leaderboard", "The ordered list of members by XP.")],
 ["Default XP per award is 15 to 25, with a 60 second cooldown.", "xp_for_level(level) = sum of 5n squared + 50n + 100 for n below level.", "award() runs in a transaction and returns the rank and whether the member levelled up.", "A message in cooldown still counts but earns no XP.", "Rank cards are drawn with Pillow off the main loop."],
 [T("Think of a video game. Early levels are quick, later levels take longer. A formula decides how much extra each level costs, and every player follows the same formula."),
  C("def xp_for_level(level):\n    return sum(5*n*n + 50*n + 100 for n in range(level))\n\n# level 1 = 100, level 2 = 255, level 3 = 475", "python"),
  F("7-1", "Totals needed for levels 1 to 10 grow steadily."),
  T("Finding a level from XP is the reverse: keep adding the cost of the next level until you run out. The Rank record holds the level, the XP into the level and the span of that level, which is exactly what a progress bar needs."),
  TB("Leveling settings", ["Setting", "Default"], [["xp_min", "15"], ["xp_max", "25"], ["cooldown_seconds", "60"], ["no_xp_channels", "a list of quiet channels"]]),
  F("7-2", "The steps from a message to a role reward."),
  TB("LevelStore methods", ["Method", "Does"], [["award", "give XP if off cooldown; returns rank and level-up flag"], ["add_xp", "adjust XP by hand, never below zero"], ["rank", "level, XP and position (members ahead plus one)"], ["leaderboard / many", "top members or a batch"], ["reset", "start over"], ["set_reward / remove_reward / rewards", "manage level roles"]]),
  T("Notice how the design follows chapter 2. The store contains the maths and SQL, the cog contains Vector and Pillow, and the pure formula can be tested with plain numbers.")],
 [("Default XP per award?", ["15 to 25", "1 to 5", "100", "50 to 500"], 0, "xp_min and xp_max."), ("Why a cooldown?", ["Stops spam farming", "Saves disk", "Looks nicer", "Required by Vector"], 0, "Fair XP."), ("Where is the maths?", ["Level store", "The cog", "The dashboard", "Pillow"], 0, "Stores hold logic and SQL."), ("What draws rank cards?", ["Pillow", "SQLite", "FastAPI", "YAML"], 0, "The render layer."), ("Total XP for level 2?", ["255", "100", "55", "500"], 0, "100 plus 155.")],
 [("Formula for one level step?", "5n squared plus 50n plus 100."), ("Why draw cards in a thread?", "Image work is slow and blocks the loop."), ("What is rank position?", "Members ahead plus one."), ("What does award return?", "The rank and whether the member levelled up.")],
 [MATCH("Match leveling term", "Pair each term with its meaning.", [("XP", "points for activity"), ("cooldown", "pause between awards"), ("role reward", "role at a level"), ("leaderboard", "ranking list")]),
  FILL("The curve", "Total XP to reach a level is the {{sum}} of the step costs, and a {{cooldown}} stops spam.", ),
  PL("XP needed for a level", "Write xp_for_level(level). Total XP needed to reach that level is the sum over n from 0 up to level - 1 of 5*n*n + 50*n + 100. Level 0 needs 0.", "xp_for_level(level)", '''
def xp_for_level(level):
    total = 0
    for n in range(level):
        total += 5 * n * n + 50 * n + 100
    return total
''', [[0], [1], [2], [3], [10]], "Loop n from 0 to level - 1 and add the formula."),
  PL("Level for XP", "Write level_for_xp(xp). Return the highest level whose total XP is not more than xp, using the same curve (5*n*n + 50*n + 100 for each step from level n to n+1).", "level_for_xp(xp)", '''
def level_for_xp(xp):
    level = 0
    cost = 100
    while xp >= cost:
        xp -= cost
        level += 1
        cost = 5 * level * level + 50 * level + 100
    return level
''', [[0], [99], [100], [254], [255], [3720]], "Keep subtracting the cost of the next level while you can afford it.")]))

CHS.append(CH("Economy: coins, daily streaks and atomic money",
 ("Economy", ["Wallet | has | Balance and bank", "Wallet | cannot be | Negative", "adjust | raises on | Insufficient funds", "transfer | is | Atomic", "daily | has | Streak", "work | has | Cooldown", "Shop | sells | Items", "buy | is | Atomic"]),
 ["The economy gives members coins to earn and spend. Money code must be careful, because a bug can create or destroy coins. So every change happens inside a database transaction, and the wallet table refuses negative balances as a last line of defence.",
  "Members claim a daily reward that grows with a streak, work for coins on a cooldown, pay each other, keep coins in a bank, and buy items from a shop.",
  "Two ideas matter most. Atomic operations: a transfer or a purchase either completes entirely or not at all. And injectable time and randomness: the daily and work functions accept a clock and a random function, so tests are exact."],
 [("Atomic", "Indivisible: it all happens or none of it does."), ("Streak", "Consecutive days a member has claimed the daily reward."), ("Wallet", "A member's balance, bank and history."), ("InsufficientFunds", "The error raised when a member cannot afford something."), ("Injectable", "Passed in as a parameter so tests can control it.")],
 ["Defaults: daily 200, streak bonus 25 up to a cap of 10, work 40 to 120 every 30 minutes, start balance 100.", "adjust raises InsufficientFunds rather than going below zero.", "transfer moves coins between two members in one transaction.", "buy charges, reduces stock, updates inventory and logs, all together.", "Time and randomness are injected for testing."],
 [T("Imagine two friends passing a banknote. If one lets go before the other grabs it, the note falls. A transaction is the rule that says hold on until the other side has it."),
  F("8-1", "A transfer changes both wallets and the log together, or nothing."),
  T("The daily reward rewards loyalty. Claim within two days of the last claim and your streak continues; miss longer and it restarts at one. The payout is the base amount plus the bonus times the streak length minus one, with that multiplier capped."),
  F("8-2", "With the defaults, the streak reaches its cap on day 11."),
  TB("Economy defaults", ["Setting", "Default"], [["daily_amount", "200"], ["daily_streak_bonus", "25"], ["daily_streak_cap", "10"], ["work", "40 to 120 coins"], ["work_cooldown_minutes", "30"], ["start_balance", "100"]]),
  TB("Economy commands", ["Command", "Does"], [["balance", "show wallet"], ["daily / work", "earn coins"], ["pay", "send coins to a member"], ["deposit / withdraw", "move between wallet and bank"], ["richest", "leaderboard"], ["transactions", "recent history"]]),
  T("Every adjustment is also written to a transactions table with a reason. If a member asks where their coins went, the history answers, and the sum of the log matches the balance.")],
 [("What happens on insufficient funds?", ["An error is raised", "Balance goes negative", "Silent success", "Coins are created"], 0, "InsufficientFunds."), ("Why are transfers atomic?", ["No half-moved coins", "Speed", "Style", "Fewer commands"], 0, "All or nothing."), ("Default daily amount?", ["200", "20", "2000", "0"], 0, "daily_amount."), ("What caps the bonus?", ["daily_streak_cap", "work_cooldown", "start_balance", "winner_coins"], 0, "Cap 10."), ("Why inject time?", ["Exact tests", "Speed", "Style", "Security"], 0, "Tests can set the clock.")],
 [("Day 11 payout with defaults?", "200 plus 25 times 10, which is 450."), ("What if you miss two days?", "The streak restarts at one."), ("Why log transactions?", "So balances can be audited."), ("What guards against negative balance?", "adjust raises, plus a CHECK in the table.")],
 [MATCH("Match economy term", "Pair each term with its meaning.", [("atomic", "all or nothing"), ("streak", "consecutive daily claims"), ("bank", "safe store of coins"), ("shop", "items for coins")]),
  FILL("Safe money", "A transfer is {{atomic}}, a missed day resets the {{streak}}, and a spend you cannot afford raises {{InsufficientFunds}}."),
  PL("Daily payout", "Write daily_pay(amount, bonus, cap, streak). Return amount + bonus * min(streak - 1, cap).", "daily_pay(amount, bonus, cap, streak)", '''
def daily_pay(amount, bonus, cap, streak):
    return amount + bonus * min(streak - 1, cap)
''', [[200, 25, 10, 1], [200, 25, 10, 2], [200, 25, 10, 11], [200, 25, 10, 30], [100, 10, 3, 5]], "Cap the streak bonus multiplier at cap."),
  PL("Next streak", "Write next_streak(hours_since, streak). If hours_since is 48 or less the streak continues, so return streak + 1; otherwise it restarts, so return 1.", "next_streak(hours_since, streak)", '''
def next_streak(hours_since, streak):
    if hours_since <= 48:
        return streak + 1
    return 1
''', [[20, 3], [48, 3], [49, 3], [100, 9], [1, 0]], "A simple comparison against 48 hours.")]))

CHS.append(CH("Moderation, durations and the safety modules",
 ("Moderation", ["Case | records | Action", "Case | can | Expire", "Warnings | reach | Threshold", "Threshold | triggers | Timeout", "enforce | applies | Actions", "exempt | skips | Staff", "linksafety | checks | Domains", "imageguard | checks | Pictures"]),
 ["Moderation keeps a permanent record. Every warning, timeout, kick and ban is stored as a case with a number, the member, the moderator, a reason and, for temporary actions, an expiry time. Tempbans lift themselves when the time comes.",
  "Other safety modules share one engine called enforce. A link or a picture that breaks the rules triggers an action from a short ladder: log, delete, warn or timeout. Staff and exempt roles and channels are skipped.",
  "Durations such as 90m, 1h30m and 2d are parsed by a shared helper. A bare number means minutes."],
 [("Case", "A numbered moderation record."), ("Warning threshold", "The number of active warnings that triggers an automatic action."), ("Exempt", "Staff, roles or channels the safety rules skip."), ("Perceptual hash", "A fingerprint of a picture that stays similar when it is resized."), ("Blocklist", "A list of domains or pictures that are removed.")],
 ["Cases store expires_at and active; due_expiries finds what to lift.", "Default: three warnings trigger a timeout.", "enforce never raises and escalates through the moderation cog.", "Link safety uses public domain lists such as oisd and optional Safe Browsing.", "Image guard matches known pictures and can score nudity with a detector."],
 [T("A school keeps a behaviour book. Each entry has a date, a name and a reason, and some entries fade after a while. A moderation case file is exactly that, and the same book is shared by every safety rule."),
  F("9-1", "Safety modules choose from the same short ladder of actions."),
  TB("A moderation case", ["Field", "Meaning"], [["id", "case number"], ["user and moderator", "who and by whom"], ["kind", "warn, timeout, kick, ban..."], ["reason", "free text"], ["created_at / expires_at", "when, and when it lifts"], ["active", "still counts?"]]),
  T("Link safety finds every domain in a message, with or without https. It checks the allow list first, then the block list, then the downloaded public lists. A subdomain of a listed site is caught by checking each parent in turn."),
  F("9-2", "Allow beats everything; block beats the lists."),
  TB("The safety modules", ["Module", "Looks at", "Typical action"], [["moderation", "members", "warn, timeout, kick, ban"], ["linksafety", "links", "delete and say why"], ["imageguard", "pictures", "delete, remember fingerprint"], ["sentire", "behaviour over time", "strike score, raid containment"]]),
  T("Always try a new rule with action log first, read the mod log for a few days, and only then switch to delete or timeout. No detector is perfect, and a rule that never deletes can never harm a good member.")],
 [("What does a case record?", ["A moderation action", "A game score", "A coin", "A channel"], 0, "Warn, timeout, kick, ban."), ("Default warning threshold?", ["3", "1", "10", "0"], 0, "Then a timeout."), ("Does enforce raise errors?", ["Never", "Always", "Sometimes", "Only for owners"], 0, "It is safe to call."), ("Which wins in linksafety?", ["allow", "block", "oisd", "random"], 0, "Allow beats everything."), ("What does a bare 30 mean in a duration?", ["30 minutes", "30 seconds", "30 days", "an error"], 0, "Bare number is minutes.")],
 [("Why try action log first?", "To watch for mistakes without hurting members."), ("What is a perceptual hash?", "A picture fingerprint tolerant of small changes."), ("What lifts a tempban?", "A loop that finds due expiries."), ("Who is exempt?", "Staff, exempt roles and exempt channels.")],
 [MATCH("Match action to effect", "Pair each action with what it does.", [("log", "tell the mod log only"), ("delete", "remove the message"), ("warn", "also adds a warning"), ("timeout", "also mutes the member")]),
  FILL("Safe rules", "Staff are {{exempt}}, new rules start with action {{log}}, and three {{warnings}} trigger a timeout."),
  PL("Parse a duration", "Write parse_duration(text). Return seconds for text such as 90m, 1h30m, 2d, 45s or a bare number (minutes). Units: d, h, m, s. Return -1 for anything that cannot be read.", "parse_duration(text)", '''
def parse_duration(text):
    text = text.strip().lower()
    if not text:
        return -1
    if text.isdigit():
        return int(text) * 60
    units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    total = 0
    num = ""
    for ch in text:
        if ch.isdigit():
            num += ch
        elif ch in units and num:
            total += int(num) * units[ch]
            num = ""
        else:
            return -1
    if num:
        return -1
    return total
''', [["90m"], ["1h30m"], ["2d"], ["45s"], ["15"], ["abc"], ["1h30"], [""]], "Collect digits, and when a unit letter arrives multiply and add."),
  PL("Is a domain listed", "Write listed(domain, blocked). blocked is a list of domains. Return the first entry that equals the domain or is one of its parent domains (for a.b.example.com check a.b.example.com, b.example.com, then example.com, never just com). Return None if there is no match.", "listed(domain, blocked)", '''
def listed(domain, blocked):
    parts = domain.split(".")
    for i in range(len(parts) - 1):
        cand = ".".join(parts[i:])
        if cand in blocked:
            return cand
    return None
''', [["a.b.example.com", ["example.com"]], ["example.com", ["example.com"]], ["safe.org", ["example.com"]], ["x.com", ["com"]], ["a.b.example.com", ["b.example.com", "example.com"]]], "Try the whole name, then drop the leftmost part each time.")]))

CHS.append(CH("Verification: keeping bots out",
 ("Verification", ["Verification | has | Modes", "Modes | include | Question", "Modes | include | Button", "Modes | include | Captcha", "Result | is | Stored", "Role | restored on | Rejoin", "Device check | uses | HMAC marks", "on_duplicate | decides | Refuse kick softban"]),
 ["New members must prove they are people before they can join in. Vectiq offers three modes: answer a small sum, react with a tick, or pass a CAPTCHA on a personal web page.",
  "The result is stored in the database, not just as a role. So if a member loses the role or leaves and rejoins, they get it back without checking again.",
  "Against fake accounts, a device check keeps scrambled markers of the IP address, a cookie and the browser. A second account from the same device is stopped. The markers are keyed with a secret only your bot knows, so they cannot be reversed. Ideas come from GateBot by henk.tech (MIT)."],
 [("CAPTCHA", "A small test that is easy for people and hard for programs."), ("HMAC", "A keyed hash: the same input and secret give the same code, but nobody without the secret can recreate it."), ("Fingerprint", "A browser signal used as an anti-abuse hint, not proof of identity."), ("Softban", "Kick on sight, kept in Vectiq's database instead of a ban on the relay."), ("Lobby", "A holding area for members who have not yet verified.")],
 ["Modes: question, button, captcha.", "Verification is stored in verified_members, with method and an adult flag.", "Device marks are HMAC hashes kept for device_check_days (30).", "try_mark_device_verified checks and inserts in one transaction.", "on_duplicate: refuse, kick or softban."],
 [T("A nightclub bouncer checks your ID once, stamps your hand, and remembers you. If you lose the stamp, he looks you up. He also notices if the same person tries to enter again under a second name."),
  F("10-1", "Three ways to verify, and all of them are remembered."),
  TB("Verification modes", ["Mode", "What the member does", "Best for"], [["question", "answers a small sum", "small communities"], ["button", "reacts with a tick", "least effort, weakest"], ["captcha", "opens a personal link and passes a CAPTCHA", "spam-prone communities"]]),
  T("The CAPTCHA link is personal, works once, and expires after ten minutes. A new link cancels the old one. It is sent by direct message; if DMs are closed, it is posted in the channel and deleted after a minute."),
  F("10-2", "Markers are scrambled with a secret, and checked and saved in one transaction."),
  TB("When a device repeats", ["on_duplicate", "Result"], [["refuse", "the page says no; staff can verify by hand"], ["kick", "the second account is removed but may rejoin"], ["softban", "removed, and removed again whenever it returns"]]),
  T("Two tabs racing to verify could both pass a naive check. Doing the check and the insert inside one BEGIN IMMEDIATE transaction closes that gap, which is the same pattern as the money code in chapter 8.")],
 [("Where is verification stored?", ["In the database", "Only as a role", "In .env", "Nowhere"], 0, "Restores the role after rejoin."), ("Why use HMAC for device marks?", ["Cannot be reversed without a secret", "Faster", "Shorter", "Prettier"], 0, "Privacy and security."), ("Which mode needs a web address?", ["captcha", "question", "button", "all"], 0, "A personal page."), ("What does refuse do?", ["Blocks the second account", "Bans the first", "Deletes the role", "Nothing"], 0, "Staff can verify by hand."), ("How long do marks last?", ["30 days by default", "1 hour", "Forever", "1 minute"], 0, "device_check_days.")],
 [("Why store the result?", "So rejoining or losing the role needs no recheck."), ("What is in a device mark?", "A keyed hash of IP, cookie or fingerprint."), ("Why one transaction?", "So two tabs cannot both pass."), ("Who inspired this?", "GateBot by henk.tech, MIT.")],
 [MATCH("Match verification term", "Pair each term with its meaning.", [("question", "answer a sum"), ("captcha", "personal web test"), ("softban", "kick on sight"), ("HMAC", "keyed hash")]),
  FILL("Fair entry", "A {{device}} check stops second accounts, the result is {{stored}} in the database, and a {{softban}} kicks on sight."),
  PL("Device already used?", "Write seen(hashes, marks, now, days). marks is a dict from hash to the time (in seconds) it was recorded. Return True if any of the hashes is in marks and was recorded within the last days days (age less than or equal to days * 86400), otherwise False.", "seen(hashes, marks, now, days)", '''
def seen(hashes, marks, now, days):
    for h in hashes:
        t = marks.get(h)
        if t is not None and now - t <= days * 86400:
            return True
    return False
''', [[["a", "b"], {"b": 100}, 200, 1], [["a"], {"a": 0}, 86400, 1], [["a"], {"a": 0}, 86401, 1], [[], {"a": 1}, 5, 30], [["x"], {}, 5, 30]], "Look each hash up and compare its age with the window.")]))

CHS.append(CH("Games: a WebXDC referee",
 ("Games", ["Game | runs as | WebXDC app", "App | talks via | Realtime channel", "Bot | is | Referee", "Rules | are | Pure Python", "TwoPlayerGame | handles | Seats and turns", "Packager | builds | Deterministic zip", "Sender | must be | Verified", "Outcome | pays | Coins"]),
 ["Vectiq games are small web apps that run inside the chat. The command game tictactoe shares the app, and the bot joins the same realtime channel as the referee.",
  "The players' apps only show the board and send moves. The bot holds the true state, checks whose turn it is, applies the pure rules and sends back the new state. Nobody can cheat from their phone, because the phone never decides anything.",
  "Winners can earn coins through a small Bank interface that adapts the economy, so game rules never import the economy directly."],
 [("WebXDC", "A tiny web app packaged as a zip that opens inside a chat."), ("Realtime channel", "A live two-way connection between the apps and the bot."), ("Referee", "The component that owns the true game state."), ("Outcome", "The result of a finished game: winner, draw and coin payouts."), ("Deterministic build", "Building the same input always produces identical bytes.")],
 ["Game base class: state(), async handle(who, msg), optional tick and left.", "TwoPlayerGame handles hello, join, rematch and move.", "Games: tictactoe, connect4, trivia, slots.", "The packager uses a fixed timestamp so the zip is reproducible.", "Unverified senders are asked to try again."],
 [T("In a board game with a referee, players say what they want to do and the referee moves the pieces. If you shout that you won, the referee still checks. The Vectiq bot plays this referee."),
  F("11-1", "Apps send moves; only the bot decides."),
  T("A game moves through a simple conversation. Each app sends a hello, the bot answers with the current state, a player sends a move, the rules accept or reject it, and the bot sends the new state to everyone. When someone wins, an Outcome pays out coins."),
  F("11-2", "Typical messages in a game."),
  TB("Message types", ["Message", "From", "Meaning"], [["hello", "app", "I am here, show me the state"], ["join", "app", "take a seat"], ["move", "app", "my action"], ["state", "bot", "the whole truth right now"], ["error", "bot", "that move was refused"], ["rematch", "app", "play again"]]),
  TB("The games", ["Game", "Idea"], [["tictactoe", "three in a row, 3 by 3"], ["connect4", "four in a row, 6 by 7"], ["trivia", "timed questions, ticked each second"], ["slots", "one player, bets up to a limit"]]),
  C("LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]\n\ndef winner(board):\n    for a, b, c in LINES:\n        if board[a] and board[a] == board[b] == board[c]:\n            return board[a]\n    return None", "python"),
  T("The packager gives each app an id like vectiq-tictactoe and builds its zip with a fixed timestamp. A digest of the bytes tells the bot whether an app changed, so it shares the new version only when needed.")],
 [("Who decides game state?", ["The bot", "Each phone", "The relay", "Nobody"], 0, "The referee."), ("Why pure rules?", ["Easy tests", "Faster network", "Smaller zip", "Prettier"], 0, "No network, no Vector."), ("What does the packager guarantee?", ["Identical bytes each build", "Encryption", "Compression only", "Updates"], 0, "Fixed timestamp."), ("What is a Bank?", ["An interface to the economy", "A table", "A game", "A server"], 0, "Keeps rules independent."), ("What happens to unverified senders?", ["Asked to retry", "Banned", "Allowed", "Ignored forever"], 0, "The client retries.")],
 [("Why can't players cheat?", "The bot checks turns and applies the rules."), ("What does tick do?", "Advances time-based games like trivia."), ("What is a digest used for?", "Detecting that an app changed."), ("What do games pay with?", "Coins from the economy via Bank.")],
 [MATCH("Match game part", "Pair each part with its job.", [("referee", "owns true state"), ("rules", "pure Python"), ("packager", "builds the zip"), ("Bank", "pays coins")]),
  FILL("Fair play", "The bot is the {{referee}}, the rules are {{pure}} Python, and the app is a {{WebXDC}} zip."),
  PL("Tic-tac-toe winner", "Write winner(board). board is a list of 9 items: 'X', 'O' or '' (empty), read row by row. Return 'X' or 'O' if that player has three in a row, 'draw' if the board is full with no winner, otherwise None.", "winner(board)", '''
def winner(board):
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a, b, c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return "draw"
    return None
''', [[["X","X","X","","O","O","","",""]], [["O","","","O","X","","O","X","X"]], [["X","O","X","X","O","O","O","X","X"]], [["","","","","","","","",""]], [["X","","O","","X","","O","","X"]]], "Check the eight lines, then check for a full board.")]))

CHS.append(CH("Running it: restore points, dashboard, MCP and deployment",
 ("Operations", ["Restore point | is | Zip file", "Restore point | holds | Database", "Rollback | makes | Safety point first", "Dashboard | is | FastAPI", "MCP | lets | AI manage", "Webhooks | send | Events", "CLI | runs | Check and backup", "Docker | packages | Bot"]),
 ["Running a bot means planning for mistakes. Restore points are zip files holding the database, config, settings and event pictures. They are made on a schedule, automatically before risky changes such as upgrades, and by hand. Rolling back first makes a point of the current state, so a rollback can be undone.",
  "You can control the bot from chat commands, from the FastAPI dashboard, or from an AI assistant over MCP. The MCP server can be put in read-only mode, and everything an assistant does is in the audit log.",
  "The bot's key in .env is never put in a restore point, so a downloaded backup cannot be used to take over the bot."],
 [("Restore point", "A zip snapshot of everything the bot keeps, except its secret key."), ("Dashboard", "A web admin page served by the bot."), ("MCP", "Model Context Protocol: a standard way for an AI assistant to call tools."), ("Webhook", "An HTTP message the bot sends out when something happens."), ("Audit log", "A record of who changed what.")],
 ["Points are made on a schedule (every 24 hours), before risky changes, and by hand.", "The newest 14 automatic and 20 manual points are kept.", "Rollback first saves the current state.", "MCP runs on 127.0.0.1 with a bearer token; read_only lets assistants look only.", "CLI: --check, --backup, --list-backups, --restore, --modules, --mcp."],
 [T("A restore point is like a save game. You save before a risky level, you save on a timer, and loading an old save never throws away your current progress because it makes a new save first."),
  F("12-1", "A restore point holds the database, config, settings and pictures."),
  TB("When points are made", ["When", "How"], [["on a schedule", "every backup.every_hours (24)"], ["before risky changes", "import settings, save wizard, upgrade database, rollback"], ["by hand", "!restorepoint create, dashboard, or vectiq --backup"]]),
  T("The dashboard is a FastAPI app with pages for settings, modules, channels and roles, restore points and live logs. It needs the dashboard extra and should sit behind HTTPS if it is reachable from outside."),
  F("12-2", "All control surfaces end up in the same stores."),
  TB("Command line", ["Flag", "Does"], [["--check", "validate config"], ["--init", "write a starter config"], ["--setup", "run the wizard"], ["--backup / --list-backups / --restore", "restore points"], ["--modules", "list modules"], ["--new-module NAME", "scaffold a plugin"], ["--mcp", "stdio MCP bridge"]]),
  T("An MCP assistant can create channels, set permissions, give roles and moderate members. Treat its token like the bot's key: with it, an assistant can do anything the bot can. Use read_only whenever you only want answers.")],
 [("Is the bot key in a restore point?", ["Never", "Always", "Sometimes", "Only manual"], 0, "Kept in .env."), ("What does rollback do first?", ["Saves a point of now", "Deletes data", "Restarts Rust", "Nothing"], 0, "So it can be undone."), ("What does read_only do in MCP?", ["Allows looking only", "Deletes tools", "Hides logs", "Locks the DB"], 0, "No changes."), ("What serves the dashboard?", ["FastAPI", "Django", "Rails", "Node"], 0, "dashboard extra."), ("Which flag lists restore points?", ["--list-backups", "--logs", "--points-off", "--zip"], 0, "Then --restore N.")],
 [("Three ways points are made?", "Schedule, automatic before risky changes, by hand."), ("Where are points kept?", "data/restore-points as zip files."), ("Why HTTPS for the dashboard?", "To protect logins outside localhost."), ("What does MCP stand for?", "Model Context Protocol.")],
 [MATCH("Match operations term", "Pair each term with its meaning.", [("restore point", "zip snapshot"), ("dashboard", "web admin"), ("MCP", "AI tool protocol"), ("webhook", "event pushed out")]),
  FILL("Safe operations", "Make a {{restore point}} before risk, protect the {{dashboard}} with HTTPS, and use {{read_only}} MCP when you only need answers.")]))

CHS.append(CH("Testing and writing your own plugin",
 ("Plugins", ["Plugin | defines | MODULE", "Plugin | defines | setup", "Plugin | imports | vectiq.plugin", "Plugin | adds | Cog", "Tests | use | In-memory DB", "Tests | use | fake_community", "pytest | runs | asyncio auto", "New module | scaffolded by | CLI"]),
 ["The layering from chapter 2 pays off here. Pure rules are tested with plain values, stores with an in-memory SQLite database, and cogs with a fake community that imitates Vector. No live bot, no network.",
  "A plugin is a folder or package that defines a MODULE description and an async setup(bot) function that adds your cog. It imports only from vectiq.plugin, the stable API, so it keeps working as Vectiq grows.",
  "The command vectiq --new-module NAME scaffolds a working plugin. Plugins start switched off, so you enable it with !module scan and !module on NAME."],
 [("Fixture", "A pytest helper that prepares what a test needs, such as an empty database."), ("Fake", "A stand-in object that behaves like the real thing in tests."), ("Entry point", "A packaging hook that lets pip installs announce plugins."), ("API_VERSION", "The version number of the stable plugin API."), ("Scaffold", "Starter files generated for you.")],
 ["pytest uses asyncio_mode auto; fixtures give an in-memory Database and Stores.", "Rules, stores and cogs are tested at three levels.", "A plugin defines MODULE and async setup(bot).", "Import helpers from vectiq.plugin: embed, ok, fail, exempt, enforce, is_owner.", "Add a setting in DEFAULTS plus a commented config entry and a changelog line."],
 [T("Testing a bot is like rehearsing a play. You can rehearse each actor alone, then in pairs, then the whole scene on a fake stage. You never need the real theatre until opening night."),
  F("13-1", "Each layer is tested with the lightest possible stand-in."),
  TB("Testing tools", ["Tool", "Gives you"], [["Database(':memory:')", "a fresh SQL database per test"], ["Stores(db)", "all stores ready"], ["FakeBank", "a pretend economy"], ["fake_community", "pretend members and channels"], ["make_bot", "a VectiqBot without downloads"]]),
  C("async def test_no_negative(db):\n    await db.execute(\"CREATE TABLE t (n INTEGER CHECK (n >= 0))\")\n    with pytest.raises(Exception):\n        await db.execute(\"INSERT INTO t VALUES (-1)\")", "python"),
  T("To write a plugin, describe it with Module, write a cog, and add async def setup(bot). The scaffold command gives you a working example. The repository also ships a complete example, an AI-powered automod plugin."),
  F("13-2", "A plugin needs a description, a setup function and a cog."),
  TB("The stable plugin API", ["Name", "Use"], [["Module", "describe your plugin"], ["embed, ok, fail, field", "consistent messages"], ["exempt, enforce, ACTIONS", "plug into the safety engine"], ["is_owner, name_of", "small helpers"], ["API_VERSION", "check compatibility"]]),
  T("Plugins can add a dashboard page too, by giving the cog a dashboard_page attribute and methods that return sections such as status, text, list, table, log and actions. That is how a plugin gets a settings screen without any web code.")],
 [("What do you test cogs with?", ["A fake community", "A live bot", "Production", "Nothing"], 0, "No Vector needed."), ("What must a plugin define?", ["MODULE and setup", "A database", "A web page", "A class named Bot"], 0, "Description and entry function."), ("Which module should plugins import from?", ["vectiq.plugin", "vectiq.stores", "vectiq.db", "anything"], 0, "The stable API."), ("What command scaffolds a plugin?", ["vectiq --new-module NAME", "vectiq --make", "pip new", "!scaffold"], 0, "Writes a working plugin."), ("Do plugins start enabled?", ["No", "Yes", "Only owners", "Always"], 0, "Off until you switch them on.")],
 [("Why test with :memory:?", "Fast and leaves no files."), ("What is a fixture?", "A reusable test setup."), ("What does API_VERSION protect?", "Plugins from breaking changes."), ("How does a plugin get a dashboard page?", "dashboard_page plus panel and action methods.")],
 [MATCH("Match test layer", "Pair each layer with its stand-in.", [("rules", "plain values"), ("stores", "in-memory database"), ("cogs", "fake community"), ("economy in games", "FakeBank")]),
  FILL("Plugin basics", "A plugin defines {{MODULE}} and {{setup}}, imports from {{vectiq.plugin}}, and starts {{off}}."),
  PL("Slot conflicts", "Write conflicts(enabled). enabled is a list of [module_name, slot] pairs for modules that are on. Return a sorted list of the slot names that more than one enabled module claims.", "conflicts(enabled)", '''
def conflicts(enabled):
    count = {}
    for name, slot in enabled:
        count[slot] = count.get(slot, 0) + 1
    return sorted(s for s, n in count.items() if n > 1)
''', [[[["sentire", "automod"], ["sentire_official", "automod"], ["leveling", "leveling"]]], [[["a", "x"], ["b", "y"]]], [[]], [[["a", "s"], ["b", "s"], ["c", "s"], ["d", "t"], ["e", "t"]]]], "Count how many modules claim each slot.")]))
