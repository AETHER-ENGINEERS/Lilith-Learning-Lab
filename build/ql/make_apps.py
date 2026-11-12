# -*- coding: utf-8 -*-
"""webxdc labs built on Q.js (github.com/stewdio/q.js, MIT, (c) 2019-2020 Stewart Smith).
q.min.js / q.min.css are the project's own build/q.js and build/q.css, minified with terser and clean-css."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
QJS = open(os.path.join(HERE, "q.min.js"), encoding="utf-8").read().replace("</script", "<\\/script")
import sys
sys.path.insert(0, HERE)
import composer

CSS = composer.CSS

SHELL = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>@@css@@</style></head><body>
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
window.addEventListener("Q.Circuit.evaluate completed",function(e){lastRes=e.detail.results;bars(lastRes);if(window.onResults)onResults(e.detail.circuit,lastRes);if(window.conPrint)conPrint(lastRes)});
@@cjs@@
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

LEVEL_BODY = """<div class="card"><h2 id="title"></h2><div class="k" id="intro"></div></div>
@@composer@@
<div class="card"><h3>Chances</h3><div id="bars"></div></div><div id="status" class="card"></div><div id="sol"></div>
@@code@@
@@console@@
<textarea id="txt" style="display:none"></textarea><button id="apply" style="display:none"></button>
<button class="ab" id="next" style="display:none">Next level</button><button class="ab s" id="reset">Reset</button><button class="ab s" id="hint">Hint</button><button class="ab s" id="solbtn">Show a solution</button>"""



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

PLAY_BODY = """<div class="card"><h2>Free playground</h2><div class="k">Pick a gate, then tap a square. Try an H, then a CNOT. Watch the chances and the code change.</div></div>
@@composer@@
<div class="card"><h3>Chances</h3><div id="bars"></div><button class="ab" id="shots" style="margin-top:6px">Run 100 shots</button><div id="hist"></div></div>
@@code@@
@@console@@
<div class="card"><details><summary>Circuit text and ASCII picture</summary><textarea id="txt">H-X#0-I
I-X#1-I</textarea><button class="ab s" id="apply">Apply text</button><pre id="diag"></pre><div id="msg" class="k"></div></details></div>"""

PLAY_JS = """
var ran=0,kinds={};
function start(){applyText()}
function applyText(){try{loadText($("txt").value)}catch(e){$("msg").innerHTML='<span class="bad">That text is not a valid circuit.</span>'}}
function onResults(c,res){$("txt").value=textOf(c);$("diag").textContent=c.toDiagram(true);$("msg").textContent=""}
$("apply").onclick=applyText;
$("shots").onclick=function(){var counts={},i,k,res=lastRes;for(i=0;i<100;i++){var x=Math.random(),acc=0,pick=res[res.length-1].state;for(k=0;k<res.length;k++){acc+=res[k].probability;if(x<acc){pick=res[k].state;break}}counts[pick]=(counts[pick]||0)+1}
 var h="";Object.keys(counts).sort().forEach(function(s){h+='<div class="bc"><span class="v">'+counts[s]+'</span><div class="b" style="height:'+Math.round(counts[s]*0.9)+'px"></div><span class="l">'+s.replace("|","").replace("\\u27e9","")+'</span></div>'});$("hist").innerHTML='<div class="chart" style="margin-top:6px">'+h+'</div>';
 ran++;if(Object.keys(counts).length>=2||ran>=3)done()};
"""


POLAR_BODY = """<div class="card"><h2>Polarizer lab</h2><div class="k">Light waves wiggle in some direction. The first filter lets through only light wiggling straight up and down (0&deg;). The last filter is turned to 90&deg;, so it should block everything. Now add a middle filter and choose its angle.</div></div>
<div class="card"><label style="display:flex;gap:8px;align-items:center"><input type="checkbox" id="mid"> Add a middle filter</label>
<div id="angrow" style="display:none;margin:8px 0">Middle filter angle: <b id="angv">45</b>&deg;<input type="range" id="ang" min="0" max="90" value="45" step="5" style="width:100%;accent-color:#b26bff"></div>
<button class="ab" id="send" style="margin-top:8px">Send 400 photons</button><div id="res" style="margin-top:8px"></div><div id="msg" style="margin-top:6px"></div></div>"""

