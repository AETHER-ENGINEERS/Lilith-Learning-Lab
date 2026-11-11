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
INTENTS = HEAD + """
<div class="k">Intents your bot enables</div>
<label><input type="checkbox" id="guilds" checked> guilds</label>
<label><input type="checkbox" id="gm" checked> guild_messages</label>
<label><input type="checkbox" id="mc"> message_content (privileged)</label>
<label><input type="checkbox" id="mem"> members (privileged)</label>
<label><input type="checkbox" id="pres"> presences (privileged)</label>
<label><input type="checkbox" id="rx"> reactions</label>
<label><input type="checkbox" id="portal"> Also switched on in the developer portal</label>
<button id="go">Connect</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var EV=[["on_ready","guilds"],["on_message (author, channel)","gm"],["message.content has text","mc"],["on_member_join","mem"],["on_presence_update","pres"],["on_reaction_add","rx"]];
var seen={};
$("go").onclick=function(){var priv=$("mc").checked||$("mem").checked||$("pres").checked,out=[],i;
 if(priv&&!$("portal").checked){$("o").innerHTML='<b class="bad">Connection refused</b><br>A privileged intent is enabled in code but not in the developer portal.';seen.refused=1}
 else{for(i=0;i<EV.length;i++){var on=$(EV[i][1]).checked;out.push((on?'<span class="ok">receives</span> ':'<span class="bad">silent</span> ')+EV[i][0])}
  $("o").innerHTML=out.join("<br>");seen[priv?"priv":"plain"]=1}
 var n=Object.keys(seen).length;$("p").textContent="Situations seen: "+n+" of 3";if(n>=3)done()};
</script></body></html>"""
ROUTER = HEAD + """
<label>Prefix <input type="text" id="pf" value="!"></label>
<label>Message <input type="text" id="msg" value="!add 2 3"></label>
<button id="go">Send</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
function split(s){var out=[],cur="",inq=false,i,ch;for(i=0;i<s.length;i++){ch=s[i];if(ch==='"')inq=!inq;else if(ch===" "&&!inq){if(cur)out.push(cur);cur=""}else cur+=ch}if(cur)out.push(cur);return out}
var seen={};
$("go").onclick=function(){var pf=$("pf").value,m=$("msg").value,r,k;
 if(m.indexOf(pf)!==0){r="Not a command: the message does not start with the prefix.";k="ignored"}
 else{var w=split(m.slice(pf.length)),n=w[0],a=w.slice(1);
  if(n==="add"){if(a.length<2){r="MissingRequiredArgument";k="error"}else if(isNaN(+a[0])||isNaN(+a[1])){r="BadArgument: not a number";k="error"}else{r="ctx.send("+(+a[0]+ +a[1])+")";k="ok"}}
  else if(n==="say"){r="ctx.send("+a.join(" ")+")";k="ok"}
  else{r="CommandNotFound: "+n;k="error"}}
 $("o").innerHTML='<b>'+k+'</b><br>'+r.replace(/</g,"&lt;");seen[k]=1;var c=Object.keys(seen).length;$("p").textContent="Outcome kinds seen: "+c+" of 3";if(c>=3)done()};
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "intents.html"), "w").write(INTENTS)
    open(os.path.join(d, "router.html"), "w").write(ROUTER)
