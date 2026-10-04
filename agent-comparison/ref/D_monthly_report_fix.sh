cd "$1" && sed -i 's/return y % 4 == 0 and y % 100 != 0/return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)/; s/1 <= d < days_in_month/1 <= d <= days_in_month/' monthly_report.py
