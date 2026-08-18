import unittest

from scripts.bind_evidence import create_attestation
from scripts.review_change import review_change


def record(diff="diff-v1", criteria=None):
    criteria = criteria or ["requested behavior works"]
    evidence = {
        "revision": "a" * 40,
        "output_sha256": "b" * 64,
    }
    return {
        "paths": ["skills/example/SKILL.md"],
        "allowed_prefixes": ["skills/"],
        "acceptance_criteria": criteria,
        "diff": diff,
        "evidence": {
            "acceptance_criteria": criteria,
            "tests": [
                {"name": "focused", "kind": "focused", "status": "passed"},
                {"name": "boundary", "kind": "boundary", "status": "passed"},
            ],
        },
        "attestation": create_attestation(diff, criteria, evidence).__dict__,
    }


def dependency_evidence(name, status="verified"):
    return {name: {
        "source": f"https://registry.example/{name}",
        "looked_up_at": "2026-08-18T12:00:00Z",
        "status": status,
    }}


class EndToEndReviewTest(unittest.TestCase):
    def test_complete_record_is_accepted(self):
        result = review_change(record())
        self.assertTrue(result.accepted)
        self.assertTrue(result.scope_ok)
        self.assertTrue(result.evidence_ok)
        self.assertTrue(result.attestation_ok)

    def test_changed_diff_rejects_stale_record(self):
        review = record()
        review["diff"] = "diff-v2"
        result = review_change(review)
        self.assertFalse(result.accepted)
        self.assertFalse(result.attestation_ok)

    def test_sensitive_path_rejects_without_escalation(self):
        review = record()
        review["paths"] = [".github/workflows/ci.yml"]
        review["allowed_prefixes"] = [".github/workflows/"]
        result = review_change(review)
        self.assertFalse(result.accepted)
        self.assertTrue(result.scope_ok)
        self.assertFalse(result.escalation_ok)

    def test_vulnerable_dependency_blocks_complete_review(self):
        review = record()
        review["dependency"] = {
            "paths": ["requirements.txt"],
            "packages": {"old-lib": {"provenance_verified": True, "known_vulnerable": True}},
            "evidence": dependency_evidence("old-lib", "vulnerable"),
        }
        result = review_change(review)
        self.assertFalse(result.accepted)
        self.assertFalse(result.dependency_ok)

    def test_verified_dependency_can_pass_complete_review(self):
        review = record()
        review["dependency"] = {
            "paths": ["requirements.txt"],
            "packages": {"safe-lib": {"provenance_verified": True, "known_vulnerable": False}},
            "evidence": dependency_evidence("safe-lib"),
        }
        result = review_change(review)
        self.assertTrue(result.accepted)
        self.assertTrue(result.dependency_ok)

    def test_sensitive_path_accepts_valid_explicit_review(self):
        review = record()
        review["paths"] = [".github/workflows/ci.yml"]
        review["allowed_prefixes"] = [".github/workflows/"]
        review["escalation"] = {
            "reviewer": "reviewer@example.test",
            "decision": "accept",
            "rationale": "Pinned and minimal workflow change reviewed.",
            "timestamp": "2026-08-18T12:00:00Z",
            **{key: review["attestation"][key] for key in
               ("revision", "diff_sha256", "criteria_sha256")},
        }
        result = review_change(review)
        self.assertTrue(result.accepted)
        self.assertTrue(result.escalation_ok)

    def test_escalation_marker_without_rationale_is_rejected(self):
        review = record()
        review["paths"] = [".github/workflows/ci.yml"]
        review["allowed_prefixes"] = [".github/workflows/"]
        review["escalation"] = {"reviewer": "reviewer", "decision": "accept"}
        result = review_change(review)
        self.assertFalse(result.accepted)
        self.assertFalse(result.escalation_ok)

    def test_approval_copied_to_different_diff_is_rejected(self):
        approved = record()
        approved["paths"] = [".github/workflows/ci.yml"]
        approved["allowed_prefixes"] = [".github/workflows/"]
        approved["escalation"] = {
            "reviewer": "reviewer@example.test",
            "decision": "accept",
            "rationale": "Reviewed workflow change.",
            "timestamp": "2026-08-18T12:00:00Z",
            **{key: approved["attestation"][key] for key in
               ("revision", "diff_sha256", "criteria_sha256")},
        }
        copied = dict(approved)
        copied["diff"] = "different-diff"
        result = review_change(copied)
        self.assertFalse(result.accepted)
        self.assertFalse(result.attestation_ok)
        self.assertFalse(result.escalation_ok)


if __name__ == "__main__":
    unittest.main()
