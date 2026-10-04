#!/usr/bin/env bash
# usage: run2.sh <label> <url1> <url2> ; two parallel workers, 3 tasks x 2 attempts each
D=$(cd "$(dirname "$0")" && pwd); AB=$D/ab; L=$1
worker() { # url label tasks
  for n in 1 2; do for t in $3; do echo "$(date +%T) $2 $t $n" >> $D/$L.log; CC_URL=$1 $AB/run_one.sh $D/cc-url.sh $2 $t $n >> $D/$L.log 2>&1; done; done; }
T0=$(date +%s); echo "=== $L start $(date +%T)" >> $D/$L.log
worker $2 $L-w1 "A_textstats B_inventory C_rename" & 
worker $3 $L-w2 "D_report E_wc F_expr" &
wait; echo "=== $L done makespan=$(( $(date +%s)-T0 ))s" >> $D/$L.log
