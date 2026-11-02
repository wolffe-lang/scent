#!/usr/bin/env python3
"""Companion hyperfine samples; canonical tools/speed retains exact pipe tuples."""
import json, os, pathlib, statistics, subprocess, sys
root = pathlib.Path('/work/scent')
record = json.loads((root/sys.argv[1]).read_text())
output = root/sys.argv[2]
raw = output.with_suffix('')
raw.mkdir(parents=True, exist_ok=True)
corpus = root/'target/ct05-corpus'
inputs = {name: corpus/path for path, names in [
    ('text', ['literal', 'class', 'alternation', 'list']),
    ('log', ['backreference', 'ignore-case', 'word', 'count', 'only-matching', 'invert']),
    ('binary', ['binary']), ('tree', ['recursive']), ('utf8', ['utf8-fold']),
    ('many', ['fixed-1', 'fixed-10', 'fixed-1000'])] for name in names}
binaries = {'scent': root/'target/release/scent', 'gnu': root/'.oracle/grep',
            'before': root/'target/before/scent'}
result = {'head': record['head'], 'affinity': sorted(os.sched_getaffinity(0)),
          'hyperfine': subprocess.check_output(['hyperfine', '--version'], text=True).strip(),
          'protocol': 'one warmup; eleven interleaved single-run shell-free hyperfine samples; output=pipe; canonical tuple checks in paired tools/speed report',
          'canonical_binaries': record['binaries'], 'rows': []}
for row in record['rows']:
    times = {name: [] for name in binaries}
    for turn in range(12):
        for engine in (list(binaries) if turn % 2 == 0 else list(reversed(binaries))):
            filename = raw/f'{row["name"]}-{turn}-{engine}.json'
            # hyperfine --shell=none performs its own argument splitting.
            import shlex
            command = shlex.join([str(binaries[engine]), *row['argv'], str(inputs[row['name']])])
            subprocess.run(['hyperfine', '--shell=none', '--runs', '1', '--warmup', '0',
                            '--output', 'pipe', '--ignore-failure', '--export-json', str(filename), command],
                           env=dict(os.environ, LC_ALL=row['locale']), stdout=subprocess.DEVNULL, check=True)
            measured = json.loads(filename.read_text())['results'][0]
            assert measured['exit_codes'] == [row['tuples'][engine]['status']], (engine, measured)
            if turn:
                times[engine].append(measured['times'][0])
    medians = {engine: statistics.median(samples) for engine, samples in times.items()}
    result['rows'].append({'name': row['name'], 'seconds': times, 'median': medians,
                           'ratio': medians['scent']/medians['gnu'],
                           'm4_2x': medians['scent']/medians['gnu'] <= 2})
    output.write_text(json.dumps(result, indent=2)+'\n')
    print('hyperfine', row['name'], medians, flush=True)
