# Cycle 0090 — Combine reference existence with content and result validation

Date: 2026-08-18
Status: completed

## Question

Combine reference existence with content and result validation

## Decision

Combined bundle validation now requires structured assertion shape, existing
evidence references, and agreement with a fresh successful capture.

## Evidence and provenance

Tests accept the current 0087 bundle and reject it when the available reference
inventory is empty.

## Disconfirming evidence sought

The bundle composes repository checks but does not independently verify file
content digests or command semantics beyond captured status and digest presence.

## Next action

Validation passed locally. Next cycle: connect bundle validation to content-digest
checks for referenced evidence files.
