#!/usr/bin/env python3
"""Reproduce ct03 STOPs inside the lane container, never on the host."""
import hashlib,json,os,pathlib,socket,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();root.mkdir(parents=True,exist_ok=True)
candidate=pathlib.Path(sys.argv[2]).resolve();oracle=pathlib.Path(sys.argv[3]).resolve()
assert hashlib.file_digest(open(oracle,'rb'),'sha256').hexdigest()=='92b211f7a6422d621d4ab1330739b3dbe520283c5e628b848f36f8c29b9be7ea'
assert subprocess.check_output(['ldd','--version']).splitlines()[0]==b'ldd (Ubuntu GLIBC 2.39-0ubuntu8.9) 2.39'
assert subprocess.check_output([oracle,'--version']).splitlines()[0]==b'grep (GNU grep) 3.12'
assert os.sched_getaffinity(0)=={12,13,14,15}
tree=root/'tree';tree.mkdir(exist_ok=True)
fd=os.open(os.fsencode(tree)+b'/\xff',os.O_CREAT|os.O_TRUNC|os.O_WRONLY,0o644)
os.write(fd,b'x\n');os.close(fd)
sock=root/'socket'
if not sock.exists():
    handle=socket.socket(socket.AF_UNIX);handle.bind(str(sock));handle.close()
fifo=root/'fifo'
if not fifo.exists():os.mkfifo(fifo)
normal=root/'normal';normal.mkdir(exist_ok=True)
nsock=normal/'socket'
if not nsock.exists():
    handle=socket.socket(socket.AF_UNIX);handle.bind(str(nsock));handle.close()
results=[]
for name,args in [('socket-default',['x','socket']),('socket-skip',['-Dskip','x','socket']),('socket-read',['-Dread','x','socket']),('socket-recursive-explicit',['-r','-Dskip','x','socket']),('socket-recursive-walked',['-r','-Dskip','x','normal']),('fifo-skip',['-Dskip','x','fifo']),('raw-path',['-r','x','tree'])]:
    entry={'name':name,'argv':args}
    for tag,exe in [('gnu',oracle),('scent',candidate)]:
        r=subprocess.run(['grep',*args],executable=exe,cwd=root,env={'LC_ALL':'C','PATH':os.defpath},capture_output=True,timeout=5)
        entry[tag]={'stdout_hex':r.stdout.hex(),'stderr_hex':r.stderr.hex(),'status':r.returncode}
        for key,data in [('stdout',r.stdout),('stderr',r.stderr),('status',str(r.returncode).encode())]:(root/(name+'.'+tag+'.'+key)).write_bytes(data)
    results.append(entry)
print(json.dumps(results,indent=2))
(root/'witnesses.json').write_text(json.dumps(results,indent=2)+'\n')
