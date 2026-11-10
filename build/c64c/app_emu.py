"""Generates C64 emulator labs (webxdc): real C64 emulator (WASM from floooh/chips via 8bitworkshop, zlib),
mini 6510 assembler, optional cc65 C compiler (WASM). Usage: from app_emu import make_app."""
import json, re, os
import app_asm
from pack import emu_blob, tools_blob

HERE = os.path.dirname(os.path.abspath(__file__))
_h = app_asm.HTML
ASM_JS = _h[_h.index("var OPS="):_h.index("var cpu=")]
SHIM = open(os.path.join(HERE, "tc", "shim_inline.js"), encoding="utf-8").read()
EMU = emu_blob()
TOOLS = None

CSS = """<style>
*{box-sizing:border-box}body{font:14px system-ui,Roboto,sans-serif;margin:0;padding:8px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:18px;padding:6px 12px;background:#2d2046;color:#e7d9ff;font-weight:600;margin:2px}
button.on,button.go{background:#b26bff;color:#1b0b33}.m{color:#c9b8e8;margin:4px 0}.ok{color:#8fe3a8}.bad{color:#ff9b9b}
textarea,input[type=text]{width:100%;font:12px ui-monospace,Menlo,monospace;background:#0e0820;color:#f1ebff;border:1px solid #3a2a5c;border-radius:8px;padding:6px}
textarea{height:190px}canvas{width:100%;max-width:560px;display:block;margin:4px auto;image-rendering:pixelated;border-radius:6px;background:#000;outline:none}
.row{display:flex;flex-wrap:wrap;gap:2px;align-items:center}#log{font:11px ui-monospace,monospace;white-space:pre-wrap;color:#ffd27f;max-height:90px;overflow:auto}
.pad button{width:44px;padding:8px 0;border-radius:10px}li{margin:2px 0}ul{margin:4px 0;padding-left:18px}
</style>"""

