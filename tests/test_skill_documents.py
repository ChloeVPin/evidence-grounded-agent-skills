import unittest
from pathlib import Path


class SkillDocumentTest(unittest.TestCase):
    def test_dependency_audit_contains_required_operational_sections(self):
        text = Path("skills/dependency-security-audit/SKILL.md").read_text()
        for section in (
            "## Purpose and scope", "## Triggers and prerequisites",
            "## Procedure", "## Acceptance checklist",
            "## Failure modes and recovery", "## Validation evidence and provenance",
        ):
            self.assertIn(section, text)
        self.assertGreaterEqual(text.count("- [ ]"), 7)

    def test_test_effectiveness_contains_required_operational_sections(self):
        text = Path("skills/test-effectiveness-analysis/SKILL.md").read_text()
        for section in (
            "## Purpose and scope", "## Triggers and prerequisites",
            "## Procedure", "## Acceptance checklist",
            "## Failure modes and recovery", "## Validation evidence and provenance",
        ):
            self.assertIn(section, text)
        self.assertGreaterEqual(text.count("- [ ]"), 7)


if __name__ == "__main__":
    unittest.main()
