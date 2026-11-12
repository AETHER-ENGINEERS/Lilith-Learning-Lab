# -*- coding: utf-8 -*-
"""webxdc labs built on Q.js (github.com/stewdio/q.js, MIT, (c) 2019-2020 Stewart Smith).
q.min.js / q.min.css are the project's own build/q.js and build/q.css, minified with terser and clean-css."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
QJS = open(os.path.join(HERE, "q.min.js"), encoding="utf-8").read().replace("</script", "<\\/script")
QCSS = open(os.path.join(HERE, "q.min.css"), encoding="utf-8").read()

CSS = """
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button.ab{font:inherit;border:0;border-radius:18px;padding:8px 14px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px 3px 3px 0;cursor:pointer}
button.ab.s{background:#3a2a5c;color:#f1ebff}
h2{margin:4px 0;font-size:17px}.k{color:#c9b8e8}.ok{color:#8fe3a8}.bad{color:#ff8a8a}
.qwrap{background:#f4f1fa;color:#222;border-radius:10px;padding:8px;margin:8px 0;overflow-x:auto;min-height:60px}
.box{background:#0e0820;border-radius:8px;padding:10px;margin:6px 0;line-height:1.6}
.bar{display:flex;align-items:center;margin:2px 0;font-family:monospace}.bar span.n{width:70px}
.bar span.t{display:inline-block;height:14px;background:#b26bff;border-radius:3px;margin-right:8px;min-width:1px}
textarea{width:100%;font:13px monospace;padding:8px;border-radius:8px;border:1px solid #5c4a85;background:#2a1b48;color:#f1ebff;height:120px}
.con{background:#0e0820;border:1px solid #5c4a85;border-radius:10px;padding:8px;margin:8px 0}.con h3{margin:0 0 4px;font-size:14px}
#out{max-height:240px;overflow:auto;font:13px/1.5 ui-monospace,Menlo,monospace}#out div{margin:2px 0;white-space:pre-wrap}.you{color:#b26bff}.sys{color:#c9b8e8}
.chips{margin:6px 0}button.chip{font:12px system-ui;border:1px solid #5c4a85;border-radius:14px;padding:4px 9px;background:#2a1b48;color:#f1ebff;margin:2px 3px 2px 0;cursor:pointer}
.crow{display:flex;gap:6px}.crow input{flex:1;font:14px ui-monospace,Menlo,monospace;padding:9px;border-radius:8px;border:1px solid #5c4a85;background:#2a1b48;color:#f1ebff}
.legend{font-size:12px;color:#c9b8e8;margin:2px 0 6px}
pre{white-space:pre;overflow-x:auto;margin:0;font-size:12px}
.qwrap p{display:none}
"""

SHELL = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>@@qcss@@</style><style>@@css@@</style></head><body>
@@body@@
<script>@@qjs@@</script>
<script>
var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
Q.verbosity=0;
var cur=null,lastRes=[],solved={};
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;")}
function pOf(res,prefixOrState){var s=0;res.forEach(function(r){var st=r.state.replace("|","").replace("\\u27e9","");if(st.indexOf(prefixOrState)===0)s+=r.probability});return s}
function gates(text){return text.split(/[-\\s=+]+/).filter(Boolean).map(function(t){return t.split("#")[0].split(".")[0]})}
function count(text,sym){return gates(text).filter(function(g){return g===sym}).length}
function only(text,allowed){return gates(text).every(function(g){return allowed.indexOf(g)>=0})}
function textOf(c){var t=c.toText();return t.charAt(0)==="\\n"?t.substr(1):t}
function bars(res){var h="";res.forEach(function(r){var p=r.probability;if(p<0.0005&&res.length>8)return;h+='<div class="bar"><span class="n">'+esc(r.state)+'</span><span class="t" style="width:'+Math.round(p*180)+'px"></span>'+(p*100).toFixed(1)+'%</div>'});$("bars").innerHTML=h}
function loadText(text){var c=Q(text);c.name="lab";c.sort$();var el=$("circuit");while(el.lastChild)el.removeChild(el.lastChild);c.toDom(el);Array.prototype.slice.call(el.querySelectorAll("p")).forEach(function(p){if(/console/i.test(p.textContent))p.parentNode.removeChild(p)});cur=c;c.evaluate$();}
window.addEventListener("Q gui altered circuit",function(e){cur=e.detail.circuit;cur.evaluate$()});
window.addEventListener("Q.Circuit.evaluate completed",function(e){lastRes=e.detail.results;bars(lastRes);if(window.onResults)onResults(e.detail.circuit,lastRes);if(window.conPrint)conPrint(lastRes)});
window.addEventListener("DOMContentLoaded",function(){var p=$("palette");if(p)Q.Circuit.Editor.createPalette(p);if(window.start)start()});
@@js@@
</script></body></html>"""

LEVEL_JS = """
var li=0;
function show(){var L=LEVELS[li];$("title").innerHTML="Level "+(li+1)+" of "+LEVELS.length+": "+esc(L.title);$("intro").innerHTML=L.intro;$("status").innerHTML="";$("sol").innerHTML="";loadText(L.start);$("next").style.display="none";}
function start(){show()}
$("apply").onclick=function(){try{loadText($("txt").value)}catch(e){$("status").innerHTML='<span class="bad">That text is not a valid circuit.</span>'}};
function onResults(c,res){var L=LEVELS[li];if(document.activeElement!==$("txt"))$("txt").value=textOf(c);var t=textOf(c);var ok=false;try{ok=L.check(t,res)}catch(e){}
 if(ok){$("status").innerHTML='<span class="ok">Solved!</span> '+esc(L.after||"");solved[li]=1;if(li<LEVELS.length-1)$("next").style.display="";if(Object.keys(solved).length>=LEVELS.length)done();}
 else{$("status").innerHTML='<span class="k">Not yet. '+esc(L.tip||"")+'</span>'}}
$("next").onclick=function(){if(li<LEVELS.length-1){li++;show()}};
$("reset").onclick=function(){show()};
$("hint").onclick=function(){$("sol").innerHTML='<span class="k">Hint: '+esc(LEVELS[li].hint)+'</span>'};
$("solbtn").onclick=function(){var L=LEVELS[li];$("sol").innerHTML='<span class="k">One solution (type it in the circuit, or press Load):</span><pre>'+esc(L.solution)+'</pre><button class="ab s" id="load">Load it</button>';$("load").onclick=function(){loadText(L.solution)}};
"""

LEVEL_BODY = """<h2 id="title"></h2><div class="k" id="intro"></div>
<div class="qwrap"><div class="Q-circuit-palette" id="palette"></div><div id="circuit"></div></div>
<div class="box"><div id="bars"></div></div><div id="status"></div><div id="sol"></div>
@@console@@
<textarea id="txt" style="display:none"></textarea><button id="apply" style="display:none"></button>
<button class="ab" id="next" style="display:none">Next level</button><button class="ab s" id="reset">Reset</button><button class="ab s" id="hint">Hint</button><button class="ab s" id="solbtn">Show a solution</button>"""



CONSOLE_HTML = """<div class="legend">Tap a gate and drag it into the circuit. <b>c</b> makes a gate controlled (a CNOT). <b>s</b> swaps two qubits. The arrows undo and redo. Or just type commands below.</div>
<div class="con"><h3>&#x1F5A5;&#xFE0F; Q Console</h3><div id="out"></div>
<div class="chips" id="chips"></div>
<div class="crow"><input id="cmd" type="text" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="Type a command, like  H 1"><button class="ab" id="go">Go</button></div></div>"""

CONSOLE_JS = r"""
var hist=[],pending=false,CHIPS=%CHIPS%;
function say(h,c){var d=document.createElement("div");if(c)d.className=c;d.innerHTML=h;$("out").appendChild(d);$("out").scrollTop=$("out").scrollHeight}
function gridOf(){return textOf(cur).split(/\r?\n/).filter(Boolean).map(function(r){return r.trim().split(/[-\s=+]+/).filter(Boolean)})}
function gridText(g){return g.map(function(r){return r.join("-")}).join("\n")}
function lastUsed(g){var m=-1;g.forEach(function(r){r.forEach(function(t,i){if(t!=="I"&&i>m)m=i})});return m}
function blank(n,m){var g=[],i,j;for(i=0;i<n;i++){g.push([]);for(j=0;j<m;j++)g[i].push("I")}return g}
function applyGrid(g,msg){hist.push(textOf(cur));pending=true;loadText(gridText(g));if(msg)say(msg,"sys")}
function addGate(spec,msg){var g=gridOf(),col=lastUsed(g)+1;while(col>=g[0].length)g.forEach(function(r){r.push("I")});spec.forEach(function(s){g[s[0]][col]=s[1]});applyGrid(g,msg+" (step "+(col+1)+")")}
function q(n,g){var i=parseInt(n,10);if(!(i>=1&&i<=g.length)){say("&#x1F914; This circuit has "+g.length+" qubit"+(g.length>1?"s":"")+". Use a number from 1 to "+g.length+", or make a bigger circuit with <b>new 3</b>.","bad");return -1}return i-1}
var NAMES={h:"H",x:"X",y:"Y",z:"Z",t:"T",p:"P",coin:"H",flip:"X",not:"X",hadamard:"H",phase:"T"};
var NOTE={H:"a coin flip!",X:"it flips 0 and 1.",Y:"a flip with a twist.",Z:"it turns the phase (you cannot see that yet).",T:"a small phase turn.",P:"a phase turn."};
function bar(p){var n=Math.round(p*20),s="";for(var i=0;i<20;i++)s+=i<n?"\u2588":"\u2591";return s}
function explain(res){var big=res.filter(function(r){return r.probability>0.005});
 if(big.length===1)return "It always ends as "+big[0].state+". No luck involved.";
 var nq=res[0].state.replace("|","").replace("\u27e9","").length;
 if(nq>1){var marg=[],i,k;for(i=0;i<nq;i++){var p1=0;res.forEach(function(r){if(r.state.replace("|","").charAt(i)==="1")p1+=r.probability});marg.push(p1)}
  var ent=res.some(function(r){var st=r.state.replace("|","").replace("\u27e9","");var pr=1;for(k=0;k<nq;k++)pr*=st.charAt(k)==="1"?marg[k]:1-marg[k];return Math.abs(pr-r.probability)>0.02});
  if(ent)return "Entangled! The qubits are linked: knowing one tells you about the others.";}
 var eq=big.every(function(r){return Math.abs(r.probability-big[0].probability)<0.02});
 if(eq)return "A fair mix of "+big.length+" outcomes. That is superposition!";
 return "A weighted mix: some outcomes are more likely than others.";}
function conPrint(res){if(!pending)return;pending=false;var h="";res.forEach(function(r){if(r.probability>=0.005||res.length<=4)h+=r.state+" "+bar(r.probability)+" "+Math.round(r.probability*100)+"%\n"});say(h,"sys");say("&#x1F4A1; "+explain(res),"ok")}
function sample(n){var counts={},i,k;for(i=0;i<n;i++){var x=Math.random(),acc=0,pick=lastRes[lastRes.length-1].state;for(k=0;k<lastRes.length;k++){acc+=lastRes[k].probability;if(x<acc){pick=lastRes[k].state;break}}counts[pick]=(counts[pick]||0)+1}return counts}
function helpText(){say("<b>Add a gate</b> (each one goes in the next step):\n  H 1   coin flip on qubit 1\n  X 2   flip qubit 2\n  Z 1, Y 1, T 1\n  CNOT 1 2   copy-flip: qubit 1 controls qubit 2\n  CZ 1 2, SWAP 1 2\n<b>See what happens</b>:\n  run      the chances\n  shots 20 measure it 20 times\n  show     draw the circuit\n  text     the circuit as text\n<b>Other</b>:\n  new 3    a fresh circuit with 3 qubits\n  clear    empty it\n  undo     take back the last command\n  help     this list","sys")}
function runCmd(line){
 var w=line.trim().toLowerCase().replace(/^[>\u203a$\s]+/,"").split(/[\s,]+/).filter(Boolean);if(!w.length)return;
 if(w.length===1){var m=w[0].match(/^([a-z]+)(\d+)$/);if(m)w=[m[1],m[2]]}
 var c=w[0],g;
 say("&#x203a; "+esc(line),"you");
 if(c==="help"||c==="?"){helpText();return}
 if(NAMES[c]){g=gridOf();var a=q(w[1]||"1",g);if(a<0)return;var gate=NAMES[c];addGate([[a,gate]],"Added "+gate+" on qubit "+(a+1)+": "+(NOTE[gate]||""));return}
 if(c==="cnot"||c==="cx"||c==="copy"||c==="cz"||c==="swap"){g=gridOf();var a1=q(w[1],g),b=a1<0?-1:q(w[2],g);if(a1<0||b<0)return;if(a1===b){say("&#x1F914; Pick two different qubits, like <b>"+c+" 1 2</b>.","bad");return}
  if(c==="swap"){var g2=gridOf(),col=lastUsed(g2)+1;while(col+2>=g2[0].length)g2.forEach(function(r){r.push("I")});
   g2[a1][col]="X#0";g2[b][col]="X#1";g2[b][col+1]="X#0";g2[a1][col+1]="X#1";g2[a1][col+2]="X#0";g2[b][col+2]="X#1";applyGrid(g2,"Swapped qubits "+(a1+1)+" and "+(b+1)+" using three CNOTs (steps "+(col+1)+" to "+(col+3)+").");return}
  var t=c==="cz"?"Z":"X";addGate([[a1,t+"#0"],[b,t+"#1"]],"Added "+(c==="cz"?"CZ":"CNOT")+": qubit "+(a1+1)+" controls qubit "+(b+1));return}
 if(c==="run"||c==="explain"||c==="go"||c==="results"||c==="chances"){pending=true;cur.evaluate$();return}
 if(c==="shots"||c==="measure"||c==="flipcoins"){var n=Math.max(1,Math.min(1000,parseInt(w[1],10)||20)),cnt=sample(n),h="Measured "+n+" time"+(n>1?"s":"")+":\n";Object.keys(cnt).sort().forEach(function(s){h+=s+" "+(cnt[s]>40?"\u2588".repeat(Math.round(cnt[s]/n*30)):"\u2588".repeat(cnt[s]))+" "+cnt[s]+"\n"});say(h,"sys");say("Every measurement gives just one answer. The chances show up when you repeat it.","ok");if(window.onShots)onShots(cnt);return}
 if(c==="show"||c==="draw"||c==="diagram"){say(esc(cur.toDiagram(true)),"sys");return}
 if(c==="text"){say(esc(textOf(cur)),"sys");return}
 if(c==="new"||c==="qubits"){var nq=parseInt(w[1],10)||1;if(nq<1||nq>5){say("&#x1F914; Pick 1 to 5 qubits.","bad");return}applyGrid(blank(nq,8),"New circuit with "+nq+" qubit"+(nq>1?"s":"")+", all starting as 0.");return}
 if(c==="clear"||c==="reset"){var gg=gridOf();applyGrid(blank(gg.length,gg[0].length),"Cleared.");return}
 if(c==="undo"){if(!hist.length){say("Nothing to undo.","bad");return}pending=true;loadText(hist.pop());say("Undone.","sys");return}
 var guess=["help","run","shots","show","text","new","clear","undo","H","X","Z","CNOT"],near="";guess.forEach(function(x){if(!near&&x.toLowerCase().charAt(0)===c.charAt(0))near=x});
 say("&#x1F914; I do not know <b>"+esc(c)+"</b> yet."+(near?" Did you mean <b>"+near+"</b>?":"")+" Type <b>help</b> to see what I know.","bad");}
window.addEventListener("Q gui altered circuit",function(){pending=true});
window.addEventListener("DOMContentLoaded",function(){var ch=$("chips");CHIPS.forEach(function(c){var b=document.createElement("button");b.className="chip";b.textContent=c;b.onclick=function(){$("cmd").value=c;$("go").click()};ch.appendChild(b)});
 $("go").onclick=function(){var v=$("cmd").value;$("cmd").value="";runCmd(v)};$("cmd").addEventListener("keydown",function(e){if(e.key==="Enter")$("go").click()});
 say("Hi! I am the Q Console. Type <b>help</b> or tap a button below.","sys")});
"""


def rows(n, m, fill="I"):
    return "\n".join("-".join([fill] * m) for _ in range(n))


GATES_JS = LEVEL_JS + """
var LEVELS=[
{title:"Flip the bit",intro:"Every qubit starts as |0\\u27e9. Drag a gate into the circuit so that the result is |1\\u27e9 with 100% certainty.",start:"{SIX}",
 check:function(t,r){return pOf(r,"1")>0.99},hint:"The X gate is the quantum NOT.",solution:"X-I-I-I-I-I",after:"X swaps |0\\u27e9 and |1\\u27e9."},
{title:"Coin flip",intro:"Make the qubit a perfect 50/50 coin: half the time |0\\u27e9, half the time |1\\u27e9.",start:"{SIX}",
 check:function(t,r){return Math.abs(pOf(r,"0")-0.5)<0.01},hint:"The H gate is called Hadamard.",solution:"H-I-I-I-I-I",after:"That is superposition."},
{title:"Undo the coin flip",intro:"This circuit starts with an H. Add more gates so the qubit ends as |0\\u27e9 with certainty, keeping the H in place.",start:"H-I-I-I-I-I",
 check:function(t,r){return pOf(r,"0")>0.99&&count(t,"H")>=1&&gates(t).filter(function(g){return g!=="I"}).length>=2},hint:"Gates can be their own undo button.",solution:"H-H-I-I-I-I",after:"H is its own inverse."},
{title:"Interference",intro:"Using only H and Z gates, make the qubit end as |1\\u27e9 with certainty. Z does not change the probabilities by itself, so think about what happens between two H gates.",start:"{SIX}",
 check:function(t,r){return pOf(r,"1")>0.99&&only(t,["H","Z","I"])&&count(t,"H")>=2},hint:"Sandwich a Z between two H gates.",solution:"H-Z-H-I-I-I",after:"The two paths cancel for |0\\u27e9 and add up for |1\\u27e9."},
{title:"A weighted coin",intro:"Make the result about 85% |0\\u27e9 and 15% |1\\u27e9 (anything between 80% and 90% for |0\\u27e9). You may use H and T gates.",start:"{SIX}",
 check:function(t,r){var p=pOf(r,"0");return p>0.8&&p<0.9&&only(t,["H","T","I"])},hint:"A small phase between two H gates tilts the coin.",solution:"H-T-H-I-I-I",after:"A small phase gives a biased coin."},
{title:"Build a Z from T gates",intro:"Use only H and T gates to end as |1\\u27e9 with certainty. Four T gates in a row add up to a full half turn of phase.",start:"{SIX}",
 check:function(t,r){return pOf(r,"1")>0.99&&only(t,["H","T","I"])&&count(t,"T")>=2},hint:"H, then four T gates, then H.",solution:"H-T-T-T-T-H",after:"Four T gates make one Z."}
];
""".replace("{SIX}", "-".join(["I"] * 6))

ENT_JS = LEVEL_JS + """
var LEVELS=[
{title:"Copy a bit",intro:"The first qubit starts as |1\\u27e9. Use a controlled-NOT (a gate with a control dot and a target) so that the first two qubits both end as 1, giving |110\\u27e9.",
 start:"X-I-I-I-I\\nI-I-I-I-I\\nI-I-I-I-I",check:function(t,r){return pOf(r,"110")>0.99&&t.indexOf("#")>=0},hint:"Put X#0 on qubit 1 (the control) and X#1 on qubit 2 (the target) in the same column.",solution:"X-X#0-I-I-I\\nI-X#1-I-I-I\\nI-I-I-I-I",after:"CNOT copies a classical bit."},
{title:"Make a Bell pair",intro:"Make qubits 1 and 2 entangled so you only ever see |000\\u27e9 or |110\\u27e9, each half of the time.",
 start:"I-I-I-I-I\\nI-I-I-I-I\\nI-I-I-I-I",check:function(t,r){return Math.abs(pOf(r,"000")-0.5)<0.01&&Math.abs(pOf(r,"110")-0.5)<0.01&&t.indexOf("#")>=0},hint:"H on qubit 1, then a CNOT from qubit 1 to qubit 2.",solution:"H-X#0-I-I-I\\nI-X#1-I-I-I\\nI-I-I-I-I",after:"Neither qubit has a definite value alone, but they always agree."},
{title:"Opposite pair",intro:"Make qubits 1 and 2 always disagree: half the time |010\\u27e9, half the time |100\\u27e9.",
 start:"I-I-I-I-I\\nI-I-I-I-I\\nI-I-I-I-I",check:function(t,r){return Math.abs(pOf(r,"010")-0.5)<0.01&&Math.abs(pOf(r,"100")-0.5)<0.01},hint:"Start from the Bell pair and flip one qubit before the CNOT.",solution:"H-X#0-I-I-I\\nX-X#1-I-I-I\\nI-I-I-I-I",after:"A different Bell state."},
{title:"Three-way entanglement",intro:"Make all three qubits agree: half the time |000\\u27e9, half the time |111\\u27e9. This is the GHZ state.",
 start:"I-I-I-I-I\\nI-I-I-I-I\\nI-I-I-I-I",check:function(t,r){return Math.abs(pOf(r,"000")-0.5)<0.01&&Math.abs(pOf(r,"111")-0.5)<0.01},hint:"After H on qubit 1, use qubit 1 as the control twice, once for each other qubit.",solution:"H-X#0-X#0-I-I\\nI-X#1-I-I-I\\nI-I-X#1-I-I",after:"Entanglement can span many qubits."}
];
"""

ALGO_JS = LEVEL_JS + """
var LEVELS=[
{title:"Deutsch: a constant oracle",intro:"The circuit asks: is the hidden function constant or balanced? Qubit 1 ends as |1\\u27e9 when the function is balanced and |0\\u27e9 when it is constant. The third column is the oracle, the secret function. Right now it holds a CNOT, which is balanced. Remove it (drag the gates out) so the function becomes constant, and qubit 1 should end as |0\\u27e9.",
 start:"I-H-X#0-H\\nX-H-X#1-I",check:function(t,r){return pOf(r,"0")>0.99&&t.indexOf("#")<0},hint:"Take both halves of the CNOT out of the third column.",solution:"I-H-I-H\\nX-H-I-I",after:"A constant function leaves qubit 1 at 0."},
{title:"Deutsch: a balanced oracle",intro:"Now put the CNOT back in the oracle column (control on qubit 1, target on qubit 2). That is the function f(x)=x, which is balanced. Qubit 1 should end as |1\\u27e9, so one question reveals the answer.",
 start:"I-H-I-H\\nX-H-I-I",check:function(t,r){return pOf(r,"1")>0.99&&t.indexOf("#")>=0},hint:"Third column: X#0 on qubit 1 and X#1 on qubit 2.",solution:"I-H-X#0-H\\nX-H-X#1-I",after:"Balanced gives 1. One query told us which kind it is."},
{title:"Grover: find |11\\u27e9",intro:"Search 4 items for the marked one, |11\\u27e9. Start with H on both qubits, mark |11\\u27e9 with a controlled-Z, then reflect about the average: H, X on both, controlled-Z, X on both, H. One round finds it.",
 start:"H-I-I-I-I-I-I-I-I\\nH-I-I-I-I-I-I-I-I",check:function(t,r){return pOf(r,"11")>0.99},hint:"Use Z#0 on one qubit and Z#1 on the other in the same column for a controlled-Z.",solution:"H-Z#0-H-X-Z#0-X-H-I-I\\nH-Z#1-H-X-Z#1-X-H-I-I",after:"Amplitude was moved to the marked item."},
{title:"Grover: find |01\\u27e9",intro:"Now the marked item is |01\\u27e9. Flip qubit 1 with X before and after the marking controlled-Z, then use the same reflection.",
 start:"H-I-I-I-I-I-I-I-I\\nH-I-I-I-I-I-I-I-I",check:function(t,r){return pOf(r,"01")>0.99},hint:"The oracle is X on qubit 1, controlled-Z, X on qubit 1.",solution:"H-X-Z#0-X-H-X-Z#0-X-H\\nH-I-Z#1-I-H-X-Z#1-X-H",after:"Any single item can be found in one round for 4 items."}
];
"""

PLAY_BODY = """<h2>Free playground</h2><div class="k">Build any circuit, or type one. Rows are qubits, columns are moments. Use # for controls: X#0 is the control, X#1 the target.</div>
<textarea id="txt">H-X#0-I
I-X#1-I</textarea>
<button class="ab" id="apply">Apply</button><button class="ab s" id="shots">Run 100 shots</button>
<div class="qwrap"><div class="Q-circuit-palette" id="palette"></div><div id="circuit"></div></div>
@@console@@
<div class="box"><div id="bars"></div></div><div class="box"><div class="k">100 shots (each one a measurement)</div><div id="hist"></div></div>
<div class="box"><div class="k">ASCII diagram</div><pre id="diag"></pre></div><div id="msg" class="k"></div>"""

PLAY_JS = """
var ran=0,kinds={};
function start(){applyText()}
function applyText(){try{loadText($("txt").value)}catch(e){$("msg").innerHTML='<span class="bad">That text is not a valid circuit.</span>'}}
function onResults(c,res){$("txt").value=textOf(c);$("diag").textContent=c.toDiagram(true);$("msg").textContent=""}
$("apply").onclick=applyText;
$("shots").onclick=function(){var counts={},i,k,res=lastRes;for(i=0;i<100;i++){var x=Math.random(),acc=0,pick=res[res.length-1].state;for(k=0;k<res.length;k++){acc+=res[k].probability;if(x<acc){pick=res[k].state;break}}counts[pick]=(counts[pick]||0)+1}
 var h="";Object.keys(counts).sort().forEach(function(s){h+='<div class="bar"><span class="n">'+esc(s)+'</span><span class="t" style="width:'+counts[s]*1.8+'px"></span>'+counts[s]+'</div>'});$("hist").innerHTML=h;
 ran++;if(Object.keys(counts).length>=2||ran>=3)done()};
"""


def build():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    sets = {
        "qgates": (LEVEL_BODY, GATES_JS), "qentangle": (LEVEL_BODY, ENT_JS),
        "qalgo": (LEVEL_BODY, ALGO_JS), "qplay": (PLAY_BODY, PLAY_JS)}
    chips = {
        "qgates": ["H 1", "X 1", "Z 1", "T 1", "run", "shots 20", "undo", "help"],
        "qentangle": ["new 2", "H 1", "CNOT 1 2", "X 2", "run", "shots 20", "explain", "undo", "help"],
        "qalgo": ["new 2", "H 1", "H 2", "CZ 1 2", "run", "undo", "help"],
        "qplay": ["new 1", "H 1", "X 1", "new 2", "CNOT 1 2", "run", "shots 20", "show", "undo", "help"]}
    import json
    for name, (body, js) in sets.items():
        html = SHELL
        js = js + CONSOLE_JS.replace("%CHIPS%", json.dumps(chips[name]))
        body = body.replace("@@console@@", CONSOLE_HTML)
        for k, v in (("css", CSS), ("body", body), ("js", js), ("qcss", QCSS), ("qjs", QJS)):
            html = html.replace("@@%s@@" % k, v)
        open(os.path.join(d, name + ".html"), "w", encoding="utf-8").write(html)


def main():
    build()


if __name__ == "__main__":
    main()
