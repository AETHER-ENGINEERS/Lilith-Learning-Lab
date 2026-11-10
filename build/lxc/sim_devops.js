/* DevOps simulators on top of LinuxSim: git, docker, kubectl, iac, ci, make. Original code, deliberately simplified. */
function DevopsCmds(S) {
  var C = S.commands, v = S.vfs;
  function hash(str) { var h = 5381; for (var i = 0; i < str.length; i++) h = ((h << 5) + h + str.charCodeAt(i)) >>> 0; var s = h.toString(16); while (s.length < 8) s = "0" + s; return s }
  function hex(n, seed) { var s = ""; var k = 0; while (s.length < n) s += hash(seed + ":" + (k++)); return s.slice(0, n) }
  function fail(c, m, code) { c.err(m + "\n"); return code || 1 }
  function lineDiff(a, b) { var A = a.split("\n"), B = b.split("\n"), n = A.length, m = B.length, L = []; for (var i = 0; i <= n; i++) L.push(new Array(m + 1).fill(0)); for (var i2 = n - 1; i2 >= 0; i2--) for (var j = m - 1; j >= 0; j--) L[i2][j] = A[i2] == B[j] ? L[i2 + 1][j + 1] + 1 : Math.max(L[i2 + 1][j], L[i2][j + 1]); var i3 = 0, j3 = 0, out = []; while (i3 < n || j3 < m) { if (i3 < n && j3 < m && A[i3] == B[j3]) { out.push(" " + A[i3]); i3++; j3++ } else if (i3 < n && (j3 == m || L[i3 + 1][j3] >= L[i3][j3 + 1])) { out.push("-" + A[i3]); i3++ } else { out.push("+" + B[j3]); j3++ } } return out }
  /* ================= git ================= */
  S.git = { inited: false, root: null, head: "main", branches: {}, commits: {}, index: {}, merging: null, remotes: {}, pushed: {}, tags: {}, n: 0 };
  var G = S.git;
  function rel(p) { return p.slice(G.root.length + 1) }
  function abspath(r) { return G.root + "/" + r }
  function walk(dir, acc) { S.names(dir).forEach(function (n) { if (n == ".git") return; var q = dir + "/" + n; if (v.isDir(q)) walk(q, acc); else acc.push(rel(q)) }); return acc }
  function headTree() { var id = G.branches[G.head]; return id ? G.commits[id].tree : {} }
  function readW(r) { return v.exists(abspath(r)) ? v.read(abspath(r)) : null }
  function commitObj(msg, parents) { var tree = JSON.parse(JSON.stringify(G.index)); var id = hash(msg + JSON.stringify(tree) + parents.join(",") + (G.n++)) + hex(33, msg + G.n); id = id.slice(0, 40); G.commits[id] = { id: id, msg: msg, parents: parents, tree: tree, n: G.n }; return id }
  function ancestors(id) { var seen = {}, q = [id], order = []; while (q.length) { var x = q.shift(); if (!x || seen[x]) continue; seen[x] = 1; order.push(x); G.commits[x].parents.forEach(function (p) { q.push(p) }) } return { set: seen, order: order } }
  function writeTree(tree, from) { Object.keys(from || {}).forEach(function (r) { if (!(r in tree) && v.exists(abspath(r))) v.rm(abspath(r)) }); Object.keys(tree).forEach(function (r) { var p = abspath(r); v.mkdirp(S.dir(p)); S.writeFile(p, tree[r]) }) }
  function dirty() { var bad = []; Object.keys(G.index).forEach(function (r) { var w = readW(r); if (w !== G.index[r]) bad.push(r) }); var ht = headTree(); if (JSON.stringify(ht) != JSON.stringify(G.index)) Object.keys(G.index).concat(Object.keys(ht)).forEach(function (r) { if (G.index[r] !== ht[r] && bad.indexOf(r) < 0) bad.push(r) }); return bad }
  function switchTo(c, name) { var bad = dirty(); if (bad.length) { c.err("error: Your local changes to the following files would be overwritten by checkout:\n" + bad.map(function (b) { return "\t" + b }).join("\n") + "\nPlease commit your changes or stash them before you switch branches.\nAborting\n"); return 1 } var from = headTree(); G.head = name; var to = headTree(); writeTree(to, from); G.index = JSON.parse(JSON.stringify(to)); return 0 }
  function resolveRef(x) { if (G.branches[x]) return G.branches[x]; if (G.tags[x]) return G.tags[x]; if (G.commits[x]) return x; var m = Object.keys(G.commits).filter(function (k) { return k.indexOf(x) == 0 }); return m.length == 1 ? m[0] : null }
  C["git"] = async function (c) {
    var a = c.args.slice(), sub = a.shift();
    if (!sub || sub == "--version") { c.out("git version 2.43.0 (sandbox)\n"); return 0 }
    if (sub == "config") return 0;
    if (sub == "init") { G.inited = true; G.root = S.cwd; G.head = "main"; G.branches = {}; G.commits = {}; G.index = {}; v.mkdirp(S.cwd + "/.git"); S.create(S.cwd + "/.git", true); c.out("Initialized empty Git repository in " + S.cwd + "/.git/\n"); return 0 }
    if (sub == "clone") return fail(c, "fatal: unable to access remote: the sandbox is offline", 128);
    if (!G.inited) return fail(c, "fatal: not a git repository (or any of the parent directories): .git", 128);
    if (sub == "add") { if (!a.length) return fail(c, "Nothing specified, nothing added.", 0); var rc = 0; a.forEach(function (f) { if (f == "-A" || f == "--all") f = G.root; var p = S.abs(f); if (!v.exists(p)) { if (rel(p) in G.index) { delete G.index[rel(p)]; return } c.err("fatal: pathspec '" + f + "' did not match any files\n"); rc = 128; return } var files = v.isDir(p) ? walk(p, []) : [rel(p)]; if (f == "." || p == G.root) Object.keys(G.index).forEach(function (r) { if (!v.exists(abspath(r))) delete G.index[r] }); files.forEach(function (r) { G.index[r] = readW(r); G.merging && G.merging.conflicts.splice(G.merging.conflicts.indexOf(r) >= 0 ? G.merging.conflicts.indexOf(r) : 99, 1) }) }); return rc }
    if (sub == "rm") { a.filter(function (x) { return x[0] != "-" }).forEach(function (f) { var p = S.abs(f); delete G.index[rel(p)]; if (v.exists(p)) v.rm(p) }); return 0 }
    if (sub == "commit") {
      var mi = a.indexOf("-m"), am = a.indexOf("-am") >= 0, msg = mi >= 0 ? a[mi + 1] : (am ? a[a.indexOf("-am") + 1] : null);
      if (am) Object.keys(G.index).forEach(function (r) { var w = readW(r); if (w === null) delete G.index[r]; else G.index[r] = w });
      if (G.merging) { if (G.merging.conflicts.length) return fail(c, "error: Committing is not possible because you have unmerged files.\nhint: Fix them up in the work tree, and then use 'git add/rm <file>'", 128); var pid = G.branches[G.head]; var id0 = commitObj(msg || "Merge branch '" + G.merging.name + "'", [pid, G.merging.theirs]); G.branches[G.head] = id0; G.merging = null; c.out("[" + G.head + " " + id0.slice(0, 7) + "] " + G.commits[id0].msg + "\n"); return 0 }
      if (!msg) return fail(c, "Aborting commit due to empty commit message.", 1);
      var ht = headTree(); if (JSON.stringify(ht) == JSON.stringify(G.index)) { c.out("On branch " + G.head + "\nnothing to commit, working tree clean\n"); return 1 }
      var par = G.branches[G.head] ? [G.branches[G.head]] : []; var id = commitObj(msg, par); G.branches[G.head] = id;
      var ch = Object.keys(G.index).filter(function (r) { return ht[r] !== G.index[r] }).length + Object.keys(ht).filter(function (r) { return !(r in G.index) }).length;
      c.out("[" + G.head + (par.length ? "" : " (root-commit)") + " " + id.slice(0, 7) + "] " + msg + "\n " + ch + " file" + (ch == 1 ? "" : "s") + " changed\n"); return 0 }
    if (sub == "status") {
      var h = headTree(), staged = [], unst = [], untr = [], files = walk(G.root, []);
      Object.keys(G.index).forEach(function (r) { if (!(r in h)) staged.push("new file:   " + r); else if (h[r] !== G.index[r]) staged.push("modified:   " + r) }); Object.keys(h).forEach(function (r) { if (!(r in G.index)) staged.push("deleted:    " + r) });
      Object.keys(G.index).forEach(function (r) { if (G.merging && G.merging.conflicts.indexOf(r) >= 0) return; var w = readW(r); if (w === null) unst.push("deleted:    " + r); else if (w !== G.index[r]) unst.push("modified:   " + r) });
      files.forEach(function (r) { if (!(r in G.index)) untr.push(r) });
      c.out("On branch " + G.head + "\n");
      if (G.merging) { c.out("You have unmerged paths.\n  (fix conflicts and run \"git commit\")\n\n"); if (G.merging.conflicts.length) { c.out("Unmerged paths:\n"); G.merging.conflicts.forEach(function (r) { c.out("\tboth modified:   " + r + "\n") }); c.out("\n") } }
      if (staged.length) { c.out("Changes to be committed:\n  (use \"git restore --staged <file>...\" to unstage)\n"); staged.forEach(function (x) { c.out("\t" + x + "\n") }); c.out("\n") }
      if (unst.length) { c.out("Changes not staged for commit:\n  (use \"git add <file>...\" to update what will be committed)\n"); unst.forEach(function (x) { c.out("\t" + x + "\n") }); c.out("\n") }
      if (untr.length) { c.out("Untracked files:\n  (use \"git add <file>...\" to include in what will be committed)\n"); untr.forEach(function (x) { c.out("\t" + x + "\n") }); c.out("\n") }
      if (!staged.length && !unst.length && !untr.length && !G.merging) c.out(G.branches[G.head] ? "nothing to commit, working tree clean\n" : "\nNo commits yet\n\nnothing to commit (create/copy files and use \"git add\" to track)\n");
      return 0 }
    if (sub == "log") { var one = a.indexOf("--oneline") >= 0, ni = a.findIndex(function (x) { return /^-\d+$/.test(x) }), lim = ni >= 0 ? -parseInt(a[ni]) : 999; var id1 = G.branches[G.head]; if (!id1) return fail(c, "fatal: your current branch '" + G.head + "' does not have any commits yet", 128); ancestors(id1).order.sort(function (x, y) { return G.commits[y].n - G.commits[x].n }).slice(0, lim).forEach(function (id) { var o = G.commits[id]; if (one) c.out(id.slice(0, 7) + (id == G.branches[G.head] ? " (HEAD -> " + G.head + ")" : "") + " " + o.msg + "\n"); else c.out("commit " + id + "\nAuthor: User <user@lilith>\nDate:   Mon Nov 9 10:00:00 2026\n\n    " + o.msg + "\n\n") }); return 0 }
    if (sub == "branch") { var names = a.filter(function (x) { return x[0] != "-" }); if (a.indexOf("-d") >= 0 || a.indexOf("-D") >= 0) { names.forEach(function (n) { delete G.branches[n]; c.out("Deleted branch " + n + "\n") }); return 0 } if (names.length) { if (G.branches[names[0]]) return fail(c, "fatal: a branch named '" + names[0] + "' already exists", 128); G.branches[names[0]] = G.branches[G.head]; return 0 } if (!G.branches[G.head]) return 0; Object.keys(G.branches).sort().forEach(function (b) { c.out((b == G.head ? "* " : "  ") + b + "\n") }); return 0 }
    if (sub == "checkout" || sub == "switch") {
      var nb = a.indexOf("-b") >= 0 || a.indexOf("-c") >= 0; var nm = a.filter(function (x) { return x[0] != "-" })[0];
      if (sub == "checkout" && !nb && a.indexOf("--") >= 0) { a.slice(a.indexOf("--") + 1).forEach(function (f) { var t = headTree()[rel(S.abs(f))]; if (t !== undefined) S.writeFile(S.abs(f), t) }); return 0 }
      if (!nm) return fail(c, "fatal: missing branch name", 128);
      if (nb) { if (G.branches[nm]) return fail(c, "fatal: a branch named '" + nm + "' already exists", 128); G.branches[nm] = G.branches[G.head]; G.head = nm; c.err("Switched to a new branch '" + nm + "'\n"); return 0 }
      if (!G.branches[nm]) { var f2 = S.abs(nm); if (sub == "checkout" && v.exists(f2) && headTree()[rel(f2)] !== undefined) { S.writeFile(f2, headTree()[rel(f2)]); return 0 } return fail(c, "error: pathspec '" + nm + "' did not match any file(s) known to git", 1) }
      if (nm == G.head) { c.err("Already on '" + nm + "'\n"); return 0 }
      var r0 = switchTo(c, nm); if (!r0) c.err("Switched to branch '" + nm + "'\n"); return r0 }
    if (sub == "merge") {
      var nm2 = a.filter(function (x) { return x[0] != "-" })[0]; if (!G.branches[nm2]) return fail(c, "merge: " + nm2 + " - not something we can merge", 1);
      var ours = G.branches[G.head], theirs = G.branches[nm2]; if (dirty().length) return fail(c, "error: Your local changes would be overwritten by merge. Commit or stash them first.", 1);
      var ao = ancestors(ours), at = ancestors(theirs);
      if (ao.set[theirs]) { c.out("Already up to date.\n"); return 0 }
      if (at.set[ours]) { var from = headTree(); G.branches[G.head] = theirs; var to = headTree(); writeTree(to, from); G.index = JSON.parse(JSON.stringify(to)); c.out("Updating " + ours.slice(0, 7) + ".." + theirs.slice(0, 7) + "\nFast-forward\n"); return 0 }
      var base = ao.order.filter(function (x) { return at.set[x] })[0], bt = base ? G.commits[base].tree : {}, ot = G.commits[ours].tree, tt = G.commits[theirs].tree, conflicts = [], res = {};
      var keys = {}; [bt, ot, tt].forEach(function (t) { Object.keys(t).forEach(function (k) { keys[k] = 1 }) });
      Object.keys(keys).forEach(function (k) { var b = bt[k], o = ot[k], t = tt[k]; if (o === t) { if (o !== undefined) res[k] = o } else if (o === b) { if (t !== undefined) res[k] = t } else if (t === b) { if (o !== undefined) res[k] = o } else { conflicts.push(k); res[k] = "<<<<<<< HEAD\n" + (o === undefined ? "" : o.replace(/\n?$/, "\n")) + "=======\n" + (t === undefined ? "" : t.replace(/\n?$/, "\n")) + ">>>>>>> " + nm2 + "\n" } });
      writeTree(res, ot);
      var idx = {}; Object.keys(res).forEach(function (k) { idx[k] = conflicts.indexOf(k) >= 0 ? (ot[k] === undefined ? "" : ot[k]) : res[k] }); G.index = idx;
      if (conflicts.length) { G.merging = { theirs: theirs, name: nm2, conflicts: conflicts }; conflicts.forEach(function (k) { c.out("Auto-merging " + k + "\nCONFLICT (content): Merge conflict in " + k + "\n") }); c.out("Automatic merge failed; fix conflicts and then commit the result.\n"); return 1 }
      var mid = commitObj("Merge branch '" + nm2 + "'", [ours, theirs]); G.branches[G.head] = mid; c.out("Merge made by the 'ort' strategy.\n"); return 0 }
    if (sub == "diff") { var staged2 = a.indexOf("--staged") >= 0 || a.indexOf("--cached") >= 0, h2 = headTree(); var any = false; Object.keys(G.index).forEach(function (r) { var before = staged2 ? h2[r] : G.index[r], after = staged2 ? G.index[r] : readW(r); if (before === after || after === null || (!staged2 && after === undefined)) return; any = true; c.out("diff --git a/" + r + " b/" + r + "\n--- a/" + r + "\n+++ b/" + r + "\n"); lineDiff(before === undefined ? "" : before.replace(/\n$/, ""), after.replace(/\n$/, "")).forEach(function (l) { if (l[0] != " ") c.out(l + "\n") }) }); return 0 }
    if (sub == "tag") { if (a[0]) { G.tags[a[0]] = G.branches[G.head]; return 0 } Object.keys(G.tags).sort().forEach(function (t) { c.out(t + "\n") }); return 0 }
    if (sub == "remote") { if (a[0] == "add") { G.remotes[a[1]] = a[2]; return 0 } Object.keys(G.remotes).forEach(function (r) { c.out(r + (a[0] == "-v" ? "\t" + G.remotes[r] + " (push)" : "") + "\n") }); return 0 }
    if (sub == "push") { var rem = a.filter(function (x) { return x[0] != "-" })[0] || "origin", br = a.filter(function (x) { return x[0] != "-" })[1] || G.head; if (!G.remotes[rem]) return fail(c, "fatal: '" + rem + "' does not appear to be a git repository", 128); if (!G.branches[br]) return fail(c, "error: src refspec " + br + " does not match any", 1); var was = G.pushed[br] === G.branches[br]; G.pushed[br] = G.branches[br]; c.out(was ? "Everything up-to-date\n" : "To " + G.remotes[rem] + "\n * [new branch]      " + br + " -> " + br + "\n"); return 0 }
    if (sub == "pull" || sub == "fetch") { c.out("Already up to date.\n"); return 0 }
    if (sub == "restore") { var st = a.indexOf("--staged") >= 0; a.filter(function (x) { return x[0] != "-" }).forEach(function (f) { var r = rel(S.abs(f)), t = headTree()[r]; if (st) { if (t === undefined) delete G.index[r]; else G.index[r] = t } else if (G.index[r] !== undefined) S.writeFile(S.abs(f), G.index[r]) }); return 0 }
    if (sub == "revert") { var id2 = G.branches[G.head], o2 = id2 && G.commits[id2]; if (!o2 || !o2.parents.length) return fail(c, "error: nothing to revert", 1); var pt = G.commits[o2.parents[0]].tree; var from3 = headTree(); G.index = JSON.parse(JSON.stringify(pt)); writeTree(pt, from3); var nid = commitObj("Revert \"" + o2.msg + "\"", [id2]); G.branches[G.head] = nid; c.out("[" + G.head + " " + nid.slice(0, 7) + "] Revert \"" + o2.msg + "\"\n"); return 0 }
    return fail(c, "git: '" + sub + "' is not supported in this sandbox", 1);
  };
  /* ================= docker ================= */
  S.dk = { images: { "alpine:latest": { size: "7.8MB", id: hex(12, "alpine") }, "nginx:latest": { size: "187MB", id: hex(12, "nginx"), web: true } }, known: { alpine: "7.8MB", nginx: "187MB", python: "1.0GB", node: "1.1GB", redis: "138MB", ubuntu: "78MB" }, containers: [], cache: {}, n: 0 };
  var D = S.dk;
  function imgRef(x) { return x.indexOf(":") >= 0 ? x : x + ":latest" }
  function findC(x) { return D.containers.filter(function (k) { return k.name == x || k.id.indexOf(x) == 0 })[0] }
  C["docker"] = async function (c) {
    var a = c.args.slice(), sub = a.shift();
    if (!sub || sub == "--version") { c.out("Docker version 26.1.0 (sandbox simulator)\n"); return 0 }
    if (sub == "pull") { var im = imgRef(a[0] || ""), base = im.split(":")[0]; if (!D.known[base] && !D.images[im]) return fail(c, "Error response from daemon: pull access denied for " + base + ", repository does not exist", 1); if (!D.images[im]) D.images[im] = { size: D.known[base], id: hex(12, im), web: base == "nginx" }; c.out("Pulling from library/" + base + "\nStatus: Downloaded newer image for " + im + "\n"); return 0 }
    if (sub == "images") { c.out("REPOSITORY".padEnd(16) + "TAG".padEnd(12) + "IMAGE ID".padEnd(14) + "SIZE\n"); Object.keys(D.images).forEach(function (k) { var p = k.split(":"); c.out(p[0].padEnd(16) + p[1].padEnd(12) + D.images[k].id.padEnd(14) + D.images[k].size + "\n") }); return 0 }
    if (sub == "rmi") { a.forEach(function (x) { delete D.images[imgRef(x)] }); return 0 }
    if (sub == "build") {
      var ti = a.indexOf("-t"), tag = ti >= 0 ? imgRef(a[ti + 1]) : null, ctx = S.abs(a.filter(function (x, i) { return x[0] != "-" && a[i - 1] != "-t" })[0] || "."), df = ctx + "/Dockerfile";
      if (!v.exists(df)) return fail(c, "ERROR: failed to read dockerfile: open Dockerfile: no such file or directory", 1);
      var lines = v.read(df).split("\n").map(function (l) { return l.trim() }).filter(function (l) { return l && l[0] != "#" }), key = "", cmd = null, size = 7.8, expose = null, env = {}, n = lines.length, steps = [];
      for (var i = 0; i < lines.length; i++) { var L = lines[i], ins = L.split(/\s+/)[0].toUpperCase(), rest = L.slice(ins.length).trim(); c.out("Step " + (i + 1) + "/" + n + " : " + L + "\n"); if (i == 0 && ins != "FROM") return fail(c, "ERROR: Dockerfile parse error: first instruction must be FROM", 1);
        if (ins == "FROM") { var fi = imgRef(rest.split(/\s+/)[0]), fb = fi.split(":")[0]; if (!D.known[fb] && !D.images[fi]) return fail(c, "ERROR: pull access denied for " + fb, 1); if (!D.images[fi]) D.images[fi] = { size: D.known[fb], id: hex(12, fi) }; key = fi; size = parseFloat(D.images[fi].size) || 7.8; if (/GB/.test(D.images[fi].size)) size *= 1000; steps = []; c.out(" ---> " + D.images[fi].id + "\n"); continue }
        var extra = ""; if (ins == "COPY" || ins == "ADD") { var src = rest.split(/\s+/)[0], sp = S.abs(ctx + "/" + src); if (!v.exists(sp)) return fail(c, "ERROR: failed to compute cache key: \"/" + src + "\" not found", 1); var walkf = function (p) { return v.isDir(p) ? S.names(p).map(function (nn) { return walkf(p + "/" + nn) }).join("") : v.read(p) }; extra = hash(walkf(sp)); size += 0.2 }
        if (ins == "RUN") size += 12; if (ins == "CMD" || ins == "ENTRYPOINT") cmd = rest; if (ins == "EXPOSE") expose = rest; if (ins == "ENV") { var ev = rest.split(/[= ]/); env[ev[0]] = ev.slice(1).join("=") }
        key = hash(key + "|" + L + "|" + extra); var cached = !!D.cache[key] && ins != "CMD" && ins != "EXPOSE" && ins != "ENV" || (D.cache[key] && (ins == "CMD" || ins == "EXPOSE" || ins == "ENV")); steps.push({ ins: ins, cached: !!D.cache[key] }); if (D.cache[key]) c.out(" ---> Using cache\n"); else { c.out(" ---> Running in " + hex(12, key + D.n) + "\n"); D.cache[key] = 1 } c.out(" ---> " + hex(12, key) + "\n") }
      var iid = hex(12, key); var tg = tag || "<none>:<none>"; D.images[tg] = { size: size.toFixed(0) + "MB", id: iid, cmd: cmd, expose: expose, env: env, web: false }; c.out("Successfully built " + iid + "\n" + (tag ? "Successfully tagged " + tag + "\n" : "")); D.builds = (D.builds || []).concat([{ tag: tg, steps: steps }]); return 0 }
    if (sub == "run") {
      var o = { d: false, name: null, ports: [], rm: false, env: [] }, rest2 = [];
      for (var k = 0; k < a.length; k++) { var x = a[k]; if (rest2.length) { rest2.push(x); continue } if (x == "-d" || x == "--detach") o.d = true; else if (x == "--rm") o.rm = true; else if (x == "--name") o.name = a[++k]; else if (x == "-p") o.ports.push(a[++k]); else if (x == "-e") o.env.push(a[++k]); else if (x == "-it" || x == "-i" || x == "-t") { } else if (x[0] == "-") { } else rest2.push(x) }
      if (!rest2.length) return fail(c, "docker: \"run\" requires at least 1 argument.", 125);
      var im2 = imgRef(rest2[0]), cmdw = rest2.slice(1), b2 = im2.split(":")[0];
      if (!D.images[im2]) { if (!D.known[b2]) return fail(c, "docker: Error response from daemon: pull access denied for " + b2 + ", repository does not exist or may require 'docker login'.", 125); c.out("Unable to find image '" + im2 + "' locally\nStatus: Downloaded newer image for " + im2 + "\n"); D.images[im2] = { size: D.known[b2], id: hex(12, im2), web: b2 == "nginx" } }
      var info = D.images[im2], cid = hex(64, "c" + (D.n++)), nm = o.name || ["quirky_turing", "calm_hopper", "brave_ritchie", "eager_thompson"][D.n % 4];
      if (findC(nm)) return fail(c, "docker: Error response from daemon: Conflict. The container name \"/" + nm + "\" is already in use.", 125);
      var ct = { id: cid.slice(0, 12), full: cid, name: nm, image: im2, ports: o.ports, status: "Up", cmd: cmdw.length ? cmdw.join(" ") : (info.cmd || (info.web ? "nginx -g 'daemon off;'" : "/bin/sh")), logs: "", env: o.env, web: !!info.web };
      if (o.d) { ct.logs = info.web ? "nginx: ready for connections\n" : "started: " + ct.cmd + "\n"; D.containers.push(ct); c.out(cid + "\n"); return 0 }
      var words = cmdw.length ? cmdw : null; if (!words && info.cmd) { words = info.cmd.replace(/^\[|\]$/g, "").replace(/["',]/g, " ").trim().split(/\s+/) }
      var out = ""; if (words && (C[words[0]] || S.builtins[words[0]])) { await S.call(words, { stdin: "", out: function (s) { out += s; c.out(s) }, err: c.err }) } else if (words) { out = "started: " + words.join(" ") + "\n"; c.out(out) }
      ct.status = "Exited (0)"; ct.logs = out; if (!o.rm) D.containers.push(ct); return 0 }
    if (sub == "ps") { var all = a.indexOf("-a") >= 0; c.out("CONTAINER ID".padEnd(14) + "IMAGE".padEnd(16) + "COMMAND".padEnd(28) + "STATUS".padEnd(14) + "PORTS".padEnd(24) + "NAMES\n"); D.containers.filter(function (k) { return all || k.status == "Up" }).forEach(function (k) { c.out(k.id.padEnd(14) + k.image.padEnd(16) + ('"' + k.cmd + '"').slice(0, 26).padEnd(28) + k.status.padEnd(14) + k.ports.map(function (p) { return "0.0.0.0:" + p.replace(":", "->") + "/tcp" }).join(",").padEnd(24) + k.name + "\n") }); return 0 }
    if (sub == "stop" || sub == "kill") { var rc = 0; a.forEach(function (x) { var k = findC(x); if (!k) { c.err("Error response from daemon: No such container: " + x + "\n"); rc = 1; return } k.status = "Exited (0)"; c.out(x + "\n") }); return rc }
    if (sub == "start") { a.forEach(function (x) { var k = findC(x); if (k) { k.status = "Up"; c.out(x + "\n") } }); return 0 }
    if (sub == "rm") { var rc2 = 0; a.filter(function (x) { return x[0] != "-" }).forEach(function (x) { var k = findC(x); if (!k) { c.err("Error response from daemon: No such container: " + x + "\n"); rc2 = 1; return } if (k.status == "Up" && a.indexOf("-f") < 0) { c.err("Error response from daemon: cannot remove a running container. Stop the container before attempting removal or force remove\n"); rc2 = 1; return } D.containers.splice(D.containers.indexOf(k), 1); c.out(x + "\n") }); return rc2 }
    if (sub == "logs") { var k2 = findC(a[a.length - 1]); if (!k2) return fail(c, "Error response from daemon: No such container: " + a[a.length - 1], 1); c.out(k2.logs); return 0 }
    if (sub == "exec") { var k3 = findC(a[0]); if (!k3) return fail(c, "Error response from daemon: No such container: " + a[0], 1); if (k3.status != "Up") return fail(c, "Error response from daemon: container is not running", 1); c.out("(in " + k3.name + ") " + a.slice(1).join(" ") + "\n"); return 0 }
    if (sub == "inspect") { var k4 = findC(a[0]); if (!k4) return fail(c, "Error: No such object: " + a[0], 1); c.out(JSON.stringify({ Id: k4.full, Name: "/" + k4.name, Image: k4.image, State: { Status: k4.status == "Up" ? "running" : "exited" }, Ports: k4.ports }, null, 2) + "\n"); return 0 }
    return fail(c, "docker: '" + sub + "' is not supported in this sandbox", 1);
  };
  var curl0 = C["curl"];
  C["curl"] = async function (cc) { var u = cc.args.filter(function (x) { return x[0] != "-" }).pop() || "", m = /localhost:(\d+)/.exec(u); if (m) { var k = D.containers.filter(function (x) { return x.status == "Up" && x.ports.some(function (p) { return p.split(":")[0] == m[1] }) })[0]; if (k) { cc.out(k.web ? "<html><h1>Welcome to nginx!</h1></html>\n" : "Hello from " + k.name + "\n"); return 0 } var d = S.k8s.svcPorts[m[1]]; if (d) { cc.out("Hello from " + d + "\n"); return 0 } } return curl0(cc) };
  /* ================= kubectl ================= */
  S.k8s = { deploys: {}, svcs: {}, svcPorts: {}, n: 0 };
  var K = S.k8s, SUF = ["x7k2p", "9fq4d", "m2w8z", "c5t6r", "h3n1b", "j8v0s", "q4y9e", "u6l2a"];
  function mkPods(d, n) { var out = []; for (var i = 0; i < n; i++) out.push({ n: d.name + "-" + d.hash + "-" + SUF[(K.n++) % SUF.length], age: "1m" }); return out }
  function bad(img) { return /broken|bad|missing|nonexistent/.test(img) }
  function podStatus(d) { return bad(d.image) ? ["0/1", "ImagePullBackOff"] : ["1/1", "Running"] }
  C["kubectl"] = async function (c) {
    var a = c.args.slice(), sub = a.shift();
    if (sub == "version") { c.out("Client Version: v1.30 (sandbox simulator)\n"); return 0 }
    if (sub == "apply" || sub == "create") {
      var fi = a.indexOf("-f"); if (fi < 0) return fail(c, "error: must specify one of -f and -k", 1); var p = S.abs(a[fi + 1]); if (!v.exists(p)) return fail(c, "error: the path \"" + a[fi + 1] + "\" does not exist", 1);
      var docs = v.read(p).split(/^---\s*$/m); var rc = 0;
      docs.forEach(function (doc) { if (!doc.trim()) return; var kind = (/^kind:\s*(\S+)/m.exec(doc) || [])[1], name = (/metadata:\s*\n\s+name:\s*(\S+)/.exec(doc) || [])[1]; if (!kind || !name) { c.err("error: unable to recognize manifest: missing kind or metadata.name\n"); rc = 1; return }
        if (kind == "Deployment") { var rep = parseInt((/replicas:\s*(\d+)/.exec(doc) || [0, 1])[1]), img = (/image:\s*(\S+)/.exec(doc) || [])[1]; if (!img) { c.err("error: deployment spec.template.spec.containers[0].image is required\n"); rc = 1; return } var ex = K.deploys[name]; if (!ex) { var d = { name: name, replicas: rep, image: img, prev: null, hash: hex(10, name + img) }; d.pods = mkPods(d, rep); K.deploys[name] = d; c.out("deployment.apps/" + name + " created\n") } else if (ex.replicas == rep && ex.image == img) c.out("deployment.apps/" + name + " unchanged\n"); else { if (ex.image != img) { ex.prev = ex.image; ex.image = img; ex.hash = hex(10, name + img); ex.pods = mkPods(ex, rep) } ex.replicas = rep; while (ex.pods.length < rep) ex.pods.push(mkPods(ex, 1)[0]); ex.pods = ex.pods.slice(0, rep); c.out("deployment.apps/" + name + " configured\n") } }
        else if (kind == "Service") { var port = (/port:\s*(\d+)/.exec(doc) || [0, 80])[1], sel = (/app:\s*(\S+)/.exec(doc) || [])[1] || name; K.svcs[name] = { name: name, port: port, sel: sel, ip: "10.96." + (K.n % 200) + "." + (10 + Object.keys(K.svcs).length) }; K.svcPorts[port] = sel; c.out("service/" + name + " created\n") }
        else { c.out(kind.toLowerCase() + "/" + name + " created\n") } });
      return rc }
    if (sub == "get") { var what = (a[0] || "").replace(/s$/, "");
      if (what == "pod" || what == "po") { c.out("NAME".padEnd(32) + "READY".padEnd(8) + "STATUS".padEnd(18) + "RESTARTS  AGE\n"); Object.keys(K.deploys).forEach(function (n) { var d = K.deploys[n], st = podStatus(d); d.pods.forEach(function (pd) { c.out(pd.n.padEnd(32) + st[0].padEnd(8) + st[1].padEnd(18) + "0         " + pd.age + "\n") }) }); if (!Object.keys(K.deploys).length) c.err("No resources found in default namespace.\n"); return 0 }
      if (what == "deployment" || what == "deploy") { if (!Object.keys(K.deploys).length) { c.err("No resources found in default namespace.\n"); return 0 } c.out("NAME".padEnd(14) + "READY".padEnd(8) + "UP-TO-DATE".padEnd(12) + "AVAILABLE\n"); Object.keys(K.deploys).forEach(function (n) { var d = K.deploys[n], up = bad(d.image) ? 0 : d.replicas; c.out(n.padEnd(14) + (up + "/" + d.replicas).padEnd(8) + String(d.replicas).padEnd(12) + up + "\n") }); return 0 }
      if (what == "service" || what == "svc") { c.out("NAME".padEnd(14) + "TYPE".padEnd(12) + "CLUSTER-IP".padEnd(16) + "PORT(S)\n"); c.out("kubernetes".padEnd(14) + "ClusterIP".padEnd(12) + "10.96.0.1".padEnd(16) + "443/TCP\n"); Object.keys(K.svcs).forEach(function (n) { var s = K.svcs[n]; c.out(n.padEnd(14) + "ClusterIP".padEnd(12) + s.ip.padEnd(16) + s.port + "/TCP\n") }); return 0 }
      return fail(c, "error: the server doesn't have a resource type \"" + a[0] + "\"", 1) }
    if (sub == "scale") { var tgt = a.filter(function (x) { return x[0] != "-" }), nm = (tgt[0] || "").replace(/^deployments?\/|^deploy\//, "") || tgt[1]; if (/^deployments?$/.test(tgt[0])) nm = tgt[1]; var ri = a.filter(function (x) { return /^--replicas=/.test(x) })[0]; if (!ri) return fail(c, "error: required flag(s) \"replicas\" not set", 1); var d2 = K.deploys[nm]; if (!d2) return fail(c, "Error from server (NotFound): deployments.apps \"" + nm + "\" not found", 1); var n = parseInt(ri.split("=")[1]); d2.replicas = n; while (d2.pods.length < n) d2.pods.push(Object.assign(mkPods(d2, 1)[0], { age: "2s" })); d2.pods = d2.pods.slice(0, n); c.out("deployment.apps/" + nm + " scaled\n"); return 0 }
    if (sub == "delete") { var kind2 = (a[0] || "").replace(/s$/, ""), nm2 = a[1]; if (kind2.indexOf("/") > 0) { nm2 = kind2.split("/")[1]; kind2 = kind2.split("/")[0] } if (kind2 == "deployment" || kind2 == "deploy") { if (!K.deploys[nm2]) return fail(c, "Error from server (NotFound): deployments.apps \"" + nm2 + "\" not found", 1); delete K.deploys[nm2]; c.out("deployment.apps \"" + nm2 + "\" deleted\n"); return 0 } if (kind2 == "pod" || kind2 == "po") { var found = false; Object.keys(K.deploys).forEach(function (n) { var d = K.deploys[n]; var i = d.pods.findIndex(function (pd) { return pd.n == nm2 }); if (i >= 0) { found = true; d.pods.splice(i, 1, Object.assign(mkPods(d, 1)[0], { age: "3s" })) } }); if (!found) return fail(c, "Error from server (NotFound): pods \"" + nm2 + "\" not found", 1); c.out("pod \"" + nm2 + "\" deleted\n"); return 0 } if (kind2 == "service" || kind2 == "svc") { delete K.svcs[nm2]; c.out("service \"" + nm2 + "\" deleted\n"); return 0 } return fail(c, "error: unsupported resource", 1) }
    if (sub == "set" && a[0] == "image") { var dn = (a[1] || "").replace(/^deployments?\//, ""), d3 = K.deploys[dn], im = (a[2] || "").split("=")[1]; if (!d3) return fail(c, "Error from server (NotFound): deployments.apps \"" + dn + "\" not found", 1); d3.prev = d3.image; d3.image = im; d3.hash = hex(10, dn + im); d3.pods = mkPods(d3, d3.replicas); c.out("deployment.apps/" + dn + " image updated\n"); return 0 }
    if (sub == "rollout") { var dn2 = (a[1] || "").replace(/^deployments?\//, ""), d4 = K.deploys[dn2]; if (!d4) return fail(c, "Error from server (NotFound): deployments.apps \"" + dn2 + "\" not found", 1); if (a[0] == "undo") { if (!d4.prev) return fail(c, "error: no rollout history found", 1); var t = d4.image; d4.image = d4.prev; d4.prev = t; d4.hash = hex(10, dn2 + d4.image); d4.pods = mkPods(d4, d4.replicas); c.out("deployment.apps/" + dn2 + " rolled back\n"); return 0 } if (a[0] == "status") { if (bad(d4.image)) { c.out("Waiting for deployment \"" + dn2 + "\" rollout to finish: 0 of " + d4.replicas + " updated replicas are available...\n"); return 1 } c.out("deployment \"" + dn2 + "\" successfully rolled out\n"); return 0 } }
    if (sub == "describe" || sub == "logs") { var pn = a[a.length - 1], dd = null; Object.keys(K.deploys).forEach(function (n) { K.deploys[n].pods.forEach(function (pd) { if (pd.n == pn) dd = K.deploys[n] }) }); if (!dd) return fail(c, "Error from server (NotFound): pods \"" + pn + "\" not found", 1); if (sub == "logs") { if (bad(dd.image)) return fail(c, "Error from server (BadRequest): container is waiting to start: trying and failing to pull image", 1); c.out("Listening on port 80\n"); return 0 } c.out("Name:         " + pn + "\nImage:        " + dd.image + "\nStatus:       " + podStatus(dd)[1] + "\nEvents:\n" + (bad(dd.image) ? "  Warning  Failed  Failed to pull image \"" + dd.image + "\": not found\n" : "  Normal   Started  Started container\n")); return 0 }
    return fail(c, "kubectl: '" + (sub || "") + "' is not supported in this sandbox", 1);
  };
  /* ================= iac ================= */
  function parseInfra(txt) { var m = {}; txt.split("\n").forEach(function (l) { l = l.trim(); if (!l || l[0] == "#") return; var p = l.split(/\s+/); m[p[0] + "." + p[1]] = p.slice(2).join(" ") }); return m }
  C["iac"] = async function (c) {
    var sub = c.args[0], f = S.abs("infra.txt"), st = S.abs(".iac-state");
    if (!v.exists(f)) return fail(c, "Error: no configuration found (infra.txt)", 1);
    var want = parseInfra(v.read(f)), have = v.exists(st) ? JSON.parse(v.read(st)) : {}, add = [], chg = [], del = [];
    Object.keys(want).forEach(function (k) { if (!(k in have)) add.push(k); else if (have[k] != want[k]) chg.push(k) }); Object.keys(have).forEach(function (k) { if (!(k in want)) del.push(k) });
    if (sub == "plan" || sub == "apply") {
      if (!add.length && !chg.length && !del.length) { c.out("No changes. Infrastructure matches the configuration.\n"); return 0 }
      add.forEach(function (k) { c.out("  + " + k + " (" + want[k] + ")\n") }); chg.forEach(function (k) { c.out("  ~ " + k + " (" + have[k] + " -> " + want[k] + ")\n") }); del.forEach(function (k) { c.out("  - " + k + " (" + have[k] + ")\n") });
      c.out("Plan: " + add.length + " to add, " + chg.length + " to change, " + del.length + " to destroy.\n");
      if (sub == "apply") { S.writeFile(st, JSON.stringify(want)); c.out("Apply complete! Resources: " + add.length + " added, " + chg.length + " changed, " + del.length + " destroyed.\n") } return 0 }
    if (sub == "state") { Object.keys(have).sort().forEach(function (k) { c.out(k + "\n") }); return 0 }
    return fail(c, "usage: iac plan | apply | state", 1) };
  /* ================= ci and make ================= */
  S.ci = { runs: 0, last: null };
  C["ci"] = async function (c) {
    var f = S.abs("pipeline.txt"); if (!v.exists(f)) return fail(c, "ci: no pipeline.txt in this directory", 1);
    var stages = v.read(f).split("\n").map(function (l) { return l.trim() }).filter(function (l) { return l && l[0] != "#" }).map(function (l) { var i = l.indexOf(":"); return { name: l.slice(0, i).trim(), cmd: l.slice(i + 1).trim() } });
    var res = { passed: [], failed: null, skipped: [] }; S.ci.runs++;
    for (var i = 0; i < stages.length; i++) { var s = stages[i]; if (res.failed) { res.skipped.push(s.name); c.out("- " + s.name + ": skipped\n"); continue } c.out("== stage: " + s.name + " ==\n"); var code; try { code = await S.execList(S.parse(s.cmd), { stdin: "", out: c.out, err: c.out }) } catch (e) { code = 1 } if (code === 0) { res.passed.push(s.name); c.out("PASS " + s.name + "\n") } else { res.failed = s.name; c.out("FAIL " + s.name + " (exit " + code + ")\n") } }
    S.ci.last = res; c.out(res.failed ? "Pipeline failed at " + res.failed + "\n" : "Pipeline passed\n"); return res.failed ? 1 : 0 };
  C["make"] = async function (c) {
    var f = S.abs("Makefile"); if (!v.exists(f)) return fail(c, "make: *** No targets specified and no makefile found.  Stop.", 2);
    var rules = {}, cur = null, first = null; v.read(f).split("\n").forEach(function (l) { if (/^\t/.test(l) && cur) rules[cur].cmds.push(l.trim()); else { var m = /^([A-Za-z0-9_.-]+)\s*:\s*(.*)$/.exec(l); if (m) { cur = m[1]; rules[cur] = { deps: m[2].split(/\s+/).filter(Boolean), cmds: [] }; if (!first) first = cur } } });
    var done = {}; async function build(t) { if (done[t]) return 0; if (!rules[t]) { if (v.exists(S.abs(t))) return 0; c.err("make: *** No rule to make target '" + t + "'.  Stop.\n"); return 2 } done[t] = 1; for (var i = 0; i < rules[t].deps.length; i++) { var r = await build(rules[t].deps[i]); if (r) return r } for (var j = 0; j < rules[t].cmds.length; j++) { c.out(rules[t].cmds[j] + "\n"); var code = await S.execList(S.parse(rules[t].cmds[j].replace(/^@/, "")), { stdin: "", out: c.out, err: c.err }); if (code) { c.err("make: *** [Makefile:" + t + "] Error " + code + "\n"); return 2 } } return 0 }
    var targets = c.args.length ? c.args : [first]; for (var k = 0; k < targets.length; k++) { var r2 = await build(targets[k]); if (r2) return r2 } return 0 };
}
