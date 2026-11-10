# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = """<style>*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}
button.s{background:#3a2a5c;color:#f1ebff}.k{color:#c9b8e8}.ok{color:#8fe3a8}.bad{color:#ff9b9b}.grid{display:flex;flex-wrap:wrap}
canvas{width:100%;max-width:360px;display:block;margin:8px auto;background:#0e0820;border-radius:8px}code{background:#0e0820;padding:2px 6px;border-radius:6px}</style>"""
EAR = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + STYLE + """</head><body>
<div><button id="play">Play interval</button><button id="again" class="s">Hear again</button></div>
<div class="k">Which interval did you hear (going up)?</div><div class="grid" id="opts"></div>
<div id="msg" style="margin-top:8px;min-height:22px"></div><div class="k" id="prog"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var N=["unison","minor 2nd","major 2nd","minor 3rd","major 3rd","perfect 4th","tritone","perfect 5th","minor 6th","major 6th","minor 7th","major 7th","octave"];
var ctx=null,cur=null,base=60,good=0,tried=0;
function tone(m,t,d){var o=ctx.createOscillator(),g=ctx.createGain();o.type="triangle";o.frequency.value=440*Math.pow(2,(m-69)/12);g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(0.4,t+0.03);g.gain.exponentialRampToValueAtTime(0.0001,t+d);o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+d+0.05)}
function hear(){if(!ctx)ctx=new (window.AudioContext||window.webkitAudioContext)();var t=ctx.currentTime+0.05;tone(base,t,0.7);tone(base+cur,t+0.8,0.9)}
function next(){cur=1+Math.floor(Math.random()*12);base=55+Math.floor(Math.random()*12);hear()}
var box=$("opts");for(var i=1;i<=12;i++)(function(i){var b=document.createElement("button");b.className="s";b.textContent=N[i];b.onclick=function(){if(cur===null){$("msg").textContent="Press Play interval first.";return}
 tried++;if(i===cur){good++;$("msg").innerHTML="<span class='ok'>Correct: "+N[cur]+"</span>";cur=null}else{$("msg").innerHTML="<span class='bad'>Not quite. It was a "+N[cur]+". Press Hear again or Play interval.</span>";cur=null}
 $("prog").textContent="Correct: "+good+" of 5 needed ("+tried+" tried)";if(good>=5)done()};box.appendChild(b)})(i);
$("play").onclick=next;$("again").onclick=function(){if(cur!==null)hear()};
</script></body></html>"""
FIFTHS = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + STYLE + """</head><body>
<canvas id="c" width="360" height="360"></canvas>
<div id="info" class="k">Tap a key on the circle.</div><div id="prog" class="k" style="margin-top:6px"></div>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var MAJ=["C","G","D","A","E","B","F\\u266f","D\\u266d","A\\u266d","E\\u266d","B\\u266d","F"];
var MIN=["Am","Em","Bm","F\\u266fm","C\\u266fm","G\\u266fm","D\\u266fm","B\\u266dm","Fm","Cm","Gm","Dm"];
var SH=[0,1,2,3,4,5,6,-5,-4,-3,-2,-1];
var NAMEPC=[0,7,2,9,4,11,6,1,8,3,10,5];
var SHARPN=["C","C\\u266f","D","D\\u266f","E","F","F\\u266f","G","G\\u266f","A","A\\u266f","B"],FLATN=["C","D\\u266d","D","E\\u266d","E","F","G\\u266d","G","A\\u266d","A","B\\u266d","B"];
var sel=-1,seen={};
function draw(){var g=$("c").getContext("2d");g.clearRect(0,0,360,360);g.textAlign="center";g.textBaseline="middle";
 for(var i=0;i<12;i++){var a=-Math.PI/2+i*Math.PI/6,x=180+135*Math.cos(a),y=180+135*Math.sin(a),x2=180+85*Math.cos(a),y2=180+85*Math.sin(a);
  g.fillStyle=i===sel?"#b26bff":"#2d2046";g.beginPath();g.arc(x,y,24,0,6.3);g.fill();g.fillStyle=i===sel?"#1b0b33":"#f1ebff";g.font="bold 16px sans-serif";g.fillText(MAJ[i],x,y);
  g.fillStyle="#3a2a5c";g.beginPath();g.arc(x2,y2,17,0,6.3);g.fill();g.fillStyle="#c9b8e8";g.font="12px sans-serif";g.fillText(MIN[i],x2,y2)}}
function scale(i){var t=NAMEPC[i],st=[0,2,4,5,7,9,11],names=SH[i]<0?FLATN:SHARPN;return st.map(function(s){return names[(t+s)%12]}).join(" ")}
$("c").onclick=function(e){var r=$("c").getBoundingClientRect(),x=(e.clientX-r.left)*360/r.width-180,y=(e.clientY-r.top)*360/r.height-180;
 var a=Math.atan2(y,x)+Math.PI/2;if(a<0)a+=2*Math.PI;var i=Math.round(a/(Math.PI/6))%12;sel=i;draw();
 var n=SH[i];$("info").innerHTML="<b>"+MAJ[i]+" major</b>: "+scale(i)+"<br>"+(n===0?"No sharps or flats":(n>0?n+" sharp"+(n>1?"s":""):(-n)+" flat"+(n<-1?"s":"")))+"<br>Relative minor: "+MIN[i];
 seen[i]=1;var c=Object.keys(seen).length;$("prog").textContent="Keys visited: "+c+" of 4 needed";if(c>=4)done()};
draw();
</script></body></html>"""
def main():
    os.makedirs(os.path.join(HERE, "apps"), exist_ok=True)
    open(os.path.join(HERE, "apps", "ear.html"), "w", encoding="utf-8").write(EAR)
    open(os.path.join(HERE, "apps", "fifths.html"), "w", encoding="utf-8").write(FIFTHS)
if __name__ == "__main__":
    main(); print("ok")
