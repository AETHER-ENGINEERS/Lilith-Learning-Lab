"""An MC-AIXI-style scientific inquiry agent with artificial curiosity and creativity.

World: a hidden system with unknown dynamics in a domain the agent has never seen (a new 'lab bench').
Actions: run an experiment (choose a starting value and how long to watch) or predict which pattern governs the system (ends the episode).
Percepts: a noisy time series (after an experiment) or a reward.

AIXI part (Hutter), approximated the way Veness et al. do in MC-AIXI-CTW, but with a smaller model class:
  * environment model = Bayesian MIXTURE over hypotheses with prior 2^-(description bits)   [Solomonoff-style; MC-AIXI uses context-tree weighting here]
  * planning = Monte-Carlo tree search (UCT) over action sequences; each rollout samples a world from the current posterior and simulates the percepts.
    (Approximation: open-loop tree over actions, one sampled world per rollout, no posterior update inside the tree, finite horizon.)
Curiosity (Schmidhuber): intrinsic reward = how much the experiment improves the agent's compression of its data = Bayesian information gain,
  KL(posterior after || posterior before).  Pure noise gives no gain, so the agent is not drawn to it.
Creativity: when the best hypotheses stop compressing the data (bits per observation stay above the noise floor), the agent invents new
  hypotheses by combining library patterns (sum of effects, or one gating the other) and adds them to the mixture with a complexity penalty.
"""
import math, random, itertools
import numpy as np

SIG = 0.08   # observation noise (known)
STARTS = (0.5, 1.0, 2.0); HORIZONS = (3, 6)
ACTIONS = [(x0, h) for x0 in STARTS for h in HORIZONS]

# ---- the pattern library (what the agent knows from OTHER domains: the vault's cross-domain patterns) ----
def step_pos(x, v, a): return x + a * x, v                       # growth feeds itself
def step_neg(x, v, a): return x + a * (1.0 - x), v               # correction pulls toward a set point
def step_osc(x, v, a): return x + v, v - a * (x - 1.0)           # delayed correction swings
def step_drift(x, v, a): return x + a, v                         # constant push
PRIM = {'pos': (step_pos, (0.2, 0.4)), 'neg': (step_neg, (0.3, 0.6)), 'osc': (step_osc, (0.3, 0.6)), 'drift': (step_drift, (0.2, 0.4))}

def incr(name, x, v, a):
    nx, nv = PRIM[name][0](x, v, a); return nx - x, nv - v

class Model:
    def __init__(self, family, params, bits):
        self.family, self.params, self.bits = family, params, bits
    def series(self, x0, h):
        x, v, out = x0, 0.0, []
        for _ in range(h):
            x, v = self.step(x, v); out.append(x)
            if abs(x) > 1e3: out += [x] * (h - len(out)); break
        return np.array(out)
    def step(self, x, v):
        f = self.family
        if f in PRIM: return PRIM[f][0](x, v, self.params[0])
        kind, (p, q) = f.split(':')[0], f.split(':')[1].split('+') if '+' in f else f.split(':')[1].split('*')
        if kind == 'sum':
            dx1, dv1 = incr(p, x, v, self.params[0]); dx2, dv2 = incr(q, x, v, self.params[1]); return x + dx1 + dx2, v + dv1 + dv2
        if kind == 'gate':                                           # the first effect, throttled by the second effect's room (logistic-like)
            dx1, dv1 = incr(p, x, v, self.params[0]); room = max(0.0, 1.0 - x / self.params[1]); return x + dx1 * room, v + dv1 * room

def library():
    return [Model(f, (a,), 3.0) for f, (_, grid) in PRIM.items() for a in grid]
def invented(prim_only=True):
    """creative step: combine two library patterns; each invention costs extra description bits"""
    out = []
    for p, q in itertools.permutations(PRIM, 2):
        if p in ('osc',) or q in ('osc',): continue
        if p < q:
            for a in PRIM[p][1]:
                for b in PRIM[q][1]: out.append(Model(f'sum:{p}+{q}', (a, b), 3 + 3 + 4))
        for a in PRIM[p][1]:
            for K in (2.0, 3.0): out.append(Model(f'gate:{p}*{q}', (a, K), 3 + 3 + 5))
    return out

class Mixture:
    def __init__(self, models):
        self.set(models)
    def set(self, models):
        self.models = models; self.prior = np.array([2.0 ** -m.bits for m in models]); self.prior /= self.prior.sum()
        self.table = {a: [m.series(*a) for m in models] for a in ACTIONS}; self.logw = np.log(self.prior)
    def add(self, models):
        keep = list(zip(self.models, self.logw))
        self.set(self.models + models)
        n = len(keep); w = np.log(self.prior) ; w[:n] = [lw for _, lw in keep]; self.logw = w   # old evidence kept; new models enter at their prior mass against the old best
        m = np.max(self.logw[:n]); self.logw[n:] = np.log(self.prior[n:]) - np.log(self.prior[:n].max()) + np.max(self.logw[:n]) - 0   # fair start relative to the current best
    def post(self, logw=None):
        lw = self.logw if logw is None else logw; p = np.exp(lw - lw.max()); return p / p.sum()
    def loglik(self, a, obs):
        M = np.array(self.table[a]); return -0.5 * np.sum((M - obs) ** 2, axis=1) / SIG ** 2 - len(obs) * math.log(SIG * math.sqrt(2 * math.pi))
    def update(self, a, obs):
        ll = self.loglik(a, obs); self.logw = self.logw + ll; return ll
    def family_probs(self):
        p = self.post(); d = {}
        for m, pi in zip(self.models, p): d[m.family] = d.get(m.family, 0) + pi
        return d

