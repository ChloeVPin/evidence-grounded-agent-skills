import unittest

from scripts.tool_audit import build_audit, validate_audit


class ToolAuditTest(unittest.TestCase):
    def test_audit_binds_identity_decision_and_output_digest(self):
        audit = build_audit(
            caller="agent-1", tool="repo.read", action="read", resource="repo/docs/a.md",
            parameters={"path": "a.md"}, decision="allow", approval=False,
            timestamp="2026-08-18T12:00:00Z", output="file contents",
        )
        self.assertEqual(len(audit.output_sha256), 64)
        self.assertEqual(validate_audit(audit.__dict__), ())

    def test_secret_parameters_are_redacted_recursively(self):
        audit = build_audit(
            caller="agent-1", tool="repo.write", action="write", resource="repo/a",
            parameters={"token": "value", "nested": {"password": "hidden"}},
            decision="allow", approval=True, timestamp="2026-08-18T12:00:00Z", output="ok",
        )
        self.assertEqual(audit.parameters["token"], "[REDACTED]")
        self.assertEqual(audit.parameters["nested"]["password"], "[REDACTED]")

    def test_invalid_timestamp_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "timestamp"):
            build_audit(
                caller="agent-1", tool="repo.read", action="read", resource="repo/a",
                parameters={}, decision="deny", approval=False, timestamp="later", output="",
            )


if __name__ == "__main__":
    unittest.main()
