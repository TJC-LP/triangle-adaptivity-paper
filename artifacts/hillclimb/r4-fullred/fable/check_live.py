# Brute-force verification of the live gadget closed forms, the union, and the family L(v) (v = 2, 3; v = 4 separately).
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import sys, random, time, itertools
from fractions import Fraction as Fr
from lbcore import Ids, Inst, add_union, b2_bracket, ratio_bracket, fmt
from live_gadget import (params_ok, gen_live, closed_live, union_closed, family_params, family_closed,
                         general_params, build_union)

KEYS = ('R', 'S', 'T', 'N', 'Out', 'Cx', 'Cy', 'Cz', 'al', 'be', 'ga', 'alp', 'bep', 'gap')

# 1. single gadgets: every parameter tuple in a box, closed forms vs brute force
cnt = 0; worst_ratio_cx = None
tuples = []
for t in range(1, 5):
    for p in range(t, 4 * t + 1, t):
        for q in range(1, 7):
            for g in range(1, 7):
                for k in range(1, 4):
                    for w in range(1, 5):
                        if params_ok(p, q, t, g, k, w):
                            tuples.append((p, q, t, g, k, w))
for pr in tuples:
    ids = Ids(); inst = Inst()
    for rel, a, b in gen_live(ids, *pr):
        inst.add(rel, a, b)
    e = inst.evaluate(); c = closed_live(*pr)
    assert e['adds'] == e['N'], ('duplicate tuples', pr)
    assert e['fully_reduced'], ('not fully reduced', pr, e)
    for key in KEYS:
        assert e[key] == c[key], (pr, key, e[key], c[key])
    assert e['Cx'] >= c['pqt']
    cnt += 1
print(f"[1] single live gadget: {cnt} parameter tuples; brute force == closed forms for {KEYS}; all fully reduced; Cx >= pqt")

# 2. random union triples
rng = random.Random(20261009)
small = [pr for pr in tuples if pr[0] * pr[1] * pr[2] <= 64]
cnt = 0
for _ in range(60):
    trip = (rng.choice(small), rng.choice(small), rng.choice(small))
    e = build_union(trip).evaluate(); c = union_closed(*trip)
    assert e['adds'] == e['N'] and e['fully_reduced'], trip
    for key in ('R', 'S', 'T', 'N', 'Out', 'Cx', 'Cy', 'Cz', 'al', 'be', 'ga', 'alp', 'bep', 'gap', 'C'):
        assert e[key] == c[key], (trip, key, e[key], c[key])
    # each root costs at least pqt of its designated copy
    assert e['Cx'] >= trip[0][0] * trip[0][1] * trip[0][2]
    assert e['Cy'] >= trip[1][0] * trip[1][1] * trip[1][2]
    assert e['Cz'] >= trip[2][0] * trip[2][1] * trip[2][2]
    cnt += 1
print(f"[2] live union: {cnt} random triples; brute force == closed forms (sizes, costs, Out, fwd+bwd norms); fully reduced; C_v >= p_v q_v t_v")

# 3. the family L(v)
vs = [int(a) for a in sys.argv[1:]] or [2, 3]
for v in vs:
    t0 = time.time()
    pr = family_params(v)
    e = build_union((pr, pr, pr)).evaluate()
    f = family_closed(v); g1 = closed_live(*pr)
    assert e['adds'] == e['N']
    assert e['fully_reduced'], e
    assert e['N'] == f['N'] and e['C'] == f['C'] and e['Cx'] == e['Cy'] == e['Cz'] == f['C'] and e['Out'] == f['Out']
    assert e['al'] == e['be'] == e['ga'] == f['fwd'] and e['alp'] == e['bep'] == e['gap'] == f['bwd']
    assert g1['Cx'] == f['Cx_gadget'] and g1['Cy'] == f['Cy_gadget'] and g1['Cz'] == f['Cz_gadget']
    assert f['Cx_gadget'] + f['Cy_gadget'] + f['Cz_gadget'] == f['C']
    lo, hi, m = b2_bracket(e)
    assert lo == hi == f['fwd'] and f['fwd'] < f['bwd']
    r0, r1 = ratio_bracket(e)
    print(f"[3] L(v={v}): {fmt(e)}  ratio exact = {r0} = {float(r0):.4f}  time {time.time() - t0:.0f}s")
    print(f"    gadget costs (Cx,Cy,Cz) = ({g1['Cx']},{g1['Cy']},{g1['Cz']}); claim 'every root >= v^12+v^10+3v^8+v^7' = {v**12 + v**10 + 3*v**8 + v**7}: {e['C'] >= v**12 + v**10 + 3*v**8 + v**7}")
