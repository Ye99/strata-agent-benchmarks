import sys, os, tempfile, json; sys.path.insert(0, '.'); sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..'))
from harness import check, finish
from inventory import Inventory
import storage
def eq(a, b): assert a == b, f'{a!r} != {b!r}'
def raises(exc, f, *a):
    try: f(*a)
    except exc: return
    raise AssertionError(f'no {exc.__name__}')
def mk():
    i = Inventory(); i.add('b', 5, 2.5); i.add('a', 1, 10); return i
check('add+qty', lambda: eq((mk().quantity('a'), mk().quantity('b'), mk().quantity('zz')), (1, 5, 0)))
def readd():
    i = mk(); i.add('a', 4, 12.0); eq(i.quantity('a'), 5); eq(i.to_dict()['items']['a'], {'qty': 5, 'price': 12.0})
check('re-add price replaced', readd)
check('add bad qty', lambda: (raises(ValueError, mk().add, 'x', 0, 1), raises(ValueError, mk().add, 'x', -2, 1)))
check('add bad price', lambda: raises(ValueError, mk().add, 'x', 1, -0.5))
def rem():
    i = mk(); i.remove('b', 2); eq(i.quantity('b'), 3); i.remove('b', 3); eq('b' in i.to_dict()['items'], False)
check('remove', rem)
check('remove errors', lambda: (raises(KeyError, mk().remove, 'nope', 1), raises(ValueError, mk().remove, 'a', 2), raises(ValueError, mk().remove, 'a', 0)))
check('total_value', lambda: eq(mk().total_value(), 22.5))
def tv2():
    i = Inventory(); i.add('x', 3, 0.1); i.add('y', 1, 0.2); eq(i.total_value(), 0.5)
check('total rounding', tv2)
check('total empty', lambda: eq(Inventory().total_value(), 0))
check('low_stock', lambda: eq(mk().low_stock(6), ['a', 'b']) or eq(mk().low_stock(2), ['a']))
check('low_stock none', lambda: eq(mk().low_stock(1), []))
check('to_dict', lambda: eq(mk().to_dict(), {'items': {'a': {'qty': 1, 'price': 10}, 'b': {'qty': 5, 'price': 2.5}}}))
def rt():
    i = Inventory.from_dict(mk().to_dict()); eq(i.to_dict(), mk().to_dict()); eq(i.quantity('b'), 5)
check('from_dict', rt)
def sv():
    d = tempfile.mkdtemp(); p = os.path.join(d, 'inv.json'); storage.save(mk(), p)
    eq(open(p).read(), json.dumps(mk().to_dict(), indent=2, sort_keys=True))
    eq(storage.load(p).to_dict(), mk().to_dict())
check('save/load', sv)
check('load missing', lambda: eq(storage.load('/tmp/definitely/missing.json').to_dict(), {'items': {}}))
def bad():
    p = tempfile.mktemp(); open(p, 'w').write('{nope'); raises(ValueError, storage.load, p)
check('load invalid json', bad)
finish()
