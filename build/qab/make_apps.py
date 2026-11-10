# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
TREE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:8px;background:#150d27;color:#f1ebff}
svg{width:100%;max-width:340px;display:block;margin:0 auto;background:#0e0820;border-radius:8px}.k{color:#c9b8e8}
#info{margin-top:8px;padding:8px;background:#0e0820;border-radius:8px;min-height:92px}.he{font-size:22px;direction:rtl}
</style></head><body>
<svg id="s" viewBox="0 0 340 520"></svg>
<div id="info"><span class="k">Tap a sephirah.</span></div><div class="k" id="prog" style="margin-top:6px"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var S=[null,
{n:"Kether",h:"\\u05db\\u05ea\\u05e8",m:"Crown",p:"Primum Mobile",pl:"Balance",x:170,y:35,c:"#f1ebff"},
{n:"Chokmah",h:"\\u05d7\\u05db\\u05de\\u05d4",m:"Wisdom",p:"Zodiac",pl:"Mercy",x:270,y:95,c:"#9bb7ff"},
{n:"Binah",h:"\\u05d1\\u05d9\\u05e0\\u05d4",m:"Understanding",p:"Saturn",pl:"Severity",x:70,y:95,c:"#c9a0ff"},
{n:"Chesed",h:"\\u05d7\\u05e1\\u05d3",m:"Mercy",p:"Jupiter",pl:"Mercy",x:270,y:185,c:"#7fb2ff"},
{n:"Geburah",h:"\\u05d2\\u05d1\\u05d5\\u05e8\\u05d4",m:"Strength",p:"Mars",pl:"Severity",x:70,y:185,c:"#ff8f8f"},
{n:"Tiphareth",h:"\\u05ea\\u05e4\\u05d0\\u05e8\\u05ea",m:"Beauty",p:"Sun",pl:"Balance",x:170,y:235,c:"#ffd36b"},
{n:"Netzach",h:"\\u05e0\\u05e6\\u05d7",m:"Victory",p:"Venus",pl:"Mercy",x:270,y:330,c:"#8fe3a8"},
{n:"Hod",h:"\\u05d4\\u05d5\\u05d3",m:"Splendour",p:"Mercury",pl:"Severity",x:70,y:330,c:"#ffb36b"},
{n:"Yesod",h:"\\u05d9\\u05e1\\u05d5\\u05d3",m:"Foundation",p:"Moon",pl:"Balance",x:170,y:395,c:"#d0b4ff"},
{n:"Malkuth",h:"\\u05de\\u05dc\\u05db\\u05d5\\u05ea",m:"Kingdom",p:"Earth",pl:"Balance",x:170,y:475,c:"#c4a67a"}];
var P=[[1,2],[1,3],[1,6],[2,3],[2,6],[2,4],[3,6],[3,5],[4,5],[4,6],[4,7],[5,6],[5,8],[6,7],[6,9],[6,8],[7,8],[7,9],[7,10],[8,9],[8,10],[9,10]];
var svg=$("s"),NS="http://www.w3.org/2000/svg",seen={};
function el(t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);return e}
P.forEach(function(p){svg.appendChild(el("line",{x1:S[p[0]].x,y1:S[p[0]].y,x2:S[p[1]].x,y2:S[p[1]].y,stroke:"#3a2a5c","stroke-width":2}))});
var circles={};
for(var i=1;i<=10;i++)(function(i){var s=S[i],g=el("g",{style:"cursor:pointer"});var c=el("circle",{cx:s.x,cy:s.y,r:24,fill:"#1d1236",stroke:s.c,"stroke-width":3});g.appendChild(c);
 var t=el("text",{x:s.x,y:s.y+5,"text-anchor":"middle",fill:"#f1ebff","font-size":"15","font-weight":"bold"});t.textContent=i;g.appendChild(t);
 g.onclick=function(){Object.keys(circles).forEach(function(k){circles[k].setAttribute("fill","#1d1236")});c.setAttribute("fill",s.c+"55");
  var nb=[];P.forEach(function(p,j){if(p[0]===i||p[1]===i)nb.push(11+j)});
  $("info").innerHTML="<div class='he'>"+s.h+"</div><b>"+i+". "+s.n+"</b> \\u2014 "+s.m+"<br>Pillar: "+s.pl+"<br>Hermetic planet: "+s.p+"<br><span class='k'>Paths touching it: "+nb.join(", ")+"</span>";
  seen[i]=1;var n=Object.keys(seen).length;$("prog").textContent="Sephiroth visited: "+n+" of 6 needed";if(n>=6)done()};
 circles[i]=c;svg.appendChild(g)})(i);
</script></body></html>"""
def main():
    os.makedirs(os.path.join(HERE, "apps"), exist_ok=True)
    open(os.path.join(HERE, "apps", "tree.html"), "w", encoding="utf-8").write(TREE)
if __name__ == "__main__":
    main(); print("ok")
