> Archived research report (problem P3, spectral bound with two measured norms), verbatim except that machine-local paths were removed. Verdicts and paper-ready statements: `../verified.md` §3. Two items needed repairs: "option (c) is settled" covers exactly two measured norms (the one-norm six-term variant is `../verified.md` P3.15), and the closing sentence on `cycle4_obstruction.py` overstates what the script computes: it checks the witness (Out = n) and the bound Out <= |R||T|, while the block optimum 1 is established by the two-line argument in the text (`../verified.md` P3.13).

**[proved] Option (c) is settled: with all three size bounds and operator norms known for two relations, an explicit six-term bound characterizes the worst-case output within the sharp factor \(4\).** The construction uses integer blocks. Moreover, a planner need only consider driving one of the two relations whose norms are known.

This is an explicit specialization of the paper’s triangle theorem. The report below gives an independent proof, proves that all six terms are necessary, and establishes the planner consequence.

**[proved] Two-norm spectral AGM theorem.**

Let
\[
R\subseteq X\times Y,\qquad S\subseteq Y\times Z,\qquad T\subseteq Z\times X
\]
be finite set relations, with incidence matrices \(A,B,C\). Impose
\[
|R|\le r_R,\quad |S|\le r_S,\quad |T|\le r_T,\qquad
\|A\|_{\mathrm{op}}\le\sigma_R,\quad
\|B\|_{\mathrm{op}}\le\sigma_S.
\]
There is **no supplied norm constraint on \(T\)**. Assume the five supplied bounds are at least \(1\), and put
\[
p=\min(\sigma_R^2,r_R),\qquad q=\min(\sigma_S^2,r_S).
\]
Define
\[
\boxed{
U_2=\min\left\{
\underbrace{\sqrt{p r_Sr_T}}_{H_R},
\underbrace{\sqrt{q r_Rr_T}}_{H_S},
\underbrace{r_Rq}_{D_{R,S}},
\underbrace{r_Sp}_{D_{S,R}},
\underbrace{r_Tp}_{D_{T,R}},
\underbrace{r_Tq}_{D_{T,S}}
\right\}.
}
\]
If \(W_2\) denotes the supremum of \(\operatorname{tr}(ABC)\) over admissible instances, then
\[
\boxed{\frac{U_2}{4}<W_2\le U_2.}
\]
The upper constant \(1\) is attained. The lower constant \(1/4\) is best possible over the paper’s domain of real-valued bounds.

If any nonnegative supplied bound is below \(1\), the corresponding relation must be empty, so \(W_2=0\). A negative bound leaves the admissible class empty, with value \(0\) under the paper’s convention.

**[proved] Complete upper-bound proof.**

For any binary matrix \(A\), a column of degree \(d\) satisfies
\[
d=\|Ae_y\|_2^2\le\|A\|_{\mathrm{op}}^2.
\]
Applying the same argument to \(A^\top\) bounds row degrees. Also,
\[
\|A\|_{\mathrm{op}}^2\le\|A\|_F^2=|R|.
\]
Thus every row and column degree of \(R\) is at most \(p\), and every degree of \(S\) is at most \(q\).

For each \(R\)-tuple \((x,y)\), there are at most \(d_S^+(y)\le q\) possible triangle completions. Hence
\[
\mathrm{Out}\le r_Rq.
\]
Counting by \(S\)-tuples similarly gives \(\mathrm{Out}\le r_Sp\). For each \(T\)-tuple \((z,x)\), possible \(y\)'s lie in
\[
R(x,\cdot)\cap S(\cdot,z),
\]
whose size is at most both \(p\) and \(q\). Therefore
\[
\mathrm{Out}\le r_Tp,\qquad \mathrm{Out}\le r_Tq.
\]

For the spectral term, define vectors
\[
u_z(y)=1_{S(y,z)},\qquad v_z(x)=1_{T(z,x)}.
\]
Then
\[
\begin{aligned}
\mathrm{Out}
&=\sum_z v_z^\top A u_z\\
&\le \|A\|_{\mathrm{op}}\sum_z\|v_z\|_2\|u_z\|_2\\
&\le \|A\|_{\mathrm{op}}
   \left(\sum_z\|v_z\|_2^2\right)^{1/2}
   \left(\sum_z\|u_z\|_2^2\right)^{1/2}\\
&=\|A\|_{\mathrm{op}}\sqrt{|T||S|}
\le\sqrt{p r_Tr_S}.
\end{aligned}
\]
Cyclically applying this argument to \(B\) gives
\[
\mathrm{Out}\le\sqrt{q r_Rr_T}.
\]
Together these prove \(\mathrm{Out}\le U_2\). No norm of \(T\) was used. \(\square\)

