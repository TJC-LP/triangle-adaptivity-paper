> Archived research report (problem P2, exponent questions), verbatim except that machine-local paths were removed. Verdicts and paper-ready statements: `../verified.md` §2. One item needed a repair: the single-order result (d) is exact 1/4 on general inputs only; on pairwise semijoin-reduced inputs the single-GAO gap lies in [1/5, 1/4] (`../verified.md` P2.13).

**[Proved] Questions (b), (c), and (d) are settled. Question (a) remains open, with a stronger verified lower bound.**

Write \(D=N+B_2\). The results are:

| Question | Status | Result |
|---|---|---|
| (a) Fully reduced inputs | **Open-with-obstruction** | The gap \(C/D=N^{\delta+o(1)}\) has \(\delta\in[1/12,1/8]\). In the alternative normalization \(C=D^{\rho+o(1)}\), the interval is \([15/14,9/8]\). |
| (b) Slopes \(5/6<\kappa<1\) | **Proved** | \(C=O(D)\) for \(\kappa\le9/10\). For every real \(9/10<\kappa<1\), the sharp exponent is \(C=\Theta(N^{(10\kappa-1)/8})\). |
| (c) Best of six fixed orders | **Proved** | Exact gap \(1/5\), hence exact comparator exponent \(6/5\). |
| (d) One prescribed fixed order | **Proved** | Exact gap \(1/4\), hence exact comparator exponent \(5/4\). |

**[Refuted]** Theorem 5.3’s exponent \(3/8+3\kappa/4\) is sharp throughout the interval \((5/6,1)\). The improved bound below is strictly stronger there.

All constructions and proofs concern the paper’s full shorter-run charges. They do not assert matching lower bounds for actual galloping comparisons. In particular, the inspected `intersectWalk` returns when its longer-run cursor reaches the end. All files written and computations performed were in the private scratch directory; no repository was edited.

---

**[Proved] Definitions and conventions.**

