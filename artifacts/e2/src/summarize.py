"""Merge per-dataset CSVs into results.csv and write summary.md."""
import csv
import glob
import json
import math
import os
import sys

import numpy as np

E = sys.argv[1]
OUT = os.path.join(E, "out")
GROUP = {"sci50": "sci50", "codex-l": "KG", "wikidata5m": "KG"}

rows = []
for p in sorted(glob.glob(os.path.join(OUT, "*.csv"))):
    with open(p) as f:
        rows.extend(csv.DictReader(f))
num = ["r1", "r2", "r3", "U", "U_schur", "U_cw", "U_cert", "U_hi", "U_lo", "agm", "deg_bound", "l2",
       "l2_fwd", "l2_rev", "out", "M", "sigma1", "sigma2", "sigma3", "s1", "s2", "s3"]
for r in rows:
    for k in num:
        r[k] = float(r[k])
    r["group"] = GROUP.get(r["dataset"], "SNAP")
    r["agm_over_U"] = r["agm"] / r["U"]
    r["l2_over_U"] = r["l2"] / r["U"]
    r["deg_over_U"] = r["deg_bound"] / r["U"]
    r["U_over_out"] = r["U"] / r["out"]
    r["l2_over_out"] = r["l2"] / r["out"]
    r["M_over_U"] = r["M"] / r["U"]
    r["Ucert_over_U"] = r["U_cert"] / r["U"]
    r["Uschur_over_U"] = r["U_schur"] / r["U"]
    r["Ucw_over_U"] = r["U_cw"] / r["U"]
    r["best_prior"] = min(r["agm"], r["l2"], r["deg_bound"])
    r["bestprior_over_U"] = r["best_prior"] / r["U"]
    r["min_all"] = min(r["best_prior"], r["U"])

