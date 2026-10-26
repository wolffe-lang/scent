## Forbidden

No GNU grep, gnulib, glibc implementation/locale data, busybox or PCRE2 source read. Only specifications, permitted own-code references, UCD data and black-box oracle measurements informed the implementation. No dependency beyond wolf-std. No Mac builds, host package installation, labels, merges, tags, releases or issues filed. Execution used the lane-owned pinned Ubuntu container on kasumi CPUs4–7 under the shared core lock, with core dumps disabled. Linux archives were independently downloaded and hashed twice on the Mac, never extracted/executed there. No attribution trailers or edits to the planning repo or personal configuration.

The wrapper prohibits Markdown report files; this PR body is the five-section report, with evidence under `notes/ct04-evidence/`.

## Inputs verified

- Baseline `143bf55`; unchanged wolf0.2.35 / lupin0.1.56 / std `2386522eb059cca5a84108562c2c0a0e72345d34` pin. Independent double archive digests: `notes/ct04-evidence/toolchain-digests.txt`.
- Oracle GNU3.12, `--disable-perl-regexp`, glibc2.39, binary SHA256 `92b211f7a6422d621d4ab1330739b3dbe520283c5e628b848f36f8c29b9be7ea`; signature-verified unseen build from `scent-oracle.toml`.
- UCD15.0.0/15.1.0/16.0.0, Unicode licence and twice-read digests in `ucd/MANIFEST`. Own-code references: yew's generator/property parsers and byte-window decoder, cited in the source headers.
- Initial locale probe lists only C, C.utf8 and POSIX. First nonempty LC_ALL > LC_CTYPE > LANG wins. Absent en_US.UTF-8 falls back to C in GNU, while scent's own tables honor the UTF-8 codeset (R-ct04-1, separate environment class).

## Prediction

Committed before implementation at `2471eb3` (`notes/ct04-evidence/prediction.txt`). Predicted15.0.0; measured15.1.0 wins. Predicted tiny override counts; actual2,732 class memberships across707 code points. Predicted two non-simple fold classes; GNU first disproved equivalence itself, and the consistent closure differs from UCD simple folding in nine components/24 code points. Predicted absent en_US fallback and empty-variable precedence correctly. Predicted dot rejects errors; GNU's context-dependent leaked spans required the published consistency rule. Predicted10,500 UTF-8 rows; actual38,706. Original C9478 agreements/120 exact reviews stay unchanged; the one former explicitly UTF-8 refusal now agrees.

## Evidence index

Implementation chunks:
- `07ccd7f`: locale precedence/aliases and selection units.
- `c4c9616`: generated encoding-error probes and decoder.
- `8be196f`: exhaustive classes, directed-fold measurements and wolf generator.
- `500c0dc`: UTF-8 matching, byte spans, binary output and consistency policy.
- `9e90418`: inherited/UTF-8 matrices, exact review classes and reference replay.
- `442d475`: isolated C byte VM and original fixed matcher layout; removes the measured first-draft performance regression.
- `8dad9a6`: replay tamper guards, file-list controls and alias reproducer.
- `0386e7c`: exhaustive malformed-byte brackets and uppercase range ordering.

### Tables and semantics

Every1,112,064 scalar was measured for12 POSIX classes and word membership, using both counts and member streams. NUL requires `-a`; LF is measured separately under `-z`, since LF cannot be a one-character LF-delimited record. The measured winner is15.1.0. Overrides by class: alpha670, alnum670, digit0, upper31, lower4, space4, blank3, punct673, cntrl2, graph3, print2, xdigit0, word670. Version totals:15.0=5,857;15.1=2,732;16.0=27,149. Every member/override is committed under `tests/fixtures/ctype/`.

The all-scalar measurement issued3,668 fold queries and completed in13.199s launcher wall time; its final progress marker was12.6s. The original symmetry assertion then stopped, correctly: nine historic Cyrillic sources have18 asymmetric directed edges. The entire raw query log is retained. UCD simple upper/lower composition needs42 source-pattern overrides/49 membership edits to reproduce2,938 measured nonidentity edges. The108 cross-engine controls agreed. Ruling122 then requires their symmetric/transitive closure, adding20 directed edges, consistently for selection and output. Nine components differ from UCD15.1 simple folding: dotless I, Kelvin, Angstrom, sharp S, theta/Ohm symbols, two Greek dialytika/tonos–oxia pairs and ST ligatures. Exact sets: `fold-simple-comparison.json`; sigma/Cherokee/Georgian agree.

Under `-i`, upper and lower each equal alpha exactly (139,057 members), not their union. Valid non-ASCII range/collation endpoints are refused as GNU measures; invalid single bytes retain byte-valued endpoint behavior. The additional4,680 bracket rows cover every rejected byte128–255, both syntaxes and case modes.

### Matrix, consistency and locale-free execution

Final acceptance totals:48,305 CLI cases =47,514 agreements +790 exact reviews +1 environment difference; zero unapproved differences/not-yet. Reviews comprise772 published differences and18 upstream-blocked rows. Of published reviews,550 are `gnu-inconsistent` under122:480 fold-selection rows and70 strict-dot rows. Original C and UTF-8 inherited reviews remain separately pinned; no blanket waiver or output normalization was added.

