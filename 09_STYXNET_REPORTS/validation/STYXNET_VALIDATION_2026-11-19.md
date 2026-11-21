# StyxNet Validation — 2026-11-19

**Status:** accuracy review of `09_STYXNET_REPORTS/`
**Raw export:** `styxnet_UTTP_csv_1789803261.csv`
**Raw SHA-256:** `fa3b9dfad46da9db644d26be13cf5e23555c791ea7cfae6c241b6ef1ae92a858`
**Raw rows:** 823 (`761` exact, `62` similarity)
**Rule:** raw exports are preserved unchanged; this pass produces a corrected,
machine-readable review layer. No ownership is confirmed.

> **No target list. No private individuals. No operational instructions.**
> This is a data-quality review for researchers, platforms, and lawful
> authorities. It does not authorise contact, infiltration, or retaliation.

---

## 1. What was wrong

The raw StyxNet export contains three different things mixed together:

1. **Target-string profile URLs** — a URL contains `UTTP`, but that does not prove
   the account belongs to UTTP or has any connection to it.
2. **Search, login, error, and gated pages** — query pages and login walls that
   contain `UTTP` in the URL but are not profiles.
3. **Handle-like strings from page metadata** — platform names, UI labels, and
   unrelated words that contain the letters `u-t-t-p`.

The earlier README recorded a manual rejection list, but the list had a count
error: it called the platform-name section **48** entries when the supplied list
contains **47** variants. The raw export also describes **823 rows**, not 823
profiles.

This pass fixes the count, makes the blocklist machine-readable, and separates
**profile-path candidates** from **confirmed ownership**.

---

## 2. Platform-name blocklist

The platform list is now a blocklist, not a handle list:

- **47 variants**
- **37 unique normalized keys** (some variants collapse, e.g. `HackThisSite.org`,
  `hackthissite`, `HackThisSite`)
- **0 platform names in the candidate handle output**

File: [`styxnet_platform_name_blocklist.csv`](styxnet_platform_name_blocklist.csv)

Examples of canonical mappings:

| Variant(s) | Canonical platform |
| --- | --- |
| `Codecademy` | Codecademy |
| `codersrank-org`, `codersrank` | CodersRank |
| `thesimsresourcedotcom`, `TheSimsResource` | The Sims Resource |
| `livetrack24`, `LiveTrack24` | LiveTrack24 |
| `HackThisSite.org`, `hackthissite`, `HackThisSite` | HackThisSite |
| `MAGIX_INT`, `MAGIX`, `magix` | MAGIX |
| `WynkMusic`, `wynkmusic` | Wynk Music |
| `Salon24pl`, `salon24.pl` | Salon24 |
| `FlashFlashRevolution`, `TheOfficial_FFR`, `ffr` | FlashFlashRevolution |
| `Podcastindex-org`, `PodcastindexOrg` | Podcast Index |
| `subscan_io` | Subscan |
| `stackernews` | Stacker News |
| `cssbattle.dev`, `css_battle` | CSSBattle |
| `coddytech`, `coddy.tech`, `coddylearn`, `coddy_tech` | Coddy |
| `flyertalkforums`, `FlyerTalk` | FlyerTalk |
| `prokoni.ru`, `prokoni_ru` | Prokoni |
| `car72ru`, `wwwcar72ru` | Car72 |
| `LancerX.ru`, `LancerX_ru` | LancerX |
| `TTSPORT.ru` | TTSPORT |
| `poembook_ru` | Poembook |
| `maccentre_ru` | MacCentre |
| `yamaya_ru` | Yamaya |
| `radiomedru` | Radiomed |
| `romanticcollectionru` | RomanticCollection |
| `bysoloby` | BySoloby |

**Rule:** if a candidate handle normalizes to a blocklist key, it is rejected as
`platform_identity_string`. It is not a user handle.

---

## 3. Handle-level validation

The raw export has **54 unique handle values** across the `aliases` and
`similar_username` fields. Applying strict structural rules produces:

| Outcome | Count | Meaning |
| --- | ---: | --- |
| Candidate — brand token or cluster | 14 | Structurally consistent with UTTP branding; **not ownership-confirmed** |
| Candidate — exact target only | 1 | The literal string `uttp`; no alignment evidence |
| Rejected — `butt*` collision | 18 | `uttp` spans an unrelated word |
| Rejected — Uttapal/name collision | 16 | Unrelated personal name containing `uttp` |
| Rejected — fuzzy match | 3 | `utp`, `Utti`, `Utop` are not exact |
| Rejected — low-signal numeric | 2 | `uttp3`, `uttp333` |
| **Total** | **54** | |

