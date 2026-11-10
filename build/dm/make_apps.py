# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}button.s{background:#3a2a5c;color:#f1ebff}
canvas{display:block;margin:6px auto;background:#0e0820;border-radius:8px;max-width:100%}.k{color:#c9b8e8}label{display:block;margin-top:6px}input[type=range]{width:100%;accent-color:#b26bff}
input[type=text]{width:100%;font:inherit;padding:8px;border-radius:8px;border:1px solid #5c4a85;background:#2a1b48;color:#f1ebff}
.box{background:#0e0820;border-radius:8px;padding:10px;margin:6px 0}
</style></head><body>"""
COMMON = """var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}"""
DECIDE = HEAD + """
<label>Message <input type="text" id="m" value="my card was charged twice and I want a refund"></label>
<label>Question <select id="q"><option value="0">Which team? (billing / shipping / account)</option><option value="1">Is it urgent? (yes / no)</option></select></label>
<label>Temperature: <b id="tv"></b><input id="t" type="range" min="3" max="40" value="10"></label>
<label>Escalation threshold: <b id="hv"></b><input id="h" type="range" min="40" max="99" value="70"></label>
<button id="go">Decide</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var Q=[{o:["billing","shipping","account"],w:{billing:"card charged charge refund payment invoice twice price bill",shipping:"parcel package delivery arrived shipping courier tracking late",account:"password login account email profile username locked"}},
{o:["yes","no"],w:{yes:"urgent now asap immediately emergency twice locked angry never",no:"thanks later whenever question maybe curious"}}];
var seen={};
function run(){var q=Q[+$("q").value],txt=$("m").value.toLowerCase().split(/\\W+/),T=$("t").value/10,th=$("h").value/100;$("tv").textContent=T.toFixed(1);$("hv").textContent=th.toFixed(2);
 var sc=q.o.map(function(o){var ws=q.w[o].split(" "),s=0;txt.forEach(function(w){if(ws.indexOf(w)>=0)s+=1.5});return s+(o==="no"?0.4:0)}),m=Math.max.apply(null,sc),
 e=sc.map(function(s){return Math.exp((s-m)/T)}),t=e.reduce(function(a,b){return a+b},0),p=e.map(function(x){return x/t}),b=p.indexOf(Math.max.apply(null,p));
 var h="";q.o.forEach(function(o,i){h+='<div style="display:flex;align-items:center;gap:6px"><span style="width:6em">'+o+'</span><div style="height:12px;border-radius:6px;background:#b26bff;width:'+Math.round(p[i]*100)+'%"></div><span class="k">'+p[i].toFixed(2)+'</span></div>'});
 h+="<br><b>"+(p[b]>=th?"Answer: "+q.o[b]:"Escalate to a big model (confidence "+p[b].toFixed(2)+" is below "+th.toFixed(2)+")")+"</b>";$("o").innerHTML=h;return $("m").value}
$("go").onclick=function(){var v=run();seen[v.trim().toLowerCase()]=1;var n=Object.keys(seen).length;$("p").textContent="Different messages tried: "+n+" of 3";if(n>=3)done()};
$("t").oninput=run;$("h").oninput=run;$("q").onchange=run;run();
</script></body></html>"""
CALIB = HEAD + """
<label>Temperature: <b id="tv"></b><input id="t" type="range" min="5" max="60" value="10"></label>
<canvas id="c" width="320" height="320"></canvas><div id="o" class="k"></div>
<script>""" + COMMON + """
var seed=11;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff}
var Z=[],Y=[],i;for(i=0;i<400;i++){var z=(rnd()-0.5)*8,pt=1/(1+Math.exp(-z/2.4));Z.push(z);Y.push(rnd()<pt?1:0)}
function sg(x){return 1/(1+Math.exp(-x))}
function draw(){var T=$("t").value/10;$("tv").textContent=T.toFixed(1);var B=10,n=[],c=[],a=[],b;for(b=0;b<B;b++){n.push(0);c.push(0);a.push(0)}
 var correctConf=[];Z.forEach(function(z,j){var p=sg(z/T),conf=Math.max(p,1-p),ok=((p>=0.5)?1:0)===Y[j]?1:0,k=Math.min(B-1,Math.floor((conf-0.5)*2*B));n[k]++;c[k]+=conf;a[k]+=ok});
 var e=0,N=Z.length;for(b=0;b<B;b++)if(n[b])e+=n[b]/N*Math.abs(a[b]/n[b]-c[b]/n[b]);
 var g=$("c").getContext("2d");g.clearRect(0,0,320,320);g.strokeStyle="#5c4a85";g.beginPath();g.moveTo(10,310);g.lineTo(310,10);g.stroke();g.fillStyle="#b26bff";
 for(b=0;b<B;b++)if(n[b]){var x=10+(c[b]/n[b]-0.5)*600,y=310-(a[b]/n[b]-0.5)*600;g.beginPath();g.arc(x,y,3+Math.sqrt(n[b])/2.5,0,6.3);g.fill()}
 g.fillStyle="#c9b8e8";g.fillText("confidence ->",230,305);g.fillText("accuracy",14,20);
 $("o").textContent="ECE = "+e.toFixed(3)+(e<0.04?" (well calibrated)":" (points below the diagonal mean overconfident)");if(e<0.04)done()}
$("t").oninput=draw;draw();
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "decide.html"), "w").write(DECIDE)
    open(os.path.join(d, "calib.html"), "w").write(CALIB)
