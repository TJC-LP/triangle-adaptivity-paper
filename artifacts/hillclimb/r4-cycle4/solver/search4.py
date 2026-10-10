"""Counterexample search for the 4-cycle monomial bounds.

For each candidate monomial prod r_e^lam_e s_e^mu_e we hill-climb (simulated annealing over
0/1 matrices, float sigma via numpy) to maximise  log Out - log(monomial).  Any candidate
with ratio > 1 - eps is re-verified EXACTLY: Out and sizes are integers, s_e is replaced by a
rigorous rational UPPER bound s_hi >= s_e (Collatz-Wielandt), and the inequality
Out^D > prod r^lamD s_hi^muD (D = common denominator) is decided in integers/Fractions.
A confirmed violation refutes the monomial as an upper bound.

usage: python3 -I search4.py <seed> <restarts> <steps> [which]
  which = 'all' (default) or comma-separated indices into the vertex list.
"""
import os
import sys
import math
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fractions import Fraction
from lp_vertices import vertices, monomial_str, prune
from cyc4 import out4, size, sigma2_upper, sigma2_lower, mono_pow

names = ["R", "S", "T", "Q"]


def np_stats(mats):
    r = [float(M.sum()) for M in mats]
    s = []
    for M, re in zip(mats, r):
        if re == 0:
            s.append(0.0)
            continue
        sv = np.linalg.norm(M, 2) ** 2
        s.append(min(sv, re))
    return r, s


def np_out(mats):
    AR, AS, AT, AQ = mats
    return float(np.trace(AR @ AS @ AT @ AQ))


def score(mats, lam, mu):
    o = np_out(mats)
    if o <= 0:
        return -1e9
    r, s = np_stats(mats)
    if min(r) <= 0 or min(s) <= 0:
        return -1e9
    val = math.log(o)
    for e in range(4):
        val -= lam[e] * math.log(r[e]) + mu[e] * math.log(s[e])
    return val


def random_instance(rng, dims):
    nx, ny, nz, nw = dims
    shapes = [(nx, ny), (ny, nz), (nz, nw), (nw, nx)]
    mats = []
    for (a, b) in shapes:
        kind = rng.random()
        if kind < 0.3:
            p = rng.uniform(0.2, 1.0)
            M = (np.random.default_rng(rng.randrange(1 << 30)).random((a, b)) < p).astype(np.int64)
        elif kind < 0.6:
            # block diagonal-ish: random partition into blocks, complete inside
            M = np.zeros((a, b), dtype=np.int64)
            kb = rng.randint(1, max(1, min(a, b)))
            ra = [rng.randrange(kb) for _ in range(a)]
            rb = [rng.randrange(kb) for _ in range(b)]
            for i in range(a):
                for j in range(b):
                    if ra[i] == rb[j]:
                        M[i, j] = 1
        elif kind < 0.8:
            M = np.ones((a, b), dtype=np.int64)
        else:
            M = np.zeros((a, b), dtype=np.int64)
            for i in range(a):
                M[i, rng.randrange(b)] = 1
            for j in range(b):
                M[rng.randrange(a), j] = 1
        mats.append(M)
    return mats


def anneal(rng, lam, mu, steps, dims):
    mats = random_instance(rng, dims)
    cur = score(mats, lam, mu)
    best = cur
    best_mats = [M.copy() for M in mats]
    T0 = 0.5
    for t in range(steps):
        temp = T0 * (1 - t / steps) + 1e-3
        e = rng.randrange(4)
        M = mats[e]
        i = rng.randrange(M.shape[0])
        j = rng.randrange(M.shape[1])
        M[i, j] ^= 1
        new = score(mats, lam, mu)
        if new >= cur or rng.random() < math.exp((new - cur) / temp):
            cur = new
            if cur > best:
                best = cur
                best_mats = [M.copy() for M in mats]
        else:
            M[i, j] ^= 1
    return best, best_mats


def exact_check(mats, lam, mu):
    """Return (ratio_lo_exact, ratio_hi_exact, violated) where ratio^D = Out^D / mono^D using
    s_hi (rigorous upper bounds on s) for the 'violation' test and s_lo for the optimistic ratio."""
    L = [[int(x) for x in row] for row in mats[0].tolist()], [[int(x) for x in row] for row in mats[1].tolist()], \
        [[int(x) for x in row] for row in mats[2].tolist()], [[int(x) for x in row] for row in mats[3].tolist()]
    AR, AS, AT, AQ = L
    o = out4(AR, AS, AT, AQ)
    r = [size(M) for M in L]
    s_hi = [min(sigma2_upper(M, 40), Fraction(re)) for M, re in zip(L, r)]
    s_lo = [min(sigma2_lower(M, 40), Fraction(re)) for M, re in zip(L, r)]
    D = 1
    for v in list(lam) + list(mu):
        D = D * v.denominator // math.gcd(D, v.denominator)
    lamD = [int(v * D) for v in lam]
    muD = [int(v * D) for v in mu]
    mono_hi = mono_pow(r, s_hi, lamD, muD, D)  # (monomial with s_hi)^D
    mono_lo = mono_pow(r, s_lo, lamD, muD, D)
    outD = Fraction(o) ** D
    violated = outD > mono_hi  # rigorous: Out^D > (bound with s >= true s)^D
    return (outD / mono_lo) ** Fraction(1, D) if mono_lo > 0 else None, (outD / mono_hi) if mono_hi > 0 else None, violated, o, r, s_lo, s_hi


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    which = sys.argv[4] if len(sys.argv) > 4 else 'all'
    rng = random.Random(seed)
    A, E, verts = vertices(4)
    kept = prune(verts, 4)
    idx = list(range(len(kept))) if which == 'all' else [int(x) for x in which.split(',')]
    worst_overall = []
    for vi in idx:
        v = kept[vi]
        lam, mu = v[:4], v[4:]
        best = -1e9
        best_m = None
        for rst in range(restarts):
            dims = tuple(rng.randint(1, 7) for _ in range(4))
            b, m = anneal(rng, lam, mu, steps, dims)
            if b > best:
                best, best_m = b, m
        # exact verification of the best float candidate
        rlo, rhi, viol, o, r, s_lo, s_hi = exact_check(best_m, lam, mu)
        flag = "VIOLATION" if viol else ""
        print(f"[{vi:2d}] {monomial_str(v,4,names):50s} float ratio={math.exp(best):.4f} exact(opt) ratio~{float(rlo) if rlo is not None else None:.4f} {flag}")
        if viol:
            print("   Out", o, "r", r, "s_lo", [str(x) for x in s_lo], "s_hi", [str(x) for x in s_hi])
            for M in best_m:
                print("   ", M.tolist())
        worst_overall.append((math.exp(best), vi))
        sys.stdout.flush()
    worst_overall.sort(reverse=True)
    print("top float ratios:", worst_overall[:8])


if __name__ == "__main__":
    main()
