# -*- coding: utf-8 -*-
import os, json
from data import NOUNS, VERBS, PHRASES, VERSES
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = """<style>*{box-sizing:border-box}body{font:15px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:8px 14px;background:#2d2046;color:#e7d9ff;font-weight:600;margin:2px}button.go{background:#b26bff;color:#1b0b33}
.card{background:#211538;border:1px solid #3a2a5c;border-radius:14px;padding:18px;margin:10px 0;text-align:center;min-height:130px}
.big{font-size:34px;line-height:1.3;margin:6px 0}.sm{color:#c9b8e8;font-size:13px}.row{display:flex;flex-wrap:wrap;gap:4px;align-items:center;justify-content:center}
.ok{color:#8fe3a8}.bad{color:#ff9b9b}.bar{height:8px;background:#2d2046;border-radius:4px;overflow:hidden;margin:8px 0}.bar i{display:block;height:100%;background:#b26bff}
.w{display:inline-block;margin:4px;padding:6px 8px;border:1px solid #3a2a5c;border-radius:10px;cursor:pointer;background:#1b1030}.w.on{background:#3a2a5c}.w b{display:block;font-size:22px}
.w span{display:block;font-size:11px;color:#c9b8e8}.rtl{direction:rtl}</style>"""

CARDS = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + CSS + """</head><body>
<div class="row"><select id="deck"><option value="nouns">Nouns</option><option value="verbs">Verbs and adjectives</option><option value="phrases">Phrases</option></select>
<select id="from"></select><span class="sm">&rarr;</span><select id="to"></select></div>
<div class="bar"><i id="pb" style="width:0%"></i></div><div class="sm" id="stat"></div>
<div class="card"><div class="sm" id="lab"></div><div class="big" id="q"></div><div class="sm" id="tr"></div><div id="a" style="display:none"><hr style="border-color:#3a2a5c"><div class="big" id="ans"></div><div class="sm" id="ans2"></div><div class="sm" id="hook" style="margin-top:8px;color:#ffd27f"></div></div></div>
<div class="row"><button class="go" id="show">Show answer</button><button id="no" style="display:none">I missed it</button><button id="yes" class="go" style="display:none">I knew it</button></div>
<div class="sm" style="margin-top:10px">Leitner boxes: a card you know moves up a box and returns later; a missed card goes back to box 1. Reach box 3 on 12 cards to finish the lab.</div>
<script>
var D=__DATA__;var LANGS={en:"English",he:"Hebrew",gr:"Greek",la:"Latin"};
var $=function(i){return document.getElementById(i)};
function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
function fld(r,l,p){var m={en:[0,null],he:[1,2],gr:[3,4],la:[5,null]}[l];return p?(m[1]===null?"":r[m[1]]):r[m[0]]}
["from","to"].forEach(function(id){Object.keys(LANGS).forEach(function(k){var o=document.createElement("option");o.value=k;o.textContent=LANGS[k];$(id).appendChild(o)})});
$("from").value="en";$("to").value="la";
var box={},cur=null,seen=0;
function key(){return $("deck").value+"|"+$("from").value+"|"+$("to").value}
function B(){return box[key()]=box[key()]||{}}
function pick(){var rows=D[$("deck").value],b=B(),best=null,bs=1e9;rows.forEach(function(r,i){var bx=b[i]||1,s=bx*10+Math.random()*9+(b["l"+i]||0);if(bx<5&&s<bs){bs=s;best=i}});if(best===null)best=Math.floor(Math.random()*rows.length);return best}
function stats(){var b=B(),n=0,t=D[$("deck").value].length,m=0;for(var i=0;i<t;i++){var x=b[i]||1;if(x>=3)n++;m+=x}
 var all=0;Object.keys(box).forEach(function(k){for(var i=0;i<D[k.split("|")[0]].length;i++)if((box[k][i]||1)>=3)all++});
 $("pb").style.width=Math.min(100,Math.round(n/t*100))+"%";$("stat").textContent="This deck: "+n+" of "+t+" cards in box 3 or higher. Total in box 3+: "+all+" of 12 needed.";if(all>=12)done()}
function show(){var r=D[$("deck").value][cur],f=$("from").value,t=$("to").value;$("lab").textContent=LANGS[f]+" ("+"box "+(B()[cur]||1)+")";$("q").textContent=fld(r,f);$("q").className="big"+(f=="he"?" rtl":"");$("tr").textContent=(f=="he"||f=="gr")?fld(r,f,1):"";
 $("a").style.display="none";$("show").style.display="";$("yes").style.display=$("no").style.display="none"}
function next(){cur=pick();show();stats()}
$("show").onclick=function(){var r=D[$("deck").value][cur],t=$("to").value;$("ans").textContent=fld(r,t);$("ans").className="big"+(t=="he"?" rtl":"");$("ans2").textContent=(t=="he"||t=="gr")?fld(r,t,1):"";$("hook").textContent=r[6];$("a").style.display="";$("show").style.display="none";$("yes").style.display=$("no").style.display=""};
$("yes").onclick=function(){var b=B();b[cur]=Math.min(5,(b[cur]||1)+1);b["l"+cur]=3;Object.keys(b).forEach(function(k){if(k[0]=="l"&&k!="l"+cur&&b[k]>0)b[k]--});next()};
$("no").onclick=function(){var b=B();b[cur]=1;b["l"+cur]=0;next()};
["deck","from","to"].forEach(function(i){$(i).onchange=next});next();
</script></body></html>"""

