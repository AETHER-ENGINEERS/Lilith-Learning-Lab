# -*- coding: utf-8 -*-
"""discord.py course, part 2: views, modals and embeds, tasks and logging, security."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Views, buttons and select menus",
 ("Components", [
  "View | holds | Components",
  "Button | calls | Callback",
  "Select | offers | Choices",
  "timeout | disables | View",
  "custom_id | makes | View persistent",
  "5 per row | limits | Buttons",
  "edit_message | updates | The message"]),
 ["A View is a container for interactive components such as buttons and select menus. You attach it to a message, and each component calls one of your coroutines when a user presses it.",
  "Views time out after 180 seconds by default, after which the buttons stop working. A persistent view sets timeout to None, gives every item a custom_id and is registered at startup so it survives restarts.",
  "Discord limits a message to five rows with five buttons each, so at most 25 buttons, and a select menu takes a whole row."],
 [("View", "A discord.ui.View: a set of components attached to one message."),
  ("Button", "A clickable component declared with the discord.ui.button decorator."),
  ("Select", "A dropdown menu component with up to 25 options."),
  ("custom_id", "A string of up to 100 characters that identifies a component across restarts."),
  ("Persistent view", "A view with timeout None and fixed custom ids, re-registered when the bot starts.")],
 ["Subclass discord.ui.View and decorate methods with discord.ui.button.",
  "Handler signature: (self, interaction, button).",
  "Respond with interaction.response.edit_message(view=self).",
  "Default timeout is 180 seconds; use None plus custom_id for persistence.",
  "Maximum 25 buttons: five rows of five."],
 [T("A message can carry little controls, like a remote control stuck to it. In discord.py each control is a component and the whole set is a View. When someone presses a button Discord sends an interaction, and the library calls the method you decorated."),
  C("import discord\n\nclass Counter(discord.ui.View):\n    @discord.ui.button(label='0', style=discord.ButtonStyle.red)\n    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):\n        number = int(button.label) if button.label else 0\n        button.label = str(number + 1)\n        if number + 1 >= 5:\n            button.style = discord.ButtonStyle.green\n        await interaction.response.edit_message(view=self)\n\n# in a command:  await ctx.send('Press!', view=Counter())", "python"),
  T("This mirrors the project's counter example. The button changes its own label, and edit_message redraws the message with the updated view. Notice that the button is a parameter, so the same method can change its own style and label."),
  T("A view only lives as long as the bot's memory and its timeout. When the timeout passes, on_timeout is called and the buttons stop responding. For menus that must live forever, give timeout=None, set a custom_id on each item and call bot.add_view in setup_hook."),
  T("Use interaction_check to limit who may press: return False for anyone except the person who started the command. That stops other users from confirming someone else's action."),
  T("Layout is automatic, filling rows left to right, but you can set row explicitly. A select menu occupies a full row, so a message can hold five selects, or four selects and a row of buttons, up to five rows in total.")],
 [("How many buttons fit in one message?", ["25", "5", "100", "10"], 0, "Five rows of five."),
  ("Default view timeout?", ["180 seconds", "5 seconds", "1 hour", "Never"], 0, "Three minutes."),
  ("What makes a view persistent?", ["timeout=None and custom_ids, added at startup", "Only a bigger timeout", "ephemeral=True", "A cog"], 0, "Survives restarts."),
  ("How to update the message after a click?", ["interaction.response.edit_message", "print", "ctx.reload", "bot.sync"], 0, "Edit."),
  ("Which method limits who can press?", ["interaction_check", "on_ready", "describe", "defer"], 0, "Return False to block."),
  ("How wide is a select menu in the layout?", ["A whole row", "One slot", "Half a row", "Two rows"], 0, "Full row.")],
 [("custom_id", "Stable identifier, up to 100 characters"), ("on_timeout", "Called when a view expires"), ("interaction_check", "Gate who may use the view"), ("add_view", "Re-register a persistent view")],
 [APP("INTENTS", "Intents explorer", "A second look at how intents choose events; try a reaction bot configuration."),
  MATCH("Match the setting", "Pair each need with the setting.", [("buttons survive restarts", "timeout=None and custom_id"), ("only the author may press", "interaction_check"), ("redraw after a click", "edit_message"), ("limit of buttons", "25")]),
  FILL("Views", "A {{View}} holds components. The default {{timeout}} is 180 seconds. A persistent view needs a {{custom_id}} on every item. A message holds at most {{25}} buttons."),
  PL("Rows needed", "Write rows_needed(buttons): each row holds 5 buttons. Return the number of rows needed, or -1 if more than 25 buttons.", "rows_needed(buttons)", '''
def rows_needed(buttons):
    if buttons > 25:
        return -1
    return (buttons + 4) // 5
''', [[0], [1], [5], [6], [25], [26]], "Ceiling division."),
  PL("Counter button", "Write press(label, presses): the label is the current number as text. Apply the given number of presses and return [new_label, style] where style is 'green' when the new number is 5 or more, otherwise 'red'.", "press(label, presses)", '''
def press(label, presses):
    n = int(label) + presses
    style = 'green' if n >= 5 else 'red'
    return [str(n), style]
''', [['0', 1], ['4', 1], ['0', 5], ['7', 0]], "Add, then choose the style."),
  PL("Persistent?", "Write is_persistent(timeout, ids): ids is a list of custom_id values (None where unset). Return True only when timeout is None and every id is a non-empty string.", "is_persistent(timeout, ids)", '''
def is_persistent(timeout, ids):
    if timeout is not None:
        return False
    for i in ids:
        if i is None or i == '':
            return False
    return True
''', [[None, ['a', 'b']], [180, ['a']], [None, ['a', None]], [None, []], [None, ['']]], "Both conditions."),
  PL("Who may press", "Write may_press(user_id, owner_id, allow_all): True when allow_all is true or the user is the owner.", "may_press(user_id, owner_id, allow_all)", '''
def may_press(user_id, owner_id, allow_all):
    return allow_all or user_id == owner_id
''', [[1, 1, False], [2, 1, False], [2, 1, True]], "Like interaction_check.")]))


CHS.append(CH(
 "Modals, embeds and message limits",
 ("Rich messages", [
  "Modal | collects | Text input",
  "TextInput | has | max_length",
  "Embed | formats | Rich content",
  "Embed total | limit is | 6000 characters",
  "Message | limit is | 2000 characters",
  "Fields | limit is | 25",
  "on_submit | receives | Answers"]),
 ["A Modal is a popup form. You declare TextInput fields on a class, show the modal in response to an interaction, and receive the typed answers in on_submit.",
  "An Embed is a formatted card with a title, description, fields, colour and footer. Discord limits sizes: a description up to 4096 characters, field values up to 1024, a footer up to 2048, at most 25 fields, and 6000 characters across the whole embed.",
  "Ordinary message text is limited to 2000 characters, so long output must be split."],
 [("Modal", "A popup form with text inputs, shown in response to an interaction."),
  ("TextInput", "A modal field with a label, placeholder, style and length limits."),
  ("Embed", "A rich card attached to a message."),
  ("Field", "A name and value pair inside an embed, optionally inline."),
  ("Chunking", "Splitting long text into pieces that fit the message limit.")],
 ["Modal subclass with title and TextInput attributes.",
  "Show it with interaction.response.send_modal(Feedback()).",
  "Embed limits: 4096 description, 1024 field value, 25 fields, 6000 total.",
  "Message text limit is 2000 characters.",
  "A modal can only be opened from an interaction, not from a plain message."],
 [T("A modal asks several questions at once. You write a class with one TextInput per question, and when the user presses submit Discord sends all the answers back together so your on_submit method can read them."),
  C("import discord\n\nclass Feedback(discord.ui.Modal, title='Feedback'):\n    name = discord.ui.TextInput(label='Name', placeholder='Your name here...')\n    feedback = discord.ui.TextInput(\n        label='What do you think?',\n        style=discord.TextStyle.long,\n        placeholder='Type your feedback here...',\n        required=False,\n        max_length=300)\n\n    async def on_submit(self, interaction: discord.Interaction):\n        await interaction.response.send_message('Thanks, %s!' % self.name.value, ephemeral=True)\n\n# await interaction.response.send_modal(Feedback())", "python"),
  T("This follows the repository's modal example. Each TextInput is a class attribute, and after submission its value property holds what the person typed. Use max_length and required to validate on the client side."),
  C("embed = discord.Embed(title='Server stats', description='Updated hourly', colour=discord.Colour.blurple())\nembed.add_field(name='Members', value='120', inline=True)\nembed.add_field(name='Online', value='34', inline=True)\nembed.set_footer(text='Powered by discord.py')\nawait ctx.send(embed=embed)", "python"),
  T("Embeds are rejected if any limit is exceeded, and the total of all text across the embed may not pass 6000 characters. The library exposes len(embed) so you can check before sending."),
  T("Plain messages are limited to 2000 characters. To send longer text, split it at line breaks so no piece exceeds the limit, and send the pieces in order. Never split in the middle of a word if you can avoid it.")],
 [("How do you open a modal?", ["interaction.response.send_modal", "ctx.send", "bot.run", "embed.add_field"], 0, "From an interaction."),
  ("Where do typed values appear?", ["TextInput.value in on_submit", "ctx.args", "embed", "intents"], 0, "Read after submit."),
  ("Maximum embed fields?", ["25", "5", "100", "10"], 0, "Twenty-five."),
  ("Maximum message length?", ["2000 characters", "500", "4096", "10000"], 0, "Ordinary text."),
  ("Total embed text limit?", ["6000 characters", "2000", "100", "1024"], 0, "Across all parts."),
  ("Can a plain message open a modal?", ["No, only an interaction", "Yes", "Only in DMs", "Only with views"], 0, "Needs an interaction.")],
 [("discord.TextStyle.long", "Multi-line modal input"), ("add_field", "Adds a name/value field to an embed"), ("Colour.blurple", "Discord's brand colour"), ("len(embed)", "Total text length for the limit check")],
 [MATCH("Match the limit", "Pair each item with its limit.", [("message text", "2000"), ("embed description", "4096"), ("field value", "1024"), ("fields per embed", "25")]),
  FILL("Rich", "A popup form is a {{Modal}}. Answers arrive in {{on_submit}}. Plain text is limited to {{2000}} characters, and an embed may hold {{25}} fields."),
  PL("Embed problems", "Write embed_problems(description, field_count, field_value_lengths): return a sorted list of problem names: 'description' if description is longer than 4096; 'fields' if field_count is over 25; 'value' if any field value length is over 1024. Empty list if all fine.", "embed_problems(description, field_count, field_value_lengths)", '''
def embed_problems(description, field_count, field_value_lengths):
    out = []
    if len(description) > 4096:
        out.append('description')
    if field_count > 25:
        out.append('fields')
    for n in field_value_lengths:
        if n > 1024:
            if 'value' not in out:
                out.append('value')
    out.sort()
    return out
''', [['hi', 3, [10, 20]], ['x' * 4097, 26, [2000]], ['ok', 25, [1024]], ['', 0, []]], "Three independent checks."),
  PL("Chunk a message", "Write chunk(text, limit): split text into pieces each at most limit characters, breaking only at newline characters where possible. Lines are separated by '\\n'. A piece is built by adding whole lines; a single line longer than limit is cut into limit sized parts. Return the list of pieces (without trailing newlines).", "chunk(text, limit)", '''
def chunk(text, limit):
    out = []
    cur = ''
    for line in text.split('\\n'):
        while len(line) > limit:
            if cur != '':
                out.append(cur)
                cur = ''
            out.append(line[:limit])
            line = line[limit:]
        if cur == '':
            cur = line
        elif len(cur) + 1 + len(line) <= limit:
            cur = cur + '\\n' + line
        else:
            out.append(cur)
            cur = line
    if cur != '':
        out.append(cur)
    return out
''', [['aaa\nbbb\nccc', 7], ['abcdefghij', 4], ['x', 10], ['one\ntwo', 3]], "Fill each piece with whole lines."),
  PL("Modal check", "Write modal_ok(values, required, max_len): values and required are dicts name to text and name to bool; max_len is a number. Return the sorted list of field names that fail: required but empty, or longer than max_len.", "modal_ok(values, required, max_len)", '''
def modal_ok(values, required, max_len):
    bad = []
    for name in values:
        v = values[name]
        if required.get(name, False) and v == '':
            bad.append(name)
        elif len(v) > max_len:
            bad.append(name)
    bad.sort()
    return bad
''', [[{'name': 'Ann', 'feedback': ''}, {'name': True, 'feedback': False}, 300], [{'name': '', 'feedback': 'x' * 301}, {'name': True, 'feedback': False}, 300]], "Two rules per field."),
  PL("Embed fields layout", "Write inline_rows(count): inline fields show up to 3 per row. Return the number of rows needed for count inline fields.", "inline_rows(count)", '''
def inline_rows(count):
    return (count + 2) // 3
''', [[0], [1], [3], [4], [7]], "Ceiling division by 3.")]))


CHS.append(CH(
 "Background tasks, logging and error handling",
 ("Reliability", [
  "tasks.loop | repeats | Coroutine",
  "before_loop | waits for | Ready",
  "Logging | records | Library activity",
  "log_handler | configures | client.run",
  "Backoff | spaces | Retries",
  "Forbidden | means | Missing access",
  "HTTPException | wraps | API errors"]),
 ["The tasks extension runs a coroutine on a fixed schedule, such as every 60 seconds. You start it in setup_hook and make it wait until the bot is ready before it touches channels.",
  "discord.py uses the standard logging module. By default client.run sets up a handler and a level for you; you can pass your own log_handler and log_level, or pass log_handler=None to configure logging yourself.",
  "Network calls fail in predictable ways. Forbidden means the bot lacks access, NotFound means the object is gone, and HTTPException covers other API errors. Retrying should back off instead of hammering Discord."],
 [("tasks.loop", "A decorator that repeats a coroutine on an interval."),
  ("before_loop", "A hook that runs before the loop begins, often awaiting wait_until_ready."),
  ("Logging", "Python's standard logging; discord.py logs its gateway and HTTP activity under 'discord'."),
  ("Forbidden", "The error raised when the bot lacks permission or access."),
  ("Backoff", "Waiting longer after each failed attempt.")],
 ["@tasks.loop(seconds=60) repeats; start with .start() in setup_hook.",
  "@loop.before_loop: await self.wait_until_ready().",
  "client.run(token, log_handler=handler, log_level=logging.DEBUG).",
  "log_handler=None disables the default setup.",
  "Catch Forbidden, NotFound and HTTPException around API calls."],
 [T("Some jobs must happen on a schedule, such as posting a daily summary. The tasks extension wraps a coroutine in a loop that sleeps between runs and recovers from many transient errors for you."),
  C("import discord\nfrom discord.ext import tasks\n\nclass MyClient(discord.Client):\n    def __init__(self, *args, **kwargs):\n        super().__init__(*args, **kwargs)\n        self.counter = 0\n\n    async def setup_hook(self):\n        self.my_background_task.start()\n\n    @tasks.loop(seconds=60)\n    async def my_background_task(self):\n        channel = self.get_channel(1234567)  # replace with a channel id\n        self.counter += 1\n        await channel.send(str(self.counter))\n\n    @my_background_task.before_loop\n    async def before_my_task(self):\n        await self.wait_until_ready()", "python"),
  T("This is the project's background task example. before_loop waits until the cache is ready, because get_channel returns None until the guilds are loaded. Also remember that a loop keeps running until you call cancel on it."),
  C("import logging\nhandler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')\nclient.run(token, log_handler=handler, log_level=logging.DEBUG)", "python"),
  T("The documentation also describes discord.utils.setup_logging for use when you do not call run, and a root_logger option if you want your own modules to share the same handler. Raise the level to DEBUG while diagnosing a problem."),
  T("When an API call fails, catch the narrowest error you can. Forbidden means fix permissions, not retry. For a transient HTTPException, wait, double the wait on each failure, cap it, and give up after a few tries.")],
 [("How often does tasks.loop(seconds=60) run?", ["Every 60 seconds", "Once", "Every hour", "On every message"], 0, "Interval."),
  ("Why await wait_until_ready in before_loop?", ["get_channel is None until cached", "To log in", "To sync commands", "To hide the token"], 0, "Cache."),
  ("How to stop the default logging setup?", ["log_handler=None", "log_level=0", "intents.none()", "Delete discord.log"], 0, "Configure yourself."),
  ("Forbidden means:", ["The bot lacks access", "The server is down", "The token expired", "A typo"], 0, "Fix permissions."),
  ("Good retry strategy?", ["Exponential backoff with a cap", "Retry instantly forever", "Never retry", "Restart the bot"], 0, "Be polite."),
  ("Where to start a loop?", ["setup_hook", "on_message", "a view", "the portal"], 0, "Once.")],
 [("tasks.loop", "Repeating coroutine"), ("wait_until_ready", "Await the cache being filled"), ("log_level", "Minimum severity logged"), ("NotFound", "The object does not exist")],
 [MATCH("Match the error", "Pair each error with the right response.", [("Forbidden", "fix permissions"), ("NotFound", "skip or clean up"), ("HTTPException 5xx", "retry with backoff"), ("BadArgument", "tell the user")]),
  FILL("Reliability", "A repeating job uses {{tasks}}.loop. Wait for the cache with {{wait_until_ready}}. Turn off the default logging with log_handler={{None}}. Spacing retries out is called {{backoff}}."),
  PL("Loop runs", "Write loop_runs(elapsed, interval): the loop runs once immediately at start, then every interval seconds. Return how many runs happened after elapsed seconds.", "loop_runs(elapsed, interval)", '''
def loop_runs(elapsed, interval):
    return elapsed // interval + 1
''', [[0, 60], [59, 60], [60, 60], [185, 60]], "Floor division plus the first run."),
  PL("Backoff schedule", "Write backoff(attempts, base, cap): return the list of waits for that many retries; the first wait is base, each next doubles, and no wait exceeds cap.", "backoff(attempts, base, cap)", '''
def backoff(attempts, base, cap):
    out = []
    w = base
    for i in range(attempts):
        out.append(min(w, cap))
        w = w * 2
    return out
''', [[5, 1, 8], [3, 2, 100], [0, 1, 5], [4, 10, 25]], "Double, then clamp."),
  PL("Log filter", "Write visible(records, level): records is a list of [severity, text] with severity one of DEBUG, INFO, WARNING, ERROR in rising order. Return the texts whose severity is at or above level, keeping order.", "visible(records, level)", '''
def visible(records, level):
    order = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    min_i = order.index(level)
    out = []
    for sev, text in records:
        if order.index(sev) >= min_i:
            out.append(text)
    return out
''', [[[['DEBUG', 'a'], ['INFO', 'b'], ['ERROR', 'c']], 'INFO'], [[['WARNING', 'x']], 'ERROR'], [[['DEBUG', 'a']], 'DEBUG']], "Compare positions in the list."),
  PL("Pick a response", "Write on_error(name): 'Forbidden' gives 'fix permissions'; 'NotFound' gives 'skip'; 'HTTPException' gives 'retry'; 'BadArgument' gives 'tell user'; anything else gives 'raise'.", "on_error(name)", '''
def on_error(name):
    table = {'Forbidden': 'fix permissions', 'NotFound': 'skip', 'HTTPException': 'retry', 'BadArgument': 'tell user'}
    return table.get(name, 'raise')
''', [['Forbidden'], ['NotFound'], ['HTTPException'], ['BadArgument'], ['KeyError']], "A lookup with a default.")]))


CHS.append(CH(
 "Permissions, tokens and deployment",
 ("Security", [
  "Token | is | A password",
  "Permissions | are | A bitmask",
  "Administrator | overrides | All checks",
  "Least privilege | limits | Damage",
  "Environment | holds | Secrets",
  "Reset token | after | A leak",
  "Hosting | needs | Restart policy"]),
 ["Your bot token is a password. Anyone who has it can act as your bot. Keep it out of source control and out of screenshots, and read it from an environment variable or a secrets file.",
  "Discord permissions are bit flags combined in one integer. Administrator overrides all of the others. Ask for the minimum your bot needs when you generate the invite link, and check the bot's own permissions before you act.",
  "If a token leaks, regenerate it in the developer portal at once. A deployed bot needs a process manager or container that restarts it after a crash and keeps logs."],
 [("Token", "The secret string that logs your bot in."),
  ("Permission bitmask", "An integer where each bit is one permission."),
  ("Least privilege", "Granting only the permissions the bot needs."),
  ("Environment variable", "A process setting used to pass secrets without writing them in code."),
  ("Process manager", "A tool such as systemd or a container runtime that restarts the bot.")],
 ["Never hardcode or commit the token; read it from the environment.",
  "If it leaks, reset it in the developer portal immediately.",
  "Permissions are bits: administrator is 1 << 3, send_messages 1 << 11.",
  "Administrator overrides every other permission.",
  "Run under a supervisor with logs and a restart policy."],
 [T("A token is like the key to a building. If it is pasted into a public repository, bots scan for it within minutes and use it. Discord scans too and may reset leaked tokens, but do not rely on that. Treat the token like a password."),
  C("import os\nimport discord\n\ntoken = os.environ['DISCORD_TOKEN']\nintents = discord.Intents.default()\nclient = discord.Client(intents=intents)\nclient.run(token)\n\n# shell:\n#   export DISCORD_TOKEN='...'\n#   python bot.py", "python"),
  T("Add your .env file or secrets file to .gitignore, and keep a template without values in the repository. If the token ever appears in a log, a chat message or a commit, reset it and update the deployment."),
  T("Permissions are an integer where each bit is one capability, for example kick_members is bit one, administrator is bit three, view_channel is bit ten, send_messages is bit eleven and manage_messages is bit thirteen. You test one with a bitwise and."),
  T("Request only what you use. A music bot needs to connect and speak, not to ban members. When a command acts on a member, also check that the bot's role is above the target's role, or Discord will refuse with Forbidden."),
  T("In production run the bot under systemd, Docker or a hosting platform that restarts it and captures logs. Handle signals so it can close cleanly, and monitor for repeated reconnects, which can mean rate limits or a bad token.")],
 [("Where should the token live?", ["An environment variable or secrets file", "In the source file", "In a screenshot", "In the README"], 0, "Not in code."),
  ("What do you do after a token leak?", ["Reset it in the portal", "Ignore it", "Rename the bot", "Add a prefix"], 0, "Regenerate."),
  ("Which permission overrides the rest?", ["administrator", "send_messages", "view_channel", "embed_links"], 0, "All-powerful."),
  ("How do you test a permission bit?", ["Bitwise and with the mask", "String compare", "Addition", "A coroutine"], 0, "Mask."),
  ("Why a process manager?", ["Restarts the bot and keeps logs", "Makes it faster", "Hides the token", "Syncs commands"], 0, "Uptime."),
  ("Kick fails with Forbidden. Why?", ["Bot role is not above the target", "Wrong prefix", "No embed", "Old Python"], 0, "Role order.")],
 [("Bitwise and", "Tests whether a flag is set"), ("systemd", "A Linux service manager that can restart a bot"), (".gitignore", "Keeps secret files out of git"), ("Role hierarchy", "A bot can only manage roles and members below its highest role")],
 [APP("ROUTER", "Command router", "Final practice: route a few messages through prefix and slash handling."),
  MATCH("Match the practice", "Pair each risk with the safeguard.", [("leaked token", "reset it"), ("too many powers", "least privilege"), ("crash at night", "process manager restart"), ("secret in git", ".gitignore and env vars")]),
  FILL("Security", "The bot token is like a {{password}}. Store it in an {{environment}} variable. Ask for {{least}} privilege. The {{administrator}} permission overrides all others."),
  PL("Has a permission", "Write has_perm(mask, name): name is one of kick_members (bit 1), ban_members (2), administrator (3), view_channel (10), send_messages (11), manage_messages (13), manage_roles (28). Return True if the bit is set or if the administrator bit is set; False for an unknown name.", "has_perm(mask, name)", '''
def has_perm(mask, name):
    bits = {'kick_members': 1, 'ban_members': 2, 'administrator': 3, 'view_channel': 10, 'send_messages': 11, 'manage_messages': 13, 'manage_roles': 28}
    if name not in bits:
        return False
    if (mask >> 3) & 1:
        return True
    return ((mask >> bits[name]) & 1) == 1
''', [[1 << 11, 'send_messages'], [1 << 3, 'ban_members'], [0, 'kick_members'], [1 << 10, 'send_messages'], [1 << 10, 'nothing']], "Shift and mask; administrator first."),
  PL("Build a mask", "Write make_mask(names): combine the permissions into one integer using these bits: kick_members 1, ban_members 2, administrator 3, view_channel 10, send_messages 11, manage_messages 13, manage_roles 28. Ignore unknown names.", "make_mask(names)", '''
def make_mask(names):
    bits = {'kick_members': 1, 'ban_members': 2, 'administrator': 3, 'view_channel': 10, 'send_messages': 11, 'manage_messages': 13, 'manage_roles': 28}
    m = 0
    for n in names:
        if n in bits:
            m = m | (1 << bits[n])
    return m
''', [[['view_channel', 'send_messages']], [[]], [['administrator']], [['kick_members', 'nope', 'manage_roles']]], "OR the bits together."),
  PL("Missing permissions", "Write missing(mask, needed): needed is a list of permission names from the same table (kick_members 1, ban_members 2, administrator 3, view_channel 10, send_messages 11, manage_messages 13, manage_roles 28). Return the sorted list of names not granted. Administrator grants all.", "missing(mask, needed)", '''
def missing(mask, needed):
    bits = {'kick_members': 1, 'ban_members': 2, 'administrator': 3, 'view_channel': 10, 'send_messages': 11, 'manage_messages': 13, 'manage_roles': 28}
    if (mask >> 3) & 1:
        return []
    out = []
    for n in needed:
        if ((mask >> bits[n]) & 1) == 0 and n not in out:
            out.append(n)
    out.sort()
    return out
''', [[(1 << 10) | (1 << 11), ['view_channel', 'send_messages', 'manage_messages']], [8, ['ban_members']], [0, ['kick_members', 'ban_members']]], "Check each needed bit."),
  PL("Config source", "Write get_token(env, file_value): return env['DISCORD_TOKEN'] if present and non-empty; otherwise file_value if non-empty; otherwise the string 'missing'.", "get_token(env, file_value)", '''
def get_token(env, file_value):
    t = env.get('DISCORD_TOKEN', '')
    if t != '':
        return t
    if file_value != '':
        return file_value
    return 'missing'
''', [[{'DISCORD_TOKEN': 'abc'}, 'zzz'], [{}, 'zzz'], [{}, ''], [{'DISCORD_TOKEN': ''}, 'f']], "Environment first."),
  PL("Role above target", "Write can_act(bot_top, target_top, bot_has_perm): True only when the bot has the permission and its highest role position is greater than the target's.", "can_act(bot_top, target_top, bot_has_perm)", '''
def can_act(bot_top, target_top, bot_has_perm):
    return bot_has_perm and bot_top > target_top
''', [[5, 3, True], [3, 3, True], [5, 3, False], [1, 9, True]], "Hierarchy.")]))
