# Independent triangle and slope audit

This report covers §2.7–2.8 and triangle claims in §3.1 of the supplied claim, plus the high-slope fully reduced completion requested during coordination. It does not certify the 4-cycle theorem or the six-parameter live gadget (other lanes own those).

All executable verification here was freshly written, run with `python3 -I`, and uses integers or `fractions.Fraction`; no solver script was run or imported. `triangle_audit_additional.py`, `triangle_audit_fans.py`, and `triangle_audit_padding.py` load only our own `triangle_audit_exact.py`. Solver files were read to recover the claimed definitions. Incidence supports are rebuilt as Python sets; all reported C, M, moments and outputs are recomputed from those supports. Spectral cap admissibility is decided by exact rational symmetric elimination on `sI-AᵀA`. Squared bounds avoid all floating arithmetic.

## Verdicts

| Claim | Status | Qualification or repair |
|---|---|---|
| Two measured norms: six-term U₂; U₂/4 < W₂ ≤ U₂ | **proved** | Both proofs and literal integer-block witnesses verified. |
| Factor 4 sharp in the two-norm class | **proved** | Same t∈[1,2) family works without T's norm bound; use R's column degree, not a bound on T. |
| Six-term collapse from nine-term U at s_T=r_T | **proved** | H_T,D_(R,T),D_(S,T) are dominated as claimed. |
| All six and all nine terms necessary | **proved** | Every listed family attains its unique minimum; deleting it multiplies U by exactly n for n≥2. |
| Exact integer cardinalities by isolated-edge padding | **proved** | Requires regular statistics and freely extendable finite domains, as in the paper. |
| Planner inequalities and choosing R or S from statistics | **proved** | All listed inequalities hold. The claim only rules out always choosing the unmeasured T; it does not say T can never be a good choice. |
| Clipping for every known-norm subset P, triangle | **proved** | Set s_e=r_e off P. Factor 4 is sharp for every nonempty P, including a single measured norm. |
| e(κ)=1 throughout [0,9/10] | **refuted** | e(κ)≤(6κ−1)/4<1 for asymptotic slopes 1/3≤κ<5/6. At κ=5/6 the bound equals 1; strictness at this endpoint is false. |
| “No instance has κ<1/3” | **refuted literally; proved asymptotically** | One triangle has N=3,B₂=1 and log_N B₂=0. For families with N→∞ and B₂=Θ(N^κ)>0, necessarily 1/3≤κ≤2. |
| e(κ)=3/2 for κ≥3/2 | **proved after domain repair** | Restrict to κ∈[3/2,2]. Indeed attainment holds even on fully reduced inputs, by the explicit clique-plus-fans construction below. |
| GMIN constant 3^(3/5), not 3^(6/5) | **proved** | The fifth power of the upper-bound/actual ratio tends to 27. |
| General-input qualifier on exact fixed-GAO gap 1/4 | **proved repair** | The proof and known lower family cover general inputs; semijoin-reduced bounds remain [1/5,1/4]. |
| At most 1 below κ=9/10 | **proved** | This is an upper bound, not a matching lower bound. |
| max((10κ−1)/8,(27κ−9)/16) lower bound on all [5/6,9/10) | **open-with-obstruction** | The first cited construction is feasible only for κ≥6/7. At κ=5/6 its g₁ exponent is −1/48. No counterexample to the proposed bound is established, but the supplied proof does not prove it on [5/6,6/7). |
| Fixed-root gap [1/8,1/2] and fixed-GAO semijoin gap [1/5,1/4] | **proved as ranges of established bounds** | Rebuilt G₈ and semijoin padding of GMIN verify the lower witnesses. This audit does not close either interval. |

## Proof audit: triangle spectral theorem and specializations

