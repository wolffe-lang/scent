# scent module map

The process edge in `src/scent.lu` turns argv into `opts.Options`, reads
pattern sources without decoding file bytes, compiles one matcher, then
feeds each operand through `reader.scan` to the byte writer in `out`.

`argv → options → pattern list → matcher → reader → output`

- `src/opts/`: getopt_long-shaped parsing, permutation, diagnostics and
  the sole `program()` prefix seam. R-ct00-3 fixes it to `grep` until
  wolf-lang#899 provides argv[0]. No `os_exe` substitution.
- `src/fixed/`: immutable literal bytes with KMP failure links. Search
  is linear in the line length per pattern, not a naive quadratic retry.
  ASCII folding and word/whole-line constraints are C-locale byte tests.
  Workspace caches each pattern's next candidate with monotonic KMP
  cursors, so a missing alternative is not rescanned for every -o span.
  Begin each span sequence at from == lo, or call line_matches first.
- `src/matcher/`: dispatch seam for ct02. `Matcher` is immutable;
  `Workspace` owns scratch allocated by `workspace_new` once per read chunk,
  never per line. Both entry
  points accept a half-open `(buf: List[byte], lo, hi)` line window:
  `line_matches(re, mut ws, buf, lo, hi) -> bool` and
  `next_span(re, mut ws, buf, lo, hi, from) -> Span ! {none}`. Spans
  are leftmost-longest, in buffer coordinates. Empty patterns are tested by `line_matches`; `next_span` returns
  nonempty spans only, avoiding quadratic rescans with empty alternatives. `compile(patterns: List[List[byte]], syntax,
  flags) -> Matcher ! {invalid}` is ct02's sole syntax dispatch. Until
  then G/E refuse by name; ct02 replaces those arms with ct01's `re`.
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
invocations are separately counted not-yet under #899; non-UTF-8
arguments are separately counted under #406. M2 owns recursion/colour.

## Terminator-bearing patterns

R-ct00-5 defers the cross-record adapter to ct02, for F/G/E together. A
pattern may contain the active terminator: GNU prints the touched records
as one output unit, not independent per-record selections. The normal
reader's delimiter-excluding window cannot express that. `scent.lu`
refuses this mode by name before the syntax dispatch. The 216 measured
`cross-*` witnesses cover all three syntaxes, leading/trailing NUL, three
records and a 96 KiB boundary, with count/spans/prefixes/inversion/limit/
whole-line/word/context controls. `patterns-07` and `nul-pattern-z` belong
to the same explicit not-yet column; no expected GNU bytes were changed.
