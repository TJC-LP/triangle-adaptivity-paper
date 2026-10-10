# Weaver's outside checks

Weaver, TJC's internal work agent, reviewed the third draft of the paper and
wrote these five Python scripts from the paper's definitions alone, sharing
no code with `artifacts/`. `RUN_OUTPUT.txt` is the output Weaver recorded.
The paper's Section "Use of AI tools" and Appendix "Verification" describe
what they checked. Section and result numbers in the scripts and the output
are those of the third draft.

| File | What it checks |
|---|---|
| `lib.py` | A from-scratch rebuild of the cost model: degrees, moments, `Out`, the kernel work `M`, the per-root costs, the semijoin and full reductions, rotations, unions and padding |
| `families1.py` | The explicit families: `G8(m)` and its rotation union, padded `U(m)`, `F_{i,j}(u)`, `I_v`, `D(L,a,h)` and its union, against the paper's closed forms and tables |
| `families2.py` | `F_a`, `GMR`, the sharp family, `GMIN` and its padding, `H_a`, the Ferrers profiles, the stride-grid instance of the sampler proposition, and the spectral bound on 200,000 random regular statistics |
| `stress.py` | The upper bounds on 5,987 random instances (exact operator norms on a subset) and 3,000-step hill climbs per ratio (needs numpy) |
| `scheduler.py` | The price-then-run scheduler on 3,996 random instances, its tight family and the stray-tuple family |

## Provenance

The files are unchanged from the archive Weaver attached to its review
(`weaver-review-checks.zip`, 16,880 bytes, SHA-256
`0511088e91ce5efab86755679495c5289ead1b6f77b61f6fbbac84723ce1f4a1`), which
holds these six files in a directory `weaver-review-checks/`.

## Running them

Each script prepends Weaver's own working directory to `sys.path` and then
imports `lib` from it. `python3 -I` leaves the script's directory off
`sys.path`, so run them from this directory as

```sh
python3 -I -c "import runpy, sys; sys.path.insert(0, '.'); runpy.run_path('families1.py', run_name='__main__')"
```

and likewise for `families2.py`, `stress.py` and `scheduler.py`.

Re-run with Python 3.11 and numpy 2.3, `families1.py`, `families2.py` and
`stress.py` reproduce `RUN_OUTPUT.txt` exactly. `scheduler.py` reproduces it
except for one number: the worst `(pricing - 4n)/C` over the random
instances, recorded as 3.00, is 3.00, 3.20 or 4.00 depending on Python's
per-process string-hash seed. The instances are sets of tuples of strings,
so the order in which each binding's tuples are walked, and with it the
scheduler's lockstep advances, follows the hash seed (`PYTHONHASHSEED`,
which `-I` ignores; set it and run with `python3 -s` to fix it). Over seeds
0 to 49 the value was 3.00 for 25 seeds, 3.20 for one and 4.00 for 24.
Every run reports 0 failures, and every value is below the proven
constant 6. The paper reports the range.
