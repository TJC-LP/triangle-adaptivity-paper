# Independent upper-bound and proof audit

Sources read: the paper's §§2, 3, and 5.1 in `spectral_agm.typ`; the original Fable report embedded in `../P3-spectral-verify-astra/task.md`, lines 18 onward. No solver or earlier-verifier program was executed or imported. All code in `proof_exact.py` was independently written and run as `python3 -I proof_exact.py > proof_exact.out`; it uses integers and `Fraction` only. This audit handles the analytic upper bounds and auxiliary formulas; the root audit separately handles exhaustive/random instances and the LP/rounding enumeration.

## Verdict

**T1 is proved.** The 38 separate inequalities follow from the displayed analytic arguments after adding routine zero-matrix cases. Lemma Lambda, F2, H3, and the dyadic/tensor proof of G are valid. No counterexample or substantive upper-bound proof gap was found.

**The T4 counterfamily is proved with an exact stronger description:** for every `1 <= t <= L`,

\[
U_4((L,t,L,L),(t,t,t,L))
=\min\{t^3,\sqrt{Lt^3}\}.
\]

Thus `L >= t^3` is the exact threshold for the asserted value `t^3`. The earlier condition `L >= t^2` is insufficient. A fixed `L=8` works simultaneously for all `1 <= t < 2`; no limit `L -> infinity` is needed.

**The kite and single-pair tightness examples are proved.** The quoted output 972 is correct. There are several minor proof/description repairs below, including a duplicated full-arc factor in the rounding display and an incomplete description of the T5 arc realization.

## Line-by-line analytic check

### Setting, clipping, and zero cases

The paper uses sets and binary incidence matrices, cardinality upper bounds, and operator norm upper bounds. These are essential. The output is a tuple count, unrelated to the per-binding execution cost `C`; the 4-cycle result does not by itself establish a 4-cycle algorithmic work bound. Nothing from the paper's min-side operation model is used in T1.

For a binary matrix, squared column/row Euclidean norms are column/row degrees, and the squared Frobenius norm is its number of ones. Therefore all degrees are at most the squared operator norm and all squared operator norms are at most cardinalities. Replacing actual sizes and squared norms by `r_e` and `s_e` is valid by coordinatewise monotonicity.

If any relation is empty, the output is zero and all upper bounds hold. This case should be explicitly removed before dividing by `sigma_R` in Lemma Lambda, taking logarithms of cardinalities in G, or choosing Perron vectors. For nonempty relations all norms and cardinalities are at least one. Infeasible negative input bounds need the paper's existing empty-class convention and should not be inserted into radical monomials; the theorem should state nonnegative statistics, with regularity for the lower bound.

### A, B, C/C', D, and E

**A, 12 inequalities — proved.** For a fixed R-edge, its extensions are bounded by each of `d_S^+(y) Delta_T^+`, `d_S^+(y)d_Q^-(x)`, and `d_Q^-(x)Delta_T^-`. These are valid counts obtained by independently choosing successive or opposite remaining vertices. Bounding degrees by squared norms and summing over R gives the three listed terms. Rotation gives all twelve. A is two dihedral orbits, of sizes eight and four, not a single orbit.

**B, four inequalities — proved.** For an R-edge, the extension count is `1_{N_S(y)}^T A_T 1_{N_Q(x)}`. The operator norm inequality gives `sigma_T sqrt(d_S^+(y)d_Q^-(x))`, bounded by `sqrt(s_S s_T s_Q)`. Sum over R and rotate.

**C/C', six inequalities — proved.** For adjacent operator-norm positions R,S, trace/Frobenius Cauchy–Schwarz and matrix norm submultiplicativity give

\[
\mathrm{Out}\le\|A_RA_SA_T\|_F\|A_Q\|_F
\le\sigma_R\sigma_S\sqrt{|T||Q|}.
\]

For opposite operator-norm positions R,T, split the trace into `(A_R A_S)(A_T A_Q)` and bound each factor in Frobenius norm. This yields `sigma_R sigma_T sqrt(|S||Q|)`. These are all six placements. The report names C/C' by the *cardinality* pair; complementing pairs preserves adjacent/opposite status, so its proof ordering causes no algebraic discrepancy.

**D, two inequalities — proved.** An output tuple is determined by its two opposite edges. Injectivity gives the two products of opposite cardinalities.

**E, four inequalities — proved.** Forgetting Q injects the output tuples into 3-paths. Their count is `(d_R^-)^T A_S d_T^+`. Apply the operator bound and `sum d^2 <= Delta sum d <= sigma^2 |e|`. Reversing the path does not create additional terms; rotation gives exactly four.

### Lemma Lambda

**Proved, including disconnected support S.** Let `rho=A_R^T A_R`, `tau=A_T A_T^T`, indexed as in the report. Restrict to nonempty connected components of the binary bipartite support of S. On each component choose strictly positive left/right singular vectors `p,q` and singular value `sigma_c`. Components containing no edges never index K.

