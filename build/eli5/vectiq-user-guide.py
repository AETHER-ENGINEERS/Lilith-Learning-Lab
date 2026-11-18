# -*- coding: utf-8 -*-
"""Expanded ELI5 blocks for the Vectiq course (one per chapter)."""
import re


def _split(t, lim=380):
    if len(t) <= lim:
        return [t]
    cuts = [m.end() for m in re.finditer(r"[.!?] (?=[A-Z(])", t)]
    if not cuts:
        return [t]
    k = min(cuts, key=lambda c: abs(c - len(t) / 2))
    return _split(t[:k].rstrip(), lim) + _split(t[k:], lim)


def E(pic, words, tryit, keep):
    return ("\n\n".join(_split(pic) + _split("Now the real words. " + words) + ["Try it. " + tryit, "If you remember one thing: " + keep]), "")


FEY = [
 E('You are hiring a helper for your clubhouse. You give the helper their own key card, not yours, and a desk that stays open. If the desk is closed, the helper is not there.', 'Vectiq runs on a computer that stays on, with its own Vector account. You install it, put its key in .env, invite it, and test with !ping.', 'Say why the bot needs its own key.', 'Own account, always-on computer, !ping.'),
 E('A control panel with lots of switches. A helper walks you through them one at a time. If you set a dial to nonsense, a checker tells you in words before anything breaks.', 'Settings live in config.yaml. Use the wizard, or edit, run the checker, then reload. Module switches need a restart.', 'Write the three steps for changing a setting safely.', 'Edit, check, reload.'),
 E('The door of a clubhouse. First someone says hello, then checks your ticket, then offers you a badge for your hobby.', 'Welcome greets, verification proves you are a person, and onboarding with a role menu lets you pick roles by tapping reactions.', "Write a welcome message using the member's name.", 'Greet, prove, pick.'),
 E("A teacher's notebook with numbered pages. Every page says who, what, when and why. After three pages about the same child, something happens.", 'Moderation actions are cases. Warnings escalate at the threshold, timeouts mute for a while, tempbans lift themselves, and softbans repeat.', 'Say what happens at warning number six by default.', 'Every action is a case, and warnings escalate.'),
 E("A shop with a bouncer who reads labels, a memory for troublemakers' faces, and a watcher who notices bad behaviour. At first they only write notes.", 'Link safety, image guard and Sentire protect the community. Start every rule with action log and read the log before deleting.', 'Say why writing notes first is wise.', 'Log first, delete later.'),
 E('An arcade. You earn tickets for playing, you can save or spend them on prizes, and visiting every day earns a little extra.', 'Chatting gives XP and levels, !daily and !work give coins, a streak adds a bonus, and the shop sells items that can give roles.', 'Work out how many coins a streak of three days pays.', 'XP for chatting, coins for claiming.'),
 E('Planning a party. You send invitations, people tick yes or maybe, you remind them the day before, and if the room is small, extra guests wait in line.', 'Events have RSVPs, a waitlist, reminders and repeats. Set the time zone once. Giveaways and polls are quick extras.', 'Write an event line with a title, a time and a length.', 'Set the zone first.'),
 E('A help desk where each customer gets a numbered booth and a staff member says I will take this one. Afterwards the notes are filed.', 'Tickets are private channels you open, claim and close, with a transcript kept. The security cam is a separate tool that copies everything to a staff channel.', 'Say who can see a ticket.', 'Open, claim, close.'),
 E('A games room with a referee holding the dice, a music corner with a queue, and a notice board that adds new posts without repeating old ones.', 'Games, music and feed alerts are modules. The bot is the referee. Music needs ffmpeg and yt-dlp. New feeds do not flood the channel.', 'Name the four games.', 'The bot is the referee.'),
 E('The control room of a theatre with screens for every part of the show, a doorbell for visitors, and a key you can hand to a trusted helper.', 'The dashboard manages the bot in a browser. Webhooks let tools post in. MCP lets an assistant manage the community with a token.', 'Say what you do before exposing the dashboard.', 'Lock the control room.'),
 E("A shop owner who locks up every night, keeps a copy of the accounts in another building, and reads the day's notes when something looks odd.", 'Restore points, updates and the log keep the bot healthy. Copy backups off the machine and read the log first.', 'List the three parts of the routine.', 'Save, read, copy.'),
]
