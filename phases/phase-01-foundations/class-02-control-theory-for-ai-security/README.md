# Control Theory for AI Security

> **Module:** Phase 1 — Foundations | **Class:** 02 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Define and explain the core control theory concepts: feedback loops, controllers, plants, disturbances, reference signals, and error signals
2. Map each control theory concept to its AI system analog with concrete examples
3. Explain the difference between open-loop and closed-loop control and why closed-loop is essential for AI safety
4. Describe supervisory control as a control-theoretic concept and explain why it is the right frame for AI safety
5. Analyze an AI system's stability properties using control-theoretic concepts (time constants, damping, oscillation)

---

## Control-Theoretic View

### Objective

The safety goal the system must maintain:

> Ensure that the AI system's output converges to the reference signal (safe, intended behavior) despite disturbances (adversarial inputs), with bounded error and stable dynamics.

### Controller

The component responsible for making decisions to maintain the objective:

> The supervisory control layer monitors the AI model's behavior and applies corrective actions when the system deviates from the reference trajectory, ensuring bounded error and stable convergence.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Deviation from expected behavior | Behavioral classifier | Per request |
| Tool call parameter validity | Tool mediation layer | Per tool call |
| Context window composition | Context analyzer | Per request |
| Policy compliance score | Policy engine | Per request |
| Historical violation trend | Control ledger | Continuous |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Inject corrective context | Reorient the model toward safe behavior | Behavioral deviation detected |
| Block request/response | Prevent unsafe output from reaching user | Policy violation detected |
| Throttle processing rate | Prevent cascade failures | Anomaly threshold exceeded |
| Reset conversation state | Return system to known-safe initial conditions | State contamination detected |
| Activate fallback model | Switch to a simpler, more constrained model | Primary model instability detected |

### Feedback

How the controller learns whether its actions achieved the objective:

> Post-action behavioral classification compares the system's trajectory after intervention against the expected convergence path. If the corrective action reduced the deviation, the control gain is validated. If the deviation persists or grows, the control strategy is escalated — moving from corrective context injection to blocking to system reset, mirroring the gain-scheduling approach in adaptive control.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Adversarial prompt injection | Untrusted user input | Input classification + context separation |
| Poisoned retrieval results | Compromised knowledge base | Document provenance validation |
| Manipulated tool responses | Compromised external APIs | Response validation + sandboxing |
| State contamination from prior turns | Polluted conversation history | State isolation + memory quarantine |
| Model degradation under load | Infrastructure pressure | Rate limiting + circuit breakers |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Divergent behavior | Error signal grows instead of shrinking | Progressive loss of safety constraints |
| Oscillatory behavior | System alternates between safe and unsafe | Intermittent policy violations |
| Steady-state error | System converges to wrong reference | Consistent subtle policy violations |
| Controller saturation | Supervisory controls overwhelmed | Effective open-loop operation |
| Instability cascade | One failure triggers another in a chain | System-wide safety breakdown |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> A two-level supervisory hierarchy: (1) a local supervisory controller that monitors and corrects individual requests in real-time, and (2) a global supervisory controller that monitors aggregate system behavior, adjusts control parameters (thresholds, gains, policies), and activates safety fallbacks (circuit breakers, kill switches) when the local controller cannot maintain stability.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Average behavioral deviation score | > 0.3 (warning), > 0.6 (critical) | Control gain adjustment / Circuit breaker |
| Policy violation rate (5-min window) | > 2% / > 5% | Security team escalation |
| Tool call rejection rate | > 5% / > 15% | Tool access review / Tool suspension |
| Conversation reset rate | > 1% / > 5% | Model stability review |
| Time-to-convergence trend | Increasing over 30-min window | Control parameter tuning trigger |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Identify the type of instability (divergence, oscillation, saturation, cascade)
2. Apply the corresponding stabilization action (reset, throttle, shed load, isolate)
3. Verify that the system has returned to a stable operating point by running a known-safe test
4. Update control parameters based on the failure analysis (adjust thresholds, refine classifiers)
5. Generate assurance evidence documenting the instability, the stabilization action, and the verification

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 2.1 | Build an open-loop AI controller and observe its failure modes | 30 min |
| Lab 2.2 | Add feedback and close the loop — observe convergence | 30 min |
| Lab 2.3 | Add supervisory control — observe bounded error under disturbance | 45 min |

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

- [ ] Completed lab worksheets with control-loop diagrams for open-loop, closed-loop, and supervised configurations
- [ ] Written analysis of stability properties for each configuration (200+ words)
- [ ] Comparison table mapping all 6 core control theory concepts to AI security analogs
- [ ] Passing security regression test suite for Lab 2.3
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
- Working development environment (Python 3.11+, Docker, make)
- Basic familiarity with the control-loop model from Class 01

---

## References

1. Åström, K.J. & Murray, R.M. (2021). *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd ed. Princeton University Press.
2. Leveson, N. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press.
3. framework/03-supervisory-controls.md — AI Security from Scratch internal framework document.
4. NIST SP 800-53 Rev. 5 — Security and Privacy Controls for Information Systems.
5. IEC 61508 — Functional Safety of Electrical/Electronic/Programmable Electronic Safety-Related Systems.

---

*Class 02 | AI Security from Scratch | Phase 1 — Foundations*
