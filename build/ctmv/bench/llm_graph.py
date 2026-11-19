"""Ask a language model to turn each domain note into a small signed relation graph (open vocabulary, no pattern list).
usage: OLLAMA_KEY=.. python3 llm_graph.py VAULT_DIR N"""
import json, os, sys, re, glob, urllib.request, concurrent.futures as cf
HOST = 'https://ollama.com'; MODEL = os.environ.get('OLLAMA_MODEL', 'gemma4:31b'); KEY = os.environ['OLLAMA_KEY']
PROMPT = """Describe how the system in this note works as a small directed graph. Reply with JSON only: {"edges":[["from","to","+"], ...]}.
- Nodes are the things, quantities or events in the note, as short lowercase snake_case names. Reuse the same node name when the note mentions the same thing again, and include loops when the note describes one (the last effect feeding back into the first cause).
- Each edge says "from" influences "to". Sign "+" if more of from gives more of to (or makes it happen); "-" if more of from gives less of to, stops it or removes it.
- At most 7 edges. If the note states only a plain fact with no mechanism, return {"edges":[]}.
Note: %s"""
def call(n):
    req = urllib.request.Request(HOST + '/api/chat', data=json.dumps({'model': MODEL, 'stream': False, 'think': False, 'options': {'temperature': 0},
        'messages': [{'role': 'user', 'content': PROMPT % (n['body'].split('. It was')[0])}]}).encode(), headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'})
    for _ in range(4):
        try:
            t = json.load(urllib.request.urlopen(req, timeout=120))['message']['content']; E = json.loads(t[t.index('{'):t.rindex('}') + 1])['edges']
            return [[re.sub(r'[^a-z0-9_]+', '_', a.lower()).strip('_'), re.sub(r'[^a-z0-9_]+', '_', b.lower()).strip('_'), s] for a, b, s in E if s in '+-' and a and b]
        except Exception as e: err = e
    print('FAILED', n['name'], err, flush=True); return []
if __name__ == '__main__':
    d, k = sys.argv[1], int(sys.argv[2])
    for f in sorted(glob.glob(d + '/vault_*.json'))[:k]:
        V = json.load(open(f))
        if 'graphs' in V: continue
        notes = [n for n in V['notes'] if n['domain'] != 'meta']
        with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(call, notes))
        V['graphs'] = {n['name']: g for n, g in zip(notes, res)}; json.dump(V, open(f, 'w')); print(f, sum(len(g) > 0 for g in res), '/', len(res), flush=True)
