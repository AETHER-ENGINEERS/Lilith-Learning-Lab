import sys, json, numpy as np, inquiry as I
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
rows = []
conds = [('random experiments', 'random', False), ('AIXI-style planner, no curiosity', 'plain', False), ('AIXI-style planner + curiosity', 'curious', False),
         ('AIXI-style planner + curiosity + creativity', 'curious', True), ('random + creativity', 'random', True)]
for wtype, comp in (('library pattern', False), ('new composite pattern', True)):
    for name, mode, cr in conds:
        ok = []; used = []; inv = []
        for ep in range(N):
            rng = np.random.default_rng(1000 + ep); w = I.make_world(rng, comp)
            g, u, f = I.episode(w, rng, mode, creative=cr); ok.append(g == w.family); used.append(u); inv.append(f)
        rows.append(dict(world=wtype, agent=name, acc=float(np.mean(ok)), se=float(np.std(ok) / np.sqrt(N)), exp=float(np.mean(used)), invented=float(np.mean(inv)),
                         reward=float(np.mean([(1 if o else -1) - 0.05 * u for o, u in zip(ok, used)]))))
        print(rows[-1], flush=True)
json.dump(rows, open(sys.argv[2] if len(sys.argv) > 2 else '/tmp/inquiry.json', 'w'))
