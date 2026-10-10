# Sorted fresh-call kernels: the sharp quarter logarithm

**Status: proved**, under the following quantifiers. Fix a deterministic generic comparison routine (or finitely many prescribed routines for the potential calls) before the adversary chooses the term order. A call can access only the two sorted runs and their lengths; it must compute their intersection correctly for arbitrary sorted runs. It cannot import certificates from other calls, exploit key arithmetic, or use graph structure to certify an answer without intersecting. Choice of root and of the two options can be by an omniscient oracle. This is stronger than any fixed ordinary merge/galloping/leapfrog routine; it is weaker than unrestricted comparison algorithms for the whole join. Arbitrary label-dependent selection of a different hardcoded decision tree is not allowed.

## Universal upper bound

Put h(p,q)=0 if either argument is zero. Otherwise let s=min(p,q), l=max(p,q), and

    h(p,q)=s(1+ceil(log2(l/s))).

For an absolute K, ordinary doubling galloping intersects two sorted sets in at most K h(p,q) key comparisons and neighbor reads. This follows by doubling and binary search in each skipped gap: a skip of length g costs O(1+log2(g+1)); summing the at most O(s) skips, whose total is O(l), and using concavity of log gives O(s(1+log2(l/s))). Empty intersections can be identified from their supplied lengths. K is independent of all lengths.

Let L_N=1+ceil(log2 N) for N>=2. The following two bounds hold:

    h(p,q) <= L_N p,       h(p,q) <= 3 sqrt(pq).

For the first, when p is shorter use l<=N; when p is longer use h<=2p and L_N>=2. For the second, write m=ceil(log2(l/s)). If m=0 it is immediate. If m>=1, r=l/s>2^(m-1), and (m+1)^2<=9*2^(m-1). The latter follows from the m=1,2 cases and (m+2)^2<=2(m+1)^2 for m>=2.

At root x, let a=d_R^+(x), b=d_T^-(x),

    P=sum_{y in R(x)} h(d_S^+(y),b),
    Q=sum_{z in T^-1(x)} h(a,d_S^-(z)),
    w(x)=sum_{z in T^-1(x)} sqrt(d_S^-(z)).

Exactly the paper's five steps now give

    P <= L_N sqrt(a beta),
    Q <= 3 sqrt(a) w(x),
    min(P,Q) <= P^(1/4) Q^(3/4)
             <= L_N^(1/4) 3^(3/4) beta^(1/8) sqrt(a) w(x)^(3/4).

Holder over x and Cauchy--Schwarz over z yield

    C_hat_x <= |R|+|T|
      + 3^(3/4) L_N^(1/4) alpha^(1/4) beta^(1/8) (gamma |S|)^(3/8).

