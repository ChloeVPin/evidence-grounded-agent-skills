# Cycle 0110 — Audit self-validation bundle against current assertion chain

Date: 2026-08-18
Status: completed

## Question

Audit self-validation bundle against current assertion chain

## Decision

The self-validation bundle must name the discovered current assertion, not merely
an available assertion file. The chain validator now rejects a superseded
assertion reference while accepting the current 0093 head.

## Evidence and provenance

Evidence: `ledger/evidence/0108-self-validation-bundle.json`, the new
`validate_self_validation_bundle_against_chain` validator, and its regression
test in `tests/test_decision_ledger.py`.

## Disconfirming evidence sought

Reference presence alone was insufficient: a bundle could have pointed at the
valid but superseded 0087 assertion. The new check closes that gap. It still
does not independently verify the captured command output digest.

## Next action

Verify the self-validation capture itself against its recorded output digest.
