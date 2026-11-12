# -*- coding: utf-8 -*-
"""Lilith Composer: a mobile-first circuit editor styled like the Lilith Learning Lab app.
The Q.js engine does the maths; this file draws the editor, the chart and the code views."""

CSS = r"""
:root{--bg:#0f0b18;--panel:#1b1429;--panel2:#261b3b;--line:#3a2d55;--tx:#f1ebff;--dim:#a99dc7;--g:#b26bff;--g2:#d9acff;--pink:#e06aa8;--ok:#7be0a4;--err:#ff7a9a;--blue:#6bb6ff;--tonal:#33244f}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{font:14px/1.5 Roboto,system-ui,sans-serif;margin:0;padding:8px;background:var(--bg);color:var(--tx)}
h2{margin:0 0 4px;font-size:17px;font-weight:600}h3{margin:0;font-size:14px;font-weight:500}
.k{color:var(--dim)}.ok{color:var(--ok)}.bad{color:var(--err)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:10px 12px;margin:8px 0}
button.ab{font:500 14px/1 Roboto,system-ui,sans-serif;border:0;border-radius:20px;min-height:38px;padding:0 16px;background:var(--g);color:#22083d;margin:3px 4px 3px 0;cursor:pointer}
button.ab.s{background:var(--tonal);color:#eadbff}
button.ic{font:500 15px/1 Roboto,system-ui,sans-serif;width:38px;height:38px;border-radius:19px;border:1px solid var(--line);background:transparent;color:var(--g2);cursor:pointer;padding:0}
button.ic:disabled{opacity:.35}
.pal{display:flex;gap:6px;overflow-x:auto;padding:2px 0 6px}
.gb{flex:0 0 auto;min-width:42px;height:42px;border-radius:10px;border:2px solid transparent;font:700 16px Roboto,system-ui,sans-serif;color:#1a0a2a;cursor:pointer;padding:0 8px}
.gb.H{background:var(--pink)}.gb.X,.gb.Y,.gb.Z{background:var(--blue)}.gb.T{background:var(--g)}
.gb.CX,.gb.CZ{background:var(--tonal);color:var(--g2);border-color:var(--line);font-size:13px}
.gb.E{background:transparent;color:var(--dim);border-color:var(--line);font-size:13px}
.gb.on{border-color:#fff;box-shadow:0 0 0 2px var(--g)}
#tip{font-size:12.5px;color:var(--dim);min-height:19px;margin:0 0 4px}
.gw{overflow-x:auto;padding-bottom:4px}#grid{position:relative;display:inline-block;min-width:100%}
.row{display:flex;height:44px;align-items:center}.lab{flex:0 0 46px;font:12px ui-monospace,Menlo,monospace;color:var(--dim)}
.cell{flex:0 0 42px;height:44px;position:relative;display:grid;place-items:center;cursor:pointer}
.cell:before{content:"";position:absolute;left:0;right:0;top:50%;height:1.5px;background:#5a4a80}
.cell.sel{background:rgba(178,107,255,.18);border-radius:8px}
.cell:not(.has):hover:after{content:"";position:absolute;inset:6px;border:1px dashed var(--line);border-radius:8px}
.g{position:relative;z-index:2;width:34px;height:34px;border-radius:8px;display:grid;place-items:center;font:700 15px Roboto,system-ui,sans-serif;color:#1a0a2a}
.g.H{background:var(--pink)}.g.X,.g.Y,.g.Z{background:var(--blue)}.g.T{background:var(--g)}.g.o{background:#6b5d8c;color:#fff}
.dot{position:relative;z-index:2;width:13px;height:13px;border-radius:50%;background:var(--g2)}
.tg{position:relative;z-index:2;width:28px;height:28px;border-radius:50%;border:2px solid var(--g2);background:var(--panel);display:grid;place-items:center;color:var(--g2);font:600 20px/1 system-ui}
.tg.z{border-radius:50%;width:13px;height:13px;border:0;background:var(--g2)}
.ln{position:absolute;width:2px;background:var(--g2);z-index:1;margin-left:-1px}
.ring{flex:0 0 28px;height:28px;border-radius:50%;margin-left:6px;border:1.5px solid var(--line);background:conic-gradient(var(--g) 0deg,var(--g) 0deg,transparent 0deg)}
.tools{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:4px}.tools .sp{flex:1}.tools span.k{font-size:12px}
.chart{display:flex;gap:6px;align-items:flex-end;height:128px;overflow-x:auto;padding-top:4px}
.bc{flex:0 0 auto;min-width:34px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.bc .v{font:11px Roboto,system-ui,sans-serif;color:var(--dim)}.bc .b{width:26px;border-radius:5px 5px 0 0;background:linear-gradient(180deg,var(--pink),var(--g));min-height:2px}
.bc .l{font:11px ui-monospace,Menlo,monospace;color:var(--g2);margin-top:3px}
details{margin:0}summary{cursor:pointer;font-weight:500;color:var(--g2);padding:2px 0;list-style:none}summary::-webkit-details-marker{display:none}
summary:before{content:"\25B8  ";color:var(--dim)}details[open]>summary:before{content:"\25BE  "}
pre{white-space:pre;overflow-x:auto;margin:6px 0;font:12px/1.5 ui-monospace,Menlo,monospace;background:#0f0b18;border:1px solid var(--line);border-radius:10px;padding:8px}
button.chip{font:500 12.5px/1 Roboto,system-ui,sans-serif;min-height:32px;padding:0 11px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--dim);margin:2px 4px 2px 0;cursor:pointer}
button.chip.on{background:var(--tonal);color:#eadbff;border-color:transparent}
#out{max-height:150px;overflow:auto;font:12.5px/1.5 ui-monospace,Menlo,monospace}#out div{margin:2px 0;white-space:pre-wrap}.you{color:var(--g2)}.sys{color:var(--dim)}
.crow{display:flex;gap:6px;margin-top:6px}.crow input{flex:1;min-width:0;font:14px ui-monospace,Menlo,monospace;padding:0 12px;min-height:40px;border-radius:20px;border:1px solid var(--line);background:#0f0b18;color:var(--tx)}
textarea{width:100%;font:13px ui-monospace,Menlo,monospace;padding:8px;border-radius:10px;border:1px solid var(--line);background:#0f0b18;color:var(--tx);height:80px}
"""

