# ct07 — the last M4 rows, and the plan for -P

_Materialised from scent#19's body at the merge (`154f9938`); the Codex wrapper writes no .md notes._


## Prediction

`8442bcc` committed before implementation. Use the same sixteen workloads, one warmup and eleven before/candidate/GNU samples on locked kasumi CPUs 12–15. Retain a target-median improvement only when no other candidate range is wholly above its before range. Range overlap is the declared noise rule, not statistical significance. Keep the separate 2× M4 target and 32,768 KiB memory ceiling.

Retain EOF workspace deferral. Reject constant-capture inference and count-only dispatch on measured control regressions, despite target wins. M4 remains unmet. No result establishes that every remaining miss requires a new language surface.

This PR body is the five-section note and phased `-P` plan. The orchestrator materialises `notes/ct07-the-last-m4-rows-and-the-p-plan.md` from it; no Markdown report file was written by this lane.

## Forbidden

No GNU grep, PCRE2, gnulib, libc or other third-party implementation source read. No `-P` code, dependency change, package installation, workflow/tier change, language/runtime change, new waiver, label, merge, tag, release or issue action. No Mac build/test, taskset/flock/kill shim, shared prune, planning-repo edit or personal-configuration edit. The existing compiler/runtime pair and non-PCRE oracle remain pinned.

## Inputs verified

- Base `3711901`: scent trunk `bd451ba9` plus ct06's materialised note. Contract, RULES 1–10, ct06 note, table and twice-read toolchain evidence read.
- wolf 0.2.35, lupin 0.1.56, std `2386522eb059cca5a84108562c2c0a0e72345d34`. ct06's twice-read archive/tag evidence remains `notes/ct06-evidence/toolchain-digests.txt`; empty archive directories were not redownloaded.
- Actual image ID verified: `bad63142bf60230bcf147c864f57ce9b51d982a49bedd661456d1f9698734032`. Ubuntu base digest: `sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55`.
- GNU grep 3.12, `--disable-perl-regexp`, executable SHA256 `92b211f7a6422d621d4ab1330739b3dbe520283c5e628b848f36f8c29b9be7ea`. Original ct06 production control SHA256 `96e05922907529ca6dd10be412efe17be935122fc8ac5f7a4f2b7e42333d5af3`.
- Every timed row has exact per-engine status, stdout SHA256/length, empty stderr and all twelve checked runs. The checker rejects missing/unequal tuples and non-finite samples. Source and binary hashes accompany each run. `SCENT_CPUS=12-15` passes the actual CPU block directly to taskset; no shim.
- The adopted agent's aborted trial is not evidence. All three ct07 trials below were rerun from committed source.

## Evidence index

### Commits

- `293f3eb`: persist output tuples and enforce paired retention.
- `1965bef`: trial constant-capture proof with positive, fallback, folded/scalar and VM controls.
- `e327725`: finite M1 syntax census and extraction controls.
- `995c527`: reject capture proof; preserve exact patch, table and counterexample.
- `f60f4e8`: defer matcher/output allocation at EOF without a carried record.
- `9251f21`: run EOF oracle controls with identical argv[0], preserving the first harness red.
- `a9ae88d`: retain recursive improvement, 64.412 → 50.532 ms.
- `21113dc`: trial count-only record dispatch with expanded EOF/count controls.
- `f874b76`: reject count-only dispatch; preserve patch and all sixteen measurements.
- `9b6ce9a`: permanent EOF/census tests and direct CPU selection in the existing speed gate.
- `de4b778`: README-only refresh; install/build/module/count statements read against the pass.
- `c4c188c`: record both draft plant identities and named local red logs.
- `154f993`: retain final green acceptance, source bindings and sixteen-row paired table.

### Controlled trials

| Lever | Target before → candidate ms | GNU ms | Decision and control |
| --- | ---: | ---: | --- |
| Straight-line constant captures | backreference 75.971 → 7.606 | 36.799 | **Rejected**: fixed-1000 6.312 → 6.900; before range [6.131, 6.491], candidate [6.676, 7.106] ms |
| Skip workspace allocation at empty EOF | recursive 64.412 → 50.532 | 5.836 | **Retained**: all sixteen ranges satisfy the declared rule; recursive still 8.659× GNU |
| Count-only record state | count 10.685 → 10.369 | 2.591 | **Rejected**: only-matching 10.326 → 11.177, entire candidate range slower |

