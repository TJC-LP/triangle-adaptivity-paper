import csv, sys, math
from fractions import Fraction as F
def med(xs):
    xs=sorted(xs); n=len(xs); return xs[n//2] if n%2 else (xs[n//2-1]+xs[n//2])/2
def q(xs,p):
    xs=sorted(xs); return xs[max(0,math.ceil(p*len(xs))-1)]
for p in sys.argv[1:]:
    by={}
    for r in csv.DictReader(open(p)): by.setdefault(r['query_id'],{})[r['policy']]=r
    oc={}; ex={}; ro=[]; still=0; s15=0; o15=0; gto=[]
    for k,pol in by.items():
        s=pol['sampled']; oc[s['outcome']]=oc.get(s['outcome'],0)+1
        e=pol['exact']; ex[e['outcome']]=ex.get(e['outcome'],0)+1
        g=pol['greedy']
        if not g['median_ns'] or g['outcome']=='timeout': gto.append(k)
        f=[int(pol[f'forced:{i}']['median_ns']) for i in range(3) if pol[f'forced:{i}']['median_ns']]
        orc=min(f)
        if s['outcome']=='rescued': ro.append(F(int(s['median_ns']),orc))
        if s['outcome']=='gate' and g['median_ns']:
            still+=1
            gt=int(g['median_ns'])
            # sampled choice without the gate: forced time of sampled pick
            pk=s['pick']; ft=int(pol[f'forced:{pk}']['median_ns'])
            if F(gt,ft)>F(3,2): s15+=1
            if F(gt,orc)>F(3,2): o15+=1
    print(p, 'outcomes',oc,'exact',ex,'greedy timeouts',gto)
    print(f'  rescued/oracle median {float(med(ro)):.3f} p90 {float(q(ro,0.9)):.3f}; still declined {still}: sampled-nogate>1.5x {s15}, oracle>1.5x {o15}')
