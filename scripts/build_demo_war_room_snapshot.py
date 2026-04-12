#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
examples = [
    root / 'examples' / 'example_trading_subsystem' / 'exports' / 'daily_summary.json',
    root / 'examples' / 'example_knowledge_subsystem' / 'exports' / 'daily_summary.json',
    root / 'examples' / 'example_email_subsystem' / 'exports' / 'daily_summary.json',
]

agents = []
for path in examples:
    agents.append(json.loads(path.read_text()))

snapshot = {
    'generated_at': '2026-01-01T09:30:00+08:00',
    'overall_status': 'warning',
    'executive': {
        'top_priorities': ['Review subsystem warnings'],
        'top_risks': ['Queue pressure in email', 'Trading instability'],
        'top_actions': ['Review priority replies', 'Review trading readiness']
    },
    'control_plane': {
        'health': {
            'telegram': 'healthy',
            'scheduler': 'healthy'
        }
    },
    'agents': agents,
}

out_dir = root / 'output'
out_dir.mkdir(exist_ok=True)
out = out_dir / 'war_room_snapshot.json'
out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
print(out)
