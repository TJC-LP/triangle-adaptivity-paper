# Independent exact evaluator for the per-binding cost model of spectral_agm.typ (Sec. 2 cost model, Sec. 5 definitions).
# Written from the paper's definitions only; does not import anything from the solver's directory.
#   R subset X x Y (tuples (x,y)), S subset Y x Z (tuples (y,z)), T subset Z x X (tuples (z,x)).
#   root x: option R walks y in R(x,.) at 1 + min(d+S(y), d-T(x)); option T walks z in T(.,x) at 1 + min(d+R(x), d-S(z)).
#   root y: option R walks x in R(.,y) at 1 + min(d+S(y), d-T(x)); option S walks z in S(y,.) at 1 + min(d-R(y), d+T(z)).
#   root z: option S walks y in S(.,z) at 1 + min(d-R(y), d+T(z)); option T walks x in T(z,.) at 1 + min(d+R(x), d-S(z)).
#   C_v = sum over bindings of the smaller option; C = min(C_x, C_y, C_z).
#   alpha, beta, gamma = sum of squared out-degrees of R, S, T; alpha', beta', gamma' = squared in-degrees.
#   B2 = min(alpha beta gamma, alpha' beta' gamma')^(1/3).  Out = number of triangles.
#   fully reduced = every tuple of R, S, T lies in a triangle.
from fractions import Fraction


class Ids:
    """Globally unique integer vertex ids (never reused across classes or copies)."""
    def __init__(self):
        self.n = 0

    def fresh(self, k):
        r = list(range(self.n, self.n + k))
        self.n += k
        return r


class Inst:
    def __init__(self):
        self.Rout = {}; self.Rin = {}; self.Sout = {}; self.Sin = {}; self.Tout = {}; self.Tin = {}
        self.adds = 0

    @staticmethod
    def _add(d, a, b):
        s = d.get(a)
        if s is None:
            d[a] = {b}
        else:
            s.add(b)

    def addR(self, x, y):
        self.adds += 1; self._add(self.Rout, x, y); self._add(self.Rin, y, x)

    def addS(self, y, z):
        self.adds += 1; self._add(self.Sout, y, z); self._add(self.Sin, z, y)

    def addT(self, z, x):
        self.adds += 1; self._add(self.Tout, z, x); self._add(self.Tin, x, z)

    def add(self, rel, a, b):
        if rel == 'R':
            self.addR(a, b)
        elif rel == 'S':
            self.addS(a, b)
        else:
            self.addT(a, b)

    def evaluate(self, full=True):
        Rout, Rin, Sout, Sin, Tout, Tin = self.Rout, self.Rin, self.Sout, self.Sin, self.Tout, self.Tin
        dRo = {k: len(v) for k, v in Rout.items()}; dRi = {k: len(v) for k, v in Rin.items()}
        dSo = {k: len(v) for k, v in Sout.items()}; dSi = {k: len(v) for k, v in Sin.items()}
        dTo = {k: len(v) for k, v in Tout.items()}; dTi = {k: len(v) for k, v in Tin.items()}
        nR = sum(dRo.values()); nS = sum(dSo.values()); nT = sum(dTo.values())
        assert nR == sum(dRi.values()) and nS == sum(dSi.values()) and nT == sum(dTi.values())
        sq = lambda d: sum(v * v for v in d.values())
        al, be, ga, alp, bep, gap = sq(dRo), sq(dSo), sq(dTo), sq(dRi), sq(dSi), sq(dTi)
        E = ()
        Cx = Cy = Cz = 0
        MR = MS = MT = 0
        for x in set(dRo) | set(dTi):
            dr = dRo.get(x, 0); dt = dTi.get(x, 0)
            cR = sum(1 + min(dSo.get(y, 0), dt) for y in Rout.get(x, E))
            cT = sum(1 + min(dr, dSi.get(z, 0)) for z in Tin.get(x, E))
            Cx += min(cR, cT)
            MR += cR - dr  # sum over R-tuples at x of min(d+S(y), d-T(x))
        for y in set(dRi) | set(dSo):
            ds = dSo.get(y, 0); dr = dRi.get(y, 0)
            cR = sum(1 + min(ds, dTi.get(x, 0)) for x in Rin.get(y, E))
            cS = sum(1 + min(dr, dTo.get(z, 0)) for z in Sout.get(y, E))
            Cy += min(cR, cS)
            MS += cS - ds
        for z in set(dSi) | set(dTo):
            dt = dTo.get(z, 0); ds = dSi.get(z, 0)
            cS = sum(1 + min(dRi.get(y, 0), dt) for y in Sin.get(z, E))
            cT = sum(1 + min(dRo.get(x, 0), ds) for x in Tout.get(z, E))
            Cz += min(cS, cT)
            MT += cT - dt
        res = dict(R=nR, S=nS, T=nT, N=nR + nS + nT, al=al, be=be, ga=ga, alp=alp, bep=bep, gap=gap,
                   Cx=Cx, Cy=Cy, Cz=Cz, C=min(Cx, Cy, Cz), MR=MR, MS=MS, MT=MT, adds=self.adds,
                   nx=len(set(dRo) | set(dTi)), ny=len(set(dRi) | set(dSo)), nz=len(set(dSi) | set(dTo)))
        if full:
            out = 0; deadR = deadS = deadT = 0
            for x, ys in Rout.items():
                tin = Tin.get(x)
                if not tin:
                    deadR += len(ys); continue
                for y in ys:
                    so = Sout.get(y)
                    if not so:
                        deadR += 1; continue
                    c = len(so & tin)
                    if c == 0:
                        deadR += 1
                    out += c
            for y, zs in Sout.items():
                rin = Rin.get(y)
                if not rin:
                    deadS += len(zs); continue
                for z in zs:
                    to = Tout.get(z)
                    if not to or rin.isdisjoint(to):
                        deadS += 1
            for z, xs in Tout.items():
                sin = Sin.get(z)
                if not sin:
                    deadT += len(xs); continue
                for x in xs:
                    ro = Rout.get(x)
                    if not ro or sin.isdisjoint(ro):
                        deadT += 1
            res.update(Out=out, deadR=deadR, deadS=deadS, deadT=deadT, fully_reduced=(deadR == deadS == deadT == 0))
        return res


