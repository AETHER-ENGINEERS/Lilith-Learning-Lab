"""Shell lab definitions for the Linux course."""
import random

def F(c, mode=0o644, owner="user", group=None):
    return {"c": c, "mode": mode, "owner": owner, "group": group or owner}

def D(mode=0o755, owner="user", group=None):
    return {"dir": True, "mode": mode, "owner": owner, "group": group or owner}

def weblog():
    r = random.Random(7)
    pages = ["/home", "/home", "/home", "/home", "/about", "/about", "/login", "/login", "/login", "/pricing", "/missing"]
    ips = ["10.0.0.%d" % i for i in range(1, 8)]
    lines = []
    for i in range(40):
        p = r.choice(pages)
        st = "404" if p == "/missing" else ("302" if p == "/login" and r.random() < .4 else "200")
        lines.append("%s GET %s %s" % (r.choice(ips), p, st))
    return "\n".join(lines) + "\n", lines

LOGTXT, LOGLINES = weblog()
from collections import Counter
TOP = Counter(l.split()[2] for l in LOGLINES).most_common(1)[0]

HELPNAV = "Tab completes names and the arrow keys recall history. Click a chip to paste a command."

LABS = {}

LABS["nav"] = dict(
    intro="<b>Find your way around.</b> You are logged in as <code>user</code>.",
    hints=["pwd", "ls", "ls -a", "cd projects", "cat readme.txt", "cd", "ls -l"],
    files={"/home/user/notes.txt": "buy milk\ncall mum\n", "/home/user/.secret": "hidden file\n", "/home/user/docs/a.md": "# A\n", "/home/user/projects/readme.txt": "This is the projects folder.\n"},
    tasks=[
        {"t": "Print your working directory with pwd", "check": "ran('^pwd')"},
        {"t": "List all files, including hidden ones, with ls -a", "check": "ran('^ls +(-[A-Za-z]*a|-a)')"},
        {"t": "Move into the projects directory", "check": "ran('cd +(~/|/home/user/|\\\\./)?projects/?$')"},
        {"t": "Read readme.txt with cat", "check": "ran('^cat .*readme\\\\.txt') && out.indexOf('projects folder')>=0"},
        {"t": "Come back home with a bare cd", "check": "ran('^cd *$') && cwd=='/home/user'"},
    ],
    solution="pwd\nls -a\ncd projects\ncat readme.txt\ncd")

LABS["files"] = dict(
    intro="<b>Organise a project.</b> Create, copy, move and remove files.",
    hints=["mkdir -p project/src", "touch project/src/main.txt", "cp project/src/main.txt project/notes.txt", "mv project/notes.txt project/readme.txt", "rm data.txt", "ls -R project"],
    files={"/home/user/data.txt": "old data\n"},
    tasks=[
        {"t": "Create the directory project/src (mkdir -p)", "check": "fs.isDir('project/src')"},
        {"t": "Create an empty file project/src/main.txt", "check": "fs.exists('project/src/main.txt')"},
        {"t": "Copy main.txt to project/notes.txt with cp", "check": "ran('^cp ') && fs.exists('project/notes.txt')"},
        {"t": "Rename project/notes.txt to project/readme.txt with mv", "check": "ran('^mv ') && fs.exists('project/readme.txt') && !fs.exists('project/notes.txt')"},
        {"t": "Delete data.txt", "check": "!fs.exists('data.txt')"},
    ],
    solution="mkdir -p project/src\ntouch project/src/main.txt\ncp project/src/main.txt project/notes.txt\nmv project/notes.txt project/readme.txt\nrm data.txt")

LABS["redir"] = dict(
    intro="<b>Write, append and search.</b> Use redirection with <code>&gt;</code>, <code>&gt;&gt;</code>, <code>2&gt;</code> and grep.",
    hints=["echo hello > greeting.txt", "echo again >> greeting.txt", "ls /nope 2> err.txt", "grep ERROR app.log > errors.txt", "grep -c ERROR app.log", "cat errors.txt"],
    files={"/home/user/app.log": "INFO start\nERROR disk full\nINFO retry\nERROR disk full\nWARN slow\nINFO done\n"},
    tasks=[
        {"t": "Create greeting.txt containing the word hello (use >)", "check": "fs.read('greeting.txt').indexOf('hello')>=0"},
        {"t": "Add a second line to greeting.txt (use >>)", "check": "fs.read('greeting.txt').trim().split('\\n').length>=2 && ran('>>')"},
        {"t": "Capture an error message in err.txt with 2>", "check": "fs.read('err.txt').indexOf('No such file')>=0"},
        {"t": "Save only the ERROR lines of app.log in errors.txt", "check": "(function(){var t=fs.read('errors.txt').trim();return !!t&&t.split('\\n').every(function(l){return l.indexOf('ERROR')>=0})})()"},
        {"t": "Count the ERROR lines with grep -c", "check": "ran('grep +-c') && /(^|\\n)2\\n/.test(out)"},
    ],
    solution="echo hello > greeting.txt\necho again >> greeting.txt\nls /nope 2> err.txt\ngrep ERROR app.log > errors.txt\ngrep -c ERROR app.log")

