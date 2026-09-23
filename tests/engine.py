import json
from pathlib import Path

import yaml
from pygrok import Grok


ROOT = Path(__file__).resolve().parent.parent
RULESET_PATH = ROOT / "rulesets" / "ssh.yml"


def load_ruleset(path: str | Path):
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    rules = data.get("rules", [])
    return [
        {"match": rule["match"], "alert_type": rule.get("alert_type"), "id": rule.get("id")}
        for rule in rules
        if rule.get("type") == "grok"
    ]


def load_cases(base_dir: str | Path):
    base_path = Path(base_dir)
    fixture_dir = base_path / "fixtures"
    expected_dir = base_path / "expected"

    cases = []
    for fixture_path in sorted(fixture_dir.glob("*.log")):
        expected_path = expected_dir / f"{fixture_path.stem}.json"
        if not expected_path.exists():
            raise FileNotFoundError(f"Missing expected results: {expected_path}")

        lines = [line.strip() for line in fixture_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            raise ValueError(f"Fixture file is empty: {fixture_path}")

        cases.append(
            {
                "name": fixture_path.stem,
                "line": lines[0],
                "expected": json.loads(expected_path.read_text(encoding="utf-8")),
            }
        )

    return cases


def run_case(case, patterns):
    expected = case["expected"]
    line = case["line"]
    matches = []

    for rule in patterns:
        grok = Grok(rule["match"])
        actual = grok.match(line)
        if actual is not None:
            actual["alert_type"] = rule.get("alert_type")
            matches.append({"rule_id": rule.get("id"), "pattern": rule["match"], "actual": actual})

    if expected.get("match") is False:
        if not matches:
            return True, {"case": case["name"], "matched": False, "line": line}
        return False, {"case": case["name"], "expected": {"match": False}, "actual_matches": matches, "line": line}

    if not matches:
        return False, {"case": case["name"], "error": "pattern did not match", "line": line}

    for match in matches:
        actual = match["actual"]
        mismatches = [
            f"{field}: expected={expected[field]!r}, actual={actual.get(field)!r}"
            for field in expected
            if actual.get(field) != expected[field]
        ]
        if not mismatches:
            return True, {"case": case["name"], "rule_id": match["rule_id"], "pattern": match["pattern"], "actual": actual}

    return False, {"case": case["name"], "expected": expected, "actual_matches": matches, "line": line}


def run_suite(base_dir: str | Path):
    patterns = load_ruleset(RULESET_PATH)
    failures = []
    for case in load_cases(base_dir):
        passed, payload = run_case(case, patterns)
        if not passed:
            failures.append(payload)

    return failures


if __name__ == "__main__":
    from pprint import pprint

    suite_dir = Path(__file__).resolve().parent / "ssh"
    failures = run_suite(suite_dir)
    if failures:
        print("FAILED")
        pprint(failures)
        raise SystemExit(1)

    print("PASSED")
