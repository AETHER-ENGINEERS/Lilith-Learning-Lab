"""DevOps course, chapters 9-15. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *
from lx1 import SH

B = []

B.append(CH(
 "Infrastructure as code",
 ("IaC", ["Code | describes | Infrastructure", "Plan | shows | Differences", "Apply | makes | Changes real", "State | records | What exists", "Idempotent | means | Safe to repeat", "Drift | is | Unplanned change"]),
 ["Infrastructure as code means servers, networks and databases are described in files and created by tools, not by clicking in a console. The files live in version control and are reviewed like any other code.",
  "A good tool works in two steps. Plan compares the files with what exists and shows the difference. Apply makes the world match the files. Running apply twice changes nothing the second time.",
  "That property, idempotence, is what makes automation safe to run again and again."],
 [("Declarative", "Describing the end state you want rather than the steps to reach it."), ("State", "The tool's record of the resources it created."), ("Drift", "When real infrastructure differs from the code, usually after a manual change."), ("Immutable infrastructure", "Replacing servers with new ones instead of modifying them.")],
 ["Describe, plan, review, apply.", "Never hand-edit what code manages.", "Plans are reviewed like code.", "Apply twice must change nothing."],
 [T("Clicking through a console is quick once and impossible to repeat exactly. Code can be reviewed, tested, copied to make a second environment and rolled back through version control. Tools such as Terraform, OpenTofu, Pulumi and CloudFormation turn a description of resources into API calls."),
  C("# infra.txt: one resource per line, 'type name properties'\nserver web size=small\ndb main size=large\n\niac plan     # + server.web, + db.main\niac apply    # creates them\niac apply    # No changes. Infrastructure matches the configuration."),
  T("The plan lists what would be created with a plus, changed with a tilde and destroyed with a minus. Read it before every apply: a surprising minus is the thing the review exists to catch. The state file lets the tool know which real resources belong to which lines of code, so protect it and keep it in a shared, locked place."),
  T("Drift happens when someone changes a resource by hand. The next plan shows the difference and apply corrects it. Many teams go further and forbid manual changes entirely. Servers become cattle, not pets: if one is wrong you replace it from code instead of nursing it."),
  SH("diac", "Lab: plan, apply and change infrastructure", "A tiny infrastructure tool called iac reads infra.txt. Create, change and remove resources and watch the plan.", 620)],
 [("What does plan do?", ["Shows what would change", "Makes the changes", "Deletes state", "Builds images"], 0, "Review before apply."), ("What does idempotent mean here?", ["A second apply changes nothing", "Apply is fast", "Apply is secret", "State is optional"], 0, "Safe to repeat."), ("What is drift?", ["Reality differs from the code", "A slow network", "A bug in tests", "A merge conflict"], 0, "Usually manual edits.")],
 [("Why code for infrastructure?", "Review, repeat, version and roll back."), ("What is state?", "The record of what the tool created."), ("What does a minus in a plan mean?", "A resource will be destroyed."), ("Pets or cattle?", "Cattle: replace, don't nurse.")],
 [PL("Build a plan", "Write plan(want, have). Both are dictionaries from resource name to a settings string. Return a sorted list of lines: '+ name' for resources in want but not in have, '~ name' for resources whose settings differ and '- name' for resources in have but not in want. Sort the lines as plain text.", "plan(want, have)",
"""def plan(want, have):
    out = []
    for k in want:
        if k not in have:
            out.append('+ ' + k)
        elif want[k] != have[k]:
            out.append('~ ' + k)
    for k in have:
        if k not in want:
            out.append('- ' + k)
    return sorted(out)
