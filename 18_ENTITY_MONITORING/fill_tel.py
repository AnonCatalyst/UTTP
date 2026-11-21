#!/usr/bin/env python3
"""Fill or update TEL from the group-level entity intelligence register.

This is idempotent: existing entities are updated, new entities are created, and
no personal identifiers are published.
"""
import json, os, re, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DATA = BASE / 'entity-intelligence.json'
API = os.environ.get('TEL_API', 'http://127.0.0.1:5004/api')
TOKEN = os.environ.get('OWNER_API_KEY')
if not TOKEN:
    raise SystemExit('OWNER_API_KEY is required')

def norm(s):
    return ''.join(ch for ch in (s or '').lower() if ch.isalnum())

def req(path, method='GET', body=None):
    url = API + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header('Content-Type', 'application/json')
    r.add_header('Authorization', 'Bearer ' + TOKEN)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors='replace')
        raise RuntimeError(f'{method} {path}: HTTP {e.code}: {msg}') from e

def threat_level(e):
    score = e.get('learning', {}).get('risk_score', 0)
    if e['id'] in {'764', 'O9A'}:
        return 'critical'
    if e['watch_priority'] == 'high' and e['confidence'] in {'E', 'C'}:
        return 'high'
    if e['watch_priority'] == 'high':
        return 'medium'
    if score >= 0.7:
        return 'high'
    if score >= 0.45:
        return 'medium'
    return 'low'

def entity_type(e):
    mapping = {
        'harassment brand/network': 'Harassment Network',
        'hardcore UTTP offshoot': 'Offshoot Network',
        'designated NVE network': 'Designated NVE Network',
        'designated occult/NVE network': 'Designated NVE Network',
        '2026 faction/revival': 'Offshoot Faction',
        '2026 faction': 'Offshoot Faction',
        '2026 splinter': 'Splinter Group',
        '2026 subgroup': 'Subgroup',
        '2025-2026 revival': 'Revival Faction',
        'target ecosystem': 'Target Ecosystem',
        'role-play/AU brand': 'Role-Play Brand',
        'adjacent network': 'Adjacent Network',
        'affiliate/lead': 'Lead Entity',
        'offshoot/lead': 'Lead Entity',
        'historical group': 'Historical Group',
        'historical splinter': 'Historical Splinter',
        'historical opposition': 'Historical Opposition',
        'opposition/adjacent': 'Opposition Group',
        'opposition coalition': 'Opposition Coalition',
        'opposition': 'Opposition Group',
        'self-harm/recruitment cult': 'Adjacent Cult',
        '764 offshoot': '764 Offshoot',
        'legacy archive label': 'Archive Label',
        'defence/blacklist platform': 'Defence Platform',
        'documenter': 'Documenter',
    }
    return mapping.get(e['type'], e['type'][:50])

def category(e):
    if e['id'] in {'764', 'O9A', 'HARMNATION'}:
        return 'NVE Ecosystem'
    if e['id'] in {'UTTP', 'UTTP-EMPIRE', 'CIRCUSFALL', 'OFFICERSLAPPY', 'AFR', 'BN0R', 'RDF', 'DPOS'}:
        return 'UTTP Ecosystem'
    if e['id'] in {'FPE', 'FPE-POLICE'}:
        return 'Target Ecosystem'
    if e['id'] in {'GATEKEEPER', 'WIC'}:
        return 'Defence'
    return 'Adjacent Ecosystem'

def tags_for(e):
    tags = [e['id'], e['confidence'], e['watch_priority'], 'group-level', 'no-target-list']
    tags += [t[:100] for t in e.get('tactics', [])[:8]]
    return [t for t in tags if t][:25]

def description_for(e):
    parts = [e['summary'], 'Current state: ' + e['current_state']]
    if e.get('not_supported'):
        parts.append('Not supported: ' + '; '.join(e['not_supported'][:4]))
    return ' '.join(parts)[:1900]

def find_existing(existing, name):
    key = norm(name)
    for e in existing:
        if norm(e['name']) == key:
            return e
    # Fuzzy prefix match for renamed historical records.
    prefix = key[:12]
    matches = [e for e in existing if norm(e['name'])[:12] == prefix]
    if len(matches) == 1:
        return matches[0]
    return None

data = json.loads(DATA.read_text(encoding='utf-8'))
existing = req('/entities').get('entities', [])
offshoot_ids = {'DPOS', 'CIRCUSFALL', 'OFFICERSLAPPY', 'AFR', 'BN0R', 'RDF', 'RDFPARTY'}
uttp_id = None
for e in existing:
    if norm(e['name'])[:12] == norm('UTTP / UTube Troll Police')[:12]:
        uttp_id = e['id']
        break

created = []
updated = []
for e in data['entities']:
    body = {
        'name': e['name'],
        'entity_type': entity_type(e),
        'category': category(e),
        'title': e['name'],
        'description': description_for(e),
        'threat_level': threat_level(e),
        'tags': tags_for(e),
        'links': [{'title': 'Archive record', 'url': 'https://github.com/WinterGate-IC/UTTP'}],
        'notes': [{'content': 'Group-level entity from the UTTP archive. ' + e['summary'][:1500]}],
    }
    if e['id'] in offshoot_ids and uttp_id:
        body['parent_clusters'] = [{'parent_cluster_id': uttp_id, 'parent_name': 'UTTP / UTube Troll Police', 'is_primary_parent': 1}]
    match = find_existing(existing, e['name'])
    if match:
        req(f"/entities/{match['id']}", 'PUT', body)
        updated.append((e['id'], match['id'], e['name']))
        print(f"updated {e['id']} -> TEL id {match['id']}: {e['name']}")
    else:
        resp = req('/entities', 'POST', body)
        created.append((e['id'], resp.get('id'), e['name']))
        print(f"created {e['id']} -> TEL id {resp.get('id')}: {e['name']}")

existing = req('/entities').get('entities', [])
monitor_path = BASE / 'monitor_feed.json'
site_monitor = Path('/var/www/html/data/monitor-feed.json')
feed = {}
if monitor_path.exists():
    feed = json.loads(monitor_path.read_text(encoding='utf-8'))
feed['updated'] = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
feed['tel_records'] = len(existing)
monitor_path.parent.mkdir(parents=True, exist_ok=True)
monitor_path.write_text(json.dumps(feed, indent=2) + '\n', encoding='utf-8')
if site_monitor.parent.exists():
    site_monitor.parent.mkdir(parents=True, exist_ok=True)
    site_monitor.write_text(json.dumps(feed, indent=2) + '\n', encoding='utf-8')

print('created', len(created))
print('updated', len(updated))
print('tel_records', len(existing))
