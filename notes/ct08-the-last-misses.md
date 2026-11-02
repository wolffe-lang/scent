# ct08 — the last misses

Materialised from PR #25's body at the merge (`b672e24`); the lane handed its note back in the PR body.

## Prediction

Retain ct07's constant-capture idea only if its backreference target improves and no other candidate range is wholly slower than baseline. `eed9f75` committed the prediction before changes; `3172714` refined it before the trial: infer only at REF nodes from completed exact GROUP proofs, with no capture table/GROUP bookkeeping for ordinary patterns. Conditional, repeated, folded, scalar, unfinished and unknown captures retain the VM. One warmup, eleven interleaved before/candidate/GNU samples on the same sixteen workloads; exact tuples, unchanged ceilings, separate 2× M4 target and 32,768 KiB memory ceiling.

## Forbidden

No GNU grep, PCRE, gnulib or third-party implementation source read. No oracle expectation/review, pin, dependency, workflow, tier or language/runtime surface changed. No labels, merge, tag, issue creation/closure or CI wait. No protected disks, servers, steamlib or personal data touched. `-P` remains the pinned refusal.

## Inputs verified

- Base `7734fb25`; wolf 0.2.36 / lupin 0.1.58 / std 78b9d3cbc41d51db44d18c40b6694403644d1c83. Release APIs/archive digests read twice; actual compiler/runtime/oracle hashes read twice in `capture-first-red.log`.
- GNU grep 3.12 disabled-Perl oracle SHA256 92b211f7a6422d621d4ab1330739b3dbe520283c5e628b848f36f8c29b9be7ea; pinned Ubuntu/glibc identity verified by fetch-oracle.
- Kasumi slot 8–11 locked, taskset inside, 12 GiB container. Benchmark image ID 113ff19c7ace3180dc87d5e3b891eca8a9e295fa9b606a743500c38fefa01266 derives from ct05's image and adds Ubuntu hyperfine 1.18.0-2build1 only inside the image, never the host.
- Timing baseline e035896f74f037b9fd2ad8dfb87f5e6573388318 is **trunk runtime + separator repair**, not the old buggy baseline. Candidate `18ce308` adds only the capture lever to that runtime. Both pass all 271 expanded record tuples before timing; candidate also passes the full release oracle and 396 existing EOF tuples.
- Baseline executable SHA256 98a6845721fede119f5c2301a7fa632ffce5a58d102d231090ac8e4738c90036; candidate fcdb428acc0988c323a4de0602a8f23ace3874b3ead1fe7785f19566bbd7196b.

## Evidence index

### Commits

- `eed9f75` — Predict isolated capture and record trials
- `4f5113f` — Require exact straight-line capture proofs
- `5f13203` — Cover final records and capture fallbacks
- `3172714` — Predict REF-only proof inference before trial
- `a5b8526` — Record named capture red and invalid empty launch
- `eeea47e` — Infer constant captures only at reference nodes
- `4354417` — Record binary context separator STOP and EOF plant
- `1e8b536` — Predict separate separator repair and corrected timing controls
- `bdb71d6` — Name the binary context separator regression row
- `8dfe6d2` — Record named separator red against trunk runtime
- `18ce308` — Preserve group state after a binary match
- `62580af` — Run expanded record controls in the existing reader gate
- `ebc376d` — Refresh README for capture proofs and remaining M4 misses
- `6197b0e` — Retain paired capture measurements and final gate inputs

- `b672e24` — implement ruled CI timeout 40 → 60; retain the measured duration table in the commit message.

### Separator regression and repair

Fix for scent#26: **`18ce308`**, independently committed from the capture lever. The issue remains open for closure at merge. Named `binary-context-separator` row committed at `bdb71d6`, observed red on trunk's runtime in `separator-red.log`, then green on repaired baseline. Under C, first file `needle\0other\nneedle`, second `other\nneedle`, `-F -C1`: GNU prints the `--\n` separator before the later text group; old scent omitted it. The repair establishes prior-group state after a selected binary record without printing a separator at that point. No expectation was relaxed. All 271 expanded record tuples pass on **both** repaired timing engines; the existing CI reader gate now runs them.

### Controlled capture trial

Both the canonical pipe-drained tuple rig and the shell-free, stdout=pipe hyperfine companion use one warmup and eleven interleaved triplets. Canonical timing retains each engine's exact status/stdout SHA256+length/empty stderr and twelve checked runs per row. All three engines agree on every timed tuple. Hyperfine retains all raw single-run exports and exit codes. **Both** records pass the same all-row range-overlap retention function for target backreference. This is a target win, not statistical-significance or universal speed claims.

