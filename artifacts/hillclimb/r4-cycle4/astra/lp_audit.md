# Independent C4 arc LP audit

**Verdict: proved.** The arc LP has precisely 50 vertices, and precisely 38 are necessary on the regular cone `1 <= s_e <= r_e`. The 13-arc and 9-arc families have the same real LP optimum and even the same integer optimum. All 38 named terms match the independently generated vertices exactly. Every term has a nontrivial equality construction, and every term is indispensable even for a constant-factor estimate.

Only solver source text was read. No solver program/module was executed or imported. All executable calculations were newly written in `lp_independent.py`, executed with `python3 -I`; its imports are Python standard library only. Exact results and certificates are in `lp_independent.json`; stdout is in `lp_independent.out`.

## Polyhedron and complete enumeration

For each nonempty connected arc A of the 4-cycle, let a_A in {0,1}^8 have first four coordinates `1[A meets e]` and last four `1[|A intersect e|=1]`, in R,S,T,Q order. The dual is `v >= 0`, `a_A dot v >= 1`. If a vertex has m strictly positive coordinates, the active arc rows restricted to those coordinates have rank m. Otherwise a nonzero direction supported on those coordinates preserves every tight constraint, and sufficiently small perturbations in both directions remain feasible, contradicting extremality. Conversely m independent tight arc rows plus the zero-coordinate constraints determine a vertex. Thus enumerating all positive supports and square active-row systems is exhaustive.

The new code enumerates every support of size m=1,...,8 and every m-element subset of the arc rows, performs exact Fraction forward elimination and back substitution, rejects singular systems, and checks positivity and all inequalities exactly. The one all-zero support is infeasible and omitted. Counts:

| Case | Arcs | Square systems attempted | Vertices | Needed | Dominated |
|---|---:|---:|---:|---:|---:|
| Triangle | 7 | 1,715 | 13 | 9 | 4 |
| C4 reduced | 9 | 24,309 | 50 | 38 | 12 |
| C4 full | 13 | 203,489 | 50 | 38 | 12 |

The last two vertex lists are exactly equal. Their attempt counts are `binom(17,8)-1` and `binom(21,8)-1`. The triangle count is `binom(13,6)-1`. This full-support argument is equivalent to exhaustive bases including nonnegativity rows, with the impossible all-zero basis removed.

There is also a direct proof of equality of the C4 polyhedra. A triple arc meets all four edges; its row is the full-arc row plus two nonnegative mu coordinates. Its constraint is therefore implied by the full-arc constraint and nonnegativity. Primal interpretation: replace every triple-arc factor of multiplicity n by a full-arc factor of multiplicity n. All four cardinalities and the output stay the same; its two boundary squared norms decrease by factor n. This proves equivalence of integer optima too.

## Irredundancy and exact certificates

Put `d_e=log(r_e/s_e)>=0` and `b_e=log s_e>=0`. A dual vector v=(lambda,mu) has transformed exponents `(lambda,lambda+mu)` in variables `(d,b)`. Coordinatewise domination in those transformed exponents therefore proves redundancy throughout the regular cone. Each of the 12 discarded vertices is directly dominated by one of the 38 retained vertices, as listed below.

For each retained vertex v, the new code independently found an integer c=(rho,varsigma) satisfying rho>=varsigma>=0, and verified exactly that `(u-v) dot c >= gap > 0` for all 49 other vertices u. These are complete strict-separation certificates; the displayed gap is the minimum over all 49 competitors. Finding them took 1,090 seeded integer draws; certification itself is exhaustive, not probabilistic. A small interior perturbation of c, if needed, preserves its positive margin and gives an open regular region.

The finite certificate files also contain, for each strict witness c, an independently solved feasible nonnegative rational primal vector nu with `sum nu = v dot c`. Its denominators belong to {1,2,3,4}. Clearing denominators with D and setting every arc multiplicity to `n^(D nu_A)` gives an integer arc family attaining v at bounds `r_e=n^(D rho_e)`, `s_e=n^(D varsigma_e)`. Every other term exceeds its output by at least `n^(D gap)`. Thus every term remains necessary even up to an arbitrary universal multiplicative constant.

