# Data Dictionary

This describes the formats in the archive. It does not alter any raw file.

## File families

| Type | Where | Notes |
| --- | --- | --- |
| Markdown dossiers/reports | `02_*`, `09_*`, `10_*`, `11_*` | Human-readable analysis. Check claim ledger before citing. |
| JSON exports | `02_CORE_INVESTIGATION/Members_List/`, `10_SOURCES/` | Some are strict JSON; some are exported text with JSON-like structure. Validate before parsing. |
| CSV exports | `09_STYXNET_REPORTS/` | StyxNet OSINT table; header fields are described below. |
| User/ID text lists | `07_*`, `08_*`, `03_*` | Plain text exports; lines vary. Treat IDs as historical identifiers only. |
| RAR multipart archives | `03_*`, `08_*` | Part files belong together; do not extract one part in isolation. |
| Images/video | `03_*`, `04_*`, `06_*`, `07_*` | Historical captures/media. Content warnings apply. |
| PDF/DOCX | `02_*`, `04_*`, `07_*` | Reports and notices. |
| Manifest | `00_READ_FIRST/MANIFEST.csv` | Current files, size, SHA-256. |

## StyxNet CSV header

`09_STYXNET_REPORTS/styxnet_UTTP_csv_1789803261.csv` begins:

```text
search_type,platform,handle,similar_username,url,confidence,title,bio,display_name,user_id,verified,status,aliases
```

- `search_type`: match type (e.g. exact).
- `platform`, `handle`, `url`: public profile surface.
- `confidence`: source confidence score as exported; not WIC verification.
- `user_id`: platform identifier when the export captured one; historical.
- `aliases`: delimiter/encoding varies.

## Text indicator lists

Plain-text exports in `Members_List`, `DTAD 2025`, and `07_DONATED_DOCUMENTS`
use different layouts. Common patterns:

- section headers in `[BRACKETS]`
- one public handle or ID per line
- pipe-delimited rows such as `id | username | note`
- free-text notes from donors

Do not assume a single schema. The archive preserves the original export
format because normalising it would destroy provenance.

## JSON caution

Not every `.json` file is strict JSON. Some are JSON-with-notes or exported
text. `python -m json.tool` is the quick validation test. If a file fails,
treat it as text and read it with its source context; do not rewrite the raw
file.

## Multipart RAR sets

Sets such as `data.part01.rar` … `data.part05.rar` and `148corps.part1.rar` …
`part3.rar` must be kept together. Check the set is complete before extraction;
names and sizes are in `MANIFEST.csv`.

## Manifest schema

`MANIFEST.csv`:

```text
path,size_bytes,sha256
```

The manifest covers the working tree at the time of generation and excludes
`.git/`. `MANIFEST.sha256` contains the hash of the manifest itself.

## Identifiers and privacy

Historical IDs/usernames are preserved for provenance. They are not an
invitation to contact or expose anyone. Do not join private spaces, message
accounts, or publish new personal data from the archive.