""", [[{"web": "small", "db": "large"}, {}], [{"web": "large"}, {"web": "small", "old": "x"}], [{"a": "1"}, {"a": "1"}], [{}, {"a": "1"}]], "Check three cases: new, changed and removed. Sort the finished list.")]))

B.append(CH(
 "Configuration and secrets",
 ("Config", ["Config | differs by | Environment", "Env vars | carry | Settings", "Secret | must stay | Private", "Vault | stores | Secrets", "Twelve-factor | separates | Config from code", "Rotation | limits | Leaks"]),
 ["The same build runs in development, staging and production, so what differs between them must be configuration kept outside the code: addresses, feature flags and credentials.",
  "Environment variables are the simplest way to pass configuration into a program. Settings are layered: defaults in code, then a config file, then environment variables, with later layers winning.",
  "Secrets such as passwords and API keys need extra care: never commit them, store them in a secrets manager, give them the least access needed and rotate them."],
 [("Environment variable", "A named value passed to a process by its environment."), ("Secret", "A credential such as a password, token or private key."), ("Secrets manager", "A service that stores secrets, controls access and logs use."), ("Rotation", "Regularly replacing a secret so a leaked one stops working.")],
 ["Code is the same everywhere; config differs.", "Never commit secrets.", "Layer settings: defaults, file, environment.", "Rotate and limit every secret."],
 [T("The twelve-factor approach to building applications says to store configuration in the environment. The code reads DATABASE_URL and does not care whether it points at a test database or the real one. The same artifact, with different variables, becomes a different environment."),
  C("# layered settings: later wins\ndefaults:  port=8080 debug=false\nfile:      port=9090\nenv:       DEBUG=true\n=> port=9090 debug=true\n\nexport API_URL=https://staging.example.com\n./app"),
  T("A secret committed to Git is compromised forever. Even after you delete it, it stays in the history, and bots scan public repositories for keys within minutes. Keep secrets out of the repository and out of images. Put them in a secrets manager or in your platform's secret store, and inject them at run time."),
  T("If a secret does leak, the fix is not to delete the commit but to revoke the secret and issue a new one. Make this easy by rotating secrets on a schedule, scoping each one to the least access it needs and keeping an audit log of who used it.")],
 [("Where should a database password live?", ["In a secrets manager", "In the Git repository", "In the image", "In a comment"], 0, "Injected at run time."), ("What does twelve-factor say about config?", ["Keep it in the environment", "Hard-code it", "Use a new build per environment", "Put it in tests"], 0, "Same build, different variables."), ("If a key is committed, you should", ["Revoke and replace it", "Delete the commit only", "Ignore it", "Rename the file"], 0, "History keeps it.")],
 [("Pass config to a program?", "Environment variables."), ("Layer order?", "Defaults, then file, then environment."), ("Leaked secret?", "Revoke and rotate."), ("Where do secrets go?", "A secrets manager.")],
 [PL("Resolve settings", "Write resolve(defaults, file, env). Each is a dictionary of text settings. Later layers override earlier ones: env beats file beats defaults. Return a sorted list of [key, value] pairs.", "resolve(defaults, file, env)",
"""def resolve(defaults, file, env):
    out = {}
    for layer in (defaults, file, env):
        for k in layer:
            out[k] = layer[k]
    return [[k, out[k]] for k in sorted(out)]
