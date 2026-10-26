# ct06 — the speed, part two

_Materialised from scent#15's PR body at the merge (bd451ba9); the lane's wrapper could not write Markdown notes._

## Prediction

Committed before implementation in 45c53f0. Start from trunk `8f69f8f445c4622d8d4942f100dec11d77260eeb`; preserve byte-exact behavior and the 32,768 KiB gate. Investigate ct05's dense transitions, local trie edges, indexed skips and read path before new levers. Retain a target-median improvement only when no other after range is wholly above its before range. This predeclared range-overlap band is not a statistical-significance claim.

**M4 remains unmet: 3/16 pass, 13 miss.** Every original miss has a named measured lever in `notes/ct06-evidence/row-levers.txt`. The pass does **not** establish that every remaining miss requires a new language surface: the issue drafts separate measured API opportunities from unfinished scent work. That part of the stronger contract remains unproved, not silently certified.

The wrapper prohibits Markdown report files. This PR body is the five-section note; materialise `notes/ct06-the-speed-part-two.md` from it at merge.

## Forbidden

No GNU grep, gnulib, libc, PCRE2 or other third-party implementation source read. Only scent's own code and previously recorded black-box/API controls. No C adapter linked into scent. No dependency/pin, workflow, tier, runtime or spec change; no package installation, Mac build, label, merge, tag, release or issue action. No planning-repo or personal-configuration edit, shared prune, process-name/group kill, or attribution trailer.

## Inputs verified

- Full ct05 note, table and raw JSON evidence, scent index/rulings and RULES 1–10 read. Correct evidence path is `notes/ct05-evidence/`, not the contract's `notes/ct05/`.
- wolf 0.2.35 / lupin 0.1.56 / std `2386522eb059cca5a84108562c2c0a0e72345d34` unchanged. Release archive hashes and dereferenced tag commits read twice: `toolchain-digests.txt`. Complete compiler/runtime pair copied from ct05.
- GNU grep 3.12, `--disable-perl-regexp`, Ubuntu/glibc 2.39; oracle SHA `92b211f7a6422d621d4ab1330739b3dbe520283c5e628b848f36f8c29b9be7ea` verified. Image `bad63142bf60230bcf147c864f57ce9b51d982a49bedd661456d1f9698734032`.
- All builds and timings on kasumi with `flock /home/mfwolffe/lanes/kasumi-cores-4-7.lock` and physical CPUs 4–7. A lane-local taskset shim maps inherited 0–3 test commands to 4–7; reports record actual affinity.
- One warmup and eleven interleaved samples per engine; output drained through pipes, full stdout hash/status/stderr checked. Later phases interleave before/candidate/GNU in one run. Early copied-source experiments retain their actual remote HEAD field; `phase-source-map.json` binds their binaries to local commits/retained patches rather than pretending those trees were clean.

## Evidence index

### Commits

- 45c53f0: Record ct06 speed prediction
- a5093d6: Reject dense specialization at 298.478 to 301.179 ms
- 5247bec: Index trie roots: fixed-10 7.607 to 4.723 ms
- ef0bffc: Reject single skips: word 8.854 to 9.373 ms
- 8532e61: Skip unused history regions: binary 20.352 to 19.066 ms
- ee2a5f6: Split exact unions: alternation 300.304 to 152.987 ms
- 3c56d91: Unroll byte scans: literal 105.197 to 89.636 ms
- 41ca3a2: Skip exact spans: only-matching 42.174 to 10.818 ms
- 02b3356: Reject empty DFA lever at 68.885 to 69.305 ms
- 93b1cde: Format retained speed changes
- 2541c53: Record physical cores and interleaved control evidence
- 5300fef: Initialize span proofs in direct regex test fixtures
- 5ba0860: Refresh README for measured speed paths
- 5ce1381: Record read controls: sc72 45.719 versus chunk 7.630 ms
- 03a17a7: Record three restored local plants
- 6fc5589: Record green acceptance and the sixteen-row paired table
- bd451ba: Name remaining M4 work without inventing surface blockers

### Acceptance

