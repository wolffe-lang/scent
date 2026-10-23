#!/usr/bin/env python3
"""Build the pinned binary, never examine GNU's implementation."""
import hashlib, json, os, pathlib, shutil, subprocess, tempfile, tomllib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
PIN = tomllib.loads((ROOT/'scent-oracle.toml').read_text())['oracle']
def digest(p):
    return hashlib.file_digest(open(p,'rb'), 'sha256').hexdigest()
def require(ok, text):
    if not ok: raise SystemExit('fetch-oracle: REFUSED: '+text)
def run(args, **kw):
    return subprocess.run(args, check=True, **kw)
def verify(binary):
    require(digest(binary)==PIN['binary_sha256'], 'binary digest mismatch')
    require(subprocess.check_output([str(binary),'--version']).splitlines()[0].decode()==PIN['version_line'], 'version identity')
    libc=subprocess.check_output(['ldd','--version']).splitlines()[0].decode()
    require(libc==PIN['glibc_line'], 'libc identity: '+libc)
    r=subprocess.run(['grep','-P','x'], executable=str(binary), input=b'', capture_output=True)
    require(r.returncode==PIN['perl_status'] and r.stdout==b'' and r.stderr==(PIN['perl_refusal']+'\n').encode(), 'Perl refusal')
stage=ROOT/'.oracle'; stage.mkdir(exist_ok=True)
if all((stage/name).exists() for name in ['grep','egrep','fgrep']):
    verify(stage/'grep'); print('fetch-oracle: pinned binary verified'); raise SystemExit(0)
# Fixed build paths are part of deterministic debug information.
source=pathlib.Path('/work/unseen-source'); build=pathlib.Path('/work/build')
require(not source.exists() and not build.exists(), 'build paths are not empty')
with tempfile.TemporaryDirectory(prefix='scent-oracle-',dir=stage) as tmp:
    tmp=pathlib.Path(tmp)
    for name,url in [('grep.tar.xz',PIN['url']),('grep.sig',PIN['sig_url']),('keyring.gpg',PIN['keyring_url'])]:
        urllib.request.urlretrieve(url,tmp/name)
    for key,name in [('sha256','grep.tar.xz'),('keyring_sha256','keyring.gpg')]:
        require(digest(tmp/name)==PIN[key],name+' digest'); require(digest(tmp/name)==PIN[key],name+' second digest')
    home=tmp/'gnupg'; home.mkdir(mode=0o700)
    sig=subprocess.run(['gpg','--batch','--homedir',str(home),'--no-default-keyring','--keyring',str(tmp/'keyring.gpg'),'--status-fd','1','--verify',str(tmp/'grep.sig'),str(tmp/'grep.tar.xz')],capture_output=True)
    require(sig.returncode==0 and ('[GNUPG:] VALIDSIG '+PIN['signing_fingerprint']+' ').encode() in sig.stdout, 'signature fingerprint')
    source.mkdir();build.mkdir()
    try:
        run(['tar','-xJf',str(tmp/'grep.tar.xz'),'-C',str(source)])
        with open(tmp/'configure.log','wb') as log:
            run([str(source/'grep-3.12/configure'),PIN['configure_args']],cwd=build,stdout=log,stderr=subprocess.STDOUT)
        with open(tmp/'make.log','wb') as log:
            run(['make','-j4'],cwd=build,stdout=log,stderr=subprocess.STDOUT)
        verify(build/'src/grep')
        shutil.copy2(build/'src/grep',stage/'grep')
        # Install and copy wrappers without reading their source.
        installed=tmp/'installed'
        run(['make','install','DESTDIR='+str(installed)],cwd=build,stdout=subprocess.DEVNULL)
        for name in ['egrep','fgrep']:
            shutil.copy2(installed/'usr/local/bin'/name,stage/name)
        shutil.copy2(source/'grep-3.12/doc/grep.info',stage/'grep.info')
        (stage/'identity.json').write_text(json.dumps(PIN,sort_keys=True)+'\n')
    finally:
        shutil.rmtree(source);shutil.rmtree(build)
print('fetch-oracle:',PIN['binary_sha256'])
