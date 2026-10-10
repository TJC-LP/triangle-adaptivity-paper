"""Screen candidate lemmas for G.  h = A_Q A_R A_S (W x Z), 3-paths w->x->y->z.
  G3 : ||h||_1 * ||h||_F^2 <= r_S r_Q s_R s_S s_Q
  G4 : ||h||_F^2 <= sqrt(r_S r_Q) s_R sqrt(s_S s_Q)  * sqrt(||h||_1 / ... )  (not used)
  GN : lambda_max(normalized Gram of v_r = q_x (x) s_y, r in R) * ||h||_1^2 <= r_S r_Q s_R s_S s_Q
  GH : ||h||_F^2 * ||h||_1 <= r_T-free bound check in the form (sum_T h)^3 <= r_T * ... is G itself
"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from claims import rand_mat, anneal as _anneal

def claims(mats):
    AR, AS, AT, AQ = mats
    r = [float(M.sum()) for M in mats]
    if min(r) == 0: return {}
    s = [min(np.linalg.norm(M, 2)**2, re) for M, re in zip(mats, r)]
    rR, rS, rT, rQ = r; sR, sS, sT, sQ = s
    h = AQ @ AR @ AS
    h1 = float(h.sum()); hF2 = float((h**2).sum())
    out = float(np.trace(AR @ AS @ AT @ AQ))
    res = {}
    res['G'] = out**3 / (rS*rT*rQ*sR*sS*sQ)
    res['G3'] = h1 * hF2 / (rS*rQ*sR*sS*sQ)
    # normalized Gram over R-edges
    Redges = np.argwhere(AR == 1)
    GQ = AQ.T @ AQ; GS = AS @ AS.T
    dQ = np.diag(GQ); dS = np.diag(GS)
    idx = [(x, y) for (x, y) in Redges if dQ[x] > 0 and dS[y] > 0]
    if idx:
        n = len(idx)
        Gm = np.zeros((n, n))
        for i, (x, y) in enumerate(idx):
            for j, (x2, y2) in enumerate(idx):
                Gm[i, j] = GQ[x, x2] * GS[y, y2] / math.sqrt(dQ[x]*dQ[x2]*dS[y]*dS[y2])
        lam = np.linalg.eigvalsh(Gm).max()
        res['GN'] = lam * h1**2 / (rS*rQ*sR*sS*sQ)
    return res

def rand_instance(rng):
    nx, ny, nz, nw = [rng.randint(1, 6) for _ in range(4)]
    return [rand_mat(rng, nx, ny), rand_mat(rng, ny, nz), rand_mat(rng, nz, nw), rand_mat(rng, nw, nx)]

def anneal(rng, key, steps, mats):
    def sc(m):
        v = claims(m).get(key)
        return math.log(v) if v and v > 0 else -1e9
    cur = sc(mats); best, best_m = cur, [M.copy() for M in mats]
    for t in range(steps):
        temp = 0.4*(1-t/steps)+1e-3
        e = rng.randrange(4); M = mats[e]
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
keys = ['G', 'G3', 'GN']
worst = {k: (0.0, None) for k in keys}
for it in range(nrand):
    c = claims(rand_instance(rng))
    for k, v in c.items():
        if v > worst[k][0]: worst[k] = (v, None)
print("random:", {k: round(worst[k][0], 5) for k in keys})
for k in keys:
    for rst in range(restarts):
        b, m = anneal(rng, k, steps, rand_instance(rng))
        if math.exp(b) > worst[k][0]: worst[k] = (math.exp(b), [M.tolist() for M in m])
for k in keys:
    flag = " <-- VIOLATION?" if worst[k][0] > 1+1e-9 else ""
    print(f"  {k:3s} {worst[k][0]:.5f}{flag}")
    if worst[k][0] > 1+1e-9: print("    ", worst[k][1])
