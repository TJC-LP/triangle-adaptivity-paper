# Independent audit: arc construction, rounding, constant obstruction, complete blocks

Verdicts: the arc formulas, factor-16 lower bound, asymptotic factor-8 obstruction, and complete-block obstruction are **proved**. The original sufficient condition `L >= t^2` for `U4=t^3` is **refuted** and has the exact replacement `L >= t^3`. The sharp universal factor remains **open-with-obstruction**. In particular, the literal rounding rule applied to an arbitrary real optimum itself has sharp factor 16, even though that does not settle the true worst-case output constant.

I read the paper's cost/statistics definitions, spectral triangle theorem, and per-binding definitions. The claims audited here concern output cardinality under size and operator-norm bounds; they are not bounds on the paper's per-binding cost or on a four-cycle join implementation.

All code was newly written in `round_independent.py`, executed using `python3 -I` from this directory. No Fable or prior-verifier script was executed or imported. Their source was read only. The original report is embedded in `../P3-spectral-verify-astra/task.md`.

## 1. Exact computational method

The script generates the 38 exponent vectors directly from their displayed formulas. Comparisons use 12th powers of monomials, hence integer/Fraction arithmetic. Arc sets and explicit relations are generated independently from the coordinate-equality definition.

The rounding checks improve on both reported implementations' treatment of real LP values: this script uses **no floating-point arithmetic at all**. A logarithmic LP right-hand side is represented as `sum_p q_p log(p)` with exact rational coefficients at primes. To compare two such expressions, denominators are cleared and the resulting rational products of integer prime powers are compared. A Bland-rule primal simplex tableau has rational coefficients and these exact logarithmic right-hand sides. Every LP output is checked for exact primal feasibility and exact equality to `log(U4)`. Algebraic multiplicities are floored by integer binary search after clearing rational exponents. No epsilon, approximate logarithm, numerical LP, or post-rounding repair is used.

The exact integer arc optimum is computed separately by exhaustive recursion over all integer multiplicities of the reduced nine-arc family. This reduction is exact: a triple meets all four edges, as does the full arc, but a triple contributes to two norm products whereas the full arc contributes to none. Replacing any triple multiplicity by an equal full-arc factor preserves all sizes and output and weakens all norm constraints. The same argument makes the four triple constraints redundant in the dual.

## 2. Arc formulas: proved

For each nonempty connected cyclic vertex set A, give every vertex in A one coordinate in `[n_A]`. Along each edge internal to A, enforce equality of that coordinate; on an edge with only one endpoint in A, it is free. Connectivity of A implies that every cycle tuple carries a single shared coordinate value for A. Different arc coordinates are independent. Consequently

`|e| = product_{A intersects e} n_A`,

`sigma_e^2 = product_{|A intersects e|=1} n_A`,

`Out = product_A n_A`.

The norm identity follows either from Kronecker factors or directly from biregularity: each constructed incidence matrix has constant row degree d and column degree d', so the all-ones singular pair gives squared norm dd', while the Schur bound gives the matching upper bound. The script rebuilds actual 0/1 edge sets, counts all four-tuples, and derives d,d' from the edge sets.

Selected exact rebuilds:

| Multiplicities | Vertex dimensions | Sizes (R,S,T,Q) | Squared norms | Out |
|---|---|---|---|---|
| All singletons 2 | (2,2,2,2) | (4,4,4,4) | (4,4,4,4) | 16 |
| All pairs 2 | (4,4,4,4) | (8,8,8,8) | (4,4,4,4) | 16 |
| All triples 2 | (8,8,8,8) | (16,16,16,16) | (4,4,4,4) | 16 |
| Full arc 3 | (3,3,3,3) | (3,3,3,3) | (1,1,1,1) | 3 |
| X=2,YZ=3,WX=2,full=2 | (8,6,6,4) | (24,6,12,8) | (12,1,6,2) | 24 |

The original kite example `(a,b,c,d,p,q,m)=(3,2,3,2,3,3,3)` gives dimensions `(27,18,27,18)`, sizes `(162,54,162,54)`, squared norms `(54,6,54,6)`, and **Out=972**. Precisely the C term with size pair R,T, the H term with size pair S,Q, and the two G terms missing size R and size T are tight. Other independent kite outputs were 128 and 72. The one-pair F-family outputs were 64,72,72; the F term `r_S r_Q^2 s_R s_S s_T` is exactly Out cubed in each case. Exact full results are in `round_examples.out`.

## 3. Factor-16 rounding: proved, with one transcription correction

Let real multiplicities n_A>=1 attain U4. Denote the full arc by V, and set `a_A=floor(n_A)` for A!=V. Let

`h = min_e r_e / product_{A!=V, A intersects e} a_A`, `m=floor(h)`.

Line-by-line audit:

