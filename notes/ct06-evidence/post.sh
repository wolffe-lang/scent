#!/bin/bash
set -uo pipefail
root=/home/mfwolffe/lanes/ct06
cd "$root/scent"
echo $$ > "$root/post.pid"
while [ ! -f "$root/accept.status" ]; do echo 'Waiting for owned whole acceptance'; sleep 60; done
if [ "$(cat "$root/accept.status")" != 0 ]; then echo 2 > "$root/post.status"; exit 2; fi
printf 'START '; date -u +%FT%TZ
flock /home/mfwolffe/lanes/kasumi-cores-4-7.lock taskset -c 4-7 env SCENT_IMAGE=localhost/ct05-scent SCENT_CONTAINER_ARGS='--cpuset-cpus 4-7' tools/in-container python3 -I tools/speed --before-bin target/ct06-baseline --output notes/ct06-evidence/final-paired.json --ceilings tests/speed-ceilings.json > "$root/final-paired.log" 2>&1
rc=$?
if [ "$rc" = 0 ]; then
flock /home/mfwolffe/lanes/kasumi-cores-4-7.lock taskset -c 4-7 podman run --rm --cpuset-cpus 4-7 -v "$root/scent:/work/scent:Z" -w /work/scent localhost/px80-ubuntu bash -c '
set -euo pipefail
ulimit -c 0
rm -rf /usr/lib/locale
unset LANG LANGUAGE LC_ALL LC_CTYPE
export SCENT_IN_CONTAINER=1 SCENT_NO_LOCALE=1
test ! -e /usr/lib/locale
printf "PAX posture: existing Ubuntu/glibc 2.39 image, no locale files, static scent, no package installation\n"
python3 -I tools/oracle.py --bin target/mkscent/scent --replay-reference target/pax-reference.json.gz
' > "$root/posture.log" 2>&1
rc=$?
fi
printf 'END '; date -u +%FT%TZ
printf 'EXIT %s\n' "$rc"; echo "$rc" > "$root/post.status"; exit "$rc"
