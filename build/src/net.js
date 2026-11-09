/* Lilith Learning Lab: network layer for the AI features and the hidden agent workspace.
   - Android: http/https requests go through the app's native bridge (AndroidTTS.httpStart), streamed back in chunks.
     Ollama Cloud and most APIs send no CORS headers, so a WebView page (file://) cannot call them with fetch itself.
   - Web: requests go out with fetch; when a CORS proxy is set (AI settings), cross-site requests go through it
     (local and private addresses never do, and neither do sites that already allow every page).
   - https://kit.local/ is a virtual host for the Jade Agent Kit's own files (BusyBox, MicroPython), served from memory
     so the workspace works offline.
   - LilithNet.loadKit() loads kit.js (the Jade Agent Kit bundle) the first time the agent needs it. */
(function (root) {
  'use strict';
  var NET = root.LilithNet = root.LilithNet || {};
  NET.assets = NET.assets || {};
  var orig = root.fetch ? root.fetch.bind(root) : null;
  NET.origFetch = orig;

  function b64bytes(s) { var bin = atob(s), u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u; }
  NET.b64bytes = b64bytes;
  function headObj(h) {
    var o = {}; if (!h) return o;
    if (typeof h.forEach === 'function' && !Array.isArray(h)) h.forEach(function (v, k) { o[k] = v; });
    else if (Array.isArray(h)) h.forEach(function (p) { o[p[0]] = p[1]; });
    else for (var k in h) o[k] = h[k];
    return o;
  }
  NET.hasNative = function () { return !!(root.AndroidTTS && typeof root.AndroidTTS.httpStart === 'function'); };

  /* ---------- Android native HTTP, streamed ---------- */
  var seq = 0, pend = {};
  root.__httpEv = function (id, kind, a, b) {
    var p = pend[id]; if (!p) return;
    if (kind === 'h') p.head(+a, b);
    else if (kind === 'd') p.data(a);
    else if (kind === 'e') { delete pend[id]; p.end(); }
    else { delete pend[id]; p.fail(a); }
  };
  NET.nativeFetch = function (url, init) {
    init = init || {};
    return new Promise(function (resolve, reject) {
      var id = ++seq, ctrl = null, headed = false, done = false, queue = [];
      var stream = new ReadableStream({
        start: function (c) { ctrl = c; queue.forEach(function (q) { q(); }); queue = []; },
        cancel: function () { done = true; delete pend[id]; try { root.AndroidTTS.httpAbort(id); } catch (e) {} }
      });
      function withCtrl(f) { if (ctrl) f(); else queue.push(f); }
      pend[id] = {
        head: function (status, hjson) {
          headed = true; var h = {}; try { h = JSON.parse(hjson || '{}'); } catch (e) {}
          var nullBody = status === 101 || status === 204 || status === 205 || status === 304;
          var st = status >= 200 && status <= 599 ? status : 502;
          try { resolve(new Response(nullBody ? null : stream, { status: st, headers: h })); } catch (e) { resolve(new Response(nullBody ? null : stream, { status: st })); }
        },
        data: function (b) { withCtrl(function () { if (!done) try { ctrl.enqueue(b64bytes(b)); } catch (e) {} }); },
        end: function () { withCtrl(function () { if (!done) { done = true; try { ctrl.close(); } catch (e) {} } }); },
        fail: function (m) {
          var err = new TypeError('network error: ' + m);
          if (!headed) reject(err); else withCtrl(function () { if (!done) { done = true; try { ctrl.error(err); } catch (e) {} } });
        }
      };
      var sig = init.signal;
      if (sig) {
        if (sig.aborted) { delete pend[id]; reject(new DOMException('stopped', 'AbortError')); return; }
        sig.addEventListener('abort', function () {
          var p = pend[id]; delete pend[id]; try { root.AndroidTTS.httpAbort(id); } catch (e) {}
          var err = new DOMException('stopped', 'AbortError');
          if (!headed) reject(err); else if (p) withCtrl(function () { if (!done) { done = true; try { ctrl.error(err); } catch (e) {} } });
        });
      }
      var body = init.body == null ? '' : init.body;
      if (typeof body !== 'string') { try { body = new TextDecoder().decode(body); } catch (e) { body = String(body); } }
      try { root.AndroidTTS.httpStart(id, String(init.method || 'GET').toUpperCase(), String(url), JSON.stringify(headObj(init.headers)), body); }
      catch (e) { delete pend[id]; reject(new TypeError('network error: ' + (e.message || e))); }
    });
  };

  /* ---------- CORS proxy (web version only) ---------- */
  var OPEN = /^https:\/\/([a-z0-9-]+\.)*(wikipedia\.org|githubusercontent\.com|r\.jina\.ai)\//i;   // these already allow every page
  function isLocal(u) { return /^https?:\/\/(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|\[::1\]|[^/]*\.local(:|\/|$))/i.test(u); }
  NET.proxyFor = function (url) {
    var p = ''; try { p = (JSON.parse(root.localStorage.getItem('lilith.ai') || '{}').corsProxy) || ''; } catch (e) {}
    if (!p || NET.hasNative() || isLocal(url) || OPEN.test(url)) return url;
    try { if (new URL(url).origin === root.location.origin) return url; } catch (e) {}
    if (url.indexOf(p.replace('{url}', '')) === 0) return url;
    return p.indexOf('{url}') >= 0 ? p.replace('{url}', encodeURIComponent(url)) : p + url;
  };

  /* ---------- the kit's own files ---------- */
  NET.kitAsset = function (url) {
    var path = url.replace(/^https:\/\/kit\.local\//, '').split('?')[0], name = path.split('/').pop(), a;
    if (/micropython\.(mjs|wasm)$/.test(name) && root.LilithMP) {
      a = name === 'micropython.wasm' ? b64bytes(root.LilithMP.wasm) : root.LilithMP.mjs;
    } else {
      a = NET.assets[name];
      if (a && a.b64) a = NET.assets[name] = b64bytes(a.b64);
    }
    if (a == null) return Promise.resolve(new Response('not bundled: ' + name, { status: 404 }));
    var type = /\.wasm$/.test(name) ? 'application/wasm' : 'text/javascript';
    return Promise.resolve(new Response(a, { status: 200, headers: { 'Content-Type': type } }));
  };

  if (orig && !orig.__lilith) {
    var wrapped = function (input, init) {
      var url = typeof input === 'string' ? input : input && input.url ? input.url : String(input);
      if (url.indexOf('https://kit.local/') === 0) return NET.kitAsset(url);
      if (/^https?:\/\//i.test(url)) {
        if (NET.hasNative()) {
          if (typeof input !== 'string' && input && input.url && !init) init = { method: input.method, headers: input.headers };
          return NET.nativeFetch(url, init);
        }
        var p = NET.proxyFor(url); if (p !== url) return orig(p, init);
      }
      return orig(input, init);
    };
    wrapped.__lilith = true;
    root.fetch = wrapped;
  }

  /* explain a failed request in plain words */
  NET.explain = function (e, url) {
    var m = String(e && e.message || e);
    if (/Failed to fetch|NetworkError|Load failed|network error/i.test(m)) {
      if (NET.hasNative()) return m + ' (no connection, or the server is not reachable from this phone)';
      if (url && isLocal(url)) return 'could not reach ' + url + '. Is "ollama serve" running? Allow this site with OLLAMA_ORIGINS (for example OLLAMA_ORIGINS="*").';
      return 'the browser blocked the request (the server does not allow web pages to call it: CORS). Set a CORS proxy in AI settings, or use the Android app.';
    }
    return m;
  };

  /* ---------- the Jade Agent Kit bundle ---------- */
  var kitP = null;
  NET.loadKit = function () {
    if (root.JadeKit) return Promise.resolve(root.JadeKit);
    return kitP = kitP || new Promise(function (res, rej) {
      var s = root.document.createElement('script'); s.src = 'kit.js';
      s.onload = function () { root.JadeKit ? res(root.JadeKit) : rej(new Error('kit.js loaded but JadeKit is missing')); };
      s.onerror = function () { kitP = null; rej(new Error('could not load kit.js')); };
      root.document.head.appendChild(s);
    });
  };
})(typeof window !== 'undefined' ? window : globalThis);
