#!/usr/bin/env python3
"""Validate durable contradiction and failure-learning ledger entries."""
from dataclasses import dataclass
import re

OUTCOMES = {"supported_refuted", "contextual", "unresolved", "failure"}


@dataclass(frozen=True)
class LedgerAssessment:
    valid: bool
    reason: str


def find_matching_entries(entries: list[dict], claim: str) -> list[dict]:
    """Return prior entries whose recorded claims contain the exact claim."""
    return [entry for entry in entries if claim in entry.get("claims", [])]


def find_paraphrase_candidates(
    entries: list[dict], claim: str, *, min_shared_terms: int = 2,
) -> list[dict]:
    """Return possible matches for human review; never merge or resolve claims."""
    query_terms = _terms(claim)
    candidates = []
    for entry in entries:
        recorded_terms = set().union(*(_terms(item) for item in entry.get("claims", [])))
        if len(query_terms & recorded_terms) >= min_shared_terms:
            candidates.append(entry)
    return candidates


def candidate_metrics(expected_ids: set[str], predicted_ids: set[str]) -> dict[str, float | int]:
    """Score candidate retrieval without treating candidates as resolved matches."""
    true_positive = len(expected_ids & predicted_ids)
    false_positive = len(predicted_ids - expected_ids)
    false_negative = len(expected_ids - predicted_ids)
    return {
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": true_positive / len(predicted_ids) if predicted_ids else 0.0,
        "recall": true_positive / len(expected_ids) if expected_ids else 0.0,
    }


def evaluate_labeled_queries(
    entries: list[dict], labels: list[dict], *, min_shared_terms: int = 2,
) -> dict[str, float | int]:
    """Aggregate retrieval errors across labeled queries without changing policy."""
    expected = set()
    predicted = set()
    for label in labels:
        expected.update(label["expected_ids"])
        predicted.update(
            entry["entry_id"]
            for entry in find_paraphrase_candidates(
                entries, label["query"], min_shared_terms=min_shared_terms,
            )
        )
    return candidate_metrics(expected, predicted)


def _terms(text: str) -> set[str]:
    return {term for term in re.findall(r"[a-z0-9]+", text.lower()) if len(term) > 3}


def validate_entry(entry: dict) -> LedgerAssessment:
    required = ("entry_id", "cycle_id", "artifacts", "claims", "outcome", "evidence", "decision")
    missing = [field for field in required if field not in entry]
    if missing:
        return LedgerAssessment(False, f"missing fields: {', '.join(missing)}")
    if not isinstance(entry["claims"], list) or not entry["claims"]:
        return LedgerAssessment(False, "claims are required")
    if not isinstance(entry["artifacts"], list) or not entry["artifacts"]:
        return LedgerAssessment(False, "artifact references are required")
    if entry["outcome"] not in OUTCOMES:
        return LedgerAssessment(False, "unknown outcome")
    if not entry["evidence"]:
        return LedgerAssessment(False, "evidence is required")
    if entry["outcome"] == "failure":
        for field in ("mechanism", "corrective_action", "regression_trigger"):
            if not entry.get(field):
                return LedgerAssessment(False, f"failure requires {field}")
    if entry["outcome"] == "unresolved" and not entry.get("next_action"):
        return LedgerAssessment(False, "unresolved entry requires next action")
    return LedgerAssessment(True, "valid ledger entry")
