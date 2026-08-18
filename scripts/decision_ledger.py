#!/usr/bin/env python3
"""Validate durable contradiction and failure-learning ledger entries."""
from dataclasses import dataclass
import re

OUTCOMES = {"supported_refuted", "contextual", "unresolved", "failure"}
PARAPHRASE_MIN_SHARED_TERMS = 2
TERM_ALIASES = {
    "authorization": "authority",
    "unrestricted": "wildcard",
}


@dataclass(frozen=True)
class LedgerAssessment:
    valid: bool
    reason: str


def find_matching_entries(entries: list[dict], claim: str) -> list[dict]:
    """Return prior entries whose recorded claims contain the exact claim."""
    return [entry for entry in entries if claim in entry.get("claims", [])]


def find_paraphrase_candidates(
    entries: list[dict], claim: str, *, min_shared_terms: int = PARAPHRASE_MIN_SHARED_TERMS,
    context: str | None = None,
) -> list[dict]:
    """Return possible matches for human review; never merge or resolve claims."""
    query_terms = _terms(claim)
    candidates = []
    for entry in entries:
        if context is not None and context not in entry.get("contexts", []):
            continue
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
    entries: list[dict], labels: list[dict], *, min_shared_terms: int = PARAPHRASE_MIN_SHARED_TERMS,
) -> dict[str, float | int]:
    """Aggregate retrieval errors across labeled queries without changing policy."""
    totals = {"true_positive": 0, "false_positive": 0, "false_negative": 0}
    for label in labels:
        predicted = {
            entry["entry_id"]
            for entry in find_paraphrase_candidates(
                entries, label["query"], min_shared_terms=min_shared_terms,
                context=label.get("context"),
            )
        }
        metrics = candidate_metrics(set(label["expected_ids"]), predicted)
        for key in totals:
            totals[key] += metrics[key]
    true_positive = totals["true_positive"]
    predicted_count = true_positive + totals["false_positive"]
    expected_count = true_positive + totals["false_negative"]
    return {
        **totals,
        "precision": true_positive / predicted_count if predicted_count else 0.0,
        "recall": true_positive / expected_count if expected_count else 0.0,
    }


def _terms(text: str) -> set[str]:
    terms = {term for term in re.findall(r"[a-z0-9]+", text.lower()) if len(term) > 3}
    return {TERM_ALIASES.get(term, term) for term in terms}


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
