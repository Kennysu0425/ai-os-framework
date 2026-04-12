#!/usr/bin/env python3
import json
import re
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

snapshot_json = json.dumps(snapshot, ensure_ascii=False, indent=2)

# Write the JSON file
out_dir = root / 'output'
out_dir.mkdir(exist_ok=True)
out = out_dir / 'war_room_snapshot.json'
out.write_text(snapshot_json)
print(out)

# Inject fallback data into the War Room demo HTML
html_path = root / 'demo' / 'war_room' / 'index.html'
if html_path.exists():
    html = html_path.read_text()
    replacement = (
        '// FALLBACK_DATA_START\n'
        '    var FALLBACK_DATA = ' + json.dumps(snapshot, ensure_ascii=False, indent=2).replace('\n', '\n    ') + ';\n'
        '    // FALLBACK_DATA_END'
    )
    updated = re.sub(
        r'// FALLBACK_DATA_START\n.*?// FALLBACK_DATA_END',
        replacement,
        html,
        flags=re.DOTALL,
    )
    if updated != html:
        html_path.write_text(updated)
        print(f"Injected fallback data into {html_path}")
