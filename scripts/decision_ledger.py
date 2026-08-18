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


def validate_four_check_capture(
    capture: dict, expected_command: str, history_revisions: set[str],
) -> ContextAssessment:
    """Validate the structured versioned capture of a successful CLI audit."""
    required = (
        "capture_id", "audit_id", "command", "revision", "exit_status",
        "output_sha256", "checks", "result", "error_code",
    )
    missing = [field for field in required if field not in capture]
    if missing:
        return ContextAssessment(False, f"four-check capture missing: {', '.join(missing)}")
    evidence_check = validate_generation_evidence(
        capture, expected_command, history_revisions,
    )
    if not evidence_check.valid:
        return evidence_check
    if not isinstance(capture["audit_id"], str) or capture["result"] != "passed":
        return ContextAssessment(False, "four-check capture result is malformed")
    if capture["checks"] != {
        "bundle": True, "content": True, "freshness": True, "result": True,
    } or capture["error_code"] is not None:
        return ContextAssessment(False, "four-check capture checks are incomplete")
    return ContextAssessment(True, "four-check capture is valid")


def validate_snapshot_diagnostic_capture(
    capture: dict, snapshot: dict, available_paths: set[str],
    history_revisions: set[str],
) -> ContextAssessment:
    """Validate a capture that binds a diagnostic snapshot to an audit run."""
    required = (
        "capture_id", "command", "revision", "exit_status", "output_sha256",
        "snapshot_ref", "snapshot_sha256", "audit_result",
    )
    missing = [field for field in required if field not in capture]
    if missing:
        return ContextAssessment(False, f"snapshot capture missing: {', '.join(missing)}")
    evidence_check = validate_generation_evidence(
        capture, "python3 scripts/audit_current_assertion.py", history_revisions,
    )
    if not evidence_check.valid:
        return evidence_check
    if capture["snapshot_ref"] not in available_paths:
        return ContextAssessment(False, "snapshot capture reference is unavailable")
    expected_digest = hashlib.sha256(
        json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if capture["snapshot_sha256"] != expected_digest:
        return ContextAssessment(False, "snapshot capture digest is stale")
    if capture["audit_result"] != "passed":
        return ContextAssessment(False, "snapshot capture audit result is not passed")
    return ContextAssessment(True, "snapshot diagnostic capture is valid")


def validate_graph_state_diagnostic_capture(
    capture: dict, graph: dict, available_paths: set[str],
    history_revisions: set[str], snapshot: dict | None = None,
) -> ContextAssessment:
    """Validate a capture that binds graph policy to a successful audit run."""
    required = (
        "capture_id", "command", "revision", "exit_status", "output_sha256",
        "graph_ref", "graph_policy_sha256", "audit_result",
    )
    missing = [field for field in required if field not in capture]
    if missing:
        return ContextAssessment(False, f"graph capture missing: {', '.join(missing)}")
    evidence_check = validate_generation_evidence(
        capture, "python3 scripts/audit_current_assertion.py", history_revisions,
    )
    if not evidence_check.valid:
        return evidence_check
    if capture["graph_ref"] not in available_paths:
        return ContextAssessment(False, "graph capture reference is unavailable")
    if capture["graph_policy_sha256"] != graph.get("policy_sha256"):
        return ContextAssessment(False, "graph capture policy digest is stale")
    if snapshot is not None:
        if capture.get("snapshot_ref") != "ledger/evidence/0130-dependency-state-diagnostics.json":
            return ContextAssessment(False, "graph capture snapshot reference is invalid")
        expected_digest = hashlib.sha256(
            json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if capture.get("snapshot_sha256") != expected_digest:
            return ContextAssessment(False, "graph capture snapshot digest is stale")
        if capture.get("edge_refs") != [[
            "ledger/evidence/0154-freshness-capture-inventory.json",
            "ledger/evidence/0134-snapshot-diagnostic-capture.json",
        ]]:
            return ContextAssessment(False, "graph capture provenance edges are stale")
    if capture["audit_result"] != "passed":
        return ContextAssessment(False, "graph capture audit result is not passed")
    return ContextAssessment(True, "graph state diagnostic capture is valid")


def validate_audit_capture_dependency_summary(
    summary: dict, available_paths: set[str], expected_refs: dict[str, set[str]],
) -> ContextAssessment:
    """Validate the complete versioned capture/state/policy reference summary."""
    if summary.get("summary_id") != "0146-audit-capture-dependencies":
        return ContextAssessment(False, "audit capture dependency summary ID is invalid")
    if not isinstance(summary.get("summary_sha256"), str):
        return ContextAssessment(False, "audit capture dependency summary digest is missing")
    for field, expected in expected_refs.items():
        values = summary.get(field)
        if not isinstance(values, list) or set(values) != expected or len(values) != len(expected):
            return ContextAssessment(False, f"audit capture dependency summary {field} differs")
        if not set(values) <= available_paths:
            return ContextAssessment(False, f"audit capture dependency summary {field} is unavailable")
    payload = dict(summary)
    payload.pop("summary_sha256", None)
    expected_digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if summary["summary_sha256"] != expected_digest:
        return ContextAssessment(False, "audit capture dependency summary digest is stale")
    return ContextAssessment(True, "audit capture dependency summary is complete")


def validate_summary_state_diagnostic_capture(
    capture: dict, summary: dict, available_paths: set[str],
    history_revisions: set[str],
) -> ContextAssessment:
    """Validate a capture that binds summary state to a successful audit run."""
    required = (
        "capture_id", "command", "revision", "exit_status", "output_sha256",
        "summary_ref", "summary_sha256", "audit_result",
    )
    missing = [field for field in required if field not in capture]
    if missing:
        return ContextAssessment(False, f"summary capture missing: {', '.join(missing)}")
    evidence_check = validate_generation_evidence(
        capture, "python3 scripts/audit_current_assertion.py", history_revisions,
    )
    if not evidence_check.valid:
        return evidence_check
    if capture["summary_ref"] not in available_paths:
        return ContextAssessment(False, "summary capture reference is unavailable")
    if capture["summary_sha256"] != summary.get("summary_sha256"):
        return ContextAssessment(False, "summary capture digest is stale")
    if capture["audit_result"] != "passed":
        return ContextAssessment(False, "summary capture audit result is not passed")
    return ContextAssessment(True, "summary state diagnostic capture is valid")


def validate_freshness_capture_inventory(
    inventory: dict, available_paths: set[str], expected_captures: set[str],
    expected_failures: set[str] | None = None,
    expected_diagnostics: set[str] | None = None,
    expected_snapshots: set[str] | None = None,
    expected_edge_failures: set[str] | None = None,
    expected_state_failures: set[str] | None = None,
) -> ContextAssessment:
    """Validate the complete inventory of persisted freshness captures."""
    if inventory.get("inventory_id") != "0154-freshness-capture-inventory":
        return ContextAssessment(False, "freshness capture inventory ID is invalid")
    if not isinstance(inventory.get("inventory_sha256"), str):
        return ContextAssessment(False, "freshness capture inventory digest is missing")
    captures = inventory.get("capture_refs")
    if not isinstance(captures, list) or set(captures) != expected_captures or len(captures) != len(expected_captures):
        return ContextAssessment(False, "freshness capture inventory captures differ")
    if expected_failures is not None:
        failures = inventory.get("failure_refs")
        if (not isinstance(failures, list) or set(failures) != expected_failures
                or len(failures) != len(expected_failures)):
            return ContextAssessment(False, "freshness capture inventory failures differ")
    else:
        failures = inventory.get("failure_refs", [])
    if expected_diagnostics is not None:
        diagnostics = inventory.get("diagnostic_refs")
        if (not isinstance(diagnostics, list) or set(diagnostics) != expected_diagnostics
                or len(diagnostics) != len(expected_diagnostics)):
            return ContextAssessment(False, "freshness capture inventory diagnostics differ")
    else:
        diagnostics = inventory.get("diagnostic_refs", [])
    if expected_snapshots is not None:
        snapshots = inventory.get("snapshot_provenance_refs")
        if (not isinstance(snapshots, list) or set(snapshots) != expected_snapshots
                or len(snapshots) != len(expected_snapshots)):
            return ContextAssessment(False, "freshness capture inventory snapshots differ")
    else:
        snapshots = inventory.get("snapshot_provenance_refs", [])
    if expected_edge_failures is not None:
        edge_failures = inventory.get("edge_failure_refs")
        if (not isinstance(edge_failures, list) or set(edge_failures) != expected_edge_failures
                or len(edge_failures) != len(expected_edge_failures)):
            return ContextAssessment(False, "freshness capture inventory edge failures differ")
    else:
        edge_failures = inventory.get("edge_failure_refs", [])
    if expected_state_failures is not None:
        state_failures = inventory.get("state_failure_refs")
        if (not isinstance(state_failures, list) or set(state_failures) != expected_state_failures
                or len(state_failures) != len(expected_state_failures)):
            return ContextAssessment(False, "freshness capture inventory state failures differ")
    else:
        state_failures = inventory.get("state_failure_refs", [])
    refs = captures + failures + diagnostics + snapshots + edge_failures + state_failures + [inventory.get("state_ref"), inventory.get("summary_ref"), inventory.get("graph_ref")]
    if any(ref not in available_paths for ref in refs):
        return ContextAssessment(False, "freshness capture inventory reference is unavailable")
    payload = dict(inventory)
    payload.pop("inventory_sha256", None)
    expected_digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if inventory["inventory_sha256"] != expected_digest:
        return ContextAssessment(False, "freshness capture inventory digest is stale")
    return ContextAssessment(True, "freshness capture inventory is complete")


def validate_failure_evidence(record: dict, available_paths: set[str]) -> ContextAssessment:
    """Validate a persisted diagnostic record for a failed audit gate."""
    required = (
        "evidence_id", "source_capture_ref", "mutation", "failed_check",
        "error_code", "reason", "diagnostic_ref", "diagnostic_reason",
    )
    missing = [field for field in required if field not in record]
    if missing:
        return ContextAssessment(False, f"failure evidence missing: {', '.join(missing)}")
    if record["source_capture_ref"] not in available_paths:
        return ContextAssessment(False, "failure evidence source is unavailable")
    if (record["error_code"] not in CLI_ERROR_CODES or not record["reason"].strip()
            or record["diagnostic_ref"] not in available_paths
            or not record["diagnostic_reason"].strip()):
        return ContextAssessment(False, "failure evidence diagnostic fields are malformed")
    if "edge_refs" in record and record["edge_refs"] != [[
        "ledger/evidence/0154-freshness-capture-inventory.json",
        "ledger/evidence/0134-snapshot-diagnostic-capture.json",
    ]]:
        return ContextAssessment(False, "failure evidence edge provenance is malformed")
    return ContextAssessment(True, "failure evidence is valid")


def validate_audit_dependency_manifest(
    manifest: dict, available_paths: set[str], expected_paths: set[str],
) -> ContextAssessment:
    """Require an exact, existing dependency set for the executable audit."""
    if manifest.get("manifest_id") != "0125-audit-dependencies":
        return ContextAssessment(False, "audit dependency manifest ID is invalid")
    paths = manifest.get("paths")
    if not isinstance(paths, list) or any(not isinstance(path, str) for path in paths):
        return ContextAssessment(False, "audit dependency manifest paths are malformed")
    recorded = set(paths)
    if len(recorded) != len(paths):
        return ContextAssessment(False, "audit dependency manifest has duplicate paths")
    if recorded != expected_paths:
        return ContextAssessment(False, "audit dependency manifest differs from expected set")
    if not recorded <= available_paths:
        return ContextAssessment(False, "audit dependency manifest references unavailable paths")
    expected_digest = hashlib.sha256(
        json.dumps(sorted(recorded), separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if manifest.get("paths_sha256") != expected_digest:
        return ContextAssessment(False, "audit dependency manifest digest is stale")
    return ContextAssessment(True, "audit dependency manifest is complete")


def validate_dependency_diagnostic_snapshot(
    snapshot: dict, available_paths: set[str],
) -> ContextAssessment:
    """Validate the versioned expectations for dependency-state diagnostics."""
    if snapshot.get("snapshot_id") != "0130-dependency-state-diagnostics":
        return ContextAssessment(False, "dependency diagnostic snapshot ID is invalid")
    if snapshot.get("source_state_ref") not in available_paths:
        return ContextAssessment(False, "dependency diagnostic snapshot source is unavailable")
    cases = snapshot.get("cases")
    if not isinstance(cases, list) or len(cases) != 8:
        return ContextAssessment(False, "dependency diagnostic snapshot cases are incomplete")
    expected_reasons = {
        "self-validation state dependency digest differs from manifest",
        "self-validation state manifest reference is invalid",
        "self-validation state inventory digest is stale",
        "self-validation state diagnostic references are stale",
        "self-validation state graph provenance is stale",
        "self-validation state snapshot provenance is stale",
        "graph capture provenance edges are stale",
        "self-validation state edge failure provenance is stale",
    }
    reasons = set()
    for case in cases:
        if not isinstance(case, dict):
            return ContextAssessment(False, "dependency diagnostic snapshot case is malformed")
        if case.get("failed_check") != "freshness" or case.get("error_code") != "AUDIT_GATE_FAILED":
            return ContextAssessment(False, "dependency diagnostic snapshot case contract is invalid")
        reasons.add(case.get("reason"))
    if reasons != expected_reasons:
        return ContextAssessment(False, "dependency diagnostic snapshot reasons differ")
    return ContextAssessment(True, "dependency diagnostic snapshot is valid")


def validate_freshness_dependency_graph(
    graph: dict, expected_nodes: set[str], available_paths: set[str],
) -> ContextAssessment:
    """Validate the persisted graph of freshness-specific audit inputs."""
    if graph.get("graph_id") != "0137-freshness-dependency-graph":
        return ContextAssessment(False, "freshness dependency graph ID is invalid")
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or set(nodes) != expected_nodes or len(nodes) != len(expected_nodes):
        return ContextAssessment(False, "freshness dependency graph nodes differ")
    if not isinstance(edges, list) or any(
        not isinstance(edge, list) or len(edge) != 2
        or edge[0] not in expected_nodes or edge[1] not in expected_nodes
        for edge in edges
    ):
        return ContextAssessment(False, "freshness dependency graph edges are malformed")
    if not set(nodes) <= available_paths:
        return ContextAssessment(False, "freshness dependency graph references unavailable paths")
    policy_digest = hashlib.sha256(
        json.dumps(sorted(expected_nodes), separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if graph.get("policy_sha256") != policy_digest:
        return ContextAssessment(False, "freshness dependency graph policy digest is stale")
    return ContextAssessment(True, "freshness dependency graph is valid")


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
        if checks != {"bundle": True, "content": True, "result": True, "freshness": True}:
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


def validate_self_validation_state(
    state: dict, bundle_ref: str, self_capture: dict, manifest: dict | None = None,
    diagnostic_snapshot: dict | None = None, dependency_graph: dict | None = None,
    capture_summary: dict | None = None, capture_inventory: dict | None = None,
) -> ContextAssessment:
    """Validate the persisted result of the complete self-validation gate."""
    required = (
        "schema_version", "cycle_id", "status", "validated_revision", "bundle_ref", "checks",
        "self_validation_output_sha256", "dependency_manifest_ref",
        "dependency_paths_sha256", "diagnostic_snapshot_ref",
        "diagnostic_snapshot_sha256", "dependency_graph_ref",
        "dependency_graph_policy_sha256", "capture_summary_ref",
        "capture_summary_sha256", "capture_inventory_ref",
        "capture_inventory_sha256", "diagnostic_refs", "diagnostic_refs_sha256",
        "graph_provenance_refs", "graph_provenance_refs_sha256",
        "snapshot_provenance_refs", "snapshot_provenance_refs_sha256",
        "edge_failure_refs", "edge_failure_refs_sha256",
    )
    missing = [field for field in required if field not in state]
    if missing:
        return ContextAssessment(False, f"self-validation state missing: {', '.join(missing)}")
    expected_checks = {
        "bundle", "chain", "assertion", "test_result", "content",
        "self_capture", "self_output_digest",
    }
    checks = state["checks"]
    if state["schema_version"] != 1 or state["status"] != "passed":
        return ContextAssessment(False, "self-validation state is not a passing schema version 1 result")
    if state["validated_revision"] != self_capture.get("revision"):
        return ContextAssessment(False, "self-validation state revision differs from capture")
    if manifest is not None:
        if state["dependency_manifest_ref"] != "ledger/evidence/0125-audit-dependencies.json":
            return ContextAssessment(False, "self-validation state manifest reference is invalid")
        if state["dependency_paths_sha256"] != manifest.get("paths_sha256"):
            return ContextAssessment(False, "self-validation state dependency digest differs from manifest")
    if diagnostic_snapshot is not None:
        if state["diagnostic_snapshot_ref"] != "ledger/evidence/0130-dependency-state-diagnostics.json":
            return ContextAssessment(False, "self-validation state diagnostic reference is invalid")
        expected_digest = hashlib.sha256(
            json.dumps(diagnostic_snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if state["diagnostic_snapshot_sha256"] != expected_digest:
            return ContextAssessment(False, "self-validation state diagnostic digest is stale")
    if dependency_graph is not None:
        if state["dependency_graph_ref"] != "ledger/evidence/0137-freshness-dependency-graph.json":
            return ContextAssessment(False, "self-validation state graph reference is invalid")
        if state["dependency_graph_policy_sha256"] != dependency_graph.get("policy_sha256"):
            return ContextAssessment(False, "self-validation state graph policy digest is stale")
    if capture_summary is not None:
        if state["capture_summary_ref"] != "ledger/evidence/0146-audit-capture-dependencies.json":
            return ContextAssessment(False, "self-validation state summary reference is invalid")
        if state["capture_summary_sha256"] != capture_summary.get("summary_sha256"):
            return ContextAssessment(False, "self-validation state summary digest is stale")
        expected_graph_refs = capture_summary.get("graph_provenance_refs")
        if (state["graph_provenance_refs"] != expected_graph_refs
                or state["graph_provenance_refs_sha256"] != hashlib.sha256(
                    json.dumps(sorted(expected_graph_refs), separators=(",", ":")).encode("utf-8")
                ).hexdigest()):
            return ContextAssessment(False, "self-validation state graph provenance is stale")
    if capture_inventory is not None:
        if state["capture_inventory_ref"] != "ledger/evidence/0154-freshness-capture-inventory.json":
            return ContextAssessment(False, "self-validation state inventory reference is invalid")
        if state["capture_inventory_sha256"] != capture_inventory.get("inventory_sha256"):
            return ContextAssessment(False, "self-validation state inventory digest is stale")
        expected_refs = capture_inventory.get("diagnostic_refs")
        if (state["diagnostic_refs"] != expected_refs
                or state["diagnostic_refs_sha256"] != hashlib.sha256(
                    json.dumps(sorted(expected_refs), separators=(",", ":")).encode("utf-8")
                ).hexdigest()):
            return ContextAssessment(False, "self-validation state diagnostic references are stale")
        expected_snapshots = capture_inventory.get("snapshot_provenance_refs")
        if (state["snapshot_provenance_refs"] != expected_snapshots
                or state["snapshot_provenance_refs_sha256"] != hashlib.sha256(
                    json.dumps(sorted(expected_snapshots), separators=(",", ":")).encode("utf-8")
                ).hexdigest()):
            return ContextAssessment(False, "self-validation state snapshot provenance is stale")
        expected_edge_failures = capture_inventory.get("edge_failure_refs")
        if (state["edge_failure_refs"] != expected_edge_failures
                or state["edge_failure_refs_sha256"] != hashlib.sha256(
                    json.dumps(sorted(expected_edge_failures), separators=(",", ":")).encode("utf-8")
                ).hexdigest()):
            return ContextAssessment(False, "self-validation state edge failure provenance is stale")
    if state["bundle_ref"] != bundle_ref or not isinstance(checks, dict):
        return ContextAssessment(False, "self-validation state bundle or checks are malformed")
    if set(checks) != expected_checks or any(value is not True for value in checks.values()):
        return ContextAssessment(False, "self-validation state checks are incomplete")
    if state["self_validation_output_sha256"] != self_capture.get("output_sha256"):
        return ContextAssessment(False, "self-validation state digest differs from capture")
    return ContextAssessment(True, "self-validation state is a complete passing result")


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
