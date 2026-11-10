"""Linux course, chapters 1-7. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *


def SH(key, title, intro, h=560):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__SH_%s__" % key}


A = []

A.append(CH(
 "What Linux is",
 ("Linux", ["Kernel | manages | Hardware", "Distribution | bundles | Kernel and tools", "Shell | runs | Commands", "Filesystem | is one | Tree from /", "Process | is | A running program", "User | owns | Files and processes"]),
 ["Linux is a kernel, the core program that talks to the hardware and shares it between programs. Around it sits a set of tools, and the bundle is called a distribution, such as Debian, Ubuntu or Fedora.",
  "Everything is organised as one tree of files starting at a single root called slash. Devices, settings and even running processes appear as files in that tree.",
  "You will work in a terminal and a shell, because that is how servers, containers and cloud machines are run."],
 [("Kernel", "The core of the operating system. It schedules programs, manages memory and drives hardware."), ("Distribution", "A kernel plus tools, an installer and a package manager, ready to use."), ("Shell", "A program that reads your commands and runs them. Bash is the most common."), ("Root", "Two things: the top directory /, and the all-powerful administrator account.")],
 ["Linux is the kernel; a distribution is the complete system.", "One tree of files starts at /.", "Almost everything is a file or behaves like one.", "Servers, phones, routers and clouds mostly run Linux."],
 [T("Linux started in 1991 as a kernel written by Linus Torvalds and grew through thousands of contributors. The kernel decides which program runs when, hands out memory, and talks to disks, networks and screens. It does not include a text editor or a shell. Those come from other projects, and a distribution packages them together."),
  T("Distributions differ in tools and defaults, but they share the same kernel ideas and nearly the same commands. Debian and Ubuntu use the apt package manager. Fedora and Red Hat use dnf. Alpine is tiny and popular in containers. Learn the common core and you can work on all of them."),
  T("Linux has one filesystem tree. There are no drive letters. A second disk is attached at a directory, called mounting. Programs live under /usr and /bin, settings under /etc, your files under /home, logs under /var/log, temporary files under /tmp. Special files in /dev stand for devices, and /proc shows live information about running processes."),
  C("/            the root of everything\n├── bin       essential commands\n├── etc       configuration files\n├── home      one directory per user\n│   └── user\n├── tmp       temporary files, cleared on reboot\n├── usr       installed programs and libraries\n└── var       data that changes: logs, caches, mail"),
  T("The idea that many things are files is powerful. You can read a device, search a log or redirect output with the same few tools. In the lab at the end of the next chapter you will move around a small Linux-like machine that runs right inside this app.")],
 [("What is Linux, strictly?", ["A kernel", "A complete desktop", "A text editor", "A shell"], 0, "Distributions add the rest."), ("Where do settings usually live?", ["/etc", "/tmp", "/dev", "/proc"], 0, "Think etcetera: configuration."), ("How are extra disks attached?", ["Mounted at a directory", "Given a drive letter", "Copied into /bin", "Never"], 0, "One tree only.")],
 [("What is a distribution?", "A kernel bundled with tools and a package manager."), ("What is /?", "The root of the single filesystem tree."), ("Where are logs?", "Under /var/log."), ("What is /home?", "Where each user's personal files live.")],
 [MATCH("Directories", "Match each directory with its purpose.", [("/etc", "Configuration files"), ("/home", "User files"), ("/var/log", "Logs"), ("/tmp", "Temporary files"), ("/dev", "Device files")]),
  FILL("The tree", "Linux has one filesystem tree that starts at {{/}}. Programs usually live under /usr, configuration lives under {{/etc}} and the kernel is the core of the {{distribution}} you install.")]))

A.append(CH(
 "The shell and your first commands",
 ("Shell", ["Prompt | waits for | A command", "Command | takes | Options and arguments", "pwd | prints | Current directory", "ls | lists | Directory contents", "cd | changes | Directory", "man | explains | A command"]),
 ["The shell shows a prompt and waits. You type a command, possibly with options and arguments, and press Enter. The shell finds the program, runs it and prints the result.",
  "Start with five commands: pwd says where you are, ls lists what is here, cd moves, cat shows a file, and man or --help explains anything.",
  "Tab completes names and the up arrow recalls earlier lines, which saves a lot of typing."],
 [("Command", "A program or built-in the shell runs, such as ls."), ("Option", "A flag that changes behaviour, such as -l, usually starting with a dash."), ("Argument", "What the command works on, such as a file name."), ("Working directory", "The directory the shell is currently in."), ("Path", "The location of a file, absolute from / or relative to here.")],
 ["A command line is command, options, arguments.", "Absolute paths start with /; relative paths do not.", ". is here, .. is the parent, ~ is your home.", "Tab completes and history recalls."],
 [T("A command line has a simple shape: the command name, then options, then arguments. In ls -l /etc the command is ls, the option is -l, which means long listing, and the argument is the directory /etc. Options can usually be combined, so ls -la means long listing including hidden files."),
  T("A path names a file. An absolute path starts at the root and works from anywhere, like /home/user/notes.txt. A relative path starts at the working directory, like docs/a.md. Two dots mean the parent directory, one dot means here, and a tilde means your home directory. Files whose names start with a dot are hidden from a plain ls."),
  C("pwd              # print working directory\nls               # list names\nls -la           # long, including hidden files\ncd docs          # move into docs\ncd ..            # up one level\ncd               # home\ncat notes.txt    # print a file\nman ls           # the manual page"),
  T("The prompt usually shows your user, the machine and the directory, and ends with a dollar sign for a normal user or a hash for root. Press Tab to complete a name, press it twice to see the choices, and use the up arrow to recall a previous command."),
  SH("nav", "Lab: find your way around", "A small Linux-like machine runs here. Use pwd, ls, cd and cat to complete the checklist.")],
 [("What does cd .. do?", ["Moves to the parent directory", "Moves home", "Lists files", "Prints the path"], 0, "Two dots are the parent."), ("Which path is absolute?", ["/home/user/a.txt", "docs/a.txt", "../a.txt", "~a"], 0, "It starts at /."), ("What does ls -a add?", ["Hidden files", "File sizes", "Colour", "Sorting"], 0, "Names starting with a dot.")],
 [("pwd?", "Prints the working directory."), ("What is ~?", "Your home directory."), ("How to read a manual?", "man followed by the command name."), ("What does Tab do?", "Completes a file or command name.")],
 [MATCH("Commands", "Match each command with what it does.", [("pwd", "Show where you are"), ("ls", "List a directory"), ("cd", "Change directory"), ("cat", "Print a file"), ("man", "Open the manual")])]))

A.append(CH(
 "Files and directories",
 ("Files", ["mkdir | creates | Directories", "touch | creates | Empty files", "cp | copies | Files", "mv | moves or renames | Files", "rm | deletes | Files", "find | searches | The tree"]),
 ["You create, copy, move and delete with a small set of commands. mkdir makes directories, touch makes an empty file, cp copies, mv moves or renames, and rm removes.",
  "Deleting is permanent: there is no recycle bin on the command line. Use rm -r for directories and think before you press Enter.",
  "Wildcards let one pattern name many files, and find searches by name, type and more."],
 [("Wildcard", "A pattern character the shell expands: * matches any text, ? matches one character."), ("Recursive", "Applied to a directory and everything inside it, usually with -r."), ("Inode", "The record that stores a file's size, owner, permissions and where its data is."), ("Symbolic link", "A small file that points to another path.")],
 ["mkdir -p makes parent directories too.", "mv is also rename.", "rm is permanent; rm -r removes directories.", "* matches any characters, ? matches one."],
 [T("To make a directory, use mkdir. With -p it creates the whole chain, so mkdir -p project/src/app works even if project does not exist yet. To make an empty file, use touch, which also updates the modified time of a file that already exists."),
  T("cp copies a file, and cp -r copies a directory with everything in it. mv moves a file to a new place, and because moving within a directory just changes the name, mv is also the rename command. rm deletes. There is no undo, so rm -r on the wrong directory is a classic disaster. Never run rm -rf with a variable you have not checked."),
  C("mkdir -p project/src\ntouch project/src/main.txt\ncp project/src/main.txt project/backup.txt\nmv project/backup.txt project/old.txt\nrm project/old.txt\nls project/*.txt            # wildcard\nfind project -name '*.txt'  # search by name"),
  T("Wildcards are expanded by the shell before the command runs. If a directory holds a.txt, b.txt and notes.md, the pattern *.txt becomes a.txt b.txt. Quote a pattern when you want the command, not the shell, to see it, as with find -name '*.txt'."),
  SH("files", "Lab: organise a project", "Create, copy, move and remove files until the checklist is complete.")],
 [("Which command renames a file?", ["mv", "cp", "ren", "touch"], 0, "Move within a directory."), ("What does mkdir -p do?", ["Creates parent directories too", "Prints the path", "Sets permissions", "Makes a hidden folder"], 0, "Handy for deep paths."), ("What does rm -r do?", ["Removes a directory and its contents", "Renames", "Reads", "Restores"], 0, "Recursive.")],
 [("How to copy a directory?", "cp -r source destination."), ("What does touch do to a missing file?", "Creates it empty."), ("What does * match?", "Any run of characters."), ("Is rm reversible?", "No, there is no recycle bin.")],
 [MATCH("File commands", "Match each command with its job.", [("mkdir", "Make a directory"), ("touch", "Make an empty file"), ("cp", "Copy"), ("mv", "Move or rename"), ("rm", "Delete")]),
  ORDER("Reorganise", "Put the commands in an order that makes a project directory, adds a file, copies it, then deletes the copy.", ["mkdir proj", "touch proj/a.txt", "cp proj/a.txt proj/b.txt", "rm proj/b.txt"])]))

A.append(CH(
 "Viewing, searching and redirecting",
 ("Streams", ["stdin | is | Input stream", "stdout | is | Output stream", "stderr | is | Error stream", ">  | writes | A file", ">> | appends to | A file", "< | reads from | A file"]),
 ["Every program has three streams: standard input, standard output and standard error. By default they connect to the terminal, but you can redirect them.",
  "> sends output to a file and replaces it, >> appends, < feeds a file in, and 2> catches errors. This turns commands into building blocks.",
  "To look at files, use cat for short ones, head and tail for the ends, less to page, and grep to find lines."],
 [("stdin", "Standard input, stream 0: where a program reads from."), ("stdout", "Standard output, stream 1: where normal results go."), ("stderr", "Standard error, stream 2: where error messages go."), ("Redirection", "Pointing a stream at a file instead of the terminal.")],
 ["> replaces, >> appends.", "2> redirects errors; 2>&1 merges them.", "head and tail show the ends of a file.", "grep prints lines that match."],
 [T("A program reads from standard input and writes to standard output. Errors go to a separate stream, standard error, so they do not get mixed into results. Both usually show on your screen, which hides the difference until you redirect."),
  C("echo hello > greeting.txt      # create or replace\necho again >> greeting.txt       # append\ncat greeting.txt\nls /nope 2> errors.txt           # only errors go to the file\nls /nope /etc > out.txt 2>&1     # both streams into one file\nsort < names.txt                  # feed a file as input\nls /nope 2> /dev/null            # throw errors away"),
  T("/dev/null is a special file that discards everything written to it. It is the standard way to silence output you do not need."),
  T("To read files: cat prints a whole file, head -n 3 prints the first three lines, tail -n 3 prints the last three, and tail -f follows a log as it grows. less pages through a large file. grep pattern file prints matching lines; -i ignores case, -n shows line numbers, -v inverts, -c counts and -r searches a directory tree."),
  SH("redir", "Lab: write, append and search", "Use echo, redirection and grep to build and inspect files.")],
 [("What does >> do?", ["Appends to a file", "Replaces a file", "Reads a file", "Deletes a file"], 0, "Two arrows add on the end."), ("Which stream is number 2?", ["stderr", "stdout", "stdin", "stdlog"], 0, "Errors."), ("What does grep -v do?", ["Shows non-matching lines", "Verbose mode", "Counts lines", "Ignores case"], 0, "Invert.")],
 [("Replace a file's contents?", "Use > ."), ("Discard output?", "Redirect to /dev/null."), ("Follow a growing log?", "tail -f file."), ("Count matches?", "grep -c pattern file.")],
 [MATCH("Redirection", "Match each symbol with its meaning.", [(">", "Write output to a file, replacing it"), (">>", "Append output to a file"), ("<", "Read input from a file"), ("2>", "Send errors to a file"), ("|", "Send output to another command")])]))

A.append(CH(
 "Pipes and text tools",
 ("Pipes", ["Pipe | connects | Two commands", "grep | filters | Lines", "sort | orders | Lines", "uniq | collapses | Duplicates", "wc | counts | Lines and words", "awk | selects | Columns"]),
 ["A pipe, written |, sends the output of one command into the input of the next. Small tools that each do one thing combine into powerful one-line programs.",
  "The core toolbox: grep to filter, sort to order, uniq -c to count repeats, wc to count, cut and awk to pick columns, sed to edit streams and tr to translate characters.",
  "A classic pipeline counts something in a log: filter with grep, take a column, sort, count with uniq -c, sort again."],
 [("Pipe", "The | operator: output of the left command becomes input of the right."), ("Filter", "A program that reads a stream and writes a changed stream."), ("Regular expression", "A pattern language for matching text, used by grep, sed and awk."), ("Field", "A column of a line, separated by spaces or another delimiter.")],
 ["cmd1 | cmd2 feeds output to input.", "sort | uniq -c counts repeats; uniq needs sorted input.", "awk '{print $1}' prints the first column.", "sed 's/old/new/' replaces text."],
 [T("The Unix idea is small tools that do one job and work together. A pipe joins them. Because everything is text, any tool can read what another wrote, with no special format."),
  C("# which pages are visited most?\ncat access.log | awk '{print $3}' | sort | uniq -c | sort -rn | head -3\n\n# count lines that mention ERROR\ngrep -c ERROR app.log\n\n# replace text in a stream\necho 'hello world' | sed 's/world/Linux/'\n\n# first and fifth fields of the passwd file\ncut -d: -f1,5 /etc/passwd"),
  T("uniq only collapses neighbouring duplicates, which is why you nearly always sort first. sort -n sorts numerically, -r reverses, and -k picks a column. wc -l counts lines, wc -w words. tr a-z A-Z turns lowercase into uppercase. xargs turns lines of input into arguments of another command."),
  T("awk treats each line as fields named $1, $2 and so on, and $0 is the whole line. awk '{print $2}' prints the second column. awk '$4 == 404' prints lines whose fourth field is 404. sed handles replacements and deletions: sed 's/a/b/g' replaces every a, and sed '/debug/d' deletes lines containing debug."),
  SH("pipes", "Lab: analyse a web log", "A web server log is in your home directory. Build pipelines to answer questions about it.", 580)],
 [("Why sort before uniq?", ["uniq only joins adjacent duplicates", "uniq is slow", "sort adds counts", "uniq needs a file"], 0, "Neighbours only."), ("What does awk '{print $1}' print?", ["The first column", "The first line", "The last word", "Everything"], 0, "Fields are $1, $2..."), ("What does wc -l count?", ["Lines", "Letters", "Links", "Lengths"], 0, "Line count.")],
 [("Join two commands?", "Use a pipe: cmd1 | cmd2."), ("Count repeats?", "sort | uniq -c."), ("Replace text?", "sed 's/old/new/'."), ("Pick a column?", "cut -d, -f2 or awk '{print $2}'.")],
 [PL("Count status codes", "Each line of a web log looks like '10.0.0.1 GET /a 200'. Write count_status(lines) that counts how often each status (last field) appears. Return a list of [status, count] pairs sorted by count descending, then status ascending.", "count_status(lines)",
"""def count_status(lines):
    d = {}
    for line in lines:
        s = line.split()[-1]
        d[s] = d.get(s, 0) + 1
    items = sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))
    return [[k, v] for k, v in items]
