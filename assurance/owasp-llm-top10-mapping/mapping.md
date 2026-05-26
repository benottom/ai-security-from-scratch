# OWASP LLM Top 10 Mapping — AI Security Controls

## Overview

This document maps AI security controls from "AI Security from Scratch" to the OWASP Top 10 for Large Language Model Applications (2025). Each OWASP risk is matched with the specific defenses that mitigate it, along with implementation details and evidence sources.

---

## Mapping Table

### LLM01: Prompt Injection

**Risk**: User input manipulates LLM behavior by injecting malicious instructions that override system prompts.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Context Firewall | Input Filter | Separates trusted system instructions from untrusted user input; quarantines injection attempts | Firewall quarantine logs, injection detection tests |
| Policy Engine | Reference Governor | Content filter rules block known injection patterns; policy evaluation denies injection-like inputs | Policy eval results, injection rule matches |
| Security Gateway | Unified Gateway | Input validation stage detects and blocks injection attempts before they reach the LLM | Gateway block logs |
| Memory Quarantine | State Filter | Prevents injection from persisting through memory; adversarial inputs stored in quarantine | Quarantine records |

**Eval Coverage**: Prompt Injection suite (10 test cases) — covers direct injection, indirect injection, and context manipulation.

---

### LLM02: Sensitive Information Disclosure

**Risk**: LLM inadvertently reveals sensitive data, PII, or system information in its outputs.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Output Validator | Output Filter | Detects secrets (API keys, tokens, connection strings) and PII (SSN, credit cards) in outputs | Validation findings, redaction logs |
| Policy Engine | Reference Governor | Output check rules prevent disclosure of sensitive information patterns | Policy eval results |
| Security Gateway | Unified Gateway | Output validation stage blocks or redacts sensitive content before delivery | Gateway modification logs |
| Permission-RAG | Feedforward Filter | Prevents retrieval of documents the user isn't authorized to access | RAG access denied logs |

**Eval Coverage**: Data Leakage suite (8 test cases) — covers secret disclosure, PII disclosure, and system prompt leaks.

---

### LLM03: Supply Chain Vulnerabilities

**Risk**: Vulnerabilities in training data, model weights, or third-party components.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| AI-BOM Template | Inventory | Documents all supply chain components (models, data, dependencies) | Completed AI-BOM |
| Memory Quarantine | State Filter | Validates all external inputs before incorporating into trusted state | Quarantine validation logs |
| Policy Engine | Reference Governor | Policies can restrict which external sources are trusted | Policy configuration |

**Eval Coverage**: Partially covered by RAG Poisoning suite (8 test cases) — covers document-level supply chain attacks.

---

### LLM04: Data and Model Poisoning

**Risk**: Malicious actors manipulate training data or fine-tuning data to introduce backdoors or bias.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Memory Quarantine | State Filter | All new data starts in quarantine; must be validated before promotion | Quarantine records, promotion logs |
| Permission-RAG | Feedforward Filter | Document access controls limit what can be injected into the knowledge base | RAG access logs |
| Policy Engine | Reference Governor | Content filter rules detect poisoning patterns in retrieved data | Policy eval results |

**Eval Coverage**: RAG Poisoning suite (8 test cases) — covers document injection, data manipulation, and privilege escalation via poisoned data.

---

### LLM05: Improper Output Handling

**Risk**: LLM output is not properly validated before being passed to downstream systems, enabling XSS, SSRF, or code execution.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Output Validator | Output Filter | Validates outputs for dangerous content, code, and injection patterns | Validation findings |
| Security Gateway | Unified Gateway | Output validation pipeline catches dangerous outputs before delivery | Gateway block logs |
| Tool Gateway | Actuator Filter | Parameter validation prevents injection through tool parameters | Parameter validation results |

**Eval Coverage**: Data Leakage suite and Tool Abuse suite.

---

### LLM06: Excessive Agency

