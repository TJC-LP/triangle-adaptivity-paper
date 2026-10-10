# Sharp sorted-comparison bounds on every dense slope, including 9/8

**Status: proved** in the fresh-call comparison model defined in `quarter_log_proof.md`. This stronger normalization removes the logarithmic drift of that file's initial family.

For each fixed deterministic generic intersection algorithm (or prescribed call programs), the adversary chooses one global key order. The algorithm must solve arbitrary pairs of sorted runs. It receives only their contents and lengths, with opaque keys. No cross-call comparison certificate, graph-level inference, or term-id arithmetic is available. Root and option selection may be omniscient. Let Q_A denote the minimum execution cost over those root and option choices for the fixed routine A. The algorithm is fixed before labeling; one does not minimize over all possible hardcoded comparison trees separately on each already labeled instance.

## 1. Matching universal upper

Define h(p,q)=s(1+ceil(log2(l/s))) for s=min(p,q)>0,l=max(p,q), and 0 for an empty run. Standard doubling galloping uses O(h) comparisons and reads. Put L_N=1+ceil(log2 N). We have

    h(p,q)<=L_N p,       h(p,q)<=3 sqrt(pq).

At root x put a=d_R^+(x), b=d_T^-(x),

    P=sum_{y in R(x)}h(d_S^+(y),b),
    Q=sum_{z in T^-1(x)}h(a,d_S^-(z)),
    w(x)=sum_{z in T^-1(x)}sqrt(d_S^-(z)).

Then P<=L_N sqrt(a beta), Q<=3sqrt(a)w(x), and therefore

    min(P,Q)<=3^(3/4)L_N^(1/4) beta^(1/8) sqrt(a) w(x)^(3/4).

