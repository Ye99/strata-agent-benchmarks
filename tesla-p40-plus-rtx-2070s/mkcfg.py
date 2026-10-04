import json,sys,copy
base=json.load(open('/home/ye/p/Strata/strata-iq3_s.json'))
def setarg(a,flag,val):
    a=list(a)
    if flag in a:
        i=a.index(flag); a[i+1]=str(val); return a
    return a+[flag,str(val)]
def drop(a,flag):
    a=list(a)
    if flag in a:
        i=a.index(flag); del a[i:i+2]
    return a
def mk(ctx=None,res=None,kv=None,spec=None,conv=None,slots=4,gpu=1,extra=None,exe=None,libs=None):
    def f(c):
        a=c['args']
        if exe: c['exe']=exe
        if libs: c['lib_dirs']=libs
        if ctx is not None: a=setarg(a,'--max-context',ctx)
        if res is not None: a=setarg(a,'--kv-resident',res)
        if kv is not None: a=setarg(a,'--kv',kv)
        if spec is not None: a=setarg(a,'--spec',spec)
        a=drop(a,'--conversation-cache-mib'); a=drop(a,'--conversation-cache-slots')
        if conv: a=a+['--conversation-cache-mib',str(conv),'--conversation-cache-slots',str(slots)]
        for k,v in (extra or {}).items(): a=setarg(a,k,v)
        c['args']=a; c['gpu']=gpu
    return f
V={}
# setup's own default for an 8 GB card
V['base32']=mk()
# the reference VM's chosen shape, ported to this card
V['c256']=mk(ctx=262144,res=16384,kv='int8',spec=4,conv=4096)
V['c256r4']=mk(ctx=262144,res=4096,kv='int8',spec=4,conv=4096)
V['c256r32']=mk(ctx=262144,res=32768,kv='int8',spec=4,conv=4096)
V['c256k8v4']=mk(ctx=262144,res=16384,kv='k8v4',spec=4,conv=4096)
V['c256conv16']=mk(ctx=262144,res=16384,kv='int8',spec=4,conv=16384)
V['c256nocache']=mk(ctx=262144,res=16384,kv='int8',spec=4)
V['c256s2']=mk(ctx=262144,res=16384,kv='int8',spec=2,conv=4096)
V['c256s6']=mk(ctx=262144,res=16384,kv='int8',spec=6,conv=4096)
V['c128']=mk(ctx=131072,res=16384,kv='int8',spec=4,conv=4096)
# the P40 (24 GB, x16) via the experimental sm_61 engine build
SM61='/home/ye/p/Strata/engine/strata-sm61'
LIBS12=['/usr/local/cuda-12/targets/x86_64-linux/lib','/usr/lib/x86_64-linux-gnu']
V['p40']=mk(ctx=262144,res=16384,kv='int8',spec=4,conv=4096,gpu=0,exe=SM61,libs=LIBS12)
V['p40r32']=mk(ctx=262144,res=32768,kv='int8',spec=4,conv=4096,gpu=0,exe=SM61,libs=LIBS12)
V['p40r8']=mk(ctx=262144,res=8192,kv='int8',spec=4,conv=4096,gpu=0,exe=SM61,libs=LIBS12)
V['p40nocache']=mk(ctx=262144,res=16384,kv='int8',spec=4,gpu=0,exe=SM61,libs=LIBS12)
V['p40conv16']=mk(ctx=262144,res=16384,kv='int8',spec=4,conv=16384,gpu=0,exe=SM61,libs=LIBS12)
V['p40k8v4']=mk(ctx=262144,res=16384,kv='k8v4',spec=4,conv=4096,gpu=0,exe=SM61,libs=LIBS12)
V['p40s6']=mk(ctx=262144,res=16384,kv='int8',spec=6,conv=4096,gpu=0,exe=SM61,libs=LIBS12)
V['p40s2']=mk(ctx=262144,res=16384,kv='int8',spec=2,conv=4096,gpu=0,exe=SM61,libs=LIBS12)
name=sys.argv[1]; c=copy.deepcopy(base); V[name](c)
c['port']=8090; c['log']=f'/tmp/strata-exp-{name}.log'
json.dump(c,open(f'/home/ye/p/bench-p40/cfg-{name}.json','w'),indent=1)
