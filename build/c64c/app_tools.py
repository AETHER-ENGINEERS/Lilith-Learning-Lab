"""Small C64 hardware explainer labs: memory banking, user port, tape pulses, D64 disk."""
import os
from apps_common import CSS
HERE = os.path.dirname(os.path.abspath(__file__))
CSS3 = CSS.replace("</style>", "table td,table th{padding:3px 6px}.mono{font-family:ui-monospace,monospace}.bit{display:inline-block;width:30px;text-align:center;border-radius:6px;margin:1px;padding:4px 0;background:#2d2046;cursor:pointer;font:12px ui-monospace,monospace}.bit.on{background:#b26bff;color:#1b0b33}</style>")
HEAD = "<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">" + CSS3 + "</head><body>"
COMMON = "function done(){try{if(window.lilith)lilith.complete()}catch(e){}}var $=function(i){return document.getElementById(i)};function hex(v,n){var s=v.toString(16).toUpperCase();while(s.length<n)s='0'+s;return s}\n"

MEM = HEAD + """<div class="m">The 6510 sees 64 KB, but ROMs and the I/O chips share addresses with RAM. Three bits of $0001 choose the view. Try at least four different settings, including one that shows the character ROM and one that shows only RAM.</div>
<div class="row"><span class="bit" id="b0">LORAM</span><span class="bit" id="b1">HIRAM</span><span class="bit" id="b2">CHAREN</span> <span class="mono">$0001 low bits = <b id="v"></b></span></div>
<table id="t"></table><div class="row">Probe address $<input type="text" id="pa" value="D000" style="width:90px"><span id="pr" class="mono"></span></div><div id="g" class="m"></div>
<script>""" + COMMON + """
var bits=[1,1,1],seen={};
function view(l,h,c){var basic=l&&h?"BASIC ROM":"RAM",kern=h?"KERNAL ROM":"RAM",d=(l||h)?(c?"I/O (VIC, SID, CIA)":"Character ROM"):"RAM";return {a:basic,d:d,e:kern}}
function render(){var v=bits[0]|(bits[1]<<1)|(bits[2]<<2);$("v").textContent="%"+(v+8).toString(2).slice(1)+" ("+v+")";var m=view(bits[0],bits[1],bits[2]);
 [0,1,2].forEach(function(i){$("b"+i).className="bit"+(bits[i]?" on":"")});
 $("t").innerHTML="<tr><th>Range</th><th>What the CPU sees</th></tr><tr><td>$0000-$9FFF</td><td>RAM</td></tr><tr><td>$A000-$BFFF</td><td>"+m.a+"</td></tr><tr><td>$C000-$CFFF</td><td>RAM</td></tr><tr><td>$D000-$DFFF</td><td>"+m.d+"</td></tr><tr><td>$E000-$FFFF</td><td>"+m.e+"</td></tr>";
 seen[v]=m;probe();var n=Object.keys(seen).length,ch=false,ram=false;for(var k in seen){if(seen[k].d=="Character ROM")ch=true;if(seen[k].d=="RAM"&&seen[k].a=="RAM"&&seen[k].e=="RAM")ram=true}
 $("g").innerHTML="Settings tried: "+n+" / 4. Character ROM seen: "+(ch?"yes":"no")+". Pure RAM seen: "+(ram?"yes":"no");if(n>=4&&ch&&ram)done()}
function probe(){var a=parseInt($("pa").value,16)||0,m=view(bits[0],bits[1],bits[2]),w="RAM";if(a>=0xA000&&a<0xC000)w=m.a;else if(a>=0xD000&&a<0xE000)w=m.d;else if(a>=0xE000)w=m.e;$("pr").textContent="$"+hex(a&65535,4)+" is "+w}
[0,1,2].forEach(function(i){$("b"+i).onclick=function(){bits[i]^=1;render()}});$("pa").oninput=probe;render();
</script></body></html>"""