- Whole `tools/gate` GREEN at source head `5300fef0427658615a92e939a2587b8c00c150c8`, 2026-10-26 17:24:53–17:41:42Z, exit 0, SKIP=0. All **190** accepted source/harness/test hashes match the final branch; subsequent commits are README/evidence only. `acceptance.log`, `accept-inputs.json`.
- 29 checked tests and root native/lupin controls pass; engine gate 19 units plus malformed/generated/projection/cost controls. Native, release, deterministic static and original-VM matrices each retain **48,305 cases: 47,514 agree, 790 exact reviews (18 upstream-blocked), one environment, zero unapproved differences/not-yet**.
- Locale-free static replay GREEN, exit 0 at 17:44:13Z. Used existing Ubuntu image `8ba042cb51b75ddc0c1c801a547144363c50844429e9df64ba6d15b8f0eff648`, no locale files and no package installation. Capture remains `d635cc1dde428cdb7437e7680d1d8c457901ad2a85de801684daac25062daeae`; static ELF built twice at `8800d06c88f813022e14b692a9c3b689bd05ca212531315e98fa026beb9cb2f6`.
- Five 2 GiB memory peaks: **2900 / 2812 / 2896 / 4192 / 2844 KiB**, all below unchanged 32,768 KiB. `memory-final.json`.
- Three local plants, then restored green: `plant-root.log` → `RED fixed-prefix-pattern`; `plant-history.log` → `RED history-leading-context`; `plant-longest.log` → `RED exact-span-longest`. `plants.json` hashes each mutation; no CI plant dispatched for this module footprint.
- Honest first whole-gate red: two direct test fixtures omitted the new span-proof field; fixed in 5300fef. `accept-first.log` and its input manifest retained.
- Rejected experiments retained: dense specialization 298.478→301.179 ms on alternation; indexed single skip despite other gains because paired word regressed 8.854→9.373 ms; empty-DFA allocation 68.885→69.305 ms on recursive. No rejected patch is applied.
- `final-paired.json` binds saved baseline and accepted binaries and hashes sources. Every retained lever has its numbers and decision file. Final ranges show no row wholly slower than its paired baseline range. Existing sixteen regression ceilings pass; they are not M4 waivers.
- README read and refreshed. `prune.txt` lists only ct06 downloads, generated corpora/builds and obsolete controls; retained compiler/runtime, oracle, final binaries and evidence. No other lane's files touched.

### Final performance table

All medians in **milliseconds**, eleven interleaved before/after/GNU samples on the same container and cores. Ratio = after/GNU; boolean is the independent M4 bar.

| Workload | Before ms | After ms | GNU ms | Ratio | M4 |
| --- | ---: | ---: | ---: | ---: | --- |
| literal | 114.244 | 94.360 | 11.297 | 8.352 | false |
| class | 113.337 | 94.736 | 11.549 | 8.203 | false |
| alternation | 303.359 | 141.785 | 10.495 | 13.510 | false |
| backreference | 81.432 | 80.518 | 38.563 | 2.088 | false |
| ignore-case | 9.434 | 8.033 | 2.856 | 2.813 | false |
| word | 9.798 | 7.915 | 4.334 | 1.826 | true |
| count | 13.150 | 10.969 | 2.754 | 3.983 | false |
| list | 0.478 | 0.482 | 0.316 | 1.528 | true |
| only-matching | 46.818 | 11.112 | 10.349 | 1.074 | true |
| invert | 13.195 | 11.056 | 2.795 | 3.955 | false |
| binary | 21.340 | 19.246 | 5.815 | 3.309 | false |
| recursive | 72.258 | 68.508 | 6.598 | 10.383 | false |
| utf8-fold | 139.426 | 106.210 | 32.098 | 3.309 | false |
| fixed-1 | 4.363 | 4.046 | 1.377 | 2.938 | false |
| fixed-10 | 6.062 | 4.470 | 1.422 | 3.145 | false |
| fixed-1000 | 8.170 | 6.673 | 1.648 | 4.048 | false |

### Issue drafts and recommendations

No issue filed or closed. These texts are ready for the orchestrator; A extends the existing open wolf-std#89 rather than duplicating it. B is distinct from closed wolf-std#94. C deliberately does not invent a language-surface blocker.

Issue text A — append to wolf-std#89 (OPEN), or a linked implementation issue
Title: Bounded allocation-free byte and candidate searches for scent M4

scent ct06 retains scalar unrolled delimiter scans and scalar indexed literal searches. Its remaining literal/class/alternation, ignore-case, count/invert/binary, UTF-8-fold and fixed-pattern misses are named in the attached eleven-pair table. A bounded bytes.find_byte(buffer, start, end, byte) primitive, and a measured find-any/subslice companion, would let scent reject spans without copying a list window or scanning each byte through a generic loop. Preserve arbitrary bytes, exact offsets, no overread, and record-boundary rules. Do not replace the 98,304-byte read/binary semantics.

A separate same-container, same-cores 64 MiB control measures current Wolf chunk-read at 7.630 ms and read+scalar-scan at 27.983 ms. The original C black-box API control measures reused reads at 6.094 ms and reads+memchr at 7.396 ms. Scan increments are 20.353 versus 1.302 ms (19.052 ms opportunity). These are measured opportunities, NOT a promise that one primitive closes every remaining 2x miss. Production scent remains pure wolf; the C adapter is diagnostic only. Acceptance: checked/native/lupin boundary and arbitrary-byte tests, 11-sample controls, and unchanged scent conformance/memory gate. See read-cost.json, tools/read-probe/reference.c and the final performance table.

