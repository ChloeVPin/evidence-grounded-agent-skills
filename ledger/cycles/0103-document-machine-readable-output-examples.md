# Cycle 0103 — Document machine-readable output examples

Date: 2026-08-18
Status: completed

## Question

Document machine-readable output examples

## Decision

Added success and failure JSON examples to the CLI contract, including null
success code, stable malformed-evidence code, checks, and result fields.

## Evidence and provenance

Contract tests assert the examples’ stable machine-readable fields and codes.

## Disconfirming evidence sought

Examples are illustrative output shapes; diagnostic reason text and audit IDs
vary by repository state.

## Next action

Validation passed locally. Next cycle: add a command-level contract verifier for
all documented output fields.