**[proved] Explicit integer construction and complete lower-bound proof.**

For integers \(a,b,c,m\ge1\), take
\[
X=[m]\times[a],\quad Y=[m]\times[b],\quad Z=[m]\times[c].
\]
Include a pair in each relation exactly when its endpoints have the same first coordinate. These are \(m\) vertex-disjoint complete tripartite blocks. Direct counting gives
\[
|R|=mab,\quad |S|=mbc,\quad |T|=mca,\qquad
\mathrm{Out}=mabc.
\]
An all-ones \(a\times b\) matrix is an outer product of vectors of lengths \(\sqrt a,\sqrt b\), so its squared operator norm is \(ab\). A block-diagonal union takes the maximum norm of its blocks. Consequently
\[
\|A\|_{\mathrm{op}}^2=ab,\quad
\|B\|_{\mathrm{op}}^2=bc,\quad
\|C\|_{\mathrm{op}}^2=ca.
\]

Set
\[
\widehat a=\max(1,U_2/r_S),\quad
\widehat b=\max(1,U_2/r_T),\quad
\widehat c=\max(1,U_2/r_R).
\]
Using
\[
\max(1,u)\max(1,v)=\max(1,u,v,uv),
\]
we obtain
\[
\widehat a\widehat b
=\max\left(1,\frac{U_2}{r_S},\frac{U_2}{r_T},
                 \frac{U_2^2}{r_Sr_T}\right)\le p.
\]
The four inequalities follow respectively from regularity and the terms
\(D_{S,R},D_{T,R},H_R\). Similarly,
\[
\widehat b\widehat c\le q
\]
follows from regularity and \(D_{T,S},D_{R,S},H_S\).

The remaining pair product satisfies
\[
\widehat c\widehat a
=\max\left(1,\frac{U_2}{r_R},\frac{U_2}{r_S},
                 \frac{U_2^2}{r_Rr_S}\right)\le r_T,
\]
because
\[
U_2\le r_Tp\le r_Tr_R,\qquad
U_2\le r_Tq\le r_Tr_S,\qquad
U_2^2\le p r_Sr_T\le r_Rr_Sr_T.
\]
Thus the real multiplicity
\[
m^*=\min\left\{
\frac{r_R}{\widehat a\widehat b},
\frac{r_S}{\widehat b\widehat c},
\frac{r_T}{\widehat c\widehat a}
\right\}
\]
is at least \(1\). Its relaxed output is
\[
\begin{aligned}
m^*\widehat a\widehat b\widehat c
&=\min(r_R\widehat c,r_S\widehat a,r_T\widehat b)\\
&=\min_{i\in\{R,S,T\}}\max(r_i,U_2)=U_2.
\end{aligned}
\]
For the last equality, each of the six terms defining \(U_2\) is at least
\(\min(r_R,r_S,r_T)\).

Now choose the integers
\[
\boxed{
a=\lfloor\widehat a\rfloor,\quad
b=\lfloor\widehat b\rfloor,\quad
c=\lfloor\widehat c\rfloor,\qquad
m=\left\lfloor\min\left\{
\frac{r_R}{ab},\frac{r_S}{bc},\frac{r_T}{ca}
\right\}\right\rfloor.
}
\]
Flooring preserves \(ab\le p\), \(bc\le q\), and \(ca\le r_T\). Writing the minimum inside the final floor as \(\mu\), we have \(\mu\ge1\). Hence all four integers are positive, and the construction satisfies every size and norm constraint.

For every real \(x\ge1\), \(\lfloor x\rfloor>x/2\). Therefore
\[
\begin{aligned}
\mu abc
&=\min(r_Rc,r_Sa,r_Tb)\\
&>\frac12\min(r_R\widehat c,r_S\widehat a,r_T\widehat b)
=\frac{U_2}{2}.
\end{aligned}
\]
Since \(m>\mu/2\),
\[
\mathrm{Out}=mabc>\frac{U_2}{4}.
\]
This proves the lower bound. \(\square\)

**[proved] Relation to the paper’s nine-term formula.**

Set the unmeasured third norm bound to \(\sqrt{r_T}\), which is automatically valid, so its clipped statistic is \(s_T=r_T\). The nine-term theorem then reduces exactly to the six terms above:

- \(H_T=\sqrt{r_Rr_Sr_T}\) is dominated by \(H_R\).
- \(D_{R,T}=r_Rr_T\) is dominated by \(r_Tp\).
- \(D_{S,T}=r_Sr_T\) is dominated by \(r_Tq\).

