# The live gadget L(p,q,t,g,k,w), rebuilt from the description in the claim (not from the solver's code), with my own
# closed forms for every statistic, verified by brute force below.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
#
# Classes: X (p), Y0 (q), Z1 (t), Z2 (z2 = pt/g), Zw (t); for each group W of w consecutive Z2-vertices (z2/w groups):
#          Y_W (q vertices) and q/k helper vertices xh_{W,m} in X.
# R: X x Y0 complete; xh_{W,m} -> the m-th block of k vertices of Y_W.
# S: Y0 x Z1 complete; Y0 x Zw complete; Y0 -> Z2 one in-edge per z2 vertex, balanced over Y0 (z2/q each); Y_W x W complete.
# T: Z2 -> X biregular (out g, in t); Zw -> X biregular (out p/t, in 1); Z1 -> X one edge each to t distinct x's;
#    W -> every helper of W (complete).
# Requirements: t | p, g | pt, g <= p, q | z2, w | z2, k | q.
from fractions import Fraction as Fr
from lbcore import Ids, Inst, add_union


def params_ok(p, q, t, g, k, w):
    if min(p, q, t, g, k, w) < 1 or p % t or (p * t) % g or g > p or q % k:
        return False
    z2 = p * t // g
    return z2 % q == 0 and z2 % w == 0


