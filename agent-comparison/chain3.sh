#!/usr/bin/env bash
# Phase 1: every task on Strata; phase 2: every task on vLLM; then restart Strata.
AB=$(cd "$(dirname "$0")" && pwd); LOG=$AB/chain3.log
TASKS="A_textstats B_inventory C_rename D_report E_wc F_expr"
suite() { for t in $TASKS; do for n in 1 2 3; do echo "$(date +%T) $2 $t $n" >> $LOG; $AB/run_one.sh $1 $2 $t $n >> $LOG 2>&1; done; done; }
echo "=== phase 1 strata $(date +%T)" >> $LOG
curl -s -m 3 http://127.0.0.1:8080/health | grep -q '"loaded": *true' || echo "strata not up" >> $LOG
suite ~/.local/bin/claude-qwen-strata-iq3_s strata
echo "=== stopping strata $(date +%T)" >> $LOG
kill $(pgrep -f "[s]erve/server.py") 2>/dev/null; sleep 10
echo "=== phase 2 vllm $(date +%T)" >> $LOG; nvidia-smi --query-gpu=index,memory.used --format=csv,noheader >> $LOG
suite ~/.local/bin/claude-qwen-vllm vllm
echo "=== stopping vllm $(date +%T)" >> $LOG
P=$(cat ~/p/vllm/bench/claude-qwen-vllm.pid 2>/dev/null)
if [ -n "$P" ]; then
  kill -INT -- "-$P" 2>/dev/null || kill -INT "$P" 2>/dev/null
  for i in $(seq 1 45); do kill -0 "$P" 2>/dev/null || break; sleep 1; done
  kill -0 "$P" 2>/dev/null && { kill -TERM -- "-$P" 2>/dev/null; sleep 15; }
  kill -0 "$P" 2>/dev/null && kill -KILL -- "-$P" 2>/dev/null
  rm -f ~/p/vllm/bench/claude-qwen-vllm.pid
fi
sleep 10; nvidia-smi --query-gpu=index,memory.used --format=csv,noheader >> $LOG
echo "=== restarting strata $(date +%T)" >> $LOG
cd /home/ye/p/Strata && (setsid nohup ./run-iq3_s.sh > strata-server.out 2>&1 < /dev/null &)
echo "=== done $(date +%T)" >> $LOG
