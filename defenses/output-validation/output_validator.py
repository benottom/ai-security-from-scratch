"""
Output Validator — Output validation layer for AI systems.

Checks generated content for PII, secrets, policy violations, and other
sensitive information using regex-based pattern matching and simple heuristics.

Control-Theoretic View:
    In the control loop, the output validator is the output filter — it inspects
    the plant's (LLM's) output before it reaches the environment (user). This is
    the final defense layer before the system's actions become visible, making it
    critical for preventing data leakage and policy violations.

Key Properties:
    1. PII detection: SSNs, phone numbers, email addresses, credit cards
    2. Secret detection: API keys, tokens, private keys, connection strings
    3. Content policy checks: harmful content, injection artifacts
    4. Configurable severity levels and actions
    5. Redaction support: sensitive content can be masked in output
"""

from __future__ import annotations

import enum
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


class ValidationAction(enum.Enum):
    """Action to take when a validation rule triggers."""
    BLOCK = "block"
    REDACT = "redact"
    WARN = "warn"


class Severity(enum.Enum):
    """Severity level of a validation finding."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ValidationFinding:
    """A single finding from output validation."""
    rule_name: str
    category: str
    severity: Severity
    matched_text: str
    start_position: int
    end_position: int
    description: str = ""
    action: ValidationAction = ValidationAction.BLOCK

    def to_dict(self) -> dict:
        return {
            "rule_name": self.rule_name,
            "category": self.category,
            "severity": self.severity.value,
            "matched_text": self._mask_matched(),
            "start_position": self.start_position,
            "end_position": self.end_position,
            "description": self.description,
            "action": self.action.value,
        }

    def _mask_matched(self) -> str:
        """Return a masked version of the matched text for safe logging."""
        if len(self.matched_text) <= 4:
            return "*" * len(self.matched_text)
        return self.matched_text[:2] + "*" * (len(self.matched_text) - 4) + self.matched_text[-2:]


@dataclass
class ValidationResult:
    """Result of validating a piece of content."""
    is_valid: bool
    findings: list[ValidationFinding] = field(default_factory=list)
    redacted_content: str = ""
    original_content: str = ""
    validation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def has_critical_findings(self) -> bool:
        return any(f.severity == Severity.CRITICAL for f in self.findings)

    @property
    def has_high_findings(self) -> bool:
        return any(f.severity == Severity.HIGH for f in self.findings)

    @property
    def blocked_findings(self) -> list[ValidationFinding]:
        return [f for f in self.findings if f.action == ValidationAction.BLOCK]

    @property
    def should_block(self) -> bool:
        return len(self.blocked_findings) > 0

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "findings": [f.to_dict() for f in self.findings],
            "has_critical": self.has_critical_findings,
            "has_high": self.has_high_findings,
            "should_block": self.should_block,
            "validation_id": self.validation_id,
            "timestamp": self.timestamp,
        }


@dataclass
class ValidationRule:
    """A validation rule with a regex pattern and associated action."""
    name: str
    category: str
    pattern: str
    severity: Severity = Severity.MEDIUM
    action: ValidationAction = ValidationAction.BLOCK
    description: str = ""
    redaction_template: str = "[REDACTED_{CATEGORY}]"
    _compiled: Optional[re.Pattern] = field(default=None, repr=False, init=False)

    def __post_init__(self):
        try:
            self._compiled = re.compile(self.pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern in rule '{self.name}': {e}")

    def check(self, content: str) -> list[ValidationFinding]:
        """Check content against this rule. Returns a list of findings."""
        findings = []
        if not self._compiled:
            return findings

        for match in self._compiled.finditer(content):
            findings.append(ValidationFinding(
                rule_name=self.name,
                category=self.category,
                severity=self.severity,
                matched_text=match.group(),
                start_position=match.start(),
                end_position=match.end(),
                description=self.description,
                action=self.action,
            ))
        return findings


# Built-in validation rules for common sensitive patterns
BUILTIN_RULES: list[ValidationRule] = [
    # Secrets & Credentials
    ValidationRule(
        name="openai_api_key",
        category="secret",
        pattern=r"sk-[a-zA-Z0-9]{20,}",
        severity=Severity.CRITICAL,
        description="OpenAI API key detected",
    ),
    ValidationRule(
        name="aws_access_key",
        category="secret",
        pattern=r"AKIA[A-Z0-9]{16}",
        severity=Severity.CRITICAL,
        description="AWS access key ID detected",
    ),
    ValidationRule(
        name="github_pat",
        category="secret",
        pattern=r"ghp_[a-zA-Z0-9]{36}",
        severity=Severity.CRITICAL,
        description="GitHub personal access token detected",
    ),
    ValidationRule(
        name="slack_token",
        category="secret",
        pattern=r"xox[baprs]-[a-zA-Z0-9\-]+",
        severity=Severity.CRITICAL,
        description="Slack token detected",
    ),
    ValidationRule(
        name="google_api_key",
        category="secret",
        pattern=r"AIza[a-zA-Z0-9_\-]{35}",
        severity=Severity.CRITICAL,
        description="Google API key detected",
    ),
    ValidationRule(
        name="private_key",
        category="secret",
        pattern=r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----",
        severity=Severity.CRITICAL,
        description="Private key detected in output",
    ),
    ValidationRule(
        name="connection_string",
        category="secret",
        pattern=r"(?:mongodb(?:\+srv)?|postgres(?:ql)?|mysql|redis)://[^\s'\"]+",
        severity=Severity.CRITICAL,
        description="Database connection string detected",
    ),
    ValidationRule(
        name="generic_password",
        category="secret",
        pattern=r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"]?[^\s'\"]{8,}",
        severity=Severity.HIGH,
        description="Password value detected in output",
    ),
    ValidationRule(
        name="generic_secret",
        category="secret",
        pattern=r"(?i)(?:secret[_-]?key|api[_-]?key|auth[_-]?token)\s*[:=]\s*['\"]?[^\s'\"]{8,}",
        severity=Severity.HIGH,
        description="Secret/key value detected in output",
    ),
    # PII
    ValidationRule(
        name="ssn",
        category="pii",
        pattern=r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",
        severity=Severity.HIGH,
        description="Potential Social Security Number detected",
        action=ValidationAction.REDACT,
    ),
    ValidationRule(
        name="credit_card",
        category="pii",
        pattern=r"\b(?:\d[ -]?){13,16}\b",
        severity=Severity.HIGH,
        description="Potential credit card number detected",
        action=ValidationAction.REDACT,
    ),
    ValidationRule(
        name="email_address",
        category="pii",
        pattern=r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b",
        severity=Severity.MEDIUM,
        description="Email address detected",
        action=ValidationAction.WARN,
    ),
    ValidationRule(
        name="phone_number",
        category="pii",
        pattern=r"(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        severity=Severity.MEDIUM,
        description="Phone number detected",
        action=ValidationAction.WARN,
    ),
    # Content policy
    ValidationRule(
        name="injection_artifact",
        category="content_policy",
        pattern=r"(?i)ignore\s+(?:previous|above|all)\s+(?:instructions|prompts|rules)",
        severity=Severity.HIGH,
        description="Injection artifact detected in output",
    ),
    ValidationRule(
        name="system_prompt_leak",
        category="content_policy",
        pattern=r"(?i)(?:system|assistant)\s*(?:prompt|instructions?)\s*[:=]",
        severity=Severity.HIGH,
        description="System prompt leak detected in output",
    ),
]


class OutputValidator:
    """
    Output validation layer for AI systems.

    Checks generated content for PII, secrets, and policy violations
    using regex-based pattern matching.

    Usage:
        validator = OutputValidator()
        result = validator.validate("The API key is sk-abc123...")
        assert not result.is_valid
    """

    def __init__(self, custom_rules: Optional[list[ValidationRule]] = None, use_builtin_rules: bool = True):
        self._rules: list[ValidationRule] = []
        self._audit_log: list[dict] = []

        if use_builtin_rules:
            self._rules.extend(BUILTIN_RULES)

        if custom_rules:
            self._rules.extend(custom_rules)

    @property
    def rules(self) -> list[ValidationRule]:
        return list(self._rules)

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit_log)

    def add_rule(self, rule: ValidationRule) -> None:
        """Add a custom validation rule."""
        self._rules.append(rule)

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name."""
        for i, rule in enumerate(self._rules):
            if rule.name == name:
                self._rules.pop(i)
                return True
        return False

    def validate(self, content: str) -> ValidationResult:
        """
        Validate content against all rules.

        Args:
            content: The text to validate.

        Returns:
            A ValidationResult with findings and redacted content.
        """
        all_findings: list[ValidationFinding] = []

        for rule in self._rules:
            findings = rule.check(content)
            all_findings.extend(findings)

        # Sort findings by position
        all_findings.sort(key=lambda f: f.start_position)

        # Determine if content is valid (no BLOCK findings)
        is_valid = not any(f.action == ValidationAction.BLOCK for f in all_findings)

        # Create redacted content
        redacted = self._redact_content(content, all_findings)

        result = ValidationResult(
            is_valid=is_valid,
            findings=all_findings,
            redacted_content=redacted,
            original_content=content,
        )

        self._log_validation(result)

        return result

    def validate_and_redact(self, content: str) -> str:
        """
        Validate and return redacted content. If any BLOCK-level findings
        exist, returns empty string.

        Args:
            content: The text to validate.

        Returns:
            Redacted content, or empty string if blocked.
        """
        result = self.validate(content)
        if result.should_block:
            return ""
        return result.redacted_content

    def get_findings_by_category(self, result: ValidationResult, category: str) -> list[ValidationFinding]:
        """Filter findings by category."""
        return [f for f in result.findings if f.category == category]

    def get_findings_by_severity(self, result: ValidationResult, severity: Severity) -> list[ValidationFinding]:
        """Filter findings by severity."""
        return [f for f in result.findings if f.severity == severity]

    def _redact_content(self, content: str, findings: list[ValidationFinding]) -> str:
        """Redact sensitive content based on findings."""
        if not findings:
            return content

        # Work backwards to preserve positions
        redacted = content
        for finding in sorted(findings, key=lambda f: f.start_position, reverse=True):
            if finding.action in (ValidationAction.REDACT, ValidationAction.BLOCK):
                category_tag = finding.category.upper()
                replacement = f"[REDACTED_{category_tag}]"
                redacted = redacted[:finding.start_position] + replacement + redacted[finding.end_position:]

        return redacted

    def _log_validation(self, result: ValidationResult) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "validate",
            "validation_id": result.validation_id,
            "is_valid": result.is_valid,
            "finding_count": len(result.findings),
            "blocked": result.should_block,
            "categories": list(set(f.category for f in result.findings)),
            "max_severity": max(
                (f.severity.value for f in result.findings), default="none"
            ),
        }
        self._audit_log.append(entry)

    def get_summary(self) -> dict:
        """Return a summary of the validator state."""
        categories = set(r.category for r in self._rules)
        return {
            "total_rules": len(self._rules),
            "categories": sorted(categories),
            "audit_log_entries": len(self._audit_log),
        }
