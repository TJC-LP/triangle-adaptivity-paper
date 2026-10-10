"""Independent re-implementation of the paper's cost model (Sections 2 and 5).

Instances are three sets of pairs R (x,y), S (y,z), T (z,x) over hashable labels.
All quantities are exact integers (Fractions where needed).
"""
from collections import Counter, defaultdict
from fractions import Fraction
from math import isqrt
import itertools, random


class Inst:
    def __init__(self, R, S, T):
        self.R, self.S, self.T = set(R), set(S), set(T)
        # degrees
        self.dRp = Counter(x for x, y in self.R)   # d_R^+(x)
        self.dRm = Counter(y for x, y in self.R)   # d_R^-(y)
        self.dSp = Counter(y for y, z in self.S)   # d_S^+(y)
        self.dSm = Counter(z for y, z in self.S)   # d_S^-(z)
        self.dTp = Counter(z for z, x in self.T)   # d_T^+(z)
        self.dTm = Counter(x for z, x in self.T)   # d_T^-(x)
        self.Rx = defaultdict(list); self.Ry = defaultdict(list)
        self.Sy = defaultdict(list); self.Sz = defaultdict(list)
        self.Tz = defaultdict(list); self.Tx = defaultdict(list)
        for x, y in self.R: self.Rx[x].append(y); self.Ry[y].append(x)
        for y, z in self.S: self.Sy[y].append(z); self.Sz[z].append(y)
        for z, x in self.T: self.Tz[z].append(x); self.Tx[x].append(z)

    # --- sizes and moments ---
    @property
    def N(self): return len(self.R) + len(self.S) + len(self.T)
    def sizes(self): return len(self.R), len(self.S), len(self.T)
    def moments(self):
        sq = lambda c: sum(v * v for v in c.values())
        return (sq(self.dRp), sq(self.dSp), sq(self.dTp)), (sq(self.dRm), sq(self.dSm), sq(self.dTm))
    def B2_cubed(self):
        (a, b, c), (a2, b2, c2) = self.moments()
        return min(a * b * c, a2 * b2 * c2)

    # --- output ---
    def out(self):
        n = 0
        for x, y in self.R:
            if self.dSp[y] == 0 or self.dTm[x] == 0: continue
            zs = set(self.Sy[y])
            n += sum(1 for z in self.Tx[x] if z in zs)
        return n

    # --- kernel probe work M_pi (Section 2) ---
    def M(self):
        MR = sum(min(self.dSp[y], self.dTm[x]) for x, y in self.R)
        MS = sum(min(self.dTp[z], self.dRm[y]) for y, z in self.S)
        MT = sum(min(self.dRp[x], self.dSm[z]) for z, x in self.T)
        return MR, MS, MT

    # --- per-binding costs (Section 5.1) ---
    def per_root(self):
        # root x: option R walks y in R(x,.), cost 1+min(dS+(y), dT-(x)); option T walks z in T(.,x), 1+min(dR+(x), dS-(z))
        Cx = 0
        for x in set(self.Rx) | set(self.Tx):
            cR = sum(1 + min(self.dSp[y], self.dTm[x]) for y in self.Rx[x])
            cT = sum(1 + min(self.dRp[x], self.dSm[z]) for z in self.Tx[x])
            Cx += min(cR, cT)
        Cy = 0
        for y in set(self.Ry) | set(self.Sy):
            cR = sum(1 + min(self.dSp[y], self.dTm[x]) for x in self.Ry[y])
            cS = sum(1 + min(self.dRm[y], self.dTp[z]) for z in self.Sy[y])
            Cy += min(cR, cS)
        Cz = 0
        for z in set(self.Sz) | set(self.Tz):
            cS = sum(1 + min(self.dRm[y], self.dTp[z]) for y in self.Sz[z])
            cT = sum(1 + min(self.dRp[x], self.dSm[z]) for x in self.Tz[z])
            Cz += min(cS, cT)
        return Cx, Cy, Cz
    def C(self): return min(self.per_root())

    def semijoin_reduced(self):
        for x, y in self.R:
            if self.dTm[x] == 0 or self.dSp[y] == 0: return False
        for y, z in self.S:
            if self.dRm[y] == 0 or self.dTp[z] == 0: return False
        for z, x in self.T:
            if self.dSm[z] == 0 or self.dRp[x] == 0: return False
        return True

    def fully_reduced(self):
        # every tuple lies in a triangle
        inR, inS, inT = set(), set(), set()
        for x, y in self.R:
            zs = set(self.Sy[y])
            for z in self.Tx[x]:
                if z in zs:
                    inR.add((x, y)); inS.add((y, z)); inT.add((z, x))
        return inR == self.R and inS == self.S and inT == self.T


def union(*insts):
    """vertex-disjoint union, tagging labels by component index"""
    R, S, T = [], [], []
    for k, I in enumerate(insts):
        R += [((k, x), (k, y)) for x, y in I.R]
        S += [((k, y), (k, z)) for y, z in I.S]
        T += [((k, z), (k, x)) for z, x in I.T]
    return Inst(R, S, T)


def rotate(I):
    """(R,S,T) on (X,Y,Z) -> (S,T,R) on (Y,Z,X): new R := old S, new S := old T, new T := old R"""
    return Inst(I.S, I.T, I.R)


def three_rotations(I):
    return union(I, rotate(I), rotate(rotate(I)))


def pad(I):
    """Lemma 5.8 padding: for every vertex with a tuple in exactly one of its two relations add a fresh triangle."""
    R, S, T = set(I.R), set(I.S), set(I.T)
    fresh = itertools.count()
    p = 0
    for x in set(I.Rx) | set(I.Tx):
        if (I.dRp[x] > 0) != (I.dTm[x] > 0):
            y2, z2 = ('fy', next(fresh)), ('fz', next(fresh))
            R.add((x, y2)); S.add((y2, z2)); T.add((z2, x)); p += 1
    for y in set(I.Ry) | set(I.Sy):
        if (I.dRm[y] > 0) != (I.dSp[y] > 0):
            x2, z2 = ('fx', next(fresh)), ('fz', next(fresh))
            R.add((x2, y)); S.add((y, z2)); T.add((z2, x2)); p += 1
    for z in set(I.Sz) | set(I.Tz):
        if (I.dSm[z] > 0) != (I.dTp[z] > 0):
            x2, y2 = ('fx', next(fresh)), ('fy', next(fresh))
            R.add((x2, y2)); S.add((y2, z)); T.add((z, x2)); p += 1
    return Inst(R, S, T), p


def icbrt(n):
    """floor cube root"""
    x = int(round(n ** (1 / 3)))
    while x ** 3 > n: x -= 1
    while (x + 1) ** 3 <= n: x += 1
    return x


def biregular(left, right, dl):
    """left -> right block, every left vertex has out-degree dl, every right vertex in-degree |left|*dl/|right| (must divide)."""
    L, Rt = list(left), list(right)
    assert (len(L) * dl) % len(Rt) == 0, (len(L), dl, len(Rt))
    pairs = []
    k = 0
    for l in L:
        for _ in range(dl):
            pairs.append((l, Rt[k % len(Rt)])); k += 1
    assert len(set(pairs)) == len(pairs)
    return pairs
