#!/usr/bin/env python3
"""Compose tool authorization with mandatory redacted audit recording."""
from dataclasses import asdict
import hashlib

from scripts.tool_audit import build_audit
from scripts.tool_policy import ToolPolicy, authorize


def authorize_and_audit(
    policy: ToolPolicy, *, caller: str, tool: str, action: str,
    resource: str, parameters: dict, approval: bool, timestamp: str,
    output: str,
) -> tuple[object, dict]:
    decision = authorize(
        policy, action=action, resource=resource,
        parameters=parameters, approval=approval,
    )
    audit = build_audit(
        caller=caller, tool=tool, action=action, resource=resource,
        parameters=parameters, decision="allow" if decision.allowed else "deny",
        approval=approval, timestamp=timestamp, output=output,
    )
    return decision, asdict(audit)


def verify_output(audit: dict, output: str) -> bool:
    return audit.get("output_sha256") == hashlib.sha256(output.encode()).hexdigest()
