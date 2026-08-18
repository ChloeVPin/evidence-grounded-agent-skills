# Cycle 0068 — Validate malformed or ambiguous context declarations

Date: 2026-08-18
Status: completed

## Question

Validate malformed or ambiguous context declarations

## Decision

Context declarations now require a non-empty list of unique, non-wildcard
strings. Evaluation rejects malformed declarations rather than silently
changing review scope.

## Evidence and provenance

Tests cover empty, duplicate, wildcard, non-string, valid multi-context, and
fail-closed evaluation cases.

## Disconfirming evidence sought

Validation cannot establish that a syntactically valid context is semantically
correct; context ownership and meaning remain caller-provided claims.

## Next action

Validation passed locally. Next cycle: add a durable context-policy schema and
validate its relationship to ledger artifact paths.
