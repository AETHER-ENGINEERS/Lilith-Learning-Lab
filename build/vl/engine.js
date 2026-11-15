/* Verilog engine: Icarus Verilog (ivlpp, ivl, vvp) in WebAssembly, from VeriSim (GPL-2.0). Offline. */
window.__VLM = {};
const VL = (function () {
  const B = window.VL_BLOBS;
  async function inflate(b64) {
    const bin = atob(b64), u = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    const ds = new DecompressionStream('deflate-raw');
    const w = ds.writable.getWriter(); w.write(u); w.close();
    return new Uint8Array(await new Response(ds.readable).arrayBuffer());
  }
  const wasm = {}; let ready = null;
  function load() {
    if (ready) return ready;
    ready = (async () => {
      for (const n of ['ivlpp', 'ivl', 'vvp']) {
        const js = new TextDecoder().decode(await inflate(B[n + '_js']));
        wasm[n] = await inflate(B[n + '_wasm']);
        const s = document.createElement('script'); s.textContent = js; document.head.appendChild(s);
      }
    })();
    return ready;
  }
  const mod = (n, o) => window.__VLM[n](Object.assign({ wasmBinary: wasm[n] }, o));
  const CONF = g => 'basedir:/\nmodule:system.vpi\ngeneration:' + g + '\ngeneration:no-specify\nout:/out.vvp\niwidth:32\nwidthcap:65536\nfunctor:cprop\nfunctor:nodangle\nflag:DLL=vvp.tgt\n';
  /* files: [{name, src}]; returns {ok, log, vcd, err} */
  async function run(files, gen) {
    await load(); gen = gen || '2005';
    const code = [];
    const pp = await mod('ivlpp', { print: s => code.push(s), printErr: () => {} });
    const args = ['-L'];
    for (const f of files) { pp.FS.writeFile('/' + f.name, f.src.endsWith('\n') ? f.src : f.src + '\n'); args.push('/' + f.name); }
    pp.callMain(args);
    const err = [];
    const c = await mod('ivl', { print: () => {}, printErr: s => err.push(s) });
    c.FS.writeFile('/ivl.conf', CONF(gen)); c.FS.writeFile('/src.v', code.join('\n') + '\n');
    try { c.callMain(['-C/ivl.conf', '--', '/src.v']); } catch (e) {}
    let vvp = null; try { vvp = c.FS.readFile('/out.vvp'); } catch (e) {}
    const eText = err.filter(l => !/system\.vpi|dynamic linking not enabled/.test(l)).join('\n');
    if (!vvp) return { ok: false, log: eText || 'compile failed', vcd: null, err: eText };
    const out = [];
    const v = await mod('vvp', { print: s => out.push(s), printErr: s => out.push(s) });
    v.FS.writeFile('/sim.vvp', vvp);
    try { v.callMain(['/sim.vvp']); } catch (e) {}
    let vcd = null; try { vcd = v.FS.readFile('/dump.vcd', { encoding: 'utf8' }); } catch (e) {}
    return { ok: true, log: out.join('\n'), vcd: vcd, err: eText };
  }
  return { run, load };
})();
