import unittest

from scripts.bind_evidence import create_attestation, verify_attestation


EVIDENCE = {"revision": "a" * 40, "output_sha256": "b" * 64}


class BindEvidenceTest(unittest.TestCase):
    def test_attestation_matches_original_inputs(self):
        attestation = create_attestation("diff-v1", ["criterion a", "criterion b"], EVIDENCE)
        self.assertTrue(verify_attestation(
            attestation.__dict__, "diff-v1", ["criterion b", "criterion a"],
        ))

    def test_changed_diff_invalidates_attestation(self):
        attestation = create_attestation("diff-v1", ["criterion a"], EVIDENCE)
        self.assertFalse(verify_attestation(attestation.__dict__, "diff-v2", ["criterion a"]))

    def test_changed_criteria_invalidates_attestation(self):
        attestation = create_attestation("diff-v1", ["criterion a"], EVIDENCE)
        self.assertFalse(verify_attestation(
            attestation.__dict__, "diff-v1", ["criterion a", "criterion b"],
        ))


if __name__ == "__main__":
    unittest.main()
