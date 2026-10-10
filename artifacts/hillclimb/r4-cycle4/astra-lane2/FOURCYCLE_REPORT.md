# Independent adversarial audit: the labelled 4-cycle

All work below was written from scratch in `v2-fr10-astra` and executed with `python3 -I`. I read the solver's report embedded in `../P3-spectral-verify-astra/task.md`, and read selected original/verifier source files to understand the constructions. I neither ran nor imported any original solver/verifier program. `fourcycle_extra.py` loads only my newly written `fourcycle_check.py`. No repository file was edited. Every load-bearing computation uses integers or `fractions.Fraction`; the exhaustive 2×2 test implements the exact field Q(√5) as pairs of Fractions.

Artifacts:

- `fourcycle_check.py`: independent monomial generator, fraction-free vertex enumeration, exact strict-separation certificates, exhaustive 0/1 checks, literal arc matrices, rounding and integer-grid checks.
- `fourcycle_dual.out` and `fourcycle_dual_certificates.json`: independently generated exact dual results/certificates.
- `fourcycle_tests.out`: exact exhaustive, adversarial, construction and grid results.
- `fourcycle_extra.py` / `fourcycle_extra.out`: direct H3 checks, D4 orbit decomposition, sharpness counterexample and literal-rounding obstruction.

Reproduction commands: `python3 -I fourcycle_check.py dual`; `python3 -I fourcycle_check.py small random arcs grid`; `python3 -I fourcycle_extra.py`.

## Verdicts

| Claim | Status | Result |
|---|---|---|
| Each of the 38 monomials bounds Out, constant 1 | **proved** | Checked every proof step; all independently generated terms match the independently enumerated necessary vertices. Exact exhaustive and adversarial tests found no violation. |
| Lemma Λ | **proved** | Weighted AM–GM/Perron proof is valid, including disconnected S after selecting Perron vectors separately in each nonempty component. Handle empty relations first. |
| Cubic moment F2 and F | **proved** | Expansion is exact; Λ and Hölder apply with the stated constants. Independent cubic-moment checks pass. |
| Incidence norm H3 and H | **proved** | Entrywise Gram domination and Λ give the claimed bound; 236 direct exact H3 certificates pass. |
| G via dyadic partition and tensor powers | **proved** | All estimates and the logarithm-removal argument are valid. The restriction A_Rjk has norm at most σ_R by nonnegative matrix monotonicity. |
| Arc sizes, norms, and output | **proved** | Kronecker-factor calculation is exact; 38 separately rebuilt actual matrix witnesses checked. |
| 50 dual vertices, 38 necessary, 12 redundant | **proved** by exhaustive exact computation | Independently enumerated all possible positive supports and active bases; both 13 and 9 arc systems return the same 50 vertices. All 38 strict-separation certificates are newly generated integer vectors. |
| “9 D4 orbits” | **refuted** | There are 10: sizes 2,2,2,4,4,4,4,4,4,8. A splits into 8 and 4. The listed 38 inequalities themselves are correct. |
| U4/16 < W ≤ U4 | **proved**, with one display repaired | Literal rounding proof is valid after removing a duplicated full-arc factor in its displayed inequality. |
| Sharp constant lies in [8,16] | **proved** | Sharpness family works with **L≥t³**, exactly; the asserted sufficient condition L≥t² is false. |
| Sharp constant equals 8, or smaller grids settle it | **open-with-obstruction** | The particular literal rounding procedure really can lose arbitrarily close to 16. The finite grids do not reduce the continuous constant question to a finite check. |
| Complete blocks lose a polynomial factor | **proved** | n=2,3,5,7 gives outputs 8,27,125,343 while all complete-block constructions have at most 4,9,25,49. The tight term is orbit C, not C′. |
| “The pair arc {Z,W} alone is exactly that instance” | **refuted** literally | It also needs singleton arcs {X} and {Y}, each of multiplicity n. The corrected arc construction gives exactly the stated matrices. |
| Astra obstruction (r,s)=((1,n,n,n),(1,n,1,n)) has U4=n | **proved** | Independent exact evaluation at n=2,3,5,7, and the singleton-pair arc construction proves it for all n. |
| Clipping for any measured subset P | **proved** | Omitted norm bounds equal the automatic bound σ_e²≤r_e; admissible classes coincide, so the relevant full-statistics theorem applies unchanged. |
| “4 is sharp for every nonempty P” | **proved only for the triangle** | It cannot mean the 4-cycle: with all four norms measured the proved sharpness example already forces constant at least 8. For the 4-cycle use 16 universally, with lower bound 8 whenever P contains an opposite pair. |

