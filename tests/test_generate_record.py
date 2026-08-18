import unittest

from scripts.generate_record import generate_record
from scripts.review_record import validate_record
from scripts.review_change import review_change


REVISION = "a" * 40


def evidence():
    return {
        "command": "python3 -m unittest",
        "revision": REVISION,
        "exit_status": 0,
        "output_sha256": "b" * 64,
        "acceptance_criteria": ["behavior works"],
        "tests": [
            {"name": "focused", "kind": "focused", "status": "passed"},
            {"name": "boundary", "kind": "boundary", "status": "passed"},
        ],
    }


class GenerateRecordTest(unittest.TestCase):
    def test_complete_capture_generates_valid_record(self):
        record = generate_record(
            revision=REVISION, paths=["skills/example/SKILL.md"],
            allowed_prefixes=["skills/"], criteria=["behavior works"],
            diff="diff", evidence=evidence(),
        )
        self.assertEqual(validate_record(record), ())
        self.assertEqual(record["attestation"]["revision"], REVISION)
        result = review_change(record)
        self.assertTrue(result.accepted)
        self.assertTrue(result.dependency_ok)

    def test_mutated_generated_diff_is_rejected_by_complete_review(self):
        record = generate_record(
            revision=REVISION, paths=["skills/example/SKILL.md"],
            allowed_prefixes=["skills/"], criteria=["behavior works"],
            diff="diff", evidence=evidence(),
        )
        record["diff"] = "mutated diff"
        result = review_change(record)
        self.assertFalse(result.accepted)
        self.assertFalse(result.attestation_ok)

    def test_mismatched_capture_revision_is_rejected(self):
        captured = evidence()
        captured["revision"] = "c" * 40
        with self.assertRaisesRegex(ValueError, "capture revision"):
            generate_record(
                revision=REVISION, paths=["skills/example/SKILL.md"],
                allowed_prefixes=["skills/"], criteria=["behavior works"],
                diff="diff", evidence=captured,
            )

    def test_incomplete_capture_is_rejected(self):
        captured = evidence()
        captured["tests"] = [{"name": "happy path", "kind": "focused", "status": "passed"}]
        with self.assertRaisesRegex(ValueError, "incomplete evidence"):
            generate_record(
                revision=REVISION, paths=["skills/example/SKILL.md"],
                allowed_prefixes=["skills/"], criteria=["behavior works"],
                diff="diff", evidence=captured,
            )


if __name__ == "__main__":
    unittest.main()
