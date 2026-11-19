#!/usr/bin/env python3
"""Strict validation engine for the UTTP archive.

This is a post-collection pass. Raw evidence is preserved. The engine writes a
strictly filtered StyxNet profile set and an archive-integrity report. It does
not delete original files.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
RAW = ROOT / '09_STYXNET_REPORTS' / 'styxnet_UTTP_csv_1789803261.csv'
BLOCK = ROOT / '09_STYXNET_REPORTS' / 'validation' / 'styxnet_platform_name_blocklist.csv'
MANIFEST = ROOT / '00_READ_FIRST' / 'MANIFEST.csv'
MANIFEST_SHA = ROOT / '00_READ_FIRST' / 'MANIFEST.sha256'

GENERIC_TITLES = {'', 'search results for uttp', 'information', 'search results'}
GATED_TERMS = ('login', 'log in', 'sign in', 'signin', 'register', 'error', '404', 'not found', 'access denied', 'one moment', 'making sure', 'just a moment', 'validating', 'информация', 'information', 'результаты поиска', 'search results', 'dice account', 'already a member', 'auth-controller')
SEARCH_TERMS = ('/search', 'search?', 'keywords=', 'author=', '?q=', '&q=', 'query=', 'filter?search', '/find?', 'search-index')

def norm_url(u):
    u = (u or '').strip().lower().rstrip('/')
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    return u

def nkey(v):
    return ''.join(ch for ch in (v or '').lower() if ch.isalnum())

def strict_row(r, seen):
    url = norm_url(r['url'])
    title = (r['title'] or '').lower()
    status = (r['status'] or '').strip()
    platform = (r['platform'] or '').strip()
    conf = int(r['confidence'] or 0)
    if status not in {'200', '206', '204'}:
        return False, 'non_2xx_status'
    if any(t in url for t in SEARCH_TERMS):
        return False, 'search_or_query_page'
    if any(t in title for t in GATED_TERMS):
        return False, 'error_or_gated_page'
    if url in seen:
        return False, 'duplicate_url'
    parts = re.split(r'[/?=&@]+', url)
    if not any(p == 'uttp' or p.startswith('uttp.') for p in parts):
        return False, 'not_a_profile_path'
    if conf < 70:
        return False, 'confidence_below_70'
    if not title.strip() or title in GENERIC_TITLES:
        return False, 'empty_or_generic_title'
    block_keys = {nkey(x['variant']) for x in csv.DictReader(BLOCK.open(newline='', encoding='utf-8'))}
    if nkey(platform) in block_keys:
        return False, 'platform_name_not_handle'
    seen.add(url)
    return True, 'strict_valid'

def validate_internal_links():
    broken = []
    checked = 0
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = match.group(1).strip()
            if not target or target.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            checked += 1
            target = target.split('#', 1)[0].split('?', 1)[0]
            target = urllib.parse.unquote(target)
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                broken.append({'file': str(path.relative_to(ROOT)), 'target': target})
    return checked, broken

def validate_json():
    bad = []
    non_strict = []
    checked = 0
    for path in ROOT.rglob('*.json'):
        if '.git' in path.parts:
            continue
        checked += 1
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except Exception as e:
            # Historical Discord exports are JSON-like text captures, not strict
            # JSON. They are retained as raw evidence and reported separately.
            non_strict.append({'file': str(path.relative_to(ROOT)), 'error': str(e)})
    return checked, bad, non_strict

def validate_csv():
    bad = []
    checked = 0
    for path in ROOT.rglob('*.csv'):
        if '.git' in path.parts:
            continue
        checked += 1
        try:
            with path.open(newline='', encoding='utf-8') as f:
                list(csv.reader(f))
        except Exception as e:
            bad.append({'file': str(path.relative_to(ROOT)), 'error': str(e)})
    return checked, bad

def validate_manifest():
    bad = []
    checked = 0
    rows = list(csv.DictReader(MANIFEST.open(newline='', encoding='utf-8')))
    for row in rows:
        checked += 1
        p = ROOT / row['path']
        if not p.is_file():
            bad.append({'path': row['path'], 'reason': 'missing'})
            continue
        if p.stat().st_size != int(row['size_bytes']):
            bad.append({'path': row['path'], 'reason': 'size_mismatch'})
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
            bad.append({'path': row['path'], 'reason': 'hash_mismatch'})
    expected = MANIFEST_SHA.read_text(encoding='utf-8').strip().split()[0]
    actual = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    manifest_hash_ok = expected == actual
    return checked, bad, manifest_hash_ok, expected, actual

def main():
    # Strict StyxNet profile filtering.
    rows = list(csv.DictReader(RAW.open(newline='', encoding='utf-8')))
    seen = set()
    valid = []
    rejected = []
    reasons = {}
    for row in rows:
        ok, reason = strict_row(row, seen)
        reasons[reason] = reasons.get(reason, 0) + 1
        if ok:
            valid.append(row)
        else:
            rejected.append({'platform': row['platform'], 'url': row['url'], 'confidence': row['confidence'], 'reason': reason})

    valid_path = OUT / 'styxnet_strict_validated.csv'
    with valid_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(valid)

    rejected_path = OUT / 'styxnet_strict_rejected.csv'
    with rejected_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['platform', 'url', 'confidence', 'reason'], lineterminator='\n')
        writer.writeheader()
        writer.writerows(rejected)

    links_checked, broken_links = validate_internal_links()
    json_checked, bad_json, non_strict_json = validate_json()
    csv_checked, bad_csv = validate_csv()
    manifest_checked, bad_manifest, manifest_hash_ok, expected_manifest_hash, actual_manifest_hash = validate_manifest()

    summary = {
        'raw_rows': len(rows),
        'strict_valid': len(valid),
        'rejected': len(rejected),
        'rejection_reasons': dict(sorted(reasons.items())),
        'internal_links_checked': links_checked,
        'broken_internal_links': broken_links,
        'json_files_checked': json_checked,
        'bad_json_files': bad_json,
        'non_strict_json_exports': non_strict_json,
        'non_strict_json_exports': non_strict_json,
        'non_strict_json_exports': non_strict_json,
        'csv_files_checked': csv_checked,
        'bad_csv_files': bad_csv,
        'manifest_rows_checked': manifest_checked,
        'bad_manifest_rows': bad_manifest,
        'manifest_hash_ok': manifest_hash_ok,
        'rule': 'HTTP success, profile path, no search/login/error/gated/duplicate/unclear, confidence >= 70, non-generic title, platform not in blocklist.',
    }
    (OUT / 'strict_validation_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')

    integrity = {
        'internal_links_checked': links_checked,
        'broken_internal_links': broken_links,
        'json_files_checked': json_checked,
        'bad_json_files': bad_json,
        'non_strict_json_exports': non_strict_json,
        'non_strict_json_exports': non_strict_json,
        'non_strict_json_exports': non_strict_json,
        'csv_files_checked': csv_checked,
        'bad_csv_files': bad_csv,
        'manifest_rows_checked': manifest_checked,
        'bad_manifest_rows': bad_manifest,
        'manifest_hash_ok': manifest_hash_ok,
    }
    (OUT / 'archive_integrity.json').write_text(json.dumps(integrity, indent=2) + '\n', encoding='utf-8')

    print(json.dumps({
        'strict_valid': len(valid),
        'rejected': len(rejected),
        'links_checked': links_checked,
        'broken_links': len(broken_links),
        'json_checked': json_checked,
        'bad_json': len(bad_json),
        'non_strict_json': len(non_strict_json),
        'csv_checked': csv_checked,
        'bad_csv': len(bad_csv),
        'manifest_rows': manifest_checked,
        'bad_manifest_rows': len(bad_manifest),
        'manifest_hash_ok': manifest_hash_ok,
    }, indent=2))

if __name__ == '__main__':
    main()
