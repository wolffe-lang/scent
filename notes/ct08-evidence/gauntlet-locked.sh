#!/usr/bin/env bash
set -euo pipefail
home=$1; head=$2; slot=$3; expected=$4
path="$home/final-$head"
image=113ff19c7ace3180dc87d5e3b891eca8a9e295fa9b606a743500c38fefa01266
set +e
podman run --rm --memory 12g -e SCENT_IN_CONTAINER=1 -e SCENT_CPUS="$slot" -e LC_ALL=C -e GITHUB_SHA="$head" \
 -v "$path:/work/scent:Z" -v "$home/gauntlet-inner.sh:/lane/gauntlet-inner.sh:ro" \
 -w /work/scent "$image" taskset -c "$slot" bash /lane/gauntlet-inner.sh </dev/null
rc=$?
set -e
printf 'END joined-gauntlet exit=%s\n' "$rc"
[ "$rc" -eq 0 ]
set +e
actual=$(sha256sum "$path/target/release/scent" | cut -d' ' -f1)
[ "$actual" = "$expected" ]
rc=$?
set -e
printf 'END paired-binary-binding exit=%s\n' "$rc"
[ "$rc" -eq 0 ]
set +e
podman run --rm --memory 12g -v "$path:/work/scent:Z" -w /work/scent \
 8ba042cb51b75ddc0c1c801a547144363c50844429e9df64ba6d15b8f0eff648 taskset -c "$slot" bash -c '
set -euo pipefail
ulimit -c 0
rm -rf /usr/lib/locale
unset LANG LANGUAGE LC_ALL LC_CTYPE
export SCENT_IN_CONTAINER=1 SCENT_NO_LOCALE=1
test ! -e /usr/lib/locale/locale-archive
printf "PAX posture: LANG=%s; no locale data; static scent\n" "${LANG-unset}"
python3 -I tools/oracle.py --bin target/mkscent/scent --replay-reference target/pax-reference.json.gz
' </dev/null
rc=$?
set -e
printf 'END locale-free-posture exit=%s\n' "$rc"
[ "$rc" -eq 0 ]
printf '%s\n' "$head" > "$home/gauntlet.complete"
echo 'END final-complete exit=0'