The capture and EOF controls use the saved ct06 binary. The count-only control is the accepted EOF binary, so it tests one incremental lever. No rerun was selected to erase either rejected control. Raw records, exact tuples, decision files and rejected patches are under `notes/ct07-evidence/`: `constant-capture.*`, `eof-workspace.*`, `count-only.*`. Expanded reader controls cover 396 exact tuples across empty files, unterminated records, 96 KiB boundaries, stdin, binary/NUL handling, and count/list/quiet/context/limit precedence.

### Final acceptance and sixteen-row table

- Whole `tools/gate` GREEN at source head `de4b778d673563ae8a00d1bf0aff9f1a7513f8c3`, 2026-10-27 02:49:48–03:08:30Z, exit 0, SKIP=0. All **193** accepted source/harness/test/pin hashes are retained in `accept-inputs.json`; later commits are evidence only. `acceptance.log` and `accept-summary.json` record the result.
- 29 checked tests, native/lupin controls and 19 regex units pass. Native, release, deterministic static and original-VM CLI matrices each retain **48,305 cases: 47,514 agree, 790 exact reviews (18 upstream-blocked), one environment, zero unapproved differences/not-yet**. Engine malformed/generated/projection/cost controls pass.
- Five 2 GiB peak RSS values: **2604 / 3084 / 3052 / 4248 / 2776 KiB**, all below the unchanged 32,768 KiB ceiling (`memory-final.json`).
- Locale-free static replay GREEN, exit 0 at 03:10:28Z, using existing image `8ba042cb51b75ddc0c1c801a547144363c50844429e9df64ba6d15b8f0eff648`; no package install. `posture.log` retains the full matrix. Reference capture SHA256 remains `d635cc1dde428cdb7437e7680d1d8c457901ad2a85de801684daac25062daeae`.
- Final accepted executable SHA256 `b2cce4feaaa9136e62a4b84b2b81e7db719e2bf57d38ec8fd71f2ad4867c5f96`. `final-paired.json` has the before/candidate/GNU samples and exact tuples; its retained-target guard passes again. No final candidate range is wholly slower than its paired baseline range. `gate-speed.json` independently passes the unchanged regression ceilings.

All medians below are milliseconds. Ratio = after/GNU. The last column names each remaining miss's controlled trial; final production contains only EOF deferral. Full per-lever sixteen-row tables are in `trial-tables.txt`, with rejected patches and tuples beside them.

| Workload | Before ms | After ms | GNU ms | Ratio | M4 | Controlled lever |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| literal | 94.518 | 93.832 | 12.058 | 7.782 | false | count-only: rejected |
| class | 94.211 | 94.417 | 11.979 | 7.882 | false | count-only: rejected |
| alternation | 144.186 | 143.733 | 11.256 | 12.769 | false | count-only: rejected |
| backreference | 80.975 | 80.956 | 38.865 | 2.083 | false | constant capture: rejected |
| ignore-case | 8.436 | 8.165 | 3.011 | 2.711 | false | count-only: rejected |
| word | 8.367 | 8.135 | 4.588 | 1.773 | true | control |
| count | 11.172 | 11.408 | 2.933 | 3.889 | false | count-only: rejected |
| list | 0.517 | 0.525 | 0.343 | 1.529 | true | control |
| only-matching | 11.585 | 11.224 | 10.343 | 1.085 | true | control |
| invert | 11.271 | 11.491 | 2.950 | 3.895 | false | count-only: rejected |
| binary | 18.814 | 18.943 | 4.314 | 4.391 | false | count-only: rejected |
| recursive | 67.538 | 52.936 | 6.342 | 8.347 | false | EOF allocation: retained |
| utf8-fold | 106.831 | 106.704 | 31.981 | 3.336 | false | count-only: rejected |
| fixed-1 | 4.048 | 3.947 | 1.010 | 3.909 | false | count-only: rejected |
| fixed-10 | 4.414 | 4.557 | 1.349 | 3.377 | false | count-only: rejected |
| fixed-1000 | 6.527 | 6.903 | 1.533 | 4.504 | false | count-only: rejected |

