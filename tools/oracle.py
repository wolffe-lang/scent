#!/usr/bin/env python3
"""Byte oracle: no expected-output snapshots to edit around a disagreement."""
import gzip
import argparse, base64, fnmatch, hashlib, json, os, pathlib, shutil, subprocess, tempfile, threading, time, tomllib, sys, select, runpy, socket, errno, pty, termios
ROOT=pathlib.Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--only');p.add_argument('--field',action='store_true');p.add_argument('--bin',default='target/native/scent');p.add_argument('--cases',default='tests/cases');p.add_argument('--capture-reference');p.add_argument('--replay-reference');a=p.parse_args()
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
require(not (a.field and (a.capture_reference or a.replay_reference)), 'field results cannot be record snapshots')
require(not (a.capture_reference and a.replay_reference), 'capture and replay are exclusive')
replay=json.loads(gzip.decompress((ROOT/a.replay_reference).read_bytes())) if a.replay_reference else None
if replay:require(replay['oracle']==pin, 'reference capture pin drift')
captured={'oracle':pin,'cases':{}}
print('oracle:', 'FIELD (non-gating)' if a.field else ('RECORD REPLAY' if replay else 'RECORD'), str(reference),flush=True)
stage=ROOT/'target/oracle';stage.mkdir(parents=True,exist_ok=True)
def data(spec):
    if isinstance(spec,str):return spec.encode()
    if 'parts' in spec:return b''.join(data(part) for part in spec['parts'])
    if 'base64' in spec:return base64.b64decode(spec['base64'])
    return spec.get('text','').encode()*spec.get('repeat',1)
def prepare(work, c):
    fixtures=list(c.get('files',{}).items())
    fixtures += [(os.fsdecode(base64.b64decode(r['name_base64'])),r) for r in c.get('raw_names',[])]
    for name,spec in fixtures:
        dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True)
        if spec.get('kind')=='missing':continue
        if spec.get('kind')=='directory':dest.mkdir(exist_ok=True)
        elif spec.get('kind')=='fifo':os.mkfifo(dest)
        elif spec.get('kind')=='symlink':dest.symlink_to(spec['target']);continue
        elif spec.get('kind')=='socket':
            sock=socket.socket(socket.AF_UNIX);sock.bind(str(dest));sock.close()
        else:dest.write_bytes(data(spec))
        dest.chmod(spec.get('mode',0o644) if spec.get('kind')!='directory' else spec.get('mode',0o755))
def launch(binary, c, work, bindir):
    env={'PATH':str(bindir)+':'+os.defpath,'HOME':str(work),'TERM':'dumb'}
    if os.environ.get('SCENT_NO_LOCALE')!='1':env['LC_ALL']='C'
    env.update(c.get('env',{}))
    stdin=data(c.get('stdin',''))
    args=[c.get('invocation',c.get('wrapper','grep'))]+c['argv']
    executable=str(binary) if c.get('invocation') else None
    if c.get('argument_base64'):
        raw=os.fsdecode(base64.b64decode(c['argument_base64']))
        if c['argument_role']=='pattern':args[2]=raw
        else:args.append(raw)
    source=None
    if c.get('stdin_file'):
        source=open(work/c['stdin_file'],'rb');source.seek(c.get('stdin_seek',0));input_arg=None
    else:input_arg=stdin
    output=None;pre=None
    terminal=None
    if c.get('stdout_tty'):
        master,slave=pty.openpty();settings=termios.tcgetattr(slave);settings[1]=0;termios.tcsetattr(slave,termios.TCSANOW,settings)
        output=os.fdopen(slave,'wb',buffering=0);terminal=master
    if c.get('stdout')=='full':output=open('/dev/full','wb')
    if c.get('stdout')=='input':output=open(work/c['stdout_file'],'ab')
    if c.get('stdout')=='closed':
        def pre():os.close(1)
    if c.get('nonroot') and os.getuid()==0:
        previous=pre
        def pre():
            if previous:previous()
            os.setgid(65534);os.setuid(65534)
    writers=[];stop_writers=threading.Event()
    for name,spec in c.get('files',{}).items():
        if spec.get('kind')=='fifo':
            def write_fifo(dest=work/name,payload=data(spec)):
                while not stop_writers.is_set():
                    try:
                        fd=os.open(dest,os.O_WRONLY|os.O_NONBLOCK)
                        try:os.write(fd,payload)
                        finally:os.close(fd)
                        return
                    except OSError as error:
                        if error.errno!=errno.ENXIO:return
                        stop_writers.wait(.01)
            t=threading.Thread(target=write_fifo,daemon=True);t.start();writers.append(t)
    try:
        if c.get('stream'):
            child=subprocess.Popen(args,executable=executable,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=work,env=env)
            child.stdin.write(b'x\n');child.stdin.flush()
            ready,_,_=select.select([child.stdout],[],[],3)
            if not ready:
                child.kill();child.communicate();return b'',b'HARNESS live-line TIMEOUT',124,b''
            first=os.read(child.stdout.fileno(),65536)
            child.stdin.write(b'none\nx\n');child.stdin.close();child.stdin=None
            rest,err=child.communicate(timeout=3)
            return first+rest,err,child.returncode,b'live-before-EOF' if first==b'x\n' else b'bad-first-line'
        r=subprocess.run(args,executable=executable,input=input_arg,stdin=source,stdout=output or subprocess.PIPE,stderr=subprocess.PIPE,cwd=work,env=env,preexec_fn=pre,timeout=c.get('timeout',10))
        rest=source.read() if source else b''
        stdout=r.stdout or b''
        if terminal is not None:
            output.close();output=None
            while True:
                try:
                    chunk=os.read(terminal,65536)
                    if not chunk:break
                    stdout+=chunk
                except OSError as error:
                    if error.errno!=errno.EIO:raise
                    break
        return stdout,r.stderr,r.returncode,rest
    except subprocess.TimeoutExpired:return b'',b'HARNESS TIMEOUT',124,b''
    finally:
        if source:source.close()
        if output:output.close()
        if terminal is not None:os.close(terminal)
        stop_writers.set()
        for t in writers:t.join(timeout=0.1)
