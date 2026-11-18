"""Generate benchmark vaults with planted ground truth for testing CTMV claims.
Usage: python3 gen_vaults.py OUTDIR NVAULTS   (needs fastembed; embeds notes with two real models)"""
import json, os, random, sys, hashlib, zlib
import numpy as np

DOMAINS = {
 'software':    dict(C='clients', S='requests', U='server', P='cluster'),
 'audio':       dict(C='microphones', S='sound', U='amplifier', P='room'),
 'ecology':     dict(C='animals', S='births', U='habitat', P='ecosystem'),
 'economics':   dict(C='depositors', S='withdrawals', U='bank', P='market'),
 'kitchen':     dict(C='cooks', S='heat', U='oven', P='kitchen'),
 'traffic':     dict(C='drivers', S='cars', U='junction', P='road network'),
 'epidemiology': dict(C='people', S='infections', U='ward', P='town'),
 'electronics': dict(C='circuits', S='current', U='transistor', P='board'),
}
FLAVOR = {
 'software': ['The team reviews this at the weekly standup.', 'Logs for this are kept for thirty days.', 'It was first noticed after a release.'],
 'audio': ['The sound check happens before every show.', 'Cables are labelled by colour.', 'It was first noticed during a rehearsal.'],
 'ecology': ['Field counts are made each spring.', 'Records go back several decades.', 'It was first noticed after a dry summer.'],
 'economics': ['Quarterly reports cover this in detail.', 'Regulators publish figures every month.', 'It was first noticed after a policy change.'],
 'kitchen': ['The recipe card sits by the stove.', 'Timers are set before each batch.', 'It was first noticed on a busy Saturday.'],
 'traffic': ['Counters on the main road log this hourly.', 'The council reviews it each year.', 'It was first noticed during the holidays.'],
 'epidemiology': ['Weekly surveillance reports include this.', 'Case data is anonymised.', 'It was first noticed during winter.'],
 'electronics': ['The bench notes are kept in a folder.', 'Parts are stored in labelled drawers.', 'It was first noticed on a prototype.'],
}
PATTERNS = {
 'positive_feedback': ["Once {S} start to grow, the {U} responds in a way that produces still more {S}, and the {P} runs away from normal.", "Each rise in {S} from the {C} pushes the {U} to generate more {S}, so the effect snowballs.", "The more {S} the {C} produce, the more the {U} amplifies them, and nothing in the {P} stops the growth."],
 'negative_feedback': ["When {S} rise, the {U} pushes them back down, so the {P} settles near a steady level.", "The {C} notice too many {S} and the {U} corrects, keeping the {P} stable.", "Any surge of {S} is damped by the {U}, which restores balance among the {C}."],
 'bottleneck': ["All {S} from the {C} must pass through one narrow {U}, so the whole {P} can go no faster than that part.", "A single {U} limits how many {S} the {P} can handle, and the {C} wait behind it.", "Throughput of the {P} is set by its slowest {U}; extra {S} from the {C} only pile up."],
 'buffer': ["A {U} absorbs bursts of {S} from the {C} and releases them slowly, smoothing the load on the {P}.", "Spare {S} are held in a {U} until the {C} need them, so the {P} rides out shortages.", "The {U} stores surplus {S} so that the {P} stays steady when the {C} are quiet."],
 'threshold_cascade': ["Nothing happens until {S} cross a limit; then one failing {U} pushes its neighbours over their limits and the {P} collapses in a chain.", "When one {U} fails, the {S} it carried move to others in the {P}, which then fail in turn among the {C}.", "A small shock tips a single {U} past its limit, and the {S} spread failure through the whole {P}."],
 'oscillation': ["The {P} overshoots, corrects too late, overshoots the other way, and the {S} swing back and forth.", "Because the {C} react to old {S}, the {U} keeps over-correcting and the {P} cycles up and down.", "A delay between {S} and the response of the {U} makes the {P} rock in regular swings."],
 'redundancy': ["Several copies of the {U} share the {S} of the {C}, so if one fails the {P} carries on.", "Spare units stand ready in the {P}; when one {U} is lost the {C} still get their {S}.", "The {P} keeps duplicate parts so no single loss of a {U} stops {S} reaching the {C}."],
 'contagion': ["{S} spread from one of the {C} to the next through contact until the {P} is saturated.", "Each of the {C} that receives {S} passes them on, so the {S} fan out through the {P} like a wave.", "Starting at one {U}, the {S} move outward across the {P} from neighbour to neighbour."],
}
PDESC = {  # short abstract descriptions used by the automatic tagger
 'positive_feedback': 'a loop where the output increases the input so growth feeds itself and runs away',
 'negative_feedback': 'a correction that pushes a value back down so the system settles at a steady level',
 'bottleneck': 'one narrow part limits the throughput of the whole system',
 'buffer': 'a store that absorbs bursts and releases slowly to smooth the load',
 'threshold_cascade': 'one failure pushes neighbours past their limits and failure spreads in a chain',
 'oscillation': 'delayed correction makes the system overshoot and swing back and forth',
 'redundancy': 'spare duplicate parts keep the system working when one fails',
 'contagion': 'something spreads from one member to the next through contact until all are reached',
}
POLY = [  # surface word, (domainA, senseA), (domainB, senseB)
 ('bridge', ('software', 'The adapter acts as a bridge between the old and new systems.'), ('traffic', 'The bridge on the river road is closed for repairs.')),
 ('cell', ('ecology', 'Each cell divides when nutrients are plentiful.'), ('electronics', 'The cell in the pack is rated for a few hundred cycles.')),
 ('stock', ('kitchen', 'The stock simmers for hours before it is strained.'), ('economics', 'The stock moved sharply after the announcement.')),
 ('pitch', ('audio', 'The pitch of the tone drifts when the string warms up.'), ('economics', 'The pitch to investors took twenty minutes.')),
 ('current', ('electronics', 'The current through the coil is measured at the test point.'), ('ecology', 'The current carries nutrients along the coast.')),
 ('pool', ('software', 'The pool of workers is sized for the daily peak.'), ('epidemiology', 'The pool of susceptible people shrinks as immunity grows.')),
]
TRIPLES = [  # x, y, z (entity phrases): old note says x prevents y; new note says x causes y; z is a different object
 ('long cache lifetime', 'stale reads', 'fast reads'), ('early retries', 'outage', 'quick recovery'), ('high interest rates', 'inflation', 'unemployment'),
 ('strict curfews', 'crowding', 'quiet streets'), ('heavy compression', 'clipping', 'small files'), ('crop rotation', 'soil depletion', 'better yields'),
 ('wide lanes', 'congestion', 'higher speeds'), ('dense planting', 'blight', 'shade'), ('deep fryers', 'grease fires', 'crisp food'),
 ('mass testing', 'outbreaks', 'false alarms'), ('large batches', 'latency', 'lower cost'), ('tight tolerances', 'failures', 'higher cost'),
 ('free parking', 'traffic', 'busy shops'), ('loud monitors', 'hearing loss', 'clear mixes'), ('lean stock', 'shortages', 'low waste'),
 ('fast clocks', 'overheating', 'quick answers'), ('quarantine', 'spread', 'isolation'), ('deregulation', 'bank runs', 'cheap credit'),
 ('culling', 'collapse', 'fewer predators'), ('extra yeast', 'collapse', 'faster rise'),
]
CHAINS = [  # four-step causal chains
 ['retry load', 'queue depth', 'timeouts', 'user churn'], ['feedback gain', 'loop noise', 'speaker strain', 'blown driver'],
 ['rabbit births', 'grass loss', 'fox numbers', 'rabbit decline'], ['bank panic', 'asset sales', 'price falls', 'credit freeze'],
 ['oven heat', 'crust burn', 'bitter taste', 'wasted batch'], ['rain on roads', 'wet braking', 'rear end crashes', 'lane closures'],
 ['crowded wards', 'staff fatigue', 'missed handwashing', 'ward outbreaks'], ['high voltage', 'arcing', 'contact pitting', 'relay failure'],
 ['disk latency', 'slow queries', 'page timeouts', 'abandoned carts'], ['mic proximity', 'echo build up', 'howl', 'listener walkout'],
 ['drought', 'dry pasture', 'herd stress', 'milk drop'], ['rate rise', 'loan defaults', 'bank stress', 'lending cut'],
]
REWRITTEN = {}
for _l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rewritten.txt'), encoding='utf-8'):
    if _l.strip():
        _p, _d, _t = _l.rstrip('\n').split('|', 2); REWRITTEN[(_p, _d)] = _t