| Workload | Before ms | Candidate ms | GNU ms | Ratio | Hyperfine ratio | M4 |
|---|---:|---:|---:|---:|---:|---|
| literal | 93.725 | 93.471 | 11.432 | 8.176 | 7.845 | miss |
| class | 93.484 | 92.567 | 11.138 | 8.311 | 7.857 | miss |
| alternation | 142.095 | 142.280 | 11.209 | 12.693 | 12.707 | miss |
| backreference | 81.670 | 8.156 | 39.765 | 0.205 | 0.203 | pass |
| ignore-case | 8.318 | 8.452 | 3.131 | 2.700 | 2.471 | miss |
| word | 8.262 | 8.129 | 4.731 | 1.718 | 1.789 | pass |
| count | 11.039 | 11.123 | 3.028 | 3.673 | 3.800 | miss |
| list | 0.511 | 0.480 | 0.404 | 1.188 | 1.332 | pass |
| only-matching | 11.556 | 11.344 | 10.408 | 1.090 | 1.101 | pass |
| invert | 11.271 | 11.155 | 3.113 | 3.583 | 3.784 | miss |
| binary | 19.875 | 18.434 | 4.692 | 3.929 | 4.145 | miss |
| recursive | 55.946 | 53.824 | 6.792 | 7.924 | 8.436 | miss |
| utf8-fold | 107.954 | 105.400 | 32.075 | 3.286 | 3.221 | miss |
| fixed-1 | 4.110 | 4.171 | 1.229 | 3.393 | 4.182 | miss |
| fixed-10 | 4.838 | 4.599 | 1.608 | 2.860 | 3.406 | miss |
| fixed-1000 | 6.862 | 6.630 | 1.851 | 3.582 | 4.176 | miss |

**4/16 pass; 12 miss. M4 remains unmet; scent#16 stays open.** Hyperfine backreference medians: 82.811 → 7.870 ms, GNU 38.827 ms. Canonical: 81.670 → 8.156 ms, GNU 39.765 ms.

The remaining rows and the reason this lever does not close them are explicit in `performance-table.txt`: literal/class/alternation have no REF to infer; folded/scalar modes are deliberately excluded; fixed/count/invert/binary paths are unchanged; recursive per-file/chunk workspace setup is unchanged beyond ct07's existing EOF deferral. These are untouched source paths, **not isolated root-cause profiles or certified upstream blockers**. No new per-record/per-file lever or `-P` engine was implemented in this pass; those misses remain follow-on work. ct07's rejected count-only controls remain rejected.

All measurements, exact STOP/red/green logs, source bindings and raw samples are in `notes/ct08-evidence/`. Raw hyperfine archive SHA256 1ecdb18a53b4d417f2e51194401eef3de20bb0e1b86d393b56c4f47581c624d5. The two zero-exit empty/drained-stdin launcher logs are retained and explicitly **invalid**, never passes. File-backed scripts, closed stdin and a required completion sentinel correct the launcher.

### Plant and recommendations

Draft plant #24, `f542334`, remains the sole plant. Local `RED reader-last-record` (`plant-last-record.log`): plant status 1/stdout `0\n`, GNU status 0/stdout `1\n`, empty stderr. The production row passes. No second plant, manual dispatch or label.

- **R-ct08-1 implemented:** stop on the new unapproved byte mismatch, keep its control, no waiver.
- **R-ct08-2 implemented:** do not accept an unmeasured candidate or start `-P` from unit greens.
- **R-ct08-3, coordinator, implemented:** repair scent#26 red first in separate commits; rebuild both timing engines around the repaired baseline.
- **R-ct08-4 implemented:** retain REF-only capture inference after both timing protocols pass target gain/all-row noise checks, rather than retain ct07's rejected bookkeeping draft.
- **R-ct08-6, coordinator, implemented:** preserve every CI leg and raise Linux timeout to 60 minutes for its inherited near-limit budget. No CI gate reordering.
- **R-ct08-5 implemented:** leave M4 and scent#16 open, keep twelve misses explicit and defer `-P`; no universal API-blocker claim.

### CI budget: R-ct08-6 (coordinator, C)

**New workflow head `b672e24` changes exactly one line: Linux timeout 40 → 60 minutes. All coverage and gate order remain.** Trunk itself already ran at the limit, so this fixes an inherited budget, not a supposed multi-minute branch cost. Completed trunk runs were **26:44 / 38:57 / 39:55**; 60 minutes provides **20:05 headroom above the completed maximum (50.3%)**. Head `6197b0ee` is **censored at 40:20**, not measured to completion. It was cancelled at 19:22:15Z inside **Streaming memory gate and recorded performance → tools/measure**; the job ended 19:22:17Z. All five 2 GiB memory rows had completed by 19:20:52Z, and legacy performance still reported through 19:22:09Z.

