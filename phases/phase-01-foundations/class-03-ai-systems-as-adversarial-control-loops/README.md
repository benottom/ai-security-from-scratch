# AI Systems as Adversarial Control Loops

> **Module:** Phase 1 — Foundations | **Class:** 03 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Decompose real AI systems (chatbot, RAG, agent) into their constituent control-loop elements
2. Identify the controller, plant, observations, actions, feedback, and disturbances for each system type
3. Map where disturbances enter each system type and trace their propagation through the control loop
4. Draw accurate Mermaid diagrams for chatbot, RAG, and agent control loops
5. Explain why each system type has a different attack surface and requires different supervisory controls

---

## Control-Theoretic View

### Objective

The safety goal the system must maintain:

> Ensure that AI system behavior remains within defined safe bounds across all system types — from simple chatbots to complex agents — with supervisory controls appropriate to each system's control-loop structure and attack surface.

### Controller

The component responsible for making decisions to maintain the objective:

> A system-type-specific supervisory control architecture: input/output gates for chatbots, retrieval validators for RAG systems, and tool mediators with approval gates for agents. Each architecture is tailored to the control-loop structure of the system it protects.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Input classification | Input validator | Per request |
| Retrieval content classification | Document validator | Per retrieval |
| Tool call intent and parameters | Tool mediator | Per tool call |
| Output safety classification | Output scanner | Per request |
| Behavioral anomaly score | Session monitor | Per turn |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Block input | Prevent adversarial input from reaching model | Input classified as injection |
| Sanitize retrieval | Remove instruction-like content from documents | Document contains injection patterns |
| Reject tool call | Cancel dangerous tool invocation | Tool call fails validation |
| Block output | Prevent unsafe output from reaching user | Output classified as violation |
| Activate circuit breaker | Halt processing temporarily | Aggregate violation threshold exceeded |

### Feedback

How the controller learns whether its actions achieved the objective:

> Each control action produces an entry in the control ledger. The ledger feeds into behavioral monitors that detect patterns across requests, sessions, and time windows. Trends in violation rates, rejection rates, and anomaly scores provide feedback for adjusting control parameters and thresholds.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Prompt injection via user input | Untrusted user | Input validation |
| Indirect injection via retrieved content | Compromised knowledge base | Document validation + context separation |
| Tool result injection | Compromised API | Result validation + sandboxing |
| Memory/state poisoning | Polluted session history | Memory quarantine |
| Tool parameter manipulation | Adversarial reasoning by model | Parameter validation + approval gates |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Model follows attacker instructions | Successful injection (direct or indirect) | Arbitrary behavior under attacker control |
| Unauthorized data access | Model retrieves data user shouldn't see | Information disclosure |
| Unauthorized action executed | Tool called without proper authorization | Real-world harm (data loss, financial damage) |
| Cross-session contamination | Memory poisoning propagates across sessions | Persistent compromise |
| Privilege escalation | Model uses low-privilege tool to gain high privilege | Expanded attack surface |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> Three-tier supervisory architecture: (1) local controls at each interface (input gate, retrieval validator, tool mediator, output gate), (2) session-level behavioral monitoring, and (3) system-level circuit breakers and kill switches. The architecture scales with system complexity — chatbots need fewer controls than RAG systems, which need fewer than agents.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Injection detection rate (by type) | > 3% of inputs | Security review |
| Retrieval anomaly rate | > 1% of retrievals | Knowledge base audit |
| Tool call rejection rate | > 2% / > 10% | Tool access review / Tool suspension |
| Output violation rate | > 1% / > 5% | Security team / Circuit breaker |
| Cross-session contamination indicators | Any detected | Immediate investigation |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Identify which system type and which control-loop stage was compromised
2. Isolate the affected component (session reset, tool suspension, retrieval disable)
3. Assess the blast radius — did the compromise propagate to other components?
4. Apply targeted remediation based on the attack vector (update input rules, sanitize knowledge base, revoke tool access)
5. Run security regression tests specific to the affected system type
6. Generate assurance evidence and update the threat model

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 3.1 | Decompose and diagram a chatbot control loop | 20 min |
| Lab 3.2 | Decompose and diagram a RAG system control loop | 25 min |
| Lab 3.3 | Decompose and diagram an agent control loop | 30 min |
| Lab 3.4 | Trace a disturbance through all three system types | 30 min |

Each lab follows the standard 8-step flow.

---

## Deliverables

- [ ] Three Mermaid control-loop diagrams (chatbot, RAG, agent) with all elements labeled
- [ ] Disturbance trace document showing how a single attack propagates through each system type
- [ ] Comparison table of attack surfaces across the three system types
- [ ] Written analysis of why agents require more supervisory controls than chatbots (200+ words)
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

- Completion of Class 01: AI Security as an Engineering Discipline
- Completion of Class 02: Control Theory for AI Security
- Working development environment (Python 3.11+, Docker, make)

---

## References

1. framework/01-ai-security-as-control.md — AI Security from Scratch internal framework
2. framework/02-control-loop-threat-model.md — AI Security from Scratch internal framework
3. OWASP Top 10 for LLM Applications (2025 Edition)
4. Greshake, K. et al. (2023). "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." AISec Workshop.
5. Leveson, N. (2011). *Engineering a Safer World*. MIT Press.

---

*Class 03 | AI Security from Scratch | Phase 1 — Foundations*
