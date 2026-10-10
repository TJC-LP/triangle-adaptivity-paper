Let the edge labels 0,1,2,3 denote R,S,T,Q in cyclic order. All relations below are finite sets, represented by binary incidence matrices. Assume the supplied bounds r_e,σ_e are nonnegative. Write s_e=min(σ_e²,r_e), and call the statistics regular when r_e,σ_e≥1 for every edge. Let W₄(r,σ) be the maximum output over admissible instances.

Define U₄ as the minimum of the following 38 monomials. In rows involving i,j,k,l, the four indices are distinct; an opposite pair has distance two around the cycle. Repeated descriptions of the same monomial are counted only once.

| Family | Monomials | Number |
|---|---|---:|
| A | r_i s_j s_k, with {j,k} any two labels other than i | 12 |
| B | r_i (s_j s_k s_l)^(1/2) | 4 |
| C | (r_i r_j s_k s_l)^(1/2), {i,j} opposite | 2 |
| C′ | (r_i r_j s_k s_l)^(1/2), {i,j} adjacent | 4 |
| D | r_i r_j, {i,j} opposite | 2 |
| E | (r_i r_k s_i s_j s_k)^(1/2), i,j,k consecutive | 4 |
| F | (r_i r_j² s_i s_k s_l)^(1/3), {i,j} opposite | 4 |
| G | (r_j r_k r_l s_i s_k s_l)^(1/3), {i,j} opposite | 4 |
| H | (r_i r_j)^(1/2) (s_R s_S s_T s_Q)^(1/4), {i,j} opposite | 2 |

**Theorem.** Every admissible binary instance has Out≤U₄, with constant one in each of the 38 inequalities. For regular statistics,

    U₄/16 < W₄(r,σ) ≤ U₄.

The 38 terms form ten dihedral orbits: A splits into orbits of sizes eight and four. Each term is uniquely minimal on an open region of regular statistics and is attained by an integer arc family. None may be removed while preserving a universal constant-factor estimate.

For the lower construction, it suffices to use the nine arcs consisting of four singleton vertex sets, four adjacent pairs, and the full vertex set V. Assign an integer n_A≥1 to each arc A. Vertex v has coordinate space ∏_{A∋v}[n_A]; an edge requires equality on every shared arc coordinate. Then

    |e| = ∏_{A∩e≠∅} n_A,
    ||A_e||² = ∏_{|A∩e|=1} n_A,
    Out = ∏_A n_A.

The logarithmic packing LP of these constraints has optimum log U₄. Its dual has 50 vertices; twelve are dominated on 1≤s_e≤r_e and the remaining 38 give the displayed terms. Adjoining the four triple arcs changes neither the real nor the integer optimum: moving a triple factor to the full arc preserves every size and the output and decreases two norm costs.

Choose any real optimum n_A≥1. Floor its eight proper-arc multiplicities and set

    m = floor(min_e r_e / ∏_{A≠V, A∩e≠∅} floor(n_A)).

This is admissible and has output greater than U₄/16. Indeed, writing m* for the unfloored minimum,

    m* ∏_{A≠V} floor(n_A)
      = min_e r_e ∏_{A∩e=∅} floor(n_A)
      > (1/8) min_e r_e ∏_{A∩e=∅} n_A
      ≥ U₄/8.

Exactly three arcs are disjoint from an edge. Also m*≥n_V≥1, so floor(m*)>m*/2. The final inequality uses the corrected identity ∏_A n_A=U₄; it does not multiply this product by n_V again. The same proof works with all thirteen arcs, since no triple arc is disjoint from an edge.

**Proposition.** For every 1≤t<2, set

    r=(8,t,8,8),  s=(t,t,t,8).

Then W₄=1 and U₄=t³. Consequently, if κ₄=sup_regular U₄/W₄, then 8≤κ₄≤16. More generally, for t≥1 and L≥t,

    U₄((L,t,L,L),(t,t,t,L)) = min(t³, √(Lt³)),

so U₄=t³ if and only if L≥t³. In the range t<2, |S|≤1 and the relevant R-column and T-row both have degree at most floor(t)=1; hence W₄≤1, with equality from one cycle.

