"""Padded G8(m) as one predicate, plus one X->X edge: pairwise reduced, role-expanded connected. python3 -I."""
import sys
from collections import defaultdict
sys.path.insert(0, '.')
from selfjoin_check import G8, stats, deg   # noqa: E402  (same directory)

def pad(R, S, T):
    R, S, T = set(R), set(S), set(T)
    Ro, Ri = deg(R); So, Si = deg(S); To, Ti = deg(T)
    X = set(Ro) | set(Ti); Y = set(Ri) | set(So); Z = set(Si) | set(To)
    p = 0
    for x in X:
        if (Ro[x] > 0) != (Ti[x] > 0):
            y, z = ('py', x), ('pz', x); R.add((x, y)); S.add((y, z)); T.add((z, x)); p += 1
    for y in Y:
        if (Ri[y] > 0) != (So[y] > 0):
            x, z = ('px', y), ('pz', y); R.add((x, y)); S.add((y, z)); T.add((z, x)); p += 1
    for z in Z:
        if (Si[z] > 0) != (To[z] > 0):
            x, y = ('px', z), ('py', z); R.add((x, y)); S.add((y, z)); T.add((z, x)); p += 1
    return R, S, T, p

def components(P):
    parent = {}
    def f(u):
        while parent.setdefault(u, u) != u:
            parent[u] = parent[parent[u]]; u = parent[u]
        return u
    for (u, v) in P:
        for (ru, rv) in (('a', 'b'), ('b', 'c'), ('c', 'a')):
            a, b = f((u, ru)), f((v, rv))
            if a != b: parent[a] = b
    return len({f(k) for k in list(parent)})

def pairwise_reduced(P):
    o, i = deg(P)
    return all(o[v] > 0 and i[v] > 0 for v in set(o) | set(i))

for m in (2, 3):
    R, S, T = G8(m)
    R2, S2, T2, p = pad(R, S, T)
    P = set(R2) | set(S2) | set(T2)
    print(f"m={m}: padded vertices {p}, |P| {len(P)}, components before {components(P)}")
    P.add((('x', 0), ('x', 1)))                     # one same-type edge X0 -> X1
    st = stats(P, P, P)
    B2 = min(st['fw'][0], st['rv'][0])
    print(f"   +edge: N={st['N']} C={st['C']} B2={B2} Out={st['out']} reduced={pairwise_reduced(P)} components={components(P)} C/(N+B2)={st['C']/(st['N']+B2):.3f}")
