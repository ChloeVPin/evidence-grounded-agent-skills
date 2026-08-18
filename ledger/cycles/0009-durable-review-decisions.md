# Cycle 0009 — Durable Review Decisions

Date: 2026-08-18
Status: validated with bound review decisions

## Question

How should sensitive-path review decisions be stored so they remain auditable and tied to a specific repository revision?

## Decision

Sensitive approvals are durable only when they include reviewer identity, rationale, timestamp, and the exact revision, diff digest, and criteria digest from the attestation.

## Evidence and provenance

The escalation record is validated by `scripts/review_change.py`; tests cover valid binding and copied-approval rejection.

## Disconfirming evidence sought

Changing the reviewed diff invalidates both the attestation and the copied escalation decision.

## Next action

Validation passed locally. Limitation: local records still depend on the claimed reviewer identity; repository permissions and signatures remain an operational control. Next cycle: add a repository-native review record format and a command to generate it from captured evidence.