""", [[{"port": "8080", "debug": "false"}, {"port": "9090"}, {"debug": "true"}], [{}, {}, {}], [{"a": "1"}, {}, {"a": "2", "b": "3"}]], "Copy defaults first, then file, then env, so later values win.")]))

B.append(CH(
 "Continuous delivery and release strategies",
 ("Delivery", ["Continuous delivery | keeps | Code releasable", "Blue-green | switches | Two environments", "Canary | tests | A small share", "Feature flag | hides | Unfinished features", "Rollback | restores | The old version", "Staging | rehearses | Production"]),
 ["Continuous delivery means every change that passes the pipeline could be released at any moment. Continuous deployment goes one step further and releases automatically.",
  "Release safely by exposing a change gradually. A canary sends a small share of traffic to the new version and watches the errors. Blue-green keeps two full environments and switches between them. Feature flags separate deploying code from turning a feature on.",
  "Whatever the method, you need a fast, rehearsed way back: a rollback must be one command, not a project."],
 [("Canary release", "Sending a small percentage of traffic to a new version before everyone."), ("Blue-green deployment", "Running old and new environments side by side and switching traffic."), ("Feature flag", "A switch that turns a feature on or off without deploying."), ("Rollback", "Returning to the previous known good version.")],
 ["Deploy is not release: flags separate them.", "Start with a few percent, then widen.", "Watch error rate and latency during rollout.", "Practise the rollback."],
 [T("Deploying means putting code on servers. Releasing means exposing it to users. Treating them as separate steps is what makes releases calm. With a feature flag the new code ships switched off, you turn it on for staff, then for one percent of users, then everyone, and if something is wrong you flip the switch back without a deployment."),
  T("A canary release starts the new version on a few instances, say five percent of traffic, and compares its error rate and speed with the old version. If it looks as good, the share grows in steps until everyone has it. If it looks worse, the canary is removed and most users never noticed. Blue-green keeps two production environments. You deploy to the idle one, test it, then switch the router. Rollback is switching back."),
  C("kubectl set image deployment/web web=nginx:1.27   # rolling update\nkubectl rollout status deployment/web\nkubectl rollout undo deployment/web                # roll back"),
  T("Rollouts need data to be safe. A pipeline should check health after each step and stop on its own when the error rate rises. Database changes are the hard part: make them backward compatible, in small steps, so both versions can run at once.")],
 [("What is a canary release?", ["A small share of traffic on the new version", "A full cutover", "A test with no users", "A backup"], 0, "Tests in production gently."), ("What do feature flags separate?", ["Deploying from releasing", "Dev from test", "Git from CI", "Pods from services"], 0, "Code can be dark."), ("What makes rollback quick?", ["Practice and one command", "A long meeting", "A new release", "Manual SQL"], 0, "Rehearse it.")],
 [("Deploy vs release?", "Deploy puts code on servers; release exposes it to users."), ("Blue-green idea?", "Two environments, switch traffic."), ("Safest first canary size?", "A few percent."), ("When to roll back?", "As soon as error rate or latency worsens.")],
 [PL("Canary decision", "Write canary(new_requests, new_errors, base_requests, base_errors, margin). If the canary has seen fewer than 100 requests return 'wait'. Otherwise compare error rates (errors divided by requests): return 'promote' if the canary rate is at most the baseline rate plus margin, else 'rollback'.", "canary(new_requests, new_errors, base_requests, base_errors, margin)",
"""def canary(new_requests, new_errors, base_requests, base_errors, margin):
    if new_requests < 100:
        return 'wait'
    new_rate = new_errors / new_requests
    base_rate = base_errors / base_requests if base_requests else 0.0
    if new_rate <= base_rate + margin:
        return 'promote'
    return 'rollback'
