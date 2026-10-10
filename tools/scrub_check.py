#!/usr/bin/env python3
"""Fail if the repository contains internal identifiers or machine-local paths.

Usage: python3 -I tools/scrub_check.py [--deny FILE] [repo-root]
       (default root: the parent of tools/)

Scans every file under the repository root except `.git/` and Lake's build
directory `lean/.lake/`. Text files are scanned as UTF-8 (errors replaced);
PDFs are scanned both as raw bytes and, when `pdftotext` is on PATH, as
extracted text (page text is usually compressed, so the raw scan alone would
miss it). Exit 0 when clean, 1 with one line per hit otherwise.

Flagged (the literal strings are in PATTERNS below, split so that this file
does not flag itself):
  * machine-local paths (macOS home directories, the macOS temp directory)
  * internal ticket identifiers of the engine repository (any number,
    any case) and its tracker's links
  * with --deny FILE, every non-empty, non-comment line of FILE as a
    literal string (case-insensitive): for identifiers that must not be
    written into this repository even in fragments, such as private commit
    hashes or branch names; keep FILE outside the repository
  * issue-tracker links and Claude Code session links
  * any e-mail address other than the author's
"""
import os
import re
import shutil
import subprocess
import sys

AUTHOR_EMAIL = "rcaputo3" + "@" + "tjclp.com"

# Patterns are assembled from fragments so this file does not flag itself.
PATTERNS = [
    ("machine-local path", re.compile(re.escape("/" + "Users/"))),
    ("machine-local path", re.compile(re.escape("/private" + "/tmp"))),
    ("internal ticket", re.compile(r"\b" + "tjc" + r"-\d+", re.IGNORECASE)),
    ("tracker link", re.compile(re.escape("linear" + ".app"), re.IGNORECASE)),
    ("session link", re.compile(re.escape("claude.ai/code/" + "session"), re.IGNORECASE)),
]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")

SKIP_DIRS = {".git"}
SKIP_PATHS = {os.path.join("lean", ".lake")}


def texts_of(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    yield "raw", raw.decode("utf-8", errors="replace")
    if path.lower().endswith(".pdf") and shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-q", path, "-"], capture_output=True)
        if out.returncode != 0:
            yield "pdftotext-failed", ""
        else:
            yield "pdf-text", out.stdout.decode("utf-8", errors="replace")


def scan(root, patterns=PATTERNS):
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SKIP_DIRS and os.path.normpath(os.path.join(rel_dir, d)) not in SKIP_PATHS
        )
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            for kind, text in texts_of(path):
                if kind == "pdftotext-failed":
                    hits.append(f"{rel}: pdftotext failed; cannot scan page text")
                    continue
                for lineno, line in enumerate(text.splitlines(), 1):
                    for label, pat in patterns:
                        for m in pat.finditer(line):
                            hits.append(f"{rel}:{lineno} [{kind}] {label}: {m.group(0)!r}")
                    for m in EMAIL.finditer(line):
                        if m.group(0).lower() != AUTHOR_EMAIL:
                            hits.append(f"{rel}:{lineno} [{kind}] e-mail address: {m.group(0)!r}")
    return hits


def main():
    args = sys.argv[1:]
    patterns = list(PATTERNS)
    if args[:1] == ["--deny"]:
        if len(args) < 2:
            print("usage: scrub_check.py [--deny FILE] [repo-root]", file=sys.stderr)
            return 2
        with open(args[1], encoding="utf-8") as fh:
            for line in fh:
                tok = line.strip()
                if tok and not tok.startswith("#"):
                    patterns.append(("denied string", re.compile(re.escape(tok), re.IGNORECASE)))
        args = args[2:]
    root = args[0] if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not shutil.which("pdftotext"):
        print("warning: pdftotext not found; PDFs scanned as raw bytes only", file=sys.stderr)
    hits = scan(root, patterns)
    for h in hits:
        print(h)
    if hits:
        print(f"scrub_check: FAIL ({len(hits)} hit(s))", file=sys.stderr)
        return 1
    print("scrub_check: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
