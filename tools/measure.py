#!/usr/bin/env python3
"""Memory gates and three-run median performance rows, no timing gate."""
import json,os,pathlib,statistics,subprocess,tempfile,time
root=pathlib.Path(__file__).resolve().parent.parent
assert os.environ.get('SCENT_IN_CONTAINER')=='1','measurements require own container'
ours=root/'target/release/scent';gnu=root/'.oracle/grep'
result={'host':os.uname().nodename,'affinity':sorted(os.sched_getaffinity(0)),'memory':[],'performance':[]}
assert len(result['affinity'])<=4,'run under the assigned four cores'
target=root/'target';target.mkdir(exist_ok=True)
block=(b'needle '+b'x'*56+b'\n'+b'other  '+b'z'*56+b'\n')*8192
assert len(block)==1048576
with tempfile.TemporaryDirectory(prefix='measure-',dir=target) as tmp:
 tmp=pathlib.Path(tmp);big=tmp/'2g';perf=tmp/'256m'
 for path,mib in [(big,2048),(perf,256)]:
  with open(path,'wb') as f:
   for i in range(mib):f.write(block)
 with open(os.devnull,'wb') as sink:
  for flags in [['-F','-c'],['-F','-n']]:
   row={'argv':flags+['needle'],'bytes':big.stat().st_size}
   for name,binary in [('scent',ours),('gnu',gnu)]:
    log=tmp/(name+'-time')
    run=subprocess.run(['/usr/bin/time','-f','%M %e','-o',str(log),str(binary)]+flags+['needle',str(big)],stdout=sink,stderr=subprocess.PIPE)
    assert run.returncode==0,(row,run.returncode,run.stderr)
    rss,elapsed=map(float,log.read_text().split());row[name]={'peak_rss_kib':rss,'seconds':elapsed}
   result['memory'].append(row);print('memory',json.dumps(row),flush=True)
  for flags,pat in [(['-F'],'needle'),(['-F','-i'],'NEEDLE'),(['-F','-c'],'needle'),(['-F','-v','-c'],'needle')]:
   row={'argv':flags+[pat],'bytes':perf.stat().st_size}
   for name,binary in [('scent',ours),('gnu',gnu)]:
    values=[]
    for i in range(3):
     start=time.perf_counter();r=subprocess.run([str(binary)]+flags+[pat,str(perf)],stdout=sink,stderr=subprocess.PIPE);elapsed=time.perf_counter()-start
     assert r.returncode==0,(row,r.returncode,r.stderr)
     values.append(elapsed);print('perf-run',name,flags,i+1,elapsed,flush=True)
    row[name]={'runs_seconds':values,'median_seconds':statistics.median(values)}
   row['ratio']=row['scent']['median_seconds']/row['gnu']['median_seconds'];result['performance'].append(row);print('performance',json.dumps(row),flush=True)
(root/'target/measure.json').write_text(json.dumps(result,indent=2)+'\n')
assert all(row['scent']['peak_rss_kib']<32768 for row in result['memory']),'memory gate: scent must peak below 32 MiB'
print('memory gate: PASS; performance recorded, not gated',flush=True)
