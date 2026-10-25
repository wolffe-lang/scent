# Regex engine

## Interface

`compile(patterns: List[List[byte]], options: Options,
mut diagnostics: Diagnostics) -> Regex ! {invalid}` compiles a list of byte
patterns. The caller first splits pattern sources at newlines. Group numbers
are local to each pattern. `Options` contains `extended`, `icase`, `word`,
`whole`, and the byte `terminator` (LF normally, NUL for `-z`). No dependency
other than wolf-std is needed by the engine.

`diagnostics_new()` creates an ordered diagnostic sink. Each `Diagnostic`
has a zero-based `pattern`, a `warning` flag, and byte `text` without the
program-name prefix or final newline. The CLI adds its program-name and
source-file context. Diagnostic text is bytes because patterns need not be
UTF-8. Compilation returns `invalid` after recording an error.

`workspace_new(re: Regex) -> Workspace` allocates execution storage. The
compiled value is immutable; workspaces are separate, reusable, and not
copied with it.

`line_matches(re, mut workspace, buf, lo, hi) -> bool` decides selection for
the fixed line window, including empty matches. **Selection comes first.**

`next_span(re, mut workspace, buf, lo, hi, from) -> Span ! {none}` has the
precondition that `line_matches` already selected this unchanged line using
the same workspace. It
returns only **nonempty**, half-open absolute byte spans. Pass the preceding
span's `hi` to resume; retain the original `lo` and `hi` so anchors and word
context never move. It never performs a hidden selection scan for each
span. ERE `{a}` on `a}` witnesses why the precondition matters: GNU selects
no line and prints no span, although its separate span parser can interpret
the leading brace differently.

Bounds must satisfy `0 <= lo <= hi <= buf.len`. Workspace allocation must
outlive its use. A backreference stack can grow: do not call it in a
short-lived inner allocation region while retaining the workspace outside
that region. The compiler rejects that escape. Place the workspace and
matching loop in the same persistent allocation region instead.

## Parser and programs

The parser uses explicit group frames and an indexed AST. The Thompson
compiler uses explicit continuation tasks, expanding bounded repetitions
without a recursive compiler walk. Classes are flat 256-entry byte tables;
ASCII case closure is applied before bracket negation. No consuming
instruction accepts the configured terminator. Ruling #117 also makes
each terminator-bearing pattern unreachable after syntax validation,
including a pattern with an otherwise matching alternative. Assertions inspect the
original line window.

GNU uses different rules for selection and reported spans on some unusual
expressions. Separate instruction roots preserve those measured rules.
Direct assertion repetition can be accepted by selection while the span
parser discards an ERE operator byte, leaving interval digits and a closing
brace as literals; BRE span parsing instead takes the repetition spelling
literally. Discarded leading operators also affect group-close validation.
Patterns containing a backreference or a collating/equivalence bracket
select through the span program, as does the entire pattern list containing
one of them. A byte-for-byte literal shortcut preserves literal BRE anchors.

Warnings for an escaped byte use its printable character in the C locale,
`white space` for space, and `unprintable character` for control/high bytes.
Ordinary compile errors suppress earlier warnings. Leading oversized
intervals have GNU's separately measured lowercase error and warning order.
The exhaustive short malformed-pattern and escaped-byte gate tests these
rules rather than relying only on diagnostic examples.

## Matching and memory

The reference/span regular matcher is a state-set simulation, not backtracking. Seeds enter
in increasing start order; the first visit to a program counter dominates
later starts. Acceptance retains the longest endpoint at the earliest
start. Epsilon closure uses generation marks and an explicit stack,
including for empty cycles. The word test filters candidate endpoints
before choosing the longest accepted span.

