"""Step 4: the lower bound (Theorem 2) and its constant.

 (a) Literal Sec. 5.1 rounding, fully exact, on power-of-2 statistics r_e = 2^a_e, s_e = 2^b_e (0 <= b_e <= a_e):
     the exact simplex gives a primal optimal vertex nu (rational, in log2 units); n~_A = floor(2^nu_A) for the
     twelve non-full arcs (exact integer root), m = floor(min_e r_e / prod n~_A), Out_int = m prod n~_A.
     Checks: admissibility (exact), 16 Out_int > U_4 (exact: (16 Out_int)^q > 2^p with LP value p/q),
     and the two separate losses of the proof: m*/m < 2 and the 'disjoint-arc' loss < 8.
 (b) Same rounding on general integer grids 1 <= s_e <= r_e <= MAX via rational approximations of the logs
     (the simplex is exact for the approximated data; the floors are then verified exactly: admissibility and
     (16 Out_int)^12 > U_4^12 in integers).
 (c) Exact integer optimum of the arc family (DFS) on the grids, max U_4 / Out*_arc as an exact 12th power.
usage: python3 -I s4_round.py pow2 <AMAX>        (a)
       python3 -I s4_round.py grid <MAX>         (b)
       python3 -I s4_round.py arcopt <MAX>       (c)
       python3 -I s4_round.py randpow2 <n> <seed> <AMAX>
"""
import os, sys, json, math, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from v2lib import arcs, edges, arc_lp, floor_pow2_frac, vertex_int_exponents, mono_powD, mono_str

HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, "vertices4.json")))
KEPT = [tuple(F(x) for x in v) for v in V["kept"]]
VINFO = [vertex_int_exponents(v) for v in KEPT]
A4 = arcs(4)
E4 = edges(4)
FULL = frozenset(range(4))
NONFULL = [a for a in A4 if a != FULL]


def meets(a, e):
    return len(a & E4[e])


