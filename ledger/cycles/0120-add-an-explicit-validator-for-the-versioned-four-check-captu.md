# Cycle 0120 — Add an explicit validator for the versioned four-check capture schema

Date: 2026-08-18
Status: completed

## Question

Add an explicit validator for the versioned four-check capture schema

## Decision

Added `validate_four_check_capture`, enforcing capture shape, successful command
evidence, exact four true checks, passing result, and null error code. Valid and
mutated captures are covered by tests.

## Evidence and provenance

Evidence: `ledger/evidence/0119-four-check-audit-capture.json`, the validator in
`scripts/decision_ledger.py`, and the versioned-capture integration test.

## Disconfirming evidence sought

The validator requires the recorded revision to remain in the supplied history;
it does not silently accept a capture from an unreachable revision.

## Next action

Use the schema validator inside the executable audit path.