READER = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">""" + CSS + """</head><body>
<div class="row"><select id="v"></select></div>
<div class="card" id="box"><div class="sm" id="ref"></div><div id="line" style="margin:8px 0"></div><div class="sm" id="info">Tap a word to see its sound and meaning.</div></div>
<div class="row"><button id="rev">Show smooth translation</button><button id="hide">Hide glosses</button></div>
<div class="card" id="free" style="display:none;min-height:0"></div>
<div class="sm" id="notes"></div><div class="sm" id="prog" style="margin-top:10px"></div>
<script>
var V=__DATA__;var $=function(i){return document.getElementById(i)};
function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
var seen={},cur=0,gloss=true;
V.forEach(function(v,i){var o=document.createElement("option");o.value=i;o.textContent=v.lang+": "+v.ref;$("v").appendChild(o)});
function draw(){var v=V[cur];seen[cur]=1;$("ref").textContent=v.lang+", "+v.ref;var h="";
 v.words.forEach(function(w,i){h+="<div class='w'"+" data-i='"+i+"'><b"+(v.lang=="Hebrew"?" class='rtl'":"")+">"+w[0]+"</b><span>"+w[1]+"</span>"+(gloss?"<span class='ok'>"+w[2]+"</span>":"")+"</div>"});
 $("line").innerHTML="<div class='"+(v.dir=="rtl"?"rtl":"")+"'>"+h+"</div>";
 Array.prototype.forEach.call(document.querySelectorAll(".w"),function(el){el.onclick=function(){var w=v.words[+el.dataset.i];$("info").textContent=w[0]+"  \\u2192  "+w[1]+"  =  "+w[2];Array.prototype.forEach.call(document.querySelectorAll(".w"),function(x){x.className="w"});el.className="w on"}});
 $("free").style.display="none";$("rev").textContent="Show smooth translation";$("free").textContent=v.free;
 $("notes").innerHTML="<b>Grammar notes</b><ul>"+v.notes.map(function(n){return"<li>"+n+"</li>"}).join("")+"</ul>";
 var n=Object.keys(seen).length;$("prog").textContent="Read "+n+" of "+V.length+" passages (open them all to finish).";if(n>=V.length)done()}
$("v").onchange=function(){cur=+$("v").value;draw()};
$("rev").onclick=function(){var f=$("free");f.style.display=f.style.display=="none"?"":"none";$("rev").textContent=f.style.display=="none"?"Show smooth translation":"Hide smooth translation"};
$("hide").onclick=function(){gloss=!gloss;$("hide").textContent=gloss?"Hide glosses":"Show glosses";draw()};
draw();
</script></body></html>"""

def rows(lst):
    return [list(r) for r in lst]

def main():
    out = os.path.join(HERE, "apps"); os.makedirs(out, exist_ok=True)
    d = {"nouns": rows(NOUNS), "verbs": rows(VERBS), "phrases": rows(PHRASES)}
    open(os.path.join(out, "cards.html"), "w", encoding="utf-8").write(CARDS.replace("__DATA__", json.dumps(d, ensure_ascii=False)))
    open(os.path.join(out, "reader.html"), "w", encoding="utf-8").write(READER.replace("__DATA__", json.dumps(VERSES, ensure_ascii=False)))
    print("apps written")

if __name__ == "__main__":
    main()