## Exact results from the independent code

### Dual and upper bounds

The dual enumeration gave:

```
DUAL 50 50 bases 203489 24309 needed 38 redundant 12 strict_witness_samples 212
```

The two basis counts are for all 13 arcs and the reduced singleton/pair/full system. Enumeration removes coordinates fixed to zero and solves every possible independent active set on the remaining positive support. Fraction-free elimination checks that every division is exact; solutions and feasibility are checked with Fractions. Thus this checks completeness as well as feasibility. The absent all-zero support is infeasible.

For a vertex v, another vertex u dominates it on ρ≥slog≥0 exactly when, for each edge, v_λ≥u_λ and v_λ+v_μ≥u_λ+u_μ. Twelve vertices have such a witness. For every remaining vertex v the saved integer vector c=(ρ,slog), with ρ≥slog≥0, satisfies (u−v)·c>0 for all other vertices u. No numerical LP or solver-generated separation certificate was used.

All 65,536 quartets of 2×2 0/1 matrices were enumerated. There were **32,377 positive-output instances**, **10,057 equality cases**, and maximum output **16**. Their norm squares are in {0,1,2,4,(3+√5)/2}, so all comparisons were decided exactly in Q(√5), with zero undecided cases. There were 625 distinct positive statistics vectors.

An independent 1,200-instance random/adversarial sample used dimensions 1 through 6 and included forced matchings and double-star-shaped matrices. It had **782 positive-output instances**, **74 exact equality cases**, zero upper-bound violations and zero undecided comparisons. Fraction Rayleigh quotients provide rigorous *lower* bounds for norm squares; verifying Out¹² against the resulting smaller right-hand sides certifies the true inequalities. The stronger F2 cubic moment passed separately on all 782 instances.

A separate 350-attempt sample directly formed the S×Q matrix B. It supplied **236 nonempty instances**, all certified for H3 using a rational Collatz upper bound for ||B||² and rational Rayleigh lower bounds for the four norm squares. There were **3 exact equality cases**, **zero undecided cases**.

The direct real-matrix counterexample is exact: R=T=I₂, S=Q=I₂/2 gives Out=**1/2** and H=**1/4**, using Frobenius squares as sizes. Therefore the extension of H to arbitrary real matrices is false.

### Arc witnesses, rounded witnesses, and grid optimum

For each of the 38 terms, all arcs with positive multiplicity were selected among its tight constraints. The full integer product identities were checked, and a literal matrix instance using three such arcs at multiplicity 2 was independently built. All **38** matrix instances had **Out=8**, all cardinalities and all exact norm squares agreed with the product formula, and the designated monomial equalled 8.

**1,520** independently generated rational real arc optima were floored exactly, with the full-arc multiplicity repacked exactly. All were admissible and satisfied 16 Out_int > U4. The largest ratio in this finite sample was exactly **4024588113/671088640**. It is a sample maximum, not a bound on the procedure.

The exact integer optimum was independently found for the complete small budget grids:

| Budget grid | Number of budgets | Distinct feasible integer arc statistics | Worst (U4/Out*)¹² | Witness (r;s;Out*) |
|---|---:|---:|---:|---|
| 1≤s_e≤r_e≤3 | 1,296 | 25 | 6,561 | (2,3,3,3); (1,2,2,3); 2 |
| 1≤s_e≤r_e≤4 | 10,000 | 90 | 46,656 | (2,3,4,3); (1,2,3,2); 2 |

These ratios are exactly 3^(2/3) and √6. At the displayed witnesses U4¹² is respectively **26,873,856** and **191,102,976**. All 11,296 integer optima satisfy the factor-16 theorem. Triple arcs need not be enumerated: replacing a triple by its complementary singleton preserves its output and norm factors and weakly decreases all sizes.

This audit did not claim reproduction of the solver's particular LP tie-breaking or heuristic-rounded grid maximum. Those are implementation-specific statistics, and the prior report already distinguishes them from the literal rounding and from the exact integer optimum.

### Sharpness family: exact repair

For r=(L,t,L,L), s=(t,t,t,L), with 1≤t<2, every admissible instance has |S|≤1 and the two relevant degrees in R,T at most 1. Thus W=1, attained by a single cycle.

Every term is L^a t^b. Among terms with a>0, the maximum of (3−b)/a is exactly **3**, achieved by the C term √(r_S r_Q s_R s_T)=√(L t³). Thus the exact condition for U4=t³ is **L≥t³**.

