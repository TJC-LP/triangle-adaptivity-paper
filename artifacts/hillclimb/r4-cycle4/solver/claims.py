"""Numerical screening of candidate intermediate lemmas for the 4-cycle bounds F, G, H.

Float sigma (numpy); any ratio > 1 - 1e-9 is reported with the instance so it can be rechecked
exactly.  Instances: random, block unions, stars, spiders, matchings, and annealing on each claim.

Claims (f = A_R A_S A_T : X x W, 3-path counts; h = A_Q A_R A_S : W x Z):
  F   : Out^3 <= r_S r_Q^2 s_R s_S s_T
  F2  : sum f^3 <= r_S s_R s_S s_T
  F2w : max f * ||f||_F^2 <= r_S s_R s_S s_T
  G   : Out^3 <= r_S r_T r_Q s_R s_S s_Q
  G2  : (sum h^{3/2})^2 <= r_S r_Q s_R s_S s_Q
  H   : Out^4 <= r_S^2 r_Q^2 s_R s_S s_T s_Q
  H2  : <G_S,G_T> <G_Q,G_R> <= r_S r_Q sqrt(s_R s_S s_T s_Q)   (G_S = A_S^T A_S, G_T = A_T A_T^T on Z;
                                                             G_Q = A_Q^T A_Q, G_R = A_R A_R^T on X)
  H3  : ||B||^2 <= sqrt(s_R s_S s_T s_Q),  B = incidence S-edges x Q-edges: B[(y,z),(w,x)] = R(x,y) T(z,w)
usage: python3 -I claims.py <seed> <n_random> <anneal_restarts> <anneal_steps>
"""
import os
import sys
import math
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np


def stats(mats):
    r = [float(M.sum()) for M in mats]
    s = []
    for M, re in zip(mats, r):
        if re == 0:
            s.append(0.0)
        else:
            s.append(min(np.linalg.norm(M, 2) ** 2, re))
    return r, s


def claims(mats):
    AR, AS, AT, AQ = mats
    r, s = stats(mats)
    rR, rS, rT, rQ = r
    sR, sS, sT, sQ = s
    if min(r) == 0:
        return {}
    out = float(np.trace(AR @ AS @ AT @ AQ))
    f = AR @ AS @ AT  # X x W
    h = AQ @ AR @ AS  # W x Z
    res = {}
    res['F'] = out ** 3 / (rS * rQ ** 2 * sR * sS * sT)
    res['F2'] = float((f ** 3).sum()) / (rS * sR * sS * sT)
    res['F2w'] = float(f.max() * (f ** 2).sum()) / (rS * sR * sS * sT)
    res['G'] = out ** 3 / (rS * rT * rQ * sR * sS * sQ)
    res['G2'] = float((h ** 1.5).sum()) ** 2 / (rS * rQ * sR * sS * sQ)
    res['H'] = out ** 4 / (rS ** 2 * rQ ** 2 * sR * sS * sT * sQ)
    GS = AS.T @ AS
    GT = AT @ AT.T
    GQ = AQ.T @ AQ
    GR = AR @ AR.T
    res['H2'] = float((GS * GT).sum() * (GQ * GR).sum()) / (rS * rQ * math.sqrt(sR * sS * sT * sQ))
    # B: rows = S-edges (y,z), cols = Q-edges (w,x)
    Sedges = np.argwhere(AS == 1)
    Qedges = np.argwhere(AQ == 1)
    if len(Sedges) and len(Qedges):
        B = np.zeros((len(Sedges), len(Qedges)))
        for i, (y, z) in enumerate(Sedges):
            for j, (w, x) in enumerate(Qedges):
                B[i, j] = AR[x, y] * AT[z, w]
        res['H3'] = np.linalg.norm(B, 2) ** 2 / math.sqrt(sR * sS * sT * sQ)
    return res


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
    elif kind < 0.75:  # spider / double star
        c = rng.randrange(a)
        M[c, :] = 1
        for j in range(b):
            M[rng.randrange(a), j] = 1
        for i in range(a):
            M[i, rng.randrange(b)] = 1
    elif kind < 0.9:  # near-matching
        for i in range(a):
            M[i, rng.randrange(b)] = 1
        for j in range(b):
            if rng.random() < 0.5:
                M[rng.randrange(a), j] = 1
    else:  # star
        M[rng.randrange(a), :] = 1
    return M


def rand_instance(rng):
    nx, ny, nz, nw = [rng.randint(1, 7) for _ in range(4)]
    return [rand_mat(rng, nx, ny), rand_mat(rng, ny, nz), rand_mat(rng, nz, nw), rand_mat(rng, nw, nx)]


def anneal(rng, key, steps, mats):
    def sc(m):
        c = claims(m)
        v = c.get(key)
        return math.log(v) if v and v > 0 else -1e9
    cur = sc(mats)
    best, best_m = cur, [M.copy() for M in mats]
    for t in range(steps):
        temp = 0.4 * (1 - t / steps) + 1e-3
        e = rng.randrange(4)
        M = mats[e]
        i, j = rng.randrange(M.shape[0]), rng.randrange(M.shape[1])
        M[i, j] ^= 1
        new = sc(mats)
        if new >= cur or rng.random() < math.exp((new - cur) / temp):
            cur = new
            if cur > best:
                best, best_m = cur, [M.copy() for M in mats]
        else:
            M[i, j] ^= 1
    return best, best_m


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    nrand = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    steps = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
    rng = random.Random(seed)
    keys = ['F', 'F2', 'F2w', 'G', 'G2', 'H', 'H2', 'H3']
    worst = {k: (0.0, None) for k in keys}
    for it in range(nrand):
        mats = rand_instance(rng)
        c = claims(mats)
        for k, v in c.items():
            if v > worst[k][0]:
                worst[k] = (v, [M.tolist() for M in mats])
    print("random phase worst ratios:")
    for k in keys:
        print(f"  {k:4s} {worst[k][0]:.5f}")
    for k in keys:
        for rst in range(restarts):
            b, m = anneal(rng, k, steps, rand_instance(rng))
            v = math.exp(b)
            if v > worst[k][0]:
                worst[k] = (v, [M.tolist() for M in m])
    print("after annealing worst ratios:")
    for k in keys:
        flag = "  <-- VIOLATION?" if worst[k][0] > 1 + 1e-9 else ""
        print(f"  {k:4s} {worst[k][0]:.5f}{flag}")
        if worst[k][0] > 1 + 1e-9:
            print("     instance:", worst[k][1])


if __name__ == "__main__":
    main()
