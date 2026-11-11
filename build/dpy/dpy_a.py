# -*- coding: utf-8 -*-
"""discord.py course, part 1: client, intents, commands, cogs, app commands."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "The client, events and the gateway",
 ("discord.py basics", [
  "Client | connects to | Gateway",
  "Gateway | sends | Events",
  "Event | calls | Coroutine handler",
  "on_ready | fires after | Cache is filled",
  "on_message | needs | message_content intent",
  "client.run | blocks until | Bot stops",
  "Token | identifies | Your bot"]),
 ["discord.py is an asynchronous Python library for the Discord API. You create a Client, give it intents, register event handlers, and call run with your bot token.",
  "The client keeps a websocket connection, called the gateway, open to Discord. Discord pushes events down it, such as a message being sent, and the library calls your matching coroutine.",
  "The repository at github.com/Rapptz/discord.py was at version 2.8.0a in its development branch when this course was written. The quickstart says to avoid naming your own file discord.py."],
 [("Client", "The object that connects to Discord and dispatches events to your handlers."),
  ("Gateway", "The websocket connection over which Discord pushes events to the bot."),
  ("Event handler", "An async function named on_<event>, registered with client.event."),
  ("Coroutine", "A function defined with async def, run by the event loop and paused with await."),
  ("Snowflake", "A 64-bit id used for users, guilds, channels and messages; its top bits hold a timestamp.")],
 ["Create intents, then Client(intents=intents), then client.run(token).",
  "Handlers are coroutines named on_ready, on_message and so on.",
  "Always ignore your own messages so the bot does not reply to itself.",
  "Never name your script discord.py.",
  "Snowflake time = (id >> 22) + 1420070400000 milliseconds."],
 [T("Think of the bot as a person sitting by a telephone. The Client dials Discord once and keeps the line open. Whenever something happens in a server, Discord speaks down the line, and the library turns each sentence into a call to one of your functions."),
  T("Your functions are coroutines. They are defined with async def, and they pause with await when they need to wait for the network, so one bot can handle many events at once on a single thread without blocking."),
  C("import discord\n\nintents = discord.Intents.default()\nintents.message_content = True\n\nclient = discord.Client(intents=intents)\n\n@client.event\nasync def on_ready():\n    print('Logged on as', client.user)\n\n@client.event\nasync def on_message(message):\n    if message.author == client.user:\n        return\n    if message.content.startswith('$hello'):\n        await message.channel.send('Hello!')\n\nclient.run('your token here')", "python"),
  T("This is the quickstart bot. The first lines build the intents, the next create the client, and the two decorated functions are event handlers. The check on the author matters: without it the bot could answer its own replies forever."),
  T("on_ready fires once the client has logged in and filled its cache, but it can fire more than once after reconnects, so do not start one-time work there. A later chapter shows setup_hook, which runs exactly once."),
  T("Every id in Discord is a snowflake. The top bits are the number of milliseconds since the Discord epoch, 1 January 2015, so you can read when something was created from its id alone. Shift right by 22 bits and add the epoch.")],
 [("Which call starts the bot?", ["client.run(token)", "client.start_event()", "discord.go()", "client.print()"], 0, "run blocks."),
  ("Why check message.author == client.user?", ["To avoid the bot replying to itself", "To speed it up", "To find the token", "To get intents"], 0, "Loops."),
  ("What is the gateway?", ["The websocket that pushes events", "A REST endpoint for files", "A database", "A command prefix"], 0, "Live connection."),
  ("Why not name your file discord.py?", ["It shadows the library when you import it", "It is too long", "It is reserved by Discord", "It breaks the token"], 0, "Import shadowing."),
  ("A handler is registered with:", ["@client.event", "@client.token", "@client.guild", "@client.wait"], 0, "Decorator."),
  ("What does a snowflake contain in its top bits?", ["A timestamp", "The token", "The guild name", "A password"], 0, "Creation time.")],
 [("Client", "Connects to Discord and dispatches events"), ("on_ready", "Fires after login and cache fill; may repeat on reconnect"), ("Snowflake", "64-bit id with a timestamp in the top bits"), ("Discord epoch", "1 January 2015, 1420070400000 ms")],
 [MATCH("Match the piece", "Pair each term with its job.", [("Client", "connects and dispatches"), ("Gateway", "websocket event stream"), ("on_message", "runs when a message arrives"), ("Snowflake", "id carrying a timestamp")]),
  FILL("Basics", "A function defined with async def is a {{coroutine}}. The websocket connection to Discord is the {{gateway}}. Handlers are registered with the {{event}} decorator, and the bot starts with client.{{run}}(token)."),
  PL("Handler name", "Write handler_name(event): return 'on_' followed by the event name, for example 'message' gives 'on_message'.", "handler_name(event)", '''
def handler_name(event):
    return 'on_' + event
''', [['message'], ['ready'], ['member_join']], "Concatenate the prefix."),
  PL("Reply to a message?", "Write should_reply(author_id, bot_id, content, prefix): return True only when the author is not the bot and the content starts with the prefix.", "should_reply(author_id, bot_id, content, prefix)", '''
def should_reply(author_id, bot_id, content, prefix):
    if author_id == bot_id:
        return False
    return content.startswith(prefix)
''', [[1, 2, '$hello', '$'], [2, 2, '$hello', '$'], [1, 2, 'hello', '$'], [1, 2, '', '$']], "Check the author first."),
  PL("Snowflake time", "Write snowflake_seconds(sid): return the creation time of a snowflake as whole unix seconds. Shift sid right by 22 bits, add 1420070400000, divide by 1000 using //.", "snowflake_seconds(sid)", '''
def snowflake_seconds(sid):
    ms = (sid >> 22) + 1420070400000
    return ms // 1000
''', [[175928847299117063], [0], [4194304], [1000000000000000000]], "Shift, add, divide."),
  PL("Safe script name", "Write name_ok(filename): return False when the filename (ignoring case) is exactly 'discord.py' or 'discord', otherwise True.", "name_ok(filename)", '''
def name_ok(filename):
    n = filename.lower()
    return not (n == 'discord.py' or n == 'discord')
''', [['bot.py'], ['discord.py'], ['Discord.PY'], ['discord'], ['main.py']], "Shadowing."),
  ORDER("Starting a bot", "Put these in order.", ["Create intents", "Create the Client", "Register event handlers", "Call client.run(token)", "Gateway connects and on_ready fires"])]))


CHS.append(CH(
 "Intents and the developer portal",
 ("Intents", [
  "Intent | selects | Event groups",
  "Privileged intent | needs | Portal switch",
  "members | is | Privileged",
  "presences | is | Privileged",
  "message_content | is | Privileged",
  "100 guilds | triggers | Verification",
  "Missing intent | causes | Missing events"]),
 ["Intents tell Discord which groups of events your bot wants. Fewer intents mean less data, less memory, and fewer events to process.",
  "Three intents are privileged: presences, members and message_content. You must switch each on in the Bot tab of the developer portal and also enable it in code. Enabling only one side fails.",
  "Bots in more than 100 guilds need verification and approval before they can use privileged intents. Intents.default() turns on everything except the privileged three."],
 [("Intents", "Flags that choose which events Discord sends to the bot."),
  ("Privileged intent", "An intent that must be enabled in the developer portal: presences, members, message content."),
  ("Member cache", "The library's stored copy of guild members; controlled by the members intent and MemberCacheFlags."),
  ("Developer portal", "The Discord website where you create the application, the bot user and its token."),
  ("Verification", "Discord's review required once a bot is in more than 100 guilds.")],
 ["Intents.default() leaves out presences, members and message_content.",
  "Privileged intents need the portal toggle and the code flag.",
  "Without message_content, message.content is empty for most messages.",
  "Intents.none() plus the ones you need is the leanest start.",
  "Over 100 guilds: apply for verification."],
 [T("Imagine a mailroom that sorts mail into bins. Intents are the bins you ask to receive. If you ask only for guild messages and guild changes, the mailroom never sends you reactions, typing notices or member updates. That saves your bot work and saves Discord bandwidth."),
  T("Three bins hold sensitive material. presences shows who is online and what they are playing, members shows join and leave events and fills the member list, and message_content lets you read the text of messages. These are privileged, which means a person must approve them."),
  C("import discord\n\nintents = discord.Intents.none()\nintents.guilds = True\nintents.guild_messages = True\nintents.message_content = True   # also enable in the portal\n\n# or start from the default set\nintents = discord.Intents.default()\nintents.members = True           # privileged\n\nclient = discord.Client(intents=intents)", "python"),
  T("If you forget the portal switch the bot fails to connect with a privileged intents error. If you forget the code flag, events silently never arrive. When on_message fires but message.content is empty, the cause is nearly always a missing message_content intent."),
  T("The member cache needs the members intent. Without it the library cannot list everyone, but the author of a message is still given as a Member, built from the data in the message itself. You can narrow what is cached with MemberCacheFlags."),
  T("Choose intents from the events you handle. A moderation bot wants members and message_content; a slash command bot often needs neither, because interactions arrive without them.")],
 [("Which is a privileged intent?", ["message_content", "guilds", "guild_messages", "reactions"], 0, "Also members and presences."),
  ("Where do you enable privileged intents?", ["Portal Bot tab and in code", "Only in code", "Only in the portal", "In the token"], 0, "Both."),
  ("What does Intents.default() exclude?", ["The three privileged intents", "Guilds", "Messages", "Everything"], 0, "Safe defaults."),
  ("message.content is empty. Likely cause?", ["message_content intent missing", "Wrong prefix", "Bad token", "Old Python"], 0, "Check the intent."),
  ("At how many guilds is verification needed?", ["More than 100", "More than 10", "More than 1000", "Any"], 0, "100."),
  ("Do slash commands need message_content?", ["No, interactions do not", "Yes always", "Only in DMs", "Only with views"], 0, "Interactions carry their own data.")],
 [("Privileged intents", "presences, members, message_content"), ("Intents.none()", "Start empty, enable what you need"), ("100 guilds", "Verification threshold for privileged intents"), ("MemberCacheFlags", "Tunes what the member cache stores")],
 [APP("INTENTS", "Intents explorer", "Switch intents on and off and see which events your bot would receive."),
  MATCH("Match the intent", "Pair each event with the intent it needs.", [("on_member_join", "members"), ("on_presence_update", "presences"), ("reading message text", "message_content"), ("on_guild_join", "guilds")]),
  FILL("Intents", "The three {{privileged}} intents are presences, members and message content. They must be switched on in the {{portal}} and in {{code}}. Over {{100}} guilds a bot needs verification."),
  PL("Privileged ones", "Write privileged(intents): intents is a list of names; return the sorted list of those that are privileged ('presences', 'members', 'message_content'), without duplicates.", "privileged(intents)", '''
def privileged(intents):
    p = ['presences', 'members', 'message_content']
    out = []
    for i in intents:
        if i in p and i not in out:
            out.append(i)
    out.sort()
    return out
''', [[['guilds', 'members']], [['message_content', 'presences', 'members']], [[]], [['members', 'members']]], "Filter and sort."),
  PL("Event to intent", "Write intent_for(event): 'on_member_join' and 'on_member_remove' give 'members'; 'on_presence_update' gives 'presences'; 'on_message' gives 'guild_messages'; 'on_reaction_add' gives 'reactions'; anything else gives 'guilds'.", "intent_for(event)", '''
def intent_for(event):
    if event in ('on_member_join', 'on_member_remove'):
        return 'members'
    if event == 'on_presence_update':
        return 'presences'
    if event == 'on_message':
        return 'guild_messages'
    if event == 'on_reaction_add':
        return 'reactions'
    return 'guilds'
''', [['on_member_join'], ['on_message'], ['on_presence_update'], ['on_ready'], ['on_reaction_add']], "A small lookup."),
  PL("Can the bot connect?", "Write can_connect(code_flags, portal_flags): both are lists of privileged intent names. Return True when every name in code_flags is also in portal_flags.", "can_connect(code_flags, portal_flags)", '''
def can_connect(code_flags, portal_flags):
    for f in code_flags:
        if f not in portal_flags:
            return False
    return True
''', [[['members'], ['members', 'presences']], [['members'], []], [[], []], [['message_content', 'members'], ['members']]], "Subset check."),
  PL("Verification needed?", "Write needs_verification(guilds, uses_privileged): True when the bot is in more than 100 guilds and uses a privileged intent.", "needs_verification(guilds, uses_privileged)", '''
def needs_verification(guilds, uses_privileged):
    return guilds > 100 and uses_privileged
''', [[50, True], [101, True], [101, False], [100, True], [5000, True]], "Both conditions.")]))


CHS.append(CH(
 "commands.Bot and prefix commands",
 ("Prefix commands", [
  "commands.Bot | extends | Client",
  "Prefix | triggers | Commands",
  "@bot.command | registers | Command",
  "Context | wraps | Message and channel",
  "Converter | turns | Text into objects",
  "Check | guards | A command",
  "CommandError | reports | Failures"]),
 ["The commands extension adds a Bot class that extends Client with a command system. Messages that start with a prefix are parsed into a command name and arguments.",
  "Each command is a coroutine whose first parameter is a Context. Annotations such as int or discord.Member convert the text arguments for you, and checks decide who may run the command.",
  "Errors raised by conversion or checks arrive in an error handler as subclasses of CommandError, so you can answer with a friendly message instead of a traceback."],
 [("Bot", "A Client subclass from discord.ext.commands that parses commands from messages."),
  ("Context", "An object passed to a command holding the message, author, channel and a send method."),
  ("Converter", "A type annotation or class that turns an argument string into a Python object."),
  ("Check", "A predicate that must pass before a command runs, such as has_permissions."),
  ("Cooldown", "A limit on how often a command may be used.")],
 ["commands.Bot(command_prefix='!', intents=intents).",
  "A command is async def name(ctx, ...) with @bot.command().",
  "Quote arguments with spaces: !say \"hello world\".",
  "Annotations convert: int, float, discord.Member, discord.TextChannel.",
  "Handle on_command_error for BadArgument and MissingPermissions."],
 [T("The Bot class does the parsing a person would do by hand. It watches every message, checks whether it begins with your prefix, splits off the command name, then splits the rest into arguments, respecting quotation marks."),
  C("import discord\nfrom discord.ext import commands\n\nintents = discord.Intents.default()\nintents.message_content = True\nbot = commands.Bot(command_prefix='!', intents=intents)\n\n@bot.command()\nasync def add(ctx, a: int, b: int):\n    await ctx.send(str(a + b))\n\n@bot.command()\n@commands.has_permissions(kick_members=True)\nasync def warn(ctx, member: discord.Member, *, reason: str):\n    await ctx.send(member.display_name + ' warned: ' + reason)\n\nbot.run('token')", "python"),
  T("In add, the annotations int make the library convert both arguments, and if the text is not a number it raises BadArgument. In warn, a bare star means the last parameter swallows the rest of the message as one string, so reasons can contain spaces."),
  T("Checks are decorators. has_permissions tests the author's permissions, is_owner tests the bot owner, and cooldown limits use. A failed check raises a CommandError that you can catch in one central handler."),
  C("@bot.event\nasync def on_command_error(ctx, error):\n    if isinstance(error, commands.BadArgument):\n        await ctx.send('That is not a valid value.')\n    elif isinstance(error, commands.MissingPermissions):\n        await ctx.send('You lack permission.')\n    elif isinstance(error, commands.CommandOnCooldown):\n        await ctx.send('Try again in %.1f seconds.' % error.retry_after)\n    else:\n        raise error", "python"),
  T("A prefix can be a list or a function, and commands.when_mentioned_or('!') lets people either type the prefix or mention the bot. Because prefix commands read message text, they depend on the message_content intent, which is why many new bots prefer slash commands.")],
 [("What makes the last parameter take the whole rest of the line?", ["A bare * before it", "A decorator", "An int hint", "A cooldown"], 0, "Keyword-only star."),
  ("What does int in a parameter do?", ["Converts and raises BadArgument on failure", "Rounds", "Nothing", "Makes it optional"], 0, "Converter."),
  ("What is the first parameter of a command?", ["ctx", "self only", "message_content", "bot token"], 0, "Context."),
  ("How do you send errors a friendly reply?", ["on_command_error", "print", "restart", "intents"], 0, "Central handler."),
  ("Prefix commands depend on which intent?", ["message_content", "presences", "members", "none"], 0, "They read text."),
  ("What does has_permissions do?", ["Checks the invoking user's permissions", "Grants permissions", "Kicks users", "Mutes"], 0, "A check.")],
 [("Context", "Message, author, channel and send"), ("commands.when_mentioned_or", "Accept a mention or a prefix"), ("BadArgument", "Conversion failed"), ("CommandOnCooldown", "Used too soon; has retry_after")],
 [APP("ROUTER", "Command router", "Type messages and see how a prefix bot parses them into a command and arguments."),
  MATCH("Match the error", "Pair each situation with the error.", [("text is not a number", "BadArgument"), ("author lacks a permission", "MissingPermissions"), ("used again too soon", "CommandOnCooldown"), ("no such command", "CommandNotFound")]),
  FILL("Commands", "A command receives a {{ctx}} first. A bare {{star}} makes the last parameter take the rest of the line. A failed conversion raises {{BadArgument}}, and a cooldown error offers {{retry_after}}."),
  PL("Split a command", "Write parse(content, prefix): if content does not start with the prefix return []. Otherwise return the words after the prefix split on spaces, ignoring empty words.", "parse(content, prefix)", '''
def parse(content, prefix):
    if not content.startswith(prefix):
        return []
    rest = content[len(prefix):]
    return [w for w in rest.split(' ') if w != '']
''', [['!add 1 2', '!'], ['hello', '!'], ['!  ping', '!'], ['!', '!']], "Strip the prefix first."),
  PL("Quoted arguments", "Write split_args(s): split s on spaces, but keep text inside double quotes together as one argument (without the quote characters). Return a list of strings.", "split_args(s)", '''
def split_args(s):
    out = []
    cur = ''
    inq = False
    for ch in s:
        if ch == '"':
            inq = not inq
        elif ch == ' ' and not inq:
            if cur != '':
                out.append(cur)
            cur = ''
        else:
            cur += ch
    if cur != '':
        out.append(cur)
    return out
''', [['say "hello world" now'], ['a b c'], ['"one two"'], ['  x   y ']], "Track whether you are inside quotes."),
  PL("Convert an int", "Write to_int(text): return the integer if text is made of digits with an optional leading minus, otherwise return the string 'BadArgument'.", "to_int(text)", '''
def to_int(text):
    t = text
    if t.startswith('-'):
        t = t[1:]
    if t == '':
        return 'BadArgument'
    for ch in t:
        if ch not in '0123456789':
            return 'BadArgument'
    return int(text)
''', [['42'], ['-7'], ['abc'], ['3.5'], ['']], "Check every character."),
  PL("Cooldown", "Write retry_after(last_used, now, rate_seconds): return 0 if enough time passed since last_used, else the remaining seconds (as a number rounded to 1 decimal).", "retry_after(last_used, now, rate_seconds)", '''
def retry_after(last_used, now, rate_seconds):
    left = rate_seconds - (now - last_used)
    if left <= 0:
        return 0
    return round(left, 1)
''', [[10.0, 12.5, 5.0], [10.0, 20.0, 5.0], [0.0, 0.0, 3.0], [100.0, 100.25, 2.0]], "Remaining time, never negative.")]))


CHS.append(CH(
 "Cogs, extensions and setup_hook",
 ("Structure", [
  "Cog | groups | Commands and listeners",
  "Extension | is | A module with setup",
  "load_extension | imports | Extension",
  "setup | adds | Cog",
  "setup_hook | runs | Once at start",
  "reload_extension | applies | Code changes",
  "Listener | handles | Events in a cog"]),
 ["As a bot grows, one file becomes unmanageable. Cogs are classes that group related commands and listeners, and extensions are modules that can be loaded, unloaded and reloaded while the bot runs.",
  "An extension defines an async setup function that receives the bot and adds cogs. You load it with bot.load_extension('cogs.fun'), usually inside setup_hook, which runs once before the bot connects.",
  "Reloading an extension picks up new code without a restart, which makes development fast. A cog may also define cog-wide checks and an error handler."],
 [("Cog", "A class deriving from commands.Cog that groups commands, listeners and state."),
  ("Extension", "A Python module with a setup function that registers cogs on the bot."),
  ("setup_hook", "A coroutine on the Client or Bot that runs once, before connecting, ideal for loading extensions."),
  ("Listener", "A method in a cog decorated with commands.Cog.listener() that handles an event."),
  ("Reload", "Unload and load an extension again to apply edited code.")],
 ["class Fun(commands.Cog) holds commands; add it with await bot.add_cog(Fun(bot)).",
  "Extension file defines async def setup(bot).",
  "Load in setup_hook: await self.load_extension('cogs.fun').",
  "Use @commands.Cog.listener() for events inside cogs.",
  "load, unload and reload raise errors if already or not loaded."],
 [T("Picture a shop where every department has its own team. A cog is one team: it owns some commands, some event listeners and any state they share, such as a counter. The bot is the shop that hires the teams."),
  C("# cogs/fun.py\nfrom discord.ext import commands\n\nclass Fun(commands.Cog):\n    def __init__(self, bot):\n        self.bot = bot\n        self.count = 0\n\n    @commands.command()\n    async def ping(self, ctx):\n        self.count += 1\n        await ctx.send('pong %d' % self.count)\n\n    @commands.Cog.listener()\n    async def on_member_join(self, member):\n        print('welcome', member)\n\nasync def setup(bot):\n    await bot.add_cog(Fun(bot))", "python"),
  T("Inside a cog, commands take self first and then ctx. Events use the Cog.listener decorator instead of client.event, so many cogs can listen to the same event without replacing one another."),
  C("# main.py\nclass MyBot(commands.Bot):\n    async def setup_hook(self):\n        for ext in ('cogs.fun', 'cogs.admin'):\n            await self.load_extension(ext)\n\nbot = MyBot(command_prefix='!', intents=intents)", "python"),
  T("setup_hook runs once, before the websocket connects, so it is the right place to load extensions, open a database or start background tasks. on_ready is the wrong place for those because it can fire again after a reconnect."),
  T("While developing, call await bot.reload_extension('cogs.fun') from an owner-only command. Loading a name twice raises ExtensionAlreadyLoaded, and unloading one that is not loaded raises ExtensionNotLoaded.")],
 [("What does a cog group?", ["Commands, listeners and state", "Only tokens", "Only embeds", "Only intents"], 0, "A class."),
  ("What must an extension define?", ["async def setup(bot)", "def main()", "class Bot", "token"], 0, "The entry point."),
  ("Where should extensions be loaded?", ["setup_hook", "on_ready", "on_message", "a loop"], 0, "Runs once."),
  ("How do cogs handle events?", ["commands.Cog.listener()", "client.event", "bot.token", "ctx.send"], 0, "Many listeners allowed."),
  ("Loading the same extension twice raises:", ["ExtensionAlreadyLoaded", "BadArgument", "Forbidden", "Nothing"], 0, "Error."),
  ("What does reload_extension do?", ["Re-imports edited code live", "Restarts Python", "Logs out", "Deletes the cog"], 0, "No restart.")],
 [("Cog.listener", "Event handler inside a cog"), ("add_cog", "Registers a cog on the bot"), ("ExtensionNotLoaded", "Tried to unload or reload what is not loaded"), ("setup_hook", "One-time async startup")],
 [MATCH("Match the piece", "Pair each term with its role.", [("Cog", "class grouping commands"), ("Extension", "module with setup"), ("setup_hook", "one-time startup"), ("Cog.listener", "event handler in a cog")]),
  FILL("Cogs", "A {{cog}} is a class that groups related commands. An extension module must define {{setup}}. Load extensions in {{setup_hook}}, and use {{reload_extension}} to apply edits."),
  ORDER("Startup", "Order these.", ["Construct the Bot", "setup_hook runs", "load_extension imports a module", "setup adds the cog", "Gateway connects", "on_ready fires"]),
  PL("Module path", "Write ext_name(path): turn a file path such as 'cogs/fun.py' into the extension name 'cogs.fun'. Replace '/' with '.' and drop a trailing '.py'.", "ext_name(path)", '''
def ext_name(path):
    p = path
    if p.endswith('.py'):
        p = p[:-3]
    return p.replace('/', '.')
''', [['cogs/fun.py'], ['admin.py'], ['a/b/c.py'], ['cogs/fun']], "String edits."),
  PL("Who hears the event", "Write listeners_for(listeners, event): listeners is a list of [cog_name, event_name]. Return the sorted cog names that listen to that event.", "listeners_for(listeners, event)", '''
def listeners_for(listeners, event):
    out = []
    for cog, ev in listeners:
        if ev == event:
            out.append(cog)
    out.sort()
    return out
''', [[[['Fun', 'on_message'], ['Mod', 'on_message'], ['Fun', 'on_ready']], 'on_message'], [[['A', 'x']], 'y']], "Many cogs may listen."),
  PL("Extension manager", "Write manage(commands): start with nothing loaded. Each item is [action, name] with action load, unload or reload. Return a list of results: 'ok' normally; for load of a loaded name 'ExtensionAlreadyLoaded'; for unload or reload of a name that is not loaded 'ExtensionNotLoaded'. Reload keeps it loaded.", "manage(commands)", '''
def manage(commands):
    loaded = []
    out = []
    for action, name in commands:
        if action == 'load':
            if name in loaded:
                out.append('ExtensionAlreadyLoaded')
            else:
                loaded.append(name)
                out.append('ok')
        elif action == 'unload':
            if name not in loaded:
                out.append('ExtensionNotLoaded')
            else:
                loaded.remove(name)
                out.append('ok')
        else:
            if name not in loaded:
                out.append('ExtensionNotLoaded')
            else:
                out.append('ok')
    return out
''', [[[['load', 'a'], ['load', 'a'], ['reload', 'a'], ['unload', 'a'], ['unload', 'a']]], [[['reload', 'x']]], [[['load', 'a'], ['load', 'b'], ['unload', 'a'], ['load', 'a']]]], "Keep a list of loaded names.")]))


CHS.append(CH(
 "Slash commands and the command tree",
 ("Application commands", [
  "CommandTree | holds | Slash commands",
  "tree.sync | publishes | Commands to Discord",
  "Interaction | replaces | Context",
  "response.send_message | answers | Interaction",
  "describe | documents | Parameters",
  "Guild sync | is | Instant",
  "Global sync | takes | Up to an hour"]),
 ["Slash commands are registered with Discord, so users see them in a menu with descriptions and typed options. They arrive as interactions, not as messages, so they need no message content intent.",
  "You keep them in an app_commands.CommandTree, decorate functions with tree.command, and call tree.sync to publish them. Syncing to one test guild is instant, while global commands can take up to an hour to appear.",
  "Your handler receives an Interaction. You must respond within three seconds, either with response.send_message, or by deferring first if the work takes longer."],
 [("CommandTree", "The container that stores and syncs application commands."),
  ("Interaction", "The object received for a slash command, button or modal; used to respond."),
  ("Sync", "Sending the command definitions to Discord so they appear to users."),
  ("Defer", "Telling Discord you need more time; you then answer with a followup."),
  ("Ephemeral", "A response visible only to the user who triggered it.")],
 ["Create self.tree = app_commands.CommandTree(self) in your Client.",
  "Sync in setup_hook: copy_global_to(guild=...), then sync(guild=...).",
  "Respond to an interaction within 3 seconds.",
  "Use describe and rename for friendly options.",
  "Use ephemeral=True for private replies."],
 [T("A prefix command is plain chat text that the bot reads. A slash command is a form that Discord itself draws. Discord checks the options before your code runs, so you get typed values, and users get autocomplete for free."),
  C("import discord\nfrom discord import app_commands\n\nMY_GUILD = discord.Object(id=0)  # replace with your guild id\n\nclass MyClient(discord.Client):\n    def __init__(self, *, intents):\n        super().__init__(intents=intents)\n        self.tree = app_commands.CommandTree(self)\n\n    async def setup_hook(self):\n        self.tree.copy_global_to(guild=MY_GUILD)\n        await self.tree.sync(guild=MY_GUILD)\n\nclient = MyClient(intents=discord.Intents.default())\n\n@client.tree.command()\n@app_commands.describe(first='The first value', second='The second value')\nasync def add(interaction: discord.Interaction, first: int, second: int):\n    await interaction.response.send_message(str(first + second))", "python"),
  T("This follows the project's own example. Copying the global commands to your test guild and syncing there makes changes appear immediately, which is the way to develop. For release you sync globally and wait."),
  T("The type hints define the option types. A parameter with a default of None, or annotated Optional, becomes an optional option. Required options must come before optional ones, and descriptions are limited to 100 characters."),
  C("@client.tree.command()\nasync def slow(interaction: discord.Interaction):\n    await interaction.response.defer(ephemeral=True)\n    # ... work that takes a while ...\n    await interaction.followup.send('Done!')", "python"),
  T("If you do not respond within three seconds Discord shows the user that the application did not respond. Calling defer buys up to fifteen minutes, after which you send the real answer with followup.send.")],
 [("Which intent do slash commands need to be read?", ["None for the command itself", "message_content", "members", "presences"], 0, "Interactions."),
  ("Where do slash commands live?", ["app_commands.CommandTree", "commands.Cog only", "the token", "on_ready"], 0, "The tree."),
  ("What publishes the commands?", ["tree.sync", "client.run", "copy_global", "describe"], 0, "Sync."),
  ("How long to answer an interaction?", ["3 seconds, or defer", "1 hour", "10 minutes", "No limit"], 0, "Defer for more."),
  ("Fastest way to test a command?", ["Sync to one guild", "Sync globally and wait", "Restart Discord", "Use prefix"], 0, "Guild sync is instant."),
  ("What does ephemeral=True do?", ["Only the user sees the reply", "Deletes the bot", "Pins it", "Mentions everyone"], 0, "Private.")],
 [("tree.sync", "Publish command definitions"), ("copy_global_to", "Copy global commands to a guild for fast testing"), ("defer", "Ask for more time to respond"), ("followup", "Send a message after deferring")],
 [MATCH("Match the call", "Pair each need with the call.", [("answer right now", "response.send_message"), ("need more time", "response.defer"), ("describe an option", "app_commands.describe"), ("publish commands", "tree.sync")]),
  FILL("Slash", "Slash commands are stored in a {{CommandTree}}. You publish them with tree.{{sync}}. Answer within {{3}} seconds, or call {{defer}} first."),
  PL("Valid command name", "Write name_ok(name): True when 1 to 32 characters, all lowercase letters, digits, '-' or '_'.", "name_ok(name)", '''
def name_ok(name):
    if len(name) < 1 or len(name) > 32:
        return False
    for ch in name:
        if not (ch in 'abcdefghijklmnopqrstuvwxyz0123456789-_'):
            return False
    return True
''', [['add'], ['Add'], [''], ['a-b_c1'], ['x' * 33], ['two words']], "Check length and characters."),
  PL("Option order", "Write order_ok(params): params is a list of [name, required]. Return True when no required parameter comes after an optional one.", "order_ok(params)", '''
def order_ok(params):
    seen_optional = False
    for name, required in params:
        if not required:
            seen_optional = True
        elif seen_optional:
            return False
    return True
''', [[[['a', True], ['b', False]]], [[['a', False], ['b', True]]], [[]], [[['a', True], ['b', True]]]], "Once optional, always optional."),
  PL("Description length", "Write describe_ok(text): True when the description has 1 to 100 characters.", "describe_ok(text)", '''
def describe_ok(text):
    return 1 <= len(text) <= 100
''', [['The first value'], [''], ['x' * 100], ['x' * 101]], "Bounds."),
  PL("When will it appear", "Write appears(scope, minutes_since_sync): scope is 'guild' or 'global'. Return True for guild always; for global True only when minutes_since_sync is at least 60 (the worst case).", "appears(scope, minutes_since_sync)", '''
def appears(scope, minutes_since_sync):
    if scope == 'guild':
        return True
    return minutes_since_sync >= 60
''', [['guild', 0], ['global', 5], ['global', 60], ['global', 120]], "Guild sync is instant."),
  PL("Respond in time", "Write reply_plan(seconds_needed): return 'send' when the work takes under 3 seconds, otherwise 'defer'.", "reply_plan(seconds_needed)", '''
def reply_plan(seconds_needed):
    if seconds_needed < 3:
        return 'send'
    return 'defer'
''', [[0.5], [2.9], [3], [30]], "Three seconds.")]))
