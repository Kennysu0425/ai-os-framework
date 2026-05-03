# Auditors

Auditors are control-plane modules that **observe the AI OS itself** and surface findings to operators.

The basic question they answer: **"Is the AI doing what it's supposed to be doing, and what did it do?"**

This is different from `framework/health/`, which asks "are subsystems alive and fresh." Auditors go deeper: they check behavior, drift, cost, and trust.

## When to Add an Auditor

You don't need any auditors on day one. Add them as the system grows.

| Symptom | Auditor to add |
|---------|---------------|
| "I don't know which AI run produced this report" | **Provenance auditor** — checks that summaries carry `provenance.model` and `provenance.generated_by` |
| "The system spec and the actual code drifted" | **Spec drift auditor** — diffs `module.spec.yaml` against real outputs |
| "AI runs are eating my budget" | **Token budget auditor** — tracks run frequency, duplicate summarization, report-size growth |
| "I can't tell if a run was safe" | **Runtime safety auditor** — checks for write-out-of-scope, unredacted PII, missing retries |
| "The whole system is opaque" | **System integrity auditor** — aggregates the above into one report |

## Auditor Pattern

An auditor is just a regular module that:

1. Has `layer: auditor` in its `module.spec.yaml`
2. Reads the outputs and logs of OTHER subsystems
3. Produces a `daily_summary.json` like any other subsystem
4. Sets `audience: auditor` so the War Room can group it separately

It does not need to be aware of subsystem internals. It only reads contracts and side effects.

```yaml
# module.spec.yaml fragment
module_id: A01_provenance_auditor
layer: auditor
audience: auditor
purpose: Verify that all subsystem summaries carry provenance metadata.
inputs:
  - name: all_subsystem_exports
    type: folder
    required: true
    path_or_endpoint: examples/*/exports/daily_summary.json
```

## What Goes In Each Auditor's `daily_summary.json`

The same shape as any subsystem export:

| Field | What it means for an auditor |
|-------|-----------------------------|
| `status` | `ready` if no findings, `warning` if minor, `critical` if blocking |
| `highlights` | What was checked and what passed |
| `risks` | Findings that need attention |
| `actions` | Recommended fixes, ranked |
| `metrics` | Counts: subsystems checked, findings, severity |

## Why This Is a Control-Plane Concept

Without auditors, an AI OS slowly turns into a black box. Auditors make the system **legible to operators and executives** in ways that subsystem health checks alone cannot:

- **Health** answers: "Is the email subsystem running?"
- **Auditors** answer: "Did the email subsystem do something it shouldn't have?"

For commercial use, auditors are also the foundation for compliance reports, AI transparency disclosures, and trust narratives ("here's what the AI did this quarter, with provenance").

## Example

See `examples/example_auditor_module/` for a generic auditor that checks provenance metadata across all subsystems.

## Related

- `framework/contracts/` — schemas (now include `provenance` and `audience`)
- `framework/health/` — subsystem health checks
- `templates/module.spec.template.yaml` — `layer: auditor`
