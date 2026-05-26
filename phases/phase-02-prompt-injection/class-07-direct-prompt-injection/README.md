# Direct Prompt Injection

> **Module:** Phase 2 — Prompt Injection | **Class:** 07 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Define direct prompt injection and distinguish it from indirect injection and jailbreaking
2. Demonstrate how adversarial user input overrides system instructions in an LLM-based application
3. Analyze direct prompt injection as a controller hijacking attack through the observation channel
4. Implement input classification and instruction hierarchy enforcement as defensive controls
5. Write security regression tests that detect direct injection attacks against a chatbot

---

## Control-Theoretic View

Every class in this curriculum models a security concept as a control loop. This section defines the control-theoretic framing for direct prompt injection.

### Objective

The safety goal the system must maintain:

> Ensure that user-supplied input is never interpreted as system-level instructions, and that the system prompt remains the authoritative control reference for all model decisions.

### Controller

The component responsible for making decisions to maintain the objective:

> The instruction hierarchy enforcer — a middleware layer that classifies every input token by origin (system, user, assistant, tool) and enforces precedence rules so that user-originated content can never override system-originated instructions.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Input token classification (user vs. system vs. tool) | Input parser | Per request |
| Instruction-following fidelity score | Output classifier | Per response |
| System prompt integrity hash | Configuration store | Per request |
| Conversation turn count | Session manager | Per request |
| Output content category (safe / policy-violating / instruction-leaking) | Output classifier | Per response |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Block request | Prevents user input from reaching the model | Input classified as adversarial |
| Sanitize input | Strips instruction-like patterns from user input | Instruction-like content detected in user input |
| Inject reminder | Prepends a system-prompt reinforcement before user input | Instruction-following fidelity drops below threshold |
| Escalate to human | Routes conversation to a human operator | Repeated adversarial patterns detected |
| Terminate session | Ends the conversation entirely | Controller determines session is irrecoverably compromised |

### Feedback

How the controller learns whether its actions achieved the objective:

> Post-generation output classification confirms whether the model followed system instructions or was diverted by user input. If output analysis reveals instruction override, the event is logged and the classification model is updated. Trend analysis on injection success rate feeds back into the input classification thresholds.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Adversarial user input containing override instructions | Malicious user | Input classification + instruction hierarchy |
| Social engineering prompts ("ignore previous instructions") | Malicious user | Pattern detection + reinforcement reminders |
| Multi-turn gradual manipulation | Patient adversary | Conversation-level anomaly detection |
| Encoding tricks (Unicode, base64, markdown) | Technical attacker | Input normalization before classification |
| Context-window stuffing to push out system prompt | Technical attacker | System prompt pinning + context management |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Controller hijacked | Model follows user-originated instructions over system prompt | Attacker controls model behavior |
| Policy bypass | Model produces output that violates safety policy | Harmful content reaches users |
| Instruction leakage | Model reveals system prompt contents in response | Attacker gains intelligence for targeted attacks |
| Tool misuse | Model calls tools based on injected instructions | Unauthorized actions executed |
| Privilege escalation | Model grants user elevated capabilities via injection | Access control violated |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> An output validation layer that independently classifies every model response against safety policies, regardless of whether the instruction hierarchy enforcer approved the input. This layer can block, redact, or replace responses that violate policy even if the primary controller was bypassed. Additionally, a circuit breaker that tracks injection-attempt rates per session and per user, automatically escalating to a human review queue when the rate exceeds a configurable threshold.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Injection attempt rate (per session) | > 3 attempts in 5 minutes | Warning to session monitor |
| Instruction override success rate | > 0% over any rolling 1-hour window | Critical alert to security team |
| System prompt integrity violations | Any violation detected | Immediate critical alert |
| Input classifier confidence drop | Average confidence < 0.7 over 100 requests | Warning to ML ops team |
| Output policy violation rate | > 0.5% of responses | Warning to content safety team |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Immediately block the offending user session and preserve conversation logs for forensic analysis
2. Reset the system prompt integrity hash and verify no configuration drift has occurred
3. Replay the attack through the classification pipeline to determine why it was not detected
4. Update input classification rules and/or instruction hierarchy enforcement logic based on findings
5. Run the full security regression test suite to confirm the fix and verify no regressions
6. Generate an incident report documenting the attack, the failure, the fix, and the evidence

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 7a | Attacking the Class-06 Chatbot | 45 minutes |
| Lab 7b | Building an Instruction Hierarchy Enforcer | 60 minutes |
| Lab 7c | Regression Testing Against Injection | 30 minutes |

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

- [ ] Completed lab worksheet with control-loop analysis of direct prompt injection
- [ ] Working instruction hierarchy enforcer that blocks the provided attack payloads
- [ ] Passing security regression test suite (minimum 5 test cases covering direct injection variants)
- [ ] Written explanation of the controller hijacking failure mode and remediation
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

- Completion of Class 06: Build Your First Vulnerable AI Assistant
- Familiarity with Python, pytest, and basic LLM API usage
- Working development environment (see setup guide)
- Understanding of the control-loop model from Phase 1

---

## References

1. OWASP Top 10 for LLM Applications (2025) — LLM01: Prompt Injection
2. Greshake, K., et al. (2023). "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"
3. NIST AI Risk Management Framework (AI RMF 1.0)
4. Leveson, N. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety*
5. Perrig, A., et al. (2024). "Attack and Defense Perspectives on Prompt Injection"

---

*Class 07 | AI Security from Scratch*
