#!/usr/bin/env bash
D=$(cd "$(dirname "$0")" && pwd)
for v in "$@"; do
  echo "=== $v $(date +%T)" >> $D/chain2.log
  $D/runvar.sh $v >> $D/chain2.log 2>&1 || { echo "FAILED $v" >> $D/chain2.log; continue; }
  grep -E "expert_slots|arena" <(curl -s http://127.0.0.1:8090/metrics | tr ',' '\n') | tr '\n' ' ' >> $D/chain2.log; echo >> $D/chain2.log
  REPS=2 python3 $D/agent_bench.py http://127.0.0.1:8090 6000,50000 $D/res-$v-a.json > $D/log-$v-a.txt 2>&1
  REPS=1 python3 $D/agent_bench.py http://127.0.0.1:8090 120000,190000 $D/res-$v-b.json > $D/log-$v-b.txt 2>&1
  nvidia-smi --query-gpu=index,memory.used --format=csv,noheader >> $D/chain2.log; free -g | sed -n 2p >> $D/chain2.log
done
echo "=== done $(date +%T)" >> $D/chain2.log
