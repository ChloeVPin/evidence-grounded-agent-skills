# Cycle 0204 — Bind diagnostic-case provenance into the state-diagnostic capture chain

Date: 2026-08-18
Status: completed

## Question

Bind diagnostic-case provenance into the state-diagnostic capture chain

## Decision

The summary state-diagnostic capture now records the diagnostic-case references and canonical digest, and its validator compares them with the dependency summary.

## Evidence and provenance

Evidence: `ledger/evidence/0151-summary-state-diagnostic-capture.json` carries both case references; `scripts/decision_ledger.py` enforces their exact-list digest; the live audit passed all checks and all 183 tests passed.

## Disconfirming evidence sought

The first verification run correctly failed only the content gate because the two policy manifests still referenced earlier source and test hashes. Refreshing those manifests restored the gate; no audit-output recapture was needed because the emitted audit JSON was unchanged.

## Next action

Bind diagnostic-case provenance into the state-diagnostic capture chain.
