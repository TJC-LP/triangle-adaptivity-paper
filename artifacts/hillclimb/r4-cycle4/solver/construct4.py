"""Exact check of the 4-cycle lower construction on a grid of integer statistics.

For integer statistics 1 <= s_e <= r_e (e in R,S,T,Q):
  1. U_4^12 = min over the 38 needed monomials of prod r_e^(12 lam_e) s_e^(12 mu_e)  (exact integers;
     all exponents have denominators dividing 12).
  2. Solve the arc LP  max sum nu_A  s.t.  sum_{A∩e≠∅} nu_A <= log r_e, sum_{|A∩e|=1} nu_A <= log s_e
     (float logs approximated by Fractions; the exact simplex returns a vertex).  n_A = exp(nu_A).
  3. Integer multiplicities: n~_A = floor(n_A) for the 12 non-full arcs, repaired downward until the
     four norm constraints  prod_{|A∩e|=1} n~_A <= s_e  hold EXACTLY; then
     m = min_e floor( r_e / prod_{A∩e≠∅, A≠full} n~_A )  (exact integer division).  Requires m >= 1.
  4. Out_int = m * prod n~_A.  Check Out_int^12 * 16^12 > U_4^12 exactly, and record the exact maximum
     of U_4 / Out_int over the grid (as a 12th root of a rational, printed as float).
  5. For a sample of grid points the actual 0/1 matrices are built (cyc4.arc_instance) and Out,
     the sizes, and sigma^2 brackets are recomputed exactly to validate the closed forms.
Also checks that the LP value agrees with log U_4 to float precision (duality sanity check).

usage: python3 -I construct4.py grid <MAX>            (exhaustive 1 <= s_e <= r_e <= MAX)
       python3 -I construct4.py random <n> <seed> <RMAX>
Exit status 0 iff every check passes.
"""
import os
import sys
import math
import random
import itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from lp_vertices import vertices, prune
from exact_lp import solve_lp
from cyc4 import arc_instance, out4, size, sigma2_lower, sigma2_upper, all_arcs

EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]
ARCS = all_arcs(4)
FULL = frozenset(range(4))
NONFULL = [a for a in ARCS if a != FULL]


def meets(arc, e):
    return len(arc & set(EDGES[e]))


A_, E_, VERTS = vertices(4)
KEPT = prune(VERTS, 4)
assert len(KEPT) == 38
VINFO = [([int(q * 12) for q in v[:4]], [int(q * 12) for q in v[4:]]) for v in KEPT]
for v in KEPT:
    for q in v:
        assert (q * 12).denominator == 1


def U4_pow12(r, s):
    best = None
    for lam, mu in VINFO:
        val = 1
        for e in range(4):
            val *= r[e] ** lam[e] * s[e] ** mu[e]
        if best is None or val < best:
            best = val
    return best


def lp_solution(r, s):
    """Return (value, nu dict) for the arc LP with float logs."""
    nvar = len(ARCS)
    c = [-1] * nvar  # maximise sum nu
    A_ub, b_ub = [], []
    for e in range(4):
        row = [1 if meets(a, e) >= 1 else 0 for a in ARCS]
        A_ub.append(row)
        b_ub.append(Fraction(math.log(r[e])).limit_denominator(10 ** 9))
        row = [1 if meets(a, e) == 1 else 0 for a in ARCS]
        A_ub.append(row)
        b_ub.append(Fraction(math.log(s[e])).limit_denominator(10 ** 9))
    st, x, val = solve_lp(c, A_ub, b_ub)
    assert st == 'optimal', st
    return -val, {a: float(x[i]) for i, a in enumerate(ARCS)}


