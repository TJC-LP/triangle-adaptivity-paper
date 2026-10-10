# Exponent LP for the design space "three rotated live gadgets, any parameters" (base: N = u^1).
# Variables (exponents): per gadget i = 1,2,3: P,Q,T,G,K,W >= 0 (Z2 := P + T - G); union forward norm exponents A,B,Gm;
# union backward norm exponents Ap,Bp,Gp; cost exponent c; m = max(1, slope).
# Term lists come from my closed forms (live_gadget.closed_live), each term = exponent of one monomial of the closed form.
#   sizes:  R: P+Q, Z2+Q-W | S: Q+T, Z2, Z2+Q | T: P+T, P, T, Z2+Q-K
#   fwd:    alpha: P+2Q, Z2+Q+K-W | beta: Q+2T, 2Z2-Q, Z2+Q+W | gamma: T, 2P-T, Z2+2G, Z2+2Q-2K
#   bwd:    alpha': 2P+Q, Z2+Q-W | beta': T+2Q, Z2+2Q, Z2 | gamma': P+2T, Z2+Q+W-K
#   cost of the designated root >= pqt: c <= P+Q+T (exact up to constants: every other cost term is a size term, see report)
#   parameters: T <= P, G <= P, K <= Q, W <= Z2, Q <= Z2
# Rotation of copy k: local (R,S,T) -> global index +k; local (alpha,beta,gamma) -> global index +k; same for backward.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from fractions import Fraction as Fr
from exact_lp import simplex_max

GAD = ['P', 'Q', 'T', 'G', 'K', 'W']
NAMES = [f'{v}{i}' for i in (1, 2, 3) for v in GAD] + ['A', 'B', 'Gm', 'Ap', 'Bp', 'Gp', 'c', 'm']
IDX = {n: i for i, n in enumerate(NAMES)}


def lin(i, **kw):
    """linear form over gadget i's variables: lin(1, P=1, Q=2) -> {P1:1, Q1:2}; Z2 expands to P+T-G."""
    d = {}
    for k, v in kw.items():
        if k == 'Z2':
            for kk, vv in (('P', 1), ('T', 1), ('G', -1)):
                d[f'{kk}{i}'] = d.get(f'{kk}{i}', 0) + v * vv
        else:
            d[f'{k}{i}'] = d.get(f'{k}{i}', 0) + v
    return d


def terms(i):
    L = lambda **kw: lin(i, **kw)
    size = {'R': [L(P=1, Q=1), L(Z2=1, Q=1, W=-1)],
            'S': [L(Q=1, T=1), L(Z2=1), L(Z2=1, Q=1)],
            'T': [L(P=1, T=1), L(P=1), L(T=1), L(Z2=1, Q=1, K=-1)]}
    fwd = {'al': [L(P=1, Q=2), L(Z2=1, Q=1, K=1, W=-1)],
           'be': [L(Q=1, T=2), L(Z2=2, Q=-1), L(Z2=1, Q=1, W=1)],
           'ga': [L(T=1), L(P=2, T=-1), L(Z2=1, G=2), L(Z2=1, Q=2, K=-2)]}
    bwd = {'alp': [L(P=2, Q=1), L(Z2=1, Q=1, W=-1)],
           'bep': [L(T=1, Q=2), L(Z2=1, Q=2), L(Z2=1)],
           'gap': [L(P=1, T=2), L(Z2=1, Q=1, W=1, K=-1)]}
    return size, fwd, bwd


def size_terms_all():
    out = []
    for i in (1, 2, 3):
        size, _, _ = terms(i)
        for rel in ('R', 'S', 'T'):
            for f in size[rel]:
                out.append((i, rel, f))
    return out


def build(case='F', fix_m=None, fix_slope=None, size_eq=None, extra=(), symmetric=False):
    """case 'F': m >= fwd average; 'B': m >= bwd average. fix_m: m == value. fix_slope: case average == value.
    size_eq: (i, rel, idx) size term forced == 1 (N exponent exactly 1). Returns (status, value, dict)."""
    rows = []
    def add(form, sense, rhs):
        rows.append(({IDX[k]: v for k, v in form.items()}, sense, rhs))
    fwd_names = ['A', 'B', 'Gm']; bwd_names = ['Ap', 'Bp', 'Gp']
    for i, k in ((1, 0), (2, 1), (3, 2)):
        size, fwd, bwd = terms(i)
        for rel in ('R', 'S', 'T'):
            for f in size[rel]:
                add(f, '<=', 1)
        for li, key in enumerate(('al', 'be', 'ga')):
            g = fwd_names[(li + k) % 3]
            for f in fwd[key]:
                d = dict(f); d[g] = d.get(g, 0) - 1; add(d, '<=', 0)
        for li, key in enumerate(('alp', 'bep', 'gap')):
            g = bwd_names[(li + k) % 3]
            for f in bwd[key]:
                d = dict(f); d[g] = d.get(g, 0) - 1; add(d, '<=', 0)
        add({**lin(i, P=1, Q=1, T=1), 'c': -1}, '>=', 0)       # c <= P+Q+T
        add(lin(i, T=1, P=-1), '<=', 0); add(lin(i, G=1, P=-1), '<=', 0); add(lin(i, K=1, Q=-1), '<=', 0)
        add(lin(i, W=1, Z2=-1), '<=', 0); add(lin(i, Q=1, Z2=-1), '<=', 0)
    add({'m': 1}, '>=', 1)
    avg = {n: Fr(1, 3) for n in (fwd_names if case == 'F' else bwd_names)}
    add({**avg, 'm': -1}, '<=', 0)                               # m >= case average
    if fix_m is not None:
        add({'m': 1}, '==', fix_m)
    if fix_slope is not None:
        add(dict(avg), '==', fix_slope)
    if size_eq is not None:
        i, rel, idx = size_eq
        add(terms(i)[0][rel][idx], '==', 1)
    for form, sense, rhs in extra:
        add(form, sense, rhs)
    if symmetric:
        for v in GAD:
            add({f'{v}1': 1, f'{v}2': -1}, '==', 0); add({f'{v}1': 1, f'{v}3': -1}, '==', 0)
    st, val, x = simplex_max(len(NAMES), rows, {IDX['c']: 1, IDX['m']: -1})
    sol = dict(zip(NAMES, x)) if x is not None else None
    return st, val, sol


