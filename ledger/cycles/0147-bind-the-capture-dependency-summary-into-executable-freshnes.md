# Cycle 0147 — Bind the capture-dependency summary into executable freshness validation

Date: 2026-08-18
Status: completed

## Question

Bind the capture-dependency summary into executable freshness validation

## Decision

The executable audit now validates the 0146 capture/state/policy summary as part
of freshness. Adding an untracked capture reference fails with
`AUDIT_GATE_FAILED` and a precise diagnostic.

## Evidence and provenance

Evidence: summary binding in `scripts/audit_current_assertion.py` and the
temporary-root drift test.

## Disconfirming evidence sought

The expected reference sets are code-level policy; summary changes require an
intentional validator/policy update.

## Next action

Persist a digest for the complete capture-dependency summary.
