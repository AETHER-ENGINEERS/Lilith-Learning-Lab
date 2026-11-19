"""Ask a language model which of Kulikauskas's three structures a note's mechanism has. usage: OLLAMA_KEY=.. python3 llm_kind.py VAULT_DIR N"""
import json, os, sys, glob, urllib.request, concurrent.futures as cf
KEY = os.environ['OLLAMA_KEY']
P = """Which structure best describes how the things in this note are organised?
- sequence: an ordered chain, one thing after another, no branching and no loops
- hierarchy: a tree, parts nested in wholes or one thing splitting into several, each thing with one parent
- network: things linked to each other in many ways, including loops, feedback, or several things leading to the same thing
- none: no structure is described
Reply with JSON only: {"kind":"sequence"|"hierarchy"|"network"|"none"}
Note: %s"""
def call(n):
    req = urllib.request.Request('https://ollama.com/api/chat', data=json.dumps({'model': 'gemma4:31b', 'stream': False, 'think': False, 'options': {'temperature': 0}, 'messages': [{'role': 'user', 'content': P % n['body'].split('. It was')[0]}]}).encode(), headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'})
    for _ in range(4):
        try:
            t = json.load(urllib.request.urlopen(req, timeout=120))['message']['content']; k = json.loads(t[t.index('{'):t.rindex('}') + 1])['kind']
            if k in ('sequence', 'hierarchy', 'network', 'none'): return k
        except Exception as e: err = e
    return 'none'
d, k = sys.argv[1], int(sys.argv[2])
for f in sorted(glob.glob(d + '/vault_*.json'))[:k]:
    V = json.load(open(f))
    if 'kinds' in V: continue
    ns = [n for n in V['notes'] if n['domain'] != 'meta']
    with cf.ThreadPoolExecutor(8) as ex: r = list(ex.map(call, ns))
    V['kinds'] = {n['name']: x for n, x in zip(ns, r)}; json.dump(V, open(f, 'w')); print(f, flush=True)
