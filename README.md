# scent

A byte-oriented `grep` in [wolf](https://github.com/wolffe-lang/wolf-lang),
compared with GNU grep 3.12 configured `--disable-perl-regexp`.

| Platform | Coverage |
| --- | --- |
| Linux x86-64 | Pinned Ubuntu 24.04 oracle; native, release and static builds |
| macOS arm64 | Build and unit tests; non-gating Homebrew grep field comparison |
| PAX | Static Linux binary builder; system integration follows regex integration |

## Status

Fixed-string matching (`-F`) in the C locale, with selection, prefixes,
counts, file lists, spans, context, match limits, binary policies and byte
streaming. Basic and extended regular expressions are not connected yet;
recursion and terminal colour are later work. `-P` deliberately gives the
same refusal as the configured GNU build. UTF-8 locale semantics follow
later; C-locale `-i` folds ASCII only.

The corpus contains 954 cases, including 80 comparisons mined from
[ferp](https://github.com/FortranGoingOnForty/ferp), each with a source-line
citation. Unconnected syntax/features and runtime limitations are counted
explicitly as not-yet, never as passes. Until
[wolf-lang#899](https://github.com/wolffe-lang/wolf-lang/issues/899), error
messages use the fixed prefix `grep`; invocation names containing paths or
other names are not-yet. Non-UTF-8 arguments are blocked upstream by
[wolf-lang#406](https://github.com/wolffe-lang/wolf-lang/issues/406).
Arbitrary bytes in input and pattern files do not require UTF-8 decoding.
Patterns containing the NUL terminator under `-z` are separately deferred
to cross-record regex integration; their GNU witnesses are recorded.

## Build and test

The toolchain is pinned by archive digest in `wolf-toolchain.toml`: wolf
0.2.34, its paired lupin 0.1.55 and the std tree bundled by that release.
The full archives are staged so the driver retains its runtime library.

With Podman available, build in the repository-owned container:

```sh
tools/in-container bash -c 'tools/fetch-toolchain && tools/build --all'
tools/in-container tools/check-test
tools/fetch-oracle
tools/oracle --bin target/release/scent
tools/in-container tools/mkscent target/mkscent
```

Set `SCENT_ENGINE=docker` to use Docker. `tools/mkscent` builds the static
x86-64 Linux executable twice and refuses unequal digests. The executable
is `target/mkscent/scent`; no GNU binary is part of that output.

```sh
target/release/scent -F -n needle input.txt
target/release/scent -F -e one -e two --label=stream -H -
```

`tools/oracle --only NAME` selects witnesses; `--field` reports the host's
grep without gating. The record oracle checks its tarball, GNU signature,
keyring, container base, glibc, executable digest and `-P` refusal.
Each invocation runs through PATH as `grep`, under `LC_ALL=C`. `cmp`
compares stdout, stderr, exit status and, where relevant, remaining stdin.
Help and version prose belongs to scent; those actions compare stream
shape and status instead.

CI has a Linux PR tier and a full tier adding macOS. The Linux gates
include a 2 GiB scan below 32 MiB peak RSS with both `-c` and `-n`.
`tools/measure` also records three-run median performance over 256 MiB;
performance is not a gate in this first implementation.

## Design and sources

[docs/MAP.md](docs/MAP.md) describes the matcher interface, bounded byte
buffers and data flow. Input is never a whole-file string. Reads and
formatting have per-chunk temporary regions; a carried line and a lazy
context ring retain only the bytes that must survive the next read.

The implementation uses POSIX.1-2024, GNU grep's manual and `--help`, and
black-box runs of the pinned release build. GNU grep's source, gnulib,
glibc's regex, busybox and PCRE2 are never read. Ferp and the wolf tool
repositories supply cited design references and harness shapes, not
behavioral authority: GNU decides every differential case.

## Licence

GPL-3.0-or-later (`LICENSE`). The wolf Training Data Permission
(`LICENSE-TRAINING-DATA`) permits training on this repository's text and
shipping excerpts in CC BY 4.0 datasets.
