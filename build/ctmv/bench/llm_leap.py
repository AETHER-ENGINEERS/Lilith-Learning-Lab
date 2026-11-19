"""Creative leap by language model: show it the notes that no known pattern explains and ask it to group the ones that share an
underlying mechanism across different domains, naming the mechanism in its own words (no ontology given).
usage: OLLAMA_KEY=.. python3 llm_leap.py VAULT_DIR N OUT_JSON"""
import json, os, sys, re, glob, collections, urllib.request, concurrent.futures as cf
import numpy as np
HOST = os.environ.get('OLLAMA_HOST', 'https://ollama.com'); MODEL = os.environ.get('OLLAMA_MODEL', 'gemma4:31b'); KEY = os.environ['OLLAMA_KEY']
PROMPT = """Below are short notes from a personal knowledge base, each from some domain. Some of them describe the SAME underlying mechanism (the same abstract structure) in different domains, with different words. Find those groups. A group needs at least 2 notes from different domains. Ignore notes that are plain facts, opinions or filler.
Reply with JSON only: {"groups":[{"mechanism":"short name in your own words","notes":["id","id",...]}]}
Notes:
%s"""
def ask(V):
    items = [n for n in V['notes'] if n['domain'] != 'meta']
    txt = '\n'.join(f"{n['name']} [{n['domain']}]: {n['body'].split('. It was')[0]}" for n in items)
    req = urllib.request.Request(HOST + '/api/chat', data=json.dumps({'model': MODEL, 'stream': False, 'think': False, 'options': {'temperature': 0},
        'messages': [{'role': 'user', 'content': PROMPT % txt}]}).encode(), headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'})
    for _ in range(3):
        try:
            t = json.load(urllib.request.urlopen(req, timeout=240))['message']['content']; return json.loads(t[t.index('{'):t.rindex('}') + 1])['groups']
        except Exception as e: err = e
    print('FAILED', V['seed'], err, flush=True); return []
def score(V, groups):
    truth = V['truth']['pattern_of']; dom = {n['name']: n['domain'] for n in V['notes']}; names = set(dom)
    pure = tot = 0; covered = set(); ffbad = 0; found = set()
    for g in groups:
        ns = [n for n in g.get('notes', []) if n in names]
        if len(ns) < 2: continue
        tot += 1; lab = [truth.get(n, 'none') for n in ns]; maj, c = collections.Counter(lab).most_common(1)[0]
        if maj != 'none' and c / len(ns) >= .75: pure += 1; found.add(maj); covered |= {n for n in ns if truth.get(n) == maj}
    pairs = {tuple(sorted(p)) for p in V['truth']['bridges']}; got = set()
    for g in groups:
        ns = [n for n in g.get('notes', []) if n in names]
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)): got.add(tuple(sorted((ns[i], ns[j]))))
    return dict(groups=tot, pure=pure, patterns_found=len(found), patterns=len(set(truth.values())), pairs_proposed=len(got), pairs_true=len(got & pairs), bridges=len(pairs), covered=len(covered), pattern_notes=len(truth))
d, k, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
Vs = [json.load(open(f)) for f in sorted(glob.glob(d + '/vault_*.json'))[:k]]
with cf.ThreadPoolExecutor(6) as ex: G = list(ex.map(ask, Vs))
res = [dict(seed=V['seed'], raw=g, **score(V, g)) for V, g in zip(Vs, G)]
json.dump(res, open(out, 'w'))
S = lambda key: sum(r[key] for r in res)
print('vaults', len(res), 'groups', S('groups'), 'pure', S('pure'), 'patterns found %d/%d' % (S('patterns_found'), S('patterns')), 'pairs proposed', S('pairs_proposed'), 'true bridges hit %d/%d' % (S('pairs_true'), S('bridges')), 'precision %.2f recall %.2f' % (S('pairs_true') / max(1, S('pairs_proposed')), S('pairs_true') / S('bridges')))
