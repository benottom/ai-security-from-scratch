# AI Security as an Engineering Discipline

> **Module:** Phase 1 — Foundations | **Class:** 01 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Define AI security as the discipline of ensuring that an AI system's behavior remains within defined safe bounds under adversarial conditions
2. Explain why AI systems are fundamentally control systems and map AI components to control-theoretic elements (controller, plant, disturbance)
3. Identify the three load-bearing concepts of AI security: behavior, safe bounds, and adversarial disturbances
4. Articulate why "secure the model" is insufficient and why "secure the control loop" is the necessary paradigm
5. Recognize the analogy between classical control-theory failure modes and AI security failures (sensor failure ↔ observation corruption, controller compromise ↔ reasoning manipulation, actuator failure ↔ unsafe actuation)

---

## Control-Theoretic View

Every class in this curriculum models a security concept as a control loop. This section defines the control-theoretic framing for the topic covered in this class.

### Objective

The safety goal the system must maintain:

> Ensure that every AI system output remains within explicitly defined safe bounds, even when the system receives adversarial inputs designed to push it outside those bounds.

### Controller

The component responsible for making decisions to maintain the objective:

> The supervisory control layer — external, deterministic, and auditable mechanisms that monitor and constrain the AI model's behavior, independent of the model's own reasoning.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Input classification result | Input validation service | Per request |
| Output content category | Output classifier | Per request |
| Tool call intent and parameters | Tool mediation layer | Per tool call |
| Conversation anomaly score | Behavioral monitor | Per turn |
| Policy violation rate | Control ledger | Continuous |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Block input | Prevent adversarial input from reaching the model | Input classified as suspicious |
| Redact output | Remove PII, secrets, or policy-violating content from output | Output scanner detects violation |
| Reject tool call | Cancel a dangerous tool invocation before execution | Tool call fails parameter validation |
| Escalate to human | Route request to human operator for review | Anomaly score exceeds threshold |
| Activate circuit breaker | Halt all processing until safety is confirmed | Violation rate exceeds critical threshold |

### Feedback

How the controller learns whether its actions achieved the objective:

> Post-incident analysis feeds back into policy rules, classification models, and threshold configurations. The control ledger records every decision, enabling audit trails that inform control updates and assurance evidence generation.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Direct prompt injection | Malicious user input | Input validation and classification |
| Indirect prompt injection | Poisoned retrieval documents | Document provenance validation |
| Context window manipulation | Oversized inputs designed to drown system prompt | Context budget enforcement |
| Tool result spoofing | Compromised external APIs | Result validation and sandboxing |
| Memory poisoning | Long-term conversation state | Memory quarantine and isolation |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| System prompt leaked | Model output contains internal instructions | Attacker gains intelligence for further exploitation |
| Unauthorized action executed | Tool called without proper authorization | Data exfiltration, system compromise |
| PII exposed in output | Output contains personally identifiable information | Privacy violation, regulatory penalty |
| Policy-violating content generated | Model produces harmful or disallowed content | Reputational damage, user harm |
| Adversarial control achieved | Attacker's instructions override system behavior | Full system compromise |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> A layered supervisory architecture: (1) an AI security gateway that inspects all inputs and outputs, (2) a tool call mediation layer that validates and gates all tool invocations, and (3) a control ledger that records every decision for audit and analysis. Each layer operates independently and can override the model unilaterally.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Prompt injection detection rate | > 5% of requests flagged | Security team notification |
| Policy violation rate | > 1% of outputs | Circuit breaker activation warning |
| Tool call rejection rate | > 2% of tool calls | Tool access review |
| System prompt leakage attempts | Any detected | Immediate escalation |
| Anomaly score trend | Rising over 10-minute window | Behavioral analysis trigger |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Halt the affected conversation session and preserve all context for forensic analysis
2. Evaluate whether the violation was contained or whether side effects (e.g., unauthorized tool calls) require remediation
3. Update supervisory control rules to address the specific attack pattern that succeeded
4. Run security regression tests to verify the control update is effective and does not introduce regressions
5. Generate assurance evidence documenting the incident, remediation, and verification

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 1.1 | Observe an unprotected chatbot under adversarial input | 30 min |
| Lab 1.2 | Map the chatbot's control-loop elements and identify missing controls | 30 min |
| Lab 1.3 | Add a single supervisory control and measure the improvement | 45 min |

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

- [ ] Completed lab worksheet with control-loop analysis for the unprotected chatbot
- [ ] Written comparison of "secure the model" vs. "secure the control loop" approaches (300+ words)
- [ ] Diagram mapping at least 3 AI failure scenarios to control-theory analogs
- [ ] Passing security regression test suite for Lab 1.3
- [ ] Evidence artifacts from `make evidence`

---

## Estimated Time

| Activity | Duration |
|---|---|
| Lecture / Reading | 1.5 hours |
| Lab Work | 1.5 hours |
| Exercises | 0.5 hours |
| Review & Deliverables | 0.5 hours |
| **Total** | **4 hours** |

---

## Prerequisites

- Familiarity with basic AI/ML concepts (what a language model is, what it does)
- Working development environment (Python 3.11+, Docker, make)
- No prior security or control theory knowledge required — this is the starting point

---

## References

1. Leveson, N. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press.
2. NIST AI Risk Management Framework (AI RMF 1.0), January 2023.
3. OWASP Top 10 for LLM Applications (2025 Edition).
4. Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control*. Viking.
5. framework/01-ai-security-as-control.md — AI Security from Scratch internal framework document.

---

*Class 01 | AI Security from Scratch | Phase 1 — Foundations*
