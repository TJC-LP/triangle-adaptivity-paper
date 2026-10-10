#!/bin/zsh
S=${S:-$PWD/gates-out}; mkdir -p $S
W=${W:?set W to a checkout of the operator branch (build N)}
export ZIG_LOCAL_CACHE_DIR="$W/.zig-cache"
cd $W
zig build test-unit -Denable-onnx=false > $S/g_unit.log 2>&1; echo "test-unit=$?" >> $S/gates.rc
zig build lint -- --max-warnings 0 > $S/g_lint.log 2>&1; echo "lint=$?" >> $S/gates.rc
zig build test -Denable-onnx=false -Dtest-filter="sparql: " > $S/g_sparql.log 2>&1; echo "sparql=$?" >> $S/gates.rc
python3 scripts/changelog.py check > $S/g_changelog.log 2>&1; echo "changelog=$?" >> $S/gates.rc
zig fmt --check src bench build.zig > $S/g_fmt.log 2>&1; echo "fmt=$?" >> $S/gates.rc
echo done >> $S/gates.rc
