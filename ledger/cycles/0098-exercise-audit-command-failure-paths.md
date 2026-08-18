# Cycle 0098 — Exercise audit command failure paths

Date: 2026-08-18
Status: completed

## Question

Exercise audit command failure paths

## Decision

The audit command now supports an explicit root and returns structured nonzero
failure when evidence is absent, while the real repository continues to pass.

## Evidence and provenance

Tests exercise both valid repository execution and an evidence-free `/tmp` root.

## Disconfirming evidence sought

The failure test checks missing evidence only; it does not exhaustively mutate
every bundle field or filesystem error mode.

## Next action

Validation passed locally. Next cycle: add tampered-bundle failure coverage.
