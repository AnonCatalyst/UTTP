# Claim Ledger — Accuracy Review

**Review date:** 2026-11-19
**Scope:** the public-facing claims, labels, and numbers in this archive.
**Rule:** a claim can be cited only at the confidence level shown here. A file
being in the archive does not make its allegation a verified fact.

Legend:

- **E** — Established: government instrument, court record, primary document, or direct observation.
- **C** — Corroborated: at least two independent sources.
- **A** — Assessment: WIC analysis of the available record.
- **S** — Single-source / alleged.
- **D** — Community documentation: wiki, directory, donated note.
- **X** — Disputed, outdated, or superseded. Do not repeat as fact.

---

## 1. Corrections that apply across the archive

### Archive size

- **Old wording:** “6 GB of the 10 GB total; 4 GB held back.”
- **Correction:** the public release is **6 GB**. Do not cite a 10 GB total or a
  pending 4 GB release unless WIC publishes a new release notice that says so.
- **Status:** X (old wording), current release notice corrected.
- **Where:** `01_ARCHIVE_RELEASE/6GB_Public_Archive/`, root `README.md`.

### “UTTP is a terrorist entity”

- **Correction:** **UTTP itself has not been listed as a terrorist entity** by
  Canada or New Zealand in the sources reviewed here. Canada listed **764**
  (December 2025); New Zealand designated **O9A/ONA** on 2025-12-07. UTTP is assessed by
  independent analysts as an NVE-adjacent/overlapping network, not as a
  designated entity.