exact_review=runpy.run_path(str(ROOT/'tools/oracle-review.py'))['exact_review']
reviews=json.loads((ROOT/'tests/divergences.json').read_text())
reviews.update(json.loads((ROOT/'tests/m3-divergences.json').read_text()) if (ROOT/'tests/m3-divergences.json').exists() else {})
field_reviews=json.loads((ROOT/'tests/field-divergences.json').read_text()) if a.field else {}
if a.field and (ROOT/'tests/m3-field-divergences.json').exists():
    for platform, entries in json.loads((ROOT/'tests/m3-field-divergences.json').read_text()).items():
        field_reviews.setdefault(platform,{}).update(entries)
field_support=runpy.run_path(str(ROOT/'tools/oracle-field.py'))
cases=[json.loads(raw) for file in sorted((ROOT/a.cases).glob('*.jsonl')) for raw in file.read_text().splitlines()]
selected=[c for c in cases if not a.only or fnmatch.fnmatchcase(c['name'],a.only)]
capabilities={}
if a.field and any(field_support['needs_non_utf8_name'](case) for case in selected):
    capabilities['non-utf8-filename']=field_support['probe_non_utf8_name'](stage)
    print('FIELD capability',json.dumps(capabilities,sort_keys=True),flush=True)
if a.field:(stage/'field-capabilities.json').write_text(json.dumps(capabilities,indent=2)+'\n')
counts={'environment':0,'gnu-inconsistent':0,'upstream-blocked':0,'reviewed':0,'agree':0,'differ':0,'not-yet':0,'argv0-diagnostic':0,'argv0-usage':0,'argv-bytes':0,'field-unavailable':0,'terminator-pattern':0,'stale-review':0};seen=0
unavailable=[]
for c in selected:
    name=c['name']
    seen+=1
    reason=field_support['unavailable_reason'](c,capabilities) if a.field else None
    if reason:
        counts['field-unavailable']+=1;unavailable.append({'case':name,'reason':reason});print('FIELD unavailable',name,reason,flush=True);continue
    if a.field and c.get('wrapper') and not (reference.parent/c['wrapper']).is_file():
        counts['field-unavailable']+=1;unavailable.append({'case':name,'reason':'distribution wrapper absent'});print('FIELD unavailable',name,'distribution wrapper absent',flush=True);continue
    if a.field and sys.platform != 'linux' and (c.get('nonroot') or c.get('stdout')=='full' or any(f.get('kind')=='fifo' for f in c.get('files',{}).values())):
        counts['field-unavailable']+=1;unavailable.append({'case':name,'reason':'Linux fixture only'});print('FIELD unavailable',name,'Linux fixture only',flush=True);continue
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
            if tag=='gnu' and replay:
                saved=replay['cases'].get(name)
                identity=hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()
                require(saved is not None and saved['case_sha256']==identity, name+' reference capture missing or stale')
                out,err,rc,rest=saved['result']
                results.append((bytes.fromhex(out),bytes.fromhex(err),rc,bytes.fromhex(rest)))
                continue
            work=top/('shared' if c.get('shared_fixture') else tag)
            fresh=not work.exists()
            if fresh:work.mkdir(mode=0o755)
            bindir=work/'bin'
            if fresh:bindir.mkdir()
            else:(bindir/'grep').unlink()
            (bindir/'grep').symlink_to(binary)
            if c.get('wrapper'):
                wrapper=ROOT/'wrappers'/c['wrapper'] if tag=='scent' else reference.parent/c['wrapper']
                (bindir/c['wrapper']).symlink_to(wrapper)
            if fresh:prepare(work,c)
            if c.get('stdout')=='input':(work/c['stdout_file']).write_bytes(data(c['files'][c['stdout_file']]))
            results.append(launch(binary,c,work,bindir))
        g,s=results
        if a.capture_reference:
            captured['cases'][name]={'case_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest(), 'result':[g[0].hex(),g[1].hex(),g[2],g[3].hex()]}
        shape=c.get('shape')
        # The prose exception follows the action, including unique prefixes.
        if g[0].startswith(b'Usage: grep ') and s[0].startswith(b'Usage: grep '):shape='help'
        if g[0].startswith(b'grep (GNU grep) ') and s[0].startswith(b'scent '):shape='version'
        if shape:
            same=g[2]==s[2] and bool(g[0])==bool(s[0]) and g[1]==s[1]
            if shape=='version':same= same and s[0].startswith(b'scent ')
            if shape=='help':same= same and s[0].startswith(b'Usage: grep ')
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
        review=field_reviews.get(sys.platform,{}).get(name) if a.field else reviews.get(name)
        if review:
            if a.field:require(review.get('class')=='upstream-blocked' and review.get('platform')==sys.platform,name+' field review scope')
            if not same and exact_review(review,c,g,s):
                if review.get('class')=='environment':counts['environment']+=1
                else:counts['reviewed']+=1
                if review.get('class')=='gnu-inconsistent':counts['gnu-inconsistent']+=1
                if review.get('kind')=='upstream':counts['upstream-blocked']+=1
                if a.field:
                    record=stage/name;record.mkdir(exist_ok=True)
                    for tag,result in [('gnu',g),('scent',s)]:
                        for suffix,value in zip(['stdout','stderr','status','stdin-rest'],result):
                            (record/(tag+'.'+suffix)).write_bytes(str(value).encode() if isinstance(value,int) else value)
                    (record/'case.json').write_text(json.dumps(c,indent=2)+'\n')
                    (record/'classification.json').write_text(json.dumps({'class':review['class'],'platform':sys.platform,'source_run':review['source_run']},indent=2)+'\n')
                    print('UPSTREAM-BLOCKED',name,'reviewed',sys.platform,'source-run',review['source_run'],flush=True)
                else:print('REVIEWED',name,'ruling',review['ruling'],flush=True)
                continue
            same=False
            counts['stale-review']+=1
            print('STALE REVIEW',name,'classification',review.get('ruling',review.get('class')),flush=True)
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
print('{reviewed} reviewed divergences (including {upstream-blocked} upstream-blocked)'.format(**counts),flush=True)
print('{environment} environment differences / {gnu-inconsistent} gnu-inconsistent reviews'.format(**counts),flush=True)
print('not-yet columns: argv0-diagnostic={argv0-diagnostic} argv0-usage={argv0-usage} argv-bytes={argv-bytes} terminator-pattern={terminator-pattern}'.format(**counts),flush=True)
if a.field:
    print('FIELD summary:',json.dumps({k:counts[k] for k in ['agree','differ','reviewed','upstream-blocked','not-yet','field-unavailable','stale-review']},sort_keys=True),flush=True)
    (stage/'field-unavailable.json').write_text(json.dumps(unavailable,indent=2)+'\n')
(stage/'summary.json').write_text(json.dumps(counts,sort_keys=True)+'\n')
if a.capture_reference:
    require(counts['differ']==0 and counts['stale-review']==0 and counts['not-yet']==0, 'only a complete green live run may capture reference results')
    (ROOT/a.capture_reference).write_bytes(gzip.compress(json.dumps(captured,separators=(',',':')).encode(),mtime=0))
raise SystemExit(0 if counts['stale-review']==0 and (a.field or counts['differ']==0) else 1)
