import runpy
from itertools import product
A=runpy.run_path('triangle_audit_exact.py');stats=A['stats'];dead=A['dead'];union=A['union']
for m in (2,3,4):
 E=dead(m**4,m*m,m**3,m,0)
 for j in range(m**8):E[2].add(((0,'z0',j),(0,'x',j%(m**4))))
 d=stats(E);assert d['Cs']==[m**9+m**6,m**5,m**8] and d['N']==2*m**8+m**7+m**6+m**5
 print('G8_SINGLE',m,d)
for m in (2,3,4):
 G=[]
 for tag in range(3):
  X=[(tag,'x',i) for i in range(m**3)];Y=[(tag,'y',i) for i in range(m)];Z=[(tag,'z',i) for i in range(m*m)]
  G.append([set(product(X,Y)),set(product(Y,Z)),{((tag,'zz',i,j),X[i]) for i in range(m**3) for j in range(m*m)}])
 E=union(G);out=[{a for a,b in E[i]} for i in range(3)];inc=[{b for a,b in E[(i-1)%3]} for i in range(3)]
 for i in range(3):
  for v in out[i]^inc[i]:
   verts=[('helper',i,v,j) if j!=i else v for j in range(3)]
   for j in range(3):E[j].add((verts[j],verts[(j+1)%3]))
 d=stats(E)
 for i in range(3):assert {a for a,b in E[i]}=={b for a,b in E[(i-1)%3]}
 assert d['N']==12*m**5+3*m**4+3*m**3+9*m*m
 assert d['f']==[8*m**5+3*m*m]*3 and d['Q']==(8*m**5+3*m*m)**3
 print('PADDED_GMIN',m,d)
