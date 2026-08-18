# Cycle 0022 — Dependency Evidence Records

Date: 2026-08-18
Status: validated with dependency evidence schema

## Question

How should dependency provenance and advisory evidence be represented in generated review records without implying that fixture flags are live security lookups?

## Decision

Each dependency result requires an authoritative source, ISO lookup timestamp, and explicit `verified`, `vulnerable`, or `unknown` status. `unknown` is recorded uncertainty, not implicit safety.

## Evidence and provenance

Implemented in `scripts/dependency_evidence.py` and integrated into `review_change`, with unit and complete-review tests.

## Disconfirming evidence sought

Missing source, invalid timestamp, and invalid status are rejected; explicit unknown status is structurally valid but remains subject to policy decision.

## Next action

Validation passed locally. Limitation: the schema does not authenticate the source or freshness beyond syntax; the next cycle should define policy for unknown/stale evidence and bind it to generated records.
