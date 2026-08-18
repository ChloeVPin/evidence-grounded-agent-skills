# Cycle 0010 — Review Record Format

Date: 2026-08-18
Status: validated with versioned record schema

## Question

What repository-native artifact should preserve a complete review decision for later audit?

## Decision

Use schema version 1 with required revision, paths, allowed prefixes, acceptance criteria, diff, evidence, and attestation fields. The attestation revision must match the record revision.

## Evidence and provenance

Implemented in `scripts/review_record.py` with three schema tests in `tests/test_review_record.py`.

## Disconfirming evidence sought

Missing revision and revision-mismatched attestations are rejected.

## Next action

Validation passed locally. Limitation: schema validation does not prove the truth of evidence fields. Next cycle: generate complete records from the existing capture, bind, and review utilities, then validate them as one artifact.
