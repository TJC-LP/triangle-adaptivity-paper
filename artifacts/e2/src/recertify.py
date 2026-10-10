"""Re-derive the certified columns of existing E2 outputs with exact arithmetic.

usage: recertify.py <old-out-dir> <prep-dir> <new-out-dir>

The first E2 run computed the Schur and Collatz-Wielandt "certified" sigma in
floating point; six spectral views came out below the true norm.  This script
rebuilds every spectral view from the prepared .npz files, reruns
`bounds.spectral` (whose float power iteration is unchanged, so sigma, svds and
the iteration count reproduce) and replaces, per CSV row, only the columns that
are certificates: sig_cert1-3, U_schur, U_cw, U_cert, U_hi, plus the new U_lo.
Every other column, Out and the counts included, is copied byte for byte, so
the triangle counts need not be redone.  It asserts that the stored sigma
estimates reproduce and reports any that fall outside the exact bracket.
"""
import csv
import glob
import json
import os
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bounds as B  # noqa: E402
from run import FIELDS  # noqa: E402

NPZ = {"wikidata5m": "w5m"}  # dataset label -> prep/out file stem, where they differ


def main():
    old, prep, new = sys.argv[1:4]
    os.makedirs(new, exist_ok=True)
    report = []
    for spath in sorted(glob.glob(os.path.join(old, "*.spectral.json"))):
        stem = os.path.basename(spath)[: -len(".spectral.json")]
        olds = json.load(open(spath))
        label = olds[0]["dataset"]
        assert NPZ.get(label, label) == stem, (label, stem)
        z = np.load(os.path.join(prep, stem + ".npz"))
        n = int(z["n"][0])
        names = list(z["preds"])
        sig, news = {}, []
        for o in olds:
            i = names.index(o["pred"])
            s, t = z[f"s_{i}"], z[f"o_{i}"]
            if o["variant"] == "sym":
                s, t = np.concatenate([s, t]), np.concatenate([t, s])
            m = B.csr_from_edges(s, t, n)
            assert m.nnz == o["r"], (o["pred"], m.nnz, o["r"])
            sp = B.spectral(m)
            # the float estimator must reproduce; only the certificates change.  svds (ARPACK)
            # is not bit-reproducible, so sigma may move in the last bits: keep the stored
            # sigma (the CSV's U column was computed from it) and test it against the bracket.
            for k in ("iters", "maxrow", "maxcol"):
                assert sp[k] == o[k], (label, o["pred"], k, sp[k], o[k])
            assert abs(sp["sigma"] / o["sigma"] - 1) <= 1e-9, (label, o["pred"], sp["sigma"], o["sigma"])
            sp["sigma_rerun"], sp["sigma"] = sp["sigma"], o["sigma"]
            s2, lo2, hi2 = Fraction(o["sigma"]) ** 2, Fraction(sp["lo_sq"]), Fraction(sp["hi_sq"])
            sp["sigma_in_bracket"] = bool(lo2 <= s2 <= hi2)
            # how far outside, relative (0 when inside); sigma is an estimate, not a bound
            sp["sigma_outside_rel"] = max(0.0, float(lo2 - s2) / float(lo2) / 2, float(s2 - hi2) / float(hi2) / 2)
            rec = dict(dataset=label, variant=o["variant"], pred=o["pred"], r=m.nnz, **sp)
            rec["old_schur"], rec["old_cw_few"], rec["old_sigma_lo"], rec["old_sigma_hi"] = (
                o["schur"], o["cw_few"], o["sigma_lo"], o["sigma_hi"])
            rec["old_sig_cert"] = min(o["schur"], o["cw_few"])
            rec["old_cert_valid"] = bool(Fraction(rec["old_sig_cert"]) ** 2 >= Fraction(sp["lo_sq"]))
            news.append(rec)
            sig[(o["variant"], o["pred"])] = sp
            report.append(rec)
            print(f"{label} {o['variant']} {o['pred']} r={m.nnz} sigma={sp['sigma']:.9g} "
                  f"cert {rec['old_sig_cert']:.12g}->{sp['sig_cert']:.12g} "
                  f"bracket [{sp['sigma_lo']:.10g},{sp['sigma_hi']:.10g}] w={sp['rel_width']:.2e}"
                  f"{'' if sp['converged'] else ' NOT-CONVERGED'}"
                  f"{'' if sp['sigma_in_bracket'] else ' SIGMA-OUTSIDE-BRACKET'}"
                  f"{'' if rec['old_cert_valid'] else ' OLD-CERT-INVALID'}", flush=True)
        with open(os.path.join(new, stem + ".spectral.json"), "w") as f:
            json.dump(news, f, indent=1, default=float)

        rows = list(csv.DictReader(open(os.path.join(old, stem + ".csv"))))
        for row in rows:
            sg = [sig[(row["variant"], row[f"p{k}"])] for k in (1, 2, 3)]
            r = [int(float(row[f"r{k}"])) for k in (1, 2, 3)]
            for k in (1, 2, 3):
                row[f"sig_cert{k}"] = repr(sg[k - 1]["sig_cert"])
            for key, val in B.certified_U(r, sg).items():
                row[key] = repr(val)
        with open(os.path.join(new, stem + ".csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for row in rows:
                w.writerow({k: row.get(k, "") for k in FIELDS})
    bad = [r for r in report if not r["old_cert_valid"]]
    print(f"views {len(report)}; old certificate below the exact lower bound: {len(bad)}")
    for r in bad:
        print(f"  {r['dataset']} {r['pred']} old {r['old_sig_cert']!r} lo_sq {r['lo_sq']} "
              f"maxdeg {max(r['maxrow'], r['maxcol'])}")
    nc = [r for r in report if not r["converged"]]
    print(f"not converged to 1e-6: {len(nc)}")
    for r in nc:
        print(f"  {r['dataset']} {r['pred']} iters {r['iters']} bracket [{r['sigma_lo']!r}, "
              f"{r['sigma_hi']!r}] rel_width {r['rel_width']:.3e}")
    ob = [r for r in report if not r["sigma_in_bracket"]]
    print(f"sigma estimate outside exact bracket: {len(ob)}")
    for r in ob:
        print(f"  {r['dataset']} {r['pred']} sigma {r['sigma']!r} [{r['sigma_lo']!r}, {r['sigma_hi']!r}] "
              f"outside by {r['sigma_outside_rel']:.1e} relative")


if __name__ == "__main__":
    main()
