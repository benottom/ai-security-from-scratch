# Risk Register — AI System

## Instructions

Use this template to track risks identified during AI security assessments. Each risk should be linked to specific controls, test evidence, and mitigation plans.

## Risk Scoring

### Likelihood Scale

| Level  | Score | Description |
|--------|-------|-------------|
| Rare   | 1     | Unlikely to occur |
| Unlikely | 2   | Could occur but not expected |
| Possible | 3   | Reasonable likelihood |
| Likely | 4     | More likely than not |
| Almost Certain | 5 | Expected to occur |

### Impact Scale

| Level  | Score | Description |
|--------|-------|-------------|
| Negligible | 1 | Minor effect, easily recoverable |
| Minor | 2     | Limited effect, some effort to recover |
| Moderate | 3   | Significant effect, substantial recovery effort |
| Major | 4      | Severe effect, major recovery effort |
| Catastrophic | 5 | System-wide failure, unrecoverable damage |

### Risk Matrix

| | Negligible (1) | Minor (2) | Moderate (3) | Major (4) | Catastrophic (5) |
|---|---|---|---|---|---|
| **Almost Certain (5)** | 5 | 10 | 15 | 20 | 25 |
| **Likely (4)** | 4 | 8 | 12 | 16 | 20 |
| **Possible (3)** | 3 | 6 | 9 | 12 | 15 |
| **Unlikely (2)** | 2 | 4 | 6 | 8 | 10 |
| **Rare (1)** | 1 | 2 | 3 | 4 | 5 |

### Risk Levels

| Score Range | Risk Level | Action Required |
|-------------|------------|-----------------|
| 20-25       | Critical   | Immediate mitigation required; escalate to leadership |
| 12-19       | High       | Mitigation plan required within 30 days |
| 6-11        | Medium     | Mitigation plan required within 90 days |
| 1-5         | Low        | Monitor; review at next assessment |

---

## Risk Register

| ID | Risk Description | Category | Likelihood | Impact | Risk Score | Risk Level | Current Controls | Control Gap | Mitigation Plan | Owner | Status | Review Date |
|----|-----------------|----------|------------|--------|------------|------------|------------------|-------------|-----------------|-------|--------|-------------|
| R-001 | Prompt injection bypasses system instructions | Input Integrity | 4 | 4 | 16 | High | Context Firewall | Does not catch all indirect injection | Add output monitoring | | Open | |
| R-002 | Unauthorized access to confidential documents via RAG | Access Control | 3 | 4 | 12 | High | Permission-Aware RAG | Role mapping incomplete | Audit role assignments | | Open | |
| R-003 | LLM outputs contain API keys or secrets | Data Leakage | 3 | 5 | 15 | High | Output Validator | Regex patterns may miss obfuscated secrets | Add semantic detection | | Open | |
| R-004 | Destructive tool call executed without approval | Tool Safety | 2 | 5 | 10 | Medium | Tool Gateway | Approval bypass possible | Add secondary auth | | Open | |
| R-005 | Poisoned RAG document influences model behavior | Input Integrity | 3 | 3 | 9 | Medium | Context Firewall, Policy Engine | Document trust not scored | Memory quarantine for RAG | | Open | |
| R-006 | PII leakage through multi-turn conversation | PII Protection | 3 | 4 | 12 | High | Output Validator | Cross-turn tracking missing | Session-level PII tracking | | Open | |
| R-007 | System prompt extraction via creative prompting | Confidentiality | 4 | 3 | 12 | High | Context Firewall | Creative extraction not covered | Add output pattern detection | | Open | |
| R-008 | Memory corruption through adversarial inputs | State Integrity | 2 | 4 | 8 | Medium | Memory Quarantine | Quarantine TTL too long | Reduce TTL, add validators | | Open | |

---

## Risk Trend Tracking

| Risk ID | Date | Likelihood | Impact | Score | Notes |
|---------|------|------------|--------|-------|-------|
| R-001 | | 4 | 4 | 16 | Initial assessment |
| R-001 | | 3 | 4 | 12 | After context firewall improvement |
| R-002 | | 3 | 4 | 12 | Initial assessment |
| R-002 | | 2 | 4 | 8 | After role mapping audit |
