# Cycle 0091 — Connect bundle validation to content-digest checks

Date: 2026-08-18
Status: completed

## Question

Connect bundle validation to content-digest checks

## Decision

Assertion references now require SHA-256 content digests, allowing the bundle to
detect replacement of an existing path as well as missing paths.

## Evidence and provenance

The current 0087 assertion’s capture, implementation, and test references are
digest-bound; a tampered capture digest is rejected.

## Disconfirming evidence sought

Content digests verify bytes at audit time, not semantic correctness or authorship
of the referenced files.

## Next action

Validation passed locally. Next cycle: persist a complete current assertion bundle
with references, digests, and fresh result together.
