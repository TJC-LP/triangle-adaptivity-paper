> Consolidated verdicts on the three reports in this directory (two independent verifier lenses per report), with the paper-ready statements used in revision 3. Report paths below are relative to this directory. Paper numbering refers to revision 2.

# Astra reports P1–P3: consolidated verdicts and paper-ready statements

Date: 2026-10-09. Inputs: the three Astra reports (`P1-sorted/report.md`,
`P2-exponents/report.md`, `P3-spectral/report.md`) and the two
independent verifier verdict sets per report (lens A and lens B below), against the paper
`spectral_agm.typ`, revision 2 ("Levels of adaptivity and spectral worst-case bounds for
labeled triangle joins"). Where a closed form is restated below it was also re-checked in
exact arithmetic by the editor (python3 -I, all passed; the editor's script is not archived).

**Status rules.** ACCEPT = both lenses verified, or one verified by exact rebuild and the
other found no error. REPAIR = true after a stated fix. REJECT = refuted. UNRESOLVED =
neither lens could settle. Items a lens listed that are not claims of the report are marked
OPEN (no claim).

**Tally.** 57 items. ACCEPT 51, REPAIR 4, REJECT 0, UNRESOLVED 0, OPEN (no claim) 2.

| Report | Items | ACCEPT | REPAIR | REJECT | UNRESOLVED | OPEN (no claim) |
|---|---:|---:|---:|---:|---:|---:|
| P1 sorted intersections | 21 | 20 | 1 (randomized bound needs a Markov step) | 0 | 0 | 0 |
| P2 exponents | 20 | 18 | 1 (single-GAO gap must be qualified "general inputs") | 0 | 0 | 1 |
| P3 spectral, two norms | 16 | 13 | 2 (one-norm scope; script-provenance sentence) | 0 | 0 | 1 |

**Paper numbering used below (rendered, confirmed from the PDF).** §2 Preliminaries (cost
model). §3: Thm 3.1 (spectral AGM, `thm-main`), Lemma 3.2, Lemmas 3.3–3.4, Remarks 3.5–3.6,
Thm 3.7 (constant 4 sharp, `thm-sharp`), Cor 3.8 (single norm, `cor-single`). §4: Lemma 4.1,
Prop 4.2 (`prop-kernel`), Cor 4.3 (`cor-kernel`), Prop 4.4. §5: Lemma 5.1 (sum identities),
Lemma 5.2 (per-root), Thm 5.3 (`thm-pb-upper`), Cor 5.4, Thm 5.5 (G8, `thm-pb-lower`),
Cor 5.6, Lemma 5.7 (padding), Remark 5.8, Thm 5.9 (slopes), Thm 5.10 (separations),
Remark 5.11 (`rem-notshow`), Remark 5.12, Lemma 5.13, Prop 5.14 (price-then-run),
Remark 5.15, Prop 5.16 (Ferrers). §11 Open problems, items 1–12 in the order printed.
(A verifier's "Cor 3.5" is Cor 3.8.) Notation: N = |R|+|S|+|T|; α,β,γ / α',β',γ' forward
and reverse squared-degree sums; Q = min(αβγ, α'β'γ'); B2 = Q^{1/3}; Λ = (αβγ)^{1/2};
M_π kernel probe work; C = min(C_x,C_y,C_z) per-binding cost (min-side charge); U the
nine-term spectral bound; W(r,σ) the worst-case output.

**Reading the reports' labels.** Several report items labeled "[refuted]" refute the natural
conjecture, i.e. they are positive results (e.g. "a factor smaller than 4 is impossible";
"the log-free translation of Thm 5.3 to sorted cost is false"). They are listed here as
claims with their positive content.

---

## 1. P1 — comparison-based intersection of sorted runs (open problem 5, first half)

Directory: `P1-sorted/`. Lens A and lens B both rebuilt the constructions
independently (A: `cert_complexity.py`, `lemma_bruteforce.py`, `indep_stats.py`,
`indep_separations.py`, `indep_port.py`, plus a Zig harness compiled against the verbatim
`sorted_runs.zig`; B: `port.py`, `g8.py`, `g8pad.py`, `families.py`, `quarterlog.py`,
`separations.py`). Every numerical claim of the report was reproduced by both.

### The model (used by every P1 statement)

**P1.1 Model and scope. ACCEPT** (A verified against §2/§5 definitions; B used the same model
throughout, no error).

Paper-ready (new definition, for a new subsection "Sorted intersections" in §5 or §2):

> *Sorted fresh-call comparison model.* An intersection call receives two strictly increasing
> runs of opaque keys and their lengths. It may compare any two keys (three-way or Boolean
> predicates) and do index arithmetic; key arithmetic, hashing and addressing by key value
> are unavailable. Every key comparison costs one unit; a plan is additionally charged one
> unit per visited outer tuple. A call is *fresh*: it knows the internal order of its two
> runs and nothing else (no comparison results, certificates, aliases or rank hints from
> other calls). The routine A is fixed before the adversary assigns term identifiers (one
> global total order on each of X, Y, Z); the root and the per-binding option may be chosen
> with full knowledge of the labeling. Q_A is the minimum, over roots and per-binding
> options, of the resulting cost (comparisons plus outer visits) of a correct run of A.
> Relabeling permutes rows and columns of A_R, A_S, A_T, so sizes, degrees, singular values,
> N, B2, U and Out are unchanged: nothing in §§3–4 depends on the labeling.

Changes: §2 "Cost model" paragraph ("with galloping over sorted runs an extra logarithmic
factor appears, which we do not analyse ... we do not claim the lower bounds of §5 for that
model") becomes a pointer to the new subsection; the clause "with contiguous identifiers
leapfrog finishes after a few seeks" is retained as the reason the adversary controls the
identifiers.

**P1.2 Comparison certificate. ACCEPT** (A: proof checked, brute force over Delannoy-enumerated
inputs; B: certificate = ternary-merge count on all 2,095,436 G8 calls, 2s−1 for s ≤ 40).

> *Lemma (comparison certificate).* Let A, B be disjoint strictly increasing runs and t(A,B)
> the number of adjacent pairs of their merged order whose members lie in different runs.
> Every correct fresh intersection routine makes at least t(A,B) key comparisons on (A,B).
> If the runs alternate, a_0 < b_0 < … < a_{s−1} < b_{s−1}, then t = 2s − 1, and ternary
> merge makes exactly 2s − 1 comparisons. (Proof: an uncompared adjacent opposite-run pair
> can be identified; both runs stay strictly increasing, every other comparison outcome is
> unchanged, and the answer becomes nonempty.)

**P1.3 Simultaneous interleaving. ACCEPT** (both: realized concretely in all families).

> *Lemma (one order for all rows).* For A = {a_k : k < s} and pairwise disjoint private sets
> B_h = {b_{h,k} : k < s}, the single order a_k, b_{0,k}, b_{1,k}, … (k = 0, …, s−1) restricts
> to a perfect alternation on A ∪ B_h for every h. Orders on disjoint term domains, and on
> vertex-disjoint components, concatenate to one global order.

### Lower bounds in the sorted model, no logarithm

**P1.4 G8 under one explicit global order; exponent 9/8. ACCEPT** (A: degrees match
Table tab-g8, closed forms asserted for m = 2..5; B: full per-row enumeration m = 2..5).

> *Theorem (Thm 5.5 and Cor 5.6 in the sorted model).* Realize G8(m) with X = {(g,h) : g < m^3,
> h < m}, Z2 = {(g,t) : g < m^3, t < m^3}, T complete between Z_{2,g} and X_g for each g
> (d_T^+ = m on Z2, m^3 into each x), m^4 private Z0-predecessors per x, a private
> S-predecessor set Y_{2,z} of size m^2 for each z ∈ Z2, R = X × Y0, S ⊇ Y0 × Z1 (degrees
> exactly as in Table tab-g8). Order Z as: for t < m^3, Z1[t], Z2[0,t], …, Z2[m^3−1,t]; then
> all of Z0. Order Y as: for k < m^2, Y0[k], then Y_{2,z}[k] for every z ∈ Z2. Then,
> simultaneously for all x and all z, every call (Z1, T_x) needs ≥ 2m^3 − 1 comparisons and
> every call (Y0, Y_{2,z}) needs ≥ 2m^2 − 1. For every eligible routine A and every critical
> x, option R costs q_R(x) ≥ 2m^5 and option T costs q_T(x) ≥ m^4 + 2m^5 (comparisons plus
> outer visits), with equality for ternary merge; the other roots of G8 cost m^5 and m^8.
> On the three-rotation union U(m) every root has exact optimal ternary cost
> 2m^9 + m^8 + m^5, which is a lower bound on Q_A for every A; N = 3(2m^8+m^7+m^6+m^5),
> α = β = γ = 5m^8, reverse sums m^12+2m^11+3m^10+m^7, so B2 = 5m^8 and
> Q_A/(N + B2) ≥ m/7 ≥ (N/9)^{1/8}/7. Hence no c, and no c = O(log^k N), satisfies
> Q_A ≤ c(N + B2) for comparison-based sorted intersection (plain merge, leapfrog, galloping
> with any step schedule) under an adversarial identifier assignment.

Exact values (both lenses): (N, B2, Q_ternary) = (2208, 1280, 1312), (48843, 32805, 46170),
(457728, 327680, 590848), (2634375, 1953125, 4300000) for m = 2..5.
Changes: Thm 5.5/Cor 5.6 gain a sorted-model clause (constant m/7 instead of m/14 because
a certificate is 2s−1 rather than s); §11 item 5, first half, is answered for fresh calls.

**P1.5 Padding preserves the sorted-model bound. ACCEPT** (A: argument checked against
Lemma 5.7; B: `g8pad.py`, m = 2,3, hard-row certificates before = after).

> *Addendum to Remark 5.8(a).* In G8 the padded vertices are Y2 (S-only), Z0 (T-only) and
> Z1 (S-only); X, Y0, Z2 have tuples in both relations and are not padded, and every added
> tuple touches a fresh vertex, so S^+(y) = Z1, T_x, R(x) = Y0 and S^−(z) = Y_{2,z} are
> unchanged for original vertices. Placing all fresh keys before all original keys keeps
> every hard run and its certificate; the critical root still costs ≥ 2m^9 per root, while
> N' ≤ 7N and B2' = O(m^8) by Lemma 5.7(ii),(iv). So the sorted-model gap Ω(N^{1/8}) holds on
> pairwise semijoin-reduced inputs with Θ(N) triangles. (B, m = 2,3: padded vertices
> 2m^8 + m^3 = 520, 13149; R-hard certificates m^6(2m^3−1) = 960, 38637 and T-hard
> m^7(2m^2−1) = 896, 37179, unchanged; N' = 2296, 55728.)

**P1.6 F_{i,j} with interleaved orders (Thm 5.9 in the sorted model). ACCEPT** (A: degrees
match Thm 5.9, closed forms asserted; B: explicit construction, all four table rows).

> *Theorem.* Fix i ≥ j ≥ 1, u ≥ 2, n = u^{4i}, a = u^{4i−2j}, b = u^{4i−j}, d = u^{4i−3j},
> H = u^{3j}. Partition X into H groups of size d and Z2 into H groups of size b, make the
> paired T-blocks complete, give every z ∈ Z2 a private a-element S-predecessor set, and use
> the interleaving lemma (Z1 against every Z2 group; Y0 against every Y_{2,z}). Both options
> at every critical x cost exactly 2ab for ternary merge and at least 2ab for every eligible
> routine; the other gadget roots cost ab and u^{8i}. The three-rotation union has exact
> optimal cost Q = 2u^{12i−3j} + u^{8i} + u^{8i−3j}, N = 3(u^{8i} + u^{8i−j} + u^{8i−2j} +
> u^{8i−3j}), B2 = 3u^{12i−4j} + u^{8i} (reverse sums 3u^{12i−2j} + u^{12i−5j} are larger).
> Thus B2 = Θ(N^κ), κ = 3/2 − j/(2i), and Q = Θ(N^{3/8} B2^{3/4}) with no logarithmic
> factor, because every hard call is balanced.

Table (both lenses): (i,j,u) = (1,1,2): N 1440, B2 1024, Q 1312; (1,1,3): 29160, 26244,
46170; (2,1,2): 368640, 3211264, 4268032; (2,2,2): 261120, 262144, 590848.
Changes: Thm 5.9 gains a sorted-model clause.

**P1.14 Theorem 5.10's separations 1/6, 1/4, 1/5 in the sorted model, no log loss. ACCEPT**
(A: own constructions and own padding reproduce every number, report's `check.py` output
byte-identical; B: `separations.py`, all certificate sums and padded statistics).

> *Theorem (Thm 5.10(1)–(2) against N + B2 in the sorted model).* (1) F_a with z_{i,k}
> ordered by (k,i): every off-diagonal R-row (x_i, y_j) is an alternating pair of length-a
> runs, so the hard R-rows need a(a−1)(2a−1) comparisons in total (6, 30, 84, 180 for
> a = 2..5), with N = 3a^2, B2 = a^{8/3}: a fixed GAO with second relation R loses
> Θ(N^{1/6}) against N + B2 on a pairwise semijoin-reduced instance. GMR with the common Z1
> layered against every private B_x: all m^4 R-rows need 2m − 1, total m^4(2m−1)
> (48, 405, 1792, 5625), N = 2m^4 + m^2, B2 = m^4: loss Θ(N^{1/4}). (2) GMIN with the three
> layerings (Z1 vs Z0-fibers, X2 vs X1-fibers, Y2 vs Y3-fibers, disjoint domains, one
> order): each driver has m^4 hard rows of 2m^2 − 1, total m^4(2m^2−1) (112, 1377, 7936,
> 30625), all other rows meet an empty run; N = 3(m^5+m^4+m^3), B2 = 3m^5: the best of the
> six GAOs loses Θ(N^{1/5}) against N + B2 and against adaptive execution plus N. Padded
> GMIN (fresh keys first): N' = 12m^5+3m^4+3m^3+9m^2, B2' = 8m^5+3m^2, Out' = 3m^5+3m^2
> (492/268/108, 3321/1971/756, 13392/8240/3120, 39975/25075/9450), the hard original rows are
> unchanged, and the cheap options are O(1)-per-edge singleton searches for a fresh key
> before all original keys, so adaptive execution is Θ(N') while every GAO costs Θ(m^6).
> All lower bounds hold for every eligible routine; merge attains them.

Editorial note (B): label the padded-GMIN certificate column "hard rows" (the all-row sums of
the padded drivers are 260/2403/12144/43325 because fresh rows add unit-cost terms).
Changes: Thm 5.10(1)–(2) gain a sorted-model clause.

**P1.15 Fixed-root separation H_a. ACCEPT** (A and B: both options at every x contain a
alternating length-a pairs; certificates 12, 45, 112, 225 = a^2(2a−1)).

> *Thm 5.10(3) in the sorted model.* In H_a, with Y1, Y2 alternated and the common Z2
> layered against every private Z1-fiber, each option at every x ∈ X has aggregate
> certificate a^2(2a−1); fixed root x costs Θ(a^3), root y costs Θ(a^2); fresh-first padding
> leaves the certificates of the original X unchanged (fresh bindings add a + a^2 unit-cost
> rows), so the Θ(N^{1/2}) loss of a fixed root against adaptive cost plus N holds on
> semijoin-reduced inputs in the sorted model.

Wording fix (B, optional): "unchanged by padding" should read "on the original X".

**P1.16 Qualification: the Θ(a) ratio of F_a/G_a against C does not transfer unchanged.
ACCEPT** (both verified as a caution).

> *Remark.* In F_a and G_a the cheap options are singleton membership tests in length-a
> runs; a fresh singleton search costs up to ⌈log2(a+1)⌉ comparisons while its certificate
> is 1 or 2. So, in the sorted model, the Θ(N^{1/2}) loss of Thm 5.10(1)–(2) against C + N is
> established only between Ω(N^{1/2}/log N) and O(N^{1/2}); the ratios against N + B2 are
> unaffected.

### The quarter-logarithm: upper bound, necessity, and the price-then-run analogue

**P1.7 Universal quarter-log upper bound. ACCEPT** (A: algebra re-derived step by step from
Lemma 5.2; both: (k+1)^2 ≤ 9·2^{k−1}, h^2 ≤ 9pq, h ≤ L_N min(p,q), bit-length identity
checked exhaustively; B: empirical gallop cost ≤ 5.97 h).

> *Theorem (sorted-model analogue of Thm 5.3 and Prop 5.14).* For runs of lengths p, q put
> s = min(p,q), l = max(p,q), h(p,q) = s(1 + ⌈log2(l/s)⌉) (h = 0 if a run is empty), and
> L_N = 1 + ⌈log2 N⌉. Doubling galloping intersects the two runs with O(h(p,q))
> comparisons; h ≤ L_N·s and h ≤ 3√(pq). Let Ĉ be the per-binding cost in which every edge
> is priced 1 + h(·,·) instead of 1 + min(·,·) (same roots, options and minimum). Then
> Ĉ ≤ N + 3^{3/4} L_N^{1/4} (|R||S||T|)^{1/8} min(Λ, Λ')^{1/2} ≤ N + 3^{3/4} L_N^{1/4}
> (N/3)^{3/8} B2^{3/4}. The prices are computable from degrees in O(N) reads, with
> ⌈log2(l/s)⌉ = bitlength(⌊(l−1)/s⌋); selecting the best priced root and option and
> executing by galloping costs O(Ĉ). Hence the sorted-model per-binding cost is
> O(N + (log N)^{1/4} (|R||S||T|)^{1/8} min(Λ,Λ')^{1/2}).

Proof shape: P(x) ≤ L_N √(aβ), Q(x) ≤ 3√a·w(x), min(P,Q) ≤ P^{1/4}Q^{3/4}, Hölder (4,4/3),
Σ_x w(x) ≤ √(γ|S|) — Lemma 5.2's chain with the extra 3^{3/4} L_N^{1/4}; primed form and
cube root as in Thm 5.3.
Changes: new theorem beside Thm 5.3; Prop 5.14 gains a remark (the scheduler works with
prices h, which are degree-computable); §2 "which we do not analyse" is replaced; §11 item
11's "the galloping log factor [is] not analysed" is resolved (bag semantics stay open).

**P1.8 Logarithm-free AGM cap. ACCEPT** (both).

> *Lemma.* Σ_{(x,y)∈R} h(d_S^+(y), d_T^−(x)) ≤ 3‖A_R‖ √(|S||T|) ≤ 3√(|R||S||T|). So the
> fixed-driver galloping kernel costs O(N + ‖A_R‖√(|S||T|)): the Hölder term H_R of
> Prop 4.2, and Lemma 5.1's C ≤ N + √(|R||S||T|), survive galloping with constant 3 and no
> logarithm.

**P1.9 Statistics of the modified family. ACCEPT** (A: recomputed from degrees for eight
(i,j,h); B: seven (i,j,h), degree-profile accounting matched against an explicit small
graph of the same block shape). Folded into P1.12.

**P1.10 Decision-tree lemma. ACCEPT** (A: proof completed; brute force over every constraint
set up to (p,q) = (3,4); B: transcripts of merge and of the gallop port injective on all
shuffles for five (p,q)).

> *Lemma.* Fix a correct fresh-call routine and disjoint runs of lengths p, q. A leaf of its
> comparison tree that answers "disjoint" is reached by at most one of the C(p+q, p)
> shuffles (if the poset generated by the transcript and the two internal orders is not
> total, an incomparable opposite-run pair exists and the linear extension that ties it
> reaches the same leaf with a nonempty intersection). On disjoint inputs every comparison
> branches binarily, so fewer than 2^D shuffles are decided with fewer than D comparisons.

**P1.11 Union bound. ACCEPT** (both: q/p = u^j M^5 ≥ u, D = pL/2, bitlength(3na) ≤ D,
D ≥ 16iL > 2 + 8iL, p ≥ u^{2i} ≥ 32i, for all tested (i,j,h)). Folded into P1.12.

**P1.12 The quarter logarithm is necessary (every F-slope; Θ(N^{9/8}(log N)^{1/4}) at
B2 ≍ N). ACCEPT** (A and B: degree formulas, decision-tree argument, simultaneous ordering
and quantifiers all re-derived; upper/lower ratio constant across parameters).

> *Theorem (quarter-log lower bound).* Fix i ≥ j ≥ 1 and h ≥ 1; M = 2^h, L = M^4, u = 2^L.
> Let n = |X| = u^{4i}/M^4, a = |Y0| = u^{4i−2j} M^2, p = |Z1| = u^{4i−j}/M, q = u^{4i}M^4,
> k = pL, d = u^{4i−3j} M, c = |Z2| = u^{4i+2j}/M^2 (all integers; n/d = c/k = u^{3j}/M^5).
> Take R = X × Y0, S ⊇ Y0 × Z1, a private a-element S-predecessor set Y_{2,z} for every
> z ∈ Z2, complete T-blocks pairing d vertices of X with k vertices of Z2, and q private
> dead Z0-predecessors for every x (handshakes ca = nq = u^{8i}, cd = nk; no triangles).
> Then for the three-rotation union: N = 3(2u^{8i} + u^{8i−j}/M + u^{8i−2j}/M^2 +
> u^{8i−3j}M) ∈ [6u^{8i}, 15u^{8i}]; each forward squared-degree sum is
> 3u^{12i−4j} + 2u^{8i}, each reverse sum exceeds it, so B2 = 3u^{12i−4j} + 2u^{8i} ∈
> [3u^{12i−4j}, 5u^{12i−4j}]; and for every eligible deterministic routine A there is one
> global labeling ℓ_A (Y interleaved so that every T-option call costs ≥ 2a − 1; Z2 after
> Z1 ∪ Z0; the private dead keys of each x shuffled into the p + 1 gaps of Z1, all shuffles
> realized by one order) with
> Q_A ≥ n·a·D = (M/2)·u^{12i−3j}, D = pL/2.
> Since M = (log2 u)^{1/4} = Θ((log N)^{1/4}) and N^{3/8} B2^{3/4} = Θ(u^{12i−3j}), this
> matches P1.7 up to a constant on every slope κ = 3/2 − j/(2i) ∈ [1, 3/2). At i = j,
> B2 = Θ(N) and sup_ℓ Q_A = Ω(N^{9/8}(log N)^{1/4}); with P1.7 the worst-case sorted-model
> scale at B2 ≍ N is Θ(N^{9/8}(log N)^{1/4}). Quantifiers: for every routine there is a
> labeling (a single labeling hard for all routines cannot exist). Corollary: no universal
> constant c gives Q_A ≤ c·(N + (|R||S||T|)^{1/8} min(Λ,Λ')^{1/2}) in the sorted model; the
> ratio grows as (log N)^{1/4}. The explicitly interleaved G8 and F_{i,j} (P1.4, P1.6) have no
> logarithmic overhead; the quarter logarithm appears only in the worst case over labelings
> against a fixed routine.

Changes: new theorem; Cor 5.6's "exactly 9/8" becomes "exactly 9/8, and Θ(N^{9/8}(log N)^{1/4})
for comparison-based sorted intersections"; §11 item 5 first half closed (log factor
necessary, and it is exactly a quarter logarithm).

**P1.13 Exact finite check at i = j = 1, h = 4. ACCEPT** (both reproduce
N = 3(2^524289 + 2^458748 + 2^393208 + 2^327684), B2 = 5·2^524288, Q_lower = 2^589827, bit
lengths (524291, 524291, 589828), and (Q_lower − N)^8 > (N/3)^3 B2^6 with exact integer
quotient 134).

> *Remark.* At the smallest member with h = 4 the integer form of Thm 5.3,
> (C − N)_+^8 ≤ |R||S||T|·Q^2, already fails for the sorted-model cost Q_A (ratio ≈ 134 ≈
> (M/2)^8/(2^3·5^6)); no instance is materialized, the labeling exists by P1.12.

**P1.21 Randomized routines. REPAIR** (B: the report's one-sentence averaging argument needs
a Markov step; A did not examine it).

> *Fix (statement to use).* For a zero-error randomized routine with seed σ, each fixed seed
> is a deterministic routine, so Pr_ω[cost < D] ≤ 2^{−pL/2} for a uniform shuffle ω; hence
> E_ω[f(ω)] ≤ 2^{−pL/2} with f(ω) = Pr_σ[cost < D], and by Markov Pr_ω[f(ω) ≥ 1/2] ≤
> 2^{1−pL/2}. A union bound over the 3na critical calls gives 6na·2^{−pL/2} < 1 (log2(6na) <
> 3 + 8iL < 16iL ≤ D), so one labeling makes every critical R-call cost ≥ D/2 in expectation,
> and E[Q_A] ≥ n·a·D/2 = (M/4)·u^{12i−3j}. The conclusion of P1.12 survives for zero-error
> randomized routines up to the factor 2.

### Engine measurements and verification

**P1.17 Faithful port of the engine's intersection. ACCEPT** (A: line-by-line comparison with
`sorted_runs.zig` 361–489 and `triangle_join.zig` 750, plus a Zig harness compiled with
zig 0.16.0 against the verbatim file; B: independent port, 12,004 brute-force cases).

> *Remark (for §12 Engine integration / Artifacts).* `intersectEachBy` walks the shorter
> run and, on equal lengths, its first argument; the triangle call site passes
> `intersectEachBy(n2, n3)` with n2 the run of the walked tuple's far endpoint and n3 the
> run of the root, so option R calls (Z1, T_x) and option T calls (Y_{2,z}, Y0). On an
> alternating pair of length-s runs the engine's routine (16-step linear prefix, then
> doubling, then binary search) performs 6s − 3 key predicates in the walking-first
> orientation ((s−1) lookahead equalities + (2s−1) disorder checks + (2s−1) gallop
> comparisons + s match equalities) and 6s − 5 reversed, with Zig `work` meter 3s − 1 in
> either orientation; no gallop advances more than one position on these witnesses.

**P1.18 G8 measurements with the port, m = 2..5. ACCEPT** (A: recomputed q_R, q_T,
selections, Q and the hand-checked identities; B: every row of every root/option through
its own port, 1,472 / 32,562 / 305,152 / 1,756,250 calls).

> *Remark.* On the relabeled U(m), per critical x the engine's routine costs q_R(x) =
> 6m^5 − 2m^2 and q_T(x) = 6m^5 + m^4 − 4m^3 (comparisons plus outer visits); the
> comparison-plus-outer optimum selects T at m = 2,3 and R for m ≥ 4; each root costs
> Q(m) = m^4 min(q_R, q_T) + m^8 + m^5 = 3104, 122715, 1631232, 12081250 (Q/m^9 = 97/16,
> 505/81, 1593/256, 3866/625), and Q(m) = 6m^9 + m^8 − 2m^6 + m^5 for m ≥ 4: an exact
> degree-9 polynomial against N of degree 8 (Q(4)/Q(2) = 50976/97, N(4)/N(2) = 4768/23).
> Zig work plus outer visits: 1824, 65853, 852992, 6253125; optimal ternary plus outer:
> 1312, 46170, 590848, 4300000; selected-plan comparisons 2432, 107163, 1560576, 11671875
> with outer visits 672, 15552, 70656, 409375; pure-comparison minima 6m^9 − 5m^7.
> Scope: modeled per-binding optima of intersection-port counts; relation seeks, sorting and
> planning are excluded.

**P1.19 Verification scope (15,876 bag-pair checks, 9,920 lower-bound searches, one stop and
one disorder case; 144, 1539, 8448, 31875 port calls). ACCEPT** (A: reran the report's
scripts, identical; B: not executed but arithmetically consistent, own tests cover the same
paths).

**P1.20 Scope limit: not a bound for unrestricted comparison-based join algorithms.
ACCEPT** (both: semijoin pruning of unpadded G8 and memoization of identical calls defeat the
per-row sum; consistent with Prop 5.16).

> *Remark (after the new theorems).* The lower bounds are for fresh calls. In unpadded G8,
> one semijoin pass (Z1 has no T-tuples, so Y0 × Z1 and then X × Y0 are deleted) leaves only
> cheap structure; and all d_R^+(x) R-calls at a binding x are the identical pair (Z1, T_x),
> so memoizing calls reduces the critical root to m^4 distinct calls. Both are outside the
> model; Prop 5.16 shows degree metadata can determine an instance. Algorithms using
> different orders on value ranges (ADOPT; §11 item 5, second half) remain open.

---

## 2. P2 — exponent questions of §11 (items 1, 2, 6, 7)

Directory: `P2-exponents/`. Lens A reran all five report scripts (identical
output) and tested the inequalities on 10,500 random/skewed instances plus hill climbs; lens
B rebuilt every gadget from its textual definition (`check_D.py`, `check_H.py`,
`check_I.py`, `check_ineq.py`) and tested on 10,720 + 7,169 random instances. All costs are
the paper's min-side per-binding charges (§5.1), not galloping comparisons.

### (b) Slopes κ ∈ (5/6, 1): a second ℓ2 bound and its sharpness

**P2.1 New universal per-binding bound. ACCEPT** (A: proof line by line, exponents with
Fractions, 10,500 instances, max ratio 2^{−48}; B: 10,720 + 36 structured instances, cited
extreme ratio reproduced exactly).

> *Theorem (second per-binding ℓ2 bound; companion to Thm 5.3).* For every instance with
> N > 0, C ≤ N + 3^{1/8} N^{−1/8} B2^{5/4}; in integers, N^3 (C − N)_+^{24} ≤ 27 Q^{10} with
> Q = min(αβγ, α'β'γ'). Proof: with H_v = C_v minus the sizes of the two relations walked at
> root v, (C − N)_+ ≤ min(H_x, H_y, H_z) (Lemma 5.2's split); Lemma 5.2 gives H_x ≤ |S|^{3/8}
> α^{1/4} β^{1/8} γ^{3/8} and |S| ≤ β (d^2 ≥ d) gives H_x ≤ α^{1/4} β^{1/2} γ^{3/8},
> H_y ≤ β^{1/4} γ^{1/2} α^{3/8}; so (C − N)_+ ≤ H_x^{2/3} H_y^{1/3} ≤ (αβγ)^{5/12} α^{−1/8}.
> Reflect so that the forward product realizes Q, then rotate so that R is a largest relation
> (both preserve C and N; rotation permutes the moments cyclically), whence α ≥ |R| ≥ N/3.
> The bound is sharper than Thm 5.3 exactly when B2 < N/3 (the main terms' ratio is
> √(3B2/N)); both have exponent 9/8 at κ = 1. Largest observed ratio of the integer form:
> 9.567·10^{−16} at (N, C, Q) = (211, 601, 188201832).

Changes: new theorem in §5.2 (Thm 5.3'); fig-fbeta's solid curve becomes
max(1, (10κ−1)/8) for κ ≤ 1 and 3/8 + 3κ/4 for κ ∈ [1, 3/2]; the shaded region disappears.

**P2.2 C = O(N + B2) for κ ≤ 9/10; Thm 5.3 is not sharp on (5/6, 1). ACCEPT** (both).

> *Corollary (replaces Cor 5.4(2)).* If B2 ≤ c·N^κ then C ≤ N + 3^{1/8} c^{5/4}
> N^{(10κ−1)/8}; in particular C ≤ (1 + 3^{1/8}) N < 2.15 N whenever B2 ≤ N^{9/10}, so the
> per-binding gap against N + B2 is 0 for every slope κ ≤ 9/10 (previously only κ ≤ 5/6).
> The exponent (10κ−1)/8 of the new bound is below Thm 5.3's 3/8 + 3κ/4 by (1 − κ)/2 on
> (5/6, 1), so Thm 5.3 is not tight there.

Changes: Cor 5.4(2); §11 item 2 (first half) answered: Thm 5.3 is not tight on (5/6,1); the
true worst-case exponent is max(1, (10κ−1)/8) (lower bound from P2.4–P2.6).

**P2.3 Building block D(L,a,h). ACCEPT** (A: 80 parameter triples brute force, 0 mismatches;
B: 120 triples incl. a < h, a = h, a > h).

> *Definition and statistics.* For integers L, a, h ≥ 1 with h | L, b = L/h, tagged classes
> X = [h]×[b], Y0 = [a], Y2 = [h]^2×[a], Z1 = [h], Z2 = [h]^2, and R = X × Y0,
> S = (Y0 × Z1) ∪ {((i,j,k),(i,j))}, T = {((i,j),(i,ℓ)) : i,j ∈ [h], ℓ ∈ [b]}:
> (|R|,|S|,|T|) = (La, ah + ah^2, Lh); (α,β,γ) = (La^2, 2ah^2, L^2);
> (α',β',γ') = (aL^2, a^2(h+h^2), Lh^2); (M_R,M_S,M_T) = (Lah, 0, Lah);
> (C_x,C_y,C_z) = (Lah + L·min(a,h), ah, ah^2); Out = 0.
> Note D(u^{4i}, u^{4i−2j}, u^{4i−j}) = F_{i,j}(u) of Thm 5.9 (degrees coincide).

**P2.4 The asymmetric slope family D1, D2, D3. ACCEPT** (A: all 12 N-terms and 12 cost terms
re-derived, 189 (u,p,q) checked symbolically, 12 random D-triples brute-forced; B: exact
exponent polynomials, three digit-for-digit evaluations).

> *Theorem (slopes 9/10 ≤ p/q ≤ 1).* Let u ≥ 2 and integers p, q with 9/10 ≤ p/q ≤ 1. Take the
> vertex-disjoint union of D1 = D(u^{8p−4q}, u^{6q−4p}, u^{6p−3q}) in its own orientation,
> D2 = D(u^{4q}, u^{4p−2q}, u^{6p−3q}) with its local R, S, T placed as the global S, T, R
> (its X, Y, Z become the global Y, Z, X), and D3 = D(u^{4p}, u^{6p−4q}, u^{6q−3p}) with
> local R, S, T placed as the global T, R, S. All parameters are integers with h_i | L_i
> (exponent differences 2p−q, 7q−6p, 7p−6q ≥ 0) and a_i ≤ h_i (10p−9q, 2p−q, 10q−9p ≥ 0).
> Then (α,β,γ) = (4u^{8q}, 4u^{8p}, 4u^{16p−8q}), each reverse moment is at least its forward
> counterpart (α' = 2u^{12p−2q} + u^{9p−2q} + u^{6p+4q}, β' = u^{9q−2p} + 2u^{4p+6q} +
> u^{12q−2p}, γ' = 2u^{20p−10q} + u^{14p−7q} + u^{14p−4q}), so B2 = 4u^{8p};
> C = C_x = u^{10p−q} + u^{4p+2q} + u^{16p−8q} + u^{3p+2q};
> N = 2u^{4p+2q} + u^{2p+3q} + u^{8p} + u^{14p−7q} + u^{10p−5q} + u^{16p−8q} + u^{6p+q} +
> u^{10p−4q} + u^{3p+2q} + u^{8q} + u^{p+6q}; and u^{8q} ≤ N ≤ 12u^{8q},
> u^{10p−q} ≤ C ≤ 4u^{10p−q}.

Editorial (B): state the rotation mapping explicitly as above; the table phrase "local (R,S,T)
becomes (S,T,R)" is correct only under the reading "local R becomes global S".
Exact evaluations (both lenses): (u,p,q) = (2,9,10): N = 1214275593117998941995008,
B2 = 18889465931478580854784, C = 1208944338557034410541056,
C/(N+B2) = 1099528470656/1121557087617 (< 1, the transition point); (2,10,11): N =
310776595586757567692406784, B2 = 4835703278458516698824704, C = 618974746625362625149534208,
ratio 17592320393344/8970241051009; (2,19,20): ratio 1208925837629027751297152/1203668645819051934081
≈ 1004.4.

**P2.5 Finite table at p = q = 1 (three rotations of D(u^4,u^2,u^3) = F_{1,1}(u)). ACCEPT**
(both by literal enumeration): u = 2: N 1440, B2 1024, C 864; u = 3: 29160, 26244, 27216;
u = 4: 261120, 262144, 332800 (each relation 480/9720/87040, each M_π 1024/39366/524288,
Out = 0).

**P2.6 Sharp exponent on (9/10, 1), rational and irrational κ. ACCEPT** (A: ratio/N^{1/16} →
1 at κ = 19/20, C/(new bound) constant 0.1541 for u = 2,4,8,16 while C/(N^{3/8}B2^{3/4}) → 0;
B: bounded-factor argument for p = ⌊κq⌋).

> *Theorem (worst-case per-binding exponent at slopes in (5/6, 1)).* For every real
> κ ∈ (9/10, 1) there are instances (u = 2, q → ∞, p = ⌊κq⌋) with B2 = Θ(N^κ) and
> C = Θ(N^{(10κ−1)/8}), hence C/(N + B2) = Θ(N^{(10κ−9)/8}) → ∞; with P2.1 the worst-case
> exponent of C at slope κ is exactly (10κ − 1)/8, and the new bound is attained up to a
> constant (C ≥ (3^{1/8}·4^{5/4})^{−1} times its main term asymptotically). For
> κ ∈ (5/6, 9/10] the exponent is 1. So C = O(N + B2) fails, even with any fixed polylog
> factor, exactly on (9/10, 1).

Changes: Thm 5.9 gains the asymmetric family (Thm 5.9'); the paragraph after Thm 5.9 and
§11 item 2: only irrational κ ∈ (1, 3/2) remain open.

**P2.7 (reports' "[Refuted]") Thm 5.3's exponent 3/8 + 3κ/4 is not sharp on (5/6, 1).
ACCEPT** — the correct reading of the report's refutation; see P2.2/P2.6.

### (c) Best of six fixed orders: exact gap 1/5

**P2.8 Sharp inequality for the best rotation. ACCEPT** (A: proof checked, 10,500 instances
+ hill climbs, max ratio 1 at complete tripartite; B: all six per-rotation forms, equality on
K_{a,b,c} for six shapes).

> *Theorem (best of six against the ℓ2 moments).* On every instance
> min(M_R, M_S, M_T)^5 ≤ |R||S||T| · min(αβγ, α'β'γ'), i.e.
> min_π M_π ≤ (|R||S||T|)^{1/5} B2^{3/5} ≤ (N/3)^{3/5} B2^{3/5}. Proof: with a_x = d_R^+(x),
> t_x = d_T^−(x), P_x = Σ_{y∈R(x)} min(d_S^+(y), t_x) one has P_x ≤ a_x t_x and
> P_x ≤ √(a_x β), so P_x ≤ β^{1/5} a_x^{4/5} t_x^{3/5}; Hölder (5/2, 5/3) gives
> M_R ≤ |T|^{3/5} α^{2/5} β^{1/5}; rotations give M_S ≤ |R|^{3/5} β^{2/5} γ^{1/5},
> M_T ≤ |S|^{3/5} γ^{2/5} α^{1/5}; multiply and take the cube root; reflection gives the primed
> product. The constant 1 is attained by every complete tripartite instance (M_π = abc,
> |R||S||T| = (abc)^2, both moment products (abc)^3).

**P2.9 Consequences and the exact gap 1/5. ACCEPT** (both: v^{3/5}/(1+v) maximal at v = 3/2;
GMIN rows reproduced).

> *Corollary (closes §11 item 6).* min_π M_π ≤ (2^{2/5}/5)·N^{1/5}(N + B2) ≈ 0.2639
> N^{1/5}(N + B2), and min_π M_π ≤ 12^{−3/5}(N + B2)^{6/5} ≈ 0.2252 (N + B2)^{6/5}. Since a
> GAO with second relation π costs |π| + M_π ≤ N + M_π (Lemma 5.1) and GMIN (Thm 5.10(2))
> attains min_π M_π/(N + B2) = m^3/(6m^2+3m+3) = Θ(N^{1/5}), the best of the six GAOs has
> worst-case gap exactly 1/5 against N + B2 and worst-case cost Θ((N + B2)^{6/5}). The
> inequality also delivers both halves asked for in §11 item 6 at once: for B2 < N it gives
> min_π M_π ≤ 3^{−3/5} N^{6/5}.

Changes: Remark 5.11 and §11 item 6 ("open ... suggests the answer is yes") become proved;
Table tab-gaps row "best of six GAOs" becomes exact 1/5.

**P2.10 Gadget H(L,a,h); GMIN = three rotations of H(m^3,m,m^2); GMR = H(m^3,m,m). ACCEPT**
(A: 100 triples brute force; B: 216 triples, literal GMIN m = 1..8 and GMR m = 1..12).

> *Statistics.* H(L,a,h): |X| = L, |Y| = a, |Z1| = h, Z0 = {z_{x,j}}, R = X × Y, S = Y × Z1,
> T = {(z_{x,j}, x)}: (|R|,|S|,|T|) = (La, ah, Lh); (α,β,γ) = (La^2, ah^2, Lh);
> (α',β',γ') = (aL^2, ha^2, Lh^2); (M_R,M_S,M_T) = (Lah,0,0); (C_x,C_y,C_z) = (Lh, ah, 0);
> Out = 0. Three rotations of H(m^3,m,m^2) realize GMIN(m): N = 3(m^5+m^4+m^3), forward
> moments 3m^5, reverse 2m^7 + m^4 (2m^7 + m^4 − 3m^5 = m^4(m−1)(2m^2+2m−1) ≥ 0), B2 = 3m^5,
> every M_π = m^6, every C_v = m^5 + m^3, Out = 0 (literal m = 1..8: N 9, 168, 1053, 4032,
> 11625, 27864, 58653, 112128; M/(N+B2) = 1/12, 8/33, 9/22, 64/111, 125/168, 72/79, 343/318,
> 512/411).

### (d) One prescribed fixed order: exact gap 1/4 on general inputs

**P2.11 Single-driver inequalities. ACCEPT** (A: proof incl. the y-grouped form, equality on
GMR and complete tripartite; B: all three drivers, max ratio 1).

> *Theorem.* M_R^4 ≤ |R||T|^2 αβ ≤ |R||T|·αβγ and M_R^4 ≤ |R||S|^2 α'γ' ≤ |R||S|·α'β'γ'.
> Proof: weighted Cauchy–Schwarz M_R^2 ≤ |T| Σ_{t_x>0} P_x^2/t_x; min(b,t)^2 ≤ bt gives
> P_x^2/t_x ≤ a_x Σ_{y∈R(x)} b_y; regrouping by y with v_y = Σ_{x∈R^−(y)} a_x,
> Σ_y b_y v_y ≤ √β √(Σ v_y^2) and v_y^2 ≤ d_R^−(y)·α, Σ_y v_y^2 ≤ |R|α; so
> M_R^2 ≤ |T|√(|R|αβ); γ ≥ |T|. Grouping by y instead gives the primed form (β' ≥ |S|).

**P2.12 Consequences; exact gap 1/4; sharp coefficient. ACCEPT** (A: v^{3/4}/(1+v) maximal at
v = 3, limit on H(u^3,6u,6u) exact; B: fourth-power identity, literal tables).

> *Corollary (closes the first half of §11 item 7).* For any prescribed driver,
> M_R ≤ (N/2)^{1/2} B2^{3/4} ≤ (3^{3/4}/(4√2))·N^{1/4}(N + B2) ≈ 0.4030 N^{1/4}(N + B2).
> With GMR (Thm 5.10(1), M_R/(N + B2) = m^3/(3m^2+1) = Θ(N^{1/4})) the single-GAO gap
> against N + B2 is exactly 1/4 and its worst-case cost is Θ((N + B2)^{5/4}), on general
> inputs. The coefficient is asymptotically sharp: H(u^3, 6u, 6u) has N = 12u^4 + 36u^2,
> B2 = 36u^4, M_R = 36u^5 and M_R/(N^{1/4}(N + B2)) → 36/(12^{1/4}·48) = 3^{3/4}/(4√2)
> (ratios M_R/(N+B2) = 3/7, 24/19, 27/13, 192/67, 375/103, 216/49 for u = 1..6).

**P2.13 Scope of (d): semijoin-reduced inputs. REPAIR** (B: the report and its summary table
say "exact gap 1/4" without qualifying the input class; §11 item 7 lists the semijoin-reduced
interval separately; GMR is not semijoin-reduced and padding it only yields Ω(N^{1/6}) since
the padded forward product is O(m^13)).

> *Fix (sentence to add).* On general inputs the single-GAO gap is exactly 1/4. On pairwise
> semijoin-reduced inputs it now lies in [1/5, 1/4] (upper bound from the corollary above,
> lower bound from padded GMIN, Thm 5.10(2)) and remains open.

Changes: Remark 5.11, §11 item 7 (single GAO: 1/4 exact in general, [1/5, 1/4] reduced;
fixed root still [1/8, 1/2]); Table tab-gaps.

### (a) Fully reduced inputs: δ ∈ [1/12, 1/8], with an obstruction

**P2.14 Fully reduced gadget I_v. ACCEPT** (A: hand re-derivation, brute force v = 1,2,3 with
every-tuple-supported check, v = 4 literal enumeration 29.5 s / 2.8 GB; B: independent
int/bitset evaluator, v = 1..4, all tuples supported).

> *Construction.* Coordinates in [v]; X = {(A,B) : A,B ∈ [v]^3}, Y0 = [v]^4, Z1 = [v]^5,
> Y2 = {(A,B,E,e)}, Z2 = {(A,E,F) : F ∈ [v]^2}; f(A,B) = (A,B1,B2) ∈ Z1;
> R = X × Y0 ∪ {((A,B),(A,B,E,e))}, S = Y0 × Z1 ∪ {((A,B,E,e),(A,E,F))},
> T = {(f(x), x)} ∪ {((A,E,F),(A,B))}. Every tuple lies in a triangle; Out(I_v) = v^10 + v^12;
> (|R|,|S|,|T|) = (2v^10, v^12 + v^9, v^11 + v^6); (α,β,γ) = (4v^14, 2v^14, v^14 + v^7);
> (α',β',γ') = (v^16 + v^10, v^16 + v^13, v^16 + 2v^11 + v^6); C_x = v^15 + v^11 + v^10 + v^6
> (option T at every x, cheaper by v^6 − v^5 + v^4 − 1), C_y = v^12 + 2v^10 + v^9,
> C_z = 2v^12 + v^10 + v^6. (v = 4 literal: sizes (2097152, 17039360, 4198400), forward
> (1073741824, 536870912, 268451840), reverse (4296015872, 4362076160, 4303360000), costs
> (1078988800, 19136512, 34607104), Out 17825792.)

**P2.15 Union U_v and its tables. ACCEPT** (both; literal v = 1,2, closed forms v ≤ 8).

> *Theorem (fully reduced separation).* U_v, the disjoint union of I_v and its two rotations,
> is fully reduced with N = 3(v^12 + v^11 + 2v^10 + v^9 + v^6), C = v^15 + 3v^12 + v^11 +
> 4v^10 + v^9 + 2v^6, B2 = 7v^14 + v^7 (reverse sums 3v^16 + v^13 + 2v^11 + v^10 + v^6,
> larger for v ≥ 2, equal at v = 1), Out = 3(v^12 + v^10). Hence C/(N + B2) ~ v/7 =
> Θ(N^{1/12}) and C = Θ((N + B2)^{15/14}); v = 8 is an explicit fully reduced instance with
> C > N + B2 (ratio 45017942/39450457). Tables: v = 1: 18/8/12/6 (ratio 6/13); v = 2:
> 26304/114816/51840/15360 (18/49); v = 3: 2541294/33482970/16377714/1771470 (11233/24708);
> v = 4: 70004736/1879064576/1132732416/53477376 (276546/475847); v = 5..8 ratios
> 334292/465793, 10230842/11929041, 4073331/4077242, 45017942/39450457.

**P2.16 Intervals and the obstruction. ACCEPT** (both: Out ≥ max(|R|,|S|,|T|) ≥ N/3 on fully
reduced instances, Out ≤ B2 re-proved by entropy/Jensen and tested).

> *Statement (updates §11 item 1).* On fully reduced inputs the per-binding gap against
> N + B2 satisfies 1/12 ≤ δ ≤ 1/8, and the exponent ρ in C = (N + B2)^{ρ+o(1)} satisfies
> 15/14 ≤ ρ ≤ 9/8 (upper bounds: Cor 5.4(1) and Thm 5.3). The family attains Thm 5.3's
> exponent at slope κ = 7/6. Obstruction: a triangle contains exactly one tuple of each
> relation, so on a fully reduced instance Out ≥ max(|R|,|S|,|T|) ≥ N/3, and Out ≤ B2
> (ANOS24 Eq. (4)/JRR21) gives B2 ≥ N/3; no fully reduced family has slope κ < 1, so the
> low-slope families cannot be imported. The paper's suggested 1/10 (unverified coset
> construction) is neither confirmed nor excluded; 1/12 < 1/10.

**P2.17 Recovery of Thm 5.3 from Lemma 5.2. ACCEPT** (both; no paper change).

**P2.18 Verification record (python3 -I, exact arithmetic, instance counts, seeds). ACCEPT**
(A reran every script, output identical incl. the extreme ratio; B did not execute the
report's scripts, own runs cover the same inequalities).

**P2.19 Caveat on the engine: `intersectWalk` returns when the longer-run cursor reaches the
end, so the min-side charge is a model, not a galloping lower bound. ACCEPT** (B:
`sorted_runs.zig` line 463; the P2 report makes no comparison-count claims).

**P2.20 Scope note: irrational κ ∈ [1, 3/2] and the sharp fully reduced exponent are not
settled. OPEN (no claim)** (A: noted so the report is not over-credited).

---

## 3. P3 — spectral AGM with two measured norms (option (c)), and a 4-cycle obstruction

Directory: `P3-spectral/`. Lens A reran the report's scripts (identical output) and
wrote `random_upper_bound.py` (exact PSD tests), `construction_grid.py` (1,193,589 cases),
`nine_term_irredundancy.py`, `sharp_bruteforce.py`, `driver_T_unbounded.py`,
`padding_check.py`, `cycle4_blocks.py`; lens B wrote `brute_force.py` (true operator norms
decided exactly by Sylvester/Fraction determinants, exhaustive on small shapes),
`construct.py`, `nine_terms.py`, `misc_checks.py`, `cycle4.py`.

**P3.1 Two-norm theorem. ACCEPT** (A: it is Thm 3.1 at σ_T = √r_T, 2,900 random instances,
1.19 M grid cases, worst U2/Out ≈ 3.79 < 4; B: exhaustive 0/1 triples on (2,2,2), (2,3,2),
(3,2,2), (2,2,3) and random up to 5×5 with exact norms, 0 failures; grids of 154,350 and
47,916 cases).

> *Corollary 3.9 (two measured norms).* Let |R| ≤ r_R, |S| ≤ r_S, |T| ≤ r_T, ‖A_R‖ ≤ σ_R,
> ‖A_S‖ ≤ σ_S, with no norm bound on T, all five bounds ≥ 1; put p = min(σ_R^2, r_R),
> q = min(σ_S^2, r_S) and
> U2 = min{ √(p r_S r_T), √(q r_R r_T), r_R q, r_S p, r_T p, r_T q }.
> Then U2/4 < W2 ≤ U2, where W2 is the supremum of Out over the class; the upper constant 1
> is attained and the lower constant 1/4 is best possible (P3.4). U2 equals the nine-term U
> at σ_T = √r_T (s_T = r_T): H_T, D_{R,T}, D_{S,T} are then dominated by H_R, D_{T,R}, D_{T,S},
> so nothing is lost against §3 with the missing norm replaced by its Frobenius bound. If a
> nonnegative supplied bound is below 1 the relation is empty and W2 = 0; a negative bound
> gives the empty class, value 0 by the §2 convention.

Changes: new corollary in §3.4 next to Cor 3.8.

**P3.2 Upper-bound proof (degrees ≤ p, q; four counting terms; two Hölder terms; no norm of
T used). ACCEPT** (both re-derived line by line).

**P3.3 Lower-bound construction. ACCEPT** (both: real shape â = max(1,U2/r_S),
b̂ = max(1,U2/r_T), ĉ = max(1,U2/r_R) satisfies âb̂ ≤ p, b̂ĉ ≤ q, ĉâ ≤ r_T (this last step is
where the missing T-norm is absorbed: U2 ≤ r_T p ≤ r_T r_R, U2 ≤ r_T q ≤ r_T r_S,
U2^2 ≤ p r_S r_T ≤ r_R r_S r_T); m* ≥ 1; m*âb̂ĉ = U2; floors give Out = mabc > U2/4; the
report's grids 10,368 / 5,488 reproduced with the same maxima 45/4 at (5,7,6;5,6) and 15/2
at (3/2,2,5/2;3/2,2)).

> *Witness.* Blk(a,b,c,m) with a = ⌊â⌋, b = ⌊b̂⌋, c = ⌊ĉ⌋, m = ⌊min(r_R/ab, r_S/bc, r_T/ca)⌋
> (the block of Thm 3.1 with U replaced by U2) is admissible without any norm on T and has
> Out > U2/4.

**P3.4 Sharpness of 4 in the two-norm class. ACCEPT** (A: exhaustive 3×3 brute force at
t = 3/2 and 19/10, max Out 1; Pell rows; B: 44,200 instances at t = 49/25, max Out 1).

> *Theorem (Thm 3.7 without the T-norm).* For 1 ≤ t < 2, r = (t^2, t, t^2), σ_R = √t,
> σ_S = 1 give p = t, q = 1, the six terms (t^2, t^2, t^2, t^2, t^3, t^2), U2 = t^2 and
> W2 = 1 (|S| ≤ 1 and every column degree of R is ≤ 1, no norm of T needed); hence
> inf W2/U2 over regular two-norm statistics is 1/4 and is not attained. The rational Pell
> rows (7,5), (41,29), (239,169), (1393,985), (8119,5741) give U2 = 2401/625, 2825761/707281,
> 3262808641/815730721, 3765342321601/941336550625, 4345203949621921/1086301020364561, block
> (1,1,1,1), Out = 1.

**P3.5 All six terms are necessary. ACCEPT** (both recomputed the 6×6 exponent matrix and
materialized the blocks at n = 2, 3, 7, 16 with exactly computed norms).

> *Proposition.* For every n ≥ 2 the following regular statistics make the named term the
> unique minimum of U2, the stated block attains Out = U2 exactly (so W2 = U2), and deleting
> the term raises the minimum by the factor n: H_R: r = (n^4,n^4,n^4), (p,q) = (n^2,n^4),
> Blk(n,n,n,n^2), Out n^5; H_S: same r, (p,q) = (n^4,n^2), same block, n^5; D_{R,S}:
> r = (n^2,n^6,n^6), (n^2,n^2), Blk(1,1,n^2,n^2), n^4; D_{S,R}: r = (n^6,n^2,n^6), (n^2,n^2),
> Blk(n^2,1,1,n^2), n^4; D_{T,R}: r = (n^6,n^6,n^2), (n^2,n^4), Blk(1,n^2,1,n^2), n^4;
> D_{T,S}: same r, (n^4,n^2), same block, n^4. (Exponent rows: H_R (5,6,8,6,6,8), H_S
> (6,5,6,8,8,6), D_{R,S} (7,5,4,8,8,8), D_{S,R} (5,7,8,4,8,8), D_{T,R} (5,6,10,8,4,6), D_{T,S}
> (6,5,8,10,6,4).)

**P3.6 Extension: all nine terms of U are necessary. ACCEPT** (A: 21,952 exponent regimes
enumerated, explicit witnesses for all nine terms at n = 2, 3; B: two witness families and
their S_3 orbit, materialized at n = 2, 3, 5 with exact norms; independent exponent search
found 121 / 1288 witness families per Hölder / degree term).

> *Proposition (irredundancy of Thm 3.1's nine terms; strengthens Remark 3.5).* For every
> n ≥ 2 and each of the nine terms there are regular statistics, powers of n, at which that
> term is the unique minimum, the block of Thm 3.1 is admissible with Out = U exactly, and
> deleting the term raises the minimum by the factor n. Witnesses (exponent vectors
> (e_R,e_S,e_T; f_R,f_S,f_T) of (r; s)): H_R: (4,4,4; 2,4,4), Blk(n,n,n,n^2), U = n^5, the
> other eight ≥ n^6; D_{R,S}: (2,6,6; 2,2,4), Blk(1,1,n^2,n^2), U = n^4, the others ≥ n^5; the
> remaining seven terms by the S_3 action that leaves U invariant: H_S (4,4,4; 4,2,4), H_T
> (4,4,4; 4,4,2), D_{R,T} (2,6,6; 2,4,2), D_{S,R} (6,2,6; 2,2,4), D_{S,T} (6,2,6; 4,2,2),
> D_{T,R} (6,6,2; 2,4,2), D_{T,S} (6,6,2; 4,2,2). Caveat (A): choose integer-exponent
> regimes; e.g. (6,3,3; 3,3,3) has H_R unique minimum with exponent 9/2 and the floored block
> gives Out = 16 < U ≈ 22.6 at n = 2 (within the factor 4, not equality).

Changes: new proposition in §3 (after Remark 3.5).

**P3.7 Relation to the nine-term formula. ACCEPT** (both; folded into P3.1).

**P3.8 Exact integer cardinalities. ACCEPT** (both: isolated edges on fresh endpoints are
norm-1 block-diagonal components, create no triangle; `padding_check.py`, `misc_checks.py`).

> *Remark (closes the equality-constraint part of §11 item 11, for all of §3).* For regular
> (r, σ) with integer r_i, sup{Out : |i| = r_i, ‖A_i‖ ≤ σ_i for all i} = W(r, σ): any
> admissible instance pads to exact sizes with isolated edges on fresh endpoints, which add
> norm-1 components (‖A_i‖ becomes max(‖A_i‖, 1) ≤ σ_i) and no triangles, while the
> exact-size class is a subclass. The same holds for the two-norm class of Cor 3.9.

**P3.9 Planner consequence. ACCEPT** (A: proofs match Prop 4.2 with D_{R,T}, D_{S,T} dropped;
73,984 budget cases max ratio 1; complement found: driver T is not worst-case optimal;
B: all eight probe inequalities on every exhaustive/random triple).

> *Corollary 4.5 (two measured norms suffice for the planner).* On every admissible instance
> M_R ≤ min(√(p r_S r_T), r_R q, r_S p, r_T p) and M_S ≤ min(√(q r_R r_T), r_S p, r_R q, r_T q);
> every term of U2 occurs in one of the lists, so min(M_R, M_S) ≤ U2 < 4W2. A planner
> drives R when a minimizing term is H_R, D_{S,R} or D_{T,R}, and S when it is H_S, D_{R,S}
> or D_{T,S}. The restriction to the two measured relations is necessary: with R and S
> perfect matchings on k vertices and T = K_{k,k}, p = q = 1, r = (k, k, k^2),
> U2 = W2 = Out = M_R = M_S = k while M_T = k^2, so M_T/U2 = k is unbounded.

Changes: new corollary in §4; §12 planner discussion (stride estimator) can cite it.

**P3.10 Cost-model qualification (probe-work bound O(N + U2); no log-free comparison bound
for the galloping engine). ACCEPT** (both; B read `sorted_runs.zig` 361–475).

**P3.11 Exact computational checks (grid counts 10,368 / 5,488, maxima 45/4 and 15/2 with
witnesses, 24 irredundancy cases with squared deletion ratios 4/9/49/256, Pell table,
4,096 matrix triples / 73,984 budget cases / 55,815 positive / 0 failures). ACCEPT** (both
reproduced every number).

**P3.12 Four-cycle obstruction. ACCEPT** (A: exhaustive enumeration of admissible
Blk4(a,b,c,d,m), unique feasible (1,1,1,1,1); B: own gadget rebuild n ≤ 64, brute-force W4
on small shapes = n).

> *Remark (for §11 item 10).* For the 4-cycle R(x,y)S(y,z)T(z,w)Q(w,x) at sizes
> r = (1, n, n, n) and squared norms s = (1, n, 1, n) (attained by R = {(x,y)},
> S = {(y,z_i)}, T = {(z_i,w_i)}, Q = {(w_i,x)}), the worst case is W4 = n exactly
> (Out ≤ |R||T|, since a 4-cycle tuple is determined by its R-edge and its T-edge), while
> every vertex-disjoint union of complete four-partite blocks admissible at these bounds has
> at most one tuple (|R| ≤ 1 forces one block with a = b = 1, and cd ≤ s_T = 1 forces
> c = d = 1). So the block family of Thm 3.1 does not extend to 4-cycles with a constant
> factor; any matching construction must use shared endpoints, stars or matchings.

**P3.13 Script-provenance sentence for the obstruction. REPAIR** (A: `cycle4_obstruction.py`
sets `block_best = 1` as a constant, so "it produced ... complete-component optimum 1 in every
case" overstates what the script computed; the mathematics is correct and A's
`cycle4_blocks.py` computes it).

> *Fix.* Reword to: the script checks the witness (Out = n) and the bound Out ≤ |R||T|; the
> block optimum 1 is established by the two-line argument (or computed by enumeration as in
> the verifier's script).

**P3.14 Degenerate cases (bound below 1 empties the relation; negative bound gives the empty
class). ACCEPT** (both; matches §2).

**P3.15 Scope of "option (c) is settled". REPAIR** (A: the theorem covers exactly two
measured norms; the one-norm case with all three sizes is not written out; B did not flag
it).

> *Fix (paragraph to add, same corollary of Thm 3.1).* With only σ_R measured and all three
> sizes known (σ_S = √r_S, σ_T = √r_T), the nine terms reduce to
> U1' = min{ √(p r_S r_T), r_S p, r_T p, r_R r_S, r_R r_T, r_S r_T }, p = min(σ_R^2, r_R),
> and U1'/4 < W ≤ U1'; Cor 3.8 is the case r_R ≥ max(σ^2, r_S r_T) with r_S ≤ r_T (the
> r_R-terms and r_T p drop out, leaving U1). Alternatively narrow the headline to "two
> measured norms".

**P3.16 General four-cycle characterization. OPEN (no claim)** (both: appropriately labeled
open-with-obstruction).

---

## 4. Consolidated list of paper changes

§1, Table tab-gaps: best of six GAOs: exact 1/5 (P2.9); one fixed GAO: exact 1/4 on general
inputs, [1/5, 1/4] semijoin-reduced (P2.12–P2.13); per-binding: gap 0 for κ ≤ 9/10 and
exponent (10κ−1)/8 on (9/10, 1) (P2.2, P2.6); fully reduced: [1/12, 1/8] (P2.16).

§2, Cost model: replace the unanalysed-galloping clause with a pointer to the sorted-model
subsection (P1.1, P1.7, P1.12).

§3: Cor 3.9 two measured norms (P3.1–P3.4, P3.7, P3.14); Proposition: all nine terms
necessary (P3.5–P3.6); Remark: exact cardinalities by isolated-edge padding (P3.8); one-norm
six-term variant beside Cor 3.8 (P3.15).

§4: Cor 4.5 planner with two measured norms, T not a worst-case-optimal driver (P3.9);
remark that H_R survives galloping with constant 3 (P1.8).

§5.2: Thm 5.3' C ≤ N + 3^{1/8} N^{−1/8} B2^{5/4} (P2.1); Cor 5.4(2) → κ ≤ 9/10 with constant
1 + 3^{1/8} (P2.2); fig-fbeta solid curve max(1,(10κ−1)/8) on κ ≤ 1 (P2.1–P2.6).

§5.3: Thm 5.5/Cor 5.6 and Remark 5.8(a) gain sorted-model clauses (P1.4, P1.5); Thm 5.9
gains the sorted clause (P1.6) and the asymmetric family D1–D3 for every real κ ∈ (9/10, 1)
(P2.3–P2.6); the "open slopes" paragraph shrinks to irrational κ ∈ (1, 3/2).

§5.4: Thm 5.10 gains sorted-model clauses (P1.14–P1.16); new theorems
min_π M_π^5 ≤ |R||S||T|·Q and M_R^4 ≤ |R||T|^2 αβ / |R||S|^2 α'γ' with the exact gaps 1/5 and
1/4 (P2.8–P2.12); Remark 5.11 rewritten (P2.9, P2.13); fully reduced family U_v (P2.14–P2.16).

New §5.x "Sorted intersections": model (P1.1), certificate and interleaving lemmas
(P1.2–P1.3), quarter-log upper bound and price-then-run with prices h (P1.7–P1.8),
quarter-log necessity with the randomized Markov variant (P1.9–P1.13, P1.21), scope remark
(P1.20).

§5.5 Prop 5.14: remark that the scheduler runs on degree-computable prices h in a sorted
store (P1.7).

§12/§13 Engine and artifacts: port measurements and the exact degree-9 polynomial of the
engine's routine on relabeled G8 (P1.17–P1.19).

§11 Open problems: 1 → verified interval [1/12, 1/8] with the obstruction B2 ≥ N/3 (1/10 still
unverified); 2 → first half closed (not tight; exponent max(1,(10κ−1)/8)), second half
(irrational κ ∈ (1, 3/2)) open; 5 → first half closed for fresh calls (log factor necessary,
exactly (log N)^{1/4}), value-range orders open; 6 → closed, yes; 7 → single GAO exact 1/4
general / [1/5, 1/4] reduced, fixed root still [1/8, 1/2]; 10 → add the 4-cycle obstruction;
11 → equality constraints closed, galloping log analysed, bags open.

## 5. Cross-report consistency notes

1. P1.7 and P2.1 use the same per-root chain (Lemma 5.2). Since P1.7's per-root bound is
   Lemma 5.2's with the constant 3^{3/4} L_N^{1/4}, P2.1's manipulation applies verbatim and
   gives, in the sorted model, Ĉ ≤ N + 3^{7/8} L_N^{1/4} N^{−1/8} B2^{5/4}. This combination
   is immediate but was not claimed by either report nor checked by the verifiers; mark it
   accordingly if used.
2. P1.12's quarter-log necessity covers κ = 3/2 − j/(2i) ∈ [1, 3/2); whether the
   (log N)^{1/4} factor is also necessary on (9/10, 1) in the sorted model, against P2.4's
   asymmetric family, is not claimed by anyone.
3. P2's constant-1 sharpness statements are for the min-side charge; in the sorted model the
   analogous constants are 2 (certificate 2s−1 per balanced call, P1.2), e.g. m/7 vs m/14 on
   G8.
4. P3's results hold for the (r, σ) statistics and do not depend on B2; relabeling (P1) does
   not affect them.
5. Both verifiers of P1 note that the "exact" claims are modeled per-binding optima of
   intersection counts with omniscient plan choice; the engine runs one fixed driver, so
   P1.18 is a confirmation of the exponent, not an engine benchmark.
