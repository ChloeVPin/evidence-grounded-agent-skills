#!/usr/bin/env python3
"""Run the complete current policy-assertion audit as one command."""
import json
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

NO_CURRENT_ASSERTION = "NO_CURRENT_ASSERTION"
MALFORMED_EVIDENCE = "MALFORMED_EVIDENCE"
AUDIT_GATE_FAILED = "AUDIT_GATE_FAILED"

EXPECTED_DEPENDENCIES = {
    "scripts/audit_current_assertion.py",
    "ledger/evidence/0085-generation-policy-audit.json",
    "ledger/evidence/0087-generation-policy-audit.json",
    "ledger/evidence/0093-generation-policy-audit.json",
    "ledger/evidence/0093-current-assertion-bundle.json",
    "ledger/evidence/0093-generation-rerun.json",
    "ledger/evidence/0093-policy-content-digests.json",
    "ledger/evidence/0108-self-validation-bundle.json",
    "ledger/evidence/0108-audit-command-capture.json",
    "ledger/evidence/0119-four-check-audit-capture.json",
    "ledger/evidence/0122-capture-schema-failure.json",
    "ledger/evidence/0154-freshness-capture-inventory.json",
    "ledger/evidence/0162-graph-edge-failure.json",
    "ledger/state/0113-complete-self-validation-gate.json",
}
EXPECTED_FRESHNESS_GRAPH_NODES = {
    "scripts/audit_current_assertion.py",
    "ledger/evidence/0125-audit-dependencies.json",
    "ledger/evidence/0130-dependency-state-diagnostics.json",
    "ledger/evidence/0134-snapshot-diagnostic-capture.json",
    "ledger/state/0113-complete-self-validation-gate.json",
    "ledger/evidence/0154-freshness-capture-inventory.json",
}

from scripts.decision_ledger import (
    compare_policy_audit,
    discover_current_assertion,
    validate_current_assertion_bundle,
    validate_policy_assertion_content,
    validate_self_validation_state,
    validate_four_check_capture,
    validate_failure_evidence,
    validate_audit_dependency_manifest,
    validate_dependency_diagnostic_snapshot,
    validate_snapshot_diagnostic_capture,
    validate_freshness_dependency_graph,
    validate_graph_state_diagnostic_capture,
    validate_audit_capture_dependency_summary,
    validate_summary_state_diagnostic_capture,
    validate_freshness_capture_inventory,
    validate_cli_output,
)


def _emit(payload: dict) -> bool:
    valid = validate_cli_output(payload).valid
    print(json.dumps(payload, sort_keys=True))
    return valid


