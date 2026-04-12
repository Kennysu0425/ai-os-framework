# Module Model

A module is a named operating capability in the control plane.

Examples:

- daily briefing
- market scan
- command center
- healthcheck
- knowledge summary bridge

A module may stay inside the control plane or later be promoted into a subsystem.

## Promotion rule

A module should be considered for subsystem promotion if it grows:

- its own long-lived state
- its own dashboard
- its own runtime schedule
- its own domain complexity
- its own contract and lifecycle
