import sys
args = sys.argv[1:]; flags = {'-l', '-w', '-c', '-L'}
sel = {a for a in args if a in flags}; files = [a for a in args if a not in flags]
if not sel: sel = {'-l', '-w', '-c'}
def count(data):
    text = data.decode('utf-8', errors='replace')
    lines = text.split('\n')
    return {'-l': data.count(b'\n'), '-w': len(text.split()), '-c': len(data), '-L': max((len(x) for x in lines), default=0)}
def fmt(c, name=None):
    s = ' '.join(f'{c[k]:7d}' for k in ['-l', '-w', '-c', '-L'] if k in sel)
    return s + (' ' + name if name else '')
if not files or files == ['-']:
    print(fmt(count(sys.stdin.buffer.read()))); sys.exit(0)
tot = {'-l': 0, '-w': 0, '-c': 0, '-L': 0}; rc = 0; n = 0
for fn in files:
    try: data = open(fn, 'rb').read()
    except OSError:
        print(f'mini_wc.py: {fn}: No such file or directory', file=sys.stderr); rc = 1; continue
    c = count(data); n += 1
    for k in tot: tot[k] = max(tot[k], c[k]) if k == '-L' else tot[k] + c[k]
    print(fmt(c, fn))
if len(files) > 1: print(fmt(tot, 'total'))
sys.exit(rc)
