# Cycle 0171 — Bind the expanded diagnostic case into the graph-state capture provenance

Date: 2026-08-18
Status: completed

## Question

Bind the expanded diagnostic case into the graph-state capture provenance

## Decision

Graph-state diagnostic capture now binds the expanded dependency snapshot by
reference and canonical digest, and rejects stale snapshot provenance.

## Evidence and provenance

Evidence: updated 0143 graph capture, validator support, content-digest refresh,
and executable graph provenance validation.

## Disconfirming evidence sought

The graph capture remains valid and the complete audit passes; 183 tests,
compilation, and all four public checks pass.

## Next action

Bind snapshot provenance into the graph dependency summary.