1. A real optimum exists: the logarithmic LP is nonempty and closed, and every nonnegative variable is bounded by a finite size right-hand side for an edge it meets.
2. Every floored norm product weakly decreases. The full arc never appears in a norm product.
3. Original feasibility and `a_A<=n_A` imply `h>=n_V>=1`; therefore m>=1.
4. The definition of m gives all four size constraints.
5. Multiplying out the definition of h gives the exact identity
   `h product_{A!=V} a_A = min_e r_e product_{A disjoint from e} a_A`.
6. The only arcs disjoint from an edge are the two opposite singleton arcs and their joining pair arc: exactly three.
7. For each of those three factors, `floor(n)>n/2` for n>=1. Thus the product loses strictly less than 8.
8. Original size feasibility gives `r_e product_{A disjoint from e} n_A >= product_{all A} n_A = U4`.
9. Finally, `m>h/2`. Combining the last four lines gives `m product_{A!=V} a_A > U4/16`.

The original Sec. 5.1 writes the RHS at step 8 as `n_full product_A n_A=U4`, which counts the full factor twice if the product is over all arcs. Delete `n_full`, or explicitly restrict that product to non-full arcs. The intended argument above is valid.

Exact grid results:

| Grid | Points | Literal-rounding max U4/Out | Worst literal point (r;s;Out) | Integer arc max U4/Out* |
|---|---:|---|---|---|
| 1<=s_e<=r_e<=3 | 1,296 | 3; 12th power 531441 | (1,2,3,3); (1,2,2,3); 1 | 3^(2/3); 12th power 6561 |
| 1<=s_e<=r_e<=4 | 10,000 | 3*2^(1/3); 12th power 8503056 | (3,4,3,4); (2,3,2,4); 2 | sqrt(6); 12th power 46656 |

The exact-optimum worst points were `(r;s;Out*)=((2,3,3,3);(1,2,2,3);2)` and `((2,3,4,3);(1,2,3,2);2)` respectively. Every grid point had an exactly certified LP objective, feasible literal witness, and strict `16 Out>U4`.

An additional 256 random statistics vectors with `r_e<=300` and seed 20261009 all passed. The worst literal ratio was **995/143**, at `r=(25,224,199,257)`, `s=(13,194,110,176)`, `U4=4975`, `Out=715`; the rounded instance has only singleton-X multiplicity 13 and singleton-Z multiplicity 55 nontrivial. The printed exact 12th power is

`941622806914375817930331445556640625 / 73119371471655725294164801`.

These larger literal-rounding losses do not contradict the original repaired/greedily improved construction's lower empirical losses.

## 4. Factor-8 obstruction: proved; original L threshold refuted

For `r=(L,t,L,L)` and `s=(t,t,t,L)`, assume `t>=1,L>=t`. Direct substitution into all 38 monomials yields the stronger exact formula

`U4 = min(t^3, sqrt(t^3 L))`.

To verify it symbolically, write L=tu, u>=1. The C term with size pair S,Q is `t^2 sqrt(u)`, and the only term independent of L is `t^3`. Every other term, written `t^a L^b`, has `a+b>=2` and `b>=1/2`, so it is at least `t^2 sqrt(u)`. These inequalities are asserted separately for all 38 exponent vectors in the script.

It follows that `U4=t^3` **if and only if** `L>=t^3`. In particular `L=t^2` instead gives `U4=t^(5/2)` when t>1, refuting the original sufficient condition. The smallest integral L for the reported t-values is:

| t | t^3 | Smallest integral L |
|---|---|---:|
| 3/2 | 27/8 | 4 |
| 7/4 | 343/64 | 6 |
| 15/8 | 3375/512 | 7 |
| 31/16 | 29791/4096 | 8 |
| 63/32 | 250047/32768 | 8 |

The script checks the exact U4 12th power at L=t^2, L=t^3, and L=10^6 for every row. Exact integer/Fraction values are printed in `round_examples.out`.

For 1<=t<2, every admissible S has at most one edge, and the corresponding R in-degree and T out-degree are each at most one since their squared-norm caps are t<2. Hence Out<=1; a single cycle is feasible, so **W=1**. Choosing **L=8 for the entire family** suffices: U4=t^3 and W/U4=t^(-3)->1/8.

Paper-ready corrected proposition:

> For each t in [1,2), let r=(8,t,8,8) and s=(t,t,t,8). Then U4=t^3 and W=1. Consequently the supremum of U4/W over regular statistics is at least 8. More generally, for L>=t>=1, these statistics satisfy U4=min(t^3,sqrt(t^3 L)); equality U4=t^3 holds exactly when L>=t^3.

Together with the lower witness, this places the universal approximation factor in [8,16]. It does not determine the sharp factor.

## 5. Obstruction to improving literal rounding: proved

There is an explicit optimal real arc representation on which the literal rule approaches factor 16. For 1<=t<2, set the singleton-Z, singleton-W, pair-ZW, and full-arc multiplicities equal to t, and every other multiplicity equal to 1. Its statistics are

