/* Lilith Learning Lab: course format (JSON), validation, lab engines.
   Pure functions, no DOM, so the same code runs in the app and in Node tests.

   A course is one JSON file:
   { "format": "lilith-course", "version": 1, "id": "my-course", "title": "...", "subtitle": "...", "author": "...",
     "images": { "fig.svg": "<svg ...>" },
     "chapters": [ {
        "title": "...",                       (required)
        "maps":     [ { "title": "...", "links": ["A [ch2] | relation | B", ...] } ],
        "summary":  ["sentence or paragraph", ...],
        "glossary": [ { "term": "...", "def": "..." } ],
        "keyPoints":["..."],
        "lesson":   [ {"type":"text","items":["..."]}, {"type":"code","lang":"bash","code":"..."},
                      {"type":"figure","image":"fig.svg","caption":"..."}, {"type":"math","tex":"\\frac{a}{b}"}, {"type":"map","title":"...","links":[...]} ],
        "quiz":     [ { "q": "...", "options": ["a","b","c"], "answer": 1, "explain": "..." } ],
        "cards":    [ { "q": "...", "a": "..." } ],
        "practice": [ labs: fill | order | match | write | code | python | terminal | webxdc ]
     } ],
     "finalExam": { "title": "Final exam", "passMark": 70, "size": 20, "questions": [ same shape as quiz ] },   (optional; a plain list of questions also works.
                  Without it the app builds the exam from every chapter quiz.)
     "sandbox": { a terminal lab, optional free practice terminal },
     "apps": [ { "title": "...", "xdc": "<base64 .xdc>" | "html": "..." } ]    (extra webxdc apps shown in Practice > Apps)
   Practice lab {"type":"webxdc","xdc":"<base64 zip>"|"html":"..."|"files":{...}} runs any interactive webxdc app inside the lab;
   the app can call window.lilith.complete() to mark the lab done. */
