# Cycle 0077 — Detect source-inventory drift after a new decision entry is added

Date: 2026-08-18
Status: completed

## Question

Detect source-inventory drift after a new decision entry is added

## Decision

Source-inventory drift is now detected by recomputing the recorded digest; the
original four-entry inventory passes and a simulated fifth entry fails.

## Evidence and provenance

Regression tests exercise both matching and stale-digest paths against the
durable migration record.

## Disconfirming evidence sought

The check detects changes only when the caller supplies the changed inventory;
it does not itself discover untracked entries.

## Next action

Validation passed locally. Next cycle: add inventory provenance that enumerates
the source files used to derive entry IDs.
