#!/bin/zsh
V=${V:?set V to the A/B workspace holding data/, A/ and N/}
cd $V/data
out=$V/ab.csv; : > $out
for r in 1 2 3; do
 for d in skew.lb skew.ttl uni.lb medium.lb medium.ttl; do
  for b in A N; do
   $V/$b/zig-out/bin/leatherback bench --query --runs 5 --filter vf_ $d > $V/.ab.tmp 2>&1
   rc=$?
   grep VFTIME $V/.ab.tmp | sed "s|^|$b,$r,$d,|" >> $out
   echo "$b,$r,$d,rc=$rc" >> $V/ab.rc
  done
 done
done
echo done >> $V/ab.rc