**M4: 3/16 pass, 13 miss.** No waiver. These tables name measured scent trials, not hypothetical upstream speedups.

### Named local plants

- Draft scent#17, branch `ct07-plant-retained-regression`, head `e33aa310878e9d40db348658ca332b27268444a2`. `python3 -I tools/ct07-retention-plant` falsely retains the real rejected capture record and exits 1: `RED retained-lever-regression: fixed-1000`. Local kasumi log: `notes/ct07-evidence/plant-retention.log`.
- Draft scent#18, branch `ct07-plant-missing-tuple`, head `ddd69e34421aeb02bcff4078a826bc71d4e698a4`. `python3 -I tools/ct07-tuple-plant` removes only the recursive row's tuple in memory and exits 1: `RED missing-row-tuple: recursive`. Local kasumi log: `notes/ct07-evidence/plant-tuple.log`.
- The unmutated EOF record with `--retained-target recursive` and the negative-test suite pass separately. Neither plant branch is merged; no plant CI dispatch or label. These are local module-footprint witnesses.

### The phased `-P` plan (M5; design only)

**Oracle prerequisite, shared by every phase.** Build a separate GNU grep **3.12** oracle configured `--enable-perl-regexp`; do not replace the current `--disable-perl-regexp` oracle or its refusal cases. Start from the same Ubuntu 24.04 digest `sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55`. The planned image recipe is the current `ci/oracle.Containerfile` package list plus `libpcre2-dev`, then the existing signature-verified GNU 3.12 tarball (SHA256 `2649b27c0e90e632eadcd757be06c6e9a4f48d941de51e7c0f83ff76408a07b9`) and `./configure --enable-perl-regexp`. Build machinery may compile the oracle, but no implementation source is design input. The current image has the runtime library, not the development package or `pcre2-config`; **this oracle was not built in ct07**.

Before phase 1, pin the resulting image by its actual digest and record the exact PCRE2 package version, linked library SHA, GNU executable SHA, configure flags, libc line and environment. Read the hashes twice. The base digest alone is not the identity of a future PCRE2 build: no invented image/executable digest here. Assert an actual `-P` match and capture the version/feature probes; a disabled-Perl refusal is a failed prerequisite, never a parity pass. All four phases use that same frozen PCRE2-enabled build; changing it requires a new census and explicit review.

**Engine shape.** Add an original, explicit-stack ordered backtracking matcher beside the existing DFA/VM, selected per compiled pattern. Keep the parser/IR's capture numbering, ordered branches, greedy/lazy choice points, assertion state and byte offsets explicit. `-P` is leftmost-first, not POSIX leftmost-longest: `a|ab` on `ab` must not silently inherit `-E` span selection. Only a proven regular subset may use DFA boolean rejection/selection; span extraction, priority-sensitive alternatives, lazy quantifiers and later nonregular features use the ordered engine. Roll back captures with choice points; bound machine stack usage with heap frames, and measure match/depth/resource errors against the pinned oracle instead of silently converting exhaustion to “no match.” Reuse the existing CLI, streaming reader, byte offsets and output interface; preserve record boundaries, NUL/binary policy, `-o` empty-match progress, `-w`, `-x`, `-m`, stdin resume and exact diagnostics. No host PCRE binding or source port.

