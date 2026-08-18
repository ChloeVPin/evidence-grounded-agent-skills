# Cycle 0115 — Add explicit failure-semantics coverage to persisted-state audit

Date: 2026-08-18
Status: completed

## Question

Add explicit failure-semantics coverage to persisted-state audit

## Decision

The persisted-state validator now rejects four independent failure classes:
failed status, a false check, digest mismatch, and unexpected check keys. The
CLI tests separately retain `AUDIT_GATE_FAILED` and `MALFORMED_EVIDENCE`.

## Evidence and provenance

Evidence: the expanded state-validation test in `tests/test_decision_ledger.py`,
`validate_self_validation_state` in `scripts/decision_ledger.py`, and the
existing executable CLI failure tests.

## Disconfirming evidence sought

A passing state artifact can still become stale after later repository changes;
these checks validate its shape and bindings, not continuous freshness.

## Next action

Add freshness metadata to the persisted self-validation state.