Here C_hat prices each visited outer tuple by 1+h. Rotate and reflect, multiply the three bounds, and take a cube root:

    C_hat <= N + 3^(3/4) L_N^(1/4)
        (|R||S||T|)^(1/8) min(Lambda,Lambda')^(1/2).

Actual galloping work is O(C_hat). The prices require a single O(N) pass over all six directed tuple views using degree reads. The ceiling logarithm is computed by integer bit lengths and one shift/compare. Thus this is an implementable upper bound, not an oracle-only guarantee.

## Matching necessity of the quarter logarithm

Let h>=1 be an integer and put L=2^h, u=2^L. All numbers below are integers, including d=u^5/L.

Use parts X, Y0, Y2, Z0, Z1, Z2 with:

    n=|X|=u^8,       a=|Y0|=u^6,       p=|Z1|=u^7,
    q=u^8,          k=pL,              d=u^5/L,
    c=|Z2|=nk/d=u^10 L^2.

Let R=X times Y0. Let S contain Y0 times Z1, and for each z in Z2 give z its own disjoint a-element predecessor set Y2_z; all Y2 vertices have S outdegree 1. Thus |Y2|=ca=u^16 L^2. Partition X into n/d groups of size d and Z2 into equally many groups of size k; T is complete from each Z2 group to the corresponding X group. Finally give each x q private predecessors in Z0, each of T outdegree 1. There are nq=u^16 such dead vertices. No triangle exists.

Order Y by layers: for each l=0,...,a-1, put Y0[l] followed by Y2_z[l] for all z. Every positive T-option call intersects perfectly alternating a-element disjoint sets and must make at least 2a-1 comparisons. At every x the T option therefore costs at least k(2a-1)>=apL.

For Z labels, put all Z2 after every Z1 and Z0. For each x, choose a shuffle of its q private Z0 keys with the common ordered p-element Z1 set. There are

    M=binom(p+q,p) >= (q/p)^p = u^p = 2^(pL)

possible shuffles. These choices are independent and consistent with one global order: for each of the p+1 Z1 gaps concatenate the dead keys assigned to that gap, in any fixed order of the x's. The Z2 tail is appended last.

A correct comparison decision tree for disjointness must identify the entire shuffle at every disjoint leaf. Indeed if two shuffles reach the same leaf, some cross pair is incomparable in the partial order induced by the leaf and the two internal sorted orders. Equating that incomparable pair preserves every comparison result and the strict internal orders, but makes the intersection nonempty. This contradicts correctness. Fixed tail comparisons create no extra entropy. Therefore a prescribed call program has at most 2^D disjoint inputs on which it uses fewer than D comparisons: along disjoint paths all comparisons are binary (< or >); predetermined same-entry equalities carry no information.

Choose D=pL/2. Under the uniform shuffle, any prescribed R-option call has probability at most 2^(-pL/2) of costing fewer than D comparisons. In the disjoint union of three rotated copies there are 3na=3u^14 relevant potential R-option calls. Union bound gives one simultaneous labeling for which all of them cost at least D, since

    3u^14 * 2^(-pL/2) < 1.

Explicitly log2(3u^14)<2+14L<16L<=u^7 L/2 for L>=2. The argument allows different prescribed call programs indexed by root/binding/option, provided their behavior does not depend on term comparisons learned in other calls. An omniscient option selector cannot escape because at each x its R option costs at least aD=apL/2 and its T option at least apL. Every root of the rotated union contains one such critical X part. Hence

    C_cmp >= n apL/2 = u^21 L/2.

The exact sizes and moments are

    D_size = u^14+u^13+u^16 L^2+u^15 L+u^16,
    |R_union|=|S_union|=|T_union|=D_size,   N=3 D_size,
    A=alpha=beta=gamma=3u^20+u^16(L^2+1),
    A'=alpha'=beta'=gamma'
      =u^24+2u^23 L+u^22(1+2L^2)+u^19.

Since A'>=u^24> A, B2=A exactly. Also

    3u^16 L^2 <= N <=15u^16 L^2,
    3u^20 <=B2<=4u^20,
    log2 N <=20L.

Consequently the paper's log-free spectral term has order

    (|R||S||T|)^(1/8) B2^(3/4) = Theta(u^21 L^(3/4)),

while C_cmp=Omega(u^21 L). The N term is smaller. Thus the ratio to N plus the log-free bound is Omega(L^(1/4))=Omega((log N)^(1/4)). The universal upper's quarter logarithm is necessary and sufficient.

This necessity is an adversarial existence result for each fixed comparison routine, not a single explicit labeling simultaneously hard to every possible decision tree. Such a universal logarithmic labeling cannot exist: an individual known interleaving admits a short certificate and a routine can test that certificate first. The explicit G8/F alternating labels, in contrast, force their linear comparison lower bounds against every correct fresh-call routine on that very same labeling.

## Explicit finite arithmetic certificate

For h=16, L=65536, u=2^65536, `python3 -I slopes/quarter_log_finite.py` directly checked

    (u^21 L/2 - N)^8 > D_size^3 A^6.

This is exactly the integer form of a violation of the paper's constant-one log-free bound by the comparison lower bound. The graph is not materialized, and its adversarial labels are existential for each fixed routine. Exact output:

    h=16 L=65536 u=2^65536
    bit_lengths N,B2,lower = 1048610 1310722 1376272
    program_count_bit_length = 917506
    R_depth_bit_length = 458768
    certified_lower_eighth_over_spectral_eighth_at_least = 512
    N_less_than_lower_half = True
    lower_minus_N_eighth_exceeds_spectral_eighth = True

The small certificate behind the full integer check is D_size<=2u^16 L^2, A<=4u^20, and therefore lower^8/(D_size^3 A^6)>=L^2/2^23=512; also N<lower/2. The direct calculation was performed as well.

For emphasis, the quarter-log lower statement is: for each fixed eligible algorithm A there exists a global labeling such that the cost Q_A, minimized over root and per-binding option choices, satisfies the displayed bound. It is not a lower bound on the nonuniform quantity obtained by minimizing over all possible correct algorithms separately on each already labeled instance. That latter quantity admits guessed-certificate algorithms and is a different notion.