slug = lambda s: s.replace(' ', '_')

def mk_note(name, title, body, domain, claims, links=None):
    return dict(name=name, title=title, body=body, domain=domain, claims=[list(c) for c in claims], links=links or [])

def gen_vault(seed, style='templated'):
    R = random.Random(seed)
    doms = R.sample(sorted(DOMAINS), 5); pats = R.sample(sorted(PATTERNS), 6)
    notes, truth = [], dict(bridges=[], false_friends=[], supersede=[], disputes=[], benign=[], chains=[], pattern_of={})
    cell = {}
    for d in doms:
        for p in pats:
            if R.random() < 0.7:
                nm = f'{d}-{p.split("_")[0]}-{len(notes)}'
                body = (R.choice(PATTERNS[p]).format(**DOMAINS[d]) if style == 'templated' else REWRITTEN[(p, d)]) + ' ' + R.choice(FLAVOR[d])
                title = f'Notes on the {DOMAINS[d]["U"]} in the {DOMAINS[d]["P"]} ({len(notes)})'
                subj = slug(f'{d}_{DOMAINS[d]["U"]}_{len(notes)}')
                notes.append(mk_note(nm, title, body, d, [(subj, 'is', p)])); cell[nm] = p; truth['pattern_of'][nm] = p
    pnames = list(cell)
    for i in range(len(pnames)):
        for j in range(i + 1, len(pnames)):
            a, b = pnames[i], pnames[j]
            if cell[a] == cell[b] and a.split('-')[0] != b.split('-')[0]: truth['bridges'].append([a, b])
    # false friends: same surface word, different senses and different patterns
    for k, (w, (da, sa), (db, sb)) in enumerate(R.sample(POLY, 4)):
        pa, pb = R.sample(sorted(PATTERNS), 2)
        a = f'poly-{w}-a{k}'; b = f'poly-{w}-b{k}'
        notes.append(mk_note(a, f'About the {w} ({da})', sa + ' ' + R.choice(FLAVOR[da]), da, [(slug(f'{w}_{da}'), 'is', f'{w}_sense_{da}')]))
        notes.append(mk_note(b, f'About the {w} ({db})', sb + ' ' + R.choice(FLAVOR[db]), db, [(slug(f'{w}_{db}'), 'is', f'{w}_sense_{db}')]))
        truth['false_friends'].append([a, b])
    # supersession, disputes, benign
    tr = R.sample(TRIPLES, 6 + 4 + 6); queries = []
    for k, (x, y, z) in enumerate(tr[:6]):
        old, new = f'old-{slug(x)}', f'new-{slug(x)}'
        notes.append(mk_note(old, f'Does {x} stop {y}?', f'We believe {x} helps avoid {y} in our setup. {R.choice(FLAVOR[R.choice(doms)])}', 'meta', [(slug(x), 'prevents', slug(y))]))
        notes.append(mk_note(new, f'Update on {x} and {y}', f'Correction: {x} actually brings {y}; the earlier note was wrong. {R.choice(FLAVOR[R.choice(doms)])}', 'meta', [(slug(x), 'causes', slug(y)), (new, 'supersedes', old)], links=[old]))
        truth['supersede'].append(dict(old=old, new=new)); queries.append(dict(id=f'sup{k}', type='supersede', text=f'does {x} lead to {y}?', relevant=[new], stale=[old]))
    for k, (x, y, z) in enumerate(tr[6:10]):
        a, b = f'dispute-a-{slug(x)}', f'dispute-b-{slug(x)}'
        notes.append(mk_note(a, f'Author A on {x}', f'In my experience {x} helps prevent {y}. {R.choice(FLAVOR[R.choice(doms)])}', 'meta', [(slug(x), 'prevents', slug(y))]))
        notes.append(mk_note(b, f'Author B on {x}', f'I have seen {x} cause {y} more than once. {R.choice(FLAVOR[R.choice(doms)])}', 'meta', [(slug(x), 'causes', slug(y))]))
        truth['disputes'].append([a, b]); queries.append(dict(id=f'dis{k}', type='dispute', text=f'does {x} lead to {y}?', relevant=[a, b], stale=[]))
    for k, (x, y, z) in enumerate(tr[10:]):
        a, b = f'benign-a-{slug(x)}', f'benign-b-{slug(x)}'
        notes.append(mk_note(a, f'{x} and {y}', f'Our data shows {x} brings {y}. {R.choice(FLAVOR[R.choice(doms)])}', 'meta', [(slug(x), 'causes', slug(y))]))
        notes.append(mk_note(b, f'{x} and {z}', f'We also find {x} protects {z}. {R.choice(FLAVOR[R.choice(doms)])}', 'meta', [(slug(x), 'prevents', slug(z))]))
        truth['benign'].append([a, b])
    # causal chains
    for k, ch in enumerate(R.sample(CHAINS, 6)):
        names = []
        for i in range(3):
            nm = f'chain{k}-{i}'; names.append(nm)
            body = f'A rise in {ch[i]} is followed by a rise in {ch[i + 1]}, as the team has seen before. {R.choice(FLAVOR[R.choice(doms)])}'
            notes.append(mk_note(nm, f'Observation: {ch[i]} and {ch[i + 1]}', body, 'meta', [(slug(ch[i]), 'causes', slug(ch[i + 1]))]))
        truth['chains'].append(names); queries.append(dict(id=f'chain{k}', type='chain', text=f'what does a rise in {ch[0]} eventually lead to?', relevant=names, stale=[]))
    for i in range(20):  # filler notes with no claims
        d = R.choice(doms)
        notes.append(mk_note(f'filler-{i}', f'Misc {d} note {i}', ' '.join(R.sample(FLAVOR[d], 2)) + f' Item {i} was logged.', d, []))
    R.shuffle(notes)
    return dict(seed=seed, notes=notes, truth=truth, queries=queries, doms=doms, pats=pats)

