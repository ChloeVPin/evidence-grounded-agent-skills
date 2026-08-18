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

from scripts.decision_ledger import (
    compare_policy_audit,
    discover_current_assertion,
    validate_current_assertion_bundle,
    validate_policy_assertion_content,
    validate_self_validation_state,
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
    state_path = root / "ledger/state/0113-complete-self-validation-gate.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    freshness_check = validate_self_validation_state(
        state, "ledger/evidence/0108-self-validation-bundle.json", self_capture,
    )
    checks = {
        "bundle": bundle_check.valid,
        "result": result_check.valid,
        "content": content_check.valid,
        "freshness": freshness_check.valid,
    }
    passed = all(checks.values())
    output = {"audit_id": audit["audit_id"], "checks": checks,
              "error_code": None if passed else AUDIT_GATE_FAILED,
              "result": "passed" if passed else "failed"}
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
