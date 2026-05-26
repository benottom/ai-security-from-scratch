# Sample Risk Register — AI Assistant System

## System Information

| Field | Value |
|---|---|
| System Name | Corporate RAG Assistant |
| Version | 2.1.0 |
| Assessment Date | 2025-01-15 |
| Assessor | Security Team |
| Risk Owner | VP of Engineering |

---

## Risk Register

### R-001: Direct Prompt Injection Bypass

| Field | Value |
|---|---|
| **ID** | R-001 |
| **Category** | Input Integrity |
| **Description** | Attacker crafts input that bypasses the context firewall's injection detection, causing the LLM to follow injected instructions instead of system instructions |
| **OWASP LLM Top 10** | LLM01: Prompt Injection |
| **Likelihood** | 4 (Likely) |
| **Impact** | 4 (Major) |
| **Risk Score** | 16 (High) |
| **Current Controls** | Context Firewall with injection threshold 0.5; Policy Engine with content filter rules |
| **Control Gap** | Novel injection patterns not covered by regex detection; indirect injection through retrieved documents |
| **Mitigation Plan** | (1) Add semantic injection detection using embedding similarity; (2) Increase context firewall trust-level enforcement; (3) Run prompt injection eval suite weekly |
| **Owner** | ML Platform Team |
| **Status** | Open |
| **Target Date** | 2025-02-15 |
| **Review Date** | 2025-02-01 |

### R-002: Unauthorized Document Access

| Field | Value |
|---|---|
| **ID** | R-002 |
| **Category** | Access Control |
| **Description** | User accesses documents beyond their authorized access level through the RAG system, either through misconfigured ACLs or through the LLM revealing information from authorized documents in an unauthorized context |
| **OWASP LLM Top 10** | LLM02: Sensitive Information Disclosure |
| **Likelihood** | 3 (Possible) |
| **Impact** | 4 (Major) |
| **Risk Score** | 12 (High) |
| **Current Controls** | Permission-Aware RAG with role-based document access; Policy Engine with data access rules |
| **Control Gap** | Role mapping may be incomplete; LLM may synthesize restricted information from authorized fragments |
| **Mitigation Plan** | (1) Audit all document ACLs quarterly; (2) Add output-level access control checks; (3) Implement differential privacy for sensitive aggregations |
| **Owner** | Data Governance Team |
| **Status** | Open |
| **Target Date** | 2025-03-01 |
| **Review Date** | 2025-02-15 |

### R-003: Secret/PII Leakage in Output

| Field | Value |
|---|---|
| **ID** | R-003 |
| **Category** | Data Leakage |
| **Description** | LLM output contains API keys, credentials, PII, or other sensitive information that should have been redacted or blocked |
| **OWASP LLM Top 10** | LLM02: Sensitive Information Disclosure |
| **Likelihood** | 3 (Possible) |
| **Impact** | 5 (Catastrophic) |
| **Risk Score** | 15 (High) |
| **Current Controls** | Output Validator with 16+ built-in rules; Security Gateway with output validation pipeline |
| **Control Gap** | Regex-based detection misses obfuscated or rephrased secrets; no cross-turn PII tracking |
| **Mitigation Plan** | (1) Add NER-based PII detection as secondary validator; (2) Implement session-level PII tracking; (3) Run data leakage eval suite after every model update |
| **Owner** | Security Team |
| **Status** | Open |
| **Target Date** | 2025-02-28 |
| **Review Date** | 2025-02-10 |

### R-004: Destructive Tool Call Without Approval

| Field | Value |
|---|---|
| **ID** | R-004 |
| **Category** | Tool Safety |
| **Description** | LLM triggers a destructive tool (delete_database, format_disk) without proper human approval, either through tool gateway bypass or social engineering the approver |
| **OWASP LLM Top 10** | LLM06: Excessive Agency |
| **Likelihood** | 2 (Unlikely) |
| **Impact** | 5 (Catastrophic) |
| **Risk Score** | 10 (Medium) |
| **Current Controls** | Secure Tool Gateway with risk classification and approval workflow; Policy Engine with tool call rules |
| **Control Gap** | Approval bypass through parameter manipulation; social engineering of approvers |
| **Mitigation Plan** | (1) Add secondary authentication for critical tool approval; (2) Implement tool call confirmation with context display; (3) Run tool abuse eval suite monthly |
| **Owner** | Platform Security Team |
| **Status** | Open |
| **Target Date** | 2025-03-15 |
| **Review Date** | 2025-03-01 |