The branch adds **one 271-tuple reader call** inside the existing `tools/measure → speed-ci → reader-eof-test` path. About **1.4 s** is a conservative allowance: the entire logged reader block, including inherited EOF controls, is 1.398 s. No native/release/static oracle leg, locale-free replay, VM oracle, or measure.py memory/performance pass was added by this branch; all are present in the three trunk logs. The additional three record legs in the local gauntlet are not CI additions. Existing unit steps additionally run the constant-capture unit and expanded fast/VM controls; these are added cases, not added jobs or oracle legs (checked/native/lupin: head 15.85 s versus trunk 13.23–16.23 s).

Durations below are mm:ss from each job log's `##[group]Run` timestamp to the next command-group start. `##[endgroup]` closes the printed command prelude, not execution. Last successful artifact duration includes small teardown overhead; the cancelled final measure duration is a lower bound. Raw job logs/metadata and extraction script are retained under `/Users/mfwolffe/lanes/ct08/ci-duration-inputs/` and `/Users/mfwolffe/lanes/ct08/duration-table.py`. The timeout commit message carries this same full table.

| Linux step | Trunk 41275866151 | Trunk 40447227649 | Trunk 40378506459 | Head 41501627600 attempt 1 |
|---|---:|---:|---:|---:|
| Checkout | 0:01.50 | 0:01.57 | 0:01.49 | 0:01.72 |
| Cache | 0:00.25 | 0:01.19 | 0:01.42 | 0:02.01 |
| Build Ubuntu image | 0:26.02 | 0:32.05 | 0:31.77 | 0:27.13 |
| Stage pinned tools/oracle | 0:36.09 | 0:00.39 | 0:00.41 | 0:00.38 |
| M2 corpus | 0:00.12 | 0:00.17 | 0:00.17 | 0:00.15 |
| UTF-8 corpus | 0:01.89 | 0:02.89 | 0:02.73 | 0:02.80 |
| Unicode regeneration | 0:02.43 | 0:03.42 | 0:03.38 | 0:03.43 |
| Format + both builds | 0:06.52 | 0:07.65 | 0:07.88 | 0:07.61 |
| Field guards | 0:00.81 | 0:01.60 | 0:01.78 | 0:01.10 |
| Checked/native/lupin | 0:13.23 | 0:15.93 | 0:16.23 | 0:15.85 |
| Oracle selectors | 0:01.01 | 0:01.52 | 0:01.61 | 0:01.45 |
| Replay guards | 0:02.22 | 0:03.43 | 0:03.38 | 0:03.23 |
| Native oracle | 4:40.85 | 7:05.25 | 7:32.29 | 7:29.91 |
| Release oracle | 4:22.64 | 6:44.41 | 7:05.63 | 7:11.11 |
| Regex engine | 1:59.46 | 2:11.35 | 2:12.03 | 2:12.39 |
| Static build twice | 0:10.63 | 0:13.02 | 0:13.19 | 0:13.23 |
| Static oracle | 4:14.39 | 6:43.34 | 6:49.90 | 7:02.29 |
| Locale-free replay | 2:43.30 | 4:37.53 | 4:35.00 | 4:47.28 |
| Measure wrapper + VM oracle | 6:49.54 | 10:01.92 | 10:05.23 | ≥10:12.56 |
| Artifacts / final cleanup | 0:09.27 | 0:06.69 | 0:06.85 | not reached |
| **Job wall** | 26:44.00 | 38:57.00 | 39:55.00 | 40:20.00 |

No cuts, splits, gate movement, new waiver or manual CI cancellation/rerun. Option A would remove distinct coverage without a separate coverage argument; B retains coverage but adds artifact/provenance and runner-scheduling machinery. C retains all coverage with measured completed-trunk headroom; it does not invent an uncensored head duration.

### Runtime acceptance and new workflow head

Program/runtime acceptance head: 6197b0eeb6ae8cfdd9126ab88f2a8d4038070018. New PR workflow head: b672e2401db0c569bba0a096d324d897c24c76b0 changes only the ruled timeout. **One runtime-head local gauntlet GREEN, exit 0**, on kasumi slot 8–11. Native/release/static/original-VM matrices and locale-free static replay pass without new/unapproved differences. `wolf test` reports 30 passed/zero not passed; native/lupin controls and 20 regex units pass. All three added 271-tuple record gates pass. Five 2 GiB memory peaks: **2508 / 2768 / 2640 / 3880 / 2724 KiB**, below unchanged 32768 KiB. Final speed gate passes and still reports only 4/16 M4 passes. All 335 source/test/tool/pin/fixture hashes are bound to runtime head 6197b0ee in `target/final-inputs.json`; b672e24 changes only the workflow hash/budget, not program sources. The tested runtime release SHA256 exactly equals the accepted paired candidate. Static SHA256 b9fb6390f6dadb883159592c77d7610544842a99b778ce7325c40c56aa6f5652.

