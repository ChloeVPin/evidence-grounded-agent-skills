# Cycle 0123 — Add a machine-readable validator for persisted failure evidence

Date: 2026-08-18
Status: completed

## Question

Add a machine-readable validator for persisted failure evidence

## Decision

Added `validate_failure_evidence`, requiring the persisted diagnostic schema,
available source capture, stable error code, and non-empty reason. Positive,
missing-source, and empty-reason cases are tested.

## Evidence and provenance

Evidence: `ledger/evidence/0122-capture-schema-failure.json`, the validator in
`scripts/decision_ledger.py`, and its machine-readable test.

## Disconfirming evidence sought

The validator checks diagnostic integrity and provenance, not whether the
mutation was independently replayed; the executable temporary-root test covers
that replay path.

## Next action

Bind failure-evidence validation into the audit’s diagnostic path.
