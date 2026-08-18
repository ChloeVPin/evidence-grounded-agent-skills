# Cycle 0066 — Measure context-filter recall on cross-domain queries

Date: 2026-08-18
Status: completed

## Question

Measure context-filter recall on cross-domain queries

## Decision

Context filtering preserves single-domain matches but loses a cross-domain
match when the query is scoped to only one context. It is therefore a precision
control with an explicit recall cost, not a safe default for every query.

## Evidence and provenance

The labeled context test reports four true positives, zero false positives, and
one false negative: 0.8 recall. The missed entry is the test-effectiveness
failure in a differential-review-scoped query.

## Disconfirming evidence sought

The cross-domain label is synthetic and the sample has four records; broader
context ontologies may reduce or increase this tradeoff.

## Next action

Validation passed locally. Next cycle: define an explicit cross-domain context
policy before making context filtering automatic.