COMPOSER_HTML = """<div class="card"><div class="pal" id="pal"></div><div id="tip"></div>
<div class="gw"><div id="grid"></div></div>
<div class="tools"><button class="ic" id="uq" title="Fewer qubits">&minus;</button><span class="k">qubits</span><button class="ic" id="aq" title="More qubits">+</button>
<button class="ic" id="us" title="Fewer steps">&minus;</button><span class="k">steps</span><button class="ic" id="as" title="More steps">+</button>
<span class="sp"></span><button class="ic" id="undo" title="Undo">&#x21B6;</button><button class="ic" id="redo" title="Redo">&#x21B7;</button><button class="ic" id="clr" title="Clear">&#x2715;</button></div></div>"""

CODE_HTML = """<div class="card"><details><summary>Code for this circuit</summary>
<div style="margin-top:6px"><button class="chip on" data-t="qiskit">Qiskit</button><button class="chip" data-t="qasm">OpenQASM 3</button><button class="chip" data-t="qtext">Q.js text</button><button class="chip" id="copy">Copy</button></div>
<pre id="code"></pre><div class="k" id="codenote"></div></details></div>"""

CONSOLE_HTML = """<div class="card"><details open><summary>&#x1F5A5;&#xFE0F; Q Console: type commands</summary>
<div id="out" style="margin-top:6px"></div><div id="chips" style="margin-top:6px"></div>
<div class="crow"><input id="cmd" type="text" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="Type a command, like  H 1"><button class="ab" id="go" style="margin:0">Go</button></div></details></div>"""

