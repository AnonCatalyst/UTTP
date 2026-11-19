#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
steps = [
 [sys.executable, str(ROOT / '19_STRICT_VALIDATION' / 'strict_validate.py')],
 [sys.executable, str(ROOT / '20_LIVE_MONITORING' / 'monitor.py')],
 [sys.executable, str(ROOT / '18_ENTITY_TRACKING' / 'build_entity_intelligence.py')],
 [sys.executable, str(ROOT / '20_LIVE_MONITORING' / 'update_manifest.py')],
]
for step in steps:
    print('RUN', ' '.join(step))
    subprocess.run(step, check=True)
print('PIPELINE OK')
