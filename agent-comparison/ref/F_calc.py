import re
TOK = re.compile(r'\s*(?:(\d+\.\d*|\.\d+|\d+)|(\*\*|//|[-+*/%()]))')
def tokenize(s):
    pos, out = 0, []
    s = s.rstrip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m: raise ValueError('bad char')
        out.append(('n', m.group(1)) if m.group(1) else ('o', m.group(2))); pos = m.end()
    return out
def evaluate(text):
    toks = tokenize(text); i = [0]
    def peek(): return toks[i[0]] if i[0] < len(toks) else (None, None)
    def eat(): t = toks[i[0]]; i[0] += 1; return t
    def expr():
        v = term()
        while peek() in (('o', '+'), ('o', '-')):
            op = eat()[1]; r = term(); v = v + r if op == '+' else v - r
        return v
    def term():
        v = unary()
        while peek()[0] == 'o' and peek()[1] in ('*', '/', '//', '%'):
            op = eat()[1]; r = unary()
            v = v * r if op == '*' else v / r if op == '/' else v // r if op == '//' else v % r
        return v
    def unary():
        if peek() == ('o', '-'): eat(); return -unary()
        if peek() == ('o', '+'): eat(); return +unary()
        return power()
    def power():
        b = atom()
        if peek() == ('o', '**'): eat(); return b ** unary()
        return b
    def atom():
        k, v = peek()
        if k == 'n': eat(); return float(v) if '.' in v else int(v)
        if (k, v) == ('o', '('):
            eat(); r = expr()
            if peek() != ('o', ')'): raise ValueError('paren')
            eat(); return r
        raise ValueError('unexpected')
    r = expr()
    if i[0] != len(toks): raise ValueError('trailing')
    return r
