"""Field capabilities are measured on the corpus filesystem, not guessed by OS."""
import base64,errno,os,pathlib,tempfile

def needs_non_utf8_name(case):
    names=[os.fsencode(name) for name in case.get('files',{})]
    names.extend(base64.b64decode(row['name_base64']) for row in case.get('raw_names',[]))
    for name in names:
        try:name.decode('utf-8')
        except UnicodeDecodeError:return True
    return False

def probe_non_utf8_name(stage,opener=os.open):
    # Permission/storage failures are harness errors, never an unavailable fixture.
    rejected={errno.EILSEQ,errno.EINVAL,errno.ENOTSUP}
    with tempfile.TemporaryDirectory(prefix='raw-name-probe-',dir=stage) as directory:
        name=os.fsencode(directory)+b'/\xff'
        try:
            fd=opener(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except OSError as error:
            if error.errno not in rejected:raise
            return {'available':False,'reason':f'non-UTF-8 filename rejected: errno={error.errno} {error.strerror}'}
        else:os.close(fd)
    return {'available':True,'reason':'filesystem accepts the byte FF filename'}

def unavailable_reason(case,capabilities):
    raw=capabilities.get('non-utf8-filename',{})
    if needs_non_utf8_name(case) and raw.get('available') is False:return raw['reason']
    return None
