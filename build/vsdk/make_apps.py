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
 else{r="pending: waits until your code calls accept_invite";c="un"}
 $("o").innerHTML='<b class="'+c+'">'+r+'</b>';seen[pol+s]=1;var n=Object.keys(seen).length;$("p").textContent="Cases seen: "+n+" of 4";if(n>=4)done()};
</script></body></html>"""
EVENTS = HEAD + """
<div class="k">Pick an event and see where it goes</div>
<label>Event <select id="ev"><option>Message</option><option>MessageUpdate</option><option>Delete</option><option>MemberJoin</option><option>MemberLeave</option><option>Typing</option><option>Invite</option><option>Removed</option></select></label>
<label><input type="checkbox" id="mine"> The message was sent by the bot itself</label>
<button id="go">Dispatch</button><div id="o" class="box"></div><div id="p" class="k"></div>
<script>""" + COMMON + """
var R={Message:"on_message handler: chat",MessageUpdate:"on_event: chat edit",Delete:"on_event: moderation",MemberJoin:"on_event: welcome the member",MemberLeave:"on_event: update the member list",Typing:"on_event: usually ignore (expires in 30 s)",Invite:"on_event: apply the invite policy",Removed:"on_event: forget the community"};
var seen={};
$("go").onclick=function(){var e=$("ev").value,r=R[e],c="ok";
 if(e==="Message"&&$("mine").checked){r="skipped: is_mine() is true, so no loop";c="un"}
 $("o").innerHTML='<b class="'+c+'">'+e+'</b><br>'+r;seen[e+($("mine").checked?"m":"")]=1;var n=Object.keys(seen).length;$("p").textContent="Events tried: "+n+" of 6";if(n>=6)done()};
</script></body></html>"""
def main():
    d = os.path.join(HERE, "apps")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "policy.html"), "w").write(POLICY)
    open(os.path.join(d, "events.html"), "w").write(EVENTS)
