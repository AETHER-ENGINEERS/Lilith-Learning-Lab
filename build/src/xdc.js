/* webxdc host helpers for Lilith Learning Lab.
   A webxdc app is a ZIP with index.html (+ manifest.toml). A course can carry one inside its JSON:
     { "type": "webxdc", "title": "...", "xdc": "<base64 of the .xdc zip>" }      packed app
     { "type": "webxdc", "title": "...", "html": "<!doctype html>..." }            one inline page
     { "type": "webxdc", "title": "...", "files": { "index.html": "...", "app.js": "..." } }
   The app is run in a sandboxed iframe with a window.webxdc shim (updates are stored on the device) and
   window.lilith.complete() so a lab can tell the app that the learner finished it. */
(function (root) {
  'use strict';

  function b64ToBytes(b64) {
    var bin = (typeof atob === 'function') ? atob(String(b64).replace(/\s+/g, '')) : Buffer.from(String(b64), 'base64').toString('binary');
    var u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u;
  }
  function bytesToB64(u8) {
    var s = ''; for (var i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
    return (typeof btoa === 'function') ? btoa(s) : Buffer.from(s, 'binary').toString('base64');
  }
  function text(u8) { return new TextDecoder('utf-8').decode(u8); }
  function isZip(u8) { return u8 && u8.length > 4 && u8[0] === 0x50 && u8[1] === 0x4b && (u8[2] === 3 || u8[2] === 5); }

  function inflateRaw(u8) {
    if (typeof DecompressionStream === 'undefined') return Promise.reject(new Error('This device cannot unpack compressed apps (DecompressionStream missing).'));
    var ds = new DecompressionStream('deflate-raw');
    var w = ds.writable.getWriter(); w.write(u8); w.close();
    return new Response(ds.readable).arrayBuffer().then(function (b) { return new Uint8Array(b); });
  }

  /* minimal ZIP reader: stored (0) and deflate (8) entries */
  function unzip(u8) {
    var dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength), eocd = -1, i;
    for (i = u8.length - 22; i >= Math.max(0, u8.length - 66000); i--) { if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; } }
    if (eocd < 0) return Promise.reject(new Error('Not a zip file'));
    var n = dv.getUint16(eocd + 10, true), off = dv.getUint32(eocd + 16, true), jobs = [], out = {};
    for (var k = 0; k < n; k++) {
      if (dv.getUint32(off, true) !== 0x02014b50) break;
      var method = dv.getUint16(off + 10, true), csize = dv.getUint32(off + 20, true), nl = dv.getUint16(off + 28, true), el = dv.getUint16(off + 30, true), cl = dv.getUint16(off + 32, true), lho = dv.getUint32(off + 42, true);
      var name = text(u8.subarray(off + 46, off + 46 + nl));
      off += 46 + nl + el + cl;
      if (/\/$/.test(name) || /(^|\/)\.\.(\/|$)/.test(name)) continue;
      var lnl = dv.getUint16(lho + 26, true), lel = dv.getUint16(lho + 28, true), start = lho + 30 + lnl + lel;
      var data = u8.subarray(start, start + csize);
      (function (nm, m, d) {
        if (m === 0) out[nm] = d;
        else if (m === 8) jobs.push(inflateRaw(d).then(function (r) { out[nm] = r; }));
      })(name, method, data);
    }
    return Promise.all(jobs).then(function () { return out; });
  }

  function manifest(files) {
    var t = files['manifest.toml'] ? text(files['manifest.toml']) : '', m = /^\s*name\s*=\s*"(.*)"\s*$/m.exec(t);
    return { name: m ? m[1] : '' };
  }

  var MIME = { png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif', webp: 'image/webp', svg: 'image/svg+xml', ico: 'image/x-icon', woff2: 'font/woff2', woff: 'font/woff', mp3: 'audio/mpeg', ogg: 'audio/ogg', wav: 'audio/wav' };
  function dataUri(path, u8) { var ext = path.split('.').pop().toLowerCase(); return 'data:' + (MIME[ext] || 'application/octet-stream') + ';base64,' + bytesToB64(u8); }
  function norm(p) { return String(p).replace(/^\.\//, '').replace(/^\//, '').split('?')[0].split('#')[0]; }
  function asText(f) { return typeof f === 'string' ? f : text(f); }

  /* shim injected before the app's own scripts */
  function shim(init, selfName) {
    var j = JSON.stringify(init || []).replace(/[<]/g, '\\u003c');
    return '<script>(function(){var updates=' + j + ',listener=null,name=' + JSON.stringify(selfName || 'Learner') + ';' +
      'function post(m){try{parent.postMessage(m,"*")}catch(e){}}' +
      'window.webxdc={selfAddr:"learner@lilith.local",selfName:name,' +
      'sendUpdate:function(u,d){u=u||{};var n=updates.length+1,upd={payload:u.payload,info:u.info,summary:u.summary,serial:n,max_serial:n};updates.push(upd);post({lilith:"update",update:upd});' +
      'if(upd.payload&&typeof upd.payload==="object"&&upd.payload.lilith==="complete")post({lilith:"complete"});if(listener)listener(upd);},' +
      'setUpdateListener:function(cb,serial){listener=cb;var s=serial||0;updates.forEach(function(u){if(u.serial>s)cb(u)});return Promise.resolve();},' +
      'getAllUpdates:function(){return Promise.resolve(updates)},sendToChat:function(){return Promise.resolve()},importFiles:function(){return Promise.resolve([])}};' +
      'window.lilith={complete:function(score){post({lilith:"complete",score:score})},report:function(m){post({lilith:"report",msg:String(m)})}};})();<\/script>';
  }

  /* turn a file map into one self-contained HTML document */
  function buildHtml(files, init, selfName) {
    var idx = files['index.html'];
    if (idx === undefined) throw new Error('The app has no index.html');
    var html = asText(idx);
    var get = function (p) { return files[norm(p)]; };
    html = html.replace(/<script([^>]*?)\ssrc=["']([^"']+)["']([^>]*)>\s*<\/script>/gi, function (m, a, src, b) {
      var f = get(src); if (f === undefined) return m;
      return '<script' + a + b + '>' + asText(f).replace(/<\/script/gi, '<\\/script') + '<\/script>';
    });
    html = html.replace(/<link([^>]*?)href=["']([^"']+)["']([^>]*)>/gi, function (m, a, href, b) {
      if (!/stylesheet/i.test(a + b)) return m;
      var f = get(href); if (f === undefined) return m;
      return '<style>' + asText(f).replace(/<\/style/gi, '<\\/style') + '</style>';
    });
    html = html.replace(/(<(?:img|source|audio|video)[^>]*?\ssrc=)["']([^"']+)["']/gi, function (m, pre, src) {
      var f = get(src); if (f === undefined || typeof f === 'string') return m;
      return pre + '"' + dataUri(src, f) + '"';
    });
    var sh = shim(init, selfName);
    if (/<head[^>]*>/i.test(html)) return html.replace(/<head[^>]*>/i, function (m) { return m + sh; });
    return sh + html;
  }

  /* a lab (or stored app) -> Promise<{html, name}> */
  function labToHtml(lab, init, selfName) {
    return Promise.resolve().then(function () {
      if (lab.xdc) return unzip(b64ToBytes(lab.xdc)).then(function (files) { return { html: buildHtml(files, init, selfName), name: manifest(files).name }; });
      if (lab.files && typeof lab.files === 'object') return { html: buildHtml(lab.files, init, selfName), name: '' };
      if (lab.html) return { html: buildHtml({ 'index.html': lab.html }, init, selfName), name: '' };
      throw new Error('This lab has no app inside.');
    });
  }

  var api = { b64ToBytes: b64ToBytes, bytesToB64: bytesToB64, isZip: isZip, unzip: unzip, manifest: manifest, buildHtml: buildHtml, labToHtml: labToHtml, shim: shim };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LilithXdc = api;
})(typeof window !== 'undefined' ? window : globalThis);
