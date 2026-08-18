# Cycle 0032 — Fault Injection Fixture

Date: 2026-08-18
Status: validated with real boundary mutation

## Question

Can a small executable fixture demonstrate that a meaningful boundary test kills a plausible fault while a happy-path-only test lets it survive?

## Decision

The happy-path case lets a `<= 0` to `< 0` mutant survive; the zero boundary case kills it.

## Evidence and provenance

Fixture: `fixtures/fault_target.py`; executable tests: `tests/test_fault_injection.py`.

## Disconfirming evidence sought

The mutant is syntactically valid and behaviorally distinguishable at the zero boundary.

## Next action

Validation passed locally. Limitation: this is one hand-authored mutation, not a general mutation engine; next cycle should record the fixture as a completed test-effectiveness milestone and select the next bounded extension.
