#!/usr/bin/env bash
set -euo pipefail
ulimit -c 0
step() {
 label=$1; shift
 set +e; "$@"; rc=$?; set -e
 printf 'END %s exit=%s\n' "$label" "$rc"
 [ "$rc" -eq 0 ]
}
step tiers python3 -I ci/tiers-test.py
step regex-harness python3 -I tools/re-ci-test
step m2-harness python3 -I tools/m2-ci-test
step m1-harness python3 -I tools/m1-ci-test
step m3-harness python3 -I tools/m3-ci-test
step ctype-regeneration tools/check-ctype-regen
step review-guards python3 -I tools/oracle-review-test
step format tools/check-fmt
step build-all tools/build --all
step field-guards python3 -I tools/oracle-field-test
step checked-native-lupin tools/check-test
step oracle-selection tools/oracle-select-test
step oracle-replay-guards tools/oracle-replay-test
step native-oracle tools/oracle --bin target/native/scent
step release-oracle tools/oracle --bin target/release/scent
step regex-engine tools/re-ci
step deterministic-static tools/mkscent target/mkscent
step static-oracle tools/oracle --bin target/mkscent/scent --capture-reference target/pax-reference.json.gz
step records-native python3 -I tools/ct08-record-test --bin target/native/scent
step records-release python3 -I tools/ct08-record-test
step records-static python3 -I tools/ct08-record-test --bin target/mkscent/scent
step memory python3 -I tools/measure.py --memory-only --output target/final-memory.json
step speed-and-vm tools/speed-ci
step source-bindings python3 -I - <<'PY'
import hashlib,json,os,pathlib
root=pathlib.Path('.')
report={'head':os.environ['GITHUB_SHA'],'files':{},'binaries':{}}
for directory in ['src','tools','tests','ci','.github','ucd']:
 for path in sorted((root/directory).rglob('*')):
  if path.is_file() and '__pycache__' not in path.parts:
   report['files'][str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
for name in ['wolf-toolchain.toml','scent-oracle.toml','README.md']:
 report['files'][name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
for name in ['target/native/scent','target/release/scent','target/mkscent/scent']:
 report['binaries'][name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
(root/'target/final-inputs.json').write_text(json.dumps(report,indent=2)+'\n')
PY
