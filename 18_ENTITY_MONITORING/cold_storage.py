#!/usr/bin/env python3
"""Resource-aware cold storage for generated intelligence.

Keeps compressed assessment snapshots, prunes old data, and can sync to GitHub
with a strict 24-hour rate limit.
"""
import gzip, json, os, subprocess, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_JSON = Path('/var/www/html/data/entity-intelligence.json')
MONITOR_FEED = Path(__file__).resolve().parent / 'monitor_feed.json'
STRICT = Path(__file__).resolve().parent / 'strict_validation_summary.json'
TEL_DB = Path('/var/lib/wintergate/threat_api.db')
COLD = Path('/var/lib/wintergate/cold_storage/entity_intelligence')
LOCK = Path('/var/lib/wintergate/cold_storage/.lock')
LAST_SYNC = Path('/var/lib/wintergate/cold_storage/.last_github_sync')
LAST_VACUUM = Path('/var/lib/wintergate/cold_storage/.last_full_vacuum')
STATUS = Path(__file__).resolve().parent / 'cold_storage_status.json'
SITE_STATUS = Path('/var/www/html/data/cold-storage-status.json')
MAX_SNAPSHOTS = 24
MAX_BYTES = 50 * 1024 * 1024

def now():
    return datetime.now(timezone.utc)

def compact(data, feed, strict):
    return {
        'updated': data.get('meta', {}).get('updated'),
        'counts': data.get('meta', {}),
        'monitor': data.get('monitor', {}),
        'strict': {
            'strict_valid': strict.get('strict_valid', 0),
            'rejected': strict.get('rejected', 0),
            'broken_links': strict.get('broken_internal_links', []),
            'manifest_hash_ok': strict.get('manifest_hash_ok', False),
        },
        'tel_intake': data.get('tel_intake', {}),
        'entities': [
            {
                'id': e.get('id'),
                'name': e.get('name'),
                'type': e.get('type'),
                'status': e.get('status'),
                'confidence': e.get('confidence'),
                'watch_priority': e.get('watch_priority'),
                'risk_score': (e.get('learning') or {}).get('risk_score'),
                'sources': len(e.get('sources', [])),
                'areas': len(e.get('areas', [])),
                'tactics': len(e.get('tactics', [])),
                'events': len(e.get('evolution', [])),
            }
            for e in data.get('entities', [])
        ],
        'source_watch': {
            'updated': feed.get('updated'),
            'checked': feed.get('urls_checked', 0),
            'ok': sum(1 for r in feed.get('results', []) if r.get('ok')),
        },
    }

def prune():
    snaps = sorted(COLD.glob('*.json.gz'))
    while len(snaps) > MAX_SNAPSHOTS:
        snaps[0].unlink(missing_ok=True)
        snaps = sorted(COLD.glob('*.json.gz'))
    total = sum(p.stat().st_size for p in snaps)
    if total <= MAX_BYTES:
        return
    # Compress older snapshots harder, then drop the oldest if still needed.
    for p in snaps[:max(1, len(snaps) // 2)]:
        try:
            raw = gzip.decompress(p.read_bytes())
            p.write_bytes(gzip.compress(raw, compresslevel=9))
        except Exception:
            pass
    snaps = sorted(COLD.glob('*.json.gz'))
    total = sum(p.stat().st_size for p in snaps)
    while total > MAX_BYTES and snaps:
        snaps[0].unlink(missing_ok=True)
        snaps = sorted(COLD.glob('*.json.gz'))
        total = sum(p.stat().st_size for p in snaps)


def db_maintenance():
    info = {'checked': False}
    if not TEL_DB.exists():
        return info
    import sqlite3
    conn = sqlite3.connect(str(TEL_DB))
    try:
        info['checked'] = True
        info['page_count'] = conn.execute('PRAGMA page_count').fetchone()[0]
        info['freelist_before'] = conn.execute('PRAGMA freelist_count').fetchone()[0]
        auto_vacuum = conn.execute('PRAGMA auto_vacuum').fetchone()[0]
        if auto_vacuum in (1, 2):
            try:
                conn.execute('PRAGMA incremental_vacuum')
            except Exception:
                pass
        try:
            last = datetime.fromisoformat(LAST_VACUUM.read_text().strip().replace('Z', '+00:00')) if LAST_VACUUM.exists() else None
        except Exception:
            last = None
        if last is None or (now() - last) >= timedelta(hours=24):
            conn.execute('VACUUM')
            conn.execute('ANALYZE')
            LAST_VACUUM.write_text(now().isoformat().replace('+00:00', 'Z'))
            info['full_vacuum'] = True
        else:
            info['full_vacuum'] = False
        info['freelist_after'] = conn.execute('PRAGMA freelist_count').fetchone()[0]
        try:
            conn.execute('PRAGMA optimize')
        except Exception:
            pass
    finally:
        conn.close()
    return info

def github_sync(path):
    if os.environ.get('GITHUB_COLD_SYNC') != '1':
        return 'disabled'
    try:
        last = datetime.fromisoformat(LAST_SYNC.read_text().strip().replace('Z', '+00:00')) if LAST_SYNC.exists() else None
    except Exception:
        last = None
    if last and (now() - last) < timedelta(hours=24):
        return 'rate_limited'
    try:
        subprocess.run(['gh', 'release', 'upload', 'archive-v3-20261119', str(path), '--clobber'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        LAST_SYNC.write_text(now().isoformat().replace('+00:00', 'Z'))
        return 'uploaded'
    except Exception as e:
        return f'failed: {e}'

def main():
    COLD.mkdir(parents=True, exist_ok=True)
    if LOCK.exists() and time.time() - LOCK.stat().st_mtime < 300:
        print('locked')
        return
    LOCK.write_text(str(os.getpid()))
    try:
        data = json.loads(SITE_JSON.read_text(encoding='utf-8'))
        feed = json.loads(MONITOR_FEED.read_text(encoding='utf-8')) if MONITOR_FEED.exists() else {}
        strict = json.loads(STRICT.read_text(encoding='utf-8')) if STRICT.exists() else {}
        snapshot = compact(data, feed, strict)
        stamp = now().strftime('%Y%m%dT%H%M%SZ')
        out = COLD / f'entity-intelligence-{stamp}.json.gz'
        out.write_bytes(gzip.compress(json.dumps(snapshot, separators=(',', ':')).encode('utf-8'), compresslevel=9))
        prune()
        db_info = db_maintenance()
        raw_bytes = len(json.dumps(snapshot, separators=(',', ':')).encode('utf-8'))
        status = github_sync(out)
        status_obj = {
            'updated': now().isoformat().replace('+00:00', 'Z'),
            'latest_snapshot': str(out),
            'snapshot_bytes': out.stat().st_size,
            'snapshots': len(list(COLD.glob('*.json.gz'))),
            'total_bytes': sum(p.stat().st_size for p in COLD.glob('*.json.gz')),
            'github': status,
            'tel_records': data.get('monitor', {}).get('tel_records'),
            'raw_snapshot_bytes': raw_bytes,
            'bytes_saved': max(0, raw_bytes - out.stat().st_size),
            'db': db_info,
        }
        STATUS.parent.mkdir(parents=True, exist_ok=True)
        STATUS.write_text(json.dumps(status_obj, indent=2) + '\n', encoding='utf-8')
        site_status = Path('/var/www/html/data/cold-storage-status.json')
        if site_status.parent.exists():
            site_status.write_text(json.dumps(status_obj, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(status_obj, indent=2))
    finally:
        try:
            LOCK.unlink()
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    main()
