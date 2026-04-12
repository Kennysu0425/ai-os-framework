#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
paths = [
    root / 'examples' / 'example_trading_subsystem' / 'exports' / 'daily_summary.json',
    root / 'examples' / 'example_knowledge_subsystem' / 'exports' / 'daily_summary.json',
    root / 'examples' / 'example_email_subsystem' / 'exports' / 'daily_summary.json',
]
required = {'subsystem_id', 'title', 'status', 'updated_at', 'highlights', 'risks', 'actions', 'artifacts'}

ok = True
for path in paths:
    data = json.loads(path.read_text())
    missing = required - set(data)
    if missing:
        ok = False
        print(f'FAIL {path}: missing {sorted(missing)}')
    else:
        print(f'OK   {path}')
if not ok:
    raise SystemExit(1)
