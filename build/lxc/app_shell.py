"""Generate a self-contained webxdc shell-lab page: Jade Agent Kit VFS + BusyBox wasm + LinuxSim."""
import os, json, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "c64c"))
from pack import pack
V = os.path.join(HERE, "..", "vendor", "jade-agent-kit")

def rd(p, mode="r"):
    return open(p, mode if "b" in mode else mode, **({} if "b" in mode else {"encoding": "utf-8"})).read()

_cache = {}
def parts():
    if _cache: return _cache
    core = rd(os.path.join(HERE, "sim_core.js"))
    cmds = rd(os.path.join(HERE, "sim_cmds.js"))
    cmds = cmds.replace("(function (S) {", "function LinuxCmds(S) {", 1)
    cmds = cmds.rstrip()
    assert cmds.endswith("})(window.__SIM);")
    cmds = cmds[:-len("})(window.__SIM);")] + "}"
    kit = rd(os.path.join(HERE, "sim_lite.js"))
    dev = rd(os.path.join(HERE, "sim_devops.js"))
    blob = ""
    _cache.update(core=core, cmds=cmds, kit=kit, blob=blob, dev=dev)
    return _cache

CSS = """*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#d6e2f0;font:14px/1.45 ui-monospace,Menlo,Consolas,monospace;display:flex;flex-direction:column;height:100vh}
#top{padding:8px 10px;background:#161b22;border-bottom:1px solid #263041;font:13px system-ui,sans-serif}
#top b{color:#ffd166}#tasks{margin:6px 0 0;padding:0;list-style:none}#tasks li{padding:1px 0}#tasks li.ok{color:#7ee787}#tasks li.ok:before{content:"\\2714  "}#tasks li:not(.ok):before{content:"\\25CB  ";color:#8b98a8}
#term{flex:1;overflow:auto;padding:8px 10px;white-space:pre-wrap;word-break:break-word}.e{color:#ff8b8b}.p{color:#7ee787}.pp{color:#79c0ff}
#bar{display:flex;gap:6px;padding:6px 8px;background:#161b22;border-top:1px solid #263041}
#in{flex:1;background:#0d1117;color:#fff;border:1px solid #3a4658;border-radius:6px;padding:8px;font:inherit}
button{background:#238636;color:#fff;border:0;border-radius:6px;padding:8px 12px;font:13px system-ui}button.g{background:#30363d}
#chips{padding:4px 8px;background:#161b22;display:flex;gap:6px;flex-wrap:wrap}#chips span{background:#21262d;border:1px solid #30363d;border-radius:12px;padding:3px 9px;font-size:12px;cursor:pointer}
#done{display:none;background:#12361f;color:#7ee787;padding:8px 10px;font:14px system-ui}#sol{display:none;background:#2a2410;color:#ffd166;padding:8px 10px;font:12px system-ui;white-space:pre-wrap}"""