Files:

- [`styxnet_handle_candidates.csv`](styxnet_handle_candidates.csv) — candidates only.
- [`styxnet_handle_class_counts.csv`](styxnet_handle_class_counts.csv) — counts by class.
- [`validate_styxnet.py`](validate_styxnet.py) — reproducible script.

### Candidate tiers

| Tier | Handles | Confidence |
| --- | ---: | --- |
| Tier 1 — brand/faction token | 3 | **A** structural |
| Tier 2 — Bluesky cluster | 7 | **A** structural |
| Tier 3 — single-source brand token | 4 | **S** unverified |
| Target-only | 1 | **S** |
| **Total** | **15** | No `E`-level ownership |

The earlier README's **22 candidates** combine **14 CSV-backed brand candidates**
and **8 prior-extraction candidates** that are not in this CSV (including the
Tumblr subdomain and the seven prior Tier 3 handles). The README also lists
**11** Tier 3 entries while labelling the tier as 10; the unique count is what
matters. This pass does not re-verify those eight; they remain leads.

---

## 4. Row-level validation

The 823 rows are not 823 profiles. Structural classification:

| Row class | Count | What it means |
| --- | ---: | --- |
| `profile_path_unverified` | 580 | URL contains a target-string path segment; ownership unverified |
| `error_or_gated_page` | 108 | Login walls, errors, bot checks, 404s, or non-200 |
| `non_profile_artifact` | 1 | Mislabeled npm row pointing at a GitHub repository |
| `search_or_query_page` | 48 | Search/query/filter/author pages |
| `gated_or_generic_page` | 6 | Generic information/search/login page |
| `duplicate_url` | 7 | Repeated normalized URLs after the first occurrence |
| `unclear` | 73 | Needs manual review |
| **Total** | **823** | |

File: [`styxnet_row_class_counts.csv`](styxnet_row_class_counts.csv)

**Important:** `profile_path_unverified` is **not** a validated account. It means
the URL looks like a profile path and contains the target string. It may be an
unrelated person, a brand squatter, a viewer page, or a dead account. The raw
export includes no live ownership check.

**Ownership verified in this pass: 0.**

---

## 5. Corrections to the earlier README

| Earlier wording | Correction |
| --- | --- |
| “48 platform-name entries” | **47 variants / 37 normalized keys** |
| “760 primary detections” | **761 exact rows + 62 similarity rows = 823 rows**; 760 unique platform labels |
| “Profiles: 823” in the raw StyxNet markdown | **Rows: 823**, not 823 profiles |
| “22 validated findings” | **22 candidates**, not confirmed ownership |
| Tier 3 “10” | The README lists **11** Tier 3 entries; unique total is 22 after de-duplication |
| “Confirmed” in Tier 1 heading | **Candidate**, unless a live account check is attached |

---

## 6. What this does not prove

- That any candidate handle is controlled by UTTP or a UTTP member.
- That a profile is active, authentic, or currently aligned.
- That two accounts share an operator.
- That a username contains a real name or location.
- That the raw export is complete or unbiased.

A handle is a string. It is not an identity.

---

## 7. Reproduce

```bash
python3 09_STYXNET_REPORTS/validation/validate_styxnet.py
```

The script:

1. reads the raw CSV read-only;
2. applies the platform-name blocklist;
3. classifies handles and rows;
4. writes the candidate/blocklist/count files;
5. fails if a platform name leaks into the candidate output.

---

## 8. Next steps

1. Apply the blocklist and row classes in the extractor before generating future
   reports.
2. Add a `platform_url_mismatch` check for rows where the platform label and URL
   host disagree (for example, an “npm” row pointing at a GitHub repository).
3. Verify Tier 1/Tier 2 candidates live, with screenshots and timestamps, before
   calling them confirmed.
4. Keep rejected personal-name collisions out of public summaries; use patterns,
   not names.
5. Do not publish Tier 3 candidates as UTTP-linked without independent evidence.

---

## 9. Citation

> WIC, *StyxNet Validation — 2026-11-19*, `09_STYXNET_REPORTS/validation/`, 2026-11-19.

For the raw export, cite `09_STYXNET_REPORTS/styxnet_UTTP_csv_1789803261.csv` and
this validation layer separately.