def construct(r, s):
    val, nu = lp_solution(r, s)
    n = {a: max(1, int(math.floor(math.exp(nu[a]) + 1e-9))) for a in NONFULL}
    # repair norm constraints exactly (float error could overshoot)
    changed = True
    while changed:
        changed = False
        for e in range(4):
            prod = 1
            for a in NONFULL:
                if meets(a, e) == 1:
                    prod *= n[a]
            if prod > s[e]:
                # decrement the largest involved multiplicity > 1
                cand = [a for a in NONFULL if meets(a, e) == 1 and n[a] > 1]
                assert cand, (r, s, n)
                a = max(cand, key=lambda t: n[t])
                n[a] -= 1
                changed = True
    m = None
    for e in range(4):
        prod = 1
        for a in NONFULL:
            if meets(a, e) >= 1:
                prod *= n[a]
        me = r[e] // prod
        m = me if m is None else min(m, me)
    assert m >= 1, (r, s, n, m)
    n[FULL] = m

    def feasible(nn):
        for e in range(4):
            p1 = 1
            p2 = 1
            for a in ARCS:
                k = meets(a, e)
                if k >= 1:
                    p1 *= nn[a]
                if k == 1:
                    p2 *= nn[a]
            if p1 > r[e] or p2 > s[e]:
                return False
        return True

    assert feasible(n)
    # greedy improvement: raise any multiplicity by one while all eight constraints stay satisfied
    improved = True
    while improved:
        improved = False
        for a in ARCS:
            n[a] += 1
            if feasible(n):
                improved = True
            else:
                n[a] -= 1
    out = 1
    for a in ARCS:
        out *= n[a]
    return val, n, out


def check_point(r, s, build=False):
    u12 = U4_pow12(r, s)
    val, n, out = construct(r, s)
    # duality sanity: LP value vs log U4 (float)
    logU = math.log(u12) / 12
    assert abs(val - logU) < 1e-6, (r, s, val, logU)
    # theorem: out > U4/16
    assert (16 * out) ** 12 > u12, ("construction below U4/16", r, s, n, out, u12)
    ratio12 = Fraction(u12, out ** 12)
    if build:
        mats = arc_instance(n)
        o = out4(*mats)
        assert o == out, (o, out)
        for e in range(4):
            re = size(mats[e])
            assert re <= r[e], (re, r[e])
            s2 = 1
            for a in ARCS:
                if meets(a, e) == 1:
                    s2 *= n[a]
            lo, hi = sigma2_lower(mats[e], 40), sigma2_upper(mats[e], 40)
            assert lo <= s2 <= hi, (lo, s2, hi)
            assert s2 <= s[e]
    return ratio12, n, out, u12


def main():
    mode = sys.argv[1]
    worst = (Fraction(0), None)
    count = 0
    built = 0
    if mode == 'grid':
        MAX = int(sys.argv[2])
        vals = [(rv, sv) for rv in range(1, MAX + 1) for sv in range(1, rv + 1)]
        for combo in itertools.product(vals, repeat=4):
            r = [c[0] for c in combo]
            s = [c[1] for c in combo]
            build = (count % 997 == 0)
            ratio12, n, out, u12 = check_point(r, s, build=build)
            built += build
            count += 1
            if ratio12 > worst[0]:
                worst = (ratio12, (r, s, {tuple(sorted(a)): v for a, v in n.items() if v > 1}, out, u12))
    else:
        nn = int(sys.argv[2])
        seed = int(sys.argv[3])
        RMAX = int(sys.argv[4])
        rng = random.Random(seed)
        for it in range(nn):
            r = [rng.randint(1, RMAX) for _ in range(4)]
            s = [rng.randint(1, re) for re in r]
            # bias: sometimes make s a power-ish of r
            build = (it % 200 == 0)
            ratio12, n, out, u12 = check_point(r, s, build=build)
            built += build
            count += 1
            if ratio12 > worst[0]:
                worst = (ratio12, (r, s, {tuple(sorted(a)): v for a, v in n.items() if v > 1}, out, u12))
    wr = float(worst[0]) ** (1 / 12)
    print(f"{mode}: {count} statistics vectors checked, {built} with matrices rebuilt and norms bracketed; all passed")
    print(f"  max U_4/Out_construction = {wr:.6f} (exact 12th power {worst[0]}) at r={worst[1][0]} s={worst[1][1]} arcs={worst[1][2]} Out={worst[1][3]}")


if __name__ == "__main__":
    main()
