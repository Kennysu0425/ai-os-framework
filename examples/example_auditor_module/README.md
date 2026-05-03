# Example Auditor Module

A generic provenance auditor that checks whether every subsystem in the AI OS records **how its output was generated** (`provenance` field).

This example is intentionally simple — its purpose is to show the auditor pattern, not to ship a production auditor.

## What It Checks

For each subsystem export in `examples/*/exports/daily_summary.json`:

- Does the file include `provenance.generated_by`?
- Does the file include `provenance.model` (when an LLM was involved)?
- Are required fields populated?

## What It Produces

A standard `daily_summary.json` with:

- `status: warning` when any subsystem is missing provenance
- `risks` listing each subsystem missing metadata
- `actions` recommending the fix

## Why This Matters

Without provenance, you can't answer "which AI generated this report" three months later — and you can't show that answer to an executive or auditor. An auditor module catches this gap continuously.

## Trying It

The example export in `exports/daily_summary.json` is a hand-written sample. To run a real auditor, you would write a script (Python, Node, etc.) that reads other subsystems' exports and produces this same shape.

See `framework/auditors/README.md` for the full pattern.
