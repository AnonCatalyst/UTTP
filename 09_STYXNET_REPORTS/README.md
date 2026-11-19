# WINTERGATE-IC — STYXNET EXTRACTION ANALYSIS
### UTTP Identity Reconnaissance — Structural Validation Report

> WIC-ANALYSIS-2026-0919-UTTP-01_Structural_Handle_Extraction.md

[![Document](https://img.shields.io/badge/Document-WIC--ANALYSIS--2026--0919--UTTP--01-blue)]()
[![Classification](https://img.shields.io/badge/Classification-Internal%20%E2%80%94%20Analytical-orange)]()
[![Status](https://img.shields.io/badge/Status-Reviewed-blue)]()
[![Target](https://img.shields.io/badge/Target-UTTP-red)]()

---

> **Summary:** StyxNet swept 5,121 platforms against the handle `UTTP`. The raw CSV contains 823 rows (761 exact, 62 similarity) and 54 unique supplementary handle values. Most supplementary entries are not identity signals. This document contains structurally reviewed **candidates**, plus a validation methodology and a record of what was rejected and why.
>
> **2026-11-19 accuracy pass:** raw exports are unchanged. The machine-readable validation layer is in [`validation/`](validation/). Its counts supersede the approximate manual counts below where they differ. No candidate is ownership-confirmed.

---

## 📋 Document Metadata

| Field | Value |
|---|---|
| **Document ID** | `WIC-ANALYSIS-2026-0919-UTTP-01` |
| **Classification** | Public — Analytical |
| **Analyst** | WIC Threat Research |
| **Source** | StyxNet Username Search, handle extraction |
| **Date** | 2026-09-19 |
| **Target** | UTTP (UtubeTrollPolice / UTubeTrollingPolice) |
| **Raw rows** | 823 (761 exact; 62 similarity) |
| **Unique handle values** | 54 |
| **Candidate handles** | 22 (14 CSV-backed + 8 prior-extraction) |
| **Rejected CSV handle values** | 39 |
| **Profile paths unverified** | 580 |
| **Ownership verified** | 0 |

---

## 📖 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Validation Methodology](#2-validation-methodology)
3. [Tier 1 — Brand-Aligned Candidates](#3-tier-1--brand-aligned-candidates)
4. [Tier 2 — Structured Cluster](#4-tier-2--structured-cluster-bluesky-sock-network-pattern)
5. [Tier 3 — Pattern-Matched, Single Source](#5-tier-3--pattern-matched-single-source)
6. [Cross-Platform Presence Summary](#6-cross-platform-presence-summary)
7. [Rejected Findings and Reasons](#7-rejected-findings-and-reasons)
8. [Confidence Assessment and Gaps](#8-confidence-assessment-and-gaps)
9. [Methodology Limitations](#9-methodology-limitations)
10. [Recommended Next Steps](#10-recommended-next-steps)
11. [Appendix — Candidate Handle Index](#11-appendix--candidate-handle-index)

---

## 1. Executive Summary

StyxNet swept 5,121 platforms against the target handle `UTTP`. The raw CSV has 823 rows: 761 exact-string rows, 62 similarity rows, and 760 unique platform labels. The supplementary handle fields contain 54 unique values.

Of the raw extraction output, **the majority of entries are not identity signals**. They fall into four categories:

| Category | Description | Status |
|---|---|---|
| (a) Platform names | Scraped as handles | **False** |
| (b) Generic UI/field labels | Buttons, state keys | **False** |
| (c) Random strings | Nonces, cache keys, hashes | **False** |
| (d) Substring collisions | Unrelated words containing "uttp" | **False** |

After a manual analyst pass applying strict structural criteria, **22 candidate handles** remain (14 CSV-backed + 8 prior-extraction). They are **not ownership-confirmed**. The 2026-11-19 machine-readable pass is in [`validation/`](validation/); use its counts in preference to the approximate ones below.

This document contains only what passed the structural review. Rejected entries and the reasons for rejection are recorded in [Section 7](#7-rejected-findings-and-reasons).

---

## 2. Validation Methodology

The raw extraction output cannot be used directly. It must be filtered through validation rules before any entry can be treated as a finding.

### 2.1 Validation Rules Applied

| Rule | Requirement |
|---|---|
| **V1. User-Owned Only** | Handle must be the actual username of an account, appear in a profile URL, or appear in a user JSON field. Platform names, share buttons, SDK references, CDN hosts, and widget identifiers are NOT user-owned handles. |
| **V2. No Substring Collision** | If "uttp" appears inside a longer unrelated word, the match is rejected. |
| **V3. No Third-Party Identity** | Developers, extension authors, and platform owners whose handles appear in site footers or metadata are excluded. |
| **V4. No Generic Field Labels** | Words like `share`, `member`, `user`, `channel`, `playlist` are UI/state labels, not identities. |
| **V5. No Random Strings** | Strings with no semantic content (nonces, cache keys, hashes) are rejected. |
| **V6. Brand or Faction Patterning** | Handle is treated as UTTP-aligned if it contains "uttp" as a standalone token, or if it contains recognizable faction nomenclature (THTDC, THDTC, ZNTP, STR, UTTPTV, Mastodon Department). |
| **V7. Corroborated or Cluster-Matched** | An isolated handle with a coincidental substring is weak. A handle belonging to a cluster of structurally similar handles is stronger. |
| **V8. Platform-Name Blocklist** | If a handle normalizes to a known platform/site identity, reject it as `platform_identity_string`. The machine-readable blocklist is in `validation/styxnet_platform_name_blocklist.csv`. |
| **V9. No Search/Login/Error Rows** | A search page, login wall, error page, bot check, or non-200 response is not a profile finding. |

### 2.2 Confidence Tiers

| Tier | Definition | Confidence |
|---|---|---|
| **Tier 1** | Handle contains UTTP as standalone token or faction brand. Consistent with UTTP naming conventions. | **HIGH** for brand alignment. **MEDIUM** for current operation. |
| **Tier 2** | Handle belongs to a set on the same platform sharing a consistent naming scheme (rank, role, brand prefix). | **MEDIUM-HIGH** for common operator. **MEDIUM** for UTTP link. |
| **Tier 3** | Handle matches UTTP naming but appears once without cluster corroboration. | **LOW-MEDIUM**. Requires independent verification. |
| **Rejected** | Fails V1–V5. Recorded for completeness only. | **NOT A FINDING** |

---

## 3. Tier 1 — Brand-Aligned Candidates

These handles contain UTTP as a standalone brand token or use recognized UTTP faction nomenclature. They are treated as the strongest UTTP-presence **candidates**, not confirmed accounts.

### 3.1 `uttp.tumblr.com`

| Field | Value |
|---|---|
| **Platform** | Tumblr (subdomain) |
| **Pattern** | Direct subdomain under `tumblr.com` using the target handle |
| **Validation** | V1 (user-owned subdomain), V6 (standalone token) |
| **Notes** | A Tumblr subdomain is user-registered. Directly-owned presence, not a mention. |

### 3.2 `UTTP_OFFICAL`

| Field | Value |
|---|---|
| **Platform** | Multiple (appears in cross-platform handle list) |
| **Pattern** | Brand handle with deliberate "OFFICAL" spelling variant |
| **Validation** | V6 (standalone token, brand spelling) |
| **Notes** | The misspelling "OFFICAL" (not "OFFICIAL") is a distinctive marker. Consistent across two entries in extraction output. |

### 3.3 `UTTPmastdept`

| Field | Value |
|---|---|
| **Platform** | Mastodon (implied by naming) |
| **Pattern** | "UTTP" + "mastdept" (Mastodon Department) |
| **Validation** | V6 (standalone token, faction nomenclature) |
| **Notes** | "Department" naming implies organizational structure. |

### 3.4 `frickfunnymikeuttpthtdc`

| Field | Value |
|---|---|
| **Platform** | Mastodon (`mastodon.social` observed) |
| **Pattern** | UTTP + THTDC faction suffix |
| **Validation** | V6 (standalone token + faction acronym) |
| **Notes** | THTDC and THDTC are observed as UTTP faction markers. |

### 3.5 `kiloratstrzntputtp.bsky.social`

| Field | Value |
|---|---|
| **Platform** | Bluesky |
| **Pattern** | KiloRat + STR + ZNTP + UTTP (multi-faction naming) |
| **Validation** | V2 (standalone), V6 (multi-faction), V7 (cluster member) |
| **Notes** | Combines KiloRat, STR, ZNTP, and UTTP faction tokens in a single handle. **Strongest faction-naming signal in the extraction.** |

---

## 4. Tier 2 — Structured Cluster (Bluesky Sock Network Pattern)

Seven handles on Bluesky share a consistent naming structure. This pattern is characteristic of a single operator or small coordinated group maintaining a network of brand-aligned accounts.

| Handle | Pattern |
|---|---|
| `uttparkrosie.bsky.social` | UTTP + name |
| `michaelsuttptv.bsky.social` | "Michael's UTTP TV" + name |
| `uttpalette.bsky.social` | UTTP + concept |
| `kiloratstrzntputtp.bsky.social` | Multi-faction + UTTP |
| `uttpofficercoplord.bsky.social` | UTTP + rank (officer) + role (coplord) |
| `uttp-lieutenant2.bsky.social` | UTTP + rank (lieutenant) + number |
| `uttpus.bsky.social` | UTTP + collective (us) |

**Validation:** V7 (cluster corroboration), V6 (brand tokens throughout)

### 4.1 Observations

- **Rank Naming Convention** — Two handles use military/police rank titles (`officer`, `lieutenant`). Consistent with UTTP's observed "Degeneracy Police Order State" (DPOS) offshoot branding.
- **"COPLORD" Token** — `uttpofficercoplord` combines "officer", "cop", and "lord". Distinctive role self-designation.
- **"Michael" Identifier** — `michaelsuttptv.bsky.social` references a named individual. Same identifier appears in earlier extraction data as "Michael's UTTP TV Studios".
- **Cluster Cohesion** — Seven handles, one platform, consistent brand prefix, two with rank titles, one with a named operator. Probability of independent chance matching is low.

### 4.2 Confidence

- **MEDIUM-HIGH** for common operator across the cluster
- **MEDIUM** for a possible link to UTTP core organization

---

## 5. Tier 3 — Pattern-Matched, Single Source

These handles contain UTTP as a token or faction marker but do not appear in a corroborating cluster. Each requires independent verification before being treated as a UTTP-linked account.

| Handle | Pattern | Notes |
|---|---|---|
| `uttpower` | UTTP embedded | Single occurrence |
| `kecuttpikding1970` | UTTP + dated suffix | 1970 suffix |
| `vecuttpadi1981` | UTTP + dated suffix | 1981 suffix |
| `uttpthdtc` | UTTP + THDTC faction | Faction marker |
| `UTTP_OFFICAL` | Brand handle | Also Tier 1 |
| `demiurge-ash` | Named identity | From prior extraction |
| `chicken_hammer_bot` | Named bot | From prior extraction |
| `DarrenOfficial` | Named operator | From prior extraction |
| `pamegacorp` / `PA_Megacorp` | Corporate brand cluster | Two variants |
| `safesurvival` / `safesurvivalofficial` | Server brand cluster | Two variants |

**Confidence:** LOW-MEDIUM. Requires verification.

> **Note on dated suffixes:** `kecuttpikding1970` and `vecuttpadi1981` use year-based suffixes in a pattern often seen in bulk-registered sock accounts. The base words do not correspond to obvious real words, suggesting constructed identifiers.

---

## 6. Cross-Platform Presence Summary

Based on Tier 1 and Tier 2 candidates, UTTP brand-aligned **candidates** are present on the following platforms. This is structural evidence, not ownership confirmation:

| Platform | Presence Type |
|---|---|
| **Bluesky** | 7-handle structured cluster (Tier 2) |
| **Tumblr** | Direct subdomain (Tier 1) |
| **Mastodon** | Multiple faction handles (Tier 1) |
| **Multi-platform** | Brand handle `UTTP_OFFICAL` (Tier 1) |

**Additional platforms where presence is indicated by single-source findings and requires verification:**

| Platform | Finding |
|---|---|
| Streamlabs | `uttp / Streamlabs` (from prior extraction) |
| DeviantArt | `UTTP on DeviantArt` (from prior extraction) |

---

## 7. Rejected Findings and Reasons

For transparency, the following categories of entries were excluded from the candidate findings. They are recorded here so future analysis does not re-introduce them.

### 7.1 Platform Names Scraped as Handles

The list below contains **47 variants** (37 unique normalized keys). The machine-readable form is [`validation/styxnet_platform_name_blocklist.csv`](validation/styxnet_platform_name_blocklist.csv). Earlier wording said “48”; that count was wrong.

`Codecademy`, `codersrank-org`, `codersrank`, `thesimsresourcedotcom`, `TheSimsResource`, `livetrack24`, `LiveTrack24`, `HackThisSite.org`, `hackthissite`, `HackThisSite`, `MAGIX_INT`, `MAGIX`, `magix`, `WynkMusic`, `wynkmusic`, `Salon24pl`, `salon24.pl`, `FlashFlashRevolution`, `TheOfficial_FFR`, `ffr`, `Podcastindex-org`, `PodcastindexOrg`, `pennyarcadetv`, `subscan_io`, `stackernews`, `cssbattle.dev`, `css_battle`, `dicedotcom`, `coddytech`, `coddy.tech`, `coddylearn`, `coddy_tech`, `flyertalkforums`, `FlyerTalk`, `prokoni.ru`, `prokoni_ru`, `car72ru`, `wwwcar72ru`, `LancerX.ru`, `LancerX_ru`, `TTSPORT.ru`, `poembook_ru`, `maccentre_ru`, `yamaya_ru`, `radiomedru`, `romanticcollectionru`, `bysoloby`

> **Reason:** These are the platforms themselves. They appear in page headers, footers, metadata, or JSON fields as site identity, not as user handles.

### 7.2 Generic Field Labels

`platform`, `share`, `member`, `user`, `channel`, `dialog`, `intent`, `playlist`, `pages`, `images`, `uploads`, `en-us`, `pastebin`, `sharer.php`

> **Reason:** UI elements and state labels, not identities.

### 7.3 Substring Collision — "Butt" + "P" Words

`TacoButtPlug`, `Waluigis_Talking_Buttplug`, `SEND_BUTTPLUG_PICS`, `buttPickle`, `improvisedbuttplug`, `SpicedUpButtplug`, `buttpooper`, `Buttpounder69`, `buttpuddle`, `SendMeYourButtPics`, `Buttplugpeddler`, `buttpee`, `pnuttpad`, `FreeButtPlugs`, `Mrbuttpk`, `Ahmadbuttpunjab`, `smuttprogramming`, `puttputt`

> **Reason:** The letters `u-t-t-p` appear consecutively inside the longer word "buttplug" (`b-u-t-t-p-l-u-g`) and its variants. The substring matcher flagged these as containing the target token. They do not.
>
> ⚠️ **This is the single largest source of false positives in the raw extraction.** Any handle containing "buttplug", "buttp", "buttpee", "nuttpad", or similar constructs will match at the character level and must be excluded by V2.

### 7.4 Substring Collision — "Uttapal" (Indian Given Name)

`uttpal`, `UttpalSingh`, `Uttpalmishra`, `Uttpal47`, `uttpalKachhawa`, `UttpatiSahu`, `Uttpol11`, `UTTPALKANT`, `Uttpal-Tripathy`, `uttpal1`, `uttp3`, `uttpaul`, `uttpal95`, `uttpal-076`, `Uttprerak`, `uttp333`, `Uttpal-Kumar`

> **Reason:** "Uttapal" and "Uttpal" are real Indian given names containing the sequence `u-t-t-p`. These are unrelated individuals.
>
> ⚠️ **Publishing or acting on these names as UTTP-linked would be a false accusation.** They must be excluded under V2.

### 7.5 Third-Party Developer Handles

`Chocobozzz`, `marttiphpbb`, `TecharoHQ`

> **Reason:** `Chocobozzz` is the PeerTube developer. `marttiphpbb` is a phpBB extension author. `TecharoHQ` owns the Anubis proxy. Their handles appear in footers of every site using their software.

### 7.6 Scaffolding and Infrastructure

`pinterest.com`, `snapchat.com`, `connect.facebook.net`, `redditstatic.com`, `tiktok.cn.com`, `substackcdn.com`, `vkontakte.ru`, `vk.com`, `oauth.vk.com`, `ok.ru`, `flickr.com`, `fr.pinterest.com`, `vk.ru`, `64.media.tumblr.com`, `tumblr.com`, `cdn-cgi`

> **Reason:** Share buttons, social SDKs, CDNs, and OAuth endpoints. Every site with a share widget links to these domains. They are not cross-identity links.
>
> **Example:** The raw extraction reported "vk.com linked 15 similar". This does not mean 15 accounts share a VK identity. It means 15 profiles contained a VK share button. The count is meaningless as an identity signal.

---

## 8. Confidence Assessment and Gaps

### 8.1 What the record supports (not ownership-confirmed)

- ✅ Candidate brand-aligned handles were found on Bluesky, Tumblr, and Mastodon.
- ✅ A seven-handle Bluesky cluster is structurally consistent (same platform, brand prefix, rank naming).
- ✅ The naming convention `UTTP + faction` (THTDC, ZNTP, STR, mastdept) appears in extraction data.
- ✅ A named operator identifier (“Michael”) appears in UTTP TV branding data; this is not identity verification.

### 8.2 What Is Not Confirmed

- ❌ Whether the Bluesky cluster belongs to one operator or multiple.
- ❌ Whether any Tier 3 handle belongs to UTTP or to an unrelated user.
- ❌ Whether the `UTTP OFFICAL` (misspelled) handle is genuine or a copycat.
- ❌ Current activity status of any listed handle.
- ❌ Whether any listed handle is currently operated by the same person.

### 8.3 Rejection Breakdown

**Machine-readable CSV handle pass (2026-11-19):**

| Category | Count | Rule |
|---|---:|---|
| Platform-name variants in blocklist | 47 | V8 |
| Substring collisions ("butt" + p) | 18 | V2 |
| Substring collisions ("Uttapal" / personal names) | 16 | V2 |
| Fuzzy matches (`utp`, `Utti`, `Utop`) | 3 | V5 |
| Low-signal numeric (`uttp3`, `uttp333`) | 2 | V5 |
| **Total CSV handle values rejected** | **39** | — |

The 47 platform-name variants normalize to **37 unique keys**. None were present in the CSV handle fields; the blocklist is preventive.

**After rejection, the candidate set is:**

- 14 CSV-backed brand candidates
- 8 prior-extraction candidates not in the CSV
- **22 unique candidates**

Candidate means “structurally consistent,” not “confirmed account.” Ownership verified in this pass: **0**.

---

## 9. Methodology Limitations

This analysis is a manual pass on top of raw automated extraction. It is subject to the following limitations:

### 9.1 Substring Matching Remains the Primary Failure Mode

The extractor matches `uttp` at the character level. Any word containing `uttp` as a substring will produce a false positive. Known collision sources include `buttplug`, `buttp`, `Uttapal`, `Uttpal`, `smuttp`, `pnuttpad`. Further collisions are likely.

### 9.2 No Independent Verification Performed

Validation confirms that handle strings appear in the extraction output and pass structural rules. It does not confirm that any handle belongs to a real UTTP member, that the account is active, or that the account has done anything.

### 9.3 No Attribution to Individuals

Handles are not identities. A handle containing `uttp` may be a copycat, a parody, a compromised account, or an unrelated user with a coincidental name. **No individual should be identified as a UTTP member on the basis of a handle match alone.**

### 9.4 Cross-Platform Clustering Not Validated

The "linked" counts in the raw extraction mixed user-owned links with platform scaffolding. Any conclusion about how many platforms a single user appears on requires re-running the correlation with a corrected extractor.

---

## 10. Recommended Next Steps

| # | Action | Priority |
|---|---|---|
| 10.1 | **Patch extractor — reject substring collisions.** Implement exact-token match for `uttp` with word boundary. | Critical |
| 10.2 | **Patch extractor — separate link types.** Distinguish user-owned links from scaffolding (share buttons, SDKs, CDNs). | Critical |
| 10.3 | **Independently verify Tier 1 and Tier 2 handles.** Confirm each resolves to a live account, is UTTP-aligned, and check current activity. | High |
| 10.4 | **Do not publish Tier 3 without verification.** Tier 3 handles are single-source and may be unrelated individuals. | High |
| 10.5 | **Document collision sources.** Maintain a running list of substring collisions discovered during extraction so future analyses do not re-introduce them. | Medium |
| 10.6 | **Apply the platform-name blocklist before extraction/reporting.** Use `validation/styxnet_platform_name_blocklist.csv` and fail if a platform name is emitted as a handle. | Critical |
| 10.7 | **Separate profile paths from ownership.** Do not count `profile_path_unverified` rows as confirmed accounts. | High |

---

## 11. Appendix — Candidate Handle Index

### Tier 1 — Brand-Aligned Candidates (5)

```
uttp.tumblr.com
UTTP_OFFICAL
UTTPmastdept
frickfunnymikeuttpthtdc
kiloratstrzntputtp.bsky.social
```

### Tier 2 — Structured Cluster Candidates (7)

```
uttparkrosie.bsky.social
michaelsuttptv.bsky.social
uttpalette.bsky.social
uttpofficercoplord.bsky.social
uttp-lieutenant2.bsky.social
uttpus.bsky.social
kiloratstrzntputtp.bsky.social
```

### Tier 3 — Pattern-Matched, Single Source Candidates (11)

```
uttpower
kecuttpikding1970
vecuttpadi1981
uttpthdtc
demiurge-ash
chicken_hammer_bot
DarrenOfficial
pamegacorp
PA_Megacorp
safesurvival
safesurvivalofficial
```

---

## 📊 Summary Totals

| Metric | Count |
|---|---|
| **Total candidates** | **22** |
| **CSV handle values rejected** | **39** |
| **Platform-name variants blocklisted** | **47** (37 keys) |
| **Raw rows** | **823** |
| **Ownership verified** | **0** |

---

**END OF DOCUMENT**
