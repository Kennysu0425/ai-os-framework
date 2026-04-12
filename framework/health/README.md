# Health

Health monitoring is a first-class concern in the AI OS. The goal is to know when the system is degraded — not just to run automations blindly.

## Health Dimensions

| Dimension | What to check | Example |
|-----------|--------------|---------|
| **Readiness** | Can the module run its next cycle? | Config loaded, dependencies reachable |
| **Freshness** | Is the subsystem's last export recent enough? | `updated_at` within expected window |
| **Notification health** | Are alerts and reports reaching operators? | Telegram/email delivery confirmed |
| **Recovery visibility** | Can the operator see what failed and retry? | Failed steps logged, retry available |

## Getting Started

A minimal health check reads a subsystem's `daily_summary.json` and verifies freshness and status:

```python
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

def check_health(export_path, max_age_hours=24):
    data = json.loads(Path(export_path).read_text())

    # Check status
    if data["status"] in ("critical", "missing"):
        return {"status": "degraded", "reason": f"subsystem status is {data['status']}"}

    # Check freshness
    updated = datetime.fromisoformat(data["updated_at"])
    age = datetime.now(timezone.utc) - updated
    if age > timedelta(hours=max_age_hours):
        return {"status": "stale", "reason": f"last update was {age.total_seconds() / 3600:.1f}h ago"}

    return {"status": "healthy"}
```

## What Belongs Here

- Health check scripts for each module and subsystem
- Aggregated health summary builders
- Recovery and retry logic

## Key References

- Health schema: `framework/contracts/health_summary.schema.json`
- Template: `templates/health_summary.template.json`
- Validation script: `scripts/validate_contracts.py`