- **Status:** X for “UTTP is designated”; E for the 764/O9A designations.
- **Sources:** [Public Safety Canada, 2025-12-10](https://www.canada.ca/en/public-safety-canada/news/2025/12/government-of-canada-lists-four-new-terrorist-entities0.html);
  [Canada Gazette SOR/2025-263](https://gazette.gc.ca/rp-pr/p2/2025/2025-12-17/html/sor-dors263-eng.html);
  [NZ Gazette 2025-au7135](https://gazette.govt.nz/notice/id/2025-au7135);
  corrigendum [2025-au7194](https://gazette.govt.nz/notice/id/2025-au7194).

### New Zealand O9A notice number

- **Old wording:** NZ Gazette `2025-go11755`.
- **Correction:** the O9A/ONA designation is **2025-au7135**, published
  2025-12-10, for a designation made on 2025-12-07. A corrigendum is
  **2025-au7194**, published 2025-12-11.
- **Status:** X for `2025-go11755`; E for `2025-au7135`.
- **Where:** `11_RESEARCH_EXPANSION/SOURCE_LEDGER_2026.md`,
  `00_READ_FIRST/TIMELINE.md`, `13_UTTP_764_OVERLAP/SOURCES.md`,
  `12_TRACKING/TRACKING_REGISTER.csv`, `10_SOURCES/`.

### "O9A parent entity / 764 operational arm"

- **Correction:** the NZ statement of case lists **764 as an O9A nexion**, but
  nexions are **operationally independent** and O9A has no established central
  leaders directing terrorism. "Parent company," "operational arm," and "O9A
  commands 764" overstate the evidence.
- **Status:** E for the nexion listing; X for command/parent-company language.
- **Where:** `14_O9A_764_TRACE/EVIDENCE_AND_LIMITS.md`;
  legacy `05_PARENT_ENTITIES/` and `02_CORE_INVESTIGATION/Historical/` language
  is retained for provenance but should be read with this correction.

### Source-index URL corrections

- The local source index JSON points to `SOR/2025-276` for the Canadian
  regulation. The official instrument listing **764** is **SOR/2025-263**,
  published 2025-12-17. Use the official Canada Gazette link in
  `11_RESEARCH_EXPANSION/SOURCE_LEDGER_2026.md`.
- Some legacy JSON entries contain placeholder or malformed links (for example a
  Xinhua URL with a repeated hex pattern). Treat those as broken leads, not
  citations.
- **Status:** E for the official instrument; X for the local JSON link.
- **Action:** keep the original JSON for provenance; use the corrected link in
  new work.

### “FBI classified 764 as Tier 1 terrorist threat”

- **Status:** S/X. The archive repeats this phrase, but a primary FBI document
  using “Tier 1” was not located in this review. Government documents establish
  that 764 is a designated terrorist entity in Canada and the subject of FBI/DOJ
  cases; they do not, in the documents reviewed, establish the “Tier 1” label.
- **Action:** cite the designation and the prosecutions, not “Tier 1,” unless a
  primary FBI source is attached.

### “No private individuals / no doxing”

- **Correction:** the archive contains historical usernames, user IDs,
  screenshots, and donated material. The presence of an identifier in the record
  is **not** permission to contact, expose, or target anyone. The archive's rule
  is non-contact and non-doxing; it cannot claim that no identifier exists in a
  historical capture.
- **Status:** X for the absolute wording; policy remains non-harassment.
- **Where:** root `README.md`, `06_COMMUNITY_NOTES/README.md`.

### “All content is legal / public”

- **Correction:** the archive is public-interest OSINT and donated material, but
  “legal” is jurisdiction-dependent and some files are graphic or NSFW. Read the
  content warning. Do not reuse media without considering law, consent, and
  platform policy.
- **Status:** A/X for absolute wording.

---

## 2. Founding and early history

| Claim | Confidence | Basis | Note |
| --- | --- | --- | --- |
| UTTP emerged in 2011 as a YouTube trolling group | C | Multiple community histories and independent analysis | Exact founding day varies by source. |
| Founding date is 12 February 2011 | D | tommyparky.com, EverybodyWiki, community histories | Some WIC documents say 12–13 February. Treat the exact day as approximate. |
| Founder is Thomas Parkinson / “Tommy Parky” | D | Community histories, encyclopedic sources | Name is public in community records; WIC has not independently verified personal details. Do not add private information. |
| UTTP began as “anti-troll”/bait-spam group and shifted toward harassment | C | Community histories, Sparx Intelligence | The shift is the relevant finding, not the exact date. |
| 2014–2016 escalation to account takeover, DoS, raids | C | Sparx Intelligence, community histories | Independent analysis supports the trend. |
| UTTP is a decentralised brand/franchise with multiple factions | C | Sparx Intelligence, WIC analysis, community histories | Factions and leaders change; do not treat one faction as the whole. |

---

## 3. Relationship to 764, O9A, and NVE networks

| Claim | Confidence | Basis | Note |
| --- | --- | --- | --- |
| 764 is a designated terrorist entity in Canada | E | Public Safety Canada; Canada Gazette | Listed 2025-12-10/17. |
| O9A is a designated terrorist entity in New Zealand | E | NZ Gazette 2025-au7135; NZ DPMC; NZ Police statement of case | Designated 2025-12-07; notice published 2025-12-10. |
| 764 is listed as an O9A nexion in the NZ statement of case | E | NZ Police statement of case, para 20.5 | Nexions are operationally independent; this is not a command chain. |
| 764 and O9A overlap in the same extremist ecosystem | C/E | NZ statement of case; GNET; CTC West Point; ISD | “Adjacent/nexion” is supported; “764 = O9A” and “O9A commands 764” are not. |
| UTTP overlaps with 764/NVE networks | A/C | Sparx Intelligence (2026-07-15); WIC archive; community records | Sparx describes UTTP as an NVE network with overlap to 764/NLM/MMC. The specific recruitment pipeline is WIC/community assessment. |
| UTTP leadership deliberately recruited 764/Foodist members | A/S | WIC archive, GitHub Issue #1 commenter, community records | The commenter's account is a party admission/claim, not a court finding. Label as assessed/single-source. |
| UTTP is itself a listed terrorist entity | X | No listing found for UTTP | Do not state this. |
| “09A Cult” is O9A's headquarters or UTTP's parent | X | Archive label only; no primary source | “09A” is an alternate spelling; the folder is legacy context. |
| “FBI Tier 1” label | S/X | No primary FBI source located | Use “designated in Canada” and “FBI/DOJ cases” instead. |

---

## 4. Current state (2026)

| Claim | Confidence | Basis | Note |
| --- | --- | --- | --- |
| UTTP is fragmented and reduced in 2026 | A/C | Soyjak Wiki (community), WIC observations, Sparx analysis | Community wiki says “complete DNB / almost no members”; this is a community assessment, not a measured census. Splinter activity continues. |
| UTTP ran an “Operation Circusfall” revival in 2026 | D | Soyjak Wiki UTTP page | Community documentation; not independently verified. |
| A split produced Anti-Fandom Resistance (AFR) | D | Soyjak Wiki, WIC alias list | Treat as a community-reported splinter, not a confirmed formal entity. |
| UTTP is “in retreat” as of 2026-09-28 | D | Soyjak Wiki cited by WIC | Community source. Do not call it independent validation. |
| UTTP is active/operating | A | WIC observations, community reports, current splinters | Active as a brand/splinter ecosystem, not necessarily as one organisation. |

---

## 5. Tactics

| Claim | Confidence | Basis | Note |
| --- | --- | --- | --- |
| Coordinated mass reporting / false reports | C | WIC archive, community histories, platform context | A core documented tactic. |
| Comment raids and spam | E/C | Public posts, community records, WIC observations | Directly observable in public threads. |
| Doxing and swatting threats | C/A | WIC archive, community records, journalism | Distinguish threat from completed act. |
| Bot/automation use | A | WIC archive; platform observations | Specific botnet attribution varies. |
| Infiltration of fandoms and impersonation | A/C | WIC FPE record; community records; Sparx analysis | Strong pattern; individual cases require evidence. |
| CSAM/gore distribution allegations | C/A | DOJ 764 cases; community documentation; WIC archive | Do not repeat graphic detail. 764 prosecutions are established; UTTP-specific involvement is assessed/community unless sourced. |
| “Psyop”/provocation as a tactic | A | WIC methodology, WIC FPE record | WIC's own method; not an independent finding about UTTP. |
| AI-generated content as provocation | A | WIC FPE record | WIC's own account; not independently verified. |

---

## 6. FPE / Operation Crown Drop

| Claim | Confidence | Basis | Note |
| --- | --- | --- | --- |
| WIC temporarily accepted and returned an FPE “crown” | A | WIC's own historical record, `Operation_Crown_Drop...md` | Self-authored. No independent confirmation located. |
| The FPE ecosystem was infiltrated/poisoned by UTTP | A/S | WIC record; FPE affiliation notes; community context | WIC assessment; individual claims require evidence. |
| WIC used controlled provocation for intelligence | A | WIC public methodology; WIC FPE record | WIC's stated method; not independent. |
| WIC is an FPE partner or governs FPE | X | WIC's current position and public listing | WIC states it is not a partner and did not accept a governing role. |
| The departure image was AI-generated | A | WIC record | WIC's own account. |
| “The operation caused UTTP to retreat” | A/X | WIC record; Soyjak Wiki | Correlation/claim, not a controlled causal finding. |

---

## 7. Archive and release

| Claim | Confidence | Basis | Note |
| --- | --- | --- | --- |
| 6 GB public release | E (release notice) | Archive release README, WIC statement | Public release is 6 GB. |
| “10 GB total / 4 GB remaining” | X | Older wording | Superseded. Do not repeat. |
| 534 original tracked files preserved; manifest currently lists 586 files | E | Git history + `MANIFEST.csv` at 2026-11-19 | Count excludes `.git`; the increase is new documentation, not deletion. |
| Every original file preserved in reorg | E | Git rename history + manifest | No content deletion in the 2026-11-19 pass; paths changed. |
| Archive is a “target list” | X | Archive scope and policy | It explicitly is not. |

---

## 8. How to use this ledger

1. Find the claim in the relevant document.
2. Check this ledger for its confidence and correction.
3. Open the linked primary/independent source.
4. Cite the source and the ledger entry, not a screenshot alone.
5. If a claim is `S` or `D`, write “alleged” or “community-reported.”

If you find a primary source that changes a row, open an issue with the source
and the exact claim. WIC reviews corrections before changing the ledger.

---

## 9. StyxNet validation

| Claim | Confidence | Basis | Note |
| --- | --- | --- | --- |
| StyxNet raw export contains 823 rows | E | Raw CSV row count | 761 exact; 62 similarity. |
| “823 profiles” | X | Raw report wording | Rows are not profiles; many are search/login/error pages. |
| “760 primary detections” | X | Earlier summary | There are 823 rows and 760 unique platform labels. |
| 47 platform-name variants, 37 normalized keys | E | `validation/styxnet_platform_name_blocklist.csv` | Earlier “48” was wrong. |
| No platform name is a validated handle | E | Blocklist + script check | Platform names are site identity, not handles. |
| 15 CSV-backed structural candidates | A/S | `validation/styxnet_handle_candidates.csv` | 14 brand-token + 1 target-only; ownership not verified. |
| 22 candidate handles in the manual report | A/S | 14 CSV-backed + 8 prior-extraction | Not confirmed accounts. |
| Ownership verified for any StyxNet handle | X | No live ownership check in this pass | 0 verified. |
| 580 `profile_path_unverified` rows | A | Heuristic row classification | URL shape only; not identity. |

Read `09_STYXNET_REPORTS/validation/STYXNET_VALIDATION_2026-11-19.md` before
citing a StyxNet handle.
