# TLB-Rules

TLB-Rules is a detection and parsing rule repository designed for security log normalization and SIEM use cases. It centralizes Grok-based patterns for common system and security telemetry sources, with an initial focus on OpenSSH sshd activity and a structure that can be extended to HTTP servers, authentication systems, firewalls, proxies, and application logs.

## Project purpose

This project is intended to support security operations and detection engineering workflows by providing:

- reusable log parsing rules
- structured field extraction for SIEM ingestion
- rule validation through fixture-based tests
- a clean foundation for adding new log sources beyond SSHd

The repository is built to be expanded as a rule library for operational security monitoring, where each log source gets a dedicated ruleset and test corpus.

## Current contents

- [rulesets/ssh.yml](rulesets/ssh.yml): security-focused sshd parsing rules for suspicious authentication activity
- [tests/ssh](tests/ssh): fixture-based tests for sshd samples and expected parsed fields
- [tests/engine.py](tests/engine.py): Grok test harness built around `pygrok`
- [tests/test_ssh.py](tests/test_ssh.py): the SSH validation entrypoint

## Security focus

The rules are intentionally scoped to suspicious or potentially malicious events rather than normal successful activity. For example, the project does not treat a successful SSH login as a security event, but it does flag patterns such as:

- failed authentication attempts
- invalid users
- repeated auth failures / brute-force indicators
- disallowed or restricted accounts
- root login attempts
- public-key failures
- abnormal SSH protocol behavior

This makes the ruleset suitable for SIEM alerting, investigation, and enrichment pipelines where benign traffic should not create noise.

## Rule model

Each ruleset is designed as a collection of Grok patterns, each with a clear security meaning and expected extracted fields. The repository follows a test-first approach: a log sample is stored as a fixture, the expected output is stored alongside it, and the parser is checked against the real Grok library.

This helps ensure that new rules remain accurate and repeatable as the project grows beyond SSHd.

## Local testing

The repository uses a Python virtual environment and the `pygrok` library for validation.

From the project root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip -r requirements.txt
python -m unittest discover -s tests -p 'test_*.py' -v
```

This runs the complete fixture-driven suite across all rulesets, including sshd and su, and validates that suspicious events match while benign activity does not.

## Extending the project

To add support for another log source, follow the same pattern:

1. create a new ruleset file under [rulesets](rulesets)
2. add representative log fixtures under a matching folder in [tests](tests)
3. add expected extracted fields in JSON format
4. expand the test runner or add a new test file if needed
5. validate locally with the Python unit test command above

This repository is intended to evolve into a broader SIEM-oriented rules library covering multiple toolchains and security telemetry streams beyond SSHd.
