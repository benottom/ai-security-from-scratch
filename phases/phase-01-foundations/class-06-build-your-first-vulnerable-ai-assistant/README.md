# Build Your First Vulnerable AI Assistant

> **Module:** Phase 1 — Foundations | **Class:** 06 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Build a simple AI chatbot using FastAPI with LLM integration — with no security controls
2. Demonstrate prompt injection attacks against the vulnerable chatbot and observe their success
3. Identify the specific control-loop failures that make the chatbot vulnerable
4. Explain why each vulnerability exists in terms of the control-theoretic framework from Classes 01-05
5. Propose and prioritize specific security controls to address each vulnerability

---

## Control-Theoretic View

### Objective

The safety goal the system must maintain:

> Ensure that the AI assistant's behavior remains within defined safe bounds — never revealing internal instructions, never producing harmful content, and never executing unauthorized actions — even under adversarial input.

### Controller

The component responsible for making decisions to maintain the objective:

> **Current state (vulnerable):** The LLM itself is both the primary controller and the only controller — there is no supervisory layer. The system prompt is the only safety mechanism, and it is inside the controller where it can be overridden. This is an open-loop system with respect to safety.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| User message | API request | Per request |
| System prompt | Configuration | Per request |
| Conversation history | Session store | Per request |

**Critical gap:** No safety observations. The system does not classify inputs, does not classify outputs, and does not monitor behavior. It is blind to its own safety state.

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Generate text | Output delivered directly to user | None — no preconditions, no validation |

**Critical gap:** No safety actions. The system cannot block, modify, or halt output. It can only generate text and deliver it. This is the definition of an open-loop controller.

### Feedback

How the controller learns whether its actions achieved the objective:

> **Current state (vulnerable):** There is no safety feedback. The system has no mechanism to determine whether its output complies with safety requirements. No error signal is computed. No corrective action is possible. The loop is open.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Current Mitigation |
|---|---|---|
| Direct prompt injection | User input | None — system prompt is inside the controller |
| Multi-turn manipulation | User across turns | None — no behavioral monitoring |
| Context overflow | Long inputs | None — no input length limits |
| Encoding evasion | Obfuscated inputs | None — no input normalization |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Model follows attacker instructions | Successful injection | Arbitrary behavior under attacker control |
| System prompt leaked | Extraction attack | IP exposure, attack facilitation |
| Harmful content produced | Jailbreak | Offensive or dangerous output |
| Open-loop operation | No supervisory controls | All attacks succeed |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> **Current state (vulnerable):** None. The system has zero supervisory controls. There is no input validation, no output classification, no behavioral monitoring, no circuit breaker, and no kill switch. The LLM operates as an unsupervised controller with full authority and zero constraints.

### Monitoring

Ongoing observability for the control loop:

> **Current state (vulnerable):** None. The system logs requests for debugging but does not compute any safety metrics. There is no violation rate tracking, no anomaly detection, and no alerting.

### Recovery

Procedures for restoring the system to a safe state after a violation:

> **Current state (vulnerable):** Manual only. If a violation is discovered, a developer must manually restart the service, update the system prompt, or take the system offline. There are no automated recovery procedures.

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 6.1 | Build the vulnerable chatbot from scratch | 30 min |
| Lab 6.2 | Attack the chatbot with prompt injection techniques | 30 min |
| Lab 6.3 | Analyze the control-loop failures | 20 min |
| Lab 6.4 | Design and propose security controls | 20 min |

Each lab follows the standard 8-step flow.

---

## Deliverables

- [ ] Working FastAPI chatbot application (vulnerable version)
- [ ] Attack report documenting at least 5 successful prompt injection techniques
- [ ] Control-loop failure analysis mapping each vulnerability to a control-theoretic concept
- [ ] Proposed security control design with priority ranking
- [ ] Evidence artifacts from `make evidence`

---

## Estimated Time

| Activity | Duration |
|---|---|
| Lecture / Reading | 1 hour |
| Lab Work (Build + Attack) | 1.5 hours |
| Analysis + Design | 1 hour |
| Review & Deliverables | 0.5 hours |
| **Total** | **4 hours** |

---

## Prerequisites

- Completion of Classes 01-05
- Working development environment (Python 3.11+, Docker, make)
- Basic Python and FastAPI familiarity
- OpenAI API key or local model access

---

## References

1. Willison, S. (2023). "Prompt injection attacks against LLM applications." simonwillison.net.
2. OWASP Top 10 for LLM Applications (2025 Edition)
3. Greshake, K. et al. (2023). "Not What You've Signed Up For." AISec Workshop.
4. framework/02-control-loop-threat-model.md — AI Security from Scratch internal framework
5. FastAPI documentation — https://fastapi.tiangolo.com/

---

*Class 06 | AI Security from Scratch | Phase 1 — Foundations*
