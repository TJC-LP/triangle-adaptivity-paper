"""Rebuild results.csv and summary.md from the committed files and compare.

usage: python3 -I check/rebuild_summary.py      (run from artifacts/e2/; needs numpy)

`src/summarize.py` merges the per-dataset `out/*.csv` files and reads the
per-predicate `out/*.spectral.json` files. Those `out/` files are not
committed, but `results.csv` is their concatenation (with derived columns
that summarize.py recomputes identically) and `spectral/` holds the
spectral files. This script lays them out as `out/` in a temporary
directory, runs `src/summarize.py` on it, and checks that the rebuilt
`results.csv` and `summary.md` equal the committed ones byte for byte.
Exit 0 when both match, 1 otherwise.
"""
import filecmp
import glob
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "out")
        os.makedirs(out)
        shutil.copyfile(os.path.join(HERE, "results.csv"), os.path.join(out, "all.csv"))
        for p in glob.glob(os.path.join(HERE, "spectral", "*.spectral.json")):
            shutil.copyfile(p, os.path.join(out, os.path.basename(p)))
        run = subprocess.run([sys.executable, "-I", os.path.join(HERE, "src", "summarize.py"), tmp],
                             stdout=subprocess.DEVNULL)
        if run.returncode != 0:
            print(f"summarize.py exited {run.returncode}")
            return 1
        ok = True
        for name in ("results.csv", "summary.md"):
            same = filecmp.cmp(os.path.join(tmp, name), os.path.join(HERE, name), shallow=False)
            print(f"{name}: {'identical' if same else 'DIFFERS'}")
            ok &= same
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
