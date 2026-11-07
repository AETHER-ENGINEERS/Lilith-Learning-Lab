/* Core logic for the Jetson AGX Xavier interactive tutorial.
   Pure functions only (no DOM) so it can be tested in Node and reused in the Android app.
   Everything here is a SIMULATION: numbers are illustrative, not measurements. */
(function (root) {
  'use strict';

  /* ---------- DLA layer-support checker (rules summarized in tutorial chapter 10) ---------- */
  function checkLayer(l) {
    var t = String(l.type || '').toLowerCase();
    var ok = function (r) { return { device: 'DLA', reason: r || 'supported on DLA' }; };
    var no = function (r) { return { device: 'GPU', reason: r }; };
    switch (t) {
      case 'conv': case 'fc': case 'batchnorm': case 'scale': case 'eltwise': case 'lrn':
      case 'shuffle': case 'relu': case 'sigmoid': case 'tanh': case 'leakyrelu': case 'clippedrelu':
        return ok();
      case 'pool':
        if ((l.window || 2) > 8) return no('pooling window must be in [1,8]');
        return ok();
      case 'concat':
        if (l.axis !== undefined && l.axis !== 1) return no('concat is supported only along the channel axis');
        return ok();
      case 'deconv':
        if ((l.padding || 0) !== 0) return no('deconvolution padding must be 0 (recent TensorRT docs)');
        if ((l.groups || 1) !== 1) return no('grouped deconvolution is not supported');
        if ((l.stride || 2) > 16) return no('deconvolution stride must be in [1,16]');
        return ok();
      case 'resize': {
        var s = l.scale;
        if (!Number.isInteger(s)) return no('resize needs an integer scale factor on DLA');
        var lim = l.mode === 'bilinear' ? 4 : 32;
        if (s > lim) return no('resize ' + (l.mode || 'nearest') + ' scale must be <= ' + lim);
        return ok();
      }
      case 'reduce':
        if (l.op !== 'max') return no('Reduce supports the MAX operation only');
        return ok();
      case 'softmax': return no('Softmax is not supported on Xavier DLA (Orin only)');
      case 'argmax': case 'topk': return no('ArgMax/TopK are not supported on DLA');
      case 'lstm': case 'gru': return no('recurrent layers are not supported on DLA (verify in docs)');
      case 'attention': return no('attention is not supported on DLA (verify in docs)');
      case 'matmul': return no('generic MatMul is not supported: express it as a 1x1 conv or fully connected layer');
      case 'gelu': return no('GELU is not in the DLA activation list');
      case 'gather': case 'embedding': return no('gather/embedding lookups are not supported on DLA');
      case 'conv3d': return no('only 2D spatial layers are supported on DLA');
      default: return no('unknown or unsupported layer type: ' + t);
    }
  }

  function planDLA(layers, opts) {
    opts = opts || {};
    var per = layers.map(function (l, i) {
      var r = checkLayer(l);
      return { name: l.name || (l.type + i), type: l.type, device: r.device, reason: r.reason };
    });
    var fallbacks = per.filter(function (p) { return p.device === 'GPU'; }).length;
    var subgraphs = 0, transitions = 0, prev = null;
    per.forEach(function (p) {
      if (p.device === 'DLA' && prev !== 'DLA') subgraphs++;
      if (prev !== null && p.device !== prev) transitions++;
      prev = p.device;
    });
    var firstBad = per.filter(function (p) { return p.device === 'GPU'; })[0];
    return {
      per: per, fallbacks: fallbacks, subgraphs: subgraphs, transitions: transitions,
      error: (!opts.fallback && firstBad) ? ('Layer ' + firstBad.name + ' (' + firstBad.type + ') cannot run on DLA: ' + firstBad.reason + '. Add --allowGPUFallback to run it on the GPU.') : null
    };
  }

  /* ---------- demo ONNX models used by the simulated terminal ---------- */
  var MODELS = {
    'model.onnx': {
      about: 'demo network: conv-relu-conv-relu-resize-conv-softmax',
      layers: [
        { type: 'conv', name: 'conv1' }, { type: 'relu', name: 'relu1' },
        { type: 'conv', name: 'conv2', stride: 2 }, { type: 'relu', name: 'relu2' },
        { type: 'resize', name: 'up1', mode: 'nearest', scale: 2 },
        { type: 'conv', name: 'conv3' }, { type: 'softmax', name: 'softmax' }]
    },
    'decoder.onnx': {
      about: 'VAE-style decoder using transposed convolutions with padding 1',
      layers: [
        { type: 'conv', name: 'dec_conv1' }, { type: 'relu', name: 'dec_relu1' },
        { type: 'deconv', name: 'deconv1', padding: 1 }, { type: 'relu', name: 'dec_relu2' },
        { type: 'deconv', name: 'deconv2', padding: 1 }, { type: 'sigmoid', name: 'out' }]
    },
    'vqscore.onnx': {
      about: 'VQ-VAE codebook scores as a 1x1 conv, followed by argmin',
      layers: [{ type: 'conv', name: 'score_conv' }, { type: 'argmax', name: 'argmin' }]
    }
  };

  var POWER = [
    { id: 0, name: 'MAXN', cpus: 8, cpuMhz: 2265, gpuMhz: 1377, emc: 2133 },
    { id: 1, name: 'MODE_10W', cpus: 2, cpuMhz: 1200, gpuMhz: 520, emc: 1331 },
    { id: 2, name: 'MODE_15W', cpus: 4, cpuMhz: 1200, gpuMhz: 670, emc: 1331 },
    { id: 3, name: 'MODE_30W_ALL', cpus: 8, cpuMhz: 1200, gpuMhz: 900, emc: 1600 },
    { id: 4, name: 'MODE_30W_6CORE', cpus: 6, cpuMhz: 1450, gpuMhz: 900, emc: 1600 },
    { id: 5, name: 'MODE_30W_4CORE', cpus: 4, cpuMhz: 1780, gpuMhz: 900, emc: 1600 },
    { id: 6, name: 'MODE_30W_2CORE', cpus: 2, cpuMhz: 2100, gpuMhz: 900, emc: 1600 },
    { id: 7, name: 'MODE_15W_DESKTOP', cpus: 4, cpuMhz: 1500, gpuMhz: 670, emc: 1331 }
  ];

  var MISSIONS = [
    { id: 'identify', text: 'Identify your software: cat /etc/nv_tegra_release' },
    { id: 'mode', text: 'Query the power mode: sudo nvpmodel -q' },
    { id: 'maxn', text: 'Set MAXN and lock clocks: sudo nvpmodel -m 0 ; sudo jetson_clocks' },
    { id: 'gpu', text: 'Build a GPU FP16 engine: trtexec --onnx=model.onnx --fp16 --saveEngine=gpu.engine' },
    { id: 'dla', text: 'Build for DLA with fallback and read the placement: add --useDLACore=0 --allowGPUFallback --verbose' },
    { id: 'cuda', text: 'Compile and run CUDA: export PATH=/usr/local/cuda/bin:$PATH ; nvcc -arch=sm_72 vector_add.cu -o vector_add ; ./vector_add' },
    { id: 'stats', text: 'Watch the system: tegrastats' }
  ];

  var VECTOR_ADD = [
    '// vector_add.cu',
    '__global__ void add(const float* a, const float* b, float* c, int n) {',
    '  int i = blockIdx.x * blockDim.x + threadIdx.x;',
    '  if (i < n) c[i] = a[i] + b[i];',
    '}',
    '// main(): n = 1<<20, 256 threads/block, blocks = (n+255)/256'
  ];

  function fmt(n, d) { return Number(n).toFixed(d === undefined ? 3 : d); }

  /* ---------- simulated terminal ---------- */
  function makeTerm(rng) {
    rng = rng || Math.random;
    var S = {
      mode: 0, locked: false, fan: false, cuda: false, gpuBusy: 0, swap: false,
      files: {
        'model.onnx': { kind: 'onnx' }, 'decoder.onnx': { kind: 'onnx' }, 'vqscore.onnx': { kind: 'onnx' },
        'vector_add.cu': { kind: 'cu' }, 'export.py': { kind: 'py' }
      },
      done: {}, hist: []
    };
    function pw() { return POWER[S.mode]; }
    function factor() {
      var f = 0.5 + 0.5 * pw().gpuMhz / 1377;
      if (!S.locked) f *= 0.88;               // clocks not locked: dynamic scaling costs speed and adds variance
      return f;
    }
    function jitter(x, pct) { return x * (1 + (rng() - 0.5) * 2 * (pct || 0.03)); }
    function mark(id) { S.done[id] = true; }
    function L(t, c) { return { t: t, c: c || '' }; }
    function out(arr) { return arr.map(function (x) { return typeof x === 'string' ? L(x) : x; }); }

    function splitArgs(s) {
      var m = s.match(/"[^"]*"|'[^']*'|\S+/g) || [];
      return m.map(function (x) { return x.replace(/^["']|["']$/g, ''); });
    }

    function trtexec(args) {
      var flag = function (n) { return args.some(function (a) { return a === n; }); };
      var val = function (n) {
        for (var i = 0; i < args.length; i++) {
          if (args[i].indexOf(n + '=') === 0) return args[i].slice(n.length + 1);
        }
        return null;
      };
      var res = [];
      var onnx = val('--onnx'), load = val('--loadEngine'), save = val('--saveEngine');
      var dlaArg = val('--useDLACore');
      var dla = dlaArg !== null && dlaArg !== '' ? parseInt(dlaArg, 10) : null;
      var fp16 = flag('--fp16'), int8 = flag('--int8'), fb = flag('--allowGPUFallback'), verbose = flag('--verbose');
      var prec = int8 ? 'INT8' : (fp16 ? 'FP16' : 'FP32');
      res.push(L('&&&& RUNNING TensorRT.trtexec [TensorRT v8502] # trtexec ' + args.join(' '), 'dim'));
      var layers = null, engineMeta = null;

      if (load) {
        var f = S.files[load];
        if (!f || f.kind !== 'engine') return res.concat([L('[E] Engine file not found: ' + load + ' (build one first with --saveEngine)', 'err'), L('&&&& FAILED TensorRT.trtexec', 'err')]);
        engineMeta = f.meta;
        if (dla !== null && engineMeta.dla === null) res.push(L('[W] --useDLACore ignored: this engine was built for the GPU.', 'warn'));
        res.push(L('[I] Loaded engine ' + load + ' (' + engineMeta.prec + ', ' + (engineMeta.dla === null ? 'GPU' : 'DLA core ' + engineMeta.dla) + ', ' + engineMeta.model + ')'));
        layers = MODELS[engineMeta.model].layers;
        prec = engineMeta.prec; dla = engineMeta.dla;
        fb = true;
      } else if (onnx) {
        if (!MODELS[onnx] || !S.files[onnx]) return res.concat([L('[E] Could not open ' + onnx + '. Try: ls', 'err'), L('&&&& FAILED TensorRT.trtexec', 'err')]);
        layers = MODELS[onnx].layers;
        res.push(L('[I] Parsing ONNX model ' + onnx + ' (' + layers.length + ' layers)'));
        if (dla !== null) {
          if (dla < 0 || dla > 1) return res.concat([L('[E] DLA core ' + dla + ' does not exist: the AGX Xavier has cores 0 and 1.', 'err'), L('&&&& FAILED TensorRT.trtexec', 'err')]);
          if (prec === 'FP32') return res.concat([L('[E] DLA supports only FP16 and INT8. Add --fp16 (or --int8).', 'err'), L('&&&& FAILED TensorRT.trtexec', 'err')]);
        }
        if (prec === 'INT8') res.push(L('[W] No calibration data given: INT8 scales are placeholders. Use this run for timing only.', 'warn'));
      } else {
        return res.concat([L('Usage: trtexec --onnx=model.onnx [--fp16|--int8] [--useDLACore=0|1 --allowGPUFallback] [--saveEngine=x.engine] [--verbose]', 'dim'), L('       trtexec --loadEngine=x.engine [--useDLACore=N] [--iterations=N]', 'dim')]);
      }

      var plan = null, fallbacks = 0;
      if (dla !== null) {
        plan = planDLA(layers, { fallback: fb });
        if (plan.error && !load) {
          return res.concat([L('[E] ' + plan.error, 'err'), L('[E] Engine build failed.', 'err'), L('&&&& FAILED TensorRT.trtexec', 'err')]);
        }
        fallbacks = plan.fallbacks;
        if (!load) {
          if (verbose) {
            plan.per.forEach(function (p) {
              res.push(L('[V] ' + p.name + ' (' + p.type + ') -> ' + p.device + (p.device === 'GPU' ? '  [fallback: ' + p.reason + ']' : ''), p.device === 'GPU' ? 'warn' : ''));
            });
          } else if (fallbacks) {
            res.push(L('[W] ' + fallbacks + ' layer(s) will run on the GPU. Add --verbose to see which.', 'warn'));
          }
          res.push(L('[I] DLA subgraphs: ' + plan.subgraphs + ', DLA/GPU transitions: ' + plan.transitions + (plan.transitions > 2 ? '  (many transitions add overhead)' : '')));
        }
      }
      if (!load) {
        res.push(L('[I] Building engine (' + prec + (dla !== null ? ', DLA core ' + dla : ', GPU') + ') ... done in ' + fmt(jitter(dla !== null ? 42 : 25, 0.1), 1) + ' s'));
        if (save) {
          S.files[save] = { kind: 'engine', meta: { prec: prec, dla: dla, model: onnx, fallbacks: fallbacks } };
          res.push(L('[I] Saved engine to ' + save));
        }
      }
      // timing model
      var base = { FP32: 4.8, FP16: 2.1, INT8: 1.4 }[prec];
      if (dla !== null) base = { FP16: 5.6, INT8: 3.9 }[prec] + 0.7 * fallbacks + 0.15 * (plan ? plan.transitions : 0);
      var ms = base / factor();
      var iters = parseInt(val('--iterations') || '10', 10) || 10;
      var mean = jitter(ms, S.locked ? 0.02 : 0.08);
      res.push(L('[I] Running ' + iters + ' iterations on ' + (dla !== null ? 'DLA core ' + dla + (fallbacks ? ' (+GPU for ' + fallbacks + ' layer(s))' : '') : 'GPU') + ', power mode ' + pw().name + (S.locked ? ', clocks locked' : ', clocks NOT locked')));
      res.push(L('[I] Latency: min = ' + fmt(mean * 0.97) + ' ms, max = ' + fmt(mean * (S.locked ? 1.05 : 1.2)) + ' ms, mean = ' + fmt(mean) + ' ms'));
      res.push(L('[I] Throughput: ' + fmt(1000 / mean, 1) + ' qps (batch 1)'));
      res.push(L('&&&& PASSED TensorRT.trtexec', 'ok'));
      S.gpuBusy = dla !== null ? Math.min(30, 4 + fallbacks * 6) : 95;
      if (!load && dla === null && fp16 && save) mark('gpu');
      if (!load && dla !== null) mark('dla');
      return res;
    }

    function tegrastats() {
      var lines = [];
      var p = pw();
      for (var k = 0; k < 4; k++) {
        var busy = S.gpuBusy;
        var cpu = [];
        for (var i = 0; i < 8; i++) {
          cpu.push(i < p.cpus ? Math.round(jitter(8 + busy * 0.15, 0.6)) + '%@' + p.cpuMhz : 'off');
        }
        var g = Math.max(0, Math.min(99, Math.round(jitter(busy, 0.1))));
        var gm = busy > 0 || S.locked ? p.gpuMhz : 114;
        var t = 38 + busy * 0.12 + (S.fan ? -4 : 0);
        var d = new Date();
        var ts = String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0') + '-' + d.getFullYear() + ' ' + d.toTimeString().slice(0, 8);
        lines.push(L(ts + ' RAM ' + Math.round(2900 + busy * 12) + '/31920MB (lfb 7078x4MB) SWAP ' + (S.swap ? '120' : '0') + '/15960MB CPU [' + cpu.join(',') + '] EMC_FREQ ' + Math.round(3 + busy * 0.25) + '%@' + p.emc + ' GR3D_FREQ ' + g + '%@' + gm + ' AO@' + fmt(t - 2, 1) + 'C GPU@' + fmt(t + 1, 1) + 'C Tdiode@' + fmt(t + 3, 1) + 'C thermal@' + fmt(t, 1) + 'C', ''));
        S.gpuBusy = Math.max(0, S.gpuBusy - 25);
      }
      lines.push(L('(simulated output; real lines include more fields and vary by release)', 'dim'));
      mark('stats');
      return lines;
    }

    function nvpmodel(args, sudo) {
      if (args.indexOf('-q') >= 0) {
        mark('mode');
        var res = [L('NV Power Mode: ' + pw().name), L(String(pw().id))];
        if (args.indexOf('--verbose') >= 0) {
          res = [L('NVPM VERB: Config file: /etc/nvpmodel.conf')];
          POWER.forEach(function (m) { res.push(L('  MODE ' + m.id + ': ' + m.name + '  (cpus online: ' + m.cpus + ', GPU max ' + m.gpuMhz + ' MHz)  [illustrative]', m.id === S.mode ? 'ok' : '')); });
          res.push(L('NV Power Mode: ' + pw().name));
          res.push(L(String(pw().id)));
        }
        return res;
      }
      var i = args.indexOf('-m');
      if (i >= 0) {
        if (!sudo) return [L('NVPM ERROR: Run this command as root (use sudo).', 'err')];
        var id = parseInt(args[i + 1], 10);
        if (!(id >= 0 && id < POWER.length)) return [L('NVPM ERROR: Invalid mode id. Use "sudo nvpmodel -q --verbose" to list modes.', 'err')];
        S.mode = id; S.locked = false;
        return [L('NVPM WARN: clocks reset by the new power mode; run sudo jetson_clocks to lock them again.', 'warn'), L('Power mode set: ' + pw().name, 'ok')];
      }
      return [L('Usage: sudo nvpmodel -q [--verbose] | sudo nvpmodel -m <mode id>', 'dim')];
    }

    function help() {
      return out([
        'Simulated Jetson AGX Xavier shell. Try these:',
        '  cat /etc/nv_tegra_release      sudo nvpmodel -q [--verbose]   sudo nvpmodel -m 0',
        '  sudo jetson_clocks [--show|--fan]    tegrastats    free -h    lscpu    df -h    lsusb',
        '  ls    cat model.onnx    trtexec --onnx=model.onnx --fp16 --saveEngine=gpu.engine',
        '  trtexec --onnx=model.onnx --fp16 --useDLACore=0 --allowGPUFallback --verbose',
        '  trtexec --loadEngine=gpu.engine --iterations=100',
        '  export PATH=/usr/local/cuda/bin:$PATH ; nvcc -arch=sm_72 vector_add.cu -o vector_add ; ./vector_add',
        '  apt-cache show nvidia-jetpack    gst-launch-1.0 ...    dmesg | tail    python3 -c "import tensorrt; ..."',
        '  missions   (your checklist)     hint     history     clear',
        'Pipes with grep / head / tail / tee are supported (e.g. trtexec ... 2>&1 | grep -i dla).',
        'Everything here is a simulation: numbers are illustrative, not measurements.'
      ]);
    }

    function missions() {
      var r = [L('Missions (chapters 5-10):', 'dim')];
      MISSIONS.forEach(function (m) { r.push(L((S.done[m.id] ? '[x] ' : '[ ] ') + m.text, S.done[m.id] ? 'ok' : '')); });
      return r;
    }

    function hint() {
      for (var i = 0; i < MISSIONS.length; i++) if (!S.done[MISSIONS[i].id]) return [L('Next mission: ' + MISSIONS[i].text, 'warn')];
      return [L('All missions done. Try the DLA on decoder.onnx and vqscore.onnx and read why layers fall back.', 'ok')];
    }

    function runOne(line) {
      line = line.replace(/2>&1/g, '').trim();
      if (!line) return [];
      var args = splitArgs(line);
      var sudo = false;
      if (args[0] === 'sudo') { sudo = true; args.shift(); }
      var cmd = args.shift();
      if (!cmd) return [];
      cmd = cmd.replace('/usr/src/tensorrt/bin/', '');
      switch (cmd) {
        case 'help': return help();
        case 'missions': return missions();
        case 'hint': return hint();
        case 'whoami': return [L('nvidia')];
        case 'pwd': return [L('/home/nvidia')];
        case 'nproc': return [L(String(pw().cpus))];
        case 'echo': return [L(args.join(' '))];
        case 'uname': return [L('Linux jetson-xavier 5.10.104-tegra #1 SMP PREEMPT aarch64 aarch64 aarch64 GNU/Linux  (simulated)')];
        case 'ls': return [L(Object.keys(S.files).sort().map(function (n) { return S.files[n].kind === 'engine' ? n + '*' : n; }).join('  '))];
        case 'cat': {
          var f = args[0];
          if (f === '/etc/nv_tegra_release') { mark('identify'); return [L('# R35 (release), REVISION: 2.1, BOARD: t186ref, EABI: aarch64   (simulated)'), L('# Jetson Linux 35.2.1 is the L4T release inside JetPack 5.1', 'dim')]; }
          if (f === '/etc/nvpmodel.conf') return [L('# power model definitions for the AGX Xavier (use nvpmodel -q --verbose)', 'dim')];
          if (MODELS[f]) return [L(f + ': ' + MODELS[f].about)].concat(MODELS[f].layers.map(function (x) { return L('  ' + x.name + '  (' + x.type + ')' + (x.padding ? ' padding=' + x.padding : '') + (x.scale ? ' scale=' + x.scale : ''), 'dim'); }));
          if (f === 'vector_add.cu') return VECTOR_ADD.map(function (x) { return L(x, 'dim'); });
          if (f === 'export.py') return [L('# torch.onnx.export(net, x, "model.onnx", opset_version=13)', 'dim')];
          return [L('cat: ' + (f || '') + ': No such file or directory', 'err')];
        }
        case 'free': return [L('              total        used        free      shared  buff/cache   available'), L('Mem:           31Gi       ' + fmt(2.9 + S.gpuBusy * 0.012, 1) + 'Gi        26Gi       0.4Gi       2.3Gi        28Gi'), L('Swap:          15Gi          0B        15Gi')];
        case 'df': return [L('Filesystem      Size  Used Avail Use% Mounted on'), L('/dev/mmcblk0p1   28G   17G  9.3G  65% /'), L('tmpfs            16G     0   16G   0% /dev/shm')];
        case 'lscpu': return [L('Architecture:        aarch64'), L('CPU(s):              ' + pw().cpus + ' online (of 8)'), L('Thread(s) per core:  1'), L('Model name:          ARMv8 Processor rev 0 (v8l)   [Carmel]'), L('Vendor ID:           Nvidia')];
        case 'lsusb': return [L('Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub'), L('Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub'), L('(on the host PC in recovery mode you would see an "NVIDIA Corp." device instead)', 'dim')];
        case 'export':
          if (args.join(' ').indexOf('/usr/local/cuda') >= 0) { S.cuda = true; return []; }
          return [];
        case 'which': return [L(args[0] === 'nvcc' && S.cuda ? '/usr/local/cuda/bin/nvcc' : (args[0] === 'trtexec' ? '/usr/src/tensorrt/bin/trtexec' : ''))];
        case 'nvcc': {
          if (!S.cuda) return [L('bash: nvcc: command not found', 'err'), L('hint: export PATH=/usr/local/cuda/bin:$PATH', 'warn')];
          if (args[0] === '--version') return [L('nvcc: NVIDIA (R) Cuda compiler driver'), L('Cuda compilation tools, release 11.4, V11.4.315')];
          var src = null, outn = 'a.out', arch = null;
          for (var i = 0; i < args.length; i++) {
            if (/\.cu$/.test(args[i])) src = args[i];
            else if (args[i] === '-o') outn = args[++i];
            else if (args[i].indexOf('-arch=') === 0) arch = args[i].slice(6);
          }
          if (!src || !S.files[src]) return [L('nvcc fatal   : No input files specified or file not found', 'err')];
          S.files[outn] = { kind: 'exe', arch: arch };
          var r = [];
          if (!arch) r.push(L('note: no -arch given; for the Xavier GPU use -arch=sm_72', 'warn'));
          r.push(L('compiled ' + src + ' -> ' + outn + (arch ? ' for ' + arch : ''), 'ok'));
          return r;
        }
        case 'trtexec': return trtexec(args);
        case 'nvpmodel': return nvpmodel(args, sudo);
        case 'jetson_clocks': {
          if (!sudo) return [L('jetson_clocks must be run as root (use sudo).', 'err')];
          if (args.indexOf('--show') >= 0) {
            return [L('SOC family:tegra194  Machine:' + 'Jetson AGX Xavier'), L('Online CPUs: 0-' + (pw().cpus - 1)), L('GPU MinFreq=114750000 MaxFreq=' + pw().gpuMhz + '000000 CurrentFreq=' + (S.locked ? pw().gpuMhz : 114) + '000000'), L('Fan: speed=' + (S.fan ? 255 : 80) + '   (clocks ' + (S.locked ? 'LOCKED at max' : 'dynamic') + ')')];
          }
          if (args.indexOf('--fan') >= 0) { S.fan = true; return []; }
          if (args.indexOf('--store') >= 0) return [L('settings stored', 'dim')];
          if (args.indexOf('--restore') >= 0) { S.locked = false; return [L('settings restored', 'dim')]; }
          S.locked = true; if (S.mode === 0) mark('maxn');
          return [L('clocks locked at the maximum of ' + pw().name, 'ok')];
        }
        case 'tegrastats': return tegrastats();
        case 'apt-cache': return [L('Package: nvidia-jetpack'), L('Version: 5.1-b147'), L('(simulated; run on your device for the real value)', 'dim')];
        case 'dpkg': return [L('ii  tensorrt  8.5.2.2-1+cuda11.4  arm64  Meta package for TensorRT'), L('ii  libcudnn8  8.6.0.166-1+cuda11.4  arm64  cuDNN runtime'), L('ii  libnvvpi2  2.2.7  arm64  VPI runtime'), L('(simulated)', 'dim')];
        case 'python3': {
          var j = args.join(' ');
          if (j.indexOf('tensorrt') >= 0) return [L('8.5.2.2')];
          if (j.indexOf('torch') >= 0) return [L('1.13.0a0+d0d6b1f2.nv22.09 True   (a Jetson-specific wheel; a pip default wheel would print False)')];
          return [L('(python simulated: only tiny version checks are supported here)', 'dim')];
        }
        case 'jtop': return [L('jtop is a full-screen app: pages CPU, GPU, MEM, ENG (engines), PWR, CTRL. Install with: sudo pip3 install -U jetson-stats', 'dim')];
        case 'dmesg': return [L('[  812.114] nvgpu: gpu power on'), L('[ 1203.552] tegra-pmc: power mode changed'), L('[ 2290.010] (look here for "Out of memory", USB and thermal messages)', 'dim')];
        case 'gst-launch-1.0': {
          var j2 = args.join(' ');
          if (j2.indexOf('nvarguscamerasrc') >= 0) return [L('Setting pipeline to PAUSED ...'), L('GST_ARGUS: Creating output stream'), L('(simulated: camera -> ISP -> VIC -> display; on hardware the frames stay in NVMM memory)', 'dim')];
          return [L('Setting pipeline to PLAYING ...', 'dim'), L('(simulated)', 'dim')];
        }
        case 'clear': return 'CLEAR';
        case 'history': return S.hist.map(function (h, i) { return L(String(i + 1).padStart(4) + '  ' + h); });
        default:
          if (cmd.indexOf('./') === 0) {
            var nm = cmd.slice(2), fx = S.files[nm];
            if (!fx || fx.kind !== 'exe') return [L('bash: ' + cmd + ': No such file or directory', 'err')];
            if (fx.arch && fx.arch !== 'sm_72') return [L('CUDA error: no kernel image is available for execution on the device (built for ' + fx.arch + '; Xavier is sm_72)', 'err')];
            S.gpuBusy = 70; mark('cuda');
            return [L('c[0] = 3.000000 (expected 3.0)', 'ok')];
          }
          return [L('bash: ' + cmd + ': command not found. Type help.', 'err')];
      }
    }

    function exec(line) {
      line = line.trim();
      if (line) S.hist.push(line);
      var segs = line.split(/\s*;\s*/);
      var all = [];
      for (var s = 0; s < segs.length; s++) {
        var seg = segs[s];
        var pipe = seg.split(/\s*\|\s*/);
        var res = runOne(pipe[0]);
        if (res === 'CLEAR') return 'CLEAR';
        for (var p = 1; p < pipe.length; p++) {
          var a = splitArgs(pipe[p]);
          var c = a.shift();
          if (c === 'grep') {
            var ic = a.indexOf('-i') >= 0; a = a.filter(function (x) { return x[0] !== '-'; });
            var re = new RegExp((a[0] || '').replace(/[.+^${}()[\]\\]/g, '\\$&'), ic ? 'i' : '');
            res = res.filter(function (x) { return re.test(x.t); });
          } else if (c === 'head') { var nh = parseInt((a.filter(function (x) { return /^-?\d+$/.test(x); })[0] || '10').replace('-', ''), 10); res = res.slice(0, nh); }
          else if (c === 'tail') { var nt = parseInt((a.filter(function (x) { return /^-?\d+$/.test(x); })[0] || '10').replace('-', ''), 10); res = res.slice(-nt); }
          else if (c === 'tee') { /* pass through */ }
          else if (c === 'wc') { res = [L(String(res.length))]; }
          else res = res.concat([L(c + ': unsupported pipe command in this simulation', 'warn')]);
        }
        all = all.concat(res);
      }
      return all;
    }

    return { exec: exec, state: S, missions: MISSIONS, POWER: POWER };
  }

  /* ---------- code lab challenges ---------- */
  function seeded(seed) { var s = seed; return function () { s = (s * 1664525 + 1013904223) % 4294967296; return s / 4294967296; }; }

  function bruteNearest(a, cb) {
    var best = 0, bd = Infinity;
    for (var k = 0; k < cb.length; k++) {
      var d = 0; for (var i = 0; i < a.length; i++) { var x = a[i] - cb[k][i]; d += x * x; }
      if (d < bd) { bd = d; best = k; }
    }
    return best;
  }

  var CHALLENGES = [
    {
      id: 'grid', chapter: 8, title: 'CUDA grid size',
      intro: 'Write gridSize(n, block): the number of blocks needed so that blocks * block >= n (ceiling division, no Math.ceil on a float division).',
      starter: 'function gridSize(n, block) {\n  // return the number of blocks\n}',
      hint: 'Add (block - 1) to n before the integer division: (n + block - 1) / block, then truncate.',
      solution: 'function gridSize(n, block) {\n  return Math.floor((n + block - 1) / block);\n}',
      test: function (fn) {
        var cases = [[1000000, 256, 3907], [256, 256, 1], [257, 256, 2], [1, 128, 1], [0, 256, 0]];
        var msgs = [], pass = true;
        cases.forEach(function (c) { var g = fn(c[0], c[1]); var ok = g === c[2]; pass = pass && ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + 'gridSize(' + c[0] + ', ' + c[1] + ') = ' + g + ' (expected ' + c[2] + ')'); });
        return { pass: pass, msgs: msgs };
      },
      entry: 'gridSize'
    },
    {
      id: 'bw', chapter: 15, title: 'Bandwidth budget',
      intro: 'Write mbPerSecond(width, height, channels, bytesPerValue, moves, fps): megabytes per second (1 MB = 1,000,000 bytes) when each frame is moved "moves" times.',
      starter: 'function mbPerSecond(width, height, channels, bytesPerValue, moves, fps) {\n  // your code\n}',
      hint: 'bytes per frame = width*height*channels*bytesPerValue; multiply by moves and fps; divide by 1e6.',
      solution: 'function mbPerSecond(width, height, channels, bytesPerValue, moves, fps) {\n  return width * height * channels * bytesPerValue * moves * fps / 1e6;\n}',
      test: function (fn) {
        var cases = [[256, 256, 3, 2, 4, 30, 47.18592], [3840, 2160, 3, 1, 10, 30, 7464.96], [1, 1, 1, 1, 1, 1, 0.000001]];
        var msgs = [], pass = true;
        cases.forEach(function (c) { var v = fn.apply(null, c.slice(0, 6)); var ok = typeof v === 'number' && Math.abs(v - c[6]) < 0.01; pass = pass && ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + 'mbPerSecond(' + c.slice(0, 6).join(', ') + ') = ' + v + ' (expected about ' + c[6] + ')'); });
        return { pass: pass, msgs: msgs };
      },
      entry: 'mbPerSecond'
    },
    {
      id: 'gr3d', chapter: 7, title: 'Parse tegrastats',
      intro: 'Write parseGr3d(line): return {load, mhz} from the GR3D_FREQ field of a tegrastats line. Some releases print the clock in brackets.',
      starter: 'function parseGr3d(line) {\n  // return { load: <number>, mhz: <number> }\n}',
      hint: 'Use a regular expression such as /GR3D_FREQ\\s+(\\d+)%@\\[?(\\d+)\\]?/ and convert the groups with Number().',
      solution: 'function parseGr3d(line) {\n  var m = /GR3D_FREQ\\s+(\\d+)%@\\[?(\\d+)\\]?/.exec(line);\n  if (!m) return null;\n  return { load: Number(m[1]), mhz: Number(m[2]) };\n}',
      test: function (fn) {
        var cases = [
          ['RAM 2951/31920MB CPU [12%@2265,off] EMC_FREQ 5%@2133 GR3D_FREQ 37%@1377 AO@38C', 37, 1377],
          ['GR3D_FREQ 0%@114 thermal@41C', 0, 114],
          ['EMC_FREQ 9%@2133 GR3D_FREQ 88%@[1377] GPU@50C', 88, 1377]];
        var msgs = [], pass = true;
        cases.forEach(function (c) { var v = fn(c[0]); var ok = v && v.load === c[1] && v.mhz === c[2]; pass = pass && !!ok; msgs.push((ok ? 'PASS ' : 'FAIL ') + 'load=' + (v && v.load) + ', mhz=' + (v && v.mhz) + ' (expected ' + c[1] + ', ' + c[2] + ')'); });
        var none = fn('no gpu field here'); var okn = none === null || none === undefined; pass = pass && okn; msgs.push((okn ? 'PASS ' : 'FAIL ') + 'a line without GR3D_FREQ returns null');
        return { pass: pass, msgs: msgs };
      },
      entry: 'parseGr3d'
    },
    {
      id: 'vq', chapter: 11, title: 'VQ-VAE nearest codebook entry',
      intro: 'Write nearest(a, codebook): return the index of the closest codebook vector using the score ||b||^2 - 2 a.b (do not compute ||a - b||^2 directly). This is the math you would put in a 1x1 convolution on the DLA.',
      starter: '// a: array of D numbers; codebook: array of K arrays, each with D numbers\nfunction nearest(a, codebook) {\n  // your code\n}',
      hint: 'For each k: score = sum(b_i^2) - 2*sum(a_i*b_i). Return the index with the smallest score. ||a||^2 is the same for every k, so skip it.',
      solution: 'function nearest(a, codebook) {\n  var best = 0, bs = Infinity;\n  for (var k = 0; k < codebook.length; k++) {\n    var b = codebook[k], nb = 0, dot = 0;\n    for (var i = 0; i < a.length; i++) { nb += b[i] * b[i]; dot += a[i] * b[i]; }\n    var score = nb - 2 * dot;\n    if (score < bs) { bs = score; best = k; }\n  }\n  return best;\n}',
      test: function (fn) {
        var r = seeded(42), msgs = [], pass = true, bad = 0, trials = 200;
        for (var t = 0; t < trials; t++) {
          var D = 8, K = 16, cb = [], a = [];
          for (var k = 0; k < K; k++) { var v = []; for (var i = 0; i < D; i++) v.push(r() * 4 - 2); cb.push(v); }
          for (var j = 0; j < D; j++) a.push(r() * 4 - 2);
          if (fn(a, cb) !== bruteNearest(a, cb)) bad++;
        }
        pass = bad === 0; msgs.push((pass ? 'PASS ' : 'FAIL ') + (trials - bad) + '/' + trials + ' random trials match the brute-force answer');
        return { pass: pass, msgs: msgs };
      },
      entry: 'nearest'
    },
    {
      id: 'dla', chapter: 10, title: 'Make the model DLA-friendly',
      intro: 'Edit the layer list so it runs as ONE DLA subgraph, with at most one GPU layer and that layer must be the final argmax. Keep at least 5 layers and at least one conv. Use the Xavier DLA rules from chapter 10. The function must return the layer array.',
      starter: 'return [\n  { type: "conv", name: "enc1" },\n  { type: "gelu", name: "act1" },\n  { type: "conv", name: "enc2", stride: 2 },\n  { type: "softmax", name: "attn_norm" },\n  { type: "deconv", name: "up1", padding: 1 },\n  { type: "relu", name: "act2" },\n  { type: "resize", name: "up2", mode: "bilinear", scale: 2.5 },\n  { type: "conv", name: "out" },\n  { type: "argmax", name: "pick" }\n];',
      hint: 'GELU -> relu. Softmax is not on Xavier DLA: remove it (apply it on the CPU later if you need it). Deconv with padding 1 -> resize nearest scale 2 followed by a conv. Bilinear scale 2.5 -> nearest or bilinear with an integer scale.',
      solution: 'return [\n  { type: "conv", name: "enc1" },\n  { type: "relu", name: "act1" },\n  { type: "conv", name: "enc2", stride: 2 },\n  { type: "resize", name: "up1", mode: "nearest", scale: 2 },\n  { type: "conv", name: "up1_conv" },\n  { type: "relu", name: "act2" },\n  { type: "resize", name: "up2", mode: "nearest", scale: 2 },\n  { type: "conv", name: "out" },\n  { type: "argmax", name: "pick" }\n];',
      isBody: true,
      test: function (layers) {
        var msgs = [], pass = true;
        if (!Array.isArray(layers)) return { pass: false, msgs: ['FAIL the code must return an array of layers'] };
        var plan = planDLA(layers, { fallback: true });
        plan.per.forEach(function (p) { msgs.push((p.device === 'DLA' ? '  DLA ' : '  GPU ') + p.name + ' (' + p.type + ')' + (p.device === 'GPU' ? '  -> ' + p.reason : '')); });
        var last = layers[layers.length - 1];
        var checks = [
          [layers.length >= 5, 'at least 5 layers'],
          [layers.some(function (l) { return l.type === 'conv'; }), 'contains a conv'],
          [plan.subgraphs === 1, 'exactly 1 DLA subgraph (found ' + plan.subgraphs + ')'],
          [plan.fallbacks <= 1, 'at most 1 GPU layer (found ' + plan.fallbacks + ')'],
          [plan.fallbacks === 0 || (last && last.type === 'argmax'), 'any GPU layer is the final argmax']
        ];
        checks.forEach(function (c) { pass = pass && c[0]; msgs.push((c[0] ? 'PASS ' : 'FAIL ') + c[1]); });
        return { pass: pass, msgs: msgs };
      }
    }
  ];

  function runChallenge(ch, code) {
    try {
      var v;
      if (ch.isBody) v = new Function(code)();
      else v = new Function(code + '\nreturn ' + ch.entry + ';')();
      var res = ch.isBody ? ch.test(v) : ch.test(v);
      return res;
    } catch (e) {
      return { pass: false, msgs: ['ERROR ' + (e && e.message ? e.message : String(e))] };
    }
  }

  var api = { checkLayer: checkLayer, planDLA: planDLA, makeTerm: makeTerm, MODELS: MODELS, POWER: POWER, MISSIONS: MISSIONS, CHALLENGES: CHALLENGES, runChallenge: runChallenge, bruteNearest: bruteNearest };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.XavierCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
