# Entity Intelligence — Group-Level Monitoring Board

**Prepared:** 2026-11-19
**Public page:** https://wintergate.org/entities.html
**Portal jump:** `/entities.html` from `portal.html`

> **No target list. No private identifiers.** This folder contains group-level
> entity data, sources, areas, claims, and a generator. It does not contain
> usernames, account IDs, invite links, victim data, or personal identifiers.

## Files

| File | Use |
| --- | --- |
| `entity-intelligence.json` | Machine-readable entity, source, area, claim, and watchlist data. |
| `build_entity_intelligence.py` | Rebuilds the JSON from archive registers and source lists. |
| `README.md` | This note. |

## What the page does

- Loads the JSON and renders an interactive entity registry.
- Search, type filter, confidence filter.
- Click an entity for overview, evolution, areas, tactics, claims, sources, full
  tracking record, and a rule-based learning model.
- Shows a source library, area intelligence, and claim ledger.
- “Run learning model” recomputes adaptive scores from the current data.

## Automation

```bash
python3 18_ENTITY_TRACKING/build_entity_intelligence.py
```

The script reads:

- `02_CORE_INVESTIGATION/AREA_INTELLIGENCE/UTTP_AREA_REGISTER.csv`
- `15_VALIDATED_CLAIMS/VALIDATED_CLAIMS.csv`
- `16_VALIDATED_FALSE_CLAIMS/FALSE_CLAIMS.csv`
- `17_CURRENT_STATE_PACKAGE/OFFSHOOT_WATCHLIST.csv`

It writes:

- `18_ENTITY_TRACKING/entity-intelligence.json`
- `/var/www/html/data/entity-intelligence.json` if the web root exists.

## Safety boundary

This is group-level intelligence. Areas are platforms/surfaces, not people.
Handles are leads, not identities. A confidence label is not proof of
membership or command.
