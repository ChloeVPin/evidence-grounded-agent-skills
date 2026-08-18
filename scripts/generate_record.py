#!/usr/bin/env python3
"""Generate a complete review record from captured evidence and change inputs."""
import argparse
import json
from pathlib import Path

from scripts.bind_evidence import create_attestation
from scripts.evidence_review import review_evidence
from scripts.review_record import validate_record
from scripts.dependency_evidence import validate_dependency_evidence


def generate_record(
    *, revision: str, paths: list[str], allowed_prefixes: list[str],
    criteria: list[str], diff: str, evidence: dict,
    dependency: dict | None = None,
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
    if dependency is not None:
        dependency_errors = validate_dependency_evidence(
            dependency.get("evidence", {}), dependency.get("packages", {}),
        )
        if dependency_errors:
            raise ValueError(f"invalid dependency evidence: {dependency_errors}")
        record["dependency"] = dependency
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
    parser.add_argument("--dependency-file", type=Path)
    args = parser.parse_args()
    dependency = json.loads(args.dependency_file.read_text()) if args.dependency_file else None
    record = generate_record(
        revision=args.revision, paths=args.path, allowed_prefixes=args.allowed,
        criteria=args.criteria, diff=args.diff_file.read_text(),
        evidence=json.loads(args.evidence_file.read_text()), dependency=dependency,
    )
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
