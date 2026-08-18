#!/usr/bin/env python3
"""Compose Hermes' deterministic pre-merge review gates."""
from dataclasses import dataclass
import argparse
import json
from pathlib import Path
from datetime import datetime

from scripts.bind_evidence import verify_attestation
from scripts.change_review import review_paths
from scripts.evidence_review import review_evidence
from scripts.dependency_review import review_dependencies


@dataclass(frozen=True)
class ChangeReview:
    scope_ok: bool
    evidence_ok: bool
    attestation_ok: bool
    escalation_ok: bool
    dependency_ok: bool

    @property
    def accepted(self) -> bool:
        return (
            self.scope_ok and self.evidence_ok and self.attestation_ok
            and self.escalation_ok and self.dependency_ok
        )


def valid_escalation(escalation: dict | None, attestation: dict) -> bool:
    if not escalation:
        return False
    required = (
        "reviewer", "decision", "rationale", "timestamp",
        "revision", "diff_sha256", "criteria_sha256",
    )
    if any(not escalation.get(field) for field in required):
        return False
    if escalation["decision"] != "accept":
        return False
    for field in ("revision", "diff_sha256", "criteria_sha256"):
        if escalation[field] != attestation.get(field):
            return False
    try:
        datetime.fromisoformat(escalation["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def review_change(record: dict) -> ChangeReview:
    paths = review_paths(
        record["paths"], tuple(record["allowed_prefixes"]),
    )
    evidence = review_evidence(record["evidence"])
    attestation_ok = verify_attestation(
        record["attestation"], record["diff"], record["acceptance_criteria"],
    )
    escalation_ok = not paths.sensitive or (
        attestation_ok
        and valid_escalation(record.get("escalation"), record["attestation"])
    )
    dependency = record.get("dependency")
    dependency_ok = True
    if dependency is not None:
        dependency_result = review_dependencies(
            dependency.get("paths", []), dependency.get("packages", {}),
        )
        dependency_ok = dependency_result.accepted
    return ChangeReview(
        scope_ok=not paths.out_of_scope,
        evidence_ok=evidence.accepted,
        attestation_ok=attestation_ok,
        escalation_ok=escalation_ok,
        dependency_ok=dependency_ok,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    result = review_change(json.loads(args.record.read_text()))
    print(json.dumps({
        "accepted": result.accepted,
        "scope_ok": result.scope_ok,
        "evidence_ok": result.evidence_ok,
        "attestation_ok": result.attestation_ok,
        "escalation_ok": result.escalation_ok,
        "dependency_ok": result.dependency_ok,
    }, indent=2))


if __name__ == "__main__":
    main()
