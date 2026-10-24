"""Exact case/result reviews; only two blocked runtime rows have a typed PID."""
import hashlib,json,re
PID_CASES={'not-yet-argv-bytes-0','not-yet-argv-bytes-1','utf8-not-yet-argv-bytes-0','utf8-not-yet-argv-bytes-1'}
PID_HEADER=re.compile(br"\A\nthread '<unnamed>' \(([0-9]+)\) panicked at ")
def result_tuple(result,typed_pid=False):
    out,err,status,rest=result
    if typed_pid:
        match=PID_HEADER.match(err)
        if match is None:return None
        err=err[:match.start(1)]+b'{pid}'+err[match.end(1):]
    return [out.hex(),err.hex(),status,rest.hex()]
def exact_review(review,case,gnu,scent):
    typed=review.get('scent_pid_field',False)
    if typed and (case['name'] not in PID_CASES or review.get('kind')!='upstream'):return False
    identity=hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return (gnu!=scent and review['case_sha256']==identity and
            result_tuple(gnu)==review['gnu'] and result_tuple(scent,typed)==review['scent'])
