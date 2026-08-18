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

    def test_tool_authorization_contains_required_operational_sections(self):
        text = Path("skills/tool-authorization-audit/SKILL.md").read_text()
        for section in (
            "## Purpose and scope", "## Triggers and prerequisites",
            "## Procedure", "## Acceptance checklist",
            "## Failure modes and recovery", "## Validation evidence and provenance",
        ):
            self.assertIn(section, text)
        self.assertGreaterEqual(text.count("- [ ]"), 8)

    def test_differential_patch_review_contains_required_operational_sections(self):
        text = Path("skills/differential-patch-review/SKILL.md").read_text()
        for section in (
            "## Purpose and scope", "## Triggers and prerequisites",
            "## Procedure", "## Acceptance checklist",
            "## Failure modes and recovery", "## Validation evidence and provenance",
        ):
            self.assertIn(section, text)
        self.assertGreaterEqual(text.count("- [ ]"), 7)

    def test_knowledge_maintenance_contains_required_operational_sections(self):
        text = Path("skills/knowledge-maintenance/SKILL.md").read_text()
        for section in (
            "## Purpose and scope", "## Triggers and prerequisites",
            "## Procedure", "## Acceptance checklist",
            "## Failure modes and recovery", "## Validation evidence and provenance",
        ):
            self.assertIn(section, text)
        self.assertGreaterEqual(text.count("- [ ]"), 8)

    def test_contradiction_resolution_contains_required_operational_sections(self):
        text = Path("skills/contradiction-resolution/SKILL.md").read_text()
        for section in (
            "## Purpose and scope", "## Triggers and prerequisites",
            "## Procedure", "## Acceptance checklist",
            "## Failure modes and recovery", "## Validation evidence and provenance",
        ):
            self.assertIn(section, text)
        self.assertGreaterEqual(text.count("- [ ]"), 8)


if __name__ == "__main__":
    unittest.main()
