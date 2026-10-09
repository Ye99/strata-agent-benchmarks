#!/usr/bin/env bash
# usage: run_one.sh <launcher> <label> <task> <attempt>   appends one JSON line to results-<label>.jsonl
AB=$(cd "$(dirname "$0")" && pwd); L=$1; LABEL=$2; T=$3; N=$4
W=$(mktemp -d); /bin/cp -rf $AB/tasks/$T/start/. $W; cd $W && git init -q
export CLAUDE_CODE_EFFORT_LEVEL=medium VLLM_KEEP_SERVER=1
T0=$(date +%s.%N)
timeout 1500 $L -p "$(cat $AB/tasks/$T/prompt.txt)" --permission-mode default \
  --allowedTools Read Write Edit Glob Grep "Bash(python3 -m unittest:*)" "Bash(python3 *.py:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(grep:*)" "Bash(head:*)" "Bash(tail:*)" "Bash(wc:*)" "Bash(diff:*)" --max-turns 40 --output-format json < /dev/null > $AB/out/$LABEL-$T-$N.json 2> $AB/out/$LABEL-$T-$N.err
RC=$?; WALL=$(echo "$(date +%s.%N) - $T0" | bc)
V=$(timeout 90 python3 $AB/tasks/$T/verify.py 2>&1 | tail -1)
python3 - "$AB" "$LABEL" "$T" "$N" "$RC" "$WALL" "$V" "$W" <<'PY'
import json,sys
ab,label,t,n,rc,wall,v,w=sys.argv[1:9]
try: o=json.load(open(f'{ab}/out/{label}-{t}-{n}.json'))
except Exception: o={}
try: vv=json.loads(v)
except Exception: vv={'passed':0,'total':None,'fails':[v[-160:]]}
u=o.get('usage') or {}
r=dict(label=label,task=t,attempt=int(n),rc=int(rc),wall_s=round(float(wall),1),turns=o.get('num_turns'),subtype=o.get('subtype'),is_error=o.get('is_error'),
       api_s=round((o.get('duration_api_ms') or 0)/1000,1),out_tokens=u.get('output_tokens'),in_tokens=u.get('input_tokens'),
       passed=vv.get('passed'),total=vv.get('total'),ok=(vv.get('total') is not None and vv.get('passed')==vv.get('total')),fails=vv.get('fails'),workdir=w)
open(f'{ab}/results-{label}.jsonl','a').write(json.dumps(r)+'\n'); print(json.dumps({k:r[k] for k in ('task','attempt','turns','wall_s','passed','total','ok','subtype')}))
PY
