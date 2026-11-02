#!/usr/bin/env bash
set -euo pipefail
home=/home/mfwolffe/lanes/ct08
slot=${1:?slot}
expected=${2:?expected release binary digest}
echo $$ > "$home/gauntlet.pid"
trap 'echo $? > "$home/gauntlet.exit"' EXIT
git -C "$home/scent" fetch "$home/final.bundle" ct08
head=$(git -C "$home/scent" rev-parse FETCH_HEAD)
path="$home/final-$head"
git -C "$home/scent" worktree add "$path" "$head"
cp -a "$home/base-317271411f5e0a597b71fb5b550f41c5a16aec74/.wolf-bin" "$home/base-317271411f5e0a597b71fb5b550f41c5a16aec74/.oracle" "$path/"
printf 'ct08 gauntlet head=%s slot=%s expected=%s time=%s\n' "$head" "$slot" "$expected" "$(date -u)"
flock -w 21600 "/home/mfwolffe/lanes/kasumi-cores-$slot.lock" bash "$home/gauntlet-locked.sh" "$home" "$head" "$slot" "$expected" </dev/null
grep -qx "$head" "$home/gauntlet.complete"
