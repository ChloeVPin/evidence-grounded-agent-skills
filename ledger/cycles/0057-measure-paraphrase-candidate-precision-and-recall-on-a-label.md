# Cycle 0057 — Measure paraphrase candidate precision and recall on a labeled ledger set

Date: 2026-08-18
Status: completed

## Question

Measure paraphrase candidate precision and recall on a labeled ledger set

## Decision

The labeled evaluator reports precision and recall independently; the current
small label set is a measurement fixture, not evidence sufficient to change the
matching threshold.

## Evidence and provenance

`candidate_metrics` correctly reports one true positive, one false positive,
and one false negative as 0.5 precision and 0.5 recall. The labels are stored
in `ledger/evaluations/0057-paraphrase-labels.json`.

## Disconfirming evidence sought

The set contains only three queries and hand-labeled expectations; it cannot
estimate production recall or validate semantic equivalence at scale.

## Next action

Validation passed locally. Next cycle: expand the labeled set before changing
the paraphrase threshold.