POLAR_JS = """
var best=0;
function row(label,n,tot,exp){return '<div style="margin:6px 0"><div style="display:flex;justify-content:space-between"><span>'+label+'</span><span class="k">'+n+' photons'+(exp!==undefined?' (expect about '+exp+')':'')+'</span></div><div style="height:14px;background:#0f0b18;border:1px solid var(--line);border-radius:7px;overflow:hidden"><div style="height:100%;width:'+Math.round(n/tot*100)+'%;background:linear-gradient(90deg,var(--pink),var(--g))"></div></div></div>'}
function c2(d){var r=d*Math.PI/180;return Math.cos(r)*Math.cos(r)}
function pass(n,p){var k=0,i;for(i=0;i<n;i++)if(Math.random()<p)k++;return k}
$("mid").onchange=function(){$("angrow").style.display=$("mid").checked?"block":"none"};
$("ang").oninput=function(){$("angv").textContent=$("ang").value};
$("send").onclick=function(){var N=400,mid=$("mid").checked,a=+$("ang").value;
 var n1=pass(N,0.5),h=row("Start",N,N)+row("After filter 1 (0\u00b0)",n1,N,Math.round(N*0.5)),last;
 if(mid){var n2=pass(n1,c2(a));h+=row("After middle filter ("+a+"\u00b0)",n2,N,Math.round(N*0.5*c2(a)));last=pass(n2,c2(90-a));h+=row("After last filter (90\u00b0)",last,N,Math.round(N*0.5*c2(a)*c2(90-a)))}
 else{last=pass(n1,c2(90));h+=row("After last filter (90\u00b0)",last,N,0)}
 $("res").innerHTML=h;
 if(!mid)$("msg").innerHTML='<span class="k">Crossed filters block it all. Now tick the box and add a middle filter.</span>';
 else if(last>0){$("msg").innerHTML='<span class="ok">Surprise! Light came back, though you added a blocker. Each filter acts like a measurement and re-sets the photon\u2019s direction.</span>';done()}
 else $("msg").innerHTML='<span class="k">Nothing got through this time. Try 45\u00b0, which lets the most light through.</span>'};
"""

def build():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    sets = {
        "qgates": (LEVEL_BODY, GATES_JS), "qentangle": (LEVEL_BODY, ENT_JS),
        "qalgo": (LEVEL_BODY, ALGO_JS), "qplay": (PLAY_BODY, PLAY_JS)}
    chips = {
        "qgates": ["H 1", "X 1", "Z 1", "T 1", "shots 20", "undo", "help"],
        "qentangle": ["new 2", "H 1", "CNOT 1 2", "X 2", "run", "shots 20", "explain", "undo", "help"],
        "qalgo": ["new 2", "H 1", "H 2", "CZ 1 2", "run", "undo", "help"],
        "qplay": ["new 1", "H 1", "X 1", "new 2", "CNOT 1 2", "run", "shots 20", "show", "undo", "help"]}
    import json
    for name, (body, js) in sets.items():
        html = SHELL
        js = js + composer.CONSOLE_JS.replace("%CHIPS%", json.dumps(chips[name]))
        body = body.replace("@@composer@@", composer.COMPOSER_HTML).replace("@@code@@", composer.CODE_HTML).replace("@@console@@", composer.CONSOLE_HTML)
        for k, v in (("css", CSS), ("body", body), ("js", js), ("cjs", composer.COMPOSER_JS), ("qjs", QJS)):
            html = html.replace("@@%s@@" % k, v)
        open(os.path.join(d, name + ".html"), "w", encoding="utf-8").write(html)
    pol = ("<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><style>" + CSS + "</style></head><body>" + POLAR_BODY +
           "<script>var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}" + POLAR_JS + "</script></body></html>")
    open(os.path.join(d, "qpolar.html"), "w", encoding="utf-8").write(pol)


def main():
    build()


if __name__ == "__main__":
    main()
