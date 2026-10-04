import re
def word_count(s): return len(s.split())
def most_common(s, n=3):
    c = {}
    for w in s.split():
        w = w.lower().strip('.,!?;:')
        if w: c[w] = c.get(w, 0) + 1
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
def avg_word_length(s):
    ws = [re.sub(r'[^A-Za-z]', '', w) for w in s.split()]; ws = [w for w in ws if w]
    return round(sum(map(len, ws)) / len(ws), 2) if ws else 0.0
