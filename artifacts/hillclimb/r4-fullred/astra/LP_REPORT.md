# Independent live-gadget exponent and LP audit

Status: the global **1/10 cap within the live-gadget design is proved** after adding a missing cost lemma. The stated **1/11 at slope 1 is not the optimum of the unpadded three-gadget design**. It is the optimum of a size-budget relaxation. It becomes an attainable fully reduced lower bound when isolated triangles are explicitly added.

All executable files here were written independently and run with `python3 -I`. Solver scripts were read only, never imported or executed. Arithmetic in `lp_audit_exact.py` is `Fraction` throughout; each optimum is checked against an exact dual certificate (nonnegative inequality multipliers, `A^T y >= objective`, and equality of primal and dual values). `lp_audit_general.py` uses exact integers/Fractions. It evaluates independently derived formulas; literal relation reconstruction is the root verifier's separate lane.

## 1. What the supplied LP actually optimizes

Let the three gadgets have parameter exponents `(P_i,Q_i,T_i,G_i,K_i,W_i)`. Write `c_i=P_i+Q_i+T_i`. Their scripts constrain an objective `c <= c_i` for every `i`; `c` initially models a certified lower bound, not the actual work. Therefore a cap on that LP by itself does not cap actual work.

This is repairable. With `z=pt/g` and gadget size `N_g`, the exact per-root formulas give

- `C_x <= pqt + 3N_g`;
- `C_y <= (3/2)N_g`;
- `C_z <= 2N_g`.

For the second bound, select the `z` traversal at each original `y`, use `min(p,g+q/k)<=g+q/k`, and sum: `C_y <= N_g+qt <= (3/2)N_g`. For the third, select the `y` traversal at each `z2`; this gives `C_z <= N_g+zq <= 2N_g`. In the first, the original-vertex contribution is at most `pqt+2pq+qt`; helpers contribute at most `zq+zq/w`.

Consequently, for a disjoint union of three rotated gadgets,

`min_i p_i q_i t_i <= C <= 3N + min_i p_i q_i t_i`.

Thus the LP correctly models every **positive** gap exponent once this lemma is supplied. An exact grid of 26,382 valid parameter tuples (`p<=30`, `q,w<=12`) satisfied these three upper bounds with zero violations. This formula check supplements, rather than replaces, the algebraic proof.

## 2. Exact certificates for the global cap

For one gadget write `c=P+Q+T` and retain four forward norm monomials

`a=P+2Q`, `b=Q+2T`, `d=P+T+G`, `r=2P+2T-2G-Q`.

The size monomial `s=P+Q+T-G` is at most the normalized size exponent 1. Two exact identities are

`11c = 5a + (5/2)b + 3d + (3/2)r`,

`c = (3/8)s + (1/4)a + (1/8)b + (3/8)d`.

Sum these identities over the three cyclic rotations. Global forward norm exponents bound each assigned norm monomial; each global norm appears with the same total weight. If `m` is their average, and `c_*` is the minimum designated-cost exponent, then

`c_* <= 12m/11`, and `c_* <= 3/8 + 3m/4`.

Every fully reduced instance has `m>=1` because output is at least `N/3`. Hence

`c_* - m <= min(m/11, (3-2m)/8) <= 1/10`.

Equality requires `m=11/10`. These inequalities cover unequal parameters in the three rotated gadgets; no symmetry assumption is needed.

For the reverse branch, the monomials `2P+Q`, `P+T-G+2Q`, and `P+2T` sum to `3c+(P-G)>=3c`. Summing rotations gives `c_*<=m_reverse`. Thus a controlling reverse bound yields no positive gap.

The independent exact LP reproduces: forward optimum `1/10` at `c=6/5,m=11/10`; reverse optimum `0`. A forward optimizer is `(P,Q,T,G)=(1/2,3/10,2/5,1/5)` in all three copies. These facts are **proved**, with exact identities stronger than finite numerical evidence.

## 3. The fixed-slope normalization error

The supplied LP has all size exponents **at most** 1, but does not force any to equal 1. Its fixed `m=1` optimum is `c=12/11`, achieved at `(P,Q,T,G)=(5,3,4,2)/11`. The actual maximum size exponent is `10/11`. The corresponding construction has actual slope `(1)/(10/11)=11/10`, not 1.

For any valid live gadget, the dominant size exponent is exactly

`max(P+Q, P+T, P+Q+T-G)`.

All other size terms are dominated using nonnegative `K,W` and `G<=P`. In the three-gadget union some one of these nine terms must equal 1. Cyclic symmetry reduces the extra finite check to three alternatives in gadget zero. Our exact LP imposed each equality and checked exact dual certificates.

| Claimed fixed slope | Original relaxed forward gap | Forward gap with actual `N` normalization |
|---|---:|---:|
| `1` | `1/11` | `0` |
| `21/20` | `21/220` | `59/660` |
| `11/10` | `1/10` | `1/10` |
| `23/20` | `7/80` | `7/80` |
| `6/5` | `3/40` | `3/40` |
| `5/4` | `1/16` | `1/16` |
| `13/10` | `1/20` | `1/20` |
| `7/5` | `1/40` | `1/40` |
| `3/2` | `0` | `0` |

At slope 1 the three forward alternatives have designated gap optima `-1,-1/8,0`. The backward alternatives are `-1,-1/2,infeasible`; the actual work's possible linear-size contribution only restores an upper bound of zero positive gap. Nonzero dual multipliers for the three forward alternatives are saved in `lp_audit_certificates.out`.

