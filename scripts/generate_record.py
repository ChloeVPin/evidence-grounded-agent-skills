#!/usr/bin/env python3
"""Generate a complete review record from captured evidence and change inputs."""
import argparse
import json
from pathlib import Path

from scripts.bind_evidence import create_attestation
from scripts.evidence_review import review_evidence
from scripts.review_record import validate_record


def generate_record(
    *, revision: str, paths: list[str], allowed_prefixes: list[str],
    criteria: list[str], diff: str, evidence: dict,
) -> dict:
    if evidence.get("revision") != revision:
        raise ValueError("capture revision does not match requested revision")
    evidence_result = review_evidence(evidence)
    if not evidence_result.accepted:
        raise ValueError(f"incomplete evidence: {evidence_result.missing + evidence_result.failed}")
    record = {
        "schema_version": 1,
        "revision": revision,
        "paths": paths,
        "allowed_prefixes": allowed_prefixes,
        "acceptance_criteria": criteria,
        "diff": diff,
        "evidence": evidence,
    }
    record["attestation"] = create_attestation(diff, criteria, evidence).__dict__
    errors = validate_record(record)
    if errors:
        raise ValueError(f"invalid generated record: {errors}")
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", required=True)
    parser.add_argument("--path", action="append", required=True)
    parser.add_argument("--allowed", action="append", required=True)
    parser.add_argument("--criteria", action="append", required=True)
    parser.add_argument("--diff-file", type=Path, required=True)
    parser.add_argument("--evidence-file", type=Path, required=True)
    args = parser.parse_args()
    record = generate_record(
        revision=args.revision, paths=args.path, allowed_prefixes=args.allowed,
        criteria=args.criteria, diff=args.diff_file.read_text(),
        evidence=json.loads(args.evidence_file.read_text()),
    )
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
