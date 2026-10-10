"""Independent recomputation of selected E2 rows from raw data."""
import csv, gzip, math, random, sys, time, json
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import svds
import numba

E = sys.argv[1]
import os
SCI = os.environ.get("SCI50_NT", "data/sci50.nt")  # bench/sparqloscope replicate.py output
rows = list(csv.DictReader(open(f"{E}/results.csv")))

# ---------- row selection ----------
rng = random.Random(20261009)
by = {}
for i, x in enumerate(rows):
    g = x['dataset'] if x['dataset'] in ('sci50', 'codex-l', 'wikidata5m') else 'snap'
    by.setdefault(g, []).append(i)
pick = set()
for g, k in (('sci50', 4), ('codex-l', 4), ('wikidata5m', 4), ('snap', 4)):
    pick.update(rng.sample(by[g], k))
for i, x in enumerate(rows):
    q = x['query']
    if (x['dataset'] == 'wikidata5m' and q in ('P17 . P47 . P17^T', 'P17 . P17 . P17', 'P131 . P131 . P131')) \
       or (x['dataset'] == 'sci50' and 'Award_Nominations' in q and 'Influenced_By' in q and x['p1'].endswith('Award_Nominations>')) \
       or (x['dataset'] == 'com-youtube'):
        pick.add(i)
pick = sorted(pick)
need = {}
for i in pick:
    x = rows[i]; need.setdefault((x['dataset']), set()).update({x['p1'], x['p2'], x['p3']})
print("picked", len(pick), {k: len(v) for k, v in need.items()}, flush=True)

# ---------- loaders (own code) ----------
def load_kg(paths, preds):
    ids = {}; E = {p: ([], []) for p in preds}
    for path in paths:
        with open(path) as fh:
            for line in fh:
                t = line.split()
                if len(t) != 3 or t[1] not in E: continue
                a = ids.setdefault(t[0], len(ids)); b = ids.setdefault(t[2], len(ids))
                E[t[1]][0].append(a); E[t[1]][1].append(b)
    return ids, E

def load_nt(path, preds):
    ids = {}; E = {p: ([], []) for p in preds}
    with open(path, encoding="utf-8", errors="surrogateescape") as fh:
        for line in fh:
            # subject and predicate are IRIs/bnodes without spaces; object = remainder minus " ."
            i1 = line.find(' '); i2 = line.find(' ', i1 + 1)
            if i1 < 0 or i2 < 0: continue
            p = line[i1 + 1:i2]
            if p not in E: continue
            o = line[i2 + 1:].rstrip()
            if o.endswith('.'): o = o[:-1].rstrip()
            a = ids.setdefault(line[:i1], len(ids)); b = ids.setdefault(o, len(ids))
            E[p][0].append(a); E[p][1].append(b)
    return ids, E

def load_snap(path, sym):
    s = []; o = []
    with gzip.open(path, 'rt') as fh:
        for line in fh:
            if line.startswith('#'): continue
            t = line.split()
            if len(t) < 2: continue
            s.append(int(t[0])); o.append(int(t[1]))
    s = np.array(s); o = np.array(o)
    if sym: s, o = np.concatenate([s, o]), np.concatenate([o, s])
    return s, o

def mat(s, o, n):
    s = np.asarray(s, np.int64); o = np.asarray(o, np.int64)
    m = sp.csr_matrix((np.ones(len(s), np.float64), (s, o)), shape=(n, n))
    m.sum_duplicates(); m.data[:] = 1.0; m.sort_indices()
    return m

# ---------- spectral ----------
def sigma(A):
    A = A.tocsr(); At = A.T.tocsr()
    rows_ = np.diff(A.indptr); cols_ = np.diff(At.indptr)
    schur = math.sqrt(rows_.max() * cols_.max())
    v = (cols_ > 0).astype(np.float64)
    cw5 = None
    lo = 0.0; hi = math.inf
    for it in range(1, 5000):
        w = At @ (A @ v)
        mask = v > 0
        cw = float(np.max(w[mask] / v[mask]))
        hi = min(hi, cw)
        lo = max(lo, float(v @ w) / float(v @ v))
        if it == 5: cw5 = math.sqrt(cw)
        v = w / np.linalg.norm(w)
        if it >= 5 and math.sqrt(hi) - math.sqrt(lo) <= 1e-7 * math.sqrt(lo): break
    def cw5side(X):
        Xt = X.T.tocsr(); v = (np.diff(Xt.indptr) > 0).astype(np.float64)
        for _ in range(4): v = Xt @ (X @ v); v /= v.max()
        w = Xt @ (X @ v); m = v > 0
        return math.sqrt(float(np.max(w[m] / v[m])))
    cwA, cwB = cw5side(A), cw5side(At)
    sv = svds(A, k=1, return_singular_vectors=False)[0]
    return dict(lo=math.sqrt(lo), hi=math.sqrt(hi), svds=float(sv), schur=schur, cw5=cw5, cwA=cwA, cwB=cwB, iters=it)