""", [[500, 2, 10000, 40, 0.005], [500, 20, 10000, 40, 0.005], [50, 0, 10000, 40, 0.005], [200, 1, 5000, 10, 0.0]], "Compute both error rates as fractions and compare with the margin.")]))

B.append(CH(
 "Monitoring and observability",
 ("Observability", ["Metrics | count | Things over time", "Logs | record | Events", "Traces | follow | A request", "Dashboard | shows | Health", "Alert | wakes | A human", "Percentile | describes | Latency"]),
 ["You cannot run what you cannot see. Observability rests on three kinds of data: metrics, which are numbers over time; logs, which are records of events; and traces, which follow a single request through many services.",
  "For averages, use percentiles. The 99th percentile latency says how slow the slowest one in a hundred requests is, and that is what unhappy users feel.",
  "Alert on symptoms that users notice, such as errors and slowness, not on every internal number, or people will learn to ignore the pager."],
 [("Metric", "A numeric measurement sampled over time, such as requests per second."), ("Log", "A timestamped record of something that happened."), ("Trace", "The path and timing of one request across services."), ("Percentile", "The value below which a given share of measurements fall.")],
 ["Metrics, logs and traces answer different questions.", "Average hides pain; look at p95 and p99.", "Alert on user-facing symptoms.", "Every alert needs an action."],
 [T("Metrics are cheap and tell you that something is wrong: error rate is up. Logs tell you what happened in detail: this request failed with a timeout. Traces tell you where the time went across services: the delay is in the payment call. You use them in that order, from the dashboard to the log to the trace."),
  T("Averages lie. If ninety-nine requests take 100 milliseconds and one takes ten seconds, the average is about 200 milliseconds and looks fine, but one user in a hundred waited ten seconds. Percentiles describe the tail. The 50th percentile is the median, the 95th is the value that 95 percent of requests beat, and the 99th shows the worst experiences."),
  C("# each log line: time status latency_ms\nawk '{print $3}' app.log | sort -n | tail -1      # slowest\ngrep -c ' 5[0-9][0-9] ' app.log                    # server errors\nawk '$2 >= 500 {e++} END {print e / NR * 100}' app.log   # error percent"),
  T("An alert should mean a human must act now. Page on symptoms, such as the error rate is above the target or the site is slow, rather than causes, such as CPU is at 80 percent, which may be harmless. Every alert needs a runbook, a short document that says what it means and what to do. If an alert fires often and nobody acts, delete it or fix its cause."),
  SH("dmon", "Lab: read the numbers", "A request log is waiting. Use grep, awk and sort to measure error rate and find the slowest requests.", 620)],
 [("What does p99 latency tell you?", ["How slow the slowest 1% of requests are", "The average", "The fastest request", "The CPU use"], 0, "Look at the tail."), ("Which data follows one request across services?", ["Traces", "Metrics", "Dashboards", "Tags"], 0, "Distributed tracing."), ("What should an alert have?", ["An action to take", "A joke", "A long delay", "No owner"], 0, "Runbook.")],
 [("Three signals?", "Metrics, logs, traces."), ("Why not averages?", "They hide slow outliers."), ("Alert on what?", "Symptoms users feel."), ("What is a runbook?", "Steps for responding to an alert.")],
 [PL("Percentile", "Write percentile(values, p) using the nearest-rank method: sort the values, compute rank = ceil(p / 100 * n) with a minimum of 1, and return the value at that rank (counting from 1). Return 0 for an empty list.", "percentile(values, p)",
"""def percentile(values, p):
    if not values:
        return 0
    s = sorted(values)
    n = len(s)
    r = p * n / 100
    k = int(r)
    if k < r:
        k += 1
    if k < 1:
        k = 1
    return s[k - 1]
""", [[[10, 20, 30, 40, 50], 50], [[10, 20, 30, 40, 50], 95], [[3, 1, 2], 100], [[], 90], [[100, 100, 100, 100, 9000], 99], [[5], 1]], "Nearest rank: round the position up, then subtract one for zero-based indexing.")]))

B.append(CH(
 "SLOs, error budgets and incidents",
 ("SRE", ["SLI | measures | Service quality", "SLO | sets | A target", "Error budget | allows | Some failure", "Incident | needs | A response", "Postmortem | learns | Without blame", "Toil | is | Automated away"]),
 ["A service level indicator, SLI, is a measurement of how well a service works, for instance the share of requests that succeed. A service level objective, SLO, is the target for it, such as 99.9 percent over 30 days.",
  "The gap between perfect and the SLO is the error budget. While budget remains you can ship quickly; when it runs out you slow down and fix reliability.",
  "When something breaks, handle it as an incident: one person leads, you communicate, you restore service first and investigate afterwards, then write a blameless postmortem."],
 [("SLI", "Service level indicator: a measured value such as the success rate."), ("SLO", "Service level objective: the target for an SLI."), ("Error budget", "The amount of failure the SLO allows in a period."), ("Postmortem", "A written, blameless review of an incident and what to change.")],
 ["100% is the wrong target.", "Budget = 100% minus the SLO.", "Spend budget on change; protect it when low.", "Restore first, find the cause second."],
 [T("Perfect reliability is impossible and absurdly expensive, and users cannot tell the difference between 99.99 percent and 100 percent. So you pick a target that is good enough, for example 99.9 percent of requests succeed over thirty days. That is the SLO, and everything you do is balanced against it."),
  M(r"\text{allowed failures}=(1-\text{SLO})\times\text{total requests}"),
  T("With a 99.9 percent SLO and one million requests in the period, the budget is one thousand failed requests. If you have used four hundred, you have six hundred left. A fast burn tells you to stop risky releases and fix the cause. A budget barely touched means you may be too cautious and can release faster. This turns the argument between speed and stability into arithmetic."),
  T("During an incident, name an incident lead, open a channel, tell users what you know, and focus on restoring service, often by rolling back, before hunting the root cause. Afterwards, write a postmortem. A good one describes the timeline, the impact and the contributing causes, and ends with concrete actions. It asks what in the system allowed this to happen, not who made the mistake. Blame teaches people to hide problems, and hidden problems come back bigger.")],
 [("What is an error budget?", ["The failure the SLO allows", "Money for fixing bugs", "A log file", "A test limit"], 0, "100% minus the SLO."), ("In an incident, what comes first?", ["Restore service", "Find who is to blame", "Write the report", "Redesign"], 0, "Mitigate, then investigate."), ("Why blameless postmortems?", ["People report problems honestly", "To save time", "To avoid writing", "They are legal rules"], 0, "Learning needs honesty.")],
 [("SLO of 99.9% over 1M requests allows?", "1000 failed requests."), ("What is an SLI?", "A measured quality number."), ("Budget exhausted?", "Slow releases, fix reliability."), ("First incident step?", "Restore service.")],
 [PL("Error budget", "Write error_budget(slo, total, failed) where slo is a percentage such as 99.9, total the number of requests and failed the number that failed. Return [allowed failures rounded down to a whole number, remaining budget as a whole number which may be negative]. Allowed is (100 - slo) / 100 * total.", "error_budget(slo, total, failed)",
"""def error_budget(slo, total, failed):
    allowed = int(round((100 - slo) * total / 100.0, 6))
    return [allowed, allowed - failed]
