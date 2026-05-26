# Test Engineer Agent

## Purpose

The Test Engineer Agent transforms attacks and defenses into **automated, repeatable test suites** that verify both the vulnerability (in the vulnerable app) and the mitigation (in the patched app). These tests serve as living evidence for the assurance pipeline and ensure that regressions are caught. This agent is the **sixth stage** in the content pipeline.

## Input Format

The agent requires:

1. **Class specification** — The `class-spec.yaml` produced by the Curriculum Architect Agent
2. **Vulnerable application code** — The `vulnerable/app.py` from the Lab Builder Agent
3. **Patched application code** — The `patched/app.py` from the Lab Builder Agent
4. **Attack script** — The `attacks/attack.py` from the Red-Team Scenario Agent
5. **Defense module** — The `defense.py` from the Blue-Team Defense Agent
6. **Control ledger** — The `assurance/control-ledger.yaml` from the Blue-Team Defense Agent

## Output Format

The agent must produce three test files:

### 1. `tests/test_vulnerable.py`

Tests that **verify the vulnerability exists** in the vulnerable app:

```python
"""
Tests for the VULNERABLE version of: {Class Title}
These tests CONFIRM the vulnerability exists — they are expected to show
that the attack succeeds against the vulnerable application.
"""

import pytest
import requests

BASE_URL_VULN = os.environ.get("VULN_APP_URL", "http://localhost:5000")


class TestVulnerabilityExists:
    """Confirm the vulnerability is present in the vulnerable app."""

    def test_app_running(self):
        """Verify the vulnerable app is accessible."""
        response = requests.get(f"{BASE_URL_VULN}/health")
        assert response.status_code == 200

    def test_vulnerability_exploitable(self):
        """Verify the specific vulnerability can be exploited."""
        # This test demonstrates the attack succeeds
        # Using the same payload as attacks/attack.py
        ...

    def test_attack_payload_succeeds(self):
        """Verify the attack payload produces the expected result."""
        ...


class TestControlAbsence:
    """Verify that the expected controls are ABSENT in the vulnerable app."""

    def test_no_input_validation(self):
        """Verify that malicious input is not rejected."""
        ...

    def test_no_output_sanitization(self):
        """Verify that sensitive data is not sanitized in responses."""
        ...
```

### 2. `tests/test_patched.py`

Tests that **verify the patch works** in the patched app:

```python
"""
Tests for the PATCHED version of: {Class Title}
These tests CONFIRM the mitigation works — they are expected to show
that the attack fails against the patched application.
"""

import pytest
import requests

BASE_URL_PATCHED = os.environ.get("PATCHED_APP_URL", "http://localhost:5001")


class TestPatchEffective:
    """Confirm the patch prevents the attack."""

    def test_app_running(self):
        """Verify the patched app is accessible."""
        response = requests.get(f"{BASE_URL_PATCHED}/health")
        assert response.status_code == 200

    def test_attack_blocked(self):
        """Verify the attack is blocked by the patch."""
        ...

    def test_legitimate_use_preserved(self):
        """Verify legitimate requests still work after patching."""
        ...


class TestControlPresence:
    """Verify that each control from the ledger is effective."""

    def test_ctl1_rejects_malicious_input(self):
        """CTL-1: Verify malicious input is rejected."""
        ...

    def test_ctl1_allows_legitimate_input(self):
        """CTL-1: Verify legitimate input is allowed."""
        ...

    def test_ctl2_detects_anomaly(self):
        """CTL-2: Verify anomalous behavior is detected."""
        ...


class TestDefenseInDepth:
    """Verify defense-in-depth: if one control fails, others still protect."""

    def test_secondary_control_when_primary_bypassed(self):
        """Verify secondary control catches what primary misses."""
        ...
```

### 3. `tests/conftest.py`

Shared test fixtures:

```python
"""
Shared test fixtures for: {Class Title}
"""

import pytest
import requests
import subprocess
import time
import os


@pytest.fixture(scope="session")
def vulnerable_app():
    """Start the vulnerable app for the test session."""
    port = int(os.environ.get("VULN_PORT", "5000"))
    proc = subprocess.Popen(
        ["python", "vulnerable/app.py"],
        env={**os.environ, "PORT": str(port)},
        cwd=os.path.dirname(os.path.dirname(__file__)),
    )
    # Wait for app to be ready
    for _ in range(30):
        try:
            requests.get(f"http://localhost:{port}/health", timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(0.5)
    yield f"http://localhost:{port}"
    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture(scope="session")
def patched_app():
    """Start the patched app for the test session."""
    port = int(os.environ.get("PATCHED_PORT", "5001"))
    proc = subprocess.Popen(
        ["python", "patched/app.py"],
        env={**os.environ, "PORT": str(port)},
        cwd=os.path.dirname(os.path.dirname(__file__)),
    )
    for _ in range(30):
        try:
            requests.get(f"http://localhost:{port}/health", timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(0.5)
    yield f"http://localhost:{port}"
    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture
def attack_payloads():
    """Return deterministic attack payloads matching attacks/attack.py."""
    return [
        # Payload 1: ...
        # Payload 2: ...
    ]


@pytest.fixture
def legitimate_payloads():
    """Return legitimate request payloads that should always work."""
    return [
        # Payload 1: ...
        # Payload 2: ...
    ]
```

