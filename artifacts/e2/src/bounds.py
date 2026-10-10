"""Triangle-query bounds: spectral U (Theorem B), AGM, degree, cyclic l2, true Out, kernel M."""
import math
import time
from fractions import Fraction

import numba
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import svds


def csr_from_edges(s, o, n):
    a = sp.csr_matrix((np.ones(len(s), dtype=np.float64), (s, o)), shape=(n, n))
    a.sum_duplicates()
    a.data[:] = 1.0
    a.sort_indices()
    return a


# ---------------------------------------------------------------- spectral norm
#
# Certification is exact. The power iteration runs in floating point, but every
# number this module calls a bound is an exact rational computed from integers:
#
#   * Schur:  sigma^2 <= max_row_deg * max_col_deg, an integer.
#   * Collatz-Wielandt (CW): for B = M^T M (entrywise nonnegative) and any vector
#     w > 0, rho(B) = sigma^2 <= max_i (Bw)_i / w_i.  We round the float iterate
#     UP to a positive integer vector w, compute Bw in int64 (an a-priori bound
#     rules out overflow), and take the maximum ratio as a Fraction.
#   * Rayleigh: sigma^2 >= |Mw|^2 / |w|^2 for any w != 0, computed in Python ints.
#   * Degree:   sigma^2 >= max(max_row_deg, max_col_deg) (a row or column of A).
#
# Squared bounds are stored as exact fractions ("p/q" strings); the float
# columns derived from them are square roots rounded outward (up for upper
# bounds, down for lower bounds) and verified exactly, so sigma <= sig_cert holds
# as a statement about the stored float, not about an approximation of it.


def up_sqrt(q):
    """Smallest-ish float f with f*f >= q exactly (q a Fraction or int >= 0)."""
    q = Fraction(q)
    f = math.sqrt(float(q))
    while Fraction(f) ** 2 < q:
        f = math.nextafter(f, math.inf)
    return f


def down_sqrt(q):
    """A float f >= 0 with f*f <= q exactly."""
    q = Fraction(q)
    f = math.sqrt(float(q))
    while f > 0 and Fraction(f) ** 2 > q:
        f = math.nextafter(f, 0.0)
    return f


def _int_matrix(m):
    mi = m.astype(np.int64)
    mi.data[:] = 1
    return mi


def _int_vector(w, scale):
    """Round a nonnegative float vector (max entry 1) up to a positive int64 vector."""
    wi = np.ceil(np.asarray(w, dtype=np.float64) / float(np.max(w)) * float(scale)).astype(np.int64)
    np.maximum(wi, 1, out=wi)
    return wi


def _exact_max_ratio(num, den):
    """max_i num_i/den_i as a Fraction (num >= 0, den > 0, both int64 < 2**63).

    Float ratios carry relative error < 4 * 2**-53, so the exact maximiser lies among
    indices whose float ratio is within 1e-12 of the float maximum."""
    f = num.astype(np.float64) / den.astype(np.float64)
    fmax = float(f.max())
    cand = np.flatnonzero(f >= fmax * (1 - 1e-12))
    pairs = set(zip(num[cand].tolist(), den[cand].tolist()))
    return max(Fraction(p, q) for p, q in pairs)


class _ExactB:
    """Exact arithmetic on B = M^T M for a 0/1 integer matrix M."""

    def __init__(self, m):
        self.m = _int_matrix(m)
        self.mt = self.m.T.tocsr()
        ones = np.ones(self.m.shape[1], dtype=np.int64)
        rs = self.mt @ (self.m @ ones)  # row sums of B, <= nnz
        self.maxrowsum = int(rs.max())
        self.cw_ones = Fraction(self.maxrowsum)  # CW bound at w = 1
        # largest power-of-two scale with scale * maxrowsum < 2**62: then every entry
        # of M w and of B w is < 2**62 for w with entries in [1, scale].
        self.scale = 1 << max(0, 62 - self.maxrowsum.bit_length())

    def _apply(self, wi):
        u = self.m @ wi
        bw = self.mt @ u
        assert u.dtype == np.int64 and bw.dtype == np.int64
        assert int(u.min()) >= 0 and int(bw.min()) >= 0
        assert int(bw.max()) <= int(wi.max()) * self.maxrowsum < 2 ** 63
        return u, bw

    def cw(self, w):
        wi = _int_vector(w, self.scale)
        _, bw = self._apply(wi)
        return _exact_max_ratio(bw, wi)

    def rayleigh(self, w):
        wi = _int_vector(w, self.scale)
        u, _ = self._apply(wi)
        uu = sum(x * x for x in u.tolist())
        ww = sum(x * x for x in wi.tolist())
        return Fraction(uu, ww)


