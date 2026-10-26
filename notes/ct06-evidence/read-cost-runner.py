#!/usr/bin/env python3
"""Isolate read/allocation/copy and delimiter scanning; never a scent binding."""
import hashlib,json,os,pathlib,statistics,subprocess,time
root=pathlib.Path.cwd()
assert os.environ.get('SCENT_IN_CONTAINER')=='1' and sorted(os.sched_getaffinity(0))==[4,5,6,7]
path=root/'target/ct05-corpus/text'; data=path.read_bytes(); size=len(data);lines=data.count(b'\n');del data
commands={f'{name}-{mode}':[str(root/binary),mode,str(path)] for name,binary in [('chunk','target/read-probe'),('sc72-into','target/read-into-probe'),('reused-c','target/read-reference')] for mode in ['read','scan']}
values={name:[] for name in commands}
for turn in range(12):
 for name in (list(commands) if turn%2==0 else list(reversed(commands))):
  start=time.perf_counter();p=subprocess.run(commands[name],capture_output=True,check=True);elapsed=time.perf_counter()-start
  assert not p.stderr and p.stdout==f'{size} {lines if name.endswith("-scan") else 0}\n'.encode(),(name,p.stdout,p.stderr)
  if turn:values[name].append(elapsed)
 print('read-cost pair',turn,flush=True)
calls=subprocess.check_output([str(root/'target/read-probe'),'calls',str(path)],text=True).split()
assert int(calls[0])==size
result={'read_calls_including_eof':int(calls[1]),'region_allocated_bytes':int(calls[2]),'binaries':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['target/read-probe','target/read-into-probe','target/read-reference']},'bytes':size,'lines':lines,'chunk_bytes':98304,'affinity':[4,5,6,7],'std_measurement_rev':'78b9d3cbc41d51db44d18c40b6694403644d1c83','repeats':11,'warmups':1,'seconds':values,'median':{k:statistics.median(v) for k,v in values.items()},'interpretation':'C is an original black-box API control, not code linked to scent; deltas are measured opportunities, not promises for a future std implementation.'}
(root/'notes/ct06-evidence/read-cost.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