Thus the six-term formula loses nothing relative to applying §3 with the missing norm replaced by its Frobenius bound.

**[proved] Sharpness of the constant \(4\).**

For \(1\le t<2\), choose
\[
(r_R,r_S,r_T)=(t^2,t,t^2),\qquad
\sigma_R=\sqrt t,\quad \sigma_S=1.
\]
Then \(p=t,q=1\), and the six terms are, in the displayed order,
\[
(t^2,t^2,t^2,t^2,t^3,t^2).
\]
Hence \(U_2=t^2\).

Every admissible instance has \(|S|\le t<2\), so \(S\) contains at most one tuple. Every column degree of \(R\) is an integer at most \(t<2\), hence at most \(1\). If the single \(S\)-tuple is \((y,z)\), at most one \(x\) can satisfy \(R(x,y)\). This proves \(\mathrm{Out}\le1\), regardless of \(T\)'s operator norm.

One triangle is admissible, so
\[
W_2=1,\qquad \frac{W_2}{U_2}=\frac1{t^2}\longrightarrow\frac14
\quad(t\uparrow2).
\]
Together with the strict lower bound,
\[
\inf_{\text{regular bounds}}\frac{W_2}{U_2}=\frac14,
\]
and the infimum is not attained. \(\square\)

**[refuted] A universally smaller factor than \(4\), for this \(U_2\), is impossible.** This sharpness statement concerns real-valued bounds, as in the paper; it does not assert that \(4\) is optimal under an additional restriction to integer size bounds.

**[proved] Every one of the six terms is necessary, even for constant-factor accuracy.**

For every integer \(n\ge2\), the following instances attain their indicated term exactly.

| Active term | \((r_R,r_S,r_T)\) | \((p,q)\) | Integer block \((a,b,c,m)\) | \(W_2=U_2=\mathrm{Out}\) |
|---|---|---|---|---:|
| \(H_R\) | \((n^4,n^4,n^4)\) | \((n^2,n^4)\) | \((n,n,n,n^2)\) | \(n^5\) |
| \(H_S\) | \((n^4,n^4,n^4)\) | \((n^4,n^2)\) | \((n,n,n,n^2)\) | \(n^5\) |
| \(D_{R,S}\) | \((n^2,n^6,n^6)\) | \((n^2,n^2)\) | \((1,1,n^2,n^2)\) | \(n^4\) |
| \(D_{S,R}\) | \((n^6,n^2,n^6)\) | \((n^2,n^2)\) | \((n^2,1,1,n^2)\) | \(n^4\) |
| \(D_{T,R}\) | \((n^6,n^6,n^2)\) | \((n^2,n^4)\) | \((1,n^2,1,n^2)\) | \(n^4\) |
| \(D_{T,S}\) | \((n^6,n^6,n^2)\) | \((n^4,n^2)\) | \((1,n^2,1,n^2)\) | \(n^4\) |

For completeness, substituting these parameters into the six terms gives the following exponent vectors, meaning that the terms are \(n\) raised to these powers:
\[
\begin{array}{c|rrrrrr}
H_R&5&6&8&6&6&8\\
H_S&6&5&6&8&8&6\\
D_{R,S}&7&5&4&8&8&8\\
D_{S,R}&5&7&8&4&8&8\\
D_{T,R}&5&6&10&8&4&6\\
D_{T,S}&6&5&8&10&6&4
\end{array}
\]
The size and squared-norm formulas for the displayed blocks verify admissibility directly. Each block’s output equals the unique smallest term, so the upper bound proves \(W_2=U_2\). Deleting that term increases the remaining minimum by exactly \(n\), an unbounded factor. \(\square\)

**[proved] Exact integer cardinalities can also be required.**

When the three size bounds are integers, pad each relation to its specified size using isolated edges on fresh endpoints that participate in no other relation. These edges create no triangles. In each incidence matrix they form additional norm-one components, so they preserve the measured norm constraints when those bounds are at least \(1\).

Consequently the worst-case output for exact integer sizes equals that for the corresponding size upper bounds.

**[proved] Planner consequence: the two measured relations suffice as drivers.**

In the paper’s shorter-side probe model, let
\[
M_R=\sum_{(x,y)\in R}\min(d_S^+(y),d_T^-(x)),
\]
\[
M_S=\sum_{(y,z)\in S}\min(d_T^+(z),d_R^-(y)).
\]
Then
\[
\boxed{
\begin{aligned}
M_R&\le\min(H_R,r_Rq,r_Sp,r_Tp),\\
M_S&\le\min(H_S,r_Sp,r_Rq,r_Tq).
\end{aligned}}
\]
In particular,
\[
\boxed{\min(M_R,M_S)\le U_2<4W_2.}
\]

