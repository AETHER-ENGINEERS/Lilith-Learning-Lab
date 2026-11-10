"""Shell lab definitions for the DevOps course."""
import random
from labs_linux import F

BUGPIPE = "build: test -f app.txt && echo compiling\ntest: grep -q \"a + b\" app.txt\ndeploy: echo deploying to staging\n"

def monlog():
    r = random.Random(11)
    lines = []
    st = ["200"] * 51 + ["404"] * 3 + ["500", "500", "503", "500", "503", "500"]
    r.shuffle(st)
    lat = [r.randint(20, 400) for _ in range(60)]
    lat[7], lat[23], lat[41] = 1800, 950, 870
    for i in range(60):
        lines.append("10:%02d:%02d %s %d" % (i // 60, i % 60, st[i], lat[i]))
    errs = sum(1 for s in st if s[0] == "5")
    return "\n".join(lines) + "\n", errs, sorted(lat, reverse=True)[:3]

MON, ERRS, TOP3 = monlog()

DEP = ("apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: web\nspec:\n  replicas: 2\n  template:\n    spec:\n      containers:\n      - name: web\n        image: nginx:1.25\n"
       "---\napiVersion: v1\nkind: Service\nmetadata:\n  name: web\nspec:\n  ports:\n  - port: 80\n  selector:\n    app: web\n")
SHOPDEP = ("apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: shop\nspec:\n  replicas: 1\n  template:\n    spec:\n      containers:\n      - name: shop\n        image: shop:0.9\n")

LABS = {}
GITBASE = ["git init", "printf 'title: Demo\\n' > app.txt", "git add .", "git commit -m base", "git checkout -b feature", "echo 'title: Feature' > app.txt", "git commit -am feature-title", "git checkout main", "echo 'title: Main' > app.txt", "git commit -am main-title"]

LABS["dgit1"] = dict(devops=True, intro="<b>Your first repository.</b> You are in an empty project with two files.",
    hints=["git init", "git status", "git add .", "git commit -m \"first\"", "echo \"print('bye')\" >> app.py", "git commit -am \"second\"", "git log --oneline"],
    files={"/home/user/README.md": "My project\n", "/home/user/app.py": "print('hello')\n"},
    tasks=[{"t": "Create a repository with git init", "check": "S.git.inited"},
           {"t": "Commit both files (git add . then git commit)", "check": "Object.keys(S.git.commits).length>=1 && Object.keys(S.git.index).length>=2"},
           {"t": "Change app.py and make a second commit", "check": "Object.keys(S.git.commits).length>=2"},
           {"t": "Read the history with git log --oneline", "check": "ran('git log')"},
           {"t": "Check that the working tree is clean with git status", "check": "ran('git status') && out.indexOf('working tree clean')>=0"}],
    solution="git init\ngit add .\ngit commit -m first\necho \"print('bye')\" >> app.py\ngit commit -am second\ngit log --oneline\ngit status")

LABS["dgit2"] = dict(devops=True, intro="<b>Merge and resolve a conflict.</b> Branches <code>main</code> and <code>feature</code> both changed the title in <code>app.txt</code>. You are on main.",
    hints=["git log --oneline", "git branch", "git merge feature", "git status", "cat app.txt", "echo 'title: Both' > app.txt", "git add app.txt", "git commit -m \"merge feature\""],
    files={}, init=GITBASE,
    tasks=[{"t": "Try to merge feature into main", "check": "ran('git merge') && out.indexOf('CONFLICT')>=0"},
           {"t": "Look at the conflict markers in app.txt", "check": "ran('cat app.txt')"},
           {"t": "Edit app.txt so it has one title line and no markers", "check": "fs.read('app.txt').indexOf('<<<<')<0 && fs.read('app.txt').indexOf('title')>=0"},
           {"t": "Stage the file and commit the merge", "check": "!S.git.merging && Object.keys(S.git.commits).some(function(k){return S.git.commits[k].parents.length==2})"},
           {"t": "Show the history with git log --oneline", "check": "ran('git log')"}],
    solution="git merge feature\ncat app.txt\necho 'title: Both' > app.txt\ngit add app.txt\ngit commit -m merged\ngit log --oneline")

LABS["dci"] = dict(devops=True, intro="<b>Make the pipeline green.</b> <code>ci</code> runs the stages in <code>pipeline.txt</code>. The code has a bug.",
    hints=["cat pipeline.txt", "ci", "cat app.txt", "sed -i 's/a - b/a + b/' app.txt", "echo 'lint: test -s app.txt' >> pipeline.txt"],
    files={"/home/user/app.txt": "total = a - b\n", "/home/user/pipeline.txt": BUGPIPE},
    tasks=[{"t": "Run the pipeline and watch it fail at test", "check": "ran('^ci') && out.indexOf('FAIL test')>=0"},
           {"t": "Fix the bug in app.txt (a - b should be a + b)", "check": "fs.read('app.txt').indexOf('a + b')>=0"},
           {"t": "Run the pipeline again: all three stages pass", "check": "!!S.ci.last && !S.ci.last.failed && S.ci.last.passed.length>=3"},
           {"t": "Add a lint stage to pipeline.txt", "check": "fs.read('pipeline.txt').indexOf('lint:')>=0"},
           {"t": "Run it: four stages pass", "check": "!!S.ci.last && !S.ci.last.failed && S.ci.last.passed.length>=4"}],
    solution="ci\nsed -i 's/a - b/a + b/' app.txt\nci\necho 'lint: test -s app.txt' >> pipeline.txt\nci")

LABS["dmake"] = dict(devops=True, intro="<b>A build with make.</b> <code>Makefile</code> lines that start a recipe use a tab.",
    hints=["cat Makefile", "make", "make test", "printf 'package: test\\n\\techo packaged\\n' >> Makefile", "make package"],
    files={"/home/user/Makefile": "all: build test\nbuild:\n\techo compiling\ntest: build\n\techo running tests\n"},
    tasks=[{"t": "Run make with no target (it builds the first target)", "check": "ran('^make *$')"},
           {"t": "Run make test and notice that build runs first", "check": "ran('^make test') && out.indexOf('compiling')>=0"},
           {"t": "Add a package target that depends on test", "check": "fs.read('Makefile').indexOf('package:')>=0"},
           {"t": "Run make package and see packaged", "check": "ran('^make package') && out.indexOf('packaged')>=0"}],
    solution="make\nmake test\nprintf 'package: test\\n\\techo packaged\\n' >> Makefile\nmake package")

LABS["ddock1"] = dict(devops=True, intro="<b>Run and stop containers.</b> This is a Docker simulator: no real images are downloaded.",
    hints=["docker run alpine echo hello", "docker run -d --name web -p 8080:80 nginx", "docker ps", "curl http://localhost:8080", "docker logs web", "docker stop web", "docker rm web"],
    files={},
    tasks=[{"t": "Run alpine and make it say hello", "check": "ran('docker run .*alpine') && out.indexOf('hello')>=0"},
           {"t": "Start nginx detached as web, mapping port 8080 to 80", "check": "S.dk.containers.some(function(c){return c.name=='web'&&c.status=='Up'&&c.ports.length>0})"},
           {"t": "List running containers with docker ps", "check": "ran('docker ps')"},
           {"t": "Fetch the page with curl on port 8080", "check": "out.indexOf('Welcome to nginx')>=0"},
           {"t": "Stop and remove web", "check": "ran('docker stop') && !S.dk.containers.some(function(c){return c.name=='web'})"}],
    solution="docker run alpine echo hello\ndocker run -d --name web -p 8080:80 nginx\ndocker ps\ncurl http://localhost:8080\ndocker stop web\ndocker rm web")

LABS["ddock2"] = dict(devops=True, intro="<b>Build an image and watch the cache.</b> The Dockerfile copies the requirements first, then the code.",
    hints=["cat Dockerfile", "docker build -t myapp:1 .", "docker build -t myapp:2 .", "echo \"print('v2')\" >> app.py", "docker build -t myapp:3 .", "docker run -d --name app myapp:3", "docker logs app"],
    files={"/home/user/Dockerfile": "FROM python:3.12-slim\nCOPY requirements.txt /app/\nRUN pip install -r /app/requirements.txt\nCOPY app.py /app/\nCMD python /app/app.py\n", "/home/user/requirements.txt": "flask\n", "/home/user/app.py": "print('v1')\n"},
    tasks=[{"t": "Build the image as myapp:1", "check": "!!S.dk.images['myapp:1']"},
           {"t": "Build again as myapp:2 without changes: every step is cached", "check": "!!S.dk.builds && S.dk.builds.length>=2 && S.dk.builds[1].steps.every(function(s){return s.cached})"},
           {"t": "Edit app.py and build myapp:3: the pip step stays cached, the code copy does not", "check": "(function(){var b=S.dk.builds&&S.dk.builds[2];if(!b)return false;var r=b.steps.filter(function(s){return s.ins=='RUN'})[0];var cp=b.steps.filter(function(s){return s.ins=='COPY'});return !!r&&r.cached&&!cp[cp.length-1].cached})()"},
           {"t": "Run myapp:3 in the background as app and read its logs", "check": "S.dk.containers.some(function(c){return c.image=='myapp:3'}) && ran('docker logs')"}],
    solution="docker build -t myapp:1 .\ndocker build -t myapp:2 .\necho \"print('v2')\" >> app.py\ndocker build -t myapp:3 .\ndocker run -d --name app myapp:3\ndocker logs app")

LABS["dk8s"] = dict(devops=True, intro="<b>Run an app on a cluster.</b> A cluster simulator understands apply, get, scale, delete, set image and rollout undo.",
    hints=["cat dep.yaml", "kubectl apply -f dep.yaml", "kubectl get pods", "kubectl scale deployment web --replicas=4", "kubectl delete pod web-4df5c8114d-x7k2p", "kubectl set image deployment/web web=nginx:1.27", "kubectl set image deployment/web web=nginx:broken", "kubectl rollout undo deployment/web"],
    files={"/home/user/dep.yaml": DEP},
    tasks=[{"t": "Create the deployment and service from dep.yaml", "check": "!!S.k8s.deploys.web && !!S.k8s.svcs.web"},
           {"t": "Scale web to 4 replicas", "check": "!!S.k8s.deploys.web && S.k8s.deploys.web.replicas==4 && S.k8s.deploys.web.pods.length>=4"},
           {"t": "Delete one pod and see that the deployment replaces it", "check": "ran('kubectl delete pod') && S.k8s.deploys.web.pods.length>=4"},
           {"t": "Roll out nginx:1.27", "check": "ran('nginx:1\\\\.27')"},
           {"t": "Roll out the broken image nginx:broken, then undo it", "check": "ran('nginx:broken') && ran('rollout undo') && S.k8s.deploys.web.image.indexOf('broken')<0"}],
    solution="kubectl apply -f dep.yaml\nkubectl scale deployment web --replicas=4\nkubectl delete pod web-4df5c8114d-x7k2p\nkubectl set image deployment/web web=nginx:1.27\nkubectl set image deployment/web web=nginx:broken\nkubectl get pods\nkubectl rollout undo deployment/web")

LABS["diac"] = dict(devops=True, intro="<b>Plan and apply infrastructure.</b> <code>iac</code> reads <code>infra.txt</code> (one resource per line) and keeps a state file.",
    hints=["cat infra.txt", "iac plan", "iac apply", "sed -i 's/server web size=small/server web size=large/' infra.txt", "sed -i '/^db /d' infra.txt", "iac state"],
    files={"/home/user/infra.txt": "server web size=small\ndb main size=large\ncache redis size=small\n"},
    tasks=[{"t": "Look at the plan before applying", "check": "ran('iac plan')"},
           {"t": "Apply it to create the resources", "check": "fs.exists('.iac-state') && fs.read('.iac-state').indexOf('db.main')>=0"},
           {"t": "Change the web server to size=large and apply", "check": "fs.read('.iac-state').indexOf('\"server.web\":\"size=large\"')>=0"},
           {"t": "Remove the db line and apply: the db is destroyed", "check": "fs.exists('.iac-state') && fs.read('.iac-state').indexOf('db.main')<0 && fs.read('.iac-state').indexOf('server.web')>=0"},
           {"t": "Apply once more and see that nothing changes", "check": "out.indexOf('No changes')>=0"}],
    solution="iac plan\niac apply\nsed -i 's/server web size=small/server web size=large/' infra.txt\niac apply\nsed -i '/^db /d' infra.txt\niac apply\niac apply")

LABS["dmon"] = dict(intro="<b>Read the numbers.</b> <code>app.log</code> lines are <code>time status latency_ms</code>.",
    hints=["wc -l app.log", "grep -c ' 5[0-9][0-9] ' app.log", "awk '{print $3}' app.log | sort -n | tail -1", "awk '$2 >= 500 {e++} END {print e / NR * 100}' app.log", "awk '{print $3}' app.log | sort -n | tail -3 > slow.txt"],
    files={"/home/user/app.log": MON},
    tasks=[{"t": "Count the requests with wc -l", "check": "ran('wc +-l') && out.indexOf('60')>=0"},
           {"t": "Count the server errors (status 5xx) with grep -c", "check": "ran('grep +-c') && /(^|\\n)%d\\n/.test(out)" % ERRS},
           {"t": "Work out the error percentage with awk", "check": "ran('awk') && /(^|\\n)%s(\\n|\\.)/.test(out)" % ("%d" % round(ERRS / 60 * 100))},
           {"t": "Find the slowest request with sort and tail", "check": "ran('sort') && ran('tail') && out.indexOf('%d')>=0" % TOP3[0]},
           {"t": "Save the three slowest latencies in slow.txt", "check": "fs.read('slow.txt').trim().split('\\n').length==3 && fs.read('slow.txt').indexOf('%d')>=0" % TOP3[0]}],
    solution="wc -l app.log\ngrep -c ' 5[0-9][0-9] ' app.log\nawk '$2 >= 500 {e++} END {print e / NR * 100}' app.log\nawk '{print $3}' app.log | sort -n | tail -1\nawk '{print $3}' app.log | sort -n | tail -3 > slow.txt")

LABS["dsec"] = dict(devops=True, intro="<b>Find and fix leaked secrets.</b> The project has a hard-coded key and password, no ignore rule for <code>.env</code>, and runs as root.",
    hints=["cat app.conf", "grep -rn -i 'key' .", "echo 'API_KEY=sk_live_abc123' > .env", "sed -i 's/sk_live_abc123/${API_KEY}/' app.conf", "sed -i 's/hunter2/${DB_PASSWORD}/' app.conf", "echo '.env' >> .gitignore", "echo 'USER app' >> Dockerfile"],
    files={"/home/user/app.conf": "db_host=localhost\napi_key=sk_live_abc123\npassword=hunter2\n", "/home/user/.gitignore": "*.pyc\n", "/home/user/Dockerfile": "FROM python:3.12-slim\nCOPY app.py /app/\nCMD python /app/app.py\n", "/home/user/app.py": "print('app')\n"},
    tasks=[{"t": "Search the project for secrets with grep -r", "check": "ran('^grep +-[a-z]*r')"},
           {"t": "Remove the key and password from app.conf", "check": "fs.read('app.conf').indexOf('sk_live_abc123')<0 && fs.read('app.conf').indexOf('hunter2')<0"},
           {"t": "Keep the key in a .env file instead", "check": "fs.read('.env').indexOf('sk_live_abc123')>=0"},
           {"t": "Add .env to .gitignore", "check": "fs.read('.gitignore').split('\\n').indexOf('.env')>=0"},
           {"t": "Make the Dockerfile run as a non-root USER", "check": "/^USER +(?!root)\\w+/m.test(fs.read('Dockerfile'))"}],
    solution="grep -rn -i key .\necho 'API_KEY=sk_live_abc123' > .env\nsed -i 's/sk_live_abc123/${API_KEY}/' app.conf\nsed -i 's/hunter2/${DB_PASSWORD}/' app.conf\necho '.env' >> .gitignore\necho 'USER app' >> Dockerfile")

LABS["dcap"] = dict(devops=True, intro="<b>From bug to production.</b> The project has a bug, a pipeline, a Dockerfile and a manifest that still points at shop:0.9.",
    hints=["ls", "git init", "git add .", "git commit -m start", "ci", "sed -i 's/a - b/a + b/' app.txt", "git commit -am \"fix total\"", "docker build -t shop:1.0 .", "sed -i 's/shop:0.9/shop:1.0/' deploy.yaml", "kubectl apply -f deploy.yaml", "kubectl scale deployment shop --replicas=3"],
    files={"/home/user/app.txt": "total = a - b\n", "/home/user/pipeline.txt": BUGPIPE, "/home/user/Dockerfile": "FROM python:3.12-slim\nCOPY app.txt /app/\nCMD python /app/app.txt\n", "/home/user/deploy.yaml": SHOPDEP},
    tasks=[{"t": "Put the project under version control with a first commit", "check": "S.git.inited && Object.keys(S.git.commits).length>=1"},
           {"t": "Fix the bug in app.txt", "check": "fs.read('app.txt').indexOf('a + b')>=0"},
           {"t": "Make the pipeline pass (run ci)", "check": "!!S.ci.last && !S.ci.last.failed"},
           {"t": "Commit the fix", "check": "Object.keys(S.git.commits).length>=2"},
           {"t": "Build the image shop:1.0", "check": "!!S.dk.images['shop:1.0']"},
           {"t": "Point deploy.yaml at shop:1.0 and apply it", "check": "!!S.k8s.deploys.shop && S.k8s.deploys.shop.image=='shop:1.0'"},
           {"t": "Scale shop to 3 replicas", "check": "!!S.k8s.deploys.shop && S.k8s.deploys.shop.replicas==3"}],
    solution="git init\ngit add .\ngit commit -m start\nsed -i 's/a - b/a + b/' app.txt\nci\ngit commit -am 'fix total'\ndocker build -t shop:1.0 .\nsed -i 's/shop:0.9/shop:1.0/' deploy.yaml\nkubectl apply -f deploy.yaml\nkubectl scale deployment shop --replicas=3\nkubectl get pods")
