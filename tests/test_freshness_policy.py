import unittest
from datetime import datetime, timezone

from scripts.freshness_policy import assess_artifact


NOW = datetime(2026, 8, 18, tzinfo=timezone.utc)


class FreshnessPolicyTest(unittest.TestCase):
    def test_recent_trusted_artifact_is_fresh(self):
        result = assess_artifact(
            state="trusted", last_validated="2026-08-01T00:00:00Z",
            now=NOW, review_window_days=90,
        )
        self.assertEqual(result.outcome, "fresh")

    def test_old_artifact_is_review_due(self):
        result = assess_artifact(
            state="validated", last_validated="2025-01-01T00:00:00Z",
            now=NOW, review_window_days=90,
        )
        self.assertEqual(result.outcome, "review_due")

    def test_deprecated_and_superseded_are_distinct(self):
        self.assertEqual(assess_artifact(state="deprecated", last_validated=None, now=NOW, review_window_days=90).outcome, "deprecated")
        self.assertEqual(assess_artifact(state="superseded", last_validated=None, now=NOW, review_window_days=90).outcome, "superseded")

    def test_missing_date_is_unknown(self):
        result = assess_artifact(state="trusted", last_validated=None, now=NOW, review_window_days=90)
        self.assertEqual(result.outcome, "unknown")


if __name__ == "__main__":
    unittest.main()
