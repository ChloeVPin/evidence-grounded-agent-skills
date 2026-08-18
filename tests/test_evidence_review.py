import unittest

from scripts.evidence_review import review_evidence


class EvidenceReviewBehaviorTest(unittest.TestCase):
    def test_complete_evidence_is_accepted(self):
        result = review_evidence({
            "acceptance_criteria": ["reject unrelated files"],
            "tests": [
                {"name": "focused scope test", "kind": "focused", "status": "passed"},
                {"name": "unrelated file test", "kind": "boundary", "status": "passed"},
            ],
        })
        self.assertTrue(result.accepted)

    def test_missing_boundary_evidence_is_rejected(self):
        result = review_evidence({
            "acceptance_criteria": ["change behaves as requested"],
            "tests": [{"name": "happy path", "kind": "focused", "status": "passed"}],
        })
        self.assertEqual(result.missing, ("boundary_or_regression_test",))
        self.assertFalse(result.accepted)

    def test_failed_test_is_rejected(self):
        result = review_evidence({
            "acceptance_criteria": ["change behaves as requested"],
            "tests": [{"name": "regression", "kind": "regression", "status": "failed"}],
        })
        self.assertEqual(result.failed, ("regression",))
        self.assertFalse(result.accepted)
