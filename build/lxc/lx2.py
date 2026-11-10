"""Linux course, chapters 8-15. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *
from lx1 import SH

B = []

B.append(CH(
 "Processes, jobs and signals",
 ("Processes", ["Process | has | A PID", "ps | lists | Processes", "kill | sends | Signals", "SIGTERM | asks to | Stop", "SIGKILL | forces | Stop", "Background job | runs with | &"]),
 ["A process is a running program with its own number, the PID, an owner and its own memory. The first process, init or systemd, is PID 1 and starts the rest.",
  "ps shows a snapshot, top shows it live. kill does not just kill: it sends a signal. SIGTERM, the default, asks politely; SIGKILL cannot be ignored.",
  "Add & to run a command in the background so you keep your prompt."],
 [("PID", "Process id: the number the kernel uses to name a running program."), ("Signal", "A small message sent to a process, such as TERM or KILL."), ("Daemon", "A background process that provides a service."), ("Zombie", "A finished process whose parent has not yet collected its exit status.")],
 ["ps aux lists all processes.", "kill sends TERM (15) by default; kill -9 sends KILL.", "A trailing & runs a command in the background.", "Exit code 0 means success."],
 [T("Every command you run becomes a process. The kernel gives it a PID and records who started it, which is its owner. A process can start children. Your shell is the parent of the commands you type. When a parent ends, its children are adopted by PID 1."),
  C("ps                 # your own processes\nps aux             # every process, with owner and CPU use\nps -ef | grep ssh  # find one by name\ntop                # live view\nsleep 300 &        # run in the background\njobs               # background jobs of this shell\nkill 1234          # ask process 1234 to stop (TERM)\nkill -9 1234       # force it (KILL)"),
  T("Signals are numbered messages. 15 is TERM, a polite request that lets the program clean up. 2 is INT, what Ctrl+C sends. 1 is HUP, often used to make a daemon reload its settings. 9 is KILL, which the kernel carries out immediately and no program can catch, so it gives no chance to save work. Try TERM first, and use KILL only when a process refuses to stop."),
  T("You may only signal your own processes unless you are root. Every command also ends with an exit code, a number that the shell keeps in the variable $?. Zero means success and anything else means failure. Scripts and pipelines use this to decide what to do next."),
  SH("proc", "Lab: stop a runaway job", "Find the background process that is hogging the machine and stop it.")],
 [("Which signal cannot be caught?", ["KILL (9)", "TERM (15)", "INT (2)", "HUP (1)"], 0, "The kernel enforces it."), ("What does a trailing & do?", ["Runs the command in the background", "Joins two commands", "Redirects errors", "Appends to a file"], 0, "You get the prompt back."), ("What is PID 1?", ["The first process, init or systemd", "The shell", "The kernel", "Root's shell"], 0, "Parent of everything else.")],
 [("Default signal of kill?", "TERM, number 15."), ("What does Ctrl+C send?", "INT, signal 2."), ("Exit code of success?", "Zero."), ("List all processes?", "ps aux.")],
 [MATCH("Signals", "Match each signal with its use.", [("TERM 15", "Polite request to stop"), ("KILL 9", "Forced stop"), ("INT 2", "Ctrl+C"), ("HUP 1", "Reload configuration")]),
  PL("Find the hog", "Each line is 'pid cpu name' such as '312 8.5 python'. Write hog(lines) that returns the pid (as text) with the highest cpu. If the list is empty return ''.", "hog(lines)",
"""def hog(lines):
    best = ''
    top = -1.0
    for line in lines:
        f = line.split()
        c = float(f[1])
        if c > top:
            top = c
            best = f[0]
    return best
