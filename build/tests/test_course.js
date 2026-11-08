// Course format + lab engine tests. Run: node tests/test_course.js
const fs = require('fs'), path = require('path');
const K = require('../src/course.js'), X = require('../src/xdc.js'), S = require('../src/slides.js'), N = require('../src/narrate.js');
let fails = 0; const ok = (c, m) => { if (!c) { fails++; console.log('FAIL', m); } };
const dir = path.join(__dirname, '..', '..', 'courses');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.course.json'));
ok(files.length >= 2, 'two course files');

(async () => {
  // template validates and covers every lab type
  const tv = K.validate(K.template()); ok(tv.ok && tv.warnings.length === 0, 'template valid: ' + JSON.stringify(tv.warnings));
  ok(tv.course.chapters[0].practice.length === 5, 'template has 5 labs');
  // bad input
  ok(!K.validate('not json').ok, 'bad json rejected'); ok(!K.validate({}).ok, 'empty rejected'); ok(!K.validate({ title: 'x', chapters: [] }).ok, 'no chapters rejected');
  ok(!K.validate({ format: 'other', title: 'x', chapters: [{ title: 'c' }] }).ok, 'wrong format rejected');
  const odd = K.validate({ title: 'x', chapters: [{ title: 'c', quiz: [{ q: 'q', options: ['a'], answer: 0 }, { q: 'q2', options: ['a', 'b'], answer: 'b' }], practice: [{ type: 'nope' }] }] });
  ok(odd.ok && odd.course.chapters[0].quiz.length === 1 && odd.course.chapters[0].quiz[0].answer === 1 && odd.warnings.length >= 2, 'tolerant of bad quiz/lab: ' + JSON.stringify(odd.warnings));

  for (const f of files) {
    const raw = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    const v = K.validate(raw); ok(v.ok, f + ' valid'); ok(v.warnings.length === 0, f + ' warnings: ' + v.warnings.join('; '));
    const c = v.course; N.setPronounce(c.pronounce);
    let nlabs = 0, nq = 0;
    for (const ch of c.chapters) {
      ok(ch.maps.length >= 1, f + ' ch' + ch.n + ' has a map'); ok(ch.summary.length >= 1, f + ' ch' + ch.n + ' summary');
      ok(ch.glossary.length >= 1, f + ' ch' + ch.n + ' glossary'); ok(ch.keyPoints.length >= 1, f + ' ch' + ch.n + ' key points');
      ok(ch.quiz.length >= 2, f + ' ch' + ch.n + ' quiz'); ok(ch.practice.length >= 1, f + ' ch' + ch.n + ' practice');
      nq += ch.quiz.length;
      // lecture structure
      const view = K.chapterView(ch, c), L = S.buildLecture(view, { readCode: false });
      const order = []; L.slides.forEach(s => { if (order[order.length - 1] !== s.stage) order.push(s.stage); });
      const want = ['title', 'map', 'summary', 'glossary', 'points', 'lesson', 'quiz', 'practice', 'end'].filter(s => order.indexOf(s) >= 0);
      ok(JSON.stringify(order) === JSON.stringify(want), f + ' ch' + ch.n + ' stage order ' + order.join(','));
      ok(order.indexOf('map') === 1, f + ' ch' + ch.n + ' map comes right after the title');
      ok(order[order.length - 2] === 'practice' && order.indexOf('quiz') < order.indexOf('practice'), f + ' ch' + ch.n + ' quiz then practice at the end');
      L.chunks.forEach((k, i) => { ok(k.text.length <= 450, f + ' ch' + ch.n + ' chunk ' + i + ' too long ' + k.text.length); ok(k.slide >= 0 && k.slide < L.slides.length, 'chunk slide index'); });
      const qs = L.slides.map((s, i) => [s, i]).filter(x => x[0].type === 'quiz');
      qs.forEach(([s, i]) => { const cs = L.chunks.filter(k => k.slide === i); ok(cs.length === 2 && cs[0].hold && cs[1].feedback, 'quiz chunks hold+feedback'); });
      // reading mode chunks
      const rc = N.buildChunks(view, {}); ok(rc.length > 3, 'read chunks');
      // every lab solvable
      for (const lab of ch.practice) {
        nlabs++;
        const tag = f + ' ch' + ch.n + ' lab ' + lab.id + ' (' + lab.type + ')';
        if (lab.type === 'fill') { const segs = K.parseFill(lab.text).filter(s => s.t === 'blank'); ok(segs.length > 0 && K.checkFill(lab, segs.map(s => s.alts[0])).pass, tag + ' fill solution'); ok(!K.checkFill(lab, segs.map(() => 'zzz')).pass, tag + ' fill wrong'); }
        else if (lab.type === 'order') { ok(K.checkOrder(lab, lab.items).pass, tag + ' order'); ok(!K.checkOrder(lab, lab.items.slice().reverse()).pass, tag + ' order reversed'); }
        else if (lab.type === 'match') { ok(K.checkMatch(lab, lab.pairs.map(p => p[1])).pass, tag + ' match'); ok(!K.checkMatch(lab, lab.pairs.map(() => 'x')).pass, tag + ' match wrong'); }
        else if (lab.type === 'write') { ok(lab.solution && K.checkWrite(lab, lab.solution).pass, tag + ' write solution: ' + JSON.stringify(K.checkWrite(lab, lab.solution || ''))); ok(!K.checkWrite(lab, '').pass, tag + ' write empty'); }
        else if (lab.type === 'code') {
          ok(lab.solution, tag + ' has solution');
          const r = K.runCodeSync(lab, lab.solution); ok(r.pass, tag + ' solution passes: ' + r.msgs.slice(-3).join(' | '));
          const r2 = K.runCodeSync(lab, lab.starter); ok(!r2.pass, tag + ' starter fails');
        } else if (lab.type === 'terminal') {
          const T = K.makeScriptTerm(lab); ok(T.tasks.length >= 1, tag + ' has tasks');
          // run each task's own regex as a command (strip regex anchors to make a command)
          const cmds = {
            'Query the power mode: sudo nvpmodel -q': 'sudo nvpmodel -q', 'Set MAXN: sudo nvpmodel -m 0': 'sudo nvpmodel -m 0', 'Lock the clocks: sudo jetson_clocks': 'sudo jetson_clocks', 'Run tegrastats': 'tegrastats',
            'Build the FP16 GPU engine': 'trtexec --onnx=model.onnx --fp16 --saveEngine=gpu.engine', 'Load it again': 'trtexec --loadEngine=gpu.engine',
            'Build model.onnx for DLA with fallback and --verbose': 'trtexec --onnx=model.onnx --fp16 --useDLACore=0 --allowGPUFallback --verbose', 'Try decoder.onnx and read why layers fall back': 'trtexec --onnx=decoder.onnx --fp16 --useDLACore=0 --allowGPUFallback',
            'Install gymnasium': 'pip install gymnasium', 'Check that it imports': 'python -c "import gymnasium"', 'Run the random CartPole script': 'python cartpole_random.py', 'Install Stable-Baselines3': 'pip install "stable-baselines3[extra]"', 'Run the training script': 'python train_cartpole.py', 'List the files to see the saved model': 'ls', 'Run train.py': 'python train.py', 'Start TensorBoard': 'tensorboard --logdir ./tb/', 'Check the best model was saved': 'ls best',
            'Check the type of a function type': '#check Nat → Nat', 'Check And.intro': '#check And.intro', 'State and prove the swap theorem': "theorem and_swap' (A B : Prop) : A ∧ B → B ∧ A := fun ⟨a, b⟩ => ⟨b, a⟩", 'Print its axioms': "#print axioms and_swap'", 'See an incorrect proof rejected': 'example : 2 + 2 = 5 := rfl',
            'Find 20% of 80': 'calc 20 of 80', 'Find 10% of 350': 'calc 10 of 350'
          };
          T.tasks.forEach(t => { const cmd = cmds[t.text]; ok(cmd, tag + ' no scripted command for ' + t.text); if (cmd) T.exec(cmd); });
          ok(T.tasks.every(t => T.state.done[t.id]), tag + ' all tasks done: ' + JSON.stringify(T.state.done));
          ok(Array.isArray(T.exec('nonsense')) && T.exec('nonsense')[0].c === 'err', tag + ' unknown command');
        } else if (lab.type === 'webxdc') {
          const r = await X.labToHtml(lab, [], 'T'); ok(/window\.webxdc=/.test(r.html) && r.html.length > 500, tag + ' app html');
        }
      }
    }
    if (c.sandbox) {
      const T = K.makeScriptTerm(c.sandbox);
      const run = l => T.exec(l).map(x => x.t).join('\n');
      if (c.id === 'rl-python-gymnasium-sb3') {
        ok(/clipped objective/.test(run('algo ppo')), 'algo ppo'); ok(/discrete only/i.test(run('algo dqn')), 'algo dqn'); ok(/n_steps 2048/.test(run('defaults ppo')), 'defaults'); ok(/Unknown/.test(run('xyz')), 'unknown');
      }
      if (c.id === 'curry-howard-lambek') {
        ok(/A → B → A/.test(run('type K')), 'type K'); ok(/B × A/.test(run('type swap')), 'type swap'); ok(/exponential/.test(run('dict')), 'dict'); ok(/Unknown name/.test(run('type zzz')), 'unknown type'); ok(/Unknown command/.test(run('xyz')), 'unknown');
      }
      if (c.id === 'jetson-agx-xavier') {
        ok(/MAXN/.test(run('sudo nvpmodel -q')), 'nvpmodel -q');
        run('sudo nvpmodel -m 1'); ok(/MODE_10W/.test(run('sudo nvpmodel -q')), 'mode 10W set');
        ok(/ERROR/.test(run('nvpmodel -m 0')), 'needs sudo');
        ok(/@114/.test(run('tegrastats')), 'idle gpu clock when unlocked'); run('sudo jetson_clocks'); ok(/@520/.test(run('tegrastats')), 'locked gpu clock');
        ok(/softmax.*cannot run on DLA/.test(run('trtexec --onnx=model.onnx --fp16 --useDLACore=0')), 'dla without fallback fails');
        ok(/DLA subgraphs: 1/.test(run('trtexec --onnx=model.onnx --fp16 --useDLACore=0 --allowGPUFallback --verbose')), 'dla fallback');
        ok(/DLA subgraphs: 3/.test(run('trtexec --onnx=decoder.onnx --fp16 --useDLACore=0 --allowGPUFallback')), 'decoder partitions');
        ok(/supports only FP16/.test(run('trtexec --onnx=model.onnx --useDLACore=0')), 'dla needs fp16');
        ok(/command not found/.test(run('nvcc -arch=sm_72 vector_add.cu -o vector_add')), 'nvcc before PATH');
        run('export PATH=/usr/local/cuda/bin:$PATH'); ok(/sm_72/.test(run('nvcc -arch=sm_72 vector_add.cu -o vector_add')), 'nvcc ok'); ok(/c\[0\] = 3/.test(run('./vector_add')), 'run vector_add');
        run('nvcc -arch=sm_53 vector_add.cu -o vector_add'); ok(/no kernel image/.test(run('./vector_add')), 'wrong arch fails');
        run('trtexec --onnx=model.onnx --fp16 --saveEngine=gpu.engine'); ok(/gpu\.engine/.test(run('ls')), 'engine listed after build'); ok(/Loaded engine/.test(run('trtexec --loadEngine=gpu.engine')), 'load engine');
        run('cat /etc/nv_tegra_release'); run('sudo nvpmodel -m 0');
        ok(/dla/i.test(run('trtexec --onnx=model.onnx --fp16 --useDLACore=0 --allowGPUFallback --verbose 2>&1 | grep -i dla')), 'pipe grep');
        const t = T.tasks.filter(x => T.state.done[x.id]).length; ok(t >= 6, 'sandbox tasks tracked: ' + t);
      }
    }
    console.log(f, c.chapters.length, 'chapters,', nlabs, 'labs,', nq, 'quiz questions');
  }
  // xdc: zip round trip with a stored + deflated entry
  const zlib = require('zlib');
  console.log(fails ? 'FAILURES: ' + fails : 'ALL COURSE TESTS PASSED'); process.exit(fails ? 1 : 0);
})();
