# Cycle 0006 — Bind Evidence to Change

Date: 2026-08-18
Status: validated with integrity-binding fixture

## Question

How should captured evidence prove it applies to the exact reviewed diff and declared acceptance criteria?

## Decision

Bind each evidence record to the SHA-256 digests of the reviewed diff and normalized acceptance criteria.

## Evidence and provenance

Implemented in `scripts/bind_evidence.py` with three behavioral tests in `tests/test_bind_evidence.py`.

## Disconfirming evidence sought

Changing either the diff or acceptance criteria invalidates the attestation; reordering criteria does not, because criteria are normalized before hashing.

## Next action

Validation passed locally. Limitation: hashes establish input identity, not semantic correctness or trusted provenance of the captured command. Next cycle: integrate the attestation with the evidence-review record and expose stale-record rejection in one end-to-end fixture.
