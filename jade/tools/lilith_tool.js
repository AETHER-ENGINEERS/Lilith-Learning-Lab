#!/usr/bin/env node
/* lilith_tool.js - Jade's helper for Lilith Learning Lab course files (JSON, format "lilith-course").
   Zero dependencies. Options are key=value (no --flags). lilith_course.js must sit next to this file (used for validation).
   Courses are found with course=<file>, else env LILITH_COURSES (a folder), else ./courses, else /Jade/Courses. */
'use strict';
const fs = require('fs'), path = require('path');
const die = m => { console.error('error: ' + m); process.exit(1); };
function opts(args) { const o = { _: [] }; args.forEach(a => { const m = /^([A-Za-z_]+)=([\s\S]*)$/.exec(a); if (m) o[m[1]] = m[2]; else o._.push(a); }); return o; }
function K() { try { return require(path.join(__dirname, 'lilith_course.js')).LilithCourse || require(path.join(__dirname, 'lilith_course.js')); } catch (e) { die('lilith_course.js must be next to this script (' + e.message + ')'); } }
function dirs() { return [process.env.LILITH_COURSES, path.join(process.cwd(), 'courses'), '/Jade/Courses', path.join(__dirname, '..', 'courses')].filter(Boolean); }
function files() { const out = []; dirs().forEach(d => { try { fs.readdirSync(d).forEach(f => { if (/\.json$/i.test(f)) out.push(path.join(d, f)); }); } catch (e) {} }); return out; }
function load(o) {
  let f = o.course;
  if (f && !fs.existsSync(f)) { const m = files().find(x => path.basename(x).toLowerCase().includes(f.toLowerCase())); if (m) f = m; }
  if (!f) { const all = files(); if (all.length === 1) f = all[0]; else die('say which course: course=<file or part of its name>. Found: ' + (all.map(x => path.basename(x)).join(', ') || 'none')); }
  if (!fs.existsSync(f)) die('no such course file: ' + f);
  const v = K().validate(fs.readFileSync(f, 'utf8'));
  if (!v.ok) die('invalid course: ' + v.errors.join('; '));
  return v.course;
}
const clip = (s, n) => s.length > n ? s.slice(0, n) + ' ...' : s;
const tok = s => (String(s).toLowerCase().match(/[a-z0-9_.+-]+/g) || []).filter(w => w.length > 1);
function docs(c) {
  const d = [];
  c.chapters.forEach(ch => {
    const parts = [['summary', ch.summary.join('\n')], ['key points', ch.keyPoints.join('\n')], ['glossary', ch.glossary.map(g => g.term + ': ' + g.def).join('\n')],
      ['lesson', ch.lesson.map(b => b.type === 'text' ? (b.items || []).join('\n') : b.type === 'code' ? b.code : '').join('\n')],
      ['quiz', ch.quiz.map(q => q.q + ' ' + q.options[q.answer] + ' ' + q.explain).join('\n')], ['cards', ch.cards.map(x => x.q + ' ' + x.a).join('\n')]];
    parts.forEach(([part, t]) => { if (!t) return; const w = tok(ch.title + ' ' + t); d.push({ ch, part, t, w, tf: w.reduce((m, x) => (m[x] = (m[x] || 0) + 1, m), {}) }); });
  });
  return d;
}
function search(c, q, k) {
  const D = docs(c), N = D.length, avg = D.reduce((a, d) => a + d.w.length, 0) / (N || 1), qs = tok(q), df = {};
  qs.forEach(t => { df[t] = D.filter(d => d.tf[t]).length; });
  D.forEach(d => { d.score = 0; qs.forEach(t => { const f = d.tf[t] || 0; if (!f) return; d.score += Math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5)) * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * d.w.length / avg)); }); if (qs.length && tok(d.ch.title).some(x => qs.includes(x))) d.score *= 1.3; });
  return D.filter(d => d.score > 0).sort((a, b) => b.score - a.score).slice(0, k);
}
const HELP = ['lilith_tool.js <command> course=<file> key=value ...',
  '  list                          list course files found',
  '  validate file.json            check a course file and print warnings (use before giving one to the user)',
  '  template                      print an empty course to fill in',
  '  toc                           chapters with counts of quiz questions and labs',
  '  search "words" k=5            BM25 search across summaries, points, glossary, lessons, quizzes',
  '  chapter 3 part=summary|points|glossary|lesson|quiz|labs|map|all',
  '  glossary "term"               look up a term across the course',
  '  quiz n=5 chapter=3 answers=yes   quiz questions (whole course unless chapter=)',
  '  exam n=20                     a final-exam style set drawn from all chapters (uses finalExam if the course has one)'].join('\n');