COMPOSER_JS = r"""
var G=[["I"]],tool="H",pend=null,undoS=[],redoS=[],codeTab="qiskit",MAXQ=5,MAXC=14;
var TOOLS=[["H","H"],["X","X"],["Y","Y"],["Z","Z"],["T","T"],["CX","CNOT"],["CZ","CZ"],["E","Erase"]];
var TIPS={H:"H makes a coin flip.",X:"X flips 0 and 1.",Y:"Y flips with a twist.",Z:"Z turns the phase.",T:"T turns the phase a little.",CX:"CNOT: tap the control, then the target in the same step.",CZ:"CZ: tap one qubit, then another in the same step.",E:"Tap a gate to remove it."};
function gtext(g){return g.map(function(r){return r.join("-")}).join("\n")}
function parseG(t){var g=t.split(/\r?\n/).filter(function(r){return r.trim()}).map(function(r){return r.trim().split(/[-\s=+]+/).filter(Boolean)});var w=0;g.forEach(function(r){if(r.length>w)w=r.length});g.forEach(function(r){while(r.length<w)r.push("I")});return g.length?g:[["I"]]}
function commit(g,fromCon){undoS.push(gtext(G));if(undoS.length>60)undoS.shift();redoS=[];pend=null;if(fromCon)pending=true;loadText(gtext(g))}
function doUndo(){if(!undoS.length)return false;redoS.push(gtext(G));pend=null;loadText(undoS.pop());return true}
function doRedo(){if(!redoS.length)return;undoS.push(gtext(G));pend=null;loadText(redoS.pop())}
function clearLink(g,c){var l=[];g.forEach(function(r,i){if(/#/.test(r[c]))l.push(i)});l.forEach(function(i){g[i][c]="I"})}
function tapCell(r,c){var g=G.map(function(x){return x.slice()}),t=g[r][c],T=tool;
 if(T==="CX"||T==="CZ"){var k=T==="CX"?"X":"Z";
  if(!pend||pend.c!==c){pend={r:r,c:c};render();$("tip").textContent="Now tap the target qubit in this same step.";return}
  if(pend.r===r){pend=null;render();return}
  clearLink(g,c);g[pend.r][c]=k+"#0";g[r][c]=k+"#1";commit(g);return}
 pend=null;
 if(T==="E"||t===T){if(/#/.test(t))clearLink(g,c);else g[r][c]="I";commit(g);return}
 if(/#/.test(t))clearLink(g,c);g[r][c]=T;commit(g)}
function render(){var n=G.length,m=G[0].length,h="",r,c,lines="";
 for(r=0;r<n;r++){h+='<div class="row"><div class="lab">q['+r+']</div>';
  for(c=0;c<m;c++){var t=G[r][c],has=t!=="I",inner="",sel=pend&&pend.r===r&&pend.c===c;
   if(/^X#0$|^Z#0$/.test(t))inner='<span class="dot"></span>';
   else if(t==="X#1")inner='<span class="tg">+</span>';
   else if(t==="Z#1")inner='<span class="dot"></span>';
   else if(/#/.test(t))inner='<span class="g o">'+esc(t.split("#")[0])+'</span>';
   else if(has)inner='<span class="g '+(/^[HXYZT]$/.test(t)?t:"o")+'">'+esc(t)+'</span>';
   else if(sel)inner='<span class="dot"></span>';
   h+='<div class="cell'+(has||sel?" has":"")+(sel?" sel":"")+'" data-r="'+r+'" data-c="'+c+'">'+inner+'</div>'}
  h+='<div class="ring" id="ring'+r+'"></div></div>'}
 for(c=0;c<m;c++){var rs=[];for(r=0;r<n;r++)if(/#/.test(G[r][c]))rs.push(r);
  if(rs.length>1)lines+='<div class="ln" style="left:'+(46+c*42+21)+'px;top:'+(Math.min.apply(0,rs)*44+22)+'px;height:'+((Math.max.apply(0,rs)-Math.min.apply(0,rs))*44)+'px"></div>'}
 $("grid").innerHTML=h+lines;
 Array.prototype.forEach.call(document.querySelectorAll(".cell"),function(e){e.onclick=function(){tapCell(+e.getAttribute("data-r"),+e.getAttribute("data-c"))}});
 $("undo").disabled=!undoS.length;$("redo").disabled=!redoS.length;$("uq").disabled=n<=1;$("aq").disabled=n>=MAXQ;$("us").disabled=m<=1;$("as").disabled=m>=MAXC;
 if(!pend)$("tip").textContent=TIPS[tool];
 paintRings(lastRes);paintCode()}
function paintRings(res){if(!res||!res.length)return;for(var i=0;i<G.length;i++){var p=0;res.forEach(function(r){if(r.state.replace("|","").charAt(i)==="1")p+=r.probability});var e=$("ring"+i);if(e)e.style.background="conic-gradient(var(--g) "+Math.round(p*360)+"deg,transparent 0deg)"}}
function buildPal(){var h="";TOOLS.forEach(function(t){h+='<button class="gb '+t[0]+(t[0]===tool?" on":"")+'" data-t="'+t[0]+'">'+t[1]+'</button>'});$("pal").innerHTML=h;
 Array.prototype.forEach.call(document.querySelectorAll(".gb"),function(b){b.onclick=function(){tool=b.getAttribute("data-t");pend=null;buildPal();render()}})}
function qiskit(){var n=G.length,m=G[0].length,l=["from qiskit import QuantumCircuit","from qiskit.quantum_info import Statevector","","qc = QuantumCircuit("+n+")"],c,r;
 for(c=0;c<m;c++){var ctl=-1,tg=-1,k="";for(r=0;r<n;r++){var t=G[r][c];if(t==="I")continue;
  if(/#0$/.test(t)){ctl=r;k=t.charAt(0)}else if(/#1$/.test(t))tg=r;else l.push("qc."+t.toLowerCase()+"("+r+")")}
  if(ctl>=0&&tg>=0)l.push("qc."+(k==="X"?"cx":"cz")+"("+ctl+", "+tg+")")}
 l.push("","print(Statevector(qc).probabilities_dict())","# or: qc.measure_all() and run it on a Sampler");return l.join("\n")}
function qasm(){var n=G.length,m=G[0].length,l=["OPENQASM 3.0;","include \"stdgates.inc\";","qubit["+n+"] q;"],c,r;
 for(c=0;c<m;c++){var ctl=-1,tg=-1,k="";for(r=0;r<n;r++){var t=G[r][c];if(t==="I")continue;
  if(/#0$/.test(t)){ctl=r;k=t.charAt(0)}else if(/#1$/.test(t))tg=r;else l.push(t.toLowerCase()+" q["+r+"];")}
  if(ctl>=0&&tg>=0)l.push((k==="X"?"cx":"cz")+" q["+ctl+"], q["+tg+"];")}
 l.push("bit["+n+"] c;","c = measure q;");return l.join("\n")}
function paintCode(){var s=codeTab==="qiskit"?qiskit():codeTab==="qasm"?qasm():gtext(G);$("code").textContent=s;
 $("codenote").textContent=codeTab==="qiskit"?"Heads up: Qiskit numbers qubits from 0, and prints qubit 0 on the right. Here q[0] is the top row and the leftmost bit.":codeTab==="qasm"?"OpenQASM 3 is the standard text format that many quantum tools read.":"Q.js text: rows are qubits, columns are steps. X#0 and X#1 make a CNOT."}
function loadText(text){var c=Q(text);c.name="lab";c.sort$();cur=c;G=parseG(textOf(c));render();c.evaluate$()}
function bars(res){var n=G.length,h="",lim=n<=3?0:0.0005;res.forEach(function(r){var p=r.probability;if(p<=lim&&n>3)return;var s=r.state.replace("|","").replace("⟩","");
 h+='<div class="bc"><span class="v">'+Math.round(p*100)+'%</span><div class="b" style="height:'+Math.round(p*92)+'px"></div><span class="l">'+s+'</span></div>'});$("bars").innerHTML='<div class="chart">'+h+'</div>';paintRings(res)}
window.addEventListener("DOMContentLoaded",function(){buildPal();
 $("aq").onclick=function(){var g=G.map(function(r){return r.slice()});g.push(g[0].map(function(){return "I"}));commit(g)};
 $("uq").onclick=function(){var g=G.map(function(r){return r.slice()}),i=g.length-1;g.pop();g[0].forEach(function(_,c){var any=false;g.forEach(function(r){if(/#/.test(r[c]))any=true});if(any){var cnt=0;g.forEach(function(r){if(/#/.test(r[c]))cnt++});if(cnt<2)clearLink(g,c)}});commit(g)};
 $("as").onclick=function(){var g=G.map(function(r){return r.slice().concat(["I"])});commit(g)};
 $("us").onclick=function(){var g=G.map(function(r){var x=r.slice();x.pop();return x});commit(g)};
 $("undo").onclick=doUndo;$("redo").onclick=doRedo;
 $("clr").onclick=function(){commit(G.map(function(r){return r.map(function(){return "I"})}))};
 Array.prototype.forEach.call(document.querySelectorAll("[data-t]"),function(b){if(b.className.indexOf("chip")<0)return;b.onclick=function(){codeTab=b.getAttribute("data-t");Array.prototype.forEach.call(document.querySelectorAll("button.chip[data-t]"),function(x){x.className="chip"+(x===b?" on":"")});paintCode()}});
 $("copy").onclick=function(){var t=$("code").textContent;try{navigator.clipboard.writeText(t).then(function(){$("copy").textContent="Copied"},function(){$("copy").textContent="Select and copy"})}catch(e){$("copy").textContent="Select and copy"}setTimeout(function(){$("copy").textContent="Copy"},1500)};
 if(window.start)start()});
"""

