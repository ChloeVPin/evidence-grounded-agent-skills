import unittest

from scripts.tool_call_review import authorize_and_audit, verify_output
from scripts.tool_policy import ToolPolicy


READ = ToolPolicy(frozenset({"read"}), ("repo/docs/",), frozenset({"path"}))
WRITE = ToolPolicy(frozenset({"write"}), ("repo/docs/",), frozenset({"path", "content"}))


class ToolCallReviewTest(unittest.TestCase):
    def test_allowed_call_is_audited(self):
        decision, audit = authorize_and_audit(
            READ, caller="agent-1", tool="repo.read", action="read",
            resource="repo/docs/a.md", parameters={"path": "a.md"}, approval=False,
            timestamp="2026-08-18T12:00:00Z", output="contents",
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(audit["decision"], "allow")
        self.assertTrue(verify_output(audit, "contents"))

    def test_denied_call_is_also_audited(self):
        decision, audit = authorize_and_audit(
            WRITE, caller="agent-1", tool="repo.write", action="write",
            resource="repo/docs/a.md", parameters={"path": "a.md", "content": "x"}, approval=False,
            timestamp="2026-08-18T12:00:00Z", output="denied",
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(audit["decision"], "deny")

    def test_tampered_output_fails_digest_check(self):
        _, audit = authorize_and_audit(
            READ, caller="agent-1", tool="repo.read", action="read",
            resource="repo/docs/a.md", parameters={"path": "a.md"}, approval=False,
            timestamp="2026-08-18T12:00:00Z", output="contents",
        )
        self.assertFalse(verify_output(audit, "tampered"))


if __name__ == "__main__":
    unittest.main()
