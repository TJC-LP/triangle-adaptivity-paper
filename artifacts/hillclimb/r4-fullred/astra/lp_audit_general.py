from fractions import Fraction as F

def exact(p,q,t,g,k,w):
    assert p%t==0 and p*t%g==0 and g<=p
    z=p*t//g
    assert z%q==0 and z%w==0 and q%k==0
    rr=p*q+z*q//w
    ss=2*q*t+z*(q+1)
    tt=p*t+p+t+z*q//k
    a=p*q*q+z*q*k//w
    b=q*(2*t+z//q)**2+z*q*w
    d=z*(g+q//k)**2+p*p//t+t
    ap=p*p*q+z*q//w
    bp=2*t*q*q+z*(q+1)**2
    dp=(p-t)*(t+1)**2+t*(t+2)**2+z*q*w//k
    cx=(p-t)*(q*(t+1)+min(q,t+1))+t*(q*(t+2)+min(q,t+2))+(z//w)*(q//k)*(k*w+min(k,w))
    cy=q*min(p*(t+2)+t,3*t+p+(z//q)*(1+min(p,g+q//k)))+(z*q//w)*(w+1)
    cz=t*(q+1)+p*q+t*min(q,p//t)+z*min(1+min(p,g+q//k)+2*q,g*(q+1)+(q//k)*(k+1))
    out=p*q+q*t+p*t+z*q
    return {'N':3*(rr+ss+tt),'C':cx+cy+cz,'Out':3*out,'Bf':a+b+d,'Bb':ap+bp+dp,'costs':(cx,cy,cz)}

print('GENERAL FAMILY exact closed-form evaluation')
for i,j,u in [(1,0,2),(2,1,2),(3,2,2),(5,4,2),(5,4,3),(10,7,2)]:
    par=(u**(4*i),u**(4*i-2*j),u**(4*i-j),u**(4*i-3*j),u**j,1)
    e=exact(*par);e['B2']=min(e['Bf'],e['Bb'])
    assert e['C']>=u**(12*i-3*j)
    print((i,j,u),'params',par,'stats',e,'gap',F(e['C'],e['N']+e['B2']))
# Check homogeneous identities that certify LP upper bounds for the whole class.
forms={'c':(1,1,1,0),'a':(1,2,0,0),'b':(0,1,2,0),'d':(1,0,1,1),'r':(2,-1,2,-2),'size':(1,1,1,-1)}
for weights,target in [({'a':5,'b':F(5,2),'d':3,'r':F(3,2)},11),({'size':F(3,8),'a':F(1,4),'b':F(1,8),'d':F(3,8)},1)]:
    got=tuple(sum(F(w)*forms[name][i] for name,w in weights.items()) for i in range(4))
    assert got==tuple(target*x for x in forms['c'])
    print('certificate',weights,'coefficients',got,'=',target,'c')
print('RELAXED SLOPE 1 optimizer has true N exponent',F(10,11),'B exponent',1,'C exponent',F(12,11),'hence actual slope',F(11,10))
print('ISOLATED TRIANGLE padding example')
for v in [2,3,4,5]:
    e=exact(v**5,v**3,v**4,v**2,v,1)
    pad=v**11
    e['N']+=3*pad;e['C']+=2*pad;e['Out']+=pad;e['Bf']+=pad;e['Bb']+=pad
    print(v,'triangles',pad,'stats',e,'ratio',F(e['C'],e['N']+min(e['Bf'],e['Bb'])))

print('RANDOM/GRID COST UPPER BOUNDS')
checked=0
for p in range(1,31):
 for t in range(1,p+1):
  if p%t:continue
  for g in range(1,p+1):
   if p*t%g:continue
   z=p*t//g
   for q in range(1,min(z,12)+1):
    if z%q:continue
    for k in range(1,q+1):
     if q%k:continue
     for w in range(1,min(z,12)+1):
      if z%w:continue
      e=exact(p,q,t,g,k,w);ng=e['N']//3;cx,cy,cz=e['costs']
      assert cx<=p*q*t+3*ng
      assert 2*cy<=3*ng
      assert cz<=2*ng
      checked+=1
print('checked',checked,'valid tuples, zero violations')
