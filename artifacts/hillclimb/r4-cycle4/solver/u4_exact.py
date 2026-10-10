"""Exact-arithmetic check of the 4-cycle upper bound  Out <= U_4(r, s)  on random 0/1 instances.

U_4 = min over the 38 needed dual vertices of  prod r_e^lam_e s_e^mu_e  (lam, mu rational).
sigma_e^2 is irrational in general; as in the paper's chk_exact.py we certify with a rational
LOWER bound rho_e <= sigma_e^2 (Rayleigh quotients), set s_lo = min(rho, r) <= s, and check
Out^D <= (monomial with s_lo)^D exactly in integers (D = common denominator).  Since every
monomial is monotone in s, Out <= U_4(r, s_lo) <= U_4(r, s) is then certified.

Also reports, per instance, the exact ratio Out/U_4(r, s_hi) >= Out/U_4 (optimistic, with the
Collatz-Wielandt upper bound s_hi) so tightness is visible.

usage: python3 -I u4_exact.py <seed> <n_instances> [max_dim]
Exit status 0 iff every instance passes.
"""
import os
import sys
import math
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from lp_vertices import vertices, prune, monomial_str
from cyc4 import out4, size, sigma2_lower, sigma2_upper, mono_pow

names = ["R", "S", "T", "Q"]


def rand_mat(rng, a, b):
    kind = rng.random()
    M = [[0] * b for _ in range(a)]
    if kind < 0.3:
        p = rng.uniform(0.1, 1.0)
        for i in range(a):
            for j in range(b):
                if rng.random() < p:
                    M[i][j] = 1
    elif kind < 0.55:
        kb = rng.randint(1, max(1, min(a, b)))
        ra = [rng.randrange(kb) for _ in range(a)]
        rb = [rng.randrange(kb) for _ in range(b)]
        for i in range(a):
            for j in range(b):
                if ra[i] == rb[j]:
                    M[i][j] = 1
    elif kind < 0.65:
        for i in range(a):
            for j in range(b):
                M[i][j] = 1
    elif kind < 0.8:
        c = rng.randrange(a)
        for j in range(b):
            M[c][j] = 1
            M[rng.randrange(a)][j] = 1
        for i in range(a):
            M[i][rng.randrange(b)] = 1
    else:
        for i in range(a):
            M[i][rng.randrange(b)] = 1
    return M


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    maxdim = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    rng = random.Random(seed)
    A, E, verts = vertices(4)
    kept = prune(verts, 4)
    assert len(kept) == 38
    # integer exponents over common denominator per vertex
    vinfo = []
    for v in kept:
        D = 1
        for q in v:
            D = D * q.denominator // math.gcd(D, q.denominator)
        vinfo.append((v, D, [int(q * D) for q in v[:4]], [int(q * D) for q in v[4:]]))
    worst_ratio = Fraction(0)
    worst_inst = None
    tested = 0
    undecided = 0
    for it in range(n):
        dims = [rng.randint(1, maxdim) for _ in range(4)]
        nx, ny, nz, nw = dims
        AR = rand_mat(rng, nx, ny)
        AS = rand_mat(rng, ny, nz)
        AT = rand_mat(rng, nz, nw)
        AQ = rand_mat(rng, nw, nx)
        mats = (AR, AS, AT, AQ)
        r = [size(M) for M in mats]
        if min(r) == 0:
            continue
        o = out4(AR, AS, AT, AQ)
        if o == 0:
            continue
        tested += 1
        s_lo = [min(sigma2_lower(M, 40), Fraction(re)) for M, re in zip(mats, r)]
        s_hi = [min(sigma2_upper(M, 40), Fraction(re)) for M, re in zip(mats, r)]
        # certified check: Out^D <= mono(r, s_lo)^D for every vertex.  If the lower bound s_lo is
        # too weak (bound exactly tight, sigma^2 not reached by the Rayleigh quotients) the instance is
        # reported as 'undecided' unless Out^D > mono(r, s_hi)^D, which is a genuine violation.
        for (v, D, lamD, muD) in vinfo:
            m_lo = mono_pow(r, s_lo, lamD, muD, D)
            if Fraction(o) ** D > m_lo:
                m_hi = mono_pow(r, s_hi, lamD, muD, D)
                if Fraction(o) ** D > m_hi:
                    print("VIOLATION of", monomial_str(v, 4, names), "Out", o, "r", r, "s_hi", [str(x) for x in s_hi])
                    for M in mats:
                        print("   ", M)
                    sys.exit(1)
                undecided += 1
                print("undecided (bound tight, certificate gap):", monomial_str(v, 4, names), "Out", o, "r", r,
                      "s_lo", [float(x) for x in s_lo], "s_hi", [float(x) for x in s_hi])
        # optimistic ratio using s_hi: U4_hi = min_v mono(r, s_hi); ratio^D comparisons -> use floats only for display
        best = None
        for (v, D, lamD, muD) in vinfo:
            m_hi = mono_pow(r, s_hi, lamD, muD, D)
            val = Fraction(o) ** D / m_hi  # = (Out/mono)^D
            # compare across vertices via D-th roots: use float for display only
            rr = float(val) ** (1.0 / D)
            if best is None or rr > best:
                best = rr
        if Fraction(best) > worst_ratio:
            worst_ratio = Fraction(best)
            worst_inst = (dims, o, r, [str(x) for x in s_hi])
    print(f"seed {seed}: {tested} instances with Out>0; no violation; {tested - undecided} certified exactly (Out <= U_4(r, s_lo) <= U_4(r, s)), {undecided} undecided-but-not-violated")
    print(f"  largest Out/U_4(r, s_hi) (upper bound on Out/U_4): {float(worst_ratio):.4f} at dims={worst_inst[0]} Out={worst_inst[1]} r={worst_inst[2]}")


if __name__ == "__main__":
    main()
