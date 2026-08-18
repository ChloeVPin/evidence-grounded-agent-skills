# Cycle 0089 — Audit assertion evidence references and detect missing or stale captures

Date: 2026-08-18
Status: completed

## Question

Audit assertion evidence references and detect missing or stale captures

## Decision

Assertion auditing now requires every referenced capture, script, and test path
to exist in the supplied repository inventory.

## Evidence and provenance

Tests accept the two stored assertions against their four referenced paths and
reject an empty path inventory.

## Disconfirming evidence sought

Path existence does not prove content freshness; content digests and rerun
comparison remain separate gates.

## Next action

Validation passed locally. Next cycle: combine reference existence with content
and policy-result validation.
