# usage: mkcfg.py <variant>   writes cfg-<variant>.json (port 8090) from Strata's strata-iq3_s.json
import json,sys,copy
base=json.load(open('/home/ye/p/Strata/strata-iq3_s.json'))
def setarg(a,flag,val=None,drop=False):
    a=list(a)
    if flag in a:
        i=a.index(flag)
        if drop: del a[i:i+(2 if val is not None or True else 1)]; return a
        a[i+1]=str(val); return a
    if not drop: a+= [flag,str(val)]
    return a
V={}
V['base']=lambda c:None
V['spec2']=lambda c:c.update(args=setarg(c['args'],'--spec',2))
V['spec6']=lambda c:c.update(args=setarg(c['args'],'--spec',6))
V['minp03']=lambda c:c.update(args=setarg(c['args'],'--spec-min-p',0.3))
V['kvres64k']=lambda c:c.update(args=setarg(c['args'],'--kv-resident',65536))
V['kvq4']=lambda c:c.update(args=setarg(c['args'],'--kv','q4_0'))
def single(c):
    c['gpu']=[0]; c.pop('layer_split',None); c['gpus_asked']=False
V['gpu0']=single
def ctx128(c):
    c.update(args=setarg(c['args'],'--max-context',131072))
V['ctx128k']=ctx128
def mk(ctx,res=32768,kv='int8',spec=4,minp=0.5,gpu=None,conv=False,rope=None,mib=8192):
    def f(c):
        a=c['args']
        a=setarg(a,'--max-context',ctx); a=setarg(a,'--kv-resident',res); a=setarg(a,'--kv',kv); a=setarg(a,'--spec',spec); a=setarg(a,'--spec-min-p',minp)
        if rope: a=a+['--rope-scaling','yarn','--rope-scale',str(rope)]
        if conv: a=a+['--conversation-cache-mib',str(mib),'--conversation-cache-slots','4']
        c['args']=a
        if gpu is not None: c['gpu']=[gpu]; c.pop('layer_split',None); c['gpus_asked']=False
    return f
V['L256']=mk(262144)
V['L256q4']=mk(262144,kv='q4_0')
V['L256r16']=mk(262144,res=16384)
V['L256r64']=mk(262144,res=65536)
V['L256g0']=mk(262144,gpu=0)
V['L256g0c']=mk(262144,gpu=0,conv=True)
V['L384']=mk(393216,rope=1.5)
V['L256s6']=mk(262144,spec=6)
V['L256s2']=mk(262144,spec=2)
V['G16']=mk(262144,res=16384,gpu=0,conv=True,mib=16384)
V['Gq4']=mk(262144,kv='q4_0',gpu=0,conv=True,mib=16384)
V['Gs6']=mk(262144,spec=6,gpu=0,conv=True,mib=16384)
V['G384']=mk(393216,res=16384,gpu=0,conv=True,mib=16384,rope=1.5)
name=sys.argv[1]; c=copy.deepcopy(base); V[name](c)
c['port']=8090; c['log']=f'/tmp/strata-exp-{name}.log'
json.dump(c,open(f'cfg-{name}.json','w'),indent=1)