LABS["pipes"] = dict(
    intro="<b>Analyse a web log.</b> <code>access.log</code> lines look like <code>ip METHOD path status</code>.",
    hints=["wc -l access.log", "grep 404 access.log", "awk '{print $3}' access.log | sort | uniq -c | sort -rn", "awk '{print $3}' access.log | sort | uniq -c | sort -rn | head -3", "cut -d' ' -f1 access.log | sort -u | wc -l"],
    files={"/home/user/access.log": LOGTXT},
    tasks=[
        {"t": "Count the lines in access.log with wc -l", "check": "ran('wc +-l') && out.indexOf('%d')>=0" % len(LOGLINES)},
        {"t": "Show only the 404 responses with grep", "check": "ran('grep.*404')"},
        {"t": "Rank pages by visits using sort and uniq -c", "check": "ran('uniq +-c') && ran('sort')"},
        {"t": "Save the top 3 pages (with counts) to top3.txt", "check": "fs.read('top3.txt').trim().split('\\n').length==3 && fs.read('top3.txt').indexOf('%s')>=0" % TOP[0]},
        {"t": "Count how many different visitor IPs there are", "check": "ran('sort +-u|uniq') && ran('wc')"},
    ],
    solution="wc -l access.log\ngrep 404 access.log\nawk '{print $3}' access.log | sort | uniq -c | sort -rn | head -3 > top3.txt\ncut -d' ' -f1 access.log | sort -u | wc -l")

LABS["perm"] = dict(
    intro="<b>Lock it down.</b> Fix the modes. Use <code>ls -l</code> to look and <code>chmod</code> to change.",
    hints=["ls -l", "chmod 600 secret.txt", "chmod +x script.sh", "chmod 644 public/index.html", "chmod 750 shared", "./script.sh"],
    files={"/home/user/secret.txt": F("my password is hunter2\n", 0o644),
           "/home/user/script.sh": F("#!/bin/bash\necho script ran\n", 0o644),
           "/home/user/public/index.html": F("<h1>hi</h1>\n", 0o600),
           "/home/user/id_key": F("PRIVATE KEY\n", 0o666),
           "/home/user/shared/team.txt": F("team notes\n", 0o644)},
    init=["chmod 777 /home/user/shared"],
    tasks=[
        {"t": "Make secret.txt private: owner read/write only (600)", "check": "fs.mode('secret.txt')=='600'"},
        {"t": "Make script.sh executable by the owner and run it", "check": "parseInt(fs.mode('script.sh')[0])%2==1 && out.indexOf('script ran')>=0"},
        {"t": "Make public/index.html readable by everyone (644)", "check": "fs.mode('public/index.html')=='644'"},
        {"t": "Fix the private key id_key to 600", "check": "fs.mode('id_key')=='600'"},
        {"t": "Make the shared directory 750 (group may enter, others may not)", "check": "fs.mode('shared')=='750'"},
    ],
    solution="chmod 600 secret.txt\nchmod +x script.sh && ./script.sh\nchmod 644 public/index.html\nchmod 600 id_key\nchmod 750 shared")

LABS["users"] = dict(
    intro="<b>Add a teammate.</b> You are <code>user</code>, a member of the sudo group.",
    hints=["id", "sudo useradd -m carol", "sudo groupadd team", "sudo usermod -aG team carol", "sudo mkdir /srv/team", "sudo chgrp team /srv/team", "sudo chmod 770 /srv/team", "ls -ld /srv/team", "tail -3 /etc/passwd"],
    files={},
    tasks=[
        {"t": "Run id to see your own groups", "check": "ran('^id')"},
        {"t": "Create the user carol with a home directory", "check": "!!S.users.carol"},
        {"t": "Create the group team and add carol to it", "check": "!!S.users.carol && S.users.carol.groups.indexOf('team')>=0"},
        {"t": "Create /srv/team owned by group team", "check": "fs.isDir('/srv/team') && fs.group('/srv/team')=='team'"},
        {"t": "Give the group full access and others none (mode 770)", "check": "fs.mode('/srv/team')=='770'"},
    ],
    solution="id\nsudo useradd -m carol\nsudo groupadd team\nsudo usermod -aG team carol\nsudo mkdir /srv/team\nsudo chgrp team /srv/team\nsudo chmod 770 /srv/team")

