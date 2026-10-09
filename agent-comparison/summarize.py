# Prints per-task and per-backend summaries of results-strata.jsonl and results-vllm.jsonl.
import json,glob,statistics as st,collections
R={}
for lab in ['strata','vllm']:
    try: R[lab]=[json.loads(l) for l in open(f'results-{lab}.jsonl')]
    except FileNotFoundError: R[lab]=[]
tasks=sorted({r['task'] for l in R.values() for r in l})
f=lambda x:'-' if x is None else (f'{x:.0f}' if isinstance(x,(int,float)) else x)
print(f"{'task':12} | " + " | ".join(f"{l:>34}" for l in R))
print(f"{'':12} | " + " | ".join(f"{'ok  partial  turns(avg)  wall s':>34}" for _ in R))
for t in tasks:
    row=[]
    for l in R:
        rs=[r for r in R[l] if r['task']==t]
        if not rs: row.append(f"{'-':>34}"); continue
        ok=sum(r['ok'] for r in rs); part=st.mean((r['passed'] or 0)/(r['total'] or 1) for r in rs)
        tu=[r['turns'] for r in rs if r['turns']]; w=st.mean(r['wall_s'] for r in rs)
        row.append(f"{ok}/{len(rs)}   {part*100:5.0f}%   {st.mean(tu) if tu else float('nan'):6.1f}   {w:8.0f}".rjust(34))
    print(f"{t:12} | "+" | ".join(row))
print()
for l,rs in R.items():
    if not rs: continue
    tu=[r['turns'] for r in rs if r['turns']]
    print(f"{l}: runs={len(rs)} full-pass={sum(r['ok'] for r in rs)}/{len(rs)} partial={st.mean((r['passed'] or 0)/(r['total'] or 1) for r in rs)*100:.0f}% turns avg={st.mean(tu):.1f} median={st.median(tu)} wall avg={st.mean(r['wall_s'] for r in rs):.0f}s total={sum(r['wall_s'] for r in rs)/60:.0f} min out_tokens avg={st.mean(r['out_tokens'] or 0 for r in rs):.0f}")
