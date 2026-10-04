class Inventory:
    def __init__(self): self._i = {}
    def add(self, sku, qty, price):
        if not isinstance(qty, int) or qty <= 0: raise ValueError('qty')
        if price < 0: raise ValueError('price')
        old = self._i.get(sku, {'qty': 0})['qty']
        self._i[sku] = {'qty': old + qty, 'price': price}
    def remove(self, sku, qty):
        if sku not in self._i: raise KeyError(sku)
        if qty <= 0 or qty > self._i[sku]['qty']: raise ValueError('qty')
        self._i[sku]['qty'] -= qty
        if self._i[sku]['qty'] == 0: del self._i[sku]
    def quantity(self, sku): return self._i.get(sku, {'qty': 0})['qty']
    def total_value(self): return round(sum(v['qty'] * v['price'] for v in self._i.values()), 2)
    def low_stock(self, t): return sorted(k for k, v in self._i.items() if v['qty'] < t)
    def to_dict(self): return {'items': {k: dict(v) for k, v in self._i.items()}}
    @classmethod
    def from_dict(cls, d):
        o = cls(); o._i = {k: dict(v) for k, v in d['items'].items()}; return o
