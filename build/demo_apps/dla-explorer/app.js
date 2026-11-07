var TYPES = [
  ['conv', null], ['relu', null], ['batchnorm', null], ['pool', null], ['concat', null],
  ['resize nearest x2', null], ['deconv pad 0', null],
  ['softmax', 'Softmax is Orin only'], ['gelu', 'GELU is not a DLA activation'], ['deconv pad 1', 'deconv padding must be 0'],
  ['resize bilinear x2.5', 'resize needs an integer scale'], ['argmax', 'ArgMax is not supported']
];
var model = [], done = false;
var pal = document.getElementById('pal'), stack = document.getElementById('stack'), stat = document.getElementById('stat');
TYPES.forEach(function (t, i) {
  var b = document.createElement('button'); b.textContent = '+ ' + t[0];
  b.onclick = function () { model.push(i); save(); draw(); }; pal.appendChild(b);
});
function save() { webxdc.sendUpdate({ payload: { model: model } }, 'model'); }
function draw() {
  stack.innerHTML = ''; var gpu = 0, sub = 0, prev = null;
  model.forEach(function (i, k) {
    var why = TYPES[i][1], dev = why ? 'gpu' : 'dla';
    if (why) gpu++; if (dev === 'dla' && prev !== 'dla') sub++; prev = dev;
    var d = document.createElement('div'); d.className = 'l ' + dev;
    d.innerHTML = '<span>' + (k + 1) + '. ' + TYPES[i][0] + (why ? '<small>' + why + '</small>' : '') + '</span><b>' + dev.toUpperCase() + '</b>';
    d.onclick = function () { model.splice(k, 1); save(); draw(); }; stack.appendChild(d);
  });
  var last = TYPES[model[model.length - 1]];
  var ok = model.length >= 4 && sub === 1 && gpu <= 1 && (gpu === 0 || (last && last[0] === 'argmax'));
  stat.className = ok ? 'win' : '';
  stat.textContent = model.length + ' layers, ' + sub + ' DLA subgraph(s), ' + gpu + ' GPU layer(s). ' + (ok ? 'Great: this runs almost entirely on the DLA.' : 'Tap a layer to remove it.');
  if (ok && !done) { done = true; if (window.lilith) lilith.complete(); }
}
document.getElementById('clear').onclick = function () { model = []; done = false; save(); draw(); };
document.getElementById('demo').onclick = function () { model = [0, 8, 0, 7, 9, 1, 10, 0, 11]; done = false; save(); draw(); };
webxdc.setUpdateListener(function (u) { if (u.payload && u.payload.model) { model = u.payload.model; draw(); } }, 0);
draw();
