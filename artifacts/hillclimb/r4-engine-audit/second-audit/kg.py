import csv, sys, math
from fractions import Fraction as F
for ds in ('codex-l','sci50','w5m'):
    rows=list(csv.DictReader(open(f'engine/kg2/{ds}.csv')))
    by={}
    for r in rows: by.setdefault(r['query_id'],{})[r['policy']]=r
    pols=sorted({r['policy'] for r in rows})
    to=tn=F(0); rs=[]; dec_o=dec_n=0; resc=[]; same=[]; ans=sum(r['answer_ok']=='1' for r in rows)
    for q,p in by.items():
        s,o=p['sampled'],p['stage1']
        dec_o+= o['outcome']=='gate'; dec_n+= s['outcome']=='gate'
        if not s['median_ns'] or not o['median_ns']: continue
        a,b=int(o['median_ns']),int(s['median_ns']); to+=a; tn+=b
        r=F(a,b); rs.append(r)
        (resc if s['outcome']=='rescued' else same).append(F(b,a))
    rs.sort()
    p90=rs[math.ceil(.9*len(rs))-1]
    print(ds,len(by),'pols',pols,f'total {float(to)/1e6:.1f}->{float(tn)/1e6:.1f} ({float(tn/to-1)*100:.1f}%)',
      'declines',dec_o,'->',dec_n, f'p90 {float(p90):.2f} max {float(rs[-1]):.1f}',
      'resc>1.2',sum(x>F(6,5) for x in resc),f'worst {float(max(resc)):.3f}','minspeedup',f'{float(1/max(resc)):.2f}',
      'same>1.2',sum(x>F(6,5) for x in same),'answers',ans,'/',len(rows))
    if ds=='codex-l':
        for pol in ('sampled','stage1'): print('  0267',pol,{k:by['codex-l-0267'][pol][k] for k in ('outcome','pick','median_ns','n_0','n_1','n_2')})
