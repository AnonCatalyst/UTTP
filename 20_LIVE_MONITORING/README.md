# Live Monitoring — Automated Entity Intelligence

**Prepared:** 2026-11-19
**Mode:** automated, resource-aware, group-level

> **No target list. No private identifiers.** This folder monitors public sources
> and archive-derived intelligence. It does not authorise contact, infiltration,
> or retaliation.

## Files

| File | Use |
| --- | --- |
| `monitor.py` | Lightweight source-watch feed using StyxNet and critical source URLs. |
| `run_pipeline.py` | Runs strict validation, monitoring, TEL fill, and JSON build. |
| `run_pipeline.sh` | Environment-aware wrapper that sources the TEL owner key. |
| `monitor_feed.json` | Latest source-watch feed. |

## Automation

- Pipeline: every 15 minutes via cron.
- Page: auto-refresh every 60 seconds.
- TEL: auto-filled from the entity intelligence register.
- StyxNet: overtime monitoring counts and source-watch results are exposed in the
  page.

## Safety boundary

This is monitoring and documentation automation. It is not enforcement, not a
target list, and not an instruction to contact or act against anyone.
