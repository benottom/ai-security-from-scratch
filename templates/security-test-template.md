# Security Test: [TEST_NAME]

> **Test ID:** [TEST_ID] | **Version:** [VERSION] | **Last Updated:** [DATE] | **Author:** [AUTHOR]

---

## Test Identification

| Field | Value |
|---|---|
| **Test ID** | [TEST_ID — e.g., SEC-PROMPT-001] |
| **Test Name** | [TEST_NAME — e.g., "System prompt extraction via role override"] |
| **Security Claim** | [CLAIM — e.g., "System instructions are not accessible or influenceable by user input"] |
| **Attack Category** | [CATEGORY — e.g., Prompt Injection / Data Exfiltration / Unauthorized Tool Use / Permission Bypass / Output Manipulation / Supply Chain] |
| **Test Type** | [NEGATIVE — attack must be blocked / POSITIVE — expected behavior must be confirmed] |
| **Severity** | [CRITICAL|HIGH|MEDIUM|LOW] |

---

## Test Specification

### Input Specification

**Input to the system under test:**

```json
{
  "messages": [
    {
      "role": "system",
      "content": "[SYSTEM_INSTRUCTION]"
    },
    {
      "role": "user",
      "content": "[ATTACK_PAYLOAD]"
    }
  ],
  "temperature": [TEMPERATURE],
  "max_tokens": [MAX_TOKENS],
  "tools": [TOOLS_SPECIFICATION_IF_APPLICABLE]
}
```

**Attack payload:**

```
[ATTACK_PAYLOAD — the specific adversarial input being tested]
```

**Payload variants:**

| Variant ID | Payload | Variation Type | Rationale |
|---|---|---|---|
| V-01 | [PAYLOAD_1] | [BASELINE|ENCODING|OBFUSCATION|CHAINING|CONTEXT_SWITCH] | [WHY_THIS_VARIANT] |
| V-02 | [PAYLOAD_2] | [BASELINE|ENCODING|OBFUSCATION|CHAINING|CONTEXT_SWITCH] | [WHY_THIS_VARIANT] |
| V-03 | [PAYLOAD_3] | [BASELINE|ENCODING|OBFUSCATION|CHAINING|CONTEXT_SWITCH] | [WHY_THIS_VARIANT] |

---

## Expected Behavior

### Vulnerable Application (No Defense)

| Aspect | Expected Result |
|---|---|
| **Response Content** | [WHAT_THE_VULNERABLE_APP_RETURNS — e.g., "Model reveals system instructions verbatim"] |
| **Status Code** | [HTTP_STATUS] |
| **Tool Execution** | [WHETHER_TOOLS_ARE_INVOKED] |
| **Audit Log** | [WHETHER_ATTACK_IS_LOGGED] |

**Evidence of vulnerability:**

```
[EXPECTED_OUTPUT_FROM_VULNERABLE_APP]
```

### Patched Application (With Defense)

| Aspect | Expected Result |
|---|---|
| **Response Content** | [WHAT_THE_PATCHED_APP_RETURNS — e.g., "Model declines the request with a safe refusal message"] |
| **Status Code** | [HTTP_STATUS] |
| **Tool Execution** | [WHETHER_TOOLS_ARE_BLOCKED] |
| **Audit Log** | [WHETHER_ATTACK_AND_BLOCK_ARE_LOGGED] |

**Evidence of defense:**

```
[EXPECTED_OUTPUT_FROM_PATCHED_APP]
```

---

## Control Objective

The safety objective this test validates:

> **Control Objective:** [CONTROL_OBJECTIVE — e.g., "User input must never cause the system to reveal, modify, or override system-level instructions."]

**Control-loop mapping:**

| Element | Specification |
|---|---|
| **What is observed** | [WHAT_THE_CONTROLLER_OBSERVES] |
| **What is decided** | [WHAT_DECISION_THE_CONTROLLER_MAKES] |
| **What action is taken** | [WHAT_ACTION_IS_EXECUTED] |
| **Expected feedback** | [WHAT_FEEDBACK_IS_GENERATED] |

---

## Assertion Code

