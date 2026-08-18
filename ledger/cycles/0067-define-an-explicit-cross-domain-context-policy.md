# Cycle 0067 — Define an explicit cross-domain context policy

Date: 2026-08-18
Status: completed

## Question

Define an explicit cross-domain context policy

## Decision

Context policy is explicit: no context performs unfiltered review, one context
narrows candidates, and multiple declared contexts form an explicit union for
cross-domain review.

## Evidence and provenance

The new test restores the previously missed cross-domain entry when both
contexts are declared, while single-context evaluation retains the measured
0.8 recall tradeoff.

## Disconfirming evidence sought

Context declarations are still claims supplied by the caller and may be wrong;
the policy does not infer cross-domain scope from text.

## Next action

Validation passed locally. Next cycle: add a durable context-policy schema and
validate malformed or ambiguous context declarations.