Committed launcher inputs are in the evidence directory. Durable remote log `/home/mfwolffe/lanes/ct08/gauntlet.log`, marker `/home/mfwolffe/lanes/ct08/gauntlet.exit` = 0; the completed final worktree was removed by exact path after archiving accepted binaries/reports under `/home/mfwolffe/lanes/ct08/accepted-evidence/`. Final artifacts are also copied under `/Users/mfwolffe/lanes/ct08/final-evidence/`. No program source or performance evidence changed after the tested runtime head; the later b672e24 workflow-budget commit requires its own new CI verdict. Completed stale probes and the clean pushed Mac checkout/worktrees were removed; accepted artifacts remain in the archive; paired samples/source bindings are committed and control branches are pushed.

Every final-head END line:

```text
END tiers exit=0
END regex-harness exit=0
END m2-harness exit=0
END m1-harness exit=0
END m3-harness exit=0
END ctype-regeneration exit=0
END review-guards exit=0
END format exit=0
END build-all exit=0
END field-guards exit=0
END checked-native-lupin exit=0
END oracle-selection exit=0
END oracle-replay-guards exit=0
END native-oracle exit=0
END release-oracle exit=0
END regex-engine exit=0
END deterministic-static exit=0
END static-oracle exit=0
END records-native exit=0
END records-release exit=0
END records-static exit=0
END memory exit=0
END speed-and-vm exit=0
END source-bindings exit=0
END joined-gauntlet exit=0
END paired-binary-binding exit=0
END locale-free-posture exit=0
END final-complete exit=0
```

The prior module-head audit ran **once**, from the org directory, at runtime head 6197b0ee; it is historical, not an audit of the new workflow head. A new audit is deferred until the new main run is green, as directed. The prior audit result was Exact last line: **`AUDIT FAIL (footprint: module)`**. Its only failures are the in-progress PR run and absence of a green tier at that head. Ancestry, module paths, no trailers, five sections, all 14 cited commits, no spec changes, removed Mac checkout and no local orphans pass. The prior audit observed run **41501627600** in progress; its attempt 1 later timed out as tabulated above. The coordinator owns CI watches; no lane CI wait or label. The immediate post-push lookup had only returned old-head run 41498725241; that is not final-head acceptance. **Do not merge until the new workflow head is green and its audit has run.**

### Final workflow and plant verdicts

The coordinator reports **labelled run 41516408914 SUCCESS at unchanged head b672e2401db0c569bba0a096d324d897c24c76b0**. Rebuilt plant run **41516035362** at bd6aa53 is a valid EOF red: first failing step **Exact-name and explicit-glob oracle selection**, sole first-step row **chunk-00**. The later utf8-m2-colour-edge-057/058/059 rows use `-zC1`; their LF-ended input lacks a NUL terminator, so they are the same omitted final-record defect, not an unrelated colour bug. #24 now records the actual log, complete first-step row list, later red counts and this classification. Capture units are green. No source push followed these verdicts. Cleanup is complete: every linked Mac/Linux worktree was removed by exact path after preserving accepted evidence and bundles. The new-head audit ran once after this green run and ended **`AUDIT CLEAN (footprint: cross-cutting)`**; full output `/Users/mfwolffe/lanes/ct08/audit-b672e24.log`. All jobs/steps/annotations pass, tier full selected 3/3 jobs, full-matrix label and head match verified. Cancelled run 41515547687 ran no steps and is explicitly not evidence. No source push followed the green verdict or audit.

## Done-when

- [x] Committed prediction and named capture red before the lever; Mac red also preserved and its completed worktree pruned.
- [x] scent#26 named red → separate fix → green; repaired baseline and candidate both pass 271 expanded tuples.
- [x] Candidate format, 20 regex units, release matrix, 396 EOF tuples; no new/unapproved differences.
- [x] Sixteen canonical/hyperfine triplets; exact tuples/raw samples retained; both retention guards pass.
- [x] One EOF plant, draft PR, named local red.
- [x] README read/refreshed in its own commit; existing CI reader gate covers new regression.
- [x] Runtime-head6197 native/release/static/VM, checked/native/lupin, memory and locale-free gauntlet green; exit0. Timeout-only workflow head b672e24 awaits its new CI verdict.
- [x] Labelled new-head run 41516408914 green at b672e24; no lane label/wait.
- [x] New workflow-head audit once after green labelled run41516408914: AUDIT CLEAN (footprint: cross-cutting); old module-head audit retained historically.
- [ ] Every workload within 2× GNU: twelve named misses remain; M4 not met and `-P` not started.

Footprint: cross-cutting