JS = r"""
var CFG=/*CFG*/{}/*END*/;
var $=function(i){return document.getElementById(i)};
function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
function unb64(s){var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
async function gunzip(u){var r=new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream("gzip")));return new Uint8Array(await r.arrayBuffer())}
function unpack(u){var o={},p=0,dv=new DataView(u.buffer,u.byteOffset,u.byteLength);while(p<u.length){var pl=dv.getUint16(p,true),dl=dv.getUint32(p+2,true);p+=6;var name=new TextDecoder().decode(u.subarray(p,p+pl));p+=pl;o[name]=u.slice(p,p+dl);p+=dl}return o}
function hex(v,n){var s=v.toString(16).toUpperCase();while(s.length<n)s="0"+s;return s}
function log(t,bad){var e=$("log");e.textContent=t;e.className=bad?"bad":""}
/*ASM*/
var G=CFG.goals||[];var X=null,SYS=0,PX=null,cv=$("scr"),cx=cv.getContext("2d"),img=cx.createImageData(392,272),img32=new Uint32Array(img.data.buffer);
var queue=[],actx=null,proc=null,peak=0,frames=0,joy=0,okGoals={},finished=false,quiet=true,booted=false;
async function boot(){
 var f=unpack(await gunzip(unb64(EMUB64)));
 var w=await WebAssembly.instantiate(f["c64.wasm"],{});X=w.instance.exports;X.memory.grow(96);
 var bp=X.malloc(f["c64.bios"].length);new Uint8Array(X.memory.buffer,bp,f["c64.bios"].length).set(f["c64.bios"]);
 SYS=X.machine_init(bp);X.c64_set_joystick_type(SYS,1);hardReset();G.forEach(function(g){if(g.border)g.border0=PX[2*392+2];if(g.bg)g.bg0=PX[100*392+60]});booted=true}
function connect(){PX=new Uint32Array(X.memory.buffer,X.machine_get_pixel_buffer(SYS),392*272)}
function run(n){for(var i=0;i<n;i++){X.machine_exec(SYS,19656)}}
function hardReset(){X.machine_reset(SYS);connect();run(150);peak=0;queue=[]}
function key(c){X.machine_exec(SYS,20000);X.machine_key_down(SYS,c);X.machine_exec(SYS,20000);X.machine_key_up(SYS,c);X.machine_exec(SYS,1)}
function typeText(s){for(var i=0;i<s.length;i++){var ch=s[i];if(ch=="\n")key(13);else{var c=ch.charCodeAt(0);if(c>=97&&c<=122)c-=32;key(c)}}}
function rd(a){return X.machine_mem_read(SYS,a&65535)}
function wr(a,v){X.machine_mem_write(SYS,a&65535,v&255)}
function screenText(){var s="";for(var i=0;i<1000;i++){var v=rd(1024+i)&127;s+=v==0?"@":v<=26?String.fromCharCode(v+64):v<64?String.fromCharCode(v):(v>=65&&v<=90)?String.fromCharCode(v):" "}return s}
function colors(){var set={};for(var y=40;y<232;y+=3)for(var x=40;x<350;x+=3)set[PX[y*392+x]]=1;return Object.keys(set).length}
function loadPRG(prg){var a=prg[0]|(prg[1]<<8);hardReset();var end=a+prg.length-2;for(var k=2;k<prg.length;k++)wr(a+k-2,prg[k]);
 if(a==0x801){[0x2d,0x2f,0x31].forEach(function(p){wr(p,end&255);wr(p+1,end>>8)});typeText("RUN\n")}else typeText("SYS "+a+"\n");log("Loaded "+(prg.length-2)+" bytes at $"+hex(a,4)+".")}
function pcOf(){return X.machine_cpu_get_pc(SYS)}
/* audio */
function startAudio(){if(actx)return;try{actx=new (window.AudioContext||window.webkitAudioContext)();proc=actx.createScriptProcessor(2048,0,1);var ratio=44100/actx.sampleRate,pos=0;
 proc.onaudioprocess=function(e){var o=e.outputBuffer.getChannelData(0);for(var i=0;i<o.length;i++){var k=Math.floor(pos);if(k<queue.length){o[i]=queue[k];pos+=ratio}else o[i]=0}
  if(pos>=queue.length){queue=[];pos=0}else if(pos>20000){queue.splice(0,Math.floor(pos));pos-=Math.floor(pos)}};proc.connect(actx.destination)}catch(e){}}
function frame(){if(!booted)return;X.machine_exec(SYS,19656);frames++;
 var n=X.machine_get_sample_count(),sb=new Float32Array(X.memory.buffer,X.machine_get_sample_buffer(),16384);
 for(var i=0;i<n;i++){var v=sb[i];if(Math.abs(v)>peak)peak=Math.abs(v);if(queue.length<30000)queue.push(v)}
 PX=new Uint32Array(X.memory.buffer,X.machine_get_pixel_buffer(SYS),392*272);img32.set(PX);cx.putImageData(img,0,0);if(frames%15==0)goals()}
function loop(){try{frame()}catch(e){}requestAnimationFrame(loop)}
/* goals */
function evalGoal(g){if(g.screen)return screenText().indexOf(g.screen.toUpperCase())>=0;if(g.ram)return rd(g.ram[0])==g.ram[1];if(g.ramnz)return rd(g.ramnz)!=0;if(g.sound)return peak>0.02;
 if(g.colors)return colors()>=g.colors;if(g.border){return PX[2*392+2]!=g.border0&&(g.border===true||PX[2*392+2]==g.border)}if(g.bg)return PX[100*392+60]!=g.bg0;if(g.ramlow)return (rd(g.ramlow[0])&g.ramlow[1])==g.ramlow[2];if(g.ramgt)return rd(g.ramgt[0])>g.ramgt[1];if(g.pc)return pcOf()>=g.pc[0]&&pcOf()<=g.pc[1];if(g.ramrange){var n=0;for(var i=0;i<g.ramrange[1];i++)if(rd(g.ramrange[0]+i))n++;return n>=g.ramrange[2]}return false}
function goals(){if(!G.length)return;var all=true,h="";G.forEach(function(g,i){var ok=okGoals[i]||(okGoals[i]=evalGoal(g));if(!ok)all=false;h+="<li class='"+(ok?"ok":"")+"'>"+(ok?"&#10003; ":"&#9744; ")+g.t+"</li>"});$("goals").innerHTML=h;if(all&&!finished){finished=true;done()}}
/* keyboard */
function mapKey(e){var k=e.key;if(k=="Enter")return 13;if(k=="Backspace")return 1;if(k.length==1){var c=k.charCodeAt(0);if(c>=97&&c<=122)c-=32;return c}return 0}
var JK={ArrowUp:1,ArrowDown:2,ArrowLeft:4,ArrowRight:8,z:16,Z:16};
function setJoy(){X&&X.c64_joystick(SYS,0,joy)}
document.addEventListener("keydown",function(e){if(document.activeElement!==cv)return;if($("jk").checked&&JK[e.key]){joy|=JK[e.key];setJoy();e.preventDefault();return}var c=mapKey(e);if(c){X.machine_key_down(SYS,c);e.preventDefault()}});
document.addEventListener("keyup",function(e){if(document.activeElement!==cv)return;if($("jk").checked&&JK[e.key]){joy&=~JK[e.key];setJoy();e.preventDefault();return}var c=mapKey(e);if(c){X.machine_key_up(SYS,c);X.machine_exec(SYS,1);e.preventDefault()}});
cv.onclick=function(){cv.focus();startAudio()};
function padbtn(id,bit){var b=$(id);var dn=function(e){joy|=bit;setJoy();e.preventDefault()},up=function(e){joy&=~bit;setJoy();e.preventDefault()};b.onmousedown=b.ontouchstart=dn;b.onmouseup=b.onmouseleave=b.ontouchend=up}
padbtn("ju",1);padbtn("jd",2);padbtn("jl",4);padbtn("jr",8);padbtn("jf",16);
$("send").onclick=function(){var t=$("typ").value;if(!t)return;typeText(t.toUpperCase()+"\n");$("typ").value=""};
$("rst").onclick=function(){hardReset();finished=false;log("Machine reset.")};
$("ret").onclick=function(){key(13)};
/* tabs and build */
var TAB=CFG.tab||"asm",SRC=CFG.src||{};
function showTab(t){TAB=t;["asm","c"].forEach(function(k){var b=$("tab_"+k);if(b)b.className=k==t?"on":""});$("src").value=SRC[t]||""}
function saveSrc(){SRC[TAB]=$("src").value}
$("src").oninput=saveSrc;
["asm","c"].forEach(function(k){var b=$("tab_"+k);if(b)b.onclick=function(){saveSrc();showTab(k)}});
function asmBuild(src){var r=assemble(src),lo=65535,hi=0;r.blocks.forEach(function(b){if(b.b.length){if(b.a<lo)lo=b.a;if(b.a+b.b.length>hi)hi=b.a+b.b.length}});
 if(hi<=lo)throw "Nothing assembled";var d=new Uint8Array(hi-lo+2);d[0]=lo&255;d[1]=lo>>8;r.blocks.forEach(function(b){b.b.forEach(function(v,i){d[2+b.a-lo+i]=v})});
 var st=r.blocks.filter(function(b){return b.b.length})[0].a;return {prg:d,start:st}}
$("go").onclick=async function(){startAudio();saveSrc();log("Building...");await new Promise(function(r){setTimeout(r,20)});
 try{if(TAB=="asm"){var o=asmBuild(SRC.asm);loadPRG(o.prg);if(o.start!=(o.prg[0]|(o.prg[1]<<8))){}}
  else{var p=await buildC(SRC.c);if(p)loadPRG(p)}}catch(e){log(String(e&&e.message||e),1)}finished=false;okGoals={}};
/*STUDIO*/
boot().then(function(){var pre=CFG.autorun;showTab(TAB);goals();loop();if(pre)$("go").onclick()}).catch(function(e){log("Could not start the emulator: "+e,1)});
"""

