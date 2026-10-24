#!/bin/bash
# Test the draft PKGBUILD's check/package functions without installing on a host.
set -euo pipefail
root=$(cd "$(dirname "$0")/../.." && pwd)
cd "$root"
[ "${SCENT_IN_CONTAINER:-}" = 1 ]
ulimit -c 0
work="$root/target/package-smoke"
mkdir -p "$work/scent-0.2.0"
cp target/release/scent README.md CHANGELOG.md LICENSE LICENSE-TRAINING-DATA "$work/scent-0.2.0/"
cp -R wrappers "$work/scent-0.2.0/"
bash -n packaging/PKGBUILD
source packaging/PKGBUILD
(cd "$work"; check)
(cd "$work"; pkgdir="$work/stage"; package)
compat="$work/stage/usr/lib/scent/bin"
[ -x "$compat/grep" ] && [ -x "$compat/egrep" ] && [ -x "$compat/fgrep" ]
[ "$(PATH="$compat:$PATH" grep --version | head -1)" = 'scent 0.2.0' ]
[ "$(PATH="$compat:$PATH" grep -rh --include='*.txt' hit "$work/scent-0.2.0/.package-tree")" = hit ]
printf 'PASS draft PKGBUILD checks, staged payload and compatibility PATH; no host install\n'
