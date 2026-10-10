from collections import Counter, defaultdict
from fractions import Fraction
from random import Random


def evaluate(relations):
    outgoing = []
    incoming = []
    for relation in relations:
        out = defaultdict(set)
        inc = defaultdict(set)
        for a, b in relation:
            out[a].add(b)
            inc[b].add(a)
        outgoing.append(out)
        incoming.append(inc)
    sizes = tuple(map(len, relations))
    forward = tuple(sum(len(v)**2 for v in d.values()) for d in outgoing)
    reverse = tuple(sum(len(v)**2 for v in d.values()) for d in incoming)
    works = []
    weighted = []
    for i, relation in enumerate(relations):
        work = 0
        endpoint_costs = (Counter(), Counter())
        for a, b in relation:
            w = min(len(outgoing[(i + 1) % 3].get(b, ())),
                    len(incoming[(i + 2) % 3].get(a, ())))
            work += w
            endpoint_costs[0][a] += 1 + w
            endpoint_costs[1][b] += 1 + w
        works.append(work)
        weighted.append(endpoint_costs)
    roots = []
    for i in range(3):
        left = weighted[i][0]
        right = weighted[(i - 1) % 3][1]
        roots.append(sum(min(left[x], right[x]) for x in left.keys() | right.keys()))
    output = sum(len(outgoing[1].get(y, set()) & incoming[2].get(x, set()))
                 for x, y in relations[0])
    p = forward[0] * forward[1] * forward[2]
    pp = reverse[0] * reverse[1] * reverse[2]
    for i in range(3):
        assert works[i]**5 <= sizes[(i + 2) % 3]**3 * forward[i]**2 * forward[(i + 1) % 3]
        assert works[i]**5 <= sizes[(i + 1) % 3]**3 * reverse[i]**2 * reverse[(i + 2) % 3]
    assert min(works)**5 <= sizes[0] * sizes[1] * sizes[2] * min(p, pp)
    return sizes, forward, reverse, tuple(works), tuple(roots), output


def family(m):
    a, b, c = m**3, m, m**2
    result = [set(), set(), set()]
    for copy in range(3):
        xs = [(copy, 'x', i) for i in range(a)]
        ys = [(copy, 'y', i) for i in range(b)]
        zs = [(copy, 'z1', i) for i in range(c)]
        base = [set(), set(), set()]
        base[0] = {(x, y) for x in xs for y in ys}
        base[1] = {(y, z) for y in ys for z in zs}
        base[2] = {((copy, 'z0', i, j), x) for i, x in enumerate(xs) for j in range(c)}
        for i in range(3):
            result[(i - copy) % 3].update(base[i])
    return result


print('family columns: m, r=s=t, N, forward_each=B2, reverse_each, M_each, C_each, Out, M/(N+B2), M^5/(rst*B2^3)')
for m in range(1, 9):
    sizes, f, rev, works, roots, output = evaluate(family(m))
    r = m**5 + m**4 + m**3
    n = 3*r
    b2 = 3*m**5
    assert sizes == (r,)*3
    assert f == (b2,)*3
    assert rev == (2*m**7 + m**4,)*3
    assert min(f[0]**3, rev[0]**3) == b2**3
    assert works == (m**6,)*3
    assert roots == (m**5+m**3,)*3
    assert output == 0
    print(m, r, n, b2, rev[0], works[0], roots[0], output,
          Fraction(works[0], n+b2), Fraction(works[0]**5, r**3*b2**3), sep=' | ')

rng = Random(271828)
checked = 0
max_q = Fraction(0)
max_witness = None
for _ in range(10000):
    dimensions = [rng.randrange(1, 11) for _ in range(3)]
    rels = []
    for i in range(3):
        threshold = rng.randrange(0, 17)
        rels.append({(a,b) for a in range(dimensions[i]) for b in range(dimensions[(i+1)%3])
                     if rng.randrange(16) < threshold})
    sizes, f, rev, works, roots, output = evaluate(rels)
    denominator = sizes[0]*sizes[1]*sizes[2] * min(f[0]*f[1]*f[2], rev[0]*rev[1]*rev[2])
    if denominator:
        q = Fraction(min(works)**5, denominator)
        if q > max_q:
            max_q = q
            max_witness = (dimensions, sizes, f, rev, works)
    checked += 1
print('random_checked =', checked)
print('random_max_exact_ratio =', max_q)
print('random_max_witness =', max_witness)