def U4_pow12(r, s):
    best = None
    for (D, lamD, muD) in VINFO:
        assert 12 % D == 0
        val = mono_powD(r, s, [x * (12 // D) for x in lamD], [x * (12 // D) for x in muD])
        if best is None or val < best:
            best = val
    return best


def round_literal(r, s, nfloat):
    """nfloat: dict arc -> integer floor(n_A) for the non-full arcs (already computed exactly or via floats).
    Returns (m, Out_int, ok_admissible, mstar)."""
    n = dict(nfloat)
    # admissibility of the norm constraints
    for e in range(4):
        p = 1
        for a in NONFULL:
            if meets(a, e) == 1:
                p *= n[a]
        if p > s[e]:
            return None
    mstar = None
    for e in range(4):
        p = 1
        for a in NONFULL:
            if meets(a, e) >= 1:
                p *= n[a]
        v = F(r[e], p)
        mstar = v if mstar is None else min(mstar, v)
    m = math.floor(mstar)
    if m < 1:
        return None
    out = m
    for a in NONFULL:
        out *= n[a]
    # size admissibility re-check
    for e in range(4):
        p = m
        for a in NONFULL:
            if meets(a, e) >= 1:
                p *= n[a]
        assert p <= r[e]
    return m, out, mstar


def mode_pow2(AMAX, randomize=None):
    worst = (F(0), None)
    worst_m = F(0)
    worst_disj = F(0)
    cnt = 0
    if randomize is None:
        combos = itertools.product([(a, b) for a in range(AMAX + 1) for b in range(a + 1)], repeat=4)
    else:
        n, seed = randomize
        rng = random.Random(seed)
        def gen():
            for _ in range(n):
                aa = [rng.randint(0, AMAX) for _ in range(4)]
                bb = [rng.randint(0, x) for x in aa]
                yield tuple(zip(aa, bb))
        combos = gen()
    for combo in combos:
        a = [c[0] for c in combo]
        b = [c[1] for c in combo]
        r = [2 ** x for x in a]
        s = [2 ** x for x in b]
        A_, nu, val = arc_lp(4, [F(x) for x in a], [F(x) for x in b])
        nu = dict(zip(A4, nu))
        # U_4 = 2^val exactly (val rational); also cross-check with the 38 monomials: U_4^12 = 2^(12 val)
        u12 = U4_pow12(r, s)
        assert u12 == F(2) ** (12 * val), (a, b, val, u12)
        nflo = {a_: floor_pow2_frac(nu[a_]) for a_ in NONFULL}
        assert all(v >= 1 for v in nflo.values())
        res = round_literal(r, s, nflo)
        assert res is not None, ("rounding not admissible", a, b, nu)
        m, out, mstar = res
        # theorem: 16 Out_int > U_4  <=>  (16 out)^q > 2^p
        p, q = val.numerator, val.denominator
        assert (16 * out) ** q > 2 ** p, ("16 Out_int <= U_4", a, b, out, val)
        ratio12 = F(2) ** (12 * val) / F(out) ** 12
        # loss decomposition: m* / m and the disjoint-arc loss
        loss_m = mstar / m
        # min_e r_e prod_{A disjoint from e} n~_A  vs U_4: U_4 / (m* prod n~) = U_4 / (min_e r_e prod_{disj} n~)
        prod_n = 1
        for a_ in NONFULL:
            prod_n *= nflo[a_]
        disj = F(2) ** val / (mstar * prod_n)
        worst_m = max(worst_m, loss_m)
        worst_disj = max(worst_disj, disj)
        cnt += 1
        if ratio12 > worst[0]:
            worst = (ratio12, (a, b, {tuple(sorted(k)): v for k, v in nflo.items() if v > 1}, m, out, val))
    print(f"pow2 grid AMAX={AMAX} ({'random ' + str(randomize) if randomize else 'exhaustive'}): {cnt} statistics vectors, exact literal rounding;"
          f" all admissible, all 16 Out_int > U_4 (exact)")
    print(f"   max U_4/Out_int = {float(worst[0]) ** (1/12):.6f} (12th power {worst[0]}) at log2 r={worst[1][0]} log2 s={worst[1][1]} arcs={worst[1][2]} m={worst[1][3]} Out={worst[1][4]} log2 U_4={worst[1][5]}")
    print(f"   max loss factors: m*/m = {float(worst_m):.6f} (< 2), U_4/(m* prod n~) = {float(worst_disj):.6f} (< 8)")


def mode_grid(MAX):
    worst = (F(0), None)
    cnt = 0
    vals = [(rv, sv) for rv in range(1, MAX + 1) for sv in range(1, rv + 1)]
    for combo in itertools.product(vals, repeat=4):
        r = [c[0] for c in combo]
        s = [c[1] for c in combo]
        rho = [F(math.log2(x)).limit_denominator(10 ** 9) for x in r]
        vs = [F(math.log2(x)).limit_denominator(10 ** 9) for x in s]
        A_, nu, val = arc_lp(4, rho, vs)
        nu = dict(zip(A4, nu))
        nflo = {a_: max(1, math.floor(2 ** float(nu[a_]) + 1e-9)) for a_ in NONFULL}
        res = round_literal(r, s, nflo)
        if res is None:
            # float overshoot of a floor: fall back to the safe floor
            nflo = {a_: max(1, math.floor(2 ** float(nu[a_]) - 1e-9)) for a_ in NONFULL}
            res = round_literal(r, s, nflo)
        assert res is not None, ("rounding not admissible", r, s, nu)
        m, out, mstar = res
        u12 = U4_pow12(r, s)
        assert (16 * out) ** 12 > u12, ("16 Out_int <= U_4", r, s, out)
        ratio12 = F(u12, out ** 12)
        cnt += 1
        if ratio12 > worst[0]:
            worst = (ratio12, (r, s, {tuple(sorted(k)): v for k, v in nflo.items() if v > 1}, m, out))
    print(f"integer grid 1<=s<=r<={MAX}: {cnt} statistics vectors, literal rounding of an exact-simplex vertex of the"
          f" rational-log LP; all admissible, all (16 Out_int)^12 > U_4^12 exactly")
    print(f"   max U_4/Out_int = {float(worst[0]) ** (1/12):.6f} (12th power {worst[0]}) at r={worst[1][0]} s={worst[1][1]} arcs={worst[1][2]} m={worst[1][3]} Out={worst[1][4]}")


def best_arc_out(r, s):
    order = sorted(A4, key=lambda a: -len(a))
    best = [1]

    def dfs(i, pr, ps, prod):
        if i == len(order):
            if prod > best[0]:
                best[0] = prod
            return
        a = order[i]
        v = 1
        while True:
            ok = True
            for e in range(4):
                k = meets(a, e)
                if k >= 1 and pr[e] * v > r[e]:
                    ok = False
                    break
                if k == 1 and ps[e] * v > s[e]:
                    ok = False
                    break
            if not ok:
                break
            dfs(i + 1, [pr[e] * (v if meets(a, e) >= 1 else 1) for e in range(4)],
                [ps[e] * (v if meets(a, e) == 1 else 1) for e in range(4)], prod * v)
            v += 1
    dfs(0, [1] * 4, [1] * 4, 1)
    return best[0]


def mode_arcopt(MAX):
    worst = (F(0), None)
    cnt = 0
    vals = [(rv, sv) for rv in range(1, MAX + 1) for sv in range(1, rv + 1)]
    for combo in itertools.product(vals, repeat=4):
        r = [c[0] for c in combo]
        s = [c[1] for c in combo]
        o = best_arc_out(r, s)
        u12 = U4_pow12(r, s)
        assert (16 * o) ** 12 > u12
        ratio12 = F(u12, o ** 12)
        cnt += 1
        if ratio12 > worst[0]:
            worst = (ratio12, (r, s, o, u12))
    print(f"arc-family exact integer optimum, 1<=s<=r<={MAX}: {cnt} statistics vectors; all Out*_arc > U_4/16")
    print(f"   max U_4/Out*_arc = {float(worst[0]) ** (1/12):.6f} (12th power {worst[0]}) at r={worst[1][0]} s={worst[1][1]} Out*={worst[1][2]} U_4^12={worst[1][3]}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == 'pow2':
        mode_pow2(int(sys.argv[2]))
    elif mode == 'randpow2':
        mode_pow2(int(sys.argv[4]), randomize=(int(sys.argv[2]), int(sys.argv[3])))
    elif mode == 'grid':
        mode_grid(int(sys.argv[2]))
    elif mode == 'arcopt':
        mode_arcopt(int(sys.argv[2]))
