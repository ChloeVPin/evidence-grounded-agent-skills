import unittest
from pathlib import Path

from scripts.capture_evidence import capture


ROOT = Path(__file__).resolve().parents[1]


class CaptureEvidenceTest(unittest.TestCase):
    def test_captures_successful_command_and_revision(self):
        result = capture("python3 -c 'print(\"ok\")'", ROOT)
        self.assertEqual(result.exit_status, 0)
        self.assertEqual(len(result.revision), 40)
        self.assertEqual(len(result.output_sha256), 64)

    def test_captures_failed_command_without_fabricating_success(self):
        result = capture("python3 -c 'raise SystemExit(3)'", ROOT)
        self.assertEqual(result.exit_status, 3)
        self.assertEqual(len(result.output_sha256), 64)


if __name__ == "__main__":
    unittest.main()
