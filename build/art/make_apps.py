# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = """<style>*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}
button.s{background:#3a2a5c;color:#f1ebff}.k{color:#c9b8e8}.ok{color:#8fe3a8}input[type=range]{width:100%}
canvas{width:100%;max-width:380px;display:block;margin:8px auto;background:#0e0820;border-radius:8px;touch-action:none}.sw{display:flex;flex-wrap:wrap;gap:6px}.sw div{width:84px;height:64px;border-radius:8px;font-size:11px;padding:4px;display:flex;align-items:flex-end}</style>"""
HARMONY = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + STYLE + """</head><body>
<div class="k">Base hue: <b id="hv">0</b>&deg;</div><input id="h" type="range" min="0" max="359" value="0">
<div><button class="s" data-k="complementary">complementary</button><button class="s" data-k="analogous">analogous</button><button class="s" data-k="triadic">triadic</button><button class="s" data-k="split">split-complementary</button></div>
<canvas id="c" width="260" height="260" style="max-width:260px"></canvas>
<div id="sw" class="sw"></div><div class="k" id="prog" style="margin-top:8px"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var kind="complementary",seen={};
function hsl(h,s,l){h=((h%360)+360)%360;s/=100;l/=100;var a=s*Math.min(l,1-l);function f(n){var k=(n+h/30)%12;var c=l-a*Math.max(-1,Math.min(k-3,9-k,1));return Math.round(255*c)}return[f(0),f(8),f(4)]}
function hex(c){return"#"+c.map(function(v){return(v<16?"0":"")+v.toString(16)}).join("").toUpperCase()}
var OFF={complementary:[0,180],analogous:[-30,0,30],triadic:[0,120,240],split:[0,150,210]};
function draw(){var base=+$("h").value;$("hv").textContent=base;var g=$("c").getContext("2d");g.clearRect(0,0,260,260);
 for(var a=0;a<360;a++){g.strokeStyle="hsl("+a+",80%,55%)";g.lineWidth=14;g.beginPath();var r=Math.PI*(a-90)/180;g.arc(130,130,100,r,r+0.03);g.stroke()}
 var hs=OFF[kind].map(function(o){return base+o}),sw=$("sw");sw.innerHTML="";
 hs.forEach(function(h){var hh=((h%360)+360)%360,r=Math.PI*(hh-90)/180;g.fillStyle="#fff";g.beginPath();g.arc(130+100*Math.cos(r),130+100*Math.sin(r),9,0,6.3);g.fill();
  var c=hsl(hh,75,50),d=document.createElement("div");d.style.background=hex(c);d.style.color="#111";d.textContent=Math.round(hh)+"\\u00b0 "+hex(c);sw.appendChild(d)});
 seen[kind]=1;var n=Object.keys(seen).length;$("prog").textContent="Harmonies tried: "+n+" of 4 needed";if(n>=4)done()}
$("h").oninput=draw;Array.prototype.forEach.call(document.querySelectorAll("button[data-k]"),function(b){b.onclick=function(){kind=b.getAttribute("data-k");draw()}});draw();
</script></body></html>"""
COMPOSE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + STYLE + """</head><body>
<div><button id="t" class="s">thirds</button><button id="gr" class="s">golden</button><button id="cl" class="s">clear</button></div>
<canvas id="c" width="380" height="250"></canvas>
<div id="msg" class="k">Tap to place the subject.</div><div id="prog" class="k" style="margin-top:6px"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var W=380,H=250,mode="thirds",px=190,py=125,hit={};
function pts(){var a=mode==="thirds"?1/3:0.381966,b=1-a;return[[W*a,H*a],[W*b,H*a],[W*a,H*b],[W*b,H*b]]}
function draw(){var g=$("c").getContext("2d");g.clearRect(0,0,W,H);var a=mode==="thirds"?1/3:0.381966,b=1-a;g.strokeStyle="#5c4a85";g.lineWidth=1;
 [a,b].forEach(function(f){g.beginPath();g.moveTo(W*f,0);g.lineTo(W*f,H);g.moveTo(0,H*f);g.lineTo(W,H*f);g.stroke()});
 pts().forEach(function(p){g.fillStyle="#3a2a5c";g.beginPath();g.arc(p[0],p[1],7,0,6.3);g.fill()});
 g.fillStyle="#b26bff";g.beginPath();g.arc(px,py,16,0,6.3);g.fill();g.fillStyle="#f1ebff";g.beginPath();g.arc(px+5,py-5,5,0,6.3);g.fill()}
function place(e){var r=$("c").getBoundingClientRect();px=(e.clientX-r.left)*W/r.width;py=(e.clientY-r.top)*H/r.height;draw();
 var best=-1,bd=1e9;pts().forEach(function(p,i){var d=Math.hypot(p[0]-px,p[1]-py);if(d<bd){bd=d;best=i}});
 if(bd<=22){hit[mode+best]=1;$("msg").innerHTML="<span class='ok'>On a strong point.</span>"}else{var cd=Math.hypot(px-W/2,py-H/2);$("msg").textContent=cd<22?"Dead centre: stable, but static.":"Try a glowing intersection."}
 var n=Object.keys(hit).length;$("prog").textContent="Strong points used: "+n+" of 3 needed";if(n>=3)done()}
var c=$("c");c.onpointerdown=function(e){place(e);c.onpointermove=place};c.onpointerup=function(){c.onpointermove=null};
$("t").onclick=function(){mode="thirds";draw()};$("gr").onclick=function(){mode="golden";draw()};$("cl").onclick=function(){px=190;py=125;hit={};draw();$("msg").textContent="Tap to place the subject."};draw();
</script></body></html>"""
def main():
    os.makedirs(os.path.join(HERE, "apps"), exist_ok=True)
    open(os.path.join(HERE, "apps", "harmony.html"), "w", encoding="utf-8").write(HARMONY)
    open(os.path.join(HERE, "apps", "compose.html"), "w", encoding="utf-8").write(COMPOSE)
if __name__ == "__main__":
    main(); print("ok")
