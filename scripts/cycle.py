#!/usr/bin/env python3
"""Create a dated, explicitly incomplete research-cycle record."""
from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CYCLES = ROOT / "ledger" / "cycles"

def main():
    parser = ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--question")
    args = parser.parse_args()
    files = sorted(CYCLES.glob("*.md"))
    if args.list:
        for path in files:
            print(path.relative_to(ROOT))
        return
    if not args.start or not args.question:
        parser.error("use --list or --start --question '...'")
    numbers = [int(m.group(1)) for p in files if (m := re.match(r"(\d+)-", p.name))]
    number = max(numbers, default=0) + 1
    slug = re.sub(r"[^a-z0-9]+", "-", args.question.lower()).strip("-")[:60]
    path = CYCLES / f"{number:04d}-{slug}.md"
    path.write_text(f"""# Cycle {number:04d} — {args.question}\n\nDate: {date.today().isoformat()}\nStatus: in progress\n\n## Question\n\n{args.question}\n\n## Decision\n\n_To be determined from evidence._\n\n## Evidence and provenance\n\n_To be recorded. Primary sources required._\n\n## Disconfirming evidence sought\n\n_To be recorded._\n\n## Next action\n\n_Research, validate, and update this record._\n""")
    print(path.relative_to(ROOT))

if __name__ == "__main__":
    main()
