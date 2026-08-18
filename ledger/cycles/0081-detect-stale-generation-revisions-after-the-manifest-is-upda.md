# Cycle 0081 — Detect stale generation revisions after the manifest is updated

Date: 2026-08-18
Status: completed

## Question

Detect stale generation revisions after the manifest is updated

## Decision

Generation provenance remains valid across later commits when its recorded
revision is still in repository history; unknown revisions are rejected.

## Evidence and provenance

Tests accept the manifest’s historical generation revision in a supplied history
set and reject the same revision when it is absent.

## Disconfirming evidence sought

The check requires an authoritative history set from the caller and does not
itself query Git or prove that the generation command was actually run.

## Next action

Validation passed locally. Next cycle: bind the revision check to captured Git
history evidence.