Let
\[
R\subseteq X\times Y,\quad S\subseteq Y\times Z,\quad
T\subseteq Z\times X,\qquad
r=|R|,\ s=|S|,\ t=|T|,\quad N=r+s+t.
\]
Put
\[
\begin{aligned}
\alpha&=\sum_x d_R^+(x)^2,&
\beta&=\sum_y d_S^+(y)^2,&
\gamma&=\sum_z d_T^+(z)^2,\\
\alpha'&=\sum_y d_R^-(y)^2,&
\beta'&=\sum_z d_S^-(z)^2,&
\gamma'&=\sum_x d_T^-(x)^2,
\end{aligned}
\]
and
\[
Q=\min(\alpha\beta\gamma,\alpha'\beta'\gamma'),
\qquad B_2=Q^{1/3}.
\]

The \(R\)-driven probe charge is
\[
M_R=\sum_{(x,y)\in R}\min(d_S^+(y),d_T^-(x)),
\]
with cyclic definitions for \(M_S,M_T\). A fixed order driven by \(R\) costs \(r+M_R\).

At root \(x\), the two options cost
\[
\begin{aligned}
c_R(x)&=\sum_{y\in R(x)}
 \left(1+\min(d_S^+(y),d_T^-(x))\right),\\
c_T(x)&=\sum_{z\in T^-(x)}
 \left(1+\min(d_R^+(x),d_S^-(z))\right).
\end{aligned}
\]
Define \(C_x=\sum_x\min(c_R(x),c_T(x))\), cyclically define \(C_y,C_z\), and let \(C=\min(C_x,C_y,C_z)\).

### (b): the transition is exactly \(9/10\)

**[Proved] A stronger universal per-binding upper bound is**
\[
\boxed{C\le N+3^{1/8}N^{-1/8}B_2^{5/4}}\qquad(N>0).
\tag{1}
\]
Its exact integer form is
\[
\boxed{N^3(C-N)_+^{24}\le27Q^{10}.}
\tag{2}
\]

Here is a complete proof. For root \(x\), abbreviate
\[
a_x=d_R^+(x),\quad t_x=d_T^-(x),\quad
b_y=d_S^+(y),\quad e_z=d_S^-(z),
\]
and set
\[
P_x=\sum_{y\in R(x)}\min(b_y,t_x),\qquad
V_x=\sum_{z\in T^-(x)}\min(a_x,e_z),\qquad
H_x=\sum_x\min(P_x,V_x).
\]
Separating scan charges gives
\[
C_x\le r+t+H_x,\qquad
(C-N)_+\le\min(H_x,H_y,H_z).
\tag{3}
\]

Cauchy–Schwarz over the distinct neighbors of \(x\) gives
\[
P_x\le\sqrt{a_x\beta}.
\]
Writing \(w_x=\sum_{z\in T^-(x)}\sqrt{e_z}\), the inequality
\(\min(a,e)\le\sqrt{ae}\) gives \(V_x\le\sqrt{a_x}w_x\). Consequently,
\[
\min(P_x,V_x)\le P_x^{1/4}V_x^{3/4}
 \le\beta^{1/8}a_x^{1/2}w_x^{3/4}.
\]
Hölder and then double counting give
\[
H_x\le\beta^{1/8}\alpha^{1/4}
       \left(\sum_xw_x\right)^{3/4},
\]
\[
\sum_xw_x
 =\sum_z d_T^+(z)\sqrt{e_z}
 \le\sqrt{\gamma s}.
\]
Thus
\[
H_x\le s^{3/8}\alpha^{1/4}\beta^{1/8}\gamma^{3/8}.
\tag{4}
\]
Since integer degrees satisfy \(d^2\ge d\), \(s\le\beta\), so
\[
H_x\le\alpha^{1/4}\beta^{1/2}\gamma^{3/8}.
\]
Its cyclic rotation is
\[
H_y\le\alpha^{3/8}\beta^{1/4}\gamma^{1/2}.
\]
Therefore
\[
(C-N)_+
 \le H_x^{2/3}H_y^{1/3}
 \le(\alpha\beta\gamma)^{5/12}\alpha^{-1/8}.
\tag{5}
\]
If \(C>N\), the moments in this expression are positive. Rotate the instance so that \(R\) is a largest relation. Then
\[
\alpha\ge r\ge N/3.
\]
Apply the argument in whichever orientation realizes \(Q\), reflecting first if necessary. Equation (5) becomes (1). The case \(C\le N\) is immediate.

**[Proved]** This also recovers the original universal upper bound needed below: multiply (4) and its two rotations, take a cube root, and apply the better orientation:
\[
\boxed{C\le N+(rst)^{1/8}B_2^{3/4}
       \le N+(N/3)^{3/8}B_2^{3/4}.}
\tag{6}
\]

**[Proved]** If \(B_2=\Theta(N^\kappa)\), (1) gives
\[
C=O\!\left(N+N^{(10\kappa-1)/8}\right).
\tag{7}
\]
Thus \(C=O(N+B_2)\) throughout \(5/6<\kappa\le9/10\). Above \(9/10\), the following family attains (7).

**[Proved] An explicit building block.** For positive integers \(L,a,h\) with \(h\mid L\), put \(b=L/h\). Use disjoint tagged classes
\[
X=[h]\times[b],\quad Y_0=[a],\quad Y_2=[h]^2\times[a],
\quad Z_1=[h],\quad Z_2=[h]^2.
\]
Define \(D(L,a,h)\) by
\[
R=X\times Y_0,
\]
\[
S=(Y_0\times Z_1)
 \cup\{((i,j,k),(i,j)):i,j\in[h],\,k\in[a]\},
\]
\[
T=\{((i,j),(i,\ell)):i,j\in[h],\,\ell\in[b]\}.
\]

Its exact statistics are
\[
\begin{aligned}
(r,s,t)&=(La,ah+ah^2,Lh),\\
(\alpha,\beta,\gamma)&=(La^2,2ah^2,L^2),\\
(\alpha',\beta',\gamma')&=(aL^2,a^2(h+h^2),Lh^2),\\
(M_R,M_S,M_T)&=(Lah,0,Lah),\\
(C_x,C_y,C_z)&=(Lah+L\min(a,h),ah,ah^2),\\
\mathrm{Out}&=0.
\end{aligned}
\tag{8}
\]

To verify the costs, an \(R\)-edge sees degrees \(h,h\), while a \(T\)-edge sees degrees \(a,a\). Every \(S\)-edge has one zero adjacent degree. At each \(x\), the two options are \(a(1+h)\) and \(h(1+a)\). At \(Y_0\), choosing \(S\) costs \(h\); at \(Y_2\), the \(R\)-option is empty. At \(Z_1\), the \(T\)-option is empty; at \(Z_2\), choosing \(S\) costs \(a\), while choosing \(T\) costs \((L/h)(1+a)>a\). This proves all cost formulas; the moment formulas follow directly from the constant degrees.

**[Proved] The asymmetric slope family.** Let \(u\ge2\) and let positive integers \(p,q\) satisfy
\[
9/10\le p/q\le1.
\]
Take these three vertex-disjoint gadgets:

| Gadget | \(L\) | \(a\) | \(h\) | Local \((R,S,T)\) becomes |
|---|---:|---:|---:|---|
| \(D_1\) | \(u^{8p-4q}\) | \(u^{6q-4p}\) | \(u^{6p-3q}\) | \((R,S,T)\) |
| \(D_2\) | \(u^{4q}\) | \(u^{4p-2q}\) | \(u^{6p-3q}\) | \((S,T,R)\) |
| \(D_3\) | \(u^{4p}\) | \(u^{6p-4q}\) | \(u^{6q-3p}\) | \((T,R,S)\) |

All parameters are integers and \(h_i\mid L_i\). The exponent differences establishing divisibility are
\[
2p-q,\quad7q-6p,\quad7p-6q.
\]
The differences establishing \(a_i\le h_i\) are
\[
10p-9q,\quad2p-q,\quad10q-9p.
\]
All are nonnegative.

By (8), the exact forward moments are
\[
(\alpha,\beta,\gamma)
 =(4u^{8q},4u^{8p},4u^{16p-8q}).
\tag{9}
\]
The reverse moments are
\[
\begin{aligned}
\alpha'&=2u^{12p-2q}+u^{9p-2q}+u^{6p+4q},\\
\beta'&=u^{9q-2p}+2u^{4p+6q}+u^{12q-2p},\\
\gamma'&=2u^{20p-10q}+u^{14p-7q}+u^{14p-4q}.
\end{aligned}
\tag{10}
\]
Each reverse moment is at least its forward counterpart: select the terms with exponents \(6p+4q,12q-2p,14p-4q\). Their excesses over \(8q,8p,16p-8q\) are respectively
\[
6p-4q,\quad12q-10p,\quad4q-2p,
\]
integers at least two. Since \(u\ge2\), these terms alone provide the required factor four. Hence
\[
\boxed{B_2=4u^{8p}.}
\tag{11}
\]

The exact root costs are
\[
\begin{aligned}
C_x&=u^{10p-q}+u^{4p+2q}+u^{16p-8q}+u^{3p+2q},\\
C_y&=u^{10p-q}+u^{4p+2q}+u^{8q}+u^{2p+3q},\\
C_z&=u^{7p+2q}+u^{10p-4q}+u^{8p}+u^{10p-5q}.
\end{aligned}
\tag{12}
\]
Here \(C_x\le C_y\) termwise. Every term of \(C_x\) is at most \(u^{10p-q}\). If \(p<q\), the leading term of \(C_z\) is at least \(8u^{10p-q}>C_x\); if \(p=q\), all three costs coincide. Thus
\[
\boxed{C=C_x.}
\tag{13}
\]

The exact input size is
\[
\begin{aligned}
N={}&2u^{4p+2q}+u^{2p+3q}+u^{8p}+u^{14p-7q}
 +u^{10p-5q}+u^{16p-8q}\\
 &+u^{6p+q}+u^{10p-4q}+u^{3p+2q}
 +u^{8q}+u^{p+6q}.
\end{aligned}
\tag{14}
\]
All exponents are at most \(8q\), and the coefficients sum to twelve. Therefore
\[
u^{8q}\le N\le12u^{8q},\qquad
u^{10p-q}\le C\le4u^{10p-q}.
\tag{15}
\]

For fixed rational \(\kappa=p/q\in(9/10,1)\), equations (11)–(15) give
\[
\boxed{B_2=\Theta(N^\kappa),\qquad
C=\Theta\!\left(N^{(10\kappa-1)/8}\right).}
\tag{16}
\]
Consequently
\[
\boxed{\frac{C}{N+B_2}
 =\Theta\!\left(N^{(10\kappa-9)/8}\right).}
\tag{17}
\]

**[Refuted]** \(C=O(N+B_2)\), even with any fixed polylogarithmic factor, at every slope \(\kappa\in(9/10,1)\).

**[Proved] Irrational slopes are included.** Fix \(u=2\), let \(q\to\infty\), and set \(p=\lfloor\kappa q\rfloor\). Eventually \(9/10\le p/q<1\). Since \(-1<p-\kappa q\le0\), the discrepancy changes every relevant power of two by a bounded factor. The uniform bounds (15) therefore prove (16) and (17) for irrational \(\kappa\) as well.

**[Proved: exact finite checks]** Literal enumeration verified seven explicit \(D\)-gadgets, another 100 deterministic pseudorandom gadgets, and the three complete unions below. These calculations recomputed degrees and costs from relation tuples.

| \(u\), with \(p=q=1\) | Each relation size | Each forward moment | Each reverse moment | Each \(M_\pi\) | \(N\) | \(B_2\) | \(C\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 480 | 1,024 | 3,200 | 1,024 | 1,440 | 1,024 | 864 |
| 3 | 9,720 | 26,244 | 179,334 | 39,366 | 29,160 | 26,244 | 27,216 |
| 4 | 87,040 | 262,144 | 3,162,112 | 524,288 | 261,120 | 262,144 | 332,800 |

For the proper rational slopes, the graphs are enormous. The following are **exact evaluations of their proved degree-class formulas, not literal enumeration**:

```text
u=2, p=9, q=10:
N  = 1214275593117998941995008
B₂ = 18889465931478580854784
C  = 1208944338557034410541056
C/(N+B₂) = 1099528470656/1121557087617

u=2, p=10, q=11:
N  = 310776595586757567692406784
B₂ = 4835703278458516698824704
C  = 618974746625362625149534208
C/(N+B₂) = 17592320393344/8970241051009

u=2, p=19, q=20:
N  = 1467233647608522269153623626141259710658154332160
B₂ = 22835963083295358096932575511191922182123945984
C  = 1496577698927589869848104603119462669939164785410048
C/(N+B₂) = 1208925837629027751297152/1203668645819051934081
```

### (c): best of six has exact exponent \(6/5\)

**[Proved] The stronger sharp inequality is**
\[
\boxed{\min(M_R,M_S,M_T)^5\le rst\,Q.}
\tag{18}
\]
Equivalently,
\[
\boxed{\min_\pi M_\pi\le(rst)^{1/5}B_2^{3/5}
 \le(N/3)^{3/5}B_2^{3/5}.}
\tag{19}
\]

For the proof, put \(a_x=d_R^+(x)\), \(t_x=d_T^-(x)\), and
\[
P_x=\sum_{y\in R(x)}\min(d_S^+(y),t_x).
\]
We have both
\[
P_x\le a_xt_x,\qquad P_x\le\sqrt{a_x\beta}.
\]
Interpolating these two bounds gives
\[
P_x\le(a_xt_x)^{3/5}(a_x\beta)^{1/5}
 =\beta^{1/5}(a_x^2)^{2/5}t_x^{3/5}.
\]
Hölder now yields
\[
M_R\le t^{3/5}\alpha^{2/5}\beta^{1/5}.
\tag{20}
\]
Its rotations are
\[
M_S\le r^{3/5}\beta^{2/5}\gamma^{1/5},\qquad
M_T\le s^{3/5}\gamma^{2/5}\alpha^{1/5}.
\]
Multiply and take a cube root:
\[
\min_\pi M_\pi\le(rst\,\alpha\beta\gamma)^{1/5}.
\]
Reflection gives the same inequality with the primed product, proving (18). Empty relations cause no difficulty: all three probe charges then vanish.

**[Proved]** The constant one in (18) is sharp. On a complete tripartite instance with part sizes \(a,b,c\), every \(M_\pi=abc\), \(rst=(abc)^2\), and both moment products equal \((abc)^3\).

Writing \(v=B_2/N\), equation (19) gives
\[
\frac{\min_\pi M_\pi}{N+B_2}
 \le3^{-3/5}N^{1/5}\frac{v^{3/5}}{1+v}.
\]
The scalar factor is maximized at \(v=3/2\), so
\[
\boxed{\min_\pi M_\pi
 \le\frac{2^{2/5}}5N^{1/5}(N+B_2).}
\tag{21}
\]
Also, \(NB_2\le(N+B_2)^2/4\) gives
\[
\boxed{\min_\pi M_\pi\le12^{-3/5}(N+B_2)^{6/5}.}
\tag{22}
\]
The scan charge is at most \(N\), so it does not change either exponent.

**[Proved] A matching explicit family.** Define a second gadget \(H(L,a,h)\) using
\[
|X|=L,\quad |Y|=a,\quad |Z_1|=h,\quad
Z_0=\{z_{x,j}:x\in X,\ j\in[h]\},
\]
with
\[
R=X\times Y,\qquad S=Y\times Z_1,\qquad
T=\{(z_{x,j},x):x\in X,\ j\in[h]\}.
\]
Direct counting gives
\[
\begin{aligned}
(r,s,t)&=(La,ah,Lh),\\
(\alpha,\beta,\gamma)&=(La^2,ah^2,Lh),\\
(\alpha',\beta',\gamma')&=(aL^2,ha^2,Lh^2),\\
(M_R,M_S,M_T)&=(Lah,0,0),\\
(C_x,C_y,C_z)&=(Lh,ah,0),\qquad \mathrm{Out}=0.
\end{aligned}
\tag{23}
\]
Indeed, only \(R\)-edges have nonzero intersection budgets, and every such budget is \(h\). The cheap root-\(x\) option walks its private \(T\)-leaves; the cheap root-\(y\) option walks \(S\); every \(z\) has an empty option.

Take the union of three cyclic rotations of \(H(m^3,m,m^2)\). This is an explicit realization of GMIN. It has
\[
\begin{aligned}
r=s=t&=m^5+m^4+m^3,&N&=3(m^5+m^4+m^3),\\
\alpha=\beta=\gamma&=3m^5,&
\alpha'=\beta'=\gamma'&=2m^7+m^4,\\
B_2&=3m^5,&M_R=M_S=M_T&=m^6,\\
C_x=C_y=C_z&=m^5+m^3,&\mathrm{Out}&=0.
\end{aligned}
\tag{24}
\]
For the orientation minimum,
\[
2m^7+m^4-3m^5
 =m^4(m-1)(2m^2+2m-1)\ge0.
\]
Thus
\[
\frac{\min_\pi M_\pi}{N+B_2}
 =\frac{m^3}{6m^2+3m+3}
 =\Theta(N^{1/5}),
\]
and \(\min_\pi M_\pi=\Theta((N+B_2)^{6/5})\). This proves both claimed optimal exponents.

**[Proved: exact finite checks]** Literal enumeration produced:

| \(m\) | \(N\) | \(B_2\) | Each reverse moment | Each \(M_\pi\) | Each \(C_v\) | \(M/(N+B_2)\) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 3 | 3 | 1 | 2 | \(1/12\) |
| 2 | 168 | 96 | 272 | 64 | 40 | \(8/33\) |
| 3 | 1,053 | 729 | 4,455 | 729 | 270 | \(9/22\) |
| 4 | 4,032 | 3,072 | 33,024 | 4,096 | 1,088 | \(64/111\) |
| 5 | 11,625 | 9,375 | 156,875 | 15,625 | 3,250 | \(125/168\) |
| 6 | 27,864 | 23,328 | 561,168 | 46,656 | 7,992 | \(72/79\) |
| 7 | 58,653 | 50,421 | 1,649,487 | 117,649 | 17,150 | \(343/318\) |
| 8 | 112,128 | 98,304 | 4,198,400 | 262,144 | 33,280 | \(512/411\) |

All output counts were zero. Another 10,000 deterministic random instances satisfied all six individual fifth-power inequalities and (18). The maximum exact ratio in (18) was \(1\), attained by a complete tripartite instance with part sizes \((1,2,1)\): both sides equal \(32\).

### (d): one prescribed order has exact exponent \(5/4\)

**[Proved] For the prescribed driver \(R\),**
\[
\boxed{M_R^4\le rt^2\alpha\beta\le rt\,\alpha\beta\gamma,}
\tag{25}
\]
\[
\boxed{M_R^4\le rs^2\alpha'\gamma'\le rs\,\alpha'\beta'\gamma'.}
\tag{26}
\]

For a complete proof, retain \(a_x,t_x,P_x\) from above and put \(b_y=d_S^+(y)\). Terms with \(t_x=0\) have \(P_x=0\). Weighted Cauchy–Schwarz gives
\[
M_R^2\le t\sum_{x:t_x>0}\frac{P_x^2}{t_x}.
\]
Since \(\min(b,t)^2\le bt\),
\[
\frac{P_x^2}{t_x}
 \le\left(\sum_{y\in R(x)}\sqrt{b_y}\right)^2
 \le a_x\sum_{y\in R(x)}b_y.
\]
Set \(v_y=\sum_{x:(x,y)\in R}a_x\). Then
\[
M_R^2\le t\sum_yb_yv_y
 \le t\sqrt{\beta}\sqrt{\sum_yv_y^2}.
\]
For each \(y\),
\[
v_y^2
 \le d_R^-(y)\sum_xa_x^2
 =d_R^-(y)\alpha.
\]
Summing gives \(\sum_yv_y^2\le r\alpha\), and hence
\[
M_R^2\le t\sqrt{r\alpha\beta}.
\]
This proves the first inequality in (25); \(\gamma\ge t\) proves the second. Grouping by \(y\) instead proves (26), using \(\beta'\ge s\).

Both \(rt\) and \(rs\) are at most \(N^2/4\). Choose the orientation defining \(Q\):
\[
\boxed{M_R\le(N/2)^{1/2}B_2^{3/4}.}
\tag{27}
\]
The maximum of \(v^{3/4}/(1+v)\) is \(3^{3/4}/4\), attained at \(v=3\). Therefore
\[
\boxed{M_R\le
 \frac{3^{3/4}}{4\sqrt2}\,N^{1/4}(N+B_2).}
\tag{28}
\]
Again, the additional scan charge \(r\le N\) does not affect the exponent.

**[Proved] Matching family.** Specialize (23) to \(H(m^3,m,m)\), the paper’s GMR:
\[
\begin{aligned}
(r,s,t)&=(m^4,m^2,m^4),&
N&=2m^4+m^2,\\
(\alpha,\beta,\gamma)&=(m^5,m^3,m^4),&
(\alpha',\beta',\gamma')&=(m^7,m^3,m^5),\\
B_2&=m^4,&M_R&=m^5,\\
(C_x,C_y,C_z)&=(m^4,m^2,0),&
M_S=M_T=\mathrm{Out}&=0.
\end{aligned}
\tag{29}
\]
Thus
\[
\frac{M_R}{N+B_2}
 =\frac{m^3}{3m^2+1}
 =\Theta(N^{1/4}),
\]
and \(M_R=\Theta((N+B_2)^{5/4})\). Relabeling handles any prescribed driver.

**[Proved] The coefficient in (28) is asymptotically sharp.** Use \(H(u^3,6u,6u)\). Then
\[
N=12u^4+36u^2,\qquad B_2=36u^4,\qquad M_R=36u^5.
\]
Consequently
\[
\lim_{u\to\infty}
\frac{M_R}{N^{1/4}(N+B_2)}
=\frac{36}{12^{1/4}\cdot48}
=\frac{3^{3/4}}{4\sqrt2}.
\]

**[Proved: exact finite checks]** Literal GMR enumeration gave:

| \(m\) | \(N\) | \(B_2\) | \(M_R\) | \(C_x\) | \(C_y\) | \(M_R/(N+B_2)\) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 1 | 1 | 1 | 1 | \(1/4\) |
| 2 | 36 | 16 | 32 | 16 | 4 | \(8/13\) |
| 3 | 171 | 81 | 243 | 81 | 9 | \(27/28\) |
| 4 | 528 | 256 | 1,024 | 256 | 16 | \(64/49\) |
| 5 | 1,275 | 625 | 3,125 | 625 | 25 | \(125/76\) |
| 6 | 2,628 | 1,296 | 7,776 | 1,296 | 36 | \(216/109\) |
| 7 | 4,851 | 2,401 | 16,807 | 2,401 | 49 | \(343/148\) |
| 8 | 8,256 | 4,096 | 32,768 | 4,096 | 64 | \(512/193\) |
| 9 | 13,203 | 6,561 | 59,049 | 6,561 | 81 | \(729/244\) |
| 10 | 20,100 | 10,000 | 100,000 | 10,000 | 100 | \(1000/301\) |
| 11 | 29,403 | 14,641 | 161,051 | 14,641 | 121 | \(1331/364\) |
| 12 | 41,616 | 20,736 | 248,832 | 20,736 | 144 | \(1728/433\) |

In every row \(C_z=M_S=M_T=\mathrm{Out}=0\). Literal checks of the sharp-coefficient family gave:

| \(u\) | \(N\) | \(B_2\) | \(M_R\) | \(M_R/(N+B_2)\) |
|---:|---:|---:|---:|---:|
| 1 | 48 | 36 | 36 | \(3/7\) |
| 2 | 336 | 576 | 1,152 | \(24/19\) |
| 3 | 1,296 | 2,916 | 8,748 | \(27/13\) |
| 4 | 3,648 | 9,216 | 36,864 | \(192/67\) |
| 5 | 8,400 | 22,500 | 112,500 | \(375/103\) |
| 6 | 16,848 | 46,656 | 279,936 | \(216/49\) |

### (a): a fully reduced separation, with the sharp exponent still open

**[Proved] There are fully reduced instances with**
\[
N=\Theta(v^{12}),\qquad B_2=\Theta(v^{14}),\qquad C=\Theta(v^{15}).
\tag{30}
\]
Thus
\[
\boxed{\frac{C}{N+B_2}=\Theta(N^{1/12}).}
\tag{31}
\]

Here is a coordinate construction requiring no finite field. Every coordinate ranges over \([v]\). Take
\[
X=\{(A,B):A,B\in[v]^3\},\quad
Y_0=[v]^4,\quad Z_1=[v]^5,
\]
\[
Y_2=\{(A,B,E,e):A,B,E\in[v]^3,\ e\in[v]\},
\]
\[
Z_2=\{(A,E,F):A,E\in[v]^3,\ F\in[v]^2\}.
\]
All classes are separately tagged. Write \(B=(B_1,B_2,B_3)\) and define the surjection
\[
f(A,B)=(A,B_1,B_2)\in Z_1.
\]

The relations are the unions of these blocks:
\[
\begin{aligned}
R_0&=X\times Y_0,&
S_0&=Y_0\times Z_1,&
T_1&=\{(f(x),x):x\in X\},\\
R_2&=\{((A,B),(A,B,E,e))\},\\
S_2&=\{((A,B,E,e),(A,E,F))\},\\
T_2&=\{((A,E,F),(A,B))\}.
\end{aligned}
\tag{32}
\]
Unspecified coordinates in each displayed set range freely.

**[Proved] Every tuple is supported by a triangle.**

- An \(R_0\)-tuple is supported by \(f(x)\); an \(S_0\)-tuple by any preimage under \(f\); a \(T_1\)-tuple by any \(y_0\).
- An \(R_2\)-tuple is supported by any \(F\).
- An \(S_2\)-tuple is supported by the unique \(x=(A,B)\) specified by its \(Y_2\)-endpoint.
- A \(T_2\)-tuple is supported by any \(e\).

There are no mixed triangles because \(S\) connects only \(Y_0\) to \(Z_1\) and \(Y_2\) to \(Z_2\). Therefore, for this one gadget \(I_v\),
\[
\mathrm{Out}(I_v)=v^{10}+v^{12}.
\tag{33}
\]

**[Proved] Exact degrees and costs.**

| Class | One incident degree | Other incident degree |
|---|---:|---:|
| \(X\) | \(d_R^+=2v^4\) | \(d_T^-=v^5+1\) |
| \(Y_0\) | \(d_R^-=v^6\) | \(d_S^+=v^5\) |
| \(Y_2\) | \(d_R^-=1\) | \(d_S^+=v^2\) |
| \(Z_1\) | \(d_S^-=v^4\) | \(d_T^+=v\) |
| \(Z_2\) | \(d_S^-=v^4\) | \(d_T^+=v^3\) |

Thus
\[
(r,s,t)=(2v^{10},v^{12}+v^9,v^{11}+v^6),
\tag{34}
\]
\[
(\alpha,\beta,\gamma)=(4v^{14},2v^{14},v^{14}+v^7),
\tag{35}
\]
\[
(\alpha',\beta',\gamma')
 =(v^{16}+v^{10},v^{16}+v^{13},
   v^{16}+2v^{11}+v^6).
\tag{36}
\]

For each \(x\),
\[
c_R(x)=v^9+v^6+2v^4,\qquad
c_T(x)=v^9+v^5+v^4+1.
\]
The latter is smaller because their difference is
\[
v^6-v^5+v^4-1\ge0.
\]
At \(Y_0\), choosing \(S\) costs \(v^6+v^5\); at \(Y_2\), choosing \(R\) costs \(1+v^2\). At \(Z_1\), choosing \(T\) costs \(v^5+v\); at \(Z_2\), choosing \(S\) costs \(2v^4\), versus \(v^7+v^3\) for \(T\). These comparisons establish
\[
\begin{aligned}
C_x(I_v)&=v^{15}+v^{11}+v^{10}+v^6,\\
C_y(I_v)&=v^{12}+2v^{10}+v^9,\\
C_z(I_v)&=2v^{12}+v^{10}+v^6.
\end{aligned}
\tag{37}
\]

Let \(U_v\) be the disjoint union of \(I_v\) and its two cyclic rotations. Each root total is the sum of the three entries in (37). Hence
\[
\boxed{N(U_v)=3(v^{12}+v^{11}+2v^{10}+v^9+v^6),}
\tag{38}
\]
\[
\boxed{C(U_v)=v^{15}+3v^{12}+v^{11}+4v^{10}+v^9+2v^6,}
\tag{39}
\]
\[
\boxed{B_2(U_v)=7v^{14}+v^7,\qquad
\mathrm{Out}(U_v)=3(v^{12}+v^{10}).}
\tag{40}
\]
For (40), every forward moment equals \(7v^{14}+v^7\), and every reverse moment equals
\[
3v^{16}+v^{13}+2v^{11}+v^{10}+v^6.
\]
They agree at \(v=1\); for \(v\ge2\), the latter is larger already from its \(3v^{16}\) term.

Equations (38)–(40) prove (30) and (31). They also show that this fully reduced family attains Theorem 5.3’s exponent at slope \(\kappa=7/6\).

**[Refuted]** Full reduction restores \(C=O(N+B_2)\). Every tuple in this construction belongs to a triangle, yet
\[
C/(N+B_2)\sim v/7\longrightarrow\infty.
\]

**[Proved: exact finite checks]** Literal adjacency construction, evaluation of both options at every binding, triangle counting, and a triangle-support check for every tuple passed for \(v=1,2,3,4\):

| \(v\) | \(N\) | \(B_2\) | \(C\) | Out | \(C/(N+B_2)\) |
|---:|---:|---:|---:|---:|---:|
| 1 | 18 | 8 | 12 | 6 | \(6/13\) |
| 2 | 26,304 | 114,816 | 51,840 | 15,360 | \(18/49\) |
| 3 | 2,541,294 | 33,482,970 | 16,377,714 | 1,771,470 | \(11233/24708\) |
| 4 | 70,004,736 | 1,879,064,576 | 1,132,732,416 | 53,477,376 | \(276546/475847\) |

For example, at \(v=4\), literal enumeration of one gadget gave
\[
(r,s,t)=(2097152,17039360,4198400),
\]
\[
(\alpha,\beta,\gamma)
 =(1073741824,536870912,268451840),
\]
\[
(\alpha',\beta',\gamma')
 =(4296015872,4362076160,4303360000),
\]
\[
(C_x,C_y,C_z)=(1078988800,19136512,34607104),
\quad \mathrm{Out}=17825792.
\]

Exact formula evaluations beyond the enumerated sizes were:

| \(v\) | \(N\) | \(B_2\) | \(C\) | \(C/(N+B_2)\) |
|---:|---:|---:|---:|---:|
| 5 | 943,406,250 | 42,724,687,500 | 31,339,875,000 | \(334292/465793\) |
| 6 | 8,011,908,288 | 548,549,428,608 | 477,330,164,352 | \(10230842/11929041\) |
| 7 | 49,272,107,094 | 4,747,562,333,486 | 4,792,233,188,190 | \(4073331/4077242\) |
| 8 | 238,774,124,544 | 30,786,327,674,880 | 35,403,550,162,944 | \(45017942/39450457\) |

Thus \(v=8\) is an explicit fully reduced member with \(C>N+B_2\).

**[Open-with-obstruction]** The sharp fully reduced exponent remains unresolved. Bound (6) supplies the universal gap \(1/8\), while (31) supplies \(1/12\):
\[
\boxed{1/12\le\delta_{\mathrm{fully\ reduced}}\le1/8.}
\]
For the comparator-power normalization, this construction gives
\[
C=\Theta((N+B_2)^{15/14}),
\]
so the corresponding interval is
\[
\boxed{15/14\le\rho_{\mathrm{fully\ reduced}}\le9/8.}
\]

A concrete obstruction to importing the low-slope family is that full reduction implies
\[
\mathrm{Out}\ge\max(r,s,t)\ge N/3.
\]
Since \(B_2\) bounds output,
\[
\boxed{B_2\ge N/3}
\]
on every fully reduced instance. Consequently no fully reduced family has asymptotic slope \(\kappa<1\). The paper’s suggested fully reduced gap \(1/10\) is not established by this report.

---

**[Proved: verification record]** Every reported calculation used `python3 -I` and integer or `Fraction` arithmetic. The analytic proofs establish the universal inequalities; finite checks provide independent validation.

The new per-binding integer inequality (2) also passed 5,000 random instances with seed `314159`. Its largest measured exact ratio was
\[
\frac{
390542412019613042979529897749423980712890625
}{
408199529820044454560361263205395741513176815873979797542464
},
\]
at \((N,C,Q)=(211,601,188201832)\).

The executable verification files are:

- [Intermediate-slope construction checks](verify_slopes.py)
- [New per-binding upper-bound checks](verify_new_upper.py)
- [Best-of-six checks](best_six_verify.py)
- [Single-order checks](verify_single_order.py)
- [Fully reduced construction and every-tuple support checks](verify_fully_reduced.py)