**Risk**: LLM system has too much autonomy, allowing it to perform actions beyond its intended scope.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Tool Gateway | Actuator Filter | Risk classification limits tool access; approval required for high-risk tools | Gateway approval logs |
| Policy Engine | Reference Governor | Tool call policies restrict which tools can be used and by whom | Policy eval results |
| Security Gateway | Unified Gateway | Policy check stage enforces tool permissions | Gateway deny logs |

**Eval Coverage**: Tool Abuse suite (8 test cases) — covers unauthorized tool access, parameter manipulation, and privilege escalation.

---

### LLM07: System Prompt Leakage

**Risk**: System prompts or instructions are exposed through model outputs.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Context Firewall | Input Filter | System instructions isolated in TRUSTED segments; not mixed with user input | Firewall boundary markers |
| Output Validator | Output Filter | Detects system prompt patterns in output (e.g., "system prompt:", "you are a helpful") | Validation findings |
| Policy Engine | Reference Governor | Output check rules block system prompt disclosure patterns | Policy eval results |

**Eval Coverage**: Data Leakage suite (test cases DL-005, DL-006) — covers system prompt extraction.

---

### LLM08: Vector and Embedding Weaknesses

**Risk**: Vulnerabilities in vector store or embedding mechanisms allow data poisoning or unauthorized access.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Permission-RAG | Feedforward Filter | Access control on vector store documents; retrieval filtered by authorization | RAG access logs |
| Memory Quarantine | State Filter | RAG outputs validated before being incorporated into context | Quarantine records |
| Policy Engine | Reference Governor | Content filter rules scan retrieved content for injection patterns | Policy eval results |

**Eval Coverage**: RAG Poisoning suite (8 test cases).

---

### LLM09: Misinformation

**Risk**: LLM generates false, inaccurate, or misleading content.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Memory Quarantine | State Filter | Cross-referencing validators check memory consistency | Validation history |
| Policy Engine | Reference Governor | Policies can require source citations or confidence indicators | Policy configuration |
| Control Ledger | Observer Record | Audit trail enables post-hoc verification of generated content | Ledger events |

**Eval Coverage**: Partially covered by RAG Poisoning suite (data manipulation test cases).

---

### LLM10: Unbounded Consumption

**Risk**: Resource exhaustion through excessive input, output, or API usage.

| Defense | Control Type | How It Mitigates | Evidence |
|---|---|---|---|
| Tool Gateway | Actuator Filter | Rate limiting on tool calls per minute | Rate limit logs |
| Context Firewall | Input Filter | Max segments limit prevents context overflow | Firewall capacity limits |
| Security Gateway | Unified Gateway | Input size limits and rate limiting | Gateway configuration |

**Eval Coverage**: Partially covered by Tool Abuse suite (rate limit test cases).

---

## Coverage Summary

| OWASP LLM Top 10 Risk | Primary Defense | Eval Coverage | Status |
|---|---|---|---|
| LLM01: Prompt Injection | Context Firewall | ✅ 10 test cases | Strong |
| LLM02: Sensitive Info Disclosure | Output Validator | ✅ 8 test cases | Strong |
| LLM03: Supply Chain | AI-BOM, Memory Quarantine | ⚠️ Partial | Moderate |
| LLM04: Data/Model Poisoning | Memory Quarantine | ✅ 8 test cases | Strong |
| LLM05: Improper Output Handling | Output Validator | ✅ Partial coverage | Moderate |
| LLM06: Excessive Agency | Tool Gateway | ✅ 8 test cases | Strong |
| LLM07: System Prompt Leakage | Context Firewall | ✅ 2 test cases | Moderate |
| LLM08: Vector/Embedding | Permission-RAG | ✅ 8 test cases | Strong |
| LLM09: Misinformation | Memory Quarantine | ⚠️ Partial | Moderate |
| LLM10: Unbounded Consumption | Tool Gateway | ⚠️ Partial | Moderate |

**Overall**: Strong coverage for the top 6 risks; moderate coverage for supply chain, misinformation, and resource consumption risks.
