# Cycle 0095 — Discover current assertion head automatically

Date: 2026-08-18
Status: completed

## Question

Discover current assertion head automatically

## Decision

Current-head selection now discovers all stored generation-policy assertions,
validates the full supersession chain, and returns the single current 0093 head.

## Evidence and provenance

The test loads policy assertions by repository glob and verifies automatic
discovery of `0093-generation-policy-audit`.

## Disconfirming evidence sought

Discovery depends on complete repository enumeration; an omitted or untracked
assertion cannot be found by this local audit.

## Next action

Validation passed locally. Next cycle: make automatic discovery include bundle
and content validation for the selected head.
