#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the vector-sdk-py course. Usage: python3 make_vector_sdk_py_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "vpy"))
import cmk, vpy_a, vpy_b, make_apps  # noqa: E402
make_apps.main()
CHS = vpy_a.CHS + vpy_b.CHS
PRONOUNCE = {"Vector": "vec tor", "vector-sdk-py": "vector S D K pie", "Nostr": "nos ter", "npub": "en pub", "nsec": "en sec", "PyO3": "pie oh three", "Rust": "rust", "maturin": "mat your in",
    "pytest": "pie test", "asyncio": "a sink eye oh", "async": "a sink", "await": "a wait", "wheel": "wheel", "abi3": "A B I three", "cmake": "see make", "Opus": "oh pus", "FFmpeg": "eff eff em peg",
    "PCM": "P C M", "kHz": "kilohertz", "WebXDC": "web X D C", "xdc": "X D C", "NIP-40": "nip forty", "ephemeral": "eh fem er al", "cogs": "cogs", "Cog": "cog", "Greedy": "greedy", "Literal": "literal",
    "whisper": "whisper", "Tor": "tor", "I2P": "eye two P", "SDK": "S D K", "API": "A P I", "DM": "D M", "DMs": "D Ms", "JSON": "jay son", "UI": "you eye", "npub1": "en pub one", "nsec1": "en sec one"}
SANDBOX = cmk.terminal("vector-sdk-py cheat sheet", "vpy>", "A scripted lookup. Try: install, key, run, command, hints, cog, cooldown, embed, view, community, voice, xdc, dev", [
    ("install", ["pip install git+https://github.com/lucky-edgelord/vector-sdk-py. Needs Rust and cmake. Python 3.9+. Opt-in: --features whisper,tor,i2p."]),
    ("key", ["vector.generate_nsec(). bot.run(nsec) or bot.run() to reuse the key in data_dir (default ./vector-bot-data). mnemonic= also works."]),
    ("run", ["bot = commands.Bot(command_prefix='!', invite_policy='public'); bot.run(os.environ.get('VECTOR_NSEC'))"]),
    ("command", ["@bot.command() async def ping(ctx): await ctx.reply('pong'). Also published as native /ping. Default prefix is '/'."]),
    ("hints", ["str=text, int=int, float=number, bool=flag, Member/User=user, Literal=choice, rest/args/Greedy=trailing text. Uppercase names or >8 args stay prefix only."]),
    ("cog", ["class X(commands.Cog) ... async def setup(bot): await bot.add_cog(X(bot)). Load in setup_hook."]),
    ("cooldown", ["@commands.cooldown(rate, per, commands.BucketType.user) raises CommandOnCooldown with retry_after."]),
    ("embed", ["vector.Embed(title=, description=, colour=) rendered as coloured markdown. delete_after sets a NIP-40 expiry and deletes."]),
    ("view", ["ui.View with @ui.button and @ui.select built from reactions. Buttons get A B C; options 1-10 then letters. ui.Modal asks questions in chat."]),
    ("community", ["create_role, set_permissions, member.timeout, guild.bulk_ban, audit_logs, guild.delete (dissolve, owner only)."]),
    ("voice", ["await vc.connect(); vc.play(FFmpegPCMAudio(path)); vc.utterances(); Transcriber needs the whisper build. 48 kHz mono 16-bit PCM."]),
    ("xdc", ["@bot.xdc_app('app-id') async def f(session): async for event in session: data, peer_join, peer_leave."]),
    ("dev", ["pip install maturin pytest pytest-asyncio; maturin develop --release; pytest tests (fake native bot)."]),
])
EXAM = [
 ("What powers vector-sdk-py underneath?", ["The Rust vector_sdk via PyO3", "discord.py", "Matrix", "A web API"], 0, "Compiled into the package."),
 ("What plays the role of the token?", ["The nsec key", "A password", "An API key", "An email"], 0, "A Nostr key."),
 ("What does Guild alias?", ["Community", "Channel", "Role", "Member"], 0, "Compatibility."),
 ("What happens to Intents?", ["Accepted and ignored", "Required", "Privileged", "Removed"], 0, "All events are sent."),
 ("Why is Rust needed to install?", ["The SDK is compiled", "For tests only", "For docs", "It is not needed"], 0, "Unless a wheel exists."),
 ("Default invite policy?", ["manual", "public", "whitelist", "none"], 0, "Fires on_community_invite."),
 ("run() with no key:", ["Reuses or creates the stored key", "Fails", "Uses a public key", "Prompts"], 0, "From data_dir."),
 ("A kick fires:", ["on_member_kick", "Only on_member_remove", "Nothing", "on_ban"], 0, "Separate event."),
 ("Default command prefix?", ["/", "!", "?", "None"], 0, "Native only."),
 ("Literal becomes:", ["A choice", "A flag", "A number", "A user"], 0, "Dropdown."),
 ("float becomes:", ["number", "int", "text", "flag"], 0, "Vector arg."),
 ("Which commands stay prefix only?", ["Uppercase names or over 8 args", "All", "None", "Those with str"], 0, "Cannot be native."),
 ("What must an extension define?", ["async def setup(bot)", "def main", "token", "class Bot"], 0, "Entry point."),
 ("A cooldown allows:", ["rate uses per period", "One use ever", "Unlimited", "Ten uses"], 0, "Token bucket."),
 ("owner_id takes:", ["An npub", "A number", "A name", "A URL"], 0, "Vector identity."),
 ("An Embed renders as:", ["Coloured markdown", "A PDF", "Nothing", "An image only"], 0, "No native embeds."),
 ("delete_after adds:", ["NIP-40 expiry and a delete", "A pin", "A reaction", "A ban"], 0, "Honoured by clients."),
 ("An ephemeral reply goes to:", ["The user's DMs", "The channel", "A file", "Nowhere"], 0, "Emulated."),
 ("Buttons are built from:", ["Reactions", "Native components", "Links", "Commands"], 0, "No components."),
 ("Buttons without emoji get:", ["Letters A B C", "Numbers", "Nothing", "Stars"], 0, "Regional letters."),
 ("A Modal is asked as:", ["Chat questions", "A popup", "A page", "A file"], 0, "Conversation."),
 ("bulk_ban gives:", ["One rekey for many bans", "A longer ban", "A list", "A mute"], 0, "Efficiency."),
 ("Who may dissolve a community?", ["The owner", "Any member", "Any admin", "The relay"], 0, "Irreversible."),
 ("Voice audio is:", ["48 kHz mono 16-bit PCM", "MP3", "Stereo 44.1 kHz", "Opus bytes"], 0, "Raw bytes."),
 ("Tests run against:", ["A fake native bot", "The live network", "A phone", "A browser"], 0, "No network needed."),
]
CFG = dict(id="vector-sdk-py", title="vector-sdk-py: discord.py-style Vector Bots",
    subtitle="Write Vector messenger bots in Python with the discord.py API, on top of the Rust vector_sdk, with Python labs",
    description="A hands-on course based on lucky-edgelord/vector-sdk-py (MIT, alpha), a discord.py-style Python library for Vector messenger bots built on the official Rust vector_sdk with PyO3. Learn the mapping from discord.py, installing and keys, events (including Vector's own), prefix and native slash commands with type hints, cogs, checks, cooldowns and tasks, embeds rendered as markdown, views built from reactions, community moderation, voice, Mini Apps and the development workflow. Labs run offline and simulate the library's rules in Python.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="vpy", apps={"__POLICY__": "policy.html", "__EVENTS__": "events.html", "__HINTS__": "hints.html", "__REACT__": "react.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "vector-sdk-py.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
