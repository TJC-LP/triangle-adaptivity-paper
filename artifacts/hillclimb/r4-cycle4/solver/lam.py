"""Numerical test of Claim Lambda and relatives.

K is indexed by S-edges (y,z): K[(y,z),(y',z')] = sqrt( |N^-_R(y) ∩ N^-_R(y')| * |N^+_T(z) ∩ N^+_T(z')| ).
Claim Lambda: lambda_max(K) <= sigma_R sigma_S sigma_T.
Also tested:
  Lam1 : lambda_max(K) <= sigma_R sigma_T sqrt(r_S)         (weak, should always hold)
  LamG : lambda_max of K_G[(y,z),(y',z')] = |N_R(y)∩N_R(y')| * |N_T(z)∩N_T(z')|  <= sigma_R^2 sigma_T^2  (compression, must hold)
  LamS : Claim Lambda with R,T complete reduces to |S| <= sigma_S sqrt(|Y||Z|)
usage: python3 -I lam.py <seed> <n_random> <anneal_restarts> <anneal_steps>
"""
import os
import sys
import math
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from claims import rand_mat


def claims(mats):
    AR, AS, AT = mats
    sR = np.linalg.norm(AR, 2)
    sS = np.linalg.norm(AS, 2)
    sT = np.linalg.norm(AT, 2)
    if min(AR.sum(), AS.sum(), AT.sum()) == 0:
        return {}
    GR = AR.T @ AR  # Y x Y
    GT = AT @ AT.T  # Z x Z
    Sedges = np.argwhere(AS == 1)
    n = len(Sedges)
    K = np.zeros((n, n))
    KG = np.zeros((n, n))
    for i, (y, z) in enumerate(Sedges):
        for j, (y2, z2) in enumerate(Sedges):
            KG[i, j] = GR[y, y2] * GT[z, z2]
            K[i, j] = math.sqrt(KG[i, j])
    lam = np.linalg.eigvalsh(K).max()
    lamG = np.linalg.eigvalsh(KG).max()
    res = {}
    res['Lam'] = lam / (sR * sS * sT)
    res['Lam1'] = lam / (sR * sT * math.sqrt(n))
    res['LamG'] = lamG / (sR ** 2 * sT ** 2)
    return res


def rand_instance(rng):
    nx, ny, nz, nw = [rng.randint(1, 7) for _ in range(4)]
    return [rand_mat(rng, nx, ny), rand_mat(rng, ny, nz), rand_mat(rng, nz, nw)]


def anneal(rng, key, steps, mats):
    def sc(m):
        c = claims(m)
        v = c.get(key)
        return math.log(v) if v and v > 0 else -1e9
    cur = sc(mats)
    best, best_m = cur, [M.copy() for M in mats]
    for t in range(steps):
        temp = 0.4 * (1 - t / steps) + 1e-3
        e = rng.randrange(3)
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
    nrand = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    steps = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
    rng = random.Random(seed)
    keys = ['Lam', 'Lam1', 'LamG']
    worst = {k: (0.0, None) for k in keys}
    for it in range(nrand):
        mats = rand_instance(rng)
        c = claims(mats)
        for k, v in c.items():
            if v > worst[k][0]:
                worst[k] = (v, [M.tolist() for M in mats])
    print("random phase worst ratios:")
    for k in keys:
        print(f"  {k:5s} {worst[k][0]:.5f}")
    for k in keys:
        for rst in range(restarts):
            b, m = anneal(rng, k, steps, rand_instance(rng))
            v = math.exp(b)
            if v > worst[k][0]:
                worst[k] = (v, [M.tolist() for M in m])
    print("after annealing worst ratios:")
    for k in keys:
        flag = "  <-- VIOLATION?" if worst[k][0] > 1 + 1e-9 else ""
        print(f"  {k:5s} {worst[k][0]:.5f}{flag}")
        if worst[k][0] > 1 + 1e-9:
            print("     instance (AR, AS, AT):", worst[k][1])


if __name__ == "__main__":
    main()
