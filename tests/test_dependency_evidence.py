import unittest

from scripts.dependency_evidence import validate_dependency_evidence


class DependencyEvidenceTest(unittest.TestCase):
    def test_complete_verified_evidence_is_valid(self):
        errors = validate_dependency_evidence(
            {"safe-lib": {
                "source": "https://registry.example/safe-lib",
                "looked_up_at": "2026-08-18T12:00:00Z",
                "status": "verified",
            }},
            {"safe-lib": {}},
        )
        self.assertEqual(errors, ())

    def test_missing_source_is_rejected(self):
        errors = validate_dependency_evidence(
            {"safe-lib": {"looked_up_at": "2026-08-18T12:00:00Z", "status": "unknown"}},
            {"safe-lib": {}},
        )
        self.assertIn("source:safe-lib", errors)

    def test_unknown_status_is_explicit_but_not_missing(self):
        errors = validate_dependency_evidence(
            {"safe-lib": {
                "source": "https://registry.example/safe-lib",
                "looked_up_at": "2026-08-18T12:00:00Z",
                "status": "unknown",
            }},
            {"safe-lib": {}},
        )
        self.assertEqual(errors, ())


if __name__ == "__main__":
    unittest.main()
