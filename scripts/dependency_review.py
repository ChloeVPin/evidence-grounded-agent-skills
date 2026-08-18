#!/usr/bin/env python3
"""Deterministic policy checks for dependency and supply-chain changes."""
from dataclasses import dataclass

DEPENDENCY_FILES = (
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "pyproject.toml", "poetry.lock", "requirements.txt", "go.mod", "go.sum",
    "Cargo.toml", "Cargo.lock", "Gemfile", "Gemfile.lock",
)
EXECUTION_PATHS = (
    ".github/workflows/", "Dockerfile", "docker-compose", "Makefile",
    "package.json", "pyproject.toml", "setup.py",
)


@dataclass(frozen=True)
class DependencyReview:
    dependency_files: tuple[str, ...]
    unverified: tuple[str, ...]
    vulnerable: tuple[str, ...]
    execution_paths: tuple[str, ...]

    @property
    def accepted(self) -> bool:
        return not self.unverified and not self.vulnerable and not self.execution_paths


def _matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(path == pattern or path.endswith("/" + pattern) or pattern in path for pattern in patterns)


def review_dependencies(
    paths: list[str], packages: dict[str, dict],
) -> DependencyReview:
    dependency_files = tuple(sorted(path for path in paths if _matches(path, DEPENDENCY_FILES)))
    execution_paths = tuple(sorted(path for path in paths if _matches(path, EXECUTION_PATHS)))
    unverified = tuple(sorted(name for name, data in packages.items() if not data.get("provenance_verified", False)))
    vulnerable = tuple(sorted(name for name, data in packages.items() if data.get("known_vulnerable", False)))
    return DependencyReview(dependency_files, unverified, vulnerable, execution_paths)
