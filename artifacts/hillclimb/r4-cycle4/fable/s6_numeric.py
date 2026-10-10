"""Step 6: numeric stress tests (numpy floats) of the intermediate lemmas, with exact re-checks of anything that
comes within 1e-9 of violating.  The lemmas are proved on paper (see report); this is an independent search for
a counterexample to any proof step.

  Lam : lambda_max(K) <= sigma_R sigma_S sigma_T,   K_{ss'} = sqrt(rho_{yy'} tau_{zz'})  (Lemma Lambda)
  F2  : sum_{x,w} M_{xw}^3 <= |S| sigma_R^2 sigma_S^2 sigma_T^2,  M = A_R A_S A_T      (Lemma F2)
  H3  : ||B||^2 <= sigma_R sigma_S sigma_T sigma_Q, B_{(y,z),(w,x)} = R(x,y) T(z,w)      (Lemma H3)
  Gcls: for every dyadic class R_jk:  Out_jk^3 <= 4 |T||S||Q| sigma_R^2 sigma_S^2 sigma_Q^2 (G, per class)
  Gsum: Out^3 <= |T||S||Q| sigma_R^2 sigma_S^2 sigma_Q^2 (the G term itself)
  plus the annealed Out / monomial ratio for each of the 10 F/G/H monomials (exact re-check of the best).
usage: python3 -I s6_numeric.py <seed> <n_random> <restarts> <steps>
"""
import os, sys, math, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fractions import Fraction as F
from v2lib import certify_instance, vertex_int_exponents, mono_str, out4, size, stats_brackets, mono_powD

HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, "vertices4.json")))
KEPT = [tuple(F(x) for x in v) for v in V["kept"]]
CLS = V["class"]
VINFO = [vertex_int_exponents(v) for v in KEPT]
FGH = [i for i, v in enumerate(KEPT) if CLS[mono_str(v, 4)] in ("F", "G", "H")]


def rand_mat(rng, a, b):
    kind = rng.random()
    M = np.zeros((a, b), dtype=np.int64)
    if kind < 0.25:
        p = rng.uniform(0.15, 1.0)
        M = (np.random.default_rng(rng.randrange(1 << 30)).random((a, b)) < p).astype(np.int64)
    elif kind < 0.5:
        kb = rng.randint(1, max(1, min(a, b)))
        ra = [rng.randrange(kb) for _ in range(a)]
        rb = [rng.randrange(kb) for _ in range(b)]
        for i in range(a):
            for j in range(b):
                if ra[i] == rb[j]:
                    M[i, j] = 1
    elif kind < 0.6:
        M[:] = 1
    elif kind < 0.75:
        c = rng.randrange(a)
        M[c, :] = 1
        d = rng.randrange(b)
        M[:, d] = 1
        for _ in range(rng.randint(0, 2)):
            M[rng.randrange(a), rng.randrange(b)] = 1
    elif kind < 0.9:
        for i in range(a):
            M[i, rng.randrange(b)] = 1
        if rng.random() < 0.5:
            for j in range(b):
                M[rng.randrange(a), j] = 1
    else:
        M[rng.randrange(a), :] = 1
    return M


def rand_instance(rng, maxdim=7):
    nx, ny, nz, nw = [rng.randint(1, maxdim) for _ in range(4)]
    return [rand_mat(rng, nx, ny), rand_mat(rng, ny, nz), rand_mat(rng, nz, nw), rand_mat(rng, nw, nx)]


def sig(M):
    return float(np.linalg.norm(M.astype(float), 2))


def lemma_ratios(mats):
    AR, AS, AT, AQ = mats
    if min(int(M.sum()) for M in mats) == 0:
        return {}
    sR, sS, sT, sQ = sig(AR), sig(AS), sig(AT), sig(AQ)
    res = {}
    rho = AR.T @ AR
    tau = AT @ AT.T
    Sedges = np.argwhere(AS == 1)
    n = len(Sedges)
    K = np.zeros((n, n))
    for i, (y, z) in enumerate(Sedges):
        for j, (y2, z2) in enumerate(Sedges):
            K[i, j] = math.sqrt(rho[y, y2] * tau[z, z2])
    lam = float(np.linalg.eigvalsh(K).max())
    res['Lam'] = lam / (sR * sS * sT)
    M = AR @ AS @ AT
    res['F2'] = float((M.astype(float) ** 3).sum()) / (n * sR ** 2 * sS ** 2 * sT ** 2)
    Qedges = np.argwhere(AQ == 1)
    B = np.zeros((n, len(Qedges)))
    for i, (y, z) in enumerate(Sedges):
        for j, (w, x) in enumerate(Qedges):
            B[i, j] = AR[x, y] * AT[z, w]
    res['H3'] = float(np.linalg.norm(B, 2) ** 2) / (sR * sS * sT * sQ)
    out = float(np.trace(AR @ AS @ AT @ AQ))
    rT, rS, rQ = float(AT.sum()), float(AS.sum()), float(AQ.sum())
    res['Gsum'] = out ** 3 / (rT * rS * rQ * sR ** 2 * sS ** 2 * sQ ** 2)
    # per-class G bound
    dQm = AQ.sum(axis=0)  # d^-_Q(x), indexed by x
    dSp = AS.sum(axis=1)  # d^+_S(y)
    worst_cls = 0.0
    classes = {}
    for (x, y) in np.argwhere(AR == 1):
        if dQm[x] == 0 or dSp[y] == 0:
            continue
        key = (int(math.floor(math.log2(dQm[x]))), int(math.floor(math.log2(dSp[y]))))
        classes.setdefault(key, []).append((x, y))
    for key, edges_ in classes.items():
        Rjk = np.zeros_like(AR)
        for (x, y) in edges_:
            Rjk[x, y] = 1
        o = float(np.trace(Rjk @ AS @ AT @ AQ))
        worst_cls = max(worst_cls, o ** 3 / (4 * rT * rS * rQ * sR ** 2 * sS ** 2 * sQ ** 2))
    res['Gcls'] = worst_cls
    return res


