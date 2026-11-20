#!/usr/bin/env python3
"""Incremental discovery layer: sources, rebrands, and migration timing."""
import csv
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
OUT = BASE
DATA = BASE / 'entity-intelligence.json'
GENERAL_LIST = ROOT / '02_CORE_INVESTIGATION' / 'Members_List' / 'General_List_v2_Structured_2026-11-19.md'
AREA_REGISTER = ROOT / '02_CORE_INVESTIGATION' / 'AREA_INTELLIGENCE' / 'UTTP_AREA_REGISTER.csv'
STATE_PATH = OUT / 'discovery_state.json'
SOURCES_PATH = OUT / 'discovered_sources.json'
REBRANDS_PATH = OUT / 'rebrands.json'
MIGRATIONS_PATH = OUT / 'migration_events.json'
STYXNET_RAW = ROOT / '09_STYXNET_REPORTS' / 'styxnet_UTTP_csv_1789803261.csv'
STYXNET_PROFILES_PATH = OUT / 'styxnet_profiles.json'

URL_RE = re.compile(r'https?://[^\s\)\]\}"\'<>]+')
SCAN_GLOBS = [
    '00_READ_FIRST/*.md',
    '12_TRACKING/*.md',
    '13_UTTP_764_OVERLAP/*.md',
    '14_O9A_764_TRACE/*.md',
    '15_VALIDATED_CLAIMS/*.csv',
    '16_VALIDATED_FALSE_CLAIMS/*.csv',
    '17_CURRENT_STATE_PACKAGE/*.md',
    '18_ENTITY_MONITORING/*.md',
    '18_ENTITY_MONITORING/*.md',
    '02_CORE_INVESTIGATION/AREA_INTELLIGENCE/*.csv',
    '02_CORE_INVESTIGATION/Members_List/General_List_v2_Structured_2026-11-19.md',
]

TOKENS = {
    'UTTP': {'uttp', 'utube', 'troll', 'police'},
    'UTTP-EMPIRE': {'empire', 'nuuttp'},
    'CIRCUSFALL': {'circusfall'},
    'OFFICERSLAPPY': {'officerslappy', 'slappy', 'forum'},
    'AFR': {'afr', 'antifandomresistance'},
    'BN0R': {'bn0r', 'empire'},
    'RDF': {'rdf', 'reddit', 'defence', 'defense', 'rdfparty'},
    'DPOS': {'dpos', 'degeneracy', 'police', 'order', 'state'},
    '764': {'764'},
    'O9A': {'o9a', 'ona', 'nine', 'angles'},
    'HARMNATION': {'harmnation', 'harm'},
    'SPAWNISM': {'spawnism', 'spawn'},
    'FPE': {'fpe', 'fundamental', 'paper', 'education'},
    'FPE-POLICE': {'fpepolice', 'police'},
    'TNM': {'tnm', 'militia'},
    'ENCLAVE': {'enclave', 'imperium'},
}

ALIASES = {
    'uttputubetrollpolice': 'UTTP',
    'uttpempirenuuttp': 'UTTP-EMPIRE',
    'circusfallfaction': 'CIRCUSFALL',
    'officerslappyfactionuttpforum': 'OFFICERSLAPPY',
    'dposdegeneracypoliceorderstate': 'DPOS',
    'antifandomresistanceafr': 'AFR',
    'bn0rempire': 'BN0R',
    'redditdefenceforcerdf': 'RDF',
    'kktkkukluxtrollklan': 'KKTK',
    'yfga': 'YFGA',
    'vgcpvideogamecartoonpolice': 'VGCP',
    'affantifandomfront': 'AFF',
    'auttpantiuttp': 'AUTTP',
    '764': '764',
    'harmnation': 'HARMNATION',
    'o9aona': 'O9A',
    'spawnism': 'SPAWNISM',
    'fpepolice': 'FPE-POLICE',
    'fpeecosystem': 'FPE',
    'tnmthemilitia': 'TNM',
    '1481488': '148',
    'imperiumoftheenclavegrs': 'ENCLAVE',
}


def nkey(value):
    return re.sub(r'[^a-z0-9]+', '', (value or '').lower())


def norm_url(value):
    value = (value or '').strip().rstrip('.,;:').lower()
    value = re.sub(r'^https?://', '', value)
    value = re.sub(r'^www\.', '', value).rstrip('/')
    return value


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def domain_of(url):
    m = re.match(r'^(?:https?://)?(?:www\.)?([^/\s]+)', url or '')
    return m.group(1).lower() if m else ''


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return default


def scan_files():
    urls = {}
    files = {}
    for pattern in SCAN_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:
                continue
            try:
                text = path.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            rel = str(path.relative_to(ROOT))
            files[rel] = hashlib.sha256(text.encode('utf-8')).hexdigest()
            for raw in URL_RE.findall(text):
                url = raw.rstrip('.,;:')
                urls.setdefault(norm_url(url), {'url': url, 'files': set()})['files'].add(rel)
    for item in urls.values():
        item['files'] = sorted(item['files'])
    return files, urls


def read_register_names():
    names = []
    if not GENERAL_LIST.exists():
        return names
    section = None
    for line in GENERAL_LIST.read_text(encoding='utf-8').splitlines():
        if line.startswith('#'):
            section = line.lstrip('#').strip()
            continue
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 2:
            continue
        name = cells[0].strip()
        if not name or name.lower() in {'group', 'name', 'campaign', 'handle'} or set(name) <= set('-: '):
            continue
        if section and section.startswith(('2.', '3.')) and not section.startswith('###'):
            names.append(name)
    return names


