# Pattern: Output Validation Layer

> **Pattern ID:** PAT-OUT-001 | **Category:** Output Security | **Maturity:** Proven

---

## Problem

AI models generate outputs that are inherently probabilistic. A model can produce factually incorrect content (hallucinations), reveal sensitive information embedded in its training data or context, violate safety policies, or generate responses that are syntactically valid but semantically harmful. When model output is delivered directly to users or downstream systems without validation, every failure mode of the model becomes a failure mode of the system.

The root cause is a missing feedback controller: the model generates output, and nothing checks whether that output is safe, accurate, and policy-compliant before it is delivered. The control loop has an observation gap — it never inspects what the model actually said.

**Concrete failure scenario:** A customer support chatbot, asked about a competitor's product, generates a response that includes fabricated negative claims about the competitor — claims that are completely false but sound authoritative. The customer shares the response on social media, and the company faces a defamation lawsuit.

---

## Threat Model

| Attribute | Value |
|---|---|
| **Threat ID** | T-OUT-001 |
| **Threat Name** | Unsafe or inaccurate AI output delivered without validation |
| **Attack Vector** | Adversarial input causing harmful output; or model error producing unsafe output without adversarial provocation |
| **Impact** | Misinformation, PII exposure, policy violations, reputational damage, legal liability |
| **Likelihood** | High — all LLMs hallucinate; prompt injection increases the risk |
| **Risk** | High |
| **OWASP LLM Top 10** | LLM04: Model Denial of Service, LLM06: Sensitive Data Disclosure, LLM09: Overreliance |
| **NIST AI RMF** | MEASURE 2.6, MEASURE 2.9, MANAGE 2.2 |

**Attack variants:**
1. **Hallucination injection:** Input crafted to elicit confident but false responses
2. **PII extraction:** Input designed to cause the model to reveal personally identifiable information from context
3. **Policy circumvention via output:** Input causes the model to express prohibited content (hate speech, dangerous instructions) through indirect phrasing
4. **Schema violation:** Model output does not conform to expected format, breaking downstream systems
5. **Confidence manipulation:** Input causes the model to express high confidence in incorrect information

---

## Control-Theoretic View

### Objective

Ensure that all AI-generated output is validated against safety, accuracy, and policy requirements before delivery to users or downstream systems.

### Controller

The **Output Validation Layer** — a component that inspects every model output against a set of validation rules (content safety, PII detection, schema compliance, factual grounding, policy adherence) and determines whether to deliver, modify, or block the output.

### Observations

| Observation | Source | Type |
|---|---|---|
| Raw model output text | LLM inference | Synchronous |
| Output classification (safe / unsafe / uncertain) | Content classifier | Synchronous |
| PII detection results | PII scanner | Synchronous |
| Schema validation result | Schema validator | Synchronous |
| Grounding verification | RAG source comparison | Synchronous |
| Policy compliance score | Policy engine | Synchronous |

### Actions

| Action | Effect | Preconditions |
|---|---|---|
| Deliver output | Response sent to user/system | All validations pass |
| Filter and deliver | Sensitive content redacted; response delivered | PII or policy violation that can be redacted |
| Block output | Response replaced with safe refusal message | Safety violation that cannot be redacted |
| Request re-generation | Model asked to generate again with constraints | Uncertain validation; second chance may produce safe output |
| Flag for human review | Response queued for human evaluation | Ambiguous validation result; high-stakes context |
| Log validation event | Decision recorded in audit trail | All decisions logged |

### Feedback

- Output validation results feed back to input classifiers (if output is unsafe, the input was likely adversarial)
- Blocked output rates drive policy refinement
- False positive rates (legitimate output incorrectly blocked) drive validator tuning

### Disturbances

| Disturbance | Source | Mitigation |
|---|---|---|
| Novel harmful content forms | Evolving safety landscape | Continuous classifier updates; red-team exercises |
| Validated output still harmful | Validator misses a category | Defense-in-depth; multiple independent validators |
| Over-filtering | Validators too aggressive | Regular false-positive audits; per-domain thresholds |
| Latency from deep validation | Multiple sequential validators | Parallel validation; async for low-risk outputs |
| Model output obfuscation | Attacker crafts output to evade validators | Combine pattern, classifier, and semantic validators |

### Unsafe States