def spectral(a, tol=1e-6, max_iter=3000, few=5):
    """Return dict with sigma (best estimate), an exact certified bracket and cheap certified bounds.

    Works on B = A^T A or A A^T (smaller side), restricted to its support.
    The float loop is the original estimator: Rayleigh quotient w.Bw/w.w below,
    Collatz-Wielandt max_i (Bw)_i/w_i above.  Every bound returned is then
    re-derived exactly (see the module comment above): *_sq fields are exact
    squared bounds on sigma, and schur, cw_few, sig_cert, sigma_hi (sigma_lo) are
    their square roots rounded up (down).
    """
    t0 = time.time()
    rdeg = np.diff(a.indptr)
    cdeg = np.bincount(a.indices, minlength=a.shape[1])
    if a.nnz == 0:
        z = "0"
        return dict(sigma=0.0, sigma_lo=0.0, sigma_hi=0.0, schur=0.0, cw_few=0.0, sig_cert=0.0,
                    cw1=0.0, iters=0, svds=0.0, secs=0.0, maxrow=0, maxcol=0, schur_sq=0,
                    cw_few_sq=z, cert_sq=z, hi_sq=z, lo_sq=z, rel_width=0.0, converged=True,
                    sigma_in_bracket=True, sigma_lo_fp=0.0, sigma_hi_fp=0.0)
    maxrow, maxcol = int(rdeg.max()), int(cdeg.max())
    schur_sq = maxrow * maxcol  # exact integer
    deg_lo = max(maxrow, maxcol)
    # restrict to support: rows with rdeg>0, cols with cdeg>0
    rows = np.flatnonzero(rdeg)
    cols = np.flatnonzero(cdeg)
    m = a[rows][:, cols].tocsr()
    if m.shape[0] < m.shape[1]:
        m = m.T.tocsr()
    mt = m.T.tocsr()  # B = mt @ m, dimension m.shape[1] (the smaller side)
    w = np.ones(m.shape[1])
    best_hi = math.inf
    best_lo = 0.0
    cw_list = []
    few_iterates = []   # w at steps 1..few (CW at step k uses w = B^(k-1) 1, normalised)
    w_best_hi = w
    w_best_lo = w
    it = 0
    cw_valid = True
    for it in range(1, max_iter + 1):
        if it <= few:
            few_iterates.append(w)
        bw = mt @ (m @ w)
        lo = float(w @ bw) / float(w @ w)
        if lo > best_lo:
            best_lo, w_best_lo = lo, w
        if cw_valid:
            if np.all(w > 1e-280):
                hi = float(np.max(bw / w)) * (1 + 1e-12)
                if hi < best_hi:
                    best_hi, w_best_hi = hi, w
            else:
                cw_valid = False  # positivity lost (underflow): keep earlier valid CW bounds
        if it <= few:
            cw_list.append(best_hi)
        if best_hi < math.inf and math.sqrt(best_hi) - math.sqrt(best_lo) <= tol * math.sqrt(best_hi) and it >= few:
            break
        w = bw / np.max(bw)
    w_final = w
    while len(cw_list) < few:
        cw_list.append(best_hi)
    try:
        sv = float(svds(m.astype(np.float64), k=1, tol=1e-10, return_singular_vectors=False,
                        random_state=0)[0])
    except Exception:  # noqa: BLE001
        sv = float("nan")
    sig_lo_fp = math.sqrt(best_lo)
    sig_hi_fp = math.sqrt(best_hi)
    sigma = sig_lo_fp
    if not math.isnan(sv) and sv <= sig_hi_fp * (1 + 1e-9):
        sigma = max(sigma, sv)

    # ---- exact certification
    eb = _ExactB(m)
    cw_few_sq = min(eb.cw(x) for x in few_iterates)  # CW_5: best of the first `few` iterates
    cw_few_sq = min(cw_few_sq, eb.cw_ones)
    cert_sq = min(Fraction(schur_sq), cw_few_sq)
    hi_sq = min(cert_sq, eb.cw(w_best_hi), eb.cw(w_final))
    lo_sq = max(Fraction(deg_lo), eb.rayleigh(w_best_lo), eb.rayleigh(w_final))
    # elementary consistency: a row/column of degree d forces sigma^2 >= d
    assert cert_sq >= deg_lo and hi_sq >= deg_lo, (cert_sq, hi_sq, deg_lo)
    assert lo_sq <= hi_sq, (lo_sq, hi_sq)
    sig_hi = up_sqrt(hi_sq)
    sig_lo = down_sqrt(lo_sq)
    s2 = Fraction(sigma) ** 2
    return dict(sigma=sigma, sigma_lo=sig_lo, sigma_hi=sig_hi, schur=up_sqrt(schur_sq),
                cw_few=up_sqrt(cw_few_sq), sig_cert=up_sqrt(cert_sq),
                cw1=up_sqrt(eb.cw_ones), iters=it, svds=sv, secs=time.time() - t0,
                maxrow=maxrow, maxcol=maxcol,
                schur_sq=schur_sq, cw_few_sq=str(cw_few_sq), cert_sq=str(cert_sq),
                hi_sq=str(hi_sq), lo_sq=str(lo_sq),
                rel_width=(sig_hi - sig_lo) / sig_hi, converged=(sig_hi - sig_lo) <= tol * sig_hi,
                sigma_in_bracket=bool(lo_sq <= s2 <= hi_sq),
                sigma_lo_fp=sig_lo_fp, sigma_hi_fp=sig_hi_fp)


