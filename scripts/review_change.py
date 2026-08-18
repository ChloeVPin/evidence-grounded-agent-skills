#!/usr/bin/env python3
"""Compose Hermes' deterministic pre-merge review gates."""
from dataclasses import dataclass
import argparse
import json
from pathlib import Path

from scripts.bind_evidence import verify_attestation
from scripts.change_review import review_paths
from scripts.evidence_review import review_evidence


@dataclass(frozen=True)
class ChangeReview:
    scope_ok: bool
    evidence_ok: bool
    attestation_ok: bool

    @property
    def accepted(self) -> bool:
        return self.scope_ok and self.evidence_ok and self.attestation_ok


def review_change(record: dict) -> ChangeReview:
    paths = review_paths(
        record["paths"], tuple(record["allowed_prefixes"]),
    )
    evidence = review_evidence(record["evidence"])
    attestation_ok = verify_attestation(
        record["attestation"], record["diff"], record["acceptance_criteria"],
    )
    return ChangeReview(
        scope_ok=not paths.out_of_scope and not paths.sensitive,
        evidence_ok=evidence.accepted,
        attestation_ok=attestation_ok,
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
    }, indent=2))


if __name__ == "__main__":
    main()