fields = list(rows[0].keys())
with open(os.path.join(E, "results.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

# sanity: every bound must dominate Out
viol = [(r["query"], b) for r in rows for b in ("U", "U_cert", "U_hi", "agm", "l2", "deg_bound")
        if r["out"] > r[b] * (1 + 1e-9)]


def q(xs, p):
    return float(np.quantile(np.asarray(xs), p)) if xs else float("nan")


def dist(xs):
    if not xs:
        return "n/a"
    return (f"{q(xs,0):.3g} / {q(xs,0.5):.3g} / {q(xs,0.9):.3g} / {max(xs):.3g}")


def block(sel, title):
    n = len(sel)
    if n == 0:
        return []
    L = [f"### {title} (n = {n})", ""]
    L.append("| quantity | min / median / p90 / max |")
    L.append("|---|---|")
    for key, lab in (("agm_over_U", "AGM / U"), ("l2_over_U", "ℓ2 / U"),
                     ("deg_over_U", "degree bound / U"),
                     ("bestprior_over_U", "min(AGM, ℓ2, deg) / U"),
                     ("U_over_out", "U / Out"), ("l2_over_out", "ℓ2 / Out"),
                     ("M_over_U", "M / U"),
                     ("Ucert_over_U", "U_cert / U (σ² → exact min(Schur, CW₅))"),
                     ("Uschur_over_U", "U_Schur / U"), ("Ucw_over_U", "U_CW₅ / U")):
        L.append(f"| {lab} | {dist([r[key] for r in sel])} |")
    lt_l2 = sum(r["U"] < r["l2"] for r in sel)
    lt_agm = sum(r["U"] < r["agm"] for r in sel)
    lt_deg = sum(r["U"] < r["deg_bound"] for r in sel)
    lt_all = sum(r["U"] < r["best_prior"] for r in sel)
    cert_l2 = sum(r["U_cert"] < r["l2"] for r in sel)
    cert_all = sum(r["U_cert"] < r["best_prior"] for r in sel)
    L.append("")
    L.append(f"- U < ℓ2: **{lt_l2}/{n}** ({100*lt_l2/n:.1f}%); U < AGM: {lt_agm}/{n}; "
             f"U < degree bound: {lt_deg}/{n}; U < min(AGM, ℓ2, deg): **{lt_all}/{n}** ({100*lt_all/n:.1f}%)")
    L.append(f"- with certified σ (exact min(Schur, CW₅)): U_cert < ℓ2: {cert_l2}/{n}; "
             f"U_cert < min(AGM, ℓ2, deg): {cert_all}/{n}")
    L.append(f"- M ≤ U: {sum(r['M'] <= r['U'] for r in sel)}/{n}; "
             f"Out = 0 rows: {sum(r['out'] == 0 for r in sel)}")
    terms = {}
    for r in sel:
        terms[r["U_term"]] = terms.get(r["U_term"], 0) + 1
    L.append("- binding U term: " + ", ".join(f"`{k}` {v}" for k, v in sorted(terms.items(), key=lambda t: -t[1])))
    L.append("")
    return L


md = ["# E2: spectral triangle bound U on real data", ""]
md.append("Every row is one triangle query `?x R ?y . ?y S ?z . ?z T ?x` (R/S/T possibly transposed) "
          "with Out > 0. Queries are canonical up to rotation and whole-cycle reversal. "
          "U uses the estimate σ from power iteration (Rayleigh lower, Collatz–Wielandt upper, stopped at 1e-6 "
          "relative width or 3000 steps) cross-checked against `svds`; U is an estimate of the bound, not a certificate. "
          "Certified quantities are exact: σ² ≤ maxrow·maxcol (Schur, an integer) and σ² ≤ max_i (Bw)_i/w_i "
          "(Collatz–Wielandt, B = AᵀA, w the float iterate rounded up to a positive integer vector, the ratio "
          "an exact rational). U_cert replaces σ² by min(Schur, CW after 5 power steps from 𝟙); U_hi and U_lo use the "
          "exact bracket σ² ∈ [max(maxdeg, Rayleigh), min(U_cert's bound, CW at the final and best iterates)]. "
          "Every U is evaluated from the exact squared terms and its square root is rounded outward "
          "(up for U_schur, U_cw, U_cert, U_hi; down for U_lo). "
          "ℓ2 = min(ΣaΣbΣc², Σa'²Σb'²Σc'²)^{1/3}. Out is counted exactly, and cross-checked with "
          "`(A_R@A_S).multiply(A_T.T).sum()` wherever the SpGEMM was ≤3e8 flops.")
md.append("")
md.append(f"Sanity: rows where some bound < Out: **{len(viol)}**" + (f" {viol[:5]}" if viol else ""))
mm = [r for r in rows if r["matmul_check"]]
md.append(f"; SpGEMM cross-checks: {sum(r['matmul_check']=='ok' for r in mm)}/{len(mm)} ok.")
md.append("")
md.append("Distribution columns are min / median / p90 / max.")
md.append("")
md += block(rows, "All queries")
for g in ("sci50", "SNAP", "KG"):
    md += block([r for r in rows if r["group"] == g], f"Group {g}")

# per-dataset short table
md.append("## Per dataset")
md.append("")
md.append("| dataset | variant | n | med AGM/U | med ℓ2/U | U<ℓ2 | U<min(prior) | med U/Out | med U_cert/U |")
md.append("|---|---|---|---|---|---|---|---|---|")
keys = sorted({(r["dataset"], r["variant"]) for r in rows})
for d, v in keys:
    sel = [r for r in rows if r["dataset"] == d and r["variant"] == v]
    md.append(f"| {d} | {v} | {len(sel)} | {q([r['agm_over_U'] for r in sel],.5):.3g} | "
              f"{q([r['l2_over_U'] for r in sel],.5):.3g} | {sum(r['U']<r['l2'] for r in sel)} | "
              f"{sum(r['U']<r['best_prior'] for r in sel)} | {q([r['U_over_out'] for r in sel],.5):.3g} | "
              f"{q([r['Ucert_over_U'] for r in sel],.5):.3g} |")
md.append("")

# SNAP full table
md.append("## SNAP queries (all)")
md.append("")
md.append("| dataset | variant | pattern | r | σ | Schur | CW₅ | U | ℓ2 | AGM | deg | Out | M | ℓ2/U |")
md.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
snap_json = {}
for p in glob.glob(os.path.join(OUT, "*.spectral.json")):
    for s in json.load(open(p)):
        snap_json[(s["dataset"], s["variant"], s["pred"])] = s
for r in rows:
    if r["group"] != "SNAP":
        continue
    s = snap_json[(r["dataset"], r["variant"], r["p1"])]
    md.append(f"| {r['dataset']} | {r['variant']} | {r['pattern']} | {r['r1']:.0f} | {s['sigma']:.5g} | "
              f"{s['schur']:.4g} | {s['cw_few']:.5g} | {r['U']:.4g} | {r['l2']:.4g} | {r['agm']:.4g} | "
              f"{r['deg_bound']:.4g} | {r['out']:.4g} | {r['M']:.4g} | {r['l2_over_U']:.3f} |")
md.append("")

# losses
loss = sorted([r for r in rows if r["l2"] < r["U"]], key=lambda r: r["l2_over_U"])
md.append(f"## Losses: ℓ2 < U ({len(loss)} rows); 15 worst")
md.append("")
md.append("| dataset | query | U | ℓ2 | ℓ2/U | AGM | Out | U term |")
md.append("|---|---|---|---|---|---|---|---|")
for r in loss[:15]:
    md.append(f"| {r['dataset']}/{r['variant']} | `{r['query']}` | {r['U']:.4g} | {r['l2']:.4g} | "
              f"{r['l2_over_U']:.3f} | {r['agm']:.4g} | {r['out']:.4g} | {r['U_term']} |")
md.append("")
wins = sorted([r for r in rows if r["U"] < r["best_prior"]], key=lambda r: r["bestprior_over_U"], reverse=True)
md.append(f"## Biggest wins: U < min(AGM, ℓ2, deg) ({len(wins)} rows); 15 largest")
md.append("")
md.append("| dataset | query | U | min prior | prior/U | Out | U/Out | U term |")
md.append("|---|---|---|---|---|---|---|---|")
for r in wins[:15]:
    md.append(f"| {r['dataset']}/{r['variant']} | `{r['query']}` | {r['U']:.4g} | {r['best_prior']:.4g} | "
              f"{r['bestprior_over_U']:.3g} | {r['out']:.4g} | {r['U_over_out']:.3g} | {r['U_term']} |")
md.append("")
flip = [r for r in rows if r["U"] < r["l2"] <= r["U_cert"]]
md.append(f"## Where certified σ matters")
md.append("")
md.append(f"- Rows where exact-σ U beats ℓ2 but U_cert does not: **{len(flip)}**; "
          f"rows where exact-σ U beats min(prior) but U_cert does not: "
          f"{sum(r['U'] < r['best_prior'] <= r['U_cert'] for r in rows)}.")
md.append(f"- U_cert/U > 1.01 in {sum(r['Ucert_over_U'] > 1.01 for r in rows)}/{len(rows)} rows; "
          f"> 1.5 in {sum(r['Ucert_over_U'] > 1.5 for r in rows)}; "
          f"Schur alone > 1.5× in {sum(r['Uschur_over_U'] > 1.5 for r in rows)}.")
md.append("")

# exact certification of sigma, per spectral view
views = []
for p in sorted(glob.glob(os.path.join(OUT, "*.spectral.json"))):
    views.extend(json.load(open(p)))
md.append("## Certification of σ (exact arithmetic)")
md.append("")
nv = len(views)
md.append(f"- Spectral views: {nv}. Every view satisfies, exactly, max(maxrow, maxcol) ≤ lo_sq ≤ hi_sq ≤ cert_sq ≤ "
          f"maxrow·maxcol (asserted in `bounds.spectral`), and every stored float sig_cert satisfies sig_cert² ≥ cert_sq.")
if views and "old_cert_valid" in views[0]:
    bad = [v for v in views if not v["old_cert_valid"]]
    md.append(f"- Views whose float certificate of the first run (min(Schur, CW₅) in floating point) lay below the "
              f"exact lower bound on σ: **{len(bad)}**: " + ", ".join(
                  f"{v['dataset']} `{v['pred'].rsplit('/', 1)[-1].strip('<>')}` (old {v['old_sig_cert']!r}, "
                  f"σ² ≥ {v['lo_sq']})" for v in bad) + ".")
    chg = [v for v in views if v["sig_cert"] != v["old_sig_cert"]]
    md.append(f"- Views whose certified σ changed at all: {len(chg)}/{nv}; largest relative change "
              f"{max((abs(v['sig_cert'] / v['old_sig_cert'] - 1) for v in chg), default=0):.2e}.")
nc = [v for v in views if not v["converged"]]
md.append(f"- Views whose exact bracket is wider than 1e-6 relative: **{len(nc)}**" + (": " + "; ".join(
    f"{v['dataset']} `{v['pred'].rsplit('/', 1)[-1].strip('<>')}` ({v['iters']} steps, σ ∈ [{v['sigma_lo']:.10g}, "
    f"{v['sigma_hi']:.10g}], relative width {v['rel_width']:.2e})" for v in nc) if nc else "") + ".")
cap = [v for v in views if v["iters"] >= 3000]
md.append(f"- Views where the float power iteration hit its 3000-step cap without meeting its own 1e-6 stopping "
          f"test: **{len(cap)}**" + (": " + "; ".join(
    f"{v['dataset']} `{v['pred'].rsplit('/', 1)[-1].strip('<>')}` (float bracket [{v['sigma_lo_fp']!r}, "
    f"{v['sigma_hi_fp']!r}], relative width {(v['sigma_hi_fp'] - v['sigma_lo_fp']) / v['sigma_hi_fp']:.2e}, "
    f"because the float CW test stops once an iterate entry underflows; the exact bracket from the final "
    f"iterate rounded up to integers is [{v['sigma_lo']!r}, {v['sigma_hi']!r}], width {v['rel_width']:.2e})"
    for v in cap) if cap else "") + ".")
ob = [v for v in views if not v["sigma_in_bracket"]]
md.append(f"- Views whose σ estimate (the float Rayleigh value or `svds`) lies outside its exact bracket: {len(ob)}, "
          f"by at most {max((v.get('sigma_outside_rel', 0.0) for v in ob), default=0.0):.1e} relative "
          f"(floating-point rounding of the estimate; no certified quantity uses it).")
md.append(f"- Max relative width of the exact bracket over all views: {max(v['rel_width'] for v in views):.2e}; "
          f"rows whose U estimate is outside [U_lo, U_hi]: {sum(not (r['U_lo'] <= r['U'] <= r['U_hi']) for r in rows)}; "
          f"max U_hi/U_lo: {max(r['U_hi'] / r['U_lo'] for r in rows):.9g}.")
md.append(f"- Rigorous wins (U_hi < min(AGM, ℓ2, deg)): {sum(r['U_hi'] < r['best_prior'] for r in rows)}/{len(rows)}; "
          f"U_cert < min(AGM, ℓ2, deg): {sum(r['U_cert'] < r['best_prior'] for r in rows)}; "
          f"U_cert/U ≤ 1.02 on {sum(r['Ucert_over_U'] <= 1.02 for r in rows)}/{len(rows)} rows "
          f"(p90 {q([r['Ucert_over_U'] for r in rows], .9):.6g}, max {max(r['Ucert_over_U'] for r in rows):.6g}).")
md.append("")

# the pre-registered criterion (F3): per (dataset, variant, predicate) and per query
md.append("## Pre-registered criterion (F3)")
md.append("")
uses = {}
for r in rows:
    for p in {r["p1"], r["p2"], r["p3"]}:
        uses.setdefault((r["dataset"], r["variant"], p), []).append(r)
npred = len(uses)
no_l2 = sum(all(r["U_cert"] >= r["l2"] for r in v) for v in uses.values())
no_bp = sum(all(r["U_cert"] >= r["best_prior"] for r in v) for v in uses.values())
q_l2 = sum(r["U_cert"] >= r["l2"] for r in rows)
q_bp = sum(r["U_cert"] >= r["best_prior"] for r in rows)
md.append(f"- Predicates (dataset, variant, predicate) used by some row: {npred}. "
          f"U_cert ≥ ℓ2 on every query using it: {no_l2} ({100*no_l2/npred:.1f}%); "
          f"U_cert ≥ min(AGM, ℓ2, deg) on every query using it: {no_bp} ({100*no_bp/npred:.1f}%).")
md.append(f"- Per query: U_cert ≥ ℓ2 on {q_l2}/{len(rows)} ({100*q_l2/len(rows):.1f}%); "
          f"U_cert ≥ min(AGM, ℓ2, deg) on {q_bp}/{len(rows)} ({100*q_bp/len(rows):.1f}%).")
md.append("")

md.append("## Datasets (URL, sha256 of the downloaded file)")
md.append("")
PROV = [
 ("sci50", "sci50.nt built by bench/sparqloscope/replicate.py (path in $SCI50_NT)"),
 ("ca-GrQc", "https://snap.stanford.edu/data/ca-GrQc.txt.gz", "a254442cdf5d684712578b630c2e0d7543518ab154ef2341cabb607572ce7230"),
 ("email-Eu-core", "https://snap.stanford.edu/data/email-Eu-core.txt.gz", "4b47acdb80197b085fe63c819c357ae488131ee904ed93d1b219a68b0f9e245f"),
 ("wiki-Vote", "https://snap.stanford.edu/data/wiki-Vote.txt.gz", "7d3e53626e14b8b09fb3b396bece9d481ad606bd64ceab066349ff57d4ada7fc"),
 ("soc-Epinions1", "https://snap.stanford.edu/data/soc-Epinions1.txt.gz", "69a2dab71fa5e3a0715487599fc16ca17ddc847379325a6c765bbad6e3e36938"),
 ("com-youtube", "https://snap.stanford.edu/data/bigdata/communities/com-youtube.ungraph.txt.gz", "dff1b97ba7d2fa9c59884b67dcd2275e717ff9501f86ed82ce6582ed4971f3e0"),
 ("com-dblp", "https://snap.stanford.edu/data/bigdata/communities/com-dblp.ungraph.txt.gz", "9eb0bd30312ddd04e2624f7c36c0983a2e99b116f0385be5a7fce6d6170f4cb3"),
 ("wikidata5m", "https://www.dropbox.com/s/6sbhm0rwo4l73jq/wikidata5m_transductive.tar.gz?dl=1 (train+valid+test)", "c233bb9d7dfc4eb2f038e0e5cee4b647b39dc4652f05ff118081077a454b3171"),
 ("codex-l train", "https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/train.txt", "4f2a696eb192a5fb076551b363a09a753565da7e4b7962202907309d39bf5f17"),
 ("codex-l valid", "https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/valid.txt", "f0119a22dc663e8df4a942cde7404927935b0c42e5a8980f5fb48ac6886e416f"),
 ("codex-l test", "https://raw.githubusercontent.com/tsafavi/codex/master/data/triples/codex-l/test.txt", "2d8188d6f199fc548c8e5fb97336a7ffd079240fc84c0425ed9c29d39bfdab8d"),
]
for t in PROV:
    md.append(f"- {t[0]}: {t[1]}" + (f" — `{t[2]}`" if len(t) > 2 else ""))
md.append("")
md.append(f"Which bound is tightest per row: U {sum(r['U'] <= r['best_prior'] for r in rows)}, "
          f"ℓ2 {sum(r['l2'] < r['U'] and r['l2'] <= min(r['agm'], r['deg_bound']) for r in rows)}, "
          f"degree {sum(r['deg_bound'] < r['U'] and r['deg_bound'] < r['l2'] for r in rows)}, "
          f"AGM {sum(r['agm'] < min(r['U'], r['l2'], r['deg_bound']) for r in rows)}.")
md.append(f"Median min(U, ℓ2, deg, AGM)/Out = {q([r['min_all']/r['out'] for r in rows], .5):.3g}; "
          f"median min(ℓ2, deg, AGM)/Out = {q([r['best_prior']/r['out'] for r in rows], .5):.3g}.")
md.append("")
open(os.path.join(E, "summary.md"), "w").write("\n".join(md) + "\n")
print("\n".join(md[:80]))
