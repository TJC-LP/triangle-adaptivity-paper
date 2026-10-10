"""Step 7: the constant gap [8, 16] (Sec. 5.3 of the solver's report) and non-arc instances.

 (i)  r = (t, t^3, t^4, t^3), s = (1, t^2, t^2, t^2): U_4 = t^4 exactly (rational t < 2); for t -> 2^- the admissible
      instances have |R| = 1, S and Q stars of degree <= 3 at the R-endpoints, and Out = |T'| for T' inside a
      3 x 3 box with sigma_T'^2 < 4: W(t) = max{|T'| : T' in {0,1}^{3x3}, lambda_max(T'^T T') <= t^2}, computed
      exactly for t = 63/32, 127/64 (and the limit value for sigma^2 < 4).
 (ii) r = (3, 4, 2, 4), s = (2, 4, 1, 4): U_4^12 exactly, exact integer arc optimum, and a hand-built non-arc
      instance (R a 2-matching, S and Q = K_{2,2}, T a 2-matching) with Out = 4, verified exactly.
 (iii) At the worst grid points of the arc family (r = (2,3,3,3), s = (1,2,2,3) and r = (2,3,4,3), s = (1,2,3,2)),
      a random+greedy search for admissible 0/1 instances (exact sigma^2) with Out above the arc optimum.
"""
import os, sys, json, random, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from v2lib import (vertex_int_exponents, mono_powD, mono_str, out4, size, sigma2_bracket, lambda_max_bracket,
                   gram_small, charpoly, poly_eval)
import s4_round as s4

HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, "vertices4.json")))
KEPT = [tuple(F(x) for x in v) for v in V["kept"]]
VINFO = [vertex_int_exponents(v) for v in KEPT]


def U4_12(r, s):
    best, arg = None, None
    for v, (D, lamD, muD) in zip(KEPT, VINFO):
        val = mono_powD(r, s, [x * (12 // D) for x in lamD], [x * (12 // D) for x in muD])
        if best is None or val < best:
            best, arg = val, v
    return best, arg


print("(i) r = (t, t^3, t^4, t^3), s = (1, t^2, t^2, t^2)")
for t in [F(3, 2), F(7, 4), F(31, 16), F(63, 32), F(127, 64)]:
    r = [t, t ** 3, t ** 4, t ** 3]
    s = [F(1), t ** 2, t ** 2, t ** 2]
    u12, arg = U4_12(r, s)
    # W(t): |R| <= floor(t) = 1 edge (x0,y0); S-edges at y0: d <= floor(t^2) (<= 3), Q-edges at x0: d <= 3;
    # T' = T restricted to N_S(y0) x N_Q(x0): Out = |T'|; sigma_{T'}^2 <= sigma_T^2 <= t^2; so W(t) <= max |T'| over
    # 3x3 patterns with lambda_max <= t^2, and this is attained (take S, Q the stars, T = T').  |T| = |T'| <= 15 ok.
    best = 0
    for bits in itertools.product([0, 1], repeat=9):
        M = [list(bits[0:3]), list(bits[3:6]), list(bits[6:9])]
        k = sum(bits)
        if k <= best or k == 0:
            continue
        lo, hi, ex = sigma2_bracket(M, 50)
        if hi <= t ** 2 or (ex and lo <= t ** 2):
            best = k
        elif lo < t ** 2 <= hi:
            print("    (bracket straddles t^2; refine)", M, lo, hi)
    print(f"  t={str(t):7s}: U_4^12 == t^48: {u12 == t**48} (argmin {mono_str(arg,4)}); W(t) = {best}; W/U_4 = {best/float(t**4):.4f}  (U_4 -> 16, W -> 5 as t -> 2)")

print("(ii) r = (3, 4, 2, 4), s = (2, 4, 1, 4)")
r = [3, 4, 2, 4]
s = [2, 4, 1, 4]
u12, arg = U4_12(r, s)
print(f"  U_4^12 = {u12} = 32^6: {u12 == 32**6}  (U_4 = sqrt(32) = {math.sqrt(32):.4f}, argmin {mono_str(arg,4)}); arc optimum = {s4.best_arc_out(r, s)}")
R = [[1, 0], [0, 1]]           # X = {x, x'}, Y = {y, y'}: matching
S = [[1, 1], [1, 1]]           # Y x Z = K_{2,2}
T = [[1, 0], [0, 1]]           # Z x W matching
Q = [[1, 1], [1, 1]]           # W x X = K_{2,2}
o = out4(R, S, T, Q)
rr = [size(M) for M in (R, S, T, Q)]
ss = [sigma2_bracket(M, 50) for M in (R, S, T, Q)]
print(f"  hand-built instance: Out = {o}, |e| = {rr}, sigma^2 = {[str(x[0]) for x in ss]} (all exact integers: {all(x[2] for x in ss)}); admissible for r, s: {all(rr[e] <= r[e] and ss[e][1] <= s[e] for e in range(4))}")
print(f"  so W >= {o} > arc optimum {s4.best_arc_out(r, s)} at this point; U_4/W <= {math.sqrt(32)/o:.4f}")


def search_W(r, s, rng, trials, dims=(4, 4, 4, 4)):
    """random instances with |e| <= r_e, greedy fill, exact sigma^2 admissibility; returns the best Out found."""
    best, best_inst = 0, None
    nx, ny, nz, nw = dims
    shapes = [(nx, ny), (ny, nz), (nz, nw), (nw, nx)]
    for _ in range(trials):
        mats = []
        ok = True
        for e, (a, b) in enumerate(shapes):
            M = [[0] * b for _ in range(a)]
            cells = [(i, j) for i in range(a) for j in range(b)]
            rng.shuffle(cells)
            cnt = 0
            for (i, j) in cells:
                if cnt >= r[e]:
                    break
                M[i][j] = 1
                lo, hi, ex = sigma2_bracket(M, 40)
                if hi > s[e] and not (ex and lo <= s[e]):
                    M[i][j] = 0
                else:
                    cnt += 1
            if cnt == 0:
                ok = False
            mats.append(M)
        if not ok:
            continue
        o = out4(*mats)
        if o > best:
            best, best_inst = o, mats
    return best, best_inst


print("(iii) search for non-arc instances above the arc optimum at the worst grid points")
rng = random.Random(3)
for (r, s) in [([2, 3, 3, 3], [1, 2, 2, 3]), ([2, 3, 4, 3], [1, 2, 3, 2]), ([3, 4, 2, 4], [2, 4, 1, 4]), ([2, 2, 2, 2], [1, 2, 2, 2])]:
    u12, arg = U4_12(r, s)
    arc = s4.best_arc_out(r, s)
    bestW, inst = search_W(r, s, rng, 4000, dims=(3, 3, 3, 3))
    print(f"  r={r} s={s}: U_4={float(u12)**(1/12):.4f}, arc optimum {arc}, best admissible 0/1 instance found Out={bestW} -> U_4/W <= {float(u12)**(1/12)/max(bestW,1):.4f}")
    if bestW > arc:
        print("     instance:", inst)
print("STEP-7 DONE")
