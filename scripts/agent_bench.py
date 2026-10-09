"""Agent-shaped benchmark for a Strata server (OpenAI /v1/chat/completions, streaming).

Usage: agent_bench.py <host> <depth,depth,...> <out.json>   (env REPS: repetitions per depth, default 2)

The context is real source code from the Strata repo, up to about `depth` tokens (code drafts well; random words
do not). For each depth, turn 1 is cold. Turn 2 resends the same prefix plus the assistant's reply and a new
question, after an unrelated short title request; this is the Claude Code pattern, so the server's prompt cache
should make turn 2's first token fast.
Reports cold prefill tok/s, turn-2 TTFT, decode tok/s, and draft acceptance from the /metrics totals."""
import json,sys,time,random,string,glob,urllib.request,os
host,depths,out=sys.argv[1],[int(x) for x in sys.argv[2].split(',')],sys.argv[3]
reps=int(os.environ.get('REPS','2'))
files=sorted(glob.glob('~/p/Strata/**/*.py',recursive=True)+glob.glob('~/p/Strata/src/**/*.cpp',recursive=True)+glob.glob('~/p/Strata/src/**/*.cu',recursive=True)+glob.glob('~/p/Strata/docs/*.md'))
corpus=''
for f in files:
    try: corpus+=f'\n### FILE {f}\n'+open(f,errors='ignore').read()
    except: pass
def chat(msgs,max_tokens=300,effort='none'):
    body=json.dumps({'model':'strata','messages':msgs,'max_tokens':max_tokens,'temperature':0,'stream':True,
      'stream_options':{'include_usage':True},'reasoning_effort':effort}).encode()
    req=urllib.request.Request(host+'/v1/chat/completions',body,{'Content-Type':'application/json'})
    t0=time.perf_counter(); ttft=None; txt=''; usage=None
    with urllib.request.urlopen(req,timeout=1800) as r:
        for line in r:
            line=line.decode().strip()
            if not line.startswith('data:') or line.endswith('[DONE]'): continue
            o=json.loads(line[5:])
            if o.get('usage'): usage=o['usage']
            for ch in o.get('choices',[]):
                d=ch.get('delta',{}); s=(d.get('content') or '')+(d.get('reasoning_content') or '')+(d.get('reasoning') or '')
                if s:
                    if ttft is None: ttft=time.perf_counter()-t0
                    txt+=s
    return dict(ttft=ttft,wall=time.perf_counter()-t0,text=txt,usage=usage)
def totals():
    try: return json.load(urllib.request.urlopen(host+'/metrics',timeout=10)).get('totals',{})
    except Exception as e: return {}
res=[]
for depth in depths:
    for rep in range(reps):
        nonce=''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        # ~3.2 chars/token for code
        rs=random.Random(depth*100+rep); L=int(depth*2.7); body=corpus[rs.randint(0,max(0,len(corpus)-L)):][:L]
        word=''.join(rs.choice(string.ascii_lowercase) for _ in range(6))+'-'+str(rs.randint(100,999)); k=int(len(body)*0.4); body=body[:k]+f'\n# NOTE: the deployment passphrase is {word}\n'+body[k:]
        sys_msg=f'Session {nonce}. You are a coding agent. Source context follows.\n{body}'
        m=[{'role':'system','content':sys_msg},{'role':'user','content':'First, what is the deployment passphrase noted in the context? Then list three functions or classes you see in the context and say in one line what each does.'}]
        t0=totals(); a=chat(m); t1=totals()
        pt=a['usage']['prompt_tokens']; ct=a['usage']['completion_tokens']
        chat([{'role':'system','content':'You write very short titles.'},{'role':'user','content':'Title for: fixing a flaky test'}],max_tokens=16)
        m2=m+[{'role':'assistant','content':a['text']},{'role':'user','content':'Now name one possible bug or edge case in the first one you listed, in two sentences.'}]
        b=chat(m2); t2=totals()
        def dacc(x,y):
            o=y.get('drafts_offered',0)-x.get('drafts_offered',0); k=y.get('drafts_accepted',0)-x.get('drafts_accepted',0)
            return k/o if o else None
        r=dict(depth=depth,rep=rep,prompt_tokens=pt,t1_ttft=a['ttft'],t1_prefill_tps=pt/a['ttft'],
               t1_decode_tps=ct/(a['wall']-a['ttft']) if a['wall']>a['ttft'] else None,t1_ct=ct,needle_ok=word in a['text'],t1_accept=dacc(t0,t1),
               t2_prompt_tokens=b['usage']['prompt_tokens'],t2_ttft=b['ttft'],t2_cached=(b['usage'].get('prompt_tokens_details') or {}).get('cached_tokens'),
               t2_decode_tps=b['usage']['completion_tokens']/(b['wall']-b['ttft']) if b['wall']>b['ttft'] else None,t2_accept=dacc(t1,t2))
        res.append(r); print(json.dumps({k:(round(v,2) if isinstance(v,float) else v) for k,v in r.items()}),flush=True)
json.dump(res,open(out,'w'),indent=1)