def noise(vault, R, p=1.0, c=0.0, q=0.0, a=1.0):
    """Degrade the true claims like an imperfect extractor: keep each with prob p, rename entities with prob c, add a wrong pattern with prob q."""
    out = {}
    pats = sorted(PATTERNS)
    for n in vault['notes']:
        cl = []
        for (s, r, o) in n['claims']:
            if R.random() > p: continue
            if r == 'is' and o in PATTERNS and R.random() > a: o = R.choice([x for x in pats if x != o])   # classifier mistake
            if r != 'is' and r != 'supersedes' and R.random() < c: s = s + '_x'   # entity not canonicalised
            if r == 'supersedes' and R.random() < c: o = o + '_x'
            cl.append([s, r, o])
        if q and n['domain'] != 'meta' and R.random() < q:
            cl.append([slug(n['name']) + '_w', 'is', R.choice(pats)])
        out[n['name']] = cl
    return out

VARIANTS = {  # name -> (p, c, q)
 'oracle': (1, 0, 0), 'recall80': (.8, 0, 0), 'recall50': (.5, 0, 0), 'recall30': (.3, 0, 0),
 'canon30': (1, .3, 0), 'wrong20': (1, 0, .2), 'realistic': (.7, .2, .1),
 'acc90': (1, 0, 0, .9), 'acc70': (1, 0, 0, .7), 'acc50': (1, 0, 0, .5),
}

