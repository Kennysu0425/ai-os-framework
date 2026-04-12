# Control Plane

The control plane is the governance layer of the AI OS. It does not own domain-specific business logic — it owns visibility, aggregation, and contract enforcement.

## Responsibilities

- Module registration and naming
- Subsystem boundary definitions
- Contract consumption and validation
- Health aggregation
- War Room snapshot generation

## What Belongs Here

Add your own scripts and configuration to this directory:

- Aggregation scripts (collect subsystem exports into a unified view)
- Health checkers (verify subsystem freshness and readiness)
- Contract consumers (read and validate `daily_summary.json` from each subsystem)
- War Room builders (produce `war_room_snapshot.json`)

## Getting Started

The working example is `scripts/build_demo_war_room_snapshot.py`. It shows the core pattern:

```python
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]

# Collect exports from each subsystem
subsystems = [
    root / "examples" / "example_trading_subsystem" / "exports" / "daily_summary.json",
    root / "examples" / "example_email_subsystem" / "exports" / "daily_summary.json",
]

agents = []
for path in subsystems:
    agents.append(json.loads(path.read_text()))

# Build the aggregated snapshot
snapshot = {
    "generated_at": "...",
    "overall_status": "warning",
    "executive": { ... },
    "control_plane": { "health": { ... } },
    "agents": agents,
}
```

The control plane reads thin contracts — it never reaches into subsystem internals.

## Key References

- Contract schemas: `framework/contracts/`
- Templates: `templates/module.spec.template.yaml`
- Architecture docs: `docs/architecture.md`
