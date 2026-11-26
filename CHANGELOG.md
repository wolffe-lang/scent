# Changelog

## Unreleased — 0.2.1

- Ask the descriptor's offset only for standard input and stat each file once: two system calls fewer per file. scent's system calls per file on the many-files row are held exactly; add oracle rows for operand offsets and widths.

- Find line ends with the runtime's vector byte search, sixteen bytes at a time; add oracle rows for line ends at vector and chunk edges.

- Hold each operand's unfinished line and context in a region block freed when the operand ends: resident memory no longer grows with the number of files.

- Search each read once for the pattern's one required literal where nothing but the selected lines is counted or printed, in the C locale, and send only the lines it lands in to the matcher; a read falls back to visiting every line once seven sixteenths of its bytes hold the literal. On the held block the literal row reads 1.10 times GNU's CPU (from 2.2), the regular expression 0.98 (from 1.87) and the many-files row 1.75 (from 2.0). Where reads fall back, the rows read up to 3.6 % over the code before the search: dense and gap15 within 3 % of it, density50 and density75 within 4 % (they measured 3.1 to 3.6 % and 3.3 % over it). Under a UTF-8 locale the search never runs, and each line costs about 35 more instructions than before, 0.5 % (counted on one Mac, not timed). Add ratio rows by how much of the input holds the literal, and oracle rows on both sides of the search and across its fallback.

- Accept GNU's keyring by the signer's fingerprint, not by the file's digest: GNU replaced the file three times in 26 days with the tarball, its signer and the oracle binary unchanged. The tarball digest, the signer's fingerprint and the binary digest stay pinned; the keyring's digest is recorded as observed. Add an offline test of the source check.

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