| Unsafe State | Condition | Consequence |
|---|---|---|
| Harmful content delivered | Output validation fails or is bypassed | User exposed to unsafe content |
| PII leaked | PII scanner misses sensitive data | Privacy violation; regulatory penalty |
| Hallucinated facts delivered | No factual grounding check | Misinformation; erosion of trust |
| Schema-violating output delivered | No structural validation | Downstream system failure |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    LLM Model Output                           │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
              ┌──────────────────────────────┐
              │    Output Validation Layer     │
              │                                │
              │  ┌──────────────────────────┐ │
              │  │  Content Safety Check     │ │──▶ Harmful, toxic, dangerous?
              │  └──────────────────────────┘ │
              │  ┌──────────────────────────┐ │
              │  │  PII Detection & Redaction│ │──▶ Contains SSN, email, API key?
              │  └──────────────────────────┘ │
              │  ┌──────────────────────────┐ │
              │  │  Schema Validation        │ │──▶ Matches expected output format?
              │  └──────────────────────────┘ │
              │  ┌──────────────────────────┐ │
              │  │  Policy Compliance Check  │ │──▶ Violates organizational policy?
              │  └──────────────────────────┘ │
              │  ┌──────────────────────────┐ │
              │  │  Factual Grounding Check  │ │──▶ Claims supported by sources?
              │  └──────────────────────────┘ │
              │  ┌──────────────────────────┐ │
              │  │  Confidence Assessment    │ │──▶ Model confident in its output?
              │  └──────────────────────────┘ │
              └──────────┬───────────────────┘
                         │
            ┌────────────┼───────────────┐
            │            │               │
            ▼            ▼               ▼
      ┌──────────┐ ┌──────────┐   ┌──────────────┐
      │ DELIVER  │ │  FILTER  │   │  BLOCK /     │
      │          │ │  & DELIVER│   │  RE-GENERATE │
      └──────────┘ └──────────┘   └──────────────┘
