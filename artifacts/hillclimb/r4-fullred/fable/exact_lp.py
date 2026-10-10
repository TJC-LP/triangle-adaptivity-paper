# Exact rational simplex (dense tableau, Bland's rule, two phases). Written for this verification; no third-party code.
from fractions import Fraction as Fr


def simplex_max(nvars, rows, obj):
    """maximize sum obj[j] x_j subject to rows = list of (coeffs: dict j->coef, sense in '<=','>=','==', rhs), x >= 0.
    Returns (status, value, x) with status in 'optimal', 'infeasible', 'unbounded'."""
    # normalise: every row with rhs >= 0
    norm = []
    for coeffs, sense, rhs in rows:
        rhs = Fr(rhs); coeffs = {j: Fr(v) for j, v in coeffs.items() if v != 0}
        if rhs < 0:
            coeffs = {j: -v for j, v in coeffs.items()}; rhs = -rhs
            sense = {'<=': '>=', '>=': '<=', '==': '=='}[sense]
        norm.append((coeffs, sense, rhs))
    m = len(norm)
    nslack = sum(1 for _, s, _ in norm if s in ('<=', '>='))
    nart = sum(1 for _, s, _ in norm if s in ('>=', '=='))
    ncol = nvars + nslack + nart
    T = [[Fr(0)] * (ncol + 1) for _ in range(m)]
    basis = [None] * m
    si = nvars; ai = nvars + nslack
    art_cols = []
    for i, (coeffs, sense, rhs) in enumerate(norm):
        for j, v in coeffs.items():
            T[i][j] = v
        T[i][ncol] = rhs
        if sense == '<=':
            T[i][si] = Fr(1); basis[i] = si; si += 1
        elif sense == '>=':
            T[i][si] = Fr(-1); si += 1
            T[i][ai] = Fr(1); basis[i] = ai; art_cols.append(ai); ai += 1
        else:
            T[i][ai] = Fr(1); basis[i] = ai; art_cols.append(ai); ai += 1
    art_set = set(art_cols)

    def run(cost, allowed):
        # cost: list of length ncol; returns 'optimal' or 'unbounded'; T, basis updated in place
        # reduced cost row r_j = sum_i cost[B_i] T_ij - cost_j
        while True:
            cb = [cost[b] for b in basis]
            r = [None] * ncol
            enter = None
            for j in range(ncol):
                if j not in allowed:
                    continue
                rj = -cost[j]
                for i in range(m):
                    if T[i][j] != 0 and cb[i] != 0:
                        rj += cb[i] * T[i][j]
                if rj < 0:
                    enter = j; break   # Bland: smallest index
            if enter is None:
                return 'optimal'
            leave = None; best = None
            for i in range(m):
                if T[i][enter] > 0:
                    ratio = T[i][ncol] / T[i][enter]
                    if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                        best = ratio; leave = i
            if leave is None:
                return 'unbounded'
            piv = T[leave][enter]
            rowl = T[leave]
            if piv != 1:
                for j in range(ncol + 1):
                    if rowl[j] != 0:
                        rowl[j] /= piv
            for i in range(m):
                if i != leave and T[i][enter] != 0:
                    f = T[i][enter]; rowi = T[i]
                    for j in range(ncol + 1):
                        if rowl[j] != 0:
                            rowi[j] -= f * rowl[j]
            basis[leave] = enter

    allowed = set(range(ncol))
    if art_cols:
        cost1 = [Fr(0)] * ncol
        for a in art_cols:
            cost1[a] = Fr(-1)
        st = run(cost1, allowed)
        val = sum(cost1[b] * T[i][ncol] for i, b in enumerate(basis))
        if val < 0:
            return 'infeasible', None, None
        # drive artificials out of the basis
        for i in range(m):
            if basis[i] in art_set:
                piv_col = None
                for j in range(ncol):
                    if j not in art_set and T[i][j] != 0:
                        piv_col = j; break
                if piv_col is None:
                    continue  # redundant row (all zeros); leave the artificial basic at level 0 and forbid entering
                piv = T[i][piv_col]; rowl = T[i]
                for j in range(ncol + 1):
                    if rowl[j] != 0:
                        rowl[j] /= piv
                for i2 in range(m):
                    if i2 != i and T[i2][piv_col] != 0:
                        f = T[i2][piv_col]; rowi = T[i2]
                        for j in range(ncol + 1):
                            if rowl[j] != 0:
                                rowi[j] -= f * rowl[j]
                basis[i] = piv_col
        allowed = set(j for j in range(ncol) if j not in art_set)
    cost2 = [Fr(0)] * ncol
    for j, v in obj.items():
        cost2[j] = Fr(v)
    st = run(cost2, allowed)
    if st == 'unbounded':
        return 'unbounded', None, None
    x = [Fr(0)] * nvars
    for i, b in enumerate(basis):
        if b < nvars:
            x[b] = T[i][ncol]
    val = sum(cost2[j] * x[j] for j in range(nvars))
    return 'optimal', val, x


if __name__ == '__main__':
    # tiny self-tests
    # max x + y s.t. x + 2y <= 4, 3x + y <= 6 -> x = 8/5, y = 6/5, value 14/5
    st, v, x = simplex_max(2, [({0: 1, 1: 2}, '<=', 4), ({0: 3, 1: 1}, '<=', 6)], {0: 1, 1: 1})
    assert st == 'optimal' and v == Fr(14, 5) and x == [Fr(8, 5), Fr(6, 5)], (st, v, x)
    # equality and >= rows: max x s.t. x + y == 3, x >= 1, y >= 1 -> 2
    st, v, x = simplex_max(2, [({0: 1, 1: 1}, '==', 3), ({0: 1}, '>=', 1), ({1: 1}, '>=', 1)], {0: 1})
    assert st == 'optimal' and v == 2, (st, v, x)
    # infeasible: x >= 2, x <= 1
    st, v, x = simplex_max(1, [({0: 1}, '>=', 2), ({0: 1}, '<=', 1)], {0: 1})
    assert st == 'infeasible'
    # unbounded
    st, v, x = simplex_max(1, [({0: -1}, '<=', 1)], {0: 1})
    assert st == 'unbounded'
    # degenerate / negative rhs: max -x - y s.t. -x - y <= -1 -> -1
    st, v, x = simplex_max(2, [({0: -1, 1: -1}, '<=', -1)], {0: -1, 1: -1})
    assert st == 'optimal' and v == -1
    print("exact_lp self-tests ok")