function main() {
  const [cmd, ...rest] = process.argv.slice(2), o = opts(rest);
  if (!cmd || cmd === 'help') return console.log(HELP);
  if (cmd === 'template') return console.log(JSON.stringify(K().template(), null, 2));
  if (cmd === 'list') { files().forEach(f => { try { const j = JSON.parse(fs.readFileSync(f, 'utf8')); console.log(path.basename(f) + '  ' + (j.title || '?') + '  (' + (j.chapters || []).length + ' chapters)'); } catch (e) { console.log(path.basename(f) + '  (not valid JSON)'); } }); return; }
  if (cmd === 'validate') {
    const f = o._[0]; if (!f) die('usage: validate file.json');
    let v; try { v = K().validate(fs.readFileSync(f, 'utf8')); } catch (e) { die(e.message); }
    if (!v.ok) { console.log('INVALID'); v.errors.forEach(e => console.log(' - ' + e)); process.exit(1); }
    const c = v.course; console.log('OK: "' + c.title + '" ' + c.chapters.length + ' chapters, ' + c.chapters.reduce((a, x) => a + x.quiz.length, 0) + ' quiz questions, ' + c.chapters.reduce((a, x) => a + x.practice.length, 0) + ' labs' + (c.exam ? ', final exam of ' + c.exam.questions.length : ', no finalExam (the app builds one from the chapter quizzes)'));
    v.warnings.forEach(w => console.log(' note: ' + w)); return;
  }
  const c = load(o);
  switch (cmd) {
    case 'toc': console.log(c.title + (c.subtitle ? ' - ' + c.subtitle : '')); c.chapters.forEach(h => console.log(h.n + '. ' + h.title + '  [' + h.quiz.length + ' quiz, ' + h.practice.length + ' labs, ' + h.maps.length + ' maps]')); break;
    case 'search': { const q = o._.join(' '); if (!q) die('usage: search "words"'); const hits = search(c, q, +(o.k || 5)); if (!hits.length) return console.log('No match in this course. Say so plainly instead of guessing.'); hits.forEach((h, i) => console.log('[' + (i + 1) + '] chapter ' + h.ch.n + ' "' + h.ch.title + '" / ' + h.part + '  (' + h.score.toFixed(2) + ')\n    ' + clip(h.t.replace(/\s+/g, ' '), 260))); break; }
    case 'chapter': {
      const n = +o._[0], h = c.chapters.find(x => x.n === n); if (!h) die('no chapter ' + o._[0] + ' (try toc)'); const p = o.part || 'summary', all = p === 'all';
      console.log('# ' + h.n + '. ' + h.title);
      if (p === 'map' || all) h.maps.forEach(m => console.log('\n## Concept map: ' + m.title + '\n' + m.links.join('\n')));
      if (p === 'summary' || all) console.log('\n## Summary\n' + h.summary.join('\n'));
      if (p === 'glossary' || all) console.log('\n## Glossary\n' + h.glossary.map(g => '- ' + g.term + ': ' + g.def).join('\n'));
      if (p === 'points' || all) console.log('\n## Key points\n' + h.keyPoints.map(x => '- ' + x).join('\n'));
      if (p === 'lesson' || all) console.log('\n## Lesson\n' + h.lesson.map(b => b.type === 'text' ? (b.items || []).join('\n') : b.type === 'code' ? '```' + (b.lang || '') + '\n' + b.code + '\n```' : '[' + b.type + ']').join('\n\n'));
      if (p === 'quiz' || all) console.log('\n## Quiz\n' + h.quiz.map((q, i) => (i + 1) + '. ' + q.q + '\n   ' + q.options.map((x, k) => 'ABCDEFGH'[k] + ') ' + x).join('  ') + '\n   Answer: ' + 'ABCDEFGH'[q.answer] + '. ' + q.explain).join('\n'));
      if (p === 'labs' || all) console.log('\n## Practice labs\n' + h.practice.map(l => '- ' + l.id + ' [' + l.type + '] ' + l.title).join('\n'));
      break;
    }
    case 'glossary': { const q = o._.join(' ').toLowerCase(); let n = 0; c.chapters.forEach(h => h.glossary.forEach(g => { if (n < 12 && (!q || (g.term + ' ' + g.def).toLowerCase().includes(q))) { console.log(g.term + ' (ch ' + h.n + '): ' + g.def); n++; } })); if (!n) console.log('Term not in the glossary.'); break; }
    case 'quiz': case 'exam': {
      let qs = []; if (cmd === 'exam' && c.exam) c.exam.questions.forEach(q => qs.push(Object.assign({ n: '-' }, q)));
      else c.chapters.forEach(h => { if (!o.chapter || +o.chapter === h.n) h.quiz.forEach(q => qs.push(Object.assign({ n: h.n }, q))); });
      qs = qs.sort(() => Math.random() - 0.5).slice(0, +(o.n || (cmd === 'exam' ? 20 : 5)));
      qs.forEach((q, i) => console.log((i + 1) + '. (ch ' + q.n + ') ' + q.q + '\n   ' + q.options.map((x, k) => 'ABCDEFGH'[k] + ') ' + x).join('  ') + (o.answers === 'yes' ? '\n   Answer: ' + 'ABCDEFGH'[q.answer] + '. ' + q.explain : '')));
      break;
    }
    default: die('unknown command "' + cmd + '". Try: help');
  }
}
main();