1. Every row/column degree of a 0/1 matrix is bounded by its squared operator norm, by applying the matrix or transpose to a coordinate vector. The Frobenius norm gives σ²≤r after clipping. Both steps apply to 0/1 set relations as required.
2. Counting triangle completions per relation edge gives all six degree terms r_i s_j. Applying Cauchy–Schwarz to `sum_z <t_z,A_R u_z>` gives H_R, and rotation gives H_S,H_T. No inequality needs an unmeasured norm after replacing that statistic by r.
3. For the real shape â=max(1,U/r_S), b̂=max(1,U/r_T), ĉ=max(1,U/r_R), expand âb̂ as max(1,U/r_S,U/r_T,U²/(r_Sr_T)). The four constraints are exactly regularity, two degree bounds and H_R. Rotating gives the remaining six inequalities. The iff statement for any V>0 is valid.
4. Real multiplicity μ*≥1 because products are ≤s_i≤r_i. Its output is min(max(r_R,U),max(r_S,U),max(r_T,U))=U because each of the nine terms is at least min_i r_i.
5. Flooring the three shape coordinates loses less than a factor 2 in `min(c r_R,a r_S,b r_T)`, not 2³. Flooring multiplicity loses less than another factor 2. Thus the strict `Out>U/4` and admissibility are correct.
6. For s_T=r_T, H_T≥H_R since s_R≤r_R; D_(R,T)≥D_(T,R) and D_(S,T)≥D_(T,S). Precisely the displayed six terms remain. This is an equality of minima, not an approximation.
7. In the sharpness family r=(t²,t,t²), p=t,q=1, the six terms are (t²,t²,t²,t²,t³,t²). Since |S|≤t<2, S has at most one edge; since every R column has degree ≤t<2, it has at most one neighbor. That S edge extends to at most one triangle. A single triangle is admissible. W₂=1, U₂=t², ratio tends to 4 as t↑2. None of these steps uses T's norm.
8. The same sharpness proof uses only the R norm, |S|≤t and the three sizes. Hence it witnesses sharpness for a single measured norm and, by adding whichever redundant/t-compatible norm caps and relabeling, every nonempty subset P.
9. Irredundancy is checked by exact substitution. H_R's witness gives n⁵ versus next term n⁶; D_(R,S)'s witness gives n⁴ versus next term n⁵. Label permutations produce nine witnesses. The six two-norm witnesses have the same strict separation and exact attained output.
10. An isolated fresh edge adds a separate 1×1 block to its relation matrix. Its norm is 1 and it has no adjacent edges in the other relations, so it creates no triangle. Thus exact-size padding preserves feasibility and output and can fill every integer deficit.
11. For M_R, min(p,q)≤√(pq) followed by the operator bound gives H_R. Bounding the per-edge minimum by the S degree gives r_R q. Summing S degrees by incoming R degree gives r_S p; grouping by x gives r_T p. The corresponding S bounds follow by rotation/reflection. Their union covers U₂, so one of the two measured relations is a valid driver chosen solely from supplied statistics.
12. Matchings R,S and T=K_(k,k) give Out=M_R=M_S=U₂=k, M_T=k². Thus a policy restricted to T can be arbitrarily bad against U₂.

Exact independent spectral checks:

- All **4,096** 2×2 Boolean relation triples; **289,815** admissible rational norm-cap budget cases; zero upper-bound/planner violations.
- **12,000** seeded random instances and star-shaped adversaries on parts of size 1–7; zero triangle, per-binding, fixed-driver, best-driver or low-slope chain violations. Maximum `min(M)^5/(|R||S||T|Q)` was exactly 1. Maximum `(C−N)_+^8/(|R||S||T|Q²)` was exactly **17181861798319201/1900033747998750000**.
- **10,368** integer statistics vectors with r_i≤8, 1≤p≤r_R,1≤q≤r_S: nine/six collapse exact and rounded block feasible with 16Out²>U₂² throughout. Worst squared ratio U₂²/Out² was **45/4**, at r=(5,7,6), p=5,q=6, block=(1,2,2,1), Out=4.
- Nine witnesses at n=2: outputs **(32,32,32,16,16,16,16,16,16)**, deletion ratio 2. At n=3: **(243,243,243,81,81,81,81,81,81)**, ratio 3. At n=5: **(3125,3125,3125,625,625,625,625,625,625)**, ratio 5. Six-witness outputs are respectively (32,32,16,16,16,16), (243,243,81,81,81,81), (3125,3125,625,625,625,625).
- **192** isolated-edge padding cases preserved exact output and reached the requested integer sizes.
- Pell pairs (7,5),(41,29),(239,169),(1393,985) produced U₂/W₂ exactly **2401/625**, **2825761/707281**, **3262808641/815730721**, **3765342321601/941336550625**; W₂=1 throughout.
- Unmeasured-driver examples k=2,3,5,8 produced `(Out,M_R,M_S,M_T)` = **(2,2,2,4)**, **(3,3,3,9)**, **(5,5,5,25)**, **(8,8,8,64)**.

