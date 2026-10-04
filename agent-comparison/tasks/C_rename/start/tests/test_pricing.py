import unittest
from pkg import calc, calc_tax
from pkg.cart import checkout


class PricingTests(unittest.TestCase):
    def test_calc(self):
        self.assertEqual(calc([("a", 2.0, 3)]), 6.0)

    def test_calc_empty(self):
        self.assertEqual(calc([]), 0)

    def test_calc_tax(self):
        self.assertEqual(calc_tax(10), 2.0)

    def test_checkout(self):
        self.assertEqual(checkout([("a", 10.0, 1)])["total"], 12.0)


if __name__ == "__main__":
    unittest.main()
