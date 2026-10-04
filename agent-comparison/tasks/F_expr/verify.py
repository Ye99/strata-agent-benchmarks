import sys, re; sys.path.insert(0, '.'); sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..'))
from harness import check, finish
import calc
src = open('calc.py').read()
check('no eval/ast', lambda: (_ for _ in ()).throw(AssertionError('uses eval/ast')) if re.search(r'\beval\s*\(|\bexec\s*\(|(?<![.\w])compile\s*\(|import\s+ast|from\s+ast', src) else None)
CASES = ['1+2', '2*3+4', '2+3*4', '(2+3)*4', '10/4', '10//4', '-7//2', '7%3', '-7%3', '2**3**2', '-2**2', '2**-1', '--3', '- -3', '+-+3', ' 1 +  2 ', '.5+.5', '10.', '3.25*4', '2*(3+(4-1))*2', '100/10/5', '2-3-4', '8/2*3', '2**0.5*2**0.5', '(((7)))', '-(2+3)', '-(-(4))', '1+-2', '5%3*2', '2*-3', '10-2**3', '1e3' if False else '12345678901234567890*10', '7//-2', '-8%3', '0.1+0.2', '3*(2+1)**2', '4/2', '2**10', '1 - -1']
for c in CASES:
    check(c, lambda c=c: (lambda got, exp: None if (got == exp and type(got) is type(exp)) or (isinstance(exp, float) and abs(got - exp) < 1e-12) else (_ for _ in ()).throw(AssertionError(f'{got!r} != {exp!r}')))(calc.evaluate(c), eval(c)))
def errs(text, exc):
    def f():
        try: calc.evaluate(text)
        except exc: return
        except BaseException as e: raise AssertionError(f'{type(e).__name__}')
        raise AssertionError('no error')
    return f
for t in ['', '   ', '(1+2', '1+2)', '1 2', '1+', '*3', '1+*2', '2 $ 3', '()', '1..2', 'abc', '1+(2*)']:
    check('ValueError ' + repr(t), errs(t, ValueError))
for t in ['1/0', '1//0', '5%0', '1/(2-2)']:
    check('ZeroDiv ' + t, errs(t, ZeroDivisionError))
finish()
