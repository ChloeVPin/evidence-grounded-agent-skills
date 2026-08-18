# Cycle 0150 — Expose summary-state freshness failures as distinct diagnostics

Date: 2026-08-18
Status: completed

## Question

Expose summary-state freshness failures as distinct diagnostics

## Decision

Summary-state freshness now has distinct executable diagnostics for stale summary
digest and invalid summary reference, alongside the existing state bindings.

## Evidence and provenance

Evidence: `validate_self_validation_state` and expanded temporary-root mutation
coverage in `tests/test_decision_ledger.py`.

## Disconfirming evidence sought

Stable consumers continue using `AUDIT_GATE_FAILED` and the false freshness check;
diagnostic prose is explanatory.

## Next action

Persist a summary-state diagnostic capture.
