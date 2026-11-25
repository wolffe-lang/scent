# Changelog

## Unreleased — 0.2.1

- Find line ends with the runtime's vector byte search, sixteen bytes at a time; add oracle rows for line ends at vector and chunk edges.

- Hold each operand's unfinished line and context in a region block freed when the operand ends: resident memory no longer grows with the number of files.

## 0.2.0 — 2026-11-24

- Release as the v0.2.0 source tag: the binary, this file and both packaging recipes are checked to name one version.

- Name each reviewed difference by its rule in words, never by a number or a tag.

- Make one stdout buffer per run; add CPU and resident-size ratio rows against the pinned GNU build, bounded from a calibrated take.

- Select nothing and read no file for an empty pattern set without -v or -L; read colour settings after the pattern files.

- Pin wolf 0.2.36 / lupin 0.1.58; replay the byte-FF argv reviews at its argument-utf8 trap.

- Add raw-order recursive walking, directory/device policies and ordered glob filters.
- Add terminal colour, GREP_COLORS capabilities and deprecated GREP_COLOR warnings.
- Gate M2 against the pinned GNU build; publish socket-skip and byte-path differences.
- Keep UTF-8 locale semantics explicitly refused until M3.

- Establish the pinned toolchain and GNU grep 3.12 clean-room oracle.

- Join default BRE and ERE to the C-locale CLI and pin wolf 0.2.35.
- Add exact published differences, obsolete-name wrappers and the M1 matrix.
- Check output identity by descriptor; draft source packaging and PAX handoff.
