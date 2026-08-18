# Cycle 0086 — Rerun audit and compare with persisted assertion

Date: 2026-08-18
Status: completed

## Question

Rerun audit and compare with persisted assertion

## Decision

The persisted policy assertion matches a fresh successful rerun of the exact
command; the current revision changed, but both results remain auditable.

## Evidence and provenance

`ledger/evidence/0086-generation-rerun.json` captures the current revision,
success status, and output digest. Comparison tests reject a contradictory
persisted result.

## Disconfirming evidence sought

The comparison verifies command/result agreement, not semantic sufficiency of
the test suite or external provenance of the process.

## Next action

Validation passed locally. Next cycle: record the current passing audit as a new
versioned policy assertion.
