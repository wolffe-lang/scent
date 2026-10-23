# scent

A byte-oriented `grep` in [wolf](https://github.com/wolffe-lang/wolf-lang),
compared with GNU grep 3.12 configured `--disable-perl-regexp`.

| Platform | Coverage |
| --- | --- |
| Linux x86-64 | Ubuntu 24.04 oracle; native, release and deterministic static builds |
| macOS arm64 | Builds and units; non-gating Homebrew grep field comparison |
| PAX | Static builder and locale-free acceptance; OS integration is next |

## Status

C-locale basic regular expressions (the default, `-G`), extended regular
expressions (`-E`) and fixed strings (`-F`) are connected to the full M1
selection/output interface. This includes backreferences, classes, GNU
assertions, intervals, case folding, word/whole-line matching, context,
prefixes, spans, counts, file lists, binary policies and bounded streaming.
`-P` gives the configured GNU build's refusal. Recursion and terminal colour
are M2; UTF-8 locale semantics are M3. C-locale `-i` folds ASCII only.

The generated CLI matrix has **5,072 cases**: 40 option rows × three
syntaxes × seven pattern families × six input forms, plus 32 source and
diagnostic cases. Separate CLI rows cover the original 958-case corpus,
150 reviewed-family cases, 18 wrapper cases and nine context/span joins.
The engine also gates 20,000 generated pattern–line pairs per syntax,
exhaustive short malformed patterns, and bounded regular/backreference costs.

The exact reviewed cases below are not counted as agreement. Eight runtime
gaps are separately marked upstream-blocked; only 12 recursion/colour cases
remain not-yet. All input and pattern-file bytes remain arbitrary bytes.

## Install and build

No release is published yet. `packaging/scent.rb` and `packaging/PKGBUILD`
are **drafts** for a future `v0.1.0` source tag: their release digest must be
filled before use. They build with the pinned compiler, not a moving wolf
package, and do not replace the system grep. Optional compatibility names
are installed in a separate directory.

```sh
tools/fetch-toolchain
tools/build --all
tools/check-test
```

The pin is wolf **0.2.35**, paired lupin **0.1.56**, and bundled wolf-std
`2386522eb059cca5a84108562c2c0a0e72345d34`. Archives are checked by digest;
complete runtime/compiler pairs stay together. Build on a compatible host,
not with an arbitrary compiler from PATH.

`wrappers/egrep` and `wrappers/fgrep` are shell scripts requiring `/bin/sh`.
Place them beside a `grep` link to scent. They emit GNU 3.12's measured
obsolescence warning on stderr, even with `--help`, and prepend `-E`/`-F`.
A later conflicting syntax flag is an error, not an override.

## Acceptance

```sh
tools/in-container tools/gate
tools/pax-posture
```

The oracle is a signature-verified release-tarball build in pinned Ubuntu
24.04/glibc 2.39, never the host's distribution grep. `tools/oracle --only
NAME` selects exactly one witness; explicit glob selectors are supported.
`--field` reports distribution differences without gating. `cmp` compares
stdout, stderr, exit status and remaining stdin. Help/version are scent's
own prose; those two actions compare stream shape and status, with exact
stderr (including wrapper warnings).

Every reviewed difference in [`tests/divergences.json`](tests/divergences.json)
locks the complete case identity and both result tuples. A new input,
changed output, or vanished difference fails the gate. The only dynamic
field is the numeric runtime PID in the two upstream-blocked panic rows.
`tools/oracle-review-test` rejects nondigits there and changes to every
other byte. No other output is normalized.

`tools/mkscent OUTDIR` builds the static ELF twice and prints equal digests,
size and stripped size. `tools/pax-posture` runs the whole byte suite in a
plain Ubuntu container without locale data or `LANG`; Python is only the
test coordinator. The Linux PR gate includes both compiler tiers, units,
all CLI cases, engine costs, deterministic static builds, locale-free
acceptance and the 2 GiB streaming-memory gate (below 32 MiB peak RSS).
`tools/measure` records three-run medians on 256 MiB for `-F`, `-G` and `-E`;
speed is recorded, not gated, until M4. Full CI adds the macOS field leg.

## Published differences

These are deliberate consistency choices, approved as rulings #115–#117.
The witness bytes use `\0` for NUL; ordinary output ends in newline.
The complete individual cases and exact answers are in the manifest above.

| Rule | Minimal witness | GNU 3.12 | scent | Why |
| --- | --- | --- | --- | --- |
| #115: whole-word, leftmost-longest | `-E -a -o -b -w '.{1,2}'`, four spaces then `ab` | `0:  \n4:ab\n` | `0:  \n2: \n4:ab\n` | Keep the valid shorter whole-word span GNU's retry omits. BRE is equivalent. |
| #116: `**` means `*` | `-E` pattern `(A**&#124;.)(a)\1**` on `a` | No output, status 1 | `a\n`, status 0 | Replacing either `**` with `*` restores GNU's empty-capture path; POSIX leaves adjacent duplication undefined. |
| #117: never cross records | Pattern-file bytes `x\0y\n`, `-F -z`, input `x\0y\0` | `x\0y\0`, status 0 when in one read | No output, status 1 | GNU `-G`/`-E`, `-F -w` and cross-read `-F` already reject it. Input record boundaries must not depend on read placement. |

The CLI family rows are **94 agree + 56 reviewed** (22 word-span and
34 double-star differences). The 216 NUL-pattern rows are **164 agree +
52 reviewed**; the original two additional NUL witnesses add one agreement and one
reviewed difference under the same rule. The
98,304-byte read-boundary witness is checked as agreement, not waived.
A short double-star bug report is drafted in
[`notes/ct02-evidence/gnu-double-star-report.txt`](notes/ct02-evidence/gnu-double-star-report.txt);
it has not been sent.

### Blocked upstream, retires at the pin that ships `env_arg0` / `env_args_bytes`

These eight are scent/runtime gaps, not GNU quirks. Each row is executed
and checked as an exact expected difference. Let `D(name)` be
`name: unrecognized option '--bad'\n`, and `U(name)` be
`Usage: name [OPTION]... PATTERNS [FILE]...\nTry 'name --help' for more information.\n`.
The invocation rows all use `--bad`, empty stdin, no stdout and status 2.

| Exact case name | GNU stderr | scent stderr | Upstream |
| --- | --- | --- | --- |
| `not-yet-argv0-diagnostic-0` | `D(/abs/path/grep) + U(grep)` | `D(grep) + U(grep)` | wolf-lang#899, #904 |
| `not-yet-argv0-diagnostic-1` | `D(./grep) + U(grep)` | `D(grep) + U(grep)` | wolf-lang#899, #904 |
| `not-yet-argv0-diagnostic-2` | `D(hound) + U(hound)` | `D(grep) + U(grep)` | wolf-lang#899, #904 |
| `not-yet-argv0-usage-0` | `D(/abs/path/grep) + U(grep)` | `D(grep) + U(grep)` | wolf-lang#899, #904 |
| `not-yet-argv0-usage-1` | `D(./grep) + U(grep)` | `D(grep) + U(grep)` | wolf-lang#899, #904 |
| `not-yet-argv0-usage-2` | `D(hound) + U(hound)` | `D(grep) + U(grep)` | wolf-lang#899, #904 |
| `not-yet-argv-bytes-0`: `-F`, byte FF pattern, empty stdin | No output/status 1 | Runtime panic below, abort | wolf-lang#406, #904 |
| `not-yet-argv-bytes-1`: `-F x`, byte FF filename | `grep: <FF>: No such file or directory\n`, status 2 | Runtime panic below, abort | wolf-lang#406, #904 |

The two byte-argument rows have no stdout. Their full stderr is fixed in
the manifest, with just `{pid}` typed as one or more ASCII digits; status
is abort (`-6` in the subprocess harness):

```text

thread '<unnamed>' ({pid}) panicked at /rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/std/src/env.rs:876:51:
called `Result::unwrap()` on an `Err` value: "\xFF"
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
fatal runtime error: failed to initiate panic, error 5, aborting
```

Until those builtins ship, ordinary `grep` file/regex diagnostics already
say `grep`; full-path invalid-option prefixes and alternate invocation
names differ. `/bin/grep` can be a symlink to scent without a private
name-override option. Raw invalid-UTF-8 argv can abort; use pattern files
for arbitrary pattern bytes. Retirement requires replaying these witnesses
at the new pin, not deleting them without a check.

## Design and sources

[docs/MAP.md](docs/MAP.md) describes the matcher seam and bounded buffers;
[docs/RE.md](docs/RE.md) describes the immutable regex and reusable workspace.
Input is never a whole-file string. Per-chunk regions release temporary
reads/output; only unfinished lines and requested context survive.

Sources are POSIX.1-2024, GNU grep documentation and black-box runs, plus
cited design references from the project's own ferp and yew engines.
GNU grep, gnulib, glibc regex, busybox and PCRE2 implementation sources are
never read. GNU is the behavioral oracle except for the explicit,
individually checked consistency decisions above.

## Licence

GPL-3.0-or-later (`LICENSE`), with the wolf Training Data Permission
(`LICENSE-TRAINING-DATA`).
