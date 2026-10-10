import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from fractions import Fraction as Fr
from lp_design import build, actual_norms, terms
size, _, _ = terms(1)
for kap in (Fr(102, 100), Fr(103, 100), Fr(104, 100), Fr(21, 20), Fr(106, 100), Fr(107, 100), Fr(108, 100), Fr(109, 100), Fr(1095, 1000)):
    bv = None
    for rel in ('R', 'S', 'T'):
        for idx in range(len(size[rel])):
            st, val, sol = build(case='F', fix_slope=kap, size_eq=(1, rel, idx))
            if st == 'optimal' and (bv is None or val > bv):
                bv = val
    print(f"exact-N case F kappa={kap} ({float(kap):.4f}): gap = {bv} ({float(bv):.5f}); 2(kappa-1) = {float(2*kap-2):.5f}; (3-2kappa)/8 = {float((3-2*kap)/8):.5f}")
