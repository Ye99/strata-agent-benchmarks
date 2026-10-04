#!/usr/bin/env bash
# usage: runvar.sh <variant>   starts the server for that variant on :8090 and waits until loaded
D=$(cd "$(dirname "$0")" && pwd); N=$1
pkill -f "[s]erve/server.py.*--port 8090" ; pkill -f "[s]erve/server.py.*--port 8080"; sleep 5
python3 $D/mkcfg.py $N || exit 1
cd ~/p/Strata
setsid nohup .venv/bin/python serve/server.py --engine strata --config $D/cfg-$N.json --port 8090 > $D/server-$N.out 2>&1 < /dev/null &
for i in $(seq 1 90); do curl -s -m 3 http://127.0.0.1:8090/health | grep -q '"loaded": *true' && { echo loaded; exit 0; }; sleep 5; done
echo FAILED_TO_LOAD; tail -5 $D/server-$N.out; exit 1
