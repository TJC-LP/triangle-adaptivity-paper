"""Independent exact checks for the upper-bound audit; standard library only.

Run: python3 -I proof_exact.py. No solver/verifier code is read or imported.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import prod


def terms():
    answer = []

    def put(name, r, s, den=1):
        answer.append((name, tuple(F(x, den) for x in r + s)))

    def vec(*pairs):
        x = [0] * 4
        for i, v in pairs:
            x[i] += v
        return x

    for i in range(4):
        rest = [j for j in range(4) if j != i]
        for j, k in combinations(rest, 2):
            put(f'A{i}{j}{k}', vec((i, 1)), vec((j, 1), (k, 1)))
        put(f'B{i}', vec((i, 2)), vec(*[(j, 1) for j in rest]), 2)
    for i, j in combinations(range(4), 2):
        rest = [k for k in range(4) if k not in (i, j)]
        put(f'C{i}{j}', vec((i, 1), (j, 1)), vec(*[(k, 1) for k in rest]), 2)
    for i in range(2):
        put(f'D{i}', vec((i, 1), (i+2, 1)), vec())
        put(f'H{i}', vec((i, 2), (i+2, 2)), [1]*4, 4)
    for i in range(4):
        j, k, l = (i+1)%4, (i+2)%4, (i+3)%4
        put(f'E{i}', vec((i, 1), (k, 1)), vec((i, 1), (j, 1), (k, 1)), 2)
        put(f'F{i}', vec((i, 1), (k, 2)), vec((i, 1), (j, 1), (l, 1)), 3)
        put(f'G{i}', vec((j, 1), (k, 1), (l, 1)), vec((i, 1), (j, 1), (l, 1)), 3)
    assert len(answer) == len(set(e for _, e in answer)) == 38
    return answer


TERMS = terms()


def value12(r, s):
    return min(prod(F(x) ** int(12*p) for x, p in zip(r+s, exponents))
               for _, exponents in TERMS)


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def arc_instance(factors):
    """Build coordinates and binary relations from first principles."""
    active = [(frozenset(arc), n) for arc, n in factors if n > 1]
    keys = [[i for i, (arc, _) in enumerate(active) if v in arc] for v in range(4)]
    coords = [list(product(*[range(active[i][1]) for i in kv])) for kv in keys]
    matrices = []
    for v in range(4):
        w = (v+1) % 4
        shared = [(keys[v].index(i), keys[w].index(i)) for i in keys[v] if i in keys[w]]
        matrices.append([[int(all(a[i] == b[j] for i,j in shared)) for b in coords[w]] for a in coords[v]])
    sizes = [sum(map(sum, a)) for a in matrices]
    norms2 = []
    for a in matrices:
        rows, cols = set(map(sum, a)), set(map(sum, zip(*a)))
        assert len(rows) == len(cols) == 1
        # Biregular matrix: constants are singular vectors and the row/column
        # Schur bound gives equality. Thus this is an exact norm certificate.
        norms2.append(next(iter(rows))*next(iter(cols)))
    cycle = multiply(multiply(multiply(matrices[0], matrices[1]), matrices[2]), matrices[3])
    out = sum(cycle[i][i] for i in range(len(cycle)))
    expected_sizes = [prod(n for arc,n in factors if set(arc)&{v,(v+1)%4}) for v in range(4)]
    expected_norms = [prod(n for arc,n in factors if len(set(arc)&{v,(v+1)%4}) == 1) for v in range(4)]
    assert sizes == expected_sizes and norms2 == expected_norms
    assert out == prod(n for _,n in factors)
    assert out**12 == value12(sizes,norms2)
    return sizes,norms2,out


def check_kite(a,b,c,d,p,q,m):
    factors = [([0],a),([1],b),([2],c),([3],d),([1,2],p),([3,0],q),([0,1,2,3],m)]
    r,s,out = arc_instance(factors)
    tight = [name for name,e in TERMS if prod(F(x)**int(12*p) for x,p in zip(r+s,e)) == out**12]
    assert {'C02','H1','G0','G2'} <= set(tight)
    if q == 1:
        assert 'F1' in tight
    print('kite', (a,b,c,d,p,q,m), 'r=',r,'s=',s,'Out=',out,'tight=',','.join(tight))


def sharp_family():
    # On r=(L,t,L,L), s=(t,t,t,L), each term is L^a t^b.
    # For L=t^ell, prove its exponent is >= min(3,(ell+3)/2)
    # for every ell>=1, by affine comparison on [1,3] and [3,infinity).
    print('sharp-family symbolic monomial exponents (power of L, power of t)')
    for name,e in TERMS:
        a = e[0]+e[2]+e[3]+e[7]
        b = e[1]+e[4]+e[5]+e[6]
        assert a+b >= 2 and 3*a+b >= 3 and a >= 0
        print(name, str(a), str(b))
    for t in (F(3,2),F(7,4),F(15,8),F(31,16),F(63,32)):
        threshold = t**3
        smallest_integer_L = -(-threshold.numerator//threshold.denominator)
        for L in (t,t*t,threshold,F(10**6)):
            r,s = [L,t,L,L],[t,t,t,L]
            actual = value12(r,s)
            expected = min(t**36,(L*t**3)**6)
            assert actual == expected
            print('sharp', 't=',t,'L=',L,'U^12=',actual)
        print('threshold',t,'L>=',threshold,'min_integer_L=',smallest_integer_L)
    # Adjacent known norms R,S are sufficient too: force Q to one edge,
    # then its R-neighbor and that neighbor's S-neighbor are each unique.
    for name,e in TERMS:
        a=e[0]+e[1]+e[2]+e[6]
        b=e[3]+e[4]+e[5]+e[7]
        assert a+b >= 2 and 3*a+b >= 3 and a >= 0
    for t in (F(3,2), F(7,4), F(15,8), F(31,16)):
        actual=value12([8,8,8,t],[t,t,8,t])
        assert actual==t**36
        print('adjacent-two-known-norms', 't=',t,'L=8','U^12=',actual,'W=1')


def real_counterexample():
    I = [[F(1),F(0)],[F(0),F(1)]]
    half = [[x/2 for x in row] for row in I]
    mats = [I,half,I,half]
    r=[sum(x*x for row in a for x in row) for a in mats]
    s=[F(1),F(1,4),F(1),F(1,4)]
    c=multiply(multiply(multiply(*mats[:2]),mats[2]),mats[3])
    out=sum(c[i][i] for i in range(2))
    h4=r[1]**2*r[3]**2*prod(s)
    assert out==F(1,2) and h4==F(1,256) and out**4>h4
    print('real-H counterexample: Frobenius^2=',r,'sigma^2=',s,'Out=',out,'Out^4=',out**4,'H^4=',h4)


def degree_counterexamples():
    for m in (2,3,4,7):
        leaves=m*(m-1)
        a=[[int(i==0 or j==0) for j in range(leaves+1)] for i in range(leaves+1)]
        perron=[m]+[1]*leaves
        assert [sum(x*y for x,y in zip(row,perron)) for row in a] == [m*x for x in perron]
        # Positive eigenvector certifies top eigenvalue m. The only other
        # nonzero eigenvalue is -(m-1), so squared operator norm is m^2.
        d=max(map(sum,a))
        print('double-star', 'm=',m,'shape=',len(a),'Delta+Delta-=',d*d,'sigma^2=',m*m)
    for k in (1,2,4,8):
        n=k+k**3
        a=[[0]*n for _ in range(n)]
        for i in range(k):
            for j in range(k):
                a[i][j]=1
            for j in range(k+i*k*k,k+(i+1)*k*k):
                a[i][j]=a[j][i]=1
        d=list(map(sum,a))
        r=sum(d)
        weighted=sum(d[i]*d[j] for i in range(n) for j in range(n) if a[i][j])
        assert r==k*k*(2*k+1) and weighted==k**4*(k+1)*(k+3)
        # Equitable core/leaf eigenproblem gives lambda^2-k lambda-k^2=0;
        # hence sigma^2=k^2(3+sqrt(5))/2<3k^2. Print rational lower bound.
        print('degree-sum', 'k=',k,'r=',r,'weighted=',weighted,
              'sigma^2 polynomial=',(1,-3*k*k,k**4),
              'ratio >', F(weighted,r*3*k*k))


if __name__ == '__main__':
    for args in ((1,1,1,1,2,2,1),(2,3,1,2,2,3,1),(3,2,3,2,3,3,3),(2,1,2,3,2,1,2)):
        check_kite(*args)
    sharp_family()
    real_counterexample()
    degree_counterexamples()
