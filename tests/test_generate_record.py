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

    def test_dependency_metadata_is_serialized_when_evidence_is_valid(self):
        dependency = {
            "paths": ["requirements.txt"],
            "packages": {"safe-lib": {"provenance_verified": True, "known_vulnerable": False}},
            "evidence": {"safe-lib": {
                "source": "https://registry.example/safe-lib",
                "looked_up_at": "2026-08-18T12:00:00Z",
                "status": "verified",
            }},
        }
        record = generate_record(
            revision=REVISION, paths=["requirements.txt"],
            allowed_prefixes=["."], criteria=["behavior works"],
            diff="diff", evidence=evidence(), dependency=dependency,
        )
        self.assertEqual(record["dependency"], dependency)

    def test_dependency_metadata_without_provenance_is_rejected(self):
        dependency = {
            "paths": ["requirements.txt"],
            "packages": {"safe-lib": {}}, "evidence": {},
        }
        with self.assertRaisesRegex(ValueError, "invalid dependency evidence"):
            generate_record(
                revision=REVISION, paths=["requirements.txt"],
                allowed_prefixes=["."], criteria=["behavior works"],
                diff="diff", evidence=evidence(), dependency=dependency,
            )


if __name__ == "__main__":
    unittest.main()
