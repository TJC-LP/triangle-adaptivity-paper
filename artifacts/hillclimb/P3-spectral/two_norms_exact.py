from fractions import Fraction as F
from math import isqrt
from itertools import product


def fsqrt(x):
    return isqrt(x.numerator // x.denominator)


def check(r, p, q):
    r = tuple(map(F, r))
    p, q = F(p), F(q)
    rr, rs, rt = r
    assert 1 <= p <= rr and 1 <= q <= rs
    terms2 = [p*rs*rt, q*rr*rt, (rr*q)**2, (rs*p)**2,
              (rt*p)**2, (rt*q)**2]
    u2 = min(terms2)
    a, b, c = (max(1, fsqrt(u2 / v**2)) for v in (rs, rt, rr))
    mu = min(rr/(a*b), rs/(b*c), rt/(c*a))
    m = mu.numerator // mu.denominator
    out = m*a*b*c
    assert a*b <= p and b*c <= q
    assert m*a*b <= rr and m*b*c <= rs and m*c*a <= rt
    assert out*out <= u2 < 16*out*out
    return u2, (a,b,c,m), out, tuple(terms2)


ints = [F(n) for n in range(1,9)]
halves = list(map(F, [1, F(3,2), 2, F(5,2), 3, 4, 8]))
for name, vals in [('integer_grid', ints), ('rational_grid', halves)]:
    count = 0
    max_gap2 = F(0)
    witness = None
    for rr, rs, rt in product(vals, repeat=3):
        for p in vals:
            if p > rr: continue
            for q in vals:
                if q > rs: continue
                u2, shape, out, _ = check((rr,rs,rt), p,q)
                count += 1
                if u2 / out**2 > max_gap2:
                    max_gap2 = u2/out**2
                    witness = (rr,rs,rt,p,q,shape,out,u2)
    print(name, 'checks=',count, 'max_U2_over_Out2=',max_gap2,
          'witness=', witness)

examples = [((16,16,16),4,16), ((16,16,16),16,4),
            ((2,8,16),2,2), ((8,2,16),2,2),
            ((8,8,2),2,4), ((8,8,2),4,2)]
for r,p,q in examples:
    u2,shape,out,terms = check(r,p,q)
    print('example r=',r, 'p=',p,'q=',q,'terms_squared=',terms,
          'U2=',u2,'shape=',shape,'Out=',out)

pell_p, pell_q = 7,5
for _ in range(5):
    assert pell_p*pell_p - 2*pell_q*pell_q == -1
    t = F(pell_p*pell_p,pell_q*pell_q)
    r = (t*t,t,t*t)
    u2,shape,out,_ = check(r,t,1)
    assert u2 == t**4 and shape == (1,1,1,1) and out == 1
    print('pell p=',pell_p,'q=',pell_q,'t=',t,'U=',t*t,
          'W=',1,'W_over_U=',1/(t*t),'shape=',shape)
    pell_p,pell_q=3*pell_p+4*pell_q,2*pell_p+3*pell_q
