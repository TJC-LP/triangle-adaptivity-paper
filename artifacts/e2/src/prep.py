"""Convert raw datasets into per-predicate integer edge lists (deduplicated).

Output: <out>.npz with arrays  n (term count), preds (names), and for each
predicate index i: s_i, o_i (int32).  Edges are deduplicated sets.
"""
import gzip
import sys

import numpy as np


def finish(out, n, edges, names=None):
    arrs = {"n": np.array([n], dtype=np.int64)}
    pnames = []
    for i, (p, (s, o)) in enumerate(edges.items()):
        s = np.asarray(s, dtype=np.int64)
        o = np.asarray(o, dtype=np.int64)
        key = np.unique(s * n + o)
        arrs[f"s_{i}"] = (key // n).astype(np.int32)
        arrs[f"o_{i}"] = (key % n).astype(np.int32)
        pnames.append(p if names is None else names[p])
    arrs["preds"] = np.array(pnames)
    np.savez(out, **arrs)
    print(out, "terms", n, "preds", len(pnames),
          "edges", sum(len(arrs[f"s_{i}"]) for i in range(len(pnames))))


def read_nt(path, out):
    ids = {}
    edges = {}
    get = ids.setdefault
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
        for line in f:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            if line.endswith(" ."):
                line = line[:-2]
            parts = line.split(" ", 2)
            if len(parts) != 3:
                continue
            s, p, o = parts
            si = get(s, len(ids))
            oi = get(o.strip(), len(ids))
            e = edges.get(p)
            if e is None:
                e = edges[p] = ([], [])
            e[0].append(si)
            e[1].append(oi)
    finish(out, len(ids), edges)


def read_tsv(paths, out):
    ids = {}
    edges = {}
    get = ids.setdefault
    for path in paths:
        with open(path) as f:
            for line in f:
                parts = line.split()
                if len(parts) != 3:
                    continue
                s, p, o = parts
                si = get(s, len(ids))
                oi = get(o, len(ids))
                e = edges.get(p)
                if e is None:
                    e = edges[p] = ([], [])
                e[0].append(si)
                e[1].append(oi)
    finish(out, len(ids), edges)


def read_snap(path, out, name):
    a = []
    with gzip.open(path, "rt") as f:
        for line in f:
            if line[0] == "#" or not line.strip():
                continue
            u, v = line.split()[:2]
            a.append((int(u), int(v)))
    a = np.array(a, dtype=np.int64)
    uniq, inv = np.unique(a.ravel(), return_inverse=True)
    inv = inv.reshape(a.shape)
    finish(out, len(uniq), {name: (inv[:, 0], inv[:, 1])})


if __name__ == "__main__":
    kind = sys.argv[1]
    if kind == "nt":
        read_nt(sys.argv[2], sys.argv[3])
    elif kind == "tsv":
        read_tsv(sys.argv[3:], sys.argv[2])
    elif kind == "snap":
        read_snap(sys.argv[2], sys.argv[3], sys.argv[4])