## A complete proof of the low-slope upper bound

Let Q=B₂³. Relabel/refelect so that relation sizes r≥s≥t with r≥N/3. Write Q_f=αβγ and Q_b=α′β′γ′. The paper's single-driver fourth-power inequalities, C≤|i|+M_i, integer degrees, and Cauchy–Schwarz imply

`N(C−t)_+^4 ≤ 3Q_f²`,
`N(C−s)_+^4 ≤ 3Q_b²`,
`N(C−t)_+² ≤ 3tQ_b`.

Here the first follows from M_T⁴≤t s² γα≤st Q_f and st≤Q_f/r≤3Q_f/N. The second uses the reflected M_S bound. For the third, M_T²≤γβ′, γ≤t², α′≥r and γ′≥t imply M_T²≤tQ_b/r≤3tQ_b/N. These also cover zero degrees by nonnegative inequalities.

Assume 1≤B₂≤N^(5/6), and put h=Q^(1/2)N^(−1/4). If Q=Q_f, then t≤√(3Q/N)≤√3 h, and M_T≤3^(1/4)h, so C<4h. If Q=Q_b and s≤h, the second inequality gives C≤(1+3^(1/4))h. If instead s>h, then t≤3Q/(Ns)<3Q^(1/2)N^(−3/4)≤3h; the third bound gives M_T<3Q^(3/4)N^(−7/8)≤3h, where the last step is Q≤N^(5/2). Thus universally

**C ≤ 6 N^(−1/4) B₂^(3/2), whenever 1≤B₂≤N^(5/6).**

For B₂=Θ(N^κ), the same proof with constants gives e(κ)≤(6κ−1)/4 on 1/3≤κ≤5/6. This is strictly below 1 only for κ<5/6. A separate exact sample of 10,000 random instances had **6,237** satisfying Q²≤N⁵, and the maximum C⁴N/Q² was **48**, below 6⁴=1296. Finite testing supplements the proof; it does not establish sharpness.

## Slope domains, lower witnesses and remaining obstruction

For nonempty relations, moments are at least their relation's size and at most its squared size. Hence `(N/3)^(1/3)≤(|R||S||T|)^(1/3)≤B₂≤(|R||S||T|)^(2/3)≤(N/3)²`. Consequently growing families with positive power-law B₂ have slopes only in [1/3,2]. This is an asymptotic statement; it must not be phrased as a restriction on finite `log_N B₂`.

The dead gadget G(p,q,t,g) was rebuilt for **285** integer parameter tuples with p,q,t,g≤5, g≤p and g|pt. All 13 scalar formulas for relation sizes, root costs, forward/reverse moments and Out=0 agreed exactly. Each Z₂ vertex numbered j has g neighbors X[(jg+h) mod p], h=0,…,g−1, and q private incoming Y₂ vertices. This is simple and biregular because g≤p and g divides pt. Its expensive-root cost is pqt+p min(q,t); cheap-root costs are qt and pqt/g. The disjoint three-rotation union yields the quoted lower families.

For the asymmetric V(κ) construction, the first gadget has g-exponent `(7κ−6)/8`. At κ=5/6 this is **−1/48**, so g=u^(−D/48)<1 for u>1; there is no integral graph construction. All parameters and exponents are feasible for κ≥6/7. Exact tropical checks give:

| κ | N exponent | C exponent | B₂ exponent |
|---|---:|---:|---:|
| 6/7 | 1 | 53/56 | 6/7 |
| 7/8 | 1 | 31/32 | 7/8 |
| 8/9 | 1 | 71/72 | 8/9 |
| 9/10 | 1 | 1 | 9/10 |
| 1 | 1 | 9/8 | 1 |

The invalid formal substitution κ=5/6 outputs C exponent 11/12 but does not define an instance. Closed-form integer evaluations for feasible κ at u=2 and 3 are in `triangle_audit_additional.out`; for example κ=6/7,D=56,u=2 gives **N=72631040924975104,C=9008337421074432,B₂³=1427247692705959881058285969449495136382746624**. At κ=9/10,D=80,u=2: **N=1214275593117998941995008,C=1208944338557034410541056**, confirming the supplied large-number row independently.