""", [[["312 8.5 python", "99 71.2 miner", "7 0.1 sshd"]], [[]], [["1 0.0 init"]]], "Track the biggest cpu seen so far and its pid.")]))

B.append(CH(
 "Packages and services",
 ("Packages", ["apt | installs | Packages", "Repository | hosts | Packages", "dpkg | installs | .deb files", "systemd | manages | Services", "systemctl | controls | Services", "journalctl | reads | Service logs"]),
 ["A package manager installs software, resolves what it depends on, and keeps it updated from trusted repositories. On Debian and Ubuntu that is apt.",
  "A service is a program that runs in the background, such as a web server. systemd starts services at boot and systemctl controls them.",
  "The pattern is always the same: install the package, start the service, enable it for boot, check its status and read its logs."],
 [("Package", "A bundle of files plus metadata such as version and dependencies."), ("Repository", "A server that holds signed packages."), ("systemd", "The init system that boots the machine and supervises services."), ("Unit", "A thing systemd manages, such as nginx.service.")],
 ["sudo apt update refreshes the list; apt install adds a package.", "systemctl start, stop, restart, status control a service.", "enable makes it start at boot; start runs it now.", "journalctl -u name reads its log."],
 [T("On Debian-style systems, apt update downloads the list of what is available, apt install name installs it and everything it needs, apt remove deletes it, and apt search finds names. All of these except search need root, so you write sudo in front. Packages are signed, so a repository cannot slip you something altered."),
  C("sudo apt update\nsudo apt install nginx\nsystemctl status nginx          # is it running?\nsudo systemctl start nginx      # run it now\nsudo systemctl enable nginx     # and at every boot\nsudo systemctl restart nginx    # after changing its config\njournalctl -u nginx -n 20       # the last 20 log lines"),
  T("systemd reads small unit files that say what to run, what it needs and when to restart it. Start means run now, enable means run at boot, and they are separate. A service can be enabled but stopped, or running but not enabled. After editing a unit file, run systemctl daemon-reload."),
  T("Other families use other tools with the same ideas: dnf or yum on Fedora and Red Hat, apk on Alpine, pacman on Arch. Learning one makes the others easy."),
  SH("svc", "Lab: install and run a web server", "Install nginx with apt, start it, enable it and fetch the page with curl.")],
 [("Which command refreshes the package list?", ["apt update", "apt upgrade-list", "apt refresh", "apt sync"], 0, "Update the index first."), ("What does enable do?", ["Starts the service at boot", "Starts it now", "Installs it", "Deletes it"], 0, "Boot-time behaviour."), ("Why does apt install need sudo?", ["It changes system files", "It is slow", "It uses the network", "It reads logs"], 0, "Only root may.")],
 [("Install a package?", "sudo apt install name."), ("Run a service now?", "systemctl start name."), ("See a service's logs?", "journalctl -u name."), ("Boot-time start?", "systemctl enable name.")],
 [MATCH("systemctl verbs", "Match each verb with its effect.", [("start", "Run it now"), ("stop", "Stop it now"), ("enable", "Start at boot"), ("status", "Show its state"), ("restart", "Stop then start")]),
  ORDER("Web server setup", "Put these steps in a sensible order.", ["sudo apt update", "sudo apt install nginx", "sudo systemctl enable nginx", "sudo systemctl start nginx", "curl http://localhost"])]))

B.append(CH(
 "Shell scripting I: variables, arguments and tests",
 ("Scripts", ["Script | is | A text file of commands", "Shebang | names | The interpreter", "Variable | stores | Text", "$1 | is | First argument", "if | tests | A condition", "Exit code | reports | Success or failure"]),
 ["A shell script is a text file of commands. Start it with a shebang line like #!/bin/bash, make it executable with chmod +x, and run it with ./script.sh.",
  "Variables hold text. Assign with name=value, no spaces, and read with $name. Arguments arrive as $1, $2 and so on, and $# is how many there are.",
  "if tests a condition, usually with [ ] and operators such as -f for file exists, -eq for equal numbers and = for equal text."],
 [("Shebang", "The first line #! followed by the interpreter, like #!/bin/bash."), ("Variable", "A named piece of text. You set it with name=value and read it with $name."), ("Argument", "A value passed on the command line, available as $1, $2, ..."), ("Test", "The [ ] command, which succeeds or fails depending on a condition.")],
 ["No spaces around = in an assignment.", "Quote variables: \"$name\".", "[ -f file ] tests that a file exists.", "$? holds the last exit code."],
 [T("A script is just commands you would otherwise type. Put #!/bin/bash on the first line so the system knows which interpreter to use, save the file, run chmod +x on it and start it with ./name.sh. The dot-slash is needed because the current directory is normally not on your command search path."),
  C("#!/bin/bash\n# greet.sh: say hello\nname=\"$1\"\nif [ -z \"$name\" ]; then\n  echo \"usage: $0 NAME\"\n  exit 1\nfi\necho \"Hello, $name!\"\necho \"You gave $# argument(s)\""),
  T("Variables have no spaces around the equals sign: name=Lilith works, name = Lilith does not. Always put double quotes around a variable when you use it, so that a value with spaces stays one word. Single quotes stop all expansion. $(command) captures a command's output, as in today=$(date)."),
  T("The test command, written [ ], returns success or failure. Useful tests: -f is a regular file, -d is a directory, -e exists, -z string empty, -n string not empty, = and != compare text, -eq -ne -lt -gt compare numbers. Combine with && for and, and || for or. Every command sets an exit code, readable as $?, and if looks at it."),
  SH("script", "Lab: write and run a script", "Create a script with echo and redirection, make it executable and run it.", 580)],
 [("What must the first line of a script be?", ["A shebang like #!/bin/bash", "A comment with the name", "An empty line", "The exit code"], 0, "It selects the interpreter."), ("Which is a correct assignment?", ["name=Ada", "name = Ada", "$name=Ada", "set name Ada"], 0, "No spaces."), ("What is $#?", ["The number of arguments", "The first argument", "The script name", "The exit code"], 0, "A count.")],
 [("Make a script runnable?", "chmod +x script.sh."), ("Capture output into a variable?", "var=$(command)."), ("Last exit code?", "$?."), ("Why quote variables?", "So values with spaces stay one word.")],
 [FILL("A script", "The first line of a script is the {{shebang}}. Arguments are read as $1 and $2, and {{$#}} is how many there are. Use chmod {{+x}} to make the script executable.")]))

B.append(CH(
 "Shell scripting II: loops, functions and robustness",
 ("Loops", ["for | repeats over | A list", "while | repeats while | A test is true", "Function | groups | Commands", "case | chooses by | Pattern", "set -e | stops on | Errors", "trap | runs on | Signals"]),
 ["for repeats a block for each item in a list, while repeats as long as a test succeeds. Functions give a name to a group of commands.",
  "Scripts should fail loudly. set -e stops the script at the first failing command, and checking exit codes lets you react to problems.",
  "Small, tested scripts are the glue of system administration: backups, deployments, reports and clean-up jobs."],
 [("Loop", "A construct that repeats commands."), ("Function", "A named group of commands you can call like a command."), ("Glob", "A wildcard pattern such as *.log, expanded by the shell."), ("Idempotent", "Safe to run twice: the second run changes nothing.")],
 ["for x in list; do ...; done.", "while test; do ...; done.", "set -e stops at the first error.", "Write idempotent scripts: mkdir -p, not mkdir."],
 [C("# for loop over files\nfor f in *.txt; do\n  echo \"checking $f\"\n  wc -l \"$f\"\ndone\n\n# counting loop\ni=1\nwhile [ $i -le 3 ]; do\n  echo \"round $i\"\n  i=$((i + 1))\ndone\n\n# a function\nbackup() {\n  cp \"$1\" \"$1.bak\"\n  echo \"saved $1\"\n}\nbackup notes.txt"),
  T("The for loop walks a list: words, file names from a wildcard, or numbers from seq. The while loop repeats while its test succeeds. Inside a loop, break leaves the loop and continue skips to the next round. Arithmetic uses double parentheses: $((i + 1))."),
  T("A function takes its own arguments as $1, $2, and returns an exit code with return. case matches a value against patterns and is tidier than a chain of ifs when you check an option or an extension."),
  T("Robust scripts check their work. Put set -e near the top so a failure stops the script instead of letting it plough on. Test that a file exists before reading it. Quote everything. Make scripts idempotent: use mkdir -p, ln -sf and cp -u so running them again is harmless. Print what you are doing so a log shows where it failed."),
  SH("loop", "Lab: loops and functions", "Write a loop that creates several files and a function that reports on them.", 580)],
 [("How do you do arithmetic in bash?", ["$((i + 1))", "i+1", "$i+1", "calc i 1"], 0, "Double parentheses."), ("What does set -e do?", ["Stops at the first failing command", "Prints every command", "Exports variables", "Ends the script"], 0, "Fail fast."), ("What does idempotent mean?", ["Running twice is the same as once", "Fast", "Secret", "Needs root"], 0, "Safe to repeat.")],
 [("Loop over files?", "for f in *.txt; do ...; done."), ("Leave a loop?", "break."), ("Return from a function with failure?", "return 1."), ("Print numbers 1 to 5?", "seq 1 5.")],
 [ORDER("A counting loop", "Put the lines of a loop that prints 1 to 3 in order.", ["i=1", "while [ $i -le 3 ]; do", "echo $i", "i=$((i + 1))", "done"])]))

B.append(CH(
 "Networking basics",
 ("Network", ["IP address | identifies | A host", "Port | identifies | A service", "DNS | maps | Names to addresses", "Subnet | groups | Addresses", "ping | tests | Reachability", "curl | fetches | URLs"]),
 ["Every machine on a network has an IP address. A port number picks the program on that machine, so a web server listens on 80 or 443 and SSH on 22.",
  "DNS turns names such as example.com into addresses. A subnet like 192.168.1.0/24 describes a block of addresses that share a prefix.",
  "Learn four tools: ip addr to see your address, ping to test reachability, curl to talk to web services, and ss to see what is listening."],
 [("IP address", "A number that identifies a network interface, like 192.168.1.23."), ("Port", "A number from 0 to 65535 that picks a service on a host."), ("DNS", "The system that maps names to addresses."), ("CIDR", "Notation like /24 saying how many leading bits form the network part.")],
 ["22 is SSH, 80 HTTP, 443 HTTPS, 53 DNS.", "/24 means the first 24 bits are the network.", "ping tests reachability; curl tests a service.", "ss -tln shows listening TCP ports."],
 [T("An IPv4 address is four numbers from 0 to 255, such as 192.168.1.23. Those are 32 bits. A slash number says how many leading bits name the network. A /24 network has 256 addresses that share the first three numbers. Private ranges such as 192.168.0.0/16, 10.0.0.0/8 and 172.16.0.0/12 are not routed on the internet."),
  C("ip addr              # my addresses\nping -c 2 localhost  # is it reachable?\ncurl http://localhost    # fetch a page\nss -tln              # which TCP ports are listening\ncurl -I https://example.com   # headers only"),
  T("A connection needs an address and a port. The same machine can run SSH on 22 and a web server on 80 at once. When a service is down, curl says connection refused. When a name does not resolve, it says could not resolve host. Those two messages point to different problems: the service or the DNS."),
  T("To work on remote machines you use SSH, a secure shell. ssh user@host logs in, and key pairs are safer than passwords. scp and rsync copy files over it. This sandbox is offline, so ssh is not available here, but the commands are the same on a real server."),
  M(r"\text{addresses in a /}n\text{ block}=2^{32-n}")],
 [("Which port does HTTPS use?", ["443", "80", "22", "25"], 0, "Secure web."), ("How many addresses are in a /24?", ["256", "24", "255", "1024"], 0, "2 to the 8."), ("What does connection refused mean?", ["Nothing is listening on that port", "DNS failed", "Wrong password", "Disk full"], 0, "A reachability success with no service.")],
 [("Show my IP?", "ip addr."), ("Test a web service?", "curl url."), ("Port for SSH?", "22."), ("What is /24?", "A network whose first 24 bits are fixed.")],
 [PL("In the subnet?", "Write in_subnet(ip, cidr) that returns True if the IPv4 address ip is inside the block cidr, such as '192.168.1.0/24'.", "in_subnet(ip, cidr)",
"""def to_bits(ip):
    out = ''
    for p in ip.split('.'):
        b = bin(int(p))[2:]
        out += '0' * (8 - len(b)) + b
    return out


