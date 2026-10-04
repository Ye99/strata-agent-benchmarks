# mini_wc

Write `mini_wc.py`, a small `wc` clone: `python3 mini_wc.py [-l] [-w] [-c] [-L] [FILE ...]`

- `-l` newline count, `-w` words (runs of non-whitespace), `-c` bytes, `-L` length in characters of the longest line (excluding the newline).
- With no flags it behaves like `-l -w -c`. The columns are always printed in the order l, w, c, L no matter the order of the flags.
- Every number is right-aligned in a field of width 7, fields are joined with one space. For a file, a space and the file name follow the numbers. With no FILE (or `-` as a file) the input is stdin and no name is printed.
- With more than one FILE a final line with the totals is printed, named `total` (for `-L` the total is the maximum, not the sum).
- A file that cannot be opened: print `mini_wc.py: NAME: No such file or directory` to stderr, continue with the other files (it is not counted in the total) and exit with status 1 at the end. Otherwise exit status 0.
- Files may contain non-UTF-8 bytes: count bytes for `-c`, and decode with `errors="replace"` for `-L`.
