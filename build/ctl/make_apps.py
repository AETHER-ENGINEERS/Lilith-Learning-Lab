# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
canvas{width:100%;display:block;margin:6px 0;background:#0e0820;border-radius:8px}.k{color:#c9b8e8}input[type=range]{width:100%;accent-color:#b26bff}label{display:block;margin-top:6px}
.ok{color:#8fe3a8;font-weight:600}.bad{color:#ff8f8f;font-weight:600}
</style></head><body>"""
POLES = HEAD + """
<label>Real part of pole: <b id="vs"></b><input id="s" type="range" min="-40" max="10" value="-10"></label>
<label>Imaginary part: <b id="vw"></b><input id="w" type="range" min="0" max="60" value="30"></label>
<canvas id="m" width="400" height="140"></canvas><canvas id="r" width="400" height="180"></canvas>
<div id="o" class="k"></div><div id="prog" class="k"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var seen={};
function upd(){var s=$("s").value/10,w=$("w").value/10;$("vs").textContent=s.toFixed(1);$("vw").textContent=w.toFixed(1);
 var m=$("m").getContext("2d");m.clearRect(0,0,400,140);m.fillStyle="#2a1b48";m.fillRect(0,0,200,140);m.strokeStyle="#5c4a85";m.beginPath();m.moveTo(200,0);m.lineTo(200,140);m.moveTo(0,70);m.lineTo(400,70);m.stroke();
 m.fillStyle="#c9b8e8";m.fillText("stable",70,14);m.fillText("unstable",290,14);
 var px=200+s*40,py=70-w*20;m.fillStyle="#ffd36b";[py,140-py].forEach(function(y){m.beginPath();m.arc(px,y,5,0,7);m.fill()});
 var a0=s*s+w*w,a1=-2*s,y=0,v=0,dt=0.002,pts=[],pk=0;
 for(var i=0;i<=5000;i++){if(i%12==0)pts.push(y);var acc=a0*(1-y)-a1*v;v+=dt*acc;y+=dt*v;if(Math.abs(y)>1e6)break}
 var g=$("r").getContext("2d");g.clearRect(0,0,400,180);g.strokeStyle="#5c4a85";g.beginPath();g.moveTo(0,130-100);g.lineTo(400,30);g.stroke();
 g.strokeStyle="#b26bff";g.beginPath();for(var j=0;j<pts.length;j++){var Y=Math.max(-20,Math.min(200,130-pts[j]*100)),X=j/pts.length*400;if(j==0)g.moveTo(X,Y);else g.lineTo(X,Y)}g.stroke();
 var kind,msg;
 if(s>=0.05){kind="unstable";msg="Unstable: a pole in the right half-plane makes the response grow."}
 else if(w>1&&s<-0.05){kind="osc";msg="Stable and oscillating: ringing that decays."}
 else if(s<-0.05){kind="stable";msg="Stable and smooth: decays without much ringing."}
 else{kind="marginal";msg="Marginal: no decay."}
 $("o").innerHTML='<span class="'+(kind=="unstable"?"bad":"ok")+'">'+msg+'</span>';
 seen[kind]=1;var n=(seen.unstable?1:0)+(seen.osc?1:0)+(seen.stable?1:0);$("prog").textContent="Cases seen: "+n+" of 3 (smooth, oscillating, unstable)";if(n>=3)done()}
$("s").oninput=upd;$("w").oninput=upd;upd();
</script></body></html>"""
PID = HEAD + """
<label>Kp: <b id="a"></b><input id="kp" type="range" min="0" max="100" value="20"></label>
<label>Ki: <b id="b"></b><input id="ki" type="range" min="0" max="100" value="0"></label>
<label>Kd: <b id="c"></b><input id="kd" type="range" min="0" max="50" value="0"></label>
<canvas id="cv" width="400" height="200"></canvas>
<div id="o" class="k"></div>
<div class="k" style="font-size:12px">Plant: a lag (time constant 1 s) with 0.2 s delay. Setpoint 1. Command limited to -5..5.</div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
function run(kp,ki,kd){var dt=0.01,T=10,n=T/dt,y=0,I=0,prev=1,ud=[],hist=[],D=20;for(var i=0;i<D;i++)ud.push(0);
 for(var k=0;k<n;k++){var e=1-y;I+=e*dt;var d=(e-prev)/dt;prev=e;var u=kp*e+ki*I+kd*d;if(u>5){u=5;if(e>0)I-=e*dt}if(u<-5){u=-5;if(e<0)I-=e*dt}
  ud.push(u);var uu=ud.shift();y+=dt*(uu-y);if(!isFinite(y)||Math.abs(y)>1e4){y=1e4*(y<0?-1:1)}hist.push(y)}return hist}
function upd(){var kp=$("kp").value/10,ki=$("ki").value/10,kd=$("kd").value/10;$("a").textContent=kp.toFixed(1);$("b").textContent=ki.toFixed(1);$("c").textContent=kd.toFixed(1);
 var h=run(kp,ki,kd),g=$("cv").getContext("2d");g.clearRect(0,0,400,200);g.strokeStyle="#5c4a85";g.beginPath();g.moveTo(0,160-100);g.lineTo(400,60);g.stroke();
 g.strokeStyle="#b26bff";g.beginPath();for(var i=0;i<h.length;i+=5){var Y=Math.max(0,Math.min(200,160-h[i]*100)),X=i/h.length*400;if(i==0)g.moveTo(X,Y);else g.lineTo(X,Y)}g.stroke();
 var mx=Math.max.apply(null,h),os=Math.max(0,(mx-1)*100),st=-1;for(var i=h.length-1;i>=0;i--){if(Math.abs(h[i]-1)>0.02){st=(i+1)*0.01;break}}
 var fin=Math.abs(h[h.length-1]-1)<0.02&&isFinite(mx)&&mx<100;
 var s=fin?(st<0?0:st).toFixed(2)+" s":"does not settle";
 var good=fin&&os<10&&st<8;
 $("o").innerHTML="Overshoot: "+(mx>100?"huge":os.toFixed(1)+"%")+" | Settling (2%): "+s+" | Final error: "+(Math.abs(h[h.length-1]-1)*100).toFixed(1)+"%<br>"+(good?'<span class="ok">Good tuning!</span>':'<span class="bad">Not yet: aim for overshoot below 10% and settling within a few seconds.</span>');
 if(good)done()}
["kp","ki","kd"].forEach(function(i){$(i).oninput=upd});upd();
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "poles.html"), "w").write(POLES)
    open(os.path.join(d, "pid.html"), "w").write(PID)