def icbrt_floor(n):
    assert n >= 0
    if n < 2:
        return n
    c = 1 << ((n.bit_length() + 2) // 3)
    while c * c * c > n:
        c = (2 * c + n // (c * c)) // 3
    while (c + 1) ** 3 <= n:
        c += 1
    while c ** 3 > n:
        c -= 1
    return c


def b2_bracket(e):
    """Exact integer bracket [lo, hi] with lo^3 <= min(L2, L2') <= hi^3; lo == hi iff B2 is an integer."""
    m = min(e['al'] * e['be'] * e['ga'], e['alp'] * e['bep'] * e['gap'])
    lo = icbrt_floor(m)
    hi = lo if lo ** 3 == m else lo + 1
    return lo, hi, m


def ratio_bracket(e):
    """Exact rational bracket for C/(N + B2): [C/(N+hi), C/(N+lo)]."""
    lo, hi, _ = b2_bracket(e)
    return Fraction(e['C'], e['N'] + hi), Fraction(e['C'], e['N'] + lo)


def rotate_rel(rel, k):
    """Global relation name of a copy's local relation under the paper's rotation applied k times:
    rotating once relabels (R,S,T) on (X,Y,Z) as (S,T,R) on (Y,Z,X): local R -> global S, S -> T, T -> R."""
    order = 'RST'
    return order[(order.index(rel) + k) % 3]


def add_union(inst, gens):
    """gens: list of three generators of (rel, a, b) tuples (local orientation, globally fresh ids).
    Copy k is rotated k times, so copy 0's root x, copy 1's root x and copy 2's root x become the union's x, y, z."""
    for k, gen in enumerate(gens):
        for rel, a, b in gen:
            inst.add(rotate_rel(rel, k), a, b)
    return inst


def fmt(e):
    lo, hi, _ = b2_bracket(e)
    r0, r1 = ratio_bracket(e)
    b2s = str(lo) if lo == hi else f"({lo},{hi}]"
    return (f"N={e['N']} (|R|,|S|,|T|)=({e['R']},{e['S']},{e['T']}) C={e['C']} (Cx,Cy,Cz)=({e['Cx']},{e['Cy']},{e['Cz']}) "
            f"Out={e.get('Out')} fully_reduced={e.get('fully_reduced')} dead=({e.get('deadR')},{e.get('deadS')},{e.get('deadT')}) "
            f"fwd=({e['al']},{e['be']},{e['ga']}) bwd=({e['alp']},{e['bep']},{e['gap']}) B2={b2s} "
            f"C/(N+B2)={float(r0):.6f}" + ("" if r0 == r1 else f"..{float(r1):.6f}"))