""", [[["1.1.1.1 GET /a 200", "1.1.1.2 GET /b 404", "1.1.1.1 GET /c 200"]], [["a GET / 500", "b GET / 200", "c GET / 500", "d GET / 200"]], [[]]], "This is sort | uniq -c written as code: count in a dict, then sort.")]))

A.append(CH(
 "Permissions and ownership",
 ("Permissions", ["Owner | is | A user", "Group | is | A set of users", "r | means | Read", "w | means | Write", "x | means | Execute", "chmod | changes | Mode bits"]),
 ["Every file has an owner, a group and three sets of permission bits: for the owner, for the group and for everyone else. Each set can allow read, write and execute.",
  "ls -l shows them as ten characters like -rwxr-xr--. chmod changes them with numbers, such as 755, or letters, such as u+x.",
  "Permissions on a directory mean something different: read lists names, write adds or removes entries, execute lets you enter."],
 [("Mode", "The permission bits of a file."), ("Octal", "Base 8: one digit per set, r=4, w=2, x=1 added together."), ("umask", "A mask that removes permissions from newly created files."), ("setuid", "A bit that makes a program run with its owner's rights.")],
 ["r=4, w=2, x=1; add them per set.", "755 is rwxr-xr-x, 644 is rw-r--r--.", "Directories need x to be entered.", "umask 022 gives files 644 and directories 755."],
 [T("A line from ls -l reads like this: -rwxr-xr-- 1 alice dev 120 Nov 9 10:00 run.sh. The first character is the type, a dash for a file and d for a directory. Then come three triples for the owner, the group and others. Then the link count, the owner, the group, the size, the date and the name."),
  C("-rwxr-xr--   owner can read, write, execute\n                group can read, execute\n                others can only read\n\nr = 4   w = 2   x = 1\nrwx = 7   r-x = 5   r-- = 4   so this mode is 754"),
  T("chmod accepts a number or a symbolic expression. chmod 644 notes.txt sets rw-r--r--. chmod u+x run.sh adds execute for the owner. chmod go-w file removes write from group and others. chmod -R applies to a whole tree. Only the owner or root can change a file's mode, and only root can change its owner with chown."),
  T("For directories: read lets you list the names, write lets you create or delete entries inside, and execute lets you cd into it and reach the files inside. A directory with mode 700 is private to its owner. The sticky bit on /tmp stops users from deleting each other's files even though everyone can write there."),
  T("New files get 666 for files and 777 for directories, minus the umask. With the usual umask 022, files come out 644 and directories 755. A umask of 077 makes everything private."),
  SH("perm", "Lab: lock it down", "Fix the permissions on the files in your home directory to complete the checklist.")],
 [("What is mode 640?", ["rw-r-----", "rwxr-x---", "rw-rw-r--", "r--r-----"], 0, "6=rw-, 4=r--, 0=---."), ("What does chmod u+x do?", ["Lets the owner execute", "Lets everyone execute", "Removes execute", "Changes the owner"], 0, "u is the user/owner."), ("What does x mean on a directory?", ["You can enter it", "You can run it as a program", "You can delete it", "It is hidden"], 0, "Traverse.")],
 [("r, w, x values?", "4, 2 and 1."), ("What is 755?", "rwxr-xr-x."), ("Who may chown?", "Only root."), ("What does umask 077 do?", "New files are private to the owner.")],
 [PL("Permission string to octal", "Write perm_to_octal(s) that turns a nine-character string like 'rwxr-xr--' into the three-digit octal text '754'.", "perm_to_octal(s)",
"""def perm_to_octal(s):
    out = ''
    for i in range(0, 9, 3):
        n = 0
        if s[i] == 'r':
            n += 4
        if s[i + 1] == 'w':
            n += 2
        if s[i + 2] == 'x':
            n += 1
        out += str(n)
    return out
