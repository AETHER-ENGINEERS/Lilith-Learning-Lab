"""Adds an 'llm' extractor variant to generated vaults: a language model reads each note and returns claims.
usage: python3 llm_extract.py VAULT_DIR N_VAULTS   (env OLLAMA_KEY, OLLAMA_HOST, OLLAMA_MODEL)"""
import json, os, sys, re, urllib.request, concurrent.futures as cf
HOST = os.environ.get('OLLAMA_HOST', 'https://ollama.com'); MODEL = os.environ.get('OLLAMA_MODEL', 'gemma4:31b'); KEY = os.environ['OLLAMA_KEY']
PATS = ['positive_feedback', 'negative_feedback', 'bottleneck', 'buffer', 'threshold_cascade', 'oscillation', 'redundancy', 'contagion']
PROMPT = """You turn one short note into structured claims. Reply with JSON only: {"claims":[["subject","relation","object"], ...]}.
Rules:
- relation "causes": the note says A leads to / brings / raises B. relation "prevents": the note says A stops / avoids / reduces B. Write A and B as short lowercase snake_case noun phrases copied from the note (for example "retry_load"). Use the same words the note uses.
- relation "is": only if the note describes how some system works and that mechanism is one of: positive_feedback (growth feeds itself), negative_feedback (correction pulls back to a steady level), bottleneck (one narrow part limits all), buffer (a store smooths bursts), threshold_cascade (one failure pushes others past their limits), oscillation (delayed correction swings back and forth), redundancy (spare duplicate parts), contagion (spreads member to member). Then write ["%(name)s_auto","is","<mechanism>"].
- Give no claim when the note says nothing like that. Ignore filler sentences. Do not invent anything.
Note title: %(title)s
Note text: %(body)s"""
def call(n):
    req = urllib.request.Request(HOST + '/api/chat', data=json.dumps({'model': MODEL, 'stream': False, 'think': False, 'options': {'temperature': 0},
        'messages': [{'role': 'user', 'content': PROMPT % dict(name=re.sub(r'[^a-z0-9]+', '_', n['name'].lower()), title=n['title'], body=n['body'])}]}).encode(),
        headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'})
    for _ in range(4):
        try:
            txt = json.load(urllib.request.urlopen(req, timeout=120))['message']['content']
            cl = json.loads(txt[txt.index('{'):txt.rindex('}') + 1]).get('claims', [])
            out = []
            for c in cl:
                if isinstance(c, list) and len(c) == 3 and all(isinstance(x, str) and x for x in c):
                    s, r, o = [re.sub(r'[^a-z0-9_]+', '_', x.lower()).strip('_') for x in c]
                    if r in ('causes', 'prevents') or (r == 'is' and o in PATS): out.append([s, r, o])
            return out
        except Exception as e: err = e
    print('FAILED', n['name'], err, flush=True); return []
d, k = sys.argv[1], int(sys.argv[2])
for i in range(k):
    f = f'{d}/vault_{i:03d}.json'; v = json.load(open(f))
    if 'llm' in v['variants']: continue
    with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(call, v['notes']))
    v['variants']['llm'] = {n['name']: r for n, r in zip(v['notes'], res)}
    # score against the oracle claims
    orc = v['variants']['oracle']; tp = fp = fn = 0
    for n in v['notes']:
        a = {tuple(c) for c in v['variants']['llm'][n['name']] if c[1] != 'is'}; b = {tuple(c) for c in orc[n['name']] if c[1] in ('causes', 'prevents')}
        tp += len(a & b); fp += len(a - b); fn += len(b - a)
    pt = v['truth']['pattern_of']; ok = tot = 0
    for n in v['notes']:
        got = [c[2] for c in v['variants']['llm'][n['name']] if c[1] == 'is']
        if n['name'] in pt: tot += 1; ok += bool(got) and got[0] == pt[n['name']]
    v['llm_stats'] = dict(causal_tp=tp, causal_fp=fp, causal_fn=fn, pattern_acc=ok / max(1, tot))
    json.dump(v, open(f, 'w')); print(i, v['llm_stats'], flush=True)
