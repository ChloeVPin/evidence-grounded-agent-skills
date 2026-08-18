import unittest

from scripts.lookup_adapter import normalize_lookup


class LookupAdapterTest(unittest.TestCase):
    def test_resolved_clean_lookup_is_verified(self):
        result = normalize_lookup(
            {"registry_resolved": True, "advisories": []},
            source="registry", looked_up_at="2026-08-18T12:00:00Z",
        )
        self.assertEqual(result.status, "verified")
        self.assertEqual(len(result.raw_output_sha256), 64)

    def test_unavailable_lookup_is_unknown(self):
        result = normalize_lookup(None, source="registry", looked_up_at="2026-08-18T12:00:00Z")
        self.assertEqual(result.status, "unknown")

    def test_advisory_lookup_is_vulnerable(self):
        result = normalize_lookup(
            {"registry_resolved": True, "advisories": ["CVE-example"]},
            source="advisory-db", looked_up_at="2026-08-18T12:00:00Z",
        )
        self.assertEqual(result.status, "vulnerable")

    def test_malformed_response_is_unknown(self):
        result = normalize_lookup(
            {"registry_resolved": "yes", "advisories": "none"},
            source="registry", looked_up_at="2026-08-18T12:00:00Z",
        )
        self.assertEqual(result.status, "unknown")


if __name__ == "__main__":
    unittest.main()