| Vertex ID | Monomial | Strict c=(rho; varsigma) | Gap |
|---:|---|---|---:|
| 0 | `r_Q s_S s_T` | `(27, 25, 11, 7); (8, 6, 0, 1)` | 1 |
| 1 | `r_Q s_R^(1/2) s_S^(1/2) s_T^(1/2)` | `(14, 24, 30, 6); (7, 10, 13, 0)` | 1/2 |
| 2 | `r_Q s_R s_T` | `(14, 30, 9, 12); (2, 11, 1, 12)` | 4/3 |
| 3 | `r_Q s_R s_S` | `(5, 16, 16, 3); (4, 4, 15, 3)` | 1 |
| 4 | `r_T^(1/2) r_Q^(1/2) s_R^(1/2) s_S^(1/2)` | `(18, 24, 17, 8); (2, 8, 11, 7)` | 1/2 |
| 5 | `r_T s_S s_Q` | `(27, 21, 6, 17); (10, 5, 6, 4)` | 1/2 |
| 6 | `r_T s_R^(1/2) s_S^(1/2) s_Q^(1/2)` | `(27, 24, 8, 23); (12, 11, 2, 6)` | 3/2 |
| 7 | `r_T s_R s_Q` | `(17, 33, 13, 14); (4, 15, 13, 3)` | 5/3 |
| 8 | `r_T s_R s_S` | `(21, 14, 2, 22); (2, 4, 0, 15)` | 9/2 |
| 11 | `r_S^(1/3) r_Q^(2/3) s_R^(1/3) s_S^(1/3) s_T^(1/3)` | `(25, 21, 31, 14); (8, 3, 13, 9)` | 2/3 |
| 12 | `r_S^(1/3) r_T^(1/3) r_Q^(1/3) s_R^(1/3) s_S^(1/3) s_Q^(1/3)` | `(18, 17, 15, 9); (12, 12, 12, 1)` | 1/4 |
| 13 | `r_S^(1/2) r_Q^(1/2) s_S^(1/2) s_T^(1/2) s_Q^(1/2)` | `(17, 7, 14, 5); (13, 0, 11, 0)` | 1/2 |
| 14 | `r_S^(1/2) r_Q^(1/2) s_R^(1/4) s_S^(1/4) s_T^(1/4) s_Q^(1/4)` | `(26, 13, 28, 22); (7, 1, 11, 11)` | 1/3 |
| 15 | `r_S^(1/2) r_Q^(1/2) s_R^(1/2) s_T^(1/2)` | `(17, 16, 9, 14); (2, 14, 1, 12)` | 1/2 |
| 16 | `r_S^(1/2) r_Q^(1/2) s_R^(1/2) s_S^(1/2) s_Q^(1/2)` | `(17, 10, 18, 9); (4, 6, 13, 2)` | 1/4 |
| 17 | `r_S^(1/2) r_T^(1/2) s_R^(1/2) s_Q^(1/2)` | `(22, 12, 20, 17); (9, 12, 15, 2)` | 5/6 |
| 19 | `r_S^(2/3) r_Q^(1/3) s_R^(1/3) s_T^(1/3) s_Q^(1/3)` | `(23, 14, 27, 11); (14, 14, 12, 7)` | 1/4 |
| 20 | `r_S s_T s_Q` | `(18, 2, 15, 19); (8, 0, 0, 5)` | 3/2 |
| 21 | `r_S s_R^(1/2) s_T^(1/2) s_Q^(1/2)` | `(22, 8, 31, 25); (11, 5, 13, 6)` | 2/3 |
| 22 | `r_S s_R s_Q` | `(15, 15, 28, 7); (3, 13, 15, 0)` | 1/3 |
| 23 | `r_S s_R s_T` | `(8, 10, 17, 16); (0, 10, 2, 6)` | 1 |
| 24 | `r_S r_Q` | `(16, 0, 19, 6); (11, 0, 12, 0)` | 5/2 |
| 27 | `r_R^(1/3) r_T^(1/3) r_Q^(1/3) s_R^(1/3) s_S^(1/3) s_T^(1/3)` | `(19, 22, 20, 22); (5, 10, 9, 15)` | 1/6 |
| 28 | `r_R^(1/3) r_T^(2/3) s_R^(1/3) s_S^(1/3) s_Q^(1/3)` | `(14, 27, 14, 23); (3, 13, 11, 4)` | 1/3 |
| 29 | `r_R^(1/3) r_S^(1/3) r_Q^(1/3) s_S^(1/3) s_T^(1/3) s_Q^(1/3)` | `(22, 22, 32, 19); (13, 7, 15, 4)` | 7/12 |
| 30 | `r_R^(1/3) r_S^(1/3) r_T^(1/3) s_R^(1/3) s_T^(1/3) s_Q^(1/3)` | `(5, 12, 15, 29); (1, 12, 5, 12)` | 1/3 |
| 31 | `r_R^(1/2) r_Q^(1/2) s_S^(1/2) s_T^(1/2)` | `(9, 30, 22, 19); (7, 12, 9, 13)` | 1/6 |
| 32 | `r_R^(1/2) r_T^(1/2) s_S^(1/2) s_Q^(1/2)` | `(11, 16, 11, 22); (7, 0, 10, 7)` | 7/6 |
| 33 | `r_R^(1/2) r_T^(1/2) s_R^(1/4) s_S^(1/4) s_T^(1/4) s_Q^(1/4)` | `(15, 24, 18, 19); (0, 14, 10, 11)` | 1/12 |
| 34 | `r_R^(1/2) r_T^(1/2) s_R^(1/2) s_T^(1/2) s_Q^(1/2)` | `(16, 31, 10, 20); (0, 14, 3, 10)` | 1/4 |
| 35 | `r_R^(1/2) r_T^(1/2) s_R^(1/2) s_S^(1/2) s_T^(1/2)` | `(18, 16, 9, 28); (9, 5, 0, 15)` | 1/4 |
| 37 | `r_R^(1/2) r_S^(1/2) s_T^(1/2) s_Q^(1/2)` | `(10, 14, 20, 11); (9, 7, 2, 3)` | 1/2 |
| 40 | `r_R^(2/3) r_T^(1/3) s_S^(1/3) s_T^(1/3) s_Q^(1/3)` | `(13, 20, 15, 20); (10, 14, 9, 7)` | 1/3 |
| 41 | `r_R s_T s_Q` | `(6, 31, 27, 16); (4, 13, 10, 2)` | 1/2 |
| 42 | `r_R s_S^(1/2) s_T^(1/2) s_Q^(1/2)` | `(0, 22, 14, 23); (0, 9, 11, 7)` | 1/6 |
| 43 | `r_R s_S s_Q` | `(6, 27, 21, 14); (1, 9, 15, 3)` | 3/2 |
| 44 | `r_R s_S s_T` | `(2, 12, 18, 18); (1, 4, 1, 11)` | 3 |
| 47 | `r_R r_T` | `(6, 15, 1, 21); (4, 14, 1, 7)` | 5/2 |

