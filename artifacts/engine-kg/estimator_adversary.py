"""Fixed-stride triangle-driver adversary; standard-library analysis only."""
from collections import Counter


def check(m):
    assert m % 64 == 0
    X = range(100000, 100000 + m)
    Y = range(200000, 200000 + m)
    # Alternating exclusive IDs, with one shared ID, avoid a trivial
    # contiguous disjoint-neighbour-run explanation for large M_R.
    zs = [300000] + [300000 + 2 * i for i in range(1, m)]
    zt = [300000] + [300001 + 2 * i for i in range(1, m)]
    R = sorted((x, y) for x in X for y in Y)
    S = sorted([(y, z) for y in list(Y)[1:] for z in zs]
               + [(200000 + m, 400000 + i) for i in range(m)])
    T = sorted((z, x) for z in zt for x in X)
    r_x, r_y = Counter(x for x, y in R), Counter(y for x, y in R)
    s_y, s_z = Counter(y for y, z in S), Counter(z for y, z in S)
    t_z, t_x = Counter(z for z, x in T), Counter(x for z, x in T)
    # Shape edge order R, T, S: greedy's first join uses R's subject x.
    rows = [R, T, S]
    costs = [lambda row: min(s_y[row[1]], t_x[row[0]]),
             lambda row: min(r_x[row[1]], s_z[row[0]]),
             lambda row: min(t_z[row[1]], r_y[row[0]])]
    exact = [sum(fn(row) for row in rel) for rel, fn in zip(rows, costs)]
    estimated = [len(rel) * sum(fn(rel[s * len(rel) // 64])
                               for s in range(64)) // 64
                 for rel, fn in zip(rows, costs)]
    model = [2 * len(rel) + a for rel, a in zip(rows, estimated)]
    pick = min(range(3), key=model.__getitem__)
    greedy = len(R) + len(R) * sum(t_x[R[s * len(R) // 64][0]]
                                 for s in range(64)) // 64
    assert len(R) == len(S) == len(T) == m * m
    assert exact == [m * m * (m - 1), m * (m - 1), m * (m - 1)]
    assert estimated[0] == 0 and pick == 0 and model[pick] <= greedy
    print(dict(m=m, lengths=[len(r) for r in rows], exact=exact,
               estimated=estimated, pick=pick, accepts=True,
               pick_over_best_M=exact[pick] // min(exact)))


for size in (64, 128, 256):
    check(size)