For `s=(y,z)` set `theta_s=sqrt(q_z/p_y)`. These weights need not have a common normalization across components. Every pair of S-edges, even in different components, satisfies

\[
\sqrt{\rho_{yy'}\tau_{zz'}}
\le \tfrac12\big(\kappa\theta_s\theta_{s'}\rho_{yy'}
+\kappa^{-1}(\theta_s\theta_{s'})^{-1}\tau_{zz'}\big).
\]

This is scalar AM–GM: the product of the two terms is exactly `rho tau`. Since K is symmetric and entrywise nonnegative, it suffices to test nonnegative unit vectors u. Multiplying by `u_su_s'` and summing is legitimate.

The first quadratic form groups to `U^T rho U`, where `U_y=sum_z u_yz theta_yz`. Rowwise Cauchy–Schwarz gives

\[
U_y^2\le \frac{1}{p_y}\Big(\sum_{z\in N_S(y)}u_{yz}^2\Big)
\Big(\sum_{z\in N_S(y)}q_z\Big)
=\sigma_{c(y)}\sum_z u_{yz}^2.
\]

Thus `||U||^2 <= sigma_S ||u||^2`. The second form gives `V^T tau V` with `||V||^2 <= sigma_S ||u||^2`. Cross-component entries of rho and tau pose no issue: their full quadratic forms are bounded by their global operator norms. Consequently

\[
u^TKu\le\tfrac12(\kappa\sigma_R^2+\kappa^{-1}\sigma_T^2)\sigma_S.
\]

Taking `kappa=sigma_T/sigma_R` proves the claim. If R or T is empty, K is zero and this division is skipped.

The Perron assertion is valid: on a connected nonempty bipartite component the left Gram matrix is irreducible on its nonisolated row vertices, and the right vector obtained from `A_S^T p/sigma_c` is positive. Bipartite periodicity does not invalidate this argument.

### F2 and F

**Proved.** For the integer 3-path count matrix `M=A_R A_S A_T`, expand two of the three copies in `M_xw^3` as ordered S-edge choices. Summing the remaining copy M over x,w gives exactly

\[
\sum_{x,w}M_{xw}^3
=\sum_{s,s'\in S}1_{X_{ss'}}^T M 1_{W_{ss'}}.
\]

This is an identity, including repeated S-edges and the diagonal `s=s'`. Binary entries ensure products of incidences equal intersection indicators. Every summand is at most `||M|| sqrt(|X||W|) <= sigma_R sigma_S sigma_T K_ss'`. Summing gives `sigma_R sigma_S sigma_T 1^T K 1`, bounded by `|S| sigma_R sigma_S sigma_T lambda_max(K)`. Lambda completes F2.

Holder on the Q-edge set gives

\[
\mathrm{Out}^3\le |Q|^2\sum_{(w,x)\in Q}M_{xw}^3
\le |Q|^2|S|\sigma_R^2\sigma_S^2\sigma_T^2.
\]

The omission of the S-norm or its position would change the inequality; the report's displayed term has the correct positions. The four rotations give exactly four F terms.

### H3 and H

**Proved.** The S-by-Q matrix `B_(y,z),(w,x)=A_R(x,y)A_T(z,w)` is binary, and summing all its entries counts output tuples once. Its Gram entry is the number of Q-edges between the R common-neighbor set and T common-neighbor set. Hence

\[
(BB^T)_{ss'}\le \sigma_Q\sqrt{\rho_{yy'}\tau_{zz'}}=\sigma_QK_{ss'}.
\]

Entrywise domination implies domination of the largest eigenvalue for symmetric nonnegative matrices, even though K need not be positive semidefinite. Therefore `||B||^2 <= sigma_Q lambda_max(K) <= sigma_R sigma_S sigma_T sigma_Q`. Operator Cauchy–Schwarz on `1_S^T B 1_Q` gives the stated H term. Rotation gives the second opposite pair.

**Weighted-real extension — refuted as asserted.** For `A_R=A_T=I_2`, `A_S=A_Q=I_2/2`, interpreting `r_e=||A_e||_F^2` and `s_e=||A_e||^2`, exact computation gives

`r=(2,1/2,2,1/2)`, `s=(1,1/4,1,1/4)`, `Out=1/2`, `H=1/4`.

The code certifies `Out^4=1/16 > H^4=1/256`. The report should explicitly state the Frobenius-squared interpretation of `r` when discussing real matrices; cardinality of a weighted matrix is otherwise ambiguous.

The sentence “the 0/1 structure enters only through Lemma 0(vi)” is too strong. Perron vectors exist for general nonnegative matrices too; the needed special fact is the *unweighted support* identity `sum_{z in N(y)}q_z=sigma_c p_y`. Also the F2/H3 indicator and neighborhood identities use 0/1 entries. Replace that sentence with “The support identities and incidence expansions in these proofs use the 0/1 hypothesis.”

### G and tensor powers

**Proved.** The buckets partition precisely the R-edges on which both relevant degrees are positive. All removed edges lie on no output cycle. For each bucket the nonnegative matrix `h=A_Q A_Rjk A_S` satisfies

\[
\mathrm{Out}_{jk}\le\min(\|h\|_1,\sqrt{|T|}\|h\|_F)
\le(|T|\|h\|_1\|h\|_F^2)^{1/3}.
\]

Here `||h||_1` means the *entrywise sum*, not the induced matrix 1-norm. The report marks it as `ell_1`; retain that distinction in the paper.

The identities/bounds are `||h||_1 <= 2^(j+k+2)|R_jk|` and `||h||_F <= sigma_Q sigma_S sqrt(|R_jk|)`. If `X_jk,Y_jk` are touched vertices, then `|R_jk| <= 1_X^T A_R 1_Y <= sigma_R sqrt(|X||Y|)`; this avoids any implicit appeal to spectral monotonicity of masked matrices. The lower bucket endpoints give `2^j |X| <= |Q|`, `2^k |Y| <= |S|`. Combining yields the factor 4 exactly, then at most `(1+log_2|Q|)(1+log_2|S|)` buckets.

The tensor argument is fully valid. Binary matrices remain binary under Kronecker powers; output, each cardinality, and each operator norm multiply. For a fixed nonempty instance, the prefactor is at most polynomial in the tensor exponent n, so its nth root tends to one. This removes both 4^(1/3) and the logarithmic factor. No hidden degree-dependent constant remains, and no assertion about convergence of chosen partitions is needed. The remaining three G terms follow by rotating the omitted r-position and opposite omitted s-position together.

## Arc identities and descriptive repairs

Each arc coordinate is independent, and connectedness of the arc forces all its participating vertices to use one common coordinate around the cycle. Thus the product formula for Out is exact. Matrix factors are identity, one-sided all-ones vectors, or scalar 1; their numbers of ones and squared norms give the claimed formulas.

Triple arcs are unnecessary in a stronger sense than numerical agreement of dual lists. Every triple meets all four edges, just as the full arc does, and contributes to two norm constraints while the full arc contributes to none. Moving its multiplicity to the full arc preserves all sizes and output and weakly decreases all norms. This works for both real and integer multiplicities. Thus the reduced nine-arc family and full thirteen-arc family have exactly the same real and integer optima.

The report's complementary-slackness argument is correct. A construction supported on tight arc constraints saturates its chosen monomial at its own statistics. No fractional/cardinality rounding is needed for this separate assertion.

The report's §5.1 rounding display duplicates the full-arc factor. Its inequality should read

\[
r_e\prod_{A\cap e=\varnothing}n_A
\ge n_V\prod_{A\ne V}n_A=U_4,
\]

not `n_V prod_A n_A=U4`. The intended inequality follows immediately from the size constraint and is otherwise sound. This typo does not affect the factor 16 proof.

In the T5 matching example, the tight term is C with cardinality pair `{S,Q}`, not C'. Its exact realization needs `n_{X}=n_{Y}=n_{ZW}=n`, all other multiplicities one. The lone `{Z,W}` arc has dimensions `(1,1,n,n)` and output n; it is not literally the stated n-by-n example without the two singleton factors.

## Exact kite checks

For singleton multiplicities `(a,b,c,d)`, pair multiplicities `p=n_YZ`, `q=n_WX`, and full multiplicity m, direct rebuilding gives

\[
r=m(abpq,bcp,cdpq,daq),\qquad
s=(abpq,bc,cdpq,da),\qquad
\mathrm{Out}=mabcdpq.
\]

For every positive integer choice, the following four terms equal Out: C with cardinality pair `{R,T}`, H with pair `{S,Q}`, G omitting `r_R,s_T`, and G omitting `r_T,s_R`. When q=1 the F term `(r_S r_Q^2 s_R s_S s_T)^(1/3)` also equals Out. So the arbitrary-singleton assertion is valid, not just the symmetric example.

| `(a,b,c,d,p,q,m)` | Exact r | Exact s | Out = U4 |
|---|---|---|---:|
| `(1,1,1,1,2,2,1)` | `(4,2,4,2)` | `(4,1,4,1)` | 4 |
| `(2,3,1,2,2,3,1)` | `(36,6,12,12)` | `(36,3,12,4)` | 72 |
| `(3,2,3,2,3,3,3)` | `(162,54,162,54)` | `(54,6,54,6)` | 972 |
| `(2,1,2,3,2,1,2)` | `(8,8,24,12)` | `(4,2,12,6)` | 48 |

These are actual coordinate-level binary matrices and direct integer matrix-product traces. Their norm certificates are exact: each relation is biregular, so the constant singular vectors and the Schur upper bound agree, giving squared norm `(row degree)(column degree)`.

## Exact T4 threshold and clipping improvement

For the original T4 family, every term is `L^a t^b`. The exact exponent check establishes `a>=0`, `a+b>=2`, and `3a+b>=3` for all 38 terms. On `1<=L<=t^3` with `L>=t`, comparing exponents at the two endpoints shows every term is at least `sqrt(L t^3)`. Above `L=t^3`, monotonicity gives at least `t^3`. The A and C terms attain these two candidate values. This proves the exact envelope, not merely sampled agreement.

| t | Exact threshold t^3 | Smallest integral L |
|---:|---:|---:|
| 3/2 | 27/8 | 4 |
| 7/4 | 343/64 | 6 |
| 15/8 | 3375/512 | 7 |
| 31/16 | 29791/4096 | 8 |
| 63/32 | 250047/32768 | 8 |

At `L=t`, `L=t^2`, `L=t^3`, and `L=10^6` for all five t values, the program checks the exact twelfth-power formula `U4^12=min(t^36,(Lt^3)^6)`. Full rational numbers are in `proof_exact.out`. For instance at `t=3/2,L=9/4`, `U4^12=205891132094649/1073741824`, whereas the incorrect asserted `t^3` would have twelfth power `150094635296999121/68719476736`.

The clipping corollary is valid because the admissible classes coincide exactly after setting unconstrained `s_e=r_e`. Its stated condition for the lower bound 8 can be strengthened from three known norms to **any two known norms**:

* For opposite known positions `{R,T}`, use the original family with L=8. S's norm bound is already implied by `|S|<=t`; Q is unconstrained. A singleton S-edge and degree bounds on R,T force W=1.
* For adjacent known positions `{R,S}`, take `r=(8,8,8,t)`, `s=(t,t,8,t)`. Q has at most one edge; successive R and S extensions each have degree at most one, again forcing W=1. The exact exponent test gives `U4=t^3` here too. Symmetry covers every adjacent pair, and adding known norms cannot invalidate the witness statistics.

The adjacent case was checked exactly at t=`3/2,7/4,15/8,31/16`; all have `U4^12=t^36`. Thus the universal constant for any known-norm subset of cardinality at least two is at least 8. This is a strengthening, not a repair required for the original corollary.

## Auxiliary refuted proof routes

The double-star warning is correct. Independently construct a symmetric binary matrix whose first row and column are all ones, with `m(m-1)` leaves and all other entries zero. It has positive eigenvector `(m,1,...,1)`, top eigenvalue m, other nonzero eigenvalue `-(m-1)`, and squared norm m². Exact outputs:

| m | Matrix dimension | Delta+ Delta- | sigma² |
|---:|---:|---:|---:|
| 2 | 3 | 9 | 4 |
| 3 | 7 | 49 | 9 |
| 4 | 13 | 169 | 16 |
| 7 | 43 | 1849 | 49 |

The unbounded degree-product-sum warning is also correct. With k core rows/columns joined by `K_kk`, and k² private leaves on each core row/column, direct binary rebuilding gives `r=k²(2k+1)` and `sum_(x,y in R) d+(x)d-(y)=k^4(k+1)(k+3)`. Squared norm is `k²(3+sqrt(5))/2`, the largest root of `z²-3k²z+k^4`; thus the ratio to `r sigma²` is larger than the exact rational `(k+1)(k+3)/(3(2k+1))`, which diverges. Program outputs `(k,r,weighted)` equal `(1,3,8)`, `(2,20,240)`, `(4,144,8960)`, `(8,1088,405504)`.

The report's other numerical failed candidates have no explicit construction in its narrative and are not used in any theorem. Their precise annealing ratios are historical search claims, not proved by this audit; they should not be treated as mathematical certificates without publishing the actual matrices.

## Paper-ready corrected proposition

Let `1 <= t < 2` and `L >= t`. For cardinality bounds `(L,t,L,L)` and clipped squared-norm bounds `(t,t,t,L)`, the worst-case labelled 4-cycle output is exactly 1, and

\[
U_4=\min\{t^3,\sqrt{Lt^3}\}.
\]

In particular, choosing `L=8` gives `W/U_4=t^{-3}->1/8` as `t->2^-`. Consequently no universal lower-bound denominator smaller than 8 is possible. The same obstruction applies when norms are supplied on any subset of at least two relations, using the adjacent-pair variant above when needed.

For the upper theorem, state binary set relations, define the 38 terms with the exact opposite-position condition in G, count ten D4 orbits (splitting A), and include a sentence handling empty relations. With these presentation repairs, all analytic upper inequalities have constant one.
