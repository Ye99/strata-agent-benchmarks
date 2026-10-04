import re


def word_count(s):
    """Number of words: runs of non-whitespace characters."""
    return len(s.split(' '))


def most_common(s, n=3):
    """Top n (word, count) pairs.

    Words are lower-cased and stripped of the punctuation characters . , ! ? ; :
    at both ends; empty tokens are ignored. Highest count first; ties are
    broken alphabetically.
    """
    counts = {}
    for w in s.split():
        w = w.strip('.,!?;:')
        counts[w] = counts.get(w, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])[:n]


def avg_word_length(s):
    """Mean word length counting letters only (A-Z, a-z), rounded to 2 places.

    Tokens with no letters are ignored. Returns 0.0 when there are no words.
    """
    words = s.split()
    total = sum(len(w) for w in words)
    return round(total // len(words), 2)
