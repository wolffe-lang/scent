#!/usr/bin/env python3
"""Memory gates and three-run median performance rows, no timing gate."""
import argparse,json,os,pathlib,statistics,subprocess,tempfile,time
root=pathlib.Path(__file__).resolve().parent.parent
assert os.environ.get('SCENT_IN_CONTAINER')=='1','measurements require own container'
ours=root/'target/release/scent';gnu=root/'.oracle/grep'
parser=argparse.ArgumentParser();parser.add_argument('--memory-only',action='store_true');parser.add_argument('--bin',default='target/release/scent');parser.add_argument('--output');parser.add_argument('--no-utf8',action='store_true');args=parser.parse_args();ours=root/args.bin
result={'output':'pipe drained in 64 KiB blocks; never /dev/null','host':os.uname().nodename,'affinity':sorted(os.sched_getaffinity(0)),'memory':[],'performance':[]}
assert len(result['affinity'])<=4,'run under the assigned four cores'
target=root/'target';target.mkdir(exist_ok=True)
def drain(argv):
    # GNU optimizes stdout=/dev/null into a quiet early exit, even for -c.
    # Keep descriptor 1 a pipe and drain it without retaining the output.
    with tempfile.TemporaryFile() as errors:
        child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=errors)
        total=0;head=b''
        while True:
            block=child.stdout.read(65536)
            if not block:break
            total+=len(block)
            if len(head)<128:head=(head+block)[:128]
        rc=child.wait();errors.seek(0);error=errors.read(4096)
    assert rc==0,(argv,rc,error)
    return total,head

block=(b'needle '+b'x'*56+b'\n'+b'other  '+b'z'*56+b'\n')*8192
assert len(block)==1048576
with tempfile.TemporaryDirectory(prefix='measure-',dir=target) as tmp:
 tmp=pathlib.Path(tmp);big=tmp/'2g';perf=tmp/'256m'
 for path,mib in [(big,2048),(perf,256)]:
  with open(path,'wb') as f:
   for i in range(mib):f.write(block)
 for flags in [['-F','-c'],['-F','-n']]:
  row={'argv':flags+['needle'],'bytes':big.stat().st_size}
  for name,binary in [('scent',ours),('gnu',gnu)]:
   log=tmp/(name+'-time')
   output_bytes,head=drain(['/usr/bin/time','-f','%M %e','-o',str(log),str(binary)]+flags+['needle',str(big)])
   if '-c' in flags:assert head==b'16777216\n',(name,head)
   else:assert output_bytes>1073741824,(name,output_bytes)
   rss,elapsed=map(float,log.read_text().split());row[name]={'peak_rss_kib':rss,'seconds':elapsed,'output_bytes':output_bytes}
  assert row['scent']['output_bytes']==row['gnu']['output_bytes'],row
  result['memory'].append(row);print('memory',json.dumps(row),flush=True)
 rows=[(['-F'],'needle'),(['-F','-i'],'NEEDLE'),(['-F','-c'],'needle'),(['-F','-v','-c'],'needle')]
 for syntax in ['G','E']:
  rows.extend([(['-'+syntax],'needle'),(['-'+syntax],'n[e]edle'),(['-'+syntax],r'needle\|absent' if syntax=='G' else 'needle|absent'),(['-'+syntax],r'n\(e\)\1dle' if syntax=='G' else r'n(e)\1dle'),(['-'+syntax,'-i'],'NEEDLE'),(['-'+syntax,'-v','-c'],'needle')])
 for flags,pat in ([] if args.memory_only else rows):
  row={'argv':flags+[pat],'bytes':perf.stat().st_size}
  for name,binary in [('scent',ours),('gnu',gnu)]:
   values=[]
   for i in range(3):
    start=time.perf_counter();output_bytes,head=drain([str(binary)]+flags+[pat,str(perf)]);elapsed=time.perf_counter()-start
    if '-c' in flags:assert head==b'2097152\n',(name,head)
    else:assert output_bytes==134217728,(name,output_bytes)
    values.append(elapsed);print('perf-run',name,flags,i+1,elapsed,flush=True)
   row[name]={'runs_seconds':values,'median_seconds':statistics.median(values),'output_bytes':output_bytes}
  row['ratio']=row['scent']['median_seconds']/row['gnu']['median_seconds'];result['performance'].append(row);print('performance',json.dumps(row),flush=True)
 if not args.memory_only and not args.no_utf8:
  utf8=tmp/'utf8-64m'
  payload=('é needle α '+ '中'*15+'\n').encode()
  data=payload*(65536//len(payload))
  with utf8.open('wb') as f:
   for _ in range(1024):f.write(data)
  row={'argv':['-F','-i','-c','É'],'bytes':utf8.stat().st_size,'locale':'C.UTF-8'}
  old_locale=os.environ.get('LC_ALL')
  os.environ['LC_ALL']='C.UTF-8'
  for name,binary in [('scent',ours),('gnu',gnu)]:
   values=[]
   for i in range(3):
    start=time.perf_counter();output_bytes,head=drain([str(binary),'-F','-i','-c','É',str(utf8)]);elapsed=time.perf_counter()-start
    assert int(head)==(65536//len(payload))*1024,(name,head)
    values.append(elapsed);print('utf8-perf-run',name,i+1,elapsed,flush=True)
   row[name]={'runs_seconds':values,'median_seconds':statistics.median(values),'output_bytes':output_bytes}
  if old_locale is None:os.environ.pop('LC_ALL',None)
  else:os.environ['LC_ALL']=old_locale
  row['ratio']=row['scent']['median_seconds']/row['gnu']['median_seconds'];result['performance'].append(row);print('performance',json.dumps(row),flush=True)
 if not args.memory_only:
  tree=tmp/'tree';tree.mkdir()
  payload=block[:4096]
  for i in range(10000):(tree/f'entry-{i:05d}').write_bytes(payload)
  row={'argv':['-r','-F','-c','needle'],'files':10000,'bytes':40960000}
  for name,binary in [('scent',ours),('gnu',gnu)]:
   values=[]
   for i in range(3):
    start=time.perf_counter();output_bytes,head=drain([str(binary),'-r','-F','-c','needle',str(tree)]);elapsed=time.perf_counter()-start
    expected=sum(len(str(tree/f'entry-{j:05d}').encode())+4 for j in range(10000))
    assert output_bytes==expected,(name,output_bytes,expected)
    assert b':32\n' in head,(name,head)
    values.append(elapsed);print('perf-tree-run',name,i+1,elapsed,flush=True)
   row[name]={'runs_seconds':values,'median_seconds':statistics.median(values),'output_bytes':output_bytes}
  row['ratio']=row['scent']['median_seconds']/row['gnu']['median_seconds'];result['performance'].append(row);print('performance-tree',json.dumps(row),flush=True)
(root/(args.output or ('target/memory.json' if args.memory_only else 'target/measure.json'))).write_text(json.dumps(result,indent=2)+'\n')
assert all(row['scent']['peak_rss_kib']<32768 for row in result['memory']),'memory gate: scent must peak below 32 MiB'
print('memory gate: PASS; performance recorded, not gated',flush=True)
