# Adapters

The framework is **runtime-agnostic by design**. A subsystem can be a Python script, a Node service, an n8n workflow, a Claude Code skill, a webhook receiver, or anything else — as long as it produces a contract-compliant `daily_summary.json`.

To make this explicit, the framework defines three kinds of adapters. You don't need all three. Most subsystems only need one or two.

## The Three Adapter Types

```
┌────────────────────────────────────────────────┐
│  War Room (operator surface)                   │
├────────────────────────────────────────────────┤
│  Control Plane (contracts + aggregation)       │
├────────────────────────────────────────────────┤
│  ▼ 1. Subsystem Runtime Adapter                │
│      "How a runtime becomes a subsystem"
├────────────────────────────────────────────────┤
│  ▼ 2. Tool / Data Source Adapter               │
│      "How a subsystem reads SQL / API / MCP"
├────────────────────────────────────────────────┤
│  ▼ 3. Agent Adapter                            │
│      "How an LLM/agent plugs into a subsystem"
└────────────────────────────────────────────────┘
```

### 1. Subsystem Runtime Adapter

Defines **how a piece of running code becomes a subsystem** the control plane can talk to.

The contract is intentionally minimal:

| Requirement | Meaning |
|------------|---------|
| Produces `exports/daily_summary.json` | Conforms to `framework/contracts/daily_summary.schema.json` |
| Path is stable | Control plane reads from a known location |
| Output is idempotent | Re-running produces the same shape |

That's it. The framework does not care if the subsystem is:

- a Python cron job
- a Node.js service
- an n8n workflow that writes to a file
- a Claude Code skill triggered by `/run-daily`
- a webhook handler
- a manual export from a notebook

Set `runtime: <type>` in your `module.spec.yaml` so the control plane can render it correctly. See `templates/module.spec.template.yaml` for the field.

### 2. Tool / Data Source Adapter

Defines **how a subsystem internally reaches into the world** — databases, SaaS APIs, files, MCP servers, etc.

The framework deliberately does not standardize this layer. Different tools have different auth/retry/rate-limit behavior, and forcing a uniform interface creates more friction than it removes.

What the framework does require:

- The `inputs[]` block in `module.spec.yaml` declares what data sources a subsystem touches
- Use `type: folder | file | sheet | api | mcp | env` so reviewers can see the data surface at a glance
- Secrets stay in `.env` or your secret manager, never inline

If a useful pattern emerges across many subsystems, it can be promoted to a first-class framework concept later.

### 3. Agent Adapter

Defines **where LLMs and agents live in the architecture**.

The framework's stance: **agents are an implementation detail of a subsystem, not a control-plane concept.**

That means:

- Subsystems may use Claude / GPT / Gemini / local models internally
- The control plane only sees the resulting `daily_summary.json`
- The optional `provenance.model` field lets you record which model produced an output, for audit and AI transparency
- The optional `agent_prompt` block in `module.spec.yaml` documents the prompt contract

This separation keeps the control plane simple and lets subsystems swap agents without breaking anyone.

## Why This Matters

### For self-host users (default)

You can plug in any runtime you already use. No rewrite required. As long as it produces the contract, the War Room works.

### For future commercial use

By keeping the runtime layer pluggable, the same framework can support:

- Single-user self-host (default)
- Small-team SaaS (with `tenant_id` populated)
- Connector marketplace (third-party adapters publish subsystems)

The schema fields `tenant_id`, `policy_id`, `audience`, `data_classification`, and `provenance` are reserved for these scenarios. They are optional today and have no effect on self-host deployments.

## Reference Adapters

The included examples already demonstrate three runtimes:

- `examples/example_trading_subsystem` — file-based export
- `examples/example_email_subsystem` — file-based export with metrics
- `examples/example_knowledge_subsystem` — file-based export

Future examples will show Node.js, n8n, and Claude Code variants of the same contract.
