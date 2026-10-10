from itertools import product
from fractions import Fraction as F
import runpy,random
A=runpy.run_path('triangle_audit_exact.py');stats=A['stats'];block=A['block'];union=A['union']
for s,n in ((2,2),(2,4),(3,5),(3,9),(4,8),(4,16),(5,25),(8,64)):
 G=[]
 for tag in range(3):
  x=(tag,'x');Y=[(tag,'y',i) for i in range(n)];Z=[(tag,'z',i) for i in range(n)]
  G.append([{(x,y) for y in Y},set(zip(Y,Z)),{(z,x) for z in Z}])
 E=union(G);K=block(s,s,s,1);E=[a|b for a,b in zip(E,K)];d=stats(E)
 assert d['N']==3*s*s+9*n and d['out']==s**3+3*n and d['Cs']==[s*s*(s+1)+6*n]*3
 assert d['f']==d['b']==[s**3+n*n+2*n]*3
 # Every tuple supported, checked via neighbor intersections, not just counts.
 for i in range(3):
  for a,b in E[i]:assert any((b,c) in E[(i+1)%3] and (c,a) in E[(i+2)%3] for c,_ in E[(i+2)%3])
 print('FULLY_REDUCED_CLIQUE_FANS',s,n,'N',d['N'],'C',d['C'],'Out',d['out'],'B2',d['f'][0])
rng=random.Random(97531);cnt=0;worst=F(0)
for k in range(10000):
 D=[rng.randrange(1,7) for _ in range(3)];E=[{(a,b) for a in range(D[i]) for b in range(D[(i+1)%3]) if rng.randrange(3)==0} for i in range(3)]
 d=stats(E);N=d['N'];Q=d['Q']
 if Q and Q*Q<=N**5:
  ratio=F(d['C']**4*N,Q*Q);worst=max(worst,ratio);assert ratio<=1296;cnt+=1
print('LOW_SLOPE_DIRECT_C4_N_OVER_Q2',cnt,'qualifying_of_10000','max',worst,'violations',0)
