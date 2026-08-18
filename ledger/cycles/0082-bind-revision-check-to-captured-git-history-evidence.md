# Cycle 0082 — Bind revision check to captured Git history evidence

Date: 2026-08-18
Status: completed

## Question

Bind revision check to captured Git history evidence

## Decision

Generation revision checks now bind to successful `capture_evidence` output;
revision mismatches and failed commands are rejected.

## Evidence and provenance

Integration tests capture a real repository revision and successful command, then
reject a fabricated revision.

## Disconfirming evidence sought

Captured evidence is local process output and does not prove remote identity or
that the command was the intended generation procedure.

## Next action

Validation passed locally. Next cycle: persist a generation-evidence record beside
the source manifest.
