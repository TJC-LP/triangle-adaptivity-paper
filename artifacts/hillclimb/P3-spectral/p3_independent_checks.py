"""Independent exact checks for the two-known-norms spectral triangle bound.

Run: python3 -I p3_independent_checks.py
No floating-point arithmetic, eigensolver, or repository imports.
"""
from fractions import Fraction as F
from itertools import product


def norm_squared_le(a, p):
    # p I - A A^t is positive semidefinite iff its principal minors are >=0.
    d0 = sum(x*x for x in a[0])
    d1 = sum(x*x for x in a[1])
    off = sum(x*y for x, y in zip(a[0], a[1]))
    return p >= d0 and p >= d1 and (p-d0)*(p-d1) >= off*off


def terms_squared(r, p, q):
    x, y, z = r
    return (p*y*z, q*x*z, (x*q)**2, (y*p)**2,
            (z*p)**2, (z*q)**2)


def evaluate(R, S, T):
    out = sum(1 for x, y in R for yy, z in S
              if y == yy and (z, x) in T)
    ds, dt = {}, {}
    for y, z in S:
        ds[y] = ds.get(y, 0) + 1
    for z, x in T:
        dt[x] = dt.get(x, 0) + 1
    mr = sum(min(ds.get(y, 0), dt.get(x, 0)) for x, y in R)
    dr, dtout = {}, {}
    for x, y in R:
        dr[y] = dr.get(y, 0) + 1
    for z, x in T:
        dtout[z] = dtout.get(z, 0) + 1
    ms = sum(min(dr.get(y, 0), dtout.get(z, 0)) for y, z in S)
    return out, mr, ms


def small_matrices():
    mats = [((v[0], v[1]), (v[2], v[3])) for v in product((0,1), repeat=4)]
    rels = [{(i,j) for i in range(2) for j in range(2) if a[i][j]} for a in mats]
    budgets = tuple(map(F, (0, 1, F(3,2), 2, F(5,2), 3, 4)))
    valid = [[p for p in budgets if norm_squared_le(a,p)] for a in mats]
    count = positive = 0
    max_out_ratio = max_probe_ratio = F(0)
    for ir, iss, it in product(range(16), repeat=3):
        R, S, T = rels[ir], rels[iss], rels[it]
        r = tuple(map(len, (R,S,T)))
        out, mr, ms = evaluate(R,S,T)
        for pp, qq in product(valid[ir], valid[iss]):
            p, q = min(pp, r[0]), min(qq, r[1])
            v = terms_squared(r,p,q)
            k = min(v)
            assert out*out <= k
            assert min(mr,ms)**2 <= k
            assert mr*mr <= min(v[0],v[2],v[3],v[4])
            assert ms*ms <= min(v[1],v[2],v[3],v[5])
            count += 1
            if k:
                positive += 1
                max_out_ratio = max(max_out_ratio,F(out*out,k))
                max_probe_ratio = max(max_probe_ratio,F(min(mr,ms)**2,k))
    print('matrix_triples=',16**3,'feasible_budget_cases=',count,
          'positive_U_cases=',positive,'failures=',0)
    print('max_Out_squared_over_U_squared=',max_out_ratio,
          'max_min_MR_MS_squared_over_U_squared=',max_probe_ratio)


def block(a,b,c,m):
    R = {((h,x),(h,y)) for h in range(m) for x in range(a) for y in range(b)}
    S = {((h,y),(h,z)) for h in range(m) for y in range(b) for z in range(c)}
    T = {((h,z),(h,x)) for h in range(m) for z in range(c) for x in range(a)}
    return R,S,T


def regimes():
    # These rows follow the order of the six monomials.
    rows = [((16,16,16),4,16,(2,2,2,4)),
            ((16,16,16),16,4,(2,2,2,4)),
            ((2,8,16),2,2,(1,1,2,2)),
            ((8,2,16),2,2,(2,1,1,2)),
            ((8,8,2),2,4,(1,2,1,2)),
            ((8,8,2),4,2,(1,2,1,2))]
    for j,(r,p,q,shape) in enumerate(rows):
        R,S,T=block(*shape)
        out,mr,ms=evaluate(R,S,T)
        v=terms_squared(r,p,q)
        assert v[j] < min(v[i] for i in range(6) if i != j)
        assert out*out == v[j]
        a,b,c,m=shape
        assert a*b<=p and b*c<=q
        assert all(len(e)<=budget for e,budget in zip((R,S,T),r))
        print('regime=',j+1,'r=',r,'p_q=',(p,q),
              'shape=',shape,'actual_sizes=',tuple(map(len,(R,S,T))),
              'actual_norms_squared=',(a*b,b*c,c*a),
              'terms_squared=',v,'Out_MR_MS=',(out,mr,ms))


def asymptotic_regimes():
    count = 0
    for n in (2,3,7,16):
        rows = [((n**4,n**4,n**4),n**2,n**4,(n,n,n,n**2)),
                ((n**4,n**4,n**4),n**4,n**2,(n,n,n,n**2)),
                ((n**2,n**6,n**6),n**2,n**2,(1,1,n**2,n**2)),
                ((n**6,n**2,n**6),n**2,n**2,(n**2,1,1,n**2)),
                ((n**6,n**6,n**2),n**2,n**4,(1,n**2,1,n**2)),
                ((n**6,n**6,n**2),n**4,n**2,(1,n**2,1,n**2))]
        outputs, ratios = [], []
        for j,(r,p,q,(a,b,c,m)) in enumerate(rows):
            ts = terms_squared(r,p,q)
            out = m*a*b*c
            assert a*b <= p and b*c <= q
            assert all(s<=t for s,t in zip((m*a*b,m*b*c,m*c*a),r))
            assert ts[j] == out*out
            ratio = F(min(t for i,t in enumerate(ts) if i!=j),out*out)
            assert ratio == n*n
            outputs.append(out)
            ratios.append(ratio)
            count += 1
        print('irredundancy_n=',n,'six_outputs=',tuple(outputs),
              'squared_deletion_ratios=',tuple(ratios))
    print('irredundancy_cases=',count,'failures=',0)


small_matrices()
regimes()
asymptotic_regimes()
