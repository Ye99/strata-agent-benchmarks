#!/usr/bin/env bash
# usage: chain.sh <variant> [...]   start each variant, bench it, log memory
D=$(cd "$(dirname "$0")" && pwd)
for v in "$@"; do
  echo "=== $v $(date +%T)" >> $D/chain.log
  $D/runvar.sh $v >> $D/chain.log 2>&1 || { echo "FAILED $v" >> $D/chain.log; continue; }
  curl -s http://127.0.0.1:8090/metrics | tr ',' '\n' | grep -E "expert_slots|arena|cached_experts|vram" | tr '\n' ' ' >> $D/chain.log; echo >> $D/chain.log
  REPS=1 python3 $D/agent_bench.py http://127.0.0.1:8090 ${DEPTHS:-6000,43000} $D/res-$v.json > $D/log-$v.txt 2>&1
  nvidia-smi --query-gpu=index,memory.used --format=csv,noheader >> $D/chain.log
  free -g | sed -n 2p >> $D/chain.log
done
echo "=== done $(date +%T)" >> $D/chain.log