LABS["proc"] = dict(
    intro="<b>Stop a runaway job.</b> Something is eating the CPU. Find it with <code>ps aux</code> and stop it, but leave the others alone.",
    hints=["ps aux", "ps aux | grep miner", "kill 2210", "sleep 100 &", "jobs", "ps"],
    files={},
    procs=[{"pid": 2210, "user": "user", "cmd": "./cryptominer --fast", "state": "R", "cpu": 97.3, "mem": 12.1},
           {"pid": 2211, "user": "user", "cmd": "sleep 3000", "state": "S", "cpu": 0.0, "mem": 0.1},
           {"pid": 2300, "user": "root", "cmd": "/usr/sbin/backup-agent", "state": "S", "cpu": 0.4, "mem": 1.2}],
    tasks=[
        {"t": "List every process with ps aux", "check": "ran('^ps +aux')"},
        {"t": "Try to kill the root-owned backup-agent (pid 2300) and read the error", "check": "ran('kill +(-[0-9A-Z]+ +)?2300') && out.indexOf('not permitted')>=0"},
        {"t": "Stop the cryptominer (pid 2210)", "check": "!S.procs.some(function(p){return p.pid==2210})"},
        {"t": "Leave the harmless sleep job (pid 2211) running", "check": "S.procs.some(function(p){return p.pid==2211}) && !S.procs.some(function(p){return p.pid==2210})"},
        {"t": "Start your own background job with & and list jobs", "check": "ran(' &$') && ran('^jobs')"},
    ],
    solution="ps aux\nkill 2300\nkill 2210\nsleep 100 &\njobs")

LABS["svc"] = dict(
    intro="<b>Install and run a web server.</b> Use <code>sudo</code> with apt and systemctl, then fetch the page with curl.",
    hints=["sudo apt update", "sudo apt install nginx", "systemctl status nginx", "sudo systemctl start nginx", "sudo systemctl enable nginx", "curl http://localhost"],
    files={"/var/www/html/index.html": F("<html><h1>Welcome to nginx!</h1></html>\n", 0o644, "root")},
    tasks=[
        {"t": "Update the package list", "check": "ran('apt update')"},
        {"t": "Install nginx", "check": "!!S.pkgs.installed.nginx"},
        {"t": "Start the service", "check": "S.services.nginx.active"},
        {"t": "Enable it at boot", "check": "S.services.nginx.enabled"},
        {"t": "Fetch the home page with curl http://localhost", "check": "out.indexOf('Welcome to nginx')>=0"},
    ],
    solution="sudo apt update\nsudo apt install nginx\nsudo systemctl start nginx\nsudo systemctl enable nginx\ncurl http://localhost")

LABS["script"] = dict(
    intro="<b>Write and run a script.</b> There is no editor here, so build the file with <code>printf</code> or <code>echo</code> and redirection.",
    hints=["printf '#!/bin/bash\\necho \"Hello, $1!\"\\n' > hello.sh", "cat hello.sh", "chmod +x hello.sh", "./hello.sh Lilith"],
    files={},
    tasks=[
        {"t": "Create hello.sh whose first line is #!/bin/bash", "check": "fs.read('hello.sh').indexOf('#!/bin/bash')==0"},
        {"t": "Make it print Hello, followed by its first argument", "check": "fs.read('hello.sh').indexOf('$1')>=0"},
        {"t": "Make it executable", "check": "parseInt(fs.mode('hello.sh')[0])%2==1"},
        {"t": "Run it as ./hello.sh Lilith", "check": "ran('^\\\\./hello\\\\.sh +Lilith') && out.indexOf('Hello, Lilith!')>=0"},
    ],
    solution="printf '#!/bin/bash\\necho \"Hello, $1!\"\\n' > hello.sh\nchmod +x hello.sh\n./hello.sh Lilith")

