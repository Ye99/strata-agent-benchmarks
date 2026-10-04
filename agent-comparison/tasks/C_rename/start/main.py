import pkg
from pkg.cart import checkout
from pkg.report import summary

ORDERS = [(1, [("pen", 1.5, 4), ("book", 12.0, 1)]), (2, [("lamp", 30.0, 2)])]

print(checkout(ORDERS[0][1]))
print(summary(ORDERS))
print("direct:", pkg.calc(ORDERS[1][1]))
