# Cycle 0031 — Validate Test Effectiveness

Date: 2026-08-18
Status: validated with mutation-classification fixture

## Question

Can test-effectiveness analysis produce a small executable fixture that distinguishes killed, surviving, equivalent, and invalid mutations?

## Decision

The fixture distinguishes killed, survived, equivalent, invalid, and unexecuted mutations; score denominator includes only killed and survived cases.

## Evidence and provenance

Implemented in `scripts/mutation_review.py` with four tests in `tests/test_mutation_review.py`.

## Disconfirming evidence sought

Equivalent, invalid, and unexecuted cases are excluded from the score; unknown statuses are rejected.

## Next action

Validation passed locally. Limitation: the fixture classifies supplied outcomes but does not mutate or execute source code. Next cycle: connect mutation classification to a small real fault-injection fixture and test assertion sensitivity.
