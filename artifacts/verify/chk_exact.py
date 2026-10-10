"""Exact-arithmetic checks of Theorem B (spectral AGM for the labeled triangle).

Every comparison below is made in integers or `fractions.Fraction`; no float
enters a decision.  Square roots never appear: the Hölder terms are compared
through their squares, and U itself is carried as U^2 = Q.

Notation (paper, Section 3): r_i = |relation i| bound, sigma_i = operator-norm
bound, s_i = min(sigma_i^2, r_i).  With (R, S, T) = (0, 1, 2),

  U = min( sqrt(s_R r_S r_T), sqrt(s_S r_R r_T), sqrt(s_T r_R r_S),
           r_R s_S, r_R s_T, r_S s_R, r_S s_T, r_T s_R, r_T s_S ).

Checks
  grid    Exhaustive over integer statistics 1 <= s_i <= r_i <= MAX
          ((MAX(MAX+1)/2)^3 vectors; MAX = 15 gives 1,728,000).  For each:
          (a) the floored block (a, b, c, m) of the lower construction is
              admissible: ab <= s_R, bc <= s_S, ca <= s_T (degree/norm side)
              and m ab <= r_R, m bc <= r_S, m ca <= r_T (size side), m >= 1;
          (b) U < 4 m a b c, i.e. Q < 16 (mabc)^2;
          (c) the relaxed real shape is feasible and has value exactly U:
              alpha beta <= s_R (and rotations), m* >= 1, m* alpha beta gamma = U,
              each decided exactly through Q;
          and reports the exact maximum of U / (mabc) with its argmax.
  random  Random 0/1 instances (sizes <= 9): Out <= U for the instance's own
          statistics.  sigma^2 is irrational in general, so the check is a
          certificate: a rational lower bound rho <= sigma^2 from the Rayleigh
          quotient of an exact integer power iterate of A^T A gives
          U_lo = U(r, min(rho, r)) <= U, and Out <= U_lo is decided exactly.
  pell    The sharpness family of Section 11: (p, q) = (7, 5),
          (p, q) -> (3p + 4q, 2p + 3q); u = p/q, t = u^2, r = (t^2, t, t^2),
          sigma = (u, 1, u).  Checks p^2 - 2 q^2 = -1, U = t^2 exactly, the
          floored construction is (1, 1, 1, 1), and prints U/W = t^2 (W = 1).

Usage:  python3 -I chk_exact.py [--max 15] [--random 3000] [--seed 7] [--pell 6]
Exit status 0 iff every check passes.
"""
import argparse
import random
import sys
from fractions import Fraction
from math import gcd, isqrt


