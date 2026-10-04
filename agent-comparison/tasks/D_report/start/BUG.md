# Bug report

`python3 monthly_report.py transactions.csv` prints monthly totals, but they come out too low:
transactions dated on the last day of a month seem to be missing, and the one from 2000-02-29 vanished too.
Genuinely impossible dates (for example 2023-02-29) must still be skipped with a message on stderr.
