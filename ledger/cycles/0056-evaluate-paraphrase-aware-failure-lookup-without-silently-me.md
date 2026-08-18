# Cycle 0056 — Evaluate paraphrase-aware failure lookup without silently merging claims

Date: 2026-08-18
Status: completed

## Question

Evaluate paraphrase-aware failure lookup without silently merging claims

## Decision

Paraphrase lookup can surface a candidate using a minimum shared-term
threshold, but it remains a review queue and does not merge ledger claims.

## Evidence and provenance

The regression test finds the boundary failure from a reworded claim and finds
no candidate for an unrelated database-migration claim. Exact lookup remains
available for unambiguous matches.

## Disconfirming evidence sought

Token overlap can miss valid paraphrases and can produce false candidates;
semantic equivalence still requires explicit human or higher-order review.

## Next action

Validation passed locally. Next cycle: measure candidate precision and recall on
a larger labeled set before changing the matching policy.
