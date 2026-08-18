# Cycle 0060 — Review threshold policy only after cross-domain metrics remain stable

Date: 2026-08-18
Status: completed

## Question

Review threshold policy only after cross-domain metrics remain stable

## Decision

Retain the paraphrase candidate threshold at two shared terms. The current
cross-domain fixture is perfect, but its small size does not justify a policy
change or semantic auto-resolution.

## Evidence and provenance

The threshold is now an explicit constant, and the seven-query fixture measures
1.0 precision and 1.0 recall. Tests verify the default remains two terms.

## Disconfirming evidence sought

The labels are hand-authored and cover only three failure records; exact token
overlap remains vulnerable to both missed paraphrases and false candidates.

## Next action

Validation passed locally. Next cycle: collect more cross-domain labels before
revisiting the threshold.
