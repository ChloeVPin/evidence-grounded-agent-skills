#!/usr/bin/env python3
"""Small, deterministic pre-review gate for changed repository paths."""
from dataclasses import dataclass
import argparse
import json

SENSITIVE_PATTERNS = (
    ".github/workflows/",
    "Dockerfile",
    "docker-compose",
    "package.json",
    "pyproject.toml",
    "setup.py",
    "Makefile",
    "Taskfile",
    "Gemfile",
    "go.mod",
)


@dataclass(frozen=True)
class Review:
    out_of_scope: tuple[str, ...]
    sensitive: tuple[str, ...]

    @property
    def accepted(self) -> bool:
        return not self.out_of_scope and not self.sensitive


def review_paths(paths: list[str], allowed_prefixes: tuple[str, ...]) -> Review:
    out_of_scope = tuple(sorted(
        path for path in paths
        if not any(prefix == "." or path == prefix or path.startswith(prefix.rstrip("/") + "/")
                   for prefix in allowed_prefixes)
    ))
    sensitive = tuple(sorted(
        path for path in paths
        if any(pattern in path for pattern in SENSITIVE_PATTERNS)
    ))
    return Review(out_of_scope=out_of_scope, sensitive=sensitive)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allowed", action="append", required=True,
                        help="allowed path prefix; repeat for multiple prefixes")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    result = review_paths(args.paths, tuple(args.allowed))
    print(json.dumps({
        "accepted_without_escalation": result.accepted,
        "out_of_scope": result.out_of_scope,
        "sensitive": result.sensitive,
    }, indent=2))


if __name__ == "__main__":
    main()
