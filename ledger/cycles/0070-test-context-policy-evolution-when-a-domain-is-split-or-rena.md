# Cycle 0070 — Test context-policy evolution when a domain is split or renamed

Date: 2026-08-18
Status: completed

## Question

Test context-policy evolution when a domain is split or renamed

## Decision

Context renames are explicit migrations. The differential context can become
`behavioral-differential` while retaining its artifact binding, and collisions
are rejected rather than silently collapsing scope.

## Evidence and provenance

Tests cover successful rename, renamed-context artifact validation, and duplicate
scope produced by a conflicting rename.

## Disconfirming evidence sought

Legacy records retain their original context names; migration does not rewrite
history. Renamed labels require a separately reviewed update.

## Next action

Validation passed locally. Next cycle: audit legacy context names and migration
coverage before introducing another rename.
