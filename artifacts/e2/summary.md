# E2: spectral triangle bound U on real data

Every row is one triangle query `?x R ?y . ?y S ?z . ?z T ?x` (R/S/T possibly transposed) with Out > 0. Queries are canonical up to rotation and whole-cycle reversal. U uses the estimate σ from power iteration (Rayleigh lower, Collatz–Wielandt upper, stopped at 1e-6 relative width or 3000 steps) cross-checked against `svds`; U is an estimate of the bound, not a certificate. Certified quantities are exact: σ² ≤ maxrow·maxcol (Schur, an integer) and σ² ≤ max_i (Bw)_i/w_i (Collatz–Wielandt, B = AᵀA, w the float iterate rounded up to a positive integer vector, the ratio an exact rational). U_cert replaces σ² by min(Schur, CW after 5 power steps from 𝟙); U_hi and U_lo use the exact bracket σ² ∈ [max(maxdeg, Rayleigh), min(U_cert's bound, CW at the final and best iterates)]. Every U is evaluated from the exact squared terms and its square root is rounded outward (up for U_schur, U_cw, U_cert, U_hi; down for U_lo). ℓ2 = min(ΣaΣbΣc², Σa'²Σb'²Σc'²)^{1/3}. Out is counted exactly, and cross-checked with `(A_R@A_S).multiply(A_T.T).sum()` wherever the SpGEMM was ≤3e8 flops.

Sanity: rows where some bound < Out: **0**
; SpGEMM cross-checks: 2842/2842 ok.

Distribution columns are min / median / p90 / max.

### All queries (n = 3124)

| quantity | min / median / p90 / max |
|---|---|
| AGM / U | 1.47 / 9.57 / 63.9 / 361 |
| ℓ2 / U | 0.00173 / 0.502 / 1.41 / 10.5 |
| degree bound / U | 0.000253 / 0.282 / 1.48 / 137 |
| min(AGM, ℓ2, deg) / U | 0.000253 / 0.209 / 0.827 / 4 |
| U / Out | 2.35 / 5.39e+04 / 5.33e+06 / 1.23e+09 |
| ℓ2 / Out | 1.69 / 2.34e+04 / 1.45e+06 / 1.5e+08 |
| M / U | 1.77e-09 / 0.000153 / 0.00742 / 0.586 |
| U_cert / U (σ² → exact min(Schur, CW₅)) | 1 / 1 / 1.02 / 1.14 |
| U_Schur / U | 1 / 2.64 / 6.05 / 11.6 |
| U_CW₅ / U | 1 / 1 / 1.02 / 1.14 |

- U < ℓ2: **589/3124** (18.9%); U < AGM: 3124/3124; U < degree bound: 612/3124; U < min(AGM, ℓ2, deg): **204/3124** (6.5%)
- with certified σ (exact min(Schur, CW₅)): U_cert < ℓ2: 587/3124; U_cert < min(AGM, ℓ2, deg): 203/3124
- M ≤ U: 3124/3124; Out = 0 rows: 0
- binding U term: `sqrt(sR rS rT)` 1215, `sqrt(sT rR rS)` 1017, `sqrt(sS rR rT)` 733, `rS sT` 89, `rT sS` 59, `rT sR` 5, `rR sS` 3, `rS sR` 2, `rR sT` 1

### Group sci50 (n = 456)

| quantity | min / median / p90 / max |
|---|---|
| AGM / U | 8.64 / 63.4 / 140 / 361 |
| ℓ2 / U | 0.199 / 0.767 / 2.19 / 10.5 |
| degree bound / U | 0.000253 / 0.307 / 1.43 / 3.05 |
| min(AGM, ℓ2, deg) / U | 0.000253 / 0.291 / 0.881 / 3.05 |
| U / Out | 15 / 1.41e+03 / 2.36e+04 / 2.52e+05 |
| ℓ2 / Out | 15.3 / 1.39e+03 / 1.79e+04 / 2.09e+05 |
| M / U | 3.96e-06 / 0.00192 / 0.0173 / 0.262 |
| U_cert / U (σ² → exact min(Schur, CW₅)) | 1 / 1 / 1.02 / 1.06 |
| U_Schur / U | 1 / 1.73 / 2.91 / 4.69 |
| U_CW₅ / U | 1 / 1 / 1.02 / 1.06 |

- U < ℓ2: **163/456** (35.7%); U < AGM: 456/456; U < degree bound: 113/456; U < min(AGM, ℓ2, deg): **33/456** (7.2%)
- with certified σ (exact min(Schur, CW₅)): U_cert < ℓ2: 163/456; U_cert < min(AGM, ℓ2, deg): 33/456
- M ≤ U: 456/456; Out = 0 rows: 0
- binding U term: `sqrt(sT rR rS)` 219, `sqrt(sR rS rT)` 156, `sqrt(sS rR rT)` 38, `rS sT` 28, `rT sS` 10, `rT sR` 3, `rR sS` 2

### Group SNAP (n = 16)

| quantity | min / median / p90 / max |
|---|---|
| AGM / U | 2.35 / 3.73 / 12.1 / 13.8 |
| ℓ2 / U | 0.146 / 0.838 / 1.03 / 2.35 |
| degree bound / U | 1.52 / 4.43 / 19.8 / 137 |
| min(AGM, ℓ2, deg) / U | 0.146 / 0.838 / 1.03 / 2.35 |
| U / Out | 3.54 / 14.8 / 74.8 / 180 |
| ℓ2 / Out | 1.69 / 6.56 / 85.8 / 161 |
| M / U | 0.0507 / 0.274 / 0.556 / 0.586 |
| U_cert / U (σ² → exact min(Schur, CW₅)) | 1 / 1 / 1.06 / 1.14 |
| U_Schur / U | 1.78 / 3.04 / 7.25 / 11.6 |
| U_CW₅ / U | 1 / 1 / 1.06 / 1.14 |

- U < ℓ2: **2/16** (12.5%); U < AGM: 16/16; U < degree bound: 16/16; U < min(AGM, ℓ2, deg): **2/16** (12.5%)
- with certified σ (exact min(Schur, CW₅)): U_cert < ℓ2: 2/16; U_cert < min(AGM, ℓ2, deg): 2/16
- M ≤ U: 16/16; Out = 0 rows: 0
- binding U term: `sqrt(sR rS rT)` 16

### Group KG (n = 2652)

| quantity | min / median / p90 / max |
|---|---|
| AGM / U | 1.47 / 8.98 / 63.9 / 89.3 |
| ℓ2 / U | 0.00173 / 0.451 / 1.27 / 10.3 |
| degree bound / U | 0.00281 / 0.275 / 1.48 / 32.9 |
| min(AGM, ℓ2, deg) / U | 0.00173 / 0.199 / 0.801 / 4 |
| U / Out | 2.35 / 1.04e+05 / 6.82e+06 / 1.23e+09 |
| ℓ2 / Out | 2.08 / 4.27e+04 / 1.85e+06 / 1.5e+08 |
| M / U | 1.77e-09 / 9.34e-05 / 0.00417 / 0.57 |
| U_cert / U (σ² → exact min(Schur, CW₅)) | 1 / 1 / 1.02 / 1.05 |
| U_Schur / U | 1.41 / 3 / 8.84 / 9.49 |
| U_CW₅ / U | 1 / 1 / 1.02 / 1.05 |

- U < ℓ2: **424/2652** (16.0%); U < AGM: 2652/2652; U < degree bound: 483/2652; U < min(AGM, ℓ2, deg): **169/2652** (6.4%)
- with certified σ (exact min(Schur, CW₅)): U_cert < ℓ2: 422/2652; U_cert < min(AGM, ℓ2, deg): 168/2652
- M ≤ U: 2652/2652; Out = 0 rows: 0
- binding U term: `sqrt(sR rS rT)` 1043, `sqrt(sT rR rS)` 798, `sqrt(sS rR rT)` 695, `rS sT` 61, `rT sS` 49, `rT sR` 2, `rS sR` 2, `rR sS` 1, `rR sT` 1

## Per dataset

| dataset | variant | n | med AGM/U | med ℓ2/U | U<ℓ2 | U<min(prior) | med U/Out | med U_cert/U |
|---|---|---|---|---|---|---|---|---|
| ca-GrQc | dir | 2 | 3.73 | 0.37 | 0 | 0 | 4.56 | 1 |
| ca-GrQc | sym | 1 | 3.73 | 0.37 | 0 | 0 | 4.56 | 1 |
| codex-l | dir | 871 | 6.34 | 0.641 | 224 | 79 | 1.13e+04 | 1 |
| com-dblp | dir | 1 | 13.8 | 0.146 | 0 | 0 | 35 | 1 |
| com-dblp | sym | 1 | 12.5 | 0.188 | 0 | 0 | 18.2 | 1 |
| com-youtube | dir | 1 | 9.39 | 0.588 | 0 | 0 | 180 | 1.11 |
| com-youtube | sym | 1 | 11.6 | 2.35 | 1 | 1 | 68.6 | 1.14 |
| email-Eu-core | dir | 2 | 2.46 | 0.896 | 0 | 0 | 4.01 | 1 |
| email-Eu-core | sym | 1 | 2.35 | 0.97 | 0 | 0 | 3.54 | 1 |
| sci50 | dir | 456 | 63.4 | 0.767 | 163 | 33 | 1.41e+03 | 1 |
| soc-Epinions1 | dir | 2 | 5.11 | 0.84 | 0 | 0 | 25.9 | 1.02 |
| soc-Epinions1 | sym | 1 | 4.89 | 0.998 | 0 | 0 | 15.3 | 1.02 |
| wiki-Vote | dir | 2 | 3.12 | 0.883 | 0 | 0 | 47.7 | 1 |
| wiki-Vote | sym | 1 | 3.25 | 1.05 | 1 | 1 | 7.63 | 1 |
| wikidata5m | dir | 1781 | 9.57 | 0.351 | 200 | 90 | 3.96e+05 | 1 |

## SNAP queries (all)

| dataset | variant | pattern | r | σ | Schur | CW₅ | U | ℓ2 | AGM | deg | Out | M | ℓ2/U |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca-GrQc | dir | cyclic | 28980 | 45.617 | 81 | 45.656 | 1.322e+06 | 4.889e+05 | 4.933e+06 | 2.347e+06 | 2.898e+05 | 3.726e+05 | 0.370 |
| ca-GrQc | dir | acyclic | 28980 | 45.617 | 81 | 45.656 | 1.322e+06 | 4.889e+05 | 4.933e+06 | 2.347e+06 | 2.898e+05 | 3.726e+05 | 0.370 |
| ca-GrQc | sym | cyclic | 28980 | 45.617 | 81 | 45.656 | 1.322e+06 | 4.889e+05 | 4.933e+06 | 2.347e+06 | 2.898e+05 | 3.726e+05 | 0.370 |
| com-dblp | dir | acyclic | 1049866 | 74.162 | 186 | 74.21 | 7.786e+07 | 1.133e+07 | 1.076e+09 | 1.186e+08 | 2.224e+06 | 4.858e+06 | 0.146 |
| com-dblp | sym | cyclic | 2099732 | 115.85 | 343 | 115.95 | 2.432e+08 | 4.566e+07 | 3.043e+09 | 7.202e+08 | 1.335e+07 | 2.459e+07 | 0.188 |
| com-youtube | dir | acyclic | 2987624 | 184.14 | 1.103e+04 | 203.54 | 5.501e+08 | 3.236e+08 | 5.164e+09 | 1.272e+10 | 3.056e+06 | 2.789e+07 | 0.588 |
| com-youtube | sym | cyclic | 5975248 | 210.4 | 2.875e+04 | 239.51 | 1.257e+09 | 2.955e+09 | 1.461e+10 | 1.718e+11 | 1.834e+07 | 1.629e+08 | 2.350 |
| email-Eu-core | dir | cyclic | 25571 | 64.901 | 266.1 | 64.943 | 1.66e+06 | 1.436e+06 | 4.089e+06 | 5.421e+06 | 3.957e+05 | 9.085e+05 | 0.865 |
| email-Eu-core | dir | acyclic | 25571 | 64.901 | 266.1 | 64.943 | 1.66e+06 | 1.538e+06 | 4.089e+06 | 5.421e+06 | 4.328e+05 | 9.376e+05 | 0.927 |
| email-Eu-core | sym | cyclic | 32770 | 77.172 | 346 | 77.209 | 2.529e+06 | 2.454e+06 | 5.932e+06 | 1.134e+07 | 7.151e+05 | 1.482e+06 | 0.970 |
| soc-Epinions1 | dir | cyclic | 508837 | 139.62 | 2338 | 142.2 | 7.104e+07 | 5.477e+07 | 3.63e+08 | 9.164e+08 | 2.221e+06 | 1.688e+07 | 0.771 |
| soc-Epinions1 | dir | acyclic | 508837 | 139.62 | 2338 | 142.2 | 7.104e+07 | 6.451e+07 | 3.63e+08 | 9.164e+08 | 3.586e+06 | 1.891e+07 | 0.908 |
| soc-Epinions1 | sym | cyclic | 811480 | 184.18 | 3044 | 187.45 | 1.495e+08 | 1.492e+08 | 7.31e+08 | 2.47e+09 | 9.747e+06 | 5.405e+07 | 0.998 |
| wiki-Vote | dir | cyclic | 103689 | 103.19 | 638.8 | 103.44 | 1.07e+07 | 8.674e+06 | 3.339e+07 | 4.739e+07 | 1.319e+05 | 1.367e+06 | 0.811 |
| wiki-Vote | dir | acyclic | 103689 | 103.19 | 638.8 | 103.44 | 1.07e+07 | 1.023e+07 | 3.339e+07 | 4.739e+07 | 7.466e+05 | 2.565e+06 | 0.956 |
| wiki-Vote | sym | cyclic | 201524 | 138.15 | 1065 | 138.59 | 2.784e+07 | 2.929e+07 | 9.047e+07 | 2.146e+08 | 3.65e+06 | 1.414e+07 | 1.052 |

## Losses: ℓ2 < U (2535 rows); 15 worst

| dataset | query | U | ℓ2 | ℓ2/U | AGM | Out | U term |
|---|---|---|---|---|---|---|---|
| wikidata5m/dir | `P17 . P17 . P17` | 8.341e+08 | 1.44e+06 | 0.002 | 1.613e+09 | 247 | sqrt(sR rS rT) |
| wikidata5m/dir | `P31 . P463 . P17` | 2.218e+08 | 1.158e+06 | 0.005 | 7.139e+08 | 1 | sqrt(sS rR rT) |
| wikidata5m/dir | `P17 . P17 . P463` | 1.327e+08 | 8.198e+05 | 0.006 | 4.271e+08 | 26 | sqrt(sT rR rS) |
| wikidata5m/dir | `P17 . P17 . P206` | 4.237e+07 | 2.889e+05 | 0.007 | 1.225e+08 | 37 | sqrt(sT rR rS) |
| wikidata5m/dir | `P17 . P17 . P706` | 3.408e+07 | 3.463e+05 | 0.010 | 1.877e+08 | 8 | sqrt(sT rR rS) |
| wikidata5m/dir | `P31 . P17 . P527` | 1.355e+08 | 1.556e+06 | 0.011 | 5.899e+08 | 24 | sqrt(sT rR rS) |
| wikidata5m/dir | `P31 . P527 . P17` | 1.355e+08 | 1.556e+06 | 0.011 | 5.899e+08 | 1 | sqrt(sS rR rT) |
| wikidata5m/dir | `P131 . P131 . P131` | 9.213e+07 | 1.168e+06 | 0.013 | 8.817e+08 | 47 | sqrt(sR rS rT) |
| wikidata5m/dir | `P17 . P463 . P463` | 3.515e+07 | 4.666e+05 | 0.013 | 1.131e+08 | 3 | sqrt(sS rR rT) |
| wikidata5m/dir | `P17 . P17 . P527` | 8.106e+07 | 1.102e+06 | 0.014 | 3.529e+08 | 34 | sqrt(sT rR rS) |
| wikidata5m/dir | `P17 . P463 . P740` | 1.051e+07 | 1.8e+05 | 0.017 | 4.487e+07 | 2 | sqrt(sT rR rS) |
| wikidata5m/dir | `P17 . P463 . P159` | 1.87e+07 | 3.217e+05 | 0.017 | 1.047e+08 | 44 | sqrt(sT rR rS) |
| wikidata5m/dir | `P131 . P131 . P159` | 2.761e+07 | 4.915e+05 | 0.018 | 2.643e+08 | 3 | sqrt(sR rS rT) |
| wikidata5m/dir | `P159 . P159 . P159` | 4.242e+06 | 8.7e+04 | 0.021 | 2.374e+07 | 4 | sqrt(sR rS rT) |
| wikidata5m/dir | `P131 . P17 . P463` | 3.65e+07 | 7.646e+05 | 0.021 | 3.493e+08 | 1 | sqrt(sR rS rT) |

## Biggest wins: U < min(AGM, ℓ2, deg) (204 rows); 15 largest

| dataset | query | U | min prior | prior/U | Out | U/Out | U term |
|---|---|---|---|---|---|---|---|
| wikidata5m/dir | `P17 . P47 . P17^T` | 1.411e+07 | 5.639e+07 | 4 | 1.74e+04 | 811 | sqrt(sS rR rT) |
| wikidata5m/dir | `P47 . P30 . P30^T` | 2.108e+05 | 8.422e+05 | 4 | 1332 | 158 | sqrt(sR rS rT) |
| wikidata5m/dir | `P47 . P206 . P206^T` | 8.137e+04 | 3.252e+05 | 4 | 1664 | 48.9 | sqrt(sR rS rT) |
| wikidata5m/dir | `P31 . P47 . P31^T` | 3.942e+07 | 1.575e+08 | 4 | 2 | 1.97e+07 | sqrt(sS rR rT) |
| wikidata5m/dir | `P463 . P463^T . P47` | 9.896e+05 | 3.955e+06 | 4 | 7615 | 130 | sqrt(sT rR rS) |
| wikidata5m/dir | `P47 . P527 . P527^T` | 6.757e+05 | 2.618e+06 | 3.87 | 8 | 8.45e+04 | sqrt(sR rS rT) |
| wikidata5m/dir | `P47 . P527^T . P527` | 6.757e+05 | 2.618e+06 | 3.87 | 1802 | 375 | sqrt(sR rS rT) |
| sci50/dir | `<http://example.org/sci/Award_Nominations> . <http://example.org/sci/Award_Nominations>^T . <http://example.org/sci/Influenced_By>` | 7.147e+05 | 2.179e+06 | 3.05 | 400 | 1.79e+03 | sqrt(sT rR rS) |
| wikidata5m/dir | `P47 . P361 . P361^T` | 1.399e+06 | 4.014e+06 | 2.87 | 957 | 1.46e+03 | sqrt(sR rS rT) |
| wikidata5m/dir | `P47 . P361^T . P361` | 1.399e+06 | 4.014e+06 | 2.87 | 14 | 9.99e+04 | sqrt(sR rS rT) |
| codex-l/dir | `P161 . P495 . P495^T` | 1.042e+05 | 2.734e+05 | 2.62 | 11 | 9.47e+03 | sqrt(sR rS rT) |
| wikidata5m/dir | `P47 . P706 . P206^T` | 1.247e+05 | 3.252e+05 | 2.61 | 12 | 1.04e+04 | sqrt(sR rS rT) |
| wikidata5m/dir | `P47 . P206 . P706^T` | 1.247e+05 | 3.252e+05 | 2.61 | 13 | 9.59e+03 | sqrt(sR rS rT) |
| codex-l/dir | `P47 . P530 . P530` | 5.54e+04 | 1.383e+05 | 2.5 | 1.432e+04 | 3.87 | sqrt(sR rS rT) |
| codex-l/dir | `P47 . P530 . P530^T` | 5.54e+04 | 1.383e+05 | 2.5 | 1.452e+04 | 3.82 | sqrt(sR rS rT) |

## Where certified σ matters

- Rows where exact-σ U beats ℓ2 but U_cert does not: **2**; rows where exact-σ U beats min(prior) but U_cert does not: 1.
- U_cert/U > 1.01 in 599/3124 rows; > 1.5 in 0; Schur alone > 1.5× in 2786.

## Certification of σ (exact arithmetic)

- Spectral views: 153. Every view satisfies, exactly, max(maxrow, maxcol) ≤ lo_sq ≤ hi_sq ≤ cert_sq ≤ maxrow·maxcol (asserted in `bounds.spectral`), and every stored float sig_cert satisfies sig_cert² ≥ cert_sq.
- Views whose float certificate of the first run (min(Schur, CW₅) in floating point) lay below the exact lower bound on σ: **6**: sci50 `Date_of_birth` (old 53.85164807134504, σ² ≥ 2900), sci50 `Date_of_death` (old 31.622776601683793, σ² ≥ 1000), sci50 `Place_of_death` (old 17.175564037317667, σ² ≥ 295), sci50 `Height` (old 24.49489742783178, σ² ≥ 600), sci50 `People_who_have_had_this_role` (old 4.795831523312719, σ² ≥ 23), sci50 `Named_after` (old 2.449489742783178, σ² ≥ 6).
- Views whose certified σ changed at all: 141/153; largest relative change 1.14e-01.
- Views whose exact bracket is wider than 1e-6 relative: **0**.
- Views where the float power iteration hit its 3000-step cap without meeting its own 1e-6 stopping test: **1**: wikidata5m `P106` (float bracket [410.0305388720186, 410.03240480202385], relative width 4.55e-06, because the float CW test stops once an iterate entry underflows; the exact bracket from the final iterate rounded up to integers is [410.03053887196165, 410.03053887212945], width 4.09e-13).
- Views whose σ estimate (the float Rayleigh value or `svds`) lies outside its exact bracket: 52, by at most 2.8e-13 relative (floating-point rounding of the estimate; no certified quantity uses it).
- Max relative width of the exact bracket over all views: 9.97e-07; rows whose U estimate is outside [U_lo, U_hi]: 405; max U_hi/U_lo: 1.00000199.
- Rigorous wins (U_hi < min(AGM, ℓ2, deg)): 204/3124; U_cert < min(AGM, ℓ2, deg): 203; U_cert/U ≤ 1.02 on 2915/3124 rows (p90 1.01543, max 1.13839).

## Pre-registered criterion (F3)

- Predicates (dataset, variant, predicate) used by some row: 134. U_cert ≥ ℓ2 on every query using it: 22 (16.4%); U_cert ≥ min(AGM, ℓ2, deg) on every query using it: 61 (45.5%).
- Per query: U_cert ≥ ℓ2 on 2537/3124 (81.2%); U_cert ≥ min(AGM, ℓ2, deg) on 2921/3124 (93.5%).

## Datasets (URL, sha256 of the downloaded file)

- sci50: sci50.nt built by bench/sparqloscope/replicate.py (path in $SCI50_NT)
- ca-GrQc: https://snap.stanford.edu/data/ca-GrQc.txt.gz — `a254442cdf5d684712578b630c2e0d7543518ab154ef2341cabb607572ce7230`
- email-Eu-core: https://snap.stanford.edu/data/email-Eu-core.txt.gz — `4b47acdb80197b085fe63c819c357ae488131ee904ed93d1b219a68b0f9e245f`
- wiki-Vote: https://snap.stanford.edu/data/wiki-Vote.txt.gz — `7d3e53626e14b8b09fb3b396bece9d481ad606bd64ceab066349ff57d4ada7fc`
- soc-Epinions1: https://snap.stanford.edu/data/soc-Epinions1.txt.gz — `69a2dab71fa5e3a0715487599fc16ca17ddc847379325a6c765bbad6e3e36938`
- com-youtube: https://snap.stanford.edu/data/bigdata/communities/com-youtube.ungraph.txt.gz — `dff1b97ba7d2fa9c59884b67dcd2275e717ff9501f86ed82ce6582ed4971f3e0`
- com-dblp: https://snap.stanford.edu/data/bigdata/communities/com-dblp.ungraph.txt.gz — `9eb0bd30312ddd04e2624f7c36c0983a2e99b116f0385be5a7fce6d6170f4cb3`
- wikidata5m: https://www.dropbox.com/s/6sbhm0rwo4l73jq/wikidata5m_transductive.tar.gz?dl=1 (train+valid+test) — `c233bb9d7dfc4eb2f038e0e5cee4b647b39dc4652f05ff118081077a454b3171`
- codex-l train: https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/train.txt — `4f2a696eb192a5fb076551b363a09a753565da7e4b7962202907309d39bf5f17`
- codex-l valid: https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/valid.txt — `f0119a22dc663e8df4a942cde7404927935b0c42e5a8980f5fb48ac6886e416f`
- codex-l test: https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/test.txt — `2d8188d6f199fc548c8e5fb97336a7ffd079240fc84c0425ed9c29d39bfdab8d`

Which bound is tightest per row: U 204, ℓ2 1018, degree 1902, AGM 0.
Median min(U, ℓ2, deg, AGM)/Out = 1e+04; median min(ℓ2, deg, AGM)/Out = 1.01e+04.

