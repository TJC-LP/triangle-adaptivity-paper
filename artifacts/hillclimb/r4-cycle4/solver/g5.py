"""Screen G5: ||h||_1^2 * ||h||_inf <= r_S r_Q s_R s_S s_Q, h = A_Q A_R A_S.  Also G3 again."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from claims import rand_mat

def claims(mats):
    AR, AS, AQ = mats
    r = [float(M.sum()) for M in mats]
    if min(r) == 0: return {}
    s = [min(np.linalg.norm(M, 2)**2, re) for M, re in zip(mats, r)]
    rR, rS, rQ = r; sR, sS, sQ = s
    h = AQ @ AR @ AS
    h1 = float(h.sum()); hF2 = float((h**2).sum()); hinf = float(h.max())
    return {'G3': h1*hF2/(rS*rQ*sR*sS*sQ), 'G5': h1*h1*hinf/(rS*rQ*sR*sS*sQ)}

def rand_instance(rng):
    nx, ny, nz, nw = [rng.randint(1, 7) for _ in range(4)]
    return [rand_mat(rng, nx, ny), rand_mat(rng, ny, nz), rand_mat(rng, nw, nx)]

def anneal(rng, key, steps, mats):
    def sc(m):
        v = claims(m).get(key)
        return math.log(v) if v and v > 0 else -1e9
    cur = sc(mats); best, best_m = cur, [M.copy() for M in mats]
    for t in range(steps):
        temp = 0.4*(1-t/steps)+1e-3
        e = rng.randrange(3); M = mats[e]
        i, j = rng.randrange(M.shape[0]), rng.randrange(M.shape[1])
        M[i, j] ^= 1
        new = sc(mats)
        if new >= cur or rng.random() < math.exp((new-cur)/temp):
            cur = new
            if cur > best: best, best_m = cur, [M.copy() for M in mats]
        else: M[i, j] ^= 1
    return best, best_m

seed = int(sys.argv[1]); nrand = int(sys.argv[2]); restarts = int(sys.argv[3]); steps = int(sys.argv[4])
rng = random.Random(seed)
keys = ['G3', 'G5']
worst = {k: (0.0, None) for k in keys}
for it in range(nrand):
    c = claims(rand_instance(rng))
    for k, v in c.items():
        if v > worst[k][0]: worst[k] = (v, None)
print("random:", {k: round(float(worst[k][0]), 5) for k in keys})
for k in keys:
    for rst in range(restarts):
        b, m = anneal(rng, k, steps, rand_instance(rng))
        if math.exp(b) > worst[k][0]: worst[k] = (math.exp(b), [M.tolist() for M in m])
for k in keys:
    flag = " <-- VIOLATION?" if worst[k][0] > 1+1e-9 else ""
    print(f"  {k:3s} {float(worst[k][0]):.5f}{flag}")
    if worst[k][0] > 1+1e-9: print("    (AR, AS, AQ) =", worst[k][1])