def _run(root: Path = ROOT) -> int:
    evidence_dir = root / "ledger" / "evidence"
    assertions = [
        json.loads(path.read_text())
        for path in sorted(evidence_dir.glob("*-generation-policy-audit.json"))
    ]
    head = discover_current_assertion(assertions)
    if not head.valid:
        _emit({"error_code": NO_CURRENT_ASSERTION,
               "result": "failed", "reason": head.reason})
        return 1
    dependency_manifest = json.loads(
        (evidence_dir / "0125-audit-dependencies.json").read_text()
    )
    dependency_available = {
        path for path in EXPECTED_DEPENDENCIES
        if (root / path).exists()
        or (path == "scripts/audit_current_assertion.py" and Path(__file__).exists())
    }
    dependency_check = validate_audit_dependency_manifest(
        dependency_manifest, dependency_available, EXPECTED_DEPENDENCIES,
    )
    dependency_graph = json.loads(
        (evidence_dir / "0137-freshness-dependency-graph.json").read_text()
    )
    graph_available = {
        path for path in dependency_graph.get("nodes", [])
        if (root / path).exists()
        or (path == "scripts/audit_current_assertion.py" and Path(__file__).exists())
    }
    graph_check = validate_freshness_dependency_graph(
        dependency_graph, EXPECTED_FRESHNESS_GRAPH_NODES, graph_available,
    )
    audit = head.assertion
    bundle_path = evidence_dir / f"{audit['audit_id'][:4]}-current-assertion-bundle.json"
    bundle = json.loads(bundle_path.read_text())
    expected_assertion_ref = f"ledger/evidence/{audit['audit_id']}.json"
    available = set(audit["evidence_refs"]) | {
        expected_assertion_ref, bundle["content_digest_ref"],
    }
    bundle_check = validate_current_assertion_bundle(bundle, available)
    capture = json.loads((root / bundle["capture_ref"]).read_text())
    result_check = compare_policy_audit(audit, capture)
    digests = json.loads((root / bundle["content_digest_ref"]).read_text())
    content_check = validate_policy_assertion_content(audit, digests)
    self_bundle = json.loads((evidence_dir / "0108-self-validation-bundle.json").read_text())
    self_capture = json.loads((root / self_bundle["self_validation_capture_ref"]).read_text())
    diagnostic_snapshot = json.loads(
        (evidence_dir / "0130-dependency-state-diagnostics.json").read_text()
    )
    capture_summary = json.loads(
        (evidence_dir / "0146-audit-capture-dependencies.json").read_text()
    )
    capture_inventory = json.loads(
        (evidence_dir / "0154-freshness-capture-inventory.json").read_text()
    )
    state_path = root / "ledger/state/0113-complete-self-validation-gate.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    freshness_check = validate_self_validation_state(
        state, "ledger/evidence/0108-self-validation-bundle.json", self_capture,
        dependency_manifest,
        diagnostic_snapshot,
        dependency_graph,
        capture_summary,
        capture_inventory,
    )
    four_check_capture = json.loads(
        (evidence_dir / "0119-four-check-audit-capture.json").read_text()
    )
    capture_schema_check = validate_four_check_capture(
        four_check_capture, "python3 scripts/audit_current_assertion.py",
        {four_check_capture.get("revision")},
    )
    failure_evidence = json.loads(
        (evidence_dir / "0122-capture-schema-failure.json").read_text()
    )
    failure_evidence_check = validate_failure_evidence(
        failure_evidence, {
            "ledger/evidence/0119-four-check-audit-capture.json",
            "ledger/evidence/0154-freshness-capture-inventory.json",
        },
    )
    graph_failure_evidence = json.loads(
        (evidence_dir / "0162-graph-edge-failure.json").read_text()
    )
    graph_failure_evidence_check = validate_failure_evidence(
        graph_failure_evidence, {
            "ledger/evidence/0143-graph-state-diagnostic-capture.json",
            "ledger/evidence/0154-freshness-capture-inventory.json",
        },
    )
    diagnostic_snapshot_check = validate_dependency_diagnostic_snapshot(
        diagnostic_snapshot, {"ledger/state/0113-complete-self-validation-gate.json"},
    )
    snapshot_capture = json.loads(
        (evidence_dir / "0134-snapshot-diagnostic-capture.json").read_text()
    )
    snapshot_capture_check = validate_snapshot_diagnostic_capture(
        snapshot_capture, diagnostic_snapshot,
        {"ledger/evidence/0130-dependency-state-diagnostics.json"},
        {snapshot_capture.get("revision")},
    )
    graph_capture = json.loads(
        (evidence_dir / "0143-graph-state-diagnostic-capture.json").read_text()
    )
    graph_capture_check = validate_graph_state_diagnostic_capture(
        graph_capture, dependency_graph,
        {"ledger/evidence/0137-freshness-dependency-graph.json"},
        {graph_capture.get("revision")},
    )
    capture_summary_check = validate_audit_capture_dependency_summary(
        capture_summary,
        {path for values in (
            capture_summary.get("capture_refs", []),
            capture_summary.get("state_refs", []),
            capture_summary.get("policy_refs", []),
        ) for path in values if (root / path).exists()},
        {
            "capture_refs": {
                "ledger/evidence/0093-generation-rerun.json",
                "ledger/evidence/0108-audit-command-capture.json",
                "ledger/evidence/0119-four-check-audit-capture.json",
                "ledger/evidence/0134-snapshot-diagnostic-capture.json",
                "ledger/evidence/0143-graph-state-diagnostic-capture.json",
            },
            "state_refs": {"ledger/state/0113-complete-self-validation-gate.json"},
            "policy_refs": {
                "ledger/evidence/0125-audit-dependencies.json",
                "ledger/evidence/0130-dependency-state-diagnostics.json",
                "ledger/evidence/0137-freshness-dependency-graph.json",
            },
        },
    )
    summary_capture = json.loads(
        (evidence_dir / "0151-summary-state-diagnostic-capture.json").read_text()
    )
    summary_capture_check = validate_summary_state_diagnostic_capture(
        summary_capture, capture_summary,
        {"ledger/evidence/0146-audit-capture-dependencies.json"},
        {summary_capture.get("revision")},
    )
    capture_inventory = json.loads(
        (evidence_dir / "0154-freshness-capture-inventory.json").read_text()
    )
    inventory_expected = {
        "ledger/evidence/0093-generation-rerun.json",
        "ledger/evidence/0108-audit-command-capture.json",
        "ledger/evidence/0119-four-check-audit-capture.json",
        "ledger/evidence/0134-snapshot-diagnostic-capture.json",
        "ledger/evidence/0143-graph-state-diagnostic-capture.json",
        "ledger/evidence/0151-summary-state-diagnostic-capture.json",
    }
    inventory_available = {
        path for values in (
            capture_inventory.get("capture_refs", []),
            [capture_inventory.get("state_ref"), capture_inventory.get("summary_ref"), capture_inventory.get("graph_ref")],
        ) for path in values if path and (root / path).exists()
    }
    inventory_check = validate_freshness_capture_inventory(
        capture_inventory, inventory_available, inventory_expected,
    )
    checks = {
        "bundle": bundle_check.valid,
        "result": result_check.valid,
        "content": content_check.valid,
        "freshness": (
            freshness_check.valid and capture_schema_check.valid
            and failure_evidence_check.valid and dependency_check.valid
            and graph_failure_evidence_check.valid
            and diagnostic_snapshot_check.valid
            and snapshot_capture_check.valid
            and graph_check.valid
            and graph_capture_check.valid
            and capture_summary_check.valid
            and summary_capture_check.valid
            and inventory_check.valid
        ),
    }
    passed = all(checks.values())
    output = {"audit_id": audit["audit_id"], "checks": checks,
              "error_code": None if passed else AUDIT_GATE_FAILED,
              "result": "passed" if passed else "failed"}
    if not passed:
        failed_reasons = [
            assessment.reason for assessment in (
                bundle_check, result_check, content_check,
                freshness_check, capture_schema_check,
                failure_evidence_check, dependency_check,
                graph_failure_evidence_check,
                diagnostic_snapshot_check,
                snapshot_capture_check,
                graph_check,
                graph_capture_check,
                capture_summary_check,
                summary_capture_check,
                inventory_check,
            ) if not assessment.valid
        ]
        output["reason"] = "; ".join(failed_reasons)
    emitted = _emit(output)
    return 0 if passed and emitted else 1


def main(root: Path = ROOT) -> int:
    try:
        return _run(root)
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        _emit({"error_code": MALFORMED_EVIDENCE,
               "result": "failed", "reason": str(error)})
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    sys.exit(main(parser.parse_args().root.resolve()))
