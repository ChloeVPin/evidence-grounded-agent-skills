# Cycle 0112 — Create a single validator for the complete self-validation bundle

Date: 2026-08-18
Status: completed

## Question

Create a single validator for the complete self-validation bundle

## Decision

Added `validate_complete_self_validation_bundle`, which composes bundle shape,
current-head chain, current assertion bundle, test-result, content-integrity,
self-capture success, and exact output-digest gates.

## Evidence and provenance

Evidence: `ledger/evidence/0108-self-validation-bundle.json`, the validator in
`scripts/decision_ledger.py`, and the integration test in
`tests/test_decision_ledger.py`.

## Disconfirming evidence sought

The first integration test failed because its fixture omitted internal bundle
references; adding those repository paths made all gates pass without weakening
the validator.

## Next action

Persist a state record for the complete bundle gate and audit its failure output.
