#!/usr/bin/env python3
"""Regenerate the archive manifest after automated pipeline updates."""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / '00_READ_FIRST' / 'MANIFEST.csv'
MANIFEST_SHA = ROOT / '00_READ_FIRST' / 'MANIFEST.sha256'

rows = []
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():
        continue
    if '.git' in path.parts or '__pycache__' in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel in {'00_READ_FIRST/MANIFEST.csv', '00_READ_FIRST/MANIFEST.sha256'}:
        continue
    rows.append((rel, path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()))

with MANIFEST.open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['path', 'size_bytes', 'sha256'])
    writer.writerows(rows)

MANIFEST_SHA.write_text(hashlib.sha256(MANIFEST.read_bytes()).hexdigest() + '  MANIFEST.csv\n', encoding='utf-8')
print({'manifest_rows': len(rows)})
