#!/usr/bin/env python3
"""Run one declared command and capture verifiable execution metadata."""
from dataclasses import asdict, dataclass
import argparse
import hashlib
from pathlib import Path
import shlex
import subprocess
import sys


@dataclass(frozen=True)
class Evidence:
    command: str
    revision: str
    exit_status: int
    output_sha256: str


def capture(command: str, root: Path) -> Evidence:
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    result = subprocess.run(
        shlex.split(command), cwd=root, capture_output=True, text=True,
    )
    output = result.stdout + result.stderr
    digest = hashlib.sha256(output.encode()).hexdigest()
    return Evidence(command, revision, result.returncode, digest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="one executable command, parsed without a shell")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    evidence = capture(args.command, args.root.resolve())
    import json
    print(json.dumps(asdict(evidence), indent=2))
    return evidence.exit_status


if __name__ == "__main__":
    sys.exit(main())