JS = r"""
function b2u(b){var s=atob(b),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u}
async function unpack(b64){var ds=new Response(new Blob([b2u(b64)]).stream().pipeThrough(new DecompressionStream('gzip'))),buf=new Uint8Array(await ds.arrayBuffer()),dv=new DataView(buf.buffer),o=0,r={};while(o<buf.length){var pl=dv.getUint16(o,true),dl=dv.getUint32(o+2,true);o+=6;var p=new TextDecoder().decode(buf.subarray(o,o+pl));o+=pl;r[p]=buf.subarray(o,o+dl);o+=dl}return r}
var term=document.getElementById('term'),inp=document.getElementById('in'),S=null,hi=-1,busy=false,doneFlag=false,hist=[];
function put(t,c){var s=document.createElement('span');if(c)s.className=c;s.textContent=t;term.appendChild(s);term.scrollTop=term.scrollHeight}
function prompt(){var h=S.users[S.user].home,w=S.cwd;if(w==h)w='~';else if(w.indexOf(h+'/')==0)w='~'+w.slice(h.length);return S.user+'@lilith:'+w+(S.user=='root'?'# ':'$ ')}
function renderTasks(){var ul=document.getElementById('tasks');ul.innerHTML='';CFG.tasks.forEach(function(t,i){var li=document.createElement('li');li.textContent=t.t;if(t.ok)li.className='ok';ul.appendChild(li)})}
var fsH=null;
function checks(){if(!S)return;var fs={exists:function(p){return S.vfs.exists(S.abs(p))},isDir:function(p){return S.vfs.exists(S.abs(p))&&S.vfs.isDir(S.abs(p))},read:function(p){try{return S.vfs.read(S.abs(p))}catch(e){return ''}},mode:function(p){var m=S.getMeta(S.abs(p)).mode&0o7777;var s=m.toString(8);while(s.length<3)s='0'+s;return s},owner:function(p){return S.getMeta(S.abs(p)).owner},group:function(p){return S.getMeta(S.abs(p)).group},ls:function(p){return S.names(S.abs(p||'.'))}};
 var ran=function(re){return S.hist.some(function(h){return new RegExp(re).test(h)})};
 var all=true;CFG.tasks.forEach(function(t){if(t.ok)return;try{var f=new Function('fs','hist','out','cwd','user','S','ran','return ('+t.check+')');if(f(fs,S.hist,S.allout,S.cwd,S.user,S,ran))t.ok=true}catch(e){}if(!t.ok)all=false});renderTasks();
 if(all&&!doneFlag){doneFlag=true;document.getElementById('done').style.display='block';try{window.lilith&&window.lilith.complete&&window.lilith.complete()}catch(e){}}}
async function runLine(line){if(busy)return;busy=true;put(prompt(),'pp');put(line+'\n');if(line.trim()){hist.push(line);hi=hist.length;var r=await S.run(line);if(r.out.indexOf('\x1b[clear]')>=0){term.innerHTML='';r.out=r.out.replace('\x1b[clear]','')}if(r.out)put(r.out.replace(/\x1b\[clear\]/g,''));if(r.err)put(r.err,'e')}checks();busy=false;put('','');inp.focus()}
function complete(){var v=inp.value,m=/(\S*)$/.exec(v),w=m[1],first=!/\s/.test(v.slice(0,v.length-w.length).trim())&&v.slice(0,v.length-w.length).trim()==='';var cands=[];if(first&&w.indexOf('/')<0){cands=Object.keys(S.commands).concat(Object.keys(S.builtins)).filter(function(c){return c.indexOf(w)==0&&S.ext[c]!==false})}else{var di=w.lastIndexOf('/'),d=di>=0?w.slice(0,di+1):'',b=w.slice(di+1);try{var p=S.abs(d||'.');cands=S.names(p).filter(function(n){return n.indexOf(b)==0&&(n[0]!='.'||b[0]=='.')}).map(function(n){return d+n+(S.vfs.isDir(p+'/'+n)?'/':'')})}catch(e){}}
 if(cands.length==1)inp.value=v.slice(0,v.length-w.length)+cands[0]+(cands[0].slice(-1)=='/'?'':' ');else if(cands.length>1){var pre=cands.reduce(function(a,b){var i=0;while(i<a.length&&a[i]==b[i])i++;return a.slice(0,i)});if(pre.length>w.length)inp.value=v.slice(0,v.length-w.length)+pre;else put(prompt()+v+'\n'+cands.join('  ')+'\n')}}
inp.addEventListener('keydown',function(e){if(e.key=='Enter'){var l=inp.value;inp.value='';runLine(l)}else if(e.key=='ArrowUp'){if(hi>0){hi--;inp.value=hist[hi]}e.preventDefault()}else if(e.key=='ArrowDown'){if(hi<hist.length-1){hi++;inp.value=hist[hi]}else{hi=hist.length;inp.value=''}e.preventDefault()}else if(e.key=='Tab'){e.preventDefault();complete()}else if(e.ctrlKey&&e.key=='l'){e.preventDefault();term.innerHTML=''}});
document.getElementById('go').onclick=function(){var l=inp.value;inp.value='';runLine(l)};
document.getElementById('solb').onclick=function(){var s=document.getElementById('sol');s.style.display=s.style.display=='block'?'none':'block'};
document.getElementById('rst').onclick=function(){location.reload()};
(CFG.hints||[]).forEach(function(h){var s=document.createElement('span');s.textContent=h;s.onclick=function(){inp.value=h;inp.focus()};document.getElementById('chips').appendChild(s)});
document.getElementById('intro').innerHTML=CFG.intro;document.getElementById('sol').textContent=CFG.solution||'';if(!CFG.solution)document.getElementById('solb').style.display='none';
(async function(){put('Starting the sandbox...\n');try{var kit={vfs:new LiteVFS()};
 S=new LinuxSim(kit,CFG.sim||{});LiteText(S);LinuxCmds(S);if(CFG.devops)DevopsCmds(S);S.syncPasswd();(CFG.procs||[]).forEach(function(p){S.procs.push(p)});
 S.vars.HOME=S.users[S.user].home;S.vars.USER=S.user;
 for(var i=0;i<(CFG.init||[]).length;i++){await S.run(CFG.init[i])}S.hist=[];S.allout='';
 window.__S=S;term.innerHTML='';put(CFG.welcome||'Type a command. Tab completes, arrow keys recall history.\n','');renderTasks();inp.disabled=false;inp.focus();window.__ready=1}catch(e){put('Could not start: '+e+'\n','e')}})();
"""

def make_shell(cfg, out=None):
    P = parts()
    cfg = dict(cfg)
    sim = cfg.setdefault("sim", {})
    sim.setdefault("user", cfg.get("user", "user"))
    sim.setdefault("cwd", cfg.get("cwd", "/home/user"))
    if "files" in cfg:
        sim["files"] = cfg.pop("files")
    cj = json.dumps(cfg).replace("</", "<\\/")
    html = ("<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><style>" + CSS + "</style></head><body>"
            "<div id=top><div id=intro></div><ul id=tasks></ul></div><div id=done>Lab complete. Nice work!</div><div id=sol></div>"
            "<div id=term></div><div id=chips></div><div id=bar><input id=in autocapitalize=off autocomplete=off autocorrect=off spellcheck=false disabled placeholder='type a command'><button id=go>Run</button><button class=g id=solb>Hint</button><button class=g id=rst>Reset</button></div>"
            "<script>" + P["kit"].replace("</script", "<\\/script") + "</script>"
            "<script>" + P["core"] + "\n" + P["cmds"] + ("\n" + P["dev"] if cfg.get("devops") else "") + "</script>"
            "<script>var CFG=" + cj + ";var BLOB=\"" + P["blob"] + "\";" + JS + "</script></body></html>")
    if out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(html)
    return html

if __name__ == "__main__":
    cfg = {"intro": "<b>Test lab</b>", "tasks": [{"t": "Create a file hello.txt", "check": "fs.exists('hello.txt')"}], "hints": ["ls", "touch hello.txt"],
           "files": {"/home/user/notes.txt": "one\ntwo\nthree\n", "/home/user/docs/a.md": "# A\n"}}
    make_shell(cfg, os.path.join(HERE, "apps", "t_shell.html"))
    print("ok", os.path.getsize(os.path.join(HERE, "apps", "t_shell.html")))
