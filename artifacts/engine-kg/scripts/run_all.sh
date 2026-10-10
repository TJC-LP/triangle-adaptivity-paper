#!/bin/bash
# Reproduce the engine-kg driver-policy experiment (Fable item 6).
# usage: run_all.sh <leatherback-binary> <e2-dir> <sci50.nt> <workdir>
# The binary is a ReleaseFast build of the driver-policy branch
# (zig build -Doptimize=ReleaseFast -Denable-onnx=false).
set -euo pipefail
B=$1; E2=$2; SCI=$3; W=$4; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W"/data "$W"/stores "$W"/raw
K=$E2/data/kg
python3 -I "$HERE/tsv2nt.py" http://wd/ "$W/data/codex-l.nt" $K/codex-l-train.txt $K/codex-l-valid.txt $K/codex-l-test.txt
python3 -I "$HERE/tsv2nt.py" http://wd/ "$W/data/w5m.nt" $K/w5m/wikidata5m_transductive_{train,valid,test}.txt
"$B" build -o "$W/stores/codex-l.lb" "$W/data/codex-l.nt"
"$B" build -o "$W/stores/w5m.lb" "$W/data/w5m.nt"
"$B" build -o "$W/stores/sci50.lb" "$SCI"
python3 -I "$HERE/make_queries.py" "$E2/results.csv" "$W/queries"
for n in codex-l sci50 w5m; do
  "$B" bench --triangle-drivers --runs 5 --timeout-ms 30000 "$W/stores/$n.lb" "$W/queries/$n.tsv" > "$W/raw/$n.csv"
done
python3 -I "$HERE/analyze.py" "$W/queries/meta.csv" "$W/summary.md" codex-l="$W/raw/codex-l.csv" sci50="$W/raw/sci50.csv" w5m="$W/raw/w5m.csv"