| Phase | Syntax admitted | Oracle/corpus gate before phase completion |
| --- | --- | --- |
| 1: regular core | Literal/escaped bytes, dot, bracket classes, alternation, groups, anchors, greedy and non-greedy `* + ? {m,n}`; `\d \D \w \W \s \S \b \B`. Translate the regular BRE inventory and escape fixed patterns rather than reinterpret their spelling. Include absolute anchors and simple inline mode/noncapturing forms only once separately probed. Backreferences in GNU `-E` are explicitly phase 3, not smuggled into “everything E covers.” | The frozen PCRE2 GNU oracle; a new phase-1 JSONL corpus projected from the counted eligible M1 patterns, plus independent priority/lazy/boundary/empty/error/CLI controls. Enumerate and report the actual generated pattern and case counts before implementation; capture all oracle tuples and source hashes. Require zero unapproved tuple differences, no unsupported construct counted as an agreement, native/release/checked unit controls, streaming memory gate, and a named local red. |
| 2: assertions and commitment | Positive/negative lookahead and lookbehind; atomic groups `(?>...)` and possessive quantifiers. Respect the pinned PCRE2 version's lookbehind length limits, not a floating manual's newest feature set. | Same frozen oracle. Add measured fixed/variable-length lookbehind acceptance/diagnostic pairs, nested assertion capture rollback, zero-width progress and atomic/possessive counterexamples; cross product with `-o`, `-w`, `-x`, `-z`, boundaries and errors. Exact tuples on the accumulated phase-1+2 corpus; resource/error counts reported separately. |
| 3: capture references and recursion | Numbered/named captures and backreferences; whole-pattern recursion `(?R)` and numbered/named subroutine calls. Distinguish backreference spelling such as `\g{name}` from subroutine spelling `\g<name>`. | Same oracle. Start from the 492 counted backreference pattern instances, translated by original syntax, then measure unset/empty/nested captures, recursion/call rollback, ambiguous alternatives, `-i`, failed recursion and bounded resource limits. All earlier corpora plus the measured phase-3 corpus must remain byte-identical. Unsupported conditional/branch-reset/control-verb syntax stays explicitly outside the admitted grammar, not silently accepted. |
| 4: Unicode properties | `\p{...}` / `\P{...}`, property-aware classes and boundaries, pinned UTF/UCP/locale behavior and case relations. Treat grapheme `\X`, `\R` and extended class operations as separately measured features, not implied by adding properties. | Same oracle and recorded Unicode/PCRE2 version. Exhaustive scalar probes for each admitted property/class, malformed byte sequences, UTF-8 boundaries and property/case cross-products. Preserve original byte spans; byte-exact output/status/stderr/remaining-stdin gates on every accumulated phase. Publish any inconsistency witness and request a recommendation before diverging; do not automatically inherit `-E` exceptions. |

Each phase's new corpus is **to be measured**, not claimed measured now. Its gate records case identities and exact stdout/stderr/status/remaining-stdin; reviewed diagnostics, resource limits and unsupported syntax have distinct counts. No phase completes on unit tests alone: full CLI integration and native/release/static replay plus the unchanged bounded-stream memory ceiling are required. Add focused adversarial cost cases so explicit backtracking cannot turn a bounded test into an unattended soak.

**Version and record caveats.** GNU's documentation says `grep -P` treats `\d` as ASCII digits, while `[[:digit:]]`/`\p{Nd}` include Unicode decimal digits; PCRE2 10.43+ adds `(?aD)`/`(?-aD)` controls. Measure the actual pinned version rather than enabling those forms unconditionally. Normal grep matching is per record; `(?s)` does not automatically make ordinary newline-delimited input one subject. `-z` permits newline-crossing within a NUL record, and GNU documents whole-file memory pressure when no NUL occurs. Retain scent's streaming contract and measure long-record behavior explicitly; do not quietly read the entire input or waive the 2 GiB bounded-record test. Defer callouts, control verbs, branch-reset/duplicate names, conditionals, script runs and recent extended-class/non-atomic assertion features until their grammar and oracle rows are named. No claim of complete PCRE2 compatibility after these four phase titles alone.

