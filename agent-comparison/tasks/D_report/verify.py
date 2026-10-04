import sys, subprocess; sys.path.insert(0, '.'); sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..'))
from harness import check, finish
r = subprocess.run([sys.executable, 'monthly_report.py', 'transactions.csv'], capture_output=True, text=True)
EXP = ['2000-02 42.00', '2023-01 150.50', '2023-02 20.00', '2023-03 10.25', '2023-04 80.00', '2023-12 200.99', '2024-02 61.00']
check('stdout exact', lambda: (_ for _ in ()).throw(AssertionError(r.stdout + r.stderr[-200:])) if r.stdout.split('\n')[:-1] != EXP else None)
bad = [l for l in r.stderr.splitlines() if 'skipping invalid date' in l]
check('skips exactly 3 bad dates', lambda: (_ for _ in ()).throw(AssertionError(str(bad))) if sorted(l.split()[-1] for l in bad) != ['1900-02-29', '2023-02-29', '2023-13-01'] else None)
import hashlib
check('csv untouched', lambda: (_ for _ in ()).throw(AssertionError('csv changed')) if len(open('transactions.csv').read().splitlines()) != 15 else None)
finish()
