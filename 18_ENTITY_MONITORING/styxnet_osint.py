#!/usr/bin/env python3
"""Passive StyxNet OSINT poller.

Polls cached username hunts and, when the service is idle, starts one shallow
hunt at a time. Findings are group-level leads only; no ownership is inferred.
"""
import json
import re
import sqlite3
import time
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
STATE_PATH = BASE / 'styxnet_osint_state.json'
OUT = BASE / 'styxnet_osint.json'
DB = Path('/opt/wintergate/styxnet_data/styxnet.db')
API = 'http://127.0.0.1:9980'
TARGETS = [
    'uttp', 'uttp_thdtc', 'uttp_offical', 'dpos', 'fpe', '764', 'o9a',
    'spawnism', 'circusfall', 'officerslappy', 'afr', 'rdf', 'bn0r',
]
HUNT_INTERVAL_HOURS = 6
POLL_TIMEOUT = 8
HUNT_TIMEOUT = 70


def now():
    return datetime.now(timezone.utc)


def stamp():
    return now().strftime('%Y-%m-%dT%H:%M:%SZ')


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            return default
    return default


def token():
    if not DB.exists():
        return None
    try:
        conn = sqlite3.connect(str(DB))
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT access_token FROM users WHERE role='owner' AND is_active=1 LIMIT 1").fetchone()
        if not row:
            row = conn.execute("SELECT access_token FROM users WHERE username='AnonCatalyst' LIMIT 1").fetchone()
        conn.close()
        return row['access_token'] if row else None
    except Exception:
        return None


def auth_headers(tok):
    return {'Authorization': 'Bearer ' + tok}


def get_json(url, tok=None, timeout=POLL_TIMEOUT):
    headers = auth_headers(tok) if tok else {}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def health():
    try:
        return get_json(API + '/api/health', timeout=5)
    except Exception:
        return {}


def poll_results(username, tok):
    try:
        return get_json(f'{API}/api/username-search/results?username={username}', tok)
    except Exception:
        return {}


def run_hunt(username, tok):
    url = (f'{API}/api/username-search/stream?username={username}&depth=0'
           f'&max_concurrency=2&sim_thresh=0.80&token={tok}')
    findings = []
    try:
        req = urllib.request.Request(url, headers=auth_headers(tok))
        with urllib.request.urlopen(req, timeout=HUNT_TIMEOUT) as r:
            for raw in r:
                line = raw.decode('utf-8', 'replace').strip()
                if not line.startswith('data: '):
                    continue
                try:
                    event = json.loads(line[6:])
                except Exception:
                    continue
                if event.get('type') == 'result':
                    findings.append(event)
    except Exception:
        pass
    return findings


def main():
    tok = token()
    state = load_json(STATE_PATH, {'findings': {}, 'last_hunt': None, 'last_target': None})
    state.setdefault('findings', {})
    if not tok:
        print(json.dumps({'skipped': 'no StyxNet token'}))
        return

    h = health()
    active = int(h.get('streams', {}).get('hunts_active', 0) or 0)
    new = 0
    for username in TARGETS:
        data = poll_results(username, tok)
        for item in data.get('results', []) or []:
            url = item.get('url') or ''
            key = (username + '|' + url).lower()
            if not url or key in state['findings']:
                continue
            state['findings'][key] = {
                'id': f'OS{len(state["findings"]) + 1:04d}',
                'username': username,
                'platform': item.get('platform', ''),
                'url': url,
                'title': item.get('title', ''),
                'status': item.get('status'),
                'confidence': item.get('confidence'),
                'search_type': item.get('search_type', ''),
                'similar_username': item.get('similar_username', ''),
                'detection_in': item.get('detection_in', []),
                'first_seen': stamp(),
                'last_seen': stamp(),
            }
            new += 1

    # Start at most one shallow hunt per interval, and only when the service is idle.
    last_hunt = state.get('last_hunt')
    try:
        last_hunt_dt = datetime.fromisoformat(last_hunt.replace('Z', '+00:00')) if last_hunt else None
    except Exception:
        last_hunt_dt = None
    can_hunt = active == 0 and (last_hunt_dt is None or (now() - last_hunt_dt) >= timedelta(hours=HUNT_INTERVAL_HOURS))
    hunted = None
    if can_hunt:
        order = TARGETS[state.get('last_target_index', -1) + 1:] + TARGETS[:state.get('last_target_index', -1) + 1]
        for username in order:
            data = poll_results(username, tok)
            if data.get('found'):
                state['last_target_index'] = TARGETS.index(username)
                break
        else:
            username = order[0]
            findings = run_hunt(username, tok)
            for item in findings:
                url = item.get('url') or ''
                key = (username + '|' + url).lower()
                if not url or key in state['findings']:
                    continue
                state['findings'][key] = {
                    'id': f'OS{len(state["findings"]) + 1:04d}',
                    'username': username,
                    'platform': item.get('platform', ''),
                    'url': url,
                    'title': item.get('title', ''),
                    'status': item.get('status'),
                    'confidence': item.get('confidence'),
                    'search_type': item.get('search_type', ''),
                    'similar_username': item.get('similar_username', ''),
                    'detection_in': item.get('detection_in', []),
                    'first_seen': stamp(),
                    'last_seen': stamp(),
                }
                new += 1
            hunted = username
            state['last_target_index'] = TARGETS.index(username)
            state['last_hunt'] = stamp()

    findings = sorted(state['findings'].values(), key=lambda x: x['id'])
    OUT.write_text(json.dumps(findings, indent=2) + '\n', encoding='utf-8')
    STATE_PATH.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')
    exact = sum(1 for x in findings if x.get('search_type') == 'exact' or x.get('similar_username') == x.get('username'))
    high = sum(1 for x in findings if int(x.get('confidence') or 0) >= 70)
    print(json.dumps({
        'findings': len(findings),
        'new': new,
        'exact': exact,
        'high_confidence': high,
        'hunted': hunted,
        'hunts_active': active,
    }, indent=2))


if __name__ == '__main__':
    main()
