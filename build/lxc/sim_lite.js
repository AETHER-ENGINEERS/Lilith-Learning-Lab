/* Light-weight replacement for the Jade kit: a tiny in-memory VFS plus JS versions of grep, sed, awk, sort, uniq, wc, cut, tr, head, tail and find. Original code. */
function LiteVFS() {
  var F = {}, D = { "/": 1 };
  function norm(p) { var a = [], o = String(p).split("/"); o.forEach(function (x) { if (x === "" || x === ".") return; if (x === "..") a.pop(); else a.push(x) }); return "/" + a.join("/") }
  function par(p) { p = norm(p); return p.slice(0, p.lastIndexOf("/")) || "/" }
  var v = this;
  v.exists = function (p) { p = norm(p); return p in F || p in D };
  v.isDir = function (p) { return norm(p) in D };
  v.read = function (p) { p = norm(p); if (!(p in F)) throw new Error("ENOENT " + p); return F[p] };
  v.mkdirp = function (p) { p = norm(p); var cur = ""; p.split("/").filter(Boolean).forEach(function (x) { cur += "/" + x; D[cur] = 1 }) };
  v.write = function (p, c) { p = norm(p); v.mkdirp(par(p)); F[p] = String(c) };
  v.list = function (p) { p = norm(p); var pre = p == "/" ? "/" : p + "/", out = {}; Object.keys(F).concat(Object.keys(D)).forEach(function (k) { if (k != p && k.indexOf(pre) == 0) { var r = k.slice(pre.length).split("/")[0]; if (r) out[r] = 1 } }); return Object.keys(out).sort() };
  v.rm = function (p, rec) { p = norm(p); var pre = p + "/"; Object.keys(F).forEach(function (k) { if (k == p || k.indexOf(pre) == 0) delete F[k] }); Object.keys(D).forEach(function (k) { if (k != "/" && (k == p || k.indexOf(pre) == 0)) delete D[k] }) };
  v.copy = function (a, b, rec) { a = norm(a); b = norm(b); if (a in F) { v.write(b, F[a]); return } v.mkdirp(b); var pre = a + "/"; Object.keys(F).forEach(function (k) { if (k.indexOf(pre) == 0) v.write(b + "/" + k.slice(pre.length), F[k]) }); Object.keys(D).forEach(function (k) { if (k.indexOf(pre) == 0) D[b + "/" + k.slice(pre.length)] = 1 }) };
  v.move = function (a, b) { v.copy(a, b, true); v.rm(a, true) };
  v._all = function () { return Object.keys(F).concat(Object.keys(D)).sort() };
}
function LiteText(S) {
  var v = S.vfs;
  function rf(f, c) { var p = S.abs(f); if (!v.exists(p)) { c.e.push(f + ": No such file or directory\n"); c.rc = 2; return null } if (v.isDir(p)) { c.e.push(f + ": Is a directory\n"); c.rc = 2; return null } return v.read(p) }
  function lines(t) { if (t === "") return []; var a = t.split("\n"); if (a[a.length - 1] === "") a.pop(); return a }
  function flags(args, withVal) { var f = {}, pos = [], i = 0; for (; i < args.length; i++) { var x = args[i]; if (x == "--") { pos = pos.concat(args.slice(i + 1)); break } if (/^-[A-Za-z]/.test(x)) { var j = 1; while (j < x.length) { var ch = x[j]; if (withVal.indexOf(ch) >= 0) { var val = x.slice(j + 1); if (!val) val = args[++i]; (f[ch] = f[ch] || []).push(val); break } f[ch] = f[ch] || [true]; j++ } } else if (/^-\d+$/.test(x)) { f.n = [x.slice(1)] } else pos.push(x) } return { f: f, pos: pos } }
  function inputs(P, from, c, stdin) { var fs = P.pos.slice(from); if (!fs.length) return [{ n: "(standard input)", t: stdin || "" }]; var o = []; fs.forEach(function (f) { var t = rf(f, c); if (t !== null) o.push({ n: f, t: t }) }); return o }
  function re(p, f) { try { return new RegExp(p, f) } catch (e) { return null } }
  function ere(p) { return p.replace(/\\([<>])/g, "\\b").replace(/\[\[:digit:\]\]/g, "[0-9]").replace(/\[\[:space:\]\]/g, "\\s").replace(/\[\[:alpha:\]\]/g, "[A-Za-z]").replace(/\[\[:upper:\]\]/g, "[A-Z]").replace(/\[\[:lower:\]\]/g, "[a-z]").replace(/\[:digit:\]/g, "0-9").replace(/\[:space:\]/g, "\\s").replace(/\[:alpha:\]/g, "A-Za-z").replace(/\[:alnum:\]/g, "A-Za-z0-9") }
  function bre(p) { return ere(p.replace(/\\([(){}|+?])/g, "\u0001$1").replace(/([(){}|+?])/g, "\\$1").replace(/\u0001/g, "")) }
  var T = {};
  T.grep = function (args, stdin, c) {
    var P = flags(args, ["e", "A", "B", "C", "m"]), f = P.f, pats = f.e ? f.e.slice() : [P.pos.shift()];
    if (pats[0] === undefined) { c.e.push("Usage: grep [OPTION]... PATTERNS [FILE]...\n"); c.rc = 2; return }
    var conv = f.E || f.P ? ere : (f.F ? function (x) { return x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") } : bre);
    var src = pats.map(function (x) { return conv(x) }).join("|"); if (f.w) src = "\\b(?:" + src + ")\\b"; if (f.x) src = "^(?:" + src + ")$";
    var R = re(src, f.i ? "i" : ""); if (!R) { c.e.push("grep: Unmatched ( or \\(\n"); c.rc = 2; return }
    var files = P.pos, ins;
    if (f.r || f.R) { ins = []; var roots = files.length ? files : ["."]; roots.forEach(function (r) { var walk = function (p, show) { if (v.isDir(S.abs(p))) { v.list(S.abs(p)).forEach(function (n) { walk((p == "." ? "." : p.replace(/\/$/, "")) + "/" + n, 1) }) } else if (v.exists(S.abs(p))) ins.push({ n: p == "." ? p : p.replace(/^\.\//, ""), t: v.read(S.abs(p)) }) }; if (!v.exists(S.abs(r))) { c.e.push("grep: " + r + ": No such file or directory\n"); c.rc = 2; return } walk(r, 0) }); ins.forEach(function (x) { if (x.n.indexOf("./") == 0) x.n = x.n.slice(2) }) }
    else ins = inputs({ pos: files }, 0, c, stdin);
    var multi = ins.length > 1 || f.r || f.R, any = false, ctxA = +((f.A || f.C || [0])[0]) || 0, ctxB = +((f.B || f.C || [0])[0]) || 0, mx = f.m ? +f.m[0] : 1e9;
    ins.forEach(function (x) { var L = lines(x.t), cnt = 0, last = -1, shown = {}; L.forEach(function (l, i) { var m = R.test(l) != !!f.v; if (m && cnt < mx) { cnt++; any = true; if (f.q) return; if (f.c || f.l || f.L) return; for (var k = Math.max(0, i - ctxB); k <= Math.min(L.length - 1, i + ctxA); k++) { if (shown[k]) continue; shown[k] = 1; if ((ctxA || ctxB) && last >= 0 && k > last + 1) c.o.push("--\n"); last = k; var pre = (multi && !f.h ? x.n + (k == i ? ":" : "-") : "") + (f.n ? (k + 1) + (k == i ? ":" : "-") : ""); if (f.o && k == i) { var g = new RegExp(R.source, R.flags + "g"), mm; while ((mm = g.exec(l))) { c.o.push(pre + mm[0] + "\n"); if (!mm[0]) g.lastIndex++ } } else c.o.push(pre + L[k] + "\n") } } }); if (f.c) c.o.push((multi && !f.h ? x.n + ":" : "") + cnt + "\n"); if (f.l && cnt) c.o.push(x.n + "\n"); if (f.L && !cnt) c.o.push(x.n + "\n") });
    if (!any && !c.rc) c.rc = 1;
  };
  function sedParse(prog) {
    var cmds = [], i = 0, s = prog;
    function addr() { var m, a = null; if ((m = /^(\d+|\$)/.exec(s.slice(i)))) { a = { n: m[1] == "$" ? "$" : +m[1] }; i += m[1].length } else if (s[i] == "/") { var j = i + 1; while (j < s.length && s[j] != "/") { if (s[j] == "\\") j++; j++ } a = { re: re(bre(s.slice(i + 1, j)), "") }; i = j + 1 } return a }
    while (i < s.length) {
      while (i < s.length && /[\s;]/.test(s[i])) i++; if (i >= s.length) break;
      var a1 = addr(), a2 = null; if (a1 && s[i] == ",") { i++; a2 = addr() } var neg = false; if (s[i] == "!") { neg = true; i++ } var ch = s[i++], cmd = { a1: a1, a2: a2, neg: neg, c: ch };
      if (ch == "s") { var d = s[i++], parts = [], cur = ""; while (i < s.length && parts.length < 2) { if (s[i] == "\\" && s[i + 1] == d) { cur += d; i += 2; continue } if (s[i] == "\\") { cur += s[i] + s[i + 1]; i += 2; continue } if (s[i] == d) { parts.push(cur); cur = ""; i++; continue } cur += s[i++] } var fl = ""; while (i < s.length && /[gpiI0-9]/.test(s[i])) fl += s[i++]; cmd.rep = parts[1]; cmd.g = fl.indexOf("g") >= 0; cmd.p = fl.indexOf("p") >= 0; cmd.re = re(bre(parts[0]), /[iI]/.test(fl) ? "i" : ""); if (!cmd.re) throw new Error("unterminated `s' command") }
      else if (ch == "y") { var d2 = s[i++], aa = "", bb = ""; while (s[i] != d2) aa += s[i++]; i++; while (s[i] != d2) bb += s[i++]; i++; cmd.y = [aa, bb] }
      else if ("aic".indexOf(ch) >= 0) { var t = s.slice(i).replace(/^\\?\s*/, ""); cmd.t = t.split("\n")[0]; i = s.length }
      else if ("dpq=".indexOf(ch) < 0) throw new Error("unknown command: `" + ch + "'");
      cmds.push(cmd);
    }
    return cmds;
  }
  function sedRun(cmds, text, quiet) {
    var L = lines(text), out = [], st = cmds.map(function () { return { on: false } });
    for (var n = 0; n < L.length; n++) {
      var line = L[n], del = false, quit = false, pr = [];
      for (var k = 0; k < cmds.length && !del; k++) {
        var m = cmds[k], on = true;
        if (m.a1) { var hit = function (a) { return a.re ? a.re.test(line) : (a.n == "$" ? n == L.length - 1 : a.n == n + 1) }; if (!m.a2) on = hit(m.a1); else { if (st[k].on) { on = true; if (hit(m.a2) || (m.a2.n && n + 1 >= m.a2.n)) st[k].on = false } else if (hit(m.a1)) { on = true; if (!(m.a2.n && m.a2.n <= n + 1) && !(m.a2.re && false)) st[k].on = true } else on = false } }
        if (m.neg) on = !on; if (!on) continue;
        if (m.c == "s") { var did = false; if (m.g) { line = line.replace(new RegExp(m.re.source, m.re.flags + "g"), function () { did = true; return sedRep(m.rep, arguments) }) } else line = line.replace(m.re, function () { did = true; return sedRep(m.rep, arguments) }); if (did && m.p) pr.push(line) }
        else if (m.c == "d") del = true; else if (m.c == "p") pr.push(line); else if (m.c == "q") quit = true; else if (m.c == "=") out.push(String(n + 1));
        else if (m.c == "y") line = line.split("").map(function (x) { var q = m.y[0].indexOf(x); return q >= 0 ? m.y[1][q] : x }).join("");
        else if (m.c == "a") { pr.after = (pr.after || []).concat(m.t) } else if (m.c == "i") out.push(m.t); else if (m.c == "c") { out.push(m.t); del = true }
      }
      pr.forEach(function (x) { out.push(x) }); if (!del && !quiet) out.push(line); (pr.after || []).forEach(function (x) { out.push(x) }); if (quit) break;
    }
    return out.length ? out.join("\n") + "\n" : "";
  }
  function sedRep(rep, g) { var m = Array.prototype.slice.call(g, 0, -2).filter(function (x) { return typeof x != "object" }); return rep.replace(/\\(\d)|&|\\n|\\t|\\(.)/g, function (all, d, esc) { if (d !== undefined) return m[+d] || ""; if (all == "&") return m[0]; if (all == "\\n") return "\n"; if (all == "\\t") return "\t"; return esc }) }
  T.sed = function (args, stdin, c) {
    var P = flags(args, ["e", "f"]), f = P.f, progs = f.e ? f.e : [P.pos.shift()];
    if (progs[0] === undefined) { c.e.push("Usage: sed [OPTION]... {script} [input-file]...\n"); c.rc = 1; return }
    var cmds; try { cmds = sedParse(progs.join("\n")) } catch (e) { c.e.push("sed: -e expression #1, char 0: " + e.message + "\n"); c.rc = 1; return }
    if (f.i) { P.pos.forEach(function (fn) { var t = rf(fn, c); if (t !== null) { v.write(S.abs(fn), sedRun(cmds, t, !!f.n)); } }); return }
    inputs(P, 0, c, stdin).forEach(function (x) { c.o.push(sedRun(cmds, x.t, !!f.n)) });
  };
  function awkExpr(s, vars) {
    var out = "", i = 0;
    while (i < s.length) {
      var ch = s[i], m;
      if (ch == '"') { var j = i + 1; while (j < s.length && s[j] != '"') { if (s[j] == "\\") j++; j++ } out += s.slice(i, j + 1); i = j + 1; continue }
      if (ch == "/" && /(^|[(,~!&|\s])$/.test(out.slice(-2) || " ") && !/[\w)\]]\s*$/.test(out)) { var j2 = i + 1; while (j2 < s.length && s[j2] != "/") { if (s[j2] == "\\") j2++; j2++ } out += "RX(" + JSON.stringify(s.slice(i + 1, j2)) + ")"; i = j2 + 1; continue }
      if (ch == "$") { var rest = s.slice(i + 1); if ((m = /^(\d+|[A-Za-z_]\w*|\([^)]*\))/.exec(rest))) { out += "FLD(" + awkExpr(m[1], vars) + ")"; i += 1 + m[1].length; continue } }
      if ((m = /^[A-Za-z_]\w*/.exec(s.slice(i)))) { var id = m[0]; i += id.length; if (id == "length") { out += s[i] == "(" ? "LEN" : "LEN()"; continue } if (/^(int|sqrt|substr|index|split|toupper|tolower|sprintf|sin|cos|exp|log)$/.test(id)) { out += "FN." + id; continue } out += s[i] == "[" ? "A." + id : "V." + id; if (s[i] == "[") { var j3 = s.indexOf("]", i); out += "[" + awkExpr(s.slice(i + 1, j3), vars) + "]"; i = j3 + 1 } continue }
      if ((m = /^\d+(\.\d+)?/.exec(s.slice(i)))) { out += m[0]; i += m[0].length; continue }
      if (s.slice(i, i + 2) == "!~") { out += " NM "; i += 2; continue } if (ch == "~") { out += " MT "; i++; continue }
      out += ch; i++;
    }
    return out.replace(/\bV\.(NR|NF)\b/g, "ENVV.$1");
  }
  function awkStmt(st, vars) {
    st = st.trim(); if (!st) return "";
    var m;
    if ((m = /^printf\s+(.*)$/.exec(st))) return "OUT.push(FN.sprintf(" + awkExpr(m[1], vars) + "));";
    if ((m = /^print(?:\s+(.*))?$/.exec(st))) { var a = m[1] ? splitTop(m[1], ",").map(function (x) { return "(" + awkExpr(x, vars) + ")" }) : ["REC.$0"]; return "OUT.push([" + a.join(",") + '].map(function(x){return typeof x=="number"?String(+x.toFixed(6)):x}).join(OFS)+"\\n");' }
    if (/^next$/.test(st)) return "throw NEXT;"; if (/^exit/.test(st)) return "throw EXIT;";
    return awkExpr(st, vars).replace(/\bA\.(\w+)\[([^\]]*)\]\s*(\+\+|\+=|=)/g, function (all, n, k, op) { return all }) + ";";
  }
  function splitTop(s, sep) { var r = [], d = 0, cur = "", q = false; for (var i = 0; i < s.length; i++) { var c = s[i]; if (c == '"') q = !q; if (!q) { if ("([{".indexOf(c) >= 0) d++; if (")]}".indexOf(c) >= 0) d--; if (c == sep && d == 0) { r.push(cur); cur = ""; continue } } cur += c } r.push(cur); return r }
  function awkBlock(body, vars) {
    var out = "", parts = splitTop(body, ";");
    parts.forEach(function (p) { p = p.trim(); var m; if ((m = /^if\s*\((.*?)\)\s*(.*?)(?:\s+else\s+(.*))?$/.exec(p))) { out += "if(T(" + awkExpr(m[1], vars) + ")){" + awkStmt(m[2], vars) + "}" + (m[3] ? "else{" + awkStmt(m[3], vars) + "}" : "") } else if ((m = /^for\s*\(\s*(\w+)\s+in\s+(\w+)\s*\)\s*(.*)$/.exec(p))) { out += "for(var _k in A." + m[2] + "){V." + m[1] + "=isNaN(_k)?_k:+_k;" + awkStmt(m[3], vars) + "}" } else out += awkStmt(p, vars) });
    return out;
  }
  T.awk = function (args, stdin, c) {
    var P = flags(args, ["F", "v", "f"]), f = P.f, prog = P.pos.shift(), fs = f.F ? f.F[0].replace(/^\\t$/, "\t") : null;
    if (prog === undefined) { c.e.push("Usage: awk [OPTIONS] 'PROGRAM' [FILE...]\n"); c.rc = 1; return }
    var rules = [], i = 0, s = prog.trim();
    try {
      while (i < s.length) {
        while (i < s.length && /[\s;]/.test(s[i])) i++; if (i >= s.length) break;
        var pat = "", kind = "main";
        if (/^BEGIN\b/.test(s.slice(i))) { kind = "begin"; i += 5 } else if (/^END\b/.test(s.slice(i))) { kind = "end"; i += 3 } else { var j = i, q = false, rx = false; while (j < s.length && (s[j] != "{" || q || rx)) { if (s[j] == '"' && !rx) q = !q; if (s[j] == "/" && !q) rx = !rx; j++ } pat = s.slice(i, j).trim(); i = j }
        while (s[i] == " ") i++; var body = null;
        if (s[i] == "{") { var d = 0, j2 = i; for (; j2 < s.length; j2++) { if (s[j2] == "{") d++; if (s[j2] == "}") { d--; if (!d) break } } body = s.slice(i + 1, j2); i = j2 + 1 }
        rules.push({ kind: kind, pat: pat, body: body });
      }
    } catch (e) { c.e.push("awk: syntax error\n"); c.rc = 2; return }
    var V = {}, A = {}, OUT = [], OFS = " ", ENVV = { NR: 0, NF: 0 }, REC = { $0: "" }, fields = [];
    (f.v || []).forEach(function (kv) { var q = kv.indexOf("="); V[kv.slice(0, q)] = kv.slice(q + 1) });
    var NEXT = { n: 1 }, EXIT = { e: 1 };
    function FLD(n) { n = +n; return n == 0 ? REC.$0 : (fields[n - 1] === undefined ? "" : (isNaN(fields[n - 1]) || fields[n - 1] === "" ? fields[n - 1] : +fields[n - 1])) }
    function setRec(l) { REC.$0 = l; fields = fs === null || fs === " " ? l.trim().split(/\s+/).filter(function (x) { return x !== "" }) : (fs.length == 1 ? l.split(fs) : l.split(new RegExp(fs))); ENVV.NF = fields.length; ENVV.NR++ }
    var FN = { int: function (x) { return Math.trunc(x) }, sqrt: Math.sqrt, sin: Math.sin, cos: Math.cos, exp: Math.exp, log: Math.log, toupper: function (x) { return String(x).toUpperCase() }, tolower: function (x) { return String(x).toLowerCase() }, substr: function (x, a, b) { x = String(x); return b === undefined ? x.slice(a - 1) : x.substr(a - 1, b) }, index: function (x, y) { return String(x).indexOf(y) + 1 }, split: function (x, arr, sep) { return 0 }, sprintf: function (fmt) { var a = Array.prototype.slice.call(arguments, 1), k = 0; return String(fmt).replace(/%(-?\d*)(?:\.(\d+))?([sdifc%])/g, function (all, w, p, t) { if (t == "%") return "%"; var val = a[k++]; var r = t == "s" ? String(val) : (t == "c" ? String(val) : (t == "f" ? Number(val).toFixed(p === undefined ? 6 : +p) : String(Math.trunc(val)))); if (w) { var n = Math.abs(+w); while (r.length < n) r = +w < 0 ? r + " " : " " + r } return r }).replace(/\\n/g, "\n").replace(/\\t/g, "\t") } };
    function LEN(x) { return String(x === undefined ? REC.$0 : x).length }
    function RX(p) { var r = re(ere(p), ""); return { test: function () { return r.test(REC.$0) }, r: r, valueOf: function () { return r.test(REC.$0) ? 1 : 0 } } }
    function T(x) { return x === "" || x === 0 || x === false || x === undefined ? false : (typeof x == "string" && !isNaN(x) ? +x != 0 : !!x) }
    var asProxy = function (o) { return new Proxy(o, { get: function (t, k) { if (!(k in t)) t[k] = typeof k == "string" ? 0 : undefined; return t[k] } }) };
    V = asProxy(V); var Aobj = new Proxy(A, { get: function (t, k) { if (!(k in t)) t[k] = asProxy({}); return t[k] } });
    var comp = function (code) { return new Function("V", "A", "FLD", "FN", "RX", "LEN", "T", "OUT", "OFS", "ENVV", "REC", "NEXT", "EXIT", "MT", "NM", "with(ENVV){return function(){" + code + "}}") };
    var MT = function (a, b) { return b && b.r ? b.r.test(String(a)) : re(ere(String(b)), "").test(String(a)) };
    var run = function (code, extra) { var fn = comp(code)(V, Aobj, FLD, FN, RX, LEN, T, OUT, OFS, ENVV, REC, NEXT, EXIT, MT, null); return fn() };
    var cond = function (pat) { var e = awkExpr(pat, V).replace(/ MT /g, " ~ ").replace(/ NM /g, " !~ "); e = e.replace(/(FLD\([^)]*\)|V\.\w+|REC\.\$0)\s*~\s*(RX\([^)]*\)|"[^"]*"|\w+)/g, "MT($1,$2)").replace(/(FLD\([^)]*\)|V\.\w+|REC\.\$0)\s*!~\s*(RX\([^)]*\)|"[^"]*"|\w+)/g, "!MT($1,$2)").replace(/\bRX\(("(?:[^"\\]|\\.)*")\)(?!\s*[,)])/g, "RX($1).test()"); return "return T(" + e + ");" };
    var fixed = rules.map(function (r) { return { kind: r.kind, cond: r.pat ? cond(r.pat) : null, code: r.body === null ? "OUT.push(REC.$0+'\\n');" : awkBlock(r.body, V).replace(/MT\b/g, "MT") } });
    try {
      fixed.forEach(function (r) { if (r.kind == "begin") try { run(r.code) } catch (e) { if (e !== EXIT) throw e } });
      var stop = false;
      if (fixed.some(function (r) { return r.kind != "begin" })) inputs(P, 0, c, stdin).forEach(function (x) { if (stop) return; lines(x.t).forEach(function (l) { if (stop) return; setRec(l); try { fixed.forEach(function (r) { if (r.kind != "main") return; if (r.cond === null || run(r.cond)) run(r.code) }) } catch (e) { if (e === EXIT) stop = true; else if (e !== NEXT) throw e } }) });
      fixed.forEach(function (r) { if (r.kind == "end") try { run(r.code) } catch (e) { if (e !== EXIT) throw e } });
    } catch (e) { c.e.push("awk: " + e.message + "\n"); c.rc = 2 }
    c.o.push(OUT.join(""));
  };
  T.sort = function (args, stdin, c) {
    var P = flags(args, ["k", "t", "o"]), f = P.f, all = []; inputs(P, 0, c, stdin).forEach(function (x) { all = all.concat(lines(x.t)) });
    var sep = f.t ? f.t[0] : null, kk = f.k ? f.k[0].split(",")[0].replace(/[nrh]/g, "") : null, kn = f.k && /n/.test(f.k[0]);
    function key(l) { if (!kk) return l; var p = sep ? l.split(sep) : l.trim().split(/\s+/); return p[+kk - 1] === undefined ? "" : p[+kk - 1] }
    var num = f.n || kn || f.h, hum = function (s) { var m = /^([\d.]+)\s*([KMGT]?)/i.exec(s.trim()); if (!m) return 0; return parseFloat(m[1]) * Math.pow(1024, "KMGT".indexOf(m[2].toUpperCase()) + 1) };
    all.sort(function (a, b) { var x = key(a), y = key(b), r; if (f.h) r = hum(x) - hum(y); else if (num) r = (parseFloat(x) || 0) - (parseFloat(y) || 0); else { if (f.f) { x = x.toLowerCase(); y = y.toLowerCase() } r = x < y ? -1 : x > y ? 1 : 0 } if (r === 0 && !num) r = 0; return r });
    if (f.r || (f.k && /r/.test(f.k[0]))) all.reverse(); if (f.u) all = all.filter(function (x, i) { return i == 0 || key(x) != key(all[i - 1]) });
    c.o.push(all.length ? all.join("\n") + "\n" : "");
  };
  T.uniq = function (args, stdin, c) {
    var P = flags(args, []), f = P.f, L = lines(inputs(P, 0, c, stdin)[0].t), o = [], i = 0;
    while (i < L.length) { var j = i; while (j < L.length && (f.i ? L[j].toLowerCase() == L[i].toLowerCase() : L[j] == L[i])) j++; var n = j - i; if (!(f.d && n < 2) && !(f.u && n > 1)) o.push(f.c ? ("       " + n).slice(-7) + " " + L[i] : L[i]); i = j }
    c.o.push(o.length ? o.join("\n") + "\n" : "");
  };
  T.wc = function (args, stdin, c) {
    var P = flags(args, []), f = P.f, ins = inputs(P, 0, c, stdin), tot = [0, 0, 0], any = f.l || f.w || f.c || f.m;
    ins.forEach(function (x) { var l = (x.t.match(/\n/g) || []).length, w = x.t.split(/\s+/).filter(Boolean).length, b = x.t.length; tot[0] += l; tot[1] += w; tot[2] += b; var s = []; if (!any || f.l) s.push(l); if (!any || f.w) s.push(w); if (!any || f.c || f.m) s.push(b); c.o.push(s.map(function (n) { return any && s.length == 1 ? String(n) : ("       " + n).slice(-7) }).join(" ") + (P.pos.length ? " " + x.n : "") + "\n") });
    if (ins.length > 1) { var s2 = []; if (!any || f.l) s2.push(tot[0]); if (!any || f.w) s2.push(tot[1]); if (!any || f.c) s2.push(tot[2]); c.o.push(s2.map(function (n) { return ("       " + n).slice(-7) }).join(" ") + " total\n") }
  };
  T.cut = function (args, stdin, c) {
    var P = flags(args, ["d", "f", "c"]), f = P.f, d = f.d ? f.d[0] : "\t", spec = (f.f || f.c || [""])[0];
    var pick = function (n, len) { return spec.split(",").some(function (r) { var m = /^(\d*)(-?)(\d*)$/.exec(r); if (!m) return false; var a = m[1] ? +m[1] : 1, b = m[2] ? (m[3] ? +m[3] : len) : a; return n >= a && n <= b }) };
    inputs(P, 0, c, stdin).forEach(function (x) { lines(x.t).forEach(function (l) { if (f.c) { c.o.push(l.split("").filter(function (_, i) { return pick(i + 1, l.length) }).join("") + "\n"); return } if (l.indexOf(d) < 0) { if (!f.s) c.o.push(l + "\n"); return } var p = l.split(d); c.o.push(p.filter(function (_, i) { return pick(i + 1, p.length) }).join(d) + "\n") }) });
  };
  T.tr = function (args, stdin, c) {
    var P = flags(args, []), f = P.f, exp = function (s) { s = s.replace(/\[:upper:\]/g, "A-Z").replace(/\[:lower:\]/g, "a-z").replace(/\[:digit:\]/g, "0-9").replace(/\[:space:\]/g, " \t\n").replace(/\[:alpha:\]/g, "A-Za-z").replace(/\\n/g, "\n").replace(/\\t/g, "\t"); return s.replace(/(.)-(.)/g, function (_, a, b) { var r = ""; for (var k = a.charCodeAt(0); k <= b.charCodeAt(0); k++) r += String.fromCharCode(k); return r }) };
    var a = exp(P.pos[0] || ""), b = P.pos[1] !== undefined ? exp(P.pos[1]) : "", t = stdin || "", o = "";
    if (f.d) { for (var i = 0; i < t.length; i++) if ((a.indexOf(t[i]) >= 0) == !!f.c) { if (!f.c) continue; } else o += t[i]; if (f.c) { o = ""; for (var k = 0; k < t.length; k++) if (a.indexOf(t[k]) >= 0) o += t[k] } c.o.push(o); return }
    for (var j = 0; j < t.length; j++) { var q = a.indexOf(t[j]), ch = t[j]; if (f.c) { q = q < 0 ? 0 : -1; if (q >= 0) ch = b[b.length - 1] } else if (q >= 0) ch = b[Math.min(q, b.length - 1)] === undefined ? ch : b[Math.min(q, b.length - 1)]; if (f.s && o.length && o[o.length - 1] == ch && b.indexOf(ch) >= 0) continue; o += ch }
    c.o.push(o);
  };
  function headTail(isHead) { return function (args, stdin, c) { var P = flags(args, ["n", "c"]), f = P.f, n = f.n ? parseInt(f.n[0], 10) : 10, ins = inputs(P, 0, c, stdin); ins.forEach(function (x, i) { var L = lines(x.t), r; if (isHead) r = n < 0 ? L.slice(0, n) : L.slice(0, n); else r = f.n && /^\+/.test(f.n[0]) ? L.slice(n - 1) : L.slice(Math.max(0, L.length - n)); if (ins.length > 1) c.o.push((i ? "\n" : "") + "==> " + x.n + " <==\n"); c.o.push(r.length ? r.join("\n") + "\n" : "") }) } }
  T.head = headTail(true); T.tail = headTail(false);
  T.find = function (args, stdin, c) {
    var roots = [], i = 0; while (i < args.length && args[i][0] != "-" && args[i] != "!") roots.push(args[i++]); if (!roots.length) roots = ["."];
    var opt = { name: null, type: null, max: 99, iname: null, size: null, empty: false }, rest = args.slice(i);
    for (var j = 0; j < rest.length; j++) { var a = rest[j]; if (a == "-name") opt.name = rest[++j]; else if (a == "-iname") opt.iname = rest[++j]; else if (a == "-type") opt.type = rest[++j]; else if (a == "-maxdepth") opt.max = +rest[++j]; else if (a == "-size") opt.size = rest[++j]; else if (a == "-empty") opt.empty = true; else if (a == "-print") { } else if (a == "-perm" || a == "-user" || a == "-mtime") j++ }
    var glob = function (g, fl) { return new RegExp("^" + g.replace(/[.+^${}()|\\]/g, "\\$&").replace(/\*/g, ".*").replace(/\?/g, ".") + "$", fl) };
    roots.forEach(function (r) { var ap = S.abs(r); if (!v.exists(ap)) { c.e.push("find: '" + r + "': No such file or directory\n"); c.rc = 1; return } var walk = function (p, disp, d) { var isD = v.isDir(p), base = disp.slice(disp.lastIndexOf("/") + 1), ok = d <= opt.max; if (ok && opt.name && !glob(opt.name, "").test(base)) ok = false; if (ok && opt.iname && !glob(opt.iname, "i").test(base)) ok = false; if (ok && opt.type && (opt.type == "d") != isD) ok = false; if (ok && opt.empty && (isD ? v.list(p).length : v.read(p).length)) ok = false; if (ok && opt.size) { var m = /^([+-]?)(\d+)([ckMG]?)$/.exec(opt.size); if (m && !isD) { var u = { "": 512, c: 1, k: 1024, M: 1048576, G: 1073741824 }[m[3]], sz = Math.ceil(v.read(p).length / u), n = +m[2]; if (m[1] == "+" ? !(sz > n) : m[1] == "-" ? !(sz < n) : sz != n) ok = false } } if (ok) c.o.push(disp + "\n"); if (isD && d < opt.max) v.list(p).forEach(function (nm) { walk((p == "/" ? "" : p) + "/" + nm, (disp.replace(/\/$/, "")) + "/" + nm, d + 1) }) }; walk(ap, r, 0) });
  };
  S.bbRun = async function (name, args, stdin) {
    var c = { o: [], e: [], rc: 0 };
    if (!T[name]) return { stdout: "", stderr: name + ": applet not found\n", code: 127 };
    try { T[name](args, stdin || "", c) } catch (e) { c.e.push(name + ": " + e.message + "\n"); c.rc = c.rc || 1 }
    return { stdout: c.o.join(""), stderr: c.e.join(""), code: c.rc };
  };
}
