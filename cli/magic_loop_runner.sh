#!/bin/bash
N=${1:-1}
for ((i=1; i<=N; i++)); do
  echo -e "\n=== Magic Loop Run $i/$N ==="
  ./cli/magic_loop_full.sh || echo "Magic loop run $i failed."
  sleep 2
done
