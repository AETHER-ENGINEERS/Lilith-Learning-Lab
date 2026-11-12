# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:10px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:8px 12px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px}button.s{background:#3a2a5c;color:#f1ebff}
.k{color:#c9b8e8}label{display:block;margin-top:6px}input[type=text],textarea{width:100%;font:inherit;padding:8px;border-radius:8px;border:1px solid #5c4a85;background:#2a1b48;color:#f1ebff}
.box{background:#0e0820;border-radius:8px;padding:10px;margin:6px 0;line-height:1.7}.ev{font-family:monospace}.ok{color:#8fe3a8}.bad{color:#ff8a8a}.un{color:#ffd28a}
</style></head><body>"""
COMMON = """var $=function(i){return document.getElementById(i)};function done(){try{if(window.lilith)lilith.complete()}catch(e){}}"""
POLICY = HEAD + """
<label>Invite policy <select id="pol"><option value="manual">Manual (default)</option><option value="public">Public</option><option value="whitelist">Whitelist</option></select></label>
<label>Sender <select id="snd"><option value="friend">npub1friend (on the whitelist)</option><option value="stranger">npub1stranger (not listed)</option></select></label>
<label><input type="checkbox" id="off"> The invite arrived while the bot was offline (bot just started)</label>
<button id="go">Deliver invite</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var seen={};
$("go").onclick=function(){var pol=$("pol").value,s=$("snd").value,off=$("off").checked,r,c;
 if(pol==="public"){r=off?"accepted on startup":"accepted at once";c="ok"}
 else if(pol==="whitelist"){if(s==="friend"){r=off?"accepted on startup":"accepted at once";c="ok"}else{r="silently ignored: no reply is sent to the sender";c="bad"}}
 else{r="queued: on_community_invite fires and you call invite.accept()";c="un"}
 $("o").innerHTML='<b class="'+c+'">'+r+'</b>';seen[pol+s]=1;var n=Object.keys(seen).length;$("p").textContent="Cases seen: "+n+" of 4";if(n>=4)done()};
</script></body></html>"""
EVENTS = HEAD + """
<label>What happened <select id="ev"><option value="kick">A member was kicked</option><option value="ban">A member was banned</option><option value="timeout">A member was timed out</option><option value="roles">A member's roles changed</option><option value="nickname">A nickname changed</option><option value="overwrite">A channel overwrite changed</option><option value="pin">A message was pinned</option><option value="dissolve">The owner dissolved the community</option></select></label>
<button id="go">Fire</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var H={kick:"on_member_kick (and on_community_change)",ban:"on_member_ban (and on_community_change)",timeout:"on_member_timeout, later on_member_timeout_end",roles:"on_member_roles_update(member, added, removed)",nickname:"on_member_nickname_update(member, nick)",overwrite:"on_overwrite_update(channel, target, overwrite)",pin:"on_guild_channel_pins_update (and on_community_change)",dissolve:"on_community_dissolve(guild)"};
var seen={};
$("go").onclick=function(){var e=$("ev").value;$("o").innerHTML='<b class="ok">'+H[e]+'</b><br>Every change also arrives raw as on_community_change(change), naming who made it.';seen[e]=1;var n=Object.keys(seen).length;$("p").textContent="Changes tried: "+n+" of 8";if(n>=6)done()};
</script></body></html>"""
HINTS = HEAD + """
<label>Python type hint <select id="h"><option>str</option><option>int</option><option>float</option><option>bool</option><option>vector.Member</option><option>Literal["c","f"]</option><option>Greedy[Member]</option><option>*, rest: str</option><option>Role</option><option>TextChannel</option></select></label>
<label>Command name <input type="text" id="n" value="convert"></label>
<label>Number of arguments <input type="text" id="a" value="2"></label>
<button id="go">Publish</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var M={"str":"text","int":"int","float":"number","bool":"flag","vector.Member":"user picker",'Literal["c","f"]':"choice (dropdown c|f)","Greedy[Member]":"trailing text","*, rest: str":"trailing text","Role":"text, converted in Python","TextChannel":"text, converted in Python"};
var seen={};
$("go").onclick=function(){var h=$("h").value,n=$("n").value,a=parseInt($("a").value)||0,r;
 if(n!==n.toLowerCase()||a>8){r='<b class="un">prefix only</b><br>'+(n!==n.toLowerCase()?"Uppercase names":"More than 8 arguments")+" cannot be expressed natively, so a log line says so."}
 else{r='<b class="ok">/'+n.replace(/</g,"")+'</b> argument type: <b>'+M[h]+'</b><br>Vector checks the input and replies with usage before your code runs.'}
 $("o").innerHTML=r;seen[h]=1;var c=Object.keys(seen).length;$("p").textContent="Hints tried: "+c+" of 5";if(c>=5)done()};
</script></body></html>"""
REACT = HEAD + """
<div class="k">Buttons (leave an emoji blank to get a letter)</div>
<input type="text" id="b1" value="✅"><input type="text" id="b2" value=""><input type="text" id="b3" value="">
<div class="k">Select options</div><label>Number of options <input type="text" id="no" value="3"></label>
<button id="go">Build view</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var NUM=["1","2","3","4","5","6","7","8","9","10"];
var seen={};
$("go").onclick=function(){var used=[],out=[],i,n=0;
 var bs=[$("b1").value.trim(),$("b2").value.trim(),$("b3").value.trim()];bs.forEach(function(b){if(b)used.push(b)});
 bs.forEach(function(b,i){if(b)out.push("Button "+(i+1)+": "+b);else{var L=String.fromCharCode(65+n);while(used.indexOf(L)>=0){n++;L=String.fromCharCode(65+n)}out.push("Button "+(i+1)+": letter "+L);n++}});
 var no=Math.min(25,parseInt($("no").value)||0);for(i=0;i<no;i++)out.push("Option "+(i+1)+": "+(i<10?NUM[i]:String.fromCharCode(65+i-10)));
 $("o").innerHTML=out.join("<br>")+"<br><span class='k'>Reacting clicks it; removing the reaction clicks again.</span>";seen[no>10?"many":"few"]=1;seen["b"+used.length]=1;var c=Object.keys(seen).length;$("p").textContent="Layouts tried: "+c+" of 3";if(c>=3)done()};
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    for k, v in (("policy", POLICY), ("events", EVENTS), ("hints", HINTS), ("react", REACT)):
        open(os.path.join(d, k + ".html"), "w").write(v)
