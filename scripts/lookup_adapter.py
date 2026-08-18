#!/usr/bin/env python3
"""Normalize external dependency lookup output without inventing certainty."""
from dataclasses import asdict, dataclass
import hashlib
import json


@dataclass(frozen=True)
class LookupEvidence:
    source: str
    looked_up_at: str
    status: str
    raw_output_sha256: str
    reason: str


def normalize_lookup(raw: dict | None, *, source: str, looked_up_at: str) -> LookupEvidence:
    serialized = json.dumps(raw, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(serialized.encode()).hexdigest()
    if not source or not looked_up_at:
        return LookupEvidence(source, looked_up_at, "unknown", digest, "missing provenance")
    if raw is None:
        return LookupEvidence(source, looked_up_at, "unknown", digest, "lookup unavailable")
    if not isinstance(raw.get("registry_resolved"), bool) or not isinstance(raw.get("advisories"), list):
        return LookupEvidence(source, looked_up_at, "unknown", digest, "malformed lookup response")
    if raw["advisories"]:
        return LookupEvidence(source, looked_up_at, "vulnerable", digest, "advisory reported")
    if raw["registry_resolved"]:
        return LookupEvidence(source, looked_up_at, "verified", digest, "registry resolved without advisory")
    return LookupEvidence(source, looked_up_at, "unknown", digest, "registry did not resolve package")


def as_record(raw: dict | None, *, source: str, looked_up_at: str) -> dict:
    return asdict(normalize_lookup(raw, source=source, looked_up_at=looked_up_at))