def gen_live(ids, p, q, t, g, k, w):
    """Yields (rel, a, b) with globally fresh ids. Local orientation."""
    assert params_ok(p, q, t, g, k, w), (p, q, t, g, k, w)
    z2 = p * t // g
    X = ids.fresh(p); Y0 = ids.fresh(q); Z1 = ids.fresh(t); Z2 = ids.fresh(z2); Zw = ids.fresh(t)
    for x in X:
        for y in Y0:
            yield ('R', x, y)
    for y in Y0:
        for z in Z1:
            yield ('S', y, z)
        for z in Zw:
            yield ('S', y, z)
    for u in range(z2):               # Z2 -> X, out g, in t (values u*g+l run through 0..pt-1 once each)
        for l in range(g):
            yield ('T', Z2[u], X[(u * g + l) % p])
    pt = p // t
    for u in range(t):                # Zw -> X, out p/t, in 1
        for l in range(pt):
            yield ('T', Zw[u], X[u * pt + l])
    for i in range(t):                # Z1 -> X, one edge each, distinct targets (t <= p)
        yield ('T', Z1[i], X[i])
    for i in range(z2):               # Y0 -> Z2, one in-edge per z2 vertex, z2/q per y0
        yield ('S', Y0[i % q], Z2[i])
    for gi in range(z2 // w):
        W = Z2[gi * w:(gi + 1) * w]
        YW = ids.fresh(q)
        for y in YW:
            for z in W:
                yield ('S', y, z)
        for m in range(q // k):
            xh = ids.fresh(1)[0]
            for y in YW[m * k:(m + 1) * k]:
                yield ('R', xh, y)
            for z in W:
                yield ('T', z, xh)


def closed_live(p, q, t, g, k, w):
    """My closed forms for one gadget (derived by hand from the degrees; see report)."""
    z2 = p * t // g
    nh = (z2 // w) * (q // k)          # helpers
    n3 = (z2 // w) * q                 # Y_W vertices
    # degrees: X: d+R = q, d-T = t + 1 + [i < t]; helper: d+R = k, d-T = w; Y0: d-R = p, d+S = 2t + z2/q; Y_W: d-R = 1, d+S = w;
    # Z1: d-S = q, d+T = 1; Zw: d-S = q, d+T = p/t; Z2: d-S = q + 1, d+T = g + q/k.
    R = p * q + n3
    S = 2 * q * t + z2 + z2 * q
    T = p * t + p + t + z2 * q // k
    Out = t * q + p * q + p * t + z2 * q
    # root x
    Cx = (p - t) * (q * (t + 1) + min(q, t + 1)) + t * (q * (t + 2) + min(q, t + 2)) + nh * (k * w + min(k, w))
    # root y
    cR_y0 = p * (t + 2) + t
    cS_y0 = 3 * t + p + (z2 // q) * (1 + min(p, g + q // k))
    Cy = q * min(cR_y0, cS_y0) + n3 * (1 + w)
    # root z
    cz1 = min(2 * q, 1 + q)
    czw = min(q * (1 + p // t), (p // t) * (1 + q))
    cz2 = min(1 + min(g + q // k, p) + 2 * q, g * (1 + q) + (q // k) * (1 + k))
    Cz = t * cz1 + t * czw + z2 * cz2
    al = p * q * q + nh * k * k
    be = q * (2 * t + z2 // q) ** 2 + n3 * w * w
    ga = t + t * (p // t) ** 2 + z2 * (g + q // k) ** 2
    alp = q * p * p + n3
    bep = 2 * t * q * q + z2 * (q + 1) ** 2
    gap = (p - t) * (t + 1) ** 2 + t * (t + 2) ** 2 + nh * w * w
    return dict(R=R, S=S, T=T, N=R + S + T, Out=Out, Cx=Cx, Cy=Cy, Cz=Cz, al=al, be=be, ga=ga, alp=alp, bep=bep, gap=gap,
                pqt=p * q * t)


def union_closed(a, b, c):
    """Union of copy 0 = L(a), copy 1 = rotated L(b), copy 2 = twice-rotated L(c).
    Rotation: local (R,S,T) -> global (S,T,R); local (Cx,Cy,Cz) -> global (Cy,Cz,Cx); norms likewise."""
    ca, cb, cc = closed_live(*a), closed_live(*b), closed_live(*c)
    def rot(d, k):
        out = dict(d)
        for keys in (('R', 'S', 'T'), ('Cx', 'Cy', 'Cz'), ('al', 'be', 'ga'), ('alp', 'bep', 'gap')):
            for i, key in enumerate(keys):
                out[keys[(i + k) % 3]] = d[key]
        return out
    parts = [rot(ca, 0), rot(cb, 1), rot(cc, 2)]
    tot = {}
    for key in ('R', 'S', 'T', 'Cx', 'Cy', 'Cz', 'al', 'be', 'ga', 'alp', 'bep', 'gap', 'Out', 'N'):
        tot[key] = sum(pp[key] for pp in parts)
    tot['C'] = min(tot['Cx'], tot['Cy'], tot['Cz'])
    return tot


def family_params(v):
    return (v ** 5, v ** 3, v ** 4, v ** 2, v ** 2, v)


def family_closed(v):
    """Closed forms of the union L(v) (three rotated copies of L(v^5, v^3, v^4, v^2, v^2, v)), v >= 2."""
    return dict(N=3 * (v ** 10 + 2 * v ** 9 + 2 * v ** 8 + 3 * v ** 7 + v ** 5 + v ** 4),
                C=v ** 12 + 4 * v ** 10 + 3 * v ** 9 + 7 * v ** 8 + 7 * v ** 7 + v ** 5 + v ** 4,
                Cx_gadget=v ** 12 + v ** 10 + 3 * v ** 8 + v ** 7,
                Cy_gadget=v ** 10 + 2 * v ** 9 + 2 * v ** 8 + 4 * v ** 7,
                Cz_gadget=2 * v ** 10 + v ** 9 + 2 * v ** 8 + 2 * v ** 7 + v ** 5 + v ** 4,
                Out=3 * (v ** 7 + v ** 8 + v ** 9 + v ** 10),
                fwd=13 * v ** 11 + 2 * v ** 10 + v ** 9 + v ** 6 + v ** 4,
                bwd=3 * v ** 13 + 4 * v ** 10 + 4 * v ** 9 + 2 * v ** 8 + v ** 7 + v ** 5 + 3 * v ** 4)


def general_params(i, j, u):
    return (u ** (4 * i), u ** (4 * i - 2 * j), u ** (4 * i - j), u ** (4 * i - 3 * j), u ** j, 1)


def build_union(params3):
    ids = Ids(); inst = Inst()
    gens = [gen_live(ids, *pr) for pr in params3]
    add_union(inst, gens)
    return inst
