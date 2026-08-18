# Cycle 0102 — Document CLI contract and exit codes

Date: 2026-08-18
Status: completed

## Question

Document CLI contract and exit codes

## Decision

Documented the current-head audit CLI contract, success/failure exit statuses,
optional root behavior, and stable error codes.

## Evidence and provenance

`AUDIT_CLI.md` is linked from the README and tested for the command and all
stable codes.

## Disconfirming evidence sought

The contract documents interface stability, not semantic sufficiency of the
underlying audit or permanence of diagnostic reason text.

## Next action

Validation passed locally. Next cycle: add machine-readable failure codes
documentation to the generated audit output examples.