Dominating pairs below mean left monomial is >= right monomial for every regular statistic.

| Redundant ID and term | Dominating ID and term |
|---|---|
| 9: `r_T r_Q s_S` | 0: `r_Q s_S s_T` |
| 10: `r_T r_Q s_R` | 2: `r_Q s_R s_T` |
| 18: `r_S^(1/2) r_T^(1/2) r_Q^(1/2) s_R^(1/2)` | 4: `r_T^(1/2) r_Q^(1/2) s_R^(1/2) s_S^(1/2)` |
| 25: `r_S r_T s_Q` | 5: `r_T s_S s_Q` |
| 26: `r_S r_T s_R` | 8: `r_T s_R s_S` |
| 36: `r_R^(1/2) r_T^(1/2) r_Q^(1/2) s_S^(1/2)` | 4: `r_T^(1/2) r_Q^(1/2) s_R^(1/2) s_S^(1/2)` |
| 38: `r_R^(1/2) r_S^(1/2) r_Q^(1/2) s_T^(1/2)` | 15: `r_S^(1/2) r_Q^(1/2) s_R^(1/2) s_T^(1/2)` |
| 39: `r_R^(1/2) r_S^(1/2) r_T^(1/2) s_Q^(1/2)` | 17: `r_S^(1/2) r_T^(1/2) s_R^(1/2) s_Q^(1/2)` |
| 45: `r_R r_Q s_T` | 2: `r_Q s_R s_T` |
| 46: `r_R r_Q s_S` | 3: `r_Q s_R s_S` |
| 48: `r_R r_S s_Q` | 22: `r_S s_R s_Q` |
| 49: `r_R r_S s_T` | 23: `r_S s_R s_T` |

## Equality matrices rebuilt independently

For every one of the 38 retained vertices and each n=2,3,4, the verifier sets multiplicity n on every tight arc in the reduced9 family and 1 on the other arcs. It constructs each endpoint as an explicit tuple of coordinate values; each relation is built by testing agreement on the shared coordinates. It does not fill matrices using the asserted cardinality or norm formulas.

