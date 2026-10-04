# Expression evaluator

Write `calc.py` exposing `evaluate(text) -> int | float`, a safe arithmetic evaluator. You must not use `eval`, `exec`, `compile` or the `ast` module: write a tokenizer and a parser.

Supported:
- numbers: integers and decimals (`3`, `2.5`, `.5`, `10.`), no exponent notation
- binary operators `+ - * / // % **` with Python's precedence and associativity (`**` is right-associative and binds tighter than a unary minus on its left: `-2 ** 2 == -4`, but `2 ** -1 == 0.5`)
- unary `+` and `-`, including stacked (`--3`, `- -3`, `+-+3`)
- parentheses, and any amount of whitespace between tokens
- semantics are Python's: `/` gives a float, `//` and `%` floor, division by zero raises `ZeroDivisionError`
- any malformed input (empty text, unbalanced parentheses, two numbers in a row, a trailing operator, an unknown character) raises `ValueError`