# ---------------------------------------------------------------- counting
@numba.njit(cache=True)
def _count(du, dv, p_ptr, p_idx, q_ptr, q_idx):
    """sum over driver edges (u,v) of |P[v] ∩ Q[u]| (rows sorted)."""
    total = 0
    for e in range(du.shape[0]):
        u = du[e]
        v = dv[e]
        a0 = p_ptr[v]
        a1 = p_ptr[v + 1]
        b0 = q_ptr[u]
        b1 = q_ptr[u + 1]
        la = a1 - a0
        lb = b1 - b0
        if la == 0 or lb == 0:
            continue
        if la > lb:
            a0, a1, b0, b1 = b0, b1, a0, a1
            pa, pb = q_idx, p_idx
            la, lb = lb, la
        else:
            pa, pb = p_idx, q_idx
        if la * 16 < lb:
            # galloping-free binary search of each small-side element
            lo = b0
            for i in range(a0, a1):
                x = pa[i]
                hi = b1
                while lo < hi:
                    mid = (lo + hi) >> 1
                    if pb[mid] < x:
                        lo = mid + 1
                    else:
                        hi = mid
                if lo < b1 and pb[lo] == x:
                    total += 1
                    lo += 1
                if lo >= b1:
                    break
        else:
            i = a0
            j = b0
            while i < a1 and j < b1:
                x = pa[i]
                y = pb[j]
                if x == y:
                    total += 1
                    i += 1
                    j += 1
                elif x < y:
                    i += 1
                else:
                    j += 1
    return total


def rowdeg(m):
    return np.diff(m.indptr).astype(np.int64)


def coldeg(m):
    return np.bincount(m.indices, minlength=m.shape[1]).astype(np.int64)


def coo_rows(m):
    return np.repeat(np.arange(m.shape[0], dtype=np.int64), np.diff(m.indptr)), m.indices.astype(np.int64)


class Rel:
    """A directed relation view: m (x->y csr, sorted), mt (its transpose csr), degrees, coo."""

    def __init__(self, m, mt=None):
        self.m = m
        self.mt = mt if mt is not None else _sorted(m.T.tocsr())
        self.nnz = m.nnz
        self.rd = rowdeg(m)
        self.cd = rowdeg(self.mt)
        self.u, self.v = coo_rows(m)
        self.ptr = m.indptr.astype(np.int64)
        self.idx = m.indices.astype(np.int64)
        self.tptr = self.mt.indptr.astype(np.int64)
        self.tidx = self.mt.indices.astype(np.int64)
        self.rmax = int(self.rd.max()) if self.nnz else 0
        self.cmax = int(self.cd.max()) if self.nnz else 0
        self.f2 = float((self.rd.astype(np.float64) ** 2).sum())
        self.b2 = float((self.cd.astype(np.float64) ** 2).sum())

    def flipped(self):
        r = Rel.__new__(Rel)
        r.m, r.mt = self.mt, self.m
        r.nnz = self.nnz
        r.rd, r.cd = self.cd, self.rd
        r.u, r.v = coo_rows(self.mt)
        r.ptr, r.idx, r.tptr, r.tidx = self.tptr, self.tidx, self.ptr, self.idx
        r.rmax, r.cmax = self.cmax, self.rmax
        r.f2, r.b2 = self.b2, self.f2
        return r


def _sorted(m):
    m.sort_indices()
    return m


def kernel_M(rels):
    mt = []
    for i in range(3):
        nx, pv = rels[(i + 1) % 3], rels[(i + 2) % 3]
        a = rels[i]
        mt.append(float(np.minimum(nx.rd[a.v], pv.cd[a.u]).sum()))
    return mt


