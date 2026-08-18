# Cycle 0079 — Detect source-file manifest drift after a decision file is moved or replaced

Date: 2026-08-18
Status: completed

## Question

Detect source-file manifest drift after a decision file is moved or replaced

## Decision

The source manifest now detects both path mapping drift and content replacement
through per-file SHA-256 digests.

## Evidence and provenance

Tests validate the live manifest and reject a changed recorded file digest;
mapping digest checks continue to detect moved paths.

## Disconfirming evidence sought

The check is local and repository-backed; it does not detect an untracked copy
outside the manifest or establish authorship of file contents.

## Next action

Validation passed locally. Next cycle: add inventory-level provenance for the
manifest generation command and revision.
