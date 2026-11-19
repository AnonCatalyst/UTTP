# StyxNet Validation Layer

**Prepared:** 2026-11-19
**Raw export:** `../styxnet_UTTP_csv_1789803261.csv` (unchanged)

This folder is a data-quality review of the StyxNet export. It does not confirm
ownership, membership, or intent.

## Read first

- [`STYXNET_VALIDATION_2026-11-19.md`](STYXNET_VALIDATION_2026-11-19.md) — findings, corrections, limits.

## Files

| File | Use |
| --- | --- |
| `styxnet_platform_name_blocklist.csv` | 47 platform-name variants (37 normalized keys); reject before treating a string as a handle. |
| `styxnet_handle_candidates.csv` | 15 structural candidates; not ownership-confirmed. |
| `styxnet_handle_class_counts.csv` | 54 unique handle values by class. |
| `styxnet_row_class_counts.csv` | 823 rows by structural class. |
| `styxnet_validation_summary.json` | Machine-readable counts and raw-file SHA-256. |
| `validate_styxnet.py` | Reproducible validator; fails if a platform name leaks into candidates. |

## Run

```bash
python3 09_STYXNET_REPORTS/validation/validate_styxnet.py
```

## Rule

A platform name is not a handle. A profile path is not an owned account. A
candidate is not a confirmed identity.
