**The fully reduced \(1/10\) lower bound is proved.** The overall gap remains in \([1/10,1/8]\).

The independent rebuild reproduced:

| \(v\) | \(N\) | \(C\) | Out | \(B_2\) |
|---:|---:|---:|---:|---:|
| 2 | 8,976 | 12,464 | 5,760 | 29,264 |
| 3 | 355,266 | 888,246 | 262,440 | 2,441,502 |
| 4 | 5,263,104 | 22,332,672 | 4,177,920 | 56,889,600 |

Two material claims were refuted:

- **LP normalization:** exactly three unpadded live gadgets do not attain gap \(1/11\) at slope \(1\). Adding isolated triangles repairs attainment.
- **Engine pruning:** a literal 31,000-tuple instance makes floor-pruned rescue accept while the fully sampled rule declines. This refutes decision preservation, not answer correctness.

The four-cycle theorem survives with the documented repairs; its sharp constant remains open in \([8,16]\).

The [complete audit](./REPORT.md) contains claim-by-claim verdicts, proof checks, exact outputs, counterexamples, and paper-ready corrected statements. Fresh verifier code and `reproduce.sh` are alongside it. No original solver scripts were executed or imported, and no repository source was changed.