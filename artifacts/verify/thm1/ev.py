# Independent evaluator for the paper section: literal definitions (general-plan.md 1.1, corrected A_z).
from collections import defaultdict
def ev(R,S,T):
    a=defaultdict(int);ap=defaultdict(int);b=defaultdict(int);bp=defaultdict(int);c=defaultdict(int);cp=defaultdict(int)
    Rf=defaultdict(list);Rb=defaultdict(list);Sf=defaultdict(list);Sb=defaultdict(list);Tf=defaultdict(list);Tb=defaultdict(list)
    for x,y in R: a[x]+=1;ap[y]+=1;Rf[x].append(y);Rb[y].append(x)
    for y,z in S: b[y]+=1;bp[z]+=1;Sf[y].append(z);Sb[z].append(y)
    for x,z in T: cp[x]+=1;c[z]+=1;Tf[x].append(z);Tb[z].append(x)
    sq=lambda d: sum(v*v for v in d.values())
    al,be,ga=sq(a),sq(b),sq(c); alp,bep,gap=sq(ap),sq(bp),sq(cp)
    # root x: option R walks y in R(x,.), intersects T(x,.) with S(y,.); option T walks z in T(x,.), intersects R(x,.) with S(.,z)
    rx={x:(sum(1+min(cp[x],b[y]) for y in Rf[x]), sum(1+min(a[x],bp[z]) for z in Tf[x])) for x in set(Rf)|set(Tf)}
    # root y: option x walks x in R(.,y), intersects S(y,.) with T(x,.); option z walks z in S(y,.), intersects R(.,y) with T(.,z)
    ry={y:(sum(1+min(b[y],cp[x]) for x in Rb[y]), sum(1+min(ap[y],c[z]) for z in Sf[y])) for y in set(Rb)|set(Sf)}
    # root z: option y walks y in S(.,z), intersects T(.,z) with R(.,y); option x walks x in T(.,z), intersects S(.,z) with R(x,.)
    rz={z:(sum(1+min(c[z],ap[y]) for y in Sb[z]), sum(1+min(bp[z],a[x]) for x in Tb[z])) for z in set(Sb)|set(Tb)}
    Ax=sum(min(p) for p in rx.values()); Ay=sum(min(p) for p in ry.values()); Az=sum(min(p) for p in rz.values())
    MR=sum(min(cp[x],b[y]) for x,y in R); MS=sum(min(ap[y],c[z]) for y,z in S); MT=sum(min(a[x],bp[z]) for x,z in T)
    N=len(R)+len(S)+len(T)
    return dict(N=N,R=len(R),S=len(S),T=len(T),al=al,be=be,ga=ga,alp=alp,bep=bep,gap=gap,Ax=Ax,Ay=Ay,Az=Az,A=min(Ax,Ay,Az),
                MR=MR,MS=MS,MT=MT,rx=rx,ry=ry,rz=rz,Rf=Rf,Sf=Sf,Tf=Tf,Rb=Rb,Sb=Sb,Tb=Tb,deg=(a,ap,b,bp,c,cp))
def B2(e): return min(e['al']*e['be']*e['ga'], e['alp']*e['bep']*e['gap'])**(1/3)
def Q(e):
    return sum(1 for x,ys in e['Rf'].items() for y in ys for z in e['Sf'].get(y,()) if z in set(e['Tf'].get(x,())))
def rotate(R,S,T):  # X'=Z, Y'=X, Z'=Y : R'(z,x)=T(x,z), S'(x,y)=R(x,y), T'(z,y)=S(y,z)
    return {(z,x) for x,z in T}, set(R), {(z,y) for y,z in S}
def biregular(L,Rt,deg_left):
    p,q=len(L),len(Rt); ne=p*deg_left; assert ne%q==0
    return {(L[u],Rt[(u*deg_left+l)%q]) for u in range(p) for l in range(deg_left)}