""", [["rwxr-xr--"], ["rw-r--r--"], ["---------"], ["rwxrwxrwx"], ["rwx------"]], "Take the letters three at a time and add 4, 2 and 1."),
  PL("Octal to permission string", "Write octal_to_perm(o) that turns '640' into 'rw-r-----'.", "octal_to_perm(o)",
"""def octal_to_perm(o):
    out = ''
    for d in o:
        n = int(d)
        out += 'r' if n >= 4 else '-'
        out += 'w' if n % 4 >= 2 else '-'
        out += 'x' if n % 2 == 1 else '-'
    return out
""", [["640"], ["755"], ["000"], ["777"], ["604"]], "For each digit test the 4, 2 and 1 bits.")]))

A.append(CH(
 "Users, groups and sudo",
 ("Users", ["User | has | A UID", "Group | has | A GID", "/etc/passwd | lists | Users", "/etc/group | lists | Groups", "root | is | UID 0", "sudo | runs as | root"]),
 ["Every process and file belongs to a user and a group. A user is a number, the UID, with a name; root is UID 0 and may do anything.",
  "Day to day you work as a normal user and borrow root's power only when needed, with sudo, which asks for your password and logs what you ran.",
  "Users and groups live in plain text files under /etc, and a handful of commands manage them: useradd, usermod, groupadd, passwd, id and groups."],
 [("UID", "The numeric id of a user. Root is 0; normal users usually start at 1000."), ("GID", "The numeric id of a group."), ("sudo", "Runs one command with another user's rights, normally root's, if you are allowed."), ("sudoers", "The configuration that says who may use sudo.")],
 ["id shows your uid, gid and groups.", "Work as a normal user; use sudo only when needed.", "usermod -aG adds a user to a group; forget -a and you replace the groups.", "/etc/passwd has seven colon-separated fields."],
 [T("Linux decides what you may do by your user id and group ids. The names are only labels; the kernel works with numbers. The id command shows both. A user can belong to many groups, which is how you share a project directory: put the team in one group and give that group write access."),
  C("# /etc/passwd: name : x : uid : gid : comment : home : shell\nalice:x:1001:1001:Alice:/home/alice:/bin/bash\n\nid                       # uid=1000(user) gid=1000(user) groups=...\nsudo useradd -m zed      # make a user and a home directory\nsudo usermod -aG dev zed # add zed to the group dev\nsudo passwd zed          # set a password\nsudo -u alice ls /home/alice   # run one command as alice"),
  T("Root can read every file, kill any process and change any setting, so a typo as root can destroy a machine. That is why servers disable direct root logins and rely on sudo. Members of the sudo group, or of wheel on some distributions, may use it. Each use is written to the log."),
  T("Be careful with usermod. The option -aG appends to the supplementary groups. Without -a the user's groups are replaced by exactly the list you gave, which can lock someone out of the sudo group by accident."),
  SH("users", "Lab: add a teammate", "Create a user, a shared group and a shared directory using sudo.")],
 [("What is the UID of root?", ["0", "1", "1000", "-1"], 0, "Zero."), ("What does usermod -aG dev zed do?", ["Adds zed to dev, keeping other groups", "Replaces zed's groups", "Deletes zed", "Renames dev"], 0, "-a means append."), ("Why use sudo rather than root?", ["Least privilege and an audit trail", "It is faster", "Root cannot log in", "It is required to type commands"], 0, "Borrow power, log use.")],
 [("Show your ids?", "Run id."), ("Where are users listed?", "/etc/passwd."), ("Run one command as root?", "sudo command."), ("Make a user with a home?", "useradd -m name.")],
 [PL("Find human users", "A passwd file has lines 'name:x:uid:gid:comment:home:shell'. Write human_users(text) that returns the names of users with uid 1000 or more, in file order.", "human_users(text)",
"""def human_users(text):
    out = []
    for line in text.split('\\n'):
        if not line:
            continue
        f = line.split(':')
        if int(f[2]) >= 1000:
            out.append(f[0])
    return out
""", [["root:x:0:0:r:/root:/bin/bash\nuser:x:1000:1000:U:/home/user:/bin/bash\nalice:x:1001:1001:A:/home/alice:/bin/bash\n"], ["daemon:x:1:1::/:/sbin/nologin\n"], ["bob:x:1500:1500:B:/home/bob:/bin/zsh"]], "Split each line on colons and compare field 2 (the uid) with 1000.")]))
