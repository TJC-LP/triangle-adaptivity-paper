"""Convert KG TSV triples (head<TAB>rel<TAB>tail) to N-Triples.

usage: tsv2nt.py <prefix-iri> <out.nt> <in.tsv>...
Entity e -> <prefix e>, relation r -> <prefix r>. Lines without exactly three
fields are skipped (as E2's prep.py did); duplicates are left to the store's
set semantics (E2 deduplicated per predicate too).
"""
import sys

prefix, out, ins = sys.argv[1], sys.argv[2], sys.argv[3:]
n = skipped = 0
with open(out, "w", encoding="utf-8") as w:
    for path in ins:
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) != 3:
                    skipped += 1
                    continue
                s, p, o = parts
                w.write(f"<{prefix}{s}> <{prefix}{p}> <{prefix}{o}> .\n")
                n += 1
print(out, "triples", n, "skipped", skipped)
