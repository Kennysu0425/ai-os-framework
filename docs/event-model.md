# Event Model

Every module in the AI OS — subsystems, control-plane modules, auditors — follows the same four-step lifecycle:

```
trigger  →  process  →  report  →  log
```

This is the framework's single mental model. If your module doesn't fit, you usually have two modules glued together.

## The Four Steps

### 1. Trigger

What causes the module to run.

| Mode | Description |
|------|-------------|
| `scheduled` | Cron, launchd, systemd timer, or any clock-based scheduler |
| `manual` | A human invokes it (CLI, slash command, dashboard button) |
| `event` | A signal from another module or external webhook |

Declared in `module.spec.yaml` under `trigger.mode`.

### 2. Process

What the module does between trigger and report. This is where:

- The runtime adapter (Python / Node / n8n / Claude Code / etc.) executes
- Inputs declared under `inputs[]` are read
- LLMs / agents are called (if any)
- Side-effect actions declared under `actions[]` happen

The framework is intentionally silent on **how** processing works. That's where you get to plug in any tool, any agent, any data source.

### 3. Report

The contract output. **Every module produces a `daily_summary.json`** conforming to `framework/contracts/daily_summary.schema.json`.

This is the only piece the control plane sees. Everything else is implementation detail.

A subsystem's report typically contains:

- `highlights` — what happened
- `risks` — what to worry about
- `actions` — what to do next
- `metrics` — domain-specific counts

An auditor's report follows the same shape but answers different questions (see `framework/auditors/README.md`).

### 4. Log

What was retained for later inspection.

| What gets logged | Where |
|------------------|-------|
| Run telemetry (success/duration/errors) | `observability.log_path` in spec |
| Generated reports | `outputs.report_path` |
| Raw artifacts | `artifacts[]` field in `daily_summary.json` |
| AI provenance | `provenance` block in `daily_summary.json` |

The log layer is what makes the system **legible after the fact** — for debugging, audit, and trust narratives.

## Mapping to the Contracts

| Step | Spec field | Output |
|------|-----------|--------|
| Trigger | `trigger.mode` + `trigger.schedule_local` | — |
| Process | `inputs[]`, `agent_prompt`, `actions[]` | side effects |
| Report | `outputs.daily_summary` | `daily_summary.json` |
| Log | `observability.log_path`, `provenance` | log files + metadata |

## Why This Model Is Useful

- **Onboarding**: a new contributor learns one lifecycle, not one per module
- **Debugging**: when something breaks, you ask which step failed
- **Composition**: an event from one module's `report` step can be another module's `trigger`
- **Auditors**: they read the `report` and `log` outputs of other modules

## Related

- [contract-model.md](contract-model.md) — the `daily_summary.json` contract details
- [../framework/adapters/README.md](../framework/adapters/README.md) — runtime adapters at the process step
- [../framework/auditors/README.md](../framework/auditors/README.md) — modules that read reports/logs
