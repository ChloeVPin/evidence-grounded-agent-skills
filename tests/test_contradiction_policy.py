import unittest

from scripts.contradiction_policy import Claim, resolve_claims


class ContradictionPolicyTest(unittest.TestCase):
    def claims(self, first_context="same", second_context="same", first_strength=2, second_strength=1):
        return Claim("first", first_context, first_strength), Claim("second", second_context, second_strength)

    def test_stronger_discriminating_evidence_supports_one_claim(self):
        first, second = self.claims()
        result = resolve_claims(first, second, discriminating_evidence=True)
        self.assertEqual(result.outcome, "supported_refuted")
        self.assertEqual(result.winner, "first")

    def test_different_contexts_are_not_forced_into_one_winner(self):
        first, second = self.claims("python", "javascript")
        result = resolve_claims(first, second, discriminating_evidence=True)
        self.assertEqual(result.outcome, "contextual")
        self.assertIsNone(result.winner)

    def test_missing_discriminating_evidence_is_unresolved(self):
        first, second = self.claims()
        result = resolve_claims(first, second, discriminating_evidence=False)
        self.assertEqual(result.outcome, "unresolved")

    def test_equal_evidence_remains_unresolved(self):
        first, second = self.claims(first_strength=2, second_strength=2)
        result = resolve_claims(first, second, discriminating_evidence=True)
        self.assertEqual(result.outcome, "unresolved")


if __name__ == "__main__":
    unittest.main()