| t | Smallest integer L with U4=t³ | W/U4 |
|---|---:|---:|
| 3/2 | 4 | 8/27 |
| 7/4 | 6 | 64/343 |
| 15/8 | 7 | 512/3375 |
| 31/16 | 8 | 4096/29791 |
| 63/32 | 8 | 32768/250047 |

The asserted weaker condition L≥t² fails at t=3/2,L=3: **U4¹²=282429536481/262144**, whereas **t³⁶=150094635296999121/68719476736**. Taking L≥t³ and t→2⁻ proves inf W/U4≤1/8.

Only the norms of R and T are actually needed here. The S norm bound is automatically implied by r_S=t, and Q already has s_Q=r_Q=L. Therefore the lower bound 8 persists with any measured subset containing this opposite pair (or its rotation).

### A useful obstruction to improving the rounding constant

Set n_{Z}=n_{W}=n_{ZW}=n_full=t and every other arc multiplicity to 1, where 1≤t<2. These are real feasible optima for

r=(t,t³,t⁴,t³), s=(1,t²,t²,t²), U4=t⁴.

Literal flooring makes every non-full multiplicity 1, and the repacked full multiplicity is floor(min r_e)=floor(t)=1. Consequently Out_int=1 and the literal rounding ratio tends to **16**. Exact values include:

| t | U4 / Out_int |
|---|---:|
| 3/2 | 81/16 |
| 7/4 | 2401/256 |
| 15/8 | 50625/4096 |
| 31/16 | 923521/65536 |
| 63/32 | 15752961/1048576 |
| 1023/512 | 1095222947841/68719476736 |

This does **not** refute a possible sharp worst-case constant 8, because a better integer construction can outperform this rounding. It does refute any attempt to prove 8 by asserting that this literal procedure, applied to an arbitrary optimum, always loses less than 8.

## Proof audit, step by step

1. **Basic tools.** Degree ≤σ² follows from individual row/column Euclidean norms. The operator/Frobenius inequalities and nonnegative spectral monotonicity are valid for rectangular matrices of the displayed dimensions. A connected nonempty bipartite component supplies positive singular vectors. Empty relations imply Out=0 and should be excluded before ratios or σ_T/σ_R are introduced.

2. **A.** Fixing a driver edge leaves a two-vertex completion. The three independent counts are d_S(y)Δ_T⁺, d_S(y)d_Q(x), d_Q(x)Δ_T⁻. Substitution of degree bounds yields the 12 stated monomials.

3. **B.** The completion count is an indicator-vector bilinear form across the opposite matrix. Its operator-norm bound gives √(s_S s_T s_Q) per R edge, and all rotations follow.

4. **C and C′.** Group the trace into two factors and use Frobenius duality. For adjacent norm factors, use ||R S T||_F≤σ_R σ_S ||T||_F. For opposite norm factors, use ||R S||_F≤σ_R ||S||_F and ||T Q||_F≤σ_T ||Q||_F. These produce all six terms, with the labels C=opposite cardinality pair, C′=adjacent cardinality pair.

5. **D.** A pair of opposite relation tuples fixes all four variables. Thus Out≤|R||T| and Out≤|S||Q|.

6. **E.** Forgetting one closing edge injects cycles into three-paths. Their count is d_R^-ᵀ S d_T^+, bounded by σ_S ||d_R^-||₂ ||d_T^+||₂. Since Σd²≤ΔΣd≤s r, the asserted four terms follow.

7. **Λ.** On each S component choose positive p,q with S q=σ_c p and Sᵀp=σ_c q; define θ_yz=√(q_z/p_y). For nonnegative unit u on S, apply weighted AM–GM entrywise to √(ρ_yy′ τ_zz′). The resulting quadratic forms factor through U_y=Σ_z u_yz θ_yz and V_z=Σ_y u_yz/θ_yz. Cauchy–Schwarz gives ||U||²,||V||²≤σ_S. Cross-component pairs cause no problem because factorization uses globally assembled U,V, while the Cauchy–Schwarz estimate is componentwise. Hence uᵀKu≤σ_S(κσ_R²+κ⁻¹σ_T²)/2. Taking κ=σ_T/σ_R proves the lemma. The proof is 0/1-sensitive through the support pattern used to define the Perron vectors and the edge-indexed unweighted sums.

8. **F2.** Expanding two of the three factors in M_xw³ identifies an ordered pair s,s′ of S edges and the common endpoint sets X_ss′,W_ss′. Summing the remaining M factor over these sets gives exactly 1_Xᵀ M 1_W. This is at most ||M||√(|X||W|)≤σ_Rσ_Sσ_T K_ss′. Summing and applying 1ᵀK1≤|S|λ_max(K) proves ΣM³≤|S|σ_R²σ_S²σ_T². Hölder over Q then yields F without a lost factor.

