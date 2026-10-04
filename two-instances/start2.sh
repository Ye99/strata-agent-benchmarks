#!/usr/bin/env bash
# usage: start2.sh <name> <gpu> <port> <pool>  (does NOT kill others)
D=$(cd "$(dirname "$0")" && pwd); python3 $D/mk2.py $1 $2 $3 $4 || exit 1
cd /home/ye/p/Strata
setsid nohup .venv/bin/python serve/server.py --engine strata --config $D/cfg-$1.json --port $3 > $D/server-$1.out 2>&1 < /dev/null &
for i in $(seq 1 120); do curl -s -m 3 http://127.0.0.1:$3/health | grep -q '"loaded": *true' && { echo "$1 loaded after $((i*5))s"; exit 0; }; sleep 5; done
echo "$1 FAILED"; tail -5 $D/server-$1.out; exit 1
