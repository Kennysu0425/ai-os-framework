# Contributing to AI OS Framework

Contributions are welcome if they improve control-plane clarity, contract quality, subsystem patterns, portability, observability, or demo usability.

## Local Setup

```bash
git clone https://github.com/user/ai-os-framework.git
cd ai-os-framework
make bootstrap
```

This copies `.env.example` to `.env`, builds the demo War Room snapshot, and validates all contracts. No third-party dependencies required.

Open `demo/war_room/index.html` to verify the setup is working.

## Adding a New Example Subsystem

1. Create the directory structure:

```bash
mkdir -p examples/example_your_subsystem/exports
```

2. Copy the template:

```bash
cp templates/daily_summary.template.json examples/example_your_subsystem/exports/daily_summary.json
cp templates/subsystem_README.template.md examples/example_your_subsystem/README.md
```

3. Fill in the required fields in `daily_summary.json`:
   - `subsystem_id` — unique identifier (e.g., `"your_subsystem"`)
   - `title` — display name
   - `status` — one of: `ready`, `warning`, `critical`, `baseline`, `missing`
   - `updated_at` — ISO 8601 timestamp
   - `highlights`, `risks`, `actions`, `artifacts` — arrays of strings

4. Register your subsystem in the build and validation scripts:
   - Add the export path to the `examples` list in `scripts/build_demo_war_room_snapshot.py`
   - Add the export path to the `paths` list in `scripts/validate_contracts.py`

5. Validate and rebuild:

```bash
make validate
make demo
```

## Validating Contracts

```bash
make validate
```

This runs `scripts/validate_contracts.py`, which checks that every example export contains all required fields defined in `framework/contracts/daily_summary.schema.json`.

## Code Style

- **Python scripts**: stdlib only for core functionality. No third-party imports in anything that `make bootstrap` or `make validate` calls.
- **JSON**: 2-space indent, UTF-8, `ensure_ascii=False`.
- **Shell scripts**: `set -euo pipefail` at the top.
- **HTML/CSS**: Keep the demo minimal and self-contained — no build tools or bundlers.

## Pull Request Guidelines

- One concern per PR.
- Run `make validate` before submitting.
- Include a brief description of what changed and why.
- If adding a new example subsystem, include the export JSON and update both the build and validation scripts.
- If modifying contracts or schemas, update the corresponding templates in `templates/`.

## What Not to Include

- Private CRM, email, or personal data
- Real memory stores or knowledge archives
- Tokens, keys, or host-specific confidential paths
- Raw personal digital twin content

Keep those in private repos and expose them only through explicit contracts.