# ---------- counting ----------
@numba.njit(cache=False)
def count(e1p, e1i, e2p, e2i, e3tp, e3ti):
    # sum over (u,v) in E1 of |E2[v,:] ∩ E3^T[u,:]|
    tot = 0
    n = len(e1p) - 1
    for u in range(n):
        a0 = e3tp[u]; a1 = e3tp[u + 1]
        if a0 == a1: continue
        for k in range(e1p[u], e1p[u + 1]):
            v = e1i[k]
            b0 = e2p[v]; b1 = e2p[v + 1]
            i = a0; j = b0
            while i < a1 and j < b1:
                x = e3ti[i]; y = e2i[j]
                if x == y:
                    tot += 1; i += 1; j += 1
                elif x < y: i += 1
                else: j += 1
    return tot

def Mterm(E1, E2, E3):
    # driver E1=(u,v): third var w with E2[v,w], E3[w,u]
    E1c = E1.tocoo()
    r2 = np.diff(E2.indptr); c3 = np.asarray((E3 > 0).sum(axis=0)).ravel()
    return float(np.minimum(r2[E1c.col], c3[E1c.row]).sum())

def analyse(rel, label):
    E = rel
    r = [E[k].nnz for k in range(3)]
    M = [Mterm(E[0], E[1], E[2]), Mterm(E[1], E[2], E[0]), Mterm(E[2], E[0], E[1])]
    k = int(np.argmin(M))
    A, B, C = E[k], E[(k + 1) % 3], E[(k + 2) % 3]
    Ct = C.T.tocsr(); Ct.sort_indices()
    t0 = time.time()
    out = count(A.indptr, A.indices, B.indptr, B.indices, Ct.indptr, Ct.indices)
    ct = time.time() - t0
    # second independent count for small cases: dense-free SpGEMM
    mm = None
    if M[k] < 3e8:
        mm = int(round((E[0] @ E[1]).multiply(E[2].T).sum()))
    rowd = [np.diff(E[i].indptr) for i in range(3)]
    cold = [np.diff(E[i].T.tocsr().indptr) for i in range(3)]
    fwd = math.prod(float((d.astype(np.float64) ** 2).sum()) for d in rowd)
    rev = math.prod(float((d.astype(np.float64) ** 2).sum()) for d in cold)
    l2 = min(fwd, rev) ** (1 / 3)
    # degree bound: per driver edge (u,v), w ∈ E2[v,:] ∩ E3[:,u]
    deg = min(float(r[i]) * float(min(rowd[(i + 1) % 3].max(), cold[(i + 2) % 3].max())) for i in range(3))
    return dict(r=r, M=M, out=out, mm=mm, l2=l2, l2f=fwd ** (1 / 3), l2r=rev ** (1 / 3), deg=deg,
                agm=math.sqrt(r[0] * r[1] * r[2]), secs=ct)

def Ufrom(r, sig):
    s = [min(sig[i] ** 2, r[i]) for i in range(3)]
    t = [math.sqrt(s[0] * r[1] * r[2]), math.sqrt(s[1] * r[0] * r[2]), math.sqrt(s[2] * r[0] * r[1])]
    t += [r[i] * s[j] for i in range(3) for j in range(3) if i != j]
    return min(t), s

# ---------- main ----------
SNAPF = {'ca-GrQc': 'ca-GrQc.txt.gz', 'email-Eu-core': 'email-Eu-core.txt.gz', 'wiki-Vote': 'wiki-Vote.txt.gz',
         'soc-Epinions1': 'soc-Epinions1.txt.gz', 'com-youtube': 'com-youtube.ungraph.txt.gz',
         'com-dblp': 'com-dblp.ungraph.txt.gz'}
results = []
def rel(x, dset_mats):
    out = []
    for k in (1, 2, 3):
        m = dset_mats[x[f'p{k}']]
        out.append(m.T.tocsr() if x[f'd{k}'] == '1' else m)
    for m in out: m.sort_indices()
    return out