Issue text B — wolf-lang, with a wolf-std wrapper follow-up
Title: True read-into-existing-buffer primitive, without allocating then copying a chunk

wolf-std#94 is CLOSED, but sc72's wrapper at 78b9d3c allocates via read_chunk and copies into the retained list. In ct06's pinned Ubuntu/GNU container on locked CPUs 4-7, eleven-sample 64 MiB read-only medians are current chunk-read 7.630 ms, sc72 read_into 45.719 ms (5.99x), and the original reusable C read control 6.094 ms. 684 builtin calls including EOF allocate 67,141,392 region-ledger bytes for 67,108,608 input bytes. No syscall-trace claim is made.

Request a native checked-safe operation reading into initialized caller-owned byte storage, returning a count without a fresh intermediate List or element-wise copying. Preserve partial-read, EOF/error and buffer-ownership semantics; expose it through std without changing scent's pin until measured. The read-only opportunity is 1.536 ms per 64 MiB in this control: it cannot honestly explain all M4 misses. This is a distinct zero-allocation requirement, not a claim that the closed wrapper issue was never implemented. Re-run allocation-ledger, eleven-sample timing, checked/native/lupin and bounded-stream tests before adoption.

Issue text C — scent (not an invented compiler blocker)
Title: Finish the per-record and per-file M4 misses with controlled follow-on levers

The ct06 table still has M4 misses after measured wins. In particular, no evidence establishes that the backreference and recursive rows require a new language surface. Current source leaves opportunities for a count-only record path, per-file workspace reuse and conservative constant-capture backreference proofs. The single-pattern skip draft improved count/invert/binary/recursive/fixed-1 but was rejected because the interleaved word control regressed beyond its measured range (8.854 -> 9.373 ms). Skipping empty-program DFA allocation also failed its recursive target (68.885 -> 69.305 ms). Keep those failed drafts as counterfactuals, not production code.

Use the same sixteen workloads, eleven samples, four-core lock, before/candidate/GNU interleaving and byte-identical tuples. Retain each lever only if its target improves and no other row regresses past the predeclared noise band. Keep the 32,768 KiB memory gate and every exact GNU review unchanged. Do not label an unoptimized scent path "impossible in wolf" without a separate isolating witness. The upstream APIs in A/B are enabling proposals, not certified blockers for every row. M4 remains open until each workload is within 2x, independent of the regression ceilings.

R-ct06-1: recommend retaining the measured wins with M4 explicitly unmet and all remaining rows named; implemented, no waiver.
R-ct06-2: recommend retaining the current std pin instead of adopting the slower sc72 wrapper as a speed fix, and requesting the true primitive separately; implemented.
R-ct06-3: recommend keeping unproven surface limits as scent follow-on work rather than filing speculative compiler defects as established blockers; implemented by the split issue texts and explicit qualification. No ruling decided, no issue filed or closed.

## Done-when

- [x] Prediction committed before first change; all fifteen original misses mapped to named measured levers.
- [x] Eleven-sample controls, rejected drafts retained, full final table re-pasted.
- [x] Native/release/static/original-VM conformance, checked/lupin tests and engine gate green.
- [x] Unchanged 32,768 KiB memory gate; three named local plants red then restored green.
- [x] README refreshed, raw evidence/source bindings and exact prune list retained.
- [x] Issue texts and R-ct06-1/2/3 recommendations supplied; no ruling decided.
- [ ] All sixteen rows within 2× GNU: **M4 remains unmet**.
- [ ] Proven missing language surface for every remaining miss: **not established; do not misfile conjecture as a blocker**.
- [ ] GitHub PR tier green: one direct run-ID read after the final push, no CI wait; orchestrator owns the verdict.

Publication/run/audit metadata follows after opening at this final head.

### Publication and audit

Final head: `bd451ba9404ce2cb46afa7955370c3d5bc213916`.
Sole direct run-ID read after the push: **40372345968**, `in_progress`. No CI wait or label.

The required audit was run **once** at this head. Its last line was:

`AUDIT FAIL (footprint: module)`

It reported pending PR CI/no green tier, a shortened cross-repository issue reference, and the still-present Mac worktree. The issue reference has now been expanded to `wolf-std#94` and the clean, pushed Mac worktree has been removed. These two corrections were **not re-audited**, honoring the once-at-final-head instruction; the orchestrator owns the next audit and CI verdict. All footprint, ancestry, trailer, five-section, commit-reference and orphan checks passed in the recorded audit.

Additional post-audit prune: `/Users/mfwolffe/lanes/ct06/scent` (clean worktree, removed without force after final push). The remote clone `/home/mfwolffe/lanes/ct06/scent` is clean at the final head and retains the final binaries and evidence. Both owned local job markers are exit 0; no background acceptance job remains.

