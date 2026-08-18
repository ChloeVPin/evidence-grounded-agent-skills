# Cycle 0109 — Connect self-validation capture to a versioned bundle

Date: 2026-08-18
Status: completed

## Question

Connect self-validation capture to a versioned bundle

## Decision

Create a versioned self-validation bundle that links the current policy assertion,
its test capture, and the successful audit-command capture. Keep the command
capture distinct from the underlying test capture.

## Evidence and provenance

Evidence: `ledger/evidence/0108-self-validation-bundle.json`,
`ledger/evidence/0108-audit-command-capture.json`, and the validator test in
`tests/test_decision_ledger.py`. The validator requires all references and
rejects reusing the test capture as the self-validation capture.

## Disconfirming evidence sought

Validation is limited to reference presence and capture distinctness; it does
not independently re-run the command or establish that the assertion chain is
current.

## Next action

Audit the self-validation bundle against the current assertion chain.