def mono_ratio(mats, idx):
    AR, AS, AT, AQ = mats
    out = float(np.trace(AR @ AS @ AT @ AQ))
    if out <= 0:
        return -1e9
    r = [float(M.sum()) for M in mats]
    if min(r) <= 0:
        return -1e9
    s = [min(sig(M) ** 2, re) for M, re in zip(mats, r)]
    v = KEPT[idx]
    val = math.log(out)
    for e in range(4):
        val -= float(v[e]) * math.log(r[e]) + float(v[4 + e]) * math.log(s[e])
    return val


def anneal(rng, score, steps, mats):
    cur = score(mats)
    best, best_m = cur, [M.copy() for M in mats]
    for t in range(steps):
        temp = 0.4 * (1 - t / steps) + 1e-3
        e = rng.randrange(4)
        M = mats[e]
        i, j = rng.randrange(M.shape[0]), rng.randrange(M.shape[1])
        M[i, j] ^= 1
        new = score(mats)
        if new >= cur or rng.random() < math.exp(min(0.0, (new - cur)) / temp):
            cur = new
            if cur > best:
                best, best_m = cur, [M.copy() for M in mats]
        else:
            M[i, j] ^= 1
    return best, best_m


def to_lists(mats):
    return tuple([[int(x) for x in row] for row in M.tolist()] for M in mats)


def main():
    seed, nrand, restarts, steps = [int(x) for x in sys.argv[1:5]]
    rng = random.Random(seed)
    keys = ['Lam', 'F2', 'H3', 'Gcls', 'Gsum']
    worst = {k: (0.0, None) for k in keys}
    for it in range(nrand):
        mats = rand_instance(rng)
        c = lemma_ratios(mats)
        for k, v in c.items():
            if v > worst[k][0]:
                worst[k] = (v, [M.tolist() for M in mats])
    print(f"seed {seed}: random phase ({nrand} instances) worst ratios:", {k: round(worst[k][0], 6) for k in keys})
    for k in keys:
        def sc(m, k=k):
            v = lemma_ratios(m).get(k)
            return math.log(v) if v and v > 0 else -1e9
        for rst in range(restarts):
            b, m = anneal(rng, sc, steps, rand_instance(rng))
            if math.exp(b) > worst[k][0]:
                worst[k] = (math.exp(b), [M.tolist() for M in m])
    print("after annealing worst ratios:")
    for k in keys:
        flag = "  <-- VIOLATION?" if worst[k][0] > 1 + 1e-9 else ""
        print(f"  {k:5s} {worst[k][0]:.9f}{flag}")
        if worst[k][0] > 1 + 1e-9:
            print("     instance:", worst[k][1])
    # annealing on the F/G/H monomials, with exact re-check
    print("annealed Out/monomial for the F, G, H monomials (float), exact re-check of the best instance:")
    for idx in FGH:
        best, best_m = -1e9, None
        for rst in range(restarts):
            b, m = anneal(rng, lambda mm, idx=idx: mono_ratio(mm, idx), steps, rand_instance(rng))
            if b > best:
                best, best_m = b, m
        mats = to_lists(best_m)
        out, r, s_lo, s_hi, st = certify_instance(mats, [VINFO[idx]])
        print(f"  {CLS[mono_str(KEPT[idx],4)]} {mono_str(KEPT[idx],4):44s} float ratio {math.exp(best):.9f}  exact status {st[0]}  (Out={out}, r={r})")
        if st[0] != 'ok':
            print("     instance:", mats, "s_lo", [str(x) for x in s_lo], "s_hi", [str(x) for x in s_hi])


if __name__ == "__main__":
    main()