`r=(t,t^3,t^4,t^3)`, `s=(1,t^2,t^2,t^2)`, `Out_real=t^4=U4`.

The equality is certified both by the arc products and by a tight B term `r_R sqrt(s_S s_T s_Q)=t^4`. Thus it is an actual real optimum. Flooring all three non-full factors gives 1, and recomputing the full multiplicity gives `floor(min r_e)=floor(t)=1`. Literal Out is exactly 1.

| t | U4 | Literal Out |
|---|---|---:|
| 3/2 | 81/16 | 1 |
| 7/4 | 2401/256 | 1 |
| 15/8 | 50625/4096 | 1 |
| 31/16 | 923521/65536 | 1 |
| 63/32 | 15752961/1048576 | 1 |

Hence no factor below 16 holds for **arbitrary-optimum literal rounding**. A better universal theorem needs selection/rebalancing of the optimum, a different rounding construction, or more general instances. This is a genuine obstruction, not a finite grid gap.

For these statistics W is actually **5** for all `15/8<=t<2`, which verifies and strengthens the report's statement W>=5 near 2. Since |R|<=1 and S and Q have squared norms below 4, only three Z and three W vertices can participate in a cycle. Let E be the number of T edges between them. The all-ones test vector implies `E<=||T|| sqrt(3*3)<6`, so E<=5. For the matching lower construction, use one R edge, complete stars to three Z and three W vertices, and T equal to the 3x3 upper-bidiagonal 0/1 matrix with five ones. Its Gram matrix is

`[[1,1,0],[1,2,1],[0,1,2]]`.

The leading principal minors of `(27/8)I-Gram` are exactly `19/8`, `145/64`, `379/512`, all positive, certifying squared norm below 27/8. Since `(15/8)^2=225/64>27/8`, this instance is feasible throughout the stated interval and outputs 5. The exact onset is t=2cos(pi/7), but that sharper transcendental expression is unnecessary for the rational certificate.

Thus the arbitrary-optimum literal-rounding limit 16 is compatible with W/U4->5/16 on this family, and supplies no lower bound 16 on the true universal constant.

One further local statement in original Sec. 5.3 is **refuted**: both losses need not approach their maxima only when the original full-arc multiplicity approaches 2. Set instead `n_X=n_Z=n_W=n_ZW=t`, `n_full=1`, and all remaining factors 1. Then

`r=(t,t^2,t^3,t^3)`, `s=(t,t^2,t^2,t^3)`, `Out_real=t^4=U4`,

where the D term `r_R*r_T=t^4` is tight. Literal flooring again gives Out=1, so U4/Out approaches 16 although n_full is identically 1. This is checked at all five rational t-values in the preceding table. The required near-2 quantity for the final flooring loss is the recomputed `h=m*`, not necessarily the original n_full. This error is confined to the discussion of possible improvements and does not affect the factor-16 proof.

## 6. Complete blocks and Astra's obstruction: proved

Set all vertex dimensions to n, take R,S,Q complete and T a perfect matching. Explicitly this is the arc representation with singleton-X=n, singleton-Y=n, pair-ZW=n (all others 1). The exact statistics are

`r=(n^2,n^2,n,n^2)`, `s=(n^2,n^2,1,n^2)`, `Out=n^3`.

The C term `sqrt(r_S r_Q s_R s_T)=n^3` is tight, so U4=Out. The original report calls this C-prime; with its own orbit naming it is C (the size pair S,Q is opposite).

For any `m*K_{a,b,c,d}` satisfying these caps, `cd<=s_T=1` forces c=d=1. Hence `Out=mab=|R|<=n^2`. Equality is attainable with `m=1,a=b=n,c=d=1`. This argument also covers heterogeneous disjoint complete blocks: every component must have c=d=1, and total output is then total |R|.

Exact rebuilt values:

| n | Out=U4 | Best complete-block output |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 8 | 4 |
| 3 | 27 | 9 |
| 5 | 125 | 25 |
| 7 | 343 | 49 |

A separate brute-force enumeration of all feasible complete-block integer parameters for n=1,2,3,4,5 returns 1,4,9,16,25.

For Astra's original obstruction, only the pair-ZW multiplicity n is needed. The actual domains have dimensions `(1,1,n,n)`, with sizes `(1,n,n,n)`, squared norms `(1,n,1,n)`, and Out=n. The A term `r_R s_S s_T=n` is tight (as are several others), so U4=n. Exact rebuilds n=1,2,3,5,7 return 1,2,3,5,7 respectively.

## 7. Remaining qualifications

The small integer grids do not establish the best universal factor, particularly because the factor-8 lower obstruction uses nonintegral size/norm caps. The sharp constant problem is not reduced to a finite search by these computations. A proof of U4/8<W via a suitably chosen arc witness would settle it at 8; finding only one poorly rounded arc representation would not disprove such a theorem. The dual vertex count/irreducibility and universal upper-bound proofs are audited by the other independent lanes.
