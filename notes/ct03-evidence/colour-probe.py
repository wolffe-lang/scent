#!/usr/bin/env python3
"""Retain exact passing colour bytes against the record oracle."""
import hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]);ours=pathlib.Path(sys.argv[2]).resolve();gnu=pathlib.Path(sys.argv[3]).resolve()
assert hashlib.file_digest(open(gnu,'rb'),'sha256').hexdigest()=='92b211f7a6422d621d4ab1330739b3dbe520283c5e628b848f36f8c29b9be7ea'
assert os.sched_getaffinity(0)=={12,13,14,15}
root.mkdir(parents=True,exist_ok=True);(root/'f').write_bytes(b'before\nx x\nafter\nnone\nnone\nx tail\n')
rows=[]
for name,args,env in [('default',['x'],{}),('prefix-context',['-HnbC1','x','f'],{}),('spans',['-Honb','x','f'],{'GREP_COLORS':'se=33:mt=32:ne'}),('inverse',['-vC1','x','f'],{'GREP_COLORS':'sl=41:cx=42:rv:mc=35'}),('legacy',['x'],{'GREP_COLOR':'32'})]:
 row={'name':name,'argv':['--color=always',*args],'env':env};answers=[]
 for tag,binary in [('gnu',gnu),('scent',ours)]:
  r=subprocess.run(['grep',*row['argv']],executable=binary,cwd=root,input=b'x\n',capture_output=True,env={'LC_ALL':'C','PATH':os.defpath,**env})
  answers.append((r.stdout,r.stderr,r.returncode));row[tag]={'stdout_hex':r.stdout.hex(),'stderr_hex':r.stderr.hex(),'status':r.returncode}
  for suffix,value in [('stdout',r.stdout),('stderr',r.stderr),('status',str(r.returncode).encode())]:(root/(name+'.'+tag+'.'+suffix)).write_bytes(value)
 assert answers[0]==answers[1],row
 for suffix in ['stdout','stderr','status']:subprocess.run(['cmp',str(root/(name+'.gnu.'+suffix)),str(root/(name+'.scent.'+suffix))],check=True)
 rows.append(row)
(root/'colour-witnesses.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS colour byte witnesses',len(rows))
