# Indirect Prompt Injection

> **Module:** Phase 2 — Prompt Injection | **Class:** 09 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Define indirect prompt injection and explain why it is fundamentally harder to defend than direct injection
2. Demonstrate injection through external data sources including documents, web pages, and API responses
3. Analyze indirect injection as observation channel corruption where the controller receives poisoned sensor data
4. Implement data validation and context separation defenses for RAG and tool-augmented systems
5. Design monitoring systems that detect when retrieved content is influencing model behavior

---

## Control-Theoretic View

Every class in this curriculum models a security concept as a control loop. This section defines the control-theoretic framing for indirect prompt injection.

### Objective

The safety goal the system must maintain:

> Ensure that content retrieved from external data sources (documents, web pages, API responses) is treated as data to be processed, never as instructions to be followed, and that the model's behavior is governed exclusively by its system prompt regardless of what content is retrieved.

### Controller

The component responsible for making decisions to maintain the objective:

> The context separation firewall — a middleware layer that sits between the retrieval pipeline and the LLM context window, ensuring that retrieved content is structurally separated from system instructions, marked as untrusted data, and validated against instruction-injection patterns before being included in the model's input.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Retrieved content classification (data vs. instruction-like) | Content scanner | Per retrieval |
| Context window composition (system vs. user vs. retrieved ratios) | Context manager | Per request |
| Source trust level (curated internal vs. external web vs. user-uploaded) | Data provenance tracker | Per retrieval |
| Instruction-following fidelity after retrieval | Output classifier | Per response |
| Retrieval-to-output influence score | Attribution tracker | Per response |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Sanitize retrieved content | Strip instruction-like patterns from retrieved text | Instruction-like content detected in retrieval results |
| Tag retrieved content as untrusted | Wrap retrieved text in delimiters with explicit data markers | Any retrieval occurs |
| Reduce retrieval influence | Limit the amount of retrieved content included in context | High influence score detected |
| Block retrieval source | Stop including content from flagged sources | Source trust level is "untrusted" or "compromised" |
| Alert on anomalous retrieval | Notify monitoring that retrieved content may be adversarial | Unusual patterns in retrieved content |

### Feedback

How the controller learns whether its actions achieved the objective:

> Post-generation attribution analysis determines whether the model's output was influenced by retrieved content in ways that override system instructions. When attribution reveals retrieval-driven instruction override, the source is flagged and the content scanner is updated with the attack pattern. Trend analysis on retrieval-influence scores feeds back into source trust calibration.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Malicious documents in RAG corpus | Compromised data pipeline or adversary with upload access | Document validation + provenance tracking |
| Adversarial web pages fetched by browsing tool | Public internet | Source trust levels + content scanning |
| Compromised API responses from third-party tools | Supply chain attack | Response validation + anomaly detection |
| User-uploaded files with hidden instructions | Malicious user | Upload validation + content scanning |
| Data poisoning in training corpus for embeddings | Long-term supply chain attack | Embedding quality monitoring |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Retrieved instructions override system prompt | Model follows instructions found in retrieved documents | Attacker controls model via data source |
| Tool response injection | Model follows instructions in API responses | Attacker controls model via tool output |
| Data exfiltration via retrieval | Model sends sensitive data to attacker-controlled URLs | Data breach |
| Retrieval-guided harmful output | Model produces harmful content because retrieved content instructed it | Safety policy violation |
| Persistent behavioral shift | Repeated retrieval of adversarial content shifts model baseline | Long-term compromise |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> An output attribution layer that independently analyzes every model response to determine whether it was influenced by retrieved content in policy-violating ways. This layer operates outside the generation process and can block responses where retrieval-driven influence exceeds acceptable thresholds. Additionally, a source reputation system that progressively degrades the trust level of sources whose content is repeatedly associated with suspicious outputs.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Instruction-like content rate in retrieved documents | > 5% of retrieved chunks | Warning to data team |
| Retrieval-to-output influence score | > 0.7 for any response | Critical alert |
| Source trust degradation rate | > 2 sources degraded per week | Warning to security team |
| Retrieval-driven policy violation rate | > 0.1% of responses | Critical alert |
| Untrusted source query rate | > 20% of queries hit untrusted sources | Warning to data team |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Immediately block the offending data source and purge its content from the retrieval cache
2. Assess what instructions the model followed from the corrupted source and what actions resulted
3. Review and re-validate all content from the affected source
4. Update the content scanner with the new injection pattern
5. Run security regression tests with the new attack pattern
6. Document the incident and generate an evidence package

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 9a | Injection Through RAG Documents | 40 minutes |
| Lab 9b | Building a Context Separation Firewall | 50 minutes |
| Lab 9c | Source Trust and Content Validation | 30 minutes |

Each lab follows the standard 8-step flow:

1. Start the vulnerable application
2. Run a normal test to establish baseline behavior
3. Execute the attack
4. Observe the failure
5. Explain the control-loop failure
6. Implement the defense
7. Run the security regression test
8. Generate evidence

---

## Deliverables

- [ ] Completed lab worksheet documenting indirect injection attacks and their control-loop analysis
- [ ] Working context separation firewall implementation
- [ ] Source trust scoring system with content validation
- [ ] Passing security regression test suite (minimum 5 test cases)
- [ ] Evidence artifacts from `make evidence`

---

## Estimated Time

| Activity | Duration |
|---|---|
| Lecture / Reading | 1.0 hours |
| Lab Work | 1.5 hours |
| Exercises | 1.0 hours |
| Review & Deliverables | 0.5 hours |
| **Total** | **4.0 hours** |

---

## Prerequisites

- Completion of Class 07: Direct Prompt Injection and Class 08: System Prompt Leakage
- Familiarity with RAG architecture and retrieval pipelines
- Working development environment (see setup guide)

---

## References

1. Greshake, K., et al. (2023). "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"
2. OWASP Top 10 for LLM Applications (2025) — LLM01: Prompt Injection (indirect variant)
3. Abdelnabi, S., et al. (2023). "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"
4. Leveson, N. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety*
5. NIST SP 800-53 Rev. 5 — SI-7: Software, Firmware, and Information Integrity

---

*Class 09 | AI Security from Scratch*
