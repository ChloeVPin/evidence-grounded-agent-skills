# Cycle 0008 — Escalated Review Decisions

Date: 2026-08-18
Status: validated with explicit escalation

## Question

How should Hermes represent a sensitive change that is not automatically accepted but may proceed after explicit review?

## Decision

Sensitive paths remain blocked unless an escalation record contains reviewer identity, `accept` decision, rationale, and a parseable ISO timestamp.

## Evidence and provenance

Implemented in `scripts/review_change.py` with explicit-review tests in `tests/test_review_change.py`.

## Disconfirming evidence sought

An incomplete escalation record is rejected. A complete record can accept a sensitive change while preserving the evidence and attestation gates.

## Next action

Validation passed locally. Limitation: the evaluator validates fields and timestamp syntax, not the real-world identity or authority of the reviewer. Next cycle: create durable review decision artifacts and connect them to repository history.