The output is counted from these explicit relations by separately computing the integer two-path matrices RS and TQ and summing `sum_(x,z) RS[x,z] TQ[z,x]`. This is an independent finite count; it is compared afterwards with `product_A n_A`.

All row degrees and column degrees are directly counted from the explicit relation. Each matrix is biregular with row degree a and column degree b. Cauchy-Schwarz gives `||A||^2 <= ab`; constant vectors give equality, so this certifies its squared norm exactly without numeric eigenvalue estimates. It is then compared with `product_(|A intersect e|=1) n_A`. All cardinalities are counted and compared with their products too.

Finally, the monomial equality is verified as an integer identity after raising to power 12: `Out^12 = product_e |e|^(12 lambda_e) s_e^(12 mu_e)`. No floating-point numbers appear.

**114 explicit matrix instances pass all four checks** (cardinality, exact norm, output, active-monomial equality). The maximum endpoint dimension is 256. The exact output distributions are:

| Common multiplicity n | Output: number of retained terms giving that output |
|---:|---|
| 2 | 16:12, 32:8, 64:6, 128:12 |
| 3 | 81:12, 243:8, 729:6, 2187:12 |
| 4 | 256:12, 1024:8, 4096:6, 16384:12 |

Each of the 114 records, including dimensions, all four sizes, all four squared norms, output, and tight-arc indices, is retained in the JSON.

## Corrections and paper-ready formulation

1. There are **10 D4 orbits**, not nine. Orbit A splits into an orbit of size 8 (chosen norm edges adjacent) and an orbit of size 4 (chosen norm edges opposite). The other orbit sizes are B:4, C:2, C':4, D:2, E:4, F:4, G:4, H:2. Their total is 38.
2. The triple arcs are unnecessary even for the integer construction. Describing the 13-arc family remains correct; reduced9 is a simpler sufficient family.
3. The original rounding proof contains the literal expression `n_full product_A n_A = U4`, which double-counts the full arc if A ranges over all arcs. It must read `product_all_arcs n_A = U4`, or `n_full product_nonfull_arcs n_A = U4`. This is a notation typo; the preceding size constraint gives the corrected inequality directly.

Suggested statement:

> Let A be the nine connected subsets of a labelled 4-cycle consisting of its four singletons, four adjacent pairs, and the full vertex set. For regular clipped statistics, the optimum of the arc-factor logarithmic packing LP equals log U4, where U4 is the minimum of the 38 monomials in Table [...]. The LP dual has 50 vertices; 12 are dominated on the regular cone, and the other 38 form ten dihedral orbits. Each of the 38 has an open region of unique optimality and is attained by an integer arc family. Consequently none can be removed while retaining a universal constant-factor formula. The same optimum is obtained upon adjoining the four triple arcs, for both real and integer multiplicities.

This audit verifies the LP and its equality constructions. Validity of the 38 upper bounds for arbitrary binary relations and the universal factor16 rounding argument are separate analytic claims.

## Full13 matrix cross-checks

Five additional explicit matrix instances exercise the triple-arc factors; all cardinality, exact norm, and independently counted output formulas pass. This brings the construction count to 119.

| Multiplicities | Dimensions | Cardinalities (R,S,T,Q) | Squared norms | Output |
|---|---|---|---|---:|
| all13_twos | `[128, 128, 128, 128]` | `[1024, 1024, 1024, 1024]` | `[64, 64, 64, 64]` | 8192 |
| triples_2 | `[8, 8, 8, 8]` | `[16, 16, 16, 16]` | `[4, 4, 4, 4]` | 16 |
| triples_3 | `[27, 27, 27, 27]` | `[81, 81, 81, 81]` | `[9, 9, 9, 9]` | 81 |
| triples_4 | `[64, 64, 64, 64]` | `[256, 256, 256, 256]` | `[16, 16, 16, 16]` | 256 |
| mixed | `[48, 48, 72, 72]` | `[288, 432, 288, 288]` | `[36, 54, 16, 24]` | 1728 |

The mixed multiplicity vector, in singleton0..3, pair0..3, triple0..3, full order, is `(2,3,1,2,1,2,3,1,2,1,3,2,2)`. In the triples_n cases only the four triple arcs have multiplicity n.