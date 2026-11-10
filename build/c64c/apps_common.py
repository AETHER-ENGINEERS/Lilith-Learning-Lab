CSS = """<style>
*{box-sizing:border-box}body{font:15px system-ui,Roboto,sans-serif;margin:0;padding:12px;background:#150d27;color:#f1ebff}
button,select{font:inherit;border:0;border-radius:20px;padding:8px 14px;background:#2d2046;color:#e7d9ff;font-weight:600;margin:3px 3px 3px 0}
button.on{background:#b26bff;color:#1b0b33}.m{color:#c9b8e8;margin:6px 0}.ok{color:#8fe3a8}.bad{color:#ff9b9b}
textarea,input[type=text],input[type=number]{width:100%;font:13px ui-monospace,Menlo,monospace;background:#0e0820;color:#f1ebff;border:1px solid #3a2a5c;border-radius:8px;padding:8px}
canvas{max-width:100%;image-rendering:pixelated;border-radius:6px}
table{border-collapse:collapse;font-size:13px}td,th{padding:3px 8px;border-bottom:1px solid #3a2a5c;text-align:left}
code,.mono{font-family:ui-monospace,Menlo,monospace;color:#ffd27f}.row{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.reg{font:13px ui-monospace,monospace;background:#0e0820;border-radius:8px;padding:6px 8px;margin:6px 0;white-space:pre-wrap}
</style>"""

# Shared C64 machine + text screen used by the BASIC and assembler apps.
SCREEN_JS = r"""
var PAL=["#000000","#ffffff","#883932","#67b6bd","#8b3f96","#55a049","#40318d","#bfce72","#8b5429","#574200","#b86962","#505050","#787878","#94e089","#7869c4","#9f9f9f"];
var M=new Uint8Array(65536),CR=new Uint8Array(1024),cur={row:0,col:0,color:14,rev:false},inst=0;
function wr(a,v){a&=65535;v&=255;if(a>=0xD800&&a<0xDC00)CR[a-0xD800]=v&15;else M[a]=v}
function rd(a){a&=65535;if(a>=0xD800&&a<0xDC00)return CR[a-0xD800]|0xF0;if(a==0xD012)return(inst>>2)&255;if(a==0xDC00||a==0xDC01)return 255;return M[a]}
function resetScreen(){for(var i=0;i<1000;i++){M[1024+i]=32;CR[i]=14}M[0xD020]=14;M[0xD021]=6;cur.row=0;cur.col=0;cur.color=14;cur.rev=false}
var cv=document.getElementById("scr"),cx=cv.getContext("2d");
function sc2ch(c){c&=127;if(c==0)return"@";if(c<=26)return String.fromCharCode(64+c);if(c==27)return"[";if(c==28)return"£";if(c==29)return"]";if(c==30)return"↑";if(c==31)return"←";if(c<64)return String.fromCharCode(c);return"▒"}
function draw(){var W=cv.width,H=cv.height,bx=40,by=34;cx.fillStyle=PAL[M[0xD020]&15];cx.fillRect(0,0,W,H);cx.fillStyle=PAL[M[0xD021]&15];cx.fillRect(bx,by,400,250);
cx.font="bold 11px ui-monospace,Menlo,monospace";cx.textAlign="center";cx.textBaseline="middle";
for(var r=0;r<25;r++)for(var c=0;c<40;c++){var sc=M[1024+r*40+c],x=bx+c*10,y=by+r*10;if(sc==32)continue;var col=PAL[CR[r*40+c]&15];if(sc&128){cx.fillStyle=col;cx.fillRect(x,y,10,10);cx.fillStyle=PAL[M[0xD021]&15]}else cx.fillStyle=col;cx.fillText(sc2ch(sc),x+5,y+5.5)}}
function scroll(){for(var i=0;i<960;i++){M[1024+i]=M[1064+i];CR[i]=CR[i+40]}for(var j=960;j<1000;j++){M[1024+j]=32;CR[j]=cur.color}}
function newline(){cur.col=0;cur.row++;if(cur.row>=25){scroll();cur.row=24}}
var COLC={5:1,28:2,30:5,31:6,129:8,144:0,149:9,150:10,151:11,152:12,153:13,154:14,155:15,156:4,158:7,159:3};
function chrout(p){p&=255;
if(p==13||p==141){cur.rev=false;newline();return}
if(p==147){for(var i=0;i<1000;i++){M[1024+i]=32;CR[i]=cur.color}cur.row=0;cur.col=0;return}
if(p==19){cur.row=0;cur.col=0;return}if(p==17){if(cur.row<24)cur.row++;return}if(p==145){if(cur.row>0)cur.row--;return}
if(p==29){if(cur.col<39)cur.col++;return}if(p==157){if(cur.col>0)cur.col--;return}
if(p==18){cur.rev=true;return}if(p==146){cur.rev=false;return}
if(COLC[p]!==undefined){cur.color=COLC[p];return}
if(p<32||(p>=128&&p<160))return;
var s;if(p>=192)s=p-128;else if(p>=160)s=p-64;else if(p>=96)s=p-32;else if(p>=64)s=p-64;else s=p;
if(cur.rev)s|=128;M[1024+cur.row*40+cur.col]=s;CR[cur.row*40+cur.col]=cur.color;cur.col++;if(cur.col>=40)newline()}
"""
