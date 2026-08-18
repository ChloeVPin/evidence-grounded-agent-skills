#!/usr/bin/env python3
"""Check that a change review records minimum test evidence."""
from dataclasses import dataclass
import argparse
import json
from pathlib import Path


@dataclass(frozen=True)
class EvidenceReview:
    missing: tuple[str, ...]
    failed: tuple[str, ...]

    @property
    def accepted(self) -> bool:
        return not self.missing and not self.failed


def review_evidence(record: dict) -> EvidenceReview:
    missing: list[str] = []
    failed: list[str] = []
    criteria = record.get("acceptance_criteria", [])
    tests = record.get("tests", [])
    if not criteria:
        missing.append("acceptance_criteria")
    if not tests:
        missing.append("tests")
    if tests and not any(test.get("kind") in {"boundary", "regression"}
                        for test in tests):
        missing.append("boundary_or_regression_test")
    for test in tests:
        if test.get("status") != "passed":
            failed.append(test.get("name", "unnamed test"))
    return EvidenceReview(tuple(missing), tuple(failed))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    result = review_evidence(json.loads(args.record.read_text()))
    print(json.dumps({
        "accepted_evidence": result.accepted,
        "missing": result.missing,
        "failed": result.failed,
    }, indent=2))


if __name__ == "__main__":
    main()
