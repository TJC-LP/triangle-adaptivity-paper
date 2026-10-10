import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from fractions import Fraction as Fr
from lp_design import build, actual_norms, show, terms
# 1. Fable's convention at kappa = 1: what are the actual N exponent and slope of the optimal point?
st, val, sol = build(case='F', fix_m=Fr(1))
an = actual_norms(sol)
print(f"Fable-convention kappa=1: value {val}; actual N-exp n = {an['n']}, kappa_f = {an['kf']}, kappa_b = {an['kb']}, c = {an['c']}")
print(f"   rescaled by 1/n: true slope = {an['kf'] / an['n']}, true gap = {(an['c'] - max(1, an['kf'])) / an['n']}")
print(f"   solution: {show(sol)}")
# 2. exact-N profile just above kappa = 1
for kap in (Fr(1), Fr(10001, 10000), Fr(1001, 1000), Fr(101, 100), Fr(21, 20), Fr(1091, 1000), Fr(11, 10)):
    bv = None; barg = None
    size, _, _ = terms(1)
    for rel in ('R', 'S', 'T'):
        for idx in range(len(size[rel])):
            st, val, sol = build(case='F', fix_slope=kap, size_eq=(1, rel, idx))
            if st == 'optimal' and (bv is None or val > bv):
                bv, barg = val, (rel, idx, sol)
    an = actual_norms(barg[2])
    print(f"exact-N, case F, kappa={kap} ({float(kap):.4f}): gap = {bv} ({float(bv):.5f}); (3-2k)/8 = {float((3-2*kap)/8):.5f}; 2 kappa - 2 = {float(2*kap-2):.5f}; actual kf={an['kf']} kb={an['kb']} n={an['n']} c={an['c']}; size term {barg[0]}{barg[1]}")
    if kap in (Fr(1), Fr(101, 100)):
        print(f"   solution: {show(barg[2])}")
