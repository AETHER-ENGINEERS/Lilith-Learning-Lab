/* Narration for Lilith Learning Lab: speech-friendly text, chunking, emotion tags,
   a playback engine (play/pause/next/prev/rate), speech backends (Android native bridge,
   Web Speech, silent read-along) and the avatar frame controller. No DOM access except in makeEnv(). */
(function (root) {
  'use strict';

  /* ---------- speech-friendly text ---------- */
  var SAY = [   // generic computing words; course-specific ones come from the course's "pronounce" map
    ['GPU', 'G P U'], ['CPU', 'C P U'], ['USB', 'U S B'], ['RAM', 'ram'], ['SDK', 'S D K'], ['API', 'A P I'], ['PDF', 'P D F'], ['HTML', 'H T M L'], ['JSON', 'jay son']
  ];
  var CUSTOM = [];
  function setPronounce(map) {
    CUSTOM = Object.keys(map || {}).sort(function (x, y) { return y.length - x.length; }).map(function (k) { return [k, String(map[k])]; });
  }

  function speakable(s) {
    s = String(s);
    s = s.replace(/!\[([^\]]*)\]\([^)]*\)/g, 'Figure: $1.');
    s = s.replace(/\[ch(\d+)\]/g, '');
    s = s.replace(/\*\*([^*]+)\*\*/g, '$1');
    s = s.replace(/\|\|([^|]+)\|\|\^2/g, 'the squared norm of $1');
    s = s.replace(/`([^`]+)`/g, '$1');
    s = s.replace(/->|=>|→/g, ' to ');
    s = s.replace(/(^|\s)--(\w)/g, '$1dash dash $2');
    s = s.replace(/(^|\s)-([a-zA-Z])/g, '$1dash $2');
    s = s.replace(/\b(\w+)\.(onnx|engine|cu|py|md|json|txt|xdc|toml|html)\b/g, '$1 dot $2');
    s = s.replace(/GB\/s/g, ' gigabytes per second').replace(/(\d)\s?MHz/g, '$1 megahertz').replace(/(\d)\s?GB\b/g, '$1 gigabytes').replace(/(\d)\s?MB\b/g, '$1 megabytes');
    s = s.replace(/(\d)\s?W\b/g, '$1 watts').replace(/(\d)\s?ms\b/g, '$1 milliseconds');
    s = s.replace(/\bI\/O\b/g, 'I O').replace(/(\w)\/(\w)/g, '$1 slash $2').replace(/\//g, ' slash ');
    s = s.replace(/(\d)x(?=\W|$)/g, '$1 times').replace(/×/g, ' by ').replace(/~/g, 'about ').replace(/%/g, ' percent');
    s = s.replace(/\bsm_(\d+)\b/g, 'S M $1').replace(/_/g, ' ').replace(/[#$*]/g, ' ').replace(/&/g, ' and ');
    CUSTOM.forEach(function (p) { s = s.split(p[0]).join(p[1]); });
    SAY.forEach(function (p) { s = s.split(p[0]).join(p[1]); });
    return s.replace(/\s+/g, ' ').trim();
  }

  function plain(s) {
    return String(s).replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/\[ch(\d+)\]/g, '').replace(/\*\*([^*]+)\*\*/g, '$1').replace(/`([^`]+)`/g, '$1').replace(/\s+/g, ' ').trim();
  }

  function emotionFor(text, label) {
    if (label === 'Answer' || label === 'Correct') return 'happy';
    if (label === 'Not quite') return 'sad';
    if (/\(from memory|not re-checked|unverified|double-check|confirm in the/i.test(text)) return 'shy';
    if (/end[- ]of[- ]life|discontinued|no longer (supported|available|maintained)|deprecated/i.test(text)) return 'sad';
    if (/\b(fail|fails|error|stall|crash|brownouts?|reboots?|throttl\w*|out of memory|killed|hangs?|mistake|warning|wrong)\b/i.test(text)) return 'mad';
    if (/\b(easiest|best|good|great|nice|recommended|safe|reliable|well documented|well)\b/i.test(text)) return 'happy';
    return 'neutral';
  }

  function sentences(text) {
    return text.replace(/([.!?])\s+/g, '$1\u0001').split('\u0001').map(function (x) { return x.trim(); }).filter(Boolean);
  }
  function pieces(sn, max) {
    if (sn.length <= max) return [sn];
    var parts = sn.split(/([,;:]\s)/), out = [], cur = '';
    for (var i = 0; i < parts.length; i++) {
      if (cur && (cur + parts[i]).length > max) { out.push(cur.trim()); cur = parts[i]; } else cur += parts[i];
    }
    if (cur.trim()) out.push(cur.trim());
    var res = [];
    out.forEach(function (p) {
      while (p.length > max) { var k = p.lastIndexOf(' ', max); if (k < 40) k = max; res.push(p.slice(0, k).trim()); p = p.slice(k); }
      if (p.trim()) res.push(p.trim());
    });
    return res;
  }
  function group(text, max) {
    var out = [], cur = '';
    sentences(text).forEach(function (sn) {
      pieces(sn, max).forEach(function (pc) {
        if (cur && (cur + ' ' + pc).length > max) { out.push(cur); cur = pc; } else cur = cur ? cur + ' ' + pc : pc;
      });
    });
    if (cur) out.push(cur);
    return out;
  }

  /* split a markdown section into blocks: {type:'p'|'li'|'code'|'img', text} */
  function blocks(md) {
    var lines = String(md || '').split('\n'), out = [], i = 0, para = [];
    function flush() { if (para.length) { out.push({ type: 'p', text: para.join(' ') }); para = []; } }
    while (i < lines.length) {
      var ln = lines[i], f = /^```(\w*)/.exec(ln);
      if (f) {
        flush(); var buf = []; i++;
        while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
        out.push({ type: 'code', lang: f[1], text: buf.join('\n') });
      } else if (/^!\[/.test(ln.trim())) { flush(); out.push({ type: 'img', text: ln.trim() }); }
      else if (/^\s*-\s+/.test(ln)) { flush(); out.push({ type: 'li', text: ln.replace(/^\s*-\s+/, '') }); }
      else if (!ln.trim()) flush();
      else para.push(ln.trim());
      i++;
    }
    flush();
    return out;
  }

  /* ---------- chunks for a chapter ---------- */
  function buildChunks(ch, opts) {
    opts = opts || {};
    var out = [], MAX = 230, label = opts.label || 'Chapter';
    function add(lab, shown, kind) {
      var spoken = speakable(shown);
      if (!spoken) return;
      group(spoken, MAX).forEach(function (t, k) {
        out.push({ label: lab, kind: kind || 'text', text: t, shown: k === 0 ? plain(shown) : '', emotion: emotionFor(shown, lab) });
      });
    }
    function mapSay(m) { m.links.forEach(function (l) { var p = l.split('|'); add('Concept map', p[0].replace(/\[ch\d+\]/, '').trim() + ', ' + p[1].trim() + ', ' + p[2].replace(/\[ch\d+\]/, '').trim() + '.'); }); }
    add('Chapter', label + ' ' + ch.n + '. ' + ch.title + '.', 'intro');
    (ch.maps || []).forEach(function (m) { add('Concept map', 'Concept map: ' + m.title + '.', 'head'); mapSay(m); });
    if (ch.summary) blocks(ch.summary).forEach(function (b) { add('Summary', b.text); });
    if (ch.glossary && ch.glossary.length) {
      add('Glossary', 'Glossary.', 'head');
      ch.glossary.forEach(function (g) { add('Glossary', g.term + '. ' + g.def); });
    }
    if (ch.points) { add('Key points', 'Key points.', 'head'); blocks(ch.points).forEach(function (b) { add('Key points', b.text); }); }
    if (ch.examples && ch.examples.trim()) {
      add('Lesson', 'Lesson.', 'head');
      var skipped = false;
      blocks(ch.examples).forEach(function (b) {
        if (b.type === 'img') add('Figure', b.text, 'figure');
        else if (b.type === 'code') {
          if (/conceptmap/.test(b.lang)) { add('Concept map', 'Another concept map. I will read its links.', 'head'); b.text.split('\n').forEach(function (l) { var p = l.split('|'); if (p.length === 3) add('Concept map', p[0].replace(/\[ch\d+\]/, '').trim() + ', ' + p[1].trim() + ', ' + p[2].replace(/\[ch\d+\]/, '').trim() + '.'); }); }
          else if (opts.readCode) add('Code', 'Code example. ' + b.text.split('\n').slice(0, 14).join('. '), 'code');
          else if (!skipped) { skipped = true; add('Code', 'There is a code example here. I am skipping it; read it on screen, or turn on read code in settings.', 'code'); }
        } else add('Lesson', b.text);
      });
    }
    add('Chapter', 'That is the end of ' + label.toLowerCase() + ' ' + ch.n + '. The quiz and practice are waiting for you.', 'outro');
    return out;
  }

  /* ---------- playback engine ---------- */
  function createNarrator(env, hooks) {
    hooks = hooks || {};
    var st = { chunks: [], i: 0, playing: false, rate: 1, token: 0, timer: null, held: false };
    function note() { if (hooks.onState) hooks.onState({ playing: st.playing, i: st.i, n: st.chunks.length, rate: st.rate }); }
    function clearT() { if (st.timer) { clearTimeout(st.timer); st.timer = null; } }
    function cut() { st.token++; clearT(); try { env.cancel(); } catch (e) {} }
    function advance(t) {
      if (t !== st.token || !st.playing) return;
      clearT();
      var cur = st.chunks[st.i];
      if (cur && cur.hold) {            // wait for the learner (quiz question): stop here, the app resumes with next()+play()
        st.playing = false; st.held = true; cut(); if (hooks.onSpeaking) hooks.onSpeaking(false); note(); if (hooks.onHold) hooks.onHold(st.i, cur); return;
      }
      st.i++; speakCurrent();
    }
    function speakCurrent() {
      var c = st.chunks[st.i];
      if (!c) { st.playing = false; st.i = Math.max(0, st.chunks.length - 1); note(); if (hooks.onDone) hooks.onDone(); return; }
      var t = ++st.token;
      if (hooks.onChunk) hooks.onChunk(st.i, c);
      note();
      if (c.wait) { if (hooks.onSpeaking) hooks.onSpeaking(false); clearT(); st.timer = setTimeout(function () { advance(t); }, c.wait); return; }
      var est = Math.max(1500, c.text.length * 95 / st.rate) + 5000;
      clearT(); st.timer = setTimeout(function () { advance(t); }, est);   // watchdog if the engine never reports the end
      env.speak(c.text, st.rate, {
        onstart: function () { if (t === st.token && hooks.onSpeaking) hooks.onSpeaking(true); },
        onword: function () { if (t === st.token && hooks.onWord) hooks.onWord(); },
        onend: function () { advance(t); },
        onerror: function () { advance(t); }
      });
    }
    return {
      load: function (chunks, start) { cut(); st.chunks = chunks; st.i = start || 0; st.playing = false; note(); },
      play: function () { st.held = false; if (!st.chunks.length) return; if (st.i >= st.chunks.length) st.i = 0; st.playing = true; speakCurrent(); },
      pause: function () { st.playing = false; cut(); if (hooks.onSpeaking) hooks.onSpeaking(false); note(); },
      toggle: function () { st.playing ? this.pause() : this.play(); },
      next: function () { var was = st.playing; cut(); if (st.i < st.chunks.length - 1) st.i++; st.playing = was; if (was) speakCurrent(); else { if (hooks.onChunk) hooks.onChunk(st.i, st.chunks[st.i]); note(); } },
      prev: function () { var was = st.playing; cut(); if (st.i > 0) st.i--; st.playing = was; if (was) speakCurrent(); else { if (hooks.onChunk) hooks.onChunk(st.i, st.chunks[st.i]); note(); } },
      jump: function (i) { var was = st.playing; cut(); st.i = Math.max(0, Math.min(st.chunks.length - 1, i)); st.playing = was; if (was) speakCurrent(); else { if (hooks.onChunk) hooks.onChunk(st.i, st.chunks[st.i]); note(); } },
      setRate: function (r) { st.rate = r; if (st.playing) { cut(); speakCurrent(); } else note(); },
      stop: function () { st.playing = false; cut(); st.i = 0; if (hooks.onSpeaking) hooks.onSpeaking(false); note(); },
      state: st
    };
  }

  /* ---------- speech backends ---------- */
  function silentEnv() {
    var t = null;
    return {
      kind: 'silent',
      speak: function (text, rate, cb) {
        if (cb.onstart) cb.onstart();
        var words = text.split(' '), k = 0, per = 330 / Math.max(0.5, rate);
        (function tick() {
          if (k < words.length) { if (cb.onword) cb.onword(); k++; t = setTimeout(tick, per); } else if (cb.onend) cb.onend();
        })();
      },
      cancel: function () { if (t) clearTimeout(t); t = null; }
    };
  }

  function makeEnv(win) {
    if (win && win.AndroidTTS) {
      var pending = {}, n = 0;
      win.__ttsEvent = function (id, type) {
        var cb = pending[id]; if (!cb) return;
        if (type === 'start' && cb.onstart) cb.onstart();
        else if (type === 'range' && cb.onword) cb.onword();
        else if (type === 'done') { delete pending[id]; if (cb.onend) cb.onend(); }
        else if (type === 'error') { delete pending[id]; if (cb.onerror) cb.onerror(); }
      };
      return {
        kind: 'android',
        speak: function (text, rate, cb) { var id = ++n; pending[id] = cb; win.AndroidTTS.speak(text, rate, id); },
        cancel: function () { pending = {}; win.AndroidTTS.stop(); }
      };
    }
    if (win && win.speechSynthesis && win.SpeechSynthesisUtterance) {
      var syn = win.speechSynthesis, voiceName = null;
      return {
        kind: 'web',
        voices: function () { return (syn.getVoices() || []).filter(function (v) { return /^en/i.test(v.lang); }); },
        setVoice: function (nme) { voiceName = nme; },
        speak: function (text, rate, cb) {
          var parts = group(text, 200), k = 0;
          (function next() {
            if (k >= parts.length) { if (cb.onend) cb.onend(); return; }
            var u = new win.SpeechSynthesisUtterance(parts[k++]);
            u.rate = rate; u.pitch = 1.05;
            var vs = syn.getVoices() || [], v = null;
            if (voiceName) v = vs.filter(function (x) { return x.name === voiceName; })[0];
            if (!v) v = vs.filter(function (x) { return /^en/i.test(x.lang) && /female|zira|samantha|aria|jenny|google us/i.test(x.name); })[0] || vs.filter(function (x) { return /^en/i.test(x.lang); })[0];
            if (v) u.voice = v;
            u.onstart = function () { if (cb.onstart && k === 1) cb.onstart(); };
            u.onboundary = function () { if (cb.onword) cb.onword(); };
            u.onend = next;
            u.onerror = function () { if (cb.onerror) cb.onerror(); };
            syn.speak(u);
          })();
        },
        cancel: function () { try { syn.cancel(); } catch (e) {} }
      };
    }
    return silentEnv();
  }

  /* ---------- avatar frame controller (frames: 1 eyes open/mouth closed, 2 open/open, 3 shut/closed, 4 shut/open) ---------- */
  function createAvatar(setFrame) {
    var a = { emotion: 'neutral', mouth: false, blink: false, speaking: false, mt: null, bt: null, wt: null };
    function paint() { setFrame(a.emotion, 1 + (a.blink ? 2 : 0) + (a.mouth ? 1 : 0)); }
    function mouthLoop() {
      if (!a.speaking) { a.mouth = false; paint(); return; }
      a.mouth = !a.mouth; paint();
      a.mt = setTimeout(mouthLoop, a.mouth ? 90 + Math.random() * 70 : 70 + Math.random() * 110);
    }
    function blinkLoop() {
      a.bt = setTimeout(function () { a.blink = true; paint(); setTimeout(function () { a.blink = false; paint(); blinkLoop(); }, 130); }, 2400 + Math.random() * 2800);
    }
    return {
      state: a,
      start: function () { paint(); if (!a.bt) blinkLoop(); },
      emotion: function (e) { if (e !== a.emotion) { a.emotion = e; paint(); } },
      speaking: function (on) { if (on === a.speaking) return; a.speaking = on; if (a.mt) clearTimeout(a.mt); if (on) mouthLoop(); else { a.mouth = false; paint(); } },
      word: function () {
        if (!a.speaking) return;
        if (a.mt) clearTimeout(a.mt);
        a.mouth = true; paint();
        a.mt = setTimeout(function () { a.mouth = false; paint(); a.mt = setTimeout(mouthLoop, 60); }, 110);
      },
      stop: function () { a.speaking = false; if (a.mt) clearTimeout(a.mt); if (a.bt) clearTimeout(a.bt); a.bt = null; a.mouth = false; a.blink = false; paint(); }
    };
  }

  var api = { setPronounce: setPronounce, speakable: speakable, plain: plain, emotionFor: emotionFor, buildChunks: buildChunks, createNarrator: createNarrator, makeEnv: makeEnv, silentEnv: silentEnv, createAvatar: createAvatar, blocks: blocks, sentences: sentences };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LilithNarrate = api;
})(typeof window !== 'undefined' ? window : globalThis);
