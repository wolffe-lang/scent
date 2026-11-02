#!/usr/bin/env python3
"""Isolate the STOP without changing any oracle expectation."""
import hashlib, json, os, pathlib, subprocess
work = pathlib.Path('/work/scent/target/ct08-witness')
work.mkdir(parents=True, exist_ok=True)
inputs = {'first': b'needle\0other\nneedle', 'second': b'other\nneedle'}
for name, data in inputs.items():
    (work/name).write_bytes(data)
argv = ['grep', '-F', '-C', '1', 'needle', 'first', 'second']
result = {'argv': argv, 'locale': 'C', 'inputs_hex': {k: v.hex() for k, v in inputs.items()},
          'before_head': '317271411f5e0a597b71fb5b550f41c5a16aec74',
          'candidate_head': 'eeea47ef38355778345e3fc4a7f5170db9d72066', 'engines': {}}
answers = {}
for name, binary in [('before', '/before/target/release/scent'),
                     ('candidate', '/work/scent/target/release/scent'),
                     ('gnu', '/work/scent/.oracle/grep')]:
    p = subprocess.run(argv, executable=binary, cwd=work, capture_output=True,
                       env=dict(os.environ, LC_ALL='C'))
    answer = {'status': p.returncode, 'stdout_hex': p.stdout.hex(), 'stderr_hex': p.stderr.hex()}
    result['engines'][name] = {'binary_sha256': hashlib.sha256(pathlib.Path(binary).read_bytes()).hexdigest(), **answer}
    answers[name] = answer
result['baseline_equals_candidate'] = answers['before'] == answers['candidate']
result['candidate_equals_gnu'] = answers['candidate'] == answers['gnu']
(work/'witness.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2), flush=True)
assert result['baseline_equals_candidate'], 'Candidate introduced the mismatch'
assert not result['candidate_equals_gnu'], 'Witness no longer reproduces'
print('RED binary-context-separator: baseline and candidate omit GNU group separator before second file', flush=True)
raise SystemExit(1)