The padded symmetric family with M fresh S matching edges has

`N=3(u⁸+u⁷+u⁶+u⁵)+M`, `C=u⁹+u⁸+u⁶+u⁵`,
`B₂³=(4u⁸)²(4u⁸+M)`, `Out=0`.

It is valid for M=u^t with every t≥8, not only the t∈[8,9] range tested in Fable's script. Therefore it gives e≥(27κ−9)/16 throughout 1/3<κ≤1. Literal tuples were generated at u=2,3,4 and t=8,9,10. Selected exact outputs:

| u,t | N | C | B₂³ |
|---|---:|---:|---:|
| 2,8 | 1696 | 864 | 1342177280 |
| 2,10 | 2464 | 864 | 2147483648 |
| 3,9 | 48843 | 27216 | 31632108085872 |
| 4,10 | 1309696 | 332800 | 90071992547409920 |

Safe corrected statement: **On [6/7,9/10), `(10κ−1)/8≤e(κ)≤1`. On [5/6,6/7), the supplied constructions establish at least `(27κ−9)/16≤e(κ)≤1`; the stronger first lower bound on that interval remains unproved by the supplied material.** This is a conservative correction, not a claim that the weaker lower bound is optimal.

## High-slope attainment on fully reduced inputs

Take K_(s,s,s), and on disjoint vertices add three rotated n-spoke triangle fans. One fan has a central x, vertices y_i,z_i, and edges (x,y_i),(y_i,z_i),(z_i,x). Every edge belongs to a triangle. The union has exactly

`N=3s²+9n`, `Out=s³+3n`, `C_x=C_y=C_z=s²(s+1)+6n`,
`α=β=γ=α′=β′=γ′=s³+n²+2n`, hence `B₂=s³+n²+2n`.

Every edge's triangle support was checked directly. Exact `(s,n;N,C,Out,B₂)` rows are:

(2,4;48,36,20,32), (3,9;108,90,54,126), (4,16;192,176,112,352), (8,64;768,960,704,4736).

With n=⌊s^κ⌋, κ∈[3/2,2], N=Θ(s²), B₂=Θ(s^(2κ)), C=Θ(s³). AGM gives the matching upper exponent 3/2. This extends the fully reduced attainment statement beyond [11/10,3/2] to [11/10,2] once the live-gadget interval is proved by the owning verifier lane.

## Existing separation constants and semijoin claims

Literal G₈ at m=2,3,4 gives `(N,C_x,C_y,C_z,B₂³)`:

- **(736,576,32,256,67108864)**;
- **(16281,20412,243,6561,1129718145924)**;
- **(152576,266240,1024,65536,1125899906842624)**.

Thus C_x~m⁹, N+B₂=Θ(m⁸), confirming the fixed-root gap lower bound 1/8; the general upper 1/2 follows directly from C_x≤N+AGM and AGM≤(N/3)^(3/2).

GMIN is independently built from three rotations of E(m³,m,m²). Its `(N,C,M_min,B₂)` rows are **(168,40,64,96)**, **(1053,270,729,729)**, **(4032,1088,4096,3072)**, **(11625,3250,15625,9375)**. The fifth powers of the paper's upper-bound/actual ratios are respectively **9261/64,2197/27,250047/4096,804357/15625**. Algebraically this is `27(1+1/m+1/m²)³→27`; the ratio tends to **3^(3/5)**.

Attaching one fresh triangle per half-dangling original vertex gives pairwise semijoin reduction. The rebuilt padded GMIN outputs `(N,C,M_min,Out,B₂)`:

- m=2: **(492,296,212,108,268)**;
- m=3: **(3321,2052,1755,756,1971)**;
- m=4: **(13392,8416,8304,3120,8240)**.

All relation-domain support equalities were checked. These certify the 1/5 lower bound on pairwise semijoin-reduced inputs; the known fixed-driver inequality gives the 1/4 upper bound. They do not certify full reduction, which is a distinct condition.

## Reproduction

Run from this directory:

```
python3 -I triangle_audit_exact.py
python3 -I triangle_audit_additional.py
python3 -I triangle_audit_fans.py
python3 -I triangle_audit_padding.py
```

The corresponding `.out` files preserve exact numbers. No paper source was edited.
