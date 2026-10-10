from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import product

def orient(edges,shape,d):
 a,b=shape[d];e2=next(j for j in range(3) if j!=d and b in shape[j]);e3=next(j for j in range(3) if j!=d and j!=e2)
 return e2,e3,shape[e2].index(b),shape[e3].index(a)
def budgets(edges,shape,d,sample=True):
 e2,e3,i2,i3=orient(edges,shape,d);ds2=Counter(v[i2] for v in edges[e2]);ds3=Counter(v[i3] for v in edges[e3]);R=sorted(edges[d]);n=len(R);k=min(64,n) if sample else n
 sums=[0,0,0]
 for j in range(k):
  a,b=R[j*n//k];u,v=ds2[b],ds3[a]
  for z,w in enumerate((min(u,v),u,v)):sums[z]+=w
 return dict(n=n,n2=len(edges[e2]),n3=len(edges[e3]),A=n*sums[0]//k,L=n*sums[1]//k,R=n*sums[2]//k,e2=e2,e3=e3)
def price(c,structural=False,floor=False):
 d2=max(0,(c['n2']//c['n']).bit_length()-1);d3=max(0,(c['n3']//c['n']).bit_length()-1)
 a=c['n']*(4+d2+3*d3)
 return (2*a+30*c['A'] if structural else a+20*c['A']) if not floor else (2*a if structural else a)

def reproduce_rescue():
 # Positive IDs meet the .lb range contract; +1 globally preserves PSO ordering.
 E0={(i+1,i+1) for i in range(1000)};chosen={1000*j//64 for j in range(64)}
 E1={(i+1,15*i+h+1) for i in chosen for h in range(15)}
 E2={(i+1,100000+15*i+h+1) for i in chosen for h in range(15)}
 E1.update((10001+j,200001+j) for j in range(10000-len(E1)))
 E2.update((30001+j,300001+j) for j in range(20000-len(E2)))
 E=[E0,E1,E2];shape=[(0,1),(0,2),(1,2)]
 B=[budgets(E,shape,d) for d in range(3)];print('LITERAL_POSITIVE_ID_CANDIDATES',B)
 assert all(a>0 and b>0 for e in E for a,b in e)
 assert set(b for a,b in E1).isdisjoint(b for a,b in E2)
 # Greedy orderRun: exact sizes unique, hence seed0 then connected edge1 then edge2.
 assert list(map(len,E))==[1000,10000,20000];assert sum(map(len,E))==31000>=2048
 probe=B[0]['e2']==1;path=B[0]['L' if probe else 'R'];greedy=B[0]['n']+path
 picked=[True]+[2*B[d]['n']<=greedy for d in (1,2)]
 assert picked==[True,False,False] and 2*B[0]['n']+B[0]['A']==17000>greedy==16000
 bg=B[0]['n']*(40 if probe else 9);large=2*(bg+26*path)
 def decide(prune):
  available=picked.copy()
  for d,c in enumerate(B):
   if available[d]:continue
   if prune and (c['n']<16384 or 3*price(c,floor=True)>large) and price(c,True,True)>bg:continue
   available[d]=True
  candidates=[d for d in range(3) if available[d]]
  dl=min(candidates,key=lambda d:(price(B[d]),d))
  if B[dl]['n']>=16384 and 3*price(B[dl])<=large:return available,('large',dl)
  ds=min(candidates,key=lambda d:(price(B[d],True),d))
  return available,('structural',ds) if price(B[ds],True)<=bg else None
 print('SEED','probe_first',probe,'path',path,'greedy',greedy,'total_floor_input',sum(map(len,E)))
 print('RESCUE_COSTS',[(price(c),price(c,True),price(c,floor=True),price(c,True,True)) for c in B],'budgets',large,bg)
 print('SOURCE_PRUNING',decide(True),'ALL_CANDIDATES',decide(False));assert decide(True)[1]==('large',2) and decide(False)[1] is None

def stride_adversary(m):
 # Distinct globally positive ID intervals; complete R is x-major/y-minor.
 X=list(range(1,m+1));Y=list(range(100000,100000+m));zs=[200000]+[200000+2*i for i in range(1,m)];zt=[200000]+[200000+2*i+1 for i in range(1,m)]
 pos=[j*m*m//64 for j in range(64)];J={p%m for p in pos};live=[y for j,y in enumerate(Y) if j not in J]
 R=set(product(X,Y));S=set(product(live,zs));T=set(product(zt,X))
 S.update((300000+j,400000+j) for j in range(m*m+1-len(S)))
 T.update((500000+j,600000+j) for j in range(m*m+1-len(T)))
 # Engine execution order is R(x,y),T(z,x),S(y,z), not cyclic relation order.
 E=[R,T,S];shape=[(0,1),(2,0),(1,2)];B=[budgets(E,shape,d) for d in range(3)];V=[budgets(E,shape,d,False) for d in range(3)]
 ns=sum(map(len,E));actual=[c['A'] for c in V];samp=[c['A'] for c in B]
 sy=defaultdict(set);tx=defaultdict(set)
 for y,z in S:sy[y].add(z)
 for z,x in T:tx[x].add(z)
 out=sum(len(sy[y]&tx[x]) for x,y in R)
 assert ns==3*m*m+2 and len(J)==1 and actual==[m*m*(m-1),m*(m-1),m*(m-1)] and out==m*(m-1)
 winner=min(range(3),key=lambda i:(2*B[i]['n']+B[i]['A'],i));assert winner==0
 path=B[0]['R'];assert path==m**3 and B[0]['A']==0
 obj=F(2*m*m+actual[0],min(2*c['n']+c['A'] for c in V))
 print('STRIDE',m,'N',ns,'j',len(J),'M_R_T_S',actual,'hat_M_R_T_S',samp,'Out',out,'walk_lower',m*(m-1)**2,'chosen',winner,'objective_ratio',obj,'gate_max_ratio',F(m+1,2))
reproduce_rescue()
for m in (64,128,256):stride_adversary(m)
