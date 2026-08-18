# Cycle 0116 — Add freshness metadata to the persisted self-validation state

Date: 2026-08-18
Status: completed

## Question

Add freshness metadata to the persisted self-validation state

## Decision

Added `validated_revision` to the persisted state and require it to equal the
self-validation capture’s provenance revision. This makes freshness explicit
without falsely requiring the later storage commit to equal the captured run.

## Evidence and provenance

Evidence: `ledger/state/0113-complete-self-validation-gate.json`, the revision
gate in `validate_self_validation_state`, and a stale-revision regression test.

## Disconfirming evidence sought

The metadata records provenance freshness relative to the captured run; it does
not prove the state is regenerated after every subsequent repository commit.

## Next action

Bind freshness metadata into the executable audit result.