**Lemma (lifted Gram bound).** Put ρ=A_RᵀA_R and τ=A_TA_Tᵀ, and index K by the edges s=(y,z) of S, with K_{ss′}=√(ρ_{yy′}τ_{zz′}). Then

    λ_max(K) ≤ ||A_R|| ||A_S|| ||A_T||.

If any of these norms vanishes the assertion is immediate. Otherwise choose positive left and right Perron singular vectors p,q on each nontrivial connected component of S. For s=(y,z), put θ_s=√(q_z/p_y). For a nonnegative vector u indexed by S, define U_y=∑_z u_yz θ_yz and V_z=∑_y u_yz/θ_yz. Cauchy–Schwarz and the component Perron identities imply ||U||²,||V||²≤||A_S|| ||u||². Weighted arithmetic–geometric mean gives, for κ>0,

    uᵀKu ≤ 1/2 [κ UᵀρU + κ⁻¹ VᵀτV]
          ≤ 1/2 [κ ||A_R||² + κ⁻¹ ||A_T||²] ||A_S|| ||u||².

Set κ=||A_T||/||A_R||. Since K is symmetric and entrywise nonnegative, its top eigenvalue is obtained on a nonnegative vector, proving the lemma.

The F and H terms follow as follows. For M=A_RA_SA_T, expanding two of the three factors in ∑_{x,w}M_{xw}³ over ordered pairs of S-edges gives

    ∑ M³ ≤ ||M|| 1ᵀK1 ≤ |S| ||A_R||² ||A_S||² ||A_T||².

Hölder on the Q-edges proves F. For the binary S-by-Q matrix B_{(y,z),(w,x)}=A_R(x,y)A_T(z,w), common-neighborhood counting gives BBᵀ≤||A_Q||K entrywise. Thus ||B||²≤∏_e||A_e||, and Out=1ᵀB1≤√(|S||Q|)||B|| proves H. These arguments use binary indicators in the expansions and support identities; a weighted-matrix extension is not asserted.

For G, partition R by positive dyadic degrees d_Q⁻(x)∈[2^a,2^(a+1)) and d_S⁺(y)∈[2^b,2^(b+1)). With R_ab a class and h=A_Q A_{R_ab} A_S, write ||h||₁ for its entrywise sum. Its output is at most (|T| ||h||₁ ||h||_F²)^(1/3). The bounds

    ||h||₁ ≤ 4·2^(a+b)|R_ab|,
    ||h||_F² ≤ ||A_Q||² ||A_S||² |R_ab|,
    |R_ab|² ≤ ||A_R||² |X_ab||Y_ab|,
    2^a |X_ab|≤|Q|,  2^b |Y_ab|≤|S|

give the required G monomial times 4^(1/3)(1+log₂|Q|)(1+log₂|S|). Apply this estimate to the n-fold Kronecker power of the binary instance, take nth roots, and let n→∞. The logarithmic factor has nth root tending to one, proving G with constant one. A–E follow directly from degree counting, the spectral bilinear inequality, and Frobenius Cauchy–Schwarz.

**Corollary (partial norm information).** If norm constraints are specified only for a subset P of edge labels, put s_e=r_e off P. The same U₄ upper bound holds, and the strict factor-16 lower bound holds when every size bound and every specified norm bound is at least one. The lower obstruction κ≥8 persists whenever |P|≥2: the displayed family uses only the opposite norms on R,T, and for adjacent known norms R,S one may use r=(8,8,8,t), s=(t,t,8,t). The remaining placements follow by dihedral symmetry.

The exact value of κ₄ remains open. In particular, the literal flooring rule applied to an arbitrary optimal real arc instance cannot yield a factor smaller than sixteen: take n_{Z}=n_W=n_{ZW}=n_V=t∈[1,2), all other multiplicities one. Its statistics are r=(t,t³,t⁴,t³), s=(1,t²,t²,t²), and U₄=t⁴, while literal rounding has output one. This obstructs that rounding rule, not a better bound on W₄.
