# -*- coding: utf-8 -*-
from figs import *

def F(n, f): reg("vq-%s.svg" % n, f)

F("1-1", lambda: layers("Where Vectiq sits", "Layers from your community down to the Vector network.", [
  ("Your community", "members, channels, roles", "g"), ("Vectiq", "modules: moderation, levels, economy, games...", "v"),
  ("vector-sdk-py", "discord.py style Python API", "b"), ("Rust vector_sdk", "encryption and messaging, bound with PyO3", "a"), ("Vector network", "private, relay based messaging", "p")],
  "Vectiq is the Python layer in the middle. It never handles encryption itself."))
F("1-2", lambda: columns("Vectiq modules by group", "Five groups of modules.", [("Safety", "moderation, link safety, image guard, Sentire"), ("Members", "verification, onboarding, roles, welcome"), ("Community", "tickets, events, giveaways, notifications, utility")],
  [("Fun", "leveling, economy, games, music"), ("Integrations", "webhooks, MCP, dashboard"), ("Core", "always on: core and restore points")], "Groups", "More", "Every feature is a module you switch on or off."))
F("2-1", lambda: layers("The layers of the code", "Cogs on top, stores, database, with pure rules and renderers on the side.", [
  ("cogs/", "all Vector input and output: commands, listeners, loops", "v"), ("stores/", "all SQL: one small class per feature", "b"),
  ("db/", "async SQLite facade and numbered migrations", "g"), ("games/ and render/", "pure rules and Pillow pictures, no network", "a")],
  "Each layer only calls the one below it."))
F("2-2", lambda: flow("One message, start to finish", "A message travels through a cog, a store and the database.", [
  ("on_message", "cog listener hears it", "v"), ("store.award()", "decides the XP", "b"), ("db.transaction()", "writes in one step", "g"),
  ("rank card", "Pillow draws a picture", "a"), ("channel.send", "cog replies", "v")], "Vector only appears at the two ends."))
F("3-1", lambda: flow("One connection, many callers", "Calls queue behind a lock and run in a thread.", [
  ("cog A", "await db.one()", "v"), ("asyncio.Lock", "one at a time", "a"), ("to_thread", "sqlite3 runs off the loop", "b"),
  ("SQLite file", "WAL mode", "g")], "The bot never freezes while SQLite works.", per=4))
F("3-2", lambda: flow("Starting up with migrations", "Compare user_version to the list and apply what is newer.", [
  ("read user_version", "say 3", "b"), ("MIGRATIONS list", "has 8 scripts", "v"), ("apply 4 to 8", "in order", "g"),
  ("set user_version", "now 8", "a")], "An old database upgrades itself; a newer one is refused.", per=4))
F("4-1", lambda: layers("Where a setting comes from", "Defaults, then config.yaml, then dashboard overrides.", [
  ("Dashboard overrides", "stored in the database, win over the file", "p"), ("config.yaml", "your edits, merged over the defaults", "v"),
  ("DEFAULTS in config.py", "every setting has a safe value", "b"), (".env", "secrets only: keys and tokens", "r")],
  "The top row wins. Secrets live apart from the rest."))
F("4-2", lambda: columns("A recursive merge", "Defaults and a small override become one result.", [("defaults", "economy: daily_amount 200"), ("also", "economy: work_cooldown 30")], [("your file", "economy: daily_amount 300"), ("result", "daily_amount 300, cooldown 30")], "Base", "Merged", "Only the keys you wrote change; the rest stay."))
F("5-1", lambda: flow("A module and its parts", "Module bundles cogs, defaults, settings and checks.", [
  ("Module", "name, label, group", "v"), ("cogs", "files to load", "b"), ("imports", "needed packages", "a"), ("defaults", "its settings", "g"), ("slot", "one provider at a time", "p")],
  "Switch a module on and its cogs load live."))
F("5-2", lambda: flow("Finding plugins", "Entry points or a modules folder.", [
  ("pip entry point", "group vectiq.modules", "b"), ("modules/<name>/", "folder with MODULE", "b"), ("discover()", "collects both", "v"),
  ("starts off", "you switch it on", "a")], "Plugins always start switched off.", per=4))
F("6-1", lambda: flow("Life of a command", "From message to reply.", [
  ("message", "starts with the prefix", "v"), ("checks", "permissions, module on", "a"), ("cooldown", "slow down spam", "a"),
  ("handler", "runs your code", "b"), ("reply", "embed or text", "g"), ("on_command_error", "friendly failure", "r")], "A failure at any step ends in the error handler."))
F("6-2", lambda: flow("Switching modules live", "sync_modules loads and unloads cogs.", [
  ("settings change", "dashboard or command", "p"), ("sync_modules()", "under an asyncio lock", "v"), ("load or unload cogs", "no restart", "b"), ("module_problems", "records what went wrong", "r")],
  "A broken module is reported, and the bot keeps running.", per=4))