To prove the first spectral inequality, use \(\min(u,v)\le\sqrt{uv}\):
\[
M_R\le u^\top Av
\le\|A\|_{\mathrm{op}}\|u\|_2\|v\|_2
\le H_R,
\]
where \(u_x=\sqrt{d_T^-(x)}\) and \(v_y=\sqrt{d_S^+(y)}\).

The other three inequalities follow from
\[
M_R\le |R|q,
\]
\[
M_R\le\sum_y d_R^-(y)d_S^+(y)\le p|S|,
\]
\[
M_R\le\sum_x d_R^+(x)d_T^-(x)\le p|T|.
\]
For \(M_S\), the same argument with driver matrix \(B\) gives \(H_S\), while
\[
M_S\le p|S|,\qquad
M_S\le\sum_y d_S^+(y)d_R^-(y)\le q|R|,
\]
\[
M_S\le\sum_z d_S^-(z)d_T^+(z)\le q|T|.
\]
Every term of \(U_2\) occurs in at least one list. \(\square\)

A planner can select the driver using only the supplied statistics: use \(R\) when a minimizing term is \(H_R,D_{S,R},D_{T,R}\), and \(S\) when it is \(H_S,D_{R,S},D_{T,S}\).

**[proved] Cost-model qualification.** This establishes a probe-work bound. With constant-time membership tests it gives \(O(N+U_2)\) execution work. The inspected Zig implementation uses galloping in `intersectEachBy`/`intersectWalk`; its comparisons include seek costs. The result therefore does not establish a log-free \(O(N+U_2)\) comparison bound for that implementation.

**[proved] Exact computational checks.**

All scripts were created in the private scratch directory and executed with `python3 -I`. No repository files were edited.

The verification artifacts are:

- [two_norms_exact.py](two_norms_exact.py)
- [p3_independent_checks.py](p3_independent_checks.py)

The construction verifier stores the exact rational number
\[
K=U_2^2
=\min\{p r_Sr_T,q r_Rr_T,(r_Rq)^2,(r_Sp)^2,(r_Tp)^2,(r_Tq)^2\}.
\]
For a nonnegative rational \(h\),
\[
\lfloor\sqrt h\rfloor=\operatorname{isqrt}(\lfloor h\rfloor).
\]
Thus every coordinate floor is computed exactly, without evaluating a floating-point square root. Each case checks all size and norm constraints and
\[
\mathrm{Out}^2\le K<16\,\mathrm{Out}^2.
\]

The exact grid results were:

| Grid | Cases | Failures | Largest \(K/\mathrm{Out}^2\) for the constructed block |
|---|---:|---:|---:|
| \(r_i\in\{1,\ldots,8\}\), integer \(1\le p\le r_R,\ 1\le q\le r_S\) | 10,368 | 0 | \(45/4\) |
| All five clipped parameters from \(\{1,3/2,2,5/2,3,4,8\}\), subject to clipping | 5,488 | 0 | \(15/2\) |

The respective maximizing cases were
\[
(r_R,r_S,r_T,p,q)=(5,7,6,5,6),\quad
(a,b,c,m)=(1,2,2,1),\quad K=180,\quad\mathrm{Out}=4,
\]
and
\[
(r_R,r_S,r_T,p,q)=(3/2,2,5/2,3/2,2),\quad
(a,b,c,m)=(1,1,1,1),\quad K=15/2,\quad\mathrm{Out}=1.
\]
These ratios concern the explicit construction, not an exhaustive computation of \(W_2\).

Six separately materialized block instances produced the following exact values. The squared terms follow the theorem’s order.

| \((r_R,r_S,r_T;p,q)\) | Six squared terms | \((a,b,c,m)\) | \(\mathrm{Out}=M_R=M_S=U_2\) |
|---|---|---|---:|
| \((16,16,16;4,16)\) | \((1024,4096,65536,4096,4096,65536)\) | \((2,2,2,4)\) | 32 |
| \((16,16,16;16,4)\) | \((4096,1024,4096,65536,65536,4096)\) | \((2,2,2,4)\) | 32 |
| \((2,8,16;2,2)\) | \((256,64,16,256,1024,1024)\) | \((1,1,2,2)\) | 4 |
| \((8,2,16;2,2)\) | \((64,256,256,16,1024,1024)\) | \((2,1,1,2)\) | 4 |
| \((8,8,2;2,4)\) | \((32,64,1024,256,16,64)\) | \((1,2,1,2)\) | 4 |
| \((8,8,2;4,2)\) | \((64,32,256,1024,64,16)\) | \((1,2,1,2)\) | 4 |

