# Output Validator

## Overview

The **Output Validator** is the final defense layer in the AI control loop. It inspects the LLM's generated output before it reaches the user, checking for PII, secrets, policy violations, and other sensitive information. It supports blocking, redaction, and warning actions.

## Control-Theoretic View

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Controller  │     │  Output          │     │  User /      │
│  (LLM)      │────▶│  Validator       │────▶│  Environment │
│              │     │  (Output Filter) │     │              │
└──────────────┘     └──────────────────┘     └──────────────┘
```

In the control-loop model:
- The **Output Validator** is the *output filter* — the last line of defense before the system's output reaches the environment
- Even if upstream defenses (context firewall, policy engine) fail, the output validator can catch leaked secrets, PII, or policy violations
- It acts as a *safety interlock* that prevents dangerous outputs from causing harm

### Detection Categories

| Category         | Examples                              | Default Action |
|------------------|---------------------------------------|----------------|
| **Secret**       | API keys, tokens, passwords, keys     | BLOCK          |
| **PII**          | SSNs, credit cards, emails, phones    | REDACT / WARN  |
| **Content Policy**| Injection artifacts, prompt leaks    | BLOCK          |

### Actions

| Action    | Behavior                                              |
|-----------|-------------------------------------------------------|
| BLOCK     | Finding prevents output from being delivered          |
| REDACT    | Sensitive content is replaced with `[REDACTED_X]`     |
| WARN      | Content passes through but finding is logged           |

## Usage Examples

### Basic Validation

```python
from output_validator import OutputValidator

validator = OutputValidator()

# Clean output — valid
result = validator.validate("The weather today is sunny and warm.")
assert result.is_valid

# Output with API key — invalid (blocked)
result = validator.validate("The API key is sk-abc123def456ghi789jkl012")
assert not result.is_valid
assert result.has_critical_findings
```

### Redaction

```python
# PII like SSN gets redacted (not blocked)
result = validator.validate("Your SSN is 123-45-6789")
# result.redacted_content = "Your SSN is [REDACTED_PII]"

# validate_and_redact returns safe content or empty string if blocked
safe = validator.validate_and_redact("Contact me at user@example.com")
# Returns content with email warning logged
```

### Custom Rules

```python
from output_validator import OutputValidator, ValidationRule, Severity, ValidationAction

validator = OutputValidator(use_builtin_rules=False)
validator.add_rule(ValidationRule(
    name="project_codename",
    category="internal",
    pattern=r"\bPROJECT[A-Z]+\b",
    severity=Severity.HIGH,
    action=ValidationAction.REDACT,
    description="Project codenames must be redacted",
))

result = validator.validate("The PROJECTPHOENIX launch is scheduled for Q3")
assert "PROJECTPHOENIX" not in result.redacted_content
```

### Analyzing Results

```python
result = validator.validate(some_output)

# Check by category
secrets = validator.get_findings_by_category(result, "secret")
pii = validator.get_findings_by_category(result, "pii")

# Check by severity
critical = validator.get_findings_by_severity(result, Severity.CRITICAL)
```

## Built-in Rules

The validator includes 16 built-in rules covering:

- **Secrets**: OpenAI keys, AWS keys, GitHub PATs, Slack tokens, Google API keys, private keys, connection strings, passwords, generic secrets
- **PII**: SSNs, credit card numbers, email addresses, phone numbers
- **Content Policy**: Injection artifacts, system prompt leaks

## Limitations

- Regex-based detection can produce false positives (e.g., SSN pattern matching dates).
- Does not detect semantically sensitive content (e.g., proprietary information phrased differently).
- Should be combined with upstream defenses for defense-in-depth.
- Production systems should add context-aware NER (Named Entity Recognition) for PII.
