"""Literal D(L,a,h) statistics and the D1-D3 union at p = q = 1 (python3 -I, run from this directory)."""
import sys
sys.path.insert(0, '.')
from selfjoin_check import stats   # noqa: E402

def D(L, a, h, tag):
    b = L // h
    X = [(tag, 'x', i, l) for i in range(h) for l in range(b)]
    R = [(x, (tag, 'y0', k)) for x in X for k in range(a)]
    S = [((tag, 'y0', k), (tag, 'z1', i)) for k in range(a) for i in range(h)]
    S += [((tag, 'y2', i, j, k), (tag, 'z2', i, j)) for i in range(h) for j in range(h) for k in range(a)]
    T = [((tag, 'z2', i, j), (tag, 'x', i, l)) for i in range(h) for j in range(h) for l in range(b)]
    return R, S, T

for (L, a, h) in [(4, 2, 2), (6, 3, 2), (6, 2, 3), (8, 4, 4), (9, 2, 3), (12, 5, 3), (16, 4, 8)]:
    st = stats(*D(L, a, h, 0))
    assert st['sizes'] == (L*a, a*h + a*h*h, L*h)
    assert st['fw'] == (L*a*a, 2*a*h*h, L*L) and st['rv'] == (a*L*L, a*a*(h + h*h), L*h*h)
    assert st['M'] == (L*a*h, 0, L*a*h) and (st['Cx'], st['Cy'], st['Cz']) == (L*a*h + L*min(a, h), a*h, a*h*h) and st['out'] == 0
print("D(L,a,h) statistics: 7 triples OK")

def place(R, S, T, k):  # k = 0: (R,S,T); 1: local R,S,T -> global S,T,R; 2: -> global T,R,S
    return [(R, S, T), (T, R, S), (S, T, R)][k]

u = 2
for u in (2, 3):
    p = q = 1
    parts = [D(u**(8*p-4*q), u**(6*q-4*p), u**(6*p-3*q), 1), D(u**(4*q), u**(4*p-2*q), u**(6*p-3*q), 2), D(u**(4*p), u**(6*p-4*q), u**(6*q-3*p), 3)]
    R, S, T = [], [], []
    for k, (r, s, t) in enumerate(parts):
        gR, gS, gT = place(r, s, t, k); R += gR; S += gS; T += gT
    st = stats(R, S, T)
    print(u, st['N'], st['fw'], st['C'], (st['Cx'], st['Cy'], st['Cz']))
    assert st['fw'] == (4*u**(8*q), 4*u**(8*p), 4*u**(16*p-8*q))
