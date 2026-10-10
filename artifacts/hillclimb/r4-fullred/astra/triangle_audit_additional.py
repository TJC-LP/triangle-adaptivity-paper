from fractions import Fraction as F
from itertools import product,permutations
from math import prod
import runpy,json
A=runpy.run_path('triangle_audit_exact.py')
stats=A['stats'];block=A['block'];u9=A['u9'];u2=A['u2'];dead=A['dead'];deadformula=A['deadformula']
for n in (2,3,5):
 vals=[]
 for h in range(3):
  r=[n**4]*3;s=[n**4]*3;s[h]=n*n;v=u9(r,s)
  o=stats(block(n,n,n,n*n))['out'];assert v[h]==o*o and F(min(x for j,x in enumerate(v) if j!=h),o*o)==n*n
  vals.append(o)
 for i,j in permutations(range(3),2):
  k=3-i-j;r=[n**6]*3;r[i]=n*n;s=[n*n]*3;s[k]=n**4
  v=u9(r,s);ix=3+list(permutations(range(3),2)).index((i,j));
  # choose shape from exact U; no importing solver routines.
  U=n**4;a=max(1,U//r[1]);b=max(1,U//r[2]);c=max(1,U//r[0]);m=min(r[0]//(a*b),r[1]//(b*c),r[2]//(c*a))
  o=stats(block(a,b,c,m))['out'];assert o==U and v[ix]==o*o and min(x for z,x in enumerate(v) if z!=ix)==n*n*o*o
  vals.append(o)
 print('NINE_IRREDUNDANCY',n,vals,'all_unique','deletion_ratio',n)
# Isolated-edge padding: exact matrix block structure is direct; verify cardinality/output/C effects.
count=0
for dims in ((1,1,1),(2,1,3),(2,2,2)):
 E=block(*dims,1);base=stats(E)
 for increments in product(range(4),repeat=3):
  P=[set(e) for e in E]
  for rel,n in enumerate(increments):
   for j in range(n):P[rel].add((('private',rel,'source',j),('private',rel,'target',j)))
  d=stats(P)
  assert d['r']==[x+y for x,y in zip(base['r'],increments)] and d['out']==base['out']
  count+=1
print('EXACT_SIZE_PADDING',count,'violations',0)
# Triangle sharpness with every nonempty known-norm subset: relabel the one-known construction.
for p,q in ((7,5),(41,29),(239,169)):
 t=F(p*p,q*q)
 for P in ((0,),(0,1),(0,2),(0,1,2)):
  r=[t*t,t,t*t];s=[t if 0 in P else r[0],1 if 1 in P else r[1],t if 2 in P else r[2]]
  assert min(u9(r,s))==t**4
 print('KNOWN_NORM_SUBSETS_SHARPNESS','t',t,'U',t*t,'W',1)
# Rational tropical verification of family V; all exponents computed symbolically at sample slopes.
def exps(k):
 return [(k/2,(3*k-2)/4,(6-3*k)/8,(7*k-6)/8),(k-F(1,2),(3-2*k)/4,(6*k-3)/8,(2*k-1)/8),(F(1,2),(2*k-1)/4,(6*k-3)/8,(7-6*k)/8)]
def trop(g):
 p,q,t,h=g
 return {'r':[p+q,max(q+t,p+q+t-h),p+t], 'Cs':[max(p+q+t,p+min(q,t)),q+t,p+q+t-h], 'f':[p+2*q,max(q+2*t,p+q+t-h),p+t+h], 'b':[q+2*p,max(t+2*q,p+t-h+2*q),p+2*t]}
for k in (F(5,6),F(6,7),F(7,8),F(8,9),F(9,10),F(1)):
 G=exps(k);negative=[(i,j,str(v)) for i,g in enumerate(G) for j,v in enumerate(g) if v<0]
 tt=[trop(g) for g in G]
 uu={key:[max(tt[i][key][(j-i)%3] for i in range(3)) for j in range(3)] for key in ('r','Cs','f','b')}
 n=max(uu['r']);c=min(uu['Cs']);kap=min(sum(uu['f']),sum(uu['b']))/3
 print('V_TROPICAL','k',k,'negative_parameters',negative,'N_exponent',n,'C_exponent',c,'B2_exponent',kap,'f',list(map(str,uu['f'])),'b',list(map(str,uu['b'])))
 if not negative:assert n==1 and kap==k and c==(10*k-1)/8
# Exact sums at feasible larger exponents without instantiating astronomical matrices.
for k,D in ((F(6,7),56),(F(7,8),64),(F(9,10),80),(F(1),8)):
 for u in (2,3):
  gg=[tuple(u**int(x*D) for x in g) for g in exps(k)]
  ss=[deadformula(*g) for g in gg]
  uu={key:[sum(ss[i][key][(j-i)%3] for i in range(3)) for j in range(3)] for key in ('r','Cs','f','b')}
  N=sum(uu['r']);C=min(uu['Cs']);Q=min(prod(uu['f']),prod(uu['b']))
  assert C>=u**int(D*(10*k-1)/8) and N<=12*u**D and Q<=64*u**int(3*k*D)
  print('V_EXACT',json.dumps(dict(k=str(k),D=D,u=u,N=N,C=C,B2_cubed=Q)))
# B2 endpoints and high-slope saturation: complete triangle plus three isolated stars.
for n in (2,3,5,8):
 E=block(n,n,n,1)
 for j in range(3):
  E[j].update((('star',j,'center'),('star',j,'leaf',h)) for h in range(n*n))
  E[j].update((('instar',j,'leaf',h),('instar',j,'center')) for h in range(n*n))
 d=stats(E);assert d['N']==9*n*n and d['C']==n*n*(n+1) and d['Q']==(n**4+n**3+n*n)**3
 print('KAPPA2_CEXP3OVER2',n,d)
# Lower endpoint: a single triangle plus an isolated matching of R edges.
for n in (2,3,10,100):
 E=block(1,1,1,1);E[0].update((('p',j),('q',j)) for j in range(n))
 d=stats(E);assert d['N']==n+3 and d['Q']==n+1 and d['C']==2
 print('KAPPA_ONE_THIRD',n,d)
