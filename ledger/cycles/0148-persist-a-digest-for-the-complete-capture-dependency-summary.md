# Cycle 0148 — Persist a digest for the complete capture-dependency summary

Date: 2026-08-18
Status: completed

## Question

Persist a digest for the complete capture-dependency summary

## Decision

Added a canonical SHA-256 over the capture-dependency summary payload and
required it in validation. Digest tampering is rejected separately from
reference-set drift.

## Evidence and provenance

Evidence: the 0146 summary’s `summary_sha256`, the validator, and digest mutation
coverage.

## Disconfirming evidence sought

The digest authenticates summary structure and references; referenced artifact
content remains protected by their individual gates.

## Next action

Bind summary digest into versioned state.
