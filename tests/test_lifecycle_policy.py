import unittest

from scripts.lifecycle_policy import decide_lifecycle


class LifecyclePolicyTest(unittest.TestCase):
    def test_fresh_trusted_artifact_remains_trusted(self):
        result = decide_lifecycle(current_state="trusted", freshness="fresh")
        self.assertTrue(result.allowed)
        self.assertEqual(result.state, "trusted")

    def test_review_due_artifact_is_suspended_without_evidence(self):
        result = decide_lifecycle(current_state="trusted", freshness="review_due")
        self.assertFalse(result.allowed)
        self.assertEqual(result.state, "experimental")

    def test_review_due_artifact_can_revalidate(self):
        result = decide_lifecycle(
            current_state="trusted", freshness="review_due", revalidation_evidence=True,
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.state, "validated")

    def test_deprecated_and_unknown_cannot_be_trusted(self):
        for freshness in ("deprecated", "superseded", "unknown"):
            self.assertFalse(decide_lifecycle(current_state="trusted", freshness=freshness).allowed)


if __name__ == "__main__":
    unittest.main()