CONSOLE_JS = r"""
var pending=false,CHIPS=%CHIPS%;
function say(h,c){var d=document.createElement("div");if(c)d.className=c;d.innerHTML=h;$("out").appendChild(d);$("out").scrollTop=$("out").scrollHeight}
function gridOf(){return G.map(function(r){return r.slice()})}
function lastUsed(g){var m=-1;g.forEach(function(r){r.forEach(function(t,i){if(t!=="I"&&i>m)m=i})});return m}
function blank(n,m){var g=[],i,j;for(i=0;i<n;i++){g.push([]);for(j=0;j<m;j++)g[i].push("I")}return g}
function applyGrid(g,msg){commit(g,true);if(msg)say(msg,"sys")}
function addGate(spec,msg){var g=gridOf(),col=lastUsed(g)+1;while(col>=g[0].length)g.forEach(function(r){r.push("I")});spec.forEach(function(s){g[s[0]][col]=s[1]});applyGrid(g,msg+" (step "+(col+1)+")")}
function q(n,g){var i=parseInt(n,10);if(!(i>=1&&i<=g.length)){say("&#x1F914; This circuit has "+g.length+" qubit"+(g.length>1?"s":"")+". Use a number from 1 to "+g.length+", or make a bigger circuit with <b>new 3</b>.","bad");return -1}return i-1}
var NAMES={h:"H",x:"X",y:"Y",z:"Z",t:"T",coin:"H",flip:"X",not:"X",hadamard:"H",phase:"T"};
var NOTE={H:"a coin flip!",X:"it flips 0 and 1.",Y:"a flip with a twist.",Z:"it turns the phase (you cannot see that yet).",T:"a small phase turn."};
function bar(p){var n=Math.round(p*20),s="";for(var i=0;i<20;i++)s+=i<n?"█":"░";return s}
function explain(res){var big=res.filter(function(r){return r.probability>0.005});
 if(big.length===1)return "It always ends as "+big[0].state+". No luck involved.";
 var nq=res[0].state.replace("|","").replace("⟩","").length;
 if(nq>1){var marg=[],i,k;for(i=0;i<nq;i++){var p1=0;res.forEach(function(r){if(r.state.replace("|","").charAt(i)==="1")p1+=r.probability});marg.push(p1)}
  var ent=res.some(function(r){var st=r.state.replace("|","").replace("⟩","");var pr=1;for(k=0;k<nq;k++)pr*=st.charAt(k)==="1"?marg[k]:1-marg[k];return Math.abs(pr-r.probability)>0.02});
  if(ent)return "Entangled! The qubits are linked: knowing one tells you about the others.";}
 var eq=big.every(function(r){return Math.abs(r.probability-big[0].probability)<0.02});
 if(eq)return "A fair mix of "+big.length+" outcomes. That is superposition!";
 return "A weighted mix: some outcomes are more likely than others."}
function conPrint(res){if(!pending)return;pending=false;var h="";res.forEach(function(r){if(r.probability>=0.005||res.length<=4)h+=r.state+" "+bar(r.probability)+" "+Math.round(r.probability*100)+"%\n"});say(h,"sys");say("&#x1F4A1; "+explain(res),"ok")}
function sample(n){var counts={},i,k;for(i=0;i<n;i++){var x=Math.random(),acc=0,pick=lastRes[lastRes.length-1].state;for(k=0;k<lastRes.length;k++){acc+=lastRes[k].probability;if(x<acc){pick=lastRes[k].state;break}}counts[pick]=(counts[pick]||0)+1}return counts}
function helpText(){say("<b>Add a gate</b> (it goes in the next step):\n  H 1   coin flip on qubit 1\n  X 2   flip qubit 2\n  Z 1, Y 1, T 1\n  CNOT 1 2   qubit 1 controls qubit 2\n  CZ 1 2, SWAP 1 2\n<b>See what happens</b>:\n  run      the chances\n  shots 20 measure it 20 times\n  show     draw the circuit\n  text     the circuit as text\n<b>Other</b>:\n  new 3    a fresh circuit with 3 qubits\n  clear    empty it\n  undo     take back the last change\n  help     this list","sys")}
function runCmd(line){
 var w=line.trim().toLowerCase().replace(/^[>›$\s]+/,"").split(/[\s,]+/).filter(Boolean);if(!w.length)return;
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
 if(c==="shots"||c==="measure"||c==="flipcoins"){var n=Math.max(1,Math.min(1000,parseInt(w[1],10)||20)),cnt=sample(n),h="Measured "+n+" time"+(n>1?"s":"")+":\n";Object.keys(cnt).sort().forEach(function(s){h+=s+" "+(cnt[s]>40?"█".repeat(Math.round(cnt[s]/n*30)):"█".repeat(cnt[s]))+" "+cnt[s]+"\n"});say(h,"sys");say("Every measurement gives just one answer. The chances show up when you repeat it.","ok");if(window.onShots)onShots(cnt);return}
 if(c==="show"||c==="draw"||c==="diagram"){say(esc(cur.toDiagram(true)),"sys");return}
 if(c==="text"){say(esc(gtext(G)),"sys");return}
 if(c==="new"||c==="qubits"){var nq=parseInt(w[1],10)||1;if(nq<1||nq>5){say("&#x1F914; Pick 1 to 5 qubits.","bad");return}applyGrid(blank(nq,8),"New circuit with "+nq+" qubit"+(nq>1?"s":"")+", all starting as 0.");return}
 if(c==="clear"||c==="reset"){applyGrid(blank(G.length,G[0].length),"Cleared.");return}
 if(c==="undo"){if(!doUndo()){say("Nothing to undo.","bad");return}pending=true;say("Undone.","sys");return}
 var guess=["help","run","shots","show","text","new","clear","undo","H","X","Z","CNOT"],near="";guess.forEach(function(x){if(!near&&x.toLowerCase().charAt(0)===c.charAt(0))near=x});
 say("&#x1F914; I do not know <b>"+esc(c)+"</b> yet."+(near?" Did you mean <b>"+near+"</b>?":"")+" Type <b>help</b> to see what I know.","bad")}
window.addEventListener("DOMContentLoaded",function(){var ch=$("chips");CHIPS.forEach(function(c){var b=document.createElement("button");b.className="chip";b.textContent=c;b.onclick=function(){$("cmd").value=c;$("go").click()};ch.appendChild(b)});
 $("go").onclick=function(){var v=$("cmd").value;$("cmd").value="";runCmd(v)};$("cmd").addEventListener("keydown",function(e){if(e.key==="Enter")$("go").click()});
 say("Hi! I am the Q Console. Type <b>help</b> or tap a button below.","sys")});
"""
