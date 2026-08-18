#!/usr/bin/env python3
"""Bind captured execution evidence to a diff and acceptance criteria."""
from dataclasses import asdict, dataclass
import argparse
import hashlib
import json
from pathlib import Path


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def criteria_digest(criteria: list[str]) -> str:
    normalized = json.dumps(sorted(criteria), separators=(",", ":"))
    return digest(normalized)


@dataclass(frozen=True)
class Attestation:
    revision: str
    output_sha256: str
    diff_sha256: str
    criteria_sha256: str


def create_attestation(diff: str, criteria: list[str], evidence: dict) -> Attestation:
    return Attestation(
        revision=evidence["revision"],
        output_sha256=evidence["output_sha256"],
        diff_sha256=digest(diff),
        criteria_sha256=criteria_digest(criteria),
    )


def verify_attestation(attestation: dict, diff: str, criteria: list[str]) -> bool:
    return (
        attestation.get("diff_sha256") == digest(diff)
        and attestation.get("criteria_sha256") == criteria_digest(criteria)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diff-file", type=Path, required=True)
    parser.add_argument("--criteria", action="append", required=True)
    parser.add_argument("--evidence-file", type=Path, required=True)
    args = parser.parse_args()
    evidence = json.loads(args.evidence_file.read_text())
    print(json.dumps(asdict(create_attestation(
        args.diff_file.read_text(), args.criteria, evidence,
    )), indent=2))


if __name__ == "__main__":
    main()
