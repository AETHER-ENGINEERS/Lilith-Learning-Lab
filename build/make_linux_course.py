#!/usr/bin/env python3
"""Build the Linux course. Usage: python3 make_linux_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "lxc"))
import cmk, lx1, lx2, labs_linux, app_shell  # noqa: E402

APPS = {}
for k, cfg in labs_linux.LABS.items():
    app_shell.make_shell(cfg, os.path.join(HERE, "lxc", "apps", "sh_%s.html" % k))
    APPS["__SH_%s__" % k] = "sh_%s.html" % k

PRONOUNCE = {
    "Linux": "linnux", "sudo": "sue doo", "chmod": "ch mod", "chown": "ch own", "chgrp": "ch grip", "grep": "grep", "sed": "sed", "awk": "awk", "/etc": "slash e t c",
    "/var": "slash var", "/usr": "slash user", "/tmp": "slash temp", "/dev": "slash dev", "/proc": "slash proc", "ssh": "S S H", "SSH": "S S H", "cron": "cron", "crontab": "cron tab",
    "systemd": "system dee", "systemctl": "system control", "journalctl": "journal control", "apt": "app tee", "dpkg": "D package", "dnf": "D N F", "nginx": "engine x", "stdin": "standard in",
    "stdout": "standard out", "stderr": "standard error", "bash": "bash", "umask": "you mask", "inode": "eye node", "PID": "pid", "UID": "U I D", "GID": "G I D", "ps": "P S", "df": "D F",
    "du": "D U", "wc": "W C", "tty": "T T Y", "ufw": "U F W", "DNS": "D N S", "CIDR": "cider", "HTTP": "H T T P", "HTTPS": "H T T P S", "TCP": "T C P", "IP": "I P", "TERM": "term",
    "SIGKILL": "sig kill", "SIGTERM": "sig term", "SIGINT": "sig int", "SIGHUP": "sig hup", "kernel": "kernel", "Debian": "deb ee un", "Ubuntu": "oo boon too", "Fedora": "fe door uh",
    "logrotate": "log rotate", "fstab": "F S tab", "dev/null": "dev null", "setuid": "set U I D", "sudoers": "sue doo ers", "usermod": "user mod", "useradd": "user add", "groupadd": "group add",
    "pwd": "P W D", "ls": "L S", "cd": "C D", "cat": "cat", "rm": "R M", "mv": "M V", "cp": "C P", "xargs": "ex args", "uniq": "unique", "tr": "T R", "ss": "S S", "scp": "S C P", "rsync": "R sync",
}

SANDBOX = cmk.terminal("Linux cheat sheet", "linux>", "A scripted lookup, not a real machine. Try: nav, files, view, pipes, perms, users, procs, apt, systemd, net, scripts", [
    ("nav", ["pwd, ls -la, cd dir, cd .., cd ~", "Tab completes, Ctrl+C stops, Ctrl+L clears"]),
    ("files", ["mkdir -p, touch, cp -r, mv, rm -r, find . -name '*.txt'", "ln -s target link"]),
    ("view", ["cat, head -n, tail -n, tail -f, less, grep -rin pattern dir", "> replaces, >> appends, 2> errors, 2>&1 both"]),
    ("pipes", ["cmd | sort | uniq -c | sort -rn | head", "awk '{print $1}', cut -d: -f1, sed 's/a/b/g', tr a-z A-Z, wc -l"]),
    ("perms", ["r=4 w=2 x=1; 755 = rwxr-xr-x, 644 = rw-r--r--, 600 = rw-------", "chmod u+x f, chown user:group f, umask 022"]),
    ("users", ["id, whoami, groups, sudo cmd, useradd -m, usermod -aG grp user", "/etc/passwd, /etc/group, /etc/sudoers"]),
    ("procs", ["ps aux, top, kill PID (TERM 15), kill -9 PID (KILL), cmd &, jobs", "$? is the last exit code, 0 is success"]),
    ("apt", ["sudo apt update, apt install, apt remove, apt search", "dnf on Fedora, apk on Alpine"]),
    ("systemd", ["systemctl status|start|stop|restart|enable|disable name", "journalctl -u name -n 20"]),
    ("net", ["ip addr, ping -c 2 host, curl url, ss -tln", "22 ssh, 80 http, 443 https, 53 dns"]),
    ("scripts", ["#!/bin/bash, chmod +x, ./script.sh, $1 $# $?", "for x in list; do ...; done, while [ test ]; do ...; done, set -e"]),
])

EXAM = [
 ("What is Linux, strictly speaking?", ["A kernel", "A desktop", "A shell", "A text editor"], 0, "A distribution bundles it with tools."),
 ("What is at the top of the Linux filesystem tree?", ["/", "C:", "/home", "/root only"], 0, "The root directory."),
 ("Where are configuration files normally kept?", ["/etc", "/tmp", "/dev", "/proc"], 0, "Etcetera."),
 ("Which command prints the current directory?", ["pwd", "cd", "ls", "path"], 0, "Print working directory."),
 ("What does cd .. do?", ["Goes to the parent", "Goes home", "Lists files", "Makes a folder"], 0, "Two dots."),
 ("Which command makes parent directories as needed?", ["mkdir -p", "mkdir -r", "touch -p", "cp -p"], 0, "p for parents."),
 ("Which command renames a file?", ["mv", "ren", "cp", "rn"], 0, "Move within a directory."),
 ("What does > do?", ["Replaces a file with the output", "Appends", "Reads input", "Pipes"], 0, "Overwrites."),
 ("What does >> do?", ["Appends to a file", "Replaces", "Deletes", "Reads"], 0, "Adds to the end."),
 ("What is stream number 2?", ["stderr", "stdout", "stdin", "stdlog"], 0, "Errors."),
 ("What does | do?", ["Feeds output into another command", "Joins files", "Writes a file", "Ends a command"], 0, "A pipe."),
 ("Why sort before uniq -c?", ["uniq only joins adjacent lines", "sort is faster", "uniq needs numbers", "It is a rule of bash"], 0, "Neighbours only."),
 ("What does awk '{print $2}' print?", ["The second column", "The second line", "Line two", "Nothing"], 0, "Field two."),
 ("What is mode 755?", ["rwxr-xr-x", "rw-r--r--", "rwx------", "r-xr-xr-x"], 0, "7=rwx, 5=r-x."),
 ("What is mode 600?", ["rw-------", "rwx------", "r--r--r--", "rw-rw----"], 0, "Owner read/write only."),
 ("What does chmod u+x do?", ["Adds execute for the owner", "Removes execute", "Changes the owner", "Hides the file"], 0, "u is the owner."),
 ("What does execute mean on a directory?", ["You may enter it", "You may delete it", "You may run it", "Nothing"], 0, "Traverse."),
 ("What is the UID of root?", ["0", "1", "1000", "100"], 0, "Zero."),
 ("What does usermod -aG g u do?", ["Adds u to group g, keeping others", "Replaces groups", "Deletes u", "Renames g"], 0, "-a appends."),
 ("Why prefer sudo over logging in as root?", ["Least privilege and an audit log", "It is faster", "Root cannot log in", "No password needed"], 0, "Borrow power."),
 ("Which signal cannot be caught?", ["KILL", "TERM", "INT", "HUP"], 0, "Signal 9."),
 ("What does a trailing & do?", ["Runs in the background", "Pipes", "Redirects errors", "Appends"], 0, "Prompt returns."),
 ("What is PID 1?", ["init or systemd", "The shell", "The kernel", "cron"], 0, "Parent of all."),
 ("What is the exit code of success?", ["0", "1", "-1", "255"], 0, "Zero means success."),
 ("Which command installs a package on Debian?", ["apt install", "dnf install", "pacman -S", "apk add"], 0, "apt."),
 ("What does systemctl enable do?", ["Starts at boot", "Starts now", "Stops", "Installs"], 0, "Boot-time."),
 ("Where do most logs live?", ["/var/log", "/etc", "/bin", "/home"], 0, "Variable data."),
 ("What should a script's first line be?", ["#!/bin/bash", "//bash", "bash:", "run"], 0, "The shebang."),
 ("How do you read the first argument in a script?", ["$1", "$0", "$#", "$?"], 0, "Positional."),
 ("What is $?", ["The last exit code", "The argument count", "The PID", "The script name"], 0, "Exit status."),
 ("How many addresses in a /24?", ["256", "24", "255", "1024"], 0, "Eight host bits."),
 ("Which port does SSH use?", ["22", "80", "443", "53"], 0, "Secure shell."),
 ("What does connection refused mean?", ["Nothing listens on that port", "DNS failed", "Wrong password", "Disk full"], 0, "Reachable but no service."),
 ("Which command shows free disk space?", ["df -h", "du -f", "free", "ls -s"], 0, "Disk free."),
 ("When does '*/15 * * * *' run?", ["Every 15 minutes", "At minute 15", "Every 15 hours", "Never"], 0, "A step value."),
 ("Which is safer for SSH logins?", ["Keys with passwords off", "Short passwords", "Root login", "Shared accounts"], 0, "Keys."),
 ("What is least privilege?", ["Only the access needed", "Root everywhere", "No users", "Open ports"], 0, "Limits damage."),
 ("What does idempotent mean?", ["Running twice equals once", "Very fast", "Secret", "Needs root"], 0, "Safe to repeat."),
 ("What is a good first step before changing a system?", ["Observe its state", "Reboot", "Delete logs", "chmod 777"], 0, "Look first."),
 ("Why test restores of backups?", ["An untested backup may fail", "It is quick", "Law requires", "To free space"], 0, "Prove it works."),
]

CFG = dict(id="linux-from-scratch", title="Linux from Scratch: The Shell, Files, Permissions and Servers",
    subtitle="A hands-on tour of the Linux command line, with a working Linux-like shell in every lab",
    description="A condensed, original course on using and administering Linux. It covers the filesystem tree, the shell and its commands, files and directories, redirection and pipes, text tools, permissions and ownership, users and sudo, processes and signals, packages and services, shell scripting, networking basics, disks, logs and cron, security basics, and a capstone where you fix a broken server. Every shell lab runs a Linux-like simulator inside the app, built on the Jade Agent Kit virtual filesystem, with real BusyBox WebAssembly tools for grep, sed, awk and sort. It is a teaching sandbox, not a full Linux: some commands are simulated. Credits: BusyBox (GPL-2.0) and the Jade Agent Kit (MIT).",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="lxc", apps=APPS)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "linux-from-scratch.course.json")
    chs = lx1.A + lx2.B
    for ch in chs:  # shell labs are written inline in the lesson; labs belong in practice
        labs = [b for b in ch["lesson"] if b["type"] == "webxdc"]
        ch["lesson"] = [b for b in ch["lesson"] if b["type"] != "webxdc"]
        ch["practice"] = labs + ch["practice"]
    cmk.main(CFG, chs, [sys.argv[0], out])