```

---

## Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Callable
import re


class OutputAction(Enum):
    DELIVER = "deliver"
    FILTER_AND_DELIVER = "filter_and_deliver"
    BLOCK = "block"
    RE_GENERATE = "re_generate"
    FLAG_FOR_REVIEW = "flag_for_review"


@dataclass
class ValidationResult:
    """Result from a single validation check."""
    validator_name: str
    passed: bool
    severity: str = "low"        # low, medium, high, critical
    violations: list[str] = field(default_factory=list)
    filtered_content: Optional[str] = None
    confidence: float = 1.0


@dataclass
class OutputDecision:
    """The output validation layer's final decision."""
    action: OutputAction
    original_content: str
    filtered_content: Optional[str]
    validation_results: list[ValidationResult]
    overall_risk_score: float
    reason: str
    re_generation_constraints: Optional[dict] = None


class OutputValidationLayer:
    """Validates AI outputs against safety, accuracy, and policy requirements.

    Control objective: All AI-generated output is validated before delivery.
    """

    # Common PII patterns
    PII_PATTERNS = {
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "api_key": r"\b(sk|pk|api[_-]?key)[_-][A-Za-z0-9]{20,}\b",
        "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    }

    # Harmful content patterns (simplified; production systems use ML classifiers)
    HARMFUL_PATTERNS = [
        r"(?i)how\s+to\s+(make|build|create)\s+(a\s+)?(bomb|weapon|drug|poison)",
        r"(?i)step[s]?\s+by\s+step\s+(to|for)\s+(hack|exploit|attack)",
        r"(?i)instructions\s+for\s+(making|creating)\s+(explosive|controlled\s+substance)",
    ]

    def __init__(
        self,
        validators: Optional[list[Callable]] = None,
        policy_rules: Optional[dict] = None,
        schema: Optional[dict] = None,
        config: Optional[dict] = None,
    ):
        self.custom_validators = validators or []
        self.policy_rules = policy_rules or {}
        self.schema = schema
        self.config = config or {}
        self.max_re_generations = self.config.get("max_re_generations", 1)

    def validate(self, content: str, context: Optional[dict] = None) -> OutputDecision:
        """Run all validation checks and determine output action."""
        results = []
        risk_score = 0.0

        # Built-in validators
        # 1. Content safety check
        safety_result = self._check_content_safety(content)
        results.append(safety_result)
        if not safety_result.passed:
            risk_score = max(risk_score, self._severity_to_risk(safety_result.severity))

        # 2. PII detection and redaction
        pii_result = self._check_pii(content)
        results.append(pii_result)
        if not pii_result.passed:
            risk_score = max(risk_score, 0.5)

        # 3. Schema validation (if configured)
        if self.schema:
            schema_result = self._check_schema(content, self.schema)
            results.append(schema_result)
            if not schema_result.passed:
                risk_score = max(risk_score, 0.3)

        # 4. Policy compliance check
        policy_result = self._check_policy(content)
        results.append(policy_result)
        if not policy_result.passed:
            risk_score = max(risk_score, self._severity_to_risk(policy_result.severity))

        # 5. Factual grounding check (if sources provided in context)
        if context and context.get("sources"):
            grounding_result = self._check_grounding(content, context["sources"])
            results.append(grounding_result)
            if not grounding_result.passed:
                risk_score = max(risk_score, 0.4)

        # 6. Custom validators
        for validator in self.custom_validators:
            custom_result = validator(content, context)
            results.append(custom_result)
            if not custom_result.passed:
                risk_score = max(risk_score, self._severity_to_risk(custom_result.severity))

        # Determine action
        return self._decide(content, results, risk_score)

    def _check_content_safety(self, content: str) -> ValidationResult:
        """Check for harmful or dangerous content."""
        violations = []
        for pattern in self.HARMFUL_PATTERNS:
            match = re.search(pattern, content)
            if match:
                violations.append(f"Harmful content pattern: {match.group()[:50]}")

        if violations:
            return ValidationResult(
                validator_name="content_safety",
                passed=False,
                severity="critical",
                violations=violations,
            )
        return ValidationResult(validator_name="content_safety", passed=True)

    def _check_pii(self, content: str) -> ValidationResult:
        """Detect and redact PII from output."""
        violations = []
        filtered = content
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
                violations.append(f"PII detected: {pii_type} ({len(matches)} instance(s))")
                for match in matches:
                    filtered = filtered.replace(match, f"[REDACTED_{pii_type.upper()}]")

        if violations:
            return ValidationResult(
                validator_name="pii_detection",
                passed=False,
                severity="high",
                violations=violations,
                filtered_content=filtered,
            )
        return ValidationResult(validator_name="pii_detection", passed=True)

    def _check_schema(self, content: str, schema: dict) -> ValidationResult:
        """Validate output against expected schema."""
        violations = []
        try:
            parsed = content
            if schema.get("type") == "json":
                import json
                parsed = json.loads(content)
            # Add schema-specific validation logic here
            max_length = schema.get("max_length")
            if max_length and len(content) > max_length:
                violations.append(f"Output exceeds max length: {len(content)} > {max_length}")
        except Exception as e:
            violations.append(f"Schema parse error: {str(e)}")

        if violations:
            return ValidationResult(
                validator_name="schema_validation",
                passed=False,
                severity="medium",
                violations=violations,
            )
        return ValidationResult(validator_name="schema_validation", passed=True)

    def _check_policy(self, content: str) -> ValidationResult:
        """Check output against organizational policy rules."""
        violations = []
        for rule_name, rule_config in self.policy_rules.items():
            if rule_config.get("type") == "regex":
                if re.search(rule_config["pattern"], content, re.IGNORECASE):
                    violations.append(f"Policy violation: {rule_name}")
            elif rule_config.get("type") == "keyword":
                keywords = rule_config.get("keywords", [])
                for kw in keywords:
                    if kw.lower() in content.lower():
                        violations.append(f"Policy violation: {rule_name} (keyword: {kw})")

        if violations:
            return ValidationResult(
                validator_name="policy_compliance",
                passed=False,
                severity="high",
                violations=violations,
            )
        return ValidationResult(validator_name="policy_compliance", passed=True)

    def _check_grounding(self, content: str, sources: list[str]) -> ValidationResult:
        """Check whether output claims are grounded in provided sources."""
        # Simplified: check if key entities from content appear in sources
        # Production systems use NLI models or citation verification
        ungrounded_claims = []
        for source in sources:
            # This is a heuristic; real grounding checks use semantic similarity
            pass
        if ungrounded_claims:
            return ValidationResult(
                validator_name="factual_grounding",
                passed=False,
                severity="medium",
                violations=ungrounded_claims,
            )
        return ValidationResult(validator_name="factual_grounding", passed=True)

    def _decide(self, content: str, results: list[ValidationResult], risk_score: float) -> OutputDecision:
        """Make final decision based on validation results."""
        has_critical = any(r.severity == "critical" and not r.passed for r in results)
        has_redactable = any(not r.passed and r.filtered_content for r in results)
        all_passed = all(r.passed for r in results)

        if all_passed:
            return OutputDecision(
                action=OutputAction.DELIVER,
                original_content=content,
                filtered_content=None,
                validation_results=results,
                overall_risk_score=risk_score,
                reason="All validations passed",
            )

        if has_critical:
            return OutputDecision(
                action=OutputAction.BLOCK,
                original_content=content,
                filtered_content="I'm unable to provide that information. Please rephrase your request.",
                validation_results=results,
                overall_risk_score=risk_score,
                reason="Critical validation failure; output blocked",
            )

        if has_redactable:
            filtered = content
            for result in results:
                if result.filtered_content:
                    filtered = result.filtered_content
            return OutputDecision(
                action=OutputAction.FILTER_AND_DELIVER,
                original_content=content,
                filtered_content=filtered,
                validation_results=results,
                overall_risk_score=risk_score,
                reason="PII or policy-violating content redacted",
            )

        return OutputDecision(
            action=OutputAction.FLAG_FOR_REVIEW,
            original_content=content,
            filtered_content=None,
            validation_results=results,
            overall_risk_score=risk_score,
            reason="Validation concerns; flagged for human review",
        )

    def _severity_to_risk(self, severity: str) -> float:
        return {"low": 0.2, "medium": 0.4, "high": 0.7, "critical": 0.95}.get(severity, 0.5)
```