""", [[99.9, 1000000, 400], [99.0, 10000, 150], [99.99, 1000000, 100], [100, 1000, 0]], "Allowed failures are the non-SLO share of the total; remaining is allowed minus failed.")]))

B.append(CH(
 "DevSecOps and the software supply chain",
 ("DevSecOps", ["Shift left | moves | Security earlier", "SAST | scans | Source code", "Dependency scan | finds | Known flaws", "SBOM | lists | Components", "Signing | proves | Origin", "Least privilege | limits | Damage"]),
 ["DevSecOps builds security into the pipeline instead of adding it at the end. Scanning for secrets, vulnerable dependencies and risky configuration runs on every change, where fixes are cheap.",
  "Modern software is mostly other people's code. A software bill of materials lists every component so that when a flaw is announced you can find out at once whether you use it.",
  "Protect the pipeline itself: sign artifacts, use short-lived credentials, run containers as non-root users and give each job the least access it needs."],
 [("Shift left", "Doing security checks earlier in the process, nearer to the commit."), ("SBOM", "Software bill of materials: a list of the components in a build."), ("CVE", "A public identifier for a known vulnerability."), ("Supply chain attack", "Compromising software by attacking something it depends on or the way it is built.")],
 ["Scan every commit for secrets and known vulnerable dependencies.", "Pin and update dependencies.", "Run containers as non-root.", "Sign what you build."],
 [T("Finding a security problem in a pull request costs minutes. Finding it in production costs an incident. So checks run early: a secret scanner looks for keys in each commit, a dependency scanner compares your libraries to a database of known vulnerabilities, and a linter for container and infrastructure files flags risky settings such as running as root."),
  C("grep -rn 'API_KEY\\|PASSWORD\\|secret' .     # crude secret hunt\nsed -i 's/sk_live_abc123/${API_KEY}/' app.conf    # move it to an env var\necho '.env' >> .gitignore                          # never commit it\n\n# Dockerfile: do not run as root\nRUN adduser --system app\nUSER app"),
  T("Most of your code is dependencies, and each one is a way in. Pin versions so builds are repeatable, update them regularly and let a scanner tell you when one is vulnerable. Keep a software bill of materials so that when the next big flaw is announced you can answer in minutes whether you are affected."),
  T("Attackers also target the build. Use short-lived credentials rather than long-lived keys, give each pipeline job only the access it needs, require review for changes to pipeline files, and sign artifacts so that production can check that an image really came from your pipeline.")  ,
  SH("dsec", "Lab: find and fix leaked secrets", "A project has a hard-coded key, a missing ignore rule and a container that runs as root. Fix all three.", 620)],
 [("What does shift left mean?", ["Check security earlier", "Deploy more often", "Delete old code", "Use left-hand screens"], 0, "Nearer the commit."), ("What is an SBOM?", ["A list of components in a build", "A server type", "A secret", "A test"], 0, "Bill of materials."), ("A leaked key in Git history needs", ["Revocation and rotation", "A force push only", "Nothing", "A bigger repo"], 0, "Assume it is stolen.")],
 [("Scan for what?", "Secrets, vulnerable dependencies, risky config."), ("Container user?", "Non-root."), ("What is a CVE?", "A public id for a known flaw."), ("Pin dependencies why?", "Repeatable, reviewable builds.")],
 [PL("Find vulnerable packages", "Write vulnerable(deps, advisories). deps is a list like 'requests==2.19.0'. advisories is a list like 'requests<2.20.0' meaning every version below 2.20.0 is vulnerable. Return the sorted names of vulnerable packages. Compare versions as lists of numbers.", "vulnerable(deps, advisories)",
"""def ver(s):
    return [int(x) for x in s.split('.')]


