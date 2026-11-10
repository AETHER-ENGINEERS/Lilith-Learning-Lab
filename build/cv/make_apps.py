# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}button.s{background:#3a2a5c;color:#f1ebff}
canvas{display:block;margin:6px auto;background:#0e0820;border-radius:8px;touch-action:none;max-width:100%}.k{color:#c9b8e8}label{display:block;margin-top:6px}input[type=range]{width:100%;accent-color:#b26bff}
input.n{width:3.4em;background:#2a1b48;color:#f1ebff;border:1px solid #5c4a85;border-radius:6px;padding:4px;margin:1px;text-align:center}
</style></head><body>"""
COMMON = """var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}"""
KERNEL = HEAD + """
<label>Image <select id="im"><option value="shapes">Shapes</option><option value="grad">Gradient + square</option><option value="noise">Noisy square</option></select>
Preset <select id="pr"><option value="id">Identity</option><option value="blur">Box blur</option><option value="gauss">Gaussian blur</option><option value="sharp">Sharpen</option><option value="edge">Edge (Laplacian)</option><option value="sobx">Sobel X</option><option value="soby">Sobel Y</option><option value="emb">Emboss</option></select></label>
<div id="kg"></div>
<div style="display:flex;gap:8px;justify-content:center"><canvas id="a" width="160" height="160"></canvas><canvas id="b" width="160" height="160"></canvas></div>
<div class="k" style="text-align:center">Original and filtered</div><div id="o" class="k"></div>
<script>""" + COMMON + """
var N=32,K=[[0,0,0],[0,1,0],[0,0,0]],seed=5;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff}
var PR={id:[[0,0,0],[0,1,0],[0,0,0]],blur:[[1,1,1],[1,1,1],[1,1,1]].map(function(r){return r.map(function(v){return +(v/9).toFixed(3)})}),
 gauss:[[1,2,1],[2,4,2],[1,2,1]].map(function(r){return r.map(function(v){return +(v/16).toFixed(3)})}),sharp:[[0,-1,0],[-1,5,-1],[0,-1,0]],edge:[[0,1,0],[1,-4,1],[0,1,0]],
 sobx:[[-1,0,1],[-2,0,2],[-1,0,1]],soby:[[-1,-2,-1],[0,0,0],[1,2,1]],emb:[[-2,-1,0],[-1,1,1],[0,1,2]]};
function mk(kind){var I=[],r,c;for(r=0;r<N;r++){I.push([]);for(c=0;c<N;c++){var v=30;
  if(kind==="shapes"){if(r>5&&r<16&&c>5&&c<16)v=220;var dx=c-23,dy=r-22;if(dx*dx+dy*dy<30)v=140}
  else if(kind==="grad"){v=c*4;if(r>10&&r<22&&c>10&&c<22)v=250}
  else{if(r>8&&r<24&&c>8&&c<24)v=200;v+=(rnd()-0.5)*90}
  I[r].push(Math.max(0,Math.min(255,v)))}}return I}
var img=mk("shapes"),used={};
function conv(I){var O=[],r,c,i,j;for(r=0;r<N;r++){O.push([]);for(c=0;c<N;c++){var s=0;for(i=-1;i<=1;i++)for(j=-1;j<=1;j++){var rr=Math.max(0,Math.min(N-1,r+i)),cc=Math.max(0,Math.min(N-1,c+j));s+=K[i+1][j+1]*I[rr][cc]}O[r].push(s)}}return O}
function show(cv,I,off){var g=document.getElementById(cv).getContext("2d"),s=160/N;for(var r=0;r<N;r++)for(var c=0;c<N;c++){var v=Math.max(0,Math.min(255,I[r][c]+off));g.fillStyle="rgb("+v+","+v+","+v+")";g.fillRect(c*s,r*s,s+0.5,s+0.5)}}
function grid(){var h="",i,j;for(i=0;i<3;i++){for(j=0;j<3;j++)h+='<input class="n" data-i="'+i+'" data-j="'+j+'" value="'+K[i][j]+'">';h+="<br>"}$("kg").innerHTML=h;
 var ins=document.querySelectorAll("#kg input");for(var q=0;q<ins.length;q++)ins[q].onchange=function(){K[+this.dataset.i][+this.dataset.j]=parseFloat(this.value)||0;run(true)}}
