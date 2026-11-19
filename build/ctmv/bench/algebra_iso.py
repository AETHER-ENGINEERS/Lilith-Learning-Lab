"""Isomorphism of small algebraic structures from examples: parity addition, sign multiplication, XOR on bits and more.
A 'note' states some facts  a op b = c.  We rebuild the operation table, then (1) canonicalise it up to renaming of the elements,
(2) list the laws it satisfies. Same canonical table = isomorphic. Same laws but different table = share a theory only."""
import itertools
def table(facts):
    els = sorted({x for f in facts for x in f}); idx = {e: i for i, e in enumerate(els)}; n = len(els)
    T = [[None] * n for _ in range(n)]
    for a, b, c in facts: T[idx[a]][idx[b]] = idx[c]
    return els, T
def canon(T):
    n = len(T); best = None
    for p in itertools.permutations(range(n)):
        inv = [0] * n
        for i, x in enumerate(p): inv[x] = i
        R = tuple(tuple(p[T[inv[i]][inv[j]]] for j in range(n)) for i in range(n))
        if best is None or R < best: best = R
    return best
def laws(T):
    n = len(T); L = []
    if all(T[a][b] is not None for a in range(n) for b in range(n)):
        if all(T[T[a][b]][c] == T[a][T[b][c]] for a in range(n) for b in range(n) for c in range(n)): L.append('associative')
        if all(T[a][b] == T[b][a] for a in range(n) for b in range(n)): L.append('commutative')
        e = [x for x in range(n) if all(T[x][a] == a == T[a][x] for a in range(n))]
        if e:
            L.append('has identity')
            if all(any(T[a][b] == e[0] for b in range(n)) for a in range(n)): L.append('every element has an inverse')
            if all(T[a][a] == e[0] for a in range(n)): L.append('x op x = identity (self-inverse)')
        if all(T[a][a] == a for a in range(n)): L.append('idempotent')
    else: L.append('incomplete table')
    return L
S = {
 'parity addition':   [('even','even','even'),('even','odd','odd'),('odd','even','odd'),('odd','odd','even')],
 'sign multiplication': [('+','+','+'),('+','-','-'),('-','+','-'),('-','-','+')],
 'bit XOR (1001 ^ ...)': [('0','0','0'),('0','1','1'),('1','0','1'),('1','1','0')],
 'rotate by 180 degrees': [('stay','stay','stay'),('stay','flip','flip'),('flip','stay','flip'),('flip','flip','stay')],
 'bit AND':           [('0','0','0'),('0','1','0'),('1','0','0'),('1','1','1')],
 'bit OR':            [('0','0','0'),('0','1','1'),('1','0','1'),('1','1','1')],
 'addition mod 3':    [(a, b, (a + b) % 3) for a in range(3) for b in range(3)],
 'rotating a triangle (0, 120, 240 degrees)': [(a, b, (a + b) % 3) for a in range(3) for b in range(3)],
}
def analyse(v):
    els, T = table([tuple(map(str, f)) for f in v]); return canon(T), laws(T)
res = {k: analyse(v) for k, v in S.items()}
groups = {}
for k, (c, l) in res.items(): groups.setdefault(c, []).append(k)
for c, ks in groups.items(): print('same structure:', ' = '.join(ks), '\n   laws:', '; '.join(res[ks[0]][1]))
