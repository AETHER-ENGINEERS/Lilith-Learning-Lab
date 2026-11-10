"""DevOps course, chapters 1-8. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *
from lx1 import SH

A = []

A.append(CH(
 "What DevOps is",
 ("DevOps", ["Dev | builds | Features", "Ops | runs | Services", "DevOps | joins | Both", "Automation | removes | Manual toil", "Feedback | improves | Every step", "DORA metrics | measure | Delivery"]),
 ["DevOps is a way of working in which the people who build software and the people who run it share responsibility and tools. The goal is to deliver changes to users quickly, safely and repeatedly.",
  "It rests on a few habits: keep everything in version control, automate builds, tests and deployment, ship small changes often, and watch what happens in production so you can learn fast.",
  "Four measures from the DORA research show how a team is doing: how often it deploys, how long a change takes to reach users, how often changes fail, and how fast it recovers."],
 [("Pipeline", "An automated path that takes a change from commit to production."), ("Toil", "Repetitive manual work that grows with the service and could be automated."), ("Lead time", "The time from a commit to that change running in production."), ("Change failure rate", "The share of deployments that cause a problem needing a fix or rollback.")],
 ["Share responsibility between building and running.", "Automate everything you do more than twice.", "Small, frequent changes are safer than big rare ones.", "Measure: frequency, lead time, failure rate, recovery time."],
 [T("Before DevOps, developers often wrote code and threw it over a wall to an operations team, who had to run something they had never seen. Releases were big, rare and scary. DevOps tears down the wall. A team owns a service from the first line of code to the pager at night, and uses automation to make releases boring."),
  T("Four ideas carry most of the weight. First, put everything in version control: code, configuration, infrastructure and pipeline definitions. Second, automate the path to production so that a change is built, tested and deployed the same way every time. Third, ship small changes often, because a small change is easy to understand and easy to undo. Fourth, observe the running system and feed what you learn back into the next change."),
  T("The DORA research programme found that four numbers separate high-performing teams from the rest. Deployment frequency is how often you release. Lead time for changes is how long a commit takes to reach production. Change failure rate is the share of releases that cause trouble. Time to restore service is how long it takes to recover. Notably, the best teams are better at all four at once: speed and stability do not trade off."),
  M(r"\text{change failure rate}=\frac{\text{failed deployments}}{\text{all deployments}}"),
  T("DevOps is not a job title or a single tool. Tools such as Git, Docker, Kubernetes and Terraform help, but the heart of it is culture: blameless reviews, shared ownership and a habit of automating pain away. The rest of this course takes the tools one at a time, in the order a change travels.")],
 [("What does lead time measure?", ["Commit to running in production", "Time to write code", "Time to hire", "Meeting length"], 0, "How fast a change reaches users."), ("Which is a DORA metric?", ["Change failure rate", "Lines of code", "Number of meetings", "Server count"], 0, "Along with frequency, lead time and recovery time."), ("Why ship small changes?", ["They are easier to understand and undo", "They need no tests", "They avoid version control", "They are cheaper hardware"], 0, "Small means safe.")],
 [("What is toil?", "Repetitive manual work that automation could remove."), ("Name the four DORA metrics.", "Deployment frequency, lead time, change failure rate, time to restore."), ("What goes in version control?", "Code, configuration, infrastructure and pipelines."), ("Is DevOps a tool?", "No, it is a way of working supported by tools.")],
 [MATCH("DORA metrics", "Match each metric with what it asks.", [("Deployment frequency", "How often do we release?"), ("Lead time", "How long from commit to production?"), ("Change failure rate", "How often does a release cause trouble?"), ("Time to restore", "How fast do we recover?")]),
  PL("Compute DORA numbers", "Write dora(deploys, failed, days, lead_hours). deploys is the number of deployments in the period, failed how many of them caused trouble, days the length of the period, and lead_hours a list of lead times. Return [deploys per week rounded to 2 places, failure percentage rounded to 1 place, median lead time]. For an even list use the mean of the two middle values.", "dora(deploys, failed, days, lead_hours)",
"""def dora(deploys, failed, days, lead_hours):
    per_week = round(deploys / days * 7, 2)
    pct = round(failed / deploys * 100, 1) if deploys else 0.0
    s = sorted(lead_hours)
    n = len(s)
    if n == 0:
        med = 0
    elif n % 2 == 1:
        med = s[n // 2]
    else:
        med = (s[n // 2 - 1] + s[n // 2]) / 2
    return [per_week, pct, med]
""", [[30, 3, 30, [4, 8, 2]], [10, 0, 14, [1, 3]], [0, 0, 7, []], [21, 2, 7, [10]]], "Scale deployments to a week, divide failures by deployments, and take the middle of the sorted lead times.")]))

A.append(CH(
 "Git: tracking every change",
 ("Git", ["Repository | stores | History", "Commit | is | A snapshot", "Staging area | prepares | A commit", "Branch | is | A movable pointer", "HEAD | points to | Current commit", "Remote | shares | A repository"]),
 ["Git is a distributed version control system. It records every change as a commit, a snapshot of your files with a message, and links the commits into a history.",
  "The everyday cycle is: edit files, git add to stage them, git commit to record them. git status tells you where things stand and git log shows the history.",
  "A commit has an id, an author, a message and a pointer to its parent. That chain of parents is the history, and it is what makes undo, review and collaboration possible."],
 [("Commit", "A saved snapshot of the tracked files, with a message and a parent."), ("Staging area", "Also called the index: the changes you have selected for the next commit."), ("Working tree", "The actual files in your folder."), ("Remote", "Another copy of the repository, for example on a server.")],
 ["Edit, add, commit.", "git status first, always.", "Write commit messages that say why.", "Commits are cheap; commit often."],
 [T("Git keeps three areas. The working tree holds the files you edit. The staging area holds the changes you have chosen for the next commit. The repository holds the committed history. git add copies changes from the working tree to the staging area, and git commit turns the staging area into a new commit."),
  C("git init                       # start a repository here\ngit status                     # what changed?\ngit add app.py                 # stage one file (or . for all)\ngit commit -m \"Add greeting\"   # record it\ngit log --oneline              # the history, newest first\ngit diff                       # unstaged changes\ngit diff --staged              # staged changes"),
  T("The staging area lets you build a commit from just the changes that belong together, even if you edited many files. Write the message as a short summary of the change and, if needed, why you made it. A good history reads like a changelog."),
  T("Every commit has a unique id, a long hash of its contents and its parent. Because the id depends on the history before it, nobody can change an old commit without changing all the ids after it. That makes the history trustworthy and lets two people compare their copies by comparing ids."),
  SH("dgit1", "Lab: your first repository", "Initialise a repository, make two commits and read the log.")],
 [("What does git add do?", ["Stages changes for the next commit", "Records a commit", "Uploads to a server", "Deletes files"], 0, "Working tree to staging area."), ("What does git status show?", ["Changed, staged and untracked files", "The remote URL", "Server load", "Commit authors"], 0, "Always run it first."), ("What links commits into a history?", ["Each points to its parent", "File names", "Dates", "Branch names"], 0, "A chain of parents.")],
 [("Start a repository?", "git init."), ("See the history briefly?", "git log --oneline."), ("Stage everything?", "git add ."), ("Record staged changes?", "git commit -m message.")],
 [ORDER("A first commit", "Put the commands in order for a brand new project.", ["git init", "echo hello > README.md", "git add README.md", "git commit -m \"First commit\"", "git log --oneline"]),
  MATCH("Git areas", "Match each area with what it holds.", [("Working tree", "Files you are editing"), ("Staging area", "Changes chosen for the next commit"), ("Repository", "Committed history"), ("Remote", "A shared copy on a server")])]))

A.append(CH(
 "Branches, merges and conflicts",
 ("Branching", ["Branch | isolates | Work", "Merge | combines | Branches", "Fast-forward | moves | A pointer", "Conflict | needs | A human", "Pull request | asks for | Review", "main | holds | Releasable code"]),
 ["A branch is a lightweight pointer to a commit. You create one to work on a feature without disturbing the main line, then merge it back when it is ready.",
  "If main has not moved since you branched, merging just slides the pointer forward, which is a fast-forward. If both sides changed, git makes a merge commit with two parents.",
  "When both sides changed the same lines, git cannot decide and marks a conflict. You edit the file, choose the right result, add it and commit."],
 [("Branch", "A named pointer to a commit that moves forward as you commit."), ("Merge", "Combining the work of two branches into one."), ("Conflict", "Overlapping changes that git cannot combine automatically."), ("Pull request", "A request to merge a branch, with discussion and review.")],
 ["Branch for every piece of work.", "Keep branches short-lived.", "A conflict is normal, not an error.", "Test before and after merging."],
 [C("git branch                  # list branches\ngit checkout -b feature     # create and switch\n# ...edit, add, commit...\ngit checkout main           # switch back\ngit merge feature           # bring the work in\ngit log --oneline           # see the merge"),
  T("Branches are cheap, so use them freely. A feature branch keeps unfinished work away from the code everyone else uses. In a team flow, you open a pull request, colleagues review it, an automated pipeline checks it and then it is merged. The best branches live for hours or days, not weeks, because the longer they live the more they drift from main."),
  T("A conflict happens when two branches changed the same part of the same file. Git stops and writes both versions into the file between markers: the lines after the first marker are yours, the lines after the equals line are theirs, and the closing marker ends the block. You edit the file to the result you want, delete the markers, run git add on the file and then git commit."),
  C("<<<<<<< HEAD\ntitle: Main\n=======\ntitle: Feature\n>>>>>>> feature"),
  SH("dgit2", "Lab: merge and resolve a conflict", "Two branches changed the same line. Merge them, fix the conflict and finish the merge commit.", 600)],
 [("What is a fast-forward?", ["Moving a pointer without a merge commit", "A faster push", "A deleted branch", "A conflict"], 0, "No divergence."), ("What does a merge conflict need?", ["A human decision", "A reboot", "A new repo", "More RAM"], 0, "Pick the right result."), ("How do you finish a conflict?", ["Edit, git add, git commit", "git delete", "Reinstall git", "Ignore it"], 0, "Add marks it resolved.")],
 [("Create and switch to a branch?", "git checkout -b name."), ("Merge a branch?", "git merge name, from the target branch."), ("What are the markers?", "Lines starting <<<<<<<, ======= and >>>>>>>."), ("Why short branches?", "They drift less and conflict less.")],
 [FILL("Merging", "A {{branch}} is a pointer to a commit. If main has not changed, merging does a {{fast-forward}}. If the same lines changed on both sides, git reports a {{conflict}} that you must resolve.")]))

A.append(CH(
 "Continuous integration",
 ("CI", ["Commit | triggers | A pipeline", "Stage | is | A step group", "Build | compiles | The code", "Test | checks | Behaviour", "Failure | stops | The pipeline", "Green | allows | A merge"]),
 ["Continuous integration means merging small changes into the shared branch often, and letting an automated pipeline build and test every one of them.",
  "A pipeline is a list of stages that run in order, such as build, test and package. If any stage fails, the pipeline stops and tells you which one, so a broken change never reaches the main line.",
  "Good pipelines are fast, reliable and the single source of truth about whether the code works."],
 [("Pipeline", "The automated sequence of stages run for each change."), ("Stage", "One step of a pipeline, such as build or test."), ("Runner", "The machine that executes a pipeline's jobs."), ("Flaky test", "A test that sometimes fails for no real reason and erodes trust.")],
 ["Run the pipeline on every commit.", "Fail fast: cheap checks first.", "A red pipeline blocks the merge.", "Fix flaky tests, do not ignore them."],
 [T("Continuous integration is a habit and a machine. The habit is to merge to the main branch at least daily. The machine is a server that, on every push, checks out the code, builds it, runs the tests and reports the result. Problems are found minutes after they are introduced, when the change is still fresh in mind."),
  C("# pipeline.txt: one stage per line, 'name: command'\nlint:   test -s app.py\nbuild:  echo compiling\ntest:   grep -q \"a + b\" app.py\ndeploy: echo shipping to staging\n\n# stages run in order, the first failure stops the rest"),
  T("Order stages so that the cheapest and fastest checks come first. A linter that takes a second should run before a test suite that takes ten minutes. Use caching so unchanged work is not repeated. Run independent jobs in parallel, but keep the pipeline definition itself in version control next to the code."),
  T("A pipeline you cannot trust is worse than none. A flaky test that fails one run in twenty teaches people to press retry and ignore red. Fix it or delete it. Treat a failing main branch as an emergency, because everyone's work is now blocked."),
  SH("dci", "Lab: make the pipeline green", "The sandbox has a small pipeline runner called ci. Read the failure, fix the bug and add a stage.", 600)],
 [("When should the pipeline run?", ["On every push", "Once a month", "Only before holidays", "Never automatically"], 0, "Frequent integration."), ("What happens when a stage fails?", ["Later stages are skipped", "All stages repeat", "The code is deployed", "Nothing"], 0, "Fail fast."), ("Why order cheap checks first?", ["Feedback arrives sooner", "They look nicer", "It is alphabetical", "Tests are optional"], 0, "Fast feedback.")],
 [("What is CI?", "Merging often and testing every change automatically."), ("What blocks a merge?", "A failing pipeline."), ("Where does the pipeline live?", "In version control with the code."), ("What is a flaky test?", "One that fails randomly.")],
 [PL("Order the stages", "Write stage_order(stages). stages is a list of [name, deps] pairs where deps lists the stages that must run first. Return the names in a valid run order. When several stages are ready, run them in alphabetical order. Assume there is no cycle.", "stage_order(stages)",
"""def stage_order(stages):
    deps = {}
    for name, d in stages:
        deps[name] = list(d)
    done = []
    while len(done) < len(deps):
        ready = []
        for n in deps:
            if n not in done:
                ok = True
                for d in deps[n]:
                    if d not in done:
                        ok = False
                if ok:
                    ready.append(n)
        ready.sort()
        done.append(ready[0])
    return done
""", [[[["test", ["build"]], ["build", []], ["deploy", ["test", "lint"]], ["lint", []]]], [[["a", []]]], [[["c", ["b"]], ["b", ["a"]], ["a", []]]]], "Repeat: pick the alphabetically first stage whose dependencies are all done.")]))

A.append(CH(
 "Build, test and release artifacts",
 ("Artifacts", ["Build | produces | An artifact", "Tests | gate | The release", "Semver | names | Versions", "Registry | stores | Artifacts", "Immutable | means | Never changed", "Reproducible | means | Same inputs, same output"]),
 ["A build turns source code into an artifact: a package, a binary or a container image. The same artifact should travel unchanged through every environment, so what you tested is what you ship.",
  "Version numbers follow semantic versioning: MAJOR.MINOR.PATCH. Increase PATCH for fixes, MINOR for compatible features and MAJOR for breaking changes.",
  "Tests come in layers: many fast unit tests, fewer integration tests and a handful of end-to-end checks. The pipeline runs them from fastest to slowest."],
 [("Artifact", "A built output stored for deployment, such as a package or image."), ("Semantic versioning", "A MAJOR.MINOR.PATCH scheme where each part signals the kind of change."), ("Registry", "A server that stores and serves artifacts."), ("Reproducible build", "A build that gives the same result from the same inputs.")],
 ["Build once, deploy many times.", "Never rebuild for production.", "PATCH fixes, MINOR features, MAJOR breaks.", "Many unit tests, few end-to-end tests."],
 [T("The rule is build once, deploy many. You build an artifact a single time in the pipeline, give it a unique version, store it in a registry and then promote that same artifact through test, staging and production. If you rebuild for each environment you are no longer deploying what you tested."),
  C("# a tiny Makefile; run it with: make test\nbuild:\n\techo compiling\ntest: build\n\techo running tests\n\ngrep -q 'a + b' app.py    # a one-line test: exit 0 means pass"),
  T("Semantic versioning gives numbers a meaning. Version 2.4.1 means major 2, minor 4, patch 1. A fix that changes no behaviour bumps the patch to 2.4.2. A new feature that keeps old users working bumps the minor and resets the patch to 2.5.0. A change that breaks existing users bumps the major and resets both: 3.0.0."),
  T("Tests are a pyramid. At the bottom are unit tests: fast, many, each checking one small thing. Above them are integration tests that check parts working together. At the top are a few end-to-end tests that drive the whole system. The higher you go, the slower and more fragile the tests, so keep the top thin."),
  SH("dmake", "Lab: a build with make", "Use make to run a build then a test, and read how make follows dependencies.", 560)],
 [("What does 'build once' mean?", ["Deploy the same artifact everywhere", "Compile each night", "Build only in production", "Skip tests"], 0, "No rebuild per environment."), ("What does a MAJOR bump signal?", ["A breaking change", "A typo fix", "A new colour", "A comment"], 0, "Users may need to adapt."), ("Which tests should be most numerous?", ["Unit tests", "End-to-end tests", "Manual tests", "Load tests"], 0, "The base of the pyramid.")],
 [("Version after a bug fix on 1.4.2?", "1.4.3."), ("Version after a compatible feature on 1.4.2?", "1.5.0."), ("Where are artifacts kept?", "In a registry."), ("What is a reproducible build?", "Same inputs always give the same output.")],
 [PL("Bump a version", "Write bump(version, part) where version looks like '1.4.2' and part is 'major', 'minor' or 'patch'. Return the new version as text. Bumping major resets minor and patch to 0, bumping minor resets patch to 0.", "bump(version, part)",
"""def bump(version, part):
    a, b, c = [int(x) for x in version.split('.')]
    if part == 'major':
        a += 1
        b = 0
        c = 0
    elif part == 'minor':
        b += 1
        c = 0
    else:
        c += 1
    return str(a) + '.' + str(b) + '.' + str(c)
""", [["1.4.2", "patch"], ["1.4.2", "minor"], ["1.4.2", "major"], ["0.9.9", "patch"], ["10.0.0", "minor"]], "Split into three numbers and reset the smaller ones when a larger one grows."),
  PL("Which is newer?", "Write newer(a, b) that compares two version strings and returns 1 if a is newer than b, -1 if older and 0 if equal. Compare as numbers, so 1.10.0 is newer than 1.9.0.", "newer(a, b)",
"""def newer(a, b):
    x = [int(p) for p in a.split('.')]
    y = [int(p) for p in b.split('.')]
    for i in range(3):
        if x[i] > y[i]:
            return 1
        if x[i] < y[i]:
            return -1
    return 0
""", [["1.10.0", "1.9.0"], ["1.2.3", "1.2.3"], ["0.9.9", "1.0.0"], ["2.0.1", "2.0.0"]], "Compare the major, then the minor, then the patch as integers, not as text.")]))

A.append(CH(
 "Containers and Docker",
 ("Containers", ["Image | is | A template", "Container | is | A running image", "Registry | stores | Images", "Namespace | isolates | Processes", "Port mapping | exposes | A service", "Layer | caches | Build steps"]),
 ["A container packages an application with everything it needs to run, and runs it isolated from other processes using features of the Linux kernel. It starts in a fraction of a second and behaves the same on any machine.",
  "An image is the read-only template, a container is a running instance of it. You pull images from a registry, run them, stop them and remove them.",
  "Ports are mapped from the host to the container, so a web server inside can be reached from outside."],
 [("Image", "A read-only template containing a filesystem and settings."), ("Container", "A running (or stopped) instance of an image."), ("Docker", "The most common tool for building and running containers."), ("Port mapping", "Connecting a host port to a port inside a container, such as -p 8080:80.")],
 ["Image is the recipe, container is the dish.", "docker run image starts a container.", "-p host:container publishes a port.", "Containers are disposable: keep data outside."],
 [T("A virtual machine carries a whole operating system. A container shares the host's kernel and only brings the files and libraries your program needs, so it is small and starts almost instantly. The kernel keeps containers apart using namespaces, which give each its own view of processes, network and filesystem, and control groups, which limit CPU and memory."),
  C("docker pull nginx                       # fetch an image\ndocker run -d --name web -p 8080:80 nginx   # start it in the background\ndocker ps                                # running containers\ncurl http://localhost:8080               # talk to it\ndocker logs web                          # its output\ndocker stop web                          # stop it\ndocker rm web                            # remove it"),
  T("The flag -d runs the container in the background, --name gives it a name you can use later, and -p 8080:80 sends traffic arriving at port 8080 on your machine to port 80 inside. Without -p the container's ports are not reachable from outside. docker ps shows running containers, and docker ps -a also shows stopped ones."),
  T("Treat containers as disposable. When you need a change, you build a new image and replace the container rather than logging in and patching it. Anything that must survive, such as a database's files, goes in a volume outside the container. This is what makes containers easy to scale and replace."),
  SH("ddock1", "Lab: run and stop containers", "The sandbox has a Docker simulator. Run a container, reach it on a port and clean up.", 600)],
 [("What is the difference between an image and a container?", ["An image is a template; a container is a running instance", "They are the same", "A container is a file format", "An image is a network"], 0, "Class and object."), ("What does -p 8080:80 do?", ["Maps host port 8080 to container port 80", "Sets a password", "Pulls an image", "Limits CPU"], 0, "Host side first."), ("Why use volumes?", ["Data must outlive disposable containers", "To speed up CPUs", "To hide logs", "To rename images"], 0, "Persistence.")],
 [("Start a container in the background?", "docker run -d image."), ("List all containers?", "docker ps -a."), ("See output?", "docker logs name."), ("Remove a stopped container?", "docker rm name.")],
 [MATCH("Docker commands", "Match each command with its job.", [("docker pull", "Fetch an image"), ("docker run", "Start a container"), ("docker ps", "List running containers"), ("docker stop", "Stop a container"), ("docker logs", "Show output")])]))

A.append(CH(
 "Dockerfiles and image layers",
 ("Dockerfile", ["Dockerfile | describes | An image", "FROM | picks | A base", "COPY | adds | Files", "RUN | executes | A build command", "CMD | sets | The default command", "Layer cache | reuses | Unchanged steps"]),
 ["A Dockerfile is a recipe for an image. Each instruction adds a layer: FROM chooses the base, COPY adds files, RUN executes a command during the build, and CMD says what runs when the container starts.",
  "Docker caches layers. If an instruction and everything before it are unchanged, the cached layer is reused. Once one step changes, every step after it is rebuilt.",
  "So order matters: put things that change rarely, such as installing dependencies, before things that change often, such as your own code."],
 [("Dockerfile", "A text file of instructions that builds an image."), ("Layer", "The filesystem change made by one instruction; layers stack."), ("Build cache", "Stored layers reused when a step and its predecessors are unchanged."), ("Base image", "The starting image named in FROM.")],
 ["Order from least to most frequently changing.", "Copy requirements before code.", "Keep images small.", "Do not run as root in the container."],
 [C("FROM python:3.12-slim\nCOPY requirements.txt /app/\nRUN pip install -r /app/requirements.txt\nCOPY app.py /app/\nCMD python app.py"),
  T("Read this Dockerfile top to bottom. FROM starts from a small Python image. The requirements file is copied first and the dependencies are installed. Only then is the application code copied. When you edit app.py, the first three layers are unchanged and come from the cache, so only the last COPY and CMD run again. If you had copied all the code before installing, every code edit would reinstall every dependency."),
  T("The cache key for a step includes the instruction text, the layers before it and, for COPY, the contents of the files. That is why changing one early line forces everything after it to rebuild. Small images start faster and have fewer things that can be attacked, so use slim base images, avoid leaving build tools behind and add a .dockerignore file."),
  C("docker build -t myapp:1 .     # build and tag\ndocker images                  # list local images\ndocker run -d --name app myapp:1\ndocker logs app"),
  SH("ddock2", "Lab: build and watch the cache", "Build an image, rebuild without changes, edit the code, rebuild and see which steps are cached.", 620)],
 [("What does RUN do?", ["Executes a command at build time", "Starts the container", "Copies files", "Sets the port"], 0, "Build time, adds a layer."), ("Why copy requirements before code?", ["Dependency layers stay cached when code changes", "It is alphabetical", "It makes images bigger", "Docker requires it"], 0, "Cache order."), ("What happens to steps after a changed one?", ["They rebuild", "They stay cached", "They are deleted", "They run twice"], 0, "The chain is broken.")],
 [("Tag an image while building?", "docker build -t name:tag ."), ("What starts the app?", "CMD."), ("Slim images?", "Smaller and safer."), ("Build cache rule?", "A changed step invalidates all later steps.")],
 [PL("How many steps are cached?", "Write cache_hits(old, new). Each is a list of step strings of a Dockerfile as built before and now (COPY steps are written with a content marker such as 'COPY app.py#v2'). Return how many steps from the start are identical, which is how many come from the cache.", "cache_hits(old, new)",
"""def cache_hits(old, new):
    n = 0
    for i in range(min(len(old), len(new))):
        if old[i] != new[i]:
            break
        n += 1
    return n
""", [[["FROM py", "COPY req#1", "RUN pip", "COPY app#1", "CMD run"], ["FROM py", "COPY req#1", "RUN pip", "COPY app#2", "CMD run"]], [["FROM py", "COPY app#1", "RUN pip"], ["FROM py", "COPY app#2", "RUN pip"]], [["a", "b"], ["a", "b"]], [[], ["a"]]], "Compare step by step and stop at the first difference.")]))

A.append(CH(
 "Kubernetes",
 ("Kubernetes", ["Pod | runs | Containers", "Deployment | keeps | Pods running", "Service | gives | A stable address", "Replica | is | A copy of a pod", "Control loop | closes | The gap", "kubectl | talks to | The cluster"]),
 ["Kubernetes runs containers across many machines. You do not start containers by hand. You describe the state you want, for example three copies of this image, and Kubernetes works constantly to make reality match.",
  "A pod is the smallest unit and holds one or more containers. A deployment keeps a set number of identical pods running and rolls out new versions. A service gives them one stable address.",
  "Because Kubernetes compares desired and actual state in a loop, it heals itself: if a pod dies, a new one appears."],
 [("Pod", "The smallest deployable unit: one or more containers sharing a network."), ("Deployment", "A controller that keeps a desired number of identical pods running."), ("Service", "A stable address and load balancer in front of pods."), ("Manifest", "A YAML file that declares a desired object.")],
 ["Declare the desired state; Kubernetes converges.", "Deployments own pods; services find pods.", "Scale with replicas.", "Roll back with rollout undo."],
 [T("The core idea of Kubernetes is the control loop. You write down what you want in a manifest and apply it. Controllers then watch the real state and act to remove any difference. Delete a pod and the deployment notices it is short by one and creates another. This is called declarative configuration, in contrast to imperative commands that say do this step now."),
  C("apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: web\nspec:\n  replicas: 2\n  template:\n    spec:\n      containers:\n      - name: web\n        image: nginx:1.25\n---\napiVersion: v1\nkind: Service\nmetadata:\n  name: web\nspec:\n  ports:\n  - port: 80\n  selector:\n    app: web"),
  C("kubectl apply -f dep.yaml                 # create or update from the file\nkubectl get pods                           # what is running\nkubectl scale deployment web --replicas=4  # more copies\nkubectl set image deployment/web web=nginx:1.27   # roll out a new version\nkubectl rollout undo deployment/web        # go back if it is broken\nkubectl delete pod NAME                    # it comes back"),
  T("A rolling update replaces pods a few at a time, so the service stays up. If the new version is broken, for example the image cannot be pulled, the new pods never become ready and the old ones keep serving. rollout undo returns to the previous version. get pods shows STATUS values such as Running and ImagePullBackOff, and describe pod shows the events that explain them."),
  SH("dk8s", "Lab: run an app on a cluster", "A tiny cluster simulator understands apply, get, scale, set image and rollout undo.", 640)],
 [("What does a Deployment do?", ["Keeps the desired number of pods running", "Stores secrets", "Builds images", "Routes DNS"], 0, "Self-healing replicas."), ("What happens if you delete a pod owned by a deployment?", ["A replacement is created", "Nothing", "The deployment is deleted", "The cluster stops"], 0, "Control loop."), ("What does rollout undo do?", ["Returns to the previous version", "Deletes the cluster", "Scales to zero", "Pulls logs"], 0, "Rollback.")],
 [("Apply a manifest?", "kubectl apply -f file.yaml."), ("Scale?", "kubectl scale deployment name --replicas=N."), ("What is declarative?", "Say what you want, not the steps."), ("Why a service?", "Pods come and go; the service address stays.")],
 [MATCH("Kubernetes objects", "Match each object with its role.", [("Pod", "Runs containers"), ("Deployment", "Keeps replicas running"), ("Service", "Stable address for pods"), ("Manifest", "YAML that declares state")])]))
