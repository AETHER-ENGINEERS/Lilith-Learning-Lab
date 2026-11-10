# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}button.s{background:#3a2a5c;color:#f1ebff}
canvas{width:100%;display:block;margin:6px 0;background:#0e0820;border-radius:8px;touch-action:none}.k{color:#c9b8e8}label{display:block;margin-top:6px}input[type=range]{width:100%;accent-color:#b26bff}
.ok{color:#8fe3a8;font-weight:600}
</style></head><body>"""
COMMON = """var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var _s=11;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff}function gauss(){var u=rnd()+1e-9,v=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}"""
PLOT = HEAD + """
<label>Dataset <select id="ds"><option value="house">House area vs price</option><option value="study">Study hours vs exam score</option><option value="ice">Temperature vs ice-cream sales</option><option value="noise">Unrelated noise (with outliers)</option></select>
Chart <select id="ch"><option value="scatter">Scatter</option><option value="hist">Histogram of y</option><option value="line">Line (in order)</option></select></label>
<canvas id="c" width="400" height="260"></canvas><div id="o" class="k"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var D={};(function(){var x=[],y=[],i;for(i=0;i<40;i++){var a=40+rnd()*160;x.push(a);y.push(a*1.8+20+gauss()*25)}D.house={x:x,y:y,xl:"area (m2)",yl:"price (k)"};
 x=[];y=[];for(i=0;i<40;i++){var h=rnd()*10;x.push(h);y.push(Math.min(100,45+h*5+gauss()*7))}D.study={x:x,y:y,xl:"hours studied",yl:"exam score"};
 x=[];y=[];for(i=0;i<40;i++){var t=5+rnd()*30;x.push(t);y.push(20+t*4+gauss()*12)}D.ice={x:x,y:y,xl:"temperature (C)",yl:"sales"};
 x=[];y=[];for(i=0;i<40;i++){x.push(rnd()*10);y.push(50+gauss()*8)}x.push(5);y.push(120);x.push(8);y.push(-10);D.noise={x:x,y:y,xl:"x",yl:"y"}})();
function mean(a){return a.reduce(function(s,v){return s+v},0)/a.length}
function sd(a){var m=mean(a);return Math.sqrt(mean(a.map(function(v){return (v-m)*(v-m)})))}
function corr(x,y){var mx=mean(x),my=mean(y),s=0;for(var i=0;i<x.length;i++)s+=(x[i]-mx)*(y[i]-my);return s/x.length/(sd(x)*sd(y))}
function q(a,p){var s=a.slice().sort(function(u,v){return u-v}),pos=p*(s.length-1),lo=Math.floor(pos);return lo+1>=s.length?s[lo]:s[lo]+(pos-lo)*(s[lo+1]-s[lo])}
var seen={};
function draw(){var d=D[$("ds").value],kind=$("ch").value,c=$("c").getContext("2d");c.clearRect(0,0,400,260);var x=d.x,y=d.y;
 var xmin=Math.min.apply(null,x),xmax=Math.max.apply(null,x),ymin=Math.min.apply(null,y),ymax=Math.max.apply(null,y);
 function X(v){return 40+(v-xmin)/(xmax-xmin||1)*340}function Y(v){return 230-(v-ymin)/(ymax-ymin||1)*210}
 c.strokeStyle="#5c4a85";c.beginPath();c.moveTo(40,10);c.lineTo(40,230);c.lineTo(390,230);c.stroke();c.fillStyle="#c9b8e8";c.fillText(d.xl,180,252);c.fillText(d.yl,2,12);
 if(kind==="scatter"){c.fillStyle="#b26bff";for(var i=0;i<x.length;i++){c.beginPath();c.arc(X(x[i]),Y(y[i]),3.5,0,7);c.fill()}}
 else if(kind==="line"){var o=x.map(function(_,i){return i}).sort(function(a,b){return x[a]-x[b]});c.strokeStyle="#b26bff";c.beginPath();o.forEach(function(i,j){if(j==0)c.moveTo(X(x[i]),Y(y[i]));else c.lineTo(X(x[i]),Y(y[i]))});c.stroke()}
 else{var nb=10,cnt=[],i;for(i=0;i<nb;i++)cnt.push(0);y.forEach(function(v){var b=Math.min(nb-1,Math.floor((v-ymin)/(ymax-ymin||1)*nb));cnt[b]++});var mx=Math.max.apply(null,cnt);c.fillStyle="#b26bff";cnt.forEach(function(n,b){var h=n/mx*200;c.fillRect(42+b*34,230-h,31,h)})}
 var r=corr(x,y),q1=q(y,0.25),q3=q(y,0.75),iq=q3-q1,out=y.filter(function(v){return v<q1-1.5*iq||v>q3+1.5*iq}).length;
 $("o").textContent="n="+x.length+"  mean y="+mean(y).toFixed(1)+"  std y="+sd(y).toFixed(1)+"  correlation r="+r.toFixed(2)+"  outliers (IQR rule): "+out;
 seen[$("ds").value]=1;var n=Object.keys(seen).length;$("p").textContent="Datasets viewed: "+n+" of 3 needed";if(n>=3)done()}
$("ds").onchange=draw;$("ch").onchange=draw;draw();
</script></body></html>"""
REG = HEAD + """
<div><button id="fit">Fit line</button><button id="out" class="s">Add outlier</button><button id="clr" class="s">Clear</button></div>
<canvas id="c" width="400" height="280"></canvas><div id="o" class="k">Tap the plot to add points.</div>
<script>""" + COMMON + """
var P=[],line=null,fitted=false;
function draw(){var c=$("c").getContext("2d");c.clearRect(0,0,400,280);c.strokeStyle="#5c4a85";c.beginPath();c.moveTo(0,140);c.lineTo(400,140);c.moveTo(200,0);c.lineTo(200,280);c.stroke();
 c.fillStyle="#b26bff";P.forEach(function(p){c.beginPath();c.arc(p[0],p[1],4.5,0,7);c.fill()});
 if(line){c.strokeStyle="#ffd36b";c.lineWidth=2;c.beginPath();c.moveTo(0,line[1]);c.lineTo(400,line[0]*400+line[1]);c.stroke();c.lineWidth=1}}
function fit(){var n=P.length;if(n<2)return;var mx=0,my=0;P.forEach(function(p){mx+=p[0];my+=p[1]});mx/=n;my/=n;var num=0,den=0;P.forEach(function(p){num+=(p[0]-mx)*(p[1]-my);den+=(p[0]-mx)*(p[0]-mx)});
 if(den<1e-9)return;var m=num/den,b=my-m*mx;line=[m,b];var sse=0,sst=0;P.forEach(function(p){var e=p[1]-(m*p[0]+b);sse+=e*e;sst+=(p[1]-my)*(p[1]-my)});
 $("o").textContent="slope "+(-m).toFixed(3)+" (screen up is positive), MSE "+(sse/n/100).toFixed(2)+", R squared "+(sst>0?(1-sse/sst).toFixed(3):"n/a")+", points "+n;
 fitted=true;if(n>=6)done();draw()}
$("c").onpointerdown=function(e){var r=$("c").getBoundingClientRect();P.push([(e.clientX-r.left)*400/r.width,(e.clientY-r.top)*280/r.height]);line=null;draw()};
$("fit").onclick=fit;$("out").onclick=function(){P.push([350,250]);line=null;draw()};$("clr").onclick=function(){P=[];line=null;$("o").textContent="Tap the plot to add points.";draw()};draw();
</script></body></html>"""
KNN = HEAD + """
<label>Dataset <select id="ds"><option value="blobs">Two blobs</option><option value="moons">Two moons</option><option value="rings">Rings</option></select></label>
<label>k = <b id="kv"></b><input id="k" type="range" min="1" max="25" value="5"></label>
<canvas id="c" width="400" height="300"></canvas><div id="o" class="k"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var D={};(function(){var b=[],i;for(i=0;i<40;i++){b.push([-1+gauss()*0.8,-1+gauss()*0.8,0]);b.push([1+gauss()*0.8,1+gauss()*0.8,1])}D.blobs=b;
 var m=[];for(i=0;i<40;i++){var t=rnd()*Math.PI;m.push([Math.cos(t)*1.2-0.6+gauss()*0.18,Math.sin(t)*1.2-0.3+gauss()*0.18,0]);var u=rnd()*Math.PI;m.push([0.6-Math.cos(u)*1.2+gauss()*0.18,-Math.sin(u)*1.2+0.3+gauss()*0.18,1])}D.moons=m;
 var r=[];for(i=0;i<50;i++){var a=rnd()*6.28;r.push([Math.cos(a)*0.7+gauss()*0.1,Math.sin(a)*0.7+gauss()*0.1,0]);a=rnd()*6.28;r.push([Math.cos(a)*1.6+gauss()*0.12,Math.sin(a)*1.6+gauss()*0.12,1])}D.rings=r})();
var seen={};
function pred(P,x,y,k){var d=P.map(function(p){return[(p[0]-x)*(p[0]-x)+(p[1]-y)*(p[1]-y),p[2]]}).sort(function(a,b){return a[0]-b[0]}),v=0;for(var i=0;i<k;i++)v+=d[i][1];return v*2>k?1:0}
function draw(){var P=D[$("ds").value],k=+$("k").value;$("kv").textContent=k;var c=$("c").getContext("2d");c.clearRect(0,0,400,300);
 var g=40,w=400/g,h=300/g;for(var i=0;i<g;i++)for(var j=0;j<g;j++){var x=-2.6+(i+0.5)/g*5.2,y=2.2-(j+0.5)/g*4.4;c.fillStyle=pred(P,x,y,k)?"rgba(255,211,107,0.25)":"rgba(178,107,255,0.25)";c.fillRect(i*w,j*h,w+1,h+1)}
 P.forEach(function(p){c.fillStyle=p[2]?"#ffd36b":"#b26bff";c.beginPath();c.arc((p[0]+2.6)/5.2*400,(2.2-p[1])/4.4*300,3.5,0,7);c.fill()});
 var ok=0;P.forEach(function(p,ix){var Q=P.filter(function(_,j){return j!==ix});if(pred(Q,p[0],p[1],Math.min(k,Q.length))===p[2])ok++});
 $("o").textContent="Leave-one-out accuracy at k="+k+": "+(ok/P.length*100).toFixed(0)+"%";
 seen[k<=2?"small":(k>=15?"large":"mid")]=1;var n=Object.keys(seen).length;$("p").textContent="Settings tried: "+n+" of 3 (small, middle, large k)";if(n>=3)done()}
$("ds").onchange=draw;$("k").oninput=draw;draw();
</script></body></html>"""
NN = HEAD + """
<label>Dataset <select id="ds"><option value="circle">Circle</option><option value="xor">XOR</option><option value="spiral">Spiral</option></select>
Hidden units <select id="hu"><option>2</option><option>4</option><option selected>8</option><option>16</option></select>
Learning rate <select id="lr"><option>0.03</option><option>0.1</option><option selected>0.3</option><option>1</option></select></label>
<div><button id="tr">Train 300 epochs</button><button id="rs" class="s">Reset</button></div>
<canvas id="c" width="400" height="300"></canvas><div id="o" class="k"></div>
<script>""" + COMMON + """
var P=[],W1,b1,W2,b2,H,ep=0,busy=false;
function data(){P=[];var i,n=100;var k=$("ds").value;
 if(k==="circle"){for(i=0;i<n;i++){var x=rnd()*4-2,y=rnd()*4-2;P.push([x,y,x*x+y*y<1.6?1:0])}}
 else if(k==="xor"){for(i=0;i<n;i++){var x2=rnd()*4-2,y2=rnd()*4-2;P.push([x2,y2,(x2>0)!==(y2>0)?1:0])}}
 else{for(i=0;i<n/2;i++){var t=i/(n/2)*3.2+0.3,r=t*0.5;P.push([r*Math.cos(t*2)+gauss()*0.05,r*Math.sin(t*2)+gauss()*0.05,0]);P.push([-r*Math.cos(t*2)+gauss()*0.05,-r*Math.sin(t*2)+gauss()*0.05,1])}}}
function init(){H=+$("hu").value;W1=[];b1=[];W2=[];b2=0;for(var j=0;j<H;j++){W1.push([gauss()*0.8,gauss()*0.8]);b1.push(0);W2.push(gauss()*0.5)}ep=0}
function fwd(x,y){var h=[],z=b2;for(var j=0;j<H;j++){var a=Math.tanh(W1[j][0]*x+W1[j][1]*y+b1[j]);h.push(a);z+=W2[j]*a}return{h:h,p:1/(1+Math.exp(-z))}}
function step(lr){var gW1=[],gb1=[],gW2=[],gb2=0,j;for(j=0;j<H;j++){gW1.push([0,0]);gb1.push(0);gW2.push(0)}var loss=0;
 P.forEach(function(s){var f=fwd(s[0],s[1]),d=f.p-s[2];loss+=-(s[2]*Math.log(f.p+1e-9)+(1-s[2])*Math.log(1-f.p+1e-9));gb2+=d;
  for(j=0;j<H;j++){gW2[j]+=d*f.h[j];var dh=d*W2[j]*(1-f.h[j]*f.h[j]);gW1[j][0]+=dh*s[0];gW1[j][1]+=dh*s[1];gb1[j]+=dh}});
 var n=P.length;b2-=lr*gb2/n;for(j=0;j<H;j++){W2[j]-=lr*gW2[j]/n;W1[j][0]-=lr*gW1[j][0]/n;W1[j][1]-=lr*gW1[j][1]/n;b1[j]-=lr*gb1[j]/n}ep++;return loss/n}
function draw(loss){var c=$("c").getContext("2d");c.clearRect(0,0,400,300);var g=40,w=400/g,h=300/g,i,j;
 for(i=0;i<g;i++)for(j=0;j<g;j++){var x=-2.6+(i+0.5)/g*5.2,y=2.2-(j+0.5)/g*4.4,p=fwd(x,y).p;c.fillStyle=p>0.5?"rgba(255,211,107,"+(0.1+0.3*(p-0.5)*2)+")":"rgba(178,107,255,"+(0.1+0.3*(0.5-p)*2)+")";c.fillRect(i*w,j*h,w+1,h+1)}
 var ok=0;P.forEach(function(s){c.fillStyle=s[2]?"#ffd36b":"#b26bff";c.beginPath();c.arc((s[0]+2.6)/5.2*400,(2.2-s[1])/4.4*300,3.5,0,7);c.fill();if((fwd(s[0],s[1]).p>0.5?1:0)===s[2])ok++});
 var acc=ok/P.length*100;$("o").innerHTML="Epochs: "+ep+" | loss "+(loss===undefined?"-":loss.toFixed(3))+" | accuracy "+acc.toFixed(0)+"%"+(acc>=95?' <span class="ok">Target reached!</span>':"");if(acc>=95&&ep>0)done()}
function train(){if(busy)return;busy=true;var lr=+$("lr").value,n=0,loss;var iv=setInterval(function(){for(var i=0;i<10;i++){loss=step(lr);n++}draw(loss);if(n>=300){clearInterval(iv);busy=false}},20)}
$("tr").onclick=train;$("rs").onclick=function(){if(busy)return;_s=11;data();init();draw()};$("ds").onchange=function(){if(busy)return;_s=11;data();init();draw()};$("hu").onchange=function(){if(busy)return;init();draw()};
data();init();draw();
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    for n, t in (("plot", PLOT), ("reg", REG), ("knn", KNN), ("nn", NN)):
        open(os.path.join(d, n + ".html"), "w").write(t)
