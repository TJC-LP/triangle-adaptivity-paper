# Brute-force tests of the upper-bound side on random and adversarial small instances:
#   (U1) thm-pb-upper integer form: (C - N)_+^8 <= |R||S||T| min(abc, a'b'c')^2  (source of the 1/8 cap via cor-pb(1))
#   (U2) cyclic l2 bound: Out^3 <= min(abc, a'b'c')  (Out <= B2)
#   (U3) fully reduced => Out >= max(|R|,|S|,|T|) >= N/3 (so B2 >= N/3: no slope < 1)
#   (U4) every root cost C_v >= Out; and the per-root forms of lem-perroot (eighth powers, exact integers)
# plus a hill-climb over small fully reduced instances maximising C/(N+B2) (exact rationals), to see what small instances reach.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import random, itertools, sys
from fractions import Fraction as Fr
from lbcore import Inst, b2_bracket, ratio_bracket, fmt

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
n_inst = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
rng = random.Random(seed)


def rand_instance(nx, ny, nz, pr, ps, pt, mode):
    inst = Inst()
    if mode == 'uniform':
        for x in range(nx):
            for y in range(ny):
                if rng.random() < pr: inst.addR(x, y)
        for y in range(ny):
            for z in range(nz):
                if rng.random() < ps: inst.addS(y, z)
        for z in range(nz):
            for x in range(nx):
                if rng.random() < pt: inst.addT(z, x)
    elif mode == 'skew':   # heavy hubs: a few vertices of very high degree
        hx = rng.sample(range(nx), max(1, nx // 4)); hy = rng.sample(range(ny), max(1, ny // 4)); hz = rng.sample(range(nz), max(1, nz // 4))
        for x in range(nx):
            for y in range(ny):
                p = pr * (4 if (x in hx or y in hy) else 0.3)
                if rng.random() < p: inst.addR(x, y)
        for y in range(ny):
            for z in range(nz):
                p = ps * (4 if (y in hy or z in hz) else 0.3)
                if rng.random() < p: inst.addS(y, z)
        for z in range(nz):
            for x in range(nx):
                p = pt * (4 if (z in hz or x in hx) else 0.3)
                if rng.random() < p: inst.addT(z, x)
    elif mode == 'blocks':  # union of random complete blocks plus noise
        for _ in range(rng.randint(1, 4)):
            xs = rng.sample(range(nx), rng.randint(1, nx)); ys = rng.sample(range(ny), rng.randint(1, ny)); zs = rng.sample(range(nz), rng.randint(1, nz))
            which = rng.sample(['R', 'S', 'T'], rng.randint(1, 3))
            if 'R' in which:
                for x in xs:
                    for y in ys: inst.addR(x, y)
            if 'S' in which:
                for y in ys:
                    for z in zs: inst.addS(y, z)
            if 'T' in which:
                for z in zs:
                    for x in xs: inst.addT(z, x)
        for _ in range(rng.randint(0, 5)):
            inst.add(rng.choice('RST'), rng.randrange(max(nx, ny, nz)), rng.randrange(max(nx, ny, nz)))
    return inst


def make_fully_reduced(inst):
    """Drop dead tuples repeatedly until every remaining tuple lies in a triangle (semijoin fixpoint on triangles)."""
    while True:
        R = [(x, y) for x, ys in inst.Rout.items() for y in ys]
        S = [(y, z) for y, zs in inst.Sout.items() for z in zs]
        T = [(z, x) for z, xs in inst.Tout.items() for x in xs]
        keepR = [(x, y) for (x, y) in R if not inst.Sout.get(y, set()).isdisjoint(inst.Tin.get(x, set()))]
        keepS = [(y, z) for (y, z) in S if not inst.Rin.get(y, set()).isdisjoint(inst.Tout.get(z, set()))]
        keepT = [(z, x) for (z, x) in T if not inst.Rout.get(x, set()).isdisjoint(inst.Sin.get(z, set()))]
        if len(keepR) == len(R) and len(keepS) == len(S) and len(keepT) == len(T):
            return inst
        new = Inst()
        for x, y in keepR: new.addR(x, y)
        for y, z in keepS: new.addS(y, z)
        for z, x in keepT: new.addT(z, x)
        inst = new


def check(e, tag):
    N, C = e['N'], e['C']
    L2 = e['al'] * e['be'] * e['ga']; L2p = e['alp'] * e['bep'] * e['gap']; mn = min(L2, L2p)
    lhs = max(C - N, 0) ** 8; rhs = e['R'] * e['S'] * e['T'] * mn * mn
    assert lhs <= rhs, ('U1 thm-pb-upper violated', tag, e)
    assert e['Out'] ** 3 <= mn, ('U2 Out <= B2 violated', tag, e)
    assert e['Cx'] >= e['Out'] and e['Cy'] >= e['Out'] and e['Cz'] >= e['Out'], ('U4', tag, e)
    # per-root forms of lem-perroot, eighth powers: (C_x - |R| - |T|)_+^8 <= |S|^3 a^2 b c^3 and primed
    a, b, c = e['al'], e['be'], e['ga']; ap, bp, cp = e['alp'], e['bep'], e['gap']
    R, S, T = e['R'], e['S'], e['T']
    assert max(e['Cx'] - R - T, 0) ** 8 <= S ** 3 * a ** 2 * b * c ** 3, ('perroot x', tag, e)
    assert max(e['Cx'] - R - T, 0) ** 8 <= S ** 3 * cp ** 2 * bp * ap ** 3, ('perroot x primed', tag, e)
    assert max(e['Cy'] - R - S, 0) ** 8 <= T ** 3 * b ** 2 * c * a ** 3, ('perroot y', tag, e)
    assert max(e['Cz'] - S - T, 0) ** 8 <= R ** 3 * c ** 2 * a * b ** 3, ('perroot z', tag, e)
    if e['fully_reduced'] and N > 0:
        assert e['Out'] >= max(R, S, T), ('U3', tag, e)
        assert 3 * e['Out'] >= N
    ratio = Fr(lhs, rhs) if rhs else Fr(0)
    return ratio


worst = {'U1': Fr(0), 'U2': Fr(0)}
best_fr = None; cnt = 0; cnt_fr = 0
for it in range(n_inst):
    nx, ny, nz = (rng.randint(1, 7) for _ in range(3))
    pr, ps, pt = (rng.choice([0.1, 0.3, 0.5, 0.8, 1.0]) for _ in range(3))
    mode = rng.choice(['uniform', 'uniform', 'skew', 'blocks'])
    inst = rand_instance(nx, ny, nz, pr, ps, pt, mode)
    e = inst.evaluate()
    if e['N'] == 0:
        continue
    r = check(e, (it, 'raw')); worst['U1'] = max(worst['U1'], r)
    mn = min(e['al'] * e['be'] * e['ga'], e['alp'] * e['bep'] * e['gap'])
    if mn:
        worst['U2'] = max(worst['U2'], Fr(e['Out'] ** 3, mn))
    cnt += 1
    fr = make_fully_reduced(inst); ef = fr.evaluate()
    if ef['N'] == 0:
        continue
    assert ef['fully_reduced']
    check(ef, (it, 'reduced')); cnt_fr += 1
    lo, hi = ratio_bracket(ef)
    if best_fr is None or lo > best_fr[0]:
        best_fr = (lo, ef)
print(f"seed {seed}: {cnt} random instances (uniform/skew/blocks, sides <= 7) and {cnt_fr} fully reduced reductions: U1 (thm-pb-upper), U2 (Out <= B2), U3, U4, per-root forms all hold")
print(f"  worst (C-N)_+^8 / (|R||S||T| min(...)^2) = {float(worst['U1']):.4g}; worst Out^3 / min(abc, a'b'c') = {float(worst['U2']):.4g}")
print(f"  best fully reduced C/(N+B2) among reductions: {float(best_fr[0]):.4f}: {fmt(best_fr[1])}")

# adversarial structured families, small: complete K_{a,b,c}, matchings, stars, double stars, G8-like, I_v-like via reduction
print("structured small instances:")
for (a, b, c) in ((1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4), (2, 5, 1), (1, 6, 6), (6, 1, 6)):
    inst = Inst()
    for x in range(a):
        for y in range(b): inst.addR(x, y)
    for y in range(b):
        for z in range(c): inst.addS(y, z)
    for z in range(c):
        for x in range(a): inst.addT(z, x)
    e = inst.evaluate(); check(e, ('K', a, b, c))
    lo, hi = ratio_bracket(e)
    print(f"  K_({a},{b},{c}): C={e['C']} N={e['N']} Out={e['Out']} B2 in [{b2_bracket(e)[0]},{b2_bracket(e)[1]}] C/(N+B2) ~ {float(lo):.4f} fully_reduced={e['fully_reduced']}")

# hill climb over fully reduced instances on sides <= 5 maximising C/(N+B2) (exact rational objective)
def climb(nx, ny, nz, steps):
    inst = rand_instance(nx, ny, nz, 0.5, 0.5, 0.5, 'uniform')
    inst = make_fully_reduced(inst); e = inst.evaluate()
    cur = ratio_bracket(e)[0] if e['N'] else Fr(0)
    tuples = lambda i: ([('R', x, y) for x, ys in i.Rout.items() for y in ys] + [('S', y, z) for y, zs in i.Sout.items() for z in zs] + [('T', z, x) for z, xs in i.Tout.items() for x in xs])
    for _ in range(steps):
        cand = Inst()
        for rel, p, q in tuples(inst):
            cand.add(rel, p, q)
        for _ in range(rng.randint(1, 3)):
            rel = rng.choice('RST')
            dom = {'R': (nx, ny), 'S': (ny, nz), 'T': (nz, nx)}[rel]
            cand.add(rel, rng.randrange(dom[0]), rng.randrange(dom[1]))
        cand = make_fully_reduced(cand); ec = cand.evaluate()
        if ec['N'] == 0:
            continue
        check(ec, 'climb')
        v = ratio_bracket(ec)[0]
        if v >= cur:
            inst, cur, e = cand, v, ec
    return cur, e

best = None
for trial in range(12):
    nx, ny, nz = (rng.randint(2, 5) for _ in range(3))
    cur, e = climb(nx, ny, nz, 150)
    if best is None or cur > best[0]:
        best = (cur, e)
print(f"hill climb (fully reduced, sides <= 5): best C/(N+B2) = {float(best[0]):.4f}: {fmt(best[1])}")
