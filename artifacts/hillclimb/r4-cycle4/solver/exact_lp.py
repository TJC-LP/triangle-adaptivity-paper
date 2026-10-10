"""Tiny exact (Fraction) LP solver: two-phase simplex with Bland's rule.

solve_lp(c, A_ub, b_ub, A_eq, b_eq, bounds) -> (status, x, value)
  minimize c.x  s.t.  A_ub x <= b_ub,  A_eq x == b_eq,  lo_i <= x_i <= hi_i
  (lo may be None = -inf, hi may be None = +inf).
status: 'optimal' | 'infeasible' | 'unbounded'.
Only meant for small problems (tens of variables / constraints).
"""
from fractions import Fraction

F = Fraction


def _simplex(T, basis, nvar):
    """Run primal simplex on tableau T (list of rows, last column = rhs, last row = objective row
    in the form  z - c x = 0  with reduced costs).  Bland's rule.  Returns 'optimal' or 'unbounded'."""
    m = len(T) - 1
    while True:
        # entering: smallest index with negative reduced cost
        obj = T[m]
        enter = None
        for j in range(nvar):
            if obj[j] < 0:
                enter = j
                break
        if enter is None:
            return 'optimal'
        # ratio test (Bland: smallest basis index among ties)
        best = None
        for i in range(m):
            a = T[i][enter]
            if a > 0:
                ratio = T[i][-1] / a
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None:
            return 'unbounded'
        i = best[1]
        piv = T[i][enter]
        T[i] = [v / piv for v in T[i]]
        for r in range(m + 1):
            if r != i and T[r][enter] != 0:
                f = T[r][enter]
                T[r] = [a - f * b for a, b in zip(T[r], T[i])]
        basis[i] = enter


