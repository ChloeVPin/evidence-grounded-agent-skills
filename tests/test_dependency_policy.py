import unittest
from datetime import datetime, timezone

from scripts.dependency_policy import assess_dependency_evidence


NOW = datetime(2026, 8, 18, tzinfo=timezone.utc)


class DependencyPolicyTest(unittest.TestCase):
    def item(self, status, looked_up_at="2026-08-01T00:00:00Z"):
        return {"status": status, "looked_up_at": looked_up_at}

    def test_fresh_verified_evidence_passes(self):
        self.assertEqual(assess_dependency_evidence(self.item("verified"), now=NOW).outcome, "pass")

    def test_unknown_evidence_requires_escalation(self):
        result = assess_dependency_evidence(self.item("unknown"), now=NOW)
        self.assertEqual(result.outcome, "escalate")

    def test_vulnerable_evidence_blocks(self):
        result = assess_dependency_evidence(self.item("vulnerable"), now=NOW)
        self.assertEqual(result.outcome, "block")

    def test_stale_verified_evidence_requires_escalation(self):
        result = assess_dependency_evidence(
            self.item("verified", "2025-01-01T00:00:00Z"), now=NOW,
        )
        self.assertEqual(result.outcome, "escalate")


if __name__ == "__main__":
    unittest.main()
