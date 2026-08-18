# Cycle 0142 — Expose graph-state freshness failures as distinct diagnostics

Date: 2026-08-18
Status: completed

## Question

Expose graph-state freshness failures as distinct diagnostics

## Decision

Graph-state freshness now has distinct executable diagnostics for stale policy
digest and invalid graph reference, in addition to the lower-level graph gate.

## Evidence and provenance

Evidence: `validate_self_validation_state` and expanded temporary-root mutation
coverage in `tests/test_decision_ledger.py`.

## Disconfirming evidence sought

Diagnostic text is explanatory; callers must use `AUDIT_GATE_FAILED` and the
freshness boolean as the stable contract.

## Next action

Persist a graph-state diagnostic capture.
