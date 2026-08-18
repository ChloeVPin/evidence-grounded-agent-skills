# Cycle 0173 — Expose graph provenance directly in the versioned state inventory

Date: 2026-08-18
Status: completed

## Question

Expose graph provenance directly in the versioned state inventory

## Decision

Versioned self-validation state now records graph and graph-capture provenance
references with a canonical digest tied to the aggregate summary.

## Evidence and provenance

Evidence: updated 0113 state schema, validator enforcement, content-digest
refresh, and executable state validation.

## Disconfirming evidence sought

The state remains a complete passing result; 183 tests, compilation, and the
full four-check audit pass.

## Next action

Add a dedicated graph-provenance state-drift failure artifact.
