# Cycle 0205 — Bind diagnostic-case provenance into the state-diagnostic capture chain

Date: 2026-08-18
Status: completed

## Question

Bind diagnostic-case provenance into the state-diagnostic capture chain

## Decision

The graph state-diagnostic capture now records diagnostic-case references and a canonical digest, and its validator checks them against the persisted freshness inventory.

## Evidence and provenance

Evidence: `ledger/evidence/0143-graph-state-diagnostic-capture.json` binds the two case artifacts; `scripts/audit_current_assertion.py` supplies the inventory to the graph validator; the audit passed all checks and all 183 tests passed.

## Disconfirming evidence sought

The initial verification failed only because the content manifests referenced earlier source and test hashes. Refreshing both manifests restored the content gate; the freshness and result gates remained valid.

## Next action

Bind diagnostic-case provenance into the remaining dependency graph edge checks.