9. **H3 and H.** The (s,s′) Gram entry of B is precisely 1_Wᵀ Q 1_X≤σ_Q K_ss′. Symmetric nonnegative matrix monotonicity and Λ give ||B||²≤σ_Rσ_Sσ_Tσ_Q. Finally Out=1_SᵀB1_Q≤√(|S||Q|)||B||. Raising to the fourth power produces the stated H term.

10. **G.** Partition R by positive Q-in-degree of x and S-out-degree of y. Each bucket has degrees in [2^j,2^(j+1)) and [2^k,2^(k+1)). For h=Q R_jk S, Out_jk≤min(||h||₁,√|T| ||h||_F). The bound min(a,b)≤a^(1/3)b^(2/3) is valid. Next ||h||₁≤2^(j+k+2)|R_jk| and ||h||_F²≤s_Q s_S |R_jk|. The spectral estimate |R_jk|≤σ_R√(|X_jk||Y_jk|) follows by applying R itself to the two indicators, or by 0≤R_jk≤R. Since |X_jk|≤|Q|/2^j and |Y_jk|≤|S|/2^k, the product is at most 4 s_R s_S s_Q |Q||S|. There are at most (1+log₂|Q|)(1+log₂|S|) buckets. Kronecker powers preserve 0/1 matrices and multiply outputs, sizes, and norms; taking nth roots removes the polynomial in n exactly. This proves G with constant 1.

11. **Arc formula.** For each arc, an edge matrix factor is I_n, a 1×n or n×1 all-ones matrix, or scalar 1. Edge size contributes n whenever the arc meets the edge; norm square contributes n exactly when the arc meets one endpoint. Contiguity forces all copies of an arc coordinate in a cycle to agree, leaving one free value per arc. Kronecker multiplicativity proves all three product formulas. A triple's complementary singleton has the same norm incidences and fewer size incidences; therefore triples are dispensable for the optimum.

12. **Duality.** The primal is feasible and bounded for finite regular statistics. The dual is feasible and pointed. Standard LP duality and attainment reduce the logarithmic optimum to a minimum over dual vertices. Complete exact enumeration, dominance, and strict-separation certificates then identify exactly U4. This is a rigorous finite computation, not a numerical guess.

13. **Rounding.** Let n be a real optimum. Floor non-full factors, then let m*=min_e r_e/∏_{A≠full,A∩e≠∅} floor(n_A) and m=floor(m*). Feasibility is immediate, with m*≥n_full≥1. The exact identity is

    m* ∏_{A≠full} floor(n_A) = min_e r_e ∏_{A∩e=∅} floor(n_A).

    Each edge has exactly three disjoint nonempty arcs: the two opposite singletons and their pair. Their flooring loses a factor strictly less than 8. The size constraint implies

    r_e ∏_{A∩e=∅} n_A ≥ ∏_A n_A = U4.

    The solver's display accidentally wrote n_full times the product over *all* A, duplicating the full factor. The inequality above is the correct one and proves the intended argument. Since floor(m*)>m*/2, Out_int>U4/16.

14. **Partial norm information.** For an unmeasured edge, σ²≤|e|≤r_e is automatic. Setting s_e=r_e neither removes nor adds admissible instances. The theorem and its witness therefore transfer to every subset P; there is no additional optimization issue.

## Paper-ready corrected theorem

Let R⊆X×Y, S⊆Y×Z, T⊆Z×W and Q⊆W×X be finite relations, and let r_e≥1 and s_e=min(σ_e²,r_e)≥1. Let U4 be the minimum of the 38 monomials in the stated list. Then every admissible instance has Out≤U4, and there is an integer arc-blowup instance with Out>U4/16. The 38 monomials are individually necessary on the cone 1≤s_e≤r_e, and form ten D4 orbits. The optimal universal approximation factor is between 8 and 16. The lower endpoint follows from r=(L,t,L,L), s=(t,t,t,L), 1≤t<2 and L≥t³, for which W=1 and U4=t³. If norm bounds are supplied only on a subset P of edges, set s_e=r_e on the other edges; the same factor-16 theorem holds. The lower bound 8 still applies whenever P contains an opposite pair.

The sharp factor remains **open-with-obstruction**. In particular, flooring an arbitrary real arc optimum and then repacking the full arc can itself lose a factor approaching 16, so an improvement requires a stronger rounding/choice-of-optimum argument or a different construction.
