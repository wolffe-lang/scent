#!/usr/bin/env python3
"""Three module plants; run only inside ct06's locked oracle container."""
import hashlib,json,os,pathlib,subprocess
root=pathlib.Path.cwd(); evidence=root/'notes/ct06-evidence'
assert os.environ.get('SCENT_IN_CONTAINER')=='1'
assert sorted(os.sched_getaffinity(0))==[4,5,6,7]
rows=[]
for name,path,old,new,expected in [
 ('root','src/fixed/trie.lu','trie.roots[unit] = child','trie.roots[unit] = -1','RED fixed-prefix-pattern'),
 ('history','src/reader/reader.lu','let keep_history = flags.before > 0','let keep_history = flags.before < 0','RED history-leading-context'),
 ('longest','src/re/prefilter.lu','if at < best_lo || at + size > best_hi {','if at <= best_lo {','RED exact-span-longest'),
]:
 p=root/path; original=p.read_text();assert original.count(old)==1
 planted=original.replace(old,new);p.write_text(planted)
 try:
  build=subprocess.run(['tools/build','--release'],capture_output=True,text=True)
  assert build.returncode==0,(name,build.stdout,build.stderr)
  result=subprocess.run(['python3','-I','tools/speed-test'],capture_output=True,text=True)
  log=build.stdout+build.stderr+result.stdout+result.stderr
  (evidence/f'plant-{name}.log').write_text(log)
  assert result.returncode==1 and expected in log,(name,result.returncode,log)
  rows.append({'name':name,'path':path,'before_sha256':hashlib.sha256(original.encode()).hexdigest(),'planted_sha256':hashlib.sha256(planted.encode()).hexdigest(),'replacement':[old,new],'exit':result.returncode,'expected':expected})
  print('EXPECTED RED',name,expected,flush=True)
 finally:p.write_text(original)
(evidence/'plants.json').write_text(json.dumps(rows,indent=2)+'\n')
subprocess.run(['tools/build','--release'],check=True)
subprocess.run(['python3','-I','tools/speed-test'],check=True)
print('PASS three local plants restored; SKIP=0',flush=True)