Documentation used, not implementation source: [GNU grep manual, grep Programs](https://www.gnu.org/software/grep/manual/grep.html) and [PCRE2 pattern reference](https://www.pcre.org/current/doc/html/pcre2pattern.html). The latter is a moving reference; the frozen oracle version decides supported details.

**Measured M1 syntax census.** `tools/p-plan-census` inventories all `-e`/`-f` sources in the 5,072-case generated M1 matrix; source SHA256 `6cced61c4b4c46f2b6e1913b713df5460ba7e1670eaf6761b5e843f11221e38e`. Its finite classifier fails on unknown additions; extraction/empty-file/diagnostic controls pass. Full row inventory: `notes/ct07-evidence/p-plan-census.json`.

| Census dimension | Phase-1 regular | Phase-1 literal | Phase-3 backreference | Diagnostics |
| --- | ---: | ---: | ---: | ---: |
| Pattern instances | 2,982 | 1,735 | 492 | 12 |
| Distinct (original syntax, pattern bytes) | 18 | 10 | 2 | 4 |

Thus **4,717 of 5,221 pattern instances**, and **28 of 34 syntax/pattern shapes**, are potential phase-1 syntax coverage after BRE translation or fixed escaping. At case level: **4,579 phase-1**, **480 backreference**, **3 empty pattern-file**, **10 diagnostic** cases, totaling 5,072. Empty pattern files are not empty patterns. This is not 4,579 accepted `-P` cases: the matrix includes syntax-option conflicts and option behavior, and no PCRE2-enabled oracle was run. The larger 48,305-case M1/M2/M3 suite is not the denominator. No lookaround/atomic/recursion/property syntax appears in this finite M1 inventory, so later phases need new corpora rather than a misleading inherited percentage.

### Recommendations and issue disposition

- **R-ct07-1 — implemented:** retain only EOF allocation deferral; keep both rejected patches and exact counterexamples. Do not rescue a target win by ignoring another row.
- **R-ct07-2 — implemented:** leave scent#16 open and M4 explicitly unmet. Backreference's large scent-only trial gain disproves any established claim that it necessarily needs a new API, but its failed control prevents retention. Recursive still has a measured gap after its scent-only win. No new issue filed or existing issue closed.
- **R-ct07-3 — implemented:** leave wolf-std#89 and wolf-lang#971 as measured opportunities, not universal blockers. wolf-std#94 is CLOSED; its allocation-and-copy wrapper is not the true primitive sought by wolf-lang#971. No pin adoption or duplicate issue. None of these three ct07 levers needs a new surface, so no row is falsely labelled stopped on one. A future lever that genuinely requires one stops at that boundary with its measured row gap.
- **R-ct07-4 — implemented:** phase `-P` behind a separately pinned PCRE2 oracle and independently counted corpora; no package installation or `-P` implementation in ct07. Resource limits, Unicode inconsistencies and newly exposed unsupported syntax need measured follow-on decisions, not invented rulings here.

## Done-when

- [x] Prediction before implementation; every remaining M4 miss mapped to a measured controlled lever.
- [x] Sixteen unchanged workloads, eleven interleaved samples, exact retained per-engine tuples.
- [x] Retain/reject decisions follow ct06's all-row noise rule; rejected patches preserved.
- [x] Measured M1 syntax census and phased `-P` plan, with future oracle digest explicitly not fabricated.
- [x] Two draft plant PRs, named local reds, production evidence guard green.
- [x] README read and refreshed in its own commit.
- [x] Final local gauntlet, all 396 EOF tuples, original-VM control, five memory witnesses and locale-free static replay green; accepted source hashes retained.
- [ ] All sixteen rows within 2× GNU: M4 remains unmet.
- [ ] GitHub PR tier green: read once, no waiting or label; orchestrator owns the verdict.

### Publication and audit

Final head: `154f99382a16c5c968e68e10a3c4dacab785cf63`. Remote `/home/mfwolffe/lanes/ct07/scent` is clean at that head; all 193 accepted source hashes match. Both local job markers are exit 0; no acceptance job remains running. The two clean plant worktrees were removed explicitly, without force; their branches and logs remain. No other lane's files were pruned.

Sole direct CI run-ID read, immediately after opening: **40443367591**, `in_progress`, at the final head. No CI wait or label.

The required audit was run **once**, from the org directory, with `bash wolf/tools/lane-audit.sh scent ct07 19 /Users/mfwolffe/lanes/ct07/scent`. Its last line was **`AUDIT FAIL (footprint: module)`**. Its only failures were the still-in-progress PR run and absence of a green tier at that head. Footprint/path checks, ancestry, no trailers, five sections, all 15 cited commits, no spec changes, removed Mac worktree and no local lane orphans all passed. The orchestrator owns the pending CI verdict; no audit rerun was made.

The clean, pushed Mac worktree `/Users/mfwolffe/lanes/ct07/scent` was removed before that audit. Final evidence remains committed and in the clean kasumi clone. Issues to close: none; issues to file: none (append measured progress to existing scent#16 if desired). M4 remains open.

