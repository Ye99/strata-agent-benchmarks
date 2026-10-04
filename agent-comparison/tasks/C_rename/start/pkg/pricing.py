def calc(items):
    """Return the total price of items, a list of (name, price, qty)."""
    return sum(price * qty for _name, price, qty in items)


def calc_tax(amount, rate=0.2):
    """Tax on an amount, rounded to cents."""
    return round(amount * rate, 2)