Therefore **refuted as stated** if “gives 1/11 at kappa=1” means the optimum attained by exactly three unpadded live gadgets. It is **proved** if explicitly described as the original relaxed LP value/upper cap, without asserting that it is an attained fixed slope in that design.

## 4. Constructive repair using live padding

Take the three rotations of `L(v^5,v^3,v^4,v^2,v,1)` and add `v^11` pairwise disjoint isolated triangles. This preserves full reduction. It changes `N` by `3v^11`, every root cost by `2v^11`, output by `v^11`, and each of the six squared-degree sums by `v^11`. Therefore

`N=Theta(v^11)`, `B2=Theta(v^11)`, `C=Theta(v^12)`.

The gap exponent is indeed `1/11` at actual slope 1. More generally, scaling the core exponents to `(5,3,4,2,1,0) kappa/11` and adding isolated triangles of size exponent 1 yields gap `kappa/11` for every `kappa in [1,11/10]`. Integer powers and bounded rounding errors implement real slopes. This is an added construction, outside the original “three rotated live gadgets, any parameters” design description.

Exact padded-family evaluations:

| `v` | Added triangles | `N` | `C` | `Out` | forward sum | reverse sum | exact `C/(N+B2)` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 2048 | 17424 | 17840 | 7808 | 33872 | 34000 | `1115/3206` |
| 3 | 177147 | 1044171 | 1321272 | 439587 | 2894211 | 5330205 | `8156/24311` |
| 4 | 4194304 | 20795136 | 32097536 | 8372224 | 68161792 | 211699456 | `125381/347488` |
| 5 | 48828125 | 218683125 | 402503750 | 85390625 | 791031875 | 3766489375 | `322003/807772` |

## 5. General live exponents and real slopes

Status: **proved** for integers `i>=1`, `j>=0`, `5j<=4i`, `u>=2`, taking all three rotations. Parameters are

`(p,q,t,g,k,w)=(u^(4i),u^(4i-2j),u^(4i-j),u^(4i-3j),u^j,1)`.

The divisibility conditions hold. `z=pt/g=u^(4i+2j)`. The dominant size exponent is `8i`; the designated-cost exponent is `12i-3j`. Forward norm exponent candidates reduce to

`12i-4j, 8i+j, 4i+6j, 8i, 4i+j, 4i-j`.

All are at most `12i-4j` precisely under the stated sufficient condition `5j<=4i`. Each rotated sum contains a term with exponent `12i-4j`. Reverse sums have exponent `12i-2j`, so `B2=Theta(u^(12i-4j))`. Combined with the cost lemma, `C=Theta(u^(12i-3j))`.

Thus `kappa=3/2-j/(2i)` and the cost exponent is `(3+6kappa)/8` on `[11/10,3/2]`. The reverse value need not exceed the forward value at each finite size; the endpoint `j=0` below is a counterexample to that stronger, unnecessary assertion. Both have the required common asymptotic exponent there.

Exact independent closed-form results:

| `(i,j,u)` | `N` | `C` | `Out` | forward sum | reverse sum | `B2` |
|---|---:|---:|---:|---:|---:|---:|
| `(1,0,2)` | 5520 | 8512 | 3072 | 38448 | 22608 | 22608 |
| `(2,1,2)` | 692352 | 2697600 | 368640 | 10175104 | 13960832 | 10175104 |
| `(3,2,2)` | 130759680 | 1184240640 | 66846720 | 2785035264 | 13084204032 | 2785035264 |
| `(5,4,2)` | 7024690790400 | 287335192264704 | 3518383521792 | 264982319136768 | 13516511458295808 | 264982319136768 |

Additional exact `(5,4,3)` and `(10,7,2)` values are in `lp_audit_general.out`.

For real `kappa in [11/10,3/2]`, take `u=2,i=n,j=floor((3-2kappa)n)`. The feasibility condition remains valid, and all deviations from the target exponents are bounded by constants independent of `n`. The finite number of positive monomial terms gives uniform multiplicative constants. Thus `B2=Theta(N^kappa)` and `C=Theta(N^((3+6kappa)/8))`, including irrational slopes. For the endpoint `3/2`, use `j=0` (or complete tripartite graphs). No continuity assumption on an unknown extremal function is needed.

## Paper-ready replacement

> For a disjoint union of three cyclic rotations of the live gadget, allowing different valid parameters in each copy, the gap exponent against `N+B2` is at most `1/10`, and this value is attained at slope `11/10`. Indeed, its cost is between the minimum of the three designated products `p_i q_i t_i` and that minimum plus `3N`; the forward exponent constraints imply `c<=12kappa/11` and `c<=3/8+3kappa/4`, while a controlling reverse bound implies `c<=kappa`. The fixed-size-budget LP has value `1/11` at budget slope 1, but it does not enforce the actual size exponent. To attain gap `1/11` at actual slope 1, add `v^11` disjoint isolated triangles to the three rotations of `L(v^5,v^3,v^4,v^2,v,1)`. More generally this padding gives gap `kappa/11` for every real `kappa in [1,11/10]`. The unpadded general family with `5j<=4i` attains cost exponent `(3+6kappa)/8` for every real `kappa in [11/10,3/2]`.

These results do not prove a `1/10` upper bound for **all** fully reduced instances. The global fully reduced gap remains between `1/10` and `1/8`; outside this gadget family the interval below slope `11/10` remains open.
