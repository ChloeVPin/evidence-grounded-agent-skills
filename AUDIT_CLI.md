# Current assertion audit CLI

Run the complete current-head audit from the repository root:

```bash
python3 scripts/audit_current_assertion.py
```

Success exits with status `0` and emits JSON containing `audit_id`, `checks`,
`error_code: null`, and `result: "passed"`. A failed audit exits with status
`1` and emits `result: "failed"`.

Stable failure codes:

- `NO_CURRENT_ASSERTION`: no valid current assertion head was discovered.
- `MALFORMED_EVIDENCE`: evidence JSON, required fields, or filesystem inputs
  could not be read or validated.
- `AUDIT_GATE_FAILED`: the bundle, fresh-result, or content-digest check failed.

The optional `--root PATH` argument audits another repository-shaped evidence
root. Human-readable `reason` text may change; consumers should branch on the
stable `error_code` and process exit status.
