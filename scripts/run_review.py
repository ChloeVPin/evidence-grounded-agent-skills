#!/usr/bin/env python3
"""Capture and review the current repository revision as one transient artifact."""
from dataclasses import asdict
import argparse
import json
from pathlib import Path
import subprocess

from scripts.capture_evidence import capture
from scripts.generate_record import generate_record
from scripts.review_change import review_change


def current_diff(root: Path) -> tuple[str, list[str]]:
    diff = subprocess.run(
        ["git", "diff", "HEAD^..HEAD"], cwd=root, check=True,
        capture_output=True, text=True,
    ).stdout
    names = subprocess.run(
        ["git", "diff", "--name-only", "HEAD^..HEAD"], cwd=root, check=True,
        capture_output=True, text=True,
    ).stdout.splitlines()
    return diff, names


def run_review(root: Path, command: str) -> tuple[dict, object]:
    evidence = asdict(capture(command, root))
    evidence["acceptance_criteria"] = ["repository checks pass for current revision"]
    evidence["tests"] = [{
        "name": command, "kind": "regression",
        "status": "passed" if evidence["exit_status"] == 0 else "failed",
    }]
    diff, paths = current_diff(root)
    record = generate_record(
        revision=evidence["revision"], paths=paths or ["."],
        allowed_prefixes=["."], criteria=evidence["acceptance_criteria"],
        diff=diff, evidence=evidence,
    )
    return record, review_change(record)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--command", default="python3 -m unittest discover -s tests -v")
    args = parser.parse_args()
    record, result = run_review(args.root.resolve(), args.command)
    print(json.dumps({"record": record, "decision": {
        "accepted": result.accepted,
        "scope_ok": result.scope_ok,
        "evidence_ok": result.evidence_ok,
        "attestation_ok": result.attestation_ok,
        "escalation_ok": result.escalation_ok,
    }}, indent=2))
    return 0 if result.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
