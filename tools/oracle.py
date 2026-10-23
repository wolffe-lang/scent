#!/usr/bin/env python3
"""Byte oracle: no expected-output snapshots to edit around a disagreement."""
import argparse, base64, fnmatch, hashlib, json, os, pathlib, shutil, subprocess, tempfile, threading, time, tomllib, sys, select
ROOT=pathlib.Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--only');p.add_argument('--field',action='store_true');p.add_argument('--bin',default='target/native/scent');p.add_argument('--cases',default='tests/cases');a=p.parse_args()
pin=tomllib.loads((ROOT/'scent-oracle.toml').read_text())['oracle']
ours=(ROOT/a.bin).resolve()
reference=pathlib.Path(shutil.which('ggrep') or shutil.which('grep') or '') if a.field else ROOT/'.oracle/grep'
def require(ok, message):
    if not ok: raise SystemExit('oracle: REFUSED: '+message)
require(ours.is_file(),'scent binary absent: '+str(ours))
require(reference.is_file(),'reference absent')
if not a.field:
    require(os.environ.get('SCENT_IN_CONTAINER')=='1','oracle must run in own pinned container')
    require(hashlib.file_digest(open(reference,'rb'),'sha256').hexdigest()==pin['binary_sha256'],'oracle binary digest')
    require(subprocess.check_output(['ldd','--version']).splitlines()[0].decode()==pin['glibc_line'],'libc identity')
    require(subprocess.check_output([str(reference),'--version']).splitlines()[0].decode()==pin['version_line'],'version identity')
print('oracle:', 'FIELD (non-gating)' if a.field else 'RECORD', str(reference),flush=True)
stage=ROOT/'target/oracle';stage.mkdir(parents=True,exist_ok=True)
def data(spec):
    if isinstance(spec,str):return spec.encode()
    if 'parts' in spec:return b''.join(data(part) for part in spec['parts'])
    if 'base64' in spec:return base64.b64decode(spec['base64'])
    return spec.get('text','').encode()*spec.get('repeat',1)
def prepare(work, c):
    for name,spec in c.get('files',{}).items():
        dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True)
        if spec.get('kind')=='missing':continue
        if spec.get('kind')=='directory':dest.mkdir(exist_ok=True)
        elif spec.get('kind')=='fifo':os.mkfifo(dest)
        else:dest.write_bytes(data(spec))
        dest.chmod(spec.get('mode',0o644) if spec.get('kind')!='directory' else spec.get('mode',0o755))
def launch(binary, c, work, bindir):
    env={'PATH':str(bindir)+':'+os.defpath,'LC_ALL':'C','HOME':str(work),'TERM':'dumb'};env.update(c.get('env',{}))
    stdin=data(c.get('stdin',''))
    args=['grep']+c['argv']
    source=None
    if c.get('stdin_file'):
        source=open(work/c['stdin_file'],'rb');source.seek(c.get('stdin_seek',0));input_arg=None
    else:input_arg=stdin
    output=None;pre=None
    if c.get('stdout')=='full':output=open('/dev/full','wb')
    if c.get('stdout')=='input':output=open(work/c['stdout_file'],'ab')
    if c.get('stdout')=='closed':
        def pre():os.close(1)
    if c.get('nonroot') and os.getuid()==0:
        previous=pre
        def pre():
            if previous:previous()
            os.setgid(65534);os.setuid(65534)
    writers=[]
    for name,spec in c.get('files',{}).items():
        if spec.get('kind')=='fifo':
            def write_fifo(dest=work/name,payload=data(spec)):
                try:
                    with open(dest,'wb',buffering=0) as f:f.write(payload)
                except (BrokenPipeError,OSError):pass
            t=threading.Thread(target=write_fifo,daemon=True);t.start();writers.append(t)
    try:
        if c.get('stream'):
            child=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=work,env=env)
            child.stdin.write(b'x\n');child.stdin.flush()
            ready,_,_=select.select([child.stdout],[],[],3)
            if not ready:
                child.kill();child.communicate();return b'',b'HARNESS live-line TIMEOUT',124,b''
            first=os.read(child.stdout.fileno(),65536)
            child.stdin.write(b'none\nx\n');child.stdin.close();child.stdin=None
            rest,err=child.communicate(timeout=3)
            return first+rest,err,child.returncode,b'live-before-EOF' if first==b'x\n' else b'bad-first-line'
        r=subprocess.run(args,input=input_arg,stdin=source,stdout=output or subprocess.PIPE,stderr=subprocess.PIPE,cwd=work,env=env,preexec_fn=pre,timeout=c.get('timeout',10))
        rest=source.read() if source else b''
        return r.stdout or b'',r.stderr,r.returncode,rest
    except subprocess.TimeoutExpired:return b'',b'HARNESS TIMEOUT',124,b''
    finally:
        if source:source.close()
        if output:output.close()
        for t in writers:t.join(timeout=0.1)
