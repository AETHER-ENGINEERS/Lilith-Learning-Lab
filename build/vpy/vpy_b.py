# -*- coding: utf-8 -*-
"""vector-sdk-py course, part 2: embeds and messages, reaction views, communities, voice/xdc and testing."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Messages and embeds on a messenger without embeds",
 ("Messages", [
  "Embed | renders as | Coloured markdown",
  "Colour | paints | Title and bar",
  "Inline fields | sit | Side by side",
  "timestamp | shows in | Reader timezone",
  "delete_after | sets | NIP-40 expiry",
  "ephemeral | sends | A DM",
  "File | sends | Attachment"]),
 ["Vector has no embed objects, so vector.Embed keeps discord.py's full API but renders itself into Vector's markdown. The colour paints the title and a bar character down the left edge, inline fields sit side by side separated by a vertical line, and the timestamp is shown in each reader's own timezone.",
  "Sending works as you expect: send, reply, edit, history, purge, fetch_message, attachments with await attachment.read(), custom emoji reactions and typing indicators. delete_after sets a NIP-40 expiry that every client honours and also deletes the message after that many seconds.",
  "Other emulations are worth knowing: ephemeral replies are sent as a direct message, and deleting someone else's message hides it as a moderation action, while your own messages are really deleted."],
 [("Embed", "A rich card; here rendered as coloured markdown."),
  ("NIP-40", "The Nostr rule for event expiration; used for delete_after and expires_in."),
  ("Ephemeral", "A reply only the requester should see; sent as a DM in this library."),
  ("File", "vector.File wraps a path or bytes to attach to a message."),
  ("Link preview", "An image URL on its own line so Vector shows a preview.")],
 ["Embed API is discord.py's: add_field, set_author, set_footer, set_image, to_dict.",
  "Rendering: bar char, bold title in colour, inline fields joined with a bar.",
  "attachment://name plus file=vector.File(...) sends a real attachment.",
  "delete_after sets expiry and deletes; expires_in sets expiry only.",
  "ephemeral=True sends the reply to the user's DMs."],
 [T("An embed is just a pretty way to lay out information. Since Vector has no embed object, the library turns it into markdown that looks like one. You write the same code you would for discord.py and the library does the translation."),
  C("embed = vector.Embed(title=\"Server stats\", description=\"Updated hourly\", colour=0x59FCB3)\nembed.add_field(name=\"CPU\", value=\"12%\", inline=True)\nembed.add_field(name=\"RAM\", value=\"3.1 GB\", inline=True)\nembed.set_footer(text=\"vector-sdk-py\")\nembed.timestamp = vector.utils.utcnow()\nawait ctx.send(embed=embed)", "python"),
  T("The rendering puts a coloured bar at the left of every line, then the title in bold, then the description. Two inline fields are drawn on one line separated by a vertical bar. The timestamp uses a time tag, so each reader sees their own timezone."),
  T("To send an image as a real attachment, set the embed image to attachment colon slash slash and the file name, and pass the file with the message. The image goes first and the embed becomes its caption. A plain URL image is placed on its own line so Vector shows a link preview."),
  T("delete_after is stronger than its Discord cousin. It sets an expiry that every Vector client honours, so the message vanishes even if the bot is offline, and it also schedules a deletion. If you only want the expiry, use expires_in."),
  T("Because ephemeral replies become direct messages, think twice before using them in busy chats. And remember that deleting another person's message hides it as moderation rather than erasing it.")],
 [("What does an Embed render as?", ["Coloured markdown", "A PDF", "An image only", "Nothing"], 0, "No native embeds."),
  ("What does delete_after add?", ["A NIP-40 expiry and a deletion", "A reaction", "A pin", "A ban"], 0, "Honoured by clients."),
  ("Where does an ephemeral reply go?", ["The user's DMs", "The channel", "A file", "Nowhere"], 0, "Emulation."),
  ("How are inline fields drawn?", ["Side by side with a bar", "Stacked", "Hidden", "As images"], 0, "Separated by a vertical line."),
  ("What is the timestamp shown in?", ["Each reader's timezone", "UTC only", "The bot's timezone", "Not shown"], 0, "Time tag."),
  ("What does deleting another's message do?", ["Hides it as moderation", "Erases it from relays", "Nothing", "Bans them"], 0, "Not a true delete.")],
 [("attachment://", "Reference an uploaded file from an embed"), ("expires_in", "Set expiry only"), ("purge", "Bulk delete recent messages"), ("fetch_message", "Get a message by id")],
 [APP("HINTS", "Type hint mapper", "A quick look at how hints map; relevant to the command descriptions in embeds."),
  MATCH("Match the piece", "Pair each feature with how it behaves.", [("Embed colour", "title and left bar"), ("inline fields", "one line, bar between"), ("delete_after", "expiry and delete"), ("ephemeral", "sent as a DM")]),
  FILL("Messages", "An embed is rendered as {{markdown}}. The expiry rule is {{NIP-40}}. An ephemeral reply is sent as a {{DM}}. Use {{expires_in}} for expiry without scheduling a delete."),
  PL("Render an embed", "Write render(title, description, fields): return a list of lines. First '▍ **' + title + '**', then '▍ ' + description, then for each field [name, value] two lines '▍ **' + name + '**' and '▍ ' + value.", "render(title, description, fields)", '''
def render(title, description, fields):
    bar = '\\u258d'
    out = [bar + ' **' + title + '**', bar + ' ' + description]
    for name, value in fields:
        out.append(bar + ' **' + name + '**')
        out.append(bar + ' ' + value)
    return out
''', [['Stats', 'Hourly', [['CPU', '12%']]], ['T', 'D', []]], "Bar, bold title, description, fields."),
  PL("Inline row", "Write inline_row(fields): fields is a list of [name, value]. Return two lines: names joined as '**name**' with ' │ ' between, and values joined with ' │ '.", "inline_row(fields)", '''
def inline_row(fields):
    sep = ' \\u2502 '
    names = sep.join(['**' + n + '**' for n, v in fields])
    values = sep.join([v for n, v in fields])
    return [names, values]
''', [[[['CPU', '12%'], ['RAM', '3 GB']]], [[['A', '1']]]], "Join with the separator."),
  PL("Expiry seconds", "Write expiry_s(delete_after, expires_in): expires_in wins when given (not None); otherwise delete_after; round up to whole seconds; None if neither is given.", "expiry_s(delete_after, expires_in)", '''
def expiry_s(delete_after, expires_in):
    v = expires_in if expires_in is not None else delete_after
    if v is None or v == 0:
        return None
    i = int(v)
    if i < v:
        i += 1
    return i
''', [[5, None], [None, 2.2], [3, 10], [None, None]], "Ceiling of the chosen value."),
  PL("Where does it go?", "Write target(ephemeral, user, channel): the user's DMs when ephemeral, otherwise the channel.", "target(ephemeral, user, channel)", '''
def target(ephemeral, user, channel):
    return user if ephemeral else channel
''', [[True, 'u', 'c'], [False, 'u', 'c']], "Emulated privacy."),
  PL("Split long text", "Write chunks(text, size): split text into pieces of at most size characters; empty text gives an empty list.", "chunks(text, size)", '''
def chunks(text, size):
    out = []
    i = 0
    while i < len(text):
        out.append(text[i:i + size])
        i += size
    return out
''', [['abcdefg', 3], ['', 4], ['abc', 3]], "Step through.")]))


CHS.append(CH(
 "Views, buttons, selects and modals built from reactions",
 ("Interactive UI", [
  "View | holds | Buttons and selects",
  "Button | becomes | Reaction",
  "Select option | becomes | Numbered reaction",
  "Modal | becomes | Chat questions",
  "Paginator | uses | Arrow reactions",
  "interaction_check | gates | Who may click",
  "timeout | ends | The view"]),
 ["Vector has no message components, so vector.ui builds them from reactions. Each button or select option becomes an emoji reaction that the bot adds under the message, with a legend in the message text. Reacting clicks it, and removing your reaction clicks it again.",
  "Buttons without an emoji get regional letters A, B, C and so on. Select options get number emoji one to ten, then letters. A Modal asks its TextInput fields as a short chat conversation and then calls on_submit. ui.Paginator pages text or embeds with first, previous, next, last and stop reactions.",
  "timeout, on_timeout, interaction_check, stop, wait and interaction.response.edit_message all work as in discord.py."],
 [("Reaction button", "An emoji reaction added by the bot that acts as a button."),
  ("Legend", "The text in the message that explains which emoji does what."),
  ("Interaction", "The object passed to a callback when someone clicks."),
  ("Paginator", "A view that pages through a list of pages with arrow reactions."),
  ("Modal", "A form emulated as a conversation of questions.")],
 ["Same decorators as discord.py: @ui.button, @ui.select, ui.View, ui.Modal.",
  "Buttons: given emoji, else A B C. Options: 1 to 10, then letters.",
  "Reacting clicks; removing the reaction clicks again.",
  "ephemeral=True is sent as a DM.",
  "Reaction limits mean views should stay small."],
 [T("The trick is that reactions are the one interactive thing every message already has. The library adds one reaction per control and listens for people reacting. It feels like buttons even though the mechanism is different."),
  C("class Confirm(ui.View):\n    @ui.button(label=\"Confirm\", emoji=\"✅\", style=ui.ButtonStyle.success)\n    async def confirm(self, interaction: vector.Interaction, button: ui.Button):\n        await interaction.response.send_message(\"Done!\")\n        self.stop()\n\nawait ctx.send(\"Are you sure?\", view=Confirm(timeout=60))", "python"),
  T("The message text gets a legend such as a checkmark for confirm, so people know what each reaction does. When someone reacts, your callback runs with an interaction. Calling stop ends the view, and the bot removes its reactions."),
  T("Select menus use numbered reactions: an option without its own emoji gets the number for its position, from one to ten, and after ten the regional letters. Because reactions are limited, keep menus short, or use the Paginator."),
  T("A Modal is a conversation. The bot asks each TextInput as a short question, waits for the answer, then calls on_submit with all the values. It is slower than a popup but works anywhere a chat does."),
  T("Gate who may click with interaction_check, exactly as in discord.py. Without it, anyone who can react can click, so a confirm button in a public channel should check the user.")],
 [("What is a button here?", ["A reaction the bot adds", "A native component", "A link", "A command"], 0, "Emulation."),
  ("What do buttons without an emoji get?", ["Regional letters A B C", "Numbers", "Nothing", "Stars"], 0, "Letter emoji."),
  ("What do select options get?", ["Number emoji, then letters", "Letters only", "Colours", "Nothing"], 0, "One to ten first."),
  ("How is a Modal shown?", ["As chat questions", "A popup", "A web page", "A file"], 0, "Conversation."),
  ("What clicks a button again?", ["Removing your reaction", "Typing", "Waiting", "Nothing"], 0, "Both directions."),
  ("Which method restricts clickers?", ["interaction_check", "on_timeout", "stop", "wait"], 0, "Return False to block.")],
 [("ui.Paginator", "Reaction-driven pages"), ("self.stop()", "End the view"), ("view.wait()", "Await the view finishing"), ("ButtonStyle", "Style hint; shown in the legend")],
 [APP("REACT", "Reaction view simulator", "Add buttons and options and see which reactions the bot would place."),
  MATCH("Match the control", "Pair each control with its emulation.", [("Button", "emoji reaction"), ("Select option", "numbered reaction"), ("Modal", "chat questions"), ("Paginator", "arrow reactions")]),
  FILL("UI", "Views are built from {{reactions}}. Buttons without an emoji get {{letters}}. Select options get {{numbers}} first. Restrict clickers with {{interaction_check}}."),
  PL("Button emojis", "Write button_emojis(buttons): buttons is a list of emoji strings or empty strings. Buttons with an emoji keep it; those without get the next unused letter 'A', 'B', 'C' in order. Return the list.", "button_emojis(buttons)", '''
def button_emojis(buttons):
    used = [b for b in buttons if b != '']
    out = []
    n = 0
    for b in buttons:
        if b != '':
            out.append(b)
        else:
            letter = chr(65 + n)
            while letter in used:
                n += 1
                letter = chr(65 + n)
            out.append(letter)
            n += 1
    return out
''', [[['', '', '']], [['OK', '', 'X']], [[]], [['A', '', '']]], "Skip letters already used."),
  PL("Option marker", "Write option_marker(i): for index i from 0 to 9 return the number i+1 as text; for i 10 and above return a letter 'A', 'B', ... for i-10.", "option_marker(i)", '''
def option_marker(i):
    if i < 10:
        return str(i + 1)
    return chr(65 + i - 10)
''', [[0], [9], [10], [12]], "Numbers then letters."),
  PL("Who clicked?", "Write allowed(user, owner, only_owner): when only_owner is true only the owner may click; otherwise anyone.", "allowed(user, owner, only_owner)", '''
def allowed(user, owner, only_owner):
    if only_owner:
        return user == owner
    return True
''', [['a', 'a', True], ['b', 'a', True], ['b', 'a', False]], "Like interaction_check."),
  PL("Paginator", "Write page_after(page, pages, reaction): page is the current zero-based page, pages the count. 'first' gives 0, 'prev' gives page-1 but not below 0, 'next' gives page+1 but not past pages-1, 'last' gives pages-1, anything else leaves it unchanged.", "page_after(page, pages, reaction)", '''
def page_after(page, pages, reaction):
    if reaction == 'first':
        return 0
    if reaction == 'prev':
        return max(0, page - 1)
    if reaction == 'next':
        return min(pages - 1, page + 1)
    if reaction == 'last':
        return pages - 1
    return page
''', [[2, 5, 'prev'], [0, 5, 'prev'], [4, 5, 'next'], [1, 5, 'last'], [3, 5, 'first'], [3, 5, 'stop']], "Clamp at the ends."),
  PL("Modal answers", "Write ask(fields, answers): fields is a list of [name, required]; answers is a list of replies in order. Return [values, missing] where values pairs each name with its answer (an empty string if no answer) and missing is the list of required names with empty answers.", "ask(fields, answers)", '''
def ask(fields, answers):
    values = []
    missing = []
    for i in range(len(fields)):
        name, required = fields[i]
        a = answers[i] if i < len(answers) else ''
        values.append([name, a])
        if required and a == '':
            missing.append(name)
    return [values, missing]
''', [[[['name', True], ['note', False]], ['Ann']], [[['a', True]], []]], "Walk the fields in order.")]))


CHS.append(CH(
 "Communities and moderation",
 ("Communities", [
  "Community | is | Guild alias",
  "create_role | makes | Roles",
  "set_permissions | sets | Overwrites",
  "member.timeout | silences | A member",
  "audit_logs | lists | Actions",
  "bulk_ban | bans | One rekey",
  "guild.delete | dissolves | Community"]),
 ["Communities are richer than Discord guilds. You can create communities, join by invite link, preview an invite with fetch_invite, create invites with a lifetime and label, and manage roles, categories, text, voice and forum channels.",
  "Permissions work per channel with set_permissions and overwrites, and permissions_for tells you what someone may do. Moderation includes kick, ban, unban, bulk_ban for one key rotation, member.timeout, nicknames, pins, audit_logs and bans listings, and contain_raid.",
  "Recovery and operations tools include relay management with check_relays and move_relays, refound and repair_roster. leave removes the bot, and delete dissolves the community, which is irreversible and for the owner only."],
 [("Community", "A shared space with members, roles and channels."),
  ("Overwrite", "A per-channel permission change for a role or member."),
  ("Timeout", "A temporary silence applied to a member."),
  ("Audit log", "The list of recorded moderation and settings actions."),
  ("Bulk ban", "Banning many members with a single key rotation.")],
 ["create_community, join(invite_url), fetch_invite for a preview.",
  "create_role, create_text_channel, create_category, create_forum.",
  "channel.set_permissions(target, send_messages=False) locks a channel.",
  "member.timeout(timedelta), guild.bulk_ban(members), guild.audit_logs().",
  "guild.delete() dissolves a community; owner only, irreversible."],
 [T("Think of running a community as a set of small decisions: who may enter, what they can see, who may speak, and who can undo mistakes. The library exposes each one as a method on the objects you already know from discord.py."),
  C("@commands.command()\n@commands.has_permissions(manage_channels=True)\nasync def lock(self, ctx):\n    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)\n    await ctx.send(\"Channel locked\")\n\n@commands.command()\n@commands.has_permissions(moderate_members=True)\nasync def timeout(self, ctx, member: vector.Member, minutes: int = 10):\n    await member.timeout(datetime.timedelta(minutes=minutes))", "python"),
  T("The lock command in the moderation example denies the send permission to the default role in the current channel. The timeout command silences a member for a number of minutes. Both are guarded by permission checks."),
  T("When a wave of spam arrives, ban one account at a time and each ban rotates the community key. bulk_ban bans the whole list with a single rekey. contain_raid treats a raid as one moderation unit."),
  T("The audit log is an async iterator of entries with a user, an action and a time, which makes a handy command for admins. Because each moderation call is checked the way every member's client will judge it, a refused action raises an error that you should handle."),
  T("Dissolving a community with delete cannot be undone and only the owner may do it. Never wire it to a casual command. Require an explicit confirmation from a person, for example with a confirm view that only the owner may click.")],
 [("What does set_permissions change?", ["A channel overwrite", "The bot's key", "The invite", "The relay"], 0, "Per channel."),
  ("What is bulk_ban for?", ["Banning many with one rekey", "Banning forever", "Listing bans", "Muting"], 0, "Efficiency."),
  ("What does guild.delete do?", ["Dissolves the community", "Deletes a message", "Leaves", "Kicks"], 0, "Owner only."),
  ("Which method lists recorded actions?", ["audit_logs", "bans", "invites", "history"], 0, "Async iterator."),
  ("Which method previews an invite?", ["fetch_invite", "join", "create_invite", "leave"], 0, "Before joining."),
  ("What happens if a moderation action is refused?", ["An error is raised", "It silently succeeds", "The bot dissolves", "A retry loop"], 0, "Handle it.")],
 [("contain_raid", "Handle a raid as one unit"), ("refound", "Recovery tool for a community"), ("repair_roster", "Fix the member list"), ("system_channel", "Default channel for welcome messages")],
 [MATCH("Match the method", "Pair each need with the method.", [("lock a channel", "set_permissions"), ("silence a member", "timeout"), ("ban a wave", "bulk_ban"), ("list actions", "audit_logs")]),
  FILL("Moderation", "Lock a channel by denying {{send_messages}} to the default role. Ban many at once with {{bulk_ban}}. Silence a member with {{timeout}}. Only the owner may {{dissolve}} a community."),
  PL("Rekeys needed", "Write rekeys(bans, bulk): bans is the number of accounts to ban. One rekey each normally, one rekey in total when bulk is true (and zero if there are none).", "rekeys(bans, bulk)", '''
def rekeys(bans, bulk):
    if bans == 0:
        return 0
    return 1 if bulk else bans
''', [[5, False], [5, True], [0, True], [1, False]], "Bulk is one."),
  PL("Effective permission", "Write can_send(role_allows, channel_allow, channel_deny): True when (the role allows OR the channel allows) AND NOT the channel denies. All are booleans.", "can_send(role_allows, channel_allow, channel_deny)", '''
def can_send(role_allows, channel_allow, channel_deny):
    return (role_allows or channel_allow) and not channel_deny
''', [[True, False, False], [True, False, True], [False, True, False], [False, False, False]], "Deny wins."),
  PL("Timeout end", "Write timeout_active(until_minutes, now_minutes): True while now is before until.", "timeout_active(until_minutes, now_minutes)", '''
def timeout_active(until_minutes, now_minutes):
    return now_minutes < until_minutes
''', [[10, 5], [10, 10], [10, 20]], "Strictly before."),
  PL("Confirm dissolve", "Write may_dissolve(user, owner, confirmed): True only for the owner and only when a person confirmed.", "may_dissolve(user, owner, confirmed)", '''
def may_dissolve(user, owner, confirmed):
    return user == owner and confirmed
''', [['a', 'a', True], ['a', 'a', False], ['b', 'a', True]], "Owner and confirmed."),
  PL("Audit filter", "Write by_user(entries, user): entries is a list of [user, action]. Return the actions by that user in order.", "by_user(entries, user)", '''
def by_user(entries, user):
    return [a for u, a in entries if u == user]
''', [[[['a', 'kick'], ['b', 'ban'], ['a', 'pin']], 'a'], [[], 'x']], "Filter by user."),
  PL("Invite lifetime", "Write invite_valid(created, max_age, now): max_age 0 means never expires; otherwise valid while now minus created is less than max_age.", "invite_valid(created, max_age, now)", '''
def invite_valid(created, max_age, now):
    if max_age == 0:
        return True
    return (now - created) < max_age
''', [[0, 0, 9999], [0, 60, 30], [0, 60, 60], [100, 3600, 200]], "Zero means forever.")]))


CHS.append(CH(
 "Voice, Mini Apps, testing and contributing",
 ("Beyond text", [
  "VoiceChannel.connect | joins | A call",
  "vc.play | plays | PCM audio",
  "utterances | yields | Speaker clips",
  "Transcriber | needs | whisper build",
  "xdc_app | joins | Mini App session",
  "maturin develop | builds | The extension",
  "pytest | tests | Python layer"]),
 ["Voice works like discord.py. voice_channel.connect returns a client, vc.play plays an FFmpegPCMAudio source, and bots can also listen. Audio is 48 kHz mono 16-bit PCM bytes. utterances yields one clip per speaker per pause, and a Transcriber turns a clip into text in a whisper build.",
  "Mini Apps are WebXDC apps shared in a chat. Decorate an async function with bot.xdc_app(app_id) and iterate the session for data, peer_join and peer_leave events. Sessions end after idle or quiet timeouts.",
  "For development, install maturin and pytest, run maturin develop to build the Rust extension into your virtual environment, and run pytest. The Python layer is tested against a fake native bot, so most tests need no network."],
 [("PCM", "Raw audio samples; here 48 kHz mono 16-bit."),
  ("Utterance", "One speaker's clip, cut at a pause."),
  ("XdcSession", "The bot's live link to one open Mini App."),
  ("maturin", "Builds PyO3 projects into Python packages."),
  ("Fake native bot", "A test double that stands in for the Rust bot.")],
 ["PCM bytes: 48000 samples per second, mono, 2 bytes per sample.",
  "vc.play(FFmpegPCMAudio(path)); vc.say(pcm); vc.hush().",
  "@bot.xdc_app('id') async def f(session): async for event in session.",
  "event.type: data, peer_join, peer_leave; event.verified_sender names the sender.",
  "maturin develop --release; pytest tests."],
 [T("Voice turns the bot into a participant in a call. You connect to a voice channel, play audio, and listen. Everything is raw PCM, which keeps the interface simple: bytes in, bytes out. FFmpeg decodes files for you."),
  C("vc = await voice_channel.connect()\nvc.play(vector.FFmpegPCMAudio(\"song.mp3\"), after=lambda e: print(\"done\"))\n\nasync for member, pcm in vc.utterances():     # bots can listen\n    print(member, await transcriber.transcribe(pcm))", "python"),
  T("At 48 kilohertz mono with two bytes per sample, one second of audio is 96 thousand bytes. A twenty millisecond frame is 960 samples, which is 1920 bytes. Knowing these numbers helps when you buffer or cut clips."),
  C("@bot.xdc_app(\"vector-counter\")\nasync def counter(session: vector.XdcSession):\n    async for event in session:\n        if event.type == \"data\":\n            await session.send_json({\"echo\": event.json(), \"from\": event.verified_sender})", "python"),
  T("A Mini App is a small web app shared in a chat that everyone who opens it uses together. Your bot can be a referee, an opponent or the server behind it. Use verified_sender when you must trust who sent a message, and remember players can see each other's network addresses."),
  T("The repository is built for contributors. src is the PyO3 binding, python/vector is the API, and the tests use a fake native bot. A GitHub Actions workflow builds wheels for Linux, macOS and Windows. Add a test whenever you add a feature.")],
 [("What audio format does voice use?", ["48 kHz mono 16-bit PCM", "MP3", "Stereo 44.1 kHz", "Opus bytes"], 0, "Raw PCM."),
  ("Which build feature enables Transcriber?", ["whisper", "tor", "xdc", "i2p"], 0, "Opt-in."),
  ("How do you join Mini App sessions?", ["bot.xdc_app", "bot.voice", "bot.join_app", "ctx.xdc"], 0, "Decorator."),
  ("What builds the extension for development?", ["maturin develop", "make", "npm", "cargo test only"], 0, "Then run pytest."),
  ("What do the tests use?", ["A fake native bot", "The live network", "A browser", "A phone"], 0, "No network needed."),
  ("Does the library support live video for bots?", ["No", "Yes", "Only in DMs", "Only with whisper"], 0, "Rust SDK limit.")],
 [("verified_sender", "A sender you can trust in a Mini App message"), ("FFmpegPCMAudio", "Decodes audio files to PCM"), ("vc.hush", "Stop playing queued audio"), ("peer_join", "Someone joined the Mini App session")],
 [MATCH("Match the piece", "Pair each tool with its use.", [("maturin", "build the extension"), ("pytest", "run the tests"), ("FFmpegPCMAudio", "decode files"), ("Transcriber", "speech to text")]),
  FILL("Beyond text", "Voice audio is {{48}} kHz {{mono}} PCM. Mini Apps use bot.{{xdc_app}}. Build the extension with {{maturin}} develop. Test with {{pytest}}."),
  PL("Bytes of audio", "Write pcm_bytes(rate, ms): bytes for ms milliseconds of mono 16-bit audio at the given rate.", "pcm_bytes(rate, ms)", '''
def pcm_bytes(rate, ms):
    return rate * ms // 1000 * 2
''', [[48000, 1000], [48000, 20], [16000, 500]], "Two bytes per sample."),
  PL("Frames in a clip", "Write frames(rate, clip_ms, frame_ms): number of whole frames of frame_ms in a clip of clip_ms.", "frames(rate, clip_ms, frame_ms)", '''
def frames(rate, clip_ms, frame_ms):
    return clip_ms // frame_ms
''', [[48000, 1000, 20], [48000, 55, 20], [48000, 0, 20]], "Integer division."),
  PL("Session ends", "Write session_ended(idle_min, quiet_min, returned, idle_limit, quiet_limit): True when the handler returned, or idle_min is at least idle_limit, or quiet_min is at least quiet_limit.", "session_ended(idle_min, quiet_min, returned, idle_limit, quiet_limit)", '''
def session_ended(idle_min, quiet_min, returned, idle_limit, quiet_limit):
    return returned or idle_min >= idle_limit or quiet_min >= quiet_limit
''', [[0, 0, False, 3, 15], [3, 0, False, 3, 15], [0, 15, False, 3, 15], [0, 0, True, 3, 15]], "Three ways."),
  PL("Trusted event", "Write trust(event_type, verified_sender): data events from a verified sender give 'act'; data events without one give 'ignore'; peer_join and peer_leave give 'note'; anything else gives 'ignore'.", "trust(event_type, verified_sender)", '''
def trust(event_type, verified_sender):
    if event_type == 'data':
        return 'act' if verified_sender != '' else 'ignore'
    if event_type in ('peer_join', 'peer_leave'):
        return 'note'
    return 'ignore'
''', [['data', 'npub1x'], ['data', ''], ['peer_join', ''], ['other', 'x']], "Verify before acting."),
  PL("Test plan", "Write needs_network(test_kind): 'unit' and 'fake' give False; 'live' and 'relay' give True; anything else gives True.", "needs_network(test_kind)", '''
def needs_network(test_kind):
    if test_kind in ('unit', 'fake'):
        return False
    return True
''', [['unit'], ['fake'], ['live'], ['other']], "Fake native bot needs none.")]))
