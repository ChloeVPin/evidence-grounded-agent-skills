# Cycle 0119 — Persist the four-check CLI result as a versioned audit capture

Date: 2026-08-18
Status: completed

## Question

Persist the four-check CLI result as a versioned audit capture

## Decision

Persisted `ledger/evidence/0119-four-check-audit-capture.json` records the
four-check result, command provenance, exit status, and output digest. Its test
compares both the digest and parsed live payload.

## Evidence and provenance

Evidence: the 0119 capture artifact, `scripts/audit_current_assertion.py`, and
the matching integration test in `tests/test_decision_ledger.py`.

## Disconfirming evidence sought

The artifact is only valid for the recorded revision and exact output bytes;
future output-contract changes require a new capture rather than mutation of
this historical record.

## Next action

Add an explicit validator for the versioned four-check capture schema.
