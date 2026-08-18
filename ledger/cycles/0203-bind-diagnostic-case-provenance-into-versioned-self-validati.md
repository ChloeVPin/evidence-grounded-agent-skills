# Cycle 0203 — Bind diagnostic-case provenance into versioned self-validation state

Date: 2026-08-18
Status: completed

## Question

Bind diagnostic-case provenance into versioned self-validation state

## Decision

The versioned self-validation state now requires `diagnostic_case_refs` and its canonical SHA256 digest, and validation compares both fields with the freshness inventory.

## Evidence and provenance

Evidence: `ledger/state/0113-complete-self-validation-gate.json` now binds the two diagnostic-case artifacts and their digest; `scripts/decision_ledger.py` enforces the invariant; the executable audit passed all four checks and the full 183-test suite passed.

## Disconfirming evidence sought

Before digest refresh, the expected content-drift failures occurred because both policy manifests referenced the prior source and test hashes. Updating those manifests restored the content gate without changing the audit result.

## Next action

Bind diagnostic-case provenance into the state-diagnostic capture chain.
