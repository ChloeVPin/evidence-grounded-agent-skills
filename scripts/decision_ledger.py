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
CONTEXT_ARTIFACT_HINTS = {
    "test-effectiveness": ("fault", "mutation"),
    "tool-authorization": ("tool_policy", "tool_audit"),
    "dependency-security": ("dependency",),
    "differential-review": ("differential",),
    "behavioral-differential": ("differential",),
}
CONTEXT_RENAMES = {"differential-review": "behavioral-differential"}


@dataclass(frozen=True)
class LedgerAssessment:
    valid: bool
    reason: str


@dataclass(frozen=True)
class ContextAssessment:
    valid: bool
    reason: str


@dataclass(frozen=True)
class ContextMigration:
    valid: bool
    contexts: tuple[str, ...]
    reason: str


def validate_contexts(contexts: object) -> ContextAssessment:
    """Validate explicit context scope before it can constrain a review."""
    if not isinstance(contexts, list) or not contexts:
        return ContextAssessment(False, "contexts must be a non-empty list")
    if any(not isinstance(value, str) or not value.strip() for value in contexts):
        return ContextAssessment(False, "contexts must contain non-empty strings")
    if any(value == "*" for value in contexts):
        return ContextAssessment(False, "wildcard context is forbidden")
    if len(set(contexts)) != len(contexts):
        return ContextAssessment(False, "duplicate contexts are ambiguous")
    return ContextAssessment(True, "valid context declaration")


def migrate_contexts(contexts: object, rename_map: dict[str, str]) -> ContextMigration:
    """Apply an explicit context rename without losing or duplicating scope."""
    assessment = validate_contexts(contexts)
    if not assessment.valid:
        return ContextMigration(False, (), assessment.reason)
    if any(not isinstance(key, str) or not isinstance(value, str) for key, value in rename_map.items()):
        return ContextMigration(False, (), "context rename keys and values must be strings")
    migrated = tuple(rename_map.get(context, context) for context in contexts)
    if len(set(migrated)) != len(migrated):
        return ContextMigration(False, (), "context rename creates duplicate scope")
    return ContextMigration(True, migrated, "context migration is valid")


def validate_context_artifacts(entry: dict) -> ContextAssessment:
    """Require each declared known context to be represented by an artifact."""
    contexts = entry.get("contexts")
    if contexts is None:
        return ContextAssessment(True, "no context binding declared")
    assessment = validate_contexts(contexts)
    if not assessment.valid:
        return assessment
    artifacts = entry.get("artifacts", [])
    for context in contexts:
        hints = CONTEXT_ARTIFACT_HINTS.get(context)
        if hints is None:
            return ContextAssessment(False, f"unknown context: {context}")
        if not any(any(hint in artifact for hint in hints) for artifact in artifacts):
            return ContextAssessment(False, f"context is not bound to artifacts: {context}")
    return ContextAssessment(True, "contexts are bound to artifacts")


def validate_migration(migration: dict) -> ContextAssessment:
    """Validate a durable context migration and its artifact continuity."""
    required = (
        "migration_id", "source_entry_id", "source_contexts", "target_contexts",
        "artifacts", "reason", "reversible",
    )
    missing = [field for field in required if field not in migration]
    if missing:
        return ContextAssessment(False, f"migration missing fields: {', '.join(missing)}")
    for field in ("source_contexts", "target_contexts"):
        assessment = validate_contexts(migration[field])
        if not assessment.valid:
            return ContextAssessment(False, f"{field}: {assessment.reason}")
    if not isinstance(migration["artifacts"], list) or not migration["artifacts"]:
        return ContextAssessment(False, "migration artifacts are required")
    if not migration["reason"]:
        return ContextAssessment(False, "migration reason is required")
    if not isinstance(migration["reversible"], bool):
        return ContextAssessment(False, "migration reversibility must be boolean")
    return validate_context_artifacts({
        "contexts": migration["target_contexts"],
        "artifacts": migration["artifacts"],
    })


def audit_migrations(
    migrations: list[dict], source_entry_ids: set[str] | None = None,
) -> ContextAssessment:
    """Audit every migration record for validity and unique identity."""
    migration_ids = []
    for migration in migrations:
        assessment = validate_migration(migration)
        if not assessment.valid:
            return assessment
        if source_entry_ids is not None and migration["source_entry_id"] not in source_entry_ids:
            return ContextAssessment(False, f"missing migration source entry: {migration['source_entry_id']}")
        migration_ids.append(migration["migration_id"])
    if len(set(migration_ids)) != len(migration_ids):
        return ContextAssessment(False, "duplicate migration IDs")
    return ContextAssessment(True, "all migration records are valid")


def audit_context_names(entries: list[dict]) -> ContextAssessment:
    """Audit current and legacy names without rewriting historical entries."""
    known = set(CONTEXT_ARTIFACT_HINTS) | set(CONTEXT_RENAMES)
    for entry in entries:
        assessment = validate_context_artifacts(entry)
        if not assessment.valid:
            return assessment
        for context in entry.get("contexts", []):
            if context not in known:
                return ContextAssessment(False, f"unregistered legacy context: {context}")
    return ContextAssessment(True, "all context names are registered")


def find_matching_entries(entries: list[dict], claim: str) -> list[dict]:
    """Return prior entries whose recorded claims contain the exact claim."""
    return [entry for entry in entries if claim in entry.get("claims", [])]


def find_paraphrase_candidates(
    entries: list[dict], claim: str, *, min_shared_terms: int = PARAPHRASE_MIN_SHARED_TERMS,
    context: str | set[str] | None = None,
) -> list[dict]:
    """Return possible matches for human review; never merge or resolve claims."""
    query_terms = _terms(claim)
    candidates = []
    for entry in entries:
        if context is not None and not _context_matches(entry, context):
            continue
        recorded_terms = set().union(*(_terms(item) for item in entry.get("claims", [])))
        if len(query_terms & recorded_terms) >= min_shared_terms:
            candidates.append(entry)
    return candidates


def _context_matches(entry: dict, context: str | set[str]) -> bool:
    requested = {context} if isinstance(context, str) else context
    return bool(requested & set(entry.get("contexts", [])))


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
        if "contexts" in label:
            context_assessment = validate_contexts(label["contexts"])
            if not context_assessment.valid:
                raise ValueError(context_assessment.reason)
        elif "context" in label:
            context_assessment = validate_contexts([label["context"]])
            if not context_assessment.valid:
                raise ValueError(context_assessment.reason)
        predicted = {
            entry["entry_id"]
            for entry in find_paraphrase_candidates(
                entries, label["query"], min_shared_terms=min_shared_terms,
                context=(
                    set(label["contexts"])
                    if "contexts" in label else label.get("context")
                ),
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
    context_binding = validate_context_artifacts(entry)
    if not context_binding.valid:
        return LedgerAssessment(False, context_binding.reason)
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
