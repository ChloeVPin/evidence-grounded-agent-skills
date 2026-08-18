# Cycle 0126 — Bind the dependency manifest into the executable audit

Date: 2026-08-18
Status: completed

## Question

Bind the dependency manifest into the executable audit

## Decision

The executable audit now validates the 0125 dependency manifest as part of the
freshness gate. Drifted manifests fail with `AUDIT_GATE_FAILED` while the public
four-check output remains unchanged.

## Evidence and provenance

Evidence: the dependency manifest binding in `scripts/audit_current_assertion.py`
and temporary-root drift coverage in `tests/test_decision_ledger.py`.

## Disconfirming evidence sought

The executable script is allowed as the invoked host dependency for shaped
temporary roots; all evidence and state paths remain root-local and exact.

## Next action

Persist a dependency-manifest digest for tamper-evident provenance.
