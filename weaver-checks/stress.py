import sys; sys.path.insert(0, '/workspace/review')
from lib import *
import random, math
import numpy as np

def rand_inst(rng, nx, ny, nz, p=None, skew=False):
    def rel(n1, n2, tag1, tag2):
        pairs = set()
        if skew:
            # hubs: a few left vertices with many right neighbours plus sparse rest
            hubs = rng.sample(range(n1), max(1, n1 // 4))
            for h in hubs:
                for v in rng.sample(range(n2), rng.randint(1, n2)):
                    pairs.add(((tag1, h), (tag2, v)))
            for _ in range(rng.randint(0, n1 * n2 // 3)):
                pairs.add(((tag1, rng.randrange(n1)), (tag2, rng.randrange(n2))))
        else:
            q = p if p is not None else rng.random()
            for i in range(n1):
                for j in range(n2):
                    if rng.random() < q: pairs.add(((tag1, i), (tag2, j)))
        return pairs
    return Inst(rel(nx, ny, 'x', 'y'), rel(ny, nz, 'y', 'z'), rel(nz, nx, 'z', 'x'))

def checks(I):
    r, s, t = I.sizes(); N = I.N
    (a, b, c), (a2, b2, c2) = I.moments()
    P = min(a*b*c, a2*b2*c2)
    Cx, Cy, Cz = I.per_root(); C = min(Cx, Cy, Cz)
    MR, MS, MT = I.M(); Mm = min(MR, MS, MT)
    res = {}
    # Thm 5.3 integer form: (C-N)_+^8 <= |R||S||T| * P^2
    d = max(C - N, 0)
    res['thm5.3'] = (d**8, r*s*t*P*P)
    # Lemma 5.2 per-root (unprimed), float: C_x <= |R|+|T| + |S|^(3/8) a^(1/4) b^(1/8) c^(3/8)
    res['lem5.2x'] = (Cx, r + t + s**0.375 * a**0.25 * b**0.125 * c**0.375)
    res['lem5.2x_primed'] = (Cx, r + t + s**0.375 * c2**0.25 * b2**0.125 * a2**0.375)
    res['lem5.2y'] = (Cy, r + s + t**0.375 * b**0.25 * c**0.125 * a**0.375)
    res['lem5.2z'] = (Cz, s + t + r**0.375 * c**0.25 * a**0.125 * b**0.375)
    # Thm 5.4 integer form: N^3 (C-N)_+^24 <= 27 P^10
    res['thm5.4'] = (N**3 * d**24, 27 * P**10)
    # Thm 5.15: min M^5 <= |R||S||T| P
    res['thm5.15'] = (Mm**5, r*s*t*P)
    # Thm 5.16: M_R^4 <= |R||T|^2 a b  and  <= |R||S|^2 a2 c2 ; rotations
    res['thm5.16R'] = (MR**4, min(r*t*t*a*b, r*s*s*a2*c2))
    res['thm5.16S'] = (MS**4, min(s*r*r*b*c, s*t*t*b2*a2))
    res['thm5.16T'] = (MT**4, min(t*s*s*c*a, t*r*r*c2*b2))
    # Cor 5.5(3): min M <= (Lambda Lambda')^(1/3) i.e. minM^6 <= (abc)(a2b2c2)
    res['cor5.5.3'] = (Mm**6, a*b*c*a2*b2*c2)
    # Lemma 5.1: Out <= C <= N + min M ; C <= N + sqrt(rst)
    res['lem5.1a'] = (I.out(), C)
    res['lem5.1b'] = (C, N + Mm)
    res['lem5.1c'] = (C*C, (N + math.sqrt(r*s*t))**2)
    return res

def opnorm_sq(pairs, left, right):
    if not pairs: return 0.0
    li = {v: i for i, v in enumerate(left)}; ri = {v: i for i, v in enumerate(right)}
    A = np.zeros((len(left), len(right)))
    for u, v in pairs: A[li[u], ri[v]] = 1
    return float(np.linalg.norm(A, 2)) ** 2

def spectral_checks(I):
    X = sorted(set(I.dRp) | set(I.dTm)); Y = sorted(set(I.dRm) | set(I.dSp)); Z = sorted(set(I.dSm) | set(I.dTp))
    sR = opnorm_sq(I.R, X, Y); sS = opnorm_sq(I.S, Y, Z); sT = opnorm_sq(I.T, Z, X)
    r, s, t = I.sizes()
    sR, sS, sT = min(sR, r), min(sS, s), min(sT, t)  # clipping
    H = dict(HR=math.sqrt(sR*s*t), HS=math.sqrt(sS*r*t), HT=math.sqrt(sT*r*s))
    D = dict(DRS=r*sS, DRT=r*sT, DSR=s*sR, DST=s*sT, DTR=t*sR, DTS=t*sS)
    U = min(list(H.values()) + list(D.values()))
    MR, MS, MT = I.M(); out = I.out()
    res = {}
    res['thm3.1_upper'] = (out, U * (1 + 1e-9) + 1e-9)
    res['prop4.2_R'] = (MR, min(H['HR'], D['DRS'], D['DRT'], D['DSR'], D['DTR']) * (1 + 1e-9) + 1e-9)
    res['prop4.2_S'] = (MS, min(H['HS'], D['DST'], D['DSR'], D['DTS'], D['DRS']) * (1 + 1e-9) + 1e-9)
    res['prop4.2_T'] = (MT, min(H['HT'], D['DTR'], D['DTS'], D['DRT'], D['DST']) * (1 + 1e-9) + 1e-9)
    res['cor4.3'] = (min(MR, MS, MT), U * (1 + 1e-9) + 1e-9)
    # Lemma 3.2: every degree <= sigma^2
    res['lem3.2'] = (max(list(I.dRp.values()) + list(I.dRm.values()) + [0]), opnorm_sq(I.R, X, Y) * (1 + 1e-9) + 1e-9)
    return res

rng = random.Random(3313)
viol = {}; worst = {}; n = 0
for trial in range(6000):
    nx, ny, nz = (rng.randint(1, 7) for _ in range(3))
    I = rand_inst(rng, nx, ny, nz, skew=rng.random() < 0.4)
    if I.N == 0: continue
    n += 1
    res = checks(I)
    if trial % 3 == 0 and nx * ny * nz <= 200:
        res.update(spectral_checks(I))
    for k, (lhs, rhs) in res.items():
        if lhs > rhs:
            viol.setdefault(k, []).append((lhs, rhs, I.sizes()))
        if rhs > 0:
            worst[k] = max(worst.get(k, 0), lhs / rhs)
print(f"random instances checked: {n}")
for k in sorted(worst):
    print(f"  {k:16s} worst lhs/rhs = {worst[k]:.4f}   violations: {len(viol.get(k, []))}")

# hill-climb: try to maximize each ratio by single-tuple flips
def hill(key, steps=3000, seed=0):
    rng = random.Random(seed)
    nx, ny, nz = 5, 5, 5
    I = rand_inst(rng, nx, ny, nz, p=0.4)
    def ratio(I):
        if I.N == 0: return 0
        lhs, rhs = checks(I)[key]
        return lhs / rhs if rhs > 0 else 0
    best = ratio(I)
    for _ in range(steps):
        R, S, T = set(I.R), set(I.S), set(I.T)
        which = rng.choice('RST')
        tgt = {'R': R, 'S': S, 'T': T}[which]
        tags = {'R': ('x', 'y', nx, ny), 'S': ('y', 'z', ny, nz), 'T': ('z', 'x', nz, nx)}[which]
        pr = ((tags[0], rng.randrange(tags[2])), (tags[1], rng.randrange(tags[3])))
        if pr in tgt: tgt.remove(pr)
        else: tgt.add(pr)
        J = Inst(R, S, T)
        rj = ratio(J)
        if rj >= best:
            best, I = rj, J
    return best, I
print("\nhill-climb (5x5x5, 3000 flips) best ratios:")
for key in ['thm5.3', 'thm5.4', 'thm5.15', 'thm5.16R', 'cor5.5.3']:
    bests = [hill(key, seed=s)[0] for s in range(4)]
    print(f"  {key:10s} {['%.4f' % b for b in bests]}  (must stay <= 1)")
