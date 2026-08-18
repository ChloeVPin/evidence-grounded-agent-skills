import unittest

from scripts.tool_policy import ToolPolicy, authorize


READ = ToolPolicy(frozenset({"read"}), ("repo/docs/",), frozenset({"path"}))
WRITE = ToolPolicy(frozenset({"write"}), ("repo/docs/",), frozenset({"path", "content"}))


class ToolPolicyTest(unittest.TestCase):
    def test_scoped_read_is_allowed(self):
        self.assertTrue(authorize(READ, action="read", resource="repo/docs/a.md", parameters={"path": "a.md"}).allowed)

    def test_write_requires_approval(self):
        result = authorize(WRITE, action="write", resource="repo/docs/a.md", parameters={"path": "a.md", "content": "x"})
        self.assertFalse(result.allowed)
        self.assertIn("approval", result.reason)

    def test_write_with_approval_is_allowed(self):
        result = authorize(WRITE, action="write", resource="repo/docs/a.md", parameters={"path": "a.md", "content": "x"}, approval=True)
        self.assertTrue(result.allowed)

    def test_out_of_scope_resource_is_rejected(self):
        result = authorize(READ, action="read", resource="repo/secrets/key", parameters={"path": "key"})
        self.assertFalse(result.allowed)

    def test_undeclared_parameter_is_rejected(self):
        result = authorize(READ, action="read", resource="repo/docs/a.md", parameters={"path": "a.md", "admin": True})
        self.assertFalse(result.allowed)

    def test_wildcard_authority_is_rejected(self):
        policy = ToolPolicy(frozenset({"*"}), ("repo/docs/",), frozenset())
        self.assertFalse(authorize(policy, action="read", resource="repo/docs/a", parameters={}).allowed)


if __name__ == "__main__":
    unittest.main()
