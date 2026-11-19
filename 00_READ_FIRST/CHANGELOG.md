# Changelog

## 2026-11-19 — Members and groups listings restored/expanded

- Added `02_CORE_INVESTIGATION/Members_List/README.md`.
- Added `EXPANDED/EXPANDED_MEMBERS_AND_GROUPS_2026-11-19.md`,
  `EXPANDED/GROUP_REGISTER.csv`, and `EXPANDED/PUBLIC_HANDLE_INDEX.csv`.
- Restored access to the original raw indicator lists and separated group names,
  public handles, and naming-pattern families.
- Added DPOS internal units (Empire, Task Force, Grand Palace, ISA HQ, Town,
  Outside, Logs) as observed structure, not a member roster.
- No new private identifiers were added.

## 2026-11-19 — DPOS deep dive

- Added `04_OFFSHOOTS/DPOS - Degeneracy Police Order State/README.md` and
  `ANALYSIS/DPOS_DEEP_DIVE_2026-11-19.md`.
- Added `ANALYSIS/DPOS_CONNECTIONS.csv` connecting DPOS to UTTP, 764, O9A,
  Spawnism, FPE, TNM/148/GRS/Enclave, GateKeeper, and third-party OSINT.
- Finding: DPOS is a **hardcore UTTP offshoot** and a structured
  police-state-themed bridge to 764/Com; 764 overlap is supported, but no
  764 unit/command/merger is established.
- Added DPOS claims to the validated/false-claims registers and corrected
  WIC/third-party overclaims in place with validation notes.
- Updated entity map, tracking register/board, UTTP profile, and navigation.

## 2026-11-19 — Validated claims / false-claims quarantine

- Added `15_VALIDATED_CLAIMS/` with the approved-claim register and summary.
- Added `16_VALIDATED_FALSE_CLAIMS/` with the false-claim register and a grouped
  quarantine record.
- Stripped false/superseded claims from current and historical analysis docs,
  including 10 GB/4 GB sizing, FBI “Tier 1,” O9A parent/764 operational-arm
  wording, UTTP operational-arm/merger claims, and StyxNet count errors.
- Replaced absolute privacy/legality wording with qualified wording.
- No raw evidence files were removed; no new private identifiers were added.

## 2026-11-19 — UTTP/764 arm, infiltration, and merger assessment

- Added `13_UTTP_764_OVERLAP/FINAL_ASSESSMENT_2026-11-19.md` testing the claims
  that UTTP is an operational arm of 764, was infiltrated by 764, or merged with
  764.
- Finding: **edge fusion and membership overlap are supported; operational-arm,
  merger, and 764-specific infiltration claims are not established.** 764 is
  designated; UTTP is not.
- Added Sparx, Bx Writes, DOJ, Soyjak Wiki, and community-claim sources with
  confidence labels.
- Updated the overlap analysis, evidence ledger, tracking snapshot/board, entity
  map, timeline, and claim ledger.
- No private data was added; no raw evidence was removed.

## 2026-11-19 — StyxNet accuracy pass

- Added `09_STYXNET_REPORTS/validation/` with a reproducible validator, a
  47-variant platform-name blocklist, handle/row class counts, and a
  candidate-only output.
- Corrected the platform-name count from “48” to **47 variants / 37 normalized
  keys**; earlier wording was wrong.
- Corrected “760 primary detections / 823 profiles” to **823 rows** (761 exact,
  62 similarity; 760 unique platform labels).
- Separated **profile-path candidates** from **ownership-confirmed accounts**;
  ownership verified in this pass is **0**.
- Raw StyxNet exports were not modified.
- No private data was added.

## 2026-11-19 — O9A trace and 764→O9A correction

- Added `14_O9A_764_TRACE/` with a sourced O9A profile, the 764→O9A trace,
  structure/ideology analysis, designations, evidence limits, timeline, and
  sources.
- Corrected the New Zealand notice number from the old `2025-go11755` to
  **2025-au7135** (designation 2025-12-07; published 2025-12-10; corrigendum
  **2025-au7194**).
- Clarified that the NZ statement of case lists **764 as an O9A nexion**, but
  nexions are operationally independent; "parent company" and "command" language
  is not supported.
- Added `05_PARENT_ENTITIES/09A Cult/README.md` explaining that "09A Cult" is a
  legacy archive label, not an O9A headquarters.
- Updated navigation, entity map, timeline, source ledger, tracking register, and
  the 764 profile.
- Annotated two historical WIC dossiers with a correction banner (hierarchy/parent
  language); content was not deleted.
- No original file was deleted. No private data was added.

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
- Added `12_TRACKING/` group-level tracking snapshot, register, board, methods,
  collection plan, open leads, and `INBOX/` for new tracking notes.
- Added `13_UTTP_764_OVERLAP/` dedicated UTTP/764 profiles and tactic-overlap
  evidence analysis.
- No individual tracking and no private data added.

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
