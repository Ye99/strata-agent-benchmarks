import csv
import sys
from collections import defaultdict

DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap(y):
    return y % 4 == 0 and y % 100 != 0


def days_in_month(y, m):
    return 29 if m == 2 and is_leap(y) else DAYS[m - 1]


def valid(date):
    y, m, d = (int(x) for x in date.split("-"))
    return 1 <= m <= 12 and 1 <= d < days_in_month(y, m)


def main(path):
    totals = defaultdict(float)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            if not valid(row["date"]):
                print("skipping invalid date", row["date"], file=sys.stderr)
                continue
            totals[row["date"][:7]] += float(row["amount"])
    for month in sorted(totals):
        print(month, f"{totals[month]:.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
