# -*- coding: utf-8 -*-
"""vector-sdk-py course, part 1: overview, keys, events, commands, cogs."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "What vector-sdk-py is and how it maps from discord.py",
 ("vector-sdk-py", [
  "vector-sdk-py | wraps | Rust vector_sdk",
  "PyO3 | binds | Rust to Python",
  "vector._native | is | Thin binding layer",
  "python/vector | is | discord.py style API",
  "Guild | aliases | Community",
  "user.id | aliases | npub",
  "bot.native | exposes | Raw Rust bot"]),
 ["vector-sdk-py is a Python library for Vector messenger bots. It copies the discord.py style: the same decorators, cogs, ctx, checks, cooldowns, converters, wait_for, tasks.loop, embeds and views.",
  "Underneath, every network, crypto and storage call runs in the official Rust vector_sdk crate, compiled into the package with PyO3. You get its communities, private messages, Mini Apps and voice without writing Rust.",
  "The repository is github.com/lucky-edgelord/vector-sdk-py, MIT licensed, marked alpha, and needs Python 3.9 or newer. Most discord.py bots port by changing the imports."],
 [("PyO3", "A Rust library for writing Python extension modules."),
  ("abi3 wheel", "One compiled package that works across Python versions on a platform."),
  ("Community", "Vector's name for a Discord guild; Guild is kept as an alias."),
  ("npub", "A Vector user's public key, used as the user id."),
  ("Native bot", "The raw Rust bot, reachable as bot.native for anything not wrapped.")],
 ["import vector; from vector.ext import commands, tasks.",
  "Layers: src/ is the PyO3 binding, python/vector/ is the discord.py style API.",
  "Guild is an alias of Community; user.id is an alias of npub.",
  "Intents are accepted and ignored: Vector sends every event.",
  "Anything not wrapped is reachable through bot.native."],
 [T("If you can write a discord.py bot, you already know this library. The idea is to keep your habits and swap the engine. The Python layer looks like discord.py, and the Rust layer does the secure messaging."),
  C("import os\nimport vector\nfrom vector.ext import commands\n\nbot = commands.Bot(command_prefix=\"!\")\n\n@bot.event\nasync def on_ready():\n    print(f\"Logged in as {bot.user}\")\n\n@bot.command()\nasync def ping(ctx):\n    await ctx.reply(\"pong\")\n\nbot.run(os.environ.get(\"VECTOR_NSEC\"))", "python"),
  T("Both the prefix command and Vector's native slash command work for ping. Every command is also published to the bot's manifest, so it appears in Vector's slash picker with typed arguments."),
  T("Porting is mostly renaming. Import vector as discord, or just use vector. Guild becomes Community with Guild kept as an alias, user.id becomes user.npub with id kept as an alias, and Intents are accepted but ignored because Vector delivers every event."),
  T("Some things have no direct equivalent and are emulated. Vector has no message components, so views are built from reactions. Embeds are rendered as coloured markdown. Ephemeral replies are sent as direct messages. The next chapters explain each emulation."),
  T("Because the project is alpha, expect change. Read the README and the tests for the current behaviour, and remember the Rust crate underneath also changes quickly.")],
 [("What does the library sit on top of?", ["The Rust vector_sdk crate", "discord.py", "A web API", "Matrix"], 0, "Via PyO3."),
  ("What is Guild in this library?", ["An alias of Community", "A different thing", "Removed", "A voice channel"], 0, "Compatibility."),
  ("What are Intents here?", ["Accepted and ignored", "Required", "Privileged", "Removed"], 0, "Vector sends all events."),
  ("What is a user's id?", ["Their npub", "A number", "An email", "A token"], 0, "id is an alias."),
  ("How can you reach unwrapped SDK features?", ["bot.native", "bot.raw", "vector.rust", "Not possible"], 0, "The raw Rust bot."),
  ("Which Python versions work?", ["3.9 and newer", "2.7", "3.5 only", "3.12 only"], 0, "abi3 wheel.")],
 [("bot.native", "The raw Rust bot"), ("vector._native", "The PyO3 binding module"), ("abi3", "Stable ABI wheel across Python versions"), ("alpha", "Early stage; expect changes")],
 [MATCH("Match the name", "Pair each discord.py name with the Vector equivalent.", [("Guild", "Community"), ("user.id", "user.npub"), ("bot token", "nsec key"), ("Intents", "accepted, ignored")]),
  FILL("Mapping", "The Python layer imitates {{discord.py}}. The engine is the Rust {{vector_sdk}} crate, bound with {{PyO3}}. Unwrapped features are reached through bot.{{native}}."),
  PL("Port a name", "Write port(name): 'Guild' gives 'Community'; 'guild' gives 'community'; 'token' gives 'nsec'; 'user.id' gives 'user.npub'; anything else is returned unchanged.", "port(name)", '''
def port(name):
    table = {'Guild': 'Community', 'guild': 'community', 'token': 'nsec', 'user.id': 'user.npub'}
    return table.get(name, name)
''', [['Guild'], ['token'], ['user.id'], ['channel']], "A lookup with a default."),
  PL("Port an import", "Write port_import(line): 'import discord' becomes 'import vector as discord'; 'from discord.ext import commands, tasks' becomes 'from vector.ext import commands, tasks'; any other line is unchanged.", "port_import(line)", '''
def port_import(line):
    if line == 'import discord':
        return 'import vector as discord'
    if line.startswith('from discord.ext import'):
        return line.replace('from discord.ext', 'from vector.ext', 1)
    return line
''', [['import discord'], ['from discord.ext import commands, tasks'], ['import os']], "Two patterns."),
  PL("Same user?", "Write same_user(a, b): users are dictionaries; return True when they have the same 'npub', or when one has 'npub' and the other has 'id' with the same value (id is an alias).", "same_user(a, b)", '''
def same_user(a, b):
    ka = a.get('npub', a.get('id'))
    kb = b.get('npub', b.get('id'))
    return ka is not None and ka == kb
''', [[{'npub': 'x'}, {'id': 'x'}], [{'npub': 'x'}, {'npub': 'y'}], [{}, {}]], "Treat id as npub."),
  PL("Python supported?", "Write py_ok(version): True when a version string like '3.9.1' is 3.9 or newer (major 3).", "py_ok(version)", '''
def py_ok(version):
    p = version.split('.')
    major = int(p[0])
    minor = int(p[1])
    if major != 3:
        return major > 3
    return minor >= 9
''', [['3.9.1'], ['3.8.10'], ['3.12.0'], ['2.7.18']], "Compare minor."),
  PL("Layer of a file", "Write layer(path): paths starting with 'src/' give 'rust binding'; starting with 'python/vector/' give 'python api'; starting with 'tests/' give 'tests'; anything else gives 'other'.", "layer(path)", '''
def layer(path):
    if path.startswith('src/'):
        return 'rust binding'
    if path.startswith('python/vector/'):
        return 'python api'
    if path.startswith('tests/'):
        return 'tests'
    return 'other'
''', [['src/bot.rs'], ['python/vector/client.py'], ['tests/test_bot.py'], ['README.md']], "Prefix checks.")]))


CHS.append(CH(
 "Installing, keys and starting the bot",
 ("Setup", [
  "pip install git+... | builds | Rust SDK",
  "Rust and cmake | are needed for | Build",
  "nsec | plays role of | Token",
  "bot.run | logs in with | nsec",
  "No key | reuses | data_dir key",
  "invite_policy | handles | Invites",
  "Client.features | lists | Build options"]),
 ["Install with pip install git+https://github.com/lucky-edgelord/vector-sdk-py. This compiles the Rust SDK, so you need a Rust toolchain and cmake for the Opus voice codec. Prebuilt wheels are produced by the GitHub Actions workflow, and once published to PyPI it will be pip install vector-sdk-py.",
  "A Vector identity is a Nostr key. bot.run takes an nsec key where discord.py takes a token. Called with no key it reuses the key stored in data_dir, which defaults to ./vector-bot-data, creating one on first run. A seed phrase works with mnemonic.",
  "Voice and Mini Apps are built by default. Speech to text (whisper), Tor and I2P are opt-in build features, and Client.features() tells you what your build has."],
 [("nsec", "The bot's private key; plays the role of a Discord token."),
  ("data_dir", "Where the bot keeps its database and key; default ./vector-bot-data."),
  ("invite_policy", "manual (default), public, or a whitelist of npubs."),
  ("maturin", "The build tool that compiles the Rust extension into a Python package."),
  ("Wheel", "A prebuilt Python package file.")],
 ["Needs Rust toolchain and cmake to build from source.",
  "bot.run(nsec) or bot.run() to reuse the stored key.",
  "vector.generate_nsec() mints a key; keep it secret.",
  "invite_policy: manual, public, or whitelist=[npubs].",
  "Whisper, Tor and I2P are opt-in features at build time."],
 [T("Installing this library is different from most Python packages because it compiles Rust. That takes a few minutes the first time, and later installs reuse the cache. Prebuilt wheels avoid the compile when they are available for your platform."),
  C("pip install git+https://github.com/lucky-edgelord/vector-sdk-py\n\n# opt-in features at build time\npip install \"git+https://github.com/lucky-edgelord/vector-sdk-py\" \\\n    --config-settings=build-args=\"--features whisper,tor\"", "bash"),
  T("Your bot's identity is a Nostr key. Where discord.py wants a token, this library wants the nsec. If you pass nothing, the library reuses the key it saved in data_dir, and creates one on the first run, which is perfect for experiments."),
  C("import vector\nprint(vector.generate_nsec())   # mint one and keep it secret\n\nbot = commands.Bot(command_prefix=\"!\",\n                   data_dir=\"./vector-bot-data\",\n                   invite_policy=\"public\")        # or \"manual\" or whitelist=[...]\nbot.run(os.environ.get(\"VECTOR_NSEC\"))", "python"),
  T("Invite policy decides what happens when someone invites the bot to a community. Manual queues the invite and fires on_community_invite, where you can call invite.accept. Public accepts every invite. A whitelist accepts only invites from the npubs you list."),
  T("Treat the nsec like a password: read it from an environment variable, never commit it, and do not print it. Give each bot its own data_dir, because the directory holds the key and the database.")],
 [("What does bot.run take?", ["The nsec key", "A Discord token", "A URL", "A password file"], 0, "Plays the token role."),
  ("What if you pass no key?", ["It reuses or creates the stored key", "It fails", "It uses a public key", "It asks the relay"], 0, "From data_dir."),
  ("Why is cmake needed?", ["For the Opus voice codec", "For Python", "For pip", "For tests"], 0, "Build requirement."),
  ("Default invite policy?", ["manual", "public", "whitelist", "off"], 0, "Queued."),
  ("How do you see build features?", ["Client.features()", "bot.version", "pip list", "vector.help"], 0, "Reports voice, whisper, tor..."),
  ("Where is the key stored?", ["In data_dir", "In the cloud", "In PyPI", "In the wheel"], 0, "Default ./vector-bot-data.")],
 [("generate_nsec", "Create a new key"), ("on_community_invite", "Event fired for manual invites"), ("whitelist", "Auto-accept only these npubs"), ("mnemonic", "Seed phrase login")],
 [APP("POLICY", "Invite policy lab", "Try each invite policy against different senders."),
  MATCH("Match the setting", "Pair each setting with its effect.", [("manual", "queue and fire on_community_invite"), ("public", "accept every invite"), ("whitelist", "accept listed npubs only"), ("no key", "reuse or create stored key")]),
  FILL("Setup", "The key plays the role of the {{token}}. With no key, the library reuses the key stored in {{data_dir}}. The default invite policy is {{manual}}. Build tools needed: Rust and {{cmake}}."),
  PL("Invite decision", "Write decide(policy, sender, whitelist): 'manual' gives 'queue'; 'public' gives 'accept'; 'whitelist' gives 'accept' when sender is in the list, else 'ignore'.", "decide(policy, sender, whitelist)", '''
def decide(policy, sender, whitelist):
    if policy == 'manual':
        return 'queue'
    if policy == 'public':
        return 'accept'
    if sender in whitelist:
        return 'accept'
    return 'ignore'
''', [['manual', 'a', []], ['public', 'a', []], ['whitelist', 'a', ['a']], ['whitelist', 'z', ['a']]], "Three policies."),
  PL("Which key?", "Write key_to_use(passed, mnemonic, stored): the passed nsec wins, then a mnemonic, then the stored key, otherwise 'create'.", "key_to_use(passed, mnemonic, stored)", '''
def key_to_use(passed, mnemonic, stored):
    if passed != '':
        return 'passed'
    if mnemonic != '':
        return 'mnemonic'
    if stored != '':
        return 'stored'
    return 'create'
''', [['k', '', ''], ['', 'w', 's'], ['', '', 's'], ['', '', '']], "Priority."),
  PL("Build features", "Write has_feature(build, name): build is a list of feature names the package was built with, plus the default ones 'voice' and 'xdc' are always present. True if name is in build or is a default feature.", "has_feature(build, name)", '''
def has_feature(build, name):
    return name in build or name in ('voice', 'xdc')
''', [[[], 'voice'], [[], 'tor'], [['tor'], 'tor'], [['whisper'], 'xdc']], "Defaults plus extras."),
  PL("Redact secrets", "Write redact(text): split on single spaces; any word starting with 'nsec1' becomes 'nsec1[redacted]'. Join with single spaces.", "redact(text)", '''
def redact(text):
    out = []
    for w in text.split(' '):
        if w.startswith('nsec1'):
            out.append('nsec1[redacted]')
        else:
            out.append(w)
    return ' '.join(out)
''', [['key nsec1abc loaded'], ['all clear']], "Never log keys."),
  PL("Pick a data dir", "Write dirs_ok(bots): bots is a list of [name, data_dir]. Return True when no two bots share the same data_dir.", "dirs_ok(bots)", '''
def dirs_ok(bots):
    seen = []
    for name, d in bots:
        if d in seen:
            return False
        seen.append(d)
    return True
''', [[[['a', '/x'], ['b', '/y']]], [[['a', '/x'], ['b', '/x']]], [[]]], "Each bot needs its own.")]))


CHS.append(CH(
 "Events: the discord.py names plus Vector's own",
 ("Events", [
  "@bot.event | registers | Handler",
  "@bot.listen | adds | Extra listener",
  "on_message | gets | Messages",
  "on_community_change | is | Raw audited change",
  "on_member_kick | is | Separate from remove",
  "on_slash_command | gets | Raw native command",
  "wait_for | waits for | One event"]),
 ["The usual discord.py event names fire with the usual arguments: on_ready, on_message, on_message_edit, on_message_delete, on_reaction_add, on_typing, on_member_join, on_member_remove, on_member_ban, on_guild_join, on_guild_role_create and more.",
  "Vector adds events of its own: on_community_invite, on_community_change, on_member_kick, on_member_timeout, on_member_roles_update, on_overwrite_update, on_channel_keyed, on_community_dissolve, on_xdc_presence, on_xdc_session and on_slash_command.",
  "Register with bot.event or bot.listen, and use wait_for when you want to pause a command until a particular event arrives."],
 [("Listener", "An extra handler for an event, added with bot.listen so several can coexist."),
  ("on_community_change", "The raw form of every audited community change; other events derive from it."),
  ("on_member_kick", "A kick; Discord folds this into on_member_remove."),
  ("on_channel_keyed", "The bot received the key for a private channel."),
  ("wait_for", "Await one event that passes a check, with a timeout.")],
 ["bot.event replaces a handler; bot.listen adds one.",
  "Vector extras: on_community_invite, on_member_kick, on_member_timeout.",
  "on_member_roles_update(member, added, removed) is finer than on_member_update.",
  "on_slash_command(name, args, message) sees raw native commands.",
  "Use wait_for with a check and a timeout."],
 [T("Events work the way they do in discord.py. A decorated coroutine with the right name is called when the event happens. The names and arguments match closely, so most of your handlers need no change."),
  C("@bot.event\nasync def on_member_join(member: vector.Member):\n    channel = member.guild.system_channel\n    if channel:\n        await channel.send(f\"Welcome {member.mention}!\")\n\n@bot.listen()\nasync def on_message(message):\n    if message.author == bot.user:\n        return\n    print(message.content)", "python"),
  T("Vector's richer community model produces events that Discord does not have. A timeout, a role change, a nickname change and a permission overwrite each get their own event, and they all derive from on_community_change, which carries the raw change and who made it."),
  T("A kick is its own event, on_member_kick, rather than being folded into on_member_remove as Discord does. If you want one handler for both, listen to both. The on_member_ban and on_member_unban events behave as in discord.py."),
  C("# wait for the same user's next message, up to 30 seconds\ndef check(m):\n    return m.author == ctx.author and m.channel == ctx.channel\n\nmsg = await bot.wait_for(\"message\", check=check, timeout=30)", "python"),
  T("Error handling is the same too. on_error catches exceptions in event handlers, and on_command_error catches errors from commands. Keep handlers short and push long work into tasks, so they do not block other events.")],
 [("Which registers an extra listener?", ["bot.listen", "bot.event", "bot.run", "bot.close"], 0, "Several can coexist."),
  ("Which event is Vector-specific?", ["on_member_timeout", "on_ready", "on_message", "on_typing"], 0, "Not in Discord."),
  ("How are kicks reported?", ["on_member_kick", "Only on_member_remove", "Not at all", "on_ban"], 0, "Separate event."),
  ("What does on_slash_command receive?", ["name, args, message", "ctx", "token", "nothing"], 0, "Raw native command."),
  ("What does wait_for take?", ["An event name, check and timeout", "A token", "A file", "A guild"], 0, "Pause for an event."),
  ("What is on_community_change?", ["The raw audited change event", "A chat message", "A voice call", "A login"], 0, "Source of the finer events.")],
 [("on_member_roles_update", "Roles added and removed"), ("on_member_nickname_update", "Nickname changed"), ("on_overwrite_update", "Permission overwrite changed"), ("on_community_dissolve", "Owner dissolved the community")],
 [APP("EVENTS", "Event router", "Send events through the router and see which handler fires."),
  MATCH("Match the event", "Pair each situation with the event.", [("someone is kicked", "on_member_kick"), ("someone is timed out", "on_member_timeout"), ("roles change", "on_member_roles_update"), ("owner dissolves", "on_community_dissolve")]),
  FILL("Events", "{{bot.listen}} adds an extra handler. A kick fires {{on_member_kick}}. Raw changes arrive as {{on_community_change}}. Pause a command with bot.{{wait_for}}."),
  PL("Which handler?", "Write handler_for(change): 'kick' gives 'on_member_kick'; 'ban' gives 'on_member_ban'; 'timeout' gives 'on_member_timeout'; 'roles' gives 'on_member_roles_update'; 'nickname' gives 'on_member_nickname_update'; 'overwrite' gives 'on_overwrite_update'; anything else gives 'on_community_change'.", "handler_for(change)", '''
def handler_for(change):
    table = {'kick': 'on_member_kick', 'ban': 'on_member_ban', 'timeout': 'on_member_timeout', 'roles': 'on_member_roles_update', 'nickname': 'on_member_nickname_update', 'overwrite': 'on_overwrite_update'}
    return table.get(change, 'on_community_change')
''', [['kick'], ['roles'], ['overwrite'], ['pin']], "Lookup with default."),
  PL("Role diff", "Write roles_diff(before, after): both are lists of role names. Return [added, removed] as sorted lists.", "roles_diff(before, after)", '''
def roles_diff(before, after):
    added = [r for r in after if r not in before]
    removed = [r for r in before if r not in after]
    added.sort()
    removed.sort()
    return [added, removed]
''', [[['a', 'b'], ['b', 'c']], [[], ['x']], [['x'], ['x']]], "Set differences."),
  PL("Wait for message", "Write wait_for(messages, author, channel): messages is a list of [author, channel, text]. Return the text of the first message by that author in that channel, or 'timeout' if none.", "wait_for(messages, author, channel)", '''
def wait_for(messages, author, channel):
    for a, c, t in messages:
        if a == author and c == channel:
            return t
    return 'timeout'
''', [[[['a', 'c1', 'hi'], ['b', 'c1', 'yo']], 'b', 'c1'], [[['a', 'c2', 'x']], 'a', 'c1'], [[], 'a', 'c1']], "Mimic the check."),
  PL("Is it my own message?", "Write should_handle(author, bot_npub, content): False for the bot's own messages and for empty content, otherwise True.", "should_handle(author, bot_npub, content)", '''
def should_handle(author, bot_npub, content):
    if author == bot_npub:
        return False
    return content != ''
''', [['a', 'a', 'hi'], ['b', 'a', 'hi'], ['b', 'a', '']], "Avoid loops."),
  PL("Timeout over?", "Write timed_out(until, now): True while now is before until.", "timed_out(until, now)", '''
def timed_out(until, now):
    return now < until
''', [[600, 100], [600, 600], [600, 900]], "Strictly before.")]))


CHS.append(CH(
 "Commands: prefix and native slash at once",
 ("Commands", [
  "@bot.command | defines | Prefix command",
  "Manifest | publishes | Native slash command",
  "Type hint | maps to | Vector arg type",
  "Literal | becomes | Choice",
  "Member | becomes | User picker",
  "Prefix / | is | Native only",
  "More than 8 args | stays | Prefix only"]),
 ["Every command you define is available as a text command and, where possible, as a native Vector slash command. The library publishes a manifest so the command appears in Vector's slash picker with typed arguments, and Vector checks the types before your code runs.",
  "Type hints decide the argument types: str is text, int is int, float is number, bool is a flag, Member or User is a user picker, Literal is a choice. Trailing arguments such as a keyword-only rest, args or Greedy become trailing text. Anything else is text, converted in Python.",
  "The default prefix is the slash. Set a prefix such as an exclamation mark to also accept text commands. Commands whose name or signature cannot be expressed natively stay prefix only."],
 [("Manifest", "The list of native commands published to Vector."),
  ("Literal", "A typing construct that limits a value to fixed options; shown as a dropdown."),
  ("Greedy", "A converter wrapper that consumes as many arguments as possible."),
  ("describe", "A decorator that gives each argument a description in the picker."),
  ("hybrid", "A command usable as both text and native slash; here every command is.")],
 ["command_prefix defaults to '/' (native only); '!' also accepts text.",
  "str=text, int=int, float=number, bool=flag, Member=user, Literal=choice.",
  "Rest, *args and Greedy become trailing text.",
  "Names with uppercase letters or more than 8 args stay prefix only.",
  "Groups become /name subcommand args."],
 [T("The nice thing is that you write one function and get two ways to call it. A person can type an exclamation mark and the command name, or pick the slash command from the picker and fill in typed fields."),
  C("from typing import Literal\n\n@bot.command()\n@commands.describe(temp=\"the temperature\", unit=\"what it's in\")\nasync def convert(ctx, temp: float, unit: Literal[\"c\", \"f\"]):\n    if unit == \"c\":\n        await ctx.send(f\"{temp}°C = {temp * 9 / 5 + 32:.1f}°F\")\n    else:\n        await ctx.send(f\"{temp}°F = {(temp - 32) * 5 / 9:.1f}°C\")", "python"),
  T("This is published as convert with a number field called temp and a choice called unit with the options c and f. Vector checks the input and replies with usage before your function runs, so you rarely need to validate."),
  T("Not everything can be native. Arguments that are a Role, a TextChannel or a custom converter are sent as text and converted in Python. A command whose name has uppercase letters, or which has more than eight arguments, stays prefix only, and a log line tells you so."),
  T("Groups work like in discord.py: bot.group makes a command with subcommands, published as a name followed by a subcommand and its arguments. Load your cogs in setup_hook, as discord.py recommends, so their commands are part of the manifest published at startup."),
  T("Prefix commands still use the familiar error classes. A bad conversion raises BadArgument, a missing value raises MissingRequiredArgument, and an unknown command raises CommandNotFound, which you can handle in on_command_error.")],
 [("Which hint becomes a dropdown?", ["Literal", "str", "int", "bool"], 0, "Choice."),
  ("What does float map to?", ["number", "int", "flag", "text"], 0, "Vector arg type."),
  ("Default command_prefix?", ["/", "!", "?", "none"], 0, "Native only."),
  ("Which commands stay prefix only?", ["Uppercase names or more than 8 args", "All of them", "None", "Those with Member"], 0, "Cannot be native."),
  ("Where are cogs best loaded?", ["setup_hook", "on_message", "a loop", "a command"], 0, "Before the manifest is published."),
  ("Who checks types for native commands?", ["Vector, before your code runs", "Nobody", "The relay", "Python only"], 0, "Client side.")],
 [("commands.describe", "Add argument descriptions"), ("bot.group", "A command with subcommands"), ("hybrid_command", "Same as command here"), ("CommandNotFound", "Unknown command error")],
 [APP("HINTS", "Type hint mapper", "Pick a Python type hint and see which Vector argument it becomes."),
  MATCH("Match the hint", "Pair each hint with the Vector argument.", [("str", "text"), ("float", "number"), ("Member", "user picker"), ("Literal", "choice")]),
  FILL("Commands", "The default prefix is the {{slash}}. Literal becomes a {{choice}}. Decorate with commands.{{describe}} to explain arguments. Commands with more than {{8}} arguments stay prefix only."),
  PL("Hint to argument", "Write arg_type(hint): 'str' gives 'text'; 'int' gives 'int'; 'float' gives 'number'; 'bool' gives 'flag'; 'Member' and 'User' give 'user'; 'Literal' gives 'choice'; 'Greedy' and 'rest' give 'trailing text'; anything else gives 'text'.", "arg_type(hint)", '''
def arg_type(hint):
    table = {'str': 'text', 'int': 'int', 'float': 'number', 'bool': 'flag', 'Member': 'user', 'User': 'user', 'Literal': 'choice', 'Greedy': 'trailing text', 'rest': 'trailing text'}
    return table.get(hint, 'text')
''', [['str'], ['float'], ['Member'], ['Literal'], ['Greedy'], ['Role']], "A lookup."),
  PL("Can it be native?", "Write native_ok(name, nargs): True when the name has no uppercase letters and nargs is at most 8.", "native_ok(name, nargs)", '''
def native_ok(name, nargs):
    return name == name.lower() and nargs <= 8
''', [['ping', 0], ['Ping', 0], ['big', 9], ['roll', 8]], "Two conditions."),
  PL("Describe the manifest", "Write manifest_line(name, args): args is a list of [argname, type]. Return '/name <a:type> <b:type>' with a space between pieces; with no args return '/name'.", "manifest_line(name, args)", '''
def manifest_line(name, args):
    parts = ['/' + name]
    for a, t in args:
        parts.append('<' + a + ':' + t + '>')
    return ' '.join(parts)
''', [['convert', [['temp', 'number'], ['unit', 'c|f']]], ['ping', []]], "Join the pieces."),
  PL("Which prefixes work?", "Write accepts(content, prefixes): True when the content starts with any of the given prefixes.", "accepts(content, prefixes)", '''
def accepts(content, prefixes):
    for p in prefixes:
        if content.startswith(p):
            return True
    return False
''', [['!ping', ['!']], ['/ping', ['/', '!']], ['ping', ['!']], ['', ['!']]], "Any prefix."),
  PL("Greedy consumption", "Write greedy(args, kind): args is a list of strings; kind is 'int'. Return the leading items that are all digits and stop at the first that is not. Return them as integers.", "greedy(args, kind)", '''
def greedy(args, kind):
    out = []
    for a in args:
        ok = a != ''
        for ch in a:
            if ch not in '0123456789':
                ok = False
        if not ok:
            break
        out.append(int(a))
    return out
''', [[['1', '2', 'x', '3'], 'int'], [['a'], 'int'], [['5', '6'], 'int']], "Stop at the first non-digit.")]))


CHS.append(CH(
 "Cogs, checks, cooldowns, converters and tasks",
 ("Structure", [
  "Cog | groups | Commands and listeners",
  "setup | adds | Cog",
  "has_permissions | checks | Member rights",
  "cooldown | limits | Command use",
  "Converter | builds | Objects from text",
  "tasks.loop | repeats | Coroutine",
  "Error handler | answers | Failures"]),
 ["Structure works as in discord.py. A Cog groups commands and listeners, and an extension module defines async def setup(bot) that adds it with bot.add_cog. Cog_check can apply a rule to every command in a cog.",
  "Checks such as has_permissions, guild_only and is_owner guard commands. Cooldowns limit how often a command can be used, per user, community, channel or other bucket. is_owner uses owner_id, which takes an npub.",
  "Converters turn text into objects: Member, Role, TextChannel, Greedy, Range, Literal and your own. tasks.loop repeats a coroutine on a schedule. Errors are classes such as MissingPermissions, BadArgument and CommandOnCooldown."],
 [("Cog", "A class grouping related commands and listeners."),
  ("Check", "A predicate a command must pass, such as has_permissions or guild_only."),
  ("Cooldown", "A limit of rate uses per period seconds in a bucket."),
  ("BucketType", "The scope of a cooldown: default, user, guild/community, channel, member, category or role."),
  ("tasks.loop", "A decorator that runs a coroutine every seconds, minutes or hours.")],
 ["await bot.add_cog(Cog(bot)) inside async def setup(bot).",
  "cog_check can guard every command in a cog.",
  "@commands.cooldown(rate, per, BucketType.user).",
  "has_permissions(kick_members=True), is_owner(), guild_only().",
  "@tasks.loop(minutes=5); start with .start()."],
 [T("Cogs keep a growing bot tidy. Each cog is a class with its own commands and listeners, and the bot loads them from extension modules. The examples directory has a cogs bot with moderation, fun and admin cogs."),
  C("class Moderation(commands.Cog):\n    def __init__(self, bot):\n        self.bot = bot\n\n    async def cog_check(self, ctx):\n        return ctx.guild is not None      # community-only\n\n    @commands.command()\n    @commands.has_permissions(kick_members=True)\n    async def kick(self, ctx, member: vector.Member, *, reason: str = None):\n        await member.kick(reason=reason)\n        await ctx.send(f\"Kicked {member.display_name}\")\n\nasync def setup(bot):\n    await bot.add_cog(Moderation(bot))", "python"),
  T("Checks run before the command body. If one fails, a CheckFailure subclass such as MissingPermissions is raised and goes to your error handler, so you can answer politely. A cog level error handler can be attached with the command's error decorator."),
  T("A cooldown is a token bucket. A command allows rate uses within each period of per seconds. Once the tokens are used up, the next call raises CommandOnCooldown carrying how many seconds remain. The bucket type decides who shares the allowance."),
  C("@commands.command()\n@commands.cooldown(2, 30, commands.BucketType.user)\nasync def roll(ctx):\n    ...\n\n@tasks.loop(minutes=5)\nasync def report():\n    ...\n\n@report.before_loop\nasync def before():\n    await bot.wait_until_ready()", "python"),
  T("Converters work as in discord.py, including Greedy for many arguments and Range for bounds. Errors such as MemberNotFound and RoleNotFound carry the offending argument, which makes friendly error messages easy.")],
 [("What must an extension define?", ["async def setup(bot)", "def main", "class Bot", "token"], 0, "Entry point."),
  ("What does cog_check do?", ["Guards every command in the cog", "Loads the cog", "Sends messages", "Runs tasks"], 0, "Cog-wide rule."),
  ("What is a cooldown?", ["rate uses per period seconds", "A sleep", "A timeout", "A ban"], 0, "Token bucket."),
  ("Which error does a cooldown raise?", ["CommandOnCooldown", "BadArgument", "Forbidden", "NotFound"], 0, "retry_after."),
  ("owner_id takes:", ["An npub", "A number", "A name", "An email"], 0, "Vector identity."),
  ("How do you wait before a loop starts?", ["before_loop with wait_until_ready", "sleep", "nothing", "stop()"], 0, "Cache ready.")],
 [("Greedy", "Consume many arguments"), ("Range", "Bounded numeric converter"), ("MemberNotFound", "Member converter failed"), ("max_concurrency", "Limit simultaneous runs")],
 [MATCH("Match the error", "Pair each situation with the error.", [("used too soon", "CommandOnCooldown"), ("bad number", "BadArgument"), ("lacks rights", "MissingPermissions"), ("no such member", "MemberNotFound")]),
  FILL("Structure", "A {{cog}} groups commands. Guard a command with a {{check}}. A cooldown allows {{rate}} uses every {{per}} seconds."),
  PL("Cooldown simulator", "Write cooldown(rate, per, times): simulate discord.py's bucket for one user. times is a sorted list of seconds when the command is called. A call is allowed (None) while tokens remain in the current window, which starts at the first allowed call and lasts per seconds; when no tokens remain return the seconds left rounded to 1 decimal. A window ends after per seconds and tokens reset. Return the list of results.", "cooldown(rate, per, times)", '''
def cooldown(rate, per, times):
    tokens = rate
    window = 0.0
    out = []
    for t in times:
        if t > window + per:
            tokens = rate
        if tokens == rate:
            window = t
        tokens -= 1
        if tokens < 0:
            tokens = 0
            out.append(round(per - (t - window), 1))
        else:
            out.append(None)
    return out
''', [[2, 10, [0, 1, 2, 3]], [1, 5, [0, 6]], [3, 60, [0, 10, 20, 30]], [1, 5, [0, 1, 6, 7]]], "Replicates the library's token bucket."),
  PL("Bucket key", "Write bucket_key(kind, user, channel, community): 'user' returns the user; 'channel' returns the channel; 'community' or 'guild' returns the community; 'member' returns the user and community joined with a colon; anything else returns 'global'.", "bucket_key(kind, user, channel, community)", '''
def bucket_key(kind, user, channel, community):
    if kind == 'user':
        return user
    if kind == 'channel':
        return channel
    if kind in ('community', 'guild'):
        return community
    if kind == 'member':
        return user + ':' + community
    return 'global'
''', [['user', 'u', 'c', 'g'], ['member', 'u', 'c', 'g'], ['guild', 'u', 'c', 'g'], ['default', 'u', 'c', 'g']], "Which scope shares the limit."),
  PL("Has permission", "Write has_perms(member_perms, needed): both are lists of permission names. True when every needed one is present.", "has_perms(member_perms, needed)", '''
def has_perms(member_perms, needed):
    for n in needed:
        if n not in member_perms:
            return False
    return True
''', [[['kick_members', 'send_messages'], ['kick_members']], [['send_messages'], ['kick_members']], [[], []]], "Every needed one."),
  PL("Range converter", "Write in_range(value, low, high): return the value if it is between low and high inclusive, otherwise the string 'RangeError'.", "in_range(value, low, high)", '''
def in_range(value, low, high):
    if value < low or value > high:
        return 'RangeError'
    return value
''', [[5, 1, 10], [0, 1, 10], [11, 1, 10], [10, 1, 10]], "Bounds are inclusive."),
  PL("Loop runs", "Write loop_runs(elapsed, interval): a tasks.loop runs once at start and then every interval seconds. Return how many runs happened after elapsed seconds.", "loop_runs(elapsed, interval)", '''
def loop_runs(elapsed, interval):
    return elapsed // interval + 1
''', [[0, 300], [299, 300], [600, 300]], "Floor plus one.")]))