def floor_sqrt_div(Q, r):
    """floor(sqrt(Q) / r) for integers Q >= 0, r >= 1 (exact)."""
    return isqrt(Q // (r * r))


def U2(r, s):
    """U^2 as an exact number (int or Fraction) for statistics r, s."""
    R, S, T = r
    sR, sS, sT = s
    deg = [R * sS, R * sT, S * sR, S * sT, T * sR, T * sS]
    return min([sR * S * T, sS * R * T, sT * R * S] + [d * d for d in deg])


def construction(r, s):
    """Floored block of the lower construction, decided exactly from Q = U^2.

    a = floor(max(1, U/r_S)), b = floor(max(1, U/r_T)), c = floor(max(1, U/r_R)),
    m = floor(min(r_R/(ab), r_S/(bc), r_T/(ca))).
    Statistics r_i are integers here; for rational r (pell) use construction_q.
    """
    R, S, T = r
    Q = U2(r, s)
    a = max(1, floor_sqrt_div(Q, S))
    b = max(1, floor_sqrt_div(Q, T))
    c = max(1, floor_sqrt_div(Q, R))
    m = min(R // (a * b), S // (b * c), T // (c * a))
    return Q, a, b, c, m


def floor_sqrt_frac(x):
    """floor(sqrt(x)) for a nonnegative Fraction x (exact)."""
    x = Fraction(x)
    k = isqrt(x.numerator // x.denominator)
    while (k + 1) * (k + 1) <= x:
        k += 1
    while k * k > x:
        k -= 1
    return k


def construction_q(r, s):
    """Rational-statistics version of `construction`."""
    R, S, T = (Fraction(v) for v in r)
    Q = Fraction(U2((R, S, T), tuple(Fraction(v) for v in s)))
    a = max(1, floor_sqrt_frac(Q / (S * S)))
    b = max(1, floor_sqrt_frac(Q / (T * T)))
    c = max(1, floor_sqrt_frac(Q / (R * R)))
    mu = min(R / (a * b), S / (b * c), T / (c * a))
    m = mu.numerator // mu.denominator
    return Q, a, b, c, m


def real_shape_ok(r, s, Q):
    """Exact check of the relaxed real shape (alpha, beta, gamma, m*).

    alpha = max(1, U/r_S), beta = max(1, U/r_T), gamma = max(1, U/r_R).
    For x, y >= 0, max(1,x) max(1,y) = max(1, x, y, xy), so
      alpha beta <= s_R  <=>  1 <= s_R, Q <= (s_R r_S)^2, Q <= (s_R r_T)^2, Q <= s_R r_S r_T.
    m* >= 1 <=> alpha beta <= r_R (and rotations), decided the same way.
    m* alpha beta gamma = min(gamma r_R, alpha r_S, beta r_T) = min_j max(r_j, U),
    which equals U iff U >= min_j r_j  <=>  Q >= min(r)^2.
    """
    R, S, T = r
    sR, sS, sT = s

    def prod_le(bound, x_den, y_den):  # max(1,U/x) max(1,U/y) <= bound
        return (1 <= bound and Q <= (bound * x_den) ** 2 and Q <= (bound * y_den) ** 2
                and Q <= bound * x_den * y_den)

    feas = prod_le(sR, S, T) and prod_le(sS, T, R) and prod_le(sT, R, S)
    mstar = prod_le(R, S, T) and prod_le(S, T, R) and prod_le(T, R, S)
    attains = Q >= min(r) ** 2
    return feas, mstar, attains


def grid(maxv):
    vals = [(rv, sv) for rv in range(1, maxv + 1) for sv in range(1, rv + 1)]
    n = fail = 0
    best = (Fraction(0), None)
    for rR, sR in vals:
        for rS, sS in vals:
            for rT, sT in vals:
                n += 1
                r, s = (rR, rS, rT), (sR, sS, sT)
                Q, a, b, c, m = construction(r, s)
                out = m * a * b * c
                ok = (m >= 1 and a * b <= sR and b * c <= sS and c * a <= sT
                      and m * a * b <= rR and m * b * c <= rS and m * c * a <= rT
                      and Q < 16 * out * out)
                feas, mstar, attains = real_shape_ok(r, s, Q)
                if not (ok and feas and mstar and attains):
                    fail += 1
                    if fail <= 5:
                        print("  FAIL", r, s, (a, b, c, m), ok, feas, mstar, attains)
                ratio2 = Fraction(Q, out * out)  # (U / mabc)^2
                if ratio2 > best[0]:
                    best = (ratio2, (r, s, Q, (a, b, c, m)))
    return n, fail, best


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def transpose(A):
    return [list(c) for c in zip(*A)]


def sigma2_lower(A, steps=40):
    """Rational rho <= ||A||_2^2: the largest of several Rayleigh quotients of B = A^T A.

    Every Rayleigh quotient w.Bw / w.w (w a nonzero rational vector) is <= the top
    eigenvalue sigma^2 of B, so the maximum over any candidate set is a certified
    lower bound.  Candidates: each unit vector e_j (quotient = degree of column j),
    each row of A, i.e. A^T e_i (quotient >= degree of row i), and the integer
    power iterates B^k 1.  The degree candidates certify the cases where a
    maximum-degree term of U is tight; the iterates certify the Hölder terms.
    """
    B = matmul(transpose(A), A)
    n = len(B)

    def rq(w):
        Bw = [sum(B[i][j] * w[j] for j in range(n)) for i in range(n)]
        ww = sum(x * x for x in w)
        return Fraction(sum(x * y for x, y in zip(w, Bw)), ww) if ww else Fraction(0)

    best = Fraction(0)
    for j in range(n):
        best = max(best, rq([int(i == j) for i in range(n)]))
    for row in A:
        best = max(best, rq(list(row)))
    w = [1] * n
    for _ in range(steps):
        Bw = [sum(B[i][j] * w[j] for j in range(len(w))) for i in range(len(w))]
        ww = sum(x * x for x in w)
        if ww == 0:
            break
        best = max(best, Fraction(sum(x * y for x, y in zip(w, Bw)), ww))
        g = 0
        for x in Bw:
            g = gcd(g, x)
        w = [x // g for x in Bw] if g else Bw
    return best


def random_instances(count, seed):
    rng = random.Random(seed)
    checked = certified = 0
    worst = Fraction(0)
    for _ in range(count):
        nx, ny, nz = (rng.randint(1, 9) for _ in range(3))
        ps = [rng.random() for _ in range(3)]
        AR = [[int(rng.random() < ps[0]) for _ in range(ny)] for _ in range(nx)]
        AS = [[int(rng.random() < ps[1]) for _ in range(nz)] for _ in range(ny)]
        AT = [[int(rng.random() < ps[2]) for _ in range(nx)] for _ in range(nz)]
        r = tuple(sum(map(sum, M)) for M in (AR, AS, AT))
        if min(r) == 0:
            continue
        checked += 1
        P = matmul(matmul(AR, AS), AT)
        out = sum(P[i][i] for i in range(nx))
        rho = [sigma2_lower(M) for M in (AR, AS, AT)]
        s_lo = tuple(min(rho[i], r[i]) for i in range(3))
        Q_lo = U2(r, s_lo)  # (U_lo)^2 <= U^2
        if out * out <= Q_lo:
            certified += 1
            if Q_lo:
                worst = max(worst, Fraction(out * out) / Q_lo)
        else:
            print("  UNCERTIFIED", r, out, Q_lo)
    return checked, certified, worst


def pell(n):
    p, q = 7, 5
    rows = []
    ok = True
    for _ in range(n):
        ok &= p * p - 2 * q * q == -1
        u = Fraction(p, q)
        t = u * u
        r = (t * t, t, t * t)
        s = (min(u * u, r[0]), min(Fraction(1), r[1]), min(u * u, r[2]))
        ok &= s == (t, Fraction(1), t)
        Q, a, b, c, m = construction_q(r, s)
        ok &= Q == t ** 4 and (a, b, c, m) == (1, 1, 1, 1)
        # W = 1: |S| <= r_S = t < 2 forces |S| <= 1, and every degree of R, T is
        # <= s = t < 2, hence <= 1, so Out <= 1; one triangle is admissible.
        ok &= t < 2 and r[1] < 2
        rows.append(((p, q), t * t))
        p, q = 3 * p + 4 * q, 2 * p + 3 * q
    return ok, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=15)
    ap.add_argument("--random", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--pell", type=int, default=6)
    a = ap.parse_args()
    rc = 0

    n, fail, (ratio2, arg) = grid(a.max)
    print(f"grid 1<=s_i<=r_i<={a.max}: {n} statistic vectors, {fail} failures")
    r, s, Q, abcm = arg
    print(f"  max (U/mabc)^2 = {ratio2} (< 16 required) at r={r} s={s} U^2={Q} (a,b,c,m)={abcm}")
    if fail or ratio2 >= 16:
        rc = 1

    checked, certified, worst = random_instances(a.random, a.seed)
    print(f"random 0/1 instances: {checked} with nonempty relations, {certified} certified Out <= U_lo <= U"
          f" (exact); max (Out/U_lo)^2 = {worst} ~ {float(worst):.4f}")
    if certified != checked or worst > 1:
        rc = 1

    ok, rows = pell(a.pell)
    print(f"pell sharpness family, {a.pell} terms: {'ok' if ok else 'FAIL'}")
    for (p, q), ratio in rows:
        print(f"  (p,q)=({p},{q})  U/W = {ratio} ~ {float(ratio):.9f}")
    if not ok:
        rc = 1

    print("PASS" if rc == 0 else "FAIL")
    return rc


if __name__ == "__main__":
    sys.exit(main())
