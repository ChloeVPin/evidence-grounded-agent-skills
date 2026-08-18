#!/usr/bin/env python3
"""Small least-privilege policy evaluator for tool-call fixtures."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolPolicy:
    allowed_actions: frozenset[str]
    resource_prefixes: tuple[str, ...]
    parameter_names: frozenset[str]


@dataclass(frozen=True)
class Authorization:
    allowed: bool
    reason: str


def authorize(
    policy: ToolPolicy, *, action: str, resource: str,
    parameters: dict, approval: bool = False,
) -> Authorization:
    if "*" in policy.allowed_actions or "*" in policy.resource_prefixes:
        return Authorization(False, "wildcard authority is forbidden")
    if action not in policy.allowed_actions:
        return Authorization(False, "action is not authorized")
    if not any(resource.startswith(prefix) for prefix in policy.resource_prefixes):
        return Authorization(False, "resource is outside scope")
    if not set(parameters).issubset(policy.parameter_names):
        return Authorization(False, "undeclared parameter")
    if action in {"write", "delete", "execute"} and not approval:
        return Authorization(False, "explicit approval required")
    return Authorization(True, "authorized by least-privilege policy")
