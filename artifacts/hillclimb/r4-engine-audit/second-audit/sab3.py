import itertools, random, sys
def seek(o,n): return 0 if n==0 or o<=n else (o//n).bit_length()-1
def cost(c,br,walk=None):
    n,n2,n3,w=c['n'],c['n2'],c['n3'],c['w'] if walk is None else walk
    l2,l3=seek(n2,n),seek(n3,n)
    return n*(4+l2+3*l3)+20*w if br=='L' else n*(8+2*l2+6*l3)+30*w
def floor(c,br): return cost(c,br,0)
def gcost(e,br):
    seed=e['n0']*(40 if e['pf'] else 9)
    return seed+26*e['path'] if br=='L' else seed
def cheapest(e,cand,samp,br):
    b=0
    for d in (1,2):
        if samp[d] and cost(cand[d],br)<cost(cand[b],br): b=d
    return b
def rule(e,cand,samp,md):
    a=cheapest(e,cand,samp,'L')
    if cand[a]['n']>=md and 3*cost(cand[a],'L')<=2*gcost(e,'L'): return ('L',a)
    s=cheapest(e,cand,samp,'S')
    if cost(cand[s],'S')<=gcost(e,'S'): return ('S',s)
    return None
def und(f,d,c,b): return f<c or (f==c and d<b)
def unsettled(e,cand,samp,md):
    BL=2*gcost(e,'L'); BS=gcost(e,'S')
    a=cheapest(e,cand,samp,'L'); ac=cost(cand[a],'L')
    ok=cand[a]['n']>=md and 3*ac<=BL
    s=cheapest(e,cand,samp,'S'); sc=cost(cand[s],'S')
    for d in range(3):
        if samp[d]: continue
        fl=floor(cand[d],'L')
        if 3*fl<=BL and und(fl,d,ac,a): return d
        if ok: continue
        fs=floor(cand[d],'S')
        pass
    return None
def decide(e,cand,samp,md):
    samp=list(samp); k=0
    while True:
        d=unsettled(e,cand,samp,md)
        if d is None: return rule(e,cand,samp,md),k
        samp[d]=True; k+=1
def old_skip(e,cand,samp,md):
    # build-R1-style: skip unsampled if n<md (approximation of old behaviour for sabotage)
    return None
stats={'n':0,'changed':0,'samples':0}
def check(e,cand,samp,md):
    got,k=decide(e,cand,samp,md); want=rule(e,cand,[True]*3,md)
    stats['n']+=1; stats['samples']+=k
    if rule(e,cand,samp,md)!=want: stats['changed']+=1
    if got!=want:
        print('COUNTEREXAMPLE',e,cand,samp,md,got,want); sys.exit(1)
# auditor witness
cand=[dict(n=1000,n2=20000,n3=10000,w=15000),dict(n=10000,n2=20000,n3=1000,w=0),dict(n=20000,n2=10000,n3=1000,w=0)]
e=dict(n0=1000,pf=False,path=15000)
assert [cost(c,'L') for c in cand]==[317000,50000,80000] and [cost(c,'S') for c in cand]==[484000,100000,160000]
assert 2*gcost(e,'L')==798000 and gcost(e,'S')==9000
print('witness full', rule(e,cand,[True]*3,16384), 'lazy', decide(e,cand,[True,False,False],16384), 'initial-subset', rule(e,cand,[True,False,True],16384))
check(e,cand,[True,False,False],16384); check(e,cand,[True,False,True],16384)
# exhaustive small grid (tie-heavy)
ns=[1,2,3,4,8]; ws=[0,1,2,3,5]
for n in itertools.product(ns,repeat=3):
  for w in itertools.product(ws,repeat=3):
    cnd=[]
    for d in range(3):
        o=[n[(d+1)%3],n[(d+2)%3]]
        cnd.append(dict(n=n[d],n2=o[0],n3=o[1],w=w[d]))
    for pf in (False,True):
      for path in (0,1,2,5):
        e=dict(n0=n[0],pf=pf,path=path)
        for md in (1,2,3,5,9):
          for m in itertools.product((False,True),repeat=2):
            check(e,cnd,[True,m[0],m[1]],md)
print('exhaustive',stats)
# random wide, incl. swapped n2/n3 and ties via coarse values
r=random.Random(3313)
for i in range(300000):
    L=[r.choice([1,2,10,100,1000,10000,16383,16384,20000,10**5,r.randint(1,10**5)]) for _ in range(3)]
    cnd=[]
    for d in range(3):
        o=[L[(d+1)%3],L[(d+2)%3]];
        if r.random()<.5:o.reverse()
        w=0 if r.random()<.3 else r.choice([r.randint(0,L[d]*30), r.randint(0,40)])
        cnd.append(dict(n=L[d],n2=o[0],n3=o[1],w=w))
    e=dict(n0=L[0],pf=r.random()<.5,path=r.choice([0,r.randint(0,L[0]*20),r.randint(0,100)]))
    md=r.choice([1,1000,16384,r.randint(1,50000)])
    check(e,cnd,[True,r.random()<.5,r.random()<.5],md)
print('total',stats)
