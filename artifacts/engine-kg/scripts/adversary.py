"""Independent rebuild of the open-problem-12 adversary, generalized to ANY
fixed (data-independent) sample-position rule.  Exact integer arithmetic only.

Engine semantics mirrored (src/query/triangle_join.zig, estimateCandidate):
  rows of the driver edge in PSO order (subject, object); k = min(64, n);
  sample s at position s*n//k (stride) -- or any other position rule;
  A_hat = n * sum(min(d2, d3)) // k;  pick = argmin 2n + A_hat, ties -> lowest edge;
  greedy (edge 0 = R, edge 1 = T, first join on x) = n_R + n_R * sum(d3) // k;
  gate (ratio 1, proof price 0) accepts iff 2 n_pick + A_hat_pick <= greedy.
Orientation: driver R rows (x,y): d2 = deg_S(y as subject), d3 = deg_T(x as object)
             driver S rows (y,z): d2 = deg_T(z as subject), d3 = deg_R(y as object)
             driver T rows (z,x): d2 = deg_R(x as subject), d3 = deg_S(z as object)
"""
from collections import Counter
from fractions import Fraction
import random
import sys


def stride(n, k=64):
    k = min(k, n)
    return [s * n // k for s in range(k)]


GOLDEN = 0x9E3779B97F4A7C15


def golden(n, k=64):  # data_source.samplePositions
    k = min(k, n)
    if k == n:
        return list(range(n))
    return sorted(((i * GOLDEN) % (1 << 64)) * n >> 64 for i in range(k))


def fixed_random(seed):
    def rule(n, k=64):
        rng = random.Random(seed * 1000003 + n)
        return sorted(rng.randrange(n) for _ in range(min(k, n)))
    return rule


def build(m, rule):
    """R = X x Y; S = (Y \\ Y_J) x Z_S (+pad); T = Z_T x X (+pad).
    Z_S, Z_T interleave in id order and share only z* = the smallest id."""
    X = list(range(10**6, 10**6 + m))
    Y = list(range(2 * 10**6, 2 * 10**6 + m))
    zstar = 3 * 10**6
    ZS = [zstar] + [zstar + 2 * i for i in range(1, m)]
    ZT = [zstar] + [zstar + 2 * i + 1 for i in range(1, m)]
    nR = m * m
    J = sorted({p % m for p in rule(nR)})          # row p = (X[p//m], Y[p%m])
    assert len(J) < m
    dead = {Y[j] for j in J}
    R = sorted((x, y) for x in X for y in Y)
    S = sorted((y, z) for y in Y if y not in dead for z in ZS)
    T = sorted((z, x) for z in ZT for x in X)
    # pad S and T with fresh isolated rows to m^2 + 1 rows each
    S += [(5 * 10**6 + i, 6 * 10**6 + i) for i in range(nR + 1 - len(S))]
    T += [(7 * 10**6 + i, 8 * 10**6 + i) for i in range(nR + 1 - len(T))]
    S.sort(); T.sort()
    return X, Y, ZS, ZT, R, S, T, J


def walked(a, b, swap=True):
    """Entries of the shorter run read by a shorter-side walk with monotone
    seeks into the longer one, stopping once the longer run is exhausted.
    swap=False walks `a` whatever the lengths (the other tie-break)."""
    if swap and len(a) > len(b):
        a, b = b, a
    i = cnt = 0
    for v in a:
        while i < len(b) and b[i] < v:
            i += 1
        if i == len(b):
            break
        cnt += 1
    return cnt


def analyze(m, rule):
    X, Y, ZS, ZT, R, S, T, J = build(m, rule)
    subj = lambda rel: Counter(a for a, b in rel)
    obj = lambda rel: Counter(b for a, b in rel)
    sR, oR, sS, oS, sT, oT = subj(R), obj(R), subj(S), obj(S), subj(T), obj(T)
    rels = [R, S, T]
    d23 = [lambda r: (sS[r[1]], oT[r[0]]),
           lambda r: (sT[r[1]], oR[r[0]]),
           lambda r: (sR[r[1]], oS[r[0]])]
    M = [sum(min(*f(r)) for r in rel) for rel, f in zip(rels, d23)]
    est = []
    for rel, f in zip(rels, d23):
        pos = rule(len(rel))
        est.append(len(rel) * sum(min(*f(rel[p])) for p in pos) // len(pos))
    model = [2 * len(rel) + a for rel, a in zip(rels, est)]
    pick = min(range(3), key=lambda d: (model[d], d))
    posR = rule(len(R))
    greedy = len(R) + len(R) * sum(oT[R[p][0]] for p in posR) // len(posR)
    accepts = model[pick] <= greedy
    # output: triangles (x,y,z) with (x,y) in R, (y,z) in S, (z,x) in T
    Sset, Tset = set(S), set(T)
    out = sum(1 for (x, y) in R for z in (ZS[0],) if (y, z) in Sset and (z, x) in Tset)
    # walked entries with R driving: per live row, walk N2(y)=Z_S vs N3(x)=Z_T
    walk_row = walked(ZS, ZT)
    live = sum(1 for (x, y) in R if sS[y])
    N = len(R) + len(S) + len(T)
    best = min(M)
    obj_pick = 2 * len(rels[pick]) + M[pick]
    obj_best = min(2 * len(rel) + mm for rel, mm in zip(rels, M))
    return dict(m=m, N=N, J=len(J), M=M, est=est, pick=pick, accepts=accepts,
                greedy=greedy, out=out, walked_R=walk_row * live,
                ratio_M=Fraction(M[pick], best), ratio_obj=Fraction(obj_pick, obj_best),
                ratio_M_sqrtN_sq=Fraction(M[pick] ** 2, best ** 2 * N))


def main():
    rules = [("stride", stride), ("golden", golden), ("rand7", fixed_random(7)),
             ("rand11", fixed_random(11))]
    ok = True
    for name, rule in rules:
        for m in (64, 65, 96, 128, 200, 256):
            r = analyze(m, rule)
            j = r["J"]
            exp = [m * m * (m - j), m * (m - j), m * (m - j)]
            good = (r["M"] == exp and r["est"][0] == 0 and r["pick"] == 0 and r["accepts"]
                    and r["out"] == m * (m - j) and r["ratio_M"] == m
                    and r["N"] == 3 * m * m + 2
                    and r["walked_R"] == m * m * (m - j)
                    and r["ratio_obj"] == Fraction(2 * m * m + m * m * (m - j),
                                                   2 * (m * m + 1) + m * (m - j)))
            if m >= 2 * 64:
                good &= r["ratio_obj"] >= Fraction(m, 8)
            # the other tie-break: walking Z_T against Z_S reads >= m - 1 entries
            X, Y, ZS, ZT, *_ = build(m, rule)
            good &= walked(ZT, ZS, swap=False) == m - 1 and walked(ZS, ZT) == m
            good &= 3 * m * m + 2 >= 2048
            ok &= good
            print(name, m, "|J|=%d" % j, "N=%d" % r["N"], "M=%s" % r["M"], "Ahat=%s" % r["est"],
                  "pick=%d" % r["pick"], "gate_accepts=%s" % r["accepts"],
                  "M_pick/minM=%s" % r["ratio_M"], "obj_ratio=%.3f" % float(r["ratio_obj"]),
                  "OK" if good else "FAIL")
    print("ALL OK" if ok else "FAILURES")
    sys.exit(0 if ok else 1)


main()
