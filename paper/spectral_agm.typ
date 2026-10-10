#set document(title: "Levels of adaptivity and spectral worst-case bounds for labeled triangle joins", author: "A. Richard Caputo III")
// =====================================================================
// Levels of adaptivity and spectral worst-case bounds for labeled
// triangle joins.
// arXiv-style article, Typst source. First public version, 2026-10-09.
// All cross-references use labels; do not hard-code result numbers.
// =====================================================================

// ---------- page & typography ----------
#set page(
  paper: "us-letter",
  margin: (x: 1.25in, top: 1.2in, bottom: 1.15in),
  numbering: "1",
)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 1.2em)
#set footnote(numbering: "*")

#show raw: set text(font: "DejaVu Sans Mono", size: 0.86em)
#show raw.where(block: true): it => block(
  width: 100%,
  inset: (left: 1.6em, top: 0.35em, bottom: 0.35em),
  it,
)

// ---------- headings ----------
#set heading(numbering: "1.1.")
#show heading.where(level: 1): set text(size: 12pt)
#show heading.where(level: 2): set text(size: 11pt)
#show heading: set block(above: 1.6em, below: 1.0em)

// ---------- references to equations render as "(1)" ----------
#show ref: it => {
  let el = it.element
  if el != none and el.func() == math.equation {
    link(
      el.location(),
      numbering(el.numbering, ..counter(math.equation).at(el.location())),
    )
  } else { it }
}

// ---------- equations: number only labeled ones ----------
#set math.equation(numbering: "(1)", supplement: none)
#show math.equation.where(block: true): it => {
  if it.numbering != none and not it.has("label") {
    counter(math.equation).update(n => calc.max(0, n - 1))
    math.equation(it.body, block: true, numbering: none)
  } else { it }
}

// ---------- theorem environments (referencable figures) ----------
// One shared counter per level-1 section; `@label` renders e.g. "Theorem 3.1".
#show heading.where(level: 1): it => { counter(figure.where(kind: "thm")).update(0); it }

// Appendix sections are lettered; `in-app` switches theorem numbers to "A.1".
#let in-app = state("in-app", false)
#let thmenv(head, body, name: none, italicize: true) = figure(
  kind: "thm",
  supplement: head,
  outlined: false,
  numbering: n => numbering(if in-app.get() { "A.1" } else { "1.1" }, counter(heading).get().first(), n),
  caption: name,
  if italicize { emph(body) } else { body },
)
#show figure.where(kind: "thm"): it => block(
  width: 100%, above: 1.1em, below: 1.1em, breakable: true,
  align(left, {
    strong[#it.supplement #it.counter.display(it.numbering)]
    if it.caption != none [ (#it.caption.body)]
    strong[.]
    h(0.4em)
    it.body
  }),
)
#let theorem(body, name: none) = thmenv("Theorem", body, name: name)
#let lemma(body, name: none) = thmenv("Lemma", body, name: name)
#let proposition(body, name: none) = thmenv("Proposition", body, name: name)
#let corollary(body, name: none) = thmenv("Corollary", body, name: name)
#let conjecture(body, name: none) = thmenv("Conjecture", body, name: name)
#let definition(body, name: none) = thmenv("Definition", body, name: name, italicize: false)
#let remark(body, name: none) = thmenv("Remark", body, name: name, italicize: false)
#let fact(body, name: none) = thmenv("Fact", body, name: name)

#let proof(body, of: none) = block(above: 0.9em, below: 1.1em, {
  if of == none { emph[Proof.] } else { emph[Proof of #of.] }
  h(0.4em)
  body
  h(1fr)
  box($square$)
})

// Status tags: every numbered result carries one.
#let proved = text(fill: rgb("#1a5e1a"), size: 9pt, weight: "bold")[\[Proved\]]
#let provedlean = text(fill: rgb("#1a5e1a"), size: 9pt, weight: "bold")[\[Proved; Lean-checked\]]
#let known = text(fill: rgb("#3a3a3a"), size: 9pt, weight: "bold")[\[Known\]]
#let st(body) = block(above: 0.45em, below: 0.9em, { set par(justify: false, first-line-indent: 0em); text(size: 9.5pt, body) })
#let openst = text(fill: rgb("#8a1c1c"), size: 9pt, weight: "bold")[\[Open\]]

// Clearly marked placeholders (only two are allowed in this draft).
#let todo(body) = block(
  width: 100%,
  inset: 8pt,
  stroke: (paint: rgb("#b00020"), thickness: 1pt, dash: "dashed"),
  fill: rgb("#fff4f4"),
  [#text(fill: rgb("#b00020"), weight: "bold")[TODO.] #body],
)

// ---------- math shorthands ----------
#let Out = $"Out"$
#let AGM = $"AGM"$
#let Blk = $"Blk"$
#let opn(A) = $norm(#A)_2$
#let cF = $cal(F)$
#let cG = $cal(G)$
#let cH = $cal(H)$
#let cU = $cal(U)$
#let cL = $cal(L)$

// ---------- tables ----------
#set table(stroke: none, inset: (x: 6pt, y: 3.5pt))
#show figure: set block(breakable: true)
#show figure.where(kind: table): set figure.caption(position: top)
#show figure.where(kind: table): set text(size: 9pt)
#show figure.where(kind: table): set par(justify: false)
#show figure.caption: set text(size: 10pt)

// ---------- bibliography helper ----------
#let bib(n, body) = grid(
  columns: (5.4em, 1fr),
  column-gutter: 0.4em,
  align(top)[[#n]], body,
)
#let cite(lbl, key) = link(lbl)[#key]

// =====================================================================
// Title block
// =====================================================================
#align(center)[
  #block(width: 94%)[
    #text(size: 16pt, weight: "bold")[
      Levels of adaptivity and spectral worst-case bounds \
      for labeled triangle joins
    ]
  ]
  #v(1.1em)
  #text(size: 12pt)[A. Richard Caputo III#footnote[
    TJC L.P., New York.
    Email: #link("mailto:rcaputo3@tjclp.com")[`rcaputo3@tjclp.com`].
  ]]
  #v(0.5em)
  #text(size: 11pt)[October 9, 2026]
]
#v(1.2em)

// =====================================================================
// Abstract
// =====================================================================
#pad(x: 2.6em)[
  #set text(size: 10pt)
  #set par(first-line-indent: 0em)
  *Abstract.*
  We ask how much adaptivity a variable-at-a-time join needs to be
  worst-case optimal for the labeled triangle
  $Q(x,y,z) = R(x,y) and S(y,z) and T(z,x)$, and for which statistics.
  We compare a fixed attribute order, the best of the six orders per
  instance, a fixed root with a per-binding choice of the next variable,
  and a root chosen per instance with the next variable chosen per
  binding. For the cost $C$ of the best such choice, with every
  intersection charged at its shorter run, and the cyclic $ell_2$ bound
  $B_2$ we prove $C <= N + (N\/3)^(3\/8) B_2^(3\/4)$ and
  $C <= N + 3^(1\/8) N^(-1\/8) B_2^(5\/4)$, and explicit families attain
  their minimum up to a constant factor at every slope
  $B_2 asymp N^kappa$, $kappa in [9\/10, 3\/2]$. So this unpartitioned
  class cannot attain $O(N + B_2)$, even up to polylogarithmic
  factors (exponent $9\/8$ at $B_2 asymp N$), while known
  degree-partitioned algorithms can; the first known violation has
  $N approx 2 dot 10^7$. When every tuple lies in a triangle the gap
  exponent lies in $[1\/10, 1\/8]$. Against $N + B_2$ one fixed order
  loses exactly $Theta(N^(1\/4))$ on general inputs and the best of the
  six orders $Theta(N^(1\/5))$. The lower bounds also hold for a single
  directed predicate and for fresh comparison-based sorted
  intersections under adversarial identifiers, where the worst case at
  $B_2 asymp N$ is $Theta(N^(9\/8) (log N)^(1\/4))$. Under relation
  sizes and operator norms the worst-case triangle output lies in
  $(U\/4, U]$ for an explicit nine-term $U$, with a sharp factor $4$
  (checked in Lean 4), and the best driver of the kernel does
  work at most $U$; for the labeled 4-cycle an explicit 38-term $U_4$
  gives $(U_4\/16, U_4]$. Engine measurements on knowledge-graph
  triangle queries are reported with their limits.
]
#v(0.6em)

// =====================================================================
// Introduction
// =====================================================================
= Introduction <sec-intro>
// =====================================================================

RDF engines answer basic graph patterns over a single ternary relation
of triples, stored as several sorted permutations (for example PSO and
POS). A pattern with a constant predicate $p$ is then a binary relation
$p subset.eq V times V$ that can be read in either direction, and the
out- and in-degree of any term is a constant-time read of a
compressed-sparse-row (CSR) offset array. The simplest cyclic pattern,
the triangle
```
?x p1 ?y .  ?y p2 ?z .  ?z p3 ?x
```
is the canonical case where left-deep binary plans can be polynomially
worse than worst-case optimal joins (WCOJ)
[#cite(<ref-agm>)[AGM13], #cite(<ref-nprr>)[NPRR18],
#cite(<ref-lftj>)[Vel14]]. Leatherback, the RDF engine this work comes
from (to be open-sourced), answers triangles with a variable-at-a-time kernel that, for each tuple
$(x,y)$ of a driver relation, intersects two sorted neighbour runs from
the smaller side (@sec-engine).

*Levels of adaptivity.* Such a kernel can adapt at several levels, and
this paper asks how much adaptivity worst-case optimality needs, and
for which statistics. A _fixed global attribute order_ (GAO) fixes the
variable order once. Choosing the _best of the six orders_ per instance
amounts, for the triangle, to choosing which relation drives the
kernel, its _rotation_. A _fixed root_ fixes the first variable and
chooses the second variable separately for each binding of it;
_per-binding choice_ also chooses the root per instance. Finally,
_partitioned_ algorithms split a variable's domain, for example into
degree buckets, and plan each part separately
[#cite(<ref-jrr>)[JRR21], #cite(<ref-anos>)[ANOS24],
#cite(<ref-pandaexpress>)[ANS25]]. @tab-gaps places these levels
against two comparators: the cost $C + N$ of the best per-binding
choice, and the cyclic $ell_2$ bound $B_2$ of
[#cite(<ref-anos>)[ANOS24], #cite(<ref-jrr>)[JRR21]] (plus $N$). The
headline is the last two rows: per-binding choice costs at most
$N + (N\/3)^(3\/8) B_2^(3\/4)$ and no better, so for this unpartitioned
shorter-side kernel the worst-case exponent at $B_2 asymp N$ is $9\/8$,
not $1$; every coarser level loses $Theta(N^(1\/2))$ against $C + N$.
The lower bounds against $N + B_2$ also hold when intersections are
fresh comparison-based calls on sorted runs and the adversary assigns
the identifiers (@sec-sorted).

#figure(
  caption: [The levels of adaptivity and their worst-case gaps $delta$
    (cost at most $N^(delta + o(1))$ times the comparator, and attained).
    "Reduced" means pairwise semijoin-reduced; "fully reduced" means
    that every tuple lies in a triangle. Upper bounds $1\/2$ come from
    @lem-sum. Every lower bound against $N + B_2$ also holds for fresh
    comparison-based sorted-intersection calls under adversarial
    identifiers (@sec-sorted), where per-binding choice gains exactly a
    factor $(log N)^(1\/4)$ at $B_2 asymp N$; against $C + N$ the
    losses of $cF_a$ and $cG_a$ are established there only up to a
    factor $log N$ (@rem-sorted-cheap). For the spectral statistics
    $(r, sigma)$ of @sec-main, the best of six GAOs and per-binding
    choice have gap $0$ against $N + U$ (@cor-kernel, @lem-sum), and one
    fixed GAO has gap at least $1\/4$ (@prop-norot).],
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),
    table.hline(stroke: 0.8pt),
    table.header([*Level*], [*Against $C + N$*], [*Against $N + B_2$*]),
    table.hline(stroke: 0.4pt),
    [One fixed GAO], [$1\/2$ ($cF_a$, reduced)], [exactly $1\/4$ (@thm-onegao, $"GMR"$); reduced: $[1\/5, 1\/4]$],
    [Best of six GAOs (rotation per instance)], [$1\/2$ ($cG_a$, reduced)], [exactly $1\/5$, also reduced (@thm-best6)],
    [Fixed root, per-binding option], [$1\/2$ ($cH_a$, padded: reduced)], [$[1\/8, 1\/4]$ ($G_8$; @cor-fixedroot)],
    [Per-binding (root and option)], [$0$], [exactly $1\/8$ (@thm-pb-upper, @thm-pb-lower); $0$ for $B_2 <= N^(9\/10)$; fully reduced: $[1\/10, 1\/8]$ (@thm-fullred)],
    [Partitioned [#cite(<ref-jrr>)[JRR21]]], [---], [$0$ (outside our cost model)],
    table.hline(stroke: 0.8pt),
  ),
) <tab-gaps>

*Why sizes and operator norms.* Besides the $ell_2$ statistics we
study one statistic beyond sizes: the operator norm
$sigma = opn(A)$ of each relation's 0/1 incidence matrix $A$. The class
$(r, sigma)$ of sizes and norms is worth a section for four reasons.
It is _cheap_: one number per predicate, computed at compaction time.
It is _certifiable_: a few Collatz--Wielandt steps give a guaranteed
upper bound on $sigma$, and the resulting bound is at most $2%$ above
$U$ on $90%$ of our queries (@sec-engine-summary). It gives a
_guarantee, not an estimate_, and on real queries rarely the tightest
one (@sec-engine-summary): the
nine-term $U$ bounds the output of every admissible instance with
constant $1$ and is attained up to a factor $4$. And,
among the classes studied here, it is the one in which _per-instance
rotation is provably the right lever_: under sizes alone every rotation
is already worst-case optimal (each does work at most AGM
[#cite(<ref-skew>)[NRR13]]); under $ell_2$ statistics no unpartitioned
level is (@cor-l2-false); under $(r, sigma)$ the best rotation does
work at most $U < 4W$ (@cor-kernel), while a fixed rotation loses a
polynomial factor (@prop-norot). The statistic sits between degrees and
sizes: every degree is at most $sigma^2$ (@lem-deg), and $sigma^2$ is
at most the size, because $opn(A)^2 <= norm(A)_F^2$ (@sec-prelim).

#heading(level: 2, numbering: none)[Contributions]

+ *Per-binding choice and the cyclic $ell_2$ bound (@sec-adapt).* For
  the per-binding cost $C$ (root variable chosen per instance, second
  variable chosen per binding, every intersection charged at its shorter
  run),
  $C <= N + (|R| |S| |T|)^(1\/8) min(Lambda, Lambda')^(1\/2) <= N + (N\/3)^(3\/8) B_2^(3\/4)$
  with constant $1$ (@thm-pb-upper), and
  $C <= N + 3^(1\/8) N^(-1\/8) B_2^(5\/4)$ (@thm-pb-upper2). An explicit
  family with $C\/(N + B_2) >= (N\/9)^(1\/8)\/14$ refutes
  $C = O(N + B_2)$ and its polylogarithmic relaxation (@thm-pb-lower,
  @cor-l2-false), also on inputs that are both semijoin-reduced and
  connected (@rem-pb-reduce). The minimum of the two bounds is the exact
  worst case, up to a constant factor, at every real slope
  $B_2 = N^kappa$, $kappa in [9\/10, 3\/2]$ (@thm-pb-slopes,
  @cor-real-slopes, @thm-pb-asym), and $C = O(N)$ below $9\/10$. When
  every tuple lies in a triangle the gap lies in $[1\/10, 1\/8]$, and the
  fully reduced worst case equals the general one at every slope in
  $[11\/10, 3\/2]$ (@thm-fullred). The refutation is asymptotic: the
  first violation we know needs $N approx 2 dot 10^7$, and on the
  refuting family at the sizes we evaluated exactly
  ($N <= 4.6 dot 10^5$), $C\/(N + B_2)$ is between $0.25$ and $0.42$
  (@tab-g8-values). Per-binding choice itself is prior art
  [#cite(<ref-skew>)[NRR13], #cite(<ref-simjoin>)[ABGHNR24],
  #cite(<ref-cidx>)[ABFGN25]]; the contribution is the bound for this
  cost model. #proved
+ *Exact gaps of the coarser levels (@sec-sep).* Against $N + B_2$, one
  fixed order has gap exactly $1\/4$ on general inputs (between $1\/5$
  and $1\/4$ on semijoin-reduced inputs), the best of the six exactly
  $1\/5$, also on a semijoin-reduced family with $C = Theta(N)$, and a
  fixed root between $1\/8$ and $1\/4$, against $1\/8$ for per-binding
  choice (@thm-onegao, @thm-best6, @cor-fixedroot, @tab-gaps). Against
  $C + N$, one fixed GAO, the best of the six and a fixed root can each
  lose $Theta(N^(1\/2))$ on pairwise semijoin-reduced inputs
  (@thm-sep). A deterministic price-then-run scheduler selects a root of
  cost exactly $C$ in $C + min(6C, 2N) + 4n + O(1)$ per-edge units
  without output buffering (@prop-ptr). #proved
+ *Fresh sorted-intersection calls and a single predicate
  (@sec-sorted, @prop-selfjoin).* When intersections are sorted runs
  charged by key comparisons, every call is fresh (it knows only its two
  runs) and the adversary assigns the identifiers, every lower bound
  against $N + B_2$ survives without logarithmic loss (@thm-sorted-g8,
  @thm-sorted-sep); against $C + N$ some ratios are established only up
  to a factor $log N$ (@rem-sorted-cheap). The upper bound survives up
  to a factor $(log N)^(1\/4)$ (@thm-sorted-upper), and that factor is
  necessary, also for randomized routines (@thm-quarterlog), so the
  worst case at $B_2 asymp N$ is $Theta(N^(9\/8) (log N)^(1\/4))$. The
  certificate and doubling-search ingredients are classical
  [#cite(<ref-dlm>)[DLM00], #cite(<ref-bk>)[BK02],
  #cite(<ref-by>)[BY76]]; what is new is their simultaneous realization
  inside these join constructions and the resulting tradeoff. The $9\/8$
  lower bound and the order separations also hold for one directed
  predicate, while a symmetric predicate has $C <= |P| + B_2$
  (@prop-selfjoin). #proved
+ *Spectral worst-case output bounds (@sec-main).* For regular
  statistics $(r_i, sigma_i)$ the worst-case triangle output $W$
  satisfies $U\/4 < W <= U$, with $U$ the minimum of nine monomials. The
  upper bound is textbook (Schatten--Hölder and @lem-deg). The content
  is that the nine terms are exactly the feasibility conditions of one
  block family, so one family witnesses the lower bound in every
  regime, and that $inf W\/U = 1\/4$ (@thm-sharp; this family, in
  rational form, was found by a model-based review, @sec-ai). #provedlean Two measured norms
  give the same factor-$4$ characterization with six terms
  (@cor-twonorm), and none of the nine terms can be dropped
  (@prop-irred). For the labeled 4-cycle we prove
  $U_4\/16 < W_4 <= U_4$ for an explicit minimum $U_4$ of 38 monomials,
  each needed, with the best constant in $[8, 16]$ (@thm-cycle4,
  @prop-cycle4-sharp); the new ingredient is a lifted Gram bound
  (@lem-lambda), and the witnesses are matchings along arcs of the
  cycle rather than complete blocks. #proved
+ *Per-instance rotation is optimal for $(r, sigma)$ (@sec-kernel).*
  The probe work $M_pi$ of the kernel driven by rotation $pi$ equals the
  output of an instance with the same driver relation, the same relevant
  one-sided degree vectors and the same sizes (@lem-nest), and
  $min_pi M_pi <= U$, which is $< 4W$ for regular statistics
  (@cor-kernel). #provedlean No fixed rotation, and not their sum, is
  $O(sum_i r_i + W)$ (@prop-norot). #proved
+ *Engine and experiments (@sec-engine-summary; details in
  @sec-exp and @sec-engine).* On 3,124 selected canonical triangle queries
  with nonzero output, $U$ is below AGM by a median factor $9.6$ but
  tighter than all of AGM, the cyclic $ell_2$ bound and the degree bound
  on only $6.5%$ of them. On 1,241 knowledge-graph triangles run under
  six driver policies, $min_pi M_pi <= U$ holds on every query; the
  exact planner objective picks a different driver than its $64$-row
  estimate on only 3--6% of queries and is slower end to end, although
  no fixed sampling grid has a worst-case guarantee (@prop-sampler).
  The triangle operator is faster on skewed triangle queries ($32 times$
  for rows and $114 times$ for `COUNT(*)` on a Zipf store; a median
  $8.8$--$10.2 times$ where the first admission stage admits it on the
  knowledge graphs) and neutral on a uniform store. A calibrated second
  admission stage cuts total time by 21--49% against the first stage
  measured in the same run; the rule was fitted to these queries
  (in-sample), and both stages together still decline 29--49% of them.
  At the time of writing the operator and both stages are on a
  development branch of Leatherback.

The results of @sec-main and @sec-kernel marked Lean-checked are
kernel-checked in Lean 4 (@sec-mech); everything else is proved on
paper, and every construction found during the work was also rebuilt
in exact arithmetic by at least two separately run model-based checks
(@app-verify). AI tools were used throughout; @sec-ai states how.
@sec-background recalls two classical

spectral facts used for certification; they are not contributions.

#heading(level: 2, numbering: none)[What is and is not new]

All proofs here are elementary: Cauchy--Schwarz, the Schatten--Hölder
inequality, the Schur test, Hölder's inequality, and counting. Several
ingredients are known and we do not claim them: for one symmetric
relation the Hölder term of $U$ is the folklore spectral triangle bound
$6t = tr(A^3) <= lambda_1 tr(A^2) = 2 m lambda_1$; the degree terms are
the $ell_1$/$ell_infinity$ bounds of [#cite(<ref-anos>)[ANOS24]] with
maximum degrees bounded by $sigma^2$; the smaller-side kernel is the
Generic Join intersection of [#cite(<ref-skew>)[NRR13]]; choosing
the next variable separately for each binding is already done in
[#cite(<ref-skew>)[NRR13], #cite(<ref-simjoin>)[ABGHNR24],
#cite(<ref-cidx>)[ABFGN25]]; and comparison certificates, alternation
and doubling search for sorted-set intersection are classical
[#cite(<ref-dlm>)[DLM00], #cite(<ref-bk>)[BK02], #cite(<ref-bk08>)[BK08],
#cite(<ref-by>)[BY76]]. What is new, to our knowledge, are the
_bounds_: for the per-binding cost model of @sec-adapt (one root per
instance, an option per binding chosen by exact cost, smaller-side
intersections, no partitioning), the upper bounds of @thm-pb-upper and
@thm-pb-upper2 with matching lower bounds at every slope in
$[9\/10, 3\/2]$, the fully reduced interval, the exact gaps of the
orders, and their survival under fresh sorted intersections with
adversarial identifiers; and, for sizes and operator norms, the
nine-term characterization $U\/4 < W <= U$ for three labeled relations
with an asymptotically sharp factor $4$ (@thm-sharp), its 38-term
analogue for the 4-cycle, and the worst-case optimality of choosing the
kernel's driver per instance for these statistics. Partitioned
algorithms meet $B_2$ [#cite(<ref-jrr>)[JRR21],
#cite(<ref-pandaexpress>)[ANS25]]; our lower bounds are for the
unpartitioned class only. @sec-related compares each claim with the
closest prior work.

// =====================================================================
= Preliminaries <sec-prelim>
// =====================================================================

*Instances.* Fix finite sets $X, Y, Z$ and relations
$R subset.eq X times Y$, $S subset.eq Y times Z$,
$T subset.eq Z times X$ (sets, not bags). Their incidence matrices are
$A_R in {0,1}^(X times Y)$, $A_S in {0,1}^(Y times Z)$,
$A_T in {0,1}^(Z times X)$, and
$
  Out = tr(A_R A_S A_T) = |{(x,y,z) : (x,y) in R, (y,z) in S, (z,x) in T}|.
$
Every RDF triangle pattern with three distinct variables and constant
predicates is of this form after transposing some predicates, because
each predicate slice is readable in both directions. We use the cyclic
order $R -> S -> T -> R$ of the labels throughout.

*Degrees.* For a set $P$ of pairs, $d^+_P (u)$ is the number of pairs
leaving $u$ and $d^-_P (v)$ the number entering $v$; $Delta^+_P$ and
$Delta^-_P$ are their maxima. We write $N = |R| + |S| + |T|$ and
$opn(A)$ for the largest singular value.

*Statistics.* Given reals $r_i, sigma_i$ for $i in {R,S,T}$, an instance
is _admissible_ if $|i| <= r_i$ and $opn(A_i) <= sigma_i$ for every $i$,
and $W(r, sigma) = sup{Out : "admissible instances"}$, with the
convention $sup emptyset = 0$. Some instance is admissible iff all six
statistics are nonnegative (the empty instance is then admissible;
Lean: `admissible_exists_iff_nonneg`); if a statistic is negative the
class is empty and $W = 0$ only by that convention. A nonzero 0/1
matrix has $opn(A) >= opn(A e_y) >= 1$, so if some $r_i < 1$ or
$sigma_i < 1$ that relation is empty and every admissible instance has
$Out = 0$ (Lean: `theoremB_degenerate`, which assumes no sign condition
and is vacuous when a bound is negative); for nonnegative statistics
the value $W = 0$ is attained by an admissible instance
(`theoremB_degenerate_attained`). We call $(r, sigma)$ _regular_ when
all $r_i, sigma_i >= 1$.

*Clipping.* Put $s_i = min(sigma_i^2, r_i)$. Nothing is lost, because
$opn(A_i)^2 <= norm(A_i)_F^2 = |i| <= r_i$ (Lean:
`opNorm_adj_sq_le_card`).

*The nine terms.* For $\{i,j,k\} = \{R,S,T\}$ and $i != j$ let
$
  H_i = sqrt(s_i r_j r_k) quad ("Hölder"), quad
  D_(i,j) = r_i s_j quad ("degree"), quad
  U = min{H_R, H_S, H_T, D_(R,S), D_(R,T), D_(S,R), D_(S,T), D_(T,R), D_(T,S)}.
$
AGM and the trivial bounds $r_j r_k$ are redundant: $sqrt(r_R r_S r_T) >= H_i$
and $r_j r_k >= D_(j,k)$ because $s_i <= r_i$. In particular $U <= AGM$
always. With unclipped $sigma^2$, $U$ is the minimum of thirteen
monomials. The problem and $U$ are invariant under $S_3$ acting on the
labels (rotation by cyclicity of the trace; reflection by
$tr(A_R A_S A_T) = tr(A_T^top A_S^top A_R^top)$).

*Kernel work.* The adaptive kernel driven by rotation $R$ scans $R$ and,
for each $(x,y) in R$, intersects $S(y, dot)$ with $T(dot, x)$ from the
smaller side. Its probe work is
$
  M_R = sum_((x,y) in R) min(d^+_S (y), d^-_T (x)),
$
and $M_S$, $M_T$ are its rotations:
$M_S = sum_((y,z) in S) min(d^+_T (z), d^-_R (y))$,
$M_T = sum_((z,x) in T) min(d^+_R (x), d^-_S (z))$. We write $pi$ for
a rotation, i.e. the relation that drives the kernel. Clearly
$Out <= M_pi$ for each $pi$.

*Cost model.* We charge one unit for reading a CSR offset (a degree),
one for reading one neighbour, and one for one membership test. With
hash or bitmap membership the intersection of two runs of lengths
$p <= q$ costs at most $2p$ (read each element of the shorter run and
test it). This _min-side charge_ is the cost model of @sec-adapt,
@sec-main and @sec-kernel. Sorted runs intersected by comparisons are a different
model: with contiguous identifiers leapfrog finishes after a few seeks
(on $G_8$ of @sec-conj the two runs are disjoint), so lower bounds there
must let the adversary assign the identifiers. @sec-sorted defines that
model and shows that every lower bound of @sec-adapt against $N + B_2$
survives in it without logarithmic loss (against $C + N$ some survive
only up to a factor $log N$, @rem-sorted-cheap), while its worst case at $B_2 asymp N$ gains
exactly a factor $(log N)^(1\/4)$.

*Comparators.* AGM is $sqrt(r_R r_S r_T)$. The _degree bound_ is
$
  min{ r_R min(Delta^+_S, Delta^-_T), thick
       r_S min(Delta^+_T, Delta^-_R), thick
       r_T min(Delta^+_R, Delta^-_S) },
$
the form $|R| dot norm(deg_S (Z|Y))_infinity$ of
[#cite(<ref-anos>)[ANOS24], Eq. (3)] applied to each relation. The
_cyclic $ell_2$ bound_ is
$
  B_2 = min{ (sum_x d^+_R (x)^2 sum_y d^+_S (y)^2 sum_z d^+_T (z)^2)^(1\/3),
             (sum_y d^-_R (y)^2 sum_z d^-_S (z)^2 sum_x d^-_T (x)^2)^(1\/3) },
$
an upper bound on $Out$ from [#cite(<ref-anos>)[ANOS24], Eq. (4)] and
[#cite(<ref-jrr>)[JRR21]]. In @sec-adapt, $B_2$ is the comparator for
the per-binding cost: @thm-pb-upper bounds $C$ in terms of the
squared-degree sums behind $B_2$, and @thm-pb-lower shows that $C$ can
exceed $B_2$ by a polynomial factor. No result of @sec-main or @sec-kernel
depends on $B_2$.

*Notation.* @tab-notation collects the symbols used in more than one
section.

#figure(
  caption: [Notation.],
  table(
    columns: (auto, 1fr),
    align: (left, left),
    table.hline(stroke: 0.8pt),
    table.header([*Symbol*], [*Meaning*]),
    table.hline(stroke: 0.4pt),
    [$A_R, A_S, A_T$], [0/1 incidence matrices of $R, S, T$],
    [$r_i$, $sigma_i$, $s_i$], [size bound, norm bound, clipped statistic $min(sigma_i^2, r_i)$],
    [$H_i$, $D_(i,j)$, $U$], [Hölder terms, degree terms, their minimum (@sec-prelim)],
    [$W$], [worst-case output over admissible instances ($w(x)$ in @lem-perroot is unrelated)],
    [$Blk(a,b,c,m)$], [block instance: $m$ disjoint complete block triangles (@sec-lower)],
    [$hat(a), hat(b), hat(c)$], [real block shape; $a, b, c$ are their floors (@lem-feasible)],
    [$pi$, $M_pi$], [rotation (driving relation) and the kernel's probe work],
    [$c_P (u)$, $c^*(u)$], [cost of option $P$ at binding $u$; $c^*(u)$ the smaller option cost (@sec-adapt)],
    [$C_x, C_y, C_z$, $C$], [per-binding cost for a fixed root; $C = min(C_x, C_y, C_z)$],
    [$n_v$, $n$], [number of bindings of root variable $v$ with an incident tuple; $n = n_x + n_y + n_z$],
    [$B_2$], [cyclic $ell_2$ bound],
    [$alpha, beta, gamma$; $alpha', beta', gamma'$], [forward and reverse squared-degree sums (@sec-adapt)],
    [$Lambda, Lambda'$], [$(alpha beta gamma)^(1\/2)$, $(alpha' beta' gamma')^(1\/2)$; $B_2 = min(Lambda, Lambda')^(2\/3)$],
    [$G_8 (m)$, $cU(m)$], [lower-bound gadget and its three-rotation union (@thm-pb-lower)],
    [$F_(i,j) (u)$, $kappa$], [slope family; slope $kappa$ with $B_2 = Theta(N^kappa)$ (@thm-pb-slopes); every real $kappa in [1, 3\/2]$ (@cor-real-slopes)],
    [$U_2$, $U'_1$], [two- and one-norm specializations of $U$ (@cor-twonorm)],
    [$D(L,a,h)$, $E(L,a,h)$], [gadgets of @thm-pb-asym, @thm-onegao],
    [$L(p,q,t,g,k,w)$, $cL(v)$], [live gadget and its three-rotation union (@lem-live, @thm-fullred)],
    [$U_4$, $W_4$, $K$], [4-cycle bound, its worst case, the lifted Gram matrix (@sec-cycle4)],
    [$Q_A$, $h(p,q)$, $L_N$, $hat(C)$], [sorted-model cost, galloping price, $1 + ceil(log_2 N)$, priced per-binding cost (@sec-sorted)],
    [$cF_a, cG_a, cH_a$, $"GMR"$, $"GMIN"$], [separation families (@thm-sep)],
    [padding], [attaching one fresh triangle per half-dangling vertex (@lem-pad)],
    [$L_v$], [running lower bound on $C_v$ in the price-then-run scheduler (@sec-ptr)],
    [$N$], [$|R| + |S| + |T|$],
    table.hline(stroke: 0.8pt),
  ),
) <tab-notation>

// =====================================================================
= Per-binding choice: a tight $ell_2$ bound and the exact gaps of coarser levels <sec-adapt>
// =====================================================================

For sizes and operator norms, choosing the kernel's driver per instance
is already worst-case optimal (@cor-kernel). Degree-sequence statistics
ask for finer adaptivity, and this section studies a per-binding
variant of the kernel. Its cost $C$ obeys a worst-case bound in terms
of the degree-sequence norms behind $B_2$, and a second bound that is
sharper below slope $1$ (@thm-pb-upper, @thm-pb-upper2). Their minimum
is tight at $B_2 asymp N$ (@thm-pb-lower) and, up to a constant factor,
at every real slope $B_2 = N^kappa$, $kappa in [9\/10, 3\/2]$
(@thm-pb-slopes, @cor-real-slopes, @thm-pb-asym). In particular
$C = O(N + B_2)$ is false, so this unpartitioned class, which fixes one
root per instance and intersects at the shorter run, is not optimal for
the cyclic $ell_2$ bound; whether every partition-free algorithm fails
is open (@sec-open). We then separate the per-binding strategy from
fixed attribute orders and fixed roots, with exact gaps for the orders
(@thm-sep, @thm-best6, @thm-onegao, @cor-fixedroot), and show that
the lower bounds survive fresh sorted intersections under adversarial
identifiers (@sec-sorted). A deterministic scheduler that pays for the
statistics the choice needs (@prop-ptr) and a negative result for
classes defined by degree metadata (@prop-ferrers) are in @app-ptr.

== Per-binding cost

Fix a root variable, say $x$. A binding $x$ has two options. Option $R$
walks $y in R(x, dot)$ and intersects $S(y, dot)$ with $T(dot, x)$;
option $T$ walks $z in T(dot, x)$ and intersects $R(x, dot)$ with
$S(dot, z)$. Their costs are
$
  c_R (x) = sum_(y : (x,y) in R) (1 + min(d^+_S (y), d^-_T (x))), quad
  c_T (x) = sum_(z : (z,x) in T) (1 + min(d^+_R (x), d^-_S (z))),
$
$c^*(x) = min(c_R (x), c_T (x))$, and $C_x = sum_x c^*(x)$. Roots $y$
(options $R$ and $S$) and $z$ (options $S$ and $T$) are defined
symmetrically, with per-edge costs $1 + min(d^+_S (y), d^-_T (x))$ on
$R$-tuples, $1 + min(d^-_R (y), d^+_T (z))$ on $S$-tuples and
$1 + min(d^+_R (x), d^-_S (z))$ on $T$-tuples. The per-binding cost is
$C = min(C_x, C_y, C_z)$. A _fixed global attribute order_ (GAO) fixes
the root and, for every binding, the option; the option's relation is
the GAO's _second relation_. A _fixed root_ fixes the root variable and
chooses the option per binding. We measure $C$ in _per-edge cost
units_; by the cost model of @sec-prelim, executing an edge of cost
$1 + k$ (one neighbour read, one degree read to find the smaller side,
and an intersection of cost at most $2k$) takes at most $2(1 + k)$ unit
operations.

#lemma(name: "sum identities")[
  $sum_x c_R (x) = |R| + M_R$, and likewise for the other five
  (root, option) pairs. A GAO whose second relation is $pi$ costs
  $|pi| + M_pi$, so the six GAOs have only three costs. Moreover
  $Out <= C <= min_pi (|pi| + M_pi) <= N + min(M_R, M_S, M_T)$, and
  $C <= N + sqrt(|R| |S| |T|)$.
] <lem-sum>
#st[#proved]

#proof[
  Each $R$-tuple $(x,y)$ appears once in $sum_x c_R (x)$ with cost
  $1 + min(d^+_S (y), d^-_T (x))$; this also holds in
  $sum_y c_R (y)$ for root $y$. For root $x$,
  $C_x <= min(sum_x c_R, sum_x c_T) = min(|R| + M_R, |T| + M_T)$; for
  root $y$, $C_y <= |S| + M_S$. Every triangle through binding $u$ is
  found by either option at $u$, at cost at least one per triangle, so
  $Out <= C_v$ for each root $v$. The last bound follows from
  $M_R <= opn(A_R) sqrt(|S| |T|) <= sqrt(|R| |S| |T|)$
  (@prop-kernel).
]

So per-binding choice is never asymptotically worse than the best
rotation, or than AGM.

*Degree-sequence norms.* Write
$
  alpha = sum_x d^+_R (x)^2, quad beta = sum_y d^+_S (y)^2, quad
  gamma = sum_z d^+_T (z)^2, quad
  alpha' = sum_y d^-_R (y)^2, quad beta' = sum_z d^-_S (z)^2, quad
  gamma' = sum_x d^-_T (x)^2,
$
and $Lambda = (alpha beta gamma)^(1\/2)$,
$Lambda' = (alpha' beta' gamma')^(1\/2)$, so that
$B_2 = min(Lambda, Lambda')^(2\/3)$ (@sec-prelim). The sizes, $N$,
$Out$, the probe works $M_pi$, the per-root costs $C_v$ and the six
squared-degree sums are sums over vertices or tuples of functions of
local degrees, so they add over vertex-disjoint unions. Their minima
and products do not in general: $C = min_v C_v$, $Lambda$, $Lambda'$
and $B_2$ are computed from the summed quantities, not summed
themselves. _Rotating_ an
instance means relabelling $(R, S, T)$ on $(X, Y, Z)$ as $(S, T, R)$ on
$(Y, Z, X)$; this preserves $Out$ and $N$ and permutes
$(M_R, M_S, M_T)$, $(C_x, C_y, C_z)$, $(|R|, |S|, |T|)$ and
$(alpha, beta, gamma)$ cyclically. _Reflecting_ it means replacing
$(R, S, T)$ on $(X, Y, Z)$ by $(T^top, S^top, R^top)$ on $(X, Z, Y)$;
this exchanges the two options of every root, so it preserves $C$, and
it exchanges $(alpha, beta, gamma)$ with $(gamma', beta', alpha')$, so
$Lambda <-> Lambda'$.

== An $ell_2$ upper bound for the per-binding cost <sec-pb-upper>

#lemma(name: "per-root bound")[
  For root $x$,
  $
    C_x <= |R| + |T| + |S|^(3\/8) alpha^(1\/4) beta^(1\/8) gamma^(3\/8)
    quad "and" quad
    C_x <= |R| + |T| + |S|^(3\/8) gamma'^(1\/4) beta'^(1\/8) alpha'^(3\/8).
  $
  By rotation,
  $C_y <= |R| + |S| + |T|^(3\/8) beta^(1\/4) gamma^(1\/8) alpha^(3\/8)$
  and
  $C_z <= |S| + |T| + |R|^(3\/8) gamma^(1\/4) alpha^(1\/8) beta^(3\/8)$,
  each with a reflected (primed) form.
] <lem-perroot>
#st[#proved]

#proof[
  Write $c_R (x) = d^+_R (x) + P(x)$ and $c_T (x) = d^-_T (x) + Q(x)$,
  where
  $P(x) = sum_(y in R(x, dot)) min(d^+_S (y), d^-_T (x))$ and
  $Q(x) = sum_(z : (z,x) in T) min(d^+_R (x), d^-_S (z))$. Since
  $min(u + P, v + Q) <= u + v + min(P, Q)$, summing over $x$ gives
  $C_x <= |R| + |T| + H_x$ with $H_x = sum_x min(P(x), Q(x))$. We bound
  $H_x$ in five steps; write $a = d^+_R (x)$.
  + _Cauchy--Schwarz over the $a$ distinct $y$:_
    $P(x) <= sum_(y in R(x, dot)) d^+_S (y) <= sqrt(a beta)$.
  + _$min(u, v) <= sqrt(u v)$:_ $Q(x) <= sqrt(a) dot w(x)$ with
    $w(x) = sum_(z : (z,x) in T) sqrt(d^-_S (z))$; the radical covers
    $a$ only.
  + _Split the minimum:_ $min(P, Q) <= P^(1\/4) Q^(3\/4)$ (a weighted
    geometric mean; it also holds if $P$ or $Q$ is $0$). Hence
    $min(P(x), Q(x)) <= beta^(1\/8) a^(1\/2) w(x)^(3\/4)$.
  + _Hölder with exponents $(4, 4\/3)$:_
    $sum_x d^+_R (x)^(1\/2) w(x)^(3\/4) <= alpha^(1\/4) (sum_x w(x))^(3\/4)$.
  + _Double counting, then Cauchy--Schwarz:_
    $sum_x w(x) = sum_z d^+_T (z) sqrt(d^-_S (z)) <= sqrt(gamma) sqrt(sum_z d^-_S (z)) = sqrt(gamma |S|)$.
  Together, $H_x <= alpha^(1\/4) beta^(1\/8) (gamma |S|)^(3\/8)$. The
  primed form exchanges the roles of $P$ and $Q$: use
  $min(P, Q) <= Q^(1\/4) P^(3\/4)$,
  $Q(x) <= sqrt(d^-_T (x) beta')$,
  $P(x) <= sqrt(d^-_T (x)) sum_(y in R(x, dot)) sqrt(d^+_S (y))$, Hölder
  against $gamma'$, and
  $sum_y d^-_R (y) sqrt(d^+_S (y)) <= sqrt(alpha' |S|)$. The bounds for
  roots $y$ and $z$ are the root-$x$ bounds of the rotated instance.
]

#theorem(name: [per-binding $ell_2$ bound])[
  For every instance,
  $
    C <= N + (|R| |S| |T|)^(1\/8) min(Lambda, Lambda')^(1\/2)
      <= N + (N\/3)^(3\/8) B_2^(3\/4);
  $
  equivalently, in integers,
  $(C - N)_+^8 <= |R| |S| |T| dot min(alpha beta gamma, alpha' beta' gamma')^2$.
  The constant is $1$ and there are no logarithmic factors.
] <thm-pb-upper>
#st[#proved (not formalized; exact checks in @app-verify)]

#proof[
  Let $K_x = |S|^(3\/8) alpha^(1\/4) beta^(1\/8) gamma^(3\/8)$,
  $K_y = |T|^(3\/8) beta^(1\/4) gamma^(1\/8) alpha^(3\/8)$ and
  $K_z = |R|^(3\/8) gamma^(1\/4) alpha^(1\/8) beta^(3\/8)$ be the
  multiplicative terms of the unprimed bounds of @lem-perroot; they are
  nonnegative. Since $C <= C_v$ for every root $v$ and $N$ is at least
  the sum of the two sizes walked at $v$, @lem-perroot gives
  $C - N <= K_v$ for each $v$. Hence
  $
    (C - N)_+ <= min(K_x, K_y, K_z) <= (K_x K_y K_z)^(1\/3),
  $
  the second step because the $K_v$ are nonnegative. In the product each
  of $alpha, beta, gamma$ has total exponent $1\/4 + 1\/8 + 3\/8 = 3\/4$
  and each cardinality exponent $3\/8$, so the cube root is
  $(|R| |S| |T|)^(1\/8) Lambda^(1\/2)$. The primed bounds give
  $Lambda'$ in the same way. Finally
  $min(Lambda, Lambda')^(1\/2) = B_2^(3\/4)$, AM--GM gives
  $|R| |S| |T| <= (N\/3)^3$, and the eighth power of the first bound is
  the integer form. The geometric mean must be taken of the bounds
  $K_v$, not of the differences $C_v$ minus the two walked sizes, which
  can have mixed signs: on $K_(2,3,3)$ plus ten isolated $R$-tuples,
  $(|R|, |S|, |T|) = (16, 9, 6)$ and $C_x = C_y = C_z = 24$, so the
  differences are $(2, -1, 9)$, whose geometric mean
  $-root(3, 18)$ lies below their minimum $-1$.
]

#theorem(name: [a second per-binding $ell_2$ bound])[
  For every instance with $N > 0$,
  $
    C <= N + 3^(1\/8) N^(-1\/8) B_2^(5\/4);
  $
  equivalently, in integers,
  $N^3 (C - N)_+^24 <= 27 min(alpha beta gamma, alpha' beta' gamma')^10$.
  Its main term is that of the second form of @thm-pb-upper times
  $sqrt(3 B_2 \/ N)$, so it is the sharper of the two exactly when
  $B_2 < N\/3$; at $B_2 = N^kappa$ its exponent $(10 kappa - 1)\/8$ is
  below $3\/8 + 3 kappa\/4$ by $(1 - kappa)\/2$ for $kappa < 1$, and
  both equal $9\/8$ at $kappa = 1$.
] <thm-pb-upper2>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  If $C <= N$ there is nothing to prove; let $C > N$. Reflection
  preserves $C$ and $N$ and exchanges the two moment products, so we may
  assume $alpha beta gamma = min(alpha beta gamma, alpha' beta' gamma') = B_2^3$.
  Rotation preserves $C$, $N$ and the forward product and permutes
  $(|R|, |S|, |T|)$ and $(alpha, beta, gamma)$ cyclically, so we may
  further assume that $R$ is a largest relation. Degrees are integers,
  so $d^2 >= d$ and $|R| <= alpha$, $|S| <= beta$, $|T| <= gamma$; in
  particular $alpha >= |R| >= N\/3$. With $H_v$ the sum of the minima in
  the proof of @lem-perroot (nonnegative), $C - N <= H_x$ and
  $C - N <= H_y$, and
  $
    H_x <= |S|^(3\/8) alpha^(1\/4) beta^(1\/8) gamma^(3\/8)
        <= alpha^(1\/4) beta^(1\/2) gamma^(3\/8), quad
    H_y <= |T|^(3\/8) beta^(1\/4) gamma^(1\/8) alpha^(3\/8)
        <= alpha^(3\/8) beta^(1\/4) gamma^(1\/2).
  $
  Hence
  $C - N <= min(H_x, H_y) <= H_x^(2\/3) H_y^(1\/3)
  <= alpha^(7\/24) beta^(5\/12) gamma^(5\/12)
  = (alpha beta gamma)^(5\/12) alpha^(-1\/8)
  <= B_2^(5\/4) (N\/3)^(-1\/8)$.
  The integer form is the 24th power. The comparison of main terms is
  $3^(1\/8) N^(-1\/8) B_2^(5\/4) \/ ((N\/3)^(3\/8) B_2^(3\/4))
  = (3 B_2 \/ N)^(1\/2)$.
]

#corollary(name: [consequences of @thm-pb-upper and @thm-pb-upper2])[
  + $C <= N + N^(1\/8) (N + B_2)$, and $C <= 2 max(N, B_2)^(9\/8)$.
  + $C < 2.15 N$ whenever $B_2 <= N^(9\/10)$, and
    $C <= 2(N + B_2)$ whenever $B_2 >= N^(3\/2)$.
  + $min(M_R, M_S, M_T) <= (Lambda Lambda')^(1\/3)$, so
    $C <= N + min((Lambda Lambda')^(1\/3), sqrt(|R| |S| |T|))$.
] <cor-pb>
#st[#proved]

#proof[
  (1) $(N\/3)^(3\/8) B_2^(3\/4) <= N^(1\/8) dot N^(1\/4) B_2^(3\/4)$ and
  $N^(1\/4) B_2^(3\/4) <= N\/4 + 3 B_2\/4$ by weighted AM--GM. The second
  form follows directly from @thm-pb-upper: with
  $M = max(N, B_2) >= 1$,
  $C <= N + 3^(-3\/8) M^(9\/8) <= (1 + 3^(-3\/8)) M^(9\/8) < 1.67 M^(9\/8)$.
  (2) If $B_2 <= N^(9\/10)$,
  @thm-pb-upper2 gives
  $C <= N + 3^(1\/8) N^(-1\/8) N^(9\/8) = (1 + 3^(1\/8)) N$, and
  $3^(1\/8) < 1.15$. If $B_2 >= N^(3\/2)$ then $N^(3\/8) <= B_2^(1\/4)$ in
  @thm-pb-upper. (3) $M_R <= sum_y d^-_R (y) d^+_S (y) <= sqrt(alpha' beta)$,
  $M_S <= sum_z d^-_S (z) d^+_T (z) <= sqrt(beta' gamma)$ and
  $M_T <= sum_x d^-_T (x) d^+_R (x) <= sqrt(gamma' alpha)$ by
  Cauchy--Schwarz; the product is $Lambda Lambda'$, and a minimum is at
  most the geometric mean. The last term is @lem-sum.
]

So per-binding choice meets $N + B_2$ up to a constant factor for every
slope $kappa <= 9\/10$, not only $kappa <= 5\/6$, and @thm-pb-upper is
not tight on $(5\/6, 1)$. The next subsection shows that the minimum of
the two bounds is the exact worst case for every real slope in
$[9\/10, 3\/2]$.

== Per-binding choice does not meet the $ell_2$ bound <sec-conj>

A natural conjecture is that per-binding choice is optimal for the
cyclic $ell_2$ class without partitioning: that for an absolute
constant $c$, or at least for $c = O(log^2 N)$, every instance
satisfies
$
  C^3 <= c dot (N^3 + min{
    sum_x d^+_R (x)^2 sum_y d^+_S (y)^2 sum_z d^+_T (z)^2, thick
    sum_y d^-_R (y)^2 sum_z d^-_S (z)^2 sum_x d^-_T (x)^2 }),
$
i.e. $C = O(N + B_2)$. We refute it. Small-instance search found no
violation, because the first violation needs $N approx 2 dot 10^7$.
The first member of the families
below with $C\/(N + B_2) > 1$ is the union of $F_(1,1) (7)$ and its two
rotations (@thm-pb-slopes; $F_(1,1)$ is $G_8$ without $Z_0$ and has the
better constant, $C\/(N + B_2) approx u\/7$), with $N approx 2.0 dot 10^7$
(ratio $0.93$ at $u = 6$, $1.07$ at $u = 7$). The family $cU(m)$ used in
@thm-pb-lower needs $m = 11$, $N approx 1.35 dot 10^9$ (ratio $0.97$ at
$m = 10$, $1.06$ at $m = 11$); in the cubic form displayed above it
exceeds $1$ from $m = 7$, $N approx 3.7 dot 10^7$.

*The gadget $G_8 (m)$.* For $m >= 2$ take parts $X$ of size $m^4$,
$Y_0$ of size $m^2$, $Y_2$ of size $m^8$, $Z_0$ of size $m^8$, $Z_1$ of
size $m^3$ and $Z_2$ of size $m^6$, and the blocks of
@tab-g8, each complete or biregular.

#figure(
  caption: [The gadget $G_8 (m)$. Degrees are listed as (left part, right part) of each block, in the orientation of the relation.],
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),
    table.hline(stroke: 0.8pt),
    table.header([*Block*], [*Shape*], [*Degrees*]),
    table.hline(stroke: 0.4pt),
    [$R = X times Y_0$], [complete], [$d^+_R = m^2$ on $X$, $d^-_R = m^4$ on $Y_0$],
    [$S supset.eq Y_0 times Z_1$], [complete], [$d^+_S = m^3$ on $Y_0$, $d^-_S = m^2$ on $Z_1$],
    [$S supset.eq Y_2 -> Z_2$], [biregular], [$d^+_S = 1$ on $Y_2$, $d^-_S = m^2$ on $Z_2$],
    [$T supset.eq Z_0 -> X$], [biregular], [$d^+_T = 1$ on $Z_0$, contributes $m^4$ to $d^-_T$ on $X$],
    [$T supset.eq Z_2 -> X$], [biregular], [$d^+_T = m$ on $Z_2$, contributes $m^3$ to $d^-_T$ on $X$],
    table.hline(stroke: 0.8pt),
  ),
) <tab-g8>

#theorem(name: [the per-binding $ell_2$ worst case, and refutation of $C = O(N + B_2)$])[
  Let $cU(m)$ be the disjoint union of $G_8 (m)$ and its two rotations.
  For every $m >= 2$, $Out(cU(m)) = 0$ and
  $
    C_x = C_y = C_z = m^9 + m^8 + m^6 + m^5, quad
    N = 3(2m^8 + m^7 + m^6 + m^5) <= 9 m^8, quad
    alpha = beta = gamma = 5 m^8.
  $
  Hence $B_2 <= 5 m^8$ and
  $
    C \/ (N + B_2) >= m\/14 >= (N\/9)^(1\/8) \/ 14, wide
    C^3 \/ (N^3 + min(alpha beta gamma, alpha' beta' gamma')) >= m^3 \/ 854.
  $
  So no constant $c$, and no $c = O(log^k N)$ for any fixed $k$,
  satisfies $C <= c (N + B_2)$ on all instances; the geometric-mean
  variant $(C_x C_y C_z)^(1\/3) = O(N + B_2)$ fails as well.
] <thm-pb-lower>
#st[#proved (exact values also recomputed for $m = 2, 3, 4$ by two
separately written evaluators; @tab-g8-values, @app-verify)]

#proof[
  _One gadget._ For $x in X$: $d^-_T (x) = m^4 + m^3$; option $R$ walks
  $m^2$ vertices of $Y_0$, each with $d^+_S = m^3$, so
  $c_R (x) = m^2 (1 + m^3)$; option $T$ walks $m^4$ vertices of $Z_0$
  (where $d^-_S = 0$) and $m^3$ of $Z_2$ (where $d^-_S = m^2 = d^+_R (x)$),
  so $c_T (x) = m^4 + m^3 (1 + m^2)$. Thus $c^*(x) = m^5 + m^2$ and
  $C_x (G_8) = m^9 + m^6$. For $y in Y_0$, option $S$ walks $Z_1$, where
  $d^+_T = 0$, at cost $m^3$, and option $R$ costs more; $Y_2$ has no
  $R$-tuples, so its option $R$ is empty. Hence $C_y (G_8) = m^5$. For
  $z$: $Z_0$ has no $S$-tuples and $Z_1$ no $T$-tuples (cost $0$); on
  $Z_2$, option $S$ walks $m^2$ vertices of $Y_2$ with $d^-_R = 0$
  (cost $m^2$) and option $T$ costs $m (1 + m^2)$. Hence
  $C_z (G_8) = m^8$. Sizes: $|R| = m^6$, $|S| = m^5 + m^8$,
  $|T| = m^8 + m^7$. Norms: $alpha = m^4 dot m^4 = m^8$,
  $beta = m^2 dot m^6 + m^8 = 2m^8$, $gamma = m^8 + m^6 dot m^2 = 2m^8$.
  No triangle exists: $R$ leads into $Y_0$, $S$ maps $Y_0$ into $Z_1$,
  and $T$ leaves no vertex of $Z_1$.

  _The union._ Costs and squared norms add over components, and
  rotation permutes $(C_x, C_y, C_z)$ and $(alpha, beta, gamma)$
  cyclically, so each $C_v (cU) = C_x + C_y + C_z$ of $G_8$, i.e.
  $m^9 + m^8 + m^6 + m^5$, and each forward norm is
  $m^8 + 2m^8 + 2m^8$. $N <= 9m^8$ because $m^7 + m^6 + m^5 <= m^8$ for
  $m >= 2$. Then $C\/(N + B_2) >= m^9 \/ (14 m^8)$, and
  $N^3 + alpha beta gamma <= (729 + 125) m^24$. A polylogarithm of
  $N <= 9 m^8$ is $o(m)$.
]

#figure(
  caption: [Exact values on $cU(m)$. The last column is $C$ divided by the right-hand side of @thm-pb-upper.],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: (right, right, right, right, right, right),
    table.hline(stroke: 0.8pt),
    table.header([$m$], [$N$], [$B_2$], [$C$], [$C\/(N + B_2)$], [$C\/$bound]),
    table.hline(stroke: 0.4pt),
    [2], [2,208], [1,280], [864], [0.248], [0.182],
    [3], [48,843], [32,805], [27,216], [0.333], [0.192],
    [4], [457,728], [327,680], [332,800], [0.424], [0.200],
    table.hline(stroke: 0.8pt),
  ),
) <tab-g8-values>

#corollary(name: [$C = O(N + B_2)$ fails])[
  There is no constant $c$, and no $c = O(log^k N)$, such that every
  instance satisfies
  $C^3 <= c (N^3 + min(alpha beta gamma, alpha' beta' gamma'))$. The
  partition-free per-binding strategy is not optimal for the cyclic
  $ell_2$ bound; at $B_2 asymp N$ its worst-case exponent is exactly
  $9\/8$ (@thm-pb-upper, @thm-pb-lower).
] <cor-l2-false>
#st[#proved]

Degree-bucket partitioning with multiplexing over acyclic subqueries
[#cite(<ref-jrr>)[JRR21], Thm. 4.4] computes the triangle in time
linear in the $ell_2$ bound of one orientation, given as input norm
bounds (their Theorem 4.4, with a query-dependent factor
$2^((p+1)|V|)$, $O(1)$-time B-tree access in the RAM model, and
$O(N log N)$ index construction); running it on the orientation with
the smaller product meets $B_2$ up to the same factors. Their algorithm
is outside our class: it partitions every relation into degree buckets
and chooses the plan per combination of buckets. So, within the per-binding cost model of @sec-adapt (one
root per instance, a per-binding option, min-side intersections), some
partitioning of a variable's domain is needed to reach the $ell_2$
bound; whether every partition-free algorithm fails is open
(@sec-open). Price-then-run (@prop-ptr) runs in
$O(N + N^(3\/8) B_2^(3\/4))$ rather than $O(N + B_2)$. Since $B_2$ can exceed AGM (double stars),
@thm-pb-upper is useful only together with $C <= N + sqrt(|R| |S| |T|)$
(@lem-sum).

The family $cU(m)$ has no triangles, so one may ask whether the gap is
an artefact of dead tuples. It is not.

#lemma(name: "padding")[
  Let $I$ be an instance and pad it as follows: for every vertex $v$
  that has a tuple in exactly one of its two relations, add two fresh
  vertices and the three tuples of one triangle through $v$ (for
  $v = x$: fresh $y', z'$ with $(x, y') in R$, $(y', z') in S$,
  $(z', x) in T$). Let $p <= 2N$ be the number of padded vertices. The
  padded instance $I'$ satisfies:
  (i) it is pairwise semijoin-reduced (every vertex with a tuple has a
  tuple in both of its relations);
  (ii) $N' = N + 3p <= 7N$ and $Out' = Out + p$;
  (iii) every $C_v$ and every $M_pi$ is nondecreasing, and
  $C'_v <= C_v + 9N$ for each root $v$;
  (iv) each of the six squared-degree sums is at most $2(dot) + 8N$.
] <lem-pad>
#st[#proved]

#proof[
  (i) Padded vertices gain the missing relation; fresh vertices have
  both. (ii) Each fresh pair closes exactly one triangle: a fresh
  vertex is adjacent only to its partner and to $v$. (iii) Adding tuples
  never lowers a degree, so per-edge costs and the minimum of two
  option costs do not decrease. An old vertex gains tuples only from its
  own pad, so each old degree grows by at most $1$, and each old term
  $1 + min(dot, dot)$ by at most $1$; keeping the old option choices,
  old terms add at most $N$. A padded vertex of root $v$ gains one term
  of cost at most $2$ in its chosen option (its new neighbour has degree
  $1$), and a fresh vertex of root $v$ has both options of cost $2$;
  there are at most $p$ of each, so $C'_v <= C_v + N + 4p <= C_v + 9N$.
  (iv) $(d + 1)^2 <= 2d^2 + 2$ for each of at most $p$ old vertices,
  and each of at most $2p$ fresh vertices contributes $1$.
]

#remark(name: [the gap survives reduction and connectivity])[
  (a) _Semijoin reduction._ Padding $cU(m)$ gives a pairwise
  semijoin-reduced instance with $Out = Theta(N)$ (the $m^8$ vertices
  of each copy of $Y_2$ are padded), $C >= m^9$ by monotonicity, and
  $N + B_2 = O(m^8)$ by @lem-pad(ii) and (iv). So the $Omega(N^(1\/8))$
  gap holds on semijoin-reduced inputs with $Theta(N)$ triangles; the
  measured ratios $C\/(N + B_2)$ are $0.397$, $0.425$, $0.453$ for
  $m = 2, 3, 4$.
  (b) _Root choice per component._ $cU(m)$ is disconnected, and each
  component alone has $C(G_8) = C_y (G_8) = m^5$. Adding two
  $R$-tuples that join the three copies makes the instance connected,
  changes $N$ by $2$ and the squared norms by $O(m^4)$, and cannot lower
  any cost, so $C >= m^9$ still holds. (c) _Both at once._ Add the two
  joining $R$-tuples after padding, between vertices that already have
  tuples in both of their relations. Every vertex still has tuples in
  both of its relations, so the instance stays pairwise
  semijoin-reduced; by the monotonicity of @lem-pad(iii), $C >= m^9$;
  and $N + B_2 = O(m^8)$, since the two tuples change $N$ by $2$ and the
  squared norms by $O(m^4)$. What escapes the bound is choosing
  different roots for different regions of one variable's domain, which
  is partitioning.
] <rem-pb-reduce>
#st[#proved (the ratios in (a) are measured)]

#theorem(name: [tightness of @thm-pb-upper across slopes])[
  Fix integers $i >= j >= 1$ and $u >= 2$. Let $F_(i,j) (u)$ have parts
  $X$ of size $u^(4i)$, $Y_0$ of size $u^(4i - 2j)$, $Y_2$ of size
  $u^(8i)$, $Z_1$ of size $u^(4i - j)$ and $Z_2$ of size $u^(4i + 2j)$,
  with $R = X times Y_0$ complete,
  $S = (Y_0 times Z_1) union (Y_2 -> Z_2)$ where the second block has
  $d^+_S = 1$, and $T = Z_2 -> X$ biregular with $d^-_T = u^(4i - j)$ on
  $X$ and $d^+_T = u^(4i - 3j)$ on $Z_2$. The union of $F_(i,j) (u)$
  and its two rotations satisfies $C >= u^(12i - 3j)$,
  $u^(8i) <= N <= 12 u^(8i)$ and $B_2 <= 4 u^(12i - 4j)$, hence
  $
    C >= N^(3\/8) B_2^(3\/4) \/ (12^(3\/8) dot 4^(3\/4)),
  $
  and $B_2 = Theta(N^kappa)$ with $kappa = 3\/2 - j\/(2i)$. Together with
  the complete block triangle $K_(s,s,s)$ ($kappa = 3\/2$), @thm-pb-upper
  is tight up to a constant factor on a dense set of slopes
  $kappa in [1, 3\/2]$, and by @cor-real-slopes at every slope in
  $[1, 3\/2]$.
] <thm-pb-slopes>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  For $x in X$, $c_R (x) = u^(4i - 2j) (1 + u^(4i - j))$ (each $y in Y_0$
  has $d^+_S = u^(4i - j) = d^-_T (x)$) and
  $c_T (x) = u^(4i - j) (1 + u^(4i - 2j))$ (each $z in Z_2$ has
  $d^-_S = u^(4i - 2j) = d^+_R (x)$); both are at least $u^(8i - 3j)$, so
  $C_x (F) >= u^(12i - 3j)$, and every root of the union contains a
  copy of root $x$ of $F$. Each copy has $N <= 4u^(8i)$, since $j <= i$.
  Norms of one copy: $alpha = gamma = u^(12i - 4j)$ and
  $beta = u^(12i - 4j) + u^(8i) <= 2u^(12i - 4j)$; in the union each
  forward norm is their sum. The displayed inequality follows. For the
  slope, @thm-pb-upper with $C >= u^(12i - 3j)$ and $12i - 3j > 8i$
  forces $B_2^(3\/4) = Omega(u^(9i - 3j))$, so
  $B_2 = Theta(u^(12i - 4j))$. For $K_(s,s,s)$, $N = 3s^2$,
  $B_2 = s^3$ and $C = s^2 (1 + s)$.
]

#corollary(name: [every real slope in $[1, 3\/2]$])[
  Fix a real $kappa in [1, 3\/2)$, put $theta = 3 - 2 kappa in (0, 1]$,
  and for every integer $n >= 1\/theta$ take the union of $F_(i,j) (2)$
  and its two rotations with $i = n$, $j = floor(theta n)$. Then
  $3 dot 2^(8n) <= N <= 12 dot 2^(8n)$,
  $3 dot 2^(8 kappa n) <= B_2 < 64 dot 2^(8 kappa n)$ and
  $C >= N^(3\/8) B_2^(3\/4) \/ (12^(3\/8) dot 4^(3\/4))$. Hence
  $B_2 = Theta(N^kappa)$ and $C = Theta(N^(3\/8 + 3 kappa\/4))$ with
  constants independent of $n$, and, with $K_(s,s,s)$ at $kappa = 3\/2$,
  @thm-pb-upper is tight up to a constant factor at every real
  $kappa in [1, 3\/2]$.
] <cor-real-slopes>
#st[#proved (exact checks in @app-verify. This extension was found by a model-based review: the GPT-6-Astra Pro review of the second draft, @sec-ai.)]

#proof[
  $1 <= j <= i$ because $theta n >= 1$ and $theta <= 1$. By the proof of
  @thm-pb-slopes, each forward squared-degree sum of the union is
  $3u^(12i - 4j) + u^(8i)$ and each reverse sum is
  $3u^(12i - 2j) + u^(12i - 5j)$, which is larger; so
  $B_2 = 3u^(12i - 4j) + u^(8i)$, and
  $N = 3(u^(8i) + u^(8i - j) + u^(8i - 2j) + u^(8i - 3j))$. With
  $u = 2$, $i = n$ and $epsilon = theta n - j in [0, 1)$ we get
  $12n - 4j = 8 kappa n + 4 epsilon$, so
  $3 dot 2^(8 kappa n) <= 3 dot 2^(12n - 4j) < 48 dot 2^(8 kappa n)$, and
  $2^(8n) <= 2^(8 kappa n)$ because $kappa >= 1$. The bound on $C$ is the
  displayed inequality of @thm-pb-slopes, whose constants do not depend
  on $(i, j)$. The upper bound is @thm-pb-upper.
]

*The gadget $D(L, a, h)$.* For integers $L, a, h >= 1$ with $h | L$, put
$b = L\/h$ and take tagged classes $X = [h] times [b]$, $Y_0 = [a]$,
$Y_2 = [h]^2 times [a]$, $Z_1 = [h]$, $Z_2 = [h]^2$, with
$
  R = X times Y_0, quad
  S = (Y_0 times Z_1) union {((i,j,k), (i,j))}, quad
  T = {((i,j), (i,ell)) : i, j in [h], ell in [b]}.
$
By direct counting, $(|R|, |S|, |T|) = (L a, a h + a h^2, L h)$,
$(alpha, beta, gamma) = (L a^2, 2 a h^2, L^2)$,
$(alpha', beta', gamma') = (a L^2, a^2 (h + h^2), L h^2)$,
$(M_R, M_S, M_T) = (L a h, 0, L a h)$,
$(C_x, C_y, C_z) = (L a h + L min(a, h), thick a h, thick a h^2)$ and
$Out = 0$: an $R$-tuple sees degrees $(h, h)$, a $T$-tuple $(a, a)$,
every $S$-tuple has a zero adjacent degree; at $x$ the options cost
$a(1 + h)$ and $h(1 + a)$; at $Y_0$ option $S$ costs $h$, and $Y_2$ has
an empty option; at $Z_1$ option $T$ is empty, and at $Z_2$ option $S$
costs $a < (L\/h)(1 + a)$. $D(u^(4i), u^(2i), u^(3i))$ is $F_(i,i) (u)$.

#theorem(name: [the worst-case exponent at slopes in $[9\/10, 1)$])[
  Let $u >= 2$ and integers $p, q$ with $9\/10 <= p\/q <= 1$. Take the
  vertex-disjoint union of
  $D_1 = D(u^(8p - 4q), u^(6q - 4p), u^(6p - 3q))$ in its own
  orientation;
  $D_2 = D(u^(4q), u^(4p - 2q), u^(6p - 3q))$ with its local $R, S, T$
  placed as the global $S, T, R$ (its $X, Y, Z$ become the global
  $Y, Z, X$); and $D_3 = D(u^(4p), u^(6p - 4q), u^(6q - 3p))$ with its
  local $R, S, T$ placed as the global $T, R, S$. Then
  $(alpha, beta, gamma) = (4u^(8q), 4u^(8p), 4u^(16p - 8q))$, every
  reverse moment is at least its forward counterpart, so
  $B_2 = 4u^(8p)$; $u^(8q) <= N <= 12 u^(8q)$; and
  $C = C_x = u^(10p - q) + u^(4p + 2q) + u^(16p - 8q) + u^(3p + 2q)$, so
  $u^(10p - q) <= C <= 4u^(10p - q)$ and
  $C >= 4^(-5\/4) N^(-1\/8) B_2^(5\/4)$. Consequently, for every real
  $kappa in [9\/10, 1)$ (take $u = 2$, $q -> infinity$,
  $p = floor(kappa q)$, or $p\/q = kappa$ if $kappa$ is rational) there
  are instances with $B_2 = Theta(N^kappa)$ and
  $C = Theta(N^((10 kappa - 1)\/8))$, so
  $C\/(N + B_2) = Theta(N^((10 kappa - 9)\/8))$; @thm-pb-upper2 is
  attained up to the factor $3^(1\/8) dot 4^(5\/4) < 6.5$, and
  below slope $1$, $C = O(N + B_2)$ fails, even with any fixed
  polylogarithmic factor, exactly on $(9\/10, 1)$ (by @thm-pb-slopes
  and @cor-real-slopes it also fails at every slope in $[1, 3\/2)$,
  where the exponent $3\/8 + 3 kappa \/ 4$ exceeds $kappa$, so over
  $[9\/10, 3\/2]$ it fails exactly on $(9\/10, 3\/2)$).
] <thm-pb-asym>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  _Parameters._ The exponent differences giving $h_i | L_i$ are
  $2p - q$, $7q - 6p$, $7p - 6q$, and those giving $a_i <= h_i$ are
  $10p - 9q$, $2p - q$, $10q - 9p$; all are nonnegative for
  $9\/10 <= p\/q <= 1$. _Moments._ $D_1$ contributes
  $(u^(8q), 2u^(8p), u^(16p - 8q))$ to $(alpha, beta, gamma)$. In $D_2$
  the local forward sums $(L a^2, 2 a h^2, L^2) = (u^(8p), 2u^(16p - 8q), u^(8q))$
  land on $(beta, gamma, alpha)$, and in $D_3$ the local sums
  $(u^(16p - 8q), 2u^(8q), u^(8p))$ land on $(gamma, alpha, beta)$;
  the totals are as stated. The reverse moments are
  $alpha' = 2u^(12p - 2q) + u^(9p - 2q) + u^(6p + 4q)$,
  $beta' = u^(9q - 2p) + 2u^(4p + 6q) + u^(12q - 2p)$,
  $gamma' = 2u^(20p - 10q) + u^(14p - 7q) + u^(14p - 4q)$; their terms with
  exponents $6p + 4q$, $12q - 2p$, $14p - 4q$ exceed $8q$, $8p$,
  $16p - 8q$ by $6p - 4q$, $12q - 10p$, $4q - 2p$, integers at least
  $2$, so each alone is at least $4$ times the forward counterpart.
  _Costs._ The global root $x$ is local root $x$ of $D_1$, local root $z$
  of $D_2$ and local root $y$ of $D_3$, so
  $C_x = (L a h + L a)_(D_1) + (a h^2)_(D_2) + (a h)_(D_3)$, which is the
  stated sum; likewise
  $C_y = u^(10p - q) + u^(4p + 2q) + u^(8q) + u^(2p + 3q)$ and
  $C_z = u^(7p + 2q) + u^(10p - 4q) + u^(8p) + u^(10p - 5q)$. Every
  term of $C_x$ is at most $u^(10p - q)$, so $C_x <= 4u^(10p - q)$;
  $C_x <= C_y$ termwise; and if $p < q$ the leading term of $C_z$ is
  $u^(7p + 2q) >= u^3 u^(10p - q) > C_x$, while for $p = q$ the three
  costs coincide. So $C = C_x >= u^(10p - q)$.
  _Size._ $N$ is a sum of twelve powers of $u$ with exponents at most
  $8q$, one of them $8q$. _Rate._ $N^(-1\/8) B_2^(5\/4) <= u^(-q) 4^(5\/4) u^(10p) <= 4^(5\/4) C$.
  With $u = 2$ and $p = floor(kappa q)$, eventually $9\/10 <= p\/q < 1$
  (for $kappa > 9\/10$), $8 kappa q - 8 < 8p <= 8 kappa q$, so
  $B_2 = Theta(N^kappa)$ and
  $C >= 2^(10p - q) >= 2^(-10) (2^(8q))^((10 kappa - 1)\/8)$; the upper
  bound is @thm-pb-upper2, and $N + B_2 = Theta(N)$ for $kappa < 1$.
  Below $9\/10$, @cor-pb(2) gives $C = O(N + B_2)$.
]

So the worst-case exponent of $C$ at slope $kappa$ is
$min(3\/2, max(1, min((10 kappa - 1)\/8, thick 3\/8 + 3 kappa\/4)))$
for every real $kappa >= 9\/10$, and at most $1$ below; @fig-fbeta plots
it.

#figure(
  placement: top,
  caption: [Worst-case exponent of the per-binding cost on instances with
    $B_2 = N^kappa$. Thick solid: the exponent
    $max(1, min((10 kappa - 1)\/8, 3\/8 + 3 kappa\/4))$ of the bounds of
    @thm-pb-upper2 and @thm-pb-upper, capped at $3\/2$ by
    $C <= N + sqrt(|R| |S| |T|)$ (@lem-sum). It is the exact worst-case
    exponent at every real $kappa in [9\/10, 3\/2]$ (@thm-pb-asym,
    @cor-real-slopes); thin solid, for $kappa <= 9\/10$, only the upper
    bound $C < 2.15 N$ (@cor-pb). Dotted: the exponent
    $3\/8 + 3 kappa\/4$ of @thm-pb-upper alone on $(5\/6, 1)$. Dashed:
    the exponent $max(1, kappa)$ of $N + B_2$. Dots: $F_(i,j)$ at
    $(i,j) = (1,1), (6,5), (5,4), (4,3), (3,2), (5,3), (2,1), (5,2), (3,1), (4,1), (6,1)$
    ($kappa = 3\/2 - j\/(2i)$, exponent $3\/2 - 3j\/(8i)$); diamonds: the
    asymmetric family of @thm-pb-asym at
    $p\/q = 9\/10, 11\/12, 14\/15, 19\/20, 39\/40$ (exponent
    $(10p - q)\/(8q)$); ring: the union $cU(m)$ of @thm-pb-lower
    ($kappa = 1$, exponent $9\/8$); square: $K_(s,s,s)$. The lower panel
    plots the gap over $N + B_2$: $0$ up to $9\/10$, rising to $1\/8$ at
    $kappa = 1$ and falling to $0$ at $3\/2$. Generated by
    `make_fbeta_figure.py` with exact rational exponents.],
  image("fbeta.svg", width: 100%),
) <fig-fbeta>

== Fully reduced inputs <sec-fullred>

Padding (@rem-pb-reduce) leaves most tuples outside triangles. When
_every_ tuple lies in a triangle ("fully reduced") the low-slope
families cannot be used: a triangle has one tuple of each relation, so
$Out >= max(|R|, |S|, |T|) >= N\/3$, and $Out <= B_2$ (@sec-prelim);
hence $B_2 >= N\/3$ and every growing fully reduced family has slope
$kappa >= 1$. The gap shrinks but survives. The gadget below keeps the
two expensive options of $F_(i,j)$ at every $x$ and adds helper
vertices that close every tuple.

*The live gadget $L(p, q, t, g, k, w)$.* Let $p, q, t, g, k, w$ be
positive integers with $t | p$, $g | p t$, $g <= p$, $k | q$, and, for
$z = p t \/ g$, $q | z$ and $w | z$. Take parts $X_0$ of size $p$,
$Y_0$ of size $q$, $Z_1$ and $Z_w$ of size $t$ each, and $Z_2$ of size
$z$. Split $Z_2$ into $z\/w$ groups $W$ of $w$ vertices; each group owns
$q$ fresh $y$-vertices $Y_W$, split into $q\/k$ blocks of $k$, and
$q\/k$ fresh helper $x$-vertices $h_(W,1), dots, h_(W,q\/k)$. Then
$
  R &= X_0 times Y_0 union {(h_(W,m), y) : y "in block" m "of" Y_W}, \
  S &= Y_0 times (Z_1 union Z_w) union S_0 union union.big_W Y_W times W, \
  T &= T_2 union T_w union T_1 union union.big_W W times {h_(W,1), dots, h_(W,q\/k)},
$
where $S_0 subset.eq Y_0 times Z_2$ gives every $z in Z_2$ one
predecessor and every $y in Y_0$ exactly $z\/q$ successors,
$T_2 subset.eq Z_2 times X_0$ is biregular with out-degree $g$ and
in-degree $t$, $T_w subset.eq Z_w times X_0$ is biregular with
out-degree $p\/t$ and in-degree $1$, and $T_1$ is a matching of $Z_1$
onto $t$ distinct vertices of $X_0$.

#lemma(name: "the live gadget")[
  Every tuple of $L = L(p, q, t, g, k, w)$ lies in a triangle,
  $Out(L) = t q + p q + p t + z q$, and every $x in X_0$ has both option
  costs at least $q t$, so $C_x (L) >= p q t$. Its sizes are
  $(|R|, |S|, |T|) = (p q + z q \/ w, thick 2 q t + z + z q, thick p t + p + t + z q \/ k)$,
  its forward squared-degree sums are
  $(alpha, beta, gamma) = (p q^2 + z q k \/ w, thick q (2t + z\/q)^2 + z q w, thick t + p^2\/t + z (g + q\/k)^2)$,
  and its reverse sums are
  $(alpha', beta', gamma') = (q p^2 + z q \/ w, thick 2 t q^2 + z (q + 1)^2, thick (p - t)(t + 1)^2 + t (t + 2)^2 + z q w \/ k)$.
] <lem-live>
#st[#proved]

#proof[
  _Support._ An $X_0 times Y_0$ tuple $(x, y)$ closes through the unique
  $T_w$-predecessor of $x$, since $Y_0 times Z_w$ is complete. A tuple
  $(y, z)$ with $z in Z_1 union Z_w union Z_2$ closes through any
  $T$-successor of $z$ in $X_0$, since $X_0 times Y_0$ is complete; a
  $T$-tuple $(z, x)$ with $x in X_0$ closes through a $Y_0$-predecessor
  of $z$ (every $z$ of $Z_1 union Z_w union Z_2$ has one). For a group
  $W$, a tuple $(h_(W,m), y)$, $(y, z)$ or $(z, h_(W,m))$ with $y$ in
  block $m$ of $Y_W$ and $z in W$ lies in the triangle
  $(h_(W,m), y, z)$. _Output._ The triangles are $(x_i, y, z_i)$ through
  $T_1$ ($t q$), $(x, y, z)$ through the $T_w$-predecessor of $x$
  ($p q$), $(x, y_z, z)$ through $T_2$ with $y_z$ the $S_0$-predecessor
  of $z$ ($z g = p t$), and the helper triangles ($q w$ per group,
  $z q$ in all). _Degrees._ On $X_0$, $d^+_R = q$ and
  $d^-_T = t + 1 + [x in T_1 (Z_1)]$; on a helper, $d^+_R = k$ and
  $d^-_T = w$; on $Y_0$, $d^-_R = p$ and $d^+_S = 2t + z\/q$; on
  $Y_W$, $d^-_R = 1$ and $d^+_S = w$; on $Z_1$ and $Z_w$, $d^-_S = q$
  and $d^+_T = 1$, resp. $p\/t$; on $Z_2$, $d^-_S = q + 1$ and
  $d^+_T = g + q\/k$. The sizes and moments follow. _Cost._ At
  $x in X_0$, option $R$ walks $q$ vertices $y$ with
  $min(d^+_S (y), d^-_T (x)) >= t$, and option $T$ walks at least $t$
  vertices of $Z_2$ with $min(d^+_R (x), d^-_S (z)) = q$.
]

#theorem(name: [fully reduced inputs: gap in $[1\/10, 1\/8]$])[
  For $v >= 2$ let $cL(v)$ be the disjoint union of
  $L(v^5, v^3, v^4, v^2, v^2, v)$ and its two rotations. It is fully
  reduced, with
  $
    N = 3(v^10 + 2v^9 + 2v^8 + 3v^7 + v^5 + v^4) <= 9v^10, quad
    Out = 3(v^10 + v^9 + v^8 + v^7), \
    alpha = beta = gamma = 13v^11 + 2v^10 + v^9 + v^6 + v^4 <= 15 v^11, quad
    C = v^12 + 4v^10 + 3v^9 + 7v^8 + 7v^7 + v^5 + v^4,
  $
  and every reverse moment larger than $alpha$, so $B_2 = alpha$,
  $B_2 = Theta(N^(11\/10))$ and
  $
    C \/ (N + B_2) >= v\/24 >= (N\/9)^(1\/10) \/ 24.
  $
  More generally, for integers $i >= 1$, $j >= 0$ with $5j <= 4i$ and
  $u >= 2$, the union of three rotations of
  $L(u^(4i), u^(4i - 2j), u^(4i - j), u^(4i - 3j), u^j, 1)$ is fully
  reduced with $C >= u^(12i - 3j)$, $N = Theta(u^(8i))$ and
  $B_2 = Theta(u^(12i - 4j))$, the constants independent of $i, j, u$.
  With $u = 2$, $i = n$, $j = floor((3 - 2 kappa) n)$ this gives, for
  every real $kappa in [11\/10, 3\/2]$, fully reduced instances with
  $B_2 = Theta(N^kappa)$ and $C = Theta(N^(3\/8 + 3 kappa\/4))$. So on
  fully reduced inputs the worst-case exponent of $C$ equals the general
  one (@thm-pb-upper) at every slope in $[11\/10, 3\/2]$, the
  worst-case gap against $N + B_2$, over all slopes, lies in
  $[1\/10, 1\/8]$, and it is open only on the window
  $kappa in [1, 11\/10)$.
] <thm-fullred>
#st[#proved (verified by two separately run exact-arithmetic rebuilds; not
in Lean; @app-verify)]

#proof[
  _$cL(v)$._ The parameters satisfy the divisibility conditions
  ($z = v^7$). The union of fully reduced instances is fully reduced. By
  @lem-live and rotation, each root of the union contains a copy of
  root $x$ of one gadget, so $C >= p q t = v^12$; direct counting of the
  other two roots of each gadget, whose cheaper options cost
  $O(N)$, gives the displayed polynomial. Each forward moment of the
  union is $alpha + beta + gamma$ of one gadget:
  $2v^11 + (9v^11 + v^11) + (v^4 + v^6 + v^11 + 2v^10 + v^9)$, and each
  reverse moment is $alpha' + beta' + gamma' = (v^13 + v^9) + (v^13 + 4v^10 + v^7) + (v^13 + 3v^9 + 2v^8 + v^5 + 3v^4)$,
  which exceeds the forward one for $v >= 2$ (their difference is
  $3v^13 - 13 v^11 + 2v^10 + 3v^9 + 2v^8 + v^7 - v^6 + v^5 + 2v^4 > 0$).
  $N <= 9 v^10$ because $2v^9 + 2v^8 + 3v^7 + v^5 + v^4 <= 2 v^10$ for
  $v >= 2$; then $C\/(N + B_2) >= v^12\/(9 v^10 + 15 v^11) >= v\/24$.
  _The general family._ Here $z = u^(4i + 2j)$, and $3j <= 4i$ gives
  $k | q$. By @lem-live every root of the union costs at least
  $p q t = u^(12i - 3j)$. The size monomials have exponents at most
  $8i$, attained by $z q = u^(8i)$; the forward moment monomials have exponents among
  $12i - 4j$, $8i + j$, $4i + 6j$, $8i$, $4i + j$ and $4i - j$, all at most
  $12i - 4j$ exactly when $5j <= 4i$, with $12i - 4j$ attained by
  $p q^2$; and the reverse moments contain $q p^2 = u^(12i - 2j)$. Each
  statistic is a sum of a bounded number of such monomials with bounded
  coefficients, which gives the $Theta$'s with absolute constants and
  $kappa = 3\/2 - j\/(2i) in [11\/10, 3\/2]$. For real $kappa$, the
  floor changes $4j$ by less than $4$, as in @cor-real-slopes; at
  $kappa = 3\/2$ take $j = 0$. The upper bounds are @thm-pb-upper and
  @cor-pb(1), whose gap $(3 - 2kappa)\/8$ is at most $1\/8$ and equals
  $1\/10$ at $kappa = 11\/10$.
]

#remark(name: [the window $kappa in [1, 11\/10)$])[
  (a) _A lower bound on the window._ Adding $v^11$ disjoint isolated
  triangles to the three rotations of $L(v^5, v^3, v^4, v^2, v, 1)$
  keeps the instance fully reduced and gives $N = Theta(v^11)$,
  $B_2 = Theta(v^11)$ and $C >= v^12$: gap $1\/11$ at slope $1$
  (exactly, at $v = 2$: $N = 17424$, $C = 17840$, $B_2 = 33872$;
  at $v = 3$: $N = 1044171$, $C = 1321272$, $B_2 = 2894211$). Scaling the
  core parameters in the same way gives gap $kappa\/11$ at every
  $kappa in [1, 11\/10]$, so on the window the fully reduced gap lies in
  $[kappa\/11, (3 - 2kappa)\/8]$.
  (b) _The limit of this design._ For a union of three rotated live
  gadgets with arbitrary valid parameters,
  $min_i p_i q_i t_i <= C <= 3N + min_i p_i q_i t_i$ (the other two
  roots of a gadget cost at most $3N_g\/2$ and $2N_g$, and the
  non-critical part of root $x$ at most $3N_g$). In exponent form, with
  $c = P + Q + T$ the designated cost exponent and $m$ the average
  forward moment exponent, two linear identities over the gadget
  parameters give $c <= 12 m\/11$ and $c <= 3\/8 + 3m\/4$, so
  $c - m <= min(m\/11, (3 - 2m)\/8) <= 1\/10$, with equality only at
  $m = 11\/10$, and a controlling reverse moment gives no gap at all.
  So this design cannot close the window or exceed $1\/10$; doing so
  needs another design or an upper bound that uses triangle support,
  not only pairwise support. An exponent program over the design that
  bounds size exponents by $1$ without forcing one to equal $1$ has
  value $1\/11$ at budget slope $1$, but its optimum has actual slope
  $11\/10$; the value $1\/11$ at actual slope $1$ is attained only with
  the padding of (a).
] <rem-window>
#st[#proved (exact checks in @app-verify)]

An earlier draft used a different fully reduced gadget, with gap $1\/12$ and
an explicit instance with $C > N + B_2$ already at $N approx 2.4 dot 10^11$
($cL(v)$ first exceeds $1$ at $v = 14$, $N approx 1.0 dot 10^12$); it is
kept in @app-iv.

== Separations from fixed orders and fixed roots <sec-sep>

A strategy has _worst-case gap_ $delta$ against a comparator $K$ if its
cost is at most $N^(delta + o(1)) K$ on all instances and this is
attained. By @thm-pb-upper and @thm-pb-lower, per-binding choice has
gap exactly $1\/8$ against $N + B_2$ (at $B_2 asymp N$). The families
below use three distinct relations.

*Additional families.* $"GMR"(m)$: $X$ of size $m^3$, $Y$ of size $m$,
$Z_0$ of size $m^4$, $Z_1$ of size $m$; $R = X times Y$,
$S = Y times Z_1$, and $T = Z_0 -> X$ biregular with $d^-_T = m$ on $X$
and $d^+_T = 1$ on $Z_0$. $"GMIN"(m)$, for $m >= 2$, has parts
$X_0, X_1, X_2, X_3$ of sizes $m^3, m^5, m^2, m$;
$Y_0, Y_1, Y_2, Y_3$ of sizes $m, m^3, m^2, m^5$;
$Z_0, Z_1, Z_2, Z_3$ of sizes $m^5, m^2, m, m^3$; and blocks
$R = X_0 times Y_0 union (X_1 -> Y_1) union X_3 times Y_2$,
$S = Y_0 times Z_1 union Y_1 times Z_2 union (Y_3 -> Z_3)$,
$T = (Z_0 -> X_0) union Z_2 times X_2 union Z_3 times X_3$, where
$X_1 -> Y_1$ and $Y_3 -> Z_3$ are biregular with out-degree $1$, and
$Z_0 -> X_0$ is biregular with $d^-_T = m^2$ on $X_0$ and $d^+_T = 1$ on
$Z_0$; all other blocks are complete.

#theorem(name: "fixed orders, fixed roots, and two levels of adaptivity")[
  + _(one fixed GAO)_ For $a >= 2$, $cF_a$ has $M_R = a^3$,
    $M_S = M_T = a^2$, $C = 2 a^2$, $Out = a^2$, $N = 3 a^2$,
    $B_2 = a^(8\/3)$, and is pairwise semijoin-reduced. So the GAOs whose
    second relation is $R$ cost $Theta(N^(1\/2)) dot C$ and
    $Theta(N^(1\/6)) dot (N + B_2)$. On general inputs, $"GMR"(m)$ has
    $M_R = m^5$, $M_S = M_T = 0$, $C = 0$, $N = 2m^4 + m^2$ and
    $B_2 <= m^4$, so those GAOs cost
    $M_R \/ (N + B_2) >= m\/4 = Theta(N^(1\/4))$ times $N + B_2$.
    Rotations give the same for the other second relations.
  + _(best of the six GAOs)_ For $a >= 2$, $cG_a$ has
    $min(M_R, M_S, M_T) = a^3 + 2 a^2$, $C = 6 a^2$, $N = 9 a^2$, and is
    pairwise semijoin-reduced; so the best GAO per instance costs
    $Theta(N^(1\/2)) dot C$. For $m >= 2$, $"GMIN"(m)$ has
    $M_R = M_S = M_T = m^6$, $C = m^5 + m^3 <= N$,
    $N = 3(m^5 + m^4 + m^3)$ and $alpha = beta = gamma = 3m^5$ (and
    larger reverse norms), so $B_2 = 3m^5$ and
    $min_pi M_pi \/ (N + B_2) >= m\/9 = Theta(N^(1\/5))$ while
    $min_pi M_pi \/ C >= m\/2$. $"GMIN"(m)$ has no triangles and is not
    semijoin-reduced; its padding (@lem-pad) is pairwise
    semijoin-reduced with $Out = Theta(N)$, $C = Theta(N)$,
    $N + B_2 = Theta(m^5)$ and $min_pi M_pi >= m^6$. So the best GAO
    loses $Theta(N^(1\/5))$ against both $N + B_2$ and $C + N$, on
    semijoin-reduced inputs with $C = Theta(N)$.
  + _(fixed root)_ For $a >= 2$, $cH_a$ has $C_x = a^3 + a^2$,
    $C_y = C_z = a^2$, $Out = 0$, $N = 4 a^2$; its padding is pairwise
    semijoin-reduced, keeps $C_x >= a^3$ and has $C + N = Theta(a^2)$.
    So root $x$ with per-binding option choice costs
    $Theta(N^(1\/2)) dot (C + N)$, on semijoin-reduced inputs as well.
    Against $N + B_2$, a single $G_8 (m)$ has $C_x = m^9 + m^6$,
    $C = C_y = m^5$ and $N + B_2 = Theta(m^8)$, so a fixed root loses
    $Theta(N^(1\/8))$ against $N + B_2$, and $Theta(N^(1\/2))$ against
    $C$ alone. Rotations give the same for roots $y$ and $z$.
] <thm-sep>
#st[#proved]

#proof[
  (1) $cF_a$: $X = {x_i}$, $Y = {y_j}$, $Z = {z_(i,k)}$ for
  $i, j, k in [a]$; $R = X times Y$; $S = {(y_i, z_(i,k))}$;
  $T = {(z_(i,k), x_i)}$. Degrees: $d^+_R = d^-_R = a$,
  $d^+_S (y) = a$, $d^-_S (z) = 1$, $d^+_T (z) = 1$, $d^-_T (x) = a$.
  A triangle $(x_i, y_j, z)$ needs $z = z_(j,k)$ with $(z, x_i) in T$,
  so $j = i$ and $Out = a^2$. Every endpoint of every tuple has an
  incident tuple in both other relations (the instance is pairwise
  semijoin-reduced). $M_R = a^2 dot min(a, a) = a^3$;
  $M_S = a^2 dot min(1, a) = a^2$; $M_T = a^2 dot min(a, 1) = a^2$.
  Root $x$: $c_R = a(1 + a)$ and $c_T = a(1 + 1) = 2a$, so
  $C_x = 2 a^2$; similarly $C_y = C_z = 2 a^2$ (root $y$: options cost
  $a(1+a)$ and $2a$; root $z$: both cost $2$). Forward squared degree
  sums are $a^3, a^3, a^2$ and reverse ones $a^3, a^2, a^3$, so
  $B_2 = a^(8\/3)$. Then $M_R \/ C = a\/2 = Theta(N^(1\/2))$ and
  $M_R \/ (N + B_2) = a^3 \/ (3a^2 + a^(8\/3)) = Theta(N^(1\/6))$.
  $"GMR"(m)$: every $R$-tuple has $d^+_S (y) = m = d^-_T (x)$, so
  $M_R = m^4 dot m$; $S$ ends in $Z_1$, where $d^+_T = 0$, and $T$
  starts in $Z_0$, where $d^-_S = 0$, so $M_S = M_T = 0$; for root $z$
  every binding has an empty option, so $C = 0$. Norms:
  $alpha = m^3 dot m^2$, $beta = m dot m^2$, $gamma = m^4$, so
  $B_2 <= (m^12)^(1\/3)$.

  (2) $cG_a$ is the disjoint union of $cF_a$ and its two rotations, hence
  semijoin-reduced. Each $M_pi$ equals $a^3$ on one copy and $a^2$ on
  the other two, so $M_pi = a^3 + 2a^2$ for every $pi$; by @lem-sum
  every GAO costs at least this. In $cF_a$ all of $C_x, C_y, C_z$ equal
  $2a^2$, so in each copy, whatever its rotation, every root costs
  $2a^2$, and $C = 6 a^2$.
  $"GMIN"(m)$: $M_R$ collects $m^4 dot min(m^2, m^2)$ from
  $X_0 times Y_0$ ($d^+_S = |Z_1|$ on $Y_0$, $d^-_T = m^2$ on $X_0$) and
  $0$ from the other blocks ($d^-_T = 0$ on $X_1$, $d^+_S = 0$ on
  $Y_2$). Likewise $M_S = m^6$ from $Y_1 times Z_2$
  ($d^+_T = |X_2|$, $d^-_R = m^2$) and $M_T = m^6$ from
  $Z_3 times X_3$ ($d^+_R = |Y_2|$, $d^-_S = m^2$); every other block
  meets a zero degree. Root $x$: $X_0$ takes option $T$ ($m^2$
  unit-cost tuples from $Z_0$, where $d^-_S = 0$; option $R$ costs
  $m(1 + m^2)$), giving $m^3 dot m^2$; $X_3$ takes option $R$ ($m^2$
  unit-cost tuples into $Y_2$, where $d^+_S = 0$), giving $m dot m^2$;
  $X_1$ ($d^-_T = 0$) and $X_2$ ($d^+_R = 0$) have an empty option. So
  $C_x = m^5 + m^3$. Symmetrically, $C_y = m^3 + m^5$ ($Y_0$, option $S$
  into $Z_1$, where $d^+_T = 0$; $Y_1$, option $R$ from $X_1$, where
  $d^-_T = 0$) and $C_z = m^3 + m^5$ ($Z_2$, option $T$ into $X_2$; $Z_3$,
  option $S$ from $Y_3$, where $d^-_R = 0$). Sizes:
  $|R| = m^4 + m^5 + m^3$, $|S| = m^3 + m^4 + m^5$,
  $|T| = m^5 + m^3 + m^4$. Forward norms: each of $X_0, X_1, X_3$
  contributes $m^5$ to $alpha$ ($m^3 dot m^2$, $m^5 dot 1$, $m dot m^4$),
  and likewise $Y_0, Y_1, Y_3$ to $beta$ and $Z_0, Z_2, Z_3$ to $gamma$.
  The reverse norms are larger ($alpha' >= m dot m^6 = m^7$ from $Y_0$,
  and similarly for $beta', gamma'$), so $B_2 = 3m^5$. We also checked
  every closed form exactly for $m = 2, dots, 12$ with two separately
  written evaluators. Then
  $m^6 \/ (6m^5 + 3m^4 + 3m^3) >= m\/9$ for $m >= 2$. No triangle exists,
  and, e.g., $X_3 times Y_2$ is an $R$-block whose $Y_2$ has no
  $S$-tuple. For the padding, @lem-pad gives $min_pi M_pi >= m^6$,
  $N' <= 7N$, $C' <= C + 9N = O(m^5)$, squared norms $O(m^5)$, and
  $C' >= Out' >= m^5$ (all of $Y_3$ is padded).

  (3) $cH_a$: $X = {x_i}$, $Y_1 = {y_i}$, $Y_2 = {y'_i}$,
  $Z_1 = {z_(i,k)}$, $Z_2 = {z'_i}$ for $i, k in [a]$;
  $R = X times Y_1$; $S = {(y_i, z_(i,k))} union Y_2 times Z_2$;
  $T = Z_2 times X$. Since $S$ maps $Y_1$ only into $Z_1$ and $T$ leaves
  only $Z_2$, $Out = 0$. Root $x$: $c_R (x) = a(1 + min(a, a))$ and
  $c_T (x) = a(1 + min(a, a))$, so $C_x = a^3 + a^2$. Root $y$: for
  $y in Y_1$, option $S$ costs $a(1 + min(a, 0)) = a$ (since
  $d^+_T = 0$ on $Z_1$); for $y in Y_2$ option $R$ is empty; so
  $C_y = a^2$. Root $z$: for $z in Z_1$ option $T$ is empty; for
  $z in Z_2$ option $S$ costs $a(1 + min(0, a)) = a$; so $C_z = a^2$.
  By @lem-pad the padded instance is pairwise semijoin-reduced, has
  $C'_x >= a^3 + a^2$, $C' <= C_y + 9N = 37a^2$ and $N' <= 28 a^2$; we
  also measured $C'_x \/ (C' + N') = 0.61, 0.97, 1.69, 3.14, 6.05$ for
  $a = 4, 8, 16, 32, 64$. $G_8 (m)$: see the proof of @thm-pb-lower; its
  forward norms are $m^8, 2m^8, 2m^8$, so $B_2 <= 4^(1\/3) m^8$.
]

All quantities stated for $cF_a, cG_a, cH_a$ were also recomputed by
brute force for $a in {4, 8, 16, 32}$, and those for $"GMR"$ and
$"GMIN"$ for $m = 2, 3, 4$ and $m = 2, dots, 12$, respectively. A single
fixed GAO always costs at least the best of the six, so @thm-sep(2)
also gives gap at least $1\/5$ for one fixed GAO on semijoin-reduced
inputs, superseding the $N^(1\/6)$ of $cF_a$ there. The families of
@thm-sep and of @thm-pb-lower are complementary: on $cF_a, cG_a, cH_a$
(and padded $cH_a$) $C = Theta(N)$, so their $Theta(N^(1\/2))$ losses are against $C + N$, the maximum
possible since every GAO costs at most $N + sqrt(|R| |S| |T|)$; the
families $G_8$, $"GMR"$ and $"GMIN"$ separate against $N + B_2$, but
against $C$ only $"GMIN"$ has $C = Theta(N)$. @tab-gaps, in @sec-intro, summarizes.

#theorem(name: "best of the six GAOs: exact gap 1/5")[
  On every instance
  $
    min(M_R, M_S, M_T)^5 <= |R| |S| |T| dot min(alpha beta gamma, alpha' beta' gamma'),
  $
  i.e. $min_pi M_pi <= (|R| |S| |T|)^(1\/5) B_2^(3\/5) <= (N\/3)^(3\/5) B_2^(3\/5)$.
  The product form (the displayed fifth-power inequality) holds with
  equality on every complete tripartite instance $K_(a,b,c)$; the
  relaxation to $(N\/3)^(3\/5)$ is tight only when in addition
  $|R| = |S| = |T|$. Hence
  $min_pi M_pi <= (2^(2\/5)\/5) N^(1\/5) (N + B_2) approx 0.264 N^(1\/5) (N + B_2)$,
  $min_pi M_pi <= 12^(-3\/5) (N + B_2)^(6\/5)$, and
  $min_pi M_pi <= 3^(-3\/5) N^(6\/5)$ when $B_2 < N$. With $"GMIN"(m)$,
  where $min_pi M_pi \/ (N + B_2) = m^3 \/ (6m^2 + 3m + 3)$, and its
  padding (@thm-sep(2)), the best of the six GAOs has worst-case gap
  exactly $1\/5$ against $N + B_2$, on general and on pairwise
  semijoin-reduced inputs, and worst-case cost $Theta((N + B_2)^(6\/5))$.
] <thm-best6>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  Write $a_x = d^+_R (x)$, $t_x = d^-_T (x)$ and
  $P(x) = sum_(y in R(x, dot)) min(d^+_S (y), t_x)$, so
  $M_R = sum_x P(x)$. Then $P(x) <= a_x t_x$ and, by step 1 of the proof
  of @lem-perroot, $P(x) <= sqrt(a_x beta)$; so
  $P(x) <= (a_x t_x)^(3\/5) (a_x beta)^(1\/5) = beta^(1\/5) a_x^(4\/5) t_x^(3\/5)$.
  Hölder with exponents $(5\/2, 5\/3)$ gives
  $M_R <= beta^(1\/5) (sum_x a_x^2)^(2\/5) (sum_x t_x)^(3\/5) = |T|^(3\/5) alpha^(2\/5) beta^(1\/5)$,
  and by rotation $M_S <= |R|^(3\/5) beta^(2\/5) gamma^(1\/5)$ and
  $M_T <= |S|^(3\/5) gamma^(2\/5) alpha^(1\/5)$. The minimum is at most
  the cube root of the product, $(|R| |S| |T| alpha beta gamma)^(1\/5)$;
  reflection gives the primed product. On $K_(a,b,c)$ every
  $M_pi = a b c$, $|R| |S| |T| = (a b c)^2$ and both moment products are
  $(a b c)^3$. With $v = B_2 \/ N$,
  $(N\/3)^(3\/5) B_2^(3\/5) \/ (N + B_2) = 3^(-3\/5) N^(1\/5) v^(3\/5)\/(1 + v)$,
  maximal at $v = 3\/2$; and $N B_2 <= (N + B_2)^2 \/ 4$. A GAO with second
  relation $pi$ costs $|pi| + M_pi <= N + M_pi$ (@lem-sum). For
  $"GMIN"(m)$, which is the union of three rotations of the gadget $E$
  below with $(L, a, h) = (m^3, m, m^2)$, @thm-sep(2) gives
  $B_2 = 3m^5$ exactly and $M_pi = m^6$.
]

*The gadget $E(L, a, h)$.* $|X| = L$, $|Y| = a$, $|Z_1| = h$,
$Z_0 = {z_(x,j) : x in X, j in [h]}$, $R = X times Y$, $S = Y times Z_1$,
$T = {(z_(x,j), x)}$. Then $(|R|, |S|, |T|) = (L a, a h, L h)$,
$(alpha, beta, gamma) = (L a^2, a h^2, L h)$,
$(alpha', beta', gamma') = (a L^2, h a^2, L h^2)$,
$(M_R, M_S, M_T) = (L a h, 0, 0)$, $(C_x, C_y, C_z) = (L h, a h, 0)$ and
$Out = 0$; $"GMR"(m) = E(m^3, m, m)$.

#theorem(name: "one fixed GAO: exact gap 1/4 on general inputs")[
  On every instance
  $M_R^4 <= |R| |T|^2 alpha beta <= |R| |T| alpha beta gamma$ and
  $M_R^4 <= |R| |S|^2 alpha' gamma' <= |R| |S| alpha' beta' gamma'$,
  and likewise for $M_S$, $M_T$ by rotation. Hence, for any prescribed
  driver, $M_R <= (N\/2)^(1\/2) B_2^(3\/4) <= (3^(3\/4) \/ (4 sqrt(2))) N^(1\/4) (N + B_2)$,
  and the coefficient $3^(3\/4)\/(4 sqrt(2)) approx 0.403$ is
  asymptotically sharp ($E(u^3, 6u, 6u)$: $N = 12u^4 + 36u^2$,
  $B_2 = 36u^4$, $M_R = 36u^5$). With $"GMR"(m)$, where
  $M_R \/ (N + B_2) = m^3 \/ (3m^2 + 1)$, the gap of one fixed GAO against
  $N + B_2$ is exactly $1\/4$ on general inputs, with worst-case cost
  $Theta((N + B_2)^(5\/4))$. On pairwise semijoin-reduced inputs it lies
  in $[1\/5, 1\/4]$ (lower bound: padded $"GMIN"$, @thm-sep(2)) and
  remains open.
] <thm-onegao>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  Keep $a_x, t_x, P(x)$ and put $b_y = d^+_S (y)$. Terms with $t_x = 0$
  have $P(x) = 0$, and weighted Cauchy--Schwarz gives
  $M_R^2 <= |T| sum_(x : t_x > 0) P(x)^2 \/ t_x$. Since
  $min(b, t) <= sqrt(b t)$,
  $P(x)^2 \/ t_x <= (sum_(y in R(x, dot)) sqrt(b_y))^2 <= a_x sum_(y in R(x, dot)) b_y$.
  With $v_y = sum_(x : (x,y) in R) a_x$ this sums to
  $sum_y b_y v_y <= sqrt(beta) (sum_y v_y^2)^(1\/2)$, and
  $v_y^2 <= d^-_R (y) sum_x a_x^2 = d^-_R (y) alpha$, so
  $sum_y v_y^2 <= |R| alpha$ and $M_R^2 <= |T| sqrt(|R| alpha beta)$;
  $gamma >= |T|$ gives the second form. Grouping by $y$ with weights
  $b_y$ instead,
  $M_R^2 <= |S| sum_y V_y^2 \/ b_y$ with
  $V_y = sum_(x : (x,y) in R) min(b_y, t_x)$,
  $V_y^2 \/ b_y <= d^-_R (y) sum_(x : (x,y) in R) t_x$; summing over $y$
  gives $sum_x t_x w_x$ with $w_x = sum_(y in R(x, dot)) d^-_R (y)$,
  $w_x^2 <= a_x alpha'$ and $sum_x t_x^2 = gamma'$, so
  $M_R^2 <= |S| sqrt(|R| alpha' gamma')$; $beta' >= |S|$. Since
  $|R| |T|, |R| |S| <= N^2 \/ 4$, choosing the orientation that realizes
  $B_2^3$ gives $M_R <= (N\/2)^(1\/2) B_2^(3\/4)$, and
  $v^(3\/4)\/(1 + v)$ is maximal at $v = 3$. The sharp family and $"GMR"$
  are instances of $E$ ($"GMR"$: $B_2 = m^4$ exactly).
]

#corollary(name: [a fixed root against $N + B_2$])[
  For every instance and every fixed root, e.g. $x$,
  $C_x <= |R| + M_R <= N + (3^(3\/4) \/ (4 sqrt(2))) N^(1\/4) (N + B_2)$.
  So the worst-case gap of a fixed root against $N + B_2$ lies in
  $[1\/8, 1\/4]$, the lower end from $G_8 (m)$ (@thm-sep(3)).
] <cor-fixedroot>
#st[#proved]

#proof[
  By @lem-sum, $C_x <= sum_x c_R (x) = |R| + M_R$, and @thm-onegao
  bounds $M_R$ for the prescribed driver $R$. Roots $y$ and $z$ use
  drivers $S$ and $T$.
]

#remark(name: "what this does not show")[
  The $G_8$ separation of a fixed root is instance-wise: on $G_8$,
  $C + N asymp N + B_2 asymp m^8$, and the fixed root loses $N^(1\/8)$
  against either. That exponent equals the per-binding worst-case gap
  against $N + B_2$, so it does not show that a fixed root has a worse
  _worst-case_ exponent against $N + B_2$; that exponent lies in
  $[1\/8, 1\/4]$ (@cor-fixedroot). The orders are settled: the best of
  six has gap exactly $1\/5$ (@thm-best6), and one fixed GAO exactly
  $1\/4$ on general inputs and between $1\/5$ and $1\/4$ on
  semijoin-reduced ones (@thm-onegao).
] <rem-notshow>

#proposition(name: "a single predicate")[
  For $P subset.eq V times V$ consider the cyclic self-join
  $P(a, b) and P(b, c) and P(c, a)$, the instance $R = S = T = P$ on
  $X = Y = Z = V$; its input size is $N = 3|P|$.
  + _(tagged embedding)_ Let $(R, S, T)$ be an instance on disjoint
    $X, Y, Z$ and $P = R union S union T$ on $V = X union.sq Y union.sq Z$.
    Then $Out_P = 3 Out$, $N_P = 3N$, all three roots cost
    $C_x + C_y + C_z$, every $M^P_pi = M_R + M_S + M_T$, every forward
    moment of $P$ is $alpha + beta + gamma$ and every reverse moment
    $alpha' + beta' + gamma'$, so
    $B_(2,P) = min(alpha + beta + gamma, alpha' + beta' + gamma')$.
  + _(the lower bounds survive)_ One $G_8 (m)$ embedded this way has
    exactly the values of $cU(m)$: $N = 3(2m^8 + m^7 + m^6 + m^5)$,
    $B_2 = 5m^8$, $C = m^9 + m^8 + m^6 + m^5$; so @thm-pb-lower and the
    exponent $9\/8$ of @cor-l2-false hold for one directed predicate.
    Padding keeps the embedding tagged and pairwise semijoin-reduced.
    $cF_a$ gives $N = 9a^2$, $C = 6a^2$, $Out = 3a^2$ and every GAO
    cost $a^3 + 5a^2$, a $Theta(N^(1\/2))$ loss of every order against
    $C + N$ on a semijoin-reduced instance; $"GMIN"(m)$ gives every GAO
    cost $3m^6 + 3(m^5 + m^4 + m^3)$ against $N + B_2 = 18m^5 + 9m^4 + 9m^3$,
    the gap $1\/5$. The low-slope results do not transfer: every
    directed $P$ has
    $B_(2,P) = min(sum_v d^+_P (v)^2, sum_v d^-_P (v)^2) >= |P| = N_P \/ 3$,
    so no growing single-predicate family has slope below $1$ (e.g.
    $kappa = 19\/20$ is impossible), and only the $9\/8$ case at
    $B_2 asymp N$ and the order separations above are claimed for one
    predicate.
  + _(no fixed-root or fixed-order separation)_ For the cyclic
    self-join, renaming $a -> b -> c -> a$ maps the query to itself, so
    $C_a = C_b = C_c$ and $M_R = M_S = M_T$: a fixed root costs exactly
    $C$, and all six GAOs cost the same. The separations of @thm-sep(3)
    and between one GAO and the best of six cannot occur for this query.
  + _(symmetric predicate)_ If $P = P^top$ (an undirected graph with
    degrees $d$), the two options at every binding walk the same
    neighbours at the same per-edge costs, all six moments equal
    $sum_v d(v)^2 = B_2$, and
    $C = |P| + sum_((u,v) in P) min(d(u), d(v)) <= |P| + B_2 <= N + B_2$.
    The first inequality is an equality for a single undirected edge
    ($|P| = B_2 = 2$, $C = 4$); the relaxation to $N + B_2$ is not
    ($N = 6$). There is no $N^(1\/8)$ gap for undirected
    single-relation triangles.
] <prop-selfjoin>
#st[#proved (exact checks in @app-verify. Parts (1)--(2) were found by two model-based reviews of the second draft, the GPT-6-Astra Pro review and a separate GPT-6 Pro session; parts (3)--(4) by the latter; @sec-ai.)]

#proof[
  (1) Every tuple of $P$ goes $X -> Y$, $Y -> Z$ or $Z -> X$, so a
  directed triangle of $P$ is a triangle of $(R, S, T)$ read from one of
  its three vertices, and $d^+_P, d^-_P$ restrict to the degrees of the
  relation leaving, resp. entering, each part. A binding $a in X$ of the
  self-join has options walking $P(a, dot) = R(a, dot)$ and
  $P(dot, a) = T(dot, a)$, with per-edge costs
  $1 + min(d^+_S (y), d^-_T (a))$ and $1 + min(d^+_R (a), d^-_S (z))$:
  exactly the options of root $x$. Bindings in $Y$ and $Z$ reproduce
  roots $y$ and $z$, so $C^P_a = C_x + C_y + C_z$, and by the symmetry
  in (3) the same holds for roots $b, c$. The $M$ and moment identities
  are the same restriction. (2) Substitute the values of the proof of
  @thm-pb-lower ($C_x + C_y + C_z = m^9 + m^6 + m^5 + m^8$, forward sums
  $m^8 + 2m^8 + 2m^8$, reverse sum $m^12 + 2m^11 + 3m^10 + m^7$), of
  @thm-sep(1) for $cF_a$ ($C_v = 2a^2$, $M = a^3 + 2a^2$, $|P| = 3a^2$)
  and of @thm-sep(2) for $"GMIN"$. Padding adds tagged triangles, and a
  vertex of the padded $P$ has an in- and an out-tuple, which is
  pairwise reduction for the self-join. (3) The renaming permutes the
  three atoms, the three roots, and the three drivers. (4) A binding
  $v$ walks $P(v, dot) = P(dot, v)$ in both options with per-edge cost
  $1 + min(d(v), d(u))$; summing,
  $C = |P| + sum_((v,u) in P) min(d(v), d(u)) <= |P| + sum_((v,u) in P) d(v) = |P| + sum_v d(v)^2$.
]

The tagged union of padded $G_8 (m)$ has three components in the
role-expanded instance (one per rotation), so a per-component root
choice could escape it; adding one tuple $x_0 -> x_1$ between two
vertices of $X$ makes it connected. For $m = 2, 3$ the result is
pairwise semijoin-reduced and connected, with
$(N, C, B_2, Out) = (6891, 4277, 3873, 1560)$ and
$(167187, 112924, 98515, 39447)$ (computed exactly,
`artifacts/hillclimb/checks/selfjoin_connected.py`), and the extra tuple
changes the squared sums by $O(m^4)$, so the exponent stays $9\/8$.
What remains open for self-joins is the case of two edges sharing a
predicate, where renaming the variables is not a symmetry.

== Sorted intersections <sec-sorted>

The lower bounds above charge the shorter run (@sec-prelim). An engine
that stores sorted runs intersects them by comparisons, leapfrog or
galloping, and can be much cheaper when identifiers are contiguous. We
now let the adversary choose the identifiers and charge comparisons.
Every lower bound against $N + B_2$ survives without logarithmic loss,
as do the fixed-root and padded-$"GMIN"$ bounds against $C + N$ (the
other $Theta(N^(1\/2))$ losses against $C + N$ are established only up
to a factor $log N$, @rem-sorted-cheap); the upper bound of @thm-pb-upper survives up to a factor
$(log N)^(1\/4)$, and that factor is necessary. The single-intersection
ingredients are classical: comparison certificates and alternation
lower bounds for sorted-set intersection
[#cite(<ref-dlm>)[DLM00], #cite(<ref-bk>)[BK02], #cite(<ref-bk08>)[BK08]],
including randomized lower bounds [#cite(<ref-bk>)[BK02]], and doubling
(galloping) search [#cite(<ref-by>)[BY76]]. What is new here is their
simultaneous realization, under one global labeling, inside the join
constructions of the previous subsections, and the resulting
quarter-logarithm tradeoff for per-binding choice.

#definition(name: "sorted fresh-call comparison model")[
  An intersection call receives two strictly increasing runs of opaque
  keys and their lengths. It may compare any two keys (three-way or
  Boolean predicates) and do index arithmetic; key arithmetic, hashing
  and addressing by key value are unavailable. Every key comparison
  costs one unit; a plan is additionally charged one unit per visited
  outer tuple. A call is _fresh_: it knows the internal order of its two
  runs and nothing else (no comparison results, certificates, aliases or
  rank hints from other calls). The routine $A$ is fixed before the
  adversary assigns term identifiers (one global total order on each of
  $X, Y, Z$); the root and the per-binding option may be chosen with
  full knowledge of the labeling. $Q_A$ is the minimum, over roots and
  per-binding options, of the resulting cost (comparisons plus outer
  visits) of a correct run of $A$. For a zero-error randomized routine,
  every call draws its own random tape, $Q_A$ is the same minimum for
  the realized tapes (so the plan may be chosen after seeing them), and
  we bound $E[Q_A]$, the expectation of this realized minimum; this is
  at most the minimum over plans of their expected costs.
] <def-sorted>

Relabelling permutes rows and columns of $A_R, A_S, A_T$, so sizes,
degrees, singular values, $N$, $B_2$, $U$ and $Out$ are unchanged:
nothing in @sec-main or @sec-kernel depends on the labeling.

#lemma(name: "comparison certificate")[
  Let $A, B$ be disjoint strictly increasing runs and $t(A, B)$ the
  number of adjacent pairs of their merged order whose members lie in
  different runs. Every correct fresh intersection routine makes at
  least $t(A, B)$ key comparisons on $(A, B)$. If the runs alternate,
  $a_0 < b_0 < dots < a_(s-1) < b_(s-1)$, then $t = 2s - 1$, and ternary
  merge makes exactly $2s - 1$ comparisons.
] <lem-cert>
#st[#proved (the classical certificate argument of
[#cite(<ref-dlm>)[DLM00], #cite(<ref-bk>)[BK02]], stated in our model)]

#proof[
  If an adjacent opposite-run pair is never compared, identify its two
  keys. Both runs stay strictly increasing (the keys lie in different
  runs), no key lies between them, so every other comparison has the same
  outcome, and the routine answers as before; but the intersection is
  now nonempty.
]

#lemma(name: "one order for all rows")[
  For $A = {a_k : k < s}$ and pairwise disjoint private sets
  $B_h = {b_(h,k) : k < s}$, the single order
  $a_k, b_(0,k), b_(1,k), dots$ for $k = 0, dots, s - 1$ restricts to a
  perfect alternation on $A union B_h$ for every $h$. Orders on disjoint
  term domains, and on vertex-disjoint components, concatenate to one
  global order.
] <lem-interleave>
#st[#proved]

#theorem(name: [the $9\/8$ lower bound in the sorted model])[
  Realize $G_8 (m)$ with $X = {(g, h) : g < m^3, h < m}$,
  $Z_2 = {(g, t) : g < m^3, t < m^3}$, $T$ complete between
  $Z_(2,g) = {(g, t)}$ and $X_g = {(g, h)}$ for each $g$, $m^4$ private
  $Z_0$-predecessors per $x$, a private $S$-predecessor set $Y_(2,z)$ of
  size $m^2$ for each $z in Z_2$, $R = X times Y_0$ and
  $S supset.eq Y_0 times Z_1$ (degrees exactly as in @tab-g8). Order $Z$
  as: for $t < m^3$, $Z_1 [t], Z_2 [0, t], dots, Z_2 [m^3 - 1, t]$; then
  all of $Z_0$. Order $Y$ as: for $k < m^2$, $Y_0 [k]$, then
  $Y_(2,z) [k]$ for every $z in Z_2$. Then, simultaneously for all $x$
  and $z$, every call $(Z_1, T(dot, x))$ needs at least $2m^3 - 1$
  comparisons and every call $(Y_0, Y_(2,z))$ at least $2m^2 - 1$. For
  every eligible routine $A$ and every $x$, option $R$ costs at least
  $2m^5$ and option $T$ at least $m^4 + 2m^5$, with equality for ternary
  merge; the other roots of $G_8$ cost $m^5$ and $m^8$. On $cU(m)$ every
  root has exact optimal ternary cost $2m^9 + m^8 + m^5$, a lower bound
  on $Q_A$ for every $A$; with $N = 3(2m^8 + m^7 + m^6 + m^5)$ and
  $B_2 = 5m^8$,
  $
    Q_A \/ (N + B_2) >= m\/7 >= (N\/9)^(1\/8) \/ 7.
  $
  So no $c$, and no $c = O(log^k N)$, satisfies $Q_A <= c(N + B_2)$ for
  comparison-based sorted intersection (plain merge, leapfrog, galloping
  with any step schedule) under an adversarial identifier assignment.
  Padding (@lem-pad) with all fresh keys placed before all original keys
  keeps every hard run and its certificate, so the
  $Omega(N^(1\/8))$ gap holds on pairwise semijoin-reduced inputs with
  $Theta(N)$ triangles.
] <thm-sorted-g8>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  On $Z_1 union T(dot, x)$, with $x in X_g$, the order restricts to
  $Z_1 [0], Z_2 [g, 0], Z_1 [1], Z_2 [g, 1], dots$ followed by the
  private $Z_0$-keys of $x$, which lie in the same run as their
  predecessor: $t = 2m^3 - 1$ (@lem-cert). On $Y_0 union Y_(2,z)$ the
  order alternates by @lem-interleave: $t = 2m^2 - 1$. Option $R$ at $x$
  makes $m^2$ calls $(Z_1, T(dot, x))$ and visits $m^2$ outer tuples:
  $m^2 (1 + 2m^3 - 1) = 2m^5$. Option $T$ visits $m^4$ tuples into $Z_0$
  (empty $S$-run, no comparison) and makes $m^3$ calls
  $(Y_0, Y_(2,z))$: $m^4 + m^3 (1 + 2m^2 - 1)$. At roots $y$ and $z$
  the cheap options of the proof of @thm-pb-lower meet empty runs, at
  cost one per visited tuple. In $cU(m)$ every root contains one copy of
  root $x$ of $G_8$, so it costs at least $m^4 dot 2m^5$, plus $m^5 + m^8$
  from the other copies. $N + B_2 <= 14 m^8$ for $m >= 2$. For padding,
  the padded vertices are $Y_2$, $Z_0$ and $Z_1$ (each has tuples in
  only one relation); $X$, $Y_0$, $Z_2$ are not padded, and every new
  tuple touches a fresh vertex, so the runs $Z_1$, $T(dot, x)$,
  $R(x, dot) = Y_0$ and $S(dot, z) = Y_(2,z)$ of original vertices are
  unchanged; the critical root still costs at least $2m^9$, while
  $N' <= 7N$ and $B'_2 = O(m^8)$ (@lem-pad).
]

#theorem(name: [slopes, separations and fixed roots in the sorted model])[
  + _(slopes)_ Fix $i >= j >= 1$, $u >= 2$, and put $n = u^(4i)$,
    $a = u^(4i - 2j)$, $b = u^(4i - j)$, $d = u^(4i - 3j)$, $H = u^(3j)$.
    Partition $X$ into $H$ groups of size $d$ and $Z_2$ into $H$ groups
    of size $b$, make the paired $T$-blocks complete, give every
    $z in Z_2$ a private $a$-element $S$-predecessor set, and order by
    @lem-interleave ($Z_1$ against every $Z_2$ group, $Y_0$ against
    every $Y_(2,z)$). Both options at every $x$ cost exactly $2 a b$ for
    ternary merge and at least $2 a b$ for every eligible routine; the
    union of three rotations has exact optimal cost
    $Q = 2u^(12i - 3j) + u^(8i) + u^(8i - 3j)$,
    $N = 3(u^(8i) + u^(8i - j) + u^(8i - 2j) + u^(8i - 3j))$ and
    $B_2 = 3u^(12i - 4j) + u^(8i)$, so
    $Q = Theta(N^(3\/8) B_2^(3\/4))$ at $B_2 = Theta(N^kappa)$,
    $kappa = 3\/2 - j\/(2i)$, with no logarithmic factor.
  + _(fixed GAOs)_ In $cF_a$ with $z_(i,k)$ ordered by $(k, i)$ every
    off-diagonal $R$-tuple $(x_i, y_j)$ is an alternating pair of
    length-$a$ runs, so the $R$-driven GAOs need $a(a - 1)(2a - 1)$
    comparisons in total, with $N = 3a^2$, $B_2 = a^(8\/3)$: loss
    $Theta(N^(1\/6))$ against $N + B_2$ on a pairwise semijoin-reduced
    instance. In $"GMR"(m)$ with the common $Z_1$ layered against every
    private $T$-predecessor set, all $m^4$ $R$-tuples need $2m - 1$:
    loss $Theta(N^(1\/4))$. In $"GMIN"(m)$ with the three layerings
    ($Z_1$ against the $Z_0$-fibres, $X_2$ against the $X_1$-fibres,
    $Y_2$ against the $Y_3$-fibres; disjoint domains, one order) each
    driver has $m^4$ hard tuples of $2m^2 - 1$ comparisons and every
    other tuple meets an empty run: the best of the six GAOs loses
    $Theta(N^(1\/5))$ against $N + B_2$ and against adaptive execution
    plus $N$. Padded with fresh keys first, $"GMIN"$ has
    $N' = 12m^5 + 3m^4 + 3m^3 + 9m^2$, $B'_2 = 8m^5 + 3m^2$,
    $Out' = 3m^5 + 3m^2$, unchanged hard tuples, and cheap options that
    are $O(1)$-comparison searches for a fresh key placed before all
    original keys; so adaptive execution costs $Theta(N')$ while every
    GAO costs $Theta(m^6)$.
  + _(fixed root)_ In $cH_a$ with $Y_1, Y_2$ alternated and the common
    $Z_2$ layered against every private $Z_1$-fibre, each option at
    every $x$ makes $a$ alternating calls on length-$a$ runs, aggregate
    certificate $a^2 (2a - 1)$; a fixed root $x$ costs $Theta(a^3)$ and
    root $y$ costs $Theta(a^2)$, and fresh-first padding leaves the
    certificates of the original $X$ unchanged: the $Theta(N^(1\/2))$
    loss of a fixed root against adaptive cost plus $N$ holds on
    semijoin-reduced inputs.
  All lower bounds hold for every eligible routine; merge attains them.
] <thm-sorted-sep>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  Each item applies @lem-cert to the stated alternations, which
  @lem-interleave realizes in one global order (the three rotated
  copies, and the three layerings of $"GMIN"$, live on disjoint
  domains). In (1), option $R$ at $x$ makes $a$ calls of $2b - 1$
  comparisons plus $a$ visits and option $T$ makes $b$ calls of $2a - 1$
  plus $b$ visits, both $2a b$; roots $y$ and $z$ cost $a b$ and
  $u^(8i)$ (empty runs), and the statistics are those of the proof of
  @cor-real-slopes. In (2), the counts are $a(a - 1)$ tuples times
  $2a - 1$, $m^4 (2m - 1)$ and $m^4 (2m^2 - 1)$; the statistics of
  $"GMR"$ and $"GMIN"$ are those of @thm-sep. A fresh key placed before
  all original keys is found or excluded by galloping with $O(1)$
  comparisons. In (3), option $R$ at $x$ walks $Y_1$ and intersects the
  private fibre $S(y_i, dot)$ with the common $T(dot, x) = Z_2$, and
  option $T$ walks $Z_2$ and intersects $R(x, dot) = Y_1$ with
  $S(dot, z') = Y_2$.
]

#remark(name: [the $Theta(N^(1\/2))$ ratios against $C$])[
  In $cF_a$ and $cG_a$ the cheap options are singleton membership tests
  in length-$a$ runs; a fresh singleton search costs up to
  $ceil(log_2 (a + 1))$ comparisons while its certificate is $1$ or
  $2$. So in the sorted model the $Theta(N^(1\/2))$ loss of
  @thm-sep(1)--(2) against $C + N$ is established only between
  $Omega(N^(1\/2) \/ log N)$ and $O(N^(1\/2))$; the ratios against
  $N + B_2$ in @thm-sorted-sep are unaffected.
] <rem-sorted-cheap>

*Upper bound.* For runs of lengths $p, q$ put $s = min(p, q)$,
$l = max(p, q)$ and the _price_
$h(p, q) = s (1 + ceil(log_2 (l\/s)))$, with $h = 0$ if a run is empty,
and $L_N = 1 + ceil(log_2 N)$. Doubling galloping (walk the shorter run,
gallop from the current position in the longer one) intersects the two
runs with $O(h(p, q))$ comparisons. $h$ is computable from the two
degrees: $ceil(log_2 (l\/s)) = "bitlength"(floor((l - 1)\/s))$.

#lemma(name: "galloping and the AGM cap")[
  $h(p, q) <= L_N dot s$ when $l <= N$, and
  $h(p, q) <= sqrt(9 p q \/ 2) < 3 sqrt(p q)$; below we use the round
  constant $3$. Consequently
  $sum_((x,y) in R) h(d^+_S (y), d^-_T (x)) <= 3 opn(A_R) sqrt(|S| |T|) <= 3 sqrt(|R| |S| |T|)$:
  the fixed-driver galloping kernel costs
  $O(N + opn(A_R) sqrt(|S| |T|))$ comparisons, and
  $C <= N + sqrt(|R| |S| |T|)$ of @lem-sum survives galloping with
  constant $3$ and no logarithm.
] <lem-sorted-agm>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  The first bound is $ceil(log_2 (l\/s)) <= ceil(log_2 N)$. For the
  second, if $l = s$ then $h = s = sqrt(p q)$; otherwise put $r = l\/s > 1$
  and $k = ceil(log_2 r) >= 1$, so $r > 2^(k-1)$ and
  $h^2 \/ (p q) = (k + 1)^2 \/ r < (k + 1)^2 \/ 2^(k - 1) <= 9\/2$: the
  values are $4, 9\/2, 4$ at $k = 1, 2, 3$, and they decrease from
  $k = 2$ on because $(k + 2)^2 <= 2(k + 1)^2$ for $k >= 2$. Then
  $sum h <= 3 sum_((x,y) in R) sqrt(d^-_T (x)) sqrt(d^+_S (y)) <= 3 opn(A_R) sqrt(|T| |S|)$
  as in the proof of @prop-kernel.
]

#theorem(name: [sorted-model analogue of @thm-pb-upper])[
  Let $hat(C)$ be the per-binding cost in which every edge is priced
  $1 + h(dot, dot)$ instead of $1 + min(dot, dot)$ (same roots, options
  and minimum). Then
  $
    hat(C) <= N + 3^(3\/4) L_N^(1\/4) (|R| |S| |T|)^(1\/8) min(Lambda, Lambda')^(1\/2)
           <= N + 3^(3\/4) L_N^(1\/4) (N\/3)^(3\/8) B_2^(3\/4).
  $
  The prices are computable from degrees in $O(N)$ reads; selecting the
  best priced root and options and executing by galloping costs
  $O(hat(C))$ comparisons. Hence the sorted-model per-binding cost is
  $O(N + (log N)^(1\/4) (|R| |S| |T|)^(1\/8) min(Lambda, Lambda')^(1\/2))$.
  The price-then-run scheduler of @prop-ptr runs unchanged with the
  prices $1 + h$, so (1)--(3) of @prop-ptr hold with $C$ replaced by
  $hat(C)$, in per-edge price units, without sampling.
] <thm-sorted-upper>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  At root $x$ put $a = d^+_R (x)$, $b = d^-_T (x)$,
  $hat(P)(x) = sum_(y in R(x, dot)) h(d^+_S (y), b)$,
  $hat(Q)(x) = sum_(z : (z,x) in T) h(a, d^-_S (z))$ and
  $w(x) = sum_(z : (z,x) in T) sqrt(d^-_S (z))$. By @lem-sorted-agm,
  $hat(P)(x) <= L_N sum_y d^+_S (y) <= L_N sqrt(a beta)$ and
  $hat(Q)(x) <= 3 sqrt(a) w(x)$, so
  $min(hat(P), hat(Q)) <= hat(P)^(1\/4) hat(Q)^(3\/4) <= 3^(3\/4) L_N^(1\/4) beta^(1\/8) a^(1\/2) w(x)^(3\/4)$,
  and steps 4--5 of the proof of @lem-perroot give
  $hat(C)_x <= |R| + |T| + 3^(3\/4) L_N^(1\/4) alpha^(1\/4) beta^(1\/8) (gamma |S|)^(3\/8)$.
  Rotation and reflection give the other roots and the primed forms, and
  the proof of @thm-pb-upper (geometric mean of the nonnegative bounds)
  gives the claim. Lockstep pricing (@lem-lockstep) needs only per-edge
  prices of at least $1$ revealed one at a time.
]

#corollary(name: [sorted-model analogue of @thm-pb-upper2])[
  For every instance with $N > 0$,
  $hat(C) <= N + 3^(7\/8) L_N^(1\/4) N^(-1\/8) B_2^(5\/4)$; in integers,
  $N^3 (hat(C) - N)_+^24 <= 3^21 L_N^6 min(alpha beta gamma, alpha' beta' gamma')^10$.
] <cor-sorted-upper2>
#st[#proved]

#proof[
  The proof of @thm-sorted-upper bounds the priced minima at each root
  by $3^(3\/4) L_N^(1\/4)$ times the multiplicative terms of
  @lem-perroot. Repeating the proof of @thm-pb-upper2 with these bounds
  multiplies its conclusion by $3^(3\/4) L_N^(1\/4)$:
  $hat(C) - N <= 3^(3\/4) L_N^(1\/4) B_2^(5\/4) (N\/3)^(-1\/8)$, and the
  24th power is the integer form.
]

Whether the factor $L_N^(1\/4)$ is needed below slope $1$ is open
(@sec-open).

#lemma(name: "decision trees on disjoint runs")[
  Fix a correct deterministic fresh-call routine and disjoint runs of
  lengths $p, q$, and refine its comparison tree by replacing every
  Boolean comparison with the three-way comparison of the same two keys
  (the routine ignores the extra information, so every comparison count
  is unchanged). A leaf of the _refined_ tree that answers "disjoint" is
  reached by at most one of the $binom(p + q, p)$ shuffles of the two
  runs. Hence fewer than $2^D$ shuffles are decided with fewer than $D$
  comparisons.
] <lem-decision>
#st[#proved]

#proof[
  At a refined leaf, if the partial order generated by the three-way
  outcomes and the two internal orders is not total, some opposite-run
  pair is incomparable, and the input that makes those two keys equal
  is consistent with every outcome on the path, so it reaches the same
  leaf with a nonempty intersection; hence the leaf determines the
  merged order. On disjoint inputs every three-way comparison has two
  possible outcomes, so fewer than $2^D$ refined leaves lie at depth
  below $D$. The refinement is needed: in the _unrefined_ Boolean tree
  the routine "test $a = b$; output $a$ if true" on singletons reaches
  its "false" leaf from both shuffles $a < b$ and $b < a$.
]

#theorem(name: "the quarter logarithm is necessary")[
  Fix $i >= j >= 1$ and an integer $e >= 1$; put $M = 2^e$, $L = M^4$,
  $u = 2^L$, and
  $n = |X| = u^(4i) \/ M^4$, $a = |Y_0| = u^(4i - 2j) M^2$,
  $p = |Z_1| = u^(4i - j) \/ M$, $q = u^(4i) M^4$, $k = p L$,
  $d = u^(4i - 3j) M$, $c = |Z_2| = u^(4i + 2j) \/ M^2$ (all integers;
  $n\/d = c\/k = u^(3j)\/M^5$). Take $R = X times Y_0$,
  $S supset.eq Y_0 times Z_1$, a private $a$-element $S$-predecessor set
  $Y_(2,z)$ for every $z in Z_2$, complete $T$-blocks pairing $d$
  vertices of $X$ with $k$ vertices of $Z_2$, and $q$ private dead
  $Z_0$-predecessors for every $x$ (so $c a = n q = u^(8i)$, $c d = n k$,
  no triangles). For the union of three rotations,
  $N = 3(2u^(8i) + u^(8i - j)\/M + u^(8i - 2j)\/M^2 + u^(8i - 3j) M) in [6u^(8i), 15u^(8i)]$,
  each forward squared-degree sum is $3u^(12i - 4j) + 2u^(8i)$ and each
  reverse sum exceeds it, so
  $B_2 = 3u^(12i - 4j) + 2u^(8i) in [3u^(12i - 4j), 5u^(12i - 4j)]$.
  For every eligible deterministic routine $A$ there is one global
  labeling $ell_A$ with
  $
    Q_A >= n a D = (M\/2) u^(12i - 3j), quad D = p L \/ 2.
  $
  Since $M = (log_2 u)^(1\/4) = Theta((log N)^(1\/4))$ and
  $N^(3\/8) B_2^(3\/4) = Theta(u^(12i - 3j))$, this matches
  @thm-sorted-upper up to a constant on every slope
  $kappa = 3\/2 - j\/(2i) in [1, 3\/2)$. At $i = j$, $B_2 = Theta(N)$ and
  $sup_ell Q_A = Omega(N^(9\/8) (log N)^(1\/4))$, so the worst-case
  sorted-model scale at $B_2 asymp N$ is
  $Theta(N^(9\/8) (log N)^(1\/4))$. For a zero-error randomized routine
  there is likewise one labeling on which the expected _realized_
  minimum over plans (@def-sorted) satisfies
  $E[Q_A] >= n a D \/ 2 = (M\/4) u^(12i - 3j)$; a fortiori every plan's
  expected cost is at least this.
  No universal constant gives
  $Q_A <= c(N + (|R| |S| |T|)^(1\/8) min(Lambda, Lambda')^(1\/2))$ in the
  sorted model; the ratio grows as $(log N)^(1\/4)$.
] <thm-quarterlog>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  _Labeling._ Order $Y$ by @lem-interleave so that $Y_0$ alternates with
  every $Y_(2,z)$; order $Z$ as $Z_1 union Z_0$ first and $Z_2$ last, the
  dead keys of each $x$ shuffled into the $p + 1$ gaps of $Z_1$: in each
  gap, concatenate the keys assigned to it in a fixed order of $x$, so
  that independent shuffles for all $x$ are realized by one order. The
  rotated copies use disjoint domains.
  _Option $T$._ At every $x$ it makes $k$ calls $(Y_0, Y_(2,z))$ with
  $2a - 1$ comparisons each (@lem-cert): at least $k a = 2 a D$.
  _Option $R$._ At $x$ it makes $a$ calls $(Z_1, T(dot, x))$; the $Z_2$
  part of $T(dot, x)$ lies after $Z_1$, and the hard part is the shuffle
  of the $q$ dead keys with $Z_1$. There are
  $binom(p + q, p) >= (q\/p)^p = (u^j M^5)^p >= u^p = 2^(p L)$ shuffles,
  so by @lem-decision a uniform shuffle makes a prescribed call cost less
  than $D$ with probability at most $2^D \/ 2^(p L) = 2^(-p L\/2)$. There
  are $3 n a$ critical $R$-calls in the union and
  $log_2 (3 n a) < 2 + 8 i L < 16 i L <= D$ (as $p >= u^(2i) >= 32 i$),
  so the union bound leaves a labeling, i.e. a choice of shuffles, on
  which every critical $R$-call costs at least $D$.
  _Total._ Every root of the union contains a critical copy, where both
  options cost at least $a D$ per $x$: $Q_A >= n a D$.
  _Randomized routines._ Fix random tapes for all $3 n a$ critical
  $R$-calls at once, and let $E$ be the event that at least one of them
  costs less than $D$. Each tape makes the routine deterministic, so
  for a uniform shuffle $omega$ and independent tapes,
  $Pr_(omega, "tapes") [E] <= 3 n a dot 2^(-p L\/2) < 1\/2$, since
  $log_2 (6 n a) < 3 + 8 i L < 16 i L <= D$. Hence some labeling has
  $Pr_"tapes" [E] < 1\/2$. Outside $E$ every critical call costs at
  least $D$, so every root and every choice of options, even one made
  after seeing the tapes, costs at least $n a D$; therefore
  $E[Q_A] >= n a D \/ 2$. (Bounding each plan's expected cost
  separately would not suffice: two plans with costs $(0, 2)$ and
  $(2, 0)$ under two equally likely tapes both have expectation $1$,
  while their realized minimum is $0$.)
  _Statistics._ Per gadget $|R| = u^(8i - 2j)\/M^2$,
  $|S| = u^(8i - 3j) M + u^(8i)$, $|T| = u^(8i - j)\/M + u^(8i)$, the
  forward sums are $u^(12i - 4j)$, $u^(12i - 4j) + u^(8i)$,
  $u^(12i - 4j) + u^(8i)$, and the reverse sums are
  $u^(12i - 2j)\/M^6$, $u^(12i - 5j) M^3 + u^(12i - 2j) M^2$ and
  $u^(12i) M^4 + 2u^(12i - j) M^3 + u^(12i - 2j) M^2$; in the union
  each reverse moment contains $u^(12i) M^4$, which exceeds the forward
  moment $3u^(12i - 4j) + 2u^(8i)$.
]

The quantifiers are "for every routine there is a labeling"; a single
labeling hard for all routines cannot exist. The explicitly interleaved
$G_8$ and $F_(i,j)$ have no logarithmic overhead (@thm-sorted-g8,
@thm-sorted-sep); the quarter logarithm appears only in the worst case
over labelings against a fixed routine. At the smallest member with
$e = 4$ ($i = j = 1$) the integer form of @thm-pb-upper,
$(C - N)_+^8 <= |R| |S| |T| min(alpha beta gamma, alpha' beta' gamma')^2$,
already fails for $Q_A$: with $N = 3(2^524289 + 2^458748 + 2^393208 + 2^327684)$,
$B_2 = 5 dot 2^524288$ and $Q_A >= Q_0 = 2^589827$, the quotient
$(Q_0 - N)^8 \/ ((N\/3)^3 B_2^6)$ has integer floor $134$: it equals
$(2097152\/15625) (1 - delta)^8 \/ (1 + epsilon)^3$ with
$delta = N\/Q_0 < 2\/u$ and $epsilon < 1\/u$, $u = 2^65536$, so it lies
strictly between $2096544\/15625 > 134$ and $2097152\/15625 < 135$ (no
instance is materialized). The parameters form a doubly exponential
sequence; at $i = j = 1$ one may instead take $u = 2^t$ for every
integer $t$ with $M^4 <= t < 16 M^4$, keeping $L = M^4$, since the
shuffle entropy is then at least $p t >= p L$; consecutive $t$ give
sizes within a constant factor, and isolated edges fill intermediate
sizes with $B_2 = Theta(N)$, so the bound holds for all large $N$, not
only along a sparse sequence (an observation of the GPT-6-Astra Pro
review of the third draft, @sec-ai).


#remark(name: "scope: fresh calls")[
  The lower bounds are for fresh calls. In unpadded $G_8$ one semijoin
  pass ($Z_1$ has no $T$-tuples, so $Y_0 times Z_1$ and then
  $X times Y_0$ are deleted) leaves only cheap structure, and all
  $d^+_R (x)$ calls at a binding $x$ are the identical pair
  $(Z_1, T(dot, x))$, so memoizing calls reduces the critical root to
  $m^4$ distinct calls. Both are outside the model, and @prop-ferrers
  shows that degree metadata can determine an instance. So these are not
  lower bounds for unrestricted comparison-based join algorithms;
  algorithms that reuse certificates across calls, and algorithms using
  different orders on value ranges (ADOPT), remain open (@sec-open).
] <rem-sorted-scope>

// =====================================================================
= Spectral worst-case output bounds <sec-main>
// =====================================================================

This section and the next treat the statistics $(r, sigma)$ of sizes
and operator norms, the level at which per-instance rotation suffices.
The upper bound below is textbook: its Hölder terms are the
$(infinity, 2, 2)$ case of the Schatten--Hölder inequality, and its
degree terms are the degree bounds of [#cite(<ref-anos>)[ANOS24]] with
maximum degrees bounded by $sigma^2$. The content of @thm-main is its
first sentence: the nine terms of $U$ are exactly the norm-feasibility
conditions of one family of block instances, so that one family
witnesses the lower bound in every regime. Its use for planning is
@cor-kernel: the best rotation of the kernel does work at most $U$.
@sec-cycle4 extends the characterization to the labeled 4-cycle, where
complete blocks no longer suffice.

#theorem(name: "spectral AGM for the triangle")[
  Let $(r, sigma)$ be regular. The nine terms of $U$ are exactly the
  norm-feasibility conditions of one block family: for $V > 0$, the
  real block shape
  $(max(1, V\/r_S), max(1, V\/r_T), max(1, V\/r_R))$ of @sec-lower
  satisfies the three norm constraints if and only if $V <= U$, and at
  $V = U$ its relaxed value, with real parameters and no floors, is
  exactly $U$. Flooring this shape loses less than a factor $4$:
  $
    U(r, sigma) \/ 4 < W(r, sigma) <= U(r, sigma).
  $
  The upper bound holds for every admissible instance with constant
  $1$. The lower bound is witnessed by the block instance
  $Blk(a,b,c,m)$ with
  $
    a = floor(max(1, U\/r_S)), quad b = floor(max(1, U\/r_T)), quad
    c = floor(max(1, U\/r_R)), \
    m = floor(min(r_R\/(a b), r_S\/(b c), r_T\/(c a))).
  $
] <thm-main>
#st[#provedlean (@sec-mech. The feasibility statement for $V != U$ (feasible for $V < U$, infeasible for $V > U$) is on paper only; it is immediate from the identity in the proof of @lem-feasible. The factor $4$ is best possible, @thm-sharp.)]

== Upper bound

#lemma(name: [degree at most $sigma^2$])[
  For any 0/1 matrix $A$, every row and column degree is at most
  $opn(A)^2$ and at most the number of ones of $A$.
] <lem-deg>
#st[#provedlean (`rowDeg_le_opNorm_sq`, `colDeg_le_opNorm_sq`.)]

#proof[
  For row $x$, $opn(A^top e_x)^2 = deg(x)$ and
  $opn(A^top e_x) <= opn(A^top) = opn(A)$. Columns are symmetric. The
  second bound is trivial.
]

#proof(of: [the upper bound of @thm-main])[
  Fix an admissible instance; by @lem-deg and clipping every degree of
  relation $i$ is at most $s_i$.

  _Degree terms._ Counting by $R$-tuples,
  $Out = sum_((x,y) in R) |S(y, dot) inter T(dot, x)|$, and each summand
  is at most $min(d^+_S (y), d^-_T (x)) <= min(s_S, s_T)$. Hence
  $Out <= D_(R,S)$ and $Out <= D_(R,T)$. Counting by $S$- and $T$-tuples
  gives the other four.

  _Hölder terms._ For $z in Z$ let $t_z in RR^X$,
  $t_z (x) = [(z,x) in T]$, and $u_z in RR^Y$, $u_z (y) = [(y,z) in S]$.
  Then
  $
    Out = sum_z chevron.l t_z, A_R u_z chevron.r
      <= opn(A_R) sum_z norm(t_z) norm(u_z)
      <= opn(A_R) (sum_z norm(t_z)^2)^(1\/2) (sum_z norm(u_z)^2)^(1\/2)
      = opn(A_R) sqrt(|T| |S|),
  $
  by $|chevron.l t, A u chevron.r| <= opn(A) norm(t) norm(u)$ and
  Cauchy--Schwarz. Since also $opn(A_R) <= sqrt(|R|)$, this is at most
  $H_R$. Equivalently, by trace duality,
  $tr(A_R dot A_S A_T) <= opn(A_R) norm(A_S A_T)_(S_1) <= opn(A_R) norm(A_S)_F norm(A_T)_F$.
  $H_S$ and $H_T$ follow by rotation.#footnote[A tempting nuclear-norm
  shortcut, $norm(A)_* <= |A| \/ opn(A)$, is false: for
  $A = mat(1, 1; 1, 0)$, $norm(A)_* = sqrt(5) approx 2.236$ while
  $|A| \/ opn(A) = 3\/phi approx 1.854$; the reverse inequality
  $|A| = norm(A)_F^2 <= opn(A) norm(A)_*$ always holds. The valid bound
  $Out <= sigma_R sigma_S norm(A_T)_* <= sigma_R sigma_S r_T$ is
  dominated by $D_(T,R)$ or $D_(T,S)$, since
  $min(s_R, s_S) <= sigma_R sigma_S$.]
]

== Lower bound: one block family for every regime <sec-lower>

*Block instance.* For integers $a,b,c,m >= 1$, $Blk(a,b,c,m)$ consists
of $m$ vertex-disjoint blocks, each with $a$ $x$'s, $b$ $y$'s, $c$ $z$'s
and all three bipartite pieces complete: $A_R = I_m times.o J_(a times b)$
and likewise for $S, T$. Then
$
  |R| = m a b, quad |S| = m b c, quad |T| = m c a, quad
  opn(A_R)^2 = a b, quad opn(A_S)^2 = b c, quad opn(A_T)^2 = c a, quad
  Out = m a b c.
$
(Lean: `card_blk`, `opNorm_blk_eq`, `out_blk`; feasibility needs only
"$<=$", which the Schur test $opn(A)^2 <= Delta_"row" Delta_"col"$ gives,
`opNorm_adj_le_schur`.) So $Blk$ is admissible iff $a b <= s_R$,
$b c <= s_S$, $c a <= s_T$ and $m <= min(r_R\/(a b), r_S\/(b c), r_T\/(c a))$.

#lemma(name: "the real shape is feasible")[
  Let $hat(a) = max(1, U\/r_S)$, $hat(b) = max(1, U\/r_T)$,
  $hat(c) = max(1, U\/r_R)$. Then $hat(a) hat(b) <= s_R$,
  $hat(b) hat(c) <= s_S$, $hat(c) hat(a) <= s_T$.
] <lem-feasible>
#st[#provedlean (`Stats.real_shape_feasible`.)]

#proof[
  For $p, q > 0$, $max(1,p) max(1,q) = max(1, p, q, p q)$. So
  $hat(a) hat(b) = max(1, U\/r_S, U\/r_T, U^2\/(r_S r_T))$, and each entry
  is at most $s_R$: $1 <= s_R$ by regularity; $U <= D_(S,R) = r_S s_R$;
  $U <= D_(T,R) = r_T s_R$; $U^2 <= H_R^2 = s_R r_S r_T$. Rotating the
  labels, $hat(b) hat(c) <= s_S$ uses $1, D_(T,S), D_(R,S), H_S$ and
  $hat(c) hat(a) <= s_T$ uses $1, D_(R,T), D_(S,T), H_T$. With any
  $V > 0$ in place of $U$ the same identity shows that the shape is
  feasible iff $V$ is at most each of the nine terms, i.e. iff
  $V <= U$.
]

Thus each of the nine terms is exactly one feasibility condition of the
minimal block shape; this is why $U$ is the answer (@thm-main, first
sentence).

#lemma(name: [the relaxed value is $U$])[
  With $m^* = min(r_R\/(hat(a) hat(b)), r_S\/(hat(b) hat(c)), r_T\/(hat(c) hat(a)))$
  we have $m^* >= 1$ and $m^* hat(a) hat(b) hat(c) = U$.
] <lem-value>
#st[#provedlean (`Stats.real_shape_value`, `Stats.real_shape_attains_U`.)]

#proof[
  $m^* >= 1$ because $hat(a) hat(b) <= s_R <= r_R$ and similarly. Next,
  $m^* hat(a) hat(b) hat(c) = min(hat(c) r_R, hat(a) r_S, hat(b) r_T)
  = min_j max(r_j, U)$. This equals $U$ because $U >= min_j r_j$: each
  $D_(i,j) >= r_i$ (as $s_j >= 1$) and
  $H_R >= sqrt(r_S r_T) >= min(r_S, r_T)$, and similarly for $H_S, H_T$.
]

#proof(of: [the lower bound of @thm-main])[
  Put $a = floor(hat(a))$, $b = floor(hat(b))$, $c = floor(hat(c))$, all
  $>= 1$. Flooring shrinks products, so $a b <= s_R$, $b c <= s_S$,
  $c a <= s_T$ still hold. Let
  $mu = min(r_R\/(a b), r_S\/(b c), r_T\/(c a))$. Then
  $mu >= min(r_R\/s_R, r_S\/s_S, r_T\/s_T) >= 1$, using the three norm
  conditions and $s_i <= r_i$. Also $mu a b c = min(c r_R, a r_S, b r_T)$;
  each argument floors one coordinate and $floor(x) > x\/2$ for $x >= 1$,
  so $mu a b c > min(hat(c) r_R, hat(a) r_S, hat(b) r_T) \/ 2 = U\/2$ by
  @lem-value. With $m = floor(mu) > mu\/2$ the size conditions hold
  ($m a b <= mu a b <= r_R$, etc.) and $Out = m a b c > U\/4$.
]

#remark(name: "regime witnesses")[
  If $U = D_(R,S) = r_R s_S$ then $b = 1$ (as $D_(R,S) <= H_S$ iff
  $r_R s_S <= r_T$) and $c = floor(s_S)$; when $r_R s_S <= r_S$ this is a
  "fan" in which every $R$-tuple owns $s_S$ private $z$'s. If $U = H_R$
  then $a = floor(sqrt(s_R r_T \/ r_S))$ and
  $b = floor(sqrt(s_R r_S \/ r_T))$; the $max(1, dot)$ is not needed,
  because $U = H_R$ forces $r_S <= s_R r_T$ and $r_T <= s_R r_S$. Here
  the $R$-blocks are tight for $s_R$ and the $S$- and $T$-blocks are
  slack. The tempting variant $c = s_S\/b$ is not admissible in general
  (for $r = (100,100,100)$, $s = (1, 100, 1)$ it gives $c a = 100 > s_T$);
  only the general formula of @thm-main is claimed.
] <rem-witness>

#remark(name: "the balanced block is not optimal")[
  Take $s_i = 2^12$ for all $i$, $r_R = 2^12$, $r_S = r_T = 2^16$. Then
  $U = H_S = H_T = 2^20$, and the construction gives $a = b = 16$,
  $c = 256$, $m = 16$, so $Out = 2^20 = U$ exactly. Balanced blocks
  ($a = b = c$, all three norm constraints tight) reach only $2^18$. The
  optimal shape leaves some norm constraints slack.
]

== The factor 4 is sharp

#theorem(name: [the constant $4$ is best possible])[
  For every real $t in [1, 2)$ the statistics
  $r = (r_R, r_S, r_T) = (t^2, t, t^2)$ and
  $sigma = (sqrt(t), 1, sqrt(t))$ are regular, $U = t^2$, and $W = 1$.
  Consequently
  $
    inf { W(r, sigma) \/ U(r, sigma) : (r, sigma) "regular" } = 1\/4,
  $
  and the infimum is not attained.
] <thm-sharp>
#st[#provedlean (@sec-mech, also in the two-sided form $inf W\/U = 1\/4$. This family, in the rational form below, was found by a model-based review: the GPT-5.6-sol Pro review of the first draft, @sec-ai.)]

#proof[
  Here $s_R = s_T = min(t, t^2) = t$ and $s_S = min(1, t) = 1$. The
  three Hölder terms are
  $H_R = sqrt(t dot t dot t^2)$, $H_S = sqrt(1 dot t^2 dot t^2)$ and
  $H_T = sqrt(t dot t^2 dot t)$, all equal to $t^2$; the degree terms
  are $D_(R,S) = D_(S,R) = D_(S,T) = D_(T,S) = t^2$ and
  $D_(R,T) = D_(T,R) = t^3 >= t^2$. So $U = t^2$.
  Let an instance be admissible. Then $|S| <= t < 2$, so $|S| <= 1$, and
  by @lem-deg every out-degree of $T$ is at most $opn(A_T)^2 <= t < 2$,
  so at most $1$. Counting by $S$-tuples,
  $Out = sum_((y,z) in S) |{x : (x,y) in R, (z,x) in T}| <= |S| dot max_z d^+_T (z) <= 1$.
  A single triangle ($|R| = |S| = |T| = 1$, all norms $1$) is
  admissible, so $W = 1$ and $W\/U = t^(-2) -> 1\/4$ as $t -> 2$. With
  @thm-main ($W > U\/4$ for every regular $(r, sigma)$) the infimum is
  $1\/4$ and is not attained.
]

The form of the family given in that review keeps every statistic
rational: with
$(p_1, q_1) = (7, 5)$, $p_(i+1) = 3 p_i + 4 q_i$,
$q_(i+1) = 2 p_i + 3 q_i$ one has $p_i^2 - 2 q_i^2 = -1$, and
$t_i = p_i^2 \/ q_i^2 = 2 - 1\/q_i^2$ gives $sigma_R = sigma_T = p_i\/q_i$
and $U\/W = t_i^2 = 2401\/625, 2825761\/707281, dots -> 4$ (recomputed
in exact rational arithmetic by `artifacts/verify/chk_exact.py`). On
this family the block construction of @thm-main has
$(a, b, c, m) = (1, 1, 1, 1)$ and is itself optimal; the loss of the
factor $4$ is in $U$, not in the construction: no instance at all
beats $U\/t^2$, so no better choice of blocks could improve the
constant of @thm-main.

== A single norm constraint <sec-single>

The following special case, in which only $R$'s norm is constrained
and $|R|$ is free, is a consistency check on @thm-main.

#corollary(name: "single norm constraint")[
  Let $sigma >= 1$ and $1 <= r_S <= r_T$. Then
  $
    sup{Out : opn(A_R) <= sigma, |S| <= r_S, |T| <= r_T}
      in (U_1\/4, U_1], quad
    U_1 = min(sigma^2 r_S, thick sigma sqrt(r_S r_T), thick r_S r_T).
  $
] <cor-single>
#st[#proved]

#proof[
  Any instance in the class is admissible for $r_R = |R|$ (which may be
  increased freely), $sigma_R = sigma$, $sigma_S = sqrt(r_S)$,
  $sigma_T = sqrt(r_T)$ (the last two are no constraint, by clipping).
  Take $r_R >= max(sigma^2, r_S r_T)$. Then $s_R = sigma^2$,
  $s_S = r_S$, $s_T = r_T$, and the nine terms are
  $H_R = sigma sqrt(r_S r_T)$, $H_S = H_T = sqrt(r_R r_S r_T) >= r_S r_T$,
  $D_(R,S) = r_R r_S >= r_S r_T$, $D_(R,T) = r_R r_T >= r_S r_T$,
  $D_(S,R) = r_S sigma^2$, $D_(S,T) = D_(T,S) = r_S r_T$,
  $D_(T,R) = r_T sigma^2 >= r_S sigma^2$. Hence $U = U_1$ for every such
  $r_R$. Since $U$ is nondecreasing in $r_R$, $U_1$ bounds every instance
  (@thm-main, upper bound), and the lower bound of @thm-main at
  $r_R = max(sigma^2, r_S r_T)$ gives an instance with $Out > U_1\/4$.
]

The three regimes ($sigma^2 <= r_T\/r_S$: star-shaped $R$;
$r_T\/r_S <= sigma^2 <= r_S r_T$: disjoint $K_(a,b)$ with $a b = sigma^2$;
$sigma^2 >= r_S r_T$: a single complete block) are all specializations
of the block formula. Because disjoint copies do not change $sigma$,
once $sigma$ is known the AGM bound can be off by an unbounded factor.

The next corollary measures norms for two relations only, the case of
a store that keeps $sigma$ for some predicates and not for others.

#corollary(name: "two measured norms")[
  Let $|R| <= r_R$, $|S| <= r_S$, $|T| <= r_T$, $opn(A_R) <= sigma_R$
  and $opn(A_S) <= sigma_S$, with no norm bound on $T$ and all five
  bounds at least $1$. Put $s_R = min(sigma_R^2, r_R)$,
  $s_S = min(sigma_S^2, r_S)$ and
  $
    U_2 = min{ sqrt(s_R r_S r_T), thick sqrt(s_S r_R r_T), thick
               r_R s_S, thick r_S s_R, thick r_T s_R, thick r_T s_S }
        = min{H_R, H_S, D_(R,S), D_(S,R), D_(T,R), D_(T,S)}.
  $
  Then $U_2 \/ 4 < W_2 <= U_2$, where $W_2$ is the supremum of $Out$
  over the class. The upper constant $1$ is attained, and the lower
  constant $1\/4$ is best possible: for $1 <= t < 2$ the statistics
  $r = (t^2, t, t^2)$, $sigma_R = sqrt(t)$, $sigma_S = 1$ have
  $U_2 = t^2$ and $W_2 = 1$. The witness is $Blk(a,b,c,m)$ of
  @thm-main with $U$ replaced by $U_2$.
] <cor-twonorm>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  Every $T$ with $|T| <= r_T$ has $opn(A_T)^2 <= |T| <= r_T$
  (@sec-prelim), so the class is the admissible class of @thm-main with
  $sigma_T = sqrt(r_T)$, which is regular, and $s_T = r_T$. With
  $s_T = r_T$ three of the nine terms are dominated:
  $H_T = sqrt(r_R r_S r_T) >= H_R$, $D_(R,T) = r_R r_T >= r_T s_R = D_(T,R)$
  and $D_(S,T) = r_S r_T >= r_T s_S = D_(T,S)$. So $U = U_2$, and
  @thm-main gives both bounds and the witness. For the sharpness family,
  $s_R = t$, $s_S = 1$ and the six terms are
  $(t^2, t^2, t^2, t^2, t^3, t^2)$, so $U_2 = t^2$. An admissible
  instance has $|S| <= t < 2$, so $|S| <= 1$, and every column degree of
  $R$ is an integer at most $opn(A_R)^2 <= t < 2$ (@lem-deg), so at most
  $1$; counting by $S$-tuples, $Out <= 1$, whatever $T$ is. One triangle
  is admissible, so $W_2 = 1$, and $W_2 \/ U_2 = t^(-2) -> 1\/4$ as
  $t -> 2$.
]

With only $sigma_R$ measured and all three sizes known
($s_S = r_S$, $s_T = r_T$), the nine terms reduce in the same way to
$
  U'_1 = min{ sqrt(s_R r_S r_T), thick r_S s_R, thick r_T s_R, thick
              r_R r_S, thick r_R r_T, thick r_S r_T },
$
and $U'_1 \/ 4 < W <= U'_1$. @cor-single is the case
$r_R >= max(sigma^2, r_S r_T)$ with $r_S <= r_T$, where the two
$r_R$-terms and $r_T s_R$ drop out.

#proposition(name: [every one of the nine terms is necessary])[
  For every integer $n >= 2$ and each of the nine terms of $U$ there are
  regular statistics $(r, sigma)$, all powers of $n$, at which that term
  is the unique minimum of $U$, the block of @thm-main is admissible
  with $Out = U$ exactly (so $W = U$), and deleting the term from the
  minimum raises it by the factor $n$. With $(r; s)$ written as exponent
  vectors $(e_R, e_S, e_T; f_R, f_S, f_T)$, i.e. $r_i = n^(e_i)$ and
  $s_i = n^(f_i)$, witnesses are
  $H_R$: $(4,4,4; 2,4,4)$ with $Blk(n,n,n,n^2)$ and $U = n^5$ (the other
  eight terms are at least $n^6$); $D_(R,S)$: $(2,6,6; 2,2,4)$ with
  $Blk(1,1,n^2,n^2)$ and $U = n^4$ (the others at least $n^5$); and, by
  the action of $S_3$ on the labels, which leaves $U$ invariant,
  $H_S$: $(4,4,4; 4,2,4)$, $H_T$: $(4,4,4; 4,4,2)$,
  $D_(R,T)$: $(2,6,6; 2,4,2)$, $D_(S,R)$: $(6,2,6; 2,2,4)$,
  $D_(S,T)$: $(6,2,6; 4,2,2)$, $D_(T,R)$: $(6,6,2; 2,4,2)$,
  $D_(T,S)$: $(6,6,2; 4,2,2)$. The same holds for the six terms of
  $U_2$ in @cor-twonorm.
] <prop-irred>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  For $H_R$: $s_R = n^2$, $r = (n^4, n^4, n^4)$, $s_S = s_T = n^4$ give
  $H_R = sqrt(n^2 n^8) = n^5$, $H_S = H_T = D_(S,R) = D_(T,R) = n^6$ and
  $D_(R,S) = D_(R,T) = D_(S,T) = D_(T,S) = n^8$. $Blk(n,n,n,n^2)$ has
  sizes $n^4$, squared norms $n^2 <= s_i$ and $Out = n^5$. For
  $D_(R,S)$: $r = (n^2, n^6, n^6)$, $s = (n^2, n^2, n^4)$ give
  $D_(R,S) = n^4$, $H_S = n^5$, $H_T = D_(R,T) = n^6$, $H_R = n^7$ and
  $D_(S,R) = D_(T,R) = D_(T,S) = n^8$, $D_(S,T) = n^10$. $Blk(1,1,n^2,n^2)$
  has sizes $(n^2, n^4, n^4) <= r$, squared norms $(1, n^2, n^2) <= s$
  and $Out = n^4$. In both cases $Out = U$ and the upper bound of
  @thm-main gives $W = U$. Relabelling by $S_3$ permutes the terms
  (@sec-prelim) and the witnesses. For $U_2$ the six blocks of
  `artifacts/hillclimb/P3-spectral/report.md` (same shapes) work
  verbatim.
]

So the regimes of @rem-witness are all realized: no term of $U$ can
be dropped, even for constant-factor accuracy.

#remark(name: "exact sizes")[
  For regular $(r, sigma)$ with integer $r_i$,
  $sup{Out : |i| = r_i, opn(A_i) <= sigma_i "for all" i} = W(r, sigma)$.
  An admissible instance pads to exact sizes with isolated edges on
  fresh endpoints: each adds a norm-$1$ block-diagonal component (so
  $opn(A_i)$ becomes $max(opn(A_i), 1) <= sigma_i$) and no triangle,
  while the exact-size class is a subclass. The same holds for the
  two-norm class of @cor-twonorm.
] <rem-exact-sizes>
#st[#proved]

== The labeled 4-cycle <sec-cycle4>

The same questions for the 4-cycle
$R(x,y) and S(y,z) and T(z,w) and Q(w,x)$, with
$Out = tr(A_R A_S A_T A_Q)$, have a larger answer. The labels
$R, S, T, Q$ are in cyclic order, so $\{R, T\}$ and $\{S, Q\}$ are the
opposite pairs. Sizes $r_e$, norms $sigma_e$, the clipped
$s_e = min(sigma_e^2, r_e)$, admissibility, regularity and the worst
case $W_4 (r, sigma)$ are defined as for the triangle. Complete
four-partite blocks no longer suffice: with $R$, $S$, $Q$ complete
$n times n$ and $T$ a perfect matching, $Out = n^3$, while any
admissible union of complete blocks for the same statistics
($s_T = 1$ forces the $Z$- and $W$-parts of every block to size $1$)
has output at most $|R| = n^2$.

#figure(
  placement: top,
  caption: [The 38 monomials of $U_4$. Indices $i, j, k, l$ are distinct
    labels; "opposite" means at distance two around the cycle. The
    family $A$ splits into two orbits of the dihedral group of the cycle
    ($\{j, k\}$ the two neighbours of $i$: 4 terms; otherwise: 8 terms),
    so there are ten orbits.],
  table(
    columns: (auto, auto, auto, auto),
    align: (left, left, left, right),
    table.hline(stroke: 0.8pt),
    table.header([*Family*], [*Monomial*], [*Condition*], [*Number*]),
    table.hline(stroke: 0.4pt),
    [$A$], [$r_i s_j s_k$], [$\{j, k\} subset.eq$ the other three labels], [12],
    [$B$], [$r_i (s_j s_k s_l)^(1\/2)$], [---], [4],
    [$C$], [$(r_i r_j s_k s_l)^(1\/2)$], [$\{i, j\}$ opposite], [2],
    [$C'$], [$(r_i r_j s_k s_l)^(1\/2)$], [$\{i, j\}$ adjacent], [4],
    [$D$], [$r_i r_j$], [$\{i, j\}$ opposite], [2],
    [$E$], [$(r_i r_k s_i s_j s_k)^(1\/2)$], [$i, j, k$ consecutive], [4],
    [$F$], [$(r_i r_j^2 s_i s_k s_l)^(1\/3)$], [$\{i, j\}$ opposite], [4],
    [$G$], [$(r_j r_k r_l s_i s_k s_l)^(1\/3)$], [$\{i, j\}$ opposite], [4],
    [$H$], [$(r_i r_j)^(1\/2) (s_R s_S s_T s_Q)^(1\/4)$], [$\{i, j\}$ opposite], [2],
    table.hline(stroke: 0.8pt),
  ),
) <tab-u4>

#theorem(name: "spectral AGM for the 4-cycle")[
  Let $U_4 (r, s)$ be the minimum of the 38 monomials of @tab-u4. Every
  admissible instance has $Out <= U_4$, with constant $1$ in each of the
  38 inequalities, and for regular statistics
  $
    U_4 \/ 16 < W_4 (r, sigma) <= U_4.
  $
  Each of the 38 terms is the unique minimum of $U_4$ on an open set of
  regular statistics, where an arc instance (below) attains it, so none
  can be dropped even for constant-factor accuracy.
] <thm-cycle4>
#st[#proved (on paper, not in Lean; the identification of the dual
vertices is an exact finite enumeration. Verified by two separately run
exact-arithmetic rebuilds; @app-verify.)]

The new ingredient is a bound on a "lifted" Gram matrix indexed by the
tuples of the middle relation.

#lemma(name: "lifted Gram bound")[
  Put $rho = A_R^top A_R$ and $tau = A_T A_T^top$, and let $K$ be the
  matrix indexed by the tuples $s = (y, z)$, $s' = (y', z')$ of $S$ with
  $K_(s s') = sqrt(rho_(y y') tau_(z z'))$. Then
  $lambda_max (K) <= opn(A_R) opn(A_S) opn(A_T)$.
] <lem-lambda>
#st[#proved]

#proof[
  If $R$, $S$ or $T$ is empty there is nothing to prove. On each
  connected component $c$ of the bipartite graph of $S$ choose positive
  vectors $p, q$ with $A_S q = sigma_c p$ and $A_S^top p = sigma_c q$
  on that component, where $sigma_c <= opn(A_S)$ (Perron--Frobenius).
  For $s = (y, z)$ put $theta_s = sqrt(q_z \/ p_y)$. For a nonnegative
  vector $u$ on $S$ let $U_y = sum_z u_(y z) theta_(y z)$ and
  $V_z = sum_y u_(y z) \/ theta_(y z)$. By Cauchy--Schwarz and
  $sum_(z in S(y, dot)) q_z = sigma_c p_y$,
  $U_y^2 <= sigma_c sum_z u_(y z)^2$, so
  $norm(U)^2 <= opn(A_S) norm(u)^2$, and likewise for $V$. For
  $kappa > 0$ the arithmetic--geometric mean inequality gives
  $K_(s s') <= (kappa theta_s theta_(s') rho_(y y') + kappa^(-1) (theta_s theta_(s'))^(-1) tau_(z z'))\/2$,
  hence
  $u^top K u <= (kappa U^top rho U + kappa^(-1) V^top tau V)\/2 <= (kappa opn(A_R)^2 + kappa^(-1) opn(A_T)^2) opn(A_S) norm(u)^2 \/ 2$.
  Take $kappa = opn(A_T)\/opn(A_R)$. Since $K$ is symmetric and
  nonnegative, $lambda_max (K)$ is attained at a nonnegative $u$.
]

#proof(of: [the upper bound of @thm-cycle4])[
  As for the triangle, every degree of relation $e$ is at most $s_e$
  and $opn(A_e)^2 <= s_e$. By rotation and reflection it suffices to
  prove one member of each family.
  _A, B._ An $R$-tuple $(x, y)$ extends to at most
  $d^+_S (y) Delta^+_T$, $d^+_S (y) d^-_Q (x)$ and
  $d^-_Q (x) Delta^-_T$ cycles, and to at most
  $1_(S(y, dot))^top A_T 1_(Q(dot, x)) <= opn(A_T) sqrt(d^+_S (y) d^-_Q (x))$;
  summing over $R$ gives $r_R s_S s_T$, $r_R s_S s_Q$, $r_R s_T s_Q$ and
  $r_R (s_S s_T s_Q)^(1\/2)$.
  _C, C'._
  $Out <= norm(A_R A_S)_F norm(A_T A_Q)_F <= opn(A_R) norm(A_S)_F opn(A_T) norm(A_Q)_F$,
  and $Out <= norm(A_R A_S A_T)_F norm(A_Q)_F <= opn(A_R) opn(A_S) norm(A_T)_F norm(A_Q)_F$.
  _D._ A cycle is determined by its $R$- and $T$-tuples.
  _E._ Forgetting $Q$, $Out$ is at most the number of paths
  $x -> y -> z -> w$, which is
  $(d^-_R)^top A_S d^+_T <= opn(A_S) norm(d^-_R) norm(d^+_T)$, and
  $norm(d^-_R)^2 <= Delta^-_R |R| <= s_R r_R$, $norm(d^+_T)^2 <= s_T r_T$.
  _F._ Let $M = A_R A_S A_T$, so $M_(x w)$ counts paths. Expanding two
  of the three factors of $M_(x w)^3$ over pairs of $S$-tuples,
  $sum_(x,w) M_(x w)^3 = sum_(s, s' in S) 1_(X_(s s'))^top M 1_(W_(s s'))$,
  where $X_(s s')$ is the set of common $R$-predecessors of $y, y'$ and
  $W_(s s')$ that of common $T$-successors of $z, z'$. Each term is at
  most $opn(M) sqrt(|X_(s s')| |W_(s s')|) <= opn(A_R) opn(A_S) opn(A_T) K_(s s')$,
  so by @lem-lambda
  $sum M^3 <= |S| opn(A_R)^2 opn(A_S)^2 opn(A_T)^2$, and Hölder over the
  $Q$-tuples gives $Out^3 <= |Q|^2 sum_((w,x) in Q) M_(x w)^3 <= r_Q^2 r_S s_R s_S s_T$.
  _H._ The 0/1 matrix $B$ indexed by $S times Q$ with
  $B_((y,z),(w,x)) = A_R (x, y) A_T (z, w)$ has $1^top B 1 = Out$ and
  $(B B^top)_(s s') = 1_(W_(s s'))^top A_Q 1_(X_(s s')) <= opn(A_Q) K_(s s')$
  entrywise, so $opn(B)^2 <= opn(A_Q) lambda_max (K) <= product_e opn(A_e)$
  and $Out <= opn(B) sqrt(|S| |Q|)$.
  _G._ Split $R$ into classes $R_(a b)$ by
  $d^-_Q (x) in [2^a, 2^(a+1))$ and $d^+_S (y) in [2^b, 2^(b+1))$ (tuples
  with a zero degree lie on no cycle), and let $h = A_Q A_(R_(a b)) A_S$
  and $X_(a b), Y_(a b)$ the vertices it touches. Its cycles number at
  most $min(norm(h)_1, sqrt(|T|) norm(h)_F) <= (|T| norm(h)_1 norm(h)_F^2)^(1\/3)$,
  with $norm(h)_1$ the entry sum, and
  $norm(h)_1 <= 4 dot 2^(a+b) |R_(a b)|$,
  $norm(h)_F^2 <= opn(A_Q)^2 opn(A_S)^2 |R_(a b)|$,
  $|R_(a b)|^2 <= opn(A_R)^2 |X_(a b)| |Y_(a b)|$,
  $2^a |X_(a b)| <= |Q|$ and $2^b |Y_(a b)| <= |S|$. So each class has at
  most $(4 r_T r_Q r_S s_Q s_S s_R)^(1\/3)$ cycles, and there are at most
  $(1 + log_2 |Q|)(1 + log_2 |S|)$ classes. The $n$-fold Kronecker power
  of the instance is a 0/1 instance whose output, sizes and norms are
  the $n$-th powers; applying the bound to it and taking $n$-th roots
  removes the factor $4^(1\/3)$ and the logarithms as $n -> infinity$.
]

*Arc instances.* Call the vertex classes $X, Y, Z, W$ around the cycle.
An _arc_ is a nonempty set of consecutive classes; we use the nine arcs
$\{X\}, \{Y\}, \{Z\}, \{W\}$, $\{X, Y\}, \{Y, Z\}, \{Z, W\}, \{W, X\}$
and $V = \{X, Y, Z, W\}$. Given integers $n_A >= 1$, a vertex of class
$v$ is a tuple of coordinates, one in $[n_A]$ for every arc $A$
containing $v$, and an edge of the cycle joins two vertices exactly when
they agree on every arc containing both classes. Each relation is then a
Kronecker product of identity matrices (arcs containing both ends),
all-ones vectors (arcs containing one end) and scalars, so
$
  |e| = product_(A inter e != emptyset) n_A, quad
  opn(A_e)^2 = product_(|A inter e| = 1) n_A, quad
  Out = product_A n_A.
$

#proof(of: [the lower bound of @thm-cycle4])[
  With $nu_A = log n_A >= 0$, the best real arc instance solves the
  linear program: maximize $sum_A nu_A$ subject to
  $sum_(A inter e != emptyset) nu_A <= log r_e$ and
  $sum_(|A inter e| = 1) nu_A <= log s_e$ for every edge $e$. By LP
  duality its value is the minimum, over the vertices of the dual
  polyhedron, of the corresponding combinations of $log r_e$ and
  $log s_e$. Exact enumeration gives $50$ vertices; $12$ are dominated
  by others whenever $1 <= s_e <= r_e$, and the remaining 38 are the
  terms of @tab-u4. (Adding the four arcs of three classes changes
  nothing: moving such a factor to $V$ keeps sizes and output and lowers
  two norms.) So the value is $log U_4$; let $n_A >= 1$ be an optimal
  real solution. Floor the eight proper arcs and set
  $m = floor(m^*)$ with
  $m^* = min_e r_e \/ product_(A != V, A inter e != emptyset) floor(n_A)$.
  The instance is admissible: floors only lower the norms, which do not
  involve $V$, and the sizes are at most $r_e$ by the choice of $m$.
  Exactly three proper arcs miss each edge, so
  $m^* product_(A != V) floor(n_A) = min_e r_e product_(A inter e = emptyset) floor(n_A) > min_e r_e product_(A inter e = emptyset) n_A \/ 8 >= U_4 \/ 8$,
  the last step because $r_e >= product_(A inter e != emptyset) n_A$.
  Since $m^* >= n_V >= 1$, $m > m^* \/ 2$, and $Out > U_4 \/ 16$.
  _Necessity._ For each kept vertex an exact rational point of regular
  statistics where it is the unique minimum is recorded in the
  artifacts; minimality persists on an open cone around it, and the arc
  instance supported on the vertex's tight arcs attains the term with
  equality there. Scaling along the cone makes the ratio of the next
  term to it unbounded.
]

#proposition(name: [the best constant lies in $[8, 16]$])[
  For $1 <= t <= L$, the statistics $r = (L, t, L, L)$ and
  $s = (t, t, t, L)$ have $U_4 = min(t^3, sqrt(L t^3))$. For
  $1 <= t < 2$ and $L = 8$ they are regular, $U_4 = t^3$ and $W_4 = 1$;
  hence $sup U_4 \/ W_4$ over regular statistics lies in $[8, 16]$.
] <prop-cycle4-sharp>
#st[#proved (the envelope by an exact exponent comparison of all 38
terms; @app-verify)]

#proof[
  Every term of @tab-u4 at these statistics is $L^a t^b$ with $a >= 0$,
  $a + b >= 2$ and $3a + b >= 3$; comparing exponents at $L = t$ and
  $L = t^3$, every term is at least $sqrt(L t^3)$ for $L <= t^3$ and at
  least $t^3$ above, and $r_S s_R s_T = t^3$ and
  $(r_S r_Q s_R s_T)^(1\/2) = sqrt(L t^3)$ attain the two values. For
  $t < 2$ and $L = 8 >= t^3$: $|S| <= t$, so $S$ has at most one tuple
  $(y, z)$; the column degree of $y$ in $R$ and the row degree of $z$ in
  $T$ are integers at most $s_R = s_T = t < 2$; so $Out <= 1$, and one
  cycle is admissible.
]

The condition $L >= t^3$ is needed: for $L < t^3$ the family has
$U_4 = sqrt(L t^3) < t^3$. If norms are given only for a set $P$ of
relations, put $s_e = r_e$ off $P$; @thm-cycle4 holds unchanged, and the
obstruction $8$ persists whenever $|P| >= 2$ (for adjacent $P = \{R, S\}$
use $r = (8, 8, 8, t)$, $s = (t, t, 8, t)$). The constant $16$ comes from
the rounding: flooring an arbitrary optimal real arc instance can lose
a factor approaching $16$ (take $n_Z = n_W = n_(\{Z, W\}) = n_V = t -> 2$,
all others $1$: $U_4 = t^4$ and the floored instance has one cycle).
Improving it needs a better choice among optima or instances outside
the arc family; on small integer grids the best integer arc instance is
within a factor $2.6$ of $U_4$. The 4-cycle instance with
$r = (1, n, n, n)$ and $s = (1, n, 1, n)$, which defeats complete blocks,
is the single arc $\{Z, W\}$ with $n_(\{Z, W\}) = n$, and attains
$U_4 = n$.

// =====================================================================
= Per-instance rotation: kernel optimality for $(r, sigma)$ <sec-kernel>
// =====================================================================

#lemma(name: "nested neighbourhoods")[
  Fix $R$ and the degree vectors $d^+_S$ and $d^-_T$. Order $Z$ once, and
  let $S'$ give each $y$ the first $d^+_S (y)$ elements of $Z$ and $T'$
  give each $x$ the first $d^-_T (x)$ elements. Then $S'$ has the same
  out-degrees $d^+_S$ as $S$, $T'$ has the same in-degrees $d^-_T$ as
  $T$, $|S'| = |S|$, $|T'| = |T|$, and $M_R = Out(R, S', T')$.
] <lem-nest>
#st[#provedlean (`kernelWork_eq_out_nest`, `rowDeg_nestS`, `colDeg_nestT`,
`card_nestS`, `card_nestT`.)]

#proof[
  Two prefixes of one order intersect in the shorter prefix, so
  $|S'(y, dot) inter T'(dot, x)| = min(d^+_S (y), d^-_T (x))$. Sum over
  $R$.
]

So the kernel's work is achieved as _output_ by an instance with the
same $R$, the same out-degrees of $S$, the same in-degrees of $T$ and
the same sizes; the in-degrees of $S'$ and out-degrees of $T'$ change
in general. This does *not* give $M_R <= W(r, sigma)$ for the original
norms: nesting can raise operator norms. The $2 times 2$ identity has
$opn(dot) <= 1$, while its nested version has $opn(dot)^2 >= 2$ (Lean:
`nestS_can_raise_opNorm`). We therefore combine @lem-nest only with
bounds that use no norm of $S'$ or $T'$.

#proposition(name: "kernel work against the nine terms")[
  On every admissible instance,
  $M_R <= min(H_R, D_(R,S), D_(R,T), D_(S,R), D_(T,R))$, and by rotation
  $M_S <= min(H_S, D_(S,T), D_(S,R), D_(T,S), D_(R,S))$ and
  $M_T <= min(H_T, D_(T,R), D_(T,S), D_(R,T), D_(S,T))$.
] <prop-kernel>
#st[#provedlean (`kernelWork_le_terms`, `kernelWork_le_opNorm_mul_sqrt`.)]

#proof[
  $H_R$: with $min(p,q) <= sqrt(p q)$, $u_x = sqrt(d^-_T (x))$ and
  $v_y = sqrt(d^+_S (y))$,
  $M_R <= u^top A_R v <= opn(A_R) norm(u) norm(v) = opn(A_R) sqrt(|T| |S|)$.
  $D_(R,S), D_(R,T)$: @lem-deg. $D_(S,R)$:
  $M_R <= sum_((x,y) in R) d^+_S (y) = sum_y d^-_R (y) d^+_S (y) <= s_R r_S$.
  $D_(T,R)$: $M_R <= sum_x d^+_R (x) d^-_T (x) <= s_R r_T$.
]

#corollary(name: "per-instance rotation is worst-case optimal")[
  Every one of the nine terms appears in at least one of the three lists
  of @prop-kernel. Hence on every admissible instance
  $min(M_R, M_S, M_T) <= U$, and if $(r, sigma)$ is regular then
  $U < 4 W(r, sigma)$.
] <cor-kernel>
#st[#provedlean (`kernel_min_le_U`; the second inequality is
@thm-main. Without regularity, $U$ can be positive while $W = 0$, e.g.
$r = (0.5, 1, 1)$, $sigma = (1,1,1)$.)]

The three $M_pi$ are computable exactly from degree arrays in
$O(sum_i r_i)$ time, or the rotation owning the argmin term of $U$ can be
chosen from statistics alone. Replacing $s_j$ by the corresponding
measured maximum degree in the six degree terms $D_(i,j)$ keeps every
bound valid (the Hölder terms need the norm). A kernel running the
chosen rotation with $O(1 + min)$ intersections does
$O(sum_i r_i + W)$ work for regular statistics.

#corollary(name: "two measured norms suffice for the planner")[
  In the setting of @cor-twonorm, every instance in the class satisfies
  $M_R <= min(H_R, D_(R,S), D_(S,R), D_(T,R))$ and
  $M_S <= min(H_S, D_(S,R), D_(R,S), D_(T,S))$. Every term of $U_2$
  occurs in one of the lists, so $min(M_R, M_S) <= U_2 < 4 W_2$: a
  planner drives $R$ when a minimizing term of $U_2$ is $H_R$, $D_(S,R)$
  or $D_(T,R)$, and $S$ when it is $H_S$, $D_(R,S)$ or $D_(T,S)$. The
  restriction to the two measured relations is necessary. As a budget:
  with $R$ and $S$ perfect matchings on $k$ vertices per part and
  $T = K_(k,k)$, $s_R = s_S = 1$ and $r = (k, k, k^2)$ give
  $U_2 = W_2 = Out = M_R = M_S = k$ while $M_T = k^2$, so
  $M_T \/ W_2$ is unbounded (but $M_T <= N$ there). Including the input:
  with $T = K_(k,k)$, $R$ giving each $x$ a private out-star of $k$
  vertices and $S$ giving each $z$ a private in-star of $k$ further
  vertices, $N = 3k^2$, $s_R = s_S = k$, $U_2 = k^(5\/2)$ and
  $M_T = k^3$, so $M_T \/ (N + U_2) = Theta(k^(1\/2))$.
] <cor-planner2>
#st[#proved (on paper; exact checks in @app-verify)]

#proof[
  @prop-kernel with $s_T = r_T$; $D_(R,T) = r_R r_T >= D_(T,R)$ and
  $D_(S,T) >= D_(T,S)$ are redundant. In the example an $R$-tuple
  $(x_i, y_i)$ has $d^+_S (y_i) = 1$ and $d^-_T (x_i) = k$, and an
  $S$-tuple $(y_i, z_i)$ has $d^-_R (y_i) = 1$ and $d^+_T (z_i) = k$, so
  $M_R = M_S = k$; every $T$-tuple $(z, x)$ has
  $d^+_R (x) = d^-_S (z) = 1$, so $M_T = k^2$;
  the six terms are $(k^(3\/2), k^(3\/2), k, k, k^2, k^2)$ and $Out = k$.
  In the star example, disjoint stars $K_(1,k)$ have squared norm $k$,
  so $r = (k^2, k^2, k^2)$, $s_R = s_S = k$, and the six terms are
  $(k^(5\/2), k^(5\/2), k^3, k^3, k^3, k^3)$; every $T$-tuple $(z, x)$
  has $d^+_R (x) = d^-_S (z) = k$, so $M_T = k^3$.
]

The Hölder term also survives sorted intersections: by @lem-sorted-agm
the galloping kernel driven by $R$ costs $O(N + opn(A_R) sqrt(|S| |T|))$
comparisons, with constant $3$ and no logarithm.

#proposition(name: "no fixed rotation is optimal; nor is the sum")[
  (a) There are instances with $W <= 1$ and $M_R = k$. (b) There are
  instances with $M_R \/ (sum_i r_i + U) = Theta(sqrt(k))$ while
  $M_S = M_T = 0$. By relabelling, the same holds for the fixed rotations
  $S$ and $T$, and for $M_R + M_S + M_T$.
] <prop-norot>
#st[#proved (on paper; not formalized.)]

#proof[
  (a) $R = {(x_i, y_0)}_(i <= k)$, $S = {(y_0, z_0)}$,
  $T = {(z_i, x_i)}_(i <= k)$ with $z_i != z_0$. Then $Out = 0$,
  $M_R = k$, $M_S = M_T = 0$, and $s = (k, 1, 1)$ so
  $W <= U <= D_(S,T) = 1$. (Here $M_R <= r_R$, so this refutes only
  $O(W)$.)
  (b) $R = K_(k,k)$; $S$ gives each $y$ a private out-star of $k$ $z$'s;
  $T$ gives each $x$ a private in-star of $k$ further $z$'s. Then
  $r = (k^2, k^2, k^2)$ and, since a disjoint union of stars
  $K_(1,k)$ has norm $sqrt(k)$, $s = (k^2, k, k)$. The nine terms are
  $H_R = k^3$, $H_S = H_T = k^(5\/2)$, $D_(S,R) = D_(T,R) = k^4$ and
  $k^3$ for the other four, so $U = k^(5\/2)$. Every $R$-tuple has
  $min(d^+_S, d^-_T) = k$, so $M_R = k^3$; every $S$-tuple ends at a $z$
  with $d^+_T (z) = 0$ and every $T$-tuple starts at a $z$ with
  $d^-_S (z) = 0$, so $M_S = M_T = 0$. Hence
  $M_R \/ (3 k^2 + k^(5\/2)) = Theta(sqrt(k))$ (numerically $0.80$,
  $1.37$, $2.29$, $3.70$, $5.82$ for $k = 4, 8, 16, 32, 64$).
]

Both families have $Out = 0$ and are not semijoin-reduced: one
semijoin pass empties them. Reduction does not remove the loss in (b):
padding it (@lem-pad) gives a pairwise semijoin-reduced instance with
$M_R >= k^3$ (costs only grow), sizes $Theta(k^2)$, and
$s_S, s_T = O(k)$ by the Schur test, so $U <= H_S = O(k^(5\/2))$ and the
$Theta(sqrt(k))$ loss against $sum_i r_i + U$ remains (measured ratios
$0.56$, $0.84$, $1.30$ for $k = 8, 16, 32$).

// =====================================================================
= Engine and experiments: summary <sec-engine-summary>
// =====================================================================

This section states what the engine does with the results above and
what the measurements do and do not show; @sec-exp and @sec-engine give
the setups, tables and caveats. The engine is Leatherback, which will be
open-sourced; at the time of writing the triangle operator and both
admission stages described below are on a development branch, not on
its main branch. The paper repository (@sec-artifacts) holds the
engine-run scripts and raw data.

*The operator.* Leatherback's triangle operator answers a run of three
triple patterns forming a triangle with constant predicates, in any of
the eight edge directions. It returns exactly the bag the greedy
left-deep plan would produce, or declines before any answer is visible,
and allocates nothing per row. For each tuple of the driver $E_1$ it
intersects two sorted runs from the shorter side, so its candidate
budget is $M_pi$; the entries it actually walks are at most $M_pi$ (a
Lean bridge proves this for a replica, @sec-mech), and its total work
adds scan, galloping and seek overheads. It does not implement
per-binding choice or price-then-run.

*Planning.* For each candidate driver the planner reads $64$ evenly
strided rows, estimates $hat(M) = floor(|E_1| dot "mean"(min(d_2, d_3)))$
from CSR degrees and picks the driver minimizing $2|E_1| + hat(M)$; a
gate then admits the operator only when its estimate beats greedy's
first $2$-path (stage 1), and a second stage in calibrated units
re-prices declined triangles on warm stored views (the _rescue_,
@sec-engine). @cor-kernel certifies the exact-$M$ choice and the
statistics-owner choice, *not* the sampled estimator, and no fixed
sampling grid can be certified:

#proposition(name: "no fixed sampling grid is within a constant factor")[
  Fix $k >= 1$. Let a planner price each candidate driver $E$ with
  $n = |E|$ rows by reading the rows at a set $P(n)$ of
  $1 <= k_n <= k$ positions of $E$'s scan order, chosen in advance for
  each $n$, setting
  $hat(M)_E = floor(n sum_(q in P(n)) min(d_2, d_3) \/ k_n)$, and
  choosing the argmin of $2n + hat(M)_E$, ties to the first pattern.
  (The stride $floor(s n \/ 64)$ and the golden-ratio grid that
  Leatherback's other planners sample with are two such rules.) For every $m > k$ there are an instance
  $I_m$ with $N = 3m^2 + 2$ and an integer $1 <= j <= k$ such that:
  + $hat(M)_R = 0$, the planner picks $R$, and on a warm store the gate
    admits it for every ratio $rho <= (m + 1)\/2$, and the floor does
    whenever $N >= 2048$;
  + $M_R = m dot min_pi M_pi = m dot Out = m^2 (m - j)$, and the
    operator driven by $R$ walks at least $(m - 1) m (m - j)$ entries;
  + if $m >= 2k$, then
    $(2|R| + M_R) \/ min_pi (2|E_pi| + M_pi) >= m \/ 8$.
  So on $I_m$ with $m >= 2k$ the chosen driver costs
  $Theta(N^(1\/2))$ times the best one, in budget, in walked entries and
  in the planner's own objective; no fixed bounded sample count and no
  fixed grid avoids this.
] <prop-sampler>
#st[#proved (on paper; proof in @sec-engine, exact checks in @app-verify)]


*Three planner quantities.* _Output upper bounds_ (AGM, the degree
bound, $B_2$, $U$) bound $|Out|$ and size buffers; by themselves they
bound no executor's work. _Work bounds for the chosen executor_: for
the kernel driven by $pi$ the walked entries are at most $M_pi$, and
$min_pi M_pi <= U$ (@cor-kernel), while $B_2$ is not a work bound for
this kernel even with the best driver ($"GMIN"$, @thm-sep(2)) or with
per-binding choice (@cor-l2-false). _Estimated execution costs_
($2|E_1| + hat(M)$ against greedy's sampled first $2$-path, and the
rescue's calibrated costs) are estimates, not bounds: $hat(M)$ can be
$0$ when $M_pi = Theta(N^(3\/2))$ (@prop-sampler).

*What the measurements show* (@sec-exp, @sec-engine). All rates are
for selected canonical triangle queries over the largest predicates of
each dataset, with intersecting supports and nonzero output; they are
not weighted by any workload, exclude zero-answer queries, and one
dataset (sci50) is 50 relabelled copies of one graph. First-row and tail
latency and metered kernel work were not measured.
- _Spectral bound (3,124 queries)._ $U$ is below AGM by a median factor
  $9.6$, but tighter than the best of AGM, the cyclic $ell_2$ bound and
  the degree bound on only $6.5%$ of queries, and $U_"cert" >= ell_2$
  on $81.2%$ of them: our pre-registered success criterion is not met as
  registered. $U$ is useful as one more term in a minimum, and for its
  guarantee (@cor-kernel), not as a replacement estimator.
- _Driver choice (1,241 knowledge-graph queries, six policies)._ The
  driver matters: the worst forced driver is up to $132 times$ slower
  than the best. But choosing it by the exact planner objective
  $2|E_1| + M_pi$ instead of the $64$-row estimate changes the driver on
  only 3--6% of queries, the median and p90 of the exact pick's
  forced-time gain are exactly $1$, and the exact policy is
  $36$--$90 times$ slower end to end because of its degree passes. So
  the sampled planner did as well as exact counting on this workload,
  although it has no worst-case guarantee (@prop-sampler).
- _Admission (same queries)._ Stage 1 declined 66--73% of queries, and
  on many of them the operator would have been faster. A rescue stage,
  fitted to these same queries, cuts total time by 20.6%, 48.8% and
  32.5% against a stage-1-only planner run in the same process with the
  policy order shuffled every round (run C). On queries whose plan the
  rescue leaves unchanged, the two arms agree to a median ratio of
  $1.000$--$1.005$: there the extra rescue tests stay within run-to-run
  noise (descriptively; we did no uncertainty analysis), and no rescued
  query is more than $1.2 times$ slower. A
  model-run audit (@app-verify) found that the first implementation's
  candidate pruning was not equivalent to the searched rule; the fixed
  implementation that run C measures decides as the rule over every
  candidate, which changed one decision (a CoDEx-L query now declined).
  On three synthetic control stores the rescue changes no decision; a
  $1.06 times$ slowdown on a 54 ms `COUNT(*)` seen in a single earlier
  run did not reproduce over 10 alternating process pairs (median
  $0.995$).


// =====================================================================

// =====================================================================
= Related work and novelty <sec-related>
// =====================================================================

*Worst-case optimal joins, and where the kernel comes from.* The AGM
bound [#cite(<ref-agm>)[AGM13]], NPRR [#cite(<ref-nprr>)[NPRR18]],
Leapfrog Triejoin [#cite(<ref-lftj>)[Vel14]], Ngo's survey
[#cite(<ref-ngo>)[Ngo18]] and "Skew strikes back"
[#cite(<ref-skew>)[NRR13]] establish the size-only theory; Minesweeper
[#cite(<ref-mine>)[NNRR14]] and geometric resolution
[#cite(<ref-geo>)[ANRR15]] go beyond worst case; Joglekar and Ré use
degree uniformization [#cite(<ref-jr>)[JR16]]; Free Join
[#cite(<ref-freejoin>)[WWS23]] unifies binary and WCOJ plans; Kara et
al. maintain triangle counts under updates [#cite(<ref-kara>)[KNNOZ19]].
The kernel of @sec-kernel is not new. For a fixed driver $R$, its work
$M_R$ is, up to a semijoin of $R(x, dot)$ with $pi_Y S$, the
intersection cost of Generic Join on the triangle with the order
$x, y, z$, i.e. of Algorithm 2 of [#cite(<ref-skew>)[NRR13]],
whose bound $M_R <= sqrt(|R| |S| |T|)$ is classical
[#cite(<ref-skew>)[NRR13], App. B]; Birler, Kemper and Neumann
implement the same per-tuple smaller-side intersection as the Expand3
operator [#cite(<ref-diamond>)[BKN24]]. What @sec-kernel adds is the
bound of $M_pi$ by the spectral and clipped-degree terms
(@prop-kernel) and, with @thm-main, the worst-case optimality of
choosing the driver per instance for the statistics $(r, sigma)$
(@cor-kernel).

*Per-binding and adaptive orders.* Choosing the evaluation strategy
separately for each binding is prior art, and we do not claim it.
Algorithm 1 of [#cite(<ref-skew>)[NRR13]] chooses, for each binding of
the first variable, between two evaluation options using $O(1)$ degree
products ("the power of two choices"). In compact WCOJ indexes for
graph databases, Arroyuelo et al. bind next the variable with the
fewest candidates and note that, after the first variable is bound, the
next variable to bind may differ for each binding
[#cite(<ref-simjoin>)[ABGHNR24], Sec. 5]; Arroyuelo et al.
[#cite(<ref-cidx>)[ABFGN25], Sec. 6.1] study such adaptive variable
elimination orders systematically, recomputing the second variable for
each binding from the sizes of the candidate ranges. ADOPT
[#cite(<ref-adopt>)[WTKO23]] splits the value space into hypercubes
and runs Leapfrog Triejoin on each under an attribute order chosen by
reinforcement learning; it proves AGM worst-case optimality (under the
assumption that the number of episodes is constant) and convergence to
the attribute order that minimizes the number of steps. SkinnerDB
[#cite(<ref-skinner>)[TWM+19]] learns join orders at run time, and
Graphflow [#cite(<ref-graphflow>)[MS19]] fixes the first two query
vertices, so for a triangle it has no per-binding freedom. Not all of
these guarantees are size-only. Arroyuelo et al. treat each $k$-nearest
neighbour clause as a virtual relation in which every $x$ has at most
$k$ partners, and bound the output by a linear program that extends
Ngo's bound for acyclic degree constraints; the bound is tight when the
constraint graph is acyclic. Their Leapfrog Triejoin over the Ring,
binding variables in a topological order of that graph, runs in time
$O(Q^* |Q| log N)$ for that program's value $Q^*$ when the constraints
are acyclic or form a single 2-cycle [#cite(<ref-simjoin>)[ABGHNR24],
Sec. 4, Lemma 3 and Thms. 2--3]. Their Example 4 is a triangle with one
relation replaced by a $k$-NN clause: the degree constraint lowers the
output bound from AGM's $O(N^(3\/2))$ to $O(k N)$, and the order
$y, z, x$ can need $N^(3\/2)$ variable eliminations where $y, x, z$
needs $k N$. So variable order under degree constraints is analysed
there. The differences from this paper are the statistic and the
class: their degree bound is a constant $k$ known in advance for a
similarity relation, the data relations enter only through their sizes,
and their fewest-candidates rule is not claimed worst-case optimal for
other constraint cycles. None of these works bounds the cost of
per-binding choice against degree-sequence or $ell_2$ statistics of the
data relations, and we found no statement of the cyclic $ell_2$ bound
of @thm-pb-upper, its lower bound, or the separations of @thm-sep.
Our per-binding class
(@sec-adapt) differs from these selectors in two ways that matter for
the statements. First, the option at a binding is the one of smaller
exact cost $c_P (u)$, not the one with fewer candidates; so
@thm-pb-upper bounds this exact-cost choice (and price-then-run,
@prop-ptr), not candidate-count heuristics. The lower bounds
@thm-pb-lower and @thm-pb-slopes bound the best per-binding choice, so
they apply to every selector in the class. Second, an intersection is
charged at the length of the shorter run, as with hash or bitmap
probing (the Expand3 operator and our engine); a leapfrog or galloping
intersection of sorted runs can cost less than the shorter run when
identifiers are contiguous. With adversarial identifiers our lower
bounds against $N + B_2$ hold for every fresh comparison-based
intersection routine, and the worst case at $B_2 asymp N$ gains exactly
$(log N)^(1\/4)$ (@sec-sorted).

*Adaptive sorted-set intersection.* Demaine, López-Ortiz and Munro
[#cite(<ref-dlm>)[DLM00]] gave comparison lower bounds for adaptive
intersection, union and difference of sorted sets in terms of the size
of a proof (certificate) of the answer; Barbay and Kenyon
[#cite(<ref-bk>)[BK02], #cite(<ref-bk08>)[BK08]] analysed intersection
by the alternation of the sets, with deterministic and randomized lower
bounds; and doubling search is the unbounded search of Bentley and Yao
[#cite(<ref-by>)[BY76]]. @lem-cert and @lem-decision are these
arguments for two runs in our model, and the galloping price $h$ is the
standard doubling-search cost. What @sec-sorted adds is that one global
labeling makes all the critical calls of a join construction
simultaneously hard (@lem-interleave, @thm-sorted-g8), and the
resulting tradeoff for per-binding choice: an upper bound with the
factor $(log N)^(1\/4)$ and its necessity (@thm-sorted-upper,
@thm-quarterlog).

*Partitioned algorithms.* Algorithms that meet $ell_p$ bounds partition
the data. Jayaraman, Ropell and Rudra [#cite(<ref-jrr>)[JRR21]] bucket
each relation by the power-of-two degree of its source attribute and,
for every combination of buckets, run the three spanning acyclic (path)
plans of the directed triangle in parallel, stopping at the first to
finish; for $p in (1, 2]$ this runs in time linear in the bound of one
orientation (their Thm. 4.4, with a factor $2^((p+1)|V|)$, $O(1)$-time
B-tree access in the RAM model, and $O(N log N)$ index construction).
Running it on both orientations meets $B_2$ up to that factor. Abo
Khamis et al. reduce $ell_p$ constraints to PANDA
[#cite(<ref-panda>)[ANS17]] by partitioning each relation into parts
with near-uniform degrees, losing a polylogarithmic factor
[#cite(<ref-anos>)[ANOS24], Thm. 2.6]; PANDAExpress
[#cite(<ref-pandaexpress>)[ANS25], Cor. 8.2] handles $ell_p$
constraints in time $O((N + B) log N)$ with data-dependent hyperplane
partitions, and shows that a constant number of axis-parallel
(threshold) partitions does not suffice for some disjunctive Datalog
rules. Jaguar [#cite(<ref-jaguar>)[AC26a]] evaluates Boolean conjunctive
queries under degree constraints in time $O(N^("subw" + epsilon))$ by
heavy/light partitioning guided by violations of submodularity; it does
not treat $ell_p$ constraints. Guanaco [#cite(<ref-guanaco>)[AC26b]]
evaluates Boolean conjunctive queries in time with exponent just above
the submodular width by enforcing consistency, partitioning relations
until they are globally uniform, and joining pairs of relations. Like
Jaguar and PANDAExpress, it partitions relations to control the
discrepancy of their degrees, the lever that the unpartitioned class of
@sec-adapt lacks. Capelli, Irwin and Salvati
[#cite(<ref-cis>)[CIS25]] use one _fixed_ variable order and branch on
the bits of values; their algorithm is worst-case optimal up to
polylogarithmic factors whenever the class of instances is prefix
closed for that order, which covers cardinality constraints and acyclic
degree constraints. Our @cor-l2-false is a statement about the
_unpartitioned_ class of @sec-adapt (one root per instance, an option
per binding, smaller-side intersections). It is consistent with, and
explains, the degree partitioning of [#cite(<ref-jrr>)[JRR21],
#cite(<ref-anos>)[ANOS24], #cite(<ref-pandaexpress>)[ANS25]]; it does
not say that adaptive algorithms in general cannot meet $B_2$.

*Fixed orders.* Ngo's survey records that fixed-order algorithms are
optimal under acyclic degree constraints [#cite(<ref-ngo>)[Ngo18]].
Under $ell_2$ constraints, Jayaraman, Ropell and Rudra show that no
single spanning acyclic subquery meets the $ell_2$ bound
[#cite(<ref-jrr>)[JRR21], Sec. 2.4 and Ex. B.1]: the path join
$R bowtie S$ can output $L^(5\/2)$ tuples while the triangle has at most
$L^2$, a gap of $N^(1\/4)$ at $|R| = L^2$. That example concerns path
plans, which do not intersect with the closing relation. The
separations of @thm-sep concern Generic Join _with_ smaller-side
intersections, a fixed root with per-binding options, and the best of
the six orders per instance, on pairwise semijoin-reduced inputs. ADOPT
converges to the best single attribute order, against which @thm-sep(2)
gives a loss of $N^(1\/5)$ relative to $N + B_2$ in our cost model; but
ADOPT may use different orders on different value ranges, and we have
not shown that our families defeat a constant number of value-range
cubes under an adversarial assignment of identifiers.

*Norm-based bounds and the operator norm.* Abo Khamis, Nakos, Olteanu
and Suciu bound join sizes by $ell_p$-norms of degree sequences
[#cite(<ref-anos>)[ANOS24]]; their Eq. (3) gives our degree comparator
and their Eq. (4) is the cyclic $ell_2$ bound $B_2$ (one orientation).
LpBound [#cite(<ref-lpbound>)[ZMA+25]] turns these bounds into a
pessimistic estimator with stored norms $p in {1, dots, 10, infinity}$.
The degree sequence bound [#cite(<ref-dsb>)[DSBC23]], SafeBound
[#cite(<ref-safebound>)[DSB23]] and the ambidextrous bounds of Lin and
Wang [#cite(<ref-linwang>)[LW25]] use degree sequences; MNC
[#cite(<ref-mnc>)[SBE+19]] estimates the sparsity of matrix products.
None of these uses the operator norm of the incidence matrix, and the
operator norm is not a function of degree sequences, even labeled ones:
the 0/1 matrices with rows ${1, 2}, {1}, {3}$ and with rows
${2, 3}, {1}, {1}$ both have row sums $(2, 1, 1)$ and column sums
$(2, 1, 1)$, but squared operator norms $(3 + sqrt(5))\/2$ and $2$. So
the class of @thm-main is not an $ell_p$ class. Conversely, the six
degree terms of $U$ are Eq. (3) of [#cite(<ref-anos>)[ANOS24]] with
maximum degrees replaced by the bound $sigma^2$ of @lem-deg.

*Matrix and spectral inequalities.* The Hölder term is the case
$(infinity, 2, 2)$ of the Schatten--Hölder inequality
$|tr(A B C)| <= norm(A)_(S_p) norm(B)_(S_q) norm(C)_(S_r)$,
$1\/p + 1\/q + 1\/r = 1$ [#cite(<ref-bhatia>)[Bha97], Ch. IV], combined
with $opn(A)^2 <= |A|$. The other cases with $p, q, r >= 2$ add nothing
for our statistics: $norm(A_i)_(S_p)^p <= opn(A_i)^(p-2) |A_i|$, so the
bound is at most $product_i sigma_i^(1 - 2\/p_i) r_i^(1\/p_i)$, which is
log-linear in $(1\/p_R, 1\/p_S, 1\/p_T)$ and so is minimized at a vertex
of ${theta in [0, 1\/2]^3 : sum_i theta_i = 1}$, that is, at a Hölder
term (with $sigma_i^2$ in place of $s_i$). The degree terms use the 0/1
entries (@lem-deg) and have no counterpart in this family. Hatami
[#cite(<ref-hatami>)[Hat08]] characterizes the graphs $H$ whose
homomorphism densities $t_H (dot)^(1\/|E(H)|)$ are norms through a
Hölder-type inequality; even cycles give Schatten norms, but Hölder
graphs are bipartite, so the triangle lies outside that theory, and no
lower bounds under mixed size and norm constraints are given. Collins
and Yuan [#cite(<ref-cy>)[CY26]] bound multi-leg partial traces of
tensor products of matrices under operator-norm constraints alone, by
powers of the tensor-factor dimension; with one leg the problem is
trivial, and neither sizes nor 0/1 entries enter. For a simple graph
with $m$ edges, $t$ triangles and spectral radius $lambda_1$, the
folklore bound
$6t = tr(A^3) = sum_i lambda_i^3 <= lambda_1 sum_i lambda_i^2 = 2 m lambda_1$
is our Hölder term with $R = S = T$ the symmetric edge relation,
$r_i = 2m$, $sigma_i = lambda_1$ and $Out = 6t$. Bollobás and Nikiforov
[#cite(<ref-bn>)[BN07]] bound clique counts from below by the spectral
radius; Nikiforov's survey [#cite(<ref-nik>)[Nik11]] covers spectral
Turán problems; Ning and Zhai [#cite(<ref-nz>)[NZ21]] bound the number
of triangles in terms of $n$, $m$ and $lambda_1$; Rivin
[#cite(<ref-rivin>)[Riv01]] bounds cycle counts by the number of edges;
Alon, Yuster and Zwick [#cite(<ref-ayz>)[AYZ97]] count short cycles;
EigenTriangle [#cite(<ref-tso>)[Tso08]] estimates triangle counts from
top eigenvalues. All of these concern one symmetric graph. The Schur
test [#cite(<ref-schur>)[Sch11], #cite(<ref-hs>)[HS78]], the
signless-Laplacian facts [#cite(<ref-crs>)[CRS10]] and Ryser's
interchange theorem [#cite(<ref-ryser>)[Rys57]] are classical. SPARQL
WCOJ engines include [#cite(<ref-hogan>)[HRRS19],
#cite(<ref-ring>)[AHN+21], #cite(<ref-gbhn>)[GHN26]].

*Novelty, stated carefully.* The proofs are elementary, and the
analytic ingredients (Schatten--Hölder, degree bounds, the
smaller-side kernel, per-binding choice, racing alternatives) are
known. To our knowledge, the following statements are new; we regard
(iii) and (iv) as the main contributions.
(i) Under joint size and operator-norm constraints on three labeled
relations, the worst-case triangle output satisfies $U\/4 < W <= U$
for the nine-term $U$, the factor $4$ is asymptotically sharp
(@thm-sharp, with a family found by a model-based review, @sec-ai), and one
block family witnesses the lower bound in every regime (@thm-main).
(ii) The work of the smaller-side kernel driven by the best rotation is
at most $U$, so per-instance choice of the driver is worst-case optimal
for $(r, sigma)$, while no fixed driver is (@cor-kernel,
@prop-norot). (iii) In the cost model of @sec-adapt, the best
per-binding choice costs at most
$N + (|R| |S| |T|)^(1\/8) min(Lambda, Lambda')^(1\/2)$
(@thm-pb-upper), and this is tight: at $B_2 asymp N$ the worst-case
exponent is $9\/8$ (@thm-pb-lower), and together with @thm-pb-upper2
the bound is attained up to a constant factor at every real slope in
$[9\/10, 3\/2]$ (@cor-real-slopes, @thm-pb-asym); the $9\/8$ lower
bound at $B_2 asymp N$ also holds on pairwise semijoin-reduced,
connected inputs and for a single directed predicate (@prop-selfjoin;
below slope $1$ no single-predicate family exists, since
$B_(2,P) >= N_P\/3$), and on fully reduced inputs the gap lies in
$[1\/10, 1\/8]$, exact for $kappa >= 11\/10$ (@thm-fullred). We claim these bounds for
this cost model only; per-binding choice itself is prior art, and
partitioned algorithms meet $B_2$ [#cite(<ref-jrr>)[JRR21],
#cite(<ref-pandaexpress>)[ANS25]]. (iv) The separations of @thm-sep for
Generic Join with smaller-side intersections: against $N + B_2$, one
fixed order has gap exactly $1\/4$ ($"GMR"$, @thm-onegao) and the best
of the six orders exactly $1\/5$ ($"GMIN"$, also after padding to a
semijoin-reduced family with $C = Theta(N)$; @thm-best6); against
$C + N$, a fixed
order, the best of six orders and a fixed root each lose $N^(1\/2)$;
against $N + B_2$ a fixed root loses between $N^(1\/8)$ and $N^(1\/4)$
(@cor-fixedroot). A polynomial gap for single
path plans was observed in [#cite(<ref-jrr>)[JRR21], Ex. B.1]. (v) A
deterministic scheduler that selects a root of cost exactly $C$ in
$C + min(6C, 2N) + 4n + O(1)$ per-edge units (@prop-ptr); running
alternatives in parallel and stopping at the first to finish is the
multiplexing of [#cite(<ref-jrr>)[JRR21]], and what is new is the
exact-cost selection and the bound. (vi) The Ferrers profiles of
@prop-ferrers, an elementary consequence of Ryser's theorem; they
concern _labeled_ degree sequences, and say nothing about the coarser
classes of sorted degree sequences used by
[#cite(<ref-dsb>)[DSBC23], #cite(<ref-safebound>)[DSB23],
#cite(<ref-lpbound>)[ZMA+25]]. (vii) The sorted fresh-call comparison
model of @sec-sorted: the lower bounds against $N + B_2$ of (iii) and
(iv) under one adversarial labeling, and the matching quarter logarithm
(@thm-quarterlog); the single-call certificate and doubling-search
arguments are classical [#cite(<ref-dlm>)[DLM00], #cite(<ref-bk>)[BK02],
#cite(<ref-by>)[BY76]]. (viii) For the labeled 4-cycle, the 38-term
$U_4$ with $U_4\/16 < W_4 <= U_4$, the lifted Gram bound @lem-lambda
and the arc instances (@thm-cycle4); Hatami's Schatten-norm results
for even cycles [#cite(<ref-hatami>)[Hat08]] concern one symmetric
matrix and no size constraints.

We read in full, or in all sections bearing on these claims:
#cite(<ref-agm>)[AGM13], #cite(<ref-nprr>)[NPRR18],
#cite(<ref-lftj>)[Vel14], #cite(<ref-skew>)[NRR13],
#cite(<ref-ngo>)[Ngo18], #cite(<ref-jr>)[JR16],
#cite(<ref-anos>)[ANOS24], #cite(<ref-jrr>)[JRR21],
#cite(<ref-lpbound>)[ZMA+25], #cite(<ref-cis>)[CIS25],
#cite(<ref-pandaexpress>)[ANS25], #cite(<ref-jaguar>)[AC26a],
#cite(<ref-adopt>)[WTKO23], #cite(<ref-simjoin>)[ABGHNR24],
#cite(<ref-cidx>)[ABFGN25], #cite(<ref-diamond>)[BKN24],
#cite(<ref-hatami>)[Hat08], #cite(<ref-cy>)[CY26],
#cite(<ref-freejoin>)[WWS23], #cite(<ref-skinner>)[TWM+19],
#cite(<ref-mine>)[NNRR14], #cite(<ref-geo>)[ANRR15] and
#cite(<ref-kara>)[KNNOZ19]. We read only the abstracts of
#cite(<ref-bn>)[BN07], #cite(<ref-nz>)[NZ21] and
#cite(<ref-guanaco>)[AC26b], and did not check
#cite(<ref-mnc>)[SBE+19], #cite(<ref-linwang>)[LW25],
#cite(<ref-rivin>)[Riv01], #cite(<ref-ayz>)[AYZ97] or
#cite(<ref-nik>)[Nik11] in full. We cite
#cite(<ref-dlm>)[DLM00], #cite(<ref-bk>)[BK02], #cite(<ref-bk08>)[BK08]
and #cite(<ref-by>)[BY76] for the techniques named above on the basis
of their abstracts and a summary in a model-based review (@sec-ai), not
a full reading. Searches for operator-norm or
spectral join-size bounds, for extremal traces of products of
nonnegative or 0/1 matrices under operator-norm and Frobenius
constraints, and for tensor-network contraction bounds found nothing
closer than the works above.

// =====================================================================
= Open problems <sec-open>
// =====================================================================

+ *Per-binding cost on fully reduced inputs.* When every tuple lies in a
  triangle, the worst-case gap against $N + B_2$ lies in
  $[1\/10, 1\/8]$ and equals the general value $(3 - 2kappa)\/8$ at
  every slope $kappa in [11\/10, 3\/2]$ (@thm-fullred). On the window
  $kappa in [1, 11\/10)$ it lies in $[kappa\/11, (3 - 2kappa)\/8]$
  (@rem-window), and no union of rotated live gadgets can do better than
  $1\/10$. Is the answer $1\/10$? Raising the lower end needs another
  design; lowering the upper end needs a bound that uses triangle
  support, not only pairwise support. #openst
+ *The quarter logarithm below slope $1$.* In the sorted model the
  upper bound $hat(C) <= N + 3^(7\/8) L_N^(1\/4) N^(-1\/8) B_2^(5\/4)$
  holds (@cor-sorted-upper2). Is the factor $(log N)^(1\/4)$ necessary
  on $(9\/10, 1)$, against the family of @thm-pb-asym, as it is on
  $[1, 3\/2)$ (@thm-quarterlog)? #openst
+ *Minimal partitioning.* Is a _constant_ number of root classes per
  variable, chosen from degree metadata, enough to reach $O(N + B_2)$?
  This would be the least partitioning that closes the $N^(1\/8)$ gap of
  @cor-l2-false. A computation in a relaxed exponent model (vertex
  classes and degrees as powers of $N$), not reproduced here, suggests
  that at most $7$ parts per variable matter. PANDAExpress shows that a
  constant number of axis-parallel partitions does not suffice for some
  disjunctive Datalog rules [#cite(<ref-pandaexpress>)[ANS25], Sec. 3];
  whether this happens for the $ell_2$ triangle is open. #openst
+ *Partition-free algorithms in general.* @cor-l2-false is a lower
  bound for the per-binding cost model of @sec-adapt, and
  @thm-sorted-g8 for fresh comparison-based intersection calls. Does
  _every_ partition-free algorithm, for a suitable definition of the
  class, fail to run in $O(N + B_2)$, or $tilde(O)(N + B_2)$? Semijoin
  pruning and certificate reuse already escape the fresh-call model
  (@rem-sorted-scope). #openst
+ *Value-range orders.* @sec-sorted settles sorted intersections for
  fresh calls: the lower bounds survive, and the worst case at
  $B_2 asymp N$ is $Theta(N^(9\/8) (log N)^(1\/4))$. Do they survive
  against algorithms such as ADOPT that use different orders on a
  constant number of value ranges [#cite(<ref-adopt>)[WTKO23]]? #openst
+ *A fixed root against $N + B_2$, and one GAO on reduced inputs.*
  Determine the worst-case gap of a fixed root, which lies in
  $[1\/8, 1\/4]$ (@cor-fixedroot), and the gap of one fixed GAO on
  pairwise semijoin-reduced inputs, which lies in $[1\/5, 1\/4]$
  (@thm-onegao). #openst
+ *Self-joins with two equal predicates.* @prop-selfjoin settles one
  predicate: the $9\/8$ lower bound and the order separations survive,
  a fixed root cannot be separated for the cyclic self-join, and a
  symmetric predicate has $C <= N + B_2$. Which separations survive when
  exactly two of the three edges share a predicate, where renaming the
  variables is not a symmetry? #openst
+ *A joint spectral and polymatroid bound.* Combine $sigma_i$, maximum
  degrees $Delta_i <= sigma_i^2$ and $ell_p$-norms of degree sequences
  in one bound with a matching lower bound. Replacing $s_j$ by
  $Delta_j$ in the degree terms keeps the upper bound valid; the matching
  lower bound under joint $(sigma, Delta)$ constraints, and the
  integration of $sigma$ into the polymatroid framework of
  [#cite(<ref-anos>)[ANOS24]], are open. The experiments show that the
  gain lies in combining, since $U$ alone rarely wins on the selected
  nonzero canonical queries of @sec-exp. #openst
+ *Longer cycles, and the 4-cycle constant.* The 4-cycle is settled up
  to the constant: $U_4\/16 < W_4 <= U_4$ (@thm-cycle4), and the best
  constant lies in $[8, 16]$ (@prop-cycle4-sharp). Is it $8$? For
  $k$-cycles, $k >= 5$, the arc instances and the lifted Gram argument
  appear to extend (we have not checked this), the list of needed terms
  (the vertices of the dual of the arc program) has not been computed,
  and queries with several cycles are open. #openst
+ *Bags.* Equality constraints $|R_i| = r_i$ are settled
  (@rem-exact-sizes) and the galloping logarithm is analysed
  (@sec-sorted); bag semantics is not. #openst
+ *The sampled planner.* @prop-sampler answers the question for
  fixed sampling grids: the gap to the best driver can be
  $Theta(N^(1\/2))$. Does a planner reading $O(1)$, or
  $O(log N)$, _uniformly random_ rows per candidate pick, with constant
  probability, a driver within a constant factor of
  $min_pi (2|E_pi| + M_pi)$? Do grids chosen from the data (for
  example, one row per distinct key), or semijoin-reduced inputs, avoid
  the gap? #openst

// =====================================================================
= Use of AI tools <sec-ai>
// =====================================================================

Generative AI was used throughout this work: to search for and prove
theorems, to write and run the exact-arithmetic checks and the Lean
proofs, to implement and measure the engine operator, to draft and
revise the text, and to review it. The author directed the work, checked
the results he relies on, and is responsible for every claim; no AI
system is an author. The form of this statement follows the AI-use
disclosure that closes [#cite(<ref-gbhn>)[GHN26]].

*Who did what.* Orchestration, implementation and drafting: Claude Code
with Claude Opus 5.5 (Anthropic), in one session that also launched
Claude subagents for theorem search, proofs, internal refereeing,
verification and audits, and that wrote the Lean proofs and the engine
code. Solvers and verifiers for the results added in the third and
fourth drafts: Claude Fable 5.1 agents at maximum effort and Codex CLI
agents (OpenAI) with GPT-6-Astra at "ultra" effort, run as paired solver
and verifier lanes; a Codex CLI agent also searched for the admission
rule of @sec-engine and audited its implementation. Reviews: four
internal drafts preceded this version. The first was reviewed by
GPT-5.6-sol Pro (OpenAI) and by Claude Fable 5.1; the second by
GPT-6-Astra Pro, by Claude Fable 5.1, and in a separate GPT-6 Pro
session run by the author; the third by GPT-6-Astra Pro. Before posting,
Weaver, TJC's internal work agent, reviewed the third draft and supplied
the outside checks of @app-verify. All of these reviews were
model-based; no human referee has reviewed this work.

*Credits and checks.* Where the text credits a review (@thm-sharp,
@cor-real-slopes, @prop-selfjoin, @rem-ptr and the remark after
@thm-quarterlog), the credited content came from that review;
@tab-provenance gives the provenance of every group of results. Model
output entered the paper only after the checks of @app-verify: exact
rebuilds by agents that did not share the solvers' code, line-by-line
proof audits, and, for the results tagged Lean-checked, the Lean
kernel.

// =====================================================================
// References
// =====================================================================
#heading(numbering: none)[References]


#set par(first-line-indent: 0em)
#set text(size: 10pt)

#bib("ABFGN25")[
  D. Arroyuelo, F. Barisione, A. Fariña, A. Gómez-Brandón, G. Navarro,
  New compressed indices for multijoins on graph databases,
  #emph[Information Systems], 2025;
  #link("https://arxiv.org/abs/2408.00558")[arXiv:2408.00558].
] <ref-cidx>
#bib("ABGHNR24")[
  D. Arroyuelo, B. Bustos, A. Gómez-Brandón, A. Hogan, G. Navarro,
  J. Reutter, Worst-case-optimal similarity joins on graph databases,
  in: #emph[SIGMOD 2024].
] <ref-simjoin>
#bib("AC26a")[
  M. Abo Khamis, H. Chen, Jaguar: a primal algorithm for conjunctive
  query evaluation in submodular-width time, #emph[Proc. ACM Manag.
  Data] 4(2) (PODS 2026), Article 108,
  #link("https://doi.org/10.1145/3801904")[doi:10.1145/3801904];
  #link("https://arxiv.org/abs/2603.13624")[arXiv:2603.13624].
] <ref-jaguar>
#bib("AC26b")[
  M. Abo Khamis, H. Chen, Guanaco: a global-uniformity algorithm for
  near-submodular-width conjunctive query evaluation,
  #link("https://arxiv.org/abs/2610.05440")[arXiv:2610.05440], 2026.
] <ref-guanaco>
#bib("AGM13")[
  A. Atserias, M. Grohe, D. Marx, Size bounds and query plans for
  relational joins, #emph[SIAM J. Comput.] 42(4) (2013) 1737--1767.
] <ref-agm>
#bib("AHN+21")[
  D. Arroyuelo, A. Hogan, G. Navarro, J. L. Reutter, J. Rojas-Ledesma,
  A. Soto, Worst-case optimal graph joins in almost no space, in:
  #emph[SIGMOD 2021].
] <ref-ring>
#bib("ANOS24")[
  M. Abo Khamis, V. Nakos, D. Olteanu, D. Suciu, Join size bounds using
  $ell_p$-norms on degree sequences, in: #emph[PODS 2024],
  #link("https://arxiv.org/abs/2306.14075")[arXiv:2306.14075].
] <ref-anos>
#bib("ANRR15")[
  M. Abo Khamis, H. Q. Ngo, C. Ré, A. Rudra, Joins via geometric
  resolutions: worst-case and beyond, in: #emph[PODS 2015],
  #link("https://arxiv.org/abs/1404.0703")[arXiv:1404.0703].
] <ref-geo>
#bib("ANS17")[
  M. Abo Khamis, H. Q. Ngo, D. Suciu, What do Shannon-type inequalities,
  submodular width, and disjunctive Datalog have to do with one another?,
  in: #emph[PODS 2017].
] <ref-panda>
#bib("ANS25")[
  M. Abo Khamis, H. Q. Ngo, D. Suciu, PANDAExpress: a simpler and
  faster PANDA algorithm, #emph[Proc. ACM Manag. Data] (PODS 2026),
  #link("https://doi.org/10.1145/3801910")[doi:10.1145/3801910];
  #link("https://arxiv.org/abs/2512.10217")[arXiv:2512.10217], 2025.
] <ref-pandaexpress>
#bib("AYZ97")[
  N. Alon, R. Yuster, U. Zwick, Finding and counting given length
  cycles, #emph[Algorithmica] 17(3) (1997) 209--223.
] <ref-ayz>
#bib("Bha97")[
  R. Bhatia, #emph[Matrix Analysis], Graduate Texts in Mathematics 169,
  Springer, 1997.
] <ref-bhatia>
#bib("BK02")[
  J. Barbay, C. Kenyon, Adaptive intersection and $t$-threshold
  problems, in: #emph[SODA 2002], 390--399.
] <ref-bk>
#bib("BK08")[
  J. Barbay, C. Kenyon, Alternation and redundancy analysis of the
  intersection problem, #emph[ACM Trans. Algorithms] 4(1) (2008),
  Article 4.
] <ref-bk08>
#bib("BKN24")[
  A. Birler, A. Kemper, T. Neumann, Robust join processing with diamond
  hardened joins, #emph[PVLDB] 17 (2024).
] <ref-diamond>
#bib("BN07")[
  B. Bollobás, V. Nikiforov, Cliques and the spectral radius,
  #emph[J. Combin. Theory Ser. B] 97(5) (2007) 859--865.
] <ref-bn>
#bib("BY76")[
  J. L. Bentley, A. C.-C. Yao, An almost optimal algorithm for
  unbounded searching, #emph[Inform. Process. Lett.] 5(3) (1976) 82--87.
] <ref-by>
#bib("CIS25")[
  F. Capelli, O. Irwin, S. Salvati, A simple algorithm for worst-case
  optimal join and sampling, in: #emph[ICDT 2025],
  #link("https://arxiv.org/abs/2409.14094")[arXiv:2409.14094].
] <ref-cis>
#bib("CRS10")[
  D. Cvetković, P. Rowlinson, S. Simić, #emph[An Introduction to the
  Theory of Graph Spectra], Cambridge University Press, 2010.
] <ref-crs>
#bib("CY26")[
  B. Collins, W. Yuan, Operator norm bounds for multi-leg matrix tensors
  and applications to random matrix theory,
  #link("https://arxiv.org/abs/2603.27659")[arXiv:2603.27659], 2026.
] <ref-cy>
#bib("Data")[
  Datasets: SNAP (J. Leskovec, A. Krevl, #link("https://snap.stanford.edu/data")[snap.stanford.edu/data]):
  ca-GrQc, email-Eu-core, wiki-Vote, soc-Epinions1, com-youtube,
  com-dblp; Wikidata5M (transductive split, train+valid+test);
  CoDEx-L (#link("https://github.com/tsafavi/codex")[github.com/tsafavi/codex]);
  sci50, a local synthetic RDF store made of 50 relabelled copies of a
  369,661-triple scientists knowledge graph; the copies share their
  predicates, literals and 134 non-namespace IRIs (objects only).
  SHA-256 digests of the downloaded files are recorded with the
  experiment.
] <ref-data>
#bib("DLM00")[
  E. D. Demaine, A. López-Ortiz, J. I. Munro, Adaptive set
  intersections, unions, and differences, in: #emph[SODA 2000],
  743--752;
  #link("https://cs.uwaterloo.ca/~alopez-o/cspap/adaptive_set/")[cs.uwaterloo.ca/\~alopez-o/cspap/adaptive_set].
] <ref-dlm>
#bib("dMU21")[
  L. de Moura, S. Ullrich, The Lean 4 theorem prover and programming
  language, in: #emph[CADE-28], LNCS 12699, Springer, 2021.
] <ref-lean>
#bib("DSB23")[
  K. Deeds, D. Suciu, M. Balazinska, SafeBound: a practical system for
  generating cardinality bounds, in: #emph[SIGMOD 2023],
  #link("https://arxiv.org/abs/2211.09864")[arXiv:2211.09864].
] <ref-safebound>
#bib("DSBC23")[
  K. Deeds, D. Suciu, M. Balazinska, W. Cai, Degree sequence bound for
  join cardinality estimation, in: #emph[ICDT 2023],
  #link("https://arxiv.org/abs/2201.04166")[arXiv:2201.04166].
] <ref-dsb>
#bib("GHN26")[
  A. Gómez-Brandón, A. Hogan, G. Navarro, Uplifting the superpowers of
  worst-case-optimal join algorithms,
  #link("https://arxiv.org/abs/2608.03840")[arXiv:2608.03840], 2026.
] <ref-gbhn>
#bib("Hat08")[
  H. Hatami, Graph norms and Sidorenko's conjecture,
  #link("https://arxiv.org/abs/0806.0047")[arXiv:0806.0047], 2008.
] <ref-hatami>
#bib("HRRS19")[
  A. Hogan, C. Riveros, C. Rojas, A. Soto, A worst-case optimal join
  algorithm for SPARQL, in: #emph[ISWC 2019].
] <ref-hogan>
#bib("HS78")[
  P. R. Halmos, V. S. Sunder, #emph[Bounded Integral Operators on $L^2$
  Spaces], Springer, 1978.
] <ref-hs>
#bib("JR16")[
  M. Joglekar, C. Ré, It's all a matter of degree: using degree
  information to optimize multiway joins, in: #emph[ICDT 2016],
  #link("https://arxiv.org/abs/1508.01239")[arXiv:1508.01239].
] <ref-jr>
#bib("JRR21")[
  S. V. M. Jayaraman, C. Ropell, A. Rudra, Worst-case optimal binary
  join algorithms under general $ell_p$ constraints,
  #link("https://arxiv.org/abs/2112.01003")[arXiv:2112.01003], 2021.
] <ref-jrr>
#bib("KNNOZ19")[
  A. Kara, H. Q. Ngo, M. Nikolic, D. Olteanu, H. Zhang, Counting
  triangles under updates in worst-case optimal time, in:
  #emph[ICDT 2019],
  #link("https://arxiv.org/abs/1804.02780")[arXiv:1804.02780].
] <ref-kara>
#bib("LW25")[
  Y.-T. Lin, H.-P. Wang, Ambidextrous degree sequence bounds for
  pessimistic cardinality estimation,
  #link("https://arxiv.org/abs/2510.04249")[arXiv:2510.04249], 2025.
] <ref-linwang>
#bib("Mat20")[
  The mathlib Community, The Lean mathematical library, in: #emph[CPP
  2020].
] <ref-mathlib>
#bib("MS19")[
  A. Mhedhbi, S. Salihoglu, Optimizing subgraph queries by combining
  binary and worst-case optimal joins, #emph[PVLDB] 12(11) (2019);
  #link("https://arxiv.org/abs/1903.02076")[arXiv:1903.02076].
] <ref-graphflow>
#bib("Ngo18")[
  H. Q. Ngo, Worst-case optimal join algorithms: techniques, results, and
  open problems, in: #emph[PODS 2018],
  #link("https://arxiv.org/abs/1803.09930")[arXiv:1803.09930].
] <ref-ngo>
#bib("Nik11")[
  V. Nikiforov, Some new results in extremal graph theory, in:
  #emph[Surveys in Combinatorics 2011], LMS Lecture Note Series 392,
  Cambridge University Press, 2011.
] <ref-nik>
#bib("NNRR14")[
  H. Q. Ngo, D. T. Nguyen, C. Ré, A. Rudra, Beyond worst-case analysis
  for joins with Minesweeper, in: #emph[PODS 2014],
  #link("https://arxiv.org/abs/1302.0914")[arXiv:1302.0914].
] <ref-mine>
#bib("NPRR18")[
  H. Q. Ngo, E. Porat, C. Ré, A. Rudra, Worst-case optimal join
  algorithms, #emph[J. ACM] 65(3) (2018);
  #link("https://arxiv.org/abs/1203.1952")[arXiv:1203.1952].
] <ref-nprr>
#bib("NRR13")[
  H. Q. Ngo, C. Ré, A. Rudra, Skew strikes back: new developments in the
  theory of join algorithms, #emph[SIGMOD Record] 42(4) (2013);
  #link("https://arxiv.org/abs/1310.3314")[arXiv:1310.3314].
] <ref-skew>
#bib("NZ21")[
  B. Ning, M. Zhai, Counting substructures and eigenvalues I: triangles,
  #link("https://arxiv.org/abs/2112.12937")[arXiv:2112.12937], 2021.
] <ref-nz>

#bib("Riv01")[
  I. Rivin, Counting cycles and finite dimensional $L^p$ norms,
  #link("https://arxiv.org/abs/math/0111106")[arXiv:math/0111106], 2001.
] <ref-rivin>
#bib("Rys57")[
  H. J. Ryser, Combinatorial properties of matrices of zeros and ones,
  #emph[Canad. J. Math.] 9 (1957) 371--377.
] <ref-ryser>
#bib("SBE+19")[
  J. Sommer, M. Boehm, A. V. Evfimievski, B. Reinwald, P. J. Haas, MNC:
  structure-exploiting sparsity estimation for matrix expressions, in:
  #emph[SIGMOD 2019].
] <ref-mnc>
#bib("Sch11")[
  I. Schur, Bemerkungen zur Theorie der beschränkten Bilinearformen mit
  unendlich vielen Veränderlichen, #emph[J. Reine Angew. Math.] 140
  (1911) 1--28.
] <ref-schur>
#bib("Tso08")[
  C. E. Tsourakakis, Fast counting of triangles in large real networks
  without counting: algorithms and laws, in: #emph[ICDM 2008].
] <ref-tso>
#bib("TWM+19")[
  I. Trummer, J. Wang, D. Maram, S. Moseley, S. Jo, J. Antonakakis,
  SkinnerDB: regret-bounded query evaluation via reinforcement learning,
  in: #emph[SIGMOD 2019],
  #link("https://arxiv.org/abs/1901.05152")[arXiv:1901.05152].
] <ref-skinner>
#bib("Vel14")[
  T. L. Veldhuizen, Leapfrog Triejoin: a simple, worst-case optimal join
  algorithm, in: #emph[ICDT 2014],
  #link("https://arxiv.org/abs/1210.0481")[arXiv:1210.0481].
] <ref-lftj>
#bib("WTKO23")[
  J. Wang, I. Trummer, A. Kara, D. Olteanu, ADOPT: adaptively optimizing
  attribute orders for worst-case optimal join algorithms via
  reinforcement learning, #emph[PVLDB] 16(11) (2023) 2805--2817;
  #link("https://arxiv.org/abs/2307.16540")[arXiv:2307.16540].
] <ref-adopt>
#bib("WWS23")[
  Y. R. Wang, M. Willsey, D. Suciu, Free Join: unifying worst-case
  optimal and traditional joins, in: #emph[SIGMOD 2023],
  #link("https://arxiv.org/abs/2301.10841")[arXiv:2301.10841].
] <ref-freejoin>
#bib("ZMA+25")[
  H. Zhang, C. Mayer, M. Abo Khamis, D. Olteanu, D. Suciu, LpBound:
  pessimistic cardinality estimation using $ell_p$-norms of degree
  sequences, in: #emph[SIGMOD 2025],
  #link("https://arxiv.org/abs/2502.05912")[arXiv:2502.05912].
] <ref-lpbound>

// =====================================================================
// Appendices
// =====================================================================
#pagebreak()
#set par(first-line-indent: 1.2em)
#set text(size: 11pt)
#in-app.update(true)
#counter(heading).update(0)
#set heading(numbering: "A.1.", supplement: [Appendix])
#align(center, text(size: 13pt, weight: "bold")[Appendices])

// =====================================================================
= Experiments <sec-exp>
// =====================================================================

*Setup.* Data are listed in [#cite(<ref-data>)[Data]]. For each
dataset we took the largest predicates (wikidata5m: 24, CoDEx-L: 36,
sci50: 81; each SNAP graph is one predicate, also symmetrized) and
enumerated every triangle query
```
?x p1 ?y .  ?y p2 ?z .  ?z p3 ?x
```
with each predicate possibly transposed, canonical up to rotation and
whole-cycle reversal, keeping queries whose variables' supports
intersect and whose output is nonzero: 3,124 queries (wikidata5m 1,781;
CoDEx-L 871; sci50 456; SNAP 16). The 16 SNAP queries are too few to
support any claim on their own; their column in @tab-e2 is descriptive
only. All rates below are conditional on
this selection: canonical queries over the chosen large predicates,
with intersecting supports and nonzero output. They are not weighted
by any workload and exclude zero-answer queries. The code, the
results file, the logs, the dataset URLs with SHA-256 digests, the
commands and the Python environment are in `artifacts/e2/` of the paper
repository (@sec-artifacts); re-running the commands on the six SNAP
graphs and CoDEx-L reproduces every column except timings; a checker
audits the results file for internal consistency, and the summary
script, run on the committed results file and spectral data, rebuilds
the summary exactly. The sci50 file can
be rebuilt from its one-copy input, which is its own first 369,661
lines; the repository records the SHA-256 digests of both files and the
replication recipe. We write a query as `p1 . p2 . p3`,
listing the predicates on the $R$, $S$, $T$ edges, with `^T` marking a
transposed predicate. *sci50 is not an independent knowledge graph*: it
is 50 relabelled copies of one scientists knowledge graph of 369,661
triples. Copy $k > 0$ renames every IRI of the base namespace, so the
copies share their predicates and the terms the renaming leaves alone:
42,993 literals and 134 IRIs outside the namespace, all in object
position only (2,481,777 = 50 × 48,773 + 43,127 terms). The copies
are therefore not vertex-disjoint. Since no shared term is a subject, a
triangle has at most one shared vertex and its other two vertices lie
in one copy, so every size and every $Out$ is exactly $50$ times the
copy's (checked on all 456 rows). $sigma$ is not always the copy's: a
relation whose objects are all shared is 50 row blocks over the same
columns, and its $sigma$ is $sqrt(50)$ times the copy's (11 of the 81
predicates: dates, identifiers, `label`); the 58 with no shared object
keep their $sigma$, and the other 12 lie between ($sigma^2$ ratio
$1.62$ to $12.6$). On 426 of the 456 queries the binding term of $U$
uses only unchanged $sigma$'s, so $U$ is $50$ times the copy's and
AGM$\/U$ is $sqrt(50) approx 7.07$ times the copy's; on the other 30
the factor runs from $1\/sqrt(50)$ to $6.05$. Measured on one copy, the
456 queries have median AGM$\/U$ $8.96$ (minimum $1.22$), against
$63.4$ ($8.64$) on sci50; $ell_2\/U$ has median $0.767$ on both, and
degree$\/U$ $0.316$ against $0.307$. We therefore report AGM$\/U$ with
and without sci50.

$Out$ is counted exactly and cross-checked by sparse matrix products
wherever those cost at most $3 times 10^8$ flops (2,842 of 2,842
agreed). $sigma$ comes from power iteration, cross-checked with `svds`,
and is bracketed in exact rational arithmetic: below by the larger of
the maximum degree and the Rayleigh quotient of the final iterate,
above by the Collatz--Wielandt bound of that iterate rounded up to a
positive integer vector. Every exact bracket has relative width at most
$10^(-6)$; on one view (wikidata5m `P106`) the floating-point iteration
hit its 3,000-step cap with a float bracket of width
$4.6 dot 10^(-6)$, and only the exact bracket reaches $10^(-6)$. The
_certified_ $sigma$ is $min$(Schur bound
$sqrt(Delta_"row" Delta_"col")$, Collatz--Wielandt after $5$ power steps
from $bold(1)$), each evaluated exactly (the Schur bound as the integer
$Delta_"row" Delta_"col"$, the Collatz--Wielandt bound as an exact
fraction with the iterate rounded up to integers) and its square root
rounded upward, so it is a guaranteed upper bound. An earlier
computation of these certificates in floating point without outward
rounding left the stored value one rounding step below the
maximum-degree lower bound on six sci50 views; all certificates are
recomputed here, which changes no count below. No bound fell below
$Out$ on any row. We write $M = min(M_R, M_S, M_T)$. A separately
written recomputation of 22 rows from raw data reproduced every exact
quantity (sizes, $Out$,
$M_R, M_S, M_T$, AGM, $ell_2$, degree) exactly and $sigma$ to
$5 times 10^(-8)$; its comparison of certified $sigma$ predates the
exact certificates and is superseded by them.

*Comparator caveat.* "Best prior" below is $min(AGM, ell_2, "degree")$
with the two cyclic $ell_2$ orientations of @sec-prelim. It omits the
$ell_3$ and mixed-orientation $ell_p$ bounds of
[#cite(<ref-anos>)[ANOS24], Eq. (5) and Section 1.1] and their LP over
all $ell_p$ statistics, as implemented in LpBound
[#cite(<ref-lpbound>)[ZMA+25]]. Against those, $U$ can only win less
often, so the win rate below is an upper estimate.

#figure(
  placement: top,
  caption: [Distribution of $"bound"\/U$ over the 3,124 queries
    (log scale). Left of the vertical line the prior bound is tighter
    than $U$. AGM is never tighter (by construction); the best of the
    three prior bounds is tighter on $93.5%$ of the selected nonzero
    canonical queries.],
  image("e2_ecdf.svg", width: 100%),
) <fig-ecdf>

#figure(
  placement: top,
  caption: [Summary over queries; each row names its statistic.
    KG = wikidata5m and CoDEx-L; sci50 = 50 relabelled copies of one
    knowledge graph that share their literals (AGM$\/U$ is $sqrt(50)$
    times the one-copy value on 426 of the 456 queries); best prior
    $= min(AGM, ell_2, "degree")$; $M = min_pi M_pi$.],
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, right, right, right, right),
    table.hline(stroke: 0.8pt),
    table.header([*Statistic*], [*All (3,124)*], [*KG (2,652)*],
      [*sci50 (456)*], [*SNAP (16)*]),
    table.hline(stroke: 0.4pt),
    [AGM$\/U$, median], [9.57], [8.98], [63.4], [3.73],
    [AGM$\/U$, minimum], [1.47], [1.47], [8.64], [2.35],
    [$ell_2\/U$, median], [0.502], [0.451], [0.767], [0.838],
    [degree$\/U$, median], [0.282], [0.275], [0.307], [4.43],
    [best prior$\/U$, median], [0.209], [0.199], [0.291], [0.838],
    [best prior$\/U$, maximum], [3.996], [3.996], [3.05], [2.35],
    [queries with $U < ell_2$], [589 (18.9%)], [424], [163], [2],
    [queries with $U <$ best prior], [204 (6.5%)], [169], [33], [2],
    [$U\/Out$, median], [$5.4 times 10^4$], [$1.0 times 10^5$], [$1.4 times 10^3$], [14.8],
    [$M\/U$, median (maximum)], [$1.5 times 10^(-4)$ (0.59)], [$9.3 times 10^(-5)$ (0.57)], [$1.9 times 10^(-3)$ (0.26)], [0.27 (0.59)],
    [$U_"cert"\/U$, p90 (maximum)], [1.02 (1.14)], [1.02 (1.05)], [1.02 (1.06)], [1.06 (1.14)],
    [$U_"Schur"\/U$, median], [2.64], [3.00], [1.73], [3.04],
    table.hline(stroke: 0.8pt),
  ),
) <tab-e2>

*Gap to AGM.* $U <= AGM$ always (@sec-prelim), so only the size of the
gap is empirical: the median AGM$\/U$ is $9.57$ over all queries and
$8.98$ over the 2,668 queries outside sci50 (minimum $1.47$); the sci50
median of $63.4$ is $sqrt(50)$ times the one-copy median of $8.96$
(on 426 of the 456 queries AGM$\/U$ is exactly $sqrt(50)$ times its
one-copy value).

*Which bound is tightest.* Over the 3,124 selected queries the degree
bound is the tightest on 1,902, $ell_2$ on 1,018, $U$ on 204 and AGM on none.
With the exact upper end of each $sigma$ bracket in place of the
estimate, $U$ still wins on the same 204 queries. Every one of the 204
wins of $U$ comes from a Hölder term
($sqrt(s_R r_S r_T)$: 121, $sqrt(s_T r_R r_S)$: 55,
$sqrt(s_S r_R r_T)$: 28). This is forced: by @lem-deg the maximum
degrees satisfy $Delta <= s$, so the degree terms of $U$ are never
smaller than the classical degree bound. The largest win is
$3.996 times$ (e.g. wikidata5m `P17 . P47 . P17^T`, borders between
countries); the largest losses are on hub predicates such as `P17`
(country) and `P31` (instance of), where $ell_2\/U$ falls to $0.0017$.
A hub of degree $Delta$ forces $sigma^2 >= Delta$, and the Hölder term
charges that mass to the whole relation, whereas $ell_2$ norms see the
skew.

*Certification.* The 5-step Collatz--Wielandt bound is almost exact
(median $U_"cert"\/U = 1$, maximum $1.14$), and the wins survive it
(203 of 204), while the Schur bound alone is loose (median
$2.64 times$). So a certified $sigma$ is cheap to store and to trust.

*Kernel work.* $M <= U$ on all 3,124 queries, as @cor-kernel
guarantees; the median $M\/U$ is $1.5 times 10^(-4)$. Empirically the
stronger $max(M_R, M_S, M_T) <= U$ also held on every query, which
@prop-kernel does not guarantee. All worst-case bounds are far from
real outputs: the median of the best of the four bounds over $Out$ is
about $10^4$.

*A pre-registered success criterion.* Before running the experiment we
recorded a failure condition: if the certified $sigma$ is close to
$sigma$ but the certified bound is at least the $ell_2$ bound on over
$90%$ of real predicates, the spectral bound has no planner value. The criterion was stated
per predicate; we report it per predicate view and per query. A view is
a dataset, a predicate and, for the six SNAP graphs, the directed or
symmetrized variant. Counting a view as "no value" when
$U_"cert" >= ell_2$ on every query that uses it, 22 of 134 views qualify
($16%$; merging the two variants of each SNAP graph, 16 of 128
predicates); per query, $U_"cert" >= ell_2$
on $81.2%$ (2,537 of 3,124). So the criterion as registered is not
met. Against the stronger comparator $min(AGM, ell_2, "degree")$,
which we chose after the fact, $U_"cert"$ is not better on $93.5%$ of
queries (2,921 of 3,124), above the $90%$ threshold; 61 of 134 views
($46%$; 55 of 128 predicates with the SNAP variants merged) never see
$U_"cert"$ win. In spirit, then, the
criterion is met against the best prior bound. Our reading, for
the selected nonzero canonical queries: as a cardinality estimate, $U$
adds modest value as one more term in a
minimum with $ell_2$ and degree bounds, not as a replacement. Its main
value is the optimality guarantee of @sec-kernel, which needs no claim
about tightness on real data.

// =====================================================================
= Engine details and measurements <sec-engine>
// =====================================================================

The triangle operator in Leatherback, which at the time of writing is on
a development branch together with both admission stages below, answers
a run of exactly three

triple patterns forming a triangle with three distinct variables and
constant predicates, in any of the eight edge directions, the same
predicate allowed on every edge. Its contract is "exact or decline,
and no allocation": it returns exactly the bag the greedy left-deep
path would produce (in another order), or declines before any answer
is visible. The driver edge $E_1 = (x,y)$ is scanned in PSO order; the
other two edges are keyed by $y$ and by $x$ through PSO or POS, which
covers all eight directions; for each $E_1$ row the runs
$N_2 (y)$ and $N_3 (x)$ are found by monotone galloping and intersected
from the shorter side. Per $E_1$ row the operator's ideal candidate
budget is $min(|N_2 (y)|, |N_3 (x)|)$, so the budget summed over the
driver is $M_pi$; the entries it actually walks are at most this
budget, and can be fewer, because the walk stops when the other run is
exhausted. The operator's total work is the walked entries plus scan,
galloping and seek overheads. The Lean bridge of @sec-mech proves, for
a replica of the operator, that the precharged budget equals $M_pi$
and that the walked count is at most it; with three candidates on each
side it exhibits a row where the budget is $3$ and the walk reads one
entry.

*Planning today.* For each candidate driver the planner reads $64$
evenly strided $E_1$ rows (positions $floor(s |E_1| \/ 64)$,
$s < 64$), estimates
$hat(M) = floor(|E_1| dot "mean"(min(d_2, d_3)))$ from CSR degree
reads, and picks the driver minimizing $2|E_1| + hat(M)$; the $2|E_1|$
term blocks the star example of @prop-norot(a). Admission has two
stages. _Stage 1_: the
operator runs only when the three patterns together hold at least
$2048$ triples (the _floor_) and
$rho (2|E_1| + hat(M) + p) <= n_0 + hat(P)$ (the _gate_, $rho = 1$),
where $p$ is the proof price (the length of the ranges the kernel would
still have to certify; $0$ on a warm store), $n_0$ is the length of the
first pattern in the greedy plan's order and $hat(P)$ is the sampled
size of greedy's first $2$-path. _Stage 2_ (the _rescue_; at the time
of writing the kernel, both stages and the policy knob below are on a
development branch of Leatherback, not on its main branch): a triangle
that stage 1 declined on a warm stored view
is priced again in units calibrated on the knowledge-graph runs below
(one unit is about $2$ ns): with
$L_i = floor(log_2 (|E_i| \/ |E_1|))$ when $|E_i| > |E_1|$ and $0$
otherwise, and $f = 1$ when greedy's first join is on the first
pattern's object (so it probes per seed row instead of merging),
$
  K_L = |E_1| (4 + L_2 + 3 L_3) + 20 hat(M), quad
  G_L = n_0 (9 + 31 f) + 26 hat(P),
$
$
  K_S = |E_1| (8 + 2 L_2 + 6 L_3) + 30 hat(M), quad
  G_S = n_0 (9 + 31 f).
$
If $64 hat(P) >= n_0$, the driver minimizing $K_L$ is admitted when it
has at least $16384$ rows and $3 K_L <= 2 G_L$; failing that, the driver
minimizing $K_S$ is admitted when $K_S <= G_S$. Both minimums range
over all three candidates (ties to the lower position); a candidate
stage 1 left unsampled is sampled only while its zero-walk cost could
still change the decision, which leaves the decision equal to the rule
over all three. Nothing stage 1 accepted changes. @cor-kernel certifies the exact-$M$ choice and the
statistics-owner choice (the rotation owning the argmin term of $U$),
*not* the sampled estimator, and @prop-sampler shows that no estimator
that reads a fixed set of positions can be certified.

#proof(of: [@prop-sampler])[

  Take ordered constants $x_1 < dots.c < x_m$, $y_1 < dots.c < y_m$ and
  $z_0 < z_1 < dots.c < z_(2m-1)$. Since $R = X times Y$ is scanned in
  $(x, y)$ order, the row at position $q$ is
  $(x_(floor(q\/m)+1), y_((q mod m)+1))$. Let
  $J = {q mod m : q in P(m^2)}$, $j = |J|$, so $1 <= j <= k < m$, and
  call $y_i$ _dead_ when $i - 1 in J$. Put
  $Z_S = {z_0} union {z_(2i) : 1 <= i < m}$ and
  $Z_T = {z_0} union {z_(2i+1) : 1 <= i < m}$: two runs of length $m$
  that share only $z_0$ and interleave. Let
  $
    R = X times Y, quad
    S = {(y, z) : y "live", z in Z_S} union P_S, quad
    T = Z_T times X union P_T,
  $
  where $P_S, P_T$ are tuples on fresh constants that bring $S$ and $T$
  to $m^2 + 1$ tuples each and join nothing. The query lists its
  patterns as $R(x,y), T(z,x), S(y,z)$, so greedy's first join is
  the join of $R$ and $T$ on $x$. Then $d^+_S (y) = m$ for live $y$ and $0$ for dead
  $y$; $d^-_T (x) = m$ and $d^+_R (x) = d^-_R (y) = m$ on $X$ and $Y$;
  $d^+_T (z) = m$ on $Z_T$ and $d^-_S (z) = m - j$ on $Z_S$.

  (1) Every sampled row of $R$ has a dead $y$, so
  $min(d^+_S (y), d^-_T (x)) = 0$ and $hat(M)_R = 0$. Since
  $|S| = |T| = |R| + 1$, $2|R| + 0 < 2|E| + hat(M)_E$ for
  $E in {S, T}$, and the planner picks $R$. Every sampled $d^-_T (x)$ is
  $m$, so $n_0 + hat(P) = m^2 + m^3$, and the gate
  $rho dot 2m^2 <= m^2 + m^3$ holds for $rho <= (m + 1)\/2$.

  (2) $M_R = sum_((x,y) in R) min(d^+_S (y), d^-_T (x)) = m (m - j) m$.
  An $S$-tuple $(y, z)$ contributes to
  $M_S = sum min(d^+_T (z), d^-_R (y))$ only if $z in Z_T$, i.e.
  $z = z_0$: $m - j$ tuples with $min(m, m) = m$, so
  $M_S = m(m - j)$. Likewise $M_T = sum min(d^+_R (x), d^-_S (z))$ is
  carried by the $m$ tuples $(z_0, x)$, each with
  $min(m, m - j) = m - j$, so $M_T = m(m - j)$. The triangles are the
  $(x, y, z_0)$ with $y$ live, so $Out = m(m - j) = min_pi M_pi$. For
  each of the $m(m-j)$ live rows of $R$ the operator intersects
  $N_2 (y) = Z_S$ with $N_3 (x) = Z_T$; walking either run, every
  element below the other run's last element is read before that run is
  exhausted, which is at least $m - 1$ elements.

  (3) $2|R| + M_R >= m^2 (m - j) >= m^3 \/ 2$ for $j <= k <= m\/2$,
  while $2|S| + M_S = 2m^2 + 2 + m(m - j) <= 4m^2$; divide.
  Finally $N = |R| + |S| + |T| = 3m^2 + 2$, so $m = Theta(N^(1\/2))$.
]

#remark(name: "what the proposition does not cover")[
  The family is not semijoin-reduced (dead $y$'s and the padding join
  nothing), and the samples are placed without looking at the data.
  The construction with $64 | m$ and the stride, where $J = {0}$, was
  first found by a Codex CLI agent (GPT-6-Astra) during the search for
  the admission rule (@sec-ai); the golden-ratio grid it suggested as a
  fix is covered by the proposition. Exact counting
  ($O(sum_i r_i)$, the _exact_ policy) removes the failure at the
  planning cost measured in @tab-engine-kg. Randomized positions, grids
  chosen from the data, and semijoin-reduced inputs remain open
  (@sec-open).
]

*Possible extensions.* (i) Store per predicate, at compaction, the
certified $sigma$ together with sizes and maximum degrees, so the planner
can evaluate $U$ before reading data and use it as an admission or
deadline guard. (ii) Choose the driver by exact $M_pi$ when $E_1$ is
small after selection ($O(|R|)$ by the formula of @sec-prelim).
(iii) The per-binding variant of @sec-adapt with the unbuffered
price-then-run scheduler of @prop-ptr in its re-pricing variant
(@prop-ptr(4), $O(1)$ working memory), which is compatible with the
no-allocation contract; the earlier idea of running the three roots
round-robin with private output buffers is not, and is not used.

*Measurements.* The operator, on a development branch of Leatherback,
was compared with the greedy left-deep plan of the main branch at the
time: both ReleaseFast, each built from a clean source export with a
private compiler cache, three interleaved rounds of five
runs, medians of 15 in-process execution times on one machine. Answers
were identical in all 50 comparisons. The skewed workload is a
generated graph with Zipf($1.5$) degrees: the generator writes one
million edge statements, which deduplicate to 101,411 distinct stored
triples because the sampler repeats hub pairs. "Uniform" writes one
million statements with uniform degrees (999,983 distinct). Medians are
of in-process execution times; the speedups quoted in @sec-intro are
ratios of the displayed medians, $878.5\/27.3 = 8785\/273 approx 32.2$
for rows and $941.8\/8.29 = 94180\/829 approx 113.6$ for `COUNT(*)`,
i.e. $114 times$ after rounding. Seeds, data hashes, the raw samples
(1,200 timings), the answer comparisons and the machine (Apple M4 Max,
16 cores, 128 GiB, macOS 26.7, Zig 0.16.0) are in `artifacts/engine/`
of the paper repository, with the build, data-generation and
store-build commands (reconstructed from the logs after the runs). Once
Leatherback is public, the repository will name the engine versions
these runs correspond to.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, left, right, right, right),
    table.header[*Data*][*Query*][*Greedy*][*Operator*][*Ratio*],
    [skew, `.lb`], [triangle rows (466,168)], [878.5 ms], [27.3 ms], [0.031],
    [skew, `.lb`], [cyclic triangle rows (466,827)], [881.5 ms], [24.5 ms], [0.028],
    [skew, `.lb`], [triangle `COUNT(*)`], [941.8 ms], [8.29 ms], [0.009],
    [skew, in-memory], [triangle rows / `COUNT(*)`], [1046 / 1047 ms], [32.1 / 16.4 ms], [0.031 / 0.016],
    [uniform, `.lb`], [triangle rows (gate declines)], [41.3 ms], [42.4 ms], [1.03],
    [uniform, `.lb`], [triangle `COUNT(*)` (gate declines)], [69.3 ms], [68.6 ms], [0.99],
    [100k synth], [4-cycle `adv_cycle_quad` (not a triangle)], [381.5 µs], [381.6 µs], [1.00],
    [skew, `.lb`], [non-triangle chain], [21.8 ms], [22.9 ms], [1.05],
  ),
  caption: [Engine A/B, medians of 15 runs. On skewed data the operator
  replaces the wedge blow-up of the left-deep plan; where the planner's
  gate declines, the cost is the gate itself (largest relative change: a
  3.0 µs empty selective triangle became 4.9 µs).],
) <tab-engine>

*Driver policies on the knowledge-graph triangles.* To test what
@cor-kernel says about driver choice, a benchmarking-only planner knob
(the default is the planner above, and unit tests pin that its
plans are unchanged) runs each query under six policies: _sampled_ (the
default); _exact_, which counts $M_pi$ for every candidate driver with a
full degree pass charged to planning, takes the argmin of its objective,
and applies the same admission rules; _forced:k_ for each of the three
drivers, which skips the floor and the gate; and _greedy_, with the
operator disabled. There are two runs of the same harness.
_Run A_ (a development build of Leatherback with stage 1 only) has an
exact policy that minimizes $M_pi$ alone.
_Run B_ (a later development build) adds the
rescue, and its exact policy minimizes the planner's objective
$2|E_1| + M_pi$ and applies stage 1 and the rescue to the exact
budgets, so that against _sampled_ only the sampling error differs. The
queries are those of @sec-exp, run as `COUNT(*)`: all 871 CoDEx-L
queries, and samples of 120 sci50 and 250 wikidata5m queries, stratified
to equal counts per decile of $log M$ (seed 3313). The setup is
ReleaseFast on the machine above with one worker thread; each query has
an untimed probe and one untimed warm-up per policy, then 5 timed rounds
with the policies interleaved, and we report medians of elapsed times.
In each run answers agree across the six policies in all 7,446 (query,
policy) rows; the engine's exact $M_pi$ equals the independently
computed values of @sec-exp for every rotation of all 1,241 queries;
and $min_pi M_pi <= U$ holds on every query, as @cor-kernel requires
(median $min_pi M_pi \/ U$: $6.1 dot 10^(-4)$, $2.5 dot 10^(-3)$,
$4.2 dot 10^(-5)$; maximum $0.57$, $0.056$, $0.47$). In both runs one
greedy row on wikidata5m records the 30 s timeout rather than a
completed timing (the operator took 9.4 ms in run A); it is excluded
from every greedy ratio, which therefore understate the gap.

We distinguish three time measures. The _forced time_ of a driver is
the elapsed time of the run with that driver forced: planning, kernel
and result, not a metered count of kernel work. The _oracle_ is the
best forced driver, chosen after observing all three forced times; it
is not a deployable policy. _Sampled choice without the gate_ is the
forced time of the driver the sampled planner picks, i.e. what the
default planner would take if it never declined. We did not meter walked
entries in these runs; $M_pi$ is the model budget, computed exactly
from degree arrays.

#figure(
  text(size: 9pt, table(
    columns: (2fr, auto, 1.2fr, 1.2fr, 1.2fr),
    align: (left, center, right, right, right),
    table.header[*Quantity*][*Run*][*CoDEx-L (871)*][*sci50 (120)*][*wikidata5m (250)*],
    table.cell(colspan: 5)[_Driver choice_],
    [worst ÷ best forced driver (median / p90 / max)], [A], [2.7 / 8.6 / 47], [2.19 / 6.53 / 65.7], [4.99 / 28.2 / 132],
    [fastest forced driver = argmin $M_pi$ / argmin $2|E_1| + M_pi$], [A], [515 / 532], [71 / 71], [140 / 151],
    [#h(1em) same], [B], [518 / 586], [68 / 84], [140 / 168],
    [exact pick ≠ sampled pick, exact by $M_pi$], [A], [405 (46.5%)], [53 (44.2%)], [126 (50.4%)],
    [exact pick ≠ sampled pick, exact by $2|E_1| + M_pi$], [B], [55 (6.3%)], [6 (5.0%)], [8 (3.2%)],
    [fastest forced driver = sampled / exact pick], [A], [517 / 501], [66 / 62], [147 / 139],
    [#h(1em) same], [B], [599 / 618], [86 / 83], [169 / 171],
    [forced-time gain of the exact pick (median / p90; min / max)], [A], [1 / 1.56; 0.093 / 7.19], [1 / 1.27; 0.293 / 14.2], [1 / 2.15; 0.024 / 15.2],
    [#h(1em) same], [B], [1 / 1; 0.352 / 6.50], [1 / 1; 0.295 / 5.55], [1 / 1; 0.499 / 5.49],
    [exact ÷ sampled time, end to end (median / p10)], [A], [26.2 / 7.9], [39.1 / 7.3], [69.8 / 8.7],
    [#h(1em) same], [B], [36.5 / 10.7], [62.8 / 22.7], [90.1 / 12.7],
    table.cell(colspan: 5)[_Admission (stage 1)_],
    [stage-1 declines (sampled / exact)], [A], [571 / 617], [87 / 102], [166 / 191],
    [#h(1em) same], [B], [571 / 561], [87 / 88], [166 / 163],
    [greedy ÷ operator, all queries (median / p90)], [A], [1.05 / 26.7], [1.06 / 13.2], [1.21 / 36.5],
    [greedy ÷ operator where accepted (n; median / p90 / min)], [A], [300; 10.1 / 153 / 1.23], [33; 8.76 / 80.9 / 1.23], [83; 10.2 / 751 / 0.508],
    [declined: greedy ÷ sampled choice without the gate (median / p90)], [A], [1.40 / 3.38], [2.20 / 9.78], [2.06 / 15.9],
    [#h(1em) of those, $> 1.5 times$], [A], [262/571], [64/87], [105/166],
    [declined: greedy ÷ oracle (median / p90)], [A], [1.83 / 3.92], [2.8 / 14.9], [3.53 / 20.2],
    [#h(1em) of those, $> 1.5 times$], [A], [350/571], [70/87], [116/166],
  )),
  caption: [Driver policies on the knowledge-graph triangles of @sec-exp
  (`COUNT(*)`, medians of 5 interleaved rounds). Run A: exact policy
  $= "argmin" M_pi$, stage 1 only. Run B: exact policy
  $= "argmin" (2|E_1| + M_pi)$, rescue
  live; in run B "pick" is the driver that ran, which on rescued queries
  is the rescue's choice for both policies. "Forced-time gain" is the
  forced time of the sampled pick divided by that of the exact pick;
  each row compares times within its own run. Greedy ratios exclude
  the one greedy timeout.],
) <tab-engine-kg>

@tab-engine-kg answers three questions. _Does exact pricing change the
plan?_ Only when it prices something else. Minimizing $M_pi$ alone
(run A) picks a different driver than the sampled planner on 44--50%
of queries; minimizing the planner's own objective $2|E_1| + M_pi$
(run B) does so on 3--6%, and on 23 of 281, 1 of 30 and 4 of 76 of the
queries both policies admit at stage 1. Most of run A's disagreement
was the objective, not sampling error. _Does that help?_ Not on this
workload, descriptively (we did no uncertainty analysis): in run B the
forced-time gain of the exact pick has median and p90 exactly $1$
(minimum $0.30$--$0.50$, maximum $5.5$--$6.5$), and the exact pick is the fastest forced
driver about as often as the sampled one (618 vs 599, 83 vs 86, 171 vs
169). End to end the exact policy is $36.5$--$90.1 times$ slower at the
median (run B), because its three full degree passes dominate these
mostly sub-millisecond queries. So @cor-kernel's guarantee for the
exact choice holds on every query here, and the sampled estimate does
as well on this workload, although @prop-sampler shows it has no
worst-case guarantee. _Is rotation the right lever?_ The forced-driver
spread says the driver matters (worst over best: median $2.2$--$5.0
times$, up to $132 times$), and where stage 1 admits the operator it
beats the greedy plan by a median $8.8$--$10.2 times$ (one regression,
$0.51 times$, on wikidata5m). Admission, not driver choice, was the
binding constraint: stage 1 sends 66--73% of queries to greedy. On
those, the oracle would have beaten greedy by a median
$1.8$--$3.5 times$ and by more than $1.5 times$ on 61--80% of them, but
the oracle is not a policy. The deployable comparison is the sampled
choice without the gate: a median $1.40$--$2.20 times$ faster than
greedy, and more than $1.5 times$ faster on 46--74% of the declined
queries. That is the opportunity the rescue stage below goes after.

Caveats. Most CoDEx-L runs take $0.1$--$1$ ms, which is noisy at the
scale of driver choice; restricted to queries whose fastest forced run
took at least 1 ms, the fastest driver in run A is the argmin of
$M_pi$ on 3/7, 40/53 and 59/93 queries and of $2|E_1| + M_pi$ on 6/7,
32/53 and 54/93. The wikidata5m process peaked at a footprint of
85.6 GB in run A and 91.7 GB in run B (the peak memory footprint
reported by the operating system for the whole benchmark process),
from greedy's materialized 2-paths; the operator itself allocates
nothing per row. On this graph the left-deep plan therefore costs
memory as well as time, and the timing ratios do not show that cost. The raw rows, queries, scripts and a summary that the
scripts rebuild are in `artifacts/engine-kg/`.

*The rescue stage.* The two sides of stage 1 count different units:
a greedy unit is a materialized $2$-path row, a kernel unit a scanned
edge, a seek or a walked entry. On run A, per-unit medians were 29, 62
and 57 ns for greedy and 7.4, 4.3 and 5.8 ns for the kernel, so stage 1
is several times too kind to greedy. Loosening its ratio does not
separate the declined queries the kernel wins from those it loses; two
structural signals do. One is the depth of the kernel's per-row seeks
into $E_2$ (the $L_i$ terms). The other is whether greedy's first join
probes per seed row (the $f$ term). The rule (see _Planning today_) was chosen by an
offline search over run A's rows for the most total time saved subject
to at most two regressions above $1.2 times$ per dataset and none above
$1.5 times$ (the rule chosen had a worst slowdown of $1.26 times$ on
those rows). @tab-rescue measures it in a third run.

_Run C_ (a development build that contains the pruning fix described
below) adds a bench-only policy _stage1_: the
same sampled estimate and stage-1 gate, with no rescue, i.e. the
planner before the rescue. It runs in the same process as the other
six policies on the same queries, with 6 timed rounds, and the order of
the seven policies is shuffled in every timed round (seeded by the query
id). A first, fixed-order run showed a position bias: _stage1_ always
ran right after _sampled_ and was a median 5--8% faster on queries where
both run the identical plan, which produced 74, 12 and 36 spurious
"regressions" above $1.2 times$; we report only the shuffled run. In
run C the stage-1 decision (outcome and driver) of _sampled_ equals the
_stage1_ arm's on every query, so the two arms differ only on the
rescued queries. An earlier draft reported this comparison against an
imputed baseline (run B, with the stage-1 time of a rescued query
reconstructed from greedy's time): totals $189.9 -> 144.8$,
$1004.0 -> 546.7$ and $1839.4 -> 1270.2$ ms. The measured numbers of
@tab-rescue replace them.

#figure(
  text(size: 9pt, table(
    columns: (1.6fr, 1fr, 1fr, 1fr),
    align: (left, right, right, right),
    table.header[*Quantity (run C)*][*CoDEx-L (871)*][*sci50 (120)*][*wikidata5m (250)*],
    [admitted at stage 1 / rescued / declined], [300 / 216 / 355], [33 / 52 / 35], [84 / 43 / 123],
    [decline rate, stage 1 → both stages], [65.6% → 40.8%], [72.5% → 29.2%], [66.4% → 49.2%],
    [total ms, stage 1 → both stages (measured)], [173.6 → 137.9 (−20.6%)], [1041.2 → 532.6 (−48.8%)], [1959.0 → 1322.3 (−32.5%)],
    [speedup over stage 1, all queries (median / p90 / max)], [1.01 / 5.30 / 24.6], [1.11 / 8.37 / 30.5], [1.02 / 4.80 / 153],
    [rescued queries: total ms, stage 1 → rescue], [52.8 → 17.2], [837.1 → 331.4], [735.6 → 99.6],
    [rescued queries $> 1.2 times$ slower (worst ratio)], [0 (1.14)], [0 (1.07)], [0 (0.78)],
    [unchanged plan: both-arm time ratio (median)], [1.000], [1.005], [1.002],
    [#h(1em) $> 1.2 times$ slower (noise floor)], [22 / 655], [2 / 68], [12 / 207],
    [exact policy ($2|E_1| + M_pi$): rescued / declined], [255 / 306], [59 / 29], [61 / 102],
    [answer-equality flags set across policies], [6097/6097 rows], [840/840 rows], [1750/1750 rows],
  )),
  caption: [The rescue stage on the knowledge-graph triangles against
  the stage-1 planner measured in the same run (run C; medians of 6
  rounds with the policy order shuffled per round). The median speedup is about $1$ because 57--83% of queries
  keep their stage-1 plan; the gains sit in the rescued 17--43%.
  "Unchanged plan" are the queries stage 1 admits or both stages
  decline: both arms run the identical plan there, so their ratios
  measure run-to-run noise (plus, on declined queries, the rescue's
  extra sampling). Worst ratio is rescue time over stage-1 time.
  wikidata5m includes all 250 queries (the greedy timeout affects only
  the greedy arm). The rule was fitted to these queries: the gains are
  in-sample.],
) <tab-rescue>

The rule is in-sample: it was searched on the same 1,240 queries it is
measured on (the 1,241 less the wikidata5m query whose greedy run timed
out), so @tab-rescue shows that it does what it was fitted to do
on a fresh execution, not that it generalizes. In run B, which carried
the forced-driver arms under the same rule, rescued queries ran within
a median $1.02$--$1.15 times$ of the oracle (p90 $1.32$--$2.24$). The only out-of-sample
check is the three synthetic stores of @tab-engine (skewed, uniform,
and a 100k "medium" store), where every decision and driver is
unchanged and the sorted answers are identical in 21 of 21 (store,
query) pairs. In a shuffled 10-round run of these stores the rescue
arm over the stage-1 arm is $0.99$--$1.03$ on every query above 1 ms;
the exceptions are sub-200 µs queries (a $4.7$ vs $9.0$ µs pair with
an identical plan that we cannot explain, and the medium store's two
declined triangles, $1.04$ and $1.10$, which pay the rescue's
sampling). An earlier draft reported a $1.058 times$ slowdown on the
uniform `COUNT(*)` query of about 54 ms from a single old and new run.
Rerun as
10 alternating process pairs of the pre-rescue and the fixed binary,
5 runs each, the per-pair ratio has median $0.995$ (range
$0.970$--$1.024$; the new binary slower in 4 of 10), and the pooled
medians are $52.48$ and $52.58$ ms ($1.002$, run-to-run standard
deviation about $1.5$ ms): the $1.058$ did not reproduce. These checks
show the rescue does not change decisions there; they do not test the
gains.

_Candidate pruning._ To avoid sampling hopeless candidates, the
implementation measured in run B skipped a candidate whose zero-walk cost
floors already failed, and treated a candidate below the $16384$-row
minimum as unable to pass the large branch. The searched rule instead
takes the large-cost argmin over all candidates and applies the minimum
afterwards, so a small candidate can win the argmin and veto a larger
one. A model-run audit (Codex CLI with GPT-6-Astra; @app-verify) built
a realizable 31,000-tuple warm-store instance (sizes
$1000, 10000, 20000$, no triangles) on which that implementation admits
the third driver while the all-candidate rule declines (answers were
unaffected). The fix replaces the pruning: a candidate is sampled while
its zero-walk floor could still
take a branch's argmin within that branch's budget, so the decision is
the rule over all three candidates, for at most two extra samples. A
second model-run audit (a Claude subagent) re-derived this from the
code, matched a port of it against the full rule on $2.8 dot 10^6$
exhaustive and random cases, and confirmed that the first audit's
instance, added as a test, fails on the earlier implementation and
passes on the fix. On the knowledge-graph queries the fix

changes one decision: codex-l-0267, which the pruned rule rescued
($145$ µs against greedy's $1.67$ ms), is now declined ($1.60$ ms),
because its 8,023-row candidate wins the large argmin and fails the
$16384$-row minimum. That is the searched rule as written; it shows the
cost of applying the minimum after the argmin. By design
the rescue never runs on a cold store (proof price $> 0$) or on the
in-memory graph arm, whose probe-first join is a postings lookup. The
machine carried other load throughout (load average 11--17 on 16
cores in runs A and B, 9--14 in run C); every comparison is within one
run with the policies interleaved per query, and greedy's median time
drifted by a factor $1.03$, $1.01$ and $0.98$ between runs A and B. The
wikidata5m process peaked at a footprint of 116 GB in run C. What is
left after the rescue is smaller but not zero: in run B, on the queries
both stages still decline, the sampled choice without the gate beats
greedy by more than $1.5 times$ on 106, 19 and 67 of them.

*The engine's intersection routine in the sorted model.*

#remark(name: "the engine's routine on relabelled G8")[
  The engine's `intersectEachBy` (`src/util/sorted_runs.zig`) walks the
  shorter run and, on equal lengths, its first argument; the triangle
  call site passes the run of the walked tuple's far endpoint first, so
  option $R$ calls $(Z_1, T(dot, x))$ and option $T$ calls
  $(Y_(2,z), Y_0)$. On an alternating pair of length-$s$ runs its
  routine (a 16-step linear prefix, then doubling, then binary search)
  performs $6s - 3$ key predicates in the walking-first orientation
  ($(s - 1)$ lookahead equalities, $2s - 1$ disorder checks, $2s - 1$
  gallop comparisons and $s$ match equalities) and $6s - 5$ reversed,
  with work meter $3s - 1$ either way. On $cU(m)$ relabelled as in
  @thm-sorted-g8, per $x$ it costs $q_R (x) = 6m^5 - 2m^2$ and
  $q_T (x) = 6m^5 + m^4 - 4m^3$ (comparisons plus outer visits); the
  optimum picks $T$ at $m = 2, 3$ and $R$ for $m >= 4$, and each root
  costs $Q(m) = m^4 min(q_R, q_T) + m^8 + m^5 = 3104, 122715, 1631232, 12081250$
  for $m = 2, dots, 5$, i.e. $Q(m) = 6m^9 + m^8 - 2m^6 + m^5$ for
  $m >= 4$: an exact degree-$9$ polynomial against $N$ of degree $8$.
  These are modelled per-binding optima of the port's counts with
  omniscient plan choice; relation seeks, sorting and planning are
  excluded, and the engine itself runs one sampled driver
  (@sec-engine), so this confirms the exponent, not an engine timing.
] <rem-engine-port>
#st[#proved (exact counts from a port of the engine routine; @app-verify)]


Not reported: the per-binding scheduler of @prop-ptr (not
implemented), the @thm-sep families at scale, first-row and p99
latency (the operator keeps no output buffer, but price-then-run
delivers its first row only after pricing), metered kernel work split
into pricing and execution (all times above are elapsed times), and
any out-of-sample workload for the rescue stage.

// =====================================================================
= Price-then-run, and degree metadata <app-ptr>
// =====================================================================

== Price-then-run: paying for the statistics <sec-ptr>

The per-binding choice needs $c^*(u)$, which is not known in advance.
In a sorted-permutation store every degree is an $O(1)$ offset read,
so both options can be priced without executing them.

*Lockstep pricing at one binding.* Let $P, Q$ be the two options at
binding $u$. Read the two degrees of $u$ that the per-edge costs need.
Reveal the per-edge costs of the two options one at a time; each
_advance_ is one neighbour read and one degree read ($2$ unit
operations, one per-edge unit). Keep running sums $t_P, t_Q$. Always
consider the option with the smaller running sum (ties to $P$; a
completed option's running sum is its total): if it is complete, stop
and choose it; otherwise advance it. Bindings are enumerated by merging
the key lists of the two CSR indexes, at one unit per binding.

#lemma(name: "lockstep pricing")[
  At a binding $u$ with option costs $c_P (u), c_Q (u)$, lockstep
  pricing chooses an option of cost exactly $c^*(u)$ after at most
  $min(2c^*(u) + 1, thick d_P (u) + d_Q (u))$ advances, where
  $d_P (u), d_Q (u)$ are the numbers of tuples the two options walk. At
  any intermediate moment, $min(t_P, t_Q) <= c^*(u)$ and at most
  $2 min(t_P, t_Q) + 1$ advances have been made.
] <lem-lockstep>
#st[#proved]

#proof[
  Every per-edge cost is at least $1$, and $t_P <= c_P$, $t_Q <= c_Q$.
  At any moment let $m = min(t_P, t_Q)$. The side holding $m$ was
  advanced at most $m$ times. Each advance of the other side started
  from a running sum at most the first side's running sum at that time,
  hence at most $m$; these starting values are distinct integers in
  $[0, m]$, so there are at most $m + 1$ of them. When the procedure
  stops, the chosen total is at most the other running sum, hence at
  most the other total, so it equals $c^*(u) = m$. Each advance also
  consumes a fresh tuple.
]

*The scheduler.* Run one lockstep pass per root $v in {x, y, z}$ over
the bindings of $v$, interleaved as follows. Pass $v$ maintains the
lower bound
$
  L_v = sum_("finished bindings" u) c^*(u) + min(t_P, t_Q)_("current binding"),
$
which never decreases and satisfies $L_v <= C_v$, with equality once
pass $v$ is finished. Fix the order $x < y < z$ of the roots. At each
step, take the pass whose key $(L_v, [v "unfinished"], v)$ is
lexicographically smallest: the smallest $L_v$, ties going to a
finished pass, and remaining ties to the earlier root. If it is
finished, stop and call it $v^*$; otherwise perform one step of it (one
advance, or finishing a binding and reading the degrees of the next).
Then execute the recorded option at every binding of $v^*$.

#proposition(name: "price-then-run")[
  With $O(1)$-time degree reads, the scheduler above satisfies:
  + $C_(v^*) = C$.
  + Every triangle is output exactly once.
  + In per-edge cost units, the total work is at most
    $C + min(6C, 2N) + 4n + O(1)$, where $n = n_x + n_y + n_z <= 2N$.
    In particular it is at most $7C + O(n)$ and at most $C + O(N)$. In
    the unit operations of @sec-prelim it is at most
    $2C + min(12C, 4N) + O(n)$.
  + It is deterministic and uses no sampling. Since $v^*$ is known only
    when the scheduler stops, every pass records its chosen options
    while pricing: one bit per priced binding, at most $n <= 2N$ bits in
    total. A finished pass $v$ may discard its bits once another
    _finished_ pass $v'$ beats it in the stop rule's order, i.e.
    $(C_(v'), v') < (C_v, v)$ lexicographically: a strictly smaller
    total, or an equal total and an earlier root. Such a $v$ is never
    $v^*$, because $v'$ stays finished with $L_(v') = C_(v')$ and so has
    a smaller key than $v$ at every later step. The non-strict rule
    "another finished pass has a total no larger than its own" is unsafe:
    two finished passes with equal totals would each discard their bits
    because of the other. A finished pass that is merely no longer
    minimal may still win, because an unfinished pass with smaller
    $L_v$ can later rise above it (e.g. a finished pass with
    $L_A = C_A = 10$ and an unfinished one with $L_B = 9 < C_B = 20$:
    $A$ wins once $L_B$ passes $10$). The bits of the losing passes are
    discarded at the end. The variant
    that re-prices $v^*$
    instead uses $O(1)$ working memory and adds at most
    $min(2C, 2N) + O(n_(v^*))$ per-edge units. Neither needs an output
    buffer, and both serve enumeration and counting alike.
  + Pricing every root fully before running (no scheduler), then
    re-pricing and executing the root with the smallest priced total,
    is also correct and costs at most $2C + 15N$ unit operations with
    $O(1)$ working memory.
] <prop-ptr>
#st[#proved (simulated on random instances; @app-verify)]

#proof[
  (1) When the scheduler stops,
  $C_(v^*) = L_(v^*) <= L_v <= C_v$ for every root $v$.

  (2) Every triangle has exactly one vertex in the root variable, and
  either option at that vertex finds every triangle through it, once.

  (3) A step of pass $v$ is taken only when
  $L_v <= min_(v') L_(v') <= C$. By @lem-lockstep, before its last step
  pass $v$ has made at most $sum_("finished" u) (2c^*(u) + 1) + 2 m + 1 <= 2 L_v + n_v + 1$
  advances, plus three units per binding for enumeration and degree
  reads. So pricing costs at most $sum_v (2C + 4n_v + O(1)) = 6C + 4n + O(1)$.
  Each pass is a prefix of full lockstep pricing, which by
  @lem-lockstep makes at most $d_P (u) + d_Q (u)$ advances per binding;
  each relation is walked by two roots, so all advances total at most
  $2N$. Execution costs $C_(v^*) = C$ per-edge units, i.e. at most $2C$
  unit operations, and each advance is $2$ unit operations.
  $n <= 2N$ because every binding with an incident tuple is an endpoint
  of one.

  (4) Re-pricing $v^*$ repeats its pass alone: at most
  $sum_u (2c^*(u) + 1) <= 2C + n_(v^*)$ advances, and at most
  $|P_(v^*)| + |Q_(v^*)| <= N$, plus overhead $O(n_(v^*))$.

  (5) Pricing root $v$ fully, whose options walk relations $P_v, Q_v$,
  costs at most $sum_u (3 + 2(d_P (u) + d_Q (u))) <= 3 n_v + 2(|P_v| + |Q_v|)$
  unit operations by @lem-lockstep; summed over the three roots this is
  at most $6N + 4N = 10N$. Re-pricing $v^*$ costs at most
  $3 n_(v^*) + 2(|P_(v^*)| + |Q_(v^*)|) <= 5N$, and executing it at most
  $2C$. The total is at most $2C + 15N$.
]

#remark(name: [constants, and why the minimum-$L$ rule matters])[
  The constant $6$ in (3) is tight for this scheduler (this argument is
  from the GPT-5.6-sol Pro review of the first draft, @sec-ai): on the
  union of
  three rotations of an instance with complete $R = X_p times Y_q$,
  complete $T$ between $Z_q$ and $X_p$ and empty $S$, every $C_v$
  equals $C$, and measured pricing$\/C$ is $7.97$, $6.50$, $6.25$ at
  $p = q = 8, 32, 64$, tending to $6$. This is exact, not only
  measured: since all three roots have the same final cost $C = p q$,
  the minimum-$L$ rule cannot stop before every $L_v$ reaches $C$, and
  each binding's two unit-cost options of length $q$ take $2q$ lockstep
  advances, so each root needs $2C$ advances and pricing needs $6C$ plus
  lower-order binding overhead. On random instances the worst
  measured $("pricing" - 4n)\/C$ in the runs of
  `artifacts/verify/thm1/rnd.py` was between $3.0$ and $3.5$; an
  outside re-implementation (@app-verify) found $3.00$, $3.20$ or $4.00$
  on the same 3,996 random instances, depending on the order in which
  a binding's tuples are walked (a set iteration order that varies with
  Python's per-process string hashing).
  The point of the scheduler over (5) is that pricing is bounded by
  $O(C + n)$ rather than $O(N)$: with $R = X times Y$, $T$ complete
  between $Z$ and $X$ ($m times m$ each) and $S$ a single stray tuple,
  $C = 0$ and $N = 2m^2 + 1$. Counting one unit per advance and three
  per binding started (enumeration and the two degree reads, as in the
  proof of (3)), at $m = 4, 8, 16, 32$ the scheduler's pricing was
  $26, 38, 62, 110$ units ($3m + 14 = Theta(sqrt(N))$), where pricing
  every root fully cost $77, 213, 677, 2373$ ($Theta(N)$). Here the stray
  tuple is $(y_0, z')$ with $z'$ a fresh vertex. The rule "stop at the first pass
  to finish" is not a substitute for the minimum-$L$ rule: under
  round-robin it selected a root with $C_v > C$ on about $31%$ of
  random instances. With execution-only access (costs unknown until
  paid), the usual two-option adversary forces a factor close to $2$;
  we do not prove this here. The point of @prop-ptr is that $O(1)$ CSR
  degree reads make the per-binding choice cost only a constant factor,
  or an additive $O(N)$, beyond $C$.
] <rem-ptr>

== Degree metadata alone is the wrong class <sec-ferrers>

One might hope to prove optimality against the worst output over all
instances sharing the labeled degree sequences of the input. That class
is too fine.

#proposition(name: "Ferrers profiles")[
  For every $k >= 1$ there is an instance with $N = 9 k^2$ in which each
  of $R, S, T$ is the unique relation with its labeled degree sequences,
  $Out = 0$, and $C = k^3 + k^2$, $min(M_R, M_S, M_T) = k^3$, while all
  six squared-degree sums equal $5k^3$, so $B_2 = 5k^3$. So neither
  $C$ nor $min_pi M_pi$ is bounded by $c (N + max Out)$ for a constant
  $c$, the maximum taken over the instances with the same labeled
  degrees, whereas $C = Theta(N + B_2)$ here.
] <prop-ferrers>
#st[#proved]

#proof[
  Split each of $X, Y, Z$ into three blocks of size $k$ (indices
  $0, 1, 2$) and let each relation be a union of complete block pairs:
  $R = X_1 times Y_2 union X_2 times Y_1 union X_2 times Y_2$,
  $S = Y_1 times Z_1 union Y_1 times Z_2 union Y_2 times Z_2$,
  $T = Z_0 times X_1 union Z_1 times X_1 union Z_0 times X_2$.
  The row neighbourhoods of each relation are nested ($R$:
  $emptyset subset Y_2 subset Y_1 union Y_2$; $S$:
  $emptyset subset Z_2 subset Z_1 union Z_2$; $T$:
  $emptyset subset X_1 subset X_1 union X_2$), so no $2 times 2$
  interchange (pairs $u_1 v_1, u_2 v_2$ present with $u_1 v_2, u_2 v_1$
  absent) exists. By Ryser's interchange theorem
  [#cite(<ref-ryser>)[Rys57]] all 0/1 matrices with given row and
  column sums are connected by interchanges, so each relation is the
  unique realization of its labeled degrees. $Out = 0$: from $X_1$ the
  path goes to $Y_2$, then $Z_2$, but $T$ enters $X_1$ only from
  $Z_0 union Z_1$; from $X_2$ it reaches $Z_1 union Z_2$, but $T$ enters
  $X_2$ only from $Z_0$. Degrees: $d^+_R = k, 2k$ on $X_1, X_2$;
  $d^-_R = k, 2k$ on $Y_1, Y_2$; $d^+_S = 2k, k$ on $Y_1, Y_2$;
  $d^-_S = k, 2k$ on $Z_1, Z_2$; $d^+_T = 2k, k$ on $Z_0, Z_1$;
  $d^-_T = 2k, k$ on $X_1, X_2$; all others $0$. Each degree sequence
  is one block of $k$ vertices of degree $k$ and one of degree $2k$, so
  each squared sum is $k^3 + 4k^3$. Hence $M_R = 3k^3$,
  $M_S = k^3$ (only $Y_1 times Z_1$ contributes), $M_T = k^3$ (only
  $Z_1 times X_1$). Root $x$: on $X_1$, $c_R = k(1+k)$,
  $c_T = k + k(1+k)$; on $X_2$, $c_T = k$; so $C_x = k^3 + 2k^2$.
  Root $y$: on $Y_1$, $c^* = k(1+k)$; on $Y_2$, option $S$ costs $k$;
  $C_y = k^3 + 2k^2$. Root $z$: $Z_0$ has no $S$-tuples and $Z_2$ no
  $T$-tuples (cost $0$); on $Z_1$ both options cost $k(1+k)$; so
  $C_z = k^3 + k^2 = C$.
]

This is why @thm-pb-upper and @thm-pb-lower measure $C$ against $B_2$
rather than against the worst output per degree profile. A side remark
for engines: when every slice's CSR offsets form a nested (threshold)
degree sequence, the instance, and so $Out$, is determined by the
metadata.

// =====================================================================
= Mechanization <sec-mech>
// =====================================================================

The Lean package `LeatherbackSpectral` (Lean 4 [#cite(<ref-lean>)[dMU21]]
v4.32.2, mathlib [#cite(<ref-mathlib>)[Mat20]] tag v4.32.2) was written
in Leatherback's Lean workspace, which is otherwise Std-only (a check
there enforces that only this library imports mathlib), and is
published with this paper (@sec-artifacts). It has nine modules
(`Basic`, `OpNorm`, `Upper`, `Kernel`, `Lower`, `Matrix01`,
`Degenerate`, `KernelBridge`, `Sharp`; about 1,770 lines in total) and
builds with `warningAsError` and `autoImplicit = false`.

*Model.* Vertex sets are `Fintype`s with decidable equality; relations
are `Finset`s of pairs; `adj R : Matrix X Y ℝ` is the 0/1 incidence
matrix; `out R S T := trace (adj R * adj S * adj T)` (with
`out_eq_card` identifying it with the triangle count); the norm is
mathlib's $ell_2$ operator norm on matrices
(`Matrix.instL2OpNormedAddCommGroup`); `Stats` holds the six reals,
`Stats.U` is the nested minimum of the nine terms, and `Admissible` is
the six inequalities. `kernelWork R S T` is $M_R$.

*What is checked.*
- Upper bound: `theoremB_upper` (all nine terms, constant $1$), built
  from `bilinear_le`, `rowDeg_le_opNorm_sq`, `colDeg_le_opNorm_sq`,
  `opNorm_adj_sq_le_card` (Frobenius), `opNorm_adj_le_schur` (Schur
  test), `out_le_opNorm_mul_sqrt` and the rotation lemmas; and the same
  for arbitrary 0/1 matrices (`theoremB_upper_matrix`).
- Lower bound: `theoremB_lower` (the floored block instance is
  admissible and $U < 4 dot Out$), with `card_blk`, `opNorm_blk_eq`,
  `out_blk`, `Stats.real_shape_feasible`, `Stats.real_shape_value`,
  `Stats.real_shape_attains_U`, `Stats.block_params`; and `theoremB`,
  their conjunction.
- Sharp constant (@thm-sharp, module `Sharp`): `sharpStats_regular`,
  `sharpStats_U`, `sharpStats_out_le_one`, `sharpStats_witness`,
  `sharp_family`, `factor_four_sharp` (for every $epsilon > 0$, regular
  statistics with every admissible $Out <= 1$, an admissible instance
  with $Out = 1$, and $U > 4 - epsilon$) and `theoremB_constant_sharp`
  ($inf W\/U = 1\/4$ in two-sided form, without forming $W$).
- Degenerate regime: `theoremB_degenerate` (no sign condition assumed;
  vacuous when a bound is negative), `admissible_exists_iff_nonneg`,
  `theoremB_degenerate_attained`, `opNorm_adj_empty`, and
  `theoremB_cases`, whose statement includes the universal upper bound
  together with the regular lower witness or the nonregular
  zero-output alternative.
- Kernel: `kernelWork_eq_out_nest` (@lem-nest), `out_le_kernelWork`,
  `kernelWork_le_terms` (@prop-kernel), `kernel_min_le_U`
  (@cor-kernel), and the counterexample `nestS_can_raise_opNorm`.
- Kernel bridge (`KernelBridge`): the engine's Std-only Lean workspace
  contains an executable replica of the triangle kernel with three
  counters. `model` is an _ideal precharged candidate budget_: before
  each $E_1$ row is processed it is incremented by
  $min(|N_2 (y)|, |N_3 (x)|)$. `walked` counts the entries of the chosen
  run that the replica actually consumes, and `charged` additionally
  counts galloping steps and seeks. The workspace proves that `model`
  equals a list-based sum `kernelWorkNat`, and
  $"walked" <= "model"$ (`run_walked_le_model`).
  `kernelWorkNat_eq_kernelWork` and `kernelWorkNat_eq_kernelWork_fin`
  identify that sum with `kernelWork`, and `run_model_eq_kernelWork`
  concludes that the budget `model` equals $M_R$ on sorted,
  duplicate-free, bounded edge lists, for a result sink that never
  stops the walk. `run_model_le_terms` and `run_model_le_opNorm`
  transfer the five $R$-driven bounds of @prop-kernel to `model`, and
  `run_walked_le_kernelWork_real` and `run_walked_le_terms` give
  $"walked" <= M_R$ and the same five bounds for `walked`. Equality
  $"walked" = "model"$ is *false* in general. With
  $E_1 = [(0,0)]$, $E_2 = [(0,100), (0,101), (0,102)]$ and
  $E_3 = [(0,1), (0,2), (0,3)]$ (sorted, duplicate-free) the replica
  precharges $"model" = 3 = M_R$, but its tie rule walks $E_2$, reads
  only $100$, gallops $E_3$ to its end and stops with $"walked" = 1$
  (`walked_lt_model_example`, proved by `decide +kernel` in the Std-only
  workspace, axioms `propext` and `Quot.sound` only). So the bridge
  identifies $M_R$ with a conservative budget and bounds the entries
  actually read by it; it proves no bound on `charged`, which includes
  the galloping and seek overheads.

*Hygiene.* No `sorry`, `admit`, `native_decide` or custom axiom occurs.
`LeatherbackSpectralAudit.lean` runs `#print axioms` on 80 declarations,
each inside `#guard_msgs` expecting exactly
`[propext, Classical.choice, Quot.sound]`, so the build fails if any
of them acquires `sorryAx` or `Lean.ofReduceBool`; the Std-only audit
`LeatherbackAudit.lean` checks the replica's `run_walked_le_model`,
`run_walked_le_kernelWork` and `walked_lt_model_example` in the same
way.

*Building it.* An early archive of the Lean sources, supplied to the
first model-based review (@sec-ai), contained only the spectral sources
and `lakefile.lean`, without `lean-toolchain`, `lake-manifest.json` or
the sources of the workspace's other default targets, so it could not
be built on its own. The paper repository instead carries the Lean
workspace with every source the spectral library and the replica
import. It pins Lean with `lean-toolchain`
(`leanprover/lean4:v4.32.2`) and mathlib with `lake-manifest.json`
(mathlib tag `v4.32.2`, with its dependencies). With `elan` installed,
`lake exe cache get` followed by
`lake build LeatherbackSpectral LeatherbackSpectralAudit` kernel-checks
every spectral module and the audit; the repository's README gives the
commands for the replica's audit and the full workspace check. The
spectral library, both audits and the full workspace built with exit
code $0$ on 2026-10-09; no Lean source changed after that build.

*What is not checked.* $W$ is not a Lean object: @thm-main appears as a
universal upper bound and an existential instance, and its
feasibility sentence is checked only at $V = U$. Not
formalized: @prop-norot, @cor-single, all of @sec-adapt (@lem-sum, @lem-perroot,
@thm-pb-upper, @cor-pb, @thm-pb-lower, @cor-l2-false, @lem-pad,
@thm-pb-slopes, @thm-sep, @lem-lockstep, @prop-ptr, @prop-ferrers),
@sec-background, @rem-witness, the footnote on nuclear norms in
@sec-main, and the experiments. The Zig code itself is not verified: the correspondence
between the Lean replica and `triangle_join.zig` is trusted, as are the
Zig planner's sampled cost estimator, the $O(sum r_i)$ overhead and the
galloping log factor (analysed on paper in @sec-sorted). The model has
set semantics only; bag semantics is out of scope.

*Other paper-only results.* Also not in Lean:
@cor-twonorm, @prop-irred, @rem-exact-sizes, @cor-planner2,
@thm-pb-upper2, the revised @cor-pb, @lem-live, @thm-fullred,
@rem-window, @cor-real-slopes, @thm-pb-asym, @thm-best6, @thm-onegao,
@cor-fixedroot, @prop-selfjoin, all of @sec-sorted, all of
@sec-cycle4 and @prop-sampler are proved on paper only; @app-verify
describes how they were checked.

We have also written, but not formalized, `Nat`-valued Lean statements
for most results of @sec-adapt; none of them is in the package and none
is tagged Lean-checked here.

*Trust boundary.* A reader must trust the Lean kernel, mathlib, and
that the definitions above say what the paper says: chiefly that
`adj` is the incidence matrix, that the norm instance is the $ell_2$
operator norm, and that `Stats.U` lists the nine terms. For the bridge,
the reader must also trust that the replica models the Zig kernel.
These definitions are short and are reproduced in the package's
documentation.

*Prior Leatherback results not claimed here.* The engine's Std-only
Lean workspace already proves, for the same kernel, $Out <= M$, that
the adaptive budget is at most either fixed orientation, and
$M^2 <= |R| |S| |T|$ (`AdaptiveTriangle`, `TriangleBound`). An
unrelated condensed path-counting module (`Path/CondensedCount.lean`)
is not part of this paper.

// =====================================================================
= Background: two spectral facts <sec-background>
// =====================================================================

We recall two facts used for planning and certification. Neither is a
contribution.

#fact(name: "the left-deep intermediate")[
  Let $R bowtie S$ be the intermediate of a left-deep plan, viewed as
  the bipartite graph from $R$-tuples $(x,y)$ to $S$-tuples $(y,z)$
  that share $y$. If $R$ and $S$ are read as the arcs of one layered
  digraph $X -> Y -> Z$, this graph is the line digraph restricted to
  arcs from $R$ into $S$. It is the vertex-disjoint union over $y$ of
  complete bipartite graphs $K_(d^-_R (y), d^+_S (y))$. Hence its
  biadjacency matrix has singular values $sqrt(d^-_R (y) d^+_S (y))$
  (one per $y$ with both degrees positive, the rest zero) and
  $|R bowtie S| = sum_y d^-_R (y) d^+_S (y)$, computable exactly by one
  merge of two degree arrays.
] <fact-ld>
#st[#known (elementary)]

#proof[
  An $R$-tuple and an $S$-tuple are adjacent iff they share $y$, so the
  matrix is block diagonal with one all-ones block $J$ of shape
  $d^-_R (y) times d^+_S (y)$ per $y$. A rank-one $J_(p times q)$ has
  the single nonzero singular value $sqrt(p q)$.
]

A planner can compare the exact left-deep intermediate
$sum_y d^-_R (y) d^+_S (y)$ against the bound of @cor-kernel when
deciding between WCOJ and a binary plan. This is a heuristic switch
rule, not a theorem.

#fact(name: [signless-Laplacian bound for symmetric predicates])[
  Let $G$ be a simple undirected graph with at least one edge, adjacency
  $A$, vertex--edge incidence matrix $E$, degree matrix $"Deg"$,
  signless Laplacian $Q = "Deg" + A = E E^top$ with largest eigenvalue
  $q_1 = lambda_1 (Q)$, and line graph $L(G)$. Then
  $opn(A) = lambda_1 (A) <= q_1 \/ 2 = (lambda_1 (L(G)) + 2) \/ 2$.
] <fact-q>
#st[#known (classical [#cite(<ref-crs>)[CRS10]])]

#proof[
  $A$ is symmetric and nonnegative, so $opn(A) = lambda_1 (A)$ with a
  unit Perron vector $v >= 0$. Then
  $lambda_1 = sum_(i j in E(G)) 2 v_i v_j <= sum_(i j in E(G)) (v_i^2 + v_j^2)
  = v^top "Deg" v$, so $q_1 >= v^top Q v = v^top "Deg" v + lambda_1 >= 2 lambda_1$.
  Finally $E^top E = 2I + A(L(G))$ has the same nonzero eigenvalues as
  $E E^top = Q$, so $q_1 = 2 + lambda_1 (L(G))$.
]

Our experiments do not use @fact-q: they certify $sigma$ with
Collatz--Wielandt steps on $A^top A$ directly. The exact norm is never
larger than $q_1\/2$, since $q_1\/2 >= lambda_1$, but a bound from
finitely many Collatz--Wielandt steps can be: on the path with 25
vertices, five steps on $A^top A = A^2$ from the all-ones vector give
the bound $2$, while $q_1\/2 < 2$.

// =====================================================================
= An earlier fully reduced gadget <app-iv>
// =====================================================================

An earlier draft established the fully reduced interval $[1\/12, 1\/8]$

with the following coordinate gadget. @thm-fullred supersedes its
exponent, but $I_v$ gives a smaller explicit instance with
$C > N + B_2$.

*The gadget $I_v$.* For an integer $v >= 1$ let all coordinates range
over $[v]$, and take tagged classes $X = {(A, B) : A, B in [v]^3}$,
$Y_0 = [v]^4$, $Z_1 = [v]^5$, $Y_2 = {(A, B, E, e)}$ and
$Z_2 = {(A, E, F) : F in [v]^2}$, with $A, B, E in [v]^3$ and
$e in [v]$. Put $f(A, B) = (A, B_1, B_2) in Z_1$ and
$
  R &= X times Y_0 union {((A,B), (A,B,E,e))}, \
  S &= Y_0 times Z_1 union {((A,B,E,e), (A,E,F))}, \
  T &= {(f(x), x) : x in X} union {((A,E,F), (A,B))},
$
where unspecified coordinates range freely.

#theorem(name: "a fully reduced separation")[
  Every tuple of $I_v$ lies in a triangle, and
  $Out(I_v) = v^10 + v^12$. Let $cU_v$ be the disjoint union of $I_v$
  and its two rotations. Then $cU_v$ is fully reduced,
  $
    N = 3(v^12 + v^11 + 2v^10 + v^9 + v^6), quad
    C = v^15 + 3v^12 + v^11 + 4v^10 + v^9 + 2v^6, \
    B_2 = 7v^14 + v^7, quad Out = 3(v^12 + v^10),
  $
  so $C\/(N + B_2) tilde v\/7 = Theta(N^(1\/12))$ and
  $C = Theta((N + B_2)^(15\/14))$; $B_2 = Theta(N^(7\/6))$, and $cU_v$
  attains the exponent $5\/4$ of @thm-pb-upper at slope $7\/6$. At
  $v = 8$, $C\/(N + B_2) = 45017942\/39450457 > 1$. On every fully
  reduced instance $B_2 >= Out >= max(|R|, |S|, |T|) >= N\/3$, so no
  fully reduced family has slope $kappa < 1$. Hence the worst-case
  per-binding gap against $N + B_2$ on fully reduced inputs is at least
  $1\/12$.
] <thm-fullred-iv>
#st[#proved (exact checks in @app-verify)]

#proof[
  _Support._ An $X times Y_0$ tuple $(x, y)$ closes with $f(x)$; a
  $Y_0 times Z_1$ tuple with any preimage of its $Z_1$-endpoint under
  $f$; a tuple $(f(x), x)$ with any $y in Y_0$. A tuple
  $((A,B), (A,B,E,e))$ closes with any $(A, E, F)$; a tuple
  $((A,B,E,e), (A,E,F))$ with $(A, B)$; a tuple $((A,E,F), (A,B))$ with
  any $(A, B, E, e)$. $S$ joins only $Y_0$ to $Z_1$ and $Y_2$ to $Z_2$,
  so there are no mixed triangles and $Out = v^3 v^3 v^4 + v^3 v^3 v^3 v dot v^2 = v^10 + v^12$.
  _Degrees._ On $X$: $d^+_R = 2v^4$, $d^-_T = v^5 + 1$; on $Y_0$:
  $d^-_R = v^6$, $d^+_S = v^5$; on $Y_2$: $d^-_R = 1$, $d^+_S = v^2$;
  on $Z_1$: $d^-_S = v^4$, $d^+_T = v$; on $Z_2$: $d^-_S = v^4$,
  $d^+_T = v^3$. So $(|R|, |S|, |T|) = (2v^10, v^12 + v^9, v^11 + v^6)$,
  $(alpha, beta, gamma) = (4v^14, 2v^14, v^14 + v^7)$ and
  $(alpha', beta', gamma') = (v^16 + v^10, v^16 + v^13, v^16 + 2v^11 + v^6)$.
  _Costs._ At $x$, $c_R (x) = v^9 + v^6 + 2v^4$ and
  $c_T (x) = v^9 + v^5 + v^4 + 1$, smaller by $v^6 - v^5 + v^4 - 1 >= 0$.
  At $Y_0$ option $S$ costs $v^6 + v^5$, at $Y_2$ option $R$ costs
  $1 + v^2$; at $Z_1$ option $T$ costs $v^5 + v$, at $Z_2$ option $S$
  costs $2v^4$. So $C_x (I_v) = v^15 + v^11 + v^10 + v^6$,
  $C_y (I_v) = v^12 + 2v^10 + v^9$ and $C_z (I_v) = 2v^12 + v^10 + v^6$.
  _Union._ Each root of $cU_v$ costs the sum of the three, every forward
  moment is $7v^14 + v^7$ and every reverse moment
  $3v^16 + v^13 + 2v^11 + v^10 + v^6$, larger for $v >= 2$.
  _Obstruction._ A triangle has one tuple of each relation, so on a
  fully reduced instance $Out >= max(|R|, |S|, |T|) >= N\/3$, and
  $Out <= B_2$ (@sec-prelim). The upper end $1\/8$ is @cor-pb(1).
]


// =====================================================================
= How the results were checked <app-verify>
// =====================================================================

The proofs in this paper are on paper, except the results of
@sec-main and @sec-kernel tagged Lean-checked (@sec-mech). Every
"verifier" below is a model-run agent (@sec-ai). Every construction
found by the model-run solvers of the third and fourth drafts was
rebuilt in exact integer and rational arithmetic (Python, run as
`python3 -I`) by at least two verifier agents that did not run or
import the solvers' scripts; each verifier also checked the proofs line
by line and tried to refute the claims. For the third draft, 55
statements went through this check: 51 were accepted as stated, 4 after
a repair, none rejected. For the fourth draft the fully reduced theorem,
the 4-cycle theorem and the engine's rescue stage went through it: both
theorems were accepted after presentation repairs (the 4-cycle
sharpness threshold $L >= t^3$ instead of $L >= t^2$; ten dihedral
orbits instead of nine; a duplicated factor in the rounding display),
one auxiliary claim was refuted (the value $1\/11$ at slope $1$,
@rem-window), and the engine audit refuted the claim that the
implemented candidate pruning preserves the searched rule's decisions
(@sec-engine). These checks cover instances, closed forms and proof
steps; they are evidence, not proofs, and none of these results is
tagged Lean-checked.

The final review by Weaver (@sec-ai) re-implemented the cost model and
every explicit family of @sec-adapt from the paper's definitions alone,
in exact integer arithmetic, sharing no code with the artifacts; it
reproduced every closed form it rebuilt, found no violation of the upper
bounds of @sec-adapt and @sec-main on 5,987 random instances and
3,000-step hill climbs per ratio, found a minimum $Out\/U = 0.2521$ over
200,000 random regular statistics (the block witness admissible every
time), and a worst $("pricing" - 4n)\/C$ between $3.00$ and $4.00$
for the scheduler of @prop-ptr on 3,996 random instances (the value
depends on the tuple order, which follows Python's per-process string
hashing; over 50 hash seeds it was $3.00$, $3.20$ or $4.00$). Its
scripts and recorded outputs
are in the paper repository as an outside check.

@tab-provenance names, for each group of results, who found or proved
it and who checked it; @tab-verify lists the exact checks per result,
with paths relative to `artifacts/`.

#figure(
  caption: [Provenance. CC: the orchestrating Claude Code session
    (Claude Opus 5.5) and the Claude subagents it launched (theorem
    search, provers, referees, verifier lenses, auditors); FA: Claude
    Fable 5.1 agents at maximum effort; AX: Codex CLI agents with
    GPT-6-Astra at "ultra" effort; R1: the GPT-5.6-sol Pro review of the
    first draft; R2, R3: the GPT-6-Astra Pro reviews of the second and
    third drafts; G6: a separate GPT-6 Pro session run by the author on
    the second draft; WV: Weaver (final review). "Checked" lists exact
    rebuilds and proof audits, not the author's reading, which covers
    everything.],
  text(size: 8.5pt, table(
    columns: (1fr, 1fr, 1fr),
    align: (left, left, left),
    table.hline(stroke: 0.8pt),
    table.header([*Results*], [*Found or proved by*], [*Checked by*]),
    table.hline(stroke: 0.4pt),
    [@thm-main, @lem-deg, @lem-feasible, @lem-value, @cor-single; @sec-kernel], [CC; Lean proofs written by CC], [Lean kernel; R1, R2 audits; WV],
    [@thm-sharp], [family in rational (Pell) form: R1; real form and Lean proof: CC], [Lean kernel; R2],
    [@cor-twonorm, @prop-irred, @rem-exact-sizes, @cor-planner2], [AX (solver); budget-only scope of the planner example: R3], [two CC verifier lenses; FA verifier; R3],
    [@thm-cycle4, @lem-lambda, @prop-cycle4-sharp], [FA (solver)], [AX and FA verifiers (one more AX audit for the 4-cycle); CC rebuild of the sharpness family],
    [@lem-sum, @lem-perroot, @thm-pb-upper, @thm-pb-lower, @lem-pad, @thm-pb-slopes, @thm-sep, @prop-ferrers], [CC (theorem search, provers, referees); proof repair of @thm-pb-upper (geometric mean of nonnegative terms): R2 and G6], [CC evaluators; R1, R2, R3 recomputations; WV],
    [@prop-ptr, @rem-ptr], [CC; tightness of the constant $6$ and the counterexample to the first bit-discard rule: R1], [CC simulation; R2; WV],
    [@cor-real-slopes], [R2], [CC exact script; R3; WV],
    [@thm-pb-upper2, @thm-pb-asym, @thm-best6, @thm-onegao], [AX and FA, independently (the $D$ gadget of @thm-pb-asym is AX's)], [two CC verifier lenses; FA verifier; R3; WV],
    [@cor-fixedroot], [R3], [CC],
    [@lem-live, @thm-fullred, @rem-window], [FA (solver); in @rem-window, the isolated-triangle padding of (a) and the cap of (b) with its added cost lemma: AX (verifier)], [AX and FA verifiers (AX refuted the unpadded "$1\/11$ at slope $1$"); CC rebuild],
    [@thm-fullred-iv], [AX (solver)], [two CC verifier lenses; FA verifier; R3; WV],
    [@prop-selfjoin], [(1)--(2): R2 and G6; (3)--(4): G6], [CC exact scripts; R3],
    [@def-sorted, @lem-cert, @lem-interleave, @thm-sorted-g8, @thm-sorted-sep, @rem-sorted-cheap], [AX and FA, independently], [two CC verifier lenses; FA verifier; R3],
    [@thm-sorted-upper, @thm-quarterlog, @lem-decision], [AX; three-way refinement of @lem-decision, the randomized proof and the densification: R3], [two CC verifier lenses (one repair); FA verifier; R3],
    [@cor-sorted-upper2], [R3], [CC],
    [@rem-engine-port], [AX (port of the engine routine)], [two CC verifier lenses; FA verifier],
    [@prop-sampler], [stride instance: AX; statement for every fixed grid and proof: CC], [CC exact script; R3],
    [Engine operator, planner, E2 and engine runs (@sec-exp, @sec-engine)], [CC (implementation and runs); admission rule searched by AX over 7,056 configurations], [first audit: AX; audit of the fix: CC; recomputations from the raw rows by R1 (E2) and R2 (E2 and engine)],
    table.hline(stroke: 0.8pt),
  )),
) <tab-provenance>


#figure(
  caption: [Exact checks behind the results proved on paper.],
  text(size: 8.5pt, table(
    columns: (auto, 1fr),
    align: (left, left),
    table.hline(stroke: 0.8pt),
    table.header([*Result*], [*Checks and artifacts*]),
    table.hline(stroke: 0.4pt),
    [@thm-pb-upper], [not formalized; the integer form and all six per-root
forms are also checked as exact integer inequalities on six runs of
4,500 random instances by `verify/thm1/rnd.py`, worst
ratio $0.64$ for the theorem and $0.69$ per root.],
    [@thm-pb-upper2], [on paper. The integer form held on 5,000, 10,500 and
10,720 random and skewed instances plus $36$ structured ones, in three
independent runs; largest ratio in the report's run
$9.6 dot 10^(-16)$, at $(N, C) = (211, 601)$:
`hillclimb/P2-exponents/verify_new_upper.py`.],
    [@thm-pb-slopes], [also checked exactly at $(i,j) = (1,1)$ for $u = 2, 3$
and at $(2,1), (2,2)$ for $u = 2$; ratio $C\/(N^(3\/8) B_2^(3\/4))$
about $0.236$ to $0.312$ ($0.312$, $0.279$, $0.236$, $0.267$ at
$(i,j,u) = (1,1,2), (1,1,3), (2,1,2), (2,2,2)$)],
    [@cor-real-slopes], [exact closed forms checked for all $1 <= j <= i <= 40$ at
$u = 2$, and at $kappa = sqrt(2)$, where
$j_n = 3n - "isqrt"(8 n^2) - 1$ gives
$(n, j_n) = (6, 1), (7, 1), (10, 1), (20, 3), (40, 6)$:
`hillclimb/checks/slopes_check.py`. The extension is from R2
(@tab-provenance).],
    [@thm-pb-asym], [on paper. The $D$-statistics checked by literal
enumeration on $7$ triples by `d_gadget_check.py`; the union at $p = q = 1$ against
$F_(1,1) (2), F_(1,1) (3)$; the closed forms evaluated exactly at
$(u, p, q) = (2, 9, 10), (2, 10, 11), (2, 19, 20)$, ratios
$C\/(N + B_2) = 0.980, 1.96, 1004.4$:
`hillclimb/P2-exponents/verify_slopes.py`,
`hillclimb/checks/d_gadget_check.py`.],
    [@thm-best6], [on paper. 10,000 + 10,500 random instances and hill
climbs, largest ratio exactly $1$, at complete tripartite instances;
$"GMIN"$ enumerated literally for $m = 1, dots, 8$:
`hillclimb/P2-exponents/best_six_verify.py`.],
    [@thm-onegao], [on paper. All three drivers checked on the verifiers'
random instance sets (10,500 and 10,720 + 7,169), largest ratio
$1$, attained on $"GMR"$ and complete tripartite instances; $"GMR"$ for $m = 1, dots, 12$ and the sharp family
for $u = 1, dots, 6$ enumerated literally:
`hillclimb/P2-exponents/verify_single_order.py`.],
    [@prop-selfjoin], [exact checks of (1)--(2) on $G_8 (2), G_8 (3)$, $cF_a$ for
$a = 2, 3, 4, 5, 8$ and $"GMIN"(2,3,4)$, and of (4) on 4,000 random
symmetric graphs: `hillclimb/checks/selfjoin_check.py`.],
    [@prop-ptr], [`verify/thm1/rnd.py` simulates the scheduler
on six runs of 4,500 random instances and asserts (1) and the
pricing bound of (3); no violation.],
    [@thm-sorted-g8], [exact values $(N, B_2, Q) = (2208, 1280, 1312)$,
$(48843, 32805, 46170)$, $(457728, 327680, 590848)$,
$(2634375, 1953125, 4300000)$ for $m = 2, dots, 5$ by both solvers and
the verifier rebuilds; padded $m = 2, 3$ with unchanged hard certificates:
`hillclimb/P1-sorted/`.],
    [@thm-sorted-sep], [exact certificate sums for parameters $2, dots, 5$: $cF_a$
$6, 30, 84, 180$; $"GMR"$ $48, 405, 1792, 5625$; $"GMIN"$ and padded
$"GMIN"$ (hard tuples) $112, 1377, 7936, 30625$; $cH_a$
$12, 45, 112, 225$; $F_(i,j)$ at $(i,j,u) = (1,1,2), (1,1,3), (2,1,2), (2,2,2)$:
$Q = 1312, 46170, 4268032, 590848$:
`hillclimb/P1-sorted/separations/check.py`,
`hillclimb/P1-sorted/slopes/verify_families.py`.],
    [@lem-sorted-agm], [bit-length identity and $h^2 <= 9 p q\/2$ checked
exhaustively for $s < 300$, $l < 2000$: `hillclimb/checks/slopes_check.py`
asserts $h^2 <= 9 p q$, and on the same range the largest $h^2\/(p q)$
is $2691\/599 < 9\/2$, at $(p, q) = (299, 599)$.],
    [@thm-sorted-upper], [on paper; galloping measured at most $5.97 h$ in the
verifier's port: `hillclimb/verified.md`, P1.7.],
    [@thm-quarterlog], [on paper; degree formulas, decision-tree argument,
simultaneous ordering and quantifiers re-derived by the two CC verifier
lenses: `hillclimb/P1-sorted/slopes/log_normalized_proof.md`
and `log_normalized_checks.py`.],
    [@rem-engine-port], [exact counts from a Python port checked line by line against
the Zig source and against a Zig harness compiled with Zig 0.16.0:
`hillclimb/P1-sorted/engine/`.],
    [@cor-twonorm], [on paper. Exact checks: exhaustive $0\/1$ triples on small
shapes with operator norms decided by exact determinants, 44,200
instances of the sharpness family, and the grids of the archived
report, $0$ failures: `hillclimb/P3-spectral/`.],
    [@prop-irred], [exact checks: all nine witnesses materialized at
$n = 2, 3, 5$ with exactly computed norms; 21,952 exponent regimes
enumerated; `hillclimb/verified.md`, P3.5--P3.6.],
    [@cor-planner2], [exact checks: 4,096 matrix triples, 73,984 budget
cases, $0$ failures; `hillclimb/P3-spectral/`. The rotated-star example rebuilt literally for $k = 2, 3, 4, 8$: `hillclimb/r4-fullred/editor/check_r4.py`.],
    [@prop-sampler], [on paper; every quantity checked in exact arithmetic for
the stride, the golden-ratio grid and two fixed pseudo-random grids,
$m in {64, 65, 96, 128, 200, 256}$.],
    [@lem-live, @thm-fullred], [Two verifiers rebuilt the live gadget literally: closed forms equal brute force on 733 parameter tuples and 60 random three-copy unions (all fully reduced); $cL(v)$ by brute force for $v = 2, 3, 4$ ($(N, C, Out, B_2) = (8976, 12464, 5760, 29264)$, $(355266, 888246, 262440, 2441502)$, $(5263104, 22332672, 4177920, 56889600)$) and by closed forms for $v <= 60$; the general family on 100 tuples and literally at $(i,j,u) = (2,1,2)$, $(1,0,2)$, $(1,0,3)$, $(2,0,2)$; the CC editor rebuilt $cL(2)$, $cL(3)$ and $(2,1,2)$ from the text of @sec-fullred: `hillclimb/r4-fullred/`.],
    [@rem-window], [(a) exact closed forms for $v = 2, dots, 5$ and literal rebuilds for $v = 2, 3$; (b) the cost lemma on 26,382 tuples, and both linear identities with exact dual certificates of an exact rational LP over the design (also with the size exponent forced to $1$); `hillclimb/r4-fullred/astra/LP_REPORT.md`.],
    [@thm-cycle4, @lem-lambda], [Two verifiers: line-by-line proof audits; exact enumeration of the dual polyhedron of the arc program (50 vertices, 38 needed with rational strict-separation certificates, identical for 9 and 13 arcs); all 38 inequalities certified with exact eigenvalue brackets on the 65,536 $0\/1$ instances of shape $(2,2,2,2)$, 91,173 near-tight instances of shape $(2,2,2,3)$ and about 72,000 random, adversarial and Kronecker instances, no violation; Lemma Λ on random and annealed instances; the rounding on 11,296 grid vectors (worst loss $4.48 < 16$): `hillclimb/r4-cycle4/`.],
    [@prop-cycle4-sharp], [$U_4^12 = t^36$ exactly at $L = 8$ for several $t < 2$; the envelope $min(t^3, sqrt(L t^3))$ by an exponent argument and exact checks; the adjacent variant: `hillclimb/r4-cycle4/astra/proof_exact.py`, `hillclimb/r4-fullred/editor/check_r4.py`.],
    [@thm-fullred-iv], [Literal enumeration with a triangle-support check of every tuple for $v = 1, dots, 4$ by two separately written evaluators, and closed forms for $v <= 8$:
 `hillclimb/P2-exponents/verify_fully_reduced.py`, `hillclimb/r4-fullred/fable/check_iv.py`.],
    table.hline(stroke: 0.8pt),
  )),
) <tab-verify>

// =====================================================================
= Artifacts <sec-artifacts>
// =====================================================================

The paper repository,
#link("https://github.com/TJC-LP/triangle-adaptivity-paper")[`github.com/TJC-LP/triangle-adaptivity-paper`],
holds the source of this paper and its figure scripts, the Lean
workspace of @sec-mech, and everything needed to check the
computational claims; its `README.md` indexes it, and every
`artifacts/` path in this paper is relative to it. Leatherback itself
will be open-sourced; once it is public, the repository will name the
Leatherback versions the engine runs used. Until then the repository
holds the engine-run scripts, the raw rows and the summaries built from
them.

- `artifacts/e2/` (@sec-exp): the preparation, bound, run and summary
  scripts; `results.csv` and `summary.md` with their SHA-256 digests;
  run logs; per-predicate spectral data; dataset URLs with SHA-256
  digests; the Python environment (3.11.9, numpy 2.4.6, scipy 1.17.1,
  numba 0.68.0); and the commands, reconstructed from the logs where
  they were not recorded. `check/csvcheck.py` recomputes the bounds and
  ratios and audits the results file for internal consistency, and
  `check/rebuild_summary.py` reruns the summary script on the committed
  results file and spectral data and confirms that it reproduces
  `results.csv` and `summary.md` exactly; `src/recertify.py` recomputes the
  exact $sigma$ certificates and changes only the certificate columns.
- `artifacts/verify/`: `chk_exact.py`, an exact-arithmetic check of
  @thm-main (integers and fractions only; exhaustive over
  $1 <= s_i <= r_i <= 25$, $3.4 times 10^7$ vectors, no failure) and of
  the family of @thm-sharp; the evaluators and family checks for
  @sec-adapt (`g8.py`, `thm1/`); and `OUTPUTS.md`, which records every
  command, exit code and output with script digests.
- `artifacts/engine/` (@sec-engine): data-generation seeds and digests,
  raw timing samples, summary and answer-comparison scripts and logs,
  quality-gate results and the machine description.
- `artifacts/engine-kg/` (@tab-engine-kg, @tab-rescue): the
  driver-policy runs on the knowledge-graph triangles, with the query
  files, the raw per-(query, policy) rows of runs A (`raw/`), B
  (`raw-rescue/`) and C (`raw-run-c/`, with the synthetic-store reruns
  and alternating process pairs in `controls-run-c/`), E2's bounds per
  query, the scripts that convert the data, build the queries, run the
  harness and rebuild the summary and the tables, and
  `estimator_adversary.py` and `scripts/adversary.py`, which check
  @prop-sampler in exact arithmetic.
- `artifacts/hillclimb/`: the reports, scripts and recorded outputs of
  the model-run solvers and verifiers (@app-verify, @tab-provenance):
  `verified.md` with the consolidated verdicts and `checks/` for the
  third draft; `r4-fullred/` (@sec-fullred), `r4-cycle4/`
  (@sec-cycle4) and `r4-engine-audit/` (the audits of the rescue stage,
  @sec-engine) for the fourth, each with the verifiers' reports and
  scripts.
- The Lean workspace (@sec-mech), with its pinned toolchain and
  manifest, the spectral library, the kernel replica and both audit
  files.
- Weaver's outside checks: five Python scripts written from the
  paper's definitions alone, with their recorded outputs (@app-verify).

The raw datasets and generated graphs are not committed; each README
gives the commands to download or regenerate them and their digests.