def kl(p, q): p = np.clip(p, 1e-12, 1); q = np.clip(q, 1e-12, 1); return float(np.sum(p * np.log2(p / q)))

# ---- Monte-Carlo tree search (UCT) over experiments, ending with a prediction ----
class Plan:
    def __init__(self, mix, rng, beta, cost, depth, sims, c=1.0):
        self.mix, self.rng, self.beta, self.cost, self.depth, self.sims, self.c = mix, rng, beta, cost, depth, sims, c
        self.fams = sorted(mix.family_probs())
    def rollout_value(self, true_i, lw, seq, d):
        """simulate: run the chosen experiments in a sampled world, then predict the most probable family; reward = prediction + curiosity - costs"""
        mix, rng = self.mix, self.rng; total = 0.0; lw = lw.copy()
        for a in seq:
            obs = np.array(mix.table[a][true_i]) + rng.normal(0, SIG, len(mix.table[a][true_i]))
            before = mix.post(lw); lw = lw + mix.loglik(a, obs); after = mix.post(lw)
            total += self.beta * kl(after, before) - self.cost                  # curiosity: bits of compression progress
        p = mix.post(lw); fam = {}
        for m, pi in zip(mix.models, p): fam[m.family] = fam.get(m.family, 0) + pi
        guess = max(fam, key=fam.get); total += 1.0 if guess == mix.models[true_i].family else -1.0
        return total
    def choose(self):
        mix = self.mix; post = mix.post(); N = {}; Q = {}
        def key(seq): return tuple(seq)
        frontier = [()]
        for t in range(self.sims):
            true_i = self.rng.choice(len(post), p=post)                         # a world sampled from the mixture
            seq = []
            for d in range(self.depth):
                k = key(seq); stats = N.setdefault(k, {a: 0 for a in ACTIONS}); q = Q.setdefault(k, {a: 0.0 for a in ACTIONS}); tot = sum(stats.values()) + 1
                un = [a for a in ACTIONS if stats[a] == 0]
                a = self.rng.choice(len(un)) if un else None
                a = un[a] if un else max(ACTIONS, key=lambda x: q[x] + self.c * math.sqrt(math.log(tot) / stats[x]))
                seq.append(a)
                if not un and d + 1 < self.depth: continue
                break
            while len(seq) < self.depth: seq.append(ACTIONS[self.rng.integers(len(ACTIONS))])
            # value of 'do first d+1 actions then predict'
            val = {n: self.rollout_value(true_i, mix.logw, seq[:n], n) for n in range(1, len(seq) + 1)}
            for n in range(1, len(seq) + 1):
                k = key(seq[:n - 1]); a = seq[n - 1]; stats = N.setdefault(k, {x: 0 for x in ACTIONS}); q = Q.setdefault(k, {x: 0.0 for x in ACTIONS})
                stats[a] += 1; q[a] += (val[n] - q[a]) / stats[a]
        root = N[()]; qroot = Q[()]
        # value of predicting now
        fam = mix.family_probs(); now = 2 * max(fam.values()) - 1
        best = max(ACTIONS, key=lambda a: qroot[a] if root[a] else -9)
        return best, (qroot[best] if root[best] else -9), now

def episode(world, rng, mode, max_exp=6, creative=False, beta=0.5, cost=0.05, sims=120, depth=3, stop_conf=0.9):
    mix = Mixture(library()); used = 0; hist = []; invented_flag = False
    while used < max_exp:
        fam = mix.family_probs(); conf = max(fam.values())
        if mode == 'random': a = ACTIONS[rng.integers(len(ACTIONS))]
        else:
            Pl = Plan(mix, rng, beta if mode == 'curious' else 0.0, cost, depth, sims)
            a, qv, now = Pl.choose()
            if now >= qv - 1e-9 and conf >= 0.6 and used > 0: break          # predicting now is worth at least as much as another experiment
        if mode == 'random' and used >= 4: break
        obs = np.array(world.series(*a)) + rng.normal(0, SIG, a[1]); ll = mix.update(a, obs); used += 1; hist.append((a, obs))
        if creative and not invented_flag:
            bits = -np.max(ll) / math.log(2) / len(obs)                         # best hypothesis: bits per observation vs the noise floor
            floor = 0.5 * math.log2(2 * math.pi * math.e * SIG ** 2) - math.log2(SIG * 1.0) * 0  # noise floor below is nominal, use chi-square instead
            chi2 = np.min([np.sum((np.array(mix.table[a][i]) - obs) ** 2) / SIG ** 2 / len(obs) for i in range(len(mix.models))])
            if chi2 > 4.0:                                                       # no known pattern compresses this: be creative
                mix.add(invented()); invented_flag = True
                for (a2, o2) in hist: mix.update(a2, o2)                         # new hypotheses are scored on all past data (logw for new models restarted)
    fam = mix.family_probs(); guess = max(fam, key=fam.get)
    return guess, used, invented_flag

def make_world(rng, composite):
    if not composite:
        f = rng.choice(['pos', 'neg', 'osc', 'drift']); a = PRIM[f][1][rng.integers(2)]; return Model(f, (a,), 0)
    if rng.random() < .5: return Model('sum:neg+pos', (rng.choice(PRIM['neg'][1]), rng.choice(PRIM['pos'][1])), 0)
    return Model('gate:pos*neg', (rng.choice(PRIM['pos'][1]), rng.choice((2.0, 3.0))), 0)