def in_subnet(ip, cidr):
    net, n = cidr.split('/')
    n = int(n)
    return to_bits(ip)[:n] == to_bits(net)[:n]
""", [["192.168.1.77", "192.168.1.0/24"], ["192.168.2.1", "192.168.1.0/24"], ["10.1.2.3", "10.0.0.0/8"], ["172.16.5.5", "172.16.0.0/12"], ["8.8.8.8", "0.0.0.0/0"]], "Convert both to 32-character bit strings and compare the first n bits.")]))

B.append(CH(
 "Disks, logs and scheduled jobs",
 ("Disks", ["Mount | attaches | A filesystem", "df | shows | Free space", "du | shows | Usage", "/var/log | holds | Logs", "cron | runs | Jobs on a schedule", "logrotate | trims | Old logs"]),
 ["Disks are split into partitions, each with a filesystem, and each mounted at a directory. df shows free space for every mount and du shows how much a directory uses.",
  "Logs under /var/log and in the journal are where machines explain themselves. The first question when something breaks is: what does the log say?",
  "cron runs commands on a schedule written as five time fields."],
 [("Mount", "Attach a filesystem to a directory so its files appear in the tree."), ("Partition", "A section of a disk that holds a filesystem."), ("Log", "A file or stream of timestamped messages about what a program did."), ("cron", "The scheduler that runs commands at set times.")],
 ["df -h shows free space; du -sh shows a directory's size.", "Full disks are a very common failure.", "crontab fields: minute hour day month weekday.", "*/5 means every five."],
 [T("df -h lists every mounted filesystem with its size, used space and free space in human units. du -sh dir tells you how big one directory is, and du -sh * | sort -h shows which items are largest. A full disk breaks databases and logging, so checking df is a reflex."),
  C("df -h                          # free space per mount\ndu -sh /var/log                # size of one directory\nls -lh /var/log                # sizes in human units\ntail -n 20 /var/log/syslog     # the last 20 messages\njournalctl -n 20               # same, from systemd\ngrep -i error /var/log/syslog | tail -5"),
  T("A crontab line has five time fields and then a command: minute, hour, day of month, month and day of week. A star means every value, a comma lists values, a dash gives a range and a slash gives a step. So */15 * * * * runs every 15 minutes and 30 2 * * 1 runs at 02:30 every Monday. Edit your table with crontab -e and show it with crontab -l."),
  C("# m  h  dom mon dow  command\n*/15 *  *   *   *    /home/user/check.sh\n30   2  *   *   1    /home/user/backup.sh\n0    9  1   *   *    echo monthly report"),
  T("Logs grow without limit, so logrotate renames and compresses old ones on a schedule. The /etc/fstab file lists the filesystems to mount at boot; a typo there can stop a machine from booting, so take care and keep a copy.")],
 [("Which command shows free disk space?", ["df -h", "du -f", "free", "ls -s"], 0, "Disk free."), ("When does '*/15 * * * *' run?", ["Every 15 minutes", "At minute 15 only", "Every 15 hours", "Once"], 0, "A step."), ("Where are most logs?", ["/var/log", "/etc", "/bin", "/dev"], 0, "Variable data.")],
 [("Size of a directory?", "du -sh dir."), ("Free space?", "df -h."), ("Edit cron jobs?", "crontab -e."), ("Rotate logs?", "logrotate.")],
 [PL("Cron field match", "Write cron_match(field, value) for the minute field of a crontab. The field can be '*', a number, a list like '0,30', a range like '10-20', or a step like '*/15' or '10-50/10'. Return True if value (0 to 59) matches.", "cron_match(field, value)",
"""def cron_match(field, value):
    for part in field.split(','):
        step = 1
        if '/' in part:
            a, s = part.split('/')
            part = a
            step = int(s)
        if part == '*':
            lo = 0
            hi = 59
        elif '-' in part:
            a, b = part.split('-')
            lo = int(a)
            hi = int(b)
        else:
            lo = int(part)
            hi = lo
            if step != 1:
                hi = 59
        if lo <= value <= hi and (value - lo) % step == 0:
            return True
    return False
