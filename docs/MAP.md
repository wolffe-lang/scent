# scent module map

The process edge in `src/scent.lu` turns argv into `opts.Options`, reads
pattern sources without decoding file bytes, compiles one matcher, then
feeds each operand through `reader.scan` to the byte writer in `out`.

`argv → options → pattern list → matcher → reader → output`

- `src/opts/`: getopt_long-shaped parsing, permutation, diagnostics and
  the sole `program()` prefix seam. R-ct00-3 fixes it to `grep` until
  wolf-lang#899/#904 provides argv[0]. No `os_exe` substitution.
- `src/walk/`: depth-first raw `std.fs.entries` order (never sorted),
  command-line versus walked symlink policy, ancestor dev+ino loop checks,
  directory/device filtering and per-file descriptor identity checks.
- `src/glob/`: C-locale byte glob matcher, including POSIX classes,
  one-byte collating/equivalence atoms and command-line suffix matching.
  Include/exclude rules retain order; the first rule determines fallback.
- `src/colors/`: terminal policy and validated GREP_COLORS/GREP_COLOR
  capabilities. `out` emits exact SGR/reset/erase bytes around fields,
  selected/context lines, matcher spans and group separators. `ne` omits
  erase commands and `rv` swaps selected/context backgrounds under -v.
- `src/fixed/`: immutable literal bytes with KMP failure links. Search
  is linear in the line length per pattern, not a naive quadratic retry.
  ASCII folding and word/whole-line constraints are C-locale byte tests.
  Workspace caches each pattern's next candidate with monotonic KMP
  cursors, so a missing alternative is not rescanned for every -o span.
  Begin each span sequence at from == lo, or call line_matches first.
- `src/matcher/`: joined F/G/E dispatch. `Matcher` is immutable;
  `Workspace` owns scratch allocated by `workspace_new` once per read chunk,
  never per line. Both entry
  points accept a half-open `(buf: List[byte], lo, hi)` line window:
  `line_matches(re, mut ws, buf, lo, hi) -> bool` and
  `next_span(re, mut ws, buf, lo, hi, from) -> Span ! {none}`. Spans
  are leftmost-longest, in buffer coordinates. Empty patterns are tested by `line_matches`; `next_span` returns
  nonempty spans only, avoiding quadratic rescans with empty alternatives. `compile(patterns: List[List[byte]], syntax,
  flags, mut diagnostics) -> Matcher ! {invalid}` compiles F through KMP
  and G/E through `re`. Diagnostics retain pattern-file line provenance;
  duplicate pattern bytes compile once.
- `src/re/`: the independent C-locale BRE/ERE engine for ct02's syntax
  dispatch. [RE.md](RE.md) specifies immutable compilation, a separate
  workspace, selection before nonempty span stepping, and the reviewed
  compatibility differences. Context span output establishes selection
  again for each historical buffer before asking for spans.
- `src/reader/`: files and descriptor 0; 96 KiB reads (GNU's measured
  regular-file read boundary), an unfinished-line byte buffer, and a
  lazy ring of the requested number of preceding lines. No whole-file
  input string and no bound `.bytes()` call on input. The delimiter is
  LF, or NUL under `-z`; default binary mode also treats observed NULs
  as delimiters. CR bytes are preserved on POSIX, including with `-U`.
  Each read/format/output turn has a temporary region. Carried bytes,
  context buffers live in a separate explicit region. Matcher workspace is
  chunk-local, as are stdout buffers: conservative mut-region tracking
  otherwise rejects a call with the transient output writer. Only scalar
  reader state is copied out of the temporary region.
- `src/out/`: fixed 64 KiB stdout staging, byte windows and GNU prefix
  ordering. Context has `-` fields; selected lines have `:` fields.
  Writes use descriptor 1 directly and report `os_error_text` failures.

GNU 3.12, configured `--disable-perl-regexp`, is the oracle. The source
is built unseen in the pinned Ubuntu container; no implementation from
that tree is a design input. `tools/oracle` invokes both binaries through
PATH as the bare word `grep`; stdout, stderr, status and (where requested)
remaining stdin bytes must agree. Help/version prose belongs to scent;
those two cases compare stream shape and status instead of FSF prose.

R-ct00-4 corrects the initial contract: different explicit matcher
syntaxes conflict; the same syntax may be repeated. Other-name/path
invocations and non-UTF-8 arguments are exact upstream-blocked reviews
under #899/#406/#904, not not-yet. The two abort messages type only the
PID as digits; every other byte and both statuses are exact. M2's walk, filters and colour are joined. M3's UTF-8 locale semantics
are refused by name. Help/diagnostics currently use fixed `grep` until
the pinned toolchain exposes argv[0].

## Terminator-bearing patterns

Ruling #117 replaces R-ct00-5: no pattern containing the active terminator
matches any record, for F/G/E alike. The ordinary bounded reader is
unchanged. GNU G/E consistently reject such matches; GNU F sometimes
crosses records within a read, but loses the same match across reads or
under -w. The 216 cross-* cases now count as164 agreement and52 exact
published divergences; the two original NUL cases add one agreement
and one exact reviewed difference. The README gives
the consistency decisions and separately tracked runtime gaps.

`tests/divergences.json` pins complete case identities and both answers;
reviewed rows that become agreement also fail until reviewed explicitly.
`tools/m1-ci-test` protects the generated5072-case floor, review counts and
CI wiring. `tools/gate` is the whole local acceptance, and
`tools/pax-posture` repeats the static suite without LANG or locale data.

## Recursive byte paths

`fs.entries` lists names as bytes in raw order, verified against GNU on
three 400-file trees with varied creation orders. The pin's open/stat
interfaces still require UTF-8 paths. The exact FF-name witness is an
upstream-blocked row (#687/#912), not M3 and not a blanket tree waiver.
Ruling #120's explicit socket skip is likewise one exact published
comparison family; walked sockets and FIFOs still agree with GNU.

`tools/m2-ci-test` guards the generated 3,384-case floor, shared-fixture
order posture, terminal rows and exact reviews. The M1 floor remains
5,072; neither generation step silently shrinks the other's cases.
