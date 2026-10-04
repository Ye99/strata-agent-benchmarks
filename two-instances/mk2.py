import json,sys,os
# usage: mk2.py <name> <gpu> <port> <pool_workers|0> ; env MMAP=1 for --mmap-experts, CMIB for conv cache MiB
name,gpu,port,pw=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
c=json.load(open('~/p/Strata/strata-iq3_s.json'))
a=c['args']
a[a.index('--conversation-cache-mib')+1]=os.environ.get('CMIB','16384')
if os.environ.get('MMAP'): a+=['--mmap-experts']
if pw: a+=['--pool-workers',str(pw)]
c['gpu']=[gpu]; c['port']=port; c['log']=f'/tmp/strata-exp-{name}.log'; c['host']='127.0.0.1'
json.dump(c,open(f'cfg-{name}.json','w'),indent=1)