LABS["loop"] = dict(
    intro="<b>Loops and functions.</b> Type multi-line constructs on one line, separated with <code>;</code>.",
    hints=["for i in 1 2 3; do touch file$i.txt; done", "ls", "i=1; while [ $i -le 5 ]; do echo $i; i=$((i+1)); done", "greet() { echo hi $1; }; greet Ada"],
    files={},
    tasks=[
        {"t": "Create file1.txt, file2.txt and file3.txt with a for loop", "check": "ran('^for ') && fs.exists('file1.txt') && fs.exists('file2.txt') && fs.exists('file3.txt')"},
        {"t": "Print the numbers 1 to 5 with a while loop", "check": "ran('^.*while') && out.indexOf('1\\n2\\n3\\n4\\n5\\n')>=0"},
        {"t": "Define a function and call it", "check": "ran('\\\\(\\\\) *\\\\{') && Object.keys(S.funcs).length>0"},
        {"t": "Use $? to show the exit code of a failing command (false; echo $?)", "check": "ran('echo +\\\\$\\\\?') && out.indexOf('\\n1\\n')>=0"},
    ],
    solution="for i in 1 2 3; do touch file$i.txt; done\ni=1; while [ $i -le 5 ]; do echo $i; i=$((i+1)); done\ngreet() { echo hi $1; }; greet Ada\nfalse; echo $?")

LABS["sec"] = dict(
    intro="<b>Tidy a risky home directory.</b> Anyone-can-write files are a hazard. Find them and fix them.",
    hints=["ls -lR", "find . -type f", "chmod o-w app.conf", "chmod 755 upload", "chmod 600 .ssh/id_rsa", "ls -l .ssh"],
    files={"/home/user/app.conf": F("password=changeme\n", 0o666), "/home/user/upload/readme.txt": F("uploads\n", 0o666),
           "/home/user/backup.sh": F("#!/bin/bash\necho backup\n", 0o777), "/home/user/.ssh/id_rsa": F("PRIVATE KEY\n", 0o644), "/home/user/.ssh/id_rsa.pub": F("PUBLIC KEY\n", 0o644)},
    init=["chmod 777 /home/user/upload"],
    tasks=[
        {"t": "Look at everything with ls -lR or find", "check": "ran('ls .*R|find')"},
        {"t": "No file or directory under your home may be writable by others", "check": "(function(){var bad=0;function w(p){fs.ls(p).forEach(function(n){var q=p+'/'+n;var m=fs.mode(q);if(parseInt(m[m.length-1])&2)bad++;if(fs.isDir(q))w(q)})}w('/home/user');return bad==0})()"},
        {"t": "The private key .ssh/id_rsa must be 600", "check": "fs.mode('.ssh/id_rsa')=='600'"},
        {"t": "backup.sh must stay executable by its owner", "check": "parseInt(fs.mode('backup.sh')[0])%2==1"},
    ],
    solution="ls -lR\nchmod -R o-w /home/user\nchmod 600 .ssh/id_rsa")

LABS["cap"] = dict(
    intro="<b>Capstone: fix the server.</b> You are <code>user</code> with sudo. Remember: <code>sudo echo x &gt; f</code> redirects as you, so use <code>| sudo tee f</code>.",
    hints=["ps aux", "df -h", "ls -l /var/www/html", "sudo apt install nginx", "sudo systemctl start nginx", "sudo chmod 644 /var/www/html/index.html", "kill 3001", "sudo useradd -m dana", "sudo usermod -aG dev dana", "echo 'echo deploy' | sudo tee /opt/deploy.sh", "sudo chmod 755 /opt/deploy.sh", "df -h > report.txt"],
    files={"/var/www/html/index.html": F("<html><h1>Welcome to nginx!</h1></html>\n", 0o666, "root")},
    procs=[{"pid": 3001, "user": "user", "cmd": "yes > /dev/null", "state": "R", "cpu": 99.0, "mem": 0.1}],
    tasks=[
        {"t": "Install nginx and start it", "check": "!!S.pkgs.installed.nginx && S.services.nginx.active"},
        {"t": "Make /var/www/html/index.html mode 644 (it is world-writable)", "check": "fs.mode('/var/www/html/index.html')=='644'"},
        {"t": "Stop the runaway process that is using 99% CPU", "check": "!S.procs.some(function(p){return p.pid==3001})"},
        {"t": "Create the user dana and add her to the group dev", "check": "!!S.users.dana && S.users.dana.groups.indexOf('dev')>=0"},
        {"t": "Create /opt/deploy.sh that is executable", "check": "fs.exists('/opt/deploy.sh') && parseInt(fs.mode('/opt/deploy.sh')[0])%2==1"},
        {"t": "Save the disk report to report.txt with df -h", "check": "fs.read('report.txt').indexOf('Filesystem')>=0"},
    ],
    solution="sudo apt install nginx && sudo systemctl start nginx\nsudo chmod 644 /var/www/html/index.html\nkill 3001\nsudo useradd -m dana && sudo usermod -aG dev dana\necho 'echo deploy' | sudo tee /opt/deploy.sh && sudo chmod 755 /opt/deploy.sh\ndf -h > report.txt")
