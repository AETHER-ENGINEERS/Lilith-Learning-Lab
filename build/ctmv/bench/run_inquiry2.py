import sys, json, numpy as np, inquiry as I
N = int(sys.argv[1]); out = []
for comp, wt in ((False, 'library'), (True, 'composite')):
    for cost in (0.05, 0.3, 0.6):
        for name, mode in (('plain', 'plain'), ('curious', 'curious')):
            ok = []; used = []
            for ep in range(N):
                rng = np.random.default_rng(5000 + ep); w = I.make_world(rng, comp)
                g, u, f = I.episode(w, rng, mode, creative=True, cost=cost); ok.append(g == w.family); used.append(u)
            out.append(dict(world=wt, cost=cost, agent=name, acc=float(np.mean(ok)), exp=float(np.mean(used)), reward=float(np.mean([(1 if o else -1) - cost * u for o, u in zip(ok, used)]))))
            print(out[-1], flush=True)
json.dump(out, open(sys.argv[2], 'w'))
