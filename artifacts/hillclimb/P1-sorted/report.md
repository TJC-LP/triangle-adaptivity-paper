> Archived research report (problem P1, sorted intersections), verbatim except that machine-local paths were removed. Verdicts and paper-ready statements: `../verified.md` §1. One item needed a repair: the randomized-routine sentence near the end of the quarter-log proof ("averaging the same union-bound argument over their random seeds") needs a Markov step; the corrected statement is `../verified.md` P1.21 and the paper's theorem `thm-quarterlog`.

**[PROVED] P1 holds for fresh, comparison-based sorted-intersection calls.** One global term order can force all the required rows and competing options simultaneously.

There is also a sharper answer to the logarithmic question:

\[
\boxed{
Q_{\mathrm{sorted}}
=O\!\left(
N+(\log N)^{1/4}
(|R||S||T|)^{1/8}\min(\Lambda,\Lambda')^{1/2}
\right).
}
\]

**[PROVED] The quarter-logarithmic factor is necessary in this model**, including when \(B_2=\Theta(N)\). Thus the optimal worst-case scale there is

\[
\boxed{\Theta\!\left(N^{9/8}(\log N)^{1/4}\right).}
\]

The explicitly interleaved original \(G_8\) and \(F_{i,j}\) families themselves have **no logarithmic overhead**. A modified family is needed to attain the quarter logarithm.

**[REFUTED] These conclusions do not extend to unrestricted comparison-based join algorithms.** Reusing intersection certificates, pruning relations, or exploiting global structure can defeat these examples. The precise model matters.

All files written during this work are in the private scratch directory. No repository was edited.

---

**[PROVED — model and scope]**

Write \(T_x=\{z:(z,x)\in T\}\), and use analogous neighborhood notation. As in the paper, a plan:

1. chooses one root variable for the whole instance;
2. chooses one of its two options independently at each binding;
3. visits every outer tuple of that option and invokes an intersection on the corresponding two runs.

The sorted-intersection model is:

- Each call receives two strictly increasing arrays and their lengths.
- Keys are opaque ordered objects. Comparisons may return \(<,=,>\), or use Boolean predicates. Key arithmetic, hashing, and addressing by key value are unavailable.
- Array indexing and index arithmetic are permitted. Every key comparison is charged. We additionally charge one unit per visited outer tuple.
- The call must correctly compute the intersection on **every** legal pair of sorted runs.
- Each call starts with fresh comparison knowledge: it knows the internal sorted orders, but receives no certificates, aliases, rank hints, or comparison results from previous calls.
- The intersection implementation is fixed before the adversary assigns term IDs. Root and option selection may even be omniscient.

Degree reads and plan selection can be charged separately; an \(O(N)\) metadata pass suffices for the upper bound below. Charging neighbor reads as well changes only constant factors.

Let \(Q_A\) denote the best root-and-option execution cost using a fixed eligible intersection implementation \(A\). This minimizes over plans, **not over arbitrary new programs chosen after seeing the labeling**.

The explicit alternating constructions below are hard for every correct fresh-call implementation on the same labeling. This includes plain merge, leapfrog, and galloping with any correct step schedule. Their lower bounds also hold for every execution of a zero-error randomized implementation.

The quarter-log lower bound has the standard adversarial quantifiers:

\[
\forall A\quad \exists\text{ one global labeling }\ell.
\]

Its labeling may depend on the fixed implementation.

**[PROVED — relation to §§3–4]** Relabeling permutes matrix rows and columns, so it preserves relation sizes, degrees, singular values, \(N,B_2,U\), and output cardinality. The spectral AGM theorem \(U/4<W\le U\) and its sharp constant are unaffected. The paper’s \(M_\pi\) and \(C\) remain valid min-side proxies; translating them into actual sorted-comparison work requires the analysis below.

---

**[PROVED — the comparison certificate]**

For disjoint sorted runs \(A,B\), let \(t(A,B)\) be the number of adjacent pairs in their merged order whose members belong to different runs.

Every correct fresh intersection call requires at least \(t(A,B)\) comparisons.

*Proof.* Suppose adjacent opposite-run keys \(a,b\) were never directly compared. Identify them, making their values equal. Each input remains strictly increasing because the two keys belong to different runs. Since no key lies between them, every other comparison result remains unchanged. The intersection changes from empty to nonempty, contradicting correctness. Therefore every adjacent opposite-run pair must be compared. ∎

In particular,

\[
a_0<b_0<a_1<b_1<\cdots<a_{s-1}<b_{s-1}
\]

requires \(2s-1\) comparisons. Ordinary ternary merge achieves exactly that number.

This argument charges comparisons rather than cursor increments. Arbitrary seek distances or galloping schedules cannot evade it.

**[PROVED — simultaneous interleaving lemma]**

Let \(A=\{a_k:k<s\}\), and let \(B_h=\{b_{h,k}:k<s\}\) be arbitrarily many disjoint private sets. The single order

\[
a_k,\ b_{0,k},b_{1,k},\ldots
\qquad(k=0,\ldots,s-1)
\]

makes the projection onto \(A\cup B_h\) alternate for every \(h\).

Similarly, ordering several equal-sized groups by “position within group, then group” makes every pair of distinct groups alternate.

Orders imposed on disjoint term domains can be concatenated. Orders for vertex-disjoint rotated copies can also be concatenated. Thus these constructions produce one total term-ID order, not independently chosen row orders.

---

**[PROVED — original \(G_8\): simultaneous hardness and exponent \(9/8\)]**

The construction must handle the actual neighborhoods \(T_x\subseteq Z_0\cup Z_2\), which vary with \(x\).

Use the paper’s cardinalities, with this particular biregular realization:

\[
X=\{(g,h):g<m^3,\ h<m\},
\qquad
Z_2=\{(g,t):g<m^3,\ t<m^3\}.
\]

For each \(g\), connect every \(z\in Z_{2,g}\) to every \(x\in X_g\). Thus each \(x\) receives \(m^3\) positive \(Z_2\)-neighbors, and each \(z\in Z_2\) has \(m\) outgoing \(T\)-edges.

Give each \(x\) its own \(m^4\) private \(Z_0\)-predecessors. Give each \(z\in Z_2\) its own \(m^2\)-element predecessor set \(Y_{2,z}\) in \(S\). Complete the gadget with

\[
R=X\times Y_0,\qquad S\supseteq Y_0\times Z_1.
\]

This realizes exactly the degrees specified in the paper.

Choose these orders:

- In \(Z\), for every \(t<m^3\), place
  \[
  Z_1[t],Z_2[0,t],\ldots,Z_2[m^3-1,t],
  \]
  then append all \(Z_0\)-keys.
- In \(Y\), for every \(k<m^2\), place
  \[
  Y_0[k],\quad Y_{2,z}[k]\text{ for every }z\in Z_2.
  \]

Consequently:

- Every \(Z_1\) versus \(T_x\) call has \(2m^3-1\) necessary comparisons. The unused \(Z_0\)-tail causes no extra work for merge.
- Every \(Y_0\) versus \(Y_{2,z}\) call has \(2m^2-1\) necessary comparisons.

Both properties hold simultaneously for every \(x,z\).

For one critical \(x\), including outer visits, the two ternary-merge costs are exactly

\[
q_R(x)=m^2\bigl(1+2m^3-1\bigr)=2m^5,
\]

\[
q_T(x)=m^4+m^3\bigl(1+2m^2-1\bigr)=m^4+2m^5.
\]

The certificate proves these are also lower bounds for any eligible implementation. Thus the optimal critical-root cost is exactly \(2m^9\).

At the other roots, the inexpensive options intersect empty runs:

\[
Q_y(G_8)=m^5,\qquad Q_z(G_8)=m^8.
\]

For the union \(\mathcal U(m)\) of three rotations, each global root therefore has exact optimal ternary cost

\[
\boxed{Q_{\mathrm{ternary}}(\mathcal U(m))
=2m^9+m^8+m^5.}
\]

The exact statistics are

\[
N=3(2m^8+m^7+m^6+m^5),
\qquad
B_2=5m^8.
\]

To verify the latter equality, each forward squared-degree sum is \(5m^8\); each reverse sum is

\[
m^{12}+2m^{11}+3m^{10}+m^7>5m^8.
\]

Hence

\[
Q_{\mathrm{ternary}}=\Theta(m^9)=\Theta(N^{9/8}),
\]

and, since \(N+B_2\le14m^8\),

\[
\frac{Q_A}{N+B_2}\ge \frac m7
\ge \frac1{7}\left(\frac N9\right)^{1/8}.
\]

This refutes \(O(N+B_2)\), and any fixed polylogarithmic relaxation of it, for this class.

**[PROVED — padding]** The \(G_8\) lower bound survives the paper’s padding. The endpoints defining the hard runs already have tuples in both incident relations, so those runs are unchanged. Place fresh padding keys before original keys. The previously cheap empty intersections become constant-cost singleton cases, while \(N+B_2=O(m^8)\) and the hard cost remains \(\Omega(m^9)\).

This is a direct preservation argument; it does not assume that sorted-intersection cost is monotone under tuple insertion.

---

**[PROVED — original \(F_{i,j}\) families]**

Fix \(i\ge j\ge1\), \(u\ge2\), and abbreviate

\[
n=u^{4i},\quad a=u^{4i-2j},\quad b=u^{4i-j},
\quad d=u^{4i-3j},\quad H=u^{3j}.
\]

Partition \(X\) into \(H\) groups of size \(d\), and \(Z_2\) into \(H\) groups of size \(b\). Make the corresponding \(T\)-blocks complete. For every \(z\in Z_2\), give it a private \(a\)-element \(S\)-predecessor set.

Use the simultaneous interleaving lemma:

- alternate the common \(Z_1\) against every \(Z_2\)-group;
- alternate the common \(Y_0\) against every private \(Y_{2,z}\).

Both options at every critical \(x\) now cost exactly \(2ab\), including outer visits. The other two gadget roots cost \(ab\) and \(u^{8i}\). Therefore the three-rotation union has exact optimal ternary cost

\[
\boxed{
Q_{\mathrm{ternary}}
=2u^{12i-3j}+u^{8i}+u^{8i-3j}.
}
\]

Its exact statistics are

\[
N=3\left(u^{8i}+u^{8i-j}+u^{8i-2j}+u^{8i-3j}\right),
\]

\[
B_2=3u^{12i-4j}+u^{8i}.
\]

Indeed, the reverse sum is
\[
3u^{12i-2j}+u^{12i-5j},
\]
which is larger.

Thus

\[
B_2=\Theta(N^\kappa),\qquad
\kappa=\frac32-\frac{j}{2i},
\]

and

\[
Q_{\mathrm{ternary}}
=\Theta\!\left(N^{3/8}B_2^{3/4}\right).
\]

Every hard call is balanced, so ordinary merge and galloping attain this without a logarithm.

Exact structural checks produced:

| \((i,j,u)\) | \(N\) | \(B_2\) | Exact ternary cost |
|---|---:|---:|---:|
| \((1,1,2)\) | 1,440 | 1,024 | 1,312 |
| \((1,1,3)\) | 29,160 | 26,244 | 46,170 |
| \((2,1,2)\) | 368,640 | 3,211,264 | 4,268,032 |
| \((2,2,2)\) | 261,120 | 262,144 | 590,848 |

These preserve the paper’s dense set of polynomial exponents. The next result identifies the additional factor in the actual worst-case sorted model.

---

**[PROVED — universal quarter-log upper bound]**

For nonempty runs define the degree-computable price

\[
h(p,q)=s\left(1+\left\lceil\log_2(\ell/s)\right\rceil\right),
\quad s=\min(p,q),\quad \ell=\max(p,q),
\]
and set \(h(p,q)=0\) if either run is empty.

Ordinary doubling galloping costs \(O(h(p,q))\) comparisons and reads. A skipped gap of length \(g\) costs \(O(1+\log(g+1))\); the gaps advance monotonically through the longer run. Summing and applying concavity of logarithms gives the stated bound.

Put \(L_N=1+\lceil\log_2N\rceil\). We have

\[
h(p,q)\le L_Np,\qquad h(p,q)\le3\sqrt{pq}.
\]

For the second inequality, if \(r=\ell/s>1\) and \(k=\lceil\log_2r\rceil\), then

\[
(k+1)^2\le9\cdot2^{k-1}<9r.
\]

The elementary inequality follows from the cases \(k=1,2\), followed by induction using \((k+2)^2\le2(k+1)^2\) for \(k\ge2\).

At root \(x\), put \(a=d_R^+(x)\), \(b=d_T^-(x)\), and

\[
P(x)=\sum_{y\in R(x)}h(d_S^+(y),b),
\quad
Q(x)=\sum_{z\in T_x}h(a,d_S^-(z)),
\]

\[
w(x)=\sum_{z\in T_x}\sqrt{d_S^-(z)}.
\]

Using the paper’s degree moments,

\[
P(x)\le L_N\sqrt{a\beta},
\qquad
Q(x)\le3\sqrt a\,w(x).
\]

Therefore

\[
\min(P,Q)\le P^{1/4}Q^{3/4}
\le
3^{3/4}L_N^{1/4}\beta^{1/8}
a^{1/2}w(x)^{3/4}.
\]

Hölder gives

\[
\sum_x a^{1/2}w(x)^{3/4}
\le
\alpha^{1/4}\left(\sum_xw(x)\right)^{3/4}.
\]

Double counting and Cauchy–Schwarz give

\[
\sum_xw(x)
=\sum_zd_T^+(z)\sqrt{d_S^-(z)}
\le\sqrt{\gamma|S|}.
\]

Thus the cost priced by \(1+h\) satisfies

\[
\widehat C_x
\le |R|+|T|
+3^{3/4}L_N^{1/4}
\alpha^{1/4}\beta^{1/8}(\gamma|S|)^{3/8}.
\]

Rotate, reflect, multiply the three root bounds, and take a cube root:

\[
\boxed{
\widehat C
\le N+
3^{3/4}L_N^{1/4}
(|R||S||T|)^{1/8}
\min(\Lambda,\Lambda')^{1/2}.
}
\]

Executing the selected plan by galloping costs \(O(\widehat C)\).

This is implementable: price all six options from degrees in \(O(N)\) reads, select the best root and each binding’s cheaper option, then execute. The ceiling logarithm is computed exactly by integer bit lengths. For \(0<s\le\ell\),

\[
\left\lceil\log_2(\ell/s)\right\rceil
=\operatorname{bitlength}\!\left(\left\lfloor\frac{\ell-1}{s}\right\rfloor\right).
\]

The original price-then-run proposition selects the min-side proxy; using these revised prices gives the sorted upper bound.

**[PROVED — logarithm-free AGM cap]** The same inequality \(h(p,q)\le3\sqrt{pq}\) gives

\[
\sum_{(x,y)\in R}h(d_S^+(y),d_T^-(x))
\le3\|A_R\|\sqrt{|S||T|}
\le3\sqrt{|R||S||T|}.
\]

Thus an independent \(O(N+\mathrm{AGM})\) cap remains available.

---

**[PROVED — the quarter logarithm is necessary, on every \(F_{i,j}\) slope]**

This construction strengthens the original \(G_8/F\) lower bounds.

Fix \(i\ge j\ge1\), an integer \(h\ge1\), and set

\[
M=2^h,\qquad L=M^4,\qquad u=2^L.
\]

Define

\[
\begin{aligned}
n=|X|&=\frac{u^{4i}}{M^4},
&
a=|Y_0|&=u^{4i-2j}M^2,
&
p=|Z_1|&=\frac{u^{4i-j}}M,\\
q&=u^{4i}M^4,
&
k&=pL,
&
d&=u^{4i-3j}M,
&
c=|Z_2|&=\frac{u^{4i+2j}}{M^2}.
\end{aligned}
\]

All quantities are integers. In particular,

\[
\frac nd=\frac ck=\frac{u^{3j}}{M^5}\in\mathbb N.
\]

Construct:

- \(R=X\times Y_0\);
- \(S\supseteq Y_0\times Z_1\);
- a private \(a\)-element predecessor set \(Y_{2,z}\) for every \(z\in Z_2\);
- complete paired \(T\)-blocks with \(d\) vertices of \(X\) and \(k\) vertices of \(Z_2\);
- \(q\) private dead \(Z_0\)-predecessors for each \(x\).

The handshakes are

\[
ca=nq=u^{8i},\qquad cd=nk.
\]

There are no triangles.

*The competing \(T\)-option.* Alternate \(Y_0\) with every \(Y_{2,z}\), using the simultaneous layering lemma. Its \(k\) positive intersections each require \(2a-1\) comparisons. Therefore, at every critical \(x\),

\[
q_T(x)\ge k(2a-1)\ge apL.
\]

*Making every \(R\)-call expensive.* Put all \(Z_2\)-keys after \(Z_1\cup Z_0\). For each \(x\), independently choose a shuffle of its \(q\) private dead keys with the common ordered \(p\)-element \(Z_1\).

These independent choices are compatible with one global order: in each of the \(p+1\) gaps of \(Z_1\), concatenate the private keys assigned to that gap, in a fixed order of \(x\). Append \(Z_2\) last.

There are

\[
H=\binom{p+q}{p}
\ge(q/p)^p
=(u^jM^5)^p
\ge u^p
=2^{pL}
\]

possible shuffles for each \(x\).

A correct disjoint-answer comparison leaf must determine the whole shuffle. Otherwise some opposite-run pair is incomparable in the partial order induced by the transcript and the internal sorted orders. Identifying that pair preserves all comparisons and strict internal orders but creates an intersection, contradicting correctness.

Consequently a prescribed call program has fewer than \(2^D\) shuffles on which it uses fewer than \(D\) comparisons. Choose

\[
D=pL/2.
\]

Under a uniformly chosen shuffle,

\[
\Pr[\text{a prescribed call costs}<D]\le2^{-pL/2}.
\]

Across three rotated copies there are \(3na\) relevant potential \(R\)-calls. The union bound gives

\[
\Pr[\text{any is cheap}]
\le3na\,2^{-pL/2}<1.
\]

For completeness, the last inequality follows from

\[
\log_2(3na)<2+8iL,
\qquad
D\ge16iL>2+8iL.
\]

Here \(p=u^{4i-j}/M\ge u^{2i}\ge32i\), since \(L\ge16\).

Therefore **one global labeling** makes every critical \(R\)-call cost at least \(D\). Its entire \(R\)-option costs at least \(apL/2\), while its competing \(T\)-option costs at least \(apL\).

Every global root contains one critical rotated component. Thus, regardless of root and option choices,

\[
\boxed{
Q_A\ge naD=\frac M2u^{12i-3j}.
}
\]

The proof allows different prescribed call programs; they must be fixed before labeling and cannot import learned comparison facts. For zero-error randomized routines, averaging the same union-bound argument over their random seeds gives the corresponding expected lower bound.

*Exact statistics.* Each relation in the rotated union has size

\[
S_0=
2u^{8i}+\frac{u^{8i-j}}M+
\frac{u^{8i-2j}}{M^2}+u^{8i-3j}M,
\qquad N=3S_0.
\]

Each forward squared-degree sum is

\[
A=3u^{12i-4j}+2u^{8i}.
\]

Each reverse sum is

\[
A'=
u^{12i}M^4+2u^{12i-j}M^3+
2u^{12i-2j}M^2+
\frac{u^{12i-2j}}{M^6}
+u^{12i-5j}M^3>A.
\]

Hence \(B_2=A\) exactly, and

\[
6u^{8i}\le N\le15u^{8i},
\qquad
3u^{12i-4j}\le B_2\le5u^{12i-4j}.
\]

For fixed \(i,j\),

\[
B_2=\Theta(N^{3/2-j/(2i)}),
\]

\[
N^{3/8}B_2^{3/4}=\Theta(u^{12i-3j}),
\qquad
M=\Theta((\log N)^{1/4}).
\]

This matches the universal upper bound on every dense slope represented by \(i\ge j\ge1\). In particular, \(i=j\) gives

\[
B_2\asymp N,\qquad
Q_A=\Omega(N^{9/8}(\log N)^{1/4}).
\]

At \(\kappa=3/2\), the AGM cap and complete block triangle give the logarithm-free scale \(\Theta(N^{3/2})\).

**[REFUTED — literal logarithm-free translation of Theorem 5.3]** The sorted cost cannot satisfy the paper’s bound with any universal constant multiplier. The ratio grows as \((\log N)^{1/4}\).

**[PROVED — exact finite arithmetic check]** At \(i=j=1,h=4\), the code used

\[
\begin{aligned}
N&=3(2^{524289}+2^{458748}+2^{393208}+2^{327684}),\\
B_2&=5\cdot2^{524288},\\
Q_{\rm lower}&=2^{589827},
\end{aligned}
\]

and directly verified, in integers,

\[
\boxed{
(Q_{\rm lower}-N)^8>(N/3)^3B_2^6.
}
\]

The bit lengths of \((N,B_2,Q_{\rm lower})\) were exactly

\[
(524291,\ 524291,\ 589828).
\]

The graph was not materialized. Its simultaneous adversarial labeling is established by the proof.

---

**[PROVED — Theorem 5.10’s \(1/6\), \(1/4\), and \(1/5\) separations]**

All three requested separations against \(N+B_2\) survive **without a logarithmic loss**.

**The \(1/6\) separation: \(\mathcal F_a\).** Use

\[
R=X\times Y,\quad
S=\{(y_i,z_{i,k})\},\quad
T=\{(z_{i,k},x_i)\},
\]

with \(i,k<a\), and order \(z_{i,k}\) by \((k,i)\).

For every off-diagonal \(R\)-tuple \((x_i,y_j)\), the two length-\(a\) runs alternate. The total necessary comparisons, ignoring diagonal rows, are

\[
a(a-1)(2a-1)=\Theta(a^3).
\]

Merge supplies the matching upper bound. Since

\[
N=3a^2,\qquad B_2=a^{8/3},
\]

the fixed-\(R\) GAO has gap

\[
\Theta(a^{1/3})=\Theta(N^{1/6}).
\]

This instance is already pairwise semijoin-reduced. Rotating gives the corresponding lower bound for either other fixed second relation.

The three-rotation union \(\mathcal G_a\), with concatenated component orders, forces every GAO to encounter a hard copy.

**The \(1/4\) separation: GMR.** Give each of the \(m^3\) vertices \(x\) a private \(m\)-element \(T\)-predecessor set \(B_x\). Let \(|Y|=|Z_1|=m\),

\[
R=X\times Y,\qquad S=Y\times Z_1.
\]

Layer the common \(Z_1\) against every \(B_x\). Every one of the \(m^4\) \(R\)-rows requires \(2m-1\) comparisons, giving

\[
m^4(2m-1)=\Theta(m^5).
\]

Exactly,

\[
N=2m^4+m^2,\qquad B_2=m^4.
\]

Thus the gap is \(\Theta(m)=\Theta(N^{1/4})\).

**The \(1/5\) separation: GMIN.** The part sizes are:

| Domain | Part 0 | Part 1 | Part 2 | Part 3 |
|---|---:|---:|---:|---:|
| \(X\) | \(m^3\) | \(m^5\) | \(m^2\) | \(m\) |
| \(Y\) | \(m\) | \(m^3\) | \(m^2\) | \(m^5\) |
| \(Z\) | \(m^5\) | \(m^2\) | \(m\) | \(m^3\) |

Use the paper’s blocks

\[
\begin{aligned}
R&=X_0\times Y_0\ \cup\ (X_1\to Y_1)\ \cup\ X_3\times Y_2,\\
S&=Y_0\times Z_1\ \cup\ Y_1\times Z_2\ \cup\ (Y_3\to Z_3),\\
T&=(Z_0\to X_0)\ \cup\ Z_2\times X_2\ \cup\ Z_3\times X_3.
\end{aligned}
\]

Realize each arrow as private length-\(m^2\) predecessor sets. Independently layer:

- common \(Z_1\) against every \(Z_0\)-fiber;
- common \(X_2\) against every \(X_1\)-fiber;
- common \(Y_2\) against every \(Y_3\)-fiber.

These constraints concern disjoint domains and therefore combine into one order.

Each driven relation has \(m^4\) hard rows, each requiring \(2m^2-1\) comparisons:

\[
L_R=L_S=L_T=m^4(2m^2-1)=\Theta(m^6).
\]

All remaining rows meet an empty run. Exactly,

\[
N=3(m^5+m^4+m^3),\qquad B_2=3m^5.
\]

Thus even the best GAO has gap \(\Theta(N^{1/5})\). The inexpensive adaptive options visit only \(\Theta(m^5)\) tuples with empty intersections, so this gap also holds against adaptive execution plus \(N\).

**[PROVED — padded GMIN]** Put all fresh padding keys before original keys. The hard original runs are unchanged. Keep the cheap \(x\)-root choices:

- \(X_0\): option \(T\);
- \(X_3\): option \(R\);
- \(X_1\): its new singleton \(T\)-option;
- \(X_2\): its new singleton \(R\)-option.

Their intersections are constant-sized or search for a fresh singleton before all original keys, so forward galloping takes \(O(1)\) comparisons per visited edge. Fresh vertices also have constant-cost choices.

Exactly,

\[
N'=12m^5+3m^4+3m^3+9m^2,
\]

\[
B_2'=8m^5+3m^2,\qquad
\operatorname{Out}'=3m^5+3m^2.
\]

Thus adaptive execution is \(\Theta(N')\), while every GAO still requires \(\Theta(m^6)\).

The exact certificate checks were:

| Parameter | \(\mathcal F_a\), hard \(R\)-rows | GMR | GMIN, each driver | Padded GMIN, each driver |
|---:|---:|---:|---:|---:|
| 2 | 6 | 48 | 112 | 112 |
| 3 | 30 | 405 | 1,377 | 1,377 |
| 4 | 84 | 1,792 | 7,936 | 7,936 |
| 5 | 180 | 5,625 | 30,625 | 30,625 |

Padded GMIN statistics were:

| \(m\) | \(N'\) | \(B_2'\) | Output |
|---:|---:|---:|---:|
| 2 | 492 | 268 | 108 |
| 3 | 3,321 | 1,971 | 756 |
| 4 | 13,392 | 8,240 | 3,120 |
| 5 | 39,975 | 25,075 | 9,450 |

**[PROVED — fixed-root separation]** For \(\mathcal H_a\), alternate \(Y_1,Y_2\), and layer common \(Z_2\) against every private length-\(a\) \(Z_1\)-fiber. Both options at every \(x\) contain \(a\) alternating length-\(a\) intersections. Each option’s aggregate certificate is

\[
a^2(2a-1).
\]

Thus fixed root \(x\) costs \(\Theta(a^3)\), whereas root \(y\) costs \(\Theta(a^2)\). Fresh-first padding preserves these bounds, giving the paper’s \(\Theta(N^{1/2})\) gap against adaptive execution plus input size. The certificate totals for \(a=2,3,4,5\) were **12, 45, 112, 225**, unchanged by padding.

**[PROVED — qualification for the separate \(\mathcal F_a/\mathcal G_a\) comparison against adaptive cost]** Cheap options there perform singleton membership in long runs. Ordinary stateless sorted search gives \(O(a^2\log a)\) adaptive work, so the paper’s literal constant-factor \(\Theta(a)\) ratio against its min-side \(C\) should not be transferred unchanged. This issue does not affect the requested \(1/6\) ratio against \(N+B_2\).

---

**[PROVED — faithful engine port and exact \(G_8\) measurements]**

The Python port follows:

- `intersectEachBy`;
- `intersectWalk`;
- `equalRunEnd`;
- `dropsAt`;
- `gallopLowerBoundBy`, including its 16-entry linear prefix;
- `lowerBoundBy`.

It separately counts:

1. every primitive key predicate;
2. the Zig `work` meter;
3. the `walked` test meter.

A relevant detail is that `intersectEachBy` walks its **first argument on equal lengths**. The actual triangle call site passes `intersectEachBy(n2,n3)`. Consequently:

- option \(R\) calls \((Z_1,T_x)\);
- option \(T\) calls \((Y_{2,z},Y_0)\).

For the first orientation of an alternating length-\(s\) pair, the port performs

\[
6s-3
\]

primitive comparisons, decomposed as

\[
(s-1)\text{ lookahead equalities}
+(2s-1)\text{ disorder checks}
+(2s-1)\text{ gallop comparisons}
+s\text{ match equalities}.
\]

Reversing the balanced pair gives \(6s-5\): the last gallop exhausts the other run and avoids two predicates.

Both orientations report Zig work \(3s-1\). Every gallop in these particular witnesses advances at most one position; the exponential branch is unnecessary.

The measured per-call counts were:

| \(m\) | \(Z_1\) versus \(T_x\): comparisons | \(Y_{2,z}\) versus \(Y_0\): comparisons | Zig work, respectively |
|---:|---:|---:|---:|
| 2 | 45 | 19 | 23, 11 |
| 3 | 159 | 49 | 80, 26 |
| 4 | 381 | 91 | 191, 47 |
| 5 | 747 | 145 | 374, 74 |

Including one outer visit per tuple,

\[
q_R(x)=6m^5-2m^2,
\qquad
q_T(x)=6m^5+m^4-4m^3.
\]

Thus the comparison-plus-outer optimum selects \(T\) at \(m=2,3\), and \(R\) for every integer \(m\ge4\). Each root of the rotated union costs

\[
Q(m)=m^4\min(q_R(x),q_T(x))+m^8+m^5.
\]

The exact results are:

| \(m\) | \(N\) | \(B_2\) | Primitive comparisons + outer visits \(Q\) | \(Q/m^9\) | Zig work + outer visits | Optimal ternary + outer |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 2,208 | 1,280 | 3,104 | \(97/16\) | 1,824 | 1,312 |
| 3 | 48,843 | 32,805 | 122,715 | \(505/81\) | 65,853 | 46,170 |
| 4 | 457,728 | 327,680 | 1,631,232 | \(1593/256\) | 852,992 | 590,848 |
| 5 | 2,634,375 | 1,953,125 | 12,081,250 | \(3866/625\) | 6,253,125 | 4,300,000 |

For the selected plans, the primitive comparison counts alone were

\[
2,432;\quad107,163;\quad1,560,576;\quad11,671,875,
\]

and their outer-visit counts were

\[
672;\quad15,552;\quad70,656;\quad409,375.
\]

If outer visits are excluded from the optimization objective, option \(T\) always wins. The pure-comparison minima are

\[
6m^9-5m^7
=
2,432;\quad107,163;\quad1,490,944;\quad11,328,125.
\]

For \(m\ge4\),

\[
Q(m)=6m^9+m^8-2m^6+m^5.
\]

Thus the measurements satisfy an exact degree-nine formula, while \(N\) has degree eight. The exact \(m=2\) to \(m=4\) ratios are

\[
\frac{Q(4)}{Q(2)}=\frac{50976}{97},
\qquad
\frac{N(4)}{N(2)}=\frac{4768}{23}.
\]

No floating-point exponent fit was used. These finite measurements confirm the derived \(\Theta(m^9)=\Theta(N^{9/8})\) behavior of the original interleaved \(G_8\).

**[PROVED — verification scope]** The port passed **15,876** sorted bag-pair checks, **9,920** lower-bound searches including exponential/binary paths, one stopping-callback case, and one out-of-order case.

The measurements executed **144, 1,539, 8,448, and 31,875** local port calls, respectively, covering every relevant row shape and both balanced argument orders. Repeated query invocations were aggregated by exact integer multiplicities; the modeled executor receives no cache.

These are intersection-port operation counts plus outer visits. Relation seeks, sorting, planning, and full-driver overhead are outside these totals.

---

**[REFUTED / OPEN-WITH-OBSTRUCTION — limits of the result]**

**[REFUTED]** A universal claim about arbitrary comparison-based join evaluation would be false for these examples. In unpadded \(G_8\), support pruning removes the \(S\)-edges into \(Z_1\), then the \(R\)-edges. Repeated intersections can also be computed once and reused. The per-row certificate cannot be summed when earlier calls supply its comparisons for free.

This is consistent with Proposition 5.16: degree metadata can determine an entire Ferrers instance. A generic local intersection lower bound is not a lower bound against global inference from that metadata.

**[OPEN-WITH-OBSTRUCTION]** The value-range-order part of open problem 5 remains outside this proof. Allowing different roots in different regions changes the algorithmic class; the concatenated rotated components themselves permit useful regional choices. The results above settle sorted intersections for the paper’s fixed-root/per-binding-option architecture, with fresh intersection calls.

The quarter-log theorem was independently audited for its degree formulas, decision-tree argument, simultaneous ordering, and quantifiers.

Reproducible scratch artifacts:

- [Faithful intersection port](engine/gallop_port.py)
- [G8 measurement runner](engine/measure_g8.py) and [exact results](engine/g8_counts.json)
- [Original slope-family checks](slopes/verify_families.py)
- [Quarter-log proof](slopes/log_normalized_proof.md) (an earlier draft is `slopes/quarter_log_proof.md`), [exact checks](slopes/log_normalized_checks.py), and [finite integer refutation](slopes/log_normalized_finite.py)
- [Separation checks](separations/check.py) and [exact output](separations/exact-output.txt)

All executable checks were run with `python3 -I`, using integers and `Fraction` for load-bearing arithmetic.