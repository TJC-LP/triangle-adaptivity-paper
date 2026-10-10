"""Step 3: exact certification of Theorem 1 (all 50 dual-vertex monomials, hence U_4) on 0/1 instances.

For each instance: Out and sizes are integers; sigma_e^2 is bracketed in (lo, hi] by Sturm bisection on the exact
characteristic polynomial of the Gram matrix (width <= rowsum / 2^60), or pinned exactly when it is an integer.
Monomial v: certified iff Out^D <= prod r^(lam D) s_lo^(mu D) in exact rationals; violated iff
Out^D > prod r^(lam D) s_hi^(mu D); otherwise undecided (reported).

modes:
  random <seed> <n> <maxdim>       random 0/1 instances (mixed generators), full exact certification
  adv <seed> <n>                   adversarial generators (arc instances + flips, stars, double stars, kites,
                                   Kronecker products, per-vertex tight instances + flips), full exact
  exhaustive2222                   all 65536 instances on dims (2,2,2,2), full exact
  exhaustive <nx> <ny> <nz> <nw>   all instances on the given dims, float pre-screen (numpy) + exact
                                   certification of every instance within 2% of tight on any monomial
"""
import os, sys, json, random, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from v2lib import (arcs, arc_instance, out4, size, stats_brackets, certify_instance, vertex_int_exponents,
                   mono_str, mono_powD, kron, dual_constraint_rows, arc_predicted)

HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, "vertices4.json")))
ALL = [tuple(F(x) for x in v) for v in V["all"]]
KEPT = [tuple(F(x) for x in v) for v in V["kept"]]
VINFO = [vertex_int_exponents(v) for v in ALL]
KEPT_IDX = [i for i, v in enumerate(ALL) if v in KEPT]
A4 = arcs(4)


def rand_mat(rng, a, b):
    kind = rng.random()
    M = [[0] * b for _ in range(a)]
    if kind < 0.25:
        p = rng.uniform(0.1, 1.0)
        for i in range(a):
            for j in range(b):
                if rng.random() < p:
                    M[i][j] = 1
    elif kind < 0.45:  # block union
        kb = rng.randint(1, max(1, min(a, b)))
        ra = [rng.randrange(kb) for _ in range(a)]
        rb = [rng.randrange(kb) for _ in range(b)]
        for i in range(a):
            for j in range(b):
                if ra[i] == rb[j]:
                    M[i][j] = 1
    elif kind < 0.55:
        M = [[1] * b for _ in range(a)]
    elif kind < 0.7:  # double star / spider
        c = rng.randrange(a)
        for j in range(b):
            M[c][j] = 1
        d = rng.randrange(b)
        for i in range(a):
            M[i][d] = 1
        for _ in range(rng.randint(0, 2)):
            M[rng.randrange(a)][rng.randrange(b)] = 1
    elif kind < 0.85:  # near matching
        for i in range(a):
            M[i][rng.randrange(b)] = 1
        if rng.random() < 0.5:
            for j in range(b):
                M[rng.randrange(a)][j] = 1
    else:  # biregular-ish
        d = rng.randint(1, b)
        for i in range(a):
            for j in rng.sample(range(b), d):
                M[i][j] = 1
    return M


def random_instance(rng, maxdim):
    nx, ny, nz, nw = [rng.randint(1, maxdim) for _ in range(4)]
    return (rand_mat(rng, nx, ny), rand_mat(rng, ny, nz), rand_mat(rng, nz, nw), rand_mat(rng, nw, nx))


def flip(rng, mats, nflips):
    mats = [[row[:] for row in M] for M in mats]
    for _ in range(nflips):
        e = rng.randrange(4)
        M = mats[e]
        i, j = rng.randrange(len(M)), rng.randrange(len(M[0]))
        M[i][j] ^= 1
    return tuple(mats)


def adversarial_instance(rng, which):
    if which == 0:  # arc instance + flips
        mult = {a: rng.randint(2, 3) for a in A4 if rng.random() < 0.35}
        mats = arc_instance(mult)
        if max(len(M) * len(M[0]) for M in mats) > 400:
            return None
        return flip(rng, mats, rng.randint(0, 3))
    if which == 1:  # per-vertex tight instance + flips
        v = rng.choice(ALL)
        A_, E_, rows = dual_constraint_rows(4)
        tight = [A4[i] for i, row in enumerate(rows) if sum(F(c) * x for c, x in zip(row, v)) == 1]
        mult = {a: rng.randint(1, 3) for a in tight}
        mats = arc_instance(mult)
        if max(len(M) * len(M[0]) for M in mats) > 400:
            return None
        return flip(rng, mats, rng.randint(0, 2))
    if which == 2:  # Kronecker product of two small random instances
        a = random_instance(rng, 2)
        b = random_instance(rng, 3)
        mats = tuple(kron(x, y) for x, y in zip(a, b))
        if max(len(M) * len(M[0]) for M in mats) > 400:
            return None
        return mats
    if which == 3:  # stars / double stars everywhere with random orientation
        dims = [rng.randint(2, 6) for _ in range(4)]
        shapes = [(dims[0], dims[1]), (dims[1], dims[2]), (dims[2], dims[3]), (dims[3], dims[0])]
        mats = []
        for (a, b) in shapes:
            M = [[0] * b for _ in range(a)]
            for _ in range(rng.randint(1, 2)):
                if rng.random() < 0.5:
                    i = rng.randrange(a)
                    for j in range(b):
                        M[i][j] = 1
                else:
                    j = rng.randrange(b)
                    for i in range(a):
                        M[i][j] = 1
            if rng.random() < 0.5:
                for i in range(a):
                    M[i][rng.randrange(b)] = 1
            mats.append(M)
        return tuple(mats)
    if which == 4:  # kite-like: R, T complete; S, Q block unions
        dims = [rng.randint(1, 5) for _ in range(4)]
        nx, ny, nz, nw = dims
        R = [[1] * ny for _ in range(nx)]
        T = [[1] * nw for _ in range(nz)]
        def blocks(a, b):
            kb = rng.randint(1, max(1, min(a, b)))
            ra = [rng.randrange(kb) for _ in range(a)]
            rb = [rng.randrange(kb) for _ in range(b)]
            return [[1 if ra[i] == rb[j] else 0 for j in range(b)] for i in range(a)]
        return (R, blocks(ny, nz), T, blocks(nw, nx))
    return None


