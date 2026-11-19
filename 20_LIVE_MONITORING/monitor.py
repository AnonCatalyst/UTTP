#!/usr/bin/env python3
"""Lightweight overtime monitor for the UTTP entity intelligence page.

Checks a small set of public source URLs and records their availability. This is
a source-watch feed, not a crawler and not an enforcement tool.
"""
import json, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '20_LIVE_MONITORING' / 'monitor_feed.json'
SITE = Path('/var/www/html/data/monitor-feed.json')

URLS = [
 ('S001', 'https://www.canada.ca/en/public-safety-canada/news/2025/12/government-of-canada-lists-four-new-terrorist-entities0.html'),
 ('S003', 'https://gazette.govt.nz/notice/id/2025-au7135'),
 ('S005', 'https://www.police.govt.nz/sites/default/files/publications/statement-of-case-order-of-nine-angles-terrorist-designation.pdf'),
 ('S013', 'https://sparxintel.com/publications/the-uttp-from-internet-trolling-to-violent-extremism'),
 ('S014', 'https://gnet-research.org/2026/03/16/the-designation-of-764-network-why-does-it-matter/'),
 ('S021', 'https://www.cbc.ca/news/politics/764-youth-extremist-group-9.7010571'),
 ('S023', 'https://soyjakwiki.org/UTTP'),
 ('S031', 'https://www.justice.gov/usao-nj/media/1417486/dl?inline'),
 ('S034', 'https://github.com/WinterGate-IC/UTTP/blob/main/02_CORE_INVESTIGATION/AREA_INTELLIGENCE/UTTP_AREA_REGISTER.csv'),
 ('S040', 'https://github.com/WinterGate-IC/UTTP/tree/main/17_CURRENT_STATE_PACKAGE'),
]

def check(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'WinterGateIC-EntityMonitor/1.0'})
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return {'status': r.status, 'final_url': r.geturl(), 'content_type': r.headers.get('Content-Type', ''), 'elapsed_ms': round((time.monotonic()-started)*1000), 'ok': True}
    except urllib.error.HTTPError as e:
        return {'status': e.code, 'final_url': e.geturl(), 'content_type': e.headers.get('Content-Type', ''), 'elapsed_ms': round((time.monotonic()-started)*1000), 'ok': False}
    except Exception as e:
        return {'status': 0, 'final_url': url, 'content_type': '', 'elapsed_ms': round((time.monotonic()-started)*1000), 'ok': False, 'error': str(e)[:120]}

feed = {
 'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
 'mode': 'lightweight source watch',
 'urls_checked': len(URLS),
 'results': [],
}
for sid, url in URLS:
    result = check(url)
    result['source_id'] = sid
    result['url'] = url
    feed['results'].append(result)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(feed, indent=2) + '\n', encoding='utf-8')
if SITE.parent.exists():
    SITE.parent.mkdir(parents=True, exist_ok=True)
    SITE.write_text(json.dumps(feed, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'updated': feed['updated'], 'checked': len(URLS), 'ok': sum(1 for r in feed['results'] if r['ok'])}, indent=2))
