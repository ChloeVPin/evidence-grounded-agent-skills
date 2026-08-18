# Cycle 0129 — Expose dependency-state freshness as a distinct diagnostic reason

Date: 2026-08-18
Status: completed

## Question

Expose dependency-state freshness as a distinct diagnostic reason

## Decision

Executable coverage now preserves distinct reasons for dependency-state digest
drift and invalid manifest references, rather than collapsing them into a
generic freshness failure.

## Evidence and provenance

Evidence: `validate_self_validation_state`, the CLI diagnostic aggregation, and
end-to-end temporary-root tests for both mutations.

## Disconfirming evidence sought

Diagnostic prose is intentionally non-stable; the stable contract remains the
`AUDIT_GATE_FAILED` code and false freshness check.

## Next action

Add a versioned diagnostic snapshot for dependency-state failures.
