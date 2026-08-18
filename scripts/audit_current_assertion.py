#!/usr/bin/env python3
"""Run the complete current policy-assertion audit as one command."""
import json
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.decision_ledger import (
    compare_policy_audit,
    discover_current_assertion,
    validate_current_assertion_bundle,
    validate_policy_assertion_content,
)


def main(root: Path = ROOT) -> int:
    evidence_dir = root / "ledger" / "evidence"
    assertions = [
        json.loads(path.read_text())
        for path in sorted(evidence_dir.glob("*-generation-policy-audit.json"))
    ]
    head = discover_current_assertion(assertions)
    if not head.valid:
        print(json.dumps({"result": "failed", "reason": head.reason}))
        return 1
    audit = head.assertion
    bundle_path = evidence_dir / f"{audit['audit_id'][:4]}-current-assertion-bundle.json"
    bundle = json.loads(bundle_path.read_text())
    available = set(audit["evidence_refs"]) | {
        bundle["assertion_ref"], bundle["content_digest_ref"],
    }
    bundle_check = validate_current_assertion_bundle(bundle, available)
    capture = json.loads((root / bundle["capture_ref"]).read_text())
    result_check = compare_policy_audit(audit, capture)
    digests = json.loads((root / bundle["content_digest_ref"]).read_text())
    content_check = validate_policy_assertion_content(audit, digests)
    checks = {
        "bundle": bundle_check.valid,
        "result": result_check.valid,
        "content": content_check.valid,
    }
    passed = all(checks.values())
    print(json.dumps({"audit_id": audit["audit_id"], "checks": checks,
                      "result": "passed" if passed else "failed"}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    sys.exit(main(parser.parse_args().root.resolve()))
