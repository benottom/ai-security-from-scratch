# Assurance Case: RAG Assistant

## 1. System Description

### 1.1 System Overview

The RAG Assistant is an AI-powered question-answering system that retrieves information from a document knowledge base and generates responses using a Large Language Model (LLM). It is used by employees across three roles (guest, employee, admin) to access company information.

### 1.2 System Boundary

| Component         | In Scope | Notes                                |
|-------------------|----------|--------------------------------------|
| LLM API           | Yes      | External API (OpenAI GPT-4)          |
| RAG Pipeline      | Yes      | Vector store + retrieval + embedding |
| Web Frontend      | Yes      | User-facing chat interface           |
| API Gateway       | Yes      | Request routing and auth             |
| Document Storage  | Yes      | Source documents for RAG             |
| Network Infrastructure | No  | Managed by IT operations            |
| End-user Devices  | No       | Outside system boundary              |

### 1.3 Control Loop Model

```
Reference Signal: User query + system instructions
    │
    ▼
Controller (LLM): Generates responses using retrieved context
    │
    ▼
Plant: Document knowledge base + external APIs
    │
    ▼
Actuators: Tool calls (web_search, read_file, send_email)
    │
    ▼
Sensors: User feedback, retrieval results, API responses
    │
    ▼
Disturbances: Adversarial inputs, poisoned documents, prompt injection
```

---

## 2. Security Goals

| ID   | Goal                                              | Priority |
|------|---------------------------------------------------|----------|
| G-01 | System instructions cannot be overridden by user input | Critical |
| G-02 | Users can only access documents they are authorized for | Critical |
| G-03 | Tool calls are validated and approved before execution | Critical |
| G-04 | Output does not contain secrets, PII, or policy-violating content | Critical |
| G-05 | System memory/state is not corrupted by adversarial inputs | High |
| G-06 | All security-relevant events are logged for audit | High |

---

## 3. Argument Structure

### 3.1 Goal G-01: Input Integrity

**Claim**: System instructions cannot be overridden by user input.

**Argument**: The Context Firewall separates system instructions (TRUSTED) from user input (UNTRUSTED) and quarantines content with high injection scores. When compiled into the LLM prompt, trusted and untrusted segments are clearly delineated with boundary markers.

**Evidence**:
- Context Firewall unit tests: 24/24 passing
  - Injection detection: 8/8 known injection patterns correctly quarantined
  - Benign input: 4/4 correctly passed through
  - Cross-contamination: 0 warnings on clean input
- Prompt injection eval suite: 8/10 passing
  - Direct injection: 3/3 blocked
  - Context manipulation: 3/3 blocked
  - Indirect injection: 2/4 blocked (known gap: base64-encoded, document-embedded)

**Residual Risk**: Indirect injection through encoded content and document-embedded instructions. Mitigation: add encoding detection and increase document trust scoring.

### 3.2 Goal G-02: Access Control

**Claim**: Users can only access documents they are authorized for.

**Argument**: The Permission-Aware RAG system tags every document with an access level (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED) and filters retrieval results based on the user's role. The policy engine enforces additional role-based restrictions.

**Evidence**:
- Permission RAG unit tests: 18/18 passing
  - Guest: only PUBLIC documents returned
  - Employee: PUBLIC + INTERNAL documents returned
  - Admin: all documents returned
  - Access denied events: properly logged
- RAG poisoning eval suite: 7/8 passing
  - Document injection: blocked
  - Privilege escalation via document claims: 1/2 blocked (known gap: document claims override ACL)

**Residual Risk**: Document content claiming to override access controls. Mitigation: enforce ACLs regardless of document content.

### 3.3 Goal G-03: Tool Safety

**Claim**: Tool calls are validated and approved before execution.

**Argument**: The Secure Tool Gateway registers all tools with risk classifications, validates parameters against schemas, enforces rate limits, and requires human approval for HIGH and CRITICAL risk tools.

**Evidence**:
- Tool Gateway unit tests: 22/22 passing
  - Low-risk tools: auto-allowed
  - High-risk tools: require approval
  - Critical tools: always require approval
  - Parameter validation: SQL injection, path traversal blocked
  - Rate limiting: enforced correctly