For `m` compiled instructions and `n` input bytes, one reference/span search takes O(m*n)
time and O(m) scratch. There is no string conversion, per-byte allocation,
or `Map` on this path. The base workspace scalar arrays hold `5*m + (2*m+1)` integers plus one
projection-cache integer per pattern;
compiled instructions hold four integers each, and each class holds 256
booleans. List capacity overhead does not change the bound. An empty-only
program returns `none` from `next_span` without scanning the line; a 1 MiB
unit exercises that path.

Only patterns containing backreferences take the depth-first matcher. A
regular superset is checked first: each backreference becomes any byte
string without the terminator, including under `-i`; SAVE instructions carry
no constraint. This can admit impossible captures but cannot remove an
accepting backtracking path. Feasibility is cached per pattern for the
unchanged selected line, so a missing alternative is not rescanned for each
reported span. A successful match ending at `hi` is already longest and
ends the search immediately. Unit families exercise passing projections
where the backtracker must still decide; a seeded counterfactual soak runs
every generated backreference pair both with and without the filter.

Capture slots are inline scalars, not newly allocated lists per branch. Its
separate stack grows geometrically and retains its high-water storage for
reuse; input-dependent storage and potentially exponential time are **not**
covered by the regular matcher's bounds. The cost report records peak stack
frames, native-process peak RSS, and explicit timeouts separately. A frame
contains 23 integer fields (184 bytes of logical scalar payload on a 64-bit
host); process RSS also includes compiled code, input, and allocator storage.

## Word-span divergences

Ruling #115 publishes these differences: for a selected line, scent keeps
leftmost-longest word spans where GNU's
shorter-candidate retry/stepping fails to follow a general rule. These rows
are counted separately, never as agreement. Selection, diagnostics, and exit
status still agree on these rows. The bounded matrix shifts the same input
suffix behind multiple prefixes and compares literal alternatives with
repeated general expressions; its data is
`notes/ct01-evidence/word-probe.jsonl`.

A compact witness is ERE `.{1,2}` under `-w` on four spaces followed by `ab`.
GNU emits spans 0..2 and 4..6, omitting the valid shorter 2..3 span. The exact
per-pair divergence table is generated below from the gate evidence.

