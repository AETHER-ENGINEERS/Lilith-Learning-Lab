# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = """<style>*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button{font:inherit;border:0;border-radius:18px;padding:8px 14px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}
button.s{background:#3a2a5c;color:#f1ebff}canvas{width:100%;max-width:340px;display:block;margin:8px auto;background:#0e0820;border-radius:8px}
.k{color:#c9b8e8}.ok{color:#8fe3a8}.bad{color:#ff9b9b}code{background:#0e0820;padding:2px 6px;border-radius:6px}pre{background:#0e0820;padding:8px;border-radius:8px;overflow:auto}
select{font:inherit;width:100%;background:#0e0820;color:#f1ebff;border:1px solid #3a2a5c;border-radius:8px;padding:8px}</style>"""
CIRCLE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + STYLE + """</head><body>
<div><button id="f">loop</button><button id="b" class="s">inverse loop</button><button id="r" class="s">reset</button></div>
<canvas id="c" width="340" height="340"></canvas>
<div>Word: <code id="w">(empty)</code></div><div>Reduced: <code id="rw">(empty)</code></div>
<div>Winding number: <b id="n">0</b></div>
<div class="k" id="msg" style="margin-top:8px">l = go round once forwards, L = go round once backwards. Equal winding numbers mean equal paths.</div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var word="",ang=0;
function reduce(w){var o=[];for(var i=0;i<w.length;i++){var c=w[i],t=o[o.length-1];if(t&&t!==c&&t.toLowerCase()===c.toLowerCase())o.pop();else o.push(c)}return o.join("")}
function wind(w){var n=0;for(var i=0;i<w.length;i++){if(w[i]==="l")n++;else if(w[i]==="L")n--}return n}
function draw(){var g=$("c").getContext("2d");g.clearRect(0,0,340,340);g.strokeStyle="#3a2a5c";g.lineWidth=6;g.beginPath();g.arc(170,170,110,0,6.3);g.stroke();
 g.fillStyle="#f1ebff";g.beginPath();g.arc(280,170,8,0,6.3);g.fill();g.fillText("base",270,155);
 var x=170+110*Math.cos(-ang),y=170+110*Math.sin(-ang);g.fillStyle="#b26bff";g.beginPath();g.arc(x,y,10,0,6.3);g.fill()}
var seen={};
function upd(){var n=wind(word);$("w").textContent=word||"(empty)";var rw=reduce(word);$("rw").textContent=rw||"(empty)";$("n").textContent=n;draw();
 if(Math.abs(n)>=3)seen[n>0?"p":"m"]=1;if(Math.abs(n)>=3)done()}
function step(d){word+=d>0?"l":"L";var t=ang,target=ang+d*6.2832,k=0;var iv=setInterval(function(){k++;ang=t+(target-t)*k/12;draw();if(k>=12){clearInterval(iv);ang=((target%6.2832)+6.2832)%6.2832;upd()}},20)}
$("f").onclick=function(){step(1)};$("b").onclick=function(){step(-1)};$("r").onclick=function(){word="";ang=0;upd()};upd();
</script></body></html>"""
PROPS = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + STYLE + """</head><body>
<select id="s"></select>
<div style="margin-top:8px" class="k">Statement:</div><div id="st"></div>
<div style="margin-top:8px" class="k">Type:</div><pre id="ty"></pre>
<div class="k">Program (the proof):</div><pre id="pr"></pre>
<div id="note"></div>
<div class="k" id="prog" style="margin-top:8px"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var L=[
{n:"A implies A",t:"A -> A",p:"identity x = x",s:"If A is true, then A is true."},
{n:"A implies (B implies A)",t:"A -> B -> A",p:"constFn x y = x",s:"A true gives: any B still leaves A true."},
{n:"A and B implies B and A",t:"(A, B) -> (B, A)",p:"swap (x, y) = (y, x)",s:"Swap the two halves of a pair."},
{n:"A implies (A or B)",t:"A -> Either A B",p:"orIntro x = Left x",s:"If A holds then A or B holds."},
{n:"Modus ponens",t:"(A -> B) -> A -> B",p:"apply f x = f x",s:"Given A -> B and A, you get B."},
{n:"Compose implications",t:"(A -> B) -> (B -> C) -> A -> C",p:"compose f g x = g (f x)",s:"Chain two implications."},
{n:"Excluded middle: A or not A",t:"Either A (A -> Void)",p:"(no program exists)",s:"Would decide every statement A.",bad:1},
{n:"Double negation elimination",t:"((A -> Void) -> Void) -> A",p:"(no program exists)",s:"Not provable constructively.",bad:1}];
var sel=$("s");L.forEach(function(x,i){var o=document.createElement("option");o.value=i;o.textContent=x.n;sel.appendChild(o)});
var seen={};
function show(){var x=L[+sel.value];$("st").textContent=x.s;$("ty").textContent=x.t;$("pr").textContent=x.p;
 $("note").innerHTML=x.bad?"<span class='bad'>No term has this type in pure type theory.</span>":"<span class='ok'>A program of this type is a proof.</span>";
 seen[sel.value]=1;var n=Object.keys(seen).length;$("prog").textContent="Statements viewed: "+n+" of 3 needed (include one that has no proof).";
 var hasBad=Object.keys(seen).some(function(k){return L[+k].bad});if(n>=3&&hasBad)done()}
sel.onchange=show;show();
</script></body></html>"""
def main():
    os.makedirs(os.path.join(HERE, "apps"), exist_ok=True)
    open(os.path.join(HERE, "apps", "circle.html"), "w", encoding="utf-8").write(CIRCLE)
    open(os.path.join(HERE, "apps", "props.html"), "w", encoding="utf-8").write(PROPS)
if __name__ == "__main__":
    main(); print("ok")
