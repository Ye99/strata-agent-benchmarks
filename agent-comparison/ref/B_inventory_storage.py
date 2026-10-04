import json
from inventory import Inventory
def save(inv, path):
    with open(path, 'w') as f: json.dump(inv.to_dict(), f, indent=2, sort_keys=True)
def load(path):
    try: f = open(path)
    except FileNotFoundError: return Inventory()
    with f:
        try: return Inventory.from_dict(json.load(f))
        except json.JSONDecodeError as e: raise ValueError(str(e))
