# Experiment E2: the spectral bound U on real graphs

This directory reproduces Appendix A (Section 8 in revision 3) of `spectral_agm.typ`. Each row of
`results.csv` is one triangle query `?x R ?y . ?y S ?z . ?z T ?x` with
`Out > 0`. R, S and T are predicates, each possibly transposed, and every
query is canonical up to rotation and whole-cycle reversal. `summary.md` holds
every table and count that the paper quotes.

| File | Contents |
|---|---|
| `src/prep.py` | Raw data to per-predicate deduplicated integer edge lists (`.npz`) |
| `src/bounds.py` | σ estimate (power iteration, cross-checked with `svds`); exact certificates: integer Schur bound, Collatz–Wielandt and Rayleigh bounds as exact rationals, the degree lower test as an assertion; U and its binding term; U_schur, U_cw, U_cert, U_hi (rounded up) and U_lo (rounded down) from exact squared terms; AGM, degree bound, cyclic ℓ2, exact Out (numba), kernel work M, M1–M3 |
| `src/run.py` | Enumerates canonical queries for one dataset and writes `out/<name>.csv` and `out/<name>.spectral.json` |
| `src/recertify.py` | Re-derives the certificate columns of existing `out/` files with exact arithmetic (see *Exact certification* below) |
| `src/summarize.py` | Merges `out/*.csv` into `results.csv` and writes `summary.md` |
| `results.csv` | 3,124 rows; sha256 `63e895a931d8c282b88463c319edc42d6d4c13c11da830e8f1efe3d3b2b2b50e` |
| `summary.md` | sha256 `f2ef3f363613280737a4273f0559e5f9205342ce60ac8c228ad1bd63932a345b` |
| `spectral/*.spectral.json` | Per-predicate r, σ estimate, svds, exact squared bounds (`schur_sq`, `cw_few_sq`, `cert_sq`, `hi_sq`, `lo_sq`, as integers or `p/q` strings), their outward-rounded roots, the first run's float values (`old_*`), iteration count and time |
| `logs/*.log` | The original run logs (`logs/prep-*.log` are the prep logs; `logs/recertify.log` is the exact recertification) |
| `check/csvcheck.py` | Internal-consistency audit of `results.csv` (bounds ≥ Out, U recomputed, counts) |
| `check/rebuild_summary.py` | Runs `src/summarize.py` on the committed `results.csv` and `spectral/` (laid out as `out/` in a temporary directory) and checks that it reproduces `results.csv` and `summary.md` byte for byte |
| `check/recompute.py`, `check/recompute.log` | Independent recomputation of 22 sampled rows from the prepared `.npz` files (run before the recertification: its `sig_cert`/`U_cert` comparison is against the first run's float certificates) |

The raw datasets are not committed. The commands below download them.

## Environment

- macOS 26.7 (build 25G229) on an Apple M4 Max (`hw.model` Mac16,5), 16 cores, 128 GiB
- Python 3.11.9 (python.org framework build), in a fresh venv
- `numpy==2.4.6`, `scipy==1.17.1`, `numba==0.68.0`, `llvmlite==0.50.0` (the complete `pip freeze`)

```sh
python3.11 -m venv venv
venv/bin/pip install numpy==2.4.6 scipy==1.17.1 numba==0.68.0 llvmlite==0.50.0
```

## Datasets

The SHA-256 digests are of the downloaded files. They were re-hashed when
these artifacts were assembled, and each one matches `summary.md`.

| Name | URL | sha256 |
|---|---|---|
| ca-GrQc | https://snap.stanford.edu/data/ca-GrQc.txt.gz | `a254442cdf5d684712578b630c2e0d7543518ab154ef2341cabb607572ce7230` |
| email-Eu-core | https://snap.stanford.edu/data/email-Eu-core.txt.gz | `4b47acdb80197b085fe63c819c357ae488131ee904ed93d1b219a68b0f9e245f` |
| wiki-Vote | https://snap.stanford.edu/data/wiki-Vote.txt.gz | `7d3e53626e14b8b09fb3b396bece9d481ad606bd64ceab066349ff57d4ada7fc` |
| soc-Epinions1 | https://snap.stanford.edu/data/soc-Epinions1.txt.gz | `69a2dab71fa5e3a0715487599fc16ca17ddc847379325a6c765bbad6e3e36938` |
| com-youtube | https://snap.stanford.edu/data/bigdata/communities/com-youtube.ungraph.txt.gz | `dff1b97ba7d2fa9c59884b67dcd2275e717ff9501f86ed82ce6582ed4971f3e0` |
| com-dblp | https://snap.stanford.edu/data/bigdata/communities/com-dblp.ungraph.txt.gz | `9eb0bd30312ddd04e2624f7c36c0983a2e99b116f0385be5a7fce6d6170f4cb3` |
| Wikidata5M (transductive) | https://www.dropbox.com/s/6sbhm0rwo4l73jq/wikidata5m_transductive.tar.gz?dl=1 | `c233bb9d7dfc4eb2f038e0e5cee4b647b39dc4652f05ff118081077a454b3171` |
| CoDEx-L train | https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/train.txt | `4f2a696eb192a5fb076551b363a09a753565da7e4b7962202907309d39bf5f17` |
| CoDEx-L valid | https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/valid.txt | `f0119a22dc663e8df4a942cde7404927935b0c42e5a8980f5fb48ac6886e416f` |
| CoDEx-L test | https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/test.txt | `2d8188d6f199fc548c8e5fb97336a7ffd079240fc84c0425ed9c29d39bfdab8d` |
| sci50 (local) | built from the QLever scientists collection; see below | `6ceeccb53c18dbfe8416c74c355400fc9778df6c55e0e30eaf59890d866d5542` (the 2,304,759,095-byte `sci50.nt` that was used) |

**sci50.** sci50 is 50 relabelled copies of the 369,661-triple
scientists knowledge graph: 18,483,050 triples, 157 predicates and
2,481,777 subject/object terms. `replicate.py` suffixes, in copies
1..49, every subject and object IRI under `http://example.org/sci/`
(and every blank node; there are none). It leaves predicates, literals
and IRIs outside that namespace alone, so the copies share 43,127
terms: 42,993 literals and 134 IRIs such as `<Futurama:_Bender's_Big_Score>`,
which `scientists_to_nt.py` keeps as absolute IRIs because their text
before the first `:` parses as a scheme. Every shared term appears in
all 50 copies and only as an object. Each copy has 48,773 private terms
(50 x 48,773 + 43,127 = 2,481,777).

The file used was built on 2026-09-26 with the repository's
`bench/sparqloscope` tools (see `bench/sparqloscope/README.md`):

```sh
curl -LO https://raw.githubusercontent.com/ad-freiburg/qlever/master/e2e/scientist-collection.zip
unzip scientist-collection.zip
python3 bench/sparqloscope/scientists_to_nt.py scientist-collection/scientists.nt scientists.nt
python3 bench/sparqloscope/replicate.py scientists.nt sci50.nt 50
```

Consequences, checked by re-running `run.py` on one copy (below):
sizes and Out are exactly 50 times the copy's on all 456 rows (no shared
term is a subject, so a triangle never spans two copies). sigma is the
copy's for the 58 selected predicates with no shared object, sqrt(50)
times it for the 11 whose objects are all literals (Date_of_death,
Date_of_birth, Open_Library_ID, Award_Nominations, Name_ID, Height, uri,
THOMAS_ID, QuotationsBook_ID, Weight, label), and in between for 12
mixed ones (sigma^2 ratio 1.62 to 12.6). U is 50 times the copy's on 426
rows, so AGM/U carries a factor sqrt(50); on the other 30 the factor is
between 1/sqrt(50) and 6.05. One copy: median AGM/U 8.96 (min 1.22);
sci50: 63.4 (8.64). The degree bound is not exactly 50 times on 16 rows
and M on 1 row, because shared objects multiply column degrees by 50.

