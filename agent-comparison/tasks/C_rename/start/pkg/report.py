from pkg import calc


def summary(orders):
    """One line per order plus a grand total (uses calc on every order)."""
    lines = []
    grand = 0
    for number, items in orders:
        value = calc(items)
        grand += value
        lines.append(f"order {number}: {value:.2f}")
    lines.append(f"grand total: {grand:.2f}")
    return "\n".join(lines)
