import sys, subprocess; sys.path.insert(0, '.'); sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..'))
from harness import check, finish
import textstats as t
def eq(a, b): assert a == b, f'{a!r} != {b!r}'
check('wc multi', lambda: eq(t.word_count("a\tb\nc  d"), 4))
check('wc empty', lambda: eq(t.word_count(""), 0))
check('wc spaces', lambda: eq(t.word_count("  hello   world "), 2))
check('mc case', lambda: eq(t.most_common("The cat the dog. THE end!", 2), [("the", 3), ("cat", 1)]))
check('mc ties', lambda: eq(t.most_common("b a c a b", 3), [("a", 2), ("b", 2), ("c", 1)]))
check('mc n big', lambda: eq(t.most_common("x y", 10), [("x", 1), ("y", 1)]))
check('mc punct', lambda: eq(t.most_common("Go, go; GO! stop: stop.", 2), [("go", 3), ("stop", 2)]))
check('mc empty tok', lambda: eq(t.most_common("... a", 3), [("a", 1)]))
check('avg 3.5', lambda: eq(t.avg_word_length("hi there!"), 3.5))
check('avg empty', lambda: eq(t.avg_word_length(""), 0.0))
check('avg 2.0', lambda: eq(t.avg_word_length("a bb ccc"), 2.0))
check('avg punct', lambda: eq(t.avg_word_length("Hello, world!"), 5.0))
check('avg nonletter', lambda: eq(t.avg_word_length("-- ab"), 2.0))
check('avg round', lambda: eq(t.avg_word_length("abcd efg h"), 2.67))
def visible():
    r = subprocess.run([sys.executable, '-m', 'unittest', 'test_textstats'], capture_output=True, text=True); assert r.returncode == 0, r.stderr[-200:]
check('visible tests', visible)
finish()
