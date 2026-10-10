import csv, statistics, sys, collections
t = collections.defaultdict(list); rows = collections.defaultdict(set)
for b, r, d, tag, case, ns, rc in csv.reader(open(sys.argv[1])):
    t[(d, case, b)].append(int(ns)); rows[(d, case)].add((b, int(rc)))
def f(ns):
    return f"{ns/1e6:.2f} ms" if ns >= 1e6 else f"{ns/1e3:.1f} us"
keys = sorted({(d, c) for d, c, _ in t})
print("| dataset | case | rows A | rows N | n | A median | N median | N/A | A min | N min |")
for d, c in keys:
    a, n = t[(d, c, 'A')], t[(d, c, 'N')]
    ra = {x for b, x in rows[(d, c)] if b == 'A'}; rn = {x for b, x in rows[(d, c)] if b == 'N'}
    print(f"| {d} | {c} | {ra} | {rn} | {len(a)}/{len(n)} | {f(statistics.median(a))} | {f(statistics.median(n))} | {statistics.median(n)/statistics.median(a):.2f} | {f(min(a))} | {f(min(n))} |")