function run(custom){var s=0;K.forEach(function(r){r.forEach(function(v){s+=v})});var out=conv(img);var off=(s===0)?128:0;show("a",img,0);show("b",out,off);
 var key=K.join(";");used[key]=1;var n=Object.keys(used).length;$("o").textContent="Kernel sum = "+s.toFixed(2)+(s===0?" (edge-type kernel: result shown with +128 offset)":"")+". Kernels tried: "+n+" of 4";if(n>=4)done()}
$("pr").onchange=function(){K=PR[this.value].map(function(r){return r.slice()});grid();run()};
$("im").onchange=function(){seed=5;img=mk(this.value);run()};
grid();run();
</script></body></html>"""
BOXES = HEAD + """
<div class="k">1) Drag the orange box over the purple one to see IoU.</div>
<canvas id="a" width="400" height="200"></canvas><div id="i" class="k"></div>
<div class="k" style="margin-top:10px">2) Non-maximum suppression on five detections of two objects.</div>
<label>IoU threshold: <b id="tv"></b><input id="th" type="range" min="5" max="95" value="50"></label>
<canvas id="n" width="400" height="200"></canvas><div id="o" class="k"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var A=[60,50,180,150],B=[140,80,260,180],drag=null;
function iou(a,b){var x1=Math.max(a[0],b[0]),y1=Math.max(a[1],b[1]),x2=Math.min(a[2],b[2]),y2=Math.min(a[3],b[3]),w=x2-x1,h=y2-y1;if(w<=0||h<=0)return 0;var i=w*h,u=(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-i;return i/u}
function rect(g,b,col,w){g.strokeStyle=col;g.lineWidth=w||2;g.strokeRect(b[0],b[1],b[2]-b[0],b[3]-b[1])}
function d1(){var g=$("a").getContext("2d");g.clearRect(0,0,400,200);g.fillStyle="rgba(178,107,255,0.25)";g.fillRect(A[0],A[1],A[2]-A[0],A[3]-A[1]);g.fillStyle="rgba(255,160,60,0.25)";g.fillRect(B[0],B[1],B[2]-B[0],B[3]-B[1]);rect(g,A,"#b26bff");rect(g,B,"#ff9f3c");
 $("i").textContent="IoU = "+iou(A,B).toFixed(3)}
$("a").onpointerdown=function(e){var r=this.getBoundingClientRect();var x=(e.clientX-r.left)*400/r.width,y=(e.clientY-r.top)*200/r.height;if(x>B[0]&&x<B[2]&&y>B[1]&&y<B[3])drag=[x-B[0],y-B[1]]};
$("a").onpointermove=function(e){if(!drag)return;var r=this.getBoundingClientRect();var x=(e.clientX-r.left)*400/r.width-drag[0],y=(e.clientY-r.top)*200/r.height-drag[1],w=B[2]-B[0],h=B[3]-B[1];B=[x,y,x+w,y+h];d1()};
window.addEventListener("pointerup",function(){drag=null});
var DET=[[40,40,140,140,0.95],[48,46,150,146,0.9],[35,50,135,150,0.6],[230,70,350,170,0.85],[242,64,356,176,0.7]];
var seen={};
function nms(thr){var o=DET.map(function(d,i){return i}).sort(function(a,b){return DET[b][4]-DET[a][4]}),keep=[];o.forEach(function(i){var ok=true;keep.forEach(function(j){if(iou(DET[i],DET[j])>thr)ok=false});if(ok)keep.push(i)});return keep}
function d2(){var thr=$("th").value/100;$("tv").textContent=thr.toFixed(2);var keep=nms(thr),g=$("n").getContext("2d");g.clearRect(0,0,400,200);
 DET.forEach(function(d,i){var k=keep.indexOf(i)>=0;g.setLineDash(k?[]:[4,4]);rect(g,d,k?"#8fe3a8":"#7a6a9a",k?3:1);g.fillStyle="#c9b8e8";g.fillText(d[4].toFixed(2),d[0]+3,d[1]+12)});g.setLineDash([]);
 $("o").textContent="Kept "+keep.length+" of 5 boxes (solid green). Lower thresholds suppress more.";seen[keep.length]=1;var n=Object.keys(seen).length;$("p").textContent="Distinct outcomes seen: "+n+" of 3";if(n>=3)done()}
$("th").oninput=d2;d1();d2();
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "kernel.html"), "w").write(KERNEL)
    open(os.path.join(d, "boxes.html"), "w").write(BOXES)
