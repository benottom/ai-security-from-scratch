# Threat Modeling AI Systems

> **Module:** Phase 1 — Foundations | **Class:** 04 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Apply the control-loop threat model to decompose AI systems into trust boundaries and identify threats at each boundary
2. Adapt the STRIDE threat classification framework for AI-specific threats, including prompt injection, indirect injection, and tool misuse
3. Draw and interpret attack trees for AI system threats, including multi-step and multi-vector attack chains
4. Identify trust boundaries in AI system architectures and determine what crosses each boundary
5. Complete a full threat model for a customer support chatbot, from system description to residual risk analysis

---

## Control-Theoretic View

### Objective

The safety goal the system must maintain:

> Ensure that all identified threats to the AI system's control loop are systematically cataloged, assessed, and mitigated — with no critical threat left without a corresponding control or accepted residual risk.

### Controller

The component responsible for making decisions to maintain the objective:

> The threat modeling process itself, guided by the control-loop decomposition, STRIDE-AI classification, and attack tree analysis — producing a living threat model document that drives control selection, test design, and monitoring configuration.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Threat catalog completeness | Threat model review | Per review cycle |
| Control coverage ratio | Control mapping analysis | Per review cycle |
| Attack tree depth and breadth | Attack tree review | Per review cycle |
| Trust boundary correctness | Architecture review | Per design change |
| Residual risk acceptance decisions | Risk register | Per threat |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Add threat to catalog | Ensure threat is tracked and addressed | Threat identified during analysis |
| Map control to threat | Ensure threat has mitigation | Control available or planned |
| Escalate residual risk | Ensure leadership awareness | Risk exceeds acceptance threshold |
| Update attack tree | Document new attack path | New attack vector discovered |
| Trigger control implementation | Address threat with new control | Threat has no adequate mitigation |

### Feedback

How the controller learns whether its actions achieved the objective:

> Each threat model review produces metrics: number of threats identified, percentage with controls, number of accepted residual risks, and attack tree coverage. Trends in these metrics indicate whether the threat modeling process is improving or degrading. Security incidents that exploit unmodeled threats feed back into the threat model as gaps to be addressed.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Novel attack techniques not in STRIDE-AI | Evolving threat landscape | Regular threat model updates + threat intelligence |
| System architecture changes | Feature development | Threat model as part of design review |
| Incomplete threat identification | Cognitive bias, time pressure | Structured methodology + peer review |
| Control drift | Operational changes | Periodic control validation |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Incomplete threat catalog | Threats not identified | Unknown attack surface |
| Unmapped controls | Threats without mitigations | Unmitigated risk |
| Stale threat model | Model does not reflect current architecture | False security confidence |
| Unchallenged assumptions | Trust boundaries drawn incorrectly | Hidden attack paths |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> Threat model peer review, security architecture review board, and incident-driven threat model updates serve as supervisory controls over the threat modeling process. They ensure the threat model remains accurate, complete, and actionable.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Threats without controls | > 0 critical, > 3 high | Security review |
| Threat model age | > 90 days without review | Mandatory review |
| Architecture changes without threat model update | Any | Design review hold |
| Incidents exploiting unmodeled threats | Any | Emergency threat model update |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Identify the gap in the threat model (missed threat, incorrect trust boundary, stale model)
2. Update the threat model with the new information
3. Assess whether existing controls address the newly identified threat
4. If not, design and implement new controls
5. Run security regression tests to verify the new controls
6. Generate assurance evidence documenting the threat model update

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 4.1 | Threat model a simple chatbot using control-loop decomposition | 25 min |
| Lab 4.2 | Apply STRIDE-AI to a RAG system | 30 min |
| Lab 4.3 | Build an attack tree for an agent system | 30 min |
| Lab 4.4 | Complete threat model for a customer support chatbot | 35 min |

Each lab follows the standard 8-step flow.

---

## Deliverables

- [ ] Completed threat model for a customer support chatbot (STRIDE-AI table, trust boundary diagram, attack tree)
- [ ] Attack tree diagram with at least 3 levels of depth and 2 attack paths
- [ ] Control mapping table showing each threat, its control, and the control type
- [ ] Written analysis of why trust boundaries are the most important concept in AI threat modeling (200+ words)
- [ ] Evidence artifacts from `make evidence`

---

## Estimated Time

| Activity | Duration |
|---|---|
| Lecture / Reading | 1.5 hours |
| Lab Work | 2 hours |
| Review & Deliverables | 0.5 hours |
| **Total** | **4 hours** |

---

## Prerequisites

- Completion of Class 01: AI Security as an Engineering Discipline
- Completion of Class 02: Control Theory for AI Security
- Completion of Class 03: AI Systems as Adversarial Control Loops
- Working development environment (Python 3.11+, Docker, make)

---

## References

1. Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley.
2. OWASP Top 10 for LLM Applications (2025 Edition)
3. framework/02-control-loop-threat-model.md — AI Security from Scratch internal framework
4. Microsoft STRIDE Threat Modeling Framework
5. Greshake, K. et al. (2023). "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." AISec Workshop.

---

*Class 04 | AI Security from Scratch | Phase 1 — Foundations*
