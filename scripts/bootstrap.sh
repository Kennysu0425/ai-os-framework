#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${ROOT}"

if [[ ! -f ".env" && -f ".env.example" ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

mkdir -p output

python3 scripts/build_demo_war_room_snapshot.py
python3 scripts/validate_contracts.py

echo
echo "Bootstrap complete."
echo "Open demo/war_room/index.html in a browser."