## Constraints

1. **Pytest only.** All tests must use `pytest` as the test framework. No `unittest`, no `nose`.
2. **Deterministic.** Tests must produce the same pass/fail result on every run. Seed all random values. Use fixed payloads.
3. **No flaky tests.** Tests must not depend on timing, network latency, or external services. Use health-check polling with retries for app readiness.
4. **Isolated.** Each test must clean up after itself. Use fixtures with proper teardown.
5. **Both directions.** `test_vulnerable.py` must show the attack **succeeds**; `test_patched.py` must show the attack **fails** and legitimate use **works**.
6. **Control coverage.** Every control in the control ledger must have at least one test in `test_patched.py`. The test function name must match the `test_function` field in the ledger.
7. **Defense in depth.** At least one test must verify that a secondary control still protects even if the primary is bypassed.
8. **No live servers required for collection.** Tests should be skippable with `pytest.mark.skipif` if the target app is not running (for CI environments where apps are managed externally).
9. **Descriptive test names.** Every test function name must describe what it verifies. No `test_1`, `test_2`, etc.
10. **Docstrings.** Every test function must have a docstring explaining the test's purpose and what it asserts.
11. **Session-scoped fixtures.** App fixtures must be session-scoped to avoid starting/stopping the server for every test.
12. **Timeout protection.** Each test must have a timeout (via `pytest-timeout` or explicit timeout in requests). No test may run longer than 30 seconds.
13. **Clear failure messages.** Use explicit assertion messages: `assert condition, "Expected X but got Y"`.

## Prompt Skeleton

```
You are the Test Engineer Agent for the "AI Security from Scratch" curriculum.
Your job is to create automated test suites that verify the vulnerability in the
vulnerable app and the mitigation in the patched app.

CLASS SPECIFICATION:
---
{paste class-spec.yaml here}
---

VULNERABLE APPLICATION:
---
{paste vulnerable/app.py here}
---

PATCHED APPLICATION:
---
{paste patched/app.py here}
---

ATTACK SCRIPT:
---
{paste attacks/attack.py here}
---

DEFENSE MODULE:
---
{paste defense.py here}
---

CONTROL LEDGER:
---
{paste assurance/control-ledger.yaml here}
---

INSTRUCTIONS:
1. Read all inputs carefully.
2. Create tests/test_vulnerable.py that verifies the vulnerability exists.
3. Create tests/test_patched.py that verifies the patch works.
4. Create tests/conftest.py with shared fixtures.
5. Ensure every control in the ledger has a corresponding test.
6. Include defense-in-depth tests.
7. Use deterministic payloads matching the attack script.

CONSTRAINTS:
- Pytest only
- Deterministic (fixed payloads, seeded random)
- No flaky tests (health-check polling, no timing dependencies)
- Isolated (proper teardown)
- test_vulnerable.py shows attack succeeds
- test_patched.py shows attack fails + legitimate use works
- Control coverage: every ledger entry has a test
- Defense-in-depth test included
- Descriptive test names with docstrings
- Session-scoped app fixtures
- 30-second timeout per test
- Clear assertion messages

OUTPUT:
Produce tests/test_vulnerable.py, tests/test_patched.py, and tests/conftest.py.
Begin each file with: --- FILE: {relative path} ---
```

## Validation Checklist

Before accepting the agent's output, verify:

- [ ] All tests use pytest (no unittest/nose)
- [ ] Tests are deterministic (fixed payloads, seeded random)
- [ ] No timing-dependent assertions
- [ ] Fixtures have proper teardown
- [ ] `test_vulnerable.py` shows the attack succeeds
- [ ] `test_patched.py` shows the attack fails
- [ ] `test_patched.py` shows legitimate use still works
- [ ] Every control in the ledger has a corresponding test
- [ ] Test function names match the ledger's `test_function` field
- [ ] Defense-in-depth test is present
- [ ] All test functions have descriptive names
- [ ] All test functions have docstrings
- [ ] App fixtures are session-scoped
- [ ] Tests have timeout protection
- [ ] Assertion messages are clear and descriptive
