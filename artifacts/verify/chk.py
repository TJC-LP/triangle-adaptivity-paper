import random, math
import numpy as np
def U(r, s):
    R,S,T = r; sR,sS,sT = s
    return min(math.sqrt(sR*S*T), math.sqrt(sS*R*T), math.sqrt(sT*R*S), R*sS, R*sT, S*sR, S*sT, T*sR, T*sS)
# (1) upper bound on random instances (with exact stats)
rng = random.Random(7); worst = 0
for it in range(3000):
    nx,ny,nz = [rng.randint(1,9) for _ in range(3)]
    p = rng.random()
    AR = (np.random.default_rng(it).random((nx,ny)) < p).astype(float)
    AS = (np.random.default_rng(it+10**6).random((ny,nz)) < rng.random()).astype(float)
    AT = (np.random.default_rng(it+2*10**6).random((nz,nx)) < rng.random()).astype(float)
    if min(AR.sum(),AS.sum(),AT.sum()) == 0: continue
    out = np.trace(AR@AS@AT)
    r = (AR.sum(), AS.sum(), AT.sum())
    s = tuple(min(np.linalg.norm(A,2)**2, A.sum()) for A in (AR,AS,AT))
    worst = max(worst, out / U(r,s))
print("max Out/U over random instances:", round(worst,4), "(must be <= 1)")
# (2) construction achieves > U/4
w = 0
for it in range(200000):
    r = [10**rng.uniform(0,7) for _ in range(3)]
    s = [min(r[i], 10**rng.uniform(0, math.log10(r[i])+0.5)) for i in range(3)]
    r = [math.floor(x) or 1 for x in r]; s=[max(1.0,min(s[i],r[i])) for i in range(3)]
    u = U(r,s); R,S,T = r; sR,sS,sT = s
    a = math.floor(max(1,u/S)); b = math.floor(max(1,u/T)); c = math.floor(max(1,u/R))
    m = math.floor(min(R/(a*b), S/(b*c), T/(c*a)))
    assert a*b <= sR+1e-9 and b*c <= sS+1e-9 and c*a <= sT+1e-9, (r,s,a,b,c)
    out = m*a*b*c
    w = max(w, u/out if out else float('inf'))
print("max U/Out_construction:", round(w,4), "(theorem: < 4)")
