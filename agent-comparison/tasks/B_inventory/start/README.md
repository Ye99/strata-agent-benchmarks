# Inventory

Implement two modules in this directory: `inventory.py` and `storage.py`.

## inventory.py

`class Inventory` (starts empty):

- `add(sku, qty, price)`: a new SKU stores qty and price. For an existing SKU the quantity is increased and the price is replaced by the new price. `qty` must be an int > 0 and `price` a number >= 0, otherwise `ValueError`.
- `remove(sku, qty)`: `KeyError` if the SKU is unknown; `ValueError` if `qty <= 0` or `qty` is more than on hand. When the quantity reaches 0 the SKU is deleted.
- `quantity(sku)`: on-hand quantity, `0` for an unknown SKU.
- `total_value()`: sum of `qty * price` over all SKUs, rounded to 2 decimals.
- `low_stock(threshold)`: list of SKUs whose quantity is below `threshold`, sorted alphabetically.
- `to_dict()`: `{"items": {sku: {"qty": int, "price": float}}}`.
- `Inventory.from_dict(d)`: classmethod, the inverse of `to_dict()`.

## storage.py

- `save(inv, path)`: write `inv.to_dict()` as JSON with `indent=2` and sorted keys.
- `load(path)`: return an `Inventory`. A missing file gives an empty `Inventory`. Invalid JSON raises `ValueError`.
