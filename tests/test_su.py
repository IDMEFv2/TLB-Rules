import json
import unittest
from pathlib import Path

from tests.engine import load_ruleset, run_case


class SuGrokRuleTests(unittest.TestCase):
    def test_su_fixture_cases(self):
        suite_dir = Path(__file__).resolve().parent / "su"
        patterns = load_ruleset(Path(__file__).resolve().parent.parent / "rulesets" / "su.yml")

        failures = []
        for fixture_path in sorted((suite_dir / "fixtures").glob("*.log")):
            expected_path = suite_dir / "expected" / f"{fixture_path.stem}.json"
            case = {
                "name": fixture_path.stem,
                "line": fixture_path.read_text(encoding="utf-8").strip(),
                "expected": json.loads(expected_path.read_text(encoding="utf-8")),
            }
            passed, payload = run_case(case, patterns)
            if not passed:
                failures.append(payload)

        self.assertFalse(failures, f"su Grok fixtures failed: {failures}")


if __name__ == "__main__":
    unittest.main()
