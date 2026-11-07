/* Concept-map parser and layout (pure functions, no DOM).
   Syntax inside a ```conceptmap block:
     title: Map title
     Source [ch10] | relation | Target
   A [chN] tag on any node makes it a link to chapter N. Same label = same node. */
(function (root) {
  'use strict';

  function parseOne(body) {
    var map = { title: 'Concept map', nodes: [], edges: [] }, byId = {};
    function node(raw) {
      var ch = null, label = raw.trim();
      var m = /\s*\[ch(\d+)\]\s*$/.exec(label);
      if (m) { ch = parseInt(m[1], 10); label = label.slice(0, m.index).trim(); }
      var n = byId[label];
      if (!n) { n = byId[label] = { id: label, label: label, ch: null, out: [], inn: [] }; map.nodes.push(n); }
      if (ch !== null) n.ch = ch;
      return n;
    }
    body.split('\n').forEach(function (ln) {
      ln = ln.trim(); if (!ln) return;
      var t = /^title:\s*(.*)$/.exec(ln);
      if (t) { map.title = t[1]; return; }
      var p = ln.split('|');
      if (p.length !== 3) return;
      var a = node(p[0]), b = node(p[2]);
      var e = { from: a.id, to: b.id, rel: p[1].trim() };
      map.edges.push(e); a.out.push(e); b.inn.push(e);
    });
    return map;
  }

  function parseMaps(md) {
    var maps = [], re = /```conceptmap\n([\s\S]*?)```/g, m;
    while ((m = re.exec(md))) maps.push(parseOne(m[1]));
    return maps;
  }

  function wrap(label, max) {
    var words = label.split(' '), lines = [], cur = '';
    words.forEach(function (w) {
      if ((cur + ' ' + w).trim().length > max && cur) { lines.push(cur); cur = w; } else cur = (cur + ' ' + w).trim();
    });
    if (cur) lines.push(cur);
    return lines.slice(0, 3);
  }

  function layout(map, o) {
    o = o || {};
    var W = o.nodeW || 132, GX = o.gapX || 16, GY = o.gapY || 84, PAD = 14, LH = 14;
    var by = {}; map.nodes.forEach(function (n) { by[n.id] = n; });
    // levels by BFS from nodes without incoming edges (first one first)
    var level = {}, order = [], queue = [];
    var roots = map.nodes.filter(function (n) { return n.inn.length === 0; });
    if (!roots.length && map.nodes.length) roots = [map.nodes[0]];
    roots.forEach(function (r) { level[r.id] = 0; queue.push(r.id); order.push(r.id); });
    while (queue.length) {
      var id = queue.shift();
      by[id].out.forEach(function (e) {
        if (level[e.to] === undefined) { level[e.to] = level[id] + 1; queue.push(e.to); order.push(e.to); }
      });
    }
    map.nodes.forEach(function (n) { if (level[n.id] === undefined) { level[n.id] = 0; order.push(n.id); } });
    var maxL = 0; order.forEach(function (id) { if (level[id] > maxL) maxL = level[id]; });
    var rows = []; for (var i = 0; i <= maxL; i++) rows.push([]);
    order.forEach(function (id) { rows[level[id]].push(id); });

    var pos = {};
    function height(n) { return 16 + LH * wrap(n.label, 17).length; }
    rows.forEach(function (row, L) {
      var desired = row.map(function (id, idx) {
        var ps = by[id].inn.filter(function (e) { return level[e.from] < L && pos[e.from]; });
        if (!ps.length) return { id: id, d: idx * (W + GX) + W / 2 };
        var s = 0; ps.forEach(function (e) { s += pos[e.from].x + W / 2; });
        return { id: id, d: s / ps.length };
      });
      desired.sort(function (a, b) { return a.d - b.d; });
      var right = -Infinity;
      desired.forEach(function (it) {
        var x = Math.max(right + GX, it.d - W / 2);
        pos[it.id] = { x: x, y: PAD + L * (GY + 40) };
        right = x + W;
      });
    });
    var minX = Infinity, maxX = -Infinity;
    Object.keys(pos).forEach(function (k) { minX = Math.min(minX, pos[k].x); maxX = Math.max(maxX, pos[k].x + W); });
    var shift = PAD - minX;
    var nodes = map.nodes.map(function (n) {
      var p = pos[n.id], lines = wrap(n.label, 17);
      return { id: n.id, label: n.label, ch: n.ch, x: p.x + shift, y: p.y, w: W, h: height(n), lines: lines, level: level[n.id] };
    });
    var np = {}; nodes.forEach(function (n) { np[n.id] = n; });
    var edges = map.edges.map(function (e) {
      var a = np[e.from], b = np[e.to], d, lx, ly;
      if (b.level > a.level) {
        var sx = a.x + a.w / 2, sy = a.y + a.h, tx = b.x + b.w / 2, ty = b.y, dy = (ty - sy) / 2;
        d = 'M' + sx + ',' + sy + ' C' + sx + ',' + (sy + dy) + ' ' + tx + ',' + (ty - dy) + ' ' + tx + ',' + ty;
        lx = (sx + tx) / 2; ly = (sy + ty) / 2;
      } else {
        var sx2 = a.x + a.w, sy2 = a.y + a.h / 2, tx2 = b.x + b.w, ty2 = b.y + b.h / 2, bulge = 46;
        d = 'M' + sx2 + ',' + sy2 + ' C' + (sx2 + bulge) + ',' + sy2 + ' ' + (tx2 + bulge) + ',' + ty2 + ' ' + tx2 + ',' + ty2;
        lx = Math.max(sx2, tx2) + bulge * 0.75; ly = (sy2 + ty2) / 2;
      }
      return { from: e.from, to: e.to, rel: e.rel, d: d, lx: lx, ly: ly };
    });
    var width = maxX - minX + PAD * 2 + 50, height2 = PAD + (maxL + 1) * (GY + 40);
    var outline = map.edges.map(function (e) { return e.from + ' ' + e.rel + ' ' + e.to; });
    return { title: map.title, nodes: nodes, edges: edges, width: Math.ceil(width), height: Math.ceil(height2), outline: outline };
  }

  var api = { parseMaps: parseMaps, layout: layout, wrap: wrap };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LilithMaps = api;
})(typeof window !== 'undefined' ? window : globalThis);