TAU = float(os.environ.get('TAU', '0.55'))
def main(out, n, style):
    from fastembed import TextEmbedding
    os.makedirs(out, exist_ok=True)
    models = {'bge': TextEmbedding('BAAI/bge-small-en-v1.5'), 'minilm': TextEmbedding('sentence-transformers/all-MiniLM-L6-v2')}
    cache = {}
    def emb(m, texts):
        miss = [t for t in texts if (m, t) not in cache]
        if miss:
            for t, v in zip(miss, models[m].embed(miss)): cache[(m, t)] = [round(float(x), 5) for x in v]
        return [cache[(m, t)] for t in texts]
    pd_names = sorted(PDESC); pd_vec = {m: np.array(emb(m, [PDESC[p] for p in pd_names])) for m in models}
    for seed in range(n):
        v = gen_vault(seed, style); v['style'] = style; R = random.Random(1000 + seed)
        text = lambda nt: nt['title'] + '. ' + nt['body']
        v['vec'] = {m: dict(zip([x['name'] for x in v['notes']], emb(m, [text(x) for x in v['notes']]))) for m in models}
        for qq in v['queries']: qq['vec'] = {m: emb(m, [qq['text']])[0] for m in models}
        v['variants'] = {k: noise(v, random.Random(zlib.crc32(f"{seed}-{k}".encode())), *pc) for k, pc in VARIANTS.items()}
        # automatic tagger: few-shot. Prototype of each pattern = mean embedding of example sentences from domains NOT in this vault
        # (what a user could supply as labelled examples); assign a pattern when the best similarity is high enough.
        others = [d for d in sorted(DOMAINS) if d not in v['doms']]
        ex = lambda p, d: (REWRITTEN[(p, d)] if style != 'templated' else PATTERNS[p][0].format(**DOMAINS[d]))
        proto = np.array([np.mean(np.array(emb('bge', [ex(p, d) for d in others])), axis=0) for p in pd_names]); proto /= np.linalg.norm(proto, axis=1, keepdims=True)
        M = np.array([v['vec']['bge'][x['name']] for x in v['notes']]); sims = M @ proto.T
        tag, correct, tot, fp, asg = {}, 0, 0, 0, 0
        for x, row in zip(v['notes'], sims):
            j = int(row.argmax()); pat = pd_names[j]; t = v['truth']['pattern_of'].get(x['name'])
            if row[j] > TAU and x['domain'] != 'meta':
                tag[x['name']] = [[slug(x['name']) + '_auto', 'is', pat]]; asg += 1
                if t is None: fp += 1
                elif t == pat: correct += 1
            else: tag[x['name']] = []
            if t: tot += 1
        v['variants']['tagger'] = tag; v['tagger_acc'] = correct / max(1, tot); v['tagger_assigned'] = asg; v['tagger_fp'] = fp
        json.dump(v, open(os.path.join(out, f'vault_{seed:03d}.json'), 'w'))
        print(seed, len(v['notes']), 'notes', 'bridges', len(v['truth']['bridges']), 'tagger acc %.2f assigned %d fp %d' % (v['tagger_acc'], v['tagger_assigned'], v['tagger_fp']), flush=True)

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else 'templated')