```python
"""Security test: [TEST_NAME]

Test ID: [TEST_ID]
Attack Category: [CATEGORY]
Control Objective: [CONTROL_OBJECTIVE]
"""

import pytest
from test_utils import SecurityTestClient, assert_no_leak, assert_blocked, assert_audit_logged


class Test[TEST_CLASS_NAME]:
    """Security regression test for [VULNERABILITY_TYPE]."""

    @pytest.fixture
    def client(self):
        """Initialize the security test client."""
        return SecurityTestClient(
            base_url=pytest.config.getoption("--app-url"),
            api_key=pytest.config.getoption("--api-key"),
        )

    def test_attack_blocked_patched_app(self, client):
        """Verify the patched application blocks the attack.

        NEGATIVE TEST: The attack payload must be rejected.
        """
        response = client.send_message(
            user_content="[ATTACK_PAYLOAD]",
            system_content="[SYSTEM_INSTRUCTION]",
        )

        # Assert: The attack is blocked
        assert_blocked(response), (
            f"Attack was not blocked. Response contained: {response.content}"
        )

        # Assert: No leakage of sensitive content
        assert_no_leak(response, patterns=["[LEAK_PATTERN_1]", "[LEAK_PATTERN_2]"]), (
            f"Sensitive content leaked in response: {response.content}"
        )

        # Assert: The action was logged for audit
        assert_audit_logged(response, event_type="security_block"), (
            "Security block was not recorded in audit log"
        )

    def test_normal_input_still_works_patched_app(self, client):
        """Verify the patched application still handles normal input.

        POSITIVE TEST: Normal functionality must not regress.
        """
        response = client.send_message(
            user_content="[NORMAL_INPUT]",
            system_content="[SYSTEM_INSTRUCTION]",
        )

        # Assert: Normal requests succeed
        assert response.status_code == 200, (
            f"Normal request failed with status {response.status_code}"
        )
        assert response.content is not None, "No response content for normal input"
        assert_no_leak(response, patterns=["[LEAK_PATTERN_1]"]), (
            "Normal response unexpectedly triggered security block"
        )

    def test_attack_succeeds_vulnerable_app(self, client):
        """Verify the vulnerable application is exploitable.

        This test confirms the vulnerability exists in the baseline.
        It should FAIL after the fix is applied (expected).
        """
        vulnerable_client = SecurityTestClient(
            base_url=pytest.config.getoption("--vulnerable-app-url"),
            api_key=pytest.config.getoption("--api-key"),
        )

        response = vulnerable_client.send_message(
            user_content="[ATTACK_PAYLOAD]",
            system_content="[SYSTEM_INSTRUCTION]",
        )

        # This assertion confirms the vulnerability is present
        # After patching, this test should be skipped or expected to fail
        assert not assert_blocked(response), (
            "Vulnerable app unexpectedly blocked the attack — verify test setup"
        )

    @pytest.mark.parametrize("variant_id,payload", [
        ("V-01", "[PAYLOAD_1]"),
        ("V-02", "[PAYLOAD_2]"),
        ("V-03", "[PAYLOAD_3]"),
    ])
    def test_attack_variants_blocked(self, client, variant_id, payload):
        """Verify the patched application blocks all attack variants.

        NEGATIVE TEST: All variants of the attack must be rejected.
        """
        response = client.send_message(
            user_content=payload,
            system_content="[SYSTEM_INSTRUCTION]",
        )

        assert_blocked(response), (
            f"Variant {variant_id} was not blocked. Response: {response.content}"
        )
        assert_no_leak(response, patterns=["[LEAK_PATTERN_1]", "[LEAK_PATTERN_2]"]), (
            f"Variant {variant_id} caused content leakage: {response.content}"
        )
```

---

## Test Execution

### Running This Test

```bash
# Run against the vulnerable application
pytest tests/security/test_[TEST_FILE].py --app-url http://localhost:8000 --vulnerable-app-url http://localhost:8001 -v

# Run with evidence generation
pytest tests/security/test_[TEST_FILE].py --app-url http://localhost:8000 --junitxml=evidence/[TEST_ID]-results.xml

# Run only attack-variant tests
pytest tests/security/test_[TEST_FILE].py -k "variant" -v
```

### Test Data

| Data File | Description | Sensitive |
|---|---|---|
| [DATA_FILE_1] | [DESCRIPTION] | [YES|NO] |
| [DATA_FILE_2] | [DESCRIPTION] | [YES|NO] |

---

## Traceability

| Mapping | Reference |
|---|---|
| **Threat Model** | [THREAT_ID — e.g., T-01] |
| **Control-Loop Element** | [ELEMENT — e.g., Context Firewall controller] |
| **Security Pattern** | [PATTERN — e.g., Context Firewall] |
| **OWASP LLM Top 10** | [REFERENCE — e.g., LLM01: Prompt Injection] |
| **NIST AI RMF** | [REFERENCE — e.g., MAP 2.3, MEASURE 2.6] |
| **ISO 27001** | [REFERENCE — e.g., A.8.9] |

---

*Template version: 1.0.0 | AI Security from Scratch*
