import unittest
from pathlib import Path

from tests.engine import run_suite


class SshGrokRuleTests(unittest.TestCase):
    def test_ssh_fixture_cases(self):
        suite_dir = Path(__file__).resolve().parent / "ssh"
        failures = run_suite(suite_dir)
        self.assertFalse(failures, f"SSHd Grok fixtures failed: {failures}")


if __name__ == "__main__":
    unittest.main()
