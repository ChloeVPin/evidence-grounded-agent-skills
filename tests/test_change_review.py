import unittest

from scripts.change_review import review_paths


class ChangeReviewBehaviorTest(unittest.TestCase):
    def test_allowed_change_is_not_escalated(self):
        result = review_paths(
            ["skills/repository-change-verification/SKILL.md"],
            ("skills/",),
        )
        self.assertTrue(result.accepted)
        self.assertEqual(result.out_of_scope, ())
        self.assertEqual(result.sensitive, ())

    def test_unrelated_change_is_flagged(self):
        result = review_paths(
            ["skills/example/SKILL.md", "README.md"],
            ("skills/",),
        )
        self.assertEqual(result.out_of_scope, ("README.md",))
        self.assertFalse(result.accepted)

    def test_sensitive_automation_change_is_escalated(self):
        result = review_paths(
            ["skills/example/SKILL.md", ".github/workflows/ci.yml"],
            ("skills/", ".github/workflows/"),
        )
        self.assertEqual(result.out_of_scope, ())
        self.assertEqual(result.sensitive, (".github/workflows/ci.yml",))
        self.assertFalse(result.accepted)


if __name__ == "__main__":
    unittest.main()