def triangle(rels, sig, check_matmul=True, matmul_budget=3e8, mt=None):
    """rels: [R x->y, S y->z, T z->x] as Rel views. sig: per-relation spectral dicts."""
    r = [float(x.nnz) for x in rels]
    res = {}
    res["r1"], res["r2"], res["r3"] = r
    deg = []
    for i in range(3):
        nx, pv = rels[(i + 1) % 3], rels[(i + 2) % 3]
        deg.append(r[i] * min(nx.rmax, pv.cmax))
    res["deg_bound"] = min(deg)
    if mt is None:
        mt = kernel_M(rels)
    res["M"] = min(mt)
    res["M1"], res["M2"], res["M3"] = mt
    res["agm"] = math.sqrt(r[0] * r[1] * r[2])
    f = [x.f2 for x in rels]
    b = [x.b2 for x in rels]
    res["l2_fwd"] = (f[0] * f[1] * f[2]) ** (1 / 3)
    res["l2_rev"] = (b[0] * b[1] * b[2]) ** (1 / 3)
    res["l2"] = min(res["l2_fwd"], res["l2_rev"])
    sg = [x["sigma"] for x in sig]  # the estimate: U is the paper's bound at the estimated sigma
    s = [min(sg[i] ** 2, r[i]) for i in range(3)]
    res["U"] = U_of(r, s)
    res["s1"], res["s2"], res["s3"] = s
    res["U_term"] = U_arg(r, s)
    res.update(certified_U(rels, sig))
    i = int(np.argmin(mt))
    a, nx, pv = rels[i], rels[(i + 1) % 3], rels[(i + 2) % 3]
    t0 = time.time()
    out = _count(a.u, a.v, nx.ptr, nx.idx, pv.tptr, pv.tidx)
    res["out"] = float(out)
    res["count_secs"] = time.time() - t0
    res["matmul_check"] = ""
    if check_matmul:
        flops = float((rels[0].cd * rels[1].rd).sum())
        if flops <= matmul_budget:
            mm = float((rels[0].m @ rels[1].m).multiply(rels[2].mt).sum())
            res["matmul_check"] = "ok" if mm == out else f"MISMATCH {mm}"
            if mm != out:
                raise AssertionError(f"count mismatch {mm} vs {out}")
    return res


U_NAMES = ["sqrt(sR rS rT)", "sqrt(sS rR rT)", "sqrt(sT rR rS)", "rR sS", "rR sT",
           "rS sR", "rS sT", "rT sR", "rT sS"]


def U_terms(r, s):
    rR, rS, rT = r
    sR, sS, sT = s
    return [math.sqrt(sR * rS * rT), math.sqrt(sS * rR * rT), math.sqrt(sT * rR * rS),
            rR * sS, rR * sT, rS * sR, rS * sT, rT * sR, rT * sS]


def U_of(r, s):
    return min(U_terms(r, s))


def U_arg(r, s):
    t = U_terms(r, s)
    return U_NAMES[int(np.argmin(t))]


# ---------------------------------------------------------------- exact certified U
CERT_U = (("U_schur", "schur_sq", "up"), ("U_cw", "cw_few_sq", "up"), ("U_cert", "cert_sq", "up"),
          ("U_hi", "hi_sq", "up"), ("U_lo", "lo_sq", "down"))


def U_sq_exact(r, s):
    """min of the squared U terms, exactly (r ints, s Fractions)."""
    rR, rS, rT = (Fraction(x) for x in r)
    sR, sS, sT = s
    return min(sR * rS * rT, sS * rR * rT, sT * rR * rS,
               (rR * sS) ** 2, (rR * sT) ** 2, (rS * sR) ** 2, (rS * sT) ** 2,
               (rT * sR) ** 2, (rT * sS) ** 2)


def certified_U(r, sig):
    """U_schur, U_cw, U_cert, U_hi (rounded up) and U_lo (rounded down) from exact squared sigma bounds.

    r: the three relation sizes (ints, or Rel views); sig: their spectral dicts.  U is
    monotone in each s_i = min(sigma_i^2, r_i), so an upper (lower) bound on every
    sigma_i^2 gives an upper (lower) bound on U(sigma)."""
    r = [x if isinstance(x, int) else int(x.nnz) for x in r]
    out = {}
    for key, field, rnd in CERT_U:
        s = [min(Fraction(sig[i][field]), Fraction(r[i])) for i in range(3)]
        q = U_sq_exact(r, s)
        out[key] = up_sqrt(q) if rnd == "up" else down_sqrt(q)
    return out

