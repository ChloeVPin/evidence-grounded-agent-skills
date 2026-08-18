#!/usr/bin/env python3
"""Validate the versioned, repository-native shape of a review record."""
import argparse
import json
from pathlib import Path
import re

SCHEMA_VERSION = 1
REQUIRED = (
    "schema_version", "revision", "paths", "allowed_prefixes",
    "acceptance_criteria", "diff", "evidence", "attestation",
)


def validate_record(record: dict) -> tuple[str, ...]:
    errors = [field for field in REQUIRED if field not in record]
    if errors:
        return tuple(f"missing:{field}" for field in errors)
    if record["schema_version"] != SCHEMA_VERSION:
        errors.append("schema_version")
    if not isinstance(record["revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", record["revision"]):
        errors.append("revision")
    for field in ("paths", "allowed_prefixes", "acceptance_criteria"):
        if not isinstance(record[field], list) or not record[field]:
            errors.append(field)
    if not isinstance(record["evidence"], dict) or not isinstance(record["attestation"], dict):
        errors.append("evidence_or_attestation")
    elif record["attestation"].get("revision") != record["revision"]:
        errors.append("revision_mismatch")
    return tuple(errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = validate_record(json.loads(args.record.read_text()))
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