def vulnerable(deps, advisories):
    limit = {}
    for a in advisories:
        name, v = a.split('<')
        limit[name] = ver(v)
    out = []
    for d in deps:
        name, v = d.split('==')
        if name in limit and ver(v) < limit[name]:
            out.append(name)
    return sorted(out)
""", [[["requests==2.19.0", "flask==3.0.0"], ["requests<2.20.0", "flask<2.2.5"]], [["a==1.9.0"], ["a<1.10.0"]], [[], ["a<1.0"]], [["x==1.0.0"], []]], "Parse each advisory into a name and a limit, then compare version lists.")]))

B.append(CH(
 "Capstone: ship a change end to end",
 ("Capstone", ["Commit | starts | The pipeline", "CI | validates | The change", "Image | packages | The app", "Registry | holds | The artifact", "Manifest | declares | The release", "Cluster | runs | The new version"]),
 ["Put the whole path together. A small project has a bug, a pipeline, a Dockerfile and a Kubernetes manifest. You will fix the bug, make the pipeline pass, build a versioned image and roll it out.",
  "Work like a DevOps engineer: change one thing at a time, check the result of each step, and keep everything in version control.",
  "When the checklist is complete you will have touched version control, CI, containers and orchestration on one change."],
 [("Release", "A specific version of the software made available to users."), ("Rollout", "The process of replacing the running version with a new one."), ("Provenance", "A record of how and from what an artifact was built."), ("Toil", "Manual repeated work that a pipeline should do instead.")],
 ["Commit, test, package, deploy.", "Tag images with a version, not latest.", "Verify after rollout.", "Keep the previous version ready."],
 [T("A real change flows through every chapter of this course. You edit code on a branch, commit it, and the pipeline builds and tests it. A passing change is merged, packaged into an image with a version tag, pushed to a registry and rolled out to the cluster. Monitoring then confirms that users are better off, and if not, the rollout is undone."),
  T("The lab below is that flow in miniature. The sandbox understands git, ci, docker and kubectl. The checklist gives the destination, not the route: use what you have learned. If you get stuck, press Hint for the commands."),
  SH("dcap", "Capstone lab: from bug to production", "Fix the bug, turn the pipeline green, build shop:1.0 and roll it out with three replicas.", 660),
  T("You now have the shape of modern delivery. The next steps are practice on real tools: set up a pipeline in a hosted service, deploy a container to a small cluster and watch its metrics. The ideas will carry over to every tool you meet.")],
 [("Which image tag is best for production?", ["A specific version", "latest", "test", "none"], 0, "Reproducible rollouts."), ("What confirms a rollout worked?", ["Health checks and metrics", "The deploy command exiting", "Silence", "A meeting"], 0, "Observe."), ("What should be in version control?", ["Everything: code, config, infra, pipeline", "Only code", "Only secrets", "Nothing"], 0, "Reproducibility.")],
 [("Flow of a change?", "Commit, CI, package, deploy, observe."), ("If the rollout is bad?", "Roll back."), ("Tag images with?", "Versions, not latest."), ("What goes wrong with manual steps?", "They drift and are hard to repeat.")],
 [ORDER("Ship a change", "Put the steps in a sensible order.", ["git commit -am \"fix total\"", "ci", "docker build -t shop:1.0 .", "kubectl apply -f deploy.yaml", "kubectl get pods"])]))