UPORT = HEAD + """<div class="m">The user port gives you eight pins, PB0 to PB7, on CIA 2 port B ($DD01). Each pin is an input or an output depending on its bit in the data direction register DDR ($DD03). Set DDR to $0F (low four pins out, high four in), write $05 to the port, then flip two of the input switches.</div>
<div>DDR $DD03 (1 = output)</div><div id="ddr"></div>
<div>Output register $DD01 (what you write)</div><div id="out"></div>
<div>Outside world on each pin (switches you wire to inputs)</div><div id="pin"></div>
<div class="m mono" id="res"></div><div class="m" id="g"></div>
<script>""" + COMMON + """
var D=0,O=0,P=0xF0,flips=0,mkRow=function(id,get,set){var h="";for(var i=7;i>=0;i--)h+="<span class='bit' data-i='"+i+"'>PB"+i+"</span>";$(id).innerHTML=h;Array.prototype.forEach.call($(id).children,function(b){b.onclick=function(){set(+b.dataset.i);render()}})};
function paint(id,val){Array.prototype.forEach.call($(id).children,function(b){b.className="bit"+((val>>b.dataset.i)&1?" on":"")})}
mkRow("ddr",0,function(i){D^=1<<i});mkRow("out",0,function(i){O^=1<<i});mkRow("pin",0,function(i){P^=1<<i;if(D==0x0F&&i>3)flips|=1<<i});
function render(){paint("ddr",D);paint("out",O);paint("pin",P);var rd=(O&D)|(P&~D&255);
 $("res").innerHTML="DDR=$"+hex(D,2)+"  out=$"+hex(O,2)+"  pins=$"+hex(P,2)+"<br>PEEK($DD01) = (out AND DDR) OR (pins AND NOT DDR) = <b>$"+hex(rd,2)+"</b><br>Pins driven by the C64: "+(D?hex(D,2):"none")+"; pins read from outside: "+hex((~D)&255,2);
 var fc=0;for(var i=4;i<8;i++)if((flips>>i)&1)fc++;var ok=D==0x0F&&(O&15)==5&&fc>=2;$("g").innerHTML=ok?"<span class='ok'>Done: DDR $0F, output $05, two inputs flipped.</span>":"Goal: DDR = $0F, output low nibble = %0101, flip two of PB4-PB7.";if(ok)done()}
render();
</script></body></html>"""

TAPE = HEAD + """<div class="m">The Datassette stores each bit as two pulses. Short, medium and long pulses are all you need. Type a few characters, then see the pulse train, the parity bit and the checksum.</div>
<input type="text" id="t" value="HI64" maxlength="12"><div class="row"><button id="b" class="go">Encode</button></div>
<canvas id="c" width="560" height="120"></canvas><div id="o" class="mono" style="white-space:pre-wrap;font-size:12px"></div><div id="g" class="m"></div>
<script>""" + COMMON + """
var W={S:1,M:1.45,L:1.95};
function encode(bytes){var p=[],log="",x=0;bytes.forEach(function(b){var row="byte $"+hex(b,2)+": marker L M | bits LSB first ";p.push("L","M");var ones=0;for(var i=0;i<8;i++){var bit=(b>>i)&1;ones+=bit;p.push(bit?"M":"S",bit?"S":"M");row+=bit+" "}
 var par=ones%2?0:1;p.push(par?"M":"S",par?"S":"M");row+="| parity "+par+" (odd total)";log+=row+"\\n";x^=b});p.push("L","S");log+="end of data: L S\\nchecksum (XOR of all bytes) = $"+hex(x,2)+"\\n";return {p:p,log:log,x:x}}
function draw(p){var c=$("c"),g=c.getContext("2d");g.clearRect(0,0,560,120);g.strokeStyle="#b26bff";g.lineWidth=2;g.beginPath();var x=4,hi=true,sc=11;g.moveTo(x,90);
 p.forEach(function(k){var w=W[k]*sc;if(x+w*2>556){return}g.lineTo(x,hi?30:90);g.lineTo(x+w,hi?30:90);hi=!hi;g.lineTo(x+w,hi?30:90);x+=w});g.stroke();g.fillStyle="#c9b8e8";g.font="11px sans-serif";g.fillText("each pulse is a half-wave; width = short, medium or long",8,112)}
$("b").onclick=function(){var s=$("t").value,by=[];for(var i=0;i<s.length;i++)by.push(s.charCodeAt(i)&255);if(!by.length)return;var r=encode(by);$("o").textContent=r.log+"pulses: "+r.p.join(" ");draw(r.p);$("g").textContent=by.length>=4?"Done: encoded "+by.length+" bytes.":"Encode at least 4 bytes.";if(by.length>=4)done()};
$("b").onclick();
</script></body></html>"""

