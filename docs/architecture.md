# Architecture

## Summary

The framework uses a layered model:

1. Control plane definition layer
2. Control plane runtime layer
3. Subsystem runtime layer
4. Contract/export layer
5. Operator presentation layer

## Control Plane

The control plane should define:

- modules
- subsystem boundaries
- contract rules
- naming
- health model
- War Room aggregation logic

It should not own domain-native business logic.

## Subsystems

Subsystems should own:

- runtime logic
- domain state
- domain reports
- explicit contract outputs

## War Room

The War Room should read explicit contracts and health summaries, not subsystem internals.
