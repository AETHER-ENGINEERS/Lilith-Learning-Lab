/* LinuxSim: a small Linux-like shell on top of the Jade Agent Kit VFS and BusyBox (for grep, sed, awk, sort and friends). Original code. */
function LinuxSim(kit, cfg) {
  cfg = cfg || {};
  var S = this;
  S.kit = kit; S.vfs = kit.vfs; S.bb = kit.busybox;
  S.meta = {}; S.cwd = cfg.cwd || "/home/user"; S.user = cfg.user || "user"; S.vars = {}; S.exported = {}; S.funcs = {}; S.aliases = {}; S.hist = []; S.allout = ""; S.umask = 0o022;
  S.users = cfg.users || { root: { uid: 0, gid: 0, home: "/root", groups: ["root"] }, user: { uid: 1000, gid: 1000, home: "/home/user", groups: ["user", "sudo"] }, alice: { uid: 1001, gid: 1001, home: "/home/alice", groups: ["alice", "dev"] }, bob: { uid: 1002, gid: 1002, home: "/home/bob", groups: ["bob", "dev"] } };
  S.procs = [{ pid: 1, user: "root", cmd: "/sbin/init", state: "S", cpu: 0.0, mem: 0.3 }, { pid: 412, user: "root", cmd: "/usr/sbin/sshd -D", state: "S", cpu: 0.0, mem: 0.4 }, { pid: 530, user: "root", cmd: "/usr/sbin/cron -f", state: "S", cpu: 0.0, mem: 0.1 }, { pid: 701, user: "user", cmd: "-bash", state: "S", cpu: 0.0, mem: 0.2 }];
  S.nextPid = 1200; S.services = cfg.services || { ssh: { active: true, enabled: true }, cron: { active: true, enabled: true }, nginx: { active: false, enabled: false, installed: false } };
  S.pkgs = cfg.pkgs || { installed: { bash: 1, coreutils: 1, openssh: 1 }, available: { tree: "prints a directory tree", htop: "interactive process viewer", nginx: "web server", cowsay: "a talking cow", curl: "transfers data with URLs", git: "distributed version control", jq: "command-line JSON processor", vim: "text editor" } };
  S.ext = {};
  S.setup = function () {
    var v = S.vfs;
    ["/bin", "/etc", "/home/user", "/home/alice", "/home/bob", "/root", "/tmp", "/usr/bin", "/usr/local/bin", "/var/log", "/var/www/html", "/opt", "/dev", "/proc", "/srv"].forEach(function (d) { if (!v.exists(d)) v.mkdirp(d); S.setMeta(d, { mode: 0o755, owner: "root", group: "root" }); });
    S.setMeta("/home/user", { mode: 0o755, owner: "user", group: "user" }); S.setMeta("/home/alice", { mode: 0o750, owner: "alice", group: "alice" }); S.setMeta("/home/bob", { mode: 0o750, owner: "bob", group: "bob" }); S.setMeta("/root", { mode: 0o700, owner: "root", group: "root" }); S.setMeta("/tmp", { mode: 0o1777, owner: "root", group: "root" });
    var f = function (p, c, m, o, g) { if (!v.exists(p)) v.write(p, c); S.setMeta(p, { mode: m, owner: o || "root", group: g || o || "root" }); };
    f("/etc/passwd", "root:x:0:0:root:/root:/bin/bash\nuser:x:1000:1000:User:/home/user:/bin/bash\nalice:x:1001:1001:Alice:/home/alice:/bin/bash\nbob:x:1002:1002:Bob:/home/bob:/bin/bash\n", 0o644);
    f("/etc/group", "root:x:0:\nsudo:x:27:user\nuser:x:1000:\nalice:x:1001:\nbob:x:1002:\ndev:x:2000:alice,bob\n", 0o644);
    f("/etc/shadow", "root:!:19000:0:99999:7:::\nuser:!:19000:0:99999:7:::\n", 0o640, "root", "shadow");
    f("/etc/hostname", "lilith\n", 0o644); f("/etc/os-release", 'NAME="Lilith Linux"\nVERSION="1.0"\nID=lilith\nPRETTY_NAME="Lilith Linux 1.0"\n', 0o644);
    f("/etc/hosts", "127.0.0.1 localhost\n127.0.1.1 lilith\n", 0o644); f("/etc/fstab", "# <file system> <mount point> <type> <options> <dump> <pass>\n/dev/sda1 / ext4 defaults 0 1\n/dev/sda2 none swap sw 0 0\n", 0o644);
    f("/etc/crontab", "# m h dom mon dow user command\n17 * * * * root cd / && run-parts /etc/cron.hourly\n", 0o644);
    if (cfg.files) Object.keys(cfg.files).forEach(function (p) { var o = cfg.files[p]; if (typeof o == "string") o = { c: o }; if (!v.exists(p) || o.force !== false) { v.write(p, o.c); } var own = o.owner || (p.indexOf("/home/user") == 0 || p.indexOf("/tmp") == 0 ? "user" : "root"); S.setMeta(p, { mode: o.mode != null ? o.mode : 0o644, owner: own, group: o.group || own }); if (o.exec) S.setMeta(p, { mode: 0o755, owner: own, group: o.group || own }); });
    S.vars.HOME = S.users[S.user].home; S.vars.USER = S.user; S.vars.PATH = "/usr/local/bin:/usr/bin:/bin"; S.vars.SHELL = "/bin/bash"; S.vars.PWD = S.cwd; S.vars.HOSTNAME = "lilith"; S.vars.LANG = "en_US.UTF-8"; S.vars.OLDPWD = S.cwd;
    ["HOME", "USER", "PATH", "SHELL", "PWD", "HOSTNAME", "LANG", "OLDPWD"].forEach(function (k) { S.exported[k] = 1 });
  };
  /* ---- paths and metadata ---- */
  S.abs = function (p) { if (p === undefined || p === "") return S.cwd; if (p[0] == "~") p = S.users[S.user].home + p.slice(1); if (p[0] != "/") p = S.cwd + "/" + p; var out = []; p.split("/").forEach(function (x) { if (!x || x == ".") return; if (x == "..") out.pop(); else out.push(x) }); return "/" + out.join("/") };
  S.dir = function (p) { var i = p.lastIndexOf("/"); return i <= 0 ? "/" : p.slice(0, i) };
  S.base = function (p) { return p.slice(p.lastIndexOf("/") + 1) };
  S.getMeta = function (p) { var m = S.meta[p]; if (m) return m; return { mode: S.vfs.isDir(p) ? 0o755 : 0o644, owner: "user", group: "user" } };
  S.setMeta = function (p, m) { S.meta[p] = { mode: m.mode, owner: m.owner, group: m.group } };
  S.isRoot = function () { return S.user == "root" };
  S.groupsOf = function (u) { return (S.users[u] || { groups: [] }).groups };
  S.can = function (p, bit, user) { user = user || S.user; if (user == "root") return true; var m = S.getMeta(p), mode = m.mode & 0o777, sh; if (m.owner == user) sh = (mode >> 6) & 7; else if (S.groupsOf(user).indexOf(m.group) >= 0) sh = (mode >> 3) & 7; else sh = mode & 7; return (sh & bit) != 0 };
  S.create = function (p, dir) { var m = dir ? 0o777 & ~S.umask : 0o666 & ~S.umask; S.setMeta(p, { mode: m, owner: S.user, group: S.users[S.user].groups[0] }) };
  S.modeStr = function (p) { var m = S.getMeta(p), mode = m.mode, d = S.vfs.isDir(p), s = d ? "d" : (S.meta[p] && S.meta[p].link ? "l" : "-"); for (var i = 2; i >= 0; i--) { var b = (mode >> (i * 3)) & 7; s += (b & 4 ? "r" : "-") + (b & 2 ? "w" : "-") + (b & 1 ? "x" : "-") } if (mode & 0o4000) s = s.slice(0, 3) + (s[3] == "x" ? "s" : "S") + s.slice(4); if (mode & 0o1000) s = s.slice(0, 9) + (s[9] == "x" ? "t" : "T"); return s };
  S.expect = function (c, p, bit, what) { if (!S.can(p, bit)) { c.err(what + ": " + (c.shown || p) + ": Permission denied\n"); return false } return true };
  S.readFile = function (p) { return S.vfs.read(p) };
  S.writeFile = function (p, data, append) { var ex = S.vfs.exists(p); if (append && ex) data = S.vfs.read(p) + data; S.vfs.write(p, data); if (!ex) S.create(p, false) };
  /* ---- tokenizer ---- */
  var KW = { "if": 1, "then": 1, "elif": 1, "else": 1, "fi": 1, "for": 1, "while": 1, "until": 1, "do": 1, "done": 1, "case": 1, "esac": 1, "in": 1, "{": 1, "}": 1, "!": 1, "function": 1 };
  function tokenize(src) {
    var t = [], i = 0, n = src.length;
    function push(x) { t.push(x) }
    while (i < n) {
      var c = src[i];
      if (c == " " || c == "\t") { i++; continue }
      if (c == "\\" && src[i + 1] == "\n") { i += 2; continue }
      if (c == "#") { while (i < n && src[i] != "\n") i++; continue }
      if (c == "\n") { push({ k: "nl" }); i++; continue }
      var two = src.substr(i, 2), three = src.substr(i, 3);
      if (three == "2>>") { push({ k: "op", v: "2>>" }); i += 3; continue }
      if (two == "2>" && src[i + 2] == "&" && src[i + 3] == "1") { push({ k: "op", v: "2>&1" }); i += 4; continue }
      if (two == "2>") { push({ k: "op", v: "2>" }); i += 2; continue }
      if (two == "&>") { push({ k: "op", v: "&>" }); i += 2; continue }
      if (two == "&&" || two == "||" || two == ">>" || two == ";;") { push({ k: "op", v: two }); i += 2; continue }
      if (c == "|" || c == ";" || c == "&" || c == ">" || c == "<" || c == "(" || c == ")") { push({ k: "op", v: c }); i++; continue }
      var w = "", q = null;
      while (i < n) {
        c = src[i];
        if (q) { w += c; if (c == q) q = null; else if (c == "\\" && q == '"' && i + 1 < n) { w += src[i + 1]; i++ } i++; continue }
        if (c == "'" || c == '"') { q = c; w += c; i++; continue }
        if (c == "\\" && i + 1 < n) { w += c + src[i + 1]; i += 2; continue }
        if (c == "$" && src[i + 1] == "(") { var d = 0, j = i; while (j < n) { if (src[j] == "(") d++; else if (src[j] == ")") { d--; if (d == 0) break } j++ } w += src.slice(i, j + 1); i = j + 1; continue }
        if (c == "`") { var j2 = src.indexOf("`", i + 1); if (j2 < 0) j2 = n - 1; w += src.slice(i, j2 + 1); i = j2 + 1; continue }
        if (c == "$" && src[i + 1] == "{") { var j3 = src.indexOf("}", i); if (j3 < 0) j3 = n - 1; w += src.slice(i, j3 + 1); i = j3 + 1; continue }
        if (" \t\n|&;<>()".indexOf(c) >= 0) break;
        if (c == "#" && w == "") break;
        w += c; i++;
      }
      if (q) throw new Error("unexpected EOF while looking for matching `" + q + "'");
      if (w !== "") push({ k: "w", v: w });
    }
    return t;
  }
  /* ---- parser ---- */
  function Parser(toks) { this.t = toks; this.i = 0 }
  Parser.prototype = {
    peek: function () { return this.t[this.i] }, next: function () { return this.t[this.i++] },
    isW: function (v) { var x = this.peek(); return x && x.k == "w" && x.v == v },
    isOp: function (v) { var x = this.peek(); return x && x.k == "op" && x.v == v },
    skipNl: function () { while (this.peek() && (this.peek().k == "nl" || this.isOp(";"))) this.i++ },
    parseList: function (stops) { var items = []; this.skipNl(); while (this.peek()) { if (this.peek().k == "w" && stops && stops.indexOf(this.peek().v) >= 0) break; if (this.isOp(")") || this.isOp(";;")) break; var a = this.parseAndOr(); var bg = false; if (this.isOp("&")) { this.i++; bg = true } items.push({ n: a, bg: bg }); this.skipNl() } return { type: "list", items: items } },
    parseAndOr: function () { var left = this.parsePipe(), parts = [left], ops = []; while (this.isOp("&&") || this.isOp("||")) { ops.push(this.next().v); this.skipNl(); parts.push(this.parsePipe()) } return { type: "andor", parts: parts, ops: ops } },
    parsePipe: function () { var neg = false; if (this.isW("!")) { this.i++; neg = true } var cmds = [this.parseCmd()]; while (this.isOp("|")) { this.i++; this.skipNl(); cmds.push(this.parseCmd()) } return { type: "pipe", cmds: cmds, neg: neg } },
    expectW: function (v) { this.skipNl(); if (!this.isW(v)) throw new Error("syntax error: expected `" + v + "'"); this.i++ },
    parseCmd: function () {
      var x = this.peek(); if (!x) throw new Error("syntax error: unexpected end");
      if (x.k == "w") {
        if (x.v == "if") { this.i++; var cond = this.parseList(["then"]); this.expectW("then"); var body = this.parseList(["elif", "else", "fi"]); var node = { type: "if", cond: cond, body: body, els: null }, cur = node; while (this.isW("elif")) { this.i++; var c2 = this.parseList(["then"]); this.expectW("then"); var b2 = this.parseList(["elif", "else", "fi"]); var n2 = { type: "if", cond: c2, body: b2, els: null }; cur.els = n2; cur = n2 } if (this.isW("else")) { this.i++; cur.els = this.parseList(["fi"]) } this.expectW("fi"); return this.redirs(node) }
        if (x.v == "while" || x.v == "until") { this.i++; var cd = this.parseList(["do"]); this.expectW("do"); var bd = this.parseList(["done"]); this.expectW("done"); return this.redirs({ type: "while", until: x.v == "until", cond: cd, body: bd }) }
        if (x.v == "for") { this.i++; var name = this.next().v; var words = null; this.skipNl(); if (this.isW("in")) { this.i++; words = []; while (this.peek() && this.peek().k == "w") words.push(this.next().v) } this.skipNl(); this.expectW("do"); var fb = this.parseList(["done"]); this.expectW("done"); return this.redirs({ type: "for", name: name, words: words, body: fb }) }
        if (x.v == "case") { this.i++; var subj = this.next().v; this.skipNl(); this.expectW("in"); var cases = []; this.skipNl(); while (!this.isW("esac")) { if (this.isOp("(")) this.i++; var pats = []; while (true) { pats.push(this.next().v); if (this.isOp("|")) this.i++; else break } if (this.isOp(")")) this.i++; var cb = this.parseList(["esac"]); if (this.isOp(";;")) this.i++; this.skipNl(); cases.push({ pats: pats, body: cb }) } this.expectW("esac"); return { type: "case", subj: subj, cases: cases } }
        if (x.v == "{") { this.i++; var gb = this.parseList(["}"]); this.expectW("}"); return this.redirs({ type: "group", body: gb }) }
        if (x.v == "function") { this.i++; var fname = this.next().v; if (this.isOp("(")) { this.i++; this.i++ } this.skipNl(); return { type: "func", name: fname, body: this.parseCmd() } }
        var nx = this.t[this.i + 1], nx2 = this.t[this.i + 2];
        if (nx && nx.k == "op" && nx.v == "(" && nx2 && nx2.k == "op" && nx2.v == ")" && !KW[x.v]) { this.i += 3; this.skipNl(); return { type: "func", name: x.v, body: this.parseCmd() } }
      }
      if (x.k == "op" && x.v == "(") { this.i++; var sb = this.parseList([]); if (!this.isOp(")")) throw new Error("syntax error: missing )"); this.i++; return { type: "subshell", body: sb } }
      return this.parseSimple();
    },
    redirs: function (node) { node.redirs = []; while (this.peek() && this.peek().k == "op" && [">", ">>", "<", "2>", "2>>", "2>&1", "&>"].indexOf(this.peek().v) >= 0) { var op = this.next().v; var tgt = op == "2>&1" ? null : this.next().v; node.redirs.push({ op: op, tgt: tgt }) } return node },
    parseSimple: function () { var words = [], redirs = [], assigns = []; while (this.peek()) { var x = this.peek(); if (x.k == "w") { if (!words.length && /^[A-Za-z_][A-Za-z0-9_]*=/.test(x.v)) { assigns.push(x.v); this.i++; continue } if (!words.length && KW[x.v] && ["then", "elif", "else", "fi", "do", "done", "esac", "}"].indexOf(x.v) >= 0) break; words.push(x.v); this.i++; continue } if (x.k == "op" && [">", ">>", "<", "2>", "2>>", "2>&1", "&>"].indexOf(x.v) >= 0) { this.i++; var tgt = x.v == "2>&1" ? null : this.next().v; redirs.push({ op: x.v, tgt: tgt }); continue } break } if (!words.length && !assigns.length && !redirs.length) throw new Error("syntax error near unexpected token"); return { type: "simple", words: words, redirs: redirs, assigns: assigns } }
  };
  S.parse = function (src) { var p = new Parser(tokenize(src)); var l = p.parseList([]); if (p.peek()) throw new Error("syntax error near unexpected token `" + (p.peek().v || "newline") + "'"); return l };
  /* ---- expansion ---- */
  S.pos = [""]; S.lastCode = 0;
  S.getVar = function (n) { if (n == "?") return String(S.lastCode); if (n == "#") return String(S.pos.length - 1); if (n == "@" || n == "*") return S.pos.slice(1).join(" "); if (/^\d+$/.test(n)) return S.pos[+n] === undefined ? "" : S.pos[+n]; if (n == "$") return "701"; if (n == "RANDOM") return String(Math.floor(Math.random() * 32768)); var v = S.vars[n]; return v === undefined ? "" : v };
  S.arith = function (e) { e = e.replace(/\$?([A-Za-z_][A-Za-z0-9_]*)/g, function (m, n) { var v = S.getVar(n); return /^-?\d+$/.test(v) ? "(" + v + ")" : "0" }); if (!/^[\d\s+\-*/%()<>=!&|^~.?:]+$/.test(e)) throw new Error("arithmetic syntax error"); try { var r = Function("return (" + e + ")")(); if (typeof r == "boolean") r = r ? 1 : 0; return String(Math.trunc(r)) } catch (x) { throw new Error("arithmetic syntax error") } };
  S.expand = async function (raw, noSplit) {
    var fields = [], cur = "", curHas = false, i = 0, n = raw.length, glob = false, any = false;
    function flush() { if (curHas) { fields.push({ s: cur, g: glob }); } cur = ""; curHas = false; glob = false }
    async function sub(cmd) { var r = await S.runCapture(cmd); return r.replace(/\n+$/, "") }
    while (i < n) {
      var c = raw[i];
      if (c == "'") { var j = raw.indexOf("'", i + 1); cur += raw.slice(i + 1, j); curHas = true; i = j + 1; continue }
      if (c == '"') {
        i++; curHas = true;
        while (i < n && raw[i] != '"') {
          var d = raw[i];
          if (d == "\\" && i + 1 < n && '$`"\\'.indexOf(raw[i + 1]) >= 0) { cur += raw[i + 1]; i += 2; continue }
          if (d == "$" || d == "`") { var r = await S.dollar(raw, i, sub); cur += r.val; i = r.i; continue }
          cur += d; i++;
        }
        i++; continue;
      }
      if (c == "\\") { cur += raw[i + 1] === undefined ? "\\" : raw[i + 1]; curHas = true; i += 2; continue }
      if (c == "$" || c == "`") { var r2 = await S.dollar(raw, i, sub); if (noSplit) { cur += r2.val; curHas = true } else { var parts = r2.val.split(/[ \t\n]+/); if (parts.length == 1 && parts[0] === "") { if (r2.val !== "" || r2.quotedEmpty) { } } else { parts.forEach(function (p, k) { if (k > 0) flush(); if (p !== "" ) { cur += p; curHas = true } else if (k == 0 && parts.length > 1) { } }) } } i = r2.i; continue }
      if (c == "~" && i == 0 && (n == 1 || raw[1] == "/")) { cur += S.users[S.user].home; curHas = true; i++; continue }
      if ("*?[".indexOf(c) >= 0) glob = true;
      cur += c; curHas = true; i++;
    }
    flush();
    var out = [];
    fields.forEach(function (f) { if (f.g && !noSplit) { var m = S.globMatch(f.s); if (m.length) { out = out.concat(m); return } } out.push(f.s) });
    return out;
  };
  S.dollar = async function (raw, i, sub) {
    var c = raw[i];
    if (c == "`") { var j = raw.indexOf("`", i + 1); return { val: await sub(raw.slice(i + 1, j)), i: j + 1 } }
    var nx = raw[i + 1];
    if (nx == "(" && raw[i + 2] == "(") { var d = 0, j2 = i + 1; for (; j2 < raw.length; j2++) { if (raw[j2] == "(") d++; else if (raw[j2] == ")") { d--; if (d == 0) break } } var inner = raw.slice(i + 3, j2 - 1); var ex = await S.expand(inner, true); return { val: S.arith(ex.join("")), i: j2 + 1 } }
    if (nx == "(") { var d2 = 0, j3 = i + 1; for (; j3 < raw.length; j3++) { if (raw[j3] == "(") d2++; else if (raw[j3] == ")") { d2--; if (d2 == 0) break } } return { val: await sub(raw.slice(i + 2, j3)), i: j3 + 1 } }
    if (nx == "{") { var j4 = raw.indexOf("}", i), body = raw.slice(i + 2, j4), m;
      if (body[0] == "#") return { val: String(S.getVar(body.slice(1)).length), i: j4 + 1 };
      if (m = /^([A-Za-z_0-9@*#?]+):?([-=+?])(.*)$/.exec(body)) { var v = S.getVar(m[1]), colon = body.indexOf(":") > 0; var unset = colon ? v === "" : S.vars[m[1]] === undefined && !/^\d+$/.test(m[1]); var def = (await S.expand(m[3], true)).join(""); if (m[2] == "-") return { val: unset ? def : v, i: j4 + 1 }; if (m[2] == "=") { if (unset) S.vars[m[1]] = def; return { val: unset ? def : v, i: j4 + 1 } } if (m[2] == "+") return { val: unset ? "" : def, i: j4 + 1 }; return { val: v, i: j4 + 1 } }
      if (m = /^([A-Za-z_0-9]+)([#%]{1,2})(.*)$/.exec(body)) { var vv = S.getVar(m[1]), pat = (await S.expand(m[3], true)).join(""), re = new RegExp((m[2][0] == "#" ? "^" : "") + S.globRe(pat, m[2].length == 2, m[2][0] == "%") + (m[2][0] == "%" ? "$" : "")); if (m[2][0] == "#") { var mm = vv.match(new RegExp("^" + S.globRe(pat, m[2].length == 2, false))); return { val: mm ? vv.slice(mm[0].length) : vv, i: j4 + 1 } } var k; if (m[2].length == 2) { for (k = 0; k <= vv.length; k++) if (new RegExp("^" + S.globRe(pat, true, false) + "$").test(vv.slice(k))) return { val: vv.slice(0, k), i: j4 + 1 } } else { for (k = vv.length; k >= 0; k--) if (new RegExp("^" + S.globRe(pat, false, false) + "$").test(vv.slice(k))) return { val: vv.slice(0, k), i: j4 + 1 } } return { val: vv, i: j4 + 1 } }
      return { val: S.getVar(body), i: j4 + 1 } }
    var m2 = /^[A-Za-z_][A-Za-z0-9_]*|^[0-9?#@*$]/.exec(raw.slice(i + 1));
    if (!m2) return { val: "$", i: i + 1 };
    return { val: S.getVar(m2[0]), i: i + 1 + m2[0].length };
  };
  S.globRe = function (g, greedy, tail) { var r = ""; for (var i = 0; i < g.length; i++) { var c = g[i]; if (c == "*") r += ".*"; else if (c == "?") r += "."; else if (c == "[") { var j = g.indexOf("]", i + 1); if (j < 0) r += "\\["; else { r += "[" + g.slice(i + 1, j).replace(/^!/, "^") + "]"; i = j } } else r += c.replace(/[.+^${}()|\\]/g, "\\$&") } return r };
  S.globMatch = function (pat) {
    var abs = pat[0] == "/", parts = pat.split("/").filter(function (x, i) { return x !== "" || i == 0 && false }), cur = [abs ? "/" : S.cwd];
    parts.forEach(function (seg, idx) { var next = []; cur.forEach(function (base) { if (!/[*?\[]/.test(seg)) { var p = (base == "/" ? "" : base) + "/" + seg; if (S.vfs.exists(p)) next.push(p); return } var re = new RegExp("^" + S.globRe(seg) + "$"); if (!S.vfs.isDir(base)) return; S.vfs.list(base).forEach(function (nm) { nm = nm.replace(/\/$/, ""); if (nm[0] == "." && seg[0] != ".") return; if (re.test(nm)) next.push((base == "/" ? "" : base) + "/" + nm) }) }); cur = next });
    cur = cur.sort().map(function (p) { return abs ? p : p.slice(S.cwd == "/" ? 1 : S.cwd.length + 1) });
    return cur;
  };
  /* ---- execution ---- */
  function Ctl(t, v) { this.t = t; this.v = v }
  S.runCapture = async function (cmd) { var buf = ""; var saveOut = S._out; var r = await S.execList(S.parse(cmd), { stdin: "", out: function (s) { buf += s }, err: function (s) { S._cerr(s) } }); return buf };
  S._cerr = function (s) { S._errSink && S._errSink(s) };
  S.execList = async function (list, io) { var code = 0; for (var i = 0; i < list.items.length; i++) { var it = list.items[i]; if (it.bg) { var pid = S.nextPid++; var cmdtxt = it.n.parts[0].cmds[0].words ? it.n.parts[0].cmds[0].words.join(" ") : "job"; S.procs.push({ pid: pid, user: S.user, cmd: cmdtxt, state: "S", cpu: 0.0, mem: 0.1, bg: true }); S.lastBg = pid; io.err("[" + (S.procs.filter(function (p) { return p.bg }).length) + "] " + pid + "\n"); code = 0; continue } code = await S.execAndOr(it.n, io); S.lastCode = code; if (S.errexit && code != 0 && !S._inCond) throw new Ctl("exit", code) } return code };
  S.execAndOr = async function (n, io) { var code = await S.execPipe(n.parts[0], io); S.lastCode = code; for (var i = 0; i < n.ops.length; i++) { if (n.ops[i] == "&&" && code != 0) continue; if (n.ops[i] == "||" && code == 0) continue; code = await S.execPipe(n.parts[i + 1], io); S.lastCode = code } return code };
  S.execPipe = async function (p, io) {
    if (p.cmds.length == 1) { var c1 = await S.execCmd(p.cmds[0], io); return p.neg ? (c1 ? 0 : 1) : c1 }
    var data = io.stdin, code = 0;
    for (var i = 0; i < p.cmds.length; i++) {
      var last = i == p.cmds.length - 1, buf = "";
      var sub = { stdin: data, out: last ? io.out : function (s) { buf += s }, err: io.err };
      code = await S.execCmd(p.cmds[i], sub);
      if (!last) data = buf;
    }
    return p.neg ? (code ? 0 : 1) : code;
  };
  S.withRedirs = async function (node, io, fn) {
    var out = io.out, err = io.err, stdin = io.stdin, files = [], errToOut = false, bufOut = "", bufErr = "", haveOut = false, haveErr = false;
    var rs = node.redirs || [], hasIn = false;
    for (var i = 0; i < rs.length; i++) {
      var r = rs[i];
      if (r.op == "2>&1") { errToOut = true; continue }
      var tgt = (await S.expand(r.tgt, true)).join(""), p = S.abs(tgt);
      if (r.op == "<") { if (!S.vfs.exists(p)) { io.err("bash: " + tgt + ": No such file or directory\n"); return 1 } if (!S.can(p, 4)) { io.err("bash: " + tgt + ": Permission denied\n"); return 1 } stdin = S.vfs.read(p); hasIn = true; continue }
      var append = r.op == ">>" || r.op == "2>>";
      if (p == "/dev/null") { if (r.op[0] == "2") { haveErr = true; files.push({ p: null, e: 1 }) } else { haveOut = true; files.push({ p: null }) } continue }
      var ex = S.vfs.exists(p);
      if (ex && !S.can(p, 2) || !ex && !S.can(S.dir(p), 2)) { io.err("bash: " + tgt + ": Permission denied\n"); return 1 }
      if (!S.vfs.exists(S.dir(p))) { io.err("bash: " + tgt + ": No such file or directory\n"); return 1 }
      if (S.vfs.isDir(p)) { io.err("bash: " + tgt + ": Is a directory\n"); return 1 }
      if (r.op[0] == "2") { haveErr = true; files.push({ p: p, a: append, e: 1 }) } else if (r.op == "&>") { haveOut = true; haveErr = true; errToOut = true; files.push({ p: p, a: false }) } else { haveOut = true; files.push({ p: p, a: append }) }
    }
    var cio = { stdin: stdin, out: haveOut ? function (s) { bufOut += s } : out, err: haveErr ? function (s) { bufErr += s } : err };
    if (errToOut) cio.err = cio.out;
    var code;
    try { code = await fn(cio) } finally { if (!hasIn) io.stdin = cio.stdin;
      files.forEach(function (f) { if (f.p === null) return; var d = f.e ? bufErr : bufOut; if (!f.e || true) { if (f.e && !haveErr) return; S.writeFile(f.p, d, f.a) } });
    }
    return code;
  };
  S.execCmd = async function (n, io) {
    switch (n.type) {
      case "simple": return S.execSimple(n, io);
      case "if": return S.withRedirs(n, io, async function (cio) { var sv = S._inCond; S._inCond = true; var c; try { c = await S.execList(n.cond, cio) } finally { S._inCond = sv } if (c == 0) return S.execList(n.body, cio); if (n.els) return n.els.type == "if" ? S.execCmd(n.els, cio) : S.execList(n.els, cio); return 0 });
      case "while": return S.withRedirs(n, io, async function (cio) { var code = 0, guard = 0; try { while (guard++ < 5000) { var sv = S._inCond; S._inCond = true; var c; try { c = await S.execList(n.cond, cio) } finally { S._inCond = sv } if ((c == 0) == n.until) break; try { code = await S.execList(n.body, cio) } catch (e) { if (e instanceof Ctl && e.t == "break") break; if (e instanceof Ctl && e.t == "continue") continue; throw e } } } catch (e) { throw e } return code });
      case "for": return S.withRedirs(n, io, async function (cio) { var items = []; if (n.words === null) items = S.pos.slice(1); else for (var i = 0; i < n.words.length; i++) items = items.concat(await S.expand(n.words[i])); var code = 0; for (var k = 0; k < items.length; k++) { S.vars[n.name] = items[k]; try { code = await S.execList(n.body, cio) } catch (e) { if (e instanceof Ctl && e.t == "break") break; if (e instanceof Ctl && e.t == "continue") continue; throw e } } return code });
      case "case": { var subj = (await S.expand(n.subj, true)).join(""); for (var ci = 0; ci < n.cases.length; ci++) { var cs = n.cases[ci]; for (var pi = 0; pi < cs.pats.length; pi++) { var pat = (await S.expand(cs.pats[pi], true)).join(""); if (new RegExp("^" + S.globRe(pat) + "$").test(subj)) return S.execList(cs.body, io) } } return 0 }
      case "group": return S.withRedirs(n, io, function (cio) { return S.execList(n.body, cio) });
      case "subshell": { var sv2 = { cwd: S.cwd, vars: JSON.parse(JSON.stringify(S.vars)) }; try { return await S.execList(n.body, io) } finally { S.cwd = sv2.cwd; S.vars = sv2.vars } }
      case "func": S.funcs[n.name] = n.body; return 0;
    }
    return 0;
  };
  S.execSimple = async function (n, io) {
    var words = [];
    for (var i = 0; i < n.words.length; i++) words = words.concat(await S.expand(n.words[i]));
    if (n.assigns.length && !words.length) { for (var a = 0; a < n.assigns.length; a++) { var m = /^([^=]+)=(.*)$/.exec(n.assigns[a]); S.vars[m[1]] = (await S.expand(m[2], true)).join("") } return 0 }
    var saved = {};
    for (var a2 = 0; a2 < n.assigns.length; a2++) { var m2 = /^([^=]+)=(.*)$/.exec(n.assigns[a2]); saved[m2[1]] = S.vars[m2[1]]; S.vars[m2[1]] = (await S.expand(m2[2], true)).join("") }
    try {
      if (!words.length) return S.withRedirs(n, io, async function () { return 0 });
      if (S.aliases[words[0]] && !S._noAlias) { var al = S.aliases[words[0]].split(/\s+/); words = al.concat(words.slice(1)) }
      return await S.withRedirs(n, io, function (cio) { return S.call(words, cio) });
    } finally { Object.keys(saved).forEach(function (k) { if (saved[k] === undefined) delete S.vars[k]; else S.vars[k] = saved[k] }) }
  };
  S.call = async function (words, io) {
    var name = words[0], args = words.slice(1);
    if (S.funcs[name]) { var sp = S.pos; S.pos = [name].concat(args); try { return await S.execCmd(S.funcs[name], io) } catch (e) { if (e instanceof Ctl && e.t == "return") return e.v; throw e } finally { S.pos = sp } }
    var c = { args: args, name: name, stdin: io.stdin, out: io.out, err: io.err, sim: S, io: io };
    c.err = function (s) { io.err(s) };
    if (S.builtins[name]) return await S.builtins[name](c);
    if (name.indexOf("/") >= 0) return S.runPath(name, args, io);
    var cmd = S.commands[name];
    if (cmd) {
      if (S.ext[name] === false) { io.err("bash: " + name + ": command not found\n"); return 127 }
      return await cmd(c);
    }
    var p = ["/usr/local/bin/" + name, "/usr/bin/" + name, "/bin/" + name].filter(function (x) { return S.vfs.exists(x) })[0];
    if (p) return S.runPath(p, args, io);
    io.err("bash: " + name + ": command not found\n"); return 127;
  };
  S.runPath = async function (path, args, io) {
    var p = S.abs(path);
    if (!S.vfs.exists(p)) { io.err("bash: " + path + ": No such file or directory\n"); return 127 }
    if (S.vfs.isDir(p)) { io.err("bash: " + path + ": Is a directory\n"); return 126 }
    if (!S.can(p, 1)) { io.err("bash: " + path + ": Permission denied\n"); return 126 }
    var src = S.vfs.read(p);
    var sp = S.pos, sv = { cwd: S.cwd };
    S.pos = [path].concat(args);
    try { return await S.execList(S.parse(src.replace(/^#!.*\n/, "")), io) } catch (e) { if (e instanceof Ctl && (e.t == "exit" || e.t == "return")) return e.v; throw e } finally { S.pos = sp }
  };
  /* top level */
  S.run = async function (line) {
    var out = "", err = "";
    S.hist.push(line);
    S._errSink = null;
    var io = { stdin: "", out: function (s) { out += s }, err: function (s) { err += s } };
    var code = 0;
    try { code = await S.execList(S.parse(line), io) } catch (e) { if (e instanceof Ctl) { code = e.v || 0; if (e.t == "exit" && S.onexit) S.onexit() } else { err += "bash: " + (e.message || e) + "\n"; code = 2 } }
    S.lastCode = code; S.allout += out + err;
    return { out: out, err: err, code: code };
  };
  S.Ctl = Ctl;
  S.bbRun = async function (name, args, stdin) { var r = await S.bb.exec(name, args, { stdin: stdin || "", cwd: S.cwd }); return r };
  S.builtins = {}; S.commands = {};
  S.setup();
}
