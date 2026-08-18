# Cycle 0101 — Add stable machine-readable failure codes

Date: 2026-08-18
Status: completed

## Question

Add stable machine-readable failure codes

## Decision

The audit CLI now emits stable error codes for no current assertion, malformed
evidence, and failed audit gates.

## Evidence and provenance

Failure-path tests assert `NO_CURRENT_ASSERTION`, `MALFORMED_EVIDENCE`, and
`AUDIT_GATE_FAILED` respectively.

## Disconfirming evidence sought

Codes classify failure classes but do not encode every underlying reason; the
human-readable reason remains diagnostic context.

## Next action

Validation passed locally. Next cycle: document the CLI contract and exit codes.
