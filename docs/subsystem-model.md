# Subsystem Model

A subsystem is a domain-owned runtime that publishes explicit control-plane contracts.

Examples:

- trading subsystem
- email subsystem
- knowledge subsystem

## Subsystem responsibilities

- own domain logic
- own local state
- own local reports
- publish control-plane-safe summaries

## Control-plane responsibilities

- consume published summaries
- aggregate health and priorities
- render one operator-facing view