R-ct04-3/#122: GNU does not select isolated `ᲀ` for pattern `В`, but `-o` admits it beside a valid match on `ᲀВ`. Plain/-c/-l agree on line selection; only spans expose the extra character. Scent consistently matches the closure. R-ct04-4/#122: dot never admits a nonscalar, even when GNU leaks its span beside a valid character. Consistent GNU legacy4/5/6-byte negated-class/literal behavior is matched, not waived. Minimal pairs and exact tuples are in `utf8-stop-witnesses.json`; the combined bug-grep report is drafted, not sent.

Final gate/posture evidence: `notes/ct04-evidence/acceptance.log`, exit0, 2026-10-24T22:36:41.262121+00:00 through 2026-10-24T22:52:33.917372+00:00. Source hashes in `final-run.json` match every final source byte. The full gate includes24 wolf tests, native/lupin root units, checked fallback enforcement, malformed/generated/projection/cost engine gates, native/release/static matrices, deterministic static build and2GiB memory acceptance.

Deleting locale files also makes GNU fall back to C. Therefore PAX posture replays raw GNU tuples captured only by a green live static matrix, bound to the full oracle pin and every case hash; scent itself runs with no locale data/LANG. Changed pin, changed case, missing case and changed output each fail; unchanged replay passes. Final static/capture digests: static `3f3df8f6725624be7b46223fc82f95592108f0f7a4e47dcfd107d3040f07265a` (14,998,640bytes, built twice identically); capture `d635cc1dde428cdb7437e7680d1d8c457901ad2a85de801684daac25062daeae`. Final2GiB peak RSS is2676KiB (-F -c) and2708KiB (-F -n).

### Performance and plant

`performance-table.txt` and raw JSON retain the failed first draft and interleaved correction. The initial C regex regression was7–22%; an outer dispatch to the unchanged byte VM removes it. One warmup plus three paired baseline/candidate runs: all non-improving rows have overlapping ranges; the only non-overlap is a5.81% speedup. Final fixed-layout control is+1.67% with overlap. First UTF-8 row:67,061,760bytes, `-F -i -c É`, scent0.219441s / GNU0.031021s =7.07x; recorded, not gated until M4.

CI plant `fd4c1ca`, PR#9, run40135907331 was red in linux's **Regenerate Unicode tables and compare exhaustive fixtures** step: one changed byte caused `cmp` to fail at char195,line6. PR#9 is closed unmerged. `plant-ctype-ci.log` retains the direct run log.

### Issues and follow-ons

File **wolf-interp**: local module aliases fail to resolve in lupin0.1.56. Two-file `use math as renamed; renamed.value()` prints42 under native and checked wolf, but lupin exits4 with `unsupported: renamed.value does not resolve`. Draft and minimal sources: `wolf-interp-alias-issue.txt`, `alias-witness/`; no issue filed. Existing argv/byte-path issues are not duplicated. The GNU context-leak report awaits a human send.

M4/ct05 sketch: bounded lazy DFA, locale/scalar predicate partitions, consistent-fold superset prefilters, scalar-aware many-pattern fixed search, byte offsets throughout, bounded read buffers/cache and the2x GNU gate. Preserve separate C execution and never reproduce GNU's two-matcher leakage. Full sketch plus px scent-M3 static-pin/typed-session follow-on: `m4-contract.txt`; numeric px lane assigned by the orchestrator. No PAX deployment claimed.

## Done-when

- [x] Locale precedence and aliases measured; environment difference separated.
- [x] All scalar classes/fold candidates measured; UCD generator and fixtures checked.
- [x] UTF-8 engine/output, error classes and inherited matrices implemented.
- [x] Malformed bracket expansion:4,680 live comparisons agree.
- [x] C performance correction measured against exact143bf55 baseline.
- [x] CI one-byte plant red by run id and closed unmerged.
- [x] Replay pin/case/output tamper guards exercised.
- [x] Final full gate and plain-container posture recorded.
- [x] Final CI first status and lane-audit recorded below; no lane CI wait or label.

README read and refreshed. The macOS field leg remains CI's non-blocking measurement, not a locally claimed result: expect additional UTF-8 differences from its libc/locale support, with exact tuples retained by the field harness. The orchestrator watches that final run.

After audit, prune only lane-generated target outputs/corpora and the clean plant worktree; preserve logs, static sums, reference capture and source until evidence is secured. Lane-owned paths: kasumi `/home/mfwolffe/lanes/ct04/`; Mac `/Users/mfwolffe/lanes/ct04/`. No shared/global prune.


Final head: `7f6651d68468efd8b5e9ba2dff358a841107b98c`.
The sole direct CI status read found run **40140674859**, `in_progress`.
Mandatory audit last line: **AUDIT FAIL (footprint: cross-cutting)**.
Its only holds are the in-progress run/no completed green tier and the
intentionally absent full-matrix label. Footprint, ancestry, trailers,
five-section report, plant evidence and all11 cited SHAs passed. The
orchestrator adds the label and watches CI; no CI-green claim is made.

