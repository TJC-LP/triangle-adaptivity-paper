import csv, math, sys, collections
import numpy as np
rows = list(csv.DictReader(open(sys.argv[1])))
f = lambda r,k: float(r[k])
n = len(rows); print("rows", n)
bad = collections.Counter(); worst = {}
def Ucalc(r, s):
    t = [math.sqrt(s[0]*r[1]*r[2]), math.sqrt(s[1]*r[0]*r[2]), math.sqrt(s[2]*r[0]*r[1])]
    t += [r[i]*s[j] for i in range(3) for j in range(3) if i != j]
    return min(t)
ratios = collections.defaultdict(list)
wins = collections.Counter(); tight = collections.Counter()
for x in rows:
    out = f(x,'out'); U = f(x,'U'); l2 = f(x,'l2'); agm = f(x,'agm'); deg = f(x,'deg_bound')
    r = [f(x,f'r{i}') for i in (1,2,3)]; sg = [f(x,f'sigma{i}') for i in (1,2,3)]
    s = [min(sg[i]**2, r[i]) for i in range(3)]
    if out <= 0: bad['out<=0'] += 1
    for name, b in (('U',U),('l2',l2),('agm',agm),('deg',deg),('U_cert',f(x,'U_cert')),('U_schur',f(x,'U_schur')),('U_cw',f(x,'U_cw'))):
        if out > b*(1+1e-9): bad[f'out>{name}'] += 1
    if abs(Ucalc(r,s)/U-1) > 1e-6: bad['U!=recalc'] += 1
    if abs(math.sqrt(r[0]*r[1]*r[2])/agm-1) > 1e-9: bad['agm!=recalc'] += 1
    if abs(min(f(x,'l2_fwd'),f(x,'l2_rev'))/l2-1) > 1e-9: bad['l2!=min'] += 1
    for i in range(3):
        if abs(s[i]/f(x,f's{i+1}')-1) > 1e-9: bad['s!=recalc'] += 1
    if f(x,'U_cert') < U*(1-1e-9): bad['Ucert<U'] += 1
    if 'U_lo' in x:  # exact certification (recertify.py): U_lo <= U_hi <= U_cert <= min(U_schur, U_cw)
        Ul, Uh, Uc = f(x,'U_lo'), f(x,'U_hi'), f(x,'U_cert')
        if not Ul <= Uh: bad['U_lo>U_hi'] += 1
        if not Uh <= Uc: bad['U_hi>U_cert'] += 1
        if not Uc <= min(f(x,'U_schur'), f(x,'U_cw')): bad['U_cert>min(Schur,CW)'] += 1
        if out > Uh: bad['out>U_hi'] += 1
        if not Ul <= U <= Uh: bad['info:U-outside-[U_lo,U_hi]'] += 1
    M = min(f(x,'M1'),f(x,'M2'),f(x,'M3'))
    if abs(M-f(x,'M'))>0.5: bad['M!=minMi'] += 1
    if f(x,'M') > U: bad['M>U'] += 1
    if x['matmul_check'] not in ('ok','skip',''): bad['matmul:'+x['matmul_check']] += 1
    best = min(agm,l2,deg)
    ratios['agm/U'].append(agm/U); ratios['l2/U'].append(l2/U); ratios['deg/U'].append(deg/U)
    ratios['best/U'].append(best/U); ratios['U/out'].append(U/out); ratios['l2/out'].append(l2/out)
    ratios['M/U'].append(f(x,'M')/U); ratios['Ucert/U'].append(f(x,'U_cert')/U); ratios['Uschur/U'].append(f(x,'U_schur')/U)
    wins['U<agm'] += U<agm; wins['U<l2'] += U<l2; wins['U<best'] += U<best; wins['Ucert<l2'] += f(x,'U_cert')<l2
    wins['Ucert<best'] += f(x,'U_cert')<best; wins['schur>1.5'] += f(x,'U_schur')/U>1.5
    g = 'sci50' if x['dataset']=='sci50' else ('SNAP' if x['dataset'] not in ('codex-l','wikidata5m') else 'KG')
    wins[g+':n'] += 1; wins[g+':U<l2'] += U<l2
    tight[min((U,'U'),(l2,'l2'),(deg,'deg'),(agm,'agm'))[1]] += 1
info = {k: v for k, v in bad.items() if k.startswith('info:')}
bad = {k: v for k, v in bad.items() if not k.startswith('info:')}
print("violations/inconsistencies:", bad or "none")
print("info (estimate U vs exact bracket, not a violation):", info or "none")
print("matmul_check values:", collections.Counter(x['matmul_check'] for x in rows))
for k,v in ratios.items():
    v = np.array(v); print(f"{k:10s} min {v.min():.4g} med {np.median(v):.4g} p90 {np.percentile(v,90):.4g} max {v.max():.4g}")
print(dict(wins)); print("tightest", dict(tight))