counts={'agree':0,'differ':0,'not-yet':0,'argv0-diagnostic':0,'argv0-usage':0,'argv-bytes':0,'field-unavailable':0,'terminator-pattern':0};seen=0
for file in sorted((ROOT/a.cases).glob('*.jsonl')):
 for raw in file.read_text().splitlines():
    c=json.loads(raw);name=c['name']
    if a.only and a.only not in name and not fnmatch.fnmatch(name,a.only):continue
    seen+=1
    if a.field and sys.platform != 'linux' and (c.get('nonroot') or c.get('stdout')=='full' or any(f.get('kind')=='fifo' for f in c.get('files',{}).values())):
        counts['field-unavailable']+=1;print('FIELD unavailable',name,'Linux fixture only',flush=True);continue
    if c.get('not_yet'):
        why=c['not_yet'];category=c.get('column','not-yet')
        if 'refusal' in c:
            with tempfile.TemporaryDirectory(prefix='not-yet-',dir=stage) as tmp:
                work=pathlib.Path(tmp);bindir=work/'bin';bindir.mkdir();(bindir/'grep').symlink_to(ours)
                prepare(work,c)
                answer=launch(ours,c,work,bindir)
                require(answer[2]==2 and c['refusal'].encode() in answer[1],name+' did not refuse by name')
                (bindir/'grep').unlink();(bindir/'grep').symlink_to(reference)
                measured=launch(reference,c,work,bindir)
                print('not-yet GNU',name,'status',measured[2],'stdout',repr(measured[0][:240]),'stderr',repr(measured[1][:240]),flush=True)
                record=stage/'not-yet'/name;record.mkdir(parents=True,exist_ok=True)
                for tag,result in [('gnu',measured),('scent',answer)]:
                    for suffix,value in zip(['stdout','stderr','status','stdin-rest'],result):
                        (record/(tag+'.'+suffix)).write_bytes(str(value).encode() if isinstance(value,int) else value)
                (record/'case.json').write_text(json.dumps(c,indent=2)+'\n')
        counts['not-yet']+=1
        if category!='not-yet':counts[category]+=1
        print('not-yet',name,why,flush=True);continue
    with tempfile.TemporaryDirectory(prefix='case-',dir=stage) as tmp:
        top=pathlib.Path(tmp);top.chmod(0o755)
        results=[]
        for tag,binary in [('gnu',reference),('scent',ours)]:
            work=top/tag;work.mkdir(mode=0o755)
            bindir=work/'bin';bindir.mkdir();(bindir/'grep').symlink_to(binary)
            prepare(work,c)
            results.append(launch(binary,c,work,bindir))
        g,s=results
        shape=c.get('shape')
        # The prose exception follows the action, including unique prefixes.
        if g[0].startswith(b'Usage: grep ') and s[0].startswith(b'Usage: scent '):shape='help'
        if g[0].startswith(b'grep (GNU grep) ') and s[0].startswith(b'scent '):shape='version'
        if shape:
            same=g[2]==s[2] and bool(g[0])==bool(s[0]) and bool(g[1])==bool(s[1])
            if shape=='version':same= same and s[0].startswith(b'scent ')
            if shape=='help':same= same and s[0].startswith(b'Usage: scent ')
        else:
            same=True
            for i,field in enumerate(['stdout','stderr','status','stdin-rest']):
                paths=[]
                for tag,result in [('gnu',g),('scent',s)]:
                    dest=top/(tag+'.'+field);value=result[i]
                    dest.write_bytes(str(value).encode() if isinstance(value,int) else value);paths.append(str(dest))
                compared=subprocess.run(['cmp','-s']+paths).returncode
                require(compared in (0,1),'cmp could not compare '+name+' '+field)
                same= same and compared==0
        if same:counts['agree']+=1
        else:
            counts['differ']+=1
            evidence=stage/name;evidence.mkdir(exist_ok=True)
            for tag,result in [('gnu',g),('scent',s)]:
                for suffix,value in zip(['stdout','stderr','status','stdin-rest'],result):
                    (evidence/(tag+'.'+suffix)).write_bytes(str(value).encode() if isinstance(value,int) else value)
            (evidence/'case.json').write_text(json.dumps(c,indent=2)+'\n')
            print('DIFFER',name,'GNU',repr(g),'scent',repr(s),flush=True)
    if seen%50==0:print('progress',seen,counts,flush=True)
require(seen>0,'no cases selected')
print('{agree} agree / {differ} differ / {not-yet} not-yet'.format(**counts),flush=True)
print('not-yet columns: argv0-diagnostic={argv0-diagnostic} argv0-usage={argv0-usage} argv-bytes={argv-bytes} terminator-pattern={terminator-pattern}'.format(**counts),flush=True)
(stage/'summary.json').write_text(json.dumps(counts,sort_keys=True)+'\n')
raise SystemExit(0 if a.field or counts['differ']==0 else 1)