To reproduce the one-copy comparison (copy 0 is the first 369,661
lines of `sci50.nt`, unchanged from the input):

```sh
head -n 369661 /path/to/sci50.nt > data/sci1.nt
venv/bin/python -I src/prep.py nt data/sci1.nt prep/sci1.npz      # terms 91900 preds 157 edges 369661
venv/bin/python -I src/run.py prep/sci1.npz sci1 out/sci1.csv --min-edges 20
```

`--min-edges 20` selects the same 81 predicates as `--min-edges 1000` on
sci50, and the run keeps the same 456 queries.

Rebuilding: the sci50 used here contains no blank nodes, so the later blank-node
change in the engine does not affect it. The current `replicate.py`, run
on the one-copy input used (sha256
`ee2f8c36aa901815589c562abed7244357035e077c19434745e1032e44765467`, equal to
the first 369,661 lines of sci50.nt), rebuilds `sci50.nt` byte for byte
(sha256 `6ceeccb5...d5542` above). The current `scientists_to_nt.py`
names the label predicate `rdfs:label` instead of
`<http://example.org/sci/label>`; that predicate occurs only as a
predicate, so the rename changes no row of `results.csv` except the
`label` name. The upstream zip is not pinned to a commit.

## Commands

Run from a working directory `$E` that holds `src/` (this directory), `venv/`,
`data/`, `prep/` and `out/`. All Python runs with `-I`.

