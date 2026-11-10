# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}button.s{background:#3a2a5c;color:#f1ebff}
.k{color:#c9b8e8}label{display:block;margin-top:6px}input[type=range]{width:100%;accent-color:#b26bff}
.box{background:#0e0820;border-radius:8px;padding:10px;margin:6px 0;min-height:60px;line-height:1.6}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #3a2a5c;padding:3px 5px;text-align:center}
.tk{display:inline-block;padding:4px 8px;margin:2px;border-radius:8px;background:#2a1b48;cursor:pointer}.tk.on{background:#b26bff;color:#1b0b33;font-weight:700}
</style></head><body>"""
COMMON = """var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}"""
NGRAM = HEAD + """
<label>Corpus <select id="c"><option value="0">Nursery rhyme</option><option value="1">Weather talk</option><option value="2">Tiny story</option></select>
Order <select id="o"><option value="1">Bigram</option><option value="2">Trigram</option></select></label>
<button id="g">Generate</button><button id="s" class="s">Show counts</button>
<div id="out" class="box"></div><div id="cnt" class="k"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var CORP=["the cat sat on the mat . the cat saw the dog . the dog sat on the log . the dog saw the cat . the cat ran to the mat .",
"it is sunny today . it is cold today . it will be sunny tomorrow . it will be rainy tomorrow . today it is sunny and warm . tomorrow it is rainy and cold .",
"the girl found a key . the key opened a door . the door led to a garden . the garden had a tree . the girl climbed the tree . the tree was tall ."];
var seed=7;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff}
var seen={};
function model(){var w=CORP[+$("c").value].split(" "),n=+$("o").value,m={},i,k;for(i=0;i+n<w.length;i++){k=w.slice(i,i+n).join(" ");(m[k]=m[k]||[]).push(w[i+n])}return {m:m,w:w,n:n}}
function pick(a){return a[Math.floor(rnd()*a.length)]}
$("g").onclick=function(){var M=model(),w=M.w,out=w.slice(0,M.n),i;for(i=0;i<22;i++){var k=out.slice(out.length-M.n).join(" "),nx=M.m[k];if(!nx)break;out.push(pick(nx))}
 $("out").textContent=out.join(" ");seen[$("c").value+"/"+$("o").value]=1;var n=Object.keys(seen).length;$("p").textContent="Settings tried: "+n+" of 2 needed";if(n>=2)done()};
$("s").onclick=function(){var M=model(),ks=Object.keys(M.m).slice(0,12),h="<table><tr><th>Context</th><th>Next words seen</th></tr>";ks.forEach(function(k){var c={};M.m[k].forEach(function(x){c[x]=(c[x]||0)+1});h+="<tr><td>"+k+"</td><td>"+Object.keys(c).map(function(x){return x+" x"+c[x]}).join(", ")+"</td></tr>"});$("cnt").innerHTML=h+"</table>"+"<div>Trigrams are more fluent but copy the corpus more.</div>"};
</script></body></html>"""
ATTN = HEAD + """
<label>Sentence <select id="se"><option value="0">the animal did not cross the street because it was tired</option><option value="1">the bank by the river was steep</option><option value="2">she poured water into the glass because it was empty</option></select></label>
<label><input type="checkbox" id="cm"> Causal mask (hide later words)</label>
<label>Temperature: <b id="tv"></b><input id="t" type="range" min="2" max="40" value="10"></label>
<div class="k">Tap a word to see where it attends.</div><div id="tk"></div><div id="hm" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var S=["the animal did not cross the street because it was tired","the bank by the river was steep","she poured water into the glass because it was empty"];
var REL=[{"it:animal":3,"it:street":1.2,"it:tired":1,"cross:animal":2,"cross:street":2,"did:not":2,"not:cross":1.5,"was:tired":2,"tired:animal":1.5,"because:it":1,"the:animal":.8,"the:street":.8},
{"bank:river":3,"steep:bank":2,"steep:river":1.5,"was:steep":2,"by:river":2,"river:bank":1.5,"the:bank":.8,"the:river":.8},
{"it:glass":3,"it:empty":1.2,"it:water":1,"poured:water":2.5,"poured:glass":1.5,"into:glass":2,"was:empty":2,"empty:glass":1.5,"she:poured":1.5,"because:it":1}];
var sel=0,cur=-1,seen={};
function words(){return S[+$("se").value].split(" ")}
function score(w,i,j){if(i===j)return 1.2;var k=w[i]+":"+w[j],v=REL[+$("se").value][k]||0;return v+0.3/(1+Math.abs(i-j))}
function weights(i){var w=words(),T=$("t").value/10,cm=$("cm").checked,sc=[],j,m=-1e9;for(j=0;j<w.length;j++){var s=(cm&&j>i)?-1e9:score(w,i,j)/T;sc.push(s);if(s>m)m=s}
 var e=sc.map(function(s){return s<-1e8?0:Math.exp(s-m)}),t=e.reduce(function(a,b){return a+b},0);return e.map(function(x){return x/t})}
function draw(){var w=words();$("tv").textContent=($("t").value/10).toFixed(1);var h="";w.forEach(function(x,i){h+='<span class="tk'+(i===cur?" on":"")+'" data-i="'+i+'">'+x+'</span>'});$("tk").innerHTML=h;
 var els=document.querySelectorAll(".tk");for(var q=0;q<els.length;q++)els[q].onclick=function(){cur=+this.dataset.i;seen[cur]=1;draw();var n=Object.keys(seen).length;$("p").textContent="Words explored: "+n+" of 3";if(n>=3)done()};
 if(cur<0){$("hm").textContent="Select a word.";return}
 var a=weights(cur),o="<b>"+w[cur]+"</b> attends to:<br>";a.forEach(function(x,j){o+='<div style="display:flex;align-items:center;gap:6px"><span style="width:6em">'+w[j]+'</span><div style="height:12px;border-radius:6px;background:#b26bff;width:'+Math.round(x*100)+'%"></div><span class="k">'+x.toFixed(2)+'</span></div>'});$("hm").innerHTML=o}
$("se").onchange=function(){cur=-1;draw()};$("cm").onchange=draw;$("t").oninput=draw;draw();
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "ngram.html"), "w").write(NGRAM)
    open(os.path.join(d, "attn.html"), "w").write(ATTN)
