"""Step 5: Proposition 3 (T4) and T5, exactly.

T4 family: r = (L, t, L, L), s = (t, t, t, L), 1 <= t < 2.  Claims: W = 1 (proved by hand, see report) and
U_4 = t^3 for L large.  Here: exact U_4^12 at rational t and several L; the smallest integer L with U_4 = t^3;
the binding monomial for small L; and the sharpened side condition L >= t^3.
T5: R, S, Q complete n x n, T a perfect matching: Out = n^3 = U_4; the block family reaches n^2.  Astra's
obstruction r = (1, n, n, n), s = (1, n, 1, n): U_4 = n, attained.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from v2lib import (vertex_int_exponents, mono_powD, mono_str, out4, size, arc_instance, arcs, perron_rowsum_check,
                   sigma2_bracket, classify)

HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, "vertices4.json")))
KEPT = [tuple(F(x) for x in v) for v in V["kept"]]
VINFO = [vertex_int_exponents(v) for v in KEPT]


def U4_pow12_with_argmin(r, s):
    best, arg = None, None
    for v, (D, lamD, muD) in zip(KEPT, VINFO):
        val = mono_powD(r, s, [x * (12 // D) for x in lamD], [x * (12 // D) for x in muD])
        if best is None or val < best:
            best, arg = val, v
    return best, arg


print("T4: r = (L, t, L, L), s = (t, t, t, L)")
for t in [F(1), F(3, 2), F(7, 4), F(15, 8), F(31, 16), F(63, 32), F(127, 64)]:
    # smallest integer L >= 2 with U_4 = t^3
    Lmin = None
    for L in range(2, 200):
        r = [F(L), t, F(L), F(L)]
        s = [t, t, t, F(L)]
        u12, arg = U4_pow12_with_argmin(r, s)
        if u12 == t ** 36:
            Lmin = L
            break
    r = [F(10 ** 6), t, F(10 ** 6), F(10 ** 6)]
    s = [t, t, t, F(10 ** 6)]
    u12, arg = U4_pow12_with_argmin(r, s)
    # the binding monomial at L just below Lmin
    L2 = Lmin - 1
    r2 = [F(L2), t, F(L2), F(L2)]
    s2 = [t, t, t, F(L2)]
    u12b, argb = U4_pow12_with_argmin(r2, s2)
    print(f"  t={str(t):8s} U_4^12 == t^36 at L=1e6: {u12 == t**36} (argmin {mono_str(arg,4)}); smallest L with U_4 = t^3: {Lmin}"
          f" (t^2={float(t*t):.3f}, t^3={float(t**3):.3f}); at L={L2} the minimum is {classify(argb)} {mono_str(argb,4)} = {float(u12b)**(1/12):.4f} < t^3={float(t**3):.4f}")
# check the sharpened condition: U_4 = t^3 whenever L >= t^3 (rational L on a fine grid of t)
ok = True
for i in range(1, 64):
    t = F(1) + F(i, 64)
    for Lnum in range(0, 40):
        L = t ** 3 + F(Lnum, 8)
        r = [L, t, L, L]
        s = [t, t, t, L]
        u12, arg = U4_pow12_with_argmin(r, s)
        if u12 != t ** 36:
            ok = False
            print("   counterexample to 'L >= t^3 suffices':", t, L)
print(f"  'U_4 = t^3 for all L >= t^3' on a grid of 63 x 40 (t, L) pairs: {ok}")
# and L = t^2 fails when t^2 < t^3, i.e. always for t > 1:
r = [F(9, 4), F(3, 2), F(9, 4), F(9, 4)]
s = [F(3, 2)] * 3 + [F(9, 4)]
u12, arg = U4_pow12_with_argmin(r, s)
print(f"  at t=3/2, L=t^2=9/4: U_4 = {float(u12)**(1/12):.5f} vs t^3 = {float(F(27,8)):.5f}; argmin {mono_str(arg,4)} -> the report's side condition 'L >= t^2' is insufficient")

print("T5: R, S, Q complete n x n, T perfect matching")
for n in [2, 3, 4, 5]:
    R = [[1] * n for _ in range(n)]
    S = [[1] * n for _ in range(n)]
    T = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    Q = [[1] * n for _ in range(n)]
    o = out4(R, S, T, Q)
    r = [size(M) for M in (R, S, T, Q)]
    s2 = []
    for M in (R, S, T, Q):
        lo, hi, ex = sigma2_bracket(M, 40)
        assert ex
        s2.append(min(lo, F(size(M))))
    u12, arg = U4_pow12_with_argmin(r, s2)
    tight = [mono_str(v, 4) + f" [{classify(v)}]" for v, (D, lamD, muD) in zip(KEPT, VINFO)
             if mono_powD(r, s2, [x * (12 // D) for x in lamD], [x * (12 // D) for x in muD]) == F(o) ** 12]
    print(f"  n={n}: Out={o} = n^3: {o == n**3}; r={r}, s={[int(x) for x in s2]}; U_4^12 == Out^12: {u12 == F(o)**12}; tight terms: {tight}")
# block family bound: m K_{a,b,c,d} with cd <= s_T = 1 -> c = d = 1 -> Out = m a b <= |R| = n^2 (hand argument);
# exhaustive over a,b,c,d,m for n = 4 as a check
n = 4
r = [n * n, n * n, n, n * n]
s = [n * n, n * n, 1, n * n]
best = 0
for a in range(1, 17):
    for b in range(1, 17):
        for c in range(1, 17):
            for d in range(1, 17):
                if a * b > s[0] or b * c > s[1] or c * d > s[2] or d * a > s[3]:
                    continue
                m = min(r[0] // (a * b), r[1] // (b * c), r[2] // (c * d), r[3] // (d * a))
                if m >= 1:
                    best = max(best, m * a * b * c * d)
print(f"  n=4: best complete-block output = {best} = n^2: {best == n*n} (vs Out = U_4 = {n**3})")

print("Astra obstruction: r = (1, n, n, n), s = (1, n, 1, n)")
for n in [2, 3, 5, 7]:
    r = [1, n, n, n]
    s = [1, n, 1, n]
    u12, arg = U4_pow12_with_argmin(r, s)
    mats = arc_instance({frozenset({2, 3}): n})
    o = out4(*mats)
    rr = [size(M) for M in mats]
    ss = [1, n, 1, n]
    assert all(perron_rowsum_check(mats[e], ss[e]) for e in range(4))
    print(f"  n={n}: U_4^12 == n^12: {u12 == F(n)**12} (argmin {mono_str(arg,4)}); pair-arc {{Z,W}} instance: Out={o}, |e|={rr}, sigma^2={ss} (exact)")
print("STEP-5 DONE")
