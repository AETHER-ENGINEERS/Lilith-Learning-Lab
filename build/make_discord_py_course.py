#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the discord.py course. Usage: python3 make_discord_py_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "dpy"))
import cmk, dpy_a, dpy_b, make_apps  # noqa: E402
make_apps.main()
CHS = dpy_a.CHS + dpy_b.CHS
PRONOUNCE = {"discord.py": "discord dot pie", "Discord": "discord", "asyncio": "a sink eye oh", "async": "a sink", "await": "a wait", "coroutine": "co roo teen", "Cog": "cog", "cogs": "cogs",
    "snowflake": "snow flake", "Snowflake": "snow flake", "ephemeral": "eh fem er al", "ephemeral=True": "ephemeral equals true", "Intents": "in tents", "intents": "in tents", "Modal": "moh dul",
    "setup_hook": "setup hook", "on_ready": "on ready", "on_message": "on message", "systemd": "system D", "bitmask": "bit mask", "Embed": "em bed", "embed": "em bed", "MemberCacheFlags": "member cache flags",
    "Rapptz": "rapps", "HTTP": "H T T P", "API": "A P I", "JSON": "jay son", "UI": "you eye", "CommandTree": "command tree", "nsec": "en sec"}
SANDBOX = cmk.terminal("discord.py cheat sheet", "bot>", "A scripted lookup. Try: install, minimal, intents, command, cog, slash, view, modal, task, logging, token, errors", [
    ("install", ["python3 -m pip install -U discord.py. Python 3.8 or newer. Do not name your script discord.py."]),
    ("minimal", ["intents = discord.Intents.default(); intents.message_content = True; client = discord.Client(intents=intents); client.run(token)."]),
    ("intents", ["Privileged: presences, members, message_content. Enable in the portal Bot tab and in code. Over 100 guilds needs verification."]),
    ("command", ["bot = commands.Bot(command_prefix='!', intents=intents); @bot.command() async def x(ctx, a: int): await ctx.send(...)"]),
    ("cog", ["class X(commands.Cog) with commands and Cog.listener(); extension defines async def setup(bot): await bot.add_cog(X(bot))."]),
    ("slash", ["self.tree = app_commands.CommandTree(self); @client.tree.command(); sync in setup_hook; respond within 3 seconds or defer."]),
    ("view", ["class V(discord.ui.View) with @discord.ui.button; timeout 180 s; persistent: timeout None plus custom_id plus add_view."]),
    ("modal", ["class M(discord.ui.Modal, title='...') with TextInput fields; open with interaction.response.send_modal; read in on_submit."]),
    ("task", ["@tasks.loop(seconds=60); start in setup_hook; @loop.before_loop await self.wait_until_ready()."]),
    ("logging", ["client.run(token, log_handler=handler, log_level=logging.DEBUG); log_handler=None to configure yourself."]),
    ("token", ["Read from the environment. Never commit it. If it leaks, reset it in the developer portal."]),
    ("errors", ["Forbidden: permissions. NotFound: gone. HTTPException: other API error. BadArgument: conversion. MissingPermissions: check failed."]),
])
EXAM = [
 ("What does client.run do?", ["Logs in, connects and blocks until the bot stops", "Prints the token", "Syncs commands", "Creates intents"], 0, "Blocking."),
 ("Why ignore your own messages?", ["Avoid reply loops", "Save memory", "Find the token", "Sync faster"], 0, "Loops."),
 ("Which intents are privileged?", ["presences, members, message_content", "guilds, messages, reactions", "only guilds", "none"], 0, "Three."),
 ("Where are privileged intents enabled?", ["Portal and code", "Only code", "Only portal", "The token"], 0, "Both."),
 ("What is a snowflake?", ["A 64-bit id with a timestamp", "A token", "A command", "A cog"], 0, "Ids."),
 ("What does an int hint do in a prefix command?", ["Converts or raises BadArgument", "Nothing", "Rounds", "Makes it private"], 0, "Converter."),
 ("What does a bare * do in a signature?", ["Last argument takes the rest of the line", "Multiplies", "Skips", "Makes it optional"], 0, "Keyword-only."),
 ("An extension must define:", ["async def setup(bot)", "def main", "class Bot", "a token"], 0, "Entry point."),
 ("Best place to load extensions?", ["setup_hook", "on_ready", "on_message", "a view"], 0, "Once."),
 ("Event handlers inside a cog use:", ["Cog.listener()", "client.event", "ctx.send", "bot.run"], 0, "Decorator."),
 ("Slash commands live in:", ["CommandTree", "Cog only", "Embed", "Modal"], 0, "Tree."),
 ("Fastest way to test slash commands?", ["Sync to one guild", "Global sync", "Prefix", "Restart"], 0, "Guild."),
 ("How long to respond to an interaction?", ["3 seconds, or defer", "1 minute", "1 hour", "Forever"], 0, "Defer."),
 ("Default view timeout?", ["180 seconds", "5 seconds", "1 hour", "None"], 0, "Three minutes."),
 ("Max buttons per message?", ["25", "5", "10", "100"], 0, "5 x 5."),
 ("Persistent view needs:", ["timeout None and custom_id, added at startup", "ephemeral", "a cog", "a modal"], 0, "Survives restart."),
 ("Message text limit?", ["2000 characters", "500", "4096", "256"], 0, "Chunk."),
 ("Embed total limit?", ["6000 characters", "2000", "10000", "100"], 0, "Total."),
 ("Modal values are read in:", ["on_submit via TextInput.value", "on_ready", "ctx.args", "intents"], 0, "Submit."),
 ("Why wait_until_ready in before_loop?", ["Cache is empty before then", "To log in", "To sync", "To hide token"], 0, "get_channel."),
 ("log_handler=None means:", ["Library does not set up logging", "No output ever", "Debug mode", "Log to file"], 0, "Your choice."),
 ("Forbidden means:", ["Missing access", "Server down", "Bad type", "Typo"], 0, "Permissions."),
 ("Token leaked. What now?", ["Reset it in the portal", "Ignore", "Rename bot", "Add prefix"], 0, "Reset."),
 ("Which overrides all permissions?", ["administrator", "send_messages", "view_channel", "embed_links"], 0, "Admin."),
 ("Why least privilege?", ["Limits damage if abused or leaked", "Faster", "Prettier", "Required by Python"], 0, "Safety."),
]
CFG = dict(id="discord-py", title="discord.py: Building Discord Bots",
    subtitle="Clients, intents, commands, cogs, slash commands, views, modals, tasks and deployment, with Python labs",
    description="A hands-on course based on the open-source discord.py library (github.com/Rapptz/discord.py, MIT), documented here as of its 2.8.0a development version. Learn how a bot connects, which intents it needs, how prefix and slash commands work, how to organise code with cogs and extensions, build buttons, selects and modals, run background tasks, log and handle errors, and keep tokens and permissions safe. Labs run offline and simulate the library's rules in Python, so no Discord account is needed.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="dpy", apps={"__INTENTS__": "intents.html", "__ROUTER__": "router.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "discord-py.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
