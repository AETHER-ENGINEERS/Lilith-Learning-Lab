/*! quantum-web-lab Python runner | MIT | runs MicroPython (WebAssembly) with MicroQiskit in a Worker. The payload is window.QWL_PY = {mjs, wasm, lib} (gzip + base64, built by build.py). */
(function (root) {
  'use strict';
  var QWL = root.QWL, cache = null;
  function inflate(b64) {
    var bin = atob(b64), u = new Uint8Array(bin.length), i; for (i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    return new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();
  }
  function load() {
    if (!cache) cache = Promise.all([inflate(root.QWL_PY.mjs), inflate(root.QWL_PY.wasm)]).then(function (r) { return { mjs: new TextDecoder().decode(r[0]), wasm: r[1] }; });
    return cache;
  }
  var GLUE = '\nonmessage=async function(e){var d=e.data,out=[];try{' +
    'var url=URL.createObjectURL(new Blob([d.wasm],{type:"application/wasm"}));' +
    'var mp=await loadMicroPython({url:url,heapsize:16*1024*1024,stdout:function(s){out.push(s)},stderr:function(s){out.push(s)}});' +
    'mp.FS.mkdir("/lib");mp.FS.writeFile("/lib/microqiskit.py",d.lib);mp.runPython("import sys\\nsys.path.append(\\"/lib\\")");' +
    'try{mp.runPython(d.code)}catch(err){postMessage({err:String(err&&err.message||err),out:out.join("\\n")});return}' +
    'var q="";try{mp.runPython("import microqiskit as _m\\ntry:\\n    _c = qc\\n    if not isinstance(_c, _m.QuantumCircuit):\\n        _c = _m.last()\\nexcept NameError:\\n    _c = _m.last()\\n_q = _c.qasm() if _c else \\"\\"");q=mp.globals.get("_q")||""}catch(e2){}' +
    'postMessage({out:out.join("\\n"),qasm:q})}catch(e3){postMessage({err:String(e3&&e3.message||e3),out:out.join("\\n")})}};';
  function friendly(msg) {
    var lines = String(msg).split('\n').filter(function (l) { return l.trim(); }), last = lines[lines.length - 1] || msg, ln = '';
    lines.forEach(function (l) { var m = /File "<stdin>", line (\d+)/.exec(l); if (m) ln = m[1]; });
    return (ln ? 'Line ' + ln + ': ' : '') + last;
  }
  QWL.py = {
    available: function () { return !!(root.QWL_PY && typeof Worker !== 'undefined' && typeof Blob !== 'undefined' && typeof DecompressionStream !== 'undefined'); },
    run: function (code, ms) {
      return load().then(function (d) { return new Promise(function (resolve) {
        var done = false, w, url, timer;
        function fin(r) { if (done) return; done = true; clearTimeout(timer); try { w.terminate(); } catch (e) {} try { URL.revokeObjectURL(url); } catch (e) {} if (r.err) r.err = friendly(r.err); resolve(r); }
        try { url = URL.createObjectURL(new Blob([d.mjs + GLUE], { type: 'text/javascript' })); w = new Worker(url); } catch (e) { return resolve({ err: 'Python could not start on this device.' }); }
        w.onmessage = function (e) { fin(e.data); }; w.onerror = function () { fin({ err: 'Python could not start on this device.' }); };
        timer = setTimeout(function () { fin({ err: 'Your code ran longer than ' + ((ms || 8000) / 1000) + ' seconds (an endless loop?).' }); }, ms || 8000);
        w.postMessage({ code: code, wasm: d.wasm.slice(0), lib: root.QWL_PY.lib });
      }); }, function () { return { err: 'Python could not load.' }; });
    }
  };
})(typeof window !== 'undefined' ? window : globalThis);
