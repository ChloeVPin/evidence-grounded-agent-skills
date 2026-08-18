# Cycle 0015 — Progress Ledger

Date: 2026-08-18
Status: validated with substantive-progress schema

## Question

What evidence fields should distinguish meaningful ecosystem improvement from activity?

## Decision

Progress requires numeric deltas for quality, coverage, evidence quality, validation, or uncertainty, plus evidence. File, source, and commit counts cannot qualify by themselves.

## Evidence and provenance

Implemented in `scripts/progress_record.py` with three tests in `tests/test_progress_record.py`.

## Disconfirming evidence sought

An artifact-count-only record is rejected; a quality delta without evidence is also rejected.

## Next action

Validation passed locally. Limitation: the schema validates the presence and shape of evidence but cannot independently measure the deltas. Next cycle: add durable cycle state that records mode, outcome, progress assessment, and next action.
