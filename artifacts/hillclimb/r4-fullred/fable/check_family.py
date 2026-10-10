# Exact closed-form checks of the family L(v) inequalities and of the general family L(u^{4i}, u^{4i-2j}, u^{4i-j}, u^{4i-3j}, u^j, 1),
# plus brute force on the small general members.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import time
from fractions import Fraction as Fr
from lbcore import b2_bracket, ratio_bracket, fmt, icbrt_floor
from live_gadget import (params_ok, closed_live, union_closed, family_params, family_closed, general_params, build_union)

# A. the family L(v): closed forms of the union from closed_live vs the hand-derived polynomials, v = 2..60, and the inequalities
first_gt1 = None
for v in range(2, 61):
    pr = family_params(v)
    assert params_ok(*pr)
    u = union_closed(pr, pr, pr); f = family_closed(v)
    assert u['N'] == f['N'] and u['C'] == f['C'] == u['Cx'] == u['Cy'] == u['Cz'] and u['Out'] == f['Out']
    assert u['al'] == u['be'] == u['ga'] == f['fwd'] and u['alp'] == u['bep'] == u['gap'] == f['bwd']
    assert f['bwd'] > f['fwd'], v                                   # reverse larger: B2 = forward sum exactly
    B2 = f['fwd']
    assert u['C'] >= v ** 12 + v ** 10 + 3 * v ** 8 + v ** 7 >= v ** 12
    assert f['N'] <= 9 * v ** 10, v
    assert B2 <= 15 * v ** 11, v
    ratio = Fr(u['C'], f['N'] + B2)
    assert ratio >= Fr(v, 24), (v, ratio)
    assert Fr(f['N'], 9) <= v ** 10                                 # v >= (N/9)^{1/10}
    if ratio > 1 and first_gt1 is None:
        first_gt1 = (v, ratio, f['N'], u['C'], B2)
print("[A] L(v), v = 2..60: union closed forms == hand polynomials (N, C = all three roots, Out, fwd, bwd); bwd > fwd;")
print("    C >= v^12 + v^10 + 3v^8 + v^7; N <= 9 v^10; B2 = fwd <= 15 v^11; C/(N+B2) >= v/24; N/9 <= v^10 -- all exact, all v")
print(f"    first v with C/(N+B2) > 1: v = {first_gt1[0]}, ratio = {first_gt1[1]} = {float(first_gt1[1]):.4f}, N = {first_gt1[2]}, C = {first_gt1[3]}, B2 = {first_gt1[4]}")
for v in (2, 3, 4, 5, 8, 10, 16, 24, 25, 32):
    pr = family_params(v); u = union_closed(pr, pr, pr); f = family_closed(v)
    r = Fr(u['C'], f['N'] + f['fwd'])
    import math
    print(f"    v={v}: N={f['N']} C={u['C']} Out={f['Out']} B2={f['fwd']} C/(N+B2)={float(r):.4f} (>= v/24 = {v/24:.4f})  "
          f"log_N B2={math.log(f['fwd'])/math.log(f['N']):.4f}  log_N C={math.log(u['C'])/math.log(f['N']):.4f}  "
          f"log_N(C/(N+B2))={math.log(float(r))/math.log(f['N']):.4f}")

# B. general family: exponent identities for all 5j <= 4i, u in {2,3}, i <= 10 (exact integers)
print("[B] general family L(u^{4i}, u^{4i-2j}, u^{4i-j}, u^{4i-3j}, u^j, 1), 5j <= 4i:")
cnt = 0; worst = {}
for u in (2, 3):
    for i in range(1, 11):
        for j in range(0, 4 * i // 5 + 1):
            assert 5 * j <= 4 * i
            pr = general_params(i, j, u)
            assert params_ok(*pr), (i, j, u, pr)
            un = union_closed(pr, pr, pr)
            C, N = un['C'], un['N']
            fwd = un['al']; assert un['al'] == un['be'] == un['ga'] and un['alp'] == un['bep'] == un['gap']
            bwd = un['alp']
            if j >= 1:
                assert bwd >= fwd, (i, j, u)
            else:
                j0_bwd_smaller = j0_bwd_smaller + 1 if 'j0_bwd_smaller' in dir() else 1
            B2u = min(fwd, bwd)
            assert 3 * u ** (12 * i - 4 * j) <= B2u <= 48 * u ** (12 * i - 4 * j), (i, j, u, B2u / u ** (12 * i - 4 * j))
            assert C >= u ** (12 * i - 3 * j), (i, j, u)
            assert N <= 30 * u ** (8 * i), (i, j, u, N / u ** (8 * i))
            assert N >= 3 * u ** (8 * i)
            assert fwd <= 48 * u ** (12 * i - 4 * j), (i, j, u, fwd / u ** (12 * i - 4 * j))
            assert fwd >= 3 * u ** (12 * i - 4 * j)
            worst['N/u^8i'] = max(worst.get('N/u^8i', 0), Fr(N, u ** (8 * i)))
            worst['B2/u^(12i-4j)'] = max(worst.get('B2/u^(12i-4j)', 0), Fr(fwd, u ** (12 * i - 4 * j)))
            worst['C/u^(12i-3j)'] = max(worst.get('C/u^(12i-3j)', 0), Fr(C, u ** (12 * i - 3 * j)))
            cnt += 1
print(f"    {cnt} (i,j,u) tuples: params valid, bwd >= fwd for j >= 1 (j = 0: bwd < fwd in {j0_bwd_smaller} cases, B2 = bwd there), C >= u^(12i-3j), 3u^8i <= N <= 30u^8i, 3u^(12i-4j) <= min(fwd,bwd) <= 48u^(12i-4j)")
print("    worst constants:", {k: f"{float(v):.4f}" for k, v in worst.items()})
# slope check: kappa = (12i-4j)/(8i) = 3/2 - j/(2i) in [11/10, 3/2]; exponent of C = (12i-3j)/(8i) = 3/8 + 3 kappa/4
for i, j in ((5, 4), (2, 1), (3, 2), (4, 3), (1, 0)):
    kap = Fr(12 * i - 4 * j, 8 * i); ex = Fr(12 * i - 3 * j, 8 * i)
    assert ex == Fr(3, 8) + Fr(3, 4) * kap and Fr(11, 10) <= kap <= Fr(3, 2)
    print(f"    (i,j)=({i},{j}): kappa = {kap} = {float(kap):.3f}, C-exponent = {ex} = 3/8 + 3 kappa/4, gap = {ex - kap} = (3 - 2 kappa)/8 = {(3 - 2 * kap) / 8}")

# C. brute force on small general members
for (i, j, u) in ((1, 0, 2), (1, 0, 3), (2, 0, 2), (2, 1, 2)):
    pr = general_params(i, j, u)
    t0 = time.time()
    e = build_union((pr, pr, pr)).evaluate(); c = union_closed(pr, pr, pr)
    assert e['adds'] == e['N'] and e['fully_reduced']
    for key in ('R', 'S', 'T', 'N', 'Out', 'Cx', 'Cy', 'Cz', 'C', 'al', 'be', 'ga', 'alp', 'bep', 'gap'):
        assert e[key] == c[key], (i, j, u, key, e[key], c[key])
    assert e['C'] >= u ** (12 * i - 3 * j)
    print(f"[C] (i,j,u)=({i},{j},{u}) params={pr}: {fmt(e)}  C >= u^(12i-3j) = {u ** (12 * i - 3 * j)}  time {time.time() - t0:.0f}s")
