"""Faithful scalar port of sorted_runs.zig intersectEachBy/intersectWalk.

Source: src/util/sorted_runs.zig on the operator branch,
       , lines 361-493.
Only key predicates count as comparisons; index/length tests do not.
The independent `work` field follows the Zig work meter exactly.
`walked` follows its test hook (sum of the chosen walked side's full length).
Python's unbounded integers agree with saturating usize operations here:
all measured arrays have fewer than 2**32 elements and no index overflows.
"""

from dataclasses import dataclass, field
from collections import Counter


@dataclass
class Meter:
    work: int = 0
    walked: int = 0
    predicates: Counter = field(default_factory=Counter)

    def test(self, kind, answer):
        self.predicates[kind] += 1
        return answer

    @property
    def comparisons(self):
        return sum(self.predicates.values())

    def as_dict(self):
        return dict(work=self.work, walked=self.walked,
                    comparisons=self.comparisons,
                    predicates=dict(sorted(self.predicates.items())))


LINEAR_STEPS = 16


def lower_bound_by(col, lo, hi, key, work):
    # Zig lowerBoundBy, lines 412-422.
    while lo < hi:
        mid = lo + (hi - lo) // 2
        work.work += 1
        if work.test('lower_bound_lt', col[mid] < key):
            lo = mid + 1
        else:
            hi = mid
    return lo


def gallop_lower_bound_by(col, start, key, work):
    # Zig gallopLowerBoundBy, lines 361-382.
    n = len(col)
    if start >= n:
        return n
    i = start
    linear_end = min(n, start + LINEAR_STEPS)
    while i < linear_end:
        work.work += 1
        if work.test('gallop_ge', col[i] >= key):
            return i
        i += 1
    if i >= n:
        return n
    known = i - 1
    step = 1
    while n - known > step:
        probe = known + step
        work.work += 1
        if work.test('gallop_ge', col[probe] >= key):
            return lower_bound_by(col, known + 1, probe, key, work)
        known = probe
        step *= 2
    return lower_bound_by(col, known + 1, n, key, work)


def equal_run_end(col, start, value, work):
    # Zig equalRunEnd, lines 478-482. Comparisons are *not* Zig work.
    end = start
    while end < len(col) and work.test('equal_run_end_eq', col[end] == value):
        end += 1
    return end


def drops_at(col, i, value, work):
    # Zig dropsAt, lines 488-490, production skipOutOfOrder() == false.
    return i < len(col) and work.test('drops_at_lt', col[i] < value)


def intersect_walk(s, large, visit, work):
    # Zig intersectWalk, lines 451-475; callback False stops immediately.
    sn, ln = len(s), len(large)
    work.walked += sn
    lo = 0
    i = 0
    while i < sn:
        value = s[i]
        ie = equal_run_end(s, i + 1, value, work)
        work.work += ie - i
        if drops_at(s, ie, value, work):
            return 'out_of_order'
        lo = gallop_lower_bound_by(large, lo, value, work)
        if lo >= ln:
            return 'done'
        if drops_at(large, lo, value, work):
            return 'out_of_order'
        if work.test('match_eq', large[lo] == value):
            he = equal_run_end(large, lo + 1, value, work)
            work.work += he - lo
            if drops_at(large, he, value, work):
                return 'out_of_order'
            if not visit(value, (ie - i) * (he - lo)):
                return 'stopped'
            lo = he
        i = ie
    return 'done'


def intersect_each_by(a, b, visit, work):
    # Zig intersectEachBy, lines 443-446. Tie walks its first argument.
    if len(a) <= len(b):
        return intersect_walk(a, b, visit, work)
    return intersect_walk(b, a, visit, work)


def intersect(a, b):
    work = Meter()
    visits = []
    def visit(value, multiplicity):
        visits.append((value, multiplicity))
        return True
    result = intersect_each_by(a, b, visit, work)
    return result, visits, work


def self_test():
    from itertools import combinations_with_replacement, product
    runs = [seq for n in range(5)
            for seq in combinations_with_replacement(range(1, 6), n)]
    count = 0
    for a, b in product(runs, repeat=2):
        result, visits, work = intersect(a, b)
        ca, cb = Counter(a), Counter(b)
        expected = [(key, ca[key] * cb[key]) for key in sorted(ca.keys() & cb.keys())]
        assert result == 'done'
        assert visits == expected, (a, b, visits, expected)
        assert work.walked == min(len(a), len(b))
        count += 1
    # Exercise the >16 gap path, binary phase, exhaustion and stop callback.
    gallop_cases = 0
    for n in (0, 1, 15, 16, 17, 18, 31, 32, 100, 1000):
        col = list(range(1, 2 * n + 1, 2))
        for start in (0, n // 2, n, n + 1):
            for key in range(0, 2 * n + 2):
                work = Meter()
                expected = next((j for j in range(min(start, n), n) if col[j] >= key), n)
                assert gallop_lower_bound_by(col, start, key, work) == expected
                gallop_cases += 1
    work = Meter()
    seen = []
    def stop(value, multiplicity):
        seen.append((value, multiplicity))
        return False
    assert intersect_each_by([1, 2, 3], [1, 2, 3], stop, work) == 'stopped'
    assert seen == [(1, 1)]
    assert intersect([2, 1], [1, 2, 3])[0] == 'out_of_order'
    return dict(sorted_bag_pairs=count, lower_bound_cases=gallop_cases,
                stop_callback_cases=1, disorder_cases=1)


if __name__ == '__main__':
    print(self_test())