def report(i, x, R, sigs):
    sig = [sigs[x[f'p{k}']] for k in (1, 2, 3)]
    sigma_ = [(g['lo'] + g['hi']) / 2 for g in sig]
    U, s = Ufrom(R['r'], sigma_)
    Ucert, _ = Ufrom(R['r'], [min(g['schur'], g['cw5']) for g in sig])
    U_schur, _ = Ufrom(R['r'], [g['schur'] for g in sig])
    f = lambda k: float(x[k])
    cmp = {
        'r': (R['r'], [f('r1'), f('r2'), f('r3')]),
        'sigma': (sigma_, [f('sigma1'), f('sigma2'), f('sigma3')]),
        'svds': ([g['svds'] for g in sig], [f('sigma1'), f('sigma2'), f('sigma3')]),
        'sig_cert': ([min(g['schur'], g['cw5']) for g in sig], [f('sig_cert1'), f('sig_cert2'), f('sig_cert3')]),
        'U': (U, f('U')), 'U_cert': (Ucert, f('U_cert')), 'U_schur': (U_schur, f('U_schur')),
        'cw5_either': ([min(abs(min(g['schur'], g['cwA']) - c), abs(min(g['schur'], g['cwB']) - c)) + c for g, c in zip(sig, [f('sig_cert1'), f('sig_cert2'), f('sig_cert3')])], [f('sig_cert1'), f('sig_cert2'), f('sig_cert3')]),
        'agm': (R['agm'], f('agm')), 'deg': (R['deg'], f('deg_bound')),
        'l2': (R['l2'], f('l2')), 'l2_fwd': (R['l2f'], f('l2_fwd')), 'l2_rev': (R['l2r'], f('l2_rev')),
        'out': (R['out'], f('out')), 'M': (min(R['M']), f('M')),
        'M123': (R['M'], [f('M1'), f('M2'), f('M3')]),
    }
    worst = {}
    for k, (a, b) in cmp.items():
        a = np.atleast_1d(np.asarray(a, float)); b = np.atleast_1d(np.asarray(b, float))
        worst[k] = float(np.max(np.abs(a - b) / np.maximum(np.abs(b), 1e-300)))
    wid = ['%.1e' % ((g['hi'] - g['lo']) / g['lo']) for g in sig]
    mr = {k: '%.1e' % v for k, v in worst.items()}
    flag = [k for k, v in worst.items() if v > (2e-6 if k in ('sigma', 'svds', 'U') else 1e-9)]
    print(f"row {i} {x['dataset']}/{x['variant']} [{x['query']}] out={R['out']} (mm={R['mm']}) "
          f"U={U:.6g} l2={R['l2']:.6g} deg={R['deg']:.6g} M={min(R['M']):.6g} cnt {R['secs']:.1f}s "
          f"| sigma width {wid} "
          f"| maxrel {mr} | MISMATCH {flag}", flush=True)
    results.append(dict(row=i, dataset=x['dataset'], query=x['query'], mismatches=flag, worst=worst,
                        out=int(R['out']), mm=None if R['mm'] is None else int(R['mm']), U=U, l2=R['l2'], agm=R['agm'], deg=R['deg']))

for ds, preds in need.items():
    t0 = time.time()
    idx = [i for i in pick if rows[i]['dataset'] == ds]
    if ds in SNAPF:
        for var in sorted({rows[i]['variant'] for i in idx}):
            s, o = load_snap(f"{E}/data/snap/{SNAPF[ds]}", var == 'sym')
            uniq, inv = np.unique(np.concatenate([s, o]), return_inverse=True)
            n = len(uniq); m = mat(inv[:len(s)], inv[len(s):], n)
            mats = {ds: m}; sigs = {ds: sigma(m)}
            for i in idx:
                if rows[i]['variant'] != var: continue
                report(i, rows[i], analyse(rel(rows[i], mats), ds), sigs)
        continue
    if ds == 'sci50':
        ids, Ed = load_nt(SCI, preds)
    elif ds == 'codex-l':
        ids, Ed = load_kg([f"{E}/data/kg/codex-l-{s}.txt" for s in ('train', 'valid', 'test')], preds)
    else:
        ids, Ed = load_kg([f"{E}/data/kg/w5m/wikidata5m_transductive_{s}.txt" for s in ('train', 'valid', 'test')], preds)
    n = len(ids)
    mats = {p: mat(*Ed[p], n) for p in preds}
    sigs = {p: sigma(mats[p]) for p in preds}
    print(f"[{ds}] loaded {time.time()-t0:.0f}s", flush=True)
    for i in idx:
        report(i, rows[i], analyse(rel(rows[i], mats), ds), sigs)
json.dump(results, open(f"{E}/check/recompute.json", "w"), indent=1)
print("TOTAL rows", len(results), "rows with mismatches", sum(1 for r in results if r['mismatches']))
