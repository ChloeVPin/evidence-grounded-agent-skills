import unittest

from scripts.generate_record import generate_record
from scripts.maintenance_review import revalidate


REVISION = "a" * 40


def evidence():
    return {
        "command": "python3 -m unittest",
        "revision": REVISION,
        "exit_status": 0,
        "output_sha256": "b" * 64,
        "acceptance_criteria": ["revalidation works"],
        "tests": [
            {"name": "focused", "kind": "focused", "status": "passed"},
            {"name": "boundary", "kind": "boundary", "status": "passed"},
        ],
    }


def record():
    return generate_record(
        revision=REVISION, paths=["skills/example/SKILL.md"],
        allowed_prefixes=["skills/"], criteria=["revalidation works"],
        diff="revalidation-diff", evidence=evidence(),
    )


class MaintenanceReviewTest(unittest.TestCase):
    def test_valid_attested_revalidation_returns_validated(self):
        result = revalidate("trusted", "review_due", record())
        self.assertTrue(result.allowed)
        self.assertEqual(result.state, "validated")

    def test_tampered_revalidation_cannot_restore_trust(self):
        review = record()
        review["diff"] = "tampered"
        result = revalidate("trusted", "review_due", review)
        self.assertFalse(result.allowed)
        self.assertEqual(result.state, "experimental")

    def test_fresh_artifact_does_not_need_revalidation(self):
        result = revalidate("trusted", "fresh", record())
        self.assertTrue(result.allowed)
        self.assertEqual(result.state, "trusted")


if __name__ == "__main__":
    unittest.main()
