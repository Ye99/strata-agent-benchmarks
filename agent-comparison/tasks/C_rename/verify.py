import sys, os, re, subprocess; sys.path.insert(0, '.'); sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..'))
from harness import check, finish
def files(*ext):
    for r, _d, fs in os.walk('.'):
        if '__pycache__' in r: continue
        for f in fs:
            if f.endswith(ext): yield os.path.join(r, f)
def txt(p): return open(p).read()
check('no calc left', lambda: [(_ for _ in ()).throw(AssertionError(p)) for p in files('.py', '.md') if re.search(r'\bcalc\b', txt(p))])
check('calc_tax kept', lambda: (_ for _ in ()).throw(AssertionError('missing')) if not re.search(r'def calc_tax', txt('pkg/pricing.py')) else None)
check('compute_total defined', lambda: (_ for _ in ()).throw(AssertionError('missing')) if not re.search(r'def compute_total', txt('pkg/pricing.py')) else None)
def used():
    n = sum(1 for p in files('.py', '.md') if 'pricing.py' not in p and 'compute_total' in txt(p)); assert n >= 5, n
check('used in >=5 other files', used)
def tests():
    r = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'], capture_output=True, text=True); assert r.returncode == 0, r.stderr[-200:]
check('tests pass', tests)
def out():
    r = subprocess.run([sys.executable, 'main.py'], capture_output=True, text=True)
    exp = "{'subtotal': 18.0, 'tax': 3.6, 'total': 21.6}\norder 1: 18.00\norder 2: 60.00\ngrand total: 78.00\ndirect: 60.0\n"
    assert r.stdout == exp, r.stdout + r.stderr[-200:]
check('main output unchanged', out)
def tests_edited():
    assert 'compute_total' in txt('tests/test_pricing.py') and 'calc_tax' in txt('tests/test_pricing.py')
check('tests updated', tests_edited)
finish()
