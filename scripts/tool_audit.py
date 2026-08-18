#!/usr/bin/env python3
"""Build and validate redacted audit records for tool authorization and calls."""
from dataclasses import asdict, dataclass
from datetime import datetime
import hashlib

SECRET_KEYS = {"token", "password", "secret", "api_key", "authorization"}


def redact(value):
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.lower() in SECRET_KEYS else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


@dataclass(frozen=True)
class ToolAudit:
    caller: str
    tool: str
    action: str
    resource: str
    parameters: dict
    decision: str
    approval: bool
    timestamp: str
    output_sha256: str


def build_audit(
    *, caller: str, tool: str, action: str, resource: str,
    parameters: dict, decision: str, approval: bool,
    timestamp: str, output: str,
) -> ToolAudit:
    if not all((caller, tool, action, resource, decision, timestamp)):
        raise ValueError("audit identity and decision fields are required")
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("invalid audit timestamp")
    return ToolAudit(
        caller, tool, action, resource, redact(parameters), decision,
        approval, timestamp, hashlib.sha256(output.encode()).hexdigest(),
    )


def validate_audit(audit: dict) -> tuple[str, ...]:
    required = (
        "caller", "tool", "action", "resource", "parameters", "decision",
        "approval", "timestamp", "output_sha256",
    )
    return tuple(f"missing:{field}" for field in required if field not in audit)
