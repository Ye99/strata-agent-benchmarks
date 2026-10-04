#!/usr/bin/env bash
# usage: cc_task.sh <variant> ; real Claude Code multi-turn task against the :8090 server for that variant.
# Tools are limited to writing files in a throwaway dir and running pytest.
D=$(cd "$(dirname "$0")" && pwd); V=$1
$D/runvar.sh $V || exit 1
W=$(mktemp -d); cd $W && git init -q
export ANTHROPIC_BASE_URL=http://127.0.0.1:8090 ANTHROPIC_AUTH_TOKEN=x ANTHROPIC_MODEL=claude-sonnet-5-5 ANTHROPIC_SMALL_FAST_MODEL=claude-sonnet-5-5
export CLAUDE_CODE_MAX_CONTEXT_TOKENS=262144 CLAUDE_CODE_MAX_OUTPUT_TOKENS=16000 CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=${NONESS:-1}
T0=$(date +%s)
timeout 1500 claude -p "Create fizzbuzz.py with fizzbuzz(n) returning a list, and test_fizzbuzz.py using pytest. Run the tests with python3 -m pytest, fix any failure, then reply DONE and a one-line summary." --allowedTools "Write" "Edit" "Read" "Bash(python3 -m pytest:*)" < /dev/null > $D/cc-$V.out 2>&1
echo "$V wall=$(( $(date +%s)-T0 ))s files=$(ls $W | tr '\n' ' ')" | tee -a $D/cc.log
curl -s http://127.0.0.1:8090/metrics | python3 -c "
import json,sys;d=json.load(sys.stdin)
for r in d['requests']: print('  req: prompt',r['prompt_tokens'],'reused',r['reused'],'read',r['prompt_read'],'out',r['output_tokens'],'prompt_s',round(r['prompt_ms']/1000,1),'dec_tps',r['decode_tok_s'])" | tee -a $D/cc.log
