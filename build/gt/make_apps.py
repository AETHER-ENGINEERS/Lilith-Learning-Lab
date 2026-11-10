# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}button.s{background:#3a2a5c;color:#f1ebff}
canvas{width:100%;display:block;margin:6px 0;background:#0e0820;border-radius:8px}.k{color:#c9b8e8}label{display:block;margin-top:6px}input[type=range]{width:100%;accent-color:#b26bff}
table{border-collapse:collapse;width:100%}td,th{padding:4px 6px;border-bottom:1px solid #3a2a5c;text-align:left}
</style></head><body>"""
TOURN = HEAD + """
<div class="k">Payoffs: both cooperate 3 each, both defect 1 each, defector 5 vs cooperator 0. 50 rounds per match.</div>
<div id="list"></div>
<label>Your rule: <select id="mine"><option value="tft">Tit for tat</option><option value="tf2t">Tit for two tats (forgiving)</option><option value="grim">Grim trigger</option><option value="alld">Always defect</option><option value="allc">Always cooperate</option><option value="rand">Random</option><option value="pavlov">Pavlov (win-stay, lose-shift)</option></select></label>
<div><button id="run">Run tournament</button></div>
<div id="out"></div><div id="g" class="k"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var NAMES={tft:"Tit for tat",tf2t:"Tit for two tats",grim:"Grim trigger",alld:"Always defect",allc:"Always cooperate",rand:"Random",pavlov:"Pavlov"};
var seed=3;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff}
function move(k,my,th,st){var n=my.length;
 if(k==="tft")return n==0?"C":th[n-1];
 if(k==="tf2t")return (n>=2&&th[n-1]==="D"&&th[n-2]==="D")?"D":"C";
 if(k==="grim")return th.indexOf("D")>=0?"D":"C";
 if(k==="alld")return "D";if(k==="allc")return "C";if(k==="rand")return rnd()<0.5?"C":"D";
 if(k==="pavlov"){if(n==0)return "C";var m=my[n-1],t=th[n-1];return (m===t)?"C":"D"}}
function pay(a,b){return a==="C"?(b==="C"?3:0):(b==="C"?5:1)}
function match(a,b){var ma=[],mb=[],sa=0,sb=0;for(var i=0;i<50;i++){var x=move(a,ma,mb),y=move(b,mb,ma);sa+=pay(x,y);sb+=pay(y,x);ma.push(x);mb.push(y)}return[sa,sb]}
var ks=Object.keys(NAMES);
$("run").onclick=function(){var tot={};ks.forEach(function(k){tot[k]=0});
 for(var i=0;i<ks.length;i++)for(var j=i+1;j<ks.length;j++){var r=match(ks[i],ks[j]);tot[ks[i]]+=r[0];tot[ks[j]]+=r[1]}
 var arr=ks.slice().sort(function(a,b){return tot[b]-tot[a]}),h="<table><tr><th>#</th><th>Strategy</th><th>Score</th></tr>";
 var mine=$("mine").value;arr.forEach(function(k,i){h+="<tr"+(k===mine?' style="color:#ffd36b"':"")+"><td>"+(i+1)+"</td><td>"+NAMES[k]+(k===mine?" (yours)":"")+"</td><td>"+tot[k]+"</td></tr>"});
 $("out").innerHTML=h+"</table>";
 $("g").textContent="Winner: "+NAMES[arr[0]]+". Nice, retaliating and forgiving strategies usually do well; always-defect wins single matches but loses the tournament.";done()};
</script></body></html>"""
EVOLVE = HEAD + """
<label>Game: <select id="gm"><option value="pd">Prisoner's dilemma</option><option value="hd">Hawk-dove</option><option value="sh">Stag hunt</option></select></label>
<label>Starting share of strategy 1: <b id="vx"></b><input id="x0" type="range" min="1" max="99" value="50"></label>
<div><button id="go">Evolve</button></div>
<canvas id="c" width="400" height="200"></canvas><div id="o" class="k"></div><div id="p" class="k"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var G={pd:{a:[[3,0],[5,1]],n:["Cooperate","Defect"],d:"Defect takes over: it is dominant."},
 hd:{a:[[-1,2],[0,1]],n:["Hawk","Dove"],d:"A stable mix of hawks and doves (here half and half)."},
 sh:{a:[[4,0],[3,2]],n:["Stag","Hare"],d:"Two stable outcomes; the start decides which one."}};
var seen={};
function draw(){var g=$("gm").value,A=G[g].a,x=$("x0").value/100;$("vx").textContent=Math.round(x*100)+"%";
 var c=$("c").getContext("2d");c.clearRect(0,0,400,200);c.strokeStyle="#5c4a85";c.beginPath();c.moveTo(0,100);c.lineTo(400,100);c.stroke();c.strokeStyle="#b26bff";c.beginPath();
 var dt=0.05;for(var i=0;i<=400;i++){var Y=190-x*180;if(i==0)c.moveTo(i,Y);else c.lineTo(i,Y);
  var f1=A[0][0]*x+A[0][1]*(1-x),f2=A[1][0]*x+A[1][1]*(1-x),av=x*f1+(1-x)*f2;x+=dt*x*(f1-av);if(x<0.0001)x=0.0001;if(x>0.9999)x=0.9999}
 c.fillStyle="#c9b8e8";c.fillText("share of "+G[g].n[0]+" over time (top = 100%)",6,12);
 $("o").textContent="Final share of "+G[g].n[0]+": "+Math.round(x*100)+"%. "+G[g].d;seen[g]=1;
 var n=Object.keys(seen).length;$("p").textContent="Games tried: "+n+" of 3";if(n>=3)done()}
$("go").onclick=draw;$("x0").oninput=draw;$("gm").onchange=draw;draw();
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "tourn.html"), "w").write(TOURN)
    open(os.path.join(d, "evolve.html"), "w").write(EVOLVE)