F("7-1", xpbars); reg("vq-7-1.svg", xpbars)
F("7-2", lambda: flow("Awarding XP", "Rules and steps for one message.", [
  ("skip", "bots, DMs, commands", "r"), ("cooldown", "60 s", "a"), ("award()", "15 to 25 XP", "b"), ("level up?", "compare levels", "v"), ("role reward", "give the role", "g"), ("announce", "post or card", "p")],
  "A message in cooldown still counts, it just earns no XP."))
F("8-1", lambda: flow("An atomic transfer", "Both sides change together or not at all.", [
  ("BEGIN", "IMMEDIATE", "g"), ("take from A", "fails if short", "a"), ("give to B", "", "b"), ("log both", "transactions table", "v"), ("COMMIT", "or ROLLBACK", "g")],
  "No coin is ever lost or made halfway."))
F("8-2", lambda: columns("Daily streak", "A streak raises the daily payout up to a cap.", [("day 1", "200"), ("day 2", "225"), ("day 3", "250")], [("day 11", "450 (cap reached)"), ("day 12", "450"), ("missed days", "back to day 1")], "Growing", "Capped", "paid = 200 + 25 x min(streak - 1, 10)."))
F("9-1", lambda: flow("The enforcement ladder", "Actions Vectiq's safety modules can take.", [
  ("log", "tell the mod log", "g"), ("delete", "remove the message", "a"), ("warn", "add a case", "a"), ("timeout", "mute for a while", "r"), ("threshold", "3 warnings escalate", "p")],
  "enforce() never raises; staff and exempt roles are skipped."))
F("9-2", lambda: flow("Link safety pipeline", "From a message to a verdict.", [
  ("find domains", "with or without https", "b"), ("allow list", "beats everything", "g"), ("block list", "beats the lists", "r"), ("public lists", "oisd and friends", "a"), ("action", "delete, warn...", "v")],
  "Subdomains of a listed site are caught too."))
F("10-1", lambda: columns("Three ways to verify", "Question, button and captcha modes.", [("question", "answer a small sum"), ("button", "react with a tick")], [("captcha", "personal one-time link"), ("stored result", "survives role loss")], "Easy", "Stronger", "All of them record the result in the database."))
F("10-2", lambda: flow("Device marks", "Scrambled markers stop duplicate accounts.", [
  ("ip, cookie, fingerprint", "collected by the page", "b"), ("HMAC with a secret", "cannot be guessed back", "a"), ("transaction", "check then insert", "g"), ("on_duplicate", "refuse, kick or softban", "r")],
  "Marks are never stored next to the member.", per=4))
F("11-1", lambda: layers("The game referee", "Players' apps talk through the bot.", [
  ("WebXDC apps", "one per player, shared in the chat", "g"), ("realtime channel", "messages in both directions", "b"), ("cogs/games.py", "the referee: checks who is who", "v"), ("games/ rules", "pure Python, easy to test", "a")],
  "The bot is the referee, so nobody can cheat from their phone."))
F("11-2", lambda: flow("A game conversation", "Typical messages.", [
  ("hello", "player joins", "g"), ("state", "bot sends the board", "v"), ("move", "player acts", "g"), ("update", "rules decide", "a"), ("outcome", "coins and stats", "p")],
  "Unverified senders are asked to try again."))
F("12-1", lambda: columns("Inside a restore point", "A zip file with four things.", [("vectiq.db", "the whole database"), ("config.yaml", "your settings file")], [("settings-export.yaml", "with dashboard changes"), ("event-images/", "pictures")], "Database", "Files", "The bot's key in .env is never included."))
F("12-2", lambda: columns("Ways to run the bot", "Control surfaces.", [("Chat commands", "!module on, !restorepoint"), ("Dashboard", "FastAPI web pages")], [("MCP server", "AI assistants with a token"), ("Webhooks", "events out to other tools")], "Humans", "Machines", "All of them end up in the same stores."))
F("13-1", lambda: layers("What tests cover", "Fakes replace the network.", [
  ("pure rules", "plain pytest, fastest", "a"), ("stores on :memory:", "real SQL, no files", "g"), ("cogs with fake_community", "no live Vector", "b")],
  "Because layers are separate, almost everything tests offline."))
F("13-2", lambda: flow("A plugin skeleton", "What a plugin needs.", [
  ("MODULE", "Module(...) description", "v"), ("async setup(bot)", "adds your cog", "b"), ("cog class", "commands and listeners", "g"), ("plugin API", "embed, ok, fail, exempt", "a")],
  "vectiq --new-module NAME writes this for you.", per=4))