```sh
mkdir -p data/snap data/kg/w5m prep out
cd data/snap
for f in ca-GrQc.txt.gz email-Eu-core.txt.gz wiki-Vote.txt.gz soc-Epinions1.txt.gz; do
  curl -LO https://snap.stanford.edu/data/$f; done
for f in com-youtube.ungraph.txt.gz com-dblp.ungraph.txt.gz; do
  curl -LO https://snap.stanford.edu/data/bigdata/communities/$f; done
cd ../kg
curl -L -o wikidata5m_transductive.tar.gz 'https://www.dropbox.com/s/6sbhm0rwo4l73jq/wikidata5m_transductive.tar.gz?dl=1'
tar xzf wikidata5m_transductive.tar.gz -C w5m
for s in train valid test; do
  curl -L -o codex-l-$s.txt https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/$s.txt; done
cd ../..
shasum -a 256 data/snap/* data/kg/*.txt data/kg/*.tar.gz   # compare with the table above

# prep: one .npz per dataset
for d in ca-GrQc email-Eu-core wiki-Vote soc-Epinions1; do
  venv/bin/python -I src/prep.py snap data/snap/$d.txt.gz prep/$d.npz $d; done
for d in com-youtube com-dblp; do
  venv/bin/python -I src/prep.py snap data/snap/$d.ungraph.txt.gz prep/$d.npz $d; done
venv/bin/python -I src/prep.py tsv prep/w5m.npz data/kg/w5m/wikidata5m_transductive_{train,valid,test}.txt
venv/bin/python -I src/prep.py tsv prep/codex-l.npz data/kg/codex-l-{train,valid,test}.txt
venv/bin/python -I src/prep.py nt /path/to/sci50.nt prep/sci50.npz

# run: the label (2nd argument) is the dataset name in results.csv
for d in ca-GrQc email-Eu-core wiki-Vote soc-Epinions1 com-dblp com-youtube; do
  venv/bin/python -I src/run.py prep/$d.npz $d out/$d.csv --sym > out/$d.log; done
venv/bin/python -I src/run.py prep/codex-l.npz codex-l out/codex-l.csv --min-edges 1000 > out/codex-l.log
venv/bin/python -I src/run.py prep/sci50.npz sci50 out/sci50.csv --min-edges 1000 > out/sci50.log
venv/bin/python -I src/run.py prep/w5m.npz wikidata5m out/w5m.csv \
  --preds P31,P279,P361,P527,P131,P150,P17,P47,P30,P36,P1376,P706,P276,P206,P495,P27,P19,P20,P159,P740,P106,P69,P108,P463 \
  > out/w5m.log

# exact recertification of the first run's outputs (writes out-cert/; see below)
venv/bin/python -I src/recertify.py out prep out-cert > logs/recertify.log
# then summarize from out-cert/ (move it to out/ first, keeping the original as out.orig/)

# merge and summarize (writes $E/results.csv and $E/summary.md)
venv/bin/python -I src/summarize.py "$E"

# audits
venv/bin/python -I check/csvcheck.py results.csv
venv/bin/python -I check/rebuild_summary.py     # from the committed files alone
venv/bin/python -I check/recompute.py "$E"     # needs prep/*.npz
```

Run times on the machine above: wikidata5m about 31 minutes, sci50 about 5
minutes plus spectral time, CoDEx-L about 100 s, and each SNAP graph a few
seconds.

### Provenance of the commands

- The prep commands for sci50 and wikidata5m are those recorded in
  `logs/prep-*.log` (written there with `$E` for the working directory).
  The first line of `logs/{prep-sci50,prep-w5m,sci50,w5m}.log` named the
  `.npz` by an absolute scratch path; revision 3 replaced that prefix by
  the relative `prep/` and changed nothing else.
  The SNAP and CoDEx-L prep commands follow `prep.py`'s argument order.
- The `run.py` arguments were reconstructed from the run logs and the
  experiment's report. They are: `--sym` for SNAP; `--min-edges 1000` for
  CoDEx-L (36 of 69 predicates) and sci50 (81 of 157); and the 24-predicate
  `--preds` list for Wikidata5M. When these artifacts were assembled, the
  reconstructed commands were re-run on all six SNAP graphs and on CoDEx-L
  (887 of the 3,124 rows). Their CSVs equal the originals in every column
  except `count_secs`, the wall time of the count. The selection logic was
  also re-applied to `prep/w5m.npz`, and it picks the same 24 predicates in
  the same order as `logs/w5m.log`. sci50 and Wikidata5M were not re-run
  end to end.
- `summarize.py`, re-run on the recertified `out/*.csv` and
  `out/*.spectral.json`, regenerates `results.csv` and `summary.md` byte for
  byte.
