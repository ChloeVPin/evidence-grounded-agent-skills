# Cycle 0097 — Add one command for the full current-head audit

Date: 2026-08-18
Status: completed

## Question

Add one command for the full current-head audit

## Decision

Added `scripts/audit_current_assertion.py`, a single executable audit for current
head discovery, bundle completeness, fresh result agreement, and content digests.

## Evidence and provenance

The integration test runs the command and verifies structured passing output for
the discovered 0093 head.

## Disconfirming evidence sought

The command depends on repository-local evidence layout and does not replace
external review or semantic assessment of the policy.

## Next action

Validation passed locally. Next cycle: exercise the command’s failure paths with
tampered or missing evidence.