- Tool abuse eval suite: 8/8 passing
  - Unauthorized tool access: denied
  - Parameter manipulation: blocked
  - Privilege escalation: denied

**Residual Risk**: None identified in current threat model.

### 3.4 Goal G-04: Output Safety

**Claim**: Output does not contain secrets, PII, or policy-violating content.

**Argument**: The Output Validator checks LLM outputs against 16+ built-in rules covering secrets (API keys, tokens, connection strings) and PII (SSN, credit cards, email). Blocked content is not delivered; PII is redacted.

**Evidence**:
- Output Validator unit tests: 20/20 passing
  - API key detection: 4/4 patterns detected
  - PII detection: SSN, credit card, email, phone detected
  - Redaction: working correctly
  - Custom rules: functional
- Data leakage eval suite: 7/8 passing
  - Secret disclosure: blocked
  - PII disclosure: blocked
  - System prompt leak: blocked
  - Cross-turn PII leakage: 1/2 (known gap)

**Residual Risk**: Cross-turn PII leakage. Mitigation: implement session-level PII tracking.

### 3.5 Goal G-05: State Integrity

**Claim**: System memory/state is not corrupted by adversarial inputs.

**Argument**: The Memory Quarantine system requires all new memories to start in quarantine with trust_score=0.0. Memories must be validated and reach a promotion threshold (0.7) before being stored as trusted. Compromised memories can be demoted.

**Evidence**:
- Memory Quarantine unit tests: 18/18 passing
  - New memories: quarantined
  - Promotion: after sufficient validation
  - Demotion: when trust drops
  - Expiration: quarantined memories cleaned up

**Residual Risk**: Trust scoring is numeric and may not capture semantic corruption. Mitigation: add semantic validators.

### 3.6 Goal G-06: Audit Trail

**Claim**: All security-relevant events are logged for audit.

**Argument**: The Control Ledger is an append-only, hash-chained event store. Every defense decision (allow, deny, require_approval) is recorded with full context, and the hash chain ensures tamper detection.

**Evidence**:
- Control Ledger unit tests: 16/16 passing
  - Hash chaining: verified
  - Integrity verification: detects tampering
  - Query: filtering works correctly
  - File I/O: read/write works correctly

**Residual Risk**: Ledger is file-based; production should use database-backed storage with encryption at rest.

---

## 4. Assumptions

| ID   | Assumption | Justification |
|------|-----------|---------------|
| A-01 | Attackers cannot access the server infrastructure | Network security controls in place |
| A-02 | LLM provider (OpenAI) does not maliciously modify model behavior | Contractual SLA and monitoring |
| A-03 | Document access levels are correctly assigned | Periodic ACL audits |
| A-04 | Human approvers do not approve malicious tool calls | Approval process includes context review |
| A-05 | Eval test cases represent realistic attack scenarios | Based on OWASP LLM Top 10 and published research |

---

## 5. Eval Results Summary

| Suite | Pass Rate | Critical Failures | Status |
|-------|-----------|-------------------|--------|
| Prompt Injection | 80% | 1 | Partial Pass |
| RAG Poisoning | 87.5% | 1 | Partial Pass |
| Tool Abuse | 100% | 0 | Pass |
| Data Leakage | 87.5% | 0 | Pass |
| **Overall** | **88.2%** | **2** | **Conditional Pass** |

---

## 6. Conclusion

The RAG Assistant implements defense-in-depth security controls that provide strong protection against most known AI attack vectors. The assurance case is supported by unit test evidence (118/118 passing) and eval harness results (88.2% overall pass rate).

Two critical-severity gaps have been identified:
1. **Indirect injection through documents** (PI-004): Add context-level trust tagging for retrieved documents
2. **Document-based privilege escalation** (RP-004): Enforce ACLs regardless of document content claims

These gaps are tracked in the risk register and have active mitigation plans.

**Assurance Statement**: The RAG Assistant provides adequate security for deployment in an internal corporate environment, provided the two critical gaps are addressed within 30 days and the system is continuously monitored through the control ledger and eval harness.
