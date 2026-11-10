# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}button.s{background:#3a2a5c;color:#f1ebff}
canvas{width:100%;display:block;margin:6px 0;background:#0e0820;border-radius:8px}.k{color:#c9b8e8}input[type=range]{width:100%;accent-color:#b26bff}label{display:block;margin-top:6px}
</style></head><body>"""
ALIAS = HEAD + """
<label>Tone 1: <b id="v1"></b> Hz<input id="f1" type="range" min="1" max="60" value="5"></label>
<label>Tone 2: <b id="v2"></b> Hz<input id="f2" type="range" min="0" max="60" value="0"></label>
<label>Sample rate: <b id="vs"></b> Hz<input id="fs" type="range" min="8" max="120" value="100"></label>
<canvas id="w" width="400" height="150"></canvas><canvas id="p" width="400" height="150"></canvas>
<div id="o" class="k"></div><div id="g" class="k"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var n=0,fsChanged=false;
function sig(t){var a=Math.sin(2*Math.PI*F1*t);if(F2>0)a+=Math.sin(2*Math.PI*F2*t);return a}
var F1,F2,FS;
function upd(){F1=+$("f1").value;F2=+$("f2").value;FS=+$("fs").value;$("v1").textContent=F1;$("v2").textContent=F2||"off";$("vs").textContent=FS;
 var g=$("w").getContext("2d");g.clearRect(0,0,400,150);g.strokeStyle="#5c4a85";g.beginPath();
 for(var x=0;x<=400;x++){var t=x/400*0.5,y=75-sig(t)*30;if(x==0)g.moveTo(x,y);else g.lineTo(x,y)}g.stroke();
 g.fillStyle="#ffd36b";for(var k=0;k/FS<0.5;k++){var t=k/FS;g.beginPath();g.arc(t/0.5*400,75-sig(t)*30,3,0,7);g.fill()}
 var N=128,X=[],mx=0;for(var b=0;b<=N/2;b++){var re=0,im=0;for(var i=0;i<N;i++){var a=2*Math.PI*b*i/N,s=sig(i/FS);re+=s*Math.cos(a);im-=s*Math.sin(a)}var m=Math.sqrt(re*re+im*im)/N*2;X.push(m)}
 var p=$("p").getContext("2d");p.clearRect(0,0,400,150);p.fillStyle="#b26bff";var peaks=[];
 for(var b=0;b<X.length;b++){var h=Math.min(X[b],1.5)/1.5*120;p.fillRect(b/(N/2)*390+2,140-h,4,h);if(X[b]>0.4)peaks.push((b*FS/N).toFixed(1))}
 p.fillStyle="#c9b8e8";p.fillText("0",2,148);p.fillText((FS/2)+" Hz (Nyquist)",300,148);
 var t1=F1,t2=F2,over=(F1>FS/2)||(F2>FS/2);
 $("o").textContent="Spectrum peaks seen at: "+(peaks.join(", ")||"none")+" Hz";
 $("g").textContent=over?"A tone is above "+(FS/2)+" Hz, so it aliases to a lower frequency.":"Both tones are below Nyquist ("+(FS/2)+" Hz): shown correctly.";
 n++;if(n>6&&fsChanged)done()}
["f1","f2"].forEach(function(i){$(i).oninput=upd});$("fs").oninput=function(){fsChanged=true;upd()};upd();
</script></body></html>"""
FILTER = HEAD + """
<div><button id="ma">Moving average (8)</button><button id="df" >Difference</button><button id="ws">Windowed sinc</button><button id="rs" class="s">Raw signal</button></div>
<canvas id="w" width="400" height="140"></canvas><canvas id="p" width="400" height="140"></canvas>
<div id="o" class="k">Signal = 3 Hz tone + 40 Hz tone + noise, sampled at 200 Hz.</div><div id="g" class="k"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var FS=200,N=200,x=[],seed=7;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff-0.5}
for(var i=0;i<N;i++)x.push(Math.sin(2*Math.PI*3*i/FS)+0.6*Math.sin(2*Math.PI*40*i/FS)+0.2*rnd());
function conv(b){var y=[];for(var n=0;n<N;n++){var s=0;for(var k=0;k<b.length;k++)if(n-k>=0)s+=b[k]*x[n-k];y.push(s)}return y}
function spec(y){var X=[];for(var b=0;b<=60;b++){var re=0,im=0;for(var i=0;i<N;i++){var a=2*Math.PI*b*i/N;re+=y[i]*Math.cos(a);im-=y[i]*Math.sin(a)}X.push(Math.sqrt(re*re+im*im)/N*2)}return X}
function sinc(c,m){var h=[],s=0,cen=(m-1)/2;for(var k=0;k<m;k++){var u=2*c*(k-cen),v=u==0?1:Math.sin(Math.PI*u)/(Math.PI*u);var w=0.5-0.5*Math.cos(2*Math.PI*k/(m-1));h.push(2*c*v*w);s+=2*c*v*w}return h.map(function(a){return a/s})}
var tried={};
function show(y,name){var g=$("w").getContext("2d");g.clearRect(0,0,400,140);g.strokeStyle="#b26bff";g.beginPath();for(var i=0;i<N;i++){var X=i/N*400,Y=70-y[i]*35;if(i==0)g.moveTo(X,Y);else g.lineTo(X,Y)}g.stroke();
 var S=spec(y),p=$("p").getContext("2d");p.clearRect(0,0,400,140);p.fillStyle="#ffd36b";for(var b=0;b<S.length;b++){var h=Math.min(S[b],1.2)/1.2*110;p.fillRect(b/60*385+2,128-h,5,h)}
 p.fillStyle="#c9b8e8";p.fillText("0 Hz",2,138);p.fillText("60 Hz",360,138);$("g").textContent=name}
$("rs").onclick=function(){show(x,"Raw signal: peaks at 3 Hz and 40 Hz")};
$("ma").onclick=function(){show(conv([1,1,1,1,1,1,1,1].map(function(a){return a/8})),"Moving average: the 40 Hz tone is strongly reduced");tried.ma=1;chk()};
$("df").onclick=function(){show(conv([1,-1]),"Difference: the slow 3 Hz tone is weakened, high content stays");tried.df=1;chk()};
$("ws").onclick=function(){show(conv(sinc(0.08,31)),"Windowed sinc, cutoff 16 Hz: a clean low-pass");tried.ws=1;chk()};
function chk(){if(tried.ma&&tried.df&&tried.ws)done()}
show(x,"Raw signal: peaks at 3 Hz and 40 Hz");
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "alias.html"), "w").write(ALIAS)
    open(os.path.join(d, "filter.html"), "w").write(FILTER)