def solve_lp(c, A_ub=(), b_ub=(), A_eq=(), b_eq=(), bounds=None):
    c = [F(v) for v in c]
    n = len(c)
    if bounds is None:
        bounds = [(F(0), None)] * n
    # variable substitution to get x >= 0:  x_i = lo + y_i (lo finite) ; free -> y+ - y-
    # Build list of (orig index, sign, offset) columns.
    cols = []  # each: list of (orig_var, coeff)
    offsets = [F(0)] * n
    extra_ub = []  # upper bounds as constraints
    for i, (lo, hi) in enumerate(bounds):
        if lo is None and hi is None:
            cols.append([(i, F(1))])
            cols.append([(i, F(-1))])
        elif lo is None:  # x <= hi : x = hi - y
            offsets[i] = F(hi)
            cols.append([(i, F(-1))])
        else:
            offsets[i] = F(lo)
            cols.append([(i, F(1))])
            if hi is not None:
                extra_ub.append((i, F(hi) - F(lo)))
    ny = len(cols)

    def transform_row(row):
        row = [F(v) for v in row]
        new = [F(0)] * ny
        for j, col in enumerate(cols):
            for (i, s) in col:
                new[j] += s * row[i]
        shift = sum(row[i] * offsets[i] for i in range(n))
        return new, shift

    rows = []  # (coeffs over y, rhs, kind)  kind in '<=', '=='
    for row, b in zip(A_ub, b_ub):
        new, shift = transform_row(row)
        rows.append((new, F(b) - shift, '<='))
    for row, b in zip(A_eq, b_eq):
        new, shift = transform_row(row)
        rows.append((new, F(b) - shift, '=='))
    for (i, ub) in extra_ub:
        row = [F(0)] * n
        row[i] = F(1)
        new, _ = transform_row(row)
        rows.append((new, ub, '<='))
    cy, cshift = transform_row(c)

    # standard form: add slacks for '<=' ; make rhs >= 0 ; artificials for '==' and negative rhs rows
    m = len(rows)
    nslack = sum(1 for r in rows if r[2] == '<=')
    total = ny + nslack
    tab = []
    art_cols = []
    sidx = 0
    for k, (coef, rhs, kind) in enumerate(rows):
        row = coef[:] + [F(0)] * nslack
        if kind == '<=':
            row[ny + sidx] = F(1)
            sidx += 1
        if rhs < 0:
            row = [-v for v in row]
            rhs = -rhs
            needs_art = True
        else:
            needs_art = (kind == '==')
        tab.append((row, rhs, needs_art))
    nart = sum(1 for t in tab if t[2])
    T = []
    basis = []
    aidx = 0
    for k, (row, rhs, needs_art) in enumerate(tab):
        full = row + [F(0)] * nart + [rhs]
        if needs_art:
            full[total + aidx] = F(1)
            basis.append(total + aidx)
            aidx += 1
        else:
            # basis is the slack column (must be +1) -- find it
            sl = None
            for j in range(ny, total):
                if row[j] == 1:
                    sl = j
            assert sl is not None
            basis.append(sl)
        T.append(full)
    width = total + nart + 1
    # phase 1 objective: minimize sum of artificials
    if nart:
        obj = [F(0)] * width
        for j in range(total, total + nart):
            obj[j] = F(1)
        # express in terms of nonbasic: subtract rows with artificial basis
        for i, bi in enumerate(basis):
            if bi >= total:
                obj = [a - b for a, b in zip(obj, T[i])]
        T.append(obj)
        st = _simplex(T, basis, total + nart)
        if T[-1][-1] != 0 and -T[-1][-1] != 0:
            # objective value is -T[-1][-1]?  In this layout obj row holds  -(sum art) ... check sign
            pass
        # phase-1 value = -obj_rhs ; infeasible if nonzero
        val = -T[-1][-1]
        if val != 0:
            return 'infeasible', None, None
        # drive artificials out of basis if any remain (degenerate)
        T.pop()
        for i, bi in enumerate(basis):
            if bi >= total:
                # find a nonartificial column with nonzero entry
                for j in range(total):
                    if T[i][j] != 0:
                        piv = T[i][j]
                        T[i] = [v / piv for v in T[i]]
                        for r in range(len(T)):
                            if r != i and T[r][j] != 0:
                                f = T[r][j]
                                T[r] = [a - f * b for a, b in zip(T[r], T[i])]
                        basis[i] = j
                        break
        # remove artificial columns
        T = [row[:total] + [row[-1]] for row in T]
        for i, bi in enumerate(basis):
            if bi >= total:
                # redundant zero row; keep it harmlessly (all zero) but mark basis as -1
                basis[i] = -1
        width = total + 1
    # phase 2
    obj = [F(0)] * width
    for j in range(ny):
        obj[j] = cy[j]  # reduced costs c_j - c_B B^{-1} A_j, start with c_j
    # make reduced costs consistent with basis
    for i, bi in enumerate(basis):
        if bi >= 0 and obj[bi] != 0:
            f = obj[bi]
            obj = [a - f * b for a, b in zip(obj, T[i])]
    T.append(obj)
    # rows with basis -1 are zero rows; remove them
    keep = [i for i, bi in enumerate(basis) if bi >= 0]
    T = [T[i] for i in keep] + [T[-1]]
    basis = [basis[i] for i in keep]
    st = _simplex(T, basis, total)
    if st == 'unbounded':
        return 'unbounded', None, None
    y = [F(0)] * total
    for i, bi in enumerate(basis):
        y[bi] = T[i][-1]
    x = offsets[:]
    for j, col in enumerate(cols):
        for (i, s) in col:
            x[i] += s * y[j]
    value = sum(ci * xi for ci, xi in zip(c, x))
    return 'optimal', x, value


if __name__ == "__main__":
    # smoke tests
    st, x, v = solve_lp([-1, -1], A_ub=[[1, 2], [3, 1]], b_ub=[4, 6])
    print(st, x, v)  # expect optimal, (8/5, 6/5), -14/5
    st, x, v = solve_lp([1], A_eq=[[1]], b_eq=[3], bounds=[(None, None)])
    print(st, x, v)  # 3
    st, x, v = solve_lp([-1, 0], A_ub=[[1, -1]], b_ub=[1])
    print(st)  # unbounded
    st, x, v = solve_lp([1, 1], A_ub=[[-1, -1]], b_ub=[-3], A_eq=[[1, -1]], b_eq=[0])
    print(st, x, v)  # (3/2,3/2), 3
