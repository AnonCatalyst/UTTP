# Validated False Claims — Quarantine

**Prepared:** 2026-11-19
**Purpose:** hold false, superseded, or unsupported claims that were removed from
current documents, so the archive can correct itself without silently deleting
the record.

> **This is not a target list and not a claim that the archive is finished.**
> It is a quarantine register. A claim in this folder is not approved for reuse.

## What belongs here

- Claims marked **X** in `00_READ_FIRST/CLAIM_LEDGER.md`.
- Superseded numbers (for example, “10 GB total / 4 GB remaining”).
- Claims that failed source review (for example, “FBI Tier 1”).
- Structural claims that overstate command (for example, “O9A parent entity” or
  “UTTP is an operational arm of 764”).
- Counting errors (for example, “823 profiles” or “48 platform-name entries”).

Unverified leads that are still being actively investigated and have not been
rejected stay labelled `A/S/D` in the working folders. Claims that are rejected,
not established, or failed source review are quarantined here.

## Files

| File | Use |
| --- | --- |
| [`FALSE_CLAIMS.csv`](FALSE_CLAIMS.csv) | Machine-readable register: claim, status, reason, correction, location. |
| [`QUARANTINE.md`](QUARANTINE.md) | Human-readable grouped record of the quarantined claims. |
| [`README.md`](README.md) | This rule sheet. |

## Handling rule

Do not copy a quarantined claim back into a public analysis as fact. If it is
needed for context, quote it explicitly as a **rejected claim** and link here.

## Relationship to the claim ledger

`00_READ_FIRST/CLAIM_LEDGER.md` remains the master status table. This folder holds
the rejected text that was stripped from the documents; the ledger holds the
status and correction. The two should agree.