DISK = HEAD + """<div class="m">A 1541 disk (D64 image) has 35 tracks. Outer tracks hold more sectors. Pick a track and sector to see which block of the image it is and where it sits in the file. Then add a file to the directory sector at track 18, sector 1.</div>
<div class="row">Track <input type="text" id="tr" value="18" style="width:70px"> Sector <input type="text" id="se" value="1" style="width:70px"><button id="go" class="go">Locate</button></div>
<div id="loc" class="mono"></div>
<div class="row">File name <input type="text" id="fn" value="HELLO" maxlength="16" style="width:150px"> Blocks <input type="text" id="bl" value="3" style="width:60px"><button id="add" class="go">Add to directory</button></div>
<div id="dir" class="mono" style="white-space:pre-wrap;font-size:12px"></div><div id="g" class="m"></div>
<script>""" + COMMON + """
function spt(t){return t<=17?21:t<=24?19:t<=30?18:17}
function block(t,s){var b=0;for(var i=1;i<t;i++)b+=spt(i);return b+s}
var looked={},added=0;
function locate(){var t=+$("tr").value,s=+$("se").value;if(!(t>=1&&t<=35)||!(s>=0&&s<spt(t))){$("loc").textContent="Track 1-35; this track has sectors 0-"+(t>=1&&t<=35?spt(t)-1:"?");return}
 var b=block(t,s);looked[t+","+s]=1;$("loc").innerHTML="Track "+t+" has "+spt(t)+" sectors.<br>Block index = "+b+" (of 683)<br>Byte offset in the .d64 file = "+b+" x 256 = $"+hex(b*256,5)+"<br>Each sector stores 254 data bytes after the two-byte link (next track, next sector).";chk()}
function chk(){var l18=looked["18,1"],n=Object.keys(looked).length;$("g").innerHTML="Looked up track 18 sector 1: "+(l18?"yes":"no")+". Another sector: "+(n>=2?"yes":"no")+". Files added: "+added;if(l18&&n>=2&&added>=1)done()}
var files=[];
$("add").onclick=function(){var n=$("fn").value.toUpperCase().slice(0,16),b=Math.max(1,Math.min(255,+$("bl").value||1));files.push({n:n,b:b});var used=files.reduce(function(a,f){return a+f.b},0),out="";
 files.forEach(function(f,i){var e=[0x82,18+0,0,f.b&255,0];var nm=f.n;while(nm.length<16)nm+="\\u00a0";out+="entry "+(i+1)+" (32 bytes): type $82 (PRG), first track/sector, name "+JSON.stringify(f.n)+" padded with $A0, "+f.b+" blocks\\n"});
 out+="\\nBlocks free = 664 - "+used+" = "+(664-used);$("dir").textContent=out;added=files.length;chk()};
$("go").onclick=locate;locate();
</script></body></html>"""

for name, html in (("mem.html", MEM), ("uport.html", UPORT), ("tape.html", TAPE), ("disk.html", DISK)):
    open(os.path.join(HERE, "apps", name), "w", encoding="utf-8").write(html)
print("tools written")