### R-005: RAG Document Poisoning

| Field | Value |
|---|---|
| **ID** | R-005 |
| **Category** | Input Integrity |
| **Description** | Malicious content injected into the document knowledge base influences LLM behavior when retrieved, causing incorrect or harmful outputs |
| **OWASP LLM Top 10** | LLM04: Data and Model Poisoning |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 (Medium) |
| **Current Controls** | Context Firewall with trust-level tagging; Memory Quarantine for new data |
| **Control Gap** | No document trust scoring; no cross-reference validation of retrieved content |
| **Mitigation Plan** | (1) Implement document provenance tracking; (2) Add cross-reference validation in memory quarantine; (3) Run RAG poisoning eval suite after document updates |
| **Owner** | Data Engineering Team |
| **Status** | Open |
| **Target Date** | 2025-03-31 |
| **Review Date** | 2025-03-15 |

### R-006: Cross-Turn PII Leakage

| Field | Value |
|---|---|
| **ID** | R-006 |
| **Category** | PII Protection |
| **Description** | PII is extracted across multiple conversation turns, with each turn revealing a small piece until the full PII is assembled |
| **OWASP LLM Top 10** | LLM02: Sensitive Information Disclosure |
| **Likelihood** | 3 (Possible) |
| **Impact** | 4 (Major) |
| **Risk Score** | 12 (High) |
| **Current Controls** | Output Validator with PII detection |
| **Control Gap** | No session-level PII tracking; individual turns may pass PII checks but cumulative effect leaks data |
| **Mitigation Plan** | (1) Implement session-level PII budget; (2) Track PII categories across conversation turns; (3) Add aggregate leakage detection |
| **Owner** | Security Team |
| **Status** | Open |
| **Target Date** | 2025-03-01 |
| **Review Date** | 2025-02-15 |

### R-007: System Prompt Extraction

| Field | Value |
|---|---|
| **ID** | R-007 |
| **Category** | Confidentiality |
| **Description** | Attacker uses creative prompting techniques to extract the system prompt, revealing internal instructions, tool descriptions, or security configurations |
| **OWASP LLM Top 10** | LLM07: System Prompt Leakage |
| **Likelihood** | 4 (Likely) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 12 (High) |
| **Current Controls** | Context Firewall isolates system prompt; Output Validator detects prompt leak patterns |
| **Control Gap** | Creative extraction techniques (poems, analogies) bypass pattern matching |
| **Mitigation Plan** | (1) Add semantic similarity detection for system prompt content in output; (2) Remove sensitive information from system prompts; (3) Run system prompt leak tests regularly |
| **Owner** | Security Team |
| **Status** | Open |
| **Target Date** | 2025-02-28 |
| **Review Date** | 2025-02-15 |

### R-008: Memory State Corruption

| Field | Value |
|---|---|
| **ID** | R-008 |
| **Category** | State Integrity |
| **Description** | Adversarial inputs are stored as trusted memories, persistently influencing future LLM behavior across sessions |
| **OWASP LLM Top 10** | LLM04: Data and Model Poisoning |
| **Likelihood** | 2 (Unlikely) |
| **Impact** | 4 (Major) |
| **Risk Score** | 8 (Medium) |
| **Current Controls** | Memory Quarantine with trust scoring and promotion threshold |
| **Control Gap** | Numeric trust scoring doesn't capture semantic corruption; validators may not detect subtle manipulation |
| **Mitigation Plan** | (1) Add semantic validators that check memory consistency; (2) Implement periodic memory audit; (3) Reduce quarantine TTL for high-risk sources |
| **Owner** | ML Platform Team |
| **Status** | Open |
| **Target Date** | 2025-04-01 |
| **Review Date** | 2025-03-15 |

---

## Risk Summary

| Risk Level | Count | IDs |
|---|---|---|
| Critical (20-25) | 0 | — |
| High (12-19) | 5 | R-001, R-002, R-003, R-006, R-007 |
| Medium (6-11) | 3 | R-004, R-005, R-008 |
| Low (1-5) | 0 | — |

## Top Priority Actions

1. **R-003 (Secret/PII Leakage)**: Highest impact score; implement NER-based PII detection
2. **R-001 (Prompt Injection Bypass)**: Most likely to occur; add semantic injection detection
3. **R-006 (Cross-Turn PII Leakage)**: Gap in current defenses; implement session-level tracking
