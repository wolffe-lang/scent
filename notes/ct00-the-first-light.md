# ct00 — the first light

This note was written at merge from the pull request's body (wolffe-lang/scent#3), because the lane's tooling could not write Markdown notes; the lane's own evidence is in `notes/ct00-evidence/` (`measurements.txt` is its five-section note).

## Forbidden

Clean-room: POSIX, GNU documentation/black-box runs, and cited own-code references only. No GNU/gnulib/glibc/busybox/PCRE2 implementation read. No Mac build, host package installation, foreign-lane edit, attribution trailer, merge/tag/release or issue action. Container-only dependencies and cores12–15 use the shared lock. Both plant PRs are closed unmerged.

## Inputs verified

wolf 0.2.34, paired lupin 0.1.55 and bundled std e036bec; release API digests read twice and Linux archives hashed twice. GNU grep 3.12 tarball/signature/keyring/fingerprint, `--disable-perl-regexp`, Ubuntu image, glibc and executable digest are pinned. A fresh independent build reproduced the oracle digest twice. Aspen `476edee3`, lope `bc388673`, boreutils `12de639f`; ferp `7d332b5` supplies 80 cited cases, never expected outputs.

- `ba2965a` — prediction before implementation
- `4ca8916` — toolchain/oracle pins and scaffold
- `5865ba5`, `2d6dcaa`, `da2122a`, `e1e9bd2` — literal matching, CLI, byte output, streaming/interface
- `a159d64` — monotonic per-pattern KMP cursors, linear repeated-span witnesses
- `62654a7` — exact names or explicit globs for `--only`, with CI regression
- `f1b90e8` — normal binary-policy NUL-pattern witnesses
- `035d8cf` — complete evidence; final head

## Prediction

First 610-case run: 579 agree/12 differ/19 not-yet. Largest-category prediction was wrong (output9, CLI2, patterns1); ferp80 and stripped<3MiB were correct. Literal12x prediction overestimated measured6.77x. Program-name measurement was explicitly not blind; binary prediction was incomplete about late-NUL `-I` status.

## Evidence index

`notes/ct00-evidence/measurements.txt` is the five-section note fallback: the wrapper forbids report `.md` files. It records every measured rule, all R-ct00-1..5 decisions, not-yet columns and the ct02 handoff. Raw rows/logs: `measure.json`, `kasumi-gauntlet.log`, `final-oracle.log`, `oracle-rebuild.log` in that directory. `docs/MAP.md` specifies the matcher API and region/buffer model. README refreshed.

**Final local gate:** native/release/static each 718 agree / 0 differ / 240 explicitly not-yet, total 958 cases. wolf test: 3 checked programs, the same 3 native/lupin, 0 SKIP; planner and selector regressions pass. Not-yet: G/E2; M2 recursion/colour12; argv0 diagnostics3/usage3 (wolf-lang#899); invalid UTF-8 arguments2 (wolf-lang#406); cross-record terminator patterns218 (R-ct00-5). No other pinned-record-oracle divergence is waived. The extra normal-binary NUL-pattern probe agrees in default/-c/-a/-I modes and adds no waiver.

**Memory**,2GiB, drained pipe: `-F -c`2112KiB; `-F -n`2240KiB, both below32MiB. Full counts/output lengths are asserted. **Performance**,256MiB/3 runs, scent/GNU median seconds: literal0.938782/0.138622(6.77x); ignore-case0.941376/0.140797(6.69x); count0.716929/0.099881(7.18x); inverted-count0.719722/0.100307(7.18x). Recorded, not gated; M4 owns speed. GNU's `/dev/null` early-exit rows were discarded.

**mkscent**,built twice equal: `2c3e9efaad6cbbb26a9b31a6a8690173b2654c29c066615db3e033802e673624`,14453056 bytes; stripped1190776 bytes, digest `271da6ac93b9783832d66f2e626640af3e06fff98d6d392ea3a5decf13ee02c8`.

**Plants seen red:** scent#1, run 39945903235/linux job 120388432755, wrong context separator (`1-before` vs `1;before`),0 agree/1 differ. scent#2, run 39945910445/linux job 120388440483, discarded carry with7-byte reads, `DIFFER chunk-00`; artifact proves GNU163847 output bytes/status0 vs scent0 bytes/status1. Both closed unmerged; fixed implementation preceded plants. Incidental substring-selected not-yet cases in plant2 motivated the tested exact/glob selector fix.


**macOS field leg (non-gating):** run 39957212628, macos job, recorded702 agree /5 differ /240 not-yet /11 Linux-only fixtures unavailable. All five differences: `cli-42` and `long-prefix-p` reflect Homebrew's PCRE-enabled build versus the deliberately disabled oracle; `same-input-output-0`, `same-input-output-5`, `same-input-output-6` are genuine platform defects (scent times out while GNU detects self-output, including the silent case). Linux passes those cases. R-ct00-6 asks to track the Darwin fd-identity guard, suspected path-stat versus descriptor-identity mismatch; the cause still needs confirmation. No issue filed by this lane. These are recorded field defects, not claimed byte-identical results or additional pinned-oracle waivers.

Pruned generated measurement inputs, closed plant worktrees, transferred cache, own old container images and transfer archives. Retained current lane image/downloads/binaries/logs. No global prune; no new issue filed or closed. Existing wolf-lang#899 / wolf-lang#406 and ct02's R-ct00-5 remain explicit.

## Done-when

- [x] Prediction, digest pins, unseen-source oracle build, CLI/read/output/-F and stable matcher seam
- [x] 958 cases,80 ferp citations; all three binary oracle legs and checked/native/lupin tests
- [x]Memory gate, recorded performance, deterministic static binary
- [x]Both intended CI plants red, draft PRs closed unmerged; selector regression fixed
- [x]README and evidence refreshed; final head pushed
- [x] CI `tier pr` green at final head: run 39957207749
- [x] `full-matrix` added after opening at final head; `tier full` green: run 39957212628
- [x] Lane audit read directly: `AUDIT CLEAN (footprint: cross-cutting)`

Footprint: cross-cutting