- `check/csvcheck.py results.csv` exits 0 and prints
  `violations/inconsistencies: none`, `matmul_check` `ok` 2842 and blank 282,
  and tightest-bound counts `deg 1902`, `l2 1018`, `U 204`. Its informational
  line counts 405 rows whose U *estimate* lies outside the exact
  `[U_lo, U_hi]`, by at most 1.4e-13 relative (rounding in the estimate).

## Exact certification

The first run computed the Schur bound as `sqrt(float(maxrow) * float(maxcol))`
and the Collatz–Wielandt (CW) bound in floating point. Those are approximations
to certificates, not certificates: in six sci50 views (`Date_of_birth`,
`Date_of_death`, `Place_of_death`, `Height`, `People_who_have_had_this_role`,
`Named_after`) the stored certified σ was one ulp *below* √(max degree), which
is a lower bound on σ. Example: `Named_after` has a row of degree 6 and columns
of degree 1, so σ = √6 exactly, but the stored 2.449489742783178 squares to
less than 6.

`bounds.spectral` now certifies exactly:

- Schur: `schur_sq = maxrow * maxcol`, an integer.
- CW: for B = MᵀM and any w > 0, σ² ≤ max_i (Bw)_i / w_i. The float iterate is
  rounded *up* to a positive integer vector with entries at most a power-of-two
  scale chosen so that every entry of Mw and Bw stays below 2⁶² (asserted),
  Bw is computed in int64, and the maximum ratio is an exact `Fraction`
  (candidates found in floating point within 1e-12 of the float maximum; float
  error is below 4·2⁻⁵³, so the exact maximiser is among them).
  `cw_few_sq` is the minimum over the first five iterates from 𝟙;
  `cert_sq = min(schur_sq, cw_few_sq)`; `hi_sq` also uses the best and final
  iterates.
- Lower: `lo_sq = max(maxrow, maxcol, Rayleigh)` with the Rayleigh quotient
  |Mw|²/|w|² in Python integers. The assertions `cert_sq ≥ max(maxrow, maxcol)`,
  `hi_sq ≥ max(maxrow, maxcol)` and `lo_sq ≤ hi_sq` hold for all 153 views.
- Floats: `sig_cert`, `schur`, `cw_few`, `sigma_hi` are square roots rounded up
  and checked exactly (`Fraction(f)**2 ≥ q`); `sigma_lo` is rounded down. Every
  U column is the square root of the exact minimum of the squared U terms,
  rounded up (`U_schur`, `U_cw`, `U_cert`, `U_hi`) or down (`U_lo`).

`src/recertify.py` applied this to the first run without recounting: it
rebuilt all 153 views from `prep/*.npz`, reran `bounds.spectral` (iteration
counts and degrees reproduce exactly; the `svds` cross-check moves σ by at most
1.7e-13 relative, so the stored σ, and hence the `U` column, is kept), and
replaced only `sig_cert1-3`, `U_schur`, `U_cw`, `U_cert`, `U_hi`, adding
`U_lo`. All other columns are byte-identical to the first run.

What changed: the six invalid views move up by one ulp, which raises `U_cert`
by 2.2e-16 relative on 9 rows. Integer rounding of the iterate lifts entries
that had decayed toward underflow, so the exact CW₅ bound is *tighter* in some
views (com-youtube sym 270.33 → 239.51, com-youtube dir 210.85 → 203.54,
soc-Epinions1 dir 149.14 → 142.20). The maximum `U_cert/U` drops from 1.28 to
1.14 (SNAP p90 1.11 → 1.06). No count changes: `U_cert < ℓ2` 587,
`U_cert < min(AGM, ℓ2, deg)` 203, p90 `U_cert/U` 1.0154, and the pre-registered
criterion (22 of 134 predicates, 2,537 and 2,921 of 3,124 queries).

Wikidata5M `P106` hit the 3,000-step cap. Its float CW test stopped at step 55,
when an iterate entry underflowed below 1e-280, which froze the float bracket at
[410.0305388720186, 410.03240480202385] (relative width 4.6e-6, outside the
1e-6 target). The exact bracket uses the final iterate rounded up to integers
and is [410.03053887196165, 410.03053887212945] (width 4.1e-13). Every view's
exact bracket is now within 1e-6 (largest 9.97e-7).

## Scope

The rates in `summary.md` are conditional on the selected predicates, on
canonical queries whose supports intersect, and on nonzero output. They are
not workload-weighted. Self-loops are kept, so counts are homomorphism counts
(SPARQL semantics). com-dblp and com-youtube are stored one direction per
undirected edge, so their directed cyclic pattern has `Out = 0` and is
dropped. ca-GrQc is already symmetric.
