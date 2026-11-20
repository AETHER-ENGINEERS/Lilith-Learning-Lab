/* ================= CLASSROOM =================
   In a webxdc chat (Vector, Delta Chat, PDA SEASIDE...) a lecture can be a class. Whoever starts it presents; the
   others join and follow the same slide, each device speaking for itself. Anyone can raise a hand: the lecture pauses
   for everyone, and the question and its answers are seen by all (any classmate can answer, as well as the presenter).
   Quizzes stay individual: only who has answered is shared, and each person's own score at the end, never the
   answers. Outside a chat (the web, Android) there is no webxdc and none of this shows.
   Spliced into app.html's main script by build_web.py (at the CLASS marker), so it shares the app's own state. */
// (var, not const: the app draws its first screen before this part runs, and asks for the class bar)
var XW = (window.webxdc && typeof window.webxdc.sendUpdate === 'function' && typeof window.webxdc.setUpdateListener === 'function') ? window.webxdc : null;
var CLS = { id: '', host: '', hostName: '', course: '', title: '', file: '', src: '', ch: 0, i: 0, playing: false, people: {}, asks: [], answered: {}, scores: {}, joined: false, ready: false, applying: false, sent: '' };
function meAddr() { return (XW && XW.selfAddr) || 'me'; }
function meName() { return (XW && XW.selfName) || 'Me'; }
function inClass() { return !!(CLS && CLS.id) && (CLS.joined || CLS.host === meAddr()); }
function presenting() { return !!(CLS && CLS.id) && CLS.host === meAddr(); }
function following() { return inClass() && !presenting(); }
function clsSend(p, info) {
  if (!XW) return;
  try { XW.sendUpdate({ payload: Object.assign({ lilithClass: 1, from: meAddr(), name: meName() }, p), info: info || undefined }, info || ''); } catch (e) {}
}
function haveCourse(id) { return ST.courses.some(c => c.id === id); }
function clsReset() { Object.assign(CLS, { id: '', host: '', hostName: '', course: '', title: '', file: '', src: '', ch: 0, i: 0, playing: false, people: {}, asks: [], answered: {}, scores: {}, joined: false, sent: '' }); }
function clsHandle(p) {
  if (!p || !p.lilithClass) return;
  const mine = p.from === meAddr();
  if (p.k === 'start') {
    clsReset();
    Object.assign(CLS, { id: p.id, host: p.from, hostName: p.name, course: p.course, title: p.title, file: p.file || '', src: p.src || '', ch: p.ch, i: p.i || 0, playing: false });
    CLS.people[p.from] = p.name;
  } else if (p.id !== CLS.id) {
    return;   // (an older class)
  } else if (p.k === 'end') {
    const was = inClass() && !mine; clsReset(); if (was && CLS.ready) toast('The class has ended.');
  } else if (p.k === 'join') {
    CLS.people[p.from] = p.name; if (mine) CLS.joined = true;
    if (CLS.ready && presenting() && !mine) { toast(p.name + ' joined the class'); clsPos(true); }
  } else if (p.k === 'leave') {
    delete CLS.people[p.from]; if (mine) CLS.joined = false;
  } else if (p.k === 'pos' && p.from === CLS.host) {
    Object.assign(CLS, { ch: p.ch, i: p.i, playing: !!p.playing });
    if (CLS.ready) clsFollow();
  } else if (p.k === 'ask') {
    CLS.asks.push({ qid: p.qid, who: p.name, from: p.from, q: String(p.q || '').slice(0, 600), answers: [] });
    if (CLS.ready && presenting() && NAR.state.playing) NAR.pause();
    if (CLS.ready && !mine) toast(p.name + ' raised a hand');
  } else if (p.k === 'answer') {
    const a = CLS.asks.find(x => x.qid === p.qid); if (a) a.answers.push({ who: p.name, text: String(p.text || '').slice(0, 1500) });
  } else if (p.k === 'done') {
    const a = CLS.asks.find(x => x.qid === p.qid); if (a) a.done = true;
  } else if (p.k === 'answered') {
    const key = p.ch + ':' + p.si; (CLS.answered[key] = CLS.answered[key] || {})[p.from] = p.name;
    if (CLS.ready && LEC && LEC.ch.n === p.ch) { const l = $('#clsn'); if (l) l.outerHTML = clsAnsweredLine(p.si); }
  } else if (p.k === 'score') {
    (CLS.scores[p.ch] = CLS.scores[p.ch] || {})[p.from] = { name: p.name, correct: p.correct, total: p.total };
  }
  if (CLS.ready) clsBar();
}
if (XW) {
  const backlog = XW.setUpdateListener(u => clsHandle(u && u.payload), 0);
  Promise.resolve(backlog).then(() => { CLS.ready = true; clsBar(); });
}
// the presenter's place: sent when it changes (a chunk, play or pause)
function clsPos(force) {
  if (!presenting() || !LEC || LEC.tour) return;
  const s = CLS.course + '|' + LEC.ch.n + '|' + NAR.state.i + '|' + (NAR.state.playing ? 1 : 0);
  if (!force && s === CLS.sent) return;
  CLS.sent = s; CLS.ch = LEC.ch.n; CLS.i = NAR.state.i; CLS.playing = NAR.state.playing;
  clsSend({ k: 'pos', id: CLS.id, ch: LEC.ch.n, i: NAR.state.i, playing: NAR.state.playing });
}
// a member's place follows the presenter's
function clsFollow() {
  if (!following() || CLS.applying) return;
  if (!CUR || CUR.course.id !== CLS.course) { if (!haveCourse(CLS.course)) return; openCourse(CLS.course); }
  CLS.applying = true;
  try {
    if (!LEC || LEC.tour || LEC.ch.n !== CLS.ch) { tab = 'lecture'; view = null; openLecture(CLS.ch, false, CLS.i); }
    else if (NAR.state.i !== CLS.i) NAR.jump(CLS.i);
    if (CLS.playing && !NAR.state.playing && !NAR.state.held) NAR.play();
    else if (!CLS.playing && NAR.state.playing) NAR.pause();
  } finally { CLS.applying = false; }
}
function clsStart() {
  if (!XW || !CUR || !LEC || LEC.tour) return;
  const cat = STORE.cat && STORE.cat.courses.find(x => x.id === CUR.course.id);
  const meta = ST.courses.find(x => x.id === CUR.course.id) || {};
  const id = meAddr() + ':' + Date.now().toString(36);
  clsSend({ k: 'start', id, course: CUR.course.id, title: CUR.course.title, file: cat ? cat.file : CUR.course.id + '.course.json', src: meta.src || '', ch: LEC.ch.n, i: NAR.state.i }, meName() + ' started a class: ' + CUR.course.title);
  setTimeout(() => clsPos(true), 300);
}
function clsJoin() {
  if (!CLS.id) return;
  if (!haveCourse(CLS.course)) {
    toast('Getting ' + CLS.title + ' for the class...');
    netGet(rawBase(CLS.src || DEFAULT_REPO) + CLS.file).then(t => {
      srcRepo = CLS.src || DEFAULT_REPO; try { importText(t, CLS.title); } finally { srcRepo = ''; }
      closeModal(); clsSend({ k: 'join', id: CLS.id }); setTimeout(clsFollow, 400);
    }).catch(() => modal('<h3 class="dh">You need this course first</h3><div class="muted">' + esc(CLS.hostName) + ' is presenting <b>' + esc(CLS.title) + '</b>, and it couldn\'t be downloaded here. Ask them to share its file, import it, then join.</div><div class="row end">' + btn('mx', 'close', 'Close', 'pri') + '</div>', d => { $('#mx', d).onclick = closeModal; }));
    return;
  }
  clsSend({ k: 'join', id: CLS.id });
  setTimeout(clsFollow, 300);
}
function clsLeave() { if (!CLS.id) return; if (presenting()) clsSend({ k: 'end', id: CLS.id }, meName() + ' ended the class'); else clsSend({ k: 'leave', id: CLS.id }); }
function clsAsk() {
  modal('<h3 class="dh">Raise your hand</h3><div class="muted">Everyone in the class sees your question, and the lecture pauses until it\'s answered.</div><textarea class="big" id="cq" placeholder="Your question..."></textarea><div class="row end">' + btn('cc', 'close', 'Cancel', 'txt') + btn('cs', 'help_outline', 'Ask', 'pri') + '</div>', d => {
    $('#cc', d).onclick = closeModal;
    $('#cs', d).onclick = () => { const q = $('#cq', d).value.trim(); closeModal(); if (q) clsSend({ k: 'ask', id: CLS.id, qid: meAddr() + ':' + Date.now().toString(36), q, at: { ch: CLS.ch, i: CLS.i } }, meName() + ' raised a hand'); };
  });
}
function clsAnswer(qid) {
  modal('<h3 class="dh">Answer</h3><textarea class="big" id="ca" placeholder="Your answer..."></textarea><div class="row end">' + btn('cc', 'close', 'Cancel', 'txt') + btn('cs', 'check', 'Send', 'pri') + '</div>', d => {
    $('#cc', d).onclick = closeModal;
    $('#cs', d).onclick = () => { const t = $('#ca', d).value.trim(); closeModal(); if (t) clsSend({ k: 'answer', id: CLS.id, qid, text: t }); };
  });
}
// the class bar, under the header: what the class is, who's in it, raised hands and their answers
function clsBar() {
  const el = $('#clsbar'); if (!el || !CLS) return;
  let h = '';
  if (XW && !CLS.id) {
    if (LEC && !LEC.tour) h = '<div class="row"><span class="muted" style="flex:1">Learning with others in this chat? Start a class: everyone follows your slides.</span>' + btn('clsgo', 'school', 'Start class', 'tonal sm') + '</div>';
  } else if (XW) {
    const n = Object.keys(CLS.people).length, who = Object.values(CLS.people).map(esc).join(', ');
    if (presenting()) h = '<div class="row"><span style="flex:1">' + ic('school') + ' <b>Presenting</b> ' + esc(CLS.title) + ' · ' + n + ' in class (' + who + ')</span>' + btn('clsend', 'flag', 'End class', 'sm') + '</div>';
    else if (CLS.joined) h = '<div class="row"><span style="flex:1">' + ic('school') + ' <b>In class</b> with ' + esc(CLS.hostName) + ' · ' + esc(CLS.title) + ' · ' + n + ' here</span>' + btn('clshand', 'help_outline', 'Raise hand', 'tonal sm') + btn('clsleave', 'close', 'Leave', 'sm') + '</div>';
    else h = '<div class="row"><span style="flex:1">' + ic('school') + ' <b>' + esc(CLS.hostName) + '</b> is presenting ' + esc(CLS.title) + ' · ' + n + ' in class</span>' + btn('clsjoin', 'play_lesson', 'Join', 'pri sm') + '</div>';
    const open = CLS.asks.filter(a => !a.done).slice(-3);
    if (inClass()) h += open.map(a => '<div class="clsq"><b>' + ic('help_outline') + ' ' + esc(a.who) + ':</b> ' + esc(a.q) + a.answers.map(x => '<div class="clsa"><b>' + esc(x.who) + ':</b> ' + esc(x.text) + '</div>').join('') + '<div class="row end"><button class="btn sm txt" data-cans="' + esc(a.qid) + '">' + ic('edit_note') + '<span>Answer</span></button>' + (presenting() || a.from === meAddr() ? '<button class="btn sm txt" data-cdone="' + esc(a.qid) + '">' + ic('check') + '<span>Answered</span></button>' : '') + '</div></div>').join('');
  }
  el.innerHTML = h; el.classList.toggle('hid', !h);
  const on = (id, f) => { const b = $('#' + id, el); if (b) b.onclick = f; };
  on('clsgo', clsStart); on('clsjoin', clsJoin); on('clsleave', clsLeave); on('clsend', clsLeave); on('clshand', clsAsk);
  $$('[data-cans]', el).forEach(b => b.onclick = () => clsAnswer(b.dataset.cans));
  $$('[data-cdone]', el).forEach(b => b.onclick = () => clsSend({ k: 'done', id: CLS.id, qid: b.dataset.cdone }));
}
// on a quiz slide in class: who has answered so far (never what)
function clsAnsweredLine(si) {
  if (!inClass() || !LEC) return '';
  const got = CLS.answered[LEC.ch.n + ':' + si] || {}, n = Object.keys(CLS.people).length;
  return '<div class="muted" id="clsn">' + Object.keys(got).length + ' of ' + n + ' answered' + (Object.keys(got).length ? ': ' + Object.values(got).map(esc).join(', ') : '') + '</div>';
}
// a quiz answered in class: only that it was, and the score once the chapter's quiz is done
function clsQuizAnswered(si, allDone, correct, total) {
  if (!inClass() || !LEC) return;
  clsSend({ k: 'answered', id: CLS.id, ch: LEC.ch.n, si });
  if (allDone) clsSend({ k: 'score', id: CLS.id, ch: LEC.ch.n, correct, total });
}
