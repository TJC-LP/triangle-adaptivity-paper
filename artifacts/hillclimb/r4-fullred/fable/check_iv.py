# Tier B: the gadget I_v of thm-fullred and its rotation union U_v, rebuilt from the paper's definition (Sec. 5),
# brute force for v = 1..3 and exact closed forms up to v = 8 (incl. the v = 8 ratio 45017942/39450457).
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import itertools, time
from fractions import Fraction as Fr
from lbcore import Ids, Inst, add_union, b2_bracket, ratio_bracket, fmt


def gen_iv(ids, v):
    """I_v: coordinates in [v]; X = {(A,B): A,B in [v]^3}, Y0 = [v]^4, Z1 = [v]^5, Y2 = {(A,B,E,e)}, Z2 = {(A,E,F): F in [v]^2};
    f(A,B) = (A, B1, B2) in Z1.  R = X x Y0 u {((A,B),(A,B,E,e))}; S = Y0 x Z1 u {((A,B,E,e),(A,E,F))};
    T = {(f(x), x)} u {((A,E,F),(A,B))}."""
    rng = range(v)
    cube = list(itertools.product(rng, repeat=3)); sq = list(itertools.product(rng, repeat=2))
    X = {(A, B): i for i, (A, B) in enumerate(itertools.product(cube, cube))}
    base = ids.fresh(len(X)); X = {k: base[i] for k, i in X.items()}
    Y0 = ids.fresh(v ** 4); Y0m = {k: Y0[i] for i, k in enumerate(itertools.product(rng, repeat=4))}
    Z1 = ids.fresh(v ** 5); Z1m = {k: Z1[i] for i, k in enumerate(itertools.product(rng, repeat=5))}
    Y2m = {}
    for A in cube:
        for B in cube:
            for E in cube:
                for e in rng:
                    Y2m[(A, B, E, e)] = None
    ys = ids.fresh(len(Y2m)); Y2m = {k: ys[i] for i, k in enumerate(Y2m)}
    Z2m = {}
    for A in cube:
        for E in cube:
            for F in sq:
                Z2m[(A, E, F)] = None
    zs = ids.fresh(len(Z2m)); Z2m = {k: zs[i] for i, k in enumerate(Z2m)}
    for (A, B), x in X.items():
        for y in Y0:
            yield ('R', x, y)
        fz = Z1m[(A[0], A[1], A[2], B[0], B[1])]
        yield ('T', fz, x)
        for E in cube:
            for e in rng:
                yield ('R', x, Y2m[(A, B, E, e)])
    for y in Y0:
        for z in Z1:
            yield ('S', y, z)
    for (A, B, E, e), y in Y2m.items():
        for F in sq:
            yield ('S', y, Z2m[(A, E, F)])
    for (A, E, F), z in Z2m.items():
        for B in cube:
            yield ('T', z, X[(A, B)])


def closed_iv(v):
    return dict(R=2 * v ** 10, S=v ** 12 + v ** 9, T=v ** 11 + v ** 6, Out=v ** 10 + v ** 12,
                al=4 * v ** 14, be=2 * v ** 14, ga=v ** 14 + v ** 7,
                alp=v ** 16 + v ** 10, bep=v ** 16 + v ** 13, gap=v ** 16 + 2 * v ** 11 + v ** 6,
                Cx=v ** 15 + v ** 11 + v ** 10 + v ** 6, Cy=v ** 12 + 2 * v ** 10 + v ** 9, Cz=2 * v ** 12 + v ** 10 + v ** 6)


def closed_union(v):
    c = closed_iv(v)
    return dict(N=3 * (v ** 12 + v ** 11 + 2 * v ** 10 + v ** 9 + v ** 6),
                C=v ** 15 + 3 * v ** 12 + v ** 11 + 4 * v ** 10 + v ** 9 + 2 * v ** 6,
                B2=7 * v ** 14 + v ** 7, Out=3 * (v ** 12 + v ** 10),
                bwd=3 * v ** 16 + v ** 13 + 2 * v ** 11 + v ** 10 + v ** 6,
                Csum=c['Cx'] + c['Cy'] + c['Cz'], fwdsum=c['al'] + c['be'] + c['ga'],
                bwdsum=c['alp'] + c['bep'] + c['gap'], Nsum=c['R'] + c['S'] + c['T'])


for v in (1, 2, 3):
    t0 = time.time()
    ids = Ids(); inst = Inst()
    for rel, a, b in gen_iv(ids, v):
        inst.add(rel, a, b)
    e = inst.evaluate(); c = closed_iv(v)
    assert e['adds'] == e['N']
    for key in c:
        assert e[key] == c[key], (v, key, e[key], c[key])
    assert e['fully_reduced'], (v, e)
    print(f"I_{v}: {fmt(e)}  closed forms exact  ({time.time() - t0:.0f}s)")
    ids = Ids(); inst = Inst()
    add_union(inst, [gen_iv(ids, v), gen_iv(ids, v), gen_iv(ids, v)])
    e = inst.evaluate(); u = closed_union(v)
    assert e['adds'] == e['N'] and e['fully_reduced']
    assert e['N'] == u['N'] and e['Cx'] == e['Cy'] == e['Cz'] == e['C'] == u['C'] and e['Out'] == u['Out']
    assert e['al'] == e['be'] == e['ga'] == u['B2'] and e['alp'] == e['bep'] == e['gap'] == u['bwd']
    print(f"U_{v}: {fmt(e)}  closed forms exact")
for v in range(1, 9):
    c = closed_iv(v); u = closed_union(v)
    assert u['C'] == u['Csum'] and u['B2'] == u['fwdsum'] and u['bwd'] == u['bwdsum'] and u['N'] == 3 * u['Nsum']
    B2 = u['B2'] if u['bwd'] >= u['B2'] else None
    r = Fr(u['C'], u['N'] + u['B2'])
    print(f"U_{v} closed: N={u['N']} C={u['C']} B2(fwd)={u['B2']} bwd={u['bwd']} ({'fwd<=bwd' if u['bwd'] >= u['B2'] else 'BWD SMALLER'}) Out={u['Out']} C/(N+B2)={r} = {float(r):.4f}")
r8 = Fr(closed_union(8)['C'], closed_union(8)['N'] + closed_union(8)['B2'])
print(f"v = 8 ratio exact = {r8}; claim 45017942/39450457: {r8 == Fr(45017942, 39450457)}; > 1: {r8 > 1}")
# per-x option costs of I_v (paper: c_R(x) = v^9 + v^6 + 2v^4, c_T(x) = v^9 + v^5 + v^4 + 1, difference v^6 - v^5 + v^4 - 1 >= 0)
for v in range(1, 9):
    cR = v ** 9 + v ** 6 + 2 * v ** 4; cT = v ** 9 + v ** 5 + v ** 4 + 1
    assert cR - cT == v ** 6 - v ** 5 + v ** 4 - 1 >= 0
print("per-x option costs: c_R - c_T = v^6 - v^5 + v^4 - 1 >= 0 for v = 1..8, so option T is chosen at every x")
# obstruction: on a fully reduced instance Out >= max(|R|,|S|,|T|) >= N/3 and Out <= B2 (checked by fuzz.py on random instances)
