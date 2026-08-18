import unittest
from pathlib import Path


class RepositoryChangeVerificationStructureTest(unittest.TestCase):
    def test_required_sections_exist(self):
        text = Path("skills/repository-change-verification/SKILL.md").read_text()
        self.assertIn("Lifecycle: `validated`", text)
        required = [
            "## Purpose and scope",
            "## Triggers and prerequisites",
            "## Procedure",
            "## Acceptance checklist",
            "## Failure modes and recovery",
            "## Validation evidence and provenance",
            "## Related skills and conflicts",
        ]
        for section in required:
            self.assertIn(section, text)

    def test_checklist_has_release_gates(self):
        text = Path("skills/repository-change-verification/SKILL.md").read_text()
        self.assertGreaterEqual(text.count("- [ ]"), 7)


if __name__ == "__main__":
    unittest.main()