Holder over x gives alpha^(1/4)(sum_x w)^(3/4); double counting and Cauchy--Schwarz give sum_xw<=sqrt(gamma |S|). Rotation, reflection, and geometric means give an implementable galloping plan of cost

    O(N + (log N)^(1/4)
        (|R||S||T|)^(1/8) min(Lambda,Lambda')^(1/2)).

Prices h are computed from degrees using bit lengths; all six option sums are priced in O(N) reads before selecting the root/options. Also h<=3sqrt(pq) gives a fixed-driver cost at most

    O(N + ||A_R|| sqrt(|S||T|)) <= O(N+sqrt(|R||S||T|)),

so the usual AGM cap has no logarithm.

## 2. Family with exact dense slope and sharp quarter logarithm

Fix i>=j>=1 and h>=1. Let

    M=2^h,       L=M^4,       u=2^L.

The letters are independent of the paper's M_R etc. Let

    n=|X|=u^(4i)/M^4,
    a=|Y0|=u^(4i-2j) M^2,
    p=|Z1|=u^(4i-j)/M,
    q=u^(4i) M^4,
    k=pL=u^(4i-j) M^3,
    d=u^(4i-3j) M,
    c=|Z2|=u^(4i+2j)/M^2.

All are positive integers. Also n/d=c/k=u^(3j)/M^5 is an integer. Partition X into n/d groups of size d and Z2 into matching groups of size k; include all T tuples from each Z2 group to its X group. Let R=X times Y0 and S contain Y0 times Z1. For each z in Z2 add its own private a-set Y2_z of S predecessors. Thus |Y2|=ca=u^(8i), all of S outdegree 1. Give each x its own private q predecessors in Z0, each of T outdegree 1; |Z0|=nq=u^(8i). There are no triangles.

### One global labeling forces both options

Order Y in layers, putting Y0[l] followed by Y2_z[l] for all z, for l=0,...,a-1. The projected order of Y0 and each Y2_z alternates. A disjoint sorted pair with an alternating merge has 2a-1 adjacent cross pairs, each of which must be compared: identifying an untested adjacent pair preserves all other comparisons and makes an intersection. Thus every positive T-option call costs at least 2a-1 comparisons. The whole T option at x costs at least k(2a-1)>=apL.

Put all Z2 after every Z1 and Z0. For each x, independently shuffle its q private Z0 keys with the common p-element Z1 set, preserving the within-run order. Every such family of shuffles is realized by one global labeling: in each of the p+1 gaps of Z1 concatenate the dead keys assigned to that gap, in a fixed order of x, then append Z2.

For a prescribed local call there are

    H=binom(p+q,p)>=(q/p)^p=(u^j M^5)^p>=u^p=2^(pL)

possible disjoint shuffles. Any correct disjoint-answer comparison leaf fixes the whole shuffle. Otherwise some cross pair has both orders consistent with the leaf, so it is incomparable in the comparison poset; equating it preserves all tested comparisons and both strict internal orders but changes the answer. Hence a disjoint leaf covers at most one shuffle. Comparisons on disjoint inputs have only the two strict outcomes (same-entry equality comparisons are predetermined). At most 2^D shuffles admit a transcript of fewer than D comparisons, where D=pL/2.

Under a uniform shuffle, the chance that any given prescribed R call costs less than D is at most 2^(-pL/2). Across three rotated copies there are 3na=3u^(8i-2j)/M^2 potential critical R calls. The union bound is strictly less than one:

    3na * 2^(-pL/2) <1.

For an explicit elementary bound, log2(3na)<2+8iL<16iL, whereas D/L=u^(4i-j)/(2M)>=u^(3i)/(2M)>=16i. The final inequality follows from u^3=2^(3M^4)>=32M and (u^3)^i>=i u^3. Thus there exists one simultaneous order in which every R option at each critical x costs at least aD=apL/2, while every T option costs at least apL.

Independent component orders are concatenated for the three rotated copies, so every global root has one critical X component. Therefore

    Q_A >= napL/2 = (M/2) u^(12i-3j).

This applies to any fixed correct fresh-call comparison routine, including arbitrary merge/leapfrog/galloping schedules. The quarter-log label is existential for each routine, unlike the explicit alternating original F labels that give linear certificates against all routines simultaneously.

### Exact statistics and asymptotics

One gadget has

    |R|=u^(8i-2j)/M^2,
    |S|=u^(8i)+u^(8i-3j)M,
    |T|=u^(8i)+u^(8i-j)/M.

Its forward squared degrees are

    alpha=A0=u^(12i-4j),
    beta=gamma=A0+u^(8i).

After the three rotations each relation has size

    D_size=2u^(8i)+u^(8i-j)/M+u^(8i-2j)/M^2+u^(8i-3j)M,

so N=3D_size. Each forward moment is

    A=3u^(12i-4j)+2u^(8i).

Each reverse moment is

    A'=u^(12i)M^4+2u^(12i-j)M^3+2u^(12i-2j)M^2
        +u^(12i-2j)/M^6+u^(12i-5j)M^3.

In particular A'>A, since A'>=u^(12i)M^4 and A<=5u^(12i-4j). Thus B2=A exactly. Moreover

    6u^(8i)<=N<=15u^(8i),
    3u^(12i-4j)<=B2<=5u^(12i-4j).

Consequently

    B2=Theta(N^kappa),      kappa=3/2-j/(2i),
    (|R||S||T|)^(1/8) B2^(3/4)=Theta(u^(12i-3j)),
    M=(log2 u)^(1/4)=Theta((log N)^(1/4)),
    Q_A=Omega((log N)^(1/4) N^(3/8) B2^(3/4)).

The universal upper is therefore attained up to a constant at every dense rational slope kappa in [1,3/2). At kappa=1 (i=j), worst-case sorted fresh-call cost is

    Theta(N^(9/8) (log N)^(1/4)).

The original F and G8 explicit alternating labelings still have no logarithmic overhead; this new normalization is needed to attain the extra logarithm. At kappa=3/2, the constant-factor AGM cap applies and the complete block triangle attains Theta(N^(3/2)).

## 3. Exact checks

`python3 -I slopes/log_normalized_checks.py` checks all divisibility, biregular handshakes, forward and reverse moments, exact lower costs, and union-bound bit certificates. It materializes no enormous graph. Full exact output is in `slopes/log_normalized_checks_output.txt`.

For (i,j,h)=(1,1,1), M=2,L=16,u=65536:

    N=2041701990030346958462306381305309298688
    B2=1701411834604692317316873037158841057280
    reverse=100435160273442607171961549360451092482683790173946953859072
    comparison lower=22300745198530623141535718272648361505980416
    per-call depth=1125899906842624
    program-count bit length=96

For (1,1,2), M=4,L=256, bit lengths of (N,B2,lower) are (2051,2051,2306), program-count bit length 1534, per-call-depth bit length 774. For (2,1,2), those values are (4099,5122,5378), 3582, 1798. For (1,1,3), M=8,L=4096, they are (32771,32771,36867), 24572, 12297. All checks passed.

A finite direct violation of the original constant-one upper bound was also checked at i=j=1,h=4, with M=16,L=65536,u=2^65536. `python3 -I slopes/log_normalized_finite.py` produced:

    N=3*(2^524289+2^458748+2^393208+2^327684)
    B2=5*2^524288
    lower=2^589827
    D=2^196619
    programs=3*2^393208
    bit_lengths N,B2,lower = 524291 524291 589828
    program_count_bit_length = 393210
    per_call_depth_bit_length = 196620
    lower_minus_N_eighth_exceeds_spectral_eighth = True

The last assertion was checked directly as `(lower-N)**8 > D_size**3 * B2**6`, using exact integers. This refutes the constant-one log-free inequality at a finite parameter with B2=Theta(N), for every fixed eligible routine with its corresponding existential adversarial global labeling. No enormous instance was materialized.
