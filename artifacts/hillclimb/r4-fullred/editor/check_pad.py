import sys; sys.path.insert(0,'.')
exec(open('check_r4.py').read().split("for v in (2,3):")[0])
from fractions import Fraction as F
for v in (2,3):
    pr=(v**5,v**3,v**4,v**2,v,1)
    R,S,T=rot_union([pr,pr,pr])
    for i in range(v**11):
        x=('px',i); y=('py',i); z=('pz',i); R.add((x,y)); S.add((y,z)); T.add((z,x))
    st=stats(R,S,T)
    B2=min(st['fwd'][0]*st['fwd'][1]*st['fwd'][2], st['bwd'][0]*st['bwd'][1]*st['bwd'][2])
    print(v, st['N'], st['C'], st['Out'], st['fwd'], st['bwd'], st['fr'], B2==st['fwd'][0]**3)
