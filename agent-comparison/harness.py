import sys, json
RESULTS = []
def check(name, fn):
    try:
        fn(); RESULTS.append((name, True, ''))
    except BaseException as e:
        RESULTS.append((name, False, repr(e)[:160]))
def finish():
    p = sum(1 for r in RESULTS if r[1])
    print(json.dumps({'passed': p, 'total': len(RESULTS), 'fails': [(r[0], r[2]) for r in RESULTS if not r[1]][:4]}))
    sys.exit(0 if p == len(RESULTS) else 1)
