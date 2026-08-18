# Cycle 0062 — Reassess threshold only if new domain metrics expose material errors

Date: 2026-08-18
Status: completed

## Question

Reassess threshold only if new domain metrics expose material errors

## Decision

The measurement audit found and corrected a cross-query aggregation bug: unioning
IDs could hide false positives. Metrics now score each labeled query before
aggregation; the threshold remains unchanged pending fresh measurements.

## Evidence and provenance

The new regression test demonstrates that one correct match plus one false
cross-query candidate reports 0.5 precision instead of incorrectly reporting
1.0. The corrected eight-query fixture reports five true positives, one false
positive, and one false negative: 5/6 precision and recall.

## Disconfirming evidence sought

The correction improves accounting, but the labels remain small and hand-authored;
it does not prove semantic candidate quality.

## Next action

Validation passed locally. Next cycle: investigate the false positive and false
negative before any threshold decision.