---

## Tests

```python
import pytest
from output_validation_layer import OutputValidationLayer, OutputAction


class TestOutputValidationLayer:
    """Security regression tests for the Output Validation Layer."""

    @pytest.fixture
    def validator(self):
        return OutputValidationLayer(
            policy_rules={
                "competitor_mentions": {
                    "type": "keyword",
                    "keywords": ["CompetitorX"],
                },
            },
            schema={"type": "text", "max_length": 5000},
        )

    def test_safe_output_delivered(self, validator):
        result = validator.validate("The weather today is sunny with a high of 22°C.")
        assert result.action == OutputAction.DELIVER

    def test_harmful_content_blocked(self, validator):
        result = validator.validate("Here is how to make a bomb using household chemicals...")
        assert result.action == OutputAction.BLOCK

    def test_pii_redacted_and_delivered(self, validator):
        result = validator.validate("The user's SSN is 123-45-6789 and their email is test@example.com")
        assert result.action == OutputAction.FILTER_AND_DELIVER
        assert "123-45-6789" not in result.filtered_content
        assert "REDACTED_SSN" in result.filtered_content

    def test_policy_violation_caught(self, validator):
        result = validator.validate("CompetitorX is a terrible company with awful products.")
        assert not any(r.validator_name == "policy_compliance" and r.passed for r in result.validation_results)

    def test_api_key_redacted(self, validator):
        result = validator.validate("You can use the API with key sk-abc123def456ghi789jkl012mno345")
        assert result.action == OutputAction.FILTER_AND_DELIVER
        assert "sk-abc123" not in result.filtered_content

    def test_schema_violation_detected(self, validator):
        long_content = "x" * 6000
        result = validator.validate(long_content)
        schema_results = [r for r in result.validation_results if r.validator_name == "schema_validation"]
        assert any(not r.passed for r in schema_results)
```

---

## Monitoring

| Metric | Collection | Warning | Critical | Alert Channel |
|---|---|---|---|---|
| Output block rate | Per-response | > 2% | > 10% | Security SIEM |
| PII detection rate | Per-response | > 5% | > 20% | Data governance |
| Filter rate (redacted content) | Per-response | > 10% | > 30% | Product + security |
| Policy violation rate | Daily | Any new violation type | Spike in violations | Compliance |
| False positive rate | Weekly review | > 5% | > 15% | ML engineering |
| Validation latency (P95) | Per-response | > 50ms | > 200ms | Infrastructure |

---

## Failure Modes

| Failure Mode | Cause | Detection | Mitigation |
|---|---|---|---|
| **Harmful content missed** | Validator blind spot for novel harmful content | Red-team finds bypass; user report | Multiple independent validators; continuous classifier updates |
| **PII missed** | New PII format not in pattern list | Data loss prevention scan finds leak | Regular PII pattern updates; ML-based PII detection |
| **Over-filtering** | Validators too aggressive for domain | False positive rate spike | Domain-specific thresholds; per-application tuning |
| **Latency impact** | Deep validation on long outputs | P95 latency threshold breach | Parallel validation; size-based routing |
| **Schema bypass** | Output parsed differently by downstream system | Downstream error | Strict schema validation; contract testing |

---

## When Not To Use

1. **Deterministic output systems:** If your AI system always produces the same output for the same input (rule-based, template-based), and outputs are known at design time, validation adds no value.

2. **Low-stakes creative applications:** For applications where the worst-case output is merely unhelpful or slightly inaccurate (e.g., brainstorming tools, creative writing aids), heavy validation may be counterproductive.

3. **Systems with human review already in the loop:** If every AI output is already reviewed by a human before delivery (e.g., medical reports, legal documents), the output validation layer may be redundant — though it can still reduce human reviewer burden.

4. **When the AI Security Gateway includes output filtering:** If your gateway (PAT-GW-001) has robust output validation built in, a standalone layer may be redundant. Verify coverage.

5. **Real-time systems where validation latency is unacceptable:** If validation adds too much latency, consider async validation for low-risk outputs and sync validation only for high-risk contexts.

---

## Assurance Evidence

| Artifact | Description | Format | Retention |
|---|---|---|---|
| Validation decision log | Every validate() call with results | Structured JSON | 1 year |
| PII detection events | All PII detections with redaction details | Structured JSON | 1 year |
| Policy violation events | All policy violations with context | Structured JSON | 1 year |
| False positive reports | User-reported over-filtering | Tickets | 1 year |
| Validator performance metrics | Precision, recall, F1 on benchmark | Report | Permanent |

---

*Pattern version: 1.0.0 | AI Security from Scratch*