| ERE pattern (BRE equivalent also measured) | Flags | Input bytes (hex) | scent spans | GNU spans |
| --- | --- | --- | --- | --- |
| <code>\S{,2}</code> | -i -w | `2041310d206280616130` | 1..3, 5..6 | 1..3 |
| <code>\S{,2}</code> | -i -w | `20204220302d3161090920` | 2..3, 4..5, 6..8 | 2..3, 6..8 |
| <code>\S{,2}</code> | -i -w | `42200d302d318009` | 0..1, 3..4, 5..7 | 0..1, 5..7 |
| <code>\S{,2}</code> | -i -w | `094280318062` | 1..2, 3..4, 5..6 | 5..6 |
| <code>\S{,2}</code> | -i -w | `202d2d424109ff096142` | 1..2, 3..5, 6..7, 8..10 | 3..5, 6..7, 8..10 |
| <code>\s+?</code> | -i -w | `8009090d3042` | 1..3 | 1..2 |
| <code>(b*&#124;\&#x27;)\S{,2}</code> | -w | `3100002d5f313030ff` | 0..2, 2..3 | 0..2 |
| <code>([[:space:]]{2}&#124;.)</code> | -w | `090d200942423062` | 0..2, 2..3 | 0..2 |
| <code>.{1,3}</code> | -i -w | `0031300042420d2d61806262` | 0..3, 4..7, 7..9, 10..12 | 0..3, 4..7, 10..12 |
| <code>.{1,3}</code> | -i -w | `30ff5f2d610d0941` | 0..3, 4..6, 6..8 | 0..3, 6..8 |

The engine gate and joined CLI accept only these exact reviewed pattern/flag/input/output witnesses
from `tests/re/word-divergences.json`; an unknown word-span difference stops
the run. The two dialects account for 20 separately counted pairs.

## GNU extension compatibility exceptions

POSIX leaves adjacent duplication symbols undefined (XBD 9.3.6 and 9.4.6),
and ERE backreferences are a GNU extension. Ruling #116 retains the consistent `**` = `*` interpretation.
The exception below is therefore
**not a contradiction of a POSIX requirement**. scent gives `**` the
compositional meaning of `*`; GNU's measured answer differs in this reviewed
family. New families require separate review, not automatic expansion of
this exception.

| Name | Family and scope | Witness and chosen answer |
| --- | --- | --- |
| `gnu-double-star-empty-capture` | The expressions below, BRE/ERE, with or without `-i`; no other flags | On `a`, group 1 can match empty, group 2 matches `a`, and the repeated empty backreference consumes nothing. scent selects `a`; GNU does not. |

ERE:

```text
(A**|.)(a)\1**
```

BRE:

```text
\(A**\|.\)\(a\)\1**
```

The 16-configuration neighbourhood varies both star spellings (`*`/`**`),
syntax, and `-i`. GNU loses the empty-group path only when both spellings are
`**`; replacing either by `*` restores it. This describes the measured
family, not a general rule for GNU's matcher. The original32 generated pairs per syntax are pinned with both exact
answers in `tests/re/extension-divergences.json`, including pairs where
the outputs happen to agree; a new subject/output is never admitted by
pattern spelling alone. The evidence is `notes/ct01-evidence/backref-neighbourhood.jsonl`.

Affected first-corpus subjects include `a`, `ab`, `a-bx`, `A`, and byte strings
`610d2d622009414231ff802d` and `6100098000410080314262`. On
`2d80ff41413141425f610d`, GNU also loses later spans after its first match.
The complete per-pair records retain every subject and both span sequences.

## Character and speed extensions

UTF-8 execution uses decoded units, generated C.UTF-8 class/fold tables and
byte-offset-preserving positions. Assertions use the same decoded predicates.
Malformed bytes and legacy values retain separate identities; capture slots
remain byte offsets for backreferences.

The bounded lazy-DFA cache lives in `Workspace`, while immutable mandatory-literal
proofs live in `Regex`. State-set simulation remains the fallback. Boolean
selection caches sorted raw successor sets with exact decoded units plus
start/end/word context. Assertion-free C programs use dense byte edges;
UTF-8 and context-sensitive programs use bounded keyed edges. The program
identity fixes class predicates, locale and fold closure. A full cache reruns
the unchanged record through the original VM, never answers "no match".
There are at most 128 states, 4,096 edges and 65,536 stored counters. Programs
above 2,048 instructions and any list containing a backreference stay on the
original VM. All caches die with their chunk.

Literal analysis follows AST dependencies explicitly (parser nodes can have
forward children), preserving separate selection/span roots. Concatenation
joins runs; alternation takes a common run; optional repetitions contribute no
requirement. The longest proved run is capped at 256 units and analysis at
4,096 AST nodes; beyond those bounds the proof admits rather than rejects.
This is a conservative necessary condition, not a claim of globally optimal
literal inference. Exact runs can select directly only after word/whole-line
checks. UTF-8 candidates stay on decoded boundaries, with distinct malformed
byte and legacy-value identities and the same canonical fold closure as the VM.
C scans use a last-byte skip table; `SCENT_PREFILTER=scan` is the measured
unit-step control. `SCENT_MATCH_ENGINE=vm` disables selection accelerators for
differential tests; `SCENT_DFA_LIMIT=1` exercises bounded fallback.

The existing VM still computes spans. Fixed `-F` selection uses original
prefix/failure/output-link construction for multiple C patterns and scalar
UTF-8 patterns; C single-pattern and span paths retain KMP. UTF-8 word/whole
selection stays on the regex path. No external engine source informed these
additions. Compiled-size bounds
include interval expansion; source-pattern length alone does not bound the
program linearly. Large accepted intervals and the 32767 limit are measured
explicitly in the cost gate.
