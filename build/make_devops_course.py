#!/usr/bin/env python3
"""Build the DevOps course. Usage: python3 make_devops_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "lxc"))
import cmk, dv1, dv2, labs_devops, app_shell  # noqa: E402

APPS = {}
for k, cfg in labs_devops.LABS.items():
    app_shell.make_shell(cfg, os.path.join(HERE, "lxc", "apps", "sh_%s.html" % k))
    APPS["__SH_%s__" % k] = "sh_%s.html" % k

PRONOUNCE = {
    "DevOps": "dev ops", "DORA": "dora", "CI": "C I", "CD": "C D", "YAML": "yammel", "Git": "git", "git": "git", "GitHub": "git hub", "Docker": "docker", "Dockerfile": "docker file",
    "Kubernetes": "koo ber net ees", "kubectl": "cube control", "nginx": "engine x", "Terraform": "terra form", "OpenTofu": "open tofu", "Pulumi": "pull oo mee", "CloudFormation": "cloud formation",
    "SLO": "S L O", "SLI": "S L I", "SRE": "S R E", "SBOM": "S bomb", "CVE": "C V E", "SAST": "sast", "p99": "P ninety nine", "p95": "P ninety five", "API": "A P I", "URL": "U R L",
    "semver": "sem ver", "MAJOR": "major", "SIGKILL": "sig kill", "sed": "sed", "awk": "awk", "grep": "grep", "iac": "I A C", "IaC": "I A C", "HTTP": "H T T P", "TLS": "T L S", "VM": "V M",
    "pip": "pip", "Makefile": "make file", "Jenkins": "jenkins", "Helm": "helm", "etcd": "et see dee", "RAM": "ram", "CPU": "C P U", "ssh": "S S H", "config": "con fig", "repo": "ree po",
    "canary": "canary", "rollback": "roll back", "idempotent": "eye dem po tent", "idempotence": "eye dem po tence", "toil": "toil", "postmortem": "post mortem", "runbook": "run book",
}

SANDBOX = cmk.terminal("DevOps cheat sheet", "devops>", "A scripted lookup, not a real machine. Try: git, merge, ci, docker, build, k8s, iac, slo, sec", [
    ("git", ["git init, add, commit -m, status, log --oneline, diff", "Edit, add, commit. Status first, always."]),
    ("merge", ["git checkout -b feat, git merge feat", "Conflict: edit, git add file, git commit"]),
    ("ci", ["Every push: build, test, package. First failure stops the pipeline", "Cheap checks first; fix flaky tests"]),
    ("docker", ["docker pull, run -d --name n -p 8080:80 image, ps -a, logs, stop, rm", "Image is the recipe; container is the dish"]),
    ("build", ["FROM, COPY, RUN, CMD; one layer per step", "Copy requirements first, code last for better caching"]),
    ("k8s", ["kubectl apply -f f.yaml, get pods, scale deployment n --replicas=N", "set image deployment/n c=img:tag, rollout undo deployment/n"]),
    ("iac", ["plan shows + ~ -; apply makes it real", "Second apply must change nothing"]),
    ("slo", ["budget = (100 - SLO)% of requests; 99.9% of 1M = 1000", "Restore service first, blameless postmortem after"]),
    ("sec", ["No secrets in Git; env vars or a secrets manager", "Run containers as non-root; scan dependencies; keep an SBOM"]),
])

EXAM = [
 ("What is lead time?", ["Commit to production", "Time to write code", "Meeting length", "Time to hire"], 0, "A DORA metric."),
 ("Which is not a DORA metric?", ["Lines of code", "Deployment frequency", "Change failure rate", "Time to restore"], 0, "Output size is not delivery performance."),
 ("Why ship small changes?", ["Easier to understand and undo", "They avoid tests", "They need no review", "They cost less hardware"], 0, "Small means safe."),
 ("What does git add do?", ["Stages changes", "Commits", "Pushes", "Deletes"], 0, "Working tree to staging area."),
 ("What links commits into a history?", ["Parent pointers", "File names", "Dates", "Branch names"], 0, "Each commit names its parent."),
 ("What is a fast-forward merge?", ["Moves the pointer without a merge commit", "A conflict", "A rebase", "A tag"], 0, "No divergence."),
 ("What do conflict markers look like?", ["<<<<<<< ======= >>>>>>>", "/* */", "### ###", "--- +++"], 0, "Ours, divider, theirs."),
 ("How do you finish a resolved conflict?", ["git add then git commit", "git delete", "git reset only", "Nothing"], 0, "Mark it resolved, then commit."),
 ("When should the CI pipeline run?", ["On every push", "Monthly", "Only before holidays", "By hand only"], 0, "Frequent integration."),
 ("What should happen when a stage fails?", ["Later stages are skipped", "Everything is deployed", "Tests are deleted", "Nothing"], 0, "Fail fast."),
 ("Why put cheap checks first in a pipeline?", ["Faster feedback", "Alphabetical order", "They are optional", "It is a law"], 0, "Fail early."),
 ("What does 'build once, deploy many' mean?", ["Same artifact in every environment", "Build nightly", "Rebuild per environment", "Skip builds"], 0, "What you test is what you ship."),
 ("Which version follows 1.4.2 after a breaking change?", ["2.0.0", "1.4.3", "1.5.0", "1.4.2.1"], 0, "Major bump resets the rest."),
 ("Which version follows 1.4.2 after a compatible feature?", ["1.5.0", "1.4.3", "2.0.0", "1.5.1"], 0, "Minor bump resets patch."),
 ("Which test type should be most numerous?", ["Unit", "End-to-end", "Manual", "Load"], 0, "Base of the pyramid."),
 ("What is a container image?", ["A read-only template", "A running process", "A virtual machine", "A log"], 0, "A container is the running instance."),
 ("What does -p 8080:80 do?", ["Maps host 8080 to container 80", "Limits CPU", "Pulls an image", "Sets a password"], 0, "Host side first."),
 ("Why are containers disposable?", ["State lives outside them", "They are slow", "They cannot restart", "They are free"], 0, "Volumes hold data."),
 ("What does RUN do in a Dockerfile?", ["Executes at build time", "Starts the container", "Sets the port", "Copies files"], 0, "Adds a layer."),
 ("Why copy requirements before the code?", ["Dependency layers stay cached", "It is required", "It shrinks the image to zero", "Docker sorts them"], 0, "Cache order."),
 ("What invalidates later cached layers?", ["A changed earlier step", "A new tag", "A restart", "Time"], 0, "The chain breaks."),
 ("What does a Deployment do?", ["Keeps the desired pods running", "Builds images", "Stores secrets", "Runs DNS"], 0, "Self-healing replicas."),
 ("What happens if you delete a Deployment's pod?", ["A new one is created", "Nothing", "The cluster stops", "The node reboots"], 0, "Control loop."),
 ("What does kubectl rollout undo do?", ["Returns to the previous version", "Deletes pods", "Scales to zero", "Prints logs"], 0, "Rollback."),
 ("What does a Service give pods?", ["A stable address", "More CPU", "A new image", "A password"], 0, "Pods come and go."),
 ("What does a plan show?", ["What would change", "What changed", "Logs", "Costs only"], 0, "Review before apply."),
 ("What does idempotent mean?", ["Running twice equals once", "Fast", "Secret", "Stateless"], 0, "Safe to repeat."),
 ("What is drift?", ["Reality differs from code", "Network lag", "A merge", "A tag"], 0, "Manual changes."),
 ("Where should a database password live?", ["A secrets manager", "The Git repository", "The image", "A comment"], 0, "Injected at run time."),
 ("If a key was committed, you should", ["Revoke and rotate it", "Delete the commit only", "Ignore it", "Rename the file"], 0, "History keeps it."),
 ("What is a canary release?", ["A small share of traffic on the new version", "A full cutover", "A backup", "A test with no users"], 0, "Gradual exposure."),
 ("What do feature flags separate?", ["Deploying from releasing", "Dev from test", "CI from CD", "Pods from nodes"], 0, "Dark launches."),
 ("Which data follows one request across services?", ["Traces", "Metrics", "Dashboards", "Tags"], 0, "Distributed tracing."),
 ("Why look at p99 latency?", ["It shows the slow tail", "It is the average", "It is the fastest", "It is CPU"], 0, "Averages hide pain."),
 ("What should an alert have?", ["An action to take", "No owner", "A joke", "A long delay"], 0, "Runbook."),
 ("What is an error budget?", ["Failure the SLO allows", "Money for bugs", "A log type", "A test limit"], 0, "100% minus SLO."),
 ("A 99.9% SLO over 1,000,000 requests allows how many failures?", ["1000", "100", "10000", "999"], 0, "0.1% of a million."),
 ("What comes first in an incident?", ["Restore service", "Blame", "Write the report", "Redesign"], 0, "Mitigate first."),
 ("Why blameless postmortems?", ["People report honestly", "To save time", "To skip writing", "Legal reasons"], 0, "Learning needs honesty."),
 ("What does shift left mean?", ["Check security earlier", "Deploy more", "Delete code", "Use left screens"], 0, "Closer to the commit."),
 ("What is an SBOM?", ["A list of components in a build", "A server", "A secret", "A test"], 0, "Bill of materials."),
 ("Which user should a container run as?", ["A non-root user", "root", "admin", "nobody at all"], 0, "Least privilege."),
 ("Which image tag is best for production?", ["A specific version", "latest", "test", "none"], 0, "Reproducible rollouts."),
]

CFG = dict(id="devops-from-scratch", title="DevOps from Scratch: Git, CI, Containers, Kubernetes and Reliability",
    subtitle="From commit to production, with a working simulator of git, docker, kubectl and a pipeline in every lab",
    description="A condensed, original course on DevOps. It covers the culture and the DORA metrics, Git and branching, continuous integration, build artifacts and semantic versioning, containers and Dockerfiles, Kubernetes, infrastructure as code, configuration and secrets, release strategies, monitoring, SLOs and incidents, DevSecOps, and a capstone that takes a change from bug to production. Every shell lab runs a Linux-like simulator inside the app, with simplified git, docker, kubectl, make, a CI runner and an infrastructure tool. These are teaching simulators, not the real programs, so they behave like the real tools in the common cases only. Credits: BusyBox (GPL-2.0) and the Jade Agent Kit (MIT).",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="lxc", apps=APPS)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "devops-from-scratch.course.json")
    chs = dv1.A + dv2.B
    for ch in chs:
        labs = [b for b in ch["lesson"] if b["type"] == "webxdc"]
        ch["lesson"] = [b for b in ch["lesson"] if b["type"] != "webxdc"]
        ch["practice"] = labs + ch["practice"]
    cmk.main(CFG, chs, [sys.argv[0], out])
