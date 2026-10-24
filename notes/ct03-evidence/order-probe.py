#!/usr/bin/env python3
"""Same-fixture raw std/GNU directory-order measurement; no sorting."""
import hashlib,json,os,pathlib,random,subprocess,sys
root=pathlib.Path(sys.argv[1]);listing=sys.argv[2];oracle=sys.argv[3]
assert hashlib.file_digest(open(oracle,'rb'),'sha256').hexdigest()=='92b211f7a6422d621d4ab1330739b3dbe520283c5e628b848f36f8c29b9be7ea'
assert os.sched_getaffinity(0)=={12,13,14,15}
root.mkdir(parents=True,exist_ok=True);results=[]
for seed in range(3):
    directory=root/str(seed);directory.mkdir(exist_ok=True)
    names=[f'entry-{i:04d}' for i in range(400)];random.Random(seed).shuffle(names)
    for name in names:(directory/name).write_bytes(b'x\n')
    raw=subprocess.check_output([listing,str(directory)])
    g=subprocess.run([oracle,'-rl','x','.'],cwd=directory,capture_output=True)
    assert g.returncode==0 and not g.stderr
    expected=b''.join(x.removeprefix(b'./')+b'\n' for x in g.stdout.splitlines())
    (root/f'{seed}.std').write_bytes(raw);(root/f'{seed}.gnu').write_bytes(expected)
    subprocess.run(['cmp',str(root/f'{seed}.std'),str(root/f'{seed}.gnu')],check=True)
    results.append(dict(seed=seed,entries=400,equal=True,raw_is_sorted=raw.splitlines()==sorted(raw.splitlines()),sha256=hashlib.sha256(raw).hexdigest()))
print(json.dumps(results,indent=2));(root/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
