# Cycle 0122 — Persist a capture-schema failure reason in the audit evidence ledger

Date: 2026-08-18
Status: completed

## Question

Persist a capture-schema failure reason in the audit evidence ledger

## Decision

Failure output now includes the validator reason while retaining the stable
`AUDIT_GATE_FAILED` code. The malformed-capture scenario is persisted in
`ledger/evidence/0122-capture-schema-failure.json`.

## Evidence and provenance

Evidence: the executable audit, its malformed-capture test, and the 0122
failure-evidence record linked to the 0119 source capture.

## Disconfirming evidence sought

Reasons are diagnostic text and may evolve; consumers must continue branching
on the error code and check booleans rather than exact prose.

## Next action

Add a machine-readable validator for persisted failure evidence.
