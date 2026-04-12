# War Room

The War Room is the operator-facing aggregation surface. It answers four questions:

1. **What matters now?** — Top priorities from across subsystems
2. **What is risky?** — Cross-subsystem risk signals
3. **What to do next?** — Actionable next steps
4. **Which subsystem is healthy or degraded?** — Per-agent status

## Snapshot Structure

The War Room consumes a `war_room_snapshot.json` with this structure:

```json
{
  "generated_at": "2026-01-01T09:30:00+08:00",
  "overall_status": "warning",
  "executive": {
    "top_priorities": ["Review subsystem warnings"],
    "top_risks": ["Queue pressure in email"],
    "top_actions": ["Review priority replies"]
  },
  "control_plane": {
    "health": { "telegram": "healthy", "scheduler": "healthy" }
  },
  "agents": [
    {
      "subsystem_id": "trading",
      "title": "Trading Subsystem",
      "status": "warning",
      "highlights": ["BTC intraday monitor is active"],
      "risks": ["Market structure is unstable"],
      "actions": ["Review readiness before execution"]
    }
  ]
}
```

## Getting Started

1. Run `make bootstrap` to generate the demo snapshot
2. Open `demo/war_room/index.html` to see the War Room UI
3. Inspect `output/war_room_snapshot.json` to see the raw data

## Customizing the War Room

To add your own subsystem to the War Room:

1. Create your subsystem's `exports/daily_summary.json` (see `templates/daily_summary.template.json`)
2. Add its path to the `examples` list in `scripts/build_demo_war_room_snapshot.py`
3. Rebuild: `make demo`

To customize the dashboard UI, edit `demo/war_room/index.html`. The rendering logic is a single `render()` function that maps the JSON structure to DOM elements.

## Key References

- Snapshot schema: `framework/contracts/war_room_snapshot.schema.json`
- Template: `templates/war_room_snapshot.template.json`
- Demo UI: `demo/war_room/index.html`
- Builder script: `scripts/build_demo_war_room_snapshot.py`