Their actual relation-size triples were, respectively,
\[
(16,16,16),\ (16,16,16),\ (2,4,4),\ (4,2,4),\ (4,4,2),\ (4,4,2),
\]
and their actual squared-norm triples were
\[
(4,4,4),\ (4,4,4),\ (1,2,2),\ (2,1,2),\ (2,2,1),\ (2,2,1).
\]

The asymptotic irredundancy families were checked at four values of \(n\):

| \(n\) | Outputs of the six families | Squared ratio after deleting the active term, in every family |
|---:|---|---:|
| 2 | \((32,32,16,16,16,16)\) | 4 |
| 3 | \((243,243,81,81,81,81)\) | 9 |
| 7 | \((16807,16807,2401,2401,2401,2401)\) | 49 |
| 16 | \((1048576,1048576,65536,65536,65536,65536)\) | 256 |

All **24 cases passed**, with **0 failures**.

For rational supplied norm bounds in the sharpness family, use
\[
(P,Q)\mapsto(3P+4Q,2P+3Q),\qquad(P,Q)=(7,5),
\]
which preserves \(P^2-2Q^2=-1\). Set \(t=P^2/Q^2\), so
\(\sigma_R=P/Q\) and \(t=2-1/Q^2\). The exact outputs were:

| \((P,Q)\) | \(t\) | \(U_2\) | \(W_2\) |
|---|---:|---:|---:|
| \((7,5)\) | \(49/25\) | \(2401/625\) | 1 |
| \((41,29)\) | \(1681/841\) | \(2825761/707281\) | 1 |
| \((239,169)\) | \(57121/28561\) | \(3262808641/815730721\) | 1 |
| \((1393,985)\) | \(1940449/970225\) | \(3765342321601/941336550625\) | 1 |
| \((8119,5741)\) | \(65918161/32959081\) | \(4345203949621921/1086301020364561\) | 1 |

Every constructed block was \((1,1,1,1)\). The equality \(W_2=1\) follows from the sharpness proof; the code checks the rational identities and witness.

Finally, the independent matrix check enumerated **all \(16^3=4,096\) triples of binary \(2\times2\) matrices**. Supplied squared-norm bounds were drawn from
\[
\{0,1,3/2,2,5/2,3,4\}.
\]
Feasibility was decided exactly by the principal minors of
\(pI-AA^\top\), followed by clipping. It checked the output bound and both individual driver inequalities.

```text
matrix_triples = 4096
feasible_budget_cases = 73984
positive_U_cases = 55815
failures = 0
max_Out_squared_over_U_squared = 1
max_min_MR_MS_squared_over_U_squared = 1
```

These are finite verification results. The universal statements are established by the proofs above.

**[refuted] Additional four-cycle finding: vertex-disjoint complete blocks cannot provide a constant-factor extension to option (b).**

For an integer \(n\ge1\), take
\[
R=\{(x,y)\},\quad
S=\{(y,z_i):i\in[n]\},\quad
T=\{(z_i,w_i):i\in[n]\},\quad
Q=\{(w_i,x):i\in[n]\}.
\]
The incidence matrices are a singleton, an all-ones row, \(I_n\), and an all-ones column. Thus their sizes and squared norms are
\[
r=(1,n,n,n),\qquad s=(1,n,1,n),
\]
and their output is \(n\).

Every four-cycle tuple is determined by its \(R\)-edge and opposite \(T\)-edge, so
\[
\mathrm{Out}\le |R||T|\le n.
\]
Hence the exact worst case at these bounds is \(W_4=n\).

A vertex-disjoint union of complete four-partite cycle components can have at most one nonempty component because \(|R|\le1\). Its first two part sizes must both be \(1\). Its other two part sizes \(c,d\) satisfy \(cd\le s_T=1\), so they too equal \(1\). Such a union therefore produces at most one tuple, losing the unbounded factor \(n\).

The scratch-only [cycle4_obstruction.py](cycle4_obstruction.py), run with `python3 -I`, checked
\[
n=1,2,3,7,16,64,1000.
\]
It produced outputs and exact worst cases
\[
1,2,3,7,16,64,1000,
\]
with complete-component optimum \(1\) in every case.

**[open-with-obstruction]** The general four-cycle characterization remains unproved here. The obstruction rules out the direct complete-block construction, while allowing constructions involving shared endpoints, stars, and matchings.