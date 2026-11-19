# Changelog

## 2026-11-19 — HTML capture viewing fix

### HTML capture viewing fix

- Renamed the two DPOS `.html` evidence captures to `.html.txt` so browsers and
  GitHub open them as text instead of treating them as a page to download or
  render. The bytes are unchanged; a hash comparison against the previous blobs
  was run before committing.
- Added `HTML_CAPTURE_NOTES.md` in the DPOS folder.

## 2026-11-19 — v2 organization and accuracy pass

**What changed**

- Reorganized top-level folders into numbered categories for navigation.
- Renamed the release folder from `10 GB UTTP Archive` to
  `6GB_Public_Archive` and its inner folder to `Release_2026-09-19`.
- Added `00_READ_FIRST/` navigation, claim ledger, timeline, entity map,
  glossary, data dictionary, path map, and file manifest.
- Added `11_RESEARCH_EXPANSION/` with new public-source research, source ledger,
  FPE correction, verification queue, and open questions.
- Corrected the archive-size claim to **6 GB public release**.
- Added confidence labels and identified outdated/unsupported claims in
  `CLAIM_LEDGER.md`.
- Generated `MANIFEST.csv` with path, size, and SHA-256 for every file.
- Added `12_TRACKING/` group-level tracking snapshot, register, board, collection
  plan, and open leads. No individual tracking and no private data.

**What did not change**

- No original file was removed.
- No evidence file was edited, redacted, or replaced.
- No private data was added.
- No claim was “verified” merely by moving a file.

**Counts**

- Original tracked files before the pass: **534**.
- New files in this pass: see `MANIFEST.csv` and `git diff --stat`.
- Pre-organization state: Git tag `pre-organize-20261118`.

**Corrections**

See `CLAIM_LEDGER.md`. The most important:

1. Public release is **6 GB**, not “6 of 10 GB”.
2. **UTTP itself is not a designated terrorist entity**; 764 and O9A are the
   designated entities in the sources reviewed.
3. The “FBI Tier 1” phrase is not supported by a primary FBI document located in
   this review; cite the designation/prosecutions instead.
4. The FPE “crown” operation is WIC's self-authored record, not independent
   verification of third-party claims.
