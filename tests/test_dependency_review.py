import unittest

from scripts.dependency_review import review_dependencies


class DependencyReviewTest(unittest.TestCase):
    def test_verified_dependency_change_without_execution_path_is_clean(self):
        result = review_dependencies(
            ["requirements.txt"],
            {"safe-lib": {"provenance_verified": True, "known_vulnerable": False}},
        )
        self.assertEqual(result.dependency_files, ("requirements.txt",))
        self.assertTrue(result.accepted)

    def test_unverified_package_is_rejected(self):
        result = review_dependencies(
            ["package-lock.json"],
            {"unknown-lib": {"provenance_verified": False, "known_vulnerable": False}},
        )
        self.assertEqual(result.unverified, ("unknown-lib",))
        self.assertFalse(result.accepted)

    def test_known_vulnerability_is_rejected(self):
        result = review_dependencies(
            ["pyproject.toml"],
            {"old-lib": {"provenance_verified": True, "known_vulnerable": True}},
        )
        self.assertEqual(result.vulnerable, ("old-lib",))
        self.assertFalse(result.accepted)

    def test_execution_path_is_escalated(self):
        result = review_dependencies(
            [".github/workflows/ci.yml"],
            {},
        )
        self.assertEqual(result.execution_paths, (".github/workflows/ci.yml",))
        self.assertFalse(result.accepted)


if __name__ == "__main__":
    unittest.main()
