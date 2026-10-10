"""Additional independent exact checks; loads only our own newly written verifier."""
import runpy
D=runpy.run_path('fourcycle_check.py',run_name='fourcycle_library')
globals().update({k:v for k,v in D.items() if not k.startswith('__')})

def norm_upper2(a,steps=20):
    g=gram(a); x=[1]*len(g)
    for _ in range(steps):
        y=[sum(t*v for t,v in zip(row,x)) for row in g]
        if not any(y):return F(0)
        z=0
        for v in y:z=gcd(z,v)
        x=[v//z for v in y]
    y=[sum(t*v for t,v in zip(row,x)) for row in g]
    return max(F(v,u) for u,v in zip(x,y) if u)

rng=Random(6021); count=eq=0; undecided=[]
for trial in range(350):
    dims=[rng.randrange(1,6) for _ in range(4)]; p=rng.randrange(1,10)
    mats=[[[int(rng.randrange(10)<p) for _ in range(dims[(e+1)%4])] for _ in range(dims[e])] for e in range(4)]
    if any(not sum(map(sum,a)) for a in mats):continue
    se=[(y,z) for y in range(dims[1]) for z in range(dims[2]) if mats[1][y][z]]
    qe=[(w,x) for w in range(dims[3]) for x in range(dims[0]) if mats[3][w][x]]
    b=[[mats[0][x][y]*mats[2][z][w] for w,x in qe] for y,z in se]
    hi=norm_upper2(b); slo=[lowernorm2(a) for a in mats]
    if hi*hi>prod(slo):
        hi=norm_upper2(b,120);slo=[lowernorm2(a,120) for a in mats]
    if hi*hi>prod(slo):undecided.append(trial)
    else:count+=1;eq+=hi*hi==prod(slo)
print('H3_DIRECT_CERTIFICATES',count,'equalities',eq,'undecided',undecided)

# D4 orbit partition generated from edge index permutations.
seen=set();sizes=[]
for t in TERMS:
    if t in seen:continue
    orb=set()
    for direction in (-1,1):
        for shift in range(4):
            p=[(direction*e+shift)%4 for e in range(4)]; tt=[F(0)]*8
            for e in range(4):tt[p[e]]=t[e];tt[4+p[e]]=t[4+e]
            orb.add(tuple(tt))
    assert orb<=set(TERMS);seen|=orb;sizes.append(len(orb))
print('D4_ORBITS',len(sizes),'sizes',sorted(sizes))

for t in (F(3,2),F(7,4),F(15,8),F(31,16),F(63,32),F(1023,512)):
    ns=[F(1)]*13
    for j in (2,3,6,12):ns[j]=t
    st=arc_stats(ns);u=prod(ns);assert u12(st[:4],st[4:])==u**12
    print('RAW_ROUNDING_16_LIMIT','t',t,'r',st[:4],'s',st[4:],'U',u,'Out',1)

# Exact counterexample to the report's stronger side condition L>=t^2.
t=F(3,2);L=F(3);b=u12([L,t,L,L],[t,t,t,L])
print('SMALL_L_COUNTEREXAMPLE','t',t,'L',L,'L_ge_t2',L>=t*t,'U12',b,'t36',t**36)
assert b<t**36
# Fractional Frobenius sizes and norms for the real matrix counterexample.
out=F(1,2);r=[F(2),F(1,2),F(2),F(1,2)];s=[F(1),F(1,4),F(1),F(1,4)]
h=next(t for t in TERMS if TERMS[t]=='H' and t[1])
assert val12(r,s,POWERS[h])==F(1,4)**12
print('REAL_MATRIX_H_COUNTEREXAMPLE','Out',out,'H',F(1,4))
thresholds=[]
for v,label in TERMS.items():
    a=sum(v[i] for i in (0,2,3,7));b=sum(v[i] for i in (1,4,5,6))
    if a:thresholds.append((3-b)/a)
print('CONSTANT8_EXACT_L_THRESHOLD_POWER',max(thresholds))
assert max(thresholds)==3
