#!/usr/bin/env python3
"""Sync newly listed TEL entities into the entity intelligence intake list.

This is an intake layer, not a membership claim. New TEL entries are tracked as
leads until they are reviewed and assigned confidence.
"""
import json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / '18_ENTITY_TRACKING' / 'entity-intelligence.json'
OUT = ROOT / '20_LIVE_MONITORING' / 'tel_intake.json'
SITE = Path('/var/www/html/data/tel-intake.json')
API = os.environ.get('TEL_API', 'http://127.0.0.1:5004/api')
TOKEN = os.environ.get('OWNER_API_KEY')

def norm(s):
    return ''.join(ch for ch in (s or '').lower() if ch.isalnum())

def prefix(s, n=12):
    return norm(s)[:n]

data = json.loads(DATA.read_text(encoding='utf-8'))
SKIP = {'gatekeeper', 'wintergateintelligencecollectivewic', 'nintendeen'}
existing = {norm(e['name']) for e in data.get('entities', [])}
existing_prefixes = {prefix(e['name']) for e in data.get('entities', [])}

intake = []
if TOKEN:
    req = urllib.request.Request(API + '/entities', headers={'Authorization': 'Bearer ' + TOKEN})
    with urllib.request.urlopen(req, timeout=30) as resp:
        tel = json.loads(resp.read().decode())
    for e in tel.get('entities', []):
        name = e.get('name', '')
        if norm(name) in SKIP or norm(name) in existing or prefix(name) in existing_prefixes:
            continue
        intake.append({
            'tel_id': e.get('id'),
            'name': name,
            'type': e.get('entity_type', ''),
            'threat_level': e.get('threat_level', 'unknown'),
            'category': e.get('category', ''),
            'created_at': e.get('created_at', ''),
            'tags': e.get('tags', []),
            'status': 'intake',
            'confidence': 'D/S',
            'note': 'Newly listed in TEL. Tracked as an intake lead; not yet profiled in the entity register.',
        })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'count': len(intake), 'entries': intake}, indent=2) + '\n', encoding='utf-8')
if SITE.parent.exists():
    SITE.parent.mkdir(parents=True, exist_ok=True)
    SITE.write_text(OUT.read_text(encoding='utf-8'), encoding='utf-8')
print(json.dumps({'tel_entities': len(tel.get('entities', [])) if TOKEN else 0, 'new_intake': len(intake)}, indent=2))
