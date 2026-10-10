from collections import Counter, defaultdict
from fractions import Fraction
from random import Random

def check(rel):
    R,S,T=rel
    outs=[Counter(a for a,b in e) for e in rel]
    ins=[Counter(b for a,b in e) for e in rel]
    f=[sum(v*v for v in d.values()) for d in outs]
    rev=[sum(v*v for v in d.values()) for d in ins]
    options=[defaultdict(lambda:[0,0]) for _ in range(3)]
    for k,e in enumerate(rel):
        for a,b in e:
            c=1+min(outs[(k+1)%3][b],ins[(k+2)%3][a])
            options[k][a][0]+=c
            options[(k+1)%3][b][1]+=c
    roots=[sum(min(v) for v in d.values()) for d in options]
    C=min(roots);N=sum(map(len,rel))
    Q=min(f[0]*f[1]*f[2],rev[0]*rev[1]*rev[2])
    lhs=N**3*max(C-N,0)**24
    rhs=27*Q**10
    assert lhs<=rhs,(rel,N,C,Q)
    return Fraction(lhs,rhs) if rhs else Fraction(0), (N,C,Q)

rng=Random(314159)
worst=(Fraction(0),None)
for _ in range(5000):
    dims=[rng.randrange(1,17) for _ in range(3)]
    rel=[]
    for k in range(3):
        threshold=rng.randrange(17)
        rel.append({(a,b) for a in range(dims[k]) for b in range(dims[(k+1)%3])
                    if rng.randrange(16)<threshold})
    ratio,witness=check(rel)
    if ratio>worst[0]:worst=(ratio,witness)
print('random_count=5000 seed=314159')
print('max_exact_ratio=',worst[0])
print('witness_N_C_Q=',worst[1])
print('All exact new-upper checks passed.')
