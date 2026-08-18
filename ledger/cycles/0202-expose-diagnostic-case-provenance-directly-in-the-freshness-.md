# Cycle 0202 — Expose diagnostic-case provenance directly in the freshness inventory

Date: 2026-08-18
Status: completed

## Question

Expose diagnostic-case provenance directly in the freshness inventory

## Decision

Freshness inventory validation now accepts and checks an explicit `diagnostic_case_refs` set. The executable audit includes the two diagnostic-case artifacts in inventory availability and validates the persisted inventory against them.

## Evidence and provenance

Evidence: `ledger/evidence/0154-freshness-capture-inventory.json` records both diagnostic-case references; `ledger/state/0113-complete-self-validation-gate.json` binds the refreshed inventory digest. The live audit passed with bundle, content, freshness, and result checks true.

## Disconfirming evidence sought

The first verification run failed because the audit passed the new optional validator argument in the wrong positional order and because content digests still referenced the prior validator source. Reordering the arguments and refreshing both digest manifests resolved the failures; the final audit and all 183 tests pass.

## Next action

Bind diagnostic-case provenance into versioned self-validation state.
