## codex-l (n = 871 queries)

| quantity | value |
|---|---|
| answers identical across the six policies | 5226/5226 rows |
| speedup exact vs sampled (t_sampled / t_exact): median / p90 / min | 0.0381 / 0.126 / 0.00203 |
| forced spread (worst / best forced driver): median / p90 / max | 2.7 / 8.6 / 47 |
| fastest forced driver is the exact-M argmin | 515/871 |
| fastest forced driver is the exact (2n + M) argmin | 532/871 |
|   same, queries whose fastest forced run ≥ 1 ms: M argmin / (2n+M) argmin | 3/7 / 6/7 |
| kernel-only gain of the exact pick: t_forced[sampled pick] / t_forced[exact pick], median / p90 / min / max | 1 / 1.56 / 0.0928 / 7.19 |
| sampled pick = fastest forced driver | 517/871 |
| exact pick = fastest forced driver | 501/871 |
| exact-M picks a different driver than sampled | 405/871 (46.5%) |
| sampled outcomes | accepted 300, gate 571 |
| exact outcomes | accepted 254, gate 617 |
| greedy / operator (t_greedy / t_sampled), all: median / p90 / max | 1.05 / 26.7 / 5.82e+03 |
| greedy / operator where sampled accepted: n, median / p90 / min | 300, 10.1 / 153 / 1.23 |
| gate declined: t_sampled / t_greedy (planning overhead), median / p90 | 1.04 / 1.19 |
| gate declined: t_greedy / t_best_forced, median / p90 / max; count > 1.5 | 1.83 / 3.92 / 35.4; 350/571 |
| exact (accepted) / best forced: median / p90 | 35.4 / 69.4 |
| timeouts per policy | none |
| engine exact M_π equals E2's M1..M3 (all three rotations) | 871/871 |
| Cor 4.3 (cor-kernel): min_π M_π ≤ U | 871/871 |
| min_π M_π / U: median / p90 / max | 0.000607 / 0.0104 / 0.57 |

## sci50 (n = 120 queries)

| quantity | value |
|---|---|
| answers identical across the six policies | 720/720 rows |
| speedup exact vs sampled (t_sampled / t_exact): median / p90 / min | 0.0256 / 0.138 / 0.000134 |
| forced spread (worst / best forced driver): median / p90 / max | 2.19 / 6.53 / 65.7 |
| fastest forced driver is the exact-M argmin | 71/120 |
| fastest forced driver is the exact (2n + M) argmin | 71/120 |
|   same, queries whose fastest forced run ≥ 1 ms: M argmin / (2n+M) argmin | 40/53 / 32/53 |
| kernel-only gain of the exact pick: t_forced[sampled pick] / t_forced[exact pick], median / p90 / min / max | 1 / 1.27 / 0.293 / 14.2 |
| sampled pick = fastest forced driver | 66/120 |
| exact pick = fastest forced driver | 62/120 |
| exact-M picks a different driver than sampled | 53/120 (44.2%) |
| sampled outcomes | accepted 33, gate 87 |
| exact outcomes | accepted 18, gate 102 |
| greedy / operator (t_greedy / t_sampled), all: median / p90 / max | 1.06 / 13.2 / 647 |
| greedy / operator where sampled accepted: n, median / p90 / min | 33, 8.76 / 80.9 / 1.23 |
| gate declined: t_sampled / t_greedy (planning overhead), median / p90 | 0.989 / 1.02 |
| gate declined: t_greedy / t_best_forced, median / p90 / max; count > 1.5 | 2.8 / 14.9 / 26.1; 70/87 |
| exact (accepted) / best forced: median / p90 | 68.1 / 292 |
| timeouts per policy | none |
| engine exact M_π equals E2's M1..M3 (all three rotations) | 120/120 |
| Cor 4.3 (cor-kernel): min_π M_π ≤ U | 120/120 |
| min_π M_π / U: median / p90 / max | 0.00247 / 0.0122 / 0.0556 |

## w5m (n = 250 queries)

| quantity | value |
|---|---|
| answers identical across the six policies | 1500/1500 rows |
| speedup exact vs sampled (t_sampled / t_exact): median / p90 / min | 0.0143 / 0.114 / 0.000706 |
| forced spread (worst / best forced driver): median / p90 / max | 4.99 / 28.2 / 132 |
| fastest forced driver is the exact-M argmin | 140/250 |
| fastest forced driver is the exact (2n + M) argmin | 151/250 |
|   same, queries whose fastest forced run ≥ 1 ms: M argmin / (2n+M) argmin | 59/93 / 54/93 |
| kernel-only gain of the exact pick: t_forced[sampled pick] / t_forced[exact pick], median / p90 / min / max | 1 / 2.15 / 0.024 / 15.2 |
| sampled pick = fastest forced driver | 147/250 |
| exact pick = fastest forced driver | 139/250 |
| exact-M picks a different driver than sampled | 126/250 (50.4%) |
| sampled outcomes | accepted 84, gate 166 |
| exact outcomes | accepted 59, gate 191 |
| greedy / operator (t_greedy / t_sampled), all: median / p90 / max | 1.21 / 36.5 / 4.94e+03 |
| greedy / operator where sampled accepted: n, median / p90 / min | 83, 10.2 / 751 / 0.508 |
| gate declined: t_sampled / t_greedy (planning overhead), median / p90 | 0.95 / 1.02 |
| gate declined: t_greedy / t_best_forced, median / p90 / max; count > 1.5 | 3.53 / 20.2 / 221; 116/166 |
| exact (accepted) / best forced: median / p90 | 121 / 633 |
| timeouts per policy | greedy 1 |
| engine exact M_π equals E2's M1..M3 (all three rotations) | 250/250 |
| Cor 4.3 (cor-kernel): min_π M_π ≤ U | 250/250 |
| min_π M_π / U: median / p90 / max | 4.15e-05 / 0.00209 / 0.47 |