""", [["*/15", 30], ["*/15", 31], ["1-5", 3], ["0,30", 30], ["0,30", 15], ["10-50/10", 30], ["10-50/10", 35], ["*", 7]], "Handle each comma part: split off a step, find the low and high end, then check the range and the step.")]))

B.append(CH(
 "Security basics",
 ("Security", ["Least privilege | limits | Damage", "SSH keys | replace | Passwords", "Firewall | filters | Traffic", "Updates | fix | Vulnerabilities", "Logs | reveal | Attacks", "Backups | enable | Recovery"]),
 ["Security is a habit of small controls: give every user and program only the access it needs, keep software updated, use keys instead of passwords, and close ports you do not use.",
  "On a server, the usual first steps are to disable root login over SSH, disable password logins, turn on a firewall and set up automatic security updates.",
  "Assume something will fail anyway. Logs help you notice and backups help you recover."],
 [("Least privilege", "Giving each user and program only the access needed."), ("Firewall", "A filter that allows or blocks network traffic by rule."), ("SSH key", "A pair of files: a private key you keep and a public key you put on the server."), ("Hardening", "Reducing the ways a system can be attacked.")],
 ["Disable root and password SSH logins.", "Open only the ports you need.", "Apply security updates promptly.", "Test your backups by restoring one."],
 [T("Start from least privilege. Files should be readable only by those who need them, services should run as their own unprivileged users and administrators should use sudo so that actions are logged. Never make a file world-writable to cure a permissions error. Find out which user and group actually need access and grant just that."),
  C("# /etc/ssh/sshd_config: the lines that matter\nPermitRootLogin no\nPasswordAuthentication no\nPubkeyAuthentication yes\n\nsudo ufw default deny incoming\nsudo ufw allow 22/tcp\nsudo ufw enable\n\nsudo apt update && sudo apt upgrade"),
  T("Passwords can be guessed by bots, and servers see thousands of attempts a day. SSH keys cannot be guessed: you hold the private key and the server holds the public one. Turn off password logins once your key works. A firewall then makes sure that only the ports you chose, such as 22, 80 and 443, answer at all."),
  T("Watch for trouble in the logs. Many failed logins from one address, a user you did not create, or a program running from /tmp are all warnings. And keep backups somewhere else, because a backup on the same disk fails along with it. A backup is only real after you have restored from it once."),
  SH("sec", "Lab: tidy a risky home directory", "Find and fix files that anyone can write, and remove an unwanted account's access.", 580)],
 [("What is least privilege?", ["Only the access needed", "Root for everyone", "No passwords", "Open ports"], 0, "Limit damage."), ("Which is safest for SSH?", ["Keys with passwords off", "Weak passwords", "Root login on", "Shared accounts"], 0, "Keys cannot be guessed."), ("Why test restores?", ["A backup you cannot restore is worthless", "It is quick", "It is required by law", "It frees space"], 0, "Proof.")],
 [("Safer than passwords?", "SSH keys."), ("Stop root SSH login?", "PermitRootLogin no."), ("Fix, don't chmod 777?", "Find who needs access and grant just that."), ("Keep backups where?", "On a different machine or disk.")],
 [PL("Audit sshd config", "Write ssh_problems(text) that reads sshd_config lines and returns a sorted list of problems: 'root login' if PermitRootLogin is yes, and 'passwords' if PasswordAuthentication is yes. A missing setting is not a problem. Lines starting with # are comments.", "ssh_problems(text)",
"""def ssh_problems(text):
    out = []
    for line in text.split('\\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = line.split()
        if len(p) < 2:
            continue
        if p[0] == 'PermitRootLogin' and p[1] == 'yes':
            out.append('root login')
        if p[0] == 'PasswordAuthentication' and p[1] == 'yes':
            out.append('passwords')
    return sorted(out)
""", [["PermitRootLogin yes\nPasswordAuthentication yes\n"], ["# PermitRootLogin yes\nPermitRootLogin no\nPasswordAuthentication no"], [""], ["PasswordAuthentication yes"]], "Skip comments, split on whitespace and compare the setting name and its value.")]))

B.append(CH(
 "Capstone: look after a small server",
 ("Capstone", ["Inspect | the | System", "Install | the | Service", "Secure | the | Files", "Automate | with | A script", "Verify | with | Logs", "Document | the | Result"]),
 ["Put everything together. You are handed a small server with a few problems. Look around, install and start the web service, fix risky permissions, add a teammate and check your work.",
  "Work like a system administrator: inspect first, change one thing at a time and verify each change before moving on.",
  "When the checklist is complete you will have used navigation, files, permissions, users, packages, services and scripting on one machine."],
 [("Runbook", "A written list of steps for a routine or emergency task."), ("Verify", "Check that a change did what you intended."), ("Baseline", "Known good state to compare against."), ("Audit", "A review of what exists and who may do what.")],
 ["Look before you change.", "Change one thing and verify it.", "Keep scripts and notes of what you did.", "Prefer reversible changes."],
 [T("A good administrator works in a loop: observe, change, verify. Start by finding out what you have: who you are, what is running, how much space is free and what the logs say. Then fix the most urgent problem first, and check that it worked."),
  T("In the lab below you will find a web root with files that are too open, a missing web server, a runaway process and a teammate who needs access to a shared folder. The checklist tells you what the finished system should look like but not how to get there. Use the earlier chapters and the Hint button if you get stuck."),
  SH("cap", "Capstone lab: fix the server", "The server has several problems. Complete the checklist using the commands you have learned.", 640),
  T("Congratulations on getting this far. The skills here carry straight over to real servers, containers and cloud machines, which are almost all Linux. The DevOps course builds on them with version control, pipelines, containers and monitoring.")],
 [("What is the first step of a safe change?", ["Observe the current state", "Reboot", "Delete logs", "chmod 777"], 0, "Look before you leap."), ("What is a runbook?", ["Written steps for a task", "A type of script language", "A log file", "A package"], 0, "Procedure."), ("Why verify?", ["To confirm the change worked", "To pass time", "To delete files", "It is optional"], 0, "Trust but check.")],
 [("Admin loop?", "Observe, change, verify."), ("Order of fixes?", "Most urgent first."), ("Safe habit?", "One change at a time."), ("Why notes?", "So the work can be repeated and reviewed.")],
 [MATCH("Which chapter?", "Match each task with the command family you would use.", [("Fix a file's access", "chmod and chown"), ("Add a teammate", "useradd and usermod"), ("Install software", "apt"), ("Stop a runaway process", "ps and kill"), ("Start a service at boot", "systemctl enable")])]))
