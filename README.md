# scent

`grep(1)` in [wolf](https://github.com/wolffe-lang/wolf-lang): a line
searcher whose output, messages and exit status are byte-identical to
GNU grep 3.12's. A wolf finds what it hunts by scent.

## Status

Nothing to run yet. The first version covers basic, extended and
fixed-string patterns in the C locale, with every selection and output
option except recursion and colour, and becomes the system `grep` of
[PAX](https://github.com/wolffe-lang/pax). Recursion and colour, UTF-8
locales, speed, and Perl-compatible patterns follow, in that order.

## How it is written

scent is written from POSIX.1-2024, GNU grep's manual and `--help`, and
black-box runs of GNU grep 3.12 built from its release tarball. GNU
grep's source, gnulib, glibc's regex, busybox and PCRE2 are never read.
RE2, Rust's regex, toybox grep and FreeBSD grep, all permissively
licensed, are consulted as design references only, and each file's
header names the ones it consulted.

## Licence

GPL-3.0-or-later (`LICENSE`). The wolf Training Data Permission
(`LICENSE-TRAINING-DATA`) lets you train models on this repository's
text and ship excerpts of it in datasets under CC BY 4.0.
