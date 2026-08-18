# Cycle 0064 — Test adversarial lexical variants for alias false candidates

Date: 2026-08-18
Status: completed

## Question

Test adversarial lexical variants for alias false candidates

## Decision

The aliases recover the authorization paraphrase but also surface one
adversarial unrelated query as a candidate. They remain review-only; no
automatic claim merge is permitted.

## Evidence and provenance

The nine-query fixture reports seven true positives, one false positive, and no
false negatives: precision 0.875 and recall 1.0. The adversarial test directly
exercises the false candidate.

## Disconfirming evidence sought

The adversarial query is synthetic and small; the result measures a known risk,
not a general precision estimate.

## Next action

Validation passed locally. Next cycle: evaluate whether contextual metadata can
reduce alias false candidates.
