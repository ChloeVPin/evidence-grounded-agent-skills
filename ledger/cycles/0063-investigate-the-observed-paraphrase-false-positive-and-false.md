# Cycle 0063 — Investigate the observed paraphrase false positive and false negative

Date: 2026-08-18
Status: completed

## Question

Investigate the observed paraphrase false positive and false negative

## Decision

The apparent false positive was a valid multi-domain overlap and is now
multi-labeled. The missed authorization variant is recovered by two explicit
lexical aliases; candidate lookup still requires review and does not merge.

## Evidence and provenance

The corrected eight-query fixture now reports seven true positives, zero false
positives, and zero false negatives. Tests cover both aliases and overlapping
labels.

## Disconfirming evidence sought

The aliases are hand-selected from this fixture and may not generalize; perfect
fixture metrics do not justify automatic semantic resolution or a lower term
threshold.

## Next action

Validation passed locally. Next cycle: add adversarial lexical variants to test
whether the aliases create false candidates.
