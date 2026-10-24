# scent

A byte-oriented `grep` in [wolf](https://github.com/wolffe-lang/wolf-lang),
compared with GNU grep 3.12 configured `--disable-perl-regexp`.

| Platform | Coverage |
| --- | --- |
| Linux x86-64 | Ubuntu 24.04 oracle; native, release and deterministic static builds |
| macOS arm64 | Builds and units; non-gating Homebrew grep field comparison |
| PAX | Static builder and locale-free acceptance; OS pinning is separate from the locale-free binary acceptance |

## Status

C-locale basic regular expressions (the default, `-G`), extended regular
expressions (`-E`) and fixed strings (`-F`) are connected to the full M1
selection/output interface. This includes backreferences, classes, GNU
assertions, intervals, case folding, word/whole-line matching, context,
prefixes, spans, counts, file lists, binary policies and bounded streaming.
`-r`/`-R` walk directory entries in host order without sorting, with
command-line versus walked symlink rules, directory/device policies and
ordered include/exclude globs. `--color=always|never|auto`, `GREP_COLORS`
and the deprecated `GREP_COLOR` warning are supported. `-P` gives the
configured GNU build's refusal. C and UTF-8 matching are supported, including
multibyte patterns, classes, word boundaries, backreferences and byte-exact
spans. C-locale `-i` folds ASCII only; UTF-8 uses generated, measured tables.

The generated CLI matrix has **5,072 cases**: 40 option rows × three
syntaxes × seven pattern families × six input forms, plus 32 source and
diagnostic cases. Separate CLI rows cover the original 958-case corpus,
150 reviewed-family cases, 18 wrapper cases and nine context/span joins.
The engine also gates 20,000 generated pattern–line pairs per syntax,
exhaustive short malformed patterns, and bounded regular/backreference costs.

The M2 generator adds **3,392 cases**: 2,000 shared-tree walk/filter rows,
18 edge and five self-output rows, 1,152 original colour/environment rows,
120 glob-syntax rows, and 97 additional byte-pattern, tty, colour-edge,
reviewed-gap and UTF-8 locale rows. The complete CLI matrix reports
**9,478 C-locale agreements + 111 published differences + 9 upstream-blocked**.
The former explicit UTF-8 refusal is now an agreement. A further **38,706
UTF-8 cases** include every inherited case and generated scalar, encoding-error
and consistency witnesses. The complete matrix has **48,305 cases**:
**47,514 agree, 772 published differences, 18 upstream-blocked, one environment
difference, zero unapproved differences and zero not-yet rows**. Of the published
differences, 550 cover the two UTF-8 consistency rules below: 480 case-fold
rows and 70 dot-span rows.
The reviewed cases are not counted as agreement. Input and pattern-file
bytes remain arbitrary bytes; non-UTF-8 filesystem names have the exact
upstream-blocked witness below, not a locale exception.


## Locale and Unicode

The first nonempty `LC_ALL`, `LC_CTYPE`, then `LANG` selects the locale.
A dot-delimited `UTF-8` or `utf8` codeset (case-insensitive, optionally followed
by `@modifier`) selects UTF-8 mode; everything else selects C. No locale files
are consulted. Thus `en_US.UTF-8` works even when that name is not installed.
The oracle image installs only C, C.UTF-8 and POSIX: its fallback to C for
`en_US.UTF-8` is one separately counted **environment** difference, not a
matching exception. The normal matrices explicitly select C or C.UTF-8.
[The measured alias and precedence table](docs/MAP.md#locale) gives details.

Unicode 15.1.0 is the closest of 15.0.0, 15.1.0 and 16.0.0 to the pinned
oracle. The wolf generator derives classes from checked-in UCD files and
applies 2,732 explicitly listed class-membership overrides across 707 code
points. Every scalar was measured for all twelve POSIX classes and `\w`.
The original per-class counts, version comparisons, overrides and 3,668
case-fold queries are retained in [`tests/fixtures/ctype/`](tests/fixtures/ctype/).
`tools/check-ctype-regen` regenerates the tables and checks the fixtures;
CI never silently substitutes its host's Unicode version.

Under `-i`, `[[:upper:]]` and `[[:lower:]]` each become `[[:alpha:]]`,
including uncased letters and the oracle's non-ASCII digit members. Numeric
`[[:digit:]]` remains ASCII. Ordinary multibyte bracket members work; the
pinned build rejects valid non-ASCII character range endpoints and
collating/equivalence atoms with `Invalid collation character`, and scent does too. Rejected single bytes remain byte-valued range
endpoints; 4,680 additional malformed-bracket comparisons check every
byte from0x80 through0xff under both syntaxes and case modes.

### Case matching stays consistent

The pinned GNU build's case relation is not symmetric for nine historic
Cyrillic letters: `ᲀ` matches `В` and `в`, but `В` does not select an isolated
`ᲀ`. Adding `В` elsewhere on the same line makes GNU `-o` print both letters.
Scent uses the symmetric, transitive closure of the measured relation for
selection and spans alike, so all three match in either direction. Twenty
additional directed edges are covered by exact, published consistency rows.
The generator starts from UCD simple upper/lower compositions, applies 42
source-pattern overrides (49 membership edits), then computes that closure.
Nine connected components (24 code points) differ from UCD15.1 simple case
folding: dotless I, Kelvin, Angstrom, sharp S, theta/Ohm symbols, the two
Greek dialytika/tonos–oxia pairs, and the two ST ligatures. Dotted I remains
separate; Greek sigmas, Cherokee and Georgian follow the measured simple
classes. [Exact component sets](tests/fixtures/ctype/fold-simple-comparison.json)
are retained. No full case expansion or normalization is performed.

### Encoding errors stay bytes

Offsets, `-o`, colour and output always use original byte boundaries. Dot
never matches a surrogate encoding, an overlong form or a value above
U+10FFFF. GNU sometimes emits such a dot span only beside another valid
match; scent rejects it consistently. These 70 exact differences are
published, not silently counted as agreement. Where GNU is consistent,
scent follows it: non-overlong legacy four-, five- and six-byte values up
to 0x7fffffff can match a negated class or a literal and are not binary-output
errors, but they are not Unicode scalars and never match dot. Other rejected
bytes remain available to literal byte patterns. Binary suppression follows
the bytes actually being printed, so `-o` can print valid spans from an
otherwise invalid record. The [draft bug report](notes/ct04-evidence/gnu-report-utf8-context.txt)
contains the minimal examples; it has not been sent.

## Install and build

No release is published yet. `packaging/scent.rb` and `packaging/PKGBUILD`
are **drafts** for a future `v0.2.0` source tag: their release digest must be
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
`--field` reports distribution differences without gating. It probes raw-name
support once on the corpus filesystem; APFS's rejected byte-FF name is
`field-unavailable` with a recorded reason, not a harness crash. Two exact
Darwin argv-decoding aborts are [reviewed](tests/field-divergences.json) as
`upstream-blocked`, with their
full witnesses retained; only the numeric panic PID varies. Stale reviews
remain fatal. [Runtime issue draft](notes/ct03-evidence/wolf-lang-macos-argv-issue.txt).
`cmp` compares
stdout, stderr, exit status and remaining stdin. Help/version are scent's
own prose; those two actions compare stream shape and status, with exact
stderr (including wrapper warnings).

Every reviewed difference in [`tests/divergences.json`](tests/divergences.json) and
[`tests/m3-divergences.json`](tests/m3-divergences.json) locks the complete case identity and both result tuples. A new input,
changed output, or vanished difference fails the gate. The only dynamic
field is the numeric runtime PID in the two byte-argument witnesses, repeated in each
locale.
`tools/oracle-review-test` rejects nondigits there and changes to every
other byte. No other output is normalized.

`tools/mkscent OUTDIR` builds the static ELF twice and prints equal digests,
size and stripped size. `tools/pax-posture` runs the whole suite in a plain Ubuntu container without
locale data or `LANG`; Python is only the test coordinator. Removing locale
files also makes GNU fall back to C, so this leg replays the exact GNU tuples
captured by a green live static matrix, rather than calling a C-locale oracle
under a UTF-8 name. Captures bind the full oracle pin and every case hash;
stale or missing captures fail. The static live run regenerates the capture
at the same pin before each posture run. The ct04 reference capture
SHA256 is `d635cc1dde428cdb7437e7680d1d8c457901ad2a85de801684daac25062daeae`;
[the retained capture](notes/ct04-evidence/pax-reference.json.gz) and
[run/source manifest](notes/ct04-evidence/final-run.json) record its provenance. The Linux PR gate includes both compiler tiers, units,
all CLI cases, engine costs, deterministic static builds, locale-free
acceptance and the 2 GiB streaming-memory gate (below 32 MiB peak RSS).
`tools/measure` records three-run medians on 256 MiB for `-F`, `-G` and `-E`;
the same measurement includes `-r -F -c` over 10,000 files. Speed is
recorded, not gated, until M4. Full CI adds the macOS field leg.

## Published differences

These deliberate differences keep matching and file-selection rules consistent.
The witness bytes use `\0` for NUL; ordinary output ends in newline.
The complete individual cases and exact answers are in the two manifests above.

| Rule | Minimal witness | GNU 3.12 | scent | Why |
| --- | --- | --- | --- | --- |
| Whole-word, leftmost-longest | `-E -a -o -b -w '.{1,2}'`, four spaces then `ab` | `0:  \n4:ab\n` | `0:  \n2: \n4:ab\n` | Keep the valid shorter whole-word span GNU's retry omits. BRE is equivalent. |
| `**` means `*` | `-E` with the double-star pattern below, on `a` | No output, status 1 | `a\n`, status 0 | Replacing either `**` with `*` restores GNU's empty-capture path; POSIX leaves adjacent duplication undefined. |
| Never cross records | Pattern-file bytes `x\0y\n`, `-F -z`, input `x\0y\0` | `x\0y\0`, status 0 when in one read | No output, status 1 | GNU `-G`/`-E`, `-F -w` and cross-read `-F` already reject it. Input record boundaries must not depend on read placement. |
| Explicitly named sockets obey `-Dskip` | Create a Unix-domain socket named `socket`; `grep -Dskip x socket` | stderr `grep: socket: No such device or address\n`, status 2 | Empty streams, status 1 | Follow the documented silent skip, as GNU already does for a walked socket and an explicit FIFO. Exact cases: `m2-socket-skip`, `m2-edges-11`; [witness](notes/ct03-evidence/witnesses.json). |

The double-star command is literal (the alternation bar is not escaped):

```sh
printf 'a\n' | grep -E '(A**|.)(a)\1**'
```

The CLI family rows are **94 agree + 56 reviewed** (22 word-span and
34 double-star differences). The 216 NUL-pattern rows are **164 agree +
52 reviewed**; the original two additional NUL witnesses add one agreement and one
reviewed difference under the same rule. The
98,304-byte read-boundary witness is checked as agreement, not waived.
A short double-star bug report is drafted in
[`notes/ct02-evidence/gnu-double-star-report.txt`](notes/ct02-evidence/gnu-double-star-report.txt);
it has not been sent. The socket report is also drafted, not sent, at
[`gnu-report-Dskip-socket.txt`](notes/ct03-evidence/gnu-report-Dskip-socket.txt).

### Blocked upstream: invocation names, byte argv and byte paths

These nine C-locale witnesses, also repeated under UTF-8, are scent/runtime
gaps, not GNU quirks. Each row is executed
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
| `m2-upstream-byte-name`: ASCII argv `-r x tree`, file `tree/<FF>` contains `x\n` | stdout hex `747265652fff3a780a`, empty stderr, status 0 | Empty stdout; stderr `grep: directory entry is not UTF-8\n`, status 2 | wolf-lang#687, #912: listing exposes byte names, but open/stat paths require UTF-8. [Exact witness](notes/ct03-evidence/witnesses.json). |

The two byte-argument rows have no stdout. Their full stderr is fixed in
the manifest, with just `{pid}` typed as one or more ASCII digits; status
is abort (`-6` in the subprocess harness):

```text

thread '<unnamed>' ({pid}) panicked at /rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/std/src/env.rs:876:51:
called `Result::unwrap()` on an `Err` value: "\xFF"
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
fatal runtime error: failed to initiate panic, error 5, aborting
```

Until those builtins ship, diagnostics and `--help`'s usage line
use the fixed invocation name `grep`; full-path invalid-option
prefixes and alternate invocation names differ. No `os_exe` basename is
substituted: it would be wrong under symlinks. `/bin/grep` can be a symlink
to scent without a private name-override option. Raw invalid-UTF-8 argv can abort; use pattern files
for arbitrary pattern bytes. Retirement requires replaying these witnesses
at the new pin, not deleting them without a check. The byte-filename gap
requires filesystem byte-path APIs (#687/#912), not merely byte argv or
UTF-8 locale support. `--exclude-from` itself accepts arbitrary byte
patterns, trims trailing C-locale whitespace and preserves rule order.

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
