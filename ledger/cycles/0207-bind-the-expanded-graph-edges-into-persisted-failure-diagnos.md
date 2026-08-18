# Cycle 0207 — Bind the expanded graph edges into persisted failure diagnostics

Date: 2026-08-18
Status: completed

## Question

Bind the expanded graph edges into persisted failure diagnostics

## Decision

Graph-edge failure diagnostics now carry the complete expanded edge set, including the inventory-to-snapshot edge and both inventory-to-diagnostic-case edges. The failure validator enforces that exact provenance shape.

## Evidence and provenance

Evidence: `ledger/evidence/0162-graph-edge-failure.json` and `ledger/evidence/0184-graph-edge-drift-failure.json` record all three edges; `scripts/decision_ledger.py` validates them; the audit passed all checks and all 183 tests passed.

## Disconfirming evidence sought

The first verification run failed only the content gate because the validator source digest was stale in both policy manifests. Refreshing the source digest restored all gates.

## Next action

Bind the expanded graph edges into state-failure diagnostics.
