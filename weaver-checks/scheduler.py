import sys; sys.path.insert(0, '/workspace/review')
from lib import *
import random

def options(I, v, root):
    """return the two option cost lists (per-edge costs, each >=1) at binding v of the given root"""
    if root == 'x':
        P = [1 + min(I.dSp[y], I.dTm[v]) for y in I.Rx[v]]
        Q = [1 + min(I.dRp[v], I.dSm[z]) for z in I.Tx[v]]
    elif root == 'y':
        P = [1 + min(I.dSp[v], I.dTm[x]) for x in I.Ry[v]]
        Q = [1 + min(I.dRm[v], I.dTp[z]) for z in I.Sy[v]]
    else:
        P = [1 + min(I.dRm[y], I.dTp[v]) for y in I.Sz[v]]
        Q = [1 + min(I.dRp[x], I.dSm[v]) for x in I.Tz[v]]
    return P, Q

def bindings(I, root):
    if root == 'x': return sorted(set(I.Rx) | set(I.Tx), key=repr)
    if root == 'y': return sorted(set(I.Ry) | set(I.Sy), key=repr)
    return sorted(set(I.Sz) | set(I.Tz), key=repr)

class Pass:
    def __init__(self, I, root):
        self.I, self.root = I, root
        self.binds = bindings(I, root); self.idx = 0
        self.L = 0            # sum of c* over finished bindings + current min(tP,tQ)
        self.finished_sum = 0
        self.advances = 0; self.bindings_started = 0
        self.done = len(self.binds) == 0
        self.chosen = []      # recorded option bits (0 = P, 1 = Q)
        self._start()
    def _start(self):
        if self.idx >= len(self.binds):
            self.done = True; return
        self.P, self.Q = options(self.I, self.binds[self.idx], self.root)
        self.iP = self.iQ = 0; self.tP = self.tQ = 0
        self.bindings_started += 1
    def step(self):
        """one scheduler step of this pass: one advance, or finish a binding and start the next"""
        assert not self.done
        # lockstep rule: consider the option with the smaller running sum (ties to P); completed option's sum is its total
        cP = self.iP == len(self.P); cQ = self.iQ == len(self.Q)
        pick = 'P' if self.tP <= self.tQ else 'Q'
        if (pick == 'P' and cP) or (pick == 'Q' and cQ):
            # complete: choose it, finish binding
            total = self.tP if pick == 'P' else self.tQ
            self.chosen.append(0 if pick == 'P' else 1)
            self.finished_sum += total
            self.idx += 1
            self._start()
        else:
            if pick == 'P': self.tP += self.P[self.iP]; self.iP += 1
            else: self.tQ += self.Q[self.iQ]; self.iQ += 1
            self.advances += 1
        cur = 0 if self.done else min(self.tP if self.iP < len(self.P) or True else 0, self.tQ)
        # L_v = finished c* + min(tP, tQ) of current binding
        self.L = self.finished_sum + (0 if self.done else min(self.tP, self.tQ))

def scheduler(I):
    passes = {r: Pass(I, r) for r in 'xyz'}
    order = {'x': 0, 'y': 1, 'z': 2}
    while True:
        key = lambda r: (passes[r].L, 0 if passes[r].done else 1, order[r])
        v = min('xyz', key=key)
        if passes[v].done:
            return v, passes
        passes[v].step()

rng = random.Random(7)
fails = 0; worst_price = 0; worst_rel = 0; n = 0
for trial in range(4000):
    nx, ny, nz = (rng.randint(1, 6) for _ in range(3))
    R = {(('x', i), ('y', j)) for i in range(nx) for j in range(ny) if rng.random() < rng.random()}
    S = {(('y', j), ('z', k)) for j in range(ny) for k in range(nz) if rng.random() < rng.random()}
    T = {(('z', k), ('x', i)) for k in range(nz) for i in range(nx) if rng.random() < rng.random()}
    I = Inst(R, S, T)
    if I.N == 0: continue
    n += 1
    vstar, passes = scheduler(I)
    Cx, Cy, Cz = I.per_root(); C = min(Cx, Cy, Cz); Cv = {'x': Cx, 'y': Cy, 'z': Cz}
    # (1) C_{v*} = C and L_{v*} = C_{v*}
    if Cv[vstar] != C or passes[vstar].L != C:
        fails += 1
        if fails <= 3: print("FAIL (1):", vstar, Cv, C, {r: p.L for r, p in passes.items()})
    # chosen options at v* must have cost exactly c*(u)
    for u, bit in zip(bindings(I, vstar), passes[vstar].chosen):
        P, Q = options(I, u, vstar)
        if (sum(Q) if bit else sum(P)) != min(sum(P), sum(Q)):
            fails += 1; print("FAIL option choice")
    # (3) pricing bound: advances <= min(6C, 2N) + n + O(1); per-edge units: each advance = 1 unit, 3 units per binding started
    adv = sum(p.advances for p in passes.values())
    nb = sum(len(bindings(I, r)) for r in 'xyz')
    if adv > min(6 * C, 2 * I.N) + nb + 3:
        fails += 1
        if fails <= 6: print("FAIL (3):", adv, C, I.N, nb)
    if C > 0: worst_rel = max(worst_rel, (adv + 3 * sum(p.bindings_started for p in passes.values()) - 4 * nb) / C)
print(f"instances: {n}; failures: {fails}; worst (pricing - 4n)/C over random instances: {worst_rel:.2f} (paper: 3.0-3.5 on random, 6 tight)")

# Remark 5.21 tight family: three rotations of complete R=X_p x Y_q, complete T between Z_q and X_p, empty S
for p in (8, 32):
    q = p
    X = [('x', i) for i in range(p)]; Y = [('y', j) for j in range(q)]; Z = [('z', k) for k in range(q)]
    B = Inst([(x, y) for x in X for y in Y], [], [(z, x) for z in Z for x in X])
    U = three_rotations(B)
    vstar, passes = scheduler(U)
    C = U.C(); adv = sum(p_.advances for p_ in passes.values())
    print(f"Remark 5.21 p=q={p}: C={C} (paper p*q per copy... union C={C}), all C_v={U.per_root()}, pricing advances/C = {adv/C:.3f} (paper 7.97 at 8 incl. overhead; limit 6)")

# Remark 5.21 second example: R = X x Y, T complete Z x X (m x m), S one stray tuple (y0, z') with z' fresh. C = 0.
for m in (4, 8, 16, 32):
    X = [('x', i) for i in range(m)]; Y = [('y', j) for j in range(m)]; Z = [('z', k) for k in range(m)]
    I = Inst([(x, y) for x in X for y in Y], [(('y', 0), ('zf', 0))], [(z, x) for z in Z for x in X])
    vstar, passes = scheduler(I)
    adv = sum(p_.advances for p_ in passes.values()); started = sum(p_.bindings_started for p_ in passes.values())
    print(f"stray m={m}: C={I.C()}, v*={vstar}, pricing units (1/advance + 3/binding) = {adv + 3*started} (paper 26, 38, 62, 110 = 3m+14 -> {3*m+14})")
