#!/usr/bin/env python3
"""Validate the built War Room snapshot against its schema and the embedded agent summaries."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
snapshot_path = root / "output" / "war_room_snapshot.json"
daily_schema_path = root / "framework" / "contracts" / "daily_summary.schema.json"
snapshot_schema_path = root / "framework" / "contracts" / "war_room_snapshot.schema.json"

VALID_STATUSES = {"ready", "warning", "critical", "baseline", "missing"}


def check_required(data, required, label):
    missing = set(required) - set(data)
    if missing:
        print(f"FAIL {label}: missing fields {sorted(missing)}")
        return False
    return True


def check_type(value, expected, field, label):
    type_map = {"string": str, "object": dict, "array": list}
    py_type = type_map.get(expected)
    if py_type and not isinstance(value, py_type):
        print(f"FAIL {label}: {field} should be {expected}, got {type(value).__name__}")
        return False
    return True


def validate_agent(agent, idx):
    label = f"agents[{idx}]"
    required = ["subsystem_id", "title", "status", "updated_at", "highlights", "risks", "actions", "artifacts"]
    ok = check_required(agent, required, label)
    if agent.get("status") not in VALID_STATUSES:
        print(f"FAIL {label}: status '{agent.get('status')}' not in {sorted(VALID_STATUSES)}")
        ok = False
    for field in ("highlights", "risks", "actions", "artifacts"):
        if field in agent and not isinstance(agent[field], list):
            print(f"FAIL {label}: {field} should be array")
            ok = False
    return ok


def main():
    if not snapshot_path.exists():
        print(f"FAIL snapshot not found at {snapshot_path}")
        print("Run: python3 scripts/build_demo_war_room_snapshot.py")
        sys.exit(1)

    snapshot = json.loads(snapshot_path.read_text())

    ok = True

    # Validate top-level structure
    snapshot_schema = json.loads(snapshot_schema_path.read_text())
    top_required = snapshot_schema.get("required", [])
    ok = check_required(snapshot, top_required, "snapshot") and ok

    for field, prop in snapshot_schema.get("properties", {}).items():
        if field in snapshot:
            ok = check_type(snapshot[field], prop.get("type", ""), field, "snapshot") and ok

    # Validate each agent against daily_summary schema
    agents = snapshot.get("agents", [])
    for i, agent in enumerate(agents):
        ok = validate_agent(agent, i) and ok

    if ok:
        print(f"OK   {snapshot_path} ({len(agents)} agents validated)")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
