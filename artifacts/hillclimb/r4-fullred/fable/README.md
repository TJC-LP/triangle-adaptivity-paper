# Verifier B: fully reduced inputs (revision 4)

Independent rebuild, in exact integer arithmetic, of the claim that the fully reduced
per-binding gap lies in [1/10, 1/8]. The verifier's written verdict was returned to the
editor as a message and is summarized here; the scripts and outputs are complete.

- The live gadget `L(p,q,t,g,k,w)` (`live_gadget.py`) is fully reduced; its closed forms for
  sizes, output, the three root costs and all six squared-degree sums match brute force on
  733 parameter tuples and on 60 random three-copy unions (`out_check_live*.txt`).
- `L(v)`, the union of three rotations of `L(v^5, v^3, v^4, v^2, v^2, v)`: brute force for
  v = 2, 3, 4 and closed forms for v = 2..60 (`out_check_family.txt`); C/(N + B2) >= v/24;
  the first v with C > N + B2 is v = 14.
- The general family `L(u^4i, u^(4i-2j), u^(4i-j), u^(4i-3j), u^j, 1)`, 5j <= 4i, has cost
  exponent (3 + 6 kappa)/8 at slope kappa = 3/2 - j/(2i), i.e. it equals the general
  worst case on [11/10, 3/2] (`out_check_family.txt`, part B).
- The exact design-space LP (`lp_design.py`) caps the gap of three rotated live gadgets at
  1/10, attained only at slope 11/10. The value 1/11 "at kappa = 1" in the solver's report
  is an artifact of an LP that bounds size exponents by 1 without forcing one to equal 1:
  its optimum has actual slope 11/10 (`out_lp_near1.txt`); with the size exponent forced
  to 1 the design gives 0 at slope 1 (`out_lp_design.txt`, `out_lp_profile_fine.txt`).
  The fully reduced gap at slopes in [1, 11/10) is therefore open.
- `check_iv.py` re-verifies the revision-3 gadget I_v (gap 1/12) for v = 1..8.
