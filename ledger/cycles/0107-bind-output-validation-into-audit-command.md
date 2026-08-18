# Cycle 0107 — Bind output validation into audit command

Date: 2026-08-18
Status: completed

## Question

Bind output validation into audit command

## Decision

The audit CLI now validates every emitted success or failure payload against its
documented schema before determining its exit status.

## Evidence and provenance

Live success, empty-root, tampered-bundle, and malformed-input tests continue to
pass through the shared output validator.

## Disconfirming evidence sought

Self-validation checks structure only; it cannot make an invalid underlying
audit result true.

## Next action

Validation passed locally. Next cycle: capture self-validation results as audit
evidence.
