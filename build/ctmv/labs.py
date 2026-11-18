"""CTMV webxdc labs: one page (lab.html) built from the Jade components, started in different modes."""
import base64, gzip, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..', 'vendor')
def _gz(path):
    d = open(path, 'rb').read()
    return json.dumps(base64.b64encode(gzip.compress(d, 9, mtime=0)).decode())
def _t(p): return open(os.path.join(HERE, p), encoding='utf-8').read()

LABS = {
 'three': dict(title='Lab 1: One note, three views', tabs='vgm', height=560, intro='Open one vault, look at a note as a file (V), as facts with proofs (G) and as a point in space (M). The page runs the real jade-agent-kit SQLite with sqlite-vec and the Jade Vault Datalog engine, offline.',
   goals=[('openV','Open the V tab and read a note'),('query','Ask G a question with variables (Query)'),('verify','Ask G to verify a claim and read the proof'),('knn','Ask M for nearest neighbours')]),
 'bridge': dict(title='Lab 2: Measure δ and find the bridge', tabs='dgm', height=620, intro='Compare what the manifold says with what the symbolic layer says. Find the pair of notes that are about the same loop in two different worlds but share no words and no link.',
   goals=[('openD','Open the δ table'),('bridge','Mark the cross-domain bridge between the retry storm and the squeal')]),
 'warp': dict(title='Lab 3: Warp the metric', tabs='wgd', height=680, intro='Pull causal neighbours closer, push contradicting ones away, and drop notes that a newer note replaced. Compare plain nearest-neighbour search with the warped multi-hop search.',
   goals=[('pull','Raise λ so a causal neighbour that plain search missed is found'),('push','Raise μ so disputed advice is pushed out'),('current','Search the cache question: the replaced 2023 note must not be returned')]),
 'garden': dict(title='Lab 4: Garden and replay', tabs='rvgd', height=700, intro='Add a note, run the gardener, then throw away G and M and rebuild them from the markdown with a different embedding size. The facts must come out identical.',
   goals=[('edit','Create or edit a note (it is saved with write-then-rename)'),('garden','Run the gardener'),('replay','Replay with a different embedding size and get identical facts')]),
}
def lab(key):
    c = LABS[key]
    h = _t('lab.html')
    kit = open(os.path.join(V, 'jade-agent-kit', 'jade-agent-kit.iife.js'), encoding='utf-8').read().replace('</script', '<\\/script')
    rep = {'/*__KIT__*/': kit, '/*__VAULT__*/': _t('vault.js'), '/*__ENGINE__*/': _t('engine.js'),
           '__SQLITE__': _gz(os.path.join(V, 'jade-agent-kit', 'sqlite3.wasm')), '__KGWASM__': _gz(os.path.join(V, 'jade-vault', 'jade_kg.wasm')),
           "'__MODE__'": json.dumps(key), '__GOALS__': json.dumps(c['goals']), "'__TITLE__'": json.dumps(c['title']), '__TABS__': json.dumps(list(c['tabs']))}
    for k, v in rep.items(): h = h.replace(k, v)
    return {'type': 'webxdc', 'title': c['title'], 'intro': c['intro'], 'height': c['height'], 'html': h}
if __name__ == '__main__':
    for k in LABS: print(k, len(lab(k)['html']) // 1024, 'KB')