def actual_norms(sol):
    """Actual exponents (max of terms) of the union's forward and backward norms at a solution, and the slopes."""
    ev = lambda f: sum(Fr(v) * sol[k] for k, v in f.items())
    fw = [None, None, None]; bw = [None, None, None]
    for i, k in ((1, 0), (2, 1), (3, 2)):
        size, fwd, bwd = terms(i)
        for li, key in enumerate(('al', 'be', 'ga')):
            g = (li + k) % 3
            mx = max(ev(f) for f in fwd[key]); fw[g] = mx if fw[g] is None else max(fw[g], mx)
        for li, key in enumerate(('alp', 'bep', 'gap')):
            g = (li + k) % 3
            mx = max(ev(f) for f in bwd[key]); bw[g] = mx if bw[g] is None else max(bw[g], mx)
    nmax = max(ev(f) for i in (1, 2, 3) for rel in ('R', 'S', 'T') for f in terms(i)[0][rel])
    return dict(fwd=fw, bwd=bw, kf=sum(fw) / 3, kb=sum(bw) / 3, n=nmax, c=min(sol[f'P{i}'] + sol[f'Q{i}'] + sol[f'T{i}'] for i in (1, 2, 3)))


def show(sol):
    return {k: str(v) for k, v in sol.items() if v != 0}


if __name__ == '__main__':
    import time
    t0 = time.time()
    print("== design-space LP (exact rationals) ==")
    for case in ('F', 'B'):
        st, val, sol = build(case=case)
        an = actual_norms(sol)
        print(f"case {case} (m >= {'forward' if case == 'F' else 'backward'} average), free slope: {st} value = {val} = {float(val):.5f}")
        print(f"   solution: {show(sol)}")
        print(f"   actual at solution: fwd={[str(v) for v in an['fwd']]} bwd={[str(v) for v in an['bwd']]} kappa_f={an['kf']} kappa_b={an['kb']} N-exp={an['n']} c={an['c']}")
    st, val, sol = build(case='F', symmetric=True)
    print(f"case F, symmetric gadgets: value = {val}; solution {show(sol)}")
    # uniqueness of the maximiser slope: restrict the case average away from 11/10
    for case in ('F', 'B'):
        for delta in (Fr(1, 100), Fr(1, 1000)):
            names = ['A', 'B', 'Gm'] if case == 'F' else ['Ap', 'Bp', 'Gp']
            avg = {n: Fr(1, 3) for n in names}
            st1, v1, _ = build(case=case, extra=[(dict(avg), '<=', Fr(11, 10) - delta)])
            st2, v2, _ = build(case=case, extra=[(dict(avg), '>=', Fr(11, 10) + delta)])
            print(f"case {case}: slope <= 11/10 - {delta}: value {v1} = {float(v1):.5f};  slope >= 11/10 + {delta}: value {v2} = {float(v2):.5f}")
    # Fable-style profile: m fixed = kappa, case average <= kappa, sizes <= 1 (relaxed)
    print("-- profile, Fable's convention (m = kappa fixed, forward average <= kappa, sizes <= 1):")
    for kap in (Fr(1), Fr(21, 20), Fr(11, 10), Fr(23, 20), Fr(6, 5), Fr(5, 4), Fr(13, 10), Fr(7, 5), Fr(3, 2)):
        st, val, sol = build(case='F', fix_m=kap)
        print(f"   kappa={kap} ({float(kap):.3f}): gap = {val} ({float(val):.5f}); general (3-2k)/8 = {(3 - 2 * kap) / 8} ({float((3 - 2 * kap) / 8):.5f})")
    # exact-N profile: some size term == 1 (by cyclic symmetry WLOG in gadget 1), case average == kappa, m = max(1,kappa)
    print("-- profile with N exponent exactly 1 and case average exactly kappa (max over the 9 size terms of gadget 1, both cases):")
    for kap in (Fr(1), Fr(21, 20), Fr(11, 10), Fr(23, 20), Fr(6, 5), Fr(5, 4), Fr(13, 10), Fr(7, 5), Fr(3, 2)):
        best = {}
        for case in ('F', 'B'):
            bv = None; barg = None
            size, _, _ = terms(1)
            for rel in ('R', 'S', 'T'):
                for idx in range(len(size[rel])):
                    st, val, sol = build(case=case, fix_slope=kap, size_eq=(1, rel, idx))
                    if st == 'optimal' and (bv is None or val > bv):
                        bv, barg = val, (rel, idx, sol)
            best[case] = (bv, barg)
        line = f"   kappa={kap} ({float(kap):.3f}):"
        for case in ('F', 'B'):
            bv, barg = best[case]
            if bv is None:
                line += f"  case {case}: infeasible;"
            else:
                an = actual_norms(barg[2])
                line += f"  case {case}: gap = {bv} ({float(bv):.5f}) [actual kf={an['kf']} kb={an['kb']}];"
        print(line)
    print(f"total time {time.time() - t0:.0f}s")
