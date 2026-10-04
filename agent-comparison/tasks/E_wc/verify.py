import sys, os, subprocess, tempfile; sys.path.insert(0, '.'); sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..'))
from harness import check, finish
D = tempfile.mkdtemp()
def w(name, data):
    p = os.path.join(D, name); open(p, 'wb').write(data); return p
a = w('a.txt', b'hello world\nfoo bar baz\n')
b = w('b.txt', b'one\n\ntwo  three\nlongest line here')
e = w('e.txt', b'')
u = w('u.bin', b'caf\xe9 x\n')
def run(args, inp=None):
    return subprocess.run([sys.executable, 'mini_wc.py'] + args, capture_output=True, input=inp, cwd=os.getcwd())
def f(*n): return ' '.join(f'{x:7d}' for x in n)
def eq(a, b): assert a == b, f'{a!r} != {b!r}'
check('default', lambda: eq(run([a]).stdout.decode(), f(2, 5, 24) + f' {a}\n'))
check('-l', lambda: eq(run(['-l', a]).stdout.decode(), f(2) + f' {a}\n'))
check('-w -c order', lambda: eq(run(['-c', '-w', a]).stdout.decode(), f(5, 24) + f' {a}\n'))
check('-L', lambda: eq(run(['-L', a]).stdout.decode(), f(11) + f' {a}\n'))
check('all four', lambda: eq(run(['-L', '-c', '-w', '-l', b]).stdout.decode(), f(3, 6, 33, 17) + f' {b}\n'))
check('no trailing newline', lambda: eq(run(['-l', b]).stdout.decode(), f(3) + f' {b}\n'))
check('empty file', lambda: eq(run([e]).stdout.decode(), f(0, 0, 0) + f' {e}\n'))
check('stdin', lambda: eq(run([], b'a b\nc\n').stdout.decode(), f(2, 3, 6) + '\n'))
check('stdin dash', lambda: eq(run(['-w', '-'], b'a b\nc\n').stdout.decode(), f(3) + '\n'))
def multi():
    r = run([a, b]); eq(r.stdout.decode(), f(2, 5, 24) + f' {a}\n' + f(3, 6, 33) + f' {b}\n' + f(5, 11, 57) + ' total\n')
check('multi total', multi)
def multiL():
    r = run(['-L', a, b]); eq(r.stdout.decode(), f(11) + f' {a}\n' + f(17) + f' {b}\n' + f(17) + ' total\n')
check('multi -L max', multiL)
def missing():
    r = run([a, '/nonexistent/zzz', b]); eq(r.returncode, 1)
    assert b'mini_wc.py: /nonexistent/zzz: No such file or directory' in r.stderr, r.stderr
    eq(r.stdout.decode(), f(2, 5, 24) + f' {a}\n' + f(3, 6, 33) + f' {b}\n' + f(5, 11, 57) + ' total\n')
check('missing file', missing)
check('exit 0', lambda: eq(run([a]).returncode, 0))
check('non-utf8', lambda: eq(run(['-c', '-L', u]).stdout.decode(), f(7, 6) + f' {u}\n'))
finish()
