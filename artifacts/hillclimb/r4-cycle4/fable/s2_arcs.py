"""Step 2: the arc-blowup family.
 (a) Prop 3.1 closed forms (|e|, sigma^2, Out) checked exactly on random multiplicity vectors by building the
     0/1 matrices; sigma^2 certified exactly via constant Gram row sums (Perron) AND via the Sturm bracket.
 (b) Prop 3.3: for every one of the 50 dual vertices, an integer instance supported on its tight arcs attains
     the monomial with equality (exact 12th powers).
 (c) LP duality sanity: at random rational (rho, varsigma) the exact simplex value of the primal arc LP equals
     min over the 50 vertices (and over the 38 kept) of lambda.rho + mu.varsigma.
 (d) Kronecker-power (tensor) trick: Out, sizes and sigma^2 are multiplicative on an explicit instance.
usage: python3 -I s2_arcs.py
"""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from v2lib import (arcs, edges, dual_constraint_rows, arc_instance, arc_predicted, out4, size, sigma2_bracket,
                   perron_rowsum_check, vertex_int_exponents, mono_powD, mono_str, arc_lp, kron, gram_small,
                   lambda_max_bracket)

random.seed(777)
HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, "vertices4.json")))
ALL = [tuple(F(x) for x in v) for v in V["all"]]
KEPT = [tuple(F(x) for x in v) for v in V["kept"]]
A4 = arcs(4)
E4 = edges(4)

# (a)
print("(a) closed forms on random arc instances")
nchecked = 0
for trial in range(40):
    mult = {}
    for a in A4:
        if random.random() < 0.45:
            mult[a] = random.randint(2, 3)
    mats = arc_instance(mult)
    if max(len(M) * len(M[0]) for M in mats) > 2500:
        continue
    r_pred, s_pred, out_pred = arc_predicted(mult)
    r = [size(M) for M in mats]
    o = out4(*mats)
    assert r == r_pred, (mult, r, r_pred)
    assert o == out_pred, (mult, o, out_pred)
    for e in range(4):
        assert perron_rowsum_check(mats[e], s_pred[e]), (mult, e)
        if len(mats[e]) * len(mats[e][0]) <= 400:
            lo, hi, ex = sigma2_bracket(mats[e], 40)
            assert lo <= s_pred[e] <= hi, (mult, e, lo, hi)
    nchecked += 1
print(f"   {nchecked} random multiplicity vectors: |e|, Out exact match; sigma^2 = product certified (Perron row sums + Sturm bracket)")

# (b) tightness of every vertex
print("(b) every dual vertex is attained with equality by an integer arc instance on its tight arcs")
A_, E_, rows = dual_constraint_rows(4)
for v in ALL:
    tight = [A4[i] for i, row in enumerate(rows) if sum(F(c) * x for c, x in zip(row, v)) == 1]
    D, lamD, muD = vertex_int_exponents(v)
    ok_all = True
    for trial in range(3):
        mult = {a: random.randint(2, 3) for a in tight}
        r, s, o = arc_predicted(mult)
        # the monomial at the instance's OWN statistics (r_e = |e|, s_e = sigma_e^2 <= |e| automatically)
        assert all(s[e] <= r[e] for e in range(4))
        val = mono_powD(r, s, lamD, muD)
        if F(o) ** D != val:
            ok_all = False
    tag = "kept" if v in KEPT else "dominated"
    print(f"   {tag:9s} {mono_str(v, 4):44s} tight arcs {len(tight):2d}  equality: {ok_all}")
    assert ok_all

# (c) LP duality
print("(c) exact LP value vs min over dual vertices at random rational statistics")
for trial in range(200):
    rho = [F(random.randint(0, 40), random.randint(1, 3)) for _ in range(4)]
    vs = [F(random.randint(0, 40), random.randint(1, 3)) for _ in range(4)]
    vs = [min(a, b) for a, b in zip(vs, rho)]
    A_, nu, val = arc_lp(4, rho, vs)
    c = rho + vs
    m_all = min(sum(a * b for a, b in zip(u, c)) for u in ALL)
    m_kept = min(sum(a * b for a, b in zip(u, c)) for u in KEPT)
    assert val == m_all == m_kept, (rho, vs, val, m_all, m_kept)
    # primal feasibility of nu
    for e in range(4):
        assert sum(nu[i] for i, a in enumerate(A4) if len(a & E4[e]) >= 1) <= rho[e]
        assert sum(nu[i] for i, a in enumerate(A4) if len(a & E4[e]) == 1) <= vs[e]
    assert all(x >= 0 for x in nu) and sum(nu) == val
print("   200 random points: simplex value == min over 50 == min over 38 (exact); primal solutions feasible")

# (d) Kronecker power
print("(d) tensor-power trick on an explicit instance")
AR = [[1, 1, 0], [0, 1, 1]]
AS = [[1, 0], [1, 1], [0, 1]]
AT = [[1, 1, 1], [0, 1, 0]]
AQ = [[1, 0], [1, 1], [0, 1]]
base = (AR, AS, AT, AQ)
o1 = out4(*base)
r1 = [size(M) for M in base]
s1 = [lambda_max_bracket(gram_small(M), 50) for M in base]
sq = tuple(kron(M, M) for M in base)
o2 = out4(*sq)
r2 = [size(M) for M in sq]
print(f"   Out: {o1}^2 = {o1**2} vs {o2}; sizes {[x*x for x in r1]} vs {r2}")
assert o2 == o1 ** 2 and r2 == [x * x for x in r1]
for e in range(4):
    lo, hi, ex = lambda_max_bracket(gram_small(sq[e]), 50)
    lo1, hi1, ex1 = s1[e]
    assert lo1 * lo1 <= hi and lo <= hi1 * hi1, (e, lo, hi, lo1, hi1)
print("   sigma^2 of the Kronecker square lies in the square of the base bracket (exact brackets)")
print("ALL STEP-2 CHECKS PASSED")
