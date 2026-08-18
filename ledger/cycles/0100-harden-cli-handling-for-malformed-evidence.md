# Cycle 0100 — Harden CLI handling for malformed evidence

Date: 2026-08-18
Status: completed

## Question

Harden CLI handling for malformed evidence

## Decision

The audit CLI now catches malformed JSON, missing fields, and filesystem errors,
returning structured failure output with a nonzero status.

## Evidence and provenance

Tests exercise malformed current-assertion JSON, tampered bundles, and an empty
root; none may produce an unstructured traceback.

## Disconfirming evidence sought

The handler reports exception text and does not classify every possible process
or interpreter failure.

## Next action

Validation passed locally. Next cycle: add machine-readable failure reasons and
stable error codes.
