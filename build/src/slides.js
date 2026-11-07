/* Lecture builder: turns a chapter into an animated slide deck plus a narration script.
   Chapter order: title, concept map tour, summary, glossary, key points, lesson, quiz, practice, end.
   Pure functions. Depends on narrate.js (LilithNarrate) and maps.js (LilithMaps). */
(function (root) {
  'use strict';
  var N = (typeof require !== 'undefined' && typeof module !== 'undefined') ? require('./narrate.js') : root.LilithNarrate;
  var M = (typeof require !== 'undefined' && typeof module !== 'undefined') ? require('./maps.js') : root.LilithMaps;

  /* split "Label: detail" or the first clause into a short headline and a detail */
  function headline(text) {
    var t = N.plain(text), m;
    m = /^([^:]{2,60}):\s+(.+)$/.exec(t);
    if (m && !/^(e\.g|i\.e)/i.test(m[1])) return { head: m[1], detail: m[2] };
    m = /^(.{12,80}?[.;])\s+(.+)$/.exec(t);
    if (m) return { head: m[1].replace(/[.;]$/, ''), detail: m[2] };
    if (t.length > 90) {
      var cut = t.lastIndexOf(' ', 70); if (cut < 30) cut = 70;
      return { head: t.slice(0, cut) + '...', detail: t.slice(cut).trim() };
    }
    return { head: t, detail: '' };
  }

  function buildLecture(ch, opts) {
    opts = opts || {};
    var slides = [], chunks = [];
    function slide(o) { o.steps = 0; slides.push(o); return slides.length - 1; }
    function say(si, step, label, shown, extra) {
      var spoken = N.speakable(shown);
      if (!spoken && !(extra && (extra.wait || extra.hold))) return;
      var c = { slide: si, step: step, label: label, text: spoken, shown: N.plain(shown), emotion: N.emotionFor(shown, label) };
      if (extra) for (var k in extra) c[k] = extra[k];
      chunks.push(c);
      if (slides[si].steps < step + 1) slides[si].steps = step + 1;
    }
    function bulletSlides(stage, heading, items, label) {
      var per = 4, parts = Math.max(1, Math.ceil(items.length / per));
      for (var p = 0; p < parts; p++) {
        var part = items.slice(p * per, p * per + per);
        var si = slide({ type: 'bullets', stage: stage, heading: heading + (parts > 1 ? ' (' + (p + 1) + '/' + parts + ')' : ''), bullets: part.map(function (t) { var h = headline(t); h.raw = t; return h; }) });
        part.forEach(function (t, i) { say(si, i, label, t); });
      }
    }

    var s0 = slide({ type: 'title', stage: 'title', heading: ch.title, sub: (opts.label || 'Chapter') + ' ' + ch.n });
    say(s0, 0, 'Chapter', (opts.label || 'Chapter') + ' ' + ch.n + '. ' + ch.title + '.');

    // 1. concept map tour (animated edge by edge)
    (ch.maps || []).forEach(function (mp, mi) {
      var map = M.parseMaps(require_mapblock(mp))[0]; if (!map) return;
      var L = M.layout(map);
      var si = slide({ type: 'map', stage: 'map', heading: 'Concept map' + (ch.maps.length > 1 ? ' ' + (mi + 1) + '/' + ch.maps.length : '') + ': ' + map.title, layout: L, map: { title: map.title } });
      say(si, 0, 'Concept map', 'Here is the concept map for this chapter: ' + map.title + '. Follow the links.', { edge: -1 });
      map.edges.forEach(function (e, i) { say(si, i + 1, 'Concept map', e.from.replace(/\s*\[ch\d+\]/, '') + ', ' + e.rel + ', ' + e.to.replace(/\s*\[ch\d+\]/, ''), { edge: i }); });
    });

    // 2. summary
    var sums = [];
    (ch.raw.summary || []).forEach(function (t) { N.sentences(t).forEach(function (x) { sums.push(x); }); });
    if (sums.length > 5) sums = sums.slice(0, 4).concat([sums.slice(4).join(' ')]);
    if (sums.length) bulletSlides('summary', 'The big idea', sums, 'Summary');

    // 3. glossary
    var terms = ch.glossary || [], per = 5;
    for (var g = 0; g < terms.length; g += per) {
      var part = terms.slice(g, g + per);
      var gi = slide({ type: 'bullets', stage: 'glossary', heading: 'Glossary ' + (Math.floor(g / per) + 1) + '/' + Math.ceil(terms.length / per), bullets: part.map(function (t) { return { head: t.term, detail: N.plain(t.def), raw: t.term + '. ' + t.def }; }) });
      part.forEach(function (t, i) { say(gi, i, 'Glossary', t.term + '. ' + t.def); });
    }

    // 4. key points
    var pts = ch.raw.keyPoints || [];
    if (pts.length) bulletSlides('points', 'Key points', pts, 'Key points');

    // 5. lesson: figures, text, code, extra maps
    var textBuf = [];
    function flushText() { if (textBuf.length) { bulletSlides('lesson', 'Worth knowing', textBuf, 'Lesson'); textBuf = []; } }
    (ch.raw.lesson || []).forEach(function (b) {
      if (b.type === 'figure') {
        flushText();
        var fi = slide({ type: 'figure', stage: 'lesson', heading: 'Figure', file: b.image, caption: b.caption }); say(fi, 0, 'Figure', b.caption || 'A figure.');
      } else if (b.type === 'code') {
        flushText();
        var lines = b.code.split('\n'), per2 = 12, np = Math.ceil(lines.length / per2);
        for (var c = 0; c < np; c++) {
          var ci = slide({ type: 'code', stage: 'lesson', heading: 'Example' + (np > 1 ? ' (' + (c + 1) + '/' + np + ')' : '') + ': ' + (b.lang || 'text'), lang: b.lang || 'text', code: lines.slice(c * per2, c * per2 + per2).join('\n') });
          if (opts.readCode) say(ci, 0, 'Code', 'Code example. ' + lines.slice(c * per2, c * per2 + per2).join('. '));
          else say(ci, 0, 'Code', c === 0 ? 'Here is an example. Read it on screen, or turn on read code in settings.' : 'The example continues.');
        }
      } else if (b.type === 'map') {
        flushText();
        var map2 = M.parseMaps(require_mapblock(b.map))[0];
        if (map2) {
          var L2 = M.layout(map2);
          var mi2 = slide({ type: 'map', stage: 'lesson', heading: 'Concept map: ' + map2.title, layout: L2, map: { title: map2.title } });
          map2.edges.forEach(function (e, i) { say(mi2, i, 'Concept map', e.from.replace(/\s*\[ch\d+\]/, '') + ', ' + e.rel + ', ' + e.to.replace(/\s*\[ch\d+\]/, ''), { edge: i }); });
        }
      } else if (b.type === 'text') b.items.forEach(function (t) { textBuf.push(t); });
    });
    flushText();

    // 6. quiz: interactive, the narrator waits for the answer
    var quiz = ch.quiz || [];
    quiz.forEach(function (q, i) {
      var qi = slide({ type: 'quiz', stage: 'quiz', heading: 'Quiz ' + (i + 1) + '/' + quiz.length, q: N.plain(q.q), options: q.options.map(N.plain), answer: q.answer, explain: N.plain(q.explain || ''), qi: i, total: quiz.length });
      var letters = 'ABCDEFGH', spoken = q.q + ' ' + q.options.map(function (o, k) { return 'Option ' + letters[k] + '. ' + o + '.'; }).join(' ');
      say(qi, 0, 'Question', spoken, { hold: true, shown: q.q });
      chunks.push({ slide: qi, step: 1, label: 'Answer', text: '', shown: '', emotion: 'neutral', feedback: true });   // filled in after the learner answers
      slides[qi].steps = 2;
    });

    // 7. practice: opens the labs for this chapter
    if ((ch.practice || []).length) {
      var pi = slide({ type: 'practice', stage: 'practice', heading: 'Practice time', labs: ch.practice.map(function (l) { return { id: l.id, title: l.title, kind: l.type }; }) });
      say(pi, 0, 'Practice', 'Practice time. This chapter has ' + ch.practice.length + (ch.practice.length === 1 ? ' exercise' : ' exercises') + '. Tap one to try it, then come back.', { hold: true });
    }

    var ei = slide({ type: 'end', stage: 'end', heading: (opts.label || 'Chapter') + ' ' + ch.n + ' complete', sub: ch.title });
    say(ei, 0, 'Chapter', 'That is the end of ' + (opts.label || 'chapter').toLowerCase() + ' ' + ch.n + '.');
    return { slides: slides, chunks: chunks };
  }

  function require_mapblock(m) { return '```conceptmap\ntitle: ' + m.title + '\n' + m.links.join('\n') + '\n```'; }

  /* index of the first chunk of each slide, for the slide dots */
  function slideStarts(lec) {
    var first = {}; lec.chunks.forEach(function (c, i) { if (first[c.slide] === undefined) first[c.slide] = i; });
    return first;
  }

  var api = { buildLecture: buildLecture, headline: headline, slideStarts: slideStarts };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LilithSlides = api;
})(typeof window !== 'undefined' ? window : globalThis);
