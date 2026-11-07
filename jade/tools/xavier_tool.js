#!/usr/bin/env node
/* xavier_tool.js - domain tools for the NVIDIA Jetson AGX Xavier course: trtexec command builder, DLA layer checker, simulated shell.
   Zero dependencies. Options are key=value (no --flags). Needs core.js next to it. For reading the course itself use lilith_tool.js. */
'use strict';
const fs = require('fs');
const path = require('path');

function die(m) { console.error('error: ' + m); process.exit(1); }

/* ---------- options ---------- */
function opts(args) {
  const o = { _: [] };
  args.forEach(a => { const m = /^([A-Za-z_]+)=([\s\S]*)$/.exec(a); if (m) o[m[1]] = m[2]; else o._.push(a); });
  return o;
}
function core() { try { return require(path.join(__dirname, 'core.js')); } catch (e) { die('core.js must be next to xavier_tool.js (' + e.message + ')'); } }
function readJson(v) { try { return JSON.parse(v.startsWith('@') ? fs.readFileSync(v.slice(1), 'utf8') : v); } catch (e) { die('bad JSON: ' + e.message); } }

const HELP = [
  'xavier_tool.js <command> key=value ...',
  '  trtexec model=model.onnx prec=fp16 dla=0 fallback=yes save=out.engine   build a trtexec command line',
  '  check-dla layers=@model.json  check which layers run on the Xavier DLA ([{"type":"conv","name":"c1"},...])',
  '  sim "sudo nvpmodel -q"        run a command in the simulated Xavier shell (numbers are illustrative)',
  '  help'
].join('\n');

function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const o = opts(rest);
  if (!cmd || cmd === 'help') return console.log(HELP);

  switch (cmd) {
    case 'trtexec': {
      const model = o.model || 'model.onnx', prec = (o.prec || 'fp16').toLowerCase();
      let c = '/usr/src/tensorrt/bin/trtexec --onnx=' + model;
      if (prec === 'fp16') c += ' --fp16'; else if (prec === 'int8') c += ' --int8';
      if (o.dla !== undefined) {
        if (!['0', '1'].includes(o.dla)) die('dla must be 0 or 1 on the AGX Xavier');
        if (prec === 'fp32') die('DLA supports only FP16 and INT8: use prec=fp16 or prec=int8');
        c += ' --useDLACore=' + o.dla; if (!/^(no|false|0)$/i.test(o.fallback || 'yes')) c += ' --allowGPUFallback';
      }
      if (o.save) c += ' --saveEngine=' + o.save;
      if (o.verbose !== 'no') c += ' --verbose';
      console.log(c);
      if (prec === 'int8') console.log('note: INT8 needs calibration data for accuracy; without it use the result for timing only.');
      if (o.dla !== undefined) console.log('note: read the build log for fallback layers and DLA subgraph count (chapter 10).');
      break;
    }
    case 'check-dla': {
      if (!o.layers) die('usage: check-dla layers=@file.json');
      const C = core(); const layers = readJson(o.layers); const plan = C.planDLA(layers, { fallback: true });
      plan.per.forEach(p => console.log((p.device === 'DLA' ? 'DLA ' : 'GPU ') + p.name + ' (' + p.type + ')' + (p.device === 'GPU' ? '  <- ' + p.reason : '')));
      console.log('subgraphs=' + plan.subgraphs + ' fallbacks=' + plan.fallbacks + ' transitions=' + plan.transitions);
      console.log('rules are summarized from NVIDIA docs for recent TensorRT; limits differ by version (Xavier on JetPack 5.1 uses TensorRT 8.5), so confirm with a real build log.');
      break;
    }
    case 'sim': {
      const C = core(); const t = C.makeTerm();
      const lines = o._.join(' ').split(/\s*&&\s*/);
      lines.forEach(l => { const r = t.exec(l); if (r === 'CLEAR') return; r.forEach(x => console.log(x.t)); });
      break;
    }
    default: die('unknown command "' + cmd + '". Try: help');
  }
}
main();