STUDIO_JS = r"""
var TL=null,SHARE=null;
async function loadTools(){if(TL)return;log("Loading the C toolchain (once)...");TL=unpack(await gunzip(unb64(TOOLSB64)));SHARE=new WASIMemoryFilesystem();
 Object.keys(TL).forEach(function(k){if(k.indexOf("share/")==0){var d=k.split("/");for(var i=1;i<d.length;i++)SHARE.putDirectory(d.slice(0,i).join("/"));SHARE.putFile("./"+k,TL[k])}})}
function tool(name,args,files){var w=new WASIRunner();w.fs.setParent(SHARE);w.initSync(new WebAssembly.Module(TL[name+".wasm"]));
 Object.keys(files).forEach(function(k){w.fs.putFile("./"+k,files[k])});w.addPreopenDirectory(".");w.setArgs([name].concat(args));var e=w.run();
 var err=w.fds[2].getBytesAsString().split("\n").filter(function(l){return l&&!/Warning/.test(l)}).join("\n");return {w:w,e:e,err:err}}
async function buildC(src){await loadTools();var enc=new TextEncoder();
 var r=tool("cc65",["-t","c64","-I","share/cc65/include","-I",".","-Oirs","main.c","-o","main.s"],{"main.c":enc.encode(src)});if(r.e){throw "cc65: "+r.err}
 var s=r.w.fs.getFile("main.s").getBytes();r=tool("ca65",["-t","c64","-I","share/cc65/asminc","-o","main.o","main.s"],{"main.s":s});if(r.e)throw "ca65: "+r.err;
 var o=r.w.fs.getFile("main.o").getBytes();r=tool("ld65",["-t","c64","--cfg-path","share/cc65/cfg","--lib-path","share/cc65/lib","-o","main","main.o","c64.lib"],{"main.o":o});if(r.e)throw "ld65: "+r.err;
 var p=r.w.fs.getFile("main").getBytes().slice();log("Compiled: "+p.length+" bytes.");return p}
"""

