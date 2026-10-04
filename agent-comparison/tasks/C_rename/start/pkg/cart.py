from .pricing import calc, calc_tax


def checkout(items):
    subtotal = calc(items)
    tax = calc_tax(subtotal)
    return {"subtotal": subtotal, "tax": tax, "total": round(subtotal + tax, 2)}
