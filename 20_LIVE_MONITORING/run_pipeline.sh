#!/usr/bin/env bash
set -euo pipefail
set -a
source /opt/tel/.env
set +a
cd /var/tmp/opencode/O9A-work
/usr/bin/python3 19_STRICT_VALIDATION/strict_validate.py >/var/tmp/opencode/strict-validate.log 2>&1
/usr/bin/python3 20_LIVE_MONITORING/monitor.py >/var/tmp/opencode/monitor.log 2>&1
/usr/bin/python3 18_ENTITY_TRACKING/fill_tel.py >/var/tmp/opencode/fill-tel.log 2>&1
/usr/bin/python3 20_LIVE_MONITORING/sync_tel_intake.py >/var/tmp/opencode/sync-tel-intake.log 2>&1
/usr/bin/python3 18_ENTITY_TRACKING/build_entity_intelligence.py >/var/tmp/opencode/build-json.log 2>&1
/usr/bin/python3 /var/tmp/opencode/entity-work/build_page.py >/var/tmp/opencode/build-page.log 2>&1
/usr/bin/python3 /var/tmp/opencode/O9A-work/20_LIVE_MONITORING/update_manifest.py >/var/tmp/opencode/update-manifest.log 2>&1
