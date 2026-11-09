var JadeKit=(()=>{var it=Object.defineProperty;var Qt=Object.getOwnPropertyDescriptor;var Yt=Object.getOwnPropertyNames;var Vt=Object.prototype.hasOwnProperty;var Xt=(g,e)=>{for(var t in e)it(g,t,{get:e[t],enumerable:!0})},Zt=(g,e,t,n)=>{if(e&&typeof e=="object"||typeof e=="function")for(let i of Yt(e))!Vt.call(g,i)&&i!==t&&it(g,i,{get:()=>e[i],enumerable:!(n=Qt(e,i))||n.enumerable});return g};var es=g=>Zt(it({},"__esModule",{value:!0}),g);var hs={};Xt(hs,{Agent:()=>We,BM25:()=>ae,BusyBox:()=>Oe,Cron:()=>ne,DEFAULT_TOOLS:()=>vt,Database:()=>Me,Decisions:()=>Ce,JsRunner:()=>Te,ML:()=>Ie,OLLAMA_CLOUD:()=>xe,OLLAMA_LOCAL:()=>Se,OLLAYA_LOCAL:()=>yt,Ollama:()=>he,OllamaCloud:()=>et,Python:()=>Le,Scheduler:()=>Pe,ShellSession:()=>Ae,Sqlite:()=>De,Tasks:()=>Ue,VERSION:()=>Ht,VFS:()=>qe,VectorStore:()=>Be,Webxdc:()=>Re,bm25Search:()=>wt,createKit:()=>us,createTools:()=>St,getAssetsBase:()=>At,gpuShim:()=>_t,searchFiles:()=>Ne,setAssetsBase:()=>ct,tokenize:()=>Fe});var ue=new TextEncoder,K=new TextDecoder,Ge=g=>new Promise(e=>setTimeout(e,g));function le(g){let e="";for(let t=0;t<g.length;t+=32768)e+=String.fromCharCode.apply(null,g.subarray(t,t+32768));return btoa(e)}var ot=g=>g instanceof Uint8Array?g:typeof g=="string"?ue.encode(g):g instanceof ArrayBuffer?new Uint8Array(g):ArrayBuffer.isView(g)?new Uint8Array(g.buffer,g.byteOffset,g.byteLength):ue.encode(String(g??"")),at=(g,e)=>{if(g===e)return!0;if(!g||!e||g.length!==e.length)return!1;for(let t=0;t<g.length;t++)if(g[t]!==e[t])return!1;return!0},_e=g=>!!g&&g.length>=16&&String.fromCharCode(...g.subarray(0,15))==="SQLite format 3",Ot=g=>!!g&&g.length>=8&&g[0]===0&&g[1]===97&&g[2]===115&&g[3]===109,lt=new URL("../assets/","https://kit.local/dist/jade-agent-kit.js").href,je=g=>new URL(g,lt).href,ct=g=>{g&&(lt=new URL(g.endsWith("/")?g:g+"/",location.href).href)},At=()=>lt;async function ie(g,e=g){let t;try{t=await fetch(g)}catch(n){throw new Error(`could not download ${e} (${n.message||n})`)}if(!t.ok)throw new Error(`could not download ${e}: HTTP ${t.status}`);return new Uint8Array(await t.arrayBuffer())}async function ye(g,e=g){return K.decode(await ie(g,e))}var Ke=new Map;function Qe(g,e){return e&&globalThis[e]?Promise.resolve(globalThis[e]):(Ke.has(g)||Ke.set(g,new Promise((t,n)=>{let i=document.createElement("script");i.src=g,i.async=!0,i.crossOrigin="anonymous",i.onload=()=>t(e?globalThis[e]:!0),i.onerror=()=>{Ke.delete(g),n(new Error(`could not load ${g}`))},document.head.appendChild(i)})),Ke.get(g))}function Ye(g,e="kv"){let t=null,n=()=>t??(t=new Promise((h,o)=>{let l=indexedDB.open(g,1);l.onupgradeneeded=()=>l.result.createObjectStore(e),l.onsuccess=()=>h(l.result),l.onerror=()=>{t=null,o(l.error)}})),i=async(h,o)=>{let l=await n();return new Promise((p,S)=>{let x=l.transaction(e,h),k=o(x.objectStore(e));x.oncomplete=()=>p(k?.result),x.onerror=()=>S(x.error),x.onabort=()=>S(x.error)})};return{get:h=>i("readonly",o=>o.get(h)),set:(h,o)=>i("readwrite",l=>l.put(o,h)),del:h=>i("readwrite",o=>o.delete(h)),keys:()=>i("readonly",h=>h.getAllKeys()),close:async()=>{t&&(await t).close(),t=null}}}function Ve(g,e,{timeoutMs:t=6e4,transfer:n=[],onMessage:i=null,signal:h=null,name:o="worker"}={}){let l=URL.createObjectURL(new Blob([g],{type:"text/javascript"}));return new Promise(p=>{let S;try{S=new Worker(l,{name:o})}catch(y){URL.revokeObjectURL(l),p({error:`could not start a ${o} worker (${y.message})`});return}let x=!1,k=y=>{x||(x=!0,clearTimeout(j),h?.removeEventListener?.("abort",q),S.terminate(),URL.revokeObjectURL(l),p(y))},j=setTimeout(()=>k({timeout:!0,error:`${o}: stopped after ${t/1e3}s timeout`}),t),q=()=>k({aborted:!0,error:`${o}: stopped`});h?.addEventListener?.("abort",q),S.onmessage=async y=>{i&&await i(y.data,S)||k(y.data)},S.onerror=y=>{y.preventDefault?.(),k({error:`${y.message||o+" error"}${y.lineno?` (line ${y.lineno})`:""}`,lineno:y.lineno})},S.postMessage(e,n)})}var qe=class{constructor({persist:e=!1}={}){this.nodes=new Map([["/",{dir:!0,mtime:Date.now()}]]),this.listeners=new Set,this.store=e?Ye("jade-agent-kit:"+e):null,this._t=null,this._saving=null}async load(){if(!this.store)return!1;let e=await this.store.get("vfs");return Array.isArray(e)&&e.length?(this.nodes=new Map(e),this.nodes.has("/")||this.nodes.set("/",{dir:!0,mtime:Date.now()}),!0):!1}async flush(){clearTimeout(this._t),this._t=null,this.store&&await(this._saving=this.store.set("vfs",[...this.nodes.entries()]))}on(e){return this.listeners.add(e),()=>this.listeners.delete(e)}changed(e){for(let t of this.listeners)try{t(e)}catch{}this.store&&(clearTimeout(this._t),this._t=setTimeout(()=>this.flush().catch(()=>{}),150))}norm(e,t="/"){(e==null||e==="")&&(e="."),e=String(e),e==="~"?e="/":e.startsWith("~/")&&(e="/"+e.slice(2));let n=[];for(let i of(e.startsWith("/")?e:t+"/"+e).split("/"))!i||i==="."||(i===".."?n.pop():n.push(i));return"/"+n.join("/")}parent(e){if(e==="/")return"/";let t=e.lastIndexOf("/");return t<=0?"/":e.slice(0,t)}base(e){return e==="/"?"/":e.slice(e.lastIndexOf("/")+1)}exists(e){return this.nodes.has(this.norm(e))}isDir(e){return this.nodes.get(this.norm(e))?.dir===!0}isFile(e){let t=this.nodes.get(this.norm(e));return!!t&&!t.dir}stat(e){e=this.norm(e);let t=this.nodes.get(e);if(!t)throw new Error(`${e}: No such file or directory`);return{dir:!!t.dir,size:t.dir?4096:t.data.length,mtime:t.mtime}}mkdirp(e){if(e=this.norm(e),e!=="/"){if(this.isFile(e))throw new Error(`${e}: Not a directory`);this.isDir(e)||(this.mkdirp(this.parent(e)),this.nodes.set(e,{dir:!0,mtime:Date.now()}),this.changed(e))}}mkdir(e){if(e=this.norm(e),this.exists(e))throw new Error(`${e}: File exists`);if(!this.isDir(this.parent(e)))throw new Error(`${this.parent(e)}: No such file or directory`);this.nodes.set(e,{dir:!0,mtime:Date.now()}),this.changed(e)}readBytes(e){e=this.norm(e);let t=this.nodes.get(e);if(!t)throw new Error(`${e}: No such file or directory`);if(t.dir)throw new Error(`${e}: Is a directory`);return t.data}read(e){return K.decode(this.readBytes(e))}write(e,t,{mkdirs:n=!0}={}){if(e=this.norm(e),e==="/")throw new Error("/: Is a directory");let i=this.parent(e);if(n)this.mkdirp(i);else if(!this.isDir(i))throw new Error(`${i}: No such file or directory`);if(this.isDir(e))throw new Error(`${e}: Is a directory`);this.nodes.set(e,{data:ot(t),mtime:Date.now()}),this.changed(e)}append(e,t){e=this.norm(e);let n=this.isFile(e)?this.readBytes(e):new Uint8Array,i=ot(t),h=new Uint8Array(n.length+i.length);h.set(n),h.set(i,n.length),this.write(e,h)}touch(e){e=this.norm(e);let t=this.nodes.get(e);t?(t.mtime=Date.now(),this.changed(e)):this.write(e,"")}list(e="/"){if(e=this.norm(e),!this.exists(e))throw new Error(`${e}: No such file or directory`);if(!this.isDir(e))throw new Error(`${e}: Not a directory`);let t=e==="/"?"/":e+"/",n=[];for(let i of this.nodes.keys())i!==e&&i.startsWith(t)&&!i.slice(t.length).includes("/")&&n.push(i.slice(t.length));return n.sort()}*walk(e="/"){e=this.norm(e);let t=e==="/"?"/":e+"/";for(let n of[...this.nodes.keys()].sort())(n===e||n.startsWith(t))&&(yield n)}rm(e,t=!1){if(e=this.norm(e),e==="/")throw new Error("refusing to remove '/'");if(!this.exists(e))throw new Error(`${e}: No such file or directory`);if(this.isDir(e)){if(this.list(e).length&&!t)throw new Error(`${e}: Directory not empty`);for(let n of[...this.nodes.keys()])n.startsWith(e+"/")&&this.nodes.delete(n)}this.nodes.delete(e),this.changed(e)}move(e,t){if(e=this.norm(e),t=this.norm(t),!this.exists(e))throw new Error(`${e}: No such file or directory`);if(this.isDir(t)&&(t=(t==="/"?"":t)+"/"+this.base(e)),t===e)return;if(t.startsWith(e+"/"))throw new Error(`cannot move '${e}' into itself`);if(!this.isDir(this.parent(t)))throw new Error(`${this.parent(t)}: No such file or directory`);let n=[...this.nodes.entries()].filter(([i])=>i===e||i.startsWith(e+"/"));for(let[i]of n)this.nodes.delete(i);for(let[i,h]of n)this.nodes.set(t+i.slice(e.length),h);this.changed(t)}copy(e,t,n=!1){if(e=this.norm(e),t=this.norm(t),!this.exists(e))throw new Error(`${e}: No such file or directory`);if(this.isDir(t)&&(t=(t==="/"?"":t)+"/"+this.base(e)),this.isDir(e)){if(!n)throw new Error(`-r not specified; omitting directory '${e}'`);for(let i of[...this.walk(e)]){let h=this.nodes.get(i),o=t+i.slice(e.length);h.dir?this.mkdirp(o):this.write(o,h.data.slice())}}else this.write(t,this.readBytes(e).slice())}entries(){return[...this.nodes.entries()]}replace(e){this.nodes=new Map(e),this.nodes.has("/")||this.nodes.set("/",{dir:!0,mtime:Date.now()}),this.changed("/")}snapshot(){let e={};for(let[t,n]of this.nodes)n.dir||(e[t]=n.data);return e}import(e,t="/"){for(let[n,i]of Object.entries(e))this.write(this.norm(n,t),i)}applyChanges({writes:e={},deletes:t=[],mkdirs:n=[],rmdirs:i=[]},h){for(let o of t)this.isFile(o)&&this.rm(o);for(let o of i)o!=="/"&&this.isDir(o)&&this.rm(o,!0);for(let o of n)try{this.mkdirp(o)}catch(l){h?.(l)}for(let[o,l]of Object.entries(e))try{l===null?this.isFile(o)&&this.rm(o):this.write(o,l)}catch(p){h?.(new Error(`could not save ${o}: ${p.message}`))}}};var dt=`
async function __bbExec(BusyBoxModule, MOD, d) {
  const { args, stdin, entries, cwd } = d;
  const SYS = new Set(['/dev', '/proc']);
  const inp = new TextEncoder().encode(stdin || ''); let ip = 0; const out = [], err = [];
  const M = await BusyBoxModule({
    noInitialRun: true, thisProgram: 'busybox',
    instantiateWasm(imports, cb) { WebAssembly.instantiate(MOD, imports).then(i => cb(i, MOD)); return {}; },
    stdin: () => ip < inp.length ? inp[ip++] : null,
    stdout: c => { if (c != null) out.push(c); }, stderr: c => { if (c != null) err.push(c); },
    print: () => {}, printErr: () => {},
  });
  const FS = M.FS; const defaults = new Set();
  // stdio is already open, so Emscripten's /dev, /proc and /home can go: they would leak into
  // the agent's filesystem and make grep -r / find hang on /dev/urandom
  const nuke = (q) => { let st; try { st = FS.lstat(q); } catch { return; } if (FS.isDir(st.mode)) { let kids = []; try { kids = FS.readdir(q); } catch {} for (const n of kids) if (n !== '.' && n !== '..') nuke(q + '/' + n); try { FS.rmdir(q); } catch {} } else { try { FS.unlink(q); } catch {} } };
  if (!entries.some(([p]) => p === '/home' || p.startsWith('/home/'))) nuke('/home');
  for (const q of ['/proc/self/fd', '/proc/self', '/proc']) { try { FS.rmdir(q); } catch {} }
  nuke('/dev');
  if (!entries.some(([p]) => p === '/tmp' || p.startsWith('/tmp/'))) { try { FS.rmdir('/tmp'); } catch {} }
  const scan = (dir) => { for (const n of FS.readdir(dir)) { if (n === '.' || n === '..') continue; const q = (dir === '/' ? '' : dir) + '/' + n; if (SYS.has(q)) continue; defaults.add(q); if (FS.isDir(FS.stat(q).mode)) scan(q); } };
  scan('/');
  const orig = new Set();
  for (const [p, n] of entries) { if (p === '/') continue; orig.add(p); if (n.dir) { try { FS.mkdirTree(p); } catch {} } else { try { FS.mkdirTree(p.slice(0, p.lastIndexOf('/')) || '/'); } catch {} FS.writeFile(p, n.data); } }
  try { FS.mkdirTree(cwd); } catch {} FS.chdir(cwd);
  let code = 0;
  try { code = M.callMain(args) ?? 0; } catch (x) { code = typeof x?.status === 'number' ? x.status : 134; if (typeof x?.status !== 'number') err.push(...new TextEncoder().encode(String(x?.message || x) + '\\n')); }
  const res = [['/', { dir: true }]];
  const walk = (dir) => { for (const n of FS.readdir(dir)) { if (n === '.' || n === '..') continue; const q = (dir === '/' ? '' : dir) + '/' + n; if (SYS.has(q)) continue; let st; try { st = FS.lstat(q); } catch { continue; } if (FS.isDir(st.mode)) { res.push([q, { dir: true }]); walk(q); } else if (FS.isFile(st.mode)) res.push([q, { data: FS.readFile(q) }]); } };
  walk('/');
  // drop Emscripten's own empty default dirs unless the VFS had them or something was written inside
  const keep = res.filter(([p, n]) => !(n.dir && defaults.has(p) && !orig.has(p) && !res.some(([q]) => q.startsWith(p + '/') && !(defaults.has(q) && !orig.has(q)))));
  return { ok: true, out: new Uint8Array(out), err: new Uint8Array(err), code, entries: keep };
}`,Tt=`
let __MOD = null;
self.onmessage = async (e) => {
  const d = e.data;
  if (d.type === 'init') {
    try { __MOD = await WebAssembly.compile(d.wasm); self.postMessage({ type: 'ready' }); }
    catch (x) { self.postMessage({ type: 'fail', error: 'WebAssembly compile in worker: ' + (x?.message || x) }); }
    return;
  }
  try { const r = await __bbExec(BusyBoxModule, __MOD, d); r.id = d.id; self.postMessage(r); }
  catch (x) { self.postMessage({ id: d.id, ok: false, error: String(x?.message || x) }); }
};`;var Lt=16e6,Oe=class{constructor(e){this.vfs=e,this.module=null,this.wasm=null,this.glue="",this.applets=new Set,this.host="",this.worker=null,this.seq=0,this.pending=new Map,this.mainFns=null,this._p=null,this.error=""}load(){return this._p||(this._p=(async()=>{try{let[n,i]=await Promise.all([ie(je("busybox.wasm"),"BusyBox"),ye(je("busybox.glue.js"),"BusyBox glue")]);this.wasm=n,this.glue=i,this.module=await WebAssembly.compile(n)}catch(n){return this.module=null,this.error=n.message,!1}let e=[],t=async()=>{let n=await this.run(["--list"],"",2e4);if(!n.ok)throw new Error(n.error);if(this.applets=new Set(K.decode(n.out).split(/\s+/).filter(Boolean)),!this.applets.size)throw new Error("busybox --list returned nothing")};try{return this.host="worker",await t(),!0}catch(n){e.push("worker: "+n.message)}try{return this.mainFns=this._mainHost(),this.host="main",await t(),!0}catch(n){return e.push("main thread: "+n.message),this.module=null,this.host="",this.error="BusyBox could not start ("+e.join("; ")+")",!1}})())}get ready(){return!!this.module&&this.applets.size>0}_classicGlue(){return this.glue.replace(/export\s+default\s+BusyBoxModule\s*;?\s*$/,"").replace(/import\.meta\.url/g,'"about:blank"')}_mainHost(){return new Function(this._classicGlue()+`
`+dt+`
return { BusyBoxModule, __bbExec };`)()}_spawn(){let e=URL.createObjectURL(new Blob([this._classicGlue()+`
`+dt+`
`+Tt],{type:"text/javascript"})),t,n=new Promise((i,h)=>{try{t=new Worker(e,{name:"busybox"})}catch(l){return h(new Error(`new Worker() refused: ${l.message}`))}let o=setTimeout(()=>h(new Error("worker did not answer within 10s")),1e4);t.onmessage=l=>{l.data.type==="ready"?(clearTimeout(o),t.onmessage=p=>{let S=this.pending.get(p.data.id);S&&(this.pending.delete(p.data.id),S(p.data))},i()):l.data.type==="fail"&&(clearTimeout(o),h(new Error(l.data.error)))},t.onerror=l=>{clearTimeout(o),l.preventDefault?.(),h(new Error(l.message||"worker script was blocked or failed to load"))},t.postMessage({type:"init",wasm:this.wasm})});this.worker={w:()=>t,ready:n,url:e}}_entries(){let e=[];for(let[t,n]of this.vfs.nodes)n.dir?e.push([t,{dir:!0}]):n.data.length<=Lt&&e.push([t,{data:n.data}]);return e}async run(e,t="",n=3e4,i="/"){if(this.host==="main")try{return await Promise.race([this.mainFns.__bbExec(this.mainFns.BusyBoxModule,this.module,{args:e,stdin:t,entries:this._entries(),cwd:i}),Ge(n).then(()=>({ok:!1,timeout:!0,error:`timed out after ${n/1e3}s`}))])}catch(l){return{ok:!1,error:String(l?.message||l)}}this.worker||this._spawn();try{await this.worker.ready}catch(l){return this.worker=null,{ok:!1,error:l.message}}let h=++this.seq,o=this.worker.w();return new Promise(l=>{let p=setTimeout(()=>{this.pending.delete(h),o.terminate(),this.worker?.w()===o&&(this.worker=null);for(let[,S]of this.pending)S({ok:!1,error:"worker restarted"});this.pending.clear(),l({ok:!1,timeout:!0,error:`timed out after ${n/1e3}s`})},n);this.pending.set(h,S=>{clearTimeout(p),l(S)}),o.postMessage({id:h,args:e,stdin:t,entries:this._entries(),cwd:i})})}async exec(e,t=[],{stdin:n="",cwd:i="/",timeoutMs:h=3e4}={}){if(!this.ready&&!await this.load())return{stdout:"",stderr:`busybox: ${this.error}
`,code:127};let o=new Map(this.vfs.nodes),l=await this.run([e,...t],n,h,i);return l.ok?(this._apply(l.entries,o),{stdout:K.decode(l.out),stderr:K.decode(l.err),code:l.code}):{stdout:"",stderr:`busybox ${e}: ${l.error}
`,code:l.timeout?124:126}}_apply(e,t){let n=this.vfs,i=new Set;for(let[h,o]of e){if(i.add(h),h==="/")continue;let l=t.get(h),p=n.nodes.get(h);if(o.dir){p||n.mkdirp(h);continue}l&&!l.dir&&at(l.data,o.data)||p&&!p.dir&&at(p.data,o.data)||n.write(h,o.data)}for(let[h,o]of t)h==="/"||i.has(h)||n.nodes.get(h)!==o||!o.dir&&o.data.length>Lt||n.exists(h)&&n.rm(h,!0)}close(){try{this.worker?.w()?.terminate()}catch{}this.worker?.url&&URL.revokeObjectURL(this.worker.url),this.worker=null}};function Mt(g){let e=g.vfs,t=g.busybox;g.engine||(g.engine="auto"),g.commands||(g.commands={});function n(s){let r=[],a=0,f=null,m=(c,u)=>{f??(f=[]);let _=f[f.length-1];_&&_.t==="lit"&&_.q===u?_.v+=c:f.push({t:"lit",v:c,q:u})},w=()=>{f&&(r.push({t:"w",segs:f}),f=null)},d=c=>{let u=s[a+1];if(f??(f=[]),u==="("){let b=0,v=a+1;for(;v<s.length;v++)if(s[v]==="(")b++;else if(s[v]===")"&&(b--,!b))break;if(v>=s.length)throw new Error("unterminated $(");f.push({t:"sub",v:s.slice(a+2,v),q:c}),a=v+1;return}if(u==="{"){let b=s.indexOf("}",a);if(b<0)throw new Error("bad substitution");f.push({t:"var",v:s.slice(a+2,b),q:c}),a=b+1;return}let _=/^([A-Za-z_]\w*|[?$#0-9])/.exec(s.slice(a+1));if(_){f.push({t:"var",v:_[1],q:c}),a+=1+_[1].length;return}m("$",c),a++};for(;a<s.length;){let c=s[a];if(c==="\\"){if(s[a+1]===`
`){a+=2;continue}m(s[a+1]??"",!0),a+=2;continue}if(c==="'"){let _=s.indexOf("'",a+1);if(_<0)throw new Error("unterminated quote");f??(f=[]),m(s.slice(a+1,_),!0),a=_+1;continue}if(c==='"'){for(a++,f??(f=[]),m("",!0);a<s.length&&s[a]!=='"';)s[a]==="\\"&&'"\\$`'.includes(s[a+1])?(m(s[a+1],!0),a+=2):s[a]==="$"?d(!0):(m(s[a],!0),a++);if(s[a]!=='"')throw new Error("unterminated quote");a++;continue}if(c==="$"){d(!1);continue}if(c===" "||c==="	"||c==="\r"){w(),a++;continue}if(c===`
`){w(),r.push({t:"op",v:";"}),a++;continue}if(c==="#"&&!f){for(;a<s.length&&s[a]!==`
`;)a++;continue}let u=/^(2>&1|&>|2>>|2>|>>|>&2|1>|>|<|&&|\|\||\||;|&)/.exec(s.slice(a));if(u&&!(f&&u[1].startsWith("2"))){w(),r.push({t:"op",v:u[1]}),a+=u[1].length;continue}m(c,!1),a++}return w(),r}function i(s){let r=[],a=[],f={words:[],redirs:[]},m=()=>{(f.words.length||f.redirs.length)&&a.push(f),f={words:[],redirs:[]}},w=d=>{if(m(),a.length)r.push({pipeline:a,op:d});else if(d==="&&"||d==="||")throw new Error(`syntax error near '${d}'`);a=[]};for(let d=0;d<s.length;d++){let c=s[d];if(c.t==="w"){f.words.push(c.segs);continue}switch(c.v){case"|":m();break;case"&&":case"||":case";":case"&":w(c.v==="&"?";":c.v);break;case"2>&1":case">&2":f.redirs.push({op:c.v});break;default:{let u=s[++d];if(!u||u.t!=="w")throw new Error(`syntax error near '${c.v}'`);f.redirs.push({op:c.v==="1>"?">":c.v,target:u.segs})}}}return w(";"),r}let h="";function o(s,{anchored:r=!0}={}){let a="";for(let f=0;f<s.length;f++){let m=s[f];if(m===h){a+=s[++f].replace(/[.*+?^${}()|[\]\\/]/g,"\\$&");continue}if(m==="*")a+="[^/]*";else if(m==="?")a+="[^/]";else if(m==="["){let w=s.indexOf("]",f+1);if(w>f){let d=s.slice(f+1,w);d[0]==="!"&&(d="^"+d.slice(1)),a+="["+d.replace(/\\/g,"\\\\")+"]",f=w}else a+="\\["}else a+=m.replace(/[.+^${}()|\\/\]]/g,"\\$&")}return new RegExp(r?"^"+a+"$":a)}class l{constructor({cwd:r="/",env:a={},onOutput:f=null}={}){this.cwd=r,this.env={HOME:"/",USER:"agent",SHELL:"/bin/sh",PATH:"/bin",...a},this.lastCode=0,this.onOutput=f,this.aborted=!1,this.timeoutMs=6e4}getVar(r){return r==="?"?String(this.lastCode):r==="$"?"1337":r==="#"?"0":r==="0"?"sh":r==="PWD"?this.cwd:this.env[r]??""}async expandWord(r){let a="",f=!1,m=w=>w.replace(/[*?[\]]/g,d=>h+d);for(let w of r)if(w.t==="lit")w.q?a+=m(w.v):(a+=w.v,/[*?[]/.test(w.v)&&(f=!0));else if(w.t==="var")a+=m(this.getVar(w.v));else if(w.t==="sub"){let d=await this.capture(w.v);a+=m(d.replace(/\n+$/,""))}if(f){let w=this.glob(a);if(w.length)return w}return[a.replaceAll(h,"")]}glob(r){let a=r.startsWith("/"),f=e.norm(r.replaceAll(h,""),this.cwd).replaceAll("",h),m=o(f),w=/(^|\/)\./.test(r.replaceAll(h,"")),d=[];for(let u of e.nodes.keys())u==="/"||!m.test(u)||!w&&/\/\.[^/]*$/.test(u)||d.push(u);if(d.sort(),a)return d;let c=this.cwd==="/"?"/":this.cwd+"/";return d.map(u=>u.startsWith(c)?u.slice(c.length):u)}async capture(r){let a=new l({cwd:this.cwd,env:{...this.env}});return a.aborted=this.aborted,a.timeoutMs=this.timeoutMs,(await a.run(r)).chunks.filter(m=>!m.err).map(m=>m.s).join("")}async run(r,{stdin:a=""}={}){let f=[],m=(c,u=!1)=>{c&&(f.push({s:c,err:u}),this.onOutput?.(c,u))},w;try{w=i(n(r))}catch(c){return m(`sh: ${c.message}
`,!0),this.lastCode=2,{chunks:f,code:2}}let d=";";for(let c of w){if(this.aborted){m(`^C
`,!0),this.lastCode=130;break}if(d==="&&"&&this.lastCode!==0||d==="||"&&this.lastCode===0){d=c.op;continue}try{this.lastCode=await this.runPipeline(c.pipeline,a,m)}catch(u){if(u&&u.__exit!==void 0){this.lastCode=u.__exit;break}m(`sh: ${u.message}
`,!0),this.lastCode=1}d=c.op}return{chunks:f,code:this.lastCode}}async runPipeline(r,a,f){let m=a,w=0;for(let d=0;d<r.length;d++){let c=r[d],u=d===r.length-1,_=[];for(let P of c.words)_.push(...await this.expandWord(P));let b=m,v=null,O=null,B=!1,L=!1;for(let P of c.redirs){if(P.op==="2>&1"){B=!0;continue}if(P.op===">&2"){L=!0;continue}let z=(await this.expandWord(P.target))[0],Y=z==="/dev/null"?null:e.norm(z,this.cwd);P.op==="<"?z==="/dev/null"?b="":b=e.read(Y):P.op===">"||P.op===">>"?v={p:Y,append:P.op===">>",dn:z==="/dev/null"}:P.op==="2>"||P.op==="2>>"?O={p:Y,append:P.op==="2>>",dn:z==="/dev/null"}:P.op==="&>"&&(v={p:Y,append:!1,dn:z==="/dev/null"},B=!0)}v&&!v.dn&&(v.append?e.exists(v.p)||e.write(v.p,"",{mkdirs:!1}):e.write(v.p,"",{mkdirs:!1}));let D=await this.exec(_,b??""),N=D.out||"",U=D.err||"";B&&(N+=U,U=""),L&&(U+=N,N=""),O&&(O.dn||(O.append?e.append(O.p,U):e.write(O.p,U,{mkdirs:!1})),U=""),v&&(v.dn||e.append(v.p,N),N=""),U&&f(U,!0),u?f(N):m=N,w=D.code}return w}async exec(r,a){for(;r.length&&/^[A-Za-z_]\w*=/.test(r[0]);){let c=r.shift(),u=c.indexOf("=");this.env[c.slice(0,u)]=c.slice(u+1)}if(!r.length)return{out:"",err:"",code:0};let[f,...m]=r;f==="busybox"&&m.length&&!m[0].startsWith("-")&&(f=m.shift());let w={argv:m,stdin:a,sh:this,outS:"",errS:"",o(c){this.outS+=c},e(c){this.errS+=c},P:c=>e.norm(c,this.cwd),name:f},d=c=>({out:w.outS,err:w.errS,code:c??0});try{if(T[f])return d(await T[f](w));if(g.commands[f])return d(await g.commands[f](w));let c=g.engine;if(t.ready&&t.applets.has(f)&&c!=="js"&&!A.has(f)&&!g.commands[f]){let _=await this.execWasm(f,m,a);return _.code!==0&&c==="auto"&&E[f]&&/unrecognized|invalid option|unknown option|not implemented/i.test(_.err)?d(await E[f](w)):_}return c==="wasm"&&!A.has(f)?t.ready?{out:"",err:`sh: ${f}: applet not found in this BusyBox build
`,code:127}:{out:"",err:`sh: ${f}: BusyBox is not loaded${t.error?" ("+t.error+")":""}
`,code:127}:g.commands[f]?d(await g.commands[f](w)):E[f]?d(await E[f](w)):t.ready&&t.applets.has(f)?await this.execWasm(f,m,a):e.isFile(e.norm(f,this.cwd))&&/\.(sh)$/.test(f)?d(await T.sh({...w,argv:[f,...m]})):{out:"",err:`sh: ${f}: not found
`,code:127}}catch(c){if(c&&c.__exit!==void 0)throw c;return{out:w.outS,err:w.errS+`${f}: ${c.message}
`,code:1}}}async execWasm(r,a,f){let m=await t.exec(r,a,{stdin:f,cwd:this.cwd,timeoutMs:this.timeoutMs});return{out:m.stdout,err:m.stderr,code:m.code}}}function p(s,r=""){let a=new Set([...r.matchAll(/(\w):/g)].map(w=>w[1])),f={},m=[];for(let w=0;w<s.length;w++){let d=s[w];if(d==="--"){m.push(...s.slice(w+1));break}if(/^-\d+$/.test(d)&&a.has("n")){f.n=d.slice(1);continue}if(d.startsWith("--")&&d.length>2){let[c,u]=d.slice(2).split("=");f[c]=u??!0;continue}if(d.startsWith("-")&&d.length>1){for(let c=1;c<d.length;c++){let u=d[c];if(a.has(u)){f[u]=d.slice(c+1)||s[++w];break}f[u]=!0}continue}m.push(d)}return{f,rest:m}}function S(s,r){return r.length?r.map(a=>{if(a==="-")return{name:"-",text:s.stdin};try{return{name:a,text:e.read(s.P(a))}}catch(f){return s.e(`${s.name}: ${f.message}
`),null}}).filter(Boolean):[{name:"-",text:s.stdin}]}let x=s=>{if(!s)return[];let r=s.split(`
`);return r[r.length-1]===""&&r.pop(),r};function k(s){let r="";for(let a=0;a<s.length;a++){let f=s[a];if(f==="\\"&&a+1<s.length){let m=s[++a];"(){}|+?".includes(m)?r+=m:r+="\\"+m}else"(){}|+?".includes(f)?r+="\\"+f:r+=f}return r}let j=s=>s<1024?s+"":s<1048576?(s/1024).toFixed(1)+"K":(s/1048576).toFixed(1)+"M",q="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" "),y=s=>{let r=new Date(s);return`${q[r.getMonth()]} ${String(r.getDate()).padStart(2)} ${String(r.getHours()).padStart(2,"0")}:${String(r.getMinutes()).padStart(2,"0")}`},A=new Set(["node","js","python","python3","sqlite3","help","sh","bash","xargs"]),T={cd(s){let r=s.P(s.argv[0]??"/");return e.isDir(r)?(s.sh.cwd=r,0):(s.e(`cd: ${s.argv[0]}: No such directory
`),1)},pwd(s){return s.o(s.sh.cwd+`
`),0},export(s){for(let r of s.argv){let a=r.indexOf("=");a>0&&(s.sh.env[r.slice(0,a)]=r.slice(a+1))}return 0},unset(s){for(let r of s.argv)delete s.sh.env[r];return 0},exit(s){throw{__exit:parseInt(s.argv[0]??"0")||0}},true:()=>0,false:()=>1,":":()=>0,async sh(s){let{f:r,rest:a}=p(s.argv,"c:"),f=new l({cwd:s.sh.cwd,env:{...s.sh.env}});f.timeoutMs=s.sh.timeoutMs;let m=r.c;m==null&&(a.length?m=e.read(s.P(a[0])):m=s.stdin);let w=await f.run(m);for(let d of w.chunks)d.err?s.e(d.s):s.o(d.s);return w.code},get bash(){return this.sh},source(s){return T.sh(s)},which(s){let r=0;for(let a of s.argv)T[a]||E[a]||g.commands[a]||t.applets.has(a)?s.o(`/bin/${a}
`):r=1;return r},type(s){for(let r of s.argv)s.o(T[r]?`${r} is a shell builtin
`:t.applets.has(r)&&g.engine!=="js"?`${r} is /bin/${r} (busybox.wasm)
`:E[r]?`${r} is /bin/${r} (js applet)
`:`${r}: not found
`);return 0},help(s){let r=new Set([...Object.keys(T),...Object.keys(E),...Object.keys(g.commands),...t.applets]);return s.o(`Jade Agent Kit shell \u2014 ${t.ready?`BusyBox WASM (${t.applets.size} applets) + JS`:"JS applets"}
Supports: pipes |, redirects > >> < 2> 2>&1 &>, && || ;, $VAR, $(cmd), globs * ? [..]
No loops/if blocks: use node or python for scripting. Extra: ${Object.keys(g.commands).sort().join(", ")}, xargs.

`+[...r].sort().join("  ")+`
`),0},async xargs(s){let{f:r,rest:a}=p(s.argv,"n:I:"),f=s.stdin.split(/\s+/).filter(Boolean),m=a.length?a:["echo"],w=async c=>{let u=await s.sh.exec([...c],"");return s.o(u.out),s.e(u.err),u.code},d=0;if(r.I)for(let c of s.stdin.split(`
`).filter(Boolean))d=await w(m.map(u=>u.replaceAll(r.I,c)))||d;else{let c=parseInt(r.n)||f.length||1;for(let u=0;u<Math.max(f.length,1);u+=c)d=await w([...m,...f.slice(u,u+c)])||d}return d}},E={echo(s){let r=s.argv,a=!0,f=!1;for(;r.length&&/^-[neE]+$/.test(r[0]);)r[0].includes("n")&&(a=!1),r[0].includes("e")&&(f=!0),r=r.slice(1);let m=r.join(" ");return f&&(m=m.replace(/\\(n|t|\\|e|r)/g,(w,d)=>({n:`
`,t:"	","\\":"\\",e:"\x1B",r:"\r"})[d])),s.o(m+(a?`
`:"")),0},printf(s){let[r="",...a]=s.argv,f=0,m=r.replace(/\\n/g,`
`).replace(/\\t/g,"	").replace(/%(-?\d*)([sdif%])/g,(w,d,c)=>{if(c==="%")return"%";let u=a[f++]??"";c==="d"||c==="i"?u=String(parseInt(u)||0):c==="f"&&(u=String(parseFloat(u)||0));let _=parseInt(d);return isNaN(_)?u:_<0?u.padEnd(-_):u.padStart(_)});return s.o(m),0},cat(s){let{f:r,rest:a}=p(s.argv),f=1;for(let m of S(s,a))r.n?s.o(x(m.text).map(w=>`${String(f++).padStart(6)}	${w}`).join(`
`)+`
`):s.o(m.text);return s.errS?1:0},ls(s){let{f:r,rest:a}=p(s.argv),f=a.length?a:["."],m=0,w=f.length>1||r.R,d=(u,_)=>{let b=e.stat(u);return r.l?`${b.dir?"drwxr-xr-x":"-rw-r--r--"} 1 agent agent ${(r.h?j(b.size):String(b.size)).padStart(7)} ${y(b.mtime)} ${_}${b.dir&&r.F!==!1?"/":""}`:_+(b.dir?"/":"")},c=(u,_)=>{let b=e.list(u);!r.a&&!r.A&&(b=b.filter(v=>!v.startsWith("."))),r.t&&b.sort((v,O)=>e.stat(e.norm(O,u)).mtime-e.stat(e.norm(v,u)).mtime),r.r&&b.reverse(),w&&s.o(`${_}:
`),r.l&&s.o(`total ${b.length}
`);for(let v of b)s.o(d(e.norm(v,u),v)+`
`);if(r.R)for(let v of b){let O=e.norm(v,u);e.isDir(O)&&(s.o(`
`),c(O,_==="."?"./"+v:_.replace(/\/$/,"")+"/"+v))}};for(let u of f){let _=s.P(u);if(!e.exists(_)){s.e(`ls: ${u}: No such file or directory
`),m=1;continue}e.isDir(_)&&!r.d?c(_,u):s.o(d(_,u)+`
`),w&&!r.R&&s.o(`
`)}return m},mkdir(s){let{f:r,rest:a}=p(s.argv);for(let f of a)r.p?e.mkdirp(s.P(f)):e.mkdir(s.P(f));return 0},rmdir(s){for(let r of s.argv)e.rm(s.P(r),!1);return 0},rm(s){let{f:r,rest:a}=p(s.argv),f=0;for(let m of a){let w=s.P(m);if(!e.exists(w)){r.f||(s.e(`rm: ${m}: No such file or directory
`),f=1);continue}if(e.isDir(w)&&!(r.r||r.R)){s.e(`rm: ${m}: is a directory
`),f=1;continue}e.rm(w,!0)}return f},touch(s){for(let r of p(s.argv).rest){let a=s.P(r);e.isFile(a)?e.touch(a):e.write(a,"",{mkdirs:!1})}return 0},mv(s){let{rest:r}=p(s.argv),a=s.P(r.pop());if(r.length>1&&!e.isDir(a))throw new Error(`target '${a}' is not a directory`);for(let f of r)e.move(s.P(f),a);return 0},cp(s){let{f:r,rest:a}=p(s.argv),f=s.P(a.pop());for(let m of a)e.copy(s.P(m),f,r.r||r.R||r.a);return 0},head(s){let{f:r,rest:a}=p(s.argv,"n:c:");for(let f of S(s,a))if(r.c)s.o(f.text.slice(0,+r.c));else{let m=+(r.n??10),w=x(f.text);s.o((m<0,w.slice(0,m)).map(d=>d+`
`).join(""))}return 0},tail(s){let{f:r,rest:a}=p(s.argv,"n:c:");for(let f of S(s,a))if(r.c)s.o(f.text.slice(-r.c));else{let m=x(f.text),w=String(r.n??10);s.o((w.startsWith("+")?m.slice(+w.slice(1)-1):m.slice(-Math.abs(+w)||m.length)).map(d=>d+`
`).join(""))}return 0},wc(s){let{f:r,rest:a}=p(s.argv),f=!r.l&&!r.w&&!r.c&&!r.m,m=[0,0,0],w=S(s,a),d=(c,u)=>[r.l||f?c[0]:null,r.w||f?c[1]:null,r.c||r.m||f?c[2]:null].filter(_=>_!=null).map(_=>String(_).padStart(7)).join(" ")+(u!=="-"?" "+u:"")+`
`;for(let c of w){let u=[(c.text.match(/\n/g)||[]).length,(c.text.match(/\S+/g)||[]).length,ue.encode(c.text).length];m=m.map((_,b)=>_+u[b]),s.o(d(u,c.name))}return w.length>1&&s.o(d(m,"total")),0},grep(s){let{f:r,rest:a}=p(s.argv,"e:m:A:B:C:"),f=r.e??a.shift();if(f==null)return s.e(`usage: grep [-inrvlcEFwoq] PATTERN [FILE...]
`),2;let m=r.F?f.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"):r.E||r.P?f:k(f);r.w&&(m=`\\b(?:${m})\\b`),r.x&&(m=`^(?:${m})$`);let w=new RegExp(m,r.i?"i":""),d=new RegExp(m,r.i?"gi":"g"),c=a,u=r.r||r.R;u&&!c.length&&(c=["."]);let _=[];for(let L of c){let D=s.P(L);if(e.isDir(D)){if(!u){s.e(`grep: ${L}: Is a directory
`);continue}for(let N of e.walk(D))e.isFile(N)&&!/\/(node_modules|\.git)\//.test(N)&&_.push({name:L==="."?N.slice(s.sh.cwd==="/"?1:s.sh.cwd.length+1):L.replace(/\/$/,"")+N.slice(D.length),p:N})}else _.push({name:L,p:D})}let b=c.length?_.map(L=>{try{return{name:L.name,text:e.read(L.p)}}catch(D){return s.e(`grep: ${D.message}
`),null}}).filter(Boolean):[{name:"-",text:s.stdin}],v=(b.length>1||u)&&!r.h,O=!1,B=r.m?+r.m:1/0;for(let L of b){let D=0,N=x(L.text);for(let U=0;U<N.length&&D<B;U++){if(!(w.test(N[U])!==!!r.v))continue;if(D++,O=!0,r.q)return 0;if(r.l||r.c)continue;let z=(v?L.name+":":"")+(r.n?U+1+":":"");if(r.o)for(let Y of N[U].matchAll(d))s.o(z+Y[0]+`
`);else s.o(z+N[U]+`
`)}r.l&&D&&s.o(L.name+`
`),r.c&&s.o((v?L.name+":":"")+D+`
`)}return O?0:1},find(s){let r=[...s.argv],a=[];for(;r.length&&!r[0].startsWith("-")&&r[0]!=="("&&r[0]!=="!";)a.push(r.shift());a.length||a.push(".");let f=[],m=1/0,w=0,d=!1;for(;r.length;){let c=r.shift();if(c==="!"||c==="-not"){d=!0;continue}let u=_=>{let b=d;f.push(b?(v,O)=>!_(v,O):_),d=!1};if(c==="-name"){let _=o(r.shift());u((b,v)=>_.test(v))}else if(c==="-iname"){let _=new RegExp(o(r.shift()).source,"i");u((b,v)=>_.test(v))}else if(c==="-path"||c==="-wholename"){let _=r.shift(),b=new RegExp(o(_).source.replace(/\[\^\/\]\*/g,".*"));u((v,O,B)=>b.test(B))}else if(c==="-type"){let _=r.shift();u(b=>_==="d"?e.isDir(b):e.isFile(b))}else if(c==="-maxdepth")m=+r.shift();else if(c==="-mindepth")w=+r.shift();else if(c==="-size"){let _=r.shift(),b=/^([+-]?)(\d+)([ckM]?)$/.exec(_),v={c:1,k:1024,M:1048576,"":512}[b[3]],O=+b[2]*v;u(B=>{if(!e.isFile(B))return!1;let L=e.stat(B).size;return b[1]==="+"?L>O:b[1]==="-"?L<O:L===O})}else if(c==="-empty")u(_=>e.isDir(_)?e.list(_).length===0:e.stat(_).size===0);else if(!(c==="-print"||c==="-o"||c==="-a"))return s.e(`find: unsupported option ${c} 
`),1}for(let c of a){let u=s.P(c);if(!e.exists(u)){s.e(`find: ${c}: No such file or directory
`);continue}for(let _ of e.walk(u)){let b=_===u?"":_.slice(u==="/"?1:u.length+1),v=b?b.split("/").length:0;if(v>m||v<w||/\/(node_modules|\.git)(\/|$)/.test(b)&&!c.includes("node_modules"))continue;let O=b?c==="/"?"/"+b:c.replace(/\/$/,"")+"/"+b:c;f.every(B=>B(_,e.base(_),O))&&s.o(O+`
`)}}return 0},tree(s){let{f:r,rest:a}=p(s.argv,"L:"),f=s.P(a[0]||"."),m=0,w=0,d=r.L?+r.L:1/0;s.o((a[0]||".")+`
`);let c=(u,_,b)=>{if(b>d)return;let v=e.list(u).filter(O=>r.a||!O.startsWith("."));v.forEach((O,B)=>{let L=e.norm(O,u),D=B===v.length-1,N=e.isDir(L);N?m++:w++,s.o(_+(D?"\u2514\u2500\u2500 ":"\u251C\u2500\u2500 ")+O+(N?"/":"")+`
`),N&&c(L,_+(D?"    ":"\u2502   "),b+1)})};return c(f,"",1),s.o(`
${m} directories, ${w} files
`),0},sort(s){let{f:r,rest:a}=p(s.argv,"k:t:"),f=S(s,a).flatMap(w=>x(w.text)),m=w=>r.k?(r.t?w.split(r.t):w.trim().split(/\s+/)).slice(parseInt(r.k)-1).join(" "):w;return f.sort((w,d)=>r.n?(parseFloat(m(w))||0)-(parseFloat(m(d))||0):r.f?m(w).toLowerCase().localeCompare(m(d).toLowerCase()):m(w)<m(d)?-1:m(w)>m(d)?1:0),r.r&&f.reverse(),r.u&&(f=f.filter((w,d)=>d===0||w!==f[d-1])),s.o(f.map(w=>w+`
`).join("")),0},uniq(s){let{f:r,rest:a}=p(s.argv),f=S(s,a).flatMap(w=>x(w.text)),m=[];for(let w of f)m.length&&m[m.length-1][0]===w?m[m.length-1][1]++:m.push([w,1]);for(let[w,d]of m)r.d&&d<2||r.u&&d>1||s.o((r.c?String(d).padStart(7)+" ":"")+w+`
`);return 0},cut(s){let{f:r,rest:a}=p(s.argv,"d:f:c:"),f=m=>m.split(",").flatMap(w=>{let[d,c]=w.split("-"),u=d?+d:1,_=w.includes("-")?c?+c:1e9:u,b=[];for(let v=u;v<=Math.min(_,1e3);v++)b.push(v);return b});for(let m of S(s,a).flatMap(w=>x(w.text)))if(r.c){let w=f(r.c);s.o(w.map(d=>m[d-1]??"").join("")+`
`)}else{let w=r.d??"	",d=m.split(w);if(d.length===1&&!m.includes(w)){s.o(m+`
`);continue}s.o(f(r.f||"1").filter(c=>c<=d.length).map(c=>d[c-1]).join(w)+`
`)}return 0},tr(s){let{f:r,rest:a}=p(s.argv),f=c=>{c=c.replace(/\[:upper:\]/g,"A-Z").replace(/\[:lower:\]/g,"a-z").replace(/\[:digit:\]/g,"0-9").replace(/\[:space:\]/g,` 	
`).replace(/\\n/g,`
`).replace(/\\t/g,"	");let u="";for(let _=0;_<c.length;_++)if(c[_+1]==="-"&&c[_+2]){for(let b=c.charCodeAt(_);b<=c.charCodeAt(_+2);b++)u+=String.fromCharCode(b);_+=2}else u+=c[_];return u},m=f(a[0]||""),w=f(a[1]||""),d="";for(let c of s.stdin){let u=m.indexOf(c);r.d?u<0&&(d+=c):u>=0&&w?d+=w[Math.min(u,w.length-1)]:d+=c}return r.s&&(d=d.replace(new RegExp(`([${(w||m).replace(/[\]\\^-]/g,"\\$&")}])\\1+`,"g"),"$1")),s.o(d),0},sed(s){let r=[],a=[],f=!1,m=!1,w=!1,d=s.argv;for(let L=0;L<d.length;L++){let D=d[L];D==="-n"?f=!0:D==="-i"||D.startsWith("-i")?m=!0:D==="-E"||D==="-r"?w=!0:D==="-e"?r.push(d[++L]):D.startsWith("-")&&D.length>1&&/^-[nEr]+$/.test(D)?(D.includes("n")&&(f=!0),/[Er]/.test(D)&&(w=!0)):!r.length&&!a.length&&!d.slice(0,L).includes("-e")?r.push(D):a.push(D)}let c=(L,D="")=>new RegExp(w?L:k(L),D),u=[],_=r.join(`
`),b=0,v=L=>{let D="";for(;b<_.length&&_[b]!==L;){if(_[b]==="\\"&&_[b+1]===L){D+=L,b+=2;continue}if(_[b]==="\\"&&_[b+1]==="n"&&L!=="n"){D+="\\n",b+=2;continue}D+=_[b++]}return b++,D},O=()=>{if(_[b]==="/")return b++,{re:c(v("/"))};if(_[b]==="$")return b++,{last:!0};let L=/^\d+/.exec(_.slice(b));return L?(b+=L[0].length,{n:+L[0]}):null};for(;b<_.length;){for(;/[\s;]/.test(_[b]||"");)b++;if(b>=_.length)break;let L=O(),D=null;for(L&&_[b]===","&&(b++,D=O());_[b]===" ";)b++;let N=!1;_[b]==="!"&&(N=!0,b++);let U=_[b++],P={a1:L,a2:D,bang:N,op:U,on:!1};if(U==="s"){let z=_[b++],Y=v(z),W=v(z),V="";for(;/[gipI0-9]/.test(_[b]||"");)V+=_[b++];P.re=c(Y,(V.includes("g")?"g":"")+(/[iI]/.test(V)?"i":"")),P.rep=W.replace(/\$/g,"$$$$").replace(/\\(\d)/g,"$$$1").replace(/(^|[^\\])&/g,"$1$$&").replace(/\\&/g,"&").replace(/\\n/g,`
`),P.p=V.includes("p")}else if(U==="a"||U==="i"||U==="c"){for(;_[b]===" "||_[b]==="\\";)b++;let z="";for(;b<_.length&&_[b]!==`
`&&_[b]!==";";)z+=_[b++];P.text=z}else if(!"dpq=".includes(U))return s.e(`sed: unsupported command '${U}' (BusyBox WASM sed supports it)
`),1;u.push(P)}let B=L=>{let D=x(L),N="";for(let U=0;U<D.length;U++){let P=D[U],z=!1,Y=!1,W=U===D.length-1,V="",ke="";for(let I of u){let me=Z=>Z&&(Z.n?Z.n===U+1:Z.last?W:Z.re.test(P)),X;if(I.a1?I.a2?!I.on&&me(I.a1)?(I.on=!0,X=!0,I.a2.n&&I.a2.n<=U+1&&(I.on=!1)):I.on?(X=!0,me(I.a2)&&(I.on=!1)):X=!1:X=me(I.a1):X=!0,I.bang&&(X=!X),!!X)if(I.op==="s"){I.re.lastIndex=0;let Z=P.replace(I.re,I.rep);(Z!==P||I.re.test(P))&&(P=Z,I.p&&(N+=P+`
`))}else if(I.op==="d"){z=!0;break}else if(I.op==="p")N+=P+`
`;else if(I.op==="q"){Y=!0;break}else I.op==="="?N+=U+1+`
`:I.op==="a"?ke+=I.text+`
`:I.op==="i"?V+=I.text+`
`:I.op==="c"&&(P=I.text)}if(N+=V,!z&&!f&&(N+=P+`
`),N+=ke,Y)break}return N};if(m){for(let L of a){let D=s.P(L);e.write(D,B(e.read(D)))}return 0}for(let L of S(s,a))s.o(B(L.text));return 0},awk(s){let{f:r,rest:a}=p(s.argv,"F:"),f=a.shift()||"",m=/^\s*(?:\/(.*)\/)?\s*(?:\{\s*print\s*([^}]*)\})?\s*$/.exec(f);if(!m)return s.e(`awk: only "[/re/] { print ... }" is supported by the JS fallback; BusyBox WASM provides full awk
`),2;let w=m[1]?new RegExp(m[1]):null,d=(m[2]??"$0").split(",").map(u=>u.trim()).filter(Boolean),c=0;for(let u of S(s,a).flatMap(_=>x(_.text))){if(c++,w&&!w.test(u))continue;let _=r.F?u.split(r.F==="\\t"?"	":r.F):u.trim().split(/\s+/);s.o((d.length?d:["$0"]).map(b=>b.split(/\s+/).map(v=>v==="$0"?u:/^\$\d+$/.test(v)?_[+v.slice(1)-1]??"":v==="NR"?c:v==="NF"?_.length:v==="$NF"?_[_.length-1]:v.replace(/^"|"$/g,"")).join("")).join(" ")+`
`)}return 0},tee(s){let{f:r,rest:a}=p(s.argv);for(let f of a)r.a?e.append(s.P(f),s.stdin):e.write(s.P(f),s.stdin);return s.o(s.stdin),0},seq(s){let r=s.argv.map(Number),[a,f,m]=r.length===1?[1,1,r[0]]:r.length===2?[r[0],1,r[1]]:r;for(let w=a;f>0?w<=m:w>=m;w+=f)s.o(w+`
`);return 0},async sleep(s){return await Ge(Math.min(parseFloat(s.argv[0])*1e3||0,3e4)),0},date(s){let r=new Date;return s.o(s.argv[0]==="-I"||s.argv[0]==="--iso-8601"?r.toISOString().slice(0,10)+`
`:s.argv[0]==="+%s"?Math.floor(r/1e3)+`
`:r.toString()+`
`),0},env(s){for(let[r,a]of Object.entries(s.sh.env))s.o(`${r}=${a}
`);return 0},basename(s){let r=e.base(e.norm(s.argv[0]||""));return s.argv[1]&&r.endsWith(s.argv[1])&&(r=r.slice(0,-s.argv[1].length)),s.o(r+`
`),0},dirname(s){let r=s.argv[0]||".",a=r.replace(/\/$/,"").lastIndexOf("/");return s.o((a<0?".":a===0?"/":r.slice(0,a))+`
`),0},realpath(s){for(let r of s.argv)s.o(s.P(r)+`
`);return 0},stat(s){for(let r of s.argv){let a=e.stat(s.P(r));s.o(`  File: ${r}
  Size: ${a.size}	Type: ${a.dir?"directory":"regular file"}
Modify: ${new Date(a.mtime).toISOString()}
`)}return 0},du(s){let{f:r,rest:a}=p(s.argv);for(let f of a.length?a:["."]){let m=0;for(let w of e.walk(s.P(f)))e.isFile(w)&&(m+=e.stat(w).size);s.o(`${r.h?j(m):Math.ceil(m/1024)}	${f}
`)}return 0},base64(s){let{f:r,rest:a}=p(s.argv),f=S(s,a)[0]?.text??"";if(r.d)s.o(K.decode(Uint8Array.from(atob(f.replace(/\s/g,"")),m=>m.charCodeAt(0))));else{let m="";for(let w of ue.encode(f))m+=String.fromCharCode(w);s.o(btoa(m).replace(/.{76}/g,`$&
`)+`
`)}return 0},rev(s){for(let r of S(s,s.argv).flatMap(a=>x(a.text)))s.o([...r].reverse().join("")+`
`);return 0},nl(s){let r=1;for(let a of S(s,s.argv).flatMap(f=>x(f.text)))s.o(a.trim()?`${String(r++).padStart(6)}	${a}
`:`
`);return 0},test(s){let r=[...s.argv];if(s.name==="["&&r.pop()!=="]")return s.e(`[: missing ]
`),2;let a=!1;r[0]==="!"&&(a=!0,r.shift());let f,[m,w,d]=r;if(r.length===0)f=!1;else if(r.length===1)f=m!=="";else if(r.length===2){let c=s.P(w);f={"-f":e.isFile(c),"-d":e.isDir(c),"-e":e.exists(c),"-s":e.isFile(c)&&e.stat(c).size>0,"-z":w==="","-n":w!=="","-r":e.exists(c),"-w":e.exists(c),"-x":!1}[m]??!1}else f={"=":m===d,"==":m===d,"!=":m!==d,"-eq":+m==+d,"-ne":+m!=+d,"-lt":+m<+d,"-le":+m<=+d,"-gt":+m>+d,"-ge":+m>=+d}[w]??!1;return(a?!f:f)?0:1},get"["(){return this.test},yes(s){return s.o(((s.argv[0]??"y")+`
`).repeat(100)),0},whoami(s){return s.o((s.sh.env.USER||"agent")+`
`),0},uname(s){return s.o(s.argv.includes("-a")?`JadeAgentKit browser 1.0 ${navigator.platform||"web"} wasm32
`:`JadeAgentKit
`),0},async sha256sum(s){for(let r of S(s,s.argv)){let a=await crypto.subtle.digest("SHA-256",ue.encode(r.text));s.o([...new Uint8Array(a)].map(f=>f.toString(16).padStart(2,"0")).join("")+"  "+r.name+`
`)}return 0},diff(s){let{f:r,rest:a}=p(s.argv);if(a.length<2)return s.e(`usage: diff [-u] FILE1 FILE2
`),2;let f=x(e.read(s.P(a[0]))),m=x(e.read(s.P(a[1])));return f.join(`
`)===m.join(`
`)?0:f.length*m.length>4e6?(s.o(`Files ${a[0]} and ${a[1]} differ
`),1):(s.o(`--- ${a[0]}
+++ ${a[1]}
`+$(f,m)),1)}};function $(s,r,a=3){let f=s.length,m=r.length,w=Array.from({length:f+1},()=>new Uint32Array(m+1));for(let v=f-1;v>=0;v--)for(let O=m-1;O>=0;O--)w[v][O]=s[v]===r[O]?w[v+1][O+1]+1:Math.max(w[v+1][O],w[v][O+1]);let d=[],c=0,u=0;for(;c<f||u<m;)c<f&&u<m&&s[c]===r[u]?(d.push([" ",s[c],c,u]),c++,u++):c<f&&(u>=m||w[c+1][u]>=w[c][u+1])?(d.push(["-",s[c],c,u]),c++):(d.push(["+",r[u],c,u]),u++);let _="",b=0;for(;b<d.length;){if(d[b][0]===" "){b++;continue}let v=Math.max(0,b-a),O=b;for(;O<d.length;){if(d[O][0]!==" "){O++;continue}let N=0;for(;O+N<d.length&&d[O+N][0]===" ";)N++;if(N>a*2||O+N>=d.length){O=Math.min(d.length,O+a);break}O+=N}let B=d.slice(v,O),L=B[0][2]+1,D=B[0][3]+1;_+=`@@ -${L},${B.filter(N=>N[0]!=="+").length} +${D},${B.filter(N=>N[0]!=="-").length} @@
`+B.map(N=>N[0]+N[1]+`
`).join(""),b=O}return _}return{Shell:l,BUILTINS:T,APPLETS:E,opts:p,inputs:S,splitLines:x,tokenize:n,parse:i,globToRe:o}}var Ae=class{constructor(e,{cwd:t="/",env:n={},timeoutMs:i=6e4}={},h=null,o=()=>"auto"){this.core=e,this.bb=h,this.engine=o,this.sh=new e.Shell({cwd:t,env:n}),this.sh.timeoutMs=i}get cwd(){return this.sh.cwd}set cwd(e){this.sh.cwd=e}get env(){return this.sh.env}async run(e,{stdin:t="",timeoutMs:n,onOutput:i,signal:h}={}){this.bb&&!this.bb.ready&&this.engine()!=="js"&&await this.bb.load();let o=this.sh;n&&(o.timeoutMs=n),o.onOutput=i||null,o.aborted=!1;let l=()=>{o.aborted=!0};h?.addEventListener?.("abort",l);try{let p=await o.run(String(e??""),{stdin:t}),S=p.chunks.filter(k=>!k.err).map(k=>k.s).join(""),x=p.chunks.filter(k=>k.err).map(k=>k.s).join("");return{stdout:S,stderr:x,code:p.code,output:p.chunks.map(k=>k.s).join("")}}finally{h?.removeEventListener?.("abort",l),o.onOutput=null}}};function Dt({vfs:g,busybox:e,engine:t="auto",commands:n={}}){let i={vfs:g,busybox:e,engine:t,commands:n},h=Mt(i);return{core:h,commands:n,session:o=>new Ae(h,o,e,()=>i.engine),get engine(){return i.engine},set engine(o){i.engine=o}}}var ft=`
const __out = []; let __files = {}; let __dirs = new Set(['/']); const __writes = {}; const __mk = new Set(); const __rmd = new Set(); let __cwd = '/';
const __norm = (p) => { p = String(p); if (p.startsWith('file://')) p = p.slice(7); const parts = (p.startsWith('/') ? p : __cwd + '/' + p).split('/'); const o = []; for (const s of parts) { if (!s || s === '.') continue; if (s === '..') o.pop(); else o.push(s); } return '/' + o.join('/'); };
const __fmt = (a) => a.map(x => typeof x === 'string' ? x : (() => { try { return x instanceof Error ? (x.stack || String(x)) : x === undefined ? 'undefined' : typeof x === 'function' ? '[Function]' : JSON.stringify(x, (k, v) => v instanceof Set ? [...v] : v instanceof Map ? Object.fromEntries(v) : typeof v === 'bigint' ? String(v) : v, 2) ?? String(x); } catch { return String(x); } })()).join(' ');
const __log = (k) => (...a) => { __out.push([k, __fmt(a) + '\\n']); };
const console = { log: __log('o'), info: __log('o'), debug: __log('o'), dir: __log('o'), table: __log('o'), warn: __log('e'), error: __log('e'), time() {}, timeEnd() {}, group() {}, groupEnd() {} };
const __isFile = p => (p in __writes) ? __writes[p] !== null : (p in __files);
const __isDir = p => __dirs.has(p);
const __parent = p => p === '/' ? '/' : (p.slice(0, p.lastIndexOf('/')) || '/');
const __err = (code, op, p) => { const e = new Error(\`\${code}: \${{ ENOENT: 'no such file or directory', EISDIR: 'illegal operation on a directory', ENOTDIR: 'not a directory', EEXIST: 'file already exists', ENOTEMPTY: 'directory not empty' }[code] || code}, \${op} '\${p}'\`); e.code = code; e.syscall = op; e.path = p; return e; };
const __mkp = p => { const chain = []; while (p !== '/' && !__dirs.has(p)) { if (__isFile(p)) throw __err('ENOTDIR', 'mkdir', p); chain.push(p); p = __parent(p); } for (const d of chain) { __dirs.add(d); __mk.add(d); __rmd.delete(d); } };
const __kids = p => { const pre = p === '/' ? '/' : p + '/'; const s = new Set(); const add = k => { if (k.startsWith(pre) && k !== p) s.add(k.slice(pre.length).split('/')[0]); }; for (const k of Object.keys(__files)) if (__isFile(k)) add(k); for (const k of Object.keys(__writes)) if (__writes[k] !== null) add(k); for (const d of __dirs) add(d); return [...s].sort(); };
const __enc = (o) => typeof o === 'string' ? o : o && o.encoding;
class Dirent { constructor(name, dir) { this.name = name; this._d = dir; } isFile() { return !this._d; } isDirectory() { return this._d; } isSymbolicLink() { return false; } }
const fs = {
  readFileSync(p, o) { p = __norm(p); if (__isDir(p)) throw __err('EISDIR', 'read', p); if (!__isFile(p)) throw __err('ENOENT', 'open', p); const t = (p in __writes) ? __writes[p] : __files[p]; if (t instanceof Uint8Array && (o === 'utf8' || o === 'utf-8' || (o && o.encoding))) return new TextDecoder().decode(t); return t; },
  writeFileSync(p, d) { p = __norm(p); if (__isDir(p)) throw __err('EISDIR', 'open', p); __mkp(__parent(p)); __writes[p] = typeof d === 'string' ? d : d == null ? '' : (d instanceof Uint8Array ? new TextDecoder().decode(d) : String(d)); },
  appendFileSync(p, d) { let prev = ''; try { prev = fs.readFileSync(p); } catch (e) { if (e.code !== 'ENOENT') throw e; } fs.writeFileSync(p, prev + String(d)); },
  existsSync(p) { p = __norm(p); return __isFile(p) || __isDir(p); },
  accessSync(p) { if (!fs.existsSync(p)) throw __err('ENOENT', 'access', __norm(p)); },
  readdirSync(p, o) { p = __norm(p); if (__isFile(p)) throw __err('ENOTDIR', 'scandir', p); if (!__isDir(p)) throw __err('ENOENT', 'scandir', p); const names = __kids(p); if (o && o.recursive) { const out = []; const rec = (d, pre) => { for (const n of __kids(d)) { const q = d === '/' ? '/' + n : d + '/' + n; out.push(o.withFileTypes ? new Dirent(pre + n, __isDir(q)) : pre + n); if (__isDir(q)) rec(q, pre + n + '/'); } }; rec(p, ''); return out; } return o && o.withFileTypes ? names.map(n => new Dirent(n, __isDir(p === '/' ? '/' + n : p + '/' + n))) : names; },
  statSync(p, o) { p = __norm(p); const d = __isDir(p); if (!d && !__isFile(p)) { if (o && o.throwIfNoEntry === false) return undefined; throw __err('ENOENT', 'stat', p); } const size = d ? 4096 : (x => typeof x === 'string' ? new TextEncoder().encode(x).length : x.length)(fs.readFileSync(p)); const t = new Date(); return { size, isFile: () => !d, isDirectory: () => d, isSymbolicLink: () => false, mtime: t, ctime: t, birthtime: t, mtimeMs: +t }; },
  mkdirSync(p, o) { p = __norm(p); const rec = o === true || (o && o.recursive); if (__isDir(p)) { if (rec) return undefined; throw __err('EEXIST', 'mkdir', p); } if (__isFile(p)) throw __err('EEXIST', 'mkdir', p); if (!rec && !__isDir(__parent(p))) throw __err('ENOENT', 'mkdir', p); __mkp(p); return rec ? p : undefined; },
  unlinkSync(p) { p = __norm(p); if (__isDir(p)) throw __err('EISDIR', 'unlink', p); if (!__isFile(p)) throw __err('ENOENT', 'unlink', p); __writes[p] = null; },
  rmdirSync(p, o) { p = __norm(p); if (!__isDir(p)) throw __err(__isFile(p) ? 'ENOTDIR' : 'ENOENT', 'rmdir', p); if (__kids(p).length && !(o && o.recursive)) throw __err('ENOTEMPTY', 'rmdir', p); fs.rmSync(p, { recursive: true }); },
  rmSync(p, o = {}) { p = __norm(p); if (__isFile(p)) { __writes[p] = null; return; } if (!__isDir(p)) { if (o.force) return; throw __err('ENOENT', 'rm', p); } if (p === '/') throw new Error('refusing to remove /'); if (!o.recursive && __kids(p).length) throw __err('ENOTEMPTY', 'rm', p); const pre = p + '/'; for (const k of [...Object.keys(__files), ...Object.keys(__writes)]) if (k.startsWith(pre) && __isFile(k)) __writes[k] = null; for (const d of [...__dirs]) if (d === p || d.startsWith(pre)) { __dirs.delete(d); __mk.delete(d); } __rmd.add(p); },
  renameSync(a, b) { a = __norm(a); b = __norm(b); if (__isFile(a)) { const t = fs.readFileSync(a); fs.writeFileSync(b, t); __writes[a] = null; return; } if (!__isDir(a)) throw __err('ENOENT', 'rename', a); const pre = a + '/'; __mkp(b); for (const k of [...Object.keys(__files), ...Object.keys(__writes)]) if (k.startsWith(pre) && __isFile(k)) { fs.writeFileSync(b + k.slice(a.length), fs.readFileSync(k)); __writes[k] = null; } for (const d of [...__dirs]) if (d.startsWith(pre)) __mkp(b + d.slice(a.length)); fs.rmSync(a, { recursive: true }); },
  copyFileSync(a, b) { fs.writeFileSync(b, fs.readFileSync(a)); },
  cpSync(a, b, o) { a = __norm(a); if (__isFile(a)) return fs.copyFileSync(a, b); for (const n of fs.readdirSync(a, { recursive: true })) { const q = a + '/' + n; if (__isFile(q)) fs.writeFileSync(__norm(b) + '/' + n, fs.readFileSync(q)); } },
  lstatSync(p, o) { return fs.statSync(p, o); }, realpathSync(p) { return __norm(p); }, constants: { F_OK: 0, R_OK: 4, W_OK: 2, X_OK: 1 },
};
fs.promises = {}; for (const k of ['readFile', 'writeFile', 'appendFile', 'readdir', 'stat', 'lstat', 'mkdir', 'unlink', 'rm', 'rmdir', 'rename', 'copyFile', 'access', 'cp', 'realpath']) {
  const sync = fs[k + 'Sync'];
  fs.promises[k] = async (...a) => sync(...a);
  fs[k] = (...a) => { const cb = typeof a[a.length - 1] === 'function' ? a.pop() : null; let r, e = null; try { r = sync(...a); } catch (x) { e = x; } if (cb) queueMicrotask(() => cb(e, r)); };
}
fs.exists = (p, cb) => queueMicrotask(() => cb(fs.existsSync(p)));
const path = {
  sep: '/', delimiter: ':',
  normalize: p => { const abs = String(p).startsWith('/'); const o = []; for (const s of String(p).split('/')) { if (!s || s === '.') continue; if (s === '..') { if (o.length && o[o.length - 1] !== '..') o.pop(); else if (!abs) o.push('..'); } else o.push(s); } return (abs ? '/' : '') + o.join('/') || (abs ? '/' : '.'); },
  join: (...a) => path.normalize(a.filter(x => x !== '').join('/')),
  resolve: (...a) => { let r = ''; for (const x of a) r = String(x).startsWith('/') ? x : (r ? r + '/' + x : x); return __norm(r || '.'); },
  isAbsolute: p => String(p).startsWith('/'),
  basename: (p, ext) => { let b = String(p).replace(/\\/+$/, '').split('/').pop(); return ext && b.endsWith(ext) && b !== ext ? b.slice(0, -ext.length) : b; },
  dirname: p => { p = String(p).replace(/\\/+$/, ''); const i = p.lastIndexOf('/'); return i < 0 ? '.' : i === 0 ? '/' : p.slice(0, i); },
  extname: p => { const b = path.basename(p); const i = b.lastIndexOf('.'); return i > 0 ? b.slice(i) : ''; },
  relative: (a, b) => { const A = __norm(a).split('/').filter(Boolean), B = __norm(b).split('/').filter(Boolean); let i = 0; while (i < A.length && A[i] === B[i]) i++; return [...A.slice(i).map(() => '..'), ...B.slice(i)].join('/'); },
  parse: p => { const base = path.basename(p), ext = path.extname(p); return { root: String(p).startsWith('/') ? '/' : '', dir: path.dirname(p), base, ext, name: ext ? base.slice(0, -ext.length) : base }; },
  format: o => (o.dir ? o.dir + '/' : '') + (o.base || (o.name || '') + (o.ext || '')),
};
path.posix = path;
class __Exit { constructor(c) { this.code = c; } }
const process = { argv: [], env: { HOME: '/', USER: 'jade', PWD: '/' }, cwd: () => __cwd, chdir: d => { __cwd = __norm(d); }, exit: (c = 0) => { throw new __Exit(c); }, exitCode: 0, platform: 'linux', version: 'v20.0.0-browser', versions: { node: '20.0.0' }, stdout: { write: s => { __out.push(['o', String(s)]); return true; }, isTTY: false, columns: 80 }, stderr: { write: s => { __out.push(['e', String(s)]); return true; } }, nextTick: (f, ...a) => queueMicrotask(() => f(...a)), hrtime: Object.assign((t) => { const n = performance.now(); return [Math.floor(n / 1000), Math.round((n % 1000) * 1e6)]; }, { bigint: () => BigInt(Math.round(performance.now() * 1e6)) }), memoryUsage: () => ({ heapUsed: 0 }), on() {} };
const __mods = {};

// ---- SQLite: require('node:sqlite') (DatabaseSync) and require('better-sqlite3'), on the embedded SQLite build ----
let __bins = {}, __sqMod = null, __sqApi = null; const __sqOpen = new Set();
function __sqliteApi() {
  if (__sqApi) return __sqApi;
  if (typeof __jvSqlite !== 'function' || !__sqMod) throw new Error('SQLite is not available in this script');
  return (__sqApi = __jvSqlite(__sqMod));
}
function __sqliteModule(flavor) {
  const S = __sqliteApi();
  const toObj = (cols, r) => { const o = {}; cols.forEach((c, i) => { o[c] = r[i]; }); return o; };
  class StatementSync {
    constructor(db, sql) { this._db = db; this._st = db._d.prepare(sql); this.sourceSQL = sql; this.reader = this._st.columns().length > 0; this._raw = false; this._pluck = false; }
    _p(a) { if (a.length === 1 && a[0] && typeof a[0] === 'object' && !(a[0] instanceof Uint8Array)) return Array.isArray(a[0]) ? a[0] : a[0]; return a.length ? a : null; }
    _shape(cols, r) { return this._pluck ? r[0] : this._raw ? r : toObj(cols, r); }
    all(...a) { const cols = this._st.columns(); return this._st.rows(this._p(a)).map(r => this._shape(cols, r)); }
    get(...a) { const cols = this._st.columns(); for (const r of this._st.iterate(this._p(a))) { const v = this._shape(cols, r); this._st.bind(null); return v; } return undefined; }
    run(...a) { this._st.bind(this._p(a)); while (this._st.step()) {} return { changes: this._db._d.changes(), lastInsertRowid: this._db._d.lastInsertRowid() }; }
    *iterate(...a) { const cols = this._st.columns(); for (const r of this._st.iterate(this._p(a))) yield this._shape(cols, r); }
    columns() { return this._st.columns().map(name => ({ name, column: name })); }
    raw(on = true) { this._raw = on; return this; } pluck(on = true) { this._pluck = on; return this; }
    expandedSQL() { return this.sourceSQL; } finalize() { this._st.finalize(); }
  }
  class DatabaseSync {
    constructor(path = ':memory:', opts = {}) { this._path = !path || path === ':memory:' ? null : __norm(path); this._ro = !!(opts.readOnly || opts.readonly); this._d = null; if (opts.open !== false) this.open(); }
    open() {
      if (this._d) throw new Error('database is already open');
      let bytes = null;
      if (this._path) { if (this._path in __writes) { if (__writes[this._path] instanceof Uint8Array) bytes = __writes[this._path]; else if (__writes[this._path] && __writes[this._path].length) throw new Error(\`file is not a database: \${this._path}\`); } else if (__bins[this._path]) bytes = __bins[this._path]; else if (__isFile(this._path)) { const t = fs.readFileSync(this._path); if (t.length) throw new Error(\`file is not a database: \${this._path}\`); } else if (this._ro) throw new Error(\`unable to open database file: \${this._path}\`); }
      this._d = new S.Database(bytes); __sqOpen.add(this);
    }
    get isOpen() { return !!this._d; } get open_() { return !!this._d; } get name() { return this._path || ':memory:'; } get inTransaction() { return !!this._d && this._d.inTransaction(); }
    exec(sql) { if (this._ro && !/^\\s*(select|pragma|with|explain)\\b/i.test(sql)) throw new Error('attempt to write a readonly database'); this._d.exec(sql); return this; }
    prepare(sql) { return new StatementSync(this, sql); }
    pragma(s, o = {}) { const r = this._d.exec('PRAGMA ' + s)[0]; if (!r) return []; const rows = r.values.map(v => toObj(r.columns, v)); return o.simple ? (r.values[0] ? r.values[0][0] : undefined) : rows; }
    transaction(fn) { const self = this; return function (...a) { self._d.exec('BEGIN'); try { const r = fn.apply(this, a); self._d.exec('COMMIT'); return r; } catch (e) { try { self._d.exec('ROLLBACK'); } catch {} throw e; } }; }
    _flush() { if (this._path && this._d && this._d.dirty && !this._ro) { const b = this._d.export(); __writes[this._path] = b; __bins[this._path] = b; __mkp(__parent(this._path)); this._d.dirty = false; } }
    close() { if (this._d) { this._flush(); this._d.close(); this._d = null; __sqOpen.delete(this); } return this; }
  }
  if (flavor === 'better-sqlite3') { function Database(path, opts) { return new DatabaseSync(path, opts); } Database.prototype = DatabaseSync.prototype; return Database; }
  return { DatabaseSync, StatementSync, constants: {} };
}

// ---- network: global fetch (tracked so the script waits for it), Buffer, and http/https on top of fetch ----
let __inflight = 0; const __fetch0 = self.fetch ? self.fetch.bind(self) : null;
const __track = p => { __inflight++; p.then(() => { __inflight--; }, () => { __inflight--; }); return p; };
if (__fetch0) { self.fetch = (...a) => __track(__fetch0(...a)); for (const k of ['text', 'json', 'arrayBuffer', 'blob', 'formData']) { const f = Response.prototype[k]; if (f) Response.prototype[k] = function () { return __track(f.call(this)); }; } }
class Buffer extends Uint8Array {
  static from(x, enc) {
    if (typeof x === 'string') { if (enc === 'base64') return new Buffer(Uint8Array.from(atob(x.replace(/[^A-Za-z0-9+/=]/g, '')), c => c.charCodeAt(0))); if (enc === 'hex') return new Buffer((x.match(/../g) || []).map(h => parseInt(h, 16))); return new Buffer(new TextEncoder().encode(x)); }
    if (x instanceof ArrayBuffer) return new Buffer(new Uint8Array(x)); return new Buffer(Uint8Array.from(x || []));
  }
  static alloc(n, fill = 0) { const b = new Buffer(n); b.fill(fill); return b; }
  static concat(list) { const n = list.reduce((a, b) => a + b.length, 0); const out = new Buffer(n); let o = 0; for (const b of list) { out.set(b, o); o += b.length; } return out; }
  static isBuffer(x) { return x instanceof Uint8Array; }
  static byteLength(s) { return typeof s === 'string' ? new TextEncoder().encode(s).length : s.length; }
  toString(enc) { if (enc === 'base64') { let s = ''; for (let i = 0; i < this.length; i += 0x8000) s += String.fromCharCode.apply(null, this.subarray(i, i + 0x8000)); return btoa(s); } if (enc === 'hex') return [...this].map(b => b.toString(16).padStart(2, '0')).join(''); return new TextDecoder().decode(this); }
  toJSON() { return { type: 'Buffer', data: [...this] }; }
}
const __mkHttp = (proto) => {
  function request(url, opts, cb) {
    if (url && typeof url === 'object' && !(url instanceof URL)) { cb = opts; opts = url; url = null; }
    if (typeof opts === 'function') { cb = opts; opts = {}; } opts = opts || {};
    const u = url ? new URL(String(url)) : new URL(\`\${opts.protocol || proto}//\${opts.hostname || opts.host || 'localhost'}\${opts.port ? ':' + opts.port : ''}\${opts.path || '/'}\`);
    const L = {}, chunks = []; const emit = (ev, ...a) => (L[ev] || []).forEach(f => f(...a));
    const req = {
      on(ev, f) { (L[ev] ||= []).push(f); return req; }, once(ev, f) { return req.on(ev, f); },
      write(d) { chunks.push(typeof d === 'string' ? new TextEncoder().encode(d) : d); return true; },
      setHeader(k, v) { (opts.headers ||= {})[k] = v; }, getHeader(k) { return (opts.headers || {})[k]; },
      setTimeout(ms, f) { req._to = ms; if (f) req.on('timeout', f); return req; },
      destroy(e) { try { req._ab && req._ab.abort(); } catch (x) {} if (e) emit('error', e); }, abort() { req.destroy(); },
      end(d) {
        if (d) req.write(d); if (cb) req.on('response', cb);
        const ab = new AbortController(); req._ab = ab; const to = req._to || opts.timeout;
        const timer = to ? self.setTimeout(() => { emit('timeout'); ab.abort(); }, to) : null;
        self.fetch(u.toString(), { method: String(opts.method || 'GET').toUpperCase(), headers: opts.headers || {}, body: chunks.length ? new Blob(chunks) : undefined, signal: ab.signal })
          .then(async r => {
            const buf = Buffer.from(await r.arrayBuffer()); if (timer) self.clearTimeout(timer);
            const RL = {}; const headers = {}; r.headers.forEach((v, k) => { headers[k.toLowerCase()] = v; });
            const res = { statusCode: r.status, statusMessage: r.statusText, headers, _enc: null,
              on(ev, f) { (RL[ev] ||= []).push(f); return res; }, once(ev, f) { return res.on(ev, f); }, setEncoding(e) { res._enc = e; return res; }, resume() { return res; },
              pipe(dst) { res.on('data', c => dst.write(c)); res.on('end', () => dst.end && dst.end()); return dst; } };
            emit('response', res);
            self.setTimeout(() => { if (buf.length) (RL.data || []).forEach(f => f(res._enc ? buf.toString() : buf)); (RL.end || []).forEach(f => f()); (RL.close || []).forEach(f => f()); }, 0);
          }, e => { if (timer) self.clearTimeout(timer); emit('error', e); });
        return req;
      },
    };
    return req;
  }
  return { request, get: (u, o, c) => { const r = request(u, o, c); r.end(); return r; }, Agent: function Agent() {}, globalAgent: {}, METHODS: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'], STATUS_CODES: { 200: 'OK', 201: 'Created', 204: 'No Content', 400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found', 429: 'Too Many Requests', 500: 'Internal Server Error' } };
};
const __core = (m) => { m = String(m).replace(/^node:/, ''); if (/^@tensorflow\\/tfjs(-core|-layers|-backend-cpu|-backend-webgl)?$/.test(m)) { if (self.tf) return self.tf; throw new Error("TensorFlow.js was not loaded for this script"); } if (m === 'fs') return fs; if (m === 'https') return __mkHttp('https:'); if (m === 'http') return __mkHttp('http:'); if (m === 'buffer') return { Buffer }; if (m === 'fs/promises') return fs.promises; if (m === 'path' || m === 'path/posix') return path; if (m === 'util') return { inspect: x => __fmt([x]), format: (...a) => __fmt(a), promisify: f => (...a) => new Promise((res, rej) => f(...a, (e, r) => e ? rej(e) : res(r))) }; if (m === 'os') return { EOL: '\\n', platform: () => 'linux', homedir: () => '/', tmpdir: () => '/tmp', cpus: () => [{}], hostname: () => 'jade' }; if (m === 'readline') return { createInterface: () => ({ on() {}, question(q, cb) { cb(''); }, close() {} }) }; if (m === 'sqlite') return __sqliteModule('node'); if (m === 'better-sqlite3') return __sqliteModule('better-sqlite3'); if (m === 'sqlite3') throw new Error("the callback-based 'sqlite3' npm package is not available; use require('node:sqlite') (DatabaseSync) or require('better-sqlite3'), both synchronous"); if (m === 'child_process') throw new Error("child_process is not available in the browser sandbox; use the bash tool for shell commands"); return null; };
const __mkRequire = (dir) => (m) => {
  const c = __core(m); if (c) return c;
  m = String(m);
  if (!/^(\\.{1,2}\\/|\\/)/.test(m)) throw new Error("Cannot find module '" + m + "' (browser sandbox: fs, path, util, os and local files like ./lib.js; no npm packages)");
  const base = __norm(m.startsWith('/') ? m : dir + '/' + m);
  const cand = [base, base + '.js', base + '.cjs', base + '.json', base + '/index.js'].find(p => __isFile(p));
  if (!cand) throw new Error("Cannot find module '" + m + "' (looked for " + base + "[.js|.json|/index.js])");
  if (__mods[cand]) return __mods[cand].exports;
  if (cand.endsWith('.json')) return (__mods[cand] = { exports: JSON.parse(fs.readFileSync(cand)) }).exports;
  const mod = __mods[cand] = { exports: {} };
  let src = fs.readFileSync(cand).replace(/^#!.*\\n/, '');
  src = src.replace(/^\\s*import\\s+\\*\\s+as\\s+(\\w+)\\s+from\\s+['"]([^'"]+)['"];?/gm, 'const $1 = require("$2");').replace(/^\\s*import\\s+(\\w+)\\s+from\\s+['"]([^'"]+)['"];?/gm, 'const $1 = require("$2");').replace(/^\\s*import\\s+\\{([^}]+)\\}\\s+from\\s+['"]([^'"]+)['"];?/gm, (s, a, b) => 'const {' + a.replace(/\\s+as\\s+/g, ': ') + '} = require("' + b + '");').replace(/^\\s*export\\s+default\\s+/gm, 'module.exports = ').replace(/^\\s*export\\s+(?=(const|let|var|function|class|async)\\b)/gm, '');
  new Function('module', 'exports', 'require', '__filename', '__dirname', 'console', 'process', src)(mod, mod.exports, __mkRequire(__parent(cand)), cand, __parent(cand), console, process);
  return mod.exports;
};
// ---- jade: call Jade's tools, decisions, model, shell and flows from a script ----
// Each call goes to the app over postMessage. Files the script wrote are handed over first, and files the
// call changed come back, so fs and Jade's tools see the same vault.
let __globals = {}; let __jseq = 0; const __jpend = new Map(); let __jbridge = true; let __jwhy = '';
function __takeSync() {
  const w = {}; let n = 0;
  for (const p of Object.keys(__writes)) { const d = __writes[p]; w[p] = d; n++; if (d === null) delete __files[p]; else __files[p] = d; delete __writes[p]; }
  const mk = [...__mk], rm = [...__rmd]; __mk.clear(); __rmd.clear();
  return n || mk.length || rm.length ? { writes: w, mkdirs: mk, rmdirs: rm } : null;
}
function __applySync(s) {
  if (!s) return;
  for (const p of s.deleted || []) { delete __files[p]; delete __writes[p]; }
  for (const d of s.rmdirs || []) __dirs.delete(d);
  for (const d of s.dirs || []) __dirs.add(d);
  for (const [p, d] of Object.entries(s.files || {})) { __files[p] = d; delete __writes[p]; let q = __parent(p); while (q !== '/' && !__dirs.has(q)) { __dirs.add(q); q = __parent(q); } }
}
const __jcall = (op, a) => {
  if (!__jbridge) return Promise.reject(new Error(\`jade.\${op} is not available here\${__jwhy ? ': ' + __jwhy : ''}\`));
  let args; try { args = a == null ? {} : JSON.parse(JSON.stringify(a)); } catch (e) { return Promise.reject(new Error(\`jade.\${op}: arguments must be plain JSON data (\${e.message})\`)); }
  return new Promise((res, rej) => { const id = ++__jseq; __inflight++; __jpend.set(id, { res, rej }); self.postMessage({ t: 'jade', id, op, a: args, sync: __takeSync() }); });
};
self.addEventListener('message', ev => {
  const m = ev.data; if (!m || m.t !== 'jret') return;
  const p = __jpend.get(m.id); if (!p) return; __jpend.delete(m.id); __inflight--;
  __applySync(m.sync); m.ok ? p.res(m.value) : p.rej(new Error(m.error));
});
const jade = Object.freeze({
  tool: (name, args) => __jcall('tool', { name: String(name), args: args || {} }),
  tools: new Proxy({}, { get: (_, n) => typeof n === 'string' && n !== 'then' && n !== 'toJSON' ? (args) => __jcall('tool', { name: n, args: args || {} }) : undefined }),
  list: () => __jcall('list', {}),
  decide: (o) => __jcall('decide', o || {}),
  ask: (prompt, o) => __jcall('ask', { ...(o || {}), prompt: String(prompt ?? '') }),
  agent: (message, o) => __jcall('agent', { ...(o || {}), message: String(message ?? '') }),
  flow: (name, input) => __jcall('flow', { name: String(name), input: input === undefined ? null : input }),
  flows: () => __jcall('flows', {}),
  shell: (command) => __jcall('shell', { command: String(command ?? '') }),
  notify: (title, body) => __jcall('notify', { title: String(title ?? ''), body: String(body ?? '') }),
  search: (query, limit) => __jcall('tool', { name: 'notes_search', args: { query: String(query ?? ''), ...(limit ? { limit } : {}) } }),
  kv: Object.freeze({ get: (k) => __jcall('kv', { op: 'get', k: String(k) }), set: (k, v) => __jcall('kv', { op: 'set', k: String(k), v: v === undefined ? null : v }), all: () => __jcall('kv', { op: 'all' }) }),
  prompt: (message, def) => __jcall('ui.prompt', { message: String(message ?? ''), def: def == null ? '' : String(def) }),
  suggest: (items, values, placeholder) => __jcall('ui.suggest', { items, values, placeholder }),
  sleep: (ms) => new Promise(r => setTimeout(r, Math.max(0, +ms || 0))),
});
let require = __mkRequire('/');
const module = { exports: {} }; const exports = module.exports; let __filename = '/[eval]', __dirname = '/';
let __pending = 0; const __st = self.setTimeout.bind(self), __ct = self.clearTimeout.bind(self); const __live = new Set();
self.setTimeout = (f, ms, ...a) => { const id = __st(() => { __live.delete(id); try { typeof f === 'function' && f(...a); } catch (e) { __out.push(['e', (e && e.stack || e) + '\\n']); } }, ms); __live.add(id); return id; };
self.clearTimeout = (id) => { __live.delete(id); __ct(id); };
let __code = 0;
let __ret;
self.onmessage = async (ev) => {
  if (ev.data && ev.data.t === 'jret') return;
  __globals = ev.data.globals || {}; __jbridge = ev.data.bridge !== false; __jwhy = ev.data.bridgeWhy || '';
  if (ev.data.noNet) { self.fetch = undefined; self.XMLHttpRequest = undefined; self.WebSocket = undefined; self.EventSource = undefined; }
  __files = ev.data.files; __bins = ev.data.bins || {}; __sqMod = ev.data.sqliteModule || null; __dirs = new Set(ev.data.dirs); __cwd = ev.data.cwd; process.env.PWD = __cwd; Object.assign(process.env, ev.data.env || {}); process.argv = ['node', ...ev.data.argv];
  if (ev.data.argv[0] && ev.data.argv[0].startsWith('/')) { __filename = ev.data.argv[0]; __dirname = __parent(__filename); require = __mkRequire(__dirname); } else require = __mkRequire(__cwd);
  try { if (self.__tfInit) await self.__tfInit(); __ret = await __main(); await new Promise(r => __st(r, 5)); while (__live.size || __inflight) await new Promise(r => __st(r, 10)); for (const d of __sqOpen) d._flush(); } catch (err) { if (err instanceof __Exit) __code = err.code; else { __out.push(['e', (err && (err.code ? err.message : err.stack)) || String(err)]); __out.push(['e', '\\n']); __code = 1; } }
  if (!__code && process.exitCode) __code = process.exitCode;
  let ret; if (__ret !== undefined) { try { ret = JSON.parse(JSON.stringify(__ret)); } catch (e) { ret = String(__ret); } }
  self.postMessage({ out: __out, writes: __writes, mkdirs: [...__mk], rmdirs: [...__rmd], code: __code, ret });
};
self.addEventListener('unhandledrejection', e => { __out.push(['e', 'Unhandled promise rejection: ' + ((e.reason && e.reason.stack) || e.reason) + '\\n']); });
`;var ts=/\btf\s*\.\s*[A-Za-z_$]|@tensorflow\/tfjs/,Te=class{constructor({vfs:e,sqlite:t=null,ml:n=null,bridge:i=null}){this.vfs=e,this.sqlite=t,this.ml=n,this.bridge=i}_changesSince(e){let t={},n=[],i=[],h=[];for(let[o,l]of this.vfs.nodes){let p=e.get(o);if(l.dir){p!=="d"&&i.push(o);continue}p!==l&&(_e(l.data)?t[o]=l.data:l.data.length<2e6&&(t[o]=K.decode(l.data)))}for(let[o,l]of e)this.vfs.nodes.has(o)||(l==="d"?h:n).push(o);return Object.keys(t).length||n.length||i.length||h.length?{files:t,deleted:n,dirs:i,rmdirs:h}:null}_apply(e,t){if(!e)return;let n=Object.entries(e.writes||{});this.vfs.applyChanges({deletes:n.filter(([,i])=>i===null).map(([i])=>i),rmdirs:e.rmdirs||[],mkdirs:e.mkdirs||[],writes:Object.fromEntries(n.filter(([,i])=>i!==null))},t)}async run(e,{argv:t=["[eval]"],cwd:n="/",globals:i=null,timeoutMs:h=6e4,readOnly:o=!1,network:l=!0,env:p={},signal:S=null}={}){let x=this.vfs;e=String(e??"").replace(/^#!.*\n/,""),/^\s*(import|export)\s/m.test(e)&&(e=e.replace(/^\s*import\s+\*\s+as\s+(\w+)\s+from\s+['"]([^'"]+)['"];?/gm,'const $1 = require("$2");').replace(/^\s*import\s+(\w+)\s+from\s+['"]([^'"]+)['"];?/gm,'const $1 = require("$2");').replace(/^\s*import\s+\{([^}]+)\}\s+from\s+['"]([^'"]+)['"];?/gm,(u,_,b)=>"const {"+_.replace(/\s+as\s+/g,": ")+'} = require("'+b+'");').replace(/^\s*export\s+(default\s+)?/gm,""));let k={},j=[],q={};for(let[u,_]of x.nodes)_.dir?j.push(u):_e(_.data)?(q[u]=_.data,k[u]=_.data):_.data.length<2e6&&(k[u]=K.decode(_.data));let y=u=>u.test(e)||[...x.nodes].some(([_,b])=>!b.dir&&/\.[cm]?js$/.test(_)&&b.data.length<2e6&&u.test(K.decode(b.data))),A=null,T="",E="";if(this.sqlite&&y(/sqlite/i))try{A=await this.sqlite.module(),T=this.sqlite.glueSource}catch(u){return{stdout:"",stderr:`node: could not load SQLite (${u.message})
`,code:1}}if(this.ml&&l&&y(ts))try{E=await this.ml.tfjsSource()}catch(u){return{stdout:"",stderr:`node: could not load TensorFlow.js (${u.message})
`,code:1}}let $=i?Object.keys(i).filter(u=>/^[$A-Za-z_][\w$]*$/.test(u)):[],s=$.length?`const { ${$.join(", ")} } = __globals;
`:"",r=ft+`
const kit = jade;

async function __main() {
${s}${e}
}
`+(T?`
`+T+`
`:"")+(E?`
(function () { var exports, module, define;
${E}
}).call(self);
self.__tfInit = async () => { const tf = self.tf; try { tf.env().set('IS_NODE', false); } catch (e) {} const keep = { log: console.log, info: console.info, warn: console.warn, error: console.error }; console.log = console.info = console.warn = console.error = () => {}; try { let gl = false; try { gl = typeof OffscreenCanvas !== 'undefined' && !!new OffscreenCanvas(2, 2).getContext('webgl2'); } catch (e) {} for (const b of ['webgpu', 'webgl']) { if (b === 'webgpu' && !(self.navigator && self.navigator.gpu)) continue; if (b === 'webgl' && !gl) continue; try { if (tf.findBackendFactory(b) && await tf.setBackend(b)) { await tf.ready(); const v = await tf.tensor([1, 2]).add(1).data(); if (v[0] === 2) return; } } catch (e) {} } for (const b of ['webgpu', 'webgl']) { try { tf.removeBackend(b); } catch (e) {} } await tf.setBackend('cpu'); await tf.ready(); } finally { Object.assign(console, keep); } };
`:""),a=ft.split(`
`).length+3+(s?1:0),f=URL.createObjectURL(new Blob([r],{type:"text/javascript"})),m=this.bridge,w=await new Promise(u=>{let _;try{_=new Worker(f,{name:"node"})}catch(L){u({out:[["e",`node: could not start a worker (${L.message})
`]],writes:{},code:1});return}let b=!1,v=L=>{b||(b=!0,clearTimeout(O),S?.removeEventListener?.("abort",B),_.terminate(),u(L))},O=setTimeout(()=>v({out:[["e",`node: killed after ${h/1e3}s timeout
`]],writes:{},code:124}),h),B=()=>v({out:[["e",`node: stopped
`]],writes:{},code:130});S?.addEventListener?.("abort",B),_.onmessage=async L=>{let D=L.data;if(D&&D.t==="jade"){let N;try{if(!m)throw new Error("kit calls are not available here");D.sync&&!o&&this._apply(D.sync);let U=new Map;for(let[Y,W]of x.nodes)U.set(Y,W.dir?"d":W);let P=await m(D.op,D.a||{}),z=P===void 0?null:P;try{z=JSON.parse(JSON.stringify(z))}catch{z=String(z)}N={t:"jret",id:D.id,ok:!0,value:z,sync:o?null:this._changesSince(U)}}catch(U){N={t:"jret",id:D.id,ok:!1,error:String(U?.message||U)}}b||_.postMessage(N);return}v(D)},_.onerror=L=>{L.preventDefault?.(),v({out:[["e",`${L.message||"SyntaxError"}${L.lineno?` (line ${Math.max(1,L.lineno-a)})`:""}
`]],writes:{},code:1})},_.postMessage({files:k,dirs:j,bins:q,sqliteModule:A,env:p,cwd:n,argv:t,globals:i?JSON.parse(JSON.stringify(i)):{},bridge:!!m,bridgeWhy:m?"":"no host bridge",noNet:!l})});URL.revokeObjectURL(f);let d=[];o||this._apply(w,u=>d.push(u.message+`
`));let c=w.out||[];return{stdout:c.filter(u=>u[0]==="o").map(u=>u[1]).join(""),stderr:c.filter(u=>u[0]==="e").map(u=>u[1]).join("")+d.join(""),output:c.map(u=>u[1]).join(""),code:w.code??1,result:w.ret}}command(){return async e=>{let t=e.argv,n,i,h=t.findIndex(l=>l==="-e"||l==="-p"||l==="--eval"||l==="--print");if(h>=0)n=/p/.test(t[h])?`console.log(${t[h+1]??""})`:t[h+1]??"",i=["[eval]",...t.slice(h+2)];else if(t.length&&t[0]!=="-"){let l=e.P(t[0]);if(!this.vfs.isFile(l))return e.e(`node: cannot find module '${t[0]}'
`),1;n=this.vfs.read(l),i=[l,...t.slice(1)]}else n=e.stdin,i=["[stdin]"];if(!String(n).trim())return e.e(`node: no script given. Use node file.js or node -e "code"
`),1;let o=await this.run(n,{argv:i,cwd:e.sh.cwd,timeoutMs:e.sh.timeoutMs,env:e.sh.env});return e.o(o.stdout),e.e(o.stderr),o.code}}};function Ft(g,e){let t=JSON.stringify(e+"micropython.mjs"),n={},i=String(g).replace(/import\.meta\.url/g,t).replace(/import\.meta\b/g,`({ url: ${t} })`).replace(/\bexport\s*\{([^}]*)\}\s*;?/g,(l,p)=>{for(let S of p.split(",")){let[x,k]=S.trim().split(/\s+as\s+/);x&&(n[(k||x).trim()]=x.trim())}return";"}).replace(/\bexport\s+default\s+(?=[\w$])/g,"var __mpyDefault = ").replace(/\bexport\s+(?=(?:async\s+function|function\*?|const|let|var|class)\b)/g,""),h=n.loadMicroPython||"loadMicroPython";return`const __mpyFactory = async () => {
const navigator = (() => { const n = globalThis.navigator; if (!n) return n; const ua = String(n.userAgent || '').replace(/\\s*Version\\/[\\d.]+/, '');
    return new Proxy(n, { get: (t, k) => k === 'userAgent' ? ua : (typeof t[k] === 'function' ? t[k].bind(t) : t[k]) }); })();
${i}
;return { loadMicroPython: typeof ${h} === 'function' ? ${h} : undefined };
};
`}var Nt=`def __jv_compat():
    import sys
    import os as _os
    if hasattr(_os, 'walk') and hasattr(_os, 'path'):
        return
    S_IFMT, S_IFDIR, S_IFREG = 0o170000, 0o040000, 0o100000
    class _Path:
        sep = '/'
        curdir = '.'
        def join(self, a, *p):
            for b in p:
                if b.startswith('/'):
                    a = b
                elif not a or a.endswith('/'):
                    a = a + b
                else:
                    a = a + '/' + b
            return a
        def _mode(self, p):
            try:
                return _os.stat(p)[0]
            except OSError:
                return None
        def exists(self, p):
            return self._mode(p) is not None
        def isdir(self, p):
            m = self._mode(p)
            return m is not None and (m & S_IFMT) == S_IFDIR
        def isfile(self, p):
            m = self._mode(p)
            return m is not None and (m & S_IFMT) == S_IFREG
        def getsize(self, p):
            return _os.stat(p)[6]
        def basename(self, p):
            return p.rsplit('/', 1)[-1]
        def dirname(self, p):
            if '/' not in p:
                return ''
            d = p.rsplit('/', 1)[0]
            return d if d else '/'
        def split(self, p):
            return (self.dirname(p), self.basename(p))
        def splitext(self, p):
            b = self.basename(p)
            i = b.rfind('.')
            if i <= 0:
                return (p, '')
            return (p[:len(p) - len(b) + i], b[i:])
        def normpath(self, p):
            absolute = p.startswith('/')
            out = []
            for s in p.split('/'):
                if s in ('', '.'):
                    continue
                if s == '..':
                    if out and out[-1] != '..':
                        out.pop()
                    elif not absolute:
                        out.append(s)
                else:
                    out.append(s)
            r = '/'.join(out)
            return ('/' + r) if absolute else (r or '.')
        def abspath(self, p):
            return self.normpath(p if p.startswith('/') else self.join(_os.getcwd(), p))
        def relpath(self, p, start='.'):
            a = [x for x in self.abspath(p).split('/') if x]
            b = [x for x in self.abspath(start).split('/') if x]
            i = 0
            while i < len(a) and i < len(b) and a[i] == b[i]:
                i += 1
            return '/'.join(['..'] * (len(b) - i) + a[i:]) or '.'
        def expanduser(self, p):
            return '/' + p[2:] if p.startswith('~/') else ('/' if p == '~' else p)
    path = _Path()
    def walk(top, topdown=True):
        try:
            names = _os.listdir(top)
        except OSError:
            return
        dirs, files = [], []
        for n in names:
            (dirs if path.isdir(path.join(top, n)) else files).append(n)
        if topdown:
            yield top, dirs, files
        for d in dirs:
            yield from walk(path.join(top, d), topdown)
        if not topdown:
            yield top, dirs, files
    def makedirs(p, exist_ok=False):
        cur = '/' if p.startswith('/') else ''
        for part in [x for x in p.split('/') if x]:
            cur = path.join(cur, part) if cur else part
            if not path.isdir(cur):
                _os.mkdir(cur)
            elif cur == p.rstrip('/') and not exist_ok:
                raise OSError(17)
    class _OS:
        def __getattr__(self, k):
            return getattr(_os, k)
    m = _OS()
    m.path = path
    m.sep = '/'
    if not hasattr(_os, 'walk'):
        m.walk = walk
    if not hasattr(_os, 'makedirs'):
        m.makedirs = makedirs
    sys.modules['os'] = m
    sys.modules['os.path'] = path
try:
    __jv_compat()
except Exception:
    pass
del __jv_compat
`,ut=`
const dec = new TextDecoder();
self.onmessage = async (ev) => {
  const { wasm, files, dirs, cwd, argv, code, stdin, heap, compat, sqliteModule, sqliteShim } = ev.data;
  const outB = [], errB = [], out = [];
  const flush = () => { if (outB.length) { out.push(['o', dec.decode(new Uint8Array(outB.splice(0)))]); } if (errB.length) { out.push(['e', dec.decode(new Uint8Array(errB.splice(0)))]); } };
  let exit = 0, FS = null, SQ = null; const orig = new Map(Object.entries(files));
  try {
    const { loadMicroPython } = await __mpyFactory();
    let si = 0; const sin = new TextEncoder().encode(stdin || '');
    const mp = await loadMicroPython({ url: wasm, heapsize: heap, linebuffer: false,
      stdout: b => { for (const x of b) outB.push(x); if (outB.length > 4096) flush(); },
      stderr: b => { for (const x of b) errB.push(x); if (errB.length > 4096) flush(); },
      stdin: () => si < sin.length ? sin[si++] : null });
    FS = mp.FS;
    const mk = p => { const parts = p.split('/').filter(Boolean); let cur = ''; for (const s of parts) { cur += '/' + s; try { FS.mkdir(cur); } catch {} } };
    for (const d of dirs) if (d !== '/') mk(d);
    for (const [p, data] of orig) { mk(p.slice(0, p.lastIndexOf('/')) || '/'); FS.writeFile(p, data); }
    try { FS.chdir(cwd); } catch {}
    const scriptDir = argv[0] && argv[0].startsWith('/') ? argv[0].slice(0, argv[0].lastIndexOf('/')) || '/' : cwd;
    try { mp.runPython(compat); } catch (e) {}
    if (sqliteModule && typeof __jvSqliteBridge === 'function') { SQ = __jvSqliteBridge(__jvSqlite(sqliteModule), FS); mp.registerJsModule('_jvsqlite', SQ); try { mp.runPython(sqliteShim); } catch (e) {} }
    mp.runPython('import sys\\nsys.argv[:] = ' + JSON.stringify(argv) + '\\nif ' + JSON.stringify(scriptDir) + ' not in sys.path: sys.path.insert(0, ' + JSON.stringify(scriptDir) + ')');
    await mp.runPythonAsync(code);
  } catch (e) {
    flush();
    const msg = String((e && e.message) || e);
    const m = /SystemExit(?::\\s*(-?\\d+))?\\s*$/.exec(msg.trim());
    if (m) exit = m[1] ? +m[1] : 0;
    else { out.push(['e', msg.endsWith('\\n') ? msg : msg + '\\n']); exit = 1; }
  }
  flush();
  try { SQ && SQ.flushAll(); } catch (e) {}
  const writes = {}, deletes = [], mkdirs = [];
  if (FS) {
    const seen = new Set();
    const walk = (dir) => {
      let names = []; try { names = FS.readdir(dir); } catch { return; }
      for (const n of names) {
        if (n === '.' || n === '..') continue;
        const p = (dir === '/' ? '' : dir) + '/' + n;
        if (/^\\/(dev|proc|home\\/web_user)(\\/|$)/.test(p) || p === '/home' && !dirs.includes('/home')) continue;
        let st; try { st = FS.stat(p); } catch { continue; }
        if (FS.isDir(st.mode)) { if (!dirs.includes(p) && p !== '/tmp') mkdirs.push(p); walk(p); }
        else { seen.add(p); const data = FS.readFile(p); const o = orig.get(p); if (!o || o.length !== data.length || o.some((x, i) => x !== data[i])) writes[p] = data; }
      }
    };
    walk('/');
    for (const p of orig.keys()) if (!seen.has(p)) deletes.push(p);
  }
  self.postMessage({ out, writes, deletes, mkdirs, code: exit });
};`;var It=`
self.onmessage = (ev) => {
  const { module, argv, stdin, dbBytes, files } = ev.data;
  try {
    const S = __jvSqlite(module);
    const r = S.cli({ argv, stdin, dbBytes, readFile: p => files[p] ?? null });
    self.postMessage(r, r.dbBytes ? [r.dbBytes.buffer] : []);
  } catch (e) { self.postMessage({ out: '', err: 'sqlite3: ' + ((e && e.message) || e) + '\\n', code: 1 }); }
};`,Rt=`
function __jvSqliteBridge(S, FS) {
  const H = new Map(); let hid = 0;
  const abs = p => p.startsWith('/') ? p : ((FS.cwd() === '/' ? '' : FS.cwd()) + '/' + p);
  const b64 = u => { let s = ''; for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); return btoa(s); };
  const enc = v => v instanceof Uint8Array ? { $b: b64(v) } : typeof v === 'bigint' ? { $i: v.toString() } : v;
  const revive = (k, v) => v && typeof v === 'object' && !Array.isArray(v) ? (typeof v.$b === 'string' ? Uint8Array.from(atob(v.$b), c => c.charCodeAt(0)) : typeof v.$i === 'string' ? BigInt(v.$i) : v) : v;
  const flush = (h) => { const x = H.get(h); if (x && x.fp && x.d.dirty) { FS.writeFile(x.fp, x.d.export()); x.d.dirty = false; } return 0; };
  return {
    version: () => S.version,
    open: (path) => { const p = String(path); let fp = null, bytes = null; if (p && p !== ':memory:') { fp = abs(p); try { bytes = FS.readFile(fp); } catch (e) {} } const d = new S.Database(bytes); H.set(++hid, { d, fp }); return hid; },
    execute: (h, sql, pj) => { const x = H.get(h); try { const params = pj ? JSON.parse(pj, revive) : null; let cols = [], rows = [], n = 0;
        x.d.each(String(sql), st => { if (n++) throw new Error('You can only execute one statement at a time.'); cols = st.columns(); rows = st.rows(params); });
        return JSON.stringify({ cols, rows: rows.map(r => r.map(enc)), changes: x.d.changes(), lastrowid: Number(x.d.lastInsertRowid()), total: x.d.totalChanges() });
      } catch (e) { return JSON.stringify({ error: String(e.message || e) }); } },
    script: (h, sql) => { try { H.get(h).d.exec(String(sql)); return '{}'; } catch (e) { return JSON.stringify({ error: String(e.message || e) }); } },
    flush,
    close: (h) => { flush(h); const x = H.get(h); if (x) { x.d.close(); H.delete(h); } return 0; },
    flushAll: () => { for (const h of H.keys()) flush(h); return 0; },
  };
}`,Bt=`
def __jv_sqlite():
    import sys, json, binascii
    import _jvsqlite as J
    class Error(Exception): pass
    class Warning(Exception): pass
    class InterfaceError(Error): pass
    class DatabaseError(Error): pass
    class OperationalError(DatabaseError): pass
    class IntegrityError(DatabaseError): pass
    class ProgrammingError(DatabaseError): pass
    def _enc(v):
        if isinstance(v, (bytes, bytearray)):
            return {'$b': binascii.b2a_base64(bytes(v)).decode().strip()}
        return v
    def _dec(v):
        if isinstance(v, dict):
            if '$b' in v:
                return binascii.a2b_base64(v['$b'])
            if '$i' in v:
                return int(v['$i'])
        return v
    def _raise(msg):
        low = msg.lower()
        if 'constraint' in low:
            raise IntegrityError(msg)
        if 'one statement' in low or 'parameter' in low or 'values for' in low:
            raise ProgrammingError(msg)
        raise OperationalError(msg)
    def _starts(s, words):
        for w in words:
            if s.startswith(w):
                return True
        return False
    class Row:
        def __init__(self, cols, vals):
            self._c = cols
            self._v = vals
        def keys(self):
            return list(self._c)
        def __getitem__(self, k):
            if isinstance(k, str):
                lk = k.lower()
                for i, c in enumerate(self._c):
                    if c.lower() == lk:
                        return self._v[i]
                raise IndexError('No item with that key')
            return self._v[k]
        def __len__(self):
            return len(self._v)
        def __iter__(self):
            return iter(self._v)
        def __eq__(self, o):
            return isinstance(o, Row) and o._c == self._c and o._v == self._v
        def __repr__(self):
            return '<Row %r>' % (tuple(self._v),)
    class Cursor:
        def __init__(self, conn):
            self.connection = conn
            self._rows = []
            self._i = 0
            self.description = None
            self.rowcount = -1
            self.lastrowid = None
            self.row_factory = None
            self.arraysize = 1
        def execute(self, sql, params=()):
            c = self.connection
            c._check()
            if isinstance(params, dict):
                p = {}
                for k in params:
                    p[k] = _enc(params[k])
            else:
                p = [_enc(v) for v in params]
            r = json.loads(J.execute(c._h, sql, json.dumps(p) if p else ''))
            if 'error' in r:
                _raise(r['error'])
            cols = r['cols']
            rf = self.row_factory or c.row_factory
            rows = [tuple([_dec(v) for v in row]) for row in r['rows']]
            if rf is Row:
                rows = [Row(cols, list(t)) for t in rows]
            elif rf:
                rows = [rf(self, t) for t in rows]
            self._rows = rows
            self._i = 0
            self.description = tuple([(n, None, None, None, None, None, None) for n in cols]) if cols else None
            u = sql.lstrip()[:7].upper()
            self.rowcount = r['changes'] if _starts(u, ('INSERT', 'UPDATE', 'DELETE', 'REPLACE')) else -1
            if _starts(u, ('INSERT', 'REPLACE')):
                self.lastrowid = r['lastrowid']
            c.total_changes = r.get('total', c.total_changes)
            return self
        def executemany(self, sql, seq):
            n = 0
            for p in seq:
                self.execute(sql, p)
                if self.rowcount > 0:
                    n += self.rowcount
            self.rowcount = n
            return self
        def executescript(self, script):
            self.connection.executescript(script)
            return self
        def fetchone(self):
            if self._i < len(self._rows):
                self._i += 1
                return self._rows[self._i - 1]
            return None
        def fetchmany(self, size=None):
            size = size or self.arraysize
            out = self._rows[self._i:self._i + size]
            self._i += len(out)
            return out
        def fetchall(self):
            out = self._rows[self._i:]
            self._i = len(self._rows)
            return out
        def __iter__(self):
            return self
        def __next__(self):
            r = self.fetchone()
            if r is None:
                raise StopIteration
            return r
        def close(self):
            pass
    class Connection:
        def __init__(self, path):
            self._h = J.open(str(path))
            self.row_factory = None
            self.total_changes = 0
            self.isolation_level = ''
        def _check(self):
            if self._h is None:
                raise ProgrammingError('Cannot operate on a closed database.')
        def cursor(self):
            self._check()
            return Cursor(self)
        def execute(self, sql, params=()):
            return self.cursor().execute(sql, params)
        def executemany(self, sql, seq):
            return self.cursor().executemany(sql, seq)
        def executescript(self, script):
            self._check()
            r = json.loads(J.script(self._h, script))
            if 'error' in r:
                _raise(r['error'])
            return self.cursor()
        def commit(self):
            self._check()
            J.flush(self._h)
        def rollback(self):
            pass
        def close(self):
            if self._h is not None:
                J.close(self._h)
                self._h = None
        def __enter__(self):
            return self
        def __exit__(self, t, v, tb):
            if t is None:
                self.commit()
            return False
    class _Mod:
        pass
    m = _Mod()
    m.Error = Error
    m.Warning = Warning
    m.InterfaceError = InterfaceError
    m.DatabaseError = DatabaseError
    m.OperationalError = OperationalError
    m.IntegrityError = IntegrityError
    m.ProgrammingError = ProgrammingError
    m.Row = Row
    m.Cursor = Cursor
    m.Connection = Connection
    def connect(database, *a, **k):
        return Connection(database)
    m.connect = connect
    m.sqlite_version = J.version()
    m.version = '2.6.0'
    m.PARSE_DECLTYPES = 1
    m.PARSE_COLNAMES = 2
    m.paramstyle = 'qmark'
    sys.modules['sqlite3'] = m
try:
    __jv_sqlite()
except Exception as e:
    print('sqlite3 module failed to load:', e)
del __jv_sqlite
`;var ht="1.27.0",Le=class{constructor({vfs:e,sqlite:t=null,cdn:n="https://cdn.jsdelivr.net/npm/"}){this.vfs=e,this.sqlite=t,this.base=`${n}@micropython/micropython-webassembly-pyscript@${ht}/`,this._p=null}load(){return this._p||(this._p=(async()=>{let[e,t]=await Promise.all([ye(this.base+"micropython.mjs","MicroPython"),ie(this.base+"micropython.wasm","MicroPython")]);if(!e||!Ot(t))throw new Error(`MicroPython ${ht} downloaded incomplete (${t.length} bytes of wasm)`);return{factory:Ft(e,this.base),wasm:"data:application/wasm;base64,"+le(t)}})().catch(e=>{throw this._p=null,e}))}async run(e,{argv:t=[""],cwd:n="/",stdin:i="",timeoutMs:h=6e4,heapMB:o=16,signal:l=null}={}){let p;try{p=await this.load()}catch(E){return{stdout:"",stderr:`python: ${E.message}
`,output:`python: ${E.message}
`,code:1}}let S=this.vfs,x={},k=[];for(let[E,$]of S.nodes)$.dir?k.push(E):$.data.length<4e6&&(x[E]=$.data);let j=null;if(this.sqlite&&(/sqlite/i.test(e)||[...S.nodes].some(([E,$])=>!$.dir&&E.endsWith(".py")&&$.data.length<2e6&&/sqlite/i.test(K.decode($.data)))))try{j=await this.sqlite.module()}catch(E){return{stdout:"",stderr:`python: could not load SQLite (${E.message})
`,code:1}}let q=j?p.factory+this.sqlite.glueSource+`
`+Rt+`
`+ut:p.factory+ut,y=await Ve(q,{sqliteModule:j,sqliteShim:Bt,compat:Nt,wasm:p.wasm,files:x,dirs:k,cwd:n,argv:t,code:String(e),stdin:i,heap:o*1024*1024},{timeoutMs:h,signal:l,name:"python"});if(y.error)return{stdout:"",stderr:`python: ${y.error}
`,output:`python: ${y.error}
`,code:y.timeout?124:y.aborted?130:1};let A=[];S.applyChanges({deletes:y.deletes||[],mkdirs:y.mkdirs||[],writes:y.writes||{}},E=>A.push(`python: ${E.message}
`));let T=y.out||[];return{stdout:T.filter(E=>E[0]==="o").map(E=>E[1]).join(""),stderr:T.filter(E=>E[0]==="e").map(E=>E[1]).join("")+A.join(""),output:T.map(E=>E[1]).join(""),code:y.code??1}}command(){return async e=>{let t=e.argv,n,i;if(t[0]==="--version"||t[0]==="-V")return e.o(`MicroPython ${ht} (WebAssembly)
`),0;if(t[0]==="-m"&&t[1]==="pip")return e.e(`pip is not available: MicroPython runs in the browser and has no package installer.
`),1;if(t[0]==="-c")n=t[1]??"",i=["-c",...t.slice(2)];else if(t.length&&t[0]!=="-"){let o=e.P(t[0]);if(!this.vfs.isFile(o))return e.e(`python: can't open file '${t[0]}': No such file
`),2;n=this.vfs.read(o),i=[o,...t.slice(1)]}else n=e.stdin,i=[""];if(!String(n).trim())return e.e(`python: no script given. Use python file.py or python -c "code"
`),2;let h=await this.run(n,{argv:i,cwd:e.sh.cwd,stdin:t[0]==="-c"||t.length&&t[0]!=="-"?e.stdin:"",timeoutMs:e.sh.timeoutMs});return e.o(h.stdout),e.e(h.stderr),h.code}}};function pt(g){let e=null,t={wasi_snapshot_preview1:{clock_time_get(w,d,c){return new DataView(e.buffer).setBigUint64(c,BigInt(Date.now())*1000000n,!0),0},fd_close(){return 8},fd_seek(){return 8},fd_write(w,d,c,u){let _=0,b=new DataView(e.buffer);for(let v=0;v<c;v++)_+=b.getUint32(d+v*8+4,!0);return b.setUint32(u,_,!0),0},fd_prestat_get(){return 8},fd_prestat_dir_name(){return 8},proc_exit(w){throw new Error("sqlite exited ("+w+")")},random_get(w,d){let c=new Uint8Array(e.buffer,w,d);for(let u=0;u<d;u+=65536)crypto.getRandomValues(c.subarray(u,Math.min(d,u+65536)));return 0}}},i=new WebAssembly.Instance(g,t).exports;e=i.memory,i._initialize(),i.sqlite3_initialize();let h=new TextEncoder,o=new TextDecoder,l=()=>new Uint8Array(e.buffer),p=()=>new DataView(e.buffer),S=w=>{if(!w)return null;let d=l(),c=w;for(;d[c];)c++;return o.decode(d.subarray(w,c))},x=w=>{let d=i.jv_malloc(Math.max(1,w));if(!d)throw new Error("out of memory");return d},k=(w,d)=>{let c=h.encode(String(w)),u=x(c.length+1);l().set(c,u),l()[u+c.length]=0;try{return d(u,c.length)}finally{i.jv_free(u)}},j=0,q=100,y=101,A=-1,T=S(i.sqlite3_libversion());class E extends Error{constructor(d,c){super(d),this.code=c,this.name="SqliteError"}}class ${constructor(d,c,u){this.db=d,this.p=c,this.sql=u,this.readonly=!!i.sqlite3_stmt_readonly(c)}columns(){let d=i.sqlite3_column_count(this.p),c=[];for(let u=0;u<d;u++)c.push(S(i.sqlite3_column_name(this.p,u)));return c}bind(d){if(i.sqlite3_reset(this.p),i.sqlite3_clear_bindings(this.p),d==null)return this;let c=i.sqlite3_bind_parameter_count(this.p),u=(_,b)=>{let v;if(b==null)v=i.sqlite3_bind_null(this.p,_);else if(typeof b=="bigint")v=i.sqlite3_bind_int64(this.p,_,b);else if(typeof b=="boolean")v=i.sqlite3_bind_int64(this.p,_,b?1n:0n);else if(typeof b=="number")v=Number.isSafeInteger(b)?i.sqlite3_bind_int64(this.p,_,BigInt(b)):i.sqlite3_bind_double(this.p,_,b);else if(b instanceof Uint8Array||b instanceof ArrayBuffer){let O=b instanceof Uint8Array?b:new Uint8Array(b),B=x(O.length);l().set(O,B),v=i.sqlite3_bind_blob(this.p,_,B,O.length,A),i.jv_free(B)}else v=k(typeof b=="object"?JSON.stringify(b):b,(O,B)=>i.sqlite3_bind_text(this.p,_,O,B,A));if(v!==j)throw this.db.err(v)};if(Array.isArray(d)){if(d.length>c)throw new E(`${d.length} values for ${c} parameters`,25);d.forEach((_,b)=>u(b+1,_))}else if(typeof d=="object"&&!(d instanceof Uint8Array))for(let[_,b]of Object.entries(d)){let v=0;for(let O of/^[:@$?]/.test(_)?[""]:[":","@","$"])if(v=k(O+_,B=>i.sqlite3_bind_parameter_index(this.p,B)),v)break;if(!v)throw new E(`no parameter named ${_}`,25);u(v,b)}else u(1,d);return this}value(d){switch(i.sqlite3_column_type(this.p,d)){case 1:{let c=i.sqlite3_column_int64(this.p,d);return c>=BigInt(Number.MIN_SAFE_INTEGER)&&c<=BigInt(Number.MAX_SAFE_INTEGER)?Number(c):c}case 2:return i.sqlite3_column_double(this.p,d);case 3:{let c=i.sqlite3_column_text(this.p,d),u=i.sqlite3_column_bytes(this.p,d);return o.decode(l().subarray(c,c+u))}case 4:{let c=i.sqlite3_column_blob(this.p,d),u=i.sqlite3_column_bytes(this.p,d);return l().slice(c,c+u)}default:return null}}step(){let d=i.sqlite3_step(this.p);if(d===q)return!0;if(d===y)return this.readonly||(this.db.dirty=!0),!1;throw this.db.err(d)}row(){let d=i.sqlite3_data_count(this.p),c=[];for(let u=0;u<d;u++)c.push(this.value(u));return c}*iterate(d){for(this.bind(d);this.step();)yield this.row()}rows(d){return[...this.iterate(d)]}finalize(){this.p&&(i.sqlite3_finalize(this.p),this.p=0)}}class s{constructor(d){if(this.p=k(":memory:",c=>{let u=x(4);try{let _=i.sqlite3_open_v2(c,u,6,0),b=p().getUint32(u,!0);if(_!==j)throw new E("cannot open database",_);return b}finally{i.jv_free(u)}}),this.dirty=!1,d&&d.length){let c=d.length,u=i.sqlite3_malloc64(BigInt(c));if(l().set(d,u),k("main",b=>i.sqlite3_deserialize(this.p,b,u,BigInt(c),BigInt(c),3))!==j)throw new E("file is not a database",26);try{this.exec("SELECT count(*) FROM sqlite_schema")}catch{throw new E("file is not a database",26)}}}err(d){return new E(S(i.sqlite3_errmsg(this.p))||`SQLite error ${d}`,i.sqlite3_extended_errcode(this.p))}each(d,c){let u=h.encode(String(d)),_=x(u.length+1);l().set(u,_),l()[_+u.length]=0;let b=x(4),v=x(4),O=_,B=_+u.length;try{for(;O<B;){let L=i.sqlite3_prepare_v2(this.p,O,B-O,b,v);if(L!==j)throw this.err(L);let D=p().getUint32(b,!0),N=p().getUint32(v,!0);if(D){let U=new $(this,D,o.decode(l().subarray(O,N)).trim());try{c(U)}finally{U.finalize()}}if(N<=O)break;O=N}}finally{i.jv_free(b),i.jv_free(v),i.jv_free(_)}}exec(d,c){let u=[],_=!0;return this.each(d,b=>{let v={columns:b.columns(),values:b.rows(_?c:null)};_=!1,v.columns.length&&u.push(v)}),u}prepare(d){let c=x(4);try{let u=k(d,(b,v)=>i.sqlite3_prepare_v2(this.p,b,v,c,0));if(u!==j)throw this.err(u);let _=p().getUint32(c,!0);if(!_)throw new E("empty statement",21);return new $(this,_,d)}finally{i.jv_free(c)}}changes(){return i.sqlite3_changes(this.p)}totalChanges(){return i.sqlite3_total_changes(this.p)}lastInsertRowid(){let d=i.sqlite3_last_insert_rowid(this.p);return d<=BigInt(Number.MAX_SAFE_INTEGER)?Number(d):d}inTransaction(){return!i.sqlite3_get_autocommit(this.p)}export(){let d=x(8);try{let c=k("main",b=>i.sqlite3_serialize(this.p,b,d,0)),u=Number(p().getBigInt64(d,!0));if(!c)return new Uint8Array(0);let _=l().slice(c,c+u);return i.sqlite3_free(c),_}finally{i.jv_free(d)}}close(){this.p&&(i.sqlite3_close_v2(this.p),this.p=0)}}let r=w=>k(w,d=>i.sqlite3_complete(d))!==0;function a({argv:w,stdin:d,readFile:c,dbBytes:u}){let _="",b="",v=0,O="list",B=!1,L="|",D="",N=!1,U=!1,P=null,z=[],Y=[],W=M=>{_+=M},V=M=>{b+=M},ke={"-json":"json","-csv":"csv","-column":"column","-box":"box","-table":"table","-markdown":"markdown","-line":"line","-list":"list","-html":"html","-tabs":"tabs","-quote":"quote"};for(let M=0;M<w.length;M++){let F=w[M].replace(/^--/,"-");if(ke[F])O=ke[F],["csv","tabs"].includes(O)&&(L=O==="csv"?",":"	"),["column","box","table","markdown"].includes(O)&&(B=!0);else if(F==="-header"||F==="-headers")B=!0;else if(F==="-noheader")B=!1;else if(F==="-separator")L=w[++M]??"|";else if(F==="-nullvalue")D=w[++M]??"";else if(F==="-cmd")z.push(w[++M]??"");else if(F==="-bail")N=!0;else if(F==="-readonly")U=!0;else{if(F==="-version")return W(T+`
`),{out:_,err:b,code:0};if(F==="-help")return W(m),{out:_,err:b,code:0};if(F.startsWith("-")&&F.length>1)return V(`sqlite3: unknown option: ${w[M]}
Use -help for a list of options.
`),{out:_,err:b,code:1};P===null?P=w[M]:Y.push(w[M])}}let I;try{I=new s(P&&P!==":memory:"?u:null)}catch(M){return V(`Error: unable to open database "${P}": ${M.message}
`),{out:_,err:b,code:1}}let me=!1,X=!1,Z=M=>M===null?D:M instanceof Uint8Array?O==="json"||O==="quote"?"X'"+[...M].map(F=>F.toString(16).padStart(2,"0")).join("")+"'":o.decode(M):typeof M=="bigint"?M.toString():String(M),kt=M=>/[",\n\r]/.test(M)||M!==M.trim()?'"'+M.replace(/"/g,'""')+'"':M,$t=M=>M===null?"NULL":typeof M=="number"||typeof M=="bigint"?String(M):M instanceof Uint8Array?"X'"+[...M].map(F=>F.toString(16).padStart(2,"0")).join("")+"'":"'"+String(M).replace(/'/g,"''")+"'",Kt=(M,F)=>{if(M.length){if(O==="json"){if(!F.length)return;W("["+F.map(R=>"{"+M.map((C,Q)=>JSON.stringify(C)+":"+(R[Q]instanceof Uint8Array?JSON.stringify(Z(R[Q])):typeof R[Q]=="bigint"?R[Q].toString():JSON.stringify(R[Q]))).join(",")+"}").join(`,
`)+`]
`);return}if(O==="line"){let R=Math.max(...M.map(C=>C.length));F.forEach((C,Q)=>{Q&&W(`
`),M.forEach((ee,re)=>W(ee.padStart(R)+" = "+Z(C[re])+`
`))});return}if(O==="csv"){B&&W(M.map(kt).join(L)+`\r
`);for(let R of F)W(R.map(C=>C===null?"":kt(Z(C))).join(L)+`\r
`);return}if(O==="quote"){B&&W(M.map(R=>"'"+R+"'").join(",")+`
`);for(let R of F)W(R.map($t).join(",")+`
`);return}if(O==="html"){B&&W("<TR>"+M.map(R=>`<TH>${R}</TH>`).join("")+`
</TR>
`);for(let R of F)W("<TR>"+R.map(C=>`<TD>${Z(C).replace(/&/g,"&amp;").replace(/</g,"&lt;")}</TD>`).join("")+`
</TR>
`);return}if(["column","box","table","markdown"].includes(O)){let R=F.map(H=>H.map(G=>Z(G).replace(/\n/g," "))),C=M.map((H,G)=>Math.max(H.length,...R.map(oe=>(oe[G]||"").length))),Q=M.map((H,G)=>F.length&&F.every(oe=>oe[G]===null||typeof oe[G]=="number"||typeof oe[G]=="bigint")),ee=(H,G)=>Q[G]?H.padStart(C[G]):H.padEnd(C[G]);if(O==="column"){W(M.map((H,G)=>H.padEnd(C[G])).join("  ").trimEnd()+`
`+C.map(H=>"-".repeat(H)).join("  ")+`
`);for(let H of R)W(H.map(ee).join("  ").trimEnd()+`
`);return}if(O==="markdown"){W("| "+M.map((H,G)=>H.padEnd(C[G])).join(" | ")+` |
|`+C.map((H,G)=>Q[G]?"-".repeat(H+1)+":":":"+"-".repeat(H+1)).join("|")+`|
`);for(let H of R)W("| "+H.map(ee).join(" | ")+` |
`);return}let[re,we,Je,st,nt,He,te,$e,Ee,fe,ge]=O==="box"?["\u250C","\u252C","\u2510","\u251C","\u253C","\u2524","\u2514","\u2534","\u2518","\u2500","\u2502"]:["+","+","+","+","+","+","+","+","+","-","|"],rt=(H,G,oe)=>H+C.map(Gt=>fe.repeat(Gt+2)).join(G)+oe+`
`;W(rt(re,we,Je)+ge+M.map((H,G)=>" "+H.padEnd(C[G])+" ").join(ge)+ge+`
`+rt(st,nt,He));for(let H of R)W(ge+H.map((G,oe)=>" "+ee(G,oe)+" ").join(ge)+ge+`
`);W(rt(te,$e,Ee));return}B&&W(M.join(L)+`
`);for(let R of F)W(R.map(Z).join(O==="tabs"?"	":L)+`
`)}},ze=M=>{try{I.each(M,F=>{if(U&&!F.readonly)throw new E("attempt to write a readonly database",8);let R=F.columns(),C=F.rows();Kt(R,C),me&&!F.readonly&&W(`changes: ${I.changes()}   total_changes: ${I.totalChanges()}
`)})}catch(F){V(`${/syntax error|incomplete input|unrecognized token/.test(F.message)?"Parse error":"Runtime error"}: ${F.message}
`),v=1,N&&(X=!0)}},Et=M=>I.exec(`SELECT name FROM sqlite_schema WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ${M?"AND name LIKE ?":""} ORDER BY 1`,M?[M]:null)[0]?.values.map(F=>F[0])||[],tt=M=>{let F=(M.match(/"[^"]*"|'[^']*'|\S+/g)||[]).map(C=>C.replace(/^["']|["']$/g,"")),R=F[0].slice(1);if(R==="quit"||R==="exit"){X=!0;return}if(R==="tables"){let C=Et(F[1]);C.length&&W(C.join("  ")+`
`);return}if(R==="schema"||R==="fullschema"){let C=I.exec(`SELECT sql FROM sqlite_schema WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' ${F[1]?"AND (name LIKE ?1 OR tbl_name LIKE ?1)":""} ORDER BY tbl_name, type DESC, name`,F[1]?[F[1]]:null)[0];for(let[Q]of C?.values||[])W(Q+`;
`);return}if(R==="indexes"||R==="indices"){let C=I.exec(`SELECT name FROM sqlite_schema WHERE type='index' ${F[1]?"AND tbl_name LIKE ?":""} ORDER BY 1`,F[1]?[F[1]]:null)[0];C&&W(C.values.map(Q=>Q[0]).join("  ")+`
`);return}if(R==="mode"){let C=F[1]||"list";if(!["list","csv","json","line","column","box","table","markdown","html","tabs","quote"].includes(C)){V(`Error: mode should be one of: box column csv html json line list markdown quote table tabs
`),v=1;return}O=C,C==="csv"?L=",":C==="tabs"?L="	":C==="list"&&(L="|"),["column","box","table","markdown"].includes(C)&&(B=!0);return}if(R==="headers"||R==="header"){B=/^(on|1|yes|true)$/i.test(F[1]||"");return}if(R==="separator"){L=(F[1]??"|").replace(/\\t/g,"	").replace(/\\n/g,`
`);return}if(R==="nullvalue"){D=F[1]??"";return}if(R==="changes"){me=/^(on|1|yes|true)$/i.test(F[1]||"");return}if(R==="bail"){N=/^(on|1|yes|true)$/i.test(F[1]||"");return}if(R==="databases"){W(`main: ${P&&P!==":memory:"?P:'""'} r${U?"o":"w"}
`);return}if(R==="print"){W(F.slice(1).join(" ")+`
`);return}if(R==="read"){let C=c(F[1]);if(C==null){V(`Error: cannot open "${F[1]}"
`),v=1;return}jt(C);return}if(R==="import"){let C=F.filter(te=>te.startsWith("--")),Q=F.slice(1).filter(te=>!te.startsWith("--")),[ee,re]=Q,we=c(ee);if(we==null){V(`Error: cannot open "${ee}"
`),v=1;return}let Je=f(we,O==="tabs"||C.includes("--tabs")?"	":",");if(!Je.length)return;let st=+(C.find(te=>te.startsWith("--skip"))?.split("=")[1]||0),nt=Et(re).includes(re),He=Je.slice(st);try{if(!nt){let Ee=He.shift();I.exec(`CREATE TABLE "${re.replace(/"/g,'""')}"(${Ee.map(fe=>'"'+String(fe).replace(/"/g,'""')+'" TEXT').join(", ")})`),I.dirty=!0}let te=I.exec("SELECT count(*) FROM pragma_table_info(?)",[re])[0].values[0][0],$e=I.prepare(`INSERT INTO "${re.replace(/"/g,'""')}" VALUES(${Array(te).fill("?").join(",")})`);try{I.exec("BEGIN");for(let Ee of He){let fe=Ee.slice(0,te);for(;fe.length<te;)fe.push(null);$e.bind(fe),$e.step()}I.exec("COMMIT")}finally{$e.finalize()}I.dirty=!0}catch(te){try{I.exec("ROLLBACK")}catch{}V(`Error: ${te.message}
`),v=1}return}if(R==="dump"){W(`PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
`);let C=I.exec(`SELECT type, name, sql FROM sqlite_schema WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' ${F[1]?"AND tbl_name LIKE ?":""} ORDER BY type='table' DESC, rowid`,F[1]?[F[1]]:null)[0]?.values||[];for(let[Q,ee,re]of C)if(Q==="table"){W(re+`;
`);for(let we of I.exec(`SELECT * FROM "${ee.replace(/"/g,'""')}"`)[0]?.values||[])W(`INSERT INTO ${/^[A-Za-z_]\w*$/.test(ee)?ee:'"'+ee+'"'} VALUES(${we.map($t).join(",")});
`)}for(let[Q,,ee]of C)Q!=="table"&&W(ee+`;
`);W(`COMMIT;
`);return}if(R==="help"){W(m);return}V(`Error: unknown command or invalid arguments: "${R}". Enter ".help" for help
`),v=1},de="";function jt(M){for(let F of String(M).split(/\r?\n/)){if(X)return;if(!de.trim()&&/^\s*\./.test(F)){tt(F.trim());continue}de+=F+`
`,r(de)&&(ze(de),de="")}}for(let M of z){if(X)break;/^\s*\./.test(M)?tt(M.trim()):ze(M)}if(Y.length)for(let M of Y){if(X)break;/^\s*\./.test(M)?tt(M.trim()):ze(M)}else if(d&&d.trim())jt(d),de.trim()&&!X&&ze(de);else if(!z.length)return V(`sqlite3: no SQL given. Use: sqlite3 FILE "SQL" | sqlite3 FILE < script.sql | echo "SQL" | sqlite3 FILE
`),I.close(),{out:_,err:b,code:1};let qt={out:_,err:b,code:v};return I.dirty&&P&&P!==":memory:"&&!U&&(qt.dbBytes=I.export()),I.close(),qt}function f(w,d){let c=[],u=[],_="",b=!1;for(let v=0;v<w.length;v++){let O=w[v];if(b){O==='"'?w[v+1]==='"'?(_+='"',v++):b=!1:_+=O;continue}if(O==='"'&&_===""){b=!0;continue}if(O===d){u.push(_),_="";continue}if(O===`
`||O==="\r"){O==="\r"&&w[v+1]===`
`&&v++,u.push(_),_="",(u.length>1||u[0]!=="")&&c.push(u),u=[];continue}_+=O}return(_!==""||u.length)&&(u.push(_),c.push(u)),c}let m=`SQLite ${T} shell (batch mode)
usage: sqlite3 [OPTIONS] [FILE] ["SQL" ...]      (SQL can also come from stdin or < file.sql)
options: -json -csv -column -box -table -markdown -line -list -html -tabs -quote
         -header -noheader -separator SEP -nullvalue TEXT -cmd CMD -bail -readonly -version
dot commands: .tables [pat]  .schema [table]  .indexes [table]  .mode MODE  .headers on|off
              .separator SEP  .nullvalue TEXT  .import FILE TABLE [--skip=N]  .read FILE
              .dump [table]  .changes on|off  .bail on|off  .databases  .print TEXT  .quit
`;return{Database:s,Statement:$,SqliteError:E,version:T,complete:r,cli:a,parseCsv:f}}var mt="var __jvSqlite = "+pt.toString()+";";var Me=class{constructor(e,t,n,{readOnly:i=!1}={}){this.vfs=t,this.path=n?t.norm(n):null,this.readOnly=i;let h=null;if(this.path&&t.isFile(this.path)&&(h=t.readBytes(this.path),h.length&&!_e(h)))throw new Error(`file is not a database: ${this.path}`);this.db=new e.Database(h)}exec(e,t){return this.db.exec(e,t??null)}query(e,t){let n=this.db.prepare(e);try{let i=n.columns();return n.rows(t??null).map(h=>Object.fromEntries(i.map((o,l)=>[o,h[l]])))}finally{n.finalize()}}get(e,t){return this.query(e,t)[0]}run(e,t){let n=this.db.prepare(e);try{for(n.bind(t??null);n.step(););}finally{n.finalize()}return{changes:this.db.changes(),lastInsertRowid:this.db.lastInsertRowid()}}transaction(e){this.db.exec("BEGIN");try{let t=e(this);return this.db.exec("COMMIT"),t}catch(t){try{this.db.exec("ROLLBACK")}catch{}throw t}}prepare(e){return this.db.prepare(e)}export(){return this.db.export()}save(e=this.path){if(!e)throw new Error("this database has no path: pass one to save(path)");if(this.readOnly)throw new Error("the database is read-only");return this.vfs.write(e,this.db.export()),this.path=this.vfs.norm(e),this.path}close({save:e=!0}={}){this.db&&(e&&this.path&&!this.readOnly&&this.save(),this.db.close(),this.db=null)}},De=class{constructor(e){this.vfs=e,this._mod=null,this._api=null,this.glueSource=mt}module(){return this._mod||(this._mod=ie(je("sqlite3.wasm"),"SQLite").then(e=>WebAssembly.compile(e)).catch(e=>{throw this._mod=null,e}))}async api(){return this._api||(this._api=pt(await this.module()))}async version(){return(await this.api()).version}async open(e=":memory:",t={}){return new Me(await this.api(),this.vfs,e===":memory:"?null:e,t)}async cli(e,{stdin:t="",cwd:n="/",timeoutMs:i=6e4}={}){let h=this.vfs,o=null;for(let q=0;q<e.length;q++){let y=e[q];if(["-separator","--separator","-nullvalue","--nullvalue","-cmd","--cmd"].includes(y)){q++;continue}if(!y.startsWith("-")){o=y;break}}let l=o&&o!==":memory:"?h.norm(o,n):null;if(l&&h.isDir(l))return{stdout:"",stderr:`Error: unable to open database "${o}": it is a directory
`,code:1};let p=l&&h.isFile(l)?h.readBytes(l):null;if(p&&p.length&&!_e(p))return{stdout:"",stderr:`Error: file is not a database: ${o}
`,code:1};let S={},x=[t,...e].join(`
`);for(let q of x.matchAll(/^\s*\.(?:import|read)\s+(.+)$/gm))for(let y of q[1].match(/"[^"]*"|'[^']*'|\S+/g)||[]){let A=y.replace(/^["']|["']$/g,"");if(A.startsWith("--"))continue;let T=h.norm(A,n);h.isFile(T)&&(S[A]=h.read(T))}let k;try{k=await this.module()}catch(q){return{stdout:"",stderr:`sqlite3: could not load SQLite (${q.message})
`,code:1}}let j=await Ve(mt+`
`+It,{module:k,argv:e,stdin:t,dbBytes:p,files:S},{timeoutMs:i,name:"sqlite3"});return j.error?{stdout:"",stderr:`sqlite3: ${j.error}
`,code:j.timeout?124:1}:(j.dbBytes&&l&&h.write(l,new Uint8Array(j.dbBytes)),{stdout:j.out||"",stderr:j.err||"",code:j.code??1})}command(){return async e=>{let t=await this.cli(e.argv,{stdin:e.stdin,cwd:e.sh.cwd,timeoutMs:e.sh.timeoutMs});return e.o(t.stdout),e.e(t.stderr),t.code}}};var ss=new Set("a an and are as at be but by for from had has have he her his i if in into is it its me my of on or our she so that the their them then there they this to was we were what when where which who will with you your do does did can could would should not no yes".split(" "));function Fe(g,{stopWords:e=ss,stem:t=!0}={}){let n=[];for(let i of String(g??"").toLowerCase().split(/[^\p{L}\p{N}]+/u))i.length<2||e?.has(i)||(t&&i.length>4&&/[a-z]$/.test(i)&&(i=i.replace(/(ing|ed|es|s)$/,"")),n.push(i));return n}var ae=class{constructor(e=[],{k1:t=1.5,b:n=.75,epsilon:i=.25,tokenize:h=Fe}={}){this.k1=t,this.b=n,this.epsilon=i,this.tok=h,this.docs=[],this.add(e)}add(e){for(let t of e){let n=this.docs.length;this.docs.push(typeof t=="string"?{id:n,text:t}:{...t,id:t.id??n})}return this._build(),this}_build(){let e=this.docs.map(o=>this.tok(o.text??""));this.N=e.length,this.tf=e.map(o=>{let l=new Map;for(let p of o)l.set(p,(l.get(p)||0)+1);return l}),this.len=e.map(o=>o.length),this.avgdl=this.N?this.len.reduce((o,l)=>o+l,0)/this.N:0;let t=new Map;for(let o of this.tf)for(let l of o.keys())t.set(l,(t.get(l)||0)+1);this.idf=new Map;let n=0,i=[];for(let[o,l]of t){let p=Math.log((this.N-l+.5)/(l+.5));this.idf.set(o,p),n+=p,p<0&&i.push(o)}let h=Math.max(this.epsilon*(t.size?n/t.size:0),.01);for(let o of i)this.idf.set(o,h)}scores(e){let t=Array.isArray(e)?e:this.tok(e),n=new Array(this.N).fill(0);for(let i of new Set(t)){let h=this.idf.get(i);if(h!==void 0)for(let o=0;o<this.N;o++){let l=this.tf[o].get(i);l&&(n[o]+=h*(l*(this.k1+1))/(l+this.k1*(1-this.b+this.b*this.len[o]/(this.avgdl||1))))}}return n}search(e,{limit:t=10,minScore:n=0}={}){return this.scores(e).map((h,o)=>({...this.docs[o],score:h})).filter(h=>h.score>n).sort((h,o)=>o.score-h.score).slice(0,t)}},wt=(g,e,t={})=>new ae(g,t).search(e,t);function Ne(g,e,{root:t="/",limit:n=10,maxBytes:i=1e6,include:h=/\.(md|txt|js|mjs|ts|py|json|html|css|csv|toml|ya?ml|xml|sh|sql)$/i}={}){let o=[];for(let p of g.walk(t)){if(!g.isFile(p)||!h.test(p))continue;let S=g.readBytes(p);S.length>i||o.push({id:p,path:p,text:p+`
`+new TextDecoder().decode(S)})}let l=Fe(e);return new ae(o).search(e,{limit:n}).map(({path:p,text:S,score:x})=>{let k=S.split(`
`),j=Math.max(0,k.findIndex((q,y)=>y>0&&l.some(A=>q.toLowerCase().includes(A))));return{path:p,score:+x.toFixed(4),line:j||null,snippet:k.slice(j||1,(j||1)+3).join(`
`).slice(0,300)}})}var be={tfjs:"4.22.0",onnxruntime:"1.31.1",litert:"2.5.3"};function _t(g=globalThis.navigator?.gpu){if(!g||g.__jak||typeof g.requestAdapter!="function")return;let e=g.requestAdapter.bind(g);g.requestAdapter=async t=>{let n=null;try{n=await e(t)}catch{}if(!n&&!(t&&t.featureLevel))try{n=await e({...t||{},featureLevel:"compatibility"})}catch{}if(n&&!n.__jak&&n.features?.has?.("core-features-and-limits")){let i=n.requestDevice.bind(n);n.requestDevice=(h={})=>i({...h,requiredFeatures:[...new Set([...h.requiredFeatures||[],"core-features-and-limits"])]}),n.__jak=!0}return n},g.__jak=!0}var Ct={float32:Float32Array,int32:Int32Array,uint8:Uint8Array,int8:Int8Array,float64:Float64Array,int16:Int16Array,uint16:Uint16Array},gt=(g,e=[])=>{if(Array.isArray(g))for(let t of g)gt(t,e);else e.push(+g);return e},Ut=g=>{let e=[];for(;Array.isArray(g);)e.push(g.length),g=g[0];return e},Ie=class{constructor({vfs:e,cdn:t="https://cdn.jsdelivr.net/npm/"}){this.vfs=e,this.cdn=t,this._tf=null,this._tfSrc=null,this._ort=null,this._lrt=null;try{_t()}catch{}}url(e,t,n){return`${this.cdn}${e}@${t}/${n}`}async bytes(e){if(e instanceof Uint8Array)return e;if(e instanceof ArrayBuffer)return new Uint8Array(e);let t=String(e||"");if(/^(https?:|blob:|data:)/i.test(t))return ie(t,t);if(!this.vfs.isFile(t))throw new Error(`${t} is not a file`);return this.vfs.readBytes(t)}tensorInput(e,t="float32"){if(e&&!Array.isArray(e)&&!ArrayBuffer.isView(e)&&typeof e=="object"){t=e.dtype||t;let n=e.data,i=ArrayBuffer.isView(n)?n:(Ct[t]||Float32Array).from(gt(n));return[i,e.shape||(Array.isArray(n)?Ut(n):[i.length]),t]}return ArrayBuffer.isView(e)?[e,[e.length],t]:[(Ct[t]||Float32Array).from(gt(e)),Ut(e),t]}async tf({backend:e}={}){return this._tf||(this._tf=(async()=>{let t=await Qe(this.url("@tensorflow/tfjs",be.tfjs,"dist/tf.min.js"),"tf");try{await Qe(this.url("@tensorflow/tfjs-backend-webgpu",be.tfjs,"dist/tf-backend-webgpu.min.js"))}catch{}let n=async i=>{try{return!t.findBackendFactory(i)||!await t.setBackend(i)?!1:(await t.ready(),(await t.tensor([1,2]).add(1).data())[0]===2)}catch{return!1}};for(let i of e?[e]:["webgpu","webgl","cpu"])if(await n(i))break;return t})().catch(t=>{throw this._tf=null,t}))}tfjsSource(){return this._tfSrc||(this._tfSrc=ye(this.url("@tensorflow/tfjs",be.tfjs,"dist/tf.min.js"),"TensorFlow.js").catch(e=>{throw this._tfSrc=null,e}))}ort(){return this._ort||(this._ort=(async()=>{let e=this.url("onnxruntime-web",be.onnxruntime,"dist/"),t=await Qe(e+"ort.webgpu.min.js","ort");if(!t?.InferenceSession)throw new Error("ONNX Runtime did not load");return t.env.wasm.numThreads=globalThis.crossOriginIsolated?Math.min(4,navigator.hardwareConcurrency||1):1,t.env.wasm.wasmPaths=e,t.env.logLevel="error",t})().catch(e=>{throw this._ort=null,e}))}async onnx(e,{accelerator:t}={}){let n=this,i=await this.ort(),h=await this.bytes(e),o=t||(await this.webgpu()?"webgpu":"wasm"),l,p=q=>i.InferenceSession.create(h,{executionProviders:q==="webgpu"?["webgpu","wasm"]:["wasm"],graphOptimizationLevel:"all"}),S;try{S=await p(o)}catch(q){if(o==="wasm")throw q;l=`${o} failed (${q.message}); using wasm`,o="wasm",S=await p("wasm")}let x=q=>S[q+"Names"].map((y,A)=>{let T=S[q+"Metadata"],E=Array.isArray(T)?T[A]:T?.[y];return{name:y,shape:(E?.shape||[]).map($=>typeof $=="number"?$:-1),dtype:E?.type||"float32"}}),k=x("input"),j=x("output");return{accelerator:o,note:l,inputs:k,outputs:j,session:S,async run(q){let y=Array.isArray(q)?q:k.map($=>q[$.name]??(k.length===1?q:void 0)),A={};k.forEach(($,s)=>{if(y[s]==null)throw new Error(`no data for input ${$.name}`);let[r,a,f]=n.tensorInput(y[s],y[s]?.dtype||$.dtype);if(!y[s]?.shape&&$.shape.length&&a.length!==$.shape.length&&$.shape.filter(m=>m<0).length===1){let m=$.shape.filter(w=>w>0).reduce((w,d)=>w*d,1);if(r.length%m)throw new Error(`input ${$.name} needs a multiple of ${m} values (shape ${JSON.stringify($.shape)}), got ${r.length}`);a=$.shape.map(w=>w<0?r.length/m:w)}f==="int64"?r=BigInt64Array.from(r,m=>BigInt(Math.round(Number(m)))):f==="bool"&&(r=Uint8Array.from(r,m=>m?1:0)),A[$.name]=new i.Tensor(f,r,y[s]?.shape||a)});let T=await S.run(A),E={};for(let $ of S.outputNames){let s=T[$],r=s.location&&s.location!=="cpu"?await s.getData():s.data;E[$]={data:r,shape:[...s.dims],dtype:s.type}}return E},release:()=>S.release()}}litert(){return this._lrt||(this._lrt=(async()=>{let e=await import(this.url("@litertjs/core",be.litert,"+esm"));return await e.loadLiteRt(this.url("@litertjs/core",be.litert,"wasm/")),e})().catch(e=>{throw this._lrt=null,e}))}async tflite(e,{accelerator:t}={}){let n=this,i=await this.litert(),h=await this.bytes(e),o=!1;try{o=!!await i.isWebGPUSupported?.()}catch{}let l=t||(o?"webgpu":"wasm"),p,S;try{S=await i.loadAndCompile(h,{accelerator:l})}catch(y){if(l==="wasm")throw y;p=`${l} failed (${y.message}); using wasm`,l="wasm",S=await i.loadAndCompile(h,{accelerator:"wasm"})}let x=y=>[...y?.shape||y?.layout?.dimensions||y?.dimensions||[]],k=y=>[...y].map((A,T)=>({index:T,name:A.name,shape:x(A),dtype:A.dtype||A.type?.dtype})),j=k(S.getInputDetails()),q=k(S.getOutputDetails());return{accelerator:l,note:p,inputs:j,outputs:q,model:S,async run(y){let A=Array.isArray(y)&&j.length>1||Array.isArray(y)&&(Array.isArray(y[0])||ArrayBuffer.isView(y[0])||y[0]?.data)?y:[y],T=j.map((s,r)=>{let[a,f]=n.tensorInput(A[r],s.dtype||"float32");return new i.Tensor(a,A[r]?.shape||(s.shape.length?s.shape:f))}),E;try{E=await S.run(T)}finally{T.forEach(s=>{try{s.delete()}catch{}})}let $=[];for(let[s,r]of(Array.isArray(E)?E:Object.values(E)).entries()){let a=r;if(l!=="wasm")try{let f=await a.moveTo("wasm");f&&f!==a&&(a=f)}catch{}$.push({name:q[s]?.name,data:a.toTypedArray(),shape:[...a.type?.layout?.dimensions||q[s]?.shape||[]]});try{a.delete()}catch{}}return $},delete:()=>S.delete()}}async webgpu(){if(this._gpu==null)try{this._gpu=!!(navigator.gpu&&await navigator.gpu.requestAdapter())}catch{this._gpu=!1}return this._gpu}};async function Xe(g){let e=g instanceof Uint8Array?g:new Uint8Array(g),t=new DataView(e.buffer,e.byteOffset,e.byteLength),n=-1;for(let p=e.length-22;p>=Math.max(0,e.length-65557);p--)if(t.getUint32(p,!0)===101010256){n=p;break}if(n<0)throw new Error("not a zip file (.xdc files are zip archives)");let i=t.getUint16(n+10,!0),h=t.getUint32(n+16,!0),o={},l=new TextDecoder;for(let p=0;p<i;p++){if(t.getUint32(h,!0)!==33639248)throw new Error("broken zip directory");let S=t.getUint16(h+10,!0),x=t.getUint32(h+20,!0),k=t.getUint16(h+28,!0),j=t.getUint16(h+30,!0),q=t.getUint16(h+32,!0),y=t.getUint32(h+42,!0),A=l.decode(e.subarray(h+46,h+46+k));if(h+=46+k+j+q,A.endsWith("/"))continue;let T=y+30+t.getUint16(y+26,!0)+t.getUint16(y+28,!0),E=e.subarray(T,T+x),$;if(S===0)$=E.slice();else if(S===8)$=new Uint8Array(await new Response(new Blob([E]).stream().pipeThrough(new DecompressionStream("deflate-raw"))).arrayBuffer());else throw new Error(`unsupported zip compression (${S}) for ${A}`);o[A.replace(/^\.?\//,"")]=$}return o}function Pt(g){let e={};for(let t of String(g||"").split(/\r?\n/)){let n=/^\s*([\w.-]+)\s*=\s*(?:"((?:\\.|[^"])*)"|'([^']*)'|([\w.+-]+))\s*(?:#.*)?$/.exec(t);if(n)e[n[1]]=n[2]!=null?n[2].replace(/\\"/g,'"').replace(/\\\\/g,"\\"):n[3]!=null?n[3]:/^-?\d+(\.\d+)?$/.test(n[4])?+n[4]:n[4]==="true"?!0:n[4]==="false"?!1:n[4];else if(/^\s*\[/.test(t))break}return e}var ns={html:"text/html",htm:"text/html",js:"text/javascript",mjs:"text/javascript",css:"text/css",json:"application/json",png:"image/png",jpg:"image/jpeg",jpeg:"image/jpeg",gif:"image/gif",webp:"image/webp",svg:"image/svg+xml",ico:"image/x-icon",mp3:"audio/mpeg",ogg:"audio/ogg",wav:"audio/wav",m4a:"audio/mp4",mp4:"video/mp4",webm:"video/webm",woff:"font/woff",woff2:"font/woff2",ttf:"font/ttf",otf:"font/otf",wasm:"application/wasm",txt:"text/plain",md:"text/markdown",xml:"application/xml",csv:"text/csv",toml:"text/plain"},Ze=g=>ns[(g.split(".").pop()||"").toLowerCase()]||"application/octet-stream";function ce(g,e){let t=String(e||"").trim();if(!t||/^([a-z][a-z0-9+.-]*:|\/\/|#)/i.test(t))return null;t=t.split("#")[0].split("?")[0];try{t=decodeURIComponent(t)}catch{}let n=t.startsWith("/")?[]:g.split("/").slice(0,-1);for(let i of t.split("/"))!i||i==="."||(i===".."?n.pop():n.push(i));return n.join("/")}function Wt(g,e){let t=g.files,n=y=>`data:${Ze(y)};base64,${le(t[y])}`,i=new Map,h=(y,A)=>y.replace(/@import\s+(?:url\()?\s*(['"]?)([^'")\s]+)\1\s*\)?/g,(T,E,$)=>{let s=ce(A,$);return s&&t[s]?`@import url("data:text/css;base64,${le(new TextEncoder().encode(h(K.decode(t[s]),s)))}")`:T}).replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g,(T,E,$)=>{let s=ce(A,$);return s&&t[s]?`url("${n(s)}")`:T}),o=(y,A=[])=>{if(i.has(y))return i.get(y);if(A.includes(y))return null;let T=l(K.decode(t[y]),y,[...A,y]),E=`data:text/javascript;base64,${le(new TextEncoder().encode(T))}`;return i.set(y,E),E},l=(y,A,T=[])=>y.replace(/(\bimport\s*(?:[\w$*{}\s,]+?\s*from\s*)?|\bexport\s*(?:\*(?:\s*as\s+[\w$]+)?|\{[^}]*\})\s*from\s*)(['"])([^'"\n]+)\2/g,(E,$,s,r)=>{let a=ce(A,r);if(!a||!t[a])return E;if(/\.(js|mjs)$/i.test(a)){let f=o(a,T);return f?$+s+f+s:E}return $+s+n(a)+s}).replace(/\bimport\s*\(\s*(['"])([^'"\n]+)\1\s*\)/g,(E,$,s)=>{let r=ce(A,s);if(!r||!t[r])return E;let a=/\.(js|mjs)$/i.test(r)?o(r,T):n(r);return a?`import(${$}${a}${$})`:E}).replace(/new\s+URL\(\s*(['"])([^'"\n]+)\1\s*,\s*import\.meta\.url\s*\)/g,(E,$,s)=>{let r=ce(A,s);return r&&t[r]?`new URL(${$}${n(r)}${$})`:E}),p=new DOMParser().parseFromString(K.decode(t["index.html"]),"text/html");for(let y of[...p.querySelectorAll("script")]){let A=(y.getAttribute("type")||"").toLowerCase()==="module",T=y.getAttribute("src");if(T){let E=ce("index.html",T);if(!E||!t[E]){/webxdc\.js$/.test(T)&&y.remove();continue}y.removeAttribute("src"),y.textContent=A?l(K.decode(t[E]),E,[E]):K.decode(t[E])}else A&&(y.textContent=l(y.textContent,"index.html"))}for(let y of[...p.querySelectorAll("link[href]")]){let A=(y.getAttribute("rel")||"").toLowerCase(),T=ce("index.html",y.getAttribute("href"));if(!(!T||!t[T]))if(A.includes("stylesheet")){let E=p.createElement("style");E.textContent=h(K.decode(t[T]),T),y.replaceWith(E)}else A==="modulepreload"?y.remove():y.setAttribute("href",n(T))}for(let y of p.querySelectorAll("style"))y.textContent=h(y.textContent,"index.html");for(let y of p.querySelectorAll("[style]"))y.setAttribute("style",h(y.getAttribute("style"),"index.html"));for(let y of p.querySelectorAll("img[src],audio[src],video[src],source[src],input[src],embed[src],track[src],image[href],use[href]")){let A=y.hasAttribute("src")?"src":"href",T=ce("index.html",y.getAttribute(A));T&&t[T]&&y.setAttribute(A,n(T))}let S={},x=12*1048576;for(let[y,A]of Object.entries(t))y!=="index.html"&&(A.length>x||(x-=A.length,S[y]=n(y)));let k=p.createElement("script");k.textContent=rs({app:g,assets:S,files:Object.keys(t),self:e});let j=p.createElement("meta");return j.setAttribute("http-equiv","Content-Security-Policy"),j.setAttribute("content","default-src 'self' data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src data: blob:; img-src data: blob:; media-src data: blob:; font-src data: blob:; style-src 'unsafe-inline' data: blob:; script-src 'unsafe-inline' 'unsafe-eval' data: blob:"),(p.head||p.documentElement.insertBefore(p.createElement("head"),p.body)).prepend(j,k),`<!DOCTYPE html>
`+p.documentElement.outerHTML}function rs({app:g,assets:e,files:t,self:n}){let i={addr:n.addr,name:n.name,ls:g.ls||{},assets:e,files:t,android:!!n.android};return`(() => {
const CFG = ${JSON.stringify(i).replace(/<\//g,"<\\/")};
const P = window.parent; let seq = 0; const waits = new Map(); let listener = null; const ready = [];
const post = (m) => P.postMessage(Object.assign({ __xdc: 1 }, m), '*');
const call = (t, data) => new Promise((res, rej) => { const id = ++seq; waits.set(id, { res, rej }); post({ t, id, data }); });
window.addEventListener('message', (e) => {
  if (e.source !== P || !e.data || !e.data.__xdc) return; const m = e.data;
  if (m.t === 'update') { try { listener && listener(m.update); } catch (err) { console.error(err); } }
  else if (m.t === 'listen-done') { ready.splice(0).forEach(r => r()); }
  else if (m.t === 'reply') { const w = waits.get(m.id); if (w) { waits.delete(m.id); m.error ? w.rej(new Error(m.error)) : w.res(m.data); } }
  else if (m.t === 'realtime') { rtL && rtL(new Uint8Array(m.data)); }
});
let rtL = null;
const local = (u) => { if (typeof u !== 'string') u = String(u && u.url || u); if (/^(data|blob|javascript):/i.test(u)) return null; let s = u.replace(/^about:srcdoc/, '').replace(/^https?:\\/\\/[^/]*\\.localhost\\//, '').split('#')[0].split('?')[0]; if (/^[a-z][a-z0-9+.-]*:/i.test(s)) return null; s = s.replace(/^\\.?\\//, ''); try { s = decodeURIComponent(s); } catch (e) {} return CFG.files.includes(s) ? s : null; };
window.webxdc = {
  selfAddr: CFG.addr, selfName: CFG.name, sendUpdateInterval: 1000, sendUpdateMaxSize: 128000,
  setUpdateListener(cb, serial) { listener = cb; const p = new Promise(r => ready.push(r)); post({ t: 'listen', serial: serial || 0 }); return p; },
  sendUpdate(update, descr) { post({ t: 'send', update: JSON.parse(JSON.stringify(update)), descr }); },
  getAllUpdates() { return call('all'); },
  async sendToChat(msg) {
    const out = { text: msg && msg.text || '' };
    if (msg && msg.file) { const f = msg.file; let b64 = f.base64; if (!b64 && f.plainText != null) b64 = btoa(unescape(encodeURIComponent(f.plainText))); if (!b64 && f.blob) { const u = new Uint8Array(await f.blob.arrayBuffer()); let s = ''; for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); b64 = btoa(s); } out.file = { name: f.name || 'file', base64: b64, type: f.type || (f.blob && f.blob.type) || '' }; }
    return call('chat', out);
  },
  importFiles(filter) { return new Promise((res) => { const i = document.createElement('input'); i.type = 'file'; const f = filter || {}; i.multiple = !!f.multiple; const acc = [...(f.mimeTypes || []), ...(f.extensions || [])]; if (acc.length && !(CFG.android && !(f.mimeTypes || []).length)) i.accept = acc.join(','); i.style.display = 'none'; i.onchange = () => { res([...i.files]); i.remove(); }; document.body.appendChild(i); i.click(); }); },
  joinRealtimeChannel() { post({ t: 'rt-join' }); return { setListener(f) { rtL = f; }, send(data) { post({ t: 'rt-send', data: Array.from(data || []) }); }, leave() { rtL = null; post({ t: 'rt-leave' }); } }; },
};
// storage: the frame has no origin of its own, so localStorage is kept by the app host
const mkStore = (init, persist) => { const d = Object.assign({}, init); let t = 0; const save = () => { if (!persist) return; clearTimeout(t); t = setTimeout(() => post({ t: 'ls', data: d }), 200); };
  const s = { getItem: k => Object.prototype.hasOwnProperty.call(d, k) ? d[k] : null, setItem: (k, v) => { d[k] = String(v); save(); }, removeItem: k => { delete d[k]; save(); }, clear: () => { for (const k in d) delete d[k]; save(); }, key: i => Object.keys(d)[i] ?? null, get length() { return Object.keys(d).length; } };
  return new Proxy(s, { get: (o, k) => k in o ? o[k] : (typeof k === 'string' ? s.getItem(k) : undefined), set: (o, k, v) => { s.setItem(k, v); return true; }, deleteProperty: (o, k) => { s.removeItem(k); return true; }, ownKeys: () => Object.keys(d), getOwnPropertyDescriptor: (o, k) => Object.prototype.hasOwnProperty.call(d, k) ? { value: d[k], enumerable: true, configurable: true } : undefined }); };
try { Object.defineProperty(window, 'localStorage', { value: mkStore(CFG.ls, true), configurable: true }); } catch (e) {}
try { Object.defineProperty(window, 'sessionStorage', { value: mkStore({}, false), configurable: true }); } catch (e) {}
// local files for fetch / XHR / src setters
const asset = (u) => { const p = local(u); return p ? (CFG.assets[p] || null) : null; };
const f0 = window.fetch && window.fetch.bind(window);
window.fetch = async (input, init) => { const p = local(input); if (p) { if (CFG.assets[p]) return f0(CFG.assets[p]); const r = await call('file', p); return new Response(new Uint8Array(r.bytes), { status: 200, headers: { 'Content-Type': r.type } }); } const u = String(input && input.url || input); if (/^(data|blob):/i.test(u)) return f0(input, init); throw new TypeError('webxdc apps have no internet access'); };
const xo = XMLHttpRequest.prototype.open; XMLHttpRequest.prototype.open = function (m, u, ...rest) { const a = asset(u); return xo.call(this, m, a || u, ...rest); };
for (const C of [HTMLImageElement, HTMLMediaElement, HTMLSourceElement, HTMLScriptElement]) { const d = Object.getOwnPropertyDescriptor(C.prototype, 'src'); if (d && d.set) Object.defineProperty(C.prototype, 'src', { get: d.get, set(v) { const a = asset(v); d.set.call(this, a || v); }, configurable: true }); }
const sa = Element.prototype.setAttribute; Element.prototype.setAttribute = function (k, v) { if ((k === 'src' || k === 'href') && typeof v === 'string') { const a = asset(v); if (a) v = a; } return sa.call(this, k, v); };
const A0 = window.Audio; if (A0) window.Audio = function (u) { return new A0(u ? (asset(u) || u) : u); };
window.open = (u) => { post({ t: 'open', url: String(u || '') }); return null; };
})();`}function zt(g){let e=new TextEncoder,t=[],n=[],i=0,h=(()=>{let j=new Uint32Array(256);for(let q=0;q<256;q++){let y=q;for(let A=0;A<8;A++)y=y&1?3988292384^y>>>1:y>>>1;j[q]=y>>>0}return j})(),o=j=>{let q=4294967295;for(let y=0;y<j.length;y++)q=h[(q^j[y])&255]^q>>>8;return(q^4294967295)>>>0};for(let[j,q]of Object.entries(g)){let y=e.encode(j),A=o(q),T=new DataView(new ArrayBuffer(30));T.setUint32(0,67324752,!0),T.setUint16(4,20,!0),T.setUint16(6,2048,!0),T.setUint32(14,A,!0),T.setUint32(18,q.length,!0),T.setUint32(22,q.length,!0),T.setUint16(26,y.length,!0),t.push(new Uint8Array(T.buffer),y,q);let E=new DataView(new ArrayBuffer(46));E.setUint32(0,33639248,!0),E.setUint16(4,20,!0),E.setUint16(6,20,!0),E.setUint16(8,2048,!0),E.setUint32(16,A,!0),E.setUint32(20,q.length,!0),E.setUint32(24,q.length,!0),E.setUint16(28,y.length,!0),E.setUint32(42,i,!0),n.push(new Uint8Array(E.buffer),y),i+=30+y.length+q.length}let l=n.reduce((j,q)=>j+q.length,0),p=new DataView(new ArrayBuffer(22));p.setUint32(0,101010256,!0),p.setUint16(8,Object.keys(g).length,!0),p.setUint16(10,Object.keys(g).length,!0),p.setUint32(12,l,!0),p.setUint32(16,i,!0);let S=[...t,...n,new Uint8Array(p.buffer)],x=new Uint8Array(S.reduce((j,q)=>j+q.length,0)),k=0;for(let j of S)x.set(j,k),k+=j.length;return x}var Re=class{constructor({vfs:e,persist:t=!1}){this.vfs=e,this.store=t?Ye("jade-agent-kit-xdc:"+t):null,this.apps=new Map,this.sessions=new Set,this.listeners=new Set,this._q=new Map}async load(e,{name:t="App"}={}){let n;if(e instanceof Uint8Array||e instanceof ArrayBuffer)n=await Xe(e);else if(e&&typeof e=="object")n=Object.fromEntries(Object.entries(e).map(([x,k])=>[x,typeof k=="string"?new TextEncoder().encode(k):k]));else{let x=String(e);if(/^(https?:|blob:|data:)/i.test(x))n=await Xe(await ie(x));else if(this.vfs.isDir(x)){let k=this.vfs.norm(x).replace(/\/$/,"")+"/";n={};for(let[j,q]of this.vfs.nodes)!q.dir&&j.startsWith(k)&&(n[j.slice(k.length)]=q.data);t=this.vfs.base(this.vfs.norm(x))}else if(this.vfs.isFile(x))n=await Xe(this.vfs.readBytes(x)),t=this.vfs.base(this.vfs.norm(x)).replace(/\.xdc$/i,"");else throw new Error(`${x}: not a file, folder or URL`)}if(!n["index.html"]){let x=new Set(Object.keys(n).map(k=>k.split("/")[0]));if(x.size===1){let k=[...x][0]+"/";n[k+"index.html"]&&(n=Object.fromEntries(Object.entries(n).map(([j,q])=>[j.slice(k.length),q])))}}if(!n["index.html"])throw new Error("this is not a webxdc app: index.html is missing");let i=n["manifest.toml"]?Pt(K.decode(n["manifest.toml"])):{},h=String(i.name||"").trim();if(!h){let x=/<title>([^<]{1,60})<\/title>/i.exec(K.decode(n["index.html"]));h=x&&x[1].trim()||t}let o=["icon.png","icon.jpg","icon.jpeg","icon.svg","icon.webp"].find(x=>n[x]),l="xdc-"+h.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").slice(0,40),p=this.store?await this.store.get(l):null,S={id:l,name:h,manifest:i,files:n,icon:o?`data:${Ze(o)};base64,${le(n[o])}`:null,size:Object.values(n).reduce((x,k)=>x+k.length,0),updates:p?.updates||[],ls:p?.ls||{},summary:p?.summary||"",document:p?.document||""};return this.apps.set(l,S),S}get(e){if(typeof e=="object")return e;let t=String(e).toLowerCase();return this.apps.get(e)||[...this.apps.values()].find(n=>n.name.toLowerCase()===t)||null}list(){return[...this.apps.values()].map(({id:e,name:t,size:n,summary:i,document:h,updates:o})=>({id:e,name:t,size:n,summary:i,document:h,updates:o.length}))}updates(e,t=0){return e=this.get(e),e.updates.filter(n=>n.serial>t).map(n=>this._public(n,e.updates.length))}onUpdate(e){return this.listeners.add(e),()=>this.listeners.delete(e)}_public(e,t){let n={payload:e.payload,serial:e.serial,max_serial:t,sender:e.sender,timestamp:e.ts};for(let i of["info","document","summary","href"])e[i]!=null&&(n[i]=e[i]);return n}async _save(e){this.store&&await this.store.set(e.id,{updates:e.updates,ls:e.ls,summary:e.summary,document:e.document})}send(e,t,n={addr:"agent@kit",name:"Agent"}){if(e=this.get(e),!e)return Promise.reject(new Error("no such app"));let i=(this._q.get(e.id)||Promise.resolve()).then(async()=>{if(!t||typeof t!="object"||!("payload"in t))throw new Error("an update needs a payload");let h=JSON.stringify(t.payload);if(h===void 0)throw new Error("payload must be JSON");if(h.length>128e3)throw new Error("update payload is over 128 KB");let o={serial:e.updates.length+1,payload:JSON.parse(h),sender:n.addr,senderName:n.name,ts:Date.now()};for(let l of["info","document","summary","href","notify"])t[l]!=null&&(o[l]=t[l]);e.updates.push(o),o.summary!=null&&(e.summary=String(o.summary)),o.document!=null&&(e.document=String(o.document)),await this._save(e);for(let l of this.sessions)l.app===e&&l._deliver([o]);for(let l of this.listeners)try{l(e,this._public(o,e.updates.length))}catch{}return this._public(o,e.updates.length)});return this._q.set(e.id,i.catch(()=>{})),i}open(e,{container:t,self:n={addr:"user@kit",name:"You"},onSendToChat:i=null,onOpen:h=null}={}){let o=this.get(e);if(!o)throw new Error("no such app");if(!t)throw new Error("container is required");let l=document.createElement("iframe");l.setAttribute("sandbox","allow-scripts allow-forms allow-modals allow-downloads"),l.setAttribute("allow","autoplay; fullscreen"),l.title=o.name,l.style.cssText="border:0;width:100%;height:100%;display:block;background:#fff";let p=this,S={app:o,frame:l,listening:!1,lastSent:0,post:k=>l.contentWindow?.postMessage(Object.assign({__xdc:1},k),"*"),_deliver(k){if(!this.listening)return;let j=o.updates.length;for(let q of k)q.serial>this.lastSent&&(this.post({t:"update",update:p._public(q,j)}),this.lastSent=q.serial)},send:(k,j)=>p.send(o,k,j),reload:()=>{S.listening=!1,S.lastSent=0,l.srcdoc=Wt(o,n)},close:()=>{window.removeEventListener("message",x),l.remove(),p.sessions.delete(S)}},x=async k=>{if(k.source!==l.contentWindow||!k.data?.__xdc)return;let j=k.data,q=(y,A)=>S.post({t:"reply",id:j.id,data:y,error:A});try{if(j.t==="listen")S.listening=!0,S.lastSent=+j.serial||0,S._deliver(o.updates),S.post({t:"listen-done"});else if(j.t==="send")await p.send(o,j.update,n);else if(j.t==="all")q(o.updates.map(y=>p._public(y,o.updates.length)));else if(j.t==="ls")o.ls=j.data||{},await p._save(o);else if(j.t==="file"){let y=o.files[j.data];y?q({bytes:y.buffer.slice(y.byteOffset,y.byteOffset+y.byteLength),type:Ze(j.data)}):q(null,"not found: "+j.data)}else j.t==="chat"?(i?.(j.data),q(null)):j.t==="open"&&(h?h(j.url):/^https?:/i.test(j.url)&&window.open(j.url,"_blank","noopener"))}catch(y){j.id&&q(null,String(y.message||y))}};return window.addEventListener("message",x),t.appendChild(l),this.sessions.add(S),S.reload(),S}pack(e){return zt(this.get(e).files)}async reset(e){e=this.get(e),e.updates=[],e.ls={},e.summary="",e.document="",await this._save(e)}};var xe="https://ollama.com",Se="http://localhost:11434",he=class{constructor({host:e=Se,apiKey:t=""}={}){this.host=String(e).replace(/\/+$/,""),this.apiKey=t}get cloud(){return/^https:\/\/(www\.)?ollama\.com$/i.test(this.host)}get name(){return this.cloud?"Ollama Cloud":`Ollama at ${this.host}`}get headers(){let e={"Content-Type":"application/json"};return this.apiKey&&(e.Authorization="Bearer "+this.apiKey),e}async _err(e){let t=`HTTP ${e.status}`;try{t=(await e.json()).error||t}catch{}return e.status===401?t=this.cloud?"the Ollama API key was rejected (401). Create one at https://ollama.com/settings/keys":`${this.name} refused the request (401)`:e.status===404&&/model/i.test(t)?t+=this.cloud?"":" (pull it first: ollama pull <model>)":(e.status===402||e.status===429)&&(t+=" (usage limit)"),new Error(`${this.name}: ${t}`)}async _fetch(e,t={}){if(this.cloud&&!this.apiKey)throw new Error("no Ollama Cloud API key: createKit({ ollamaKey }) or kit.ollama.apiKey = \u2026");let n;try{n=await fetch(this.host+e,{...t,headers:{...this.headers,...t.headers||{}}})}catch(i){throw i?.name==="AbortError"?i:new Error(this.cloud?`could not reach Ollama Cloud (${i.message})`:`could not reach ${this.name}. Is "ollama serve" running? If it is, the browser blocked the request: start it with OLLAMA_ORIGINS set to this page's origin (or "*").`)}if(!n.ok)throw await this._err(n);return n}_post(e,t,n){return this._fetch(e,{method:"POST",body:JSON.stringify(t),signal:n})}async models(){return((await(await this._fetch("/api/tags")).json()).models||[]).map(t=>t.name||t.model).filter(Boolean)}async embed(e,{model:t="embeddinggemma",dimensions:n,truncate:i=!0,signal:h}={}){let o=!Array.isArray(e),l=(o?[e]:e).map(String);if(!l.length)return[];let p=[];for(let S=0;S<l.length;S+=64){let x=await this._post("/api/embed",{model:t,input:l.slice(S,S+64),truncate:i,...n?{dimensions:n}:{}},h);p.push(...(await x.json()).embeddings||[])}return o?p[0]:p}async webSearch(e,{maxResults:t=5,signal:n}={}){return(await this._post("/api/web_search",{query:String(e),max_results:Math.max(1,Math.min(10,+t||5))},n)).json()}async webFetch(e,{signal:t}={}){return(await this._post("/api/web_fetch",{url:String(e)},t)).json()}async*chat({signal:e,...t}){let i=(await this._post("/api/chat",{stream:!0,...t},e)).body.getReader(),h=new TextDecoder,o="";for(;;){let{value:l,done:p}=await i.read();if(p)break;o+=h.decode(l,{stream:!0});let S;for(;(S=o.indexOf(`
`))>=0;){let x=o.slice(0,S).trim();if(o=o.slice(S+1),!x)continue;let k=JSON.parse(x);if(k.error)throw new Error(`${this.name}: ${k.error}`);yield k}}if(o.trim()){let l=JSON.parse(o);if(l.error)throw new Error(`${this.name}: ${l.error}`);yield l}}},et=class extends he{constructor({apiKey:e="",host:t=xe}={}){super({host:t,apiKey:e})}};var Be=class{constructor(e,t,{model:n,table:i="docs"}){this.db=e,this.embedFn=t,this.model=n,this.t=i.replace(/[^\w]/g,"_"),this.dims=null}async init(){let e=this.t,t=this.db;t.exec(`create table if not exists ${e}(id text primary key, text text not null, meta text, model text, dims integer)`);let n=t.get(`select dims, model from ${e} limit 1`);if(n&&(this.dims=n.dims,n.model&&n.model!==this.model))throw new Error(`${e} was embedded with ${n.model}, not ${this.model}: open it with { model: '${n.model}' }`);return this}_vecTable(e){if(this.dims&&this.dims!==e)throw new Error(`the embedding model returned ${e} dimensions; this store has ${this.dims}`);this.dims||(this.dims=e,this.db.exec(`create virtual table if not exists ${this.t}_vec using vec0(embedding float[${e}] distance_metric=cosine)`))}async add(e,{signal:t}={}){if(e=(Array.isArray(e)?e:[e]).map((o,l)=>typeof o=="string"?{text:o}:o).filter(o=>o&&String(o.text??"").trim()),!e.length)return[];let n=await this.embedFn(e.map(o=>String(o.text)),{model:this.model,signal:t});this._vecTable(n[0].length);let i=this.t,h=[];return this.db.transaction(o=>{for(let[l,p]of e.entries()){let S=String(p.id??(crypto.randomUUID?.()||Date.now()+"-"+l)),x=o.get(`select rowid from ${i} where id = ?`,[S]);x&&(o.run(`delete from ${i}_vec where rowid = ?`,[x.rowid]),o.run(`delete from ${i} where rowid = ?`,[x.rowid]));let{lastInsertRowid:k}=o.run(`insert into ${i}(id, text, meta, model, dims) values (?, ?, ?, ?, ?)`,[S,String(p.text),p.meta==null?null:JSON.stringify(p.meta),this.model,n[l].length]);o.run(`insert into ${i}_vec(rowid, embedding) values (?, ?)`,[k,JSON.stringify(n[l])]),h.push(S)}}),h}async search(e,{limit:t=5,hybrid:n=!1,signal:i}={}){if(!this.dims)return[];let[h]=await this.embedFn([String(e)],{model:this.model,signal:i}),o=this.t,l=n?Math.max(t*4,20):t,p=this.db.query(`select d.id, d.text, d.meta, v.distance from ${o}_vec v join ${o} d on d.rowid = v.rowid where v.embedding match ? and k = ? order by v.distance`,[JSON.stringify(h),l]).map(q=>({id:q.id,text:q.text,meta:q.meta?JSON.parse(q.meta):null,distance:q.distance,score:1-q.distance}));if(!n)return p.slice(0,t);let S=this.db.query(`select id, text, meta from ${o}`),x=new ae(S.map(q=>({id:q.id,text:q.text}))).search(e,{limit:l}),k=new Map,j=(q,y)=>q.forEach((A,T)=>{let E=k.get(A.id)||{...A,score:0};E.score+=y/(60+T+1),k.set(A.id,E)});return j(p,1),j(x.map(q=>{let y=p.find(T=>T.id===q.id),A=S.find(T=>T.id===q.id);return y||{id:q.id,text:A.text,meta:A.meta?JSON.parse(A.meta):null,distance:null}}),1),[...k.values()].sort((q,y)=>y.score-q.score).slice(0,t)}remove(e){let t=this.t;this.db.transaction(n=>{for(let i of[].concat(e)){let h=n.get(`select rowid from ${t} where id = ?`,[String(i)]);h&&(n.run(`delete from ${t}_vec where rowid = ?`,[h.rowid]),n.run(`delete from ${t} where rowid = ?`,[h.rowid]))}})}count(){return this.db.get(`select count(*) n from ${this.t}`).n}save(){return this.db.save()}close(){this.db.close()}};function Jt(g){return{async open(e=":memory:",{model:t="embeddinggemma",table:n="docs",ollama:i=null}={}){let h=await g.sqlite.open(e),o=i||g.local;return new Be(h,(l,p)=>o.embed(l,p),{model:t,table:n}).init()}}}var yt="http://localhost:11435",is=/^(clef|clef-flash|laya|jev|nimble|tev1|kev|winnow|largha|decider)(?=$|[:\-])/i,os={ollaya:"Ollaya",ollama:"Ollama",cloud:"Ollama Cloud"},as=(g,e)=>{let t=String(g[e]).trim(),n=t.length&&t.length<=100?t:`option_${e+1}`;return g.findIndex(i=>String(i).trim()===t)===e?n:`option_${e+1}`};function ls(g,e){let t={},n={};for(let[h,o]of Object.entries(g.questions||{})){let l={...o};if((o.type||"choice")==="choice"&&Array.isArray(o.criteria)){let p=o.criteria.map((S,x)=>as(o.criteria,x));l.criteria=Object.fromEntries(p.map((S,x)=>[S,String(o.criteria[x])])),t[h]={keys:p,opts:o.criteria.map(String)}}n[h]=l}let i=String(g.model||"");return e&&(i=i.replace(/[:\-]cloud$/i,"")),{req:{...g,model:i,questions:n},maps:t}}function cs(g,e){if(!g||typeof g!="object")return g;let t={...g};if("choice"in g&&e){let n=typeof g.choice=="number"?g.choice:e.keys.indexOf(String(g.choice));n>=0&&n<e.opts.length&&(t.choice=e.opts[n]),g.probabilities&&!Array.isArray(g.probabilities)&&(t.probabilities=Object.fromEntries(e.keys.map((i,h)=>[e.opts[h],+(g.probabilities[i]??0)])))}if(typeof g.noul=="number"){let n=Math.max(0,Math.min(1,g.noul));t.noul=n>=.5,t.p_true=n,t.probabilities={no:+(1-n).toFixed(6),yes:+n.toFixed(6)},t.confidence==null&&(t.confidence=+Math.max(n,1-n).toFixed(6))}return t}var Ce=class{constructor({server:e="ollaya",host:t="",apiKey:n="",model:i="",kit:h=null}={}){Object.assign(this,{server:e,host:t,apiKey:n,model:i,kit:h})}get name(){return os[this.server]||this.server}get base(){return this.server==="cloud"?xe:this.server==="ollama"?String(this.host||this.kit?.local?.host||Se).replace(/\/+$/,""):String(this.host||yt).replace(/\/+$/,"")}get key(){return this.server==="cloud"?this.apiKey||this.kit?.ollama?.apiKey||"":this.apiKey}get headers(){let e={"Content-Type":"application/json"};return this.key&&(e.Authorization="Bearer "+this.key),e}async _fetch(e,t={}){if(!["ollaya","ollama","cloud"].includes(this.server))throw new Error(`unknown decision server "${this.server}": use ollaya, ollama or cloud`);if(this.server==="cloud"&&!this.key)throw new Error("no Ollama Cloud API key for decisions: createKit({ ollamaKey }) or kit.decisions.apiKey = \u2026");try{return await fetch(this.base+e,{...t,headers:this.headers})}catch(n){if(n?.name==="AbortError")throw n;if(this.server==="cloud")throw new Error(`could not reach Ollama Cloud (${n.message})`);let i=this.server;throw new Error(`could not reach ${this.name} at ${this.base}. Is "${i} serve" running? If it is, the browser blocked the request: start it with ${i.toUpperCase()}_ORIGINS set to this page's origin (or "*").`)}}async _err(e,t){let n=`HTTP ${e.status}`;try{let i=await e.json();n=(i.error||n)+(i.detail?" \u2014 "+JSON.stringify(i.detail).slice(0,300):"")}catch{}return e.status===401?n+=this.server==="cloud"?" (the Ollama Cloud API key was rejected)":this.server==="ollaya"?" (the API key was rejected: OLLAYA_API_KEY)":" (the request was refused)":e.status===402?n+=" (cloud decision models need a paid Ollama plan or usage credits)":e.status===403?n+=` (${this.name} refused this page's origin: set ${this.server.toUpperCase()}_ORIGINS)`:e.status===404&&(n+=this.server==="cloud"?` (Ollama Cloud has no decision model "${t}"; try clef)`:this.server==="ollama"?" (decision models need Ollama 0.35 or newer, and the model pulled: ollama pull clef-flash)":` (pull the model: ollaya pull ${t||"<model>"})`),new Error(`${this.name} said ${e.status}: ${n}`)}async models(){let e=await this._fetch("/api/tags");if(!e.ok)throw await this._err(e);let t=((await e.json()).models||[]).map(i=>({name:i.name||i.model,caps:i.capabilities||i.details?.capabilities})).filter(i=>i.name);if(this.server==="ollaya")return t.map(i=>i.name);let n=t.filter(i=>Array.isArray(i.caps)&&i.caps.includes("decision")||is.test(i.name)).map(i=>i.name);return this.server==="cloud"&&(n=n.map(i=>i.replace(/[:\-]cloud$/i,"")),n.includes("clef")||n.unshift("clef")),[...new Set(n)]}async systemone(e,{signal:t}={}){let n=this.server!=="ollaya",i=e,h={};n&&({req:i,maps:h}=ls(e,this.server==="cloud"));let o=await this._fetch("/v1/systemone",{method:"POST",body:JSON.stringify(i),signal:t});if(!o.ok)throw await this._err(o,i.model);let l=await o.json();return n?{...l,answers:Object.fromEntries(Object.entries(l.answers||{}).map(([p,S])=>[p,cs(S,h[p])]))}:l}async decide({state:e="",question:t="",type:n="choice",options:i,model:h,signal:o}={}){if(h||(h=this.model||(this.server==="cloud"?"clef":"")),!h)throw new Error("no decision model: kit.decisions.model = '\u2026' (list them with kit.decisions.models())");let l=n==="yesno"?"noul":n,p={type:l,instructions:String(t||"")},S=(Array.isArray(i)?i:typeof i=="string"?i.split(`
`):[]).map(String).map(y=>y.trim()).filter(Boolean);if(l==="choice"){if(S.length<2)throw new Error('type "choice" needs at least 2 options');p.criteria=S.slice(0,255)}else if(l==="score"){if(S.length<2)throw new Error('type "score" needs 2-10 level descriptions, lowest first');p.criteria=S.slice(0,10)}else if(l!=="noul")throw new Error("type must be choice, score or yesno");let x=await this.systemone({model:h,state:typeof e=="string"?e:JSON.stringify(e??""),questions:{q:p}},{signal:o}),k=x.answers?.q;if(!k)throw new Error(`${this.name} returned no answer`);let j=Array.isArray(k.probabilities)?Object.fromEntries(k.probabilities.map((y,A)=>[String(A),+y])):Object.fromEntries(Object.entries(k.probabilities||{}).map(([y,A])=>[y,+A])),q={type:n==="yesno"?"yesno":l,confidence:k.confidence!=null?+k.confidence:null,probabilities:j,model:x.model||h,server:this.server};return"choice"in k&&(q.choice=k.choice,q.result=k.choice),"score"in k&&(q.score=k.score,q.result=k.score,k.legend!=null&&(q.legend=k.legend)),"noul"in k&&(q.answer=k.noul,q.result=k.noul),q}};var bt=["pending","in_progress","done"],Ue=class{constructor(e,t="/.kit/tasks.json"){this.vfs=e,this.path=t,this.items=[],this.seq=0,this.listeners=new Set;try{let n=JSON.parse(e.read(t));this.items=n.items||[],this.seq=n.seq||Math.max(0,...this.items.map(i=>i.id))}catch{}}_save(){this.vfs.write(this.path,JSON.stringify({seq:this.seq,items:this.items},null,1));for(let e of this.listeners)try{e(this.items)}catch{}}on(e){return this.listeners.add(e),()=>this.listeners.delete(e)}get(e){let t=this.items.find(n=>n.id===+e);if(!t)throw new Error(`no task #${e}`);return t}add(e){let t=(Array.isArray(e)?e:[e]).map(h=>typeof h=="string"?{title:h}:h).filter(h=>String(h?.title??"").trim());if(!t.length)throw new Error("a task needs a title");let n=Date.now(),i=t.map(h=>({id:++this.seq,title:String(h.title).trim(),status:bt.includes(h.status)?h.status:"pending",...h.notes?{notes:String(h.notes)}:{},...h.due?{due:String(h.due)}:{},created:n,updated:n}));return this.items.push(...i),this._save(),Array.isArray(e)?i:i[0]}update(e,t={}){let n=this.get(e);if(t.status!=null){if(!bt.includes(t.status))throw new Error(`status must be ${bt.join(", ")}`);n.status=t.status}for(let i of["title","notes","due"])t[i]!=null&&(n[i]=String(t[i]));return n.updated=Date.now(),this._save(),n}start(e){return this.update(e,{status:"in_progress"})}done(e){return this.update(e,{status:"done"})}remove(e){this.get(e),this.items=this.items.filter(t=>t.id!==+e),this._save()}clear({all:e=!1}={}){let t=this.items.length;return this.items=e?[]:this.items.filter(n=>n.status!=="done"),e&&(this.seq=0),this._save(),t-this.items.length}list({status:e}={}){return this.items.filter(t=>!e||t.status===e).map(t=>({...t}))}text(){if(!this.items.length)return"The task list is empty.";let e={pending:"[ ]",in_progress:"[~]",done:"[x]"};return this.items.map(t=>`${e[t.status]} #${t.id} ${t.title}${t.due?` (due ${t.due})`:""}${t.notes?` \u2014 ${t.notes}`:""}`).join(`
`)}};var ne=(()=>{let g={"@hourly":"0 * * * *","@daily":"0 0 * * *","@midnight":"0 0 * * *","@weekly":"0 0 * * 0","@monthly":"0 0 1 * *","@yearly":"0 0 1 1 *","@annually":"0 0 1 1 *"},e=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"],t=["sun","mon","tue","wed","thu","fri","sat"],n=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],i=[{name:"minute",min:0,max:59},{name:"hour",min:0,max:23},{name:"day of month",min:1,max:31},{name:"month",min:1,max:12,names:e,base:1},{name:"day of week",min:0,max:7,names:t,base:0}];function h(E,$){let s=new Set;for(let r of E.toLowerCase().split(",")){let a=/^(\*|[a-z0-9]+(?:-[a-z0-9]+)?)(?:\/(\d+))?$/.exec(r);if(!a)throw new Error(`bad ${$.name} "${r}"`);let f=c=>{if($.names){let _=$.names.indexOf(c);if(_>=0)return _+$.base}if(!/^\d+$/.test(c))throw new Error(`bad ${$.name} "${c}"`);let u=+c;if(u<$.min||u>$.max)throw new Error(`${$.name} ${u} is out of range ${$.min}-${$.max}`);return u},m,w;if(a[1]==="*")m=$.min,w=$.max,$.name==="day of week"&&(w=6);else if(a[1].includes("-")){if([m,w]=a[1].split("-").map(f),m>w)throw new Error(`${$.name} range ${a[1]} runs backwards`)}else m=f(a[1]),w=a[2]?$.max:m;let d=a[2]?+a[2]:1;if(!d)throw new Error(`${$.name} step must be at least 1`);for(let c=m;c<=w;c+=d)s.add($.name==="day of week"&&c===7?0:c)}return s}function o(E){let $=String(E||"").trim().replace(/\s+/g," ");g[$.toLowerCase()]&&($=g[$.toLowerCase()]);let s=$.split(" ");if(s.length!==5)throw new Error(`cron needs 5 fields (minute hour day month weekday), got ${s.length}`);let[r,a,f,m,w]=s.map((d,c)=>h(d,i[c]));return{expr:$,min:r,hour:a,dom:f,mon:m,dow:w,domStar:s[2]==="*",dowStar:s[4]==="*"}}function l(E,$){let s=E.dom.has($.getDate()),r=E.dow.has($.getDay());return E.domStar&&E.dowStar?!0:E.domStar?r:E.dowStar?s:s||r}function p(E,$=Date.now()){let s=typeof E=="string"?o(E):E,r=new Date($);r.setSeconds(0,0),r.setMinutes(r.getMinutes()+1);for(let a=0;a<2e5;a++){if(!s.mon.has(r.getMonth()+1)){r.setMonth(r.getMonth()+1,1),r.setHours(0,0,0,0);continue}if(!l(s,r)){r.setDate(r.getDate()+1),r.setHours(0,0,0,0);continue}if(!s.hour.has(r.getHours())){r.setHours(r.getHours()+1,0,0,0);continue}if(!s.min.has(r.getMinutes())){r.setMinutes(r.getMinutes()+1,0,0);continue}return r.getTime()}return null}function S(E,$=3,s=Date.now()){let r=[],a=s;for(let f=0;f<$&&(a=p(E,a),!!a);f++)r.push(a);return r}let x=E=>String(E).padStart(2,"0"),k=(E,$)=>new Date(2e3,0,1,E,$).toLocaleTimeString([],{hour:"numeric",minute:"2-digit"});function j(E){let $;try{$=o(E)}catch{return E}let[s,r,a,f,m]=$.expr.split(" "),w=c=>/^\d+$/.test(c),d;if((d=/^\*\/(\d+)$/.exec(s))&&r==="*"&&a==="*"&&f==="*"&&m==="*")return`every ${d[1]} minutes`;if(s==="*"&&r==="*"&&a==="*"&&f==="*"&&m==="*")return"every minute";if(w(s)&&r==="*"&&a==="*"&&f==="*"&&m==="*")return s==="0"?"every hour":`every hour at :${x(s)}`;if(w(s)&&(d=/^\*\/(\d+)$/.exec(r))&&a==="*"&&f==="*"&&m==="*")return`every ${d[1]} hours at :${x(s)}`;if(w(s)&&w(r)&&f==="*"){let c=k(+r,+s);if(a==="*"&&m==="*")return`daily at ${c}`;if(a==="*"&&(m==="1-5"||m==="mon-fri"))return`weekdays at ${c}`;if(a==="*"&&(m==="0,6"||m==="6,0"||m==="sat,sun"))return`weekends at ${c}`;if(a==="*"&&$.dow.size===1)return`every ${n[[...$.dow][0]]} at ${c}`;if(a==="*"&&m!=="*"&&$.dow.size>1)return`every ${[...$.dow].sort((u,_)=>u-_).map(u=>n[u].slice(0,3)).join(" & ")} at ${c}`;if(w(a)&&m==="*")return`monthly on day ${a} at ${c}`;if((d=/^\*\/(\d+)$/.exec(a))&&m==="*")return`every ${d[1]} days at ${c}`}return $.expr}let q={sun:0,sunday:0,sundays:0,mon:1,monday:1,mondays:1,tue:2,tues:2,tuesday:2,tuesdays:2,wed:3,weds:3,wednesday:3,wednesdays:3,thu:4,thur:4,thurs:4,thursday:4,thursdays:4,fri:5,friday:5,fridays:5,sat:6,saturday:6,saturdays:6},y='Use plain English like "every day at 9am", "weekdays at 8:30", "every monday at 6pm", "every 30 minutes", "in 20 minutes", "tomorrow at 7pm", or a 5-field cron like "0 9 * * *".';function A(E){if(/\b(noon|midday)\b/.test(E))return[12,0];if(/\bmidnight\b/.test(E))return[0,0];let $=/(?:^|\s)(?:at\s+)?(\d{1,2})(?:[:.h](\d{2}))?\s*(a\.?m\.?|p\.?m\.?)?(?=\s|$)/.exec(E);if($&&($[2]||$[3]||/\bat\s+\d/.test(E)||/^\d{1,2}$/.test(E.trim())||/\b(daily|weekdays?|weekends?|day|week)\s+\d/.test(E))){let s=+$[1],r=+($[2]||0),a=($[3]||"").replace(/\./g,"");if(a==="pm"&&s<12&&(s+=12),a==="am"&&s===12&&(s=0),s<=23&&r<=59)return[s,r]}return/\bmorning\b/.test(E)?[9,0]:/\bafternoon\b/.test(E)?[14,0]:/\bevening\b/.test(E)?[18,0]:/\b(tonight|night|nightly)\b/.test(E)?[21,0]:null}function T(E){let $=String(E??"").trim();if(!$)throw new Error("no time was given. "+y);if(g[$.toLowerCase()]||/^[\d*][\d*\/,\-]*(\s+[\d*\/,\-a-z]+){4}$/i.test($))try{return{cron:o($).expr}}catch(v){if($.split(/\s+/).length===5)throw new Error(v.message+". "+y)}let s=" "+$.toLowerCase().replace(/[,;]/g," ").replace(/\b(and|&|the|o'?clock)\b/g," ").replace(/\s+/g," ").trim()+" ",r;if(r=/\bin\s+(\d+|an?|one)\s*(m|mins?|minutes?|h|hrs?|hours?|d|days?)\b/.exec(s)){let v=/^\d+$/.test(r[1])?+r[1]:1,O=r[2][0];if(!v)throw new Error("the delay must be at least 1. "+y);return{once:Date.now()+v*(O==="m"?6e4:O==="h"?36e5:864e5)}}if(/\b(every|each)\s+minute\b/.test(s))return{cron:"* * * * *"};if(r=/\b(?:every|each)\s+(\d+)\s*(m|mins?|minutes?)\b/.exec(s)){let v=+r[1];if(v<1)throw new Error("interval must be at least 1 minute");return{cron:v>=60?"0 * * * *":`*/${v} * * * *`}}if(r=/\b(?:every|each)\s+(\d+)\s*(h|hrs?|hours?)\b/.exec(s)){let v=+r[1];if(v<1||v>23)throw new Error("hour interval must be 1-23");return{cron:`0 */${v} * * *`}}if(/\b(hourly|every hour|each hour)\b/.test(s))return{cron:"0 * * * *"};let a=/\b(?:every|each)\s+(\d+)\s*days?\b/.exec(s),f=s.replace(/\b(?:every|each|in)\s+\d+\s*\w+/g," ").replace(/\bon\s+the\s+\d{1,2}(st|nd|rd|th)?\b|\b\d{1,2}(st|nd|rd|th)\b/g," "),m=A(f),[w,d]=m||[9,0],c=new Set;for(let v of s.split(" "))v in q&&c.add(q[v]);let u=/\bweekdays?\b/.test(s)?"1-5":/\bweekends?\b/.test(s)?"0,6":c.size?[...c].sort((v,O)=>v-O).join(","):"";if(/\b(every|each|daily|nightly|weekly|monthly|weekdays?|weekends?)\b/.test(s)||/\b(sun|mon|tues|wednes|thurs|fri|satur)days\b/.test(s)){if(a){let v=+a[1];if(v<1||v>31)throw new Error("day interval must be 1-31");return{cron:`${d} ${w} */${v} * *`}}if(/\b(monthly|every month|each month)\b/.test(s)){let v=/\b(\d{1,2})(st|nd|rd|th)\b/.exec(s)?.[1]||/\bon\s+(?:the\s+)?(\d{1,2})\b/.exec(s)?.[1]||1;if(+v<1||+v>31)throw new Error("day of month must be 1-31");return{cron:`${d} ${w} ${+v} * *`}}return/\b(weekly|every week|each week)\b/.test(s)&&!u&&(u="1"),{cron:`${d} ${w} * * ${u||"*"}`}}let b=new Date;if(b.setSeconds(0,0),/\btomorrow\b/.test(s))return b.setDate(b.getDate()+1),b.setHours(w,d,0,0),{once:b.getTime()};if(c.size===1){let v=[...c][0];return b.setDate(b.getDate()+(v-b.getDay()+7)%7),b.setHours(w,d,0,0),b.getTime()<=Date.now()&&b.setDate(b.getDate()+7),{once:b.getTime()}}if(m||/\b(today|tonight)\b/.test(s))return b.setHours(w,d,0,0),b.getTime()<=Date.now()&&b.setDate(b.getDate()+1),{once:b.getTime()};throw new Error(`could not understand the time "${$}". `+y)}return{parse:o,next:p,upcoming:S,describe:j,fromText:T,HELP:y}})();var Pe=class{constructor(e,{path:t="/.kit/schedule.json",tickMs:n=15e3,catchUp:i=!0}={}){this.kit=e,this.path=t,this.tickMs=n,this.catchUp=i,this.jobs=[],this.fns=new Map,this.listeners=new Set,this.timer=null,this.running=new Set;try{this.jobs=JSON.parse(e.vfs.read(t)).jobs||[]}catch{}}_save(){this.kit.vfs.write(this.path,JSON.stringify({jobs:this.jobs.filter(e=>e.kind!=="fn")},null,1))}on(e){return this.listeners.add(e),()=>this.listeners.delete(e)}_emit(e){for(let t of this.listeners)try{t(e)}catch{}}find(e){let t=String(e),n=this.jobs.find(i=>i.id===t)||this.jobs.find(i=>i.name.toLowerCase()===t.toLowerCase());if(!n)throw new Error(`no scheduled job "${t}"`);return n}add({name:e,when:t,command:n,js:i,python:h,prompt:o,run:l,agent:p=null,enabled:S=!0,cwd:x="/"}={}){let k;if(t instanceof Date||typeof t=="number"){let A=+new Date(t);if(!(A>Date.now()))throw new Error("that time is in the past");k={once:A}}else k=ne.fromText(t);let j=l?"fn":n!=null?"shell":i!=null?"js":h!=null?"python":o!=null?"agent":null;if(!j)throw new Error("give what to run: command, js, python, prompt or run");let q="j"+Date.now().toString(36)+Math.random().toString(36).slice(2,6),y={id:q,name:String(e||(n??o??"job")).slice(0,60),kind:j,...k,payload:n??i??h??o??null,agent:p,cwd:x,enabled:!!S,created:Date.now(),runs:0,last:null};if(y.next=y.cron?ne.next(y.cron):y.once,y.cron&&!y.next)throw new Error(`"${y.cron}" never happens`);return l&&this.fns.set(q,l),this.jobs.push(y),this._save(),this._emit({type:"change",job:y}),{...y}}remove(e){let t=this.find(e);this.jobs=this.jobs.filter(n=>n!==t),this.fns.delete(t.id),this._save(),this._emit({type:"change",job:t})}enable(e,t=!0){let n=this.find(e);return n.enabled=!!t,t&&n.cron&&(n.next=ne.next(n.cron)),this._save(),this._emit({type:"change",job:n}),{...n}}disable(e){return this.enable(e,!1)}list(){return this.jobs.map(e=>({...e,when:e.cron?ne.describe(e.cron):new Date(e.once).toLocaleString()}))}async runNow(e){return this._run(this.find(e))}async _run(e){if(this.running.has(e.id))return{skipped:"still running"};this.running.add(e.id);let t=Date.now(),n;try{let i=this.kit;if(e.kind==="shell"){let h=await i.shell.session({cwd:e.cwd}).run(e.payload);n={code:h.code,output:h.output}}else if(e.kind==="js"){let h=await i.js.run(e.payload,{cwd:e.cwd});n={code:h.code,output:h.output,result:h.result}}else if(e.kind==="python"){let h=await i.python.run(e.payload,{cwd:e.cwd});n={code:h.code,output:h.output}}else if(e.kind==="agent")n={code:0,output:await i.agent({...e.agent||{}}).prompt(e.payload)};else if(e.kind==="fn"){let h=this.fns.get(e.id);if(!h)throw new Error("this function job was added on another page load; add it again");let o=await h(e);n={code:0,output:o===void 0?"":typeof o=="string"?o:JSON.stringify(o)}}else throw new Error(`unknown job kind ${e.kind}`)}catch(i){n={code:1,output:"",error:String(i?.message||i)}}finally{this.running.delete(e.id)}return n.at=t,n.ms=Date.now()-t,n.output?.length>4e3&&(n.output=n.output.slice(0,4e3)+"\u2026"),e.runs++,e.last=n,this._save(),this._emit({type:n.error||n.code?"error":"run",job:{...e},result:n}),n}async tick(e=Date.now()){let t=this.jobs.filter(n=>n.enabled&&n.next&&n.next<=e);for(let n of t)n.cron?n.next=ne.next(n.cron,e):(n.enabled=!1,n.next=null);return t.length&&this._save(),await Promise.all(t.map(n=>this._run(n))),t.length}start(){if(this.timer)return this;if(!this.catchUp){let e=Date.now();for(let t of this.jobs)t.enabled&&t.cron&&t.next<e&&(t.next=ne.next(t.cron,e))}return this.tick().catch(()=>{}),this.timer=setInterval(()=>this.tick().catch(()=>{}),this.tickMs),this}stop(){return clearInterval(this.timer),this.timer=null,this}get started(){return!!this.timer}};var ds=3e4,xt=2e3,pe=(g,e=ds)=>(g=String(g??""),g.length<=e?g:g.slice(0,e/2)+`

[\u2026 ${g.length-e} characters cut \u2026]

`+g.slice(-e/2)),J={type:"string"},ve={type:"integer"},se=(g,e=[])=>({type:"object",properties:g,required:e});function St(g){let e=g.vfs,t=null,n=()=>t||(t=g.shell.session({cwd:"/"})),i={read:{description:"Read a text file. Lines are numbered (cat -n style). Use offset (1-based line) and limit for long files.",parameters:se({path:{...J,description:"file path, e.g. /notes/todo.md"},offset:{...ve,description:"first line to read (1-based)"},limit:{...ve,description:`number of lines (default ${xt})`}},["path"]),run({path:o,offset:l=1,limit:p=xt}){let S=e.norm(o,n().cwd);if(e.isDir(S))return`${S} is a directory:
`+e.list(S).map(y=>e.isDir(e.norm(y,S))?y+"/":y).join(`
`);let x=e.read(S).split(`
`),k=Math.max(1,+l||1),j=Math.min(x.length,k-1+(+p||xt)),q=x.slice(k-1,j).map((y,A)=>`${String(k+A).padStart(6)}	${y.length>2e3?y.slice(0,2e3)+"\u2026":y}`).join(`
`);return pe(q+(j<x.length?`

[${x.length-j} more lines: read with offset ${j+1}]`:""))}},write:{description:"Create or overwrite a file with the given content (folders are created as needed).",parameters:se({path:J,content:J},["path","content"]),run({path:o,content:l}){let p=e.norm(o,n().cwd),S=e.isFile(p);return e.write(p,String(l??"")),`${S?"Overwrote":"Created"} ${p} (${new TextEncoder().encode(String(l??"")).length} bytes)`}},edit:{description:"Edit a file by replacing exact text. oldText must match the file exactly (whitespace included) and occur once, unless replaceAll is true. Read the file first.",parameters:se({path:J,oldText:{...J,description:"the exact text to replace"},newText:{...J,description:"the replacement"},replaceAll:{type:"boolean"}},["path","oldText","newText"]),run({path:o,oldText:l,newText:p,replaceAll:S=!1}){let x=e.norm(o,n().cwd),k=e.read(x),j=String(l??""),q=String(p??"");if(!j)throw new Error("oldText is empty");let y=k.split(j).length-1;if(!y)throw new Error(`oldText was not found in ${x}. Read the file and copy the text exactly.`);if(y>1&&!S)throw new Error(`oldText occurs ${y} times in ${x}. Include more surrounding text so it is unique, or set replaceAll.`);let A=S?k.split(j).join(q):k.replace(j,()=>q);e.write(x,A);let T=k.slice(0,k.indexOf(j)).split(`
`).length;return`Edited ${x}: ${S?y:1} replacement${(S?y:1)>1?"s":""} at line ${T}`}},bash:{description:"Run a shell command line (BusyBox: ls, cat, grep, sed, awk, find, \u2026; pipes, redirects, && ||, $(\u2026)). Also node, python and sqlite3. The working directory persists between calls.",parameters:se({command:J,timeout:{...ve,description:"seconds (default 60)"}},["command"]),async run({command:o,timeout:l=60},{signal:p}={}){let S=await n().run(o,{timeoutMs:Math.min(600,+l||60)*1e3,signal:p}),x=S.output.trimEnd();return pe((x||"(no output)")+(S.code?`
[exit code ${S.code}]`:""))}},python:{description:"Run MicroPython code. The file system is shared with the other tools. print() output is returned.",parameters:se({code:J},["code"]),async run({code:o}){let l=await g.python.run(o,{cwd:n().cwd});return pe((l.output.trimEnd()||"(no output)")+(l.code?`
[exit code ${l.code}]`:""))}},javascript:{description:"Run JavaScript in a Node-style sandbox (require fs, path, node:sqlite; fetch). console.log output is returned, and the value of a top-level return.",parameters:se({code:J},["code"]),async run({code:o}){let l=await g.js.run(o,{cwd:n().cwd});return pe([l.output.trimEnd(),l.result!==void 0?`=> ${JSON.stringify(l.result)}`:"",l.code?`[exit code ${l.code}]`:""].filter(Boolean).join(`
`)||"(no output)")}},sqlite:{description:'Run SQL on a SQLite database file (created if missing; ":memory:" for a scratch one). sqlite-vec (vec0, vec_distance_cosine) and FTS5 are built in. Returns rows as JSON.',parameters:se({database:{...J,description:"file path, e.g. /data/app.db"},sql:J,params:{type:"array",items:{}}},["database","sql"]),async run({database:o,sql:l,params:p}){let S=await g.sqlite.open(o===":memory:"?":memory:":e.norm(o,n().cwd));try{let x=S.exec(l,p??null);return pe(x.length?JSON.stringify(x.map(k=>k.values.map(j=>Object.fromEntries(k.columns.map((q,y)=>[q,j[y]])))).flat().slice(0,500)):`OK (${S.db.changes()} rows changed)`)}finally{S.close({save:o!==":memory:"})}}},search_files:{description:"Find files by meaning of words (BM25 ranking) under a folder. Returns paths, scores and a snippet.",parameters:se({query:J,path:{...J,description:"folder (default /)"},limit:ve},["query"]),run({query:o,path:l="/",limit:p=10}){let S=Ne(e,o,{root:e.norm(l,n().cwd),limit:p});return S.length?JSON.stringify(S,null,1):"no matches"}},search:{description:"Search the web (Ollama web search). Returns titles, URLs and text snippets.",parameters:se({query:J,max_results:{...ve,description:"1-10 (default 5)"}},["query"]),async run({query:o,max_results:l=5},p){let S=await g.ollama.webSearch(o,{maxResults:l,signal:p?.signal});return pe(S.results?.length?S.results.map((x,k)=>`[${k+1}] ${x.title}
${x.url}
${String(x.content||"").trim()}`).join(`

`):"no results")}},fetch:{description:"Fetch a web page by URL (Ollama web fetch). Returns its title, text content and links.",parameters:se({url:J},["url"]),async run({url:o},l){let p=await g.ollama.webFetch(o,{signal:l?.signal});return pe(`# ${p.title||o}

${p.content||""}${p.links?.length?`

Links:
`+p.links.slice(0,50).join(`
`):""}`)}},decide:{description:"Ask a decision model to judge something with calibrated probabilities: pick one option (choice), rate on levels (score), or answer yes/no (yesno). Fast and cheap; use it for triage, routing and checks.",parameters:se({state:{...J,description:"what to judge: a message, log, diff, error or JSON"},question:{...J,description:"what to decide, as an instruction"},type:{type:"string",enum:["choice","score","yesno"]},options:{type:"array",items:J,description:"choice: the options; score: 2-10 levels, lowest first; yesno: none"}},["state","question"]),async run(o,l){let p=await g.decide({...o,signal:l?.signal}),S=Object.entries(p.probabilities).sort((k,j)=>j[1]-k[1]).map(([k,j])=>`${k} ${j.toFixed(3)}`).join(", ");return`${p.type==="score"?`score: ${p.score}${p.legend!=null?` (${typeof p.legend=="string"?p.legend:JSON.stringify(p.legend).slice(0,200)})`:""}`:p.type==="yesno"?`answer: ${p.answer?"yes":"no"}`:`choice: ${p.choice}`}${p.confidence!=null?` | confidence ${p.confidence.toFixed(3)}`:""}${S?`
probabilities: ${S}`:""}
model: ${p.model} (${g.decisions.name})`}},tasks:{description:"Your task list for multi-step work: add tasks when you plan, mark one in_progress while you work on it and done when it is finished. Actions: add (title, or titles for several), update (id, status, title, notes), list, remove (id), clear (removes done tasks).",parameters:se({action:{type:"string",enum:["add","update","list","remove","clear"]},title:J,titles:{type:"array",items:J},id:ve,status:{type:"string",enum:["pending","in_progress","done"]},notes:J},["action"]),run(o){let l=g.tasks;if(o.action==="add"){let p=l.add(o.titles?.length?o.titles:{title:o.title,notes:o.notes});return`Added ${[].concat(p).map(S=>"#"+S.id).join(", ")}

${l.text()}`}if(o.action==="update"){let p=l.update(o.id,{status:o.status,title:o.title,notes:o.notes});return`#${p.id} is ${p.status}

${l.text()}`}if(o.action==="remove")return l.remove(o.id),`Removed #${o.id}

${l.text()}`;if(o.action==="clear"){let p=l.clear();return`Removed ${p} done task${p===1?"":"s"}

${l.text()}`}return l.text()}},schedule:{description:'Schedule work to run later or repeatedly while the page is open: a shell command, JavaScript, Python, or a prompt for an agent. "when" is plain English ("every day at 9am", "weekdays at 8:30", "every 30 minutes", "in 20 minutes", "tomorrow at 7pm") or 5-field cron. Actions: add, list, remove, enable, disable, run (now).',parameters:se({action:{type:"string",enum:["add","list","remove","enable","disable","run"]},name:J,when:J,command:{...J,description:"a shell command line"},js:J,python:J,prompt:{...J,description:"a prompt for an agent"},id:{...J,description:"job id or name"}},["action"]),async run(o){let l=g.schedule,p=x=>`${x.id} ${x.name} \xB7 ${x.cron?ne.describe(x.cron)+` (${x.cron})`:"once"} \xB7 next ${x.next?new Date(x.next).toLocaleString():"\u2014"}${x.enabled?"":" \xB7 disabled"}${x.last?` \xB7 last ${x.last.error?"failed: "+x.last.error:"exit "+x.last.code}`:""}`;if(o.action==="add"){let x=l.add({name:o.name,when:o.when,command:o.command,js:o.js,python:o.python,prompt:o.prompt});return"Scheduled "+p(x)+(l.started?"":`
(the scheduler is stopped: kit.schedule.start())`)}if(o.action==="remove")return l.remove(o.id??o.name),"Removed "+(o.id??o.name);if(o.action==="enable"||o.action==="disable")return p(l.enable(o.id??o.name,o.action==="enable"));if(o.action==="run"){let x=await l.runNow(o.id??o.name);return x.error?`Error: ${x.error}`:(x.output?.trimEnd()||"(no output)")+(x.code?`
[exit code ${x.code}]`:"")}let S=l.list();return S.length?S.map(p).join(`
`):"Nothing is scheduled."}}};i.web_search=i.search,i.web_fetch=i.fetch;let h=o=>(o||Object.keys(i).filter(l=>!l.startsWith("web_"))).filter(l=>i[l]);return{defs:i,names:()=>h(),openai:o=>h(o).map(l=>({type:"function",function:{name:l,description:i[l].description,parameters:i[l].parameters}})),anthropic:o=>h(o).map(l=>({name:l,description:i[l].description,input_schema:i[l].parameters})),async call(o,l={},p={}){let S=i[o];if(!S)return`Error: unknown tool "${o}". Tools: ${h().join(", ")}`;if(typeof l=="string")try{l=JSON.parse(l||"{}")}catch{return`Error: arguments for ${o} are not valid JSON`}try{return String(await S.run(l||{},p))}catch(x){return`Error: ${x?.message||x}`}},add(o,l){return i[o]=l,this},get shell(){return n()}}}var vt=["read","write","edit","bash","search","fetch"],fs=`You are a capable assistant working in a sandboxed browser workspace with a Unix-like file system.
Tools:
- read: read a file (numbered lines)
- write: create or overwrite a file
- edit: replace exact text in a file (read it first; oldText must match exactly)
- bash: run shell commands (ls, cat, grep, find, sed, awk, \u2026), plus node, python and sqlite3
- search: search the web
- fetch: fetch a web page
Work step by step. Prefer edit over rewriting whole files. Check your work (run it, read it back). Be concise in your final answer.`,We=class{constructor({kit:e,provider:t=null,ollama:n=null,model:i=null,system:h=fs,tools:o=vt,think:l=void 0,maxSteps:p=40,options:S=void 0,onEvent:x=null}){t||(t=e.ollama.apiKey?"cloud":"local"),this.client=n||(t==="cloud"?e.ollama:e.local),i||(i=this.client.cloud?"gpt-oss:120b":"qwen3:8b"),Object.assign(this,{kit:e,model:i,system:h,toolNames:o,think:l,maxSteps:p,options:S,onEvent:x}),this.messages=[],this.ctrl=null}emit(e){try{this.onEvent?.(e)}catch{}}reset(){this.messages=[]}abort(){this.ctrl?.abort()}async prompt(e,{images:t}={}){if(this.ctrl)throw new Error("the agent is already running");let i=(this.ctrl=new AbortController).signal,h=this.kit.tools.openai(this.toolNames);this.messages.push({role:"user",content:String(e),...t?.length?{images:t}:{}});try{for(let l=0;l<this.maxSteps;l++){let p={role:"assistant",content:""},S="",x=[];for await(let k of this.client.chat({model:this.model,messages:[{role:"system",content:this.system},...this.messages],tools:h,...this.think!==void 0?{think:this.think}:{},...this.options?{options:this.options}:{},signal:i})){let j=k.message||{};j.thinking&&(S+=j.thinking,this.emit({type:"thinking",delta:j.thinking})),j.content&&(p.content+=j.content,this.emit({type:"text",delta:j.content})),j.tool_calls?.length&&x.push(...j.tool_calls)}if(S&&(p.thinking=S),x.length&&(p.tool_calls=x),this.messages.push(p),this.emit({type:"turn_end",message:p}),!x.length)return this.emit({type:"done",text:p.content}),p.content;for(let k of x){let j=k.function?.name,q=k.function?.arguments??{};if(typeof q=="string")try{q=JSON.parse(q)}catch{q={}}this.emit({type:"tool_call",name:j,args:q});let y=await this.kit.tools.call(j,q,{signal:i});if(this.emit({type:"tool_result",name:j,result:y}),this.messages.push({role:"tool",tool_name:j,content:y}),i.aborted)throw new DOMException("stopped","AbortError")}}let o=`(stopped after ${this.maxSteps} steps)`;return this.emit({type:"done",text:o}),o}catch(o){if(o?.name==="AbortError")return this.emit({type:"done",text:"(stopped)"}),"(stopped)";throw this.emit({type:"error",error:o}),o}finally{this.ctrl=null}}};var Ht="0.1.0";async function us({persist:g=!1,files:e=null,ollamaKey:t="",ollamaHost:n=Se,decide:i={},assetsBase:h=null,cdn:o="https://cdn.jsdelivr.net/npm/",engine:l="auto",scheduler:p=!0,busybox:S=!0}={}){h&&ct(h);let x=new qe({persist:g});!await x.load().catch(()=>!1)&&e&&x.import(e);let j=new Oe(x),q=new De(x),y=new Ie({vfs:x,cdn:o}),A=new Le({vfs:x,sqlite:q,cdn:o}),T=new he({host:xe,apiKey:t}),E=new he({host:n}),$={version:Ht,vfs:x,busybox:j,sqlite:q,ml:y,python:A,ollama:T,local:E,bm25:{BM25:ae,search:wt,tokenize:Fe,searchFiles:(a,f)=>Ne(x,a,f)}};$.js=new Te({vfs:x,sqlite:q,ml:y,bridge:(a,f)=>r(a,f)});let s={node:$.js.command(),js:$.js.command(),python:A.command(),python3:A.command(),sqlite3:q.command()};$.shell=Dt({vfs:x,busybox:j,engine:l,commands:s}),$.sh=$.shell.session(),$.run=(a,f)=>$.sh.run(a,f),$.webxdc=new Re({vfs:x,persist:g}),$.embed=(a,f)=>E.embed(a,f),$.vectors=Jt($),$.decisions=new Ce({...i,kit:$}),$.decide=a=>$.decisions.decide(a),$.cron=ne,$.tasks=new Ue(x),$.schedule=new Pe($),$.tools=St($),$.agent=(a={})=>new We({kit:$,...a});async function r(a,f){if(a==="tool")return $.tools.call(f.name,f.args||{});if(a==="list")return $.tools.names();if(a==="decide")return $.decide(f);if(a==="shell"){let m=await $.shell.session().run(f.command);return{stdout:m.stdout,stderr:m.stderr,code:m.code}}throw new Error(`kit.${a} is not available in Jade Agent Kit`)}return S&&j.load(),p&&$.schedule.start(),$}return es(hs);})();
