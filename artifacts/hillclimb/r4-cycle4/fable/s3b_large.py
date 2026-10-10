"""Larger instances: random dims up to 11, and Kronecker squares of random small instances (scale probe)."""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import kron, size
import s3_certify as s3
seed = int(sys.argv[1]); n = int(sys.argv[2]); maxdim = int(sys.argv[3]); mode = sys.argv[4]
rng = random.Random(seed)
def gen():
    for _ in range(n):
        if mode == 'kron':
            a = s3.random_instance(rng, 3)
            b = s3.random_instance(rng, 3)
            mats = tuple(kron(x, y) for x, y in zip(a, b))
            if max(len(M) * len(M[0]) for M in mats) > 144:
                continue
            yield mats
        else:
            yield s3.random_instance(rng, maxdim)
viol, und = s3.run_batch(gen(), f"{mode} seed {seed} n {n} maxdim {maxdim}")
sys.exit(1 if viol else 0)