BODY = """<div class="m">__DESC__</div>
<canvas id="scr" width="392" height="272" tabindex="0"></canvas>
<div class="row"><button id="rst">Reset</button><button id="ret">RETURN</button><input type="text" id="typ" placeholder="type into the C64" style="width:46%"><button id="send">Type</button>
<label><input type="checkbox" id="jk"> joystick keys</label></div>
<div class="row pad"><button id="jl">&larr;</button><button id="ju">&uarr;</button><button id="jd">&darr;</button><button id="jr">&rarr;</button><button id="jf">FIRE</button></div>
<div class="row">__TABS__<button class="go" id="go">Build and run</button></div>
<textarea id="src" spellcheck="false"></textarea>
<div id="log"></div><ul id="goals"></ul>"""


def make_app(desc, tabs, src, goals, studio=False, autorun=False, out=None):
    global TOOLS
    cfg = {"tab": tabs[0], "src": src, "goals": goals, "autorun": autorun}
    tabhtml = "".join('<button id="tab_%s">%s</button>' % (t, {"asm": "Assembly", "c": "C (cc65)"}[t]) for t in tabs)
    html = "<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">" + CSS + "</head><body>"
    html += BODY.replace("__DESC__", desc).replace("__TABS__", tabhtml)
    js = JS.replace("/*CFG*/{}/*END*/", json.dumps(cfg)).replace("/*ASM*/", ASM_JS)
    pre = "var EMUB64=\"%s\";\n" % EMU
    if studio:
        if TOOLS is None:
            TOOLS = tools_blob()
        pre += "var TOOLSB64=\"%s\";\n" % TOOLS + SHIM + "\n"
        js = js.replace("/*STUDIO*/", STUDIO_JS)
    else:
        js = js.replace("/*STUDIO*/", "async function buildC(){throw 'C is not in this lab'}")
    html += "<script>\n" + pre + js + "\n</script></body></html>"
    if out:
        open(os.path.join(HERE, "apps", out), "w", encoding="utf-8").write(html)
    return html