(function (root) {
  'use strict';

  var FORMAT = 'lilith-course', VERSION = 1;
  var LAB_TYPES = ['fill', 'order', 'match', 'write', 'code', 'python', 'terminal', 'webxdc'];
  var LIMITS = { chapters: 200, text: 6000, items: 400 };

  function s(x) { return x === null || x === undefined ? '' : String(x); }
  function arr(x) { return Array.isArray(x) ? x : (x === null || x === undefined || x === '' ? [] : [x]); }
  function slug(t) { return s(t).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48) || 'course'; }
  function strs(x) { return arr(x).map(function (v) { return s(v).trim(); }).filter(Boolean); }

  /* ---------- normalising ---------- */
  function linkText(l) {
    if (typeof l === 'string') return l.trim();
    if (l && typeof l === 'object') return s(l.from) + ' | ' + s(l.rel) + ' | ' + s(l.to);
    return '';
  }

  function normMaps(c, w, where) {
    var raw = arr(c.maps).concat(c.map ? [c.map] : []), out = [];
    raw.forEach(function (m, i) {
      if (!m || typeof m !== 'object') return;
      var links = arr(m.links !== undefined ? m.links : m.edges).map(linkText).filter(function (t) { return t.split('|').length === 3; });
      if (!links.length) { w.push(where + ': map ' + (i + 1) + ' has no usable links (use "A | relation | B")'); return; }
      out.push({ title: s(m.title) || 'Concept map', links: links });
    });
    return out;
  }

  function normBlock(b, w, where) {
    if (typeof b === 'string') return { type: 'text', items: [b] };
    if (!b || typeof b !== 'object') return null;
    var t = s(b.type || (b.code !== undefined ? 'code' : b.image ? 'figure' : b.links ? 'map' : 'text'));
    if (t === 'text') { var it = strs(b.items !== undefined ? b.items : b.text); return it.length ? { type: 'text', items: it } : null; }
    if (t === 'math') { var tex = s(b.tex !== undefined ? b.tex : b.text).trim(); return tex ? { type: 'text', items: ['$$' + tex + '$$'] } : null; }
    if (t === 'code') { var code = s(b.code).replace(/\s+$/, ''); return code ? { type: 'code', lang: s(b.lang) || 'text', code: code } : null; }
    if (t === 'figure') { return b.image ? { type: 'figure', image: s(b.image), caption: s(b.caption) } : null; }
    if (t === 'map') { var ms = normMaps({ maps: [b] }, w, where); return ms.length ? { type: 'map', map: ms[0] } : null; }
    w.push(where + ': unknown lesson block type "' + t + '" skipped');
    return null;
  }

  function normQuiz(q, w, where) {
    if (!q || typeof q !== 'object' || !s(q.q).trim()) return null;
    var opts = strs(q.options);
    if (opts.length < 2) { w.push(where + ': quiz question needs at least 2 options'); return null; }
    var a = q.answer;
    if (typeof a === 'string' && !/^\d+$/.test(a)) { var k = opts.map(function (o) { return o.toLowerCase(); }).indexOf(a.trim().toLowerCase()); a = k; }
    a = Number(a);
    if (!(a >= 0 && a < opts.length)) { w.push(where + ': quiz answer must be an option index (0-based) or the option text'); return null; }
    return { q: s(q.q).trim(), options: opts, answer: a, explain: s(q.explain).trim() };
  }

  function normLab(l, w, where, idx) {
    if (!l || typeof l !== 'object') return null;
    var t = s(l.type).toLowerCase();
    if (LAB_TYPES.indexOf(t) < 0) { w.push(where + ': lab type "' + s(l.type) + '" is not supported (use ' + LAB_TYPES.join(', ') + ')'); return null; }
    var lab = { id: s(l.id) || ('lab' + idx), type: t, title: s(l.title) || ('Practice ' + (idx + 1)), intro: s(l.intro), hint: s(l.hint), solution: s(l.solution) };
    if (t === 'fill') {
      lab.text = s(l.text);
      if (!/\{\{[^}]+\}\}/.test(lab.text)) { w.push(where + ': fill lab needs {{answer}} blanks'); return null; }
    } else if (t === 'order') {
      lab.items = strs(l.items); if (lab.items.length < 2) { w.push(where + ': order lab needs at least 2 items'); return null; }
    } else if (t === 'match') {
      lab.pairs = arr(l.pairs).filter(function (p) { return Array.isArray(p) && p.length >= 2; }).map(function (p) { return [s(p[0]), s(p[1])]; });
      if (lab.pairs.length < 2) { w.push(where + ': match lab needs at least 2 pairs ([left, right])'); return null; }
    } else if (t === 'write') {
      lab.prompt = s(l.prompt || l.intro); lab.starter = s(l.starter); lab.lang = s(l.lang);
      lab.checks = arr(l.checks).map(function (c) { return typeof c === 'string' ? { re: c, msg: c } : { re: s(c.re), flags: s(c.flags) || 'i', msg: s(c.msg || c.re), not: !!c.not }; }).filter(function (c) { return c.re; });
      if (!lab.checks.length) { w.push(where + ': write lab needs "checks": [{"re": "...", "msg": "..."}]'); return null; }
    } else if (t === 'code') {
      lab.starter = s(l.starter); lab.fn = s(l.fn); lab.isBody = !!l.isBody; lab.checkJs = s(l.checkJs); lab.helpersJs = s(l.helpersJs);
      lab.tests = arr(l.tests).filter(function (x) { return x && typeof x === 'object'; });
      if (!lab.fn && !lab.isBody) { w.push(where + ': code lab needs "fn" (function name) or "isBody": true'); return null; }
      if (!lab.tests.length && !lab.checkJs) { w.push(where + ': code lab needs "tests" or "checkJs"'); return null; }
    } else if (t === 'python') {
      lab.starter = s(l.starter); lab.fn = s(l.fn);
      lab.tests = arr(l.tests).filter(function (x) { return x && typeof x === 'object'; });
      lab.checks = arr(l.checks).map(function (c) { return typeof c === 'string' ? { re: c, msg: c } : { re: s(c.re), flags: s(c.flags) || 'i', msg: s(c.msg || c.re), not: !!c.not }; }).filter(function (c) { return c.re; });
      if (lab.fn && !/^[A-Za-z_]\w*$/.test(lab.fn)) { w.push(where + ': python lab "fn" must be a plain function name'); return null; }
      if (!(lab.fn && lab.tests.length) && !lab.checks.length) { w.push(where + ': python lab needs "fn" with "tests", or "checks" on the printed output'); return null; }
    } else if (t === 'webxdc') {
      lab.xdc = s(l.xdc).replace(/\s+/g, ''); lab.html = s(l.html);
      lab.files = (l.files && typeof l.files === 'object' && !Array.isArray(l.files)) ? l.files : null;
      lab.height = Math.max(240, Math.min(900, Number(l.height) || 520));
      if (!lab.xdc && !lab.html && !lab.files) { w.push(where + ': webxdc lab needs "xdc" (base64 zip), "html" or "files"'); return null; }
      if (lab.xdc && !/^[A-Za-z0-9+\/=]+$/.test(lab.xdc)) { w.push(where + ': webxdc "xdc" is not valid base64'); return null; }
      if (lab.files && !lab.files['index.html']) { w.push(where + ': webxdc "files" needs an index.html'); return null; }
    } else if (t === 'terminal') {
      lab.prompt = s(l.prompt) || '$'; lab.vars = (l.vars && typeof l.vars === 'object') ? l.vars : {};
      lab.banner = s(l.banner); lab.chips = strs(l.chips);
      lab.commands = arr(l.commands).filter(function (c) { return c && typeof c === 'object' && c.re !== undefined; });
      lab.tasks = arr(l.tasks).filter(function (c) { return c && c.text && c.cmd; });
      if (!lab.commands.length) { w.push(where + ': terminal lab needs "commands"'); return null; }
    }
    return lab;
  }

  function validate(raw) {
    var errors = [], warnings = [];
    if (typeof raw === 'string') { try { raw = JSON.parse(raw); } catch (e) { return { ok: false, errors: ['Not valid JSON: ' + e.message], warnings: [] }; } }
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return { ok: false, errors: ['The file must be a JSON object.'], warnings: [] };
    if (raw.format && raw.format !== FORMAT) errors.push('"format" should be "' + FORMAT + '" (found "' + s(raw.format) + '")');
    if (!s(raw.title).trim()) errors.push('"title" is required');
    if (!Array.isArray(raw.chapters) || !raw.chapters.length) errors.push('"chapters" must be a non-empty list');
    if (errors.length) return { ok: false, errors: errors, warnings: warnings };
    var course = {
      format: FORMAT, version: VERSION, id: slug(raw.id || raw.title), title: s(raw.title).trim(), subtitle: s(raw.subtitle).trim(),
      author: s(raw.author).trim(), description: s(raw.description).trim(), teacher: s(raw.teacher).trim(), images: {}, pronounce: {}, chapters: [], sandbox: null, apps: [], exam: null
    };
    if (raw.images && typeof raw.images === 'object') Object.keys(raw.images).forEach(function (k) { if (typeof raw.images[k] === 'string' && /<svg[\s>]/i.test(raw.images[k])) course.images[k] = raw.images[k]; });
    if (raw.pronounce && typeof raw.pronounce === 'object') Object.keys(raw.pronounce).forEach(function (k) { if (typeof raw.pronounce[k] === 'string') course.pronounce[k] = raw.pronounce[k]; });
    raw.chapters.slice(0, LIMITS.chapters).forEach(function (c, i) {
      var where = 'chapter ' + (i + 1);
      if (!c || typeof c !== 'object') { warnings.push(where + ' is not an object; skipped'); return; }
      if (!s(c.title).trim()) { warnings.push(where + ' has no title; skipped'); return; }
      var n = (typeof c.number === 'number') ? c.number : (course.chapters.length ? course.chapters[course.chapters.length - 1].n + 1 : 1);
      where = 'chapter ' + n + ' (' + s(c.title).trim() + ')';
      var gl = c.glossary, glist = [];
      if (gl && !Array.isArray(gl) && typeof gl === 'object') glist = Object.keys(gl).map(function (k) { return { term: k, def: s(gl[k]) }; });
      else glist = arr(gl).filter(function (g) { return g && s(g.term) && s(g.def !== undefined ? g.def : g.definition); }).map(function (g) { return { term: s(g.term).trim(), def: s(g.def !== undefined ? g.def : g.definition).trim() }; });
      var ch = {
        id: s(c.id) || ('ch' + n), n: n, title: s(c.title).trim(),
        maps: normMaps(c, warnings, where), summary: strs(c.summary), glossary: glist, keyPoints: strs(c.keyPoints || c.points),
        lesson: arr(c.lesson).map(function (b) { return normBlock(b, warnings, where); }).filter(Boolean),
        quiz: arr(c.quiz).map(function (q) { return normQuiz(q, warnings, where); }).filter(Boolean),
        cards: arr(c.cards).filter(function (q) { return q && s(q.q) && s(q.a); }).map(function (q) { return { q: s(q.q), a: s(q.a) }; }),
        practice: arr(c.practice).map(function (l, k) { return normLab(l, warnings, where, k); }).filter(Boolean)
      };
      // unique lab ids inside a chapter
      var seen = {}; ch.practice.forEach(function (l, k) { var id = l.id; while (seen[id]) id = id + '_' + k; seen[id] = 1; l.id = id; });
      ch.lesson.forEach(function (b) { if (b.type === 'figure' && !course.images[b.image]) warnings.push(where + ': figure "' + b.image + '" is not in "images"'); });
      course.chapters.push(ch);
    });
    course.apps = arr(raw.apps).filter(function (a) { return a && typeof a === 'object' && (a.xdc || a.html || a.files); }).map(function (a, i) { return { id: s(a.id) || ('app' + (i + 1)), title: s(a.title) || ('App ' + (i + 1)), xdc: s(a.xdc).replace(/\s+/g, ''), html: s(a.html), files: a.files && typeof a.files === 'object' ? a.files : null, height: Math.max(240, Math.min(900, Number(a.height) || 520)) }; });
    if (raw.finalExam || raw.exam) {
      var fe = raw.finalExam || raw.exam, fq = Array.isArray(fe) ? fe : arr(fe.questions);
      var exq = fq.map(function (q) { return normQuiz(q, warnings, 'final exam'); }).filter(Boolean);
      if (exq.length) {
        var pm = Array.isArray(fe) ? 70 : Number(fe.passMark), sz = Array.isArray(fe) ? 0 : Number(fe.size);
        course.exam = { title: (!Array.isArray(fe) && s(fe.title).trim()) || 'Final exam', passMark: pm > 0 && pm <= 100 ? Math.round(pm) : 70, size: sz > 0 ? Math.min(Math.round(sz), exq.length) : 0, questions: exq };
      } else warnings.push('"finalExam" has no usable questions; the exam will be built from the chapter quizzes');
    }
    if (raw.sandbox) { var sb = normLab(Object.assign({ type: 'terminal', id: 'sandbox', title: 'Sandbox' }, raw.sandbox), warnings, 'sandbox', 0); if (sb) course.sandbox = sb; }
    if (!course.chapters.length) return { ok: false, errors: ['No usable chapters were found.'], warnings: warnings };
    // every chapter id unique
    var ids = {}; course.chapters.forEach(function (c) { if (ids[c.id]) c.id = c.id + '-' + c.n; ids[c.id] = 1; });
    return { ok: true, errors: [], warnings: warnings, course: course };
  }

  /* ---------- derived views (markdown-ish strings for reading mode and narration) ---------- */
  function mapBlock(m) { return '```conceptmap\ntitle: ' + m.title + '\n' + m.links.join('\n') + '\n```'; }
  function chapterView(ch, course) {
    var ex = [];
    ch.lesson.forEach(function (b) {
      if (b.type === 'text') b.items.forEach(function (t) { ex.push('- ' + t); });
      else if (b.type === 'code') ex.push('```' + b.lang + '\n' + b.code + '\n```');
      else if (b.type === 'figure') ex.push('![' + b.caption + '](images/' + b.image + ')');
      else if (b.type === 'map') ex.push(mapBlock(b.map));
      ex.push('');
    });
    return {
      n: ch.n, id: ch.id, title: ch.title, summary: ch.summary.join('\n\n'), points: ch.keyPoints.map(function (t) { return '- ' + t; }).join('\n'),
      examples: ex.join('\n'), glossary: ch.glossary, cards: ch.cards, maps: ch.maps, quiz: ch.quiz, practice: ch.practice, raw: ch
    };
  }

  /* ---------- starter template ---------- */
  function template() {
    return {
      format: FORMAT, version: VERSION, id: 'my-first-course', title: 'My First Course', subtitle: 'Replace me with your subject', author: 'You',
      chapters: [{
        title: 'Introduction',
        maps: [{ title: 'Big picture', links: ['My subject | has | Topic A', 'My subject | has | Topic B', 'Topic A | leads to | Topic B'] }],
        summary: ['Say in two or three sentences what this chapter teaches.'],
        glossary: [{ term: 'Term', def: 'A short definition.' }],
        keyPoints: ['The first thing to remember.', 'The second thing to remember.'],
        lesson: [{ type: 'text', items: ['A worked point or example.'] }, { type: 'code', lang: 'text', code: 'an example line' }],
        quiz: [{ q: 'Which option is right?', options: ['Wrong', 'Right', 'Wrong too'], answer: 1, explain: 'Why the right one is right.' }],
        cards: [{ q: 'Question for a flashcard?', a: 'Answer.' }],
        practice: [
          { type: 'fill', title: 'Fill the blanks', text: 'The capital of France is {{Paris}}.' },
          { type: 'order', title: 'Put in order', items: ['First', 'Second', 'Third'] },
          { type: 'match', title: 'Match', pairs: [['cat', 'animal'], ['rose', 'plant']] },
          { type: 'write', title: 'Write it', prompt: 'Type the word "hello".', checks: [{ re: 'hello', msg: 'contains hello' }] },
          { type: 'code', title: 'Code it', fn: 'double', intro: 'Write double(n).', starter: 'function double(n) {\n  \n}', tests: [{ args: [2], expect: 4 }, { args: [5], expect: 10 }] }
        ]
      }],
      finalExam: { title: 'Final exam', passMark: 70, questions: [{ q: 'A question that covers the whole course?', options: ['Wrong', 'Right'], answer: 1, explain: 'Why.' }] }
    };
  }

  /* ---------- lab engines ---------- */
  function norm(x) { return s(x).trim().toLowerCase().replace(/\s+/g, ' '); }

  function parseFill(text) {   // -> [{t:'text',v}, {t:'blank',alts:[...]}]
    var out = [], re = /\{\{([^}]+)\}\}/g, last = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > last) out.push({ t: 'text', v: text.slice(last, m.index) });
      out.push({ t: 'blank', alts: m[1].split('|').map(function (a) { return a.trim(); }).filter(Boolean) });
      last = re.lastIndex;
    }
    if (last < text.length) out.push({ t: 'text', v: text.slice(last) });
    return out;
  }
  function checkFill(lab, answers) {
    var segs = parseFill(lab.text), k = 0, msgs = [], pass = true;
    segs.forEach(function (sg) {
      if (sg.t !== 'blank') return;
      var a = answers[k++], ok = sg.alts.some(function (x) { return norm(x) === norm(a); });
      pass = pass && ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + 'blank ' + k + (ok ? '' : ' (not yet)'));
    });
    return { pass: pass, msgs: msgs };
  }
  function checkOrder(lab, seq) {   // seq: array of item texts in the learner's order
    var ok = seq.length === lab.items.length && seq.every(function (x, i) { return x === lab.items[i]; }), msgs = [];
    lab.items.forEach(function (x, i) { var good = seq[i] === x; msgs.push((good ? 'PASS ' : 'FAIL ') + 'position ' + (i + 1)); });
    return { pass: ok, msgs: msgs };
  }
  function checkMatch(lab, choice) {   // choice: right text chosen for each left index
    var pass = true, msgs = [];
    lab.pairs.forEach(function (p, i) { var ok = choice[i] === p[1]; pass = pass && ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + p[0] + (ok ? '' : ' (not yet)')); });
    return { pass: pass, msgs: msgs };
  }
  function checkWrite(lab, text) {
    var pass = true, msgs = [];
    lab.checks.forEach(function (c) {
      var re; try { re = new RegExp(c.re, c.flags === undefined ? 'i' : c.flags); } catch (e) { msgs.push('ERROR bad pattern: ' + c.re); pass = false; return; }
      var hit = re.test(text), ok = c.not ? !hit : hit;
      pass = pass && ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + c.msg);
    });
    return { pass: pass, msgs: msgs };
  }

  function same(a, b, tol) {
    if (typeof a === 'number' && typeof b === 'number') return tol ? Math.abs(a - b) <= tol : a === b;
    return JSON.stringify(a) === JSON.stringify(b);
  }
  function runCodeSync(lab, code) {
    try {
      var v, msgs = [], pass = true;
      var helpers = lab.helpersJs ? new Function(lab.helpersJs + '\nreturn {' + (lab.helpersJs.match(/function\s+(\w+)/g) || []).map(function (m) { var n = m.split(/\s+/)[1]; return n + ':' + n; }).join(',') + '};')() : {};
      if (lab.isBody) v = new Function(code)();
      else v = new Function(code + '\nreturn ' + lab.fn + ';')();
      if (lab.tests && lab.tests.length && !lab.isBody) {
        if (typeof v !== 'function') return { pass: false, msgs: ['FAIL ' + lab.fn + ' is not a function'] };
        lab.tests.forEach(function (t) {
          var got = v.apply(null, JSON.parse(JSON.stringify(t.args || [])));
          var ok = same(got, t.expect, t.approx);
          pass = pass && ok;
          msgs.push((ok ? 'PASS ' : 'FAIL ') + (t.label || lab.fn + '(' + (t.args || []).map(function (a) { return JSON.stringify(a); }).join(', ') + ')') + ' = ' + JSON.stringify(got) + (ok ? '' : ' (expected ' + JSON.stringify(t.expect) + ')'));
        });
      }
      if (lab.checkJs) {
        var r = new Function('result', 'helpers', lab.checkJs)(v, helpers);
        if (r && typeof r === 'object') { pass = pass && !!r.pass; msgs = msgs.concat(arr(r.msgs)); }
      }
      return { pass: pass, msgs: msgs };
    } catch (e) {
      return { pass: false, msgs: ['ERROR ' + (e && e.message ? e.message : String(e))] };
    }
  }
  /* run user code in a Worker with a time limit so an endless loop cannot freeze the app */
  function runCode(lab, code, timeoutMs) {
    timeoutMs = timeoutMs || 3000;
    return new Promise(function (resolve) {
      if (typeof Worker === 'undefined' || typeof Blob === 'undefined' || typeof URL === 'undefined' || !URL.createObjectURL) { resolve(runCodeSync(lab, code)); return; }
      var w, url, done = false;
      function finish(r) { if (done) return; done = true; try { w.terminate(); } catch (e) {} try { URL.revokeObjectURL(url); } catch (e) {} resolve(r); }
      try {
        var src = 'var same=' + same.toString() + ',arr=' + arr.toString() + ';\nvar runCodeSync=' + runCodeSync.toString() + ';\nonmessage=function(e){postMessage(runCodeSync(e.data.lab,e.data.code));};';
        url = URL.createObjectURL(new Blob([src], { type: 'text/javascript' }));
        w = new Worker(url);
        w.onmessage = function (e) { finish(e.data); };
        w.onerror = function () { finish(runCodeSync(lab, code)); };
        setTimeout(function () { finish({ pass: false, msgs: ['ERROR your code ran longer than ' + (timeoutMs / 1000) + ' seconds (endless loop?)'] }); }, timeoutMs);
        w.postMessage({ lab: lab, code: code });
      } catch (e) { resolve(runCodeSync(lab, code)); }
    });
  }

  /* ----- Python labs: MicroPython (WebAssembly) in a Worker ----- */
  /* The core takes an already loaded MicroPython instance, so Node tests and the Worker share it. */
  async function runPythonCore(mp, lab, code, out, outputOnly) {
    var msgs = [], pass = true;
    function trim(m) { m = String(m || '').split('\n').filter(function (x) { return x.trim(); }); return m.slice(-4).join(' | '); }
    function printed() { return out.slice(0, 40).map(function (l) { return 'OUT ' + l; }); }
    try { mp.runPython(code); } catch (e) { return { pass: false, msgs: printed().concat(['ERROR ' + trim(e && e.message ? e.message : e)]) }; }
    if (outputOnly) return { pass: null, msgs: out.length ? printed() : ['(the code printed nothing)'] };
    var text = out.join('\n');
    (lab.checks || []).forEach(function (c) {
      var hit = new RegExp(c.re, c.flags || 'i').test(text);
      var ok = c.not ? !hit : hit; pass = pass && ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + c.msg);
    });
    if (lab.fn && lab.tests && lab.tests.length) {
      var argsJson = JSON.stringify(JSON.stringify(lab.tests.map(function (t) { return t.args || []; })));
      var h = 'import json\n_t = json.loads(' + argsJson + ')\n_o = []\nfor _a in _t:\n    try:\n        _o.append(["ok", json.dumps(' + lab.fn + '(*_a))])\n    except Exception as _e:\n        _o.append(["err", repr(_e)])\n_res = json.dumps(_o)\n';
      var res;
      try { mp.runPython(h); res = JSON.parse(mp.globals.get('_res')); } catch (e) { return { pass: false, msgs: msgs.concat(['ERROR ' + trim(e && e.message ? e.message : e)]) }; }
      lab.tests.forEach(function (t, i) {
        var label = t.label || lab.fn + '(' + (t.args || []).map(function (a) { return JSON.stringify(a); }).join(', ') + ')';
        if (res[i][0] === 'err') { pass = false; msgs.push('FAIL ' + label + ' raised ' + res[i][1]); return; }
        var got = JSON.parse(res[i][1]), ok = same(got, t.expect, t.approx);
        pass = pass && ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + label + ' = ' + JSON.stringify(got) + (ok ? '' : ' (expected ' + JSON.stringify(t.expect) + ')'));
      });
    }
    return { pass: pass, msgs: printed().slice(0, 12).concat(msgs) };
  }
  var pyWasm = null;
  function runPython(lab, code, opts) {
    opts = opts || {};
    return new Promise(function (resolve) {
      var MP = typeof window !== 'undefined' ? window.LilithMP : null;
      if (!MP || typeof Worker === 'undefined' || typeof Blob === 'undefined') { resolve({ pass: false, msgs: ['ERROR Python is not available in this build'] }); return; }
      var w, url, done = false;
      function finish(r) { if (done) return; done = true; try { w.terminate(); } catch (e) {} try { URL.revokeObjectURL(url); } catch (e) {} resolve(r); }
      try {
        if (!pyWasm) { var bin = atob(MP.wasm), u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); pyWasm = u.buffer; }
        var glue = '\nvar same=' + same.toString() + ',arr=' + arr.toString() + ';\nvar runPythonCore=' + runPythonCore.toString() + ';\n' +
          'onmessage=async function(e){var out=[];try{var wurl=URL.createObjectURL(new Blob([e.data.wasm],{type:\'application/wasm\'}));var mp=await loadMicroPython({url:wurl,heapsize:8*1024*1024,stdout:function(s){out.push(s)},stderr:function(s){out.push(s)}});postMessage(await runPythonCore(mp,e.data.lab,e.data.code,out,e.data.outputOnly));}catch(err){postMessage({pass:false,msgs:["ERROR "+String(err&&err.message||err)]});}};';
        url = URL.createObjectURL(new Blob([MP.mjs + glue], { type: 'text/javascript' }));
        w = new Worker(url);
        w.onmessage = function (e) { finish(e.data); };
        w.onerror = function (e) { finish({ pass: false, msgs: ['ERROR Python could not start on this device'] }); };
        setTimeout(function () { finish({ pass: false, msgs: ['ERROR your code ran longer than 8 seconds (endless loop?)'] }); }, 8000);
        w.postMessage({ lab: lab, code: code, outputOnly: !!opts.outputOnly, wasm: pyWasm.slice(0) });
      } catch (e) { finish({ pass: false, msgs: ['ERROR ' + (e && e.message ? e.message : e)] }); }
    });
  }

  /* ----- scripted terminal: data-driven shell for any subject ----- */
  function subst(t, vars, caps) {
    return s(t).replace(/\{\{(\w+)\}\}/g, function (m, k) {
      if (/^\d+$/.test(k)) return caps && caps[+k] !== undefined ? caps[+k] : '';
      return vars[k] !== undefined ? vars[k] : '';
    });
  }
  function condOk(c, vars) {
    var ok = true;
    if (c.when) Object.keys(c.when).forEach(function (k) { if (String(vars[k]) !== String(c.when[k])) ok = false; });
    if (c.unless) Object.keys(c.unless).forEach(function (k) { if (String(vars[k]) === String(c.unless[k])) ok = false; });
    return ok;
  }
  function makeScriptTerm(lab) {
    var S = { vars: JSON.parse(JSON.stringify(lab.vars || {})), hist: [], done: {} };
    var cmds = lab.commands.map(function (c) { var re; try { re = new RegExp(c.re, c.flags === undefined ? '' : c.flags); } catch (e) { re = null; } return { c: c, re: re }; });
    var tasks = (lab.tasks || []).map(function (t, i) { var re; try { re = new RegExp(t.cmd, t.flags || ''); } catch (e) { re = null; } return { id: t.id || ('t' + i), text: t.text, re: re }; });
    function L(t, c) { return { t: t, c: c || '' }; }
    function builtin(line) {
      if (line === 'help' || line === '?') {
        var r = [L(lab.intro || 'Type commands. Builtins: help, tasks, hint, history, clear.', 'dim')];
        if (lab.chips && lab.chips.length) r.push(L('Try: ' + lab.chips.slice(0, 6).join('   '), 'dim'));
        return r;
      }
      if (line === 'tasks' || line === 'missions') return [L('Tasks:', 'dim')].concat(tasks.map(function (t) { return L((S.done[t.id] ? '[x] ' : '[ ] ') + t.text, S.done[t.id] ? 'ok' : ''); }));
      if (line === 'hint') {
        for (var i = 0; i < tasks.length; i++) if (!S.done[tasks[i].id]) return [L('Next task: ' + tasks[i].text, 'warn')];
        return [L(tasks.length ? 'All tasks done.' : 'No hints for this terminal.', 'ok')];
      }
      if (line === 'history') return S.hist.map(function (h, i) { return L(String(i + 1) + '  ' + h); });
      if (line === 'clear') return 'CLEAR';
      return null;
    }
    function runOne(seg) {
      seg = seg.trim(); if (!seg) return [];
      var b = builtin(seg); if (b) return b;
      for (var i = 0; i < cmds.length; i++) {
        var k = cmds[i]; if (!k.re) continue;
        var m = k.re.exec(seg); if (!m || !condOk(k.c, S.vars)) continue;
        var lines = Array.isArray(k.c.out) ? k.c.out : (k.c.out === undefined ? [] : [k.c.out]);
        if (k.c.set) Object.keys(k.c.set).forEach(function (v) { S.vars[v] = subst(k.c.set[v], S.vars, m); });
        return lines.map(function (x) { return L(subst(x, S.vars, m), k.c.cls || ''); });
      }
      return [L(subst(lab.notFound || '{{0}}: command not found. Type help.', S.vars, [seg.split(/\s+/)[0]]).replace('{{0}}', seg.split(/\s+/)[0]), 'err')];
    }
    function pipeSplit(seg) { return seg.replace(/\s2>&1/g, '').split(/\s*\|\s*/); }
    function runPiped(seg) {
      var parts = pipeSplit(seg), res = runOne(parts[0]);
      if (res === 'CLEAR') return res;
      for (var p = 1; p < parts.length; p++) {
        var a = parts[p].match(/"[^"]*"|'[^']*'|\S+/g) || [], c = a.shift();
        if (c === 'grep') {
          var ic = a.indexOf('-i') >= 0; a = a.filter(function (x) { return x[0] !== '-'; });
          var re = new RegExp((a[0] || '').replace(/^["']|["']$/g, '').replace(/[.+^${}()[\]\\]/g, '\\$&'), ic ? 'i' : '');
          res = res.filter(function (x) { return re.test(x.t); });
        } else if (c === 'head' || c === 'tail') {
          var nn = parseInt((a.filter(function (x) { return /^-?\d+$/.test(x); })[0] || '10').replace('-', ''), 10);
          res = c === 'head' ? res.slice(0, nn) : res.slice(-nn);
        } else if (c === 'wc') res = [L(String(res.length))];
        else if (c === 'tee') { /* pass through */ }
        else res = res.concat([L(c + ': this pipe command is not supported in the simulation', 'warn')]);
      }
      return res;
    }
    function exec(line) {
      line = s(line).trim(); if (line) S.hist.push(line);
      var all = [], fin = [];
      var segs = line.split(/\s*(?:;|&&)\s*/);
      for (var i = 0; i < segs.length; i++) {
        var r = runPiped(segs[i]); if (r === 'CLEAR') return 'CLEAR';
        all = all.concat(r);
      }
      tasks.forEach(function (t) {
        if (S.done[t.id] || !t.re) return;
        if (segs.concat([line]).some(function (x) { var y = x.replace(/\s2>&1/g, '').trim(); return t.re.test(y) || t.re.test(y.split('|')[0].trim()); })) { S.done[t.id] = true; fin.push(L('Task done: ' + t.text, 'ok')); }
      });
      return all.concat(fin);
    }
    return { exec: exec, state: S, tasks: tasks };
  }

  var api = { FORMAT: FORMAT, VERSION: VERSION, LAB_TYPES: LAB_TYPES, validate: validate, chapterView: chapterView, template: template, slug: slug,
    parseFill: parseFill, checkFill: checkFill, checkOrder: checkOrder, checkMatch: checkMatch, checkWrite: checkWrite, runCode: runCode, runCodeSync: runCodeSync, runPython: runPython, runPythonCore: runPythonCore, makeScriptTerm: makeScriptTerm, mapBlock: mapBlock };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LilithCourse = api;
})(typeof window !== 'undefined' ? window : globalThis);
