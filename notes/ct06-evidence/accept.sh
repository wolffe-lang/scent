#!/bin/bash
set -uo pipefail
root=/home/mfwolffe/lanes/ct06
cd "$root/scent"
echo $$ > "$root/accept.pid"
printf 'START '; date -u +%FT%TZ
git diff --exit-code -- src tools ci tests || exit 2
python3 -I - <<'PY'
import hashlib,json,pathlib,subprocess
paths=subprocess.check_output(['git','ls-files','src','tools','ci','.github','tests','wolf-toolchain.toml','scent-oracle.toml'],text=True).splitlines()
pathlib.Path('notes/ct06-evidence/accept-inputs.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'sha256':{p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest() for p in paths}},indent=2)+'\n')
PY
flock /home/mfwolffe/lanes/kasumi-cores-4-7.lock taskset -c 4-7 env SCENT_IMAGE=localhost/ct05-scent SCENT_CONTAINER_ARGS='--cpuset-cpus 4-7 -v /home/mfwolffe/lanes/ct06/bin:/lane-bin:ro -e PATH=/lane-bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' tools/in-container tools/gate &
child=$!; echo "$child" > "$root/accept-container.pid"
wait "$child"; rc=$?
printf 'END '; date -u +%FT%TZ
printf 'EXIT %s\n' "$rc"; printf '%s\n' "$rc" > "$root/accept.status"
exit "$rc"
