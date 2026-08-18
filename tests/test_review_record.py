import unittest

from scripts.review_record import validate_record


def valid_record():
    revision = "a" * 40
    return {
        "schema_version": 1,
        "revision": revision,
        "paths": ["skills/example/SKILL.md"],
        "allowed_prefixes": ["skills/"],
        "acceptance_criteria": ["behavior works"],
        "diff": "diff",
        "evidence": {"tests": []},
        "attestation": {"revision": revision},
    }


class ReviewRecordTest(unittest.TestCase):
    def test_versioned_complete_record_is_valid(self):
        self.assertEqual(validate_record(valid_record()), ())

    def test_missing_revision_is_rejected(self):
        record = valid_record()
        del record["revision"]
        self.assertIn("missing:revision", validate_record(record))

    def test_attestation_for_different_revision_is_rejected(self):
        record = valid_record()
        record["attestation"]["revision"] = "b" * 40
        self.assertIn("revision_mismatch", validate_record(record))


if __name__ == "__main__":
    unittest.main()