def read_area_snapshot():
    snapshot = {}
    if not AREA_REGISTER.exists():
        return snapshot
    for row in csv.DictReader(AREA_REGISTER.open(newline='', encoding='utf-8')):
        platform = row.get('platform', '').strip()
        if not platform:
            continue
        item = snapshot.setdefault(platform, {'rows': 0, 'statuses': {}, 'confidence': row.get('confidence', '')})
        item['rows'] += 1
        status = row.get('presence_status', 'unknown')
        item['statuses'][status] = item['statuses'].get(status, 0) + 1
    return snapshot


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    state = load_json(STATE_PATH, {})
    state.setdefault('files', {})
    state.setdefault('discovered', {})
    state.setdefault('area_snapshot', {})
    state.setdefault('styxnet_profiles', {})
    state.setdefault('last_run', None)

    existing_urls = {norm_url(s.get('url', '')) for s in data.get('sources', []) if s.get('url')}
    existing_names = {nkey(e.get('name', '')) for e in data.get('entities', [])}
    existing_ids = {e['id'] for e in data.get('entities', [])}

    files, urls = scan_files()
    next_num = 1
    for item in state['discovered'].values():
        m = re.search(r'(\d+)$', item.get('id', ''))
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)

    stamp = now()
    added = 0
    for key, item in sorted(urls.items()):
        if key in existing_urls or key in state['discovered']:
            continue
        source_id = f'D{next_num:03d}'
        next_num += 1
        state['discovered'][key] = {
            'id': source_id,
            'url': item['url'],
            'domain': domain_of(item['url']),
            'first_seen': stamp,
            'last_seen': stamp,
            'source_files': item['files'],
        }
        added += 1
    state['files'] = files
    state['last_run'] = stamp

    discovered = sorted(state['discovered'].values(), key=lambda x: x['id'])
    SOURCES_PATH.write_text(json.dumps(discovered, indent=2) + '\n', encoding='utf-8')

    rebrands = []
    seen_rebrands = set()
    for name in read_register_names():
        key = nkey(name)
        mapped = ALIASES.get(key)
        if mapped and mapped in existing_ids:
            entity_id = mapped
        else:
            entity_id = None
            low = key
            for eid, tokens in TOKENS.items():
                if eid not in existing_ids:
                    continue
                if any(token in low for token in tokens):
                    entity_id = eid
                    break
        if not entity_id:
            continue
        pair = (entity_id, key)
        if pair in seen_rebrands:
            continue
        seen_rebrands.add(pair)
        rebrands.append({
            'name': name,
            'entity_id': entity_id,
            'basis': 'name_token',
            'first_seen': stamp,
        })
    REBRANDS_PATH.write_text(json.dumps(rebrands, indent=2) + '\n', encoding='utf-8')

    current_area = read_area_snapshot()
    migrations = []
    previous = state.get('area_snapshot') or {}
    if previous:
        for platform in sorted(set(previous) | set(current_area)):
            before = previous.get(platform)
            after = current_area.get(platform)
            if before is None and after is not None:
                migrations.append({'date': stamp, 'platform': platform, 'change': 'added_surface', 'detail': f'{after["rows"]} rows'})
            elif after is None and before is not None:
                migrations.append({'date': stamp, 'platform': platform, 'change': 'removed_surface', 'detail': f'{before["rows"]} rows'})
            elif before is not None and after is not None:
                if before['statuses'] != after['statuses']:
                    migrations.append({'date': stamp, 'platform': platform, 'change': 'status_change', 'detail': f'{before["statuses"]} -> {after["statuses"]}'})
    state['area_snapshot'] = current_area
    MIGRATIONS_PATH.write_text(json.dumps(migrations, indent=2) + '\n', encoding='utf-8')

    styxnet_profiles = []
    if STYXNET_RAW.exists():
        next_p = 1
        for item in state['styxnet_profiles'].values():
            m = re.search(r'(\d+)$', item.get('id', ''))
            if m:
                next_p = max(next_p, int(m.group(1)) + 1)
        existing_profiles = set(state['styxnet_profiles'])
        for row in csv.DictReader(STYXNET_RAW.open(newline='', encoding='utf-8')):
            if row.get('status') not in {'200', '206', '204'}:
                continue
            url = row.get('url', '')
            key = norm_url(url)
            if not key or key in existing_profiles:
                continue
            if any(marker in key for marker in ('/search', 'search?', 'keywords=', 'author=', '?q=', '&q=', 'query=', 'filter?search', '/find?', 'search-index')):
                continue
            pid = f'P{next_p:03d}'
            next_p += 1
            state['styxnet_profiles'][key] = {
                'id': pid,
                'url': url,
                'platform': row.get('platform', ''),
                'first_seen': stamp,
                'last_seen': stamp,
            }
            existing_profiles.add(key)
        styxnet_profiles = sorted(state['styxnet_profiles'].values(), key=lambda x: x['id'])
    STYXNET_PROFILES_PATH.write_text(json.dumps(styxnet_profiles, indent=2) + '\n', encoding='utf-8')

    STATE_PATH.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')

    print(json.dumps({
        'scanned_files': len(files),
        'new_sources': added,
        'discovered_sources_total': len(discovered),
        'rebrands': len(rebrands),
        'migration_events': len(migrations),
        'styxnet_profiles': len(styxnet_profiles),
    }, indent=2))


if __name__ == '__main__':
    main()
