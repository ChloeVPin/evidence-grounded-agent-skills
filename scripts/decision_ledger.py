#!/usr/bin/env python3
"""Validate durable contradiction and failure-learning ledger entries."""
from dataclasses import dataclass
import hashlib
import json
import re

OUTCOMES = {"supported_refuted", "contextual", "unresolved", "failure"}
CLI_ERROR_CODES = {"NO_CURRENT_ASSERTION", "MALFORMED_EVIDENCE", "AUDIT_GATE_FAILED"}
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


@dataclass(frozen=True)
class AssertionHead:
    valid: bool
    assertion: dict | None
    reason: str


def source_inventory_digest(source_entry_ids: set[str]) -> str:
    """Return a stable digest for the sorted source-entry inventory."""
    payload = json.dumps(sorted(source_entry_ids), separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def source_file_inventory_digest(source_files: dict[str, str]) -> str:
    """Return a stable digest for entry IDs mapped to source file paths."""
    payload = json.dumps(dict(sorted(source_files.items())), separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_source_file_manifest(manifest: dict) -> ContextAssessment:
    """Validate source paths, mapping digest, and recorded file contents."""
    generated_by = manifest.get("generated_by")
    if not isinstance(generated_by, dict) or not generated_by.get("command") or not generated_by.get("revision"):
        return ContextAssessment(False, "manifest generation provenance is required")
    entries = manifest.get("entries")
    if not isinstance(entries, dict) or not entries:
        return ContextAssessment(False, "source file entries are required")
    paths = {}
    for entry_id, record in entries.items():
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            return ContextAssessment(False, f"malformed source file record: {entry_id}")
        if not isinstance(record.get("sha256"), str) or len(record["sha256"]) != 64:
            return ContextAssessment(False, f"missing source file digest: {entry_id}")
        paths[entry_id] = record["path"]
        try:
            with open(record["path"], "rb") as handle:
                actual = hashlib.sha256(handle.read()).hexdigest()
        except OSError:
            return ContextAssessment(False, f"missing source file: {record['path']}")
        if actual != record["sha256"]:
            return ContextAssessment(False, f"source file digest is stale: {entry_id}")
    if manifest.get("mapping_sha256") != source_file_inventory_digest(paths):
        return ContextAssessment(False, "source file mapping digest is stale")
    return ContextAssessment(True, "source file manifest matches")


def check_source_inventory_digest(
    recorded_digest: object, source_entry_ids: set[str],
) -> ContextAssessment:
    """Detect stale migration provenance after the source inventory changes."""
    if not isinstance(recorded_digest, str):
        return ContextAssessment(False, "recorded source inventory digest is not a string")
    expected = source_inventory_digest(source_entry_ids)
    if recorded_digest != expected:
        return ContextAssessment(False, "source inventory digest is stale")
    return ContextAssessment(True, "source inventory digest matches")


def check_generation_revision(
    recorded_revision: object, history_revisions: set[str],
) -> ContextAssessment:
    """Accept historical generation commits only when they remain reachable."""
    if not isinstance(recorded_revision, str) or not recorded_revision:
        return ContextAssessment(False, "generation revision is required")
    if recorded_revision not in history_revisions:
        return ContextAssessment(False, "generation revision is not in repository history")
    return ContextAssessment(True, "generation revision is present in history")


def check_captured_generation_revision(
    recorded_revision: object, evidence: object,
) -> ContextAssessment:
    """Bind a recorded revision to successful captured command evidence."""
    evidence_revision = getattr(evidence, "revision", None)
    exit_status = getattr(evidence, "exit_status", None)
    if isinstance(evidence, dict):
        evidence_revision = evidence.get("revision")
        exit_status = evidence.get("exit_status")
    if recorded_revision != evidence_revision:
        return ContextAssessment(False, "captured revision does not match record")
    if exit_status != 0:
        return ContextAssessment(False, "captured command did not succeed")
    return ContextAssessment(True, "captured revision is bound to successful evidence")


def validate_generation_evidence(
    evidence: dict, expected_command: str, history_revisions: set[str],
) -> ContextAssessment:
    """Audit persisted capture shape, command policy, success, and history."""
    required = ("command", "revision", "exit_status", "output_sha256")
    missing = [field for field in required if field not in evidence]
    if missing:
        return ContextAssessment(False, f"generation evidence missing: {', '.join(missing)}")
    if evidence["command"] != expected_command:
        return ContextAssessment(False, "generation command is outside policy")
    if evidence["exit_status"] != 0:
        return ContextAssessment(False, "generation evidence reports failure")
    if not isinstance(evidence["output_sha256"], str) or len(evidence["output_sha256"]) != 64:
        return ContextAssessment(False, "generation output digest is malformed")
    return check_generation_revision(evidence["revision"], history_revisions)


def validate_captured_output(evidence: dict, output: str) -> ContextAssessment:
    """Verify a capture's recorded digest against the exact command output."""
    expected = evidence.get("output_sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        return ContextAssessment(False, "captured output digest is malformed")
    actual = hashlib.sha256(output.encode()).hexdigest()
    if actual != expected:
        return ContextAssessment(False, "captured output digest does not match output")
    return ContextAssessment(True, "captured output digest matches output")


def validate_policy_audit(audit: dict) -> ContextAssessment:
    """Validate a persisted result of generation-evidence policy review."""
    required = ("audit_id", "policy", "result", "evidence_refs")
    missing = [field for field in required if field not in audit]
    if missing:
        return ContextAssessment(False, f"policy audit missing fields: {', '.join(missing)}")
    if not audit["policy"] or audit["result"] not in {"passed", "failed"}:
        return ContextAssessment(False, "policy audit policy and result are required")
    if not isinstance(audit["evidence_refs"], list) or not audit["evidence_refs"]:
        return ContextAssessment(False, "policy audit evidence references are required")
    return ContextAssessment(True, "valid policy audit")


def validate_cli_output(output: dict) -> ContextAssessment:
    """Validate the documented success or failure JSON output contract."""
    if output.get("result") == "passed":
        if not isinstance(output.get("audit_id"), str):
            return ContextAssessment(False, "successful CLI output needs audit_id")
        checks = output.get("checks")
        if checks != {"bundle": True, "content": True, "result": True}:
            return ContextAssessment(False, "successful CLI checks are incomplete")
        if output.get("error_code") is not None:
            return ContextAssessment(False, "successful CLI output must have null error code")
        return ContextAssessment(True, "valid successful CLI output")
    if output.get("result") == "failed" and output.get("error_code") in CLI_ERROR_CODES:
        return ContextAssessment(True, "valid failed CLI output")
    return ContextAssessment(False, "invalid CLI output contract")


def audit_policy_assertion_chain(assertions: list[dict]) -> ContextAssessment:
    """Ensure versioned policy assertions have one current, linked head."""
    ids = [item.get("audit_id") for item in assertions]
    if not assertions or any(not item_id for item_id in ids):
        return ContextAssessment(False, "policy assertion IDs are required")
    if len(set(ids)) != len(ids):
        return ContextAssessment(False, "duplicate policy assertion IDs")
    known = set(ids)
    current = [item for item in assertions if item.get("status") == "current"]
    if len(current) != 1:
        return ContextAssessment(False, "exactly one current policy assertion is required")
    for item in assertions:
        if item.get("status") == "superseded":
            successor = item.get("superseded_by")
            if successor not in known:
                return ContextAssessment(False, "superseded assertion references unknown successor")
        elif item.get("status") != "current":
            return ContextAssessment(False, "unknown policy assertion status")
    return ContextAssessment(True, "policy assertion chain is continuous")


def discover_current_assertion(assertions: list[dict]) -> AssertionHead:
    """Discover the current assertion only after validating the full chain."""
    chain = audit_policy_assertion_chain(assertions)
    if not chain.valid:
        return AssertionHead(False, None, chain.reason)
    current = next(item for item in assertions if item.get("status") == "current")
    return AssertionHead(True, current, "current assertion discovered")


def audit_policy_assertion_references(
    assertions: list[dict], available_paths: set[str],
) -> ContextAssessment:
    """Require every assertion evidence reference to exist in the repository."""
    for assertion in assertions:
        validation = validate_policy_audit(assertion)
        if not validation.valid:
            return validation
        missing = [ref for ref in assertion["evidence_refs"] if ref not in available_paths]
        if missing:
            return ContextAssessment(False, f"missing policy evidence reference: {missing[0]}")
    return ContextAssessment(True, "all policy evidence references exist")


def compare_policy_audit(audit: dict, evidence: dict) -> ContextAssessment:
    """Compare a persisted policy assertion with a fresh captured result."""
    audit_check = validate_policy_audit(audit)
    if not audit_check.valid:
        return audit_check
    if audit["policy"] != evidence.get("command"):
        return ContextAssessment(False, "fresh evidence command differs from policy")
    expected_result = "passed" if evidence.get("exit_status") == 0 else "failed"
    if audit["result"] != expected_result:
        return ContextAssessment(False, "persisted policy result differs from fresh evidence")
    if evidence.get("output_sha256") in (None, ""):
        return ContextAssessment(False, "fresh evidence output digest is missing")
    return ContextAssessment(True, "persisted policy assertion matches fresh evidence")


def validate_policy_audit_bundle(
    audit: dict, evidence: dict, available_paths: set[str],
) -> ContextAssessment:
    """Compose assertion shape, reference, and fresh-result validation."""
    reference_check = audit_policy_assertion_references([audit], available_paths)
    if not reference_check.valid:
        return reference_check
    return compare_policy_audit(audit, evidence)


def validate_policy_assertion_content(
    audit: dict, content_digests: dict[str, str],
) -> ContextAssessment:
    """Verify SHA-256 content digests for every assertion reference."""
    audit_check = validate_policy_audit(audit)
    if not audit_check.valid:
        return audit_check
    for reference in audit["evidence_refs"]:
        expected = content_digests.get(reference)
        if not isinstance(expected, str) or len(expected) != 64:
            return ContextAssessment(False, f"missing content digest: {reference}")
        try:
            with open(reference, "rb") as handle:
                actual = hashlib.sha256(handle.read()).hexdigest()
        except OSError:
            return ContextAssessment(False, f"missing assertion reference: {reference}")
        if actual != expected:
            return ContextAssessment(False, f"assertion reference content drift: {reference}")
    return ContextAssessment(True, "assertion reference content matches")


def validate_current_assertion_bundle(
    bundle: dict, available_paths: set[str],
) -> ContextAssessment:
    """Validate the durable index joining current assertion evidence layers."""
    required = ("bundle_id", "assertion_ref", "capture_ref", "content_digest_ref")
    missing = [field for field in required if field not in bundle]
    if missing:
        return ContextAssessment(False, f"assertion bundle missing: {', '.join(missing)}")
    refs = [bundle[field] for field in required[1:]]
    if any(not isinstance(ref, str) or ref not in available_paths for ref in refs):
        return ContextAssessment(False, "assertion bundle reference is unavailable")
    return ContextAssessment(True, "current assertion bundle is complete")


def validate_self_validation_bundle(
    bundle: dict, available_paths: set[str],
) -> ContextAssessment:
    """Validate the bundle that records this audit's validation of an assertion."""
    required = (
        "bundle_id", "assertion_ref", "test_capture_ref",
        "self_validation_capture_ref", "current_assertion_bundle_ref",
    )
    missing = [field for field in required if field not in bundle]
    if missing:
        return ContextAssessment(False, f"self-validation bundle missing: {', '.join(missing)}")
    refs = [bundle[field] for field in required[1:]]
    if any(not isinstance(ref, str) or ref not in available_paths for ref in refs):
        return ContextAssessment(False, "self-validation bundle reference is unavailable")
    if bundle["test_capture_ref"] == bundle["self_validation_capture_ref"]:
        return ContextAssessment(False, "self-validation capture must be distinct")
    return ContextAssessment(True, "self-validation bundle is complete")


def validate_self_validation_bundle_against_chain(
    bundle: dict, assertions: list[dict], available_paths: set[str],
) -> ContextAssessment:
    """Require a self-validation bundle to name the discovered current head."""
    bundle_check = validate_self_validation_bundle(bundle, available_paths)
    if not bundle_check.valid:
        return bundle_check
    head = discover_current_assertion(assertions)
    if not head.valid:
        return ContextAssessment(False, head.reason)
    expected = f"ledger/evidence/{head.assertion['audit_id']}.json"
    if bundle["assertion_ref"] != expected:
        return ContextAssessment(False, "self-validation bundle does not name current assertion")
    return ContextAssessment(True, "self-validation bundle names current assertion")


def validate_complete_self_validation_bundle(
    bundle: dict, assertions: list[dict], current_bundle: dict,
    audit: dict, test_capture: dict, self_capture: dict,
    content_digests: dict[str, str], self_validation_output: str,
    available_paths: set[str],
) -> ContextAssessment:
    """Run every evidence-layer gate for a self-validation bundle."""
    bundle_check = validate_self_validation_bundle_against_chain(
        bundle, assertions, available_paths,
    )
    if not bundle_check.valid:
        return bundle_check
    current_check = validate_current_assertion_bundle(current_bundle, available_paths)
    if not current_check.valid:
        return current_check
    if bundle["current_assertion_bundle_ref"] not in available_paths:
        return ContextAssessment(False, "current assertion bundle reference is unavailable")
    if current_bundle["assertion_ref"] != bundle["assertion_ref"]:
        return ContextAssessment(False, "assertion bundle and self-validation bundle disagree")
    if not compare_policy_audit(audit, test_capture).valid:
        return ContextAssessment(False, "current assertion does not match test capture")
    if not validate_policy_assertion_content(audit, content_digests).valid:
        return ContextAssessment(False, "current assertion content is not intact")
    if not validate_generation_evidence(
        self_capture, "python3 scripts/audit_current_assertion.py",
        {self_capture.get("revision")},
    ).valid:
        return ContextAssessment(False, "self-validation capture is not successful")
    output_check = validate_captured_output(self_capture, self_validation_output)
    if not output_check.valid:
        return output_check
    return ContextAssessment(True, "complete self-validation bundle is valid")


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
        "artifacts", "reason", "reversible", "source_inventory_sha256",
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
    digest = migration["source_inventory_sha256"]
    if not isinstance(digest, str) or len(digest) != 64:
        return ContextAssessment(False, "source inventory digest must be sha256")
    try:
        int(digest, 16)
    except ValueError:
        return ContextAssessment(False, "source inventory digest must be hexadecimal")
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