def report(tag, tested, undecided_list, worst, worst_inst, viol):
    print(f"{tag}: {tested} instances with Out>0 certified; violations {viol}; undecided {len(undecided_list)}")
    print(f"   max Out/U_4(r,s_hi) over instances (float display of exact 12th-power ratio): {worst:.6f} at {worst_inst}")
    for u in undecided_list[:10]:
        print("   undecided:", u)


def run_batch(instances, tag, exact_all=True):
    tested = 0
    viol = 0
    und = []
    worst = 0.0
    worst_inst = None
    tight_count = 0
    for mats in instances:
        if mats is None:
            continue
        if any(size(M) == 0 for M in mats):
            continue
        out, r, s_lo, s_hi, st = certify_instance(mats, VINFO)
        if out == 0:
            continue
        tested += 1
        for i, s_ in enumerate(st):
            if s_ == 'VIOLATION':
                viol += 1
                print("VIOLATION", mono_str(ALL[i], 4), "Out", out, "r", r, "s_hi", [str(x) for x in s_hi], mats)
            elif s_ == 'undecided':
                und.append((mono_str(ALL[i], 4), out, r, [str(x) for x in s_lo], [str(x) for x in s_hi], mats))
        # optimistic ratio (Out / U_4 at s_hi), exact comparison via D-th powers, display as float
        best = 0.0
        for i in KEPT_IDX:
            D, lamD, muD = VINFO[i]
            m_hi = mono_powD(r, s_hi, lamD, muD)
            ratio = (F(out) ** D / m_hi)
            rr = float(ratio) ** (1.0 / D)
            best = max(best, rr)
        if best >= 1 - 1e-12:
            tight_count += 1
        if best > worst:
            worst = best
            worst_inst = (r, out)
    report(tag, tested, und, worst, worst_inst, viol)
    print(f"   instances tight (Out = U_4 up to 1e-12): {tight_count}")
    return viol, und


def main():
    mode = sys.argv[1]
    if mode == 'random':
        seed, n, maxdim = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        rng = random.Random(seed)
        viol, und = run_batch((random_instance(rng, maxdim) for _ in range(n)), f"random seed {seed} n {n} maxdim {maxdim}")
        sys.exit(1 if viol else 0)
    if mode == 'adv':
        seed, n = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        viol, und = run_batch((adversarial_instance(rng, i % 5) for i in range(n)), f"adversarial seed {seed} n {n}")
        sys.exit(1 if viol else 0)
    if mode == 'exhaustive2222':
        cells = list(itertools.product([0, 1], repeat=4))
        mats_of = lambda c: [[c[0], c[1]], [c[2], c[3]]]
        allm = [mats_of(c) for c in cells]
        def gen():
            for a in allm:
                for b in allm:
                    for c in allm:
                        for d in allm:
                            yield (a, b, c, d)
        viol, und = run_batch(gen(), "exhaustive dims (2,2,2,2), 65536 instances")
        sys.exit(1 if viol else 0)
    if mode == 'exhaustive':
        import numpy as np
        nx, ny, nz, nw = [int(x) for x in sys.argv[2:6]]
        shapes = [(nx, ny), (ny, nz), (nz, nw), (nw, nx)]
        lists = []
        for (a, b) in shapes:
            L = []
            for bits in itertools.product([0, 1], repeat=a * b):
                M = [list(bits[i * b:(i + 1) * b]) for i in range(a)]
                sz = sum(bits)
                if sz == 0:
                    continue
                s2 = float(np.linalg.norm(np.array(M, dtype=float), 2) ** 2)
                L.append((M, sz, min(s2, sz), np.array(M, dtype=float)))
            lists.append(L)
        # float exponents
        lam = np.array([[float(x) for x in v[:4]] for v in KEPT])
        mu = np.array([[float(x) for x in v[4:]] for v in KEPT])
        total = 0
        screened = []
        maxratio = 0.0
        for (R, rR, sR, Rf) in lists[0]:
            for (S, rS, sS, Sf) in lists[1]:
                RS = Rf @ Sf
                for (T, rT, sT, Tf) in lists[2]:
                    RST = RS @ Tf
                    for (Q, rQ, sQ, Qf) in lists[3]:
                        out = float(np.trace(RST @ Qf))
                        if out == 0:
                            continue
                        total += 1
                        lr = np.log([rR, rS, rT, rQ])
                        ls = np.log([sR, sS, sT, sQ])
                        logm = lam @ lr + mu @ ls
                        ratio = math.exp(math.log(out) - logm.min())
                        maxratio = max(maxratio, ratio)
                        if ratio > 0.98:
                            screened.append((R, S, T, Q))
        print(f"exhaustive dims {(nx, ny, nz, nw)}: {total} instances with Out>0; float max Out/U_4 = {maxratio:.6f}; "
              f"{len(screened)} instances within 2% of tight go to exact certification")
        viol, und = run_batch(iter(screened), f"exhaustive dims {(nx, ny, nz, nw)} exact part")
        sys.exit(1 if viol else 0)


if __name__ == "__main__":
    main()
