# Copilot instructions for TLB-Rules

## Project goal
This repository stores security detection and log-parsing rules for SIEM-oriented use cases. The project is designed to be extended with additional log sources beyond SSHd and su.

## Core principles
- Keep rules security-focused: prioritize suspicious or malicious behavior over benign operational logs.
- Do not mark successful authentication events as security alerts unless explicitly required.
- Prefer clear, descriptive rule IDs and alert types.
- Keep log parsing patterns deterministic and specific enough to avoid false positives.

## Repository structure
- `rulesets/`: Grok/YAML rule definitions for each log source.
- `tests/`: fixture-driven validation for rules.
- `tests/ssh/` and `tests/su/`: log fixtures and expected results for each ruleset.
- `requirements.txt`: Python dependencies for tests.
- `Makefile`: single-command project validation.

## Testing expectations
- Use the project test command when validating changes:
  ```bash
  python -m unittest discover -s tests -p 'test_*.py' -v
  ```
- Or use:
  ```bash
  make test
  ```
- Keep fixture-based tests in place. When adding a new log source, add a matching fixture directory and expected JSON files.
- Prefer real matching behavior over mock behavior.

## Rule authoring guidelines
- Add `alert_type` metadata to security-relevant rules, so parsed results explicitly describe the event category.
- Keep rule naming consistent with the log source, for example `sshd_*` or `su_*`.
- Prefer precise patterns over overly generic ones that accidentally match benign lines.
- When a rule is benign or non-alerting, keep it out of the security ruleset or mark it as non-match in tests.

## Code style
- Keep YAML rules readable and grouped by event type.
- Use small fixture sets with clear expected outputs.
- Prefer explicit expected field dictionaries instead of loose assertions.
