import unittest

from scripts.progress_record import assess_progress


class ProgressRecordTest(unittest.TestCase):
    def test_quality_gain_with_evidence_is_valid(self):
        result = assess_progress({
            "quality_delta": 1,
            "coverage_delta": 0,
            "evidence_quality_delta": 0,
            "validation_delta": 0,
            "uncertainty_delta": 0,
            "evidence": ["before and after test results"],
        })
        self.assertTrue(result.valid)

    def test_file_count_without_quality_gain_is_invalid(self):
        result = assess_progress({
            "quality_delta": 0,
            "coverage_delta": 0,
            "evidence_quality_delta": 0,
            "validation_delta": 0,
            "uncertainty_delta": 0,
            "file_count_delta": 10,
            "evidence": ["ten files created"],
        })
        self.assertFalse(result.valid)
        self.assertIn("no substantive", result.reason)

    def test_missing_evidence_is_invalid(self):
        result = assess_progress({
            "quality_delta": 1,
            "coverage_delta": 0,
            "evidence_quality_delta": 0,
            "validation_delta": 0,
            "uncertainty_delta": 0,
        })
        self.assertFalse(result.valid)
        self.assertIn("evidence", result.reason)


if __name__ == "__main__":
    unittest.main()
