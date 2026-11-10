import {WASIRunner, WASIMemoryFilesystem} from './shim.mjs';
import fs from 'fs'; import path from 'path';
const W='/home/claude/8bitworkshop/8bitworkshop/src/worker/wasm/';
const share=new WASIMemoryFilesystem();
function walk(d,rel){for(const f of fs.readdirSync(d)){const p=d+'/'+f,r=rel?rel+'/'+f:f;if(fs.statSync(p).isDirectory()){share.putDirectory(r);walk(p,r)}else share.putFile('./'+r,new Uint8Array(fs.readFileSync(p)))}}
walk('zip','');
function run(tool,args,inputs){const w=new WASIRunner();w.fs.setParent(share);w.initSync(new WebAssembly.Module(fs.readFileSync(W+tool+'.wasm')));
 for(const [k,v] of Object.entries(inputs||{}))w.fs.putFile('./'+k,v);w.addPreopenDirectory('.');w.setArgs([tool,...args]);const e=w.run();
 console.log(tool,'exit',e,w.fds[2].getBytesAsString().slice(0,400));return w}
const src=`#include <stdio.h>
#include <peekpoke.h>
int main(void){ int i; printf("HELLO FROM C\\n"); for(i=0;i<3;i++) POKE(53280,i+2); return 0; }`;
let w=run('cc65',['-t','c64','-I','share/cc65/include','-I','.','-Oirs','main.c','-o','main.s'],{'main.c':src});
const s=w.fs.getFile('main.s').getBytes();
w=run('ca65',['-t','c64','-I','share/cc65/asminc','-o','main.o','main.s'],{'main.s':s});
const o=w.fs.getFile('main.o').getBytes();
w=run('ld65',['-t','c64','--cfg-path','share/cc65/cfg','--lib-path','share/cc65/lib','-o','main','main.o','c64.lib'],{'main.o':o});
const prg=w.fs.getFile('main').getBytes();console.log('prg',prg.length,prg[0],prg[1],Array.from(prg.slice(2,12)));
fs.writeFileSync('/tmp/hello.prg',prg);
