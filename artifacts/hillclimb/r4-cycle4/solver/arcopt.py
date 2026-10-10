"""Exact integer optimum of the arc-blowup family on a grid: max prod n_A over integer n_A >= 1 subject to
prod_{A∩e≠∅} n_A <= r_e and prod_{|A∩e|=1} n_A <= s_e (exhaustive DFS with product pruning).  Reports the
exact maximum of U_4 / Out*_arc over the grid (12th powers compared exactly).
usage: python3 -I arcopt.py <MAX>"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from construct4 import U4_pow12, ARCS, FULL, meets
MAX = int(sys.argv[1])
order = sorted(ARCS, key=lambda a: -len(a))  # full arc first, then triples, pairs, singletons

def best_out(r, s):
    best = [1]
    n = {}
    def dfs(i, pr, ps, prod):
        # pr[e], ps[e]: current products for size / norm constraints
        if i == len(order):
            if prod > best[0]: best[0] = prod
            return
        a = order[i]
        # upper bound on remaining product: each remaining arc bounded by min r_e over edges it meets
        v = 1
        while True:
            ok = True
            for e in range(4):
                k = meets(a, e)
                if k >= 1 and pr[e] * v > r[e]: ok = False; break
                if k == 1 and ps[e] * v > s[e]: ok = False; break
            if not ok: break
            npr = [pr[e] * (v if meets(a, e) >= 1 else 1) for e in range(4)]
            nps = [ps[e] * (v if meets(a, e) == 1 else 1) for e in range(4)]
            dfs(i + 1, npr, nps, prod * v)
            v += 1
    dfs(0, [1]*4, [1]*4, 1)
    return best[0]

vals = [(rv, sv) for rv in range(1, MAX + 1) for sv in range(1, rv + 1)]
worst = (Fraction(0), None); cnt = 0
for combo in itertools.product(vals, repeat=4):
    r = [c[0] for c in combo]; s = [c[1] for c in combo]
    u12 = U4_pow12(r, s); o = best_out(r, s)
    ratio12 = Fraction(u12, o ** 12); cnt += 1
    assert (16 * o) ** 12 > u12
    if ratio12 > worst[0]: worst = (ratio12, (r, s, o, u12))
print(f"MAX={MAX}: {cnt} statistics vectors; exact integer arc optimum computed for each; all have Out*_arc > U_4/16")
print(f"  max U_4/Out*_arc = {float(worst[0])**(1/12):.6f} (12th power {worst[0]}) at r={worst[1][0]} s={worst[1][1]} Out*={worst[1][2]}")
