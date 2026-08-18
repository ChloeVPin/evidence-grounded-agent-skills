# Cycle 0133 — Expose diagnostic-snapshot freshness failures as distinct reasons

Date: 2026-08-18
Status: completed

## Question

Expose diagnostic-snapshot freshness failures as distinct reasons

## Decision

Executable coverage now preserves distinct reasons for diagnostic snapshot digest
staleness and invalid snapshot references, alongside the existing dependency
manifest diagnostics.

## Evidence and provenance

Evidence: `validate_self_validation_state`, the CLI diagnostic aggregation, and
temporary-root tests for both snapshot mutations.

## Disconfirming evidence sought

Stable consumers still use `AUDIT_GATE_FAILED` and the false freshness check;
diagnostic prose is explanatory rather than a versioned API.

## Next action

Add a versioned snapshot-diagnostic capture record.
